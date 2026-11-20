/* Week2Speak accounts in the browser: who you are, what you may use, and the pages that depend on it
   (Join, the paid Sprint, Tutor, your account, thank-you). Talks to /api/* (worker/index.js).
   Practice stays free with limits: anonymous visitors get about a minute, free accounts a little each day,
   Sprint students and the tutor have no limits. */
(function () {
'use strict';
const LANG = document.documentElement.lang === 'en' ? 'en' : 'es';
const SLUGS = {"es": {"home": "/", "speak": "/modo-habla/", "games": "/juegos/", "shadow": "/shadowing/", "sprint": "/sprint-7-dias/", "course": "/curso/", "tutor": "/tutora/", "join": "/unete/", "mistakes": "/errores-comunes/", "about": "/como-ensenamos/", "privacy": "/privacidad/", "terms": "/terminos/", "account": "/cuenta/", "thanks": "/gracias/"}, "en": {"home": "/en/", "speak": "/en/speech-mode/", "games": "/en/games/", "shadow": "/en/shadowing/", "sprint": "/en/7-day-sprint/", "course": "/en/course/", "tutor": "/en/tutor/", "join": "/en/join/", "mistakes": "/en/common-mistakes/", "about": "/en/about/", "privacy": "/en/privacy/", "terms": "/en/terms/", "account": "/en/account/", "thanks": "/en/thanks/"}}, P = SLUGS[LANG];
const PAGE = document.body.dataset.page || 'home';
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

const STR = {
 es: {
  signin: 'Entrar', signup: 'Crear cuenta', myAccount: 'Mi cuenta', mySprint: 'Mi Sprint', desk: 'Mi panel', startSprint: 'Empieza tu Sprint',
  name: 'Tu nombre', email: 'Email', password: 'Contraseña', pwHint: 'Mínimo 8 caracteres', source: '¿Cómo nos encontraste?',
  sources: [['', 'Elige una opción'], ['tiktok', 'TikTok'], ['instagram', 'Instagram'], ['facebook', 'Facebook'], ['youtube', 'YouTube'], ['friend', 'Me lo contó alguien'], ['google', 'Google'], ['other', 'Otro']],
  createFree: 'Crear mi cuenta gratis', doSignin: 'Entrar', haveAccount: '¿Ya tienes cuenta?', noAccount: '¿Todavía no tienes cuenta?',
  legal: 'Al crear tu cuenta aceptas los <a href="{terms}">términos</a> y el <a href="{privacy}">aviso de privacidad</a>.',
  forgot: '¿Olvidaste tu contraseña? Escríbenos a hello@week2speak.com y te mandamos un enlace para cambiarla.',
  err: {name: 'Escribe tu nombre.', email: 'Revisa tu email (por ejemplo, nombre@gmail.com).', password: 'La contraseña necesita al menos 8 caracteres.', exists: 'Ya hay una cuenta con ese email. Entra con tu contraseña.', wrong: 'El email o la contraseña no coinciden.', slow_down: 'Demasiados intentos. Espera un rato y vuelve a probar.', expired: 'Este enlace ya no sirve. Pide uno nuevo.', full: 'Esta tanda acaba de llenarse.', offline: 'No hemos podido conectar. Revisa tu conexión y vuelve a probar.', server: 'Algo ha fallado por nuestra parte. Prueba otra vez en un momento.'},
  welcome: '¡Bienvenido, {name}!', welcomeBack: '¡Hola de nuevo, {name}!', bye: 'Has cerrado sesión.',
  anonTitle: 'Crea tu cuenta gratis para seguir', anonBody: 'Vas muy bien. Con una cuenta gratis sigues practicando hoy y guardas lo que llevas.',
  softTitle: '¿Guardamos tu progreso?', softBody: 'Crea tu cuenta gratis en 20 segundos y no pierdas lo que has practicado.', later: 'Ahora no',
  freeTitle: 'Has llegado al límite de hoy', freeBody: 'Mañana tienes más práctica gratis. O empieza tu Sprint: práctica sin límites y Mei a tu lado toda la semana.', seeSprint: 'Ver el Sprint', tomorrow: 'Vale, hasta mañana',
  lessonTitle: 'Esta lección es del Sprint', lessonAnon: 'Crea tu cuenta gratis para abrir la lección 2. El curso completo viene con el Sprint.', lessonFree: 'Las lecciones 3 a 7 vienen con el Sprint, junto con las llamadas y el WhatsApp de Mei.',
  kinds: {speak: 'Respuestas en Modo Habla', game: 'Partidas de juegos', shadow: 'Repeticiones de shadowing', lesson: 'Lecciones del curso'},
  myDesk: 'Mi panel', consent: 'Marca la casilla para confirmar cuándo empieza tu Sprint.', left: (n, what) => `${what}: ${n === 1 ? 'te queda 1' : 'te quedan ' + n} hoy`, unlimited: 'Sin límites', close: 'Cerrar',
  places: n => n === 1 ? 'Queda 1 plaza' : n > 1 ? `Quedan ${n} plazas` : 'Plazas agotadas',
  of: (n, t) => `de ${t} en esta fase de prueba`,
  perDay: 'Son {p} al día durante tu semana.', value: 'Valor',
  monday: 'Lunes', reserving: 'Reservando tu plaza…', toPay: 'Te llevamos al pago seguro…', reservedNoPay: 'Plaza reservada. Mei te escribirá en menos de 24 horas para completar el pago.',
  alreadyPaid: 'Ya tienes tu plaza. ¡Vamos al Sprint!', signFirst: 'Primero crea tu cuenta gratis (o entra) y seguimos con la reserva.',
  waitOk: '¡Apuntado! Te avisamos en cuanto haya plazas.',
  day: 'Día', today: 'Hoy', done: 'Hecho', dayN: n => n === 0 ? 'Día 0' : `Día ${n}`, yourWeek: 'Tu semana', hiName: 'Hola, {name}',
  startsOn: 'Tu Sprint empieza el {date}.', started: 'Vas por el día {n}.', finished: '¡Sprint completado!',
  brief: 'May te cuenta', whyToday: 'Por qué importa', phrases: 'Las frases de hoy', freeze: 'Si te quedas en blanco', mistake: 'El error típico', challenge: 'El reto de hoy', reflect: 'Antes de cerrar el día',
  listen: 'Escuchar', go: {game: 'Jugar', scene: 'Hablar con el Buddy', clip: 'Hacer shadowing'}, practise: 'Practica en las salas',
  markDone: 'He terminado el día', dayDone: '¡Día completado!', reopen: 'Volver a abrir',
  step: {book: 'Reservar', whatsapp: 'Escribir', record: 'Grabar', reasons: 'Escribir', calendar: 'Añadir'},
  reasonsPh: 'Quiero hablar inglés porque…', saved: 'Guardado', openRes: 'Abrir', seePage: 'Ver la página',
  notesEmpty: 'Todavía no hay mensajes. Mei te escribirá aquí durante tu semana.',
  ideas: ['Mándale tu frase favorita de hoy en un audio.', 'Cuéntale qué parte te está costando más.', 'Pregúntale cómo se dice algo que necesitas en tu día a día.', 'Comparte tu pequeña victoria: una frase que te salió sin pensar.'],
  planFree: 'Cuenta gratis', planPaid: 'Sprint activo', planTutor: 'Tutora', pending: 'Pago pendiente',
  acSprintFree: 'Todavía no estás en el Sprint. Reserva tu plaza y practica sin límites, con Mei a tu lado.', acSprintPending: 'Tu plaza está reservada y esperando el pago.', acSprintPaid: 'Estás dentro. Tu Sprint empieza el {date}.',
  goSprint: 'Ir a mi Sprint', bookPlace: 'Reservar mi plaza', payNow: 'Completar el pago',
  todayUse: 'Hoy', deleted: 'Tu cuenta se ha borrado.',
  tyHi: '¡{name}, ', confirming: 'Confirmando tu pago… (suele tardar unos segundos)', confirmed: 'Pago confirmado. Tu plaza es tuya.', notYet: 'Tu plaza está reservada. Si acabas de pagar, la confirmación llegará en un momento; si no, Mei te escribirá.',
  countLeft: (d, h) => d > 0 ? `Faltan ${d} ${d === 1 ? 'día' : 'días'} y ${h} ${h === 1 ? 'hora' : 'horas'}` : h > 0 ? `Faltan ${h} ${h === 1 ? 'hora' : 'horas'}` : '¡Es hoy!',
  icsTitle: 'Sprint Week2Speak: día {n}', icsDesc: '20 minutos de inglés en voz alta. Abre tu Sprint: {url}',
  desk: {paid: 'En el Sprint', pending: 'Pendiente', free: 'Gratis', places: 'Plazas libres', active: 'Activos hoy', markPaid: 'Marcar pagado', cancel: 'Cancelar plaza', note: 'Mensaje para el alumno', send: 'Enviar', reset: 'Enlace de contraseña', copied: 'Enlace copiado', lastSeen: 'Última vez', never: 'nunca', from: 'Desde', start: 'Inicio', practice: 'Práctica', day: 'Día', none: 'Nadie por aquí todavía.', wait: 'Lista de espera', source: 'Vino de'},
  ago: s => s < 3600 ? `hace ${Math.max(1, Math.round(s / 60))} min` : s < 86400 ? `hace ${Math.round(s / 3600)} h` : `hace ${Math.round(s / 86400)} d`,
 },
 en: {
  signin: 'Sign in', signup: 'Create account', myAccount: 'My account', mySprint: 'My Sprint', desk: 'My desk', startSprint: 'Start your Sprint',
  name: 'Your name', email: 'Email', password: 'Password', pwHint: 'At least 8 characters', source: 'How did you find us?',
  sources: [['', 'Choose one'], ['tiktok', 'TikTok'], ['instagram', 'Instagram'], ['facebook', 'Facebook'], ['youtube', 'YouTube'], ['friend', 'Someone told me'], ['google', 'Google'], ['other', 'Other']],
  createFree: 'Create my free account', doSignin: 'Sign in', haveAccount: 'Already have an account?', noAccount: "Don't have an account yet?",
  legal: 'By creating your account you accept the <a href="{terms}">terms</a> and the <a href="{privacy}">privacy notice</a>.',
  forgot: 'Forgot your password? Email hello@week2speak.com and we will send you a link to change it.',
  err: {name: 'Write your name.', email: 'Check your email (for example, name@gmail.com).', password: 'The password needs at least 8 characters.', exists: 'There is already an account with that email. Sign in with your password.', wrong: "The email or password doesn't match.", slow_down: 'Too many tries. Wait a while and try again.', expired: 'This link no longer works. Ask for a new one.', full: 'This round has just filled up.', offline: "We couldn't connect. Check your connection and try again.", server: 'Something went wrong on our side. Try again in a moment.'},
  welcome: 'Welcome, {name}!', welcomeBack: 'Welcome back, {name}!', bye: 'You have signed out.',
  anonTitle: 'Create your free account to keep going', anonBody: "You're doing great. With a free account you keep practising today and save what you've done.",
  softTitle: 'Shall we save your progress?', softBody: "Create your free account in 20 seconds and don't lose what you've practised.", later: 'Not now',
  freeTitle: "You've reached today's limit", freeBody: 'Tomorrow you get more free practice. Or start your Sprint: unlimited practice and Mei by your side all week.', seeSprint: 'See the Sprint', tomorrow: 'OK, see you tomorrow',
  lessonTitle: 'This lesson is part of the Sprint', lessonAnon: 'Create your free account to open lesson 2. The full course comes with the Sprint.', lessonFree: "Lessons 3 to 7 come with the Sprint, along with the calls and Mei's WhatsApp.",
  kinds: {speak: 'Speech Mode replies', game: 'Game rounds', shadow: 'Shadowing plays', lesson: 'Course lessons'},
  myDesk: 'Tutor desk', consent: 'Tick the box to confirm when your Sprint starts.', left: (n, what) => `${what}: ${n} left today`, unlimited: 'No limits', close: 'Close',
  places: n => n === 1 ? 'Only 1 place left' : n > 1 ? `${n} places left` : 'Sold out',
  of: (n, t) => `of ${t} in this testing phase`,
  perDay: "That's {p} a day during your week.", value: 'Value',
  monday: 'Monday', reserving: 'Booking your place…', toPay: 'Taking you to secure payment…', reservedNoPay: 'Place booked. Mei will message you within 24 hours to complete the payment.',
  alreadyPaid: 'You already have your place. On to the Sprint!', signFirst: 'First create your free account (or sign in) and we carry on with the booking.',
  waitOk: "You're on the list! We'll tell you as soon as there are places.",
  day: 'Day', today: 'Today', done: 'Done', dayN: n => `Day ${n}`, yourWeek: 'Your week', hiName: 'Hi, {name}',
  startsOn: 'Your Sprint starts on {date}.', started: "You're on day {n}.", finished: 'Sprint complete!',
  brief: 'May says', whyToday: 'Why it matters', phrases: "Today's phrases", freeze: 'If you go blank', mistake: 'The typical mistake', challenge: "Today's challenge", reflect: 'Before you close the day',
  listen: 'Listen', go: {game: 'Play', scene: 'Talk to the Buddy', clip: 'Shadow it'}, practise: 'Practise in the rooms',
  markDone: "I've finished the day", dayDone: 'Day complete!', reopen: 'Open again',
  step: {book: 'Book', whatsapp: 'Message', record: 'Record', reasons: 'Write', calendar: 'Add'},
  reasonsPh: 'I want to speak English because…', saved: 'Saved', openRes: 'Open', seePage: 'See the page',
  notesEmpty: 'No messages yet. Mei will write to you here during your week.',
  ideas: ["Send her today's favourite sentence as a voice note.", "Tell her which part you're finding hardest.", 'Ask her how to say something you need in your daily life.', 'Share your small win: a sentence that came out without thinking.'],
  planFree: 'Free account', planPaid: 'Sprint active', planTutor: 'Tutor', pending: 'Payment pending',
  acSprintFree: "You're not in the Sprint yet. Book your place and practise without limits, with Mei by your side.", acSprintPending: 'Your place is booked and waiting for payment.', acSprintPaid: "You're in. Your Sprint starts on {date}.",
  goSprint: 'Go to my Sprint', bookPlace: 'Book my place', payNow: 'Complete payment',
  todayUse: 'Today', deleted: 'Your account has been deleted.',
  tyHi: '{name}, ', confirming: 'Confirming your payment… (it usually takes a few seconds)', confirmed: 'Payment confirmed. The place is yours.', notYet: "Your place is booked. If you've just paid, confirmation will arrive in a moment; if not, Mei will message you.",
  countLeft: (d, h) => d > 0 ? `${d} ${d === 1 ? 'day' : 'days'} and ${h} ${h === 1 ? 'hour' : 'hours'} to go` : h > 0 ? `${h} ${h === 1 ? 'hour' : 'hours'} to go` : "It's today!",
  icsTitle: 'Week2Speak Sprint: day {n}', icsDesc: '20 minutes of English out loud. Open your Sprint: {url}',
  desk: {paid: 'In the Sprint', pending: 'Pending', free: 'Free', places: 'Places free', active: 'Active today', markPaid: 'Mark paid', cancel: 'Cancel place', note: 'Message for the student', send: 'Send', reset: 'Password link', copied: 'Link copied', lastSeen: 'Last seen', never: 'never', from: 'From', start: 'Start', practice: 'Practice', day: 'Day', none: 'Nobody here yet.', wait: 'Waitlist', source: 'Came from'},
  ago: s => s < 3600 ? `${Math.max(1, Math.round(s / 60))} min ago` : s < 86400 ? `${Math.round(s / 3600)} h ago` : `${Math.round(s / 86400)} d ago`,
 },
}[LANG];
const fill = (s, o) => String(s).replace(/\{(\w+)\}/g, (_, k) => o[k] != null ? o[k] : '');
const ICON = {
  check: '<path d="m5 12.5 4.5 4.5L19 7.5"/>', lock: '<rect x="5" y="11" width="14" height="10" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>', x: '<path d="m6 6 12 12M18 6 6 18"/>',
  play: '<path d="M8 5.5v13l10.5-6.5Z"/>', user: '<circle cx="12" cy="8" r="4"/><path d="M4.5 20a7.5 7.5 0 0 1 15 0"/>', arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
  life: '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3.5"/><path d="m6 6 3.5 3.5M18 6l-3.5 3.5M6 18l3.5-3.5M18 18l-3.5-3.5"/>', sound: '<path d="M4 10v4h4l5 4V6L8 10Z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/>',
  chat: '<path d="M4 19.5 5.6 15A8 8 0 1 1 9 18.6Z"/><path d="M9 11h6M9 14h4"/>', calendar: '<rect x="4" y="5" width="16" height="15" rx="2.5"/><path d="M4 10h16M9 3v4M15 3v4"/>',
  warn: '<path d="M12 4 2.8 19.5h18.4Z"/><path d="M12 10v4.5M12 17.2v.3"/>', star: '<path d="m12 3.5 2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.8-5.2 2.8 1-5.8-4.3-4.1 5.9-.9Z"/>',
  spark: '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
};
const ic = n => `<svg class="ic" viewBox="0 0 24 24" aria-hidden="true">${ICON[n] || ICON.spark}</svg>`;
const store = {get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } }, set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }};

