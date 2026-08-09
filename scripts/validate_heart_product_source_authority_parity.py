#!/usr/bin/env python3
"""Validate Heart Product citation authority against native Astro sources.

Historical Heart citation inventory used reference-only MDX witnesses. Current
Product route profiles declare native Astro Body components as content authority.
This validator derives every Product owner from the immutable historical builder,
recomputes reference-MDX vs native citation surfaces, pins the exact mismatch
manifest, and requires the affected historical citation passes to be explicitly
reopened in the corrected current authority.
"""
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
RECEIPT = ROOT / "data/heart-product-source-authority-parity-2026-08-09.json"
CURRENT_V10 = ROOT / "data/heart-entry-citation-pass-current-v10-2026-08-09.json"
CURRENT_V11 = ROOT / "data/heart-entry-citation-pass-current-v11-2026-08-09.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/135_PRODUCT_SOURCE_AUTHORITY_REOPEN_2026-08-09.md"
BUILDER_BLOB = "6e8fb1af57bc72d26a9ca91d5b84b1fec3de7f12"
V10_BLOB = "2a34228ecb29d3181c6e23f0f761a48c3af0ebd5"
PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"
EXPECTED_MANIFEST_SHA = "df4fd39e73c031083d8fad145263281c3be10ededa0a20d14f89b78e64a3b576"
EXPECTED_REOPENED = {
    "HEART-BOOK-I1",
    "HEART-BOOK-I3",
    "HEART-BOOK-I4",
    "HEART-BOOK-III1",
    "HEART-BOOK-III4",
    "HEART-BOOK-X2",
    "HEART-BOOK-X3",
}
EXPECTED_UNAFFECTED_COMPLETE = {
    "HEART-BOOK-I2",
    "HEART-BOOK-II",
    "HEART-BOOK-III2",
    "HEART-BOOK-III3",
    "HEART-BOOK-IV",
    "HEART-BOOK-X1",
}
EXPECTED_ALREADY_OPEN_AFFECTED = {"HEART-BOOK-V", "HEART-BOOK-VII"}
EXPECTED_ALL_AFFECTED = EXPECTED_REOPENED | EXPECTED_ALREADY_OPEN_AFFECTED
EXPECTED_OPEN = EXPECTED_REOPENED | {
    "HEART-BOOK-V",
    "HEART-BOOK-VI",
    "HEART-BOOK-VII",
    "HEART-BOOK-VIII",
    "HEART-BOOK-IX",
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
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be a JSON object")
    return value if isinstance(value, dict) else {}


def git_blob(root: Path, rel: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(rel)], cwd=root, text=True).strip()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha_json(value: Any) -> str:
    return sha_text(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    return text[end + 5 :] if end >= 0 else text


def normalize_semantic(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"!\[([^\]]*)\]\([^\)]*\)", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^\)]*\)", r"\1", value)
    value = re.sub(r"[`*_~]+", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def quotation_manifest(text: str) -> list[str]:
    values: list[str] = []
    for pattern in (re.compile(r"«([^»\n]{8,})»"), re.compile(r"“([^”\n]{8,})”")):
        for match in pattern.finditer(text):
            value = normalize_semantic(match.group(1))
            if value:
                values.append(value)

    md_lines: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^\s*>\s?(.*)$", line)
        if match:
            md_lines.append(match.group(1))
            continue
        if md_lines:
            value = normalize_semantic(" ".join(md_lines))
            if value:
                values.append(value)
            md_lines = []
    if md_lines:
        value = normalize_semantic(" ".join(md_lines))
        if value:
            values.append(value)

    for match in re.finditer(r"<blockquote[^>]*>(.*?)</blockquote>", text, re.I | re.S):
        value = normalize_semantic(match.group(1))
        if value:
            values.append(value)

    return sorted((sha_text(value) for value in values), key=str.casefold)


def citation_surface(text: str, module: Any) -> dict[str, Any]:
    refs = sorted({module.normalize_ref(match.group(0)) for match in module.SCRIPTURE_RE.finditer(text)}, key=str.casefold)
    urls = sorted({module.trim_url(match.group(0)) for match in module.URL_RE.finditer(text)}, key=str.casefold)
    internal = sorted(set(module.ARTICLE_LINK_RE.findall(text)), key=str.casefold)
    quotes = quotation_manifest(text)
    return {
        "scriptureReferences": refs,
        "externalLinks": urls,
        "internalArticleLinks": internal,
        "quotationManifest": quotes,
        "counts": {
            "scriptureReferences": len(refs),
            "externalLinks": len(urls),
            "internalArticleLinks": len(internal),
            "quotationSemanticSurfaces": len(quotes),
        },
        "hashes": {
            "scriptureReferencesSha256": sha_json(refs),
            "externalLinksSha256": sha_json(urls),
            "internalArticleLinksSha256": sha_json(internal),
            "quotationManifestSha256": sha_json(quotes),
        },
    }


def diff_set(legacy: list[str], native: list[str]) -> dict[str, list[str]]:
    return {
        "missingFromNative": sorted(set(legacy) - set(native), key=str.casefold),
        "nativeOnly": sorted(set(native) - set(legacy), key=str.casefold),
    }


def diff_multiset(legacy: list[str], native: list[str]) -> dict[str, Any]:
    a = Counter(legacy)
    b = Counter(native)
    return {
        "missingFromNative": dict(sorted((a - b).items())),
        "nativeOnly": dict(sorted((b - a).items())),
    }


def resolve_native_body(product_root: Path, mdx_rel: str) -> dict[str, str]:
    slug = Path(mdx_rel).stem
    profile_rel = Path("data/route-profiles") / f"articles-{slug}.json"
    profile_path = product_root / profile_rel
    require(profile_path.is_file(), f"{slug}: route profile missing: {profile_rel}")
    if not profile_path.is_file():
        return {"slug": slug, "profilePath": str(profile_rel), "renderSource": "", "nativeBodyPath": ""}

    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    require(profile.get("route") == f"/articles/{slug}/", f"{slug}: route profile route mismatch")
    require(profile.get("contentSourceMode") == "astro-native-entry", f"{slug}: contentSourceMode is not astro-native-entry")
    require(profile.get("migrationMode") == "strict-native", f"{slug}: migrationMode is not strict-native")
    require(profile.get("hasMDX") is False, f"{slug}: hasMDX must be false under native authority")
    require(profile.get("mdxStatus") == "reference-only", f"{slug}: mdxStatus must be reference-only")
    require(profile.get("mdxPath") == mdx_rel, f"{slug}: route profile mdxPath mismatch")

    render_rel = Path(str(profile.get("renderSource", "")))
    render_path = product_root / render_rel
    require(render_path.is_file(), f"{slug}: renderSource missing: {render_rel}")
    if not render_path.is_file():
        return {"slug": slug, "profilePath": str(profile_rel), "renderSource": str(render_rel), "nativeBodyPath": ""}

    page = render_path.read_text(encoding="utf-8")
    imports = re.findall(r"import\s+([A-Za-z0-9_]*Body)\s+from\s+['\"]@/([^'\"]+\.astro)['\"]\s*;?", page)
    used = [(name, rel) for name, rel in imports if re.search(rf"<{re.escape(name)}(?:\s|/?>)", page)]
    require(len(used) == 1, f"{slug}: expected one rendered *Body import, got {used}")
    if len(used) != 1:
        return {"slug": slug, "profilePath": str(profile_rel), "renderSource": str(render_rel), "nativeBodyPath": ""}
    _, import_rel = used[0]
    body_rel = Path("src") / import_rel
    require((product_root / body_rel).is_file(), f"{slug}: native Body missing: {body_rel}")
    return {
        "slug": slug,
        "profilePath": str(profile_rel),
        "renderSource": str(render_rel),
        "nativeBodyPath": str(body_rel),
    }


parser = argparse.ArgumentParser()
parser.add_argument("--product-root", type=Path, required=True)
args = parser.parse_args()
product_root = args.product_root.resolve()

require(BUILDER.is_file(), "historical Heart inventory builder missing")
if BUILDER.is_file():
    require(git_blob(ROOT, BUILDER.relative_to(ROOT)) == BUILDER_BLOB, "historical Heart inventory builder blob drift")
require(CURRENT_V10.is_file(), "immutable V10 current authority missing")
if CURRENT_V10.is_file():
    require(git_blob(ROOT, CURRENT_V10.relative_to(ROOT)) == V10_BLOB, "immutable V10 current authority blob drift")

product_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=product_root, text=True).strip()
require(product_head == PRODUCT_COMMIT, f"Product witness must be exact {PRODUCT_COMMIT}, got {product_head}")

