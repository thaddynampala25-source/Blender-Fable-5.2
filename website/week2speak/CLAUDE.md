# Week2Speak: notes for Claude Code

Read PROJECT_HANDOFF.md first. The short version:

- Edit sources in `w2s-site/` and `w2s-show/showcase.pre-sprint.html`. Never edit `w2s-site/dist/` or `w2s-show/showcase.html` by hand: both are generated.
- Build: `npm run build`. Serve: `npm run serve` (static, port 8765; then `npm test`, `npm run test:buddies`) or `npm run dev` (Worker + local D1 on 8787; then `npm run test:api`).
- The site must make no requests to other domains (the privacy notice promises it). Self-host every asset.
- Keep the internal Buddy ids `mila` (Ruby) and `rio` (Max) and the `w2s:*` window events.
- Keep the labels the Sprint decks and learner guide name on the English site (/en/): Next, Go, Help me, Record, Send it, Speech Mode, and the scene names. The Spanish site translates them.
- Stop and ask before deleting files, adding dependencies other than three.js loaders, changing the privacy notice, or removing a page or feature.

## Spanish first, English at /en/ (since November 2026)

- Spanish is the site's language at `/` with Spanish paths; English is the translation at `/en/` (`w2s-site/i18n.py`, paths in `SLUG`).
- The original pages are written in English source text. `i18n_cat_pages.py` (HTML, SEO, JSON-LD) and `i18n_cat_js.py` (app strings) map each interface string to Spanish and, where the Spanish was rewritten, to new English. Matching is exact and global: never add a short word that is also learning content, a data key or the logo (`Speak`). `I18N_REPORT=1 python3 sitebuild.py` lists entries that match nothing.
- New pages (`features.py`: Sprint, Tutor, Join, account, thank-you, terms; `privacy_content.py`) are written in both languages directly.
- English the learner practises stays English on both sides.

## Accounts and the paid Sprint

- `worker/index.js` + D1 (`migrations/`): accounts, roles (tutor by `TUTOR_EMAILS`), daily free limits, bookings, Stripe webhook, progress sync. `/paid/*` is served only to paid students and the tutor.
- `w2s-site/account.js` is the front end for all of it (limits, nudges, Join, thank-you, Tutor desk, paid Sprint). Setup steps: `ACCOUNTS_SETUP.md`. Marketing: `MARKETING_PLAN.md`.
- The privacy notice now describes accounts, the one session cookie, Stripe, Cal.com, Google Meet and WhatsApp. Change it whenever data handling changes.
