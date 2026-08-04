#!/usr/bin/env python3
"""Validate the paraphrase-only Part II fallen-heart diagnosis reader."""
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
RECEIPT = ROOT / "data/heart-part2-reader-assembly-2026-08-04.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/113_READER_CHAPTER_II_FALLEN_HEART_DIAGNOSIS_2026-08-04.md"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/114_PART2_READER_ASSEMBLY_2026-08-04.md"
R3 = ROOT / "СЕРИЯ СЕРДЦЕ/65_R3_UNREGENERATE_STRUGGLE.md"
R4 = ROOT / "СЕРИЯ СЕРДЦЕ/66_R4_FOUR_SOILS.md"
I3 = ROOT / "СЕРИЯ СЕРДЦЕ/109_READER_CHAPTER_I3_FALLEN_HEART_JEREMIAH_17_2026-08-04.md"
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v5-2026-08-04.json"
INTEGRATION = ROOT / "data/heart-whole-book-integration-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"

EXPECTED_BLOBS = {
    R3: "ae55b1fad5cccbdb623c551a14222e0f51ec084a",
    R4: "f82780e13cb064aa89c06427d11a938662fc3ff8",
    I3: "a958066bff3010f14540d67c900c362bd88de98a",
    CURRENT: "2ba8c381e636a9f1148fa30e3f010d595feb42a6",
    INTEGRATION: "06d67275c42c7a9c3bd0365044f358b4b7d7a895",
    TRIAGE: "de4d49cada15b231dfc31058aced4ec7a25928a2",
    READER: "4cca195d034c70a7d3d6c3dd8edc9a04fcffcc20",
}
EXPECTED_SHA = {
    R3: "12c4344acfc96050eaae35d98ed666102e62c700ead9db34c24681a914102efb",
    R4: "1e5ff030fea335f64dda3a613898d1237d3a4e34d0c303d67f51a64af92e1964",
    READER: "c7e37a30651bf96f77f2a2eba204251591edb2ab28aff1cc8332d6c72f99086d",
}
REQUIRED_HEADINGS = [
    "Он действительно борется",
    "Горизонтальная победа и вертикальный предел",
    "Совесть не становится тайным Евангелием",
    "Моральный человек у двери",
    "Одно слово перед четырьмя сердцами",
    "Дорога: слово остаётся снаружи",
    "Камень: яркий старт без корня",
    "Терние: сердце, занятое всем остальным",
    "Добрая земля: хранить и приносить плод",
    "Не калькулятор чужих почв",
    "Единый диагноз двух линий",
    "Для размышления",
    "Переход",
]
errors: list[str] = []


def require(value: bool, message: str) -> None:
    if not value:
        errors.append(message)


def blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def json_sha(value: Any) -> str:
    return sha(json.dumps(value, ensure_ascii=False, separators=(",", ":")))


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be an object")
    return value if isinstance(value, dict) else {}


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-zА-Яа-яЁё0-9]+(?:[.–—-][A-Za-zА-Яа-яЁё0-9]+)*", text))


