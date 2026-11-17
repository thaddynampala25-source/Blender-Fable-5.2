"""Stage 4: eyes, brows, lash lines and the skin shader (work/stylised.blend -> work/dressed.blend)."""
from pathlib import Path
import math
import numpy as np
import bmesh
import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
SRC, OUT = HERE / "work" / "stylised.blend", HERE / "work" / "dressed.blend"

SKIN = (0.110, 0.038, 0.017)        # warm deep brown (linear)
SKIN_DEEP = (0.070, 0.024, 0.013)   # creases
LIP = (0.105, 0.035, 0.026)
IRIS = (0.050, 0.020, 0.008)
SCLERA = (0.78, 0.70, 0.62)


def group_idx(ob, name, thr=0.5):
    gi = ob.vertex_groups[name].index
    return [v.index for v in ob.data.vertices if any(g.group == gi and g.weight > thr for g in v.groups)]


def node(nt, kind, **inputs):
    n = nt.nodes.new(kind)
    for k, v in inputs.items():
        n.inputs[k].default_value = v
    return n


def link(nt, a, b):
    nt.links.new(a, b)


def skin_material(ob):
    me = ob.data
    # painted masks as a colour attribute: R = lips
    lips = set(group_idx(ob, "lips", 0.2))
    scalp = set(group_idx(ob, "scalp", 0.3))
    attr = me.color_attributes.new("mask", "FLOAT_COLOR", "POINT")
    for i, d in enumerate(attr.data):
        d.color = (1.0 if i in lips else 0.0, 1.0 if i in scalp else 0.0, 0, 1)
    m = bpy.data.materials.new("Kairo.skin"); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Subsurface Weight"].default_value = 0.3
    b.inputs["Subsurface Radius"].default_value = (1.0, 0.38, 0.2)
    b.inputs["Subsurface Scale"].default_value = 0.012
    b.inputs["Specular IOR Level"].default_value = 0.32
    b.inputs["Coat Weight"].default_value = 0.0
    b.inputs["Coat Roughness"].default_value = 0.35
    b.inputs["Sheen Weight"].default_value = 0.06
    b.inputs["Sheen Tint"].default_value = (1.0, 0.75, 0.6, 1)
    # colour: base, darkened in cavities (AO) and blended to the lip colour
    ao = node(nt, "ShaderNodeAmbientOcclusion"); ao.inputs["Distance"].default_value = 0.02
    crease = node(nt, "ShaderNodeMix", Factor=0.0); crease.data_type = "RGBA"
    crease.inputs["A"].default_value = (*SKIN_DEEP, 1); crease.inputs["B"].default_value = (*SKIN, 1)
    gam = node(nt, "ShaderNodeMath"); gam.operation = "POWER"; gam.inputs[1].default_value = 0.6
    link(nt, ao.outputs["AO"], gam.inputs[0]); link(nt, gam.outputs[0], crease.inputs["Factor"])
    # broad tonal variation so the skin is never one flat colour
    nz = node(nt, "ShaderNodeTexNoise", Scale=9.0, Detail=3.0)
    var = node(nt, "ShaderNodeMix"); var.data_type = "RGBA"; var.blend_type = "OVERLAY"
    var.inputs["Factor"].default_value = 0.12
    link(nt, crease.outputs["Result"], var.inputs["A"]); link(nt, nz.outputs["Color"], var.inputs["B"])
    att = nt.nodes.new("ShaderNodeVertexColor"); att.layer_name = "mask"
    sep = nt.nodes.new("ShaderNodeSeparateColor"); link(nt, att.outputs["Color"], sep.inputs[0])
    lipmix = node(nt, "ShaderNodeMix"); lipmix.data_type = "RGBA"
    lipmix.inputs["B"].default_value = (*LIP, 1)
    link(nt, sep.outputs["Red"], lipmix.inputs["Factor"]); link(nt, var.outputs["Result"], lipmix.inputs["A"])
    scalpmix = node(nt, "ShaderNodeMix"); scalpmix.data_type = "RGBA"
    scalpmix.inputs["B"].default_value = (0.012, 0.007, 0.005, 1)
    link(nt, sep.outputs["Green"], scalpmix.inputs["Factor"]); link(nt, lipmix.outputs["Result"], scalpmix.inputs["A"])
    link(nt, scalpmix.outputs["Result"], b.inputs["Base Color"])
    # roughness: slightly glossier lips and T-zone variation
    rr = node(nt, "ShaderNodeMapRange"); rr.inputs["To Min"].default_value = 0.5; rr.inputs["To Max"].default_value = 0.66
    link(nt, nz.outputs["Fac"], rr.inputs["Value"])
    rl = node(nt, "ShaderNodeMix"); rl.inputs["B"].default_value = 0.38
    link(nt, sep.outputs["Red"], rl.inputs["Factor"]); link(nt, rr.outputs["Result"], rl.inputs["A"])
    link(nt, rl.outputs["Result"], b.inputs["Roughness"])
    # micro detail: fine pores, soft
    pore = node(nt, "ShaderNodeTexNoise", Scale=900.0, Detail=2.0)
    bump = node(nt, "ShaderNodeBump", Strength=0.035, Distance=0.0004)
    link(nt, pore.outputs["Fac"], bump.inputs["Height"]); link(nt, bump.outputs["Normal"], b.inputs["Normal"])
    me.materials.clear(); me.materials.append(m)


