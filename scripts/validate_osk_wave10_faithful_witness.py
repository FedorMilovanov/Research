#!/usr/bin/env python3
"""Validate OSK Wave 10 including its transitive Wave 9 parent source pool."""
from __future__ import annotations

import json
import pathlib
import re
import sys
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "data/osk-wave10-faithful-witness-cases-2026-08-01.json"
SOURCES_PATH = ROOT / "data/osk-wave10-faithful-witness-new-sources-2026-08-01.json"
RESPONSES_PATH = ROOT / "data/osk-wave10-twenty-faithful-responses-2026-08-01.json"
PARENT_MANIFEST_PATH = ROOT / "data/osk-wave9-modern-diotrophes-source-manifest-2026-08-01.json"
PARENT_OUTLINE_PATH = ROOT / "data/osk-wave9-modern-diotrophes-outline-2026-08-01.json"
REPORT_PATH = ROOT / "ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/43_WAVE10_FAITHFUL_WITNESS_UNDER_PRESSURE_2026-08-01.md"
ROOT_AUTHORITY_PATH = ROOT / "00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md"

AUTHORITY = "RESEARCH-OSK-AUTHORITY-2026-08-01-W10-FAITHFUL-WITNESS"
PARENT_AUTHORITY = "RESEARCH-OSK-AUTHORITY-2026-08-01-W9"
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load(path: pathlib.Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)} must contain an object")
        return {}
    return value


def parent_source_pool(manifest: dict) -> set[str]:
    """Rebuild the actual Wave 9 source pool from its declared direct inputs."""
    pool: set[str] = set()
    sets = manifest.get("source_sets", [])
    if not isinstance(sets, list):
        errors.append("Wave 9 source_sets must be a list")
        return pool
    for spec in sets:
        if not isinstance(spec, dict):
            errors.append("Wave 9 source-set entry must be an object")
            continue
        if "shards" in spec:
            included = set(spec.get("included_case_ids", []))
            excluded = set(spec.get("excluded_source_ids", []))
            for rel in spec.get("shards", []):
                shard = load(ROOT / str(rel))
                for source in shard.get("sources", []):
                    if not isinstance(source, dict):
                        continue
                    sid = source.get("id")
                    case_id = source.get("case_id")
                    if isinstance(sid, str) and case_id in included and sid not in excluded:
                        pool.add(sid)
        elif "registry" in spec:
            registry = load(ROOT / str(spec.get("registry", "")))
            registry_ids = {
                source.get("id")
                for source in registry.get("sources", [])
                if isinstance(source, dict) and isinstance(source.get("id"), str)
            }
            requested = spec.get("included_source_ids", [])
            unknown = sorted(set(requested) - registry_ids)
            if unknown:
                errors.append(f"Wave 9 parent references missing control IDs: {unknown}")
            pool.update(item for item in requested if isinstance(item, str) and item in registry_ids)
        else:
            errors.append(f"Wave 9 source set lacks shards/registry: {spec.get('id')}")
    return pool


