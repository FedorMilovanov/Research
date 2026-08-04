#!/usr/bin/env python3
"""Validate the exact completed I.2 entry citation pass."""
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
REVIEW = ROOT / "data/heart-i2-citation-review-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/79_READER_CHAPTER_I2_HEART_IN_EDEN_2026-08-02.md"
DOSSIER = ROOT / "СЕРИЯ СЕРДЦЕ/75_P0_EDEN_HEART_CREATED_AND_FALLEN_2026-08-02.md"
P0 = ROOT / "data/heart-p0-architecture-dossiers-2026-08-02.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/92_I2_CITATION_REVIEW_2026-08-04.md"

BLOBS = {
    READER: "204545a59477d92839245800f56791466bf45349",
    DOSSIER: "15f5e7fb3b152cf7a6a1470c1cea86e720be933b",
    P0: "71c26fed5de96cead1e2f8dcdedbfefc05f3e628",
}
READER_QUOTES = [
    "сердце — это разум, чувства и воля",
    "сердце в Эдеме",
    "Выбери смерть",
    "Бог скрывает от тебя настоящее добро. Ты должен сам определить, что тебе нужно",
    "не оправдывайся",
    "Как обнаружить внутри себя неповреждённого человека?",
    "Как Дух обновляет меня по образу Христа?",
]
DOSSIER_QUOTES = [
    "сердце в Эдеме",
    "весьма хорошо",
    "настоящем духовном я",
    "станьте злыми",
    "неиспорченного ядра внутри",
    "В Эдеме сердце означало разум, эмоции и волю",
    "Ева согрешила, потому что была эмоциональнее Адама",
    "После падения образ Божий исчез",
    "Тело стало плохим после грехопадения",
    "Все люди одинаково злы во всех отношениях",
    "Грех передаётся только дурным примером",
    "Спасение возвращает нас к состоянию Адама",
    "Сердце в Эдеме",
]
BLOCK_STARTS = [
    "До падения внутренний человек был создан",
    "Бытие 1–2 прямо определяет сердце",
    "Грех не создал способность желать",
    "Сердце исцеляется не возвращением",
]
CLAIMS = {f"EDEN-{number:02}" for number in range(1, 9)}
SOURCES = {"HP0-S01", "HP0-S02", "HP0-S03", "HP0-S04", "HP0-S05", "HP0-S06", "HP0-S10", "HP0-S11"}
errors: list[str] = []


def require(value: bool, message: str) -> None:
    if not value:
        errors.append(message)


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    return data if isinstance(data, dict) else {}


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True).strip()


