"""The paid 7-Day Sprint: what a student opens each day. Written in Spanish; English follows the Spanish.
Served as /paid/sprint.es.json and /paid/sprint.en.json, which the Worker only gives to paid students.
English the learner practises stays English in both files (phrases are [English, Spanish])."""
import sprint_content as S

# Day 0 is the warm-up before Monday; days 1-7 follow the Sprint's DAYS.
DAYS = [
 {'n': 0,
  'title': ('Antes de empezar', 'Before you start'),
  'brief': ('¡Hola! Soy May. Esta semana vas a decir tus primeras frases en inglés en voz alta. No hace falta que sean perfectas: hace falta que salgan. Hoy solo preparamos el terreno.',
            "Hi! I'm May. This week you're going to say your first English sentences out loud. They don't have to be perfect: they just have to come out. Today we only get ready."),
  'why': ('Lo que más frena a un principiante no es la gramática: es el miedo a abrir la boca. Por eso empezamos grabándote tal como estás hoy.',
          "What holds a beginner back most isn't grammar: it's the fear of opening your mouth. That's why we start by recording you exactly as you are today."),
  'steps': [('Reserva tu primera llamada con Mei (25 minutos).', 'Book your first call with Mei (25 minutes).', 'book'),
            ('Escríbele un «hola» a Mei por WhatsApp.', 'Send Mei a "hello" on WhatsApp.', 'whatsapp'),
            ('Graba tu Día 1: lee la tarjeta en voz alta, aunque te salga mal.', 'Record your Day 1: read the card out loud, even if it comes out badly.', 'record'),
            ('Escribe tres razones por las que quieres hablar inglés.', 'Write down three reasons you want to speak English.', 'reasons'),
            ('Añade la semana a tu calendario: 20 minutos al día.', 'Add the week to your calendar: 20 minutes a day.', 'calendar')],
  'challenge': ('Di en voz alta: «Hi, I\'m …». Solo eso. Ya has empezado.', 'Say out loud: "Hi, I\'m …". Just that. You\'ve started.'),
 },
 {'n': 1,
  'brief': ('Hoy hablas de ti. Nombre, de dónde eres, a qué te dedicas, qué te gusta. Son las frases que vas a usar en todas las conversaciones de tu vida.',
            "Today you talk about yourself. Your name, where you're from, what you do, what you like. These are the sentences you'll use in every conversation of your life."),
  'why': ('Presentarte sin leer es la primera victoria. Cuando te sale sola, el resto de la conversación ya no da tanto miedo.',
          "Introducing yourself without reading is the first win. Once it comes out on its own, the rest of the conversation stops being so scary."),
  'freeze': [["Sorry, I'm a bit nervous.", 'Perdona, estoy un poco nervioso.'], ['My English is not very good, but I\'m learning.', 'Mi inglés no es muy bueno, pero estoy aprendiendo.'], ['Can you speak slowly, please?', '¿Puedes hablar despacio, por favor?']],
  'mistake': ('Para la edad no se usa «have»: en inglés eres tus años.', 'You don\'t use "have" for age: in English you are your years.'),
  'challenge': ('Preséntate en voz alta delante del espejo, cinco frases, sin mirar el móvil.', 'Introduce yourself out loud in front of the mirror, five sentences, without looking at your phone.'),
 },
 {'n': 2,
  'brief': ('Hoy pides cosas: un café, algo de comer, la cuenta. En inglés pedir con «I\'d like» y «Can I have» suena educado y natural.',
            'Today you ask for things: a coffee, something to eat, the bill. In English, asking with "I\'d like" and "Can I have" sounds polite and natural.'),
  'why': ('Pedir es la situación real más común cuando viajas. Si sabes pedir, ya te puedes mover solo.', "Ordering is the most common real situation when you travel. If you can order, you can get by on your own."),
  'freeze': [['Sorry, what was that?', 'Perdona, ¿qué has dicho?'], ['Just this one, please.', 'Solo este, por favor.'], ['Can I pay by card?', '¿Puedo pagar con tarjeta?']],
  'mistake': ('«Give me a coffee» suena brusco en inglés. Usa «Can I have…?» o «I\'d like…».', '"Give me a coffee" sounds rude in English. Use "Can I have…?" or "I\'d like…".'),
  'challenge': ('Pide tu desayuno de hoy en inglés, en voz alta, aunque estés en casa.', 'Order today\'s breakfast in English, out loud, even if you\'re at home.'),
 },
 {'n': 3,
  'brief': ('Hoy preguntas: dónde está algo, a qué hora sale algo, cómo se llega. Una buena pregunta te salva en cualquier sitio.',
            'Today you ask questions: where something is, what time something leaves, how to get there. A good question saves you anywhere.'),
  'why': ('Quien pregunta, dirige la conversación. Y cuando no entiendas la respuesta, también sabrás qué decir.', "Whoever asks the questions leads the conversation. And when you don't understand the answer, you'll know what to say too."),
  'freeze': [['Sorry, can you repeat that?', 'Perdona, ¿puedes repetirlo?'], ['Can you show me on the map?', '¿Me lo puedes enseñar en el mapa?'], ['Left or right?', '¿A la izquierda o a la derecha?']],
  'mistake': ('En las preguntas, el verbo va antes: «Where is the bathroom?», no «Where the bathroom is?».', 'In questions the verb comes first: "Where is the bathroom?", not "Where the bathroom is?".'),
  'challenge': ('Hazle tres preguntas en inglés a alguien (o a tu mascota). Lo importante es decirlas.', 'Ask someone (or your pet) three questions in English. What matters is saying them.'),
 },
 {'n': 4,
  'brief': ('Hoy cuentas lo que hiciste ayer. El pasado parece difícil, pero con diez verbos ya puedes contar casi todo.',
            "Today you tell what you did yesterday. The past looks hard, but with ten verbs you can already tell almost anything."),
  'why': ('Contar tu día es lo que hace que una charla dure más de un minuto.', 'Telling your day is what makes a chat last more than a minute.'),
  'freeze': [['Let me think…', 'Déjame pensar…'], ['How do you say «…» in English?', '¿Cómo se dice «…» en inglés?'], ['It was a normal day.', 'Fue un día normal.']],
  'mistake': ('Después de «did» el verbo vuelve a su forma base: «I didn\'t go», no «I didn\'t went».', 'After "did" the verb goes back to its base form: "I didn\'t go", not "I didn\'t went".'),
  'challenge': ('Cuenta tu día de ayer en cuatro frases antes de dormir.', 'Tell your yesterday in four sentences before you go to sleep.'),
 },
 {'n': 5,
  'brief': ('Hoy das tu opinión. «I think», «I agree», «It depends». Con estas tres frases ya puedes participar en cualquier charla.',
            'Today you give your opinion. "I think", "I agree", "It depends". With these three you can join any chat.'),
  'why': ('Opinar te convierte de oyente en participante. Y no hace falta tener razón: hace falta decir algo.', "Giving an opinion turns you from a listener into a participant. You don't need to be right: you need to say something."),
  'freeze': [['Good question.', 'Buena pregunta.'], ["I'm not sure, but I think…", 'No estoy seguro, pero creo que…'], ['What about you?', '¿Y tú?']],
  'mistake': ('«I am agree» no existe. Es «I agree», sin «am».', '"I am agree" doesn\'t exist. It\'s "I agree", without "am".'),
  'challenge': ('Da tu opinión en voz alta sobre algo que veas hoy: una comida, una canción, una noticia.', 'Give your opinion out loud on something you see today: a meal, a song, a piece of news.'),
 },
 {'n': 6,
  'brief': ('Hoy aprendes a no quedarte callado. Cuando no sabes una palabra, hay frases que te dan tiempo y mantienen viva la conversación.',
            "Today you learn not to go silent. When you don't know a word, there are phrases that buy you time and keep the conversation alive."),
  'why': ('Nadie habla sin huecos, ni siquiera en su idioma. La diferencia es saber qué decir mientras piensas.', "Nobody speaks without gaps, not even in their own language. The difference is knowing what to say while you think."),
  'freeze': [['Let me think for a second.', 'Déjame pensar un segundo.'], ["It's like… how can I say it…", 'Es como… ¿cómo lo digo…?'], ['What I mean is…', 'Lo que quiero decir es…']],
  'mistake': ('«I don\'t know nothing» lleva dos negaciones. En inglés basta una: «I don\'t know anything».', '"I don\'t know nothing" has two negatives. English needs one: "I don\'t know anything".'),
  'challenge': ('Habla un minuto seguido sobre tu ciudad. Cuando te bloquees, usa una frase de rescate y sigue.', 'Talk for one minute about your city. When you get stuck, use a rescue phrase and keep going.'),
 },
 {'n': 7,
  'brief': ('Hoy es tu día: dos minutos hablando en inglés. Quién eres, qué te gusta, qué hiciste la semana pasada y por qué aprendes inglés. Sin guion.',
            "Today is your day: two minutes speaking English. Who you are, what you like, what you did last week and why you're learning English. No script."),
  'why': ('Comparar tu Día 1 con tu Día 7 es la prueba de que esta semana ha servido. Y te la llevas grabada.', "Comparing your Day 1 with your Day 7 is the proof that this week worked. And you keep it on record."),
  'freeze': [['Another thing is…', 'Otra cosa es…'], ['To finish…', 'Para terminar…'], ['Thank you for listening.', 'Gracias por escucharme.']],
  'mistake': ('«Explain me» no se dice. Es «explain to me» o «tell me».', 'You don\'t say "explain me". It\'s "explain to me" or "tell me".'),
  'challenge': ('Haz tu charla de 2 minutos en tu llamada final con Mei, y graba tu Día 7.', 'Give your 2-minute talk on your final call with Mei, and record your Day 7.'),
 },
]

