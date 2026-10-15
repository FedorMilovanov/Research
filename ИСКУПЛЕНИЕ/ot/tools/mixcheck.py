# -*- coding: utf-8 -*-
"""Mixed-script check for the OT cards, the authority doc and the SSOT.

[A] defekt: one *segment* (token part after a dash or a slash) mixes Cyrillic
    letters with Greek, Hebrew or Latin letters — a wrong-script character
    inside a word (a Cyrillic т inside τῷ, a Latin a inside аппарат).
[B] review: compounds mixing scripts across parts that the whitelist of
    accepted Latin/English fragments (S23, LXX, MT, OCR, PDF, …) does not explain.

Usage: python3 mixcheck.py <files...>
"""
import io
import re
import sys

CYR = re.compile(r'[А-Яа-яЁё]')
GRK = re.compile(r'[\u0370-\u03ff\u1f00-\u1fff]')
HEB = re.compile(r'[\u0590-\u05ff]')
LAT = re.compile(r'[A-Za-z]')

TOKEN = re.compile(r'[^\s«»„“”"\'()\[\]{}<>,;:!?—–…\\]+', re.UNICODE)
SEG = re.compile(r'[-‑/|]+')

LATIN_OK = re.compile(r'^(S\d+[a-z]?|O\d+[a-z]?|A\d+[a-z]?|B\d+[a-z]?|T\d+[a-z]?|G\d+[a-z]?|H\d+[a-z]?|'
                      r'F1K|ELI|SOL|SBLGNT|MT|LXX|НЗ|ВЗ|NT|OG|Th|BHS|WLC|HALOT|LSJ|BDB|OCR|PDF|PT|kpr|'
                      r'ID|URL|DOI|CSS|HTML|JSON|XML|beta|code|Tel|Aviv|theancientbible|org|articles?)$')

a_count = 0
b_count = 0
for path in sys.argv[1:]:
    text = io.open(path, encoding='utf-8').read()
    name = path.split('/')[-1]
    for ln, line in enumerate(text.split('\n'), 1):
        for m in TOKEN.finditer(line):
            tok = m.group(0)
            segs = [x for x in SEG.split(tok) if x]
            bad = None
            for x in segs:
                if CYR.search(x) and (GRK.search(x) or HEB.search(x) or LAT.search(x)):
                    bad = x
                    break
            if bad:
                print('  [A] %s:%d: %s' % (name, ln, tok[:60]))
                a_count += 1
                continue
            if len(segs) > 1:
                scripts = [rx for rx in (CYR, GRK, HEB, LAT) if any(rx.search(x) for x in segs)]
                if CYR in scripts and LAT in scripts:
                    runs = re.findall(r'[A-Za-z][A-Za-z0-9_]*', tok)
                    if not all(LATIN_OK.match(r) for r in runs):
                        print('  [B] %s:%d: %s' % (name, ln, tok[:60]))
                        b_count += 1
print('mixed-script defects [A]: %d | tokens to review [B]: %d' % (a_count, b_count))
