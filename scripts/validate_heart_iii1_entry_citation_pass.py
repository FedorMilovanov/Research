#!/usr/bin/env python3
"""Validate the complete III.1 entry citation pass."""
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
RECEIPT_PATH = ROOT / "data/heart-iii1-citation-review-2026-08-04.json"
HUMAN_PATH = ROOT / "СЕРИЯ СЕРДЦЕ/119_III1_ENTRY_CITATION_PASS_2026-08-04.md"
READER_PATH = ROOT / "СЕРИЯ СЕРДЦЕ/117_READER_CHAPTER_III1_NEW_HEART_PROMISE_2026-08-04.md"
WORKFLOW_PATH = ROOT / ".github/workflows/heart-reader-assembly.yml"
PRODUCT_REL = Path("src/content/articles/novoe-serdce.mdx")
PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"
PRODUCT_BLOB = "8d4936d6b58b380215b259a5511a8c2bfad33a46"
READER_BLOB = "f0355d4a9a451ecbe6a2256a36876839a0c4889e"
ROW_HASH = "c4c80641561a004cb94fcaf28afabef46315f3de74fb1fd61e113bf7ba6f264f"
CLASSIFIED_HASH = "e926d96d89333c5121fe55e7a5b6d1509090d6defa068c7ebce9ed2ed670d5b0"
REFERENCE_HASH = "63f105a753816613de66c9ac6f675d9ecbaa9fd4ce3130374305d8ca016b3c0e"
EXPECTED_BLOBS = {
    ROOT / "data/heart-entry-citation-pass-current-v6-2026-08-04.json": "fd46d6f99a735301f2966b0e2912eb68805bdff9",
    ROOT / "data/heart-iii1-reader-assembly-2026-08-04.json": "9012cec659ddbac7e65cb0d23ab8a639e0787bab",
}
CLASSES = {
    "SCRIPTURE_DIRECT_OR_EXPLICIT_BIBLICAL_FRAGMENT": [3,4,5,6,8,9,11,12,13,15,17,18,20,21,22,23,25,27,31,32,33,34,35,36,37,38,40,41,42,46,48,51,52,55,56,57,59,60],
    "EDITORIAL_OR_PASTORAL_FORMULATION": [16,19,43,47,49,53,54],
    "LEXICAL_TRANSLATION_OR_THEOLOGICAL_TERM": [24,28,39,44,58,61,62,63,64,65,66],
    "TITLE_HEADING_OR_LINK_LABEL": [1,2,7,10,14,29,30,45,50,67],
    "ATTRIBUTED_THEOLOGICAL_PARAPHRASE_HOLD": [26],
}
TARGET_OCCURRENCES = {
    "/articles/krajne-li-isporcheno-serdce/": 2,
    "/articles/kak-menyaetsya-serdce/": 4,
    "/articles/serdce-i-duh/": 1,
    "/articles/serdce-hrista-k-nemoshchnym/": 2,
}
TARGET_FILES = {
    "/articles/krajne-li-isporcheno-serdce/": "src/content/articles/krajne-li-isporcheno-serdce.mdx",
    "/articles/kak-menyaetsya-serdce/": "src/content/articles/kak-menyaetsya-serdce.mdx",
    "/articles/serdce-i-duh/": "src/content/articles/serdce-i-duh.mdx",
    "/articles/serdce-hrista-k-nemoshchnym/": "src/content/articles/serdce-hrista-k-nemoshchnym.mdx",
}
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def git_blob(path: Path, repo_root: Path = ROOT) -> str:
    return subprocess.check_output(["git", "hash-object", str(path.relative_to(repo_root))], cwd=repo_root, text=True).strip()


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be a JSON object")
    return value if isinstance(value, dict) else {}


def norm(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()
product_path = product_root / PRODUCT_REL
receipt = load(RECEIPT_PATH)
human = HUMAN_PATH.read_text(encoding="utf-8")
reader = READER_PATH.read_text(encoding="utf-8")
source = product_path.read_text(encoding="utf-8")
workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

for path, expected in EXPECTED_BLOBS.items():
    require(path.is_file(), f"immutable authority missing: {path.relative_to(ROOT)}")
    if path.is_file():
        require(git_blob(path) == expected, f"immutable authority blob drift: {path.relative_to(ROOT)}")
require(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=product_root, text=True).strip() == PRODUCT_COMMIT, "Product checkout is not pinned")
require(git_blob(product_path, product_root) == PRODUCT_BLOB, "III.1 Product blob drift")
require(git_blob(READER_PATH) == READER_BLOB, "III.1 reader blob drift")

scan = module.scan_owner(module.p(str(PRODUCT_REL), "historical full III.1 owner"), product_root)
reader_scan = module.scan_owner(module.r(str(READER_PATH.relative_to(ROOT)), "assembled III.1 reader"), product_root)
require(len(scan["scriptureReferences"]) == 30, "III.1 Scripture reference count drift")
require(digest(scan["scriptureReferences"]) == REFERENCE_HASH, "III.1 Scripture reference set drift")
require(scan["inlineQuotationSegments"] + scan["markdownBlockquotes"] + scan["htmlBlockquotes"] == 67, "III.1 quotation count drift")
require(len(scan["externalLinks"]) == 0, "III.1 external link detected")
require(len(scan["internalArticleLinks"]) == 4, "III.1 unique internal target count drift")

