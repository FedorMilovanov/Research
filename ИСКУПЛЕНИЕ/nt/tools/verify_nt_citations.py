#!/usr/bin/env python3
"""Проверяльщик греческих цитат под-корпуса ИСКУПЛЕНИЕ/nt.

Что делает:
  1. Читает все *.md в ИСКУПЛЕНИЕ/nt/.
  2. Вытаскивает фрагменты в обратных кавычках, содержащие греческие буквы.
  3. Нормализует их (снимает пунктуацию; диакритику сохраняет) и ищет каждый
     фрагмент в корпусе свидетеля S1 (MorphGNT/SBLGNT).
  4. Сверяет заявленные в таблицах подсчёты лемм с фактическими в S1.

Правила приёма фрагмента:
  - список через «/» разбивается на части, проверяется каждая;
  - многоточие «…» / «...» делит цитату на сегменты, проверяется каждый
    (цитата с пропуском обязана быть верной в обеих половинах);
  - одиночное слово принимается, если оно встречается в S1 как словоформа
    ИЛИ как лемма (словарная форма типа λυτρόομαι в тексте не встречается);
  - корень поля с дефисом (ἀγοραζ-, ἱλασκ-) — имя поля, не цитата, пропускается.

Корпус S1 не хранится в Git (00_NT_AUTHORITY, §3): путь задаётся переменной
окружения NT_SBLGNT_DIR. Скрипт не изменяет рабочее дерево и не входит в CI.
"""
from __future__ import annotations

import os
import re
import sys
import unicodedata
from pathlib import Path

DEFAULT_SBLGNT = "/home/user/nt-corpus/py-sblgnt-master/pysblgnt/sblgnt"
CARD_DIR = Path(__file__).resolve().parent.parent
GREEK = re.compile(r"[\u0370-\u03FF\u1F00-\u1FFF]")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    return "".join(ch for ch in s if GREEK.match(ch))


def load_corpus(root: Path) -> tuple[dict[str, int], str]:
    lemma_count: dict[str, int] = {}
    words: list[str] = []
    for path in sorted(root.glob("*-morphgnt.txt")):
        for line in path.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) != 8:
                continue
            word, lemma = parts[5], parts[7]
            lemma_count[lemma] = lemma_count.get(lemma, 0) + 1
            words.append(word)
    return lemma_count, norm(" ".join(words))


def segments(raw: str) -> list[str]:
    out: list[str] = []
    for part in re.split(r"/", raw):
        for seg in re.split(r"\.\.\.|…", part):
            n = norm(seg)
            if len(n) >= 3:
                out.append(n)
    return out


def main() -> int:
    root = Path(os.environ.get("NT_SBLGNT_DIR", DEFAULT_SBLGNT))
    if not root.is_dir():
        print(f"NT corpus not found at {root}; set NT_SBLGNT_DIR")
        return 2
    lemma_count, blob = load_corpus(root)
    total_forms = sum(lemma_count.values())
    print(f"S1 loaded: {total_forms} word forms, {len(lemma_count)} lemmas")

    failures: list[str] = []
    checked = 0
    skipped = 0
    files = sorted(CARD_DIR.glob("*.md"))
    for md in files:
        text = md.read_text(encoding="utf-8")
        for raw in re.findall(r"`([^`]+)`", text):
            if not GREEK.search(raw):
                continue
            if raw.rstrip().endswith("-"):
                skipped += 1
                continue
            for frag in segments(raw):
                checked += 1
                if frag in blob or frag in lemma_count:
                    continue
                failures.append(f"{md.name}: NOT IN S1 -> {raw!r}")
                break
    print(f"Greek fragments checked: {checked}; field-stems skipped: {skipped}")

    declared: list[tuple[str, str, int]] = []
    for md in files:
        in_lemma_table = False
        for line in md.read_text(encoding="utf-8").splitlines():
            if line.startswith("|"):
                # заголовок таблицы решает, декларация ли это подсчёта лемм
                if re.match(r"^\|\s*Лемма\s*\|", line):
                    in_lemma_table = True
                    continue
                if in_lemma_table and set(line.replace("|", "").strip()) <= {"-", " ", ":"}:
                    continue
            else:
                in_lemma_table = False
                continue
            if not in_lemma_table:
                continue
            m = re.match(r"^\|\s*`([^`]+)`[^|]*\|\s*\**(\d+)\**\s*\|", line)
            if m and GREEK.search(m.group(1)):
                declared.append((md.name, m.group(1), int(m.group(2))))
    print(f"Declared lemma counts found in tables: {len(declared)}")
    ok = 0
    for md, lemma, n in declared:
        actual = lemma_count.get(lemma, 0)
        if actual == n:
            ok += 1
            print(f"  ok        {md:46s} {lemma:14s} {n}")
        else:
            print(f"  MISMATCH  {md:46s} {lemma:14s} declared={n} actual={actual}")
            failures.append(f"{md}: lemma {lemma} declared {n}, S1 has {actual}")

    if failures:
        print(f"\nFAIL ({len(failures)} problems)")
        for f in failures:
            print("  - " + f)
        return 1
    print(f"\nPASS: {checked} Greek fragments occur verbatim in S1; "
          f"{ok}/{len(declared)} declared lemma counts match S1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