REFLECT = [('¿Qué frase de hoy te salió mejor?', 'Which sentence came out best today?'),
           ('Del 1 al 5, ¿cuánto miedo te dio hablar hoy?', 'From 1 to 5, how scary was speaking today?')]

# The library. Items are [English, Spanish] when they are phrases to say; tips are (heading, text) per language.
LIBRARY = [
 {'id': 'survival', 'icon': 'life',
  'title': ('Kit de supervivencia: 30 frases para no quedarte en blanco', 'Survival kit: 30 phrases so you never go blank'),
  'desc': ('Las frases que te sacan de cualquier apuro. Guárdalas en el móvil.', 'The phrases that get you out of any jam. Keep them on your phone.'),
  'groups': [
   (('Cuando no entiendes', "When you don't understand"), [["Sorry, could you say that again?", 'Perdona, ¿puedes repetirlo?'], ["Could you speak more slowly, please?", '¿Puedes hablar más despacio, por favor?'], ["What does that mean?", '¿Qué significa eso?'], ["Sorry, I didn't catch that.", 'Perdona, no lo he pillado.'], ["Can you write it down, please?", '¿Me lo puedes escribir, por favor?'], ["Do you mean…?", '¿Quieres decir…?']]),
   (('Cuando te falta una palabra', "When you're missing a word"), [["How do you say «…» in English?", '¿Cómo se dice «…» en inglés?'], ["It's like a…", 'Es como un…'], ["I don't know the word, but…", 'No sé la palabra, pero…'], ["The thing you use for…", 'La cosa que se usa para…'], ["Let me think for a second.", 'Déjame pensar un segundo.'], ["What I mean is…", 'Lo que quiero decir es…']]),
   (('Para mantener la conversación', 'To keep the conversation going'), [["What about you?", '¿Y tú?'], ["Really? Tell me more.", '¿En serio? Cuéntame más.'], ["That's interesting.", 'Qué interesante.'], ["Me too.", 'Yo también.'], ["I agree.", 'Estoy de acuerdo.'], ["Why do you think that?", '¿Por qué lo piensas?']]),
   (('Para ser amable', 'To be polite'), [["Excuse me…", 'Disculpe…'], ["Could you help me, please?", '¿Me podría ayudar, por favor?'], ["Thank you so much.", 'Muchísimas gracias.'], ["No problem.", 'No hay problema.'], ["Sorry, my mistake.", 'Perdón, fue culpa mía.'], ["Have a nice day!", '¡Que tengas un buen día!']]),
   (('Para salir del paso', 'To get by'), [["I'm learning English.", 'Estoy aprendiendo inglés.'], ["Can I pay by card?", '¿Puedo pagar con tarjeta?'], ["Where is the nearest…?", '¿Dónde está el … más cercano?'], ["How much is it?", '¿Cuánto cuesta?'], ["I'm looking for…", 'Estoy buscando…'], ["Is it far from here?", '¿Está lejos de aquí?']]),
  ]},
 {'id': 'sounds', 'icon': 'sound',
  'title': ('Pronunciación: 8 sonidos que delatan a un hispanohablante', 'Pronunciation: 8 sounds that give away a Spanish speaker'),
  'desc': ('No necesitas un acento perfecto. Con estos ocho ajustes te van a entender mucho mejor.', "You don't need a perfect accent. With these eight tweaks you'll be understood much better."),
  'tips': [
   (('Sin «e» delante de la s', 'No "e" before s'), ('Decimos «espain» o «estudent». La s va sola: «Spain», «student». Empieza con un siseo: sss-pain.', 'We say "espain" or "estudent". The s goes on its own: "Spain", "student". Start with a hiss: sss-pain.'), ['Spain', 'student', 'school', 'speak']),
   (('La «th» de «think»', 'The "th" in "think"'), ('Saca un poco la lengua entre los dientes y sopla. Como la z de España: «think», «thank you».', 'Stick your tongue out a little between your teeth and blow. Like the z in Spain: "think", "thank you".'), ['think', 'three', 'thank you', 'birthday']),
   (('«ship» y «sheep» no son iguales', '"ship" and "sheep" are not the same'), ('La i corta (ship, live, it) es más relajada que nuestra i. La larga (sheep, leave, eat) se alarga.', 'The short i (ship, live, it) is more relaxed than our i. The long one (sheep, leave, eat) is stretched.'), ['ship / sheep', 'live / leave', 'it / eat']),
   (('La «v» suave', 'The soft "v"'), ('En inglés la v se hace con los dientes de arriba sobre el labio de abajo: «very», «video».', 'In English the v is made with your top teeth on your bottom lip: "very", "video".'), ['very', 'video', 'have', 'love']),
   (('La «h» se oye', 'The "h" is heard'), ('No es muda: es un soplido suave, como una j muy flojita. «hello», «house», «happy».', "It's not silent: it's a soft breath, like a very gentle j. \"hello\", \"house\", \"happy\"."), ['hello', 'house', 'happy', 'hotel']),
   (('El final «-ed»', 'The "-ed" ending'), ('Casi nunca suena «ed». «worked» suena «workt», «played» suena «pleid». Solo con t o d delante suena «id»: «wanted».', 'It almost never sounds "ed". "worked" sounds "workt", "played" sounds "pleid". Only after t or d is it "id": "wanted".'), ['worked', 'played', 'watched', 'wanted']),
   (('La «j» y la «y»', 'The "j" and the "y"'), ('La j inglesa suena «ch» suave con voz: «job», «January». La y es como nuestra i: «yes», «you».', 'The English j sounds like a voiced, soft "ch": "job", "January". The y is like our i: "yes", "you".'), ['job', 'January', 'yes', 'you']),
   (('El acento de la palabra', 'Word stress'), ('Una sílaba suena más fuerte que las demás, y si la cambias, cambia la palabra: «PHOtograph», «phoTOgraphy».', 'One syllable sounds stronger than the rest, and if you move it, the word changes: "PHOtograph", "phoTOgraphy".'), ['PHOtograph', 'phoTOgraphy', 'comFORtable', 'deVELop']),
  ]},
 {'id': 'intro', 'icon': 'user',
  'title': ('Tu presentación en 30 segundos', 'Your 30-second introduction'),
  'desc': ('Una plantilla para rellenar con tu vida. Apréndetela y la usarás siempre.', "A template to fill in with your life. Learn it and you'll use it forever."),
  'template': [["Hi, I'm ____.", 'Hola, soy ____.'], ["I'm from ____, in ____.", 'Soy de ____, en ____.'], ["I'm a ____ / I work in ____.", 'Soy ____ / Trabajo en ____.'], ["I live in ____ with ____.", 'Vivo en ____ con ____.'], ["In my free time I like ____ and ____.", 'En mi tiempo libre me gusta ____ y ____.'], ["I'm learning English because ____.", 'Estoy aprendiendo inglés porque ____.'], ["Nice to meet you!", '¡Encantado de conocerte!']]},
 {'id': 'questions', 'icon': 'chat',
  'title': ('20 preguntas para que la charla no se apague', '20 questions to keep a chat alive'),
  'desc': ('Cuando no sepas qué decir, pregunta. A la gente le encanta hablar de sí misma.', "When you don't know what to say, ask. People love talking about themselves."),
  'groups': [
   (('Para conocer a alguien', 'To get to know someone'), [["Where are you from?", '¿De dónde eres?'], ["What do you do?", '¿A qué te dedicas?'], ["How long have you lived here?", '¿Cuánto tiempo llevas viviendo aquí?'], ["Do you like it here?", '¿Te gusta vivir aquí?'], ["What do you do in your free time?", '¿Qué haces en tu tiempo libre?']]),
   (('Sobre gustos', 'About likes'), [["What kind of music do you like?", '¿Qué música te gusta?'], ["What's your favourite food?", '¿Cuál es tu comida favorita?'], ["Have you seen any good films lately?", '¿Has visto alguna película buena últimamente?'], ["Do you like travelling?", '¿Te gusta viajar?'], ["Coffee or tea?", '¿Café o té?']]),
   (('Sobre el pasado y los planes', 'About the past and plans'), [["What did you do at the weekend?", '¿Qué hiciste el fin de semana?'], ["How was your day?", '¿Qué tal tu día?'], ["Where did you go on holiday?", '¿Dónde fuiste de vacaciones?'], ["What are you doing tonight?", '¿Qué haces esta noche?'], ["Any plans for the summer?", '¿Algún plan para el verano?']]),
   (('Para profundizar', 'To go deeper'), [["Why do you think that?", '¿Por qué lo piensas?'], ["What was that like?", '¿Y cómo fue?'], ["How did you feel?", '¿Cómo te sentiste?'], ["What would you do?", '¿Tú qué harías?'], ["What's the best thing about it?", '¿Qué es lo mejor de eso?']]),
  ]},
 {'id': 'after', 'icon': 'calendar',
  'title': ('Después del Sprint: tu plan de 30 días', 'After the Sprint: your 30-day plan'),
  'desc': ('El Sprint rompe el miedo. Este plan de 15 minutos al día hace que no vuelva.', 'The Sprint breaks the fear. This 15-minutes-a-day plan stops it coming back.'),
  'tips': [
   (('Semana 1: repetir', 'Week 1: repeat'), ('Repite cada día una conversación de Modo Habla. La misma. Cuando salga sin pensar, cambia a otra.', "Repeat one Speech Mode conversation a day. The same one. When it comes out without thinking, switch to another."), []),
   (('Semana 2: tu voz', 'Week 2: your voice'), ('Haz shadowing de 5 minutos al día con tu propio guion. Grábate el domingo y compáralo con tu Día 7.', 'Shadow your own script for 5 minutes a day. Record yourself on Sunday and compare it with your Day 7.'), []),
   (('Semana 3: la calle', 'Week 3: the street'), ('Una frase real en inglés al día: en una tienda, en un comentario, en un audio a un amigo.', 'One real sentence in English a day: in a shop, in a comment, in a voice note to a friend.'), []),
   (('Semana 4: más largo', 'Week 4: longer'), ('Habla 3 minutos seguidos sobre un tema nuevo cada día. Usa las frases de rescate cuando te bloquees.', 'Talk for 3 minutes in a row on a new topic every day. Use the rescue phrases when you get stuck.'), []),
  ]},
 {'id': 'mistakes', 'icon': 'warn', 'link': 'mistakes',
  'title': ('Los 16 errores típicos de los hispanohablantes', 'The 16 typical mistakes of Spanish speakers'),
  'desc': ('«I have 25 years», «I am agree»… Con la frase correcta y el porqué de cada uno.', '"I have 25 years", "I am agree"… With the right sentence and why each one happens.')},
]


