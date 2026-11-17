"""Stage 5: Kairo's locs (work/dressed.blend -> work/hair.blend).

Each loc is grown as a strand from a root on the scalp: it leaves along the scalp normal,
bends under gravity, and is kept off the head and shoulders by collision against the body.
Front locs part to the sides so the face stays clear, except a few that fall across his left
eye. The upper locs are gathered into a half-bun at the back of the crown.

Geometry nodes turn the strands into twisted ropes with rounded tips and store "t"
(0 at the root, 1 at the tip) for the shader's dark-brown-to-honey-gold fade.
"""
from pathlib import Path
import math
import random
import numpy as np
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

HERE = Path(__file__).resolve().parent
SRC, OUT = HERE / "work" / "clothes.blend", HERE / "work" / "kairo_wip.blend"
SEED = 7
RADIUS = 0.0168          # loc radius (m): chunky locs (v2: ~1/8 of the head width across)
SPACING = 0.035          # minimum distance between roots
SEG = 0.009              # strand segment length
PART_X = 0.014           # side parting, toward his left
HAIRLINE_Z = None        # set from the eyes in build()


def scalp_samples(body, rng):
    me = body.data
    gi = body.vertex_groups["scalp"].index
    inside = np.zeros(len(me.vertices), bool)
    hairline = HAIRLINE_Z
    for v in me.vertices:
        w = body.matrix_world @ v.co
        on_head = w.z > hairline and abs(w.x) < 0.17
        inside[v.index] = any(g.group == gi and g.weight > 0.3 for g in v.groups) or on_head
    me.calc_loop_triangles()
    tris, areas = [], []
    mw = body.matrix_world
    for t in me.loop_triangles:
        if all(inside[i] for i in t.vertices):
            a, b, c = (mw @ me.vertices[i].co for i in t.vertices)
            tris.append((a, b, c, t.normal.copy()))
            areas.append(t.area)
    areas = np.array(areas); cum = np.cumsum(areas) / areas.sum()
    pts = []
    for _ in range(40000):
        a, b, c, n = tris[int(np.searchsorted(cum, rng.random()))]
        u, v = rng.random(), rng.random()
        if u + v > 1:
            u, v = 1 - u, 1 - v
        p = a + (b - a) * u + (c - a) * v
        sp = SPACING * (0.74 if p.z > HAIRLINE_Z + 0.05 else 1.0)
        if all((p - q).length > sp for q, _ in pts):
            pts.append((p, n))
    return pts


