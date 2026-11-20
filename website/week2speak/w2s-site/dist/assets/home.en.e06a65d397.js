(() => {
'use strict';
const NULL_EL = new Proxy(() => {}, {get: (t, k) => k === Symbol.toPrimitive ? (() => '') : (k === Symbol.iterator || k === 'then') ? undefined : k === 'length' ? 0 : (k === 'toString' || k === 'valueOf') ? (() => '') : NULL_EL, set: () => true, apply: () => NULL_EL, has: () => false});
const $ = (s, r = document) => (!r || r === NULL_EL) ? NULL_EL : (r.querySelector(s) || NULL_EL);
const $$ = (s, r = document) => (!r || r === NULL_EL) ? [] : Array.from(r.querySelectorAll(s));
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const reduced = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
const gs = window.gsap || null, ST = window.ScrollTrigger || null;
if (gs && ST) gs.registerPlugin(ST);
const live = !!gs && !reduced;
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const W = window.W2S;
const onHome = (document.body.dataset.page || 'home') === 'home';
const PLAY = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5l11 7-11 7z"/></svg>';
const PAUSE = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>';

/* ---------- headings: every heading is a line waiting to be spoken ---------- */
$$('[data-split]').forEach(h => { const t = h.textContent.trim(); h.setAttribute('aria-label', t); h.innerHTML = t.split(/\s+/).map(w => `<span class="w" aria-hidden="true">${esc(w)}</span>`).join(' '); });
function sweep(words, step = 70, hold = 260) { words.forEach((w, i) => { setTimeout(() => w.classList.add('on'), i * step); setTimeout(() => w.classList.remove('on'), i * step + hold); }); }
if (!reduced && 'IntersectionObserver' in window) {
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { sweep($$('.w', e.target)); io.unobserve(e.target); } }), {threshold: .6});
  $$('[data-split]').forEach(h => io.observe(h));
}


/* ---------- moving between rooms ---------- */
const onView = d => {
  const name = d.name, changed = d.changed;
  if (name === 'home') { $$('.ac').forEach(x => x.setAttribute('aria-pressed', x.dataset.acc === W.accent())); if (ST) requestAnimationFrame(() => ST.refresh()); return; }
  if (!live || !changed) return;
  const v = $('[data-view="' + name + '"]'); if (!v) return;
  gs.fromTo($$('.vh > *, .panel, details.day, .mod, .seg', v).slice(0, 26), {y: 28, opacity: 0}, {y: 0, opacity: 1, duration: .55, ease: 'expo.out', stagger: .035, clearProps: 'transform,opacity', overwrite: true});
};
document.addEventListener('w2s:view', e => onView(e.detail));
onView({name: document.body.dataset.page || 'home', changed: true});

/* ---------- nav: smooth jumps and a highlighter that tracks the scroll ---------- */
document.addEventListener('click', e => { const a = e.target.closest('[data-jump]'); if (!a) return; e.preventDefault(); const t = document.getElementById(a.dataset.jump); if (t && t.offsetParent !== null) window.scrollTo({top: t.getBoundingClientRect().top + window.scrollY - ($('.nav').offsetHeight - 2), behavior: reduced ? 'auto' : 'smooth'}); });
const prog = $('#progress');
const onScroll = () => { const max = document.documentElement.scrollHeight - innerHeight; prog.style.transform = 'scaleX(' + (max > 0 ? clamp(window.scrollY / max, 0, 1) : 0) + ')'; };
window.addEventListener('scroll', onScroll, {passive: true}); onScroll();
if (!onHome) return;

