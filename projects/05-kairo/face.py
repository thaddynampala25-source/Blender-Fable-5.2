"""Stage 2: Kairo's face shape on top of the MPFB base (work/base.blend -> work/face.blend).

Each entry is an MPFB target and its weight. Pairs written "l-/r-" are applied to both sides
unless a side-specific value is given, so asymmetries are deliberate.
"""
from pathlib import Path
import bpy
from bl_ext.user_default.mpfb.services.targetservice import TargetService

HERE = Path(__file__).resolve().parent
SRC, OUT = HERE / "work" / "base.blend", HERE / "work" / "face.blend"

BOTH = {   # applied as l-<name> and r-<name>
    "eye-eyefold-down": 0.45,      # hooded upper lid: the relaxed look
    "eye-height2-incr": 0.25,      # open the eye a little: relaxed, not squinting
        "eye-bag-incr": 0.35,          # visible under-eye fold
    "eye-bag-height-incr": 0.2,
    "eye-scale-incr": 1.0,        # stylised: slightly larger eyes
    "eye-trans-out": 0.15,
    "eye-corner1-down": 0.15,
    "cheek-bones-incr": 0.45,
    "cheek-volume-decr": 0.25,
    "ear-scale-incr": 0.15,
    "ear-flap-incr": 0.2,
}
SINGLE = {
    "head-oval": 0.55, "head-scale-vert-incr": 0.25, "head-scale-horiz-decr": 0.08,
    "chin-height-incr": 0.35, "chin-prominent-incr": 0.35, "chin-width-decr": 0.3, "chin-triangle": 0.25, "chin-bones-incr": 0.3,
    "forehead-scale-vert-decr": 0.15,
    "nose-scale-vert-incr": 0.35, "nose-point-width-incr": 0.35, "nose-flaring-incr": 0.35,
    "nose-trans-forward": 0.15, "nose-volume-incr": 0.15, "nose-nostrils-width-incr": 0.25,
    "mouth-upperlip-volume-decr": 0.25, "mouth-lowerlip-volume-decr": 0.15, "mouth-scale-horiz-incr": 0.12,
    "mouth-cupidsbow-incr": 0.35, "mouth-trans-backward": 0.25, "mouth-scale-depth-decr": 0.6,
    "eyebrows-trans-down": 0.25, "eyebrows-angle-down": 0.2,
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
