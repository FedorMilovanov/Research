# -*- coding: utf-8 -*-
"""Local source access library for the OT sub-corpus work (scratch tool, never committed).

Corpora (all fetched from the registry URLs, checks only):
  * MT            — openscriptures/morphhb (WLC, OSIS)                     [S13]
  * ELI 1930      — eliranwong/LXX-Swete-1930 (token CSV)                  [S11]
  * SOL 1909      — Sollupulo/Swete-1909-LXX (Gen–2 Kings only)            [S10]
  * F1K           — OpenGreekAndLatin/First1KGreek tlg0527 (LXX books)     [S23-source]
  * S23           — nathans/lxx-swete (token-per-line mirrors)             [S23]
  * SBLGNT        — morphgnt/sblgnt (NT Greek)                             [S16]
"""
import functools
import glob
import io
import os
import re
import unicodedata

SRC = '/tmp/arena-scratch/src'

# ------------------------------------------------------------------ MT (morphhb)

MT_DIR = os.path.join(SRC, 'morphhb', 'wlc')

# F1K / S23 LXX book numbering (tlg0527), ELI 1930 abbreviations
LXX = {
    'Gen':   ('tlg001', 1,  'Gen'),
    'Exod':  ('tlg002', 2,  'Exo'),
    'Lev':   ('tlg003', 3,  'Lev'),
    'Num':   ('tlg004', 4,  'Num'),
    'Deut':  ('tlg005', 5,  'Deu'),
    'Josh':  ('tlg006', 6,  'Jos'),
    'Judg':  ('tlg008', 8,  'Jdg'),
    'Ruth':  ('tlg010', 10, 'Rut'),
    '1Sam':  ('tlg011', 11, '1Sa'),
    '2Sam':  ('tlg012', 12, '2Sa'),
    '1Kgs':  ('tlg013', 13, '1Ki'),
    '2Kgs':  ('tlg014', 14, '2Ki'),
    '1Chr':  ('tlg015', 15, '1Ch'),
    '2Chr':  ('tlg016', 16, '2Ch'),
    'Ezra':  ('tlg018', 18, 'Ezr'),
    'Neh':   ('tlg018', 18, 'Neh'),
    'Esth':  ('tlg019', 19, 'Est'),
    'Job':   ('tlg032', 32, 'Job'),
    'Ps':    ('tlg027', 27, 'Psa'),
    'Prov':  ('tlg029', 29, 'Pro'),
    'Eccl':  ('tlg030', 30, 'Ecc'),
    'Song':  ('tlg031', 31, 'Sng'),
    'Isa':   ('tlg048', 48, 'Isa'),
    'Jer':   ('tlg049', 49, 'Jer'),
    'Lam':   ('tlg051', 51, 'Lam'),
    'Ezek':  ('tlg053', 53, 'Eze'),
    'DanOG': ('tlg056', 56, 'Dan'),
    'DanTh': ('tlg057', 57, 'Dan'),
    'Hos':   ('tlg036', 36, 'Hos'),
    'Joel':  ('tlg039', 39, 'Joe'),
    'Amos':  ('tlg037', 37, 'Amo'),
    'Obad':  ('tlg040', 40, 'Oba'),
    'Jonah': ('tlg041', 41, 'Jon'),
    'Mic':   ('tlg038', 38, 'Mic'),
    'Nah':   ('tlg042', 42, 'Nah'),
    'Hab':   ('tlg043', 43, 'Hab'),
    'Zeph':  ('tlg044', 44, 'Zep'),
    'Hag':   ('tlg045', 45, 'Hag'),
    'Zech':  ('tlg046', 46, 'Zec'),
    'Mal':   ('tlg047', 47, 'Mal'),
}

NT_FILES = {'Mt': '61-Mt', 'Mk': '62-Mk', 'Lk': '63-Lk', 'Jn': '64-Jn', 'Ac': '65-Ac',
            'Rom': '66-Ro', '1Cor': '67-1Co', '2Cor': '68-2Co', 'Gal': '69-Ga', 'Eph': '70-Eph',
            'Phil': '71-Php', 'Col': '72-Col', '1Thess': '73-1Th', '2Thess': '74-2Th',
            '1Tim': '75-1Ti', '2Tim': '76-2Ti', 'Tit': '77-Tit', 'Phlm': '78-Phm', 'Heb': '79-Heb',
            'Jas': '80-Jas', '1Pet': '81-1Pe', '2Pet': '82-2Pe', '1Jn': '83-1Jn', '2Jn': '84-2Jn',
            '3Jn': '85-3Jn', 'Jude': '86-Jud', 'Rev': '87-Re'}

