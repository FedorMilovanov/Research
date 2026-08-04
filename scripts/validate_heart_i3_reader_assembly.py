#!/usr/bin/env python3
"""Validate the paraphrase-only I.3 final-book reader assembly."""
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
RECEIPT_PATH = ROOT / "data/heart-i3-reader-assembly-2026-08-04.json"
READER_PATH = ROOT / "СЕРИЯ СЕРДЦЕ/109_READER_CHAPTER_I3_FALLEN_HEART_JEREMIAH_17_2026-08-04.md"
HUMAN_PATH = ROOT / "СЕРИЯ СЕРДЦЕ/110_I3_READER_ASSEMBLY_2026-08-04.md"
PRODUCT_REL = Path("src/content/articles/krajne-li-isporcheno-serdce.mdx")

EXPECTED_RESEARCH_BLOBS = {
    ROOT / "data/heart-entry-citation-pass-current-v4-2026-08-04.json": "d0ddea6cf1fc33dfab53ae9691aaf2d903d03b73",
    ROOT / "data/heart-whole-book-integration-2026-08-04.json": "06d67275c42c7a9c3bd0365044f358b4b7d7a895",
    ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json": "de4d49cada15b231dfc31058aced4ec7a25928a2",
    ROOT / "СЕРИЯ СЕРДЦЕ/105_READER_CHAPTER_I1_WHAT_BIBLE_CALLS_HEART_2026-08-04.md": "a5d35df1a87ab39abc8a85b1d84f1b1ab03da105",
    ROOT / "СЕРИЯ СЕРДЦЕ/79_READER_CHAPTER_I2_HEART_IN_EDEN_2026-08-02.md": "204545a59477d92839245800f56791466bf45349",
    ROOT / "СЕРИЯ СЕРДЦЕ/65_R3_UNREGENERATE_STRUGGLE.md": "ae55b1fad5cccbdb623c551a14222e0f51ec084a",
    ROOT / "СЕРИЯ СЕРДЦЕ/66_R4_FOUR_SOILS.md": "f82780e13cb064aa89c06427d11a938662fc3ff8",
}
EXPECTED_SELECTED_IDS = [
    "istoricheskiy-fon",
    "greh-vyrezannyy",
    "dva-obraza-doveriya",
    "serdce-istochnik-samoobmana",
    "otnositsya-li-k-veruyushchemu",
    "chto-izmenilos",
    "kak-greh-stanovitsya-strukturoy",
    "kak-nelzya-primenyat",
    "praktika",
    "velikaya-nadezhda",
]
EXPECTED_EXCLUDED_IDS = ["sec-quiz", "zaklyuchenie", "istochniki", "literatura", "spravka"]
EXPECTED_FALSE_POSITIVE_SOURCE_HEADINGS = ["Два источника доверия", "Сердце как источник самообмана"]
EXPECTED_REQUIRED_HEADINGS = [
    "Пророческое слово накануне катастрофы",
    "Грех, вошедший в устройство жизни",
    "Два источника доверия",
    "Сердце как источник самообмана",
    "Описывает ли этот текст верующего",
    "Что изменилось и что осталось",
    "Как грех становится внутренней структурой",
    "Две противоположные ошибки",
    "Божье испытание и евангельская безопасность",
    "Практика испытания сердца",
    "Надежда нового завета",
    "Для размышления",
    "Переход",
]
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


