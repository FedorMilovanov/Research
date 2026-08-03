#!/usr/bin/env python3
"""Normalize the append-only Baptist proof ledger into canonical schema v2.

The legacy CSV remains untouched. Historical transport pointers, year ranges,
and secondary-ID aliases are preserved losslessly while the canonical view uses
one stable ID, one sortable integer year (or blank), and HTTPS-only URL fields.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from io import StringIO
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "data/baptist-proof-ledger-schema-v2.json"
DEFAULT_INPUT = ROOT / "БАПТИСТЫ РОССИИ/baptists_v120_TRUE_GROUPED/data/PROOF_STATUS_LEDGER.csv"
YEAR_RE = re.compile(r"(?:18|19|20)\d{2}")


def clean(value: object) -> str:
    return str(value or "").strip()


def append_note(base: str, note: str) -> str:
    base = clean(base)
    note = clean(note)
    if not note:
        return base
    return f"{base} | {note}" if base else note


def normalize_year(raw: str, issue: str) -> tuple[str, str]:
    """Return canonical first year and an optional lossless raw-expression note."""
    value = clean(raw)
    if value:
        try:
            number = float(value)
        except ValueError:
            years = YEAR_RE.findall(value)
            if not years:
                return "", f"legacy year expression: {value}"
            return years[0], f"legacy year expression: {value}"
        if not number.is_integer():
            years = YEAR_RE.findall(value)
            if years:
                return years[0], f"legacy year expression: {value}"
            raise ValueError(f"non-integral year {value!r}")
        year = int(number)
        if not 1800 <= year <= 2099:
            raise ValueError(f"year out of range {year}")
        return str(year), "" if value == str(year) else f"legacy year expression: {value}"
    match = YEAR_RE.search(issue)
    return (match.group(0), "") if match else ("", "")


def normalize_url(raw: str, source: str, note: str) -> tuple[str, str, str]:
    value = clean(raw)
    if not value:
        return "", source, note
    parsed = urlparse(value)
    if parsed.scheme == "https" and parsed.netloc:
        return value, source, note
    # tg://, http:// and other historical transport pointers are evidence
    # history, not canonical public URLs. Preserve them verbatim outside the
    # HTTPS-only source_url field.
    source = append_note(source, f"legacy source pointer: {value}")
    note = append_note(note, "canonical source_url left blank: legacy pointer is not HTTPS")
    return "", source, note


def render_csv(rows: list[dict[str, str]], columns: list[str]) -> str:
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


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
            record_id = item_id or secondary_id
            if not record_id:
                errors.append(f"row {row_number}: empty record_id")
                continue
            if record_id in seen:
                errors.append(f"row {row_number}: duplicate record_id {record_id!r}; first row {seen[record_id]}")
                continue
            seen[record_id] = row_number

            issue = clean(row.get("issue"))
            note = clean(row.get("verification_note"))
            if item_id and secondary_id and item_id != secondary_id:
                note = append_note(note, f"legacy secondary id alias: {secondary_id}")

            try:
                year, year_note = normalize_year(clean(row.get("year")), issue)
            except ValueError as exc:
                errors.append(f"row {row_number}: {exc}")
                continue
            note = append_note(note, year_note)

            source = clean(row.get("source"))
            source_url, source, note = normalize_url(clean(row.get("source_url")), source, note)
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
                "source": source,
                "source_url": source_url,
                "verification_note": note,
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
    payload = render_csv(canonical, columns)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text("\ufeff" + payload, encoding="utf-8")
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
