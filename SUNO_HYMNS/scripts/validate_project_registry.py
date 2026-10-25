#!/usr/bin/env python3
"""Read-only, fail-closed consistency checks for the SUNO_HYMNS project registries."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "SUNO_HYMNS"

EVIDENCE_CLASSES = {"A1", "A2", "A3", "B1", "C", "D"}
ACCESS_STATES = {"FULL_OBJECT_VERIFIED", "PARTIAL_OBJECT", "CATALOG_ONLY", "LINK_ONLY", "NOT_ACQUIRED"}
LOCATOR_STATES = {"EXACT_LOCATOR_VERIFIED", "COARSE_LOCATOR_ONLY", "LOCATOR_MISSING"}
RIGHTS_STATES = {"PUBLICATION_ELIGIBLE", "STORAGE_ONLY", "PRIVATE_STUDY_ONLY", "PERMISSION_REQUIRED", "RIGHTS_UNKNOWN"}
PUBLICATION_STATES = {"PROMOTE", "REFERENCE", "SUPERSEDED", "BLOCKED"}
HOLDS = {"EVIDENCE_HOLD", "LOCATOR_HOLD", "ARCHIVE_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"}
PRODUCTION_STATES = {
    "NOT_STARTED", "RESEARCH_IN_PROGRESS", "LYRIC_DRAFT", "SUNO_OUTPUT_GENERATED",
    "ASSETS_PREPARED", "READY_FOR_REVIEW", "PUBLISHED_VERIFIED", "BLOCKED",
}
PUBLIC_RELEASE_STATES = {"UNKNOWN_NOT_VERIFIED", "PUBLISHED_VERIFIED"}
WORK_TYPES = {
    "DEVOTIONAL_SONG_WITH_TUNE_DIRECTION",
    "LATER_HYMNBOOK_REWORKING",
    "SONNET_MODERN_MUSICAL_SETTING",
}
CLAIM_STATES = {
    "SUPPORTED_WITH_SCOPE_LIMITS",
    "SUPPORTED_BY_SECONDARY_SOURCE_NEEDS_COLLATION",
    "EVIDENCE_HOLD",
    "RESEARCH_OPEN",
    "REPORTED_NOT_INDEPENDENTLY_VERIFIED",
}


def load_json(relative: str, errors: list[str]) -> dict[str, Any]:
    path = PROJECT / relative
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{relative}: cannot load valid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{relative}: root must be a JSON object")
        return {}
    if value.get("schemaVersion") != 1:
        errors.append(f"{relative}: schemaVersion must be 1")
    return value


def unique_ids(items: Any, field: str, label: str, errors: list[str]) -> set[str]:
    if not isinstance(items, list):
        errors.append(f"{label}: expected an array")
        return set()
    values: list[str] = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get(field), str) or not item[field]:
            errors.append(f"{label}: every item needs a non-empty {field}")
            continue
        values.append(item[field])
    if len(values) != len(set(values)):
        errors.append(f"{label}: duplicate {field} values")
    return set(values)


def check_source_states(sources: list[dict[str, Any]], errors: list[str]) -> None:
    for source in sources:
        label = f"source {source.get('id', '<unknown>')}"
        checks = (
            ("evidenceClass", EVIDENCE_CLASSES),
            ("accessState", ACCESS_STATES),
            ("locatorState", LOCATOR_STATES),
            ("rightsState", RIGHTS_STATES),
            ("publicationState", PUBLICATION_STATES),
        )
        for field, allowed in checks:
            if source.get(field) not in allowed:
                errors.append(f"{label}: invalid {field}={source.get(field)!r}")
        holds = source.get("holds")
        if not isinstance(holds, list) or any(hold not in HOLDS for hold in holds):
            errors.append(f"{label}: holds must use the canonical global HOLD values")
        elif source.get("rightsState") == "RIGHTS_UNKNOWN" and "RIGHTS_HOLD" not in holds:
            errors.append(f"{label}: RIGHTS_UNKNOWN must retain RIGHTS_HOLD")
        if source.get("accessState") == "NOT_ACQUIRED" and source.get("locatorState") == "EXACT_LOCATOR_VERIFIED":
            errors.append(f"{label}: NOT_ACQUIRED conflicts with EXACT_LOCATOR_VERIFIED")


def check_refs(records: list[dict[str, Any]], field: str, known: set[str], label: str, errors: list[str]) -> None:
    for record in records:
        values = record.get(field, [])
        if not isinstance(values, list):
            errors.append(f"{label} {record.get('id')}: {field} must be an array")
            continue
        for value in values:
            if value not in known:
                errors.append(f"{label} {record.get('id')}: unknown {field} reference {value}")


def main() -> int:
    errors: list[str] = []
    sources_doc = load_json("data/source-registry-v1.json", errors)
    authors_doc = load_json("data/author-registry-v1.json", errors)
    tracks_doc = load_json("data/track-catalog-v1.json", errors)
    claims_doc = load_json("data/claim-ledger-v1.json", errors)
    songbooks_doc = load_json("data/songbook-registry-v1.json", errors)

    sources = sources_doc.get("sources", [])
    authors = authors_doc.get("authors", [])
    tracks = tracks_doc.get("works", [])
    claims = claims_doc.get("claims", [])
    songbooks = songbooks_doc.get("songbooks", [])

    source_ids = unique_ids(sources, "id", "sources", errors)
    author_ids = unique_ids(authors, "id", "authors", errors)
    track_ids = unique_ids(tracks, "id", "tracks", errors)
    claim_ids = unique_ids(claims, "id", "claims", errors)
    songbook_ids = unique_ids(songbooks, "id", "songbooks", errors)

    if set(claims_doc.get("claimStatusVocabulary", [])) != CLAIM_STATES:
        errors.append("claim ledger: claimStatusVocabulary differs from its allowed state set")

    check_source_states(sources, errors)
    check_refs(authors, "sourceIds", source_ids, "author", errors)
    check_refs(tracks, "sourceIds", source_ids, "track", errors)
    check_refs(songbooks, "sourceIds", source_ids, "songbook", errors)
    check_refs(claims, "sourceIds", source_ids, "claim", errors)

    for track in tracks:
        label = f"track {track.get('id')}"
        if track.get("authorId") not in author_ids:
            errors.append(f"{label}: unknown authorId {track.get('authorId')!r}")
        if track.get("workType") not in WORK_TYPES:
            errors.append(f"{label}: unknown project workType {track.get('workType')!r}")
        if track.get("productionState") not in PRODUCTION_STATES:
            errors.append(f"{label}: invalid productionState")
        if track.get("publicPublicationStatus") not in PUBLIC_RELEASE_STATES:
            errors.append(f"{label}: invalid publicPublicationStatus")
        for reviser in track.get("reviserIds", []):
            if reviser not in author_ids:
                errors.append(f"{label}: unknown reviserId {reviser!r}")
        for version in track.get("versions", []):
            if version.get("promptCapture") != "NOT_CAPTURED":
                # If prompts are later acquired, the exact verbatim artifact and its review record must be committed too.
                if not version.get("promptText") or not version.get("promptSource"):
                    errors.append(f"{label}: prompt capture cannot be promoted without promptText and promptSource")
        if track.get("publicPublicationStatus") == "PUBLISHED_VERIFIED" and not track.get("publicationReceipts"):
            errors.append(f"{label}: PUBLISHED_VERIFIED needs at least one checked publication receipt")

    for claim in claims:
        if claim.get("claimStatus") not in CLAIM_STATES:
            errors.append(f"claim {claim.get('id')}: unknown claimStatus")
        if any(hold not in HOLDS for hold in claim.get("holds", [])):
            errors.append(f"claim {claim.get('id')}: non-canonical HOLD")
        if claim.get("claimStatus") == "EVIDENCE_HOLD" and "EVIDENCE_HOLD" not in claim.get("holds", []):
            errors.append(f"claim {claim.get('id')}: EVIDENCE_HOLD status must carry typed EVIDENCE_HOLD")

    for book in songbooks:
        label = f"songbook {book.get('id')}"
        for field, allowed in (
            ("evidenceClass", EVIDENCE_CLASSES),
            ("accessState", ACCESS_STATES),
            ("locatorState", LOCATOR_STATES),
            ("rightsState", RIGHTS_STATES),
            ("publicationState", PUBLICATION_STATES),
        ):
            if book.get(field) not in allowed:
                errors.append(f"{label}: invalid {field}")
        if any(hold not in HOLDS for hold in book.get("holds", [])):
            errors.append(f"{label}: non-canonical HOLD")
        if book.get("rightsState") == "RIGHTS_UNKNOWN" and "RIGHTS_HOLD" not in book.get("holds", []):
            errors.append(f"{label}: RIGHTS_UNKNOWN must retain RIGHTS_HOLD")
        if book.get("accessState") == "NOT_ACQUIRED" and book.get("locatorState") == "EXACT_LOCATOR_VERIFIED":
            errors.append(f"{label}: NOT_ACQUIRED conflicts with EXACT_LOCATOR_VERIFIED")

    # The validator is deliberately read-only: no write calls or repair behavior.
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        "SUNO_HYMNS registry validation passed: "
        f"{len(source_ids)} sources, {len(author_ids)} authors, {len(track_ids)} tracks, "
        f"{len(claim_ids)} claims, {len(songbook_ids)} songbooks. Read-only."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
