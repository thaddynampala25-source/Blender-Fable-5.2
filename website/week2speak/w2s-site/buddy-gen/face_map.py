"""Face data for the integrated face animation (blinks and mouth movement on the model's own surface).

Used by build_buddy.py; pure numpy, so it can be previewed outside Blender.

The faces of these models are painted into one texture and the mesh is one fused surface: there are no
eyelids and no separate mouth. Instead of laying new pieces over the face, the runtime animates the
painted features themselves:

- Blink: the character's own upper lash line (with any wings) slides down over the eye; the white,
  iris and pupil it passes over give way to skin. For that the runtime needs, in a small front-view
  raster of the eye band: the original colours (where the lash line is), the skin with the eyes
  painted out ("clean", filled smoothly from the skin around them), a mask of the eye features, and
  per column the top of the eye opening and its height.
- Mouth: the mesh around the mouth deforms (lower lip and jaw down, corners in or out); only the gap
  that opens between the lips is shaded. For that the runtime needs the line where the lips part
  (the seam) and the mouth's width.

Coordinates: Blender (x right, -y front, z up) in, glTF/three.js (x, y up, z front) out.
"""
import numpy as np

PX = 0.0015          # raster pixel size in metres (about the texture's own density on the face)
LUMA = np.array([0.3, 0.59, 0.11], np.float32)


def _shift(a, dy, dx):
    return np.roll(a, (dy, dx), (0, 1))


def _dil(m, r):
    o = m.copy()
    for _ in range(r):
        o = o | _shift(o, 1, 0) | _shift(o, -1, 0) | _shift(o, 0, 1) | _shift(o, 0, -1)
    return o


def _ero(m, r):
    return ~_dil(~m, r)


def _flood(seed, allowed):
    r = seed & allowed
    while True:
        n = _dil(r, 1) & allowed
        if (n == r).all():
            return r
        r = n


