#!/usr/bin/env python3
"""Validate the paraphrase-only I.4 final-book reader assembly."""
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
ASSEMBLY = ROOT / "data/heart-i4-reader-assembly-2026-08-04.json"
OWNER = ROOT / "data/heart-i4-owner-closure-2026-08-04.json"
CURRENT_V2 = ROOT / "data/heart-entry-citation-pass-current-v2-2026-08-04.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/101_READER_CHAPTER_I4_INNER_PERSON_EMBODIED_LIFE_2026-08-04.md"
V81 = ROOT / "СЕРИЯ СЕРДЦЕ/60_V81_JAY_ADAMS_PRIMARY_SOURCE_DEEPENING.md"
V82 = ROOT / "СЕРИЯ СЕРДЦЕ/61_V82_PSYCHOTROPIC_MEDICATION_BODY_SOUL_BIBLICAL_COUNSELING.md"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/102_I4_READER_ASSEMBLY_2026-08-04.md"
PRIMARY_PATH = Path("src/content/articles/serdce-i-telo.mdx")
SUPPORT_PATH = Path("src/content/articles/chto-bibliya-nazyvaet-serdcem.mdx")

BLOBS = {
    OWNER: "5a7aa3ef29571255708c49692a6232177b7bcf14",
    CURRENT_V2: "66d2f46cf639d9825b5b09fc4e94111be3af2a11",
    READER: "d683ed3f1e8d699f0232f9ee7a30dc0fa2400d74",
    V81: "f5b3491acad2e6a68197d6c1191ea3b9fb74aa75",
    V82: "d62d76abe607335861745cc732a9aad8edc3b743",
}
PRODUCT_BLOBS = {
    PRIMARY_PATH: "dca5863c614cf3a4f8503d52a79bb76e705c9d2c",
    SUPPORT_PATH: "acc12804f5b2450efebbb6e0b2cabd31066ef48c",
}
PRODUCT_FULL_SHA = {
    PRIMARY_PATH: "79a1ce46206e504d082d0af9094bd308afc6abe3163d432099263ca5229c3ec2",
    SUPPORT_PATH: "50657f3473c06e16d75ffe740828a9311f642562e824f148113ae28ff9b03c07",
}
PRIMARY_MANIFEST = [
    ("telo-ne-vrag", "829781f61eb45cc6ab9b944fb714fb20e59064a6047408a193fd605f43c36bb4", 2546, 1, 3, 0, []),
    ("chleny-oruzhie", "89f3fb186c98c0fa48e8f36784bb92816a9530ec570a2a7c982c3f47af76ab07", 2234, 3, 6, 0, ["/articles/starye-dorozhki-serdca/"]),
    ("hram-kuplennyj", "db012a80d9b42f70d2d2759acc77790e6e3c735b77dae659427eab7afacb2dd2", 1903, 1, 5, 0, []),
    ("zhivaya-zhertva", "0d9f0cee0b2ded2445f8f9374ed55147915eefb623072af4d831cf7b2cc27c41", 1880, 1, 7, 0, []),
    ("komfort-gospodin", "cd9609ec4a0f8588716141025147adead8c97ebe57d084ded0148679abaaa4c0", 1928, 0, 6, 0, ["/articles/skrytye-idoly-serdca/"]),
    ("ustalost", "a29a2ab752e30f47d60505525d8f99957ac64ef57eb2cd359fd01643b43c9dba", 2075, 0, 5, 0, []),
    ("ne-hlebom-odnim", "18016ebca67607fa7359bbfa5b280d8a4f627d14af3ea57fbd106fcecf6c7b87", 1424, 2, 3, 0, ["/articles/serdce-i-iskushenie/"]),
    ("tverdo-ne-dubinkoy", "b66b4e79b62b305096dd0a72d5b494442de1b4ee0d81b65c75b240ffd6fabdb5", 2134, 0, 5, 0, []),
    ("kak-otlichit", "919646023c3622cfa980f2b164115adaf8240a095b31bbdac2ee17d21fcc627a", 1223, 0, 0, 0, []),
    ("vyhod", "6b49facc0c618d7f9f648dd0fc39a2401fd36fc718e3d748e2960f537e445577", 1527, 0, 3, 0, []),
]
SUPPORT_MANIFEST = [
    ("vnutrenniy-chelovek", "d6ffdf64d0b46b23cee96f4943f76ed20be117c531efdc6ca30bae199737c0b8", 3115, 1, 3, 0, []),
    ("serdce-dusha-duh", "0cc608846137d909c8e5a3cd391c5b71b8d23a27e60d60d68658865382f2c33d", 5035, 5, 7, 0, []),
]
READER_HEADINGS = [
    "## Один человек перед Богом",
    "## Тело не враг и не господин",
    "## Внутренний человек действует через члены",
    "## Привычка как выученная телесная дорожка",
    "## Тело принадлежит Христу",
    "## Комфорт, аппетит и скрытое господство",
    "## Усталость требует двойной оценки",
    "## Медицинская компетенция и пастырская граница",
    "## Практика нового пути",
    "## Границы главы",
    "## Для размышления",
    "## Переход",
]
EXPECTED_REMAINING = {
    "HEART-BOOK-I1", "HEART-BOOK-I3", "HEART-BOOK-II", "HEART-BOOK-III1",
    "HEART-BOOK-III2", "HEART-BOOK-III4", "HEART-BOOK-IV", "HEART-BOOK-V",
    "HEART-BOOK-VI", "HEART-BOOK-VII", "HEART-BOOK-VIII", "HEART-BOOK-IX",
}
V81_MARKERS = (
    "Сердце — целостный внутренний человек",
    "Остаточный грех как склонность и привычный принцип",
    "Четыре свойства укоренившейся привычки",
    "исторически описанной позицией автора",
)
V82_MARKERS = (
    "Редукционизм 1 — человек есть только тело",
    "Редукционизм 2 — тело почти не имеет значения",
    "Писание обладает верховной, непогрешимой и достаточной властью",
    "не назначает, не отменяет и не меняет дозировку",
)
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


