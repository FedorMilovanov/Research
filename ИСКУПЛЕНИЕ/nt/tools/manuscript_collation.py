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

import glob
import os
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

HOME = Path(os.environ.get("NT_CORPUS_HOME", Path.home() / "nt-corpus"))
DEFAULT_SBLGNT = "/home/user/nt-corpus/py-sblgnt-master/pysblgnt/sblgnt"

BOOKS = ["Мф", "Мк", "Лк", "Ин", "Деян", "Рим", "1 Кор", "2 Кор", "Гал", "Еф",
         "Флп", "Кол", "1 Фес", "2 Фес", "1 Тим", "2 Тим", "Тит", "Флм",
         "Евр", "Иак", "1 Пет", "2 Пет", "1 Ин", "2 Ин", "3 Ин", "Иуд", "Откр"]
NAME_BY_CODE = {f"{i:02d}": b for i, b in enumerate(BOOKS, start=1)}
# обратная карта: имя книги -> её код в нумерации S1 (01=Мф … 27=Откр).
# Отдельная карта нужна потому, что коды в файлах McCollum НЕ совпадают со
# стандартной нумерацией (B26 там — Откровение, а в S1 26 — Иуда).
S1_CODE = {v: k for k, v in NAME_BY_CODE.items()}

# Каждый файл описан отдельно: шаблон пути (tarball распаковывается в каталог
# с полным SHA, поэтому glob, а не фиксированное имя), формат id юнита и книга,
# которую файл покрывает. Книга помечена знаком вопроса там, где код в файле
# расходится со стандартной нумерацией, — это и проверяет --verify.
FILES = [
    ("S9", "ECM Марк (2025)", "comp-tc-mark-*/xml/ecm_mark.xml", "xmlid", "Мк"),
    ("S10a", "ECM Деяния (2023)", "sbl-2023-talk-*/xml/ecm_acts.xml", "ecmacts", "Деян"),
    ("S10b", "UBS Марк (2023)", "sbl-2023-talk-*/xml/ecm_mark.xml", "xmlid", "Мк"),
    ("S10c", "UBS Ефесянам (2023)", "sbl-2023-talk-*/xml/ubs_ephesians.xml", "xmlid", "Еф"),
    ("S10d", "UBS 1 Петра (2023)", "sbl-2023-talk-*/xml/ubs_1_peter.xml", "xmlid", "1 Пет"),
    ("S10e", "UBS Откровение (2023)", "sbl-2023-talk-*/xml/ubs_revelation.xml", "xmlid", "Откр"),
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
        hits = sorted(glob.glob(str(HOME / pattern)))
        if not hits:
            raise SystemExit(f"{sid}: файл не найден по шаблону {pattern}; "
                             f"запустите tools/fetch_nt_corpus.sh")
        self.path = Path(hits[0])
        self.raw = self.path.read_text(encoding="utf-8")
        self.units: list[Unit] = []
        self.wit_types: Counter[str] = Counter()
        self._witnesses()
        self._parse()

    # -- список свидетелей
    def _witnesses(self):
        # ВАЖНО: `\s+`, а не пробел. В этих файлах атрибуты переносятся на
        # новую строку, и `<witness n="` даёт 204 совпадения там, где
        # `<witness` — 284. Первая версия парсера теряла 80 свидетелей Марка
        # и 17 — Ефесян именно на этом.
        # Порядок атрибутов не фиксирован: часть свидетелей записана как
        # <witness type="version" n="L:V">. Шаблон «сначала n=» терял 80 из
        # 284 свидетелей Марка. Разбор идёт по всему открывающему тегу.
        for mtag in re.finditer(r'<witness\b([^>]*?)/?>', self.raw):
            attrs = dict(re.findall(r'([\w:.-]+)="([^"]*)"', mtag.group(1)))
            if "n" not in attrs:
                continue
            self.wit_types[attrs.get("type") or "—"] += 1
        self.n_wit = sum(self.wit_types.values())

    # -- юниты
    def _parse(self):
        if self.style == "xmlid":
            rx = re.compile(r'<app\s+xml:id="(B\d+K(\d+)V(\d+)U[^"]*)"[^>]*>(.*?)</app>', re.S)
        else:
            # Позиция бывает не только одиночной: из 9555 юнитов Деяний
            # 6708 записаны как /7, 2844 как /7-9, 2 как /7-9/11 и 1 как
            # /7-9:11/13. Шаблон «только цифры» молча терял 2847 юнитов.
            rx = re.compile(r'<app\s+n="Acts (\d+):(\d+)/([^"]+)"[^>]*>(.*?)</app>', re.S)
        for m in rx.finditer(self.raw):
            if self.style == "xmlid":
                uid, ch, v, body = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
                pos = uid.split("U", 1)[1]
                # Книгу берём из объявления файла, а НЕ из кода в xml-id:
                # нумерация McCollum нестандартная (B26 у него — Откровение,
                # тогда как в 27-книжной нумерации 26 — Иуд), и маппинг по
                # таблице молча уводил все 70 юнитов Откровения в Иуду.
                # Правильность объявления проверяет --verify по тексту S1.
                book = self.book
            else:
                ch, v, pos, body = int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)
                uid, book = f"Деян {ch}:{v}/{pos}", self.book
            lemel = re.search(r"<lem\b[^>]*>(.*?)</lem>", body, re.S)
            lem = self._words(lemel.group(1)) if lemel else ""
            self.units.append(Unit(uid, book, ch, v, pos, lem, self._rdgs(body)))

    def _rdgs(self, body: str) -> list[tuple[str, str, list[str]]]:
        """Чтения юнита. Разбор идёт по открывающему тегу, а не по шаблону
        «n= потом wit=», потому что порядок атрибутов не гарантирован и тег
        бывает самоуничтожающимся (`<rdg ... />` = пропуск, пустое чтение)."""
        out = []
        for part in re.split(r"(?=<rdg\b)", body):
            if not part.startswith("<rdg"):
                continue
            mtag = re.match(r"<rdg\b([^>]*?)(/?)>", part, re.S)
            if not mtag:
                continue
            attrs = dict(re.findall(r'([\w:.-]+)="([^"]*)"', mtag.group(1)))
            content = "" if mtag.group(2) == "/" else part[mtag.end():].split("</rdg>")[0]
            out.append((attrs.get("n", ""), self._words(content),
                        (attrs.get("wit") or "").split()))
        return out

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
        print(f"    чтение {n}: n={len(wl):4d}  {text or '— (пропуск)'!r}")
        if keys:
            print(f"        ключевые свидетели: {', '.join(keys)}")
        if witnesses:
            print(f"        все: {' '.join(wl)}")


