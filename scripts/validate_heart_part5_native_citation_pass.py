#!/usr/bin/env python3
"""Red-first calibration for the Part V native-authority citation pass."""
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
PART2 = ROOT / "data/heart-part2-citation-review-2026-08-04.json"
V11 = ROOT / "data/heart-entry-citation-pass-current-v11-2026-08-09.json"
ASSEMBLY = ROOT / "data/heart-part5-reader-assembly-2026-08-09.json"
R3 = ROOT / "СЕРИЯ СЕРДЦЕ/65_R3_UNREGENERATE_STRUGGLE.md"
R4 = ROOT / "СЕРИЯ СЕРДЦЕ/66_R4_FOUR_SOILS.md"
R5 = ROOT / "СЕРИЯ СЕРДЦЕ/67_R5_TWO_STRUGGLES.md"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/133_READER_CHAPTER_V_HEART_IN_WAR_2026-08-09.md"
PRODUCT_REL = Path("src/components/article-pilots/rimlyanam7/Rimlyanam7Body.astro")
PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"
EXPECTED_BLOBS = {
    R3: "ae55b1fad5cccbdb623c551a14222e0f51ec084a",
    R4: "f82780e13cb064aa89c06427d11a938662fc3ff8",
    R5: "846277b099e58bf36b88c2ae0dfe4e24e6bec53b",
    READER: "183819bf469d7e28f270fa6891b8ae1534e2f6ef",
    PART2: "d3a156bbbf67a3c45d1a019ab1ffc7da261ad692",
    V11: "58e9dcf7f724b03c7b9d09b49f75922f8bf73b23",
    ASSEMBLY: "cf58624519e3f3ea7290fde518afce85f258863c",
}
EXPECTED_PRODUCT_BLOB = "35ed2f340ae725485533e322b3e1db0a68e01747"


