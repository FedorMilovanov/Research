#!/usr/bin/env python3
"""Validate the heart-series primary-source closure registry."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "СЕРИЯ СЕРДЦЕ" / "74_SOURCE_CLOSURE_REGISTRY_2026-08-01.json"

ALLOWED_STATUSES = {
    "PRIMARY_VERIFIED",
    "PRIMARY_AUDIO_VERIFIED",
    "OFFICIAL_REPLACEMENT",
    "PARAPHRASE_ONLY",
    "REMOVE",
    "RECEPTION_ONLY",
}
QUOTE_SAFE_STATUSES = {
    "PRIMARY_VERIFIED",
    "PRIMARY_AUDIO_VERIFIED",
    "OFFICIAL_REPLACEMENT",
}
REQUIRED_CLAIMS = {
    "CLM-WHITEFIELD-ANECDOTE",
    "CLM-WHITEFIELD-STONY",
    "CLM-SPURGEON-FREE-WILL",
    "CLM-SPURGEON-LION-LAMB",
    "CLM-BAUCHAM-SISSIFIED",
    "CLM-OWEN-BURN-BIBLES",
    "CLM-HUGHES-EXPULSIVE",
    "CLM-AUGUSTINE-SPLENDIDA",
    "CLM-WATSON-MORALITY",
    "CLM-MCHEYNE-TEN-LOOKS",
    "CLM-KOTZKER-HEART",
    "CLM-WATSON-PANDECT",
    "CLM-HAMILTON-MONOGRAPH",
    "CLM-FERGUSON-BOOK",
    "CLM-ORTLUND-CH15",
    "CLM-ROGERS-ADVICE",
    "CLM-MLJ-BOOK",
    "CLM-PDF-LONG-QUOTES",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def main() -> int:
    errors: list[str] = []

    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing registry: {REGISTRY}")
        return 1
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")
        return 1

    sources = data.get("sources")
    claims = data.get("claims")
    trusted_classes = set(data.get("trusted_source_classes", []))
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

    for index, source in enumerate(sources):
        prefix = f"sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{prefix} must be an object")
            continue

        source_id = source.get("id")
        url = source.get("url")
        source_class = source.get("class")

        for field in ("id", "author", "work", "url", "class", "format", "use"):
            value = source.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")

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
                errors.append(f"{prefix}.url must be an absolute https URL: {url}")

        if source_class in trusted_classes:
            trusted_count += 1

    if len(source_ids) < minimum:
        errors.append(f"only {len(source_ids)} unique sources; required >= {minimum}")
    if trusted_count < 50:
        errors.append(f"only {trusted_count} trusted sources; required >= 50")

    claim_ids: set[str] = set()
    for index, claim in enumerate(claims):
        prefix = f"claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix} must be an object")
            continue

        claim_id = claim.get("id")
        status = claim.get("status")
        quote_safe = claim.get("quote_safe")
        support = claim.get("support")

        for field in ("id", "label", "status", "decision"):
            value = claim.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")

        if isinstance(claim_id, str):
            if claim_id in claim_ids:
                errors.append(f"duplicate claim id: {claim_id}")
            claim_ids.add(claim_id)

        if status not in ALLOWED_STATUSES:
            errors.append(f"{prefix}.status is not allowed: {status!r}")
        if not isinstance(quote_safe, bool):
            errors.append(f"{prefix}.quote_safe must be boolean")
        if not isinstance(support, list) or not all(isinstance(x, str) for x in support):
            errors.append(f"{prefix}.support must be a list of source IDs")
            support = []

        missing_support = [source_id for source_id in support if source_id not in source_by_id]
        if missing_support:
            errors.append(f"{prefix} references missing sources: {missing_support}")

        if quote_safe:
            if status not in QUOTE_SAFE_STATUSES:
                errors.append(f"{prefix} is quote-safe with non-quote-safe status {status}")
            if not support:
                errors.append(f"{prefix} is quote-safe but has no support")
            low_trust = [
                source_id
                for source_id in support
                if source_by_id.get(source_id, {}).get("class") not in trusted_classes
            ]
            if low_trust:
                errors.append(f"{prefix} uses non-trusted support for quote-safe claim: {low_trust}")
        elif status in QUOTE_SAFE_STATUSES:
            errors.append(f"{prefix} has quote-safe status {status} but quote_safe=false")

    missing_claims = sorted(REQUIRED_CLAIMS - claim_ids)
    if missing_claims:
        errors.append(f"required disputed claims missing: {missing_claims}")

    counts = data.get("counts", {})
    expected_counts = {
        "unique_sources": len(source_ids),
        "trusted_sources": trusted_count,
        "claims": len(claim_ids),
        "quote_safe_claims": sum(bool(c.get("quote_safe")) for c in claims if isinstance(c, dict)),
        "non_quote_claims": sum(not bool(c.get("quote_safe")) for c in claims if isinstance(c, dict)),
    }
    if counts != expected_counts:
        errors.append(f"stored counts {counts!r} do not match computed counts {expected_counts!r}")

    if errors:
        for error in errors:
            fail(error)
        return 1

    print(
        "heart source closure OK: "
        f"{len(source_ids)} unique sources, "
        f"{trusted_count} trusted, "
        f"{len(claim_ids)} disputed claims classified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