starts = list(re.finditer(r'<h2\s+id="([^"]+)"[^>]*>', source, flags=re.I))
sections: list[tuple[int, int, str]] = []
for index, match in enumerate(starts):
    end = starts[index + 1].start() if index + 1 < len(starts) else len(source)
    sections.append((match.start(), end, match.group(1)))


def section_for(pos: int) -> str:
    for start, end, section_id in sections:
        if start <= pos < end:
            return section_id
    return "frontmatter-or-intro"


rows: list[dict[str, Any]] = []
for kind, pattern in (
    ("RUSSIAN_GUILLEMETS", re.compile(r"«([^»\n]{8,})»")),
    ("CURLY_QUOTES", re.compile(r"“([^”\n]{8,})”")),
):
    for match in pattern.finditer(source):
        rows.append({
            "offset": match.start(),
            "section": section_for(match.start()),
            "kind": kind,
            "normalizedSha256": hashlib.sha256(norm(match.group(1)).encode("utf-8")).hexdigest(),
        })
for match in re.finditer(r"^\s*>\s?(\S.*)$", source, flags=re.M):
    rows.append({
        "offset": match.start(),
        "section": section_for(match.start()),
        "kind": "MARKDOWN_BLOCKQUOTE_LINE",
        "normalizedSha256": hashlib.sha256(norm(match.group(1)).encode("utf-8")).hexdigest(),
    })
rows.sort(key=lambda row: row["offset"])
hashes = [row["normalizedSha256"] for row in rows]
require(len(hashes) == 67, "III.1 deterministic quotation decomposition drift")
require(digest(hashes) == ROW_HASH, "III.1 quotation hash order drift")

all_indices = [index for indices in CLASSES.values() for index in indices]
require(sorted(all_indices) == list(range(1, 68)), "III.1 class assignment is not exhaustive")
require(len(all_indices) == len(set(all_indices)), "III.1 class assignment overlaps")
index_to_class = {index: name for name, indices in CLASSES.items() for index in indices}
manifest = [{"index": index, "normalizedSha256": hashes[index - 1], "class": index_to_class[index]} for index in range(1, 68)]
require(digest(manifest) == CLASSIFIED_HASH, "III.1 classified manifest drift")

link_occurrences: dict[str, int] = {}
for match in module.ARTICLE_LINK_RE.finditer(source):
    link_occurrences[match.group(0)] = link_occurrences.get(match.group(0), 0) + 1
require(link_occurrences == TARGET_OCCURRENCES, "III.1 internal target occurrence drift")
for target, path in TARGET_FILES.items():
    require((product_root / path).is_file(), f"III.1 pinned Product target missing: {target}")

product = receipt.get("productOwner", {})
require(receipt.get("authorityId") == "HEART-III1-CITATION-REVIEW-2026-08-04", "III.1 citation authority drift")
require(receipt.get("status") == "III1_ENTRY_CITATION_PASS_COMPLETE_READER_REVIEWED_ZERO_NEW_DIRECT_QUOTES", "III.1 citation status drift")
require(product.get("commit") == PRODUCT_COMMIT and product.get("gitBlob") == PRODUCT_BLOB, "III.1 receipt Product witness drift")
require(product.get("scriptureReferences") == scan["scriptureReferences"], "III.1 receipt Scripture references drift")
require(product.get("scriptureReferenceSetSha256") == REFERENCE_HASH, "III.1 receipt Scripture hash drift")
require(product.get("quotationSurfaceHashesInOrder") == hashes, "III.1 receipt surface list drift")
require(product.get("quotationSurfaceHashListSha256") == ROW_HASH, "III.1 receipt surface hash drift")
classification = product.get("quotationClassification", {})
require(classification.get("classes") == CLASSES, "III.1 receipt class map drift")
require(classification.get("classifiedManifestSha256") == CLASSIFIED_HASH, "III.1 receipt classified hash drift")
require(classification.get("counts") == {name: len(indices) for name, indices in CLASSES.items()}, "III.1 class counts drift")
require(classification.get("total") == 67, "III.1 class total drift")
require(product.get("externalLinks") == {"unique": 0, "occurrences": 0, "disposition": "NONE_PRESENT"}, "III.1 external-link disposition drift")
internal = product.get("internalLinks", {})
require(internal.get("uniqueTargets") == list(TARGET_OCCURRENCES), "III.1 internal target list drift")
require(internal.get("occurrences") == 9, "III.1 internal occurrence total drift")
require(internal.get("targetOccurrences") == TARGET_OCCURRENCES, "III.1 internal occurrence map drift")
require(internal.get("disposition") == "ALL_TARGETS_EXIST_ON_PINNED_PRODUCT_READER_TRANSFER_ZERO", "III.1 internal disposition drift")

