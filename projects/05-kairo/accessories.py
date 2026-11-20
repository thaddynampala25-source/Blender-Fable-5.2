"""Stage 8: accessories (work/kairo_wip.blend -> kairo.blend).

A small silver hoop in his left ear, and a thin silver chain lying on the tee with a
speech-bubble charm: the Week2Speak cast's shared motif.
"""
from pathlib import Path
import math
import numpy as np
import bmesh
import bpy
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

HERE = Path(__file__).resolve().parent
SRC, OUT = HERE / "work" / "kairo_wip.blend", HERE / "kairo.blend"
SILVER = (0.90, 0.90, 0.92)


def silver():
    m = bpy.data.materials.get("Kairo.silver") or bpy.data.materials.new("Kairo.silver")
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*SILVER, 1); b.inputs["Metallic"].default_value = 1.0
    b.inputs["Roughness"].default_value = 0.16
    return m


def torus_into(bm, center, tangent, normal, R, r, stretch=1.0, seg=14, ring=6):
    """Append a (stretched) torus to bm: its long axis along tangent, lying in the tangent/normal plane."""
    t = tangent.normalized(); n = normal.normalized(); b = t.cross(n).normalized(); n = b.cross(t)
    grid = []
    for i in range(seg):
        a = i / seg * 2 * math.pi
        c = center + t * math.cos(a) * R * stretch + n * math.sin(a) * R
        radial = (t * math.cos(a) * stretch + n * math.sin(a)).normalized()
        row = []
        for j in range(ring):
            q = j / ring * 2 * math.pi
            row.append(bm.verts.new(c + radial * math.cos(q) * r + b * math.sin(q) * r))
        grid.append(row)
    for i in range(seg):
        for j in range(ring):
            bm.faces.new((grid[i][j], grid[(i + 1) % seg][j], grid[(i + 1) % seg][(j + 1) % ring], grid[i][(j + 1) % ring]))


def earring(body, mat):
    co = np.array([v.co[:] for v in body.data.vertices])
    gi = body.vertex_groups["ears"].index
    idx = [v.index for v in body.data.vertices if any(g.group == gi and g.weight > 0.5 for g in v.groups) and v.co.x > 0]
    ear = co[idx]
    lobe = Vector(ear[np.argmin(ear[:, 2])])
    bm = bmesh.new()
    torus_into(bm, lobe + Vector((0.002, -0.002, -0.0085)), Vector((0, 0, 1)), Vector((0, 1, 0)), 0.0095, 0.0015, seg=40, ring=10)
    me = bpy.data.meshes.new("Kairo.earring"); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("Kairo.earring", me); bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(mat)


def chain(mat):
    dg = bpy.context.evaluated_depsgraph_get()
    tee = bpy.data.objects["Kairo.tee"]; body = bpy.data.objects["Kairo.body"]
    trees = [BVHTree.FromObject(tee, dg), BVHTree.FromObject(body, dg)]
    neck = Vector((0, 0.0, 1.62))
    # path round the neck: high at the back, dipping to a V on the chest
    path = []
    for k in range(121):
        t = k / 120                                   # 0 and 1 at the front, 0.5 at the back
        a = -math.pi / 2 + t * 2 * math.pi
        front = (math.cos(t * 2 * math.pi) + 1) / 2   # 1 at the front, 0 at the back
        z = 1.635 - 0.115 * front ** 2.2
        o = neck + Vector((math.cos(a), math.sin(a), 0)) * 0.35
        o.z = z
        best = None
        for tr in trees:
            hit, n, _, _ = tr.ray_cast(o, Vector((neck.x, neck.y, z)) - o)
            if hit is not None and (best is None or (hit - o).length < (best[0] - o).length):
                best = (hit, n)
        if best:
            path.append((best[0] + best[1] * 0.0035, best[1]))
    # evenly spaced links
    pts = [p for p, _ in path]; nors = [n for _, n in path]
    L = [0.0]
    for i in range(1, len(pts)):
        L.append(L[-1] + (pts[i] - pts[i - 1]).length)
    step = 0.0058
    bm = bmesh.new()
    k = 0
    d = 0.0
    while d < L[-1]:
        i = max(1, min(len(pts) - 1, int(np.searchsorted(L, d))))
        f = (d - L[i - 1]) / max(1e-6, L[i] - L[i - 1])
        c = pts[i - 1].lerp(pts[i], f); n = nors[i - 1].lerp(nors[i], f)
        tg = (pts[i] - pts[i - 1]).normalized()
        nn = n if k % 2 == 0 else tg.cross(n)          # alternate links turn 90 degrees
        torus_into(bm, c, tg, nn, 0.0024, 0.00075, stretch=1.45, seg=12, ring=5)
        d += step; k += 1
    me = bpy.data.meshes.new("Kairo.chain"); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("Kairo.chain", me); bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(mat)
    # the charm hangs from the lowest point of the chain
    low = min(range(len(pts)), key=lambda i: pts[i].z)
    return pts[low], nors[low]


def charm(at, normal, mat):
    """A speech bubble: rounded rectangle with a tail, 22 x 16 mm, 3 mm thick."""
    w, h, r = 0.022, 0.016, 0.005
    outline = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for k in range(7):
            a = math.radians(a0 + k * 15)
            outline.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
        if a0 == 180:
            # the tail, at the bottom left
            outline += [(-w / 2 + 0.006, -h / 2), (-w / 2 + 0.002, -h / 2 - 0.006), (-w / 2 + 0.011, -h / 2)]
    bm = bmesh.new()
    vs = [bm.verts.new((x, 0, y)) for x, y in outline]
    f = bm.faces.new(vs)
    ex = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in ex["geom"]:
        if isinstance(v, bmesh.types.BMVert):
            v.co.y -= 0.003
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("Kairo.charm"); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("Kairo.charm", me); bpy.context.scene.collection.objects.link(ob)
    bv = ob.modifiers.new("bevel", "BEVEL"); bv.width = 0.0012; bv.segments = 3; bv.limit_method = "ANGLE"
    ob.location = at + normal * 0.002 + Vector((0, 0, -h / 2 - 0.002))
    # face outwards along the chest normal
    ob.rotation_euler = (-normal).to_track_quat("Y", "Z").to_euler()
    me.materials.append(mat)
    # a jump ring joining it to the chain
    bm = bmesh.new(); torus_into(bm, Vector((0, -0.0015, h / 2 + 0.002)), Vector((0, 0, 1)), Vector((1, 0, 0)), 0.0022, 0.0006, seg=16, ring=6)
    rme = bpy.data.meshes.new("Kairo.charm.ring"); bm.to_mesh(rme); bm.free()
    ring = bpy.data.objects.new("Kairo.charm.ring", rme); bpy.context.scene.collection.objects.link(ring)
    ring.parent = ob; rme.materials.append(mat)


bpy.ops.wm.open_mainfile(filepath=str(SRC))
with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
    m = silver()
    earring(bpy.data.objects["Kairo.body"], m)
    at, n = chain(m)
    charm(at, n, m)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True, relative_remap=True)
    print("accessories done")
