"""Stage 6: Kairo's layered streetwear (work/hair.blend -> work/clothes.blend).

Concept A: a long white tee, a sunshine-yellow ribbed knit vest, and a cropped, boxy
cobalt canvas work jacket worn open, with a folded collar, chest patch pockets with button
flaps, hem and cuff bands, brass buttons and yellow contrast stitching.

Garments are shells grown from the body: the region is cut from the body mesh, pushed
out along the normals, relaxed (Laplacian smoothing, so fabric bridges the hollows instead
of shrink-wrapping them) and kept clear of the body and of the layer beneath.
"""
from pathlib import Path
import math
import numpy as np
import bmesh
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

HERE = Path(__file__).resolve().parent
SRC, OUT = HERE / "work" / "dressed.blend", HERE / "work" / "clothes.blend"

COBALT = (0.007, 0.017, 0.20)
NAVY = (0.006, 0.009, 0.040)
OPEN = 0.078              # half-width of the jacket's open front
SUN = (1.0, 0.62, 0.035)
TEE = (0.80, 0.78, 0.74)
BRASS = (0.62, 0.42, 0.16)


# ---------------------------------------------------------------- landmarks
def joints(body):
    me = body.data
    co = np.array([v.co[:] for v in me.vertices])
    vg = {g.index: g.name for g in body.vertex_groups if g.name.startswith("joint-")}
    acc = {}
    for v in me.vertices:
        for g in v.groups:
            if g.group in vg and g.weight > 0.5:
                acc.setdefault(vg[g.group], []).append(v.index)
    return {k: Vector(co[i].mean(0)) for k, i in acc.items()}


class Arm:
    """The arm as two segments, shoulder -> elbow -> wrist; s runs 0..1 along their length."""
    def __init__(self, J, side):
        self.a = J[f"joint-{side}-shoulder"]
        self.e = J[f"joint-{side}-elbow"]
        self.b = J[f"joint-{side}-hand"]
        self.l1 = (self.e - self.a).length; self.l2 = (self.b - self.e).length
        self.L = self.l1 + self.l2
        self.ab = self.b - self.a           # overall direction (used for cuff and seam frames)

    def _nearest(self, p):
        best = None
        for a, b, off, ln in ((self.a, self.e, 0.0, self.l1), (self.e, self.b, self.l1, self.l2)):
            d = b - a
            t = (p - a).dot(d) / d.length_squared
            tc = max(0.0, min(1.0, t))
            q = a + d * tc
            dist = (p - q).length
            # allow running past the shoulder end (t < 0) so s can be negative for the torso
            s = (off + t * ln) / self.L if (a is self.a and t < 0) or (b is self.b and t > 1) else (off + tc * ln) / self.L
            if best is None or dist < best[1]:
                best = (s, dist)
        return best

    def s(self, p):
        return self._nearest(p)[0]

    def dist(self, p):
        return self._nearest(p)[1]

    def point(self, s):
        x = max(0.0, min(1.0, s)) * self.L
        if x <= self.l1:
            return self.a + (self.e - self.a) * (x / self.l1)
        return self.e + (self.b - self.e) * ((x - self.l1) / self.l2)

    def direction(self, s):
        return ((self.e - self.a) if s * self.L <= self.l1 else (self.b - self.e)).normalized()


# ---------------------------------------------------------------- shells
def body_bm(body):
    bm = bmesh.new(); bm.from_mesh(body.data)
    gi = body.vertex_groups["body"].index
    lay = bm.verts.layers.deform.active
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if gi not in v[lay]], context="VERTS")
    for k in list(bm.verts.layers.deform.keys()):
        pass
    bm.verts.ensure_lookup_table()
    return bm


