"""Third layer, applied by apply_sprint.py after apply_more.py: the practice loop, made for a nervous first-timer on a phone.

- Microphone: every capture can be cancelled (switching game, item, scene or page drops its result), and each outcome
  has its own message: silence, blocked, no microphone, recognition failed. None of them counts as a wrong answer.
- Games: an item is scored once (double taps, a late spoken result after typing, stale callbacks after Next);
  feedback shows the English phrase first and the XP smaller; tiles travel between word bank and tray;
  a round ends with a recap of every phrase and a quick round of the ones that were missed.
- Imita: honest wording for Solo (the microphone recognised words; it does not grade pronunciation),
  and each mode ends with a button into the next one.
- Home: the first action is a finishable Day 1 sample (introduce yourself), right under the hero, with one step on
  into the Day 1 round; returning learners get a Continue link to their next Sprint task.
- Voice: recorded clips from a manifest when one exists (word timings drive the highlight and the Buddy's mouth),
  the device voice otherwise.
- track(): learning-behaviour events, counted on this device only (no network).
"""
import json


ENDROUND = r"""function targetOf(it) { return G.kind === 'order' ? it.s : G.kind === 'gap' ? it.t.replace('___', it.a) : G.kind === 'sound' ? it.w + ' / ' + it.alt : G.kind === 'quick' ? it.m : it.a[0]; }
function endRound() {
  const items = gItems(), n = items.length, miss = items.map((_, k) => k).filter(k => G.marks[k] !== 1);
  const review = !!G.queue; let bonusLine = '';
  if (!G.paid) { G.paid = true; const bonus = 20 + G.first * 2; addXP(bonus); markActivity('game:' + G.kind + ':' + (G.day + 1)); bonusLine = '<span class="xp-chip num">+' + bonus + ' XP</span>'; }
  track('round_complete', {mode: 'game:' + G.kind, first: G.first, n, review});
  const keys = Object.keys(GAMES), nextKind = keys[(keys.indexOf(G.kind) + 1) % keys.length];
  const list = '<ul class="recap-list">' + items.map((it, k) => '<li class="' + (G.marks[k] === 1 ? 'ok' : 'miss') + '">' + ic(G.marks[k] === 1 ? 'check' : 'refresh') + '<span lang="en">' + esc(targetOf(it)) + '</span></li>').join('') + '</ul>';
  gameBody.innerHTML = '<div class="recap"><h2 class="recap-h">' + (review ? (miss.length ? 'Review done' : 'All of them right now') : 'Round done') + '</h2>' +
    '<p class="recap-score"><span class="score num">' + (n - miss.length) + '/' + n + '</span> ' + (review ? 'right now' : 'right on the first try') + ' ' + bonusLine + '</p>' + list +
    '<div class="row">' + (miss.length ? '<button type="button" class="key primary" data-retry="1">' + ic('refresh') + 'Practise the ones you missed' + ' (' + miss.length + ')</button>' : '') +
    '<button type="button" class="key' + (miss.length ? '' : ' primary') + '" data-switch="' + nextKind + '">' + 'Next game' + ': ' + esc(GAMES[nextKind].name) + ic('arrow') + '</button>' +
    '<button type="button" class="key ghost" data-again="1">' + 'Play this round again' + '</button></div></div>';
  if (!miss.length) burstFrom(gameBody.querySelector('.recap-h'));
  const f = gameBody.querySelector('.recap-h'); if (f) { f.tabIndex = -1; f.focus({preventScroll: true}); }
}
"""


