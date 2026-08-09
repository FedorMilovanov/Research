#!/usr/bin/env python3
"""Calibrate Heart Product citation surfaces against current native source authority.

This first red calibration intentionally has no mergeable authority receipt yet.
It derives Product owners from the immutable whole-book inventory, resolves each
reference-only MDX through the Product route profile to the native Astro Body,
and prints one deterministic manifest. A follow-up commit must pin that manifest
and remove the calibration failure before this lane can merge.
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
BUILDER_BLOB = "6e8fb1af57bc72d26a9ca91d5b84b1fec3de7f12"
PRODUCT_COMMIT = "0fbe7d1ead9ebd1bea867418e254da438ec63329"

errors: list[str] = []


def require(value: bool, message: str) -> None:
    if not value:
        errors.append(message)


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
    for pattern in (
        re.compile(r"«([^»\n]{8,})»"),
        re.compile(r"“([^”\n]{8,})”"),
    ):
        for match in pattern.finditer(text):
            value = normalize_semantic(match.group(1))
            if value:
                values.append(value)

    # Group contiguous Markdown quote lines as one semantic block.
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
    imports = re.findall(
        r"import\s+([A-Za-z0-9_]*Body)\s+from\s+['\"]@/([^'\"]+\.astro)['\"]\s*;?",
        page,
    )
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
    parity = all(
        not diff[side]
        for diff in set_diffs.values()
        for side in ("missingFromNative", "nativeOnly")
    )

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
        "legacyBodyOnlySurface": {
            "counts": legacy_surface["counts"],
            "hashes": legacy_surface["hashes"],
        },
        "nativeSurface": {
            "counts": native_surface["counts"],
            "hashes": native_surface["hashes"],
        },
        "citationSurfaceParity": parity,
        "diff": set_diffs,
    })
    require(parity, f"{resolution['slug']} sections={sections}: native citation surfaces differ from reference MDX body")

summary = {
    "schemaVersion": 1,
    "authorityId": "HEART-PRODUCT-SOURCE-AUTHORITY-PARITY-CALIBRATION-2026-08-09",
    "researchBase": "062a7fe14d98c89fe04fc376fdfeb8bb2b060378",
    "productSnapshot": PRODUCT_COMMIT,
    "historicalBuilderBlob": BUILDER_BLOB,
    "ownerSpecsChecked": len(rows),
    "uniqueSlugsChecked": len({row["slug"] for row in rows}),
    "allCitationSurfacesParity": bool(rows) and all(row["citationSurfaceParity"] for row in rows),
    "rows": rows,
}
summary["manifestSha256"] = sha_json(summary["rows"])
print("HEART_PRODUCT_SOURCE_AUTHORITY_CALIBRATION=" + json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(",", ":")))

# Red-first calibration: even a semantically green manifest is not merge authority
# until a second commit freezes the emitted manifest in an immutable receipt.
errors.append("CALIBRATION_ONLY: freeze the emitted native-authority manifest in a versioned receipt before merge")

print("Heart Product source-authority parity: FAIL (calibration)", file=sys.stderr)
for error in errors:
    print(f"- {error}", file=sys.stderr)
raise SystemExit(1)
