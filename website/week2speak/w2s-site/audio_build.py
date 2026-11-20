"""Recorded voices for the fixed lines: plan a batch, split a generated take into clips, write the manifest.

1. plan    python3 audio_build.py plan 1 2 > batch.json          lines of Sprint days 1-2 (audio_lines.py), with the
           batch prompt in batch.json["prompt"]: every line once, separated by "[long pause]" (ElevenLabs eleven_v4).
           Generate the prompt once per voice. Cost: one credit per character per take.
2. split   python3 audio_build.py split take.mp3 batch.json f [0.8]  cut the take at its long pauses into
           audio/clips/<f|m>-<id>.mp3 (mono, 64 kb/s). Stops if the pause count does not match the line count.
3. build   python3 audio_build.py build                          compose the Sound Lab pairs ("ship. sheep.") from the
           single words and write audio/manifest.json. sitebuild.py ships it as window.W2S_AUDIO.

Clip keys are accent|gender|text: these recordings are US English; Ruby and May use the female voice, Max and
Kairo the male one. Lines with no clip, or other accents, keep the device voice.
Voices used (ElevenLabs premade): f = Matilda (XrExE9yKIg1WjnnlVkGX), m = Chris (iP95p4xoKVk53GoZ742B)."""
import hashlib, json, os, re, subprocess, sys
import audio_lines as A, sprint_content as C

OUT = 'audio/clips'
ACCENT = 'us'


def cid(text): return hashlib.sha1(text.encode()).hexdigest()[:10]


def plan(days):
    items = [x for x in A.lines(days) if not x['where'].endswith('sound-pair')]
    have = {x['text'] for x in items}
    for d in days:
        for w, alt, _ in C.SOUND[d]:
            if alt not in have: have.add(alt); items.append({'id': cid(alt), 'text': alt, 'chars': len(alt), 'where': f'd{d+1}:sound-alt'})
    fix = lambda t: t if t[-1] in '.?!' else t + '.'
    return {'items': items, 'prompt': ' [long pause] '.join(fix(x['text']) for x in items)}


def probe(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout)


def split(take, batch, g, d=0.8):
    items = json.load(open(batch))['items']
    log = subprocess.run(['ffmpeg', '-hide_banner', '-i', take, '-af', f'silencedetect=noise=-40dB:d={d}', '-f', 'null', '-'], capture_output=True, text=True).stderr
    dur = probe(take)
    S = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]; E = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
    gaps = [(s, e) for s, e in zip(S, E) if s > 0.05 and e < dur - 0.05]
    if len(gaps) != len(items) - 1:
        sys.exit(f'{take}: {len(gaps)} pauses for {len(items)} lines; try another take or another -d')
    bounds = [0.0] + [x for gp in gaps for x in gp] + [dur]
    os.makedirs(OUT, exist_ok=True)
    trim = 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.12'
    for k, it in enumerate(items):
        a, b = max(0, bounds[2 * k] - (0.08 if k else 0)), min(dur, bounds[2 * k + 1] + 0.15)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{a:.3f}', '-to', f'{b:.3f}', '-i', take, '-af', trim,
                        '-ac', '1', '-ar', '44100', '-b:a', '64k', f'{OUT}/{g}-{it["id"]}.mp3'], check=True)
    print(f'{len(items)} clips from {take}')


def build():
    texts = {}
    for d, day in enumerate(C.SOUND):
        for w, alt, _ in day: texts[cid(w)] = w; texts[cid(alt)] = alt
    for x in A.lines(list(range(len(C.S)))): texts[x['id']] = x['text']
    clips = {}
    for g in ('f', 'm'):
        for d, day in enumerate(C.SOUND):        # the pair Sound Lab plays after an answer: "word. other."
            for w, alt, _ in day:
                a, b = f'{OUT}/{g}-{cid(w)}.mp3', f'{OUT}/{g}-{cid(alt)}.mp3'
                pair = f'{w}. {alt}.'; out = f'{OUT}/{g}-{cid(pair)}.mp3'
                if os.path.exists(a) and os.path.exists(b) and not os.path.exists(out):
                    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', a, '-i', b, '-filter_complex',
                                    '[0:a]apad=pad_dur=0.35[x];[x][1:a]concat=n=2:v=0:a=1', '-ac', '1', '-b:a', '64k', out], check=True)
                texts[cid(pair)] = pair
        for f in sorted(os.listdir(OUT)):
            m = re.fullmatch(g + r'-([0-9a-f]{10})\.mp3', f)
            if m and m.group(1) in texts:
                clips[f'{ACCENT}|{g}|{texts[m.group(1)]}'] = {'f': f, 'd': round(probe(f'{OUT}/{f}') * 1000)}
    json.dump({'note': 'Made by audio_build.py. Keys: accent|gender|text, exactly as the page speaks it.', 'clips': clips},
              open('audio/manifest.json', 'w'), ensure_ascii=False, indent=0, sort_keys=True)
    print(len(clips), 'clips in audio/manifest.json')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'plan': print(json.dumps(plan([int(a) - 1 for a in sys.argv[2:]] or [0, 1]), ensure_ascii=False, indent=1))
    elif cmd == 'split': split(sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]) if len(sys.argv) > 5 else 0.8)
    elif cmd == 'build': build()
    else: sys.exit(__doc__)
