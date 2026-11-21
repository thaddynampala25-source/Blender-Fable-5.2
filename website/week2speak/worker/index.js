/* Week2Speak API: accounts, usage limits, the 7-Day Sprint enrolment and the tutor's tools.
   Runs in the same Cloudflare Worker that serves the site (static assets); only /api/* reaches this code.
   Storage: Cloudflare D1 (binding DB). Free tier; no third-party auth.

   Settings (wrangler.jsonc "vars", or secrets for the ones marked secret):
     PLACES_TOTAL     Sprint places open at a time (testing phase: 5)
     TUTOR_EMAILS     comma-separated emails that get the tutor role
     TUTOR_WHATSAPP   tutor's WhatsApp number, digits with country code (shown to paid students only)
     CAL_LINK         Cal.com booking page for the two calls (shown to paid students only)
     PAY_LINKS        JSON {tierId: Stripe Payment Link URL}
     STRIPE_WEBHOOK_SECRET (secret)  signing secret of the Stripe webhook
     IP_SALT (secret)  any random string; IPs are only ever stored hashed with it              */

const DAY = 86400, SESSION_DAYS = 30, COOKIE = 'w2s_s';

// Free use: anonymous visitors are limited in the browser (a minute or so); free accounts per day here.
const LIMITS = {free: {speak: 10, game: 3, shadow: 5, lesson: 2}, paid: null};

// Regional prices. amount and anchor are in minor units; zero-decimal currencies noted.
const TIERS = {
  gbp:       {currency: 'GBP', amount: 4900,     anchor: 12900,    symbol: '£',   zero: false},
  eur:       {currency: 'EUR', amount: 4900,     anchor: 12900,    symbol: '€',   zero: false},
  eur_es:    {currency: 'EUR', amount: 3900,     anchor: 10900,    symbol: '€',   zero: false},
  usd:       {currency: 'USD', amount: 4900,     anchor: 12900,    symbol: 'US$', zero: false},
  usd_latam: {currency: 'USD', amount: 2900,     anchor: 7900,     symbol: 'US$', zero: false},
  mxn:       {currency: 'MXN', amount: 69000,    anchor: 189000,   symbol: 'MX$', zero: false},
  cop:       {currency: 'COP', amount: 11990000, anchor: 34990000, symbol: 'COP', zero: false},
};
const COUNTRY_TIER = {GB: 'gbp', ES: 'eur_es', PT: 'eur_es', MX: 'mxn', CO: 'cop',
  US: 'usd', CA: 'usd', AU: 'usd', NZ: 'usd', CH: 'usd', NO: 'usd', SE: 'usd', DK: 'usd', IS: 'usd',
  AR: 'usd_latam', BO: 'usd_latam', CL: 'usd_latam', CR: 'usd_latam', CU: 'usd_latam', DO: 'usd_latam', EC: 'usd_latam', SV: 'usd_latam',
  GT: 'usd_latam', HN: 'usd_latam', NI: 'usd_latam', PA: 'usd_latam', PY: 'usd_latam', PE: 'usd_latam', PR: 'usd_latam', UY: 'usd_latam', VE: 'usd_latam', GQ: 'usd_latam'};
const EURO = new Set(['AT', 'BE', 'CY', 'DE', 'EE', 'FI', 'FR', 'GR', 'HR', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'SI', 'SK']);
function tierFor(country) { return COUNTRY_TIER[country] || (EURO.has(country) ? 'eur' : 'usd'); }
function price(country, env) {
  const id = tierFor(country), t = TIERS[id]; let links = {}; try { links = JSON.parse(env.PAY_LINKS || '{}'); } catch (e) {}
  // the struck-through reference price shows only when SHOW_ANCHOR is "1": UK law requires it to be a genuine price (e.g. the price after the testing phase)
  return {tier: id, currency: t.currency, amount: t.amount, anchor: env.SHOW_ANCHOR === '1' ? t.anchor : null, symbol: t.symbol, perDay: Math.round(t.amount / 7), payable: !!links[id]};
}