/* ---------- the server ---------- */
let ME = null, ONLINE = true;
async function api(path, body) {
  let r;
  try { r = await fetch(path, body === undefined ? {credentials: 'same-origin'} : {method: 'POST', credentials: 'same-origin', headers: {'content-type': 'application/json'}, body: JSON.stringify(body)}); }
  catch (e) { return {ok: false, status: 0, data: {error: 'offline'}}; }
  let data = {}; try { data = await r.json(); } catch (e) { data = {error: r.ok ? '' : 'server'}; }
  return {ok: r.ok, status: r.status, data};
}
async function refresh() {
  const r = await api('/api/me');
  if (r.ok) { ME = r.data; ONLINE = true; } else { ONLINE = r.status !== 0 && r.status !== 404 ? true : false; ME = ME || {user: null, places: null, price: null, limits: {free: {speak: 10, game: 3, shadow: 5, lesson: 2}}}; }
  document.documentElement.dataset.plan = plan();
  return ME;
}
const user = () => ME && ME.user;
function plan() { const u = user(); if (!u) return 'anon'; if (u.role === 'tutor') return 'tutor'; return ME.plan === 'paid' ? 'paid' : 'free'; }
const unlimited = () => plan() === 'paid' || plan() === 'tutor';

/* ---------- money, dates ---------- */
const ZERO = {COP: false};
function money(minor, cur, sym) {
  const v = minor / 100, whole = Math.abs(v - Math.round(v)) < 0.005;
  const n = v.toLocaleString(LANG === 'es' ? 'es-ES' : 'en-GB', {minimumFractionDigits: whole ? 0 : 2, maximumFractionDigits: whole ? 0 : 2});
  return cur === 'COP' ? 'COP ' + n : (sym || '') + n;
}
function dateLong(iso, cap) { const d = new Date(iso + 'T12:00:00'); const s = d.toLocaleDateString(LANG === 'es' ? 'es-ES' : 'en-GB', {weekday: 'long', day: 'numeric', month: 'long'}); return cap ? s.charAt(0).toUpperCase() + s.slice(1) : s; }
function sprintDayNow(start) {   // 0 before the start, 1..7 during, 8 after
  if (!start) return 0; const s = new Date(start + 'T00:00:00'), n = new Date(); n.setHours(0, 0, 0, 0);
  const d = Math.floor((n - s) / 86400000) + 1; return d < 1 ? 0 : Math.min(8, d);
}

