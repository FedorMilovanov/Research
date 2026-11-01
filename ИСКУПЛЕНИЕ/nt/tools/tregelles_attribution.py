#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка атрибуции S7 независимым текстом Tregelles (S8).

Зачем
-----
Аппарат S7 приписывает чтения изданиям (`#Treg`, `#RP`, `#WH`, `#NA`, `#NIV`).
До сих пор это принималось на веру: своих рукописей у корпуса нет, а издания —
есть, но только Tregelles (S8) представлен полным текстом. Значит слой
атрибуции проверяется по нему: если S7 говорит «Treg читает X», текст S8 в этом
стихе обязан содержать X.

Как считается
-------------
* S8 — транскрипция Tyndale House 2009, строка = стих, `Book.CH:VS <текст>`.
* Из S7 берётся **каждое** чтение, в списке свидетелей которого есть `Treg`.
* Сравнение идёт по нормализованным словам (Robinson ASCII, без диакритики и
  регистра), с допуском на орфографию XIX века: расстояние Левенштейна ≤1 при
  длине ≥4 и ≤2 при длине ≥9 (`Ἰωάνου` / `Ἰωάννου`, `Δαυεὶδ` / `Δαυίδ`).
* `…` в чтении — пропуск внутри цитаты: фрагменты ищутся по порядку.
* `[ν]` внутри слова — факультативная подвижная ν: скобки снимаются, буква
  остаётся (`ἤνοιξε[ν]` → `ἤνοιξεν`).
* Пустое чтение — пропуск: подтверждается, если слова леммы в стихе S8 нет;
  если такое слово в стихе есть, случай признаётся **нерешаемым** (омонима не
  отличить от другого вхождения).
* `+ N …` — добавление целого стиха; стих проверяется как отдельная строка S8.

Границы
-------
Транскрипция S8 может быть неполной, а S7 — ошибаться; локально решается только
факт расхождения, не виновный. Печатный Tregelles и печатный SBLGNT не получены.
Атрибуция рукописям этим не проверяется вообще.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True

from nt_sources import witness_dir
from sbl_apparatus import Apparatus
from verify_nt_variants import greek_words

TR_NAMES = {"Mat": "Мф", "Mark": "Мк", "Luke": "Лк", "John": "Ин", "Acts": "Деян",
            "Rom": "Рим", "1Co": "1 Кор", "2Co": "2 Кор", "Gal": "Гал", "Eph": "Еф",
            "Phi": "Флп", "Col": "Кол", "1Th": "1 Фес", "2Th": "2 Фес", "1Ti": "1 Тим",
            "2Ti": "2 Тим", "Tit": "Тит", "Phm": "Флм", "Heb": "Евр", "Jas": "Иак",
            "1Pet": "1 Пет", "2Pet": "2 Пет", "1John": "1 Ин", "2John": "2 Ин",
            "3John": "3 Ин", "Jude": "Иуд", "Rev": "Откр"}

S8_LINE = re.compile(r"([0-9A-Za-z]+)\.(\d+):(\d+)(?:\s+(.*))?$")


def s8_verses() -> dict[str, list[str]]:
    path = witness_dir("S8") / "TNT.txt"
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = S8_LINE.match(line)
        if not m or m[1] not in TR_NAMES:
            continue
        result[f"{TR_NAMES[m[1]]} {int(m[2])}:{int(m[3])}"] = greek_words(m[4] or "")
    if not result:
        raise ValueError("S8 has no parsed verses")
    return result


def _lev(a: str, b: str) -> int:
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def close_enough(a: str, b: str) -> bool:
    """Орфографический допуск XIX века, а не смысловой: длина и одна-две буквы."""
    if a == b:
        return True
    distance = _lev(a, b)
    longest = max(len(a), len(b))
    return (distance == 1 and longest >= 4) or (distance <= 2 and longest >= 9)


def reading_words(text: str) -> list[str]:
    """Слова чтения S7 без скобок; `[ν]` — подвижная ν внутри слова."""
    text = re.sub(r"\+\s*\d+\s*", " ", text)
    text = text.replace("[", "").replace("]", "")
    text = text.replace("(", " ").replace(")", " ").replace("+", " ")
    return [w for fragment in text.split("…") for w in greek_words(fragment)]


def found_in_order(verse: list[str], words: list[str]) -> bool:
    position = 0
    for word in words:
        hit = False
        for i in range(position, len(verse)):
            if close_enough(word, verse[i]):
                position, hit = i + 1, True
                break
            if close_enough(word, verse[i] + verse[i + 1]) if i + 1 < len(verse) else False:
                position, hit = i + 2, True
                break
        if not hit:
            return False
    return True


def _next_ref(ref: str) -> str:
    book, loc = ref.rsplit(" ", 1)
    chapter, verse = loc.split(":")
    return f"{book} {int(chapter)}:{int(verse) + 1}"


ADDED_VERSE = re.compile(r"^\+\s*\d+")


def classify(ref: str, text: str, verse: list[str], s8: dict[str, list[str]]) -> str:
    """Почему чтение не нашлось: артефакт деления или содержательное расхождение."""
    stripped = text.strip()
    if re.match(r"^\d+\s", stripped):
        return "перенумерация стихов"
    if stripped.startswith("+") and (ADDED_VERSE.match(stripped) or re.search(r"\b\d+\b", stripped)):
        return "добавленный стих"
    words = reading_words(text)
    if words and "".join(words) in "".join(verse):
        return "деление слов"
    following = s8.get(_next_ref(ref), [])
    if following and found_in_order(verse + following, words):
        return "пролёт через границу стиха"
    if re.search(r"[Ἀ-Ὧ]\w*\.", text):
        return "сокращение в цитате"
    return "содержательное"


def check_tregelles_attribution() -> dict:
    s8 = s8_verses()
    apparatus = Apparatus()
    stats = Counter()
    mismatches = []
    for ref, entries in sorted(apparatus.entries.items()):
        for entry in entries:
            for reading in entry["rdg"]:
                if not any("Treg" in w for w in reading["wit"]):
                    continue
                verse = s8.get(ref)
                text = reading["text"].strip()
                if verse is None:
                    stats["нет_стиха_в_S8"] += 1
                    mismatches.append([ref, entry["lem"], text, "нет стиха в S8"])
                    continue
                if not text:
                    if not verse:
                        stats["пропуск_подтверждён"] += 1  # стих есть, но пуст
                        continue
                    lemma = greek_words(entry["lem"])
                    if any(w in verse for w in lemma):
                        stats["пропуск_нерешаем"] += 1
                    else:
                        stats["пропуск_подтверждён"] += 1
                    continue
                if found_in_order(verse, reading_words(text)):
                    stats["совпало"] += 1
                else:
                    kind = classify(ref, text, verse, s8)
                    stats["разошлось: " + kind] += 1
                    mismatches.append([ref, entry["lem"], text, kind])
    return {"stats": dict(stats), "total": sum(stats.values()),
            "scope": "Атрибуция S7 изданиям, а не рукописям; S8 — одна транскрипция XIX в. "
                     "Допуск на орфографию, не на смысл. Расхождение фиксируется, виновный не назначается.",
            "mismatches": mismatches}


if __name__ == "__main__":
    result = check_tregelles_attribution()
    print(result["stats"], "всего", result["total"])
    for row in result["mismatches"]:
        print(row)
