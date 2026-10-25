#!/usr/bin/env python3
"""Fail when a document quotes a length that no longer matches the block.

This guards a real defect: the YouTube description was described as 4182
characters in four places, as 4190 in a fifth, and measured 4461 by the end of
that pass; the two pinned comments were quoted at 1503 and 1579 and were 1467
and 1590; the Telegram post was quoted at 1479 and carried 1477. Every one of
those numbers was true on the day it was typed.

A first version of this script only asked whether the number appeared *somewhere*
in the document, which passed while half the mentions were stale. It now reads
the number out of each specific sentence and compares it with the recomputed
value:

- description: the sentence "<N> знаков, до лимита 5000" and the checklist line
  "- [x] <N> знаков;" of DUTCH-005_YOUTUBE.md;
- pinned comments: "Закреп 1 … <N> знаков" and "Закреп 2 … <N> знаков" in § 3 of
  the same file, against the two fenced blocks of DUTCH-005_PINNED.md;
- Telegram: "Длина: **<N>** видимых знаков" in DUTCH-005_TELEGRAM.md, against the
  post text with markup characters stripped.

Read-only. Usage:
    python3 SUNO_HYMNS/scripts/check_copy_lengths.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUNO = ROOT / "SUNO_HYMNS" / "SUNO"

YT_LIMIT = 5000
TG_LIMIT = 4096


def description() -> str:
    src = (SUNO / "DUTCH-005_YOUTUBE.md").read_text(encoding="utf-8")
    section = src.split("## 2.", 1)[1]
    body = re.search(r"```text\n(.*?)\n```", section, re.S)
    if body is None:
        raise SystemExit("DUTCH-005_YOUTUBE.md § 2 has no fenced description block")
    return body.group(1)


def pinned() -> list[str]:
    src = (SUNO / "DUTCH-005_PINNED.md").read_text(encoding="utf-8")
    return re.findall(r"```text\n(.*?)\n```", src, re.S)


def telegram_visible() -> str:
    src = (SUNO / "DUTCH-005_TELEGRAM.md").read_text(encoding="utf-8")
    start = src.index("**«Хвала Славе»**", src.index("## 1."))
    end = src.index("\n", src.index("#ХристианскийГимн", start))
    return re.sub(r"\*", "", src[start:end])


def claimed(patterns: list[str], text: str, label: str, problems: list[str]) -> list[int]:
    found: list[int] = []
    for pattern in patterns:
        match = re.search(pattern, text)
        if match is None:
            problems.append(f"{label}: the document no longer states its length ({pattern})")
        else:
            found.append(int(match.group(1)))
    return found


def main() -> int:
    problems: list[str] = []

    yt = (SUNO / "DUTCH-005_YOUTUBE.md").read_text(encoding="utf-8")
    tg = (SUNO / "DUTCH-005_TELEGRAM.md").read_text(encoding="utf-8")

    desc = len(description())
    pins = [len(block) for block in pinned()]
    tg_len = len(telegram_visible())

    print(f"description: {desc} characters")
    for value in claimed(
        [r"(\d+) знаков, до лимита 5000", r"- \[x\] (\d+) знак"],
        yt,
        "DUTCH-005_YOUTUBE.md description",
        problems,
    ):
        if value != desc:
            problems.append(f"DUTCH-005_YOUTUBE.md says the description is {value}, it is {desc}")

    if len(pins) != 2:
        problems.append(f"DUTCH-005_PINNED.md: expected 2 pinned comments, found {len(pins)}")
    for index, length in enumerate(pins, 1):
        print(f"pinned comment {index}: {length} characters")
        stated = claimed(
            [rf"\*\*Закреп {index}\*\*[^\n]*?(\d+) знак"],
            yt,
            f"DUTCH-005_YOUTUBE.md § 3, pinned comment {index}",
            problems,
        )
        for value in stated:
            if value != length:
                problems.append(
                    f"DUTCH-005_YOUTUBE.md says pinned comment {index} is {value}, it is {length}"
                )

    print(f"Telegram post: {tg_len} visible characters")
    for value in claimed([r"Длина: \*\*(\d+)\*\* видимых знаков"], tg, "DUTCH-005_TELEGRAM.md", problems):
        if value != tg_len:
            problems.append(f"DUTCH-005_TELEGRAM.md says the post is {value}, it is {tg_len}")

    if desc > YT_LIMIT:
        problems.append(f"YouTube description is {desc} characters, over the {YT_LIMIT} limit")
    if tg_len > TG_LIMIT:
        problems.append(f"Telegram post is {tg_len} visible characters, over the {TG_LIMIT} limit")

    for problem in problems:
        print(f"FAIL: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
