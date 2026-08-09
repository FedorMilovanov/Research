#!/usr/bin/env python3
"""Validate the versioned Heart current citation state V10."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v10-2026-08-09.json"
PREVIOUS = ROOT / "data/heart-entry-citation-pass-current-v9-2026-08-04.json"
DELTA = ROOT / "data/heart-part4-citation-review-2026-08-04.json"
ASSEMBLY = ROOT / "data/heart-part4-reader-assembly-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/132_ENTRY_CITATION_PASS_CURRENT_V10_2026-08-09.md"
WORKFLOW = ROOT / ".github/workflows/heart-reader-assembly.yml"

PREVIOUS_BLOB = "d8a65b5233a471e024f5642e1dc3d1a50f13babf"
DELTA_BLOB = "2f458ae92cd13010ccc1f13ee56cfceec77bc5f7"
ASSEMBLY_BLOB = "58f0922734601cf9cf16e448d50836b269b624e0"

COMPLETE = {
    "HEART-BOOK-I1", "HEART-BOOK-I2", "HEART-BOOK-I3", "HEART-BOOK-I4", "HEART-BOOK-II",
    "HEART-BOOK-III1", "HEART-BOOK-III2", "HEART-BOOK-III3", "HEART-BOOK-III4", "HEART-BOOK-IV",
    "HEART-BOOK-X1", "HEART-BOOK-X2", "HEART-BOOK-X3",
}
OPEN = {"HEART-BOOK-V", "HEART-BOOK-VI", "HEART-BOOK-VII", "HEART-BOOK-VIII", "HEART-BOOK-IX"}
PRODUCT = {"HEART-BOOK-V", "HEART-BOOK-VII"}
DOSSIER = {"HEART-BOOK-VI", "HEART-BOOK-VIII", "HEART-BOOK-IX"}

EXPECTED_COUNTS = {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 13,
    "entryCitationPassOpen": 5,
    "assembledReaderEntries": 13,
    "assembledReaderCitationReviewsComplete": 13,
    "missingStandaloneFinalReaders": 5,
    "productSourceOnlyEntries": 2,
    "researchDossierOnlyEntries": 3,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 55,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
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
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be an object")
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

# Immutable V9 boundary.
require(previous.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V9-2026-08-04", "V9 authority drift")
require(previous.get("currentCounts") == {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 12,
    "entryCitationPassOpen": 6,
    "assembledReaderEntries": 12,
    "assembledReaderCitationReviewsComplete": 12,
    "missingStandaloneFinalReaders": 6,
    "productSourceOnlyEntries": 2,
    "researchDossierOnlyEntries": 4,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 46,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "newDirectQuotesApproved": 0,
}, "V9 current-count block drift")
require("HEART-BOOK-IV" in set(previous.get("openEntryIds", [])), "V9 no longer leaves Part IV open")
require(previous.get("nextTransaction", {}).get("preferredEntryId") == "HEART-BOOK-IV", "V9 next-entry boundary drift")

# Immutable Part IV receipt and assembly must prove exactly this delta.
require(delta.get("authorityId") == "HEART-PART4-CITATION-REVIEW-2026-08-04", "Part IV delta authority drift")
require(delta.get("entry", {}).get("id") == "HEART-BOOK-IV", "Part IV delta entry drift")
require(delta.get("entry", {}).get("order") == 10, "Part IV delta order drift")
require(delta.get("effectiveState") == {
    "entryCitationPassComplete": True,
    "assembledReaderCitationReviewComplete": True,
    "sourceQuotationSurfacesCopiedToReader": 0,
    "sourceLinksCopiedToReader": 0,
    "newDirectQuotesApproved": 0,
}, "Part IV delta effective-state drift")
require(delta.get("effectiveCounts") == {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 13,
    "entryCitationPassOpen": 5,
    "assembledReaders": 13,
    "assembledReaderCitationReviewsComplete": 13,
    "missingStandaloneFinalReaders": 5,
    "productSourceOnlyEntries": 2,
    "researchDossierOnlyEntries": 3,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 55,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "newDirectQuotesApproved": 0,
}, "Part IV delta effective-count drift")
require(delta.get("retainedRepairAndHoldBacklog") == {
    "productSourceRepairsRequired": 4,
    "precedingDossierUrlHoldsRetained": 46,
    "part4DossierUrlHoldsAdded": 9,
    "currentDossierUrlHoldsRetained": 55,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "part4NewUnresolvedInternalPaths": 0,
}, "Part IV repair/hold backlog drift")
require(delta.get("externalLinkReview", {}).get("statusCounts") == {
    "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD": 9,
    "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE": 27,
}, "Part IV URL status drift")
require(delta.get("externalLinkReview", {}).get("sourceUrlRepairsAdded") == 0, "Part IV unexpectedly adds URL repairs")
internal = delta.get("internalLinkReview", {})
require(internal.get("detected") == 2, "Part IV detected internal-path count drift")
require(internal.get("externalUrlPathFragmentFalsePositives") == 2, "Part IV false-positive classification drift")
require(internal.get("newUnresolvedInternalPaths") == 0, "Part IV unexpectedly adds unresolved internal paths")
require(delta.get("nextTransaction") == "Compose a separate versioned current V10 authority from immutable current V9 plus this Part IV citation receipt.", "Part IV next-transaction drift")

require(assembly.get("authorityId") == "HEART-PART4-READER-ASSEMBLY-2026-08-04", "Part IV assembly authority drift")
require(assembly.get("effectiveCounts", {}).get("assembledReaders") == 13, "Part IV assembly reader count drift")
require(assembly.get("effectiveCounts", {}).get("entryCitationPassComplete") == 12, "Part IV assembly must retain pre-review citation count")
require(assembly.get("publicationBoundary", {}).get("part4EntryCitationPassComplete") is False, "Part IV assembly falsely claims citation completion")

# V10 is composition only: one set transition, no silent closure.
require(current.get("schemaVersion") == 10, "V10 schema drift")
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V10-2026-08-09", "V10 authority drift")
require(current.get("status") == "THIRTEEN_ENTRY_PASSES_COMPOSED_ALL_THIRTEEN_READERS_REVIEWED_FIVE_READERS_OPEN", "V10 status drift")

previous_ref = current.get("previousCurrentAuthority", {})
require(previous_ref.get("path") == str(PREVIOUS.relative_to(ROOT)), "V10 previous path drift")
require(previous_ref.get("gitBlob") == PREVIOUS_BLOB, "V10 previous blob drift")
require(previous_ref.get("authorityId") == previous.get("authorityId"), "V10 previous authority mismatch")
require(previous_ref.get("historicalCounts", {}).get("entryCitationPassComplete") == 12, "V10 historical completion count drift")
require(previous_ref.get("historicalCounts", {}).get("dossierUrlHoldsRetained") == 46, "V10 historical hold count drift")

receipt = current.get("deltaReceipt", {})
require(receipt.get("path") == str(DELTA.relative_to(ROOT)), "V10 delta path drift")
require(receipt.get("gitBlob") == DELTA_BLOB, "V10 delta blob drift")
require(receipt.get("authorityId") == delta.get("authorityId"), "V10 delta authority mismatch")
require(receipt.get("readerAssemblyPath") == str(ASSEMBLY.relative_to(ROOT)), "V10 assembly path drift")
require(receipt.get("readerAssemblyGitBlob") == ASSEMBLY_BLOB, "V10 assembly blob drift")
require(receipt.get("id") == "HEART-BOOK-IV" and receipt.get("order") == 10, "V10 delta identity drift")
require(receipt.get("composedCountAfterReceipt") == "13 / 18", "V10 composed count drift")
require(receipt.get("dossierUrlHoldsAdded") == 9, "V10 hold delta drift")
require(receipt.get("dossierSourceUrlRepairsAdded") == 0, "V10 source-repair delta drift")
require(receipt.get("unresolvedInternalPathsAdded") == 0, "V10 unresolved-path delta drift")
require(receipt.get("externalUrlPathFragmentFalsePositives") == 2, "V10 false-positive delta drift")
require(receipt.get("newDirectQuotesApproved") == 0, "V10 quote delta drift")

require(current.get("currentCounts") == EXPECTED_COUNTS, "V10 current-count block drift")
require(set(current.get("completedEntryIds", [])) == COMPLETE, "V10 completed set drift")
require(set(current.get("openEntryIds", [])) == OPEN, "V10 open set drift")
require(COMPLETE.isdisjoint(OPEN) and len(COMPLETE | OPEN) == 18, "V10 complete/open partition drift")
lanes = current.get("openEntriesBySourceLane", {})
require(set(lanes.get("productSourceOnly", [])) == PRODUCT, "V10 Product lane drift")
require(set(lanes.get("researchDossierOnly", [])) == DOSSIER, "V10 dossier lane drift")
require(PRODUCT | DOSSIER == OPEN and not PRODUCT & DOSSIER, "V10 open lanes are not disjoint/exhaustive")
backlog = current.get("readerAssemblyBacklog", {})
require(backlog.get("removedByDelta") == "HEART-BOOK-IV", "V10 removed-delta drift")
require(set(backlog.get("remaining", [])) == OPEN, "V10 reader backlog set drift")
require(backlog.get("effectiveMissingStandaloneFinalReaders") == 5, "V10 reader backlog count drift")

retained = current.get("retainedRepairAndHoldBacklog", {})
require(retained.get("productSourceRepairs") == previous.get("retainedRepairAndHoldBacklog", {}).get("productSourceRepairs"), "V10 silently changed Product repairs")
require(retained.get("iii1AttributedTheologicalLocatorHolds") == previous.get("retainedRepairAndHoldBacklog", {}).get("iii1AttributedTheologicalLocatorHolds"), "V10 silently changed III.1 attributed hold")
require(retained.get("iii1LexicalSupportLocatorHolds") == previous.get("retainedRepairAndHoldBacklog", {}).get("iii1LexicalSupportLocatorHolds"), "V10 silently changed III.1 lexical holds")
require(retained.get("iii2DossierSourceUrlRepairs") == previous.get("retainedRepairAndHoldBacklog", {}).get("iii2DossierSourceUrlRepairs"), "V10 silently changed III.2 source repairs")
require(retained.get("part2UnresolvedInternalPath") == previous.get("retainedRepairAndHoldBacklog", {}).get("part2UnresolvedInternalPath"), "V10 silently changed unresolved Part II path")
require(retained.get("iii2FalsePositiveInternalPath") == previous.get("retainedRepairAndHoldBacklog", {}).get("iii2FalsePositiveInternalPath"), "V10 silently changed III.2 false-positive path")
require(retained.get("iii4InternalTargetReview") == previous.get("retainedRepairAndHoldBacklog", {}).get("iii4InternalTargetReview"), "V10 silently changed III.4 target review")
require(retained.get("dossierUrlHolds") == {
    "totalRetained": 55,
    "components": [
        {"entryId": "HEART-BOOK-II", "retained": 15, "promoted": 0},
        {"entryId": "HEART-BOOK-III2", "retained": 25, "promoted": 0},
        {"entryId": "HEART-BOOK-III4", "retained": 6, "promoted": 0},
        {"entryId": "HEART-BOOK-IV", "retained": 9, "promoted": 0},
    ],
}, "V10 dossier-hold composition drift")
require(retained.get("part4InternalLinkReview") == {
    "detected": 2,
    "externalUrlPathFragmentFalsePositives": 2,
    "newUnresolvedInternalPaths": 0,
    "readerTransfer": False,
}, "V10 Part IV internal-link carry-forward drift")

boundary = current.get("publicationBoundary", {})
require(boundary.get("allCurrentlyAssembledReadersReviewed") is True, "V10 assembled-reader review drift")
for key in (
    "wholeBookReaderAssemblyComplete",
    "wholeBookCitationPassComplete",
    "wholeBookTransitionDedupPassComplete",
    "wholeBookLineEditComplete",
    "manuscriptBundleComplete",
    "productReleaseComplete",
    "productSourceRepairsComplete",
    "dossierUrlHoldsResolved",
    "dossierSourceUrlRepairsComplete",
    "unresolvedInternalPathsResolved",
):
    require(boundary.get(key) is False, f"V10 falsely closes publication boundary: {key}")
require(boundary.get("newDirectQuotesApproved") == 0, "V10 publication boundary approves new quotes")
require(current.get("nextTransaction", {}).get("type") == "STANDALONE_READER_ASSEMBLY", "V10 next transaction type drift")
require(current.get("nextTransaction", {}).get("preferredEntryId") == "HEART-BOOK-V", "V10 next entry must be Part V")

require(HUMAN.is_file(), "V10 human authority missing")
if HUMAN.is_file():
    human = HUMAN.read_text(encoding="utf-8")
    for marker in (
        "ENTRY CITATION PASSES COMPLETE = 13 / 18",
        "ENTRY CITATION PASSES OPEN = 5 / 18",
        "ASSEMBLED READERS = 13 / 18",
        "DOSSIER URL HOLDS RETAINED = 55",
        "PRODUCT SOURCE REPAIRS REQUIRED = 4",
        "UNRESOLVED INTERNAL PATHS RETAINED = 1",
        "NEXT READER ASSEMBLY = HEART-BOOK-V",
        "PRODUCT RELEASE = NOT CLAIMED",
    ):
        require(marker in human, f"V10 human authority missing marker: {marker}")

require(WORKFLOW.is_file(), "Heart workflow missing")
if WORKFLOW.is_file():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    require("scripts/validate_heart_entry_citation_pass_current_v10.py" in workflow, "workflow does not compile/run V10 validator")
    require("Validate current thirteen-entry composition" in workflow, "workflow missing V10 validation step")

if errors:
    print("Heart current V10 composition: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart current V10 composition: PASS — 13/18 reviewed, five readers open, 55 holds retained, zero silent closure")
