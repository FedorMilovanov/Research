#!/usr/bin/env python3
"""Read-only, fail-closed consistency checks for the SUNO_HYMNS project registries.

Beyond per-record state validation this gate checks that the Markdown view and the JSON
registry have not drifted apart, that every source and every claim has a traceable link to
a work or an explicit project-level role, and that a recorded prompt is byte-identical to
the one published in its production package.
"""
from __future__ import annotations

import json
import re
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
    "BIBLICAL_CANTICLE_OR_SCRIPTURE_EXPANSION",
    # The ancient-hymn lane: a whole pre-Reformation Greek or Latin hymn, carried as a
    # text with a named witness rather than as a poem with a printed tune direction.
    "ANCIENT_GREEK_LAMPLIGHTING_HYMN",
    # Added 2026-10-26 for PHOS-007: a Greek hymn in classical quantitative metre that
    # closes a prose treatise. It is carried as a candidate rather than as a track — no
    # witness of liturgical use, no melody, and the text itself unsettled between editions.
    "ANCIENT_GREEK_TREATISE_EPILOGUE_HYMN",
}
CANDIDATE_STATES = {"OPEN", "ACTIVATED", "REJECTED", "SUPERSEDED"}
CLAIM_STATES = {
    "SUPPORTED_WITH_SCOPE_LIMITS",
    "SUPPORTED_BY_SECONDARY_SOURCE_NEEDS_COLLATION",
    "EVIDENCE_HOLD",
    "RESEARCH_OPEN",
    "REPORTED_NOT_INDEPENDENTLY_VERIFIED",
    # a claim that was looked for in a primary text and found to be false: stronger
    # than REPORTED_NOT_INDEPENDENTLY_VERIFIED, weaker than a positive SUPPORTED state
    "VERIFIED_NEGATIVE",
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
        if source.get("rightsState") == "PERMISSION_REQUIRED" and "RIGHTS_HOLD" not in holds:
            errors.append(f"{label}: PERMISSION_REQUIRED must retain RIGHTS_HOLD")
        if source.get("accessState") == "NOT_ACQUIRED" and source.get("locatorState") == "EXACT_LOCATOR_VERIFIED":
            errors.append(f"{label}: NOT_ACQUIRED conflicts with EXACT_LOCATOR_VERIFIED")
        if not source.get("supports"):
            errors.append(f"{label}: must state what the source supports")


def check_refs(records: list[dict[str, Any]], field: str, known: set[str], label: str, errors: list[str]) -> None:
    for record in records:
        values = record.get(field, [])
        if not isinstance(values, list):
            errors.append(f"{label} {record.get('id')}: {field} must be an array")
            continue
        for value in values:
            if value not in known:
                errors.append(f"{label} {record.get('id')}: unknown {field} reference {value}")


def check_version_ids(tracks: list[dict[str, Any]], errors: list[str]) -> set[str]:
    """Version IDs must be unique across the whole catalog, not only within a work."""
    seen: dict[str, str] = {}
    for track in tracks:
        versions = track.get("versions", [])
        if not isinstance(versions, list):
            errors.append(f"track {track.get('id')}: versions must be an array")
            continue
        for version in versions:
            version_id = version.get("versionId")
            if not isinstance(version_id, str) or not version_id:
                errors.append(f"track {track.get('id')}: every version needs a versionId")
                continue
            if version_id in seen:
                errors.append(
                    f"version {version_id}: duplicate versionId (also in track {seen[version_id]})"
                )
            seen[version_id] = str(track.get("id"))
    return set(seen)


def check_reported_assets(tracks: list[dict[str, Any]], errors: list[str]) -> None:
    """A prepared asset must be represented by at least one version, and no version may claim
    prepared audio while its own asset map is empty."""
    for track in tracks:
        label = f"track {track.get('id')}"
        if track.get("productionState") == "ASSETS_PREPARED" and not track.get("versions"):
            errors.append(f"{label}: ASSETS_PREPARED needs at least one version record")
        for version in track.get("versions", []):
            version_id = version.get("versionId")
            has_assets = bool(version.get("assets"))
            if version.get("audioExport") == "NONE" and has_assets:
                errors.append(
                    f"{label}/{version_id}: audioExport NONE contradicts a populated assets map"
                )
            if version.get("generatedOutput") == "NONE" and version.get("assets"):
                errors.append(
                    f"{label}/{version_id}: assets recorded while generatedOutput is NONE"
                )


def check_prompt_verbatim(tracks: list[dict[str, Any]], errors: list[str]) -> None:
    """A prompt recorded in JSON must exist byte-identically in its published package.

    This is the only defence against a registry prompt and a documented prompt diverging,
    which would make every downstream version ID unreliable.
    """
    for track in tracks:
        for version in track.get("versions", []):
            prompt_text = version.get("promptText")
            if not prompt_text:
                continue
            package = version.get("productionPackage")
            if not package:
                errors.append(
                    f"version {version.get('versionId')}: promptText present but no productionPackage to check it against"
                )
                continue
            # The style prompt may live in a dedicated style document rather than in the
            # production package: SUNO/README.md requires the lyric, the SUNO-ready text
            # and the style to be kept apart. Any document listed in promptDocuments is
            # accepted, and the prompt must appear verbatim in at least one of them.
            documents = [package] + list(version.get("promptDocuments") or [])
            found = False
            read_any = False
            for document in documents:
                try:
                    content = (PROJECT / document).read_text(encoding="utf-8")
                except OSError as exc:
                    if document == package:
                        errors.append(
                            f"version {version.get('versionId')}: cannot read {document}: {exc}"
                        )
                    else:
                        errors.append(
                            f"version {version.get('versionId')}: cannot read prompt document {document}: {exc}"
                        )
                    continue
                read_any = True
                if prompt_text in content:
                    found = True
                    break
            if read_any and not found:
                errors.append(
                    f"version {version.get('versionId')}: promptText is not verbatim in any of {documents}"
                )


def check_sources_are_used(
    sources: list[dict[str, Any]],
    referrers: dict[str, list[dict[str, Any]]],
    errors: list[str],
) -> None:
    """Every registered source must be pointed at by something; an orphan source is an
    unreviewed claim waiting to happen."""
    used: set[str] = set()
    for records in referrers.values():
        for record in records:
            used.update(record.get("sourceIds", []) or [])
    for source in sources:
        if source.get("id") not in used:
            errors.append(f"source {source.get('id')}: registered but not referenced by any claim, work, author or songbook")


def check_claims_linked(
    claims: list[dict[str, Any]], tracks: list[dict[str, Any]], errors: list[str]
) -> None:
    """Each claim is either used by a work or explicitly declared project-level.

    A claim with neither is a fact with no traceable consequence, which is what this gate
    exists to prevent.
    """
    referenced: set[str] = set()
    for track in tracks:
        referenced.update(track.get("claimIds", []) or [])
    for claim in claims:
        claim_id = claim.get("id")
        if claim.get("projectLevel") is True:
            continue
        if claim_id not in referenced:
            errors.append(
                f"claim {claim_id}: not referenced by any work claimIds and not marked projectLevel"
            )
    for claim in claims:
        if claim.get("claimStatus") == "EVIDENCE_HOLD":
            gap = claim.get("evidenceGap")
            next_check = claim.get("nextCheck")
            if not isinstance(gap, str) or not gap.strip():
                errors.append(f"claim {claim.get('id')}: EVIDENCE_HOLD must state evidenceGap")
            if not isinstance(next_check, str) or not next_check.strip():
                errors.append(f"claim {claim.get('id')}: EVIDENCE_HOLD must state nextCheck")


def check_candidates(
    tracks_doc: dict[str, Any], tracks: list[dict[str, Any]], errors: list[str]
) -> None:
    """The backlog list in JSON must mirror the backlog Markdown exactly.

    Both directions are checked: an ID that exists only in the Markdown would let a future
    agent re-open an already activated candidate, and an ID only in the JSON would be an
    invisible candidate nobody can find.
    """
    candidates = tracks_doc.get("candidates", [])
    candidate_ids = unique_ids(candidates, "id", "candidates", errors)
    track_ids = {track.get("id") for track in tracks}

    for candidate in candidates:
        state = candidate.get("status")
        if state not in CANDIDATE_STATES:
            errors.append(f"candidate {candidate.get('id')}: invalid status {state!r}")
        if state == "ACTIVATED":
            target = candidate.get("activatedAsTrackId")
            if target not in track_ids:
                errors.append(
                    f"candidate {candidate.get('id')}: ACTIVATED must name an existing activatedAsTrackId"
                )
        elif candidate.get("activatedAsTrackId"):
            errors.append(
                f"candidate {candidate.get('id')}: only ACTIVATED candidates may name a track"
            )

    backlog = PROJECT / "RESEARCH" / "DUTCH_HYMN_BACKLOG.md"
    try:
        backlog_ids = set(re.findall(r"DUTCH-CAND-\d{3}", backlog.read_text(encoding="utf-8")))
    except OSError as exc:
        errors.append(f"cannot read the backlog Markdown: {exc}")
        backlog_ids = set()
    if backlog_ids != candidate_ids:
        missing = sorted(backlog_ids - candidate_ids)
        extra = sorted(candidate_ids - backlog_ids)
        errors.append(
            "backlog Markdown and track-catalog candidates disagree"
            f" (markdown-only={missing}, json-only={extra})"
        )

    # Two catalogs, one works list: the Dutch lane and the ancient-hymn lane are kept
    # apart on the page and together in the registry. An ID that appears in neither, or
    # twice, must fail here rather than go invisible.
    catalogs = (
        PROJECT / "RESEARCH" / "DUTCH_HYMN_CATALOG.md",
        PROJECT / "RESEARCH" / "ANCIENT_HYMNS_CATALOG.md",
    )
    catalog_ids: set[str] = set()
    seen_ids: list[str] = []
    for catalog in catalogs:
        try:
            found = re.findall(
                r"^##\s+([A-Z]{2,10}-\d{3})\b", catalog.read_text(encoding="utf-8"), re.MULTILINE
            )
        except OSError as exc:
            errors.append(f"cannot read the catalog Markdown {catalog.name}: {exc}")
            continue
        seen_ids.extend(found)
        catalog_ids.update(found)
    if len(seen_ids) != len(set(seen_ids)):
        errors.append("the same work ID is catalogued in more than one catalog file")
    if catalog_ids != track_ids:
        missing = sorted(catalog_ids - track_ids)
        extra = sorted(track_ids - catalog_ids)
        errors.append(
            "catalog Markdown and track-catalog works disagree"
            f" (markdown-only={missing}, json-only={extra})"
        )


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
    check_refs(tracks, "claimIds", claim_ids, "track", errors)
    check_refs(tracks, "reviserIds", author_ids, "track", errors)

    check_version_ids(tracks, errors)
    check_reported_assets(tracks, errors)
    check_prompt_verbatim(tracks, errors)
    check_claims_linked(claims, tracks, errors)
    check_candidates(tracks_doc, tracks, errors)
    check_sources_are_used(
        sources,
        {"authors": authors, "tracks": tracks, "songbooks": songbooks, "claims": claims},
        errors,
    )

    as_of = {
        name: doc.get("asOf")
        for name, doc in (
            ("track-catalog", tracks_doc),
            ("source-registry", sources_doc),
            ("author-registry", authors_doc),
            ("claim-ledger", claims_doc),
            ("songbook-registry", songbooks_doc),
        )
    }
    if len(set(as_of.values())) != 1:
        errors.append(f"registries disagree on asOf: {as_of}")

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
        if book.get("rightsState") == "PERMISSION_REQUIRED" and "RIGHTS_HOLD" not in book.get("holds", []):
            errors.append(f"{label}: PERMISSION_REQUIRED must retain RIGHTS_HOLD")
        if not book.get("sourceIds"):
            errors.append(f"{label}: must cite at least one source")
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
