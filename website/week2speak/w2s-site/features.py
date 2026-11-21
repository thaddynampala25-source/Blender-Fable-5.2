"""The pages that sell, run and support the paid 7-Day Sprint, written in Spanish and English directly.
account.js brings them to life (accounts, prices, the paid Sprint, the tutor area); the Worker in
../worker/index.js keeps the data. Paid content is not in these pages: it is /paid/sprint.<lang>.json."""
import json
import i18n as I
import sprint_content as SC
import sprint_paid as SP
import buddy_roster as BR

TITLES = {
    'sprint':  {'es': ('Sprint de 7 días: habla inglés en una semana | Week2Speak', 'Siete días, veinte minutos al día y una tutora que habla tu idioma. Para hispanohablantes que empiezan de cero y quieren decir sus primeras frases.'),
                'en': ('7-Day Sprint: speak English in a week | Week2Speak', 'Seven days, twenty minutes a day and a tutor who speaks your language. For Spanish speakers starting from zero who want to say their first sentences.')},
    'join':    {'es': ('Reserva tu plaza en el Sprint de 7 días | Week2Speak', 'Dos llamadas 1 a 1 con tu tutora, WhatsApp directo y acceso completo a Week2Speak durante tu semana. Plazas limitadas en la fase de prueba.'),
                'en': ('Book your place in the 7-Day Sprint | Week2Speak', 'Two 1-to-1 calls with your tutor, direct WhatsApp and full access to Week2Speak during your week. Limited places in the testing phase.')},
    'tutor':   {'es': ('Mei, tu tutora de inglés | Week2Speak', 'Conoce a Mei, la tutora del Sprint de 7 días: llamadas 1 a 1 y WhatsApp directo durante tu semana.'),
                'en': ('Mei, your English tutor | Week2Speak', 'Meet Mei, the tutor of the 7-Day Sprint: 1-to-1 calls and direct WhatsApp during your week.')},
    'terms':   {'es': ('Términos y condiciones | Week2Speak', 'Las condiciones del Sprint de 7 días de Week2Speak: qué incluye, pagos, reembolsos, cuentas y uso de la web.'),
                'en': ('Terms and conditions | Week2Speak', "The conditions of Week2Speak's 7-Day Sprint: what it includes, payment, refunds, accounts and use of the website.")},
    'account': {'es': ('Tu cuenta | Week2Speak', 'Entra en tu cuenta de Week2Speak o crea una gratis.'), 'en': ('Your account | Week2Speak', 'Sign in to your Week2Speak account or create one for free.')},
    'thanks':  {'es': ('¡Ya estás dentro! | Week2Speak', 'Tu plaza en el Sprint de 7 días está reservada.'), 'en': ("You're in! | Week2Speak", 'Your place in the 7-Day Sprint is booked.')},
}
PAGES = set(TITLES)

ICONS = {
    'check': '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    'lock': '<rect x="5" y="11" width="14" height="10" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    'chat': '<path d="M4 19.5 5.6 15A8 8 0 1 1 9 18.6Z"/><path d="M9 11h6M9 14h4"/>',
    'phone': '<path d="M6.5 4h3l1.5 4-2 1.5a11 11 0 0 0 5.5 5.5L16 13l4 1.5v3A2.5 2.5 0 0 1 17.5 20C10 20 4 14 4 6.5A2.5 2.5 0 0 1 6.5 4Z"/>',
    'calendar': '<rect x="4" y="5" width="16" height="15" rx="2.5"/><path d="M4 10h16M9 3v4M15 3v4"/>',
    'play': '<path d="M8 5.5v13l10.5-6.5Z"/>',
    'sound': '<path d="M4 10v4h4l5 4V6L8 10Z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4.5 20a7.5 7.5 0 0 1 15 0"/>',
    'life': '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3.5"/><path d="m6 6 3.5 3.5M18 6l-3.5 3.5M6 18l3.5-3.5M18 18l-3.5-3.5"/>',
    'warn': '<path d="M12 4 2.8 19.5h18.4Z"/><path d="M12 10v4.5M12 17.2v.3"/>',
    'spark': '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'mic': '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/>',
    'book': '<path d="M5 4.5h9a3 3 0 0 1 3 3V20H8a3 3 0 0 1-3-3Z"/><path d="M5 17a3 3 0 0 1 3-3h9"/>',
    'heart': '<path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7.3 4.3 4.3 0 0 1 19.5 10C19.5 15.4 12 20 12 20Z"/>',
    'gift': '<rect x="4" y="9" width="16" height="11" rx="2"/><path d="M4 13h16M12 9v11M12 9S10.5 4.5 8 5s-1 4 4 4c5 0 6.5-3.5 4-4s-4 4-4 4"/>',
    'star': '<path d="m12 3.5 2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.8-5.2 2.8 1-5.8-4.3-4.1 5.9-.9Z"/>',
    'whatsapp': '<path d="M4 20l1.3-4.2A8 8 0 1 1 8.4 19Z"/><path d="M9.2 8.8c.3 2.4 2.6 4.8 5.2 5.4l1.2-1.4-1.7-1-1 .8c-1-.4-1.9-1.3-2.3-2.3l.8-1-1-1.7Z"/>',
}


