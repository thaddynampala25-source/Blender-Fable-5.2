"""Stage 2: Kairo's face shape on top of the MPFB base (work/base.blend -> work/face.blend).

Each entry is an MPFB target and its weight. Pairs written "l-/r-" are applied to both sides
unless a side-specific value is given, so asymmetries are deliberate.
"""
from pathlib import Path
import bpy
from bl_ext.user_default.mpfb.services.targetservice import TargetService

HERE = Path(__file__).resolve().parent
SRC, OUT = HERE / "work" / "base.blend", HERE / "work" / "face.blend"

# v2 (see REVIEW_v1.md): broader, softer, shorter face; shorter nose with a broad tip; full
# cheeks over a defined jaw; wide-set eyes; a wider mouth.
BOTH = {   # applied as l-<name> and r-<name>
    "eye-eyefold-down": 0.2,      # hooded upper lid
        "eye-scale-incr": 1.0,
    "eye-trans-out": 0.35,         # wide-set
    "eye-corner2-up": 0.25,        # a slight upward tilt at the outer corner
    "eye-height2-incr": 0.8,
    "cheek-bones-incr": 0.6,
    "cheek-volume-incr": 0.12,     # rounded cheeks, not puffy
    "cheek-trans-up": 0.25,
    "ear-scale-incr": 0.1,
}
SINGLE = {
    "head-round": 0.2, "head-square": 0.3, "head-scale-horiz-incr": 0.1, "head-scale-vert-decr": 0.08, "head-fat-decr": 0.5,
    "chin-height-decr": 0.1, "chin-width-decr": 0.05, "chin-prominent-incr": 0.2, "chin-bones-incr": 0.45,
    "forehead-scale-vert-decr": 0.5,
    "nose-scale-vert-decr": 0.3, "nose-point-width-incr": 0.75, "nose-flaring-incr": 0.6,
    "nose-nostrils-width-incr": 0.5, "nose-volume-incr": 0.25, "nose-point-up": 0.25, "nose-compression-compress": 0.25,
    "mouth-scale-horiz-incr": 0.3, "mouth-upperlip-volume-decr": 0.25, "mouth-lowerlip-volume-decr": 0.45,
    "mouth-cupidsbow-incr": 0.45, "mouth-trans-backward": 0.15, "mouth-scale-depth-decr": 0.45,
    "mouth-trans-up": 0.2,
    "eyebrows-trans-down": 0.15,
    "neck-scale-horiz-incr": 0.25,
}


def apply(body):
    names = dict(SINGLE)
    for k, v in BOTH.items():
        names["l-" + k] = names.get("l-" + k, v)
        names["r-" + k] = names.get("r-" + k, v)
    missing = []
    for name, w in names.items():
        path = TargetService.target_full_path(name)
        if not path:
            missing.append(name)
            continue
        TargetService.load_target(body, path, weight=w, name=name)
    return missing


bpy.ops.wm.open_mainfile(filepath=str(SRC))
with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
    body = bpy.data.objects["Kairo.body"]
    print("missing targets:", apply(body))
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)
