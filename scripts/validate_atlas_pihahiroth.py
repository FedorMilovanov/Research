#!/usr/bin/env python3
"""Validate the Pihahiroth uncertainty-geometry authority."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/atlas-pihahiroth-authority-2026-08-02.json"
DOSSIER = ROOT / "БИБЛЕЙСКИЙ АТЛАС/GEO-DOSSIER-pihahiroth.md"
CURRENT = ROOT / "БИБЛЕЙСКИЙ АТЛАС/00_CURRENT_AUTHORITY_2026-08-02.md"
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


def load(path: Path) -> dict:
    try:
        value = json.loads(read(path))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain an object")
    return value if isinstance(value, dict) else {}


registry = load(REGISTRY)
require(registry.get("schemaVersion") == 1, "schemaVersion drift")
require(registry.get("authorityId") == "ATLAS-PIHAHIROTH-AUTHORITY-2026-08-02", "authority ID drift")
require(registry.get("status") == "CURRENT_TEXTUAL_CONSTRAINTS_CLOSED_EXACT_LOCATION_UNRESOLVED", "status drift")
require(registry.get("exactCoordinateStatus") == "UNRESOLVED", "exact coordinate must remain unresolved")
require(registry.get("publicationDecision") == "CANDIDATE_CORRIDORS_ONLY_NO_SINGLE_AUTHORITATIVE_POINT", "publication decision drift")
require(registry.get("directQuotesApproved") is False, "new direct quotations forbidden")

constraints = registry.get("textualConstraints")
require(isinstance(constraints, list) and len(constraints) == 8, "exactly eight textual constraints required")
constraints = constraints if isinstance(constraints, list) else []
constraint_ids = [row.get("id") for row in constraints if isinstance(row, dict)]
require(len(constraint_ids) == len(set(constraint_ids)), "constraint IDs must be unique")
status_counts = Counter(row.get("status") for row in constraints if isinstance(row, dict))
require(status_counts == Counter({"CLOSED": 5, "BOUNDARY_CLOSED": 3}), f"constraint status drift: {dict(status_counts)}")
for row in constraints:
    require(isinstance(row, dict), "constraint object required")
    if not isinstance(row, dict):
        continue
    cid = str(row.get("id", ""))
    require(bool(str(row.get("claim", "")).strip()), f"{cid}: claim required")
    locators = row.get("locators")
    require(isinstance(locators, list) and bool(locators), f"{cid}: locators required")

candidates = registry.get("candidates")
require(isinstance(candidates, list) and len(candidates) == 3, "exactly three candidates required")
candidates = candidates if isinstance(candidates, list) else []
required_candidates = {"PH-CAND-NORTH", "PH-CAND-BALLAH", "PH-CAND-BITTER"}
require({row.get("id") for row in candidates if isinstance(row, dict)} == required_candidates, "candidate set drift")
for row in candidates:
    if not isinstance(row, dict):
        continue
    cid = str(row.get("id", ""))
    require(row.get("geometry") == "CORRIDOR_NOT_POINT", f"{cid}: point geometry forbidden")
    require(row.get("status") in {"CANDIDATE", "ALTERNATIVE"}, f"{cid}: invalid status")
    require(row.get("confidence") in {"LOW", "MODERATE_LOW"}, f"{cid}: confidence overclaim")
    require(isinstance(row.get("supports"), list) and len(row["supports"]) >= 2, f"{cid}: insufficient supports")
    require(isinstance(row.get("problems"), list) and len(row["problems"]) >= 3, f"{cid}: insufficient problems")

map_contract = registry.get("mapContract") or {}
require(map_contract.get("canonicalFeatureType") == "uncertainty-area", "feature type drift")
require(map_contract.get("renderSinglePoint") is False, "single authoritative point forbidden")
require(map_contract.get("renderCandidates") is True, "candidate rendering required")
require(map_contract.get("defaultCandidate") == "PH-CAND-BALLAH", "default candidate drift")
require(map_contract.get("defaultCandidateIsCertain") is False, "default candidate cannot be certain")
require("Точное место" in str(map_contract.get("requiredReaderLabel", "")), "reader uncertainty label missing")
require(isinstance(map_contract.get("forbiddenClaims"), list) and len(map_contract["forbiddenClaims"]) >= 5, "forbidden claim list too small")

rights = registry.get("rightsContract") or {}
require(rights.get("baseMap", {}).get("publicationState") == "APPROVED_WITH_ATTRIBUTION_NOTE", "base-map rights drift")
require(rights.get("archaeologicalMaps", {}).get("publicationState") == "LINK_OR_DERIVED_SCHEMATIC_ONLY_UNLESS_LICENSE_EXPLICIT", "archaeological map rights drift")

sources = registry.get("sources")
require(isinstance(sources, list) and len(sources) == 9, "exactly nine sources required")
sources = sources if isinstance(sources, list) else []
source_ids: list[str] = []
for row in sources:
    require(isinstance(row, dict), "source object required")
    if not isinstance(row, dict):
        continue
    sid = str(row.get("id", "")).strip()
    source_ids.append(sid)
    require(row.get("class") in {"A1", "A2", "A3"}, f"{sid}: invalid source class")
    raw_url = str(row.get("url", "")).strip()
    parsed = urlparse(raw_url)
    require(parsed.scheme == "https" and bool(parsed.netloc), f"{sid}: HTTPS URL required")
    require(isinstance(row.get("locators"), list) and bool(row["locators"]), f"{sid}: locator required")
    require(bool(str(row.get("use", "")).strip()), f"{sid}: use required")
require(len(source_ids) == len(set(source_ids)), "source IDs must be unique")

counts = registry.get("counts") or {}
require(counts.get("textualConstraints") == 8, "constraint count drift")
require(counts.get("closedConstraints") == 5, "closed count drift")
require(counts.get("boundaryClosedConstraints") == 3, "boundary count drift")
require(counts.get("candidates") == 3, "candidate count drift")
require(counts.get("sources") == 9, "source count drift")
require(counts.get("directQuotesApproved") == 0, "direct quote count must remain zero")
require(counts.get("authoritativePoints") == 0, "authoritative point count must remain zero")

dossier = read(DOSSIER)
current = read(CURRENT)
for marker in (
    "ATLAS-PIHAHIROTH-AUTHORITY-2026-08-02",
    "TEXTUAL CONSTRAINTS CLOSED / EXACT LOCATION UNRESOLVED",
    "Точное место Пи-Гахирофа и перехода не установлено",
    "SINGLE AUTHORITATIVE POINT = FORBIDDEN",
    "data/atlas-pihahiroth-authority-2026-08-02.json",
):
    require(marker in dossier, f"dossier marker missing: {marker}")
require(len(re.findall(r"[А-Яа-яЁё]{2,}", dossier)) >= 1200, "dossier below depth floor")
for forbidden in ("TODO", "TBD", "PUBLICATION_HOLD", "Археологи нашли точное место перехода"):
    require(forbidden not in dossier, f"unresolved/forbidden dossier marker: {forbidden}")
require("ATLAS-CURRENT-AUTHORITY-2026-08-02" in current, "current Atlas authority missing")
require("single authoritative point | `FORBIDDEN`" in current, "current authority must forbid single point")
require("Product implementation open" in current or "PRODUCT IMPLEMENTATION OPEN" in current, "implementation boundary missing")

if errors:
    print(f"Atlas Pihahiroth: FAIL ({len(errors)})", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Atlas Pihahiroth: PASS — 8 constraints, 3 corridors, 9 sources, 0 authoritative points")
