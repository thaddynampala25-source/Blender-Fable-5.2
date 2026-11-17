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
LID_UP, LID_LOW = 0.30, -0.07      # radians: upper lid down, lower lid up


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

    # the half-smile: lift the character's left mouth corner (and a little of the cheek above it),
    # the right corner barely, so the resting face already has an attitude
    lips = set(v.index for v in me.vertices if any(g.group == ob.vertex_groups["lips"].index and g.weight > 0.3 for g in v.groups))
    lc = co[list(lips)]
    for sgn, up, back in ((1, 0.0095, 0.0032), (-1, 0.0035, 0.0012)):
        corner = lc[np.argmax(lc[:, 0] * sgn)]
        d2 = ((co - corner) ** 2).sum(1)
        g = np.exp(-d2 / (2 * 0.013 ** 2)) * body
        co[:, 2] += up * g
        co[:, 1] += back * g
        co[:, 0] += sgn * 0.0028 * g
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
    me.vertices.foreach_set("co", co.ravel()); me.update()
    h = co[body, 2].max(); hz = co[body, 2].max() - (chin - (chin - neck_top) )
    print("height", round(h, 3))
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)
