# Kairo: the first premium Language Buddy

Concept A ("studio cool") from `CHARACTER_REFERENCE_ANALYSIS.md`: chunky shoulder-length locs
fading from dark brown to honey-gold, a side-swept fringe and gold loc cuffs; a cropped, boxy
cobalt twill work jacket worn open with a navy corduroy collar, over a sunshine-yellow ribbed
knit vest with navy trims and a long white tee; a silver hoop and a thin chain with a
speech-bubble charm.

**Status: v2 bust checkpoint (visual review). Not rigged, animated or integrated yet.**

| Version | File | Renders | Notes |
|---|---|---|---|
| v1 | `kairo_v1.blend` (and git commit "Kairo: bust checkpoint") | `renders/checkpoint-01/` | critical review: `REVIEW_v1.md` |
| v2 | `kairo.blend` | `renders/checkpoint-02/` | face resculpt, lid lines, closed smirk, thicker locs, outfit layering |

To go back to v1: open `kairo_v1.blend`, or check out the v1 commit's scripts and run `build.sh`.

## Workflow (agreed with the owner)

MPFB 2 base mesh (clean animation topology, real eyelids, mouth interior, skeleton-ready),
pushed to heroic-stylised proportions by script; everything else built procedurally in
Blender. Nothing is sent to outside services.

| Stage | Script | Produces |
|---|---|---|
| install | `install_mpfb.sh` (+ `install_mpfb.py`) | MPFB 2.0.18, checksum-verified, enabled in the live Blender |
| 1 | `base.py` | MPFB human: male, 25, lean, African macro → `work/base.blend` |
| 2 | `face.py` | MPFB face targets: broad, soft face; short nose with a broad tip; wide-set eyes; wider mouth |
| 3 | `stylise.py` | head ×1.36, thicker neck, hands, legs; larger eyes; relaxed lid rotation; closed mouth; face smoothing; half-smile and dimple |
| 4 | `dress.py` | eyes (procedural iris with limbal ring, glossy cornea), graphic brows, traced lid lines with flick, zoned skin shader |
| 5 | `clothes.py` | tee, knit vest (navy trims), open jacket shell with twill and folds; corduroy collar, pockets, flaps, brass buttons, seams, stitching |
| 6 | `hair.py` | locs grown with collision against head and jacket; twisted, swelling rope geometry nodes; fringe; gold cuffs |
| 7 | `accessories.py` | hoop earring, chain, speech-bubble charm → **`kairo.blend`** |

Run everything: `projects/05-kairo/build.sh` (Blender must be up: `scripts/blender-up.sh`).

## Renders

```bash
blender -b projects/05-kairo/kairo.blend --python projects/05-kairo/render_views.py -- bust  <outdir> 64 1080x1350
blender -b projects/05-kairo/kairo.blend --python projects/05-kairo/render_views.py -- face  <outdir> 64 1080x1200
blender -b projects/05-kairo/kairo.blend --python projects/05-kairo/render_views.py -- body  <outdir> 64 1080x1620
```

`studio.py` holds the cyclorama (sunshine yellow, so the cobalt jacket reads as its
complement), the lighting recipe (warm key, hot yellow kick light behind, cool fill, top light)
and the cameras. Cycles CPU, AgX Medium High Contrast.

`renders/checkpoint-01/` and `checkpoint-02/`: the same cameras and settings, for direct comparison.