def build(lang):
    """The paid file for one language."""
    i = 0 if lang == 'es' else 1
    days = []
    for d in DAYS:
        n = d['n']
        if n == 0:
            days.append({'n': 0, 'title': d['title'][i], 'brief': d['brief'][i], 'why': d['why'][i], 'challenge': d['challenge'][i],
                         'steps': [{'text': st[i], 'id': st[2]} for st in d['steps']]})
            continue
        base = S.DAYS[n - 1]
        days.append({'n': n, 'title': base['title'], 'can': base['can'], 'goal': base['goal'],
                     'brief': d['brief'][i], 'why': d['why'][i], 'challenge': d['challenge'][i], 'mistakeWhy': d['mistake'][i],
                     'phrases': [[p[0], p[1]] for p in S.S[n - 1]], 'freeze': d['freeze'],
                     'mistake': {'bad': S.COURSE[n - 1]['bad'], 'good': S.COURSE[n - 1]['good']},
                     'go': {'game': base['game'], 'scene': base['scene'], 'clip': base['clip']}})
    lib = []
    for r in LIBRARY:
        x = {'id': r['id'], 'icon': r['icon'], 'title': r['title'][i], 'desc': r['desc'][i]}
        if 'groups' in r: x['groups'] = [{'h': g[0][i], 'items': g[1]} for g in r['groups']]
        if 'tips' in r: x['tips'] = [{'h': tp[0][i], 'p': tp[1][i], 'ex': tp[2]} for tp in r['tips']]
        if 'template' in r: x['template'] = r['template']
        if 'link' in r: x['link'] = r['link']
        lib.append(x)
    return {'days': days, 'library': lib, 'reflect': [q[i] for q in REFLECT]}
