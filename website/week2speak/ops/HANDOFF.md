# Handoff: Week2Speak, 20 Nov 2026

For the next person or Claude session taking over Week2Speak (week2speak.com), an English-speaking practice site
for Spanish-speaking adults. Read this first, then the documents it points to. Nothing in the plans below has been
approved by the owner yet unless it says "deployed".

## Where everything is

| What | Where |
| --- | --- |
| Operating-system audit, roles, pipeline, metrics, 7-day plan, first ten tasks | Claude Docs: "Week2Speak Operating System: Audit and 7-Day Plan", https://claude.ai/artifact/Mh2GYDiGHWZyeDDERW66is (read/edit with the Claude Docs connector, not web fetch) |
| Decision log | `website/week2speak/ops/decisions.md` |
| Site rules for Claude | `website/week2speak/CLAUDE.md` (read first), then `PROJECT_HANDOFF.md` |
| Practice-loop upgrade (what changed, how to test, what is left) | `website/week2speak/UX_UPGRADE_HANDOFF.md` |
| Payments, accounts, D1 setup | `website/week2speak/ACCOUNTS_SETUP.md`, `NEXT_STEPS.md` |
| Marketing plan (positioning, 20 video ideas, funnel targets marked unverified) | `website/week2speak/MARKETING_PLAN.md` |
| Code branch | `claude/keen-pascal-b935nd` in `thaddynampala25-source/Blender-Fable-5.2` (the repo also holds unrelated game and Blender projects; Week2Speak is `website/week2speak/`) |

## State right now

- **Live site** = the Cloudflare Worker `week2speak` (custom domains week2speak.com and www). Last deploy:
  version `c2a0593a-49da-4e1b-a015-fe1178fa8a32`. Deploy from `website/week2speak/`: `npm run build`, then
  `npx wrangler@4 deploy` (needs `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` in the environment,
  `WRANGLER_SEND_METRICS=false`). Do not create a Cloudflare Pages project: the site is a Worker.
