"""Speech Mode, built around the Language Buddies.
APP is the whole Speech Mode screen (stage, subtitle, reply bar, bottom sheet), CSS styles it and script() runs it.
The 3D lives in buddies.js; everything here works without it (the static pictures stay on stage)."""

import json
from buddy_roster import ROSTER, ACTIVE

# Display names, from the roster (buddy_roster.py). The internal ids stay `mila` and `rio` so a saved choice still loads.
NAMES = {b['id']: b['name'] for b in ROSTER}
FIRST = ACTIVE[0]
# the static pictures: the first active Buddy loads at once, the others lazily
PICTURES = '\n'.join(
    f'        <img class="bf bf-{b["id"]}" src="/assets/buddies/{b["file"]}.webp" width="540" height="774" alt="{b["alt"]}" decoding="async"{"" if i == 0 else " loading=\"lazy\""}>'
    for i, b in enumerate(ACTIVE))
SWITCH_HIDDEN = ' hidden' if len(ACTIVE) < 2 else ''
# Switch Buddy: one tap swaps to the next Buddy. The button shows the face of the Buddy it will bring in.
SWITCH_FACES = ''.join(f'<img class="bs-face bs-{b["id"]}" src="/assets/buddies/{b["file"]}.webp" alt="" width="30" height="30" decoding="async">' for b in ACTIVE)

I_MENU = '<svg class="ic" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h10" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>'
I_SWAP = '<svg class="ic" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M7 4 3 8l4 4M3 8h13M17 12l4 4-4 4M21 16H8" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_SOUND = '<svg class="ic" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M4 10v4h4l5 4V6l-5 4z" fill="currentColor"/><path class="on" d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><path class="off" d="m17 9 5 6m0-6-5 6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'
I_REPLAY = '<svg class="ic" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M4 12a8 8 0 1 0 2.6-5.9M4 4v4.5h4.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_STOP = '<svg class="ic" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect x="6" y="6" width="12" height="12" rx="2.5" fill="currentColor"/></svg>'
I_SEND = '<svg class="ic" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M12 19V5m-6 6 6-6 6 6" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_CLOSE = '<svg class="ic" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/></svg>'

APP = f'''<div class="smx" id="sm" data-state="landing">
    <div class="sm-stage buddy" id="buddy" data-buddy="{FIRST['id']}">
      <div class="buddy-stage" id="buddyStage"><div class="buddy-fallback">
{PICTURES}
      </div></div>
      <div class="sm-top">
        <button class="sm-pill sm-menu" id="smMenu" type="button" aria-haspopup="dialog" aria-controls="smSheet" aria-expanded="false">{I_MENU}<span class="sm-menu-t"><small>Scene</small><b id="missionTitle"></b></span></button>
        <button class="sm-pill sm-swap" id="buddySwitch" type="button" aria-label="Switch Buddy"{SWITCH_HIDDEN}><span class="bs-faces" aria-hidden="true">{SWITCH_FACES}</span>{I_SWAP}<span>Switch Buddy</span></button>
        <button class="sm-pill sm-ic" id="buddyMute" type="button" aria-pressed="true" aria-label="Buddy sounds" title="Buddy sounds">{I_SOUND}</button>
      </div>
      <div class="sm-over" id="smOver">
        <div class="sm-landing" id="smLanding">
          <p class="sm-who"><b id="buddyName">{FIRST['name']}</b><span id="buddyFrom">{FIRST['from']}</span></p>
          <button class="key hl big" id="smStart" type="button">Start talking</button>
          <p class="sm-tip">Listen, then answer out loud.</p>
        </div>
        <div class="sm-card" id="smCard" hidden></div>
        <div class="hint" id="hint" hidden></div>
        <div class="sm-done" id="smDone" hidden></div>
        <div class="sm-sub" id="smSub" hidden>
          <p class="sm-sub-h"><b id="smSpeaker">{FIRST['name']}</b><span class="sm-turn" id="smTurn"></span></p>
          <div class="sm-sub-b"><p id="smLine" aria-live="polite"></p><div class="sm-ctl"><button class="sm-replay sm-stop" id="smStop" type="button" aria-label="Stop speaking" hidden>{I_STOP}</button><button class="sm-replay" id="smReplay" type="button" aria-label="Hear it again">{I_REPLAY}</button></div></div>
        </div>
      </div>
      <pre class="sm-fps" id="smFps" hidden></pre>
      <p class="sr-only" id="buddyLive" aria-live="polite"></p>
    </div>
    <div class="sm-thread" id="smThread"></div>
    <div class="sm-sheet" id="smSheet" role="dialog" aria-label="Scene, accent and conversation">
      <div class="sm-sheet-head"><span class="sm-grab" aria-hidden="true"></span><h2>Scene and settings</h2><button class="sm-pill sm-ic" id="smClose" type="button" aria-label="Close">{I_CLOSE}</button></div>
      <div class="sm-sheet-body">
        <section class="sm-g sm-g-scene"><h3>Scene <span class="tag live ai-only">AI tutor live</span></h3><div class="chips" id="missions"></div></section>
        <section class="sm-g sm-g-chat"><h3>Conversation</h3><div class="chat" id="chat" role="log" aria-label="Conversation"></div>
          <div class="row"><button class="key sm" id="restartBtn" type="button"></button></div></section>
        <div class="sm-g2"><section class="sm-g sm-g-accent"><h3>Accent</h3><div class="chips" data-accents></div><p class="small muted" data-voicenote></p>
          <div class="sm-togs"><label class="tog"><input type="checkbox" id="speakAloud" checked> Read tutor lines aloud</label>
          <label class="tog"><input type="checkbox" id="buddyShow" checked> Show the Buddy</label>
          <label class="tog"><input type="checkbox" id="smSubs" checked> Show subtitles</label></div>
          <h3 class="sm-h3b">Speaking pace</h3><div class="chips" id="smPace"><button type="button" class="chip" data-pace="normal" aria-pressed="true">Normal</button><button type="button" class="chip" data-pace="slow" aria-pressed="false">Slow</button></div></section>
        <section class="sm-g sm-g-tally"><h3>This session</h3><div class="tally"><div><b class="num" id="sSent">0</b><span>sentences</span></div><div><b class="num" id="sFix">0</b><span>fixes</span></div><div><b class="num" id="sHelp">0</b><span>hints used</span></div></div></section></div>
        <nav class="sm-more" aria-label="More practice"><a href="/games/">Games</a><a href="/shadowing/">Shadowing</a><a href="/7-day-sprint/">7-Day Sprint</a><a href="/course/">Course</a><a href="/">Home</a></nav>
      </div>
    </div>
    <form class="composer sm-bar" id="composer" autocomplete="off">
      <button class="key round mic-only" id="speakMic" type="button" aria-label="Speak your answer"></button>
      <div class="sm-field"><textarea class="field" id="speakInput" rows="1" enterkeyhint="send" autocapitalize="sentences" spellcheck="true" placeholder="Type your answer in English" aria-label="Your answer"></textarea>
        <button class="key primary" id="speakSend" type="submit"><span class="sm-send-t">Send</span>{I_SEND}</button></div>
      <button class="sm-help" id="helpBtn" type="button"></button>
    </form>
    <div class="sm-scrim" id="smScrim" hidden></div>
  </div>
'''


