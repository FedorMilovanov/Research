#!/usr/bin/env python3
import json
import pathlib
import re
import sys
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "data/osk-wave10-faithful-witness-cases-2026-08-01.json"
SOURCES_PATH = ROOT / "data/osk-wave10-faithful-witness-new-sources-2026-08-01.json"
RESPONSES_PATH = ROOT / "data/osk-wave10-twenty-faithful-responses-2026-08-01.json"
REPORT_PATH = ROOT / "ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/43_WAVE10_FAITHFUL_WITNESS_UNDER_PRESSURE_2026-08-01.md"
ROOT_AUTHORITY_PATH = ROOT / "00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md"

AUTHORITY = "RESEARCH-OSK-AUTHORITY-2026-08-01-W10-FAITHFUL-WITNESS"
errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

cases_doc = json.loads(CASES_PATH.read_text(encoding="utf-8"))
sources_doc = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
responses_doc = json.loads(RESPONSES_PATH.read_text(encoding="utf-8"))
report = REPORT_PATH.read_text(encoding="utf-8")
root_authority = ROOT_AUTHORITY_PATH.read_text(encoding="utf-8")

require(cases_doc.get("authority_id") == AUTHORITY, "case authority id drift")
require(sources_doc.get("authority_id") == AUTHORITY, "source authority id drift")
require(responses_doc.get("authority_id") == AUTHORITY, "response authority id drift")
require(cases_doc.get("parent_authority") == "RESEARCH-OSK-AUTHORITY-2026-08-01-W9", "wrong parent authority")
require(cases_doc.get("status") == "RESEARCH_CLOSED_PRODUCT_PUBLICATION_HOLD", "wrong publication boundary")

cases = cases_doc.get("case_records", [])
sources = sources_doc.get("sources", [])
responses = responses_doc.get("responses", [])
require(len(cases) == 15, f"expected 15 case pathways, found {len(cases)}")
require(len(sources) == 33, f"expected 33 new sources, found {len(sources)}")
require(len(responses) == 20, f"expected 20 faithful responses, found {len(responses)}")

case_ids = [item.get("case_id") for item in cases]
require(len(set(case_ids)) == 15, "case ids must be unique")
source_ids = [item.get("id") for item in sources]
require(len(set(source_ids)) == 33, "new source ids must be unique")
response_ids = [item.get("id") for item in responses]
require(len(set(response_ids)) == 20, "response ids must be unique")
require(response_ids == [f"FW-{i:02d}" for i in range(1, 21)], "response ids/order drift")

required_case_fields = {
    "case_id", "display_name", "actor_groups", "loyalty_tension", "observed_problem",
    "action_chain", "what_helped", "what_failed", "pastoral_lesson", "boundary", "sources"
}
all_refs = []
role_groups = set()
action_groups = set()
for item in cases:
    require(required_case_fields.issubset(item), f"missing case fields: {item.get('case_id')}")
    require(len(item.get("actor_groups", [])) >= 2, f"insufficient actor plurality: {item.get('case_id')}")
    require(len(item.get("action_chain", [])) >= 3, f"insufficient action chain: {item.get('case_id')}")
    require(len(item.get("sources", [])) >= 4, f"insufficient source pathway: {item.get('case_id')}")
    require(len(item.get("boundary", "")) >= 45, f"weak boundary: {item.get('case_id')}")
    require(len(item.get("pastoral_lesson", "")) >= 55, f"weak pastoral lesson: {item.get('case_id')}")
    all_refs.extend(item.get("sources", []))
    role_groups.update(item.get("actor_groups", []))
    action_groups.update(item.get("action_chain", []))

require(len(all_refs) == 105, f"expected 105 case-to-source references, found {len(all_refs)}")
require(len(cases_doc.get("inherited_source_ids", [])) == 72, "expected 72 inherited source ids")
require(set(all_refs) == set(cases_doc.get("inherited_source_ids", [])) | set(source_ids), "case source pool mismatch")
require(len(role_groups) >= 20, f"actor-role diversity too low: {len(role_groups)}")
require(len(action_groups) >= 12, f"action taxonomy coverage too low: {len(action_groups)}")

for item in sources:
    require(item.get("source_class") in {"A1", "A2", "A3", "B1"}, f"invalid source class: {item.get('id')}")
    parsed = urlparse(item.get("url", ""))
    require(parsed.scheme == "https" and bool(parsed.netloc), f"non-HTTPS source URL: {item.get('id')}")
    if item.get("source_class") == "B1":
        require(item.get("quote_safe") is False, f"B1 cannot be quote-safe: {item.get('id')}")
require(sum(1 for item in sources if item.get("source_class") in {"A1","A2","A3"}) >= 17, "new A-class count below 17")

required_response_fields = {
    "id", "title", "anti_advice_tension", "faithful_response", "when_appropriate",
    "when_not_enough", "case_ids", "scripture_controls"
}
covered_cases = set()
for item in responses:
    require(required_response_fields.issubset(item), f"missing response fields: {item.get('id')}")
    require(len(item.get("case_ids", [])) >= 3, f"response lacks case grounding: {item.get('id')}")
    require(set(item.get("case_ids", [])).issubset(set(case_ids)), f"response references unknown case: {item.get('id')}")
    require(len(item.get("scripture_controls", [])) >= 2, f"response lacks biblical controls: {item.get('id')}")
    covered_cases.update(item.get("case_ids", []))
require(len(covered_cases) >= 13, f"response coverage too narrow: {len(covered_cases)} cases")

controls = responses_doc.get("controls", {})
for key in (
    "no_universal_private_confrontation", "no_gossip_or_factionalism",
    "no_crime_concealment", "no_automatic_belief_or_automatic_disbelief",
    "no_self_declared_restoration"
):
    require(controls.get(key) is True, f"missing pastoral safety control: {key}")

counts = cases_doc.get("counts", {})
expected_counts = {
    "detailed_cases": 15,
    "action_pathway_source_references": 105,
    "inherited_source_ids": 72,
    "new_source_records": 33,
    "total_governing_source_pool": 181,
    "faithful_response_records": 20,
    "public_product_writes": 0,
}
for key, value in expected_counts.items():
    require(counts.get(key) == value, f"count drift for {key}: {counts.get(key)} != {value}")

for marker in (
    "RESEARCH_CLOSED / PRODUCT_PUBLICATION_HOLD / NO PRODUCT WRITE",
    "Пятнадцать документированных путей",
    "Двадцать верных ответов",
    "105 ссылок case-to-source",
    "33 новых source records",
    "181 источник",
):
    require(marker in report, f"report marker missing: {marker}")
require(len(re.findall(r"[А-Яа-яЁё]{2,}", report)) >= 1200, "report below 1200 Russian words")
require("43_WAVE10_FAITHFUL_WITNESS_UNDER_PRESSURE_2026-08-01.md" in root_authority, "root authority missing Wave 10")
require("181-source governing pool" in root_authority, "root authority missing Wave 10 count")
require("NO PRODUCT WRITE" in root_authority, "root authority lost product boundary")

for forbidden in ("src/pages/", "sitemap", "RSS", "Product write completed"):
    require(forbidden not in report, f"forbidden publication claim in report: {forbidden}")

if errors:
    print(f"❌ OSK Wave 10 faithful-witness authority failed ({len(errors)})")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print(
    "✅ OSK Wave 10 faithful-witness authority passed: "
    "15 cases, 105 case-source refs, 33 new sources, 181-source pool, "
    "20 faithful responses, 0 Product writes"
)
