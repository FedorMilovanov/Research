#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Рукописный уровень: колляции ECM / UBS5 (свидетели S9 и S10).

Зачем этот скрипт существует
---------------------------
Аппарат S7 (SBLGNT-TEI) атрибутирует чтения **изданиям**: `#NA`, `#TR`, `#RP`,
`#WH`, `#Treg`. Рукописей в нём нет — ни א, ни B, ни P46. Поэтому LOCATOR_HOLD
после S7 остался открытым: «кто именно читает» было неизвестно.

S9 (`jjmccollum/comp-tc-mark`) и S10 (`jjmccollum/sbl-2023-talk`) дают ровно то,
чего не хватало: TEI-колляции **по рукописям**, собранные из аппарата Editio
Critica Maior (Деяния, Марк) и UBS5 (Марк, Ефесянам, 1 Петра, Откровение).
В них `wit="..."` — это сиглы Григория—Аланда: папирусы, унциалы, минускулы,
лекционарии, версии и отцы.

Что скрипт НЕ делает
-------------------
Не решает, какое чтение верное, и не снимает EVIDENCE_HOLD. Он отвечает только
на вопрос «какие рукописи что читают в данной позиции» и печатает числа.

Три вещи, которые скрипт проверяет сам, а не принимает на веру
-------------------------------------------------------------
1. Код книги. В файлах McCollum книга кодируется как `B02`, `B10`, `B21`,
   `B26`, и эта нумерация **не совпадает** со стандартной: `B26` здесь —
   Откровение, тогда как в 27-книжной нумерации B26 — Иуда. Поэтому код книги
   определяется не по таблице, а сверкой лемм юнитов с текстом S1
   (`--verify` печатает процент совпадений и лучшую альтернативу).
2. Порядок чтений. В колляции Деяний нет `<lem>`, то есть исходный текст
   (Ausgangstext) в файле не помечен. Приписывать чтению `a` статус исходного
   нельзя; скрипт вместо этого считает, как часто чтение `a` совпадает с S1.
3. Категории свидетелей. В `ecm_acts.xml` у каждого `<witness>` есть
   `type=` (papyrus / majuscule / minuscule / lectionary / version / father /
   corrector). Сводка по типам берётся из файла, а не из догадки о сигле.

Использование
-------------
  manuscript_collation.py --stats
  manuscript_collation.py --verify
  manuscript_collation.py --ref "Деян 20:28"
  manuscript_collation.py --ref "Откр 5:9" --witnesses
  manuscript_collation.py --scan
