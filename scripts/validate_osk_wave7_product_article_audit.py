#!/usr/bin/env python3
"""Validate OSK Wave 7 against the exact checked-out Product commit and blob."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "data/osk-wave7-product-article-audit-2026-08-01.json"
REGISTRY_PATH = ROOT / "data/osk-wave7-article-audit-source-registry-2026-08-01.json"
REPORT_PATH = ROOT / "ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/41_WAVE7_PRODUCT_ARTICLE_PARAGRAPH_AUDIT_2026-08-01.md"
ROOT_AUTHORITY_PATH = ROOT / "00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md"
AUTHORITY_ID = "RESEARCH-OSK-AUTHORITY-2026-08-01-W7"
EXPECTED_PRODUCT = "efaf2a51b1fcc7b7d3f8c9558ecb5acf849df3b3"
EXPECTED_BLOB = "c7d3e1be69d81d3dec299d7d6ebcfa015548b459"
CANONICAL_SOURCE = "src/components/article-pilots/antisovetov/AntisovetovBody.astro"
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)} must contain an object")
        return {}
    return value


def nonempty(value: Any, context: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{context}: non-empty string required")
    return value.strip() if isinstance(value, str) else ""


def git(repo: Path, *args: str) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def verify_product() -> None:
    raw = os.environ.get("PRODUCT_REPO", "").strip()
    require(bool(raw), "PRODUCT_REPO is required")
    if not raw:
        return
    repo = Path(raw).resolve()
    require((repo / ".git").exists(), f"PRODUCT_REPO is not a Git checkout: {repo}")
    if not (repo / ".git").exists():
        return
    code, head, stderr = git(repo, "rev-parse", "HEAD")
    require(code == 0, f"Product rev-parse HEAD failed: {stderr}")
    require(head == EXPECTED_PRODUCT, f"Product HEAD drift: {head} != {EXPECTED_PRODUCT}")
    code, _, stderr = git(repo, "cat-file", "-e", f"{EXPECTED_PRODUCT}^{{commit}}")
    require(code == 0, f"Product commit unavailable: {stderr}")
    source = repo / CANONICAL_SOURCE
    require(source.is_file(), f"Product canonical source missing: {CANONICAL_SOURCE}")
    code, commit_blob, stderr = git(repo, "rev-parse", f"{EXPECTED_PRODUCT}:{CANONICAL_SOURCE}")
    require(code == 0, f"Product commit:path lookup failed: {stderr}")
    require(commit_blob == EXPECTED_BLOB, f"Product commit blob drift: {commit_blob} != {EXPECTED_BLOB}")
    code, working_blob, stderr = git(repo, "hash-object", CANONICAL_SOURCE)
    require(code == 0, f"Product working-byte hash failed: {stderr}")
    require(working_blob == EXPECTED_BLOB, f"Product working bytes drift: {working_blob} != {EXPECTED_BLOB}")
    code, status, stderr = git(repo, "status", "--porcelain")
    require(code == 0, f"Product status failed: {stderr}")
    require(not status, "Product checkout is dirty")


def main() -> int:
    verify_product()
    audit = load(AUDIT_PATH)
    registry = load(REGISTRY_PATH)
    for document, label in ((audit, "audit"), (registry, "registry")):
        require(document.get("schema_version") == 1, f"{label}: schema_version drift")
        require(document.get("authority_id") == AUTHORITY_ID, f"{label}: authority_id drift")
        require(document.get("product_snapshot") == EXPECTED_PRODUCT, f"{label}: product snapshot drift")
        require(document.get("canonical_source") == CANONICAL_SOURCE, f"{label}: canonical source drift")
        require(document.get("canonical_blob_sha") == EXPECTED_BLOB, f"{label}: canonical blob drift")
    require(
        audit.get("source_registry") == REGISTRY_PATH.relative_to(ROOT).as_posix(),
        "audit source-registry pointer drift",
    )

    sources = registry.get("sources", [])
    require(isinstance(sources, list) and len(sources) == 54, "exactly 54 source records required")
    if not isinstance(sources, list):
        sources = []
    source_ids: list[str] = []
    urls: list[str] = []
    families: Counter[str] = Counter()
    for index, source in enumerate(sources):
        require(isinstance(source, dict), f"sources[{index}] must be an object")
        if not isinstance(source, dict):
            continue
        sid = nonempty(source.get("id"), f"sources[{index}].id")
        nonempty(source.get("category"), sid)
        nonempty(source.get("title"), sid)
        url = nonempty(source.get("url"), sid)
        nonempty(source.get("purpose"), sid)
        nonempty(source.get("source_class"), sid)
        require(url.startswith("https://"), f"{sid}: HTTPS required")
        require(source.get("quote_safe") is False, f"{sid}: Wave 7 approves no direct quotation")
        source_ids.append(sid)
        urls.append(url)
        if sid.startswith("W7-BIB-"):
            families["biblical"] += 1
        elif sid.startswith("W7-PSY-"):
            families["psychology"] += 1
        elif sid.startswith("W7-SAF-"):
            families["safeguarding"] += 1
        else:
            errors.append(f"{sid}: invalid source family")
    require(len(source_ids) == len(set(source_ids)) == 54, "source IDs must be 54 unique values")
    require(len(urls) == len(set(urls)) == 54, "source URLs must be 54 unique values")
    require(families == {"biblical": 18, "psychology": 18, "safeguarding": 18}, f"source family drift: {dict(families)}")
    require(
        registry.get("counters") == {
            "source_records": 54,
            "biblical_lexical_exegetical": 18,
            "psychology_organization": 18,
            "safeguarding_pastoral_governance": 18,
            "unique_urls": 54,
            "new_direct_quotes_approved": 0,
        },
        "registry counters drift",
    )
    source_id_set = set(source_ids)

    require(
        audit.get("decision") == {
            "product_disposition": "REFERENCE",
            "product_write_performed": False,
            "current_body_owner": "CONCEPTUAL_BIBLICAL_PASTORAL_CORE",
            "next_product_action": "APPLY_14_MANDATORY_FIXES_AND_12_SOURCE_NOTES_IN_SEPARATE_PR",
            "new_case_roster_approved": False,
            "new_direct_quotes_approved": False,
        },
        "Wave 7 product decision drift",
    )

    points = audit.get("point_records", [])
    require(isinstance(points, list) and len(points) == 20, "exactly 20 point records required")
    if not isinstance(points, list):
        points = []
    seen_points: set[int] = set()
    for point in points:
        require(isinstance(point, dict), "point record must be an object")
        if not isinstance(point, dict):
            continue
        number = point.get("point_number")
        require(isinstance(number, int) and 1 <= number <= 20, f"invalid point number: {number}")
        if not isinstance(number, int):
            continue
        require(point.get("id") == f"W7-P{number:02d}", f"point {number}: id drift")
        require(point.get("anchor") == f"point-{number}", f"point {number}: anchor drift")
        require(number not in seen_points, f"duplicate point number: {number}")
        seen_points.add(number)
        nonempty(point.get("heading"), f"point {number}.heading")
        nonempty(point.get("note"), f"point {number}.note")
        require(point.get("disposition") == "PRESERVE_WITH_BOUNDARY", f"point {number}: disposition drift")
        for field in ("product_edit_required", "case_roster_approved", "new_direct_quote_approved"):
            require(point.get(field) is False, f"point {number}: {field} must be false")
    require(seen_points == set(range(1, 21)), "point coverage drift")
    if len(points) >= 19:
        require("no-merits" in points[3].get("note", "") and "no-merits" in points[18].get("note", ""), "Platt no-merits boundary missing")
        require("Gray and Guay" in points[8].get("note", ""), "Gray/Guay exclusion missing")

    fixes = audit.get("mandatory_fixes", [])
    notes = audit.get("source_notes", [])
    require(isinstance(fixes, list) and len(fixes) == 14, "exactly 14 mandatory fixes required")
    require(isinstance(notes, list) and len(notes) == 12, "exactly 12 source notes required")
    if not isinstance(fixes, list):
        fixes = []
    if not isinstance(notes, list):
        notes = []
    fix_ids: list[str] = []
    severities: Counter[str] = Counter()
    critical: list[dict] = []
    for fix in fixes:
        require(isinstance(fix, dict), "fix must be an object")
        if not isinstance(fix, dict):
            continue
        fid = nonempty(fix.get("id"), "fix.id")
        for field in ("selector", "class", "action", "direction"):
            nonempty(fix.get(field), f"{fid}.{field}")
        severity = nonempty(fix.get("severity"), f"{fid}.severity")
        require(severity in {"CRITICAL", "HIGH", "MEDIUM"}, f"{fid}: invalid severity")
        refs = fix.get("source_ids", [])
        require(isinstance(refs, list) and bool(refs) and set(refs) <= source_id_set, f"{fid}: invalid source references")
        fix_ids.append(fid)
        severities[severity] += 1
        if severity == "CRITICAL":
            critical.append(fix)
    require(len(fix_ids) == len(set(fix_ids)) == 14, "mandatory-fix IDs must be unique")
    require(severities == {"CRITICAL": 1, "HIGH": 8, "MEDIUM": 5}, f"severity drift: {dict(severities)}")
    if critical:
        require(critical[0].get("id") == "W7-FIX-07", "critical fix ID drift")
        require("1 Тим. 5:19" in critical[0].get("selector", ""), "critical 1 Timothy 5:19 selector missing")

    note_ids: list[str] = []
    for note in notes:
        require(isinstance(note, dict), "source note must be an object")
        if not isinstance(note, dict):
            continue
        nid = nonempty(note.get("id"), "source-note.id")
        for field in ("term", "action", "boundary"):
            nonempty(note.get(field), f"{nid}.{field}")
        refs = note.get("source_ids", [])
        require(isinstance(refs, list) and bool(refs) and set(refs) <= source_id_set, f"{nid}: invalid source references")
        note_ids.append(nid)
    require(len(note_ids) == len(set(note_ids)) == 12, "source-note IDs must be unique")

    require(
        audit.get("counters") == {
            "point_records": 20,
            "preserve_with_boundary": 20,
            "mandatory_fixes": 14,
            "critical_fixes": 1,
            "high_fixes": 8,
            "medium_fixes": 5,
            "source_notes": 12,
            "source_records": 54,
            "product_files_changed": 0,
        },
        "audit counters drift",
    )
    try:
        authority_text = REPORT_PATH.read_text(encoding="utf-8") + ROOT_AUTHORITY_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"authority text read failed: {exc}")
        authority_text = ""
    for marker in ("Wave 7", "14", "12", "54", "1 CRITICAL", "PRODUCT FIX NOT YET APPLIED", "Wave 8"):
        require(marker in authority_text, f"authority marker missing: {marker}")

    if errors:
        print(f"OSK Wave 7: FAIL ({len(errors)})", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("OSK Wave 7: PASS — exact Product commit/blob verified; 20 points, 14 fixes, 12 notes, 54 sources, 0 writes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
