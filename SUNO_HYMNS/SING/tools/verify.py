#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify.py — сверка цитат серии SING с первоисточниками.

    python3 tools/verify.py selftest              калибровка корпусов (делать первой)
    python3 tools/verify.py greek                 все греческие цитаты (SBLGNT / LXX / TR)
    python3 tools/verify.py russian               все русские цитаты против Синодального
    python3 tools/verify.py hebrew                все еврейские цитаты против WLC
    python3 tools/verify.py all                   всё сразу
    python3 tools/verify.py all --report /tmp/rep.md
    python3 tools/verify.py greek --verbose       печатать и подтверждённые цитаты тоже

Принципы, по которым инструмент устроен:

1. ОДНА НОРМАЛИЗАЦИЯ НА ВСЁ. Индекс корпуса и цитата нормализуются одной и той же
   функцией. Расхождение нормализаций — главный источник ложной браковки: цитата
   «не находится» там, где она абсолютно верна.
2. СНАЧАЛА КАЛИБРОВКА. `selftest` сверяет каждый корпус по местам, известным наверняка.
   Если калибровка не прошла, отчёт недостоверен, и это видно сразу.
3. ССЫЛКА ИЩЕТСЯ ПО КОНТЕКСТУ, А НЕ ПО СТРОКЕ: ближайший заголовок выше (с разворотом
   полных названий книг), затем соседние строки, кроме табличных, затем окно ±12.
4. ИНСТРУМЕНТ НЕ ПРАВИТ ТЕКСТЫ. Он сообщает. Решение о правке — за человеком,
   и каждая правка вносится отдельным патчем с проверкой `count == 1`.
5. ОТЧЁТ ГРАДУИРОВАННЫЙ, а не «да/нет»: «точно», «расхождение» (с коэффициентом
   и текстом источника рядом), «не найдено». Средняя зона — это то, что надо читать
   глазами: там и наш собственный перевод, и неточная ссылка, и редкая ошибка текста.
