#!/usr/bin/env python3
"""Validate the Bratsky Listok authority manifest and publication ledger."""

from __future__ import annotations

import base64
import csv
import gzip
import hashlib
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M_PATH = ROOT / "data/bratsky-listok-authority-manifest.json"
L_PATH = ROOT / "data/bratsky-listok-publication-ledger.json"
S25 = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/BRATSKY_LISTOK_PRIMARY_PAGE_MAP_STAGE25_2026-08-01.csv.gz.b64"
S24 = ROOT / "RUSSIAN_BAPTISTS_ARCHIVE/BRATSKY_LISTOK_PRIMARY_PAGE_MAP_STAGE24_2026-08-01.csv"
LOCAL = {
    (1906, 6), (1906, 7), (1906, 8), (1906, 9), (1906, 11),
    (1907, 9), (1907, 11), (1907, 12),
    (1908, 2), (1908, 5), (1908, 8), (1908, 10), (1908, 11),
    (1909, 2), (1909, 7), (1909, 9), (1909, 10),
    (1910, 6), (1910, 7), (1910, 8), (1910, 11), (1910, 12),
}
UNKNOWN = {
    (1907, 4), (1908, 6), (1908, 9), (1909, 5),
    (1910, 1), (1910, 3), (1910, 4), (1910, 5),
}
COVERAGE = Counter(full=17, targeted=4, truncated=1)
SUMMARY = {
    "binaryFilesRetained": 23,
    "semanticPositions": 22,
    "fullMaps": 17,
    "truncatedFragments": 1,
    "targetedMaps": 4,
    "unmappedLocalPositions": 0,
}
COLS = {
    "record_id", "year", "issue", "primary_heading", "content_summary",
    "evidence_status", "source_sha256", "transcription_guard",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def load(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)} must contain an object")
        return {}
    return value


