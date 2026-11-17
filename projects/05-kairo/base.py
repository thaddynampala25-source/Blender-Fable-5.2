"""Stage 1: Kairo's base body from MPFB, before stylisation.

Run: scripts/bmcp.py code projects/05-kairo/base.py   (MPFB must be installed: install_mpfb.py)
"""
from pathlib import Path
import bpy
from bl_ext.user_default.mpfb.services.humanservice import HumanService
from bl_ext.user_default.mpfb.services.targetservice import TargetService

HERE = Path(__file__).resolve().parent
OUT = HERE / "work" / "base.blend"

window = None
bpy.ops.wm.read_homefile(use_empty=True)
window = bpy.context.window_manager.windows[0]
with bpy.context.temp_override(window=window):
    macro = TargetService.get_default_macro_info_dict()
    macro.update(gender=1.0, age=0.5, muscle=0.45, weight=0.38, height=0.55, proportions=0.75)
    macro["race"] = {"african": 1.0, "asian": 0.0, "caucasian": 0.0}
    human = HumanService.create_human(scale=0.1, macro_detail_dict=macro)
    human.name = "Kairo.body"
    groups = sorted(g.name for g in human.vertex_groups)
    print("verts", len(human.data.vertices), "height", round(human.dimensions.z, 3))
    print("groups", [g for g in groups if not g.startswith("joint-")][:120])
    OUT.parent.mkdir(exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)
