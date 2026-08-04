#!/usr/bin/env python3
"""Validate the bounded Heart whole-book owner and citation integration manifest."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/heart-whole-book-integration-2026-08-04.json"
READER = ROOT / "data/heart-reader-assembly-2026-08-02.json"
P0 = ROOT / "data/heart-p0-architecture-dossiers-2026-08-02.json"
R1R9 = ROOT / "СЕРИЯ СЕРДЦЕ/74_SOURCE_CLOSURE_REGISTRY_2026-08-01.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/83_WHOLE_BOOK_INTEGRATION_MANIFEST_2026-08-04.md"
CURRENT = ROOT / "СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-04.md"
PREVIOUS = ROOT / "СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-02.md"

EXPECTED_RESEARCH_SNAPSHOT = "bd0a0809f6cae37a8650333930020fa53153f2d1"
EXPECTED_PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"
EXPECTED_PRODUCT_BLOB = "553adbd67a459fa9e022f00b924e8c20201bf400"
EXPECTED_PRODUCT_PATH = "src/components/article-pilots/_shared/heartSeriesData.ts"
EXPECTED_PRODUCT_ITEMS = [
    ("prolog", "chto-bibliya-nazyvaet-serdcem"),
    ("krajne", "krajne-li-isporcheno-serdce"),
    ("rimlyanam", "rimlyanam-7-veruyushchiy-ili-neveruyushchiy"),
    ("novoe", "novoe-serdce"),
    ("serdce-duh", "serdce-i-duh"),
    ("spravochnik", "serdce-spravochnik"),
]
EXPECTED_LABELS = [
    "I.1 Что Библия называет сердцем",
    "I.2 Сердце в Эдеме",
    "I.3 Падшее сердце: Иеремия 17",
    "I.4 Внутренний человек и телесная жизнь",
    "II Диагноз падшего сердца",
    "III.1 Обещание нового сердца",
    "III.2 Рождение свыше и обновление",
    "III.3 Сокрушённое сердце: покаяние",
    "III.4 Сердце и Дух",
    "IV Сердце и слово Божие",
    "V Сердце в борьбе с грехом",
    "VI Сердце ученика и фарисея",
    "VII Сердце в страдании и унынии",
    "VIII Взирая на славу Христа",
    "IX Христос Апокалипсиса и сердце",
    "X.1 Суд сердца: два воскресения",
    "X.2 Освобождённое сердце",
    "X.3 Заключительная надежда",
]
EXPECTED_STATE_COUNTS = {
    "ASSEMBLED_READER": 3,
    "PRODUCT_SOURCE_ONLY": 5,
    "RESEARCH_DOSSIER_ONLY": 6,
    "OWNER_REQUIRED": 4,
}
EXPECTED_CITATION_COUNTS = {
    "P0_READER_BOUNDARIES_VALIDATED": 3,
    "PRODUCT_SOURCE_CITATION_PASS_REQUIRED": 5,
    "R_DOSSIER_BOUNDARIES_AVAILABLE_MANUSCRIPT_REQUIRED": 6,
    "OWNER_AND_CITATION_PASS_REQUIRED": 4,
}
EXPECTED_READER_PATHS = {
    "HEART-BOOK-I2": "СЕРИЯ СЕРДЦЕ/79_READER_CHAPTER_I2_HEART_IN_EDEN_2026-08-02.md",
    "HEART-BOOK-III3": "СЕРИЯ СЕРДЦЕ/80_READER_CHAPTER_III3_BROKEN_HEART_REPENTANCE_2026-08-02.md",
    "HEART-BOOK-X1": "СЕРИЯ СЕРДЦЕ/81_READER_CHAPTER_X1_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md",
}

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)}: root object required")
        return {}
    return value


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return ""


def run_git(repo: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        errors.append(f"git -C {repo} {' '.join(args)} failed: {exc}")
        return ""
    return result.stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--product-root", type=Path, required=True)
    return parser.parse_args()


args = parse_args()
product_root = args.product_root.resolve()
manifest = load(MANIFEST)
reader = load(READER)
p0 = load(P0)
r1r9 = load(R1R9)

require(manifest.get("schemaVersion") == 1, "integration schema drift")
require(manifest.get("authorityId") == "HEART-WHOLE-BOOK-INTEGRATION-2026-08-04", "integration authority drift")
require(manifest.get("status") == "EIGHTEEN_ENTRY_MAPPING_COMPLETE_MANUSCRIPT_AND_CITATION_PASSES_OPEN", "integration status drift")
require(manifest.get("generatedAt") == "2026-08-04", "integration generated date drift")
require(manifest.get("lastVerifiedAt") == "2026-08-04", "integration verification date drift")
require(manifest.get("researchSnapshot") == EXPECTED_RESEARCH_SNAPSHOT, "Research snapshot drift")
require(manifest.get("readerAssemblyAuthority") == "data/heart-reader-assembly-2026-08-02.json", "reader authority pointer drift")
require(manifest.get("p0EvidenceAuthority") == "data/heart-p0-architecture-dossiers-2026-08-02.json", "P0 authority pointer drift")
require(manifest.get("r1r9SourceAuthority") == "СЕРИЯ СЕРДЦЕ/74_SOURCE_CLOSURE_REGISTRY_2026-08-01.json", "R1-R9 authority pointer drift")

require(reader.get("authorityId") == "HEART-READER-ASSEMBLY-2026-08-02", "reader assembly authority missing")
require(reader.get("newDirectQuotesApproved") == 0, "reader direct-quote boundary drift")
require(p0.get("authorityId") == "HEART-P0-ARCHITECTURE-CLOSURE-2026-08-02", "P0 authority missing")
require(p0.get("counts", {}).get("claims") == 26, "P0 claim count drift")
require(r1r9.get("counts") == {
    "unique_sources": 85,
    "trusted_sources": 81,
    "claims": 18,
    "quote_safe_claims": 9,
    "non_quote_claims": 9,
}, "R1-R9 source closure counts drift")

entries = manifest.get("entries")
require(isinstance(entries, list) and len(entries) == 18, "exactly eighteen integration entries required")
entries = entries if isinstance(entries, list) else []
require([row.get("order") for row in entries if isinstance(row, dict)] == list(range(1, 19)), "integration order must be 1..18")
require([row.get("bookLabel") for row in entries if isinstance(row, dict)] == EXPECTED_LABELS, "integration labels/order drift")
require(reader.get("finalBookOrder") == EXPECTED_LABELS, "reader authority and integration final order diverged")

ids: list[str] = []
states: Counter[str] = Counter()
citations: Counter[str] = Counter()
product_ids: list[str] = []
for row in entries:
    require(isinstance(row, dict), "integration entry object required")
    if not isinstance(row, dict):
        continue
    entry_id = str(row.get("id", ""))
    ids.append(entry_id)
    require(re.fullmatch(r"HEART-BOOK-(?:I1|I2|I3|I4|II|III1|III2|III3|III4|IV|V|VI|VII|VIII|IX|X1|X2|X3)", entry_id) is not None, f"{entry_id}: invalid integration ID")
    state = str(row.get("primaryState", ""))
    citation = str(row.get("citationState", ""))
    states[state] += 1
    citations[citation] += 1
    require(state in EXPECTED_STATE_COUNTS, f"{entry_id}: invalid primary state {state}")
    require(citation in EXPECTED_CITATION_COUNTS, f"{entry_id}: invalid citation state {citation}")
    require(len(str(row.get("dedupOwner", ""))) >= 80, f"{entry_id}: dedup owner too weak")

    product = row.get("productOwner")
    owners = row.get("researchOwners")
    require(isinstance(owners, list), f"{entry_id}: researchOwners array required")
    owners = owners if isinstance(owners, list) else []
    for owner in owners:
        require(isinstance(owner, str) and (ROOT / owner).is_file(), f"{entry_id}: missing Research owner {owner}")

    if state == "ASSEMBLED_READER":
        require(product is None, f"{entry_id}: assembled P0 reader must not invent Product owner")
        expected_reader = EXPECTED_READER_PATHS.get(entry_id)
        require(expected_reader is not None and expected_reader in owners, f"{entry_id}: expected reader owner missing")
        require(citation == "P0_READER_BOUNDARIES_VALIDATED", f"{entry_id}: assembled reader citation state drift")
    elif state == "PRODUCT_SOURCE_ONLY":
        require(isinstance(product, dict), f"{entry_id}: Product owner required")
        if isinstance(product, dict):
            product_ids.append(str(product.get("id", "")))
            require((str(product.get("id", "")), str(product.get("slug", ""))) in EXPECTED_PRODUCT_ITEMS, f"{entry_id}: non-canonical Product owner")
        require(citation == "PRODUCT_SOURCE_CITATION_PASS_REQUIRED", f"{entry_id}: Product citation pass must remain open")
    elif state == "RESEARCH_DOSSIER_ONLY":
        require(product is None, f"{entry_id}: dossier-only entry must not claim Product owner")
        require(bool(owners), f"{entry_id}: dossier-only entry requires Research owner")
        require(citation == "R_DOSSIER_BOUNDARIES_AVAILABLE_MANUSCRIPT_REQUIRED", f"{entry_id}: dossier-only citation state drift")
    elif state == "OWNER_REQUIRED":
        require(product is None, f"{entry_id}: owner-required entry must not claim Product owner")
        require(owners == [], f"{entry_id}: owner-required entry must not hide an owner in researchOwners")
        require(citation == "OWNER_AND_CITATION_PASS_REQUIRED", f"{entry_id}: owner-required citation state drift")

require(len(ids) == len(set(ids)) == 18, "integration IDs must be unique")
require(dict(states) == EXPECTED_STATE_COUNTS, f"primary-state counts drift: {dict(states)}")
require(dict(citations) == EXPECTED_CITATION_COUNTS, f"citation-state counts drift: {dict(citations)}")
require(product_ids == ["prolog", "krajne", "novoe", "serdce-duh", "rimlyanam"], "book-matched Product owner order drift")

product = manifest.get("productSnapshot", {})
require(product.get("repository") == "FedorMilovanov/gb-is-my-strength", "Product repository drift")
require(product.get("commit") == EXPECTED_PRODUCT_COMMIT, "Product commit drift")
require(product.get("path") == EXPECTED_PRODUCT_PATH, "Product path drift")
require(product.get("blobSha") == EXPECTED_PRODUCT_BLOB, "Product blob drift")
require([(row.get("id"), row.get("slug")) for row in product.get("currentCoreItems", []) if isinstance(row, dict)] == EXPECTED_PRODUCT_ITEMS, "Product snapshot item registry drift")
require(product.get("bookMatchedCoreItems") == 5, "Product matched core count drift")
require(product.get("outsideFinalBookOrder") == ["spravochnik"], "Product outside-book set drift")

require(product_root.is_dir(), f"Product checkout missing: {product_root}")
product_head = run_git(product_root, "rev-parse", "HEAD")
require(product_head == EXPECTED_PRODUCT_COMMIT, f"Product checkout head drift: {product_head}")
product_file = product_root / EXPECTED_PRODUCT_PATH
require(product_file.is_file(), "Product heartSeriesData.ts missing")
product_blob = run_git(product_root, "hash-object", EXPECTED_PRODUCT_PATH)
require(product_blob == EXPECTED_PRODUCT_BLOB, f"Product heartSeriesData blob drift: {product_blob}")
product_text = product_file.read_text(encoding="utf-8") if product_file.is_file() else ""
parsed_items = re.findall(r"\{\s*id:\s*'([^']+)',\s*slug:\s*'([^']+)'", product_text)
require(parsed_items == EXPECTED_PRODUCT_ITEMS, f"Product core item parse drift: {parsed_items}")
require("export const HEART_SERIES_ITEMS" in product_text, "Product series owner export missing")

boundary = manifest.get("integrationBoundary", {})
require(boundary == {
    "finalOrderMapped": True,
    "productSnapshotVerified": True,
    "readerOwnersMapped": True,
    "r1r9EvidenceOwnersMapped": True,
    "standaloneOwnerGapsEnumerated": True,
    "wholeBookLineEditComplete": False,
    "wholeBookCitationPassComplete": False,
    "manuscriptBundleComplete": False,
    "productReleaseComplete": False,
    "newDirectQuotesApproved": 0,
}, "integration boundary drift")
require(manifest.get("counts") == {
    "finalBookEntries": 18,
    "assembledReader": 3,
    "productSourceOnly": 5,
    "researchDossierOnly": 6,
    "ownerRequired": 4,
    "currentProductCoreItems": 6,
    "bookMatchedProductCoreItems": 5,
    "newDirectQuotesApproved": 0,
}, "integration counts drift")

human = read(HUMAN)
for marker in (
    "HEART-WHOLE-BOOK-INTEGRATION-2026-08-04",
    "18-ENTRY OWNER MAPPING = COMPLETE",
    "ASSEMBLED READER OWNERS = 3",
    "PRODUCT SOURCE OWNERS = 5",
    "RESEARCH DOSSIER OWNERS = 6",
    "STANDALONE OWNER GAPS = 4",
    "WHOLE-BOOK CITATION PASS = OPEN",
    "PRODUCT RELEASE = NOT CLAIMED",
    EXPECTED_PRODUCT_COMMIT,
    EXPECTED_PRODUCT_BLOB,
):
    require(marker in human, f"human integration authority marker missing: {marker}")

current = read(CURRENT)
for marker in (
    "HEART-CURRENT-AUTHORITY-2026-08-04",
    "THREE P0 READER CHAPTERS = ASSEMBLED",
    "R9 ROLE = CLOSED",
    "FINAL ORDER = CLOSED",
    "18-ENTRY OWNER MAPPING = COMPLETE",
    "WHOLE-BOOK LINE EDIT = OPEN",
    "WHOLE-BOOK CITATION PASS = OPEN",
    "PRODUCT RELEASE = NOT CLAIMED",
):
    require(marker in current, f"current authority marker missing: {marker}")

previous = read(PREVIOUS)
require("SUPERSEDED FOR CURRENT STATUS BY" in previous, "previous current authority lacks supersession marker")
require("00_CURRENT_AUTHORITY_2026-08-04.md" in previous, "previous authority successor pointer missing")

for path, text in ((HUMAN, human), (CURRENT, current)):
    for forbidden in ("TODO", "TBD", "PUBLICATION_HOLD", "WHOLE-BOOK CITATION PASS = CLOSED", "PRODUCT RELEASE = COMPLETE"):
        require(forbidden not in text, f"{path.relative_to(ROOT)} contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart whole-book integration: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart whole-book integration: PASS — 18 mapped entries, 3 assembled readers, 5 Product sources, 6 dossier-only, 4 owner gaps, citation pass open")
