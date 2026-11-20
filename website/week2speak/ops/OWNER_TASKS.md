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

## 2. Mei

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
- **Anonymous practice counts** (metric 3, "visitors who practise"): needs a privacy-notice change; owner decides.
- **Social accounts** (TikTok, Instagram) for the first posts; Mei sets them up. Then Claude drafts three posts (T9).
- **Notion "Week2Speak HQ"** (T5): Claude creates it only after the owner OKs pages in the personal workspace.
- **Monday review** (45 minutes) once posts are out; **five Week2Speak lines in the morning brief** if wanted.

## Done

- 21 Nov 2026: six voices chosen and recorded for Days 1-3; drafts in `ops/` approved; Stripe live; Mei's tutor
  account, WhatsApp and Cal.com link set; Cloudflare analytics permission added.
