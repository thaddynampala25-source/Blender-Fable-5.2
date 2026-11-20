"""Stage 3: push MPFB's realistic proportions to Kairo's heroic-stylised ones
(work/face.blend -> work/stylised.blend).

Bakes the targets into the mesh, then moves every vertex (helpers included, so eyes,
teeth and the future rig joints follow) with smooth falloffs:
  head x HEAD about the top of the neck, hands x HAND about the wrists,
  legs lengthened by LEG below the hips.
"""
from pathlib import Path
import numpy as np
import bpy
from bl_ext.user_default.mpfb.services.targetservice import TargetService

HERE = Path(__file__).resolve().parent
SRC, OUT = HERE / "work" / "face.blend", HERE / "work" / "stylised.blend"
HEAD, HAND, LEG, NECK = 1.36, 1.14, 1.05, 1.22
LID_UP, LID_LOW = 0.27, -0.08      # radians: upper lid down, lower lid up
EYE_SCALE = 1.3
SMOOTH_ITERS = 8


def ss(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def group_center(ob, name, co):
    gi = ob.vertex_groups[name].index
    idx = [v.index for v in ob.data.vertices if any(g.group == gi and g.weight > 0.5 for g in v.groups)]
    return co[idx].mean(axis=0), idx


bpy.ops.wm.open_mainfile(filepath=str(SRC))
with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
    ob = bpy.data.objects["Kairo.body"]
    TargetService.bake_targets(ob)
    me = ob.data
    n = len(me.vertices)
    co = np.zeros(n * 3); me.vertices.foreach_get("co", co); co = co.reshape(n, 3)
    body = np.zeros(n, bool)
    gi = ob.vertex_groups["body"].index
    for v in me.vertices:
        body[v.index] = any(g.group == gi for g in v.groups)

    eye, _ = group_center(ob, "helper-l-eye", co)
    top = co[body, 2].max()
    # chin: lowest body vertex near the face's centre line in front of the neck
    front = body & (np.abs(co[:, 0]) < 0.02) & (co[:, 2] > eye[2] - 0.2) & (co[:, 1] < eye[1] + 0.02)
    chin = co[front, 2].min()
    neck_top = chin - 0.015
    pivot = np.array([0.0, eye[1] + 0.055, neck_top])
    print("top", round(top, 3), "eye z", round(eye[2], 3), "chin", round(chin, 3))

    # head: full scale above the chin line, fading out down the neck
    w = ss(neck_top - 0.09, neck_top + 0.01, co[:, 2])
    s = 1 + (HEAD - 1) * w
    co = pivot + (co - pivot) * s[:, None]
    # neck: thicken (x and y only) so the bigger head sits on a matching neck, fading out at the collarbones
    wn = ss(neck_top - 0.22, neck_top - 0.10, co[:, 2]) * (1 - w)
    sn = 1 + (NECK - 1) * wn
    co[:, 0] = co[:, 0] * sn
    co[:, 1] = pivot[1] + (co[:, 1] - pivot[1]) * sn

    # hands: scale about each wrist, fading in from the wrist
    for side, sx in (("l", 1), ("r", -1)):
        wrist_x = np.sign(sx) * 0.0
    xs = np.abs(co[:, 0]); hips_z = co[body, 2].min() + 0.0
    # wrist position: MPFB A-pose; find the outermost body x and take 0.17 m inwards along x
    outer = xs[body].max()
    wx = outer - 0.17
    for sgn in (1, -1):
        m = (np.sign(co[:, 0]) == sgn)
        wh = ss(wx - 0.01, wx + 0.04, xs) * m
        piv = np.array([sgn * wx, 0, 0])
        sel = wh > 0
        if sel.any():
            pz = co[m & (np.abs(xs - wx) < 0.015) & body, 2].mean()
            py = co[m & (np.abs(xs - wx) < 0.015) & body, 1].mean()
            piv = np.array([sgn * wx, py, pz])
            co = co + (piv + (co - piv) * HAND - co) * wh[:, None]

    # legs: stretch everything below the crotch downward, then put the feet back on the floor
    crotch = co[body & (np.abs(co[:, 0]) < 0.01), 2]
    crotch = np.percentile(crotch, 5) + 0.06
    wl = 1 - ss(crotch - 0.15, crotch, co[:, 2])
    co[:, 2] = co[:, 2] + (co[:, 2] - crotch) * (LEG - 1) * wl
    co[:, 2] -= co[body, 2].min()

    # v2: larger eyes. Scale each eye socket (lids, surrounding skin and the eyeball helper
    # together) about the eye centre, fading out across the brow, cheek and temple.
    for side in ("l", "r"):
        c, idx = group_center(ob, f"helper-{side}-eye", co)
        r = float(np.linalg.norm(co[idx] - c, axis=1).mean())
        d = np.linalg.norm(co - c, axis=1)
        w = ss(r * 3.0, r * 1.4, d)
        co = c + (co - c) * (1 + (EYE_SCALE - 1) * w)[:, None]

    lips = set(v.index for v in me.vertices if any(g.group == ob.vertex_groups["lips"].index and g.weight > 0.3 for g in v.groups))
    lc = co[list(lips)]
    # v2: close the mouth. Find the mouth line (the most recessed lip vertices on the centre
    # line) and squeeze the band around it together, most at the middle, fading to the corners.
    centre = lc[np.abs(lc[:, 0]) < 0.004]
    mid = centre[(centre[:, 2] > np.percentile(centre[:, 2], 25)) & (centre[:, 2] < np.percentile(centre[:, 2], 75))]
    zm = mid[np.argmax(mid[:, 1]), 2]
    half_w = np.abs(lc[:, 0]).max()
    lipmask = np.zeros(len(co)); lipmask[list(lips)] = 1
    dz = co[:, 2] - zm
    wx = np.clip(1 - (np.abs(co[:, 0]) / (half_w * 1.05)) ** 2, 0, 1)
    wz = np.exp(-(dz / 0.007) ** 2)
    k = 1 - 0.75 * wx * wz * lipmask
    co[:, 2] = zm + dz * k
    print("mouth line z", round(float(zm), 4))

    # relaxed lids: rotate the upper lid down about each eye's centre (as a lid bone would),
    # and lift the lower lid a touch
    for side in ("l", "r"):
        c, idx = group_center(ob, f"helper-{side}-eye", co)
        r = float(np.linalg.norm(co[idx] - c, axis=1).mean())
        rel = co - c
        d = np.linalg.norm(rel, axis=1)
        front = rel[:, 1] < r * 0.2
        wd = ss(r * 1.75, r * 1.08, d) * body * front
        for sign, ang in ((1, LID_UP), (-1, LID_LOW)):
            m = (rel[:, 2] * sign > -r * 0.05)
            w = wd * m * np.clip(np.abs(rel[:, 2]) / (r * 0.35), 0, 1)
            th = ang * w
            y, z = rel[:, 1], rel[:, 2]
            ny = y * np.cos(th) - z * np.sin(th); nz = y * np.sin(th) + z * np.cos(th)
            co[:, 1] = c[1] + ny; co[:, 2] = c[2] + nz
            rel = co - c
    # v2: simplify the face into smooth sculpted planes (the stylised look): Laplacian smoothing
    # over the head, protecting the lid margins, the eyeballs and the lip line
    eyes_c = [group_center(ob, f"helper-{sd}-eye", co) for sd in ("l", "r")]
    w = (ss(neck_top - 0.03, neck_top + 0.03, co[:, 2]) * body).astype(float)
    for c, idx in eyes_c:
        r = float(np.linalg.norm(co[idx] - c, axis=1).mean())
        w *= ss(r * 1.15, r * 1.9, np.linalg.norm(co - c, axis=1))
    lipw = np.zeros(len(co)); lipw[list(lips)] = 1
    w *= 1 - 0.7 * lipw
    e = np.array([[ed.vertices[0], ed.vertices[1]] for ed in me.edges])
    deg = np.bincount(e.ravel(), minlength=len(co)).astype(float)
    for _ in range(SMOOTH_ITERS):
        acc = np.zeros_like(co)
        np.add.at(acc, e[:, 0], co[e[:, 1]]); np.add.at(acc, e[:, 1], co[e[:, 0]])
        avg = acc / np.maximum(deg, 1)[:, None]
        co = co + (avg - co) * (0.5 * w)[:, None]

    # the half-smile: corners lifted and pulled back, his left side more, with the cheek above
    # it rising and a soft crease beside it: a knowing smile, not a grin
    lc = co[list(lips)]
    for sgn, up, back, out, cheek in ((1, 0.0120, 0.0050, 0.0040, 0.0055), (-1, 0.0055, 0.0028, 0.0020, 0.0025)):
        line = lc[np.abs(lc[:, 2] - zm) < 0.005]            # the corner is the end of the mouth line
        corner = line[np.argmax(line[:, 0] * sgn)]
        d2 = ((co - corner) ** 2).sum(1)
        g = np.exp(-d2 / (2 * 0.011 ** 2)) * body
        co[:, 2] += up * g
        co[:, 1] += back * g
        co[:, 0] += sgn * out * g
        # cheek lift above and outside the corner
        ck = corner + np.array([sgn * 0.022, -0.004, 0.03])
        gc = np.exp(-((co - ck) ** 2).sum(1) / (2 * 0.018 ** 2)) * body
        co[:, 2] += cheek * gc
        co[:, 1] -= cheek * 0.6 * gc
        # a small dimple just outside the corner sells the smirk (his left side only)
        if sgn > 0:
            dp = corner + np.array([0.007, 0.0, 0.003])
            gd = np.exp(-((co - dp) ** 2).sum(1) / (2 * 0.004 ** 2)) * body
            co[:, 1] += 0.0028 * gd
    me.vertices.foreach_set("co", co.ravel()); me.update()
    h = co[body, 2].max(); hz = co[body, 2].max() - (chin - (chin - neck_top) )
    print("height", round(h, 3))
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)