def main(argv: list[str]) -> int:
    s1root = Path(os.environ.get("NT_SBLGNT_DIR", DEFAULT_SBLGNT))
    s1 = load_s1(s1root) if s1root.is_dir() else {}
    colls = load_all()

    if "--scan" in argv or "--stats" in argv or not argv:
        print("КОЛЛЯЦИИ (S9, S10) — рукописный уровень")
        print(f"{'id':6} {'файл':26} {'юнитов':>7} {'стихов':>7} {'свидет.':>8}  книга")
        for c in colls:
            print(f"{c.sid:6} {c.label:26} {len(c.units):7d} {len(c.verses()):7d} "
                  f"{c.n_wit:8d}  {c.book} (код {c.book_code()})")
        print(f"\nвсего юнитов: {sum(len(c.units) for c in colls)}")

    if "--verify" in argv or not argv:
        print("\nПРОВЕРКА КОДА КНИГИ ПО ТЕКСТУ S1 (не по таблице)")
        if not s1:
            print("  S1 не найден — проверка пропущена")
        maxch = {}
        for (bc, ch, v) in s1:
            maxch[NAME_BY_CODE[bc]] = max(maxch.get(NAME_BY_CODE[bc], 0), ch)
        for c in colls:
            hits, top = c.verify_book(s1)
            lead = top[0] if top else ("—", 0)
            flag = "СОВПАЛО" if lead[0] == c.book else "РАСХОЖДЕНИЕ"
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
                    ws = set(bare(" ".join(u.words())).split())
                    hay = " ".join(ws)
                    # Основы прогоняются через тот же bare(): casefold()
                    # превращает конечную сигму ς в σ, поэтому «διαθηκης»
                    # из словаря никогда не совпадал с «διαθηκησ» из юнита и
                    # διαθήкая давала 0 вместо 2. Нормализация с обеих сторон.
                    st_norm = [bare(x) for x in stems]
                    hit = any(st in ws for st in st_norm) if mode == "word" \
                        else any(st in hay for st in st_norm)
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
