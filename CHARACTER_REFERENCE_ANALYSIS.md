# Character reference analysis and visual direction

What the *Miss The Rage* visualizer does well, what Week2Speak's Buddies should
take from it, and how we intend to reach a comparable polish in Blender and in
the browser. Requirements are in `CHARACTER_DESIGN_BRIEF.md`.

**Status: proposal, awaiting approval. No modelling has started.**

## 1. Source

- `references/miss-the-rage-reference.mp4`: 3 min 58 s, 1920x1080, 30 fps.
- Studied as 79 frames taken every 3 seconds (`references/frames/sheet-0..4.jpg`)
  plus full-resolution stills of the key shots (`references/frames/01-07*.jpg`).
- The video loops one set of shots: two stylised characters on a saturated
  red cyclorama, with a yellow SUV, a jewellery pendant close-up, 2D fire and
  lightning effects, dance moves, close-ups and extreme low angles.

These are likenesses of real artists. We study **how** they are made, not
**who** they are.

## 2. What makes the reference look premium

### 2.1 Proportions and silhouette

- **Heroic-stylised, not chibi.** The head (with hair) is about 1/4.5 to 1/5 of
  body height (frame 03). The current Buddies are about 1/3, which reads as a
  children's toy.
- Long slim legs, narrow hips, slightly broad shoulders, **big expressive hands**
  (often gloved), and **chunky footwear**. Body small, head and feet heavy.
  That contrast is what gives the "designer vinyl figure" read.
- **The silhouette is carried by the hair and clothing.** Locs make a wide,
  irregular mass around a narrow face; a cropped jacket or boxy jersey sets up
  a clear shape against slim trousers. Each character is recognisable as a
  flat black shape.

### 2.2 Face

- **Relaxed, heavy-lidded eyes are the main design note.** At rest the upper
  lid crosses the iris about a third to half of the way down. Small dark
  irises, a visible lower lid and under-eye fold, warm (not pure white)
  sclera, thin dark lash lines. That makes them look cool and knowing rather
  than wide-eyed (frames 01 and 02).
- **Graphic eyebrows.** Thick, dark, flat-shaded slabs with crisp ends sitting
  just proud of the skin. They make expressions readable from far away.
- **Long, specific features.** A long nose with defined nostril wings and a
  lit tip, full lips with a darker lip line and an asymmetric half-smile, a
  long narrow jaw, visible ears. The features are exaggerated but every one
  is anatomically placed. That is the "deliberate" quality.
- **Facial hair and markings are solid sculpted shapes**, not textures:
  the goatee is a clean slab with its own highlight.
- **Skin:** smooth and pore-less, warm subsurface glow where light passes
  through (ears, nose, fingers), a soft sheen on forehead and nose, and darker
  painted crease shading around the eyes and mouth.

### 2.3 Hair

- **Locs built as real geometry:** each one a tapering tube with a spiral
  twist pattern, a rounded tip, and slight variation in thickness and length.
- Grouped into clumps that obey gravity and the head shape. Several fall
  across the face and over one eye, which adds attitude and breaks symmetry.
- Darker roots at the scalp with a visible parting, so the hair grows *out of*
  the head rather than sitting on it like a helmet.
- The twists catch strong, sparkling highlights. That surface detail is a
  large part of why the hair looks expensive.

### 2.4 Clothing, materials and accessories

- **Thick, simplified fabric:** a few big confident folds at elbows, knees and
  cuffs; compression gathers at elastic ankles; clean seam lines; piping
  stripes; buttons and poppers as real geometry.
- **Material contrast is the trick.** Glossy leather with streaky
  high-contrast highlights next to matte knit, next to sparkling jewellery,
  next to soft skin. Each surface reads as what it is from across a room.
- **Accessories as hero props:** cuban-link chains with modelled links, pavé
  pendants with individual stones, gloves with a bold graphic print, chunky
  sneakers with real sole tread.

### 2.5 Lighting and render

- A **saturated single-colour cyclorama**, so the character is the only
  complex thing in frame.
- **A strong warm yellow-white kick light** from one side, high and behind.
  It draws a hot edge along hair, shoulders and leather, plus a soft frontal
  key. The red environment bounces into the shadows and tints the skin.
- High contrast, filmic tone mapping, occasional shallow depth of field,
  extreme low and wide angles for drama.
