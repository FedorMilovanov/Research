#!/usr/bin/env python3
"""Validate the completed Part IV entry citation pass."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
SOURCE = ROOT / "СЕРИЯ СЕРДЦЕ/68_R7A_WORD_AND_HEART.md"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/129_READER_CHAPTER_IV_HEART_AND_WORD_2026-08-04.md"
ASSEMBLY = ROOT / "data/heart-part4-reader-assembly-2026-08-04.json"
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v9-2026-08-04.json"
RECEIPT = ROOT / "data/heart-part4-citation-review-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/131_PART4_ENTRY_CITATION_PASS_2026-08-04.md"
WORKFLOW = ROOT / ".github/workflows/heart-reader-assembly.yml"
EXPECTED_BLOBS = {
    SOURCE: "ceff41072982c664606bc377ef8f1f0f241677da",
    READER: "55eda03de3cc29e7946a705fe0fffbd2acc4e36d",
    ASSEMBLY: "58f0922734601cf9cf16e448d50836b269b624e0",
    CURRENT: "d8a65b5233a471e024f5642e1dc3d1a50f13babf",
    BUILDER: "6e8fb1af57bc72d26a9ca91d5b84b1fec3de7f12",
}
SOURCE_SHA = "420e5fd82739edcd77258440125fa65dd4a6c8cf36e5377e32a3c2e143285089"
READER_SHA = "b3a103936c9495484a2a5478262ec4d4e47ab49f5192dd523add1deeb7d23d58"
MANIFEST_HASHES = {
    "scriptureReferenceSetSha256": "f7539fc92fd79dc29d4ba97bad1e43a173cf6d77a77006ea1a77a08059224b3a",
    "sourceSurfaceBaseManifestSha256": "95ebde518aff552e30f1c08b2ce659f9c75d334cf285c2263be9f9561170d581",
    "classifiedSurfaceManifestSha256": "7adb959304e297d8a57ce3cb43755c38c2ed2df3b06f7acce6766c7d2fe00e32",
    "roleSectionMapSha256": "1176f36eac7ed7e182b4ec0304c6ccc4105c62baf356c285421466d1138bf8e5",
    "sectionSummarySha256": "de421a44aa20c53c52992c990ccea1b5ddc9eaac8165d2595a4ad9a39b5201df",
    "externalLinkSetSha256": "452a0db94764d231a3f8798368c71d624c98fae30825a94e68c98b4f168b4219",
    "internalLinkSetSha256": "26f4a242663e5d878d4b09e33890abddf605a0cbcdda9c653c1e41cd6849c0d3",
}
ROLE_COUNTS = {
    "ATTRIBUTED_WITNESS_OR_SOURCE_BANK_SURFACE": 91,
    "EDITORIAL_STRUCTURAL_OR_CAUTION_SURFACE": 18,
    "EXEGETICAL_SCRIPTURE_OR_DOCTRINAL_SURFACE": 116,
}
URL_COUNTS = {
    "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD": 9,
    "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE": 27,
}
URL_REGISTRY_SHA = "9bd28bb0399e0de1abb4078a82bb07de311710ba04fb29a01cc36dee9014f493"
INTERNAL_REGISTRY_SHA = "57286008310028af6aeffd85d6d5c6d1cf0251d2d0594febd55e0589823f73c8"
EXPECTED_COUNTS = {
    "finalBookEntries": 18,
    "entryCitationPassComplete": 13,
    "entryCitationPassOpen": 5,
    "assembledReaders": 13,
    "assembledReaderCitationReviewsComplete": 13,
    "missingStandaloneFinalReaders": 5,
    "productSourceOnlyEntries": 2,
    "researchDossierOnlyEntries": 3,
    "productSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 55,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "newDirectQuotesApproved": 0,
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


def blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def text_sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def json_sha(value: Any, *, sort_keys: bool = False) -> str:
    return text_sha(json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=sort_keys))


def normalize(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def qcount(scan: dict[str, Any]) -> int:
    return scan["inlineQuotationSegments"] + scan["markdownBlockquotes"] + scan["htmlBlockquotes"]


def headings(text: str) -> list[dict[str, Any]]:
    return [
        {"offset": match.start(), "level": len(match.group(1)), "title": match.group(2).strip()}
        for match in re.finditer(r"(?m)^(#{1,4})\s+(.+?)\s*$", text)
    ]


def heading_for(rows: list[dict[str, Any]], offset: int) -> str:
    current = "frontmatter-or-introduction"
    for row in rows:
        if row["offset"] > offset:
            break
        current = str(row["title"])
    return current


def extract_surfaces(text: str, module: Any) -> list[dict[str, Any]]:
    heading_rows = headings(text)
    rows: list[dict[str, Any]] = []
    patterns = [
        ("RUSSIAN", re.compile(r"«([^»\n]{8,})»")),
        ("CURLY", re.compile(r"“([^”\n]{8,})”")),
        ("MD_BLOCK", re.compile(r"(?m)^\s*>\s?(\S.*)$")),
        ("HTML_BLOCK", re.compile(r"<blockquote[^>]*>(.*?)</blockquote>", re.S | re.I)),
    ]
    for surface_type, pattern in patterns:
        for match in pattern.finditer(text):
            value = normalize(match.group(1))
            section = heading_for(heading_rows, match.start())
            left = max(0, match.start() - 300)
            right = min(len(text), match.end() + 300)
            nearby = sorted(
                {module.normalize_ref(item.group(0)) for item in module.SCRIPTURE_RE.finditer(text[left:right])},
                key=str.casefold,
            )
            rows.append({
                "position": match.start(),
                "section": section,
                "type": surface_type,
                "sha256": text_sha(value),
                "chars": len(value),
                "nearbyScripture": nearby,
            })
    rows.sort(key=lambda row: int(row["position"]))
    for index, row in enumerate(rows, start=1):
        row["surfaceIndex"] = index
        del row["position"]
    return rows


def contexts_for_url(text: str, url: str, method: dict[str, Any]) -> list[dict[str, Any]]:
    heading_rows = headings(text)
    rows: list[dict[str, Any]] = []
    cursor = 0
    while True:
        offset = text.find(url, cursor)
        if offset < 0:
            break
        left = max(0, offset - 500)
        right = min(len(text), offset + len(url) + 500)
        context = normalize(text[left:right])
        rows.append({
            "section": heading_for(heading_rows, offset),
            "contextSha256": text_sha(context),
            "holdTerms": sorted({term for term in method["holdTerms"] if term.casefold() in context.casefold()}, key=str.casefold),
            "verifiedTerms": sorted({term for term in method["verifiedTerms"] if term.casefold() in context.casefold()}, key=str.casefold),
        })
        cursor = offset + 1
    return rows


def classify_url(contexts: list[dict[str, Any]], fallback: str) -> str:
    if any(row["holdTerms"] for row in contexts) or any("Открытые вопросы" in row["section"] for row in contexts):
        return "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD"
    if any(row["verifiedTerms"] for row in contexts):
        return "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE"
    return fallback


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()

for path, expected in EXPECTED_BLOBS.items():
    require(path.is_file(), f"immutable authority missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(path) == expected, f"immutable authority blob drift: {path.relative_to(ROOT)}")

receipt = read_json(RECEIPT)
assembly = read_json(ASSEMBLY)
current = read_json(CURRENT)
source_text = SOURCE.read_text(encoding="utf-8") if SOURCE.is_file() else ""
reader_text = READER.read_text(encoding="utf-8") if READER.is_file() else ""
require(text_sha(source_text) == SOURCE_SHA, "Part IV source SHA drift")
require(text_sha(reader_text) == READER_SHA, "Part IV reader SHA drift")

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
source_scan = module.scan_owner(module.r(str(SOURCE.relative_to(ROOT)), "Part IV R7a owner"), product_root)
reader_scan = module.scan_owner(module.r(str(READER.relative_to(ROOT)), "Part IV reader"), product_root)
refs = sorted(source_scan["scriptureReferences"], key=str.casefold)
urls = sorted(source_scan["externalLinks"], key=str.casefold)
internal_paths = sorted(source_scan["internalArticleLinks"], key=str.casefold)
surfaces = extract_surfaces(source_text, module)
base_manifest = [
    {key: row[key] for key in ("surfaceIndex", "section", "type", "sha256", "chars", "nearbyScripture")}
    for row in surfaces
]
role_map = receipt.get("fullOwnerReview", {}).get("roleSectionMap", {})
classified_manifest: list[dict[str, Any]] = []
for row in base_manifest:
    assigned = ""
    for role_name, sections in role_map.items():
        if row["section"] in sections:
            assigned = role_name
            break
    require(bool(assigned), f"Part IV unmapped quotation section: {row['section']}")
    classified_manifest.append({**row, "class": assigned})
section_summary: dict[str, dict[str, Any]] = {}
for row in classified_manifest:
    bucket = section_summary.setdefault(row["section"], {"surfaces": 0, "classes": Counter(), "types": Counter()})
    bucket["surfaces"] += 1
    bucket["classes"][row["class"]] += 1
    bucket["types"][row["type"]] += 1
section_summary = {
    key: {
        "surfaces": value["surfaces"],
        "classes": dict(sorted(value["classes"].items())),
        "types": dict(sorted(value["types"].items())),
    }
    for key, value in sorted(section_summary.items())
}
actual_hashes = {
    "scriptureReferenceSetSha256": json_sha(refs),
    "sourceSurfaceBaseManifestSha256": json_sha(base_manifest),
    "classifiedSurfaceManifestSha256": json_sha(classified_manifest),
    "roleSectionMapSha256": json_sha(role_map, sort_keys=True),
    "sectionSummarySha256": json_sha(section_summary, sort_keys=True),
    "externalLinkSetSha256": json_sha(urls),
    "internalLinkSetSha256": json_sha(internal_paths),
}
require((len(refs), len(surfaces), len(urls), len(internal_paths)) == (65, 225, 36, 2), "Part IV source surface count drift")
require(qcount(source_scan) == 225, "Part IV source quotation scanner drift")
require(actual_hashes == MANIFEST_HASHES, "Part IV manifest hash drift")
require(dict(sorted(Counter(row["class"] for row in classified_manifest).items())) == ROLE_COUNTS, "Part IV role-count drift")

link_review = receipt.get("externalLinkReview", {})
method = link_review.get("method", {})
url_registry: list[dict[str, Any]] = []
for url in urls:
    contexts = contexts_for_url(source_text, url, method)
    url_registry.append({
        "url": url,
        "status": classify_url(contexts, method.get("fallback", "")),
        "occurrences": len(contexts),
        "sections": sorted({row["section"] for row in contexts}, key=str.casefold),
        "contexts": contexts,
        "readerTransfer": False,
        "directQuoteBulkApproval": False,
    })
require(sum(row["occurrences"] for row in url_registry) == 40, "Part IV URL occurrence drift")
require(dict(sorted(Counter(row["status"] for row in url_registry).items())) == URL_COUNTS, "Part IV URL status-count drift")
require(json_sha(url_registry, sort_keys=True) == URL_REGISTRY_SHA, "Part IV URL registry drift")

internal_registry: list[dict[str, Any]] = []
for path in internal_paths:
    containing_urls = sorted([url for url in urls if path in url], key=str.casefold)
    if containing_urls:
        internal_registry.append({
            "path": path,
            "status": "EXTERNAL_URL_PATH_FRAGMENT_FALSE_POSITIVE",
            "containingExternalUrls": containing_urls,
            "productTargetChecked": False,
            "readerTransfer": False,
        })
    else:
        slug = path.removeprefix("/articles/").removesuffix("/")
        target = Path("src/content/articles") / f"{slug}.mdx"
        target_path = product_root / target
        internal_registry.append({
            "path": path,
            "status": "PINNED_PRODUCT_TARGET_EXISTS" if target_path.is_file() else "UNRESOLVED_PRODUCT_TARGET",
            "target": str(target),
            "exists": target_path.is_file(),
            "targetBlob": subprocess.check_output(["git", "hash-object", str(target)], cwd=product_root, text=True).strip() if target_path.is_file() else None,
            "readerTransfer": False,
        })
require(json_sha(internal_registry, sort_keys=True) == INTERNAL_REGISTRY_SHA, "Part IV internal registry drift")
require(internal_registry == receipt.get("internalLinkReview", {}).get("registry"), "Part IV internal disposition receipt drift")
require(all(row.get("status") == "EXTERNAL_URL_PATH_FRAGMENT_FALSE_POSITIVE" for row in internal_registry), "Part IV internal detection is not a false positive")

require((
    len(re.findall(r"(?u)\b[\wЁёА-Яа-я]+\b", reader_text)),
    len(reader_scan["scriptureReferences"]), qcount(reader_scan),
    len(reader_scan["externalLinks"]), len(reader_scan["internalArticleLinks"]),
    reader_scan["footnoteDefinitions"], len(reader_scan["sourceHeadings"]),
) == (1580, 18, 0, 0, 0, 0, 0), "Part IV reader review drift")

require(receipt.get("authorityId") == "HEART-PART4-CITATION-REVIEW-2026-08-04", "Part IV receipt authority drift")
require(receipt.get("status") == "PART4_ENTRY_CITATION_PASS_COMPLETE_ALL_THIRTEEN_READERS_REVIEWED_ZERO_NEW_DIRECT_QUOTES", "Part IV receipt status drift")
require(receipt.get("fullOwnerReview", {}).get("quotationRoleCounts") == ROLE_COUNTS, "Part IV receipt role-count drift")
require(receipt.get("externalLinkReview", {}).get("statusCounts") == URL_COUNTS, "Part IV receipt URL-count drift")
require(receipt.get("externalLinkReview", {}).get("supportOnlyLinks") == 0, "Part IV unexpected support-only links")
require(receipt.get("externalLinkReview", {}).get("sourceUrlRepairsAdded") == 0, "Part IV unexpectedly adds URL repairs")
require(receipt.get("internalLinkReview", {}).get("newUnresolvedInternalPaths") == 0, "Part IV unexpectedly adds unresolved paths")
require(receipt.get("retainedRepairAndHoldBacklog") == {
    "productSourceRepairsRequired": 4,
    "precedingDossierUrlHoldsRetained": 46,
    "part4DossierUrlHoldsAdded": 9,
    "currentDossierUrlHoldsRetained": 55,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "part4NewUnresolvedInternalPaths": 0,
}, "Part IV retained backlog drift")
require(receipt.get("effectiveState") == {
    "entryCitationPassComplete": True,
    "assembledReaderCitationReviewComplete": True,
    "sourceQuotationSurfacesCopiedToReader": 0,
    "sourceLinksCopiedToReader": 0,
    "newDirectQuotesApproved": 0,
}, "Part IV effective-state drift")
require(receipt.get("effectiveCounts") == EXPECTED_COUNTS, "Part IV effective-count drift")
require(receipt.get("nextTransaction") == "Compose a separate versioned current V10 authority from immutable current V9 plus this Part IV citation receipt.", "Part IV next-transaction drift")

require(assembly.get("authorityId") == "HEART-PART4-READER-ASSEMBLY-2026-08-04", "Part IV assembly authority drift")
require(assembly.get("effectiveCounts", {}).get("assembledReaders") == 13, "Part IV assembly reader count drift")
require(assembly.get("effectiveCounts", {}).get("entryCitationPassComplete") == 12, "Part IV assembly must retain pre-review citation count")
require(assembly.get("publicationBoundary", {}).get("part4EntryCitationPassComplete") is False, "Part IV assembly falsely claims citation completion")
require(current.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V9-2026-08-04", "current V9 authority drift")

publication = receipt.get("publicationBoundary", {})
require(publication.get("part4EntryCitationPassComplete") is True, "Part IV citation pass incomplete")
require(publication.get("allCurrentlyAssembledReadersReviewed") is True, "Part IV reader-review state drift")
for key in (
    "wholeBookReaderAssemblyComplete", "wholeBookCitationPassComplete",
    "wholeBookTransitionDedupPassComplete", "wholeBookLineEditComplete",
    "manuscriptBundleComplete", "productReleaseComplete", "productSourceRepairsComplete",
    "dossierUrlHoldsResolved", "dossierSourceUrlRepairsComplete", "unresolvedInternalPathsResolved",
):
    require(publication.get(key) is False, f"Part IV falsely closes {key}")

human = HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for marker in (
    "HEART-PART4-CITATION-REVIEW-2026-08-04",
    "SCRIPTURE REFERENCES GOVERNED = 65 / 65",
    "QUOTATION SURFACES CLASSIFIED = 225 / 225",
    "EXEGETICAL / DOCTRINAL SURFACES = 116",
    "ATTRIBUTED WITNESS SURFACES = 91",
    "EDITORIAL / CAUTION SURFACES = 18",
    "EXTERNAL LINKS DISPOSITIONED = 36 / 36",
    "VERIFIED OR SAFE CLOSURE LINKS = 27",
    "OPEN OR DIRECT-QUOTE HOLDS = 9",
    "INTERNAL PATH FALSE POSITIVES = 2 / 2",
    "READER QUOTATION SURFACES = 0",
    "READER LINKS = 0",
    "ENTRY CITATION PASSES COMPLETE = 13 / 18",
    "ASSEMBLED READER CITATION REVIEWS = 13 / 13",
    "DOSSIER URL HOLDS RETAINED = 55",
    "NEXT TRANSACTION = CURRENT V10 COMPOSITION",
    EXPECTED_BLOBS[SOURCE], EXPECTED_BLOBS[READER], EXPECTED_BLOBS[ASSEMBLY], EXPECTED_BLOBS[CURRENT],
):
    require(marker in human, f"Part IV human authority marker missing: {marker}")
for forbidden in (
    "ENTRY CITATION PASSES COMPLETE = 18 / 18", "DOSSIER URL HOLDS RETAINED = 0",
    "WHOLE-BOOK READER ASSEMBLY = COMPLETE", "WHOLE-BOOK CITATION PASS = COMPLETE",
    "PRODUCT RELEASE = COMPLETE", "TODO", "TBD",
):
    require(forbidden not in human, f"Part IV human authority contains forbidden marker: {forbidden}")
workflow = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.is_file() else ""
require("validate_heart_part4_entry_citation_pass.py" in workflow, "Part IV citation workflow gate missing")
require("diagnose_heart_part4_citation.py" not in workflow, "Part IV diagnostic leaked into permanent workflow")
require(not (ROOT / "scripts/diagnose_heart_part4_citation.py").exists(), "temporary Part IV diagnostic script remains")
require(not (ROOT / ".github/workflows/diagnose-heart-part4-citation.yml").exists(), "temporary Part IV diagnostic workflow remains")

if errors:
    print(f"Heart Part IV citation pass: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Heart Part IV citation pass: PASS — 65/225/36/2 governed, roles 116/91/18, links 27/9, false positives 2/2, reviews 13/13")