/* ---------- helpers ---------- */
const enc = new TextEncoder();
const hex = b => [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('');
const b64u = b => btoa(String.fromCharCode(...new Uint8Array(b))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const rand = n => crypto.getRandomValues(new Uint8Array(n));
const sha256 = async s => hex(await crypto.subtle.digest('SHA-256', enc.encode(s)));
const now = () => Math.floor(Date.now() / 1000);
const today = () => new Date().toISOString().slice(0, 10);
const uid = () => b64u(rand(12));
async function pbkdf2(password, saltHex) {
  const key = await crypto.subtle.importKey('raw', enc.encode(password), 'PBKDF2', false, ['deriveBits']);
  const salt = new Uint8Array(saltHex.match(/../g).map(h => parseInt(h, 16)));
  return hex(await crypto.subtle.deriveBits({name: 'PBKDF2', hash: 'SHA-256', salt, iterations: 100000}, key, 256));
}
function same(a, b) { if (a.length !== b.length) return false; let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i); return d === 0; }
function json(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), {status, headers: Object.assign({'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store'}, headers)});
}
const err = (code, status = 400) => json({error: code}, status);
function cookieOf(req, name) { const m = (req.headers.get('cookie') || '').match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)')); return m ? m[1] : null; }
function setCookie(token, maxAge) { return `${COOKIE}=${token}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${maxAge}`; }
async function body(req) { const t = await req.text(); if (t.length > 20000) throw new Error('too big'); return t ? JSON.parse(t) : {}; }
const cleanEmail = e => String(e || '').trim().toLowerCase().slice(0, 120);
const okEmail = e => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(e);
const tutorEmails = env => String(env.TUTOR_EMAILS || '').split(',').map(cleanEmail).filter(Boolean);
const ipKey = async (req, env) => sha256((req.headers.get('cf-connecting-ip') || '0') + '|' + (env.IP_SALT || 'w2s'));

async function throttle(env, key, max) {
  const hour = new Date().toISOString().slice(0, 13);
  const r = await env.DB.prepare('INSERT INTO throttle (key, hour, n) VALUES (?1, ?2, 1) ON CONFLICT(key, hour) DO UPDATE SET n = n + 1 RETURNING n').bind(key, hour).first();
  return r.n <= max;
}
async function newSession(env, userId) {
  const token = b64u(rand(32)), t = now();
  await env.DB.prepare('INSERT INTO sessions (id, user_id, created_at, expires_at) VALUES (?1, ?2, ?3, ?4)').bind(await sha256(token), userId, t, t + SESSION_DAYS * DAY).run();
  return setCookie(token, SESSION_DAYS * DAY);
}
async function currentUser(req, env) {
  const token = cookieOf(req, COOKIE); if (!token) return null;
  const row = await env.DB.prepare('SELECT u.* FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.id = ?1 AND s.expires_at > ?2').bind(await sha256(token), now()).first();
  if (row && (!row.last_seen || now() - row.last_seen > 300)) await env.DB.prepare('UPDATE users SET last_seen = ?1 WHERE id = ?2').bind(now(), row.id).run();
  return row || null;
}
async function enrollmentOf(env, userId) { return env.DB.prepare('SELECT * FROM enrollments WHERE user_id = ?1').bind(userId).first(); }
async function placesLeft(env) {
  const total = parseInt(env.PLACES_TOTAL || '5', 10);
  const r = await env.DB.prepare("SELECT COUNT(*) AS n FROM enrollments WHERE status = 'paid' OR (status = 'pending' AND created_at > ?1)").bind(now() - 2 * DAY).first();
  return {total, left: Math.max(0, total - r.n)};
}
const isPaid = e => !!(e && e.status === 'paid');
function publicUser(u) { return {id: u.id, name: u.name, email: u.email, role: u.role, lang: u.lang, country: u.country, createdAt: u.created_at}; }
function tutorContact(env, u) {
  const wa = String(env.TUTOR_WHATSAPP || '').replace(/\D/g, '');
  const hi = (u.lang === 'en' ? 'Hi Mei! I am ' : '¡Hola, Mei! Soy ') + u.name + (u.lang === 'en' ? ', from the 7-Day Sprint.' : ', del Sprint de 7 días.');
  const cal = env.CAL_LINK ? env.CAL_LINK + (env.CAL_LINK.includes('?') ? '&' : '?') + 'name=' + encodeURIComponent(u.name) + '&email=' + encodeURIComponent(u.email) : null;
  return {whatsapp: wa ? 'https://wa.me/' + wa + '?text=' + encodeURIComponent(hi) : null, booking: cal};
}

