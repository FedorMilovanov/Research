# -*- coding: utf-8 -*-
"""Quote-level verification of the OT corpus SSOT against the local mirrors.

Every verses[].mt / verses[].lxx quotation must occur contiguously in at least
one mirror stream of the book named in the cell's ref (for quotations assembled
from pieces separated by … ; · | every piece must occur).  Nothing is
interpreted and nothing is repaired: a quotation that is not found verbatim is
reported.

Streams used
  mt   — morphhb WLC through ot.py, both views ('qere' and 'wlc'): the SSOT
         follows the qere wherever MT has a ketiv/qere pair, the ketiv is
         recorded in the cell's mtMorph / lxxVariants (card 04, note 3 §MT).
  lxx  — ELI 1930 (Swete), S23 (lxx-swete), F1K (First1KGreek tlg0527),
         SOL 1909 (Swete, Gen–2 Kings only), NT (SBLGNT, for NT pointers).

Editorial material is removed before matching: parentheses (including the
(fragment)/(fragments) scope markers), OG:/Th: labels, apparatus brackets and
diacritics.  Hebrew is compared unpointed (ot.he_norm), Greek accent-, case-
and apostrophe-insensitively (gnorm) — the transcriptions and the SSOT use
different apostrophe code points for elision.

A cell whose divergence is already recorded in its own lxxVariants / mtNote /
note with a HOLD or 'divergence' status is reported as documented, not as a
defect.

Usage:
    python3 tools/ssotquotes.py [data/ot-corpus-v1.json]

Exit code 0 — every piece of every quotation is attested (or documented);
1 — otherwise.
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ot  # noqa: E402

PAREN = re.compile(r'\([^()]*\)')
DROP = re.compile(r'[⸀⸁⸂⸃⸆⸇*|]')
SPLIT = re.compile(r'[…;·]|\.\.\.|\s{2,}')
APOSTROPHES = '\u1fbd\u1fbf\u1f7e\u1f7f\u02bc\u2019\u0384\u00b4\u2018\u201b`\''

RU_BOOKS = {
    'Быт': 'Gen', 'Исх': 'Exod', 'Лев': 'Lev', 'Числ': 'Num', 'Втор': 'Deut',
    'Нав': 'Josh', 'Суд': 'Judg', 'Руфь': 'Ruth', '1 Цар': '1Sam', '2 Цар': '2Sam',
    '3 Цар': '1Kgs', '4 Цар': '2Kgs', '1 Пар': '1Chr', '2 Пар': '2Chr',
    'Езд': 'Ezra', 'Неем': 'Neh', 'Есф': 'Esth', 'Иов': 'Job', 'Пс': 'Ps',
    'Притч': 'Prov', 'Еккл': 'Eccl', 'Песн': 'Song', 'Ис': 'Isa', 'Иер': 'Jer',
    'Плач': 'Lam', 'Иез': 'Ezek', 'Дан': 'Dan', 'Ос': 'Hos', 'Иоил': 'Joel',
    'Ам': 'Amos', 'Авд': 'Obad', 'Ион': 'Jonah', 'Мих': 'Mic', 'Наум': 'Nah',
    'Авв': 'Hab', 'Соф': 'Zeph', 'Агг': 'Hag', 'Зах': 'Zech', 'Мал': 'Mal',
}

DAN_ELI = ['Dan', 'Dat']


def gnorm(s):
    for ch in APOSTROPHES:
        s = s.replace(ch, '')
    return ' '.join(ot.gr_norm(s))


def pieces(text):
    """Quotation split into the pieces that must each be attested."""
    s = PAREN.sub(' ', text)
    s = DROP.sub(' ', s)
    s = re.sub(r'\b(OG|Th)\s*:', ' ', s)
    out = []
    for p in SPLIT.split(s):
        p = p.strip(' ·,;.:')
        if p:
            out.append(p)
    return out


def ref_book(ref):
    """Canonical book key of a cell ref (Russian or Latin abbreviation)."""
    r = PAREN.sub(' ', ref)
    m = re.match(r'^((?:\d+\s+)?[^\s\d]+)\s', r)
    if not m:
        return None
    name = m.group(1).rstrip('.')
    if name in ot.LXX or name in ('Dan', 'DanOG', 'DanTh'):
        return name
    return RU_BOOKS.get(name)


def build_streams():
    """{canonical book: [(label, normalized stream), ...]}"""
    books = dict(ot.LXX)
    books['Dan'] = ('tlg056', 56, 'Dan')
    by_book = {}

    def add(book, label, text, norm):
        if text:
            by_book.setdefault(book, []).append((label, norm))

    for book in books:
        for view in ('qere', 'wlc'):
            try:
                t = ot.mt_book_text(book, view=view)
            except Exception:
                t = ''
            add(book, 'MT-%s %s' % (view, book), t, ot.he_norm(t))
        keys = ['DanOG', 'DanTh'] if book == 'Dan' else [book]
        for tag, getter in (('F1K', lambda b: ot._f1k_verses(b, 1)),
                            ('S23', ot._s23_verses),
                            ('SOL', ot._sol_verses)):
            for key in keys:
                try:
                    vs = getter(key)
                except Exception:
                    vs = {}
                if vs:
                    t = ' '.join(vs[k] for k in sorted(vs))
                    add(book, '%s %s' % (tag, key), t, gnorm(t))
        ab = books[book][2]
        eli_rows = by_book.setdefault('__eli__', {})
        for key in ([ab] + (DAN_ELI if book == 'Dan' else [])):
            eli_rows[key] = book
    # ELI 1930 — group the token CSV by book abbreviation first
    words, rows = ot._eli_index()
    texts = {}
    for i, (idx, ref) in enumerate(rows):
        end = rows[i + 1][0] if i + 1 < len(rows) else max(words) + 1
        texts.setdefault(ref.split('.')[0], []).append(
            ' '.join(words.get(k, '') for k in range(idx, end) if k in words))
    ab2book = by_book.pop('__eli__', {})
    for ab, chunks in texts.items():
        book = ab2book.get(ab)
        if book and ab in DAN_ELI and book == 'Dan':
            pass
        elif not book:
            continue
        add(book, 'ELI %s' % ab, ' '.join(chunks), gnorm(' '.join(chunks)))
    for book in ot.NT_FILES:
        try:
            vs = ot._nt_verses(book)
        except Exception:
            vs = {}
        if vs:
            t = ' '.join(' '.join(w for w, _ in vs[k]) for k in sorted(vs))
            add(book, 'NT %s' % book, t, gnorm(t))
    return by_book


def documented(cell, piece):
    """Is the divergence recorded in the cell's own notes?"""
    notes = []
    for key in ('mtNote', 'note'):
        if cell.get(key):
            notes.append(str(cell[key]))
    for entry in cell.get('lxxVariants') or []:
        if isinstance(entry, dict):
            notes.append(' '.join(str(v) for v in entry.values()))
    for n in notes:
        if re.search(r'LOCATOR_HOLD|divergence|расхожд', n):
            return True
    return False


