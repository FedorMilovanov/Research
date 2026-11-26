#!/usr/bin/env python3
"""Read-only, fail-closed editorial crosswalk for Names of God reader pilots.

Confirms section headings, typed Research claim/source references and editorial
publication gates. DOES NOT independently validate Hebrew, paleography,
theological truth, copyright or scholarly review.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CROSSWALK = ROOT / "data/names_reader_claim_crosswalk_v1.json"
CLAIMS = ROOT / "data/names_claim_registry_v1.json"
SOURCES = ROOT / "data/source_access_register_v1.json"
EXPECTED_READER_FILES = {
    "CH-PILOT-01": "reader/CH-PILOT-01_WHAT_SCRIPTURE_CALLS_GODS_NAME.md",
    "CH-PILOT-02": "reader/CH-PILOT-02_YHWH_EHYEH_EXODUS_3_6.md",
    "CH-PILOT-03": "reader/CH-PILOT-03_EL_ELOHIM_SHADDAI.md",
}
WORD_BUDGETS = {"CH-PILOT-01": 3200, "CH-PILOT-02": 3200, "CH-PILOT-03": 3600}
# Three direct modern printed-MT verse surfaces, not attestation or critical apparatus.
CH03_UNMAPPED_MT_LOCI = (
    ("Ruth 1:20–21", "https://mechon-mamre.org/p/pt/pt2901.htm",
     "NAOMI_GRIEF_HUMAN_SPEECH_NOT_DIVINE_SELF_IDENTIFICATION"),
    ("Job 5:17", "https://mechon-mamre.org/p/pt/pt2705.htm",
     "ELIPHAZ_ADMONITION_HUMAN_SPEECH_NOT_DIVINE_SPEECH"),
    ("Job 42:7–9", "https://mechon-mamre.org/p/pt/pt2742.htm",
     "YHWH_REBUKES_THREE_FRIENDS_NO_BLANKET_DENIAL_OF_EVERY_ELIPHAZ_SENTENCE"),
)

# Independently checked digital-MT verse excerpts, scoped editorial assertions only.
# These READ-prefixed IDs are NOT registered CLM or ATT IDs; peer review is absent.
CH03_PROVISIONAL_ASSERTIONS = (
    ("READ-CH03-RUTH1-20-21", "Ruth 1:20–21", "וְשַׁדַּי הֵרַע לִי",
     "Naomi speaks in first person about Shaddai as the cause of her suffering; she also mentions YHWH in the same lament. This is narrated human speech, not a direct divine self-designation.",
     "Do not promote Naomi's grief statement to YHWH's self-description or a guaranteed conclusion that the narrator endorses Naomi's entire evaluation."),
    ("READ-CH03-JOB5-17", "Job 5:17", "וּמוּסַר שַׁדַּי",
     "Eliphaz, a human speaker in dialogue, speaks of Shaddai's discipline while referring to Eloah in the same verse. The narrator does not present this sentence as a direct oracle of YHWH.",
     "Do not treat all of Eliphaz's instruction as automatically endorsed by God merely because it uses Shaddai or Eloah."),
    ("READ-CH03-JOB42-7-9", "Job 42:7–9", "לֹא דִבַּרְתֶּם אֵלַי נְכוֹנָה",
     "The narrator explicitly represents YHWH as rebuking Eliphaz and his two companions for their speech and commanding them to seek Job's intercession.",
     "Do not infer universal logical negation of every earlier Eliphaz sentence; speaking to/about God and the rebuke's precise scope remain contested."),
)

ROLES = {
    "EXACT_RESEARCH_CLAIM_MATCH",
    "SECONDARY_ATTRIBUTED_NOT_IN_CLAIM_GRAPH",
    "EVIDENCE_MAPPED_WITH_SCHOLARLY_GAP",
    "BIBLICAL_LOCI_NOT_IN_LOCKED_105_ATTESTATIONS",
}


def reader_words(text: str) -> int:
    """Operational word count: whitespace tokens in the reader portion only."""
    return len(text.split())


def validate_reader_crosswalk(
    crosswalk: dict,
    claims: dict,
    sources: dict,
    reader_texts: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    if not isinstance(crosswalk, dict):
        return ["reader: crosswalk must be an object"]
    if (crosswalk.get("schemaVersion") != 1
            or crosswalk.get("id") != "NAMES_READER_CHAPTER_CLAIM_CROSSWALK_V1"
            or crosswalk.get("authority") != "ИМЕНА БОГА/data/names_claim_registry_v1.json"):
        errors.append("reader: schema and source authority must not drift")
    if (crosswalk.get("status") != "INTERNAL_RESEARCH_EDITORIAL_TRACE_ONLY_NOT_SCHOLARLY_PEER_REVIEW_OR_PUBLICATION_APPROVAL"
            or crosswalk.get("publicationState") != "BLOCKED"
            or crosswalk.get("independentScholarlyReviewsAccepted") != 0
            or crosswalk.get("productApprovals") != 0
            or crosswalk.get("criticalManuscriptCollationsCompleted") != 0
            or crosswalk.get("rightsClearanceGranted") is not False):
        errors.append("reader: crosswalk cannot grant scientific, rights or Product approvals")
    if len(crosswalk.get("knownHolds", [])) < 4:
        errors.append("reader: known manuscript, rights and source-gaps cannot disappear")
    chapter_rows = crosswalk.get("chapters")
    if not isinstance(chapter_rows, list):
        return errors + ["reader: chapters must be a list"]
    chapter_ids = [c.get("chapterId") for c in chapter_rows if isinstance(c, dict)]
    if (len(chapter_rows) != 3
            or set(chapter_ids) != set(EXPECTED_READER_FILES)
            or len(set(chapter_ids)) != len(chapter_rows)
            or crosswalk.get("readerChapterCount") != 3):
        errors.append("reader: exactly three unique original pilot chapters required")

    by_claim_id = {c["claimId"]: c for c in claims.get("records", [])
                   if isinstance(c, dict) and isinstance(c.get("claimId"), str)}
    by_source_id = {s["id"]: s for s in sources.get("records", [])
                    if isinstance(s, dict) and isinstance(s.get("id"), str)}
    all_sections = 0
    for chapter in chapter_rows:
        if not isinstance(chapter, dict):
            errors.append("reader: malformed chapter row")
            continue
        cid = chapter.get("chapterId")
        expected_file = EXPECTED_READER_FILES.get(cid)
        if not expected_file:
            continue
        if chapter.get("path") != expected_file:
            errors.append(f"reader: {cid} reader path drifted")
        if chapter.get("maxReaderWords") != WORD_BUDGETS[cid]:
            errors.append(f"reader: {cid} fixed reader-length budget changed")
        text = reader_texts.get(expected_file, "")
        marker = "## Редакторский аппарат"
        if not text or text.count(marker) != 1:
            errors.append(f"reader: {cid} separate editor apparatus missing or duplicated")
            continue
        reading, appendix = text.split(marker, 1)
        if "NOT EDITORIAL_READY" not in reading and "NOT EDITORIAL_READY" not in appendix:
            errors.append(f"reader: {cid} editorial hold removed")
        if "PUBLICATION_BLOCKED" not in reading and "PUBLICATION_HOLD" not in reading:
            errors.append(f"reader: {cid} reader publication boundary removed")
        if reader_words(reading) > WORD_BUDGETS[cid]:
            errors.append(f"reader: {cid} main reader narrative exceeds word budget")
        heading_matches = list(re.finditer(r"^### (.+?)\s*$", reading, flags=re.MULTILINE))
        headings = [m.group(1) for m in heading_matches]
        section_bodies = {
            match.group(1): reading[
                match.end():(
                    heading_matches[i + 1].start()
                    if i + 1 < len(heading_matches) else len(reading)
                )
            ]
            for i, match in enumerate(heading_matches)
        }
        sections = chapter.get("sections", [])
        if not isinstance(sections, list):
            errors.append(f"reader: {cid} sections not a list")
            continue
        listed = [x.get("heading") for x in sections if isinstance(x, dict)]
        if listed != headings or len(listed) != len(sections) or len(set(listed)) != len(listed):
            errors.append(f"reader: {cid} actual narrative headings and section map differ")
        all_sections += len(sections)
        for row in sections:
            if not isinstance(row, dict):
                errors.append(f"reader: {cid} malformed section")
                continue
            heading = row.get("heading")
            role = row.get("editorialRole")
            if role not in ROLES:
                errors.append(f"reader: {cid}/{heading} unknown evidence role")
            ids = row.get("claimIds")
            if not isinstance(ids, list) or len(ids) != len(set(ids)):
                errors.append(f"reader: {cid}/{heading} missing or duplicate claim list")
                continue
            missing = [x for x in ids if x not in by_claim_id]
            if missing:
                errors.append(f"reader: {cid}/{heading} orphaned registered claim ID(s)")
            referenced_sources: set[str] = set()
            for claim_id in ids:
                claim = by_claim_id.get(claim_id)
                if not claim:
                    continue
                referenced_sources.update(claim.get("sourceIds", []))
                if (claim.get("editorialState") != "RESEARCH_HOLD"
                        or claim.get("publicationState") != "BLOCKED"
                        or claim.get("criticalWitnessStatus") != "NOT_COLLATED"):
                    errors.append(f"reader: {cid}/{heading} cannot promote mapped research-held claim")
            stored_sources = row.get("claimSourceIds")
            if (not isinstance(stored_sources, list)
                    or stored_sources != sorted(referenced_sources)):
                errors.append(f"reader: {cid}/{heading} stored claim-source trace differs")
            supplements = row.get("supplementalSourceIds", [])
            if (not isinstance(supplements, list) or len(set(supplements)) != len(supplements)
                    or any(x not in by_source_id for x in supplements)):
                errors.append(f"reader: {cid}/{heading} unsupported supplemental source")
            if any(x not in by_source_id for x in referenced_sources):
                errors.append(f"reader: {cid}/{heading} claim points to nonexistent source")
            for source_id in set(supplements) | referenced_sources:
                source = by_source_id.get(source_id)
                if source and source.get("publicationState") != "BLOCKED":
                    errors.append(f"reader: {cid}/{heading} source was prematurely promoted")
            if "directTextLoci" in row and not (
                    cid == "CH-PILOT-03"
                    and heading == "Когда «Шаддай» звучит без «Эль»"):
                errors.append("reader: direct digital-MT trace illegally attached to unrelated section")
            if cid == "CH-PILOT-03" and heading == "Когда «Шаддай» звучит без «Эль»":
                seow = by_source_id.get("SRC-SEOW-INTERPRETATION-2026-JOB42-7-10-DIVINE-ANGER", {})
                if (row.get("supplementalSourceIds") != ["SRC-SEOW-INTERPRETATION-2026-JOB42-7-10-DIVINE-ANGER"]
                        or seow.get("sourceRole") !=
                        "SEOW2026_ORIGINAL_JOURNAL_JOB42_7_10_MULTIPLE_SCHOLARLY_INTERPRETATIONS_NOT_CRITICAL_GREEK_HEBREW_COLLATION"
                        or seow.get("evidenceClass") != "B1"
                        or seow.get("criticalEditionCollated") is not False
                        or seow.get("rightsState") != "PERMISSION_REQUIRED"
                        or seow.get("publicationState") != "BLOCKED"):
                    errors.append("reader: CH03 Seow commentary attribution/status drifted")
                if ("https://journals.sagepub.com/doi/full/10.1177/00209643251410214" not in appendix
                        or "Сеоу" not in appendix
                        or "SOURCE_GRAPH_HOLD" not in appendix):
                    errors.append("reader: CH03 Seow original journal review boundary missing")
                provisional = [
                    {
                        "id": assertion_id,
                        "locus": locus,
                        "sourceId": "SRC-MT-MECHON",
                        "hebrewExcerpt": excerpt,
                        "boundedAssertion": statement,
                        "prohibitedInference": boundary,
                        "state": "PROVISIONAL_DIGITAL_MT_READER_ASSERTION_NOT_LOCKED_CLM_ATT",
                        "publicationState": "BLOCKED",
                    }
                    for assertion_id, locus, excerpt, statement, boundary
                    in CH03_PROVISIONAL_ASSERTIONS
                ]
                if row.get("provisionalReaderAssertions") != provisional:
                    errors.append("reader: CH03 Ruth/Job provisional source-located assertions drifted")
                if any(excerpt not in appendix for _, _, excerpt, _, _ in CH03_PROVISIONAL_ASSERTIONS):
                    errors.append("reader: CH03 Ruth/Job exact original-script excerpt missing from editorial apparatus")
                if any(r["locus"] != original["locus"]
                       for r, original in zip(provisional, row.get("directTextLoci", []))):
                    errors.append("reader: CH03 Ruth/Job provisional assertion to verse map drifted")
                expected = [
                    {
                        "locus": locus,
                        "sourceId": "SRC-MT-MECHON",
                        "url": url,
                        "speakerAndForce": speech_role,
                        "witnessScope": "MODERN_EDITED_HEBREW_TEXT_NOT_CRITICAL_MANUSCRIPT_COLLATION",
                        "claimGraphStatus": "NO_STANDALONE_LOCKED_ATT_OR_CLM",
                    }
                    for locus, url, speech_role in CH03_UNMAPPED_MT_LOCI
                ]
                if (row.get("directTextLoci") != expected
                        or ids != [] or stored_sources != []
                        or role != "BIBLICAL_LOCI_NOT_IN_LOCKED_105_ATTESTATIONS"):
                    errors.append("reader: CH03 Ruth/Job direct digital-MT trace drifted")
                src = by_source_id.get("SRC-MT-MECHON", {})
                if (src.get("evidenceClass") != "B1" or src.get("accessState") != "PARTIAL_OBJECT"
                        or src.get("sourceRole") != "DIGITAL_TEXT_SURFACE_ONLY"
                        or src.get("criticalEditionCollated") is not False
                        or src.get("publicationState") != "BLOCKED"):
                    errors.append("reader: CH03 Ruth/Job modern MT source was falsely upgraded")
                own_section = section_bodies.get(heading, "")
                if any(
                        own_section.count(f"]({url})") != 1
                        for _, url, _ in CH03_UNMAPPED_MT_LOCI):
                    errors.append(
                        "reader: CH03 Ruth/Job source hyperlink must appear exactly once "
                        "inside its own narrative section"
                    )
                if "SOURCE_GRAPH_HOLD" not in (row.get("unresolvedArgumentBoundary") or ""):
                    errors.append("reader: CH03 Ruth/Job graph HOLD removed")
            gap = row.get("unresolvedArgumentBoundary")
            if not ids and role not in {
                "SECONDARY_ATTRIBUTED_NOT_IN_CLAIM_GRAPH",
                "BIBLICAL_LOCI_NOT_IN_LOCKED_105_ATTESTATIONS",
            }:
                errors.append(f"reader: {cid}/{heading} unproved section lacks explicit gap role")
            if role != "EXACT_RESEARCH_CLAIM_MATCH" and (
                    not isinstance(gap, str) or len(gap.strip()) < 60):
                errors.append(f"reader: {cid}/{heading} uncertainty or claim gap not explained")
        if cid == "CH-PILOT-03":
            marker = chapter.get("requiredAppendixHeading")
            if marker != "Исследовательское приложение — Дейр-Алла: первичные отчёты, реконструкции, споры и изображения":
                errors.append("reader: CH03 authoritative research appendix ID drifted")
            if (not marker or marker not in appendix or reading.count("![") != 1
                    or appendix.count("![") < 2 or chapter.get("maxEmbeddedImagesInReader") != 1):
                errors.append("reader: CH03 Deir Alla image and original research preservation failed")
            if not all(x in appendix for x in ("GrN-", "Хакетт", "1976", "2019", "Фогеля")):
                errors.append("reader: CH03 Deir Alla detailed research evidence missing")
            if "tal_dayr_alla_bileam_jordanmus.jpg" not in reading:
                errors.append("reader: CH03 original museum photo replaced by an unaudited reconstruction")
            if "Дейр-Алла: древняя находка и пределы сравнения" not in reading:
                errors.append("reader: CH03 scientifically scoped concise evidence bridge missing")
    if (all_sections != 32 or crosswalk.get("selectedSectionCount") != 32):
        errors.append("reader: evidence section inventory no longer 32 actual reader headings")
    return errors


def main() -> int:
    try:
        crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
        claims = json.loads(CLAIMS.read_text(encoding="utf-8"))
        sources = json.loads(SOURCES.read_text(encoding="utf-8"))
        readers = {
            path: (ROOT / path).read_text(encoding="utf-8")
            for path in EXPECTED_READER_FILES.values()
        }
        errors = validate_reader_crosswalk(crosswalk, claims, sources, readers)
    except (OSError, ValueError, TypeError) as exc:
        print(f"FAIL: reader crosswalk files invalid: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print("FAIL: " + error, file=sys.stderr)
        return 1
    unique_claims = {
        claim_id for c in crosswalk["chapters"] for row in c["sections"]
        for claim_id in row["claimIds"]
    }
    print(f"PASS: 3 reader chapters, 32 mapped narrative headings, "
          f"{len(unique_claims)} distinct held research claims; "
          "CH03 concise narrative + full research appendix; "
          "no implied peer review, critical edition collation or publication rights")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
