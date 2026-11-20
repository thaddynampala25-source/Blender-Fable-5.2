# Week2Speak: student, tutor and thank-you features (brainstorm)

**Opportunity.** Absolute-beginner Spanish speakers pay £49 (regional prices) for the 7-Day Sprint: full
access to Speech Mode, games, course and the Sprint, plus two 1-to-1 calls and WhatsApp with their tutor,
Mei. The risk with any self-paced course is that a beginner opens it alone, freezes, and quits on day 2.
**Desired outcome:** every paid student feels someone is with them all week, finishes Day 7, and says
their first 2 minutes of English out loud. Free visitors hit a usage limit within about a minute and make
an account; free accounts hit a stricter daily limit and see what the Sprint adds.

## Ideas by perspective

### Product manager (value, fit, advantage)
1. **One clear offer, scarce:** "5 plazas" for the testing phase, a live count from the database, and a
   waitlist when it is full (no dead end).
2. **Regional prices with psychology:** price by country (from Cloudflare's own country header, no
   third-party lookup), charm endings, an anchor ("valor" crossed out), the price per day of the week
   ("menos que un café al día"), and the guarantee next to the button.
3. **A visible before/after:** Day 1 and Day 7 recordings side by side, saved to the account: the
   product's proof, and the student's own trophy.
4. **Free tools as the funnel:** strict usage meters that explain what the Sprint unlocks, never a blank
   wall.
5. **Tutor-side leverage:** a tutor dashboard listing every student, their day, streak, last activity
   and recordings, so Mei can message the one who went quiet before they quit.

### Product designer (onboarding, engagement, feeling accompanied)
1. **"Tu tutora" tab:** Mei's card, her availability, the student's booked calls, a one-tap WhatsApp
   button (paid only), and a short "message from Mei" for today.
2. **Day-by-day Sprint with a guide:** each day opens with May (the Buddy) saying today's goal, then
   a checklist of tasks; finishing a day unlocks the next with a small celebration.
3. **Streak and progress ring:** the week as seven circles, the current day pulsing; a friendly nudge
   when today is unfinished ("May sigue esperándote").
4. **Thank-you page as a moment:** confetti, the student's name, a countdown to their start, three big
   next steps (book call 1, say hi on WhatsApp, add the week to the calendar) with ticks as they do them.
5. **Resources library:** printable cheat sheets (phrase bank, the 16 typical mistakes, survival
   questions), pronunciation tips, and "what to say when you freeze".

### Software engineer (platform, integrations)
1. **Accounts on Cloudflare (free):** the existing Worker plus D1 (SQLite) and the same domain:
   email and password (PBKDF2 in WebCrypto), httpOnly session cookie, roles (student, tutor), no
   third-party auth provider and no monthly cost.
2. **Server-side usage meters:** the Worker counts Speech Mode turns, games and shadowing clips per
   account per day; anonymous visitors are counted in the browser (and by a hashed IP on the server
   for the hard limit).
3. **Enrolment record:** paid status, start Monday, region, price paid; Mei marks a payment as
   received from her dashboard (Stripe Payment Links for now; a Stripe webhook later).
4. **Progress sync:** Sprint ticks, streak, XP and Day 1 / Day 7 recordings stored per account, so a
   student can switch phone and keep their week.
5. **Calendar file and booking links:** an .ics for the seven days, generated on the page; the Cal.com
   booking link carries the student's name and email.

## Top five (built first)
| # | Idea | Why first | Assumption to test |
|---|------|-----------|--------------------|
| 1 | Accounts on Cloudflare D1 with roles and usage meters | Everything else hangs off it; free; on our domain | Beginners will make an account after about a minute of free use |
| 2 | Paid-only Sprint, overhauled: day path, May's daily brief, checklists, resources, Day 1/7 recordings | It is what the £49 buys; must feel full | Structure plus a person makes beginners finish the week |
| 3 | "Tu tutora" tab with WhatsApp (paid only), call booking, today's message | Answers "I paid, now what?" in one place | A visible human stops day-2 drop-off |
| 4 | Tutor dashboard: students, day, streak, last active, mark paid | Lets one tutor look after five students well | Mei can spot a quiet student in time |
| 5 | Thank-you page as a celebration with next steps | First paid moment sets the tone; reduces "did it work?" messages | Students complete the three steps within a day |

Later: Stripe webhook, email reminders, Spanish/English audio for every resource, certificates as images
to share.
