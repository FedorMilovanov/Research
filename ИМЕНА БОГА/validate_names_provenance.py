#!/usr/bin/env python3
"""Fail-closed provenance graph validation for names research.

NOT a textual-critical apparatus, a remote source truth check, or a Product
publication license. This makes source and edition connections queryable
without silently manufacturing 105 independently certified interpretations.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
BASELINE_PATH = DATA / "names_ledger_v1.json"
EXTENSION_PATH = DATA / "names_extension_ledger_v1.json"
SOURCE_PATH = DATA / "source_access_register_v1.json"
EDITIONS_PATH = DATA / "names_edition_registry_v1.json"
CLAIMS_PATH = DATA / "names_claim_registry_v1.json"

EXPECTED_EDITIONS = {
    "ED-MECHON-MT-ONLINE",
    "ED-SBLGNT-2010-BIBLEGATEWAY",
    "ED-THGNT-2017-BIBLEGATEWAY",
    "ED-RAHLFS-HANHART-2006-PUBLISHER",
}
ED_MT = "ED-MECHON-MT-ONLINE"
ED_SBL = "ED-SBLGNT-2010-BIBLEGATEWAY"
ED_THG = "ED-THGNT-2017-BIBLEGATEWAY"
ED_LXX = "ED-RAHLFS-HANHART-2006-PUBLISHER"

PUBLISHER_LXX = {
    "EXO.3": "SRC-RAHLFS-EXODUS3",
    "EXO.17": "SRC-RAHLFS-EXODUS17",
    "ISA.7.14": "SRC-RAHLFS-ISAIAH",
}
CORE_CLAIMS = {
    "CLM-EX3-15-DIVINE-NAME",
    "CLM-IS43-10-NEGATED-EL",
    "CLM-IS43-12-YHWH-EL",
    "CLM-GEN22-14-PLACE-NAME",
    "CLM-EX17-15-ALTAR-MT-LXX",
    "CLM-JUD6-23-24-PEACE-ALTAR",
    "CLM-JOHN9-9-HUMAN-EGO-EIMI",
    "CLM-LXX-EX3-JOHN8-DIFFERENT-CLAUSES",
    "CLM-ABBA-THREE-PRAYER-SUBJECTS",
    "CLM-YHWH-HISTORICAL-PRONUNCIATION",
}
CLAIM_REQUIRED_ATTESTATIONS = {
    "CLM-EX3-15-DIVINE-NAME": {"ATT-BASE-YHWH-01"},
    "CLM-IS43-10-NEGATED-EL": {"ATT-BASE-EL-04"},
    "CLM-IS43-12-YHWH-EL": {"ATT-BASE-EL-05"},
    "CLM-GEN22-14-PLACE-NAME": {"ATT-BASE-YIREH-02"},
    "CLM-EX17-15-ALTAR-MT-LXX": {"ATT-BASE-NISSI-01", "ATT-BASE-NISSI-02"},
    "CLM-JUD6-23-24-PEACE-ALTAR": {"ATT-BASE-SHALOM-01", "ATT-BASE-SHALOM-02"},
    "CLM-JOHN9-9-HUMAN-EGO-EIMI": {"ATT-BASE-EGO-EIMI-03"},
    "CLM-LXX-EX3-JOHN8-DIFFERENT-CLAUSES": {"ATT-BASE-EHYEH-03", "ATT-BASE-EGO-EIMI-02"},
    "CLM-ABBA-THREE-PRAYER-SUBJECTS": {"ATT-BASE-ABBA-01", "ATT-BASE-ABBA-02", "ATT-BASE-ABBA-03"},
    "CLM-YHWH-HISTORICAL-PRONUNCIATION": {"ATT-BASE-YHWH-01", "ATT-BASE-YHWH-02"},
}


def validate_provenance(
    baseline: dict, extension: dict, sources: dict, editions: dict, claims: dict
) -> list[str]:
    errors: list[str] = []
    if editions.get("schemaVersion") != 1 or editions.get("corpusId") != "NAMES_OF_GOD_CANONICAL_DIGITAL_TEXT_EDITIONS":
        errors.append("provenance: wrong edition-registry version or authority")
    if claims.get("schemaVersion") != 1 or claims.get("corpusId") != "NAMES_OF_GOD_CLAIM_LEVEL_EVIDENCE":
        errors.append("provenance: wrong claim-registry version or authority")
    if editions.get("status") != "RESEARCH_ONLY_NOT_CRITICAL_MANUSCRIPT_EDITORIAL_APPROVAL":
        errors.append("provenance: edition registry improperly elevated to primary manuscript authority")

    source_rows = sources.get("records", [])
    source_map = {s["id"]: s for s in source_rows if isinstance(s, dict) and isinstance(s.get("id"), str)}
    if len(source_map) != len(source_rows):
        errors.append("provenance: missing or duplicate source IDs")
    if "SRC-SBLGNT-DIGITAL-NT" not in source_map:
        errors.append("provenance: no SBLGNT generic passage source, only license/other verse")

    edition_rows = editions.get("records", [])
    edition_map = {e["id"]: e for e in edition_rows if isinstance(e, dict) and isinstance(e.get("id"), str)}
    if len(edition_rows) != len(edition_map) or set(edition_map) != EXPECTED_EDITIONS:
        errors.append("provenance: four distinct stable edition IDs required")
    for edition_id, item in edition_map.items():
        if item.get("criticalEditionCollated") is not False or item.get("publicationState") != "BLOCKED":
            errors.append(f"provenance: edition {edition_id} was falsely promoted")
        permitted = item.get("sourceRecordIds", [])
        if not isinstance(permitted, list) or not permitted or any(x not in source_map for x in permitted):
            errors.append(f"provenance: edition {edition_id} has orphan source ID")
        if edition_id == ED_SBL:
            if item.get("publisherLicenseSourceId") != "SRC-SBLGNT-CCBY-LICENSE" or item.get("rightsState") != "RIGHTS_UNKNOWN":
                errors.append("provenance: SBLGNT host license improperly inherited from publisher")
        if edition_id in {ED_THG, ED_LXX} and item.get("rightsState") != "PERMISSION_REQUIRED":
            errors.append(f"provenance: copyright of Greek edition {edition_id} falsely waived")

    seen: set[str] = set()
    att_by_id: dict[str, dict] = {}
    num = 0
    for ledger_name, ledger, prefix, expected_count in (
        ("baseline", baseline, "BASE", 29),
        ("extension", extension, "EXT", 13),
    ):
        rows = ledger.get("records", [])
        if not isinstance(rows, list) or len(rows) != expected_count:
            errors.append(f"provenance: {ledger_name} record count changed")
            continue
        for parent in rows:
            if not isinstance(parent, dict):
                errors.append(f"provenance: invalid {ledger_name} record")
                continue
            candidate_id = parent.get("id", "")
            attestations = parent.get("attestations", [])
            if not isinstance(attestations, list) or not attestations:
                errors.append(f"provenance: {ledger_name}/{candidate_id} has no original-language usage")
                continue
            for obs in attestations:
                if not isinstance(obs, dict):
                    errors.append(f"provenance: invalid occurrence {candidate_id}")
                    continue
                num += 1
                aid = obs.get("attestationId")
                if not isinstance(aid, str) or not re.fullmatch(
                    rf"ATT-{prefix}-{re.escape(str(candidate_id).upper())}-[0-9]{{2,}}", aid
                ) or aid in seen:
                    errors.append(f"provenance: missing/duplicate/stale attestation ID {aid}")
                    continue
                seen.add(aid)
                att_by_id[aid] = obs
                edition_id = obs.get("editionId")
                source_id = obs.get("sourceId")
                edition = edition_map.get(edition_id, {})
                source = source_map.get(source_id, {})
                if not edition:
                    errors.append(f"provenance: {aid} has orphan edition {edition_id}")
                    continue
                if not source:
                    errors.append(f"provenance: {aid} has orphan source {source_id}")
                if source_id not in edition.get("sourceRecordIds", []):
                    errors.append(f"provenance: {aid} linked source not of that edition family")
                if obs.get("edition") not in edition.get("compatibleRawEditionStrings", []):
                    errors.append(f"provenance: {aid} printed edition text does not match its edition ID")
                if obs.get("language") not in edition.get("languageGroup", []):
                    errors.append(f"provenance: {aid} language does not fit edition")
                if not str(obs.get("sourceUrl", "")).startswith("https://"):
                    errors.append(f"provenance: {aid} exact original passage URL missing")
                if not str(obs.get("verse", "")).strip() or not str(obs.get("surface", "")).strip():
                    errors.append(f"provenance: {aid} lacks original script or verse locator")
                if obs.get("criticalEditionStatus") != "NOT_COLLATED":
                    errors.append(f"provenance: {aid} falsely certified critical apparatus")
                if obs.get("publicationState") not in (None, "BLOCKED"):
                    errors.append(f"provenance: {aid} unauthorized publication")
                if source and source.get("publicationState") != "BLOCKED":
                    errors.append(f"provenance: {aid} linked to unreviewed Product-approved source")
                if source and obs.get("rightsState") != source.get("rightsState"):
                    errors.append(f"provenance: {aid} rights changed from source-level citation")
                url = obs.get("sourceUrl", "")
                if edition_id == ED_MT:
                    correct = "SRC-DANIEL-ARAMAIC" if obs.get("language") == "aramaic" else "SRC-MT-MECHON"
                    if source_id != correct or "mechon-mamre.org" not in url:
                        errors.append(f"provenance: {aid} MT Aramaic/Hebrew source binding incorrect")
                if edition_id == ED_SBL:
                    if source_id != "SRC-SBLGNT-DIGITAL-NT":
                        errors.append(f"provenance: {aid} SBLGNT passage source incorrectly assigned")
                    has_pin = bool(re.search(r"[?&]version=SBLGNT(?:&|$|%3B)", url, re.IGNORECASE))
                    if has_pin and obs.get("editionPinStatus") != "URL_VERSION_PINNED":
                        errors.append(f"provenance: {aid} incorrect URL edition-pin status")
                    if not has_pin and (
                        obs.get("editionPinStatus") != "MULTI_EDITION_DISPLAY_REQUIRES_RECHECK"
                        or aid not in {
                            "ATT-BASE-SABAOTH-05",
                            "ATT-BASE-SABAOTH-06",
                            "ATT-BASE-ABBA-03",
                        }
                    ):
                        errors.append(f"provenance: {aid} unpinned Greek edition not explicitly review-held")
                if edition_id == ED_LXX:
                    match = [value for key, value in PUBLISHER_LXX.items() if key in url]
                    if len(match) != 1 or source_id != match[0] or "die-bibel.de" not in url:
                        errors.append(f"provenance: {aid} publisher LXX chapter/edition misattributed")
                if edition_id == ED_THG:
                    if source_id != "SRC-THGNT-LUKE" or "Luke" not in url:
                        errors.append(f"provenance: {aid} THGNT Luke1 provenance incorrect")
                    if aid != "ATT-EXT-KYRIOS-HO-THEOS-01" or (
                        obs.get("editionPinStatus") != "MULTI_EDITION_DISPLAY_REQUIRES_RECHECK"
                    ):
                        errors.append(f"provenance: {aid} THGNT multiedition display needs explicit edition review HOLD")
    if num != 105 or len(seen) != 105:
        errors.append(f"provenance: all 105 current original-language attestations must be uniquely linked, not {num}/{len(seen)}")

    claim_rows = claims.get("records", [])
    if not isinstance(claim_rows, list):
        return errors + ["provenance: claim record list missing"]
    claim_map = {c.get("claimId"): c for c in claim_rows if isinstance(c, dict)}
    if set(claim_map) != CORE_CLAIMS or len(claim_rows) != len(CORE_CLAIMS):
        errors.append("provenance: ten curated stable claims missing or duplicate")
    for cid, claim in claim_map.items():
        if not isinstance(claim, dict):
            errors.append(f"provenance: malformed claim {cid}")
            continue
        refs = claim.get("attestationIds", [])
        sources_refs = claim.get("sourceIds", [])
        if not isinstance(refs, list) or not refs or len(refs) != len(set(refs)):
            errors.append(f"provenance: claim {cid} missing or duplicate text references")
            continue
        if not isinstance(sources_refs, list) or not sources_refs:
            errors.append(f"provenance: claim {cid} lacking scholarly bibliography")
            continue
        if set(refs) != CLAIM_REQUIRED_ATTESTATIONS.get(cid, set()):
            errors.append(f"provenance: claim {cid} lost its independently reviewed text witnesses")
        if any(r not in att_by_id for r in refs):
            errors.append(f"provenance: claim {cid} cites orphaned attestation")
        if any(r not in source_map for r in sources_refs):
            errors.append(f"provenance: claim {cid} cites orphaned source")
        if not set(refs).difference(att_by_id):
            required_sources = {att_by_id[r]["sourceId"] for r in refs}
            if not required_sources.issubset(set(sources_refs)):
                errors.append(f"provenance: claim {cid} lost mandatory direct textual sources")
        if (claim.get("criticalWitnessStatus") != "NOT_COLLATED"
            or claim.get("editorialState") != "RESEARCH_HOLD"
            or claim.get("publicationState") != "BLOCKED"):
            errors.append(f"provenance: claim {cid} falsely authorized for Product")
        if not str(claim.get("statement", "")).strip():
            errors.append(f"provenance: claim {cid} lacks factual language")
    return errors


def main() -> int:
    try:
        load = lambda path: json.loads(path.read_text(encoding="utf-8"))
        problems = validate_provenance(
            load(BASELINE_PATH), load(EXTENSION_PATH), load(SOURCE_PATH),
            load(EDITIONS_PATH), load(CLAIMS_PATH)
        )
    except (OSError, ValueError, TypeError) as exc:
        print(f"FAIL: provenance could not be loaded: {exc}", file=sys.stderr)
        return 1
    if problems:
        for p in problems:
            print("FAIL: " + p, file=sys.stderr)
        return 1
    print("PASS: all 105 immutable evidence IDs linked to 4 text editions and source records; "
          "10 curated claim IDs have non-orphan, HOLD-guarded evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
