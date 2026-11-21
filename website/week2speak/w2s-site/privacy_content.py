"""Privacy notice for week2speak.com. Plain HTML, written to match what the site and the tutoring actually do."""
UPDATED = '18 November 2026'
EMAIL = 'hello@week2speak.com'


import re


def _stack(html):
    """Label each cell with its column heading so tables can stack into cards on phones."""
    def one(m):
        t = m.group(0)
        heads = re.findall(r'<th>(.*?)</th>', t.split('</thead>')[0])
        def row(r):
            i = iter(heads[1:])
            return re.sub(r'<td>', lambda _: f'<td data-label="{next(i, "")}">', r.group(0))
        return t.replace('<div class="tbl">', '<div class="tbl stack">').split('</thead>')[0] + '</thead>' + re.sub(r'<tr>.*?</tr>', row, t.split('</thead>')[1], flags=re.S)
    return re.sub(r'<div class="tbl">.*?</table></div>', one, html, flags=re.S)


def privacy_page(owner='', lang='es'):
    """The notice in Spanish (the site's language) or English. Written to match what the site, the accounts and the Sprint actually do."""
    es = lang == 'es'
    T = lambda a, b: a if es else b
    owner = owner or 'Mei Gabriela Parrablanco'
    E = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    acc = '/cuenta/' if es else '/en/account/'
    rows = [
        (T('Tu cuenta: nombre, email y contraseña', 'Your account: name, email and password'), T('Cuando creas una cuenta', 'When you create an account'),
         T('Para que entres, guardar tu progreso y aplicar los límites de uso gratis. La contraseña se guarda cifrada con un hash (PBKDF2); nadie puede leerla, ni nosotros.', 'To sign you in, keep your progress and apply the free daily limits. Your password is stored as a salted hash (PBKDF2); nobody can read it, us included.'),
         T('Prestarte el servicio que pides (contrato)', 'Providing the service you ask for (contract)')),
        (T('Cómo nos conociste (opcional)', 'How you heard about us (optional)'), T('Al crear la cuenta, si lo eliges', 'At sign-up, if you choose to'),
         T('Para saber qué canales funcionan', 'To learn which channels work'), T('Tu consentimiento', 'Your consent')),
        (T('Tu progreso de práctica: XP, racha, tareas hechas, frases que escribes o dices, acento elegido, días del Sprint completados y tus reflexiones', 'Practice progress: XP, streak, tasks done, sentences you type or say, chosen accent, Sprint days completed and your reflections'),
         T('Cuando practicas', 'When you practise'),
         T('Sin cuenta, se queda solo en tu navegador. Con cuenta, se copia a tu cuenta para que no lo pierdas y puedas seguir en otro dispositivo. Mei lo ve si haces el Sprint, para preparar tus llamadas.', 'Without an account it stays in your browser only. With an account it is copied to your account so you do not lose it and can continue on another device. Mei sees it if you take the Sprint, to prepare your calls.'),
         T('Contrato', 'Contract')),
        (T('Cuántas veces usas cada herramienta al día', 'How many times a day you use each tool'), T('Cuando practicas', 'When you practise'),
         T('Para aplicar los límites diarios. Sin cuenta, el contador se queda en tu navegador.', 'To apply the daily limits. Without an account the counter stays in your browser.'),
         T('Contrato', 'Contract')),
        (T('Tu reserva del Sprint: fecha de inicio, precio, moneda, estado del pago', 'Your Sprint booking: start date, price, currency, payment status'), T('Cuando reservas', 'When you book'),
         T('Para darte acceso al Sprint y organizar tus llamadas', 'To give you access to the Sprint and arrange your calls'), T('Contrato; registros fiscales (obligación legal)', 'Contract; tax records (legal obligation)')),
        (T('Notas de Mei, tus mensajes y audios de WhatsApp, los errores que repites', 'Mei\'s notes, your WhatsApp messages and voice notes, the mistakes you repeat'), T('Durante el Sprint', 'During the Sprint'),
         T('Para enseñarte, darte feedback y preparar tus llamadas', 'To teach you, give feedback and prepare your calls'), T('Contrato', 'Contract')),
        (T('Las grabaciones de antes y después que haces en la web', 'The before-and-after recordings you make on the site'), T('Cuando pulsas Grabar', 'When you tap Record'),
         T('Para que oigas tu progreso. Se guardan solo en tu navegador; no nos llegan salvo que tú se las mandes a Mei.', 'So you can hear your progress. They are saved only in your browser and do not reach us unless you send them to Mei.'),
         T('No las recogemos', 'Not collected by us')),
        (T('Tu voz, mientras el micrófono está encendido', 'Your voice, while the microphone is on'), T('Cuando pulsas un botón de micrófono', 'When you tap a microphone button'),
         T('Para convertir lo que dices en texto y corregirlo. Lo hace tu navegador (mira «Quién más trata tus datos»).', 'To turn what you say into text so the exercise can check it. Your browser does this (see "Who else handles your data").'),
         T('Tu elección; también puedes escribir', 'Your choice; you can type instead')),
        (T('Grabaciones de llamadas', 'Call recordings'), T('Solo si aceptas', 'Only if you agree'),
         T('Para que tú y Mei oigáis tu progreso', 'So you and Mei can hear your progress'), T('Tu consentimiento', 'Your consent')),
        (T('Clips tuyos en la web o en redes', 'Clips of you on the site or social media'), T('Solo si aceptas aparte, por escrito', 'Only if you agree separately, in writing'),
         T('Para enseñar a otros lo que se consigue en una semana', 'To show others what one week can do'), T('Tu consentimiento aparte', 'Your separate consent')),
        (T('Datos de pago', 'Payment details'), T('Cuando pagas', 'When you pay'),
         T('Stripe cobra el pago. Nunca vemos el número completo de tu tarjeta.', 'Stripe takes the payment. We never see your full card number.'), T('Contrato; obligación legal', 'Contract; legal obligation')),
        (T('Un recuento anónimo de práctica', 'An anonymous practice count'), T('La primera vez al día que practicas cada cosa', 'The first time each day you practise each thing'),
         T('Contamos, de forma anónima, cuántos navegadores practican cada día (Modo Habla, juegos, Imita, curso). Solo se guarda un número por día; no guardamos quién eres, tu IP ni ningún identificador. Tu navegador recuerda en tu dispositivo que ya contó hoy.', 'We count, anonymously, how many browsers practise each day (Speech Mode, games, Shadowing, course). Only one number per day is kept; we do not store who you are, your IP or any identifier. Your browser remembers on your device that it has already been counted today.'),
         T('Interés legítimo en saber si la web ayuda a practicar', 'Legitimate interest in knowing whether the site helps people practise')),
        (T('Datos técnicos: dirección IP, país, navegador, páginas pedidas', 'Technical data: IP address, country, browser, pages requested'), T('Siempre que visitas la web', 'Whenever you visit'),
         T('Nuestro proveedor los usa para servir y proteger la web. Usamos el país para mostrarte el precio en tu moneda, y una huella cifrada de tu IP (no la IP) para frenar abusos en el inicio de sesión.', 'Our host uses them to serve and protect the site. We use your country to show the price in your currency, and a salted hash of your IP (not the IP itself) to slow down abuse of sign-in.'),
         T('Interés legítimo en una web segura', 'Legitimate interest in a secure site')),
    ]
    th = T('<th>Qué</th><th>Cuándo</th><th>Para qué</th><th>Base legal</th>', '<th>What</th><th>When</th><th>Why we use it</th><th>Legal basis</th>')
    body = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td><td>{d}</td></tr>\n' for a, b, c, d in rows)
    prov = [
        ('Cloudflare', T('Alojar la web, tu cuenta y su base de datos', 'Hosting the site, your account and its database'), T('Datos técnicos y los datos de tu cuenta', 'Technical data and your account data')),
        ('Stripe', T('Cobrar el Sprint', 'Taking payment for the Sprint'), T('Tu email, tus datos de pago y la referencia de tu reserva', 'Your email, payment details and your booking reference')),
        ('Cal.com', T('Reservar tus llamadas', 'Booking your calls'), T('Tu nombre, email y la hora que eliges', 'Your name, email and the time you choose')),
        (T('Google Meet', 'Google Meet'), T('Las videollamadas con Mei', 'Video calls with Mei'), T('Tu nombre, vídeo y audio durante la llamada', 'Your name, video and audio during the call')),
        ('WhatsApp (Meta)', T('Hablar con Mei durante el Sprint', 'Talking to Mei during the Sprint'), T('Tu número, tus mensajes y audios', 'Your number, messages and voice notes')),
        (T('El servicio de voz de tu navegador (por ejemplo Google en Chrome, Apple en Safari)', 'Your browser\'s speech service (for example Google for Chrome, Apple for Safari)'), T('Convertir tu voz en texto cuando usas el micrófono', 'Turning speech into text when you use a microphone button'), T('El audio de lo que dices con el micrófono encendido, según las condiciones de tu navegador', 'The audio of what you say while the microphone is on, under your browser provider\'s own terms')),
    ]
    pth = T('<th>Proveedor</th><th>Para qué</th><th>Qué recibe</th>', '<th>Provider</th><th>What for</th><th>What it receives</th>')
    pbody = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>\n' for a, b, c in prov)
    return _stack(f"""<section class="light"><div class="wrap view">
<div class="vh"><h1>{T('Aviso de privacidad', 'Privacy notice')}</h1><p>{T('Qué datos tuyos recogemos, para qué, quién más los trata, cuánto tiempo los guardamos y qué derechos tienes.', 'What personal data Week2Speak collects, why, who else handles it, how long we keep it, and the rights you have.')}</p></div>
<div class="prose">
<p class="updated">{T('Última actualización: 21 de noviembre de 2026', 'Last updated 21 November 2026')}</p>

<h2>{T('Quiénes somos', 'Who we are')}</h2>
<p>{T(f'Week2Speak es un servicio de {owner}, que trabaja como autónoma (sole trader) en el Reino Unido y es la responsable de los datos que se describen aquí. Para cualquier cosa de este aviso, escríbenos a {E}.', f'Week2Speak is run by {owner}, a sole trader in the United Kingdom, who is the data controller for the personal data described here. Contact us about anything in this notice at {E}.')}</p>

<h2>{T('Lo esencial', 'The short version')}</h2>
<ul>
<li>{T('Puedes practicar sin cuenta: entonces tu progreso se queda solo en tu navegador.', 'You can practise without an account: your progress then stays in your browser only.')}</li>
<li>{T('Si creas una cuenta, guardamos tu nombre, tu email, tu progreso y cuánto usas cada herramienta, para que no pierdas nada y para los límites gratis.', 'If you create an account, we keep your name, email, progress and how much you use each tool, so you lose nothing and the free limits work.')}</li>
<li>{T('Solo usamos una cookie, la que mantiene tu sesión abierta. Nada de cookies de publicidad ni analítica, y no te seguimos por otras webs.', 'We use one cookie, the one that keeps you signed in. No advertising or analytics cookies, and we do not track you across other websites.')}</li>
<li>{T('Grabamos llamadas solo si dices que sí, y pedimos permiso aparte antes de usar un clip en público.', 'We record calls only if you say yes, and ask separately before using any clip publicly.')}</li>
<li>{T('No vendemos tus datos.', 'We do not sell your data.')}</li>
</ul>

<h2>{T('Qué recogemos y para qué', 'What we collect and why')}</h2>
<div class="tbl"><table>
<thead><tr>{th}</tr></thead>
<tbody>
{body}</tbody></table></div>

<h2>{T('Grabaciones y clips', 'Recordings and clips')}</h2>
<p>{T('Antes de tu primera llamada te hacemos dos preguntas por separado, y ninguna viene marcada:', 'Before your first call we ask two separate questions, and neither is ticked for you:')}</p>
<ol>
<li>{T('¿Podemos grabar tus llamadas para que tú y Mei oigáis tu progreso?', 'May we record your calls so you and Mei can hear your progress?')}</li>
<li>{T('¿Podemos usar clips cortos tuyos en la web o en redes?', 'May we use short clips of you on our website or social media?')}</li>
</ol>
<p>{T(f'Puedes decir que sí a la primera y no a la segunda, o que no a las dos. Puedes cambiar de idea cuando quieras escribiendo a Mei o a {E}. Si retiras el permiso de los clips, dejamos de usarlos y quitamos los que controlamos.', f'You can agree to the first and not the second, or to neither. You can change your mind at any time by messaging Mei or emailing {E}. If you withdraw permission for clips, we stop using them and remove the ones we control.')}</p>

<h2>{T('Cookies y almacenamiento del navegador', 'Cookies and browser storage')}</h2>
<p>{T('Si entras en tu cuenta, ponemos una cookie llamada <code>w2s_s</code> que mantiene tu sesión abierta 30 días. Es estrictamente necesaria, no sirve para nada más y desaparece al cerrar sesión. Además, la web guarda en el almacenamiento local de tu navegador tu progreso, tus grabaciones de antes y después, tu idioma y, sin cuenta, el contador de uso diario, además de una marca de si ya se contó tu práctica de hoy (mira el recuento anónimo arriba). No usamos analítica de terceros ni rastreadores de publicidad.', 'If you sign in, we set one cookie, <code>w2s_s</code>, that keeps you signed in for 30 days. It is strictly necessary, does nothing else and is removed when you sign out. The site also keeps your progress, your before-and-after recordings, your language and, without an account, the daily usage counter in your browser\'s local storage, plus a mark of whether today\'s practice has already been counted (see the anonymous count above). We use no third-party analytics or advertising trackers.')}</p>

<h2>{T('Quién más trata tus datos', 'Who else handles your data')}</h2>
<p>{T('Usamos pocos proveedores, y cada uno trata tus datos solo para darnos su servicio.', 'We use a small number of providers. Each one handles your data only to provide its service to us.')}</p>
<div class="tbl"><table>
<thead><tr>{pth}</tr></thead>
<tbody>
{pbody}</tbody></table></div>
<p>{T('Algunos tratan datos fuera del Reino Unido y del Espacio Económico Europeo, por ejemplo en Estados Unidos. Cuando lo hacen, se apoyan en garantías legales como las cláusulas contractuales tipo o el puente de datos Reino Unido–EE. UU.', 'Some of these providers process data outside the UK and the European Economic Area, including in the United States. Where they do, they rely on legal safeguards such as standard contractual clauses or the UK-US data bridge.')}</p>

<h2>{T('Cuánto tiempo lo guardamos', 'How long we keep it')}</h2>
<ul>
<li>{T(f'<strong>Tu cuenta y tu progreso:</strong> mientras tengas la cuenta. Puedes borrarla tú mismo en <a href="{acc}">Tu cuenta</a> y se borra todo al momento.', f'<strong>Your account and progress:</strong> while you have the account. You can delete it yourself in <a href="{acc}">Your account</a>, and everything goes at once.')}</li>
<li>{T('<strong>Cuentas sin usar:</strong> si pasas 24 meses sin entrar, la borramos.', '<strong>Unused accounts:</strong> deleted after 24 months without a sign-in.')}</li>
<li>{T('<strong>Notas de Mei, mensajes y grabaciones de llamadas:</strong> hasta 12 meses después de tu Sprint.', '<strong>Mei\'s notes, messages and call recordings:</strong> up to 12 months after your Sprint.')}</li>
<li>{T('<strong>Clips que aceptaste publicar:</strong> hasta que retires el permiso.', '<strong>Clips you agreed to publish:</strong> until you withdraw permission.')}</li>
<li>{T('<strong>Pagos y registros fiscales:</strong> lo que exija la ley fiscal del Reino Unido, hoy al menos 5 años.', '<strong>Payment and tax records:</strong> as long as UK tax law requires, currently at least 5 years.')}</li>
</ul>

<h2>{T('Tus derechos', 'Your rights')}</h2>
<p>{T('Según la ley de protección de datos del Reino Unido y de la UE (UK GDPR y RGPD) puedes pedirnos:', 'Under UK and EU data protection law (UK GDPR and the GDPR) you can ask us to:')}</p>
<ul>
<li>{T('una copia de tus datos;', 'give you a copy of the personal data we hold about you;')}</li>
<li>{T('que corrijamos lo que esté mal;', 'correct data that is wrong or incomplete;')}</li>
<li>{T('que los borremos;', 'delete your data;')}</li>
<li>{T('que limitemos su uso o dejemos de usarlos;', 'restrict or object to how we use it;')}</li>
<li>{T('recibirlos en un formato que puedas llevarte;', 'give you your data in a format you can take elsewhere;')}</li>
<li>{T('retirar cualquier consentimiento cuando quieras, sin que afecte a lo anterior.', 'withdraw any consent you gave, at any time, without affecting what we did before.')}</li>
</ul>
<p>{T('En México tienes los derechos ARCO (acceso, rectificación, cancelación y oposición) de la Ley Federal de Protección de Datos Personales en Posesión de los Particulares. En Colombia puedes conocer, actualizar y rectificar tus datos y revocar tu autorización según la Ley 1581 de 2012.', 'Learners in Mexico have the rights of access, rectification, cancellation and opposition under Mexico\'s Federal Law on the Protection of Personal Data Held by Private Parties. Learners in Colombia can know, update and correct their data and revoke their authorisation under Law 1581 of 2012.')}</p>
<p>{T(f'Para usar cualquiera de estos derechos, escribe a {E}. Te respondemos en menos de un mes y es gratis.', f'To use any of these rights, email {E}. We reply within one month. It is free.')}</p>

<h2>{T('Reclamaciones', 'Complaints')}</h2>
<p>{T('Si algo no te parece bien, escríbenos primero para arreglarlo. También puedes reclamar ante una autoridad de protección de datos:', 'If you are unhappy with how we handle your data, please contact us first so we can put it right. You can also complain to a data protection authority:')}</p>
<ul>
<li>{T('Reino Unido', 'United Kingdom')}: Information Commissioner's Office, <a href="https://ico.org.uk/make-a-complaint/" rel="noopener">ico.org.uk</a></li>
<li>{T('España', 'Spain')}: Agencia Española de Protección de Datos, <a href="https://www.aepd.es" rel="noopener">aepd.es</a></li>
<li>Colombia: Superintendencia de Industria y Comercio, <a href="https://www.sic.gov.co" rel="noopener">sic.gov.co</a></li>
<li>{T('México: la autoridad federal de protección de datos personales', 'Mexico: the federal authority responsible for personal data protection')}</li>
</ul>

<h2>{T('Edad', 'Age')}</h2>
<p>{T('Week2Speak es para mayores de 18 años. No recogemos a sabiendas datos de menores.', 'Week2Speak is for adults aged 18 and over. We do not knowingly collect data from anyone younger.')}</p>

<h2>{T('Cambios en este aviso', 'Changes to this notice')}</h2>
<p>{T('Si cambiamos cómo usamos tus datos, actualizamos esta página y la fecha de arriba. Si el cambio te afecta como alumno, te avisamos antes.', 'If we change how we use your data, we update this page and the date at the top. If a change affects you as a learner, we tell you directly before it applies.')}</p>
</div></div></section>
""")