def git_blob(path: Path, repo_root: Path = ROOT) -> str:
    return subprocess.check_output(["git", "hash-object", str(path.relative_to(repo_root))], cwd=repo_root, text=True).strip()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalized(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def word_count(value: str) -> int:
    return len(re.findall(r"[A-Za-zА-Яа-яЁё0-9]+(?:[.–—-][A-Za-zА-Яа-яЁё0-9]+)*", value))


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()
product_path = product_root / PRODUCT_REL

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

receipt = read_json(RECEIPT_PATH)
current_v4 = read_json(ROOT / "data/heart-entry-citation-pass-current-v4-2026-08-04.json")
integration = read_json(ROOT / "data/heart-whole-book-integration-2026-08-04.json")
triage = read_json(ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json")
reader_text = READER_PATH.read_text(encoding="utf-8")
product_text = product_path.read_text(encoding="utf-8")

for path, expected_blob in EXPECTED_RESEARCH_BLOBS.items():
    require(path.is_file(), f"immutable Research witness missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(git_blob(path) == expected_blob, f"immutable Research witness blob drift: {path.relative_to(ROOT)}")
require(git_blob(READER_PATH) == "a958066bff3010f14540d67c900c362bd88de98a", "I.3 reader blob drift")
require(git_blob(product_path, product_root) == "dc27b7a06d37321a068e971c02af4a0df3028ae6", "I.3 Product blob drift")
require(sha256_text(reader_text) == "6d00cbd44a7d3540faddcbdbc03bfff1fd1c5a441c380392010f973d76ce92f9", "I.3 reader SHA-256 drift")
require(sha256_text(product_text) == "4292f76ff3e2fa15dfd682b5a421400ce9a62ec391109b3109aef14d72b224f0", "I.3 Product SHA-256 drift")

full_scan = module.scan_owner(module.p(str(PRODUCT_REL), "historical full I.3 owner"), product_root)
reader_scan = module.scan_owner(module.r(str(READER_PATH.relative_to(ROOT)), "assembled I.3 reader"), product_root)
require(len(full_scan["scriptureReferences"]) == 71, "I.3 historical Product Scripture count drift")
require(full_scan["inlineQuotationSegments"] + full_scan["markdownBlockquotes"] + full_scan["htmlBlockquotes"] == 224, "I.3 historical Product quotation count drift")
require(len(full_scan["externalLinks"]) == 15, "I.3 historical Product external-link count drift")
require(len(full_scan["internalArticleLinks"]) == 3, "I.3 historical Product internal-link count drift")

section_starts = [(m.start(), m.group(1)) for m in re.finditer(r'<h2\s+id="([^"]+)"', product_text)]
section_rows: list[dict[str, Any]] = []
for index, (start, section_id) in enumerate(section_starts):
    end = section_starts[index + 1][0] if index + 1 < len(section_starts) else len(product_text)
    scoped = product_text[start:end]
    refs = sorted({module.normalize_ref(m.group(0)) for m in module.SCRIPTURE_RE.finditer(scoped)}, key=str.casefold)
    external = sorted({module.trim_url(m.group(0)) for m in module.URL_RE.finditer(scoped)}, key=str.casefold)
    internal = sorted(set(module.ARTICLE_LINK_RE.findall(scoped)))
    russian = re.findall(r"«([^»\n]{8,})»", scoped)
    curly = re.findall(r"“([^”\n]{8,})”", scoped)
    markdown_blocks = [line.lstrip()[1:].strip() for line in scoped.splitlines() if re.match(r"^\s*>\s?\S", line)]
    html_blocks = [re.sub(r"<[^>]+>", " ", item).strip() for item in re.findall(r"<blockquote[^>]*>(.*?)</blockquote>", scoped, flags=re.S | re.I)]
    section_rows.append({"id": section_id, "sha256": sha256_text(scoped), "bytes": len(scoped.encode("utf-8")), "scriptureReferences": refs, "externalLinks": external, "internalArticleLinks": internal, "inlineQuotationSegments": len(russian) + len(curly), "markdownBlockquotes": len(markdown_blocks), "htmlBlockquotes": len(html_blocks), "quotationSurfaces": len(russian) + len(curly) + len(markdown_blocks) + len(html_blocks), "text": scoped})
require(len(section_rows) == 15, "I.3 Product H2 section count drift")
selected_rows = [row for row in section_rows if row["id"] in EXPECTED_SELECTED_IDS]
require([row["id"] for row in selected_rows] == EXPECTED_SELECTED_IDS, "I.3 selected section order drift")
require(sorted(set(row["id"] for row in section_rows) - set(EXPECTED_SELECTED_IDS)) == sorted(EXPECTED_EXCLUDED_IDS), "I.3 excluded section set drift")

selected_refs = sorted({ref for row in selected_rows for ref in row["scriptureReferences"]}, key=str.casefold)
selected_external = sorted({url for row in selected_rows for url in row["externalLinks"]}, key=str.casefold)
selected_internal = sorted({url for row in selected_rows for url in row["internalArticleLinks"]})
manifest = [{key: row[key] for key in ("id", "sha256", "bytes", "quotationSurfaces")} for row in selected_rows]
require(sum(row["bytes"] for row in selected_rows) == 100152, "I.3 selected byte count drift")
require(len(selected_refs) == 62, "I.3 selected Scripture count drift")
require(sum(row["quotationSurfaces"] for row in selected_rows) == 193, "I.3 selected quotation count drift")
require(len(selected_external) == 6, "I.3 selected external-link count drift")
require(len(selected_internal) == 1, "I.3 selected internal-link count drift")
require(sha256_text(json.dumps(selected_refs, ensure_ascii=False, separators=(",", ":"))) == "ebad12d8f1a9d8c1f0c1bd5fd4790ee49fd24f0d4e04626e5cd785cfdb2b702b", "I.3 selected Scripture-set hash drift")
require(sha256_text(json.dumps(manifest, ensure_ascii=False, separators=(",", ":"))) == "8804a6e3488a8c5feea6c264b8d08e6ec8530852f452167a73a2db4f1919ebc2", "I.3 selected section-manifest hash drift")

receipt_rows = receipt.get("exactProductSource", {}).get("selectedAssemblySections", [])
require([{key: row.get(key) for key in ("id", "sha256", "bytes", "quotationSurfaces")} for row in receipt_rows] == manifest, "I.3 receipt section manifest drift")
require(receipt.get("exactProductSource", {}).get("selectedAggregate", {}).get("uniqueScriptureReferences") == 62, "I.3 receipt selected Scripture count drift")
require(receipt.get("exactProductSource", {}).get("historicalFullOwner", {}) == {"ownerSurfaces": 1, "sourceHeadings": 0, "scriptureReferences": 71, "quotationSurfaces": 224, "externalLinks": 15, "internalArticleLinks": 3}, "I.3 receipt historical owner drift")

require(word_count(reader_text) == 1708, "I.3 reader word count drift")
require(1600 <= word_count(reader_text) <= 2200, "I.3 reader outside accepted word boundary")
require(len(reader_scan["scriptureReferences"]) == 13, "I.3 reader Scripture locator count drift")
require(reader_scan["inlineQuotationSegments"] + reader_scan["markdownBlockquotes"] + reader_scan["htmlBlockquotes"] == 0, "I.3 reader quotation surface detected")
require(len(reader_scan["externalLinks"]) == 0, "I.3 reader external link detected")
require(len(reader_scan["internalArticleLinks"]) == 0, "I.3 reader internal article link detected")
require(reader_scan["footnoteDefinitions"] == 0, "I.3 reader footnote definition detected")
require(reader_scan["sourceHeadings"] == EXPECTED_FALSE_POSITIVE_SOURCE_HEADINGS, "I.3 source-heading false-positive set drift")
for heading in EXPECTED_REQUIRED_HEADINGS:
    require(f"## {heading}" in reader_text, f"I.3 reader heading missing: {heading}")
for marker in ("PARAPHRASE-ONLY", "ENTRY CITATION PASS OPEN", "Новые прямые цитаты:** `0`", "Эта глава не заменяет широкий диагноз невозрождённого человека", "Следующая часть расширяет перспективу"):
    require(marker in reader_text, f"I.3 reader boundary marker missing: {marker}")

reader_normalized = normalized(reader_text).casefold()
for row in selected_rows:
    source_normalized = normalized(row["text"]).casefold()
    for sentence in re.split(r"(?<=[.!?])\s+", source_normalized):
        sentence = sentence.strip(" -*")
        if len(sentence) >= 140:
            require(sentence not in reader_normalized, f"I.3 reader copies a long Product sentence from {row['id']}")

require(current_v4.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V4-2026-08-04", "current V4 authority drift")
require(current_v4.get("currentCounts", {}).get("entryCitationPassComplete") == 7, "current V4 completed count drift")
require("HEART-BOOK-I3" in current_v4.get("openEntryIds", []), "current V4 does not retain I.3 as open")
integration_entry = next((row for row in integration.get("entries", []) if row.get("id") == "HEART-BOOK-I3"), {})
require(integration_entry.get("dedupOwner") == "Owns the Jeremiah 17 diagnosis and its gospel-qualified application; later diagnosis chapters must not duplicate the full exposition.", "I.3 integration ownership boundary drift")
triage_entry = next((row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-I3"), {})
require(triage_entry.get("detected") == {"ownerSurfaces": 1, "sourceHeadings": 0, "scriptureReferences": 71, "externalLinks": 15, "internalArticleLinks": 3, "quotationSurfaces": 224}, "I.3 historical triage row drift")
require(triage_entry.get("disposition", {}).get("triageState") == "TRIAGED_OPEN", "I.3 historical triage state rewritten")

require(receipt.get("authorityId") == "HEART-I3-READER-ASSEMBLY-2026-08-04", "I.3 receipt authority drift")
require(receipt.get("effectiveCounts") == {"finalBookEntries": 18, "assembledReader": 8, "missingStandaloneFinalReaders": 10, "entryCitationPassComplete": 7, "entryCitationPassOpen": 11, "assembledReaderCitationReviewsComplete": 7, "productSourceOnly": 4, "researchDossierOnly": 6, "newDirectQuotesApproved": 0}, "I.3 effective count block drift")
require(receipt.get("publicationBoundary", {}).get("i3EntryCitationPassComplete") is False, "I.3 citation pass falsely closed")
require(receipt.get("publicationBoundary", {}).get("wholeBookCitationPassComplete") is False, "whole-book citation pass falsely closed")
require(receipt.get("publicationBoundary", {}).get("productReleaseComplete") is False, "Product release falsely closed")

human = HUMAN_PATH.read_text(encoding="utf-8") if HUMAN_PATH.is_file() else ""
for marker in ("HEART-I3-READER-ASSEMBLY-2026-08-04", "ASSEMBLED READERS = 8 / 18", "MISSING STANDALONE FINAL READERS = 10", "ENTRY CITATION PASSES COMPLETE = 7 / 18", "I.3 ENTRY CITATION PASS = OPEN", "SELECTED ASSEMBLY SECTIONS = 10", "SELECTED SOURCE SURFACES = 62 / 193 / 6 / 1", "HISTORICAL OWNER SURFACES = 71 / 224 / 15 / 3", "NEW DIRECT QUOTES APPROVED = 0"):
    require(marker in human, f"I.3 human authority marker missing: {marker}")
for forbidden in ("I.3 ENTRY CITATION PASS = COMPLETE", "ENTRY CITATION PASSES COMPLETE = 8 / 18", "WHOLE-BOOK CITATION PASS = COMPLETE", "PRODUCT RELEASE = COMPLETE", "TODO", "TBD"):
    require(forbidden not in human, f"I.3 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart I.3 reader assembly: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart I.3 reader assembly: PASS — 1708 words, reader 13/0/0, selected 10 sections 62/193/6/1, historical 71/224/15/3, readers 8/18, citation 7/18")