holds = receipt.get("retainedHoldsAndRepairs", {})
require(holds.get("productScriptureLocatorRepairsRequired") == [{"surfaceIndex": 57, "requiredLocator": "Флп. 1:6", "reason": "existing Product Scripture fragment lacks an explicit locator"}], "III.1 Product locator repair drift")
require(holds.get("attributedTheologicalLocatorHolds") == [{"surfaceIndex": 26, "attribution": "Stephen Charnock", "reason": "existing attributed paraphrase remains support-only without a precise primary-source locator"}], "III.1 attributed hold drift")
require(holds.get("lexicalSupportLocatorHolds") == {"surfaceIndices": [24,39,44,62,63,64,65,66], "count": 8, "readerTransfer": 0}, "III.1 lexical hold drift")
require(holds.get("existingProductUrlRepairsRetainedFromI3") == 3, "I.3 Product repair carry-forward drift")
require(holds.get("part2DossierUrlHoldsRetained") == 15, "Part II dossier hold carry-forward drift")
require(holds.get("part2UnresolvedInternalPathRetained") == 1, "Part II unresolved path carry-forward drift")

require(len(reader_scan["scriptureReferences"]) == 18, "III.1 reader Scripture count drift")
require(reader_scan["inlineQuotationSegments"] + reader_scan["markdownBlockquotes"] + reader_scan["htmlBlockquotes"] == 0, "III.1 reader quote detected")
require(len(reader_scan["externalLinks"]) == 0 and len(reader_scan["internalArticleLinks"]) == 0, "III.1 reader link detected")
require(reader_scan["footnoteDefinitions"] == 0, "III.1 reader footnote detected")
review = receipt.get("readerReview", {})
require(review.get("gitBlob") == READER_BLOB and review.get("wordCount") == 1791, "III.1 reader review witness drift")
for key in ("quotationSurfaces","externalLinks","internalLinks","footnotes","historicalProductQuotationTransfer","historicalProductLinkTransfer","newDirectQuotesApproved"):
    require(review.get(key) == 0, f"III.1 reader review {key} drift")
require(review.get("scriptureReferences") == 18, "III.1 reader review Scripture drift")

require(receipt.get("effectiveState") == {
    "previous": "ASSEMBLED_READER_CITATION_OPEN",
    "current": "ENTRY_CITATION_PASS_COMPLETE",
    "entryCitationPassComplete": True,
    "assembledReaderCitationReviewComplete": True,
}, "III.1 effective state drift")
require(receipt.get("effectiveCounts") == {
    "finalBookEntries":18,"entryCitationPassComplete":10,"entryCitationPassOpen":8,
    "assembledReaders":10,"assembledReaderCitationReviewsComplete":10,"missingStandaloneFinalReaders":8,
    "productSourceOnlyEntries":3,"researchDossierOnlyEntries":5,
    "productSourceRepairsRequired":4,"dossierUrlHoldsRetained":15,"unresolvedInternalPathsRetained":1,
    "newDirectQuotesApproved":0,
}, "III.1 effective counts drift")
boundary = receipt.get("publicationBoundary", {})
require(boundary.get("iii1EntryCitationPassComplete") is True, "III.1 pass not marked complete")
require(boundary.get("allCurrentlyAssembledReadersCitationReviewed") is True, "III.1 reader review not complete")
for key in ("currentV7CompositionComplete","wholeBookReaderAssemblyComplete","wholeBookCitationPassComplete","wholeBookTransitionDedupPassComplete","wholeBookLineEditComplete","manuscriptBundleComplete","productReleaseComplete"):
    require(boundary.get(key) is False, f"III.1 publication boundary weakened: {key}")
require(boundary.get("newDirectQuotesApproved") == 0, "III.1 direct quote approval drift")

for marker in (
    "HEART-III1-CITATION-REVIEW-2026-08-04",
    "30 / 30", "67 / 67", "38", "7", "11", "10", "CURRENT V7 COMPOSITION COMPLETE = FALSE",
    "WHOLE-BOOK CITATION PASS = OPEN", "PRODUCT RELEASE = NOT CLAIMED",
):
    require(marker in human, f"III.1 human authority marker missing: {marker}")
require(not (ROOT / "scripts/diagnose_heart_iii1_citation.py").exists(), "temporary III.1 diagnostic script retained")
require("diagnose_heart_iii1_citation.py" not in workflow and "Diagnose III.1 citation surface" not in workflow, "temporary III.1 diagnostic workflow retained")
require("validate_heart_iii1_entry_citation_pass.py" in workflow, "permanent III.1 citation gate missing")

if errors:
    print("III.1 entry citation pass validation failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    sys.exit(1)

print("III.1 entry citation pass validated")
print("- Product: 30 Scripture / 67 classified quotation surfaces / 0 external / 4 internal targets")
print("- taxonomy: 38 Scripture / 7 editorial / 11 lexical / 10 titles / 1 attributed hold")
print("- reader: 18 Scripture / 0 quote-link-footnote surfaces")
print("- effective state: 10/18 complete; 10/10 assembled readers reviewed; V7 composition still separate")
