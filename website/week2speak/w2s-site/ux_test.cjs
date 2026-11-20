// Practice-loop checks (apply_ux.py): scoring once, stale captures, mic outcomes, recap, home sample, Continue, audio clips.
// Run with the site served on port 8765:  node ux_test.cjs [base]
// The browser's speech recognition is replaced by a scripted fake, so microphone paths run without a microphone.
const { chromium, devices } = require('playwright');
const BASE = process.argv[2] || 'http://127.0.0.1:8765';
const FAKE_SR = () => {
  window.__sr = {mode: 'ok', inst: []};
  class FakeSR {
    constructor() { window.__sr.inst.push(this); }
    start() { const m = window.__sr.mode; setTimeout(() => {
      if (m === 'deny') { this.onerror && this.onerror({error: 'not-allowed'}); this.onend && this.onend(); return; }
      if (m === 'nomic') { this.onerror && this.onerror({error: 'audio-capture'}); this.onend && this.onend(); return; }
      this.onstart && this.onstart();
      if (m === 'silence') setTimeout(() => { this.onerror && this.onerror({error: 'no-speech'}); this.onend && this.onend(); }, 40);
      if (m === 'network') setTimeout(() => { this.onerror && this.onerror({error: 'network'}); this.onend && this.onend(); }, 40);
    }, 10); }
    stop() { setTimeout(() => { this.onend && this.onend(); }, 30); }
    say(t) { const r = [{transcript: t}]; r.isFinal = true; this.onresult && this.onresult({resultIndex: 0, results: [r]}); }
  }
  window.SpeechRecognition = undefined; window.webkitSpeechRecognition = FakeSR;
};
const results = []; const ok = (name, cond, extra) => { results.push([name, !!cond]); console.log((cond ? 'ok  ' : 'FAIL') + ' ' + name + (extra ? '  ' + extra : '')); };
const xp = pg => pg.evaluate(() => { try { return JSON.parse(localStorage.getItem('w2s.v1')).xp; } catch (e) { return 0; } });
async function fresh(b, opts = {}) {
  const ctx = await b.newContext({...devices['iPhone 13'], locale: 'es-ES', ...opts});
  await ctx.addInitScript(FAKE_SR);
  if (opts.audio) await ctx.addInitScript(opts.audio);
  const pg = await ctx.newPage(); pg.errs = []; pg.on('pageerror', e => pg.errs.push(e.message)); return {ctx, pg};
}
const tapInOrder = async (pg, sentence, scope) => {
  const toks = sentence.replace(/[.,?!]/g, '').split(' ');
  for (const w of toks) { await pg.evaluate(([w, scope]) => { const t = [...document.querySelectorAll(scope + ' .tile:not(.gone):not([disabled])')].find(x => x.textContent === w && !x.closest('.tray')); t.click(); }, [w, scope]); }
};

