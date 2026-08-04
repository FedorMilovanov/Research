#!/usr/bin/env python3
"""Fail-closed validation for the Heart X.2 owner overlay."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/heart-whole-book-integration-2026-08-04.json"
VII = ROOT / "data/heart-vii-owner-closure-2026-08-04.json"
I4 = ROOT / "data/heart-i4-owner-closure-2026-08-04.json"
X2 = ROOT / "data/heart-x2-owner-closure-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/86_X2_GORIFIED_HEART_OWNER_CLOSURE_2026-08-04.md"
CURRENT = ROOT / "СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-04.md"
X1_DOSSIER = ROOT / "СЕРИЯ СЕРДЦЕ/77_P0_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md"
X1_READER = ROOT / "СЕРИЯ СЕРДЦЕ/81_READER_CHAPTER_X1_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md"

PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"
SATELLITE_PATH = "src/components/article-pilots/_shared/series/hardTextsSeriesConfig.ts"
SATELLITE_BLOB = "152c90b2dcee67d1683289445d0d2239905ed41c"
ARTICLE_PATH = "src/content/articles/osvobozhdennoe-serdce.mdx"
ARTICLE_BLOB = "16a2390da6e0d0382165fc8bf8b7150cb9253c1f"
SECTIONS = [
    "chetyre-sostoyaniya",
    "vopl-i-otvet",
    "ne-besplotnoe-parenie",
    "ne-sposobno-greshit",
    "pobeda-nad-vragom",
]

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    require(isinstance(value, dict), f"{path.relative_to(ROOT)}: object required")
    return value if isinstance(value, dict) else {}


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return ""


def git(repo: Path, *args: str) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        errors.append(f"git {' '.join(args)} failed: {exc}")
        return ""


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
product_root = parser.parse_args().product_root.resolve()

base = load(BASE)
vii = load(VII)
i4 = load(I4)
x2 = load(X2)

require(base.get("authorityId") == "HEART-WHOLE-BOOK-INTEGRATION-2026-08-04", "base authority drift")
require(base.get("counts", {}).get("productSourceOnly") == 5, "base Product count drift")
require(base.get("counts", {}).get("ownerRequired") == 4, "base gap count drift")
entries = base.get("entries", [])
require(isinstance(entries, list) and len(entries) == 18, "base must contain 18 entries")
base_x2 = next((row for row in entries if isinstance(row, dict) and row.get("id") == "HEART-BOOK-X2"), {})
require(base_x2.get("bookLabel") == "X.2 Освобождённое сердце", "base X.2 label drift")
require(base_x2.get("primaryState") == "OWNER_REQUIRED", "base X.2 historical state drift")
require(base_x2.get("productOwner") is None and base_x2.get("researchOwners") == [], "base X.2 snapshot mutated")

require(vii.get("authorityId") == "HEART-VII-OWNER-CLOSURE-2026-08-04", "VII dependency drift")
require(vii.get("effectiveCounts", {}).get("productSourceOnly") == 6, "VII Product count drift")
require(vii.get("effectiveCounts", {}).get("ownerRequired") == 3, "VII gap count drift")
require(i4.get("authorityId") == "HEART-I4-OWNER-CLOSURE-2026-08-04", "I.4 dependency drift")
require(i4.get("effectiveCounts", {}).get("productSourceOnly") == 7, "I.4 Product count drift")
require(i4.get("effectiveCounts", {}).get("ownerRequired") == 2, "I.4 gap count drift")
require(i4.get("remainingOwnerGaps") == ["HEART-BOOK-X2", "HEART-BOOK-X3"], "I.4 gap set drift")

require(x2.get("schemaVersion") == 1, "X.2 schema drift")
require(x2.get("authorityId") == "HEART-X2-OWNER-CLOSURE-2026-08-04", "X.2 authority drift")
require(x2.get("status") == "X2_PRODUCT_SOURCE_ESTABLISHED_UNIFIED_READER_AND_BOOK_CITATION_PASS_OPEN", "X.2 status drift")
require(x2.get("generatedAt") == x2.get("lastVerifiedAt") == "2026-08-04", "X.2 date drift")
require(x2.get("baseAuthorityId") == base.get("authorityId"), "X.2 base authority mismatch")
require(x2.get("dependsOnOverlays") == [
    "data/heart-vii-owner-closure-2026-08-04.json",
    "data/heart-i4-owner-closure-2026-08-04.json",
], "X.2 dependency order drift")
require(x2.get("researchSnapshot") == "4a3f3966d3ebf9df7d0ff2b3777ec9d446321a9b", "X.2 Research snapshot drift")

snapshot = x2.get("productSnapshot", {})
require(snapshot.get("repository") == "FedorMilovanov/gb-is-my-strength", "Product repository drift")
require(snapshot.get("commit") == PRODUCT_COMMIT, "Product commit drift")
require(snapshot.get("satelliteRegistry") == {"path": SATELLITE_PATH, "blobSha": SATELLITE_BLOB}, "satellite witness drift")
require(snapshot.get("articleOwner") == {"path": ARTICLE_PATH, "blobSha": ARTICLE_BLOB}, "article witness drift")

override = x2.get("entryOverride", {})
require(override.get("id") == "HEART-BOOK-X2", "X.2 ID drift")
require(override.get("previousPrimaryState") == "OWNER_REQUIRED", "X.2 previous state drift")
require(override.get("effectivePrimaryState") == "PRODUCT_SOURCE_ONLY", "X.2 effective state drift")
require(override.get("primaryProductOwner") == {
    "id": "osvobozhdennoe",
    "slug": "osvobozhdennoe-serdce",
    "minutes": 27,
    "role": "glorification-bodily-redemption-final-freedom-from-sin primary source",
    "sourcePath": ARTICLE_PATH,
    "sourceBlobSha": ARTICLE_BLOB,
}, "X.2 Product owner drift")
require([row.get("id") for row in override.get("sectionOwners", []) if isinstance(row, dict)] == SECTIONS, "X.2 section order drift")
require(all(len(str(row.get("role", ""))) >= 30 for row in override.get("sectionOwners", []) if isinstance(row, dict)), "X.2 section role too weak")
require(override.get("researchOwners") == [
    "СЕРИЯ СЕРДЦЕ/77_P0_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md",
    "СЕРИЯ СЕРДЦЕ/81_READER_CHAPTER_X1_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md",
], "X.2 Research owner drift")
require(override.get("effectiveCitationState") == "PRODUCT_SOURCE_CITATION_PASS_REQUIRED", "X.2 citation state drift")
require(override.get("manuscriptState") == "SOURCE_SELECTED_UNIFIED_X2_READER_NOT_ASSEMBLED", "X.2 manuscript state drift")
require(len(str(override.get("dedupOwner", ""))) >= 300, "X.2 dedup boundary too weak")

boundary = override.get("supportBoundary", {})
require(len(boundary.get("supports", [])) == 4, "X.2 support set drift")
require(len(boundary.get("doesNotSupport", [])) == 6, "X.2 non-support set drift")
require("X.2 automatically owns the separate X.3 book conclusion" in boundary.get("doesNotSupport", []), "X.2/X.3 separation missing")

require(x2.get("effectiveCounts") == {
    "finalBookEntries": 18,
    "assembledReader": 3,
    "productSourceOnly": 8,
    "researchDossierOnly": 6,
    "ownerRequired": 1,
    "currentProductCoreItems": 6,
    "bookMatchedProductCoreItems": 5,
    "selectedProductSatelliteItems": 4,
    "newDirectQuotesApproved": 0,
}, "X.2 effective count drift")
require(x2.get("remainingOwnerGaps") == ["HEART-BOOK-X3"], "X.2 remaining gap drift")
require(x2.get("publicationBoundary") == {
    "x2SourceOwnerClosed": True,
    "x2UnifiedReaderAssembled": False,
    "wholeBookLineEditComplete": False,
    "wholeBookCitationPassComplete": False,
    "manuscriptBundleComplete": False,
    "productReleaseComplete": False,
    "newDirectQuotesApproved": 0,
}, "X.2 publication boundary drift")

require(product_root.is_dir(), "Product checkout missing")
require(git(product_root, "rev-parse", "HEAD") == PRODUCT_COMMIT, "Product checkout head drift")
require(git(product_root, "hash-object", SATELLITE_PATH) == SATELLITE_BLOB, "satellite blob drift")
require(git(product_root, "hash-object", ARTICLE_PATH) == ARTICLE_BLOB, "article blob drift")
satellite_text = read(product_root / SATELLITE_PATH)
article_text = read(product_root / ARTICLE_PATH)
require(re.search(r"id:\s*'osvobozhdennoe'[\s\S]{0,140}?slug:\s*'osvobozhdennoe-serdce'[\s\S]{0,80}?minutes:\s*27", satellite_text) is not None, "Product registry pair/minutes drift")
for marker in (
    'h1: "Конец войне: сердце, освобождённое навсегда"',
    'slug: "osvobozhdennoe-serdce"',
    'sourcesRequired: true',
    'readingTime: 27',
    '  - "прославление"',
    '  - "воскресение"',
    'состояние славы, где сердце окончательно освобождается от греха',
    'Надежда эта — не бесплотное парение на облаках, а телесное воскресение и новое творение',
    'сделана совершенно и неизменно свободной только к добру',
    'И ничего уже не будет проклятого',
):
    require(marker in article_text, f"Product article marker missing: {marker}")
for section in SECTIONS:
    require(f'id="{section}"' in article_text, f"Product section missing: {section}")
require('id="vyhod"' in article_text, "separate X.3 candidate section missing")

x1_dossier = read(X1_DOSSIER)
x1_reader = read(X1_READER)
require("EVIDENCE CLOSED / BOUNDARIES CLOSED / CHAPTER-READY" in x1_dossier, "X.1 dossier authority missing")
require("тело и преображение" in x1_dossier, "X.1 bodily boundary missing")
require("ясные тексты и система тысячелетия" in x1_dossier, "X.1 millennial boundary missing")
require("**Reader assembly authority:** `HEART-READER-ASSEMBLY-2026-08-02`" in x1_reader, "X.1 reader authority missing")
require("Бог спасает целого человека и поднимет тело" in x1_reader, "X.1 whole-person resurrection missing")
require("тело получит качества нетления, славы и силы" in x1_reader, "X.1 glorified-body marker missing")

human = read(HUMAN)
current = read(CURRENT)
for marker in (
    "HEART-X2-OWNER-CLOSURE-2026-08-04",
    "X.2 SOURCE OWNER = CLOSED",
    "UNIFIED X.2 READER = NOT ASSEMBLED",
    "OWNER GAPS REMAINING = 1",
    PRODUCT_COMMIT,
    SATELLITE_BLOB,
    ARTICLE_BLOB,
):
    require(marker in human, f"X.2 human marker missing: {marker}")
for marker in (
    "X.2 SOURCE OWNER = CLOSED",
    "UNIFIED X.2 READER = NOT ASSEMBLED",
    "PRODUCT SOURCE OWNERS = 8",
    "STANDALONE OWNER GAPS = 1",
    "X.3 `Заключительная надежда`",
):
    require(marker in current, f"current authority marker missing: {marker}")
gaps = current.split("### Manuscript owner gaps", 1)[-1].split("### Dossier-to-reader assembly", 1)[0]
require("X.3 `Заключительная надежда`" in gaps, "X.3 missing from current gap section")
for closed in (
    "I.4 `Внутренний человек и телесная жизнь`",
    "VII `Сердце в страдании и унынии`",
    "X.2 `Освобождённое сердце`",
):
    require(closed not in gaps, f"closed owner returned to gap section: {closed}")

for text, name in ((human, "human"), (current, "current")):
    for forbidden in (
        "UNIFIED X.2 READER = ASSEMBLED",
        "WHOLE-BOOK CITATION PASS = CLOSED",
        "PRODUCT RELEASE = COMPLETE",
        "NEW DIRECT QUOTES = 1",
        "TODO",
        "TBD",
    ):
        require(forbidden not in text, f"{name} authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart X.2 owner closure: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart X.2 owner closure: PASS — exact Product glorification source selected, 1 owner gap remains, reader/citation/Product release open")
