#!/usr/bin/env python3
"""Validate the paraphrase-only I.1 final-book reader assembly."""
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
ASSEMBLY = ROOT / "data/heart-i1-reader-assembly-2026-08-04.json"
INTEGRATION = ROOT / "data/heart-whole-book-integration-2026-08-04.json"
CURRENT_V3 = ROOT / "data/heart-entry-citation-pass-current-v3-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/105_READER_CHAPTER_I1_WHAT_BIBLE_CALLS_HEART_2026-08-04.md"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/106_I1_READER_ASSEMBLY_2026-08-04.md"
PRODUCT_PATH = Path("src/content/articles/chto-bibliya-nazyvaet-serdcem.mdx")

BLOBS = {
    INTEGRATION: "06d67275c42c7a9c3bd0365044f358b4b7d7a895",
    CURRENT_V3: "407c8d78baa966a3336e7bd60edfa51178b74f32",
    TRIAGE: "de4d49cada15b231dfc31058aced4ec7a25928a2",
    READER: "bb593d52f4838cff079a7409441d2982c4f823ea",
}
PRODUCT_BLOB = "acc12804f5b2450efebbb6e0b2cabd31066ef48c"
PRODUCT_SHA = "50657f3473c06e16d75ffe740828a9311f642562e824f148113ae28ff9b03c07"
MANIFEST = [
    ("nepravilno-slyshim","f9a0f50c32df5ac2e439726c2ff212f0e17bebe3ccdedbf3fe208510dd0055bf",2553,8,10,0,0),
    ("vnutrenniy-chelovek","d6ffdf64d0b46b23cee96f4943f76ed20be117c531efdc6ca30bae199737c0b8",3115,1,3,0,0),
    ("serdce-dusha-duh","0cc608846137d909c8e5a3cd391c5b71b8d23a27e60d60d68658865382f2c33d",5035,5,7,0,0),
    ("bog-trebuet-vsyo","6ec02621b6e29ede2314149d22ca8366fccf29055dd0c4a69a12effb11cedd93",1260,3,3,0,0),
    ("bog-vidit-serdce","1f3dd8697be57b878a66e8b76ef77e7404fc8e0f8367f3e149c19bae2bf1195a",1809,4,6,0,0),
    ("serdce-myslit","42d2ee381d43c6afe8e118a2490db3bda8657cb5514c72525e56964eb57c65ba",1210,5,6,0,0),
    ("serdce-reshaet","fbcffd8dacefea983e3395797c2fb69cc19b29e4d3ae954e7b4d02bd76cbed18",1501,4,4,0,0),
    ("serdce-lyubit","91c7e07697369d36e04e1e6f3320753a17dee95e01ecd38610ccffc05abec16d",1355,2,6,0,1),
    ("serdce-chuvstvuet","a7fd93f8181a962e8233f3e9c7a852f2e72defdb3301ef9586dba3442254de9d",2087,11,7,0,0),
    ("serdce-govorit","94bb9fcfa80fbaff55ac82a75fb5e908da1adb25e51d0f0f56eea41513e4e078",1255,3,3,0,0),
    ("serdce-sovest","7e46340bb1b4c397a2f1f81b8afe3864779fde8d54a0977a102558646464c095",1632,5,5,0,0),
    ("serdce-veruet","d0be28983ac95f0599276cbeef2f055c7ed80f1b1f8f92821fdf49f489f7cc8a",1384,6,6,0,0),
    ("hranit-serdce","a4f8c998ce00a1eae3043242f7b79aeda28e3e13c65c2316a533ea01419a2ad1",977,2,3,0,0),
    ("serdce-boga","33fdb1b6cdb8ca815116cbae8b8457b485abd62ffca3bb4b913f359e31a8f4a2",2018,6,6,0,1),
    ("karta-pisaniya","aecd3b43675b4d0f53f87a897be2f13d7a9bff205faa5fb5541610cd6d45c8e5",3411,93,0,0,0),
    ("tverdo-ne-dubinkoy","bae7f0945b05f6fd2ac882c6e4daf1ad56691c45179375cc47f1964ba29d371c",2161,0,2,0,0),
    ("vyhod","166a8d505766d7144f3ef1404097a0ed63856b617160a120f8f8c9e7604eb75a",1700,6,3,0,0),
]
EXCLUDED = {"padshee-serdce", "novoe-serdce", "istochniki"}
READER_HEADINGS = [
    "## Не только чувства", "## Внутренний человек перед Богом", "## Сердце, душа, дух и ум",
    "## Бог требует всего человека", "## Бог видит сердце", "## Сердце мыслит и истолковывает",
    "## Сердце решает и намеревается", "## Сердце любит и желает", "## Сердце чувствует",
    "## Сердце говорит и действует", "## Сердце и совесть", "## Сердце верует",
    "## Хранить сердце", "## Когда Писание говорит о сердце Бога", "## Как пользоваться определением",
    "## Границы главы", "## Для размышления", "## Переход",
]
REMAINING = {"HEART-BOOK-I3","HEART-BOOK-II","HEART-BOOK-III1","HEART-BOOK-III2","HEART-BOOK-III4","HEART-BOOK-IV","HEART-BOOK-V","HEART-BOOK-VI","HEART-BOOK-VII","HEART-BOOK-VIII","HEART-BOOK-IX"}
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