/* ---------- small UI: toast, modal ---------- */
function toast(text) {
  let t = $('#fxToast'); if (!t) { t = document.createElement('div'); t.id = 'fxToast'; t.className = 'fx-toast'; t.setAttribute('role', 'status'); document.body.appendChild(t); }
  t.textContent = text; t.classList.remove('on'); void t.offsetWidth; t.classList.add('on'); clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('on'), 3600);
}
let modalEl = null, lastFocus = null;
function modal(html, opts = {}) {
  closeModal(true); lastFocus = document.activeElement;
  modalEl = document.createElement('div'); modalEl.className = 'fx-modal'; modalEl.innerHTML = `<div class="fx-scrim" data-close></div><div class="fx-sheet" role="dialog" aria-modal="true" aria-labelledby="fxMT">${opts.noClose ? '' : `<button class="fx-x" type="button" data-close aria-label="${STR.close}">${ic('x')}</button>`}${html}</div>`;
  document.body.appendChild(modalEl); document.documentElement.classList.add('fx-locked');
  modalEl.addEventListener('click', e => { if (e.target.closest('[data-close]')) { closeModal(); if (opts.onClose) opts.onClose(); } });
  const f = modalEl.querySelector('input, button:not(.fx-x), a'); if (f) setTimeout(() => f.focus(), 60);
  return modalEl;
}
function closeModal(silent) { if (!modalEl) return; modalEl.remove(); modalEl = null; document.documentElement.classList.remove('fx-locked'); if (!silent && lastFocus && lastFocus.focus) lastFocus.focus(); }
document.addEventListener('keydown', e => { if (e.key === 'Escape' && modalEl && !modalEl.querySelector('[data-noesc]')) closeModal(); });

