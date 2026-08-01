#!/usr/bin/env python3
"""Validate Bratsky Listok authority, historical commit pins, and byte identity."""
from __future__ import annotations

import base64
import csv
import gzip
import hashlib
import io
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
M_PATH = ROOT / "data/bratsky-listok-authority-manifest.json"
L_PATH = ROOT / "data/bratsky-listok-publication-ledger.json"
STAGES: tuple[dict[str, Any], ...] = (
    {"stage": 18, "path": "RUSSIAN_BAPTISTS_ARCHIVE/bratsky_listok_primary_page_map_stage18_2026-07-31.csv", "commit": "30cd0cbb4f65644ff40d82f5120546023657d9b2", "encoding": "csv"},
    {"stage": 19, "path": "RUSSIAN_BAPTISTS_ARCHIVE/bratsky_listok_primary_page_map_stage19_2026-07-31.csv", "commit": "f9a393c1262bd9a0eaa0336f5b9472da49576dc9", "encoding": "csv"},
    {"stage": 20, "path": "RUSSIAN_BAPTISTS_ARCHIVE/bratsky_listok_primary_page_map_stage20_2026-07-31.csv", "commit": "223e1acfe05bf91dfb0fededa8c037cc531c2933", "encoding": "csv"},
    {"stage": 21, "path": "RUSSIAN_BAPTISTS_ARCHIVE/bratsky_listok_primary_page_map_stage21_2026-07-31.csv", "commit": "c832ed1dbb88bbbbd65547173e42f96d2bce86cb", "encoding": "csv"},
    {"stage": 22, "path": "RUSSIAN_BAPTISTS_ARCHIVE/BRATSKY_LISTOK_PRIMARY_PAGE_MAP_STAGE22_2026-08-01.csv", "commit": "939c2b398aa2b5b1af28c8a6fd31c8cd0baf2d2b", "encoding": "csv"},
    {"stage": 23, "path": "RUSSIAN_BAPTISTS_ARCHIVE/BRATSKY_LISTOK_PRIMARY_PAGE_MAP_STAGE23_2026-08-01.csv", "commit": "f3601a30f071385da8987acf1d96090b28a6af52", "encoding": "csv"},
    {"stage": 24, "path": "RUSSIAN_BAPTISTS_ARCHIVE/BRATSKY_LISTOK_PRIMARY_PAGE_MAP_STAGE24_2026-08-01.csv", "commit": "a9e020058e3b0d5e17439a6ee05ee84a9f5cb64a", "encoding": "csv"},
    {"stage": 25, "path": "RUSSIAN_BAPTISTS_ARCHIVE/BRATSKY_LISTOK_PRIMARY_PAGE_MAP_STAGE25_2026-08-01.csv.gz.b64", "commit": "3da5aab25505b4ccd91b629bc20bfc2ff26c434b", "blobSha": "d06cd8959bfc854f9efc75c3f0005235167f51dd", "encoding": "base64+gzip+csv"},
)
CROSS_ISSUE_RECORDS: tuple[dict[str, Any], ...] = (
    {"stage": 25, "recordId": "BL25-CROSS-1905-CONGRESS-CALENDAR", "role": "cross-issue-synthesis", "issueKeyRequired": False},
    {"stage": 25, "recordId": "BL25-CROSS-1906-1908-UNION-PRECURSOR", "role": "cross-issue-synthesis", "issueKeyRequired": False},
)
CROSS_KEYS = {(item["stage"], item["recordId"]) for item in CROSS_ISSUE_RECORDS}
LOCAL = {
    (1906, 6), (1906, 7), (1906, 8), (1906, 9), (1906, 11),
    (1907, 9), (1907, 11), (1907, 12),
    (1908, 2), (1908, 5), (1908, 8), (1908, 10), (1908, 11),
    (1909, 2), (1909, 7), (1909, 9), (1909, 10),
    (1910, 6), (1910, 7), (1910, 8), (1910, 11), (1910, 12),
}
UNKNOWN = {(1907, 4), (1908, 6), (1908, 9), (1909, 5), (1910, 1), (1910, 3), (1910, 4), (1910, 5)}
COVERAGE = Counter(full=17, targeted=4, truncated=1)
SUMMARY = {"binaryFilesRetained": 23, "semanticPositions": 22, "fullMaps": 17, "truncatedFragments": 1, "targetedMaps": 4, "unmappedLocalPositions": 0}
COLS = {"record_id", "year", "issue", "primary_heading", "content_summary", "evidence_status", "source_sha256", "transcription_guard"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(ROOT), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)} must contain an object")
        return {}
    return value