def grow(bvh, root, normal, length, rng, head, mode, bun=None):
    """Return a list of points for one strand."""
    p = root.copy()
    d = normal.normalized()
    side = 1 if root.x > PART_X else -1
    front = root.y < head["front_y"]
    # leave the scalp in the direction the loc will fall, hugging the head rather than standing up
    if mode == "bun":
        fall = (bun - root).normalized()
    elif mode == "fringe":
        fall = Vector((0.75, -0.25, -0.62))
    elif front:
        fall = Vector((side * 1.0, 0.55, -0.35))     # part to the sides and back, away from the face
    else:
        fall = Vector((side * 0.45 * min(1, abs(root.x) / 0.06), 0.55, -0.8))
    fall.normalize()
    tang = (fall - d * fall.dot(d)).normalized()
    d = (tang * 0.9 + d * 0.3).normalized()
    wander = Vector((rng.uniform(-1, 1), rng.uniform(-1, 1), 0)) * 0.035
    p = p - normal.normalized() * RADIUS * 0.6       # sink the root into the scalp
    pts = [p.copy()]
    travelled = 0.0
    tied = False
    lift = head["vol"] * (0.4 + 0.6 * min(1.0, max(0.0, (root.z - head["eye_z"]) / 0.12)))
    while travelled < length:
        t = travelled / length
        if mode == "bun" and not tied:
            to = (bun - p)
            if to.length < 0.02:
                tied = True
                d = Vector((rng.uniform(-0.15, 0.15), 0.35, -1)).normalized()
            else:
                d = (d * 0.75 + to.normalized() * 0.25).normalized()
        elif mode == "bun":
            d = (d * 0.9 + Vector((0, 0.04, -1)) * 0.1).normalized()
        elif mode == "fringe":
            # sweep across the forehead, then fall past the temple and cheek on his left
            target = Vector((0.85, -0.05, -0.5)) if p.z > head["eye_z"] + 0.005 else Vector((0.5, 0.45, -0.75))
            d = (d * 0.75 + target.normalized() * 0.25).normalized()
        else:
            stiff = 0.9 - 0.25 * min(1.0, travelled / 0.06)
            d = (d * stiff + Vector((0, 0, -1)) * (1 - stiff) + Vector((side * 0.03, 0.035, 0)) + wander * math.sin(t * 6.0)).normalized()
        p = p + d * SEG
        travelled += SEG
        # collision with the body: keep the strand a little off the surface; more volume higher up
        off = RADIUS * 0.85 + 0.002 + lift * min(1.0, max(0.0, travelled - 0.03) / 0.12)
        for k, tree in enumerate(bvh):
            o = off if k == 0 else RADIUS + 0.003
            hit, n, _, dist = tree.find_nearest(p)
            if hit is not None:
                inside = (p - hit).dot(n) < 0
                if inside or dist < o:
                    p = hit + n * o
                    d = (d - n * d.dot(n)).normalized() if d.dot(n) < 0 else d
        # keep the face clear (except the locs that are meant to cross it)
        if mode == "down" and head["chin_z"] - 0.03 < p.z < head["brow_z"] + 0.03 and p.y < head["face_y"] and abs(p.x) < head["face_hw"]:
            p.x = math.copysign(head["face_hw"], p.x if abs(p.x) > 1e-4 else side)
        pts.append(p.copy())
    clean = [pts[0]]
    for q in pts[1:]:
        if (q - clean[-1]).length > SEG * 0.5:
            clean.append(q)
    pts = clean
    # smooth out kinks (they flatten the twisted profile into ribbons); keep the root fixed
    for _ in range(8):
        pts = [pts[0]] + [pts[i - 1] * 0.25 + pts[i] * 0.5 + pts[i + 1] * 0.25 for i in range(1, len(pts) - 1)] + [pts[-1]]
    return pts


def bun_coil(center, rng):
    """A half-bun: a few locs coiled round a point at the back of the crown."""
    strands = []
    for k in range(5):
        pts = []
        r0 = 0.018 + 0.006 * k
        turns = 1.2 + 0.25 * k
        ph = rng.random() * 6.28
        n = int(turns * 40)
        for i in range(n + 1):
            a = ph + i / n * turns * 2 * math.pi
            r = r0 * (1 - 0.35 * i / n)
            # coil in a plane facing up and back
            local = Vector((math.cos(a) * r, math.sin(a) * r * 0.7, 0.012 * math.sin(a * 0.5) + 0.004 * k))
            pts.append(center + Vector((local.x, local.y + local.z * 0.6, local.z + 0.01 + 0.006 * k)))
        strands.append(pts)
    return strands


