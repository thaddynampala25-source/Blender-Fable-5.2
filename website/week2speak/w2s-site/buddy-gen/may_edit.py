"""May's texture edits, applied by build_buddy.py (--edit) to a copy of the template's texture.

Owner's notes: scarf beige, not pink; hair a little lighter than black; look a bit more like the
reference photos (Japanese features), without exaggerating. The face is painted into the texture,
so every change is a texture edit located through the baked 3D position of each texel:

- scarf: pink -> warm beige, keeping its shading
- hair: the template's black, unchanged
- eyes: the grey irises recoloured brown (colour only: the eye shape, pupil, catchlight and liner
  are the template's own)
- brows: the template's own
- lips unchanged; cheeks: a faint warm blush
- chin: the dark painted crescent under it is painted over with the neck's skin tone
- texels just outside the UV islands take the colour of the island next to them, so the old
  black does not bleed into the seams when the texture is filtered
All arrays are Blender image order (rows bottom-up), float RGBA 0..1.
"""
import numpy as np


def _hsv_sat(rgb):
    mx = rgb.max(-1); mn = rgb.min(-1)
    return (mx - mn) / np.maximum(mx, 1e-4), mx


def edit(tex, pos, nor, covered, info):
    out = tex.copy()
    rgb = out[..., :3]
    x, y, z = pos[..., 0], pos[..., 1], pos[..., 2]
    sat, val = _hsv_sat(rgb)
    H = info["height"]
    eyes = info["eyes"]; ez = np.mean([e["center"][2] for e in eyes.values()])
    mouth = info.get("mouth")
    neck = (mouth["center"][2] - 0.13) if mouth else ez - 0.3
    frontish = covered & (nor[..., 1] < -0.35)

    # ---- scarf: the fluffy collar is a cool pink (blue channel above green); make it warm beige
    pink = covered & (rgb[..., 2] > rgb[..., 1] + 0.03) & (rgb[..., 0] > 0.75) & (z > 0.55) & (z < neck + 0.1) & (np.abs(x) < 0.4)
    lum = rgb[pink].mean(-1, keepdims=True)
    beige = np.array([0.93, 0.85, 0.73], np.float32)
    rgb[pink] = np.clip(beige * (lum / max(float(lum.mean()), 1e-3)) ** 1.1, 0, 1)

    # ---- hair: near-black surfaces that are hair, by where they are on the figure
    dark = covered & (val < 0.2)
    ax = np.abs(x)
    hair = dark & (
        (z > neck) |                                              # head, above the neck
        ((nor[..., 1] > 0.15) & (z > 0.86)) |                     # the back, down to the hair ends
        ((ax > 0.36) & (z > 0.86)) |                              # strands hanging outside the arms
        ((ax > 0.17) & (z > neck - 0.2) & (nor[..., 1] < 0.15)) | # strands over the shoulders, in front
        # hair ends hanging behind the jacket: the jacket's back is at y < 0.13 and the arms' at
        # y < 0.05, the hair behind them further back
        ((z > 0.66) & (ax < 0.46) & (y > np.where(ax < 0.3, 0.16, 0.065)))
    )
    # keep the face's painted features (brows, liner, pupils) out of the hair mask
    face_box = (np.abs(x) < 0.29) & (z > ez - 0.08) & (z < ez + 0.16) & (nor[..., 1] < -0.5)
    hair &= ~face_box
    # the hair stays the template's black (owner's choice); the mask is still used to keep the
    # chin fix off the hair

    # ---- eyes
    skin_ref = rgb[frontish & (np.abs(x) < 0.08) & (z > ez - 0.12) & (z < ez - 0.05) & (sat > 0.15) & (val > 0.8)]
    skin = np.median(skin_ref, 0) if len(skin_ref) > 50 else np.array([0.94, 0.73, 0.6], np.float32)
    liner_col = np.array([0.035, 0.025, 0.025], np.float32)
    for side, e in eyes.items():
        cx, cz = e["center"][0], e["center"][2]; w, h = e["w"], e["h"]
        sgn = 1 if cx > 0 else -1
        u = (x - cx) / (w * 0.5) * sgn              # -1 inner corner .. +1 outer corner
        v = (z - cz) / (h * 0.5)                    # -1 bottom .. +1 top
        region = frontish & (np.abs(u) < 1.45) & (np.abs(v) < 1.9)
        r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
        skinlike = (sat > 0.18) & (val > 0.55) & (r > g) & (g > b)
        eye = region & ~skinlike & (np.abs(u) < 1.05) & (np.abs(v) < 1.35)
        opening = eye & (val > 0.13)
        liner = region & (val <= 0.13)
        if opening.sum() < 50:
            continue
        # the iris: the grey disc in the opening. Its centre and radius come from the grey texels;
        # inside it, every grey texel is recoloured brown on a ramp that follows the painted
        # brightness. The pupil (near-black), the white catchlight and the sclera keep their colours.
        grey = eye & (sat < 0.25) & (val > 0.12) & (val < 0.86)
        gx, gz = float(np.median(x[grey])), float(np.median(z[grey]))
        rr = np.hypot(x - gx, z - gz)
        rad = float(np.percentile(rr[grey], 90)) * 1.08
        iris = eye & (rr < rad) & (sat < 0.3) & (val > 0.12) & (val < 0.86)
        L = np.clip((val[iris] - 0.12) / 0.6, 0, 1)[:, None] ** 0.8
        dark_b, light_b = np.array([0.22, 0.11, 0.05]), np.array([0.62, 0.40, 0.22])
        rgb[iris] = dark_b + (light_b - dark_b) * L

    # ---- brows: the template's own (they match the black hair)

    # ---- the dark painted crescent under the chin (owner's note: "get rid of that weird black part"):
    # paint it with the neck's own skin tone, shading kept
    if mouth:
        mz = mouth["center"][2]
        chin = covered & (np.abs(x) < 0.16) & (z > mz - 0.19) & (z < mz - 0.06) & (y < -0.1) & ~hair & ((val < 0.55) | ((val < 0.88) & (nor[..., 2] < -0.2) & (z < mz - 0.15)))
        neck_ref = rgb[covered & (np.abs(x) < 0.07) & (z > mz - 0.2) & (z < mz - 0.13) & (val > 0.6) & (sat > 0.15)]
        neck = np.median(neck_ref, 0) if len(neck_ref) > 30 else skin * 0.92
        rgb[chin] = neck * 0.95

    # ---- lips: left as the template painted them (an earlier rose tint was removed at the owner's request); faint blush
    for e in eyes.values():
        cx, cz = e["center"][0], e["center"][2]
        d = ((x - cx * 1.05) / 0.09) ** 2 + ((z - (cz - 0.12)) / 0.05) ** 2
        f = np.clip(1 - d, 0, 1) ** 1.5 * 0.12 * frontish
        blush = np.array([0.95, 0.55, 0.52], np.float32)
        rgb[:] = rgb * (1 - f[..., None]) + blush * f[..., None]
    # ---- pad: texels outside the UV islands take the nearest island colour (up to 12 texels out)
    filled = covered.copy()
    for _ in range(12):
        acc = np.zeros_like(rgb); n = np.zeros(rgb.shape[:2], np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            f = np.roll(filled, (dy, dx), (0, 1)); c = np.roll(rgb, (dy, dx), (0, 1))
            acc += c * f[..., None]; n += f
        grow = ~filled & (n > 0)
        rgb[grow] = acc[grow] / n[grow][:, None]
        filled |= grow
    out[..., :3] = rgb
    return out