HEB = re.compile(r'[\u0590-\u05FF]')
GRK = re.compile(r'[\u0370-\u03FF\u1F00-\u1FFF]')
TEAMIM = re.compile(r'[\u0591-\u05AF\u05BD\u05BF\u05C0\u05C3]')


def he_norm(s, vowels=False):
    s = TEAMIM.sub('', s)
    if not vowels:
        s = re.sub(r'[\u05B0-\u05BC\u05C1\u05C2\u05C4\u05C5\u05C7]', '', s)
    s = s.replace('\u05BE', ' ')          # maqaf
    s = re.sub(r'[\u0590-\u05CF]', '', s)  # leftover points
    return re.sub(r'\s+', ' ', s).strip()


def gr_norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.replace('ς', 'σ').lower()
    return re.sub(r'[^α-ω\u1f00-\u1fff\u0370-\u03ff]', ' ', s).split()


# ------------------------------------------------------------------ MT


@functools.lru_cache(maxsize=None)
def _mt_raw(book):
    return io.open(os.path.join(MT_DIR, book + '.xml'), encoding='utf-8').read()


@functools.lru_cache(maxsize=None)
def _mt_verses(book):
    t = _mt_raw(book)
    out = {}
    for m in re.finditer(r'<verse osisID="%s\.(\d+)\.(\d+)"[^>]*>(.*?)</verse>' % re.escape(book), t, re.S):
        out[(int(m.group(1)), int(m.group(2)))] = m.group(3)
    return out


TOKEN_SPLIT = re.compile(r'(<w\b[^>]*>.*?</w>|<note\b[^>]*>.*?</note>|<seg\b[^>]*>.*?</seg>|<[^>]+>)', re.S)


def _mt_words(book, ch, vs, view='wlc'):
    """Yield (word, lemma) pairs for a verse.

    view='wlc'  — WLC as printed (ketiv in the text, qere dropped)
    view='qere' — qere words substituted for the ketiv
    """
    seg = _mt_verses(book)[(ch, vs)]
    out = []
    i = 0
    while i < len(seg):
        m = re.compile(r'<w\b[^>]*>.*?</w>|<note\b[^>]*>.*?</note>', re.S).search(seg, i)
        if not m:
            break
        piece = m.group(0)
        if piece.startswith('<note'):
            i = m.end()
            continue
        attrs = piece[:piece.index('>')]
        word = re.sub(r'<[^>]+>', '', piece).replace('/', '')
        lemma = (re.search(r'lemma="([^"]+)"', attrs) or [None, ''])[1]
        ketiv = 'x-ketiv' in attrs
        # look ahead for the qere note that belongs to this ketiv word
        nxt = re.compile(r'<note\b[^>]*>.*?</note>', re.S).match(seg, m.end())
        qere_words = []
        if ketiv and nxt:
            for w in re.finditer(r'<w\b[^>]*>.*?</w>', nxt.group(0), re.S):
                qattrs = w.group(0)[:w.group(0).index('>')]
                qword = re.sub(r'<[^>]+>', '', w.group(0)).replace('/', '')
                qlemma = (re.search(r'lemma="([^"]+)"', qattrs) or [None, ''])[1]
                qere_words.append((qword, qlemma))
        if ketiv and view == 'qere' and qere_words:
            out.extend(qere_words)
        else:
            out.append((word, lemma))
        i = nxt.end() if (ketiv and nxt) else m.end()
    return out


def _join(words):
    """Join MT words, honouring maqqef (a word ending in ־ keeps the next word attached)."""
    out = ''
    for w, _ in words:
        if not out:
            out = w
        elif out.endswith('\u05BE'):
            out += w
        else:
            out += ' ' + w
    return out


def mt_words(book, ch, vs, view='wlc'):
    return _mt_words(book, ch, vs, view)


def mt_show(book, ch, vs, view='wlc'):
    return _join(_mt_words(book, ch, vs, view))