"""
from __future__ import annotations

import os
import re
import hashlib
import sys
sys.dont_write_bytecode = True
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from nt_sources import registry, witness_dir, witnesses

DEFAULT_SBLGNT = str(witness_dir("S1", verify=False))

BOOKS = ["Мф", "Мк", "Лк", "Ин", "Деян", "Рим", "1 Кор", "2 Кор", "Гал", "Еф",
         "Флп", "Кол", "1 Фес", "2 Фес", "1 Тим", "2 Тим", "Тит", "Флм",
         "Евр", "Иак", "1 Пет", "2 Пет", "1 Ин", "2 Ин", "3 Ин", "Иуд", "Откр"]
NAME_BY_CODE = {f"{i:02d}": b for i, b in enumerate(BOOKS, start=1)}
# обратная карта: имя книги -> её код в нумерации S1 (01=Мф … 27=Откр).
# Отдельная карта нужна потому, что коды в файлах McCollum НЕ совпадают со
# стандартной нумерацией (B26 там — Откровение, а в S1 26 — Иуда).
S1_CODE = {v: k for k, v in NAME_BY_CODE.items()}

# Каждый файл описан отдельно: имя внутри exact-pinned XML-каталога, формат
# id юнита и книга,
# которую файл покрывает. Книга помечена знаком вопроса там, где код в файле
# расходится со стандартной нумерацией, — это и проверяет --verify.
FILES = [
    ("S9", "ECM Марк (2025)", "ecm_mark.xml", "xmlid", "Мк"),
    ("S10a", "ECM Деяния (2023)", "ecm_acts.xml", "ecmacts", "Деян"),
    ("S10b", "UBS Марк (2023)", "ecm_mark.xml", "xmlid", "Мк"),
    ("S10c", "UBS Ефесянам (2023)", "ubs_ephesians.xml", "xmlid", "Еф"),
    ("S10d", "UBS 1 Петра (2023)", "ubs_1_peter.xml", "xmlid", "1 Пет"),
    ("S10e", "UBS Откровение (2023)", "ubs_revelation.xml", "xmlid", "Откр"),
]

# Лексика искупления для --scan. Даны основы без ударений: поиск идёт по
# тексту, приведённому к нижнему регистру и без диакритики, поэтому форма
# «περιεποιησατο» находится по основе «περιποι».
# Лексика искупления для --scan. Два режима, и это существенно:
#   stem — поиск основы внутри слова (λυτρ ловит λυτρωτης, λυτρον, απολυτρωσις);
#   word — только целое слово. Предлогам и квантификаторам нужен именно word:
#   при поиске подстроки «αντι» находится λυσαντι (Откр 1:5), а «περι» —
#   περιεσσω и περιεποιησατο. Первая версия скана на этом врала: 35 «ἀντί»
#   вместо реальных единиц.
LEXEMES = {
    "λυτρ-": ("stem", ["λυτρ"]),
    "αγοραζ- / εξαγοραζ-": ("stem", ["αγοραζ"]),
    "αἷμα (αἷμα/αἵματος/αἵματι)": ("stem", ["αιμα"]),
    "ἱλασκ- / ἱλασμός": ("stem", ["ιλασ"]),
    "καταλλαγ-": ("stem", ["καταλλα"]),
    "σφαζω / ἐσφαγμένον": ("stem", ["σφαζ", "εσφαγ"]),
    "περιποι-": ("stem", ["περιποι"]),
    "ὑπέρ (целое слово)": ("word", ["υπερ"]),
    "ἀντί (целое слово)": ("word", ["αντι"]),
    "περί (целое слово)": ("word", ["περι"]),
    "πολλοί/πολλῶν (целое слово)": ("word", ["πολλων", "πολλοι", "πολλους", "πολλαι",
                                              "πολλα", "πολλης", "πολλοις"]),
    "πᾶς/πάντες (целое слово)": ("word", ["παντας", "παντες", "παντων", "πας", "παν",
                                           "πασιν", "πασα", "πασαν"]),
    "κόσμος (целое слово)": ("word", ["κοσμος", "κοσμου", "κοσμω", "κοσμον"]),
    "ἐκκλησία (целое слово)": ("word", ["εκκλησια", "εκκλησιας", "εκκλησιαν", "εκκλησιαι"]),
    "ἴδιος (целое слово)": ("word", ["ιδιος", "ιδιου", "ιδιον", "ιδιαν", "ιδιων", "ιδιω"]),
    "ψυχή (целое слово)": ("word", ["ψυχην", "ψυχης", "ψυχη", "ψυχας"]),
    "διαθήκη (целое слово)": ("word", ["διαθηκης", "διαθηκην", "διαθηκη"]),
}

KEY_WITNESSES = ["A", "MT", "P45", "P74", "P84", "P88", "P137", "01", "02", "03", "04", "05", "08", "044"]


# S1 печатает сиглы аппарата прямо в тексте и приклеивает их к слову
# (⸀χριστου): 0x2E00 встречается 5114 раза, 0x2E02 — 1764, 0x2E03 — 1765.
# Без их снятия пословное сравнение с колляциями не работает вообще.
NOISE = re.compile(r"[\u2E00-\u2E0F\u27E6\u27E7\u2019\u2014\u00B7.,;:!?\-\u2010-\u2015\"'()\[\]{}]")


def bare(s: str) -> str:
    """Без диакритики и в нижнем регистре.

    casefold обязателен: заглавная в начале предложения — орфография, а не
    другая лексема. Без него терялись Ἐπικατάρατος и Ἔλθατε.
    """
    s = unicodedata.normalize("NFD", s.casefold())
    return "".join(c for c in s if not unicodedata.combining(c))


# ---------------------------------------------------------------- S1 (текст)

def clean_words(s: str) -> str:
    """Убирает вклеенные сиглы и пунктуацию, оставляя только словоформы."""
    return re.sub(r"\s+", " ", NOISE.sub(" ", s)).strip()


def load_s1(root: Path) -> dict[tuple[str, int, int], str]:
    """Стих -> текст S1 (без диакритики). Формат строки:
    `020101 N- ----NSF- N-NSF Ἀρχὴ Ἀρχὴ ἀρχή ἀρχή` — поле 4 это словоформа,
    поле 0 начинается с двузначного кода книги (02 = Мк).
    """
    out: dict[tuple[str, int, int], list[str]] = {}
    for path in sorted(root.glob("*-morphgnt.txt")):
        for line in path.read_text(encoding="utf-8").splitlines():
            p = line.split()
            if len(p) != 8 or len(p[0]) != 6 or not p[0].isdigit():
                continue
            key = (p[0][0:2], int(p[0][2:4]), int(p[0][4:6]))
            out.setdefault(key, []).append(p[4])
    return {k: bare(clean_words(" ".join(v))) for k, v in out.items()}


# --------------------------------------------------------------- колляции

class Unit:
    __slots__ = ("uid", "book", "ch", "v", "pos", "lem", "rdg")

    def __init__(self, uid, book, ch, v, pos, lem, rdg):
        self.uid, self.book, self.ch, self.v, self.pos = uid, book, ch, v, pos
        self.lem, self.rdg = lem, rdg  # rdg: list[(n, text, [wit...])]

    @property
    def ref(self) -> str:
        return f"{self.book} {self.ch}:{self.v}"

    def words(self) -> list[str]:
        w = self.lem.split()
        for _, t, _ in self.rdg:
            w += t.split()
        return w


class Collation:
    def __init__(self, sid: str, label: str, pattern: str, style: str, book: str):
        self.sid, self.label, self.style, self.book = sid, label, style, book
        source = "S9" if sid == "S9" else "S10"
        self.path = witness_dir(source) / pattern
        self.raw = self.path.read_text(encoding="utf-8")
        root = ET.fromstring(self.raw)
        for element in root.iter():
            if isinstance(element.tag, str) and element.tag.startswith("{"):
                element.tag = element.tag.split("}", 1)[1]
        self.units: list[Unit] = []
        self.wit_types: Counter[str] = Counter()
        sigla = set()
        for witness in root.iter("witness"):
            name = witness.get("n")
            if not name or name in sigla:
                raise ValueError(f"{sid}: missing/duplicate witness identifier: {name}")
            sigla.add(name)
            self.wit_types[witness.get("type") or "—"] += 1
        self.n_wit = len(sigla)
        xmlid = "{http://www.w3.org/XML/1998/namespace}id"
        unit_ids = set()
        self.unmapped_tokens = set()
        for app in root.iter("app"):
            uid = app.get(xmlid, "") if style == "xmlid" else app.get("n", "")
            rx = r"B\d+K(\d+)V(\d+)U(.+)" if style == "xmlid" else r"Acts (\d+):(\d+)/(.+)"
            match = re.fullmatch(rx, uid)
            if not match or uid in unit_ids:
                raise ValueError(f"{sid}: invalid/duplicate unit identifier: {uid}")
            unit_ids.add(uid)
            ch, verse, pos = int(match[1]), int(match[2]), match[3]
            lem = app.find("lem")
            lem_text = self._words(ET.tostring(lem, encoding="unicode")) if lem is not None else ""
            readings = []
            for reading in app.findall("rdg"):
                wit = (reading.get("wit") or "").replace("#", "").split()
                self.unmapped_tokens.update(set(wit) - sigla)
                readings.append((reading.get("n", ""), self._words(ET.tostring(reading, encoding="unicode")), wit))
            if not readings:
                raise ValueError(f"{sid}: variation unit without readings: {uid}")
            self.units.append(Unit(uid, book, ch, verse, pos, lem_text, readings))
        row = witnesses()[source]
        self.active_unit_count = len(self.units)
        self.active_verse_count = len(self.verses())
        receipt = row["unmappedReadingTokenReceipts"][Path(pattern).stem]
        digest = hashlib.sha256("\n".join(sorted(self.unmapped_tokens)).encode()).hexdigest()
        if len(self.unmapped_tokens) != receipt["count"] or digest != receipt["sha256OfSortedNewlineSeparatedTokens"]:
            raise ValueError(f"{sid}: unresolved reading-token receipt drift")
        expected = row["stats"] if source == "S9" else row["stats"][Path(pattern).stem]
        actual = (len(self.units), len(self.verses()), self.n_wit)
        wanted = tuple(expected[k] for k in ("variationUnits", "verses", "witnesses"))
        if actual != wanted:
            raise ValueError(f"{sid}: parsed cardinality mismatch: {actual} != {wanted}")
        quarantine = set(row.get("quarantinedUnits", {}).get(Path(pattern).stem, {}).get("ids", []))
        found = {u.uid for u in self.units if u.uid in quarantine}
        if found != quarantine:
            raise ValueError(f"{sid}: quarantined unit receipt drift")
        self.quarantined_units = [u for u in self.units if u.uid in quarantine]
        self.units = [u for u in self.units if u.uid not in quarantine]
        if len(self.units) != expected.get("eligibleUnits", expected["variationUnits"]) or len(self.verses()) != expected.get("eligibleVerses", expected["verses"]):
            raise ValueError(f"{sid}: eligible unit/verse cardinality mismatch")

    @staticmethod
    def _words(xml: str) -> str:
        xml = re.sub(r"</?w>", " ", xml)
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", xml)).strip()

    # -- выборки
    def verses(self) -> set[tuple[int, int]]:
        return {(u.ch, u.v) for u in self.units}

    def at(self, book: str, ch: int, v: int) -> list[Unit]:
        return [u for u in self.units if u.book == book and u.ch == ch and u.v == v]

    def rdg_a_matches_s1(self, s1: dict, limit: int = 400) -> tuple[int, int]:
        """Как часто чтение `a` совпадает с текстом S1. Это проверка порядка
        чтений, а не утверждение о том, что `a` и есть Ausgangstext.

        Стих берётся по ИМЕНИ книги, а не по коду из файла: код B26 в S10e —
        это Откровение, тогда как в нумерации S1 26 — Иуда. Первая версия
        брала код из файла и потому давала по Откровению 0/70."""
        code = S1_CODE.get(self.book, "")
        hit = tot = 0
        for u in self.units[:limit]:
            if not u.rdg:
                continue
            text = bare(u.rdg[0][1])
            if not text:
                continue
            verse = s1.get((code, u.ch, u.v), "")
            tot += 1
            if text in verse:
                hit += 1
        return hit, tot

    def book_code(self) -> str:
        for u in self.units[:1]:
            if u.uid.startswith("B"):
                return u.uid[1:3]
        return S1_CODE.get(self.book, "")

    def max_chapter(self) -> int:
        return max((u.ch for u in self.units), default=0)

    def verify_book(self, s1: dict, limit: int = 120) -> tuple[int, list]:
        """Определяет книгу по тексту, а не по таблице кодов.

        Метод: у каждого юнита берутся все словоформы (lem + все чтения)
        длиной ≥ 6 знаков — короткие (του, και, εν) есть в любом стихе и
        ничего не различают — и считается, сколько из них встречается в стихе
        S1 у каждой из 27 книг. Заявленная книга обязана выиграть; если
        выигрывает другая, код книги в файле означает не то, что мы думаем.
        """
        score: Counter[str] = Counter()
        for u in self.units[:limit]:
            blob = u.lem + " " + " ".join(t for _, t, _ in u.rdg)
            words = {bare(w) for w in blob.split() if len(bare(w)) >= 6}
            if not words:
                continue
            for bc, bname in NAME_BY_CODE.items():
                verse = s1.get((bc, u.ch, u.v), "")
                if not verse:
                    continue
                score[bname] += len(words & set(verse.split()))
        return score.get(self.book, 0), score.most_common(3)


def load_all() -> list[Collation]:
    return [Collation(*spec) for spec in FILES]


def parse_ref(s: str) -> tuple[str, int, int]:
    m = re.match(r"^\s*([123]?\s?[А-Яа-яЁё]+\.?)\s+(\d+):(\d+)\s*$", s)
    if not m:
        raise SystemExit(f"не разобрал ссылку {s!r}; формат: «Деян 20:28»")
    book = m.group(1).replace(".", "").replace(" ", "")
    for b in BOOKS:
        if b.replace(" ", "") == book:
            return b, int(m.group(2)), int(m.group(3))
    raise SystemExit(f"неизвестная книга {book!r}")


def show(coll: Collation, u: Unit, witnesses: bool) -> None:
    print(f"\n  {coll.sid} {u.uid}")
    if u.lem:
        print(f"    lem: {u.lem}")
    for n, text, wl in u.rdg:
        keys = [k for k in KEY_WITNESSES if k in wl]
        print(f"    чтение {n}: literal-siglum-tokens={len(wl):4d}  {text or '— (пропуск)'!r}")
        if keys:
            print(f"        ключевые свидетели: {', '.join(keys)}")
        if witnesses:
            print(f"        все: {' '.join(wl)}")


def unit_matches(unit: Unit, mode: str, patterns: list[str]) -> bool:
    words = set(bare(" ".join(unit.words())).split())
    needles = [bare(x) for x in patterns]
    if mode == "word":
        return any(needle in words for needle in needles)
    if mode == "stem":
        return any(needle in word for needle in needles for word in words)
    raise ValueError(f"unsupported probe mode: {mode}")


def probe_counts(colls: list[Collation]) -> dict[str, int]:
    return {label: sum(unit_matches(u, mode, patterns) for c in colls for u in c.units)
            for label, (mode, patterns) in LEXEMES.items()}


def main(argv: list[str]) -> int:
    allowed = {"--stats", "--verify", "--scan", "--ref", "--witnesses", "--check"}
    for i, arg in enumerate(argv):
        if i > 0 and argv[i - 1] == "--ref":
            continue
        if arg not in allowed:
            raise ValueError(f"unknown manuscript argument: {arg}")
    if "--ref" in argv and argv.index("--ref") == len(argv) - 1:
        raise ValueError("--ref requires a reference")
    s1root = witness_dir("S1")
    s1 = load_s1(s1root)
    failures = []
    colls = load_all()

    if "--scan" in argv or "--stats" in argv or not argv:
        print("КОЛЛЯЦИИ (S9, S10) — рукописный уровень")
        print(f"{'id':6} {'файл':26} {'юнитов':>7} {'стихов':>7} {'свидет.':>8}  книга")
        for c in colls:
            print(f"{c.sid:6} {c.label:26} {c.active_unit_count:7d} {c.active_verse_count:7d} "
                  f"{c.n_wit:8d}  {c.book} (код {c.book_code()}); unmapped tokens={len(c.unmapped_tokens)}; quarantined={len(c.quarantined_units)}")
        print(f"\nстрок юнитов по шести файлам: {sum(c.active_unit_count for c in colls)} (Марк включён дважды; одна строка в quarantine)")
        print(f"без более раннего марковского S10b: {sum(len(c.units) for c in colls if c.sid != 'S10b')}")

    if "--verify" in argv or "--check" in argv or not argv:
        print("\nПРОВЕРКА КОДА КНИГИ ПО ТЕКСТУ S1 (не по таблице)")
        if not s1:
            raise ValueError("S1 not found: manuscript verification cannot be skipped")
        maxch = {}
        for (bc, ch, v) in s1:
            maxch[NAME_BY_CODE[bc]] = max(maxch.get(NAME_BY_CODE[bc], 0), ch)
        for c in colls:
            hits, top = c.verify_book(s1)
            lead = top[0] if top else ("—", 0)
            matched = lead[0] == c.book and lead[1] > 0 and (len(top) < 2 or lead[1] > top[1][1])
            flag = "СОВПАЛО" if matched else "РАСХОЖДЕНИЕ"
            if not matched or c.max_chapter() > maxch.get(c.book, 0):
                failures.append(f"{c.sid}: book identity/structure mismatch")
            struct = f"глав в файле {c.max_chapter()} / в S1 у «{c.book}» {maxch.get(c.book)}"
            print(f"  {c.sid:6} код в файле {c.book_code()} -> заявлено {c.book:6} "
                  f"| по тексту лидирует {lead[0]} ({lead[1]}) [{flag}] | {struct}")
            print(f"         топ-3: " + ", ".join(f"{n} {k}" for n, k in top))
        print("\nПОРЯДОК ЧТЕНИЙ: как часто чтение `a` совпадает с S1")
        for c in colls:
            h, t = c.rdg_a_matches_s1(s1)
            print(f"  {c.sid:6} {h:4d}/{t:4d}")

    if "--stats" in argv:
        print("\nСВИДЕТЕЛИ ПО ТИПАМ (тип берётся из атрибута type= самого файла)")
        for c in colls:
            kinds = ", ".join(f"{k} {v}" for k, v in c.wit_types.most_common())
            print(f"  {c.sid:6} {kinds}")

    if "--scan" in argv:
        print("\nПОИСК ЛЕКСИКИ ИСКУПЛЕНИЯ ВО ВСЕХ АППАРАТАХ (основы, без диакритики)")
        for name, (mode, stems) in LEXEMES.items():
            per: dict[str, list[str]] = {}
            for c in colls:
                found = []
                for u in c.units:
                    hit = unit_matches(u, mode, stems)
                    if hit:
                        found.append(u.uid)
                if found:
                    per[c.sid] = found
            tot = sum(len(v) for v in per.values())
            det = "  ".join(f"{k}:{len(v)}" for k, v in per.items())
            print(f"  {name:26} юнитов: {tot:3d}   {det}")
            for k, v in per.items():
                if len(v) <= 6:
                    print(f"        {k}: {', '.join(v)}")

    if "--profile" in argv:
        print("\nПОВЕДЕНИЕ СИГЛ: как часто сигла стоит на чтении, совпадающем с S1")
        print("Имена кодексов в файлах НЕ даны (только type= и <origDate>), поэтому это")
        print("проверка поведения сиглы, а не её отождествление с именованным кодексом.")
        for c in colls:
            code = S1_CODE.get(c.book, "")
            agree: Counter[str] = Counter()
            total: Counter[str] = Counter()
            usable = 0
            for u in c.units:
                verse = s1.get((code, u.ch, u.v), "")
                if not verse:
                    continue
                good = set()
                for _, t, w in u.rdg:
                    if t and bare(t) in verse:
                        good |= set(w)
                if not good:
                    continue
                usable += 1
                for _, _, w in u.rdg:
                    for sig in w:
                        total[sig] += 1
                        if sig in good:
                            agree[sig] += 1
            print(f"  {c.sid:6} {c.book}: юнитов, где хоть одно чтение совпало с S1 — {usable}")
            rows = [(g, agree[g], total[g]) for g in KEY_WITNESSES if total[g]]
            for sig, a, t in sorted(rows, key=lambda r: -(r[1] / r[2])):
                print(f"        {sig:6} {a:4d}/{t:4d} = {100 * a / t:5.1f} %")

    if "--ref" in argv:
        ref = argv[argv.index("--ref") + 1]
        book, ch, v = parse_ref(ref)
        print(f"\n{book} {ch}:{v}")
        any_hit = False
        for c in colls:
            if c.book != book:
                continue
            units = c.at(book, ch, v)
            if not units:
                print(f"  {c.sid} {c.label}: юнитов НЕТ")
                continue
            any_hit = True
            print(f"  {c.sid} {c.label}: юнитов {len(units)}")
            for u in units:
                show(c, u, "--witnesses" in argv)
        if not any_hit:
            print("  ни одна колляция S9/S10 эту книгу не покрывает")
    if "--check" in argv:
        expected = registry()["manuscriptCollation"]
        counts = (sum(c.active_unit_count for c in colls), sum(len(c.units) for c in colls),
                  sum(len(c.units) for c in colls if c.sid != "S10b"))
        wanted = tuple(expected[k] for k in ("totalVariationUnits", "eligibleFileUnitRows", "preferredNonOverlappingFileUnitRows"))
        if counts != wanted or probe_counts(colls) != expected["verifiedProbeCounts"]:
            failures.append("manuscript active/eligible census or lexical probes differ from SSOT")
    if failures:
        print("FAIL: " + "; ".join(failures))
        return 1
    if "--check" in argv:
        print("PASS: manuscript census, eligible book identities and declared lexical probes match SSOT")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (KeyError, OSError, ValueError, ET.ParseError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
