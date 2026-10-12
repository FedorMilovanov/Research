#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Парная сверка MT (S6, BHS) ↔ LXX (S5, Swete 1901) по связям под-корпуса.

Зачем
-----
До S6 файл 11_NT_LXX_COLLATION.md строился только на греческой стороне:
«LXX передаёт כַּפֹּרֶת как ἱλαστήριон» было выводом из соответствия, а не
проверкой, и стояло под MT_HOLD. Здесь каждое такое утверждение исполняется
по обоим текстам сразу.

Что инструмент НЕ делает
------------------------
Он не выравнивает слова и не решает, какой еврейский корень «на самом деле»
стоит за греческим словом. Он печатает оба текста рядом, а решение остаётся
в карточке и помечается как цитата / аллюзия / натяжка.

Использование:
  python3 ИСКУПЛЕНИЕ/nt/tools/mt_lxx_collation.py           # вся таблица
  python3 ИСКУПЛЕНИЕ/nt/tools/mt_lxx_collation.py --count   # только счётчики
Переменные: NT_MT_DIR, NT_LXX_DIR.
"""
from __future__ import annotations

import os
import re
import sys
import unicodedata
from pathlib import Path


def bare(w: str) -> str:
    """Слово без ударений, придыханий и пунктуации.

    Обязателен: ἱλαστήριον (именительный, η с ударением) и ἱλαστηρίου
    (родительный, η без ударения) — РАЗНЫЕ строки. Поиск по префиксу
    «ἱλαστηρ» с η без удара находит только родительный падеж и молча
    теряет 14 из 28 вхождений. Так и получилось в первом прогоне: 14 вместо 28.
    """
    w = unicodedata.normalize("NFD", w.strip("·,.:;\'\u0313\u0314"))
    w = "".join(c for c in w if not unicodedata.combining(c))
    # Регистр обязателен: Ἐπικατάρατος (Втор 27:26) и Ἔλθατε (Притч 9:5)
    # начинаются с заглавной, и без casefold префиксный поиск их теряет.
    return w.replace("ς", "σ").casefold()

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mt_lookup  # noqa: E402
from mt_lookup import MT  # noqa: E402

HOME = Path(os.environ.get("NT_CORPUS_HOME", Path.home() / "nt-corpus"))
MT_DIR = mt_lookup.DEFAULT  # glob по bhsa-min-<sha>/tf/2021
def _lxx_root() -> Path:
    # Path("") истинно, поэтому `Path(env) or ...` молча вернул бы '.', а
    # пустой каталог выглядел бы как «в LXX ноль вхождений». Только явная
    # непустая строка окружения.
    env = os.environ.get("NT_LXX_DIR", "")
    if env:
        return Path(env)
    hits = sorted(HOME.glob("lxx-swete-*/data"))
    return hits[0] if hits else HOME / "lxx-swete" / "data"


LXX_ROOT = _lxx_root()


class LXX:
    """Swete 1901 через First1KGreek: `книга.глава.стих слово` по строке."""

    def __init__(self, root: Path):
        if not root.is_dir():
            raise SystemExit(f"LXX не найден в {root}; задайте NT_LXX_DIR")
        self.root = root
        self.verses: dict[str, list[str]] = {}
        for path in sorted(root.glob("*.txt")):
            m = re.match(r"(\d+)\.(.+)\.txt$", path.name)
            if not m:
                continue
            book = m.group(2)
            for line in path.read_text(encoding="utf-8").splitlines():
                parts = line.split(" ", 1)
                if len(parts) != 2 or parts[0].count(".") != 2:
                    continue
                _, ch, vs = parts[0].split(".")
                self.verses.setdefault(f"{book} {ch}:{vs}", []).append(parts[1])

    def text(self, ref: str) -> str:
        w = self.verses.get(ref)
        return " ".join(w) if w else "НЕТ ТАКОГО СТИХА"

    def has(self, ref: str, word_prefix: str) -> bool:
        """Префиксное сравнение ПОСЛЕ нормализации (см. bare)."""
        pre = bare(word_prefix)
        return any(bare(x).startswith(pre) for x in self.verses.get(ref, []))

    def count_word(self, word: str) -> int:
        """Все словоформы основы, а не одна флекcия (см. bare)."""
        pre = bare(word)
        return sum(1 for ws in self.verses.values() for x in ws
                   if bare(x).startswith(pre))

    def verses_with(self, word: str) -> list[tuple[str, int]]:
        pre = bare(word)
        out = [(r, sum(1 for x in ws if bare(x).startswith(pre)))
               for r, ws in self.verses.items()
               if any(bare(x).startswith(pre) for x in ws)]
        return sorted(out)


# (MT-ссылка, LXX-ссылка, связь в 11_, греческое слово, еврейская лексема)
# Еврейская лексема — та, которую, по утверждению карточки, передаёт греческое
# слово. Инструмент проверяет присутствие обоих, но НЕ выравнивает слова.
LINKS: list[tuple[str, str, str, str, str]] = [
    # (MT-ссылка, LXX-ссылка, связь, греческое слово, еврейская лексема)
    # LXX-ссылки — ПО НУМЕРАЦИИ LXX, которая в Исходе местами расходится с MT:
    # в Исх 25 LXX идёт на единицу ниже MT (проверено на 8 стихах подряд,
    # 25:16–23 LXX = 25:17–24 MT), а исполнение в Исх 37 у MT соответствует
    # Исх 38 у LXX. Поэтому ссылки проставлены раздельно, а не одной строкой.

    # --- ἱλαστήριον ↔ כַּפֹּרֶת: MT 22 стиха, LXX 21 стих (28 форм) ---
    ("Exodus 25:17", "Exodus 25:16", "כַּפֹּרֶת → ἱλαστήριον (сдвиг -1)", "ἱλαστηρ", "כפרת"),
    ("Exodus 25:18", "Exodus 25:17", "כַּפֹּרֶת → ἱλαστήριον", "ἱλαστηρ", "כפרת"),
    ("Exodus 25:19", "Exodus 25:18", "כַּפֹּרֶת → ἱλαστήριον", "ἱλαστηρ", "כפרת"),
    ("Exodus 25:20", "Exodus 25:19", "כַּפֹּרֶת → ἱλαστήριον", "ἱλαστηρ", "כפרת"),
    ("Exodus 25:21", "Exodus 25:20", "כַּפֹּרֶת → ἱλαστήριον", "ἱλαστηρ", "כפרת"),
    ("Exodus 25:22", "Exodus 25:21", "כַּפֹּרֶת → ἱλαστήριον", "ἱλαστηρ", "כפרת"),
    ("Exodus 26:34", "Exodus 26:34", "MT כַּפֹּרֶת; LXX ἱλαστήριον?", "ἱλαστηρ", "כפרת"),
    ("Exodus 30:6", "Exodus 30:6", "MT כַּפֹּרֶת; LXX ἱλαστήριон?", "ἱλαστηρ", "כפרת"),
    ("Exodus 31:7", "Exodus 31:7", "כַּפֹּרֶת → ἱλαστήριον", "ἱλαστηρ", "כפרת"),
    ("Exodus 35:12", "Exodus 35:11", "כַּפֹּרֶת → ἱλαστήριον (сдвиг -1)", "ἱλαστηρ", "כפרת"),
    ("Exodus 37:6", "Exodus 38:5", "כַּפֹּרֶת → ἱλαστήριον (МТ 37 = LXX 38)", "ἱλαστηρ", "כפרת"),
    ("Exodus 37:7", "Exodus 38:6", "כַּפֹּרֶת → LXX сокращает", "ἱλαστηρ", "כפרת"),
    ("Exodus 37:8", "Exodus 38:7", "כַּפֹּרֶת → ἱλαστήριον", "ἱλαστηρ", "כפרת"),
    ("Exodus 37:9", "Exodus 38:8", "כַּפֹּרֶת → ἱλαστήριον", "ἱλαστηρ", "כפרת"),
    ("Exodus 39:35", "Exodus 39:35", "MT есть; стиха нет в LXX (сокращение)", "ἱλαστηρ", "כפרת"),
    ("Exodus 40:20", "Exodus 40:20", "MT כַּפֹּרֶת; LXX ἱλαστήριον?", "ἱλαστηρ", "כפרת"),
    ("Leviticus 16:2", "Leviticus 16:2", "כַּפֹּרֶת → ἱλαστήριον ×2", "ἱλαστηρ", "כפרת"),
    ("Leviticus 16:13", "Leviticus 16:13", "כַּפֹּרֶת → ἱλαστήριον", "ἱλαστηρ", "כפרת"),
    ("Leviticus 16:14", "Leviticus 16:14", "כַּפֹּרֶת → ἱλαστήριον ×2", "ἱλαστηρ", "כפרת"),
    ("Leviticus 16:15", "Leviticus 16:15", "כַּפֹּרֶת → ἱλαστήριον ×2", "ἱλαστηρ", "כפרת"),
    ("Numbers 7:89", "Numeri 7:89", "כַּפֹּרֶת → ἱλαστήριον", "ἱλαστηρ", "כפרת"),
    ("1_Chronicles 28:11", "Paralipomenon_I 28:11",
     "כַּפֹּרֶת → οἶκος τοῦ ἐξιλασμοῦ, НЕ ἱλαστήριον", "ἐξιλασμ", "כפרת"),

    # --- LXX даёт ἱλαστήριον там, где в MT כַּפֹּרֶת нет ---
    ("Amos 9:1", "Amos 9:1", "LXX ἱλαστήριον ← MT כַּפְתּוֹר (не כפרת!)",
     "ἱλαστηρ", "כפתור"),
    ("Ezekiel 43:14", "Ezechiel 43:14", "LXX ἱλαστήριон ×3 ← MT אראיל",
     "ἱλαστηρ", "—"),
    ("Ezekiel 43:17", "Ezechiel 43:17", "LXX ἱλαστήριον ← MT עזרה",
     "ἱλαστηρ", "—"),
    ("Ezekiel 43:20", "Ezechiel 43:20", "LXX ἱλαστήριον ← MT без כפרת",
     "ἱλαστηρ", "—"),

    # --- λύτρον / λύτρωσις: MT גאל и פדה, а не כפר ---
    ("Exodus 21:30", "Exodus 21:30", "λύτρα ×2 ← כֹּפֶר + פִּדְיֹן נַפְשׁוֹ",
     "λυτρ", "כפר"),
    ("Psalms 111:9", "Psalmi 110:9", "λύτρωσιν ἀπέστειλεν ← пдyт (LXX -1)",
     "λυτρ", "פדות"),
    ("Psalms 49:8", "Psalmi 48:8", "ἐξίλασμα + λύτρωσις ψυχῆς",
     "λυτρ", "כפר"),
    ("Psalms 49:9", "Psalmi 48:9", "τιμὴν λυτρώσεως ψυχῆς ← יקר + פדיון נפש", "τιμη", "פדיון"),
    ("Isaiah 43:3", "Isaias 43:3", "ἄλλαγμα ← כָּפְרְךָ, НЕ λύτρον", "αλλαγμα", "כפר"),
    ("Isaiah 43:4", "Isaias 43:4", "ἀνθρώπους πολλοὺς ὑπὲρ σοῦ ← אדם תחתיך", "ὑπερ", "תחת"),
    ("Isaiah 52:3", "Isaias 52:3", "λυτρωθήσεσθε ← גאל, без כסף", "λυτρ", "גאל"),
    ("Leviticus 25:25", "Leviticus 25:25", "גאל в LXX — не λυτρ-?", "λυτρ", "גאל"),
    ("Ruth 4:4", "Ruth 4:4", "גאל — родственный выкуп", "λυτρ", "גאל"),
    ("Proverbs 6:35", "Proverbia 6:35", "λύτρα = выкуп за вину", "λυτρ", "כפר"),

    # --- πολλοί ↔ רבים (Ис 53) ---
    ("Isaiah 53:11", "Isaias 53:11", "πολλοί ← רַבִּים", "πολλ", "רב"),
    ("Isaiah 53:12", "Isaias 53:12", "πολλοί ← רַבִּים (2 раза)", "πολλ", "רב"),
    ("Isaiah 52:14", "Isaias 52:14", "контекст Ис 53", "πολλ", "—"),
    ("Isaiah 52:15", "Isaias 52:15", "многие народы", "πολλ", "גוי"),

    # --- ось предложения ---
    ("Isaiah 55:1", "Isaias 55:1", "ἄνευ ἀργυρίου ← לוא־כסף ומחיר",
     "αργυρι", "כסף"),
    ("Proverbs 9:5", "Proverbia 9:5", "Ἐλθατε ← לְכוּ (лексема הלך)", "ελθατ", "הלך"),
    ("Deuteronomy 32:11", "Deuteronomium 32:11", "πτέρυγας ← MT אֶבְרָה (Мф 23:37)",
     "πτερυγ", "אברה"),
    ("Isaiah 25:6", "Isaias 25:6", "πᾶσι τοῖς ἔθνεσιν ← לְכָל־הָעַמִּים (Мф 22)",
     "εθν", "עם"),
    ("Isaiah 49:6", "Isaias 49:6", "цитата в Деян 13:47", "εθνων", "גוי"),
    ("Zechariah 14:8", "Zacharias 14:8", "ὕδωρ ζῶν ← מים חיים (Ин 7:37)",
     "ζων", "חי"),
    ("Deuteronomy 27:26", "Deuteronomium 27:26", "цитата в Гал 3:10, С РАСХОЖД.",
     "επικαταρατο", "ארר"),
    ("Exodus 12:5", "Exodus 12:5", "τέλειον ← תָּמִים (1 Пет 1:19 ἄμωμος)",
     "τελειον", "תמים"),
]


def main(argv: list[str]) -> int:
    mt = MT(MT_DIR)
    lxx = LXX(LXX_ROOT)
    if "--count" in argv:
        print("=== MT: точные лексемы BHSA ===")
        for lx in ["כפרת", "כפר", "גאל", "פדה", "פדות", "רב", "כסף",
                   "תמים", "מחיר", "כפתור"]:
            print(f"  {lx:8s}: {mt.count_lexeme(lx)}")
        print()
        print("=== LXX: счёт ПО ОСНОВЕ (bare-нормализация), не по одной флексии")
        print("    префикс          словоформ  стихов")
        for stem, label in [("ιλαστηρ", "ἱλαστηρ- (ἱλαστήριον)"),
                            ("ιλασμ", "ἱλασμ- (ἱλασμός)"),
                            ("λυτρ", "λυτρ- (λύτρον/λύτρωσις)"),
                            ("πολλ", "πολλ- (πολλοί)"),
                            ("αλλαγμα", "ἄλλαγμα")]:
            vs = lxx.verses_with(stem)
            n = sum(k for _, k in vs)
            print(f"    {label:20s} {n:6d}   {len(vs):5d}")
            for ref, k in vs:
                print(f"        {ref:24s} ×{k}")
        return 0

    print(f"MT: {len(mt.by_ref)} стихов ({MT_DIR})")
    print(f"LXX: {len(lxx.verses)} стихов ({LXX_ROOT})")
    print(f"связей в таблице: {len(LINKS)}"
          f" ({len(LINKS) * 2} обращений к текстам)\n")
    ok = miss_mt = miss_lxx = 0
    for mt_ref, lxx_ref, note, gr, heb in LINKS:
        mt_t = mt.text(mt_ref) if mt_ref in mt.by_ref else "НЕТ В MT"
        lx_t = lxx.text(lxx_ref)
        if mt_t == "НЕТ В MT":
            miss_mt += 1
        if lx_t == "НЕТ ТАКОГО СТИХА":
            miss_lxx += 1
        if mt_t != "НЕТ В MT" and lx_t != "НЕТ ТАКОГО СТИХА":
            ok += 1
        heb_hit = (heb == "—") or (mt_ref in mt.by_ref and
                                   mt.has_lexeme(mt_ref, heb))
        gr_hit = (gr == "—") or lxx.has(lxx_ref, gr)
        print(f"[{mt_ref} | {lxx_ref}] {note}")
        print(f"    MT : {mt_t}")
        print(f"    LXX: {lx_t}")
        print(f"    MT-лексема «{heb}»: {'есть' if heb_hit else 'НЕТ'}"
              f"   |   LXX-слово «{gr}»: {'есть' if gr_hit else 'НЕТ'}")
        print()
    print(f"итого: пар прочитано {ok}, MT-пропусков {miss_mt}, "
          f"LXX-пропусков {miss_lxx}; обращений к текстам {len(LINKS) * 2}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