/* ---------- routes ---------- */
async function me(req, env) {
  const country = (req.cf && req.cf.country) || req.headers.get('cf-ipcountry') || 'XX';
  const out = {country, price: price(country, env), places: await placesLeft(env), limits: LIMITS, user: null, count: env.COUNT_PRACTICE === '1'};
  const u = await currentUser(req, env); if (!u) return json(out);
  const e = await enrollmentOf(env, u.id), paid = isPaid(e) || u.role === 'tutor';
  const usage = {}; (await env.DB.prepare('SELECT kind, n FROM usage WHERE user_id = ?1 AND day = ?2').bind(u.id, today()).all()).results.forEach(r => { usage[r.kind] = r.n; });
  const prog = await env.DB.prepare('SELECT data FROM progress WHERE user_id = ?1').bind(u.id).first();
  const notes = (await env.DB.prepare('SELECT body, created_at FROM notes WHERE user_id = ?1 ORDER BY created_at DESC LIMIT 20').bind(u.id).all()).results;
  if (u.country !== country && country !== 'XX') await env.DB.prepare('UPDATE users SET country = ?1 WHERE id = ?2').bind(country, u.id).run();
  return json(Object.assign(out, {
    user: publicUser(u), plan: paid ? 'paid' : 'free', usage,
    enrollment: e ? {status: e.status, start: e.start_date, paidAt: e.paid_at} : null,
    progress: prog ? JSON.parse(prog.data) : null, notes,
    tutor: paid ? tutorContact(env, u) : null,
  }));
}

async function signup(req, env) {
  const b = await body(req), email = cleanEmail(b.email), name = String(b.name || '').trim().slice(0, 60), pw = String(b.password || '');
  if (!name) return err('name'); if (!okEmail(email)) return err('email'); if (pw.length < 8) return err('password');
  if (!(await throttle(env, 'signup:' + await ipKey(req, env), 10))) return err('slow_down', 429);
  if (await env.DB.prepare('SELECT 1 FROM users WHERE email = ?1').bind(email).first()) return err('exists', 409);
  const id = uid(), salt = hex(rand(16)), role = tutorEmails(env).includes(email) ? 'tutor' : 'student';
  const country = (req.cf && req.cf.country) || null, lang = b.lang === 'en' ? 'en' : 'es';
  await env.DB.prepare('INSERT INTO users (id, email, name, pw_hash, pw_salt, role, country, lang, source, created_at, last_seen) VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?10)')
    .bind(id, email, name, await pbkdf2(pw, salt), salt, role, country, lang, String(b.source || '').slice(0, 60) || null, now()).run();
  // practice done before signing up (anonymous progress) is kept
  if (b.progress && typeof b.progress === 'object') await env.DB.prepare('INSERT INTO progress (user_id, data, updated_at) VALUES (?1, ?2, ?3)').bind(id, JSON.stringify(b.progress).slice(0, 60000), now()).run();
  return json({ok: true}, 200, {'set-cookie': await newSession(env, id)});
}

async function login(req, env) {
  const b = await body(req), email = cleanEmail(b.email), pw = String(b.password || '');
  if (!(await throttle(env, 'login:' + await ipKey(req, env), 20))) return err('slow_down', 429);
  const u = await env.DB.prepare('SELECT * FROM users WHERE email = ?1').bind(email).first();
  if (!u || !same(await pbkdf2(pw, u.pw_salt), u.pw_hash)) return err('wrong', 401);
  if (u.role !== 'tutor' && tutorEmails(env).includes(email)) await env.DB.prepare("UPDATE users SET role = 'tutor' WHERE id = ?1").bind(u.id).run();
  return json({ok: true}, 200, {'set-cookie': await newSession(env, u.id)});
}

async function logout(req, env) {
  const token = cookieOf(req, COOKIE); if (token) await env.DB.prepare('DELETE FROM sessions WHERE id = ?1').bind(await sha256(token)).run();
  return json({ok: true}, 200, {'set-cookie': setCookie('', 0)});
}

