# Experiments

**Approved by the owner, 20 Nov 2026.** Written by Claude; change only with the owner's OK. One row per experiment, failed ones
included. **[A]** marks guesses.

## How we run one

1. Write the hypothesis with a number: "If we X, then Y moves from A to B within N days."
2. Decide the stop date and the source of the number first (`ops/weekly_metrics.py`, Stripe, Cloudflare).
3. Change one thing at a time.
4. Write the result, even "no change", and add a line to `decisions.md` if it changes what we do.

## Log

| # | Start | Hypothesis | Measure | Stop | Result | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 20 Nov | Raising the anonymous Modo Habla limit from 3 to 5 lets newcomers finish the café scene, so more create an account [A] | Metric 4, new free accounts per week | 4 Dec | | Running (live 20 Nov) |
| 2 | 20 Nov | Recorded voices with a Female/Male choice make learners finish more Day 1-2 items than device voices did [A] | Metric 5, activated accounts | 4 Dec | | Running; no baseline from before, so compare week 1 with week 2 |
| 3 | first post | The first 5 places sell within 14 days of the soft launch [A: MARKETING_PLAN.md goal] | Metric 6, places paid | 14 days after the first post | | Ready: payments live 20 Nov; waits for the first post |
| 4 | after T9 | Videos about one Spanish-transfer mistake get more profile visits than general tips [A] | Profile visits per 1,000 views, by platform | 10 posts | | Not started |

## Baseline (evening, 20 Nov 2026)

From `ops/weekly_metrics.py`, week to 20 Nov:

- **Visitors:** 1,345 daily visitors and 1,821 page views over 7 days, counted by Cloudflare (bots included; Cloudflare has data for 9 days only).
- **Accounts:** 1 new student account (source: TikTok), probably the owner's test. 0 activated.
- **Bookings:** 1 place held, not paid; 0 paid.
- **Errors:** 0 Worker errors in 172 API requests.
