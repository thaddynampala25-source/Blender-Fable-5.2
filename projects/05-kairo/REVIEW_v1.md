# Kairo v1: critical review against the reference

Compared: `renders/checkpoint-01/` with `references/frames/01-03`, side by side
(`face_front.png` next to `01-face-closeup-relaxed.jpg`). v1 is preserved as `kairo_v1.blend`
and in git history (commit "Kairo: bust checkpoint").

Verdict: v1 is a competent procedural model, not a designed character. The reference
reads as a sculpted collectible figure; v1 reads as a realistic base mesh dressed up.

## Largest differences, in order of impact

| # | Area | Reference | Kairo v1 | Why it matters |
|---|---|---|---|---|
| 1 | **Face shape** | broad, soft, rounded planes; short mid-face; short nose with a wide lit tip; full cheeks | long narrow realistic face, tall forehead, long nose, hollow cheeks | the realistic skull is the main reason v1 looks "base mesh" |
| 2 | **Eyes and lids** | heavy upper lid covering ~45% of a dark iris; a thick dark upper lid line that extends past the outer corner; visible lower lid; eyes set wide | small eyes, thin lash line, lids only slightly lowered, light amber iris | the eyes carry the attitude; v1's read as tired, not cool |
| 3 | **Mouth and expression** | lips closed, wide mouth, corners lifted into a knowing half-smile, crisp lip edge | lips parted, heavy pouty lower lip, smile too faint to read | no personality without a readable expression |
| 4 | **Hair volume** | thick bulbous locs (≈ ⅛ of head width each), dense, layered, wider than the head, framing and overlapping the face | thinner rope locs, sparse at the crown, scalp showing at the parting, a flat curtain | silhouette and luxury both come from hair mass |
| 5 | **Outfit construction** | strong garment shapes, clear material contrast, trims | good details (pockets, stitching, buttons) but a uniform cobalt mass; vest hidden; collar same fabric; no wrinkles | the outfit reads as one smooth shell, not layered fashion |
| 6 | **Surface materials** | skin with warm subsurface glow and colour zones; glossy-vs-matte contrast; fabric texture visible | skin evenly coloured and slightly plastic; canvas weave too fine to see; no fabric weight | "procedural" look comes from uniform surfaces |
| 7 | **Production finish** | contrasty lighting, specular sparkle on hair and metal, soft depth of field | flat-ish key, no depth of field | small cost, large polish gain |

## What v1 already does well (keep)

Twisted-rope loc construction and colour fade; brows as graphic shapes; jacket details
(pockets, flaps, brass buttons, contrast stitching, seams); the speech-bubble charm; the
complementary cobalt-on-sunshine palette; the stage-by-stage rebuildable pipeline.

## Nothing childish to remove? Two things

- The A-pose with a big head and plain features reads as a toy. A broader but *adult* face
  (defined jaw, cheekbones, lid line, smirk) fixes that more than shrinking the head would.
- Uniform saturated colour blocks (all-cobalt jacket) read as kids' wear. Contrast trims,
  layering and texture read as fashion.

## v2 plan

1. Face: rounder, shorter, broader planes; shorter nose with a broad tip; fuller cheeks;
   defined jaw. Larger eyes with heavy lids (~45% cover), a sculpted dark upper lid line with
   an outer flick, darker iris with a limbal ring, warm sclera.
2. Mouth: lips closed, wider; asymmetric half-smile with a cheek lift; lip edge defined.
3. Skin: zone colouring (warmer cheeks, nose, ears; darker lids), stronger subsurface,
   specular break-up, glossier lips.
4. Hair: thicker, denser locs with real volume framing the face, a few falling across the
   forehead; no exposed parting; gold loc cuffs as jewellery.
5. Outfit: the knit vest shown at the front with navy rib trims; navy corduroy contrast
   collar; wider-open jacket; visible twill texture; wrinkles at arms and waist.
6. Finish: lighting contrast, depth of field on the close-ups.

Renders from the same cameras go to `renders/checkpoint-02/`.
