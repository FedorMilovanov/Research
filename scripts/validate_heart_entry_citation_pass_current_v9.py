#!/usr/bin/env python3
"""Validate the versioned Heart current citation state V9."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v9-2026-08-04.json"
PREVIOUS = ROOT / "data/heart-entry-citation-pass-current-v8-2026-08-04.json"
DELTA = ROOT / "data/heart-iii4-citation-review-2026-08-04.json"
ASSEMBLY = ROOT / "data/heart-iii4-reader-assembly-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/128_ENTRY_CITATION_PASS_CURRENT_V9_2026-08-04.md"
WORKFLOW = ROOT / ".github/workflows/heart-reader-assembly.yml"
PREVIOUS_BLOB = "6736f90211e34c5dbb7d9943e617102b660bb5be"
DELTA_BLOB = "ee8fc5302c18351c83d1d3b15010a67d162bd947"
ASSEMBLY_BLOB = "b9dfda284cfa36d8ee6a7d970dc3bf2a9eeba7c9"
COMPLETE = {
    "HEART-BOOK-I1", "HEART-BOOK-I2", "HEART-BOOK-I3", "HEART-BOOK-I4", "HEART-BOOK-II",
    "HEART-BOOK-III1", "HEART-BOOK-III2", "HEART-BOOK-III3", "HEART-BOOK-III4",
    "HEART-BOOK-X1", "HEART-BOOK-X2", "HEART-BOOK-X3",
}
OPEN = {
    "HEART-BOOK-IV", "HEART-BOOK-V", "HEART-BOOK-VI",
    "HEART-BOOK-VII", "HEART-BOOK-VIII", "HEART-BOOK-IX",
}
PRODUCT = {"HEART-BOOK-V", "HEART-BOOK-VII"}
DOSSIER = {"HEART-BOOK-IV", "HEART-BOOK-VI", "HEART-BOOK-VIII", "HEART-BOOK-IX"}
EXPECTED_COUNTS = {
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

require(previous.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V8-2026-08-04", "V8 authority drift")
require(previous.get("currentCounts") == {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 11,
    "entryCitationPassOpen": 7,
    "assembledReaderEntries": 11,
    "assembledReaderCitationReviewsComplete": 11,
    "missingStandaloneFinalReaders": 7,
    "productSourceOnlyEntries": 3,
    "researchDossierOnlyEntries": 4,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 40,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "newDirectQuotesApproved": 0,
}, "V8 count block drift")
require(set(previous.get("completedEntryIds", [])) == COMPLETE - {"HEART-BOOK-III4"}, "V8 completed set drift")
require(set(previous.get("openEntryIds", [])) == OPEN | {"HEART-BOOK-III4"}, "V8 open set drift")
require(previous.get("nextTransaction", {}).get("preferredEntryId") == "HEART-BOOK-III4", "V8 next-entry boundary drift")

require(delta.get("authorityId") == "HEART-III4-CITATION-REVIEW-2026-08-04", "III.4 delta authority drift")
require(delta.get("entry", {}).get("id") == "HEART-BOOK-III4", "III.4 delta entry drift")
require(delta.get("effectiveState") == {
    "entryCitationPassComplete": True,
    "assembledReaderCitationReviewComplete": True,
    "sourceQuotationSurfacesCopiedToReader": 0,
    "sourceLinksCopiedToReader": 0,
    "newDirectQuotesApproved": 0,
}, "III.4 delta effective-state drift")
require(delta.get("effectiveCounts") == {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 12,
    "entryCitationPassOpen": 6,
    "assembledReaders": 12,
    "assembledReaderCitationReviewsComplete": 12,
    "missingStandaloneFinalReaders": 6,
    "productSourceOnlyEntries": 2,
    "researchDossierOnlyEntries": 4,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 46,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "newDirectQuotesApproved": 0,
}, "III.4 delta effective-count drift")
require(delta.get("retainedRepairAndHoldBacklog") == {
    "productSourceRepairsRequired": 4,
    "precedingDossierUrlHoldsRetained": 40,
    "iii4DossierUrlHoldsAdded": 6,
    "currentDossierUrlHoldsRetained": 46,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "iii4NewUnresolvedInternalPaths": 0,
}, "III.4 delta backlog drift")
require(delta.get("externalLinkReview", {}).get("statusCounts") == {
    "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD": 6,
    "DOSSIER_SUPPORT_RECORD_NO_READER_TRANSFER": 5,
    "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE": 19,
}, "III.4 URL status drift")
require(delta.get("externalLinkReview", {}).get("sourceUrlRepairsAdded") == 0, "III.4 unexpectedly adds URL repair")
require(delta.get("internalLinkReview", {}).get("detected") == 6, "III.4 Product-target count drift")
require(delta.get("internalLinkReview", {}).get("allTargetsExistOnPinnedProductCommit") is True, "III.4 Product targets not all verified")
require(delta.get("internalLinkReview", {}).get("newUnresolvedInternalPaths") == 0, "III.4 unexpectedly adds unresolved path")
require(delta.get("publicationBoundary", {}).get("allCurrentlyAssembledReadersReviewed") is True, "III.4 reader-review state drift")
require(delta.get("publicationBoundary", {}).get("wholeBookReaderAssemblyComplete") is False, "III.4 falsely closes whole-book assembly")
require(delta.get("nextTransaction") == "Compose a separate versioned current V9 authority from immutable current V8 plus this III.4 citation receipt.", "III.4 next-transaction drift")

require(assembly.get("authorityId") == "HEART-III4-READER-ASSEMBLY-2026-08-04", "III.4 assembly authority drift")
require(assembly.get("effectiveCounts", {}).get("assembledReaders") == 12, "III.4 assembly reader count drift")
require(assembly.get("effectiveCounts", {}).get("entryCitationPassComplete") == 11, "III.4 assembly must retain pre-review citation count")
require(assembly.get("publicationBoundary", {}).get("iii4EntryCitationPassComplete") is False, "III.4 assembly falsely claims citation completion")

require(current.get("schemaVersion") == 9, "V9 schema drift")
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V9-2026-08-04", "V9 authority drift")
require(current.get("status") == "TWELVE_ENTRY_PASSES_COMPOSED_ALL_TWELVE_READERS_REVIEWED_SIX_READERS_OPEN", "V9 status drift")
previous_ref = current.get("previousCurrentAuthority", {})
require(previous_ref.get("path") == str(PREVIOUS.relative_to(ROOT)), "V9 previous path drift")
require(previous_ref.get("gitBlob") == PREVIOUS_BLOB, "V9 previous blob drift")
require(previous_ref.get("authorityId") == previous.get("authorityId"), "V9 previous authority mismatch")
require(previous_ref.get("historicalCounts") == {
    "entryCitationPassComplete": 11,
    "entryCitationPassOpen": 7,
    "assembledReaderEntries": 11,
    "assembledReaderCitationReviewsComplete": 11,
    "missingStandaloneFinalReaders": 7,
    "productSourceOnlyEntries": 3,
    "researchDossierOnlyEntries": 4,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 40,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
}, "V9 historical-count block drift")

delta_ref = current.get("deltaReceipt", {})
require(delta_ref.get("path") == str(DELTA.relative_to(ROOT)), "V9 delta path drift")
require(delta_ref.get("gitBlob") == DELTA_BLOB, "V9 delta blob drift")
require(delta_ref.get("authorityId") == delta.get("authorityId"), "V9 delta authority mismatch")
require(delta_ref.get("readerAssemblyPath") == str(ASSEMBLY.relative_to(ROOT)), "V9 assembly path drift")
require(delta_ref.get("readerAssemblyGitBlob") == ASSEMBLY_BLOB, "V9 assembly blob drift")
require(delta_ref.get("id") == "HEART-BOOK-III4" and delta_ref.get("order") == 9, "V9 delta identity drift")
require(delta_ref.get("composedCountAfterReceipt") == "12 / 18", "V9 composed-count drift")
require(delta_ref.get("dossierUrlHoldsAdded") == 6, "V9 hold delta drift")
require(delta_ref.get("dossierSourceUrlRepairsAdded") == 0, "V9 repair delta drift")
require(delta_ref.get("unresolvedInternalPathsAdded") == 0, "V9 unresolved-path delta drift")
require(delta_ref.get("productInternalTargetsVerified") == 6, "V9 target-verification delta drift")
require(delta_ref.get("newDirectQuotesApproved") == 0, "V9 quote delta drift")

require(current.get("currentCounts") == EXPECTED_COUNTS, "V9 current-count block drift")
require(set(current.get("completedEntryIds", [])) == COMPLETE, "V9 completed set drift")
require(set(current.get("openEntryIds", [])) == OPEN, "V9 open set drift")
lanes = current.get("openEntriesBySourceLane", {})
require(set(lanes.get("productSourceOnly", [])) == PRODUCT, "V9 Product lane drift")
require(set(lanes.get("researchDossierOnly", [])) == DOSSIER, "V9 dossier lane drift")
require(PRODUCT | DOSSIER == OPEN and not PRODUCT & DOSSIER, "V9 lanes are not disjoint/exhaustive")
backlog = current.get("readerAssemblyBacklog", {})
require(backlog.get("removedByDelta") == "HEART-BOOK-III4", "V9 removed-delta drift")
require(set(backlog.get("remaining", [])) == OPEN, "V9 reader backlog set drift")
require(backlog.get("effectiveMissingStandaloneFinalReaders") == 6, "V9 reader backlog count drift")

retained = current.get("retainedRepairAndHoldBacklog", {})
require(retained.get("productSourceRepairs") == {
    "totalRequired": 4,
    "complete": False,
    "items": [
        {"entryId": "HEART-BOOK-I3", "kind": "SOURCE_URL_REPAIR", "required": 3},
        {"entryId": "HEART-BOOK-III1", "kind": "SCRIPTURE_LOCATOR_REPAIR", "required": 1, "surfaceIndex": 57, "requiredLocator": "Флп. 1:6"},
    ],
}, "V9 Product repair backlog drift")
require(retained.get("iii1AttributedTheologicalLocatorHolds") == {
    "entryId": "HEART-BOOK-III1", "retained": 1, "surfaceIndex": 26, "readerTransfer": False
}, "V9 III.1 attributed hold drift")
require(retained.get("iii1LexicalSupportLocatorHolds") == {
    "entryId": "HEART-BOOK-III1", "retained": 8,
    "surfaceIndices": [24, 39, 44, 62, 63, 64, 65, 66], "readerTransfer": False
}, "V9 III.1 lexical hold drift")
require(retained.get("dossierUrlHolds") == {
    "totalRetained": 46,
    "components": [
        {"entryId": "HEART-BOOK-II", "retained": 15, "promoted": 0},
        {"entryId": "HEART-BOOK-III2", "retained": 25, "promoted": 0},
        {"entryId": "HEART-BOOK-III4", "retained": 6, "promoted": 0},
    ],
}, "V9 dossier-hold composition drift")
require(retained.get("iii2DossierSourceUrlRepairs") == {
    "entryId": "HEART-BOOK-III2",
    "required": 2,
    "complete": False,
    "tokens": [
        "https://www.monergism.com/regeneration-6`",
        "https://www.reformedreader.org/ccc/1689lbc/english/Chapter10.htm**",
    ],
}, "V9 dossier source-repair backlog drift")
require(retained.get("part2UnresolvedInternalPath") == {
    "path": "/articles/opinion/", "retained": 1, "readerTransfer": False
}, "V9 unresolved-path backlog drift")
require(retained.get("iii2FalsePositiveInternalPath") == {
    "path": "/articles/onsite/",
    "status": "EXTERNAL_URL_PATH_FRAGMENT_FALSE_POSITIVE",
    "unresolvedInternalPathsAdded": 0,
    "readerTransfer": False,
}, "V9 III.2 false-positive path drift")
require(retained.get("iii4InternalTargetReview") == {
    "verifiedOnPinnedProductCommit": 6,
    "newUnresolvedInternalPaths": 0,
    "readerTransfer": False,
}, "V9 III.4 target-review carry-forward drift")

boundary = current.get("publicationBoundary", {})
require(boundary.get("allCurrentlyAssembledReadersReviewed") is True, "V9 assembled-reader review drift")
for key in (
    "wholeBookReaderAssemblyComplete", "wholeBookCitationPassComplete",
    "wholeBookTransitionDedupPassComplete", "wholeBookLineEditComplete",
    "manuscriptBundleComplete", "productReleaseComplete", "productSourceRepairsComplete",
    "dossierUrlHoldsResolved", "dossierSourceUrlRepairsComplete", "unresolvedInternalPathsResolved",
):
    require(boundary.get(key) is False, f"V9 falsely closes {key}")
require(boundary.get("newDirectQuotesApproved") == 0, "V9 direct-quote boundary drift")
next_tx = current.get("nextTransaction", {})
require(next_tx.get("type") == "STANDALONE_READER_ASSEMBLY", "V9 next transaction type drift")
require(next_tx.get("preferredEntryId") == "HEART-BOOK-IV", "V9 next entry drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-ENTRY-CITATION-PASS-CURRENT-V9-2026-08-04",
    "ENTRY CITATION PASSES COMPLETE = 12 / 18",
    "ENTRY CITATION PASSES OPEN = 6 / 18",
    "ASSEMBLED READERS = 12 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 12 / 12",
    "MISSING STANDALONE FINAL READERS = 6",
    "PRODUCT SOURCE ONLY = 2",
    "RESEARCH DOSSIER ONLY = 4",
    "PRODUCT SOURCE REPAIRS REQUIRED = 4",
    "DOSSIER URL HOLDS RETAINED = 46",
    "DOSSIER SOURCE URL REPAIRS REQUIRED = 2",
    "UNRESOLVED INTERNAL PATHS RETAINED = 1",
    "NEXT READER ASSEMBLY = HEART-BOOK-IV",
    PREVIOUS_BLOB, DELTA_BLOB, ASSEMBLY_BLOB,
):
    require(marker in human, f"V9 human authority marker missing: {marker}")
for forbidden in (
    "ENTRY CITATION PASSES COMPLETE = 18 / 18",
    "PRODUCT SOURCE REPAIRS REQUIRED = 0",
    "DOSSIER URL HOLDS RETAINED = 0",
    "DOSSIER SOURCE URL REPAIRS REQUIRED = 0",
    "UNRESOLVED INTERNAL PATHS RETAINED = 0",
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "WHOLE-BOOK READER ASSEMBLY = COMPLETE",
    "PRODUCT RELEASE = COMPLETE",
    "TODO", "TBD",
):
    require(forbidden not in human, f"V9 human authority contains forbidden marker: {forbidden}")
workflow = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.is_file() else ""
require("validate_heart_entry_citation_pass_current_v9.py" in workflow, "V9 permanent workflow gate missing")

if errors:
    print(f"Heart entry citation pass current V9: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart entry citation pass current V9: PASS — 12/18 completed, 6 open, reviews 12/12, backlog 6 = 2 Product + 4 dossier, 4 Product repairs, 46 dossier holds, next Part IV")
