#!/usr/bin/env python3
"""Build a deterministic Baptist scan-request package and validate byte receipts.

The script never promotes catalog evidence to acquisition. It reads the current
NEXT_MICROBATCH, composes verified receipts where present, and emits request-ready
records for everything else.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "data/baptist-scan-acquisition-policy-v2.json"
RECEIPTS_PATH = ROOT / "data/baptist-scan-receipts-v1.json"
QUEUE_PATH = ROOT / "БАПТИСТЫ РОССИИ/baptists_v120_TRUE_GROUPED/data/NEXT_MICROBATCH.csv"
ID_FIELDS = ("record_id", "item_id", "id", "queue_id", "source_id")
ISSUE_FIELDS = ("issue", "title", "item", "requested_item_designation")
HOLDING_FIELDS = ("holding", "holding_or_provider", "archive", "provider")
SOURCE_FIELDS = ("source", "catalog", "catalog_or_source_url", "source_url")
ACTION_FIELDS = ("next_action", "action", "request_action")
STATE_ORDER = {
    "CATALOG_VERIFIED_REQUEST_READY": 0,
    "REQUEST_SENT": 1,
    "RECEIVED_UNVERIFIED": 2,
    "FILE_VERIFIED": 3,
    "OCR_COMPLETE_VISUAL_PENDING": 4,
    "QUOTE_READY": 5,
    "RIGHTS_HOLD": 5,
    "REJECTED_NOT_SOURCE_FILE": 2,
}
errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def pick(row: dict[str, str], fields: tuple[str, ...]) -> str:
    for field in fields:
        value = str(row.get(field, "") or "").strip()
        if value:
            return value
    return ""


def clean_url(value: str) -> str:
    value = value.strip()
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return ""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)}: object required")
        return {}
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_receipt_fields(record: dict[str, Any], required: list[str], context: str) -> None:
    for field in required:
        value = record.get(field)
        if value is None or value == "" or value == []:
            fail(f"{context}: required receipt field missing: {field}")


def normalize_queue() -> list[dict[str, str]]:
    try:
        handle = QUEUE_PATH.open(encoding="utf-8-sig", newline="")
    except OSError as exc:
        fail(f"cannot open queue: {exc}")
        return []
    with handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            fail("NEXT_MICROBATCH has no header")
            return []
        records: list[dict[str, str]] = []
        seen: set[str] = set()
        for row_number, raw in enumerate(reader, start=2):
            row = {str(key or "").strip(): str(value or "").strip() for key, value in raw.items()}
            record_id = pick(row, ID_FIELDS)
            issue = pick(row, ISSUE_FIELDS)
            if not record_id:
                fail(f"queue row {row_number}: stable ID is required")
                continue
            if record_id in seen:
                fail(f"queue row {row_number}: duplicate ID {record_id}")
                continue
            seen.add(record_id)
            if not issue:
                fail(f"queue row {row_number}/{record_id}: issue/title is required")
                continue
            holding = pick(row, HOLDING_FIELDS)
            source = pick(row, SOURCE_FIELDS)
            action = pick(row, ACTION_FIELDS)
            source_url = clean_url(row.get("source_url", "")) or clean_url(source)
            if source_url:
                parsed = urlparse(source_url)
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    fail(f"queue row {row_number}/{record_id}: malformed source URL")
            if not holding and not source:
                fail(f"queue row {row_number}/{record_id}: holding or source pointer required")
            if not action:
                action = "Request scan or source file; record byte receipt; perform OCR and visual page review."
            records.append({
                "record_id": record_id,
                "corpus": row.get("corpus", "").strip(),
                "issue": issue,
                "year": row.get("year", "").strip(),
                "queue_status": row.get("status", "").strip(),
                "pages": row.get("pages", "").strip(),
                "holding_or_provider": holding or source,
                "source": source,
                "catalog_or_source_url": source_url,
                "next_action": action,
                "legacy_version": row.get("version", "").strip(),
            })
        return records


def validate_receipts(policy: dict[str, Any], queue: list[dict[str, str]], receipts: dict[str, Any]) -> dict[str, dict[str, Any]]:
    allowed = set(policy.get("allowedStates", []))
    rules = policy.get("promotionRules", {})
    queue_ids = {row["record_id"] for row in queue}
    records = receipts.get("records")
    if not isinstance(records, list):
        fail("receipt records must be a list")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            fail(f"receipt #{index}: object required")
            continue
        record_id = str(record.get("record_id", "")).strip()
        state = str(record.get("state", "")).strip()
        context = f"receipt #{index}/{record_id or 'NO_ID'}"
        if not record_id:
            fail(f"{context}: record_id required")
            continue
        if record_id in result:
            fail(f"{context}: duplicate receipt")
            continue
        if record_id not in queue_ids:
            fail(f"{context}: receipt is not in current NEXT_MICROBATCH")
        if state not in allowed:
            fail(f"{context}: invalid state {state}")
            continue
        require_receipt_fields(record, list(rules.get(state, [])), context)
        if STATE_ORDER.get(state, -1) >= STATE_ORDER["RECEIVED_UNVERIFIED"] and state != "REJECTED_NOT_SOURCE_FILE":
            sha = str(record.get("sha256", ""))
            size = record.get("byte_size")
            if not re.fullmatch(r"[0-9a-f]{64}", sha):
                fail(f"{context}: valid SHA-256 required")
            if not isinstance(size, int) or size <= 0:
                fail(f"{context}: positive byte_size required")
            storage = record.get("storage_receipt")
            if not isinstance(storage, dict) or storage.get("state") not in policy.get("custody", {}).get("durableStates", []):
                fail(f"{context}: durable storage receipt required")
        if STATE_ORDER.get(state, -1) >= STATE_ORDER["FILE_VERIFIED"] and state not in {"RIGHTS_HOLD", "REJECTED_NOT_SOURCE_FILE"}:
            if not isinstance(record.get("page_count"), int) or record["page_count"] <= 0:
                fail(f"{context}: positive page_count required")
            if record.get("title_page_visual_review") is not True or record.get("issue_identity_review") is not True:
                fail(f"{context}: visual identity review required")
        if state == "QUOTE_READY":
            if record.get("rights_state") not in {"PUBLIC_DOMAIN", "OPEN_LICENSE", "PRIVATE_RESEARCH_QUOTATION_REVIEWED", "PERMISSION_GRANTED"}:
                fail(f"{context}: quote-ready rights state invalid")
            if not isinstance(record.get("quote_cards"), list) or not record["quote_cards"]:
                fail(f"{context}: quote cards required")
        result[record_id] = record
    return result


def build_package(queue: list[dict[str, str]], receipt_map: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    package: list[dict[str, Any]] = []
    for row in queue:
        receipt = receipt_map.get(row["record_id"])
        if receipt:
            package.append({**row, "state": receipt["state"], "receipt": receipt})
        else:
            package.append({
                **row,
                "state": "CATALOG_VERIFIED_REQUEST_READY",
                "request_target": row["holding_or_provider"],
                "requested_item_designation": row["issue"],
                "request_template": (
                    f"Please provide a complete scan or source file for {row['issue']}. "
                    "Please preserve cover/title page, all numbered and unnumbered pages, and identify any copy/page-count variant."
                ),
            })
    return package


def write_outputs(output_dir: Path, package: list[dict[str, Any]], queue_sha: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "baptist-scan-request-package.json"
    json_path.write_text(json.dumps({
        "schemaVersion": 1,
        "authorityId": "BAPTIST-SCAN-REQUEST-PACKAGE-2026-08-02",
        "custodyState": "EPHEMERAL_ACTION_ARTIFACT",
        "queueSha256": queue_sha,
        "records": package,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    csv_fields = [
        "record_id", "corpus", "issue", "year", "state", "pages",
        "holding_or_provider", "catalog_or_source_url", "next_action",
    ]
    with (output_dir / "baptist-scan-request-package.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fields)
        writer.writeheader()
        for row in package:
            writer.writerow({field: row.get(field, "") for field in csv_fields})
    lines = [
        "# Baptist scan request package",
        "",
        "**Custody:** `EPHEMERAL_ACTION_ARTIFACT` — this package is a request queue, not acquired scans.",
        "",
    ]
    for row in package:
        lines.extend([
            f"## {row['record_id']} — {row['issue']}",
            "",
            f"- state: `{row['state']}`",
            f"- corpus: {row.get('corpus') or 'not supplied'}",
            f"- holding/provider: {row['holding_or_provider']}",
            f"- catalog/source: {row.get('catalog_or_source_url') or row.get('source') or 'not supplied'}",
            f"- page note: {row.get('pages') or 'not supplied'}",
            f"- next action: {row['next_action']}",
            "",
            row.get("request_template", "Receipt already exists; follow the receipt state and next action."),
            "",
        ])
    (output_dir / "REQUESTS.md").write_text("\n".join(lines), encoding="utf-8")
    sums = []
    for path in sorted(output_dir.iterdir()):
        if path.name == "SHA256SUMS.txt" or not path.is_file():
            continue
        sums.append(f"{sha256_file(path)}  {path.name}")
    (output_dir / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    policy = load_json(POLICY_PATH)
    receipts = load_json(RECEIPTS_PATH)
    if policy.get("schemaVersion") != 2 or policy.get("authorityId") != "BAPTIST-SCAN-ACQUISITION-POLICY-2026-08-02":
        fail("acquisition policy authority drift")
    if receipts.get("schemaVersion") != 1 or receipts.get("authorityId") != "BAPTIST-SCAN-RECEIPTS-2026-08-02":
        fail("receipt authority drift")
    queue = normalize_queue()
    if not queue:
        fail("NEXT_MICROBATCH must contain at least one request")
    receipt_map = validate_receipts(policy, queue, receipts)
    package = build_package(queue, receipt_map)
    counts = {
        "queue": len(queue),
        "requestReady": sum(row["state"] == "CATALOG_VERIFIED_REQUEST_READY" for row in package),
        "receivedOrHigher": sum(STATE_ORDER.get(row["state"], -1) >= STATE_ORDER["RECEIVED_UNVERIFIED"] for row in package),
        "fileVerified": sum(STATE_ORDER.get(row["state"], -1) >= STATE_ORDER["FILE_VERIFIED"] and row["state"] != "REJECTED_NOT_SOURCE_FILE" for row in package),
        "quoteReady": sum(row["state"] == "QUOTE_READY" for row in package),
    }
    declared = receipts.get("counts", {})
    require_declared = {
        "fileVerified": counts["fileVerified"],
        "quoteReady": counts["quoteReady"],
    }
    for key, expected in require_declared.items():
        if declared.get(key) != expected:
            fail(f"receipt count drift: {key}={declared.get(key)} expected {expected}")
    if args.output_dir:
        write_outputs(args.output_dir, package, sha256_file(QUEUE_PATH))
    if errors:
        print(f"Baptist scan acquisition: FAIL ({len(errors)})", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(json.dumps(counts, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
