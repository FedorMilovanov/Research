# -*- coding: utf-8 -*-
"""Lightweight quote verifier (rebuilt after the loss of qa.py).

For every file given:
  * extract Hebrew runs and Greek runs of >= 2 tokens
  * check that the run is attested, word-for-word (points/diacritics ignored),
    inside some verse of some source:
      - MT   : morphhb WLC, per-verse skeleton strings
      - LXX  : ELI 1930 per-verse word strings (all OT books), F1K Daniel (OG + Th),
               S23 lxx-swete (all OT books; codex A readings quoted in the cards)
      - NT   : SBLGNT per-verse strings

Output: [A] not attested (problem), [B] attested only with a mismatch of one
character run (informational, e.g. mirror typo), plus per-file counters.
"""
import glob
import io
import os
import re
import sys
import unicodedata

sys.path.insert(0, '/tmp/arena-scratch/tools')
import ot  # noqa: E402

HEB = re.compile(r'[\u0590-\u05FF][\u0590-\u05FF\s\u05BE\u05F3\u05F4]*')
GRK = re.compile(r'[\u0370-\u03FF\u1F00-\u1FFF][\u0370-\u03FF\u1F00-\u1FFF\s\u2019\u02BC]*')
POINTS = re.compile(r'[\u0591-\u05bd\u05bf-\u05c7]')


def heb_norm(s):
    s = POINTS.sub('', s).replace('\u05be', ' ').replace('/', '')
    return ' '.join(w for w in s.split() if w)


def grk_norm(s):
    s = s.replace('\u2019', ' ').replace('\u02bc', ' ')
    s = s.replace('\u1fbd', ' ').replace('\u1fbf', ' ').replace('\u1ffe', ' ')  # elision marks
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r'[^\u0370-\u03ff\u1f00-\u1fff\s]', ' ', s)
    return ' '.join(w.replace('ς', 'σ') for w in s.split() if w)


QERE = re.compile(r'<rdg type="x-qere">(.*?)</rdg>', re.S)
QERE_W = re.compile(r'<w[^>]*>([^<]*)</w>')


def mt_corpus():
    out = []
    for f in sorted(glob.glob('/tmp/arena-scratch/src/morphhb/wlc/*.xml')):
        b = os.path.basename(f)[:-4]
        if b == 'VerseMap':
            continue
        raw = io.open(f, encoding='utf-8').read()
        for (c, v) in ot._mt_verses(b):
            out.append(heb_norm(ot.mt_show(b, c, v)))
        # qere readings: the ketiv word stands in the text, the qere in <rdg>
        for verse in re.findall(r'<verse osisID="[^"]*">(.*?)</verse>', raw, re.S):
            words = []
            for block in re.findall(r'<note type="variant">(.*?)</note>', verse, re.S):
                rdg = QERE.search(block)
                if rdg:
                    words += QERE_W.findall(rdg.group(1))
            if words:
                out.append(heb_norm(' '.join(words)))
    return out


S23_DIR = '/tmp/arena-scratch/src/lxx-swete/data'


def s23_corpus():
    """S23 = lxx-swete (First1KGreek tlg0527), one token per line prefixed by ref."""
    out = []
    for f in sorted(glob.glob(S23_DIR + '/*.txt')):
        verse = None
        toks = []
        def flush():
            if toks:
                out.append(grk_norm(' '.join(toks)))
        for line in io.open(f, encoding='utf-8'):
            line = line.rstrip('\n')
            if not line.strip():
                continue
            head, _, tok = line.partition(' ')
            if head != verse:
                flush()
                verse, toks = head, []
            if tok.strip():
                toks.append(tok.strip())
        flush()
    return out


def lxx_corpus():
    out = []
    # F1K Daniel, both versions
    for book in ('DanOG', 'DanTh'):
        for (c, v) in sorted(ot._f1k_verses(book, 1)):
            t = ot.f1k(book, c, v)
            if t:
                out.append(grk_norm(t))
    # ELI 1930: whole OT word stream, verse by verse
    words, rows = ot._eli_index()
    for i, (idx, ref) in enumerate(rows):
        book, c, v = ref.rsplit('.', 1)[0], None, None
        parts = ref.split('.')
        if len(parts) == 3:
            book, c, v = parts
        end = rows[i + 1][0] if i + 1 < len(rows) else max(words) + 1
        txt = ' '.join(words.get(k, '') for k in range(idx, end) if k in words)
        out.append(grk_norm(txt))
    out += s23_corpus()
    return out


def nt_corpus():
    out = []
    for b in ot.NT_FILES:
        for (c, v) in ot._nt_verses(b):
            t = ot.nt(b, c, v)
            if t:
                out.append(grk_norm(t))
    return out


def frags(text, regex, norm, min_tokens=2):
    out = []
    for m in regex.finditer(text):
        raw = m.group(0)
        n = norm(raw)
        if len(n.split()) >= min_tokens:
            out.append((raw.strip(), n))
    return out


def has(corpus, frag):
    for verse in corpus:
        if frag in verse:
            return True
    return False


def fuzzy(corpus, frag, k=1):
    toks = frag.split()
    for verse in corpus:
        vt = verse.split()
        n = len(toks)
        for i in range(len(vt) - n + 1):
            win = ' '.join(vt[i:i + n])
            if len(win) == len(frag):
                diff = sum(1 for a, b in zip(win, frag) if a != b)
                if diff <= k:
                    return win
    return None


def main(paths):
    mtc = lxxc = ntc = None
    problems = 0
    info = 0
    for p in paths:
        text = io.open(p, encoding='utf-8').read().replace('**', '')
        hf = frags(text, HEB, heb_norm)
        gf = frags(text, GRK, grk_norm)
        if hf and mtc is None:
            mtc = mt_corpus()
        if gf:
            if lxxc is None:
                lxxc = lxx_corpus()
            if ntc is None:
                ntc = nt_corpus()
        for raw, n in hf:
            if has(mtc, n):
                continue
            near = fuzzy(mtc, n)
            problems += 1
            print('[A] %s HE: %r%s' % (os.path.basename(p), raw[:70],
                                       (' ~ %r' % near if near else '')))
        for raw, n in gf:
            if has(lxxc, n) or has(ntc, n):
                continue
            near = fuzzy(lxxc, n) or fuzzy(ntc, n)
            if near:
                info += 1
                print('[B] %s GR (variant 1 char): %r ~ %r' % (os.path.basename(p), raw[:60], near[:60]))
            else:
                problems += 1
                print('[A] %s GR: %r' % (os.path.basename(p), raw[:70]))
        print('== %s: HE %d, GR %d, problems %d, informational %d'
              % (os.path.basename(p), len(hf), len(gf), problems, info))
    print('TOTAL problems [A]: %d | informational [B]: %d' % (problems, info))


if __name__ == '__main__':
    main(sys.argv[1:])
