#!/usr/bin/env python3
"""Validate the versioned Heart current citation state V4."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v4-2026-08-04.json"
PREVIOUS = ROOT / "data/heart-entry-citation-pass-current-v3-2026-08-04.json"
DELTA = ROOT / "data/heart-i1-citation-review-2026-08-04.json"
ASSEMBLY = ROOT / "data/heart-i1-reader-assembly-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/108_ENTRY_CITATION_PASS_CURRENT_V4_2026-08-04.md"

PREVIOUS_BLOB = "407c8d78baa966a3336e7bd60edfa51178b74f32"
DELTA_BLOB = "bb7c20c740aed7fadc181ee3f5e3b79951580edf"
ASSEMBLY_BLOB = "e4b805585fbe9606efb5ed4c59861d52ec08c699"
EXPECTED_COMPLETE = {
    "HEART-BOOK-I1", "HEART-BOOK-I2", "HEART-BOOK-I4", "HEART-BOOK-III3",
    "HEART-BOOK-X1", "HEART-BOOK-X2", "HEART-BOOK-X3",
}
EXPECTED_OPEN = {
    "HEART-BOOK-I3", "HEART-BOOK-II", "HEART-BOOK-III1", "HEART-BOOK-III2",
    "HEART-BOOK-III4", "HEART-BOOK-IV", "HEART-BOOK-V", "HEART-BOOK-VI",
    "HEART-BOOK-VII", "HEART-BOOK-VIII", "HEART-BOOK-IX",
}
EXPECTED_PRODUCT = {
    "HEART-BOOK-I3", "HEART-BOOK-III1", "HEART-BOOK-III4", "HEART-BOOK-V", "HEART-BOOK-VII",
}
EXPECTED_DOSSIER = {
    "HEART-BOOK-II", "HEART-BOOK-III2", "HEART-BOOK-IV", "HEART-BOOK-VI", "HEART-BOOK-VIII", "HEART-BOOK-IX",
}
EXPECTED_COUNTS = {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 7,
    "entryCitationPassOpen": 11,
    "assembledReaderEntries": 7,
    "assembledReaderCitationReviewsComplete": 7,
    "missingStandaloneFinalReaders": 11,
    "productSourceOnlyEntries": 5,
    "researchDossierOnlyEntries": 6,
    "newDirectQuotesApproved": 0,
}
errors: list[str] = []


def require(value: bool, message: str) -> None:
    if not value:
        errors.append(message)


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be a JSON object")
    return value if isinstance(value, dict) else {}


def blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


for path, expected in ((PREVIOUS, PREVIOUS_BLOB), (DELTA, DELTA_BLOB), (ASSEMBLY, ASSEMBLY_BLOB)):
    require(path.is_file(), f"immutable authority missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(path) == expected, f"immutable authority blob drift: {path.relative_to(ROOT)}")

previous = read_json(PREVIOUS)
delta = read_json(DELTA)
assembly = read_json(ASSEMBLY)
current = read_json(CURRENT)

require(previous.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V3-2026-08-04", "previous authority drift")
require(previous.get("currentCounts") == {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 6,
    "entryCitationPassOpen": 12,
    "assembledReaderEntries": 6,
    "assembledReaderCitationReviewsComplete": 6,
    "missingStandaloneFinalReaders": 12,
    "productSourceOnlyEntries": 6,
    "researchDossierOnlyEntries": 6,
    "newDirectQuotesApproved": 0,
}, "historical V3 count drift")
require(set(previous.get("completedEntryIds", [])) == EXPECTED_COMPLETE - {"HEART-BOOK-I1"}, "historical V3 completed set drift")
require(set(previous.get("openEntryIds", [])) == EXPECTED_OPEN | {"HEART-BOOK-I1"}, "historical V3 open set drift")

require(delta.get("authorityId") == "HEART-I1-CITATION-REVIEW-2026-08-04", "I.1 delta authority drift")
require(delta.get("entry", {}).get("id") == "HEART-BOOK-I1", "I.1 delta entry drift")
require(delta.get("effectiveState") == {
    "entryId": "HEART-BOOK-I1",
    "previous": "ASSEMBLED_READER_CITATION_OPEN",
    "current": "ENTRY_CITATION_PASS_COMPLETE",
}, "I.1 delta transition drift")
require(delta.get("effectiveCounts", {}).get("entryCitationPassComplete") == 7, "I.1 delta completion count drift")
require(delta.get("effectiveCounts", {}).get("assembledReader") == 7, "I.1 delta reader count drift")
require(delta.get("disposition", {}).get("newDirectQuotesApproved") == 0, "I.1 delta direct quote drift")
require(delta.get("publicationBoundary", {}).get("i1EntryCitationPassComplete") is True, "I.1 delta pass incomplete")
require(delta.get("publicationBoundary", {}).get("wholeBookCitationPassComplete") is False, "I.1 delta falsely closes whole-book pass")

require(assembly.get("authorityId") == "HEART-I1-READER-ASSEMBLY-2026-08-04", "I.1 assembly authority drift")
require(assembly.get("effectiveCounts", {}).get("assembledReader") == 7, "I.1 assembly count drift")
require(assembly.get("effectiveCounts", {}).get("entryCitationPassComplete") == 6, "I.1 assembly must preserve pre-review count")

require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V4-2026-08-04", "V4 authority drift")
require(current.get("status") == "SEVEN_ENTRY_PASSES_COMPOSED_ALL_SEVEN_READERS_REVIEWED_ELEVEN_READERS_OPEN", "V4 status drift")
prev_ref = current.get("previousCurrentAuthority", {})
require(prev_ref.get("gitBlob") == PREVIOUS_BLOB, "V4 previous blob drift")
require(prev_ref.get("authorityId") == previous.get("authorityId"), "V4 previous authority mismatch")
delta_ref = current.get("deltaReceipt", {})
require(delta_ref.get("gitBlob") == DELTA_BLOB, "V4 delta blob drift")
require(delta_ref.get("authorityId") == delta.get("authorityId"), "V4 delta authority mismatch")
require(delta_ref.get("readerAssemblyGitBlob") == ASSEMBLY_BLOB, "V4 assembly blob drift")
require(delta_ref.get("id") == "HEART-BOOK-I1", "V4 delta ID drift")
require(delta_ref.get("composedCountAfterReceipt") == "7 / 18", "V4 delta count drift")
require(delta_ref.get("newDirectQuotesApproved") == 0, "V4 delta quote boundary drift")
require(current.get("currentCounts") == EXPECTED_COUNTS, "V4 count block drift")
require(set(current.get("completedEntryIds", [])) == EXPECTED_COMPLETE, "V4 completed set drift")
require(set(current.get("openEntryIds", [])) == EXPECTED_OPEN, "V4 open set drift")
lanes = current.get("openEntriesBySourceLane", {})
require(set(lanes.get("productSourceOnly", [])) == EXPECTED_PRODUCT, "V4 Product lane drift")
require(set(lanes.get("researchDossierOnly", [])) == EXPECTED_DOSSIER, "V4 dossier lane drift")
require(EXPECTED_PRODUCT | EXPECTED_DOSSIER == EXPECTED_OPEN, "V4 lanes not exhaustive")
require(EXPECTED_PRODUCT & EXPECTED_DOSSIER == set(), "V4 lanes overlap")
backlog = current.get("readerAssemblyBacklog", {})
require(backlog.get("removedByDelta") == "HEART-BOOK-I1", "V4 removed delta drift")
require(set(backlog.get("remaining", [])) == EXPECTED_OPEN, "V4 remaining-reader set drift")
require(backlog.get("effectiveMissingStandaloneFinalReaders") == 11, "V4 remaining-reader count drift")
boundary = current.get("publicationBoundary", {})
require(boundary.get("allCurrentlyAssembledReadersReviewed") is True, "V4 assembled-reader review state drift")
for key in (
    "wholeBookReaderAssemblyComplete", "wholeBookCitationPassComplete",
    "wholeBookTransitionDedupPassComplete", "wholeBookLineEditComplete",
    "manuscriptBundleComplete", "productReleaseComplete",
):
    require(boundary.get(key) is False, f"V4 falsely closes {key}")
require(boundary.get("newDirectQuotesApproved") == 0, "V4 direct quote boundary drift")
next_tx = current.get("nextTransaction", {})
require(next_tx.get("type") == "STANDALONE_READER_ASSEMBLY", "V4 next transaction type drift")
require(next_tx.get("preferredEntryId") == "HEART-BOOK-I3", "V4 next entry drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-ENTRY-CITATION-PASS-CURRENT-V4-2026-08-04",
    "ENTRY CITATION PASSES COMPLETE = 7 / 18",
    "ENTRY CITATION PASSES OPEN = 11 / 18",
    "ASSEMBLED READERS = 7 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 7 / 7",
    "MISSING STANDALONE FINAL READERS = 11",
    "PRODUCT SOURCE ONLY = 5",
    "RESEARCH DOSSIER ONLY = 6",
    "NEXT READER ASSEMBLY = HEART-BOOK-I3",
    PREVIOUS_BLOB, DELTA_BLOB,
):
    require(marker in human, f"V4 human authority marker missing: {marker}")
for forbidden in (
    "ENTRY CITATION PASSES COMPLETE = 18 / 18",
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "WHOLE-BOOK READER ASSEMBLY = COMPLETE",
    "PRODUCT RELEASE = COMPLETE", "TODO", "TBD",
):
    require(forbidden not in human, f"V4 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart entry citation pass current V4: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Heart entry citation pass current V4: PASS — 7/18 completed, 11 open, reviews 7/7, backlog 11 = 5 Product + 6 dossier, next I.3")
