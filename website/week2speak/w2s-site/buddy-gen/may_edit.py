"""May's texture edits, applied by build_buddy.py (--edit) to a copy of the template's texture.

Owner's notes: scarf beige, not pink; hair a little lighter than black; look a bit more like the
reference photos (Japanese features), without exaggerating. The face is painted into the texture,
so every change is a texture edit located through the baked 3D position of each texel:

- scarf: pink -> warm beige, keeping its shading
- hair: near-black -> very dark brown
- eyes: dark brown irises (were grey); a slightly lower upper lid with the liner moved down,
  lowered more at the inner corner than the outer one: a softer, slightly upturned almond shape
- brows: dark brown instead of grey-black
- lips: a little rosier; cheeks: a faint warm blush
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
        ((ax > 0.17) & (z > neck - 0.2) & (nor[..., 1] < 0.15))   # strands over the shoulders, in front
    )
    # keep the face's painted features (brows, liner, pupils) out of the hair mask
    face_box = (np.abs(x) < 0.29) & (z > ez - 0.08) & (z < ez + 0.16) & (nor[..., 1] < -0.5)
    hair &= ~face_box
    brown = np.array([0.20, 0.135, 0.10], np.float32)
    rgb[hair] = np.clip(rgb[hair] / 0.08 * brown, 0, 1)

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
        # iris circle (from the darker part of the opening), measured on the original colours
        darkp = opening & (val < 0.62)
        ic_u, ic_v = float(np.median(u[darkp])), float(np.median(v[darkp]))
        area = darkp.sum() / max(1, opening.sum()) * (np.pi * (w / 2) * (h / 2))
        rad = np.sqrt(area / np.pi) * 1.2
        du = (u - ic_u) * (w * 0.5); dv = (v - ic_v) * (h * 0.5)
        in_iris = (du ** 2 + dv ** 2 < rad ** 2)
        # 1) a slightly lower upper lid along a smooth curve
        uu, vv = u[opening], v[opening]
        bins = np.linspace(-0.95, 0.95, 20); tu, tv = [], []
        for i in range(len(bins) - 1):
            m = (uu >= bins[i]) & (uu < bins[i + 1])
            if m.sum() > 5:
                tu.append((bins[i] + bins[i + 1]) / 2); tv.append(np.percentile(vv[m], 97))
        if len(tu) < 6:
            continue
        top = np.polyval(np.polyfit(tu, tv, 2), u)
        cut = 0.18 - 0.08 * np.clip((u + 1) / 2, 0, 1)   # half-heights: more at the inner corner -> a soft upturn
        nt = top - cut
        lw = 0.30                                          # a bold liner, like the photos
        inner = region & (np.abs(u) < 1.0)
        old = inner & (val < 0.32) & (v > top - 0.12) & (v < top + 0.75) & (u < 0.82)
        above = inner & (v > nt) & (v < top + 0.75) & (u < 0.82) & (old | opening | in_iris)
        rgb[above] = skin
        lwu = lw * (0.8 + 0.4 * np.clip((u + 1) / 2, 0, 1))
        rgb[inner & (v >= nt) & (v <= nt + lwu) & ((v <= top + 0.05) | opening | old)] = liner_col
        # 2) iris: dark brown below the lid, keeping the painted shading
        iris = opening & in_iris & (val < 0.84) & (v < nt)
        L = rgb[iris].mean(-1, keepdims=True)
        dark_b, light_b = np.array([0.06, 0.035, 0.022]), np.array([0.55, 0.35, 0.21])
        rgb[iris] = np.clip(dark_b + (light_b - dark_b) * np.clip((L - 0.08) / 0.7, 0, 1) ** 0.9, 0, 1)
        # 3) a fresh catchlight in the visible part of the iris (the old one is under the lid now)
        cl_u = ic_u + 0.35 * rad / (w * 0.5)
        cl_v = min(ic_v + 0.25 * rad / (h * 0.5), float(np.interp(cl_u, [-1, 1], [np.polyval(np.polyfit(tu, tv, 2), -1), np.polyval(np.polyfit(tu, tv, 2), 1)])) - 0.45)
        cdu = (u - cl_u) * (w * 0.5); cdv = (v - cl_v) * (h * 0.5); cr = rad * 0.2
        rgb[opening & (cdu ** 2 + cdv ** 2 < cr ** 2)] = np.array([1.0, 1.0, 1.0])

    # ---- brows: dark brown
    brow = frontish & (np.abs(x) < 0.3) & (z > ez + 0.04) & (z < ez + 0.17) & (val < 0.35)
    rgb[brow] = np.clip(rgb[brow] / np.maximum(rgb[brow].mean(-1, keepdims=True), 1e-3) * 0.0 + np.array([0.17, 0.11, 0.08]) * (0.6 + rgb[brow].mean(-1, keepdims=True) * 2), 0, 1)

    # ---- lips rosier, faint blush
    if mouth:
        mx_, mz_ = mouth["center"][0], mouth["center"][2]
        d = ((x - mx_) / 0.075) ** 2 + ((z - mz_) / 0.045) ** 2
        f = np.clip(1 - d, 0, 1) ** 0.7 * 0.32 * frontish
        rose = np.array([0.85, 0.50, 0.52], np.float32)
        rgb[:] = rgb * (1 - f[..., None]) + rose * f[..., None]
    for e in eyes.values():
        cx, cz = e["center"][0], e["center"][2]
        d = ((x - cx * 1.05) / 0.09) ** 2 + ((z - (cz - 0.12)) / 0.05) ** 2
        f = np.clip(1 - d, 0, 1) ** 1.5 * 0.12 * frontish
        blush = np.array([0.95, 0.55, 0.52], np.float32)
        rgb[:] = rgb * (1 - f[..., None]) + blush * f[..., None]
    out[..., :3] = rgb
    return out