"""

import argparse
import difflib
import glob
import os
import pickle
import re
import sys
import unicodedata

# =====================================================================
# 1. НОРМАЛИЗАЦИЯ
# =====================================================================

def norm_greek(word):
    """Греческое слово -> сопоставимая форма: без диакритик, коро́ниса, пунктуации.

    Коро́нис (U+1FBF) и придыхания отдельно: это НЕ буквы, и их нельзя оставлять,
    иначе `ἀπ’` != `απ` и цитата «не находится».
    """
    w = unicodedata.normalize('NFD', word)
    w = ''.join(ch for ch in w if unicodedata.category(ch) != 'Mn')
    w = w.lower()
    return ''.join(ch for ch in w
                   if unicodedata.category(ch).startswith('L')
                   and ('Ͱ' <= ch <= 'Ͽ' or 'ἀ' <= ch <= 'ῼ'))


HEB_FINALS = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'}

def norm_hebrew(word):
    """Еврейское слово -> согласные без огласовок и кантилляции; финальные формы к обычным."""
    out = []
    for ch in word:
        o = ord(ch)
        if 0x0591 <= o <= 0x05C7:            # кантилляция, огласовки, соф пасук
            continue
        if 0x05D0 <= o <= 0x05EA:            # согласные
            out.append(HEB_FINALS.get(ch, ch))
    return ''.join(out)


RUS_FOLD = {'і': 'и', 'ѣ': 'е', 'ѳ': 'ф', 'ѵ': 'и', 'ѫ': 'у', 'ѧ': 'я', '№': '№'}

def norm_rus(word):
    """Русское слово -> сопоставимая форма: ё→е, дореформенные буквы, без пунктуации и кавычек."""
    w = word.lower().replace('ё', 'е')
    w = ''.join(RUS_FOLD.get(ch, ch) for ch in w)
    w = w.rstrip('ъ')
    return ''.join(ch for ch in w if ch.isalpha() or ch.isdigit())


# =====================================================================
# 2. КАРТЫ КНИГ
# =====================================================================

# Новый Завет: номер файла morphgnt (61..87 = Mt..Re)
NT = {'Мф': 61, 'Мк': 62, 'Лк': 63, 'Ин': 64, 'Деян': 65, 'Рим': 66, '1 Кор': 67,
      '2 Кор': 68, 'Гал': 69, 'Еф': 70, 'Флп': 71, 'Кол': 72, '1 Фес': 73, '2 Фес': 74,
      '1 Тим': 75, '2 Тим': 76, 'Тит': 77, 'Флм': 78, 'Евр': 79, 'Иак': 80, '1 Пет': 81,
      '2 Пет': 82, '1 Ин': 83, '2 Ин': 84, '3 Ин': 85, 'Иуд': 86, 'Откр': 87}

# Имя файла TR Скривенера по номеру книги morphgnt
TR_FILE = {61: 'MT', 62: 'MR', 63: 'LU', 64: 'JOH', 65: 'AC', 66: 'RO', 67: '1CO',
           68: '2CO', 69: 'GA', 70: 'EPH', 71: 'PHP', 72: 'COL', 73: '1TH', 74: '2TH',
           75: '1TI', 76: '2TI', 77: 'TIT', 78: 'PHM', 79: 'HEB', 80: 'JAS', 81: '1PE',
           82: '2PE', 83: '1JO', 84: '2JO', 85: '3JO', 86: 'JUDE', 87: 'RE'}

# Ветхий Завет: код книги в LXX (books_main.csv)
OT_LXX = {'Быт': 'Gen', 'Исх': 'Exod', 'Лев': 'Lev', 'Числ': 'Num', 'Втор': 'Deut',
          'Нав': 'JoshB', 'Суд': 'JudgB', 'Руфь': 'Ruth', '1 Цар': '1Sam', '2 Цар': '2Sam',
          '3 Цар': '1Kgs', '4 Цар': '2Kgs', '1 Пар': '1Chr', '2 Пар': '2Chr', 'Ездр': 'Ezra',
          'Неем': 'Neh', 'Есф': 'Esth', 'Иов': 'Job', 'Пс': 'Ps', 'Притч': 'Prov',
          'Еккл': 'Qoh', 'Песн': 'Cant', 'Ис': 'Isa', 'Иер': 'Jer', 'Плач': 'Lam',
          'Иез': 'Ezek', 'Дан': 'DanOG', 'Ос': 'Hos', 'Иоил': 'Joel', 'Ам': 'Amos',
          'Авд': 'Obad', 'Ион': 'Jonah', 'Мих': 'Mic', 'Наум': 'Nah', 'Авв': 'Hab',
          'Соф': 'Zeph', 'Агг': 'Hag', 'Зах': 'Zech', 'Мал': 'Mal', 'Иудифь': 'Jdt',
          'ПсСол': 'PsSol', 'Сир': 'Sir', 'Прем': 'Wis'}

# Ветхий Завет: имя файла Ленинградского кодекса (openscriptures/morphhb, wlc/).
# Файлы называются ПОЛНЫМИ именами (Gen.xml, Ps.xml, Song.xml), а не кодами Вестминстера;
# книг 39 (еврейский канон) плюс служебный VerseMap.xml — всего 40 файлов.
OT_WLC = {'Быт': 'Gen', 'Исх': 'Exod', 'Лев': 'Lev', 'Числ': 'Num', 'Втор': 'Deut',
          'Нав': 'Josh', 'Суд': 'Judg', 'Руфь': 'Ruth', '1 Цар': '1Sam', '2 Цар': '2Sam',
          '3 Цар': '1Kgs', '4 Цар': '2Kgs', '1 Пар': '1Chr', '2 Пар': '2Chr',
          'Ездр': 'Ezra', 'Неем': 'Neh', 'Есф': 'Esth', 'Иов': 'Job', 'Пс': 'Ps',
          'Притч': 'Prov', 'Еккл': 'Eccl', 'Песн': 'Song', 'Ис': 'Isa', 'Иер': 'Jer',
          'Плач': 'Lam', 'Иез': 'Ezek', 'Дан': 'Dan', 'Ос': 'Hos', 'Иоил': 'Joel',
          'Ам': 'Amos', 'Авд': 'Obad', 'Ион': 'Jonah', 'Мих': 'Mic', 'Наум': 'Nah',
          'Авв': 'Hab', 'Соф': 'Zeph', 'Агг': 'Hag', 'Зах': 'Zech', 'Мал': 'Mal'}

# Перенумерация глав Иеремии: МТ -> LXX (оракулы о народах стоят в LXX в середине книги)
JER_MT2LXX = {**{i: i for i in range(1, 25)},
              46: 26, 47: 29, 48: 31, 49: 30, 50: 27, 51: 28,
              26: 33, 27: 34, 28: 35, 29: 36, 30: 37, 31: 38, 32: 39, 33: 40, 34: 41,
              35: 42, 36: 43, 37: 44, 38: 45, 39: 46, 40: 47, 41: 48, 42: 49, 43: 50,
              44: 51, 45: 51, 52: 52}


def mt2lxx(ps, verse):
    """Нумерация псалма и стиха по МТ -> нумерация LXX (принятая в серии таблица)."""
    if ps <= 9:                 return ps, verse
    if ps == 10:                return 9, verse + 21
    if 11 <= ps <= 113:         return ps - 1, verse
    if ps == 114:               return 113, verse
    if ps == 115:               return 113, verse + 8
    if ps == 116:               return (114, verse) if verse <= 9 else (115, verse - 9)
    if 117 <= ps <= 146:        return ps - 1, verse
    if ps == 147:               return (146, verse) if verse <= 11 else (147, verse - 11)
    return ps, verse


LEMMA_RE = re.compile(r'lemma="([^"]*)"')
MORPH_RE = re.compile(r'morph="([^"]*)"')


def lemma_of(attrs):
    """Номер леммы (Стронга) из атрибутов <w>.

    В morphhb лемма бывает составной: `l/5329` (предлог + лемма), `c/b/3915`,
    просто `3068`, или `2617 a`. Лемма слова — то, что после последнего слэша;
    из него берём число.
    """
    m = LEMMA_RE.search(attrs)
    if not m:
        return ''
    tail = m.group(1).split('/')[-1]
    d = re.match(r'\s*(\d+)', tail)
    return d.group(1) if d else ''


def morph_of(attrs):
    """Морфологический код слова (morphhb)."""
    m = MORPH_RE.search(attrs)
    return m.group(1) if m else ''


def lxx_code(books, book):
    """Книга LXX: и английское имя ('Ps'), и числовой код из индекса (230)."""
    if isinstance(book, int):
        return book
    return books.get(book)


# =====================================================================
# 3. КОРПУСА
# =====================================================================

BETA_MAP = {  # вариант бета-кода в byztxt/Scrivener: c=χ, x=ξ, y=θ, q=ψ, v=ς
    'a': 'α', 'b': 'β', 'g': 'γ', 'd': 'δ', 'e': 'ε', 'z': 'ζ', 'h': 'η', 'y': 'θ',
    'i': 'ι', 'k': 'κ', 'l': 'λ', 'm': 'μ', 'n': 'ν', 'x': 'ξ', 'o': 'ο', 'p': 'π',
    'r': 'ρ', 's': 'σ', 't': 'τ', 'u': 'υ', 'f': 'φ', 'c': 'χ', 'q': 'ψ', 'w': 'ω',
    'v': 'ς'}
BETA_DIAC = {'/': '́', '\\': '̀', '=': '͂', '|': 'ͅ', '+': '̈',
             ')': '̔', '(': '̓'}


def from_beta(word):
    out, i = [], 0
    while i < len(word):
        ch = word[i].lower()
        if ch in BETA_MAP:
            out.append(BETA_MAP[ch])
            i += 1
            while i < len(word) and word[i] in BETA_DIAC:
                i += 1
        else:
            i += 1
    return ''.join(out)


class Corpus:
    """Ленивая загрузка корпусов из /tmp/bible (см. fetch_corpora.sh)."""

    def __init__(self, root='/tmp/bible'):
        self.root = root
        self._nt = self._tr = self._lxx = self._rst = self._wlc = self._wlck = self._wlclemma = self._wlcfull = self._ntlemma = None
        self._books = {}          # (source, book) -> ([слова], [(глава, стих)])
        self._vocab = {}          # (source, book) -> множество слов

    # ---------- общий кэш ----------
    def _cached(self, name, builder):
        attr = '_' + name
        if getattr(self, attr) is None:
            setattr(self, attr, builder())
        return getattr(self, attr)

    # ---------- Новый Завет, morphgnt ----------
    def _nt_build(self, lemmas=False):
        idx = {}
        for path in glob.glob(os.path.join(self.root, 'sblgnt', '*-morphgnt.txt')):
            book = int(os.path.basename(path).split('-')[0])
            for line in open(path, encoding='utf-8'):
                parts = line.split()
                if len(parts) < 4:
                    continue
                ref = parts[0]
                ch, vs = int(ref[2:4]), int(ref[4:6])
                # morphgnt: ссылка, 2 морфокода, слово, нормализованная форма, лемма
                raw = parts[-1] if lemmas else parts[3]
                w = norm_greek(raw)
                if w:
                    idx.setdefault((book, ch, vs), []).append(w)
        return idx

    def nt(self):
        return self._cached('nt', lambda: self._nt_build())

    def nt_lemma(self):
        """(книга, глава, стих) -> [лемма] по morphgnt (лемма — последнее поле)."""
        return self._cached('ntlemma', lambda: self._nt_build(lemmas=True))

    def nt_count(self, lemma):
        """Сколько раз лемма стоит в Новом Завете и где: [(книга, глава, стих)]."""
        out = []
        for (book, ch, vs), ls in self.nt_lemma().items():
            for l in ls:
                if l == lemma:
                    out.append((book, ch, vs))
        return sorted(out)

    # ---------- TR Скривенера ----------
    def tr(self):
        def build():
            idx = {}
            for num, name in TR_FILE.items():
                path = os.path.join(self.root, 'tr', 'textonly', name + '.SCV')
                if not os.path.exists(path):
                    continue
                text = open(path, encoding='utf-8', errors='replace').read().replace('\n', ' ')
                chunks = re.split(r'(\d{1,3}:\d{1,3})', text)
                for k in range(1, len(chunks), 2):
                    ref, body = chunks[k], chunks[k + 1] if k + 1 < len(chunks) else ''
                    ch, vs = (int(x) for x in ref.split(':'))
                    words = [norm_greek(from_beta(w)) for w in body.split()]
                    idx[(num, ch, vs)] = [w for w in words if w]
            return idx
        return self._cached('tr', build)

    # ---------- Септуагинта ----------
    def lxx(self):
        def build():
            cache = os.path.join(self.root, 'lxx', '_index.pkl')
            if os.path.exists(cache):
                return pickle.load(open(cache, 'rb'))
            books = {}
            for line in open(os.path.join(self.root, 'lxx', 'books_main.csv'), encoding='utf-8'):
                f = line.strip().split('\t')
                if len(f) >= 4:
                    books[f[2]] = int(f[1])
            tag = re.compile(r'</?[Sm]>[^<]*</?[Sm]>|<[^>]+>')
            idx = {}
            for line in open(os.path.join(self.root, 'lxx', 'LXX_final_main.csv'), encoding='utf-8'):
                f = line.rstrip('\n').split('\t')
                if len(f) < 4:
                    continue
                book, ch, vs = int(f[0]), int(f[1]), int(f[2])
                words = [norm_greek(w) for w in tag.sub(' ', f[3]).split()]
                idx[(book, ch, vs)] = [w for w in words if w]
            data = (books, idx)
            pickle.dump(data, open(cache, 'wb'))
            return data
        return self._cached('lxx', build)

    # ---------- Синодальный ----------
    def rst(self):
        def build():
            idx, files = {}, {}
            for path in glob.glob(os.path.join(self.root, 'rst', '*.usfm')):
                head = open(path, encoding='utf-8').read(400)
                m = re.search(r'\\id\s+(\w+)', head)
                if m:
                    files[m.group(1)] = path
            code = {'Быт': 'GEN', 'Исх': 'EXO', 'Лев': 'LEV', 'Числ': 'NUM', 'Втор': 'DEU',
                    'Нав': 'JOS', 'Суд': 'JDG', 'Руфь': 'RUT', '1 Цар': '1SA', '2 Цар': '2SA',
                    '3 Цар': '1KI', '4 Цар': '2KI', '1 Пар': '1CH', '2 Пар': '2CH',
                    'Ездр': 'EZR', 'Неем': 'NEH', 'Есф': 'EST', 'Иов': 'JOB', 'Пс': 'PSA',
                    'Притч': 'PRO', 'Еккл': 'ECC', 'Песн': 'SNG', 'Ис': 'ISA', 'Иер': 'JER',
                    'Плач': 'LAM', 'Иез': 'EZK', 'Дан': 'DAN', 'Ос': 'HOS', 'Иоил': 'JOL',
                    'Ам': 'AMO', 'Авд': 'OBA', 'Ион': 'JON', 'Мих': 'MIC', 'Наум': 'NAM',
                    'Авв': 'HAB', 'Соф': 'ZEP', 'Агг': 'HAG', 'Зах': 'ZEC', 'Мал': 'MAL',
                    'Мф': 'MAT', 'Мк': 'MRK', 'Лк': 'LUK', 'Ин': 'JHN', 'Деян': 'ACT',
                    'Рим': 'ROM', '1 Кор': '1CO', '2 Кор': '2CO', 'Гал': 'GAL', 'Еф': 'EPH',
                    'Флп': 'PHP', 'Кол': 'COL', '1 Фес': '1TH', '2 Фес': '2TH', '1 Тим': '1TI',
                    '2 Тим': '2TI', 'Тит': 'TIT', 'Флм': 'PHM', 'Евр': 'HEB', 'Иак': 'JAS',
                    '1 Пет': '1PE', '2 Пет': '2PE', '1 Ин': '1JN', '2 Ин': '2JN', '3 Ин': '3JN',
                    'Иуд': 'JUD', 'Откр': 'REV'}
            for abbr, usfm in code.items():
                path = files.get(usfm)
                if not path:
                    continue
                text = open(path, encoding='utf-8').read()
                for book_block in re.split(r'\\c\s+', text)[1:]:
                    lines = book_block.split('\n')
                    ch = int(re.match(r'\s*(\d+)', lines[0]).group(1))
                    for vmark, body in zip(re.findall(r'\\v\s+(\d+)', book_block),
                                           re.split(r'\\v\s+\d+', book_block)[1:]):
                        body = re.sub(r'\\sp\b.*?\\sp\*', ' ', body, flags=re.S)
                        body = re.sub(r'\\[a-zA-Z]+\*?', ' ', body)
                        words = [norm_rus(w) for w in body.split()]
                        idx[(abbr, ch, int(vmark))] = [w for w in words if w]
            return idx
        return self._cached('rst', build)

    # ---------- Ленинградский кодекс ----------
    # morphhb даёт рядом написанное (x-ketiv) и читаемое (x-qere). Печатные издания
    # печатают кере, поэтому основной корпус строится по кере; по кетив строится
    # второй индекс (источник 'wlck') и опрашивается вторым (правило 60).
    # Пара «написано / читается» стоит в тексте рядом: <w type="x-ketiv">…</w> и сразу
    # за ним <note type="variant"><rdg type="x-qere"><w>…</w></rdg></note>. Совпадение
    # ищем только по соседству: иначе «.*?» съест весь текст между двумя разными парами.
    KQ = re.compile(r'<w type="x-ketiv"[^>]*>(.*?)</w>\s*'
                    r'<note type="variant">(.*?)</note>', re.S)
    KQ_QERE = re.compile(r'<rdg type="x-qere">\s*<w[^>]*>(.*?)</w>', re.S)

    def _wlc_kq(self, text, prefer):
        """Оставить по одному чтению из каждой пары кетив/кере (соседство обязательно)."""
        out, pos = [], 0
        for m in self.KQ.finditer(text):
            qere = self.KQ_QERE.search(m.group(2))
            if not qere:
                continue
            kept = qere.group(1) if prefer == 'qere' else m.group(1)
            out.append(text[pos:m.start()])
            out.append('<w>' + kept + '</w>')      # обёртка: иначе слово выпадет из разбора
            pos = m.end()
        out.append(text[pos:])
        return ''.join(out)

    def _wlc_build(self, prefer, mode='words'):
        idx = {}
        for abbr, stem in OT_WLC.items():
            path = os.path.join(self.root, 'wlc', stem + '.xml')
            if not os.path.exists(path):
                continue
            text = self._wlc_kq(open(path, encoding='utf-8').read(), prefer)
            for m in re.finditer(r'<verse osisID="([^"]+)"[^>]*>(.*?)</verse>',
                                 text, flags=re.S):
                osis, body = m.group(1), m.group(2)
                ref = osis.split('.')
                if len(ref) != 3:
                    continue
                try:
                    ch, vs = int(ref[1]), int(ref[2])
                except ValueError:
                    continue
                tags = re.findall(r'<w\b([^>]*)>(.*?)</w>', body, flags=re.S)
                words = [norm_hebrew(t) for a, t in tags]
                pairs = [(w, a) for w, (a, t) in zip(words, tags) if w]
                if not pairs:
                    continue
                if mode == 'lemmas':
                    idx[(abbr, ch, vs)] = [lemma_of(a) for _, a in pairs]
                elif mode == 'full':
                    idx[(abbr, ch, vs)] = [(w, lemma_of(a), morph_of(a))
                                           for w, a in pairs]
                else:
                    idx[(abbr, ch, vs)] = [w for w, _ in pairs]
        return idx

    def wlc(self):
        return self._cached('wlc', lambda: self._wlc_build('qere'))

    def wlc_ketiv(self):
        return self._cached('wlck', lambda: self._wlc_build('ketiv'))

    def wlc_lemma(self):
        """(книга, глава, стих) -> [номер леммы (Стронга)] по кере."""
        return self._cached('wlclemma', lambda: self._wlc_build('qere', mode='lemmas'))

    def wlc_full(self):
        """(книга, глава, стих) -> [(слово, лемма, морфологический код)] по кере."""
        return self._cached('wlcfull', lambda: self._wlc_build('qere', mode='full'))

    def forms_of_lemma(self, lemma, book=None):
        """Все формы леммы: [(книга, глава, стих, слово, морфкод)]."""
        out = []
        for (abbr, ch, vs), items in self.wlc_full().items():
            if book and abbr != book:
                continue
            for w, l, m in items:
                if l == str(lemma):
                    out.append((abbr, ch, vs, w, m))
        return sorted(out)

    def verses_with_lemma(self, lemma, book=None):
        """Стихи, где стоит слово этой леммы: [(книга, глава, стих)]."""
        out = []
        for (abbr, ch, vs), ls in self.wlc_lemma().items():
            if book and abbr != book:
                continue
            if str(lemma) in ls:
                out.append((abbr, ch, vs))
        return sorted(out)

    def words_with_lemma(self, lemma, book=None):
        """Слова этой леммы: [(книга, глава, стих, слово)]."""
        words = self.wlc()
        out = []
        for key, ls in self.wlc_lemma().items():
            if book and key[0] != book:
                continue
            for i, l in enumerate(ls):
                if l == str(lemma) and key in words and i < len(words[key]):
                    out.append((key[0], key[1], key[2], words[key][i]))
        return sorted(out)

    # ---------- доступ по главе ----------
    def chapter(self, source, book, chapter):
        """Возвращает [(номер стиха, [слова])] по главе; пусто, если корпус недоступен."""
        try:
            if source == 'nt':
                idx = self.nt()
                keys = [(k, v) for k, v in idx.items() if k[0] == book and k[1] == chapter]
            elif source == 'tr':
                idx = self.tr()
                keys = [(k, v) for k, v in idx.items() if k[0] == book and k[1] == chapter]
            elif source == 'lxx':
                books, idx = self.lxx()
                code = lxx_code(books, book)
                if code is None:
                    return []
                keys = [(k, v) for k, v in idx.items() if k[0] == code and k[1] == chapter]
            elif source == 'rst':
                idx = self.rst()
                keys = [(k, v) for k, v in idx.items() if k[0] == book and k[1] == chapter]
            elif source in ('wlc', 'wlck'):
                idx = self.wlc() if source == 'wlc' else self.wlc_ketiv()
                keys = [(k, v) for k, v in idx.items() if k[0] == book and k[1] == chapter]
            else:
                return []
        except (FileNotFoundError, OSError):
            return []
        keys.sort(key=lambda kv: kv[0][2])
        return [(k[2], v) for k, v in keys]

    # ---------- книга целиком (для поиска «где же это на самом деле») ----------
    def book_words(self, source, book):
        """Все слова книги подряд + владелец каждого слова (глава, стих)."""
        key = (source, book)
        if key in self._books:
            return self._books[key]
        try:
            if source in ('nt', 'tr'):
                idx = self.nt() if source == 'nt' else self.tr()
                keys = sorted(k for k in idx if k[0] == book)
            elif source == 'lxx':
                books, idx = self.lxx()
                keys = sorted(k for k in idx if k[0] == lxx_code(books, book))
            else:
                if source == 'rst':
                    idx = self.rst()
                elif source == 'wlck':
                    idx = self.wlc_ketiv()
                else:
                    idx = self.wlc()
                keys = sorted(k for k in idx if k[0] == book)
        except (FileNotFoundError, OSError):
            self._books[key] = ([], [])
            self._vocab[key] = set()
            return self._books[key]
        flat, owner = [], []
        for k in keys:
            for w in idx[k]:
                flat.append(w)
                owner.append((k[1], k[2]))
        self._books[key] = (flat, owner)
        self._vocab[key] = set(flat)
        return self._books[key]

    def locate_in_book(self, source, book, segs):
        """Сегменты внутри книги целиком -> (глава, стих, стих)."""
        flat, owner = self.book_words(source, book)
        pos, first, last = 0, None, None
        for seg in segs:
            hit = None
            for i in range(pos, len(flat) - len(seg) + 1):
                if flat[i:i + len(seg)] == seg:
                    hit, start = i + len(seg), i
                    break
            if hit is None:
                return None
            if first is None:
                first = owner[start]
            last = owner[hit - 1]
            pos = hit
        return first[0], first[1], last[1]

    def all_books(self, source):
        """Все книги корпуса (ключи как они хранятся в индексе)."""
        try:
            if source == 'nt':
                return sorted({k[0] for k in self.nt()})
            if source == 'tr':
                return sorted({k[0] for k in self.tr()})
            if source == 'lxx':
                books, idx = self.lxx()
                return sorted({k[0] for k in idx})
            if source == 'rst':
                return sorted({k[0] for k in self.rst()})
            if source == 'wlc':
                return sorted({k[0] for k in self.wlc()})
        except (FileNotFoundError, OSError):
            return []
        return []

    def book_name(self, source, book):
        """Ключ книги -> русское сокращение."""
        if source in ('nt', 'tr'):
            for abbr, num in NT.items():
                if num == book:
                    return abbr
        if source == 'lxx':
            books = self.lxx()[0]
            for abbr, code in OT_LXX.items():
                if books.get(code) == book:
                    return abbr
        return str(book)

    def locate_anywhere(self, sources, segs, prefer=None):
        """Где эта цитата стоит на самом деле.

        `prefer` — список (source, book), которые надо попробовать первыми (обычно
        книга, названная в тексте). Перебор дешёвый: сканируем только те книги,
        в словаре которых есть все слова цитаты.
        """
        words = {w for seg in segs for w in seg}
        prefer = prefer or []
        sources = tuple(sources)
        if 'wlc' in sources:
            sources = sources + ('wlck',)          # кере, потом кетив
        for source in sources:
            books = self.all_books(source)
            first = [b for (src, b) in prefer if src == source and b in books]
            order = first + [b for b in books if b not in first]
            for book in order:
                self.book_words(source, book)                  # построить словарь книги
                if not words <= self._vocab.get((source, book), set()):
                    continue
                loc = self.locate_in_book(source, book, segs)
                if loc:
                    return source, book, loc
        return None

    def best_ratio_in_book(self, source, book, quote):
        """Лучшее сходство цитаты с окном внутри книги -> (коэффициент, глава, стих, окно)."""
        flat, owner = self.book_words(source, book)
        if not flat or not quote:
            return 0.0, None, None, None
        n = len(quote)
        best, at, size_best = 0.0, 0, n
        for size in (n, n + 2, max(1, n - 2)):
            step = 1 if size <= 12 else 3      # длинные цитаты сканируем разреженно
            for i in range(0, max(1, len(flat) - size + 1), step):
                r = difflib.SequenceMatcher(None, flat[i:i + size], quote).ratio()
                if r > best:
                    best, at, size_best = r, i, size
        return best, owner[at][0], owner[at][1], flat[at:at + size_best]

    def has(self, source):
        if source == 'nt':
            return bool(glob.glob(os.path.join(self.root, 'sblgnt', '*-morphgnt.txt')))
        if source == 'tr':
            return os.path.isdir(os.path.join(self.root, 'tr', 'textonly'))
        if source == 'lxx':
            return os.path.exists(os.path.join(self.root, 'lxx', 'LXX_final_main.csv'))
        if source == 'rst':
            return bool(glob.glob(os.path.join(self.root, 'rst', '*.usfm')))
        if source in ('wlc', 'wlck'):
            return bool(glob.glob(os.path.join(self.root, 'wlc', '*.xml')))
        return False


# =====================================================================
# 4. РАЗБОР ФАЙЛОВ СЕРИИ
# =====================================================================

BOOKKEYS = sorted(set(list(NT) + list(OT_LXX)), key=len, reverse=True)
REF = re.compile(r'(%s)\.?\s*(\d{1,3}):(\d{1,3})' % '|'.join(re.escape(k) for k in BOOKKEYS))

FULL_NAMES = [
    (r'(\d)\s*Коринфянам', r'\1 Кор'), (r'(\d)\s*Фессалоникийцам', r'\1 Фес'),
    (r'(\d)\s*Тимофею', r'\1 Тим'), (r'(\d)\s*Петра', r'\1 Пет'),
    (r'\bМатфе(?:я|й)\b', 'Мф'), (r'\bМарк(?:а|у)?\b', 'Мк'), (r'\bЛук(?:и|а)\b', 'Лк'),
    (r'\bИоанна\b', 'Ин'), (r'\bДеяни(?:й|я)\b', 'Деян'), (r'\bРимлянам\b', 'Рим'),
    (r'\bГалатам\b', 'Гал'), (r'\bЕфесянам\b', 'Еф'), (r'\bФилиппийцам\b', 'Флп'),
    (r'\bКолоссянам\b', 'Кол'), (r'\bТиту\b', 'Тит'), (r'\bФилимону\b', 'Флм'),
    (r'\bЕвреям\b', 'Евр'), (r'\bИаков(?:а|у)\b', 'Иак'), (r'\bИуды\b', 'Иуд'),
    (r'\b(?:Откровени(?:я|е)|Апокалипсис)\b', 'Откр'),
    (r'\bПсал(?:ом|ма|ме|тырь)\b', 'Пс'), (r'\bИсаи(?:я|и)\b', 'Ис'),
    (r'\bИереми(?:я|и)\b', 'Иер'), (r'\bАмос(?:а|у)?\b', 'Ам'), (r'\bОси(?:я|и)\b', 'Ос'),
    (r'\bМихе(?:я|ю)\b', 'Мих'), (r'\bИо(?:ва|ву)\b', 'Иов'), (r'\bИсход(?:а|е)\b', 'Исх'),
    (r'\bВторозакони(?:я|е)\b', 'Втор'), (r'\bИезекиил(?:я|ю)\b', 'Иез'),
    (r'\bПритч(?:и|ей|ам)\b', 'Притч'), (r'\bНееми(?:и|я)\b', 'Неем'),
    (r'\bДаниил(?:а|у)\b', 'Дан'), (r'\bИудифи\b', 'Иудифь')]


def expand_names(line):
    for pattern, repl in FULL_NAMES:
        line = re.sub(pattern, repl, line)
    return line


def read_units(path):
    """Цитатные единицы файла: (номер строки, вид, текст).

    Виды: 'врезка' (цитата `>`), 'в строке' (обратные кавычки), 'русская' («кавычки»).
    Врезки склеиваются: в Markdown перевод строки внутри цитаты — это пробел.
    """
    lines = open(path, encoding='utf-8').read().split('\n')
    units, i = [], 0
    while i < len(lines):
        if lines[i].startswith('>'):
            block, start = [], i + 1
            while i < len(lines) and lines[i].startswith('>'):
                block.append(re.sub(r'^>\s?', '', lines[i]))
                i += 1
            # две цитаты подряд внутри одной врезки — это две единицы, а не одна
            joined = ' '.join(block)
            pieces = re.split(r'(?<=»)\s*(?:\([^)]{0,40}\)\s*)?(?=«)', joined)
            for n, piece in enumerate(pieces):
                if piece.strip():
                    units.append((start, 'врезка', piece))
            continue
        for m in re.finditer(r'`([^`\n]+)`', lines[i]):
            units.append((i + 1, 'в строке', m.group(1)))
        for m in re.finditer(r'«([^»]{6,}?)»', lines[i]):
            units.append((i + 1, 'русская', m.group(1)))
        i += 1
    return lines, units


def find_refs(lines, start, limit=6):
    """Ссылки на Писание для цитаты: сначала ближайший заголовок, потом соседние строки."""
    refs = []
    for j in range(start - 1, max(-1, start - 15), -1):
        if lines[j].startswith('#'):
            refs += REF.findall(expand_names(lines[j]))
            break
    for d in (0, -1, 1, -2, 2, -3, 3):
        j = start - 1 + d
        if not (0 <= j < len(lines)):
            continue
        # Своя строка — самый надёжный источник ссылки, пусть даже табличная.
        # Соседние строки таблиц не берём: там ссылки из других столбцов и строк.
        if d != 0 and lines[j].lstrip().startswith('|'):
            continue
        refs += REF.findall(lines[j])
    if not refs:
        refs = REF.findall('\n'.join(lines[max(0, start - 12):start + 10]))
    out = []
    for r in refs:
        if r not in out:
            out.append(r)
    return out[:limit]


# =====================================================================
# 5. СЛИЧЕНИЕ
# =====================================================================

ELLIPSIS = re.compile(r'\s*(?:…|\.\.\.|\[\.\.\.\]|\*…\*|\*\*…\*\*)\s*')


def segments(text, normalizer, keep):
    """Цитата -> список сегментов (по многоточию) из нормализованных слов."""
    out = []
    for part in ELLIPSIS.split(text):
        words = [normalizer(w) for w in part.split()]
        words = [w for w in words if w and keep(w)]
        if words:
            out.append(words)
    return out


def locate(verses, segs):
    """Все сегменты стоят в главе в порядке возрастания позиций -> (стих, стих)."""
    flat, owner = [], []
    for verse, words in verses:
        flat += words
        owner += [verse] * len(words)
    pos, first, last = 0, None, None
    for seg in segs:
        hit = None
        for i in range(pos, len(flat) - len(seg) + 1):
            if flat[i:i + len(seg)] == seg:
                hit = i + len(seg)
                start = i
                break
        if hit is None:
            return None
        if first is None:
            first = owner[start]
        last = owner[hit - 1]
        pos = hit
    return first, last


def best_ratio(verses, quote):
    """Максимальное сходство цитаты с окном внутри главы (для русских цитат)."""
    flat = []
    for _, words in verses:
        flat += words
    n = len(quote)
    if not n or not flat:
        return 0.0, None
    best, at = 0.0, None
    for size in (n, n + 2, max(1, n - 2)):
        for i in range(0, max(1, len(flat) - size + 1)):
            window = flat[i:i + size]
            r = difflib.SequenceMatcher(None, window, quote).ratio()
            if r > best:
                best, at = r, i
    return best, flat[at:at + len(quote)] if at is not None else None


def looks_like_quote(text):
    """Отсеять нашу собственную речь в «кавычках» — это не цитата из Писания."""
    noise = ('Синодальный', '(МТ', 'Син.)', 'ARCHIVE_HOLD', 'LOCATOR_HOLD', 'HOLD',
             'часть ', 'см. ', ' раздел', 'таблиц', '=', '⟦', '⟧')
    return not any(n in text for n in noise)


MARKERS = re.compile(r'наш перевод|перевод серии|перевожу|мы переводим|перевод наш|'
                     r'переда[юё]м|точнее|буквально|в отличие от Синодального|'
                     r'Синодальны[йм] (?:читает|передаёт|ставит|говорит|идёт)|'
                     r'Вариация чтения|вариант перевода|не Синодальный', re.I)


def is_marked(lines, start, text):
    """Помечено ли расхождение как перевод серии: возвращает пометку или ''.

    Конвенция серии (правило 49а в чартере): русский текст в «кавычках» — это либо
    Синодальный, либо наш перевод, и читатель должен видеть, что именно. Видно это тремя
    способами, и все три инструмент распознаёт:
      • жирная подача: **«…»**;
      • перевод при греческой или еврейской цитате: «…» рядом с языком оригинала;
      • явная оговорка в соседних строках («наш перевод», «Вариация чтения»…).
    """
    raw = lines[start - 1] if 0 <= start - 1 < len(lines) else ''
    if re.search(r'\*\*«', raw):
        return 'жирная подача перевода'
    if '**' in text:
        return 'выделение внутри цитаты'
    if raw.lstrip().startswith('|'):          # строка таблицы: пометка — в её заголовке
        for j in range(start - 2, max(-1, start - 40), -1):
            if not lines[j].lstrip().startswith('|'):
                break
            if re.search(r'перевод|Синодальн|наш', lines[j], re.I):
                return 'заголовок таблицы: ' + lines[j].strip()[:60]
    if re.search(r'[Ͱ-Ͽἀ-ῼ֐-׿]', raw) and '«' in raw:
        return 'перевод при цитате на языке оригинала'
    if re.search(r'(?:утверждает|читает|передаёт|называет|говорит|написано|сказано)'
                 r'[^«]{0,40}«', raw, re.I):
        return 'атрибуция источника в строке'
    context = '\n'.join(lines[max(0, start - 12):start + 6])
    m = MARKERS.search(context)
    return m.group(0) if m else ''


# =====================================================================
# 6. ПРОВЕРКИ
# =====================================================================

class Result:
    __slots__ = ('file', 'line', 'kind', 'ref', 'status', 'where', 'quote', 'source', 'marked')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k, '' if k != 'marked' else None))


def candidates_lxx(abbr, chapter):
    """Кандидаты глав LXX для ссылки: с учётом сдвига псалмов и перенумерации Иеремии."""
    if abbr == 'Пс':
        return [(OT_LXX['Пс'], mt2lxx(chapter, 1)[0], 'LXX Пс %d' % mt2lxx(chapter, 1)[0]),
                (OT_LXX['Пс'], chapter, 'Пс %d (без сдвига)' % chapter)]
    if abbr == 'Иер':
        return [(OT_LXX['Иер'], JER_MT2LXX.get(chapter, chapter),
                 'LXX Иер %d' % JER_MT2LXX.get(chapter, chapter)),
                (OT_LXX['Иер'], chapter, 'Иер %d (без сдвига)' % chapter)]
    return [(OT_LXX[abbr], chapter, '%s %d' % (abbr, chapter))]


def candidates_rst(abbr, chapter):
    """Кандидаты для Синодального: номер как есть и, для псалмов, со сдвигом из МТ."""
    if abbr == 'Пс':
        return [(chapter, 'Пс %d (Син.)' % chapter),
                (mt2lxx(chapter, 1)[0], 'Пс %d (из МТ)' % mt2lxx(chapter, 1)[0])]
    return [(chapter, '%s %d' % (abbr, chapter))]


def check_greek(parts, corpus, min_words=4, verbose=False):
    results = []
    for path in parts:
        lines, units = read_units(path)
        for start, kind, text in units:
            greek = len(re.findall(r'[Ͱ-Ͽἀ-ῼ]', text))
            segs = segments(text, norm_greek, bool)
            nwords = sum(len(s) for s in segs)
            if greek < 8 or not segs:
                continue
            if kind == 'в строке' and nwords < min_words:
                continue                      # одиночная лемма — не цитата
            refs = find_refs(lines, start)
            status, where, source_text = 'не найдено', '', ''
            for abbr, ch, vs in refs:
                for source, book, chapter, sign in (greek_candidates(abbr, int(ch))):
                    verses = corpus.chapter(source, book, chapter)
                    if not verses:
                        continue
                    loc = locate(verses, segs)
                    if loc:
                        a, b = loc
                        status = 'точно'
                        where = '%s:%d%s (%s)' % (sign, a, '' if b == a else '-%d' % b,
                                                  {'nt': 'SBLGNT', 'lxx': 'LXX',
                                                   'tr': 'TR'}[source])
                        break
                    r, _ = best_ratio(verses, [w for s in segs for w in s])
                    if r > 0.6 and not source_text:
                        source_text = 'похоже на %s (%d%%)' % (sign, round(r * 100))
                if status == 'точно':
                    break
            if status != 'точно':
                prefer = []
                for abbr, ch, vs in refs[:3]:
                    if abbr in NT:
                        prefer.append(('nt', NT[abbr]))
                    if abbr in OT_LXX and corpus.has('lxx'):
                        code = corpus.lxx()[0].get(OT_LXX[abbr])
                        if code is not None:
                            prefer.append(('lxx', code))
                hit = corpus.locate_anywhere(('nt', 'lxx'), segs, prefer=prefer)
                if hit:
                    src, book, (chap, v1, v2) = hit
                    status = 'найдено в другом месте'
                    where = '%s %d:%d%s (%s)' % (corpus.book_name(src, book), chap, v1,
                                                 '' if v2 == v1 else '-%d' % v2,
                                                 {'nt': 'SBLGNT', 'lxx': 'LXX'}[src])
            if status != 'точно' and source_text and status != 'найдено в другом месте':
                status = 'расхождение'
                where = source_text
            if status == 'точно' and not verbose:
                results.append(Result(file=os.path.basename(path), line=start, kind=kind,
                                      ref=refs[0] if refs else '', status=status, where=where,
                                      quote='', source=''))
                continue
            results.append(Result(file=os.path.basename(path), line=start, kind=kind,
                                  ref='%s %s:%s' % refs[0] if refs else '', status=status,
                                  where=where,
                                  quote=' … '.join(' '.join(s) for s in segs)[:160],
                                  source=source_text))
    return results


def greek_candidates(abbr, chapter):
    """[(source, book, chapter, подпись)] для греческой ссылки."""
    out = []
    if abbr in NT:
        out.append(('nt', NT[abbr], chapter, '%s %d' % (abbr, chapter)))
    if abbr in OT_LXX:
        for code, ch, sign in candidates_lxx(abbr, chapter):
            out.append(('lxx', code, ch, sign))
    return out


def _find_hebrew(corpus, segs, refs):
    """Поиск еврейской цитаты: сначала по ссылке, потом по всему корпусу.

    Пробует два написания каждого сегмента: как он стоит в тексте и с союзом «вав»
    в начале (правило 60б) — слово часто цитируют с префиксом, а в Писании оно идёт
    без него (или наоборот). И два чтения рукописи: кере, потом кетив (правило 60).
    """
    PREFIX = 'ובכלמהש'                       # союзы и предлоги, пишущиеся слитно
    variants = [segs]
    if len(segs) <= 4:
        for pre in PREFIX:
            variants.append([[pre + seg[0]] + seg[1:] for seg in segs])

    def once(vsegs):
        for abbr, ch, vs in refs:
            if abbr not in OT_WLC:
                continue
            for chapter in ({int(ch), mt2lxx(int(ch), 1)[0]} if abbr == 'Пс' else {int(ch)}):
                for src in ('wlc', 'wlck'):
                    verses = corpus.chapter(src, abbr, chapter)
                    loc = locate(verses, vsegs) if verses else None
                    if loc:
                        a, b = loc
                        return ('точно', 'WLC %s %d:%d%s%s' % (
                            abbr, chapter, a, '' if b == a else '-%d' % b,
                            ' (по кетив)' if src == 'wlck' else ''))
        prefer = [('wlc', abbr) for abbr, ch, vs in refs[:3] if abbr in OT_WLC]
        hit = corpus.locate_anywhere(('wlc',), vsegs, prefer=prefer)
        if hit:
            _, book, (chap, v1, v2) = hit
            return ('найдено в другом месте',
                    'WLC %s %d:%d%s%s' % (book, chap, v1, '' if v2 == v1 else '-%d' % v2,
                                          ' (по кетив)' if _ == 'wlck' else ''))
        return ('не найдено', '')

    best = ('не найдено', '')
    for n, vsegs in enumerate(variants):
        status, where = once(vsegs)
        if status == 'точно':
            return status, (where + ' (с приставкой)' if n else where)
        if status == 'найдено в другом месте':
            best = (status, (where + ' (с приставкой)' if n else where))
    return best


def check_hebrew(parts, corpus, min_words=2):
    results = []
    for path in parts:
        lines, units = read_units(path)
        for start, kind, text in units:
            if len(re.findall(r'[֐-׿]', text)) < 4:
                continue
            items = [t for t in re.split(r'\s*·\s*', text) if t.strip()] if '·' in text else [text]
            groups = []
            for item in items:
                segs = segments(item, norm_hebrew, bool)
                if not segs or sum(len(x) for x in segs) < min_words:
                    continue
                groups.append(segs)
            if not groups:
                continue
            refs = find_refs(lines, start)
            if len(groups) > 1:                    # список лексем: проверяем каждую порознь
                found = 0
                for segs in groups:
                    status, _ = _find_hebrew(corpus, segs, refs)
                    found += (status == 'точно')
                results.append(Result(
                    file=os.path.basename(path), line=start, kind=kind,
                    ref=('%s %s:%s' % refs[0]) if refs else '',
                    status='список: найдено %d из %d' % (found, len(groups)),
                    where='', quote=text[:160]))
                continue
            segs = groups[0]
            status, where = _find_hebrew(corpus, segs, refs)
            if status == 'не найдено' and refs:
                quote = [w for x in segs for w in x]
                r, ch, vs, win = corpus.best_ratio_in_book(
                    'wlc', refs[0][0], quote) if refs[0][0] in OT_WLC else (0, 0, 0, [])
                if r >= 0.8:
                    where = 'похоже на %s %s:%s (%.0f%%): %s' % (
                        refs[0][0], ch, vs, r * 100, ' '.join(win)[:70])
            results.append(Result(file=os.path.basename(path), line=start, kind=kind,
                                  ref=('%s %s:%s' % refs[0]) if refs else '', status=status,
                                  where=where,
                                  quote=' … '.join(' '.join(x) for x in segs)[:160]))
    return results


def check_russian(parts, corpus, min_words=3, exact=0.95, fuzzy=0.6):
    results = []
    for path in parts:
        lines, units = read_units(path)
        for start, kind, text in units:
            words = [norm_rus(w) for w in text.split()]
            words = [w for w in words if w and not w.isdigit()]  # номера стихов внутри врезок
            if len(words) < min_words:
                continue
            if len(re.findall(r'[Ͱ-Ͽἀ-ῼ]|[֐-׿]', text)):
                continue                       # не русская цитата
            if kind == 'русская' and not looks_like_quote(text):
                continue                       # наша собственная речь, не цитата
            refs = find_refs(lines, start)
            if not refs:
                continue
            best = (-1.0, None, None, None)   # -1: полное несовпадение не маскируется под «нет корпуса»
            for abbr, ch, vs in refs[:4]:
                for chapter, sign in candidates_rst(abbr, int(ch)):
                    verses = corpus.chapter('rst', abbr, chapter)
                    if not verses:
                        continue
                    r, window = best_ratio(verses, words)
                    if r > best[0]:
                        best = (r, sign, abbr, window)
            r, sign, abbr, window = best
            if sign is None:
                status, where = 'нет корпуса', ''
            elif r >= exact:
                status, where = 'точно', sign
            elif r >= fuzzy:
                status, where = 'расхождение', '%s (%d%%)' % (sign, round(r * 100))
            else:
                status, where = 'не найдено', '%s (%d%%)' % (sign, round(r * 100))
            if status == 'не найдено' and sign is not None:
                abbr0 = refs[0][0]
                r2, ch2, v2, win = corpus.best_ratio_in_book('rst', abbr0, words)
                if r2 >= exact:
                    status = 'точно'
                    where = '%s %s:%s (в другой нумерации)' % (abbr0, ch2, v2)
                    window = win
                elif r2 >= fuzzy:
                    status = 'найдено в другом месте'
                    where = '%s %s:%s (%d%%)' % (abbr0, ch2, v2, round(r2 * 100))
                    window = win
                elif r2 > r:
                    where = 'ближайшее: %s %s:%s (%d%%)' % (abbr0, ch2, v2, round(r2 * 100))
                    window = win
            if status == 'не найдено':
                # последняя добивка: теми же словами, но в другой книге (правило 61)
                hit = corpus.locate_anywhere(('rst',), [words], prefer=[('rst', abbr0)])
                if hit:
                    _, book, (ch3, v1, v2) = hit
                    status = 'найдено в другом месте'
                    where = '%s %s:%s%s (слово в слово)' % (
                        book, ch3, v1, '' if v2 == v1 else '-%d' % v2)
                    window = corpus.rst().get((book, ch3, v1), [])[:len(words) + 6]
            results.append(Result(file=os.path.basename(path), line=start, kind=kind,
                                  ref=('%s %s:%s' % refs[0]), status=status, where=where,
                                  quote=text[:120],
                                  source=' '.join(window) if window else '',
                                  marked=is_marked(lines, start, text) if status != 'точно' else ''))
    return results


# =====================================================================
# 7. КАЛИБРОВКА
# =====================================================================

CALIBRATION = [
    ('nt',  'Еф 5:19',      ['ψαλμοις', 'υμνοις', 'ωδαις']),
    ('nt',  '1 Кор 14:15',  ['ψαλω', 'τω', 'πνευματι']),
    ('nt',  'Мф 26:30',     ['υμνησαντες', 'εξηλθον']),
    ('nt',  'Евр 2:12',     ['απαγγελω', 'υμνησω']),
    ('lxx', 'Пс 97:1',      ['ψαλμος', 'τω', 'δαυιδ', 'ασατε']),
    ('lxx', 'Пс 21:23',     ['εκκλησιας', 'υμνησω']),
    ('lxx', 'Пс 150:4',     ['χορδαις', 'οργανω']),
    ('lxx', 'Ам 5:23',      ['ηχον', 'ωδων', 'σου', 'οργανων']),
    ('tr',  '1 Кор 14:19',  ['δια', 'του', 'νοος', 'μου']),
    ('tr',  'Деян 17:25',   ['διδους', 'πασιν', 'ζωην', 'πνοην']),
    ('tr',  'Еф 5:19',      ['αδοντες', 'ψαλλοντες', 'εν', 'τη', 'καρδια']),
    ('rst', 'Ин 3:16',      ['возлюбил', 'бог', 'мир']),
    ('rst', 'Мф 5:3',       ['блаженны', 'нищие', 'духом']),
    ('rst', 'Пс 96:1',      ['господь', 'царствует']),
    ('wlc', 'Быт 1:1',      ['בראשית', 'ברא', 'אלהימ']),   # финальные формы нормализованы
    ('wlc', 'Пс 1:1',       ['אשרי', 'האיש']),
    # кетив и кере — разные чтения одного места: в кере «песнь Его», в кетив «песнь»
    ('wlc', 'Пс 42:9',      ['יוממ', 'יצוה', 'שירו', 'עמי']),
    ('wlck', 'Пс 42:9',     ['יוממ', 'יצוה', 'שירה', 'עמי']),
    ('wlc', '1 Пар 25:1',   ['הנבאימ', 'בכנרות', 'בנבלימ']),   # קרי: הנבאים
]


CALIBRATION_FILE = """# Калибровочный файл (не часть серии): эталоны — что бывает, а чего не бывает