def eye_material():
    m = bpy.data.materials.new("Kairo.eye"); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.3
    b.inputs["Coat Weight"].default_value = 1.0
    b.inputs["Coat Roughness"].default_value = 0.02
    b.inputs["Subsurface Weight"].default_value = 0.1
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); link(nt, tc.outputs["Object"], sep.inputs[0])
    # radial distance from the eye's forward (-Y) axis, only on the front half
    vx = node(nt, "ShaderNodeCombineXYZ"); link(nt, sep.outputs["X"], vx.inputs["X"]); link(nt, sep.outputs["Z"], vx.inputs["Y"])
    ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"; link(nt, vx.outputs[0], ln.inputs[0])
    back = node(nt, "ShaderNodeMath"); back.operation = "GREATER_THAN"; back.inputs[1].default_value = -0.004
    link(nt, sep.outputs["Y"], back.inputs[0])
    r = node(nt, "ShaderNodeMath"); r.operation = "ADD"; back_scale = node(nt, "ShaderNodeMath"); back_scale.operation = "MULTIPLY"; back_scale.inputs[1].default_value = 1.0
    link(nt, back.outputs[0], back_scale.inputs[0]); link(nt, ln.outputs["Value"], r.inputs[0]); link(nt, back_scale.outputs[0], r.inputs[1])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); cr = ramp.color_ramp; cr.interpolation = "EASE"
    stops = [(0.0, (0.004, 0.003, 0.003)), (0.0042, (0.006, 0.004, 0.003)), (0.0052, (0.10, 0.045, 0.016)),
             (0.0090, IRIS), (0.0106, (0.012, 0.006, 0.004)), (0.0114, SCLERA), (1.0, SCLERA)]
    cr.elements[0].position, cr.elements[0].color = stops[0][0], (*stops[0][1], 1)
    cr.elements[1].position, cr.elements[1].color = stops[-1][0], (*stops[-1][1], 1)
    for p, c in stops[1:-1]:
        e = cr.elements.new(p); e.color = (*c, 1)
    link(nt, r.outputs[0], ramp.inputs["Fac"]); link(nt, ramp.outputs["Color"], b.inputs["Base Color"])
    # fine iris fibres
    fib = node(nt, "ShaderNodeTexWave", Scale=60.0, Distortion=6.0); fib.wave_type = "RINGS"
    bump = node(nt, "ShaderNodeBump", Strength=0.08); link(nt, fib.outputs["Fac"], bump.inputs["Height"]); link(nt, bump.outputs["Normal"], b.inputs["Normal"])
    return m


