# Week2Speak operating system

Status: **proposed, awaiting the owner's review** (20 Nov 2026). Nothing here has been approved yet.

The audit, architecture, roles, integrations, content pipeline, routines, metrics, seven-day plan and the first ten
tasks are in the Claude Docs document "Week2Speak Operating System: Audit and 7-Day Plan":
https://claude.ai/artifact/Mh2GYDiGHWZyeDDERW66is (read and edit it through the Claude Docs connector). A PDF copy
(20 Nov 2026) is in this folder: `operating-system-audit-and-7-day-plan.pdf`; sessions that cannot open the doc read that.

Baseline facts at audit time (live D1, read-only aggregate query, 20 Nov 2026): 1 account, 0 enrolments,
0 waitlist entries, 0 usage rows. Stripe links are in test mode; `STRIPE_WEBHOOK_SECRET`, `TUTOR_EMAILS`,
`TUTOR_WHATSAPP` and `CAL_LINK` are not set. The Cloudflare token lacks Zone Analytics Read.

Recommended first task: **T1, make one test purchase work end to end** (owner sets the webhook secret and Mei's
three contact details; an agent then tests with a Stripe test card).

Drafts for task T4 (20 Nov, not approved yet): `brand.md`, `audience.md`, `product.md`, `teaching.md`,
`experiments.md`. `decisions.md` is below.

Also here: `weekly_metrics.py` (T6, read-only weekly numbers; `python3 ops/weekly_metrics.py --md`) and
`lesson_review_day1_day2.md` (the Day 1-2 quality review that replaced the T7 checklist).
