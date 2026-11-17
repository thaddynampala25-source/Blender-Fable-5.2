"""Build a Language Buddy's web model from a template GLB, in Blender, on a copy (the source is never changed).

    blender -b --python w2s-site/buddy-gen/build_buddy.py -- <src.glb> <out.glb> <name> [--tris N] [--tex PX] [--dump DIR] [--edit EDIT.py]

Steps
1. Optimise: merge split vertices, decimate to a web budget, feet on y = 0, centred, 2.2 units tall.
2. Texel map: bake, for every texture pixel, the 3D position and normal behind it (so texture edits
   and landmark detection can work in model space).
3. Landmarks: find the painted eyes (sclera) and the mouth, for the runtime's face cards.
4. Optional texture edit (EDIT.py defines edit(tex, pos, nor, info) -> tex), e.g. May's recolours.
5. Minimal skeleton: Hips, Spine, Head, with weights computed from body regions (not automatic
   weights): the head and everything above the neck follows Head with a soft blend over the
   neck; the chest follows Spine; the rest stays on Hips. Enough for breathing, posture shifts,
   nods, tilts and turns. No arm bones: arms, hair and clothes are fused in these templates.
6. Export GLB with scene extras {"w2s": {height, faceWidth, face: {...}}}.
"""
import math
import os
import sys
import numpy as np
import bpy
from mathutils import Vector

A = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT, NAME = A[0], A[1], A[2]
def opt(flag, default, cast=str):
    return cast(A[A.index(flag) + 1]) if flag in A else default
TRIS = opt("--tris", 70000, int)
TEX = opt("--tex", 2048, int)
DUMP = opt("--dump", None)
EDIT = opt("--edit", None)
HEIGHT = 2.2


def log(*a):
    print("BUDDY", *a, flush=True)


