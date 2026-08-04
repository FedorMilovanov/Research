#!/usr/bin/env python3
"""Validate the paraphrase-only X.2 final-book reader assembly."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
ASSEMBLY = ROOT / "data/heart-x2-reader-assembly-2026-08-04.json"
OWNER = ROOT / "data/heart-x2-owner-closure-2026-08-04.json"
CURRENT_PASS = ROOT / "data/heart-entry-citation-pass-current-2026-08-04.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/97_READER_CHAPTER_X2_GLORIFIED_HEART_2026-08-04.md"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/98_X2_READER_ASSEMBLY_2026-08-04.md"
PRODUCT_PATH = Path("src/content/articles/osvobozhdennoe-serdce.mdx")

OWNER_BLOB = "c1fdcfba816bdc6131d157760632d4899f89731c"
CURRENT_PASS_BLOB = "79cfd859180a95da76c8102bc4167f245487dd74"
READER_BLOB = "72f6a9d70b32af65d7a44c297d467e9fabdc4a85"
PRODUCT_BLOB = "16a2390da6e0d0382165fc8bf8b7150cb9253c1f"
PRODUCT_FULL_SHA = "621c0ab9af7a417cf73d9012f7ed02be74d02223a24af65a836b875a06d32e9d"
EXPECTED_SECTIONS = [
    ("chetyre-sostoyaniya", "1f85220c268c2c11b7e3b50345241fa42baf8690c21dd17ba525655ffa7466aa", 2381, [], 2, 0),
    ("vopl-i-otvet", "ecbec7c26d082cb710fc141521561e31d68e9414f65d4f6ebcb85aca810d9d96", 1885, ["Рим.7:24", "Рим.7:25", "Рим.8:23", "Флп.1:6"], 7, 1),
    ("ne-besplotnoe-parenie", "9627108225bf3d8791ae9f8ba01b5e4e44819eb46e3c815a5cb141dbdc54db01", 2428, ["1 Кор.15:42,44", "Флп.3:21"], 5, 1),
    ("ne-sposobno-greshit", "2b5d382283b401e016257e2f14eac7f17c51a86482f98ce53cf9e86ea652aa6f", 2396, ["1 Ин.3:2", "Евр.12:23", "Мф.5:8"], 5, 0),
    ("pobeda-nad-vragom", "fded44e3bae5140bfb54536f75c483d65272da7f19f347f02cf51ba4ff1583d2", 1605, ["1 Кор.15:55,57"], 4, 1),
]
EXPECTED_HEADINGS = [
    "## После суда — положительная цель спасения",
    "## Четыре состояния и направление искупления",
    "## Стенание имеет предел",
    "## Искупление всего человека",
    "## Свобода, которую нельзя утратить",
    "## Последний враг будет уничтожен",
    "## Что эта надежда меняет сейчас",
    "## Границы главы",
    "## Для размышления",
    "## Переход",
]
EXPECTED_REMAINING = {
    "HEART-BOOK-I1", "HEART-BOOK-I3", "HEART-BOOK-I4", "HEART-BOOK-II",
    "HEART-BOOK-III1", "HEART-BOOK-III2", "HEART-BOOK-III4", "HEART-BOOK-IV",
    "HEART-BOOK-V", "HEART-BOOK-VI", "HEART-BOOK-VII", "HEART-BOOK-VIII",
    "HEART-BOOK-IX",
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


def git_blob(root: Path, path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=root, text=True).strip()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def import_builder() -> Any:
    spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
    require(spec is not None and spec.loader is not None, "inventory builder import unavailable")
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[`*_#>\[\](){}]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def long_sentences(text: str) -> set[str]:
    return {
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", normalize(text))
        if len(sentence.strip()) >= 120
    }


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
product_root = parser.parse_args().product_root.resolve()
product_file = product_root / PRODUCT_PATH
require(product_root.is_dir(), "exact Product checkout missing")
require(product_file.is_file(), "exact X.2 Product source missing")

for path, blob in ((OWNER, OWNER_BLOB), (CURRENT_PASS, CURRENT_PASS_BLOB), (READER, READER_BLOB)):
    require(path.is_file(), f"immutable Research source missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(git_blob(ROOT, path.relative_to(ROOT)) == blob, f"immutable Research blob drift: {path.relative_to(ROOT)}")
if product_file.is_file():
    require(git_blob(product_root, PRODUCT_PATH) == PRODUCT_BLOB, "immutable Product blob drift")

reader_text = READER.read_text(encoding="utf-8") if READER.is_file() else ""
product_text = product_file.read_text(encoding="utf-8") if product_file.is_file() else ""
require(sha256_text(product_text) == PRODUCT_FULL_SHA, "X.2 Product full SHA drift")
require(reader_text.startswith("# X.2. Освобождённое сердце\n"), "X.2 reader title drift")
positions = [reader_text.find(heading) for heading in EXPECTED_HEADINGS]
require(all(position >= 0 for position in positions), "X.2 reader required heading missing")
require(positions == sorted(positions), "X.2 reader heading order drift")
for marker in (
    "HEART-X2-READER-ASSEMBLY-2026-08-04",
    "**Новые прямые цитаты:** `0`",
    "ASSEMBLED / PARAPHRASE-ONLY / ENTRY CITATION PASS OPEN",
    "X.2 READER ASSEMBLY = COMPLETE",
    "X.2 ENTRY CITATION PASS = OPEN",
    "WHOLE-BOOK ENTRY CITATION PASSES = 4 / 18",
    "WHOLE-BOOK READER ASSEMBLY = INCOMPLETE",
    "NEW DIRECT QUOTES = 0",
    "PRODUCT RELEASE = NOT CLAIMED",
):
    require(marker in reader_text, f"X.2 reader boundary marker missing: {marker}")
for forbidden in (
    "X.2 ENTRY CITATION PASS = COMPLETE",
    "WHOLE-BOOK ENTRY CITATION PASSES = 5 / 18",
    "WHOLE-BOOK READER ASSEMBLY = COMPLETE",
    "NEW DIRECT QUOTES = 1",
    "PRODUCT RELEASE = COMPLETE",
):
    require(forbidden not in reader_text, f"X.2 reader contains forbidden marker: {forbidden}")

builder = import_builder()
reader_scan: dict[str, Any] = {}
if builder is not None:
    reader_scan = builder.scan_owner(builder.r(str(READER.relative_to(ROOT)), "assembled X.2 reader"), product_root)
reader_refs = reader_scan.get("scriptureReferences", [])
require(len(reader_refs) == 9, f"X.2 reader Scripture-reference count drift: {len(reader_refs)}")
require(reader_scan.get("externalLinks") == [], "X.2 reader external links must remain absent")
require(reader_scan.get("internalArticleLinks") == [], "X.2 reader internal links must remain absent")
require(reader_scan.get("footnoteDefinitions") == 0, "X.2 reader footnotes must remain absent")
require(reader_scan.get("markdownBlockquotes") == 0, "X.2 reader Markdown blockquotes must remain absent")
require(reader_scan.get("htmlBlockquotes") == 0, "X.2 reader HTML blockquotes must remain absent")
require(reader_scan.get("inlineQuotationSegments") == 0, "X.2 reader quotation surfaces must remain zero")
word_count = len(re.findall(r"[A-Za-zА-Яа-яЁё0-9-]+", reader_text))
require(1200 <= word_count <= 2200, f"X.2 reader word count outside boundary: {word_count}")

actual_sections: list[dict[str, Any]] = []
source_refs: set[str] = set()
source_quotes: list[str] = []
source_blocks: list[str] = []
source_texts: list[str] = []
for section_id, expected_sha, expected_bytes, expected_refs, expected_inline, expected_blocks in EXPECTED_SECTIONS:
    scoped = builder.extract_sections(product_text, [section_id]) if builder is not None else ""
    refs = sorted({builder.normalize_ref(match.group(0)) for match in builder.SCRIPTURE_RE.finditer(scoped)}, key=str.casefold) if builder is not None else []
    urls = sorted({builder.trim_url(match.group(0)) for match in builder.URL_RE.finditer(scoped)}, key=str.casefold) if builder is not None else []
    internal = sorted(set(builder.ARTICLE_LINK_RE.findall(scoped))) if builder is not None else []
    quotes = re.findall(r"«([^»\n]{8,})»", scoped) + re.findall(r"“([^”\n]{8,})”", scoped)
    blocks = [line.lstrip()[1:].strip() for line in scoped.splitlines() if re.match(r"^\s*>\s?\S", line)]
    require(bool(scoped.strip()), f"X.2 Product section missing: {section_id}")
    require(sha256_text(scoped) == expected_sha, f"X.2 Product section SHA drift: {section_id}")
    require(len(scoped.encode("utf-8")) == expected_bytes, f"X.2 Product section byte drift: {section_id}")
    require(refs == expected_refs, f"X.2 Product section Scripture set drift: {section_id}")
    require(len(quotes) == expected_inline, f"X.2 Product section inline quotation drift: {section_id}")
    require(len(blocks) == expected_blocks, f"X.2 Product section blockquote drift: {section_id}")
    require(urls == [], f"X.2 Product section external-link drift: {section_id}")
    expected_internal = ["/articles/krajne-li-isporcheno-serdce/"] if section_id == "chetyre-sostoyaniya" else []
    require(internal == expected_internal, f"X.2 Product section internal-link drift: {section_id}")
    source_refs.update(refs)
    source_quotes.extend(quotes)
    source_blocks.extend(blocks)
    source_texts.append(scoped)
    actual_sections.append({"id": section_id, "sha": expected_sha, "bytes": expected_bytes, "refs": refs, "inline": len(quotes), "blocks": len(blocks)})
require(len(source_refs) == 10, "X.2 Product aggregate Scripture count drift")
require(len(source_quotes) == 23, "X.2 Product aggregate inline quotation count drift")
require(len(source_blocks) == 3, "X.2 Product aggregate blockquote count drift")
require(len(source_quotes) + len(source_blocks) == 26, "X.2 Product aggregate quotation-surface count drift")
reader_normalized = normalize(reader_text)
for quote in source_quotes:
    normalized_quote = normalize(quote)
    if len(normalized_quote) >= 40:
        require(normalized_quote not in reader_normalized, f"X.2 reader copies a material Product quotation: {quote[:80]}")
for block in source_blocks:
    require(normalize(block) not in reader_normalized, f"X.2 reader copies a Product blockquote: {block[:80]}")
require(long_sentences("\n".join(source_texts)).isdisjoint(long_sentences(reader_text)), "X.2 reader contains a long exact Product sentence")

owner = read_json(OWNER)
require(owner.get("authorityId") == "HEART-X2-OWNER-CLOSURE-2026-08-04", "X.2 owner authority drift")
require(owner.get("status") == "X2_PRODUCT_SOURCE_ESTABLISHED_UNIFIED_READER_AND_BOOK_CITATION_PASS_OPEN", "X.2 owner status drift")
require(owner.get("productSnapshot", {}).get("commit") == "0fbe7d1ead9ebd1bea867418e254da438ec63329", "X.2 owner Product commit drift")
require(owner.get("productSnapshot", {}).get("articleOwner", {}).get("blobSha") == PRODUCT_BLOB, "X.2 owner Product blob drift")
override = owner.get("entryOverride", {})
require(override.get("id") == "HEART-BOOK-X2", "X.2 owner entry ID drift")
require(override.get("effectivePrimaryState") == "PRODUCT_SOURCE_ONLY", "X.2 historical primary state drift")
require(override.get("manuscriptState") == "SOURCE_SELECTED_UNIFIED_X2_READER_NOT_ASSEMBLED", "X.2 historical manuscript state drift")
require([row.get("id") for row in override.get("sectionOwners", [])] == [row[0] for row in EXPECTED_SECTIONS], "X.2 owner section order drift")
require(override.get("effectiveCitationState") == "PRODUCT_SOURCE_CITATION_PASS_REQUIRED", "X.2 historical citation state drift")
require(owner.get("publicationBoundary", {}).get("x2UnifiedReaderAssembled") is False, "historical X.2 owner receipt rewritten")
require(owner.get("publicationBoundary", {}).get("newDirectQuotesApproved") == 0, "X.2 owner direct-quote boundary drift")

preceding = read_json(CURRENT_PASS)
require(preceding.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-2026-08-04", "preceding current citation authority drift")
require(preceding.get("currentCounts", {}).get("entryCitationPassComplete") == 4, "preceding citation count drift")
require(preceding.get("currentCounts", {}).get("assembledReaderEntries") == 4, "preceding assembled-reader count drift")
require(preceding.get("currentCounts", {}).get("missingStandaloneFinalReaders") == 14, "preceding reader backlog drift")
require("HEART-BOOK-X2" in preceding.get("openEntryIds", []), "X.2 missing from preceding open set")

assembly = read_json(ASSEMBLY)
require(assembly.get("authorityId") == "HEART-X2-READER-ASSEMBLY-2026-08-04", "X.2 assembly authority drift")
require(assembly.get("status") == "X2_FINAL_BOOK_READER_ASSEMBLED_PARAPHRASE_ONLY_ENTRY_CITATION_PASS_OPEN", "X.2 assembly status drift")
require(assembly.get("ownerAuthority", {}).get("gitBlob") == OWNER_BLOB, "X.2 assembly owner blob drift")
require(assembly.get("precedingCurrentCitationAuthority", {}).get("gitBlob") == CURRENT_PASS_BLOB, "X.2 assembly preceding-current blob drift")
reader_receipt = assembly.get("reader", {})
require(reader_receipt.get("gitBlob") == READER_BLOB, "X.2 assembly reader blob drift")
require(reader_receipt.get("state") == "ASSEMBLED_READER_PARAPHRASE_ONLY", "X.2 assembly reader state drift")
require(reader_receipt.get("expectedDetectedScriptureReferences") == 9, "X.2 assembly reader Scripture expectation drift")
require(reader_receipt.get("quotationSurfaces") == 0, "X.2 assembly reader quotation expectation drift")
source_receipt = assembly.get("exactProductSource", {})
require(source_receipt.get("gitBlob") == PRODUCT_BLOB, "X.2 assembly Product blob drift")
require(source_receipt.get("fullFileSha256") == PRODUCT_FULL_SHA, "X.2 assembly Product SHA drift")
receipt_sections = source_receipt.get("sections", [])
require([row.get("id") for row in receipt_sections] == [row[0] for row in EXPECTED_SECTIONS], "X.2 assembly section order drift")
for receipt_row, actual_row in zip(receipt_sections, actual_sections, strict=True):
    require(receipt_row.get("scopedSha256") == actual_row["sha"], f"X.2 receipt section SHA drift: {actual_row['id']}")
    require(receipt_row.get("bytes") == actual_row["bytes"], f"X.2 receipt section byte drift: {actual_row['id']}")
    require(receipt_row.get("scriptureReferences") == actual_row["refs"], f"X.2 receipt section Scripture drift: {actual_row['id']}")
    require(receipt_row.get("inlineQuotationSegments") == actual_row["inline"], f"X.2 receipt section inline drift: {actual_row['id']}")
    require(receipt_row.get("markdownBlockquotes") == actual_row["blocks"], f"X.2 receipt section block drift: {actual_row['id']}")
composition = assembly.get("composition", {})
require(composition.get("mode") == "PARAPHRASE_ONLY", "X.2 composition mode drift")
require(composition.get("newHistoricalClaims") == 0, "X.2 historical claim drift")
require(composition.get("newDirectQuotesApproved") == 0, "X.2 direct quote drift")
require(composition.get("exactProductQuotationSegmentsCopied") == 0, "X.2 Product quote-transfer drift")
require(composition.get("exactProductBlockquotesCopied") == 0, "X.2 Product blockquote-transfer drift")
require(composition.get("longExactProductSentencesCopied") == 0, "X.2 Product sentence-transfer drift")
state = assembly.get("effectivePrimaryState", {})
require(state.get("previous") == "PRODUCT_SOURCE_ONLY" and state.get("current") == "ASSEMBLED_READER", "X.2 state transition drift")
require(state.get("entryCitationPassComplete") is False, "X.2 citation pass falsely closed")
require(assembly.get("effectiveCounts") == {
    "finalBookEntries": 18,
    "assembledReader": 5,
    "missingStandaloneFinalReaders": 13,
    "entryCitationPassComplete": 4,
    "entryCitationPassOpen": 14,
    "productSourceOnly": 7,
    "researchDossierOnly": 6,
    "newDirectQuotesApproved": 0,
}, "X.2 effective count drift")
require(set(assembly.get("remainingReaderAssemblies", [])) == EXPECTED_REMAINING, "X.2 remaining reader set drift")
boundary = assembly.get("publicationBoundary", {})
require(boundary.get("x2UnifiedReaderAssembled") is True, "X.2 reader assembly not complete")
require(boundary.get("x2EntryCitationPassComplete") is False, "X.2 citation pass falsely complete")
require(boundary.get("allCurrentlyAssembledReadersCitationReviewed") is False, "five-reader review state falsely closed")
require(boundary.get("wholeBookReaderAssemblyComplete") is False, "whole-book reader assembly falsely closed")
require(boundary.get("wholeBookCitationPassComplete") is False, "whole-book citation pass falsely closed")
require(boundary.get("productReleaseComplete") is False, "Product release falsely closed")
require(boundary.get("newDirectQuotesApproved") == 0, "X.2 publication direct-quote drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-X2-READER-ASSEMBLY-2026-08-04",
    "X.2 READER ASSEMBLY = COMPLETE",
    "X.2 ENTRY CITATION PASS = OPEN",
    "ASSEMBLED READERS = 5 / 18",
    "MISSING STANDALONE FINAL READERS = 13",
    "WHOLE-BOOK ENTRY CITATION PASSES = 4 / 18",
    "PRODUCT QUOTATION SEGMENTS COPIED = 0",
    "NEW DIRECT QUOTES APPROVED = 0",
    "WHOLE-BOOK READER ASSEMBLY = INCOMPLETE",
    READER_BLOB,
    PRODUCT_BLOB,
):
    require(marker in human, f"X.2 human authority marker missing: {marker}")
for forbidden in (
    "X.2 ENTRY CITATION PASS = COMPLETE",
    "WHOLE-BOOK ENTRY CITATION PASSES = 5 / 18",
    "WHOLE-BOOK READER ASSEMBLY = COMPLETE",
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"X.2 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart X.2 reader assembly: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "Heart X.2 reader assembly: PASS — "
    f"{word_count} words, 9 Scripture locators, paraphrase-only, "
    "5 assembled readers, 13 remaining, citation passes 4/18, 0 new direct quotes"
)
