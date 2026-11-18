# Accounts, payments and the paid Sprint: one-time setup

The site is a Cloudflare Worker (`worker/index.js`) that serves the built pages and answers `/api/*`.
Accounts, usage limits, bookings and progress live in a Cloudflare D1 database. Stripe takes payment
through Payment Links; a webhook tells the Worker who paid. Nothing here needs a server of our own.

Do these steps once, in order. Commands run from `website/week2speak/` with `CLOUDFLARE_API_TOKEN`
and `CLOUDFLARE_ACCOUNT_ID` set as **environment variables** (not network secrets) and
`WRANGLER_SEND_METRICS=false`. Never paste a key into this repository or into a chat.

## 1. The database

```bash
npx wrangler@4 d1 create week2speak
```

Copy the `database_id` it prints into `wrangler.jsonc` (replace the zeros), then create the tables:

```bash
npx wrangler@4 d1 migrations apply week2speak --remote
```

## 2. Settings (plain values, in `wrangler.jsonc` → `vars`)

| Name | What to put | Example |
| --- | --- | --- |
| `PLACES_TOTAL` | Places in this phase | `"5"` |
| `TUTOR_EMAILS` | Email(s) that get the tutor desk, comma-separated. Mei signs up with this email on `/cuenta/`. | `"mei@…"` |
| `TUTOR_WHATSAPP` | Mei's WhatsApp number, digits only with country code. Shown **only** to paid students. | `"447…"` |
| `CAL_LINK` | Mei's Cal.com booking page for the Sprint calls | `"https://cal.com/…/sprint"` |
| `PAY_LINKS` | JSON: one Stripe Payment Link per price tier (step 4) | see below |
| `SHOW_ANCHOR` | `"1"` shows a struck-through reference price. Leave `"0"` unless that price is one Mei genuinely charges (e.g. the price after testing): UK consumer law treats a made-up "was" price as misleading. | `"0"` |

## 3. Secrets (never in the repository)

```bash
npx wrangler@4 secret put STRIPE_WEBHOOK_SECRET   # from step 5
npx wrangler@4 secret put IP_SALT                 # any long random text, e.g. from: openssl rand -hex 32
```

## 4. Stripe Payment Links (one per tier)

In the Stripe Dashboard (account in Mei's name, as the seller), create one product "Sprint de 7 días"
and a Payment Link for each price below. For every link:

- **After payment** → "Don't show confirmation page" → redirect to `https://week2speak.com/gracias/`
  (students who signed up in English are sent on to `/en/thanks/` automatically).
- Collect the customer's name and email (the site prefills the email).
- Leave quantity fixed at 1.

| Tier key | Who sees it | Price |
| --- | --- | --- |
| `gbp` | United Kingdom | £49 |
| `eur` | Euro countries except Spain and Portugal | €49 |
| `eur_es` | Spain, Portugal | €39 |
| `usd` | US, Canada, Australia and everywhere not listed | US$49 |
| `usd_latam` | Latin America except Mexico and Colombia | US$29 |
| `mxn` | Mexico | MX$690 |
| `cop` | Colombia | COP 119.900 |

Then set `PAY_LINKS`, for example:

```json
{"gbp": "https://buy.stripe.com/…", "eur": "https://buy.stripe.com/…", "eur_es": "…", "usd": "…", "usd_latam": "…", "mxn": "…", "cop": "…"}
```

A tier without a link shows the price but books the place as "pending"; Mei can then send a link by
WhatsApp and mark it paid from the tutor desk.

Prices live in `worker/index.js` (`TIERS`, `COUNTRY_TIER`). If you change one, change its Payment Link too.

## 5. Stripe webhook

Stripe Dashboard → Developers → Webhooks → Add endpoint:

- URL: `https://week2speak.com/api/stripe/webhook`
- Events: `checkout.session.completed` and `checkout.session.async_payment_succeeded`

Copy its signing secret (`whsec_…`) into `STRIPE_WEBHOOK_SECRET` (step 3). The Worker checks the
signature on every call and marks the booking paid using the `client_reference_id` the site adds to
the Payment Link.

## 6. Deploy and check

```bash
npm run deploy
```

Then, on the live site:

1. Mei signs up at `/cuenta/` with the `TUTOR_EMAILS` address → the header shows "Mi panel" and `/tutora/` shows the desk.
2. A test student signs up, books on `/unete/`, pays with a Stripe test card (use test-mode links first) → `/gracias/` turns green, the Sprint unlocks, WhatsApp and Cal.com appear.
3. Switch the Payment Links to live mode and update `PAY_LINKS`.

## Day to day

- **Tutor desk** (`/tutora/` for Mei): students by status, last activity, Sprint progress, how they found us,
  mark paid or cancel, send a note (shows on the student's Tutor page), copy a password-reset link.
- **Forgotten password:** the student asks Mei; Mei copies a reset link from the desk and sends it by WhatsApp. Links work once, for 24 hours.
- **Places:** paid bookings plus pending ones less than 48 hours old count against `PLACES_TOTAL`. When full, `/unete/` shows a waiting list; it appears on the desk.
- **Accounts unused for 24 months** are deleted (the privacy notice says so). To find them:

  ```bash
  npx wrangler@4 d1 execute week2speak --remote --command "SELECT email FROM users WHERE last_seen < unixepoch() - 63072000"
  ```

## Local development

```bash
npm run dev        # builds, then serves the site and the API on http://127.0.0.1:8787 with a local database
npm run test:api   # page checks against it (in another terminal)
npm run serve      # static only, no API (then: npm test)
```

For local test values put them in `.dev.vars` (ignored by Git), for example
`TUTOR_EMAILS=mei@example.com` and `STRIPE_WEBHOOK_SECRET=whsec_test`, and apply the migrations locally once
with `npx wrangler@4 d1 migrations apply week2speak --local`.
