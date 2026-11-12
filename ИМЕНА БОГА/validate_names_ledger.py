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
MEMORIAL_CONTRACT = Path(__file__).resolve().parent / "data" / "memorial_attestation_contract_v1.json"
SPEECH_INTERTEXT_CONTRACT = Path(__file__).resolve().parent / "data" / "speech_intertext_contract_v1.json"
EXTENSION_ATTESTATION_CONTRACT = Path(__file__).resolve().parent / "data" / "extension_attestation_contract_v1.json"
CORE_NAME_LEXEME_CONTRACT = Path(__file__).resolve().parent / "data" / "core_name_lexeme_contract_v1.json"
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
    "SRC-KROGEVOLL-TORONTO-PHD-2022-EL-SHADDAI": "ATTRIBUTED_KROGEVOLL_2022_COMPLETE_PHD_SHADDAI_MOUNTAIN_CONTACT_HYPOTHESIS",
    "SRC-BROOKE-MCLEAN-LXX-EX17-16-CAMBRIDGE-1909-P211": "CAMBRIDGE_1909_PRINTED_LXX_EX17_16_CRITICAL_VARIANTS_DIRECT_FACSIMILE_NOT_GOTTINGEN_OR_MANUSCRIPT",
    "SRC-WEVERS-GOTTINGEN-EXODUS-1991-AUTHOR-INTRO-EN2006": "WEVERS1991_ENGLISH_AUTHOR_INTRO_METHOD_APP_I_APP_II_GREEK_VARIANT_FIELD_DEPENDENCE_NO_EX17_LOCUS_APPARATUS",
    "SRC-FIELD-HEXAPLA-1875-EX17-16-PRINT-P111-BSB": "FIELD1875_ORIGINAL_PRINT_EX17_16_HEXAPLARIC_EDITORIAL_COMPILATION_NOT_INDEPENDENT_GREEK_CODEX_OR_ALEPPO_LEAF",
    "SRC-KITTEL-BHK2-1909-EX17-16-P99-ORIGINAL-APP": "KITTEL_BHK2_1909_ORIGINAL_PRINT_P99_EX17_16_VARIANT_APPARATUS_NOT_BHK3_1937_OR_BHS1977_OR_ALEPPO",
    "SRC-DBG-BHS-EX17-16-PUBLISHER-TEXT": "DEUTSCHE_BIBELGESELLSCHAFT_BHS_EX17_16_PUBLISHER_MAIN_TEXT_TWO_WORDS_NO_APPARATUS_SHOWN",
    "SRC-MGKETER-BIU-COHEN-EX17-16-ONLINE-ONE-WORD": "BIU_MGKETER_COHEN_ONLINE_EX17_16_ONE_WORD_EDITORIAL_RECONSTRUCTION_NOT_LOST_ALEPPO_FOLIO",
    "SRC-LENINGRAD-B19A-F042A-EX17-16-WSRP-FACSIMILE": "LENINGRAD_B19A_F042A_ORIGINAL_PHOTO_EX17_16_EXACT_LINE_MAP_NOT_PALEOGRAPHIC_CERTIFICATION_OR_ALEPPO",
    "SRC-BL-OR4445-F59V-EX17-16-OPENN-IMAGE-UNRESOLVED": "BL_OR4445_F59V_ORIGINAL_TENTH_CENTURY_DIGITAL_FACSIMILE_EX17_16_WORD_DIVISION_UNRESOLVED_CONFLICT",
    "SRC-DOVI-MIQRA-MASORAH-CH3-EX17-16-COMPOSITE-EDITORIAL": "DOVI_ONLINE_EDITORIAL_MASORAH_METHOD_11_COMPOSITE_FORMS_EX17_16_TWO_VERSUS_REPORTED_ALEPPO_ONE_WORD_NOT_ANCIENT_CODEX",
    "SRC-KRUGER-SHADDAY-JOB-2023-CONTEXT-CRITIQUE": "ATTRIBUTED_MODERN_JOB_SHADDAY_PRAGMATICS_WITH_VERIFIED_TEXTUAL_COUNTERCHECK",
    "SRC-OFER-TEXTUS26-2016-ALEPPO-EX8-FRAGMENT": "OFER2016_EXODUS8_SURVIVING_ORIGINAL_FRAGMENT_PARTIAL_CHECK_OF_SAPHIR_ZER_QUESTIONS_NOT_EXODUS17_16_FOLIO",
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
    "SRC-EUSEBIUS-DEMONSTRATIO-7-1-135-GREEK-ISA9": "EUSEBIUS_DEMONSTRATIO_7_1_135_GREEK_SOME_COPIES_LONG_ISAIAH9_TESTIMONY",
    "SRC-PASS-PENNER-MARCHALIANUS-ISA9-ZIEGLER-REPORT": "SECONDARY_MARCHALIANUS_ISAIAH9_GREEK_LONG_READING_APPARATUS_SIGLA_REPORTED",
    "SRC-ZIEGLER-GOTTINGEN-ISAIAS-1983-ORIGINAL-APPARATUS-ACCESS": "ZIEGLER_GOTTINGEN_ISAIAS_1983_ORIGINAL_APP_I_II_PREVIEW_CH1_ISA9_UNREAD",
    "SRC-BAV-VATGR2125-MARCHALIANUS-Q-ISAIAH-IIIF": "VATICAN_ORIGINAL_Q_VAT_GR_2125_ISAIAH_171_338_IIIF_MANIFEST_NO_ISA9_FOLIO_AUTOPSY",
    "SRC-ORTHODOX-ISAIAH9": "UNPINNED_ORTHODOX_GREEK_WEB_SURFACE",
    "SRC-RASHI-ISAIAH9": "ATTRIBUTED_JEWISH_EXEGETICAL_RECEPTION",
    "SRC-RADAK-ISAIAH9": "ATTRIBUTED_JEWISH_EXEGETICAL_RECEPTION",
    "SRC-NET-ISAIAH7": "ATTRIBUTED_TRANSLATION_NOTES",
    "SRC-LEUCHTER-JER33": "ATTRIBUTED_ACADEMIC_TEXTUAL_CRITICISM_ABSTRACT",
    "SRC-RASHI-EZEK48": "ATTRIBUTED_JEWISH_EXEGETICAL_RECEPTION",
    "SRC-SBLGNT-NT-SABAOTH": "GREEK_NT_SEMITIC_TRANSLITERATION_WITNESS",
    "SRC-SUCHARD-ELOHIM-2025": "ATTRIBUTED_SECONDARY_SEMITIC_MORPHOLOGY_HYPOTHESIS",
    "SRC-CAMBRIDGE-GOD-PRONOUNS": "ATTRIBUTED_SECONDARY_GRAMMAR_AND_THEOLOGY",
    "SRC-ZER-SAPHIR-MEOROT-NATAN-1986-EX17-137": "ZER_1986_ANONYMOUS_JTS_L729_COPY_ALEPPO_WORD_JOIN_REPORT_EX17_137",
    "SRC-OFER-BREUER-MASORAH-2008-EX17-16": "OFER_2008_EDITORIAL_BREUER_TWO_WORD_VERSUS_ALEPPO_ONE_WORD_ATTRIBUTED_ANALYSIS",
    "SRC-HALEVANON-18630611-ISSUE5-EX17-16-ORIGINAL": "HALEVANON_1863_ISSUE5_P32_ORIGINAL_PRINT_EX17_16_ONE_WORD_REPORT_NOT_ALEPPO_CODEX_AUTOPSY",
    "SRC-OFER-1992-YELLIN-HALEVANON-UNSIGNED-SCHOLARLY-CROSSWALK": "OFER_1992_INDEPENDENT_HISTORIOGRAPHIC_DISPUTE_ZEEV_BERLIN_AND_UNSIGNED_HALEVANON",
    "SRC-PENKOWER-TEXTUS9-1981-SAPHIR-HALEVANON-1863": "PENKOWER_1981_PRINTED_P78_N63_SAPHIR_1863_ISSUE5_JTS729_BIBLIOGRAPHIC_CROSSWALK",
    "SRC-BREUER-MEGADIM10-1990-SITHON-SAPIR-REPORT": "BREUER_1990_ORIGINAL_P104_SAPIR_MENASHE_SITHON_YAAKOV_ZEEV_1857",
    "SRC-GOSHEN-GOTTSTEIN-TEXTUS2-1962-JTS729": "GOSHEN_GOTTSTEIN_1962_FIRSTHAND_JTS729_MANUSCRIPT_REPORT_NOT_PRESENT_DAY_AUTOPSY_AND_SCRIBE_HYPOTHESIS",
    "SRC-SAPIR-EVEN-SAPIR-1866-CH6-PRIMARY-AUTHOR": "SAPHIR_1866_FIRSTPERSON_COURIER_MENASHE_SATHON_YES_NO_REPLY_NOT_CODEx_SELF_AUTOPSY",
    "SRC-RAHLFS-EXODUS17": "PUBLISHER_LXX_EXODUS_TRANSLATIONAL_SURFACE",
    "SRC-NET-EXODUS17": "ATTRIBUTED_TRANSLATION_TEXTUAL_HYPOTHESES",
    "SRC-NET-GENESIS22": "ATTRIBUTED_TRANSLATION_GRAMMAR_ALTERNATIVES",
    "SRC-SBLGNT-JOHN10": "CHRISTOLOGICAL_INTERTEXTUAL_SURFACE",
    "SRC-SBLGNT-ABBA-PAUL-MARK": "GREEK_ABBA_DIRECT_PRAYER_AND_PAULINE_ADOPTION",
    "SRC-SBLGNT-JOHN-EGO": "GREEK_EGO_EIMI_WITH_HUMAN_NEGATIVE_CONTROL",
    "SRC-RAHLFS-EXODUS3": "PUBLISHER_GREEK_LXX_EXODUS3_SELF_REVELATION",
    "SRC-BARR-ABBA-1988": "ATTRIBUTED_ABBA_LEXICAL_CRITIQUE_CATALOG_ONLY",
    "SRC-JBQ-YAH-2014": "ATTRIBUTED_SECONDARY_YAH_NAME_USAGE_AND_TRANSLATION_HISTORY",
    "SRC-NET-PS68": "ATTRIBUTED_PS68_HEBREW_BET_OR_CONJECTURAL_KI",
    "SRC-SBLGNT-DIGITAL-NT": "GREEK_NT_EDITION_CORPUS_LEVEL_TEXT_WITNESS",
    "SRC-TMSJ-VALDIZAN-EX3-2024": "ATTRIBUTED_EXODUS3_DIVINE_NAME_TRANSLATION_2024",
    "SRC-TMSJ-VALDIZAN-ACTS2-2024": "ATTRIBUTED_ACTS2_YHWH_KYRIOS_CHRISTOLOGY_2024",
    "SRC-TMSJ-CHOU-TRANSLATION-2024": "ATTRIBUTED_TRANSLATION_FORMAL_EQUIVALENCE_THEOLOGY_2024",
    "SRC-TMSJ-BARRICK-TRANSLATION-2024": "ATTRIBUTED_BIBLICAL_TRANSLATION_NEHEMIAH8_2024",
    "SRC-TMSJ-CHOU-DANIEL-2024": "ATTRIBUTED_DANIEL7_CHRISTOLOGY_JOURNAL_CATALOG_2024",
    "SRC-VT-LIEBERMANN-JEREMIAH-2023": "ATTRIBUTED_JEREMIAH_DAVIDIC_NAME_TEXTUAL_VARIANTS_2023",
    "SRC-OTE-ERZBERGER-JER33-2013": "ATTRIBUTED_JEREMIAH_33_14_26_MT_OLD_GREEK_EXPANSION_AND_ROYAL_CITY_NAME_DEBATE_2013",
    "SRC-RAHLFS-JEREMIAH23-40": "PUBLISHER_EDITED_LXX_JEREMIAH_23_6_AND_CHAPTER_CROSSWALK",
    "SRC-QUMRAN-DIGITAL-4Q72-JER33-2023": "EDITED_4Q72_JER33_16_20_FRAGMENT55II_READ_NOT_PHOTO",
    "SRC-ETCBC-ABEGG-BOWLEY-COOK-4Q72-JER33": "ABEGG_BOWLEY_COOK_ETCBC_4Q72_JER33_EDITORIAL_MARKUP_AND_NONCOMMERCIAL_LICENSE",
    "SRC-LANGLOIS-JEREMIAH-4Q72-2019": "ATTRIBUTED_SCHOLARLY_ANALYSIS_4Q72_MT_JER33_16_20_VS_OLD_GREEK",
    "SRC-DJD-XV-TOV-4QJERC-1997": "TOV_DJD_XV_4QJERC_PRIMARY_EDITED_INTRO_TABLES_NOT_PLATE_AUTOPSY",
    "SRC-GARCIA-MARTINEZ-TIGCHELAAR-1999-STUDY-EDITION-4Q72-271272": "BRILL_1999_4Q72_SECONDARY_DIFFERENT_COLUMN_AND_POTENTIAL_MUSEUM_PLATE_TYPO",
    "SRC-DSS-REED-FASC7-4Q72-PAM43101": "ARCHIVAL_PAM_43_101_MUSEUM_PLATE_245_4Q72_COLUMNS_XXIV_XXV",
    "SRC-IAA-B279109-PAM40963-4Q72-1954": "IAA_1954_PAM_M40_963_4Q72_MULTI_MANUSCRIPT_NEGATIVE_CATALOG_ONLY",
    "SRC-IAA-B360205-4Q72-PL245F6": "IAA_B360205_OFFICIAL_INFRARED_VISUALLY_INSPECTED_NO_INDEPENDENT_GLYPH_COLLATION",
    "SRC-MAIER-IECOT-JEREMIAH-1-25-2025": "SCHOLARLY_2025_MANUSCRIPT_SIGLA_CROSSWALK_4Q72_VS_4Q72A",
    "SRC-NET-REV1-8": "ATTRIBUTED_TRANSLATION_CRITICAL_NOTES",
    "SRC-TABB-REVELATION22": "ATTRIBUTED_COMMENTARY_REVELATION_SPEAKER_INFERENCE",
    "SRC-DEIRALLA-SYMPOSIUM-1991-NYU": "DEIR_ALLA_CONTESTED_EARLY_INSCRIPTION_READING_AND_BIBLICAL_SHADDAY_RELATION",
    "SRC-DEIRALLA-STEINER-WAGEMAKERS-2019": "DEIR_ALLA_FIND_CONTEXT_FRAGMENTS_AND_PHOTO_LOCATORS",
    "SRC-DEIRALLA-BLUM-EBR-2013": "DEIR_ALLA_CONTROVERSIAL_RELIGIOUS_AND_ARCHAEOLOGICAL_INTERPRETATION",
    "SRC-BLUM-DEIRALLA-RECONSTRUCTION-2016-METATEXTE": "DEIR_ALLA_2016_BLUM_AUTHOR_RECONSTRUCTION_CONTEXTUAL_SHDYN_AND_ALT_HEAVEN_GATE_READING",
    "SRC-PATEL-WILSONWRIGHT-DEIRALLA-DIALECT-SBL2015": "ATTRIBUTED_SBL2015_DEIR_ALLA_CANAAANITE_LANGUAGE_HYPOTHESIS_VS_OTHER_CLASSIFICATIONS",
    "SRC-DANS-TELL-DEIRALLA-SLIDES-ARCHIVE-XS5-KPQN": "PRIMARY_DANS_TELL_DEIR_ALLA_ARCHAEOLOGICAL_SLIDES_ARCHIVE_CATALOG_ONLY",
    "SRC-DEIRALLA-HOFTIJZER-VANDERKOOIJ-1976-CONTENTS": "DEIR_ALLA_ORIGINAL_EDITION_ACQUISITION_QUEUE",
    "SRC-IMG-DEIRALLA-DISDERO-2020": "ILLUSTRATION_OF_RECONSTRUCTED_TEXT_CC_BY_SA_4",
    "SRC-IMG-DEIRALLA-LEIDEN-POSTER-1989": "HISTORICAL_EXHIBITION_POSTER_CC0",
    "SRC-IMG-DEIRALLA-AMIN-WHE-2019": "ORIGINAL_MUSEUM_OBJECT_PHOTO_LINK_ONLY",
    "SRC-IMG-DEIRALLA-ACOR-LAPP-1987-NOT-BALAAM": "IMAGE_MISIDENTIFICATION_GUARD_ACOR_ARCHIVE",
    "SRC-SCHOLAR-SAUNDERS-DEIRALLA-2024": "SCHOLARLY_SURVEY_DEIRALLA_REFERENTS_AND_DIALECT_CONTROVERSY",
    "SRC-TSOLIN-ORIEKHOVA-DEIRALLA-2025": "DEIR_ALLA_COMPOSITION_AND_ARCHEOLOGICAL_WALL_VS_CEILING_HYPOTHESES",
    "SRC-IMG-DEIRALLA-LENDERING-LIVIUS-CC0": "ACTUAL_DEIR_ALLA_MUSEUM_PLASTER_PHOTOGRAPH_CC0",
    "SRC-LIVIUS-LEVINE-COMPOSITE-TRANSLATION-2003": "ATTRIBUTED_DEIR_ALLA_ENGLISH_RECONSTRUCTION_1976_2003_NOT_PRIMARY_INSCRIPTION",
    "SRC-HEINTZ-DEIRALLA-1976-REVIEW-1980": "ATTRIBUTED_1980_DEIR_ALLA_EDITORIAL_LINE_DIVISION_DATING_AND_PLATE_VARIANTS",
    "SRC-LEMAIRE-DEIRALLA-SCRIBAL-2021": "DEIR_ALLA_LEMAIRE_2021_ATTRIBUTED_SCRIBAL_COPY_DATE_HYPOTHESIS",
    "SRC-HACKETT-DEIRALLA-FIRSTHAND-1986": "HACKETT_1986_FIRSTHAND_MUSEUM_INSPECTION_AND_ATTRIBUTED_SHDYN_REPOINTING_PROPOSAL",
    "SRC-LEMAIRE-REVIEW-HACKETT-1984-P142": "LEMAIRE_1984_DIRECT_CRITIQUE_OF_HACKETT_1984_FRAGMENT_PLACEMENT_INK_AND_DATING",
    "SRC-ADAJ1979-IBRAHIM-VANDERKOOIJ-PHASEIX": "PRIMARY_EXCAVATION_1979_PHASE_M_IX_PROVISIONAL_DATING_DESTRUCTION_OBSERVATION",
    "SRC-LEMAIRE-DEIRALLA-1985-RADIOCARBON-PP271272": "LEMAIRE_1985_ATTRIBUTED_C14_FRANKEN1976_P16_POSSIBLE_AMOS_EARTHQUAKE",
    "SRC-ADAJ1986-IBRAHIM-VANDERKOOIJ-2C14-P142": "PRIMARY_1986_EXCAVATION_TWO_IDENTIFIED_RADIOCARBON_SAMPLES_AND_PHASE_IX_MATERIAL_CONTEXT",
    "SRC-WEINSTEIN-1984-DEIRALLA-C14-CONFLICT-P351": "WEINSTEIN1984_GRN5283_GRN5633_SAMPLE_ID_CONFLICT_WITH_ADAJ1986",
    "SRC-VOGEL-WATERBOLK-1972-GRONINGEN-DEIRALLA-P53": "PRIMARY_1972_GRONINGEN_LAB_SAMPLE_IDS_VALUES_CONTEXT",
    "SRC-CAQUOT-LEMAIRE-DEIRALLA-REASSEMBLY-1977-P193198": "ORIGINAL_1977_CRITICAL_REASSEMBLY_EXACT_LINE_CONCORDANCE_SHDYN_VS_SDH",
    "SRC-HACKETT-DEIRALLA-MONOGRAPH-1984-SELECTED-OCR": "HACKETT1984_SELECTED_UNVERIFIED_OCR_AUTHORED_HYPOTHESES_NOT_ANCIENT_COLLATION",
    "SRC-ELLIFF-COLEMAN-DEIRALLA-I6-2023": "ELLIFF_COLEMAN2023_ATTRIBUTED_I6_TPRY_GODDESS_BOLTS_RECONSTRUCTION",
    "SRC-HOFTIJZER-BALAAM-ARTICLE-1976-BA39-1": "EARLY_DEIR_ALLA_PUBLICATION_WITH_FORMALLY_PUBLISHED_CORRIGENDUM_ACCESS_HOLD",
    "SRC-HOFTIJZER-BALAAM-ERRATUM-1976-BA39-3": "ORIGINAL_1976_JOURNAL_EDITORIAL_TITLE_DATE_CORRECTION_DIRECT_SCAN",
    "SRC-HOFTIJZER-PHOENIX22-DEIRALLA-1976-FIG41-42": "EARLY_DEIR_ALLA_HOFTIJZER1976_AUTHOR_ARTICLE_WITH_IR_PHOTO_CAPTION_AND_RECONSTRUCTED_SHADDAY_TRANSLATION",
    "SRC-FRANKEN-1967-VT-FIRST-INSCRIPTION-PHOTO-480481": "FRANKEN1967_EARLIEST_PUBLISHED_DEIRALLA_FRAGMENT_PHOTO_REPORTED_IN_LEMAIRE1985_PAGE480_TEXT_PREVIEW_ONLY",
    "SRC-IAA-DSS-4Q120-B503715-2015": "PRIMARY_IAA_4Q120_GREEK_LEVITICUS_PHOTO_CATALOGUE_NO_GLYPH_COLLATION",
    "SRC-CLEMENT-STROMATA-5-6-34-STAHLIN-GREEK": "CLEMENT_STROMATA_5_6_34_EDITED_GREEK_IAOUE_PASSAGE_NOT_AUTOGRAPH_OR_CERTAIN_PHONETICS",
    "SRC-DEISSMANN-BIBLE-STUDIES-1901-TETRAGRAM-GREEK": "DEISSMANN_1901_SECONDARY_TEXTUAL_VARIANT_WARNING_CLEMENT_IAOUE_THEODORET_FORMS",
    "SRC-ROMER-COLLEGE-DE-FRANCE-YHWH-2011": "ROMER_2011_ACADEMIC_SECONDARY_PATRISTIC_NAME_FORMS_AND_4Q120_FRAGMENT20_LEV4",
    "SRC-THEODORET-EXODUM-15-PG80-243-GREEK": "THEODORET_EXODUM_XV_PG80_243_DIRECT_DIGITAL_GREEK_PARTIAL_CUTOFF_BEFORE_JEWISH_NAME",
    "SRC-THEODORET-COMPENDIUM-V3-PG83-460-GREEK": "THEODORET_COMPENDIUM_V3_PG83_460_DIRECT_EDITED_GREEK_SHADDAI_GLOSS_AND_SAMARITAN_IABAI",
    "SRC-KINZIG-PATRISTIC-TETRAGRAM-2008-P226227": "KINZIG_2008_EARLY_CHRISTIAN_YHWH_TRANSMISSION_VARIANTS_QUAESTIONES_COMPENDIUM_CRITIQUE",
    "SRC-JTS-MS1154-L729-MEOROT-NATAN-1855-EX17-16-MICROFILM": "DIRECT_JTS_NINETEENTH_CENTURY_COPIED_QUESTION_REPLY_EX17_16_NO_ANCIENT_CODEX_SURVIVING_LEAF",
    "SRC-OFER-TEXTUS21-2002-COMPOSITE-WORDS-MASORAH": "OFER_2002_COMPOSITE_WORDS_MASORAH_LIST_VERSUS_CODEX_TEXT_METHODOLOGY_NOT_EX17_16_PROOF",
    "SRC-OFER-MEGADIM37-2003-YEIVIN82-COMPOSITE-WORDS": "OFER2003_AUTHOR_DIRECT_CITES_YEIVIN_PRINT82_FOR_PS90_ISA54_WORD_DIVISION_NOT_EX17_PROOF",
    "SRC-PESACHIM117A-COMPOSITE-KESYAH-AMORAIC-EDITED-DIGITAL": "TALMUD_PESACHIM117A_ATTRIBUTED_AMORAIC_ONE_WORD_AND_TWO_WORD_OPINIONS_NOT_ANCIENT_ALEPPO_PHOTO",
    "SRC-RASHBATZ-TASHBETZ-I177-KESYAH-RESPONSUM": "RASHBATZ_TASHBETZ_I177_DIRECT_HISTORICAL_AUTHOR_TESTIMONY_NON_ALEPPO_SCROLL_AND_CONFLICTING_MASORETIC_LISTS",
    "SRC-ARUCH-HASHULCHAN-YD27524-KESYAH-TWO-WORD-DECISION": "ARUCH_HASHULCHAN_YD27524_EXPLICIT_TWO_WORD_HALAKHIC_RULING_USING_FIVE_WORD_MASORAH_LIST",
}


