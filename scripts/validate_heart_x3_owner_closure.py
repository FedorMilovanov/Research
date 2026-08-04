#!/usr/bin/env python3
"""Validate the Heart chapter X.3 conclusion section-owner closure overlay."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/heart-whole-book-integration-2026-08-04.json"
VII = ROOT / "data/heart-vii-owner-closure-2026-08-04.json"
I4 = ROOT / "data/heart-i4-owner-closure-2026-08-04.json"
X2 = ROOT / "data/heart-x2-owner-closure-2026-08-04.json"
X3 = ROOT / "data/heart-x3-owner-closure-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/87_X3_CONCLUDING_HOPE_OWNER_CLOSURE_2026-08-04.md"
CURRENT = ROOT / "СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-04.md"
R9 = ROOT / "СЕРИЯ СЕРДЦЕ/71_R9_CHRIST_OF_REVELATION.md"
BOOK = ROOT / "СЕРИЯ СЕРДЦЕ/82_BOOK_ASSEMBLY_DECISIONS_2026-08-02.md"
X2_HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/86_X2_GORIFIED_HEART_OWNER_CLOSURE_2026-08-04.md"

PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"
SATELLITE_PATH = "src/components/article-pilots/_shared/series/hardTextsSeriesConfig.ts"
SATELLITE_BLOB = "152c90b2dcee67d1683289445d0d2239905ed41c"
ARTICLE_PATH = "src/content/articles/osvobozhdennoe-serdce.mdx"
ARTICLE_BLOB = "16a2390da6e0d0382165fc8bf8b7150cb9253c1f"
X2_SECTION_IDS = [
    "chetyre-sostoyaniya",
    "vopl-i-otvet",
    "ne-besplotnoe-parenie",
    "ne-sposobno-greshit",
    "pobeda-nad-vragom",
]
RESEARCH_OWNERS = [
    "СЕРИЯ СЕРДЦЕ/71_R9_CHRIST_OF_REVELATION.md",
    "СЕРИЯ СЕРДЦЕ/82_BOOK_ASSEMBLY_DECISIONS_2026-08-02.md",
    "СЕРИЯ СЕРДЦЕ/86_X2_GORIFIED_HEART_OWNER_CLOSURE_2026-08-04.md",
]

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
base = load(BASE)
vii = load(VII)
i4 = load(I4)
x2 = load(X2)
x3 = load(X3)

require(base.get("authorityId") == "HEART-WHOLE-BOOK-INTEGRATION-2026-08-04", "base authority drift")
entries = base.get("entries", [])
require(isinstance(entries, list) and len(entries) == 18, "base must contain eighteen entries")
base_x3 = next((row for row in entries if isinstance(row, dict) and row.get("id") == "HEART-BOOK-X3"), None)
require(isinstance(base_x3, dict), "base X.3 entry missing")
if isinstance(base_x3, dict):
    require(base_x3.get("bookLabel") == "X.3 Заключительная надежда", "base X.3 label drift")
    require(base_x3.get("primaryState") == "OWNER_REQUIRED", "base X.3 historical state drift")
    require(base_x3.get("productOwner") is None, "base X.3 must remain pre-overlay snapshot")
    require(base_x3.get("researchOwners") == [], "base X.3 historical owner set drift")

require(vii.get("effectiveCounts", {}).get("productSourceOnly") == 6, "VII dependency Product count drift")
require(vii.get("effectiveCounts", {}).get("ownerRequired") == 3, "VII dependency gap count drift")
require(i4.get("effectiveCounts", {}).get("productSourceOnly") == 7, "I.4 dependency Product count drift")
require(i4.get("effectiveCounts", {}).get("ownerRequired") == 2, "I.4 dependency gap count drift")
require(x2.get("authorityId") == "HEART-X2-OWNER-CLOSURE-2026-08-04", "X.2 dependency authority drift")
require(x2.get("effectiveCounts", {}).get("productSourceOnly") == 8, "X.2 dependency Product count drift")
require(x2.get("effectiveCounts", {}).get("ownerRequired") == 1, "X.2 dependency gap count drift")
require(x2.get("remainingOwnerGaps") == ["HEART-BOOK-X3"], "X.2 dependency gap set drift")
require(x2.get("publicationBoundary", {}).get("x2SourceOwnerClosed") is True, "X.2 dependency owner not closed")
require(x2.get("publicationBoundary", {}).get("x2UnifiedReaderAssembled") is False, "X.2 dependency reader boundary drift")

require(x3.get("schemaVersion") == 1, "X.3 overlay schema drift")
require(x3.get("authorityId") == "HEART-X3-OWNER-CLOSURE-2026-08-04", "X.3 authority drift")
require(x3.get("status") == "X3_PRODUCT_SECTION_OWNER_ESTABLISHED_BOOK_INTEGRATION_AND_CITATION_PASS_OPEN", "X.3 status drift")
require(x3.get("generatedAt") == "2026-08-04", "X.3 generated date drift")
require(x3.get("lastVerifiedAt") == "2026-08-04", "X.3 verification date drift")
require(x3.get("baseAuthorityId") == base.get("authorityId"), "X.3 base authority mismatch")
require(x3.get("baseAuthority") == "data/heart-whole-book-integration-2026-08-04.json", "X.3 base path drift")
require(x3.get("dependsOnOverlays") == [
    "data/heart-vii-owner-closure-2026-08-04.json",
    "data/heart-i4-owner-closure-2026-08-04.json",
    "data/heart-x2-owner-closure-2026-08-04.json",
], "X.3 overlay dependency drift")
require(x3.get("researchSnapshot") == "54cd176d4a01158c575c3f404a62804f92dd4a12", "X.3 Research snapshot drift")

snapshot = x3.get("productSnapshot", {})
require(snapshot.get("repository") == "FedorMilovanov/gb-is-my-strength", "X.3 Product repository drift")
require(snapshot.get("commit") == PRODUCT_COMMIT, "X.3 Product commit drift")
require(snapshot.get("satelliteRegistry") == {"path": SATELLITE_PATH, "blobSha": SATELLITE_BLOB}, "X.3 satellite registry drift")
require(snapshot.get("articleOwner") == {"path": ARTICLE_PATH, "blobSha": ARTICLE_BLOB}, "X.3 article owner drift")

override = x3.get("entryOverride", {})
require(override.get("id") == "HEART-BOOK-X3", "X.3 override ID drift")
require(override.get("bookLabel") == "X.3 Заключительная надежда", "X.3 override label drift")
require(override.get("previousPrimaryState") == "OWNER_REQUIRED", "X.3 previous state drift")
require(override.get("effectivePrimaryState") == "PRODUCT_SOURCE_ONLY", "X.3 effective state drift")
require(override.get("sharedProductSourceWith") == "HEART-BOOK-X2", "X.3 shared Product source boundary drift")
require(override.get("primarySectionOwner") == {
    "productId": "osvobozhdennoe",
    "slug": "osvobozhdennoe-serdce",
    "minutes": 27,
    "sourcePath": ARTICLE_PATH,
    "sourceBlobSha": ARTICLE_BLOB,
    "sectionId": "vyhod",
    "sectionHeading": "Выход: сердце, наконец успокоенное",
    "role": "book-level conclusion from the whole journey of the heart to final Christ-centred hope",
}, "X.3 section owner drift")
require(override.get("researchOwners") == RESEARCH_OWNERS, "X.3 Research owner set drift")
for owner in RESEARCH_OWNERS:
    require((ROOT / owner).is_file(), f"X.3 Research owner missing: {owner}")
require(override.get("effectiveCitationState") == "PRODUCT_SECTION_CITATION_PASS_REQUIRED", "X.3 citation state drift")
require(override.get("manuscriptState") == "CONCLUSION_SECTION_SELECTED_BOOK_INTEGRATION_NOT_COMPLETE", "X.3 manuscript state drift")
require(len(str(override.get("dedupOwner", ""))) >= 350, "X.3 dedup owner too weak")

support = override.get("supportBoundary", {})
require(isinstance(support.get("supports"), list) and len(support["supports"]) == 4, "X.3 support set drift")
require(isinstance(support.get("doesNotSupport"), list) and len(support["doesNotSupport"]) == 6, "X.3 non-support set drift")
require("X.3 owns X.2's detailed doctrine of glorification or X.1's judicial sequence" in support.get("doesNotSupport", []), "X.3 dedup negative boundary missing")
require("the whole eighteen-entry manuscript has been assembled into one book file" in support.get("doesNotSupport", []), "X.3 manuscript negative boundary missing")

require(x3.get("effectiveCounts") == {
    "finalBookEntries": 18,
    "assembledReader": 3,
    "productSourceOnly": 9,
    "researchDossierOnly": 6,
    "ownerRequired": 0,
    "currentProductCoreItems": 6,
    "bookMatchedProductCoreItems": 5,
    "selectedProductSatelliteItems": 4,
    "uniqueProductPagesMapped": 9,
    "newDirectQuotesApproved": 0,
}, "X.3 effective counts drift")
require(x3.get("remainingOwnerGaps") == [], "X.3 remaining gap set must be empty")
require(x3.get("publicationBoundary") == {
    "allEighteenEntriesHaveOwners": True,
    "x3ConclusionSectionOwnerClosed": True,
    "x3BookIntegrationComplete": False,
    "wholeBookLineEditComplete": False,
    "wholeBookCitationPassComplete": False,
    "manuscriptBundleComplete": False,
    "productReleaseComplete": False,
    "newDirectQuotesApproved": 0,
}, "X.3 publication boundary drift")
require("shared Product article is partitioned by section" in str(x3.get("supersessionRule", "")), "X.3 section partition rule missing")

require(product_root.is_dir(), f"Product checkout missing: {product_root}")
require(run_git(product_root, "rev-parse", "HEAD") == PRODUCT_COMMIT, "X.3 Product checkout head drift")
require(run_git(product_root, "hash-object", SATELLITE_PATH) == SATELLITE_BLOB, "X.3 satellite registry blob drift")
require(run_git(product_root, "hash-object", ARTICLE_PATH) == ARTICLE_BLOB, "X.3 article blob drift")
satellite_file = product_root / SATELLITE_PATH
article_file = product_root / ARTICLE_PATH
require(satellite_file.is_file(), "X.3 satellite registry file missing")
require(article_file.is_file(), "X.3 article file missing")
satellite_text = satellite_file.read_text(encoding="utf-8") if satellite_file.is_file() else ""
article_text = article_file.read_text(encoding="utf-8") if article_file.is_file() else ""
require(re.search(r"id:\s*'osvobozhdennoe'[\s\S]{0,140}?slug:\s*'osvobozhdennoe-serdce'[\s\S]{0,80}?minutes:\s*27", satellite_text) is not None, "X.3 Product source registry drift")
vyhod_marker = '<h2 id="vyhod">Выход: сердце, наконец успокоенное</h2>'
require(vyhod_marker in article_text, "X.3 vyhod heading missing")
for marker in (
    "И вот последнее, к чему шла вся серия.",
    "прошли через новое рождение, войну двух природ, идолов, искушения, страхи, тьму",
    "увидели Христа, Который несёт немощных",
    "не к бесконечному самокопанию, а к лицу Божьему",
    "не к вечной тревоге, а к вечному насыщению",
    "Тот, Кто дал тебе новое сердце и Кто нёс тебя во всякой тьме, доведёт начатое до конца",
    "Здесь — война. Там — Он. И этого довольно, чтобы держаться.",
):
    require(marker in article_text, f"X.3 Product conclusion marker missing: {marker}")
vyhod_position = article_text.find(vyhod_marker)
sources_position = article_text.find('<h2 id="istochniki">')
require(vyhod_position >= 0 and sources_position > vyhod_position, "X.3 conclusion/source section order drift")
for section_id in X2_SECTION_IDS:
    position = article_text.find(f'id="{section_id}"')
    require(position >= 0 and position < vyhod_position, f"X.2 section must precede X.3 conclusion: {section_id}")
require(article_text.count(vyhod_marker) == 1, "X.3 vyhod heading must be unique")

r9 = read(R9)
book = read(BOOK)
x2_human = read(X2_HUMAN)
require("R9: ХРИСТОС АПОКАЛИПСИСА" in r9, "R9 Christ owner marker missing")
require("воскресшего Христа" in r9, "R9 risen-Christ boundary missing")
require("R9 не поглощается X.1" in r9, "R9/X.1 boundary missing")
require("18. X.3 — Заключительная надежда." in book, "book final-order X.3 marker missing")
require("R9 ROLE = CLOSED" in book, "book R9 decision marker missing")
require("FINAL ORDER = CLOSED" in book, "book final order marker missing")
require("does not silently reopen `R10`" in book or "R10" not in book, "book R10 boundary drift")
require("The final `vyhod` section is not silently absorbed into X.2 ownership" in x2_human, "X.2/X.3 shared-file boundary missing")
require("X.3 remains separate" in x2_human, "X.2 human X.3 separation marker missing")

human = read(HUMAN)
for marker in (
    "HEART-X3-OWNER-CLOSURE-2026-08-04",
    "X.3 CONCLUSION SECTION OWNER = CLOSED",
    "ALL 18 ENTRY OWNERS = MAPPED",
    "STANDALONE OWNER GAPS = 0",
    "BOOK INTEGRATION = NOT COMPLETE",
    PRODUCT_COMMIT,
    SATELLITE_BLOB,
    ARTICLE_BLOB,
    "section id = vyhod",
):
    require(marker in human, f"X.3 human authority marker missing: {marker}")

current = read(CURRENT)
for marker in (
    "HEART-CURRENT-AUTHORITY-2026-08-04",
    "X.3 CONCLUSION SECTION OWNER = CLOSED",
    "ALL 18 ENTRY OWNERS = MAPPED",
    "PRODUCT SOURCE OWNERS = 9",
    "STANDALONE OWNER GAPS = 0",
    "WHOLE-BOOK CITATION PASS = OPEN",
    "MANUSCRIPT BUNDLE = INCOMPLETE",
):
    require(marker in current, f"current authority X.3 marker missing: {marker}")
owner_gap_section = current.split("### Manuscript owner gaps", 1)[-1].split("### Dossier-to-reader assembly", 1)[0]
require("NONE — all 18 entries have deterministic owners" in owner_gap_section, "current owner-gap closure marker missing")
for former_gap in (
    "I.4 `Внутренний человек и телесная жизнь`",
    "VII `Сердце в страдании и унынии`",
    "X.2 `Освобождённое сердце`",
    "X.3 `Заключительная надежда`",
):
    require(former_gap not in owner_gap_section, f"former owner gap remains listed: {former_gap}")

for path, text in ((HUMAN, human), (CURRENT, current)):
    for forbidden in (
        "X.3 CONCLUSION SECTION OWNER = OPEN",
        "BOOK INTEGRATION = COMPLETE",
        "WHOLE-BOOK CITATION PASS = CLOSED",
        "PRODUCT RELEASE = COMPLETE",
        "NEW DIRECT QUOTES = 1",
        "TODO",
        "TBD",
    ):
        require(forbidden not in text, f"{path.relative_to(ROOT)} contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart X.3 owner closure: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart X.3 owner closure: PASS — all eighteen owners mapped, conclusion section partitioned, manuscript/citation/Product release open")