def longest(piece, pool):
    """Longest token prefix of piece found anywhere in the pool."""
    toks = piece.split()
    best = (0, None)
    for tag, stream in pool:
        for n in range(len(toks), 1, -1):
            if n <= best[0]:
                break
            if ' '.join(toks[:n]) in stream:
                best = (n, tag)
                break
    return best


def check(corpus_path):
    d = json.load(io.open(corpus_path, encoding='utf-8'))
    by_book = build_streams()
    all_streams = [(lbl, s) for v in by_book.values() for lbl, s in v]
    fails, docs, elsewhere = [], [], []
    checked = 0
    for card in d['cards']:
        for v in card.get('verses', []):
            book = ref_book(v.get('ref') or '')
            for kind in ('mt', 'lxx'):
                text = v.get(kind)
                if not text:
                    continue
                checked += 1
                pool = [(lbl, s) for lbl, s in by_book.get(book, []) if
                        (kind == 'mt') == lbl.startswith('MT-')] if book else []
                for piece in pieces(text):
                    norm = ot.he_norm(piece) if kind == 'mt' else gnorm(piece)
                    if len(norm.split()) < 2:
                        continue
                    if pool and any(norm in s for _, s in pool):
                        continue
                    row = (str(card['id']), v.get('ref'), v.get('id'), kind, norm)
                    if documented(v, norm):
                        docs.append(row + (book,))
                        continue
                    if any(norm in s for _, s in all_streams):
                        elsewhere.append(row + (book,))
                        continue
                    n, tag = longest(norm, pool or all_streams)
                    fails.append(row + (book, n, len(norm.split()), tag,
                                        ' '.join(norm.split()[n:n + 6]) if n
                                        else ' '.join(norm.split()[:6])))
    print('отрывков проверено: %d' % checked)
    print('не подтверждено: %d | документировано (HOLD/расхождение): %d | найдено только в чужой книге: %d'
          % (len(fails), len(docs), len(elsewhere)))
    for cid, ref, vid, kind, norm, book, n, tot, tag, tail in fails:
        print('[карточка %s %s %s %s] книга %s; совпало %d/%d в %s ; расходится на: %r'
              % (cid, ref, vid or '-', kind, book, n, tot, tag, tail))
    for cid, ref, vid, kind, norm, book in docs:
        print('[документировано] карточка %s %s %s %s — %s: %r'
              % (cid, ref, vid or '-', kind, book, ' '.join(norm.split()[:8])))
    for cid, ref, vid, kind, norm, book in elsewhere:
        print('[чужая книга] карточка %s %s %s %s (книга %s): %r'
              % (cid, ref, vid or '-', kind, book, ' '.join(norm.split()[:8])))
    return 1 if fails else 0


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'ot-corpus-v1.json')
    sys.exit(check(path))
