# Experiments

Draft, 20 Nov 2026, written by Claude. **Not approved.** One row per experiment, failed ones included. Nothing has run yet,
so every result cell is empty. **[A]** marks guesses.

## How we run one

1. Write the hypothesis with a number: "If we X, then Y moves from A to B within N days."
2. Decide the stop date and the source of the number before starting (weekly_metrics.py, Stripe, Cloudflare).
3. Change one thing at a time.
4. Write the result, even "no change", and add a line to decisions.md if it changes what we do.

## Log

| # | Start | Hypothesis | Measure | Stop | Result | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | after deploy | Raising the anonymous Modo Habla limit from 3 to 5 lets newcomers finish the café scene, so more create an account [A] | New free accounts per week; café scenes finished (needs on-device counts or owner decision) | 14 days | | Ready, waits for deploy |
| 2 | after deploy | Recorded voices make learners replay and finish more Day 1-2 items than the device voice [A] | Days 1-2 game rounds completed per active learner | 14 days | | Ready, waits for deploy; no baseline yet |
| 3 | after T1 | The first 5 places sell within 14 days of the soft launch [A: MARKETING_PLAN.md goal] | Paid enrolments | 14 days after the first post | | Blocked by T1 (purchase path) |
| 4 | after T9 | Videos about one Spanish-transfer mistake get more profile visits than general tips [A] | Profile visits per 1,000 views, by platform | 10 posts | | Not started |

## Baseline (20 Nov 2026)

1 account, 0 enrolments, 0 waitlist entries, 0 usage rows (live D1, aggregate read). Visits: not readable until the
Cloudflare token has Zone Analytics Read (T3).
