#!/usr/bin/env python3
"""Catch the drift that the registry validator does not look for.

`validate_project_registry.py` proves that the JSON and the Markdown agree on
*structure* — ids, states, prompt identity. It does not notice that four prose
documents still describe the previous revision of a lyric, or that a document
says "five stress marks" while the shipped file carries four. Those were the
two real defects this project produced in one session, and both were found by
the owner rather than by a check.

This script compares the *prose* against the *files*:

1. **Revision drift.** For every work whose catalog entry carries a
   `versionId`, the current revision must be named in the four documents that
   are supposed to track it, and no other revision of that work may appear in
   them — except on a line that is explicitly historical (contains
   `changelog`, `replaces`, `replaced`, `retired` or `superseded`).
2. **Count drift.** Any phrase of the form "four stress marks" / "5 accents"
   in a document that describes a lyric must equal the number of distinct
   accented words actually present in the SUNO lyric.
3. **Duplicated sentence.** An identical sentence twice in a row is the
   residue of an edit applied twice; it has happened here.

Read-only, stdlib only. Exit 1 on any finding.
Usage:  python3 scripts/check_revision_consistency.py
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ACCENT = "\u0301"

# Documents that must carry the current revision, per work.
TRACKING_DOCS = (
    "SUNO/LYRIC_REGISTER.md",
    "SUNO/PROMPT_AND_VERSION_REGISTER.md",
    "SUNO/STATUS_LEDGER.md",
)

# Words that mark a line as describing history rather than the current state.
# A stale revision may legitimately appear on a line that marks it as past or
# hypothetical — a changelog row, a "replaces" note, or a named alternative the
# owner might still choose. Anywhere else it is drift.
HISTORICAL = (
    "changelog", "replaces", "replaced", "retired", "superseded", "rolled back",
    "alternative", "if the owner", "would become", "must then be recorded",
)

NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
}

STRESS_RE = re.compile(
    r"\b(" + "|".join(sorted(NUMBERS, key=len, reverse=True)) + r")\s+"
    r"(?:distinct\s+)?(?:acute\s+)?(?:stress\s+marks?|accents?|accented\s+words)\b",
    re.IGNORECASE,
)

SHARED_DOCS = {"LYRIC_REGISTER.md", "STATUS_LEDGER.md"}

SENTENCE_RE = re.compile(r"[^.!?]+[.!?]")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def accented_words(text: str) -> set[str]:
    """Distinct words carrying a combining acute, normalised for comparison.

    `re`\'s \\w does not include combining marks, so a word such as
    `соединена́` is split into fragments by any word-shaped pattern. Split on
    whitespace and punctuation instead, then test each token for the mark.
    """
    words = set()
    for token in re.split(r"[\s\.,;:!?—–\-\(\)«»\"'\[\]…]+", text):
        token = token.strip()
        if token and ACCENT in unicodedata.normalize("NFD", token):
            words.add(unicodedata.normalize("NFC", token).lower())
    return words


def version_ids(catalog: dict) -> dict[str, tuple[str, str, str]]:
    """work id -> (current versionId, work-version prefix, numeric revision)."""
    out = {}
    for work in catalog.get("works", []):
        versions = work.get("versions") or []
        if not versions:
            continue
        current = versions[-1]["versionId"]
        match = re.match(r"(.+?)[-_ ]v(\d+\.\d+)$", current)
        if not match:
            continue
        out[work["id"]] = (current, match.group(1), match.group(2))
    return out


def check_revisions(catalog: dict, findings: list[str]) -> None:
    for work_id, (current, prefix, revision) in version_ids(catalog).items():
        package = f"SUNO/{work_id}_PRODUCTION_PACKAGE.md"
        docs = list(TRACKING_DOCS)
        if (ROOT / package).exists():
            docs.append(package)

        for doc in docs:
            path = ROOT / doc
            if not path.exists():
                findings.append(f"{doc}: listed as a tracking document but missing")
                continue
            text = read(path)
            # The version is written both as `DUTCH-005-RU v0.8` and as
            # `DUTCH-005-RU-v0.8`. Either spelling satisfies the requirement.
            if not re.search(re.escape(prefix) + r"[-_ ]v" + re.escape(revision), text):
                findings.append(
                    f"{doc}: does not name the current revision {current}"
                )
            for line_no, line in enumerate(text.splitlines(), 1):
                if any(marker in line.lower() for marker in HISTORICAL):
                    continue
                found = re.findall(
                    re.escape(prefix) + r"[-_ ]v(\d+\.\d+)", line
                )
                stale = {v for v in found if v != revision}
                if stale:
                    findings.append(
                        f"{doc}:{line_no}: names stale revision(s) "
                        f"{', '.join(sorted(stale))} for {work_id} "
                        f"(current is {revision})"
                    )


LYRIC_BLOCK = re.compile(r"```[a-z]*\n(\[Intro\].*?)```", re.DOTALL)


def check_counts(findings: list[str]) -> None:
    """Declared stress-mark counts must match the shipped SUNO lyric.

    Only the fenced performable block counts: the surrounding prose in the same
    file discusses marks and would inflate the total.
    """
    for lyric in sorted((ROOT / "SUNO").glob("*_LYRICS_SUNO.md")):
        work_prefix = lyric.name.split("_")[0]
        block = LYRIC_BLOCK.search(read(lyric))
        if not block:
            findings.append(f"{lyric.name}: no fenced lyric block starting with [Intro]")
            continue
        actual = accented_words(block.group(1))
        docs = [lyric, ROOT / f"SUNO/{work_prefix}_PRODUCTION_PACKAGE.md",
                ROOT / "SUNO/LYRIC_REGISTER.md", ROOT / "SUNO/STATUS_LEDGER.md"]
        for doc in docs:
            if not doc.exists():
                continue
            for line_no, line in enumerate(read(doc).splitlines(), 1):
                # Shared registers list several works, so the line must say
                # which; a work's own package and lyric need no prefix.
                if doc.name in SHARED_DOCS and work_prefix not in line:
                    continue
                for phrase in STRESS_RE.finditer(line):
                    declared = NUMBERS[phrase.group(1).lower()]
                    if declared != len(actual):
                        findings.append(
                            f"{doc.relative_to(ROOT)}:{line_no}: says "
                            f"'{phrase.group(0)}' but {lyric.name} carries "
                            f"{len(actual)} ({', '.join(sorted(actual))})"
                        )


def check_duplicate_sentences(findings: list[str]) -> None:
    for path in sorted((ROOT / "SUNO").glob("*.md")):
        sentences = [s.strip() for s in SENTENCE_RE.findall(read(path)) if s.strip()]
        for first, second in zip(sentences, sentences[1:]):
            if first == second and len(first) > 20:
                findings.append(
                    f"{path.relative_to(ROOT)}: the sentence "
                    f"'{first[:60]}…' appears twice in a row"
                )


def main() -> int:
    catalog = json.loads(read(ROOT / "data/track-catalog-v1.json"))
    findings: list[str] = []
    check_revisions(catalog, findings)
    check_counts(findings)
    check_duplicate_sentences(findings)

    if findings:
        print(f"revision consistency: {len(findings)} finding(s)\n")
        for item in findings:
            print(f"  - {item}")
        return 1
    print("revision consistency: clean — versions, declared counts and sentences agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