async function useOne(req, env, u) {
  const b = await body(req), kind = String(b.kind || ''); if (!['speak', 'game', 'shadow', 'lesson'].includes(kind)) return err('kind');
  const e = await enrollmentOf(env, u.id);
  if (isPaid(e) || u.role === 'tutor') return json({ok: true, unlimited: true});
  const lim = LIMITS.free[kind];
  const cur = await env.DB.prepare('SELECT n FROM usage WHERE user_id = ?1 AND day = ?2 AND kind = ?3').bind(u.id, today(), kind).first();
  if (cur && cur.n >= lim) return json({ok: false, used: cur.n, limit: lim, left: 0}, 403);
  const r = await env.DB.prepare('INSERT INTO usage (user_id, day, kind, n) VALUES (?1, ?2, ?3, 1) ON CONFLICT(user_id, day, kind) DO UPDATE SET n = n + 1 RETURNING n').bind(u.id, today(), kind).first();
  return json({ok: true, used: r.n, limit: lim, left: Math.max(0, lim - r.n)});
}

async function saveProgress(req, env, u) {
  const b = await body(req); if (!b.data || typeof b.data !== 'object') return err('data');
  const s = JSON.stringify(b.data); if (s.length > 60000) return err('too_big', 413);
  await env.DB.prepare('INSERT INTO progress (user_id, data, updated_at) VALUES (?1, ?2, ?3) ON CONFLICT(user_id) DO UPDATE SET data = ?2, updated_at = ?3').bind(u.id, s, now()).run();
  return json({ok: true});
}

function nextMondays(n) {
  const out = [], d = new Date(); d.setUTCHours(0, 0, 0, 0);
  d.setUTCDate(d.getUTCDate() + ((8 - d.getUTCDay()) % 7 || 7));   // the next Monday (never today)
  for (let i = 0; i < n; i++) { out.push(d.toISOString().slice(0, 10)); d.setUTCDate(d.getUTCDate() + 7); }
  return out;
}

async function enroll(req, env, u) {
  const b = await body(req), starts = nextMondays(4), start = starts.includes(b.start) ? b.start : starts[0];
  const e = await enrollmentOf(env, u.id);
  if (isPaid(e)) return json({ok: true, paid: true});
  const p = price(u.country || (req.cf && req.cf.country) || 'XX', env);
  if (!e || e.status !== 'pending') {
    const pl = await placesLeft(env); if (pl.left <= 0) return err('full', 409);
  }
  const id = e ? e.id : uid();
  await env.DB.prepare("INSERT INTO enrollments (id, user_id, status, start_date, tier, currency, amount, created_at) VALUES (?1, ?2, 'pending', ?3, ?4, ?5, ?6, ?7) ON CONFLICT(user_id) DO UPDATE SET status = 'pending', start_date = ?3, tier = ?4, currency = ?5, amount = ?6, created_at = ?7")
    .bind(id, u.id, start, p.tier, p.currency, p.amount, now()).run();
  let links = {}; try { links = JSON.parse(env.PAY_LINKS || '{}'); } catch (x) {}
  const link = links[p.tier];
  const payUrl = link ? link + (link.includes('?') ? '&' : '?') + 'client_reference_id=' + encodeURIComponent(id) + '&prefilled_email=' + encodeURIComponent(u.email) : null;
  return json({ok: true, start, payUrl});
}

// anonymous practice counts: on only when COUNT_PRACTICE is "1" (the privacy notice must say so first)
async function practiceCount(req, env) {
  if (env.COUNT_PRACTICE !== '1') return json({ok: true, counted: false});
  const b = await body(req), kinds = ['speak', 'game', 'shadow', 'lesson'];
  const list = [...new Set([].concat(b.kinds || []).filter(k => kinds.includes(k)))]; if (!list.length) return err('kind');
  if (!(await throttle(env, 'count:' + await ipKey(req, env), 30))) return json({ok: true, counted: false});
  if (b.first) list.push('any');
  const day = today(), st = env.DB.prepare('INSERT INTO practice_daily (day, kind, n) VALUES (?1, ?2, 1) ON CONFLICT(day, kind) DO UPDATE SET n = n + 1');
  await env.DB.batch(list.map(k => st.bind(day, k)));
  return json({ok: true, counted: true});
}

async function waitlist(req, env) {
  const b = await body(req), email = cleanEmail(b.email); if (!okEmail(email)) return err('email');
  if (!(await throttle(env, 'wait:' + await ipKey(req, env), 10))) return err('slow_down', 429);
  await env.DB.prepare('INSERT OR IGNORE INTO waitlist (email, name, country, created_at) VALUES (?1, ?2, ?3, ?4)').bind(email, String(b.name || '').slice(0, 60), (req.cf && req.cf.country) || null, now()).run();
  return json({ok: true});
}

