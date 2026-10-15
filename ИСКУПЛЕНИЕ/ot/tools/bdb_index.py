# -*- coding: utf-8 -*-
"""Build a skeleton→entry-id index of BDB (HebrewLexicon) once, then look words up."""
import io
import json
import os
import re
import sys

sys.path.insert(0, '/tmp/arena-scratch/tools')

BDB = '/tmp/arena-scratch/src/HebrewLexicon/BrownDriverBriggs.xml'
CACHE = '/tmp/arena-scratch/tools/bdb_index.json'
POINTS = re.compile(r'[\u0591-\u05bd\u05bf-\u05c7]')


def skeleton(word):
    w = POINTS.sub('', word)
    return w.replace(' ', '').replace('\u05be', '')


def build():
    t = io.open(BDB, encoding='utf-8', errors='ignore').read()
    idx = {}
    for m in re.finditer(r'<entry id="([^"]+)"[^>]*>(.{0,600}?)<status', t, re.S):
        eid, head = m.group(1), m.group(2)
        w = re.search(r'<w[^>]*>([^<]+)</w>', head, re.S)
        if not w:
            continue
        key = skeleton(w.group(1))
        idx.setdefault(key, []).append(eid)
    json.dump(idx, io.open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
    return idx


def load():
    if not os.path.exists(CACHE):
        return build()
    return json.load(io.open(CACHE, encoding='utf-8'))


def find(word):
    idx = load()
    return idx.get(skeleton(word), [])


if __name__ == '__main__':
    idx = load()
    print('entries indexed:', len(idx))
    for w in sys.argv[1:]:
        print('%-14s -> %s' % (w, find(w)[:6]))