def make_eyes(body):
    co = np.array([v.co[:] for v in body.data.vertices])
    mat = eye_material()
    eyes = []
    for side in ("l", "r"):
        idx = group_idx(body, f"helper-{side}-eye")
        c = co[idx].mean(0); rad = float(np.linalg.norm(co[idx] - c, axis=1).mean())
        bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=rad * 0.98, location=c)
        e = bpy.context.object; e.name = f"Kairo.eye.{side}"
        # a gentle cornea bulge on the front
        for v in e.data.vertices:
            y = -v.co.y / rad
            if y > 0.75:
                v.co.y -= (y - 0.75) * rad * 0.18
        bpy.ops.object.shade_smooth()
        e.data.materials.append(mat)
        eyes.append(e)
    return eyes


def extract_strip(body, group, name, mat):
    """Copy a helper strip (lash line) out of the body as its own object."""
    keep = set(group_idx(body, group, 0.5))
    bm = bmesh.new(); bm.from_mesh(body.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.index not in keep], context="VERTS")
    me = bpy.data.meshes.new(name); bm.to_mesh(me)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    me.materials.append(mat)
    return ob


def flat_dark(name, color, rough=0.6):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough
    return m


def make_brow(body, side, eye_c, lift, arch, mat):
    """A thick graphic brow: a 2D outline projected onto the brow ridge, then given thickness."""
    s = 1 if side == "l" else -1
    N, M = 28, 4
    bm = bmesh.new(); grid = []
    x0, x1 = 0.012, 0.078          # inner and outer ends, from the face centre line
    for i in range(N):
        t = i / (N - 1)
        x = x0 + (x1 - x0) * t
        # centre line: low and straight at the head, a gentle arch, tail dipping down
        zc = eye_c[2] + 0.0175 + lift + arch * math.sin(min(t / 0.7, 1) * math.pi * 0.55) - 0.016 * max(0, t - 0.7) / 0.3
        th = 0.0165 * (1 - 0.25 * t) if t < 0.65 else 0.0165 * 0.84 * (1 - (t - 0.65) / 0.35) ** 0.8 + 0.0016
        if t < 0.05:
            th *= 0.8 + 4 * t      # blunt, square-ish head
        row = []
        for j in range(M):
            u = j / (M - 1) - 0.5
            row.append(bm.verts.new((s * x, eye_c[1] - 0.2, zc + u * th)))
        grid.append(row)
    for i in range(N - 1):
        for j in range(M - 1):
            f = (grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1])
            bm.faces.new(f if s > 0 else f[::-1])
    me = bpy.data.meshes.new(f"Kairo.brow.{side}"); bm.to_mesh(me)
    ob = bpy.data.objects.new(me.name, me); bpy.context.scene.collection.objects.link(ob)
    sw = ob.modifiers.new("project", "SHRINKWRAP"); sw.target = body
    sw.wrap_method = "PROJECT"; sw.use_project_y = True; sw.use_negative_direction = False
    sw.use_positive_direction = True; sw.offset = 0.0012
    so = ob.modifiers.new("thick", "SOLIDIFY"); so.thickness = 0.0028; so.offset = 1.0
    sub = ob.modifiers.new("smooth", "SUBSURF"); sub.levels = sub.render_levels = 2
    ob.data.materials.append(mat)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


bpy.ops.wm.open_mainfile(filepath=str(SRC))
with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
    body = bpy.data.objects["Kairo.body"]
    skin_material(body)
    sub = body.modifiers.new("smooth", "SUBSURF"); sub.levels = 1; sub.render_levels = 2
    for p in body.data.polygons:
        p.use_smooth = True
    eyes = make_eyes(body)
    brow_mat = flat_dark("Kairo.brow", (0.012, 0.008, 0.006), 0.55)
    lash_mat = flat_dark("Kairo.lash", (0.008, 0.006, 0.005), 0.5)
    for side in ("l", "r"):
        extract_strip(body, f"helper-{side}-eyelashes-2", f"Kairo.lash.{side}", lash_mat)
    for e, side in zip(eyes, ("l", "r")):
        # the character's left brow sits a little higher: a permanent hint of a raised brow
        make_brow(body, side, e.location, 0.004 if side == "l" else 0.0, 0.007 if side == "l" else 0.004, brow_mat)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)
    print("dressed", [o.name for o in bpy.data.objects])
