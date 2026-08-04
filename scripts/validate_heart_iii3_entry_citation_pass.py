#!/usr/bin/env python3
"""Validate the exact completed III.3 entry citation pass."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
REVIEW = ROOT / "data/heart-iii3-citation-review-2026-08-04.json"
I2_REVIEW = ROOT / "data/heart-i2-citation-review-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/80_READER_CHAPTER_III3_BROKEN_HEART_REPENTANCE_2026-08-02.md"
DOSSIER = ROOT / "СЕРИЯ СЕРДЦЕ/76_P0_BROKEN_HEART_REPENTANCE_2026-08-02.md"
P0 = ROOT / "data/heart-p0-architecture-dossiers-2026-08-02.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/93_III3_CITATION_REVIEW_2026-08-04.md"

BLOBS = {
    READER: "f7a8fe5032ceeb26d9acc4fd6f248ba5f92de29d",
    DOSSIER: "d54e86796a38f34a656829011ed17948cf6edb8f",
    P0: "71c26fed5de96cead1e2f8dcdedbfefc05f3e628",
}
EXPECTED_CLAIM_IDS = {f"REP-{index:02}" for index in range(1, 9)}
EXPECTED_SOURCE_IDS = {
    "HP0-S01",
    "HP0-S03",
    "HP0-S04",
    "HP0-S07",
    "HP0-S12",
    "HP0-S14",
    "HP0-S15",
}
EXPECTED_TRIAGE = {
    "ownerSurfaces": 2,
    "sourceHeadings": 1,
    "scriptureReferences": 20,
    "externalLinks": 0,
    "internalArticleLinks": 0,
    "quotationSurfaces": 42,
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


def import_builder() -> Any:
    spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
    require(spec is not None and spec.loader is not None, "inventory builder import unavailable")
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def declares_zero_direct_quotes(text: str) -> bool:
    compact = re.sub(r"\s+", " ", text)
    patterns = (
        r"(?i)прям\w*\s+цитат\w*[^\n]{0,120}(?:`?0`?|zero)",
        r"(?i)(?:new\s+)?direct\s+quotes?[^\n]{0,120}(?:`?0`?|zero)",
    )
    return any(re.search(pattern, compact) for pattern in patterns)


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
product_root = parser.parse_args().product_root.resolve()
require(product_root.is_dir(), "exact Product checkout missing")

for path, expected_blob in BLOBS.items():
    require(path.is_file(), f"immutable source missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(git_blob(path) == expected_blob, f"immutable blob drift: {path.relative_to(ROOT)}")

reader_text = READER.read_text(encoding="utf-8") if READER.is_file() else ""
dossier_text = DOSSIER.read_text(encoding="utf-8") if DOSSIER.is_file() else ""
require("**Claim scope:** `REP-01…REP-08`" in reader_text, "III.3 reader claim-range marker drift")
require("**Claim IDs:** `REP-01…REP-08`" in dossier_text, "III.3 dossier claim-range marker drift")
require(declares_zero_direct_quotes(reader_text), "III.3 reader zero-direct-quote declaration missing")
require(declares_zero_direct_quotes(dossier_text), "III.3 dossier zero-direct-quote declaration missing")

builder = import_builder()
if builder is not None:
    reader_scan = builder.scan_owner(
        builder.r(str(READER.relative_to(ROOT)), "assembled reader"),
        product_root,
    )
    dossier_scan = builder.scan_owner(
        builder.r(str(DOSSIER.relative_to(ROOT)), "P0 evidence dossier"),
        product_root,
    )
else:
    reader_scan = {}
    dossier_scan = {}

reader_refs = set(reader_scan.get("scriptureReferences", []))
dossier_refs = set(dossier_scan.get("scriptureReferences", []))
require(len(reader_refs) == 1, "III.3 reader Scripture-reference count drift")
require(len(dossier_refs) == 20, "III.3 dossier Scripture-reference count drift")
require(len(reader_refs | dossier_refs) == 20, "III.3 aggregate Scripture-reference count drift")
require(reader_scan.get("externalLinks") == [], "III.3 reader external links must remain absent")
require(dossier_scan.get("externalLinks") == [], "III.3 dossier external links must remain absent")
require(reader_scan.get("internalArticleLinks") == [], "III.3 reader internal links must remain absent")
require(dossier_scan.get("internalArticleLinks") == [], "III.3 dossier internal links must remain absent")
require(reader_scan.get("footnoteDefinitions") == 0, "III.3 reader footnotes must remain absent")
require(dossier_scan.get("footnoteDefinitions") == 0, "III.3 dossier footnotes must remain absent")
require(reader_scan.get("htmlBlockquotes") == 0, "III.3 reader HTML blockquotes must remain absent")
require(dossier_scan.get("htmlBlockquotes") == 0, "III.3 dossier HTML blockquotes must remain absent")
require(reader_scan.get("inlineQuotationSegments") == 16, "III.3 reader inline-quotation count drift")
require(reader_scan.get("markdownBlockquotes") == 2, "III.3 reader blockquote count drift")
require(dossier_scan.get("inlineQuotationSegments") == 19, "III.3 dossier inline-quotation count drift")
require(dossier_scan.get("markdownBlockquotes") == 5, "III.3 dossier blockquote count drift")
require(
    sum(
        int(scan.get("markdownBlockquotes", 0))
        + int(scan.get("inlineQuotationSegments", 0))
        for scan in (reader_scan, dossier_scan)
    )
    == 42,
    "III.3 aggregate quotation-surface count drift",
)
require(len(reader_scan.get("sourceHeadings", [])) == 0, "III.3 reader source-heading drift")
require(len(dossier_scan.get("sourceHeadings", [])) == 1, "III.3 dossier source-heading drift")

p0 = read_json(P0)
require(p0.get("authorityId") == "HEART-P0-ARCHITECTURE-CLOSURE-2026-08-02", "P0 authority drift")
require(p0.get("directQuotesApproved") is False, "P0 direct-quote boundary drift")
require(p0.get("publicationEligible") is True, "P0 publication eligibility drift")
claims = [
    row
    for row in p0.get("claims", [])
    if isinstance(row, dict) and row.get("id") in EXPECTED_CLAIM_IDS
]
require({row.get("id") for row in claims} == EXPECTED_CLAIM_IDS, "III.3 REP claim set drift")
require(
    all(row.get("dossierId") == "HEART-P0-REPENTANCE" for row in claims),
    "III.3 REP dossier binding drift",
)
require(
    all(row.get("status") in {"CLOSED", "BOUNDARY_CLOSED"} for row in claims),
    "III.3 claim closure drift",
)
require(all(row.get("support") for row in claims), "III.3 claim support missing")
require(all(row.get("locators") for row in claims), "III.3 claim locators missing")
require(
    all(row.get("publicationBoundary") for row in claims),
    "III.3 claim publication boundary missing",
)
source_rows = {
    row.get("id"): row for row in p0.get("sources", []) if isinstance(row, dict)
}
used_sources = {source_id for row in claims for source_id in row.get("support", [])}
require(used_sources == EXPECTED_SOURCE_IDS, "III.3 governing source set drift")
require(all(source_id in source_rows for source_id in EXPECTED_SOURCE_IDS), "III.3 source record missing")
require(all(source_rows[source_id].get("url") for source_id in EXPECTED_SOURCE_IDS), "III.3 source URL missing")
require(
    all(source_rows[source_id].get("locators") for source_id in EXPECTED_SOURCE_IDS),
    "III.3 source locator missing",
)

triage = read_json(TRIAGE)
triage_rows = [
    row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-III3"
]
require(len(triage_rows) == 1, "historical III.3 triage row missing")
if triage_rows:
    row = triage_rows[0]
    require(
        row.get("inventoryEntrySha256")
        == "91ccbce5aa0bf8a22c75af4ab984b09dd8928623666eaef30ded88cbb1fe4c73",
        "III.3 inventory-entry SHA drift",
    )
    require(row.get("detected") == EXPECTED_TRIAGE, "III.3 aggregate inventory counts drift")
    require(
        row.get("disposition", {}).get("triageState") == "TRIAGED_OPEN",
        "historical III.3 triage state drift",
    )

review = read_json(REVIEW)
require(review.get("authorityId") == "HEART-III3-CITATION-REVIEW-2026-08-04", "III.3 review authority drift")
require(review.get("status") == "III3_ENTRY_CITATION_PASS_COMPLETE_WHOLE_BOOK_OPEN", "III.3 review status drift")
immutable = review.get("immutableSources", {})
require(immutable.get("reader", {}).get("gitBlob") == BLOBS[READER], "III.3 receipt reader blob drift")
require(immutable.get("evidenceDossier", {}).get("gitBlob") == BLOBS[DOSSIER], "III.3 receipt dossier blob drift")
require(immutable.get("evidenceRegistry", {}).get("gitBlob") == BLOBS[P0], "III.3 receipt P0 blob drift")
scripture = review.get("scriptureReview", {})
require(scripture.get("readerDetectedReferences") == 1, "III.3 receipt reader Scripture count drift")
require(scripture.get("dossierDetectedReferences") == 20, "III.3 receipt dossier Scripture count drift")
require(scripture.get("aggregateUniqueReferences") == 20, "III.3 receipt Scripture total drift")
require(scripture.get("translationVersionIdentifierRequired") is False, "III.3 translation-version boundary drift")
require(scripture.get("reviewComplete") is True, "III.3 Scripture review incomplete")
quotation = review.get("quotationReview", {})
require(quotation.get("aggregateQuotationSurfaces") == 42, "III.3 receipt quotation total drift")
require(quotation.get("reader", {}).get("inlineQuotationSegments") == 16, "III.3 receipt reader inline drift")
require(quotation.get("reader", {}).get("markdownBlockquotes") == 2, "III.3 receipt reader blockquote drift")
require(quotation.get("reader", {}).get("historicalOrSourceDirectQuotes") == 0, "III.3 reader direct-quote drift")
require(quotation.get("evidenceDossier", {}).get("inlineQuotationSegments") == 19, "III.3 receipt dossier inline drift")
require(quotation.get("evidenceDossier", {}).get("markdownBlockquotes") == 5, "III.3 receipt dossier blockquote drift")
require(
    quotation.get("evidenceDossier", {}).get("historicalOrSourceDirectQuotesApproved") == 0,
    "III.3 dossier direct-quote drift",
)
require(quotation.get("reviewComplete") is True, "III.3 quotation review incomplete")
governance = review.get("claimGovernance", {})
require(governance.get("governingDossierId") == "HEART-P0-REPENTANCE", "III.3 receipt dossier ID drift")
require(set(governance.get("claimIds", [])) == EXPECTED_CLAIM_IDS, "III.3 receipt claim set drift")
require(set(governance.get("requiredSourceIds", [])) == EXPECTED_SOURCE_IDS, "III.3 receipt source set drift")
require(governance.get("claimsReviewed") == 8, "III.3 receipt claim count drift")
require(governance.get("requiredSourcesPresent") == 7, "III.3 receipt source count drift")
require(governance.get("reviewComplete") is True, "III.3 claim governance incomplete")
require(review.get("disposition", {}).get("remainingEntryBlockers") == [], "III.3 blockers remain")
require(review.get("disposition", {}).get("readerManuscriptChanged") is False, "III.3 reader mutation falsely claimed")
require(review.get("disposition", {}).get("evidenceDossierChanged") is False, "III.3 dossier mutation falsely claimed")
require(review.get("disposition", {}).get("newHistoricalClaims") == 0, "III.3 new historical claim drift")
require(review.get("disposition", {}).get("newDirectQuotesApproved") == 0, "III.3 new direct quote drift")
require(review.get("disposition", {}).get("entryCitationPassComplete") is True, "III.3 entry pass not complete")
require(review.get("wholeBookBoundary", {}).get("entryCitationPassComplete") == "2 / 18", "whole-book completion count drift")
require(review.get("wholeBookBoundary", {}).get("entryCitationPassOpen") == "16 / 18", "whole-book open count drift")
require(review.get("wholeBookBoundary", {}).get("assembledReaderCitationReviewsComplete") == "2 / 4", "assembled-reader review count drift")
require(review.get("wholeBookBoundary", {}).get("wholeBookCitationPassComplete") is False, "whole-book citation pass falsely closed")
require(review.get("wholeBookBoundary", {}).get("productReleaseComplete") is False, "Product release falsely closed")

i2_review = read_json(I2_REVIEW)
require(i2_review.get("disposition", {}).get("entryCitationPassComplete") is True, "I.2 preceding pass missing")
require(i2_review.get("wholeBookBoundary", {}).get("entryCitationPassComplete") == "1 / 18", "I.2 historical count drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-III3-CITATION-REVIEW-2026-08-04",
    "III.3 ENTRY CITATION PASS = COMPLETE",
    "WHOLE-BOOK ENTRY CITATION PASSES = 2 / 18",
    "SCRIPTURE REFERENCES GOVERNED = 20 / 20",
    "QUOTATION SURFACES CLASSIFIED = 42 / 42",
    "READER DIRECT QUOTES = 0",
    "DOSSIER DIRECT QUOTES APPROVED = 0",
    "READER MANUSCRIPT CHANGES = 0",
    "WHOLE-BOOK CITATION PASS = OPEN",
    BLOBS[READER],
    BLOBS[DOSSIER],
):
    require(marker in human, f"III.3 human authority marker missing: {marker}")
for forbidden in (
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "NEW DIRECT QUOTES APPROVED = 1",
    "READER MANUSCRIPT CHANGES = 1",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"III.3 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart III.3 entry citation pass: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "Heart III.3 entry citation pass: PASS — "
    "1 reader + 20 dossier refs = 20 unique; "
    "42 quotation surfaces; 8 governed claims; 7 source records; "
    "0 direct quotes; whole-book 2/18"
)