/* ---------- hero: karaoke headline, live waveform, flipping bubbles, marquee ---------- */
const heroWords = $$('#heroLine .w'); let pulse = 0;
if (!reduced && onHome) { let i = -1; (function next() { heroWords.forEach(w => w.classList.remove('on')); i++; if (i >= heroWords.length) { i = -1; setTimeout(next, 1500); return; } heroWords[i].classList.add('on'); pulse = 1; setTimeout(next, 430); })(); }
else heroWords[0].classList.add('on');
if (live) {
  gs.from(heroWords, {yPercent: 110, rotate: 8, opacity: 0, duration: .9, ease: 'expo.out', stagger: .07, clearProps: 'transform,opacity'});
  gs.from('.lede, .hero .row', {y: 24, opacity: 0, duration: .8, ease: 'expo.out', delay: .35, stagger: .1});
  gs.from('.flip', {scale: .4, opacity: 0, y: 40, duration: .8, ease: 'back.out(1.7)', delay: .5, stagger: .12});
}
const flips = $$('.flip'); let flipI = 0;
flips.forEach(f => f.addEventListener('click', () => f.classList.toggle('fixed')));
if (!reduced && onHome) setInterval(() => { if (flipI < flips.length) flips[flipI++].classList.add('fixed'); else if (flipI++ > flips.length + 1) { flips.forEach(f => f.classList.remove('fixed')); flipI = 0; } }, 1500);
else flips.forEach(f => f.classList.add('fixed'));
const STAR = '<svg viewBox="0 0 24 24"><path d="M12 1l2.6 7.4L22 11l-7.4 2.6L12 21l-2.6-7.4L2 11l7.4-2.6z"/></svg>';
const LINES = ["I'd like a coffee, please.", 'Where is gate 12?', "I'm twenty-five years old.", 'It depends on the price.', 'Nice to meet you.', 'Could I have a window seat?', 'I agree.', 'What time does the shop open?'];
$('#mq').innerHTML = (LINES.map(l => `<span>${esc(l)}</span>${STAR}`).join('')).repeat(2);
const cv = $('#wave'), cx = cv.getContext('2d'); let px = -999, heroOn = true;
function drawWave(t) {
  const dpr = Math.min(2, devicePixelRatio || 1), w = cv.clientWidth, h = cv.clientHeight;
  if (cv.width !== Math.round(w * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
  cx.setTransform(dpr, 0, 0, dpr, 0, 0); cx.clearRect(0, 0, w, h);
  const gap = 14, n = Math.ceil(w / gap);
  for (let i = 0; i < n; i++) {
    const x = i * gap + 3, base = (Math.sin(i * .35 + t * 1.7) + Math.sin(i * .13 - t * 1.1) + 2) / 4;
    const near = Math.exp(-((x - px) ** 2) / (2 * 130 * 130));
    const bh = Math.max(6, (0.16 + 0.5 * base) * (0.32 + pulse * 0.45 + near * 1.15) * h * 0.62);
    cx.fillStyle = near > .3 ? '#FFD93B' : 'rgba(255,255,255,.17)';
    cx.beginPath(); if (cx.roundRect) cx.roundRect(x, h - bh, 8, bh, 4); else cx.rect(x, h - bh, 8, bh); cx.fill();
  }
  pulse *= 0.93;
}
if (!reduced && onHome) { (function loop(ts) { if (heroOn) drawWave(ts / 1000); requestAnimationFrame(loop); })(0); if ('IntersectionObserver' in window) new IntersectionObserver(es => { heroOn = es[0].isIntersecting; }).observe($('#hero')); }
else drawWave(1.2);
$('#hero').addEventListener('pointermove', e => { px = e.clientX; if (live) { const rx = e.clientX / innerWidth - .5, ry = e.clientY / innerHeight - .5; flips.forEach((f, i) => gs.to(f, {x: rx * (14 + i * 9), y: ry * (10 + i * 6), duration: .6, ease: 'power2.out', overwrite: 'auto'})); } });
$('#hero').addEventListener('pointerleave', () => { px = -999; });

/* ---------- magnetic keys ---------- */
if (live && matchMedia('(hover:hover)').matches) $$('[data-magnet]').forEach(k => {
  k.addEventListener('pointermove', e => { const r = k.getBoundingClientRect(); gs.to(k, {x: (e.clientX - r.left - r.width / 2) * .25, y: (e.clientY - r.top - r.height / 2) * .35, duration: .3, ease: 'power2.out'}); });
  k.addEventListener('pointerleave', () => gs.to(k, {x: 0, y: 0, duration: .7, ease: 'elastic.out(1,.4)'}));
});

/* ---------- unlearn: the worksheet leaves, the voice arrives ---------- */
$('#eq').innerHTML = Array.from({length: 28}, (_, i) => `<i style="animation-delay:${(-i * .137 % 1).toFixed(2)}s"></i>`).join('');
const vkWords = $$('#vk .w'), stepEls = $$('#steps li'), countEl = $('#count');
if (live && ST) {
  const mm = gs.matchMedia();
  mm.add('(min-width: 900px)', () => {
    const tl = gs.timeline({scrollTrigger: {trigger: '#unlearn', start: 'top 58px', end: '+=140%', pin: true, scrub: .6, onUpdate: s => {
      const p = s.progress; countEl.textContent = Math.round(p * 12);
      stepEls.forEach((li, i) => li.classList.toggle('on', p > [.12, .45, .78][i]));
      const k = Math.floor(p * 3 * vkWords.length) % vkWords.length; vkWords.forEach((w, i) => w.classList.toggle('on', p > .2 && p < .98 && i === k));
    }}});
    tl.fromTo('#sheet', {x: 0, y: 0, rotate: -2, scale: 1, opacity: 1}, {x: -70, y: -30, rotate: -13, scale: .82, opacity: .35, ease: 'none', duration: 1}, 0)
      .fromTo('#strike', {scaleX: 0}, {scaleX: 1, ease: 'none', duration: .35}, .05)
      .fromTo('#voice', {yPercent: 70, opacity: 0, rotate: 7}, {yPercent: 0, opacity: 1, rotate: 0, ease: 'none', duration: .7}, .2);
    return () => { stepEls.forEach(li => li.classList.add('on')); countEl.textContent = '12'; };
  });
}

/* ---------- films ---------- */
const fPlay = $('#fPlay'), fSeek = $('#fSeek'), fTime = $('#fTime'), fCap = $('#fCap'), vid = $('#recVid');
const CAPS = {
  speak: 'Speech Mode. You answer out loud, a mistake that comes from Spanish gets a one-line fix, and if you freeze, Help me gives you a way to start.',
  order: 'Word Order. Build the sentence from tiles, then say it. Each correct sentence raises the combo.',
  shadow: 'Shadowing. Listen, speak along, then go solo. The score counts how many words came through clearly.',
  rec: 'A screen recording of the test app, captured in a browser. No sound.'
};
const F = {active: 'speak', playing: false, inView: false, tls: {}, drag: false, fresh: false};
const fmt = s => Math.floor(s / 60) + ':' + String(Math.floor(s % 60)).padStart(2, '0');
function buildSpeak() {
  const items = $$('.film[data-film="speak"] [data-s]'), hint = $('#faHint'), ring = $('#faRing'), xp = $('#faXp');
  const tl = gs.timeline({paused: true, repeat: -1, repeatDelay: 1.2});
  tl.set(items, {autoAlpha: 0, y: 14, scale: .96}).set(hint, {autoAlpha: 0, x: 30}).set(xp, {textContent: 0}).set(ring, {scale: 1, opacity: 0});
  const pop = (el, t) => tl.to(el, {autoAlpha: 1, y: 0, scale: 1, duration: .4, ease: 'back.out(1.8)'}, t);
  const speak = t => tl.fromTo(ring, {scale: 1, opacity: .7}, {scale: 1.9, opacity: 0, duration: .55, repeat: 1, ease: 'power1.out'}, t);
  pop(items[0], .3); speak(1.2); pop(items[1], 2.3);
  tl.to(xp, {textContent: 10, snap: {textContent: 1}, duration: .4}, 2.5);
  pop(items[2], 3.2); pop(items[3], 4.6);
  tl.to(hint, {autoAlpha: 1, x: 0, duration: .5, ease: 'expo.out'}, 5.5).from($$('.fchips i', hint), {scale: 0, duration: .3, ease: 'back.out(2)', stagger: .08}, 5.8);
  speak(6.6); pop(items[4], 7.7);
  tl.to(xp, {textContent: 20, snap: {textContent: 1}, duration: .4}, 7.9).to({}, {duration: 1.4});
  return tl;
}
const ORDER = ['Where', 'is', 'the', 'bus', 'station?'], POOL = [4, 0, 2, 1, 3];
$('#fbTray').innerHTML = ORDER.map(w => `<span class="ft">${w}</span>`).join('');
$('#fbPool').innerHTML = POOL.map(i => `<span class="ft" data-i="${i}">${ORDER[i]}</span>`).join('');
$('#fbBurst').innerHTML = Array.from({length: 18}, (_, i) => `<i style="background:${['#FFD93B', '#2D4BFF', '#E0245E', '#19C79C'][i % 4]}"></i>`).join('');
function buildOrder() {
  const tiles = $$('#fbPool .ft'), slots = $$('#fbTray .ft'), res = $('#fbRes'), combo = $('#fbCombo'), dots = $$('#fbBurst i');
  gs.set(tiles, {clearProps: 'all'});
  const w = $('#screen').clientWidth;
  const tl = gs.timeline({paused: true, repeat: -1, repeatDelay: 1.2});
  tl.set(res, {autoAlpha: 0, y: 12}).set(combo, {textContent: 0}).set(dots, {x: 0, y: 0, opacity: 0, scale: 0});
  ORDER.forEach((_, i) => {
    const tile = tiles.find(t => +t.dataset.i === i), a = tile.getBoundingClientRect(), b = slots[i].getBoundingClientRect();
    tl.to(tile, {x: b.left - a.left, y: b.top - a.top, duration: .5, ease: 'back.out(1.3)'}, .7 + i * .6);
  });
  tl.to(tiles, {backgroundColor: '#DDF6EE', color: '#087F63', boxShadow: '0 .28em 0 #19C79C', duration: .2, stagger: .05}, 3.9)
    .to(res, {autoAlpha: 1, y: 0, duration: .35, ease: 'expo.out'}, 4.1)
    .to(combo, {textContent: 1, snap: {textContent: 1}, duration: .2}, 4.1)
    .to(dots, {x: i => Math.cos(i * 2.4) * w * (.12 + (i % 5) * .035), y: i => Math.sin(i * 2.4) * w * (.09 + (i % 4) * .03) - w * .04, rotate: i => i * 70, scale: 1, opacity: 1, duration: .45, ease: 'power3.out'}, 3.95)
    .to(dots, {y: '+=' + w * .12, opacity: 0, duration: .7, ease: 'power1.in'}, 4.4)
    .to({}, {duration: 1.6});
  return tl;
}
const SH = 'Could I have a window seat, please?'.split(' ');
$('#fcLine').innerHTML = SH.map(w => `<span class="fw">${w}</span>`).join(' ');
$$('.f-wave').forEach(wv => wv.insertAdjacentHTML('beforeend', Array.from({length: 34}, (_, i) => `<i style="animation-delay:${(-i * .173 % .7).toFixed(2)}s"></i>`).join('')));
function buildShadow() {
  const words = $$('#fcLine .fw'), modes = $$('#fcModes i'), w1 = $('#fcW1'), w2 = $('#fcW2'), bar = $('#fcBar'), pct = $('#fcPct');
  const PASS = [[.5, 3.1], [3.7, 6.3], [6.9, 9.5]], state = {t: 0};
  const render = () => {
    const t = state.t; let pass = -1, idx = -1;
    PASS.forEach(([a, b], i) => { if (t >= a && t < b) { pass = i; idx = Math.min(words.length - 1, Math.floor((t - a) / ((b - a) / words.length))); } });
    const mode = t < PASS[1][0] - .3 ? 0 : t < PASS[2][0] - .3 ? 1 : 2, done = t >= 9.7, p = clamp((t - 9.7) / .9, 0, 1);
    modes.forEach((m, i) => m.classList.toggle('on', i === mode));
    words.forEach((el, i) => { el.classList.toggle('on', i === idx); el.classList.toggle('hit', done && i !== 4); el.classList.toggle('miss', done && i === 4); });
    w1.dataset.play = pass === 0 || pass === 1 ? '1' : '0'; w2.dataset.play = pass === 1 || pass === 2 ? '1' : '0';
    bar.style.width = (p * 86) + '%'; pct.textContent = Math.round(p * 6) + ' of 7';
  };
  const tl = gs.timeline({paused: true, repeat: -1, repeatDelay: 1});
  tl.to(state, {t: 11.6, duration: 11.6, ease: 'none', onUpdate: render});
  return tl;
}
const BUILD = {speak: buildSpeak, order: buildOrder, shadow: buildShadow};
function ctl() {
  if (F.active === 'rec') return {dur: () => vid.duration || 0, get: () => (vid.duration ? vid.currentTime / vid.duration : 0), set: p => { if (vid.duration) vid.currentTime = p * vid.duration; }, play: () => { const r = vid.play(); if (r && r.catch) r.catch(() => {}); }, pause: () => vid.pause()};
  const tl = F.tls[F.active];
  if (!tl) return {dur: () => 0, get: () => 0, set() {}, play() {}, pause() {}};
  return {dur: () => tl.duration(), get: () => tl.progress(), set: p => tl.progress(p), play: () => tl.play(), pause: () => tl.pause()};
}
function setPlaying(on) { F.playing = on; const c = ctl(); if (on && F.fresh && F.tls[F.active] && F.active !== 'rec') { F.fresh = false; F.tls[F.active].restart(); } else if (on) c.play(); else c.pause(); fPlay.innerHTML = on ? PAUSE : PLAY; fPlay.setAttribute('aria-label', on ? 'Pause film' : 'Play film'); }
function showFilm(id) {
  ctl().pause(); F.active = id;
  $$('.film').forEach(f => { f.hidden = f.dataset.film !== id; });
  $$('#ftabs button').forEach(b => b.setAttribute('aria-selected', b.dataset.film === id));
  fCap.textContent = CAPS[id]; const tr = {speak: ['/en/speech-mode/', 'Try Speech Mode'], order: ['/en/games/', 'Play Word Order'], shadow: ['/en/shadowing/', 'Open the shadowing studio'], rec: ['/en/7-day-sprint/', 'Start the 7-Day Sprint']}[id]; $('#fTry').setAttribute('href', tr[0]); $('#fTry').textContent = tr[1];
  if (gs && BUILD[id]) { if (F.tls[id]) F.tls[id].kill(); F.tls[id] = BUILD[id](); F.tls[id].time(F.tls[id].duration() - .05); F.fresh = true; }
  if (id === 'rec') vid.currentTime = 0;
  $('#fctl').hidden = id !== 'rec' && !gs;
  setPlaying(F.inView && !reduced);
  tickUI();
}
function tickUI() { const c = ctl(), p = c.get(); if (!F.drag) fSeek.value = Math.round(p * 1000); fTime.textContent = fmt(p * c.dur()) + ' / ' + fmt(c.dur()); }
$('#ftabs').addEventListener('click', e => { const b = e.target.closest('[data-film]'); if (b) showFilm(b.dataset.film); });
fPlay.addEventListener('click', () => setPlaying(!F.playing));
fSeek.addEventListener('input', () => { F.drag = true; F.fresh = false; if (F.playing) setPlaying(false); ctl().set(fSeek.value / 1000); tickUI(); });
fSeek.addEventListener('change', () => { F.drag = false; });
if (gs) gs.ticker.add(() => { if (F.playing) tickUI(); }); else vid.addEventListener('timeupdate', tickUI);
vid.addEventListener('error', () => { const b = $('#ftabs [data-film="rec"]'); if (b) b.hidden = true; if (F.active === 'rec') showFilm('speak'); });
vid.addEventListener('loadedmetadata', tickUI);
if ('IntersectionObserver' in window) new IntersectionObserver(es => { F.inView = es[0].isIntersecting; if (!F.inView) setPlaying(false); else if (!reduced) setPlaying(true); }, {threshold: .35}).observe($('#screen'));
let rsT; window.addEventListener('resize', () => { clearTimeout(rsT); rsT = setTimeout(() => { if (gs && F.active === 'order') { const p = F.tls.order ? F.tls.order.progress() : 0; if (F.tls.order) F.tls.order.kill(); F.tls.order = buildOrder(); F.tls.order.progress(p); if (F.playing) F.tls.order.play(); } }, 250); });
if (live && matchMedia('(hover:hover)').matches) {
  const th = $('#theatre'), sc = $('#screen');
  th.addEventListener('pointermove', e => { const r = sc.getBoundingClientRect(); gs.to(sc, {rotateY: ((e.clientX - r.left) / r.width - .5) * 5, rotateX: -((e.clientY - r.top) / r.height - .5) * 4, duration: .5, ease: 'power2.out'}); });
  th.addEventListener('pointerleave', () => gs.to(sc, {rotateX: 0, rotateY: 0, duration: .8, ease: 'expo.out'}));
}
showFilm(gs ? 'speak' : 'rec');

/* ---------- playground 1: catch mistakes that come from Spanish ---------- */
const RULES = W.RULES;
const EXAMPLES = ['I have 25 years and I am agree with you', 'Is raining and people is late', 'I went to the shop for buy bread', 'It depends of the price', "I'd like a coffee, please"];
$('#cChips').innerHTML = EXAMPLES.map(x => `<button type="button" class="chip" data-ex="${esc(x)}">${esc(x)}</button>`).join('');
const cIn = $('#cIn'), cOut = $('#cOut'), cFix = $('#cFix'); let lastKey = '';
function catchIt() {
  const text = cIn.value; const hits = [];
  RULES.forEach(r => { const m = r.re.exec(text); if (m) { const lead = m[1] && /[.!?]/.test(m[1]) ? m[1].length : 0; hits.push({r, a: m.index + lead, b: m.index + m[0].length}); } });
  hits.sort((x, y) => x.a - y.a);
  let html = '', pos = 0; hits.forEach(h => { if (h.a < pos) return; html += esc(text.slice(pos, h.a)) + '<mark>' + esc(text.slice(h.a, h.b)) + '</mark>'; pos = h.b; });
  cOut.innerHTML = html + esc(text.slice(pos));
  const key = hits.map(h => h.r.name).join('|') + (text.trim() ? '' : '#empty');
  if (key === lastKey) return; lastKey = key;
  if (!text.trim()) cFix.innerHTML = '<div class="fixc"><b>Waiting for a sentence</b><span>Type one above, or tap an example.</span></div>';
  else if (!hits.length) cFix.innerHTML = '<div class="clean">Nothing caught. That sentence has none of the usual Spanish-speaker mistakes.</div>';
  else cFix.innerHTML = hits.map(h => `<div class="fixc"><b>${esc(h.r.name)}</b><span>${esc(h.r.tip)}</span><small>${esc(h.r.es)}</small></div>`).join('');
  if (live) gs.from(cFix.children, {y: 14, opacity: 0, scale: .96, duration: .4, ease: 'back.out(1.6)', stagger: .07});
}
cIn.addEventListener('input', catchIt);
$('#cChips').addEventListener('click', e => { const b = e.target.closest('[data-ex]'); if (!b) return; cIn.value = b.dataset.ex; catchIt(); });
catchIt();

/* ---------- playground 2: word order ---------- */
const GS = ["Hi, I'm Ana.", "I'm from Colombia.", "I'm thirty years old.", 'Nice to meet you.'];
const gTray = $('#gTray'), gPool = $('#gPool'), gMsg = $('#gMsg'), gDots = $('#gDots'); const GM = {i: 0, toks: [], busy: false};
const shuffle = a => { const r = a.slice(); for (let i = r.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; } return r; };
function gDotsDraw() { gDots.innerHTML = GS.map((_, k) => `<i class="${k < GM.i ? 'd' : k === GM.i ? 'c' : ''}"></i>`).join(''); }
function gLoad() {
  GM.busy = false; gTray.classList.remove('ok'); gTray.innerHTML = ''; gMsg.textContent = ''; gMsg.className = 'gmsg'; gDotsDraw(); gAct.innerHTML = '';
  if (GM.i >= GS.length) { gPool.innerHTML = ''; gMsg.textContent = 'You can introduce yourself in four sentences. Day 1 has eight more.'; gMsg.className = 'gmsg ok done';
    gAct.innerHTML = '<a class="key hl big" href="' + W.path('games') + '" data-go=\'{"game":"order","day":0}\'>' + 'Play the Day 1 round' + '</a><a class="key" href="' + W.path('speak') + '" data-go=\'{"mission":"cafe"}\'>' + 'Order a coffee with a Buddy' + '</a><button type="button" class="key ghost" id="gAgain">Play again</button>';
    W.track && W.track('round_complete', {mode: 'home:order'}); W.burst(gMsg); return; }
  GM.toks = GS[GM.i].replace(/[.,?!]/g, '').split(' ');
  let p; do { p = shuffle(GM.toks.map((_, k) => k)); } while (p.every((v, k) => v === k));
  gPool.innerHTML = p.map(k => `<button type="button" class="tile" data-k="${k}">${esc(GM.toks[k])}</button>`).join('');
  if (live) gs.from(gPool.children, {y: 20, opacity: 0, scale: .7, duration: .4, ease: 'back.out(2)', stagger: .05});
}
function flipTo(tile, parent) {
  const a = tile.getBoundingClientRect(); parent.appendChild(tile); const b = tile.getBoundingClientRect();
  if (live) gs.fromTo(tile, {x: a.left - b.left, y: a.top - b.top}, {x: 0, y: 0, duration: .38, ease: 'back.out(1.5)', overwrite: true});
}
function gClick(e) {
  if (e.target.id === 'gAgain') { GM.i = 0; gLoad(); return; }
  const t = e.target.closest('.tile'); if (!t || GM.busy) return; if (W.track && !GM.started) { GM.started = true; W.track('practice_start', {mode: 'home:order'}); }
  flipTo(t, t.parentElement === gPool ? gTray : gPool); gMsg.textContent = ''; gMsg.className = 'gmsg';
  if (gPool.children.length) return;
  const built = $$('.tile', gTray).map(x => x.textContent).join(' ').toLowerCase();
  if (built === GM.toks.join(' ').toLowerCase()) {
    GM.busy = true; gTray.classList.add('ok'); gMsg.innerHTML = '<b lang="en">' + esc(GS[GM.i]) + '</b> ' + esc('Now say it out loud.'); gMsg.className = 'gmsg ok'; W.Voice.speak(GS[GM.i], {rate: .95}); W.addXP(10); W.logLine('Home: Word Order', GS[GM.i]);
    W.track && W.track('feedback', {mode: 'home:order', result: 'right'});
    if (live) gs.fromTo(gTray.children, {y: 0}, {y: -6, duration: .12, ease: 'power2.out', yoyo: true, repeat: 1});
    gAct.innerHTML = '<button type="button" class="key" id="gHear">' + W.ic('speaker') + 'Hear it' + '</button><button type="button" class="key primary" id="gNext">' + (GM.i + 1 < GS.length ? 'Next sentence' : 'See how you did') + W.ic('arrow') + '</button>';
    const nx = document.getElementById('gNext'); if (nx) nx.focus({preventScroll: true});
  } else {
    gMsg.textContent = 'Not yet. It starts with "' + GM.toks.slice(0, 2).join(' ') + '". Tap a word to take it back.'; gMsg.className = 'gmsg no'; W.track && W.track('feedback', {mode: 'home:order', result: 'retry'});
    if (live) gs.fromTo(gTray, {x: -8}, {x: 0, duration: .5, ease: 'elastic.out(1.2,.25)'});
  }
}
const gAct = $('#gAct');
gAct.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return;
  if (b.id === 'gHear') W.Voice.speak(GS[GM.i], {rate: .9});
  else if (b.id === 'gNext') { W.Voice.stop(); GM.i++; gLoad(); W.track && W.track('next', {mode: 'home:order'}); const f = gPool.querySelector('.tile'); if (f) f.focus({preventScroll: true}); }
  else if (b.id === 'gAgain') { GM.i = 0; gLoad(); } });
