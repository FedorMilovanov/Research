#!/usr/bin/env python3
"""Validate the paraphrase-only final-book reader assembly for Heart X.3."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / "data/heart-x3-owner-closure-2026-08-04.json"
ASSEMBLY = ROOT / "data/heart-x3-reader-assembly-2026-08-04.json"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/88_READER_CHAPTER_X3_CONCLUDING_HOPE_2026-08-04.md"
CURRENT = ROOT / "СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-04.md"

PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"
ARTICLE_PATH = "src/content/articles/osvobozhdennoe-serdce.mdx"
ARTICLE_BLOB = "16a2390da6e0d0382165fc8bf8b7150cb9253c1f"
MAIN_SECTIONS = [
    "Последнее движение книги",
    "Не самокопание, а лицо Божье",
    "Здесь война, там Христос",
    "Надежда, которая сохраняет границы",
    "Заключение",
]
EXCLUDED_X2_TOPICS = [
    "четыре состояния человечества",
    "non posse peccare destination",
    "ἀπολύτρωσις",
    "σῶμα πνευματικόν",
    "ἀφθαρσία",
    "νῖκος",
]
EXACT_PRODUCT_SENTENCES = [
    "И вот последнее, к чему шла вся серия.",
    "не к бесконечному самокопанию, а к лицу Божьему; не к вечной тревоге, а к вечному насыщению.",
    "Здесь — война. Там — Он. И этого довольно, чтобы держаться.",
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

owner = load(OWNER)
assembly = load(ASSEMBLY)
reader = read(READER)
current = read(CURRENT)

# Owner overlay remains the exact source boundary and historical pre-assembly snapshot.
require(owner.get("authorityId") == "HEART-X3-OWNER-CLOSURE-2026-08-04", "X.3 owner authority drift")
require(owner.get("entryOverride", {}).get("effectivePrimaryState") == "PRODUCT_SECTION_ONLY", "X.3 owner source-state drift")
require(owner.get("entryOverride", {}).get("primaryProductOwner", {}).get("sectionId") == "vyhod", "X.3 owner section drift")
require(owner.get("publicationBoundary", {}).get("x3ConclusionSectionSelected") is True, "X.3 section owner not closed")
require(owner.get("publicationBoundary", {}).get("x3FinalBookConclusionAssembled") is False, "X.3 owner snapshot must remain pre-assembly")
require(owner.get("effectiveCounts", {}).get("productSectionOnly") == 1, "X.3 owner snapshot section count drift")
require(owner.get("effectiveCounts", {}).get("ownerRequired") == 0, "X.3 owner snapshot gap drift")

# Reader assembly authority.
require(assembly.get("schemaVersion") == 1, "X.3 reader schema drift")
require(assembly.get("authorityId") == "HEART-X3-READER-ASSEMBLY-2026-08-04", "X.3 reader authority drift")
require(assembly.get("status") == "X3_FINAL_BOOK_READER_ASSEMBLED_PARAPHRASE_ONLY_WHOLE_BOOK_QA_OPEN", "X.3 reader status drift")
require(assembly.get("generatedAt") == assembly.get("lastVerifiedAt") == "2026-08-04", "X.3 reader date drift")
require(assembly.get("ownerAuthorityId") == owner.get("authorityId"), "X.3 reader/owner authority mismatch")
require(assembly.get("ownerAuthority") == "data/heart-x3-owner-closure-2026-08-04.json", "X.3 reader owner path drift")
require(assembly.get("researchSnapshot") == "18d25e0173fada290e30ecbd1b8cd7f0dc6d9c23", "X.3 reader Research snapshot drift")
require(assembly.get("reader") == {
    "id": "HEART-READER-X3-CONCLUDING-HOPE-2026-08-04",
    "bookEntryId": "HEART-BOOK-X3",
    "bookLabel": "X.3 Заключительная надежда",
    "path": "СЕРИЯ СЕРДЦЕ/88_READER_CHAPTER_X3_CONCLUDING_HOPE_2026-08-04.md",
    "state": "ASSEMBLED_READER_PARAPHRASE_ONLY",
    "sections": MAIN_SECTIONS,
}, "X.3 reader registry drift")
require(assembly.get("exactSource") == {
    "repository": "FedorMilovanov/gb-is-my-strength",
    "commit": PRODUCT_COMMIT,
    "path": ARTICLE_PATH,
    "blobSha": ARTICLE_BLOB,
    "sectionId": "vyhod",
    "sectionTitle": "Выход: сердце, наконец успокоенное",
    "sectionEndId": "istochniki",
}, "X.3 reader exact-source drift")
require(assembly.get("composition") == {
    "mode": "PARAPHRASE_ONLY",
    "newHistoricalClaims": 0,
    "newDirectQuotesApproved": 0,
    "exactProductProseQuotesCopied": 0,
    "x2OwnedSectionsCopied": 0,
    "sourceOwnerChanged": False,
    "x2OwnershipChanged": False,
    "wholeBookOrderChanged": False,
}, "X.3 reader composition boundary drift")
require(len(assembly.get("requiredBoundaries", [])) == 6, "X.3 reader required-boundary set drift")
require(assembly.get("effectivePrimaryState") == {
    "entryId": "HEART-BOOK-X3",
    "previous": "PRODUCT_SECTION_ONLY",
    "current": "ASSEMBLED_READER",
    "sourceBackedByProductSection": True,
}, "X.3 reader effective-state drift")
require(assembly.get("effectiveCounts") == {
    "finalBookEntries": 18,
    "assembledReader": 4,
    "productSourceOnly": 8,
    "productSectionOnly": 0,
    "researchDossierOnly": 6,
    "ownerRequired": 0,
    "sourceBackedByProductSection": 1,
    "uniqueProductPagesMapped": 9,
    "newDirectQuotesApproved": 0,
}, "X.3 reader effective count drift")
require(assembly.get("remainingReaderAssemblies") == [
    "HEART-BOOK-I4",
    "HEART-BOOK-II",
    "HEART-BOOK-III2",
    "HEART-BOOK-IV",
    "HEART-BOOK-VI",
    "HEART-BOOK-VII",
    "HEART-BOOK-VIII",
    "HEART-BOOK-IX",
    "HEART-BOOK-X2",
], "X.3 remaining reader assembly set drift")
require(assembly.get("publicationBoundary") == {
    "allEighteenEntriesOwnerMapped": True,
    "x3FinalBookConclusionAssembled": True,
    "wholeBookReaderAssemblyComplete": False,
    "wholeBookCitationPassComplete": False,
    "wholeBookTransitionDedupPassComplete": False,
    "wholeBookLineEditComplete": False,
    "manuscriptBundleComplete": False,
    "productReleaseComplete": False,
    "newDirectQuotesApproved": 0,
}, "X.3 reader publication boundary drift")

# Exact Product owner is unchanged and section remains available.
require(product_root.is_dir(), "Product checkout missing")
require(git(product_root, "rev-parse", "HEAD") == PRODUCT_COMMIT, "Product checkout head drift")
require(git(product_root, "hash-object", ARTICLE_PATH) == ARTICLE_BLOB, "Product article blob drift")
article = read(product_root / ARTICLE_PATH)
require('<h2 id="vyhod">Выход: сердце, наконец успокоенное</h2>' in article, "Product vyhod section missing")
require('<h2 id="istochniki">Источники и сверка</h2>' in article, "Product source-section boundary missing")

# Reader manuscript: complete, paraphrase-only and bounded.
require(reader.startswith("# X.3. Заключительная надежда\n"), "X.3 reader title drift")
for marker in (
    "**Reader authority:** `HEART-X3-READER-ASSEMBLY-2026-08-04`",
    "**Source owner:** `data/heart-x3-owner-closure-2026-08-04.json`",
    "**Exact Product section:** `osvobozhdennoe-serdce#vyhod`",
    "**Новые прямые цитаты:** `0`",
    "**Статус:** `ASSEMBLED / PARAPHRASE-ONLY / WHOLE-BOOK LINE EDIT OPEN`",
    "## Source and editorial boundary",
    "NEW HISTORICAL CLAIMS = 0",
    "NEW DIRECT QUOTES = 0",
    "X.2 SECTION OWNERSHIP CHANGED = 0",
    "WHOLE-BOOK CITATION PASS = OPEN",
    "PRODUCT RELEASE OF FINAL BOOK = NOT CLAIMED",
):
    require(marker in reader, f"X.3 reader marker missing: {marker}")
for section in MAIN_SECTIONS:
    require(f"## {section}" in reader, f"X.3 reader section missing: {section}")
require(len(reader) >= 9000, "X.3 reader is too short for final-book conclusion")
word_count = len(re.findall(r"[A-Za-zА-Яа-яЁё0-9-]+", reader))
require(word_count >= 1100, f"X.3 reader word count too low: {word_count}")
require(not any(line.startswith(">") for line in reader.splitlines()), "X.3 reader contains Markdown direct quotation")
require("<blockquote" not in reader.lower(), "X.3 reader contains HTML blockquote")
for exact in EXACT_PRODUCT_SENTENCES:
    require(exact not in reader, f"X.3 reader copied exact Product prose: {exact}")
for topic in EXCLUDED_X2_TOPICS:
    require(topic not in reader, f"X.3 reader imported X.2 detailed exposition: {topic}")
for forbidden in (
    "NEW DIRECT QUOTES = 1",
    "NEW HISTORICAL CLAIMS = 1",
    "WHOLE-BOOK CITATION PASS = CLOSED",
    "WHOLE-BOOK LINE EDIT = CLOSED",
    "MANUSCRIPT BUNDLE = COMPLETE",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in reader, f"X.3 reader contains forbidden marker: {forbidden}")

# Current authority must reflect the later reader transaction while preserving owner history.
for marker in (
    "ALL 18 ENTRIES OWNER-MAPPED = TRUE",
    "X.3 CONCLUSION SECTION OWNER = CLOSED",
    "FINAL-BOOK X.3 MANUSCRIPT = ASSEMBLED",
    "ASSEMBLED READER OWNERS = 4",
    "PRODUCT SOURCE OWNERS = 8",
    "CURRENT PRIMARY PRODUCT SECTION OWNERS = 0",
    "SOURCE-BACKED PRODUCT SECTION READERS = 1",
    "STANDALONE OWNER GAPS = 0",
    "WHOLE-BOOK READER ASSEMBLY = INCOMPLETE",
):
    require(marker in current, f"current authority X.3 reader marker missing: {marker}")
for forbidden in (
    "WHOLE-BOOK CITATION PASS = CLOSED",
    "WHOLE-BOOK LINE EDIT = CLOSED",
    "MANUSCRIPT BUNDLE = COMPLETE",
    "PRODUCT RELEASE = COMPLETE",
):
    require(forbidden not in current, f"current authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart X.3 reader assembly: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Heart X.3 reader assembly: PASS — {word_count} words, paraphrase-only, 4 assembled readers, whole-book QA open")
