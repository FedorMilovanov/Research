# -*- coding: utf-8 -*-
"""Lexicon access (BDB from openscriptures/HebrewLexicon, LSJ from cltk/greek_lexica_perseus).

Memory-safe: LSJ files are 60–70 MB each, so they are scanned with plain str.find
(never with nested-quantifier regexes) and the full text is kept only once per file.
"""
import functools
import glob
import io
import re

BDB = '/tmp/arena-scratch/src/HebrewLexicon/BrownDriverBriggs.xml'
LSJ_FILES = sorted(glob.glob('/tmp/arena-scratch/src/greek_lexica_perseus/greek_english_lexicon_lsj_*.xml'))
STRONG = '/tmp/arena-scratch/src/HebrewLexicon/HebrewStrong.xml'


@functools.lru_cache(maxsize=None)
def bdb(entry_id):
    """BDB entry text by id, e.g. bdb('k.ct.ac')."""
    t = io.open(BDB, encoding='utf-8', errors='ignore').read()
    m = re.search(r'<entry id="%s".*?</entry>' % re.escape(entry_id), t, re.S)
    if not m:
        return None
    body = m.group(0)
    body = re.sub(r'<status[^>]*>.*?</status>', '', body, flags=re.S)
    body = re.sub(r'<ref[^>]*>([^<]*)</ref>', r'[\1]', body)
    body = re.sub(r'<[^>]+>', ' ', body)
    return re.sub(r'\s+', ' ', body).strip()


@functools.lru_cache(maxsize=None)
def bdb_find(word):
    """Entry ids whose first 400 chars contain the word."""
    t = io.open(BDB, encoding='utf-8', errors='ignore').read()
    ids = []
    for m in re.finditer(r'<entry id="([^"]+)"[^>]*>(.{0,400}?)<status', t, re.S):
        if re.search(r'<w[^>]*>\s*%s\s*</w>' % re.escape(word), m.group(2)):
            ids.append(m.group(1))
    return ids


@functools.lru_cache(maxsize=None)
def strong_heb(num):
    t = io.open(STRONG, encoding='utf-8', errors='ignore').read()
    m = re.search(r'<entry id="H%d">(.*?)</entry>' % int(num), t, re.S)
    if not m:
        return None
    body = re.sub(r'<w[^>]*>([^<]*)</w>', r'\1 ', m.group(1))
    body = re.sub(r'<[^>]+>', ' ', body)
    return re.sub(r'\s+', ' ', body).strip()[:800]


@functools.lru_cache(maxsize=4)
def _lsj_text(fn):
    return io.open(fn, encoding='utf-8', errors='ignore').read()


def _entries_with_orth(fn, word, limit=20):
    """Yield (start, end) of entries containing an orth form equal to `word`."""
    t = _lsj_text(fn)
    needle = '>%s<' % word
    i = 0
    seen = set()
    while len(seen) < limit:
        j = t.find(needle, i)
        if j < 0:
            break
        i = j + len(needle)
        # only accept when the match sits inside an <orth> tag
        k = t.rfind('<orth', max(0, j - 60), j + 1)
        if k < 0:
            continue
        start = t.rfind('<entry', 0, j)
        if start < 0:
            continue
        if start in seen:
            continue
        end = t.find('</entry>', j)
        if end < 0:
            continue
        seen.add(start)
        yield start, end + len('</entry>')


def lsj(word, limit=3, chars=1200):
    """LSJ article text for a headword."""
    out = []
    for fn in LSJ_FILES:
        for start, end in _entries_with_orth(fn, word, limit):
            body = _lsj_text(fn)[start:end]
            body = re.sub(r'<quote[^>]*>', ' [', body)
            body = re.sub(r'</quote>', '] ', body)
            body = re.sub(r'<[^>]+>', ' ', body)
            body = re.sub(r'\s+', ' ', body).strip()
            if body:
                out.append((fn.split('/')[-1], body[:chars]))
    return out


def lsj_has(word):
    return [(fn.split('/')[-1], sum(1 for _ in _entries_with_orth(fn, word, 50)))
            for fn in LSJ_FILES if any(True for _ in _entries_with_orth(fn, word, 50))]


LEXIDX = '/tmp/arena-scratch/src/HebrewLexicon/LexicalIndex.xml'


@functools.lru_cache(maxsize=None)
def _lexidx():
    t = io.open(LEXIDX, encoding='utf-8', errors='ignore').read()
    out = {}
    for m in re.finditer(r'<entry id="[^"]+">(.*?)</entry>', t, re.S):
        chunk = m.group(1)
        x = re.search(r'<xref bdb="([^"]+)" strong="(\d+)"', chunk)
        if x:
            out[int(x.group(2))] = x.group(1)
    return out


def bdb_id(num):
    return _lexidx().get(int(num))


def bdb_by_strong(num, chars=900):
    eid = bdb_id(num)
    if not eid:
        return None
    t = bdb(eid)
    return (eid, t[:chars] if t else None)
