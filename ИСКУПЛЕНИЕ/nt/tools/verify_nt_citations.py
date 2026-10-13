#!/usr/bin/env python3
"""Проверяльщик греческих цитат под-корпуса ИСКУПЛЕНИЕ/nt.

Что делает:
  1. Читает все *.md в ИСКУПЛЕНИЕ/nt/.
  2. Вытаскивает фрагменты в обратных кавычках, содержащие греческие буквы.
  3. Нормализует их (снимает пунктуацию; диакритику сохраняет) и ищет каждый
     фрагмент в корпусе свидетеля S1 (MorphGNT/SBLGNT).
  4. Сверяет заявленные в таблицах подсчёты лемм с фактическими в S1.

Правила приёма фрагмента:
  - содержимое fenced-блоков (``` … ```) не рассматривается: там команды и
    определения, а не цитаты (см. strip_fences);
  - список через «/» разбивается на части, проверяется каждая;
  - многоточие «…» / «...» делит цитату на сегменты, проверяется каждый
    (цитата с пропуском обязана быть верной в обеих половинах);
  - одиночное слово принимается, если оно встречается в S1 как словоформа
    ИЛИ как лемма (словарная форма типа λυτρόομαι в тексте не встречается);
  - корень поля с дефисом (ἀγοραζ-, ἱλασκ-) — имя поля, не цитата, пропускается.

Корпус S1 не хранится в Git (00_NT_AUTHORITY, §3): путь задаётся переменной
окружения NT_SBLGNT_DIR. Скрипт не изменяет рабочее дерево. Пины проверяются до чтения цитат.
"""
from __future__ import annotations

import os
import re
import sys
sys.dont_write_bytecode = True
import unicodedata
from pathlib import Path

from nt_sources import ROOT, registry, witness_dir
from nt_refs import cards, expand, s1_verses

# Compatibility names resolve exact pins, never a master or wildcard checkout.
DEFAULT_SBLGNT = str(witness_dir("S1", verify=False))
DEFAULT_LXX = str(witness_dir("S5", verify=False))
# Цитата LXX помечается префиксом «LXX» внутри обратных кавычек:
#   `LXX ἱλαστήριον`   -> проверяется по свидетелю S5
#   `λύτρον`           -> проверяется по свидетелю S1 (НЗ)
# Без маршрутизации цитата LXX не прошла бы сверку: её нет в НЗ.
CARD_DIR = Path(__file__).resolve().parent.parent
GREEK = re.compile(r"[\u0370-\u03FF\u1F00-\u1FFF]")
CYRILLIC = re.compile(r"[\u0400-\u04FF]")


def case_variants_first_char(frag: str) -> list[str]:
    """Варианты фрагмента, отличающиеся ТОЛЬКО регистром первого символа.

    Заглавная буква в начале предложения — орфография, а не лексика, поэтому
    первый символ терпим. Регистр в середине цитаты — уже не орфография:
    греческое слово с заглавной внутри — другое слово (имя собственное против
    нарицательного), и прежний сплошной casefold() всей строки это молча
    проглатывал.
    """
    if not frag:
        return [frag]
    first = frag[0]
    out = {frag}
    for ch in (first.upper(), first.casefold(), first.title()):
        if ch:
            out.add(ch + frag[1:])
    return sorted(out)


def norm(s: str) -> str:
    """NFC and punctuation removal, preserving every word boundary/diacritic."""
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"\s+", " ", "".join(
        ch if GREEK.match(ch) and unicodedata.category(ch)[0] in "LM" else " "
        for ch in s)).strip()


def occurs(frag: str, blob: str, lemmas: dict[str, int] | None = None) -> bool:
    # Each verse is separately padded. Neither substrings of words nor a quote
    # straddling two verses can match. Lemmas are allowed only as single words.
    return any(" " + v + " " in blob or (lemmas is not None and " " not in v and v in lemmas)
               for v in case_variants_first_char(frag))


def strip_fences(text: str) -> str:
    """Убирает содержимое fenced-блоков (``` … ```).

    Зачем: извлечение фрагментов идёт по ``([^`]+)``, где [^`]+ проходит через
    переводы строк. Ограждение блока — это три обратные кавычки, поэтому
    первая и последняя кавычки двух соседних ограждений образуют пару, между
    которой оказывается shell-команда с кириллицей. Это срабатывало как
    «смешение письма» на разметке, а не на цитате.

    Правило структурное, а не подгонка под данные: греческая цитата в этом
    под-корпусе живёт в одиночных обратных кавычках внутри строки, а
    fenced-блок держит команды и определения. Проверено на всём корпусе
    ИСКУПЛЕНИЕ/: ни один fenced-блок не содержит греческих букв, поэтому
    пропуск блоков не способен спрятать ни одной реальной цитаты.
    """
    out: list[str] = []
    inside = False
    for line in text.splitlines(keepends=True):
        if line.startswith("```"):
            inside = not inside
            continue
        if not inside:
            out.append(line)
    return "".join(out)


def load_lxx(root: Path) -> str:
    verses: dict[str, list[str]] = {}
    paths = sorted(root.glob("*.txt"))
    if not paths:
        raise ValueError(f"S5 text files missing: {root}")
    for path in paths:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            parts = line.split(" ", 1)
            if len(parts) != 2 or parts[0].count(".") != 2:
                raise ValueError(f"S5 malformed row: {path.name}:{lineno}")
            verses.setdefault(parts[0], []).append(parts[1])
    return "\n".join(" " + norm(" ".join(words)) + " " for words in verses.values())