- **Deployed and tested this session**: the header shows every section at every width (Menu button on phones);
  the Spanish name for Shadowing is "Imita"; the practice-loop upgrade (home Day 1 sample and Continue, score-once,
  stale mic captures dropped, separate mic messages, round recap and review, Imita next-step buttons,
  recorded-clip playback layer, on-device event counts). Tests: `w2s-site/ux_test.cjs` 37/37, `w2s-site/test.cjs`
  pass, `buddy_test.cjs` all but `noErrors` (only the static server's `/api/me` 404s).
- **Baseline data** (live D1, aggregate read-only, 20 Nov): 1 account, 0 enrolments, 0 waitlist, 0 usage rows.
- **Not working yet**: Stripe Payment Links are in test mode; `STRIPE_WEBHOOK_SECRET` is not set; `TUTOR_EMAILS`,
  `TUTOR_WHATSAPP`, `CAL_LINK` are empty in `wrangler.jsonc` vars. A buyer could not get the Sprint or book a call.
- **Pushed**: all work is on GitHub (`lfs.github.com` is now reachable; T2 is done). If a later push fails on
  `lfs.github.com` again, the owner adds it under the environment's Allowed domains; never force a push without the
  LFS objects.
- **Cloudflare token** lacks Zone Analytics Read, so daily visitor counts cannot be read yet.

## What to do next (the doc's first ten tasks, in order)

1. **T1 purchase path (highest value, do first).** Ask the owner for: the Stripe webhook signing secret (they paste
   it into Cloudflare themselves, never in chat or the repo), and Mei's login email, WhatsApp number and Cal.com
   link (not secret; go into `wrangler.jsonc` vars). Then test with a Stripe test card on `/unete/`: `/gracias/`
   confirms, the tutor desk shows the enrolment as paid, the booking link opens. Deploy only with the owner's yes.
2. T2 done: pushing works (20 Nov).
3. T3 owner adds Zone Analytics Read to the token; verify with a 7-day visits query.
4. T4 draft `ops/brand.md`, `audience.md`, `product.md`, `teaching.md`, `experiments.md` (each under 400 words,
   every claim marked evidence or assumption; owner and Mei sign off).
5. T5 Week2Speak HQ in Notion (Tasks, Content, Decisions, Experiments databases), only after the owner approves
   creating pages in their workspace (it is otherwise personal).
6. T6 weekly metrics script (read-only D1 + Stripe + Cloudflare) for the eight metrics in section 8 of the doc.
7. T7 Educational QA checklist for the Day 1 path; Mei listens to device voices on her phone.
8. T8 owner decides the free limit: anonymous users get 3 Modo Habla replies; the café scene needs 5.
9. T9 first three content pieces to Approved (from `MARKETING_PLAN.md`); agents never publish.
10. T10 switch Stripe to live links after T1 passes; owner makes one live purchase and refund.

Open owner decisions: free limit (T8), recorded-voice budget (ElevenLabs is connected but costs credits: explain
output and cost before any generation), anonymous first-party practice counts (needs a privacy-notice change).

## Rules that matter

- Never deploy, publish, contact people, buy anything or spend credits without the owner's explicit yes.
  Keep drafted, approved and published clearly separate.
- Never fabricate research, customer data or results. Never write keys into the repo.
- The site makes no requests to other domains (privacy promise). No third-party analytics.
- Edit sources, never `w2s-site/dist/` or `w2s-show/showcase.html`. Practice-loop patches live in
  `w2s-site/apply_ux.py`. Every new English UI string needs a Spanish entry in `i18n_cat_js.py` or
  `i18n_cat_pages.py`. In the built site `$()` never returns null: use `querySelector` for existence checks.
- Free limits are access rules: change only with the owner's decision.

## Suggested skills

- `productivity:task-management` and `engineering:standup`: Chief of Staff routines.
- `stripe:stripe-best-practices`: T1 webhook and live-mode switch.
- `marketing:content-creation`, `anthropic-skills:copywriting`, `marketing:brand-review`: T4 and T9.
- `anthropic-skills:deep-research`, `marketing:competitive-brief`: audience and competitor evidence for T4.
- `anthropic-skills:saas-animation` (storyboard first, approval before render): animated Buddy content.
- `dataviz`: when the weekly numbers become a chart.
- `anthropic-skills:find-skills`: Tool Scout comparisons before installing anything.

## Update, 20 Nov 2026 (later the same day)

Owner decisions: anonymous Modo Habla limit is **5** (T8 done); recorded voices **approved** (ElevenLabs connected);
T7 replaced by a real review of Days 1 and 2; T4 drafts wanted.

Done on the branch, **built and tested, not deployed** (deploy needs the owner's yes):
- `account.js` `ANON.speak` 5. Day 1-2 content fixes (see `ops/lesson_review_day1_day2.md`).
- Recorded clips for every fixed Day 1-2 line, `w2s-site/audio/`, shipped as `/media/voice/` + `window.W2S_AUDIO`.
  **Superseded the same day**: Matilda and Chris were the agent's pick, not the owner's. See the voices update below.
- `ops/weekly_metrics.py` (T6). Visits fail until the token has Zone Analytics Read (T3).
- T4 drafts: `ops/brand.md`, `audience.md`, `product.md`, `teaching.md`, `experiments.md`.

Gotcha: a fresh clone has Git LFS pointers instead of the Buddy models. Run `git lfs install --local && git lfs pull`
**before `npm run build`**, or the built site ships 130-byte .glb files and the Buddies never load.

## Update, 20 Nov 2026: the owner's voices, Female/Male choice, Mei's details (deployed)

- Voices (owner's picks, ElevenLabs library, ids in `w2s-site/audio_build.py` `VOICES`):
  US woman Brittney (Social Media Voice), US man Joe (Confident Idiot), US May Genevieve, US Kairo Young Jamal;
  British woman and May Charlotte (Warm, Clear British RP), British man and Kairo Marcus (Black British London);
  Australian woman and May Jane (Warm & Professional), Australian man and Kairo Paul (metropolitan Australian;
  there is also "Paul - Australian Professional Presenter" if the owner meant that one).
- Clip keys are `accent|voice|text`; voice is `f`/`m` (the learner's Female/Male choice, shown in Games, Imita and
  the course) or the Buddy id in Speech Mode (`may`, `kairo`), falling back to the Buddy's gender. 87 lines x 8 voices.
- Clips are cut by word timings from a local speech-to-text model (`audio_words.py`, faster-whisper, nothing
  uploaded) and each clip was transcribed back and compared with its line. Nobody has listened by ear yet.
- Credits: 25,451 for the eight takes; about 2,200 of 40,000 left this month. Days 3-7 for eight voices would cost
  about 60,000 credits: a bigger plan or several months.
- `wrangler.jsonc`: TUTOR_EMAILS wamulow@gmail.com, TUTOR_WHATSAPP, CAL_LINK set. Mei becomes tutor at her next login.
