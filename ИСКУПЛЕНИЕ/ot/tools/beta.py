# -*- coding: utf-8 -*-
"""Minimal TLG beta-code converter (enough for the Perseus LSJ dump)."""
import re
import unicodedata

LETTERS = {'a': 'α', 'b': 'β', 'g': 'γ', 'd': 'δ', 'e': 'ε', 'z': 'ζ', 'h': 'η', 'q': 'θ',
           'i': 'ι', 'k': 'κ', 'l': 'λ', 'm': 'μ', 'n': 'ν', 'c': 'ξ', 'o': 'ο', 'p': 'π',
           'r': 'ρ', 's': 'σ', 't': 'τ', 'u': 'υ', 'f': 'φ', 'x': 'χ', 'y': 'ψ', 'w': 'ω'}
ROUGH = {'α': 'ἁ', 'ε': 'ἑ', 'η': 'ἡ', 'ι': 'ἱ', 'ο': 'ὁ', 'υ': 'ὑ', 'ω': 'ὡ',
         'ρ': 'ῥ'}
SMOOTH = {'α': 'ἀ', 'ε': 'ἐ', 'η': 'ἠ', 'ι': 'ἰ', 'ο': 'ὀ', 'υ': 'ὐ', 'ω': 'ὠ'}
ACCENT = {'/': '\u0301', '\\': '\u0300', '=': '\u0342', '^': '\u0342'}


def to_unicode(beta):
    out = []
    i = 0
    cap = False
    while i < len(beta):
        ch = beta[i]
        if ch == '*':
            cap = True
            i += 1
            continue
        low = ch.lower()
        if low in LETTERS:
            base = LETTERS[low]
            j = i + 1
            breath = None
            accents = []
            iota = False
            while j < len(beta) and beta[j] in ')(/\\=|^+':
                if beta[j] == '(':          # TLG: ( = rough breathing
                    breath = 'rough'
                elif beta[j] == ')':        # TLG: ) = smooth breathing
                    breath = 'smooth'
                elif beta[j] in ACCENT:
                    accents.append(ACCENT[beta[j]])
                elif beta[j] == '|':
                    iota = True
                j += 1
            if cap or ch.isupper():
                base = base.upper()
                cap = False
            if breath == 'rough' and base.lower() in ROUGH:
                base = ROUGH[base.lower()].upper() if base.isupper() else ROUGH[base.lower()]
            elif breath == 'smooth' and base.lower() in SMOOTH:
                base = SMOOTH[base.lower()].upper() if base.isupper() else SMOOTH[base.lower()]
            # final sigma
            if base == 'σ' and (j >= len(beta) or not beta[j:j + 1].isalpha()):
                base = 'ς'
            out.append(base + ''.join(accents) + ('\u0345' if iota else ''))
            i = j
        else:
            if ch in '.,;:·':
                out.append({'.': '.', ',': ',', ';': ';', ':': '·', '·': '·'}[ch])
            else:
                out.append(ch)
            i += 1
    return unicodedata.normalize('NFC', ''.join(out))


def from_unicode(word):
    """Rough Unicode → beta code (for searching the LSJ dump)."""
    word = unicodedata.normalize('NFD', word)
    out = []
    mapping = {v: k for k, v in LETTERS.items()}
    cap_map = {v.upper(): k.upper() for k, v in {'a': 'Α', 'b': 'Β', 'g': 'Γ', 'd': 'Δ', 'e': 'Ε',
                                                 'z': 'Ζ', 'h': 'Η', 'q': 'Θ', 'i': 'Ι', 'k': 'Κ',
                                                 'l': 'Λ', 'm': 'Μ', 'n': 'Ν', 'c': 'Ξ', 'o': 'Ο',
                                                 'p': 'Π', 'r': 'Ρ', 's': 'Σ', 't': 'Τ', 'u': 'Υ',
                                                 'f': 'Φ', 'x': 'Χ', 'y': 'Ψ', 'w': 'Ω'}.items()}
    for ch in word:
        if ch == 'ς':
            out.append('s')
        elif ch in ('\u0314',):
            out.append('(')
        elif ch in ('\u0313',):
            out.append(')')
        elif ch == '\u0301':
            out.append('/')
        elif ch == '\u0300':
            out.append('\\')
        elif ch == '\u0342':
            out.append('=')
        elif ch == '\u0345':
            out.append('|')
        elif ch in mapping:
            out.append(mapping[ch])
        elif ch.upper() in cap_map:
            out.append(cap_map[ch.upper()])
        else:
            out.append(ch)
    return ''.join(out)


if __name__ == '__main__':
    import sys
    for a in sys.argv[1:]:
        if a.isascii():
            print(a, '->', to_unicode(a))
        else:
            print(a, '->', from_unicode(a))