def apply(s):
    def rep(a, b, n=1):
        nonlocal s
        assert s.count(a) == n, ('EXPECTED', n, s.count(a), a[:100])
        s = s.replace(a, b)

    # ---------- icons ----------
    rep("refresh:'<path d=\"M20 11a8 8 0 1 0-2.3 5.7M20 4v7h-7\"/>'",
        "refresh:'<path d=\"M20 11a8 8 0 1 0-2.3 5.7M20 4v7h-7\"/>', x:'<path d=\"M6 6l12 12M18 6L6 18\"/>', alert:'<path d=\"M12 8v5M12 16.5v.5\"/><circle cx=\"12\" cy=\"12\" r=\"9\"/>'")

    # ---------- track(): events kept on this device ----------
    rep("/* ---------- feedback: toast, xp, confetti ---------- */", r"""/* ---------- learning-behaviour events: counted on this device only, never sent anywhere ---------- */
const T0 = Date.now(), FIRST = {};
function track(name, props) {
  const d = Object.assign({name, ms: Date.now() - T0, page: document.body.dataset.page || ''}, props || {});
  if (!FIRST[name]) { FIRST[name] = d.ms; d.first = true; }
  window.W2S_FIRST = FIRST; emit('metric', d);
  try { const k = 'w2s.metrics', m = JSON.parse(localStorage.getItem(k) || '{}'), day = today(); m[day] = m[day] || {}; m[day][name] = (m[day][name] || 0) + 1;
    Object.keys(m).sort().slice(0, -14).forEach(x => delete m[x]); localStorage.setItem(k, JSON.stringify(m)); } catch (e) {}
}
window.addEventListener('w2s:speakstart', e => { if (e.detail && e.detail.audio) track('audio_start'); });

/* ---------- feedback: toast, xp, confetti ---------- */""")

    # ---------- Voice: recorded clips first, then the device voice ----------
    rep("  function stop() { emit('speakend'); token++; clear(); try { if (synth) synth.cancel(); } catch (e) {} if (tts) { try { tts.stop().catch(() => {}); } catch (e) {} } }",
        r"""  /* recorded clips: window.W2S_AUDIO = {base, clips: {key: {f, w: [word start in ms], d: duration ms}}}; key = accent|gender|text */
  const AUD = window.W2S_AUDIO || null; let el = null; const pre = {};
  /* Speech Mode speaks as the Buddy (its own voice first, e.g. us|kairo, then its gender); every other room uses the
     learner's Female/Male voice choice (state.voiceG). */
  const clipKey = text => { const acc = state.accent; return voiceSlots().map(v => acc + '|' + v + '|' + text).concat([acc + '|' + text]); };
  function clipOf(text) { if (!AUD || !AUD.clips) return null; for (const k of clipKey(String(text).trim())) if (AUD.clips[k]) return AUD.clips[k]; return null; }
  function preload(text) { const c = clipOf(text); if (!c || pre[c.f]) return; const a = new Audio(); a.preload = 'auto'; a.src = AUD.base + c.f; pre[c.f] = a; }
  function playClip(c, text, rate, opts, id, end, fallback) {
    if (!el) { el = new Audio(); el.preload = 'auto'; }
    const a = el; a.onended = a.onerror = a.ontimeupdate = null; a.src = AUD.base + c.f; a.playbackRate = Math.max(.5, Math.min(2, rate));
    try { a.preservesPitch = true; a.webkitPreservesPitch = true; } catch (e) {}
    let started = false, last = -1, raf = 0;
    const tick = () => { if (id !== token) return; const ms = a.currentTime * 1000; let i = 0; while (c.w && i + 1 < c.w.length && c.w[i + 1] <= ms) i++; if (c.w && i !== last) { last = i; if (opts.onWord) opts.onWord(i); } if (!a.paused) raf = requestAnimationFrame(tick); };
    a.onplaying = () => { if (id !== token) return; if (!started) { started = true; emit('speakstart', {audio: true, clip: true}); emit('timing', {exact: !!c.w}); if (!c.w) plan(text, rate, opts.onWord, null, id); } tick(); };
    a.onended = () => { cancelAnimationFrame(raf); end(); };
    a.onerror = () => { cancelAnimationFrame(raf); if (id !== token) return; track('audio_fail', {via: 'clip'}); if (!started) fallback(); else end(); };
    const p = a.play(); if (p && p.catch) p.catch(err => { if (id !== token) return; track('audio_fail', {via: 'clip', blocked: err && err.name === 'NotAllowedError'}); fallback(); });
  }
  function stop() { emit('speakend'); token++; clear(); if (el) { try { el.pause(); } catch (e) {} } try { if (synth) synth.cancel(); } catch (e) {} if (tts) { try { tts.stop().catch(() => {}); } catch (e) {} } }""")
    rep("""    const viaClaude = () => { emit('speakstart', {audio: true}); plan(text, rate, opts.onWord, null, id); tts.speak(text, {rate: Math.min(1.5, Math.max(.7, rate)), language:'en'}).then(end, end); };
    if (r.kind === 'device') {""",
        """    const viaClaude = () => { emit('speakstart', {audio: true}); plan(text, rate, opts.onWord, null, id); tts.speak(text, {rate: Math.min(1.5, Math.max(.7, rate)), language:'en'}).then(end, end); };
    const clip = clipOf(text);
    if (clip) { playClip(clip, text, rate, opts, id, end, () => device(true)); return; }
    device(false);
    function device(afterClip) {
    if (afterClip) clear();
    if (r.kind === 'device') {""")
    rep("""    } else if (r.kind === 'claude') viaClaude();
    else { emit('speakstart', {audio: false}); plan(text, rate, opts.onWord, end, id); }
  }
  return {speak, pace, stop, note: () => route().note, setTts: t => { tts = t; renderVoiceNotes(); }};""",
        """    } else if (r.kind === 'claude') viaClaude();
    else { track('audio_fail', {via: 'none'}); emit('speakstart', {audio: false}); plan(text, rate, opts.onWord, end, id); }
    }
  }
  return {speak, pace, stop, preload, hasClip: t => !!clipOf(t), kind: () => route().kind, note: () => route().note, setTts: t => { tts = t; renderVoiceNotes(); }};""")
    rep("      u.onerror = () => { if (id !== token) return; if (!started) { broken = ++fails >= 2;",
        "      u.onerror = () => { if (id !== token) return; if (!started) { track('audio_fail', {via: 'device'}); broken = ++fails >= 2;")

    # ---------- Mic: cancel, and one message per outcome ----------
    rep("""      if (code === 'not_granted' || code === 'unavailable') { root.classList.remove('has-mic'); toast('The microphone is off for this page. You can keep typing.'); }
      if (c && c.onEnd) c.onEnd('', code || 'error');""",
        """      track('mic_fail', {reason: code || 'error'});
      if (code === 'not_granted' || code === 'no_mic') root.classList.remove('has-mic');
      if (!(c && c.quiet)) toast(micWhy(code));
      if (c && c.onEnd) c.onEnd('', code || 'error');""")
    rep("    Voice.stop(); text = ''; cur = h; setBtn(true);", "    Voice.stop(); text = ''; cur = h; setBtn(true); track('mic_start');")
    rep("  function stop() { if (d && cur) { try { d.stop().catch(() => {}); } catch (e) {} } }\n  return {attach, start, stop, active",
        "  function stop() { if (d && cur) { try { d.stop().catch(() => {}); } catch (e) {} } }\n"
        "  function cancel() { if (!cur) return; cur = null; setBtn(false); if (d) { try { d.stop().catch(() => {}); } catch (e) {} } }\n"
        "  return {attach, start, stop, cancel, active")
    rep("/* ---------- text helpers ---------- */", r"""function micWhy(r) {
  if (r === 'silence' || r === 'stopped' || !r) return 'I did not hear anything. Move a little closer to the microphone and try again. It does not count as a mistake.';
  if (r === 'not_granted') return 'The microphone is blocked for this site, so type your answer instead. To speak, allow the microphone in your browser settings.';
  if (r === 'no_mic') return 'No microphone was found. Type your answer instead.';
  return 'Speech recognition did not work this time. It does not count as a mistake. Try again, or type your answer.';
}

/* ---------- text helpers ---------- */""")
    # anything that starts something new drops a capture that is still running
    rep("function startMission(id) {\n  if (MISSIONS[id].ai && !cap.sample) id = 'cafe';\n  Voice.stop(); Mic.stop();",
        "function startMission(id) {\n  if (MISSIONS[id].ai && !cap.sample) id = 'cafe';\n  Voice.stop(); Mic.cancel(); track('practice_start', {mode: 'speak:' + id});")
    rep("  Voice.stop(); Mic.stop(); if (SH.playing) shStop(); if (TALK.run) talkStop(false);",
        "  Voice.stop(); Mic.cancel(); if (SH.playing) shStop(); if (TALK.run) talkStop(false);")
    rep("function shStop() { Voice.stop(); Mic.stop();", "function shStop() { Voice.stop(); Mic.cancel();")
    # Modo Habla: count the turn and keep the reason for an empty capture
    rep("onEnd: (said, reason) => { if (said) { emit('micresult'); sendLine(said); } else emit('micempty', {reason: reason || ''}); }});",
        "onEnd: (said, reason) => { if (said) { emit('micresult'); track('attempt', {mode: 'speak', input: 'mic'}); sendLine(said); } else { track('mic_empty', {reason: reason || ''}); emit('micempty', {reason: reason || ''}); } }});")
    rep("$('#composer').addEventListener('submit', e => { e.preventDefault(); sendLine($('#speakInput').value); });",
        "$('#composer').addEventListener('submit', e => { e.preventDefault(); if ($('#speakInput').value.trim()) track('attempt', {mode: 'speak', input: 'typed'}); sendLine($('#speakInput').value); });")
    rep("  addXP(bonus); markActivity('speak:' + S.id); burstFrom(chat); emit('done', {bonus});",
        "  addXP(bonus); markActivity('speak:' + S.id); burstFrom(chat); emit('done', {bonus}); track('round_complete', {mode: 'speak:' + S.id});")

    # ---------- games: state ----------
    rep("const G = {kind:'order', day:0, picked:false, i:0, marks:[], combo:0, tries:0, solved:false, tray:[], pool:[], toks:[], first:0};",
        "const G = {kind:'order', day:0, picked:false, i:0, marks:[], combo:0, tries:0, solved:false, tray:[], pool:[], toks:[], first:0, tok:0, queue:null, qi:0, paid:false};")
    rep("function startGame(kind, day) {\n  Voice.stop(); Mic.stop();", "function startGame(kind, day) {\n  Voice.stop(); Mic.cancel();")
    rep("Object.assign(G, {kind, day: Math.max(0, Math.min(6, +day || 0)), i:0, marks:[], combo:0, first:0});",
        "Object.assign(G, {kind, day: Math.max(0, Math.min(6, +day || 0)), i:0, marks:[], combo:0, first:0, queue:null, qi:0, paid:false});\n  track('practice_start', {mode: 'game:' + kind});")
    rep("  $$('#gameTabs button').forEach(b => b.setAttribute('aria-pressed', b.dataset.game === kind));",
        "  $$('#gameTabs button').forEach(b => b.setAttribute('aria-pressed', b.dataset.game === kind));\n"
        "  { const on = document.querySelector('#gameTabs [aria-pressed=true]'), bar = document.getElementById('gameTabs'); if (on && bar && bar.scrollWidth > bar.clientWidth) bar.scrollLeft = Math.max(0, on.offsetLeft - 8); }")
    rep("  G.tries = 0; G.solved = false; G.fb = null; G.heard = ''; G.typed = '';",
        "  Mic.cancel(); G.tok++; G.tries = 0; G.solved = false; G.fb = null; G.heard = ''; G.typed = '';")

    # ---------- games: feedback block (phrase first, XP small, space reserved) ----------
    rep("""function fbHtml() {
  if (!G.fb) return '<div class="fb info" style="visibility:hidden" aria-hidden="true">.</div>';
  return `<div class="fb ${G.fb.kind}" role="status">${esc(G.fb.title)}${G.fb.body ? `<span>${G.fb.body}</span>` : ''}</div>`;
}""", """function fbHtml() {
  if (!G.fb) return '<div class="fb fb-empty" aria-hidden="true"></div>';
  const f = G.fb, icon = f.kind === 'ok' ? ic('check') : f.kind === 'bad' ? ic('refresh') : f.kind === 'warn' ? ic('alert') : '';
  return `<div class="fb ${f.kind}${f.nudge ? ' nudge' : ''}" role="status"><b class="fb-t">${icon}${esc(f.title)}${f.xp ? `<span class="xp-chip num">+${f.xp} XP</span>` : ''}</b>` +
    (f.say ? `<p class="fb-say" lang="en">${esc(f.say)}</p>` : '') + (f.body ? `<span class="fb-b">${f.body}</span>` : '') + '</div>';
}""")

    # ---------- games: score once ----------
    rep("""function solve(ok, title, body, bonus) {
  G.solved = true; G.marks[G.i] = ok && G.tries === 0 ? 1 : 0;
  if (ok) { G.combo++; if (G.tries === 0) G.first++; const xp = 10 + Math.min(10, (G.combo - 1) * 2) + (bonus || 0); addXP(xp); G.fb = {kind:'ok', title: title + ' +' + xp + ' XP', body}; if (G.kind !== 'sound') logLine(GAMES[G.kind].name, G.kind === 'quick' && G.typed ? G.typed : target()); }
  else { G.combo = 0; G.fb = {kind:'bad', title, body}; }
  renderGame();
  if (ok) burstFrom($('.prompt', gameBody) || $('.tray', gameBody));
  Voice.speak(target(), {rate:.9});
}""", """function solve(ok, title, body, bonus) {
  if (G.solved) return;
  G.solved = true; G.marks[G.i] = ok && G.tries === 0 ? 1 : 0;
  const say = target();
  if (ok) { G.combo++; if (G.tries === 0 && !G.queue) G.first++; const xp = 10 + Math.min(10, (G.combo - 1) * 2) + (bonus || 0); addXP(xp); G.fb = {kind:'ok', title, body, xp, say}; if (G.kind !== 'sound') logLine(GAMES[G.kind].name, G.kind === 'quick' && G.typed ? G.typed : say); }
  else { G.combo = 0; G.fb = {kind:'bad', title, body, say}; }
  track('feedback', {mode: 'game:' + G.kind, result: ok ? 'right' : 'shown'});
  renderGame();
  if (ok) burstFrom(gameBody.querySelector('.fb-say') || gameBody.querySelector('.prompt') || gameBody.querySelector('.tray') || gameBody);
  Voice.speak(say, {rate:.9});
  const nx = gameBody.querySelector('[data-next]'); if (nx) nx.focus({preventScroll: true});
}""")
    rep("function checkQuick(text, spoken) {\n  const it = gItems()[G.i]; G.typed = text;\n  if (!text.trim()) return;",
        "function checkQuick(text, spoken) {\n  if (G.solved) return;\n  const it = gItems()[G.i]; G.typed = text;\n  if (!text.trim()) return;\n  track('attempt', {mode: 'game:quick', input: spoken ? 'mic' : 'typed'});")
    rep("function checkFlash(text, spoken) {\n  const it = gItems()[G.i]; G.typed = text;\n  if (!text.trim()) return;",
        "function checkFlash(text, spoken) {\n  if (G.solved) return;\n  const it = gItems()[G.i]; G.typed = text;\n  if (!text.trim()) return;\n  track('attempt', {mode: 'game:flash', input: spoken ? 'mic' : 'typed'});")
    rep("function miss(title, body) { G.tries++; G.combo = 0; G.fb = {kind:'bad', title, body}; renderGame(); }",
        "function miss(title, body) { if (G.solved) return; G.tries++; G.combo = 0; G.fb = {kind:'bad', title, body, nudge: true}; track('feedback', {mode: 'game:' + G.kind, result: 'retry'}); renderGame(); }")
    # the model phrase now sits in its own line, so the bodies stop repeating it
    rep("solve(true, 'Correct.', 'Now say it out loud: <b>' + esc(it.s) + '</b>');", "solve(true, 'Correct.', 'Now say it out loud.');")
    rep("    const built = G.tray.map(k => G.toks[k]).join(' ').toLowerCase();", "    const built = G.tray.map(k => G.toks[k]).join(' ').toLowerCase(); track('attempt', {mode: 'game:order', input: 'tap'});")
    rep("solve(false, 'Here is the order.', '<b>' + esc(it.s) + '</b> Say it out loud twice.'); }", "solve(false, 'Here is the order.', 'Say it out loud twice.'); }")
    rep("if (G.tries >= 1) return solve(false, 'Here is the answer.', '<b>' + esc(it.a[0]) + '</b> Say it out loud twice.');",
        "if (G.tries >= 1) return solve(false, 'Here is the answer.', 'Say it out loud twice.');")

    # ---------- games: tiles travel (FLIP), so the eye can follow a word ----------
    rep("  gameBody.innerHTML = html;\n}", r"""  const from = {};
  if (G.kind === 'order' && !reduced) $$('.tray .tile, .pool .tile:not(.gone)', gameBody).forEach(t => { from[t.dataset.tile || t.dataset.untile] = t.getBoundingClientRect(); });
  gameBody.innerHTML = html;
  if (G.kind === 'order' && !reduced && Object.keys(from).length) $$('.tray .tile, .pool .tile:not(.gone)', gameBody).forEach(t => {
    const a = from[t.dataset.tile || t.dataset.untile]; if (!a) return; const b = t.getBoundingClientRect(); const dx = a.left - b.left, dy = a.top - b.top;
    if (Math.abs(dx) + Math.abs(dy) < 2 || !t.animate) return;
    t.animate([{transform: `translate(${dx}px,${dy}px)`}, {transform: 'none'}], {duration: 190, easing: 'cubic-bezier(.2,.8,.2,1)'});
  });
}""")

    # ---------- games: spoken answers belong to the item they were given for ----------
    rep("""    G.fb = {kind:'info', title:'Listening. Say "' + it.w + '".'}; renderGame();
    Mic.start({button: $('[data-sayword]', gameBody), onText: () => {}, onEnd: said => {
      const heard""", """    G.fb = {kind:'info', title:'Listening. Say "' + it.w + '".'}; renderGame(); const tok = G.tok;
    Mic.start({quiet: true, button: $('[data-sayword]', gameBody), onText: () => {}, onEnd: (said, reason) => {
      if (tok !== G.tok) return;
      if (!said) { G.fb = {kind:'warn', title: micWhy(reason)}; renderGame(); return; }
      const heard""")
    rep("""      if (!said) G.fb = {kind:'info', title:'I did not catch that. Try again.'};
      else if (heard.includes(' ' + it.w + ' '))""", """      if (heard.includes(' ' + it.w + ' '))""")
    rep("""    G.heard = ''; G.fb = {kind:'info', title:'Listening. Say the sentence.'}; if (G.kind === 'flash' || G.kind === 'quick') G.typed = $('#flashInput').value || ''; renderGame();
    Mic.start({button: $('[data-say]', gameBody), onText: t => { const inp = $('#flashInput'); if (inp) inp.value = t; }, onEnd: said => {
      if (!said) { G.fb = {kind:'info', title:'I did not catch that. Try again.'}; renderGame(); return; }""",
        """    G.heard = ''; G.fb = {kind:'info', title:'Listening. Say the sentence.'}; if (G.kind === 'flash' || G.kind === 'quick') G.typed = $('#flashInput').value || ''; renderGame(); const tok = G.tok;
    Mic.start({quiet: true, button: $('[data-say]', gameBody), onText: t => { if (tok !== G.tok) return; const inp = $('#flashInput'); if (inp) inp.value = t; }, onEnd: (said, reason) => {
      if (tok !== G.tok || G.solved) return;
      if (!said) { G.fb = {kind:'warn', title: micWhy(reason)}; renderGame(); const inp = document.getElementById('flashInput'); if (inp && (reason === 'not_granted' || reason === 'no_mic')) inp.focus(); return; }""")
    rep("if (similar(it.s, said) >= .85) { G.tray = G.toks.map((_, k) => k); solve(true, 'You said it.', '<b>' + esc(it.s) + '</b>', 5); }",
        "track('attempt', {mode: 'game:order', input: 'mic'}); if (similar(it.s, said) >= .85) { G.tray = G.toks.map((_, k) => k); solve(true, 'The microphone understood it.', '', 5); }")
    # Sound Lab: say clearly when the device cannot play a word
    rep("  else if (b.dataset.hearword) { G.played = true; renderGame(); Voice.speak(it.w, {rate:.85}); }",
        "  else if (b.dataset.hearword) { G.played = true; if (Voice.kind() === 'none' && !Voice.hasClip(it.w)) G.fb = {kind:'warn', title:'This device has no English voice, so Sound Lab cannot play the word. Try Word Order or Fill the Gap instead.'}; renderGame(); Voice.speak(it.w, {rate:.85}); }")
    rep("    if (G.choice === it.w) solve(true, 'Correct: \"' + it.w + '\".', esc(it.n));",
        "    track('attempt', {mode: 'game:sound', input: 'tap'});\n    if (G.choice === it.w) solve(true, 'Correct: \"' + it.w + '\".', esc(it.n));")
    rep("    G.choice = b.dataset.opt;\n    if (G.choice === it.a)", "    G.choice = b.dataset.opt; track('attempt', {mode: 'game:gap', input: 'tap'});\n    if (G.choice === it.a)")

    # ---------- games: next, recap, quick review of the misses ----------
    rep("  else if (b.dataset.next) { if (G.i + 1 < gItems().length) { G.i++; loadItem(); } else endRound(); }",
        """  else if (b.dataset.next) { track('next', {mode: 'game:' + G.kind});
    if (G.queue) { G.qi++; if (G.qi < G.queue.length) { G.i = G.queue[G.qi]; loadItem(); } else endRound(); }
    else if (G.i + 1 < gItems().length) { G.i++; loadItem(); } else endRound(); }
  else if (b.dataset.retry) { const miss = gItems().map((_, k) => k).filter(k => G.marks[k] !== 1); if (miss.length) { G.queue = miss; G.qi = 0; G.i = miss[0]; G.combo = 0; loadItem(); } }""")
    i0 = s.index("function endRound() {"); i1 = s.index("\n$('#gameTabs').addEventListener", i0)
    s = s[:i0] + ENDROUND + s[i1:]

    # ---------- Imita: honest result text, and a next step at the end of each mode ----------
    rep("of the words came through clearly. Underlined words were not heard: listen to those again. +15 XP",
        "of the words were recognised by the microphone. That checks the words, not your accent. Underlined words were not recognised: listen to those again. +15 XP")
    rep("$('#shPlay').addEventListener('click', shPlay);", r"""$('#shPlay').addEventListener('click', shPlay);
$('#shResult').addEventListener('click', e => { const b = e.target.closest('[data-shnext]'); if (!b) return; const m = b.dataset.shnext;
  if (m === 'clip') { const ids = Object.keys(CLIPS).filter(k => k !== 'mine'), i = ids.indexOf(SH.clip); SH.clip = ids[(i + 1) % ids.length]; SH.reps = 0; SH.mode = 'listen'; renderShadow(); }
  else { SH.mode = m; renderShadow(); shPlay(); } track('next', {mode: 'shadow:' + m}); });
const shNext = m => '<div class="row sh-next"><button type="button" class="key primary" data-shnext="' + m + '">' + (m === 'shadow' ? ic('play') + 'Now speak along' : m === 'solo' ? ic('mic') + 'Now try it solo' : 'Next clip' + ic('arrow')) + '</button></div>';""")
    rep("""onEnd: () => shDone('<div class="fb info">Heard it. <span>Play it again, or move to Shadow and speak along.</span></div>', 0)});""",
        """onEnd: () => { track('round_complete', {mode: 'shadow:listen'}); shDone('<div class="fb info">Heard it. <span>Play it again, or move to Shadow and speak along.</span></div>', 0); }});""")

    rep("function shDone(html, xp) { SH.playing = false; shButton(); if (xp) addXP(xp); $('#shResult').innerHTML = html; }",
        "function shDone(html, xp) { SH.playing = false; shButton(); if (xp) addXP(xp);\n"
        "  const nx = /data-rate-self/.test(html) ? '' : SH.mode === 'listen' ? 'shadow' : SH.mode === 'shadow' ? (SH.reps % 3 === 0 ? 'solo' : 'shadow') : (xp ? 'clip' : 'solo');\n"
        "  if (SH.mode !== 'listen' && xp) track('round_complete', {mode: 'shadow:' + SH.mode});\n"
        "  $('#shResult').innerHTML = html + (nx ? shNext(nx) : ''); }")
    rep("const shNext = m => '<div class=\"row sh-next\"><button type=\"button\" class=\"key primary\" data-shnext=\"' + m + '\">' + (m === 'shadow' ? ic('play') + 'Now speak along' :",
        "const shNext = m => '<div class=\"row sh-next\"><button type=\"button\" class=\"key primary\" data-shnext=\"' + m + '\">' + (m === 'shadow' ? ic('play') + (SH.mode === 'shadow' ? 'Speak along again' : 'Now speak along') :")

    # ---------- home: the first action is a finishable sample ----------
    rep("""      <div class="row">
        <a class="key hl big" data-magnet href="#sprint">Start the 7-Day Sprint</a>
        <a class="key ghost big" data-magnet href="#films" data-jump="films">Watch a session</a>
      </div>""", """      <a class="resume" id="resume" hidden></a>
      <div class="row hero-cta">
        <a class="key hl big" data-magnet href="#try" data-jump="try">Introduce yourself in English</a>
        <a class="key ghost big" href="#sprint">Start the 7-Day Sprint</a>
      </div>
      <p class="hero-note">Free, no account. Tap the words in order, then say them out loud.</p>""")
    # move the playground straight under the hero
    i = s.index('<section class="try light" id="try">'); j = s.index('</div></section>', i) + len('</div></section>')
    tri = s[i:j]; s = s[:i] + s[j:]
    tri = tri.replace('<h2 data-split>Try it on this page</h2>\n  <p class="sub">Two pieces of the practice rooms, working right here.</p>',
                      '<h2 data-split>Introduce yourself in English</h2>\n  <p class="sub">Four real Day 1 sentences. Tap the words in order, hear the sentence, say it out loud.</p>')
    # Word Order first: it is the finishable sample; Catch your Spanish second
    a0 = tri.index('    <div class="toy">\n      <h3>Catch your Spanish</h3>'); a1 = tri.index('    <div class="toy">\n      <div class="g-top"><h3>Word Order</h3>')
    a2 = tri.index('  </div>\n  <div class="row" style="margin-top:30px">')
    tri = tri[:a0] + tri[a1:a2] + tri[a0:a1] + tri[a2:]
    tri = tri.replace('<p>Tap the words in order to build the sentence.</p>', '<p>Tap the words in order to build the sentence. Tap a word in the sentence to take it back.</p>')
    tri = tri.replace('<p class="gmsg" id="gMsg" role="status"></p>', '<p class="gmsg" id="gMsg" role="status"></p>\n      <div class="row g-act" id="gAct"></div>')
    k = s.index('<section class="unlearn light" id="unlearn">'); s = s[:k] + tri + '\n\n' + s[k:]

    # the home Word Order: Day 1 sentences, a Next button instead of a timer, and one step on into the full round
    rep("const GS = ['Where is the bus station?', 'Can you help me, please?', 'I am twenty-five years old.', 'What time does the shop open?'];",
        "const GS = [\"Hi, I'm Ana.\", \"I'm from Lima, in Peru.\", \"I'm thirty years old.\", 'Nice to meet you.'];")
    rep("  GM.busy = false; gTray.classList.remove('ok'); gTray.innerHTML = ''; gMsg.textContent = ''; gMsg.className = 'gmsg'; gDotsDraw();",
        "  GM.busy = false; gTray.classList.remove('ok'); gTray.innerHTML = ''; gMsg.textContent = ''; gMsg.className = 'gmsg'; gDotsDraw(); gAct.innerHTML = '';")
    rep("""  if (GM.i >= GS.length) { gPool.innerHTML = '<button type="button" class="key cobalt" id="gAgain">Play again</button>'; gMsg.textContent = 'Four sentences built. Now say each one out loud.'; gMsg.className = 'gmsg ok'; return; }""",
        """  if (GM.i >= GS.length) { gPool.innerHTML = ''; gMsg.textContent = 'You can introduce yourself in four sentences. Day 1 has eight more.'; gMsg.className = 'gmsg ok done';
    gAct.innerHTML = '<a class="key hl big" href="' + W.path('games') + '" data-go=\\'{"game":"order","day":0}\\'>' + 'Play the Day 1 round' + '</a><a class="key" href="' + W.path('speak') + '" data-go=\\'{"mission":"cafe"}\\'>' + 'Order a coffee with a Buddy' + '</a><button type="button" class="key ghost" id="gAgain">Play again</button>';
    W.track && W.track('round_complete', {mode: 'home:order'}); W.burst(gMsg); return; }""")
    rep("""    GM.busy = true; gTray.classList.add('ok'); gMsg.textContent = GS[GM.i] + ' Say it out loud.'; gMsg.className = 'gmsg ok'; W.burst(gTray); W.Voice.speak(GS[GM.i], {rate: .95}); W.addXP(10); W.logLine('Home: Word Order', GS[GM.i]);
    if (live) gs.fromTo(gTray.children, {y: 0}, {y: -10, duration: .18, ease: 'power2.out', yoyo: true, repeat: 1, stagger: .04});
    setTimeout(() => { GM.i++; gLoad(); }, 1900);""",
        """    GM.busy = true; gTray.classList.add('ok'); gMsg.innerHTML = '<b lang="en">' + esc(GS[GM.i]) + '</b> ' + esc('Now say it out loud.'); gMsg.className = 'gmsg ok'; W.Voice.speak(GS[GM.i], {rate: .95}); W.addXP(10); W.logLine('Home: Word Order', GS[GM.i]);
    W.track && W.track('feedback', {mode: 'home:order', result: 'right'});
    if (live) gs.fromTo(gTray.children, {y: 0}, {y: -6, duration: .12, ease: 'power2.out', yoyo: true, repeat: 1});
    gAct.innerHTML = '<button type="button" class="key" id="gHear">' + W.ic('speaker') + 'Hear it' + '</button><button type="button" class="key primary" id="gNext">' + (GM.i + 1 < GS.length ? 'Next sentence' : 'See how you did') + W.ic('arrow') + '</button>';
    const nx = document.getElementById('gNext'); if (nx) nx.focus({preventScroll: true});""")
    rep("""    gMsg.textContent = 'Not yet. It starts with "' + GM.toks.slice(0, 2).join(' ') + '". Tap a word to take it back.'; gMsg.className = 'gmsg no';""",
        """    gMsg.textContent = 'Not yet. It starts with "' + GM.toks.slice(0, 2).join(' ') + '". Tap a word to take it back.'; gMsg.className = 'gmsg no'; W.track && W.track('feedback', {mode: 'home:order', result: 'retry'});""")
    rep("  const t = e.target.closest('.tile'); if (!t || GM.busy) return;",
        "  const t = e.target.closest('.tile'); if (!t || GM.busy) return; if (W.track && !GM.started) { GM.started = true; W.track('practice_start', {mode: 'home:order'}); }")
    rep("gTray.addEventListener('click', gClick); gPool.addEventListener('click', gClick); gLoad();",
        """const gAct = $('#gAct');
gAct.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return;
  if (b.id === 'gHear') W.Voice.speak(GS[GM.i], {rate: .9});
  else if (b.id === 'gNext') { W.Voice.stop(); GM.i++; gLoad(); W.track && W.track('next', {mode: 'home:order'}); const f = gPool.querySelector('.tile'); if (f) f.focus({preventScroll: true}); }
  else if (b.id === 'gAgain') { GM.i = 0; gLoad(); } });
gTray.addEventListener('click', gClick); gPool.addEventListener('click', gClick); gLoad();""")
    rep("window.W2S = {Voice, RULES, addXP, logLine, burst: burstFrom,", "window.W2S = {Voice, RULES, addXP, logLine, track, ic, path: v => (typeof pathOf === 'function' ? pathOf(v) : '#' + v), burst: burstFrom,")

    # ---------- home: Continue, for a learner with saved progress on this device ----------
    rep("/* ---------- boot ---------- */", r"""/* ---------- Continue: the next Sprint task, for a learner who has started ---------- */
function renderResume() {
  const a = document.getElementById('resume'); if (!a) return;
  const started = Object.keys(state.sprint || {}).some(k => state.sprint[k]) || (state.sessions || 0) > 0 || state.xp > 0;
  if (!started) { a.hidden = true; return; }
  const d = sprintDay(), tasks = DAYS[d].tasks, ti = tasks.findIndex((t, k) => t.go && !state.sprint[taskId(d, k)]);
  const t = ti >= 0 ? tasks[ti] : tasks.find(x => x.go); if (!t) { a.hidden = true; return; }
  const go = t.go === 'talk' ? 'sprint' : t.go;
  a.href = (typeof pathOf === 'function' ? pathOf(go) : '#' + go);
  a.dataset.go = JSON.stringify(Object.assign({}, t.set, t.go === 'talk' ? {talk: 1} : {}));
  a.innerHTML = '<span class="resume-k">' + 'Continue · Day' + ' ' + (d + 1) + '</span><b>' + esc(t.short || t.label) + '</b>' + ic('arrow');
  a.hidden = false;
}

/* ---------- boot ---------- */""")
    # ---------- Female or Male voice in every practice room (Speech Mode follows the Buddy) ----------
    rep("const Voice = (() => {", r"""function inSpeak() { try { return currentView === 'speak'; } catch (e) { return false; } }
function voiceG() { return inSpeak() ? (window.W2S_BUDDY_GENDER || 'f') : (state.voiceG === 'm' ? 'm' : 'f'); }
function voiceSlots() { const g = voiceG(); return inSpeak() && window.W2S_BUDDY ? [window.W2S_BUDDY, g] : [g]; }
const VOICE_G = [['f', 'Female voice'], ['m', 'Male voice']];
function renderVoiceG() {
  document.querySelectorAll('[data-voicegender]').forEach(box => { box.setAttribute('role', 'group'); box.setAttribute('aria-label', 'Choose the voice');
    box.innerHTML = VOICE_G.map(([id, name]) => `<button type="button" class="chip" data-vg="${id}" aria-pressed="${(state.voiceG === 'm' ? 'm' : 'f') === id}">${esc(name)}</button>`).join(''); });
}
document.addEventListener('click', e => { const b = e.target.closest('[data-vg]'); if (!b) return;
  state.voiceG = b.dataset.vg === 'm' ? 'm' : 'f'; save(); Voice.stop(); renderVoiceG(); renderVoiceNotes(); });
const Voice = (() => {""")
    rep("const want = window.W2S_BUDDY_GENDER, same", "const want = voiceG(), same")
    # Device voice of the right gender: a woman's line never falls back to a man's voice (Windows lists
    # "Microsoft David" first and has no Australian voice), even if that means another English accent.
    rep("    return same.length ? best(same) : best(m);\n  }",
        """    return same.length ? best(same) : null;
  }
  function anyVoice(acc) {
    if (broken || !voices.length) return null;
    const FEM = /female|zira|jenny|aria|ava|emma|michelle|sonia|libby|hazel|susan|natasha|clara|samantha|karen|catherine|kate|serena|moira|tessa|google us english/i;
    const MAL = /(^|[^e])male|david|mark\\b|guy\\b|ryan|george|james|william|daniel|thomas|oliver|christopher|eric|roger|steffan/i;
    const g = voiceG(), same = voices.filter(v => g === 'm' ? (MAL.test(v.name) && !/female/i.test(v.name)) : FEM.test(v.name));
    const pool = same.length ? same : voices, near = acc.id === 'us' ? /en-us/ : /en-gb|en-au|en-ie|en-nz/;
    const top = l => l.find(v => /natural|online|google/i.test(v.name)) || l[0];
    return top(pool.filter(v => near.test(norm(v)))) || top(pool);
  }""")
    rep("    const any = !broken && voices[0];", "    const any = anyVoice(acc);")
    rep('    <div class="panel stack" id="gameBody"></div>',
        '    <div class="panel stack" id="gameBody"></div>\n    <div class="chips vg-row" data-voicegender style="margin-top:12px"></div>')
    rep('<div class="panel"><h2>Accent</h2><div class="chips" data-accents></div><p class="small muted" data-voicenote style="margin-top:10px"></p></div>',
        '<div class="panel"><h2>Accent</h2><div class="chips" data-accents></div><div class="chips" data-voicegender style="margin-top:10px"></div><p class="small muted" data-voicenote style="margin-top:10px"></p></div>')
    rep('  <div class="course"><div class="mods"', '  <div class="chips vg-row" data-voicegender style="margin-bottom:14px"></div>\n  <div class="course"><div class="mods"')
    rep("renderStats(); renderAccents(); renderMissions(); renderSprint(); save();",
        "renderStats(); renderAccents(); renderVoiceG(); renderMissions(); renderSprint(); renderResume(); save();")
    return s
