#!/usr/bin/env python3
"""Validate the V3 composed Heart entry-citation-pass current state."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v3-2026-08-04.json"
PREVIOUS = ROOT / "data/heart-entry-citation-pass-current-v2-2026-08-04.json"
I4_REVIEW = ROOT / "data/heart-i4-citation-review-2026-08-04.json"
I4_ASSEMBLY = ROOT / "data/heart-i4-reader-assembly-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/104_ENTRY_CITATION_PASS_CURRENT_V3_2026-08-04.md"

PREVIOUS_BLOB = "66d2f46cf639d9825b5b09fc4e94111be3af2a11"
I4_REVIEW_BLOB = "af16fca67f9eee2763b59c2cd4fae24dc7649388"
I4_ASSEMBLY_BLOB = "83c535047dbc8bb9f19676d539e04a5e700e43ab"
PREVIOUS_COMPLETE = {"HEART-BOOK-I2","HEART-BOOK-III3","HEART-BOOK-X1","HEART-BOOK-X2","HEART-BOOK-X3"}
COMPLETE = PREVIOUS_COMPLETE | {"HEART-BOOK-I4"}
PRODUCT_OPEN = {"HEART-BOOK-I1","HEART-BOOK-I3","HEART-BOOK-III1","HEART-BOOK-III4","HEART-BOOK-V","HEART-BOOK-VII"}
DOSSIER_OPEN = {"HEART-BOOK-II","HEART-BOOK-III2","HEART-BOOK-IV","HEART-BOOK-VI","HEART-BOOK-VIII","HEART-BOOK-IX"}
OPEN = PRODUCT_OPEN | DOSSIER_OPEN
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
    return subprocess.check_output(["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True).strip()


for path, expected in ((PREVIOUS, PREVIOUS_BLOB), (I4_REVIEW, I4_REVIEW_BLOB), (I4_ASSEMBLY, I4_ASSEMBLY_BLOB)):
    require(path.is_file(), f"immutable authority missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(path) == expected, f"immutable authority blob drift: {path.relative_to(ROOT)}")

previous = read_json(PREVIOUS)
review = read_json(I4_REVIEW)
assembly = read_json(I4_ASSEMBLY)
current = read_json(CURRENT)

require(previous.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V2-2026-08-04", "previous V2 authority drift")
require(previous.get("currentCounts") == {
    "finalBookEntries":18,"entryCitationPassComplete":5,"entryCitationPassOpen":13,
    "assembledReaderEntries":5,"assembledReaderCitationReviewsComplete":5,
    "missingStandaloneFinalReaders":13,"productSourceOnlyEntries":7,
    "researchDossierOnlyEntries":6,"newDirectQuotesApproved":0,
}, "previous V2 count block drift")
require(set(previous.get("completedEntryIds", [])) == PREVIOUS_COMPLETE, "previous completed set drift")
require(set(previous.get("openEntryIds", [])) == OPEN | {"HEART-BOOK-I4"}, "previous open set drift")
require("HEART-BOOK-I4" in previous.get("openEntriesBySourceLane", {}).get("productSourceOnly", []), "I.4 absent from previous Product lane")

require(assembly.get("authorityId") == "HEART-I4-READER-ASSEMBLY-2026-08-04", "I.4 assembly authority drift")
require(assembly.get("effectiveState") == {"entryId":"HEART-BOOK-I4","previous":"PRODUCT_SOURCE_ONLY","current":"ASSEMBLED_READER","entryCitationPassComplete":False}, "I.4 assembly historical state drift")
require(assembly.get("effectiveCounts", {}).get("assembledReader") == 6, "I.4 assembly reader count drift")
require(assembly.get("effectiveCounts", {}).get("missingStandaloneFinalReaders") == 12, "I.4 assembly backlog drift")
require(set(assembly.get("remainingReaderAssemblies", [])) == OPEN, "I.4 assembly remaining set drift")

require(review.get("authorityId") == "HEART-I4-CITATION-REVIEW-2026-08-04", "I.4 review authority drift")
require(review.get("entry", {}).get("id") == "HEART-BOOK-I4", "I.4 review entry drift")
require(review.get("disposition", {}).get("entryCitationPassComplete") is True, "I.4 citation pass incomplete")
require(review.get("disposition", {}).get("remainingEntryBlockers") == [], "I.4 citation blockers remain")
require(review.get("disposition", {}).get("newDirectQuotesApproved") == 0, "I.4 review direct-quote drift")
review_boundary = review.get("wholeBookBoundary", {})
require(review_boundary.get("entryCitationPassComplete") == "6 / 18", "I.4 review completion count drift")
require(review_boundary.get("entryCitationPassOpen") == "12 / 18", "I.4 review open count drift")
require(review_boundary.get("assembledReaderEntries") == "6 / 18", "I.4 review reader count drift")
require(review_boundary.get("assembledReaderCitationReviewsComplete") == "6 / 6", "I.4 review assembled-review count drift")
require(review_boundary.get("wholeBookCitationPassComplete") is False, "I.4 review falsely closes whole-book pass")
require(review_boundary.get("productReleaseComplete") is False, "I.4 review falsely closes Product release")

require(current.get("schemaVersion") == 3, "current V3 schema drift")
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V3-2026-08-04", "current V3 authority drift")
require(current.get("status") == "SIX_ENTRY_PASSES_COMPOSED_ALL_SIX_READERS_REVIEWED_TWELVE_READERS_OPEN", "current V3 status drift")
base = current.get("previousCurrentAuthority", {})
require(base.get("gitBlob") == PREVIOUS_BLOB, "current V3 previous blob drift")
require(base.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V2-2026-08-04", "current V3 previous ID drift")
require(base.get("historicalCounts") == {
    "entryCitationPassComplete":5,"entryCitationPassOpen":13,"assembledReaderEntries":5,
    "assembledReaderCitationReviewsComplete":5,"missingStandaloneFinalReaders":13,
}, "current V3 historical counts drift")
delta = current.get("deltaReceipt", {})
require(delta.get("id") == "HEART-BOOK-I4", "current V3 delta entry drift")
require(delta.get("gitBlob") == I4_REVIEW_BLOB, "current V3 review blob drift")
require(delta.get("readerAssemblyGitBlob") == I4_ASSEMBLY_BLOB, "current V3 assembly blob drift")
require(delta.get("composedCountAfterReceipt") == "6 / 18", "current V3 delta count drift")
require(delta.get("newDirectQuotesApproved") == 0, "current V3 delta quote drift")
require(current.get("currentCounts") == {
    "finalBookEntries":18,"entryCitationPassComplete":6,"entryCitationPassOpen":12,
    "assembledReaderEntries":6,"assembledReaderCitationReviewsComplete":6,
    "missingStandaloneFinalReaders":12,"productSourceOnlyEntries":6,
    "researchDossierOnlyEntries":6,"newDirectQuotesApproved":0,
}, "current V3 count block drift")
require(set(current.get("completedEntryIds", [])) == COMPLETE, "current V3 completed set drift")
require(set(current.get("openEntryIds", [])) == OPEN, "current V3 open set drift")
lanes = current.get("openEntriesBySourceLane", {})
require(set(lanes.get("productSourceOnly", [])) == PRODUCT_OPEN, "current V3 Product lane drift")
require(set(lanes.get("researchDossierOnly", [])) == DOSSIER_OPEN, "current V3 dossier lane drift")
require(PRODUCT_OPEN.isdisjoint(DOSSIER_OPEN) and PRODUCT_OPEN | DOSSIER_OPEN == OPEN, "current V3 source lanes invalid")
backlog = current.get("readerAssemblyBacklog", {})
require(backlog.get("removedByDelta") == "HEART-BOOK-I4", "current V3 backlog delta drift")
require(set(backlog.get("remaining", [])) == OPEN, "current V3 backlog set drift")
require(backlog.get("effectiveMissingStandaloneFinalReaders") == 12, "current V3 backlog count drift")
boundary = current.get("publicationBoundary", {})
require(boundary.get("allCurrentlyAssembledReadersReviewed") is True, "current V3 assembled reviews open")
for key in ("wholeBookReaderAssemblyComplete","wholeBookCitationPassComplete","wholeBookTransitionDedupPassComplete","wholeBookLineEditComplete","manuscriptBundleComplete","productReleaseComplete"):
    require(boundary.get(key) is False, f"current V3 falsely closes {key}")
require(boundary.get("newDirectQuotesApproved") == 0, "current V3 direct-quote drift")
next_tx = current.get("nextTransaction", {})
require(next_tx.get("type") == "STANDALONE_READER_ASSEMBLY", "current V3 next type drift")
require(next_tx.get("preferredEntryId") == "HEART-BOOK-I1", "current V3 next entry drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-ENTRY-CITATION-PASS-CURRENT-V3-2026-08-04",
    "ENTRY CITATION PASSES COMPLETE = 6 / 18",
    "ENTRY CITATION PASSES OPEN = 12 / 18",
    "ASSEMBLED READERS = 6 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 6 / 6",
    "MISSING STANDALONE FINAL READERS = 12",
    "PRODUCT SOURCE ONLY = 6",
    "RESEARCH DOSSIER ONLY = 6",
    "NEXT READER ASSEMBLY = HEART-BOOK-I1",
    "WHOLE-BOOK CITATION PASS = OPEN",
    "NEW DIRECT QUOTES APPROVED = 0",
    PREVIOUS_BLOB,
    I4_REVIEW_BLOB,
):
    require(marker in human, f"current V3 human marker missing: {marker}")
for forbidden in ("ENTRY CITATION PASSES COMPLETE = 18 / 18","WHOLE-BOOK CITATION PASS = COMPLETE","PRODUCT RELEASE = COMPLETE","TODO","TBD"):
    require(forbidden not in human, f"current V3 human contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart entry citation pass current V3: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart entry citation pass current V3: PASS — 6/18 completed, 12 open, reviews 6/6, backlog 12 = 6 Product + 6 dossier, next I.1")
