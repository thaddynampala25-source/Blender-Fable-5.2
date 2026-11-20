"""Recorded voices for the fixed lines: plan a batch, split a generated take into clips, write the manifest.

1. plan    python3 audio_build.py plan f 1 2 > batch-f.json         lines of Sprint days 1-2 (audio_lines.py), with the
           batch prompt in batch.json["prompt"]: every line once, separated by "[long pause]" (ElevenLabs eleven_v4).
           Generate the prompt once per voice. Cost: one credit per character per take.
2. words   python3 audio_words.py take.mp3                           word timings from a local speech-to-text model
           (pip install faster-whisper; nothing leaves the machine) -> take.mp3.words.json
3. split   python3 audio_build.py split take.mp3 batch.json gb f take.mp3.words.json   cut the take where each line
           starts and ends into audio/clips/<accent>-<voice>-<id>.mp3 (mono, 64 kb/s).
4. check   python3 audio_words.py --check gb f batch.json             transcribe every clip and list the ones that
           do not match their line.
5. build   python3 audio_build.py build                          compose the Sound Lab pairs ("ship. sheep.") from the
           single words and write audio/manifest.json. sitebuild.py ships it as window.W2S_AUDIO.

Clip keys are accent|voice|text. voice is f or m (the Female/Male choice in the games, Imita and the course) or a
Buddy id (may, kairo) for Speech Mode, which falls back to the Buddy's gender when the Buddy has no own voice.
Lines with no clip keep the device voice. Voices are the owner's choice (ElevenLabs library), see VOICES."""
import hashlib, json, os, re, subprocess, sys
import audio_lines as A, sprint_content as C

OUT = 'audio/clips'
# accent -> voice slot -> (ElevenLabs voice name, voice_id). Owner's picks, 20 Nov 2026.
VOICES = {   # owner's picks, 21 Nov 2026. Kairo uses the male voice of the accent, May the female one.
    'us': {'f': ('Savvy - Warm, Grounded & Natural', 'ogwqBH5bbF03DSbNiRNN'), 'm': ('Young Jamal', '6OzrBCQf8cjERkYgzSg8')},
    'gb': {'f': ('Charlotte - Sweet, Warm and Modern', '6fZce9LFNG3iEITDfqZZ'), 'm': ('Marcus - Black British London accent', 'XPItcki6tTIlq8JhllXm')},
    'au': {'f': ('Sophia - Young Australian Female', 'LtPsVjX1k0Kl4StEMZPK'), 'm': ('Ben', 'sai9UY7iXkRDSsXHR0bZ')},
}
BUDDY = {'f': 'May', 'm': 'Kairo'}   # scenes say the Buddy's name where the script says "Sam" (nameMissions in apply_ux.py)


def cid(text): return hashlib.sha1(text.encode()).hexdigest()[:10]


def plan(days, g):
    """Lines for these Sprint days as voice g says them: "Sam" becomes that voice's Buddy, plus the Buddy's greeting."""
    import buddy_roster
    name = BUDDY[g]
    items, have = [], set()
    def add(text, where):
        text = re.sub(r'\bSam\b', name, text)
        if text not in have: have.add(text); items.append({'id': cid(text), 'text': text, 'chars': len(text), 'where': where})
    for x in A.lines(days):
        if not x['where'].endswith('sound-pair'): add(x['text'], x['where'])
    for d in days:
        for w, alt, _ in C.SOUND[d]: add(alt, f'd{d+1}:sound-alt')
    for b in buddy_roster.ROSTER:
        if b['name'] == name: add(b['greet'], 'greet')
    fix = lambda t: t if t[-1] in '.?!' else t + '.'
    return {'items': items, 'prompt': ' [long pause] '.join(fix(x['text']) for x in items)}


def probe(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout)


def norm_words(t):
    return [w for w in re.sub(r"[^a-z0-9' ]+", ' ', t.lower().replace('\u2019', "'")).split() if w]