def long_sentences(text: str, minimum: int = 120) -> set[str]:
    return {
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", normalize(text))
        if len(sentence.strip()) >= minimum
    }


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
product_root = parser.parse_args().product_root.resolve()
require(product_root.is_dir(), "exact Product checkout missing")

for path, expected_blob in BLOBS.items():
    require(path.is_file(), f"immutable Research source missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(git_blob(ROOT, path.relative_to(ROOT)) == expected_blob, f"immutable Research blob drift: {path.relative_to(ROOT)}")
for path, expected_blob in PRODUCT_BLOBS.items():
    full = product_root / path
    require(full.is_file(), f"immutable Product source missing: {path}")
    if full.is_file():
        require(git_blob(product_root, path) == expected_blob, f"immutable Product blob drift: {path}")

reader_text = READER.read_text(encoding="utf-8") if READER.is_file() else ""
v81_text = V81.read_text(encoding="utf-8") if V81.is_file() else ""
v82_text = V82.read_text(encoding="utf-8") if V82.is_file() else ""
require(reader_text.startswith("# I.4. Внутренний человек и телесная жизнь\n"), "I.4 reader title drift")
for heading in READER_HEADINGS:
    require(heading in reader_text, f"I.4 reader heading missing: {heading}")
for marker in (
    "HEART-I4-READER-ASSEMBLY-2026-08-04",
    "**Новые прямые цитаты:** `0`",
    "ASSEMBLED / PARAPHRASE-ONLY / ENTRY CITATION PASS OPEN",
    "I.4 READER ASSEMBLY = COMPLETE",
    "I.4 ENTRY CITATION PASS = OPEN",
    "WHOLE-BOOK ENTRY CITATION PASSES = 5 / 18",
    "ASSEMBLED READERS = 6 / 18",
    "MISSING STANDALONE FINAL READERS = 12",
    "WHOLE-BOOK READER ASSEMBLY = INCOMPLETE",
    "WHOLE-BOOK CITATION PASS = OPEN",
    "NEW DIRECT QUOTES = 0",
    "PRODUCT RELEASE = NOT CLAIMED",
):
    require(marker in reader_text, f"I.4 reader boundary marker missing: {marker}")
for forbidden in (
    "I.4 ENTRY CITATION PASS = COMPLETE",
    "WHOLE-BOOK ENTRY CITATION PASSES = 6 / 18",
    "WHOLE-BOOK READER ASSEMBLY = COMPLETE",
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "NEW DIRECT QUOTES = 1",
    "PRODUCT RELEASE = COMPLETE",
):
    require(forbidden not in reader_text, f"I.4 reader contains forbidden marker: {forbidden}")
for marker in V81_MARKERS:
    require(marker in v81_text, f"V81 boundary marker missing: {marker}")
for marker in V82_MARKERS:
    require(marker in v82_text, f"V82 boundary marker missing: {marker}")

builder = import_builder()
reader_scan: dict[str, Any] = {}
if builder is not None:
    reader_scan = builder.scan_owner(builder.r(str(READER.relative_to(ROOT)), "assembled I.4 reader"), product_root)
require(len(reader_scan.get("scriptureReferences", [])) == 9, f"I.4 reader Scripture count drift: {len(reader_scan.get('scriptureReferences', []))}")
require(reader_scan.get("externalLinks") == [], "I.4 reader external links must remain absent")
require(reader_scan.get("internalArticleLinks") == [], "I.4 reader internal links must remain absent")
require(reader_scan.get("footnoteDefinitions") == 0, "I.4 reader footnotes must remain absent")
require(reader_scan.get("markdownBlockquotes") == 0, "I.4 reader Markdown blockquotes must remain absent")
require(reader_scan.get("htmlBlockquotes") == 0, "I.4 reader HTML blockquotes must remain absent")
require(reader_scan.get("inlineQuotationSegments") == 0, "I.4 reader quotation surfaces must remain zero")
word_count = len(re.findall(r"[A-Za-zА-Яа-яЁё0-9-]+", reader_text))
require(1400 <= word_count <= 2300, f"I.4 reader word count outside boundary: {word_count}")

source_texts: list[str] = []
combined_refs: set[str] = set()
combined_quotes: list[str] = []
combined_blocks: list[str] = []
combined_external: set[str] = set()
combined_internal: set[str] = set()
actual_manifests: dict[str, list[list[Any]]] = {"primary": [], "support": []}
for lane, path, manifest in (
    ("primary", PRIMARY_PATH, PRIMARY_MANIFEST),
    ("support", SUPPORT_PATH, SUPPORT_MANIFEST),
):
    text = (product_root / path).read_text(encoding="utf-8")
    require(sha256_text(text) == PRODUCT_FULL_SHA[path], f"Product full SHA drift: {path}")
    lane_refs: set[str] = set()
    lane_quotes = 0
    lane_blocks = 0
    lane_external: set[str] = set()
    lane_internal: set[str] = set()
    for section_id, expected_sha, expected_bytes, expected_ref_count, expected_inline, expected_blocks, expected_internal in manifest:
        scoped = builder.extract_sections(text, [section_id]) if builder is not None else ""
        refs = sorted({builder.normalize_ref(m.group(0)) for m in builder.SCRIPTURE_RE.finditer(scoped)}, key=str.casefold) if builder is not None else []
        external = sorted({builder.trim_url(m.group(0)) for m in builder.URL_RE.finditer(scoped)}, key=str.casefold) if builder is not None else []
        internal = sorted(set(builder.ARTICLE_LINK_RE.findall(scoped))) if builder is not None else []
        inline = re.findall(r"«([^»\n]{8,})»", scoped) + re.findall(r"“([^”\n]{8,})”", scoped)
        blocks = [line.lstrip()[1:].strip() for line in scoped.splitlines() if re.match(r"^\s*>\s?\S", line)]
        require(bool(scoped.strip()), f"Product section missing: {path}#{section_id}")
        require(sha256_text(scoped) == expected_sha, f"Product section SHA drift: {path}#{section_id}")
        require(len(scoped.encode("utf-8")) == expected_bytes, f"Product section byte drift: {path}#{section_id}")
        require(len(refs) == expected_ref_count, f"Product section Scripture count drift: {path}#{section_id}")
        require(len(inline) == expected_inline, f"Product section inline quote drift: {path}#{section_id}")
        require(len(blocks) == expected_blocks, f"Product section blockquote drift: {path}#{section_id}")
        require(external == [], f"Product external links introduced: {path}#{section_id}")
        require(internal == expected_internal, f"Product internal-link drift: {path}#{section_id}")
        lane_refs.update(refs)
        lane_quotes += len(inline)
        lane_blocks += len(blocks)
        lane_external.update(external)
        lane_internal.update(internal)
        combined_refs.update(refs)
        combined_quotes.extend(inline)
        combined_blocks.extend(blocks)
        combined_external.update(external)
        combined_internal.update(internal)
        source_texts.append(scoped)
        actual_manifests[lane].append([section_id, expected_sha, expected_bytes, len(refs), len(inline), len(blocks), len(internal)])
    expected_lane = (8, 43, 0, 3) if lane == "primary" else (6, 10, 0, 0)
    require(len(lane_refs) == expected_lane[0], f"{lane} aggregate Scripture count drift")
    require(lane_quotes + lane_blocks == expected_lane[1], f"{lane} aggregate quotation count drift")
    require(len(lane_external) == expected_lane[2], f"{lane} aggregate external-link drift")
    require(len(lane_internal) == expected_lane[3], f"{lane} aggregate internal-link drift")
require(len(combined_refs) == 14, "I.4 Product combined Scripture count drift")
require(len(combined_quotes) + len(combined_blocks) == 53, "I.4 Product combined quotation count drift")
require(combined_external == set(), "I.4 Product combined external-link drift")
require(combined_internal == {
    "/articles/starye-dorozhki-serdca/",
    "/articles/skrytye-idoly-serdca/",
    "/articles/serdce-i-iskushenie/",
}, "I.4 Product combined internal-link set drift")
reader_normalized = normalize(reader_text)
for quote in combined_quotes:
    normalized = normalize(quote)
    if len(normalized) >= 40:
        require(normalized not in reader_normalized, f"I.4 reader copies Product quote: {quote[:80]}")
for block in combined_blocks:
    require(normalize(block) not in reader_normalized, f"I.4 reader copies Product blockquote: {block[:80]}")
require(long_sentences("\n".join(source_texts)).isdisjoint(long_sentences(reader_text)), "I.4 reader contains a long exact Product sentence")
require(long_sentences(v81_text).isdisjoint(long_sentences(reader_text)), "I.4 reader contains a long exact V81 sentence")
require(long_sentences(v82_text).isdisjoint(long_sentences(reader_text)), "I.4 reader contains a long exact V82 sentence")

owner = read_json(OWNER)
require(owner.get("authorityId") == "HEART-I4-OWNER-CLOSURE-2026-08-04", "I.4 owner authority drift")
require(owner.get("status") == "I4_PRODUCT_SOURCE_CLUSTER_ESTABLISHED_UNIFIED_READER_AND_BOOK_CITATION_PASS_OPEN", "I.4 owner status drift")
override = owner.get("entryOverride", {})
require(override.get("id") == "HEART-BOOK-I4", "I.4 owner entry ID drift")
require(override.get("effectivePrimaryState") == "PRODUCT_SOURCE_ONLY", "I.4 historical primary state drift")
require(override.get("manuscriptState") == "SOURCE_CLUSTER_SELECTED_UNIFIED_READER_NOT_ASSEMBLED", "I.4 historical manuscript state drift")
require(owner.get("publicationBoundary", {}).get("i4UnifiedReaderAssembled") is False, "historical I.4 owner receipt rewritten")
require(owner.get("publicationBoundary", {}).get("newDirectQuotesApproved") == 0, "I.4 owner direct-quote boundary drift")

current = read_json(CURRENT_V2)
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V2-2026-08-04", "preceding current V2 authority drift")
require(current.get("currentCounts", {}).get("entryCitationPassComplete") == 5, "preceding citation count drift")
require(current.get("currentCounts", {}).get("assembledReaderEntries") == 5, "preceding reader count drift")
require(current.get("currentCounts", {}).get("missingStandaloneFinalReaders") == 13, "preceding reader backlog drift")
require("HEART-BOOK-I4" in current.get("openEntryIds", []), "I.4 missing from preceding open set")

assembly = read_json(ASSEMBLY)
require(assembly.get("authorityId") == "HEART-I4-READER-ASSEMBLY-2026-08-04", "I.4 assembly authority drift")
require(assembly.get("status") == "I4_FINAL_BOOK_READER_ASSEMBLED_PARAPHRASE_ONLY_ENTRY_CITATION_PASS_OPEN", "I.4 assembly status drift")
immutable = assembly.get("immutableAuthorities", {})
require(immutable.get("ownerClosure", [None, None])[1] == BLOBS[OWNER], "I.4 assembly owner blob drift")
require(immutable.get("precedingCurrentV2", [None, None])[1] == BLOBS[CURRENT_V2], "I.4 assembly current V2 blob drift")
require(immutable.get("v81", [None, None])[1] == BLOBS[V81], "I.4 assembly V81 blob drift")
require(immutable.get("v82", [None, None])[1] == BLOBS[V82], "I.4 assembly V82 blob drift")
reader_receipt = assembly.get("reader", {})
require(reader_receipt.get("gitBlob") == BLOBS[READER], "I.4 assembly reader blob drift")
require(reader_receipt.get("expectedDetectedScriptureReferences") == 9, "I.4 assembly reader Scripture expectation drift")
require(reader_receipt.get("quotationSurfaces") == 0, "I.4 assembly reader quote expectation drift")
product = assembly.get("productSnapshot", {})
require(product.get("commit") == "0fbe7d1ead9ebd1bea867418e254da438ec63329", "I.4 assembly Product commit drift")
require(product.get("primary", {}).get("gitBlob") == PRODUCT_BLOBS[PRIMARY_PATH], "I.4 assembly primary Product blob drift")
require(product.get("support", {}).get("gitBlob") == PRODUCT_BLOBS[SUPPORT_PATH], "I.4 assembly support Product blob drift")
require(product.get("primary", {}).get("sectionManifest") == actual_manifests["primary"], "I.4 primary manifest drift")
require(product.get("support", {}).get("sectionManifest") == actual_manifests["support"], "I.4 support manifest drift")
require(product.get("combinedAggregate") == {"uniqueScriptureReferences":14,"quotationSurfaces":53,"externalLinks":0,"internalArticleLinks":3}, "I.4 combined aggregate drift")
composition = assembly.get("composition", {})
for key in ("newHistoricalClaims", "newDirectQuotesApproved", "productQuotationSegmentsCopied", "productLongSentencesCopied", "researchQuotationSegmentsCopied"):
    require(composition.get(key) == 0, f"I.4 composition boundary drift: {key}")
require(composition.get("mode") == "PARAPHRASE_ONLY", "I.4 composition mode drift")
state = assembly.get("effectiveState", {})
require(state == {"entryId":"HEART-BOOK-I4","previous":"PRODUCT_SOURCE_ONLY","current":"ASSEMBLED_READER","entryCitationPassComplete":False}, "I.4 effective state drift")
require(assembly.get("effectiveCounts") == {
    "finalBookEntries":18,
    "assembledReader":6,
    "missingStandaloneFinalReaders":12,
    "entryCitationPassComplete":5,
    "entryCitationPassOpen":13,
    "assembledReaderCitationReviewsComplete":5,
    "productSourceOnly":6,
    "researchDossierOnly":6,
    "newDirectQuotesApproved":0,
}, "I.4 effective count drift")
require(set(assembly.get("remainingReaderAssemblies", [])) == EXPECTED_REMAINING, "I.4 remaining reader set drift")
boundary = assembly.get("publicationBoundary", {})
require(boundary.get("i4UnifiedReaderAssembled") is True, "I.4 reader assembly not complete")
require(boundary.get("i4EntryCitationPassComplete") is False, "I.4 citation pass falsely complete")
require(boundary.get("allCurrentlyAssembledReadersCitationReviewed") is False, "six-reader review state falsely closed")
require(boundary.get("wholeBookReaderAssemblyComplete") is False, "whole-book reader assembly falsely closed")
require(boundary.get("wholeBookCitationPassComplete") is False, "whole-book citation pass falsely closed")
require(boundary.get("productReleaseComplete") is False, "Product release falsely closed")
require(boundary.get("newDirectQuotesApproved") == 0, "I.4 publication direct-quote drift")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-I4-READER-ASSEMBLY-2026-08-04",
    "I.4 READER ASSEMBLY = COMPLETE",
    "I.4 ENTRY CITATION PASS = OPEN",
    "ASSEMBLED READERS = 6 / 18",
    "MISSING STANDALONE FINAL READERS = 12",
    "ENTRY CITATION PASSES COMPLETE = 5 / 18",
    "PRODUCT SOURCE QUOTATION SURFACES TRANSFERRED = 0",
    "READER DIRECT QUOTES = 0",
    "WHOLE-BOOK READER ASSEMBLY = INCOMPLETE",
    "WHOLE-BOOK CITATION PASS = OPEN",
    BLOBS[READER],
    PRODUCT_BLOBS[PRIMARY_PATH],
    PRODUCT_BLOBS[SUPPORT_PATH],
):
    require(marker in human, f"I.4 human authority marker missing: {marker}")
for forbidden in (
    "I.4 ENTRY CITATION PASS = COMPLETE",
    "ENTRY CITATION PASSES COMPLETE = 6 / 18",
    "WHOLE-BOOK READER ASSEMBLY = COMPLETE",
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"I.4 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart I.4 reader assembly: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "Heart I.4 reader assembly: PASS — "
    f"{word_count} words, 9 reader locators, 0 quote/link surfaces, "
    "12 Product sections pinned, 6 assembled readers, 12 remaining, citation passes 5/18"
)
