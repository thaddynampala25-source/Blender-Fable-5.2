# Character design brief: premium 3D AI Language Buddies

The owner's brief for replacing the Week2Speak Language Buddies, saved so every
session works from the same requirements. The reference study and the agreed
visual direction are in `CHARACTER_REFERENCE_ANALYSIS.md`; the website is in
`website/week2speak/` (read its `PROJECT_HANDOFF.md` first).

Roles for Claude on this work: lead 3D character artist, creative director,
Blender technical artist and frontend engineer.

## 1. What is being built

An interactive language-learning site where learners practise speaking with
AI-powered 3D conversation partners called **Buddies**. The site already has:

- 3D avatars named Ruby and Max
- interactive conversation scenarios
- speech recognition and text input
- spoken tutor responses
- different tutor accents
- character switching
- conversation feedback and progress tracking

**The existing website must remain functional.** The goal is to turn the
avatars into a collection of beautifully designed, high-quality, animated 3D
characters with distinct personalities.

## 2. Primary visual reference

The official visualizer for **Trippie Redd – Miss The Rage ft. Playboi Carti**
(`references/miss-the-rage-reference.mp4`, key frames in `references/frames/`).

Study:

- smooth, high-quality stylised geometry
- exaggerated but deliberate facial proportions
- distinctive facial expressions and relaxed eyes
- detailed hairstyles
- streetwear styling and accessories
- strong, recognisable silhouettes
- material quality and lighting
- confident, expressive body language
- the overall quality of the character design

**Do not recreate Playboi Carti, Trippie Redd or their visualizer characters.**
Translate the design principles into original characters for a premium
language-learning product. They should look cool, fashionable and appealing to
teenagers and adults, not like children's educational-game mascots: the
friendliness and expressiveness of Duolingo's cast with the fashion-forward
attitude and sophistication of premium stylised 3D animation.

## 3. Problems with the current avatars

Ruby and Max are too basic: simplistic facial anatomy, very prominent wide-open
eyes, primitive-looking geometry, unconvincing hair, plastic-looking surfaces,
basic clothing with little detail, limited facial personality. **A substantial
redesign is wanted, not cosmetic adjustments.**

## 4. Initial cast

Four original characters, one cohesive art direction, very different looks and
personalities. These are starting points, not rigid specifications; explore
different visual concepts.

- **Kairo, the confident one.** A stylish young Black man with medium-length
  locs, expressive half-lidded eyes, a confident smile, fashionable layered
  streetwear, subtle jewellery and relaxed body language. Charismatic, funny,
  confident, laid-back.
- **Ruby, the fashionable one.** A stylish young woman with an auburn
  hairstyle, expressive green eyes, modern fashion and playful expressions.
  Witty, welcoming, intelligent, slightly sarcastic.
- **Max, the energetic one.** A young man with voluminous textured hair, an
  expressive face, modern casual fashion and energetic gestures. Friendly,
  enthusiastic, encouraging.
- **Nova, the alternative one.** Experimental fashion, an unconventional
  hairstyle, accessories and a creative silhouette. Adventurous, eccentric,
  expressive.

## 5. Quality requirements

- professionally designed facial topology
- smooth, sculpted geometry
- stylised but believable facial anatomy
- proper eyelids and eye shapes
- detailed hair geometry
- convincing fabric and clothing forms
- refined materials and shading
- expressive facial rigs
- distinctive poses and gestures
- smooth, polished animation

The result must not look assembled from spheres, cubes and cylinders. A high
polygon count is not good design: silhouette, proportions, modelling quality
and materials come first.

## 6. Animation and speech

The characters must blink naturally, keep eye contact, look around, listen
attentively, think before responding, lip-sync convincingly, smile and laugh,
show confusion, react positively to correct answers, and make subtle hand and
body gestures.

Build a **reusable animation system** with the states idle, listening,
thinking, speaking, success and confusion.

## 7. Website integration

- Create and animate the characters in Blender.
- Export web-compatible GLB/glTF with rigs, animation clips and facial shape keys.
- Inspect the existing site architecture before choosing the rendering integration.
- Preserve: conversation logic, microphone, text-to-speech, accent selection,
  scenario switching, conversation history, feedback and progress tracking.
- Replace the character visuals without rewriting the site.
- Optimise for desktop and mobile.

## 8. Development order

1. Inspect the existing website and Blender environment.
2. Study the visual references.
3. Establish a consistent character-design style.
4. Propose several character concepts.
5. Begin with Kairo.
6. Create a polished visual prototype.
7. Render front, side and three-quarter views.
8. Evaluate the visual quality against the references.
9. Refine the approved character.
10. Build the facial and body rigs.
11. Implement animation and speech integration.
12. Export and integrate the GLB into the website.
13. Test performance and interaction.
14. Expand the cast after the first character succeeds.

**Do not build all four at once.**

## 9. Standing instructions

- Visual quality is the highest priority. Do not rush into several simple characters.
- If procedural Blender modelling alone cannot reach the quality, research and
  recommend better workflows (external character-generation tools, sculpting,
  retopology, rigging tools) and explain the trade-offs.
- Never claim the output matches the reference unless real renders show
  comparable quality.
- Preserve the existing website and its functionality throughout.
- Agree the approach with the owner before generating characters.
