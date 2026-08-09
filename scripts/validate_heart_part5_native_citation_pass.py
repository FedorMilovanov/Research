#!/usr/bin/env python3
"""Validate the Part V citation pass against current native Product authority."""
from __future__ import annotations

import argparse
import hashlib
import html
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
RECEIPT = ROOT / "data/heart-part5-native-citation-review-2026-08-09.json"
V11 = ROOT / "data/heart-entry-citation-pass-current-v11-2026-08-09.json"
ASSEMBLY = ROOT / "data/heart-part5-reader-assembly-2026-08-09.json"
PART2 = ROOT / "data/heart-part2-citation-review-2026-08-04.json"
R3 = ROOT / "СЕРИЯ СЕРДЦЕ/65_R3_UNREGENERATE_STRUGGLE.md"
R4 = ROOT / "СЕРИЯ СЕРДЦЕ/66_R4_FOUR_SOILS.md"
R5 = ROOT / "СЕРИЯ СЕРДЦЕ/67_R5_TWO_STRUGGLES.md"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/133_READER_CHAPTER_V_HEART_IN_WAR_2026-08-09.md"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/136_PART5_NATIVE_ENTRY_CITATION_PASS_2026-08-09.md"
TEMP_WORKFLOW = ROOT / ".github/workflows/heart-part5-calibration-temp.yml"
TEMP_DISPOSITION = ROOT / "scripts/calibrate_heart_part5_dispositions_temp.py"
TEMP_READER_REF_WORKFLOW = ROOT / ".github/workflows/heart-part5-reader-ref-diagnostic-temp.yml"
TEMP_READER_REF_DIAGNOSTIC = ROOT / "scripts/diagnose_heart_part5_reader_refs_temp.py"
PRODUCT_REL = Path("src/components/article-pilots/rimlyanam7/Rimlyanam7Body.astro")
PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"
EXPECTED_BLOBS = {
    V11: "58e9dcf7f724b03c7b9d09b49f75922f8bf73b23",
    ASSEMBLY: "cf58624519e3f3ea7290fde518afce85f258863c",
    PART2: "c746a626953ee57a394a41a5f82a83630f1cd782",
    R3: "ae55b1fad5ccdb623c551a14222e0f51ec084a",
    R4: "f82780e13cb064aa89c06427d11a938662fc3ff8",
    R5: "846277b099e58bf36b88c2ae0dfe4e24e6bec53b",
    READER: "183819bf469d7e28f270fa6891b8ae1534e2f6ef",
}
EXPECTED_PRODUCT_BLOB = "35ed2f340ae725485533e322b3e1db0a68e01747"
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


def blob(root: Path, rel: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(rel)], cwd=root, text=True).strip()