(async () => {
  const b = await chromium.launch({args: ['--autoplay-policy=no-user-gesture-required']});

  // 1. Home: the hero leads to a finishable Day 1 sample, with a Next button, then one step on
  { const {ctx, pg} = await fresh(b);
    await pg.goto(BASE + '/'); await pg.waitForTimeout(600);
    const cta = await pg.locator('#hero a.key.hl').first(); ok('home: hero action is the sample', (await cta.textContent()).includes('Preséntate'));
    await cta.click(); await pg.waitForTimeout(900);
    const top = await pg.evaluate(() => document.getElementById('try').getBoundingClientRect().top);
    ok('home: action scrolls to the sample', Math.abs(top) < 120, 'top=' + Math.round(top));
    const GS = ["Hi, I'm Ana.", "I'm from Lima, in Peru.", "I'm thirty years old.", 'Nice to meet you.'];
    for (let i = 0; i < GS.length; i++) {
      await tapInOrder(pg, GS[i], '#try');
      await pg.waitForTimeout(300);
      ok('home: sentence ' + (i + 1) + ' right, model phrase shown', (await pg.textContent('#gMsg')).includes(GS[i]));
      await pg.waitForTimeout(2200);
      ok('home: no auto advance (waits for Next)', (await pg.textContent('#gMsg')).includes(GS[i]));
      await pg.click('#gNext');
    }
    const links = await pg.$$eval('#gAct a', as => as.map(a => a.getAttribute('href')));
    ok('home: continues into the Day 1 round and the café', links.includes('/juegos/') && links.includes('/modo-habla/'), links.join(' '));
    await pg.click('#gAct a[href="/juegos/"]'); await pg.waitForTimeout(900);
    ok('home → games: Day 1 Word Order opened', (await pg.textContent('#gameBody .gtop')).includes('Ordena') && await pg.evaluate(() => document.querySelector('#gameDays [aria-pressed="true"]').textContent.includes('1')));
    // Continue appears once there is progress
    await pg.goto(BASE + '/'); await pg.waitForTimeout(500);
    const res = await pg.evaluate(() => { const a = document.getElementById('resume'); return {hidden: a.hidden, href: a.getAttribute('href'), text: a.textContent}; });
    ok('home: Continue shows the next Sprint task', !res.hidden && /Continuar/.test(res.text) && res.href.startsWith('/'), JSON.stringify(res));
    ok('home: no page errors', !pg.errs.length, pg.errs.join('|'));
    await ctx.close(); }

  // 2. Word Order: fast taps keep every tile in order; a double Check scores once; Next is focused
  { const {ctx, pg} = await fresh(b);
    await pg.goto(BASE + '/juegos/'); await pg.waitForTimeout(700);
    const firstTop = await pg.evaluate(() => document.querySelector('#gameBody .pool .tile').getBoundingClientRect().bottom);
    ok('games: first question on the first phone screen', firstTop < innerHeightOf(), 'tile bottom=' + Math.round(firstTop));
    await tapInOrder(pg, "Hi, I'm Ana.", '#gameBody');
    const built = await pg.$$eval('#gameBody .tray .tile', t => t.map(x => x.textContent).join(' '));
    ok('games: rapid taps keep every tile, in order', built === "Hi I'm Ana", built);
    const x0 = await xp(pg);
    await pg.evaluate(() => { const c = document.querySelector('[data-check]'); c.click(); c.click(); });
    await pg.waitForTimeout(200);
    const x1 = await xp(pg);
    ok('games: double Check scores once', x1 - x0 === 10, 'gained ' + (x1 - x0));
    ok('games: model phrase in the feedback', (await pg.textContent('#gameBody .fb-say')) === "Hi, I'm Ana.");
    ok('games: Next has focus', await pg.evaluate(() => document.activeElement && document.activeElement.dataset.next === '1'));
    await ctx.close(); }

  // 3. Flash: typed answer + a late spoken result score once; a capture from a previous item is dropped
  { const {ctx, pg} = await fresh(b);
    await pg.goto(BASE + '/juegos/'); await pg.waitForTimeout(600);
    await pg.click('[data-game="flash"]'); await pg.waitForTimeout(300);
    await pg.click('#gameBody [data-say]'); await pg.waitForTimeout(80);
    await pg.fill('#flashInput', "Hi, I'm Ana."); const x0 = await xp(pg);
    await pg.evaluate(() => { const f = document.getElementById('flashForm'); f.requestSubmit(); f.requestSubmit(); });
    await pg.evaluate(() => { const r = window.__sr.inst.at(-1); r.say("Hi, I'm Ana."); r.onend && r.onend(); });
    await pg.waitForTimeout(250);
    const x1 = await xp(pg);
    ok('flash: typed + late spoken answer score once', x1 - x0 === 10, 'gained ' + (x1 - x0));
    await pg.click('[data-next]'); await pg.waitForTimeout(150);
    // start a capture on item 2, move to another day, then the old capture reports
    await pg.click('#gameBody [data-say]'); await pg.waitForTimeout(80);
    await pg.click('[data-gday="1"]'); await pg.waitForTimeout(150);
    const before = await pg.evaluate(() => [document.querySelector('#gameBody .fb').className, localStorage.getItem('w2s.v1')]);
    await pg.evaluate(() => { const r = window.__sr.inst.at(-1); r.say("I'd like a coffee, please."); });
    await pg.waitForTimeout(200);
    const after = await pg.evaluate(() => [document.querySelector('#gameBody .fb').className, localStorage.getItem('w2s.v1')]);
    ok('flash: a capture from before the switch is dropped', before[0] === after[0] && JSON.parse(before[1]).xp === JSON.parse(after[1]).xp, after[0]);
    await ctx.close(); }

  // 4. Microphone outcomes: blocked, silence, no microphone, recognition error. None counts as a miss.
  for (const [mode, re] of [['deny', /bloqueado/], ['silence', /No te oí/], ['nomic', /micrófono/], ['network', /no funcionó/]]) {
    const {ctx, pg} = await fresh(b);
    await pg.goto(BASE + '/juegos/'); await pg.waitForTimeout(500);
    await pg.click('[data-game="flash"]'); await pg.waitForTimeout(200);
    await pg.evaluate(m => { window.__sr.mode = m; }, mode);
    await pg.click('#gameBody [data-say]'); await pg.waitForTimeout(350);
    const fb = await pg.evaluate(() => { const f = document.querySelector('#gameBody .fb'); return {cls: f.className, text: f.textContent, marks: document.querySelectorAll('#gameBody .prog i.m').length}; });
    ok('mic ' + mode + ': own message, not a miss', re.test(fb.text) && !/bad/.test(fb.cls) && fb.marks === 0, fb.text.slice(0, 70));
    if (mode === 'deny') ok('mic deny: typing stays available', await pg.evaluate(() => !document.getElementById('flashInput').disabled && document.activeElement && document.activeElement.id === 'flashInput'));
    await ctx.close();
  }

  // 5. Round end: recap of every phrase, a review of the misses, the round bonus paid once
  { const {ctx, pg} = await fresh(b);
    await pg.goto(BASE + '/juegos/'); await pg.waitForTimeout(500);
    await pg.click('[data-game="gap"]'); await pg.waitForTimeout(200);
    for (let i = 0; i < 8; i++) {
      // miss the first two (pick a wrong option), get the rest right
      await pg.evaluate(i => { const it = [...document.querySelectorAll('#gameBody [data-opt]')]; const ans = window.__gapAns = window.__gapAns || null; return it.length; }, i);
      const pick = await pg.evaluate(i => { const opts = [...document.querySelectorAll('#gameBody [data-opt]')].map(b => b.dataset.opt); return opts; }, i);
      if (i < 2) { await pg.click(`#gameBody [data-opt="${pick[0]}"]`); if (!(await pg.$('[data-next]'))) await pg.click(`#gameBody [data-opt="${pick[1]}"]`); }
      else { for (const o of pick) { if (await pg.$('[data-next]')) break; await pg.click(`#gameBody [data-opt="${o}"]`); } }
      await pg.waitForTimeout(60); await pg.click('[data-next]');
    }
    const recap = await pg.evaluate(() => ({h: document.querySelector('.recap-h') && document.querySelector('.recap-h').textContent, rows: document.querySelectorAll('.recap-list li').length, miss: document.querySelectorAll('.recap-list li.miss').length, retry: !!document.querySelector('[data-retry]')}));
    ok('recap: every phrase listed, misses marked, review offered', recap.rows === 8 && recap.miss >= 1 && recap.retry, JSON.stringify(recap));
    const x0 = await xp(pg);
    await pg.click('[data-retry]'); await pg.waitForTimeout(150);
    for (let k = 0; k < recap.miss; k++) {
      const pick = await pg.evaluate(() => [...document.querySelectorAll('#gameBody [data-opt]')].map(b => b.dataset.opt));
      for (const o of pick) { if (await pg.$('[data-next]')) break; await pg.click(`#gameBody [data-opt="${o}"]`); }
      await pg.click('[data-next]'); await pg.waitForTimeout(60);
    }
    const end = await pg.evaluate(() => ({h: document.querySelector('.recap-h').textContent, chip: !!document.querySelector('.recap .xp-chip')}));
    ok('recap: review ends without a second round bonus', !end.chip, JSON.stringify(end));
    const acts = await pg.evaluate(() => JSON.parse(localStorage.getItem('w2s.anon') || '{}').game || 0);
    ok('recap: the review does not use another free round', acts === 1, 'game rounds counted: ' + acts);
    ok('games: no page errors', !pg.errs.length, pg.errs.join('|'));
    await ctx.close(); }

  // 6. Modo Habla: a capture started in one scene never lands in the next
  { const {ctx, pg} = await fresh(b);
    await pg.goto(BASE + '/modo-habla/'); await pg.waitForTimeout(900);
    await pg.click('text=Empieza a hablar'); await pg.waitForTimeout(500);
    await pg.click('#speakMic'); await pg.waitForTimeout(80);
    await pg.evaluate(() => { const b = document.querySelector('[data-mission="airport"]'); b.click(); });
    await pg.waitForTimeout(150);
    await pg.evaluate(() => { const r = window.__sr.inst.at(-1); r.say('I would like a coffee please'); r.onend && r.onend(); });
    await pg.waitForTimeout(400);
    const lines = await pg.$$eval('#chat > *', d => d.map(x => x.textContent));
    ok('speak: old capture does not reach the new scene', !lines.some(t => /coffee please/.test(t)), lines.join(' | ').slice(0, 120));
    await pg.fill('#speakInput', 'Hi, here is my passport.'); await pg.press('#speakInput', 'Enter'); await pg.waitForTimeout(400);
    ok('speak: typing still moves the new scene on', (await pg.$$eval('#chat .msg.t', d => d.length)) >= 2);
    ok('speak: no page errors', !pg.errs.length, pg.errs.join('|'));
    await ctx.close(); }

  // 7. Recorded clips: a clip in the manifest plays from its file with word timing; replay makes no synthesis call
  { const AUDIO = () => { window.W2S_AUDIO = {base: '/audio-fixture/', clips: {"us|Hi, I'm Ana.": {f: 'hi.wav', w: [0, 250, 500], d: 900}}};
      window.__spoken = 0; const s = window.speechSynthesis; if (s) { const orig = s.speak.bind(s); s.speak = u => { window.__spoken++; return orig(u); }; } };
    const {ctx, pg} = await fresh(b, {audio: AUDIO});
    await ctx.route('**/audio-fixture/**', route => route.fulfill({body: wav(0.9), contentType: 'audio/wav'}));
    await pg.goto(BASE + '/juegos/'); await pg.waitForTimeout(500);
    const ev = await pg.evaluate(() => new Promise(res => { const words = []; let clip = false;
      addEventListener('w2s:speakstart', e => { clip = !!(e.detail && e.detail.clip); });
      addEventListener('w2s:word', e => words.push(e.detail.i));
      window.W2S.Voice.speak("Hi, I'm Ana.", {rate: 1, onEnd: () => setTimeout(() => res({clip, words, spoken: window.__spoken}), 50)}); setTimeout(() => res({clip, words, spoken: window.__spoken, timeout: true}), 4000); }));
    ok('audio: a clip plays from its file with word timing', ev.clip && ev.words.includes(2) && ev.spoken === 0, JSON.stringify(ev));
    const fb = await pg.evaluate(() => new Promise(res => { let started = false; addEventListener('w2s:speakstart', () => { started = true; });
      window.W2S.Voice.speak('A sentence with no clip.', {rate: 1, onEnd: () => res({started, spoken: window.__spoken})}); setTimeout(() => res({started, timeout: true}), 6000); }));
    ok('audio: without a clip the device voice path still runs', fb.started, JSON.stringify(fb));
    await ctx.close(); }

  // 8. Reduced motion: feedback is still shown, nothing waits on an animation
  { const {ctx, pg} = await fresh(b, {reducedMotion: 'reduce'});
    await pg.goto(BASE + '/juegos/'); await pg.waitForTimeout(500);
    await tapInOrder(pg, "Hi, I'm Ana.", '#gameBody'); await pg.click('[data-check]'); await pg.waitForTimeout(50);
    ok('reduced motion: feedback and Next at once', await pg.evaluate(() => !!document.querySelector('#gameBody .fb.ok') && !!document.querySelector('[data-next]')));
    ok('reduced motion: no tile animations', await pg.evaluate(() => document.getAnimations().filter(a => a.effect && a.effect.target && a.effect.target.classList && a.effect.target.classList.contains('tile')).length === 0));
    await ctx.close(); }

  await b.close();
  const bad = results.filter(r => !r[1]).length; console.log(bad ? bad + ' failing of ' + results.length : 'all ' + results.length + ' checks pass'); process.exit(bad ? 1 : 0);
})();
function innerHeightOf() { return devices['iPhone 13'].viewport.height; }
function wav(sec) { // a quiet tone, made here so no audio fixture ships with the site
  const rate = 16000, n = Math.round(rate * sec), buf = Buffer.alloc(44 + n * 2);
  buf.write('RIFF', 0); buf.writeUInt32LE(36 + n * 2, 4); buf.write('WAVEfmt ', 8); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(1, 22);
  buf.writeUInt32LE(rate, 24); buf.writeUInt32LE(rate * 2, 28); buf.writeUInt16LE(2, 32); buf.writeUInt16LE(16, 34); buf.write('data', 36); buf.writeUInt32LE(n * 2, 40);
  for (let i = 0; i < n; i++) buf.writeInt16LE(Math.round(Math.sin(i / rate * 2 * Math.PI * 440) * 3000), 44 + i * 2);
  return buf;
}