def mt_lemmas(book, ch, vs):
    """All Strong numbers of the verse: ketiv and qere readings both included."""
    out = []
    for view in ('wlc', 'qere'):
        for _, lemma in _mt_words(book, ch, vs, view):
            for part in re.split(r'[/ ]', lemma):
                if part.isdigit():
                    out.append(int(part))
                elif re.match(r'^\d+$', part):
                    out.append(int(part))
    return sorted(set(out))


def mt_verse_text(book, ch, vs, view='wlc'):
    return mt_show(book, ch, vs, view)


def mt_book_text(book, view='wlc'):
    """Continuous text of the whole book, verses in order."""
    parts = []
    for (c, v) in sorted(_mt_verses(book)):
        parts.append(mt_show(book, c, v, view))
    return ' '.join(parts)


def mt_has_verse(book, ch, vs):
    return (ch, vs) in _mt_verses(book)


def mt_lemma_index(book):
    """{strong: [(ch, vs), ...]} for one book."""
    idx = {}
    for (c, v) in _mt_verses(book):
        for s in mt_lemmas(book, c, v):
            idx.setdefault(s, []).append((c, v))
    return idx


def mt_search(book, strong):
    return mt_lemma_index(book).get(strong, [])


# ------------------------------------------------------------------ ELI 1930

ELI_DIR = os.path.join(SRC, 'LXX-Swete-1930')


@functools.lru_cache(maxsize=None)
def _eli_index():
    v = io.open(os.path.join(ELI_DIR, '00-Swete_versification.csv'), encoding='utf-8-sig').read().split('\n')
    w = io.open(os.path.join(ELI_DIR, '01-Swete_word_with_punctuations.csv'), encoding='utf-8-sig').read().split('\n')
    words = {}
    for ln in w:
        if ln.strip():
            a, b = ln.split('\t', 1)
            words[int(a)] = b
    rows = []
    for ln in v:
        if ln.strip():
            a, b = ln.split('\t', 1)
            rows.append((int(a), b))
    return words, rows


def eli(book, ch, vs, abbrev=None):
    """ELI 1930 verse text (Swete's text, token CSV); '' if the verse is absent."""
    ab = abbrev or LXX.get(book, (None, None, book))[2]
    ref = '%s.%d:%d' % (ab, ch, vs)
    words, rows = _eli_index()
    start = None
    for i, (idx, r) in enumerate(rows):
        if r == ref:
            start = (i, idx)
            break
    if start is None:
        return ''
    i, idx = start
    end = rows[i + 1][0] if i + 1 < len(rows) else max(words) + 1
    return ' '.join(words.get(k, '') for k in range(idx, end) if k in words).strip()


def eli_verse_tokens(book, ch, vs):
    t = eli(book, ch, vs)
    return [x for x in re.split(r'\s+', t) if x] if t else []


# ------------------------------------------------------------------ SOL 1909

SOL_DIR = os.path.join(SRC, 'Swete-1909-LXX')


SOL_FILES = {'Gen': '1.Genesis', 'Exod': '2.Exodus', 'Lev': '3.Leviticus', 'Num': '4.Numbers',
             'Deut': '5.Deuteronomy', 'Josh': '6.Joshua', 'Judg': '7.Judges', 'Ruth': '8.Ruth',
             '1Sam': '9.1Kingdoms', '2Sam': '10.2Kingdoms', '1Kgs': '11.3Kingdoms'}


@functools.lru_cache(maxsize=None)
def _sol_text(book):
    fn = SOL_FILES.get(book)
    if not fn:
        return ''
    return io.open(os.path.join(SOL_DIR, fn + '_Swete1909.txt'), encoding='utf-8').read()


@functools.lru_cache(maxsize=None)
def _sol_verses(book):
    t = _sol_text(book)
    out = {}
    if not t:
        return out
    cur = None
    buf = []
    for ln in t.split('\n'):
        m = re.match(r'^\s*(\d+):(\d+)\s+(.*)$', ln)
        if m:
            if cur:
                out[cur] = ' '.join(buf)
            cur = (int(m.group(1)), int(m.group(2)))
            buf = [m.group(3).strip()]
        elif cur is not None and ln.strip():
            buf.append(ln.strip())
    if cur:
        out[cur] = ' '.join(buf)
    return out