def script(ver):
    return '''<script>
/* Speech Mode screen: which Buddy is on stage, the subtitle, the cards over the stage, the bottom sheet and the keyboard layout.
   Works with or without the 3D (buddies.js), which is loaded after the first paint. */
(function () {
  var sm = document.getElementById('sm'), w = document.getElementById('buddy'); if (!sm || !w) return;
  var NAME = __NAME__, FROM = __FROM__, GENDER = __GENDER__, IDS = __IDS__;   // from buddy_roster.py
  var $ = function (id) { return document.getElementById(id); }, root = document.documentElement;
  var fire = function (n, d) { window.dispatchEvent(new CustomEvent('w2s:' + n, {detail: d || {}})); };
  var phoneMq = window.matchMedia('(max-width: 899px)'), isPhone = function () { return phoneMq.matches; };
  var loaded = false, lock = 0, cur = '', temp = false, speaking = false, state = 'landing', mic = false, turnT = 0, cardT = 0;

  /* ---- Buddy: choice, switch, sounds, show or hide ---- */
  function load3d() {
    if (loaded || w.classList.contains('is-hidden')) return; loaded = true;
    var s = document.createElement('script'); s.type = 'module'; s.src = '/assets/buddies.js?v=__VER__'; s.onerror = function () { var r = document.createElement('script'); r.type = 'module'; r.src = s.src.split('?')[0] + '?retry=' + Date.now(); r.onerror = function () { w.classList.add('no-3d'); }; document.head.appendChild(r); };   // one retry under a fresh URL
    document.head.appendChild(s);
  }
  function nextBuddy(id) { return IDS[(IDS.indexOf(id) + 1) % IDS.length]; }
  function setBuddy(id, announce) {
    w.dataset.buddy = id; window.W2S_BUDDY = id; window.W2S_BUDDY_GENDER = GENDER[id];
    $('buddyName').textContent = NAME[id]; $('buddyFrom').textContent = FROM[id]; $('smSpeaker').textContent = NAME[id];
    var nx = nextBuddy(id), sw = $('buddySwitch'); sw.dataset.next = nx; sw.setAttribute('aria-label', 'Switch Buddy to ' + NAME[nx]); sw.title = 'Switch to ' + NAME[nx];
    if (announce) { $('buddyLive').textContent = NAME[id] + ' is your Buddy now'; fire('buddy', {id: id, gender: GENDER[id]}); }
  }
  function setMute(on) { var b = $('buddyMute'); b.setAttribute('aria-pressed', String(!on)); b.setAttribute('aria-label', on ? 'Buddy sounds are off' : 'Buddy sounds are on'); b.classList.toggle('is-off', on); }
  function setShown(on) { w.classList.toggle('is-hidden', !on); $('buddyShow').checked = on; if (on) load3d(); }

  /* ---- layout: one screen on a phone, and the keyboard ---- */
  var vv = window.visualViewport, maxH = 0, lastW = 0;
  function fit() {
    var h = vv ? vv.height : window.innerHeight, wd = window.innerWidth;
    if (wd !== lastW) { lastW = wd; maxH = 0; } if (h > maxH) maxH = h;
    var nav = document.querySelector('.nav'); root.style.setProperty('--smtop', (nav ? nav.offsetHeight : 48) + 'px');
    var kb = isPhone() && document.activeElement === $('speakInput') && h < maxH - 120;
    // the visible area is only written while typing (it pins the app above the keyboard); otherwise Safari's toolbar
    // sliding in and out would restyle the page on every scroll event
    if (kb) { var vh_ = Math.round(h) + 'px', vt_ = Math.round(vv ? vv.offsetTop : 0) + 'px'; if (root.style.getPropertyValue('--vvh') !== vh_) root.style.setProperty('--vvh', vh_); if (root.style.getPropertyValue('--vvtop') !== vt_) root.style.setProperty('--vvtop', vt_); }
    // while typing on a phone the app is pinned to the visible area above the keyboard (iOS scrolls the
    // page under the keyboard otherwise); when the keyboard closes, the page goes back to the top
    if (kb !== sm.classList.contains('kb')) { sm.classList.toggle('kb', kb); fire('layout', {kb: kb}); if (!kb && window.scrollY) window.scrollTo(0, 0); if (kb) follow(true); }
    $('smSheet').inert = isPhone() && !sm.classList.contains('sheet-open');
    $('speakInput').placeholder = isPhone() ? (root.classList.contains('has-mic') ? 'Or type it' : 'Type your answer') : 'Type your answer in English';
  }

  /* ---- phones: the conversation is the main view, under a smaller stage ----
     The chat log and the cards that sit over the stage on large screens move into the thread;
     the newest tutor line shows once, as the live bubble with its word highlighting. */
  var homeChat = null, homeOver = null;
  function place() {
    var th = $('smThread'), chat = $('chat'), over = $('smOver');
    if (!homeChat) { homeChat = [chat.parentNode, chat.nextSibling]; homeOver = [over.parentNode, over.nextSibling]; }
    if (isPhone()) { if (chat.parentNode !== th) { th.appendChild(chat); th.appendChild(over); } }
    else if (chat.parentNode === th) { homeChat[0].insertBefore(chat, homeChat[1]); homeOver[0].insertBefore(over, homeOver[1]); }
    live(); follow(true);
  }
  function live() {
    var ms = $('chat').querySelectorAll('.msg'), last = ms[ms.length - 1], lastT = null;
    for (var i = ms.length - 1; i >= 0; i--) if (ms[i].classList.contains('t') && !ms[i].querySelector('.typing')) { lastT = ms[i]; break; }
    [].forEach.call($('chat').querySelectorAll('.msg.is-live'), function (m) { if (m !== lastT) m.classList.remove('is-live'); });
    if (lastT) lastT.classList.add('is-live');
    // until the Buddy answers, the thread ends with your reply (the old line would sit below it)
    sm.classList.toggle('awaiting', !!last && last !== lastT);
  }
  var stick = true;
  function follow(force) { var th = $('smThread'); if (!isPhone()) return; if (force || stick) requestAnimationFrame(function () { th.scrollTop = th.scrollHeight; }); }

  /* ---- bottom sheet ---- */
  function sheet(on) {
    if (!isPhone()) { if (on) { var c = $('missions').querySelector('[aria-pressed="true"]') || $('missions').querySelector('button'); if (c) c.focus(); } return; }
    sm.classList.toggle('sheet-open', on); $('smScrim').hidden = !on; $('smMenu').setAttribute('aria-expanded', String(on)); $('smSheet').inert = !on;
    if (on) { $('chat').scrollTop = $('chat').scrollHeight; $('smClose').focus(); } else $('smMenu').focus();
  }

  /* ---- subtitle ---- */
  function line(text) {
    var p = $('smLine'); p.textContent = '';
    String(text).split(/\\s+/).filter(Boolean).forEach(function (wd) { var s = document.createElement('span'); s.className = 'w'; s.textContent = wd; p.appendChild(s); p.appendChild(document.createTextNode(' ')); });
    $('smSub').hidden = !text;
  }
  function mark(i) { var ws = $('smLine').children; for (var k = 0; k < ws.length; k++) { ws[k].classList.toggle('on', k === i); ws[k].classList.toggle('said', i >= 0 && k < i); } }
  function turnText() { $('smTurn').textContent = mic ? 'Listening' : state === 'turn' ? 'Your turn' : state === 'speaking' && speaking ? 'Speaking' : ''; sm.dataset.mic = mic ? 'on' : 'off'; }
  function set(s) { state = s; sm.dataset.state = s; turnText(); }
  function voice(v) { sm.dataset.voice = v; var m = $('speakMic'); if (m) m.setAttribute('aria-label', {listening: 'Stop and send what you said', speaking: 'Interrupt and answer', processing: 'Working on what you said', error: 'Microphone unavailable', ready: 'Speak your answer'}[v] || 'Speak your answer'); }

  /* ---- cards over the lower stage ---- */
  function hideCard() { clearTimeout(cardT); $('smCard').hidden = true; }
  function card(nodes, kind) {
    var c = $('smCard'), body = document.createElement('div'); c.textContent = ''; c.className = 'sm-card ' + kind; body.className = 'sm-card-b';
    nodes.forEach(function (n) { body.appendChild(n); }); c.appendChild(body);
    var x = document.createElement('button'); x.type = 'button'; x.className = 'sm-x'; x.textContent = 'Got it'; x.addEventListener('click', hideCard); c.appendChild(x);
    c.hidden = false; clearTimeout(cardT); if (kind === 'note') cardT = setTimeout(hideCard, 6000);
  }
  function done(d) {
    var n = function (id) { return ($(id).textContent || '0').trim(); }, c = $('smDone');
    c.innerHTML = '<p class="sm-done-k">Scene complete</p><h3>Nice work. You kept talking.</h3><p class="sm-stats"><span><b>' + n('sSent') + '</b> sentences</span><span><b>' + n('sFix') + '</b> fixes</span><span><b>' + n('sHelp') + '</b> hints</span>' + (d && d.bonus ? '<span class="xp"><b>+' + (+d.bonus) + '</b> XP</span>' : '') + '</p><div class="sm-done-a"><button type="button" class="key hl" data-again>Play again</button><button type="button" class="key" data-next>Next scene</button></div>';
    var one = {sentences: 'sentence', fixes: 'fix', hints: 'hint', frases: 'frase', correcciones: 'corrección', pistas: 'pista'};
    Array.prototype.forEach.call(c.querySelectorAll('.sm-stats span'), function (sp) { var b = sp.querySelector('b'), t = sp.lastChild;
      if (b && t && t.nodeType === 3 && b.textContent.trim() === '1') t.textContent = t.textContent.replace(/[a-zñóé]+/i, function (w) { return one[w] || w; }); });
    c.hidden = false; hideCard(); set('done');
  }

  function watchChat() {
    var th = $('smThread');
    th.addEventListener('scroll', function () { stick = th.scrollHeight - th.scrollTop - th.clientHeight < 60; }, {passive: true});
    new MutationObserver(function () { live(); follow(); }).observe(th, {childList: true, subtree: true, attributes: true, attributeFilter: ['hidden']});
    new MutationObserver(function (list) {
      var fixes = [];
      if (list.some(function (m) { return m.removedNodes.length; })) { $('smDone').hidden = true; hideCard(); if (state === 'done') set('speaking'); }   // the scene was restarted
      list.forEach(function (m) {
        m.addedNodes.forEach(function (n) {
          if (n.nodeType !== 1) return; var cl = n.classList;
          if (cl.contains('msg') && cl.contains('t')) {
            if (n.querySelector('.typing')) return;
            cur = n.textContent.trim(); if (!temp) line(cur);
            if (state !== 'landing' && state !== 'done') { set('speaking'); clearTimeout(turnT); turnT = setTimeout(function () { if (!speaking && state === 'speaking') set('turn'); }, 450); }
          } else if (cl.contains('msg') && cl.contains('me')) { hideCard(); stick = true; }
          else if (cl.contains('fix')) { fixes.push(n); }
          else if (cl.contains('msg') && cl.contains('sys') && !/^Scene complete/.test(n.textContent)) { var p = document.createElement('span'); p.textContent = n.textContent; card([p], 'note'); }
        });
      });
      if (fixes.length && !isPhone()) { var f = fixes[0].cloneNode(true); f.className = 'sm-fix'; var k = [f]; if (fixes.length > 1) { var more = document.createElement('span'); more.className = 'small muted'; more.textContent = 'One more fix is in your conversation.'; k.push(more); } card(k, 'fix'); }
    }).observe($('chat'), {childList: true});
  }

  function init() {
    voice('ready');
    var ta = $('speakInput'), lastVal = null;
    function grow() { if (ta.value === lastVal) return; lastVal = ta.value; ta.style.height = 'auto'; ta.style.height = Math.min(ta.scrollHeight + 2, parseFloat(getComputedStyle(ta).maxHeight) || 140) + 'px'; }
    ta.addEventListener('input', grow); setInterval(grow, 250);   // also catches text set by the microphone or the word bank
    ta.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); var f = $('composer'); if (f.requestSubmit) f.requestSubmit(); else f.dispatchEvent(new Event('submit', {cancelable: true})); } });
    setBuddy(IDS.indexOf(window.W2S_BUDDY) >= 0 ? window.W2S_BUDDY : IDS[0], false);
    place(); if (phoneMq.addEventListener) phoneMq.addEventListener('change', function () { place(); fit(); }); else phoneMq.addListener(function () { place(); fit(); });
    var muted = false, hidden = false; try { muted = localStorage.getItem('w2s.buddyMute') === '1'; hidden = localStorage.getItem('w2s.buddyHidden') === '1'; } catch (e) {}
    setMute(muted); setShown(!hidden);
    // one tap: the next Buddy comes in at once (the 3D stage spins the old one out and pops the new one in)
    $('buddySwitch').addEventListener('click', function () { var b = $('buddySwitch'), t = Date.now(); if (t - lock < 250) return; lock = t;
      b.classList.remove('is-swapping'); void b.offsetWidth; b.classList.add('is-swapping'); setBuddy(nextBuddy(w.dataset.buddy), true); });
    $('buddySwitch').addEventListener('animationend', function () { $('buddySwitch').classList.remove('is-swapping'); });
    $('buddyMute').addEventListener('click', function () { var on = !$('buddyMute').classList.contains('is-off'); setMute(on); try { localStorage.setItem('w2s.buddyMute', on ? '1' : '0'); } catch (e) {} fire('mute', {on: on}); });
    $('buddyShow').addEventListener('change', function () { var on = $('buddyShow').checked; setShown(on); try { localStorage.setItem('w2s.buddyHidden', on ? '0' : '1'); } catch (e) {} fire('shown', {on: on}); });
    $('smMenu').addEventListener('click', function () { sheet(!sm.classList.contains('sheet-open')); });
    $('smClose').addEventListener('click', function () { sheet(false); }); $('smScrim').addEventListener('click', function () { sheet(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && sm.classList.contains('sheet-open')) sheet(false); });
    $('missions').addEventListener('click', function (e) { if (e.target.closest('[data-mission]') && sm.classList.contains('sheet-open')) sheet(false); });
    $('smStart').addEventListener('click', function () { window.W2S_HOLD = 0; set('speaking'); fire('start'); clearTimeout(turnT); turnT = setTimeout(function () { if (!speaking && state === 'speaking') set('turn'); }, 600); });
    $('smReplay').addEventListener('click', function () { fire('replay'); });
    $('smStop').addEventListener('click', function () { fire('stop'); });
    var pref = function (k, d) { try { var v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } }, keep = function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} };
    function setPace(v) { window.W2S_PACE = v; [].forEach.call($('smPace').querySelectorAll('[data-pace]'), function (b) { b.setAttribute('aria-pressed', String(b.dataset.pace === v)); }); }
    setPace(pref('w2s.pace', 'normal')); $('smPace').addEventListener('click', function (e) { var b = e.target.closest('[data-pace]'); if (!b) return; setPace(b.dataset.pace); keep('w2s.pace', b.dataset.pace); });
    function setSubs(on) { sm.classList.toggle('no-subs', !on); $('smSubs').checked = on; }
    setSubs(pref('w2s.subs', '1') === '1'); $('smSubs').addEventListener('change', function () { setSubs($('smSubs').checked); keep('w2s.subs', $('smSubs').checked ? '1' : '0'); });
    // the microphone never invents a transcript: an empty result or a refusal gets a clear way forward
    var MICMSG = {not_granted: 'The microphone is blocked for this site. Allow it in your browser\u2019s site settings, then reload. You can keep typing below.', unavailable: 'Speech recognition is not available in this browser. Type your answer below.', no_mic: 'No microphone was found. Type your answer below.', network: 'Speech recognition did not work this time. It does not count as a mistake. Try again, or type it.', silence: 'I did not hear anything. Move a little closer to the microphone and try again, or type it.'};
    window.addEventListener('w2s:micempty', function (e) { var r = e.detail && e.detail.reason || ''; voice(MICMSG[r] ? 'error' : 'ready'); var t = document.createElement('span'); t.textContent = MICMSG[r] || 'I didn\u2019t catch that. Try again, a little closer to the microphone, or type it.'; var k = [t];
      if (!MICMSG[r]) { var again = document.createElement('button'); again.type = 'button'; again.className = 'key sm sm-again'; again.textContent = 'Try again'; again.addEventListener('click', function () { hideCard(); $('speakMic').click(); }); k.push(again); }
      card(k, MICMSG[r] ? 'fix' : 'note'); });
    window.addEventListener('w2s:micresult', function () { voice('processing'); setTimeout(function () { if (sm.dataset.voice === 'processing') voice('ready'); }, 1200); });
    window.addEventListener('w2s:speakstart', function () { voice('speaking'); $('smStop').hidden = false; $('smSub').classList.add('approx'); });
    window.addEventListener('w2s:timing', function (e) { if (e.detail && e.detail.exact) $('smSub').classList.remove('approx'); });
    $('smDone').addEventListener('click', function (e) {
      if (e.target.closest('[data-again]')) { fire('start'); }
      else if (e.target.closest('[data-next]')) { var all = [].slice.call($('missions').querySelectorAll('[data-mission]')).filter(function (b) { return b.offsetParent !== null || isPhone(); }).filter(function (b) { return !b.classList.contains('ai-only') || root.classList.contains('has-ai'); }); var i = all.findIndex(function (b) { return b.getAttribute('aria-pressed') === 'true'; }); (all[(i + 1) % all.length] || all[0]).click(); }
    });
    window.addEventListener('w2s:speak', function (e) { speaking = true; var t = e.detail && e.detail.text || ''; if (t && t !== cur) { temp = true; line(t); } else if (temp) { temp = false; line(cur); } if (state === 'turn') set('speaking'); else turnText(); });
    window.addEventListener('w2s:word', function (e) { mark(e.detail ? e.detail.i : -1); });
    window.addEventListener('w2s:speakend', function () { $('smStop').hidden = true; if (sm.dataset.voice === 'speaking') voice('ready'); if (!speaking) return; speaking = false; mark(-1); if (temp) { temp = false; line(cur); } if (state === 'speaking') set('turn'); else turnText(); });
    window.addEventListener('w2s:mic', function (e) { mic = !!(e.detail && e.detail.on); if (mic) voice('listening'); else if (sm.dataset.voice === 'listening') voice('ready'); turnText(); });
    window.addEventListener('w2s:done', function (e) { done(e.detail); });
    watchChat(); var first = $('chat').querySelector('.msg.t:last-of-type'); if (first) { cur = first.textContent.trim(); line(cur); }
    fit(); if (vv) { vv.addEventListener('resize', fit); vv.addEventListener('scroll', fit); } window.addEventListener('resize', fit); window.addEventListener('orientationchange', fit);
    $('speakInput').addEventListener('focus', function () { if (state === 'landing') $('smStart').click(); setTimeout(fit, 60); setTimeout(fit, 350); });   // typing first starts the scene $('speakInput').addEventListener('blur', function () { setTimeout(fit, 60); });
    if (phoneMq.addEventListener) phoneMq.addEventListener('change', function () { sm.classList.remove('sheet-open'); $('smScrim').hidden = true; fit(); });
    var go = function () { if ('requestIdleCallback' in window) requestIdleCallback(load3d, {timeout: 1500}); else setTimeout(load3d, 300); };
    if (document.readyState === 'complete') go(); else window.addEventListener('load', go);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
</script>
'''.replace('__VER__', ver).replace('__NAME__', json.dumps(NAMES)).replace('__FROM__', json.dumps({b['id']: b['from'] for b in ROSTER})) \
       .replace('__GENDER__', json.dumps({b['id']: b['gender'] for b in ROSTER})).replace('__IDS__', json.dumps([b['id'] for b in ACTIVE]))


