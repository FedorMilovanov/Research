#!/usr/bin/env python3
"""Fail-closed validation of the Heart source-closure registry."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "СЕРИЯ СЕРДЦЕ" / "74_SOURCE_CLOSURE_REGISTRY_2026-08-01.json"

# Trust is policy code, not user-controlled registry data.
TRUSTED_SOURCE_CLASSES = {
    "academic_journal",
    "confessional_primary",
    "official_author_archive",
    "official_media",
    "official_ministry",
    "official_ministry_transcript",
    "official_publisher",
    "primary_scan",
    "primary_text",
    "primary_text_reproduction",
    "primary_text_rights_limited",
}
ALLOWED_UNTRUSTED_CLASSES = {
    "library_catalog",
    "open_reference",
    "primary_bibliographic",
    "public_domain_commentary",
}
ALLOWED_STATUSES = {
    "PRIMARY_VERIFIED",
    "PRIMARY_AUDIO_VERIFIED",
    "OFFICIAL_REPLACEMENT",
    "PARAPHRASE_ONLY",
    "REMOVE",
    "RECEPTION_ONLY",
}
QUOTE_SAFE_STATUSES = {"PRIMARY_VERIFIED", "PRIMARY_AUDIO_VERIFIED", "OFFICIAL_REPLACEMENT"}
REQUIRED_CLAIMS = {
    "CLM-WHITEFIELD-ANECDOTE", "CLM-WHITEFIELD-STONY", "CLM-SPURGEON-FREE-WILL",
    "CLM-SPURGEON-LION-LAMB", "CLM-BAUCHAM-SISSIFIED", "CLM-OWEN-BURN-BIBLES",
    "CLM-HUGHES-EXPULSIVE", "CLM-AUGUSTINE-SPLENDIDA", "CLM-WATSON-MORALITY",
    "CLM-MCHEYNE-TEN-LOOKS", "CLM-KOTZKER-HEART", "CLM-WATSON-PANDECT",
    "CLM-HAMILTON-MONOGRAPH", "CLM-FERGUSON-BOOK", "CLM-ORTLUND-CH15",
    "CLM-ROGERS-ADVICE", "CLM-MLJ-BOOK", "CLM-PDF-LONG-QUOTES",
}

# Exact quote-safe verification contract. Each accepted claim has an identified
# edition/version, a bounded locator, and an explicit context-verification flag.
QUOTE_SAFE_LOCATORS = {
    "CLM-WHITEFIELD-STONY": {
        "edition_or_version": "George Whitefield, Directions How to Hear Sermons, CCEL primary HTML/PDF corpus",
        "locator": "sermon Directions How to Hear Sermons; stony-ground section",
        "context_verified": True,
    },
    "CLM-SPURGEON-FREE-WILL": {
        "edition_or_version": "C. H. Spurgeon official archive",
        "locator": "Sermon No. 224, Samson Conquered",
        "context_verified": True,
    },
    "CLM-BAUCHAM-SISSIFIED": {
        "edition_or_version": "preserved official Brokenness sermon media",
        "locator": "official media clip and contemporaneous corroborating report",
        "context_verified": True,
    },
    "CLM-OWEN-BURN-BIBLES": {
        "edition_or_version": "John Owen, Pneumatologia primary text",
        "locator": "Book I ch. V §II and ch. XII §§V/X; exact replacement passages only",
        "context_verified": True,
    },
    "CLM-MCHEYNE-TEN-LOOKS": {
        "edition_or_version": "Memoir and Remains of Robert Murray M'Cheyne",
        "locator": "printed letter containing the ten-looks wording",
        "context_verified": True,
    },
    "CLM-WATSON-PANDECT": {
        "edition_or_version": "Thomas Watson, Heaven Taken by Storm, 1670 EEBO-TCP",
        "locator": "EEBO-TCP A65299.0001.001, division 1:4",
        "context_verified": True,
    },
    "CLM-FERGUSON-BOOK": {
        "edition_or_version": "official Ligonier teaching transcript",
        "locator": "official transcript passage; no unsupported book-page claim",
        "context_verified": True,
    },
    "CLM-ORTLUND-CH15": {
        "edition_or_version": "Crossway official Q&A and article",
        "locator": "official online Q&A/article passages; no unsupported chapter-page claim",
        "context_verified": True,
    },
    "CLM-ROGERS-ADVICE": {
        "edition_or_version": "Timothy Rogers, A Discourse Concerning Trouble of Mind, 1691 scan",
        "locator": "printed ii/PDF17; xii/PDF27; xiv/PDF29",
        "context_verified": True,
    },
}


def main() -> int:
    errors: list[str] = []
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read registry: {exc}", file=sys.stderr)
        return 1

    sources = data.get("sources")
    claims = data.get("claims")
    minimum = data.get("minimum_unique_sources", 60)
    if not isinstance(sources, list):
        errors.append("sources must be a list")
        sources = []
    if not isinstance(claims, list):
        errors.append("claims must be a list")
        claims = []
    if not isinstance(minimum, int) or minimum < 60:
        errors.append("minimum_unique_sources must be an integer >= 60")

    source_ids: set[str] = set()
    urls: set[str] = set()
    source_by_id: dict[str, dict] = {}
    trusted_count = 0
    allowed_classes = TRUSTED_SOURCE_CLASSES | ALLOWED_UNTRUSTED_CLASSES

    for index, source in enumerate(sources):
        prefix = f"sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in ("id", "author", "work", "url", "class", "format", "use"):
            value = source.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")
        source_id = source.get("id")
        url = source.get("url")
        source_class = source.get("class")
        if isinstance(source_id, str):
            if source_id in source_ids:
                errors.append(f"duplicate source id: {source_id}")
            source_ids.add(source_id)
            source_by_id[source_id] = source
        if isinstance(url, str):
            if url in urls:
                errors.append(f"duplicate source URL: {url}")
            urls.add(url)
            parsed = urlparse(url)
            if parsed.scheme != "https" or not parsed.netloc:
                errors.append(f"{prefix}.url must be absolute HTTPS: {url}")
        if source_class not in allowed_classes:
            errors.append(f"{prefix}.class is not recognized by Heart policy: {source_class!r}")
        if source_class in TRUSTED_SOURCE_CLASSES:
            trusted_count += 1

    if len(source_ids) < minimum:
        errors.append(f"only {len(source_ids)} unique sources; required >= {minimum}")
    if trusted_count < 50:
        errors.append(f"only {trusted_count} trusted sources; required >= 50")

    claim_ids: set[str] = set()
    quote_safe_ids: set[str] = set()
    for index, claim in enumerate(claims):
        prefix = f"claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in ("id", "label", "status", "decision"):
            value = claim.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")
        claim_id = claim.get("id")
        status = claim.get("status")
        quote_safe = claim.get("quote_safe")
        support = claim.get("support")
        if isinstance(claim_id, str):
            if claim_id in claim_ids:
                errors.append(f"duplicate claim id: {claim_id}")
            claim_ids.add(claim_id)
        if status not in ALLOWED_STATUSES:
            errors.append(f"{prefix}.status is not allowed: {status!r}")
        if not isinstance(quote_safe, bool):
            errors.append(f"{prefix}.quote_safe must be boolean")
        if not isinstance(support, list) or not all(isinstance(item, str) for item in support):
            errors.append(f"{prefix}.support must be a list of source IDs")
            support = []
        missing = [item for item in support if item not in source_by_id]
        if missing:
            errors.append(f"{prefix} references missing sources: {missing}")

        if quote_safe:
            quote_safe_ids.add(str(claim_id))
            if status not in QUOTE_SAFE_STATUSES:
                errors.append(f"{prefix} is quote-safe with invalid status {status}")
            if not support:
                errors.append(f"{prefix} is quote-safe but has no support")
            low_trust = [
                item for item in support
                if source_by_id.get(item, {}).get("class") not in TRUSTED_SOURCE_CLASSES
            ]
            if low_trust:
                errors.append(f"{prefix} uses non-trusted quote support: {low_trust}")
            contract = QUOTE_SAFE_LOCATORS.get(str(claim_id))
            if not contract:
                errors.append(f"{prefix} lacks a hardcoded quote-safe locator contract")
            else:
                if not contract.get("locator"):
                    errors.append(f"{prefix} locator is empty")
                if not contract.get("edition_or_version"):
                    errors.append(f"{prefix} edition_or_version is empty")
                if contract.get("context_verified") is not True:
                    errors.append(f"{prefix} context_verified must be true")
        elif status in QUOTE_SAFE_STATUSES:
            errors.append(f"{prefix} has quote-safe status {status} but quote_safe=false")

    missing_claims = sorted(REQUIRED_CLAIMS - claim_ids)
    if missing_claims:
        errors.append(f"required disputed claims missing: {missing_claims}")
    if quote_safe_ids != set(QUOTE_SAFE_LOCATORS):
        errors.append(
            "quote-safe claim set differs from locator contract: "
            f"{sorted(quote_safe_ids ^ set(QUOTE_SAFE_LOCATORS))}"
        )

    counts = data.get("counts", {})
    expected_counts = {
        "unique_sources": len(source_ids),
        "trusted_sources": trusted_count,
        "claims": len(claim_ids),
        "quote_safe_claims": len(quote_safe_ids),
        "non_quote_claims": len(claim_ids) - len(quote_safe_ids),
    }
    if counts != expected_counts:
        errors.append(f"stored counts {counts!r} do not match computed counts {expected_counts!r}")

    if errors:
        print(f"Heart source closure: FAIL ({len(errors)})", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        "Heart source closure: PASS — "
        f"{len(source_ids)} sources, {trusted_count} trusted, "
        f"{len(claim_ids)} claims, {len(quote_safe_ids)} locator-bound quote-safe claims"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