def text_sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def json_sha(value: Any) -> str:
    return text_sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def normalize(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def heading_rows(text: str) -> list[tuple[int, str]]:
    rows = [(m.start(), normalize(m.group(2))) for m in re.finditer(r"(?m)^(#{1,4})\s+(.+?)\s*$", text)]
    rows += [(m.start(), normalize(m.group(1))) for m in re.finditer(r"<h[2-4]\b[^>]*>(.*?)</h[2-4]>", text, re.I | re.S)]
    return sorted(rows)


def heading_for(rows: list[tuple[int, str]], offset: int) -> str:
    current = "frontmatter-or-introduction"
    for pos, title in rows:
        if pos > offset:
            break
        current = title
    return current


def quote_rows(text: str) -> list[dict[str, Any]]:
    heads = heading_rows(text)
    found: list[dict[str, Any]] = []
    patterns = [
        ("RUSSIAN", re.compile(r"«([^»\n]{8,})»")),
        ("CURLY", re.compile(r"“([^”\n]{8,})”")),
        ("MD_BLOCK", re.compile(r"(?m)^\s*>\s?(\S.*)$")),
        ("HTML_BLOCK", re.compile(r"<blockquote[^>]*>(.*?)</blockquote>", re.I | re.S)),
    ]
    for surface_type, pattern in patterns:
        for match in pattern.finditer(text):
            value = normalize(match.group(1))
            found.append({
                "pos": match.start(),
                "section": heading_for(heads, match.start()),
                "type": surface_type,
                "sha256": text_sha(value),
                "chars": len(value),
            })
    found.sort(key=lambda row: int(row["pos"]))
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(found, 1):
        rows.append({"section": row["section"], "type": row["type"], "sha256": row["sha256"], "chars": row["chars"], "index": index})
    return rows


def section_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    buckets: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        buckets[str(row["section"])][str(row["type"])] += 1
    return {
        key: {"surfaces": sum(value.values()), "types": dict(sorted(value.items()))}
        for key, value in sorted(buckets.items())
    }


def classify_roles(rows: list[dict[str, Any]], mapping: dict[str, list[str]]) -> dict[str, int]:
    reverse = {section: role for role, sections in mapping.items() for section in sections}
    missing = sorted({str(row["section"]) for row in rows if str(row["section"]) not in reverse}, key=str.casefold)
    require(not missing, f"unmapped quotation sections: {missing}")
    return dict(sorted(Counter(reverse[str(row["section"])] for row in rows if str(row["section"]) in reverse).items()))


def r5_url_registry(text: str, urls: list[str], method: dict[str, Any]) -> list[dict[str, Any]]:
    heads = heading_rows(text)
    rows: list[dict[str, Any]] = []
    for raw_url in urls:
        canonical = raw_url[:-1] if raw_url.endswith("`") else raw_url
        occurrences: list[dict[str, Any]] = []
        cursor = 0
        while True:
            pos = text.find(raw_url, cursor)
            if pos < 0:
                break
            left = max(0, pos - 500)
            right = min(len(text), pos + len(raw_url) + 500)
            context = normalize(text[left:right])
            occurrences.append({
                "section": heading_for(heads, pos),
                "contextSha256": text_sha(context),
                "holdTerms": sorted([term for term in method["holdTerms"] if term.casefold() in context.casefold()], key=str.casefold),
                "verifiedTerms": sorted([term for term in method["verifiedTerms"] if term.casefold() in context.casefold()], key=str.casefold),
            })
            cursor = pos + 1
        if raw_url.endswith("`"):
            status = "MARKDOWN_CODE_DELIMITER_SCANNER_ARTIFACT"
        elif any(row["holdTerms"] for row in occurrences):
            status = "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD"
        elif any(row["verifiedTerms"] for row in occurrences):
            status = "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE"
        else:
            status = "DOSSIER_SUPPORT_RECORD_NO_READER_TRANSFER"
        rows.append({
            "rawUrl": raw_url,
            "canonicalUrl": canonical,
            "status": status,
            "occurrences": len(occurrences),
            "sections": sorted({str(row["section"]) for row in occurrences}, key=str.casefold),
            "contexts": occurrences,
            "readerTransfer": False,
            "bulkDirectQuoteApproval": False,
        })
    return rows


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()
product_path = product_root / PRODUCT_REL

for path, expected in EXPECTED_BLOBS.items():
    require(path.is_file(), f"immutable authority missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(ROOT, path.relative_to(ROOT)) == expected, f"immutable authority blob drift: {path.relative_to(ROOT)}")
require(product_path.is_file(), f"Product native owner missing: {PRODUCT_REL}")
if product_path.is_file():
    require(blob(product_root, PRODUCT_REL) == EXPECTED_PRODUCT_BLOB, "Product native Romans 7 blob drift")
require(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=product_root, text=True).strip() == PRODUCT_COMMIT, "Product snapshot drift")
require(not TEMP_WORKFLOW.exists(), "temporary calibration workflow must not exist in final tree")
require(not TEMP_DISPOSITION.exists(), "temporary disposition calibrator must not exist in final tree")
require(not TEMP_READER_REF_WORKFLOW.exists(), "temporary reader-ref workflow must not exist in final tree")
require(not TEMP_READER_REF_DIAGNOSTIC.exists(), "temporary reader-ref diagnostic must not exist in final tree")

receipt = read_json(RECEIPT)
v11 = read_json(V11)
assembly = read_json(ASSEMBLY)
part2 = read_json(PART2)
require(receipt.get("authorityId") == "HEART-PART5-NATIVE-CITATION-REVIEW-2026-08-09", "Part V receipt authority drift")
require(receipt.get("entry", {}).get("id") == "HEART-BOOK-V", "Part V receipt entry drift")
require(receipt.get("entry", {}).get("order") == 11, "Part V receipt order drift")
require(v11.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V11-2026-08-09", "V11 authority drift")
require(v11.get("currentCounts", {}).get("entryCitationPassComplete") == 6, "V11 must remain 6/18 before Part V delta")
require(assembly.get("authorityId") == "HEART-PART5-READER-ASSEMBLY-2026-08-09", "Part V assembly authority drift")
require(part2.get("authorityId") == "HEART-PART2-CITATION-REVIEW-2026-08-04", "Part II reuse authority drift")

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
owners = {
    "PRODUCT_NATIVE": (product_path, module.p(str(PRODUCT_REL), "native Romans 7 Body")),
    "R3": (R3, module.r(str(R3.relative_to(ROOT)), "R3 support")),
    "R4": (R4, module.r(str(R4.relative_to(ROOT)), "R4 support")),
    "R5": (R5, module.r(str(R5.relative_to(ROOT)), "R5 support")),
}
texts: dict[str, str] = {}
scans: dict[str, dict[str, Any]] = {}
quotes: dict[str, list[dict[str, Any]]] = {}
for name, (path, owner_spec) in owners.items():
    texts[name] = path.read_text(encoding="utf-8")
    scans[name] = module.scan_owner(owner_spec, product_root)
    quotes[name] = quote_rows(texts[name])
    expected_count = scans[name]["inlineQuotationSegments"] + scans[name]["markdownBlockquotes"] + scans[name]["htmlBlockquotes"]
    require(len(quotes[name]) == expected_count, f"{name} quotation scanner drift")

inventory = receipt.get("surfaceInventory", {})
expected_per_owner = inventory.get("perOwner", {})
for name in owners:
    scan = scans[name]
    rows = quotes[name]
    actual = {
        "scriptureReferences": len(scan["scriptureReferences"]),
        "quotationSurfaces": len(rows),
        "externalLinks": len(scan["externalLinks"]),
        "internalArticleLinks": len(scan["internalArticleLinks"]),
        "scriptureSha256": json_sha(sorted(scan["scriptureReferences"], key=str.casefold)),
        "quotationManifestSha256": json_sha(rows),
    }
    expected = expected_per_owner.get(name, {})
    for key, value in actual.items():
        require(expected.get(key) == value, f"{name} {key} drift")
    if name in {"PRODUCT_NATIVE", "R5"}:
        require(expected.get("externalLinksSha256") == json_sha(sorted(scan["externalLinks"], key=str.casefold)), f"{name} external-link set drift")
        require(expected.get("sectionSummarySha256") == json_sha(section_summary(rows)), f"{name} section-summary drift")

union_refs = sorted({value for scan in scans.values() for value in scan["scriptureReferences"]}, key=str.casefold)
union_urls = sorted({value for scan in scans.values() for value in scan["externalLinks"]}, key=str.casefold)
union_internal = sorted({value for scan in scans.values() for value in scan["internalArticleLinks"]}, key=str.casefold)
all_quote_rows = [{"owner": name, **row} for name in owners for row in quotes[name]]
aggregate = inventory.get("aggregate", {})
require(aggregate.get("uniqueScriptureReferences") == len(union_refs) == 203, "Part V Scripture union count drift")
require(aggregate.get("quotationSurfaces") == len(all_quote_rows) == 755, "Part V quotation union count drift")
require(aggregate.get("uniqueExternalLinks") == len(union_urls) == 122, "Part V external-link union count drift")
require(aggregate.get("uniqueInternalArticleLinks") == len(union_internal) == 1, "Part V internal-link union count drift")
require(aggregate.get("scriptureSetSha256") == json_sha(union_refs), "Part V Scripture union hash drift")
require(aggregate.get("quotationManifestSha256") == json_sha(all_quote_rows), "Part V quotation manifest drift")
require(aggregate.get("externalLinkSetSha256") == json_sha(union_urls), "Part V external-link union hash drift")
require(aggregate.get("internalLinkSetSha256") == json_sha(union_internal), "Part V internal-link union hash drift")

quote_review = receipt.get("quotationReview", {})
for owner_key, data_key in (("PRODUCT_NATIVE", "productNative"), ("R5", "r5")):
    review = quote_review.get(data_key, {})
    mapping = review.get("roleSectionMap", {})
    require(review.get("roleMapSha256") == json_sha(mapping), f"{owner_key} role-map hash drift")
    require(review.get("roleCounts") == classify_roles(quotes[owner_key], mapping), f"{owner_key} role-count drift")
require(quote_review.get("bulkDirectQuotationApproval") is False, "Part V bulk direct-quote approval must remain false")
require(quote_review.get("newDirectQuotesApproved") == 0, "Part V new direct quotes must remain zero")

reuse = quote_review.get("r3r4Reuse", {})
part2_review = part2.get("fullOwnerReview", {})
require(reuse.get("authorityId") == part2.get("authorityId"), "R3/R4 reuse authority mismatch")
require(reuse.get("sourceSurfaceBaseManifestSha256") == part2_review.get("sourceSurfaceBaseManifestSha256"), "R3/R4 base manifest reuse drift")
require(reuse.get("classifiedSurfaceManifestSha256") == part2_review.get("classifiedSurfaceManifestSha256"), "R3/R4 classified manifest reuse drift")
require(reuse.get("roleCounts") == part2_review.get("quotationRoleCounts"), "R3/R4 role-count reuse drift")
require(reuse.get("reuseAllowedOnlyWithExactR3R4Blobs") is True, "R3/R4 reuse must stay exact-blob-only")

links = receipt.get("externalLinkReview", {})
product_registry = [
    {"url": url, "status": "NON_CITATION_UI_OR_SCHEMA_URL", "readerTransfer": False}
    for url in sorted(scans["PRODUCT_NATIVE"]["externalLinks"], key=str.casefold)
]
require(links.get("productNative", {}).get("statusCounts") == {"NON_CITATION_UI_OR_SCHEMA_URL": 3}, "Product native URL status drift")
require(links.get("productNative", {}).get("registrySha256") == json_sha(product_registry), "Product native URL registry drift")
method = part2.get("externalLinkReview", {}).get("method", {})
r5_registry = r5_url_registry(texts["R5"], sorted(scans["R5"]["externalLinks"], key=str.casefold), method)
r5_status_counts = dict(sorted(Counter(row["status"] for row in r5_registry).items()))
require(links.get("r5", {}).get("linksDispositioned") == len(r5_registry) == 39, "R5 URL count drift")
require(links.get("r5", {}).get("urlOccurrences") == sum(int(row["occurrences"]) for row in r5_registry) == 54, "R5 URL occurrence drift")
require(links.get("r5", {}).get("statusCounts") == r5_status_counts == {
    "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD": 12,
    "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE": 26,
    "MARKDOWN_CODE_DELIMITER_SCANNER_ARTIFACT": 1,
}, "R5 URL status drift")
require(links.get("r5", {}).get("registrySha256") == json_sha(r5_registry), "R5 URL disposition registry drift")
artifact = links.get("r5", {}).get("scannerArtifact", {})
require(artifact.get("raw") == "https://ccel.org/ccel/edwards/affections.toc.html`", "R5 scanner artifact raw token drift")
require(artifact.get("canonical") == "https://ccel.org/ccel/edwards/affections.toc.html", "R5 scanner artifact canonical URL drift")
part2_links = part2.get("externalLinkReview", {})
require(links.get("r3r4Reuse", {}).get("linksDispositioned") == part2_links.get("linksDispositioned") == 80, "R3/R4 URL reuse count drift")
require(links.get("r3r4Reuse", {}).get("statusCounts") == part2_links.get("statusCounts"), "R3/R4 URL status reuse drift")
require(links.get("r3r4Reuse", {}).get("registrySha256") == part2_links.get("dispositionRegistrySha256"), "R3/R4 URL registry reuse drift")

internal = receipt.get("internalLinkReview", {})
require(union_internal == ["/articles/opinion/"], "Part V internal-link union drift")
require(internal.get("path") == "/articles/opinion/" and internal.get("owner") == "R3", "Part V unresolved internal-link owner drift")
require(internal.get("newUnresolvedInternalPathsAdded") == 0, "Part V must not add unresolved internal paths")
require(internal.get("readerTransfer") is False, "Part V unresolved internal path transferred to reader")

reader_scan = module.scan_owner(module.r(str(READER.relative_to(ROOT)), "Part V reader"), product_root)
reader_review = receipt.get("readerReview", {})
require(reader_scan["inlineQuotationSegments"] + reader_scan["markdownBlockquotes"] + reader_scan["htmlBlockquotes"] == reader_review.get("quotationSurfaces") == 0, "Part V reader quotation boundary drift")
require(len(reader_scan["externalLinks"]) == reader_review.get("externalLinks") == 0, "Part V reader external-link boundary drift")
require(len(reader_scan["internalArticleLinks"]) == reader_review.get("internalArticleLinks") == 0, "Part V reader internal-link boundary drift")
require(reader_scan["footnoteDefinitions"] == reader_review.get("footnoteDefinitions") == 0, "Part V reader footnote boundary drift")
reader_refs = set(reader_scan["scriptureReferences"])
reader_only_refs = reader_refs - set(union_refs)
expected_reader_only_refs = {"1 Ин.1:8–2", "Гал.5", "Еф.6", "Кол.3"}
require(len(reader_refs) == reader_review.get("scriptureReferencesDetected") == 19, "Part V reader Scripture count drift")
require(len(reader_refs & set(union_refs)) == reader_review.get("ownerUnionExactMatches") == 15, "Part V reader owner-union exact-match count drift")
require(reader_review.get("readerOnlyScriptureReferencesMustBeExplicitlyDispositioned") is True, "Part V reader-only Scripture disposition boundary drift")
require(reader_only_refs == expected_reader_only_refs, f"Part V reader-only Scripture set drift: {sorted(reader_only_refs, key=str.casefold)}")
reader_only_rows = reader_review.get("readerOnlyScriptureReferences", [])
require(isinstance(reader_only_rows, list) and len(reader_only_rows) == 4, "Part V reader-only Scripture disposition count drift")
row_by_ref = {
    str(row.get("reference")): row
    for row in reader_only_rows
    if isinstance(row, dict) and row.get("reference")
}
require(set(row_by_ref) == expected_reader_only_refs, "Part V reader-only Scripture disposition registry drift")
reader_text = READER.read_text(encoding="utf-8")
for reference in sorted(expected_reader_only_refs, key=str.casefold):
    row = row_by_ref.get(reference, {})
    require(bool(row.get("role")), f"Part V reader-only Scripture role missing: {reference}")
    marker = str(row.get("contextMarker", ""))
    require(bool(marker) and marker in reader_text, f"Part V reader-only Scripture context marker drift: {reference}")
    require(row.get("sourceQuotationTransfer") == 0, f"Part V reader-only Scripture quote transfer drift: {reference}")
    require(row.get("sourceLinkTransfer") == 0, f"Part V reader-only Scripture link transfer drift: {reference}")
    if reference == "Гал.5":
        require(row.get("status") == "COVERED_ALIAS_OF_REVIEWED_OWNER_REFERENCE", "Part V Galatians 5 alias status drift")
        require(row.get("coveredBy") == "Гал.5:16–25", "Part V Galatians 5 alias target drift")
        require(row.get("coveredBy") in set(union_refs), "Part V Galatians 5 alias target escaped owner union")
    else:
        require(row.get("status") == "READER_ONLY_SCRIPTURE_LOCATOR_REVIEWED", f"Part V reader-only Scripture review status drift: {reference}")
require(reader_review.get("sourceQuotationTransfer") == 0 and reader_review.get("sourceLinkTransfer") == 0, "Part V reader source transfer drift")
require(reader_review.get("newDirectQuotesApproved") == 0, "Part V reader approves new direct quotes")

backlog = receipt.get("retainedRepairAndHoldBacklog", {})
require(backlog == {
    "historicalProductSourceRepairsRequired": 4,
    "historicalDossierUrlHoldsRetained": 55,
    "part5DossierUrlHoldsAdded": 12,
    "currentDossierUrlHoldsRetained": 67,
    "dossierSourceUrlRepairsRequired": 2,
    "part5NewSourceUrlRepairs": 0,
    "unresolvedInternalPathsRetained": 1,
    "part5NewUnresolvedInternalPaths": 0,
    "nativeSourceAuthorityReconciliationsOpen": 7,
    "silentlyClosedItems": 0,
}, "Part V retained backlog drift")
require(receipt.get("disposition", {}).get("entryCitationPassComplete") is True, "Part V pass not complete")
require(receipt.get("disposition", {}).get("assembledReaderCitationReviewComplete") is True, "Part V reader review not complete")
require(receipt.get("disposition", {}).get("newDirectQuotesApproved") == 0, "Part V disposition approves new quotes")

require(HUMAN.is_file(), "Part V human mirror missing")
if HUMAN.is_file():
    human = HUMAN.read_text(encoding="utf-8")
    for marker in (
        "203 unique Scripture refs / 755 quotation surfaces / 122 unique external URLs / 1 internal article path",
        "CURRENT DOSSIER URL HOLDS = 67 = 55 retained + 12 Part V",
        "CURRENT NATIVE-AUTHORITY CITATION PASSES COMPLETE = 7 / 18",
        "4 reader-only Scripture locators dispositioned explicitly",
        "new direct quotes approved: **0**",
        "HEART-BOOK-X2 NATIVE SOURCE AUTHORITY RECONCILIATION",
    ):
        require(marker in human, f"Part V human mirror missing marker: {marker}")

if errors:
    print("Heart Part V native citation pass: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Heart Part V native citation pass: PASS — native Product + R3/R4/R5 203/755/122/1 governed; R5 adds 12 holds; current delta ready 6→7")