- Full path-traced global illumination (an offline render), plus 2D-style fire
  and lightning overlays.

### 2.6 Body language

- Contrapposto stances, loose shoulders, head tilts, chin up for confidence or
  down for attitude; crossed arms; a hand brought to the face.
- Every finger posed; hands do half the acting.
- Animation is loose and rhythmic, with weight shifts and overlapping
  movement in the locs.

## 3. Why the current Buddies fall short (measured against 2.1–2.6)

| Area | Ruby and Max today | Reference standard |
|---|---|---|
| Proportion | head ~1/3 of height, short stubby limbs: a toddler toy | head ~1/5, long limbs, big hands and feet |
| Eyes | large, round, fully open, bright white sclera | relaxed lids, small irises, warm sclera, readable lid folds |
| Brows and features | thin, low-contrast; small generic nose and mouth | graphic brows, specific nose and lips, asymmetric expressions |
| Hair | one smooth blob (Ruby) or a field of bumps (Max) | strand groups with twist detail, roots, gravity, face overlap |
| Clothing | smooth inflated shells, no seams or folds | seams, piping, folds, gathers, real buttons |
| Materials | vertex colour, one plastic-like finish everywhere | leather vs knit vs metal vs skin contrast |
| Hands | mitten-like | posed fingers, gloves, rings |
| Lighting | flat lavender, soft fill, small rim | strong coloured kick light, coloured bounce |

The handoff itself rates the models "about 60% of the way to a hand-sculpted
film character". This is a redesign, not a tune-up.

## 4. What we take, adapt and avoid

**Take as-is (craft principles):** heroic-stylised proportions, relaxed lids,
graphic brows, hair as the silhouette, strand-group hair with surface detail,
material contrast, hero accessories, the kick-light lighting recipe, posed hands.

**Adapt for a learning product:**
- The default expression is relaxed **and warm**: half-lidded but smiling,
  with eye contact. Lids open further when listening or excited, so the
  "cool" look never reads as bored or dismissive to a nervous learner.
- **Week2Speak's palette replaces the red.** Cobalt `#2D4BFF`, sunshine
  `#FFD93B` and navy `#0B103A` are the cast's shared accent colours. Each
  character also gets a signature colour of its own.
- **Jewellery is subtle and brand-linked**: small hoops, a thin chain, maybe a
  small speech-bubble charm as a cast-wide motif.

**Avoid (identity and suitability):**
- Any likeness of either artist: no face tattoos, no red locs, no
  black-and-white striped jersey with an iced moon pendant, no red-piped
  leather jacket with goatee combination, no SUV.
- Smoking, weapons and the other props in the video.
- Copying any specific garment, logo or graphic from the video.

## 5. Proposed visual direction

**One-line pitch:** *designer-vinyl streetwear figures with film-quality faces.*
Like premium collectible figures that come alive, where the hair, the fabrics
and the eyes do the talking.

Style rules for the whole cast:

1. Head with hair = 1/4.5–1/5 of height; hands and shoes slightly oversized.
2. Eyes: relaxed upper lid at rest (crossing the iris about 25–35%), real lid
   geometry, warm sclera, coloured iris with a soft catchlight.
3. Brows: thick, simplified, graphic; the main expression driver.
4. Every face has one asymmetry: a half-smile, a raised brow, hair over one eye.
5. Hair always reads as grouped strands or locks with surface detail, never a cap.
6. Each outfit has at least three contrasting materials and one hero accessory.
7. Signature lighting for renders: cobalt-to-navy cyclorama, warm yellow kick
   light, cool fill. The same recipe goes into the web lighting rig.

### Kairo concepts (first character; pick one, or mix)

- **A. Studio cool.** Shoulder-length locs, dark brown with honey-gold tips,
  a few tied up in a half-bun and a couple falling across one eye. Boxy
  cropped cobalt work jacket (thick canvas, contrast stitching, real
  buttons) over a long white tee and a loose sunshine-yellow knit vest.
  Wide navy cargo trousers, chunky cream sneakers. Small silver hoop, one
  thin chain. A laid-back half-smile.
- **B. Night runner.** Locs pulled back under a ribbed beanie, with a few
  loose at the front. Glossy navy puffer vest (the leather-equivalent hero
  material) over a cobalt hoodie, sunshine-yellow drawcords and piping,
  tapered joggers with elastic gathers, high-top sneakers. Wireless
  earbuds case on a lanyard as the prop.
