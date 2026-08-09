#!/usr/bin/env python3
"""Validate Heart current native-authority citation state V12."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v12-2026-08-09.json"
PREVIOUS = ROOT / "data/heart-entry-citation-pass-current-v11-2026-08-09.json"
DELTA = ROOT / "data/heart-part5-native-citation-review-2026-08-09.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/136_PART5_NATIVE_ENTRY_CITATION_PASS_2026-08-09.md"
PREVIOUS_BLOB = "58e9dcf7f724b03c7b9d09b49f75922f8bf73b23"
DELTA_BLOB = "3dcf8f2ce5fc05c28203fdabdb5bbec59423aa50"
COMPLETE = {"HEART-BOOK-I2", "HEART-BOOK-II", "HEART-BOOK-III2", "HEART-BOOK-III3", "HEART-BOOK-IV", "HEART-BOOK-V", "HEART-BOOK-X1"}
OPEN = {"HEART-BOOK-I1", "HEART-BOOK-I3", "HEART-BOOK-I4", "HEART-BOOK-III1", "HEART-BOOK-III4", "HEART-BOOK-VI", "HEART-BOOK-VII", "HEART-BOOK-VIII", "HEART-BOOK-IX", "HEART-BOOK-X2", "HEART-BOOK-X3"}
REOPENED = {"HEART-BOOK-I1", "HEART-BOOK-I3", "HEART-BOOK-I4", "HEART-BOOK-III1", "HEART-BOOK-III4", "HEART-BOOK-X2", "HEART-BOOK-X3"}
MISSING_READERS = {"HEART-BOOK-VI", "HEART-BOOK-VII", "HEART-BOOK-VIII", "HEART-BOOK-IX"}
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
    return subprocess.check_output(["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True).strip()


for path, expected in ((PREVIOUS, PREVIOUS_BLOB), (DELTA, DELTA_BLOB)):
    require(path.is_file(), f"immutable authority missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(path) == expected, f"immutable authority blob drift: {path.relative_to(ROOT)}")

previous = read_json(PREVIOUS)
delta = read_json(DELTA)
current = read_json(CURRENT)
require(previous.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V11-2026-08-09", "V11 authority drift")
require(previous.get("currentCounts", {}).get("entryCitationPassComplete") == 6, "V11 completion count drift")
require(previous.get("currentCounts", {}).get("entryCitationPassOpen") == 12, "V11 open count drift")
require(previous.get("currentCounts", {}).get("dossierUrlHoldsRetained") == 55, "V11 hold count drift")
require(set(previous.get("reopenedByNativeSourceAuthority", [])) == REOPENED, "V11 reopened set drift")
require("HEART-BOOK-V" in set(previous.get("openEntryIds", [])), "V11 no longer leaves Part V open")
require(previous.get("nextTransaction", {}).get("preferredEntryId") == "HEART-BOOK-V", "V11 next entry drift")

require(delta.get("authorityId") == "HEART-PART5-NATIVE-CITATION-REVIEW-2026-08-09", "Part V delta authority drift")
require(delta.get("entry", {}).get("id") == "HEART-BOOK-V", "Part V delta identity drift")
require(delta.get("disposition", {}).get("entryCitationPassComplete") is True, "Part V delta not complete")
require(delta.get("disposition", {}).get("assembledReaderCitationReviewComplete") is True, "Part V reader review not complete")
require(delta.get("disposition", {}).get("newDirectQuotesApproved") == 0, "Part V delta approves new quotes")
require(delta.get("retainedRepairAndHoldBacklog") == {
    "historicalProductSourceRepairsRequired": 4,
    "historicalDossierUrlHoldsRetained": 55,
    "part5DossierUrlHoldsAdded": 12,
    "currentDossierUrlHoldsRetained": 67,
    "dossierSourceUrlRepairsRequired": 2,
    "part5NewSourceUrlRepairs": 0,
    "unresolvedInternalPathsRetained": 1,
    "part5NewUnresolvedInternalPaths": 0,
    "nativeSourceAuthorityReconciliationsOpen": 7,
    "silentlyClosedItems": 0,
}, "Part V delta backlog drift")

require(current.get("schemaVersion") == 12, "V12 schema drift")
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V12-2026-08-09", "V12 authority drift")
require(current.get("status") == "PART5_NATIVE_AUTHORITY_PASS_COMPOSED_SEVEN_COMPLETE_SEVEN_REOPENED", "V12 status drift")
prev_ref = current.get("previousCurrentAuthority", {})
require(prev_ref.get("path") == str(PREVIOUS.relative_to(ROOT)), "V12 previous path drift")
require(prev_ref.get("gitBlob") == PREVIOUS_BLOB, "V12 previous blob drift")
require(prev_ref.get("authorityId") == previous.get("authorityId"), "V12 previous authority mismatch")
receipt_ref = current.get("deltaReceipt", {})
require(receipt_ref.get("path") == str(DELTA.relative_to(ROOT)), "V12 delta path drift")
require(receipt_ref.get("gitBlob") == DELTA_BLOB, "V12 delta blob drift")
require(receipt_ref.get("authorityId") == delta.get("authorityId"), "V12 delta authority mismatch")
require(receipt_ref.get("entryId") == "HEART-BOOK-V" and receipt_ref.get("entryOrder") == 11, "V12 delta identity drift")
require(receipt_ref.get("part5DossierUrlHoldsAdded") == 12, "V12 Part V hold delta drift")
require(receipt_ref.get("part5NewSourceUrlRepairs") == 0, "V12 Part V source repair delta drift")
require(receipt_ref.get("part5NewUnresolvedInternalPaths") == 0, "V12 Part V unresolved path delta drift")
require(receipt_ref.get("newDirectQuotesApproved") == 0, "V12 quote delta drift")

expected_counts = {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 7,
    "entryCitationPassOpen": 11,
    "assembledReaderEntries": 14,
    "assembledReaderCitationReviewsComplete": 7,
    "assembledReadersAwaitingCitationReviewOrNativeReconciliation": 7,
    "missingStandaloneFinalReaders": 4,
    "productSourceOnlyMissingReaderEntries": 1,
    "researchDossierOnlyMissingReaderEntries": 3,
    "nativeAuthorityReopenedCompletedEntries": 7,
    "productSourceRepairsRequiredRetained": 4,
    "historicalDossierUrlHoldsRetained": 55,
    "part5DossierUrlHoldsRetained": 12,
    "dossierUrlHoldsRetained": 67,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "newDirectQuotesApproved": 0,
}
require(current.get("currentCounts") == expected_counts, "V12 current-count block drift")
require(set(current.get("completedEntryIds", [])) == COMPLETE, "V12 completed set drift")
require(set(current.get("openEntryIds", [])) == OPEN, "V12 open set drift")
require(COMPLETE.isdisjoint(OPEN) and len(COMPLETE | OPEN) == 18, "V12 complete/open partition drift")
require(set(current.get("reopenedByNativeSourceAuthority", [])) == REOPENED, "V12 reopened set drift")
require(set(previous.get("completedEntryIds", [])) | {"HEART-BOOK-V"} == COMPLETE, "V12 completion delta is not exactly Part V")
require(set(previous.get("openEntryIds", [])) - {"HEART-BOOK-V"} == OPEN, "V12 open delta is not exactly Part V")

reader = current.get("readerState", {})
require(reader.get("assembledReaders") == 14, "V12 assembled-reader count drift")
require(set(reader.get("missingStandaloneReaders", [])) == MISSING_READERS, "V12 missing-reader set drift")
require(reader.get("assembledReaderAwaitingFirstCitationPass") == [], "V12 still leaves first-pass assembled reader")
require(set(reader.get("assembledReadersNeedingNativeSourceReconciliation", [])) == REOPENED, "V12 reconciliation reader set drift")

backlog = current.get("retainedBacklog", {})
require(backlog == {
    "historicalProductSourceRepairsRequired": 4,
    "historicalDossierUrlHoldsRetained": 55,
    "part5DossierUrlHoldsRetained": 12,
    "dossierUrlHoldsRetained": 67,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "sourceAuthorityReconciliationsOpen": 7,
    "silentlyClosedItems": 0,
}, "V12 retained backlog drift")

boundary = current.get("publicationBoundary", {})
for key in (
    "allCurrentlyAssembledReadersReviewedAgainstCurrentAuthority",
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
    "nativeSourceAuthorityReconciliationComplete",
):
    require(boundary.get(key) is False, f"V12 falsely closes publication boundary: {key}")
require(boundary.get("newDirectQuotesApproved") == 0, "V12 publication boundary approves direct quotes")
next_tx = current.get("nextTransaction", {})
require(next_tx.get("type") == "NATIVE_SOURCE_AUTHORITY_RECONCILIATION", "V12 next transaction type drift")
require(next_tx.get("preferredEntryId") == "HEART-BOOK-X2", "V12 next entry must be X.2")

require(HUMAN.is_file(), "V12/Part V human mirror missing")
if HUMAN.is_file():
    human = HUMAN.read_text(encoding="utf-8")
    for marker in (
        "CURRENT NATIVE-AUTHORITY CITATION PASSES COMPLETE = 7 / 18",
        "CURRENT CITATION PASSES OPEN = 11 / 18",
        "CURRENT DOSSIER URL HOLDS = 67 = 55 retained + 12 Part V",
        "HEART-BOOK-X2 NATIVE SOURCE AUTHORITY RECONCILIATION",
    ):
        require(marker in human, f"V12 human mirror missing marker: {marker}")

if errors:
    print("Heart entry citation pass current V12: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Heart entry citation pass current V12: PASS — Part V closes exactly 6→7; seven native reconciliations and 67 holds remain explicit")
