"""Studio for Kairo's review renders: cyclorama, the signature lighting recipe, cameras.

Lighting recipe (CHARACTER_REFERENCE_ANALYSIS.md 2.5 / 5): a saturated single-colour
cyclorama (sunshine yellow, so the cobalt jacket reads as its complement), a soft warm key from the front, a hot warm-yellow kick light high
behind one shoulder, a cool fill and a top light for the hair.

Import from other scripts in this folder:
    import importlib, sys; sys.path.insert(0, HERE); import studio; importlib.reload(studio)
"""
import math
import bpy
from mathutils import Vector

BG_TOP = (0.80, 0.40, 0.025)      # deep sunshine on the wall
BG_FLOOR = (1.0, 0.70, 0.09)      # sunshine (#FFD93B family) on the floor


def _mat(name):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    return m


def cyclorama():
    if "Cyc" in bpy.data.objects:
        return bpy.data.objects["Cyc"]
    import bmesh
    me = bpy.data.meshes.new("Cyc")
    bm = bmesh.new()
    # profile in YZ: floor towards camera, curved cove, wall behind
    prof = [(y, 0.0) for y in (-9, -4, -1, 2)]
    r = 2.5
    for i in range(1, 12):
        a = i / 12 * math.pi / 2
        prof.append((2 + math.sin(a) * r, r - math.cos(a) * r))
    prof += [(4.5, 4), (4.5, 9)]
    rows = []
    for x in (-12, 12):
        rows.append([bm.verts.new((x, y, z)) for y, z in prof])
    for i in range(len(prof) - 1):
        bm.faces.new((rows[0][i], rows[0][i + 1], rows[1][i + 1], rows[1][i]))
    bm.to_mesh(me)
    ob = bpy.data.objects.new("Cyc", me)
    bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    m = _mat("Cyc")
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = 0.55
    # gradient: cobalt floor fading up to navy on the wall
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = 0.2
    mr.inputs["From Max"].default_value = 4.2
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*BG_FLOOR, 1)
    ramp.color_ramp.elements[1].color = (*BG_TOP, 1)
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    ob.data.materials.append(m)
    return ob


def area(name, loc, target, energy, size, color, size_y=None):
    ob = bpy.data.objects.get(name)
    if ob is None:
        ld = bpy.data.lights.new(name, "AREA")
        ob = bpy.data.objects.new(name, ld)
        bpy.context.scene.collection.objects.link(ob)
    ld = ob.data
    ld.energy = energy
    ld.color = color
    ld.shape = "RECTANGLE" if size_y else "SQUARE"
    ld.size = size
    if size_y:
        ld.size_y = size_y
    ob.location = loc
    d = Vector(target) - Vector(loc)
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    return ob


def lights(center=(0, 0, 1.55), scale=1.0):
    c = Vector(center)
    s = scale
    area("Key", c + Vector((1.6, -2.6, 0.9)) * s, c, 170 * s * s, 1.8 * s, (1.0, 0.90, 0.80))
    area("Kick", c + Vector((-1.7, 1.5, 0.8)) * s, c + Vector((0, 0, 0.05)), 900 * s * s, 0.5 * s, (1.0, 0.80, 0.36), size_y=2.0 * s)
    area("Kick2", c + Vector((1.9, 1.2, 0.5)) * s, c, 140 * s * s, 0.4 * s, (0.75, 0.82, 1.0), size_y=1.6 * s)
    area("Fill", c + Vector((-2.4, -1.8, -0.2)) * s, c, 70 * s * s, 2.5 * s, (0.62, 0.70, 1.0))
    area("Top", c + Vector((0.2, 0.3, 1.9)) * s, c, 90 * s * s, 1.2 * s, (1.0, 0.97, 0.92))
    w = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.10, 0.05, 0.02, 1)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.6


def camera(name, target, yaw_deg, dist, height, lens=85):
    ob = bpy.data.objects.get(name)
    if ob is None:
        ob = bpy.data.objects.new(name, bpy.data.cameras.new(name))
        bpy.context.scene.collection.objects.link(ob)
    ob.data.lens = lens
    ob.data.clip_start = 0.05
    t = Vector(target)
    a = math.radians(yaw_deg)
    ob.location = t + Vector((math.sin(a) * dist, -math.cos(a) * dist, height - t.z))
    ob.rotation_euler = (t - ob.location).to_track_quat("-Z", "Y").to_euler()
    return ob


def render_settings(samples=48, res=(1080, 1350), pct=100):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.max_bounces = 8
    sc.cycles.transparent_max_bounces = 16
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = pct
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    sc.render.film_transparent = False


def render(cam, path):
    sc = bpy.context.scene
    sc.camera = cam
    sc.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