/* ---------- sign up and sign in ---------- */
function authForm(mode, after) {
  const box = document.createElement('div'); box.className = 'fx-authbox';
  const draw = m => {
    box.dataset.mode = m;
    box.innerHTML = `<form class="fx-form" novalidate>
      ${m === 'signup' ? `<label class="fx-f"><span>${STR.name}</span><input name="name" autocomplete="given-name" maxlength="60" required></label>` : ''}
      <label class="fx-f"><span>${STR.email}</span><input name="email" type="email" autocomplete="email" inputmode="email" required></label>
      <label class="fx-f"><span>${STR.password}</span><input name="password" type="password" minlength="8" autocomplete="${m === 'signup' ? 'new-password' : 'current-password'}" required>${m === 'signup' ? `<small>${STR.pwHint}</small>` : ''}</label>
      ${m === 'signup' ? `<label class="fx-f"><span>${STR.source}</span><select name="source">${STR.sources.map(([v, l]) => `<option value="${v}">${l}</option>`).join('')}</select></label>` : ''}
      <button class="key hl big fx-cta" type="submit">${m === 'signup' ? STR.createFree : STR.doSignin}</button>
      <p class="fx-msg" role="status"></p>
      ${m === 'signup' ? `<p class="fx-legal">${fill(STR.legal, {terms: P.terms, privacy: P.privacy})}</p>` : `<p class="fx-legal">${STR.forgot}</p>`}
    </form>
    <p class="fx-switch">${m === 'signup' ? STR.haveAccount : STR.noAccount} <button type="button" class="fx-link" data-switch>${m === 'signup' ? STR.signin : STR.signup}</button></p>`;
    box.querySelector('[data-switch]').addEventListener('click', () => draw(m === 'signup' ? 'signin' : 'signup'));
    box.querySelector('form').addEventListener('submit', async e => {
      e.preventDefault(); const f = e.target, msg = f.querySelector('.fx-msg'), btn = f.querySelector('button[type=submit]');
      const v = Object.fromEntries(new FormData(f).entries());
      if (m === 'signup' && !String(v.name || '').trim()) { msg.textContent = STR.err.name; return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(v.email || '').trim())) { msg.textContent = STR.err.email; return; }
      if (String(v.password || '').length < 8) { msg.textContent = STR.err.password; return; }
      btn.disabled = true; msg.textContent = '';
      const body = m === 'signup' ? Object.assign(v, {lang: LANG, progress: localProgress()}) : v;
      const r = await api(m === 'signup' ? '/api/signup' : '/api/login', body);
      btn.disabled = false;
      if (!r.ok) { msg.textContent = STR.err[r.data.error] || STR.err[r.status === 0 ? 'offline' : 'server']; return; }
      store.set('w2s.anon', {}); await refresh(); paintNav(); closeModal(true);
      toast(fill(m === 'signup' ? STR.welcome : STR.welcomeBack, {name: user().name}));
      if (m === 'signin') restoreProgress();
      if (after) after(); else route();
    });
  };
  draw(mode); return box;
}
function askAccount(title, body, after, opts = {}) {
  const el = modal(`<div class="fx-gate"><img src="${MAYPIC}" alt="" width="72" height="72"><h2 id="fxMT">${title}</h2><p>${body}</p></div>`, opts);
  el.querySelector('.fx-sheet').appendChild(authForm('signup', after));
  if (opts.soft) { const later = document.createElement('button'); later.type = 'button'; later.className = 'fx-link fx-later'; later.textContent = STR.later; later.dataset.close = ''; el.querySelector('.fx-sheet').appendChild(later); }
}
const MAYPIC = (window.W2S_BUDDIES || []).filter(b => b.id === 'may').map(b => '/assets/buddies/' + b.file + '.webp')[0] || '';

/* ---------- the header: account and the Sprint ---------- */
function paintNav() {
  const join = $('.nav-join'); if (!join) return;
  const u = user(), pl = plan();
  join.textContent = pl === 'tutor' ? STR.myDesk : pl === 'paid' ? STR.mySprint : STR.startSprint;
  join.href = pl === 'tutor' ? P.tutor : pl === 'paid' ? P.sprint : P.join;
  let me = $('.nav-me');
  if (!me) { me = document.createElement('a'); me.className = 'nav-me'; join.parentNode.insertBefore(me, join); }
  me.href = P.account;
  if (u) { me.innerHTML = `<span class="nav-av" aria-hidden="true">${esc((u.name || '?').trim().charAt(0).toUpperCase())}</span><span class="nav-me-t">${esc(u.name.split(' ')[0])}</span>`; me.setAttribute('aria-label', STR.myAccount + ': ' + u.name); }
  else { me.innerHTML = `${ic('user')}<span class="nav-me-t">${STR.signin}</span>`; me.setAttribute('aria-label', STR.signin); }
}

/* ---------- free use: count, and stop at the limit ---------- */
const ANON = {speak: 3, game: 1, shadow: 2, lesson: 1};
function usedToday(kind) {
  if (!user()) return (store.get('w2s.anon', {})[kind] || 0);
  return (ME.usage && ME.usage[kind]) || 0;
}
function limitOf(kind) { return unlimited() ? Infinity : !user() ? ANON[kind] : ((ME.limits && ME.limits.free && ME.limits.free[kind]) || 0); }
const leftOf = kind => Math.max(0, limitOf(kind) - usedToday(kind));
async function count(kind) {
  if (unlimited()) return;
  if (!user()) { const a = store.get('w2s.anon', {}); a[kind] = (a[kind] || 0) + 1; store.set('w2s.anon', a); return; }
  ME.usage = ME.usage || {}; ME.usage[kind] = (ME.usage[kind] || 0) + 1;
  const r = await api('/api/usage', {kind}); if (r.data && typeof r.data.used === 'number') ME.usage[kind] = r.data.used;
}
function blocked(kind) {
  if (unlimited() || leftOf(kind) > 0) return false;
  if (!user()) askAccount(STR.anonTitle, STR.anonBody, () => toast(STR.left(leftOf(kind), STR.kinds[kind])));
  else modal(`<div class="fx-gate"><img src="${MAYPIC}" alt="" width="72" height="72"><h2 id="fxMT">${STR.freeTitle}</h2><p>${STR.freeBody}</p><div class="fx-gate-a"><a class="key hl big" href="${P.join}">${STR.seeSprint}</a><button class="key" type="button" data-close>${STR.tomorrow}</button></div></div>`);
  return true;
}
function stop(e) { e.preventDefault(); e.stopImmediatePropagation(); }
// starting something counts against the limit; at the limit it opens the account sheet instead
document.addEventListener('click', e => {
  const t = e.target;
  if (t.closest('#speakSend, #speakMic') && PAGE === 'speak') { if (blocked('speak')) return stop(e); if (t.closest('#speakMic') && !document.getElementById('speakMic').classList.contains('listening')) count('speak'); return; }
  if (t.closest('[data-game], #gameBody .key.big, .gcards button') && PAGE === 'games') { if (blocked('game')) return stop(e); return; }
  if (t.closest('#shPlay') && PAGE === 'shadow') { if (blocked('shadow')) return stop(e); return; }
  const mod = t.closest('[data-mod]');
  if (mod && PAGE === 'course') {
    const i = +mod.dataset.mod, allowed = unlimited() ? 99 : user() ? 2 : 1;
    if (i >= allowed) { stop(e); lessonLock(); }
  }
}, true);
document.addEventListener('submit', e => { if (e.target.id === 'composer' && PAGE === 'speak') { if (blocked('speak')) return stop(e); const v = $('#speakInput'); if (v && v.value.trim()) count('speak'); } }, true);
// finished rounds and clips count (the app announces them)
document.addEventListener('w2s:activity', e => { const k = String(e.detail && e.detail.key || '').split(':')[0]; if (k === 'game' || k === 'shadow') count(k); });
function lessonLock() {
  if (!user()) askAccount(STR.lessonTitle, STR.lessonAnon);
  else modal(`<div class="fx-gate"><img src="${MAYPIC}" alt="" width="72" height="72"><h2 id="fxMT">${STR.lessonTitle}</h2><p>${STR.lessonFree}</p><div class="fx-gate-a"><a class="key hl big" href="${P.join}">${STR.seeSprint}</a><button class="key" type="button" data-close>${STR.close}</button></div></div>`);
}
// a gentle nudge after about a minute of practice without an account
function nudge() {
  if (user() || !['speak', 'games', 'shadow', 'course'].includes(PAGE) || sessionStorage.getItem('w2s.nudged')) return;
  setTimeout(() => { if (user() || modalEl || document.hidden) return; sessionStorage.setItem('w2s.nudged', '1'); askAccount(STR.softTitle, STR.softBody, null, {soft: true}); }, 60000);
}
function usageBadge() {
  const kind = {speak: 'speak', games: 'game', shadow: 'shadow'}[PAGE]; if (!kind || unlimited()) return;
  let b = $('#fxUse'); if (!b) { b = document.createElement('a'); b.id = 'fxUse'; b.className = 'fx-use'; b.href = user() ? P.join : P.account; document.body.appendChild(b); }
  const n = leftOf(kind); b.innerHTML = `${ic('spark')}<span>${STR.left(n, STR.kinds[kind])}</span>`; b.classList.toggle('low', n <= 1);
}
setInterval(() => { if (ME) usageBadge(); }, 2500);

