# Week2Speak product upgrade: handoff

Working notes for the "practice loop" upgrade (owner's brief: make the core loop excellent on a phone, then make it
feel alive). A new session should read this, `CLAUDE.md` and `PROJECT_HANDOFF.md`, then carry on from "Next".

Branch: `claude/keen-pascal-b935nd`. Live site: the `week2speak` Cloudflare Worker (deploy with
`npx wrangler@4 deploy` from `website/week2speak/` after `npm run build`; needs `CLOUDFLARE_API_TOKEN`,
`CLOUDFLARE_ACCOUNT_ID`, `WRANGLER_SEND_METRICS=false`).

**Push is blocked** in the last session: the environment's network policy denies `lfs.github.com`, so commits that
touch LFS files (built PNGs in `dist/`) cannot be pushed. The owner must add `lfs.github.com` to Allowed domains.
Check `git status -sb` for unpushed commits first.

## Where the code is

| File | What |
|---|---|
| `w2s-site/apply_ux.py` | **New third patch layer**, run by `apply_sprint.py` after `apply_more.py`. All practice-loop logic changes live here as exact-match `rep()` patches on `w2s-show/showcase.html`. |
| `w2s-site/features.css` | Last stylesheet. The block "Practice loop (apply_ux.py)" at the end holds the new tokens and styles. |
| `w2s-site/sitebuild.py` | `browserSpeech()`: error reasons now `silence`, `not_granted`, `no_mic`, `network`, `stopped`, `unavailable`; a cancelled or replaced recogniser stays silent. |
| `w2s-site/buddy_block.py` | Modo Habla `MICMSG` covers the new reasons. |
| `w2s-site/i18n_cat_js.py`, `i18n_cat_pages.py` | Spanish for every new string (section "practice loop"). Matching is exact; run `I18N_REPORT=1 python3 sitebuild.py` to list unused entries (12 old ones are now unused and can be deleted). |
| `w2s-site/ux_test.cjs` | **New targeted test** (37 checks): home sample and Continue, score-once, stale captures, mic outcomes, recap and review, Modo Habla scene switch, recorded-clip playback, reduced motion. Fakes speech recognition. Run with the site on 8765: `node ux_test.cjs`. |

Note for patches: in the built site `$()` never returns null (see `nulljs.txt`), so use `querySelector` for any
"if it exists" check or `a || b` fallback.

## Baseline (before, iPhone 13 size, Spanish site)

- Home: both hero buttons led away from practice (paid Sprint page, film). First playable control at y=3747 (5.6 screens).
- Juegos: first word tile at y=835 (below the fold); usage counter covered the page heading.
- Café with Kairo: 1 tap to start, greeting plays, typed order answered with "Sure. Small, medium or large?" (works).
- Imita: 18 buttons before the clip; Escuchar below the text.
- Code issues found: a late spoken result after typing scored twice; a capture from a previous item/scene could be
  graded against the next one; silence, blocked mic and recognition failure all said "I did not catch that";
  Imita Solo said words "came through clearly" (implied pronunciation grading); the home Word Order advanced on a
  1.9 s timer with no route onward; rounds ended with a count only.
- Free limits matter for journeys: anonymous visitors get 3 Modo Habla replies, 1 game round, 2 Imita runs, 1 lesson a
  day. The café scene needs 5 replies, so a newcomer sent to it hits the sign-up sheet mid-order. Not changed
  (access rule); flagged for the owner.

## Done so far (built and tested locally; see ux_test.cjs)

1. Home: hero action "Preséntate en inglés" jumps to the sample, which now sits right under the hero; the sample uses
   four Day 1 sentences, waits for Siguiente, shows the phrase and Escúchalo, and ends with "Juega la ronda del Día 1"
   and "Pide un café con un Buddy" (real paths). "Continuar · Día N" appears for learners with progress on this device.
