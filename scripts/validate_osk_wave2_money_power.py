#!/usr/bin/env python3
"""Fail-closed validation for OSK Wave 2 conditional money/power closure."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
W1_MANIFEST = ROOT / "data/osk-case-routing-source-registry-2026-08-01.json"
W2_MANIFEST = ROOT / "data/osk-wave2-source-registry-2026-08-01.json"
W2_AUTHORITY = ROOT / "ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/36_WAVE2_CONDITIONAL_MONEY_POWER_CLOSURE_2026-08-01.md"
ROOT_AUTHORITY = ROOT / "00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md"

A_CLASSES = {"A1", "A2", "A3"}
ALLOWED_CLASSES = A_CLASSES | {"B1", "C", "D"}
ALLOWED_ROUTES = {
    "ANTISOVETY_CORE",
    "ANTISOVETY_CONDITIONAL",
    "DARK_SIDE_SERIES",
    "STANDALONE",
    "HOLD",
}
EXPECTED_DECISIONS = {
    "robert-morris": ("ANTISOVETY_CORE", "CORE_QUALIFIED"),
    "nikolay-kuznetsov": ("ANTISOVETY_CORE", "CORE_QUALIFIED"),
    "evgeny-shin": ("ANTISOVETY_CORE", "CORE_QUALIFIED"),
    "stanislav-moskvitin": ("ANTISOVETY_CORE", "CORE_VERIFIED"),
    "darrin-patrick": ("ANTISOVETY_CORE", "CORE_VERIFIED"),
    "bethel-bolz-armstrong": ("ANTISOVETY_CORE", "CORE_QUALIFIED"),
    "perry-noble": ("DARK_SIDE_SERIES", "RESTORATION_CONTRAST"),
    "david-platt": ("ANTISOVETY_CONDITIONAL", "PROCEDURAL_COMPARATOR_NO_MERITS_FINDING"),
}
EXPECTED_EFFECTIVE = {
    "ANTISOVETY_CORE": 21,
    "ANTISOVETY_CONDITIONAL": 1,
    "DARK_SIDE_SERIES": 7,
    "STANDALONE": 3,
    "HOLD": 1,
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"top-level object required: {path.relative_to(ROOT)}")
    return value


def text(record: dict[str, Any], key: str, context: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(f"{context}: non-empty string required for {key}")
    return value.strip()


def read_sources(manifest: dict[str, Any], authority_id: str) -> list[dict[str, Any]]:
    paths = manifest.get("source_shards")
    if not isinstance(paths, list) or not paths:
        fail("source_shards must be a non-empty array")
    sources: list[dict[str, Any]] = []
    shard_names: set[str] = set()
    for path_value in paths:
        if not isinstance(path_value, str) or not path_value:
            fail("invalid source shard path")
        shard = load(ROOT / path_value)
        if shard.get("schema_version") != 1:
            fail(f"invalid shard schema: {path_value}")
        if shard.get("authority_id") != authority_id:
            fail(f"authority drift in shard: {path_value}")
        shard_name = text(shard, "shard", path_value)
        if shard_name in shard_names:
            fail(f"duplicate shard name: {shard_name}")
        shard_names.add(shard_name)
        rows = shard.get("sources")
        if not isinstance(rows, list) or not rows:
            fail(f"non-empty sources required: {path_value}")
        if not all(isinstance(row, dict) for row in rows):
            fail(f"source objects required: {path_value}")
        sources.extend(rows)
    return sources


def validate_source(source: dict[str, Any], known_cases: set[str]) -> None:
    sid = text(source, "id", "source")
    case_id = text(source, "case_id", sid)
    text(source, "title", sid)
    text(source, "issuer", sid)
    cls = text(source, "source_class", sid)
    text(source, "purpose", sid)
    if case_id not in known_cases:
        fail(f"{sid}: unknown case_id {case_id}")
    if cls not in ALLOWED_CLASSES:
        fail(f"{sid}: invalid class {cls}")

    url = source.get("url")
    locator = source.get("repository_locator")
    if url is not None and (not isinstance(url, str) or not url.startswith("https://")):
        fail(f"{sid}: URL must be null or HTTPS")
    if locator is not None and (not isinstance(locator, str) or not locator.strip()):
        fail(f"{sid}: invalid repository locator")
    if not url and not locator:
        fail(f"{sid}: URL or repository locator required")

    quote_safe = source.get("quote_safe")
    if not isinstance(quote_safe, bool):
        fail(f"{sid}: quote_safe must be boolean")
    if quote_safe and cls not in A_CLASSES:
        fail(f"{sid}: weak source cannot be quote-safe")
    if quote_safe and not url:
        fail(f"{sid}: quote-safe requires exact URL")


def main() -> None:
    w1 = load(W1_MANIFEST)
    w2 = load(W2_MANIFEST)
    if w2.get("schema_version") != 1:
        fail("Wave 2 manifest schema must be 1")
    if w2.get("authority_id") != "RESEARCH-OSK-AUTHORITY-2026-08-01-W2":
        fail("unexpected Wave 2 authority_id")
    if w2.get("base_authority_id") != w1.get("authority_id"):
        fail("Wave 2 does not point to current Wave 1 authority")

    case_path = ROOT / text(w1, "case_registry", "Wave 1 manifest")
    w1_cases = load(case_path).get("cases")
    if not isinstance(w1_cases, list) or len(w1_cases) != 33:
        fail("Wave 1 case registry must retain 33 cases")
    case_by_id: dict[str, dict[str, Any]] = {}
    for case in w1_cases:
        if not isinstance(case, dict):
            fail("Wave 1 case object required")
        cid = text(case, "id", "Wave 1 case")
        if cid in case_by_id:
            fail(f"duplicate Wave 1 case: {cid}")
        case_by_id[cid] = case

    overlay_path = ROOT / text(w2, "decision_overlay", "Wave 2 manifest")
    overlay = load(overlay_path)
    if overlay.get("authority_id") != w2.get("authority_id"):
        fail("decision overlay authority drift")
    decisions = overlay.get("decisions")
    if not isinstance(decisions, list) or len(decisions) != 8:
        fail("Wave 2 must contain exactly eight decisions")

    decision_by_id: dict[str, dict[str, Any]] = {}
    for decision in decisions:
        if not isinstance(decision, dict):
            fail("decision object required")
        cid = text(decision, "case_id", "decision")
        previous = text(decision, "previous_route", cid)
        route = text(decision, "effective_route", cid)
        status = text(decision, "status", cid)
        text(decision, "decision_reason", cid)
        if cid not in case_by_id:
            fail(f"{cid}: not present in Wave 1")
        if previous != case_by_id[cid].get("route"):
            fail(f"{cid}: previous_route does not match Wave 1")
        if route not in ALLOWED_ROUTES:
            fail(f"{cid}: invalid effective route")
        if (route, status) != EXPECTED_DECISIONS.get(cid):
            fail(f"{cid}: unexpected route/status {(route, status)}")
        for field in ("permitted_claims", "blocked_claims", "power_mechanisms"):
            value = decision.get(field)
            if not isinstance(value, list) or not value:
                fail(f"{cid}: non-empty {field} required")
        decision_by_id[cid] = decision

    if set(decision_by_id) != set(EXPECTED_DECISIONS):
        fail("Wave 2 decision set drift")

    forbidden = {"grace-gray", "paul-wendy-guay", "sunday-adelaja"}
    if forbidden & set(decision_by_id):
        fail("Grace/Guay/Adelaja fail-closed routes cannot be changed by Wave 2")

    effective_routes = {
        cid: decision_by_id.get(cid, {}).get("effective_route", case.get("route"))
        for cid, case in case_by_id.items()
    }
    effective_counts = Counter(effective_routes.values())
    if dict(effective_counts) != EXPECTED_EFFECTIVE:
        fail(f"effective route drift: {dict(effective_counts)}")
    if overlay.get("effective_route_counts") != EXPECTED_EFFECTIVE:
        fail("overlay effective_route_counts drift")

    sources = read_sources(w2, w2["authority_id"])
    if len(sources) != 56:
        fail(f"Wave 2 must have 56 sources, found {len(sources)}")
    source_ids: list[str] = []
    source_counts: Counter[str] = Counter()
    a_count = exact_count = repo_count = quote_count = 0
    known_cases = set(case_by_id)
    for source in sources:
        validate_source(source, known_cases)
        sid = source["id"]
        source_ids.append(sid)
        cid = source["case_id"]
        source_counts[cid] += 1
        if source["source_class"] in A_CLASSES:
            a_count += 1
        if source.get("url"):
            exact_count += 1
        if source.get("repository_locator"):
            repo_count += 1
        if source["quote_safe"]:
            quote_count += 1

    if len(source_ids) != len(set(source_ids)):
        fail("duplicate Wave 2 source ids")
    if set(source_counts) != set(EXPECTED_DECISIONS):
        fail("Wave 2 sources must cover exactly the eight reviewed cases")
    if any(count != 7 for count in source_counts.values()):
        fail(f"every Wave 2 case requires exactly seven source records: {dict(source_counts)}")
    if a_count < 32 or exact_count < 35 or quote_count < 18:
        fail(f"source quality floor failed: A={a_count}, exact={exact_count}, quote={quote_count}")

    shin_scale = next((s for s in sources if s["id"] == "W2-SHI-07"), None)
    if not shin_scale or shin_scale["source_class"] != "C" or shin_scale["quote_safe"]:
        fail("Shin half-billion allegation must remain a non-quote-safe C negative control")
    platt = decision_by_id["david-platt"]
    if "NO_MERITS_FINDING" not in platt["status"]:
        fail("Platt no-merits boundary missing")
    noble = decision_by_id["perry-noble"]
    if noble["effective_route"] != "DARK_SIDE_SERIES":
        fail("Noble must remain a restoration contrast outside the core")
    mos_blocked = " ".join(decision_by_id["stanislav-moskvitin"]["blocked_claims"])
    if "2025" not in mos_blocked or "outside" not in mos_blocked:
        fail("Moskvitin later-prosecution exclusion missing")

    w1_counters = w1.get("counters")
    if not isinstance(w1_counters, dict):
        fail("Wave 1 counters missing")
    calculated_wave2 = {
        "wave2_case_records": 8,
        "wave2_source_records": len(sources),
        "wave2_a_class_sources": a_count,
        "wave2_exact_url_sources": exact_count,
        "wave2_repository_capture_sources": repo_count,
        "wave2_quote_safe_sources": quote_count,
        "effective_core_cases": effective_counts["ANTISOVETY_CORE"],
        "effective_conditional_cases": effective_counts["ANTISOVETY_CONDITIONAL"],
        "effective_dark_side_cases": effective_counts["DARK_SIDE_SERIES"],
        "effective_standalone_cases": effective_counts["STANDALONE"],
        "effective_hold_cases": effective_counts["HOLD"],
    }
    if w2.get("wave2_counters") != calculated_wave2:
        fail(f"Wave 2 counter drift: expected {calculated_wave2}")

    cumulative = {
        "source_records": w1_counters["source_records"] + len(sources),
        "a_class_sources": w1_counters["a_class_sources"] + a_count,
        "exact_url_sources": w1_counters["exact_url_sources"] + exact_count,
        "repository_capture_sources": w1_counters["repository_capture_sources"] + repo_count,
        "quote_safe_sources": w1_counters["quote_safe_sources"] + quote_count,
    }
    if w2.get("cumulative_counters") != cumulative:
        fail(f"cumulative counter drift: expected {cumulative}")

    authority = W2_AUTHORITY.read_text(encoding="utf-8")
    root = ROOT_AUTHORITY.read_text(encoding="utf-8")
    for marker in (
        "56", "37", "21", "Robert Morris", "Nikolay Kuznetsov",
        "Evgeny Shin", "Stanislav Moskvitin", "Darrin Patrick",
        "Bethel", "Perry Noble", "David Platt", "NO_MERITS",
        "половине миллиарда", "нежелательной организацией",
    ):
        if marker not in authority and marker not in root:
            fail(f"authority marker missing: {marker}")

    print(
        "OSK Wave 2 OK: "
        f"8 decisions, {len(sources)} sources, {a_count} A-class, "
        f"{exact_count} exact URLs, {quote_count} quote-safe; "
        f"effective routes {dict(effective_counts)}"
    )


if __name__ == "__main__":
    main()
