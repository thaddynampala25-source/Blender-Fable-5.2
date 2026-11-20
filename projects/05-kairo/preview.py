"""Quick low-sample review render of whatever is in the live scene.
Set VIEWS env-free by editing the list below; writes to .scratch/kairo/."""
import importlib, sys, os
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import studio; importlib.reload(studio)
import bpy
OUT = HERE.parents[1] / ".scratch" / "kairo"
OUT.mkdir(parents=True, exist_ok=True)
mode = globals().get("MODE", "body")
ob = bpy.data.objects.get("Kairo.body")
top = max((ob.matrix_world @ v.co).z for v in ob.data.vertices) if ob else 1.9
studio.cyclorama()
if mode == "body":
    studio.lights((0, 0, 1.0), 1.4)
    studio.render_settings(samples=16, res=(720, 1080), pct=100)
    for name, yaw in (("front", 0), ("q34", 35), ("side", 90)):
        cam = studio.camera("Cam_" + name, (0, 0, top / 2), yaw, 5.2, top / 2 + 0.1, lens=50)
        studio.render(cam, OUT / f"body_{name}.png")
elif mode == "face":
    studio.lights((0, 0, top - 0.15), 0.6)
    studio.render_settings(samples=32, res=(900, 1000), pct=100)
    for name, yaw in (("front", 0), ("q34", 30), ("side", 90)):
        cam = studio.camera("Face_" + name, (0, -0.05, top - 0.13), yaw, 1.05, top - 0.11, lens=85)
        studio.render(cam, OUT / f"face_{name}.png")
else:
    studio.lights((0, 0, top - 0.2), 0.8)
    studio.render_settings(samples=24, res=(900, 1000), pct=100)
    for name, yaw in (("front", 0), ("q34", 32), ("side", 90)):
        cam = studio.camera("Bust_" + name, (0, 0, top - 0.3), yaw, 2.3, top - 0.25, lens=85)
        studio.render(cam, OUT / f"bust_{name}.png")
print("ok")