# ---------------------------------------------------------------- 1. optimise
bpy.ops.wm.read_homefile(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
ob = [o for o in bpy.data.objects if o.type == "MESH"][0]
bpy.context.view_layer.objects.active = ob; ob.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
me = ob.data
before = len(me.polygons)
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.mesh.remove_doubles(threshold=0.00001); bpy.ops.object.mode_set(mode="OBJECT")
if before > TRIS:
    d = ob.modifiers.new("decimate", "DECIMATE"); d.decimate_type = "COLLAPSE"
    d.ratio = TRIS / before; d.use_collapse_triangulate = True
    bpy.ops.object.modifier_apply(modifier=d.name)
bb = [Vector(c) for c in ob.bound_box]
lo = Vector((min(v.x for v in bb), min(v.y for v in bb), min(v.z for v in bb)))
hi = Vector((max(v.x for v in bb), max(v.y for v in bb), max(v.z for v in bb)))
s = HEIGHT / (hi.z - lo.z)
for v in me.vertices:
    v.co = Vector(((v.co.x - (lo.x + hi.x) / 2) * s, (v.co.y - (lo.y + hi.y) / 2) * s, (v.co.z - lo.z) * s))
me.update()
for p in me.polygons:
    p.use_smooth = True
ob.name = me.name = NAME
mat = me.materials[0]; mat.name = NAME
nt = mat.node_tree
tex_node = next(n for n in nt.nodes if n.type == "TEX_IMAGE")
img = tex_node.image
if max(img.size) != TEX:
    img.scale(TEX, TEX)
log("tris", before, "->", len(me.polygons), "verts", len(me.vertices))

# ---------------------------------------------------------------- 2. texel map (bake position and normal)
sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.samples = 1; sc.cycles.device = "CPU"
sc.render.bake.margin = 4


def bake(socket_name):
    out = bpy.data.images.new("bake_" + socket_name, TEX, TEX, float_buffer=True, alpha=False)
    out.colorspace_settings.name = "Non-Color"
    geo = nt.nodes.new("ShaderNodeNewGeometry"); em = nt.nodes.new("ShaderNodeEmission")
    tgt = nt.nodes.new("ShaderNodeTexImage"); tgt.image = out
    mo = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    old = [l.from_socket for l in mo.inputs["Surface"].links]
    nt.links.new(geo.outputs[socket_name], em.inputs["Color"]); nt.links.new(em.outputs[0], mo.inputs["Surface"])
    nt.nodes.active = tgt
    bpy.ops.object.bake(type="EMIT", use_clear=True)
    for n in (geo, em, tgt):
        nt.nodes.remove(n)
    if old:
        nt.links.new(old[0], mo.inputs["Surface"])
    a = np.array(out.pixels[:], dtype=np.float32).reshape(TEX, TEX, 4)[..., :3]
    cov = np.array(out.pixels[:], dtype=np.float32).reshape(TEX, TEX, 4)[..., :3]
    bpy.data.images.remove(out)
    return a


pos = bake("Position")              # Blender coordinates: x right, y back (-y is the front), z up
nor = bake("Normal")
covered = np.linalg.norm(nor, axis=2) > 0.5
tex = np.array(img.pixels[:], dtype=np.float32).reshape(TEX, TEX, 4)
log("texel coverage", round(float(covered.mean()), 3))

# ---------------------------------------------------------------- 3. landmarks
rgb = tex[..., :3]
mx = rgb.max(2); mn = rgb.min(2); sat = (mx - mn) / np.maximum(mx, 1e-4)
front = covered & (nor[..., 1] < -0.55)
H = HEIGHT
head = front & (pos[..., 2] > 0.62 * H)
sclera = head & (mx > 0.82) & (sat < 0.12)
info = {"height": H}
eyes = {}
for side, sgn in (("l", 1), ("r", -1)):
    m = sclera & (pos[..., 0] * sgn > 0.01)
    if m.sum() < 30:
        continue
    P = pos[m]
    lo_, hi_ = np.percentile(P, 2, axis=0), np.percentile(P, 98, axis=0)
    eyes[side] = {"center": ((lo_ + hi_) / 2).tolist(), "w": float(hi_[0] - lo_[0]), "h": float(hi_[2] - lo_[2]), "front_y": float(P[:, 1].min())}
info["eyes"] = eyes
if eyes:
    ez = np.mean([e["center"][2] for e in eyes.values()])
    # mouth: the strongest colour change below the nose on the centre line; first guess: the region
    # between the eyes' midline and the chin, centred, where front-facing texels are reddest or whitest
    fy = min(e["front_y"] for e in eyes.values())
    band = front & (np.abs(pos[..., 0]) < 0.12) & (pos[..., 2] < ez - 0.09) & (pos[..., 2] > ez - 0.36) & (pos[..., 1] < fy + 0.06)
    red = (rgb[..., 0] - rgb[..., 2])
    teeth = band & (mx > 0.85) & (sat < 0.12)
    if teeth.sum() > 40:
        P = pos[teeth]; kind = "teeth"
    else:
        # lips: the front-most surface in the band (a pout), i.e. smallest y
        yb = np.where(band, pos[..., 1], 9)
        thr = np.percentile(yb[band], 14)
        P = pos[band & (pos[..., 1] <= thr)]; kind = "lips"
    lo_, hi_ = np.percentile(P, 3, axis=0), np.percentile(P, 97, axis=0)
    info["mouth"] = {"center": ((lo_ + hi_) / 2).tolist(), "w": float(hi_[0] - lo_[0]), "h": float(hi_[2] - lo_[2]), "kind": kind}
log("landmarks", info)

# ---------------------------------------------------------------- 4. texture edit
if EDIT:
    ns = {}
    exec(open(EDIT).read(), ns)
    tex = ns["edit"](tex, pos, nor, covered, info)
    img.pixels.foreach_set(tex.ravel())
    img.update()
# ---------------------------------------------------------------- 4b. face data for the integrated face animation
# (see face_map.py: the eyes' own lash lines slide down to blink; the mouth deforms along the line where the lips part)
import sys as _sys, base64, tempfile
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import face_map
face2, atlas = face_map.build(tex, pos, nor, covered, info)
if face2:
    ah, aw = atlas.shape[:2]
    aimg = bpy.data.images.new(NAME + "_face", aw, ah, alpha=True)
    aimg.pixels.foreach_set(np.flipud(atlas).astype(np.float32).ravel())
    _png = os.path.join(tempfile.mkdtemp(), "face.png"); aimg.filepath_raw = _png; aimg.file_format = "PNG"; aimg.save()
    face2["atlas"] = "data:image/png;base64," + base64.b64encode(open(_png, "rb").read()).decode()
    bpy.data.images.remove(aimg)
    log("face map", aw, "x", ah, "png", os.path.getsize(_png), "mouth", face2.get("mouth"))
if DUMP:
    os.makedirs(DUMP, exist_ok=True)
    np.savez_compressed(os.path.join(DUMP, NAME + "_texels.npz"), pos=pos.astype(np.float16), nor=nor.astype(np.float16), tex=(tex * 255).astype(np.uint8), covered=covered)
img.file_format = "JPEG"

# ---------------------------------------------------------------- 5. skeleton
co = np.array([v.co[:] for v in me.vertices])
def ss(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
ez = np.mean([e["center"][2] for e in eyes.values()]) if eyes else 0.75 * H
neck = (info["mouth"]["center"][2] - 0.13) if "mouth" in info else ez - 0.15 * H   # just under the chin
chest = 0.38 * H
hips = 0.22 * H
arm = bpy.data.armatures.new(NAME + "_rig"); rig = bpy.data.objects.new(NAME + "_rig", arm)
sc.collection.objects.link(rig)
bpy.context.view_layer.objects.active = rig; bpy.ops.object.mode_set(mode="EDIT")
def bone(n, head, tail, parent=None):
    b = arm.edit_bones.new(n); b.head = head; b.tail = tail; b.roll = 0
    if parent:
        b.parent = arm.edit_bones[parent]
    return b
bone("Hips", (0, 0, hips), (0, 0, chest - 0.02))
bone("Spine", (0, 0, chest - 0.02), (0, 0, neck), "Hips")
bone("Head", (0, 0, neck), (0, 0, H), "Spine")
bpy.ops.object.mode_set(mode="OBJECT")
wh = ss(neck - 0.05 * H, neck + 0.025 * H, co[:, 2])           # head and hair above the neck
ws = ss(hips + 0.02 * H, chest, co[:, 2]) * (1 - wh)            # chest and shoulders
wp = np.clip(1 - wh - ws, 0, 1)
for n, w in (("Head", wh), ("Spine", ws), ("Hips", wp)):
    g = ob.vertex_groups.new(name=n)
    for i in np.nonzero(w > 0.001)[0]:
        g.add([int(i)], float(w[i]), "REPLACE")
ob.parent = rig
md = ob.modifiers.new("rig", "ARMATURE"); md.object = rig
log("skeleton neck", round(float(neck), 3), "head verts", int((wh > 0.5).sum()), "spine verts", int((ws > 0.5).sum()))

# ---------------------------------------------------------------- 6. export
fw = float(co[co[:, 2] > 0.55 * H, 0].max() - co[co[:, 2] > 0.55 * H, 0].min())
def gl(p):                                  # Blender (x, y, z) -> glTF (x, z, -y)
    return [round(p[0], 4), round(p[2], 4), round(-p[1], 4)]
face = {}
for k, e in eyes.items():
    face["eye_" + k] = {"c": gl(e["center"]), "w": round(e["w"], 4), "h": round(e["h"], 4)}
if "mouth" in info:
    m = info["mouth"]; face["mouth"] = {"c": gl(m["center"]), "w": round(m["w"], 4), "h": round(m["h"], 4), "kind": m["kind"]}
sc["w2s"] = {"height": HEIGHT, "faceWidth": round(fw * 0.62, 3), "neck": round(float(neck), 3), "face": face, "rig": "w2s-chibi-1"}
if face2:
    sc["w2s"]["face2"] = face2
bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", use_selection=False, export_extras=True,
                          export_image_format="JPEG", export_jpeg_quality=86, export_draco_mesh_compression_enable=False,
                          export_apply=False, export_yup=True, export_texcoords=True, export_normals=True, export_skins=True,
                          export_animations=False)
log("exported", OUT, os.path.getsize(OUT))
