#!/usr/bin/env python3
"""Validate the V2 composed Heart entry-citation-pass current state."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRENT_V2 = ROOT / "data/heart-entry-citation-pass-current-v2-2026-08-04.json"
PREVIOUS = ROOT / "data/heart-entry-citation-pass-current-2026-08-04.json"
X2_REVIEW = ROOT / "data/heart-x2-citation-review-2026-08-04.json"
X2_ASSEMBLY = ROOT / "data/heart-x2-reader-assembly-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/100_ENTRY_CITATION_PASS_CURRENT_V2_2026-08-04.md"

PREVIOUS_BLOB = "79cfd859180a95da76c8102bc4167f245487dd74"
X2_REVIEW_BLOB = "09996dbc5dba079c3c786c2da1befc8f28c2def2"
X2_ASSEMBLY_BLOB = "c6d80a65ad7b4d764252ad48169b1e33ad88d283"
EXPECTED_PREVIOUS_COMPLETED = {
    "HEART-BOOK-I2",
    "HEART-BOOK-III3",
    "HEART-BOOK-X1",
    "HEART-BOOK-X3",
}
EXPECTED_COMPLETED = EXPECTED_PREVIOUS_COMPLETED | {"HEART-BOOK-X2"}
EXPECTED_PRODUCT_OPEN = {
    "HEART-BOOK-I1",
    "HEART-BOOK-I3",
    "HEART-BOOK-I4",
    "HEART-BOOK-III1",
    "HEART-BOOK-III4",
    "HEART-BOOK-V",
    "HEART-BOOK-VII",
}
EXPECTED_DOSSIER_OPEN = {
    "HEART-BOOK-II",
    "HEART-BOOK-III2",
    "HEART-BOOK-IV",
    "HEART-BOOK-VI",
    "HEART-BOOK-VIII",
    "HEART-BOOK-IX",
}
EXPECTED_OPEN = EXPECTED_PRODUCT_OPEN | EXPECTED_DOSSIER_OPEN
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


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
    ).strip()


for path, expected in (
    (PREVIOUS, PREVIOUS_BLOB),
    (X2_REVIEW, X2_REVIEW_BLOB),
    (X2_ASSEMBLY, X2_ASSEMBLY_BLOB),
):
    require(path.is_file(), f"immutable authority missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(git_blob(path) == expected, f"immutable authority blob drift: {path.relative_to(ROOT)}")

previous = read_json(PREVIOUS)
x2_review = read_json(X2_REVIEW)
x2_assembly = read_json(X2_ASSEMBLY)
current = read_json(CURRENT_V2)

require(previous.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-2026-08-04", "previous current authority drift")
require(previous.get("status") == "FOUR_ENTRY_PASSES_COMPOSED_ALL_ASSEMBLED_READER_REVIEWS_COMPLETE_READER_ASSEMBLY_OPEN", "previous current status drift")
previous_counts = previous.get("currentCounts", {})
require(previous_counts == {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 4,
    "entryCitationPassOpen": 14,
    "assembledReaderEntries": 4,
    "assembledReaderCitationReviewsComplete": 4,
    "missingStandaloneFinalReaders": 14,
    "newDirectQuotesApproved": 0,
}, "previous current count block drift")
require(set(previous.get("completedEntryIds", [])) == EXPECTED_PREVIOUS_COMPLETED, "previous completed-entry set drift")
require(set(previous.get("openEntryIds", [])) == EXPECTED_OPEN | {"HEART-BOOK-X2"}, "previous open-entry set drift")
require("HEART-BOOK-X2" in previous.get("openEntriesBySourceLane", {}).get("productSourceOnly", []), "X.2 absent from previous Product-open lane")

require(x2_assembly.get("authorityId") == "HEART-X2-READER-ASSEMBLY-2026-08-04", "X.2 assembly authority drift")
require(x2_assembly.get("status") == "X2_FINAL_BOOK_READER_ASSEMBLED_PARAPHRASE_ONLY_ENTRY_CITATION_PASS_OPEN", "X.2 assembly status drift")
require(x2_assembly.get("effectivePrimaryState", {}).get("current") == "ASSEMBLED_READER", "X.2 assembly primary state drift")
require(x2_assembly.get("effectivePrimaryState", {}).get("entryCitationPassComplete") is False, "historical X.2 assembly receipt rewritten")
require(x2_assembly.get("effectiveCounts", {}).get("assembledReader") == 5, "X.2 assembly reader count drift")
require(x2_assembly.get("effectiveCounts", {}).get("missingStandaloneFinalReaders") == 13, "X.2 assembly backlog count drift")
require(set(x2_assembly.get("remainingReaderAssemblies", [])) == EXPECTED_OPEN, "X.2 assembly remaining-reader set drift")

require(x2_review.get("authorityId") == "HEART-X2-CITATION-REVIEW-2026-08-04", "X.2 citation authority drift")
require(x2_review.get("status") == "X2_ENTRY_CITATION_PASS_COMPLETE_ASSEMBLED_READER_REVIEWS_FIVE_OF_FIVE_WHOLE_BOOK_OPEN", "X.2 citation status drift")
require(x2_review.get("entry", {}).get("id") == "HEART-BOOK-X2", "X.2 citation entry ID drift")
require(x2_review.get("entry", {}).get("stateAfter") == "ENTRY_CITATION_PASS_COMPLETE", "X.2 citation state transition drift")
require(x2_review.get("disposition", {}).get("entryCitationPassComplete") is True, "X.2 citation pass incomplete")
require(x2_review.get("disposition", {}).get("remainingEntryBlockers") == [], "X.2 citation blockers remain")
require(x2_review.get("disposition", {}).get("newDirectQuotesApproved") == 0, "X.2 direct-quote boundary drift")
x2_boundary = x2_review.get("wholeBookBoundary", {})
require(x2_boundary.get("entryCitationPassComplete") == "5 / 18", "X.2 composed citation count drift")
require(x2_boundary.get("entryCitationPassOpen") == "13 / 18", "X.2 open citation count drift")
require(x2_boundary.get("assembledReaderEntries") == "5 / 18", "X.2 assembled-reader count drift")
require(x2_boundary.get("assembledReaderCitationReviewsComplete") == "5 / 5", "X.2 assembled-reader review count drift")
require(x2_boundary.get("missingStandaloneFinalReaders") == 13, "X.2 missing-reader count drift")
require(x2_boundary.get("wholeBookCitationPassComplete") is False, "X.2 falsely closes whole-book citation pass")
require(x2_boundary.get("productReleaseComplete") is False, "X.2 falsely closes Product release")

require(current.get("schemaVersion") == 2, "current V2 schema drift")
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V2-2026-08-04", "current V2 authority drift")
require(current.get("status") == "FIVE_ENTRY_PASSES_COMPOSED_ALL_FIVE_ASSEMBLED_READERS_REVIEWED_THIRTEEN_READERS_OPEN", "current V2 status drift")
base = current.get("previousCurrentAuthority", {})
require(base.get("gitBlob") == PREVIOUS_BLOB, "current V2 previous-current blob drift")
require(base.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-2026-08-04", "current V2 previous authority ID drift")
require(base.get("historicalCounts") == {
    "entryCitationPassComplete": 4,
    "entryCitationPassOpen": 14,
    "assembledReaderEntries": 4,
    "assembledReaderCitationReviewsComplete": 4,
    "missingStandaloneFinalReaders": 14,
}, "current V2 historical count block drift")
delta = current.get("deltaReceipt", {})
require(delta.get("id") == "HEART-BOOK-X2", "current V2 delta entry drift")
require(delta.get("gitBlob") == X2_REVIEW_BLOB, "current V2 X.2 review blob drift")
require(delta.get("readerAssemblyGitBlob") == X2_ASSEMBLY_BLOB, "current V2 X.2 assembly blob drift")
require(delta.get("composedCountAfterReceipt") == "5 / 18", "current V2 delta count drift")
require(delta.get("newDirectQuotesApproved") == 0, "current V2 delta direct-quote drift")
require(current.get("currentCounts") == {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 5,
    "entryCitationPassOpen": 13,
    "assembledReaderEntries": 5,
    "assembledReaderCitationReviewsComplete": 5,
    "missingStandaloneFinalReaders": 13,
    "productSourceOnlyEntries": 7,
    "researchDossierOnlyEntries": 6,
    "newDirectQuotesApproved": 0,
}, "current V2 count block drift")
require(set(current.get("completedEntryIds", [])) == EXPECTED_COMPLETED, "current V2 completed-entry set drift")
require(set(current.get("openEntryIds", [])) == EXPECTED_OPEN, "current V2 open-entry set drift")
lanes = current.get("openEntriesBySourceLane", {})
require(set(lanes.get("productSourceOnly", [])) == EXPECTED_PRODUCT_OPEN, "current V2 Product-open lane drift")
require(set(lanes.get("researchDossierOnly", [])) == EXPECTED_DOSSIER_OPEN, "current V2 dossier-open lane drift")
require(EXPECTED_PRODUCT_OPEN.isdisjoint(EXPECTED_DOSSIER_OPEN), "current V2 source lanes overlap")
require(EXPECTED_PRODUCT_OPEN | EXPECTED_DOSSIER_OPEN == EXPECTED_OPEN, "current V2 source lanes are not exhaustive")
backlog = current.get("readerAssemblyBacklog", {})
require(backlog.get("removedByDelta") == "HEART-BOOK-X2", "current V2 removed backlog entry drift")
require(set(backlog.get("remaining", [])) == EXPECTED_OPEN, "current V2 reader backlog set drift")
require(backlog.get("effectiveMissingStandaloneFinalReaders") == 13, "current V2 reader backlog count drift")
boundary = current.get("publicationBoundary", {})
require(boundary.get("allCurrentlyAssembledReadersReviewed") is True, "current V2 assembled-reader review state open")
require(boundary.get("wholeBookReaderAssemblyComplete") is False, "current V2 falsely closes reader assembly")
require(boundary.get("wholeBookCitationPassComplete") is False, "current V2 falsely closes citation pass")
require(boundary.get("wholeBookTransitionDedupPassComplete") is False, "current V2 falsely closes transition/dedup")
require(boundary.get("wholeBookLineEditComplete") is False, "current V2 falsely closes line edit")
require(boundary.get("manuscriptBundleComplete") is False, "current V2 falsely closes manuscript bundle")
require(boundary.get("productReleaseComplete") is False, "current V2 falsely closes Product release")
require(boundary.get("newDirectQuotesApproved") == 0, "current V2 direct-quote boundary drift")
next_tx = current.get("nextTransaction", {})
require(next_tx.get("type") == "STANDALONE_READER_ASSEMBLY", "current V2 next transaction type drift")
require(next_tx.get("preferredEntryId") == "HEART-BOOK-I4", "current V2 preferred next entry drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-ENTRY-CITATION-PASS-CURRENT-V2-2026-08-04",
    "ENTRY CITATION PASSES COMPLETE = 5 / 18",
    "ENTRY CITATION PASSES OPEN = 13 / 18",
    "ASSEMBLED READERS = 5 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 5 / 5",
    "MISSING STANDALONE FINAL READERS = 13",
    "PRODUCT SOURCE ONLY = 7",
    "RESEARCH DOSSIER ONLY = 6",
    "NEXT READER ASSEMBLY = HEART-BOOK-I4",
    "WHOLE-BOOK CITATION PASS = OPEN",
    "WHOLE-BOOK READER ASSEMBLY = INCOMPLETE",
    "NEW DIRECT QUOTES APPROVED = 0",
    PREVIOUS_BLOB,
    X2_REVIEW_BLOB,
):
    require(marker in human, f"current V2 human authority marker missing: {marker}")
for forbidden in (
    "ENTRY CITATION PASSES COMPLETE = 18 / 18",
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "WHOLE-BOOK READER ASSEMBLY = COMPLETE",
    "NEW DIRECT QUOTES APPROVED = 1",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"current V2 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart entry citation pass current V2: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "Heart entry citation pass current V2: PASS — "
    "5/18 completed, 13/18 open, assembled-reader reviews 5/5, "
    "reader backlog 13 = 7 Product + 6 dossier, next I.4, 0 new direct quotes"
)