def blob(root: Path, path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=root, text=True).strip()


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def builder_module() -> Any:
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


def long_sentences(text: str, minimum: int = 120) -> set[str]:
    return {s.strip() for s in re.split(r"(?<=[.!?])\s+", normalize(text)) if len(s.strip()) >= minimum}


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
product_root = parser.parse_args().product_root.resolve()
product_file = product_root / PRODUCT_PATH
require(product_root.is_dir(), "exact Product checkout missing")
for path, expected in BLOBS.items():
    require(path.is_file(), f"immutable Research source missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(ROOT, path.relative_to(ROOT)) == expected, f"immutable Research blob drift: {path.relative_to(ROOT)}")
require(product_file.is_file(), "I.1 Product source missing")
if product_file.is_file():
    require(blob(product_root, PRODUCT_PATH) == PRODUCT_BLOB, "I.1 Product blob drift")

reader_text = READER.read_text(encoding="utf-8") if READER.is_file() else ""
product_text = product_file.read_text(encoding="utf-8") if product_file.is_file() else ""
require(sha(product_text) == PRODUCT_SHA, "I.1 Product full SHA drift")
require(reader_text.startswith("# I.1. Что Библия называет сердцем\n"), "I.1 reader title drift")
for heading in READER_HEADINGS:
    require(heading in reader_text, f"I.1 reader heading missing: {heading}")
for marker in (
    "HEART-I1-READER-ASSEMBLY-2026-08-04", "**Новые прямые цитаты:** `0`",
    "ASSEMBLED / PARAPHRASE-ONLY / ENTRY CITATION PASS OPEN", "I.1 READER ASSEMBLY = COMPLETE",
    "I.1 ENTRY CITATION PASS = OPEN", "ENTRY CITATION PASSES COMPLETE = 6 / 18",
    "ASSEMBLED READERS = 7 / 18", "MISSING STANDALONE FINAL READERS = 11",
    "WHOLE-BOOK READER ASSEMBLY = INCOMPLETE", "WHOLE-BOOK CITATION PASS = OPEN",
    "NEW DIRECT QUOTES = 0", "PRODUCT RELEASE = NOT CLAIMED",
):
    require(marker in reader_text, f"I.1 reader marker missing: {marker}")
for forbidden in ("I.1 ENTRY CITATION PASS = COMPLETE","ENTRY CITATION PASSES COMPLETE = 7 / 18","WHOLE-BOOK CITATION PASS = COMPLETE","PRODUCT RELEASE = COMPLETE"):
    require(forbidden not in reader_text, f"I.1 reader contains forbidden marker: {forbidden}")

builder = builder_module()
reader_scan = builder.scan_owner(builder.r(str(READER.relative_to(ROOT)), "assembled I.1 reader"), product_root) if builder is not None else {}
require(len(reader_scan.get("scriptureReferences", [])) == 20, f"I.1 reader Scripture count drift: {len(reader_scan.get('scriptureReferences', []))}")
for key in ("externalLinks", "internalArticleLinks"):
    require(reader_scan.get(key) == [], f"I.1 reader {key} must remain absent")
for key in ("footnoteDefinitions", "markdownBlockquotes", "htmlBlockquotes", "inlineQuotationSegments"):
    require(reader_scan.get(key) == 0, f"I.1 reader {key} must remain zero")
require(reader_scan.get("fullFileSha256") == "de692612cf07eefc374a7c30d5b5b9d16ad1704a78e69b3e7ee6589224067f2b", "I.1 reader SHA drift")
word_count = len(re.findall(r"[A-Za-zА-Яа-яЁё0-9-]+", reader_text))
require(1800 <= word_count <= 3000, f"I.1 reader word count outside boundary: {word_count}")

source_refs: set[str] = set()
source_quotes: list[str] = []
source_blocks: list[str] = []
source_internal: set[str] = set()
source_texts: list[str] = []
actual_manifest: list[list[Any]] = []
for section_id, expected_sha, expected_bytes, expected_refs, expected_quotes, expected_external, expected_internal in MANIFEST:
    scoped = builder.extract_sections(product_text, [section_id]) if builder is not None else ""
    refs = sorted({builder.normalize_ref(m.group(0)) for m in builder.SCRIPTURE_RE.finditer(scoped)}, key=str.casefold) if builder is not None else []
    external = sorted({builder.trim_url(m.group(0)) for m in builder.URL_RE.finditer(scoped)}, key=str.casefold) if builder is not None else []
    internal = sorted(set(builder.ARTICLE_LINK_RE.findall(scoped))) if builder is not None else []
    quotes = re.findall(r"«([^»\n]{8,})»", scoped) + re.findall(r"“([^”\n]{8,})”", scoped)
    blocks = [line.lstrip()[1:].strip() for line in scoped.splitlines() if re.match(r"^\s*>\s?\S", line)]
    require(bool(scoped.strip()), f"I.1 selected Product section missing: {section_id}")
    require(sha(scoped) == expected_sha, f"I.1 section SHA drift: {section_id}")
    require(len(scoped.encode("utf-8")) == expected_bytes, f"I.1 section byte drift: {section_id}")
    require(len(refs) == expected_refs, f"I.1 section reference count drift: {section_id}")
    require(len(quotes) + len(blocks) == expected_quotes, f"I.1 section quotation count drift: {section_id}")
    require(len(external) == expected_external, f"I.1 section external-link drift: {section_id}")
    require(len(internal) == expected_internal, f"I.1 section internal-link drift: {section_id}")
    source_refs.update(refs); source_quotes.extend(quotes); source_blocks.extend(blocks); source_internal.update(internal); source_texts.append(scoped)
    actual_manifest.append([section_id, expected_sha, expected_bytes, len(refs), len(quotes)+len(blocks), len(external), len(internal)])
require(len(source_refs) == 126, "I.1 selected aggregate Scripture count drift")
require(len(source_quotes) + len(source_blocks) == 80, "I.1 selected aggregate quotation count drift")
require(source_internal == {"/articles/skrytye-idoly-serdca/","/articles/serdce-hrista-k-nemoshchnym/"}, "I.1 selected internal-link set drift")
for section_id in EXCLUDED:
    require(bool(builder.extract_sections(product_text, [section_id]).strip()), f"I.1 excluded section missing: {section_id}")
reader_normalized = normalize(reader_text)
for quote in source_quotes:
    n = normalize(quote)
    if len(n) >= 40:
        require(n not in reader_normalized, f"I.1 reader copies Product quotation: {quote[:80]}")
for block in source_blocks:
    require(normalize(block) not in reader_normalized, f"I.1 reader copies Product blockquote: {block[:80]}")
require(long_sentences("\n".join(source_texts)).isdisjoint(long_sentences(reader_text)), "I.1 reader contains a long exact Product sentence")

full_scan = builder.scan_owner(builder.p(str(PRODUCT_PATH), "historical full I.1 owner"), product_root) if builder is not None else {}
require(len(full_scan.get("scriptureReferences", [])) == 142, "I.1 historical full reference count drift")
require(full_scan.get("inlineQuotationSegments", 0)+full_scan.get("markdownBlockquotes", 0)+full_scan.get("htmlBlockquotes", 0) == 98, "I.1 historical full quotation count drift")
require(len(full_scan.get("internalArticleLinks", [])) == 4, "I.1 historical full internal-link count drift")
require(full_scan.get("externalLinks") == [], "I.1 historical external links introduced")

integration = read_json(INTEGRATION)
require(integration.get("authorityId") == "HEART-WHOLE-BOOK-INTEGRATION-2026-08-04", "baseline integration authority drift")
current = read_json(CURRENT_V3)
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V3-2026-08-04", "preceding current V3 authority drift")
require(current.get("currentCounts", {}).get("entryCitationPassComplete") == 6, "preceding citation count drift")
require(current.get("currentCounts", {}).get("assembledReaderEntries") == 6, "preceding reader count drift")
require("HEART-BOOK-I1" in current.get("openEntryIds", []), "I.1 absent from preceding open set")
triage = read_json(TRIAGE)
rows = [row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-I1"]
require(len(rows) == 1, "historical I.1 triage row missing")
if rows:
    require(rows[0].get("inventoryEntrySha256") == "5acd1ed1ec0f50707a694332ae4ed56c274f31294d67956999f7eb7437f8250d", "I.1 inventory entry SHA drift")
    require(rows[0].get("detected") == {"ownerSurfaces":1,"sourceHeadings":0,"scriptureReferences":142,"externalLinks":0,"internalArticleLinks":4,"quotationSurfaces":98}, "I.1 historical counts drift")
    require(rows[0].get("disposition", {}).get("triageState") == "TRIAGED_OPEN", "historical I.1 triage rewritten")

assembly = read_json(ASSEMBLY)
require(assembly.get("authorityId") == "HEART-I1-READER-ASSEMBLY-2026-08-04", "I.1 assembly authority drift")
require(assembly.get("status") == "I1_FINAL_BOOK_READER_ASSEMBLED_PARAPHRASE_ONLY_ENTRY_CITATION_PASS_OPEN", "I.1 assembly status drift")
require(assembly.get("reader", {}).get("gitBlob") == BLOBS[READER], "I.1 assembly reader blob drift")
require(assembly.get("reader", {}).get("expectedDetectedScriptureReferences") == 20, "I.1 assembly reader reference expectation drift")
product = assembly.get("productSnapshot", {})
require(product.get("gitBlob") == PRODUCT_BLOB, "I.1 assembly Product blob drift")
require(product.get("selectedSectionManifest") == actual_manifest, "I.1 assembly manifest drift")
require(product.get("selectedAggregate") == {"sections":17,"bytes":34463,"uniqueScriptureReferences":126,"quotationSurfaces":80,"externalLinks":0,"internalArticleLinks":2}, "I.1 selected aggregate receipt drift")
require([row[0] for row in product.get("excludedSections", [])] == ["padshee-serdce","novoe-serdce","istochniki"], "I.1 excluded section receipt drift")
composition = assembly.get("composition", {})
for key in ("newHistoricalClaims","newDirectQuotesApproved","productQuotationSegmentsCopied","productLongSentencesCopied","productLinksCopied"):
    require(composition.get(key) == 0, f"I.1 composition boundary drift: {key}")
require(assembly.get("effectiveState") == {"entryId":"HEART-BOOK-I1","previous":"PRODUCT_SOURCE_ONLY","current":"ASSEMBLED_READER","entryCitationPassComplete":False}, "I.1 effective state drift")
require(assembly.get("effectiveCounts") == {"finalBookEntries":18,"assembledReader":7,"missingStandaloneFinalReaders":11,"entryCitationPassComplete":6,"entryCitationPassOpen":12,"assembledReaderCitationReviewsComplete":6,"productSourceOnly":5,"researchDossierOnly":6,"newDirectQuotesApproved":0}, "I.1 effective counts drift")
require(set(assembly.get("remainingReaderAssemblies", [])) == REMAINING, "I.1 remaining reader set drift")
boundary = assembly.get("publicationBoundary", {})
require(boundary.get("i1UnifiedReaderAssembled") is True and boundary.get("i1EntryCitationPassComplete") is False, "I.1 publication state drift")
require(boundary.get("wholeBookReaderAssemblyComplete") is False and boundary.get("wholeBookCitationPassComplete") is False, "I.1 falsely closes whole-book gates")
require(boundary.get("productReleaseComplete") is False and boundary.get("newDirectQuotesApproved") == 0, "I.1 release boundary drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-I1-READER-ASSEMBLY-2026-08-04", "I.1 READER ASSEMBLY = COMPLETE",
    "I.1 ENTRY CITATION PASS = OPEN", "ASSEMBLED READERS = 7 / 18",
    "MISSING STANDALONE FINAL READERS = 11", "ENTRY CITATION PASSES COMPLETE = 6 / 18",
    "SELECTED PRODUCT SCRIPTURE REFERENCES = 126", "SELECTED PRODUCT QUOTATION SURFACES = 80",
    "HISTORICAL FULL PRODUCT REFERENCES = 142", "HISTORICAL FULL PRODUCT QUOTATION SURFACES = 98",
    "READER DIRECT QUOTES = 0", "WHOLE-BOOK CITATION PASS = OPEN", BLOBS[READER], PRODUCT_BLOB,
):
    require(marker in human, f"I.1 human authority marker missing: {marker}")
for forbidden in ("I.1 ENTRY CITATION PASS = COMPLETE","ENTRY CITATION PASSES COMPLETE = 7 / 18","WHOLE-BOOK CITATION PASS = COMPLETE","PRODUCT RELEASE = COMPLETE","TODO","TBD"):
    require(forbidden not in human, f"I.1 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart I.1 reader assembly: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Heart I.1 reader assembly: PASS — {word_count} words, reader 20/0/0, selected 17 sections 126/80/2, historical 142/98/4, readers 7/18, citation 6/18")
