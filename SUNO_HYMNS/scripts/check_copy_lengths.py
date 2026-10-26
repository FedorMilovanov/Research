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

- description: the sentence "<N> знак/знака/знаков, до лимита 5000" and the checklist line
  "- [x] <N> знаков;" of DUTCH-005_YOUTUBE.md;
- pinned comments: "Закреп 1 … <N> знаков" and "Закреп 2 … <N> знаков" in § 3 of
  the same file, against the two fenced blocks of DUTCH-005_PINNED.md;
- every document that describes the present state of the copy must quote the current
  description length; the review log is exempt because it records the past;
- Telegram: "Длина: **<N>** видимых знаков" in DUTCH-005_TELEGRAM.md, against the
  post text with markup characters stripped;
- the description's own range: the channel's rule sheet allows 3500-4600
  characters, not merely the platform's 5000. That upper bound was broken for a
  whole pass (4881) while this gate said nothing, because it only knew the
  platform limit.

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

# projects/lord-god-strength/RULES.md § 4: «Объём 3500–4600 знаков (лимит площадки 5000)».
# The platform limit is not the channel's limit; a description can be legal and wrong.
DESC_MIN = 3500
DESC_MAX = 4600


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


def extra_telegram_posts() -> list[tuple[str, int, int | None]]:
    """Every other Telegram post file: (label, visible length, stated length).

    DUTCH-005_TELEGRAM.md is excluded because it has its own extraction rule
    above. Any new Telegram file drops in here with no change to this script,
    which is the point: a hand-typed length is a length waiting to go stale.
    """
    out: list[tuple[str, int, int | None]] = []
    for path in sorted(SUNO.glob("*TELEGRAM*.md")):
        if path.name == "DUTCH-005_TELEGRAM.md":
            continue
        src = path.read_text(encoding="utf-8")
        for index, block in enumerate(re.findall(r"```text\n(.*?)\n```", src, re.S), 1):
            label = f"{path.name} — сообщение {index}"
            # the number is bolded, so the closing ** has to be allowed between
            # the digits and the word that follows
            stated = re.search(rf"Сообщение {index}[^\n]*?(\d+)\*{{0,2}} знаков", src)
            out.append(
                (label, len(re.sub(r"\*", "", block)), int(stated.group(1)) if stated else None)
            )
    return out


def claimed(patterns: list[str], text: str, label: str, problems: list[str]) -> list[int]:
    found: list[int] = []
    for pattern in patterns:
        match = re.search(pattern, text)
        if match is None:
            problems.append(f"{label}: the document no longer states its length ({pattern})")
        else:
            found.append(int(match.group(1)))
    return found


DESCRIPTION_QUOTERS = [
    "SUNO_HYMNS/README.md",
    "SUNO_HYMNS/HANDOFF_FOR_NEXT_AGENT.md",
    "SUNO_HYMNS/SUNO/DUTCH-005_YOUTUBE.md",
    "SUNO_HYMNS/SUNO/STATUS_LEDGER.md",
    "SUNO_HYMNS/SUNO/NEXT_STEPS.md",
]


def check_quoted_description_lengths(actual: int, problems: list[str]) -> None:
    """Every document that quotes the description length must quote the current one.

    The documents listed above describe the *present* state; the review log does not,
    because it records what the numbers used to be. A number in those files next to
    the word 'description' therefore has to equal what the block measures now.
    """
    pattern = re.compile(r"(\d{3,5})[- ]?(?:character|знач\w*)", re.IGNORECASE)
    for name in DESCRIPTION_QUOTERS:
        path = ROOT / name
        if not path.exists():
            problems.append(f"{name}: listed as a description-length quoter but missing")
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if "description" not in line.lower() and "описан" not in line.lower():
                continue
            for number in pattern.findall(line):
                if int(number) != actual and int(number) > 1000:
                    problems.append(
                        f"{name}:{line_no}: quotes {number} characters for the description, it is {actual}"
                    )


def main() -> int:
    problems: list[str] = []

    yt = (SUNO / "DUTCH-005_YOUTUBE.md").read_text(encoding="utf-8")
    tg = (SUNO / "DUTCH-005_TELEGRAM.md").read_text(encoding="utf-8")

    desc = len(description())
    pins = [len(block) for block in pinned()]
    tg_len = len(telegram_visible())

    print(f"description: {desc} characters")
    margin = re.search(r"до лимита (\d+) остаётся (\d+)", yt)
    if margin:
        limit, stated = int(margin.group(1)), int(margin.group(2))
        if limit - desc != stated:
            problems.append(
                f"DUTCH-005_YOUTUBE.md: margin to the {limit}-character limit is stated as {stated}, it is {limit - desc}"
            )

    check_quoted_description_lengths(desc, problems)
    for value in claimed(
        [r"(\d+)\s*знак\w*, до лимита 5000", r"- \[x\] (\d+) знак"],
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

    for label, actual, stated in extra_telegram_posts():
        print(f"{label}: {actual} visible characters")
        if stated is None:
            problems.append(f"{label}: the document does not state its length")
        elif stated != actual:
            problems.append(f"{label}: states {stated} characters, it is {actual}")
        if actual > TG_LIMIT:
            problems.append(f"{label}: {actual} characters, over the {TG_LIMIT} limit")

    if desc > YT_LIMIT:
        problems.append(f"YouTube description is {desc} characters, over the {YT_LIMIT} limit")
    if desc > DESC_MAX:
        problems.append(
            f"YouTube description is {desc} characters, over the channel range of {DESC_MIN}-{DESC_MAX}"
        )
    if desc < DESC_MIN:
        problems.append(
            f"YouTube description is {desc} characters, under the channel range of {DESC_MIN}-{DESC_MAX}"
        )
    if tg_len > TG_LIMIT:
        problems.append(f"Telegram post is {tg_len} visible characters, over the {TG_LIMIT} limit")

    for problem in problems:
        print(f"FAIL: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
