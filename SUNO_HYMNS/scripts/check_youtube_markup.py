#!/usr/bin/env python3
"""Catch the one markup defect that broke a live YouTube description.

YouTube Studio's bold works as `*bold*`, and the channel standard
(`video-channel-manager/docs/youtube-description-rendering-standard.md` § 3.1)
requires the punctuation to go **inside** the wrapper when it belongs to the
wrapped phrase: `*«Uyt-spanningen»,* вышедший…`. With the comma left outside —
`*Uyt-spanningen*, вышедший` — the closing asterisk does not close: it prints
literally, the bold runs on to the next asterisk, and the paragraph cascades.

So the mechanical rule is narrow and checkable:

    a closing `*` or `_` must be followed by a space, or by end of line.

This script fails on any wrapper that closes against punctuation, on stray
asterisks, on Markdown links and HTML, and on markup in the first paragraph
(which is the part YouTube shows collapsed). It reads a description body from a
file or from stdin.

Read-only. Usage:
    python3 scripts/check_youtube_markup.py path/to/description.txt
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BOLD = re.compile(r"\*([^*\n]+)\*")
ITALIC_LINE = re.compile(r"(?m)^_([^_\n]+)_$")


def check(text: str) -> list[str]:
    problems: list[str] = []

    for match in BOLD.finditer(text):
        after = text[match.end():match.end() + 1]
        if after not in (" ", "\n", ""):
            problems.append(
                f"closing * followed by {after!r} — move the punctuation inside "
                f"the wrapper: {match.group(0)[:60]!r}"
            )

    leftover = BOLD.sub("", text)
    if "*" in leftover:
        i = leftover.index("*")
        problems.append(
            f"stray asterisk near: {leftover[max(0, i - 50):i + 50]!r}"
        )

    for match in re.finditer(r"(?m)^_([^_\n]+)_", text):
        after = text[match.end():match.end() + 1]
        if after not in ("\n", ""):
            problems.append(
                f"italic line does not end after its underscore: "
                f"{match.group(0)[:60]!r}"
            )

    for bad, why in (
        ("**", "double asterisks: YouTube prints them literally"),
        ("](", "Markdown link: paste the raw URL instead"),
        ("<b>", "HTML tag in a description"),
        ("<i>", "HTML tag in a description"),
    ):
        if bad in text:
            problems.append(f"{bad!r} found — {why}")

    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    if paragraphs and re.search(r"[*_]", paragraphs[0]):
        problems.append("the first paragraph carries markup; it shows collapsed")

    return problems


def main() -> int:
    if len(sys.argv) > 1:
        text = Path(sys.argv[1]).read_text(encoding="utf-8")
        where = sys.argv[1]
    else:
        text = sys.stdin.read()
        where = "<stdin>"

    problems = check(text)
    if problems:
        print(f"{where}: {len(problems)} problem(s)")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(
        f"{where}: clean — {len(text)} chars, "
        f"{len(BOLD.findall(text))} bold span(s), "
        f"{len(ITALIC_LINE.findall(text))} italic line(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