def main() -> int:
    errors: list[str] = []
    manifest = load(M_PATH, errors)
    ledger = load(L_PATH, errors)
    try:
        manifest_bytes = M_PATH.read_bytes()
    except FileNotFoundError:
        manifest_bytes = b""

    digest = hashlib.sha256(manifest_bytes).hexdigest()
    if ledger.get("authorityManifestSha256") != digest:
        errors.append(
            "authorityManifestSha256 mismatch: "
            f"stored={ledger.get('authorityManifestSha256')} actual={digest}"
        )
    if manifest.get("schemaVersion") != 1 or ledger.get("schemaVersion") != 1:
        errors.append("both schemaVersion values must be 1")
    if manifest.get("seriesId") != "bratsky-listok-1906-1910":
        errors.append("unexpected manifest seriesId")
    if ledger.get("seriesId") != manifest.get("seriesId"):
        errors.append("ledger seriesId differs")
    if ledger.get("researchCommitPinRequired") is not True:
        errors.append("exact Research commit pin must be required")

    positions = manifest.get("localPositions", [])
    if not isinstance(positions, list):
        positions = []
        errors.append("localPositions must be a list")
    ids: set[str] = set()
    keys: set[tuple[int, int]] = set()
    hashes: set[str] = set()
    record_ids: set[str] = set()
    coverage: Counter[str] = Counter()
    for n, item in enumerate(positions):
        if not isinstance(item, dict):
            errors.append(f"localPositions[{n}] must be an object")
            continue
        item_id = item.get("id")
        key = (item.get("year"), item.get("issue"))
        sha = item.get("canonicalSha256")
        record_id = item.get("evidenceRecordId")
        cls = item.get("coverageClass")
        if not isinstance(item_id, str) or not item_id or item_id in ids:
            errors.append(f"invalid/duplicate position id at {n}: {item_id!r}")
        else:
            ids.add(item_id)
        if not all(isinstance(x, int) for x in key) or key in keys:
            errors.append(f"invalid/duplicate semantic position at {n}: {key!r}")
        else:
            keys.add(key)
        if cls not in COVERAGE:
            errors.append(f"invalid coverage class at {n}: {cls!r}")
        else:
            coverage[cls] += 1
        if not isinstance(sha, str) or not SHA256.fullmatch(sha) or sha in hashes:
            errors.append(f"invalid/duplicate canonical SHA-256 at {n}: {sha!r}")
        else:
            hashes.add(sha)
        if not isinstance(record_id, str) or not record_id or record_id in record_ids:
            errors.append(f"invalid/duplicate evidence record at {n}: {record_id!r}")
        else:
            record_ids.add(record_id)

    if keys != LOCAL:
        errors.append(f"local issue set differs: {sorted(keys ^ LOCAL)}")
    if coverage != COVERAGE:
        errors.append(f"coverage {dict(coverage)} != {dict(COVERAGE)}")
    if manifest.get("localCorpusSummary") != SUMMARY:
        errors.append("localCorpusSummary differs from the 23/22/17/1/4/0 authority")

    unknown_items = manifest.get("unknownIssues", [])
    if not isinstance(unknown_items, list):
        unknown_items = []
        errors.append("unknownIssues must be a list")
    unknown = {
        (item.get("year"), item.get("issue"))
        for item in unknown_items if isinstance(item, dict)
    }
    if unknown != UNKNOWN:
        errors.append(f"unknown issue set differs: {sorted(unknown ^ UNKNOWN)}")
    if unknown & keys:
        errors.append("local and unknown issue sets overlap")
    for n, item in enumerate(unknown_items):
        if not isinstance(item, dict):
            continue
        if item.get("contentState") != "fully-unknown":
            errors.append(f"unknownIssues[{n}] must remain fully-unknown")
        if item.get("acquisitionState") != "ready-to-request-not-sent":
            errors.append(f"unknownIssues[{n}] request must remain unsent")

    variants = manifest.get("byteVariants", [])
    expected_variant = {
        "positionId": "BL-1906-11",
        "canonicalSha256": "fb9030ad4a1309ab578374731c07180b885488406e46ead566b13d7b837a6554",
        "variantSha256": "67c1de40d68ea200c4cc1ea80fa61db6697437d84ad3a9365bad01db1de2bc25",
        "renderComparison": {"dpi": 120, "changedPages": 0},
        "policy": "one semantic issue; retain both binaries only as provenance",
    }
    if variants != [expected_variant]:
        errors.append("November 1906 byte-variant authority changed")

    active = manifest.get("activeEvidence", {})
    if active.get("path") != str(S25.relative_to(ROOT)):
        errors.append("Stage25 is not the active evidence path")
    if active.get("commit") != "3da5aab25505b4ccd91b629bc20bfc2ff26c434b":
        errors.append("Stage25 evidence commit changed")
    superseded = manifest.get("supersededArtifacts", [])
    if not any(
        isinstance(x, dict)
        and x.get("path") == str(S24.relative_to(ROOT))
        and x.get("status") == "superseded-by-stage25"
        and x.get("directPublicationInput") is False
        for x in superseded
    ):
        errors.append("Stage24 must remain superseded and non-publication")
    if not S24.is_file():
        errors.append("Stage24 historical predecessor is missing")

    rows: list[dict[str, str]] = []
    if not S25.is_file():
        errors.append("Stage25 active evidence is missing")
    else:
        try:
            encoded = "".join(S25.read_text(encoding="utf-8").split())
            decoded = gzip.decompress(base64.b64decode(encoded, validate=True)).decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(decoded))
            missing = COLS - set(reader.fieldnames or [])
            if missing:
                errors.append(f"Stage25 missing columns: {sorted(missing)}")
            rows = list(reader)
        except (ValueError, OSError, UnicodeDecodeError, csv.Error) as exc:
            errors.append(f"Stage25 decode failed: {exc}")

    if rows:
        csv_ids: set[str] = set()
        csv_hashes: set[str] = set()
        csv_keys: set[tuple[int, int]] = set()
        for n, row in enumerate(rows, start=2):
            rid = (row.get("record_id") or "").strip()
            if not rid or rid in csv_ids:
                errors.append(f"Stage25 invalid/duplicate record_id at row {n}: {rid!r}")
            csv_ids.add(rid)
            csv_hashes.update(re.findall(r"[0-9a-f]{64}", row.get("source_sha256") or ""))
            try:
                year = int((row.get("year") or "").strip())
            except ValueError:
                year = 0
            match = re.search(r"\d+", row.get("issue") or "")
            if year and match:
                csv_keys.add((year, int(match.group())))
            for field in ("primary_heading", "content_summary", "evidence_status", "transcription_guard"):
                if not (row.get(field) or "").strip():
                    errors.append(f"Stage25 {rid or n}: empty {field}")
        if hashes - csv_hashes:
            errors.append(f"Stage25 lacks canonical hashes: {sorted(hashes - csv_hashes)}")
        if LOCAL - csv_keys:
            errors.append(f"Stage25 lacks local positions: {sorted(LOCAL - csv_keys)}")

    bundles = ledger.get("bundles", [])
    expected_inputs = {
        "data/bratsky-listok-authority-manifest.json",
        str(S25.relative_to(ROOT)),
    }
    if not isinstance(bundles, list) or len(bundles) != 1:
        errors.append("ledger must contain exactly one bundle")
    else:
        bundle = bundles[0]
        if set(bundle.get("directInputs", [])) != expected_inputs:
            errors.append("bundle directInputs must be manifest + Stage25 only")
        if bundle.get("sitePublicationEligible") is not False:
            errors.append("bundle must remain site-ineligible pending editorial/rights gates")

    gap = ledger.get("gapAcquisition", {})
    expected_gap_ids = sorted(f"{y}-{i:02d}" for y, i in UNKNOWN)
    if sorted(gap.get("issues", [])) != expected_gap_ids:
        errors.append("ledger gap list differs")
    if gap.get("requestState") != "ready-to-request-not-sent":
        errors.append("BAN request must remain unsent")
    if gap.get("paymentAuthorized") is not False:
        errors.append("payment must remain unauthorized")

    if errors:
        for message in errors:
            print(f"ERROR: {message}", file=sys.stderr)
        return 1
    print(
        f"Bratsky authority OK: {len(keys)} local positions "
        f"({coverage['full']} full/{coverage['truncated']} truncated/"
        f"{coverage['targeted']} targeted), {len(unknown)} unknown, "
        f"{len(rows)} Stage25 rows; manifest sha256={digest}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
