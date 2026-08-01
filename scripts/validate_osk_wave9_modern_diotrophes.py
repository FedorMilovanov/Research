#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/osk-wave9-modern-diotrophes-source-manifest-2026-08-01.json"
OUTLINE = ROOT / "data/osk-wave9-modern-diotrophes-outline-2026-08-01.json"
REPORT = ROOT / "ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/42_WAVE9_MODERN_DIOTROPHES_EDITORIAL_OUTLINE_2026-08-01.md"

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
A_CLASSES = {"A1", "A2", "A3"}
CASE_ALLOWED_CLASSES = A_CLASSES | {"B1"}
EXPECTED_EXCLUSIONS = {"W2-SHI-07", "W2-MOS-07"}

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}")
        return {}


manifest = load(MANIFEST)
outline = load(OUTLINE)

if manifest.get("schema_version") != 1 or outline.get("schema_version") != 1:
    fail("schema_version must be 1")
if manifest.get("authority_id") != "RESEARCH-OSK-AUTHORITY-2026-08-01-W9":
    fail("manifest authority_id drift")
if outline.get("authority_id") != manifest.get("authority_id"):
    fail("outline authority mismatch")
if outline.get("status") != "READY_FOR_EDITORIAL_DRAFT_NO_PRODUCT_WRITE":
    fail("outline status drift")
if manifest.get("route_candidate") != "/articles/diotrefy-nashego-vremeni/":
    fail("route candidate drift")

policy = manifest.get("policy", {})
for flag in (
    "one_primary_power_mechanism_per_case",
    "all_case_claims_require_a_class_support",
    "b1_is_corroboration_only",
    "c_and_d_sources_forbidden",
    "negative_and_exclusion_controls_forbidden",
    "headline_must_not_label_each_person_diotrophes",
    "no_guilt_roster",
    "dark_side_standalone_and_conditional_excluded",
):
    if policy.get(flag) is not True:
        fail(f"policy flag must be true: {flag}")
if policy.get("new_direct_quotes_approved") is not False:
    fail("new direct quotes must remain false")
if policy.get("product_write_approved") is not False:
    fail("product write must remain false")
if int(policy.get("minimum_total_sources", 0)) < 40:
    fail("minimum source threshold must be at least 40")

sets = {item.get("id"): item for item in manifest.get("source_sets", [])}
if set(sets) != {
    "wave1-core-case-evidence",
    "wave2-promoted-core-case-evidence",
    "wave7-biblical-academic-safeguarding-controls",
}:
    fail("source-set inventory drift")

case_sources: list[dict] = []
for set_id in ("wave1-core-case-evidence", "wave2-promoted-core-case-evidence"):
    spec = sets.get(set_id, {})
    included = set(spec.get("included_case_ids", []))
    excluded = set(spec.get("excluded_source_ids", []))
    if set_id == "wave2-promoted-core-case-evidence" and excluded != EXPECTED_EXCLUSIONS:
        fail("Wave 2 exclusion controls drift")
    loaded: list[dict] = []
    for rel in spec.get("shards", []):
        shard = load(ROOT / rel)
        loaded.extend(shard.get("sources", []))
    selected = [
        source for source in loaded
        if source.get("case_id") in included and source.get("id") not in excluded
    ]
    case_sources.extend(selected)

    reported = spec.get("counters", {})
    classes = Counter(source.get("source_class") for source in selected)
    calculated = {
        "sources": len(selected),
        "a_class": sum(classes[name] for name in A_CLASSES),
        "b1": classes["B1"],
        "exact_urls": sum(bool(source.get("url")) for source in selected),
        "quote_safe": sum(source.get("quote_safe") is True for source in selected),
    }
    for key, value in calculated.items():
        if reported.get(key) != value:
            fail(f"{set_id}: counter drift for {key}: {reported.get(key)} != {value}")

case_source_ids = [source.get("id") for source in case_sources]
if len(case_source_ids) != len(set(case_source_ids)):
    fail("duplicate case-evidence source IDs")
for source in case_sources:
    if source.get("source_class") not in CASE_ALLOWED_CLASSES:
        fail(f"{source.get('id')}: forbidden case source class {source.get('source_class')}")
    if source.get("source_class") == "B1" and source.get("quote_safe") is True:
        fail(f"{source.get('id')}: B1 cannot be quote_safe")

control_spec = sets.get("wave7-biblical-academic-safeguarding-controls", {})
control_registry = load(ROOT / control_spec.get("registry", ""))
all_controls = {source.get("id"): source for source in control_registry.get("sources", [])}
control_ids = control_spec.get("included_source_ids", [])
if len(control_ids) != len(set(control_ids)):
    fail("duplicate control source IDs")
controls = [all_controls.get(source_id) for source_id in control_ids]
if any(source is None for source in controls):
    fail("unknown Wave 7 control source ID")
controls = [source for source in controls if source is not None]
for source in controls:
    url = str(source.get("url", ""))
    if not url.startswith("https://"):
        fail(f"{source.get('id')}: control source requires HTTPS URL")
    if source.get("source_class") in {"PASTORAL_ARTICLE", "HISTORICAL_COMMENTARY"}:
        fail(f"{source.get('id')}: lower-control class excluded from Wave 9")

reported_controls = control_spec.get("counters", {})
categories = Counter()
for source in controls:
    sid = str(source.get("id"))
    if sid.startswith("W7-BIB-"):
        categories["biblical_exegetical"] += 1
    elif sid.startswith("W7-PSY-"):
        categories["psychology_organization"] += 1
    elif sid.startswith("W7-SAF-"):
        categories["safeguarding_governance"] += 1