def hair_material():
    m = bpy.data.materials.new("Kairo.locs"); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    at = nt.nodes.new("ShaderNodeAttribute"); at.attribute_name = "t"
    rn = nt.nodes.new("ShaderNodeAttribute"); rn.attribute_name = "rnd"
    # strand-to-strand variation in where the gold starts
    shift = nt.nodes.new("ShaderNodeMath"); shift.operation = "MULTIPLY_ADD"
    shift.inputs[1].default_value = 0.12; nt.links.new(rn.outputs["Fac"], shift.inputs[0]); nt.links.new(at.outputs["Fac"], shift.inputs[2])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); cr = ramp.color_ramp
    cr.elements[0].position = 0.0; cr.elements[0].color = (0.010, 0.0065, 0.0045, 1)
    cr.elements[1].position = 1.15; cr.elements[1].color = (0.40, 0.21, 0.065, 1)
    e = cr.elements.new(0.68); e.color = (0.020, 0.011, 0.0065, 1)
    e = cr.elements.new(0.92); e.color = (0.17, 0.085, 0.028, 1)
    nt.links.new(shift.outputs[0], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.42
    b.inputs["Specular IOR Level"].default_value = 0.55
    b.inputs["Sheen Weight"].default_value = 0.35
    b.inputs["Sheen Roughness"].default_value = 0.4
    b.inputs["Sheen Tint"].default_value = (1.0, 0.8, 0.55, 1)
    b.inputs["Subsurface Weight"].default_value = 0.05
    # fibre texture: fine noise stretched along the rope
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 520.0; nz.inputs["Detail"].default_value = 4.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.25; bump.inputs["Distance"].default_value = 0.0006
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def rope_nodes(mat):
    ng = bpy.data.node_groups.new("Kairo.rope", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N = ng.nodes; L = ng.links.new
    gi = N.new("NodeGroupInput"); go = N.new("NodeGroupOutput")
    par = N.new("GeometryNodeSplineParameter")
    # per-strand random value
    idx = N.new("GeometryNodeInputIndex")
    ev = N.new("GeometryNodeFieldOnDomain"); ev.domain = "CURVE"; ev.data_type = "INT"
    L(idx.outputs[0], ev.inputs[0])
    rnd = N.new("FunctionNodeRandomValue"); rnd.data_type = "FLOAT"; rnd.inputs["Min"].default_value = 0.0; rnd.inputs["Max"].default_value = 1.0
    L(ev.outputs[0], rnd.inputs["ID"])
    # radius: taper with a rounded tip, per-strand thickness variation
    fc = N.new("ShaderNodeFloatCurve")
    cv = fc.mapping.curves[0]
    cv.points[0].location = (0.0, 0.9); cv.points[1].location = (1.0, 0.08)
    for x, y in ((0.06, 1.0), (0.85, 0.96), (0.95, 0.8), (0.985, 0.5)):
        cv.points.new(x, y)
    fc.mapping.update()
    L(par.outputs["Factor"], fc.inputs["Value"])
    var = N.new("ShaderNodeMapRange"); var.inputs["To Min"].default_value = RADIUS * 0.82; var.inputs["To Max"].default_value = RADIUS * 1.18
    L(rnd.outputs[0], var.inputs["Value"])
    mul0 = N.new("ShaderNodeMath"); mul0.operation = "MULTIPLY"; L(fc.outputs[0], mul0.inputs[0]); L(var.outputs[0], mul0.inputs[1])
    # gentle swelling along the loc (real locs are not perfect tubes)
    bl = N.new("ShaderNodeMath"); bl.operation = "MULTIPLY_ADD"; bl.inputs[1].default_value = 2 * math.pi / 0.055
    L(par.outputs["Length"], bl.inputs[0]); L(rnd.outputs[0], bl.inputs[2])
    bl2 = N.new("ShaderNodeMath"); bl2.operation = "MULTIPLY"; bl2.inputs[1].default_value = 7.0; L(rnd.outputs[0], bl2.inputs[0])
    bl3 = N.new("ShaderNodeMath"); bl3.operation = "ADD"; L(bl.outputs[0], bl3.inputs[0]); L(bl2.outputs[0], bl3.inputs[1])
    sn = N.new("ShaderNodeMath"); sn.operation = "SINE"; L(bl3.outputs[0], sn.inputs[0])
    sw = N.new("ShaderNodeMath"); sw.operation = "MULTIPLY_ADD"; sw.inputs[1].default_value = 0.09; sw.inputs[2].default_value = 1.0
    L(sn.outputs[0], sw.inputs[0])
    mul = N.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; L(mul0.outputs[0], mul.inputs[0]); L(sw.outputs[0], mul.inputs[1])
    setr = N.new("GeometryNodeSetCurveRadius"); L(gi.outputs[0], setr.inputs["Curve"]); L(mul.outputs[0], setr.inputs["Radius"])
    # twist: one turn every ~2.4 cm of length, random start angle
    tw = N.new("ShaderNodeMath"); tw.operation = "MULTIPLY"; tw.inputs[1].default_value = 2 * math.pi / 0.034
    L(par.outputs["Length"], tw.inputs[0])
    ph = N.new("ShaderNodeMath"); ph.operation = "MULTIPLY_ADD"; ph.inputs[1].default_value = 6.28
    L(rnd.outputs[0], ph.inputs[0]); L(tw.outputs[0], ph.inputs[2])
    sett = N.new("GeometryNodeSetCurveTilt"); L(setr.outputs[0], sett.inputs["Curve"]); L(ph.outputs[0], sett.inputs["Tilt"])
    # attributes for the shader
    st = N.new("GeometryNodeStoreNamedAttribute"); st.data_type = "FLOAT"; st.domain = "POINT"; st.inputs["Name"].default_value = "t"
    L(sett.outputs[0], st.inputs["Geometry"]); L(par.outputs["Factor"], st.inputs["Value"])
    st2 = N.new("GeometryNodeStoreNamedAttribute"); st2.data_type = "FLOAT"; st2.domain = "POINT"; st2.inputs["Name"].default_value = "rnd"
    L(st.outputs[0], st2.inputs["Geometry"]); L(rnd.outputs[0], st2.inputs["Value"])
    # rope profile: a 3-lobed star, smoothed, so the twist reads as a twisted lock
    star = N.new("GeometryNodeCurveStar"); star.inputs["Points"].default_value = 3
    star.inputs["Inner Radius"].default_value = 0.8; star.inputs["Outer Radius"].default_value = 1.0
    res = N.new("GeometryNodeFilletCurve"); L(star.outputs[0], res.inputs["Curve"])
    for k, v in (("Radius", 0.45), ("Count", 5)):
        if k in res.inputs:
            res.inputs[k].default_value = v
    if "Mode" in res.inputs:
        res.inputs["Mode"].default_value = "Poly"
    elif hasattr(res, "mode"):
        res.mode = "POLY"
    c2m = N.new("GeometryNodeCurveToMesh"); c2m.inputs["Fill Caps"].default_value = True
    L(st2.outputs[0], c2m.inputs["Curve"]); L(res.outputs[0], c2m.inputs["Profile Curve"])
    if "Scale" in c2m.inputs:      # Blender 5.x: the profile is scaled by this input, not by the radius
        L(mul.outputs[0], c2m.inputs["Scale"])
    subd = N.new("GeometryNodeSubdivisionSurface"); subd.inputs["Level"].default_value = 1
    L(c2m.outputs[0], subd.inputs["Mesh"])
    smooth = N.new("GeometryNodeSetShadeSmooth"); L(subd.outputs[0], smooth.inputs["Geometry"])
    sm_mat = N.new("GeometryNodeSetMaterial"); sm_mat.inputs["Material"].default_value = mat
    L(smooth.outputs[0], sm_mat.inputs["Geometry"]); L(sm_mat.outputs[0], go.inputs[0])
    return ng


def loc_cuffs(strands, rng, count=11):
    """Gold cuffs on a few locs: short ribbed tubes threaded on the strand."""
    import bmesh
    m = bpy.data.materials.new("Kairo.gold"); m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (1.0, 0.70, 0.30, 1); bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Roughness"].default_value = 0.2
    bm = bmesh.new()
    pick = [s_ for s_ in strands if len(s_) > 30]
    rng.shuffle(pick)
    for pts in pick[:count]:
        i = int(len(pts) * rng.uniform(0.55, 0.82))
        c = pts[i]; t = (pts[i + 1] - pts[i - 1]).normalized()
        u = t.orthogonal().normalized(); w = t.cross(u)
        R = RADIUS * 1.12; H = 0.013; seg = 20
        rings = []
        for k, (h, rr) in enumerate(((-H / 2, R * 0.96), (-H / 2 + 0.002, R), (0, R * 1.04), (H / 2 - 0.002, R), (H / 2, R * 0.96))):
            rings.append([bm.verts.new(c + t * h + (u * math.cos(a) + w * math.sin(a)) * rr) for a in np.linspace(0, 2 * math.pi, seg, endpoint=False)])
        for r0, r1 in zip(rings, rings[1:]):
            for j in range(seg):
                bm.faces.new((r0[j], r0[(j + 1) % seg], r1[(j + 1) % seg], r1[j]))
    me = bpy.data.meshes.new("Kairo.loccuffs"); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("Kairo.loccuffs", me); bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(m)
    so = ob.modifiers.new("t", "SOLIDIFY"); so.thickness = 0.0012


def build(body):
    rng = random.Random(SEED)
    dg = bpy.context.evaluated_depsgraph_get()
    bvh = [BVHTree.FromObject(body, dg)] + [BVHTree.FromObject(bpy.data.objects[n], dg) for n in ("Kairo.jacket", "Kairo.collar") if n in bpy.data.objects]
    co = np.array([body.matrix_world @ v.co for v in body.data.vertices])
    def gc(name):
        gi = body.vertex_groups[name].index
        idx = [v.index for v in body.data.vertices if any(g.group == gi and g.weight > 0.5 for g in v.groups)]
        return co[idx]
    eyes = np.vstack([gc("helper-l-eye"), gc("helper-r-eye")])
    scalp = gc("scalp"); lips = gc("lips")
    crown = scalp[:, 2].max()
    head = {
        "eye_z": eyes[:, 2].mean(),
        "brow_z": eyes[:, 2].mean() + 0.04,
        "chin_z": lips[:, 2].min() - 0.06,
        "face_y": eyes[:, 1].mean() + 0.03,
        "face_hw": abs(eyes[:, 0]).max() + 0.03,
        "front_y": scalp[:, 1].min() + 0.06,
        "vol": 0.042,
    }
    hl = crown - head["chin_z"]
    bun_c = Vector((0.0, scalp[:, 1].mean() + 0.075, crown - 0.03))
    global HAIRLINE_Z
    HAIRLINE_Z = head["eye_z"] + 0.072
    roots = scalp_samples(body, rng)
    strands = []
    over_eye = 0
    for p, n in sorted(roots, key=lambda r: r[0].y):
        length = hl * rng.uniform(0.95, 1.2)
        if over_eye < 4 and p.y < head["front_y"] - 0.005 and -0.045 < p.x < 0.03:
            over_eye += 1
            strands.append(grow(bvh, p, n, rng.uniform(0.15, 0.2), rng, head, "fringe"))
            continue
        strands.append(grow(bvh, p, n, length, rng, head, "down"))
    # drop any strand that wandered in front of the face or neck below the chin (it reads as a stray)
    def stray(pts):
        return any(q.z < head["chin_z"] + 0.05 and q.y < head["face_y"] - 0.01 and abs(q.x) < head["face_hw"] - 0.01 for q in pts)
    before = len(strands); strands = [s_ for s_ in strands if not stray(s_)]
    print("dropped strays", before - len(strands))
    loc_cuffs(strands, rng)
    cu = bpy.data.curves.new("Kairo.locs", "CURVE"); cu.dimensions = "3D"
    for pts in strands:
        if len(pts) < 3:
            continue
        sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1)
        for i, q in enumerate(pts):
            sp.points[i].co = (q.x, q.y, q.z, 1)
    ob = bpy.data.objects.new("Kairo.locs", cu); bpy.context.scene.collection.objects.link(ob)
    mod = ob.modifiers.new("rope", "NODES"); mod.node_group = rope_nodes(hair_material())
    print("strands", len(cu.splines), "over-eye", over_eye, "roots", len(roots))
    return ob


bpy.ops.wm.open_mainfile(filepath=str(SRC))
with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
    build(bpy.data.objects["Kairo.body"])
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)
