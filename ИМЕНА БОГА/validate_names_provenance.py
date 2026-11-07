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
from urllib.parse import parse_qs, urlsplit

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

# Four publisher-edition URLs were verified as single-version displays.
# These exact anchors protect against edition drift and wrong-verse substitutions.
# This is NOT a manuscript collation or independent scholarship review.
PINNED_GREEK_SOURCE_URLS = {
    "ATT-BASE-SABAOTH-05": "https://www.biblegateway.com/passage/?search=James+5%3A1-11&version=SBLGNT",
    "ATT-BASE-SABAOTH-06": "https://www.biblegateway.com/passage/?search=Romans+9%3A14-29&version=SBLGNT",
    "ATT-BASE-ABBA-03": "https://www.biblegateway.com/passage/?search=Galatians+4%3A4-7&version=SBLGNT",
    "ATT-EXT-KYRIOS-HO-THEOS-01": "https://www.biblegateway.com/passage/?search=Luke+1%3A30-33&version=THGNT",
    "ATT-BASE-IMMANUEL-05": "https://www.biblegateway.com/passage/?search=Matthew+1%3A23&version=SBLGNT",
}


def pinned_bible_gateway_passage(url: object, version: str, verse: object) -> bool:
    """Verify HTTPS host, exactly one edition, and coverage of the recorded verse.

    No network request is made here. The original publisher display is manually
    checked and its URL then locked into the evidence contract.
    """
    if not isinstance(url, str) or not isinstance(verse, str):
        return False
    try:
        page = urlsplit(url)
        if (page.scheme != "https" or page.hostname != "www.biblegateway.com"
            or page.path != "/passage/" or page.username or page.password
            or page.port is not None or page.fragment):
            return False
        values = parse_qs(page.query, keep_blank_values=True)
    except ValueError:
        return False
    if (values.get("version") != [version]
        or len(values.get("search", [])) != 1
        or any(k not in {"version", "search"} for k in values)):
        return False
    required = re.fullmatch(r"(.+?)\s+(\d+):(\d+)", verse)
    location = re.fullmatch(r"(.+?)\s+(\d+)(?::(\d+)(?:-(\d+))?)?", values["search"][0])
    if required is None or location is None:
        return False
    book, chapter, number = required.group(1).casefold(), int(required.group(2)), int(required.group(3))
    if book != location.group(1).casefold() or chapter != int(location.group(2)):
        return False
    start, end = location.group(3), location.group(4)
    return start is None or (int(start) <= number <= int(end or start))


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
# The ten original research seeds and four new edition-pinned seeds are required
# minima, not a ceiling. These are digitally evidenced, not scholarly approved.
NEW_GREEK_SOURCE_CLAIMS = {
    "CLM-JAS5-4-SABAOTH-GENITIVE",
    "CLM-ROM9-29-SABAOTH-ISAIAH",
    "CLM-GAL4-6-ABBA-SPIRIT",
    "CLM-LUK1-32-GABRIEL-AGENT",
}
# The Exodus 3 referent/address correction is an independently inspectable
# semantic boundary, rather than a copied assertion from a static snapshot.
REQUIRED_EHYEH_ROLE_CLAIM = "CLM-EX3-EHYEH-DIVINE-REFERENT"
REQUIRED_EHYEH_IDS = {
    "ATT-BASE-EHYEH-01", "ATT-BASE-EHYEH-02", "ATT-BASE-EHYEH-03"
}
REQUIRED_PROPHETIC_NAMING_CLAIMS = {
    "CLM-JER23-6-DAVIDIC-ROYAL-NAME",
    "CLM-JER33-16-JERUSALEM-CITY-NAME",
    "CLM-EZ48-35-CITY-NAMING",
}
REQUIRED_ROCK_CLAIMS = {
    "CLM-DEUT32-ROCK-DIVINE-METAPHOR",
    "CLM-DEUT32-31-ROCK-CONTRAST",
    "CLM-DEUT32-37-FOREIGN-REFUGE",
}
# The first group may contain YHWH, the second contains TWO different
# referents, and the third is a polemic against foreign gods. Never certify
# a duplicated but semantically corrupted primary/contract reading.
ROCK_REFERENT_CONTROLS = {
    "ATT-BASE-TSUR-01": ("TRUE_GOD", True),
    "ATT-BASE-TSUR-02": ("TRUE_GOD", True),
    "ATT-BASE-TSUR-03": ("MIXED_TRUE_GOD_AND_OTHER_ROCK", None),
    "ATT-BASE-TSUR-04": ("FALSE_OBJECT_OF_REFUGE", False),
    "ATT-BASE-TSUR-05": ("TRUE_GOD", True),
}
REQUIRED_IMMANUEL_CLAIMS = {
    "CLM-ISA7-14-CHILD-NAMING",
    "CLM-ISA7-14-LXX-NAMING-VERB",
    "CLM-ISA8-8-IMMANUEL-ADDRESS",
    "CLM-ISA8-10-DIVINE-PRESENCE",
    "CLM-MATT1-23-IMMANUEL-GLOSS",
}
# Exact locus/role controls, not manuscripts or editorial interpretations.
IMMANUEL_PRINTED_SURFACES = {
    "ATT-BASE-IMMANUEL-01": "עִמָּנוּ אֵל",
    "ATT-BASE-IMMANUEL-02": "Εμμανουηλ",
    "ATT-BASE-IMMANUEL-03": "עִמָּנוּ אֵל",
    "ATT-BASE-IMMANUEL-04": "כִּי עִמָּנוּ אֵל",
    "ATT-BASE-IMMANUEL-05": "Ἐμμανουήλ",
}
IMMANUEL_ROLE_CONTROLS = {
    "ATT-BASE-IMMANUEL-01": ("prophetic_child_naming", "child in prophecy"),
    "ATT-BASE-IMMANUEL-02": ("prophetic_child_naming", "child in Isaiah prophecy"),
    "ATT-BASE-IMMANUEL-03": ("vocative_or_name_allusion", "Immanuel as addressee/allusion (contextual interpretation)"),
    "ATT-BASE-IMMANUEL-04": ("divine_presence_assertion", "God is with us, an assertion not new child-naming"),
    "ATT-BASE-IMMANUEL-05": ("christological_prophetic_quotation", "Jesus identified with prophetic name in quotation"),
}
# The original reviewed seeds are a required minimum, not a cap on future work.
# Additional claims must pass the same foreign-key, editorial and publication gates.
ALLOWED_CLAIM_TYPES = {
    "DIRECT_TEXTUAL_NAMING",
    "NEGATIVE_REFERENT_CONTROL",
    "POSITIVE_REFERENT_CONTROL",
    "NAMED_OBJECT_CONTROL",
    "EDITED_TEXT_DIFFERENCE",
    "NARRATIVE_SPEECH_VS_NAMING",
    "HUMAN_NEGATIVE_CONTROL",
    "CANONICAL_INTERTEXT_BOUNDARY",
    "SPEECH_AGENT_CONTROL",
    "ATTRIBUTED_HISTORICAL_RECONSTRUCTION",
    "MORPHOLOGICAL_CASE_CONTEXT",
    "CITATION_SPEECH_CONTEXT",
    "MIXED_REFERENT_CONTROL",
}
ALLOWED_INTERPRETIVE_SCOPES = {
    "NARROW_LOCUS_CLAIM_NOT_GENERAL_DICTIONARY_CLAIM",
    "AUTHOR_ARGUMENT_NOT_CLOSED",
}
ALLOWED_RELATION_TYPES = {
    "CONTRASTS_REFERENT",
    "CONTRASTS_NAMED_OBJECT",
    "LIMITS_INFERENCE",
    "REQUIRES_INDEPENDENT_ATTESTATION",
    "CONTRASTS_GRAMMATICAL_FORM",
    "SPECIFIES_SPEECH_AGENT",
}
# These four editorial comparisons must not silently disappear in later waves.
REQUIRED_SEMANTIC_RELATIONS = {
    "REL-IS43-EL-REFERENT": (
        "CLM-IS43-10-NEGATED-EL", "CLM-IS43-12-YHWH-EL", "CONTRASTS_REFERENT"
    ),
    "REL-MEMORIAL-PLACE-ALTAR": (
        "CLM-GEN22-14-PLACE-NAME", "CLM-EX17-15-ALTAR-MT-LXX",
        "CONTRASTS_NAMED_OBJECT"
    ),
    "REL-EGO-EIMI-CONTEXT": (
        "CLM-JOHN9-9-HUMAN-EGO-EIMI", "CLM-LXX-EX3-JOHN8-DIFFERENT-CLAUSES",
        "LIMITS_INFERENCE"
    ),
    "REL-YHWH-PRONUNCIATION": (
        "CLM-EX3-15-DIVINE-NAME", "CLM-YHWH-HISTORICAL-PRONUNCIATION",
        "REQUIRES_INDEPENDENT_ATTESTATION"
    ),
    "REL-SABAOTH-CASING-CONTEXT": (
        "CLM-JAS5-4-SABAOTH-GENITIVE", "CLM-ROM9-29-SABAOTH-ISAIAH",
        "CONTRASTS_GRAMMATICAL_FORM"
    ),
    "REL-ABBA-SPIRIT-SPEECH": (
        "CLM-ABBA-THREE-PRAYER-SUBJECTS", "CLM-GAL4-6-ABBA-SPIRIT",
        "SPECIFIES_SPEECH_AGENT"
    ),
    "REL-EX3-SELF-SPEECH-VS-ADDRESSEE": (
        "CLM-EX3-EHYEH-DIVINE-REFERENT",
        "CLM-LXX-EX3-JOHN8-DIFFERENT-CLAUSES",
        "SPECIFIES_SPEECH_AGENT"
    ),
    "REL-JER-ROYAL-CITY-NAMING": (
        "CLM-JER23-6-DAVIDIC-ROYAL-NAME",
        "CLM-JER33-16-JERUSALEM-CITY-NAME",
        "CONTRASTS_NAMED_OBJECT"
    ),
    "REL-JER-EZEK-CITY-NAME-LIMIT": (
        "CLM-JER33-16-JERUSALEM-CITY-NAME",
        "CLM-EZ48-35-CITY-NAMING",
        "LIMITS_INFERENCE"
    ),
    "REL-TSUR-DIVINE-AND-MIXED": (
        "CLM-DEUT32-ROCK-DIVINE-METAPHOR", "CLM-DEUT32-31-ROCK-CONTRAST",
        "CONTRASTS_REFERENT"
    ),
    "REL-TSUR-MIXED-AND-FOREIGN": (
        "CLM-DEUT32-31-ROCK-CONTRAST", "CLM-DEUT32-37-FOREIGN-REFUGE",
        "LIMITS_INFERENCE"
    ),
    "REL-IMMANUEL-MT-LXX-NAME": (
        "CLM-ISA7-14-CHILD-NAMING", "CLM-ISA7-14-LXX-NAMING-VERB",
        "LIMITS_INFERENCE"
    ),
    "REL-IMMANUEL-LXX-MATTHEW-VERB": (
        "CLM-ISA7-14-LXX-NAMING-VERB", "CLM-MATT1-23-IMMANUEL-GLOSS",
        "CONTRASTS_GRAMMATICAL_FORM"
    ),
    "REL-IMMANUEL-ISA8-ADDRESS-ASSERTION": (
        "CLM-ISA8-8-IMMANUEL-ADDRESS", "CLM-ISA8-10-DIVINE-PRESENCE",
        "LIMITS_INFERENCE"
    ),
    "REL-IMMANUEL-MT-MATTHEW-RECEPTION": (
        "CLM-ISA7-14-CHILD-NAMING", "CLM-MATT1-23-IMMANUEL-GLOSS",
        "REQUIRES_INDEPENDENT_ATTESTATION"
    ),
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
    "CLM-JAS5-4-SABAOTH-GENITIVE": {"ATT-BASE-SABAOTH-05"},
    "CLM-ROM9-29-SABAOTH-ISAIAH": {"ATT-BASE-SABAOTH-06"},
    "CLM-GAL4-6-ABBA-SPIRIT": {"ATT-BASE-ABBA-03"},
    "CLM-LUK1-32-GABRIEL-AGENT": {"ATT-EXT-KYRIOS-HO-THEOS-01"},
    "CLM-EX3-EHYEH-DIVINE-REFERENT": {
        "ATT-BASE-EHYEH-01", "ATT-BASE-EHYEH-02", "ATT-BASE-EHYEH-03"
    },
    "CLM-JER23-6-DAVIDIC-ROYAL-NAME": {"ATT-BASE-TSIDKENU-01"},
    "CLM-JER33-16-JERUSALEM-CITY-NAME": {"ATT-BASE-TSIDKENU-02"},
    "CLM-EZ48-35-CITY-NAMING": {"ATT-BASE-SHAMMAH-01"},
    "CLM-DEUT32-ROCK-DIVINE-METAPHOR": {
        "ATT-BASE-TSUR-01", "ATT-BASE-TSUR-02", "ATT-BASE-TSUR-05"
    },
    "CLM-DEUT32-31-ROCK-CONTRAST": {"ATT-BASE-TSUR-03"},
    "CLM-DEUT32-37-FOREIGN-REFUGE": {"ATT-BASE-TSUR-04"},
    "CLM-ISA7-14-CHILD-NAMING": {"ATT-BASE-IMMANUEL-01"},
    "CLM-ISA7-14-LXX-NAMING-VERB": {"ATT-BASE-IMMANUEL-02"},
    "CLM-ISA8-8-IMMANUEL-ADDRESS": {"ATT-BASE-IMMANUEL-03"},
    "CLM-ISA8-10-DIVINE-PRESENCE": {"ATT-BASE-IMMANUEL-04"},
    "CLM-MATT1-23-IMMANUEL-GLOSS": {"ATT-BASE-IMMANUEL-05"},
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
                if aid in IMMANUEL_ROLE_CONTROLS:
                    want_act, want_named = IMMANUEL_ROLE_CONTROLS[aid]
                    if obs.get("surface") != IMMANUEL_PRINTED_SURFACES[aid]:
                        errors.append(f"provenance: {aid} exact printed Immanuel source form changed")
                    if aid == "ATT-BASE-IMMANUEL-01":
                        if (obs.get("originalTerm") != "הָעַלְמָה"
                            or "grammatical dispute" not in str(obs.get("namingVerbAnalysis",""))):
                            errors.append("provenance: Isaiah 7 Hebrew lexeme/naming verb uncertainty erased")
                    if obs.get("speechAct") != want_act or obs.get("namedObject") != want_named:
                        errors.append(f"provenance: {aid} Immanuel speech act/named object conflated")
                    if aid == "ATT-BASE-IMMANUEL-02":
                        if (obs.get("namingVerbForm") != "καλέσεις second person singular"
                            or obs.get("crossEditionRelation") != "MATTHEW_SBLGNT_USES_καλέσουσιν_THIRD_PERSON_PLURAL"):
                            errors.append("provenance: LXX Isaiah καλέσεις vs Matthew καλέσουσιν contrast lost")
                    if aid == "ATT-BASE-IMMANUEL-05":
                        if (obs.get("namingVerbForm") != "καλέσουσιν 3rd plural"
                            or obs.get("translationInVerse") != "Μεθ’ ἡμῶν ὁ θεός"):
                            errors.append("provenance: Matthew Immanuel name grammar/gloss lost")
                if aid in ROCK_REFERENT_CONTROLS:
                    expected_ref, expected_divine = ROCK_REFERENT_CONTROLS[aid]
                    if (obs.get("referentClass") != expected_ref
                        or obs.get("isDivineDesignation") is not expected_divine):
                        errors.append(f"provenance: {aid} Rock referent/isDivineDesignation conflated")
                if aid in REQUIRED_EHYEH_IDS:
                    if obs.get("referent") != "God of Israel, the divine first-person speaker":
                        errors.append(f"provenance: {aid} divine self-reference wrongly attributed to addressee")
                    if obs.get("addressee") != "Moses":
                        errors.append(f"provenance: {aid} missing or incorrect speech addressee")
                    if not str(obs.get("speaker", "")).startswith(("God ", "YHWH ")):
                        errors.append(f"provenance: {aid} divine first-person speaker changed")
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
                    if (obs.get("editionPinStatus") != "URL_VERSION_PINNED"
                        or not pinned_bible_gateway_passage(url, "SBLGNT", obs.get("verse"))):
                        errors.append(f"provenance: {aid} unpinned Greek edition or wrong SBLGNT verse")
                    expected_url = PINNED_GREEK_SOURCE_URLS.get(aid)
                    if expected_url is not None and url != expected_url:
                        errors.append(f"provenance: {aid} verified pinned Greek passage URL changed")
                if edition_id == ED_LXX:
                    match = [value for key, value in PUBLISHER_LXX.items() if key in url]
                    if len(match) != 1 or source_id != match[0] or "die-bibel.de" not in url:
                        errors.append(f"provenance: {aid} publisher LXX chapter/edition misattributed")
                if edition_id == ED_THG:
                    if source_id != "SRC-THGNT-LUKE" or aid != "ATT-EXT-KYRIOS-HO-THEOS-01":
                        errors.append(f"provenance: {aid} THGNT source or locus attribution invalid")
                    if (obs.get("editionPinStatus") != "URL_VERSION_PINNED"
                        or not pinned_bible_gateway_passage(url, "THGNT", obs.get("verse"))):
                        errors.append(f"provenance: {aid} THGNT multiedition display or wrong verse")
                    if url != PINNED_GREEK_SOURCE_URLS["ATT-EXT-KYRIOS-HO-THEOS-01"]:
                        errors.append(f"provenance: {aid} verified pinned THGNT passage URL changed")
    if num != 105 or len(seen) != 105:
        errors.append(f"provenance: all 105 current original-language attestations must be uniquely linked, not {num}/{len(seen)}")

    claim_rows = claims.get("records", [])
    if not isinstance(claim_rows, list):
        return errors + ["provenance: claim record list missing"]
    claim_map: dict[str, dict] = {}
    for idx, claim in enumerate(claim_rows):
        cid = claim.get("claimId") if isinstance(claim, dict) else None
        if not isinstance(cid, str) or not re.fullmatch(r"CLM-[A-Z0-9]+(?:-[A-Z0-9]+)*", cid):
            errors.append(f"provenance: malformed claim ID or record at index {idx}")
            continue
        if cid in claim_map:
            errors.append(f"provenance: duplicate claim ID {cid}")
            continue
        claim_map[cid] = claim
    if not CORE_CLAIMS.issubset(claim_map):
        errors.append("provenance: one or more original curated claim seeds missing")
    if not NEW_GREEK_SOURCE_CLAIMS.issubset(claim_map):
        errors.append("provenance: one or more Greek source-pinned claim seeds missing")
    if REQUIRED_EHYEH_ROLE_CLAIM not in claim_map:
        errors.append("provenance: Exodus 3 divine referent claim missing")
    if not REQUIRED_PROPHETIC_NAMING_CLAIMS.issubset(claim_map):
        errors.append("provenance: required prophetic royal/city claim boundary missing")
    if not REQUIRED_ROCK_CLAIMS.issubset(claim_map):
        errors.append("provenance: required Rock contrast claim boundary missing")
    if not REQUIRED_IMMANUEL_CLAIMS.issubset(claim_map):
        errors.append("provenance: required Immanuel textual role claims missing")
    rock_statement = claim_map.get("CLM-DEUT32-31-ROCK-CONTRAST", {}).get("statement","")
    if not isinstance(rock_statement, str) or "32:30" not in rock_statement:
        errors.append("provenance: Deuteronomy 32:30 pronoun antecedent caution lost")
    for cid, claim in claim_map.items():
        if not isinstance(claim, dict):
            errors.append(f"provenance: malformed claim {cid}")
            continue
        refs = claim.get("attestationIds", [])
        sources_refs = claim.get("sourceIds", [])
        if (not isinstance(refs, list) or not refs
            or any(not isinstance(ref, str) for ref in refs)
            or len(refs) != len(set(refs))):
            errors.append(f"provenance: claim {cid} missing, non-string or duplicate text references")
            continue
        if (not isinstance(sources_refs, list) or not sources_refs
            or any(not isinstance(s, str) for s in sources_refs)
            or len(sources_refs) != len(set(sources_refs))):
            errors.append(f"provenance: claim {cid} lacking unique source references")
            continue
        expected = CLAIM_REQUIRED_ATTESTATIONS.get(cid)
        if expected is not None and set(refs) != expected:
            errors.append(f"provenance: claim {cid} lost its independently reviewed text witnesses")
        if claim.get("claimType") not in ALLOWED_CLAIM_TYPES:
            errors.append(f"provenance: claim {cid} has untyped editorial assertion")
        if claim.get("interpretiveScope") not in ALLOWED_INTERPRETIVE_SCOPES:
            errors.append(f"provenance: claim {cid} has unbounded interpretation")
        if claim.get("evidenceTier") != "DIGITAL_VERSE_SURFACE_AND_ATTRIBUTED_ARGUMENT":
            errors.append(f"provenance: claim {cid} overstates its evidence tier")
        needs = claim.get("reviewNeeded")
        if not isinstance(needs, list) or not needs or any(not isinstance(n, str) or not n.strip() for n in needs):
            errors.append(f"provenance: claim {cid} lacks pending independent review tasks")
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
        if not isinstance(claim.get("statement"), str) or not claim["statement"].strip():
            errors.append(f"provenance: claim {cid} lacks factual language")

    relation_rows = claims.get("semanticRelations")
    if not isinstance(relation_rows, list):
        return errors + ["provenance: typed claim relations missing"]
    relation_ids: set[str] = set()
    relation_map: dict[str, tuple[str, str, str]] = {}
    for idx, relation in enumerate(relation_rows):
        if not isinstance(relation, dict):
            errors.append(f"provenance: malformed semantic relation at index {idx}")
            continue
        rid, src, dst, kind = (
            relation.get("relationId"), relation.get("fromClaimId"),
            relation.get("toClaimId"), relation.get("relationType")
        )
        if not isinstance(rid, str) or not re.fullmatch(r"REL-[A-Z0-9]+(?:-[A-Z0-9]+)*", rid):
            errors.append(f"provenance: invalid semantic relation ID at index {idx}")
            continue
        if rid in relation_ids:
            errors.append(f"provenance: duplicate semantic relation ID {rid}")
            continue
        relation_ids.add(rid)
        if (not isinstance(src, str) or not isinstance(dst, str)
            or src not in claim_map or dst not in claim_map or src == dst):
            errors.append(f"provenance: {rid} orphaned or self-referential claim edge")
            continue
        if kind not in ALLOWED_RELATION_TYPES:
            errors.append(f"provenance: {rid} unknown semantic relation type")
            continue
        if relation.get("publicationState") != "BLOCKED":
            errors.append(f"provenance: {rid} unlawfully promoted relationship")
        if not isinstance(relation.get("rationale"), str) or not relation["rationale"].strip():
            errors.append(f"provenance: {rid} lacks evidence-bounded explanation")
        relation_map[rid] = (src, dst, kind)
    for rid, expected in REQUIRED_SEMANTIC_RELATIONS.items():
        if relation_map.get(rid) != expected:
            errors.append(f"provenance: required semantic boundary {rid} missing or modified")
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
    print("PASS: 105 attestation IDs / 4 editions; 26 provisional claims, "
          "15 typed relations, 5 Immanuel role/edition guards and publication HOLD gates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
