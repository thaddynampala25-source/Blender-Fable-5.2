# Tasks that need the owner (or Mei)

Kept by Claude; every session reads this and keeps it current. Newest state: 21 Nov 2026.
When a task is done, move it to "Done" with the date. Never mark a task done that the owner has not confirmed.

## 1. Record the rest of the course (hidden on the site until recorded)

These parts would only play with the computer's own voice, so they are **hidden** from learners until they are
recorded in all six voices (US Savvy / Young Jamal, UK Charlotte / Marcus, AU Sophia / Ben). They come back on the
site by themselves as soon as their recordings are in `w2s-site/audio/` (no code change needed).

| Hidden now | Where | Sprint day |
| --- | --- | --- |
| Chat about yesterday | Speech Mode scene | Day 4 |
| Coffee chat: opinions | Speech Mode scene | Day 5 |
| Job interview | Speech Mode scene | (not in the Sprint) |
| Yesterday, My opinion, Keep talking, My talk | Shadowing clips | Days 4-7 |
| Days 4-7 | Games (all five games) | Days 4-7 |
| Lessons 4-7 | Course | Days 4-7 |

- **Needs the owner:** ElevenLabs credits and an OK to spend them. Cost: about 11,600 credits per Sprint day for all
  six voices (Sophia costs 2.25x), so Days 4-7 plus Job interview is about 48,000: more than one month of the
  Starter plan (40,000). Credits reset on **20 Dec 2026**. Options: two months on Starter, or a bigger plan.
- **Before a paid student reaches Day 4**, these must be recorded: the paid Sprint still opens them from the daily
  plan, where they would use the computer's voice.
- How to record: `ops/HANDOFF.md`, "Update, 21 Nov 2026: final voices" (plan, generate, words, split, check, build).
- **Reminder (owner, 21 Nov):** the owner wants to record Days 4-7 with **VoiceStudio** (https://github.com/debpalash/voicestudio,
  already downloaded) instead of ElevenLabs, but is not yet sure how to import the six voices into it. Remind the owner,
  and help with the import when asked. The clips still go through `audio_words.py` / `audio_build.py split` and `build`.

## 2. Mei

- **Reminder (owner, 21 Nov): tutor page bio.** 3-4 lines about Mei (background, experience), no photo. Needs the facts
  from the owner or Mei; Claude writes it in both languages once they arrive.

- Listen to the single Sound Lab words in each voice, above all Sophia and Ben (heat, hand, old, hat, estrange, espy,
  esquire, air): a machine cannot confirm single words in a strong accent.
- Answer the three open questions in `ops/lesson_review_day1_day2.md`; pounds or dollars matters most (the
  American voices say "four pounds" in the café).
- Read `teaching.md` and `audience.md` (approved by the owner; Mei's comments welcome).

## 3. Owner decisions and inputs

- **Photo of Mei**: none on the site until the owner sends one (owner's instruction, 20 Nov).
- **First real sale**: when it comes in, ask Claude to "check the first sale" (confirms the live Stripe webhook
  secret; if it failed, the payment still arrived and the booking can be marked paid by hand).
- **Read-only Stripe key** (optional): puts revenue and failed payments into `ops/weekly_metrics.py`. Goes in the
  environment settings, never in chat.
- **Social accounts** (TikTok, Instagram): wanted, but **later**: the owner is still optimising the site and service
  (21 Nov). Mei sets them up; then Claude drafts three posts (T9). Remind the owner when the site work settles.
- **Notion "Week2Speak HQ"** (T5): Claude creates it only after the owner OKs pages in the personal workspace.
- **Monday review** (45 minutes) once posts are out; **five Week2Speak lines in the morning brief** if wanted.

## 4. Usability proposals still open (owner decides; Claude can build any of them)

- **Speech Mode on desktop** stacks the correction, hint and Buddy line over the Buddy's face, and shows all settings
  at once. Proposal: one message at a time; settings folded under "Settings".
- **Open questions from the bug test** (not changed): Speech Mode scenes accept any reply of two words or more; Speech
  Mode forgets "read lines aloud" and the last scene after a reload; the Join page still says "Book my place" while a
  booking waits for payment.

## Done

- 21 Nov 2026: six voices chosen and recorded for Days 1-3; drafts in `ops/` approved; Stripe live; Mei's tutor
  account, WhatsApp and Cal.com link set; Cloudflare analytics permission added.
- 21 Nov 2026 (owner approved, built and deployed): headline "Tu primera conversación en inglés, en 7 días"; two booking
  labels only ("Ver el Sprint" / "Reservar mi plaza"); home "Empieza el Día 1" opens free lesson 1; Join checkbox in plain
  words; home pricing shows the Sprint price and a "Crear cuenta gratis" button; one name per scene and button; Speech
  Mode limit card and "(opcional)" on "¿Cómo nos encontraste?"; thank-you page says "Aún no tienes plaza" without a booking.
- 21 Nov 2026: anonymous practice counts switched on after the owner approved the privacy-notice line (privacy notice
  updated in both languages; `ops/weekly_metrics.py` metric 3 reads them).
