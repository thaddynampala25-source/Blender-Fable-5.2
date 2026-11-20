"""Word timings for recorded takes, from a speech-to-text model that runs on this machine (nothing is uploaded).

    pip install faster-whisper
    python3 audio_words.py take.mp3                  -> take.mp3.words.json (used by audio_build.py split)
    python3 audio_words.py --check gb f batch.json   transcribe each clip of that voice and list mismatches

Used only while making clips; the site does not need it.
"""
import difflib, json, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

MODEL = 'small.en'


def pcm(path):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def words(model, path):
    segs, _ = model.transcribe(pcm(path), word_timestamps=True, language='en', condition_on_previous_text=False)
    return [{'w': w.word.strip(), 's': w.start, 'e': w.end} for s in segs for w in s.words]


def check(model, acc, g, batch):
    from audio_build import OUT, norm_words
    bad = []
    for it in json.load(open(batch))['items']:
        f = f'{OUT}/{acc}-{g}-{it["id"]}.mp3'
        heard = ' '.join(x['w'] for x in words(model, f))
        a, b = ' '.join(norm_words(it['text'])), ' '.join(norm_words(heard))
        r = difflib.SequenceMatcher(None, a, b).ratio()
        if r < 0.8: bad.append((round(r, 2), it['text'], heard))
    for x in bad: print('MISMATCH', *x, sep=' | ')
    print(f'{acc}-{g}: {len(bad)} of {len(json.load(open(batch))["items"])} clips do not match')
    return bad


if __name__ == '__main__':
    m = WhisperModel(MODEL, device='cpu', compute_type='int8')
    if sys.argv[1] == '--check': sys.exit(1 if check(m, *sys.argv[2:5]) else 0)
    for p in sys.argv[1:]:
        json.dump(words(m, p), open(p + '.words.json', 'w'))
        print(p + '.words.json')
