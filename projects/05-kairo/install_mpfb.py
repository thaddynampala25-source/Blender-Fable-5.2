"""Install the MPFB 2 extension (MakeHuman for Blender) into the live Blender.

The zip is downloaded to assets/cache/ (not committed) by
`install_mpfb.sh`; this script installs and enables it.
MPFB is GPL; the base meshes and targets it produces are CC0.
"""
from pathlib import Path
import addon_utils
import bpy

ZIP = Path(__file__).resolve().parents[2] / "assets" / "cache" / "mpfb-2.0.18.zip"

def installed():
    return any(m.__name__.endswith("mpfb") for m in addon_utils.modules())

if not installed():
    bpy.ops.extensions.package_install_files(filepath=str(ZIP), repo="user_default", enable_on_install=True)
mods = [m.__name__ for m in addon_utils.modules() if m.__name__.endswith("mpfb")]
print("mpfb modules:", mods, "enabled:", [addon_utils.check(m)[1] for m in mods])