2. Games: score once (guards in solve/checkFlash/checkQuick/miss); each item has a token, captures from earlier
   items are dropped; `Mic.cancel()` on game/day/item/scene/page change; distinct messages for silence, blocked,
   no mic, recognition failure (never counted as a miss; typing focused when the mic is blocked).
3. Feedback block: icon + title, the English phrase in display type (`.fb-say`, lang="en"), XP as a small chip, space
   reserved (`--fb-min`) so controls do not jump; Next gets focus.
4. Word Order tiles travel between bank and tray (FLIP, 190 ms, skipped with reduced motion); tray keeps its height.
5. Round recap lists every phrase (right/missed), offers "Repite las que fallaste (n)", next game, play again. The round
   bonus and the free-round count happen once.
6. Imita: Solo result wording is honest about recognition; every mode ends with a next-step button
   (Escucha → Ahora imita → Ahora prueba Solo → Siguiente clip).
7. Voice: recorded-clip layer in `Voice.speak` (manifest `window.W2S_AUDIO`, key `accent|gender|text` or
   `accent|text`, word timings drive highlighting and `w2s:word`, pitch-preserving rate, falls back to the device voice
   on error or blocked autoplay). `Voice.preload(text)`, `Voice.hasClip`, `Voice.kind`. No manifest ships yet.
8. `track(name, props)`: events `practice_start`, `audio_start`, `audio_fail`, `mic_start`, `mic_fail`, `mic_empty`,
   `attempt` (input typed/mic/tap), `feedback` (right/retry/shown), `next`, `round_complete`; daily counts in
   localStorage `w2s.metrics` (14 days), first-time ms in `window.W2S_FIRST`, every event as `w2s:metric`.
   Nothing is sent over the network (privacy notice unchanged).
9. Usage counter moved to the bottom-left corner; Juegos on phones: one-row game picker, 7-column day row.

10. Usage counter now sits under each page heading, in the flow (account.js `usageBadge`); Spanish names it Imita.

**Status at handoff:** deployed (Worker version `c2a0593a-49da-4e1b-a015-fe1178fa8a32`), committed on
`claude/keen-pascal-b935nd`, push blocked by `lfs.github.com` (see top). Checks: `ux_test.cjs` 37/37, `test.cjs`
pass (home sample sentence updated), `buddy_test.cjs` all pass except `noErrors`, which only fails on the static
server's `/api/me` 404s (no Worker on port 8765; same before this work). Header check all ok at 320/390/768/1440.

## Next (in order)

1. Push once `lfs.github.com` is allowed.
2. Not yet done from the brief: Sound Lab loading/playing/failed states on the Play button; Quick Answers preload of
   the next question; Completa la frase showing the chosen wrong word inside the sentence; Flash accepting more
   reviewed variants; Modo Habla current-prompt prominence; Imita stable reading area and timed Solo cues;
   Curso/Sprint day recap and missed-day resume; real-device checks (iOS Safari keyboard, Android mic).
3. Audio pipeline: `npm run audio:list` script that collects every fixed line (games, quick answers, clips, scene
   lines, hints, Buddy greetings) with stable IDs and character counts → cost estimate for the owner. Generation
   command (Polly Neural base; compare ElevenLabs where approved) writing `w2s-site/audio/` + manifest, only with
   credentials and the owner's approval. ElevenLabs is connected in this workspace as an MCP server but generating
   spends credits: ask first. Audition set: "Sure. Small, medium or large?", "Could I have a window seat, please?",
   the Preséntate paragraph, ship/sheep, state/estate.
4. Modo Habla polish (current prompt prominence, compact correction), Imita reading-area stability, Curso/Sprint
   day recap and missed-day resume.
5. Server endpoint for dynamic synthesis (Mi guion) with caps and quotas: needs a provider key.

## Owner decisions needed

- Free limit vs café scene length (3 replies vs 5 needed).
- Voice provider and budget for the fixed library; approval before any paid generation.
- Whether to send anonymous aggregate events to the site's own Worker (would need a privacy-notice change).
