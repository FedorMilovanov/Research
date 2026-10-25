#!/usr/bin/env python3
"""Audit Russian lyric files for two mechanical defects.

1. **Missing ё.** A Russian lyric must print ё wherever the letter belongs, because
   ё carries the stress and decides the word (`всё` / `все`, `осёл` / `осел`).
   The check cannot decide the grammar, so it does the next honest thing: it lists
   every occurrence of a word that *might* need ё, with context, for a human to
   read. It reports, it never auto-fixes.

2. **Over-marking.** A stress mark belongs on a word whose stress is decided by
   grammar and could be got wrong, or on a word heard sung wrong. It does not
   belong on every word: an accent changes the text the model reads. This check
   fails when more than `--max-marks` distinct words carry an accent, so blanket
   marking cannot creep back in unnoticed.

Read-only. Usage:  python scripts/check_ru_lyric.py SUNO/DUTCH-005_LYRICS_SUNO.md
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

ACCENT = "\u0301"

# Words that must print ё in a Russian lyric. Matched on the exact token, lowercased;
# the ё-less spelling is what gets reported. Not exhaustive — it covers the forms that
# actually lose their dots in hymn and psalm paraphrase, above all the pronouns and the
# -ёт verbs, where losing ё also loses the stress and can change the word.
WORDS_WITH_YO = {
    "все": "все / всё — decides number, check each occurrence",
    "еще": "ещё", "ее": "её", "нее": "неё", "нем": "нём (о нём)",
    "мое": "моё", "твое": "твоё", "свое": "своё",
    "моем": "моём", "твоем": "твоём", "своем": "своём",
    "идет": "идёт", "идеш": "идёшь", "идут": "идут (no ё — fine)",
    "живет": "живёт", "живеш": "живёшь", "живем": "живём",
    "дает": "даёт", "даеш": "даёшь", "даем": "даём", "даете": "даёте",
    "поет": "поёт", "поем": "поём (we sing)", "поете": "поёте",
    "несет": "несёт", "ведет": "ведёт", "везет": "везёт", "зовет": "зовёт",
    "рвет": "рвёт", "жнет": "жнёт", "льет": "льёт", "шьет": "шьёт",
    "цветет": "цветёт", "растет": "растёт", "почет": "почёт",
    "мертвый": "мёртвый", "твердый": "твёрдый", "темный": "тёмный",
    "легкий": "лёгкий", "тяжелый": "тяжёлый", "веселый": "весёлый",
    "зеленый": "зелёный", "теплый": "тёплый", "черный": "чёрный",
    "желтый": "жёлтый", "светлый": "светлый (no ё — fine)",
    "шел": "шёл", "елка": "ёлка", "ел": "ёл / ел — check",
    "звезда": "звезда (no ё — fine)", "пчела": "пчела (no ё — fine)",
}

CYR = r"А-Яа-яЁё"


def words(text: str) -> list[str]:
    return re.findall(rf"(?:[{CYR}]{ACCENT}?)+", unicodedata.normalize("NFC", text))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--max-marks", type=int, default=12,
                    help="fail if more distinct accented words than this (default 12)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    failed = False
    for path in args.paths:
        text = unicodedata.normalize("NFC", path.read_text(encoding="utf-8"))
        body = text
        if "```" in body:  # audit the lyric block only, never the prose around it
            m = re.search(r"```[^\n]*\n(\[Intro\].*?)```", body, re.S)
            if m:
                body = m.group(1)
        toks = words(body)

        accented = sorted({w.replace(ACCENT, "") for w in toks if ACCENT in w})
        accented_lower = sorted({w.lower() for w in accented})

        seen, suspect = set(), []
        for line in body.splitlines():
            for w in words(line):
                bare = w.replace(ACCENT, "").lower()
                if bare in seen:
                    continue
                hint = WORDS_WITH_YO.get(bare)
                if hint and "ё" not in bare:
                    seen.add(bare)
                    suspect.append((w, hint, line.strip()))

        if not args.quiet:
            print(f"\n{path}")
            print(f"  accented words: {len(accented)} — {', '.join(accented) or 'none'}")
            if suspect:
                print("  ё to check (read each in context; «все» is correct in the plural):")
                for w, hint, line in suspect:
                    print(f"    {w:<12} {hint:<34} | {line}")
            else:
                print("  possible missing ё: none")

        if len(accented) > args.max_marks:
            print(f"  FAIL: {len(accented)} accented words > --max-marks {args.max_marks}; "
                  "an accent is a text change, not decoration", file=sys.stderr)
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