CSS = '''
/* ================= Speech Mode: the Buddy is the interface ================= */
:root{--s1:4px;--s2:8px;--s3:12px;--s4:16px;--s5:24px;--s6:32px;--e1:0 1px 2px rgba(11,16,58,.10),0 4px 14px rgba(11,16,58,.10);--e2:0 2px 4px rgba(11,16,58,.12),0 14px 38px rgba(11,16,58,.20);--spring:cubic-bezier(.2,.9,.25,1.12)}
body[data-page="speak"] .view{display:flex;flex-direction:column;padding-bottom:0}
body[data-page="speak"] .vh{order:2;margin-bottom:0}
.smx{position:relative;display:grid;gap:var(--s4);grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);grid-template-rows:minmax(0,1fr) auto;grid-template-areas:"stage sheet" "bar bar";height:calc(100vh - var(--smtop,72px) - 40px);height:calc(100dvh - var(--smtop,72px) - 40px);min-height:540px;max-height:940px;margin-block:20px}
.sm-stage{grid-area:stage;position:relative;min-height:0;overflow:hidden;border-radius:28px;isolation:isolate;background:radial-gradient(60% 46% at 50% 44%,rgba(255,255,255,.95) 0,rgba(255,255,255,0) 100%),radial-gradient(120% 70% at 50% 112%,#93A6FF 0,#C6D0FF 46%,#EDF0FF 100%);box-shadow:var(--e1)}
.sm-stage[data-buddy="rio"]{background:radial-gradient(60% 46% at 50% 44%,rgba(255,255,255,.95) 0,rgba(255,255,255,0) 100%),radial-gradient(120% 70% at 50% 112%,#FFD93B 0,#FFE98F 40%,#FFF7D9 100%)}
.buddy-stage{position:absolute;inset:0;touch-action:pan-y;user-select:none;-webkit-user-select:none}
.buddy-canvas{position:absolute;inset:0;width:100%;height:100%;display:block;cursor:grab;outline:0;opacity:0;transition:opacity .35s}
.buddy.is-3d .buddy-canvas{opacity:1}
.buddy-canvas.grabbing{cursor:grabbing}
.buddy-canvas:focus-visible{box-shadow:inset 0 0 0 4px var(--hl)}
.buddy-fallback{position:absolute;inset:0;transition:opacity .35s}
.buddy-fallback .bf{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 0;display:none}
__BF_SHOW__{display:block}
.buddy.is-3d .buddy-fallback{opacity:0;pointer-events:none}
.sm-pill[hidden]{display:none}
.sm-swap{padding-left:6px}
.bs-faces{position:relative;width:30px;height:30px;flex:none;border-radius:50%;overflow:hidden;background:linear-gradient(#EDF0FF,#C6D0FF);box-shadow:0 0 0 2px #fff,0 0 0 3.5px rgba(45,75,255,.25)}
.bs-face{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 46%;transform:scale(2.1);display:none}
__BS_SHOW__{display:block}
.sm-swap .ic{transition:transform .35s var(--spring)}
.sm-swap:hover .ic{transform:rotate(180deg)}
.sm-swap.is-swapping .bs-faces{animation:bsPop .42s var(--spring)}
.sm-swap.is-swapping .ic{transform:rotate(180deg)}
@keyframes bsPop{0%{transform:scale(.4) rotate(-40deg);opacity:0}100%{transform:none;opacity:1}}
/* without 3D, the picture swaps with a small pop */
.buddy-fallback .bf{animation:bfIn .38s var(--spring)}
@keyframes bfIn{from{transform:scale(.92) translateY(10px);opacity:.2}to{transform:none;opacity:1}}
@media (prefers-reduced-motion: reduce){.sm-swap.is-swapping .bs-faces,.buddy-fallback .bf{animation:none}}
.buddy.is-hidden .buddy-stage{display:none}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}

.sm-top{position:absolute;z-index:3;top:var(--s2);left:var(--s2);right:var(--s2);display:flex;gap:6px;align-items:center;pointer-events:none}
.sm-top>*{pointer-events:auto}
.sm-pill{display:inline-flex;align-items:center;gap:6px;min-height:44px;padding:0 14px;border:0;border-radius:999px;background:rgba(255,255,255,.92);color:var(--ink);font:700 .9rem/1.1 var(--f-body);cursor:pointer;box-shadow:var(--e1);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);transition:transform .25s var(--spring),background .15s;white-space:nowrap}
.sm-pill:hover{background:#fff}
.sm-pill:active{transform:scale(.94)}
.sm-pill:focus-visible,.sm-replay:focus-visible,.sm-help:focus-visible,.sm-x:focus-visible,.sm-more a:focus-visible{outline:3px solid var(--ink);outline-offset:2px}
.sm-pill.sm-ic{width:44px;padding:0;justify-content:center;flex:none}
.sm-menu{margin-right:auto;min-width:0;padding-left:12px}
.sm-menu-t{display:grid;text-align:left;min-width:0}
.sm-menu-t small{font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2);line-height:1.1}
.sm-menu-t b{font-size:.94rem;line-height:1.15;overflow:hidden;text-overflow:ellipsis}
#buddyMute .off{display:none}
#buddyMute.is-off .on{display:none}
#buddyMute.is-off .off{display:block}
#buddyMute.is-off{color:var(--ink-2)}

.sm-over{position:absolute;z-index:3;left:0;right:0;bottom:0;display:grid;gap:var(--s2);padding:var(--s3);max-height:calc(100% - var(--sm-chin,250px));min-height:120px;overflow:auto;overscroll-behavior:contain;pointer-events:none;scrollbar-width:none}
.sm-over::-webkit-scrollbar{display:none}
.sm-over>*{pointer-events:auto;animation:smUp .45s var(--spring) both}
.sm-over>[hidden]{display:none}
@keyframes smUp{from{opacity:0;transform:translateY(14px) scale(.98)}to{opacity:1;transform:none}}
.sm-landing{display:grid;justify-items:center;gap:var(--s3);padding:var(--s2) 0 var(--s3);text-align:center}
.sm-who{display:inline-flex;align-items:baseline;gap:8px;margin:0;padding:8px 16px;border-radius:999px;background:rgba(255,255,255,.92);box-shadow:var(--e1)}
.sm-who b{font:800 1.25rem/1 var(--f-display);letter-spacing:-.01em}
.sm-who span{font-size:.92rem;font-weight:600;color:var(--ink-2)}
#smStart{min-width:min(280px,82%);min-height:60px;font-size:1.2rem}
.sm-tip{margin:0;font-size:.95rem;font-weight:600;color:var(--ink);text-shadow:0 1px 0 rgba(255,255,255,.6)}
.smx[data-state="landing"] .sm-sub,.smx:not([data-state="landing"]) .sm-landing{display:none}
.sm-sub{background:rgba(11,16,58,.9);color:#fff;border-radius:20px;padding:10px 10px 12px 16px;box-shadow:var(--e2);display:grid;gap:2px}
.sm-sub-h{display:flex;align-items:center;gap:10px;margin:0;font-size:.74rem;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--hl)}
.sm-turn{font-weight:700;letter-spacing:.04em;color:#C9D0FF;display:inline-flex;align-items:center;gap:6px}
.sm-turn:empty{display:none}
.sm-turn::before{content:"";width:8px;height:8px;border-radius:50%;background:currentColor}
.smx[data-state="turn"] .sm-turn{color:#7CF0C5}
.smx[data-mic="on"] .sm-turn{color:#FF9A9A}
.smx[data-mic="on"] .sm-turn::before{animation:smPulse 1s ease-in-out infinite}
@keyframes smPulse{50%{transform:scale(1.7);opacity:.5}}
.sm-sub-b{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:var(--s2);align-items:center}
#smLine{margin:0;font:600 1.1rem/1.4 var(--f-body);word-spacing:.14em;overflow-wrap:anywhere}
#smLine .w{border-radius:5px;transition:background .12s,color .12s,box-shadow .12s}
#smLine .w.on{background:var(--hl);color:var(--ink);box-shadow:0 0 0 2px var(--hl)}
.sm-replay{width:44px;height:44px;flex:none;display:grid;place-items:center;border:0;border-radius:50%;background:rgba(255,255,255,.16);color:#fff;cursor:pointer;transition:transform .25s var(--spring),background .15s}
.sm-replay:hover{background:rgba(255,255,255,.28)}
.sm-replay:active{transform:scale(.9) rotate(-40deg)}
.sm-ctl{display:flex;gap:6px}.sm-stop:active{transform:scale(.9)}
.sm-sub{animation:smSubIn .28s var(--spring)}@keyframes smSubIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
/* estimated timing: words fill in gently instead of claiming word-exact highlighting */
.sm-sub.approx #smLine .w.on{background:none;color:#fff;box-shadow:inset 0 -3px 0 rgba(255,217,59,.55)}
.smx.no-subs #smLine{display:none}.smx.no-subs .sm-sub-b{grid-template-columns:1fr auto}
.sm-h3b{margin-top:var(--s3)}
.sm-again{margin-left:var(--s2)}
/* the mic button shows what the conversation is doing */
.smx[data-voice="speaking"] #speakMic{box-shadow:0 0 0 4px rgba(45,75,255,.22)}
.smx[data-voice="processing"] #speakMic{opacity:.7}
.smx[data-voice="error"] #speakMic{filter:grayscale(1);opacity:.55}
#speakMic.listening{box-shadow:0 0 0 0 rgba(255,90,90,.5);animation:micPulse 1.3s ease-out infinite}
@keyframes micPulse{0%{box-shadow:0 0 0 0 rgba(255,90,90,.5)}100%{box-shadow:0 0 0 14px rgba(255,90,90,0)}}
@media (prefers-reduced-motion: reduce){.sm-sub{animation:none}#speakMic.listening{animation:none}}
.sm-card{background:color-mix(in srgb,var(--note) 8%,var(--surface));border:1px solid color-mix(in srgb,var(--note) 38%,transparent);border-radius:20px;padding:var(--s3) var(--s3) var(--s3) var(--s4);box-shadow:var(--e2);display:grid;grid-template-columns:minmax(0,1fr) auto;gap:var(--s3);align-items:center}
.sm-card.note{background:color-mix(in srgb,var(--cobalt) 7%,var(--surface));border-color:color-mix(in srgb,var(--cobalt) 30%,transparent)}
.sm-card-b{display:grid;gap:4px;font-size:1rem;line-height:1.35}
.sm-fix{display:grid;gap:3px}
.sm-fix b{color:var(--note);font-size:.8rem;letter-spacing:.06em;text-transform:uppercase}
.sm-fix span:first-of-type{font-weight:700}
.sm-x{min-height:44px;padding:0 14px;border:2px solid var(--line);border-radius:999px;background:var(--surface);color:var(--ink);font:700 .9rem var(--f-body);cursor:pointer;white-space:nowrap}
.sm-over .hint{background:color-mix(in srgb,var(--hl) 14%,var(--surface));border:1px solid color-mix(in srgb,var(--hl) 70%,transparent);box-shadow:var(--e2);border-radius:20px;padding:var(--s3) var(--s4)}
.sm-over .hint .lv{font-size:.8rem;letter-spacing:.06em;text-transform:uppercase}
.sm-over .hint .starter{margin:0;font-size:1.15rem}
.sm-over .wordbank button{min-height:44px;padding:8px 14px;font-size:1rem;background:var(--surface-2)}
.sm-done{background:var(--surface);border-radius:24px;padding:var(--s4);box-shadow:var(--e2);display:grid;gap:var(--s2);text-align:center}
.sm-done-k{margin:0;font-size:.78rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--brand-text)}
.sm-done h3{margin:0;font:800 1.45rem/1.1 var(--f-display);letter-spacing:-.02em}
.sm-stats{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 14px;margin:0;color:var(--ink-2);font-size:.95rem}
.sm-stats b{color:var(--ink);font:800 1.15rem var(--f-display)}
.sm-stats .xp{background:var(--hl);color:var(--ink);border-radius:999px;padding:0 10px}
.sm-done-a{display:flex;flex-wrap:wrap;gap:var(--s2);justify-content:center;margin-top:var(--s1)}
.sm-done-a .key{min-height:48px}
.sm-fps{position:absolute;z-index:4;left:var(--s2);top:60px;margin:0;padding:6px 10px;border-radius:10px;background:rgba(11,16,58,.86);color:#7CF0C5;font:600 12px/1.35 ui-monospace,Menlo,monospace;pointer-events:none;white-space:pre}

.sm-sheet{grid-area:sheet;min-height:0;display:flex;flex-direction:column;background:var(--surface);border-radius:28px;box-shadow:var(--e1);overflow:hidden}
.sm-sheet-head{display:none}
.sm-sheet-body{flex:1;min-height:0;display:flex;flex-direction:column;gap:var(--s4);padding:var(--s4) var(--s4) var(--s3);overflow:auto}
.sm-g{display:grid;gap:var(--s2);align-content:start}
.sm-g h3{margin:0;font:800 .78rem/1.2 var(--f-body);letter-spacing:.09em;text-transform:uppercase;color:var(--ink-2);display:flex;gap:8px;align-items:center}
.sm-g-chat{flex:1 1 0;min-height:210px;display:flex;flex-direction:column}
.sm-g-chat .chat{flex:1 1 0;min-height:0;max-height:none;overflow:auto;align-content:start;background:var(--ground);border-radius:16px;padding:var(--s3)}
.sm-g-chat .chat:empty::before{content:"Your conversation shows here.";color:var(--ink-2);font-size:.95rem}
.sm-g .chip{min-height:44px}
.sm-g .tog{min-height:44px;display:flex;align-items:center;gap:10px;font-weight:600}
.sm-g .tog input{width:22px;height:22px;accent-color:var(--cobalt)}
.sm-togs{display:flex;flex-wrap:wrap;gap:0 var(--s5)}
.sm-g2{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);gap:var(--s4)}
.sm-g2 .tally{gap:var(--s3) var(--s4)}
.sm-g [data-voicenote]{margin:0}
.sm-g [data-voicenote]:empty{display:none}
.sm-more{display:none}
.sm-scrim{display:none}
.sm-thread{display:none}

.sm-bar{grid-area:bar;display:flex;align-items:flex-end;gap:var(--s3);padding:var(--s3) var(--s4);background:var(--surface);border-radius:24px;box-shadow:var(--e1)}
.sm-bar #speakMic{flex:none;width:60px;height:60px;min-height:60px}
.sm-field{position:relative;flex:1;min-width:0;display:flex;gap:var(--s2)}
.sm-field .field{min-height:56px;font-size:1.1rem;line-height:1.4}
textarea.field{display:block;resize:none;overflow-y:auto;max-height:calc(1.4em * 3 + 28px);padding:14px 16px;font-family:inherit;field-sizing:content}
.sm-field #speakSend{flex:none;min-height:56px;min-width:96px}
.sm-field #speakSend .ic{display:none}
.sm-help{flex:none;display:inline-flex;align-items:center;justify-content:center;gap:5px;min-height:48px;min-width:96px;padding:0 14px;border:2px solid var(--line);border-radius:999px;background:var(--surface);color:var(--ink);font:700 .92rem/1 var(--f-body);cursor:pointer;white-space:nowrap;transition:transform .25s var(--spring),border-color .15s}
.sm-help:hover{border-color:var(--ink-2)}
.sm-help:active{transform:scale(.95)}
.sm-help[disabled]{opacity:.5;cursor:not-allowed}
.sm-help .ic{width:18px;height:18px;color:var(--note)}

@media (max-width:899px){
  body[data-page="speak"] .nav .tabs{display:none}
  body[data-page="speak"] .nav-in{min-height:0;height:48px;padding-block:0;align-items:center;grid-template-columns:minmax(0,1fr) auto auto;gap:8px}
  body[data-page="speak"] .nav .progress{display:none}
  .smx{grid-template-columns:minmax(0,1fr);grid-template-areas:"stage" "bar";gap:0;margin-block:0;margin-left:calc(-1 * max(16px,env(safe-area-inset-left,0px)));margin-right:calc(-1 * max(16px,env(safe-area-inset-right,0px)));min-height:0;max-height:none;height:calc(100vh - var(--smtop,48px));height:calc(100svh - var(--smtop,48px) - env(safe-area-inset-top,0px) - env(safe-area-inset-bottom,0px))}
  .sm-stage{border-radius:0;box-shadow:none}
  .sm-pill{padding:0 12px;font-size:.875rem}
  .sm-menu-t b{max-width:34vw;white-space:nowrap}
  /* one row: speak, type (send sits in the field), ask for help */
  .sm-bar{display:flex;align-items:flex-end;gap:8px;height:auto;padding:8px 10px;border-radius:0;box-shadow:none;border-top:1px solid var(--line);background:var(--surface)}
  .sm-bar #speakMic{width:52px;height:52px;min-height:52px}
  .smx.kb .sm-bar .sm-help{display:none}
  .sm-field .field{min-height:52px;font-size:1rem;line-height:1.35;padding:14px 50px 14px 14px;border-radius:16px;max-height:calc(1.35em * 3 + 28px)}
  .sm-field #speakSend{position:absolute;right:5px;bottom:5px;width:42px;height:42px;min-height:42px;min-width:42px;padding:0;border-radius:12px;box-shadow:none;transition:opacity .15s,transform .25s var(--spring)}
  .sm-field #speakSend:active{transform:scale(.92)}
  .sm-field #speakSend .ic{display:block}
  .sm-send-t{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
  .sm-field .field:placeholder-shown+#speakSend{opacity:0;pointer-events:none}
  .sm-help{min-width:0;min-height:52px;padding:0 12px;font-size:.88rem}
  .sm-sheet{position:fixed;z-index:60;left:0;right:0;bottom:0;max-height:86vh;max-height:86dvh;border-radius:28px 28px 0 0;box-shadow:0 -14px 44px rgba(11,16,58,.3);transform:translateY(104%);visibility:hidden;transition:transform .45s var(--spring),visibility 0s .45s;padding-bottom:env(safe-area-inset-bottom,0px)}
  .smx.sheet-open .sm-sheet{transform:none;visibility:visible;transition:transform .45s var(--spring),visibility 0s}
  .sm-sheet-head{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;padding:18px var(--s4) var(--s2);position:relative}
  .sm-sheet-head h2{margin:0;font:800 1.25rem/1.1 var(--f-display)}
  .sm-sheet-head .sm-pill{background:var(--surface-2);box-shadow:none}
  .sm-grab{position:absolute;top:8px;left:50%;width:44px;height:5px;margin-left:-22px;border-radius:99px;background:var(--line)}
  .sm-sheet-body{padding-top:var(--s2);gap:var(--s5)}
  .sm-g-chat{flex:none;min-height:0}
  .sm-g2{display:contents}
  .sm-g-chat .chat{flex:none;max-height:34vh}
  .sm-more{display:flex;flex-wrap:wrap;gap:var(--s2);padding-top:var(--s3);border-top:1px solid var(--line)}
  .sm-more a{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border-radius:999px;background:var(--surface-2);font-weight:700;text-decoration:none;color:var(--ink)!important}
  .sm-scrim{display:block;position:fixed;inset:0;z-index:59;background:rgba(11,16,58,.5);animation:smFade .25s both}
  .sm-scrim[hidden]{display:none}
  .smx.kb #speakMic{display:none!important}

  /* the conversation: a thread under a smaller stage */
  .smx{grid-template-rows:minmax(0,min(52%,470px)) minmax(0,1fr) auto;grid-template-areas:"stage" "thread" "bar"}
  .sm-thread{grid-area:thread;position:relative;z-index:4;display:flex;flex-direction:column;gap:10px;min-height:0;margin-top:-20px;padding:16px 14px 14px;overflow-y:auto;overscroll-behavior:contain;background:var(--surface);border-radius:22px 22px 0 0;box-shadow:0 -8px 22px -12px rgba(11,16,58,.28);scrollbar-width:none}
  .sm-thread::-webkit-scrollbar{display:none}
  .sm-thread .chat{display:grid;gap:8px;align-content:start;height:auto;min-height:0;max-height:none;margin:0;padding:0;border:0;overflow:visible;background:none}
  .smx[data-state="landing"] .sm-thread{justify-content:center}
  .sm-thread .chat:empty{display:none}
  .sm-thread .msg{max-width:86%;font-size:1rem;padding:10px 14px}
  .sm-thread .msg.t.is-live{display:none}
  .sm-thread .sm-over{position:static;display:grid;gap:10px;min-height:0;max-height:none;padding:0;overflow:visible;pointer-events:auto}
  .sm-thread .sm-landing{padding:4px 0 2px}
  .sm-thread .sm-tip{text-shadow:none;color:var(--ink-2)}
  .sm-thread .sm-sub{justify-self:start;max-width:92%;background:rgb(11,16,58);border-radius:20px 20px 20px 6px;padding:10px 8px 10px 14px;box-shadow:var(--e1)}
  .sm-thread #smLine{font-size:1.06rem}
  .sm-thread .sm-sub{order:-1}   /* the Buddy's line first, then help or a note about it */
  .smx.awaiting .sm-thread .sm-sub{display:none}
  .sm-thread .sm-card,.sm-thread .hint{box-shadow:none}
  .sm-thread .sm-done{box-shadow:none;border:1px solid var(--line)}
  .sm-g-chat>h3{display:none}
  /* typing: the stage folds away so the conversation and the field have the screen */
  .smx.kb{position:fixed;z-index:70;left:0;right:0;top:var(--vvtop,0px);height:var(--vvh,100dvh);margin:0;grid-template-rows:0 minmax(0,1fr) auto;background:var(--surface)}
  .smx.kb .sm-stage{visibility:hidden}
  .smx.kb .sm-thread{margin-top:0;border-radius:0;box-shadow:none;padding-top:10px}
}
@keyframes smFade{from{opacity:0}to{opacity:1}}
/* iOS Safari re-composites (flickers) elements with a backdrop blur that sit over a WebGL canvas; the pills are near-opaque anyway */
@media (pointer:coarse),(max-width:899px){.sm-pill{-webkit-backdrop-filter:none;backdrop-filter:none;background:#fff}}
@media (max-width:380px){.sm-swap .ic{display:none}.sm-top{gap:5px}}   /* narrow phones: the face says it; the scene name keeps its room */
@media (min-width:900px){
  .sm-g-tally .tally b{font-size:1.3rem}
  .sm-menu{cursor:default;box-shadow:var(--e1)}
  .sm-menu .ic{display:none}
  .sm-over{left:50%;right:auto;width:min(100%,620px);transform:translateX(-50%);padding:var(--s4)}
  #smLine{font-size:1.25rem}
}
@media (prefers-reduced-motion:reduce){
  .sm-over>*,.sm-scrim{animation:none}
  .sm-sheet,.smx.sheet-open .sm-sheet,.sm-pill,.sm-replay,.sm-help,#smLine .w,.buddy-canvas,.buddy-fallback{transition:none}
  .smx[data-mic="on"] .sm-turn::before{animation:none}
}
'''

CSS = CSS.replace('__BS_SHOW__', ','.join(f'#buddySwitch[data-next="{b["id"]}"] .bs-{b["id"]}' for b in ROSTER))
CSS = CSS.replace('__BF_SHOW__', ','.join(f'.buddy[data-buddy="{b["id"]}"] .bf-{b["id"]}' for b in ROSTER))
