#!/usr/bin/env python3
"""Normalize the append-only Baptist proof ledger into canonical schema v2.

The legacy CSV is preserved as historical input. All machine consumers must use
this deterministic canonical view or run this validator before reading rows.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "data/baptist-proof-ledger-schema-v2.json"
DEFAULT_INPUT = ROOT / "БАПТИСТЫ РОССИИ/baptists_v120_TRUE_GROUPED/data/PROOF_STATUS_LEDGER.csv"
YEAR_RE = re.compile(r"(?:18|19|20)\d{2}")


def clean(value: object) -> str:
    return str(value or "").strip()


def normalize_year(raw: str, issue: str) -> str:
    value = clean(raw)
    if value:
        try:
            number = float(value)
        except ValueError as exc:
            raise ValueError(f"invalid year {value!r}") from exc
        if not number.is_integer():
            raise ValueError(f"non-integral year {value!r}")
        year = int(number)
        if not 1800 <= year <= 2099:
            raise ValueError(f"year out of range {year}")
        return str(year)
    match = YEAR_RE.search(issue)
    return match.group(0) if match else ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    columns = schema["canonicalColumns"]
    aliases = schema["corpusAliases"]
    errors: list[str] = []
    canonical: list[dict[str, str]] = []
    seen: dict[str, int] = {}

    with args.input.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required_legacy = {
            "item_id", "id", "corpus", "issue", "status", "pages", "holding",
            "source", "next_action", "year", "source_url", "verification_note", "version",
        }
        missing = required_legacy - set(reader.fieldnames or [])
        if missing:
            errors.append(f"legacy header missing columns: {sorted(missing)}")
        for row_number, row in enumerate(reader, start=2):
            item_id = clean(row.get("item_id"))
            secondary_id = clean(row.get("id"))
            if item_id and secondary_id and item_id != secondary_id:
                errors.append(
                    f"row {row_number}: item_id/id conflict {item_id!r} != {secondary_id!r}"
                )
                continue
            record_id = item_id or secondary_id
            if not record_id:
                errors.append(f"row {row_number}: empty record_id")
                continue
            if record_id in seen:
                errors.append(
                    f"row {row_number}: duplicate record_id {record_id!r}; first row {seen[record_id]}"
                )
                continue
            seen[record_id] = row_number

            issue = clean(row.get("issue"))
            try:
                year = normalize_year(clean(row.get("year")), issue)
            except ValueError as exc:
                errors.append(f"row {row_number}: {exc}")
                continue
            url = clean(row.get("source_url"))
            if url:
                parsed = urlparse(url)
                if parsed.scheme != "https" or not parsed.netloc:
                    errors.append(f"row {row_number}: source_url must be HTTPS: {url}")
                    continue
            corpus_raw = clean(row.get("corpus"))
            corpus = aliases.get(corpus_raw, corpus_raw)
            if not corpus:
                errors.append(f"row {row_number}: empty corpus")
                continue
            status = clean(row.get("status"))
            if not status:
                errors.append(f"row {row_number}: empty status")
                continue

            canonical.append({
                "record_id": record_id,
                "corpus": corpus,
                "issue": issue,
                "year": year,
                "status": status,
                "pages": clean(row.get("pages")),
                "holding": clean(row.get("holding")),
                "source": clean(row.get("source")),
                "source_url": url,
                "verification_note": clean(row.get("verification_note")),
                "next_action": clean(row.get("next_action")),
                "version": clean(row.get("version")),
            })

    if len(canonical) < 50:
        errors.append(f"canonical ledger unexpectedly small: {len(canonical)} rows")
    if errors:
        print(f"Baptist proof ledger v2: FAIL ({len(errors)})", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    canonical.sort(key=lambda row: (row["corpus"], row["year"], row["issue"], row["record_id"]))
    payload = ""
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            writer.writerows(canonical)
        payload = args.output.read_text(encoding="utf-8-sig")
    else:
        from io import StringIO
        buffer = StringIO()
        writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(canonical)
        payload = buffer.getvalue()

    summary = {
        "schemaVersion": 2,
        "rows": len(canonical),
        "uniqueRecordIds": len(seen),
        "corpora": sorted({row["corpus"] for row in canonical}),
        "canonicalSha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "legacyInputSha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "legacyInput": args.input.relative_to(ROOT).as_posix(),
        "canonicalColumns": columns,
    }
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
