#!/usr/bin/env python3
"""Strict Russian NT references: a comma is a list, a dash is a range.

Chapter references can reuse the preceding book: «Мф 23:37; 11:28–30».
The parser does not invent intervening verses, cross-book ranges or references
from prose without a named book. A whole-book silence card has no verse set.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import re
from pathlib import Path

from nt_sources import ROOT, registry, witness_dir

BOOKS = ["Мф", "Мк", "Лк", "Ин", "Деян", "Рим", "1 Кор", "2 Кор", "Гал", "Еф",
         "Флп", "Кол", "1 Фес", "2 Фес", "1 Тим", "2 Тим", "Тит", "Флм",
         "Евр", "Иак", "1 Пет", "2 Пет", "1 Ин", "2 Ин", "3 Ин", "Иуд", "Откр"]
BOOKRE = "|".join(re.escape(b) for b in sorted(BOOKS, key=len, reverse=True))
ITEM = r"\d+(?:\s*[–—-]\s*\d+)?"
REFERENCE = re.compile(rf"(?<!\w)(?:(?P<book>{BOOKRE})\s+)?(?P<chapter>\d+):"
                       rf"(?P<items>{ITEM}(?:\s*,\s*{ITEM})*)")
CARD_HEADING = re.compile(r"(?m)^## ((?:0[678]|10)\.\d+) (.+)$")


def expand(text: str) -> set[str]:
    refs: set[str] = set()
    book = None
    for m in REFERENCE.finditer(text):
        book = m["book"] or book
        if book is None:
            continue
        ch = int(m["chapter"])
        for item in m["items"].split(","):
            bounds = [int(n) for n in re.split(r"\s*[–—-]\s*", item.strip())]
            first, last = bounds[0], bounds[-1]
            if ch < 1 or first < 1 or last < first:
                raise ValueError(f"invalid NT range: {m.group(0)}")
            refs.update(f"{book} {ch}:{v}" for v in range(first, last + 1))
    for m in re.finditer(r"(?<!\w)(Флм|2 Ин|3 Ин|Иуд)\s+(\d+(?:(?:\s*,\s*|\s+и\s+)\d+)*)(?![\d:])", text):
        for n in re.findall(r"\d+", m[2]):
            if int(n) < 1:
                raise ValueError(f"invalid NT verse: {m.group(0)}")
            refs.add(f"{m[1]} 1:{int(n)}")
    return refs


def cards(path: Path):
    text = path.read_text(encoding="utf-8")
    heads = list(CARD_HEADING.finditer(text))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        yield m[1], m[2], text[m.end():end]


def card_refs() -> set[str]:
    refs: set[str] = set()
    for row in registry()["pericopeCards"]:
        path = ROOT / row["file"]
        if not path.is_file():
            raise ValueError(f"required pericope file missing: {path}")
        for cid, title, body in cards(path):
            if cid in registry().get("nonTextCards", ["08.34"]) or cid.endswith(".0") or cid.startswith("10.") and int(cid.split(".")[1]) > 9:
                continue
            found = expand(title)
            if not found:
                raise ValueError(f"{path.name}: {cid}: no verse reference in heading")
            refs.update(found)
    return refs


def s1_verses() -> dict[str, list[list[str]]]:
    result: dict[str, list[list[str]]] = {}
    for path in sorted(witness_dir("S1").glob("*-morphgnt.txt")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            row = line.split()
            if len(row) != 8 or not re.fullmatch(r"\d{6}", row[0]):
                raise ValueError(f"S1 malformed row: {path.name}:{lineno}")
            code = row[0]
            book = int(code[:2])
            if not 1 <= book <= len(BOOKS):
                raise ValueError(f"S1 invalid book: {code}")
            ref = f"{BOOKS[book - 1]} {int(code[2:4])}:{int(code[4:])}"
            result.setdefault(ref, []).append(row)
    if not result:
        raise ValueError("S1 has no parsed verses")
    return result

# --- Сиглы SBLGNT внутри S1 ---------------------------------------------------
# MorphGNT хранит знаки SBLGNT в поле 4 (индекс 4): ⸀ одиночное слово, ⸁ одиночное
# слово (второй уровень), ⸂…⸃ и ⸄…⸅ — пролёты. Поле 5 — чистый текст, знаков в
# нём нет; именно поэтому «S1 сигл не хранит» — неверное чтение формата, а не факт.
SIGN_MARKS = "⸀⸁⸂⸃⸄⸅"
SIGN_PAIRS = ("⸂", "⸄")


def s1_sign_tokens(ref: str) -> list[str]:
    """Токены стиха, несущие знаки SBLGNT (поле 4)."""
    return [row[4] for row in s1_verses()[ref] if any(m in row[4] for m in SIGN_MARKS)]


def s1_sign_spans(rows: list[list[str]]) -> int:
    """Число позиций, помеченных знаками: одиночные ⸀/⸁ и открывающие ⸂/⸄."""
    total = 0
    for row in rows:
        text = row[4]
        if "⸀" in text or "⸁" in text:
            total += 1
        if any(pair in text for pair in SIGN_PAIRS):
            total += 1
    return total


def s1_sign_inventory() -> dict[str, int]:
    """Счёт знаков по всему S1 — пин против «знаков нет» и против смены транскрипции."""
    counts = {mark: 0 for mark in SIGN_MARKS}
    for rows in s1_verses().values():
        for row in rows:
            for mark in SIGN_MARKS:
                counts[mark] += row[4].count(mark)
    return counts


def s1_sign_spans_by_ref() -> dict[str, int]:
    """Число помеченных позиций по стихам (стихи без знаков не попадают в словарь)."""
    result = {}
    for ref, rows in s1_verses().items():
        spans = s1_sign_spans(rows)
        if spans:
            result[ref] = spans
    return result