def blob(root: Path, rel: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(rel)], cwd=root, text=True).strip()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha_json(value: Any) -> str:
    return sha_text(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def normalize(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def heading_rows(text: str) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    for m in re.finditer(r"(?m)^(#{1,4})\s+(.+?)\s*$", text):
        rows.append((m.start(), normalize(m.group(2))))
    for m in re.finditer(r"<h[2-4]\b[^>]*>(.*?)</h[2-4]>", text, re.I | re.S):
        rows.append((m.start(), normalize(m.group(1))))
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
    out: list[dict[str, Any]] = []
    patterns = [
        ("RUSSIAN", re.compile(r"«([^»\n]{8,})»")),
        ("CURLY", re.compile(r"“([^”\n]{8,})”")),
        ("MD_BLOCK", re.compile(r"(?m)^\s*>\s?(\S.*)$")),
        ("HTML_BLOCK", re.compile(r"<blockquote[^>]*>(.*?)</blockquote>", re.I | re.S)),
    ]
    for typ, pattern in patterns:
        for m in pattern.finditer(text):
            value = normalize(m.group(1))
            out.append({"pos": m.start(), "section": heading_for(heads, m.start()), "type": typ, "sha256": sha_text(value), "chars": len(value)})
    out.sort(key=lambda row: int(row["pos"]))
    for i, row in enumerate(out, 1):
        row["index"] = i
        del row["pos"]
    return out


def section_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    buckets: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        buckets[str(row["section"])][str(row["type"])] += 1
    return {key: {"surfaces": sum(value.values()), "types": dict(sorted(value.items()))} for key, value in sorted(buckets.items())}


def url_contexts(text: str, urls: list[str]) -> list[dict[str, Any]]:
    heads = heading_rows(text)
    out: list[dict[str, Any]] = []
    for url in urls:
        sections: list[str] = []
        cursor = 0
        occurrences = 0
        while True:
            pos = text.find(url, cursor)
            if pos < 0:
                break
            occurrences += 1
            sections.append(heading_for(heads, pos))
            cursor = pos + 1
        out.append({"url": url, "occurrences": occurrences, "sections": sorted(set(sections), key=str.casefold)})
    return out


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", required=True)
args = parser.parse_args()
product_root = Path(args.product_root).resolve()
product = product_root / PRODUCT_REL

errors: list[str] = []
def require(ok: bool, msg: str) -> None:
    if not ok:
        errors.append(msg)

for path, expected in EXPECTED_BLOBS.items():
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    if path.is_file():
        require(blob(ROOT, path.relative_to(ROOT)) == expected, f"blob drift {path.relative_to(ROOT)}")
require(product.is_file(), f"missing Product {PRODUCT_REL}")
if product.is_file():
    require(blob(product_root, PRODUCT_REL) == EXPECTED_PRODUCT_BLOB, "Product native Romans 7 blob drift")
require(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=product_root, text=True).strip() == PRODUCT_COMMIT, "Product snapshot drift")

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

owners = {
    "PRODUCT_NATIVE": (product, module.p(str(PRODUCT_REL), "native Romans 7 Body")),
    "R3": (R3, module.r(str(R3.relative_to(ROOT)), "R3 support")),
    "R4": (R4, module.r(str(R4.relative_to(ROOT)), "R4 support")),
    "R5": (R5, module.r(str(R5.relative_to(ROOT)), "R5 support")),
}
scans: dict[str, dict[str, Any]] = {}
quotes: dict[str, list[dict[str, Any]]] = {}
texts: dict[str, str] = {}
for name, (path, owner_spec) in owners.items():
    text = path.read_text(encoding="utf-8")
    texts[name] = text
    scans[name] = module.scan_owner(owner_spec, product_root)
    quotes[name] = quote_rows(text)

per_owner: dict[str, Any] = {}
for name in owners:
    scan = scans[name]
    q = quotes[name]
    require(len(q) == scan["inlineQuotationSegments"] + scan["markdownBlockquotes"] + scan["htmlBlockquotes"], f"{name} quote scanner mismatch")
    per_owner[name] = {
        "scriptureReferences": len(scan["scriptureReferences"]),
        "quotationSurfaces": len(q),
        "externalLinks": len(scan["externalLinks"]),
        "internalArticleLinks": len(scan["internalArticleLinks"]),
        "scriptureSha256": sha_json(sorted(scan["scriptureReferences"], key=str.casefold)),
        "quotationManifestSha256": sha_json(q),
        "externalLinksSha256": sha_json(sorted(scan["externalLinks"], key=str.casefold)),
        "internalLinksSha256": sha_json(sorted(scan["internalArticleLinks"], key=str.casefold)),
        "sectionSummarySha256": sha_json(section_summary(q)),
    }

union_refs = sorted({item for scan in scans.values() for item in scan["scriptureReferences"]}, key=str.casefold)
union_urls = sorted({item for scan in scans.values() for item in scan["externalLinks"]}, key=str.casefold)
union_internal = sorted({item for scan in scans.values() for item in scan["internalArticleLinks"]}, key=str.casefold)
all_quote_rows = [{"owner": name, **row} for name in owners for row in quotes[name]]

part2 = json.loads(PART2.read_text(encoding="utf-8"))
reuse = {
    "receiptAuthorityId": part2.get("authorityId"),
    "R3R4RoleCounts": part2.get("fullOwnerReview", {}).get("roleCounts"),
    "R3R4UrlStatusCounts": part2.get("externalLinkReview", {}).get("statusCounts"),
    "R3R4SourceSurfaceBaseManifestSha256": part2.get("fullOwnerReview", {}).get("sourceSurfaceBaseManifestSha256"),
    "R3R4ClassifiedSurfaceManifestSha256": part2.get("fullOwnerReview", {}).get("classifiedSurfaceManifestSha256"),
    "R3R4UrlRegistrySha256": part2.get("externalLinkReview", {}).get("dispositionRegistrySha256"),
    "R3R4ReuseAllowedOnlyWithExactBlobs": True,
}

manifest = {
    "schemaVersion": 1,
    "authorityId": "HEART-PART5-NATIVE-CITATION-CALIBRATION-2026-08-09",
    "productSnapshot": PRODUCT_COMMIT,
    "productBlob": EXPECTED_PRODUCT_BLOB,
    "perOwner": per_owner,
    "aggregate": {
        "uniqueScriptureReferences": len(union_refs),
        "quotationSurfaces": len(all_quote_rows),
        "uniqueExternalLinks": len(union_urls),
        "uniqueInternalArticleLinks": len(union_internal),
        "scriptureSetSha256": sha_json(union_refs),
        "quotationManifestSha256": sha_json(all_quote_rows),
        "externalLinkSetSha256": sha_json(union_urls),
        "internalLinkSetSha256": sha_json(union_internal),
    },
    "productNative": {
        "sectionSummary": section_summary(quotes["PRODUCT_NATIVE"]),
        "urlRegistry": url_contexts(texts["PRODUCT_NATIVE"], sorted(scans["PRODUCT_NATIVE"]["externalLinks"], key=str.casefold)),
        "internalLinks": sorted(scans["PRODUCT_NATIVE"]["internalArticleLinks"], key=str.casefold),
    },
    "r5": {
        "sectionSummary": section_summary(quotes["R5"]),
        "urlRegistry": url_contexts(texts["R5"], sorted(scans["R5"]["externalLinks"], key=str.casefold)),
        "internalLinks": sorted(scans["R5"]["internalArticleLinks"], key=str.casefold),
    },
    "r3r4Reuse": reuse,
}
manifest["manifestSha256"] = sha_json(manifest)
print("HEART_PART5_NATIVE_CITATION_CALIBRATION=" + json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")))

if errors:
    print("Heart Part V native citation calibration: FAIL before calibration boundary", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Heart Part V native citation calibration: FAIL (expected red-first calibration)", file=sys.stderr)
print("- CALIBRATION_ONLY: freeze exact native/R5 manifests and complete dispositions before merge", file=sys.stderr)
raise SystemExit(1)
