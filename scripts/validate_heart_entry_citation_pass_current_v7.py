#!/usr/bin/env python3
"""Validate the versioned Heart current citation state V7."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v7-2026-08-04.json"
PREVIOUS = ROOT / "data/heart-entry-citation-pass-current-v6-2026-08-04.json"
DELTA = ROOT / "data/heart-iii1-citation-review-2026-08-04.json"
ASSEMBLY = ROOT / "data/heart-iii1-reader-assembly-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/120_ENTRY_CITATION_PASS_CURRENT_V7_2026-08-04.md"
WORKFLOW = ROOT / ".github/workflows/heart-reader-assembly.yml"
PREVIOUS_BLOB = "fd46d6f99a735301f2966b0e2912eb68805bdff9"
DELTA_BLOB = "220c4f05339298e7f5b7ace1054f43c6286ee71a"
ASSEMBLY_BLOB = "9012cec659ddbac7e65cb0d23ab8a639e0787bab"
COMPLETE = {
    "HEART-BOOK-I1", "HEART-BOOK-I2", "HEART-BOOK-I3", "HEART-BOOK-I4", "HEART-BOOK-II",
    "HEART-BOOK-III1", "HEART-BOOK-III3", "HEART-BOOK-X1", "HEART-BOOK-X2", "HEART-BOOK-X3",
}
OPEN = {
    "HEART-BOOK-III2", "HEART-BOOK-III4", "HEART-BOOK-IV", "HEART-BOOK-V",
    "HEART-BOOK-VI", "HEART-BOOK-VII", "HEART-BOOK-VIII", "HEART-BOOK-IX",
}
PRODUCT = {"HEART-BOOK-III4", "HEART-BOOK-V", "HEART-BOOK-VII"}
DOSSIER = {"HEART-BOOK-III2", "HEART-BOOK-IV", "HEART-BOOK-VI", "HEART-BOOK-VIII", "HEART-BOOK-IX"}
EXPECTED_COUNTS = {
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
    return subprocess.check_output(["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True).strip()


for path, expected in ((PREVIOUS, PREVIOUS_BLOB), (DELTA, DELTA_BLOB), (ASSEMBLY, ASSEMBLY_BLOB)):
    require(path.is_file(), f"immutable authority missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(path) == expected, f"immutable authority blob drift: {path.relative_to(ROOT)}")
previous = read_json(PREVIOUS)
delta = read_json(DELTA)
assembly = read_json(ASSEMBLY)
current = read_json(CURRENT)

require(previous.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V6-2026-08-04", "V6 authority drift")
previous_counts = previous.get("currentCounts", {})
require(previous_counts == {
    "finalBookEntries":18,"entryCitationPassComplete":9,"entryCitationPassOpen":9,
    "assembledReaderEntries":9,"assembledReaderCitationReviewsComplete":9,"missingStandaloneFinalReaders":9,
    "productSourceOnlyEntries":4,"researchDossierOnlyEntries":5,"productSourceLinkRepairsRequired":3,
    "dossierUrlHoldsRetained":15,"unresolvedInternalPathsRetained":1,"newDirectQuotesApproved":0,
}, "V6 count block drift")
require(set(previous.get("completedEntryIds", [])) == COMPLETE - {"HEART-BOOK-III1"}, "V6 completed set drift")
require(set(previous.get("openEntryIds", [])) == OPEN | {"HEART-BOOK-III1"}, "V6 open set drift")

require(delta.get("authorityId") == "HEART-III1-CITATION-REVIEW-2026-08-04", "III.1 delta authority drift")
require(delta.get("entry", {}).get("id") == "HEART-BOOK-III1", "III.1 delta entry drift")
require(delta.get("effectiveState", {}).get("entryCitationPassComplete") is True, "III.1 delta pass incomplete")
require(delta.get("effectiveState", {}).get("assembledReaderCitationReviewComplete") is True, "III.1 reader review incomplete")
require(delta.get("effectiveCounts") == {
    "finalBookEntries":18,"entryCitationPassComplete":10,"entryCitationPassOpen":8,
    "assembledReaders":10,"assembledReaderCitationReviewsComplete":10,"missingStandaloneFinalReaders":8,
    "productSourceOnlyEntries":3,"researchDossierOnlyEntries":5,"productSourceRepairsRequired":4,
    "dossierUrlHoldsRetained":15,"unresolvedInternalPathsRetained":1,"newDirectQuotesApproved":0,
}, "III.1 delta effective counts drift")
holds = delta.get("retainedHoldsAndRepairs", {})
require(len(holds.get("productScriptureLocatorRepairsRequired", [])) == 1, "III.1 locator repair drift")
require(holds.get("productScriptureLocatorRepairsRequired", [{}])[0].get("requiredLocator") == "Флп. 1:6", "III.1 required locator drift")
require(len(holds.get("attributedTheologicalLocatorHolds", [])) == 1, "III.1 attributed hold drift")
require(holds.get("lexicalSupportLocatorHolds", {}).get("count") == 8, "III.1 lexical holds drift")
require(holds.get("existingProductUrlRepairsRetainedFromI3") == 3, "I.3 repairs carry-forward drift")
require(holds.get("part2DossierUrlHoldsRetained") == 15, "Part II holds carry-forward drift")
require(holds.get("part2UnresolvedInternalPathRetained") == 1, "Part II path carry-forward drift")
require(delta.get("readerReview", {}).get("newDirectQuotesApproved") == 0, "III.1 delta direct quote drift")
require(delta.get("publicationBoundary", {}).get("currentV7CompositionComplete") is False, "III.1 delta falsely claims V7")

require(assembly.get("authorityId") == "HEART-III1-READER-ASSEMBLY-2026-08-04", "III.1 assembly authority drift")
require(assembly.get("effectiveCounts", {}).get("assembledReader") == 10, "III.1 assembly reader count drift")
require(assembly.get("effectiveCounts", {}).get("entryCitationPassComplete") == 9, "III.1 assembly must retain pre-review count")

require(current.get("schemaVersion") == 7, "V7 schema drift")
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V7-2026-08-04", "V7 authority drift")
require(current.get("status") == "TEN_ENTRY_PASSES_COMPOSED_ALL_TEN_READERS_REVIEWED_EIGHT_READERS_OPEN", "V7 status drift")
prev_ref = current.get("previousCurrentAuthority", {})
require(prev_ref.get("path") == str(PREVIOUS.relative_to(ROOT)), "V7 previous path drift")
require(prev_ref.get("gitBlob") == PREVIOUS_BLOB, "V7 previous blob drift")
require(prev_ref.get("authorityId") == previous.get("authorityId"), "V7 previous authority mismatch")
require(prev_ref.get("historicalCounts") == {
    "entryCitationPassComplete":9,"entryCitationPassOpen":9,"assembledReaderEntries":9,
    "assembledReaderCitationReviewsComplete":9,"missingStandaloneFinalReaders":9,
    "productSourceOnlyEntries":4,"researchDossierOnlyEntries":5,"productSourceRepairsRequired":3,
}, "V7 historical counts drift")
delta_ref = current.get("deltaReceipt", {})
require(delta_ref.get("gitBlob") == DELTA_BLOB, "V7 delta blob drift")
require(delta_ref.get("authorityId") == delta.get("authorityId"), "V7 delta authority mismatch")
require(delta_ref.get("readerAssemblyGitBlob") == ASSEMBLY_BLOB, "V7 assembly blob drift")
require(delta_ref.get("id") == "HEART-BOOK-III1", "V7 delta ID drift")
require(delta_ref.get("composedCountAfterReceipt") == "10 / 18", "V7 composed count drift")
require(delta_ref.get("productScriptureLocatorRepairsAdded") == 1, "V7 locator-repair delta drift")
require(delta_ref.get("attributedTheologicalLocatorHoldsRetained") == 1, "V7 attributed hold delta drift")
require(delta_ref.get("lexicalSupportLocatorHoldsRetained") == 8, "V7 lexical hold delta drift")
require(delta_ref.get("newDirectQuotesApproved") == 0, "V7 delta quote boundary drift")
require(current.get("currentCounts") == EXPECTED_COUNTS, "V7 count block drift")
require(set(current.get("completedEntryIds", [])) == COMPLETE, "V7 completed set drift")
require(set(current.get("openEntryIds", [])) == OPEN, "V7 open set drift")
lanes = current.get("openEntriesBySourceLane", {})
require(set(lanes.get("productSourceOnly", [])) == PRODUCT, "V7 Product lane drift")
require(set(lanes.get("researchDossierOnly", [])) == DOSSIER, "V7 dossier lane drift")
require(PRODUCT | DOSSIER == OPEN and not PRODUCT & DOSSIER, "V7 source lanes not disjoint/exhaustive")
backlog = current.get("readerAssemblyBacklog", {})
require(backlog.get("removedByDelta") == "HEART-BOOK-III1", "V7 removed delta drift")
require(set(backlog.get("remaining", [])) == OPEN, "V7 remaining-reader set drift")
require(backlog.get("effectiveMissingStandaloneFinalReaders") == 8, "V7 reader backlog count drift")
retained = current.get("retainedRepairAndHoldBacklog", {})
repairs = retained.get("productSourceRepairs", {})
require(repairs.get("totalRequired") == 4 and repairs.get("complete") is False, "V7 Product repair total drift")
require(repairs.get("items") == [
    {"entryId":"HEART-BOOK-I3","kind":"SOURCE_URL_REPAIR","required":3},
    {"entryId":"HEART-BOOK-III1","kind":"SCRIPTURE_LOCATOR_REPAIR","required":1,"surfaceIndex":57,"requiredLocator":"Флп. 1:6"},
], "V7 Product repair item drift")
require(retained.get("iii1AttributedTheologicalLocatorHolds") == {"entryId":"HEART-BOOK-III1","retained":1,"surfaceIndex":26,"readerTransfer":False}, "V7 attributed hold backlog drift")
require(retained.get("iii1LexicalSupportLocatorHolds") == {"entryId":"HEART-BOOK-III1","retained":8,"surfaceIndices":[24,39,44,62,63,64,65,66],"readerTransfer":False}, "V7 lexical hold backlog drift")
require(retained.get("part2DossierUrlHolds") == {"entryId":"HEART-BOOK-II","retained":15,"promoted":0}, "V7 dossier hold backlog drift")
require(retained.get("part2UnresolvedInternalPath") == {"path":"/articles/opinion/","retained":1,"readerTransfer":False}, "V7 unresolved path backlog drift")
boundary = current.get("publicationBoundary", {})
require(boundary.get("allCurrentlyAssembledReadersReviewed") is True, "V7 assembled-reader review state drift")
for key in ("wholeBookReaderAssemblyComplete","wholeBookCitationPassComplete","wholeBookTransitionDedupPassComplete","wholeBookLineEditComplete","manuscriptBundleComplete","productReleaseComplete","productSourceRepairsComplete","dossierUrlHoldsResolved","unresolvedInternalPathsResolved"):
    require(boundary.get(key) is False, f"V7 falsely closes {key}")
require(boundary.get("newDirectQuotesApproved") == 0, "V7 direct quote boundary drift")
next_tx = current.get("nextTransaction", {})
require(next_tx.get("type") == "STANDALONE_READER_ASSEMBLY", "V7 next transaction type drift")
require(next_tx.get("preferredEntryId") == "HEART-BOOK-III2", "V7 next entry drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-ENTRY-CITATION-PASS-CURRENT-V7-2026-08-04",
    "ENTRY CITATION PASSES COMPLETE = 10 / 18", "ENTRY CITATION PASSES OPEN = 8 / 18",
    "ASSEMBLED READERS = 10 / 18", "ASSEMBLED READER CITATION REVIEWS = 10 / 10",
    "MISSING STANDALONE FINAL READERS = 8", "PRODUCT SOURCE ONLY = 3", "RESEARCH DOSSIER ONLY = 5",
    "PRODUCT SOURCE REPAIRS REQUIRED = 4", "DOSSIER URL HOLDS RETAINED = 15",
    "UNRESOLVED INTERNAL PATHS RETAINED = 1", "NEXT READER ASSEMBLY = HEART-BOOK-III2",
    PREVIOUS_BLOB, DELTA_BLOB,
):
    require(marker in human, f"V7 human authority marker missing: {marker}")
for forbidden in (
    "ENTRY CITATION PASSES COMPLETE = 18 / 18", "PRODUCT SOURCE REPAIRS REQUIRED = 0",
    "DOSSIER URL HOLDS RETAINED = 0", "UNRESOLVED INTERNAL PATHS RETAINED = 0",
    "WHOLE-BOOK CITATION PASS = COMPLETE", "WHOLE-BOOK READER ASSEMBLY = COMPLETE",
    "PRODUCT RELEASE = COMPLETE", "TODO", "TBD",
):
    require(forbidden not in human, f"V7 human authority contains forbidden marker: {forbidden}")
workflow = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.is_file() else ""
require("validate_heart_entry_citation_pass_current_v7.py" in workflow, "V7 permanent workflow gate missing")

if errors:
    print(f"Heart entry citation pass current V7: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Heart entry citation pass current V7: PASS — 10/18 completed, 8 open, reviews 10/10, backlog 8 = 3 Product + 5 dossier, 4 Product repairs, next III.2")
