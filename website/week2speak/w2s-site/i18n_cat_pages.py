"""Spanish for the original pages' HTML, attributes, JSON-LD and SEO text; see i18n.py.
Each row: (source English, Spanish[, English rewritten to follow the Spanish]).
The English that learners practise (example sentences, right/wrong pairs, dialogue, phrase lists) is left out on purpose,
so it stays English on both sides."""

_HERO_SRC = ('<h1 id="heroLine" aria-label="Speak English in 7 days."><span class="w" aria-hidden="true">Speak</span> <span class="w" aria-hidden="true">English</span>'
             '<br><span class="w" aria-hidden="true">in</span> <span class="w" aria-hidden="true">7</span> <span class="w" aria-hidden="true">days.</span></h1>')
_HERO_ES = ('<h1 id="heroLine" aria-label="Habla inglés en 7 días."><span class="w" aria-hidden="true">Habla</span> <span class="w" aria-hidden="true">inglés</span>'
            '<br><span class="w" aria-hidden="true">en</span> <span class="w" aria-hidden="true">7</span> <span class="w" aria-hidden="true">días.</span></h1>')

# the home page offer: one paid Sprint, plus the free account (replaces the old founding-cohort grid)
_PLANS_SRC = '''<h2 data-split>Be one of the first ten.</h2>
  <p class="sub">The founding cohort is free. Ten learners, seven days, one tutor, and your Day 1 and Day 7 on record.</p>
  <div class="pgrid">
    <div class="plan first"><h3>Founding cohort</h3><p class="price">Free</p><ul><li>10 places</li><li>The full 7-Day Sprint with a tutor</li><li>Day 1 and Day 7 recorded, with your consent</li></ul></div>
    <div class="plan"><h3>7-Day Sprint</h3><p class="price">Price set at launch</p><ul><li>Daily Speech Mode, games and shadowing</li><li>Group check-ins with a tutor</li><li>A 2-minute talk on Day 7</li></ul></div>
    <div class="plan"><h3>Sprint + your tutor</h3><p class="price">Price set at launch</p><ul><li>Everything in the Sprint</li><li>1-to-1 lessons with a tutor who speaks Spanish</li><li>Quests set after each lesson</li></ul></div>
  </div>'''
_PLANS_ES = '''<h2 data-split>Solo cinco plazas.</h2>
  <p class="sub">Estamos en fase de prueba, así que el Sprint es para cinco personas. Siete días, Mei a tu lado y tu antes y después grabado.</p>
  <div class="pgrid" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">
    <div class="plan first"><h3>Sprint de 7 días</h3><p class="price">Pago único</p><ul><li>Dos llamadas 1 a 1 de 25 minutos con Mei</li><li>WhatsApp directo con Mei toda la semana</li><li>Todo Week2Speak, sin límites</li><li>El Sprint día a día y tu antes y después</li><li>Biblioteca de recursos</li></ul></div>
    <div class="plan"><h3>Cuenta gratis</h3><p class="price">Gratis</p><ul><li>Modo Habla, juegos y shadowing, con un límite diario</li><li>Las lecciones 1 y 2 del curso</li><li>Sin cuenta, solo una prueba corta</li></ul></div>
  </div>'''
_PLANS_EN = '''<h2 data-split>Only five places.</h2>
  <p class="sub">We are in testing, so the Sprint is for five people. Seven days, Mei by your side and your before and after on record.</p>
  <div class="pgrid" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">
    <div class="plan first"><h3>7-Day Sprint</h3><p class="price">One payment</p><ul><li>Two 25-minute 1-to-1 calls with Mei</li><li>WhatsApp straight to Mei all week</li><li>All of Week2Speak, no limits</li><li>The Sprint day by day, and your before and after</li><li>A resource library</li></ul></div>
    <div class="plan"><h3>Free account</h3><p class="price">Free</p><ul><li>Speech Mode, games and shadowing, with a daily limit</li><li>Lessons 1 and 2 of the course</li><li>Without an account, just a short taste</li></ul></div>
  </div>'''

# the footer gets the terms page next to privacy (the build does not map /terms/, so each language has its own path)
_FOOT_SRC = '<a href="/privacy/">Privacy</a><a href="mailto:hello@week2speak.com">'
_FOOT_ES = '<a href="/privacy/">Privacidad</a><a href="/terminos/">Términos</a><a href="mailto:hello@week2speak.com">'
_FOOT_EN = '<a href="/privacy/">Privacy</a><a href="/en/terms/">Terms</a><a href="mailto:hello@week2speak.com">'

_LLMS_SRC = '''# Week2Speak

> Week2Speak is an English speaking programme for adults whose first language is Spanish. It combines a 7-Day Sprint with a Spanish-speaking tutor, short daily lessons, and browser-based speaking practice: Speech Mode conversations, sentence and sound games, and shadowing in American, British and Australian accents.

Status: in testing (November 2026). The site is in English; a Spanish version is planned. The founding cohort is free and has ten places. Paid plan prices are set before the public launch.

## Main pages
- [7-Day Sprint]({site}/7-day-sprint/): two 45-minute tutor calls (Day 1 and Day 7), about 20 minutes of practice a day in six short tasks, daily voice-note feedback.
- [Course]({site}/course/): seven lessons of 12 minutes or less, each with five key phrases and one mistake that comes from Spanish.
- [Speech Mode]({site}/speech-mode/): scripted speaking practice in six scenes with a three-step hint system.
- [Games]({site}/games/): Word Order, Fill the Gap, Flash Translate, Sound Lab and Quick Answers, with a pack for each day of the Sprint.
- [Shadowing]({site}/shadowing/): a clip for each day plus your own script, three speeds, American, British and Australian accents.
- [16 English mistakes Spanish speakers make]({site}/common-mistakes/): each with the wrong sentence, the right one and the Spanish pattern behind it.
- [How we teach]({site}/about/): the method and the research behind it.
- [Join]({site}/join/): request a founding place.

## Facts
- Audience: Spanish-speaking adults who understand some English but freeze when speaking.
- Claim scope: the Sprint does not promise fluency in 7 days. It aims for a 2-minute unscripted talk on Day 7.
- Live AI tutor: not available to the public yet; Speech Mode on the site is scripted.
'''
_LLMS_ES = '''# Week2Speak

> Week2Speak es un programa para hablar inglés, pensado para adultos cuya lengua materna es el español. Combina un Sprint de 7 días con Mei, una tutora que habla español, lecciones cortas y práctica oral en el navegador: conversaciones en Modo Habla, juegos de frases y de sonidos, y shadowing con acento estadounidense, británico y australiano.

Estado: fase de prueba (noviembre de 2026). El sitio está en español (en /) y en inglés (en /en/). Hay una sola oferta de pago, el Sprint de 7 días, con cinco plazas en esta fase. En el Reino Unido cuesta 49 £; en otros países el precio se muestra en la moneda local antes de pagar. Con una cuenta gratis se usan Modo Habla, los juegos, el shadowing y las lecciones 1 y 2 del curso, con un límite diario.

## Páginas principales
- [Sprint de 7 días]({site}/sprint-7-dias/): dos llamadas 1 a 1 de 25 minutos con Mei, WhatsApp directo con ella toda la semana, unos 20 minutos de práctica al día y una charla de 2 minutos al final.
- [Únete]({site}/unete/): precio en tu moneda, plazas libres y fecha de inicio.
- [Curso]({site}/curso/): siete lecciones de 12 minutos o menos, cada una con cinco frases clave y un error que viene del español.
- [Modo Habla]({site}/modo-habla/): práctica oral guiada en seis escenas, con pistas en tres pasos.
- [Juegos]({site}/juegos/): Ordena la frase, Completa la frase, Traducción flash, Laboratorio de sonidos y Respuestas rápidas, con un paquete para cada día del Sprint.
- [Shadowing]({site}/shadowing/): un clip para cada día y tu propio guion, tres velocidades y tres acentos.
- [16 errores de inglés que cometen los hispanohablantes]({site}/errores-comunes/): cada uno con la frase incorrecta, la correcta y el patrón del español que lo causa.
- [Cómo enseñamos]({site}/como-ensenamos/): el método y la investigación en la que se basa.
- [English version]({site}/en/): the same site in English.

## Datos
- Público: adultos hispanohablantes que empiezan desde cero, o que entienden algo de inglés pero se bloquean al hablar.
- Alcance: el Sprint no promete fluidez en 7 días. Busca que al final puedas dar una charla de 2 minutos sin guion.
- Reembolso: completo solo antes de la primera llamada.
- Tutor de IA en vivo: no disponible; Modo Habla es práctica guiada con guion.
'''
_LLMS_EN = '''# Week2Speak

> Week2Speak is a programme for speaking English, designed for adults whose first language is Spanish. It combines a 7-Day Sprint with Mei, a tutor who speaks Spanish, short lessons and speaking practice in the browser: Speech Mode conversations, sentence and sound games, and shadowing in American, British and Australian accents.

Status: in testing (November 2026). The site is in Spanish (at /) and English (at /en/). There is one paid offer, the 7-Day Sprint, with five places in this phase. In the UK it costs £49; in other countries the price is shown in the local currency before payment. A free account gives Speech Mode, the games, shadowing and lessons 1 and 2 of the course, with a daily limit.

## Main pages
- [7-Day Sprint]({site}/en/7-day-sprint/): two 25-minute 1-to-1 calls with Mei, WhatsApp straight to her all week, about 20 minutes of practice a day and a 2-minute talk at the end.
- [Join]({site}/en/join/): price in your currency, places left and start date.
- [Course]({site}/en/course/): seven lessons of 12 minutes or less, each with five key phrases and one mistake that comes from Spanish.
- [Speech Mode]({site}/en/speech-mode/): guided speaking practice in six scenes, with hints in three steps.
- [Games]({site}/en/games/): Word Order, Fill the Gap, Flash Translate, Sound Lab and Quick Answers, with a pack for each day of the Sprint.
- [Shadowing]({site}/en/shadowing/): a clip for each day and your own script, three speeds and three accents.
- [16 English mistakes Spanish speakers make]({site}/en/common-mistakes/): each with the wrong sentence, the right one and the Spanish pattern behind it.
- [How we teach]({site}/en/about/): the method and the research behind it.
- [Versión en español]({site}/): the same site in Spanish.

## Facts
- Audience: Spanish-speaking adults starting from zero, or who understand some English but freeze when speaking.
- Scope: the Sprint does not promise fluency in 7 days. It aims for a 2-minute talk with no script at the end.
- Refund: in full only before the first call.
- Live AI tutor: not available; Speech Mode is guided, scripted practice.
'''

