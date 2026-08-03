#!/usr/bin/env python3
"""Validate Heart reader chapters assembled from the three P0 dossiers."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/heart-reader-assembly-2026-08-02.json"
DECISIONS = ROOT / "СЕРИЯ СЕРДЦЕ/82_BOOK_ASSEMBLY_DECISIONS_2026-08-02.md"
EVIDENCE = ROOT / "data/heart-p0-architecture-dossiers-2026-08-02.json"
EXPECTED = {
    "HEART-READER-I2": ("I.2", "EDEN-01…EDEN-08", "СЕРИЯ СЕРДЦЕ/79_READER_CHAPTER_I2_HEART_IN_EDEN_2026-08-02.md"),
    "HEART-READER-III3": ("III.3", "REP-01…REP-08", "СЕРИЯ СЕРДЦЕ/80_READER_CHAPTER_III3_BROKEN_HEART_REPENTANCE_2026-08-02.md"),
    "HEART-READER-X1": ("X.1", "JUDG-01…JUDG-10", "СЕРИЯ СЕРДЦЕ/81_READER_CHAPTER_X1_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md"),
}
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)}: object required")
        return {}
    return value


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return ""


def words(text: str) -> int:
    # Count ordinary alphabetic word tokens, including one-letter Russian
    # conjunctions and prepositions. Excluding them made the 1500-word floor
    # depend on word length rather than the actual chapter word count.
    return len(re.findall(r"[A-Za-zА-Яа-яЁё]+", text))


registry = load(REGISTRY)
evidence = load(EVIDENCE)
require(registry.get("schemaVersion") == 1, "reader assembly schema drift")
require(registry.get("authorityId") == "HEART-READER-ASSEMBLY-2026-08-02", "reader assembly authority drift")
require(registry.get("status") == "CURRENT_THREE_CHAPTERS_ASSEMBLED_BOOK_DECISIONS_CLOSED", "reader assembly status drift")
require(registry.get("evidenceAuthorityId") == "HEART-P0-ARCHITECTURE-CLOSURE-2026-08-02", "evidence authority pointer drift")
require(registry.get("newDirectQuotesApproved") == 0, "new direct quote count must remain zero")
require(evidence.get("counts", {}).get("claims") == 26, "P0 evidence registry claim count drift")

chapters = registry.get("chapters")
require(isinstance(chapters, list) and len(chapters) == 3, "exactly three reader chapters required")
chapters = chapters if isinstance(chapters, list) else []
ids: list[str] = []
for row in chapters:
    require(isinstance(row, dict), "reader chapter object required")
    if not isinstance(row, dict):
        continue
    chapter_id = str(row.get("id", ""))
    ids.append(chapter_id)
    require(chapter_id in EXPECTED, f"unexpected reader chapter: {chapter_id}")
    if chapter_id not in EXPECTED:
        continue
    chapter, claim_range, path_raw = EXPECTED[chapter_id]
    require(row.get("chapter") == chapter, f"{chapter_id}: chapter number drift")
    require(row.get("claimRange") == claim_range, f"{chapter_id}: claim range drift")
    require(row.get("path") == path_raw, f"{chapter_id}: path drift")
    require(row.get("status") == "READER_CHAPTER_ASSEMBLED", f"{chapter_id}: status drift")
    path = ROOT / path_raw
    require(path.is_file(), f"{chapter_id}: reader file missing")
    chapter_text = read(path)
    require("HEART-READER-ASSEMBLY-2026-08-02" in chapter_text, f"{chapter_id}: authority marker missing")
    require(claim_range in chapter_text, f"{chapter_id}: claim range marker missing")
    require("Новые прямые цитаты:** `0`" in chapter_text, f"{chapter_id}: zero-direct-quote marker missing")
    require(words(chapter_text) >= 1500, f"{chapter_id}: reader chapter below 1500-word assembly floor")
    require("## Для размышления" in chapter_text, f"{chapter_id}: reflection section missing")
    require("## Переход" in chapter_text, f"{chapter_id}: transition section missing")
    for forbidden in ("TODO", "TBD", "PUBLICATION_HOLD", "SOURCE NEEDED", "FIXME"):
        require(forbidden not in chapter_text, f"{chapter_id}: unresolved marker remains: {forbidden}")
    require("<blockquote" not in chapter_text and "<q" not in chapter_text, f"{chapter_id}: direct-quote HTML markup forbidden")

require(set(ids) == set(EXPECTED), "reader chapter set drift")
require(len(ids) == len(set(ids)), "duplicate reader chapter IDs")

editorial = registry.get("editorialDecisions", {})
require(editorial.get("r9", {}).get("decision") == "RETAIN_AS_STANDALONE_CHRISTOLOGICAL_BRIDGE", "R9 decision drift")
require(editorial.get("katoptrizomenoi", {}).get("decision") == "BOUNDED_EXCURSUS_INSIDE_R8", "katoptrizomenoi decision drift")
require(editorial.get("directQuotes", {}).get("decision") == "NO_NEW_DIRECT_QUOTES", "direct-quote decision drift")
require(len(editorial.get("deduplication", {})) == 4, "deduplication owner set drift")

order = registry.get("finalBookOrder")
require(isinstance(order, list) and len(order) == 18, "final book order must contain 18 entries")
if isinstance(order, list):
    require(len(order) == len(set(order)), "final book order entries must be unique")
    require(order[1].startswith("I.2"), "I.2 placement drift")
    require(order[7].startswith("III.3"), "III.3 placement drift")
    require(order[14].startswith("IX"), "R9/Part IX placement drift")
    require(order[15].startswith("X.1"), "X.1 placement drift")

boundary = registry.get("publicationBoundary", {})
require(boundary == {
    "researchComplete": True,
    "threeReaderChaptersAssembled": True,
    "finalOrderDecided": True,
    "wholeBookLineEditComplete": False,
    "wholeBookCitationPassComplete": False,
    "productReleaseComplete": False,
}, "reader/publication boundary drift")
require(registry.get("counts") == {
    "readerChapters": 3,
    "evidenceClaimsComposed": 26,
    "editorialDecisions": 4,
    "finalBookEntries": 18,
    "newDirectQuotesApproved": 0,
}, "reader assembly counts drift")

decisions = read(DECISIONS)
for marker in (
    "HEART-READER-ASSEMBLY-2026-08-02",
    "THREE P0 READER CHAPTERS = ASSEMBLED",
    "R9 ROLE = CLOSED",
    "KATOPTRIZOMENOI ROLE = CLOSED",
    "FINAL ORDER = CLOSED",
    "PRODUCT RELEASE = NOT CLAIMED",
):
    require(marker in decisions, f"assembly decisions missing marker: {marker}")
for forbidden in ("TODO", "TBD", "PUBLICATION_HOLD"):
    require(forbidden not in decisions, f"assembly decisions contain unresolved marker: {forbidden}")

if errors:
    print(f"Heart reader assembly: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart reader assembly: PASS — 3 chapters, 26 claims composed, 18-entry order, 0 new direct quotes")
