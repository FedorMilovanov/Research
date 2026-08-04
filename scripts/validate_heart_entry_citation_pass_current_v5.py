#!/usr/bin/env python3
"""Validate the versioned Heart current citation state V5."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v5-2026-08-04.json"
PREVIOUS = ROOT / "data/heart-entry-citation-pass-current-v4-2026-08-04.json"
DELTA = ROOT / "data/heart-i3-citation-review-2026-08-04.json"
ASSEMBLY = ROOT / "data/heart-i3-reader-assembly-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/112_ENTRY_CITATION_PASS_CURRENT_V5_2026-08-04.md"

PREVIOUS_BLOB = "d0ddea6cf1fc33dfab53ae9691aaf2d903d03b73"
DELTA_BLOB = "b753e0e407bf881bc49974954b452817a99f1730"
ASSEMBLY_BLOB = "2ae5a01ed0a2c9931b7a36f4991cf93bcec3fb7a"
EXPECTED_COMPLETE = {
    "HEART-BOOK-I1", "HEART-BOOK-I2", "HEART-BOOK-I3", "HEART-BOOK-I4",
    "HEART-BOOK-III3", "HEART-BOOK-X1", "HEART-BOOK-X2", "HEART-BOOK-X3",
}
EXPECTED_OPEN = {
    "HEART-BOOK-II", "HEART-BOOK-III1", "HEART-BOOK-III2", "HEART-BOOK-III4",
    "HEART-BOOK-IV", "HEART-BOOK-V", "HEART-BOOK-VI", "HEART-BOOK-VII",
    "HEART-BOOK-VIII", "HEART-BOOK-IX",
}
EXPECTED_PRODUCT = {
    "HEART-BOOK-III1", "HEART-BOOK-III4", "HEART-BOOK-V", "HEART-BOOK-VII",
}
EXPECTED_DOSSIER = {
    "HEART-BOOK-II", "HEART-BOOK-III2", "HEART-BOOK-IV",
    "HEART-BOOK-VI", "HEART-BOOK-VIII", "HEART-BOOK-IX",
}
EXPECTED_COUNTS = {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 8,
    "entryCitationPassOpen": 10,
    "assembledReaderEntries": 8,
    "assembledReaderCitationReviewsComplete": 8,
    "missingStandaloneFinalReaders": 10,
    "productSourceOnlyEntries": 4,
    "researchDossierOnlyEntries": 6,
    "productSourceLinkRepairsRequired": 3,
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

require(previous.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V4-2026-08-04", "previous authority drift")
previous_counts = previous.get("currentCounts", {})
require(previous_counts.get("entryCitationPassComplete") == 7, "historical V4 completion count drift")
require(previous_counts.get("entryCitationPassOpen") == 11, "historical V4 open count drift")
require(previous_counts.get("assembledReaderEntries") == 7, "historical V4 reader count drift")
require(previous_counts.get("assembledReaderCitationReviewsComplete") == 7, "historical V4 review count drift")
require(previous_counts.get("missingStandaloneFinalReaders") == 11, "historical V4 backlog count drift")
require(previous_counts.get("productSourceOnlyEntries") == 5, "historical V4 Product lane drift")
require(previous_counts.get("researchDossierOnlyEntries") == 6, "historical V4 dossier lane drift")
require(set(previous.get("completedEntryIds", [])) == EXPECTED_COMPLETE - {"HEART-BOOK-I3"}, "historical V4 completed set drift")
require(set(previous.get("openEntryIds", [])) == EXPECTED_OPEN | {"HEART-BOOK-I3"}, "historical V4 open set drift")

require(delta.get("authorityId") == "HEART-I3-CITATION-REVIEW-2026-08-04", "I.3 delta authority drift")
require(delta.get("entry", {}).get("id") == "HEART-BOOK-I3", "I.3 delta entry drift")
require(delta.get("effectiveState") == {
    "entryId": "HEART-BOOK-I3",
    "previous": "ASSEMBLED_READER_CITATION_OPEN",
    "current": "ENTRY_CITATION_PASS_COMPLETE",
}, "I.3 delta transition drift")
require(delta.get("effectiveCounts", {}).get("entryCitationPassComplete") == 8, "I.3 delta completion count drift")
require(delta.get("effectiveCounts", {}).get("assembledReader") == 8, "I.3 delta reader count drift")
require(delta.get("disposition", {}).get("newDirectQuotesApproved") == 0, "I.3 delta direct quote drift")
require(delta.get("publicationBoundary", {}).get("i3EntryCitationPassComplete") is True, "I.3 delta pass incomplete")
require(delta.get("publicationBoundary", {}).get("wholeBookCitationPassComplete") is False, "I.3 delta falsely closes whole-book pass")
require(delta.get("publicationBoundary", {}).get("productSourceLinkRepairRequired") == 3, "I.3 Product repair hold drift")

require(assembly.get("authorityId") == "HEART-I3-READER-ASSEMBLY-2026-08-04", "I.3 assembly authority drift")
require(assembly.get("effectiveCounts", {}).get("assembledReader") == 8, "I.3 assembly count drift")
require(assembly.get("effectiveCounts", {}).get("entryCitationPassComplete") == 7, "I.3 assembly must preserve pre-review count")

require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V5-2026-08-04", "V5 authority drift")
require(current.get("status") == "EIGHT_ENTRY_PASSES_COMPOSED_ALL_EIGHT_READERS_REVIEWED_TEN_READERS_OPEN", "V5 status drift")
prev_ref = current.get("previousCurrentAuthority", {})
require(prev_ref.get("gitBlob") == PREVIOUS_BLOB, "V5 previous blob drift")
require(prev_ref.get("authorityId") == previous.get("authorityId"), "V5 previous authority mismatch")
delta_ref = current.get("deltaReceipt", {})
require(delta_ref.get("gitBlob") == DELTA_BLOB, "V5 delta blob drift")
require(delta_ref.get("authorityId") == delta.get("authorityId"), "V5 delta authority mismatch")
require(delta_ref.get("readerAssemblyGitBlob") == ASSEMBLY_BLOB, "V5 assembly blob drift")
require(delta_ref.get("id") == "HEART-BOOK-I3", "V5 delta ID drift")
require(delta_ref.get("composedCountAfterReceipt") == "8 / 18", "V5 delta count drift")
require(delta_ref.get("productSourceLinkRepairRequired") == 3, "V5 Product repair delta drift")
require(delta_ref.get("newDirectQuotesApproved") == 0, "V5 delta quote boundary drift")
require(current.get("currentCounts") == EXPECTED_COUNTS, "V5 count block drift")
require(set(current.get("completedEntryIds", [])) == EXPECTED_COMPLETE, "V5 completed set drift")
require(set(current.get("openEntryIds", [])) == EXPECTED_OPEN, "V5 open set drift")
lanes = current.get("openEntriesBySourceLane", {})
require(set(lanes.get("productSourceOnly", [])) == EXPECTED_PRODUCT, "V5 Product lane drift")
require(set(lanes.get("researchDossierOnly", [])) == EXPECTED_DOSSIER, "V5 dossier lane drift")
require(EXPECTED_PRODUCT | EXPECTED_DOSSIER == EXPECTED_OPEN, "V5 lanes not exhaustive")
require(EXPECTED_PRODUCT & EXPECTED_DOSSIER == set(), "V5 lanes overlap")
backlog = current.get("readerAssemblyBacklog", {})
require(backlog.get("removedByDelta") == "HEART-BOOK-I3", "V5 removed delta drift")
require(set(backlog.get("remaining", [])) == EXPECTED_OPEN, "V5 remaining-reader set drift")
require(backlog.get("effectiveMissingStandaloneFinalReaders") == 10, "V5 remaining-reader count drift")
repair = current.get("productRepairBacklog", {})
require(repair.get("entryId") == "HEART-BOOK-I3", "V5 Product repair entry drift")
require(repair.get("requiredBeforeProductPublication") == 3, "V5 Product repair count drift")
require(repair.get("researchCitationReviewComplete") is True, "V5 Research review state drift")
require(repair.get("productSourceRepairComplete") is False, "V5 Product repair falsely closed")
boundary = current.get("publicationBoundary", {})
require(boundary.get("allCurrentlyAssembledReadersReviewed") is True, "V5 assembled-reader review state drift")
for key in (
    "wholeBookReaderAssemblyComplete", "wholeBookCitationPassComplete",
    "wholeBookTransitionDedupPassComplete", "wholeBookLineEditComplete",
    "manuscriptBundleComplete", "productReleaseComplete", "productSourceLinkRepairsComplete",
):
    require(boundary.get(key) is False, f"V5 falsely closes {key}")
require(boundary.get("newDirectQuotesApproved") == 0, "V5 direct quote boundary drift")
next_tx = current.get("nextTransaction", {})
require(next_tx.get("type") == "STANDALONE_READER_ASSEMBLY", "V5 next transaction type drift")
require(next_tx.get("preferredEntryId") == "HEART-BOOK-II", "V5 next entry drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-ENTRY-CITATION-PASS-CURRENT-V5-2026-08-04",
    "ENTRY CITATION PASSES COMPLETE = 8 / 18",
    "ENTRY CITATION PASSES OPEN = 10 / 18",
    "ASSEMBLED READERS = 8 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 8 / 8",
    "MISSING STANDALONE FINAL READERS = 10",
    "PRODUCT SOURCE ONLY = 4",
    "RESEARCH DOSSIER ONLY = 6",
    "PRODUCT SOURCE LINK REPAIRS REQUIRED = 3",
    "NEXT READER ASSEMBLY = HEART-BOOK-II",
    PREVIOUS_BLOB, DELTA_BLOB,
):
    require(marker in human, f"V5 human authority marker missing: {marker}")
for forbidden in (
    "ENTRY CITATION PASSES COMPLETE = 18 / 18",
    "PRODUCT SOURCE LINK REPAIRS REQUIRED = 0",
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "WHOLE-BOOK READER ASSEMBLY = COMPLETE",
    "PRODUCT RELEASE = COMPLETE", "TODO", "TBD",
):
    require(forbidden not in human, f"V5 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart entry citation pass current V5: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Heart entry citation pass current V5: PASS — 8/18 completed, 10 open, reviews 8/8, backlog 10 = 4 Product + 6 dossier, 3 Product repairs, next Part II")
