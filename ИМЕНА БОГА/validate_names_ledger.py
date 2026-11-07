#!/usr/bin/env python3
"""Read-only, fail-closed structural checks for Names of God RESEARCH ledger.

This checks data contracts, NOT the accuracy of Hebrew/Greek, critical editions,
external URLs, licenses or publication approval. It must never modify files.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

LEDGER = Path(__file__).resolve().parent / "data" / "names_ledger_v1.json"
EXTENSION = Path(__file__).resolve().parent / "data" / "names_extension_ledger_v1.json"
SOURCES = Path(__file__).resolve().parent / "data" / "source_access_register_v1.json"
ATTESTATION_CONTRACT = Path(__file__).resolve().parent / "data" / "attestation_contract_v1.json"
ALLOWED_CLASSES = {"A1", "A2", "A3", "B1", "C", "D"}
ALLOWED_ACCESS = {"FULL_OBJECT_VERIFIED", "PARTIAL_OBJECT", "CATALOG_ONLY", "LINK_ONLY", "NOT_ACQUIRED"}
ALLOWED_LOCATOR = {"EXACT_LOCATOR_VERIFIED", "COARSE_LOCATOR_ONLY", "LOCATOR_MISSING"}
ALLOWED_RIGHTS = {"PUBLICATION_ELIGIBLE", "STORAGE_ONLY", "PRIVATE_STUDY_ONLY", "PERMISSION_REQUIRED", "RIGHTS_UNKNOWN"}
ALLOWED_PUBLICATION = {"PROMOTE", "REFERENCE", "SUPERSEDED", "BLOCKED"}
ALLOWED_HOLDS = {"EVIDENCE_HOLD", "LOCATOR_HOLD", "ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"}
ALLOWED_LANGUAGES = {"hebrew", "greek", "aramaic", "aramaic_transliterated_in_greek", "hebrew_and_greek"}
EXPECTED_TYPES = {
    "yhwh": "personal_divine_name",
    "yireh": "place_name",
    "nissi": "altar_name",
    "shalom": "altar_name",
    "shammah": "city_name",
    "el-bethel": "place_name",
    "rapha": "predication_about_yhwh",
    "ro-i": "predication_about_yhwh",
    "mekoddishkem": "predication_about_yhwh",
    "tsidkenu": "symbolic_royal_and_city_name",
}
HEBREW = re.compile(r"[\u0590-\u05ff]")
GREEK = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff]")
URL = re.compile(r"^https://[^\s]+$")


def unicode_surface_issues(label: str, form: str) -> list[str]:
    """Reject invisible format-controls and non-NFC original-script surface forms."""
    problems: list[str] = []
    if unicodedata.normalize("NFC", form) != form:
        problems.append(f"{label}: original-script text must be NFC-normalized")
    if any(unicodedata.category(char) == "Cf" for char in form):
        problems.append(f"{label}: invisible Unicode format/bidi control in text surface")
    return problems


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Ledger must be a JSON object"]
    if data.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if data.get("corpusId") != "NAMES_OF_GOD":
        errors.append("unexpected corpusId")
    rows = data.get("records")
    if not isinstance(rows, list):
        return errors + ["records must be a list"]
    if len(rows) != 29:
        errors.append(f"Arena baseline must keep 29 rows, got {len(rows)}; new discoveries belong in a separate extension ledger")
    ids: set[str] = set()
    for i, row in enumerate(rows, start=1):
        prefix = f"records[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix}: expected object")
            continue
        rid = row.get("id")
        if not isinstance(rid, str) or not rid:
            errors.append(f"{prefix}: missing id")
            continue
        prefix = rid
        if rid in ids:
            errors.append(f"{prefix}: duplicate id")
        ids.add(rid)
        if row.get("arenaOrder") != i:
            errors.append(f"{prefix}: arenaOrder must remain {i}")
        for field in ("arenaLabel", "language", "verifiedForm", "verseLocator", "category", "sourceEdition", "sourceUrl"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"{prefix}: {field} must be nonblank")
        form = row.get("verifiedForm", "")
        if isinstance(form, str):
            errors.extend(unicode_surface_issues(prefix, form))
        lang = row.get("language")
        if lang not in ALLOWED_LANGUAGES:
            errors.append(f"{prefix}: unknown language {lang!r}")
        if isinstance(form, str):
            if lang in {"hebrew", "aramaic"} and not HEBREW.search(form):
                errors.append(f"{prefix}: Hebrew/Aramaic text missing Hebrew-script letters")
            if lang in {"greek", "aramaic_transliterated_in_greek"} and not GREEK.search(form):
                errors.append(f"{prefix}: Greek-script form missing Greek letters")
            if lang == "hebrew_and_greek" and not (HEBREW.search(form) and GREEK.search(form)):
                errors.append(f"{prefix}: mixed-script witness must have both Hebrew and Greek")
        if row.get("category") == "personal_divine_name" and rid != "yhwh":
            errors.append(f"{prefix}: cannot silently promote to personal_divine_name")
        expected = EXPECTED_TYPES.get(rid)
        if expected and row.get("category") != expected:
            errors.append(f"{prefix}: referent/syntax regression; expected category {expected}")
        for field, allowed in (
            ("evidenceClass", ALLOWED_CLASSES), ("accessState", ALLOWED_ACCESS),
            ("locatorState", ALLOWED_LOCATOR), ("rightsState", ALLOWED_RIGHTS),
            ("publicationState", ALLOWED_PUBLICATION),
        ):
            if row.get(field) not in allowed:
                errors.append(f"{prefix}: invalid {field}")
        holds = row.get("holds")
        if not isinstance(holds, list) or any(h not in ALLOWED_HOLDS for h in holds):
            errors.append(f"{prefix}: invalid holds")
            holds = []
        if row.get("publicationState") != "BLOCKED" or "PUBLICATION_HOLD" not in holds:
            errors.append(f"{prefix}: publication unblocked without separate approval")
        if row.get("criticalEditionStatus") != "NOT_COLLATED":
            errors.append(f"{prefix}: critical collation state changed; research review required")
        if row.get("claimScope") != "VERIFIED_DIGITAL_SURFACE_ONLY":
            errors.append(f"{prefix}: claim scope must not be inflated")
        if not URL.match(str(row.get("sourceUrl", ""))):
            errors.append(f"{prefix}: sourceUrl must be explicit https URL")
        if "SEPTUAGINTA_SBL.pdf" in str(row.get("sourceUrl", "")):
            errors.append(f"{prefix}: obsolete unverified LXX PDF locator")
        witnesses = row.get("witnesses", [])
        if not isinstance(witnesses, list):
            errors.append(f"{prefix}: witnesses must be a list")
        else:
            for index, witness in enumerate(witnesses):
                if not isinstance(witness, dict):
                    errors.append(f"{prefix}: witnesses[{index}] must be an object")
                elif not URL.match(str(witness.get("sourceUrl", ""))):
                    errors.append(f"{prefix}: witnesses[{index}] has no explicit https source URL")
        if rid == "tsidkenu" and (not isinstance(witnesses, list) or len(witnesses) < 3):
            errors.append(f"{prefix}: must retain both MT referents and Old Greek absence marker")
        if rid == "immanuel" and (not isinstance(witnesses, list) or len(witnesses) < 2):
            errors.append(f"{prefix}: must retain both Isaiah Hebrew and Matthew Greek witnesses")

    # The Russian transcription "Рои" obscures different Hebrew consonantal roots.
    index = {row.get("id"): row for row in rows if isinstance(row, dict)}
    roi_seeing = index.get("el-roi", {})
    roi_shepherd = index.get("ro-i", {})
    if roi_seeing.get("lexicalRoot") != "ראה" or roi_shepherd.get("lexicalRoot") != "רעה":
        errors.append("lexical collision: El-Roi seeing and YHWH-ro-i shepherding must remain distinct roots")
    if roi_seeing.get("consonantalForm") != "אל ראי" or roi_shepherd.get("consonantalForm") != "יהוה רעי":
        errors.append("lexical collision: consonantal spellings must preserve א vs ע")
    if not roi_seeing.get("transliterationCollisionGroup") or roi_seeing.get("transliterationCollisionGroup") != roi_shepherd.get("transliterationCollisionGroup"):
        errors.append("lexical collision group must be preserved")
    yireh = index.get("yireh", {})
    morphological = yireh.get("morphologyNote", {})
    if not isinstance(morphological, dict):
        errors.append("Genesis 22:14 morphology note missing")
    elif (morphological.get("verb1"), morphological.get("verb2")) != ("יִרְאֶה", "יֵרָאֶה"):
        errors.append("Genesis 22:14: Qal/Niphal digital forms have been conflated")
    # Genesis 14–35: linked "El" expressions have distinct acts/referents.
    attestations_required = {
        "el-shaddai": {
            "Genesis 17:1": ("YHWH", "divine_self_identification", "God"),
            "Genesis 28:3": ("Isaac", "benediction", "God"),
            "Genesis 35:11": ("God", "divine_self_identification", "God"),
            "Exodus 6:3": ("YHWH", "retrospective_revelation_statement", "God"),
        },
        "el-elyon": {
            "Genesis 14:18": ("narrator", "priesthood_designation", "God"),
            "Genesis 14:19": ("Melchizedek", "blessing", "God"),
            "Genesis 14:20": ("Melchizedek", "doxology", "God"),
            "Genesis 14:22": ("Abram", "oath_invocation", "God"),
        },
        "el-olam": {"Genesis 21:33": ("Abraham", "name_invocation", "God")},
        "el-roi": {"Genesis 16:13": ("Hagar", "divine_name_invocation_and_direct_address", "God")},
        "el-bethel": {"Genesis 35:7": ("Jacob", "place_naming", "place")},
    }
    for rid, expected_occurrences in attestations_required.items():
        observations = index.get(rid, {}).get("attestations", [])
        if not isinstance(observations, list):
            errors.append(f"{rid}: attestations must be a list")
            continue
        occurrences_by_verse = {}
        for occurrence in observations:
            if not isinstance(occurrence, dict):
                errors.append(f"{rid}: invalid occurrence object")
                continue
            verse = occurrence.get("verse")
            if verse in occurrences_by_verse:
                errors.append(f"{rid}: duplicate exact-verse attestation: {verse}")
            occurrences_by_verse[verse] = occurrence
            form = occurrence.get("surface")
            if not isinstance(form, str) or not HEBREW.search(form):
                errors.append(f"{rid}: missing Hebrew-script verse surface")
            else:
                errors.extend(unicode_surface_issues(f"{rid}/{verse}", form))
            if not URL.match(str(occurrence.get("sourceUrl", ""))):
                errors.append(f"{rid}: missing exact-verse source URL")
            if occurrence.get("edition") != "Mechon-Mamre MT digital transcription":
                errors.append(f"{rid}: source edition was changed without review")
            if occurrence.get("checkState") != "DIGITAL_VERSE_SURFACE_CHECKED" or occurrence.get("criticalEditionStatus") != "NOT_COLLATED":
                errors.append(f"{rid}: digital check has been falsely promoted to manuscript collation")
            if occurrence.get("rightsState") != "RIGHTS_UNKNOWN":
                errors.append(f"{rid}: source rights approved without evidence")
        for verse, (speaker, act, obj) in expected_occurrences.items():
            found = occurrences_by_verse.get(verse, {})
            if (found.get("speaker"), found.get("speechAct"), found.get("namedObject")) != (speaker, act, obj):
                errors.append(f"{rid}/{verse}: speaker/speech act/named object regression")
        if not set(expected_occurrences).issubset(occurrences_by_verse):
            errors.append(f"{rid}: mandatory contextual witnesses are missing")
    # The patriarchal counter is corpus-specific, never a global attestation total.
    total = sum(len(index.get(rid, {}).get("attestations", []))
                for rid in attestations_required
                if isinstance(index.get(rid, {}).get("attestations"), list))
    if data.get("auditProtocol", {}).get("patriarchalAttestations", {}).get("totalAttestations") != total:
        errors.append("patriarchal attestation counter drift")
    if total < 11:
        errors.append("core patriarchal attestation set incomplete")
    source_roles = {key: row.get("contextualAssertion", "") for key, row in index.items()}
    for rid in attestations_required:
        if not source_roles.get(rid):
            errors.append(f"{rid}: missing assertion with claim boundary")
    # Exact checked extracts guard prepositions, conjunctions and verse-specific pointing.
    # Separate from manuscript collation; changing an edition requires explicit review.
    expected_surfaces = {
        "el-shaddai": {
            "Genesis 17:1": "אֵל שַׁדַּי",
            "Genesis 28:3": "וְאֵל שַׁדַּי",
            "Genesis 35:11": "אֵל שַׁדַּי",
            "Exodus 6:3": "בְּאֵל שַׁדָּי",
        },
        "el-elyon": {
            "Genesis 14:18": "לְאֵל עֶלְיוֹן",
            "Genesis 14:19": "לְאֵל עֶלְיוֹן",
            "Genesis 14:20": "אֵל עֶלְיוֹן",
            "Genesis 14:22": "יְהוָה אֵל עֶלְיוֹן",
        },
        "el-olam": {"Genesis 21:33": "יְהוָה אֵל עוֹלָם"},
        "el-roi": {"Genesis 16:13": "אַתָּה אֵל רֳאִי"},
        "el-bethel": {"Genesis 35:7": "אֵל בֵּית-אֵל"},
    }
    for rid, by_verse in expected_surfaces.items():
        occurrences = index.get(rid, {}).get("attestations")
        if not isinstance(occurrences, list):
            occurrences = []
        for verse, exact in by_verse.items():
            observation = next((x for x in occurrences
                                if isinstance(x, dict) and x.get("verse") == verse), {})
            if observation.get("surface") != exact:
                errors.append(f"{rid}/{verse}: exact digitally checked Hebrew surface changed")

    counts = data.get("counts", {})
    if not isinstance(counts, dict):
        errors.append("counts must be object")
    else:
        count = sum(r.get("textCheck") == "EXACT_VERSE_CHECKED_IN_NAMED_DIGITAL_EDITION" for r in rows if isinstance(r, dict))
        if counts.get("arenaCandidateCount") != len(rows) or counts.get("exactDigitalVerseChecks") != count:
            errors.append("counts: machine status totals do not match records")
        if counts.get("criticalEditionCollationsCompleted") != 0 or counts.get("publicationEligible") != 0:
            errors.append("counts: critical/publication status must remain zero absent evidence")
    if "derived_from_yhwh" in json.dumps(data, ensure_ascii=False):
        errors.append("derived_from_yhwh forbidden in data model without review")
    return errors


def validate_extension(extension: dict, baseline: dict) -> list[str]:
    """Validate separately researched candidate expressions without changing Arena IDs.

    Structural checks only: not textual, lexical, legal, or doctrinal certification.
    """
    errors: list[str] = []
    if not isinstance(extension, dict) or extension.get("schemaVersion") != 1:
        return ["extension: expected schemaVersion 1 JSON object"]
    if extension.get("corpusId") != "NAMES_OF_GOD_EXTENSION":
        errors.append("extension: unexpected corpusId")
    rows = extension.get("records")
    if not isinstance(rows, list) or not rows:
        return errors + ["extension: nonempty records list is required"]
    baseline_ids = {x.get("id") for x in baseline.get("records", []) if isinstance(x, dict)}
    extension_ids: set[str] = set()
    for i, row in enumerate(rows, start=1):
        label = f"extension[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{label}: expected object")
            continue
        rid = row.get("id")
        if not isinstance(rid, str) or not rid:
            errors.append(f"{label}: missing id")
            continue
        if rid in extension_ids or rid in baseline_ids:
            errors.append(f"{label}: duplicate ID across historical/extension ledgers: {rid}")
        extension_ids.add(rid)
        if row.get("ordinal") != i:
            errors.append(f"{label}: ordinal must be {i}")
        for field in ("editorialLabel", "verifiedDigitalForm", "verseLocator",
                      "sourceEdition", "sourceUrl", "category", "editorialCaution"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"{label}: blank {field}")
        form = str(row.get("verifiedDigitalForm", ""))
        errors.extend(unicode_surface_issues(label, form))
        lang = row.get("language")
        if lang not in {"hebrew", "aramaic", "greek"}:
            errors.append(f"{label}: language must be a single original-language layer")
        if lang in {"hebrew", "aramaic"} and not HEBREW.search(form):
            errors.append(f"{label}: original Hebrew/Aramaic script absent")
        if lang == "greek" and not GREEK.search(form):
            errors.append(f"{label}: Greek script absent")
        if not URL.match(str(row.get("sourceUrl", ""))):
            errors.append(f"{label}: sourceUrl must be explicit HTTPS")
        if row.get("category") == "personal_divine_name":
            errors.append(f"{label}: candidate cannot silently claim a new personal name")
        if row.get("evidenceClass") not in ALLOWED_CLASSES or row.get("rightsState") not in ALLOWED_RIGHTS:
            errors.append(f"{label}: evidence/rights code out of policy")
        if row.get("accessState") not in ALLOWED_ACCESS or row.get("locatorState") not in ALLOWED_LOCATOR:
            errors.append(f"{label}: access/locator code out of policy")
        if row.get("publicationState") != "BLOCKED":
            errors.append(f"{label}: publication must remain BLOCKED pending explicit review")
        holds = row.get("holds", [])
        if not isinstance(holds, list) or not {"PUBLICATION_HOLD", "RIGHTS_HOLD"}.issubset(set(holds)):
            errors.append(f"{label}: mandatory publication and rights holds missing")
        elif any(h not in ALLOWED_HOLDS for h in holds):
            errors.append(f"{label}: unsupported HOLD value")
        if row.get("digitalFormStatus") != "ONE_VERSE_DIGITAL_SURFACE_CHECKED":
            errors.append(f"{label}: digital surface status missing or inflated")
        if row.get("criticalEditionStatus") != "NOT_COLLATED":
            errors.append(f"{label}: unsupported critical edition closure")
        related = row.get("relatedBaselineIds", [])
        if not isinstance(related, list) or not related or any(x not in baseline_ids for x in related):
            errors.append(f"{label}: links must reference existing original Arena IDs")
        if row.get("relationshipType") != "thematic_or_textual_cross_reference_not_etymology":
            errors.append(f"{label}: cross-reference must not invent lexical derivation")
    counts = extension.get("counts", {})
    if not isinstance(counts, dict):
        errors.append("extension counts must be object")
    else:
        if counts.get("candidates") != len(rows):
            errors.append("extension candidate count mismatch")
        if counts.get("promotedToBaseline") != 0 or counts.get("publicationEligible") != 0 or counts.get("criticalCollations") != 0:
            errors.append("extension: unreviewed promotion, publication, or critical collation")
    return errors


EXPECTED_SOURCE_ROLES = {
    "SRC-MT-MECHON": "DIGITAL_TEXT_SURFACE_ONLY",
    "SRC-VANWOLDE-2021": "ATTRIBUTED_SECONDARY_EXEGESIS",
    "SRC-ROESEL-2007": "ATTRIBUTED_ABSTRACT_HYPOTHESIS",
    "SRC-SHAW-2002": "CATALOGUE_ABSTRACT_ONLY",
    "SRC-LEE-8HEV": "CATALOGUE_ABSTRACT_ONLY",
    "SRC-GREEVER-2020": "RECEPTION_TYPOLOGY_ONLY",
    "SRC-CALVIN-EXODUS": "HISTORICAL_INTERPRETATION_IN_TRANSLATION",
    "SRC-NET-EXO6": "ATTRIBUTED_TRANSLATION_NOTES",
    "SRC-THGNT-LUKE": "GREEK_TEXT_SURFACE_ONLY",
    "SRC-RASHI-EXO6": "HISTORICAL_JEWISH_COMMENTARY",
    "SRC-NET-GEN14": "ATTRIBUTED_TRANSLATION_NOTES",
    "SRC-CARGILL-2019": "ATTRIBUTED_HISTORICAL_CRITICAL_HYPOTHESIS_ABSTRACT",
    "SRC-SBL-REVELATION": "GREEK_TEXT_SURFACE_ONLY",
    "SRC-TR1550-REV18": "HISTORIC_PRINTED_EDITION_SURFACE",
    "SRC-THGNT-REV216": "GREEK_TEXT_SURFACE_ONLY",
    "SRC-DANIEL-ARAMAIC": "ARAMAIC_TEXT_SURFACE_ONLY",
    "SRC-SBL-INTRO": "EDITION_METHOD_NOT_MANUSCRIPT_APPARATUS",
    "SRC-SBLGNT-CCBY-LICENSE": "PUBLISHER_LICENSE_TEXT_ONLY",
    "SRC-JUDISCH-DAN7-ARAMAIC": "ATTRIBUTED_B1_ARAMAIC_GRAMMAR",
    "SRC-RAHLFS-ISAIAH": "PUBLISHER_EDITED_GREEK_LXX_SURFACE",
    "SRC-ORTHODOX-ISAIAH9": "UNPINNED_ORTHODOX_GREEK_WEB_SURFACE",
    "SRC-RASHI-ISAIAH9": "ATTRIBUTED_JEWISH_EXEGETICAL_RECEPTION",
    "SRC-RADAK-ISAIAH9": "ATTRIBUTED_JEWISH_EXEGETICAL_RECEPTION",
    "SRC-NET-ISAIAH7": "ATTRIBUTED_TRANSLATION_NOTES",
    "SRC-LEUCHTER-JER33": "ATTRIBUTED_ACADEMIC_TEXTUAL_CRITICISM_ABSTRACT",
    "SRC-RASHI-EZEK48": "ATTRIBUTED_JEWISH_EXEGETICAL_RECEPTION",
    "SRC-SBLGNT-NT-SABAOTH": "GREEK_NT_SEMITIC_TRANSLITERATION_WITNESS",
    "SRC-SUCHARD-ELOHIM-2025": "ATTRIBUTED_SECONDARY_SEMITIC_MORPHOLOGY_HYPOTHESIS",
    "SRC-CAMBRIDGE-GOD-PRONOUNS": "ATTRIBUTED_SECONDARY_GRAMMAR_AND_THEOLOGY",
}


def validate_source_access(sources: dict) -> list[str]:
    """Structural provenance/rights gate; never certifies actual content or licenses."""
    errors: list[str] = []
    if not isinstance(sources, dict) or sources.get("schemaVersion") != 1:
        return ["source register must be a schemaVersion=1 JSON object"]
    if sources.get("corpusId") != "NAMES_OF_GOD_SOURCE_ACCESS":
        errors.append("sources: wrong corpusId")
    rows = sources.get("records")
    if not isinstance(rows, list):
        return errors + ["sources: records must be list"]
    ids: set[str] = set()
    for idx, source in enumerate(rows, start=1):
        prefix = f"source[{idx}]"
        if not isinstance(source, dict):
            errors.append(f"{prefix}: not an object")
            continue
        rid = source.get("id", "")
        if not rid or rid in ids:
            errors.append(f"{prefix}: missing or duplicate id")
        ids.add(rid)
        if rid not in EXPECTED_SOURCE_ROLES:
            errors.append(f"{prefix}: unreviewed source id {rid}")
        if source.get("sourceRole") != EXPECTED_SOURCE_ROLES.get(rid):
            errors.append(f"{prefix}: source relevance/role changed without research review")
        for name in ("title", "creator", "url", "objectType",
                     "supportedUse", "forbiddenUse", "sourceObjectState"):
            if not isinstance(source.get(name), str) or not source[name].strip():
                errors.append(f"{prefix}: {name} empty")
        if not URL.match(str(source.get("url", ""))):
            errors.append(f"{prefix}: invalid https source URL")
        for name, accepted in (
            ("evidenceClass", ALLOWED_CLASSES),
            ("accessState", ALLOWED_ACCESS),
            ("locatorState", ALLOWED_LOCATOR),
            ("rightsState", ALLOWED_RIGHTS),
            ("publicationState", ALLOWED_PUBLICATION),
        ):
            if source.get(name) not in accepted:
                errors.append(f"{prefix}: invalid {name}")
        if source.get("publicationState") != "BLOCKED":
            errors.append(f"{prefix}: publication not authorized")
        holds = source.get("holds", [])
        if not isinstance(holds, list) or "PUBLICATION_HOLD" not in holds:
            errors.append(f"{prefix}: mandatory PUBLICATION_HOLD absent")
        elif any(h not in ALLOWED_HOLDS for h in holds):
            errors.append(f"{prefix}: unknown HOLD token")
        if source.get("criticalEditionCollated") is not False:
            errors.append(f"{prefix}: falsely claims edition collation")
        if source.get("rightsState") == "PUBLICATION_ELIGIBLE" and rid not in {"SRC-VANWOLDE-2021", "SRC-TR1550-REV18", "SRC-SBLGNT-CCBY-LICENSE", "SRC-CAMBRIDGE-GOD-PRONOUNS"}:
            errors.append(f"{prefix}: evidence of a source-level license missing")
        if rid == "SRC-TR1550-REV18":
            if source.get("rightsState") != "PUBLICATION_ELIGIBLE" or "Public Domain" not in str(source.get("license", "")):
                errors.append(f"{prefix}: source-specific public-domain TR1550 status changed")
            if source.get("publicationState") != "BLOCKED":
                errors.append(f"{prefix}: public domain is not permission to publish unreviewed interpretations")
        if rid in {"SRC-THGNT-REV216", "SRC-THGNT-LUKE"} and source.get("rightsState") != "PERMISSION_REQUIRED":
            errors.append(f"{prefix}: restricted THGNT rights changed")
        if rid == "SRC-DANIEL-ARAMAIC" and (source.get("sourceRole") != "ARAMAIC_TEXT_SURFACE_ONLY"
            or source.get("accessState") != "PARTIAL_OBJECT"):
            errors.append(f"{prefix}: Aramaic text cannot be promoted to fully collated Hebrew or manuscript")
        if rid == "SRC-SBL-INTRO" and "manuscript collation" not in str(source.get("forbiddenUse", "")).lower():
            errors.append(f"{prefix}: SBLGNT introduction must remain non-manuscript provenance")
        if rid == "SRC-CAMBRIDGE-GOD-PRONOUNS":
            if (source.get("creator") != "Nicholas Adams"
                or source.get("year") != 2024
                or source.get("rightsState") != "PUBLICATION_ELIGIBLE"
                or "CC BY 4.0" not in str(source.get("license", ""))
                or source.get("licenseScope") != "CAMBRIDGE_ARTICLE_ONLY_NOT_BIBLICAL_TRANSLATIONS"):
                errors.append(f"{prefix}: Nicholas Adams Cambridge CC BY article-only provenance lost")
        if rid == "SRC-SBLGNT-NT-SABAOTH":
            if (source.get("rightsState") != "RIGHTS_UNKNOWN"
                or source.get("sourceRole") != "GREEK_NT_SEMITIC_TRANSLITERATION_WITNESS"):
                errors.append(f"{prefix}: NT Sabaoth display rights/Greek transliteration role lost")
        if rid == "SRC-SUCHARD-ELOHIM-2025":
            if (source.get("evidenceClass") != "B1" or
                source.get("rightsState") != "PERMISSION_REQUIRED" or
                source.get("year") != 2025):
                errors.append(f"{prefix}: Suchard 2025 hypothesis raised to unchecked primary authority")
        if rid == "SRC-RAHLFS-ISAIAH":
            if (source.get("rightsState") != "PERMISSION_REQUIRED"
                or source.get("accessState") != "PARTIAL_OBJECT"
                or source.get("criticalEditionCollated") is not False):
                errors.append(f"{prefix}: Rahlfs-Hanhart edited digital text cannot be promoted to licensed/collated manuscript")
            if "Rahlfs" not in str(source.get("title","")):
                errors.append(f"{prefix}: Rahlfs editorial edition name lost")
        if rid == "SRC-ORTHODOX-ISAIAH9":
            if source.get("rightsState") != "PERMISSION_REQUIRED" or "unpinned" not in str(source.get("objectType", "")).lower():
                errors.append(f"{prefix}: unpinned Orthodox Greek textual provenance/rights must be retained")
        if rid == "SRC-LEUCHTER-JER33" and (source.get("accessState"), source.get("locatorState")) != ("CATALOG_ONLY", "COARSE_LOCATOR_ONLY"):
            errors.append(f"{prefix}: Leuchter abstract cannot be promoted to directly collated Old Greek witness")
        if rid == "SRC-JUDISCH-DAN7-ARAMAIC":
            if source.get("evidenceClass") != "B1" or source.get("rightsState") != "RIGHTS_UNKNOWN":
                errors.append(f"{prefix}: confessional lexical commentary has wrong rights/evidence class")
            if source.get("primaryLexiconStatus") != "BDB_REFERENCED_BY_AUTHOR_NOT_DIRECTLY_VERIFIED":
                errors.append(f"{prefix}: unpublished primary lexicon verification falsely claimed")
            if source.get("interpretiveTradition") != "Confessional Lutheran":
                errors.append(f"{prefix}: confessional provenance must not be erased")
        if rid == "SRC-SBLGNT-CCBY-LICENSE":
            if (source.get("rightsState") != "PUBLICATION_ELIGIBLE"
                or source.get("evidenceClass") != "A2"
                or source.get("accessState") != "FULL_OBJECT_VERIFIED"
                or "CC BY 4.0" not in str(source.get("license", ""))):
                errors.append(f"{prefix}: official CC BY 4.0 publisher-license evidence lost")
            if source.get("licenseScope") != "GREEK_EDITED_TEXT_ONLY_NOT_HOST_WEBSITE_OR_OTHER_EDITIONS":
                errors.append(f"{prefix}: text-only license boundaries changed")
            if source.get("publicationState") != "BLOCKED":
                errors.append(f"{prefix}: copyright eligibility is not publication approval")
        if rid == "SRC-SBL-REVELATION" and source.get("rightsState") != "RIGHTS_UNKNOWN":
            errors.append(f"{prefix}: publisher license must not be inferred for host website display")
        if rid == "SRC-VANWOLDE-2021":
            if source.get("rightsState") != "PUBLICATION_ELIGIBLE" or "CC BY 4.0" not in str(source.get("license", "")):
                errors.append(f"{prefix}: verified article-specific CC BY license lost")
        if rid in {"SRC-SHAW-2002", "SRC-LEE-8HEV"} and source.get("accessState") != "CATALOG_ONLY":
            errors.append(f"{prefix}: catalogue falsely promoted to full manuscript witness")
        if rid == "SRC-GREEVER-2020" and "יָהּ" not in str(source.get("forbiddenUse", "")):
            errors.append(f"{prefix}: Psalm 68:18 typology cannot prove Yah lexeme")
        if rid == "SRC-CARGILL-2019":
            if source.get("accessState") != "CATALOG_ONLY" or source.get("locatorState") != "COARSE_LOCATOR_ONLY":
                errors.append(f"{prefix}: Cargill chapter abstract cannot be promoted to collated manuscript evidence")
            if "gloss" not in str(source.get("supportedUse", "")):
                errors.append(f"{prefix}: Cargill hypothesis attribution lost")
        if rid == "SRC-NET-GEN14" and source.get("rightsState") != "PERMISSION_REQUIRED":
            errors.append(f"{prefix}: NET Genesis 14 rights gate removed")
        if rid == "SRC-RASHI-EXO6" and source.get("accessState") != "PARTIAL_OBJECT":
            errors.append(f"{prefix}: Rashi online excerpt cannot claim complete original edition")
        if rid == "SRC-THGNT-LUKE" and source.get("rightsState") != "PERMISSION_REQUIRED":
            errors.append(f"{prefix}: THGNT must retain reuse restriction")
    if ids != set(EXPECTED_SOURCE_ROLES):
        errors.append("sources: source-inventory IDs changed")
    counts = sources.get("counts", {})
    if not isinstance(counts, dict) or counts.get("sourceRecords") != len(rows) or counts.get("approvedForProduct") != 0:
        errors.append("sources: count/status mismatch")
    return errors


APOCALYPTIC_BASELINE_SURFACES = {
    "atiq-yomin": {
        "Daniel 7:9": ("עַתִּיק יוֹמִין", "aramaic", "direct_scene_narration"),
        "Daniel 7:13": ("עַתִּיק יוֹמַיָּא", "aramaic", "direct_scene_narration"),
        "Daniel 7:22": ("עַתִּיק יוֹמַיָּא", "aramaic", "direct_scene_narration"),
    },
    "alpha-omega": {
        "Revelation 1:8": ("τὸ Ἄλφα καὶ τὸ Ὦ", "greek", "explicit_speech_attribution_in_verse"),
        "Revelation 21:6": ("τὸ Ἄλφα καὶ τὸ Ὦ", "greek", "narrative_speaker_introduced_in_Revelation_21_5"),
        "Revelation 22:13": ("τὸ Ἄλφα καὶ τὸ Ὦ", "greek", "contextual_inference_with_intervening_angelic_speech"),
    },
    "pantokrator": {
        "Revelation 1:8": ("ὁ παντοκράτωρ", "greek", "explicit_speech_attribution_in_verse"),
        "Revelation 21:22": ("ὁ παντοκράτωρ", "greek", "vision_narration"),
    },
}
APOCALYPTIC_EXTENSION_SURFACES = {
    "ho-on-erchomenos": {
        "Revelation 1:4": "ὁ ὢν καὶ ὁ ἦν καὶ ὁ ἐρχόμενος",
        "Revelation 1:8": "ὁ ὢν καὶ ὁ ἦν καὶ ὁ ἐρχόμενος",
    },
    "arche-telos": {
        "Revelation 21:6": "ἡ ἀρχὴ καὶ τὸ τέλος",
        "Revelation 22:13": "ἡ ἀρχὴ καὶ τὸ τέλος",
    },
}


def validate_apocalyptic(baseline: dict, extension: dict) -> list[str]:
    """Fail closed on digital witness and narrative-attribution regressions.

    This is a pinned, reviewed verse-surface contract, NOT a claim of
    manuscript-critical collation, or endorsement of interpretive speakers.
    """
    errors: list[str] = []
    bmap = {r.get("id"): r for r in baseline.get("records", []) if isinstance(r, dict)}
    emap = {r.get("id"): r for r in extension.get("records", []) if isinstance(r, dict)}
    for rid, expected in APOCALYPTIC_BASELINE_SURFACES.items():
        row = bmap.get(rid, {})
        att = row.get("attestations", [])
        if not isinstance(att, list):
            errors.append(f"{rid}: apocalyptic attestation list missing")
            att = []
        found = {r.get("verse"): r for r in att if isinstance(r, dict)}
        if set(found) != set(expected) or len(att) != len(expected):
            errors.append(f"{rid}: apocalyptic verse set drift")
        for verse, (surface, language, cue) in expected.items():
            o = found.get(verse, {})
            if o.get("surface") != surface or o.get("language") != language:
                errors.append(f"{rid}/{verse}: original-script surface or language changed")
            if o.get("speakerEvidence") != cue:
                errors.append(f"{rid}/{verse}: narrative voice evidence was conflated")
            if not isinstance(o.get("speaker"), str) or not o["speaker"]:
                errors.append(f"{rid}/{verse}: speaker attribution missing")
            if not isinstance(o.get("referent"), str) or not o["referent"]:
                errors.append(f"{rid}/{verse}: referent missing")
            for field, expected_value in (
                ("checkState", "DIGITAL_VERSE_SURFACE_CHECKED"),
                ("criticalEditionStatus", "NOT_COLLATED"),
                ("rightsState", "RIGHTS_UNKNOWN"),
            ):
                if o.get(field) != expected_value:
                    errors.append(f"{rid}/{verse}: unwarranted promotion of {field}")
            if not URL.match(str(o.get("sourceUrl", ""))):
                errors.append(f"{rid}/{verse}: witness source URL invalid")
            if isinstance(o.get("surface"), str):
                errors.extend(unicode_surface_issues(f"{rid}/{verse}", o["surface"]))
        if rid == "atiq-yomin":
            note = row.get("lexicalNote", {})
            if note.get("morphologicalExplanationStatus") != "B1_SECONDARY_PARSE_VERIFIED_LEXICON_PENDING":
                errors.append("Daniel7 Aramaic B1 morphological status inflated or regressed")
            parsing = note.get("parsingEvidence", {})
            if not isinstance(parsing, dict):
                errors.append("Daniel7 Aramaic B1 parsing provenance missing")
            else:
                if (parsing.get("evidenceClass"), parsing.get("accessState")) != ("B1", "PARTIAL_OBJECT"):
                    errors.append("Daniel7 Aramaic grammar erroneously promoted to primary source")
                analyses = parsing.get("analyses", [])
                expected_states = {
                    "Daniel 7:9": ("יוֹמִין", "absolute"),
                    "Daniel 7:13": ("יוֹמַיָּא", "emphatic"),
                    "Daniel 7:22": ("יוֹמַיָּא", "emphatic"),
                }
                mapped = {x.get("verse"): x for x in analyses if isinstance(x, dict)} if isinstance(analyses, list) else {}
                if set(mapped) != set(expected_states):
                    errors.append("Daniel7 B1 grammar verse set must stay 9/13/22")
                for verse, (form, state) in expected_states.items():
                    p = mapped.get(verse, {})
                    if (p.get("form"), p.get("state")) != (form, state):
                        errors.append(f"Daniel7 {verse}: B1 absolute/emphatic plural parsing changed")
                    if p.get("certainty") != "ATTRIBUTED_SECONDARY_GRAMMATICAL_PARSE":
                        errors.append(f"Daniel7 {verse}: secondary grammar overclaimed")
            if "COMING TO" not in str(row.get("referentBoundary", "")):
                errors.append("Daniel7:13 two vision figures no longer distinguished")
    if baseline.get("auditProtocol", {}).get("apocalypticAttestations", {}).get("totalAttestations") != 8:
        errors.append("apocalyptic baseline count must stay 8 unless separately reviewed")
    for rid, expected in APOCALYPTIC_EXTENSION_SURFACES.items():
        row = emap.get(rid, {})
        att = row.get("attestations", [])
        if not isinstance(att, list):
            errors.append(f"{rid}: apocalyptic extension attestation list missing")
            att = []
        found = {r.get("verse"): r for r in att if isinstance(r, dict)}
        if set(found) != set(expected) or len(att) != len(expected):
            errors.append(f"{rid}: apocalyptic extension verse set drift")
        for verse, surface in expected.items():
            o = found.get(verse, {})
            if o.get("surface") != surface or o.get("language") != "greek":
                errors.append(f"{rid}/{verse}: Greek original surface changed")
            if not isinstance(o.get("speakerCue"), str) or not o["speakerCue"]:
                errors.append(f"{rid}/{verse}: speakerCue missing")
            if o.get("edition") != "SBLGNT 2010 via BibleGateway":
                errors.append(f"{rid}/{verse}: edition silently replaced")
            if o.get("checkState") != "DIGITAL_VERSE_SURFACE_CHECKED" or o.get("criticalEditionStatus") != "NOT_COLLATED":
                errors.append(f"{rid}/{verse}: false manuscript approval")
            if o.get("rightsState") != "RIGHTS_UNKNOWN":
                errors.append(f"{rid}/{verse}: source-specific rights silently changed")
            if not URL.match(str(o.get("sourceUrl", ""))):
                errors.append(f"{rid}/{verse}: missing source URL")
            if isinstance(o.get("surface"), str):
                errors.extend(unicode_surface_issues(f"{rid}/{verse}", o["surface"]))
    if extension.get("auditProtocol", {}).get("apocalypticAttestations", {}).get("totalAttestations") != 4:
        errors.append("apocalyptic extension count must stay 4 unless reviewed")
    ao = bmap.get("alpha-omega", {})
    variants = ao.get("printedEditionDiffs", [])
    if not isinstance(variants, list) or len(variants) != 2:
        errors.append("Rev printed-edition contrasts missing: need 1:8 and 21:6")
    else:
        index = {v.get("verse"): v for v in variants if isinstance(v, dict)}
        if set(index) != {"Revelation 1:8", "Revelation 21:6"}:
            errors.append("Rev printed-edition verse attribution changed")
        for verse, reading in index.items():
            if reading.get("claimScope") != "PRINTED_EDITIONS_NOT_MANUSCRIPT_COLLATION":
                errors.append(f"{verse}: printed-edition comparison improperly promoted")
            if not URL.match(str(reading.get("sourceA", ""))) or not URL.match(str(reading.get("sourceB", ""))):
                errors.append(f"{verse}: edition comparison URLs missing")
        r18 = index.get("Revelation 1:8", {})
        if (r18.get("editionA"), r18.get("editionB")) != ("SBLGNT 2010", "Stephanus TR1550"):
            errors.append("Rev1:8 printed editions swapped")
        if "SBLGNT has ὁ θεός, TR1550 does not" != r18.get("variant2"):
            errors.append("Rev1:8 θεός difference lost")
        r216 = index.get("Revelation 21:6", {})
        if (r216.get("editionA"), r216.get("editionB")) != ("SBLGNT 2010", "THGNT 2017"):
            errors.append("Rev21:6 printed editions swapped")
        if "without εἰμι" not in str(r216.get("variant1", "")) and "no explicit εἰμι" not in str(r216.get("variant1", "")):
            errors.append("Rev21:6 εἰμι omission must be explicit")
    return errors


PROPHETIC_NAMING_WITNESSES = {
    "el-gibbor": {
        "Isaiah 9:5 MT (English 9:6)": ("אֵל גִּבּוֹר", "royal_child_naming_formula", "royal child in complex naming sequence", "hebrew"),
        "Isaiah 10:21": ("אֶל-אֵל, גִּבּוֹר", "return_to_God", "God of Israel", "hebrew"),
    },
    "tsidkenu": {
        "Jeremiah 23:6": ("יְהוָה צִדְקֵנוּ", "naming_royal_Davidic_branch", "Davidic king", "hebrew"),
        "Jeremiah 33:16": ("יְהוָה צִדְקֵנוּ", "naming_Jerusalem", "Jerusalem", "hebrew"),
    },
    "shammah": {
        "Ezekiel 48:35": ("יְהוָה שָׁמָּה", "city_naming", "city", "hebrew"),
    },
    "immanuel": {
        "Isaiah 7:14": ("עִמָּנוּ אֵל", "prophetic_child_naming", "child in prophecy", "hebrew"),
        "Isaiah 7:14 LXX Rahlfs-Hanhart": ("Εμμανουηλ", "prophetic_child_naming", "child in Isaiah prophecy", "greek"),
        "Isaiah 8:8": ("עִמָּנוּ אֵל", "vocative_or_name_allusion", "Immanuel as addressee/allusion (contextual interpretation)", "hebrew"),
        "Isaiah 8:10": ("כִּי עִמָּנוּ אֵל", "divine_presence_assertion", "God is with us, an assertion not new child-naming", "hebrew"),
        "Matthew 1:23": ("Ἐμμανουήλ", "christological_prophetic_quotation", "Jesus identified with prophetic name in quotation", "greek"),
    },
}


def validate_prophetic_namings(baseline: dict) -> list[str]:
    """Pin researched naming roles, original-script verse forms, and editorial scope."""
    errors: list[str] = []
    rows = baseline.get("records", [])
    index = {r.get("id"): r for r in rows if isinstance(r, dict)} if isinstance(rows, list) else {}
    expected_total = sum(len(group) for group in PROPHETIC_NAMING_WITNESSES.values())
    if expected_total != 10:
        errors.append("prophetic: unexpected historical naming contract count")
    for rid, expected in PROPHETIC_NAMING_WITNESSES.items():
        row = index.get(rid, {})
        records = row.get("attestations")
        if not isinstance(records, list):
            errors.append(f"prophetic {rid}: attestation list missing")
            records = []
        witnesses = {r.get("verse"):r for r in records if isinstance(r,dict)}
        if len(witnesses) != len(records) or set(witnesses) != set(expected):
            errors.append(f"prophetic {rid}: verse witness set drift or duplicate")
        for verse, (surface, action, obj, lang) in expected.items():
            occ = witnesses.get(verse, {})
            if (occ.get("surface"), occ.get("speechAct"), occ.get("namedObject"), occ.get("language")) != (surface, action, obj, lang):
                errors.append(f"prophetic {rid}/{verse}: source surface, language or named object corrupted")
            for key, val in (("checkState", "DIGITAL_VERSE_SURFACE_CHECKED"),
                             ("criticalEditionStatus", "NOT_COLLATED")):
                if occ.get(key) != val:
                    errors.append(f"prophetic {rid}/{verse}: textual critical status incorrectly promoted")
            if lang == "greek":
                # Explicit per-witness source contract: Greek LXX ≠ Greek NT edition.
                greek_sources = {
                    "Isaiah 7:14 LXX Rahlfs-Hanhart": (
                        "Rahlfs-Hanhart 2006 via Deutsche Bibelgesellschaft",
                        "PERMISSION_REQUIRED",
                        "EDITORIAL_GREEK_TRANSLATION_NO_MANUSCRIPT_APPARATUS"),
                    "Matthew 1:23": (
                        "SBLGNT 2010 via BibleGateway",
                        "RIGHTS_UNKNOWN",
                        "NEW_TESTAMENT_CITATION_AND_TRANSLATION"),
                }
                allowed = greek_sources.get(verse)
                if allowed is None:
                    errors.append(f"prophetic {rid}/{verse}: unregistered Greek edition")
                elif (occ.get("edition"), occ.get("rightsState")) != allowed[:2]:
                    errors.append(f"prophetic {rid}/{verse}: edition-specific rights/witness provenance changed")
                elif (verse == "Isaiah 7:14 LXX Rahlfs-Hanhart"
                      and occ.get("sourceRole") != allowed[2]):
                    errors.append(f"prophetic {rid}/{verse}: LXX source role changed")
                elif (verse == "Matthew 1:23"
                      and occ.get("receptionLayer") != allowed[2]):
                    errors.append(f"prophetic {rid}/{verse}: NT reception role changed")
            elif occ.get("rightsState") != "RIGHTS_UNKNOWN":
                errors.append(f"prophetic {rid}/{verse}: unreviewed source rights were changed")
            if not URL.match(str(occ.get("sourceUrl",""))):
                errors.append(f"prophetic {rid}/{verse}: missing HTTPS text locator")
            if isinstance(occ.get("surface"),str):
                errors.extend(unicode_surface_issues(f"prophetic {rid}/{verse}",occ["surface"]))
        if not isinstance(row.get("contextualAssertion"),str) or not row["contextualAssertion"].strip():
            errors.append(f"prophetic {rid}: claim boundary missing")

    el = index.get("el-gibbor", {})
    r9 = next((a for a in el.get("attestations",[]) if isinstance(a,dict)
               and a.get("verse") == "Isaiah 9:5 MT (English 9:6)"), {})
    if r9.get("numbering") != {"hebrew": "Isaiah 9:5", "english": "Isaiah 9:6"}:
        errors.append("prophetic Isaiah 9:5 numbering systems conflated")
    if r9.get("contextualTitleSegmentation") != "INTERPRETIVE_DISPUTE":
        errors.append("prophetic Isaiah 9 royal naming dispute suppressed")
    r10 = next((a for a in el.get("attestations",[]) if isinstance(a,dict)
                and a.get("verse")=="Isaiah 10:21"),{})
    if "first אֶל- is preposition" not in str(r10.get("sourceGrammarNote","")):
        errors.append("prophetic Isaiah 10:21 Hebrew preposition was silently erased")
    greek = el.get("printedGreekWitnesses", [])
    if not isinstance(greek,list) or len(greek)!=2:
        errors.append("prophetic Isaiah 9 publisher/Orthodox printed witnesses missing")
    else:
        by_role = {w.get("sourceRole"):w for w in greek if isinstance(w,dict)}
        if set(by_role) != {"PUBLISHER_DIGITAL_GREEK_READ_EDITION","UNPINNED_GREEK_WEB_EDITION"}:
            errors.append("prophetic Isaiah 9: witness editions unreviewedly replaced")
        rh=by_role.get("PUBLISHER_DIGITAL_GREEK_READ_EDITION",{})
        orth=by_role.get("UNPINNED_GREEK_WEB_EDITION",{})
        if (rh.get("longListTheosIschyros"),rh.get("exactEditedPhrase"),rh.get("rightsState")) != (False,"Μεγάλης βουλῆς ἄγγελος","PERMISSION_REQUIRED"):
            errors.append("prophetic Isaiah 9: Rahlfs-Hanhart short name / publisher rights lost")
        if (orth.get("longListTheosIschyros"),orth.get("exactEditedPhrase"),orth.get("rightsState")) != (True,"Θεὸς ἰσχυρός","RIGHTS_UNKNOWN"):
            errors.append("prophetic Isaiah 9: unpinned Orthodox expanded name lost")
        for witness in greek:
            if not isinstance(witness,dict):
                continue
            if witness.get("criticalEditionCollated") is not False or "NO_MANUSCRIPT_CRITICAL_COLLATION" not in str(witness.get("claimScope","")):
                errors.append("prophetic Isaiah 9 Greek digital variants falsely promoted to manuscript collation")
            if not URL.match(str(witness.get("sourceUrl",""))):
                errors.append("prophetic Isaiah 9 Greek edition locator missing")
    ts=index.get("tsidkenu",{}).get("attestations",[])
    by_verse={r.get("verse"):r for r in ts if isinstance(r,dict)}
    if "שְּׁמוֹ" not in str(by_verse.get("Jeremiah 23:6",{}).get("genderCue","")):
        errors.append("prophetic Jeremiah 23:6 masculine royal name cue lost")
    if ("לָהּ" not in str(by_verse.get("Jeremiah 33:16",{}).get("nameDelimiter",""))
        or by_verse.get("Jeremiah 33:16",{}).get("oldGreekPassageStatus") != "MT_33_14_26_ABSENT_IN_OLD_GREEK_JEREMIAH"):
        errors.append("prophetic Jeremiah 33:16 feminine city cue or Old Greek absence lost")
    city=index.get("shammah",{}).get("attestations",[])
    if not any(isinstance(r,dict) and r.get("nameDelimiter") == "וְשֵׁם-הָעִיר מִיּוֹם" for r in city):
        errors.append("prophetic Ezekiel 48:35 explicit city-name phrase lost")
    im=index.get("immanuel",{}).get("attestations",[])
    names={r.get("verse"):r for r in im if isinstance(r,dict)}
    if names.get("Isaiah 7:14 LXX Rahlfs-Hanhart",{}).get("nameDelimiter") != "καλέσεις τὸ ὄνομα αὐτοῦ":
        errors.append("prophetic LXX Isaiah 7:14 singular naming verb lost")
    if names.get("Matthew 1:23",{}).get("namingVerbForm") != "καλέσουσιν 3rd plural":
        errors.append("prophetic Matthew 1:23 plural naming verb lost")
    if names.get("Isaiah 8:10",{}).get("receptionLayer") != "HEBREW_ASSURANCE_SENTENCE":
        errors.append("prophetic Isaiah 8:10 assurance falsely converted into a new name")
    audit=baseline.get("auditProtocol",{}).get("propheticAttestations",{})
    if audit.get("totalAttestations") != expected_total or audit.get("publicationEligible") != 0:
        errors.append("prophetic attestation count or Product gate changed")
    return errors


SIX_TITLE_BASELINE_IDS = {
    "sabaoth", "el-qanna", "tsur", "qedosh-yisrael", "adonai", "elohim"
}
SIX_TITLE_LOCK_FIELDS = (
    "verse", "surface", "language", "edition", "contextRole",
    "speaker", "referent", "isDivineDesignation", "sourceUrl",
    "sourceAccess", "criticalEditionStatus", "rightsState", "publicationState"
)


def validate_six_title_attestations(baseline: dict, contract: dict) -> list[str]:
    """Reusable reviewer-pinned occurrence comparison; not textual-critical collation.

    Independent, committed contract must be reviewed together with ledger on
    edits. No contract regeneration occurs in CI.
    """
    errors: list[str] = []
    if (not isinstance(contract, dict) or contract.get("schemaVersion") != 1
        or contract.get("corpusId") != "NAMES_DIVINE_TITLES_FALSE_REFERENT_ATTESTATION_CONTRACT"):
        return ["six-titles: malformed versioned attestation contract"]
    if set(contract.get("baselineIds", [])) != SIX_TITLE_BASELINE_IDS:
        errors.append("six-titles: fixed baseline ID set changed")
    if tuple(contract.get("requiredFields", [])) != SIX_TITLE_LOCK_FIELDS:
        errors.append("six-titles: core locked-field schema weakened")
    expect = contract.get("lockedAttestations", [])
    if not isinstance(expect, list):
        return errors + ["six-titles: locked witnesses missing"]
    expected_rows: dict[tuple[str, str], dict] = {}
    for idx, item in enumerate(expect):
        if not isinstance(item, dict):
            errors.append(f"six-titles: locked witness {idx} not an object")
            continue
        rid, verse = item.get("baselineId"), item.get("verse")
        key = (str(rid), str(verse))
        if rid not in SIX_TITLE_BASELINE_IDS or key in expected_rows:
            errors.append(f"six-titles: duplicate/unreviewed contract key {key}")
        expected_rows[key] = item
        if any(k not in item for k in SIX_TITLE_LOCK_FIELDS):
            errors.append(f"six-titles: required original-script field absent in contract {key}")
    b_rows = baseline.get("records", [])
    bmap = {r.get("id"):r for r in b_rows if isinstance(r, dict)} if isinstance(b_rows, list) else {}
    actual: dict[tuple[str,str],dict] = {}
    for rid in SIX_TITLE_BASELINE_IDS:
        arr = bmap.get(rid, {}).get("attestations")
        if not isinstance(arr, list):
            errors.append(f"six-titles: missing occurrence list for {rid}")
            continue
        for occurrence in arr:
            if not isinstance(occurrence,dict):
                errors.append(f"six-titles: invalid occurrence for {rid}")
                continue
            key = (rid,str(occurrence.get("verse")))
            if key in actual:
                errors.append(f"six-titles: duplicate occurrence {key}")
            actual[key] = occurrence
            if occurrence.get("sourceAccess") != "DIGITAL_VERSE_SURFACE_CHECKED":
                errors.append(f"six-titles: unverified source access {key}")
            if occurrence.get("criticalEditionStatus") != "NOT_COLLATED":
                errors.append(f"six-titles: false manuscript critical collation {key}")
            if occurrence.get("publicationState") != "BLOCKED":
                errors.append(f"six-titles: unauthorized Product promotion {key}")
            form = occurrence.get("surface")
            if not isinstance(form, str):
                errors.append(f"six-titles: original surface missing {key}")
            else:
                errors.extend(unicode_surface_issues(f"six-titles/{key}", form))
                lang = occurrence.get("language")
                if lang == "greek" and not GREEK.search(form):
                    errors.append(f"six-titles: Greek script absent in {key}")
                if lang == "hebrew" and not HEBREW.search(form):
                    errors.append(f"six-titles: Hebrew script absent in {key}")
            if not URL.match(str(occurrence.get("sourceUrl",""))):
                errors.append(f"six-titles: invalid exact verse locator {key}")
    if len(expected_rows) != 22 or len(actual) != 22:
        errors.append("six-titles: 22 reviewed contextual occurrences required")
    if set(expected_rows) != set(actual):
        errors.append("six-titles: occurrence IDs/verse set changed")
    for key, exp in expected_rows.items():
        obj = actual.get(key)
        if obj is None:
            continue
        for fld in SIX_TITLE_LOCK_FIELDS:
            if obj.get(fld) != exp.get(fld) or fld not in obj:
                errors.append(f"six-titles: {key} field {fld} differs from reviewed witness contract")
    audit = baseline.get("auditProtocol", {}).get("semanticsAndReferents", {})
    if (set(audit.get("ids", [])) != SIX_TITLE_BASELINE_IDS
        or audit.get("totalAttestations") != 22
        or audit.get("publicationEligible") != 0
        or audit.get("criticalCollationStatus") != "NOT_COLLATED"):
        errors.append("six-titles: phase counters or publication hold changed")
    if (contract.get("counts") !=
        {"records": 6, "occurrences": 22, "publicationEligible": 0}):
        errors.append("six-titles: pinned contract counters changed")
    # Cross-object semantic prohibitions not solely controlled by a JSON fixture.
    byid: dict[str,dict[str,dict]] = {}
    for (rid,verse), item in actual.items():
        byid.setdefault(rid, {})[verse] = item
    def obj(rid: str, verse: str) -> dict:
        return byid.get(rid, {}).get(verse, {})
    if obj("sabaoth", "1 Samuel 1:3").get("surface") != "לַיהוָה צְבָאוֹת":
        errors.append("six-titles: 1 Sam 1:3 lamed preposition removed")
    if obj("sabaoth","James 5:4").get("surface") != "Κυρίου Σαβαὼθ":
        errors.append("six-titles: James genitive Greek Sabaoth altered")
    if obj("sabaoth","Romans 9:29").get("surface") != "κύριος Σαβαὼθ":
        errors.append("six-titles: Romans nominative Greek Sabaoth altered")
    if obj("el-qanna","Exodus 34:14").get("nameClause") != "קַנָּא שְׁמוֹ":
        errors.append("six-titles: Exodus 34:14 naming formula suppressed")
    if obj("el-qanna","Deuteronomy 4:24").get("selfNamingInVerse") is not False:
        errors.append("six-titles: Deut 4:24 wrongly promoted to new naming act")
    if (obj("tsur","Deuteronomy 32:31").get("referentClass") != "MIXED_TRUE_GOD_AND_OTHER_ROCK"
        or obj("tsur","Deuteronomy 32:37").get("isDivineDesignation") is not False):
        errors.append("six-titles: foreign rock falsely identified as YHWH")
    if obj("qedosh-yisrael","Isaiah 1:4").get("grammaticalMarker") != "אֶת-":
        errors.append("six-titles: Isaiah 1:4 object marker deleted")
    if obj("adonai","Exodus 34:9").get("tokenOccurrenceCount") != 2:
        errors.append("six-titles: Ex 34:9 repeated Adonai token count lost")
    controls = bmap.get("adonai", {}).get("negativeControls", [])
    if not any(isinstance(x,dict) and x.get("surface") == "אֲדֹנִי"
               and "Abraham" in x.get("referent","") for x in controls if isinstance(controls,list)):
        errors.append("six-titles: Genesis 23 human adoni negative control lost")
    if obj("adonai","Psalms 8:2 MT").get("surface") != "יְהוָה אֲדֹנֵינוּ":
        errors.append("six-titles: Psalm 8 suffixed Adonenu collapsed into Adonai")
    g = obj("elohim","Genesis 1:1")
    if (g.get("verbAgreement") != "בָּרָא Qal perfect 3ms (singular)"
        or g.get("referentClass") != "SINGULAR_CREATOR_GOD"):
        errors.append("six-titles: singular agreement of Gen 1:1 creator lost")
    other = obj("elohim","Exodus 20:2 MT (English 20:3)")
    if (other.get("referentClass") != "OTHER_GODS"
        or other.get("isDivineDesignation") is not False
        or other.get("numbering") != {
            "mechonMamreHebrew": "Exodus 20:2",
            "commonEnglishRussian": "Exodus 20:3"}):
        errors.append("six-titles: Exodus 20 false gods or versification conflated")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--extension", type=Path, default=EXTENSION)
    parser.add_argument("--sources", type=Path, default=SOURCES)
    parser.add_argument("--attestation-contract", type=Path, default=ATTESTATION_CONTRACT)
    args = parser.parse_args()
    try:
        with args.ledger.open("r", encoding="utf-8") as stream:
            data = json.load(stream)
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot read ledger: {exc}", file=sys.stderr)
        return 1
    try:
        with args.extension.open("r", encoding="utf-8") as stream:
            extension = json.load(stream)
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot read extension: {exc}", file=sys.stderr)
        return 1
    try:
        with args.sources.open("r", encoding="utf-8") as stream:
            sources = json.load(stream)
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot read sources: {exc}", file=sys.stderr)
        return 1
    try:
        with args.attestation_contract.open("r", encoding="utf-8") as stream:
            title_contract = json.load(stream)
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot read attestation contract: {exc}", file=sys.stderr)
        return 1
    issues = (validate(data) + validate_extension(extension, data) +
              validate_source_access(sources) + validate_apocalyptic(data, extension) +
              validate_prophetic_namings(data) +
              validate_six_title_attestations(data, title_contract))
    if issues:
        for issue in issues:
            print("FAIL:", issue, file=sys.stderr)
        return 1
    print(f"PASS: {len(data['records'])} Arena baseline + "
          f"{len(extension['records'])} extension rows + "
          f"{len(sources['records'])} source records; publication blocked. "
          "STRUCTURAL only; original-language/content/rights checks are separate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
