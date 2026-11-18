# Week2Speak: where we are and what's next (handoff, 18 Nov 2026)

All the work is on Git branch `claude/eloquent-rubin-uixyv0` (not on main yet). A new session should check out
that branch first.

## Done (built, tested, pushed; not live yet)

- Spanish-first site at `/`, English at `/en/`, language switch, Spanish SEO.
- Accounts (email + password), tutor role for Mei, free daily limits (stricter without an account), sign-up nudges.
- Join page with regional prices and 5 places, thank-you page, paid 7-Day Sprint, "Tu tutora" page, tutor desk.
- Privacy notice and terms (14-day cancellation, start-now consent box), `MARKETING_PLAN.md`.
- Full technical reference: `ACCOUNTS_SETUP.md`.

## Still to do, in order

1. **Stripe, test mode: DONE (18 Nov).** In the "Week2Speak sandbox" Stripe account: product "Sprint de 7 días"
   (`prod_VeQv3MkoPWy0mA`), one price per tier (lookup keys `sprint_gbp`, `sprint_eur`, `sprint_eur_es`, `sprint_usd`,
   `sprint_usd_latam`, `sprint_mxn`, `sprint_cop`) and a Payment Link each, redirecting to `/gracias/`, with
   Managed Payments off. The test links are in `wrangler.jsonc` → `PAY_LINKS`. **Before launch:** recreate them in
   live mode (same settings) and swap the links in.
2. **Stripe webhook.** Endpoint `https://week2speak.com/api/stripe/webhook`, events `checkout.session.completed`
   and `checkout.session.async_payment_succeeded`. Its signing secret (`whsec_...`) is pasted **by the owner**
   into Cloudflare → Workers & Pages → week2speak → Settings → Variables and Secrets → Secret
   `STRIPE_WEBHOOK_SECRET`. Never through the chat, never in the repo.
3. **Second secret**, same place, by the owner: `IP_SALT` = any 40 random letters/numbers.
4. **Mei's details** (the owner gives them in chat; not secret) → `wrangler.jsonc` vars:
   `TUTOR_EMAILS` (her login email), `TUTOR_WHATSAPP` (digits with country code), `CAL_LINK`
   (Cal.com event "Llamada del Sprint", 25 min, Google Meet).
5. **Database: DONE** (created by another session, tables applied, checked 18 Nov). Remaining: **deploy.** Needs an environment with `CLOUDFLARE_API_TOKEN` (template "Edit Cloudflare Workers"
   plus Account → D1 → Edit), `CLOUDFLARE_ACCOUNT_ID=6e99521ecb4f385dc5fcdcc5ec403742`,
   `WRANGLER_SEND_METRICS=false`, as environment variables (not network secrets). Then:
   `npx wrangler@4 d1 migrations apply week2speak --remote` (skips if already applied) → `npm run deploy`.
6. **Check together.** Mei signs up on `/cuenta/` with her email → sees "Mi panel". Test purchase with a Stripe
   test card on `/unete/` → `/gracias/` turns green, Sprint unlocks. Then switch Stripe to live links.

## Owner decisions on record

- One paid offer: 7-Day Sprint, £49 (regional prices), 2 calls with Mei, WhatsApp 1-to-1, 5 places in testing.
- Seller: Mei (UK sole trader). No refund for not managing the 2-minute talk (terms handle the 14-day rule).
- Struck-through reference price stays off (`SHOW_ANCHOR "0"`) unless it is a real future price.
- Keep telemetry off; never write keys into the repo; never ask for keys in chat.
