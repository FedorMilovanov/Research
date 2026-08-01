#!/usr/bin/env python3
"""Fail-closed validation for the OSK case-routing and source authority."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data/osk-case-routing-source-registry-2026-08-01.json"
AUTHORITY_PATH = ROOT / "ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/35_CURRENT_AUTHORITY_POWER_CASE_ROUTING_2026-08-01.md"
ROOT_AUTHORITY_PATH = ROOT / "00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md"

ALLOWED_ROUTES = {
    "ANTISOVETY_CORE",
    "ANTISOVETY_CONDITIONAL",
    "DARK_SIDE_SERIES",
    "STANDALONE",
    "HOLD",
}
ALLOWED_CLASSES = {"A1", "A2", "A3", "B1", "C", "D"}
A_CLASSES = {"A1", "A2", "A3"}
ALLOWED_MECHANISMS = {
    "authority_capture",
    "governance_capture",
    "retaliation",
    "information_control",
    "procedure_weaponization",
    "financial_dependency",
    "sexual_spiritual_coercion",
    "reputation_shield",
}
EXPECTED_ROUTE_COUNTS = {
    "ANTISOVETY_CORE": 15,
    "ANTISOVETY_CONDITIONAL": 8,
    "DARK_SIDE_SERIES": 6,
    "STANDALONE": 3,
    "HOLD": 1,
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"top-level JSON object required: {path.relative_to(ROOT)}")
    return value


def require_text(record: dict[str, Any], field: str, context: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        fail(f"{context}: non-empty string required for {field}")
    return value.strip()


def main() -> None:
    manifest = load_json(MANIFEST_PATH)
    if manifest.get("schema_version") != 1:
        fail("manifest schema_version must be 1")

    case_path_value = require_text(manifest, "case_registry", "manifest")
    case_path = ROOT / case_path_value
    case_registry = load_json(case_path)
    if case_registry.get("schema_version") != 1:
        fail("case registry schema_version must be 1")

    shard_paths = manifest.get("source_shards")
    if not isinstance(shard_paths, list) or len(shard_paths) != 4:
        fail("manifest must declare exactly four source shards")

    sources: list[dict[str, Any]] = []
    shard_names: set[str] = set()
    for shard_path_value in shard_paths:
        if not isinstance(shard_path_value, str) or not shard_path_value:
            fail("source shard path must be a non-empty string")
        shard = load_json(ROOT / shard_path_value)
        if shard.get("schema_version") != 1:
            fail(f"source shard schema_version must be 1: {shard_path_value}")
        if shard.get("authority_id") != manifest.get("authority_id"):
            fail(f"authority_id drift in source shard: {shard_path_value}")
        shard_name = require_text(shard, "shard", shard_path_value)
        if shard_name in shard_names:
            fail(f"duplicate shard name: {shard_name}")
        shard_names.add(shard_name)
        shard_sources = shard.get("sources")
        if not isinstance(shard_sources, list) or not shard_sources:
            fail(f"non-empty sources array required: {shard_path_value}")
        for item in shard_sources:
            if not isinstance(item, dict):
                fail(f"source record must be an object: {shard_path_value}")
            sources.append(item)

    if case_registry.get("authority_id") != manifest.get("authority_id"):
        fail("case registry authority_id drift")

    cases = case_registry.get("cases")
    if not isinstance(cases, list):
        fail("case registry cases must be an array")
    if len(cases) != 33:
        fail(f"expected 33 cases, found {len(cases)}")
    if len(sources) < 60:
        fail(f"at least 60 source records required, found {len(sources)}")

    case_ids: list[str] = []
    case_by_id: dict[str, dict[str, Any]] = {}
    route_counts: Counter[str] = Counter()
    for case in cases:
        if not isinstance(case, dict):
            fail("case record must be an object")
        case_id = require_text(case, "id", "case")
        require_text(case, "name", case_id)
        route = require_text(case, "route", case_id)
        require_text(case, "claim_boundary", case_id)
        require_text(case, "status", case_id)
        require_text(case, "review_wave", case_id)
        if route not in ALLOWED_ROUTES:
            fail(f"{case_id}: invalid route {route}")
        mechanisms = case.get("power_mechanisms")
        if not isinstance(mechanisms, list):
            fail(f"{case_id}: power_mechanisms must be an array")
        unknown = set(mechanisms) - ALLOWED_MECHANISMS
        if unknown:
            fail(f"{case_id}: unknown power mechanisms {sorted(unknown)}")
        if route == "ANTISOVETY_CORE" and not mechanisms:
            fail(f"{case_id}: core case requires a documented power mechanism")
        count = case.get("source_record_count")
        if not isinstance(count, int) or count < 0:
            fail(f"{case_id}: source_record_count must be a non-negative integer")
        case_ids.append(case_id)
        case_by_id[case_id] = case
        route_counts[route] += 1

    if len(case_ids) != len(set(case_ids)):
        fail("duplicate case ids")
    if dict(route_counts) != EXPECTED_ROUTE_COUNTS:
        fail(f"route counters drift: {dict(route_counts)}")

    source_ids: list[str] = []
    source_identity: list[tuple[str, str]] = []
    source_counts: Counter[str] = Counter()
    a_count = 0
    exact_url_count = 0
    repository_capture_count = 0
    quote_safe_count = 0

    for source in sources:
        source_id = require_text(source, "id", "source")
        case_id = require_text(source, "case_id", source_id)
        title = require_text(source, "title", source_id)
        issuer = require_text(source, "issuer", source_id)
        source_class = require_text(source, "source_class", source_id)
        require_text(source, "purpose", source_id)
        if case_id not in case_by_id:
            fail(f"{source_id}: unknown case_id {case_id}")
        if source_class not in ALLOWED_CLASSES:
            fail(f"{source_id}: invalid source_class {source_class}")

        url = source.get("url")
        locator = source.get("repository_locator")
        if url is not None and (not isinstance(url, str) or not url.startswith("https://")):
            fail(f"{source_id}: URL must be null or HTTPS")
        if locator is not None and (not isinstance(locator, str) or not locator.strip()):
            fail(f"{source_id}: repository_locator must be null or non-empty")
        if not url and not locator:
            fail(f"{source_id}: exact URL or repository locator required")

        quote_safe = source.get("quote_safe")
        if not isinstance(quote_safe, bool):
            fail(f"{source_id}: quote_safe must be boolean")
        if quote_safe and source_class not in A_CLASSES:
            fail(f"{source_id}: weak source cannot be quote-safe")
        if quote_safe and not url:
            fail(f"{source_id}: quote-safe source requires an exact HTTPS URL")

        source_ids.append(source_id)
        source_identity.append((issuer.casefold(), title.casefold()))
        source_counts[case_id] += 1
        if source_class in A_CLASSES:
            a_count += 1
        if url:
            exact_url_count += 1
        if locator:
            repository_capture_count += 1
        if quote_safe:
            quote_safe_count += 1

    if len(source_ids) != len(set(source_ids)):
        fail("duplicate source ids")
    if len(source_identity) != len(set(source_identity)):
        fail("duplicate issuer/title source records")
    if a_count < 50:
        fail(f"at least 50 A-class sources required, found {a_count}")

    for case_id, case in case_by_id.items():
        declared = case["source_record_count"]
        actual = source_counts[case_id]
        if declared != actual:
            fail(f"{case_id}: declared source count {declared}, actual {actual}")
        if case["route"] == "ANTISOVETY_CORE" and actual < 4:
            fail(f"{case_id}: core case requires at least four source records")
        if case["route"] != "ANTISOVETY_CORE" and actual != 0:
            fail(f"{case_id}: wave-1 source records are restricted to core cases")

    required_cases = {
        "grace-gray": ("STANDALONE", "EXCLUDED_FROM_ANTISOVETY"),
        "paul-wendy-guay": ("STANDALONE", "ROUTE_OUT_OF_CORE"),
        "sunday-adelaja": ("HOLD", "BLOCKED"),
    }
    for case_id, expected in required_cases.items():
        case = case_by_id.get(case_id)
        if case is None:
            fail(f"required case missing: {case_id}")
        if (case["route"], case["status"]) != expected:
            fail(f"{case_id}: required fail-closed route/status is {expected}")

    calculated = {
        "case_records": len(cases),
        "source_records": len(sources),
        "a_class_sources": a_count,
        "exact_url_sources": exact_url_count,
        "repository_capture_sources": repository_capture_count,
        "quote_safe_sources": quote_safe_count,
        "core_cases": route_counts["ANTISOVETY_CORE"],
        "conditional_cases": route_counts["ANTISOVETY_CONDITIONAL"],
        "dark_side_cases": route_counts["DARK_SIDE_SERIES"],
        "standalone_cases": route_counts["STANDALONE"],
        "hold_cases": route_counts["HOLD"],
    }
    if manifest.get("counters") != calculated:
        fail(f"manifest counter drift: expected {calculated}, found {manifest.get('counters')}")

    authority = AUTHORITY_PATH.read_text(encoding="utf-8")
    root_authority = ROOT_AUTHORITY_PATH.read_text(encoding="utf-8")
    for marker in (
        "79",
        "75",
        "Grace",
        "Guay",
        "Sunday Adelaja",
        "деньги",
        "сексуальный",
        "PUBLICATION_HOLD",
    ):
        if marker not in authority and marker not in root_authority:
            fail(f"authority text missing required marker: {marker}")

    print(
        "OSK authority OK: "
        f"{len(cases)} cases, {len(sources)} sources, "
        f"{a_count} A-class, {quote_safe_count} quote-safe"
    )


if __name__ == "__main__":
    main()