spec = importlib.util.spec_from_file_location("heart_inventory", BUILDER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

owners: dict[tuple[str, tuple[str, ...]], dict[str, Any]] = {}
entry_ids_by_key: dict[tuple[str, tuple[str, ...]], list[str]] = defaultdict(list)
for entry in module.ENTRIES:
    for kind in ("manuscripts", "support"):
        for owner in entry[kind]:
            if owner.get("surface") != "product":
                continue
            key = (str(owner["path"]), tuple(owner.get("sections") or []))
            owners[key] = owner
            entry_ids_by_key[key].append(str(entry["id"]))

rows: list[dict[str, Any]] = []
for key in sorted(owners, key=lambda item: (item[0].casefold(), item[1])):
    owner = owners[key]
    mdx_rel = str(owner["path"])
    sections = list(owner.get("sections") or [])
    mdx_path = product_root / mdx_rel
    require(mdx_path.is_file(), f"historical Product MDX witness missing: {mdx_rel}")
    resolution = resolve_native_body(product_root, mdx_rel)
    native_rel = resolution["nativeBodyPath"]
    native_path = product_root / native_rel if native_rel else Path("/__missing__")
    if not mdx_path.is_file() or not native_rel or not native_path.is_file():
        continue

    mdx_full = mdx_path.read_text(encoding="utf-8")
    mdx_body = strip_frontmatter(mdx_full)
    native_full = native_path.read_text(encoding="utf-8")
    try:
        mdx_scoped = module.extract_sections(mdx_body, sections)
        native_scoped = module.extract_sections(native_full, sections)
    except ValueError as exc:
        require(False, f"{resolution['slug']}: scoped section parity cannot be resolved: {exc}")
        continue

    legacy_surface = citation_surface(mdx_scoped, module)
    native_surface = citation_surface(native_scoped, module)
    set_diffs = {
        "scriptureReferences": diff_set(legacy_surface["scriptureReferences"], native_surface["scriptureReferences"]),
        "externalLinks": diff_set(legacy_surface["externalLinks"], native_surface["externalLinks"]),
        "internalArticleLinks": diff_set(legacy_surface["internalArticleLinks"], native_surface["internalArticleLinks"]),
        "quotationManifest": diff_multiset(legacy_surface["quotationManifest"], native_surface["quotationManifest"]),
    }
    parity = all(not diff[side] for diff in set_diffs.values() for side in ("missingFromNative", "nativeOnly"))
    rows.append({
        "entryIds": sorted(entry_ids_by_key[key]),
        "slug": resolution["slug"],
        "sections": sections,
        "historicalReferenceMdx": {
            "path": mdx_rel,
            "gitBlob": git_blob(product_root, Path(mdx_rel)),
            "fullFileSha256": sha_text(mdx_full),
            "bodyOnlySha256": sha_text(mdx_body),
        },
        "routeAuthority": {
            "profilePath": resolution["profilePath"],
            "profileGitBlob": git_blob(product_root, Path(resolution["profilePath"])),
            "renderSource": resolution["renderSource"],
            "renderSourceGitBlob": git_blob(product_root, Path(resolution["renderSource"])),
            "nativeBodyPath": native_rel,
            "nativeBodyGitBlob": git_blob(product_root, Path(native_rel)),
            "nativeBodySha256": sha_text(native_full),
        },
        "legacyBodyOnlySurface": {"counts": legacy_surface["counts"], "hashes": legacy_surface["hashes"]},
        "nativeSurface": {"counts": native_surface["counts"], "hashes": native_surface["hashes"]},
        "citationSurfaceParity": parity,
        "diff": set_diffs,
    })

summary = {
    "schemaVersion": 1,
    "researchBase": "062a7fe14d98c89fe04fc376fdfeb8bb2b060378",
    "productSnapshot": PRODUCT_COMMIT,
    "historicalBuilderBlob": BUILDER_BLOB,
    "ownerSpecsChecked": len(rows),
    "uniqueSlugsChecked": len({row["slug"] for row in rows}),
    "allCitationSurfacesParity": bool(rows) and all(row["citationSurfaceParity"] for row in rows),
    "rows": rows,
}
manifest_sha = sha_json(summary["rows"])

receipt = read_json(RECEIPT)
v10 = read_json(CURRENT_V10)
v11 = read_json(CURRENT_V11)

require(len(rows) == 10, f"expected 10 Product owner specs, got {len(rows)}")
require(len({row["slug"] for row in rows}) == 9, "expected 9 unique Product slugs")
require(summary["allCitationSurfacesParity"] is False, "calibrated divergence unexpectedly disappeared; review authority before changing receipt")
require(manifest_sha == EXPECTED_MANIFEST_SHA, f"native-authority manifest drift: {manifest_sha}")

require(receipt.get("authorityId") == "HEART-PRODUCT-SOURCE-AUTHORITY-PARITY-2026-08-09", "source-authority receipt id drift")
cal = receipt.get("calibration", {})
require(cal.get("ownerSpecsChecked") == 10, "receipt owner-spec count drift")
require(cal.get("uniqueSlugsChecked") == 9, "receipt unique-slug count drift")
require(cal.get("allCitationSurfacesParity") is False, "receipt must record parity=false")
require(cal.get("mismatchingOwnerSpecs") == 10, "receipt mismatch count drift")
require(cal.get("manifestSha256") == EXPECTED_MANIFEST_SHA == manifest_sha, "receipt manifest SHA drift")

runtime_specs = {
    (tuple(row["entryIds"]), row["historicalReferenceMdx"]["path"], tuple(row["sections"]), row["routeAuthority"]["nativeBodyPath"])
    for row in rows
}
receipt_specs = {
    (tuple(item.get("entryIds", [])), item.get("referenceMdx"), tuple(item.get("sections", [])), item.get("nativeBody"))
    for item in receipt.get("mismatchingSpecs", [])
}
require(runtime_specs == receipt_specs, "receipt mismatch-spec manifest does not match runtime-derived owners")
runtime_affected = {entry for row in rows for entry in row["entryIds"]}
require(runtime_affected == EXPECTED_ALL_AFFECTED, f"runtime affected-entry set drift: {sorted(runtime_affected)}")
require(set(receipt.get("affectedEntryIds", [])) == EXPECTED_ALL_AFFECTED, "receipt affected-entry set drift")
require(set(receipt.get("completedEntriesReopened", [])) == EXPECTED_REOPENED, "receipt reopened set drift")
require(set(receipt.get("alreadyOpenAffectedEntries", [])) == EXPECTED_ALREADY_OPEN_AFFECTED, "receipt already-open affected set drift")
require(set(receipt.get("completedEntriesUnaffected", [])) == EXPECTED_UNAFFECTED_COMPLETE, "receipt unaffected-completed set drift")

decision = receipt.get("decision", {})
require(decision.get("historicalReferenceMdxMayRemainForensicWitness") is True, "receipt must preserve MDX as forensic witness")
require(decision.get("historicalReferenceMdxMayActAsCurrentCitationAuthority") is False, "reference-only MDX must not remain current citation authority")
require(decision.get("nativeAstroBodyIsCurrentProductContentAuthority") is True, "native Astro Body authority not recorded")
require(decision.get("priorCitationReceiptsRemainImmutableHistoricalEvidence") is True, "historical receipts must remain immutable")
require(decision.get("reopenedEntriesRequireNativeAuthorityCitationReview") is True, "reopened-entry review requirement missing")

require(v10.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V10-2026-08-09", "V10 authority drift")
require(v10.get("currentCounts", {}).get("entryCitationPassComplete") == 13, "V10 historical completion count drift")
require(set(v10.get("completedEntryIds", [])) == EXPECTED_UNAFFECTED_COMPLETE | EXPECTED_REOPENED, "V10 completed set drift")

require(v11.get("authorityId") == "HEART-ENTRY-CITATION-PASS-CURRENT-V11-2026-08-09", "V11 authority drift")
counts = v11.get("currentCounts", {})
require(counts.get("entryCitationPassComplete") == 6, "V11 must report 6/18 current native-authority passes")
require(counts.get("entryCitationPassOpen") == 12, "V11 must report 12/18 open")
require(counts.get("assembledReaderEntries") == 14, "V11 assembled-reader count drift")
require(counts.get("assembledReaderCitationReviewsComplete") == 6, "V11 current-authority reader-review count drift")
require(counts.get("assembledReadersAwaitingCitationReviewOrNativeReconciliation") == 8, "V11 pending assembled review count drift")
require(counts.get("missingStandaloneFinalReaders") == 4, "V11 missing-reader count drift")
require(counts.get("nativeAuthorityReopenedCompletedEntries") == 7, "V11 reopened count drift")
require(counts.get("productSourceRepairsRequiredRetained") == 4, "V11 silently changes Product repair backlog")
require(counts.get("dossierUrlHoldsRetained") == 55, "V11 silently changes dossier HOLD backlog")
require(counts.get("dossierSourceUrlRepairsRequired") == 2, "V11 silently changes dossier URL repair backlog")
require(counts.get("unresolvedInternalPathsRetained") == 1, "V11 silently changes unresolved path backlog")
require(counts.get("newDirectQuotesApproved") == 0, "V11 approves new direct quotes")
require(set(v11.get("completedEntryIds", [])) == EXPECTED_UNAFFECTED_COMPLETE, "V11 completed set drift")
require(set(v11.get("openEntryIds", [])) == EXPECTED_OPEN, "V11 open set drift")
require(set(v11.get("reopenedByNativeSourceAuthority", [])) == EXPECTED_REOPENED, "V11 reopened set drift")

reader_state = v11.get("readerState", {})
require(reader_state.get("assembledReaders") == 14, "V11 reader-state assembled count drift")
require(set(reader_state.get("missingStandaloneReaders", [])) == {"HEART-BOOK-VI", "HEART-BOOK-VII", "HEART-BOOK-VIII", "HEART-BOOK-IX"}, "V11 missing-reader set drift")
require(set(reader_state.get("assembledReaderAwaitingFirstCitationPass", [])) == {"HEART-BOOK-V"}, "V11 first-pass reader set drift")
require(set(reader_state.get("assembledReadersNeedingNativeSourceReconciliation", [])) == EXPECTED_REOPENED, "V11 native-reconciliation reader set drift")

backlog = v11.get("retainedBacklog", {})
require(backlog == {
    "historicalProductSourceRepairsRequired": 4,
    "dossierUrlHoldsRetained": 55,
    "dossierSourceUrlRepairsRequired": 2,
    "unresolvedInternalPathsRetained": 1,
    "sourceAuthorityReconciliationsOpen": 7,
    "silentlyClosedItems": 0,
}, "V11 retained backlog drift")

publication = v11.get("publicationBoundary", {})
for key in (
    "allCurrentlyAssembledReadersReviewedAgainstCurrentAuthority",
    "wholeBookReaderAssemblyComplete",
    "wholeBookCitationPassComplete",
    "wholeBookTransitionDedupPassComplete",
    "wholeBookLineEditComplete",
    "manuscriptBundleComplete",
    "productReleaseComplete",
    "productSourceRepairsComplete",
    "dossierUrlHoldsResolved",
    "dossierSourceUrlRepairsComplete",
    "unresolvedInternalPathsResolved",
    "nativeSourceAuthorityReconciliationComplete",
):
    require(publication.get(key) is False, f"V11 falsely closes publication boundary: {key}")
require(publication.get("newDirectQuotesApproved") == 0, "V11 publication boundary approves direct quotes")
require(v11.get("nextTransaction", {}).get("type") == "NATIVE_AUTHORITY_ENTRY_CITATION_PASS", "V11 next transaction type drift")
require(v11.get("nextTransaction", {}).get("preferredEntryId") == "HEART-BOOK-V", "V11 next entry must remain Part V")

require(HUMAN.is_file(), "human source-authority correction record missing")
if HUMAN.is_file():
    human = HUMAN.read_text(encoding="utf-8")
    for marker in (
        "10 / 10 owner-specs расходятся",
        "CURRENT NATIVE-AUTHORITY CITATION PASSES COMPLETE = 6 / 18",
        "CURRENT CITATION PASSES OPEN = 12 / 18",
        "ASSEMBLED READERS = 14 / 18",
        "dossier URL HOLDs: **55**",
        "NEXT = HEART-BOOK-V NATIVE-AUTHORITY ENTRY CITATION PASS",
    ):
        require(marker in human, f"human correction record missing marker: {marker}")

if errors:
    print("Heart Product source-authority reconciliation: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart Product source-authority reconciliation: PASS — 10/10 MDX owner specs diverge; seven historical passes reopened; current native authority 6/18")
