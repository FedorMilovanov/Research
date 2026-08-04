#!/usr/bin/env python3
"""Validate the versioned Heart current citation state V8."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v8-2026-08-04.json"
PREVIOUS = ROOT / "data/heart-entry-citation-pass-current-v7-2026-08-04.json"
DELTA = ROOT / "data/heart-iii2-citation-review-2026-08-04.json"
ASSEMBLY = ROOT / "data/heart-iii2-reader-assembly-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/124_ENTRY_CITATION_PASS_CURRENT_V8_2026-08-04.md"
WORKFLOW = ROOT / ".github/workflows/heart-reader-assembly.yml"
PREVIOUS_BLOB = "86c932764ca2eba3bec726876f2cb73a0c78e762"
DELTA_BLOB = "bda547518627241c96942b256134dbbcd12d29f9"
ASSEMBLY_BLOB = "82e2a70977d67591c3a290248f102601c7c4d5dc"
COMPLETE = {
    "HEART-BOOK-I1", "HEART-BOOK-I2", "HEART-BOOK-I3", "HEART-BOOK-I4", "HEART-BOOK-II",
    "HEART-BOOK-III1", "HEART-BOOK-III2", "HEART-BOOK-III3",
    "HEART-BOOK-X1", "HEART-BOOK-X2", "HEART-BOOK-X3",
}
OPEN = {
    "HEART-BOOK-III4", "HEART-BOOK-IV", "HEART-BOOK-V", "HEART-BOOK-VI",
    "HEART-BOOK-VII", "HEART-BOOK-VIII", "HEART-BOOK-IX",
}
PRODUCT = {"HEART-BOOK-III4", "HEART-BOOK-V", "HEART-BOOK-VII"}
DOSSIER = {"HEART-BOOK-IV", "HEART-BOOK-VI", "HEART-BOOK-VIII", "HEART-BOOK-IX"}
EXPECTED_COUNTS = {
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

require(previous.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V7-2026-08-04", "V7 authority drift")
require(previous.get("currentCounts") == {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 10,
    "entryCitationPassOpen": 8,
    "assembledReaderEntries": 10,
    "assembledReaderCitationReviewsComplete": 10,
    "missingStandaloneFinalReaders": 8,
    "productSourceOnlyEntries": 3,
    "researchDossierOnlyEntries": 5,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 15,
    "unresolvedInternalPathsRetained": 1,
    "newDirectQuotesApproved": 0,
}, "V7 count block drift")
require(set(previous.get("completedEntryIds", [])) == COMPLETE - {"HEART-BOOK-III2"}, "V7 completed set drift")
require(set(previous.get("openEntryIds", [])) == OPEN | {"HEART-BOOK-III2"}, "V7 open set drift")

require(delta.get("authorityId") == "HEART-III2-CITATION-REVIEW-2026-08-04", "III.2 delta authority drift")
require(delta.get("entry", {}).get("id") == "HEART-BOOK-III2", "III.2 delta entry drift")
require(delta.get("effectiveState") == {
    "previous": "ASSEMBLED_READER_CITATION_OPEN",
    "current": "ENTRY_CITATION_PASS_COMPLETE",
    "entryCitationPassComplete": True,
    "assembledReaderCitationReviewComplete": True,
}, "III.2 delta effective state drift")
require(delta.get("effectiveCounts") == {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 11,
    "entryCitationPassOpen": 7,
    "assembledReaders": 11,
    "assembledReaderCitationReviewsComplete": 11,
    "missingStandaloneFinalReaders": 7,
    "productSourceOnlyEntries": 3,
    "researchDossierOnlyEntries": 4,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 40,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "newDirectQuotesApproved": 0,
}, "III.2 delta effective counts drift")
holds = delta.get("retainedHoldsAndRepairs", {})
require(holds == {
    "productSourceRepairsRequired": 4,
    "priorPart2DossierUrlHoldsRetained": 15,
    "iii2DossierUrlHoldsAdded": 25,
    "totalDossierUrlHoldsRetained": 40,
    "iii2DossierSourceUrlRepairsRequired": 2,
    "part2UnresolvedInternalPathsRetained": 1,
    "iii2UnresolvedInternalPathsAdded": 0,
}, "III.2 delta backlog drift")
external = delta.get("externalLinkDisposition", {})
require(external.get("counts") == {
    "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE": 35,
    "DOSSIER_SUPPORT_RECORD_NO_READER_TRANSFER": 5,
    "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD": 25,
    "DOSSIER_SOURCE_URL_REPAIR_REQUIRED": 2,
}, "III.2 URL disposition drift")
require(external.get("unique") == 67 and external.get("occurrences") == 97, "III.2 URL totals drift")
require(external.get("readerTransfer") == 0 and external.get("newDirectQuotesApproved") == 0, "III.2 URL boundary drift")
internal = delta.get("internalPathDisposition", {})
require(internal.get("status") == "EXTERNAL_URL_PATH_FRAGMENT_FALSE_POSITIVE", "III.2 false-positive path disposition drift")
require(internal.get("unresolvedInternalPathsAdded") == 0, "III.2 falsely adds unresolved internal path")
require(delta.get("publicationBoundary", {}).get("currentV8CompositionComplete") is False, "III.2 delta falsely claims V8")
require(delta.get("readerReview", {}).get("newDirectQuotesApproved") == 0, "III.2 delta direct quote drift")

require(assembly.get("authorityId") == "HEART-III2-READER-ASSEMBLY-2026-08-04", "III.2 assembly authority drift")
require(assembly.get("effectiveCounts", {}).get("assembledReaders") == 11, "III.2 assembly reader count drift")
require(assembly.get("effectiveCounts", {}).get("entryCitationPassComplete") == 10, "III.2 assembly must retain pre-review count")

require(current.get("schemaVersion") == 8, "V8 schema drift")
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V8-2026-08-04", "V8 authority drift")
require(current.get("status") == "ELEVEN_ENTRY_PASSES_COMPOSED_ALL_ELEVEN_READERS_REVIEWED_SEVEN_READERS_OPEN", "V8 status drift")
previous_ref = current.get("previousCurrentAuthority", {})
require(previous_ref.get("path") == str(PREVIOUS.relative_to(ROOT)), "V8 previous path drift")
require(previous_ref.get("gitBlob") == PREVIOUS_BLOB, "V8 previous blob drift")
require(previous_ref.get("authorityId") == previous.get("authorityId"), "V8 previous authority mismatch")
require(previous_ref.get("historicalCounts") == {
    "entryCitationPassComplete": 10,
    "entryCitationPassOpen": 8,
    "assembledReaderEntries": 10,
    "assembledReaderCitationReviewsComplete": 10,
    "missingStandaloneFinalReaders": 8,
    "productSourceOnlyEntries": 3,
    "researchDossierOnlyEntries": 5,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 15,
    "unresolvedInternalPathsRetained": 1,
}, "V8 historical count block drift")

delta_ref = current.get("deltaReceipt", {})
require(delta_ref.get("gitBlob") == DELTA_BLOB, "V8 delta blob drift")
require(delta_ref.get("authorityId") == delta.get("authorityId"), "V8 delta authority mismatch")
require(delta_ref.get("readerAssemblyGitBlob") == ASSEMBLY_BLOB, "V8 assembly blob drift")
require(delta_ref.get("id") == "HEART-BOOK-III2", "V8 delta ID drift")
require(delta_ref.get("composedCountAfterReceipt") == "11 / 18", "V8 composed count drift")
require(delta_ref.get("dossierUrlHoldsAdded") == 25, "V8 dossier hold delta drift")
require(delta_ref.get("dossierSourceUrlRepairsAdded") == 2, "V8 dossier repair delta drift")
require(delta_ref.get("unresolvedInternalPathsAdded") == 0, "V8 unresolved-path delta drift")
require(delta_ref.get("newDirectQuotesApproved") == 0, "V8 direct quote delta drift")

require(current.get("currentCounts") == EXPECTED_COUNTS, "V8 count block drift")
require(set(current.get("completedEntryIds", [])) == COMPLETE, "V8 completed set drift")
require(set(current.get("openEntryIds", [])) == OPEN, "V8 open set drift")
lanes = current.get("openEntriesBySourceLane", {})
require(set(lanes.get("productSourceOnly", [])) == PRODUCT, "V8 Product lane drift")
require(set(lanes.get("researchDossierOnly", [])) == DOSSIER, "V8 dossier lane drift")
require(PRODUCT | DOSSIER == OPEN and not PRODUCT & DOSSIER, "V8 source lanes are not disjoint/exhaustive")
backlog = current.get("readerAssemblyBacklog", {})
require(backlog.get("removedByDelta") == "HEART-BOOK-III2", "V8 removed delta drift")
require(set(backlog.get("remaining", [])) == OPEN, "V8 remaining-reader set drift")
require(backlog.get("effectiveMissingStandaloneFinalReaders") == 7, "V8 reader backlog count drift")

retained = current.get("retainedRepairAndHoldBacklog", {})
product_repairs = retained.get("productSourceRepairs", {})
require(product_repairs.get("totalRequired") == 4 and product_repairs.get("complete") is False, "V8 Product repair total drift")
require(product_repairs.get("items") == [
    {"entryId": "HEART-BOOK-I3", "kind": "SOURCE_URL_REPAIR", "required": 3},
    {"entryId": "HEART-BOOK-III1", "kind": "SCRIPTURE_LOCATOR_REPAIR", "required": 1, "surfaceIndex": 57, "requiredLocator": "Флп. 1:6"},
], "V8 Product repair items drift")
require(retained.get("iii1AttributedTheologicalLocatorHolds") == {
    "entryId": "HEART-BOOK-III1", "retained": 1, "surfaceIndex": 26, "readerTransfer": False
}, "V8 III.1 attributed hold drift")
require(retained.get("iii1LexicalSupportLocatorHolds") == {
    "entryId": "HEART-BOOK-III1", "retained": 8,
    "surfaceIndices": [24, 39, 44, 62, 63, 64, 65, 66], "readerTransfer": False
}, "V8 III.1 lexical holds drift")
require(retained.get("dossierUrlHolds") == {
    "totalRetained": 40,
    "components": [
        {"entryId": "HEART-BOOK-II", "retained": 15, "promoted": 0},
        {"entryId": "HEART-BOOK-III2", "retained": 25, "promoted": 0},
    ],
}, "V8 dossier hold composition drift")
require(retained.get("iii2DossierSourceUrlRepairs") == {
    "entryId": "HEART-BOOK-III2",
    "required": 2,
    "complete": False,
    "tokens": [
        "https://www.monergism.com/regeneration-6`",
        "https://www.reformedreader.org/ccc/1689lbc/english/Chapter10.htm**",
    ],
}, "V8 dossier source-repair backlog drift")
require(retained.get("part2UnresolvedInternalPath") == {
    "path": "/articles/opinion/", "retained": 1, "readerTransfer": False
}, "V8 unresolved Part II path drift")
require(retained.get("iii2FalsePositiveInternalPath") == {
    "path": "/articles/onsite/",
    "status": "EXTERNAL_URL_PATH_FRAGMENT_FALSE_POSITIVE",
    "unresolvedInternalPathsAdded": 0,
    "readerTransfer": False,
}, "V8 III.2 false-positive path drift")

boundary = current.get("publicationBoundary", {})
require(boundary.get("allCurrentlyAssembledReadersReviewed") is True, "V8 assembled-reader review state drift")
for key in (
    "wholeBookReaderAssemblyComplete", "wholeBookCitationPassComplete",
    "wholeBookTransitionDedupPassComplete", "wholeBookLineEditComplete",
    "manuscriptBundleComplete", "productReleaseComplete", "productSourceRepairsComplete",
    "dossierUrlHoldsResolved", "dossierSourceUrlRepairsComplete", "unresolvedInternalPathsResolved",
):
    require(boundary.get(key) is False, f"V8 falsely closes {key}")
require(boundary.get("newDirectQuotesApproved") == 0, "V8 direct quote boundary drift")
next_tx = current.get("nextTransaction", {})
require(next_tx.get("type") == "STANDALONE_READER_ASSEMBLY", "V8 next transaction type drift")
require(next_tx.get("preferredEntryId") == "HEART-BOOK-III4", "V8 next entry drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-ENTRY-CITATION-PASS-CURRENT-V8-2026-08-04",
    "ENTRY CITATION PASSES COMPLETE = 11 / 18",
    "ENTRY CITATION PASSES OPEN = 7 / 18",
    "ASSEMBLED READERS = 11 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 11 / 11",
    "MISSING STANDALONE FINAL READERS = 7",
    "PRODUCT SOURCE ONLY = 3",
    "RESEARCH DOSSIER ONLY = 4",
    "PRODUCT SOURCE REPAIRS REQUIRED = 4",
    "DOSSIER URL HOLDS RETAINED = 40",
    "DOSSIER SOURCE URL REPAIRS REQUIRED = 2",
    "UNRESOLVED INTERNAL PATHS RETAINED = 1",
    "NEXT READER ASSEMBLY = HEART-BOOK-III4",
    PREVIOUS_BLOB,
    DELTA_BLOB,
):
    require(marker in human, f"V8 human authority marker missing: {marker}")
for forbidden in (
    "ENTRY CITATION PASSES COMPLETE = 18 / 18",
    "PRODUCT SOURCE REPAIRS REQUIRED = 0",
    "DOSSIER URL HOLDS RETAINED = 0",
    "DOSSIER SOURCE URL REPAIRS REQUIRED = 0",
    "UNRESOLVED INTERNAL PATHS RETAINED = 0",
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "WHOLE-BOOK READER ASSEMBLY = COMPLETE",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"V8 human authority contains forbidden marker: {forbidden}")
workflow = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.is_file() else ""
require("validate_heart_entry_citation_pass_current_v8.py" in workflow, "V8 permanent workflow gate missing")

if errors:
    print(f"Heart entry citation pass current V8: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart entry citation pass current V8: PASS — 11/18 completed, 7 open, reviews 11/11, backlog 7 = 3 Product + 4 dossier, 4 Product repairs, 40 dossier holds, 2 dossier URL repairs, next III.4")