CAT = [
    # ---------- raw blocks (markup) ----------
    (_HERO_SRC, _HERO_ES),
    (_PLANS_SRC, _PLANS_ES, _PLANS_EN),
    (_FOOT_SRC, _FOOT_ES, _FOOT_EN),
    # llms.txt as one whole string: the build has to pass C.LLMS through i18n.t to use it
    (_LLMS_SRC, _LLMS_ES, _LLMS_EN),

    # ---------- header, nav, footer ----------
    ('Week2Speak home', 'Inicio de Week2Speak'),
    ('Sections', 'Secciones'),
    ('Home', 'Inicio'),
    ('Speech Mode', 'Modo Habla'),
    ('<span class="ts">Speak</span>', '<span class="ts">Habla</span>'),
    ('Games', 'Juegos'),
    ('7-Day Sprint', 'Sprint de 7 días'),
    ('Course', 'Curso'),
    ('Tutor view', 'Tutora', 'Tutor'),
    ('Day streak', 'Racha de días'),
    ('Experience points', 'Puntos de experiencia'),
    ('Join free', 'Empieza tu Sprint', 'Start your Sprint'),
    ('English speaking practice for Spanish speakers. In testing, in English; a Spanish version comes next.',
     'Práctica para hablar inglés, hecha para hispanohablantes. En fase de prueba.',
     'Speaking practice for Spanish speakers learning English. In testing.'),
    ('Footer', 'Pie de página'),
    ('Practise', 'Practica'),
    ('Learn', 'Aprende'),
    ('Common mistakes', 'Errores comunes'),
    ('How we teach', 'Cómo enseñamos'),
    ('Join the founding cohort', 'Reserva tu plaza', 'Book your place'),
    ('Privacy', 'Privacidad'),

    # ---------- shared JSON-LD ----------
    ('English speaking practice and tutoring for Spanish speakers.', 'Práctica oral y clases de inglés para hispanohablantes.'),
    ('Week2Speak practice app walkthrough', 'Recorrido por la app de práctica de Week2Speak'),
    ('A 53-second screen recording of the Week2Speak practice rooms: a first sentence, Word Order, Speech Mode with a Spanish-speaker fix, and shadowing.',
     'Una grabación de pantalla de 53 segundos de las salas de práctica de Week2Speak: una primera frase, Ordena la frase, Modo Habla con una corrección de un error típico del español y shadowing.'),
    ('Join', 'Únete'),
    ('About', 'Cómo enseñamos', 'How we teach'),
    ('Beginner', 'Principiante'),
    ('Spoken English for Spanish speakers', 'Inglés hablado para hispanohablantes'),

    # ---------- home: SEO ----------
    ('Week2Speak: Speak English in 7 Days for Spanish Speakers', 'Aprende a hablar inglés en 7 días | Week2Speak', 'Learn to speak English in 7 days | Week2Speak'),
    ('Week2Speak: Speak English in 7 days', 'Week2Speak: habla inglés en 7 días'),
    ('Say real English sentences from day one. A 7-day Sprint with a Spanish-speaking tutor, plus speaking practice, shadowing and games for Spanish speakers.',
     'Di tus primeras frases en inglés desde el primer día. Un Sprint de 7 días con una tutora que habla español, práctica oral, juegos y shadowing.',
     'Say your first English sentences from the first day. A 7-day Sprint with a tutor who speaks Spanish, speaking practice, games and shadowing.'),

    # ---------- home: hero ----------
    ('Real sentences, out loud, from day one. Built for Spanish speakers by a tutor who knows where Spanish trips you up.',
     'Frases reales, en voz alta, desde el primer día. Hecho para hispanohablantes por una tutora que sabe en qué te tropiezas al pasar del español al inglés.',
     'Real sentences, out loud, from the first day. Made for Spanish speakers by a tutor who knows where you trip up going from Spanish to English.'),
    ('Start the 7-Day Sprint', 'Empieza el Sprint de 7 días'),
    ('Watch a session', 'Mira una sesión'),
    ('Mistakes Spanish speakers make, and the fix', 'Errores típicos de hispanohablantes, y cómo se dice bien', 'Typical Spanish-speaker mistakes, and how to say it right'),

    # ---------- home: method strip ----------
    ('Ten years of school English. How many sentences did you say out loud?',
     'Años de inglés en el colegio. ¿Cuántas frases dijiste en voz alta?',
     'Years of English at school. How many sentences did you say out loud?'),
    ('Hear it', 'Escúchala'),
    ('Listen to a real sentence in the accent you want to learn.', 'Escucha una frase real con el acento que quieres aprender.'),
    ('Say it', 'Dila'),
    ('Repeat it, shadow it, build it from word tiles until your mouth knows it.',
     'Repítela, síguela con shadowing y ármala con fichas hasta que te salga sola.',
     'Repeat it, follow it with shadowing and build it from tiles until it comes out on its own.'),
    ('Use it', 'Úsala'),
    ('Take it into a café, an airport, a job interview. Hints catch you when you freeze.',
     'Llévala a un café, a un aeropuerto, a una entrevista de trabajo. Si te bloqueas, las pistas te rescatan.',
     'Take it into a café, an airport, a job interview. If you freeze, the hints rescue you.'),
    ('Exercise 4. The verb "to be"', 'Ejercicio 4. El verbo "to be"'),
    ('sentences said out loud', 'frases dichas en voz alta'),

    # ---------- home: films ----------
    ("Three short films rebuilt from the app's real screens, and one screen recording of the test build. Drag the bar to scrub.",
     'Tres vídeos cortos hechos con las pantallas reales de la app y una grabación de pantalla de la versión de prueba. Arrastra la barra para avanzar o retroceder.',
     "Three short videos made from the app's real screens, and one screen recording of the test version. Drag the bar to move forward or back."),
    ('Films', 'Vídeos'),
    ('Word Order', 'Ordena la frase'),
    ('Screen recording', 'Grabación de pantalla'),
    ('Try Speech Mode', 'Prueba Modo Habla'),
    ('Café order', 'Pedir en un café'),
    ('"For" + verb', '"For" + verbo'),
    ('Use "to" for a purpose: a coffee to drink.', 'Para decir "para" + verbo, usa "to": a coffee to drink.', 'To say what something is for, use "to": a coffee to drink.'),
    ('Help me: start like this', 'Ayúdame: empieza así'),
    ('Put the words in order, then say the sentence.', 'Ordena las palabras y luego di la frase.'),
    ('Correct. Now say it out loud.', '¡Bien! Ahora dila en voz alta.', 'Good! Now say it out loud.'),
    ('Shadowing studio', 'Estudio de shadowing'),
    ('Listen', 'Escucha'),
    ('Native', 'Nativo'),
    ('You', 'Tú'),
    ('Words heard clearly', 'Palabras que se entienden bien', 'Words that come through clearly'),
    ('6 of 7', '6 de 7'),
    ('Screen recording of the Week2Speak test app', 'Grabación de pantalla de la app de prueba de Week2Speak'),
    ('Play film', 'Reproducir vídeo', 'Play video'),
    ('Film position', 'Posición del vídeo', 'Video position'),

    # ---------- home: try it ----------
    ('Try it on this page', 'Pruébalo aquí mismo', 'Try it right here'),
    ('Two pieces of the practice rooms, working right here.', 'Dos partes de las salas de práctica, funcionando aquí mismo.'),
    ('Catch your Spanish', 'Atrapa los errores del español', 'Catch the mistakes from Spanish'),
    ('Type an English sentence the way you would say it. Mistakes that come from Spanish get caught as you type.',
     'Escribe una frase en inglés tal como la dirías. Los errores que vienen del español saltan mientras escribes.',
     'Type an English sentence just as you would say it. Mistakes that come from Spanish pop up as you type.'),
    ('Your English sentence', 'Tu frase en inglés'),
    ('Tap the words in order to build the sentence.', 'Toca las palabras en orden para formar la frase.'),
    ('Your sentence', 'Tu frase'),
    ('Words', 'Palabras'),
    ('Open Speech Mode', 'Abrir Modo Habla'),
    ('Play all five games', 'Jugar a los cinco juegos'),
    ('Open the shadowing studio', 'Abrir el estudio de shadowing'),
    ('See the course', 'Ver el curso'),

    # ---------- the seven days (home week cards, course, paid Sprint data) ----------
    ('Seven days, twenty minutes a day', 'Siete días, veinte minutos al día'),
    ('Start Day 1', 'Empieza el Día 1'),
    ('Me', 'Yo'),
    ('Order and ask', 'Pedir y preguntar'),
    ('Questions', 'Preguntas'),
    ('Yesterday', 'Ayer'),
    ('Opinions', 'Opiniones'),
    ('Keep talking', 'Sigue hablando'),
    ('The 2-minute talk', 'La charla de 2 minutos'),
    ('I can introduce myself. Say five true sentences about yourself, without reading.', 'Puedo presentarme. Di cinco frases verdaderas sobre ti, sin leer.', 'I can introduce myself. Say five true sentences about yourself, without reading.'),
    ('I can order food and drink. Order a drink and something to eat, and pay.', 'Puedo pedir comida y bebida. Pide algo de beber y algo de comer, y paga.'),
    ('I can ask for what I need. Ask where, what time and how, and ask for something politely.', 'Puedo pedir lo que necesito. Pregunta dónde, a qué hora y cómo, y pide algo con educación.'),
    ('I can say what I did. Say three things you did yesterday and how it was.', 'Puedo contar lo que hice. Di tres cosas que hiciste ayer y qué tal fue.'),
    ('I can give my opinion. Say what you think, give a reason, and agree or disagree.', 'Puedo dar mi opinión. Di lo que piensas, da un motivo y di si estás de acuerdo o no.'),
    ('I can keep a conversation going. Ask for a repeat, ask what a word means, and send the question back.', 'Puedo mantener una conversación. Pide que te repitan, pregunta qué significa una palabra y devuelve la pregunta.'),
    ('I can talk for two minutes. Give a two-minute talk in four parts, with no script.', 'Puedo hablar dos minutos. Da una charla de dos minutos en cuatro partes, sin guion.'),
    ('Lesson 1 and Sound Lab (sp- and st-)', 'Lección 1 y Laboratorio de sonidos (sp- y st-)'),
    ('Lesson 2 and Sound Lab (the English h)', 'Lección 2 y Laboratorio de sonidos (la h inglesa)'),
    ('Lesson 3 and Sound Lab (short i and long ee)', 'Lección 3 y Laboratorio de sonidos (i corta y ee larga)'),
    ('Lesson 4 and Sound Lab (-ed endings)', 'Lección 4 y Laboratorio de sonidos (terminaciones en -ed)'),
    ('Lesson 5 and Sound Lab (th)', 'Lección 5 y Laboratorio de sonidos (th)'),
    ('Lesson 6 and Sound Lab (v and b)', 'Lección 6 y Laboratorio de sonidos (v y b)'),
    ('Lesson 7 and Sound Lab', 'Lección 7 y Laboratorio de sonidos'),
    ('Shadow "My script"', 'Shadowing: "Mi guion"', 'Shadowing: "My script"'),
    ('Shadow "Ordering coffee"', 'Shadowing: "Pedir un café"', 'Shadowing: "Ordering coffee"'),
    ('Shadow "At the airport"', 'Shadowing: "En el aeropuerto"', 'Shadowing: "At the airport"'),
    ('Shadow "Yesterday"', 'Shadowing: "Ayer"', 'Shadowing: "Yesterday"'),
    ('Shadow "My opinion"', 'Shadowing: "Mi opinión"', 'Shadowing: "My opinion"'),
    ('Shadow "Keep talking"', 'Shadowing: "Sigue hablando"', 'Shadowing: "Keep talking"'),
    ('Shadow your own talk', 'Shadowing de tu propia charla', 'Shadowing of your own talk'),
    ('Word Order and Speech Mode: Meet someone new', 'Ordena la frase y Modo Habla: Conocer a alguien'),
    ('Fill the Gap and Speech Mode: Café order', 'Completa la frase y Modo Habla: Pedir en un café'),
    ('Flash Translate and Speech Mode: Airport check-in', 'Traducción flash y Modo Habla: Facturar en el aeropuerto'),
    ('Word Order and Speech Mode: Chat about yesterday', 'Ordena la frase y Modo Habla: Charla sobre ayer'),
    ('Fill the Gap and Speech Mode: Coffee chat: opinions', 'Completa la frase y Modo Habla: Café y opiniones'),
    ('Flash Translate and Speech Mode: Meet someone new, without Help me', 'Traducción flash y Modo Habla: Conocer a alguien, sin Ayúdame'),
    ('Rehearse against the 2-minute clock', 'Ensaya con el reloj de 2 minutos'),
    ('Day 7 call: give the talk to your tutor', 'Última llamada: das tu charla a Mei', 'Last call: you give your talk to Mei'),
    ('Voice note: Tell me about yourself. 30 seconds, no reading.', 'Reto en voz alta: habla de ti. 30 segundos, sin leer.', 'Out-loud challenge: talk about yourself. 30 seconds, no reading.'),
    ('Voice note: Order your real breakfast in English. 30 seconds.', 'Reto en voz alta: pide tu desayuno de verdad en inglés. 30 segundos.', 'Out-loud challenge: order your real breakfast in English. 30 seconds.'),
    ('Voice note: Ask me three questions. I will answer them.', 'Reto en voz alta: haz tres preguntas que de verdad necesites.', 'Out-loud challenge: ask three questions you really need.'),
    ('Voice note: What did you do yesterday? 45 seconds.', 'Reto en voz alta: ¿qué hiciste ayer? 45 segundos.', 'Out-loud challenge: what did you do yesterday? 45 seconds.'),
    ('Voice note: The city or the beach? Say why. 45 seconds.', 'Reto en voz alta: ¿ciudad o playa? Di por qué. 45 segundos.', 'Out-loud challenge: the city or the beach? Say why. 45 seconds.'),
    ('Voice note: The first minute of your talk: who you are and what you like.', 'Reto en voz alta: el primer minuto de tu charla, quién eres y qué te gusta.', 'Out-loud challenge: the first minute of your talk, who you are and what you like.'),

    # ---------- home: accents, FAQ links, offer CTA ----------
    ('Choose the accent you want to learn', 'Elige el acento que quieres aprender'),
    ('Tap a flag to hear the line. Voices come from your own device, so what you hear depends on which voices it has.',
     'Toca una bandera para escuchar la frase. Las voces son las de tu propio dispositivo, así que lo que oyes depende de las voces que tenga instaladas.'),
    ('Questions people ask', 'Preguntas frecuentes', 'Frequently asked questions'),
    ('How Week2Speak teaches', 'Cómo enseñamos en Week2Speak'),
    ('16 English mistakes Spanish speakers make', '16 errores de inglés que cometen los hispanohablantes'),
    ('Ask for a founding place', 'Ver plazas y precio', 'See places and price'),

    # ---------- home FAQ (HTML and JSON-LD) ----------
    ('What is Week2Speak?', '¿Qué es Week2Speak?'),
    ('Week2Speak is an English speaking programme for Spanish speakers. It combines a 7-day Sprint with a tutor who speaks Spanish, short daily lessons, and practice rooms for speaking out loud: Speech Mode, sentence games and shadowing.',
     'Week2Speak es un programa para hablar inglés, pensado para hispanohablantes. Combina un Sprint de 7 días con Mei, una tutora que habla español, lecciones cortas y salas para practicar en voz alta: Modo Habla, juegos de frases y shadowing.',
     'Week2Speak is a programme for speaking English, designed for Spanish speakers. It combines a 7-Day Sprint with Mei, a tutor who speaks Spanish, short lessons and rooms for practising out loud: Speech Mode, sentence games and shadowing.'),
    ('Can you really speak English in 7 days?', '¿De verdad se puede hablar inglés en 7 días?'),
    ('You will not be fluent in 7 days. The Sprint aims for something smaller and real: by Day 7 you can introduce yourself, order, ask questions and give a 2-minute talk in English without a script. Your Day 1 and Day 7 recordings show the change.',
     'En 7 días no vas a hablar con fluidez. El Sprint busca algo más pequeño y real: el Día 7 puedes presentarte, pedir, hacer preguntas y dar una charla de 2 minutos en inglés sin guion. Tus grabaciones del Día 1 y del Día 7 muestran el cambio.'),
    ('Who is Week2Speak for?', '¿Para quién es Week2Speak?'),
    ('Adults whose first language is Spanish who understand some English but freeze when they have to speak. If you have never studied English at all, the first week will feel fast.',
     'Para adultos cuya lengua materna es el español y que empiezan desde cero, o que entienden algo de inglés pero se bloquean al hablar. No hace falta saber gramática: empiezas diciendo frases.',
     'Adults whose first language is Spanish who are starting from zero, or who understand some English but freeze when they speak. You do not need to know grammar: you start by saying sentences.'),
    ('How much does Week2Speak cost?', '¿Cuánto cuesta?', 'How much does it cost?'),
    ('The founding cohort is free and has ten places. Prices for the paid plans are set before the public launch.',
     'Crear una cuenta es gratis: tienes Modo Habla, los juegos, el shadowing y las lecciones 1 y 2 del curso, con un límite diario. El Sprint de 7 días es un pago único: en el Reino Unido cuesta 49 £ y en otros países ves el precio en tu moneda antes de pagar.',
     'An account is free: you get Speech Mode, the games, shadowing and lessons 1 and 2 of the course, with a daily limit. The 7-Day Sprint is a single payment: in the UK it costs £49, and in other countries you see the price in your currency before you pay.'),
    ('Do I need to download an app?', '¿Tengo que descargar una app?'),
    ('No. Everything runs in the browser on your phone or computer. The microphone works in Chrome, Edge and Safari; in other browsers you can type your answers instead.',
     'No. Todo funciona en el navegador de tu móvil o tu ordenador. El micrófono funciona en Chrome, Edge y Safari; en otros navegadores puedes escribir tus respuestas.'),
    ('Which English accents can I learn?', '¿Qué acentos de inglés puedo aprender?'),
    ('American, British and Australian. The voices come from your own device, so the accents you hear depend on the voices your phone or computer has installed.',
     'Estadounidense, británico y australiano. Las voces son las de tu propio dispositivo, así que los acentos que oyes dependen de las voces que tenga instaladas tu móvil u ordenador.'),

    # ---------- Speech Mode page ----------
    ('Speech Mode: English Speaking Practice | Week2Speak', 'Modo Habla: practica inglés hablado | Week2Speak', 'Speech Mode: practise spoken English | Week2Speak'),
    ('Practise speaking English out loud in real scenes: a café, an airport, a job interview. Get hints when you freeze and quick fixes for Spanish-speaker mistakes.',
     'Practica inglés en voz alta en escenas reales: un café, un aeropuerto, una entrevista. Pistas si te bloqueas y correcciones de errores típicos del español.',
     'Practise English out loud in real scenes: a café, an airport, an interview. Hints if you freeze and fixes for typical mistakes from Spanish.'),
    ('Speech Mode: English speaking practice', 'Modo Habla: practica inglés hablando', 'Speech Mode: practise English by speaking'),
    ('Pick a scene and answer in full sentences. Every reply earns XP, and mistakes typical for Spanish speakers get a quick fix.',
     'Elige una escena y responde con frases completas. Cada respuesta suma XP, y los errores típicos del español se corrigen al momento.'),
    ('Kairo, a Language Buddy with long locs and an orange beanie, in a striped jacket', 'Kairo, un Buddy con rastas largas y gorro naranja, con una chaqueta de rayas'),
    ('May, a Language Buddy with long dark brown wavy hair and a beige scarf', 'May, una Buddy con el pelo largo, oscuro y ondulado, y una bufanda beige'),
    ('Scene', 'Escena'),
    ('Switch Buddy', 'Cambiar de Buddy'),
    ('Buddy sounds', 'Sonidos del Buddy'),
    ('laid-back and confident', 'tranquilo y seguro de sí mismo'),
    ('Start talking', 'Empieza a hablar'),
    ('Listen, then answer out loud.', 'Escucha y responde en voz alta.'),
    ('Stop speaking', 'Parar la voz', 'Stop the voice'),
    ('Hear it again', 'Escuchar otra vez'),
    ('Scene, accent and conversation', 'Escena, acento y conversación'),
    ('Scene and settings', 'Escena y ajustes'),
    ('Close', 'Cerrar'),
    ('AI tutor live', 'Conversación en vivo', 'Live conversation'),
    ('Conversation', 'Conversación'),
    ('Tutor accent', 'Acento'),
    ('Read tutor lines aloud', 'Leer en voz alta las frases del Buddy', "Read the Buddy's lines aloud"),
    ('Show the Buddy', 'Mostrar el Buddy'),
    ('Show subtitles', 'Mostrar subtítulos'),
    ('Speaking pace', 'Velocidad de la voz', 'Voice speed'),
    ('Slow', 'Lenta'),
    ('This session', 'Esta sesión'),
    ('sentences', 'frases'),
    ('fixes', 'correcciones'),
    ('hints used', 'pistas usadas'),
    ('More practice', 'Más práctica'),
    ('Speak your answer', 'Di tu respuesta'),
    ('Type your answer in English', 'Escribe tu respuesta en inglés'),
    ('Your answer', 'Tu respuesta'),
    ('Send', 'Enviar'),
    ('About this page', 'Sobre esta página'),
    ('How Speech Mode works', 'Cómo funciona Modo Habla'),
    ('Speech Mode is a speaking practice room. The tutor says a line from a real situation, you answer in a full English sentence, and the conversation moves on. Each answer earns XP, and mistakes that are common for Spanish speakers get a short fix.',
     'Modo Habla es una sala para practicar hablando. Tu Buddy dice una frase de una situación real, tú respondes con una frase completa en inglés y la conversación sigue. Cada respuesta suma XP, y los errores típicos de los hispanohablantes reciben una corrección corta.',
     'Speech Mode is a room for practising by speaking. Your Buddy says a line from a real situation, you answer with a full English sentence and the conversation goes on. Each answer earns XP, and the typical mistakes of Spanish speakers get a short fix.'),
    ('Language Buddies.', 'Los Buddies.', 'The Buddies.'),
    ("Ruby, from London, and Max, from New York, are two 3D characters who say the tutor's lines, with mouths that move as they speak. Their line shows under them with each word lit up as it is said. Switch between them with one button, drag to spin them, and tap them to see how they react.",
     'Kairo y May son dos personajes 3D que dicen las frases de la conversación, con una boca que se mueve al hablar. Debajo aparece su frase, con cada palabra iluminada al decirla. Cambias de uno a otro con un botón, los giras arrastrando y, si los tocas, reaccionan.',
     'Kairo and May are two 3D characters who say the lines of the conversation, with a mouth that moves as they speak. Their line shows below them, with each word lit up as it is said. Switch from one to the other with a button, drag to spin them, and tap them to see them react.'),
    ('Pick a scene:', 'Elige una escena:'),
    ('Meet someone new, Café order, Airport check-in, Chat about yesterday, Coffee chat: opinions or Job interview.',
     'Conocer a alguien, Pedir en un café, Facturar en el aeropuerto, Charla sobre ayer, Café y opiniones o Entrevista de trabajo.'),
    ('Answer out loud', 'Responde en voz alta'),
    ('with the microphone, or type if your browser has no speech recognition.', 'con el micrófono, o escribe si tu navegador no reconoce la voz.'),
    ('Tap Help me', 'Toca Ayúdame'),
    ('if you freeze. The first tap gives you a sentence starter, the second a bank of useful words, the third a full sentence to say.',
     'si te bloqueas. El primer toque te da el comienzo de una frase, el segundo unas palabras útiles y el tercero una frase completa para decir.'),
    ('Want a list of the mistakes it watches for? Read', '¿Quieres ver la lista de errores que detecta? Lee'),
    ('Do I need a microphone?', '¿Necesito micrófono?'),
    ('It helps. In Chrome, Edge and Safari (including on iPhone and Android) you can answer out loud. In other browsers, say your answer out loud first and then type it.',
     'Ayuda. En Chrome, Edge y Safari (también en iPhone y Android) puedes responder en voz alta. En otros navegadores, di tu respuesta en voz alta primero y luego escríbela.'),
    ('Is the tutor in Speech Mode a real person?', '¿La conversación de Modo Habla es con una persona real?', 'Is the conversation in Speech Mode with a real person?'),
    ('No. Speech Mode is scripted practice that runs on this site. Live lessons with a human tutor are part of the 7-Day Sprint.',
     'No. Modo Habla es práctica guiada que funciona en esta web. Las llamadas con Mei, tu tutora de carne y hueso, son parte del Sprint de 7 días.',
     'No. Speech Mode is guided practice that runs on this site. The calls with Mei, your real-life tutor, are part of the 7-Day Sprint.'),
    ('What happens when I make a mistake?', '¿Qué pasa cuando me equivoco?'),
    ('If your sentence contains a mistake that is common for Spanish speakers, such as "I have 25 years", you see a one-line fix with the reason it happens in Spanish.',
     'Si tu frase tiene un error típico de los hispanohablantes, como "I have 25 years", ves una corrección de una línea y por qué pasa desde el español.'),
    ('Is Speech Mode free?', '¿Modo Habla es gratis?'),
    ('Yes, while the site is in testing.',
     'Tiene una parte gratis: con tu cuenta lo usas cada día, con un límite. El Sprint de 7 días lo desbloquea todo, sin límites.',
     'There is a free part: with your account you use it every day, with a limit. The 7-Day Sprint unlocks everything, with no limits.'),
    ('Who are the Language Buddies?', '¿Quiénes son los Buddies?', 'Who are the Buddies?'),
    ("Ruby and Max, two 3D characters in Speech Mode. Ruby is from London and Max is from New York. They speak the tutor's lines, listen while you answer and react when you get a sentence right. You can switch between them, spin them and poke them.",
     'Kairo y May, dos personajes 3D de Modo Habla. Dicen las frases de la conversación, te escuchan mientras respondes y reaccionan cuando aciertas una frase. Puedes cambiar de uno a otro, girarlos y darles un toque.',
     'Kairo and May, two 3D characters in Speech Mode. They say the lines of the conversation, listen while you answer and react when you get a sentence right. You can switch between them, spin them and give them a poke.'),

    # ---------- Games page ----------
    ('English Speaking Games for Beginners | Week2Speak', 'Juegos para practicar inglés hablado | Week2Speak', 'Games to practise spoken English | Week2Speak'),
    ('Five short games that end with you speaking: Word Order, Fill the Gap, Flash Translate, Sound Lab and Quick Answers, with a pack for each Sprint day.',
     'Cinco juegos cortos de inglés para principiantes que terminan contigo hablando: Ordena la frase, Completa la frase, Traducción flash y dos más.',
     'Five short English games for beginners that end with you speaking: Word Order, Fill the Gap, Flash Translate and two more.'),
    ('English speaking games', 'Juegos para hablar inglés', 'Games for speaking English'),
    ('Five games with a new pack for every day of the Sprint. Build the sentence, hear the sound, answer the question, and say it out loud.',
     'Cinco juegos con un paquete nuevo para cada día del Sprint. Arma la frase, escucha el sonido, responde la pregunta y dilo en voz alta.'),
    ('Game', 'Juego'),
    ('Fill the Gap', 'Completa la frase'),
    ('Flash Translate', 'Traducción flash'),
    ('Sound Lab', 'Laboratorio de sonidos'),
    ('Quick Answers', 'Respuestas rápidas'),
    ('Sprint day', 'Día del Sprint'),
    ('Five games that end with you speaking', 'Cinco juegos que terminan contigo hablando'),
    ("Every game makes you build or hear English and then say it, so you practise speaking instead of only recognising answers. Each game has a pack for every day of the 7-Day Sprint, built from that day's lesson.",
     'En cada juego armas o escuchas una frase en inglés y luego la dices, así practicas hablando y no solo reconociendo respuestas. Cada juego tiene un paquete para cada día del Sprint de 7 días, hecho con la lección de ese día.'),
    ('How it works', 'Cómo funciona'),
    ('Best for', 'Ideal para'),
    ('Put shuffled word tiles in the right order, then say the sentence.', 'Ordena las fichas de palabras y luego di la frase.'),
    ('English word order, questions', 'El orden de las palabras en inglés, las preguntas'),
    ('Choose the missing word, then say the whole sentence. Each answer explains the rule in one line.', 'Elige la palabra que falta y luego di la frase entera. Cada respuesta explica la regla en una línea.'),
    ('Mistakes that come from Spanish', 'Errores que vienen del español'),
    ('See a short sentence in Spanish and say it in English.', 'Ves una frase corta en español y la dices en inglés.'),
    ('Thinking in English faster', 'Pensar en inglés más rápido'),
    ('Hear one of two similar words, such as ship and sheep, choose the one you heard, then say it.', 'Escuchas una de dos palabras parecidas, como ship y sheep, eliges la que oíste y luego la dices.'),
    ('The six sounds Spanish speakers find hardest', 'Los seis sonidos que más cuestan a los hispanohablantes'),
    ('Hear a question, then answer out loud in a full sentence. No text unless you ask for it.', 'Escuchas una pregunta y respondes en voz alta con una frase completa. Sin texto, salvo que lo pidas.'),
    ('Understanding real questions and answering fast', 'Entender preguntas reales y responder rápido'),
    ('Why do the games ask me to say the sentence?', '¿Por qué los juegos me piden decir la frase?'),
    ('Tapping the right answer trains recognition. Saying the whole sentence trains speaking, which is the skill the Sprint is built around.',
     'Tocar la respuesta correcta entrena el reconocimiento. Decir la frase entera entrena el habla, que es justo lo que trabaja el Sprint.'),
    ('How long is a round?', '¿Cuánto dura una ronda?'),
    ('Eight sentences in Word Order, Fill the Gap and Flash Translate, and six word pairs in Sound Lab. Most rounds take three to five minutes.',
     'Ocho frases en Ordena la frase, Completa la frase y Traducción flash, y seis pares de palabras en Laboratorio de sonidos. Casi todas las rondas duran de tres a cinco minutos.'),
    ('What is Quick Answers?', '¿Qué es Respuestas rápidas?'),
    ('A listening and speaking game. You hear a question such as "Where are you from?" and answer out loud in a full sentence. The words stay hidden unless you ask to see them, so you practise understanding by ear.',
     'Un juego para escuchar y hablar. Oyes una pregunta como "Where are you from?" y respondes en voz alta con una frase completa. Las palabras quedan ocultas salvo que pidas verlas, así practicas entender de oído.'),
    ('What is Sound Lab?', '¿Qué es el Laboratorio de sonidos?'),
    ('A listening game for the six sounds Spanish speakers find hardest in English, such as ship and sheep or think and sink. You hear one word, choose which one it was, then say it yourself.',
     'Un juego de escucha con los seis sonidos del inglés que más cuestan a los hispanohablantes, como ship y sheep o think y sink. Oyes una palabra, eliges cuál era y luego la dices tú.'),
    ('Are the games part of the 7-Day Sprint?', '¿Los juegos son parte del Sprint de 7 días?'),
    ("Yes. Every game has a pack for each day of the Sprint, built from the sentences in that day's lesson, and finishing a round ticks the task on your Sprint page.",
     'Sí. Cada juego tiene un paquete para cada día del Sprint, hecho con las frases de la lección de ese día, y al terminar una ronda se marca la tarea en tu página del Sprint.'),
    ('Do I need to know grammar first?', '¿Tengo que saber gramática antes?'),
    ('No. Fill the Gap explains each answer in one line after you choose, using the mistakes Spanish speakers make most.',
     'No. Completa la frase explica cada respuesta en una línea después de elegir, a partir de los errores más comunes de los hispanohablantes.'),

    # ---------- Shadowing page ----------
    ('English Shadowing Practice for Beginners | Week2Speak', 'Shadowing en inglés para principiantes | Week2Speak', 'English shadowing for beginners | Week2Speak'),
    ('Speak along with a native voice while the words light up. Shadow a clip for each Sprint day, or your own script, in American, British or Australian English.',
     'Habla a la vez que una voz nativa mientras se iluminan las palabras. Un clip por día del Sprint o tu propio guion, en tres acentos de inglés.',
     'Speak along with a native voice while the words light up. A clip for each Sprint day or your own script, in three English accents.'),
    ('English shadowing studio', 'Estudio de shadowing en inglés'),
    ('Shadowing means speaking along with a native voice, a beat behind it. It trains rhythm and sounds faster than reading rules about them.',
     'Hacer shadowing es hablar a la vez que una voz nativa, un pelín por detrás. Entrena el ritmo y los sonidos más rápido que leer reglas sobre ellos.'),
    ('Clip', 'Clip'),
    ('My script', 'Mi guion'),
    ('Type the sentences from your lesson, or your 2-minute talk. They stay on this device.', 'Escribe las frases de tu lección o tu charla de 2 minutos. Se quedan en este dispositivo.'),
    ('Save and shadow it', 'Guardar y hacer shadowing'),
    ('Accent', 'Acento'),
    ('Speed', 'Velocidad'),
    ('Steady', 'Pausada'),
    ('Mode', 'Modo'),
    ('What is shadowing?', '¿Qué es el shadowing?'),
    ('Shadowing is a speaking exercise where you listen to a native speaker and repeat what they say almost at the same time, a beat behind them. It trains the rhythm, stress and linked sounds of English, which reading rules does not.',
     'El shadowing es un ejercicio de habla: escuchas a un hablante nativo y repites lo que dice casi a la vez, un pelín por detrás. Entrena el ritmo, el acento de las palabras y cómo se unen los sonidos en inglés, algo que leer reglas no consigue.'),
    ('How to shadow in three steps', 'Cómo hacer shadowing en tres pasos'),
    ('Listen.', 'Escucha.'),
    ('Play the clip and follow the words as they light up.', 'Pon el clip y sigue las palabras mientras se iluminan.'),
    ('Shadow.', 'Acompaña.', 'Shadow.'),
    ('Speak along with the voice, a beat behind. Do it three times.', 'Habla a la vez que la voz, un pelín por detrás. Hazlo tres veces.'),
    ('Solo.', 'Tú solo.', 'Solo.'),
    ('The words light up at speaking pace with no voice, and you say the clip alone.', 'Las palabras se iluminan al ritmo del habla, sin voz, y dices el clip tú solo.'),
    ('There is a clip for every day of the 7-Day Sprint, from Introducing yourself to My talk, plus My script, where you type your own sentences and shadow them. Choose from three speeds and three accents: American, British and Australian.',
     'Hay un clip para cada día del Sprint de 7 días, de Presentarte a Mi charla, y además Mi guion, donde escribes tus propias frases y haces shadowing con ellas. Elige entre tres velocidades y tres acentos: estadounidense, británico y australiano.'),
    ('Source:', 'Fuente:'),
    ('script-enhanced shadowing study, Instructed Second Language Acquisition', 'estudio sobre shadowing con guion, Instructed Second Language Acquisition', 'study on shadowing with a script, Instructed Second Language Acquisition'),
    ('What is shadowing in language learning?', '¿Qué es el shadowing para aprender idiomas?'),
    ('Shadowing means listening to a native speaker and repeating what they say almost at the same time, a beat behind them. It trains the rhythm, linking and stress of English.',
     'Hacer shadowing es escuchar a un hablante nativo y repetir lo que dice casi a la vez, un pelín por detrás. Entrena el ritmo, la unión de sonidos y el acento de las palabras en inglés.'),
    ('Does shadowing improve your accent?', '¿El shadowing mejora tu pronunciación?', 'Does shadowing improve your pronunciation?'),
    ('It can help you hear and copy rhythm and linked sounds. Research on shadowing is still small: one study of 24 learners found it improved how well they heard linked sounds, while the gain in their own pronunciation was not statistically significant. Use it as daily practice, not as a guaranteed accent fix.',
     'Te puede ayudar a oír y copiar el ritmo y los sonidos que se unen. Todavía hay poca investigación: un estudio con 24 estudiantes vio que mejoraban al oír los sonidos unidos, pero la mejora en su propia pronunciación no fue estadísticamente significativa. Úsalo como práctica diaria, no como un arreglo garantizado del acento.'),
    ('How long should I shadow each day?', '¿Cuánto tiempo hago shadowing al día?'),
    ('Five minutes is enough. Shadow one clip three times at Steady speed, then once at Natural speed in Solo mode.',
     'Con cinco minutos basta. Haz shadowing de un clip tres veces a velocidad Pausada y luego una vez a velocidad Natural en modo Solo.'),

    # ---------- the Sprint page (legacy tools inside the paid area, JSON-LD) ----------
    ('7-Day English Speaking Sprint', 'Sprint de 7 días para hablar inglés'),
    ('Seven days, twenty minutes a day and a tutor who speaks your language. For Spanish speakers starting from zero who want to say their first sentences.',
     'Siete días, veinte minutos al día y una tutora que habla tu idioma. Para hispanohablantes que empiezan de cero y quieren decir sus primeras frases.'),
    ('Sprint progress', 'Progreso del Sprint'),
    ('Your before and after', 'Tu antes y después'),
    ('Read the Sprint card out loud on Day 1, and again on Day 7. The same five sentences, seven days apart. Recordings stay on this device until you send them.',
     'Lee la tarjeta del Sprint en voz alta el Día 1 y otra vez el Día 7. Las mismas cinco frases, con siete días de diferencia. Las grabaciones se quedan en este dispositivo hasta que las envíes.'),
    ('Day 7: your 2-minute talk', 'Día 7: tu charla de 2 minutos'),
    ('Four parts, thirty seconds each: who you are, what you like, what you did last week, and why you are learning English. No script. Keep going until the clock stops.',
     'Cuatro partes de treinta segundos: quién eres, qué te gusta, qué hiciste la semana pasada y por qué aprendes inglés. Sin guion. Sigue hasta que pare el reloj.'),
    ('Start the clock', 'Empezar el reloj'),
    ('Can you really learn to speak English in 7 days?', '¿De verdad se aprende a hablar inglés en 7 días?'),
    ('You will not be fluent. You will have said hundreds of real sentences out loud, learned the phrases for six everyday situations, and given a 2-minute talk on Day 7. For learners who freeze when they speak, that first week is the hardest part.',
     'No vas a hablar con fluidez. Habrás dicho cientos de frases reales en voz alta, aprendido las frases de seis situaciones del día a día y dado una charla de 2 minutos al final. Si te bloqueas al hablar, esa primera semana es la parte más difícil.',
     'You will not be fluent. You will have said hundreds of real sentences out loud, learned the phrases for six everyday situations and given a 2-minute talk at the end. If you freeze when you speak, that first week is the hardest part.'),
    ('How much time does the Sprint take each day?', '¿Cuánto tiempo al día lleva el Sprint?'),
    ('About 20 minutes, in three steps: learn (the lesson and the sound of the day), practise (a game and a spoken scene), and speak (a voice note of up to 60 seconds to your tutor).',
     'Unos 20 minutos, en tres pasos: aprende (la lección y el sonido del día), practica (un juego y una escena hablada) y habla (el reto del día, en voz alta). Si quieres, le mandas un audio a Mei por WhatsApp.',
     'About 20 minutes, in three steps: learn (the lesson and the sound of the day), practise (a game and a spoken scene) and speak (the challenge of the day, out loud). If you like, you send Mei an audio on WhatsApp.'),
    ('What are the two calls with the tutor?', '¿Cómo son las dos llamadas con Mei?', 'What are the two calls with Mei like?'),
    ('On Day 1, a 45-minute Kickoff call: your goals, a short recording of where you start, and five sentences about yourself. On Day 7, a 45-minute Showcase call: your 2-minute talk, your Day 1 and Day 7 recordings side by side, and a short live lesson.',
     'Son dos llamadas 1 a 1 de 25 minutos. La primera, para arrancar: tus objetivos y tus primeras frases sobre ti. La última, para tu charla de 2 minutos delante de Mei.',
     'They are two 25-minute 1-to-1 calls. The first, to get started: your goals and your first sentences about yourself. The last, for your 2-minute talk in front of Mei.'),
    ('What happens after the Sprint?', '¿Qué pasa después del Sprint?'),
    ('If you want to keep going, you can join the 12-week programme with weekly lessons with the same tutor. There is no obligation.',
     'Te llevas tu antes y después grabado, tu biblioteca de recursos y un plan de 30 días para seguir practicando por tu cuenta.',
     'You keep your before and after recordings, your resource library and a 30-day plan to keep practising on your own.'),
    ('What homework is there?', '¿Hay deberes?', 'Is there homework?'),
    ('No written homework. Each day has six short tasks on this site: a lesson, a sound game, a clip to shadow, a sentence game, a spoken scene, and one voice note to your tutor. The page ticks them off as you finish.',
     'No hay deberes escritos. Cada día tiene tareas cortas en esta web: una lección, un juego de sonidos, un clip de shadowing, un juego de frases, una escena hablada y el reto del día. Se marcan solas cuando las terminas.',
     'There is no written homework. Each day has short tasks on this site: a lesson, a sound game, a shadowing clip, a sentence game, a spoken scene and the challenge of the day. They tick themselves off as you finish.'),
    ('What if I miss a day?', '¿Y si me salto un día?'),
    ('You can catch up the next day. The Sprint is about doing a little every day, not doing it perfectly.',
     'Lo recuperas al día siguiente. El Sprint va de hacer un poco cada día, no de hacerlo perfecto.'),

    # ---------- Course page ----------
    ('Free 7-Lesson English Speaking Course | Week2Speak', 'Curso de inglés para principiantes: 7 lecciones | Week2Speak', 'English course for beginners: 7 lessons | Week2Speak'),
    ('Seven short English lessons for Spanish speakers, one a day. Each has five key phrases, one mistake that comes from Spanish, and a speaking task.',
     'Siete lecciones cortas de inglés para hispanohablantes, una al día: cinco frases clave, un error típico del español y una tarea para hablar.'),
    ('Week2Speak 7-lesson English speaking course', 'Curso de Week2Speak para hablar inglés en 7 lecciones'),
    ('Free English speaking course', 'Curso para hablar inglés', 'English speaking course'),
    ('Seven lessons, one a day. Each has the phrases to learn, a mistake that comes from Spanish, and practice in the rooms.',
     'Siete lecciones, una al día. Cada una trae las frases que vas a aprender, un error que viene del español y práctica en las salas. Las lecciones 1 y 2 son gratis con tu cuenta.',
     'Seven lessons, one a day. Each brings the phrases you will learn, a mistake that comes from Spanish and practice in the rooms. Lessons 1 and 2 are free with your account.'),
    ('Lessons', 'Lecciones'),
    ('All seven lessons', 'Las siete lecciones'),
    ('The course has seven short lessons, one for each day of the Sprint. Each lesson takes 12 minutes or less and covers five key phrases with their Spanish meaning, one mistake that comes from Spanish, and a voice note to send to your tutor.',
     'El curso tiene siete lecciones cortas, una para cada día del Sprint. Cada lección dura 12 minutos o menos y trae cinco frases clave con su significado en español, un error que viene del español y una tarea para practicar en voz alta.',
     'The course has seven short lessons, one for each day of the Sprint. Each lesson takes 12 minutes or less and brings five key phrases with their Spanish meaning, one mistake that comes from Spanish and a task to practise out loud.'),
    ('Lesson 1: Me', 'Lección 1: Yo'),
    ('Lesson 2: Order and ask', 'Lección 2: Pedir y preguntar'),
    ('Lesson 3: Questions', 'Lección 3: Preguntas'),
    ('Lesson 4: Yesterday', 'Lección 4: Ayer'),
    ('Lesson 5: Opinions', 'Lección 5: Opiniones'),
    ('Lesson 6: Keep talking', 'Lección 6: Sigue hablando'),
    ('Lesson 7: The 2-minute talk', 'Lección 7: La charla de 2 minutos'),
    ('Key phrases:', 'Frases clave:'),
    ('Mistake from Spanish:', 'Error que viene del español:'),
    ('→ I&#x27;m thirty. Use "be" for age: "I am 25 years old."', '→ I\'m thirty. Para la edad se usa "be": "I am 25 years old."'),
    ('→ I&#x27;m hungry. Use "be": "I am hungry", "you are right".', '→ I\'m hungry. Con hambre, sed o frío, y para "tener razón", se usa "be": "I am hungry", "you are right".'),
    ('→ It&#x27;s very far. English always needs a subject: "It is raining."', '→ It\'s very far. En inglés la frase siempre necesita sujeto: "It is raining."'),
    ('→ Last week I worked. No "the": "last week", "next year".', '→ Last week I worked. Sin "the": "last week", "next year".'),
    ('→ I agree with you. "Agree" is already the verb: "I agree."', '→ I agree with you. "Agree" ya es el verbo: "I agree."'),
    ('→ I don&#x27;t know anything about it. Use "anything" or "anybody" after "not".', '→ I don\'t know anything about it. Después de "not" se usa "anything" o "anybody".'),
    ('→ I like playing football. After "like", use -ing: "I like playing football."', '→ I like playing football. Después de "like" se usa -ing: "I like playing football."'),
    ('Is the course free?', '¿El curso es gratis?'),
    ('How long is each lesson?', '¿Cuánto dura cada lección?'),
    ('Twelve minutes or less. Each lesson has five key phrases, one mistake that comes from Spanish, and a practice task.',
     'Doce minutos o menos. Cada lección tiene cinco frases clave, un error que viene del español y una tarea de práctica.'),
    ('Do I need a teacher to use the course?', '¿Necesito un profesor para hacer el curso?'),
    ('No. You can work through the lessons alone. The 7-Day Sprint adds two live calls and daily feedback on your voice notes.',
     'No. Puedes hacer las lecciones por tu cuenta. El Sprint de 7 días suma dos llamadas en directo con Mei y su WhatsApp toda la semana.',
     'No. You can do the lessons on your own. The 7-Day Sprint adds two live calls with Mei and her WhatsApp all week.'),

    # ---------- Common mistakes page ----------
    ('16 English Mistakes Spanish Speakers Make | Week2Speak', '16 errores típicos en inglés que debes evitar | Week2Speak', '16 typical English mistakes to avoid | Week2Speak'),
    ('The 16 most common English mistakes Spanish speakers make, like "I have 25 years" and "I am agree", with the correct sentence and why each one happens.',
     'Los 16 errores de inglés más comunes de los hispanohablantes, como "I have 25 years" o "I am agree", con la frase correcta y por qué pasan.'),
    ('The 16 most common English mistakes Spanish speakers make, with the wrong sentence, the right one, and the Spanish pattern behind each.',
     'Los 16 errores de inglés más comunes de los hispanohablantes, con la frase incorrecta, la correcta y el patrón del español que hay detrás de cada uno.'),
    ('English mistakes Spanish speakers make', 'Errores de inglés que cometen los hispanohablantes'),
    ('Most mistakes Spanish speakers make in English are Spanish grammar carried across word for word. Here are the 16 we see most, each with the wrong sentence, the right one, and the Spanish pattern behind it.',
     'Casi todos los errores que cometemos los hispanohablantes en inglés son gramática del español pasada palabra por palabra. Aquí tienes los 16 que más vemos, cada uno con la frase incorrecta, la correcta y el patrón del español que hay detrás.'),
    ('Last updated 11 November 2026', 'Actualizado el 11 de noviembre de 2026'),
    ('Mistakes in this guide', 'Errores de esta guía'),
    ('Age with "have"', 'La edad con "have"'),
    ('1. Age with "have"', '1. La edad con "have"'),
    ('"Have" for feelings', '"Have" para sensaciones'),
    ('2. "Have" for feelings', '2. "Have" para sensaciones'),
    ('Missing subject', 'Falta el sujeto'),
    ('5. Missing subject', '5. Falta el sujeto'),
    ('8. "For" + verb', '8. "For" + verbo'),
    ('Double negative', 'Doble negación'),
    ('14. Double negative', '14. Doble negación'),
    ('Present with "since"', 'Presente con "since"'),
    ('15. Present with "since"', '15. Presente con "since"'),
    ('"Like" + plain verb', '"Like" + verbo sin -ing'),
    ('16. "Like" + plain verb', '16. "Like" + verbo sin -ing'),
    ('Use "be" for age: "I am 25 years old." Spanish says "tengo 25 años".', 'Para la edad se usa "be": "I am 25 years old." En español decimos "tengo 25 años".'),
    ('Use "be": "I am hungry", "you are right". Spanish says "tengo hambre".', 'Con hambre, sed o frío, y para "tener razón", se usa "be": "I am hungry", "you are right". En español decimos "tengo hambre".'),
    ('"Agree" is already the verb: "I agree." Spanish says "estoy de acuerdo".', '"Agree" ya es el verbo: "I agree." En español decimos "estoy de acuerdo".'),
    ('"People" is plural: "people are". "La gente" is singular in Spanish.', '"People" es plural: "people are". En español, "la gente" es singular.'),
    ('English always needs a subject: "It is raining." Spanish can drop it: "está lloviendo".', 'En inglés la frase siempre necesita sujeto: "It is raining." En español lo podemos quitar: "está lloviendo".'),
    ('It is "depend on". Spanish says "depende de".', 'Se dice "depend on". En español decimos "depende de".'),
    ('Say "explain it to me" or "tell me". Spanish says "explícame", "dime".', 'Di "explain it to me" o "tell me". En español decimos "explícame", "dime".'),
    ('Use "to" for a purpose: "to learn English". Spanish says "para aprender".', 'Para decir para qué haces algo se usa "to": "to learn English". En español decimos "para aprender".'),
    ('No "the": "last week", "next year". Spanish says "la semana pasada".', 'Sin "the": "last week", "next year". En español decimos "la semana pasada".'),
    ('One comparative is enough: "better", "easier". A copy of "más".', 'Con un comparativo basta: "better", "easier". Es una copia del "más" del español.'),
    ('These go with "make": "make a mistake". "Hacer" is both do and make.', 'Estas van con "make": "make a mistake". En español "hacer" sirve para do y para make.'),
    ('It is "married to". Spanish says "casado con".', 'Se dice "married to". En español decimos "casado con".'),
    ('Say "I want you to come." Spanish says "quiero que vengas".', 'Di "I want you to come." En español decimos "quiero que vengas".'),
    ('Use "anything" or "anybody" after "not". Spanish doubles it: "no tengo nada".', 'Después de "not" usa "anything" o "anybody". El español repite la negación: "no tengo nada".'),
    ('Use "have": "I have lived here since 2020." Spanish uses the present: "vivo aquí desde".', 'Usa "have": "I have lived here since 2020." En español usamos el presente: "vivo aquí desde".'),
    ('After "like", use -ing: "I like playing football." Spanish says "me gusta jugar".', 'Después de "like" usa -ing: "I like playing football." En español decimos "me gusta jugar".'),
    ('How to stop making them', 'Cómo dejar de cometerlos'),
    ('Knowing the rule is not enough; the fix has to come out of your mouth without thinking. Say the correct sentence out loud five times, then use it in a real answer.',
     'Saber la regla no basta: la frase correcta tiene que salirte sin pensar. Di la frase correcta en voz alta cinco veces y luego úsala en una respuesta de verdad.'),
    ('flags these mistakes as you answer, and', 'detecta estos errores mientras respondes, y'),
    ('drills them one by one.', 'te los hace practicar uno a uno.'),

    # ---------- About page ----------
    ('How Week2Speak Teaches English', 'Cómo enseñamos inglés en Week2Speak'),
    ('Week2Speak gets Spanish speakers saying English sentences from day one: speaking first, task-based lessons, spaced review and feedback on Spanish-speaker errors.',
     'Cómo Week2Speak te hace decir frases en inglés desde el primer día: primero hablar, tareas reales, repaso espaciado y corrección de errores del español.',
     'How Week2Speak gets you saying English sentences from the first day: speaking first, real tasks, spaced review and fixes for errors from Spanish.'),
    ('How Week2Speak teaches English', 'Cómo enseñamos inglés en Week2Speak'),
    ('Week2Speak gets Spanish speakers saying real English sentences from the first day, with a tutor who speaks Spanish and short daily practice in between.',
     'En Week2Speak dices frases reales en inglés desde el primer día, con una tutora que habla español y práctica corta cada día.',
     'At Week2Speak you say real English sentences from the first day, with a tutor who speaks Spanish and short practice every day.'),
    ('Why we start with speaking', 'Por qué empezamos hablando'),
    ('Many Spanish speakers study English for years at school and still freeze when they have to speak. They have learned about English but have rarely produced it. Week2Speak reverses the order: you say a sentence first, then look at the grammar that came up in what you said.',
     'Muchos hispanohablantes estudian inglés años en el colegio y aun así se bloquean al hablar. Han aprendido sobre el inglés, pero casi nunca lo han dicho. Week2Speak le da la vuelta: primero dices una frase y después miras la gramática que salió en lo que dijiste.'),
    ('The method', 'El método'),
    ('Speak from day one.', 'Habla desde el primer día.'),
    ('On Day 1 you build five true sentences about yourself and say them out loud. Researchers such as Merrill Swain argue that producing language is what shows learners the gaps in what they know (',
     'El Día 1 armas cinco frases verdaderas sobre ti y las dices en voz alta. Investigadoras como Merrill Swain sostienen que producir el idioma es lo que te muestra los huecos en lo que sabes ('),
    ('comprehensible output', 'output comprensible'),
    ('Task first, grammar after.', 'Primero la tarea, después la gramática.'),
    ('Each lesson and call starts with a real task, like ordering in a café, and corrections come from your own sentences. This follows task-based teaching (',
     'Cada lección y cada llamada empieza con una tarea real, como pedir en un café, y las correcciones salen de tus propias frases. Así funciona la enseñanza basada en tareas ('),
    ("Willis's framework", 'el modelo de Willis', "Willis's model"),
    ('Little and often.', 'Poco y a menudo.'),
    ('Lessons are 12 minutes or less, and sentences you learned come back on later days. Reviews of the research find spaced repetition helps vocabulary stick (',
     'Las lecciones duran 12 minutos o menos, y las frases que aprendiste vuelven en los días siguientes. Las revisiones de la investigación ven que la repetición espaciada ayuda a fijar el vocabulario ('),
    ('systematic review, 2026', 'revisión sistemática, 2026'),
    ('Mistakes from Spanish, fixed in Spanish.', 'Errores del español, explicados en español.', 'Mistakes from Spanish, explained in Spanish.'),
    ('The feedback targets the errors Spanish grammar causes, explained with the Spanish pattern behind them. See',
     'Las correcciones van a los errores que causa la gramática del español, explicados con el patrón del español que hay detrás. Mira'),
    ('the 16 most common', 'los 16 más comunes'),
    ('Who is behind Week2Speak', 'Quién está detrás de Week2Speak'),
    ('Week2Speak was started by an English tutor who speaks Spanish, Portuguese and English, together with a partner who builds the practice tools. It is in testing, in English, with a free founding cohort of ten learners. A Spanish version of the site comes next.',
     'Week2Speak lo empezó Mei, una tutora de inglés que habla español, portugués e inglés, junto con un compañero que construye las herramientas de práctica. Estamos en fase de prueba, con cinco plazas para el Sprint de 7 días.',
     'Week2Speak was started by Mei, an English tutor who speaks Spanish, Portuguese and English, together with a partner who builds the practice tools. We are in testing, with five places in the 7-Day Sprint.'),

    # ---------- 404 ----------
    ('Page not found | Week2Speak', 'Página no encontrada | Week2Speak'),
    ('This page does not exist.', 'Esta página no existe.'),
    ('That page does not exist.', 'Esa página no existe.'),
    ('The link may be old, or the address has a typo.', 'Puede que el enlace sea antiguo o que la dirección tenga un error.'),
    ('Go to the home page', 'Ir al inicio'),
    ('See the 7-Day Sprint', 'Ver el Sprint de 7 días'),
    # the privacy page's title and description (the page itself is bilingual in privacy_content.py)
    ('Privacy Notice | Week2Speak', 'Aviso de privacidad | Week2Speak', 'Privacy notice | Week2Speak'),
    ('How Week2Speak collects, uses and protects your personal data: your account, practice progress, the Sprint, the providers we use and your rights.',
     'Qué datos recoge Week2Speak y cómo los protege: tu cuenta, tu progreso, el Sprint, los proveedores que usamos y tus derechos.',
     'What data Week2Speak collects and how it protects it: your account, your progress, the Sprint, the providers we use and your rights.'),
]