def load_builder() -> Any:
    spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("inventory builder import unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def quotes(text: str) -> list[str]:
    return re.findall(r"«([^»\n]{8,})»", text)


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
product_root = parser.parse_args().product_root.resolve()
require(product_root.is_dir(), "exact Product checkout missing")

for path, expected in BLOBS.items():
    require(path.is_file(), f"immutable source missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(path) == expected, f"immutable blob drift: {path.relative_to(ROOT)}")

module = load_builder()
reader_scan = module.scan_owner(module.r(str(READER.relative_to(ROOT)), "reader"), product_root)
dossier_scan = module.scan_owner(module.r(str(DOSSIER.relative_to(ROOT)), "dossier"), product_root)
reader_text = READER.read_text(encoding="utf-8")
dossier_text = DOSSIER.read_text(encoding="utf-8")

reader_refs = reader_scan["scriptureReferences"]
dossier_refs = dossier_scan["scriptureReferences"]
require(len(reader_refs) == 2, "reader reference count must be 2")
require(len(dossier_refs) == 21, "dossier reference count must be 21")
require(len(set(reader_refs) | set(dossier_refs)) == 23, "aggregate reference count must be 23")
require(reader_scan["externalLinks"] == dossier_scan["externalLinks"] == [], "external links must remain absent")
require(reader_scan["footnoteDefinitions"] == dossier_scan["footnoteDefinitions"] == 0, "footnotes must remain absent")
require(reader_scan["markdownBlockquotes"] == 0, "reader blockquote count drift")
require(reader_scan["inlineQuotationSegments"] == 7, "reader inline quote count drift")
require(dossier_scan["markdownBlockquotes"] == 4, "dossier blockquote count drift")
require(dossier_scan["inlineQuotationSegments"] == 13, "dossier inline quote count drift")
require(quotes(reader_text) == READER_QUOTES, "reader quotation surfaces drift")
require(quotes(dossier_text) == DOSSIER_QUOTES, "dossier quotation surfaces drift")
blocks = [line.lstrip()[1:].strip() for line in dossier_text.splitlines() if re.match(r"^\s*>\s?\S", line)]
require(len(blocks) == 4, "dossier authorial blockquote set drift")
for start in BLOCK_STARTS:
    require(any(item.startswith(start) for item in blocks), f"dossier blockquote missing: {start}")
require("**Новые прямые цитаты:** `0`" in reader_text, "reader direct-quote boundary drift")
require("**Прямые цитаты:** `0 approved`" in dossier_text, "dossier direct-quote boundary drift")

p0 = read_json(P0)
claim_rows = [row for row in p0.get("claims", []) if row.get("dossierId") == "HEART-P0-EDEN"]
source_rows = {row.get("id"): row for row in p0.get("sources", []) if isinstance(row, dict)}
require(p0.get("authorityId") == "HEART-P0-ARCHITECTURE-CLOSURE-2026-08-02", "P0 authority drift")
require(p0.get("directQuotesApproved") is False, "P0 direct-quote boundary drift")
require(p0.get("publicationEligible") is True, "P0 publication eligibility drift")
require({row.get("id") for row in claim_rows} == CLAIMS, "EDEN claim set drift")
require(all(row.get("status") in {"CLOSED", "BOUNDARY_CLOSED"} for row in claim_rows), "EDEN claim status drift")
require(all(row.get("support") and row.get("locators") and row.get("publicationBoundary") for row in claim_rows), "EDEN claim governance incomplete")
used_sources = {source_id for row in claim_rows for source_id in row.get("support", [])}
require(used_sources == SOURCES, "EDEN source set drift")
require(all(source_rows.get(source_id, {}).get("url") for source_id in SOURCES), "EDEN source URL missing")
require(all(source_rows.get(source_id, {}).get("locators") for source_id in SOURCES), "EDEN source locator missing")

triage = read_json(TRIAGE)
i2_rows = [row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-I2"]
require(len(i2_rows) == 1, "historical I.2 triage row missing")
if i2_rows:
    row = i2_rows[0]
    require(row.get("inventoryEntrySha256") == "fbe1a99962021e156484f25535d925ac70aeec65467d502bd14334cc4e6a8199", "I.2 inventory-entry SHA drift")
    require(row.get("detected") == {"ownerSurfaces": 2, "sourceHeadings": 1, "scriptureReferences": 23, "externalLinks": 0, "internalArticleLinks": 0, "quotationSurfaces": 24}, "I.2 aggregate inventory counts drift")
    require(row.get("disposition", {}).get("triageState") == "TRIAGED_OPEN", "historical triage state drift")

review = read_json(REVIEW)
require(review.get("authorityId") == "HEART-I2-CITATION-REVIEW-2026-08-04", "review authority drift")
require(review.get("status") == "I2_ENTRY_CITATION_PASS_COMPLETE_WHOLE_BOOK_OPEN", "review status drift")
require(review.get("scriptureReview", {}).get("readerDetectedReferences") == 2, "receipt reader count drift")
require(review.get("scriptureReview", {}).get("dossierDetectedReferences") == 21, "receipt dossier count drift")
require(review.get("scriptureReview", {}).get("aggregateUniqueReferences") == 23, "receipt aggregate count drift")
require(review.get("scriptureReview", {}).get("translationVersionIdentifierRequired") is False, "translation-version boundary drift")
require(review.get("scriptureReview", {}).get("reviewComplete") is True, "Scripture review incomplete")
require(review.get("quotationReview", {}).get("aggregateQuotationSurfaces") == 24, "receipt quotation total drift")
require(review.get("quotationReview", {}).get("reviewComplete") is True, "quotation review incomplete")
require(review.get("claimGovernance", {}).get("claimsReviewed") == 8, "claim review count drift")
require(review.get("claimGovernance", {}).get("requiredSourcesWithUrl") == 8, "source URL coverage drift")
require(review.get("claimGovernance", {}).get("requiredSourcesWithLocator") == 8, "source locator coverage drift")
require(review.get("disposition", {}).get("remainingEntryBlockers") == [], "I.2 blockers remain")
require(review.get("disposition", {}).get("readerManuscriptChanged") is False, "reader mutation falsely claimed")
require(review.get("disposition", {}).get("evidenceDossierChanged") is False, "dossier mutation falsely claimed")
require(review.get("disposition", {}).get("newHistoricalClaims") == 0, "new historical claim drift")
require(review.get("disposition", {}).get("newDirectQuotesApproved") == 0, "new direct quote drift")
require(review.get("disposition", {}).get("entryCitationPassComplete") is True, "I.2 pass not complete")
require(review.get("wholeBookBoundary", {}).get("entryCitationPassComplete") == "1 / 18", "whole-book completion count drift")
require(review.get("wholeBookBoundary", {}).get("entryCitationPassOpen") == "17 / 18", "whole-book open count drift")
require(review.get("wholeBookBoundary", {}).get("wholeBookCitationPassComplete") is False, "whole-book pass falsely closed")
require(review.get("wholeBookBoundary", {}).get("productReleaseComplete") is False, "Product release falsely closed")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-I2-CITATION-REVIEW-2026-08-04",
    "I.2 ENTRY CITATION PASS = COMPLETE",
    "WHOLE-BOOK ENTRY CITATION PASSES = 1 / 18",
    "SCRIPTURE REFERENCES GOVERNED = 23 / 23",
    "QUOTATION SURFACES CLASSIFIED = 24 / 24",
    "READER DIRECT QUOTES = 0",
    "DOSSIER DIRECT QUOTES APPROVED = 0",
    "READER MANUSCRIPT CHANGES = 0",
    "WHOLE-BOOK CITATION PASS = OPEN",
):
    require(marker in human, f"human authority marker missing: {marker}")
for forbidden in (
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "NEW DIRECT QUOTES APPROVED = 1",
    "READER MANUSCRIPT CHANGES = 1",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart I.2 entry citation pass: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart I.2 entry citation pass: PASS — 2 reader + 21 dossier refs = 23 unique; 24 quotation surfaces; 0 direct quotes; whole-book 1/18")