/* ---------- progress: kept with the account ---------- */
function localProgress() { const s = store.get('w2s.v1', null); const x = store.get('w2s.x', {}); return {app: s, x}; }
function restoreProgress() {
  const p = ME && ME.progress; if (!p || !p.app) return;
  const local = store.get('w2s.v1', null);
  if (!local || (local.sessions || 0) < (p.app.sessions || 0)) { store.set('w2s.v1', p.app); if (p.x) store.set('w2s.x', p.x); if (!sessionStorage.getItem('w2s.restored')) { sessionStorage.setItem('w2s.restored', '1'); location.reload(); } }
}
let lastSync = '';
async function sync() {
  if (!user()) return; let data = localProgress(); let s = JSON.stringify(data);
  if (s.length > 55000 && data.app) { data = {app: Object.assign({}, data.app, {log: []}), x: data.x}; s = JSON.stringify(data); }
  if (s === lastSync) return; lastSync = s; await api('/api/progress', {data});
}
setInterval(sync, 30000); document.addEventListener('visibilitychange', () => { if (document.hidden) sync(); });
const X = {get: (k, d) => (store.get('w2s.x', {})[k] ?? d), set(k, v) { const x = store.get('w2s.x', {}); x[k] = v; store.set('w2s.x', x); }};

/* ---------- Join: the offer ---------- */
async function pageJoin() {
  const pr = ME.price, pl = ME.places;
  if (pr) {
    $('#pAmount').textContent = money(pr.amount, pr.currency, pr.symbol);
    if (pr.anchor) { $('#pAnchor').textContent = money(pr.anchor, pr.currency, pr.symbol); $('#pAnchor').setAttribute('aria-label', STR.value + ' ' + money(pr.anchor, pr.currency, pr.symbol)); } else $('#pAnchor').hidden = true;
    $('#pDay').innerHTML = fill(STR.perDay, {p: '<b>' + money(Math.round(pr.amount / 7), pr.currency, pr.symbol) + '</b>'});
  }
  if (pl) {
    $('#placesText').textContent = pl.left > 0 ? STR.places(pl.left) + ' ' + STR.of(pl.left, pl.total) : STR.places(0);
    $('#placesLine').classList.toggle('few', pl.left <= 2);
    if (pl.left <= 0 && !(ME.enrollment && ME.enrollment.status === 'pending')) { $('#buyBtn').hidden = true; $('#startPick').hidden = true; $('#waitForm').hidden = false; }
  }
  const st = await api('/api/starts'); const starts = (st.data && st.data.starts) || [];
  $('#starts').innerHTML = starts.map((d, i) => `<label class="fx-day-pick"><input type="radio" name="start" value="${d}"${i === 0 ? ' checked' : ''}><span><b>${dateLong(d, true)}</b></span></label>`).join('');
  if (plan() === 'paid') { $('#buyBtn').textContent = STR.goSprint; }
  $('#buyBtn').addEventListener('click', buy);
  $('#waitForm').addEventListener('submit', async e => { e.preventDefault(); const r = await api('/api/waitlist', {email: e.target.email.value, name: user() ? user().name : ''}); $('#buyMsg').textContent = r.ok ? STR.waitOk : (STR.err[r.data.error] || STR.err.server); });
}
async function buy() {
  const msg = $('#buyMsg');
  if (plan() === 'paid') { location.href = P.sprint; return; }
  if (!user()) { msg.textContent = STR.signFirst; askAccount(STR.signup, STR.signFirst, buy); return; }
  const start = ($('input[name=start]:checked') || {}).value;
  const ok = $('#buyConsent'); if (ok && !ok.checked) { msg.textContent = STR.consent; ok.closest('label').classList.add('need'); ok.focus(); return; }
  msg.textContent = STR.reserving; $('#buyBtn').disabled = true;
  const r = await api('/api/enroll', {start}); $('#buyBtn').disabled = false;
  if (!r.ok) { msg.textContent = STR.err[r.data.error] || STR.err.server; if (r.data.error === 'full') { await refresh(); pageJoin(); } return; }
  if (r.data.paid) { msg.textContent = STR.alreadyPaid; setTimeout(() => location.href = P.sprint, 900); return; }
  X.set('start', r.data.start);
  if (r.data.payUrl) { msg.textContent = STR.toPay; location.href = r.data.payUrl; }
  else { msg.textContent = STR.reservedNoPay; setTimeout(() => location.href = P.thanks, 1600); }
}

