#!/usr/bin/env python3
"""Validate the completed I.3 entry citation pass."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
RECEIPT_PATH = ROOT / "data/heart-i3-citation-review-2026-08-04.json"
ASSEMBLY_PATH = ROOT / "data/heart-i3-reader-assembly-2026-08-04.json"
CURRENT_PATH = ROOT / "data/heart-entry-citation-pass-current-v4-2026-08-04.json"
TRIAGE_PATH = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
READER_PATH = ROOT / "СЕРИЯ СЕРДЦЕ/109_READER_CHAPTER_I3_FALLEN_HEART_JEREMIAH_17_2026-08-04.md"
HUMAN_PATH = ROOT / "СЕРИЯ СЕРДЦЕ/111_I3_CITATION_REVIEW_2026-08-04.md"
PRODUCT_REL = Path("src/content/articles/krajne-li-isporcheno-serdce.mdx")

EXPECTED_COUNTS = {
    "SCRIPTURE_DIRECT_OR_EXPLICIT_TRANSLATION": 40,
    "ATTRIBUTED_THEOLOGICAL_OR_CONFESSIONAL_DIRECT": 61,
    "TITLE_OR_LINK_LABEL": 58,
    "EDITORIAL_LEXICAL_OR_CAPTION": 65,
}
EXPECTED_URLS = [
    "https://archive.org/details/humannatureinits00bostuoft",
    "https://ccel.org/ccel/berkhof/systematictheology.vi.x.html",
    "https://ccel.org/ccel/edwards/affections/affections",
    "https://gospod-bog.ru/articles/krajne-li-isporcheno-serdce/",
    "https://web.archive.org/web/2/https://www.digitalpuritan.net/Digital%20Puritan%20Resources/Clarkson,%20David/The%20Practical%20Works%20of%20David%20Clarkson%20",
    "https://www.ccel.org/ccel/calvin/institutes.iii.xii.html",
    "https://www.ccel.org/ccel/owen/mort.i.v.html",
    "https://www.ccel.org/study/Jeremiah_17:9-10",
    "https://www.desiringgod.org/interviews/is-the-believers-heart-desperately-sick",
    "https://www.desiringgod.org/interviews/is-the-christians-heart-deceitfully-wicked",
    "https://www.monergism.com/heart-christ-heaven-towards-sinners-earth-ebook",
    "https://www.monergism.com/keeping-heart-ebook",
    "https://www.monergism.com/precious-remedies-against-satans-devices-ebook",
    "https://www.monergism.com/thethreshold/sdg/owen_remainderssin.html",
    "https://www.spurgeon.org/resource-library/sermons/honest-dealing-with-god/",
]
EXPECTED_INTERNAL = {
    "/articles/hermenevticheskaya-otsenka-hristotsentrichnoy-germenevtiki/":
        ("src/content/articles/hermenevticheskaya-otsenka-hristotsentrichnoy-germenevtiki.mdx", "ddebf8208cb6c47814926c9c488a9a9bddc04340"),
    "/articles/krajne-li-isporcheno-serdce/":
        ("src/content/articles/krajne-li-isporcheno-serdce.mdx", "dc27b7a06d37321a068e971c02af4a0df3028ae6"),
    "/articles/rimlyanam-7-veruyushchiy-ili-neveruyushchiy/":
        ("src/content/articles/rimlyanam-7-veruyushchiy-ili-neveruyushchiy.mdx", "b8c5f655446f4bbea95bcb5fff5a8a980aaf25cc"),
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
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be an object")
    return value if isinstance(value, dict) else {}


def git_blob(path: Path, repo_root: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(repo_root))],
        cwd=repo_root,
        text=True,
    ).strip()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def json_sha(value: Any, *, sort_keys: bool = False) -> str:
    return sha_text(json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=sort_keys,
    ))


def normalize(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def scan_scope(text: str, section_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    patterns = [
        ("RUSSIAN_GUILLEMETS", re.compile(r"«([^»\n]{8,})»")),
        ("CURLY_QUOTES", re.compile(r"“([^”\n]{8,})”")),
        ("MARKDOWN_BLOCKQUOTE", re.compile(r"(?m)^\s*>\s?(\S.*)$")),
        ("HTML_BLOCKQUOTE", re.compile(r"<blockquote[^>]*>(.*?)</blockquote>", re.S | re.I)),
    ]
    for surface_type, pattern in patterns:
        for match in pattern.finditer(text):
            value = normalize(match.group(1))
            rows.append({
                "sectionId": section_id,
                "type": surface_type,
                "sha256": sha_text(value),
                "characters": len(value),
            })
    return rows


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
assembly = read_json(ASSEMBLY_PATH)
current = read_json(CURRENT_PATH)
triage = read_json(TRIAGE_PATH)
product_text = product_path.read_text(encoding="utf-8")
reader_text = READER_PATH.read_text(encoding="utf-8")

require(git_blob(ASSEMBLY_PATH) == "2ae5a01ed0a2c9931b7a36f4991cf93bcec3fb7a", "I.3 assembly blob drift")
require(git_blob(CURRENT_PATH) == "d0ddea6cf1fc33dfab53ae9691aaf2d903d03b73", "current V4 blob drift")
require(git_blob(TRIAGE_PATH) == "de4d49cada15b231dfc31058aced4ec7a25928a2", "historical triage blob drift")
require(git_blob(READER_PATH) == "a958066bff3010f14540d67c900c362bd88de98a", "I.3 reader blob drift")
require(git_blob(product_path, product_root) == "dc27b7a06d37321a068e971c02af4a0df3028ae6", "I.3 Product blob drift")
require(sha_text(product_text) == "4292f76ff3e2fa15dfd682b5a421400ce9a62ec391109b3109aef14d72b224f0", "I.3 Product SHA drift")
require(sha_text(reader_text) == "6d00cbd44a7d3540faddcbdbc03bfff1fd1c5a441c380392010f973d76ce92f9", "I.3 reader SHA drift")

product_scan = module.scan_owner(module.p(str(PRODUCT_REL), "historical full I.3 owner"), product_root)
reader_scan = module.scan_owner(module.r(str(READER_PATH.relative_to(ROOT)), "assembled I.3 reader"), product_root)
refs = sorted(product_scan["scriptureReferences"], key=str.casefold)
require(len(refs) == 71, "I.3 Scripture count drift")
require(sha_text(json.dumps(refs, ensure_ascii=False, separators=(",", ":"))) == "25a12fcd595c213eb09589c08b3be4a9b76d7cb24e586ba2b505f0b7fc6c56a1", "I.3 Scripture set hash drift")
require(sorted(product_scan["externalLinks"], key=str.casefold) == EXPECTED_URLS, "I.3 external URL set drift")
require(sorted(product_scan["internalArticleLinks"]) == sorted(EXPECTED_INTERNAL), "I.3 internal URL set drift")

starts = [(m.start(), m.group(1)) for m in re.finditer(r'<h2\s+id="([^"]+)"', product_text)]
scopes: list[tuple[str, str]] = []
first_start = starts[0][0] if starts else len(product_text)
scopes.append(("frontmatter-or-introduction", product_text[:first_start]))
for index, (start, section_id) in enumerate(starts):
    end = starts[index + 1][0] if index + 1 < len(starts) else len(product_text)
    scopes.append((section_id, product_text[start:end]))
base_rows: list[dict[str, Any]] = []
for section_id, scoped in scopes:
    base_rows.extend(scan_scope(scoped, section_id))

owner = receipt.get("fullOwnerReview", {})
require(len(base_rows) == 224, "I.3 quotation surface count drift")
require(json_sha(base_rows) == owner.get("sourceSurfaceBaseManifestSha256") == "a0bbd74fb06fb3aca9c2917edfb3323b0df10d46f297e8f3032617a9da679c5a", "I.3 base surface manifest drift")

index_map = owner.get("surfaceClassOccurrenceIndices", {})
require(set(index_map) == set(EXPECTED_COUNTS), "I.3 class taxonomy drift")
require(json_sha(index_map, sort_keys=True) == owner.get("classificationIndexMapSha256") == "768d5acd3b5765eb5095295731b5f9fc0c77448ef9720472633bce440e14925a", "I.3 class index-map hash drift")
assigned: dict[int, str] = {}
for class_name, indices in index_map.items():
    require(indices == sorted(indices), f"I.3 occurrence indices not sorted: {class_name}")
    require(len(indices) == EXPECTED_COUNTS[class_name], f"I.3 class count drift: {class_name}")
    for index in indices:
        require(isinstance(index, int) and 0 <= index < 224, f"I.3 invalid occurrence index: {index}")
        require(index not in assigned, f"I.3 occurrence assigned twice: {index}")
        assigned[index] = class_name
require(set(assigned) == set(range(224)), "I.3 occurrence taxonomy is not exhaustive")

classified_rows = [
    {**row, "class": assigned[index]}
    for index, row in enumerate(base_rows)
]
require(json_sha(classified_rows) == owner.get("quotationSurfaceManifestSha256") == "4e4b33791308eb1589112e61b41fd09b7b1f04a2a1a067187fe588a6878077c3", "I.3 classified manifest drift")
require(Counter(row["class"] for row in classified_rows) == Counter(EXPECTED_COUNTS), "I.3 class occurrence counts drift")
hash_classes: dict[str, set[str]] = defaultdict(set)
for row in classified_rows:
    hash_classes[row["sha256"]].add(row["class"])
require(all(len(values) == 1 for values in hash_classes.values()), "I.3 identical source text assigned to multiple classes")

section_summary: dict[str, dict[str, Any]] = {}
for row in classified_rows:
    bucket = section_summary.setdefault(row["sectionId"], {"surfaces": 0, "classes": Counter()})
    bucket["surfaces"] += 1
    bucket["classes"][row["class"]] += 1
section_summary = {
    key: {
        "surfaces": value["surfaces"],
        "classes": dict(sorted(value["classes"].items())),
    }
    for key, value in section_summary.items()
}
require(json_sha(section_summary, sort_keys=True) == owner.get("sectionSummarySha256") == "f46b756c5f6e4f3afcda331d2e0ae94543ccabb24b6b02af537c78f1943df30e", "I.3 section summary hash drift")
require(owner.get("sectionSummary") == section_summary, "I.3 receipt section summary drift")
require(owner.get("quotationClassCounts") == EXPECTED_COUNTS, "I.3 receipt class count block drift")
require(owner.get("allScriptureReferenceTokensGoverned") is True, "I.3 Scripture governance flag drift")
require(owner.get("allQuotationSurfacesClassified") is True, "I.3 quotation governance flag drift")
require(owner.get("bulkDirectQuotationApproval") is False, "I.3 bulk quote approval must remain false")

link_review = receipt.get("externalLinkReview", {})
require(link_review.get("linksDispositioned") == 15, "I.3 external dispositions count drift")
require(link_review.get("originalLinksRequiringCanonicalReplacement") == 3, "I.3 replacement count drift")
require(json_sha(link_review.get("dispositions", []), sort_keys=True) == link_review.get("dispositionRegistrySha256") == "a1d9756c47064a182fea6a95dd06cc162fb1aac3d5304557855202ad3bfd1134", "I.3 external disposition registry drift")
require([row.get("url") for row in link_review.get("dispositions", [])] == EXPECTED_URLS, "I.3 external disposition URL order drift")
require(all(row.get("directQuoteBulkApproval") is False for row in link_review.get("dispositions", [])), "I.3 external disposition bulk-approves quotations")
require(sum(bool(row.get("replacementUrl")) for row in link_review.get("dispositions", [])) == 3, "I.3 canonical replacement registry drift")

internal_review = receipt.get("internalLinkReview", {})
internal_rows = internal_review.get("targets", [])
require(json_sha(internal_rows, sort_keys=True) == internal_review.get("targetRegistrySha256") == "3e30de9d2647a2546df6cc3fa85749d70c2fdfaf0b4dbbf41a5993a29e73976c", "I.3 internal target registry drift")
for path, (file_name, expected_blob) in EXPECTED_INTERNAL.items():
    target = product_root / file_name
    require(target.is_file(), f"I.3 Product internal target missing: {path}")
    if target.is_file():
        require(git_blob(target, product_root) == expected_blob, f"I.3 Product internal target blob drift: {path}")

require("sourcesRequired: true" in product_text, "I.3 Product sourcesRequired marker missing")
require('<h2 id="istochniki">' in product_text, "I.3 Product sources section missing")
require('<h2 id="literatura">' in product_text, "I.3 Product literature section missing")
require('<h2 id="spravka">' in product_text, "I.3 Product reference section missing")

require(len(reader_scan["scriptureReferences"]) == 13, "I.3 reader locator count drift")
require(reader_scan["inlineQuotationSegments"] + reader_scan["markdownBlockquotes"] + reader_scan["htmlBlockquotes"] == 0, "I.3 reader quotation surface detected")
require(len(reader_scan["externalLinks"]) == 0 and len(reader_scan["internalArticleLinks"]) == 0, "I.3 reader link detected")
require(reader_scan["footnoteDefinitions"] == 0, "I.3 reader footnote detected")

require(receipt.get("schemaVersion") == 2, "I.3 receipt schema drift")
require(receipt.get("authorityId") == "HEART-I3-CITATION-REVIEW-2026-08-04", "I.3 receipt authority drift")
require(receipt.get("disposition", {}).get("entryCitationPassComplete") is True, "I.3 entry citation pass not complete")
require(receipt.get("disposition", {}).get("remainingEntryBlockers") == [], "I.3 entry blockers remain")
require(receipt.get("disposition", {}).get("newDirectQuotesApproved") == 0, "I.3 new direct quote boundary drift")
require(receipt.get("effectiveCounts") == {
    "finalBookEntries": 18,
    "assembledReader": 8,
    "missingStandaloneFinalReaders": 10,
    "entryCitationPassComplete": 8,
    "entryCitationPassOpen": 10,
    "assembledReaderCitationReviewsComplete": 8,
    "productSourceOnly": 4,
    "researchDossierOnly": 6,
    "newDirectQuotesApproved": 0,
}, "I.3 effective count block drift")
require(receipt.get("publicationBoundary", {}).get("productSourceLinkRepairRequired") == 3, "I.3 Product repair boundary drift")
require(receipt.get("publicationBoundary", {}).get("wholeBookCitationPassComplete") is False, "whole-book citation pass falsely closed")
require(receipt.get("publicationBoundary", {}).get("productReleaseComplete") is False, "Product release falsely closed")

require(assembly.get("authorityId") == "HEART-I3-READER-ASSEMBLY-2026-08-04", "I.3 assembly authority drift")
require(current.get("currentCounts", {}).get("entryCitationPassComplete") == 7, "preceding V4 count drift")
triage_entry = next((row for row in triage.get("entries", []) if row.get("id") == "HEART-BOOK-I3"), {})
require(triage_entry.get("disposition", {}).get("triageState") == "TRIAGED_OPEN", "historical I.3 triage rewritten")

human = HUMAN_PATH.read_text(encoding="utf-8") if HUMAN_PATH.is_file() else ""
for marker in (
    "HEART-I3-CITATION-REVIEW-2026-08-04",
    "ENTRY CITATION PASSES COMPLETE = 8 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 8 / 8",
    "SCRIPTURE LOCATORS GOVERNED = 71 / 71",
    "QUOTATION SURFACES CLASSIFIED = 224 / 224",
    "EXTERNAL LINKS DISPOSITIONED = 15 / 15",
    "INTERNAL TARGETS RESOLVED = 3 / 3",
    "PRODUCT LINK REPAIRS REQUIRED = 3",
    "NEW DIRECT QUOTES APPROVED = 0",
):
    require(marker in human, f"I.3 human authority marker missing: {marker}")
for forbidden in (
    "DIRECT QUOTES APPROVED = 224",
    "PRODUCT LINK REPAIRS REQUIRED = 0",
    "WHOLE-BOOK CITATION PASS = COMPLETE",
    "PRODUCT RELEASE = COMPLETE",
    "TODO",
    "TBD",
):
    require(forbidden not in human, f"I.3 human authority contains forbidden marker: {forbidden}")

if errors:
    print(f"Heart I.3 entry citation pass: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "Heart I.3 entry citation pass: PASS — 71 Scripture locators, "
    "224 quotation surfaces, 15 external dispositions, 3 internal targets, "
    "3 Product link repairs retained, reader 13/0/0, whole-book 8/18"
)