def main() -> int:
    cases_doc = load(CASES_PATH)
    sources_doc = load(SOURCES_PATH)
    responses_doc = load(RESPONSES_PATH)
    parent_manifest = load(PARENT_MANIFEST_PATH)
    parent_outline = load(PARENT_OUTLINE_PATH)
    try:
        report = REPORT_PATH.read_text(encoding="utf-8")
        root_authority = ROOT_AUTHORITY_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"authority/report read failed: {exc}")
        report = ""
        root_authority = ""

    require(cases_doc.get("authority_id") == AUTHORITY, "case authority id drift")
    require(sources_doc.get("authority_id") == AUTHORITY, "source authority id drift")
    require(responses_doc.get("authority_id") == AUTHORITY, "response authority id drift")
    require(cases_doc.get("parent_authority") == PARENT_AUTHORITY, "wrong parent authority")
    require(parent_manifest.get("authority_id") == PARENT_AUTHORITY, "Wave 9 parent manifest authority drift")
    require(parent_outline.get("authority_id") == PARENT_AUTHORITY, "Wave 9 parent outline authority drift")
    require(parent_outline.get("status") == "READY_FOR_EDITORIAL_DRAFT_NO_PRODUCT_WRITE", "Wave 9 parent status drift")
    require(cases_doc.get("status") == "RESEARCH_CLOSED_PRODUCT_PUBLICATION_HOLD", "wrong publication boundary")

    parent_pool = parent_source_pool(parent_manifest)
    inherited_ids = cases_doc.get("inherited_source_ids", [])
    require(isinstance(inherited_ids, list), "inherited_source_ids must be a list")
    inherited_ids = [item for item in inherited_ids if isinstance(item, str)]
    require(len(inherited_ids) == len(set(inherited_ids)), "duplicate inherited source ids")
    missing_from_parent = sorted(set(inherited_ids) - parent_pool)
    require(not missing_from_parent, f"inherited source ids absent from Wave 9 parent: {missing_from_parent}")

    cases = cases_doc.get("case_records", [])
    sources = sources_doc.get("sources", [])
    responses = responses_doc.get("responses", [])
    require(isinstance(cases, list) and len(cases) == 15, f"expected 15 case pathways, found {len(cases) if isinstance(cases, list) else 'invalid'}")
    require(isinstance(sources, list) and len(sources) == 33, f"expected 33 new sources, found {len(sources) if isinstance(sources, list) else 'invalid'}")
    require(isinstance(responses, list) and len(responses) == 20, f"expected 20 faithful responses, found {len(responses) if isinstance(responses, list) else 'invalid'}")
    if not isinstance(cases, list):
        cases = []
    if not isinstance(sources, list):
        sources = []
    if not isinstance(responses, list):
        responses = []

    case_ids = [item.get("case_id") for item in cases if isinstance(item, dict)]
    source_ids = [item.get("id") for item in sources if isinstance(item, dict)]
    response_ids = [item.get("id") for item in responses if isinstance(item, dict)]
    require(len(case_ids) == len(set(case_ids)) == 15, "case ids must be 15 unique values")
    require(len(source_ids) == len(set(source_ids)) == 33, "new source ids must be 33 unique values")
    require(response_ids == [f"FW-{index:02d}" for index in range(1, 21)], "response ids/order drift")
    require(not (set(source_ids) & set(inherited_ids)), "new source IDs collide with inherited parent IDs")

    required_case_fields = {
        "case_id", "display_name", "actor_groups", "loyalty_tension", "observed_problem",
        "action_chain", "what_helped", "what_failed", "pastoral_lesson", "boundary", "sources",
    }
    all_refs: list[str] = []
    role_groups: set[str] = set()
    action_groups: set[str] = set()
    for item in cases:
        if not isinstance(item, dict):
            errors.append("case record must be an object")
            continue
        case_id = item.get("case_id")
        require(required_case_fields.issubset(item), f"missing case fields: {case_id}")
        require(len(item.get("actor_groups", [])) >= 2, f"insufficient actor plurality: {case_id}")
        require(len(item.get("action_chain", [])) >= 3, f"insufficient action chain: {case_id}")
        require(len(item.get("sources", [])) >= 4, f"insufficient source pathway: {case_id}")
        require(len(item.get("boundary", "")) >= 45, f"weak boundary: {case_id}")
        require(len(item.get("pastoral_lesson", "")) >= 55, f"weak pastoral lesson: {case_id}")
        all_refs.extend(item.get("sources", []))
        role_groups.update(item.get("actor_groups", []))
        action_groups.update(item.get("action_chain", []))

    require(len(all_refs) == 105, f"expected 105 case-to-source references, found {len(all_refs)}")
    require(len(inherited_ids) == 72, f"expected 72 inherited source ids, found {len(inherited_ids)}")
    require(set(all_refs) == set(inherited_ids) | set(source_ids), "case source pool mismatch")
    require(len(role_groups) >= 20, f"actor-role diversity too low: {len(role_groups)}")
    require(len(action_groups) >= 12, f"action taxonomy coverage too low: {len(action_groups)}")

    for item in sources:
        if not isinstance(item, dict):
            errors.append("source record must be an object")
            continue
        sid = item.get("id")
        require(item.get("source_class") in {"A1", "A2", "A3", "B1"}, f"invalid source class: {sid}")
        parsed = urlparse(item.get("url", ""))
        require(parsed.scheme == "https" and bool(parsed.netloc), f"non-HTTPS source URL: {sid}")
        if item.get("source_class") == "B1":
            require(item.get("quote_safe") is False, f"B1 cannot be quote-safe: {sid}")
    require(sum(1 for item in sources if item.get("source_class") in {"A1", "A2", "A3"}) >= 17, "new A-class count below 17")

    required_response_fields = {
        "id", "title", "anti_advice_tension", "faithful_response", "when_appropriate",
        "when_not_enough", "case_ids", "scripture_controls",
    }
    covered_cases: set[str] = set()
    for item in responses:
        if not isinstance(item, dict):
            errors.append("response record must be an object")
            continue
        rid = item.get("id")
        require(required_response_fields.issubset(item), f"missing response fields: {rid}")
        require(len(item.get("case_ids", [])) >= 3, f"response lacks case grounding: {rid}")
        require(set(item.get("case_ids", [])).issubset(set(case_ids)), f"response references unknown case: {rid}")
        require(len(item.get("scripture_controls", [])) >= 2, f"response lacks biblical controls: {rid}")
        covered_cases.update(item.get("case_ids", []))
    require(len(covered_cases) >= 13, f"response coverage too narrow: {len(covered_cases)} cases")

    controls = responses_doc.get("controls", {})
    for key in (
        "no_universal_private_confrontation", "no_gossip_or_factionalism",
        "no_crime_concealment", "no_automatic_belief_or_automatic_disbelief",
        "no_self_declared_restoration",
    ):
        require(controls.get(key) is True, f"missing pastoral safety control: {key}")

    expected_counts = {
        "detailed_cases": 15,
        "action_pathway_source_references": 105,
        "inherited_source_ids": 72,
        "new_source_records": 33,
        "total_governing_source_pool": 181,
        "faithful_response_records": 20,
        "public_product_writes": 0,
    }
    counts = cases_doc.get("counts", {})
    for key, value in expected_counts.items():
        require(counts.get(key) == value, f"count drift for {key}: {counts.get(key)} != {value}")

    for marker in (
        "RESEARCH_CLOSED / PRODUCT_PUBLICATION_HOLD / NO PRODUCT WRITE",
        "Пятнадцать документированных путей", "Двадцать верных ответов",
        "105 ссылок case-to-source", "33 новых source records", "181 источник",
    ):
        require(marker in report, f"report marker missing: {marker}")
    require(len(re.findall(r"[А-Яа-яЁё]{2,}", report)) >= 1200, "report below 1200 Russian words")
    require("43_WAVE10_FAITHFUL_WITNESS_UNDER_PRESSURE_2026-08-01.md" in root_authority, "root authority missing Wave 10")
    require("181-source governing pool" in root_authority, "root authority missing Wave 10 count")
    require("NO PRODUCT WRITE" in root_authority, "root authority lost product boundary")
    for forbidden in ("src/pages/", "sitemap", "RSS", "Product write completed"):
        require(forbidden not in report, f"forbidden publication claim in report: {forbidden}")

    if errors:
        print(f"OSK Wave 10 faithful-witness authority: FAIL ({len(errors)})", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        "OSK Wave 10 faithful-witness authority: PASS — "
        f"{len(parent_pool)} verified Wave 9 parent IDs, 72 inherited IDs, "
        "15 cases, 33 new sources, 20 responses, 0 Product writes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
