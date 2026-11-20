"""List every fixed English line the site speaks for the given Sprint days, with stable ids and character counts.

    python3 audio_lines.py            # days 1 and 2, summary
    python3 audio_lines.py 1 2 3 --json > lines.json

The text must match what the page passes to Voice.speak exactly: the clip layer looks clips up by text.
Run apply_sprint.py first so ../w2s-show/showcase.html holds the current scenes."""
import hashlib, json, re, sys
import sprint_content as C

DAY_SCENES = {0: ['meet'], 1: ['cafe']}          # Speech Mode scenes that belong to each day
DAY_CLIPS = {0: ['intro'], 1: ['coffee']}         # Imita clips that belong to each day
HOME = ["Hi, I'm Ana.", "I'm from Lima, in Peru.", "I'm thirty years old.", 'Nice to meet you.']   # home Word Order (apply_ux.py)


def scene_lines(name):
    src = open('../w2s-show/showcase.html', encoding='utf-8').read()
    i = src.index('  ' + name + ':{'); j = src.index('\n  ', i + 3)
    while src[j + 3:j + 4] == ' ' or src[j + 3:j + 4] == '{': j = src.index('\n  ', j + 3)   # step lines are indented deeper
    seg = src[i:j]
    out = []
    for m in re.finditer(r'(?:"t"|\bt):\s*("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', seg):
        out.append(json.loads(m.group(1)) if m.group(1)[0] == '"' else m.group(1)[1:-1].replace("\\'", "'"))
    for m in re.finditer(r'(?:"model"|\bmodel):\s*("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', seg):
        out.append(json.loads(m.group(1)) if m.group(1)[0] == '"' else m.group(1)[1:-1].replace("\\'", "'"))
    return out


def lines(days):
    seen, out = set(), []
    def add(text, where):
        text = text.strip()
        if text and text not in seen:
            seen.add(text); out.append({'id': hashlib.sha1(text.encode()).hexdigest()[:10], 'text': text, 'chars': len(text), 'where': where})
    if 0 in days:
        for t in HOME: add(t, 'home')
    for d in days:
        for x in C.S[d]: add(x[0], f'd{d+1}:sentence')
        for x in C.GAP[d]: add(x[0].replace('___', x[2]), f'd{d+1}:gap')
        for x in C.SOUND[d]: add(x[0], f'd{d+1}:sound'); add(f'{x[0]}. {x[1]}.', f'd{d+1}:sound-pair')
        for x in C.QUICK[d]: add(x[0], f'd{d+1}:quick'); add(x[2], f'd{d+1}:quick-model')
        for p in C.COURSE[d]['phr']: add(p[0], f'd{d+1}:course')
        add(C.COURSE[d]['good'], f'd{d+1}:course')
        for k in DAY_CLIPS.get(d, []): add(C.CLIPS[k][1], f'd{d+1}:clip')
        for k in DAY_SCENES.get(d, []):
            for t in scene_lines(k): add(t, f'd{d+1}:scene')
    return out


if __name__ == '__main__':
    days = [int(a) - 1 for a in sys.argv[1:] if a.isdigit()] or [0, 1]
    L = lines(days)
    if '--json' in sys.argv: print(json.dumps(L, ensure_ascii=False, indent=1))
    else:
        for x in L: print(f"{x['id']}  {x['chars']:4d}  {x['where']:16s} {x['text']}")
        print(f'{len(L)} lines, {sum(x["chars"] for x in L)} characters')