def normalize(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().casefold()


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

for path, expected in EXPECTED_BLOBS.items():
    require(path.is_file(), f"immutable witness missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(path) == expected, f"immutable witness blob drift: {path.relative_to(ROOT)}")
texts = {path: path.read_text(encoding="utf-8") for path in (R3, R4, I3, READER)}
for path, expected in EXPECTED_SHA.items():
    require(sha(texts[path]) == expected, f"source SHA drift: {path.relative_to(ROOT)}")

receipt = read_json(RECEIPT)
current = read_json(CURRENT)
integration = read_json(INTEGRATION)
triage = read_json(TRIAGE)

r3_scan = module.scan_owner(module.r(str(R3.relative_to(ROOT)), "Part II R3 owner"), product_root)
r4_scan = module.scan_owner(module.r(str(R4.relative_to(ROOT)), "Part II R4 owner"), product_root)
reader_scan = module.scan_owner(module.r(str(READER.relative_to(ROOT)), "Part II reader"), product_root)

def qcount(scan: dict[str, Any]) -> int:
    return scan["inlineQuotationSegments"] + scan["markdownBlockquotes"] + scan["htmlBlockquotes"]

require(len(r3_scan["scriptureReferences"]) == 50, "R3 Scripture count drift")
require(qcount(r3_scan) == 304, "R3 quotation count drift")
require(len(r3_scan["externalLinks"]) == 53, "R3 external-link count drift")
require(len(r3_scan["internalArticleLinks"]) == 1, "R3 internal-link count drift")
require(r3_scan["sourceHeadings"] == ["Цитатный банк (каждая цитата с источником и ссылкой)"], "R3 source-heading drift")
require(len(r4_scan["scriptureReferences"]) == 68, "R4 Scripture count drift")
require(qcount(r4_scan) == 133, "R4 quotation count drift")
require(len(r4_scan["externalLinks"]) == 27, "R4 external-link count drift")
require(len(r4_scan["internalArticleLinks"]) == 0, "R4 internal-link count drift")
require(r4_scan["sourceHeadings"] == [], "R4 source-heading drift")

union_refs = sorted(set(r3_scan["scriptureReferences"]) | set(r4_scan["scriptureReferences"]), key=str.casefold)
union_external = sorted(set(r3_scan["externalLinks"]) | set(r4_scan["externalLinks"]), key=str.casefold)
union_internal = sorted(set(r3_scan["internalArticleLinks"]) | set(r4_scan["internalArticleLinks"]), key=str.casefold)
require(len(union_refs) == 118, "Part II union Scripture count drift")
require(json_sha(union_refs) == "5d78a0e23ed09e10f71dfcf9010269430c53faf2bd6ffe1225a3160ee9ffc4a6", "Part II Scripture-set hash drift")
require(qcount(r3_scan) + qcount(r4_scan) == 437, "Part II quotation total drift")
require(len(union_external) == 80, "Part II external-link union drift")
require(json_sha(union_external) == "f5ce26d3f27bf9e6aa2c87e625d9b91875d580f296d02d80e974a27dd279187f", "Part II external-link set hash drift")
require(union_internal == ["/articles/opinion/"], "Part II internal-link set drift")
require(json_sha(union_internal) == "340d19206af863e8b9a7098a84d47199360bec49d1062545c199a4fda8572c65", "Part II internal-link set hash drift")

reader_text = texts[READER]
require(word_count(reader_text) == 1671, "Part II reader word count drift")
require(1600 <= word_count(reader_text) <= 2200, "Part II reader outside accepted word boundary")
require(len(reader_scan["scriptureReferences"]) == 20, "Part II reader Scripture count drift")
require(json_sha(sorted(reader_scan["scriptureReferences"], key=str.casefold)) == "cf61799664220cc835851e4e356198568786eb1962bfc1b17d4acdae8f2c9e23", "Part II reader Scripture-set hash drift")
require(qcount(reader_scan) == 0, "Part II reader quotation surface detected")
require(len(reader_scan["externalLinks"]) == 0, "Part II reader external link detected")
require(len(reader_scan["internalArticleLinks"]) == 0, "Part II reader internal link detected")
require(reader_scan["sourceHeadings"] == [], "Part II reader source heading detected")
require(reader_scan["footnoteDefinitions"] == 0, "Part II reader footnote detected")
for heading in REQUIRED_HEADINGS:
    require(f"## {heading}" in reader_text, f"Part II reader heading missing: {heading}")
for marker in (
    "PARAPHRASE-ONLY", "ENTRY CITATION PASS OPEN", "Новые прямые цитаты:** `0`",
    "Иер. 17 дал точную экспозицию", "Эта глава ещё не раскрывает всё учение о рождении свыше",
    "Следующая глава обращается к Божьему обещанию",
):
    require(marker in reader_text, f"Part II reader boundary marker missing: {marker}")

reader_norm = normalize(reader_text)
for source_path in (R3, R4, I3):
    for sentence in re.split(r"(?<=[.!?])\s+", normalize(texts[source_path])):
        sentence = sentence.strip(" -*")
        if len(sentence) >= 150:
            require(sentence not in reader_norm, f"Part II reader copies a long sentence from {source_path.name}")

require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V5-2026-08-04", "current V5 authority drift")
require(current.get("currentCounts", {}).get("entryCitationPassComplete") == 8, "current V5 citation count drift")
require("HEART-BOOK-II" in current.get("openEntryIds", []), "current V5 does not retain Part II open")
integration_entry = next((row for row in integration.get("entries", []) if row.get("id") == "HEART-BOOK-II"), {})
require(integration_entry.get("dedupOwner") == "Owns the unregenerate struggle ceiling and four-soils diagnosis without retelling I.2 or the full Jeremiah 17 exposition.", "Part II integration boundary drift")
triage_entry = next((row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-II"), {})
require(triage_entry.get("detected") == {"ownerSurfaces": 2, "sourceHeadings": 1, "scriptureReferences": 118, "externalLinks": 80, "internalArticleLinks": 1, "quotationSurfaces": 437}, "Part II historical triage row drift")
require(triage_entry.get("disposition", {}).get("triageState") == "TRIAGED_OPEN", "Part II historical triage rewritten")

require(receipt.get("authorityId") == "HEART-PART2-READER-ASSEMBLY-2026-08-04", "Part II receipt authority drift")
require(receipt.get("historicalUnion", {}).get("scriptureReferences") == 118, "Part II receipt Scripture union drift")
require(receipt.get("historicalUnion", {}).get("quotationSurfaces") == 437, "Part II receipt quotation union drift")
require(receipt.get("historicalUnion", {}).get("externalLinks") == 80, "Part II receipt external union drift")
require(receipt.get("historicalUnion", {}).get("internalArticleLinks") == 1, "Part II receipt internal union drift")
require(receipt.get("effectiveCounts") == {
    "finalBookEntries": 18,
    "assembledReader": 9,
    "missingStandaloneFinalReaders": 9,
    "entryCitationPassComplete": 8,
    "entryCitationPassOpen": 10,
    "assembledReaderCitationReviewsComplete": 8,
    "productSourceOnly": 4,
    "researchDossierOnly": 5,
    "productSourceLinkRepairsRequired": 3,
    "newDirectQuotesApproved": 0,
}, "Part II effective count block drift")
require(receipt.get("publicationBoundary", {}).get("part2EntryCitationPassComplete") is False, "Part II citation pass falsely closed")
require(receipt.get("publicationBoundary", {}).get("wholeBookCitationPassComplete") is False, "whole-book citation pass falsely closed")
require(receipt.get("publicationBoundary", {}).get("productReleaseComplete") is False, "Product release falsely closed")
require(receipt.get("publicationBoundary", {}).get("productSourceLinkRepairsComplete") is False, "Product link repairs falsely closed")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-PART2-READER-ASSEMBLY-2026-08-04",
    "ASSEMBLED READERS = 9 / 18",
    "MISSING STANDALONE FINAL READERS = 9",
    "ENTRY CITATION PASSES COMPLETE = 8 / 18",
    "PART II ENTRY CITATION PASS = OPEN",
    "HISTORICAL DOSSIER SURFACES = 118 / 437 / 80 / 1",
    "READER SURFACES = 20 / 0 / 0 / 0",
    "PRODUCT SOURCE LINK REPAIRS REQUIRED = 3",
    "NEW DIRECT QUOTES APPROVED = 0",
):
    require(marker in human, f"Part II human authority marker missing: {marker}")
for forbidden in (
    "PART II ENTRY CITATION PASS = COMPLETE", "ENTRY CITATION PASSES COMPLETE = 9 / 18",
    "PRODUCT SOURCE LINK REPAIRS REQUIRED = 0", "WHOLE-BOOK CITATION PASS = COMPLETE",
    "PRODUCT RELEASE = COMPLETE", "TODO", "TBD",
):
    require(forbidden not in human, f"Part II human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart Part II reader assembly: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Heart Part II reader assembly: PASS — 1671 words, reader 20/0/0/0, dossiers 118/437/80/1, readers 9/18, citation 8/18")
