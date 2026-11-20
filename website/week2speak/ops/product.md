# Product

Draft, 20 Nov 2026, written by Claude. **Not approved.** **[E]** = evidence (file or page), **[A]** = assumption.

## Free

| Tool | What it does | Free limit, no account | Free limit, free account |
| --- | --- | --- | --- |
| Modo Habla (Speech Mode) | Talk to a Buddy in a scene (café, airport, meet someone) | 5 replies a day | 10 a day |
| Juegos | Word Order, Fill the Gap, Flash Translate, Sound Lab, Quick Answers | 1 round | 3 |
| Imita (Shadowing) | Listen, speak along, then solo | 2 runs | 5 |
| Curso | 7 lessons of 12 minutes or less | 1 lesson | 2 |

[E: account.js `ANON`, worker/index.js `LIMITS`; anonymous Modo Habla raised from 3 to 5 on 20 Nov, not deployed yet]

## Paid: the 7-Day Sprint

- £49 in the UK; regional prices elsewhere, shown before paying. [E: worker price table, Sprint page]
- 5 places in the testing phase. [E: `PLACES_TOTAL`]
- Includes: daily plan (Day 0 to Day 7), two 25-minute video calls with Mei, WhatsApp with Mei, full access for the
  week, Day 1 and Day 7 recordings. [E: sprint_paid.py, Join page]
- Refund: full before the first call; after it, within 14 days, the part not yet received. [E: terms]

## Not working yet (blocks every sale)

- Stripe links are in test mode; webhook secret, Mei's email, WhatsApp and Cal.com link are not set. [E: wrangler.jsonc]

## Quality bar

- Every fixed Day 1-2 line has a recorded voice; Days 3-7 still use the device voice. [E: audio/manifest.json]
- Lesson review for Days 1-2 done 20 Nov (ops/lesson_review_day1_day2.md); Days 3-7 not reviewed. [E]

## Assumptions to test

- Two calls are enough for a beginner to feel progress. [A]
- People finish the free café scene before they think about paying. [A]
- One week is the right length; some may want a second week. [A]