def sol(book, ch, vs):
    """Swete 1909 (Sollupulo) verse text; the transcription covers Gen–2 Kings only."""
    return _sol_verses(book).get((ch, vs), '')


# ------------------------------------------------------------------ F1K (tlg0527)

F1K_DIR = os.path.join(SRC, 'First1KGreek', 'data', 'tlg0527')


@functools.lru_cache(maxsize=None)
def _f1k_verses(book, ed):
    """F1K tlg0527 verse text: XML parsed, notes/apparatus dropped, nested notes included."""
    import xml.etree.ElementTree as ET

    tlg = LXX[book][0]
    files = sorted(glob.glob(os.path.join(F1K_DIR, tlg, 'tlg0527.%s.1st1K-grc%d.xml' % (tlg, ed))))
    if not files:
        return {}
    root = ET.parse(files[0]).getroot()

    def local(tag):
        return tag.rsplit('}', 1)[-1]

    SKIP = {'note', 'app', 'rdg', 'pb'}

    def collect(el):
        parts = []
        if local(el.tag) in SKIP:
            return ''
        if el.text:
            parts.append(el.text)
        for child in el:
            parts.append(collect(child))
            if child.tail:
                parts.append(child.tail)
        return ' '.join(parts)

    out = {}
    for div in root.iter():
        if local(div.tag) != 'div':
            continue
        if div.get('subtype') != 'chapter':
            continue
        ch = int(div.get('n'))
        for vdiv in div.iter():
            if local(vdiv.tag) != 'div' or vdiv.get('subtype') != 'verse':
                continue
            n = vdiv.get('n') or ''
            m2 = re.match(r'^(\d+)', n)
            if not m2:
                continue
            vs = int(m2.group(1))
            text = re.sub(r'\s+', ' ', collect(vdiv)).strip()
            if text:
                out[(ch, vs)] = text
    return out


def f1k(book, ch, vs, ed=1):
    return _f1k_verses(book, ed).get((ch, vs), '')


def f1k_count(book, ed=1):
    return len(_f1k_verses(book, ed))


# ------------------------------------------------------------------ S23 (lxx-swete)

S23_DIR = os.path.join(SRC, 'lxx-swete', 'data')


@functools.lru_cache(maxsize=None)
def _s23_verses(book):
    num = LXX[book][1]
    files = glob.glob(os.path.join(S23_DIR, '%02d.*.txt' % num))
    if not files:
        return {}
    out = {}
    for ln in io.open(files[0], encoding='utf-8'):
        m = re.match(r'^\d+\.(\d+)\.(\d+)\s+(\S+)', ln)
        if not m:
            continue
        key = (int(m.group(1)), int(m.group(2)))
        out.setdefault(key, []).append(m.group(3))
    return {k: ' '.join(v) for k, v in out.items()}


def s23(book, ch, vs):
    return _s23_verses(book).get((ch, vs), '')


def s23_count(book):
    return len(_s23_verses(book))


# ------------------------------------------------------------------ NT (SBLGNT)

NT_DIR = os.path.join(SRC, 'sblgnt')


@functools.lru_cache(maxsize=None)
def _nt_verses(book):
    fn = os.path.join(NT_DIR, NT_FILES[book] + '-morphgnt.txt')
    out = {}
    for ln in io.open(fn, encoding='utf-8'):
        parts = ln.split()
        if len(parts) < 7:
            continue
        ch, vs = int(parts[0][2:4]), int(parts[0][4:6])
        text = parts[3]
        out.setdefault((ch, vs), []).append((text, parts[6]))
    return out


def nt(book, ch, vs):
    return ' '.join(t for t, _ in _nt_verses(book).get((ch, vs), []))


def nt_lemmas(book, ch, vs):
    return [l for _, l in _nt_verses(book).get((ch, vs), [])]


def nt_lemma_search(lemma, forms=None):
    """All NT occurrences of a lemma (and optionally of listed surface forms)."""
    found = []
    for b in NT_FILES:
        for (c, v), toks in _nt_verses(b).items():
            for t, l in toks:
                if l == lemma or (forms and (t in forms or l in forms)):
                    found.append((b, c, v))
                    break
    return found