gTray.addEventListener('click', gClick); gPool.addEventListener('click', gClick); gLoad();

/* ---------- the week, sideways ---------- */
const DAYS = [
  ['First sentences', 'Introduce yourself out loud.', ['Shadow a self-introduction', 'Meet someone new', 'Word Order round']],
  ['Ordering and asking', 'Order a drink and food without help.', ['Fill the Gap round', 'Café order', 'Shadow "Ordering coffee"']],
  ['Questions', 'Ask what a traveller needs to ask.', ['Flash Translate round', 'Airport check-in', 'Shadow "At the airport"']],
  ['Your story', 'Keep small talk going for a minute.', ['Word Order, round two', 'Meet someone, no hints', 'Shadow "Small talk"']],
  ['Work English', 'Answer two interview questions.', ['Fill the Gap, round two', 'Job interview', 'Shadow an interview answer']],
  ['Thinking in English', 'Finish a scene without Help me.', ['Flash Translate, round two', 'Café order, no hints', 'Solo shadow at natural speed']],
  ['The 2-minute talk', 'Speak for two minutes, unscripted.', ['Plan three things to say', 'Give your talk', 'Compare with Day 1']]
];
$('#wkTrack').innerHTML = DAYS.map((d, i) => `<article class="dcard${i === 6 ? ' last' : ''}"><div class="n num">${i + 1}</div><h3>${esc(d[0])}</h3><p>${esc(d[1])}</p><ul>${d[2].map(t => `<li>${esc(t)}</li>`).join('')}</ul></article>`).join('');
if (live && ST) {
  const mm2 = gs.matchMedia();
  mm2.add('(min-width: 900px)', () => {
    const sec = $('#week'), track = $('#wkTrack'), bar = $('#wkBar'); sec.classList.add('pinned');
    const dist = () => Math.max(0, track.scrollWidth - document.documentElement.clientWidth);
    const tw = gs.to(track, {x: () => -dist(), ease: 'none', scrollTrigger: {trigger: sec, start: 'top 58px', end: () => '+=' + (dist() + 300), pin: true, scrub: .5, invalidateOnRefresh: true, onUpdate: s => { bar.style.transform = 'scaleX(' + s.progress + ')'; }}});
    gs.from('.dcard .n', {scale: .5, duration: .5, ease: 'back.out(2)', stagger: .06, scrollTrigger: {trigger: sec, start: 'top 70%'}});
    return () => { sec.classList.remove('pinned'); gs.set(track, {clearProps: 'transform'}); tw.kill(); };
  });
}

