#!/usr/bin/env python3
"""Validate the composed current Heart entry-citation-pass state."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "data/heart-entry-citation-pass-current-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
X3_ASSEMBLY = ROOT / "data/heart-x3-reader-assembly-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/96_ENTRY_CITATION_PASS_CURRENT_OVERLAY_2026-08-04.md"

EXPECTED_RECEIPTS = [
    {
        "order": 2,
        "id": "HEART-BOOK-I2",
        "path": ROOT / "data/heart-i2-citation-review-2026-08-04.json",
        "blob": "c46b8879c8b48f186c74d415e1e1e059b919f1fa",
        "authority": "HEART-I2-CITATION-REVIEW-2026-08-04",
        "count": "1 / 18",
    },
    {
        "order": 8,
        "id": "HEART-BOOK-III3",
        "path": ROOT / "data/heart-iii3-citation-review-2026-08-04.json",
        "blob": "0f79e1ef077fbf77d05fd475f57717d7d10944dd",
        "authority": "HEART-III3-CITATION-REVIEW-2026-08-04",
        "count": "2 / 18",
    },
    {
        "order": 16,
        "id": "HEART-BOOK-X1",
        "path": ROOT / "data/heart-x1-citation-review-2026-08-04.json",
        "blob": "81c4f9f0354ed3e156a4f84f223035801795046e",
        "authority": "HEART-X1-CITATION-REVIEW-2026-08-04",
        "count": "3 / 18",
    },
    {
        "order": 18,
        "id": "HEART-BOOK-X3",
        "path": ROOT / "data/heart-x3-citation-review-2026-08-04.json",
        "blob": "fdb8337e9017dc33789d22334eec70d9963be354",
        "authority": "HEART-X3-CITATION-REVIEW-2026-08-04",
        "count": "4 / 18",
    },
]
EXPECTED_COMPLETED = {
    "HEART-BOOK-I2",
    "HEART-BOOK-III3",
    "HEART-BOOK-X1",
    "HEART-BOOK-X3",
}
EXPECTED_OPEN = {
    "HEART-BOOK-I1",
    "HEART-BOOK-I3",
    "HEART-BOOK-I4",
    "HEART-BOOK-II",
    "HEART-BOOK-III1",
    "HEART-BOOK-III2",
    "HEART-BOOK-III4",
    "HEART-BOOK-IV",
    "HEART-BOOK-V",
    "HEART-BOOK-VI",
    "HEART-BOOK-VII",
    "HEART-BOOK-VIII",
    "HEART-BOOK-IX",
    "HEART-BOOK-X2",
}
EXPECTED_PRODUCT_OPEN = {
    "HEART-BOOK-I1",
    "HEART-BOOK-I3",
    "HEART-BOOK-I4",
    "HEART-BOOK-III1",
    "HEART-BOOK-III4",
    "HEART-BOOK-V",
    "HEART-BOOK-VII",
    "HEART-BOOK-X2",
}
EXPECTED_DOSSIER_OPEN = {
    "HEART-BOOK-II",
    "HEART-BOOK-III2",
    "HEART-BOOK-IV",
    "HEART-BOOK-VI",
    "HEART-BOOK-VIII",
    "HEART-BOOK-IX",
}
EXPECTED_EXPLICIT_NINE = {
    "HEART-BOOK-I4",
    "HEART-BOOK-II",
    "HEART-BOOK-III2",
    "HEART-BOOK-IV",
    "HEART-BOOK-VI",
    "HEART-BOOK-VII",
    "HEART-BOOK-VIII",
    "HEART-BOOK-IX",
    "HEART-BOOK-X2",
}
EXPECTED_ADDITIONAL_FIVE = {
    "HEART-BOOK-I1",
    "HEART-BOOK-I3",
    "HEART-BOOK-III1",
    "HEART-BOOK-III4",
    "HEART-BOOK-V",
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


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
    ).strip()


current = read_json(CURRENT)
triage = read_json(TRIAGE)
assembly = read_json(X3_ASSEMBLY)

require(git_blob(TRIAGE) == "de4d49cada15b231dfc31058aced4ec7a25928a2", "historical triage blob drift")
require(git_blob(X3_ASSEMBLY) == "b8426888b2053ab5be1f18ccd1532513a8fe6cca", "historical X.3 assembly blob drift")
require(triage.get("authorityId") == "HEART-ENTRY-CITATION-DISPOSITIONS-2026-08-04", "triage authority drift")
require(triage.get("counts", {}).get("entryCitationPassComplete") == 0, "historical triage completion count drift")
require(triage.get("counts", {}).get("finalBookEntries") == 18, "triage final-entry count drift")
require(triage.get("counts", {}).get("assembledReaderEntries") == 4, "triage assembled-reader count drift")
require(triage.get("counts", {}).get("entriesRequiringReaderAssembly") == 14, "triage reader-assembly count drift")

receipt_rows: list[dict[str, Any]] = []
for expected in EXPECTED_RECEIPTS:
    path = expected["path"]
    require(path.is_file(), f"completed receipt missing: {path.relative_to(ROOT)}")
    if not path.is_file():
        continue
    require(git_blob(path) == expected["blob"], f"completed receipt blob drift: {path.relative_to(ROOT)}")
    receipt = read_json(path)
    receipt_rows.append(receipt)
    require(receipt.get("authorityId") == expected["authority"], f"receipt authority drift: {expected['id']}")
    require(receipt.get("entry", {}).get("order") == expected["order"], f"receipt order drift: {expected['id']}")
    require(receipt.get("entry", {}).get("id") == expected["id"], f"receipt entry ID drift: {expected['id']}")
    require(receipt.get("disposition", {}).get("entryCitationPassComplete") is True, f"receipt pass incomplete: {expected['id']}")
    require(receipt.get("disposition", {}).get("remainingEntryBlockers") == [], f"receipt blockers remain: {expected['id']}")
    require(receipt.get("disposition", {}).get("newDirectQuotesApproved") == 0, f"receipt direct-quote drift: {expected['id']}")
    require(receipt.get("wholeBookBoundary", {}).get("entryCitationPassComplete") == expected["count"], f"receipt composed count drift: {expected['id']}")
    require(receipt.get("wholeBookBoundary", {}).get("wholeBookCitationPassComplete") is False, f"receipt falsely closes whole-book pass: {expected['id']}")
    require(receipt.get("wholeBookBoundary", {}).get("productReleaseComplete") is False, f"receipt falsely closes Product release: {expected['id']}")

entries = [row for row in triage.get("entries", []) if isinstance(row, dict)]
require(len(entries) == 18, "triage must retain eighteen entries")
entry_by_id = {row.get("id"): row for row in entries}
require(set(entry_by_id) == EXPECTED_COMPLETED | EXPECTED_OPEN, "triage entry ID universe drift")
require(all(entry_by_id[entry_id].get("readerAssembled") is True for entry_id in EXPECTED_COMPLETED), "a completed pass is not tied to an assembled reader")
require(all(entry_by_id[entry_id].get("disposition", {}).get("triageState") == "TRIAGED_OPEN" for entry_id in EXPECTED_COMPLETED), "historical completed-entry triage state rewritten")

open_ids = set(entry_by_id) - EXPECTED_COMPLETED
require(open_ids == EXPECTED_OPEN, "current open-entry set drift")
product_open = {entry_id for entry_id in open_ids if entry_by_id[entry_id].get("currentState") == "PRODUCT_SOURCE_ONLY"}
dossier_open = {entry_id for entry_id in open_ids if entry_by_id[entry_id].get("currentState") == "RESEARCH_DOSSIER_ONLY"}
require(product_open == EXPECTED_PRODUCT_OPEN, "open Product-source lane drift")
require(dossier_open == EXPECTED_DOSSIER_OPEN, "open dossier lane drift")
require(product_open | dossier_open == EXPECTED_OPEN, "open entry source lanes are not exhaustive")

require(assembly.get("authorityId") == "HEART-X3-READER-ASSEMBLY-2026-08-04", "X.3 assembly authority drift")
explicit_nine = set(assembly.get("remainingReaderAssemblies", []))
require(explicit_nine == EXPECTED_EXPLICIT_NINE, "historical explicit nine-reader backlog drift")
require(EXPECTED_ADDITIONAL_FIVE == EXPECTED_PRODUCT_OPEN - EXPECTED_EXPLICIT_NINE, "additional Product conversion derivation drift")
require(EXPECTED_EXPLICIT_NINE | EXPECTED_ADDITIONAL_FIVE == EXPECTED_OPEN, "effective fourteen-reader backlog is not exhaustive")
require(EXPECTED_EXPLICIT_NINE & EXPECTED_ADDITIONAL_FIVE == set(), "reader backlog lanes overlap")

require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-2026-08-04", "current authority drift")
require(current.get("status") == "FOUR_ENTRY_PASSES_COMPOSED_ALL_ASSEMBLED_READER_REVIEWS_COMPLETE_READER_ASSEMBLY_OPEN", "current status drift")
base = current.get("baseTriage", {})
require(base.get("gitBlob") == "de4d49cada15b231dfc31058aced4ec7a25928a2", "current base-triage blob drift")
require(base.get("historicalEntryCitationPassComplete") == 0, "current historical count drift")
current_receipts = current.get("completedPassReceipts", [])
require(len(current_receipts) == 4, "current registry must contain four completed receipts")
require([row.get("id") for row in current_receipts] == [row["id"] for row in EXPECTED_RECEIPTS], "current receipt order drift")
for current_row, expected in zip(current_receipts, EXPECTED_RECEIPTS, strict=True):
    require(current_row.get("gitBlob") == expected["blob"], f"current receipt blob drift: {expected['id']}")
    require(current_row.get("authorityId") == expected["authority"], f"current receipt authority drift: {expected['id']}")
    require(current_row.get("composedCountAfterReceipt") == expected["count"], f"current receipt count drift: {expected['id']}")
counts = current.get("currentCounts", {})
require(counts == {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 4,
    "entryCitationPassOpen": 14,
    "assembledReaderEntries": 4,
    "assembledReaderCitationReviewsComplete": 4,
    "missingStandaloneFinalReaders": 14,
    "newDirectQuotesApproved": 0,
}, "current count block drift")
require(set(current.get("completedEntryIds", [])) == EXPECTED_COMPLETED, "current completed-entry set drift")
require(set(current.get("openEntryIds", [])) == EXPECTED_OPEN, "current open-entry set drift")
backlog = current.get("readerAssemblyBacklog", {})
require(set(backlog.get("historicalX3AssemblyReceipt", {}).get("explicitRemainingReaderAssemblies", [])) == EXPECTED_EXPLICIT_NINE, "current explicit-nine backlog drift")
require(set(backlog.get("additionalProductSourceToFinalReaderConversionsRequiredByTriage", [])) == EXPECTED_ADDITIONAL_FIVE, "current additional-five backlog drift")
require(backlog.get("effectiveMissingStandaloneFinalReaders") == 14, "current effective reader backlog count drift")
lanes = current.get("openEntriesBySourceLane", {})
require(set(lanes.get("productSourceOnly", [])) == EXPECTED_PRODUCT_OPEN, "current Product lane drift")
require(set(lanes.get("researchDossierOnly", [])) == EXPECTED_DOSSIER_OPEN, "current dossier lane drift")
boundary = current.get("publicationBoundary", {})
require(boundary.get("allCurrentlyAssembledReadersReviewed") is True, "assembled-reader reviews not closed")
require(boundary.get("wholeBookReaderAssemblyComplete") is False, "whole-book reader assembly falsely closed")
require(boundary.get("wholeBookCitationPassComplete") is False, "whole-book citation pass falsely closed")
require(boundary.get("productReleaseComplete") is False, "Product release falsely closed")
require(boundary.get("newDirectQuotesApproved") == 0, "current direct-quote boundary drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-ENTRY-CITATION-PASS-CURRENT-2026-08-04",
    "ENTRY CITATION PASSES COMPLETE = 4 / 18",
    "ENTRY CITATION PASSES OPEN = 14 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 4 / 4",
    "MISSING STANDALONE FINAL READERS = 14",
    "HISTORICAL EXPLICIT ASSEMBLY BACKLOG = 9",
    "ADDITIONAL PRODUCT-TO-READER CONVERSIONS = 5",
    "WHOLE-BOOK CITATION PASS = OPEN",
    "WHOLE-BOOK READER ASSEMBLY = INCOMPLETE",
    "NEW DIRECT QUOTES APPROVED = 0",
):
    require(marker in human, f"current human authority marker missing: {marker}")
for forbidden in (
    "ENTRY CITATION PASSES COMPLETE = 18 / 18",
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "WHOLE-BOOK READER ASSEMBLY = COMPLETE",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"current human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart entry citation pass current composition: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "Heart entry citation pass current composition: PASS — "
    "4/18 completed, 14/18 open, assembled-reader reviews 4/4, "
    "reader backlog 9 explicit + 5 Product conversions, 0 new direct quotes"
)
