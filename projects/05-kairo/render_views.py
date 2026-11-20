"""Render review views in a background Blender, leaving the live one free.

    blender -b projects/05-kairo/work/<file>.blend --python projects/05-kairo/render_views.py -- <mode> <outdir> [samples]

mode: face | bust | body (cameras and lights from studio.py).
"""
import sys
from pathlib import Path
import bpy
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import studio

argv = sys.argv[sys.argv.index("--") + 1:]
mode, out = argv[0], Path(argv[1])
samples = int(argv[2]) if len(argv) > 2 else None
res = tuple(int(x) for x in argv[3].split("x")) if len(argv) > 3 else None
out.mkdir(parents=True, exist_ok=True)
ob = bpy.data.objects["Kairo.body"]
top = max((ob.matrix_world @ v.co).z for v in ob.data.vertices if v.co.z > 0)  # crown (eval-free)
studio.cyclorama()
if mode == "face":
    studio.lights((0, 0, top - 0.15), 0.6)
    studio.render_settings(samples=samples or 32, res=res or (900, 1000))
    shots = [("front", 0), ("q34", 30), ("side", 90)]
    cam = lambda n, y: studio.camera("Face_" + n, (0, -0.05, top - 0.2), y, 1.2, top - 0.18, lens=85)
elif mode == "bust":
    studio.lights((0, 0, top - 0.2), 0.8)
    studio.render_settings(samples=samples or 32, res=res or (1080, 1350))
    shots = [("front", 0), ("q34", 32), ("side", 90)]
    cam = lambda n, y: studio.camera("Bust_" + n, (0, -0.02, top - 0.3), y, 2.3, top - 0.25, lens=85)
else:
    studio.lights((0, 0, top * 0.55), 1.4)
    studio.render_settings(samples=samples or 32, res=res or (1080, 1620))
    shots = [("front", 0), ("q34", 35), ("side", 90)]
    cam = lambda n, y: studio.camera("Body_" + n, (0, 0, top / 2), y, 6.0, top / 2 + 0.15, lens=50)
import os
only = os.environ.get("VIEWS")
if only:
    shots = [s_ for s_ in shots if s_[0] in only.split(",")]
for name, yaw in shots:
    studio.render(cam(name, yaw), out / f"{mode}_{name}.png")
