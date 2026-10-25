#!/usr/bin/env python3
"""Fail when a document quotes a length that no longer matches the file.

This is the guard for a defect that cost a whole review pass: the description
was described as 4182 characters in four places, as 4190 in a fifth, and measured
4461 by the end of that pass; the two pinned comments were quoted at 1503 and 1579 and were
1467 and 1590; the Telegram post was quoted at 1479 and carried 1477. Every one
of those numbers was true on the day it was typed.

So every quoted length is now recomputed from the block itself:

- the YouTube description is the first fenced block under "## 2." of
  DUTCH-005_YOUTUBE.md;
- each pinned comment is a fenced block of DUTCH-005_PINNED.md;
- the Telegram post is the text between the header line and the hashtag line of
  DUTCH-005_TELEGRAM.md, measured with markup characters stripped, because that
  is what the operator sees.

Read-only. Usage:
    python3 SUNO_HYMNS/scripts/check_copy_lengths.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUNO = ROOT / "SUNO_HYMNS" / "SUNO"


def fenced(text: str) -> list[str]:
    return re.findall(r"```[a-z]*\n(.*?)\n```", text, re.S)


def description() -> str:
    src = (SUNO / "DUTCH-005_YOUTUBE.md").read_text(encoding="utf-8")
    section = src.split("## 2.", 1)[1]
    return re.search(r"```text\n(.*?)\n```", section, re.S).group(1)


def telegram_visible() -> str:
    src = (SUNO / "DUTCH-005_TELEGRAM.md").read_text(encoding="utf-8")
    start = src.index("**«Хвала Славе»**", src.index("## 1."))
    end = src.index("\n", src.index("#ХристианскийГимн", start))
    return re.sub(r"\*", "", src[start:end])


def main() -> int:
    problems: list[str] = []

    yt_doc = (SUNO / "DUTCH-005_YOUTUBE.md").read_text(encoding="utf-8")
    pin_doc = (SUNO / "DUTCH-005_PINNED.md").read_text(encoding="utf-8")
    tg_doc = (SUNO / "DUTCH-005_TELEGRAM.md").read_text(encoding="utf-8")

    desc = len(description())
    pins = [len(b) for b in fenced(pin_doc)]
    tg = len(telegram_visible())

    if len(pins) != 2:
        problems.append(f"DUTCH-005_PINNED.md: expected 2 pinned comments, found {len(pins)}")

    print(f"description: {desc} characters")
    if f"{desc} знак" not in yt_doc:
        problems.append(
            f"DUTCH-005_YOUTUBE.md does not state the real description length ({desc})"
        )

    for i, n in enumerate(pins, 1):
        print(f"pinned comment {i}: {n} characters")
        if str(n) not in yt_doc:
            problems.append(f"DUTCH-005_YOUTUBE.md § 3 does not state pin {i}'s real length ({n})")

    print(f"Telegram post: {tg} visible characters")
    if str(tg) not in tg_doc:
        problems.append(f"DUTCH-005_TELEGRAM.md does not state its real length ({tg})")

    if desc > 5000:
        problems.append(f"YouTube description is {desc} characters, over the 5000 limit")
    if tg > 4096:
        problems.append(f"Telegram post is {tg} visible characters, over the 4096 limit")

    for problem in problems:
        print(f"FAIL: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