def load_corpus(root: Path) -> tuple[dict[str, int], str]:
    lemma_count: dict[str, int] = {}
    verses: dict[str, list[str]] = {}
    paths = sorted(root.glob("*-morphgnt.txt"))
    if not paths:
        raise ValueError(f"S1 text files missing: {root}")
    for path in paths:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            parts = line.split()
            if len(parts) != 8:
                raise ValueError(f"S1 malformed row: {path.name}:{lineno}")
            word, lemma = parts[5], parts[7]
            lemma_count[lemma] = lemma_count.get(lemma, 0) + 1
            verses.setdefault(parts[0], []).append(word)
    blob = "\n".join(" " + norm(" ".join(words)) + " " for words in verses.values())
    return lemma_count, blob


def segments(raw: str) -> list[str]:
    out: list[str] = []
    for part in re.split(r"/", raw):
        for seg in re.split(r"\.\.\.|…", part):
            n = norm(seg)
            if n:
                out.append(n)
    return out


def main() -> int:
    root = witness_dir("S1")
    lemma_count, blob = load_corpus(root)
    lxx_root = witness_dir("S5")
    lxx_blob = load_lxx(lxx_root)
    print(f"S5 (LXX) verified and loaded: {len(lxx_blob)} chars")
    total_forms = sum(lemma_count.values())
    print(f"S1 loaded: {total_forms} word forms, {len(lemma_count)} lemmas")

    failures: list[str] = []
    checked = 0
    skipped = 0
    files = sorted(CARD_DIR.glob("*.md"))
    required = registry().get("requiredMarkdownFiles", [])
    for name in required:
        if not (ROOT / name).is_file():
            failures.append(f"Required markdown missing: {name}")
    extra = [ROOT / "ИСКУПЛЕНИЕ" / name for name in (
        "04_LIMITED_VS_UNIVERSAL_QUESTION_MAP.md", "12_HARD_TEXTS_EXTENT_CARDS.md")]
    extra += [Path(x) for x in os.environ.get("NT_EXTRA_CARDS", "").split(":") if x]
    for e in extra:
        if e.is_file():
            if e not in files:
                files.append(e)
        else:
            failures.append(f"NT_EXTRA_CARDS: required file missing: {e}")
    for md in files:
        text = strip_fences(md.read_text(encoding="utf-8"))
        for raw in re.findall(r"`([^`]+)`", text):
            if not GREEK.search(raw):
                continue
            if raw.strip().endswith("-") or raw.strip().startswith("-"):
                skipped += 1
                continue
            # смешение письма: norm() срезает кириллицу, поэтому смотрим raw
            if CYRILLIC.search(raw):
                failures.append(f"{md.name}: MIXED SCRIPT (Cyrillic inside Greek) -> {raw!r}")
                continue
            # маршрутизация по свидетелю: «LXX …» -> S5, остальное -> S1
            stripped = raw.strip()
            if stripped.startswith("LXX ") or stripped.startswith("LXX:"):
                target = re.sub(r"^LXX\s*:?\s*", "", stripped)
                base, tag = lxx_blob, "S5"
            else:
                target = raw
                base, tag = blob, "S1"
            if re.search(r"[A-Za-z]", target):
                failures.append(f"{md.name}: MIXED SCRIPT (Latin inside Greek) -> {raw!r}")
                continue
            for frag in segments(target):
                checked += 1
                if occurs(frag, base, lemma_count if tag == "S1" else None):
                    continue
                failures.append(f"{md.name}: NOT IN {tag} -> {raw!r}")
                break
    print(f"Greek fragments checked: {checked}; field-stems skipped: {skipped}")

    # Primary S1 quotations must also belong to the card's cited verse set.
    anchored = 0
    verse_map = s1_verses()
    for row in registry()["pericopeCards"]:
        path = ROOT / row["file"]
        if not path.is_file():
            failures.append(f"Required card file missing: {path}")
            continue
        for cid, title, body in cards(path):
            match = re.search(r"\*\*Текст S1(?: \([^)]*\))?:\*\*(.*?)(?=\n\*\*|\n---|\Z)", body, re.S)
            if not match:
                continue  # mandatory primary blocks are checked by card discipline
            refs = expand(title)
            if not refs or refs - verse_map.keys():
                failures.append(f"{path.name}: {cid}: invalid/missing S1 references {sorted(refs - verse_map.keys())}")
                continue
            base = "\n".join(" " + norm(" ".join(r[5] for r in verse_map[ref])) + " " for ref in refs)
            for raw in re.findall(r"`([^`]+)`", match[1]):
                if not GREEK.search(raw):
                    continue
                for frag in segments(raw):
                    anchored += 1
                    if not occurs(frag, base):
                        failures.append(f"{path.name}: {cid}: NOT AT CITED VERSES -> {raw!r}")
    print(f"Primary quoted fragments anchored to card references: {anchored}")

    # SSOT exact lemma declarations are checked independently of markdown tables.
    ssot_counts = 0
    for field in registry()["lexicalFields"]:
        for lemma, count in field["computedCounts"].items():
            if isinstance(count, int) and GREEK.search(lemma) and not re.search(r"[-/]", lemma):
                ssot_counts += 1
                if lemma_count.get(lemma, 0) != count:
                    failures.append(f"SSOT {field['id']}: {lemma}: {count} != {lemma_count.get(lemma, 0)}")
    if total_forms != registry()["textWitnesses"][0]["parsedWordForms"]:
        failures.append(f"S1 parsed form count drift: {total_forms}")
    print(f"SSOT exact lemma counts checked: {ssot_counts}")

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
    print(f"\nPASS: {checked} Greek fragments match whole words within verses in S1/S5; "
          f"{ok}/{len(declared)} declared lemma counts match S1.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyError, OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