def verify_stage_git_object(spec: dict[str, Any], errors: list[str]) -> str:
    """Verify commit:path, pinned blob where supplied, and current working bytes."""
    stage = spec["stage"]
    commit = spec["commit"]
    rel = spec["path"]
    commit_check = git("cat-file", "-e", f"{commit}^{{commit}}")
    if commit_check.returncode:
        errors.append(f"Stage{stage}: pinned commit unavailable: {commit}")
        return ""
    object_result = git("rev-parse", f"{commit}:{rel}")  # commit:path is the actual evidence pin
    if object_result.returncode:
        errors.append(f"Stage{stage}: path absent at pinned commit: {rel}")
        return ""
    historical_blob = object_result.stdout.strip()
    declared_blob = spec.get("blobSha")
    if declared_blob and declared_blob != historical_blob:
        errors.append(f"Stage{stage}: declared blob {declared_blob} != commit blob {historical_blob}")
    current_path = ROOT / rel
    current_result = git("hash-object", rel)
    if current_result.returncode:
        errors.append(f"Stage{stage}: cannot hash current path: {rel}")
        return historical_blob
    current_blob = current_result.stdout.strip()
    if current_blob != historical_blob:
        errors.append(f"Stage{stage}: current bytes drift from pinned commit blob: {current_blob} != {historical_blob}")
    if not current_path.is_file():
        errors.append(f"Stage{stage}: current path missing: {rel}")
    return historical_blob