def shell(body, name, keep, offset, bvh_list, relax=24, box=None, push_min=0.004, constrain=None):
    """keep(p) -> bool, offset(p) -> float. bvh_list: surfaces to stay outside of."""
    bm = body_bm(body)
    bm.normal_update()
    dead = [f for f in bm.faces if not all(keep(v.co) for v in f.verts)]
    bmesh.ops.delete(bm, geom=dead, context="FACES")
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table()
    n = len(bm.verts)
    co = np.array([v.co[:] for v in bm.verts]); nor = np.array([v.normal[:] for v in bm.verts])
    off = np.array([offset(Vector(c)) for c in co])
    co = co + nor * off[:, None]
    if box:
        co = box(co)
    e = np.array([[ed.verts[0].index, ed.verts[1].index] for ed in bm.edges])
    boundary = np.array([v.is_boundary for v in bm.verts])
    deg = np.bincount(e.ravel(), minlength=n).astype(float)
    if constrain:
        co = constrain(co, boundary)
    for it in range(relax):
        acc = np.zeros_like(co)
        np.add.at(acc, e[:, 0], co[e[:, 1]]); np.add.at(acc, e[:, 1], co[e[:, 0]])
        avg = acc / np.maximum(deg, 1)[:, None]
        lam = np.where(boundary, 0.25, 0.55)[:, None]
        co = co + (avg - co) * lam
        if constrain:
            co = constrain(co, boundary)
        # stay outside the body (and the layer beneath) by at least part of the offset
        if it % 3 == 2 or it == relax - 1:
            for i in range(n):
                p = Vector(co[i])
                for bvh, clear in bvh_list:
                    hit, hn, _, d = bvh.find_nearest(p)
                    if hit is None:
                        continue
                    need = max(push_min, off[i] * clear)
                    # "inside" only counts near the surface: far from a layer (past its armhole or hem) the nearest point is meaningless
                    if ((p - hit).dot(hn) < 0 and d < 0.03) or d < need:
                        p = hit + hn * need
                co[i] = p[:]
    for i, v in enumerate(bm.verts):
        v.co = co[i]
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    return ob


def finish(ob, thickness, subd=2):
    so = ob.modifiers.new("thickness", "SOLIDIFY"); so.thickness = thickness; so.offset = -1.0
    so.use_rim = True; so.use_even_offset = False; so.thickness_clamp = 1.0
    sd = ob.modifiers.new("smooth", "SUBSURF"); sd.levels = 1; sd.render_levels = subd


def bvh_of(ob):
    dg = bpy.context.evaluated_depsgraph_get()
    return BVHTree.FromObject(ob, dg)


def mask_attr(ob, name, fn):
    """Per-vertex float attribute from fn(position) -> 0..1 (bands, plackets, wear)."""
    me = ob.data
    a = me.attributes.get(name) or me.attributes.new(name, "FLOAT", "POINT")
    for i, v in enumerate(me.vertices):
        a.data[i].value = fn(v.co)


def boundary_distance(ob):
    """Approximate surface distance of every vertex to the mesh border (BFS over edges)."""
    me = ob.data
    bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
    INF = 9.0
    dist = [INF] * len(bm.verts)
    frontier = [v.index for v in bm.verts if v.is_boundary]
    for i in frontier:
        dist[i] = 0.0
    import heapq
    heap = [(0.0, i) for i in frontier]
    while heap:
        d, i = heapq.heappop(heap)
        if d > dist[i] or d > 0.08:
            continue
        v = bm.verts[i]
        for ed in v.link_edges:
            o = ed.other_vert(v); nd = d + ed.calc_length()
            if nd < dist[o.index]:
                dist[o.index] = nd; heapq.heappush(heap, (nd, o.index))
    bm.free()
    return dist


