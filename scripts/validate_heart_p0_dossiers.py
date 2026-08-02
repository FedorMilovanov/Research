#!/usr/bin/env python3
"""Fail-closed validator for the three Heart-series P0 architecture dossiers."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/heart-p0-architecture-dossiers-2026-08-02.json"
CURRENT = ROOT / "СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-02.md"
OVERLAY = ROOT / "СЕРИЯ СЕРДЦЕ/78_P0_ARCHITECTURE_CLOSURE_OVERLAY_2026-08-02.md"
OLD_AUTHORITY = ROOT / "СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-01.md"
ARCHITECTURE = ROOT / "СЕРИЯ СЕРДЦЕ/61_BOOK_ARCHITECTURE_V2_CHAPTERS_AND_RESEARCH_TASKS.md"
EXPECTED_AUTHORITY = "HEART-P0-ARCHITECTURE-CLOSURE-2026-08-02"
EXPECTED_DOSSIERS = {
    "HEART-P0-EDEN": {
        "path": "СЕРИЯ СЕРДЦЕ/75_P0_EDEN_HEART_CREATED_AND_FALLEN_2026-08-02.md",
        "chapter": "I.2",
        "prefix": "EDEN",
        "count": 8,
        "range": "EDEN-01…EDEN-08",
    },
    "HEART-P0-REPENTANCE": {
        "path": "СЕРИЯ СЕРДЦЕ/76_P0_BROKEN_HEART_REPENTANCE_2026-08-02.md",
        "chapter": "III.3",
        "prefix": "REP",
        "count": 8,
        "range": "REP-01…REP-08",
    },
    "HEART-P0-JUDGMENT": {
        "path": "СЕРИЯ СЕРДЦЕ/77_P0_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md",
        "chapter": "X.1",
        "prefix": "JUDG",
        "count": 10,
        "range": "JUDG-01…JUDG-10",
    },
}
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read {path.relative_to(ROOT)}: {exc}")
        return ""


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(read(path))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)} must contain a JSON object")
        return {}
    return value


def nonempty(value: Any, context: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{context}: non-empty string required")
    return value.strip() if isinstance(value, str) else ""


def russian_word_count(text: str) -> int:
    return len(re.findall(r"[А-Яа-яЁё]{2,}", text))


registry = load(REGISTRY)
require(registry.get("schemaVersion") == 1, "registry schemaVersion must be 1")
require(registry.get("authorityId") == EXPECTED_AUTHORITY, "registry authorityId drift")
require(registry.get("status") == "CURRENT_EVIDENCE_AND_BOUNDARY_CLOSED", "registry status drift")
require(registry.get("directQuotesApproved") is False, "new direct quotations must remain forbidden")
require(registry.get("publicationEligible") is True, "chapter evidence must remain publication-eligible")

sources = registry.get("sources")
require(isinstance(sources, list), "sources must be a list")
sources = sources if isinstance(sources, list) else []
source_ids: list[str] = []
source_urls: list[str] = []
for index, source in enumerate(sources, start=1):
    require(isinstance(source, dict), f"source #{index}: object required")
    if not isinstance(source, dict):
        continue
    sid = nonempty(source.get("id"), f"source #{index} id")
    source_ids.append(sid)
    source_class = nonempty(source.get("class"), f"{sid} class")
    require(source_class in {"A1", "A2"}, f"{sid}: only A1/A2 are permitted in P0 evidence core")
    nonempty(source.get("type"), f"{sid} type")
    nonempty(source.get("title"), f"{sid} title")
    url = nonempty(source.get("url"), f"{sid} url")
    source_urls.append(url)
    parsed = urlparse(url)
    require(parsed.scheme == "https" and bool(parsed.netloc), f"{sid}: HTTPS URL required")
    locators = source.get("locators")
    require(isinstance(locators, list) and bool(locators), f"{sid}: at least one locator required")
    if isinstance(locators, list):
        require(all(isinstance(item, str) and item.strip() for item in locators), f"{sid}: invalid locator")
    nonempty(source.get("use"), f"{sid} use")

require(len(sources) == 17, f"expected 17 sources, found {len(sources)}")
require(len(source_ids) == len(set(source_ids)), "source IDs must be unique")
require(len(source_urls) == len(set(source_urls)), "source URLs must be unique")
source_id_set = set(source_ids)

claims = registry.get("claims")
require(isinstance(claims, list), "claims must be a list")
claims = claims if isinstance(claims, list) else []
claim_ids: list[str] = []
claim_counts: Counter[str] = Counter()
status_counts: Counter[str] = Counter()
for index, claim in enumerate(claims, start=1):
    require(isinstance(claim, dict), f"claim #{index}: object required")
    if not isinstance(claim, dict):
        continue
    cid = nonempty(claim.get("id"), f"claim #{index} id")
    claim_ids.append(cid)
    dossier_id = nonempty(claim.get("dossierId"), f"{cid} dossierId")
    require(dossier_id in EXPECTED_DOSSIERS, f"{cid}: unknown dossierId {dossier_id}")
    if dossier_id in EXPECTED_DOSSIERS:
        spec = EXPECTED_DOSSIERS[dossier_id]
        require(cid.startswith(f"{spec['prefix']}-"), f"{cid}: wrong prefix for {dossier_id}")
        claim_counts[dossier_id] += 1
    status = nonempty(claim.get("status"), f"{cid} status")
    require(status in {"CLOSED", "BOUNDARY_CLOSED"}, f"{cid}: invalid status {status}")
    status_counts[status] += 1
    nonempty(claim.get("claim"), f"{cid} claim")
    support = claim.get("support")
    require(isinstance(support, list) and bool(support), f"{cid}: support IDs required")
    if isinstance(support, list):
        require(len(support) == len(set(support)), f"{cid}: duplicate support IDs")
        unknown = set(support) - source_id_set
        require(not unknown, f"{cid}: unknown source IDs {sorted(unknown)}")
    locators = claim.get("locators")
    require(isinstance(locators, list) and bool(locators), f"{cid}: exact locators required")
    if isinstance(locators, list):
        require(all(isinstance(item, str) and item.strip() for item in locators), f"{cid}: invalid locator")
    boundary = nonempty(claim.get("publicationBoundary"), f"{cid} publicationBoundary")
    require(len(boundary) >= 35, f"{cid}: publication boundary too weak")

require(len(claims) == 26, f"expected 26 claims, found {len(claims)}")
require(len(claim_ids) == len(set(claim_ids)), "claim IDs must be unique")
require(status_counts == Counter({"CLOSED": 19, "BOUNDARY_CLOSED": 7}), f"claim status counts drift: {dict(status_counts)}")
for dossier_id, spec in EXPECTED_DOSSIERS.items():
    require(claim_counts[dossier_id] == spec["count"], f"{dossier_id}: expected {spec['count']} claims, found {claim_counts[dossier_id]}")

# Dossier declarations must exactly match the machine registry and real files.
dossiers = registry.get("dossiers")
require(isinstance(dossiers, list) and len(dossiers) == 3, "exactly three dossier declarations required")
dossiers = dossiers if isinstance(dossiers, list) else []
declared_ids: list[str] = []
for row in dossiers:
    require(isinstance(row, dict), "dossier declaration must be an object")
    if not isinstance(row, dict):
        continue
    dossier_id = nonempty(row.get("id"), "dossier id")
    declared_ids.append(dossier_id)
    require(dossier_id in EXPECTED_DOSSIERS, f"unexpected dossier declaration: {dossier_id}")
    if dossier_id not in EXPECTED_DOSSIERS:
        continue
    spec = EXPECTED_DOSSIERS[dossier_id]
    require(row.get("path") == spec["path"], f"{dossier_id}: path drift")
    require(row.get("chapter") == spec["chapter"], f"{dossier_id}: chapter drift")
    expected_claims = [cid for cid in claim_ids if cid.startswith(f"{spec['prefix']}-")]
    require(row.get("claimIds") == expected_claims, f"{dossier_id}: declared claimIds drift")

require(set(declared_ids) == set(EXPECTED_DOSSIERS), "dossier declaration set drift")

required_markers = [
    "EVIDENCE CLOSED / BOUNDARIES CLOSED / CHAPTER-READY",
    "Прямые цитаты:** `0 approved`",
    "## 11. Запрещённые формулировки",
    "Source ledger",
    "## 13. Решение",
]
# Judgment has later numbering; semantic headings are checked separately below.
for dossier_id, spec in EXPECTED_DOSSIERS.items():
    path = ROOT / spec["path"]
    require(path.is_file(), f"{dossier_id}: dossier file missing")
    dossier_text = read(path)
    require(EXPECTED_AUTHORITY in dossier_text, f"{dossier_id}: authority marker missing")
    require(spec["range"] in dossier_text, f"{dossier_id}: claim range marker missing")
    require("EVIDENCE CLOSED / BOUNDARIES CLOSED / CHAPTER-READY" in dossier_text, f"{dossier_id}: chapter-ready status missing")
    require("Прямые цитаты:** `0 approved`" in dossier_text, f"{dossier_id}: zero-direct-quotes marker missing")
    require("Запрещённые формулировки" in dossier_text, f"{dossier_id}: forbidden wording section missing")
    require("Source ledger" in dossier_text, f"{dossier_id}: source ledger pointer missing")
    require("Решение" in dossier_text, f"{dossier_id}: final decision missing")
    require("data/heart-p0-architecture-dossiers-2026-08-02.json" in dossier_text, f"{dossier_id}: registry pointer missing")
    require(russian_word_count(dossier_text) >= 1200, f"{dossier_id}: dossier below depth floor")
    for forbidden in ("TODO", "TBD", "PUBLICATION_HOLD", "SOURCE NEEDED", "FIXME"):
        require(forbidden not in dossier_text, f"{dossier_id}: unresolved marker remains: {forbidden}")
    require("<blockquote" not in dossier_text and "<q" not in dossier_text, f"{dossier_id}: HTML direct-quote markup forbidden")

current_text = read(CURRENT)
overlay_text = read(OVERLAY)
old_authority_text = read(OLD_AUTHORITY)
architecture_text = read(ARCHITECTURE)
require("HEART-CURRENT-AUTHORITY-2026-08-02" in current_text, "current authority ID missing")
require(EXPECTED_AUTHORITY in current_text, "current authority does not compose P0 overlay")
require("Product/site publication | `NOT CLAIMED`" in current_text, "current authority must preserve Product boundary")
require(EXPECTED_AUTHORITY in overlay_text, "overlay authority marker missing")
require("3 DOSSIERS" in overlay_text and "26 CLAIM NODES" in overlay_text, "overlay machine counts missing")
require("Книга полностью собрана и опубликована" in overlay_text, "overlay must explicitly forbid false completion claim")
require("§5 P0-list superseded этим overlay" in overlay_text, "supersession scope missing")
require("P0. Must close before publication-ready prose" in old_authority_text, "historical P0 statement unexpectedly lost")
require("Сердце в Эдеме" in architecture_text and "Сокрушенное сердце" in architecture_text and "два воскресения" in architecture_text, "book architecture no longer exposes the original three gaps")

counts = registry.get("counts")
require(isinstance(counts, dict), "counts object required")
if isinstance(counts, dict):
    require(counts.get("dossiers") == 3, "registry dossier count drift")
    require(counts.get("sources") == 17, "registry source count drift")
    require(counts.get("claims") == 26, "registry claim count drift")
    require(counts.get("closedClaims") == 19, "registry CLOSED count drift")
    require(counts.get("boundaryClosedClaims") == 7, "registry BOUNDARY_CLOSED count drift")
    require(counts.get("directQuotesApproved") == 0, "registry direct quote count must remain zero")

if errors:
    print(f"Heart P0 dossiers: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Heart P0 dossiers: PASS — 3 dossiers, 17 sources, 26 claims, 0 direct quotes")