for key, value in {
    "sources": len(controls),
    "unique_urls": len({source.get("url") for source in controls}),
    **categories,
}.items():
    if reported_controls.get(key) != value:
        fail(f"control counter drift for {key}: {reported_controls.get(key)} != {value}")

classes = Counter(source.get("source_class") for source in case_sources)
computed = {
    "core_cases": len({source.get("case_id") for source in case_sources}),
    "case_evidence_sources": len(case_sources),
    "a_class_case_sources": sum(classes[name] for name in A_CLASSES),
    "b1_case_sources": classes["B1"],
    "exact_url_case_sources": sum(bool(source.get("url")) for source in case_sources),
    "quote_safe_case_sources": sum(source.get("quote_safe") is True for source in case_sources),
    "control_sources": len(controls),
    "total_sources": len(case_sources) + len(controls),
}
reported = manifest.get("counters", {})
for key, value in computed.items():
    if reported.get(key) != value:
        fail(f"manifest counter drift for {key}: {reported.get(key)} != {value}")
if computed["total_sources"] < 40:
    fail("Wave 9 source pool fell below 40")
for key in ("dark_side_cases", "standalone_cases", "conditional_cases", "approved_direct_quotes"):
    if reported.get(key) != 0:
        fail(f"{key} must remain zero")

records = outline.get("case_records", [])
if len(records) != 21:
    fail(f"expected 21 case records, found {len(records)}")
record_ids = [record.get("case_id") for record in records]
if len(record_ids) != len(set(record_ids)):
    fail("duplicate outline case IDs")
source_case_ids = {source.get("case_id") for source in case_sources}
if set(record_ids) != source_case_ids:
    fail("outline case IDs differ from verified case-source pool")

sources_by_case: dict[str, list[dict]] = defaultdict(list)
for source in case_sources:
    sources_by_case[source.get("case_id")].append(source)

section_ids = {section.get("id") for section in outline.get("sections", [])}
for record in records:
    case_id = record.get("case_id")
    mechanism = record.get("primary_power_mechanism")
    if mechanism not in ALLOWED_MECHANISMS:
        fail(f"{case_id}: invalid primary mechanism")
    if record.get("route") != "ANTISOVETY_CORE":
        fail(f"{case_id}: non-core route leaked into Wave 9")
    if record.get("section_id") not in section_ids:
        fail(f"{case_id}: unknown section")
    if record.get("direct_quote_mode") != "NO_NEW_DIRECT_QUOTES":
        fail(f"{case_id}: direct quote mode drift")
    if record.get("card_mode") != "BOUNDED_EVIDENCE_CARD":
        fail(f"{case_id}: card mode drift")
    if not record.get("permitted_claim") or not record.get("blocked_claim"):
        fail(f"{case_id}: missing claim boundary")
    sources = sources_by_case.get(case_id, [])
    if len(sources) < 2:
        fail(f"{case_id}: fewer than two case sources")
    a_count = sum(source.get("source_class") in A_CLASSES for source in sources)
    if a_count < int(record.get("minimum_a_class_sources", 1)):
        fail(f"{case_id}: insufficient A-class support")
    if all(source.get("source_class") == "B1" for source in sources):
        fail(f"{case_id}: B1-only case forbidden")
    if record.get("headline_rule") != "Name the case or institution; do not state that the person is Diotrephes.":
        fail(f"{case_id}: headline rule drift")

section_case_ids: list[str] = []
for section in outline.get("sections", []):
    section_case_ids.extend(section.get("case_ids", []))
if sorted(section_case_ids) != sorted(record_ids):
    fail("section membership must contain every case exactly once")
if len(section_case_ids) != len(set(section_case_ids)):
    fail("case appears in multiple sections")

publication = outline.get("publication_controls", {})
if publication.get("case_cards") != 21 or publication.get("one_mechanism_each") is not True:
    fail("publication card controls drift")
for key in (
    "dark_side_or_standalone_cards",
    "conditional_cards",
    "new_direct_quotes",
    "product_files_changed",
):
    if publication.get(key) != 0:
        fail(f"publication control must remain zero: {key}")
if publication.get("case_headlines_are_verdicts") is not False:
    fail("case headlines cannot be verdicts")
if publication.get("modern_names_in_biblical_definition_section") is not False:
    fail("biblical definition section must remain name-free")

try:
    report = REPORT.read_text(encoding="utf-8")
except Exception as exc:
    fail(f"report unreadable: {exc}")
    report = ""
for marker in (
    "148",
    "119 case evidence + 29 controls",
    "102 A1/A2/A3",
    "READY_FOR_EDITORIAL_DRAFT / NO PRODUCT WRITE",
    "W2-SHI-07",
    "W2-MOS-07",
    "Не ярлык, а проверяемый механизм",
):
    if marker not in report:
        fail(f"report missing marker: {marker}")

if errors:
    print(f"❌ OSK Wave 9 validation failed ({len(errors)}):", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "✅ OSK Wave 9 passed: "
    f"{len(records)} core cases, {len(case_sources)} case sources "
    f"({computed['a_class_case_sources']} A-class, {computed['b1_case_sources']} B1), "
    f"{len(controls)} controls, {computed['total_sources']} total, "
    "0 dark-side/standalone/conditional cards, 0 product writes"
)