async function resetPassword(req, env) {
  const b = await body(req), pw = String(b.password || ''); if (pw.length < 8) return err('password');
  const r = await env.DB.prepare('SELECT * FROM resets WHERE id = ?1 AND expires_at > ?2').bind(await sha256(String(b.token || '')), now()).first();
  if (!r) return err('expired', 410);
  const salt = hex(rand(16));
  await env.DB.batch([
    env.DB.prepare('UPDATE users SET pw_hash = ?1, pw_salt = ?2 WHERE id = ?3').bind(await pbkdf2(pw, salt), salt, r.user_id),
    env.DB.prepare('DELETE FROM resets WHERE user_id = ?1').bind(r.user_id),
    env.DB.prepare('DELETE FROM sessions WHERE user_id = ?1').bind(r.user_id)]);
  return json({ok: true}, 200, {'set-cookie': await newSession(env, r.user_id)});
}

async function deleteAccount(req, env, u) {
  const b = await body(req);
  if (!same(await pbkdf2(String(b.password || ''), u.pw_salt), u.pw_hash)) return err('wrong', 401);
  await env.DB.batch(['sessions', 'usage', 'progress', 'notes', 'resets', 'enrollments'].map(t => env.DB.prepare(`DELETE FROM ${t} WHERE user_id = ?1`).bind(u.id)).concat([env.DB.prepare('DELETE FROM users WHERE id = ?1').bind(u.id)]));
  return json({ok: true}, 200, {'set-cookie': setCookie('', 0)});
}

/* ---------- the tutor ---------- */
async function students(req, env) {
  const rows = (await env.DB.prepare(`SELECT u.id, u.name, u.email, u.country, u.lang, u.source, u.created_at, u.last_seen,
      e.status, e.start_date, e.tier, e.currency, e.amount, e.paid_at, p.data AS progress, p.updated_at AS progress_at,
      (SELECT COALESCE(SUM(n), 0) FROM usage g WHERE g.user_id = u.id) AS practice
    FROM users u LEFT JOIN enrollments e ON e.user_id = u.id LEFT JOIN progress p ON p.user_id = u.id
    WHERE u.role = 'student' ORDER BY (e.status = 'paid') DESC, (e.status = 'pending') DESC, u.last_seen DESC LIMIT 500`).all()).results;
  rows.forEach(r => { try { r.progress = r.progress ? JSON.parse(r.progress) : null; } catch (x) { r.progress = null; } });
  return json({students: rows, places: await placesLeft(env), waitlist: (await env.DB.prepare('SELECT * FROM waitlist ORDER BY created_at DESC LIMIT 200').all()).results});
}
async function setEnrollment(req, env) {
  const b = await body(req), status = ['pending', 'paid', 'cancelled', 'refunded'].includes(b.status) ? b.status : null; if (!status || !b.userId) return err('bad');
  const u = await env.DB.prepare('SELECT * FROM users WHERE id = ?1').bind(b.userId).first(); if (!u) return err('no_user', 404);
  const p = price(u.country || 'XX', env), start = /^\d{4}-\d{2}-\d{2}$/.test(b.start || '') ? b.start : nextMondays(1)[0];
  await env.DB.prepare(`INSERT INTO enrollments (id, user_id, status, start_date, tier, currency, amount, created_at, paid_at) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9)
    ON CONFLICT(user_id) DO UPDATE SET status = ?3, start_date = COALESCE(?10, start_date), paid_at = CASE WHEN ?3 = 'paid' THEN COALESCE(paid_at, ?8) ELSE paid_at END`)
    .bind(uid(), u.id, status, start, p.tier, p.currency, p.amount, now(), status === 'paid' ? now() : null, b.start || null).run();
  return json({ok: true});
}
async function addNote(req, env) {
  const b = await body(req), text = String(b.body || '').trim().slice(0, 1000); if (!text || !b.userId) return err('bad');
  await env.DB.prepare('INSERT INTO notes (id, user_id, body, created_at) VALUES (?1, ?2, ?3, ?4)').bind(uid(), b.userId, text, now()).run();
  return json({ok: true});
}
async function resetLink(req, env) {
  const b = await body(req); if (!b.userId) return err('bad');
  const token = b64u(rand(24));
  await env.DB.prepare('INSERT INTO resets (id, user_id, expires_at) VALUES (?1, ?2, ?3)').bind(await sha256(token), b.userId, now() + DAY).run();
  return json({ok: true, path: '/cuenta/?reset=' + token});
}