def read_stage_rows(spec: dict[str, Any], errors: list[str]) -> list[dict[str, str]]:
    path = ROOT / spec["path"]
    label = f"Stage{spec['stage']}"
    if not path.is_file():
        errors.append(f"{label} evidence file is missing: {spec['path']}")
        return []
    try:
        if spec["encoding"] == "base64+gzip+csv":
            encoded = "".join(path.read_text(encoding="utf-8").split())
            text = gzip.decompress(base64.b64decode(encoded, validate=True)).decode("utf-8-sig")
        else:
            text = path.read_text(encoding="utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))
        missing = COLS - set(reader.fieldnames or [])
        if missing:
            errors.append(f"{label} missing columns: {sorted(missing)}")
        return list(reader)
    except (ValueError, OSError, UnicodeDecodeError, csv.Error, gzip.BadGzipFile) as exc:
        errors.append(f"{label} decode failed: {exc}")
        return []


def issue_key(row: dict[str, str]) -> tuple[int, int] | None:
    try:
        year = int((row.get("year") or "").strip())
    except ValueError:
        return None
    match = re.search(r"\d+", row.get("issue") or "")
    return (year, int(match.group())) if match else None


def main() -> int:
    errors: list[str] = []
    manifest = load_json(M_PATH, errors)
    ledger = load_json(L_PATH, errors)
    digest = hashlib.sha256(M_PATH.read_bytes()).hexdigest() if M_PATH.is_file() else ""
    if ledger.get("authorityManifestSha256") != digest:
        errors.append("authorityManifestSha256 does not match current manifest bytes")
    if manifest.get("schemaVersion") != 1 or ledger.get("schemaVersion") != 1:
        errors.append("both schemaVersion values must be 1")
    if manifest.get("seriesId") != "bratsky-listok-1906-1910" or ledger.get("seriesId") != manifest.get("seriesId"):
        errors.append("seriesId mismatch")
    if ledger.get("researchCommitPinRequired") is not True:
        errors.append("exact Research commit pin must be required")

    policy = manifest.get("policy", {})
    for field in {
        "siteImportRequiresPinnedResearchCommit", "siteImportRequiresManifestSha256",
        "pageMapIsNotAutomaticQuotePermission", "unknownIssueContentMayNotSupportAbsenceClaims",
        "rightsAndImageUseRequireSeparateDecision", "driveOperationalStateIsNotPublicationAuthority",
        "noIndividualStageIsCumulative",
    }:
        if not isinstance(policy, dict) or policy.get(field) is not True:
            errors.append(f"policy.{field} must be true")
    if not isinstance(policy, dict) or policy.get("completeSeriesClaimAllowed") is not False:
        errors.append("policy.completeSeriesClaimAllowed must be false")

    compiled = manifest.get("compiledEvidence", {})
    if not isinstance(compiled, dict):
        compiled = {}
        errors.append("compiledEvidence must be an object")
    if compiled.get("model") != "ordered-overlay-union":
        errors.append("compiledEvidence.model must be ordered-overlay-union")
    if compiled.get("artifacts") != list(STAGES):
        errors.append("compiledEvidence.artifacts differs from exact Stage18-25 chain")
    if compiled.get("crossIssueRecords") != list(CROSS_ISSUE_RECORDS):
        errors.append("compiledEvidence.crossIssueRecords differs from exact typed set")

    stage_blobs = {spec["stage"]: verify_stage_git_object(spec, errors) for spec in STAGES}

    positions = manifest.get("localPositions", [])
    if not isinstance(positions, list):
        positions = []
        errors.append("localPositions must be a list")
    ids: set[str] = set()
    keys: set[tuple[int, int]] = set()
    hashes: set[str] = set()
    record_ids: set[str] = set()
    coverage: Counter[str] = Counter()
    for index, item in enumerate(positions):
        if not isinstance(item, dict):
            errors.append(f"localPositions[{index}] must be an object")
            continue
        item_id = item.get("id")
        key = (item.get("year"), item.get("issue"))
        sha = item.get("canonicalSha256")
        record_id = item.get("evidenceRecordId")
        cls = item.get("coverageClass")
        if not isinstance(item_id, str) or not item_id or item_id in ids:
            errors.append(f"invalid/duplicate position id at {index}: {item_id!r}")
        else:
            ids.add(item_id)
        if not all(isinstance(value, int) for value in key) or key in keys:
            errors.append(f"invalid/duplicate semantic position at {index}: {key!r}")
        else:
            keys.add(key)
        if cls not in COVERAGE:
            errors.append(f"invalid coverage class at {index}: {cls!r}")
        else:
            coverage[cls] += 1
        if not isinstance(sha, str) or not SHA256_RE.fullmatch(sha) or sha in hashes:
            errors.append(f"invalid/duplicate canonical SHA-256 at {index}: {sha!r}")
        else:
            hashes.add(sha)
        if not isinstance(record_id, str) or not record_id or record_id in record_ids:
            errors.append(f"invalid/duplicate evidence record at {index}: {record_id!r}")
        else:
            record_ids.add(record_id)
    if keys != LOCAL:
        errors.append(f"local issue set differs: {sorted(keys ^ LOCAL)}")
    if coverage != COVERAGE:
        errors.append(f"coverage {dict(coverage)} != {dict(COVERAGE)}")
    if manifest.get("localCorpusSummary") != SUMMARY:
        errors.append("localCorpusSummary differs from 23/22/17/1/4/0 authority")

    unknown_items = manifest.get("unknownIssues", [])
    if not isinstance(unknown_items, list):
        unknown_items = []
        errors.append("unknownIssues must be a list")
    unknown = {(item.get("year"), item.get("issue")) for item in unknown_items if isinstance(item, dict)}
    if unknown != UNKNOWN:
        errors.append(f"unknown issue set differs: {sorted(unknown ^ UNKNOWN)}")
    if unknown & keys:
        errors.append("local and unknown issue sets overlap")
    for index, item in enumerate(unknown_items):
        if not isinstance(item, dict):
            continue
        if item.get("contentState") != "fully-unknown":
            errors.append(f"unknownIssues[{index}] must remain fully-unknown")
        if item.get("acquisitionState") != "ready-to-request-not-sent":
            errors.append(f"unknownIssues[{index}] request must remain unsent")

    expected_variant = {
        "positionId": "BL-1906-11",
        "canonicalSha256": "fb9030ad4a1309ab578374731c07180b885488406e46ead566b13d7b837a6554",
        "variantSha256": "67c1de40d68ea200c4cc1ea80fa61db6697437d84ad3a9365bad01db1de2bc25",
        "renderComparison": {"dpi": 120, "changedPages": 0},
        "policy": "one semantic issue; retain both binaries only as provenance",
    }
    if manifest.get("byteVariants") != [expected_variant]:
        errors.append("November 1906 byte-variant authority changed")

    all_rows: list[tuple[int, int, dict[str, str]]] = []
    csv_ids: set[str] = set()
    csv_hashes: set[str] = set()
    csv_keys: set[tuple[int, int]] = set()
    cross_seen: set[tuple[int, str]] = set()
    stage_row_counts: dict[int, int] = {}
    for spec in STAGES:
        stage = int(spec["stage"])
        rows = read_stage_rows(spec, errors)
        stage_row_counts[stage] = len(rows)
        if not rows:
            errors.append(f"Stage{stage} must contain at least one data row")
        for row_number, row in enumerate(rows, start=2):
            rid = (row.get("record_id") or "").strip()
            typed_key = (stage, rid)
            if not rid or rid in csv_ids:
                errors.append(f"Stage{stage} invalid/duplicate record_id at row {row_number}: {rid!r}")
            else:
                csv_ids.add(rid)
            csv_hashes.update(re.findall(r"[0-9a-f]{64}", row.get("source_sha256") or ""))
            key = issue_key(row)
            if typed_key in CROSS_KEYS:
                cross_seen.add(typed_key)
                if key is not None:
                    errors.append(f"Stage{stage} {rid}: cross-issue synthesis unexpectedly has issue key")
            elif key:
                csv_keys.add(key)
            else:
                errors.append(f"Stage{stage} {rid or row_number}: invalid year/issue")
            for field in ("primary_heading", "content_summary", "evidence_status", "transcription_guard"):
                if not (row.get(field) or "").strip():
                    errors.append(f"Stage{stage} {rid or row_number}: empty {field}")
            all_rows.append((stage, row_number, row))
    if cross_seen != CROSS_KEYS:
        errors.append(f"cross-issue synthesis set differs: {sorted(cross_seen ^ CROSS_KEYS)}")
    if hashes - csv_hashes:
        errors.append(f"compiled Stage18-25 union lacks canonical hashes: {sorted(hashes - csv_hashes)}")
    if LOCAL - csv_keys:
        errors.append(f"compiled Stage18-25 union lacks local positions: {sorted(LOCAL - csv_keys)}")

    bundles = ledger.get("bundles", [])
    expected_inputs = {"data/bratsky-listok-authority-manifest.json", *(spec["path"] for spec in STAGES)}
    if not isinstance(bundles, list) or len(bundles) != 1 or not isinstance(bundles[0], dict):
        errors.append("ledger must contain exactly one object bundle")
    else:
        bundle = bundles[0]
        if set(bundle.get("directInputs", [])) != expected_inputs:
            errors.append("bundle directInputs must be manifest + exact Stage18-25 chain")
        if bundle.get("sitePublicationEligible") is not False:
            errors.append("bundle must remain site-ineligible pending editorial/rights gates")
        if not any("no individual stage" in str(item).lower() for item in bundle.get("requiredDisclosures", [])):
            errors.append("bundle must disclose that no individual stage is cumulative")

    gap = ledger.get("gapAcquisition", {})
    expected_gap_ids = sorted(f"{year}-{issue:02d}" for year, issue in UNKNOWN)
    if not isinstance(gap, dict):
        errors.append("gapAcquisition must be an object")
    else:
        if sorted(gap.get("issues", [])) != expected_gap_ids:
            errors.append("ledger gap list differs")
        if gap.get("requestState") != "ready-to-request-not-sent":
            errors.append("BAN request must remain unsent")
        if gap.get("paymentAuthorized") is not False:
            errors.append("payment must remain unauthorized")

    if errors:
        print(f"Bratsky authority: FAIL ({len(errors)})", file=sys.stderr)
        for message in errors:
            print(f"- {message}", file=sys.stderr)
        return 1
    counts = ", ".join(f"S{stage}={count}" for stage, count in stage_row_counts.items())
    print(
        f"Bratsky authority: PASS — {len(keys)} local positions, {len(unknown)} unknown, "
        f"{len(all_rows)} evidence rows [{counts}], 8 historical commit/blob pins verified; "
        f"manifest sha256={digest}; blobs={stage_blobs}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