def split(take, batch, acc, g, words_json):
    """Cut the take where the transcript (audio_words.py) says each line starts and ends."""
    import difflib
    assert g in VOICES[acc], (acc, g)
    items = json.load(open(batch))['items']
    heard = json.load(open(words_json))
    exp, owner = [], []
    for k, it in enumerate(items):
        for w in norm_words(it['text']): exp.append(w); owner.append(k)
    hw, hi = [], []
    for n, x in enumerate(heard):
        for w in norm_words(x['w']): hw.append(w); hi.append(n)
    fi, li = {}, {}                                  # line -> first and last heard word index
    for a, b, size in difflib.SequenceMatcher(None, exp, hw, autojunk=False).get_matching_blocks():
        for t in range(size):
            k = owner[a + t]; fi.setdefault(k, hi[b + t]); li[k] = hi[b + t]
    # a line the model misheard (single words like "air") gets the unmatched words between its neighbours
    gaps, merged = {}, []
    for k in range(len(items)):
        if k in fi: continue
        lo = max([li[j] for j in range(k) if j in li], default=-1) + 1
        up = min([fi[j] for j in range(k + 1, len(items)) if j in fi], default=len(heard))
        if lo < up: fi[k], li[k] = lo, up - 1; continue
        # the model dropped the word: it is in the gap between the neighbours' heard words
        a = heard[lo - 1]['e'] if lo > 0 else 0.0
        b = heard[up]['s'] if up < len(heard) else probe(take)
        if b - a >= 0.3: gaps[k] = (a + 0.05, b - 0.05); continue
        merged.append(k)   # heard as one word with the line before it ("estate esteem"): split that word's span below
    first = {k: heard[fi[k]]['s'] for k in fi}; last = {k: heard[li[k]]['e'] for k in li}
    for k, (a, b) in gaps.items(): first[k], last[k] = a, b
    for k in merged:
        p0 = max(j for j in range(k) if j in first)
        a, b = first[p0], last[p0]
        log = subprocess.run(['ffmpeg', '-hide_banner', '-ss', f'{a:.3f}', '-to', f'{b:.3f}', '-i', take, '-af', 'silencedetect=noise=-35dB:d=0.08', '-f', 'null', '-'], capture_output=True, text=True).stderr
        S = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]; E = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
        sil = [(x, y) for x, y in zip(S, E) if 0.1 < x and y < b - a - 0.1]
        if not sil: sys.exit(f'{take}: cannot split {items[p0]["text"]!r} / {items[k]["text"]!r}')
        x, y = max(sil, key=lambda z: z[1] - z[0])
        last[p0], first[k], last[k] = a + x, a + y, b
    dur = probe(take)
    for k in range(len(items) - 1):
        if not last[k] <= first[k + 1]: sys.exit(f'{take}: lines {k} and {k + 1} overlap ({items[k]["text"]!r})')
    cuts = [0.0] + [(last[k] + first[k + 1]) / 2 for k in range(len(items) - 1)] + [dur]
    os.makedirs(OUT, exist_ok=True)
    trim = 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.12'
    for k, it in enumerate(items):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{cuts[k]:.3f}', '-to', f'{cuts[k + 1]:.3f}', '-i', take, '-af', trim,
                        '-ac', '1', '-ar', '44100', '-b:a', '64k', f'{OUT}/{acc}-{g}-{it["id"]}.mp3'], check=True)
    print(f'{len(items)} clips from {take} as {acc}-{g}')


def build():
    clips = {}
    for acc, slots in VOICES.items():
        for g in slots:
            pre = f'{acc}-{g}'
            texts = {x['id']: x['text'] for x in plan(list(range(len(C.S))), g)['items']}
            for d, day in enumerate(C.SOUND):        # the pair Sound Lab plays after an answer: "word. other."
                for w, alt, _ in day:
                    a, b = f'{OUT}/{pre}-{cid(w)}.mp3', f'{OUT}/{pre}-{cid(alt)}.mp3'
                    pair = f'{w}. {alt}.'; out = f'{OUT}/{pre}-{cid(pair)}.mp3'
                    if os.path.exists(a) and os.path.exists(b) and not os.path.exists(out):
                        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', a, '-i', b, '-filter_complex',
                                        '[0:a]apad=pad_dur=0.35[x];[x][1:a]concat=n=2:v=0:a=1', '-ac', '1', '-b:a', '64k', out], check=True)
                    texts[cid(pair)] = pair
            for f in sorted(os.listdir(OUT)):
                m = re.fullmatch(re.escape(pre) + r'-([0-9a-f]{10})\.mp3', f)
                if m and m.group(1) in texts:
                    clips[f'{acc}|{g}|{texts[m.group(1)]}'] = {'f': f, 'd': round(probe(f'{OUT}/{f}') * 1000)}
    json.dump({'note': 'Made by audio_build.py. Keys: accent|voice|text, exactly as the page speaks it.', 'clips': clips},
              open('audio/manifest.json', 'w'), ensure_ascii=False, indent=0, sort_keys=True)
    print(len(clips), 'clips in audio/manifest.json')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'plan': print(json.dumps(plan([int(a) - 1 for a in sys.argv[3:]] or [0, 1], sys.argv[2]), ensure_ascii=False, indent=1))
    elif cmd == 'split': split(*sys.argv[2:7])
    elif cmd == 'build': build()
    else: sys.exit(__doc__)