/* ---------- thank-you: the moment ---------- */
async function pageThanks() {
  const u = user(), e = ME.enrollment;
  if (u) $('#tyName').textContent = fill(STR.tyHi, {name: u.name.split(' ')[0]});
  const start = (e && e.start) || X.get('start', null);
  if (start) { $('#tyStart').textContent = dateLong(start, true); tick(start); setInterval(() => tick(start), 60000); } else $('#tyCount').hidden = true;
  confetti(); if (!reduced) chime();
  const status = $('#tyStatus');
  if (plan() !== 'paid' && u) {
    status.textContent = STR.confirming;
    for (let i = 0; i < 20 && plan() !== 'paid'; i++) { await new Promise(r => setTimeout(r, 3000)); await refresh(); }
    status.textContent = plan() === 'paid' ? STR.confirmed : STR.notYet; if (plan() === 'paid') confetti();
  } else if (plan() === 'paid') status.textContent = STR.confirmed;
  links(); steps();
}
function tick(start) {
  const ms = new Date(start + 'T09:00:00') - new Date(), d = Math.max(0, Math.floor(ms / 86400000)), h = Math.max(0, Math.floor(ms % 86400000 / 3600000));
  $('#tyLeft').textContent = STR.countLeft(d, h);
}
function links() {
  const T = ME && ME.tutor; [['#tyBook', T && T.booking], ['#tyWa', T && T.whatsapp], ['#bookBtn', T && T.booking], ['#waBtn', T && T.whatsapp]].forEach(([s, url]) => { const a = $(s); if (a) { if (url) a.href = url; else a.removeAttribute('href'); a.classList.toggle('off', !url); } });
}
function steps() {
  const done = X.get('tySteps', {}), list = $$('[data-step]'), bar = $('#tyBar');
  const paint = () => { let n = 0; list.forEach(li => { const on = !!done[li.dataset.step]; li.classList.toggle('done', on); n += on; }); if (bar) bar.style.width = (n / list.length * 100) + '%'; if (n === list.length && !X.get('tyAll', false)) { X.set('tyAll', true); confetti(); } };
  list.forEach(li => li.addEventListener('click', e => { if (!e.target.closest('a, button')) return; if (e.target.closest('#tyIcs')) downloadIcs(); done[li.dataset.step] = true; X.set('tySteps', done); setTimeout(paint, 300); }));
  paint();
}
function downloadIcs() {
  const start = (ME.enrollment && ME.enrollment.start) || X.get('start', null); if (!start) return;
  const pad = n => String(n).padStart(2, '0'), url = location.origin + P.sprint, s = new Date(start + 'T19:00:00');
  const ev = [0, 1, 2, 3, 4, 5, 6].map(i => { const d = new Date(s.getTime() + i * 86400000), f = x => `${x.getFullYear()}${pad(x.getMonth() + 1)}${pad(x.getDate())}T${pad(x.getHours())}${pad(x.getMinutes())}00`, e2 = new Date(d.getTime() + 20 * 60000);
    return ['BEGIN:VEVENT', `UID:w2s-${start}-${i}@week2speak.com`, `DTSTAMP:${f(new Date())}`, `DTSTART:${f(d)}`, `DTEND:${f(e2)}`, `SUMMARY:${fill(STR.icsTitle, {n: i + 1})}`, `DESCRIPTION:${fill(STR.icsDesc, {url})}`, `URL:${url}`, 'BEGIN:VALARM', 'TRIGGER:-PT10M', 'ACTION:DISPLAY', 'DESCRIPTION:Week2Speak', 'END:VALARM', 'END:VEVENT'].join('\r\n'); });
  const blob = new Blob([['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Week2Speak//Sprint//ES', 'CALSCALE:GREGORIAN'].join('\r\n') + '\r\n' + ev.join('\r\n') + '\r\nEND:VCALENDAR\r\n'], {type: 'text/calendar'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'week2speak-sprint.ics'; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
}
function confetti() {
  if (reduced) return; const c = $('#confetti') || (() => { const x = document.createElement('canvas'); x.className = 'fx-confetti'; document.body.appendChild(x); return x; })();
  const g = c.getContext('2d'), W = c.width = innerWidth * devicePixelRatio, H = c.height = innerHeight * devicePixelRatio, cols = ['#FFD93B', '#2D4BFF', '#19C79C', '#FF8FB1', '#FFFFFF'];
  const ps = Array.from({length: 140}, () => ({x: W / 2 + (Math.random() - .5) * W * .3, y: H * .35, vx: (Math.random() - .5) * 26 * devicePixelRatio, vy: (-Math.random() * 22 - 8) * devicePixelRatio, r: Math.random() * 6, vr: (Math.random() - .5) * .4, w: (6 + Math.random() * 8) * devicePixelRatio, h: (4 + Math.random() * 6) * devicePixelRatio, c: cols[Math.random() * cols.length | 0]}));
  let f = 0; (function step() { g.clearRect(0, 0, W, H); ps.forEach(p => { p.vy += .55 * devicePixelRatio; p.vx *= .99; p.x += p.vx; p.y += p.vy; p.r += p.vr; g.save(); g.translate(p.x, p.y); g.rotate(p.r); g.fillStyle = p.c; g.fillRect(-p.w / 2, -p.h / 2, p.w, p.h); g.restore(); }); if (++f < 170) requestAnimationFrame(step); else g.clearRect(0, 0, W, H); })();
}
function chime() {
  try { const A = new (window.AudioContext || window.webkitAudioContext)(); [523.25, 659.25, 783.99, 1046.5].forEach((fq, i) => { const o = A.createOscillator(), gn = A.createGain(); o.type = 'triangle'; o.frequency.value = fq; gn.gain.setValueAtTime(0, A.currentTime + i * .09); gn.gain.linearRampToValueAtTime(.12, A.currentTime + i * .09 + .02); gn.gain.exponentialRampToValueAtTime(.001, A.currentTime + i * .09 + .5); o.connect(gn); gn.connect(A.destination); o.start(A.currentTime + i * .09); o.stop(A.currentTime + i * .09 + .55); }); } catch (e) {}
}

/* ---------- account page ---------- */
async function pageAccount() {
  const reset = new URLSearchParams(location.search).get('reset');
  if (reset) {
    $('#acOut').hidden = true; $('#acReset').hidden = false;
    $('#resetForm').addEventListener('submit', async e => { e.preventDefault(); const m = e.target.querySelector('.fx-msg'); const r = await api('/api/reset', {token: reset, password: e.target.password.value}); if (!r.ok) { m.textContent = STR.err[r.data.error] || STR.err.server; return; } await refresh(); history.replaceState(null, '', P.account); paintNav(); route(); });
    return;
  }
  const u = user();
  $('#acOut').hidden = !!u; $('#acIn').hidden = !u; $('#acReset').hidden = true;
  if (!u) { const host = $('[data-auth-host]'); if (!host.firstChild) host.appendChild(authForm('signup')); return; }
  $('#acHi').textContent = fill(STR.hiName, {name: u.name.split(' ')[0]}); $('#acName').textContent = u.name; $('#acEmail').textContent = u.email;
  const pl = plan(), e = ME.enrollment;
  $('#acPlan').textContent = pl === 'tutor' ? STR.planTutor : pl === 'paid' ? STR.planPaid : e && e.status === 'pending' ? STR.pending : STR.planFree; $('#acPlan').dataset.plan = pl;
  $('#meters').innerHTML = ['speak', 'game', 'shadow'].map(k => { const lim = limitOf(k), used = usedToday(k); const inf = lim === Infinity; return `<div class="fx-meter"><span>${STR.kinds[k]}</span><div class="fx-bar"><i style="width:${inf ? 100 : Math.min(100, used / lim * 100)}%"></i></div><b class="num">${inf ? STR.unlimited : used + ' / ' + lim}</b></div>`; }).join('');
  $('#usageNote').textContent = unlimited() ? '' : STR.freeBody;
  $('#acSprintBody').innerHTML = pl === 'paid' || pl === 'tutor' ? `<p>${fill(STR.acSprintPaid, {date: e && e.start ? dateLong(e.start) : '—'})}</p><a class="key hl" href="${P.sprint}">${STR.goSprint}</a>`
    : e && e.status === 'pending' ? `<p>${STR.acSprintPending}</p><a class="key hl" href="${P.join}">${STR.payNow}</a>` : `<p>${STR.acSprintFree}</p><a class="key hl" href="${P.join}">${STR.bookPlace}</a>`;
  $('#logoutBtn').onclick = async () => { await api('/api/logout', {}); await sync(); await refresh(); paintNav(); toast(STR.bye); route(); };
  $('#delOpen').onclick = () => { $('#delForm').hidden = false; $('#delForm input').focus(); };
  $('#delForm').onsubmit = async ev => { ev.preventDefault(); const m = ev.target.querySelector('.fx-msg'); const r = await api('/api/account/delete', {password: ev.target.password.value}); if (!r.ok) { m.textContent = STR.err[r.data.error] || STR.err.server; return; } try { localStorage.removeItem('w2s.v1'); localStorage.removeItem('w2s.x'); } catch (x) {} await refresh(); paintNav(); toast(STR.deleted); route(); };
}

/* ---------- Tutor: three faces ---------- */
async function pageTutor() {
  const pl = plan();
  $('#tutorPublic').hidden = pl === 'paid' || pl === 'tutor'; $('#tutorStudent').hidden = pl !== 'paid'; $('#tutorDesk').hidden = pl !== 'tutor';
  if (pl === 'paid') {
    $('#tsHi').textContent = fill(STR.hiName, {name: user().name.split(' ')[0]}); links();
    const ideas = STR.ideas.slice(); const n = new Date().getDate() % ideas.length; $('#msgIdeas').innerHTML = ideas.slice(n).concat(ideas.slice(0, n)).slice(0, 3).map(x => `<li>${esc(x)}</li>`).join('');
    const notes = ME.notes || [];
    $('#notes').innerHTML = notes.length ? notes.map(nt => `<figure class="fx-note"><img src="${MAYPIC}" alt="" width="40" height="40"><blockquote>${esc(nt.body)}</blockquote><figcaption>Mei · ${new Date(nt.created_at * 1000).toLocaleDateString(LANG === 'es' ? 'es-ES' : 'en-GB', {day: 'numeric', month: 'short'})}</figcaption></figure>`).join('') : `<p class="muted">${STR.notesEmpty}</p>`;
  }
  if (pl === 'tutor') desk();
}
let deskData = null, deskFilter = 'paid';
async function desk() {
  $('#tdHi').textContent = fill(STR.hiName, {name: user().name.split(' ')[0]});
  const r = await api('/api/tutor/students'); if (!r.ok) return; deskData = r.data;
  const S = deskData.students, D = STR.desk, now = Date.now() / 1000;
  const paid = S.filter(s => s.status === 'paid'), pend = S.filter(s => s.status === 'pending'), act = S.filter(s => s.last_seen && now - s.last_seen < 86400);
  $('#tdKpis').innerHTML = [[D.paid, paid.length], [D.pending, pend.length], [D.places, `${deskData.places.left}/${deskData.places.total}`], [D.active, act.length]].map(([k, v]) => `<div><b class="num">${v}</b><span>${k}</span></div>`).join('');
  $$('.fx-filter [data-f]').forEach(b => { b.onclick = () => { deskFilter = b.dataset.f; $$('.fx-filter [data-f]').forEach(x => x.setAttribute('aria-pressed', String(x === b))); drawDesk(); }; });
  drawDesk();
}
function drawDesk() {
  const D = STR.desk, now = Date.now() / 1000, host = $('#students');
  if (deskFilter === 'wait') { const W = deskData.waitlist; host.innerHTML = W.length ? `<ul class="fx-wl">${W.map(w => `<li><b>${esc(w.name || '—')}</b><a href="mailto:${esc(w.email)}">${esc(w.email)}</a><span>${esc(w.country || '')}</span></li>`).join('')}</ul>` : `<p class="muted">${D.none}</p>`; return; }
  const list = deskData.students.filter(s => deskFilter === 'paid' ? s.status === 'paid' : deskFilter === 'pending' ? s.status === 'pending' : !s.status || s.status === 'cancelled' || s.status === 'refunded');
  if (!list.length) { host.innerHTML = `<p class="muted">${D.none}</p>`; return; }
  host.innerHTML = list.map(s => {
    const app = s.progress && s.progress.app, x = (s.progress && s.progress.x) || {}, dd = x.daysDone || {}, nd = Object.keys(dd).filter(k => dd[k]).length;
    const seen = s.last_seen ? STR.ago(now - s.last_seen) : D.never, quiet = s.status === 'paid' && (!s.last_seen || now - s.last_seen > 2 * 86400);
    return `<article class="fx-st${quiet ? ' quiet' : ''}" data-id="${esc(s.id)}">
      <header><span class="nav-av">${esc((s.name || '?').charAt(0).toUpperCase())}</span><div><b>${esc(s.name)}</b><a href="mailto:${esc(s.email)}">${esc(s.email)}</a></div><span class="fx-pill ${esc(s.status || 'free')}">${s.status === 'paid' ? D.paid : s.status === 'pending' ? D.pending : D.free}</span></header>
      <dl><dt>${D.lastSeen}</dt><dd>${seen}</dd><dt>${D.from}</dt><dd>${esc(s.country || '—')}${s.source ? ' · ' + esc(s.source) : ''}</dd>${s.start_date ? `<dt>${D.start}</dt><dd>${dateLong(s.start_date)}</dd>` : ''}<dt>${D.practice}</dt><dd>${s.practice || 0} · ${app ? (app.xp || 0) + ' XP' : '—'}</dd>${s.status === 'paid' ? `<dt>${D.day}</dt><dd>${sprintDayNow(s.start_date)} · ${nd}/8 ✓</dd>` : ''}</dl>
      ${x.reasons ? `<p class="fx-reason">“${esc(x.reasons)}”</p>` : ''}
      <div class="row">${s.status !== 'paid' ? `<button class="key sm primary" data-act="paid">${D.markPaid}</button>` : `<button class="key sm" data-act="cancelled">${D.cancel}</button>`}<button class="key sm" data-act="reset">${D.reset}</button></div>
      <form class="fx-noteform"><label class="fx-f"><span>${D.note}</span><textarea name="body" rows="2" maxlength="1000"></textarea></label><button class="key sm primary" type="submit">${D.send}</button></form>
    </article>`;
  }).join('');
  $$('.fx-st', host).forEach(card => {
    const id = card.dataset.id;
    card.addEventListener('click', async e => { const b = e.target.closest('[data-act]'); if (!b) return; b.disabled = true;
      if (b.dataset.act === 'reset') { const r = await api('/api/tutor/reset-link', {userId: id}); if (r.ok) { const url = location.origin + r.data.path; try { await navigator.clipboard.writeText(url); toast(STR.desk.copied); } catch (x) { prompt(STR.desk.reset, url); } } b.disabled = false; return; }
      await api('/api/tutor/enrollment', {userId: id, status: b.dataset.act}); desk(); });
    card.querySelector('.fx-noteform').addEventListener('submit', async e => { e.preventDefault(); const t = e.target.body.value.trim(); if (!t) return; const r = await api('/api/tutor/note', {userId: id, body: t}); if (r.ok) { e.target.reset(); toast(STR.saved); } });
  });
}

/* ---------- the paid Sprint ---------- */
let SP = null, spDay = 0;
async function pageSprint() {
  const pl = plan();
  if (pl !== 'paid' && pl !== 'tutor') { $('#sprintPublic').hidden = false; $('#sprintApp').hidden = true; return; }
  $('#sprintPublic').hidden = true; $('#sprintApp').hidden = false;
  if (!SP) { const r = await fetch('/paid/sprint.' + LANG + '.json', {credentials: 'same-origin'}); if (!r.ok) { $('#sprintPublic').hidden = false; $('#sprintApp').hidden = true; return; } SP = await r.json(); }
  const e = ME.enrollment, now = sprintDayNow(e && e.start), u = user();
  $('#spHi').textContent = fill(STR.hiName, {name: u.name.split(' ')[0]}) + ' · ' + (now === 0 && e && e.start ? fill(STR.startsOn, {date: dateLong(e.start)}) : now >= 8 ? STR.finished : fill(STR.started, {n: now}));
  spDay = X.get('spDay', null); if (spDay == null) spDay = Math.min(7, Math.max(0, now));
  drawRing(now); drawTabs(now); drawDay(); drawLib();
}
function daysDone() { return X.get('daysDone', {}); }
function drawRing(now) {
  const dd = daysDone();
  $('#spRing').innerHTML = SP.days.map(d => `<li class="${dd[d.n] ? 'done' : ''}${d.n === now ? ' now' : ''}" title="${STR.dayN(d.n)}"><span>${dd[d.n] ? ic('check') : d.n}</span></li>`).join('');
}
function drawTabs(now) {
  const dd = daysDone();
  $('#spTabs').innerHTML = SP.days.map(d => `<button type="button" class="fx-tab${dd[d.n] ? ' done' : ''}" data-day="${d.n}" aria-pressed="${d.n === spDay}"><small>${STR.dayN(d.n)}${d.n === now ? ' · ' + STR.today : ''}</small><b>${esc(d.title)}</b></button>`).join('');
  $('#spTabs').onclick = e => { const b = e.target.closest('[data-day]'); if (!b) return; spDay = +b.dataset.day; X.set('spDay', spDay); drawTabs(now); drawDay(); $('#spDay').scrollIntoView({behavior: reduced ? 'auto' : 'smooth', block: 'start'}); };
}
function say(text) { try { speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(text); u.lang = 'en-US'; u.rate = .88; speechSynthesis.speak(u); } catch (e) {} }
function drawDay() {
  const d = SP.days.find(x => x.n === spDay) || SP.days[0], dd = daysDone(), host = $('#spDay');
  const phrase = p => `<li><button class="fx-say" type="button" data-say="${esc(p[0])}" aria-label="${STR.listen}: ${esc(p[0])}">${ic('sound')}</button><span><b lang="en">${esc(p[0])}</b><small>${esc(p[1])}</small></span></li>`;
  const reflections = X.get('reflect', {})[d.n] || {};
  let html = `<div class="fx-may-say"><img src="${MAYPIC}" alt="" width="80" height="80"><div><small>${STR.brief}</small><p>${esc(d.brief)}</p></div></div>`;
  if (d.n === 0) {
    const s0 = X.get('day0', {});
    html += `<p class="fx-why"><b>${STR.whyToday}.</b> ${esc(d.why)}</p><ol class="fx-checklist">${d.steps.map(st => `<li class="${s0[st.id] ? 'done' : ''}" data-s0="${st.id}"><span class="fx-tick">${ic('check')}</span><span>${esc(st.text)}</span>${st.id === 'reasons' ? '' : `<button type="button" class="key sm" data-s0go="${st.id}">${STR.step[st.id]}</button>`}</li>`).join('')}</ol>
      <label class="fx-f fx-reasons"><span>${STR.step.reasons}</span><textarea id="reasons" rows="3" placeholder="${STR.reasonsPh}">${esc(X.get('reasons', ''))}</textarea></label>`;
  } else {
    html += `<div class="fx-goal"><b class="kline" lang="en">${esc(d.can)}</b><p>${esc(d.goal)}</p></div>
      <p class="fx-why"><b>${STR.whyToday}.</b> ${esc(d.why)}</p>
      <div class="fx-cols"><section><h3>${STR.phrases}</h3><ul class="fx-phrases">${d.phrases.map(phrase).join('')}</ul></section>
      <section><h3>${STR.freeze}</h3><ul class="fx-phrases fx-rescue">${d.freeze.map(phrase).join('')}</ul>
        <h3>${STR.mistake}</h3><div class="fx-mis"><p><s lang="en">${esc(d.mistake.bad)}</s></p><p><b lang="en">${esc(d.mistake.good)}</b></p><p class="small">${esc(d.mistakeWhy)}</p></div></section></div>
      <h3>${STR.practise}</h3><div class="fx-go"><a class="key" href="${P.games}" data-go='${JSON.stringify({game: d.go.game, day: d.n - 1})}'>${STR.go.game}</a><a class="key" href="${P.speak}" data-go='${JSON.stringify({mission: d.go.scene})}'>${STR.go.scene}</a><a class="key" href="${P.shadow}" data-go='${JSON.stringify({clip: d.go.clip})}'>${STR.go.clip}</a></div>`;
  }
  html += `<div class="fx-chal">${ic('star')}<div><small>${STR.challenge}</small><p>${esc(d.challenge)}</p></div></div>`;
  if (d.n > 0) html += `<section class="fx-reflect"><h3>${STR.reflect}</h3>${SP.reflect.map((q, i) => `<label class="fx-f"><span>${esc(q)}</span>${i === 1 ? `<div class="fx-scale" role="radiogroup">${[1, 2, 3, 4, 5].map(v => `<button type="button" role="radio" aria-checked="${reflections[i] == v}" data-r="${i}" data-v="${v}">${v}</button>`).join('')}</div>` : `<input data-r="${i}" value="${esc(reflections[i] || '')}">`}</label>`).join('')}</section>`;
  html += `<div class="fx-done-row">${dd[d.n] ? `<p class="fx-done-msg">${ic('check')}${STR.dayDone}</p><button type="button" class="fx-link" data-undone>${STR.reopen}</button>` : `<button type="button" class="key hl big" data-done>${STR.markDone}</button>`}</div>`;
  host.innerHTML = html;
  host.onclick = e => {
    const sb = e.target.closest('[data-say]'); if (sb) { say(sb.dataset.say); return; }
    if (e.target.closest('[data-done]')) { const x = daysDone(); x[d.n] = true; X.set('daysDone', x); confetti(); if (!reduced) chime(); toast(STR.dayDone); const now = sprintDayNow(ME.enrollment && ME.enrollment.start); drawRing(now); drawTabs(now); drawDay(); sync(); return; }
    if (e.target.closest('[data-undone]')) { const x = daysDone(); delete x[d.n]; X.set('daysDone', x); drawDay(); return; }
    const r = e.target.closest('[data-r][data-v]'); if (r) { const all = X.get('reflect', {}); all[d.n] = all[d.n] || {}; all[d.n][r.dataset.r] = +r.dataset.v; X.set('reflect', all); drawDay(); return; }
    const g = e.target.closest('[data-s0go]'); if (g) { const id = g.dataset.s0go, T = ME.tutor || {}; if (id === 'book' && T.booking) open(T.booking, '_blank', 'noopener'); if (id === 'whatsapp' && T.whatsapp) open(T.whatsapp, '_blank', 'noopener'); if (id === 'calendar') downloadIcs(); if (id === 'record') { const c = $('#clipsPanel'); if (c) c.scrollIntoView({behavior: reduced ? 'auto' : 'smooth'}); } const s0 = X.get('day0', {}); s0[id] = true; X.set('day0', s0); setTimeout(drawDay, 200); }
  };
  host.oninput = e => { const r = e.target.closest('input[data-r]'); if (r) { const all = X.get('reflect', {}); all[d.n] = all[d.n] || {}; all[d.n][r.dataset.r] = r.value.slice(0, 200); X.set('reflect', all); } if (e.target.id === 'reasons') { X.set('reasons', e.target.value.slice(0, 400)); const s0 = X.get('day0', {}); if (e.target.value.trim().length > 10 && !s0.reasons) { s0.reasons = true; X.set('day0', s0); } } };
}
function drawLib() {
  $('#libList').innerHTML = SP.library.map(r => `<details class="fx-res"><summary>${ic(r.icon === 'sound' ? 'sound' : r.icon === 'chat' ? 'chat' : r.icon === 'calendar' ? 'calendar' : r.icon === 'warn' ? 'warn' : r.icon === 'user' ? 'user' : 'life')}<span><b>${esc(r.title)}</b><small>${esc(r.desc)}</small></span></summary><div class="fx-res-b">
    ${r.link ? `<a class="key" href="${P[r.link]}">${STR.seePage}</a>` : ''}
    ${(r.groups || []).map(g => `<h4>${esc(g.h)}</h4><ul class="fx-phrases">${g.items.map(p => `<li><button class="fx-say" type="button" data-say="${esc(p[0])}" aria-label="${STR.listen}">${ic('sound')}</button><span><b lang="en">${esc(p[0])}</b><small>${esc(p[1])}</small></span></li>`).join('')}</ul>`).join('')}
    ${(r.tips || []).map(tp => `<div class="fx-tip"><h4>${esc(tp.h)}</h4><p>${esc(tp.p)}</p>${tp.ex.length ? `<p class="fx-ex">${tp.ex.map(x => `<button type="button" class="chip" data-say="${esc(x.split(' / ')[0])}" lang="en">${esc(x)}</button>`).join('')}</p>` : ''}</div>`).join('')}
    ${r.template ? `<ul class="fx-phrases">${r.template.map(p => `<li><button class="fx-say" type="button" data-say="${esc(p[0].replace(/_+/g, ''))}" aria-label="${STR.listen}">${ic('sound')}</button><span><b lang="en">${esc(p[0])}</b><small>${esc(p[1])}</small></span></li>`).join('')}</ul>` : ''}
  </div></details>`).join('');
  $('#libList').onclick = e => { const b = e.target.closest('[data-say]'); if (b) say(b.dataset.say); };
}

/* ---------- the pages ---------- */
function route() {
  usageBadge();
  if (PAGE === 'join') pageJoin();
  else if (PAGE === 'thanks') { if (LANG === 'es' && user() && user().lang === 'en') { location.replace(SLUGS.en.thanks + location.search); return; } pageThanks(); }
  else if (PAGE === 'account') pageAccount();
  else if (PAGE === 'tutor') pageTutor();
  else if (PAGE === 'sprint') pageSprint();
}
(async function start() {
  await refresh(); paintNav(); route(); nudge();
  if (user()) restoreProgress();
  window.W2SAccount = {refresh, plan, leftOf, me: () => ME};
})();
})();
