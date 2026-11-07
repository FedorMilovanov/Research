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
    total = sum(len(row.get("attestations", [])) for row in rows if isinstance(row, dict) and isinstance(row.get("attestations", []), list))
    if data.get("auditProtocol", {}).get("patriarchalAttestations", {}).get("totalAttestations") != total:
        errors.append("patriarchal attestation counter drift")
    if total < 11:
        errors.append("core patriarchal attestation set incomplete")
    source_roles = {key: row.get("contextualAssertion", "") for key, row in index.items()}
    for rid in attestations_required:
        if not source_roles.get(rid):
            errors.append(f"{rid}: missing assertion with claim boundary")
    if index.get("el-shaddai", {}).get("attestations", [{}])[-1].get("surface") != "בְּאֵל שַׁדָּי":
        errors.append("Exodus 6:3 precise pointed Shaddai surface changed")
    if index.get("el-bethel", {}).get("attestations", [{}])[0].get("namedObject") != "place":
        errors.append("Genesis 35:7 is place-naming, not altar-naming")

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
        if source.get("rightsState") == "PUBLICATION_ELIGIBLE" and rid != "SRC-VANWOLDE-2021":
            errors.append(f"{prefix}: evidence of a source-level license missing")
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--extension", type=Path, default=EXTENSION)
    parser.add_argument("--sources", type=Path, default=SOURCES)
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
    issues = validate(data) + validate_extension(extension, data) + validate_source_access(sources)
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
