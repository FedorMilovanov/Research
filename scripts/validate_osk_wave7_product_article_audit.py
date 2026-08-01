#!/usr/bin/env python3
"""Fail-closed OSK Wave 7 audit with real cross-repository Product verification."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/osk-wave7-product-article-audit-2026-08-01.json"
SOURCES = ROOT / "data/osk-wave7-article-audit-source-registry-2026-08-01.json"
AUTHORITY = ROOT / "ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/41_WAVE7_PRODUCT_ARTICLE_PARAGRAPH_AUDIT_2026-08-01.md"
ROOT_AUTH = ROOT / "00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md"
EXPECTED_PRODUCT = "efaf2a51b1fcc7b7d3f8c9558ecb5acf849df3b3"
EXPECTED_BLOB = "c7d3e1be45bacbb538126c76d50399920aa53ec7"
CANONICAL_SOURCE = "src/components/article-pilots/antisovetov/AntisovetovBody.astro"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)}: object required")
    return value


def text(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{context}: non-empty string required")
    return value.strip()


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        fail(f"Product git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def verify_product_snapshot() -> None:
    raw = os.environ.get("PRODUCT_REPO", "").strip()
    if not raw:
        fail("PRODUCT_REPO is required; validator must run against a checked-out Product snapshot")
    repo = Path(raw).resolve()
    if not (repo / ".git").exists():
        fail(f"PRODUCT_REPO is not a Git checkout: {repo}")
    head = git(repo, "rev-parse", "HEAD")
    if head != EXPECTED_PRODUCT:
        fail(f"Product HEAD drift: {head} != {EXPECTED_PRODUCT}")
    if git(repo, "cat-file", "-e", f"{EXPECTED_PRODUCT}^{{commit}}"):
        fail("unreachable")
    path = repo / CANONICAL_SOURCE
    if not path.is_file():
        fail(f"Product canonical source missing: {CANONICAL_SOURCE}")
    actual_blob = git(repo, "rev-parse", f"{EXPECTED_PRODUCT}:{CANONICAL_SOURCE}")
    if actual_blob != EXPECTED_BLOB:
        fail(f"Product blob drift: {actual_blob} != {EXPECTED_BLOB}")
    working_blob = git(repo, "hash-object", CANONICAL_SOURCE)
    if working_blob != EXPECTED_BLOB:
        fail(f"checked-out Product bytes differ from pinned blob: {working_blob} != {EXPECTED_BLOB}")
    if git(repo, "status", "--porcelain"):
        fail("Product checkout is dirty")


def main() -> None:
    verify_product_snapshot()
    audit = load(AUDIT)
    registry = load(SOURCES)
    for obj, name in ((audit, "audit"), (registry, "registry")):
        if obj.get("schema_version") != 1 or obj.get("authority_id") != "RESEARCH-OSK-AUTHORITY-2026-08-01-W7":
            fail(f"{name}: authority drift")
        if obj.get("product_snapshot") != EXPECTED_PRODUCT:
            fail(f"{name}: Product snapshot declaration drift")
        if obj.get("canonical_source") != CANONICAL_SOURCE:
            fail(f"{name}: canonical source drift")
        if obj.get("canonical_blob_sha") != EXPECTED_BLOB:
            fail(f"{name}: Product blob declaration drift")
    if audit.get("source_registry") != "data/osk-wave7-article-audit-source-registry-2026-08-01.json":
        fail("source registry pointer drift")

    sources = registry.get("sources")
    if not isinstance(sources, list) or len(sources) != 54:
        fail("exactly 54 source records required")
    ids: list[str] = []
    urls: list[str] = []
    categories: Counter[str] = Counter()
    allowed_classes = {"A1", "A2", "A3", "B1", "BIBLICAL_PRIMARY", "ACADEMIC", "OFFICIAL_GUIDANCE"}
    for row in sources:
        if not isinstance(row, dict):
            fail("source object required")
        sid = text(row.get("id"), "source id")
        category = text(row.get("category"), sid)
        text(row.get("title"), sid)
        url = text(row.get("url"), sid)
        text(row.get("purpose"), sid)
        source_class = text(row.get("source_class"), sid)
        if source_class not in allowed_classes:
            fail(f"{sid}: unsupported source class {source_class}")
        if not url.startswith("https://"):
            fail(f"{sid}: HTTPS required")
        if row.get("quote_safe") is not False:
            fail(f"{sid}: Wave 7 approves no direct quotations")
        ids.append(sid)
        urls.append(url)
        if sid.startswith("W7-BIB-"):
            categories["biblical"] += 1
        elif sid.startswith("W7-PSY-"):
            categories["psychology"] += 1
        elif sid.startswith("W7-SAF-"):
            categories["safeguarding"] += 1
        else:
            fail(f"{sid}: invalid source family {category}")
    if len(set(ids)) != 54 or len(set(urls)) != 54:
        fail("source IDs and URLs must be unique")
    if categories != {"biblical": 18, "psychology": 18, "safeguarding": 18}:
        fail(f"source family drift: {dict(categories)}")
    expected_source_counts = {
        "source_records": 54,
        "biblical_lexical_exegetical": 18,
        "psychology_organization": 18,
        "safeguarding_pastoral_governance": 18,
        "unique_urls": 54,
        "new_direct_quotes_approved": 0,
    }
    if registry.get("counters") != expected_source_counts:
        fail("source counter drift")
    source_ids = set(ids)

    decision = audit.get("decision")
    expected_decision = {
        "product_disposition": "REFERENCE",
        "product_write_performed": False,
        "current_body_owner": "CONCEPTUAL_BIBLICAL_PASTORAL_CORE",
        "next_product_action": "APPLY_14_MANDATORY_FIXES_AND_12_SOURCE_NOTES_IN_SEPARATE_PR",
        "new_case_roster_approved": False,
        "new_direct_quotes_approved": False,
    }
    if decision != expected_decision:
        fail("product decision drift")

    points = audit.get("point_records")
    if not isinstance(points, list) or len(points) != 20:
        fail("exactly 20 point records required")
    seen: set[int] = set()
    for point in points:
        if not isinstance(point, dict):
            fail("point object required")
        number = point.get("point_number")
        if number not in range(1, 21) or point.get("id") != f"W7-P{number:02d}" or point.get("anchor") != f"point-{number}" or number in seen:
            fail(f"point identity drift: {point}")
        seen.add(number)
        text(point.get("heading"), f"point {number}")
        text(point.get("note"), f"point {number}")
        if point.get("disposition") != "PRESERVE_WITH_BOUNDARY":
            fail(f"point {number}: disposition drift")
        for flag in ("product_edit_required", "case_roster_approved", "new_direct_quote_approved"):
            if point.get(flag) is not False:
                fail(f"point {number}: {flag} must be false")
    if seen != set(range(1, 21)):
        fail("point coverage drift")
    if "no-merits" not in points[3]["note"] or "no-merits" not in points[18]["note"]:
        fail("Platt boundary missing from points 4/19")
    if "Gray and Guay" not in points[8]["note"]:
        fail("Gray/Guay exclusion missing from point 9")

    fixes = audit.get("mandatory_fixes")
    notes = audit.get("source_notes")
    if not isinstance(fixes, list) or len(fixes) != 14:
        fail("exactly 14 mandatory fixes required")
    if not isinstance(notes, list) or len(notes) != 12:
        fail("exactly 12 source notes required")
    fix_ids: list[str] = []
    severities: Counter[str] = Counter()
    critical: list[dict] = []
    for item in fixes:
        if not isinstance(item, dict):
            fail("fix object required")
        fid = text(item.get("id"), "fix id")
        for field in ("selector", "class", "action", "direction"):
            text(item.get(field), fid)
        severity = text(item.get("severity"), fid)
        if severity not in {"CRITICAL", "HIGH", "MEDIUM"}:
            fail(f"{fid}: invalid severity")
        refs = item.get("source_ids")
        if not isinstance(refs, list) or not refs or not set(refs) <= source_ids:
            fail(f"{fid}: invalid source references")
        fix_ids.append(fid)
        severities[severity] += 1
        if severity == "CRITICAL":
            critical.append(item)
    if len(set(fix_ids)) != 14 or severities != {"CRITICAL": 1, "HIGH": 8, "MEDIUM": 5}:
        fail(f"fix severity drift: {dict(severities)}")
    if critical[0].get("id") != "W7-FIX-07" or "1 Тим. 5:19" not in critical[0].get("selector", ""):
        fail("critical fix must remain the 1 Timothy 5:19 correction")

    note_ids: list[str] = []
    for item in notes:
        if not isinstance(item, dict):
            fail("source note object required")
        nid = text(item.get("id"), "note id")
        for field in ("term", "action", "boundary"):
            text(item.get(field), nid)
        refs = item.get("source_ids")
        if not isinstance(refs, list) or not refs or not set(refs) <= source_ids:
            fail(f"{nid}: invalid source references")
        note_ids.append(nid)
    if len(set(note_ids)) != 12:
        fail("duplicate source-note IDs")

    expected_audit_counts = {
        "point_records": 20,
        "preserve_with_boundary": 20,
        "mandatory_fixes": 14,
        "critical_fixes": 1,
        "high_fixes": 8,
        "medium_fixes": 5,
        "source_notes": 12,
        "source_records": 54,
        "product_files_changed": 0,
    }
    if audit.get("counters") != expected_audit_counts:
        fail("audit counter drift")

    combined = AUTHORITY.read_text(encoding="utf-8") + ROOT_AUTH.read_text(encoding="utf-8")
    for marker in ("Wave 7", "20", "14", "12", "54", "1 CRITICAL", "PRODUCT FIX NOT YET APPLIED", "Wave 8"):
        if marker not in combined:
            fail(f"authority marker missing: {marker}")
    print(
        "OSK Wave 7: PASS — real Product commit/blob verified; "
        "20 points, 14 mandatory fixes, 12 source notes, 54 sources, 0 Product writes"
    )


if __name__ == "__main__":
    main()