# ---------------------------------------------------------------- materials
def principled(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, m.node_tree, m.node_tree.nodes["Principled BSDF"]


def canvas_material():
    m, nt, b = principled("Kairo.canvas")
    L = nt.links.new
    tc = nt.nodes.new("ShaderNodeTexCoord")
    # plain weave: two perpendicular fine wave patterns
    # twill: fine diagonal ribs (like workwear canvas), crossed by a fainter weave
    w1 = nt.nodes.new("ShaderNodeTexWave"); w1.bands_direction = "DIAGONAL"; w1.inputs["Scale"].default_value = 210
    w2 = nt.nodes.new("ShaderNodeTexWave"); w2.bands_direction = "X"; w2.inputs["Scale"].default_value = 420
    for w in (w1, w2):
        w.inputs["Distortion"].default_value = 0.8; L(tc.outputs["Object"], w.inputs["Vector"])
    mx = nt.nodes.new("ShaderNodeMath"); mx.operation = "MULTIPLY"; L(w1.outputs["Fac"], mx.inputs[0]); L(w2.outputs["Fac"], mx.inputs[1])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.55; bump.inputs["Distance"].default_value = 0.0008
    L(mx.outputs[0], bump.inputs["Height"])
    # broad fabric unevenness
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 30; nz.inputs["Detail"].default_value = 6
    b2 = nt.nodes.new("ShaderNodeBump"); b2.inputs["Strength"].default_value = 0.12; L(nz.outputs["Fac"], b2.inputs["Height"]); L(bump.outputs["Normal"], b2.inputs["Normal"])
    L(b2.outputs["Normal"], b.inputs["Normal"])
    # colour: cobalt, lighter where the fabric wears (edges, bands) and slightly mottled
    band = nt.nodes.new("ShaderNodeAttribute"); band.attribute_name = "band"
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    pr = nt.nodes.new("ShaderNodeMapRange"); pr.inputs["From Min"].default_value = 0.5; pr.inputs["From Max"].default_value = 0.6
    L(geo.outputs["Pointiness"], pr.inputs["Value"])
    wear = nt.nodes.new("ShaderNodeMath"); wear.operation = "MAXIMUM"; L(pr.outputs[0], wear.inputs[0])
    bw = nt.nodes.new("ShaderNodeMath"); bw.operation = "MULTIPLY"; bw.inputs[1].default_value = 0.35; L(band.outputs["Fac"], bw.inputs[0]); L(bw.outputs[0], wear.inputs[1])
    base = nt.nodes.new("ShaderNodeMix"); base.data_type = "RGBA"; base.blend_type = "OVERLAY"
    base.inputs["Factor"].default_value = 0.18; base.inputs["A"].default_value = (*COBALT, 1); L(nz.outputs["Color"], base.inputs["B"])
    worn = nt.nodes.new("ShaderNodeMix"); worn.data_type = "RGBA"
    worn.inputs["B"].default_value = (0.03, 0.065, 0.40, 1)
    wf = nt.nodes.new("ShaderNodeMath"); wf.operation = "MULTIPLY"; wf.inputs[1].default_value = 0.6; L(wear.outputs[0], wf.inputs[0])
    L(wf.outputs[0], worn.inputs["Factor"]); L(base.outputs["Result"], worn.inputs["A"])
    L(worn.outputs["Result"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.78
    b.inputs["Sheen Weight"].default_value = 0.0
    b.inputs["Specular IOR Level"].default_value = 0.35
    return m


def knit_material():
    m, nt, b = principled("Kairo.knit")
    L = nt.links.new
    tc = nt.nodes.new("ShaderNodeTexCoord")
    # vertical ribs plus a small V stitch pattern
    rib = nt.nodes.new("ShaderNodeTexWave"); rib.bands_direction = "X"; rib.wave_profile = "SIN"
    rib.inputs["Scale"].default_value = 95; L(tc.outputs["Object"], rib.inputs["Vector"])
    st = nt.nodes.new("ShaderNodeTexWave"); st.bands_direction = "Z"; st.inputs["Scale"].default_value = 260
    st.inputs["Distortion"].default_value = 3.0; L(tc.outputs["Object"], st.inputs["Vector"])
    mx = nt.nodes.new("ShaderNodeMath"); mx.operation = "MULTIPLY_ADD"; mx.inputs[1].default_value = 0.35
    L(st.outputs["Fac"], mx.inputs[0]); L(rib.outputs["Fac"], mx.inputs[2])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.6; bump.inputs["Distance"].default_value = 0.0015
    L(mx.outputs[0], bump.inputs["Height"]); L(bump.outputs["Normal"], b.inputs["Normal"])
    cr = nt.nodes.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color = (SUN[0] * 0.7, SUN[1] * 0.55, SUN[2] * 0.3, 1)
    cr.color_ramp.elements[1].color = (*SUN, 1); L(mx.outputs[0], cr.inputs["Fac"])
    band = nt.nodes.new("ShaderNodeAttribute"); band.attribute_name = "band"
    trim = nt.nodes.new("ShaderNodeMix"); trim.data_type = "RGBA"; trim.inputs["B"].default_value = (*NAVY, 1)
    crisp = nt.nodes.new("ShaderNodeMath"); crisp.operation = "GREATER_THAN"; crisp.inputs[1].default_value = 0.5
    L(band.outputs["Fac"], crisp.inputs[0])
    L(crisp.outputs[0], trim.inputs["Factor"]); L(cr.outputs["Color"], trim.inputs["A"]); L(trim.outputs["Result"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.88
    b.inputs["Sheen Weight"].default_value = 0.3; b.inputs["Sheen Roughness"].default_value = 0.5
    b.inputs["Sheen Tint"].default_value = (1.0, 0.8, 0.3, 1)
    return m


def corduroy_material():
    m, nt, b = principled("Kairo.corduroy")
    L = nt.links.new
    tc = nt.nodes.new("ShaderNodeTexCoord")
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.bands_direction = "Z"; wv.wave_profile = "SIN"; wv.inputs["Scale"].default_value = 160
    L(tc.outputs["Object"], wv.inputs["Vector"])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.8; bump.inputs["Distance"].default_value = 0.0012
    L(wv.outputs["Fac"], bump.inputs["Height"]); L(bump.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Base Color"].default_value = (*NAVY, 1); b.inputs["Roughness"].default_value = 0.8
    b.inputs["Sheen Weight"].default_value = 0.8; b.inputs["Sheen Roughness"].default_value = 0.35
    b.inputs["Sheen Tint"].default_value = (0.45, 0.5, 0.8, 1)
    return m


def cotton_material():
    m, nt, b = principled("Kairo.tee")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 700
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.15
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Base Color"].default_value = (*TEE, 1); b.inputs["Roughness"].default_value = 0.85
    b.inputs["Sheen Weight"].default_value = 0.45
    b.inputs["Subsurface Weight"].default_value = 0.05
    return m


def metal_material(name, color, rough=0.32):
    m, nt, b = principled(name)
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Metallic"].default_value = 1.0; b.inputs["Roughness"].default_value = rough
    return m


def thread_material():
    m, nt, b = principled("Kairo.thread")
    b.inputs["Base Color"].default_value = (*SUN, 1); b.inputs["Roughness"].default_value = 0.6; b.inputs["Sheen Weight"].default_value = 0.5
    return m


# ---------------------------------------------------------------- details
def stitch_nodes(mat, spacing=0.0055, radius=0.0007):
    """Geometry nodes: polyline -> dashed thread stitches lying along it."""
    ng = bpy.data.node_groups.get("Kairo.stitch")
    if ng:
        return ng
    ng = bpy.data.node_groups.new("Kairo.stitch", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N = ng.nodes; L = ng.links.new
    gi = N.new("NodeGroupInput"); go = N.new("NodeGroupOutput")
    m2c = N.new("GeometryNodeMeshToCurve"); L(gi.outputs[0], m2c.inputs["Mesh"])
    c2p = N.new("GeometryNodeCurveToPoints"); c2p.mode = "LENGTH"; c2p.inputs["Length"].default_value = spacing
    L(m2c.outputs[0], c2p.inputs["Curve"])
    cyl = N.new("GeometryNodeMeshCylinder"); cyl.inputs["Vertices"].default_value = 6
    cyl.inputs["Radius"].default_value = radius; cyl.inputs["Depth"].default_value = spacing * 0.6
    # cylinders run along Z; align Z to the curve tangent
    align = N.new("FunctionNodeAlignRotationToVector"); align.axis = "Z"
    L(c2p.outputs["Tangent"], align.inputs["Vector"])
    inst = N.new("GeometryNodeInstanceOnPoints"); L(c2p.outputs["Points"], inst.inputs["Points"]); L(cyl.outputs["Mesh"], inst.inputs["Instance"])
    L(align.outputs[0], inst.inputs["Rotation"])
    real = N.new("GeometryNodeRealizeInstances"); L(inst.outputs[0], real.inputs[0])
    sm = N.new("GeometryNodeSetMaterial"); sm.inputs["Material"].default_value = mat
    L(real.outputs[0], sm.inputs["Geometry"]); L(sm.outputs[0], go.inputs[0])
    return ng


def polyline(name, pts, mat):
    me = bpy.data.meshes.new(name)
    me.from_pydata([p[:] for p in pts], [(i, i + 1) for i in range(len(pts) - 1)], [])
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    mod = ob.modifiers.new("stitch", "NODES"); mod.node_group = stitch_nodes(mat)
    return ob


def project_front(bvh, x, z, y0=-1.0, lift=0.0):
    """Hit point on a surface along +Y from the front, nudged out by lift along the normal."""
    hit, n, _, _ = bvh.ray_cast(Vector((x, y0, z)), Vector((0, 1, 0)))
    if hit is None:
        return None, None
    return hit + n * lift, n


def patch(name, bvh, x0, x1, z0, z1, lift, mat, rows=8, cols=8, point=0.0):
    """A thin panel conformed to a surface seen from the front (pocket, flap)."""
    verts, faces = [], []
    for j in range(rows + 1):
        for i in range(cols + 1):
            u, v = i / cols, j / rows
            x = x0 + (x1 - x0) * u
            # optional pointed bottom edge (flap)
            z = z0 + (z1 - z0) * v - (point * (1 - abs(2 * u - 1)) if j == 0 else 0)
            p, _ = project_front(bvh, x, z, lift=lift)
            verts.append(p if p is not None else Vector((x, -0.2, z)))
    for j in range(rows):
        for i in range(cols):
            a = j * (cols + 1) + i
            faces.append((a, a + 1, a + cols + 2, a + cols + 1))
    me = bpy.data.meshes.new(name); me.from_pydata([v[:] for v in verts], [], faces)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    me.materials.append(mat)
    for p in me.polygons:
        p.use_smooth = True
    so = ob.modifiers.new("t", "SOLIDIFY"); so.thickness = 0.003; so.offset = 1.0
    sd = ob.modifiers.new("s", "SUBSURF"); sd.levels = 1; sd.render_levels = 2
    bev = ob.modifiers.new("b", "BEVEL"); bev.width = 0.0015; bev.segments = 2
    ob.modifiers.move(2, 1)
    edge = [verts[i] for i in range(cols + 1)] + [verts[j * (cols + 1) + cols] for j in range(1, rows + 1)] + \
           [verts[rows * (cols + 1) + i] for i in range(cols - 1, -1, -1)] + [verts[j * (cols + 1)] for j in range(rows - 1, -1, -1)]
    return ob, verts, edge


def inset_loop(pts, center, amount):
    return [c + (center - c).normalized() * amount for c in pts]


def button(name, loc, normal, mat, r=0.0085):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=r, depth=0.004, location=loc)
    ob = bpy.context.object; ob.name = name
    ob.rotation_euler = normal.to_track_quat("Z", "Y").to_euler()
    bv = ob.modifiers.new("b", "BEVEL"); bv.width = 0.0015; bv.segments = 3
    bpy.ops.object.shade_smooth()
    ob.data.materials.append(mat)
    return ob


# ---------------------------------------------------------------- build
def build():
    body = bpy.data.objects["Kairo.body"]
    J = joints(body)
    arms = [Arm(J, "l"), Arm(J, "r")]
    neck = J["joint-neck"]
    hem_j, hem_v, hem_t = 1.085, 0.985, 0.80        # jacket, vest, tee hems
    body_bvh = bvh_of(body)

    def on_arm(p):
        return max((a.s(p) if a.dist(p) < 0.13 and a.s(p) > 0.06 and abs(p.x) > 0.19 else -1) for a in arms)

    def neck_line(p, drop_front):
        f = max(0.0, min(1.0, (-p.y - 0.0) / 0.11))
        return 1.645 - drop_front * f

    def torso(p, hem, drop_front):
        return hem < p.z < neck_line(p, drop_front) and on_arm(p) < 0

    # --- tee: long, crew neck, short sleeves under the jacket
    def crew(co, boundary):
        for i in np.nonzero(boundary)[0]:
            p = co[i]
            if p[2] > 1.5 and on_arm(Vector(p)) < 0:
                f = max(0.0, min(1.0, -p[1] / 0.1))
                p[2] = 1.636 - 0.03 * f * f
        return co
    tee = shell(body, "Kairo.tee",
                keep=lambda p: torso(p, hem_t, 0.03) and not (abs(p.x) > 0.2 and p.z > 1.38),
                offset=lambda p: 0.005, bvh_list=[(body_bvh, 0.8)], relax=12, constrain=crew)
    finish(tee, 0.002); tee.data.materials.append(cotton_material())
    tee_bvh = bvh_of(tee)

    # --- vest: V-neck, sleeveless, ribbed
    def vest_keep(p):
        if not torso(p, hem_v, 0.0) or p.z > 1.625:
            return False
        if abs(p.x) > 0.205 and p.z > 1.36:        # armholes
            return False
        if p.y < 0 and p.z > 1.42 and abs(p.x) < (p.z - 1.42) * 0.55:   # V-neck
            return False
        return True
    def vee(co, boundary):
        for i in np.nonzero(boundary)[0]:
            p = co[i]
            if p[1] < 0 and 1.395 < p[2] < 1.64 and abs(p[0]) < 0.16:
                p[0] = math.copysign(max(0.0, p[2] - 1.42) * 0.55, p[0] if abs(p[0]) > 1e-5 else 1.0)
        return co
    vest = shell(body, "Kairo.vest", keep=vest_keep, offset=lambda p: 0.011, bvh_list=[(tee_bvh, 0.6), (body_bvh, 1.0)], relax=16, constrain=vee)
    finish(vest, 0.004); vest.data.materials.append(knit_material())
    vd = boundary_distance(vest)
    va = vest.data.attributes.new("band", "FLOAT", "POINT")
    for i, v in enumerate(vest.data.vertices):
        va.data[i].value = 1.0 if vd[i] < 0.016 else 0.0
        if vd[i] < 0.016:
            v.co = v.co + v.normal * 0.0015
    vest_bvh = bvh_of(vest)

    # --- jacket: cropped, boxy, open front, sleeves to the wrist
    def jacket_keep(p):
        if p.y < -0.02 and abs(p.x) < OPEN and p.z < 1.60:     # open front (worn open, the vest shows)
            return False
        s = on_arm(p)
        if s >= 0:
            return s < 0.9
        return torso(p, hem_j, 0.06)

    def jacket_off(p):
        s = on_arm(p)
        if s >= 0:
            return 0.024 + 0.006 * math.sin(min(s, 0.9) * math.pi)     # roomy sleeve
        return 0.03 if p.z < 1.5 else 0.022

    def boxy(co):
        # below the chest the jacket falls straight: never narrower than at chest height
        out = co.copy()
        for i, p in enumerate(co):
            v = Vector(p); s = on_arm(v)
            if s >= 0:
                a_ = arms[0] if v.x > 0 else arms[1]
                ss_ = max(0.0, min(1.0, a_.s(v)))
                ax = a_.point(ss_)
                r = (v - ax).length
                R_ = 0.092 - 0.034 * ss_                         # roomy at the top, narrower to the cuff
                if r < R_:
                    out[i] = (ax + (v - ax).normalized() * R_)[:]
        cy = 0.0
        chest = co[(np.abs(co[:, 2] - 1.42) < 0.02) & (np.abs(co[:, 0]) < 0.24)]
        if len(chest) == 0:
            return out
        ang_c = np.arctan2(chest[:, 1] - cy, chest[:, 0]); rad_c = np.hypot(chest[:, 0], chest[:, 1] - cy)
        order = np.argsort(ang_c); ang_c, rad_c = ang_c[order], rad_c[order]
        for i, p in enumerate(co):
            if p[2] < 1.47 and on_arm(Vector(p)) < 0:
                a = math.atan2(p[1] - cy, p[0]); r = math.hypot(p[0], p[1] - cy)
                rt = np.interp(a, ang_c, rad_c, period=2 * math.pi) * (1.0 + 0.03 * (1.42 - p[2]))
                w = min(1.0, (1.47 - p[2]) / 0.06)
                if rt > r:
                    s = (r + (rt - r) * w) / r
                    out[i, 0] = p[0] * s; out[i, 1] = cy + (p[1] - cy) * s
        return out

    def edges(co, boundary):
        # roomy tube sleeves, enforced on every relaxation step so smoothing can't shrink them back
        for i in range(len(co)):
            v = Vector(co[i]); s = on_arm(v)
            if s >= 0:
                a_ = arms[0] if v.x > 0 else arms[1]
                ss_ = max(0.0, min(1.0, a_.s(v)))
                ax = a_.point(ss_)
                R_ = 0.092 - 0.034 * ss_
                r = (v - ax).length
                if r < R_:
                    co[i] = (ax + (v - ax).normalized() * R_)[:]
        # clean garment edges: a straight front opening, a level hem, cuffs square to the arm
        for i in np.nonzero(boundary)[0]:
            p = Vector(co[i]); s = on_arm(p)
            if s >= 0.7:
                a_ = arms[0] if p.x > 0 else arms[1]
                d = a_.direction(0.95); p = p - d * ((a_.s(p) - 0.9) * a_.L)
            elif p.z < hem_j + 0.035 and s < 0:
                p.z = hem_j
            elif p.y < 0 and abs(p.x) < OPEN + 0.05 and p.z < 1.585:
                p.x = math.copysign(OPEN + 0.003, p.x)
            co[i] = p[:]
        return co

    jacket = shell(body, "Kairo.jacket", keep=jacket_keep, offset=jacket_off,
                   bvh_list=[(vest_bvh, 0.45), (tee_bvh, 0.6), (body_bvh, 1.0)], relax=70, box=boxy,
                   constrain=edges)
    # folds: compression rings at the elbows and above the cuffs
    me = jacket.data
    for v in me.vertices:
        p = v.co.copy(); s = on_arm(p)
        if s < 0:
            continue
        a = arms[0] if p.x > 0 else arms[1]
        axis_pt = a.point(a.s(p))
        radial = (p - axis_pt).normalized()
        w = math.exp(-((s - 0.52) / 0.06) ** 2) + 0.8 * math.exp(-((s - 0.84) / 0.04) ** 2)
        ang = math.atan2(radial.z, radial.y)
        v.co = p + radial * 0.008 * w * math.sin(s * 2 * math.pi / 0.045 + 1.3 * math.sin(ang * 2))
    tex = bpy.data.textures.new("Kairo.wrinkle", "DISTORTED_NOISE"); tex.noise_scale = 0.085; tex.distortion = 2.0
    dm = jacket.modifiers.new("wrinkles", "DISPLACE"); dm.texture = tex; dm.strength = 0.012; dm.mid_level = 0.0     # outward only, so folds never cut into the layers beneath
    finish(jacket, 0.0045)
    jacket.data.materials.append(canvas_material())
    # bands: hem, cuffs and front edges get a lighter, raised band
    dist = boundary_distance(jacket)
    a = me.attributes.new("band", "FLOAT", "POINT")
    for i, v in enumerate(me.vertices):
        band = 1.0 if dist[i] < 0.03 and v.co.z < 1.58 else 0.0
        a.data[i].value = band
        if band:
            v.co = v.co + v.normal * 0.002
    jacket_bvh = bvh_of(jacket)

    # --- collar: follows the jacket's neck edge, stands up, folds over and lies on the jacket
    jme = jacket.data
    jb = bmesh.new(); jb.from_mesh(jme); jb.verts.ensure_lookup_table()
    edge = [v.co.copy() for v in jb.verts if v.is_boundary and v.co.z > 1.555 and not (v.co.y < 0 and abs(v.co.x) < 0.06 and v.co.z < 1.585)]
    jb.free()
    ctr = Vector((neck.x, neck.y, 0))
    edge.sort(key=lambda q: math.atan2(q.x - ctr.x, q.y - ctr.y))      # from his right front, round the back, to his left front
    # resample evenly along the edge
    seg = [0.0]
    for i in range(1, len(edge)):
        seg.append(seg[-1] + (edge[i] - edge[i - 1]).length)
    K = 48
    ring = []
    for k in range(K + 1):
        t = seg[-1] * k / K
        i = max(1, min(len(edge) - 1, int(np.searchsorted(seg, t))))
        f = (t - seg[i - 1]) / max(1e-6, seg[i] - seg[i - 1])
        ring.append(edge[i - 1].lerp(edge[i], f))
    verts, faces = [], []
    for k, p in enumerate(ring):
        tt = k / K
        back = 1 - abs(tt - 0.5) * 2                             # 1 at the back of the neck, 0 at the fronts
        outd = Vector((p.x - ctr.x, p.y - ctr.y, 0)).normalized()
        stand = 0.032 * (0.55 + 0.45 * back)
        p1 = p + Vector((0, 0, stand)) - outd * 0.004
        p2 = p1 + outd * 0.014 + Vector((0, 0, 0.004))
        fall = []
        for reach, drop in ((0.03, 0.012), (0.052, 0.03), (0.07 + 0.02 * (1 - back) ** 2, 0.05 + 0.03 * (1 - back) ** 3)):
            q = p + outd * reach - Vector((0, 0, drop - stand * 0.3))
            hit, hn, _, _ = jacket_bvh.find_nearest(q)
            fall.append(hit + hn * 0.006 if hit else q)
        for q in [p - Vector((0, 0, 0.004)), p1, p2] + fall:
            verts.append(q)
    R = 6
    for k in range(K):
        for r in range(R - 1):
            a0 = k * R + r
            faces.append((a0, a0 + R, a0 + R + 1, a0 + 1))
    cme = bpy.data.meshes.new("Kairo.collar"); cme.from_pydata([v[:] for v in verts], [], faces)
    collar = bpy.data.objects.new("Kairo.collar", cme); bpy.context.scene.collection.objects.link(collar)
    for p in cme.polygons:
        p.use_smooth = True
    finish(collar, 0.004)
    collar.data.materials.append(corduroy_material())
    stitch_ring = [verts[k * R + 5] for k in range(K + 1)]
    polyline("Kairo.stitch.collar", [verts[k * R + 4].lerp(verts[k * R + 5], 0.75) for k in range(K + 1)], thread_material())

    # --- pockets, flaps, buttons, stitching
    canvas = jacket.data.materials[0]
    brass = metal_material("Kairo.brass", BRASS)
    thread = bpy.data.materials["Kairo.thread"]
    for sgn in (1, -1):
        x0, x1 = sorted((sgn * (OPEN + 0.02), sgn * (OPEN + 0.098)))
        pk, pv, pedge = patch(f"Kairo.pocket.{'l' if sgn > 0 else 'r'}", jacket_bvh, x0, x1, 1.34, 1.455, 0.0045, canvas)
        fl, fv, fedge = patch(f"Kairo.flap.{'l' if sgn > 0 else 'r'}", jacket_bvh, x0 - 0.004, x1 + 0.004, 1.43, 1.47, 0.0085, canvas, rows=4, point=0.012)
        c = sum(pedge, Vector()) / len(pedge)
        polyline(f"Kairo.stitch.pocket.{sgn}", inset_loop(pedge[:-1] if False else pedge, c, 0.004) + [inset_loop(pedge, c, 0.004)[0]], thread)
        cf = sum(fedge, Vector()) / len(fedge)
        polyline(f"Kairo.stitch.flap.{sgn}", inset_loop(fedge, cf, 0.004) + [inset_loop(fedge, cf, 0.004)[0]], thread)
        bp, bn = project_front(jacket_bvh, (x0 + x1) / 2, 1.432, lift=0.013)
        if bp:
            button(f"Kairo.button.pocket.{sgn}", bp, bn, brass, r=0.0065)
    # front placket buttons on his left edge, stitch lines down both front edges and round the hem
    for k, z in enumerate((1.53, 1.43, 1.33, 1.23, 1.13)):
        bp, bn = project_front(jacket_bvh, OPEN + 0.016, z, lift=0.004)
        if bp:
            button(f"Kairo.button.front.{k}", bp, bn, brass)
    for sgn in (1, -1):
        pts = [project_front(jacket_bvh, sgn * (OPEN + 0.007), z, lift=0.0055)[0] for z in np.linspace(1.095, 1.58, 60)]
        polyline(f"Kairo.stitch.front.{sgn}", [p for p in pts if p], thread)
    def seam(name, pts, crease=0.0016):
        """Double stitch line along points on the jacket, with a slight crease pressed into the mesh."""
        pts = [q for q in pts if q is not None]
        if len(pts) < 2:
            return
        for off in (0.0035, -0.0035):
            line = []
            for i, q in enumerate(pts):
                t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
                hit, hn, _, _ = jacket_bvh.find_nearest(q)
                if hit is None:
                    continue
                side = t.cross(hn).normalized()
                line.append(hit + side * off + hn * 0.0052)
            polyline(name + ("a" if off > 0 else "b"), line, thread)
        jm = jacket.data
        for v in jm.vertices:
            d = min((v.co - q).length for q in pts[:: max(1, len(pts) // 40)])
            if d < 0.006:
                v.co -= v.normal * crease * (1 - d / 0.006)

    yz = 1.495
    for sgn in (1, -1):
        seam(f"Kairo.seam.yoke.{sgn}", [project_front(jacket_bvh, sgn * x, yz + 0.012 * (x / 0.2), lift=0.0)[0] for x in np.linspace(OPEN + 0.01, 0.2, 22)])
    back = []
    for x in np.linspace(-0.2, 0.2, 40):
        hit, n, _, _ = jacket_bvh.ray_cast(Vector((x, 1.0, yz + 0.03)), Vector((0, -1, 0)))
        back.append(hit)
    seam("Kairo.seam.yoke.back", back)
    for k, a_ in enumerate(arms):
        ring = []
        sx = a_.point(0.1)
        dirv = a_.direction(0.1)
        u = dirv.cross(Vector((0, 0, 1))).normalized(); w = dirv.cross(u).normalized()
        for t in np.linspace(0, 2 * math.pi, 48):
            o = sx + (u * math.cos(t) + w * math.sin(t)) * 0.2
            hit, n, _, _ = jacket_bvh.ray_cast(o, (sx - o).normalized())
            ring.append(hit)
        seam(f"Kairo.seam.armhole.{k}", ring)
    print("clothes: tee", len(tee.data.vertices), "vest", len(vest.data.vertices), "jacket", len(jacket.data.vertices))


bpy.ops.wm.open_mainfile(filepath=str(SRC))
with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
    build()
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)
