# -*- coding: utf-8 -*-
"""LSJ lookups against the cltk/greek_lexica_perseus dump (beta-code encoded).

Entries look like  <entryFree id="n19703" key="bde/lugma" ...>
  <orth extent="full" lang="greek">bde/lug-ma</orth>, ...
so the reliable anchor is the key attribute / the orth stem.
"""
import functools
import glob
import io
import re
import sys

sys.path.insert(0, '/tmp/arena-scratch/tools')
from beta import from_unicode, to_unicode  # noqa: E402

FILES = sorted(glob.glob('/tmp/arena-scratch/src/greek_lexica_perseus/greek_english_lexicon_lsj_*.xml'))
DIAC = re.compile(r'[)(/\\=|^]')
BETA_RUN = re.compile(r"[*]?[abgdezhqiklmncoprstufxywABGDEZHQIKLMNCOPRSTUFXYW][)=/(\\|^+*.-]*")


@functools.lru_cache(maxsize=4)
def _text(fn):
    return io.open(fn, encoding='utf-8', errors='ignore').read()


def _clean(body):
    body = re.sub(r'<quote[^>]*>', ' [', body)
    body = re.sub(r'</quote>', '] ', body)
    body = re.sub(r'<foreign[^>]*>', ' «', body)
    body = re.sub(r'</foreign>', '» ', body)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = re.sub(r'\s+', ' ', body)

    def conv(m):
        run = m.group(0)
        if not DIAC.search(run):
            return run
        return to_unicode(run)

    return BETA_RUN.sub(conv, body).strip()


def _loose(beta):
    """Regex that tolerates the diacritics and hyphens LSJ inserts inside a headword."""
    return ''.join(re.escape(c) + '[-^/+\\|=)(]*' for c in beta)


def find(word, limit=3, chars=1600):
    """LSJ entries whose key or orth starts with the word (diacritics ignored)."""
    beta = from_unicode(word)
    pat_key = re.compile(r'key="(%s)' % _loose(beta))
    pat_orth = re.compile(r'<orth[^>]*>(%s)' % _loose(beta))
    hits = []
    for fn in FILES:
        t = _text(fn)
        seen = []
        for pat in (pat_key, pat_orth):
            for m in pat.finditer(t):
                j = m.start()
                start = t.rfind('<entryFree', 0, j)
                if start < 0:
                    start = t.rfind('<entry', 0, j)
                end = t.find('</entryFree', j)
                if end < 0:
                    end = t.find('</entry', j)
                if start < 0 or end < 0 or start in seen:
                    continue
                seen.append(start)
                hits.append(_clean(t[start:end]))
                if len(hits) >= limit:
                    break
            if len(hits) >= limit:
                break
        if hits:
            break
    return [h[:chars] for h in hits]


def show(word):
    print('=' * 24, word)
    for h in find(word):
        print(h)
        print('-' * 12)


if __name__ == '__main__':
    for w in sys.argv[1:]:
        show(w)