def ic(name, cls='ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


def picture(bid):
    b = next((x for x in BR.ACTIVE if x['id'] == bid), None)
    return f'/assets/buddies/{b["file"]}.webp' if b else ''


def L(lang):
    return lambda es, en: es if lang == 'es' else en


def tr(lang, s):
    return I.t(s, lang)


# ---------------------------------------------------------------- the offer (Join)
def join(lang):
    t = L(lang); A = I.SLUG[lang]
    incl = [
        ('phone', t('Dos llamadas 1 a 1 con Mei', 'Two 1-to-1 calls with Mei'), t('25 minutos cada una: la primera para arrancar, la última para tu charla de 2 minutos.', '25 minutes each: the first to get you going, the last for your 2-minute talk.')),
        ('whatsapp', t('WhatsApp directo con Mei', 'Direct WhatsApp with Mei'), t('Toda la semana. Le escribes cuando te atasques y te responde ella, no un robot.', 'All week. You message her when you get stuck and she answers, not a bot.')),
        ('spark', t('Todo Week2Speak, sin límites', 'All of Week2Speak, no limits'), t('Modo Habla, juegos, Imita y el curso completo, todo el tiempo que quieras.', 'Speech Mode, games, shadowing and the full course, as much as you like.')),
        ('book', t('El Sprint, día a día', 'The Sprint, day by day'), t('Cada día un objetivo, las frases, un error típico explicado y un reto real.', 'Every day a goal, the phrases, a typical mistake explained and a real-life challenge.')),
        ('mic', t('Tu antes y después', 'Your before and after'), t('Grabas tu Día 1 y tu Día 7. La diferencia se oye.', 'You record your Day 1 and your Day 7. You can hear the difference.')),
        ('gift', t('Biblioteca de recursos', 'Resource library'), t('Kit de supervivencia, pronunciación, plantillas y tu plan para después.', 'Survival kit, pronunciation, templates and your plan for afterwards.')),
    ]
    week = ''.join(f'<li><span class="fx-dn num">{i + 1}</span><span><b>{tr(lang, d["title"])}</b><small>{(DAY_ES.get(d["can"], tr(lang, d["can"])) if lang == "es" else d["can"])}</small></span></li>' for i, d in enumerate(SC.DAYS))
    faq = [
        (t('¿Necesito saber algo de inglés?', 'Do I need to know any English?'), t('No. El Sprint está pensado para empezar de cero. Si sabes decir «hello», ya tienes por dónde empezar.', 'No. The Sprint is made for starting from zero. If you can say "hello", you\'re ahead.')),
        (t('¿Cuánto tiempo al día?', 'How much time a day?'), t('Unos veinte minutos. Puedes hacerlo de una vez o en ratos sueltos.', 'About twenty minutes. In one go or in short bits.')),
        (t('¿Cómo son las llamadas con Mei?', 'What are the calls with Mei like?'), t('Por videollamada, 25 minutos, a la hora que reserves tú. La primera es para conoceros y arrancar; la última, para tu charla de 2 minutos.', 'Video call, 25 minutes, at a time you book. The first is to meet and get going; the last is for your 2-minute talk.')),
        (t('¿Y si un día no puedo?', "What if I can't one day?"), t('No pasa nada. El Sprint avanza contigo, no con el calendario: sigues donde lo dejaste.', "That's fine. The Sprint moves with you, not with the calendar: you pick up where you left off.")),
        (t('¿Puedo pedir un reembolso?', 'Can I get a refund?'), t('Completo si cancelas antes de tu primera llamada con Mei. Después, dentro de los 14 días, te devolvemos la parte que aún no has usado. No devolvemos dinero por el resultado: el Sprint te da el plan y a Mei, la práctica la pones tú. Lo tienes todo en los <a href="' + A['terms'] + '">términos</a>.', 'In full if you cancel before your first call with Mei. After that, within 14 days, we refund the part you have not used yet. We don\'t refund based on the outcome: the Sprint gives you the plan and Mei, the practice is yours. It\'s all in the <a href="' + A['terms'] + '">terms</a>.')),
    ]
    faq_html = ''.join(f'<details class="fx-q"><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    return f'''<section class="light fx" data-view="join"><div class="wrap view">
  <div class="fx-offer">
    <div class="fx-pitch">
      <h1 class="fx-h1">{t('Tu primera conversación en inglés, en 7 días.', 'Your first conversation in English, in 7 days.')}</h1>
      <p class="fx-lead">{t('Para hispanohablantes que empiezan de cero. Veinte minutos al día y una tutora de verdad a tu lado, para que dejes de pensar el inglés y empieces a decirlo.', 'For Spanish speakers starting from zero. Twenty minutes a day and a real tutor by your side, so you stop thinking English and start saying it.')}</p>
      <ul class="fx-incl">{''.join(f'<li>{ic(i)}<span><b>{h}</b>{p}</span></li>' for i, h, p in incl)}</ul>
    </div>
    <aside class="fx-buy" id="buyCard" aria-labelledby="buyTitle">
      <div class="fx-buy-top"><div><h2 id="buyTitle">{t('Sprint de 7 días', '7-Day Sprint')}</h2><p class="fx-places" id="placesLine"><span class="fx-dot" aria-hidden="true"></span><span id="placesText">{t('Plazas limitadas', 'Limited places')}</span></p></div></div>
      <div class="fx-price"><s id="pAnchor" aria-label="{t('Valor', 'Value')}"></s><b id="pAmount" class="num">…</b></div>
      <p class="fx-perday" id="pDay"></p>
      <p class="fx-launch">{t('Precio de lanzamiento de la fase de prueba.', 'Launch price for the testing phase.')}</p>
      <fieldset class="fx-start" id="startPick"><legend>{t('¿Qué lunes empiezas?', 'Which Monday do you start?')}</legend><div class="fx-starts" id="starts"></div></fieldset>
      <label class="fx-consent"><input type="checkbox" id="buyConsent"><span>{t('Quiero empezar mi Sprint el lunes que elija, dentro de los 14 días que tengo para cancelar. Puedo cancelar gratis antes de la primera llamada; después, pago solo lo que ya usé.', 'I want my Sprint to start on the Monday I choose, within the 14 days I have to cancel. I can cancel for free before the first call; after that, I pay only for what I have used.')} <a href="{A['terms']}">{t('Términos', 'Terms')}</a></span></label>
      <button class="key hl big fx-cta" id="buyBtn" type="button">{t('Reservar mi plaza', 'Book my place')}</button>
      <p class="fx-safe">{ic('lock')}<span>{t('Pago seguro con Stripe. Reembolso completo si cancelas antes de tu primera llamada.', 'Secure payment with Stripe. Full refund if you cancel before your first call.')}</span></p>
      <p class="fx-msg" id="buyMsg" role="status"></p>
      <form class="fx-wait" id="waitForm" hidden><p><b>{t('Esta tanda está completa.', 'This round is full.')}</b> {t('Déjanos tu email y te avisamos en cuanto se abra la siguiente.', 'Leave your email and we will tell you as soon as the next one opens.')}</p>
        <label class="fx-f"><span>{t('Email', 'Email')}</span><input type="email" name="email" required autocomplete="email"></label>
        <button class="key primary" type="submit">{t('Avísame', 'Let me know')}</button></form>
    </aside>
  </div>
  <section class="fx-week" aria-labelledby="weekH"><h2 id="weekH">{t('Tu semana', 'Your week')}</h2><ol>{week}</ol></section>
  <section class="fx-faq" aria-labelledby="faqH"><h2 id="faqH">{t('Preguntas frecuentes', 'Questions')}</h2>{faq_html}</section>
</div></section>
'''


# ---------------------------------------------------------------- the Sprint
def sprint(lang, legacy):
    """Public: what the week is and a taste of Day 1. Paid: the app (filled by account.js from /paid/)."""
    t = L(lang); A = I.SLUG[lang]
    d1 = SP.DAYS[1]
    days = ''.join(f'<li class="fx-lock-day"><span class="fx-dn num">{i + 1}</span><span><b>{tr(lang, d["title"])}</b><small>{(DAY_ES.get(d["can"], tr(lang, d["can"])) if lang == "es" else d["can"])}</small></span>{ic("lock")}</li>' for i, d in enumerate(SC.DAYS))
    # the legacy tools stay: today's tasks tick themselves, the before/after recorder and the 2-minute talk clock
    tools = legacy[legacy.index('<div class="stack" style="max-width:860px">'):legacy.rindex('</div>\n</div></section>')]
    q = tools.index('<div class="panel stack">\n      <div class="row" style="justify-content:space-between"><h2 style="margin:0">Quests from your tutor</h2>')
    tools = tools[:q] + '</div>'   # the sample quests are gone: the real ones come from Mei
    return f'''<section class="light fx" data-view="sprint"><div class="wrap view">
  <div id="sprintPublic">
    <div class="fx-hero">
      <div><h1 class="fx-h1">{t('Siete días para decir tus primeras frases en inglés.', 'Seven days to say your first sentences in English.')}</h1>
      <p class="fx-lead">{t('Un plan cerrado, veinte minutos al día y Mei a tu lado. Sin teoría eterna: cada día dices algo nuevo en voz alta.', 'A set plan, twenty minutes a day and Mei by your side. No endless theory: every day you say something new out loud.')}</p>
      <div class="row"><a class="key hl big" href="{A['join']}">{t('Reservar mi plaza', 'Book my place')}</a><a class="key big" href="{A['tutor']}">{t('Conoce a Mei', 'Meet Mei')}</a></div></div>
      <section class="fx-hero-card fx-taste" aria-labelledby="tasteH"><h2 id="tasteH">{t('Así empieza el Día 1', 'This is how Day 1 starts')}</h2>
        <blockquote class="fx-brief"><p>{d1['brief'][0 if lang == 'es' else 1]}</p></blockquote>
        <div class="fx-phr">{''.join(f'<div><b lang="en">{p[0]}</b><span>{p[1]}</span></div>' for p in SC.S[0][:4])}</div>
        <p class="muted small">{t('Y después: tareas que se marcan solas, el error típico del día, un reto real y tu reflexión. Así, siete días.', 'Then: tasks that tick themselves, the typical mistake of the day, a real challenge and your reflection. Seven days like that.')}</p>
      </section>
    </div>
    <section class="fx-week" aria-labelledby="weekH2"><h2 id="weekH2">{t('La semana', 'The week')}</h2><ol>{days}</ol>
      <a class="key hl big" href="{A['join']}">{t('Reservar mi plaza', 'Book my place')}</a></section>
  </div>
  <div id="sprintApp" hidden>
    <header class="fx-me">
      <div><p class="fx-hi" id="spHi"></p><h1 class="fx-h1" id="spTitle">{t('Tu Sprint', 'Your Sprint')}</h1></div>
      <ol class="fx-ring" id="spRing" aria-label="{t('Tu semana', 'Your week')}"></ol>
    </header>
    <nav class="fx-tabs" id="spTabs" aria-label="{t('Días', 'Days')}"></nav>
    <article class="fx-day" id="spDay" aria-live="polite"></article>
    <section class="fx-block" aria-labelledby="planH"><h2 id="planH">{ic('check')}{t('Las tareas del Sprint', 'The Sprint tasks')}</h2>
      <p class="muted">{t('Seis tareas al día. Se marcan solas cuando terminas cada sala.', 'Six tasks a day. They tick themselves when you finish each room.')}</p>
      {tools}
    </section>
    <section class="fx-block" id="spLib" aria-labelledby="libH"><h2 id="libH">{ic('gift')}{t('Tu biblioteca', 'Your library')}</h2><div class="fx-lib" id="libList"></div></section>
  </div>
</div></section>
'''


# ---------------------------------------------------------------- the tutor
def tutor(lang):
    t = L(lang); A = I.SLUG[lang]
    return f'''<section class="light fx" data-view="tutor"><div class="wrap view">
  <div id="tutorPublic">
    <div class="fx-hero fx-hero-tutor">
      <div><h1 class="fx-h1">{t('Mei, tu tutora.', 'Mei, your tutor.')}</h1>
      <p class="fx-lead">{t('Habla tu idioma y sabe dónde te vas a atascar. Durante tu Sprint la tienes a un mensaje de distancia.', "She speaks your language and knows where you'll get stuck. During your Sprint she's one message away.")}</p>
      <ul class="fx-incl">
        <li>{ic('phone')}<span><b>{t('Dos llamadas 1 a 1', 'Two 1-to-1 calls')}</b>{t('Una para empezar con buen pie y otra para tu charla final.', 'One to get you started and one for your final talk.')}</span></li>
        <li>{ic('whatsapp')}<span><b>{t('WhatsApp toda la semana', 'WhatsApp all week')}</b>{t('Dudas, audios, victorias pequeñas: se las mandas a ella.', 'Questions, voice notes, small wins: you send them to her.')}</span></li>
        <li>{ic('heart')}<span><b>{t('Sin vergüenza', 'No embarrassment')}</b>{t('Aquí equivocarse es parte del plan. Mei celebra que lo intentes.', "Here, getting it wrong is part of the plan. Mei celebrates that you try.")}</span></li>
      </ul></div>
    </div>
    <div class="fx-lockcard" id="tutorLock">{ic('lock')}<div><b>{t('El WhatsApp de Mei es para quienes hacen el Sprint.', "Mei's WhatsApp is for people doing the Sprint.")}</b><p>{t('Cuando reserves tu plaza, aquí tendrás su contacto directo, tus llamadas y sus mensajes para ti.', "Once you book your place, you'll find her direct contact, your calls and her messages for you here.")}</p></div><a class="key hl" href="{A['join']}">{t('Reservar mi plaza', 'Book my place')}</a></div>
  </div>
  <div id="tutorStudent" hidden>
    <header class="fx-me"><div><p class="fx-hi" id="tsHi"></p><h1 class="fx-h1">{t('Tu tutora', 'Your tutor')}</h1></div></header>
    <div class="fx-grid2">
      <section class="fx-block fx-contact" aria-labelledby="contactH"><h2 id="contactH">{ic('whatsapp')}{t('Escríbele a Mei', 'Message Mei')}</h2>
        <p class="muted">{t('Normalmente responde el mismo día. Mándale un audio: le encanta oírte.', 'She usually replies the same day. Send her a voice note: she loves hearing you.')}</p>
        <a class="key fx-wa big" id="waBtn" href="#" target="_blank" rel="noopener">{ic('whatsapp')}{t('Abrir WhatsApp', 'Open WhatsApp')}</a>
        <div class="fx-ideas"><b>{t('Ideas para escribirle hoy', 'Ideas for messaging her today')}</b><ul id="msgIdeas"></ul></div>
      </section>
      <section class="fx-block" aria-labelledby="callsH"><h2 id="callsH">{ic('calendar')}{t('Tus llamadas', 'Your calls')}</h2>
        <ol class="fx-calls"><li><b>{t('Llamada 1: arrancamos', 'Call 1: we get going')}</b><span>{t('Al principio de tu semana. 25 minutos.', 'At the start of your week. 25 minutes.')}</span></li><li><b>{t('Llamada 2: tu charla de 2 minutos', 'Call 2: your 2-minute talk')}</b><span>{t('El Día 7. 25 minutos.', 'On Day 7. 25 minutes.')}</span></li></ol>
        <a class="key primary" id="bookBtn" href="#" target="_blank" rel="noopener">{ic('calendar')}{t('Reservar una llamada', 'Book a call')}</a>
      </section>
    </div>
    <section class="fx-block" aria-labelledby="notesH"><h2 id="notesH">{ic('chat')}{t('Mensajes de Mei para ti', 'Messages from Mei for you')}</h2><div class="fx-notes" id="notes"></div></section>
  </div>
  <div id="tutorDesk" hidden>
    <header class="fx-me"><div><p class="fx-hi" id="tdHi"></p><h1 class="fx-h1">{t('Tu panel', 'Your desk')}</h1></div><div class="fx-kpis" id="tdKpis"></div></header>
    <div class="fx-filter" role="group" aria-label="{t('Filtrar', 'Filter')}"><button class="chip" data-f="paid" aria-pressed="true">{t('En el Sprint', 'In the Sprint')}</button><button class="chip" data-f="pending" aria-pressed="false">{t('Pendientes de pago', 'Waiting to pay')}</button><button class="chip" data-f="free" aria-pressed="false">{t('Cuentas gratis', 'Free accounts')}</button><button class="chip" data-f="wait" aria-pressed="false">{t('Lista de espera', 'Waitlist')}</button></div>
    <div class="fx-students" id="students"></div>
  </div>
</div></section>
'''


# ---------------------------------------------------------------- account
def account(lang, cfg):
    t = L(lang); A = I.SLUG[lang]
    return f'''<section class="light fx" data-view="account"><div class="wrap view fx-narrow">
  <div id="acOut">
    <h1 class="fx-h1">{t('Tu cuenta gratis', 'Your free account')}</h1>
    <p class="fx-lead">{t('Guarda tu progreso, practica cada día y, cuando quieras, empieza tu Sprint.', 'Save your progress, practise every day and, when you want, start your Sprint.')}</p>
    <div class="fx-auth" data-auth-host></div>
  </div>
  <div id="acReset" hidden>
    <h1 class="fx-h1">{t('Nueva contraseña', 'New password')}</h1>
    <form class="fx-form" id="resetForm"><label class="fx-f"><span>{t('Contraseña nueva', 'New password')}</span><input type="password" name="password" minlength="8" required autocomplete="new-password"></label>
      <button class="key primary big" type="submit">{t('Guardar y entrar', 'Save and sign in')}</button><p class="fx-msg" role="status"></p></form>
  </div>
  <div id="acIn" hidden>
    <header class="fx-me"><div><p class="fx-hi" id="acHi"></p><h1 class="fx-h1">{t('Tu cuenta', 'Your account')}</h1></div><span class="fx-plan" id="acPlan"></span></header>
    <section class="fx-block" id="acUsage" aria-labelledby="useH"><h2 id="useH">{ic('clock')}{t('Tu práctica de hoy', "Today's practice")}</h2><div class="fx-meters" id="meters"></div><p class="muted small" id="usageNote"></p></section>
    <section class="fx-block" id="acSprint" aria-labelledby="spH"><h2 id="spH">{ic('star')}{t('Sprint de 7 días', '7-Day Sprint')}</h2><div id="acSprintBody"></div></section>
    <section class="fx-block" aria-labelledby="setH"><h2 id="setH">{ic('user')}{t('Tus datos', 'Your details')}</h2>
      <dl class="fx-dl"><dt>{t('Nombre', 'Name')}</dt><dd id="acName"></dd><dt>Email</dt><dd id="acEmail"></dd></dl>
      <div class="row"><button class="key" id="logoutBtn" type="button">{t('Cerrar sesión', 'Sign out')}</button><button class="key fx-danger" id="delOpen" type="button">{t('Borrar mi cuenta', 'Delete my account')}</button></div>
      <form class="fx-form" id="delForm" hidden><p>{t('Se borrarán tu cuenta, tu progreso y tus datos. No se puede deshacer.', 'Your account, progress and data will be deleted. This cannot be undone.')}</p>
        <label class="fx-f"><span>{t('Escribe tu contraseña para confirmar', 'Type your password to confirm')}</span><input type="password" name="password" required autocomplete="current-password"></label>
        <button class="key fx-danger" type="submit">{t('Sí, borrarlo todo', 'Yes, delete everything')}</button><p class="fx-msg" role="status"></p></form>
    </section>
  </div>
</div></section>
'''


# ---------------------------------------------------------------- thank you
def thanks(lang):
    t = L(lang); A = I.SLUG[lang]
    return f'''<section class="light fx fx-thanks" data-view="thanks"><canvas class="fx-confetti" id="confetti" aria-hidden="true"></canvas><div class="wrap view fx-narrow">
  <div class="fx-ty-head">
    <h1 class="fx-ty-h"><span id="tyName"></span>{t('¡Ya estás dentro!', "You're in!")}</h1>
    <p class="fx-lead" id="tyStatus">{t('Tu plaza en el Sprint de 7 días está reservada.', 'Your place in the 7-Day Sprint is booked.')}</p>
  </div>
  <div class="fx-count" id="tyCount" aria-live="polite"><span class="fx-count-l">{t('Empiezas el', 'You start on')}</span><b id="tyStart"></b><div class="fx-count-n" id="tyLeft"></div></div>
  <section class="fx-steps" aria-labelledby="stepsH"><h2 id="stepsH">{t('Tres cosas antes del lunes', 'Three things before Monday')}</h2>
    <div class="fx-stepbar"><i id="tyBar"></i></div>
    <ol>
      <li data-step="book"><span class="fx-tick">{ic('check')}</span><div><b>{t('Reserva tu primera llamada con Mei', 'Book your first call with Mei')}</b><p>{t('25 minutos para conoceros y arrancar.', '25 minutes to meet and get going.')}</p></div><a class="key primary" id="tyBook" href="#" target="_blank" rel="noopener">{t('Reservar', 'Book')}</a></li>
      <li data-step="whatsapp"><span class="fx-tick">{ic('check')}</span><div><b>{t('Saluda a Mei por WhatsApp', 'Say hi to Mei on WhatsApp')}</b><p>{t('Un «hola» basta. Así ya tienes su número.', 'A "hello" is enough. That way you have her number.')}</p></div><a class="key fx-wa" id="tyWa" href="#" target="_blank" rel="noopener">{ic('whatsapp')}WhatsApp</a></li>
      <li data-step="calendar"><span class="fx-tick">{ic('check')}</span><div><b>{t('Añade tu semana al calendario', 'Add your week to your calendar')}</b><p>{t('Siete recordatorios de 20 minutos.', 'Seven 20-minute reminders.')}</p></div><button class="key" id="tyIcs" type="button">{ic('calendar')}{t('Añadir', 'Add')}</button></li>
    </ol>
  </section>
  <a class="fx-next" href="{A['sprint']}">{ic('arrow')}<span><b>{t('Mientras tanto: haz el Día 0', 'Meanwhile: do Day 0')}</b>{t('Graba tu antes. Dentro de una semana lo vas a agradecer.', "Record your before. In a week you'll be glad you did.")}</span></a>
</div></section>
'''


# ---------------------------------------------------------------- terms
def terms(lang, cfg):
    t = L(lang); A = I.SLUG[lang]; owner = cfg.get('owner', 'Mei Gabriela Parrablanco')
    sec = [
        (t('Quién te vende', 'Who sells to you'), t(f'Week2Speak es un servicio de {owner}, que trabaja como autónoma (sole trader) en el Reino Unido. Contacto: <a href="mailto:hello@week2speak.com">hello@week2speak.com</a>.', f'Week2Speak is a service run by {owner}, a sole trader in the United Kingdom. Contact: <a href="mailto:hello@week2speak.com">hello@week2speak.com</a>.')),
        (t('Qué incluye el Sprint de 7 días', 'What the 7-Day Sprint includes'), t('Acceso completo a la web durante tu Sprint (Modo Habla, juegos, Imita, el curso y el Sprint guiado), dos llamadas 1 a 1 de 25 minutos con tu tutora y contacto por WhatsApp con ella durante tu semana. No incluye correcciones por escrito ni clases adicionales.', 'Full access to the website during your Sprint (Speech Mode, games, shadowing, the course and the guided Sprint), two 25-minute 1-to-1 calls with your tutor, and WhatsApp contact with her during your week. It does not include written corrections or extra classes.')),
        (t('Precio y pago', 'Price and payment'), t('El precio es el que ves al reservar, según tu país, e incluye los impuestos que correspondan. El pago se hace con Stripe; nosotros no vemos ni guardamos los datos de tu tarjeta. Las plazas son limitadas y se asignan por orden de pago.', 'The price is the one shown when you book, depending on your country, and includes any applicable taxes. Payment is made with Stripe; we never see or store your card details. Places are limited and are given in order of payment.')),
        (t('Las llamadas', 'The calls'), t('Reservas tú la hora. Si necesitas cambiarla, avisa con al menos 24 horas. Si no te presentas sin avisar, esa llamada cuenta como hecha. Si tu tutora tiene que cambiarla, te propone otra hora.', 'You book the time. If you need to change it, let us know at least 24 hours before. If you miss a call without notice, it counts as done. If your tutor has to move it, she offers you another time.')),
        (t('Cancelación y reembolsos', 'Cancellation and refunds'), t('Tienes 14 días desde el pago para cancelar. Si cancelas antes de tu primera llamada con la tutora, te devolvemos el importe completo. Como el Sprint empieza dentro de esos 14 días porque tú lo pides al reservar, si cancelas después de la primera llamada te devolvemos el importe menos la parte del servicio que ya has recibido (las llamadas hechas y los días de Sprint con acceso completo). Pasados los 14 días, o terminado el Sprint, no hay reembolso. El resultado del Sprint (por ejemplo, si consigues o no hablar dos minutos) depende de tu práctica y no da derecho a reembolso. Para cancelar, escribe a <a href="mailto:hello@week2speak.com">hello@week2speak.com</a> o a Mei por WhatsApp.', 'You have 14 days from payment to cancel. If you cancel before your first call with the tutor, we refund the full amount. Because the Sprint starts within those 14 days at your request when you book, if you cancel after the first call we refund the amount minus the part of the service you have already received (calls taken and Sprint days with full access). After 14 days, or once the Sprint is over, there is no refund. The outcome of the Sprint (for example, whether you manage to speak for two minutes) depends on your practice and does not give a right to a refund. To cancel, email <a href="mailto:hello@week2speak.com">hello@week2speak.com</a> or message Mei on WhatsApp.')),
        (t('Tu cuenta', 'Your account'), t('La cuenta es personal: no la compartas. Usa datos reales y una contraseña segura. Puedes borrarla cuando quieras desde la página de tu cuenta. Las cuentas gratis tienen límites de uso diarios que pueden cambiar.', 'Your account is personal: do not share it. Use real details and a strong password. You can delete it whenever you like from your account page. Free accounts have daily usage limits, which may change.')),
        (t('Uso de la web', 'Using the website'), t('Los contenidos de Week2Speak (textos, audios, personajes 3D y diseño) son nuestros o tenemos permiso para usarlos. Puedes usarlos para aprender, no para copiarlos ni venderlos. No uses la web para molestar a nadie ni para saltarte sus límites.', "Week2Speak's content (text, audio, 3D characters and design) is ours or used with permission. You may use it to learn, not to copy or resell it. Do not use the website to harass anyone or to get around its limits.")),
        (t('Responsabilidad', 'Liability'), t('Hacemos todo lo posible para que la web funcione bien, pero puede haber cortes o errores. Nada de estos términos limita los derechos que te da la ley como consumidor.', 'We do our best to keep the website working well, but there may be outages or errors. Nothing in these terms limits your statutory rights as a consumer.')),
        (t('Cambios y ley aplicable', 'Changes and governing law'), t('Si cambiamos estos términos, la versión nueva se aplica a las compras nuevas. Se rigen por la ley de Inglaterra y Gales, sin perjuicio de las normas de protección al consumidor de tu país.', 'If we change these terms, the new version applies to new purchases. They are governed by the law of England and Wales, without prejudice to the consumer-protection rules of your country.')),
    ]
    body = ''.join(f'<section><h2>{h}</h2><p>{p}</p></section>' for h, p in sec)
    return f'''<section class="light fx" data-view="terms"><div class="wrap view fx-narrow fx-legal">
  <h1 class="fx-h1">{t('Términos y condiciones', 'Terms and conditions')}</h1>
  <p class="muted">{t('Última actualización: 18 de noviembre de 2026.', 'Last updated: 18 November 2026.')} {t('Lee también nuestro', 'Also read our')} <a href="{A['privacy']}">{t('aviso de privacidad', 'privacy notice')}</a>.</p>
  {body}
</div></section>
'''


def page(name, lang, cfg, legacy=None):
    if name == 'join': return join(lang)
    if name == 'sprint': return sprint(lang, legacy)
    if name == 'tutor': return tutor(lang)
    if name == 'account': return account(lang, cfg)
    if name == 'thanks': return thanks(lang)
    if name == 'terms': return terms(lang, cfg)
    raise KeyError(name)


DAY_ES = {   # the course's day titles and goals, for the paid Sprint in Spanish
    'Me': 'Tú', 'Order and ask': 'Pedir y preguntar', 'Questions': 'Preguntas', 'Yesterday': 'Ayer', 'Opinions': 'Opiniones', 'Keep talking': 'No cortes la charla', 'The 2-minute talk': 'Tu charla de 2 minutos',
    'I can introduce myself.': 'Sé presentarme.', 'I can order food and drink.': 'Sé pedir comida y bebida.', 'I can ask for what I need.': 'Sé pedir lo que necesito.',
    'I can say what I did.': 'Sé contar lo que hice.', 'I can give my opinion.': 'Sé dar mi opinión.', 'I can keep a conversation going.': 'Sé mantener una conversación.', 'I can talk for two minutes.': 'Sé hablar dos minutos seguidos.',
    'Say five true sentences about yourself, without reading.': 'Di cinco frases verdaderas sobre ti, sin leer.',
    'Order a drink and something to eat, and pay.': 'Pide algo de beber y de comer, y paga.',
    'Ask where, what time and how, and ask for something politely.': 'Pregunta dónde, a qué hora y cómo, y pide algo con educación.',
    'Say three things you did yesterday and how it was.': 'Cuenta tres cosas que hiciste ayer y qué tal fue.',
    'Say what you think, give a reason, and agree or disagree.': 'Di lo que piensas, da una razón y muestra si estás de acuerdo o no.',
    'Ask for a repeat, ask what a word means, and send the question back.': 'Pide que te lo repitan, pregunta qué significa una palabra y devuelve la pregunta.',
    'Give a two-minute talk in four parts, with no script.': 'Da una charla de dos minutos en cuatro partes, sin guion.',
}


def paid_json(lang):
    data = SP.build(lang)
    for d in data['days']:
        for k in ('title', 'can', 'goal'):
            if d.get(k) and lang == 'es': d[k] = DAY_ES.get(d[k], I.t(d[k], lang))
    return json.dumps(data, ensure_ascii=False)
