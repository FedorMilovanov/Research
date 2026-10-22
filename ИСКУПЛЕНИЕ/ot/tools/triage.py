# -*- coding: utf-8 -*-
"""Triage helper for qalite: same checks, but every failing fragment is printed
with its file:line, so that [A]/[B] lines can be classified one by one
(apparatus reading / lexicon citation / damaged mirror token / lemma form).

Usage:
    python3 tools/triage.py <file.md> [<file.md> ...]

[ A ] = the fragment is not attested in MT, the LXX mirrors or SBLGNT.
[ B ] = attested with a one-character difference (mirror typo or variant).
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qalite  # noqa: E402


def main(paths):
    mtc = lxxc = ntc = None
    for p in paths:
        text = io.open(p, encoding='utf-8').read()
        clean = text.replace('**', '')
        if qalite.frags(clean, qalite.HEB, qalite.heb_norm) and mtc is None:
            mtc = qalite.mt_corpus()
        if qalite.frags(clean, qalite.GRK, qalite.grk_norm) and lxxc is None:
            lxxc = qalite.lxx_corpus()
            ntc = qalite.nt_corpus()
        for i, line in enumerate(text.split('\n'), 1):
            lc = line.replace('**', '')
            for raw, n in qalite.frags(lc, qalite.HEB, qalite.heb_norm):
                if mtc and not qalite.has(mtc, n):
                    print('%s:%d HE %r' % (os.path.basename(p), i, raw[:90]))
            for raw, n in qalite.frags(lc, qalite.GRK, qalite.grk_norm):
                if not lxxc:
                    continue
                if qalite.has(lxxc, n) or qalite.has(ntc, n):
                    continue
                near = qalite.fuzzy(lxxc, n) or qalite.fuzzy(ntc, n)
                print('%s:%d %s GR %r%s' % (os.path.basename(p), i, 'B' if near else 'A', raw[:90],
                                            ('  ~ %r' % (near[:90],)) if near else ''))
        print('--- %s done' % os.path.basename(p))


if __name__ == '__main__':
    main(sys.argv[1:])