/* ---------- Stripe: a paid Payment Link unlocks the Sprint at once ---------- */
async function stripeWebhook(req, env) {
  const raw = await req.text(), sig = req.headers.get('stripe-signature') || '';
  if (!env.STRIPE_WEBHOOK_SECRET) return err('not_configured', 503);
  const parts = Object.fromEntries(sig.split(',').map(kv => kv.split('=')));
  if (!parts.t || !parts.v1 || Math.abs(now() - parseInt(parts.t, 10)) > 300) return err('signature', 400);
  const key = await crypto.subtle.importKey('raw', enc.encode(env.STRIPE_WEBHOOK_SECRET), {name: 'HMAC', hash: 'SHA-256'}, false, ['sign']);
  const expected = hex(await crypto.subtle.sign('HMAC', key, enc.encode(parts.t + '.' + raw)));
  if (!same(expected, parts.v1)) return err('signature', 400);
  const ev = JSON.parse(raw);
  if ((ev.type === 'checkout.session.completed' || ev.type === 'checkout.session.async_payment_succeeded') && ev.data && ev.data.object) {
    const s = ev.data.object, ref = s.client_reference_id;
    if (ref && s.payment_status === 'paid')
      await env.DB.prepare("UPDATE enrollments SET status = 'paid', paid_at = ?1, stripe_session = ?2, amount = COALESCE(?3, amount), currency = COALESCE(UPPER(?4), currency) WHERE id = ?5")
        .bind(now(), s.id, s.amount_total || null, s.currency || null, ref).run();
  }
  return json({received: true});
}

/* ---------- router ---------- */
export default {
  async fetch(req, env) {
    const url = new URL(req.url), path = url.pathname, m = req.method;
    // the paid Sprint's content: only for paid students and the tutor
    if (path.startsWith('/paid/')) {
      const u = await currentUser(req, env); if (!u) return err('signed_out', 401);
      if (u.role !== 'tutor' && !isPaid(await enrollmentOf(env, u.id))) return err('not_paid', 403);
      const r = await env.ASSETS.fetch(req), h = new Headers(r.headers); h.set('cache-control', 'private, no-store');
      return new Response(r.body, {status: r.status, headers: h});
    }
    if (!path.startsWith('/api/')) return env.ASSETS.fetch(req);
    try {
      if (path === '/api/stripe/webhook' && m === 'POST') return await stripeWebhook(req, env);
      // state-changing requests must come from this site
      if (m !== 'GET') { const o = req.headers.get('origin'); if (o && new URL(o).host !== url.host) return err('origin', 403); }
      if (path === '/api/me' && m === 'GET') return await me(req, env);
      if (path === '/api/signup' && m === 'POST') return await signup(req, env);
      if (path === '/api/login' && m === 'POST') return await login(req, env);
      if (path === '/api/logout' && m === 'POST') return await logout(req, env);
      if (path === '/api/waitlist' && m === 'POST') return await waitlist(req, env);
      if (path === '/api/reset' && m === 'POST') return await resetPassword(req, env);
      if (path === '/api/count' && m === 'POST') return await practiceCount(req, env);
      if (path === '/api/starts' && m === 'GET') return json({starts: nextMondays(4)});
      const u = await currentUser(req, env); if (!u) return err('signed_out', 401);
      if (path === '/api/usage' && m === 'POST') return await useOne(req, env, u);
      if (path === '/api/progress' && m === 'POST') return await saveProgress(req, env, u);
      if (path === '/api/enroll' && m === 'POST') return await enroll(req, env, u);
      if (path === '/api/account/delete' && m === 'POST') return await deleteAccount(req, env, u);
      if (path.startsWith('/api/tutor/')) {
        if (u.role !== 'tutor') return err('forbidden', 403);
        if (path === '/api/tutor/students' && m === 'GET') return await students(req, env);
        if (path === '/api/tutor/enrollment' && m === 'POST') return await setEnrollment(req, env);
        if (path === '/api/tutor/note' && m === 'POST') return await addNote(req, env);
        if (path === '/api/tutor/reset-link' && m === 'POST') return await resetLink(req, env);
      }
      return err('not_found', 404);
    } catch (e) {
      return err('server', 500);
    }
  },
};