В заголовке каждого эталона стоит ровно одна ссылка: та, которую видит инструмент.
Никаких других кавычек и ссылок в файле быть не должно, иначе эталон считает не то.

### Эталон 1. Верная греческая цитата, верная ссылка (Ин 1:1)

> ἐν ἀρχῇ ἦν ὁ λόγος

### Эталон 2. Та же цитата, но испорченное продолжение (Ин 1:1)

> ἐν ἀρχῇ ἦν ὁ λόγος καὶ ὁ λόγος ἦν πρὸς τὴν ἀρχήν

### Эталон 3. Верная цитата, но ссылка стоит чужая (Мф 5:3)

> λαλοῦντες ἑαυτοῖς ψαλμοῖς καὶ ὕμνοις καὶ ᾠδαῖς πνευματικαῖς

### Эталон 4. Выдуманные греческие слова (Ин 1:1)

> σιγματαυ υψιλον φιχι ψιωμεγα σαμπι κοππα

### Эталон 5. Верная русская цитата (Мф 5:3)

«Блаженны нищие духом, ибо их есть Царство Небесное»

### Эталон 6. Русская цитата с подменой слова (Мф 5:3)

«Блаженны нищие сердцем, ибо их есть Царство Небесное»

### Эталон 7. Верная еврейская цитата (Быт 1:1)

> בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם

### Эталон 8. Еврейская цитата с перестановкой (Быт 1:1)

> בְּרֵאשִׁית בָּרָא הַשָּׁמַיִם אֱלֹהִים אֵת
"""


def selftest_checker(corpus, tmpdir):
    """Проверка самого проверяльщика на эталонах.

    Мало уметь подтверждать верное: инструмент обязан **не подтверждать** неверное.
    Восемь эталонов; для каждого записано, какой статус допустим, а какой означает,
    что инструмент сломан. Номера строк не вбиты: они берутся из самого файла-образца.
    """
    path = os.path.join(tmpdir, 'CALIBRATION_SAMPLE.md')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(CALIBRATION_FILE)
    parts = [path]

    statuses = {}
    for r in check_greek(parts, corpus):
        statuses[('греч.', r.line)] = r.status
    for r in check_russian(parts, corpus):
        statuses[('русск.', r.line)] = r.status
    for r in check_hebrew(parts, corpus):
        statuses[('евр.', r.line)] = r.status

    _, units = read_units(path)
    order = {'греч.': [], 'русск.': [], 'евр.': []}
    for start, kind, text in units:
        if re.search(r'[\u0370-\u03ff\u1f00-\u1fff]', text):
            order['греч.'].append(start)
        elif re.search(r'[\u0590-\u05ff]', text):
            order['евр.'].append(start)
        elif kind == 'русская':
            order['русск.'].append(start)

    cases = [
        ('греч.',  0, 'верная цитата, верная ссылка',      ('точно',)),
        ('греч.',  1, 'испорченное продолжение',            ('расхождение', 'не найдено')),
        ('греч.',  2, 'верная, ссылка чужой книги',         ('найдено в другом месте',)),
        ('греч.',  3, 'выдуманные слова',                   ('не найдено',)),
        ('русск.', 0, 'верная русская цитата',              ('точно',)),
        ('русск.', 1, 'подмена слова',                      ('расхождение', 'не найдено')),
        ('евр.',   0, 'верная еврейская цитата',            ('точно',)),
        ('евр.',   1, 'перестановка слов',                  ('не найдено',)),
    ]
    print('\nПроверка самого проверяльщика (восемь эталонов)')
    failed = 0
    for kind, n, what, allowed in cases:
        lines = order[kind]
        if n >= len(lines):
            print('  ОШИБКА %-6s %-26s -> эталон не попал в разбор' % (kind, what))
            failed += 1
            continue
        line = lines[n]
        status = statuses.get((kind, line), 'нет в отчёте')
        ok = status in allowed
        print('  %s %-6s строка %-3d %-28s -> %s' % (
            'ok  ' if ok else 'ОШИБКА', kind, line, what, status))
        failed += 0 if ok else 1
    os.remove(path)
    return failed



def selftest(corpus):
    print('Калибровка корпусов (%s)\n' % corpus.root)
    failed = 0
    for source, ref, expected in CALIBRATION:
        m = re.match(r'(.+?)\s+(\d+):(\d+)$', ref)
        abbr, ch, vs = m.group(1), int(m.group(2)), int(m.group(3))
        if source == 'nt':
            book = NT[abbr]
        elif source == 'tr':
            book = NT[abbr]
        elif source == 'lxx':
            book = OT_LXX[abbr]
        else:
            book = abbr
        if not corpus.has(source):
            print('  --  %-14s %-14s корпус недоступен' % (source, ref))
            continue
        verses = corpus.chapter(source, book, ch)
        flat = [w for v, ws in verses for w in ws]
        words = [w for v, ws in verses if v == vs for w in ws]
        ok = all(e in words for e in expected)
        if not ok and not words:
            ok = all(e in flat for e in expected)
        print('  %s  %-6s %-14s %s' % ('ok  ' if ok else 'ОШИБКА', source, ref,
                                       ' '.join(words)[:76]))
        failed += 0 if ok else 1
    print('\n%s' % ('Калибровка корпусов пройдена.' if not failed
                    else 'ОШИБОК: %d — отчёт недостоверен, сначала починить корпуса.' % failed))
    if failed:
        return failed
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        failed = selftest_checker(corpus, tmpdir)
    print('\n%s' % ('Самопроверка пройдена.' if not failed
                    else 'ОШИБОК: %d — инструмент подтверждает то, чего нет, или не находит того,'
                         ' что есть.' % failed))
    return failed


# =====================================================================
# 8. ОТЧЁТ
# =====================================================================

def report(results, title, verbose=False):
    print('\n%s' % title)
    print('-' * len(title))
    counts = {}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1
    for status in sorted(counts):
        print('  %-14s %d' % (status, counts[status]))
    print('  %-14s %d' % ('всего', len(results)))
    for status in sorted(counts):
        if status == 'точно' and not verbose:
            continue
        group = [r for r in results if r.status == status]
        # пометка имеет смысл только для русских цитат (marked is None — не применимо)
        unmarked = [r for r in group if r.marked is not None and not r.marked]
        print('\n### %s (%d)' % (status, len(group)), end='')
        if status != 'точно':
            print(', из них русских без пометки %d' % len(unmarked), end='')
        print()
        for r in sorted(group, key=lambda x: bool(x.marked)):
            print('  %s:%d [%s] ссылка %s' % (r.file[:34], r.line, r.kind, r.ref))
            print('      цитата : %s' % r.quote)
            if r.where:
                print('      место  : %s' % r.where)
            if r.source and status != 'точно':
                print('      корпус : %s' % r.source)
            if r.marked is not None:      # пометка имеет смысл только для русских цитат
                print('      пометка: %s' % (r.marked or 'НЕТ — проверить вручную'))
    return counts


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('what', choices=['selftest', 'greek', 'russian', 'hebrew', 'all'])
    ap.add_argument('--corpus', default='/tmp/bible')
    ap.add_argument('--parts', default=os.path.join(os.path.dirname(__file__), '..', 'SING-*.md'))
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--report')
    args = ap.parse_args()

    corpus = Corpus(args.corpus)
    parts = sorted(glob.glob(os.path.abspath(args.parts)))
    if not parts:
        sys.exit('не найдены файлы серии: %s' % args.parts)

    if args.what == 'selftest':
        sys.exit(1 if selftest(corpus) else 0)

    out = []
    if args.what in ('greek', 'all'):
        out.append(('ГРЕЧЕСКИЕ ЦИТАТЫ (SBLGNT / LXX / TR)',
                    check_greek(parts, corpus, verbose=args.verbose)))
    if args.what in ('russian', 'all'):
        out.append(('РУССКИЕ ЦИТАТЫ (Синодальный)', check_russian(parts, corpus)))
    if args.what in ('hebrew', 'all'):
        out.append(('ЕВРЕЙСКИЕ ЦИТАТЫ (Ленинградский кодекс)', check_hebrew(parts, corpus)))

    for title, results in out:
        report(results, title, verbose=args.verbose)

    if args.report:
        with open(args.report, 'w', encoding='utf-8') as fh:
            for title, results in out:
                fh.write('\n## %s\n\n' % title)
                for r in results:
                    fh.write('| %s | %d | %s | %s | %s | %s |\n' % (
                        r.file[:34], r.line, r.ref, r.status, r.where, r.quote))
        print('\nотчёт записан: %s' % args.report)


if __name__ == '__main__':
    main()
