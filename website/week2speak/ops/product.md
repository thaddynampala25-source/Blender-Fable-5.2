# Product

**Approved by the owner, 20 Nov 2026.** Written by Claude; change only with the owner's OK.
**[E]** = evidence (file, live system), **[A]** = assumption to test.

## Free practice (live)

| Room | What it does | No account, per day | Free account, per day |
| --- | --- | --- | --- |
| Modo Habla (Speech Mode) | Scripted scenes with a 3D Buddy (May or Kairo): meet someone, café, airport and 4 more | 5 replies | 10 replies |
| Juegos | Word Order, Fill the Gap, Flash Translate, Sound Lab, Quick Answers | 1 round | 3 rounds |
| Imita (Shadowing) | Listen, speak along, then solo; 3 speeds | 2 runs | 5 runs |
| Curso | 7 short lessons | 1 lesson | 2 lessons |

[E: account.js `ANON`, worker/index.js `LIMITS`; anonymous Modo Habla raised to 5 on 20 Nov, live]

## Voices (live)

- Days 1-3 are recorded in 6 voices the owner chose: female and male for American, British and Australian.
  Learners pick Female or Male; in Speech Mode May speaks with the female voice, Kairo with the male. [E: `VOICES`]
- Other lines use a device voice of the same gender; an accent the device lacks is hidden there. [E: apply_ux.py]

## Paid: the 7-Day Sprint (live, real payments since 20 Nov)

- Price by country: £49 UK; €49 euro area; €39 Spain and Portugal; US$49 US and default; US$29 Latin America;
  MX$690 Mexico; COP 119.900 Colombia. [E: worker `TIERS`, live Stripe Payment Links]
- 5 places in the testing phase. [E: `PLACES_TOTAL`]
- Includes a daily plan, two 25-minute calls and WhatsApp with Mei, unlimited practice, Day 1 and Day 7
  recordings. [E: sprint_paid.py]
- After paying, the student sees Mei's WhatsApp and her Cal.com booking page (30 minutes). [E: wrangler.jsonc]
- Refund: full before the first call; after it, within 14 days, the part not yet received. [E: terms]

## Known gaps

- The live Stripe webhook secret is confirmed only by the first real sale; if it fails, the payment still arrives
  and Mei marks the booking paid by hand. [E: worker, Stripe connector check 20 Nov]
- Days 4-7: not recorded; Days 3-7 not reviewed. [E]
- No count of anonymous visitors who practise (owner decision). [E: audit §8]

## Assumptions to test

- Two calls are enough for a beginner to feel progress. [A]
- People finish the free café scene before they think about paying. [A]