- **C. Smart-casual creative.** Mid-length locs loose with gold cuffs.
  Oversized cream overshirt in corduroy (strong texture) over a navy turtleneck,
  pleated wide trousers, loafers with chunky soles. A small rings stack;
  pencil tucked behind ear. Reads "older sibling who's studied abroad".

Recommendation: **A**. It has the strongest silhouette, the clearest
material contrast and the most natural fit with the brand colours.

### The rest of the cast (outlines only, after Kairo succeeds)

- **Ruby:** auburn hair in a sharp, glossy, jaw-length bob with a curtain fringe
  (or a high sleek ponytail as an alternative). Oversized cobalt rain trench
  in a coated, slightly shiny fabric over a knit; yellow headphones kept as
  her link to the current Ruby. Green eyes, an arched sarcastic brow.
- **Max:** big voluminous textured curls or a high-top, a sunshine-yellow
  zip-up track top with navy stripes, baggy denim, retro runners. The most
  open eyes in the cast (energetic), with big hand gestures.
- **Nova:** a sculptural silhouette: two-tone buzzed hair with a bleached
  graphic pattern, or space buns with braided cords. Layered asymmetric
  techwear: harness straps, oversized utility vest, mesh sleeves, chunky
  platform boots, an ear cuff and visor glasses. Teal or violet as her
  signature colour so she stands apart.

## 6. Reproducing the polish

### 6.1 The honest gap: offline render vs live phone render

The reference is path-traced offline: one frame can take minutes. Our
Buddies draw live in three.js on phones at 30–60 fps. So there are two targets:

| Output | Engine | How close to the reference it can get |
|---|---|---|
| Turnarounds, posters, the static `.webp` pictures, marketing | Blender Cycles | close: same lighting recipe, real subsurface scattering, path tracing |
| The live Buddy on the site | three.js (WebGL 2) | lower: the shapes, silhouettes, hair and expressions carry over fully; lighting and materials are approximated |

To make the live version as close as possible:
- Bake ambient occlusion, cavity and soft lighting gradients into the base
  colour textures, so the shading depth is "painted in".
- Use normal maps for loc twists, stitching and knit, instead of geometry.
- Use three.js `MeshPhysicalMaterial` sheen for fabric and clearcoat for
  glossy materials.
- Light with an environment map generated at runtime (no file to download,
  no request to another domain), keep the existing rim-light shader, and
  switch the tone mapping to AgX.
- Key the live lights to the render recipe (warm kick light plus coloured
  bounce).

### 6.2 Modelling workflow options

| Workflow | Quality ceiling | Topology and rig | Cost and risk | Verdict |
|---|---|---|---|---|
| **1. Pure procedural (how the current Buddies are made)** | low–medium | custom | free; this is what produced the current look | rejected for faces and bodies |
| **2. MPFB 2 base (free Blender add-on, CC0 output) + scripted stylisation in Blender** | medium–high | clean animation topology, standard skeleton, face rig available | free; installs here (extensions.blender.org reachable). Risk: stylising a realistic base far enough takes care | **recommended base** |
| **3. AI image-to-3D (Hyper3D Rodin, Tripo, Meshy, Hunyuan3D via the MCP `generate_3d` tool)** | high for a still image | messy triangles, lighting baked into the texture, no rig; needs remeshing and re-rigging | needs your API key and credits; results vary per run; licence terms per vendor | **optional helper** for concept sculpts and props |
| **4. A human character artist sculpts (ZBrush or Blender), Claude rigs, exports and integrates** | highest | as good as the artist | money and time (days per character) | **fallback** if 2 + 3 miss the bar |
| **5. Character creators (Reallusion CC, VRoid, avatar services)** | varies | good rigs | licence limits for web delivery, recognisable "house" look, anime style (VRoid) | not recommended |

**The limitation to know about:** I can't sculpt with a pen tablet. Everything
I build is driven from code: Python in Blender, geometry nodes, modifiers,
sculpt operations run from scripts. That suits:
- hair, locs especially: twisted tapering tubes made in geometry nodes, a
  strength;
- clothing shells made from the body, with seams, piping, buttons and cloth
  simulation for folds;
- accessories, materials, lighting, rigging, shape keys, animation, export and
  integration.

