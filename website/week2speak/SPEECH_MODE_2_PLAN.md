# Speech Mode 2.0: audit and implementation plan

Status of each item is kept in the table at the end. Nothing below claims a capability the
code does not have.

## 1. What exists today (audited 17 Nov 2026)

| Area | What the code actually does | Where |
|---|---|---|
| 3D renderer | three.js 0.170, one canvas, hemisphere + 3 directional lights, contact shadow, quality steps, pause off-screen. Two rig paths: the old procedural "w2s-1" node rig, and "generic" (whole-body hops, spins, squash) | `w2s-site/buddies.js` |
| Kairo (template) | 1 fused mesh, 70 k triangles (web copy), 1 texture (2048 px); face painted on (eyes, brows, beard, an **open grin with teeth**); no skeleton, no face shapes, no animation | `buddy-models/template.glb`, source `references/model.glb` |
| Girl (new template) | same kind of file: 1 fused mesh, 563 k triangles, 23 MB, 4096 px texture; face painted on (grey eyes, winged liner) with **pouted lips modelled in 3D**; long black wavy hair, pink fluffy scarf, black outfit; no skeleton, no face shapes | `references/girl model.glb` |
| Voice out | browser `speechSynthesis`. Accent picks a voice by language (`en-US`, `en-GB`, `en-AU`) and prefers the Buddy's gender by voice name. `onboundary` gives **word start times** on some voices (Chrome desktop local voices, Safari); others (many Google network voices, much of Android) give none, and then words are lit on an **estimated** schedule. Events `w2s:speak`, `w2s:word`, `w2s:speakend` | `showcase.pre-sprint.html` `Voice` |
| Timing data | no phonemes, no visemes, no audio samples: browser speech cannot be routed into Web Audio, so there is nothing to measure loudness from | (platform limit) |
| Voice in | browser `SpeechRecognition` (Chrome, Edge, Safari); interim + final text; errors mapped to `not_granted` / `stopped` / `unavailable`; on `not_granted` the mic is hidden with a toast | `sitebuild.py` `browserSpeech`, `Mic` |
| Conversation | **scripted**: each scene is 5 fixed tutor lines, one per learner turn, whatever the learner says. Corrections come from a rule list of mistakes typical for Spanish speakers. An AI tutor path exists but only runs where the viewer offers an AI capability (`cap.sample`); a static host does not | `MISSIONS`, `scriptedNext`, `aiNext` |
| Help | three levels: starter, word bank, model sentence with Hear it | `renderHint` |
| Stats | sentences, fixes, hints this session; scene-complete card | `renderTally`, `done()` |
| Buddy choice | roster in `buddy_roster.py`; Switch Buddy cycles active Buddies (hidden with one) | `buddy_block.py` |

## 2. Answers to the brief's questions

1. **Improve now (no Blender rig needed):** the girl's web copy (decimate, recolour scarf and
   hair), both Buddies active, a character picker, lighting and framing, idle life (breathing,
   posture, head and body sway kept subtle), state reactions, microphone states, subtitle
   polish, replay/stop, pace, subtitles on/off, difficulty, session summary.
2. **Needs Blender work:** a small skeleton for each Buddy (hips, spine, neck, head, upper
   arms) with **scripted, region-based weights** (not blind auto-rigging), so the head can turn,
   nod and tilt and the shoulders breathe. Recolouring textures. All on copies; originals kept.
3. **Pure JavaScript:** the state machine, idle behaviour, blinking and lip-sync drawn on small
   face "cards" (see 5), switching, UI, conversation improvements.
4. **What the speech system supports:** start and end of each line (real playback events),
   word start times on some voices, nothing finer. Rate can be changed (Slow / Normal).
5. **Limits on facial animation:** the mouths and eyes are paint, not geometry. A mouth cannot
   open by moving vertices: there is no lip edge or mouth interior. The practical, honest
   approach for this chibi style is **2D face cards**: a small surface fitted to the face that
   draws an animated mouth over the painted one while speaking, and eyelids that close over
   the painted eyes to blink. The painted face shows unchanged at rest, so the designs are
   preserved. Eye *direction* cannot change (the irises are painted); gaze is carried by the
   head. Lip shapes follow the words of the line (letters to mouth shapes), timed by the word
   events when the voice provides them and by an estimate when it does not. This is
   **approximate lip-sync**, not phoneme-accurate, and the UI must not claim otherwise.
6. **Order:** A audit and checkpoint → B girl asset + both Buddies on stage → C skeletons +
   idle + blink + mouth cards → D tie to the speech lifecycle (start/word/end, stop) → E picker,
   mic states, subtitle, replay/stop → F difficulty, pace, summary, varied scripted dialogue →
   G measurements and tests.

## 3. Conversation: smallest viable improvement

Today the tutor says line *n* whatever the learner says. Without a server or a paid API the
tutor cannot understand free speech. The smallest real improvement, still fully scripted and
honest about it:
- per step, a few **branches** keyed on what the learner said (keywords: size, food, drink,
  bag count, yes/no), so the reply acknowledges their answer ("A large latte, nice.");
- **variants** for each tutor line so repeats do not sound identical;
- **re-asks** when the answer does not fit the question (a gentle "Sorry, small, medium or
  large?") instead of moving on;
- **difficulty** picks simpler or richer wording of the same line and how much help shows.
The AI tutor path stays as it is for viewers that offer it.

## 4. Status

| Item | Status |
|---|---|
| Audit, checkpoint | done |
| Girl web copy (decimated, scarf beige, hair lighter) | in progress |
| Both Buddies active + picker | planned |
| Skeletons (region weights) | planned |
| Idle / blink / mouth cards / states | planned |
| Mic states, subtitle, replay/stop, pace, subtitles toggle | planned |
| Difficulty, branching script, session summary | planned |
| Measurements and tests | planned |
