#!/usr/bin/env python3
"""Check the title separator rule for the hymns channel.

Owner decision, 2026-10-26: hymns and songs are separated in a YouTube title by the
sign U+271D (✝) — part · ✝ · «title» · ✝ · author. No other separator is allowed in
a title: not ✦ (the earlier placeholder), not a pipe, not a bullet, not a long dash.

This gate reads the title block of DUTCH-005_YOUTUBE.md (the fenced one-line blocks
between "## 1. Название" and "## 2."), and fails if

- a title has no ✝,
- a title contains ✦, "|", "•" or " — ",
- a title does not carry the approved name in guillemets,
- a title is longer than YouTube's 100-character limit,
- ✦ survives anywhere in the copy files at all.

Run: python3 SUNO_HYMNS/scripts/check_title_separator.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUNO = ROOT / "SUNO_HYMNS" / "SUNO"
CROSS = "\u271d"   # ✝
STAR = "\u2726"    # ✦ — retired
APPROVED_NAME = "«Хвала Славе»"
TITLE_LIMIT = 100


def main() -> int:
    problems: list[str] = []

    src = (SUNO / "DUTCH-005_YOUTUBE.md").read_text(encoding="utf-8")
    if "## 1." not in src or "## 2." not in src:
        print("FAIL: title section markers not found in DUTCH-005_YOUTUBE.md")
        return 1
    section = src.split("## 1.", 1)[1].split("## 2.", 1)[0]
    titles = [block.strip() for block in re.findall(r"```text\n(.*?)\n```", section, re.S)]
    if not titles:
        print("FAIL: no title candidates found in the title section")
        return 1

    for title in titles:
        label = title[:60]
        if len(title.splitlines()) != 1:
            problems.append(f"title is not a single line: {label}")
        if CROSS not in title:
            problems.append(f"title has no ✝ separator: {label}")
        for banned in (STAR, "|", "•", " — "):
            if banned in title:
                problems.append(f"title uses a forbidden separator {banned!r}: {label}")
        if APPROVED_NAME not in title:
            problems.append(f"title does not carry the approved name {APPROVED_NAME}: {label}")
        if len(title) > TITLE_LIMIT:
            problems.append(f"title is {len(title)} characters, over the {TITLE_LIMIT} limit: {label}")

    for name in ("DUTCH-005_YOUTUBE.md", "DUTCH-005_TELEGRAM.md", "DUTCH-005_PINNED.md"):
        text = (SUNO / name).read_text(encoding="utf-8")
        if STAR in text:
            problems.append(f"{name}: contains ✦ — the retired separator")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        return 1

    print(f"title separator: clean — {len(titles)} title candidate(s), all using ✝")
    return 0


if __name__ == "__main__":
    sys.exit(main())