def _fill_holes(img, ok, it=8):
    img = img.copy(); ok = ok.copy()
    for _ in range(it):
        acc = np.zeros_like(img); n = np.zeros(ok.shape, np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            acc += _shift(img * ok[..., None], dy, dx); n += _shift(ok, dy, dx)
        g = ~ok & (n > 0)
        img[g] = acc[g] / n[g][:, None]; ok |= g
    return img, ok


def _inpaint(img, hole, it=600):
    """Fill `hole` smoothly from the pixels around it (harmonic fill, coarse start)."""
    out = img.copy(); known = ~hole
    # start from the mean of nearby known pixels, grown outward, then relax
    filled, ok = _fill_holes(np.where(known[..., None], img, 0), known, it=60)
    out[hole] = filled[hole]
    for _ in range(it):
        avg = (_shift(out, 1, 0) + _shift(out, -1, 0) + _shift(out, 0, 1) + _shift(out, 0, -1)) / 4
        out[hole] = avg[hole]
    return out


def raster(tex, pos, nor, covered, x0, x1, z0, z1, px=PX):
    """Front view of the surface between x0..x1, z0..z1: colour and depth of the front-most layer."""
    W = int(round((x1 - x0) / px)); H = int(round((z1 - z0) / px))
    m = covered & (nor[..., 1] < -0.2) & (pos[..., 0] > x0) & (pos[..., 0] < x1) & (pos[..., 2] > z0) & (pos[..., 2] < z1)
    P = pos[m]; C = tex[..., :3][m]
    i = ((P[:, 0] - x0) / px).astype(int).clip(0, W - 1); j = ((z1 - P[:, 2]) / px).astype(int).clip(0, H - 1)
    depth = np.full((H, W), 9.0, np.float32); np.minimum.at(depth, (j, i), P[:, 1])
    keep = P[:, 1] <= depth[j, i] + 0.006
    acc = np.zeros((H, W, 3), np.float32); n = np.zeros((H, W), np.float32)
    np.add.at(acc, (j[keep], i[keep]), C[keep]); np.add.at(n, (j[keep], i[keep]), 1)
    img = acc / np.maximum(n, 1)[..., None]; ok = n > 0
    img, _ = _fill_holes(img, ok)
    dep, _ = _fill_holes(np.where(ok, depth, 0)[..., None], ok)
    return img, dep[..., 0]


def eye_data(img, eyes, x0, z1, px=PX):
    """Per eye: feature mask, lash-line mask, opening top and height per column."""
    H, W = img.shape[:2]
    lum = img @ LUMA
    col = lambda x: int(round((x - x0) / px)); row = lambda z: int(round((z1 - z) / px))
    F_all = np.zeros((H, W), bool); L_all = np.zeros((H, W), np.float32)
    T_all = np.full(W, -1.0); S_all = np.zeros(W)
    for e in eyes.values():
        ex, ez = e["center"][0], e["center"][2]; ew, eh = e["w"], e["h"]
        cx, cy = col(ex), row(ez); o = 1 if ex > 0 else -1
        xa, xb = sorted((cx - o * int(ew * 0.62 / px), cx + o * int(ew * 0.72 / px)))   # outer side: room for a wing
        box = np.zeros((H, W), bool); box[max(0, cy - int(eh * 1.6 / px)):min(H, cy + int(eh * 1.0 / px)), max(0, xa):min(W, xb)] = True
        sk = img[cy + int(eh * 0.75 / px):cy + int(eh * 0.95 / px), cx - int(ew * 0.3 / px):cx + int(ew * 0.3 / px)].reshape(-1, 3)
        s0 = np.median(sk, 0); l0 = float(s0 @ LUMA)
        nonskin = box & ((np.linalg.norm(img - s0, axis=-1) > 0.13) | (lum < 0.6 * l0))
        seed = np.zeros((H, W), bool); seed[cy, cx] = True
        F = _flood(_dil(seed, 3), nonskin)
        F = _ero(_dil(F, 4), 4) & box
        edge = box & ~_ero(box, 1)
        F = box & ~_flood(edge & ~F, box & ~F)            # holes (an iris close to skin tone) belong to the eye
        tops = [r for c in range(W) if F[:, c].any() for r in np.nonzero(F[:, c])[0][:6]]
        lin = float(np.percentile([lum[r, c] for c in range(W) if F[:, c].any() for r in np.nonzero(F[:, c])[0][:6]], 10)) if tops else 0.1
        dark = lum < lin + 0.035
        Ltop = np.full(W, np.nan); Bot = np.full(W, np.nan); T = np.full(W, np.nan)
        for c in range(W):
            rows = np.nonzero(F[:, c])[0]
            if len(rows) == 0:
                continue
            Ltop[c] = rows[0]; Bot[c] = rows[-1]
            r = rows[0]
            while r < rows[0] + 6 and r < H and F[r, c] and not dark[r, c]:
                r += 1                                     # the anti-aliased edge
            if r >= H or not dark[r, c]:
                continue
            while r < H and F[r, c] and dark[r, c]:
                r += 1                                     # the lash line
            if r < H and F[r, c] and r <= Bot[c] - 2 and lum[min(H - 1, r + 1), c] > 0.62:
                T[c] = r                                   # only where the line meets the white of the eye
        cs = np.nonzero(~np.isnan(T))[0]
        if len(cs) < 8:
            continue
        keep = np.ones(len(cs), bool)
        for _ in range(4):
            p = np.polyfit(cs[keep], T[cs][keep], 3); res = T[cs] - np.polyval(p, cs)
            keep = np.abs(res) < max(2.5, 2.5 * np.std(res[keep]))
        a, b = cs[keep].min(), cs[keep].max()
        # the bottom of the opening, also as a smooth curve, so the lid travels evenly (no torn lash line)
        bc = np.array([c for c in range(a, b + 1) if not np.isnan(Bot[c])])
        kb = np.ones(len(bc), bool)
        for _ in range(4):
            q = np.polyfit(bc[kb], Bot[bc][kb], 4); rb = Bot[bc] - np.polyval(q, bc)
            kb = np.abs(rb) < max(2.0, 2.0 * np.std(rb[kb]))
        tf = lambda c: float(np.polyval(p, c)); bf = lambda c: float(np.polyval(q, c))
        Sx = np.zeros(W)
        for c in range(a, b + 1):
            Sx[c] = max(0.0, bf(c) - tf(c) + 1.5)               # closes fully, onto the lower lid line
        ker = np.ones(9) / 9; Sx[a:b + 1] = np.convolve(np.pad(Sx[a:b + 1], 4, mode='edge'), ker, 'valid')
        span_max = 0
        for c in range(W):
            if np.isnan(Ltop[c]):
                continue
            if a <= c <= b:
                t = tf(c); s = Sx[c]
            else:                                          # a corner or a wing: it rides with the corner of the lid
                e_ = a if c < a else b; d = abs(c - e_)
                t = min(Bot[c] + 1.0, tf(e_) + 2.0)        # the wing above the lid line moves; a lower prong stays
                s = Sx[e_] * max(0.0, 1.0 - (d / 45.0) ** 2)
            T_all[c] = t; S_all[c] = s; span_max = max(span_max, s)
            colmask = F[:, c]
            above = np.arange(H) < t
            alpha = np.clip((l0 - lum[:, c]) / max(1e-3, l0 - lin), 0, 1)
            L_all[:, c] = np.maximum(L_all[:, c], colmask * above * alpha)
        core = _ero(_dil(L_all > 0.3, 1), 1) & F           # no pinholes in the lash line
        L_all = np.maximum(L_all, core.astype(np.float32))
        lash = F & dark
        if lash.any():
            lc = np.median(img[lash], 0)
            sel = (L_all > 0.02) & F
            img[sel] = lc
        F_all |= F
    return F_all, L_all, T_all, S_all


def mouth_seam(img, dep, mouth, x0, z1, px=PX):
    """The line where the lips part, as y = a + b*x + c*x^2 in three.js coordinates, and the half-width."""
    H, W = img.shape[:2]
    col = lambda x: int(round((x - x0) / px)); row = lambda z: int(round((z1 - z) / px))
    mx, mz = mouth["center"][0], mouth["center"][2]
    lum = img @ LUMA
    xs, zs = [], []; lips_hw = 0.0
    if mouth.get("kind") == "teeth":
        white = (lum > 0.82) & ((img.max(-1) - img.min(-1)) < 0.12)
        r0, r1 = row(mz + 0.05), row(mz - 0.05)
        for c in range(col(mx - 0.15), col(mx + 0.15)):
            rr = np.nonzero(white[r0:r1, c])[0]
            if len(rr) >= 2:
                xs.append(x0 + c * px); zs.append(z1 - (r0 + rr[-1] + 1) * px)    # just below the painted teeth
    else:
        # lips modelled in 3D: the crease is the deepest point between the upper and the lower lip,
        # searched only inside the lips (found by colour: redder and darker than the skin around them)
        sk = np.concatenate([img[row(mz) - 6:row(mz) + 6, col(mx + o * 0.15) - 6:col(mx + o * 0.15) + 6].reshape(-1, 3) for o in (-1, 1)])
        s0 = np.median(sk, 0)
        lipish = np.linalg.norm(img - s0, axis=-1) > 0.07
        seed = np.zeros((H, W), bool); seed[row(mz - 0.02) - 2:row(mz - 0.02) + 3, col(mx) - 2:col(mx) + 3] = True
        lips = _flood(seed, lipish & (np.abs(np.arange(W) * px + x0 - mx) < 0.13)[None, :])
        lips = _ero(_dil(lips, 2), 2)
        lc = np.nonzero(lips.any(0))[0]
        if len(lc): lips_hw = 0.88 * max(abs(x0 + lc.min() * px - mx), abs(x0 + lc.max() * px - mx))   # the opening stops short of the corners
        r0, r1 = row(mz + 0.02), row(mz - 0.09)
        for c in range(col(mx - 0.12), col(mx + 0.12)):
            rows_in = np.nonzero(lips[:, c])[0]
            if len(rows_in) < 8:
                continue
            r0, r1 = rows_in[0], rows_in[-1] + 1
            prof = dep[r0:r1, c]
            if len(prof) < 10:
                continue
            best = None
            for r in range(3, len(prof) - 3):
                v = prof[r]
                if v >= prof[r - 3:r + 4].max() - 1e-6:
                    up = prof[:r].min() if r else v; dn = prof[r + 1:].min()
                    prom = min(v - up, v - dn)
                    if prom > 0.004 and (best is None or prom > best[1]):
                        best = (r, prom)
            if best:
                xs.append(x0 + c * px); zs.append(z1 - (r0 + best[0]) * px)
    if len(xs) < 6:
        return None
    xs = np.array(xs); zs = np.array(zs)
    keep = np.ones(len(xs), bool)
    for _ in range(3):
        cf = np.polyfit(xs[keep], zs[keep], 2); res = zs - np.polyval(cf, xs); keep = np.abs(res) < max(0.003, 2.5 * np.std(res[keep]))
    xk = xs[keep]
    hw = max(float(max(abs(xk.min() - mx), abs(xk.max() - mx))), lips_hw)
    c2, c1, c0 = cf
    return {"a": round(float(c0), 5), "b": round(float(c1), 5), "c": round(float(c2), 4), "cx": round(float(mx), 4), "hw": round(float(hw), 4)}


def build(tex, pos, nor, covered, info):
    """Everything the runtime needs, plus the atlas image (H2 x W x 4, rows top-down, sRGB 0..1)."""
    eyes = info.get("eyes") or {}; mouth = info.get("mouth")
    if not eyes:
        return None, None
    ez = np.mean([e["center"][2] for e in eyes.values()]); eh = max(e["h"] for e in eyes.values())
    ew = max(e["w"] for e in eyes.values()); ex = max(abs(e["center"][0]) for e in eyes.values())
    x0, x1 = -(ex + ew * 0.85), ex + ew * 0.85
    z0, z1 = ez - eh * 1.1, ez + eh * 1.7
    img, dep = raster(tex, pos, nor, covered, x0, x1, z0, z1)
    F, L, T, S = eye_data(img, eyes, x0, z1)
    hole = _dil(F, 2)
    clean = _inpaint(img, hole)
    Fsoft = _dil(F, 1).astype(np.float32)
    Fsoft = (Fsoft + _shift(Fsoft, 1, 0) + _shift(Fsoft, -1, 0) + _shift(Fsoft, 0, 1) + _shift(Fsoft, 0, -1)) / 5
    H, W = img.shape[:2]
    atlas = np.zeros((H * 2, W, 4), np.float32)
    atlas[:H, :, :3] = img; atlas[:H, :, 3] = L
    atlas[H:, :, :3] = clean; atlas[H:, :, 3] = Fsoft
    front = float(-min(e["front_y"] for e in eyes.values()))
    data = {"px": PX, "x0": round(float(x0), 5), "top": round(float(z1), 5), "w": W, "h": H, "front": round(front, 4),
            "T": [round(float(v), 1) for v in T], "S": [round(float(v), 1) for v in S]}
    if mouth:
        mz = mouth["center"][2]; mxx = mouth["center"][0]
        mimg, mdep = raster(tex, pos, nor, covered, mxx - 0.2, mxx + 0.2, mz - 0.12, mz + 0.08)
        seam = mouth_seam(mimg, mdep, mouth, mxx - 0.2, mz + 0.08)
        if seam:
            seam["kind"] = mouth.get("kind", "lips")
            seam["front"] = round(float(-mouth["center"][1]), 4)
            data["mouth"] = seam
    return data, atlas
