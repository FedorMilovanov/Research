#!/usr/bin/env python3
"""Validate the completed I.2 reader-facing citation review without rewriting sources."""
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
REVIEW = ROOT / "data/heart-i2-citation-review-2026-08-04.json"
DISPOSITIONS = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/79_READER_CHAPTER_I2_HEART_IN_EDEN_2026-08-02.md"
DOSSIER = ROOT / "СЕРИЯ СЕРДЦЕ/75_P0_EDEN_HEART_CREATED_AND_FALLEN_2026-08-02.md"
P0_REGISTRY = ROOT / "data/heart-p0-architecture-dossiers-2026-08-02.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/92_I2_CITATION_REVIEW_2026-08-04.md"
CURRENT = ROOT / "СЕРИЯ СЕРДЦЕ/90_CITATION_INVENTORY_CURRENT_OVERLAY_2026-08-04.md"

EXPECTED_BLOBS = {
    READER: "204545a59477d92839245800f56791466bf45349",
    DOSSIER: "15f5e7fb3b152cf7a6a1470c1cea86e720be933b",
    P0_REGISTRY: "71c26fed5de96cead1e2f8dcdedbfefc05f3e628",
}
EXPECTED_READER_QUOTES = [
    "сердце — это разум, чувства и воля",
    "сердце в Эдеме",
    "Выбери смерть",
    "Бог скрывает от тебя настоящее добро. Ты должен сам определить, что тебе нужно",
    "не оправдывайся",
    "Как обнаружить внутри себя неповреждённого человека?",
    "Как Дух обновляет меня по образу Христа?",
]
EXPECTED_DOSSIER_QUOTES = [
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
EXPECTED_BLOCKQUOTE_STARTS = [
    "До падения внутренний человек был создан",
    "Бытие 1–2 прямо определяет сердце",
    "Грех не создал способность желать",
    "Сердце исцеляется не возвращением",
]
EXPECTED_SOURCE_IDS = {"HP0-S01", "HP0-S02", "HP0-S03", "HP0-S04", "HP0-S05", "HP0-S06", "HP0-S10", "HP0-S11"}
EXPECTED_CLAIM_IDS = {f"EDEN-{index:02}" for index in range(1, 9)}

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
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
    spec = importlib.util.spec_from_file_location("heart_citation_builder", BUILDER)
    require(spec is not None and spec.loader is not None, "inventory builder import unavailable")
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def quote_segments(text: str) -> list[str]:
    return re.findall(r"«([^»\n]{8,})»", text)


def markdown_blockquotes(text: str) -> list[str]:
    return [line.lstrip()[1:].strip() for line in text.splitlines() if re.match(r"^\s*>\s?\S", line)]


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
product_root = parser.parse_args().product_root.resolve()
require(product_root.is_dir(), "exact Product checkout missing")

for path, expected in EXPECTED_BLOBS.items():
    require(path.is_file(), f"immutable source missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(git_blob(path) == expected, f"immutable source blob drift: {path.relative_to(ROOT)}")

review = read_json(REVIEW)
dispositions = read_json(DISPOSITIONS)
p0 = read_json(P0_REGISTRY)
reader_text = READER.read_text(encoding="utf-8") if READER.is_file() else ""
dossier_text = DOSSIER.read_text(encoding="utf-8") if DOSSIER.is_file() else ""

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

require(len(reader_scan.get("scriptureReferences", [])) == 2, "reader Scripture-reference count drift")
require(len(dossier_scan.get("scriptureReferences", [])) == 23, "dossier Scripture-reference count drift")
require(
    len(set(reader_scan.get("scriptureReferences", [])) | set(dossier_scan.get("scriptureReferences", []))) == 23,
    "aggregate unique Scripture-reference count drift",
)
require(reader_scan.get("externalLinks") == [], "reader must have no external links")
require(dossier_scan.get("externalLinks") == [], "dossier must have no external links")
require(reader_scan.get("footnoteDefinitions") == dossier_scan.get("footnoteDefinitions") == 0, "unexpected footnotes")
require(reader_scan.get("markdownBlockquotes") == 0, "reader must have no Markdown blockquotes")
require(reader_scan.get("inlineQuotationSegments") == 7, "reader inline quotation count drift")
require(dossier_scan.get("markdownBlockquotes") == 4, "dossier blockquote count drift")
require(dossier_scan.get("inlineQuotationSegments") == 13, "dossier inline quotation count drift")
require(
    reader_scan.get("inlineQuotationSegments", 0)
    + dossier_scan.get("inlineQuotationSegments", 0)
    + reader_scan.get("markdownBlockquotes", 0)
    + dossier_scan.get("markdownBlockquotes", 0)
    == 24,
    "aggregate quotation-surface count drift",
)
require(quote_segments(reader_text) == EXPECTED_READER_QUOTES, "reader quotation classification surface drift")
require(quote_segments(dossier_text) == EXPECTED_DOSSIER_QUOTES, "dossier quotation classification surface drift")
blocks = markdown_blockquotes(dossier_text)
require(len(blocks) == 4, "dossier must retain four authorial blockquotes")
for expected_start in EXPECTED_BLOCKQUOTE_STARTS:
    require(any(block.startswith(expected_start) for block in blocks), f"dossier authorial blockquote missing: {expected_start}")

require("**Новые прямые цитаты:** `0`" in reader_text, "reader direct-quote boundary drift")
require("**Прямые цитаты:** `0 approved`" in dossier_text, "dossier direct-quote boundary drift")
require("http://" not in reader_text and "https://" not in reader_text, "reader URL surface introduced")
require("http://" not in dossier_text and "https://" not in dossier_text, "dossier URL surface introduced")

claims = [row for row in p0.get("claims", []) if row.get("dossierId") == "HEART-P0-EDEN"]
sources = {row.get("id"): row for row in p0.get("sources", []) if isinstance(row, dict)}
require(p0.get("authorityId") == "HEART-P0-ARCHITECTURE-CLOSURE-2026-08-02", "P0 authority drift")
require(p0.get("directQuotesApproved") is False, "P0 direct-quote boundary drift")
require(p0.get("publicationEligible") is True, "P0 publication eligibility drift")
require({row.get("id") for row in claims} == EXPECTED_CLAIM_IDS, "EDEN claim set drift")
require(all(row.get("status") in {"CLOSED", "BOUNDARY_CLOSED"} for row in claims), "EDEN claim closure drift")
require(all(row.get("support") for row in claims), "EDEN claim support missing")
require(all(row.get("locators") for row in claims), "EDEN claim locators missing")
require(all(row.get("publicationBoundary") for row in claims), "EDEN publication boundary missing")
used_sources = {source_id for row in claims for source_id in row.get("support", [])}
require(used_sources == EXPECTED_SOURCE_IDS, "EDEN governing source set drift")
require(all(source_id in sources for source_id in EXPECTED_SOURCE_IDS), "EDEN source record missing")
require(all(sources[source_id].get("url") for source_id in EXPECTED_SOURCE_IDS), "EDEN source URL missing")
require(all(sources[source_id].get("locators") for source_id in EXPECTED_SOURCE_IDS), "EDEN source locator missing")
require(all("quoted" in sources[source_id].get("use", "").lower() or sources[source_id].get("use") for source_id in EXPECTED_SOURCE_IDS), "EDEN source-use field missing")

triage_rows = [row for row in dispositions.get("entries", []) if row.get("id") == "HEART-BOOK-I2"]
require(len(triage_rows) == 1, "I.2 triage row missing")
if triage_rows:
    triage = triage_rows[0]
    require(triage.get("inventoryEntrySha256") == "fbe1a99962021e156484f25535d925ac70aeec65467d502bd14334cc4e6a8199", "I.2 inventory-row SHA drift")
    require(triage.get("detected") == {
        "ownerSurfaces": 2,
        "sourceHeadings": 1,
        "scriptureReferences": 23,
        "externalLinks": 0,
        "internalArticleLinks": 0,
        "quotationSurfaces": 24,
    }, "I.2 triage detected counts drift")
    require(triage.get("disposition", {}).get("triageState") == "TRIAGED_OPEN", "historical triage snapshot drift")

require(review.get("authorityId") == "HEART-I2-CITATION-REVIEW-2026-08-04", "I.2 review authority drift")
require(review.get("status") == "I2_ENTRY_CITATION_PASS_COMPLETE_WHOLE_BOOK_OPEN", "I.2 review status drift")
require(review.get("entry", {}).get("stateAfter") == "ENTRY_CITATION_PASS_COMPLETE", "I.2 state-after drift")
require(review.get("scriptureReview", {}).get("reviewComplete") is True, "I.2 Scripture review not complete")
require(review.get("scriptureReview", {}).get("translationVersionIdentifierRequired") is False, "version identifier boundary drift")
require(review.get("quotationReview", {}).get("reviewComplete") is True, "I.2 quotation review not complete")
require(review.get("quotationReview", {}).get("aggregateQuotationSurfaces") == 24, "review quotation total drift")
require(review.get("claimGovernance", {}).get("claimsReviewed") == 8, "claim review count drift")
require(review.get("claimGovernance", {}).get("requiredSourcesPresent") == 8, "source review count drift")
require(review.get("disposition", {}).get("remainingEntryBlockers") == [], "I.2 blockers remain")
require(review.get("disposition", {}).get("readerManuscriptChanged") is False, "reader mutation falsely claimed")
require(review.get("disposition", {}).get("evidenceDossierChanged") is False, "dossier mutation falsely claimed")
require(review.get("disposition", {}).get("newHistoricalClaims") == 0, "new historical claim drift")
require(review.get("disposition", {}).get("newDirectQuotesApproved") == 0, "new direct quote drift")
require(review.get("disposition", {}).get("entryCitationPassComplete") is True, "I.2 entry pass not complete")
require(review.get("wholeBookBoundary", {}).get("entryCitationPassComplete") == "1 / 18", "whole-book completed count drift")
require(review.get("wholeBookBoundary", {}).get("entryCitationPassOpen") == "17 / 18", "whole-book open count drift")
require(review.get("wholeBookBoundary", {}).get("wholeBookCitationPassComplete") is False, "whole-book citation pass falsely closed")
require(review.get("wholeBookBoundary", {}).get("productReleaseComplete") is False, "Product release falsely closed")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
current = CURRENT.read_text(encoding="utf-8") if CURRENT.is_file() else ""
for marker in (
    "HEART-I2-CITATION-REVIEW-2026-08-04",
    "I.2 ENTRY CITATION PASS = COMPLETE",
    "WHOLE-BOOK ENTRY CITATION PASSES = 1 / 18",
    "READER DIRECT QUOTES = 0",
    "DOSSIER DIRECT QUOTES APPROVED = 0",
    "QUOTATION SURFACES CLASSIFIED = 24 / 24",
    "SCRIPTURE REFERENCES GOVERNED = 23 / 23",
    "READER MANUSCRIPT CHANGES = 0",
    "WHOLE-BOOK CITATION PASS = OPEN",
):
    require(marker in human, f"I.2 human authority marker missing: {marker}")
for marker in (
    "CITATION INVENTORY = COMPLETE",
    "WHOLE-BOOK CITATION PASS = OPEN",
):
    require(marker in current, f"current overlay marker missing: {marker}")
for forbidden in (
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "NEW DIRECT QUOTES APPROVED = 1",
    "READER MANUSCRIPT CHANGES = 1",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"I.2 authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart I.2 citation review: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "Heart I.2 citation review: PASS — "
    "23/23 Scripture locators governed, 24/24 quotation surfaces classified, "
    "0 direct quotes, entry pass 1/18, manuscripts unchanged"
)
