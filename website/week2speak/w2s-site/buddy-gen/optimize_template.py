"""Make the web copy of the chibi template (references/model.glb -> buddy-models/<name>.glb).

    blender -b --python w2s-site/buddy-gen/optimize_template.py -- <src.glb> <out.glb> [tris] [texture px]

Only optimisation, no redesign: decimate the 1.5M-triangle scan-like mesh to a web budget,
downsize the 4096 px texture, stand the model on the floor (y = 0), centre it, face +Z and
scale it to the site's 2.2 units. Writes scene extras {"w2s": {"height", "faceWidth"}} so the
runtime frames it, without claiming the "w2s-1" rig (it has no skeleton).
"""
import sys
import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
src, out = argv[0], argv[1]
TRIS = int(argv[2]) if len(argv) > 2 else 70000
TEX = int(argv[3]) if len(argv) > 3 else 2048
HEIGHT = 2.2

bpy.ops.wm.read_homefile(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
ob = [o for o in bpy.data.objects if o.type == "MESH"][0]
bpy.context.view_layer.objects.active = ob; ob.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
me = ob.data
# merge the split vertices first (same position and UV) so the decimator sees one surface
before = len(me.polygons)
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.mesh.remove_doubles(threshold=0.00001); bpy.ops.object.mode_set(mode="OBJECT")
d = ob.modifiers.new("decimate", "DECIMATE"); d.decimate_type = "COLLAPSE"
d.ratio = min(1.0, TRIS / max(1, before)); d.use_collapse_triangulate = True
bpy.ops.object.modifier_apply(modifier=d.name)
# feet on the floor, centred, 2.2 units tall (Blender Z up = glTF Y up)
bb = [Vector(c) for c in ob.bound_box]
lo = Vector((min(v.x for v in bb), min(v.y for v in bb), min(v.z for v in bb)))
hi = Vector((max(v.x for v in bb), max(v.y for v in bb), max(v.z for v in bb)))
s = HEIGHT / (hi.z - lo.z)
for v in me.vertices:
    v.co = Vector(((v.co.x - (lo.x + hi.x) / 2) * s, (v.co.y - (lo.y + hi.y) / 2) * s, (v.co.z - lo.z) * s))
me.update()
for p in me.polygons:
    p.use_smooth = True
# face width: the widest point of the head band (top 45 % of the figure, below the hat brim is fine)
head = [v.co for v in me.vertices if v.co.z > HEIGHT * 0.55]
fw = max(v.x for v in head) - min(v.x for v in head)
ob.name = me.name = "Buddy"
mat = me.materials[0]; mat.name = "Buddy"
img = next(n.image for n in mat.node_tree.nodes if n.type == "TEX_IMAGE")
if max(img.size) > TEX:
    img.scale(TEX, TEX)
img.file_format = "JPEG"
bpy.context.scene["w2s"] = {"height": round(HEIGHT, 3), "faceWidth": round(fw * 0.62, 3), "source": "chibi template (references/model.glb)"}
bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", use_selection=False, export_extras=True,
                          export_image_format="JPEG", export_jpeg_quality=86, export_draco_mesh_compression_enable=False,
                          export_apply=True, export_yup=True, export_texcoords=True, export_normals=True)
print(f"OPT tris {before} -> {len(me.polygons)}  verts {len(me.vertices)}  height {HEIGHT}  faceWidth {fw:.3f}  texture {img.size[:]}")