# These are source-specific, closed-review provenance locks. They do NOT authorize
# Product publication: the per-record publicationState remains BLOCKED.
DEIR_ALLA_SOURCE_GUARDS = {
    "SRC-HOFTIJZER-BALAAM-ARTICLE-1976-BA39-1": ("CATALOG_ONLY", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-HOFTIJZER-BALAAM-ERRATUM-1976-BA39-3": ("FULL_OBJECT_VERIFIED", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-HOFTIJZER-PHOENIX22-DEIRALLA-1976-FIG41-42": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-FRANKEN-1967-VT-FIRST-INSCRIPTION-PHOTO-480481": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-DEIRALLA-SYMPOSIUM-1991-NYU": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-DEIRALLA-STEINER-WAGEMAKERS-2019": ("PARTIAL_OBJECT", "RIGHTS_UNKNOWN", "COARSE_LOCATOR_ONLY"),
    "SRC-DEIRALLA-BLUM-EBR-2013": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-BLUM-DEIRALLA-RECONSTRUCTION-2016-METATEXTE": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-PATEL-WILSONWRIGHT-DEIRALLA-DIALECT-SBL2015": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-DANS-TELL-DEIRALLA-SLIDES-ARCHIVE-XS5-KPQN": ("CATALOG_ONLY", "RIGHTS_UNKNOWN", "COARSE_LOCATOR_ONLY"),
    "SRC-DEIRALLA-HOFTIJZER-VANDERKOOIJ-1976-CONTENTS": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-IMG-DEIRALLA-DISDERO-2020": ("FULL_OBJECT_VERIFIED", "PUBLICATION_ELIGIBLE", "EXACT_LOCATOR_VERIFIED"),
    "SRC-IMG-DEIRALLA-LEIDEN-POSTER-1989": ("FULL_OBJECT_VERIFIED", "PUBLICATION_ELIGIBLE", "EXACT_LOCATOR_VERIFIED"),
    "SRC-IMG-DEIRALLA-AMIN-WHE-2019": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-IMG-DEIRALLA-ACOR-LAPP-1987-NOT-BALAAM": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-SCHOLAR-SAUNDERS-DEIRALLA-2024": ("PARTIAL_OBJECT", "RIGHTS_UNKNOWN", "EXACT_LOCATOR_VERIFIED"),
    "SRC-TSOLIN-ORIEKHOVA-DEIRALLA-2025": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-IMG-DEIRALLA-LENDERING-LIVIUS-CC0": ("FULL_OBJECT_VERIFIED", "PUBLICATION_ELIGIBLE", "EXACT_LOCATOR_VERIFIED"),
    "SRC-LIVIUS-LEVINE-COMPOSITE-TRANSLATION-2003": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-HEINTZ-DEIRALLA-1976-REVIEW-1980": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-LEMAIRE-DEIRALLA-SCRIBAL-2021": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-HACKETT-DEIRALLA-FIRSTHAND-1986": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-LEMAIRE-REVIEW-HACKETT-1984-P142": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-ADAJ1979-IBRAHIM-VANDERKOOIJ-PHASEIX": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-LEMAIRE-DEIRALLA-1985-RADIOCARBON-PP271272": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-ADAJ1986-IBRAHIM-VANDERKOOIJ-2C14-P142": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-WEINSTEIN-1984-DEIRALLA-C14-CONFLICT-P351": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-VOGEL-WATERBOLK-1972-GRONINGEN-DEIRALLA-P53": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-CAQUOT-LEMAIRE-DEIRALLA-REASSEMBLY-1977-P193198": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-HACKETT-DEIRALLA-MONOGRAPH-1984-SELECTED-OCR": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
    "SRC-ELLIFF-COLEMAN-DEIRALLA-I6-2023": ("PARTIAL_OBJECT", "PERMISSION_REQUIRED", "EXACT_LOCATOR_VERIFIED"),
}
DEIR_ALLA_VISUAL_LICENSE_GUARDS = {
    "SRC-IMG-DEIRALLA-LENDERING-LIVIUS-CC0": (
        "CC0 1.0",
        "https://creativecommons.org/publicdomain/zero/1.0/",
        "https://www.livius.org/pictures/jordan/deir-alla/deir-alla-inscription/",
    ),
    "SRC-IMG-DEIRALLA-DISDERO-2020": (
        "CC BY-SA 4.0",
        "https://creativecommons.org/licenses/by-sa/4.0/",
        "https://commons.wikimedia.org/wiki/File:Deir_%27Alla_Inscription.png",
    ),
    "SRC-IMG-DEIRALLA-LEIDEN-POSTER-1989": (
        "CC0 1.0",
        "https://creativecommons.org/publicdomain/zero/1.0/",
        "https://commons.wikimedia.org/wiki/File:Een_verhaal_voor_het_oprapen._Opgravingen_te_Deir_Alla_in_de_Jordaanvallei,_Objectnr_AF_B429.jpg",
    ),
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
        wave50_evidence_locks = {
            "SRC-PESACHIM117A-COMPOSITE-KESYAH-AMORAIC-EDITED-DIGITAL": {
                "year": None,
                "sourceRole": "TALMUD_PESACHIM117A_ATTRIBUTED_AMORAIC_ONE_WORD_AND_TWO_WORD_OPINIONS_NOT_ANCIENT_ALEPPO_PHOTO",
                "fields": {
                    "talmudPage": "Pesachim 117a",
                    "editedHebrewFullTextViewed": True,
                    "physicalOrPhotographicTalmudManuscriptViewed": False,
                    "rabbiYohananThroughRavChisdaOneWordList": ["הללויה", "כסיה", "ידידיה"],
                    "ravOneWordList": ["כסיה", "מרחביה"],
                    "rabbahOneWordList": ["מרחביה"],
                    "rabbahEditedOrthography": "רבה",
                    "rashbatzCitationLastSpeakerOrthography": "רבא",
                    "thisRabbaRavaDifferenceResolved": False,
                    "exodus17_16AuthorialInterpretation": True,
                    "originalAleppoCodexFolioSeen": False,
                    "criticalYeivinBreuerPagesRead": False,
                    "permissionToRepublishTranscriptApproved": False,
                },
            },
            "SRC-RASHBATZ-TASHBETZ-I177-KESYAH-RESPONSUM": {
                "year": None,
                "sourceRole": "RASHBATZ_TASHBETZ_I177_DIRECT_HISTORICAL_AUTHOR_TESTIMONY_NON_ALEPPO_SCROLL_AND_CONFLICTING_MASORETIC_LISTS",
                "fields": {
                    "responsumPart": 1,
                    "responsumNumber": 177,
                    "authorDeathYear": 1444,
                    "compositionYearEstablished": False,
                    "printed1738EditionPublishedExactResponsumPageVerified": False,
                    "editedHebrewFullTextViewed": True,
                    "first1738PrintFolioViewed": False,
                    "second1741PrintFolioViewed": False,
                    "any15thCenturyAutographViewed": False,
                    "authorSawSomeTorahScroll": True,
                    "authorSawAleppoCodex": False,
                    "torahScrollSeparatelyLineWrittenHebrew": "כס יה בשתי שטות",
                    "countOfTwoLetterWordsInFirstMasorahList": 6,
                    "countOfTwoLetterWordsInRivalList": 5,
                    "masoreticListConflictUnresolved": True,
                    "alternativeMasorahStatus": "פלוגתא היא מלה א׳",
                    "samekhShevaProvesWordUnity": False,
                    "samekhShevaAnalogy": "אש דת",
                    "authorDescribesPhysicalCorrection": True,
                    "originalJTS1855CopyWitnessIndependence": "DIFFERENT_HISTORICAL_TRADITION_NOT_SAME_PHYSICAL_SOURCE",
                    "lastSpeakerQuotedByAuthorOrthography": "רבא",
                    "criticalTalmudNameVariantResolved": False,
                    "rightsClearedForDigitalTranscript": False,
                    "originalAleppoCodexPhotoViewed": False,
                    "originalYeivinBreuerCriticalPagesRead": False,
                },
            },
            "SRC-ARUCH-HASHULCHAN-YD27524-KESYAH-TWO-WORD-DECISION": {
                "year": 1891,
                "sourceRole": "ARUCH_HASHULCHAN_YD27524_EXPLICIT_TWO_WORD_HALAKHIC_RULING_USING_FIVE_WORD_MASORAH_LIST",
                "fields": {
                    "section": "Yoreh Deah 275:24",
                    "editedHebrewFullSectionViewed": True,
                    "originalAuthorPrintFacsimileLocated": True,
                    "originalAuthorPrintScanCatalogueUrl": "https://commons.wikimedia.org/wiki/File:AHS_YD_B4.djvu",
                    "originalRelevantPrintedPageVisuallyInspected": False,
                    "editedPublisherObservedOneWordDispute": True,
                    "rulingHebrew": "וההכרעה היא שהם שני תיבות",
                    "masorahVerseQuoted": "כי יד על כס יה",
                    "masorahCountsTwoLetterWords": 5,
                    "authorSaysWriteBothOnSameLine": True,
                    "oneWordTalmudViewAcknowledged": True,
                    "authorPhysicalAleppoCodexViewed": False,
                    "legalDecisionsAreAncientTextualCollations": False,
                    "fullYeivinBreuerCriticalPagesRead": False,
                    "photoRepublicationRightsApproved": False,
                },
            },
        }
        if rid in wave50_evidence_locks:
            expected = wave50_evidence_locks[rid]
            v = source.get("verifiedWave50", {})
            if (source.get("year") != expected["year"]
                    or source.get("sourceRole") != expected["sourceRole"]
                    or source.get("accessState") != "PARTIAL_OBJECT"
                    or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                    or source.get("evidenceClass") != "A2"
                    or source.get("rightsState") != "PERMISSION_REQUIRED"
                    or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False
                    or set(source.get("holds", [])) != {"EVIDENCE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"}
                    or not isinstance(v, dict)
                    or any(v.get(field) != value or type(v.get(field)) is not type(value)
                           for field, value in expected["fields"].items())):
                errors.append(f"{prefix}: Wave50 historical Kesyah source cannot be ancient codex collation, other author's identity, or rights clearance")
        if rid == "SRC-ZER-SAPHIR-MEOROT-NATAN-1986-EX17-137":
            w = source.get("checkedProvenance", {})
            if (source.get("rightsState") != "PERMISSION_REQUIRED" or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False or not isinstance(w, dict)
                    or w.get("jtsShelfmark") != "JTS L 729" or w.get("copyScribe") != "ANONYMOUS_NOT_SAPHIR"
                    or w.get("itemPrintPage") != 165 or w.get("itemNumber") != 137 or w.get("notePrintPage") != 191
                    or w.get("part1ImagePageZeroBased") != 14 or w.get("part2ImagePageZeroBased") != 8
                    or w.get("originalPrintedPagesVisuallyViewed") is not True
                    or w.get("jtsOriginalManuscriptViewed") is not True
                    or w.get("jtsOriginalManuscriptImageScope") != "ONE_JTS_MS1154_1855_COPY_MICROFILM_FRAME_NOT_PHYSICAL_ITEM_OR_ANCIENT_CODEX"
                    or w.get("saphirAutographViewed") is not False
                    or w.get("aleppoExodusFolioViewed") is not False or w.get("yeivinPage82Viewed") is not False
                    or w.get("breuerPages260261Viewed") is not False):
                errors.append(f"{prefix}: Zer 1986 copied manuscript wrongly promoted to original Aleppo/Saphir/Yeivin/Breuer access")
        if rid == "SRC-ZER-SAPHIR-MEOROT-NATAN-1986-EX17-137":
            audit = source.get("zer1986PrintedP152QuestionCountAuditWave39", {})
            torah = audit.get("torahListedInclusiveRange") if isinstance(audit, dict) else None
            esther = audit.get("estherListedInclusiveRange") if isinstance(audit, dict) else None
            haft = audit.get("haftarotListedQuestionNumbers") if isinstance(audit, dict) else None
            valid_ranges = (isinstance(torah, list) and len(torah) == 2 and
                            isinstance(esther, list) and len(esther) == 2 and
                            all(type(v) is int for v in torah + esther) and
                            isinstance(haft, list) and all(type(v) is int for v in haft))
            total = (torah[1] - torah[0] + 1 + esther[1] - esther[0] + 1 + len(haft)) if valid_ranges else None
            if (not isinstance(audit, dict) or not valid_ranges
                    or audit.get("printPage") != 152 or audit.get("pdfPageZeroBased") != 1
                    or audit.get("originalPrintedPageImageVisuallyInspected") is not True
                    or audit.get("introApproximatelyQuestionsAtP151") != 550
                    or audit.get("printedTotalNumberedQuestionsAtP152") != 543
                    or audit.get("printedReportedMissingQuestionsAtP152") != 422
                    or torah != [1, 383] or esther != [507, 543]
                    or haft != [440, 401, 402, 406, 462, 463, 465, 466, 476, 477]
                    or total != 430 or len(set(haft)) != len(haft)
                    or audit.get("computedCountFromListedInclusiveRanges") != total
                    or audit.get("computedMinusPrintedReportedMissingCount") != 8
                    or audit.get("reconciliationStatus") != "UNRESOLVED_PRINTED_COUNT_VS_INCLUSIVE_RANGES"
                    or audit.get("ancientManuscriptPhotographicCollation") is not False
                    or audit.get("printNumbersMayBeSilentlyCorrected") is not False):
                errors.append(f"{prefix}: Zer1986 p152 printed 422 versus enumerated 430 remains unresolved")
        if rid == "SRC-ZER-SAPHIR-MEOROT-NATAN-1986-EX17-137":
            photo = source.get("zer1986PhotoCoveredQuestionOverlapWave40", {})
            a = photo.get("wickes1887QuestionIds") if isinstance(photo, dict) else None
            b = photo.get("segall1910Goshen1966QuestionIds") if isinstance(photo, dict) else None
            distinct = (len(set(a+b)) if isinstance(a, list) and isinstance(b, list)
                        and all(type(v) is int for v in a+b) else -1)
            if (not isinstance(photo, dict)
                    or photo.get("zerPrintPage") != 152 or photo.get("zerFootnote") != 9
                    or photo.get("zerPrintedFootnoteVisuallyInspected") is not True
                    or a != [49, 50, 51] or b != [336, 337, 338, 339, 340]
                    or photo.get("wickesPhotoBook") != "GENESIS_26_TO_27"
                    or photo.get("segallPhotoBook") != "DEUTERONOMY_4_TO_6"
                    or photo.get("wickesPhotoAncientLettersCollatedByResearch") is not False
                    or photo.get("goshen1966OriginalArticleTextRead") is not True
                    or photo.get("goshen1966PlateAncientLettersCollatedByResearch") is not False
                    or photo.get("zerListPrintPagesInspected") != [161, 172, 173]
                    or photo.get("question339IsTwicePrintedAsSeparateRows") is not True
                    or distinct != 8 or photo.get("totalDistinctPhotoCoveredQuestionNumbers") != distinct
                    or photo.get("candidateExplainsNumericDifferenceEight") is not True
                    or photo.get("editorExplicitlyStatesPhotoExclusionRule") is not False
                    or photo.get("photoExclusionHypothesis") != "PLAUSIBLE_NOT_PROVEN"
                    or photo.get("reconciliationConfirmed") is not False
                    or photo.get("aleppoOriginalMissingExodusLeafInspected") is not False):
                errors.append(f"{prefix}: Zer1986 photo-covered eight-number coincidence is an unresolved hypothesis, not a corrected author count or ancient manuscript collation")
        if rid == "SRC-OFER-BREUER-MASORAH-2008-EX17-16":
            w = source.get("checkedProvenance", {})
            if (source.get("rightsState") != "PERMISSION_REQUIRED" or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False or not isinstance(w, dict)
                    or w.get("academicArticleFullTextReproductionRead") is not True
                    or w.get("originalJSIJTypesetPdfViewed") is not False
                    or w.get("originalBreuerPagesViewed") is not False or w.get("originalYeivinPageViewed") is not False
                    or w.get("ancientAleppoExodusViewed") is not False
                    or w.get("breuerTwoWordDecisionReported") is not True
                    or w.get("aleppoOneWordReported") is not True
                    or w.get("mikraotGedolotHaKeterOneWordReported") is not True):
                errors.append(f"{prefix}: Ofer 2008 secondary review wrongly promoted to ancient/critical primary source")
        if rid == "SRC-ZER-SAPHIR-MEOROT-NATAN-1986-EX17-137":
            d = source.get("canonicalManuscriptCatalogueRoute20261110", {})
            if (not isinstance(d, dict)
                    or d.get("nliRecordId") != "NNL_ALEPH990001022670205171"
                    or d.get("nliCatalogAttributedCreator") != "Jacob Saphir (יעקב ספיר), 1822–1885"
                    or d.get("notNathanShapiraId") != "NNL_ALEPH990000621650205171"
                    or d.get("nliRecordShelfmarkIndependentlyOpened") is not True
                    or d.get("nliManuscriptImagesOpened") is not True
                    or d.get("exodus17_16HandwritingIndependentlyRead") is not True
                    or d.get("jtsPhysicalOriginalPersonallyHandled") is not False
                    or d.get("nliVerseImageSourceIdWave47") != "SRC-JTS-MS1154-L729-MEOROT-NATAN-1855-EX17-16-MICROFILM"
                    or d.get("historicalNewspaperContentReadInDigitalScan") is not False):
                errors.append(f"{prefix}: Sapir versus Shapira Maorot Nathan catalog and unearned original scan access")
        if rid == "SRC-ZER-SAPHIR-MEOROT-NATAN-1986-EX17-137":
            d = source.get("canonicalManuscriptCatalogueRoute20261110", {})
            e = d.get("iiifDigitalRouteWave46", {}) if isinstance(d, dict) else {}
            img_ids = ["FL28558008", "FL28558009", "FL28558014", "FL28558015",
                       "FL28558018", "FL28558020", "FL28558023", "FL28558025",
                       "FL28558027", "FL28558029", "FL28558031", "FL28558033", "FL28558035"]
            if (not isinstance(d, dict) or not isinstance(e, dict)
                    or d.get("nliCurrentOwnerShelfmark") != "The Jewish Theological Seminary of America, Ms. 1154"
                    or d.get("nliLutzkiCatalogueShelfmark") != "L 729"
                    or d.get("nliAdlerFormerOwnerShelfmark") != "Adler, Elkan Nathan Ms. 1632"
                    or d.get("nliManuscriptPhysicalFoliosFromCatalog") != 8
                    or d.get("nliManuscriptCatalogueYear") != 1855
                    or d.get("nliShelfmarkCrosswalkStatus") != "DIRECT_CATALOGUE_HTML_VERIFIED_MS1154_EQUALS_LUTZKI_L729"
                    or e.get("pageMetadataReadFromNliHtml") is not True
                    or e.get("htmlViewerItemUrl") != "FL28558009"
                    or e.get("nliIiifServiceUrl") != "https://iiif.nli.org.il/IIIFv21"
                    or e.get("thumbnailSequencePageCountVisible") != 13
                    or e.get("thumbnailImageIds") != img_ids
                    or e.get("lastImageInfoJsonUrl") != "https://iiif.nli.org.il/IIIFv21/FL28558035/info.json"
                    or e.get("lastImageInfoJsonHttpStatus") != 200
                    or e.get("lastImageNativePixelWidth") != 4544
                    or e.get("lastImageNativePixelHeight") != 3640
                    or e.get("lastImageJpegExample") != "https://iiif.nli.org.il/IIIFv21/FL28558035/full/1136,/0/default.jpg"
                    or e.get("exampleImageHttpStatus") != 200
                    or e.get("documentManifestAttemptUrl") != "https://iiif.nli.org.il/IIIFv21/DOCID/NNL_ALEPH990001022670205171/manifest"
                    or e.get("documentManifestHttpStatus") != 403
                    or e.get("allThirteenFullImagesVisuallyInspected") is not False
                    or e.get("manuscriptEntry137LocatedOnExactImage") is not False
                    or e.get("exodus17_16ManuscriptLettersCollated") is not False
                    or e.get("independentAncientAleppoCodexWitnessGained") is not False
                    or e.get("nliCatalogueRightsStatement") != "PUBLIC_DOMAIN_ISRAEL_WITH_ATTRIBUTION_AND_JURISDICTION_CAVEAT"
                    or e.get("iiifImageInfoRightsLink") != "http://web.nli.org.il/sites/NLI/Hebrew/library/items-terms-of-use/Pages/nli-copying-prohibited.aspx"
                    or e.get("iiifRightsLinkConsistencyResolved") is not False
                    or e.get("siteFacsimileRepublicationApproved") is not False):
                errors.append(f"{prefix}: JTS Ms1154/Lutzki L729 IIIF metadata is not handwriting collation or publication approval")
        if rid == "SRC-JTS-MS1154-L729-MEOROT-NATAN-1855-EX17-16-MICROFILM":
            p = source.get("verifiedOriginalCopyPhotoWave47", {})
            if (source.get("year") != 1855
                    or source.get("url") != "https://iiif.nli.org.il/IIIFv21/FL28558023/full/4544,/0/default.jpg"
                    or source.get("catalogueUrl") != "https://www.nli.org.il/he/manuscripts/NNL_ALEPH990001022670205171/NLI"
                    or source.get("evidenceClass") != "A2"
                    or source.get("accessState") != "PARTIAL_OBJECT"
                    or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                    or source.get("rightsState") != "PERMISSION_REQUIRED"
                    or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False
                    or set(source.get("holds", [])) != {"EVIDENCE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"}
                    or not isinstance(p, dict)
                    or p.get("owningLibrary") != "The Jewish Theological Seminary of America"
                    or p.get("physicalShelfmark") != "Ms. 1154"
                    or p.get("lutzkiShelfmark") != "L 729"
                    or p.get("formerAdlerShelfmark") != "Ms. 1632"
                    or p.get("digitalCatalogueId") != "NNL_ALEPH990001022670205171"
                    or p.get("iiifImageId") != "FL28558023"
                    or p.get("iiifViewerFrameOneBased") != 7
                    or p.get("iiifFullImageUrl") != "https://iiif.nli.org.il/IIIFv21/FL28558023/full/4544,/0/default.jpg"
                    or p.get("imageWidthPx") != 4544 or p.get("imageHeightPx") != 6455
                    or p.get("jpegBytes") != 1559912
                    or p.get("sha256") != "243a38b1b9201e3648bdd356558bcef7fa412fc98d5112fca177904153d17019"
                    or p.get("frameTargetRegion") != "LEFT_PAGE_LOWER_QUARTER_EXODUS_17_16_AFTER_17_14_ZAKHOR_BEFORE_YITRO"
                    or p.get("pageLabelVisibleAtUpperLeft") != "4a"
                    or p.get("exodus17_16VerseLabelVisible") is not True
                    or p.get("keyWordGroups") != "כס יה"
                    or p.get("questionHebrew") != "שתי מלות"
                    or p.get("answerOpeningHebrew") != "לא כן"
                    or p.get("answerMarginCoreHebrew") != "אלא חדא מלה"
                    or p.get("completeMarginalPaleographyIndependentlyCollated") is not False
                    or p.get("directlyInspectedOneMicrofilmImage") is not True
                    or p.get("physicalManuscriptHandled") is not False
                    or p.get("jtsManuscriptCopyOriginalPhotographed") is not True
                    or p.get("saphirAutographProven") is not False
                    or p.get("originalAleppoExodusFolioPhotographed") is not False
                    or p.get("independentAncientWitnessCountAdded") != 0
                    or p.get("publicDomainIsraelCatalogueClaimSeen") is not True
                    or p.get("imageRightsInternationalVerified") is not False
                    or p.get("productImageReuseApproved") is not False
                    or p.get("criticalApparatusYeivin82Breuer260261Read") is not False):
                errors.append(f"{prefix}: JTS L729 direct historic copy Ex17:16 collation cannot be ancient codex, autograph, critical apparatus or rights approval")
        if rid == "SRC-JTS-MS1154-L729-MEOROT-NATAN-1855-EX17-16-MICROFILM":
            m = source.get("verifiedCroppedMarginalDetailWave48", {})
            if (not isinstance(m, dict)
                    or m.get("imageId") != "FL28558023"
                    or m.get("sourceSha256") != "243a38b1b9201e3648bdd356558bcef7fa412fc98d5112fca177904153d17019"
                    or m.get("sourceNativeImagePixelSize") != [4544, 6455]
                    or m.get("cropNativePixelsXYXY") != [120, 4490, 1100, 5060]
                    or m.get("imageManipulation") != "CONTRAST_ENHANCED_GRAYSCALE_CROP_FOR_READABILITY_ONLY"
                    or m.get("originalUnmodifiedPhotoWasPreviouslyVisuallyRead") is not True
                    or m.get("manuscriptQuestionRead") != "שתי מלות"
                    or m.get("manuscriptAnswerOpeningRead") != "לא כן"
                    or m.get("manuscriptMarginSafeExcerpt") != "אלא חדא מלה"
                    or m.get("fullMarginDifficultHandReadingProven") is not False
                    or m.get("samekhShevaTechnicalNoteAllGlyphsConfirmed") is not False
                    or m.get("mappiqHeTechnicalNoteAllGlyphsConfirmed") is not False
                    or m.get("printedZer1986ReadingSubstitutedForUnclearInk") is not False
                    or m.get("historical1863NewspaperReadingSubstitutedForUnclearInk") is not False
                    or m.get("ancientAleppoOriginalVerseViewed") is not False
                    or m.get("secondaryAuthorEditionConflictsResolved") is not False):
                errors.append(f"{prefix}: JTS L729 Wave48 narrow direct marginal reading must not inherit edited print or unverified shva/mappiq glyphs")
        if rid == "SRC-OFER-TEXTUS21-2002-COMPOSITE-WORDS-MASORAH":
            a = source.get("verifiedWave48", {})
            if (source.get("year") != 2002 or source.get("doi") != "10.1163/2589255x-02101011"
                    or source.get("accessState") != "PARTIAL_OBJECT"
                    or source.get("locatorState") != "COARSE_LOCATOR_ONLY"
                    or source.get("rightsState") != "PERMISSION_REQUIRED"
                    or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False
                    or set(source.get("holds", [])) != {"EVIDENCE_HOLD", "LOCATOR_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"}
                    or not isinstance(a, dict)
                    or a.get("journal") != "Textus" or a.get("volume") != 21 or a.get("issue") != 1
                    or a.get("printPages") != "209–233"
                    or a.get("doi") != "10.1163/2589255x-02101011"
                    or a.get("publisherOrUniversityAbstractRead") is not True
                    or a.get("publisherFirstTwoPagePreviewExtracted") is not True
                    or a.get("originalFullArticleAllPagesRead") is not False
                    or a.get("publisherPreviewScreenshotSucceeded") is not False
                    or a.get("publisherAbstractSaysAtLeastFourDiscrepantCompositeWords") is not True
                    or a.get("originalCompositeListMayHaveLaterScribeAsAuthorConjecture") is not True
                    or a.get("exodus17_16AmongFourProven") is not False
                    or a.get("independentAncientCodexPhotoInspected") is not False
                    or a.get("rightsPermissionGranted") is not False):
                errors.append(f"{prefix}: Ofer 2002 composite list abstract is not proof of Exodus17:16 example or full critical edition")
            w54=source.get("verifiedWave54", {})
            if (not isinstance(w54,dict)
                    or source.get("officialArchiveFullPdfUrl") != "https://bibleproject.huji.ac.il/sites/default/files/he_bible_project/files/y._ofer.pdf"
                    or w54.get("officialIndexUrl") != "https://bibleproject.huji.ac.il/textus"
                    or w54.get("officialPdfUrl") != source.get("officialArchiveFullPdfUrl")
                    or w54.get("pdfStatusCode") != 200 or w54.get("pdfPages") != 25
                    or w54.get("wholeEnglishTextExtracted") is not True
                    or w54.get("exodus17_16AuthorSingleWord") is not True
                    or w54.get("exodus17_16SappirZerQ137Source") is not True
                    or w54.get("exodus17_16CodexComparisonConcordant") is not True
                    or w54.get("exodus17_16AmongDiscrepantFour") is not False
                    or w54.get("hebrewTextExtractionReliable") is not False
                    or w54.get("allPrintedPageFacsimilesInspected") is not False
                    or w54.get("extantAleppoExodusFolioViewed") is not False
                    or w54.get("yeivin82Breuer260261OriginalsRead") is not False
                    or w54.get("rightsGranted") is not False
                    or w54.get("productApproved") is not False):
                errors.append(f"{prefix}: Ofer 2002 Wave54 direct English article must not certify Hebrew facsimile or ancient leaf")
        if rid == "SRC-OFER-MEGADIM37-2003-YEIVIN82-COMPOSITE-WORDS":
            e = source.get("verifiedWave49", {})
            if (source.get("year") != 2003
                    or source.get("sourceRole") != "OFER2003_AUTHOR_DIRECT_CITES_YEIVIN_PRINT82_FOR_PS90_ISA54_WORD_DIVISION_NOT_EX17_PROOF"
                    or source.get("evidenceClass") != "B1"
                    or source.get("accessState") != "PARTIAL_OBJECT"
                    or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                    or source.get("rightsState") != "PERMISSION_REQUIRED"
                    or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False
                    or set(source.get("holds", [])) != {"EVIDENCE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"}
                    or not isinstance(e, dict)
                    or e.get("publisher") != "Torat Har Etzion / Tevunot (Megadim)"
                    or e.get("publisherDate") != "2003-02-03"
                    or e.get("megadimIssue") != 37
                    or e.get("publisherHtmlAuthorTextRead") is not True
                    or e.get("originalPrintedMegadimFacsimileReviewed") is not False
                    or e.get("articleExactOriginalPrintPagesKnown") is not False
                    or e.get("relevantSection") != "קד"
                    or e.get("authorYeivinCitationsFootnotes") != [23, 24, 26]
                    or e.get("yeivin1968_69BookPageCited") != 82
                    or e.get("psalm90_15CitedAsCompositeCase") is not True
                    or e.get("isaiah54_9CitedAsCompositeCase") is not True
                    or e.get("isaiah54_9AleppoFormAttributedByOfer") != "כי-מי"
                    or e.get("independentYeivinPage82Read") is not False
                    or e.get("exodus17_16InThisAuthorArticle") is not False
                    or e.get("breuer1977Print260261Read") is not False
                    or e.get("manuscriptMasoraAndActualCodexNotInterchangeable") is not True
                    or e.get("print2002OferFirstFullTextRead") is not False
                    or e.get("independentAncientAleppoWitnessAdded") != 0
                    or e.get("republicationRightsApproved") is not False):
                errors.append(f"{prefix}: Ofer 2003 Yeivin82 cross-reference for Psalms/Isaiah cannot become direct Yeivin Exodus or Breuer autopsy")
        if rid == "SRC-HALEVANON-18630611-ISSUE5-EX17-16-ORIGINAL":
            w = source.get("printedObjectVerificationWave42", {})
            if (source.get("year") != 1863 or source.get("url") != "https://www.nli.org.il/he/newspapers/hlb/1863/06/11/01/"
                    or source.get("sourceRole") != "HALEVANON_1863_ISSUE5_P32_ORIGINAL_PRINT_EX17_16_ONE_WORD_REPORT_NOT_ALEPPO_CODEX_AUTOPSY"
                    or source.get("evidenceClass") != "A2" or source.get("accessState") != "FULL_OBJECT_VERIFIED"
                    or source.get("rightsState") != "PERMISSION_REQUIRED" or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False or not isinstance(w, dict)
                    or w.get("archiveIssueDate") != "1863-06-11" or w.get("issueNumberFromOriginalMasthead") != 5
                    or w.get("printedPageRange") != "25-32" or w.get("fileName") != "18630611_01.pdf"
                    or w.get("physicalPages") != 8 or w.get("pdfBytes") != 686922
                    or w.get("sha256") != "16270eaf4d3165fae17d1ca8e944e5e47085d0dfa7535944c36754a0ad29cc1d"
                    or w.get("firstPageMastheadVisuallyInspected") is not True
                    or w.get("originalPrintPages31And32VisuallyInspected") is not True
                    or w.get("originalEx17_16PrintLineVisuallyRead") is not True
                    or w.get("verse") != "Exodus 17:16" or w.get("printPage") != 32
                    or w.get("pdfPageOneBased") != 8 or w.get("column") != "RIGHT_LAST_LINE_EXODUS"
                    or w.get("rubric") != "שמות" or w.get("startRubric") != "כתר תורה"
                    or w.get("reference") != "י״ז ט״ז" or w.get("typesetWordGroups") != "כס יה"
                    or w.get("wordCountStatement") != "חדא מלה"
                    or w.get("normalizedExcerpt") != "י״ז ט״ז כס יה חדא מלה והס׳ בשוא וההא במפיק"
                    or w.get("sourcePrintedOneWordReport") is not True
                    or w.get("newAncientManuscriptWitness") is not False
                    or w.get("originalAleppoExodusLeafSeen") is not False
                    or w.get("jtsL729OriginalSeen") is not False
                    or w.get("yeivinBreuerCriticalPagesSeen") is not False
                    or w.get("authorSignedNewspaperPageProven") is not False
                    or w.get("permissionToReuseNliScan") is not False
                    or w.get("ofer1992ConfirmsKeterTorahUnsigned") is not True
                    or w.get("possibleEditorBrillOnlyConjecture") is not True):
                errors.append(f"{prefix}: 1863 original newspaper one-word report is not an ancient codex or cleared scan")
        if rid == "SRC-ZER-SAPHIR-MEOROT-NATAN-1986-EX17-137":
            c = source.get("courierNewspaperComparisonWave44", {})
            if (not isinstance(c, dict)
                    or c.get("zer1986QAPrintPage") != 165
                    or c.get("zer1986QuestionWordCount") != "שתי מלות"
                    or c.get("zer1986ReplyWordCount") != "לא כן אלא חדא מלה"
                    or c.get("newspaper1863PrintPage") != 32
                    or c.get("newspaperOneWordReport") != "חדא מלה"
                    or c.get("sameReportedResultOneWord") is not True
                    or c.get("verbatimSameLiteraryWording") is not False
                    or c.get("independentAncientWitnessCountAdded") != 0
                    or c.get("zer1986NewspaperIssueNumbers") != [3,4,5,11]
                    or c.get("onlyIssueFiveOriginalPhotoInspected") is not True
                    or c.get("otherIssuesThreeFourElevenDirectlyInspected") is not False):
                errors.append(f"{prefix}: historic 1863 newspaper vs Zer1986 Q&A not verbatim identical or independent ancient witness")
        if rid == "SRC-OFER-1992-YELLIN-HALEVANON-UNSIGNED-SCHOLARLY-CROSSWALK":
            q = source.get("verifiedWave44", {})
            if (source.get("year") != 1992 or source.get("url") != "https://www.daat.ac.il/daat/vl/yosefofer/yosefofer04.pdf"
                    or source.get("sourceRole") != "OFER_1992_INDEPENDENT_HISTORIOGRAPHIC_DISPUTE_ZEEV_BERLIN_AND_UNSIGNED_HALEVANON"
                    or source.get("evidenceClass") != "B1" or source.get("accessState") != "PARTIAL_OBJECT"
                    or source.get("rightsState") != "PERMISSION_REQUIRED"
                    or source.get("publicationState") != "BLOCKED" or source.get("criticalEditionCollated") is not False
                    or not isinstance(q, dict)
                    or q.get("printYear") != 1992 or q.get("articlePrintPages") != "295–353"
                    or q.get("courierDiscussionPrintPage") != 315
                    or q.get("footnotesRead") != [75,76,77] or q.get("bibliographyPrintPage") != 352
                    or q.get("originalP315PageImageRead") is not True
                    or q.get("originalP352PageImageRead") is not True
                    or q.get("oferRejectsIdentityJoin") is not True
                    or q.get("courierLabel") != "ר' יעקב זאב"
                    or q.get("otherScholarLabel") != "ר' יעקב ברלין"
                    or q.get("zer1986ConflatedPrintedName") != "ר' יעקב זאב ברלין"
                    or q.get("historicalNewspaperUnsigned") is not True
                    or q.get("possibleEditorialWriter") != "יחיאל ברי״ל"
                    or q.get("possibleWriterIsEstablishedAuthor") is not False
                    or q.get("listedFirstPageNumbers") != [16,23,30,31,76]
                    or q.get("otherNewspaperIssuesPersonallyInspected") is not False
                    or q.get("ancientCodexOriginalInspected") is not False
                    or q.get("jtsL729ManuscriptInspected") is not False
                    or q.get("rightsApproved") is not False):
                errors.append(f"{prefix}: Ofer1992 distinct courier and unsigned newspaper claim must not be promoted to certified person/author/ancient witness")
        if rid == "SRC-PENKOWER-TEXTUS9-1981-SAPHIR-HALEVANON-1863":
            w = source.get("checkedAccess", {})
            if (source.get("url") != "https://openscholar.huji.ac.il/sites/default/files/he_bible_project/files/penkower_j.s.1.pdf"
                    or source.get("year") != 1981 or source.get("doi") != "10.1163/2589255x-00901005"
                    or source.get("rightsState") != "PERMISSION_REQUIRED" or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False or not isinstance(w, dict)
                    or w.get("originalPenkowerPublishedPdfTextPrintedPage78Read") is not True
                    or w.get("originalPenkowerPublishedPdfPage78ScreenshotSuccess") is not False
                    or w.get("penkowerPrintPage") != 78 or w.get("footnoteNumber") != 63
                    or w.get("halevanonYear") != 1863 or w.get("halevanonIssueNumber") != 5
                    or w.get("halevanonPagesReported") != "31b–32a"
                    or w.get("halevanonIssue5CandidateDateFromOfficialNLIIndex") != "1863-06-11"
                    or w.get("halevanonIssue5CalendarAndDownloadPageVerified") is not True
                    or w.get("halevanonIssue5OriginalMastheadPhotoInspected") is not True
                    or w.get("halevanonIssue5DateEvidenceState") != "DIRECT_ORIGINAL_NEWSPAPER_PRINT_CONFIRMED"
                    or w.get("halevanonPreviousMistakenDate") != "1863-07-09"
                    or w.get("july9OriginalIssueNumberDirectlyInspected") != 6
                    or w.get("july9OriginalIssuePagesDirectlyInspected") != "33-40"
                    or w.get("july9OriginalIssueFullEightPagePdfVisuallyInspected") is not True
                    or w.get("july9OriginalIssuePdfSha256") != "72c1d29b9b22c0d42cb2686be4b22fdf75b0942f2e3a08705e675eeba7f0f1a8"
                    or w.get("halevanonDirectOriginalPrintSourceId") != "SRC-HALEVANON-18630611-ISSUE5-EX17-16-ORIGINAL"
                    or w.get("june11OriginalIssuePdfSha256") != "16270eaf4d3165fae17d1ca8e944e5e47085d0dfa7535944c36754a0ad29cc1d"
                    or w.get("june11IssueArchiveUrl") != "https://www.nli.org.il/he/newspapers/hlb/1863/06/11/01/"
                    or w.get("june11FullIssuePdfDownloadPageUrl") != "https://www.nli.org.il/he/newspapers/?a=is&oid=hlb18630611-01&type=staticpdf&e=-------he-20--1--img-txIN%7CtxTI--------------1"
                    or w.get("halevanonOriginalIssuePage31and32ImageIndependentlyInspected") is not True
                    or w.get("halevanonVerseHebrewWordsIndependentlyCollated") is not True
                    or w.get("nliSaphirManuscriptCatalogueId") != "NNL_ALEPH990001022670205171"
                    or w.get("unrelatedNathanShapiraNLICatalogueId") != "NNL_ALEPH990000621650205171"
                    or w.get("jts729AutographInspected") is not False
                    or w.get("aleppoOriginalExodus17_16ManuscriptInspected") is not False):
                errors.append(f"{prefix}: Penkower 1981 historic newspaper source report crosswalk changed or ancient JTS falsely upgraded")
        if rid == "SRC-ZER-SAPHIR-MEOROT-NATAN-1986-EX17-137":
            w = source.get("respondentIdentityWave34", {})
            if (not isinstance(w, dict) or w.get("respondentHebrew") != "מנשה סיתהון"
                    or w.get("courierHebrew") != "יעקב זאב"
                    or w.get("dispatchYearAccordingToZer") != 1857
                    or w.get("printedZerP151ImageVerified") is not True
                    or w.get("aleppoProjectEarlierSectionName") != "Menashe Stahon / Sithon"
                    or w.get("aleppoProjectLaterSectionName") != "Moshe Sathon"
                    or w.get("differentEnglishNamesResolved") is not False
                    or w.get("manuscriptCopyDate1855VersusDispatch1857Resolved") is not False
                    or w.get("exodusCodexOriginalSeen") is not False
                    or w.get("jtsAutographSeen") is not False):
                errors.append(f"{prefix}: Menashe original witness replaced with Moshe or 1855/1857 chronology falsely solved")
        if rid == "SRC-PENKOWER-TEXTUS9-1981-SAPHIR-HALEVANON-1863":
            w = source.get("checkedAccess", {})
            if not isinstance(w, dict) or w.get("date1855HandCopyVersus1857DispatchReconciled") is not False:
                errors.append(f"{prefix}: Penkower JTS list 1855 date cannot be asserted identical to 1857 courier dispatch")
        if rid == "SRC-BREUER-MEGADIM10-1990-SITHON-SAPIR-REPORT":
            w = source.get("checkedAccess", {})
            if (source.get("url") != "https://kitveyet.herzog.ac.il/vtc/tvunot/mega10_broyer.pdf"
                    or source.get("year") != 1990 or source.get("rightsState") != "PERMISSION_REQUIRED"
                    or source.get("publicationState") != "BLOCKED" or source.get("criticalEditionCollated") is not False
                    or not isinstance(w, dict) or w.get("originalPrintedPage") != 104
                    or w.get("originalPdfPageIndex") != 7 or w.get("pageScreenshotDirectlyInspected") is not True
                    or w.get("personRespondentHebrew") != "מנשה סיתהון"
                    or w.get("courierHebrew") != "יעקב זאב"
                    or w.get("yearQuestionsDispatched") != 1857
                    or w.get("breuerSeparate1977BookRead") is not False
                    or w.get("exodus17_16CollationInThisPaper") is not False
                    or w.get("originalJtsOrAleppoCodexSeen") is not False
                    or w.get("rightsGranted") is not False):
                errors.append(f"{prefix}: Breuer 1990 attribution cannot become his 1977 Exodus critical apparatus or ancient autopsy")
        if rid == "SRC-ZER-SAPHIR-MEOROT-NATAN-1986-EX17-137":
            scribe = source.get("goshen1962DisagreementWave35", {})
            if (not isinstance(scribe, dict)
                    or scribe.get("zer1986ScribeClassification") != "ANONYMOUS_COPYIST_NOT_SAPHIR_AUTOGRAPH"
                    or scribe.get("earlierGoshen1962AuthorshipConjecture") != "SAPHIR_MAY_HAVE_COPIED_HIS_OWN_LIST"
                    or scribe.get("scholarlyHandwritingDisagreementResolved") is not False
                    or scribe.get("originalJTS729HandwrittenPagesIndependentlyCompared") is not False):
                errors.append(f"{prefix}: disputed JTS729 copyist Goshen 1962 versus Zer 1986 cannot be resolved by fiat")
        if rid == "SRC-GOSHEN-GOTTSTEIN-TEXTUS2-1962-JTS729":
            s = source.get("accessAndIndependenceWave35", {})
            if (source.get("url") != "https://bibleproject.huji.ac.il/sites/default/files/he_bible_project/files/goshen-gottstein_m.h.2.pdf"
                    or source.get("year") != 1962
                    or source.get("rightsState") != "PERMISSION_REQUIRED"
                    or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False
                    or not isinstance(s, dict)
                    or s.get("publisherTitleIndexVerified") is not True
                    or s.get("originalPublisherPdfOpened") is not False
                    or s.get("originalPublisherPdfScreenshotVisuallyInspected") is not False
                    or s.get("communityUploadedFullAuthorTextOcrRead") is not True
                    or s.get("communityUploadedTextContainsKnownOcrErrors") is not True
                    or s.get("goshen1962ScholarPersonallyInspectedJts729AccordingToHisPublication") is not True
                    or s.get("ourResearchJTS729OriginalImageViewed") is not False
                    or s.get("goshenFirstPageIntroductionYearReported") != 1855
                    or s.get("goshenYear1855CertainDateOfFinishedAnswerCopy") is not False
                    or s.get("zerBreuerDispatchYearReported") != 1857
                    or s.get("yearsReferToDistinctDescribedEvents") is not True
                    or s.get("fullTranscriptionChronologyProven") is not False
                    or s.get("manuscriptFolioPageCountReported") != 8
                    or s.get("goshenConjecturedSapirCopiedHisOriginalList") is not True
                    or s.get("zer1986EditorAttributedAnonymousScribe") is not True
                    or s.get("disputedScribeIdentityIndependentlyResolved") is not False
                    or s.get("commonHistoricalBaseFor1863NewspaperAndJTSReported") is not True
                    or s.get("independentAncientWitnessCountGained") != 0
                    or s.get("printed1863NewspaperIndependentlyCollated") is not True
                    or s.get("ancientAleppoExodus1716FoliosViewed") is not False
                    or s.get("specificExodus1716OriginalWordformVerifiedDirectly") is not False
                    or s.get("jacobBerlinAndYaakovZeevFullIdentityDemonstrated") is not False
                    or s.get("photoRightsGranted") is not False):
                errors.append(f"{prefix}: Goshen1962 3rd-party OCR cannot become original PDF, direct JTS photo or certified Sapir hand")
        if rid == "SRC-SAPIR-EVEN-SAPIR-1866-CH6-PRIMARY-AUTHOR":
            a = source.get("authorAccessAndClaimsWave36", {})
            if (source.get("url") != "https://benyehuda.org/read/42865"
                    or source.get("year") != 1866 or source.get("rightsState") != "PERMISSION_REQUIRED"
                    or source.get("publicationState") != "BLOCKED" or source.get("criticalEditionCollated") is not False
                    or not isinstance(a, dict) or a.get("originalPrintYear") != 1866
                    or a.get("originalPrintingPDFPagesTotal") != 498
                    or a.get("originalPrintingPageImagesVisuallyInspected") is not False
                    or a.get("authorTextModernDigitalTranscriptionRead") is not True
                    or a.get("modernTranscriptionBasePrintYear") != 1989
                    or a.get("authorHistoricalCourierHebrew") != "יעקב זאב"
                    or a.get("authorHistoricalRespondentHebrew") != "מנשה סתהון"
                    or a.get("scholarZer1986RespondentHebrew") != "מנשה סיתהון"
                    or a.get("respondentOrthographicVariantPreserved") is not True
                    or a.get("authorSaysReturnedRepliesHeldByHim") is not True
                    or a.get("authorPersonallySawAleppoCodex") is not False
                    or a.get("authorExplicitlyDisavowsWitnessOfUnseen") is not True
                    or a.get("relativeFirstReportedYears") != "לפני שבע שנים"
                    or a.get("relativeLaterReportedYears") != "לפני תשע שנים"
                    or a.get("relativeYearsConvertedToFixedGregorianYears") is not False
                    or a.get("samePhysicalReturnedSaphirPaperIdentifiedWithJTS729") is not False
                    or a.get("originalJTS729ManuscriptImagesViewed") is not False
                    or a.get("originalExodus1716CodexFolioSeen") is not False
                    or a.get("original1863PressVerseLineViewed") is not True
                    or a.get("independentAncientManuscriptWitnessesAdded") != 0
                    or a.get("modernTranscriptionRightsIndependentlyCleared") is not False
                    or a.get("photographicReusePermissionFromThisRecord") is not False):
                errors.append(f"{prefix}: Sapir 1866 first-person modern transcription must not become ancient codex/1866 scan autopsy or fixed chronology")
        if rid == "SRC-ZER-SAPHIR-MEOROT-NATAN-1986-EX17-137":
            n = source.get("courierNameCrosswalkWave37", {})
            if (not isinstance(n, dict)
                    or n.get("zerPrintP151FullName") != "ר' יעקב זאב ברלין"
                    or n.get("zerOriginalPrintedPageVisuallyInspected") is not True
                    or n.get("sapirModernAuthorTranscriptionName") != "ר' יעקב זאב"
                    or n.get("goshen1962OCRReportedName") != "Jacob Berlin"
                    or n.get("peretzGolan2023PrintPage") != 67
                    or n.get("peretzGolan2023PdfPageZeroBased") != 16
                    or n.get("peretzGolan2023OriginalPageScreenshotInspected") is not True
                    or n.get("peretzGolan2023PrintedFullName") != "ר' יעקב זאב ברלין"
                    or n.get("peretzGolan2023CitationDependsOnZer1986") is not True
                    or n.get("peretzGolan2023IndependentHistoricalWitness") is not False
                    or n.get("supportedEditorialHistoricallyNamedCourierSame") is not False
                    or n.get("identityResolutionStatusWave44") != "DISPUTED_BY_OFER_1992_TWO_HISTORICAL_ACTORS"
                    or n.get("ofer1992PrintP315Note76DirectlyViewed") is not True
                    or n.get("ofer1992ExplicitlyRejectsConflation") is not True
                    or n.get("derivative2023CannotResolveDispute") is not True
                    or n.get("independentCivilBirthDeathOrGenealogyProven") is not False
                    or n.get("thirdParty2023IndependentAncientManuscript") is not False
                    or n.get("originalManuscriptCourierSignatureInspected") is not False):
                errors.append(f"{prefix}: Yaakov Zeev Berlin composite identity disputed by Ofer1992, ancient codex unseen")
        if rid == "SRC-GOSHEN-GOTTSTEIN-TEXTUS2-1962-JTS729":
            x = source.get("accessAndIndependenceWave35", {})
            if (not isinstance(x, dict)
                    or x.get("historicalCourierNamedCrosswalkCorroboratedByZerFullHebrew") is not False
                    or x.get("ofer1992RejectsCourierIdentityConflation") is not True
                    or x.get("jacobBerlinAndYaakovZeevFullIdentityDemonstrated") is not False):
                errors.append(f"{prefix}: Goshen OCR courier identity cannot overrule distinct-actors argument Ofer1992")
        if rid == "SRC-SAPIR-EVEN-SAPIR-1866-CH6-PRIMARY-AUTHOR":
            x = source.get("authorAccessAndClaimsWave36", {})
            if (not isinstance(x, dict)
                    or x.get("zer1986LaterScholarlyFullCourierName") != "יעקב זאב ברלין"
                    or x.get("separateContextJacobBerlinSignatory") is not True
                    or x.get("ofer1992SeparatesCourierFromJacobBerlin") is not True
                    or x.get("separateContextAloneProvesPersonIdentity") is not False
                    or x.get("literalSaphirTranscriptionIncludesSurnameBerlin") is not False):
                errors.append(f"{prefix}: do not interpolate later surname Berlin into literal Saphir source")
        if rid == "SRC-ETCBC-ABEGG-BOWLEY-COOK-4Q72-JER33":
            if (source.get("url") != "https://theancientbible.org/4q72-p1/"
                    or source.get("fragmentLabel") != "f55ii"
                    or source.get("verseRange") != "Jer 33:16–20"
                    or source.get("firstLineExtantPrefix") != "יהוה צד"
                    or source.get("firstLineCompletionRestored") is not True
                    or source.get("abeggLine5Opening") != "[ה][יום] [ו]את"
                    or source.get("qumranDigitalLine5Opening") != "[היום ו]את"
                    or source.get("sameAncientWitness") != "4Q72"
                    or source.get("independentManuscript") is not False
                    or source.get("independentAncientPhotoCollation") is not False
                    or source.get("licenseNotice") != "CC BY-NC 4.0 / Abegg-Bowley-Cook ETCBC derivative"
                    or source.get("qumranDigitalSeparateNotice") != "CC BY-SA 4.0"
                    or source.get("iaaPhotoLicensedByEitherTextLicense") is not False
                    or source.get("publicationLicenseComplianceApproved") is not False):
                errors.append(f"{prefix}: Abegg/ETCBC Qumran rendering independent witness or license falsely upgraded")
        if rid == "SRC-ZIEGLER-GOTTINGEN-ISAIAS-1983-ORIGINAL-APPARATUS-ACCESS":
            if (source.get("url") != "https://septuaginta.uni-goettingen.de/publications/septuaginta/"
                    or source.get("editionVolume") != "XIV"
                    or source.get("editionYear") != 1983
                    or source.get("editionNumber") != 3
                    or source.get("editionISBN") != "3-525-53424-8"
                    or source.get("originalApparatusIIsaiah9Read") is not False
                    or source.get("originalApparatusIIIsaiah9Read") is not False
                    or source.get("licensedCompleteAccessAvailableToResearch") is not False
                    or source.get("manuscriptsIndependentlyCollated") is not False):
                errors.append(f"{prefix}: Ziegler 1983 edition preview falsely promoted to Isaiah9 apparatus autopsy")
        if rid == "SRC-BAV-VATGR2125-MARCHALIANUS-Q-ISAIAH-IIIF":
            if (source.get("url") != "https://digi.vatlib.it/view/MSS_Vat.gr.2125"
                    or source.get("iiifManifestUrl") != "https://digi.vatlib.it/iiif/MSS_Vat.gr.2125/manifest.json"
                    or source.get("shelfmark") != "Vat.gr.2125"
                    or source.get("septuagintSiglum") != "Q"
                    or source.get("isaiahPageRange") != "171–338"
                    or source.get("manifestCanvasCount") != 1718
                    or source.get("page171Canvas") != "https://digi.vatlib.it/iiif/MSS_Vat.gr.2125/canvas/p0349"
                    or source.get("exactIsaiah9CanvasVerified") is not False
                    or source.get("originalIsaiah9ImagePixelsInspected") is not False
                    or source.get("originalIsaiah9LetterformsCollated") is not False
                    or source.get("photoReusePermissionGranted") is not False):
                errors.append(f"{prefix}: official Q IIIF manifest falsely promoted to image or manuscript-letter autopsy")
            codicology = source.get("page171CodicologicalCrosscheck", {})
            if (not isinstance(codicology, dict)
                    or codicology.get("originalArticleUrl") != "https://www.fdr.uni-hamburg.de/record/11575"
                    or codicology.get("publisherArticleDoi") != "10.25592/uhhfdm.11575"
                    or codicology.get("evidenceMethod") != "ORIGINAL_SCHOLARLY_2022_JOURNAL_PDF_TEXT_EXTRACTED_AT_PRINTED_P56_SCREENSHOT_403_UNAVAILABLE"
                    or codicology.get("page171Isaiah1TextProven") is not False
                    or codicology.get("page171Mark1TextProven") is not False
                    or codicology.get("bookIncludesGospelMark") is not False
                    or codicology.get("independentAncientPhotoAutopsy") is not False
                    or codicology.get("manuscriptTargetIsaiah9VerseCanvasVerified") is not False):
                errors.append(f"{prefix}: Q page171 colophon report cannot certify Mark, Isaiah1 or Isaiah9 ancient photo reading")
        if rid == "SRC-EUSEBIUS-DEMONSTRATIO-7-1-135-GREEK-ISA9":
            if (source.get("url") != "https://www.sophiascriptura.com/fathers/eusebius-demonstratio/7-1-127/"
                    or source.get("ancientReference") != "Demonstratio Evangelica 7.1.135"
                    or source.get("editionPrintedLocator") != "Dindorf vol 3 p 453"
                    or source.get("greekVariantQualifier") != "καὶ τινα τῶν ἀντιγράφων ἔχει"
                    or source.get("someCopiesOnly") is not True
                    or source.get("independentAncientGreekCodexCollated") is not False
                    or source.get("zieglerCriticalApparatusDirectlyRead") is not False):
                errors.append(f"{prefix}: Eusebius some-copy testimony falsely turned into manuscript autopsy")
        if rid == "SRC-PASS-PENNER-MARCHALIANUS-ISA9-ZIEGLER-REPORT":
            if (source.get("url") != "https://pressbooks.atlanticoer-relatlantique.ca/isaiahincodexmarchalianus/chapter/commentary/"
                    or source.get("secondaryZieglerApparatusReport") is not True
                    or source.get("zieglerCriticalApparatusDirectlyRead") is not False
                    or source.get("ancientCodexIndependentlyCollated") is not False
                    or source.get("alexandrinusOmissionQualification") != "A and 26 omit θεός within longer additions"
                    or source.get("originalShortReadingReported") != ["Sinaiticus_original_hand_S_star","Vaticanus_B","Marchalianus_Q"]):
                errors.append(f"{prefix}: scholarly secondary apparatus witness report improperly promoted")
        if rid == "SRC-QUMRAN-DIGITAL-4Q72-JER33-2023":
            if (source.get("url") != "https://lexicon.qumran-digital.org/transcriptions/4Q72/2023-12-08/index.html"
                    or source.get("fragmentLocator") != "55 ii"
                    or source.get("passageRange") != "Jer 33:16–20"
                    or source.get("extantPrefix") != "יהוה צד"
                    or source.get("editorialCompletion") != "קנו"
                    or source.get("transcriptionVersion") != "2023-12-08"
                    or source.get("manuscriptPhotoInspected") is not False
                    or source.get("wholeHebrewNameAutopticallyRead") is not False
                    or source.get("comparisonVersion") != "2025-03-11"
                    or source.get("comparisonUrl") != "https://forum.qumran-digital.org/transcriptions/4Q72/2025-03-11/index.html"
                    or source.get("comparisonKind") != "SAME_SCHOLARLY_PROJECT_VERSION_NOT_INDEPENDENT_WITNESS"
                    or source.get("fiveLineComparisonStatus") != "DIRECT_RENDERED_TEXT_5_OF_5_IDENTICAL_WITH_2023_BASE"
                    or source.get("independentAncientManuscriptFromVersion") is not False
                    or source.get("independentPhotoLetterCollation") is not False
                    or source.get("line1EditorRestorationPreserved") is not True
                    or source.get("editionTextLicenseNotice") != "CC BY-SA 4.0 (Qumran-Digital page copyright footer)"
                    or source.get("editionTextLicenseScope") != "PROJECT_PUBLISHED_EDITION_ONLY_NOT_IAA_PHOTOGRAPH_NOT_LICENSE_TO_THIRD_PARTY_PARALLEL_TEXT"
                    or source.get("photoReusePermissionFromEdition") is not False
                    or source.get("licenseNotAutomaticallyProductApproved") is not True):
                errors.append(f"{prefix}: 4Q72 visible letters versus restoration or manuscript autopsy falsified")
        if rid == "SRC-LANGLOIS-JEREMIAH-4Q72-2019":
            if (source.get("url") != "https://michaellanglois.org/medias/langlois-2019-the-book-of-jeremiahs-redaction-history-in-light-of-its-oldest-manuscripts.pdf"
                    or source.get("selectedPagesVisuallyChecked") != [18, 19]
                    or source.get("manuscriptPhotoIndependentlyCollated") is not False
                    or source.get("originalCriticalApparatusRead") is not False):
                errors.append(f"{prefix}: Langlois original selected-page source upgraded without evidence")
        if rid == "SRC-DJD-XV-TOV-4QJERC-1997":
            if (source.get("url") != "https://catalogue.bnf.fr/ark:/12148/cb37173199v"
                    or source.get("columnJer33") != "XXV"
                    or source.get("columnJer33Verses") != "33:16–20"
                    or source.get("originalColumnXXVImageInspected") is not False
                    or source.get("originalAncientPhotographCollated") is not False
                    or source.get("mirrorDistributionRightsVerified") is not False
                    or source.get("manuscriptId") != "4Q72"
                    or source.get("scholarlySiglum") != "4QJer c"
                    or source.get("distinctManuscriptId") != "4Q72a"
                    or source.get("distinctScholarlySiglum") != "4QJer d"
                    or source.get("djdDistinctManuscriptPrintedPage") != 203
                    or source.get("originalTable8Jer33_16Status") != "bracketed_paragraph_division_reconstruction_NOT_autoptic_photo"
                    or source.get("originalTable9ColXXVLine2") != "Jer 33:17 ישב"
                    or source.get("originalTable9ColXXVLine3") != "Jer 33:18 עלה"):
                errors.append(f"{prefix}: DJD XV selected original edition versus original photo falsely upgraded")
        if rid == "SRC-DJD-XV-TOV-4QJERC-1997":
            photographic = source.get("originalEditorNegativeList20261110", {})
            if (not isinstance(photographic, dict)
                    or photographic.get("authorOriginalPublisherTextInspected") is not True
                    or photographic.get("publishedPrimaryNegativeSeriesContains") != "43.101"
                    or photographic.get("earlierNegativeInParentheses") != "40.963"
                    or photographic.get("sameManuscript4Q72") is not True
                    or photographic.get("sameFrameOrExactF55iiReidentified") is not False
                    or photographic.get("originalPAMNegativePixelsInspected") is not False
                    or photographic.get("originalDJDXVPlatesXXXtoXXXVIInspected") is not False
                    or photographic.get("originalPrintedPagePreciselyPinned") is not False
                    or photographic.get("imageRedistributed") is not False):
                errors.append(f"{prefix}: Tov original editor photo list cannot certify identical negatives, fragment55ii or inspected plates")
        if rid == "SRC-DJD-XV-TOV-4QJERC-1997":
            edition1991 = source.get("firstEdition1991SourceAccessWave21", {})
            if (not isinstance(edition1991, dict)
                    or edition1991.get("universityOriginalPublicationRecord") != "https://cris.huji.ac.il/en/publications/4qjer-4q72/"
                    or edition1991.get("series") != "Orbis Biblicus et Orientalis 109"
                    or edition1991.get("pages") != "249–276"
                    or edition1991.get("photographicPlates") != "I–VII"
                    or edition1991.get("repositoryAccessState") != "ANUBIS_ACCESS_DENIED_AUTOMATED_2026_11_10"
                    or edition1991.get("fullOriginalTextPersonallyRead") is not False
                    or edition1991.get("originalPhotographicPlatesPersonallyViewed") is not False
                    or edition1991.get("targetFrg55iiImageIdentified") is not False
                    or edition1991.get("manuscriptGlyphsIndependentlyCollated") is not False
                    or edition1991.get("publicationReusePermissionGranted") is not False
                    or edition1991.get("officialManuscriptBrowseUrl") != "https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q72-1"
                    or edition1991.get("falsePositiveSearchPhotoUrl") != "https://commons.wikimedia.org/wiki/File:4q72.jpg"
                    or edition1991.get("falsePositiveIsProteinNotScroll") is not True
                    or edition1991.get("falsePositiveAcceptedAsManuscriptPhoto") is not False):
                errors.append(f"{prefix}: first 1991 Tov plate route must not certify viewed plates or misidentified protein photo")
        if rid == "SRC-DJD-XV-TOV-4QJERC-1997":
            quarantine = source.get("similarSiglaQuarantineWave22", {})
            if (not isinstance(quarantine, dict)
                    or quarantine.get("officialJournal1994IndexUrl") != "https://bibleproject.huji.ac.il/textus"
                    or quarantine.get("journal1994TextSiglum") != "4QJer a"
                    or quarantine.get("journal1994ManuscriptId") != "4Q70"
                    or quarantine.get("journal1994NotTarget4Q72") is not True
                    or quarantine.get("edition1991TargetSiglum") != "4QJer c"
                    or quarantine.get("edition1991TargetManuscriptId") != "4Q72"
                    or quarantine.get("otherManuscriptId") != "4Q57"
                    or quarantine.get("otherManuscriptSiglum") != "4QIsa c"
                    or quarantine.get("otherFragmentLabel") != "55"
                    or quarantine.get("otherFragmentBookLocus") != "Isaiah 51:8–9"
                    or quarantine.get("targetFragmentLabel") != "55 ii"
                    or quarantine.get("targetFragmentBookLocus") != "Jeremiah 33:16–20"
                    or quarantine.get("originalManuscriptPhotosCompared") is not False
                    or quarantine.get("samePhysicalFragment") is not False
                    or quarantine.get("reused1994TextusPlatesAs1991Or1997Photos") is not False
                    or quarantine.get("sameEditionNumberedPlates") is not False
                    or quarantine.get("acceptedMisleadingSearchResultAsPrimary") is not False):
                errors.append(f"{prefix}: 4Q70 1994 Textus or 4Q57 Isaiah fragment55 falsely conflated with 4Q72 Jer33 fragment55ii")
        if rid == "SRC-DSS-REED-FASC7-4Q72-PAM43101":
            if (source.get("archivalPAM") != "43.101"
                    or source.get("museumPlate") != "245"
                    or source.get("criticalColumn") != "XXV"
                    or source.get("specificIAA2012Fragment6MatchedByImage") is not False):
                errors.append(f"{prefix}: inventory PAM/plate/column or photo match invented")
        if rid == "SRC-GARCIA-MARTINEZ-TIGCHELAAR-1999-STUDY-EDITION-4Q72-271272":
            if (source.get("url") != "https://ancientmodern.org/wp-content/uploads/2016/02/the_dead_sea_scrolls_study_edition_brill_1999.pdf"
                    or source.get("original1999PrintedPages") != [271, 272]
                    or source.get("webScreenshotPageIndices") != [295, 296]
                    or source.get("original1999PageScreenshotsInspected") is not True
                    or source.get("printedSecondaryManuscriptId") != "4Q72"
                    or source.get("printedSecondarySiglum") != "4QJer c"
                    or source.get("printedSecondaryJer33Column") != "XXIV"
                    or source.get("printedSecondaryJer33Verses") != "33:16–20"
                    or source.get("primaryTov1997UncertainPrecedingColumn") != "XXIV = Jer 33:?"
                    or source.get("primaryTov1997Jer33Column") != "XXV"
                    or source.get("primaryTov1997Jer33Verses") != "33:16–20"
                    or source.get("secondaryMuseumPlateAsPrinted") != "ROC 232, 244–346, 671"
                    or source.get("originalTovMuseumPlateAsPrinted") != "Mus. Inv. 232, 244, 245, 246, 671"
                    or source.get("secondaryTov1991PagesAsPrinted") != "248–276"
                    or source.get("authorUniversityAndPrimaryTov1991Pages") != "249–276"
                    or source.get("typographicErrorDefinitivelyEstablished") is not False
                    or source.get("reasonForNumberingChangeIndependentlyEstablished") is not False
                    or source.get("distinctAncientManuscriptFrom1997") is not False
                    or source.get("originalAncientPhotoPixelsInspected") is not False
                    or source.get("editorOriginalDJDPhotographicPlatesInspected") is not False
                    or source.get("photographReusePermissionGranted") is not False
                    or source.get("publicationLicensed") is not False
                    or source.get("secondarySummaryDoesNotReplaceFirstEdition") is not True
                    or source.get("accessState") != "PARTIAL_OBJECT"
                    or source.get("rightsState") != "PERMISSION_REQUIRED"):
                errors.append(f"{prefix}: 1999 Brill synopsis cannot overwrite Tov original column, plate IDs, or publication/photo HOLD")
        if rid == "SRC-IAA-B279109-PAM40963-4Q72-1954":
            if (source.get("url") != "https://www.deadseascrolls.org.il/explore-the-archive/image/B-279109"
                    or source.get("officialImageId") != "B-279109"
                    or source.get("archivePAMNumber") != "M40.963"
                    or source.get("archiveExposureDate") != "February 1954"
                    or source.get("originalPhotographer") != "Najib Anton Albina"
                    or source.get("archiveFilmKind") != "Scanned Infrared Negative"
                    or source.get("museumPlate245Listed") is not True
                    or source.get("manyManuscriptsInFrame") is not True
                    or source.get("official4Q72Listed") is not True
                    or source.get("archiveCatalogueSiglum") != "4Q Jer d"
                    or source.get("scholarly4Q72Siglum") != "4QJer c"
                    or source.get("fascicle9PassageRange") != "Jer 4:13–16; 33:16–20"
                    or source.get("langlois2019Footnote19MapsPAMToIAA") is not True
                    or source.get("accessState") != "CATALOG_ONLY"
                    or source.get("rightsState") != "PERMISSION_REQUIRED"
                    or source.get("directHistoricalNegativePixelsInspected") is not False
                    or source.get("preciseF55iiPieceIdentifiedOnNegative") is not False
                    or source.get("academic1954To2012SamePhotoOrFragmentMatchProven") is not False
                    or source.get("manuscriptLettersIndependentlyCollated") is not False
                    or source.get("criticalOriginalDJDPlateCollated") is not False
                    or source.get("imageReusePermissionGranted") is not False):
                errors.append(f"{prefix}: 1954 4Q72 PAM M40.963 negative falsely upgraded from multi-manuscript catalogue to glyph/fragment/licensed proof")
        if rid == "SRC-DSS-REED-FASC7-4Q72-PAM43101":
            historical = source.get("historicalNegative1954Crosscheck", {})
            if (not isinstance(historical, dict)
                    or historical.get("fascicle9Url") != "https://lyingpen.uia.no/dssinventoryproject/fascicle9/"
                    or historical.get("archivalNumber") != "40.963"
                    or historical.get("officialIAAId") != "B-279109"
                    or historical.get("isSameExposureAsPAM43101") is not False
                    or historical.get("preciseF55iiObjectIdentityEstablished") is not False):
                errors.append(f"{prefix}: historical mixed negative cannot be equated with 43.101 or editor fragment 55 ii")
        if rid == "SRC-LANGLOIS-JEREMIAH-4Q72-2019":
            note = source.get("historicalNegativeFootnote19", {})
            if (not isinstance(note, dict)
                    or note.get("pamNumber") != "40.963"
                    or note.get("officialIAAId") != "B-279109"
                    or note.get("originalPdfTextExtractionRead") is not True
                    or note.get("screenshotOfThisFootnoteObtained") is not False
                    or note.get("photoPixelsReviewedInOurResearch") is not False):
                errors.append(f"{prefix}: Langlois footnote 19 original PDF text cannot be promoted to viewed photo pixels")
        if rid == "SRC-IAA-B360205-4Q72-PL245F6":
            if (source.get("url") != "https://www.deadseascrolls.org.il/explore-the-archive/image/B-360205"
                    or source.get("archivePlate") != "245"
                    or source.get("fragmentOnPlate") != "6"
                    or source.get("catalogLabel") != "4Q Jer d"
                    or source.get("criticalEditionLabel") != "4QJer c"
                    or source.get("imagePixelsInspected") is not True
                    or source.get("accessState") != "PARTIAL_OBJECT"
                    or source.get("imageVisualReviewMethod") != "OFFICIAL_IAA_BROWSER_VIEWER_RENDERED_INFRARED_SCREENSHOT_AND_DOUBLECLICK_ZOOM"
                    or source.get("directImageVisualReviewOn") != "2026-11-10"
                    or source.get("originalNegativePixelsChecked") is not False
                    or source.get("scholarlyTranscriptLinesIndependentlyCollated") is not False
                    or source.get("screenshotRedistributedOrCommitted") is not False
                    or source.get("printedHebrewLettersIndependentlyCollated") is not False
                    or source.get("photoReusePermissionGranted") is not False
                    or source.get("academicDistinctManuscriptId") != "4Q72a"
                    or source.get("academicDistinctManuscriptSiglum") != "4QJer d"
                    or source.get("catalogSiglaConflictStatus") != "UNRESOLVED_METADATA_ID_SIGLUM_MISMATCH_PHOTO_VISUAL_NO_INDEPENDENT_OBJECT_MATCH"):
                errors.append(f"{prefix}: IAA archive metadata or unearned pixel/rights attestation")
        if rid == "SRC-MAIER-IECOT-JEREMIAH-1-25-2025":
            if (source.get("url") != "https://api.pageplace.de/preview/DT0400.9783170435391_A62581867/preview-9783170435391_A62581867.pdf"
                    or source.get("printedPageVisuallyVerified") != 14
                    or source.get("pdfPageIndexInspected") != 1
                    or source.get("distinctIdA") != "4Q72"
                    or source.get("distinctSiglumA") != "4QJer c"
                    or source.get("distinctIdB") != "4Q72a"
                    or source.get("distinctSiglumB") != "4QJer d"
                    or source.get("distinctManuscripts") is not True
                    or source.get("photoAutopsy") is not False):
                errors.append(f"{prefix}: 4Q72 versus 4Q72a independent scholarly manuscript identity conflated")
        if rid == "SRC-RAHLFS-JEREMIAH23-40":
            if (source.get("url") != "https://www.die-bibel.de/bibel/LXX/JER.23"
                    or source.get("additionalUrl") != "https://www.die-bibel.de/bibel/LXX/JER.40"
                    or source.get("chapterCrosswalk") != {
                        "MT_33_1_13": "LXX_JER_40_1_13",
                        "MT_33_14_26": "ABSENT_FROM_RAHLFS_HANHART_2006",
                        "MT_26_1_24": "LXX_JER_33_1_24",
                    }
                    or source.get("exactGreekNameJer23_6") != "Ιωσεδεκ"):
                errors.append(f"{prefix}: Jeremiah MT/LXX publisher crosswalk or printed Greek name drifted")

        if rid == "SRC-OFER-TEXTUS26-2016-ALEPPO-EX8-FRAGMENT":
            checked = source.get("verifiedSelectedPages20261112")
            expected = {
                "publisherOriginalPdfExposedAndOpenedInWeb": True,
                "wholePdfPageCount": 26,
                "printedTitlePage173VisuallyRead": True,
                "printedPagesVisuallyRead": [173, 179, 180, 181, 182],
                "originalPublisherPhotoReproductionsViewed": True,
                "figureNumbersViewed": [3, 4, 5, 6, 7],
                "originalPhysicalFragmentHandledByUs": False,
                "originalHebrewInkFullyIndependentGlyphCollation": False,
                "meorotNatanFirstQuestionEx8_7FrogNameFullyResolved": False,
                "meorotNatanSecondQuestionEx8_11RestorationSupportsReportedHatafPatah": True,
                "doesNotTestExodus17_16": True,
                "yeivin1968Page17QuotedByOferNotYeivinPage82": True,
                "breuer1976Pages260_261OriginallyRead": False,
                "brillImagesMayBeRepublished": False,
                "remoteDesktopAttemptWasPdf": False,
                "localPdfBytesClaimed": 0,
            }
            if (source.get("doi") != "10.1163/2589255X-02601009"
                    or source.get("accessState") != "PARTIAL_OBJECT"
                    or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                    or source.get("rightsState") != "PERMISSION_REQUIRED"
                    or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False
                    or not isinstance(checked, dict)
                    or any(checked.get(key) != value for key, value in expected.items())):
                errors.append(f"{prefix}: Ofer2016 Exodus8 surviving fragment does not prove lost Exodus17:16, Yeivin82, palaeographic autopsy or image rights")

        if rid == "SRC-WEVERS-GOTTINGEN-EXODUS-1991-AUTHOR-INTRO-EN2006":
            method = source.get("editorialMethodFacts20261112")
            expected = {
                "printedEditionYear": 1991,
                "authorEnglishTranslationYear": 2006,
                "authorEnglishTranslationDirectlyRead": True,
                "originalPrintedGreekVerseEx17_16Read": False,
                "original1991CriticalApparatusEx17_16Read": False,
                "apparatus1RecordsSubstantiveVariantsNotEveryItacism": True,
                "apparatus2GenerallyMarginalAndLaterTranslators": True,
                "aquilaSiglum": "α'",
                "symmachusSiglum": "σ'",
                "theodotionSiglum": "θ'",
                "threeGreekTranslatorsSiglum": "οἱ γ'",
                "field1875ComparedByEditor": True,
                "field1875IndependentNewPhysicalManuscript": False,
                "brookeMclean1909SameCriticalEditionAs1991": False,
                "criticalManuscriptsPersonallyCollated": False,
                "photographRightsApproved": False,
            }
            if (source.get("url") != "https://ccat.sas.upenn.edu/rak/temp/Wevers-Exod-n.html"
                or source.get("accessState") != "PARTIAL_OBJECT"
                or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                or source.get("rightsState") != "RIGHTS_UNKNOWN"
                or source.get("publicationState") != "BLOCKED"
                or source.get("criticalEditionCollated") is not False
                or not isinstance(method, dict)
                or any(method.get(key) != value for key, value in expected.items())):
                errors.append(f"{prefix}: Wevers 1991 apparatus introduction does not establish Exodus17:16 variant, Field independence or photo rights")

        if rid == "SRC-FIELD-HEXAPLA-1875-EX17-16-PRINT-P111-BSB":
            field = source.get("pageAutopsy20261112")
            expected_field = {
                "original1875PrintedPage111ImageVisuallyRead": True,
                "bsbCompleteVolumeIIIFCanvases": 920,
                "originalPageImageId": "bsb11340409_00221",
                "englishLatinThroneGloss": "Manus est super thronum Jah",
                "englishLatinAlternative": "Manus est super vexillum Jah",
                "originalPageGreekContainsKryphaia": True,
                "editorialSymmachusAttributionDefinitelyCertain": False,
                "editorExpressesSymmachusDoubtInNote17": True,
                "oldPartial207PagePDFCoveredEx17_16": False,
                "originalAncientAleppoEx17_16FolioVisuallyRead": False,
                "originalGreekCodicesIndependentlyCollated": False,
                "wevers1991Ex17_16OriginalApparatusRead": False,
                "paleographicCollationCompleted": False,
                "bsbDigitalImageRepublicationPermissionGranted": False,
            }
            if (source.get("originalPageIiifImageUrl") != "https://api.digitale-sammlungen.de/iiif/image/v2/bsb11340409_00221/full/1400,/0/default.jpg"
                or source.get("accessState") != "PARTIAL_OBJECT"
                or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                or source.get("rightsState") != "RIGHTS_UNKNOWN"
                or source.get("publicationState") != "BLOCKED"
                or source.get("criticalEditionCollated") is not False
                or not isinstance(field, dict)
                or any(field.get(key) != value for key, value in expected_field.items())):
                errors.append(f"{prefix}: Field1875 p111 cannot be promoted to Aleppo Ex17 autograph, independent Greek manuscript, Göttingen1991 apparatus or image rights")

        if rid == "SRC-KITTEL-BHK2-1909-EX17-16-P99-ORIGINAL-APP":
            kittel = source.get("pageAutopsy20261112")
            kittel_required = {
                "titlePageEditionYear": 1909,
                "editionDescriptor": "EDITIO ALTERA EMENDATIOR STEREOTYPICA",
                "titlePageSecondEditionVisuallyRead": True,
                "originalExodus17_16PagePrinted": 99,
                "pdfPageIndexZeroBased": 114,
                "pdfTotalPages": 568,
                "pdfBytes": 52339592,
                "originalPageAndApparatusVisuallyReviewed": True,
                "printedMainTextTwoWrittenWords": True,
                "apparatusNotesVariantWordDivision": True,
                "apparatusGreekKryphaiaPrinted": True,
                "allTinyApparatusSiglaDeciphered": False,
                "correctlyIdentifiedAsBHK3_1937": False,
                "originalLeningradManuscriptPixelsExamined": False,
                "originalAleppoManuscriptEx17_16Seen": False,
                "independentAncientManuscriptCollation": False,
                "fullCriticalApparatusOfBHSRead": False,
                "scanRightsIndependentlyCleared": False,
            }
            if (source.get("year") != 1909
                    or source.get("accessState") != "PARTIAL_OBJECT"
                    or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                    or source.get("rightsState") != "RIGHTS_UNKNOWN"
                    or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False
                    or not isinstance(kittel, dict)
                    or any(kittel.get(k) != v for k, v in kittel_required.items())):
                errors.append(f"{prefix}: Kittel1909 BHK2 and DBG BHS edition conflation or ancient apparatus/rights overclaim")
        if rid == "SRC-DOVI-MIQRA-MASORAH-CH3-EX17-16-COMPOSITE-EDITORIAL":
            editorial = source.get("authorEditorialMethodAudit20261113")
            expected = {
                "originalHebrewAndEnglishChapterThreeDirectlyRead": True,
                "editorDoviUserHostedWikisourceNotInstitutionalPeerReviewed": True,
                "sectionTitle": "Conjoined Words in the Torah",
                "authorEnumeratesCompositeCases": 11,
                "verse": "Exodus 17:16",
                "printedMainReadingTwoWords": "כֵּ֣ס יָ֔הּ",
                "reportedAlternativeJoinedReading": "כֵּ֣סְיָ֔הּ",
                "separateReadingAscribedToLeningrad": True,
                "separateReadingAscribedToYemeniteSephardiAshkenazi": True,
                "joinedReadingSiglum": "A(S)",
                "joinedReadingIsReportedAleppoNotExistingFolio": True,
                "editorStatesYemeniteScrollsNotDecisiveForAleppoWordJoining": True,
                "onlineTextIsPhysicalAncientManuscript": False,
                "elevenExamplesAreElevenOriginalManuscripts": False,
                "editorialSourceResolvesOr4445PhotoConflict": False,
                "lostAleppoExodus1716LeafExamined": False,
                "originalBHSAndGöttingenPrintedApparatusCollated": False,
                "independentCriticalManuscriptCollationCompleted": False,
                "externalScientificPeerReviewApproved": False,
                "textOrPhotoReuseRightsApproved": False,
                "productPublishingApproved": False,
            }
            if (source.get("accessState") != "PARTIAL_OBJECT"
                    or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                    or source.get("rightsState") != "RIGHTS_UNKNOWN"
                    or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False
                    or not isinstance(editorial, dict)
                    or any(editorial.get(k) != v for k, v in expected.items())):
                errors.append(f"{prefix}: Dovi editorial masorah cannot become Aleppo autopsy, extra codices, Or4445 collation, external signoff or publication right")
        if rid == "SRC-BL-OR4445-F59V-EX17-16-OPENN-IMAGE-UNRESOLVED":
            folio = source.get("originalFacsimileCrosscheck20261113")
            expected = {
                "originalAncientHebrewManuscript": "British Library Or 4445",
                "coreDateRange": "920–950 CE",
                "originalCoreNotLater1540Replacement": True,
                "originalFolio": "59v",
                "opennOriginalImageId": "13291_0125.jpg",
                "originalMasterJPEGIdentified": True,
                "opennIndexPhotographicFolioLabelVerified": True,
                "bibliographicExodusRange42rTo85rVerified": True,
                "manuscriptSectionAscribedToExodus17_16BySecondaryTable": True,
                "secondaryComparisonClaimsJoinedOneWord": True,
                "machineBrowserImageReadingClaimsTwoSeparateWords": True,
                "conflictResolvedByIndependentAutopsy": False,
                "finalOriginalWordDivision": "UNRESOLVED_CONFLICT",
                "nativePixelOriginalGlyphAndSpacingCollationCompleted": False,
                "originalMasorahMarginaliaDecoded": False,
                "comparativeTableIsAdditionalPhysicalManuscript": False,
                "sameManuscriptAsLeningradB19a": False,
                "sameManuscriptAsMissingAleppoLeaf": False,
                "criticalManuscriptCollationCompleted": False,
                "publicReplicaOrPhotoRightsCleared": False,
                "independentScientificPeerApproval": False,
                "productPublishingApproval": False,
            }
            if (source.get("accessState") != "PARTIAL_OBJECT"
                    or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                    or source.get("rightsState") != "RIGHTS_UNKNOWN"
                    or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False
                    or not isinstance(folio, dict)
                    or any(folio.get(k) != v for k, v in expected.items())):
                errors.append(f"{prefix}: Or 4445 f59v image conflict cannot be upgraded to manuscript reading, independent collation or rights approval")
        if rid == "SRC-LENINGRAD-B19A-F042A-EX17-16-WSRP-FACSIMILE":
            image = source.get("originalPhotoAndTranscriptAudit20261113")
            required = {
                "originalManuscriptIsLeningradNotAleppo": True,
                "exactFolioNumber": "042a",
                "traditionalPageSide": "42r",
                "manuscriptHoldingShelfmark": "RNL Firkovich Evr I B 19a",
                "biblicalRange": "Exodus 17:11–18:19",
                "commonsOriginalPhotoAccessible": True,
                "commonsOriginalImageWidthPx": 4090,
                "commonsOriginalImageHeightPx": 4514,
                "westSemiticResearchProjectInstitutionalPhotoProvenanceConfirmed": True,
                "independentSourceTEIColumnNumber": 1,
                "independentSourceTEILineEndKees": 15,
                "independentSourceTEILineStartYah": 16,
                "TEIEditorTextReportsTwoDistinctUnits": True,
                "digitalTextIsASeparatePhysicalHebrewManuscript": False,
                "imageViewedInBrowser": True,
                "nativePixelEnlargementAndIndividualGlyphCollationCompleted": False,
                "masoreticMarginaliaFullyDeciphered": False,
                "fullAncientCriticalCollationCompleted": False,
                "aleppoEx17LostLeafSeen": False,
                "otherAncientHebrewManuscriptIndependentlyCollated": False,
                "completeBHSAndGöttingenPrintedApparatusRead": False,
                "originalYeivinAndBreuerTargetPagesRead": False,
                "digitalPhotoRepublicationPermissionFullyCleared": False,
                "independentExternalScholarlyReviewPassed": False,
                "productPublicationApproved": False,
            }
            if (source.get("accessState") != "PARTIAL_OBJECT"
                    or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                    or source.get("rightsState") != "RIGHTS_UNKNOWN"
                    or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False
                    or not isinstance(image, dict)
                    or any(image.get(k) != v for k, v in required.items())):
                errors.append(f"{prefix}: Leningrad B19a photo and third-party line map must not become Aleppo, autopsy, second witness or rights approval")
        if rid == "SRC-MGKETER-BIU-COHEN-EX17-16-ONLINE-ONE-WORD":
            edited = source.get("publisherPageAudit20261113")
            expected = {
                "projectOfficialSiteDirectlyRead": True,
                "editorMenahemCohenNamedByProject": True,
                "mainBibleVerseLocator": "Exodus 17:16",
                "mainTextUnpointedJoinedHebrew": "כסיה",
                "mainTextOneWrittenWord": True,
                "fourMainBibleTextModesJoined": True,
                "editorProjectAcknowledgesReconstructingMissingAleppoPortions": True,
                "originalAleppoEx17_16FolioSurvivesInDigitalDisplay": False,
                "underlyingAncientAleppoFolioAutopticallyExamined": False,
                "independentPhysicalManuscriptCollationCompleted": False,
                "criticallyDecipheredOriginalBHSApparatus": False,
                "criticallyDecipheredGöttingenEx17_16Apparatus": False,
                "modernBhsPublisherPrintsSameOneWord": False,
                "medievalCommentaryQuotationUsedAsMainVerse": False,
                "permissionToRepublishDigitalEditionOrImagesGranted": False,
                "externalScholarlySignoffGranted": False,
                "productPublicationApproved": False,
            }
            if (source.get("accessState") != "PARTIAL_OBJECT"
                    or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                    or source.get("rightsState") != "PERMISSION_REQUIRED"
                    or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False
                    or not isinstance(edited, dict)
                    or any(edited.get(k) != v for k, v in expected.items())):
                errors.append(f"{prefix}: BIU HaKeter one-word modern edition falsely promoted to ancient Aleppo, BHS apparatus or publication rights")
        if rid == "SRC-DBG-BHS-EX17-16-PUBLISHER-TEXT":
            bhs = source.get("publisherPageCheck20261112")
            bhs_required = {
                "publisherOriginalOnlineChapterDirectlyRead": True,
                "publisherTitle": "Biblia Hebraica Stuttgartensia",
                "onlineReducedView": True,
                "editionCreditIncludes1977And1997": True,
                "originalVerseLocator": "Exodus 17:16",
                "mainTextWordDivisionTwoWords": True,
                "mainTextThroneWordHebrew": "כֵּס",
                "mainTextYahWordHebrew": "יָהּ",
                "originalPrintedCriticalApparatusOnSiteVisible": False,
                "originalLeningradPixelsChecked": False,
                "originalAleppoEx17_16FolioInspected": False,
                "criticalManuscriptCollationCompleted": False,
                "rightsForProductPublicationGranted": False,
            }
            if (source.get("url") != "https://www.die-bibel.de/bibel/BHS/EXO.17"
                    or source.get("accessState") != "PARTIAL_OBJECT"
                    or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                    or source.get("rightsState") != "PERMISSION_REQUIRED"
                    or source.get("publicationState") != "BLOCKED"
                    or source.get("criticalEditionCollated") is not False
                    or not isinstance(bhs, dict)
                    or any(bhs.get(k) != v for k, v in bhs_required.items())):
                errors.append(f"{prefix}: DBG BHS Ex17 reduced publisher verse text is not critical apparatus or ancient manuscript permission")

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
        if source.get("rightsState") == "PUBLICATION_ELIGIBLE" and rid not in {"SRC-KRUGER-SHADDAY-JOB-2023-CONTEXT-CRITIQUE", "SRC-VANWOLDE-2021", "SRC-TR1550-REV18", "SRC-SBLGNT-CCBY-LICENSE", "SRC-CAMBRIDGE-GOD-PRONOUNS", "SRC-SUCHARD-ELOHIM-2025", *DEIR_ALLA_VISUAL_LICENSE_GUARDS}:
            errors.append(f"{prefix}: evidence of a source-level license missing")
        if rid in {
            "SRC-CLEMENT-STROMATA-5-6-34-STAHLIN-GREEK",
            "SRC-DEISSMANN-BIBLE-STUDIES-1901-TETRAGRAM-GREEK",
            "SRC-ROMER-COLLEGE-DE-FRANCE-YHWH-2011",
        }:
            if (source.get("accessState") != "PARTIAL_OBJECT"
                or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                or source.get("publicationState") != "BLOCKED"
                or source.get("criticalEditionCollated") is not False):
                errors.append(f"{prefix}: ancient-name Greek transmission witness cannot become a certified manuscript collation or publication")
        if rid == "SRC-CLEMENT-STROMATA-5-6-34-STAHLIN-GREEK":
            clement = source.get("greekPassageWitness20261109")
            if (not isinstance(clement, dict)
                or clement.get("printedEditedForm") != "Ἰαουε"
                or clement.get("exactLoc") != "STROMATA_V_6_34_STAHLIN_VOL2_PP348_349"
                or clement.get("digitalTextDirectlyRead") is not True
                or any(clement.get(flag) is not False for flag in (
                    "originalPrintedApparatusRead",
                    "ancientManuscriptsCollated",
                    "historicalPronunciationUncontested"))):
                errors.append(f"{prefix}: Clement digital Stählin Greek text must not become an ancient autograph or undisputed phonetic witness")
        if rid == "SRC-DEISSMANN-BIBLE-STUDIES-1901-TETRAGRAM-GREEK":
            if (source.get("variantScope20261109") != "DEISSMANN1901_REPORTS_CLEMENT_DINDORF_IAOU_VARIANT_IA_OUAI_IA_OUE_LAGARDE_PREFERRED_IAOUE_OUR_MANUSCRIPT_APPARATUS_NOT_READ"
                or source.get("greekManuscriptsDirectlyCollated") is not False
                or source.get("modernCriticalApparatusInspected") is not False):
                errors.append(f"{prefix}: Deissmann's dated variant report is not direct Greek manuscript or modern apparatus inspection")
        if rid == "SRC-ROMER-COLLEGE-DE-FRANCE-YHWH-2011":
            romer = source.get("reportedAcademicWitness20261109")
            if (not isinstance(romer, dict)
                or romer.get("clement") != "STROMATA_5_6_34_IAOUE"
                or romer.get("theodoretQuestions") != "QUESTIONS_ON_EXODUS_XV_SAMARITAN_IABE_JEWISH_AIA"
                or romer.get("theodoretCompendium") != "HERETICAL_FABLES_V_3_SAMARITAN_IABAI_DISTINCT_TEXT"
                or romer.get("papyrus") != "4Q120_EDITORIAL_FRAG20_LEV4_26_28_IAO"
                or romer.get("slidesTextDirectlyRead") is not True
                or romer.get("pdfPageScreenshotVisuallyVerified") is not True
                or any(romer.get(flag) is not False for flag in (
                    "originalPatristicGreekEditionsCollated",
                    "originalDjdCriticalEditionCollated"))
                or not isinstance(romer.get("pdfPageImageCrosscheck20261109"), dict)
                or romer["pdfPageImageCrosscheck20261109"].get("zeroBasedPdfPageIndices") != [5, 6]
                or romer["pdfPageImageCrosscheck20261109"].get("printedSlideNumbers") != [11, 12, 13, 14]
                or romer["pdfPageImageCrosscheck20261109"].get("visuallyReadGreek") is not True
                or romer["pdfPageImageCrosscheck20261109"].get("figureOrManuscriptAutopsy") is not False):
                errors.append(f"{prefix}: Römer 2011 lecture cannot merge Theodoret works or certify Greek original editions, DJD or screenshots")
        if rid in {
            "SRC-THEODORET-EXODUM-15-PG80-243-GREEK",
            "SRC-THEODORET-COMPENDIUM-V3-PG83-460-GREEK",
            "SRC-KINZIG-PATRISTIC-TETRAGRAM-2008-P226227",
        }:
            if (source.get("accessState") != "PARTIAL_OBJECT"
                or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                or source.get("publicationState") != "BLOCKED"
                or source.get("criticalEditionCollated") is not False):
                errors.append(f"{prefix}: Theodoret and Kinzig witnesses remain partial printed-source evidence with publication HOLD")
        if rid == "SRC-THEODORET-EXODUM-15-PG80-243-GREEK":
            w = source.get("greekSourceWitness20261109")
            if (not isinstance(w, dict)
                or w.get("greekSamForm") != "Ἰαβὲ"
                or w.get("passage") != "QUAESTIONES_EXODUM_15_PG80_COL243"
                or w.get("digitalTextEndsExactly") != "Ἰουδαῖοι δὲ"
                or w.get("digitalGreekDirectRead") is not True
                or any(w.get(flag) is not False for flag in (
                    "jewishReadingVisibleInThisDigitalExcerpt",
                    "printedMigneCriticalApparatusCollated",
                    "manuscriptPhotoAutopsied",
                    "historicalPronunciationCertain"))):
                errors.append(f"{prefix}: truncated Theodoret Exodum Greek cannot prove unseen Jewish vowel form or manuscript collation")
        if rid == "SRC-THEODORET-EXODUM-15-PG80-243-GREEK":
            alt = source.get("alternateGreekTranscription2006")
            if (not isinstance(alt, dict)
                or alt.get("url") != "https://www.matia.gr/pisth/pdf/pg_migne/Theodoretus_of_Cyrrhus_PG_80-84/Quaestiones_in_Octateuchum.pdf"
                or alt.get("loc") != "QUAESTIONES_EXODUM_XV_PDF_TRANSCRIPTION_FOOTER41_LINES2504_2512"
                or alt.get("samaritan") != "Ἰαβέ"
                or alt.get("jewish") != "Ἰά"
                or alt.get("textOnlyDirectlyRead") is not True
                or any(alt.get(flag) is not False for flag in (
                    "pageScreenshotVisuallyInspected",
                    "modernCriticalApparatusCollated",
                    "ancientManuscriptsCollated",
                    "jewishFormUncontested"))):
                errors.append(f"{prefix}: alternate Theodoret 2006 transcript not apparatus or ancient autopsy")
        if rid == "SRC-THEODORET-EXODUM-15-PG80-243-GREEK":
            ed = source.get("criticalEditionAcquisition20261109")
            first = ed.get("firstCriticalEdition1979") if isinstance(ed, dict) else None
            later = ed.get("revisedGreekEdition2007") if isinstance(ed, dict) else None
            if (not isinstance(first, dict) or not isinstance(later, dict)
                or first.get("reviewScope") != "GAUTIER_1980_P293_SECONDARY_REPORT_53_CONSULTED_31_SELECTED_NO_STEMMA"
                or first.get("directCriticalApparatusRead") is not False
                or first.get("q15VariantIndependentlyEstablished") is not False
                or later.get("volume") != 1
                or later.get("exodusPrintedPageRange") != [222, 345]
                or later.get("institutionalFullTextAccessObtained") is not False
                or later.get("actualQ15GreekTextOrVariantNotesRead") is not False
                or later.get("ancientManuscriptsIndependentlyCollated") is not False):
                errors.append(f"{prefix}: 1979 review and 2007 catalogue are not direct Theodoret QXV critical collation")
        if rid == "SRC-THEODORET-COMPENDIUM-V3-PG83-460-GREEK":
            w = source.get("greekCompendiumWitness20261109")
            if (not isinstance(w, dict)
                or w.get("loc") != "COMPENDIUM_V3_PG83_COL460A"
                or w.get("sam") != "Ἰαβαὶ"
                or w.get("patristicShaddaiForm") != "Σαδδαῒ"
                or w.get("theodoretGloss") != "τὸν ἱκανὸν καὶ δυνατὸν"
                or w.get("jewishForm") != "Ἀϊὰ"
                or w.get("sourceGreekTextDirectRead") is not True
                or any(w.get(flag) is not False for flag in (
                    "hebrewEtymologyIndependentlyEstablished",
                    "patristicManuscriptVariantsCollated",
                    "originalAncientPlasterAutopsied",
                    "publicationRightsGranted"))):
                errors.append(f"{prefix}: Theodoret Compendium gives historical Shaddai gloss, not independently proven Hebrew etymology")
        if rid == "SRC-KINZIG-PATRISTIC-TETRAGRAM-2008-P226227":
            w = source.get("kinzigWitness20261109")
            if (not isinstance(w, dict)
                or w.get("bib") != "KINZIG_2008_SPRACHGEWINN_PP202_233"
                or w.get("exodusPrintPage") != 226
                or w.get("exodusScreenPdfPageZeroBased") != 24
                or w.get("exodusPageScreenshotDirectlyInspected") is not True
                or w.get("otherPage227TextDirectlyRead") is not True
                or w.get("otherPage227ScreenshotSuccessful") is not False
                or w.get("jewishVariantPrinted") != "Ἰά"
                or w.get("jewishVariantWide") != "Αἰά"
                or w.get("jewishVariantOther") != "αεια"
                or any(w.get(flag) is not False for flag in (
                    "printedGreekEditionManuscriptsIndependentlyCollated",
                    "modernAuthorClaimsUniversalCertainty"))
                or not isinstance(source.get("authorConclusion20261109"), dict)
                or source["authorConclusion20261109"].get("originalPublishedPageLoci") != [232, 233]
                or source["authorConclusion20261109"].get("exactSection") != "8. Ergebnisse und Fragen"
                or source["authorConclusion20261109"].get("originalGermanTextRead") is not True
                or source["authorConclusion20261109"].get("thesePagesScreenshotVisuallyVerified") is not False
                or source["authorConclusion20261109"].get("tentativePreference") != "Jaho"
                or source["authorConclusion20261109"].get("qualifiedPreferenceWithinPatristicEvidence") is not True
                or source["authorConclusion20261109"].get("reportsGreatChurchYahwehVersusGnosticJahoAssignment") is not False
                or any(source["authorConclusion20261109"].get(flag) is not False for flag in (
                    "saysAncientOriginalPronunciationCertain",
                    "modernScholarlyConsensusCertified"))):
                errors.append(f"{prefix}: Kinzig reports variant critical edition witnesses, not our autopsy or certain original pronunciation")
        if rid == "SRC-LEMAIRE-DEIRALLA-SCRIBAL-2021":
            if (source.get("hypothesisStatus") != "ATTRIBUTED_COPY_AND_9TH_10TH_CENTURY_COMPOSITION_NOT_INDEPENDENTLY_ATTESTED"
                or source.get("datingScope") != "LEMAIRE_PROPOSES_EARLY_8TH_WALL_TEXT_HEINTZ_1980_REPORTS_DIFFERENT_CIRCA_700_PALEOGRAPHIC_ESTIMATE_DISPUTED"):
                errors.append(f"{prefix}: Lemaire 2021 historical copy/dating claim falsely promoted")
        if rid == "SRC-HACKETT-DEIRALLA-FIRSTHAND-1986":
            if (source.get("hypothesisStatus") != "HACKETT_1986_SHDYN_SHEDIM_REVOCALIZATION_ATTRIBUTED_AND_1991_CONTESTED_NOT_ESTABLISHED"
                or source.get("autopsyBoundary") != "HACKETT_1979_1981_DIRECT_MUSEUM_EXAMINATION_NOT_OUR_INDEPENDENT_PLASTER_OR_1976_EDITION_COLLATION"):
                errors.append(f"{prefix}: Hackett 1986 scholarly hypothesis or firsthand material scope overclaimed")
        if rid == "SRC-LEMAIRE-REVIEW-HACKETT-1984-P142":
            if (source.get("comparisonScope") != "SPECIFIC_FRAGMENT_INK_DATING_OBJECTIONS_IN_LEMAIRE1984_PRINT_P142_NOT_FINAL_VERDICT"
                or source.get("autopsyBoundary") != "LEMAIRE_CITES_OWN_EPIGRAPHIC_INSPECTION_OUR_ACCESS_ONE_ARCHIVED_REVIEW_PAGE_NOT_PLASTER"):
                errors.append(f"{prefix}: Lemaire 1984 one-page source scope, fragment dispute or autopsy falsely promoted")
        if rid == "SRC-ADAJ1979-IBRAHIM-VANDERKOOIJ-PHASEIX":
            if (source.get("datingScope") != "ADAJ1979_PHASE_IX_PROBABLY_EIGHTH_BCE_PRELIMINARY_ARTIFACTS_C14_PENDING_AT_1979"
                or source.get("imageScope") != "OFFICIAL_PDF_PARSED_PP49_50_WEB_SCREENSHOT_HTTP502_NO_INDEPENDENT_VISUAL_VALIDATION"):
                errors.append(f"{prefix}: ADAJ1979 provisional phase dating, pending C14 or PDF visual scope falsely promoted")
        if rid == "SRC-LEMAIRE-DEIRALLA-1985-RADIOCARBON-PP271272":
            if (source.get("carbonScope") != "LEMAIRE1985_ATTRIBUTED_PRIOR_1976_P16_C14_CIRCA800_MARGIN70_PROBABILITY66_NOT_PRIMARY_SAMPLE_REVIEW"
                or source.get("earthquakeScope") != "LEMAIRE1985_AMOS1_1_EARTHQUAKE_SPECULATIVE_NOT_EVIDENCED_IDENTITY"):
                errors.append(f"{prefix}: Lemaire 1985 radiocarbon provenance or Amos-earthquake conjecture falsely promoted")
        if rid == "SRC-ADAJ1986-IBRAHIM-VANDERKOOIJ-2C14-P142":
            if (source.get("carbonScope") != "ADAJ1986_SAMPLES_GRN5633_2690PM60_BP_GRN8119_2590PM70_BP_770_880_BCE_HISTORIC_CALIBRATION_NOT_MODERN_EXACT_INSCRIPTION_DATE"
                or source.get("functionScope") != "ADAJ1986_NO_CLEAR_SANCTUARY_FUNCTION_TRADE_LIVING_AND_RELIGIOUS_HYPOTHESES_OPEN"
                or source.get("imageScope") != "ADAJ1986_ORIGINAL_PAGES137_AND142_SCREENSHOTS_VERIFIED_NOT_ALL_ARTIFACT_PLATES"):
                errors.append(f"{prefix}: ADAJ1986 original radiocarbon calibration, room function or screenshot scope falsely promoted")
        if rid == "SRC-WEINSTEIN-1984-DEIRALLA-C14-CONFLICT-P351":
            if (source.get("discrepancyScope") != "VERIFIED_1984_P351_GRN5283_2690PM60_PIT_GRN5633_2600PM50_DESTRUCTION_VS_1986_P142_GRN5633_2690PM60_UNRESOLVED"
                or source.get("laboratorySourceAccess") != "VOGEL_WATERBOLK_1972_R14_P53_CAMBRIDGE_ORIGINAL_PDF_TEXT_READ_SCREENSHOT_NOT_VERIFIED"):
                errors.append(f"{prefix}: GrN-5283/5633 source conflict or 1972 laboratory-access boundary falsely resolved")
        if rid == "SRC-DEIRALLA-HOFTIJZER-VANDERKOOIJ-1976-CONTENTS":
            if source.get("p16EvidenceScope") != "SECONDARY_EXCERPT_FRANKEN1976_P16_BB303_GRN5633_2600PM50_NOT_ORIGINAL_FACSIMILE":
                errors.append(f"{prefix}: Franken 1976 p16 secondary quotation promoted to original facsimile")
        if rid == "SRC-WEINSTEIN-1984-DEIRALLA-C14-CONFLICT-P351":
            if source.get("crossPublicationTriangulation") != "1972_LAB_P53_DIRECT_GRN5633_2600PM50_MATCHES_WEINSTEIN1984_P351_AND_SECONDARY_FRANKEN1976_P16_VS_1986_P142_GRN5633_2690PM60_CAUSE_UNRESOLVED":
                errors.append(f"{prefix}: Weinstein/Franken/1986 C14 corroboration and disagreement falsely resolved")
        if rid == "SRC-VOGEL-WATERBOLK-1972-GRONINGEN-DEIRALLA-P53":
            if source.get("labPair") != "ORIGINAL_1972_P53_GRN5283_B433A_2690PM60_PIT_GRN5633_BB303_2600PM50_CHARRED_GRAIN":
                errors.append(f"{prefix}: 1972 original lab GrN-5283/5633 sample-ID and radiocarbon measurements wrongly reassigned")
            if source.get("imageScope") != "CAMBRIDGE_ORIGINAL_1972_FULL_PDF_TEXT_P53_READ_WEB_SCREENSHOT_UNAVAILABLE_NOT_PHOTO_CROSSCHECKED":
                errors.append(f"{prefix}: 1972 Cambridge PDF original reading falsely promoted to screenshot visual proof")
            if source.get("religionScope") != "1972_LAB_LIST_TEMPLE_ANNEXES_AS_CONTEMPORARY_SITE_INTERPRETATION_NOT_PROVEN_1986":
                errors.append(f"{prefix}: 1972 lab cultic-context language falsely declared a proven temple")
        if rid == "SRC-ADAJ1986-IBRAHIM-VANDERKOOIJ-2C14-P142":
            if source.get("original1972LabDiscrepancy") != "1972_PRIMARY_P53_GRN5633_2600PM50_VS_1986_P142_SAME_ID_2690PM60_UNEXPLAINED":
                errors.append(f"{prefix}: 1986 conflicting GrN5633 sample age falsely corrected without a published erratum")
        if rid == "SRC-CAQUOT-LEMAIRE-DEIRALLA-REASSEMBLY-1977-P193198":
            if source.get("lineMappingScope") != "CAQUOT_LEMAIRE_1977_LINE6_SDYN_CORRESPONDS_1976_LINE8_AFTER_REASSEMBLY":
                errors.append(f"{prefix}: Caquot Lemaire 1977 vs 1976 line-6/line-8 concordance misrepresented")
            if source.get("lexicalDistinctionScope") != "SDYN_AS_ATTRIBUTED_PLURAL_TITLE_SADDAY_VS_DIFFERENT_BIRD_SDH_1977_LINE8":
                errors.append(f"{prefix}: distinct sdyn divine plural and sdh bird reading conflated")
            if source.get("originalScope") != "PUBLISHED_1977_AUTHOR_TEXT_P193_TO198_DIRECTLY_READ_AS_PERSEE_HTML_NOT_ORIGINAL_1976_P173_OR_PLATES_NOT_IMAGE_COLLATION":
                errors.append(f"{prefix}: original 1977 published text confused with inaccessible 1976 photos/autograph")
        if rid == "SRC-HACKETT-DEIRALLA-MONOGRAPH-1984-SELECTED-OCR":
            if (source.get("verificationBoundary") != "SELECTED_1984_MONOGRAPH_PP21_25_29_39_41_85_89_THIRD_PARTY_OCR_ONLY_NOT_PUBLISHER_FACSIMILE_OR_PLASTER_AUTOPSY"
                or source.get("hypothesisBoundary") != "HACKETT_VOCALIZES_SDYN_FROM_BIBLICAL_SHADDAY_HER_INTERPRETATION_NOT_ANCIENT_VOWELS_OR_PROVEN_SHEDIM_ETYMOLGY"):
                errors.append(f"{prefix}: Hackett 1984 partial third-party OCR or hypothetical vocalization overclaimed")
        if rid == "SRC-ELLIFF-COLEMAN-DEIRALLA-I6-2023":
            if (source.get("comparisonBoundary") != "PUBLISHER_ABSTRACT_CONFIRMS_CONTESTED_SHAMASH_TPRY_FASTEN_PROPOSAL_NOT_ACCEPTED_CONSENSUS"
                or source.get("original1976Boundary") != "1976_P173_CITED_SECONDHAND_IN_2023_THIRD_PARTY_OCR_NOT_DIRECT_ORIGINAL_1976_TRANSCRIPTION_OR_33_PLATES"):
                errors.append(f"{prefix}: Elliff Coleman 2023 I.6 hypothesis or original 1976 access overstated")
        if rid == "SRC-DEIRALLA-SYMPOSIUM-1991-NYU":
            if source.get("exact1991SourceScope") != "NYU_1991_BRILL_ORIGINAL_SCHOLARLY_SCAN_SELECTED_PRINT_PAGES_HACKETT_76_77_80_81_HOFTIJZER_121_122_135_137_WEIPPERT_169_170_176_OCR_NO_SCREENSHOT":
                errors.append(f"{prefix}: 1991 symposium selected-page text scope or image proof overclaimed")
            if source.get("lineConcordance1991") != "HOFTIJZER_1991_PRINT_P121_NOTE_EDITIO_PRINCEPS_I8_CAQUOT_LEMAIRE1977_I6_BRACKETED_NOT_TWO_WITNESSES":
                errors.append(f"{prefix}: original Hoftijzer 1991 1976/1977 line concordance conflated")
            if source.get("scholarshipBoundary1991") != "WEIPPERT1991_P170_REJECTS_HACKETT_SHEDIM_REVOCALIZATION_P176_DIRECT_NUMBERS_DEPENDENCE_AMBIGUOUS_HACKETT_P80_81_DOES_NOT_PROVE_ANCIENT_SCROLL":
                errors.append(f"{prefix}: 1991 scholarly dispute on shedim and ancient scroll falsely resolved")
            if source.get("visualAutopsy1991") != "1991_FULL_NYU_PDF_CRAWLER_TEXT_ONLY_48MB_WEB_SCREENSHOT_FAILED_1976_P173_AND_33_PLATES_NOT_COLLATED":
                errors.append(f"{prefix}: 1991 text-only OCR promoted to ancient plate/image autopsy")
        if rid == "SRC-BLUM-DEIRALLA-RECONSTRUCTION-2016-METATEXTE":
            if source.get("blumAccessScope2016") != "ORIGINAL_2016_DEGRUYTER_BOOK_SELECTED_PRINT_P24_26_35_36_44_45_TEXT_OCR_IMAGE_SCREENSHOT_FAILED_NOT_1976_P173_33_PLATES":
                errors.append(f"{prefix}: Blum 2016 original printed-page OCR cannot become 1976 palaeographic autopsy")
            if source.get("blumShdynBoundary2016") != "SHDYN_HOHE_ERHABENE_GLOSS_CONTEXTUALLY_INFERRED_FOOTNOTE97_NOT_ESTABLISHED_ANCIENT_VOWELS_OR_BIBLICAL_EL_SHADDAY_IDENTITY":
                errors.append(f"{prefix}: Blum 2016 contextual šdyn gloss cannot become ancient vowels or El Shadday identity")
            if source.get("blumCouncilBoundary2016") != "BLUM2016_FOOTNOTE94_FUNCTIONAL_MESSENGERS_VS_SHDYN_COUNCIL_NOT_LEVINE_HOSTILE_GROUPS_OR_HACKETT_CONSENSUS":
                errors.append(f"{prefix}: Blum 2016 functional messenger and council distinction cannot become hostile groups or consensus")
            if source.get("blumSkyBoundary2016") != "BLUM2016_P45_FEMALE_SUN_DEITY_CLOUD_OBSTRUCTED_HEAVEN_SLUCES_DISTINCT_FROM_HOFTIJZER1991_AND_ELLIFF_COLEMAN2023_PROPOSALS":
                errors.append(f"{prefix}: Blum 2016 sun goddess sky-sluices cannot be conflated with rival tpry reconstructions")
        if rid == "SRC-PATEL-WILSONWRIGHT-DEIRALLA-DIALECT-SBL2015":
            if source.get("patElLanguageBoundary2015") != "SBL2015_PRINT_P13_TO24_CANAANITE_AUTHOR_ARGUMENT_RELATIVE_ASH_AND_ABSOLUTE_VS_CONSTRUCT_INFINITIVES_VS_ALTERNATIVE_FOUR_WAYS_NO_CONSENSUS":
                errors.append(f"{prefix}: SBL 2015 Canaanite author case incorrectly promoted to academic consensus or god-name identity")
            if source.get("patElOriginalEvidenceScope2015") != "ORIGINAL_SBL_PRESS_2015_OA_PDF_CHAPTER_PRINT_P13_24_TEXT_READ_SCREENSHOT_403_NO_ANCIENT_PLASTER_PHOTOCOLLATION":
                errors.append(f"{prefix}: SBL 2015 original page text falsely promoted to original 1976 autopsy")
        if rid == "SRC-DEIRALLA-HOFTIJZER-VANDERKOOIJ-1976-CONTENTS":
            if source.get("original1976AcquisitionScope") != "1976_P173_178_PLUS_P179_182_AND_RELEVANT_PHOTO_P3_REASSEMBLY_DRAWING_P29_PRIORITY_SECONDARY_LOCATOR_ONLY_NO_PDF_OR_PLATE_IMAGES_READ" or source.get("original1976AccessBoundary") != "BRILL1976_ORIGINAL_FRONT_MATTER_ONLY_REPRINT2023_LIMITED_PREVIEW_1976_BODY_173_178_AND_PL3_29_NOT_ACCESSED":
                errors.append(f"{prefix}: Brill 1976 front matter and secondary plate locators cannot be treated as original 1976 body/plates autopsy")
        if rid == "SRC-DEIRALLA-HOFTIJZER-VANDERKOOIJ-1976-CONTENTS":
            if source.get("original1976PlateCatalogScope") != "ORIGINAL_BRILL1976_PUBLISHER_PLATE_LIST_DIRECT_TEXT_PL1_I_A_COLOR_PL2_I_C_COLOR_PL3_I_D_COLOR_PL9_I_A_I_C_PARTS_PL10_I_D_PARTS_PL27_28_SIGN_DRAWINGS_PL29_COMBINATION_I_DRAWING":
                errors.append(f"{prefix}: 1976 published plate catalogue cannot be replaced with invented photograph assignments")
            if source.get("original1976PlateCatalogImageAccess") != "FRONT2_PDF_ORIGINAL_TEXT_ONLY_SCREENSHOT_403_PLATE_IMAGES_AND_1976_P173_NOT_SEEN_NO_PALAEOGRAPHIC_COLLATION":
                errors.append(f"{prefix}: 1976 original textual plate index cannot imply visual plate/p173 collation")
            if source.get("original1976Plate29IndependenceBoundary") != "PLATE29_IS_EDITORIAL_DRAWING_NOT_ORIGINAL_PHOTOGRAPH_PLATE3_IS_COLOR_FRAGMENT_I_D_IMAGE_SECONDARY_UCLA_FIG8_3_NOT_SECOND_INDEPENDENT_WITNESS":
                errors.append(f"{prefix}: Plate29 original editorial drawing and UCLA copy cannot become independent photographs")
        if rid == "SRC-DANS-TELL-DEIRALLA-SLIDES-ARCHIVE-XS5-KPQN":
            if source.get("archiveDatasetIdentityBoundary") != "DANS_ARCHIVE_SLIDES_DATASET_10_17026_DANS_XS5_KPQN_1960_2009_FIELDWORK_CONTAINS_NO_VERIFIED_LIST_OF_1967_BALAAM_FRAGMENT_FILES":
                errors.append(f"{prefix}: DANS excavation Slides dataset cannot become direct 1967 Balaam inscription image evidence")
            if source.get("archiveFileAccessBoundary") != "DANS_OFFICIAL_DATAVERSE_API_SLIDES_NEGATIVES_PAPER_THREE_COMPLETE_FILE_METADATA_MANIFESTS_READ_NO_INDIVIDUAL_IMAGE_BYTES_OR_1976_PLATES_NO_VERIFIED_RIGHTS":
                errors.append(f"{prefix}: DANS catalog level CC BY4/metadata cannot become exact image file or 1976 plate license")
            if source.get("archiveCollectionSeparationBoundary") != "DANS_SLIDES_XS5_KPQN_DISTINCT_FROM_PAPER_ARCHIVE_X4N_WKHU_AND_FROM_BRILL_1976_FRONT2_AND_P29_DRAWING":
                errors.append(f"{prefix}: DANS Slides, Paper Archive and Brill drawing must stay separate objects")
        if rid == "SRC-DANS-TELL-DEIRALLA-SLIDES-ARCHIVE-XS5-KPQN":
            if source.get("archiveSlidesManifestEvidence") != "DANS_OFFICIAL_2026_DATAVERSE_PUBLISHED_SLIDES_MANIFEST_2560_FILES_DIRECTORY_YEARS_1978_TO_2004_NO_1967_LABELS_OR_BALAAM_PLASTER_FILENAMES":
                errors.append(f"{prefix}: DANS slides 1960-2009 dataset abstract is not a 1967 file inventory")
            if source.get("archiveNegativesManifestEvidence") != "DANS_OFFICIAL_2026_DATAVERSE_PUBLISHED_NEGATIVES_MANIFEST_4012_FILES_EARLIEST_LABELLED_1976_NO_1967_BALAAM_INSCRIPTION_FILENAME_OR_DIRECTORY":
                errors.append(f"{prefix}: DANS negatives 1976+ must not be described as original 1967 field negatives")
            if source.get("archivePaperManifestEvidence") != "DANS_OFFICIAL_2026_DATAVERSE_PUBLISHED_PAPER_MANIFEST_1389_FILES_EARLIEST_LABELLED_1976_ONE_1996_PDF_FILENAME_1967SECTIONS_DOES_NOT_PROVE_ORIGINAL_1967_IMAGE":
                errors.append(f"{prefix}: DANS 1996 paper filename containing 1967 is not a 1967 photograph")
            if source.get("archiveHistoricCustodyNotCurrentProof") != "DANS_HISTORICAL_2019_METADATA_1960_1967_SUBARCHIVE_AT_LEIDEN_UNIVERSITY_PLANNED_TRANSFER_RMO_NOT_VERIFIED_2026_TRANSFER_RMO_2011_OBJECTS_NOT_FIELD_PHOTO_PROOF":
                errors.append(f"{prefix}: historical planned Leiden-to-RMO transfer is not verified current archive custody")
        if rid == "SRC-DANS-TELL-DEIRALLA-SLIDES-ARCHIVE-XS5-KPQN":
            box9 = source.get("independentPhysicalArchiveInventory2019")
            if (not isinstance(box9, dict)
                or box9.get("status") != "BOX9_HISTORIC_INVENTORY_TEXT_VERIFIED_PHOTOGRAPHIC_OBJECTS_NOT_SEEN_CURRENT_CUSTODY_UNVERIFIED"
                or box9.get("url") != "https://livrepository.liverpool.ac.uk/3058583/1/201230666_MAY2019.pdf"
                or "Does NOT authenticate current 2026 custody" not in str(box9.get("holdingBoundary", ""))):
                errors.append(f"{prefix}: Liverpool 2019 Box 9 inventory is not verified 2026 custody or actual image access")
            if (not isinstance(box9, dict)
                or box9.get("documentedAsOf2019Ownership") != "HALBERTSMA_2019_PRINT_P11_STATES_DEIR_ALLA_ARCHIVE_PROPERTY_OF_DUTCH_NATIONAL_MUSEUM_OF_ANTIQUITIES_NOT_2026_CUSTODY_CONFIRMATION"
                or box9.get("additionalPhotographBox41") != "HALBERTSMA_2019_PRINT_P37_BOX41_FIELD_AND_OBJECT_PHOTOGRAPHS_FROM_ALL_FRANKEN_EXCAVATION_SEASONS_NOT_CONFIRMED_1967_IR_NEGATIVES"
                or box9.get("originalPhotoRegister") != "HALBERTSMA_2019_PRINT_P38_MANY_PHOTOS_NUMBERED_AND_MATCHED_TO_HISTORIC_PHOTO_REGISTER_NO_SPECIFIC_NEGATIVE_NUMBER_IDENTIFIED"
                or "not fully publicly accessible" not in str(source.get("rmoOfficialModernArchiveSearchLimit", ""))
                or "DOES NOT extend" not in str(source.get("rmoOfficialPhotoRightsBoundary", ""))):
                errors.append(f"{prefix}: 2019 RMO archive ownership, Box 41 and photo-register rights require source-specific holds")
        if rid in {"SRC-CAQUOT-LEMAIRE-DEIRALLA-REASSEMBLY-1977-P193198",
                   "SRC-HOFTIJZER-BALAAM-ARTICLE-1976-BA39-1",
                   "SRC-HOFTIJZER-BALAAM-ERRATUM-1976-BA39-3"}:
            witness_key = ("indirect1976ErratumWitness"
                           if rid.startswith("SRC-CAQUOT-LEMAIRE") else "indirect1977CorrectionWitness")
            if source.get(witness_key) != "CAQUOT_LEMAIRE_1977_PRINT_P189_FOOTNOTE1_ATTRIBUTES_SIXTH_CENTURY_TO_EIGHTH_SEVENTH_CORRECTION_TO_BA1976_39_3_P87_NOW_INDEPENDENTLY_CONFIRMED_BY_1976_P87_FIRST_PAGE_SCAN":
                errors.append(f"{prefix}: later 1977 reported date correction missing or falsely promoted")
            citation_key = ("indirect1976ErratumWitnessUrl"
                            if rid.startswith("SRC-CAQUOT-LEMAIRE") else "indirect1977CorrectionWitnessUrl")
            if source.get(citation_key) != "https://www.persee.fr/doc/syria_0039-7946_1977_num_54_3_6603?pageId=T1_189":
                errors.append(f"{prefix}: later 1977 dating correction must cite print p189")
        if rid == "SRC-HOFTIJZER-BALAAM-ERRATUM-1976-BA39-3":
            if source.get("originalErratumTextVerified") is not True:
                errors.append(f"{prefix}: original 1976 publisher erratum p87 must remain directly verified")
        if rid == "SRC-HOFTIJZER-BALAAM-ARTICLE-1976-BA39-1":
            if (source.get("linkedErratumId") != "SRC-HOFTIJZER-BALAAM-ERRATUM-1976-BA39-3"
                or source.get("linkedErratumUrl") != "https://doi.org/10.2307/3209398"
                or source.get("url") != "https://doi.org/10.2307/3209412"):
                errors.append(f"{prefix}: 1976 journal article must retain exact erratum link")
        if rid == "SRC-HOFTIJZER-BALAAM-ERRATUM-1976-BA39-3":
            if (source.get("correctingSourceId") != "SRC-HOFTIJZER-BALAAM-ARTICLE-1976-BA39-1"
                or source.get("url") != "https://doi.org/10.2307/3209398"
                or "directly visually read" not in str(source.get("sourceObjectState", ""))):
                errors.append(f"{prefix}: publisher erratum must preserve original image and its exact article link")
        if rid == "SRC-HOFTIJZER-BALAAM-ERRATUM-1976-BA39-3":
            witness = source.get("originalErratumPageWitness20261109")
            required = {
                "status": "PUBLISHER_ORIGINAL_1976_PRINT_P87_FIRST_PAGE_IMAGE_DIRECT_VISUAL_READ",
                "imageUrl": "https://www.journals.uchicago.edu/cms/10.2307/3209398/asset/524cb216-88da-45e3-8868-530e9fa3dc8b/assets/3209398.fp.png",
                "publication": "THE_BIBLICAL_ARCHAEOLOGIST_39_3_SEP1976_PRINT_P87",
                "locationOnPage": "LOWER_RIGHT_ERRATUM_NOTICE",
                "earlierTitleCentury": "SIXTH_CENTURY",
                "correctedTitleCentury": "EIGHTH_SEVENTH_CENTURY_BCE",
                "earlierDatingAttribution": "H_J_FRANKEN_VETUS_TESTAMENTUM_17_1967_PP480_481_LATER_DATE_ABANDONED_AS_OF_ERRATUM",
                "authorTitleOriginalTranslation": "The Decipherment of the Deir-'Alla Texts",
                "translatorOfAuthorTitle": "William Holladay",
            }
            if (not isinstance(witness, dict)
                or any(witness.get(k) != v for k, v in required.items())
                or witness.get("publisherPage") != "https://www.journals.uchicago.edu/doi/abs/10.2307/3209398"
                or any(witness.get(flag) is not True for flag in (
                    "editorialHeadlineEmbellishmentExplicit", "fullErratumNoticeContentRead"))
                or any(witness.get(flag) is not False for flag in (
                    "underlyingMarch1976ArticleFullTextRead",
                    "inscriptionPhotographCompared",
                    "originalBrill1976PlatesInspected",
                    "modernChronologyConsensusProven",
                    "photographicReusePermissionGranted"))):
                errors.append(f"{prefix}: original 1976 erratum corrects editorial headline only, not ancient glyphs, photo rights or complete March article")
        if rid == "SRC-HOFTIJZER-PHOENIX22-DEIRALLA-1976-FIG41-42":
            if (source.get("historicalFigure42Evidence") != "PHOENIX_1976_P88_FIG42_COMBINATION_I_EARLY_JERUSALEM_INFRARED_PHOTO_REPRODUCTION_CAPTION_ONLY_NOT_VISUAL_AUTOPSY"
                or source.get("shaddayTranslationBoundary") != "PHOENIX_1976_P90_HOFTIJZER_RECONSTRUCTED_DUTCH_GENDERED_SHADDAY_GODS_TRANSLATION_NOT_INDEPENDENT_SHDYN_COLLATION"):
                errors.append(f"{prefix}: Phoenix 1976 infrared photo caption and Shadday translation cannot be promoted to independently verified letters")
        if rid == "SRC-FRANKEN-1967-VT-FIRST-INSCRIPTION-PHOTO-480481":
            if (source.get("firstPhotoBoundary") != "LEMAIRE1985_FIRST_PHOTO_REPORT_1967_FRANKEN_VT17_PP480481_ONLY_ORIGINAL_1967_IMAGE_UNSEEN"
                or source.get("datingBoundary") != "HISTORICAL_TITLE_PERSIAN_PERIOD_NO_ACCEPTED_INSCRIPTION_DATE"):
                errors.append(f"{prefix}: 1967 Franken first photograph report cannot become photo autopsy or accepted Persian date")
            if (source.get("page480PreviewBoundary") != "JSTOR_1516696_BROWSER_PREVIEW_PRINT_P480_ENGLISH_TEXT_NO_INSCRIPTION_PHOTO_P481_NOT_VIEWED_REGISTRATION_GATE"
                or source.get("page481VisualEvidence") != "NOT_OBTAINED_AND_NOT_INSPECTED"
                or source.get("alternateUrl") != "https://www.jstor.org/stable/1516696"):
                errors.append(f"{prefix}: Franken 1967 p480 preview must not be extrapolated to p481 or image collation")
        if rid == "SRC-DEIRALLA-STEINER-WAGEMAKERS-2019":
            chain = source.get("excavationPhotoChain1967")
            if (not isinstance(chain, dict)
                or chain.get("status") != "HISTORICAL_CHAIN_TEXT_VERIFIED_PRECISE_PAGES_PHOTOGRAPHIC_BYTES_UNVERIFIED_CUSTODY_UNKNOWN"
                or "NOT proof" not in str(chain.get("museumIdentity", ""))
                or "NOT automatic" not in str(chain.get("modernArchive", ""))):
                errors.append(f"{prefix}: 1967 museum appointment cannot prove archived infrared negatives or IAA custody")
        if rid == "SRC-DEIRALLA-STEINER-WAGEMAKERS-2019":
            figure = source.get("laterPublishedCombinationFigureAccess2019")
            if (not isinstance(figure, dict)
                or figure.get("status") != "PUBLISHER_2019_FIG5_16_5_17_PHOTO_PIXELS_RENDERED_IN_BOOKVIEWER_NO_INDEPENDENT_SHDYN_GLYPH_COLLATION_1967_1976_ORIGINAL_HOLD"
                or figure.get("browserVisualResult") != "PUBLISHER_2019_PRINT143_VIEWER145_GENUINE_FIG5_16_5_17_PHOTO_PIXELS_RENDERED_LABELS_I_A_TO_I_D_AND_CORRECTION_ABOVE_FIRST_LINE_NO_SHDYN_COLLATION"
                or figure.get("historicalImageIdentity") != "MODERN_2019_REPRODUCTION_NOT_IDENTIFIED_AS_PHOENIX1976_FIG42_OR_BRILL1976_PLATE_INDEPENDENTLY"
                or "DOES_NOT_ISSUE_FILE_SPECIFIC_PHOTO_LICENSE" not in str(figure.get("rightsBoundary", ""))):

                errors.append(f"{prefix}: publisher 2019 figure captions are not 1976 infrared glyph collation or image reuse license")

            witness = figure.get("bookViewerDirectPhotoWitness20261109") if isinstance(figure, dict) else None
            if (not isinstance(witness, dict)
                or witness.get("publisherBookViewer") != "https://www.sidestone.com/bookviewer/9789088908736"
                or witness.get("viewerPageIndex") != 145
                or witness.get("printedPage") != 143
                or witness.get("indexOffset") != 2
                or witness.get("fig516") != "PHOTOGRAPHIC_BLACK_WHITE_PLASTER_FRAGMENT_MONTAGE_LABELS_I_A_I_B_I_C_I_D_WITH_PRINTED_LINE_NUMBERS"
                or witness.get("fig517") != "PHOTOGRAPHIC_PLASTER_INSCRIPTION_CLOSE_UP_VISIBLE_AUTHOR_DESCRIBED_ABOVE_LINE_WORD_INSERTION"
                or witness.get("captionCredit") != "PHOTO_DEIR_ALLA_PROJECT"
                or witness.get("pixelsRendered") is not True
                or witness.get("bothFigureCaptionsVerified") is not True
                or any(witness.get(flag) is not False for flag in (
                    "physicalFragmentsIndependentlyReidentified",
                    "exactAncientLettersShdynIndependentlyVerified",
                    "exactLine5And6GlyphReadingVerified",
                    "original1976BrillPlatesInspected",
                    "original1967Or1976InfraredIdentifiedAndMatched",
                    "rightsForRepublishing2019FiguresConfirmed"))):
                errors.append(f"{prefix}: Sidestone 2019 publisher photo pixels and print/viewer locator must not imply ancient shdyn collation or image rights")
        if rid == "SRC-IAA-DSS-4Q120-B503715-2015":
            photo = source.get("preliminaryBrowserVisualObservation20261108")
            if (source.get("url") != "https://www.deadseascrolls.org.il/explore-the-archive/image/B-503715"
                or source.get("photoProvenanceBoundary") != "IAA_4Q120_B503715_PLATE378_FRAG15_2015_HALEVI_RECTO_PRIMARY_IMAGE_PIXELS_VIEWED_NOT_DJD_CRITICAL_COLLATION"
                or source.get("reportedIaoEvidenceBoundary") != "BROWSER_VISUAL_2026_4Q120_B503715_PHOTO_IAO_SEQUENCE_REPORTED_OMEGA_LOWER_STROKE_FADED_DJD_IX_AND_ALTERNATIVE_PHOTO_UNCOLLATED"
                or source.get("officialLicenseBoundary") != "IAA_TERMS_2026_ALL_RIGHTS_RESERVED_PRIVATE_SINGLE_COPY_EXCEPTION_REPRODUCTION_REQUIRES_PERMISSION"
                or source.get("accessState") != "PARTIAL_OBJECT"
                or source.get("rightsState") != "PERMISSION_REQUIRED"
                or source.get("criticalEditionCollated") is not False
                or source.get("publicationState") != "BLOCKED"
                or not isinstance(photo, dict)
                or photo.get("imagePixelsRendered") is not True
                or photo.get("scientificStatus") != "PRELIMINARY_PHOTOGRAPHIC_OBSERVATION_NOT_INDEPENDENT_EPI_GRAPHIC_CRITICAL_COLLATION"
                or photo.get("rightsStatus") != "IAA_ALL_RIGHTS_RESERVED_REUSE_PERMISSION_REQUIRED_NO_BYTES_COPIED"):
                errors.append(f"{prefix}: IAA 4Q120 browser photo observation must not become critical collation or publication permission")
        if rid == "SRC-IAA-DSS-4Q120-B503715-2015":
            img = source.get("secondaryImageCrossReference20261109")
            pub = img.get("academicPaper") if isinstance(img, dict) else None
            copy = img.get("commonsDerivative") if isinstance(img, dict) else None
            if (not isinstance(pub, dict) or not isinstance(copy, dict)
                or pub.get("officialPublicationDate") != "2015-01-29"
                or pub.get("appendixPrintPage") != 84
                or pub.get("appendixImageRef") != "https://www.deadseascrolls.org.il/explore-the-archive/image/B-298692"
                or pub.get("preferredBibYear") != "2015_NOT_2014"
                or pub.get("actualFig04ImageIndependentHighResRead") is not False
                or pub.get("manuscriptDjDIXEditorialCrosswalkVerified") is not False
                or copy.get("sizePixels") != [522, 338]
                or copy.get("legalResolutionOfRightsConflict") is not False
                or copy.get("sameExactPhotoAsB503715Verified") is not False
                or copy.get("independentCriticalSignLevelReading") is not False
                or copy.get("allowedForProductWithoutRightsReview") is not False):
                errors.append(f"{prefix}: B-298692/Commons cannot prove B-503715 identity, DJD collation or IAA reproduction rights")
        if rid == "SRC-IAA-DSS-4Q120-B503715-2015":
            historical = source.get("historicalCompositeNegatives20261108")
            candidates = historical.get("candidates") if isinstance(historical, dict) else None
            expected_historical = {
                "B-278297": ("M40.633", "1953-05"),
                "B-284588": ("M43.560", "1960-06"),
            }
            historical_valid = (
                isinstance(historical, dict)
                and historical.get("status") == "CATALOG_METADATA_ONLY_NO_PIXEL_INSPECTION"
                and isinstance(candidates, list)
                and len(candidates) == len(expected_historical)
                and all(isinstance(c, dict) and isinstance(c.get("imageId"), str) for c in candidates)
                and {c.get("imageId") for c in candidates} == set(expected_historical)
                and all(
                    c.get("url") == f"https://www.deadseascrolls.org.il/explore-the-archive/image/{c.get('imageId')}"
                    and (c.get("pamNumber"), c.get("date")) == expected_historical[c.get("imageId")]
                    and c.get("imageType") == "Scanned Infrared Negative"
                    and c.get("photographer") == "Najib Anton Albina"
                    and c.get("plate378Included") is True
                    and c.get("containsOtherManuscripts") is True
                    and c.get("sameFragmentAsB503715") is None
                    and c.get("signLevelIaoReadingVerified") is False
                    for c in candidates
                )
            )
            if not historical_valid:
                errors.append(f"{prefix}: 4Q120 historical composite negatives are not fragment-specific IAO collations or 2015-photo identity proofs")
        if rid == "SRC-IAA-DSS-4Q120-B503715-2015":
            numbering = source.get("numberingCrosswalk20261108")
            expected_numbering = {
                "status": "SECONDARY_NUMBERING_CONCORDANCE_NO_DIRECT_DJD_IX_COLLATION",
                "museumPlateAndFragment": "PLATE_378_FRAGMENT_15",
                "museumSourceState": "IAA_PRIMARY_IMAGE_CATALOGUE_LABEL_DIRECTLY_CHECKED",
                "academicIndex": "GARCIA_MARTINEZ_TIGCHELAAR_1999_STUDY_EDITION_VOL1_PRINT_P293",
                "academicIndexAccess": "PRINTED_PAGE_293_DIRECTLY_INSPECTED_WITH_PAGE_IMAGE_INDEX_NOT_DJD_IX_EDITION",
                "originalDjdCitation": "SKEHAN_ULRICH_SANDERSON_DJD_IX_1992_PP167_186_PLATES_XXXIX_XLI_ORIGINAL_NOT_OBTAINED",
                "academicEditorialFragmentsLev427": "EDITORIAL_FRAGMENTS_20_21_LEVITICUS_4_26_28",
                "academicEditorialFragmentsLev46": "EDITORIAL_FRAGMENTS_12_15_LEVITICUS_4_6_8",
                "reportedCrosswalk": "VASILEIADIS_2017_P24_FIG1_EDITORIAL_FRAGMENT20_LINE4_TO_MUSEUM_PLATE378_FRAGMENT15",
                "reportedCrosswalkAccess": "AUTHOR_DEPOSIT_PDF_PRINTED_P24_FIG1_CAPTION_DIRECTLY_EXTRACTED_NO_FIGURE_PIXEL_PALEOGRAPHY",
            }
            valid_numbering = (
                isinstance(numbering, dict)
                and all(numbering.get(k) == v for k, v in expected_numbering.items())
                and numbering.get("museumImage") == "https://www.deadseascrolls.org.il/explore-the-archive/image/B-503715"
                and numbering.get("academicIndexUrl") == "https://ancientmodern.org/wp-content/uploads/2016/02/the_dead_sea_scrolls_study_edition_brill_1999.pdf"
                and numbering.get("reportedCrosswalkSource") == "https://zenodo.org/records/4260519"
                and isinstance(numbering.get("authorPdfCaptionWitness20261109"), dict)
                and numbering["authorPdfCaptionWitness20261109"].get("repository") == "ZENODO_AUTHOR_DEPOSIT"
                and numbering["authorPdfCaptionWitness20261109"].get("printedPage") == 24
                and numbering["authorPdfCaptionWitness20261109"].get("figure") == "FIGURE_1"
                and numbering["authorPdfCaptionWitness20261109"].get("machineRead") == "PDF_HTTP_200_TEXT_EXTRACTED_FROM_FIRST_6_OF_31_PAGES_CAPTION_VERIFIED"
                and numbering["authorPdfCaptionWitness20261109"].get("report") == "CAPTION_ASSOCIATES_LEV4_27_GREEK_ENTOLON_IAO_EDITORIAL_FRAGMENT20_LINE4_WITH_MUSEUM_PLATE378_FRAGMENT15"
                and numbering["authorPdfCaptionWitness20261109"].get("zenodoFileMd5") == "b78bcc5c94e202a15c2392f39dfcbd2f"
                and numbering["authorPdfCaptionWitness20261109"].get("url") == "https://zenodo.org/records/4260519/files/PV%20VTeH%20The%20god%20Iao%20and%20his%20connection%20with%20the%20Biblical%20God%2C%20with%20special%20emphasis%20on%20the%20manuscript%204QpapLXXLevb.pdf"
                and all(numbering["authorPdfCaptionWitness20261109"].get(flag) is False for flag in (
                    "authorImagePixelsIndependentlyAutopsied",
                    "directDjdCriticalEditionCollation",
                    "historicalNegativeComparisonCompleted",
                    "independentEpigrapherApproved",
                    "reprintRightsConfirmed",
                ))
                and numbering.get("distinctNumberingSchemes") is True
                and numbering.get("publishedCrosswalkSourceNotDirectDjdReview") is True
                and all(numbering.get(flag) is False for flag in (
                    "directDjdPageAndPlateChecked",
                    "physicalFragmentPhotoComparisonComplete",
                    "historicalNegativeSamePhysicalFragmentVerified",
                    "glyphByGlyphCriticalCollationComplete",
                    "imageReproductionPermissionGranted",
                ))
            )
            if not valid_numbering:
                errors.append(f"{prefix}: 4Q120 DJD editorial vs IAA museum-plate numbering crosswalk cannot be upgraded without original critical collation")
        if rid == "SRC-KROGEVOLL-TORONTO-PHD-2022-EL-SHADDAI":
            if (source.get("accessState") != "FULL_OBJECT_VERIFIED"
                or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                or source.get("rightsState") != "PERMISSION_REQUIRED"
                or source.get("pdfPages") != 194
                or source.get("full2022ThesisRetrieved") is not True
                or source.get("full2025RevisedBookRead") is not False
                or source.get("independentAncientTextCollation") is not False):
                errors.append(f"{prefix}: Krogevoll 2022 complete thesis cannot imply complete 2025 book, ancient epigraphy, or rights clearance")
        if rid == "SRC-BROOKE-MCLEAN-LXX-EX17-16-CAMBRIDGE-1909-P211":
            if (source.get("accessState") != "FULL_OBJECT_VERIFIED"
                or source.get("rightsState") != "RIGHTS_UNKNOWN"
                or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                or source.get("printedPage") != 211
                or source.get("pdfIndexZeroBased") != 69
                or source.get("originalPageFacsimileChecked") is not True
                or source.get("gottingen1991ApparatusChecked") is not False
                or source.get("ancientCodexCollationCompleted") is not False
                or source.get("allSiglaExpanded") is not False):
                errors.append(f"{prefix}: historic Cambridge 1909 text is not Gottingen 1991 or ancient codex autopsy")
        if rid == "SRC-KRUGER-SHADDAY-JOB-2023-CONTEXT-CRITIQUE":
            if (source.get("accessState") != "FULL_OBJECT_VERIFIED"
                or source.get("rightsState") != "PUBLICATION_ELIGIBLE"
                or source.get("licenseUrl") != "https://creativecommons.org/licenses/by/4.0/"
                or source.get("rightsScope") != "AUTHOR_ARTICLE_ONLY_CC_BY_4_NOT_BIBLE_OR_IMAGES"
                or source.get("mtJob83IndependentSurfaceChecked") is not True
                or source.get("job2713ParallelismNotTwoGodProof") is not True
                or source.get("job272ReferenceMismatchNoted") is not True
                or source.get("authorInterpretationDistinctionHeld") is not True
                or source.get("independentAncientManuscriptCollation") is not False):
                errors.append(f"{prefix}: Kruger Job interpretation or article-scoped license overclaimed")
        if rid in DEIR_ALLA_SOURCE_GUARDS:
            required_state = DEIR_ALLA_SOURCE_GUARDS[rid]
            actual_state = (source.get("accessState"), source.get("rightsState"), source.get("locatorState"))
            if actual_state != required_state:
                errors.append(f"{prefix}: Deir Alla access/rights/locator status changed without review")
            if source.get("publicationState") != "BLOCKED" or source.get("criticalEditionCollated") is not False:
                errors.append(f"{prefix}: Deir Alla publication or original collation falsely approved")
        if rid in DEIR_ALLA_VISUAL_LICENSE_GUARDS:
            license_name, license_url, source_url = DEIR_ALLA_VISUAL_LICENSE_GUARDS[rid]
            if (source.get("license") != license_name
                or source.get("licenseUrl") != license_url
                or source.get("url") != source_url
                or source.get("rightsState") != "PUBLICATION_ELIGIBLE"):
                errors.append(f"{prefix}: Deir Alla image license or attribution evidence missing")
            if source.get("publicationState") != "BLOCKED":
                errors.append(f"{prefix}: permitted image license does not approve Product publication")
        if rid == "SRC-IMG-DEIRALLA-ACOR-LAPP-1987-NOT-BALAAM":
            if "NOT" not in str(source.get("title", "")).upper() and "likely not" not in str(source.get("sourceObjectState", "")).lower():
                errors.append(f"{prefix}: ACOR photo misidentified as Balaam inscription")
        if rid == "SRC-LIVIUS-LEVINE-COMPOSITE-TRANSLATION-2003":
            if ("Levine" not in str(source.get("creator", ""))
                or "1976" not in str(source.get("sourceObjectState", ""))
                or "2003" not in str(source.get("sourceObjectState", ""))
                or "i.7" not in str(source.get("locator", ""))
                or source.get("rightsState") != "PERMISSION_REQUIRED"):
                errors.append(f"{prefix}: Livius composite translation wrongly treated as a primary or free text")
        if rid == "SRC-TSOLIN-ORIEKHOVA-DEIRALLA-2025" and "CC BY-NC 4.0" not in str(source.get("licenseScope", "")):
            errors.append(f"{prefix}: noncommercial source license omitted")
        if rid in {"SRC-NET-REV1-8","SRC-TABB-REVELATION22"}:
            if (source.get("rightsState") != "PERMISSION_REQUIRED"
                or source.get("accessState") != "PARTIAL_OBJECT"
                or source.get("publicationState") != "BLOCKED"
                or source.get("criticalEditionCollated") is not False):
                errors.append(f"{prefix}: Revelation secondary source falsely promoted")
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
        if rid in {"SRC-SBLGNT-ABBA-PAUL-MARK", "SRC-SBLGNT-JOHN-EGO"}:
            if (source.get("rightsState") != "RIGHTS_UNKNOWN"
                or source.get("criticalEditionCollated") is not False):
                errors.append(f"{prefix}: SBLGNT digital host rights or apparatus falsely approved")
        if rid == "SRC-SBLGNT-ABBA-PAUL-MARK":
            if not all(t in str(source.get("supportedUse", "")) for t in (
                "κράζομεν", "κρᾶζον", "Mark"
            )):
                errors.append(f"{prefix}: Abba subjects Mark, believers and Spirit were conflated")
        if rid == "SRC-SBLGNT-JOHN-EGO":
            if "John9:9" not in str(source.get("supportedUse", "")):
                errors.append(f"{prefix}: nondivine John9:9 Greek usage suppressed")
        if rid == "SRC-RAHLFS-EXODUS3":
            if (source.get("rightsState") != "PERMISSION_REQUIRED"
                or source.get("accessState") != "PARTIAL_OBJECT"
                or "ὁ ὤν" not in str(source.get("supportedUse", ""))):
                errors.append(f"{prefix}: publisher LXX full divine self-declaration and license lost")
        if rid == "SRC-BARR-ABBA-1988":
            if ((source.get("accessState"), source.get("locatorState"))
                 != ("CATALOG_ONLY", "COARSE_LOCATOR_ONLY")
                or source.get("rightsState") != "PERMISSION_REQUIRED"
                or "paywalled catalog" not in str(source.get("forbiddenUse", "")).lower()):
                errors.append(f"{prefix}: Barr paywalled full article cannot be promoted from catalog")
        if rid == "SRC-RAHLFS-EXODUS17":
            if (source.get("rightsState") != "PERMISSION_REQUIRED" or
                source.get("accessState") != "PARTIAL_OBJECT" or
                source.get("criticalEditionCollated") is not False):
                errors.append(f"{prefix}: Rahlfs Exodus17 digital LXX cannot claim free rights or collated manuscript")
            if "καταφυγή" not in str(source.get("supportedUse", "")):
                errors.append(f"{prefix}: LXX altar refuge text witness not identified")
        if rid == "SRC-NET-EXODUS17":
            if (source.get("rightsState") != "PERMISSION_REQUIRED" or
                "conjecture" not in str(source.get("forbiddenUse", ""))):
                errors.append(f"{prefix}: textual emendation must remain attributed conjecture")
        if rid == "SRC-NET-GENESIS22":
            if source.get("rightsState") != "PERMISSION_REQUIRED":
                errors.append(f"{prefix}: NET translation copyright gate removed")
        if rid == "SRC-SBLGNT-JOHN10":
            if source.get("rightsState") != "RIGHTS_UNKNOWN":
                errors.append(f"{prefix}: host SBLGNT webpage rights wrongly inherited from publisher license")
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
        if rid == "SRC-JBQ-YAH-2014":
            if (source.get("evidenceClass") != "B1" or
                source.get("rightsState") != "RIGHTS_UNKNOWN" or
                source.get("creator") != "Clifford Hubert Durousseau" or
                source.get("year") != 2014):
                errors.append(f"{prefix}: JBQ Yah bibliography/rights mistaken for editorial consensus")
        if rid == "SRC-NET-PS68":
            if (source.get("rightsState") != "PERMISSION_REQUIRED" or
                source.get("evidenceClass") != "B1" or
                "כִּי יָהּ שְׁמוֹ" not in str(source.get("supportedUse", ""))):
                errors.append(f"{prefix}: conjectural NET Psalm68 ki Yah must be attributed, not substituted for MT")
        if rid == "SRC-SBLGNT-DIGITAL-NT":
            if (source.get("rightsState") != "RIGHTS_UNKNOWN" or
                source.get("accessState") != "PARTIAL_OBJECT" or
                source.get("criticalEditionCollated") is not False):
                errors.append(f"{prefix}: SBLGNT hosted Greek verse rights cannot inherit publisher license or manuscript authority")
        if rid.startswith("SRC-TMSJ-"):
            if (source.get("year") != 2024 or
                source.get("rightsState") != "PERMISSION_REQUIRED" or
                source.get("criticalEditionCollated") is not False or
                source.get("publicationState") != "BLOCKED"):
                errors.append(f"{prefix}: TMSJ 2024 article copyright or source status falsely promoted")
            if source.get("licenseScope") is None or "permission" not in str(source.get("licenseScope", "")).lower():
                errors.append(f"{prefix}: original TMSJ permission terms not recorded")
        if rid == "SRC-TMSJ-VALDIZAN-EX3-2024":
            if (source.get("printedPages") != "53–74" or
                source.get("pdfStartPageZeroBased") != 54 or
                source.get("accessState") != "PARTIAL_OBJECT"):
                errors.append(f"{prefix}: Valdizan Exodus3 title page not full article review")
        if rid == "SRC-TMSJ-VALDIZAN-ACTS2-2024":
            if (source.get("printedPages") != "257–272" or
                source.get("pdfStartPageZeroBased") != 109 or
                source.get("accessState") != "PARTIAL_OBJECT"):
                errors.append(f"{prefix}: Valdizan Acts2 reviewed title page claim overreached")
        if rid == "SRC-TMSJ-CHOU-DANIEL-2024":
            review = source.get("originalReview20261109")
            if (source.get("accessState") != "PARTIAL_OBJECT"
                or source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"
                or source.get("printedPages") != "153–178"
                or source.get("pdfStartPageZeroBased") != 5
                or source.get("pdfEndPageZeroBased") != 30
                or not isinstance(review, dict)
                or review.get("articlePrintedPages") != [153, 178]
                or review.get("pageImagesInspected") != [153, 172, 178]
                or review.get("ancientAramaicCriticalApparatusRead") is not False
                or review.get("allCitedSourceArgumentsIndependentlyReviewed") is not False
                or review.get("assertsSameNarrativePersonAsAncientOfDays") is not False):
                errors.append(f"{prefix}: Chou published selected pages are not critical ancient manuscript collation")
        if rid == "SRC-SUCHARD-ELOHIM-2025":
            if (source.get("evidenceClass") != "B1" or
                source.get("rightsState") != "PUBLICATION_ELIGIBLE" or
                source.get("year") != 2025 or
                "CC BY 4.0" not in str(source.get("license", "")) or
                source.get("licenseScope") != "SUCHARD_ARTICLE_2025_ONLY_NOT_QUOTED_TRANSLATIONS_OR_THIRD_PARTY_REFERENCES" or
                source.get("publicationState") != "BLOCKED"):
                errors.append(f"{prefix}: Suchard 2025; Suchard article CC BY 4.0 limited rights / B1 hypothesis distinction lost")
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
        if rid == "SRC-VT-LIEBERMANN-JEREMIAH-2023":
            if (source.get("year") != 2023 or source.get("firstOnlineYear") != 2022
                or source.get("printedPages") != "62–81"
                or source.get("acceptedManuscriptPage") != "8"
                or source.get("doi") != "10.1163/15685330-bja10091"
                or source.get("rightsState") != "PERMISSION_REQUIRED"
                or source.get("accessState") != "PARTIAL_OBJECT"
                or source.get("criticalEditionCollated") is not False
                or "NOT independently collated" not in str(source.get("supportedUse",""))):
                errors.append(f"{prefix}: Liebermann issue/online year, selected page, licensing or manuscript HOLD changed")
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
    if not isinstance(controls, list) or not any(
        isinstance(x, dict) and x.get("surface") == "אֲדֹנִי"
        and "Abraham" in str(x.get("referent", ""))
        for x in controls
    ):
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


MEMORIAL_IDS = {"yireh", "nissi", "shalom", "rapha", "mekoddishkem", "ro-i"}
MEMORIAL_LOCK_FIELDS = (
    "locusId", "verse", "surface", "language", "edition", "namingActor",
    "namedObject", "speechAct", "referent", "sourceUrl", "sourceAccess",
    "criticalEditionStatus", "rightsState", "publicationState",
)


def validate_memorial_attestations(baseline: dict, contract: dict) -> list[str]:
    """Compare 16 verse contexts to independently committed locked expectations.

    Checks are structural and edition-specific. It cannot attest underlying
    manuscript authenticity, semantic exhaustiveness, theological truth,
    or rights outside one source object.
    """
    errors: list[str] = []
    if (not isinstance(contract, dict) or contract.get("schemaVersion") != 1
        or contract.get("corpusId") != "NAMES_MEMORIAL_DIVINE_PREDICATION_OCCURRENCE_CONTRACT"):
        return ["memorials: malformed contract"]
    if set(contract.get("baselineIds", [])) != MEMORIAL_IDS:
        errors.append("memorials: baseline ID set changed")
    if tuple(contract.get("lockedFields", [])) != MEMORIAL_LOCK_FIELDS:
        errors.append("memorials: required witness field contract weakened")
    if contract.get("counts") != {
        "records": 6, "occurrences": 16, "publicationEligible": 0
    }:
        errors.append("memorials: independently pinned counts or HOLD changed")
    expected = contract.get("lockedAttestations", [])
    if not isinstance(expected, list):
        return errors + ["memorials: expected attestations not a list"]
    expected_by_id: dict[str, dict] = {}
    for witness in expected:
        if not isinstance(witness, dict):
            errors.append("memorials: contract contains invalid witness")
            continue
        loc = witness.get("locusId")
        if not isinstance(loc, str) or not loc or loc in expected_by_id:
            errors.append(f"memorials: missing/duplicate contract locus {loc}")
            continue
        if witness.get("baselineId") not in MEMORIAL_IDS:
            errors.append(f"memorials: unreviewed baseline ID {loc}")
        expected_by_id[loc] = witness
    b = baseline.get("records", [])
    by_row = {r.get("id"): r for r in b if isinstance(r, dict)} if isinstance(b, list) else {}
    seen: dict[str, dict] = {}
    counts: dict[str, int] = {}
    for rid in MEMORIAL_IDS:
        row = by_row.get(rid, {})
        arr = row.get("attestations")
        if not isinstance(arr, list):
            errors.append(f"memorials: missing attestation list {rid}")
            continue
        counts[rid] = len(arr)
        if not row.get("contextualAssertion"):
            errors.append(f"memorials: missing contextual claim scope {rid}")
        for obs in arr:
            if not isinstance(obs, dict):
                errors.append(f"memorials: malformed witness for {rid}")
                continue
            loc = obs.get("locusId")
            if not isinstance(loc, str) or not loc or loc in seen:
                errors.append(f"memorials: missing/duplicate locus {loc}")
                continue
            seen[loc] = obs
            reference = expected_by_id.get(loc)
            if reference is None or reference.get("baselineId") != rid:
                errors.append(f"memorials: orphan/unreviewed locus {rid}/{loc}")
                continue
            for field in MEMORIAL_LOCK_FIELDS:
                if field not in obs or field not in reference or obs.get(field) != reference.get(field):
                    errors.append(f"memorials: {rid}/{loc}: reviewed {field} changed")
            if obs.get("sourceAccess") != "DIGITAL_VERSE_SURFACE_CHECKED":
                errors.append(f"memorials: {rid}/{loc}: false source check")
            if obs.get("criticalEditionStatus") != "NOT_COLLATED":
                errors.append(f"memorials: {rid}/{loc}: false critical manuscript collation")
            if obs.get("publicationState") != "BLOCKED":
                errors.append(f"memorials: {rid}/{loc}: illegal publication")
            if obs.get("rightsState") not in {"PERMISSION_REQUIRED", "RIGHTS_UNKNOWN"}:
                errors.append(f"memorials: {rid}/{loc}: unsupported source license")
            form = obs.get("surface")
            if isinstance(form, str):
                errors.extend(unicode_surface_issues(f"memorials/{loc}", form))
                if obs.get("language") == "hebrew" and not HEBREW.search(form):
                    errors.append(f"memorials: {rid}/{loc}: Hebrew script missing")
                if obs.get("language") == "greek" and not GREEK.search(form):
                    errors.append(f"memorials: {rid}/{loc}: Greek script missing")
            else:
                errors.append(f"memorials: {rid}/{loc}: no original-language surface")
            if not URL.match(str(obs.get("sourceUrl", ""))):
                errors.append(f"memorials: {rid}/{loc}: source URL must be HTTPS")
    if len(seen) != 16 or len(expected_by_id) != 16 or set(seen) != set(expected_by_id):
        errors.append("memorials: 16 unique reviewed contexts required")
    if counts != {
        "yireh": 3, "nissi": 4, "shalom": 3,
        "rapha": 2, "mekoddishkem": 2, "ro-i": 2
    }:
        errors.append("memorials: per-lemma occurrence counts drifted")
    audit = baseline.get("auditProtocol", {}).get("memorialsAndPredications", {})
    if (set(audit.get("ids", [])) != MEMORIAL_IDS or
        audit.get("totalAttestations") != 16 or
        audit.get("criticalEditionCollated") is not False or
        audit.get("publicationEligible") != 0):
        errors.append("memorials: ledger phase count / critical / Product HOLD changed")
    # Independent semantic checks beyond the JSON-pinned exact-surface fixture:
    def o(loc: str) -> dict:
        return seen.get(loc, {})
    if (o("gen22-memorial-place").get("namedObject") != "place"
        or o("gen22-memorial-place").get("nameClause") != "שֵׁם-הַמָּקוֹם הַהוּא"
        or o("gen22-memorial-place").get("notNamedObject") != "altar"):
        errors.append("memorials: Gen22:14 names PLACE, not earlier altar")
    if (o("gen22-abraham-answer").get("surface") != "אֱלֹהִים יִרְאֶה-לּוֹ"
        or o("gen22-mountain-proverb").get("surface") != "בְּהַר יְהוָה יֵרָאֶה"
        or o("gen22-mountain-proverb").get("notIdenticalVerbTo") != "יִרְאֶה"):
        errors.append("memorials: Gen22 Qal versus Niphal/vision/provision distinction erased")
    if (o("ex17-mt-altar").get("namedObject") != "altar"
        or o("ex17-lxx-altar").get("namedObject") != "altar"
        or o("ex17-mt-altar").get("surface") != "יְהוָה נִסִּי"
        or o("ex17-lxx-altar").get("surface") != "Κύριός μου καταφυγή"):
        errors.append("memorials: Ex17:15 altar name, MT banner vs LXX refuge distinction lost")
    if (o("ex17-lxx-altar").get("rightsState") != "PERMISSION_REQUIRED"
        or o("ex17-lxx-secret-hand").get("rightsState") != "PERMISSION_REQUIRED"):
        errors.append("memorials: copyrighted Rahlfs Exodus17 reuse gate removed")
    if (o("ex17-mt-hand-throne").get("surface") != "כִּי-יָד עַל-כֵּס יָהּ"
        or o("ex17-lxx-secret-hand").get("surface") != "ὅτι ἐν χειρὶ κρυφαίᾳ"
        or o("ex17-mt-hand-throne").get("textualStatus") !=
           "MT_SURFACE_AND_HYPOTHETICAL_EMENDATION_SEPARATE"):
        errors.append("memorials: Ex17:16 MT versus Greek secret-hand and conjecture collapsed")
    if (o("jud6-divine-assurance").get("namedObject") != "none"
        or o("jud6-gideon-altar").get("namedObject") != "altar"
        or o("jud6-baal-altar-control").get("namedObject") != "Baal altar"):
        errors.append("memorials: Judg6 peace speech / Gideon altar / Baal altar conflated")
    if (o("exo15-yhwh-healer").get("namedObject") != "none"
        or "2ms" not in str(o("exo15-yhwh-healer").get("morphology", ""))
        or o("jer17-heal-my-prayer").get("speechAct") != "prayer_for_healing"):
        errors.append("memorials: healer 2ms divine predication versus Jeremiah prayer erased")
    if any("2mp" not in str(o(loc).get("morphology", "")) for loc in (
        "exo31-sanctify-israel", "lev20-sanctify-israel"
    )):
        errors.append("memorials: sanctification 2mp 'you plural' incorrectly converted")
    if (o("ps23-yhwh-shepherd").get("root") != "רעה"
        or o("ps23-yhwh-shepherd").get("notSameRootAs") != "ראה (Hagar's El-Roi seeing)"
        or o("jn10-christ-good-shepherd").get("namingActor") != "Jesus"
        or "NOT shared lexical root" not in str(o("jn10-christ-good-shepherd").get("rootRelation", ""))):
        errors.append("memorials: seeing/shepherd roots or NT speaker/intertext conflated")
    return errors


SPEECH_INTERTEXT_IDS = {"abba", "ego-eimi", "ehyeh"}
SPEECH_INTERTEXT_LOCK_FIELDS = (
    "locusId", "verse", "surface", "language", "edition", "speaker",
    "referent", "speechAct", "sourceUrl", "checkState",
    "criticalEditionStatus", "rightsState", "publicationState"
)


def validate_speech_intertext(baseline: dict, contract: dict) -> list[str]:
    """Guard 12 speech-context witnesses; no intrinsic proper-name inference."""
    errors: list[str] = []
    if (not isinstance(contract, dict) or contract.get("schemaVersion") != 1
        or contract.get("corpusId") != "NAMES_ABBA_EGO_EIMI_EHYEH_INTERTEXT_V1"):
        return ["speech-intertext: invalid contract and version"]
    if set(contract.get("baselineIds", [])) != SPEECH_INTERTEXT_IDS:
        errors.append("speech-intertext: baseline IDs changed")
    if tuple(contract.get("lockedFields", [])) != SPEECH_INTERTEXT_LOCK_FIELDS:
        errors.append("speech-intertext: required source/speaker fields removed")
    if contract.get("counts") != {"records": 3, "occurrences": 12, "publicationEligible": 0}:
        errors.append("speech-intertext: reviewed occurrence counts or Product block changed")
    snapshots = contract.get("lockedAttestations", [])
    if not isinstance(snapshots, list):
        return errors + ["speech-intertext: expected snapshots absent"]
    expected: dict[str, dict] = {}
    for rec in snapshots:
        if not isinstance(rec, dict):
            errors.append("speech-intertext: invalid snapshot object")
            continue
        loc = rec.get("locusId")
        if not isinstance(loc, str) or not loc or loc in expected:
            errors.append(f"speech-intertext: missing/duplicate snapshot {loc}")
            continue
        if rec.get("baselineId") not in SPEECH_INTERTEXT_IDS:
            errors.append(f"speech-intertext: unreviewed snapshot baseline {loc}")
        expected[loc] = rec
    records = baseline.get("records", [])
    by_id = {r.get("id"): r for r in records if isinstance(r, dict)} if isinstance(records, list) else {}
    actual: dict[str, dict] = {}
    counters: dict[str, int] = {}
    for rid in SPEECH_INTERTEXT_IDS:
        row = by_id.get(rid, {})
        arr = row.get("attestations", [])
        if not isinstance(arr, list):
            errors.append(f"speech-intertext: non-list attestations {rid}")
            continue
        counters[rid] = len(arr)
        if not row.get("contextualAssertion"):
            errors.append(f"speech-intertext: missing editorial boundary {rid}")
        for obs in arr:
            if not isinstance(obs, dict):
                errors.append(f"speech-intertext: non-object observation in {rid}")
                continue
            loc = obs.get("locusId")
            if not isinstance(loc, str) or not loc or loc in actual:
                errors.append(f"speech-intertext: missing/duplicate locusId {loc}")
                continue
            actual[loc] = obs
            ref = expected.get(loc)
            if ref is None or ref.get("baselineId") != rid:
                errors.append(f"speech-intertext: unreviewed witness {rid}/{loc}")
                continue
            for key in SPEECH_INTERTEXT_LOCK_FIELDS:
                if key not in obs or key not in ref or obs.get(key) != ref.get(key):
                    errors.append(f"speech-intertext: {rid}/{loc} changed {key}")
            if obs.get("checkState") != "DIGITAL_VERSE_SURFACE_CHECKED":
                errors.append(f"speech-intertext: {rid}/{loc} unverified source falsely marked")
            if (obs.get("criticalEditionStatus") != "NOT_COLLATED"
                or obs.get("publicationState") != "BLOCKED"):
                errors.append(f"speech-intertext: {rid}/{loc} unauthorized publication/critical promotion")
            surface = obs.get("surface")
            if isinstance(surface, str):
                errors.extend(unicode_surface_issues(f"speech-intertext/{loc}", surface))
                if obs.get("language") == "greek" and not GREEK.search(surface):
                    errors.append(f"speech-intertext: {loc} has no Greek script")
                if obs.get("language") == "hebrew" and not HEBREW.search(surface):
                    errors.append(f"speech-intertext: {loc} has no Hebrew script")
            else:
                errors.append(f"speech-intertext: {loc} lacks original written form")
            if not URL.match(str(obs.get("sourceUrl", ""))):
                errors.append(f"speech-intertext: {loc} missing edition URL")
    if (len(actual), len(expected), set(actual) == set(expected)) != (12, 12, True):
        errors.append("speech-intertext: 12 unique locked verse-loci required")
    if counters != {"abba": 3, "ego-eimi": 6, "ehyeh": 3}:
        errors.append("speech-intertext: per-ID counts changed")
    meta = baseline.get("auditProtocol", {}).get("abbaEgoIntertext", {})
    if (set(meta.get("baselineIds", [])) != SPEECH_INTERTEXT_IDS
        or meta.get("totalAttestations") != 12
        or meta.get("negativeControl") != "ego-john9-human"
        or meta.get("criticalCollationStatus") != "NOT_COLLATED"
        or meta.get("publicationEligible") != 0):
        errors.append("speech-intertext: audit and human lexical control drifted")
    def item(loc: str) -> dict:
        return actual.get(loc, {})
    abba_forms = (
        item("abba-mark14-prayer").get("surface"),
        item("abba-rom8-adoption").get("surface"),
        item("abba-gal4-spirit").get("surface")
    )
    if abba_forms != ("Αββα ὁ πατήρ",)*3:
        errors.append("speech-intertext: SBLGNT Abba original Greek forms changed")
    if (item("abba-mark14-prayer").get("agentOfCry") != "Jesus"
        or "κράζομεν" not in str(item("abba-rom8-adoption").get("agentOfCry", ""))
        or "κρᾶζον" not in str(item("abba-gal4-spirit").get("agentOfCry", ""))):
        errors.append("speech-intertext: Jesus/believers/Spirit crying agents collapsed")
    if any(item(loc).get("languageOrigin") != "ARAMAIC_WORD_GREEK_SCRIPT" for loc in (
        "abba-mark14-prayer", "abba-rom8-adoption", "abba-gal4-spirit"
    )):
        errors.append("speech-intertext: Abba Greek script versus Aramaic lexical origin confused")
    orth = by_id.get("abba", {}).get("printedOrthography", {})
    if ((orth.get("sblgnt"), orth.get("thgnt"), orth.get("nestle1904")) !=
        ("Αββα", "ἀββᾶ", "Ἀββᾶ")):
        errors.append("speech-intertext: publisher-specific accents and case erased")
    if (item("ego-john9-human").get("isDivineDesignation") is not False
        or item("ego-john9-human").get("speaker") != "formerly blind man"
        or item("ego-john9-human").get("surface") != "Ἐγώ εἰμι"):
        errors.append("speech-intertext: John 9:9 ordinary human ego eimi control lost")
    if (item("ego-john8-preabraham").get("surface") != "ἐγὼ εἰμί"
        or "πρὶν Ἀβραὰμ γενέσθαι" not in str(item("ego-john8-preabraham").get("claimScope", ""))):
        errors.append("speech-intertext: John 8:58 before-Abraham claim context lost")
    if (item("ehyeh-ex3-promise").get("surface") != "כִּי-אֶהְיֶה עִמָּךְ"
        or item("ehyeh-ex3-hebrew").get("surface") != "אֶהְיֶה אֲשֶׁר אֶהְיֶה"):
        errors.append("speech-intertext: Exodus 3 Hebrew promise/naming distinction lost")
    if (item("ehyeh-ex3-greek").get("surface") != "Ἐγώ εἰμι ὁ ὤν"
        or item("ehyeh-ex3-greek").get("greekSecondClause") != "Ὁ ὢν ἀπέσταλκέν με"
        or item("ehyeh-ex3-greek").get("rightsState") != "PERMISSION_REQUIRED"
        or item("ehyeh-ex3-greek").get("intertextRelation") != "ALLUSION_POSSIBLE_NOT_IDENTICAL_FULL_QUOTE"):
        errors.append("speech-intertext: LXX Exodus 3:14 full ὁ ὤν / license / contextual relation erased")
    # Independent fact invariant: a copied contract and the source ledger must
    # not mutually certify the same mistaken addressee/referent interpretation.
    for loc in ("ehyeh-ex3-promise", "ehyeh-ex3-hebrew", "ehyeh-ex3-greek"):
        for label, source_row in (("ledger", actual.get(loc, {})),
                                  ("locked contract", expected.get(loc, {}))):
            if (source_row.get("referent") != "God of Israel, the divine first-person speaker"
                or source_row.get("addressee") != "Moses"):
                errors.append(f"speech-intertext: {loc} divine referent/addressee error in {label}")
    return errors


EXTENSION_NEW_IDS = {
    "yah", "eloah", "elah-shmaya", "el-hay", "avinu",
    "yhwh-ori", "el-emunah", "el-rahum-hannun",
    "kyrios-ho-theos", "poimen-ho-kalos", "anastasis-zoe",
}
EXTENSION_NEW_LOCK_FIELDS = (
    "locusId", "verse", "surface", "language", "edition", "narrativeSpeaker",
    "speechAct", "referent", "sourceUrl", "checkState",
    "criticalEditionStatus", "rightsState", "publicationState"
)


def validate_extension_attestations(extension: dict, contract: dict) -> list[str]:
    """Fail closed on 14 independent Greek/Hebrew/Aramaic attestation witnesses.

    Structural original-script contract only, not independent manuscript
    collation. The editor must revise snapshots explicitly; never regenerate.
    """
    errors: list[str] = []
    if (not isinstance(contract, dict) or contract.get("schemaVersion") != 1
        or contract.get("corpusId") != "NAMES_EXTENSION_ORIGINAL_LANGUAGE_OCCURRENCES_V1"):
        return ["extension-witness: missing or malformed versioned contract"]
    if set(contract.get("extensionIds", [])) != EXTENSION_NEW_IDS:
        errors.append("extension-witness: reviewed additional ID set was changed")
    if tuple(contract.get("lockedFields", [])) != EXTENSION_NEW_LOCK_FIELDS:
        errors.append("extension-witness: exact verse/source/speaker contract weakened")
    if contract.get("counts") != {"records": 11, "occurrences": 14, "publicationEligible": 0}:
        errors.append("extension-witness: independent count/approval lock altered")
    items = contract.get("lockedAttestations", [])
    if not isinstance(items, list):
        return errors + ["extension-witness: fixed source snapshots missing"]
    expected: dict[str, dict] = {}
    for obj in items:
        if not isinstance(obj, dict):
            errors.append("extension-witness: non-object source snapshot")
            continue
        loc = obj.get("locusId")
        if not isinstance(loc, str) or not loc or loc in expected:
            errors.append(f"extension-witness: duplicate/missing snapshot ID {loc}")
            continue
        if obj.get("extensionId") not in EXTENSION_NEW_IDS:
            errors.append(f"extension-witness: unknown extension ID in snapshot {loc}")
        expected[loc] = obj
    rows = extension.get("records", [])
    by_id = {r.get("id"): r for r in rows if isinstance(r, dict)} if isinstance(rows, list) else {}
    seen: dict[str, dict] = {}
    counts: dict[str, int] = {}
    for rid in EXTENSION_NEW_IDS:
        row = by_id.get(rid, {})
        att = row.get("attestations")
        if not isinstance(att, list):
            errors.append(f"extension-witness: no attestation list for {rid}")
            continue
        counts[rid] = len(att)
        if not row.get("contextualAssertion"):
            errors.append(f"extension-witness: claim boundary missing for {rid}")
        for obj in att:
            if not isinstance(obj, dict):
                errors.append(f"extension-witness: malformed occurrence in {rid}")
                continue
            loc = obj.get("locusId")
            if not isinstance(loc, str) or not loc or loc in seen:
                errors.append(f"extension-witness: missing/duplicate occurrence ID {loc}")
                continue
            seen[loc] = obj
            ref = expected.get(loc)
            if ref is None or ref.get("extensionId") != rid:
                errors.append(f"extension-witness: unreviewed source ID {rid}/{loc}")
                continue
            for field in EXTENSION_NEW_LOCK_FIELDS:
                if field not in obj or field not in ref or obj.get(field) != ref.get(field):
                    errors.append(f"extension-witness: {rid}/{loc}: reviewed {field} changed")
            if obj.get("checkState") != "DIGITAL_VERSE_SURFACE_CHECKED":
                errors.append(f"extension-witness: {rid}/{loc}: unreviewed digital status")
            if obj.get("criticalEditionStatus") != "NOT_COLLATED":
                errors.append(f"extension-witness: {rid}/{loc}: source promoted to false collation")
            if obj.get("publicationState") != "BLOCKED":
                errors.append(f"extension-witness: {rid}/{loc}: unauthorized Product release")
            surface = obj.get("surface")
            if not isinstance(surface, str):
                errors.append(f"extension-witness: {rid}/{loc}: original-script surface missing")
            else:
                errors.extend(unicode_surface_issues(f"extension-witness/{loc}", surface))
                if obj.get("language") == "hebrew" and not HEBREW.search(surface):
                    errors.append(f"extension-witness: {loc}: expected Hebrew script")
                if obj.get("language") == "aramaic" and not HEBREW.search(surface):
                    errors.append(f"extension-witness: {loc}: expected Hebrew script for Aramaic text")
                if obj.get("language") == "greek" and not GREEK.search(surface):
                    errors.append(f"extension-witness: {loc}: expected Greek script")
            if not URL.match(str(obj.get("sourceUrl", ""))):
                errors.append(f"extension-witness: {loc}: source URL invalid")
    if len(expected) != 14 or len(seen) != 14 or set(expected) != set(seen):
        errors.append("extension-witness: exactly 14 unique verified source contexts required")
    if counts != {
        "yah": 2, "eloah": 1, "elah-shmaya": 2, "el-hay": 1, "avinu": 1,
        "yhwh-ori": 1, "el-emunah": 1, "el-rahum-hannun": 1,
        "kyrios-ho-theos": 1, "poimen-ho-kalos": 2, "anastasis-zoe": 1,
    }:
        errors.append("extension-witness: reviewed per-lemma occurrence counters altered")
    audit = extension.get("auditProtocol", {}).get("extensionAudit", {})
    if (set(audit.get("ids", [])) != EXTENSION_NEW_IDS or
        audit.get("totalAttestations") != 14 or
        audit.get("finalEtymologiesSettled") != 0 or
        audit.get("publicationEligible") != 0 or
        audit.get("criticalEditionStatus") != "NOT_COLLATED"):
        errors.append("extension-witness: extra corpus status or publication hold changed")
    def obs(locus: str) -> dict:
        return seen.get(locus, {})
    if (obs("ext-yah-ex15-song").get("prefixOnName") != "NONE"
        or obs("ext-yah-ps68-prefixed").get("surface") != "בְּיָהּ שְׁמוֹ"
        or obs("ext-yah-ps68-prefixed").get("prefixOnName") != "בְּ"):
        errors.append("extension-witness: Psalm68 bet prefix and Exodus15 standalone Yah conflated")
    ps = obs("ext-yah-ps68-prefixed")
    if (ps.get("numbering") != {"mt": "Psalms 68:5", "commonEnglish": "Psalms 68:4"}
        or "NET proposes" not in str(ps.get("textualConjecture", ""))):
        errors.append("extension-witness: Psalm68 versification/conjecture promoted to MT")
    if (obs("ext-eloah-deut32").get("grammaticalActor") != "Jeshurun, וַיִּטֹּשׁ"
        or obs("ext-eloah-deut32").get("grammaticalObject") != "אֱלוֹהַּ"):
        errors.append("extension-witness: Eloah object of Jeshurun's rejection lost")
    if (obs("ext-elah-dan2-request").get("language") != "aramaic"
        or obs("ext-elah-dan2-praise").get("surface") != "לֶאֱלָהּ שְׁמַיָּא"
        or obs("ext-elah-dan2-praise").get("grammaticalPrefix") != "לֶ"):
        errors.append("extension-witness: Daniel2 Aramaic language/lamed prefix lost")
    controls = by_id.get("elah-shmaya", {}).get("negativeControls", [])
    if (not isinstance(controls, list) or
        not any(isinstance(x, dict) and x.get("verse") == "Daniel 2:11"
                and x.get("surface") == "אֱלָהִין" for x in controls) or
        not any(isinstance(x, dict) and x.get("verse") == "Daniel 2:28"
                and x.get("surface") == "אֱלָהּ בִּשְׁמַיָּא" for x in controls)):
        errors.append("extension-witness: Aramaic pagan gods vs God in heaven contrast removed")
    if (obs("ext-elhay-ps42").get("prefixOnEl") != "לְ"
        or obs("ext-elhay-ps42").get("numbering") != {
            "mt": "Psalms 42:3", "commonEnglish": "Psalms 42:2"
        }):
        errors.append("extension-witness: Psalm42 lamed and verse numbering lost")
    if (obs("ext-avinu-isa63").get("language") != "hebrew"
        or obs("ext-avinu-isa63").get("speechAct") != "corporate_direct_address_to_God_as_Father"):
        errors.append("extension-witness: Isaiah63 Hebrew corporate Father prayer conflated with Abba")
    if (obs("ext-yhwhori-ps27").get("namingActInVerse") is not False
        or obs("ext-yhwhori-ps27").get("linkedPoeticMetaphor") != "יְהוָה מָעוֹז-חַיַּי"):
        errors.append("extension-witness: Psalm27 poetic light falsely turned into name act")
    if (obs("ext-elemuna-deut32").get("namingActInVerse") is not False
        or "הַצּוּר" not in str(obs("ext-elemuna-deut32").get("contextParallel",""))):
        errors.append("extension-witness: Deut32 faithful God separated from Rock parallel")
    if (obs("ext-elrahum-ex34").get("introductoryClause") != "וַיִּקְרָא, יְהוָה יְהוָה"
        or obs("ext-elrahum-ex34").get("qualifier") != "NAME_PROCLAMATION_NOT_EACH_ADJECTIVE_AS_PROPER_NAME"):
        errors.append("extension-witness: Exodus34 naming proclamation vs adjectives distinction lost")
    luke = obs("ext-kyrios-luke1")
    if (luke.get("grammaticalSubject") != "κύριος ὁ θεὸς"
        or luke.get("grammaticalVerb") != "δώσει"
        or luke.get("recipient") != "Jesus (αὐτῷ)"
        or luke.get("narrativeSpeaker") != "Gabriel speaking to Mary"
        or luke.get("rightsState") != "PERMISSION_REQUIRED"):
        errors.append("extension-witness: Luke1:32 Gabriel/Lord God/Jesus role and THGNT rights conflated")
    for loc in ("ext-poimen-john1011","ext-poimen-john1014","ext-anastasis-john11"):
        if obs(loc).get("syntax") not in {
            "EXPLICIT_NOMINAL_PREDICATE", "TWO_COORDINATED_NOMINAL_PREDICATES"
        }:
            errors.append(f"extension-witness: {loc} John predicate silently made absolute ego-eimi")
    if (obs("ext-poimen-john1011").get("fullClause") != "Ἐγώ εἰμι ὁ ποιμὴν ὁ καλός"
        or obs("ext-poimen-john1014").get("fullClause") != "ἐγώ εἰμι ὁ ποιμὴν ὁ καλός"):
        errors.append("extension-witness: John10 shepherd verses' edition-specific clauses drifted")
    if obs("ext-anastasis-john11").get("fullClause") != "Ἐγώ εἰμι ἡ ἀνάστασις καὶ ἡ ζωή":
        errors.append("extension-witness: John11 both resurrection and life predicates lost")
    return errors


CORE_NAME_IDS = {"yhwh", "el"}
CORE_NAME_FIELDS = (
    "locusId", "verse", "surface", "language", "edition", "speaker",
    "speechAct", "referent", "referentClass", "sourceUrl", "checkState",
    "criticalEditionStatus", "rightsState", "publicationState"
)


def validate_core_name_lexeme(baseline: dict, contract: dict) -> list[str]:
    """Pin YHWH as personal divine name and El as context-variable noun.

    These checks are exact digital-source integrity, not historical
    vocalization claims or manuscript-critical certainties.
    """
    errors: list[str] = []
    if (not isinstance(contract, dict) or contract.get("schemaVersion") != 1
        or contract.get("corpusId") != "NAMES_YHWH_PERSONAL_NAME_EL_GENERIC_LEXEME_V1"):
        return ["core-names: invalid reviewer-pinned contract"]
    if set(contract.get("baselineIds", [])) != CORE_NAME_IDS:
        errors.append("core-names: baseline ID set must be YHWH and El only")
    if tuple(contract.get("lockedFields", [])) != CORE_NAME_FIELDS:
        errors.append("core-names: exact scripture form, speaker and referent lock weakened")
    if contract.get("counts") != {"records": 2, "occurrences": 8, "publicationEligible": 0}:
        errors.append("core-names: pinned contract counts or publication hold changed")
    snapshot = contract.get("lockedAttestations", [])
    if not isinstance(snapshot, list):
        return errors + ["core-names: missing source snapshots"]
    expected: dict[str, dict] = {}
    for row in snapshot:
        if not isinstance(row, dict):
            errors.append("core-names: malformed source snapshot")
            continue
        key = row.get("locusId")
        if not isinstance(key, str) or not key or key in expected:
            errors.append(f"core-names: missing or duplicate source locus {key}")
            continue
        expected[key] = row
        if row.get("baselineId") not in CORE_NAME_IDS:
            errors.append(f"core-names: non-core ID in source contract {key}")
    records = baseline.get("records", [])
    bmap = {r.get("id"):r for r in records if isinstance(r, dict)} if isinstance(records, list) else {}
    actual: dict[str, dict] = {}
    count: dict[str, int] = {}
    for rid in CORE_NAME_IDS:
        row = bmap.get(rid, {})
        attestations = row.get("attestations", [])
        if not isinstance(attestations, list):
            errors.append(f"core-names: missing attestations list for {rid}")
            continue
        count[rid] = len(attestations)
        if not isinstance(row.get("contextualAssertion"), str) or not row["contextualAssertion"]:
            errors.append(f"core-names: no contextual claim scope for {rid}")
        for obj in attestations:
            if not isinstance(obj, dict):
                errors.append(f"core-names: invalid attestation object for {rid}")
                continue
            key = obj.get("locusId")
            if not isinstance(key, str) or not key or key in actual:
                errors.append(f"core-names: duplicate/empty occurrence ID {key}")
                continue
            actual[key] = obj
            ref = expected.get(key)
            if ref is None or ref.get("baselineId") != rid:
                errors.append(f"core-names: unexpected or moved source {rid}/{key}")
                continue
            for field in CORE_NAME_FIELDS:
                if field not in obj or field not in ref or obj.get(field) != ref.get(field):
                    errors.append(f"core-names: {rid}/{key}: {field} source contract drifted")
            if obj.get("checkState") != "DIGITAL_VERSE_SURFACE_CHECKED":
                errors.append(f"core-names: {rid}/{key}: source marked checked without review")
            if obj.get("criticalEditionStatus") != "NOT_COLLATED":
                errors.append(f"core-names: {rid}/{key}: false critical witness approval")
            if obj.get("publicationState") != "BLOCKED" or obj.get("rightsState") != "RIGHTS_UNKNOWN":
                errors.append(f"core-names: {rid}/{key}: rights or publication silently promoted")
            surface = obj.get("surface")
            if isinstance(surface, str):
                errors.extend(unicode_surface_issues(f"core-names/{key}", surface))
                if not HEBREW.search(surface):
                    errors.append(f"core-names: original Hebrew script lost for {key}")
            else:
                errors.append(f"core-names: original-script form missing for {key}")
            if not URL.match(str(obj.get("sourceUrl", ""))):
                errors.append(f"core-names: source URL missing {key}")
    if len(expected) != 8 or len(actual) != 8 or set(expected) != set(actual):
        errors.append("core-names: exactly eight unique YHWH/El contexts required")
    if count != {"yhwh": 3, "el": 5}:
        errors.append("core-names: three YHWH and five El contexts required")
    audit = baseline.get("auditProtocol", {}).get("coreNameVsLexeme", {})
    if (set(audit.get("baselineIds", [])) != CORE_NAME_IDS
        or audit.get("totalAttestations") != 8
        or audit.get("negativeElReferents") != 2
        or audit.get("finalEtymologyDecisions") != 0
        or audit.get("criticalEditionStatus") != "NOT_COLLATED"
        or audit.get("publicationEligible") != 0):
        errors.append("core-names: audit count / etymology / Product gate changed")
    def obj(loc: str) -> dict:
        return actual.get(loc, {})
    if (obj("core-yhwh-ex3-name").get("nameClaim") != "זֶה-שְּׁמִי לְעֹלָם"
        or obj("core-yhwh-ex3-name").get("relatedButDistinct") !=
           "Exodus3:14 אֶהְיֶה אֲשֶׁר אֶהְיֶה"):
        errors.append("core-names: Exodus3 YHWH divine personal name confused with Ehyeh")
    if (obj("core-yhwh-ex6-self").get("surface") != "אֲנִי יְהוָה"
        or "לֹא נוֹדַעְתִּי" not in str(obj("core-yhwh-ex6-self").get("nextVerseQualifier",""))):
        errors.append("core-names: Exodus6:2 self-revelation or 6:3 known-to-patriarchs nuance lost")
    if (obj("core-yhwh-ex15-hymn").get("nameClaim") != "יְהוָה שְׁמוֹ"
        or obj("core-yhwh-ex15-hymn").get("speaker") != "Moses and Israel singing"):
        errors.append("core-names: Exodus15 YHWH name hymn confused with divine self-speech")
    if (obj("core-el-ex34-merciful").get("contextualClause") !=
        "יְהוָה יְהוָה, אֵל רַחוּם וְחַנּוּן"
        or obj("core-el-deut32-faithful").get("poeticParallel") !=
           "הַצּוּר תָּמִים פָּעֳלוֹ"):
        errors.append("core-names: El attribute phrases and YHWH context lost")
    negative = ("core-el-deut32-foreign","core-el-isa43-negated")
    if any(obj(loc).get("referentClass") != "OTHER_GOD_NEGATED"
           or obj(loc).get("isYHWH") is not False for loc in negative):
        errors.append("core-names: El foreign or putative god wrongly equated with YHWH")
    if (obj("core-el-deut32-foreign").get("negationClause") !=
        "וְאֵין עִמּוֹ, אֵל נֵכָר"
        or obj("core-el-isa43-negated").get("negationClause") != "לֹא-נוֹצַר אֵל"):
        errors.append("core-names: negative El clauses deleted")
    if (obj("core-el-isa43-i-am").get("isYHWH") is not True
        or obj("core-el-isa43-i-am").get("referentClass") != "YHWH"
        or obj("core-el-isa43-i-am").get("surface") != "וַאֲנִי-אֵל"):
        errors.append("core-names: Isaiah43:12 positive El divine self-predication lost")
    return errors


def validate_full_coverage(baseline: dict, extension: dict) -> list[str]:
    """All 42 researched IDs must retain at least one conservative verse witness.

    This is a coverage gate, not a claim of exhaustive attestations per name,
    independent critical collation, or readiness for public deployment.
    """
    errors: list[str] = []
    for label, data, count in (("Arena", baseline, 29), ("extension", extension, 13)):
        records = data.get("records", []) if isinstance(data, dict) else []
        if not isinstance(records, list) or len(records) != count:
            errors.append(f"coverage: {label} count changed from {count}")
            continue
        for record in records:
            if not isinstance(record, dict):
                errors.append(f"coverage: malformed {label} candidate")
                continue
            rid = record.get("id", "<unknown>")
            uses = record.get("attestations")
            if not isinstance(uses, list) or not uses:
                errors.append(f"coverage: {label}/{rid} lacks independently source-located contexts")
                continue
            if record.get("publicationState") != "BLOCKED":
                errors.append(f"coverage: {label}/{rid} unreviewed Product promotion")
            for use in uses:
                if not isinstance(use, dict):
                    errors.append(f"coverage: {label}/{rid} contains malformed verse")
                    continue
                if not str(use.get("verse", "")).strip():
                    errors.append(f"coverage: {label}/{rid} missing verse locator")
                if not isinstance(use.get("surface"), str) or not use["surface"].strip():
                    errors.append(f"coverage: {label}/{rid} missing original written form")
                if not URL.match(str(use.get("sourceUrl", ""))):
                    errors.append(f"coverage: {label}/{rid} missing source URL")
                if use.get("criticalEditionStatus") != "NOT_COLLATED":
                    errors.append(f"coverage: {label}/{rid} falsely marked as manuscript-collated")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--extension", type=Path, default=EXTENSION)
    parser.add_argument("--sources", type=Path, default=SOURCES)
    parser.add_argument("--attestation-contract", type=Path, default=ATTESTATION_CONTRACT)
    parser.add_argument("--memorial-contract", type=Path, default=MEMORIAL_CONTRACT)
    parser.add_argument("--speech-contract", type=Path, default=SPEECH_INTERTEXT_CONTRACT)
    parser.add_argument("--extension-contract", type=Path, default=EXTENSION_ATTESTATION_CONTRACT)
    parser.add_argument("--core-names-contract", type=Path, default=CORE_NAME_LEXEME_CONTRACT)
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
    try:
        with args.memorial_contract.open("r", encoding="utf-8") as stream:
            memorial_contract = json.load(stream)
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot read memorial attestation contract: {exc}", file=sys.stderr)
        return 1
    try:
        with args.speech_contract.open("r", encoding="utf-8") as stream:
            speech_contract = json.load(stream)
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot read speech/intertext contract: {exc}", file=sys.stderr)
        return 1
    try:
        with args.extension_contract.open("r", encoding="utf-8") as stream:
            extension_contract = json.load(stream)
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot read extension attestation contract: {exc}", file=sys.stderr)
        return 1
    try:
        with args.core_names_contract.open("r", encoding="utf-8") as stream:
            core_contract = json.load(stream)
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot read core name/lexeme contract: {exc}", file=sys.stderr)
        return 1
    issues = (validate(data) + validate_extension(extension, data) +
              validate_source_access(sources) + validate_apocalyptic(data, extension) +
              validate_prophetic_namings(data) +
              validate_six_title_attestations(data, title_contract) +
              validate_memorial_attestations(data, memorial_contract) +
              validate_speech_intertext(data, speech_contract) +
              validate_extension_attestations(extension, extension_contract) +
              validate_core_name_lexeme(data, core_contract) +
              validate_full_coverage(data, extension))
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
