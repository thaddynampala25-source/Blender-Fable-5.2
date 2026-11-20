# Chibi Buddy template: technical report

Source: `references/model.glb` (kept unchanged). Web copy: `w2s-site/buddy-models/template.glb`,
made by `w2s-site/buddy-gen/optimize_template.py` (Blender, local, no paid services).

## 1. What the file is

| Item | Found |
|---|---|
| Format | glTF 2.0 binary (`.glb`), written by `pygltflib` (the usual signature of AI image-to-3D output) |
| Size | 50.3 MB |
| Meshes | 1 mesh, 1 primitive, everything fused (body, clothes, hat, hair, face) |
| Geometry | 1,516,848 triangles, 802,685 vertices; positions, normals, one UV set |
| Material | 1 PBR material: base-colour texture, metallic 0, roughness 0.8, double-sided, opaque |
| Texture | 1 × 4096×4096 JPEG (6.4 MB); the eyes, brows, beard and teeth are painted into it |
| Skeleton | none |
| Animations | none |
| Morph targets (face shapes) | none |
| Placement | 1.9 units tall, centred on the origin (not standing on y = 0), facing +Z |

## 2. Suitable for the browser?

**As delivered: no.** 50 MB and 1.5 M triangles is about 25× the site's model budget
(< 2 MB, ~85 k triangles) and would stall phones.

**After optimisation: yes.** Decimated to 70 k triangles, texture 2048 px, feet on the floor,
2.2 units tall, framing data added. 2.2 MB raw, **1.75 MB as downloaded** (gzip), 1 draw call
for the model (3 in the scene), close-ups indistinguishable from the original apart from a
slightly softer knit on the beanie. The original stays in `references/`.

## 3. Suitable for speech animation?

**Not in its current form.** The things speech animation needs are missing or baked in:

| Need | In the template |
|---|---|
| a mouth that opens and shapes vowels | the mouth is modelled **open in a fixed grin**, teeth painted on; no lips to move |
| blinking and gaze | eyes are painted on the surface: no eyeballs, no eyelids |
| a skeleton for head turns and gestures | none; the mesh is one fused shell (hat, hair and body joined) |
| face shapes (visemes, blink, brows) | none |

So on the site today Kairo gets: the whole-body reactions (hop, squash and stretch, spin,
pop-in, pokes by body region), sound, all conversation events and the subtitle with word
highlighting. He does **not** get lip sync, blinking, gaze or arm and head gestures: the
runtime computes them but there is nothing on this model for them to move. The Buddy test
says so in its `notes`.

## 4. Suitable as a reusable character system?

**As a visual style: yes.** It is appealing, clear at phone size and consistent with a
premium chibi look.

**As a technical template: no, not yet.** Every character made the same way would arrive as
another fused, unrigged scan with its own topology, so nothing (rig, face shapes, animation
clips) could be shared between characters.

## 5. What realistic facial animation would need

Two routes, cheapest first.

**A. Chibi "swap" face (fits this style, days not weeks).**
1. Cut the face region out of the texture and rebuild the eyes and mouth as separate
   small meshes ("cards") lying on the face.
2. Paint 8–10 mouth shapes (closed, A, E, I, O, U, F/V, M/B/P, smile, laugh) and 3 eye states
   (open, half, closed) as texture tiles; the runtime swaps tiles per word (the lip sync already
   produces the shape names).
3. Add a simple skeleton (hips, spine, neck, head, arms) with auto-weights for head turns and
   gestures; split the beanie and locs so they follow the head.

**B. Full 3D face (the approach for many characters sharing one rig).**
1. Retopology into a clean, animation-ready mesh with edge loops round the eyes and mouth
   (or wrap one shared base topology onto each character so all of them share UVs and rig).
2. Separate parts: eyeballs, eyelids, mouth interior (teeth, tongue), hair and hat.
3. Re-bake the texture onto the new UVs; neutral, closed-mouth face.
4. A standard skeleton (Mixamo/Rigify-compatible names) with skin weights.
5. Face shapes: the Oculus visemes plus blink, brows, smile and frown (ARKit names). The
   runtime already finds these by name.
6. Runtime: apply gestures relative to each bone's rest pose (handoff §13, item 1).

## 6. Problems flagged

1. **Size** (50 MB): handled by the optimised web copy.
2. **Fixed open grin and painted eyes:** no speech animation possible without route A or B.
3. **No rig, no face shapes, one fused mesh:** see above.
4. **Origin at mid-height:** fixed in the web copy (feet on y = 0).
5. **Licence:** please confirm the template's licence allows commercial use on the site and
   modification (retopology, rigging) before investing in route A or B.
6. **Site copy:** the FAQ and About page (SEO text) still describe Ruby and Max. Not changed,
   because the site rules ask for the owner's say-so on SEO text.

## 7. How it is wired in

- `w2s-site/buddy_roster.py` lists the Buddies; `active: True` decides who appears. Today only
  Kairo (the template) is active; Ruby and Max are kept, switched off, with their ids
  `mila` and `rio` unchanged.
- The build copies the active models and pictures and writes the roster into
  `assets/config.js`; the Speech Mode screen, the app and `buddies.js` read it.
- With one active Buddy the Switch Buddy button is hidden; with two or more it cycles.
- `npm run posters` renders each active Buddy's static picture from the real model.