**Faces are the riskiest part to do in code.** Starting from a professionally
built base mesh (MPFB) gets the anatomy and edge flow right. We then push the
proportions (lids, brows, nose, jaw, lips) with scripted shape edits, and
verify with renders.

### 6.3 Recommended pipeline (Kairo first)

1. **Bust test (go/no-go gate).** MPFB base, stylised head, relaxed-lid eyes
   with real lids, graphic brows, the locs system, a collar, the jacket
   shoulders.
   - Cycles renders: front, three-quarter, side and a close-up, under the
     signature lighting.
   - The same bust rendered in three.js at phone size.
   - **We compare both side by side with `references/frames/01-02` and you
     decide.** If the face doesn't reach the bar, we escalate to workflow 3
     or 4 before building anything else.
2. **Full body.** Proportion pass, hands with real fingers, clothing with
   seams and simulated folds, sneakers, accessories. Front, side and
   three-quarter turnarounds. Your review.
3. **Low-poly and bake.** A ~30–45k-triangle web version; bake normal,
   ambient-occlusion and colour maps into 1k–2k texture atlases.
4. **Rig.**
   - Body: a standard deform skeleton of about 60 bones, built with Rigify
     controls but exporting only the deform bones.
   - Face: about 30 shape keys: the five vowel mouth shapes (visemes) plus
     closed-mouth shapes (`viseme_PP`, `viseme_FF` and so on), jawOpen,
     blinks, lid squints, brow up/down/inner, smile, frown, cheek puff,
     sneer, and mouth-left/right for asymmetric smirks.
   - Eye bones for gaze.
5. **Animation clips in Blender:** idle (two variants), listening, thinking,
   speaking gesture loops (three), success, confusion, wave, plus a few
   personality moves for the poke reactions.
6. **Runtime (`buddies.js`).**
   - Add a three.js `AnimationMixer` layer playing the clips, blended by the
     six-state machine (idle, listening, thinking, speaking, success,
     confusion), driven by the existing `w2s:*` events.
   - Keep the procedural layer for gaze, blinking, lip sync and the live poke
     reactions, applied relative to bone rest poses (handoff planned
     improvement 1).
   - Keep the `mila` and `rio` ids, the events, `W2SBuddies`, the webp
     fallbacks, quality stepping and tests. Kairo becomes a third Buddy
     option; Ruby and Max stay until their replacements are approved.
7. **Export, integrate, test.**
   - GLB with no Draco, as today.
   - Run `npm test` and `npm run test:buddies`, extended for the new rig, plus
     `?fps=1` on a mid-range phone profile.

### 6.4 Budgets per character (live version)

| Item | Target |
|---|---|
| Triangles | 30–45k (today about 85k, spent on smooth blobs rather than detail) |
| Draw calls | ≤ 15 (today about 27) |
| Bones | ~60 deform bones + eye bones |
| Face shape keys | ~30 |
| Textures | body atlas, head atlas and hair: 1k each on phones, 2k on desktop |
| GLB size | ≤ 2 MB is the current spec. Textures will probably need 2.5–3.5 MB, or a compressed-texture loader (a new dependency): **your call** |

### 6.5 Quality checks before any "it matches" claim

At each review, renders next to the reference frames, judged on:
1. Silhouette test: the black-fill silhouette is recognisable and distinct from the other cast members.
2. Face at 25% size: expression still reads.
3. Lids, brows and mouth: no doll stare; at least one asymmetry.
4. Hair: strand groups, roots, overlap with the face; no helmet.
5. Materials: at least three distinguishable surfaces under one light.
6. Hands: five distinct fingers, a posed gesture.
7. Live (three.js) version reviewed separately from the Cycles render, with the gap stated.

## 7. Decisions needed before modelling

1. Approve the visual direction, and choose Kairo concept A, B, C or a mix.
2. Approve the workflow: MPFB base + scripted stylisation, gated by the bust test.
3. Optional: API keys for an image-to-3D tool (workflow 3), and whether to
   budget for a human sculptor if the bust test fails.
4. The GLB size budget (keep ≤ 2 MB, or allow ~3 MB or a texture-compression loader).
5. Whether Kairo joins as a third Buddy alongside Ruby and Max, or Ruby and
   Max are redesigned in place first. (Recommended: Kairo as a new third
   option, so nothing that works today changes.)
