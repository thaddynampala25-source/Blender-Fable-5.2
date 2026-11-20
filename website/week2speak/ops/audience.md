# Audience

Draft, updated 20 Nov 2026 (evening), written by Claude. **Not approved.** Owner and Mei sign off.
**[E]** = evidence, **[A]** = assumption to test.

Honest status: almost no customer evidence yet. Live data, evening of 20 Nov: 2 accounts (Mei's tutor account
and one student account, both in the UK, both "found us on TikTok", most likely the owner's own test), 1 booking
not paid, 0 paid. About 1,345 daily visitors in the last 7 days, but that count includes bots. [E: D1 aggregate
read, ops/weekly_metrics.py] So most of this page is still assumption.

## Who we are building for

| Trait | Our guess | Status |
| --- | --- | --- |
| Native language | Spanish | [E: the product's design] |
| Level | A0 to A2: studied at school, cannot hold a conversation | [A] |
| Age | 25 to 55 | [A: MARKETING_PLAN.md targets 30-55 on Facebook] |
| Where | Latin America, Spain, Spanish speakers in the UK and US | [A] |
| Main block | Fear of speaking, not lack of vocabulary | [A: the core positioning; test in calls] |
| Goal | Travel, work, family abroad | [A: the "why are you learning" options in the scenes] |
| Device | Phone first | [A: check Cloudflare device data] |
| Price sensitivity | Regional prices exist because £49 is a lot in Latin America | [E: price table] [A: whether they are low enough] |

## What we need to learn first

1. Which country do the first 20 real sign-ups come from? Source: weekly metrics, `users.country`.
2. What do they answer in "how did you find us"? Source: metric 4 of the weekly numbers.
3. In the first Sprint calls, Mei asks "What stops you speaking?" and "What would make this week worth it?".
   Answers go into `experiments.md`, word for word, with consent.
4. Which free room people use most before buying: needs the owner's decision on anonymous counts.

## Who it is not for (for now)

- Advanced learners wanting exam preparation (IELTS, Cambridge). [A]
- Children: the Sprint, calls and WhatsApp are designed for adults. [A: the terms state no age; owner to decide]

## Sources to add

No competitor or audience research yet (Research role, operating-system doc §4).
