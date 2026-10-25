#!/usr/bin/env python3
"""Recompute the copy lengths and rewrite every document that quotes them.

Why this exists: four documents quoted the description length and three of them were
wrong at the same time, twice in two passes. A number that is quoted in prose is a
number that will drift, because editing the copy is a different action from editing
the sentence about the copy. This script makes the second action mechanical:

    python3 SUNO_HYMNS/scripts/sync_copy_counts.py          # rewrite, then report
    python3 SUNO_HYMNS/scripts/sync_copy_counts.py --check   # report only

The check itself lives in check_copy_lengths.py and runs in CI; this script is the
writer that keeps it green without hand-editing four files.

It touches only numbers that are followed by a form of «знак»/«character» on a line
that mentions the description, the pinned comments or the Telegram post. Anything
else in those files is left alone.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_copy_lengths import description, pinned, telegram_visible  # noqa: E402

DOCS = [
    "SUNO_HYMNS/README.md",
    "SUNO_HYMNS/HANDOFF_FOR_NEXT_AGENT.md",
    "SUNO_HYMNS/SUNO/DUTCH-005_YOUTUBE.md",
    "SUNO_HYMNS/SUNO/DUTCH-005_PINNED.md",
    "SUNO_HYMNS/SUNO/DUTCH-005_TELEGRAM.md",
    "SUNO_HYMNS/SUNO/STATUS_LEDGER.md",
    "SUNO_HYMNS/SUNO/NEXT_STEPS.md",
    "SUNO_HYMNS/SUNO/PUBLICATION_LANE.md",
]


def ru_znakov(n: int) -> str:
    """Russian plural form for «знак», agreeing with the number."""
    if 11 <= n % 100 <= 14:
        return "знаков"
    last = n % 10
    if last == 1:
        return "знак"
    if 2 <= last <= 4:
        return "знака"
    return "знаков"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="report without writing")
    args = parser.parse_args()

    desc = len(description())
    pins = [len(block) for block in pinned()]
    tg = len(telegram_visible())
    print(f"measured: description {desc} {ru_znakov(desc)}, pinned {pins[0]} and {pins[1]}, telegram {tg}")

    # (regex, value) — applied to every document below
    rules = [
        (re.compile(r"(?<=до лимита 5000 остаётся )\d+"), str(5000 - desc)),
        (re.compile(r"(?<=\[x\] )\d+(?=\s*знак)"), str(desc)),
        (re.compile(r"\d+(?=-character description)"), str(desc)),
        (re.compile(r"(?<=\()\d+(?= characters, \d+ bold)"), str(desc)),
        (re.compile(r"(?<=description )\d+(?= characters)"), str(desc)),
        (re.compile(r"(?<=описание )\d+(?=\s*знак)"), str(desc)),
    ]
    pair_rules = [
        (re.compile(r"\d+\s*знак\w*(?=,\s*до лимита 5000)"), f"{desc} {ru_znakov(desc)}"),
        (re.compile(r"(\*\*Закреп 1\*\*[^\n]{0,40}?)\d+(\s*знак)"), rf"\g<1>{pins[0]}\g<2>"),
        (re.compile(r"(\*\*Закреп 2\*\*[^\n]{0,40}?)\d+(\s*знак)"), rf"\g<1>{pins[1]}\g<2>"),
    ]

    changed: list[str] = []
    for name in DOCS:
        path = ROOT / name
        if not path.exists():
            continue
        text = original = path.read_text(encoding="utf-8")
        text = rules[0][0].sub(str(5000 - desc), text)
        text = rules[1][0].sub(str(desc), text)
        text = rules[2][0].sub(str(desc), text)
        text = rules[3][0].sub(str(desc), text)
        text = rules[4][0].sub(str(desc), text)
        text = rules[5][0].sub(str(desc), text)
        for pattern, replacement in pair_rules:
            text = pattern.sub(replacement, text)
        # Telegram: «Длина: **1477** видимых знаков»
        text = re.sub(r"(Длина: \*\*)\d+(\*\* видимых знаков)", rf"\g<1>{tg}\g<2>", text)
        if text != original:
            changed.append(name)
            if not args.check:
                path.write_text(text, encoding="utf-8")

    if changed:
        verb = "would change" if args.check else "rewrote"
        print(f"{verb}: " + ", ".join(changed))
    else:
        print("all documents already quote the measured lengths")
    return 0


if __name__ == "__main__":
    sys.exit(main())
