"""Two languages from one build. Spanish is the site's language (at /); English is the translation (at /en/).

The original pages are written in English source text. i18n_catalog.CAT maps each piece of interface and
marketing text to its Spanish version and, where the English was rewritten to follow the Spanish, to the new
English. Text that is not in the catalogue stays as it is: that is how the English the learners practise
(phrases, sentences, dialogue) stays English on both sides.

Replacement is exact, never fuzzy: whole HTML text nodes, whole attribute values, whole JavaScript string
literals, whole JSON-LD strings. Entries whose source contains markup are replaced as raw snippets first.
New pages (accounts, the Sprint, the tutor area, thank-you, terms) are written in both languages directly.
"""
import re, json
from i18n_catalog import CAT

LANGS = ('es', 'en')
SLUG = {
    'es': {'home': '/', 'speak': '/modo-habla/', 'games': '/juegos/', 'shadow': '/shadowing/', 'sprint': '/sprint-7-dias/', 'course': '/curso/',
           'tutor': '/tutora/', 'join': '/unete/', 'mistakes': '/errores-comunes/', 'about': '/como-ensenamos/', 'privacy': '/privacidad/',
           'terms': '/terminos/', 'account': '/cuenta/', 'thanks': '/gracias/'},
    'en': {'home': '/en/', 'speak': '/en/speech-mode/', 'games': '/en/games/', 'shadow': '/en/shadowing/', 'sprint': '/en/7-day-sprint/', 'course': '/en/course/',
           'tutor': '/en/tutor/', 'join': '/en/join/', 'mistakes': '/en/common-mistakes/', 'about': '/en/about/', 'privacy': '/en/privacy/',
           'terms': '/en/terms/', 'account': '/en/account/', 'thanks': '/en/thanks/'},
}
# the English paths the original source uses
SRC_PATHS = {'speak': '/speech-mode/', 'games': '/games/', 'shadow': '/shadowing/', 'sprint': '/7-day-sprint/', 'course': '/course/', 'tutor': '/tutor/',
             'join': '/join/', 'mistakes': '/common-mistakes/', 'about': '/about/', 'privacy': '/privacy/'}
_SRC_RE = re.compile(r'(?<=["\'(])(' + '|'.join(re.escape(p) for p in sorted(SRC_PATHS.values(), key=len, reverse=True)) + r')(?=[#?"\')]|$)')
_BY_SRC = {v: k for k, v in SRC_PATHS.items()}


def link(name, lang):
    return SLUG[lang][name]


def paths(text, lang):
    """Source paths (/speech-mode/ ...) to this language's paths; the home link too."""
    text = _SRC_RE.sub(lambda m: SLUG[lang][_BY_SRC[m.group(1)]], text)
    if lang != 'es':
        text = text.replace('href="/"', 'href="' + SLUG[lang]['home'] + '"')
    return text


def _norm(s):
    return ' '.join(s.split())


_RAW = {}     # entries with markup: raw snippet replacement
_TXT = {}     # plain entries: whole text node, attribute or literal
for row in CAT:
    src, es = row[0], row[1]
    en = row[2] if len(row) > 2 and row[2] else src
    (_RAW if '<' in src else _TXT)[src if '<' in src else _norm(src)] = {'es': es, 'en': en}
_RAW_KEYS = sorted(_RAW, key=len, reverse=True)
_USED = set()


def t(text, lang):
    """One whole string (a title, a JSON-LD value...)."""
    k = _norm(text)
    if k in _TXT:
        _USED.add(k)
        return _TXT[k][lang]
    return text


def _raw(text, lang):
    for k in _RAW_KEYS:
        if k in text:
            _USED.add(k)
            text = text.replace(k, _RAW[k][lang])
    return text


_ATTR = re.compile(r'(\s(?:title|aria-label|placeholder|alt|content|data-tip|data-label)=")([^"]*)(")')
_TOKEN = re.compile(r'(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<!--.*?-->|<[^>]+>|[^<]+)', re.S)


def _esc_attr(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


def _attr(m, lang):
    v = m.group(2)
    raw = v.replace('&quot;', '"').replace('&amp;', '&').replace('&#39;', "'")
    k = _norm(raw)
    if k in _TXT:
        _USED.add(k)
        return m.group(1) + _esc_attr(_TXT[k][lang]) + m.group(3)
    return m.group(0)


def html(doc, lang):
    doc = _raw(doc, lang)
    out = []
    for tok in _TOKEN.findall(doc):
        if tok.startswith('<script'):
            head_end = tok.index('>') + 1
            inner, tail = tok[head_end:-9], tok[-9:]
            if 'application/ld+json' in tok[:head_end]:
                out.append(tok[:head_end] + ld(inner, lang) + tail)
            else:
                out.append(tok[:head_end] + js(inner, lang) + tail)
        elif tok.startswith('<style') or tok.startswith('<!--'):
            out.append(tok)
        elif tok.startswith('<'):
            out.append(_ATTR.sub(lambda m: _attr(m, lang), tok))
        else:
            k = _norm(tok.replace('&amp;', '&').replace('&#39;', "'").replace('&quot;', '"'))
            if k in _TXT:
                _USED.add(k)
                lead = tok[:len(tok) - len(tok.lstrip())]
                trail = tok[len(tok.rstrip()):]
                out.append(lead + _TXT[k][lang].replace('&', '&amp;').replace('<', '&lt;') + trail)
            else:
                out.append(tok)
    return paths(''.join(out), lang)


_LIT = re.compile(r"'(?:[^'\\\n]|\\.)*'|\"(?:[^\"\\\n]|\\.)*\"|`(?:[^`\\]|\\.)*`", re.S)


def _js_lit(m, lang):
    s = m.group(0)
    q, inner = s[0], s[1:-1]
    k = _norm(inner.replace("\\'", "'").replace('\\"', '"'))
    if k in _TXT and k == _norm(inner.replace("\\'", "'").replace('\\"', '"')) and inner.strip():
        _USED.add(k)
        new = _TXT[k][lang]
        lead = inner[:len(inner) - len(inner.lstrip(' '))]
        trail = inner[len(inner.rstrip(' ')):]
        new = lead + new + trail
        if q == "'":
            new = new.replace('\\', '\\\\').replace("'", "\\'")
        elif q == '"':
            new = new.replace('\\', '\\\\').replace('"', '\\"')
        else:
            new = new.replace('`', '\\`')
        return q + new + q
    return s


def js(code, lang):
    code = _raw(code, lang)
    return paths(_LIT.sub(lambda m: _js_lit(m, lang), code), lang)


def ld(text, lang):
    """JSON-LD: translate every string value."""
    try:
        data = json.loads(text)
    except Exception:
        return text

    def walk(x):
        if isinstance(x, dict):
            return {k: walk(v) for k, v in x.items()}
        if isinstance(x, list):
            return [walk(v) for v in x]
        if isinstance(x, str):
            return t(x, lang)
        return x
    return json.dumps(walk(data), ensure_ascii=False)


def unused():
    return [k for k in list(_TXT) + _RAW_KEYS if k not in _USED]
