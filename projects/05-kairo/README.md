# Kairo: the first premium Language Buddy

Concept A ("studio cool") from `CHARACTER_REFERENCE_ANALYSIS.md`: shoulder-length locs fading
from dark brown to honey-gold, half-up with a yellow tie; a cropped, boxy cobalt canvas
work jacket over a sunshine-yellow ribbed knit vest and a long white tee; a silver hoop and
a thin chain with a speech-bubble charm.

**Status: bust checkpoint (visual review). Not rigged, animated or integrated yet.**

## Workflow (agreed with the owner)

MPFB 2 base mesh (clean animation topology, real eyelids, mouth interior, skeleton-ready),
pushed to heroic-stylised proportions by script; everything else built procedurally in
Blender. Nothing is sent to outside services.

| Stage | Script | Produces |
|---|---|---|
| install | `install_mpfb.sh` (+ `install_mpfb.py`) | MPFB 2.0.18, checksum-verified, enabled in the live Blender |
| 1 | `base.py` | MPFB human: male, 25, lean, African macro → `work/base.blend` |
| 2 | `face.py` | MPFB face targets: hooded lids, long face, chin, nose, lips |
| 3 | `stylise.py` | head ×1.36, thicker neck, hands, legs; relaxed lid rotation; half-smile |
| 4 | `dress.py` | eyes (procedural iris, glossy cornea), graphic brows, lash lines, skin shader |
| 6 | `clothes.py` | tee, knit vest, jacket shells; collar, pockets, flaps, brass buttons, seams, stitching |
| 5 | `hair.py` | locs grown with collision against head and jacket; twisted-rope geometry nodes; tie |
| 8 | `accessories.py` | hoop earring, chain, speech-bubble charm → **`kairo.blend`** |

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

`renders/checkpoint-01/`: the bust checkpoint shown to the owner.
