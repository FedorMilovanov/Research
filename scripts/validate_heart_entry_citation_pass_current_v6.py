#!/usr/bin/env python3
"""Validate the versioned Heart current citation state V6."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v6-2026-08-04.json"
PREVIOUS = ROOT / "data/heart-entry-citation-pass-current-v5-2026-08-04.json"
DELTA = ROOT / "data/heart-part2-citation-review-2026-08-04.json"
ASSEMBLY = ROOT / "data/heart-part2-reader-assembly-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/116_ENTRY_CITATION_PASS_CURRENT_V6_2026-08-04.md"
PREVIOUS_BLOB = "2ba8c381e636a9f1148fa30e3f010d595feb42a6"
DELTA_BLOB = "c746a626953ee57a394a41a5f82a83630f1cd782"
ASSEMBLY_BLOB = "7fe129945caa023e796e592d0c8fc07a01a89f69"
COMPLETE = {
    "HEART-BOOK-I1", "HEART-BOOK-I2", "HEART-BOOK-I3", "HEART-BOOK-I4",
    "HEART-BOOK-II", "HEART-BOOK-III3", "HEART-BOOK-X1", "HEART-BOOK-X2", "HEART-BOOK-X3",
}
OPEN = {
    "HEART-BOOK-III1", "HEART-BOOK-III2", "HEART-BOOK-III4", "HEART-BOOK-IV",
    "HEART-BOOK-V", "HEART-BOOK-VI", "HEART-BOOK-VII", "HEART-BOOK-VIII", "HEART-BOOK-IX",
}
PRODUCT = {"HEART-BOOK-III1", "HEART-BOOK-III4", "HEART-BOOK-V", "HEART-BOOK-VII"}
DOSSIER = {"HEART-BOOK-III2", "HEART-BOOK-IV", "HEART-BOOK-VI", "HEART-BOOK-VIII", "HEART-BOOK-IX"}
EXPECTED_COUNTS = {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 9,
    "entryCitationPassOpen": 9,
    "assembledReaderEntries": 9,
    "assembledReaderCitationReviewsComplete": 9,
    "missingStandaloneFinalReaders": 9,
    "productSourceOnlyEntries": 4,
    "researchDossierOnlyEntries": 5,
    "productSourceLinkRepairsRequired": 3,
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

require(previous.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V5-2026-08-04", "V5 authority drift")
previous_counts = previous.get("currentCounts", {})
require(previous_counts.get("entryCitationPassComplete") == 8, "V5 completion count drift")
require(previous_counts.get("entryCitationPassOpen") == 10, "V5 open count drift")
require(previous_counts.get("assembledReaderEntries") == 8, "V5 reader count drift")
require(previous_counts.get("assembledReaderCitationReviewsComplete") == 8, "V5 review count drift")
require(previous_counts.get("missingStandaloneFinalReaders") == 10, "V5 backlog count drift")
require(previous_counts.get("productSourceOnlyEntries") == 4, "V5 Product lane drift")
require(previous_counts.get("researchDossierOnlyEntries") == 6, "V5 dossier lane drift")
require(set(previous.get("completedEntryIds", [])) == COMPLETE - {"HEART-BOOK-II"}, "V5 completed set drift")
require(set(previous.get("openEntryIds", [])) == OPEN | {"HEART-BOOK-II"}, "V5 open set drift")

require(delta.get("authorityId") == "HEART-PART2-CITATION-REVIEW-2026-08-04", "Part II delta authority drift")
require(delta.get("entry", {}).get("id") == "HEART-BOOK-II", "Part II delta entry drift")
require(delta.get("effectiveState") == {"entryId":"HEART-BOOK-II","previous":"ASSEMBLED_READER_CITATION_OPEN","current":"ENTRY_CITATION_PASS_COMPLETE"}, "Part II delta transition drift")
require(delta.get("effectiveCounts", {}).get("entryCitationPassComplete") == 9, "Part II delta completion count drift")
require(delta.get("effectiveCounts", {}).get("assembledReader") == 9, "Part II delta reader count drift")
require(delta.get("externalLinkReview", {}).get("statusCounts", {}).get("DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD") == 15, "Part II URL hold count drift")
require(delta.get("internalLinkReview", {}).get("status") == "UNRESOLVED_GENERIC_PATH_NO_PRODUCT_TARGET_NO_READER_TRANSFER", "Part II unresolved path status drift")
require(delta.get("disposition", {}).get("newDirectQuotesApproved") == 0, "Part II delta direct quote drift")
require(delta.get("publicationBoundary", {}).get("part2EntryCitationPassComplete") is True, "Part II delta pass incomplete")
require(delta.get("publicationBoundary", {}).get("wholeBookCitationPassComplete") is False, "Part II delta falsely closes whole-book pass")
require(delta.get("publicationBoundary", {}).get("productSourceLinkRepairsComplete") is False, "Part II delta falsely closes Product repairs")

require(assembly.get("authorityId") == "HEART-PART2-READER-ASSEMBLY-2026-08-04", "Part II assembly authority drift")
require(assembly.get("effectiveCounts", {}).get("assembledReader") == 9, "Part II assembly count drift")
require(assembly.get("effectiveCounts", {}).get("entryCitationPassComplete") == 8, "Part II assembly must retain pre-review count")

require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V6-2026-08-04", "V6 authority drift")
require(current.get("status") == "NINE_ENTRY_PASSES_COMPOSED_ALL_NINE_READERS_REVIEWED_NINE_READERS_OPEN", "V6 status drift")
prev_ref = current.get("previousCurrentAuthority", {})
require(prev_ref.get("gitBlob") == PREVIOUS_BLOB, "V6 previous blob drift")
require(prev_ref.get("authorityId") == previous.get("authorityId"), "V6 previous authority mismatch")
delta_ref = current.get("deltaReceipt", {})
require(delta_ref.get("gitBlob") == DELTA_BLOB, "V6 delta blob drift")
require(delta_ref.get("authorityId") == delta.get("authorityId"), "V6 delta authority mismatch")
require(delta_ref.get("readerAssemblyGitBlob") == ASSEMBLY_BLOB, "V6 assembly blob drift")
require(delta_ref.get("id") == "HEART-BOOK-II", "V6 delta ID drift")
require(delta_ref.get("composedCountAfterReceipt") == "9 / 18", "V6 delta count drift")
require(delta_ref.get("dossierUrlHoldsRetained") == 15, "V6 URL hold delta drift")
require(delta_ref.get("unresolvedInternalPathsRetained") == 1, "V6 unresolved-path delta drift")
require(delta_ref.get("newDirectQuotesApproved") == 0, "V6 delta quote boundary drift")
require(current.get("currentCounts") == EXPECTED_COUNTS, "V6 count block drift")
require(set(current.get("completedEntryIds", [])) == COMPLETE, "V6 completed set drift")
require(set(current.get("openEntryIds", [])) == OPEN, "V6 open set drift")
lanes = current.get("openEntriesBySourceLane", {})
require(set(lanes.get("productSourceOnly", [])) == PRODUCT, "V6 Product lane drift")
require(set(lanes.get("researchDossierOnly", [])) == DOSSIER, "V6 dossier lane drift")
require(PRODUCT | DOSSIER == OPEN and not PRODUCT & DOSSIER, "V6 source lanes not disjoint/exhaustive")
backlog = current.get("readerAssemblyBacklog", {})
require(backlog.get("removedByDelta") == "HEART-BOOK-II", "V6 removed delta drift")
require(set(backlog.get("remaining", [])) == OPEN, "V6 remaining-reader set drift")
require(backlog.get("effectiveMissingStandaloneFinalReaders") == 9, "V6 reader backlog count drift")
retained = current.get("retainedRepairAndHoldBacklog", {})
require(retained.get("productSourceLinkRepairs", {}) == {"entryId":"HEART-BOOK-I3","required":3,"complete":False}, "V6 Product repair backlog drift")
require(retained.get("part2DossierUrlHolds", {}) == {"entryId":"HEART-BOOK-II","retained":15,"promoted":0}, "V6 dossier hold backlog drift")
require(retained.get("part2UnresolvedInternalPath", {}) == {"path":"/articles/opinion/","retained":1,"readerTransfer":False}, "V6 unresolved path backlog drift")
boundary = current.get("publicationBoundary", {})
require(boundary.get("allCurrentlyAssembledReadersReviewed") is True, "V6 assembled-reader review state drift")
for key in ("wholeBookReaderAssemblyComplete","wholeBookCitationPassComplete","wholeBookTransitionDedupPassComplete","wholeBookLineEditComplete","manuscriptBundleComplete","productReleaseComplete","productSourceLinkRepairsComplete","dossierUrlHoldsResolved","unresolvedInternalPathsResolved"):
    require(boundary.get(key) is False, f"V6 falsely closes {key}")
require(boundary.get("newDirectQuotesApproved") == 0, "V6 direct quote boundary drift")
next_tx = current.get("nextTransaction", {})
require(next_tx.get("type") == "STANDALONE_READER_ASSEMBLY", "V6 next transaction type drift")
require(next_tx.get("preferredEntryId") == "HEART-BOOK-III1", "V6 next entry drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in ("HEART-ENTRY-CITATION-PASS-CURRENT-V6-2026-08-04","ENTRY CITATION PASSES COMPLETE = 9 / 18","ENTRY CITATION PASSES OPEN = 9 / 18","ASSEMBLED READERS = 9 / 18","ASSEMBLED READER CITATION REVIEWS = 9 / 9","MISSING STANDALONE FINAL READERS = 9","PRODUCT SOURCE ONLY = 4","RESEARCH DOSSIER ONLY = 5","PRODUCT SOURCE LINK REPAIRS REQUIRED = 3","DOSSIER URL HOLDS RETAINED = 15","UNRESOLVED INTERNAL PATHS RETAINED = 1","NEXT READER ASSEMBLY = HEART-BOOK-III1",PREVIOUS_BLOB,DELTA_BLOB):
    require(marker in human, f"V6 human authority marker missing: {marker}")
for forbidden in ("ENTRY CITATION PASSES COMPLETE = 18 / 18","PRODUCT SOURCE LINK REPAIRS REQUIRED = 0","DOSSIER URL HOLDS RETAINED = 0","UNRESOLVED INTERNAL PATHS RETAINED = 0","WHOLE-BOOK CITATION PASS = COMPLETE","WHOLE-BOOK READER ASSEMBLY = COMPLETE","PRODUCT RELEASE = COMPLETE","TODO","TBD"):
    require(forbidden not in human, f"V6 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart entry citation pass current V6: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Heart entry citation pass current V6: PASS — 9/18 completed, 9 open, reviews 9/9, backlog 9 = 4 Product + 5 dossier, 3 Product repairs, 15 dossier holds, next III.1")