/* ---------- accents: the same line in the voice you choose ---------- */
const jack = '<rect width="28" height="20" fill="#012169"/><path d="M0 0l28 20M28 0L0 20" stroke="#fff" stroke-width="4"/><path d="M0 0l28 20M28 0L0 20" stroke="#C8102E" stroke-width="1.6"/><path d="M14 0v20M0 10h28" stroke="#fff" stroke-width="6"/><path d="M14 0v20M0 10h28" stroke="#C8102E" stroke-width="3.4"/>';
const stripes = Array.from({length: 7}, (_, i) => `<rect y="${(i * 2 * 20 / 13).toFixed(2)}" width="28" height="${(20 / 13).toFixed(2)}" fill="#B22234"/>`).join('');
const ACC = [
  {id:'us', name:'American', lang:'en-US', svg:`<rect width="28" height="20" fill="#fff"/>${stripes}<rect width="12" height="10.8" fill="#3C3B6E"/>`},
  {id:'gb', name:'British', lang:'en-GB', svg:jack},
  {id:'au', name:'Australian', lang:'en-AU', svg:`<rect width="28" height="20" fill="#012169"/><g transform="scale(.5)">${jack}</g><g fill="#fff"><circle cx="7" cy="15.5" r="1.7"/><circle cx="21" cy="4" r="1.1"/><circle cx="24.5" cy="8.5" r="1.1"/><circle cx="21" cy="16" r="1.1"/><circle cx="17.5" cy="9.5" r="1.1"/></g>`},
];
const AC_TEXT = 'Could I have a window seat, please?';
$('#acLine').innerHTML = AC_TEXT.split(' ').map(w => `<span class="w">${esc(w)}</span>`).join(' ');
$('#acRow').innerHTML = ACC.map(a => `<button type="button" class="ac" data-acc="${a.id}" aria-pressed="${a.id === W.accent()}"><svg viewBox="0 0 28 20" aria-hidden="true">${a.svg}</svg>${a.name}</button>`).join('');
const acWords = $$('#acLine .w');
$('#acRow').addEventListener('click', e => {
  const b = e.target.closest('[data-acc]'); if (!b) return; const a = ACC.find(x => x.id === b.dataset.acc);
  W.setAccent(a.id); $$('.ac').forEach(x => x.setAttribute('aria-pressed', x === b));
  if (live) gs.fromTo(b, {scale: .9}, {scale: 1, duration: .5, ease: 'elastic.out(1.2,.4)'});
  W.Voice.speak(AC_TEXT, {rate: .95, onWord: i => acWords.forEach((w, k) => w.classList.toggle('on', k === i))});
  $('#acNote').textContent = W.Voice.note() + ' The whole site now uses this accent.';
});
if (live && ST) gs.from('.ac', {y: 50, scale: .8, duration: .6, ease: 'back.out(1.8)', stagger: .07, scrollTrigger: {trigger: '#acRow', start: 'top 88%'}});
if (live && ST) {
  gs.from('.toy', {y: 60, rotate: i => (i ? 2 : -2), duration: .8, ease: 'expo.out', stagger: .12, scrollTrigger: {trigger: '.toys', start: 'top 85%'}});
  gs.from('.plan', {y: 50, duration: .7, ease: 'expo.out', stagger: .1, scrollTrigger: {trigger: '.pgrid', start: 'top 88%'}});
  gs.from('#screen', {scale: .86, y: 60, duration: 1, ease: 'expo.out', scrollTrigger: {trigger: '#theatre', start: 'top 92%'}});
  ST.create({onUpdate: s => { const v = clamp(s.getVelocity() / 300, -8, 8); gs.to('#mq', {skewX: -v, duration: .4, overwrite: 'auto'}); }});
  window.addEventListener('load', () => ST.refresh());
}
})();
