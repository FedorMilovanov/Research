#!/usr/bin/env python3
"""Final strict literary curation: semantic-title dedupe and false-hit removal."""

from __future__ import annotations

import re
import unicodedata

import crawl_commons_open_pdfs as collector
import crawl_commons_strict_literary_pdfs as strict

FALSE_POSITIVE = re.compile(
    r"ex\s+decreto\s+urbi\s+et\s+orbi|basilicarum\s+sanctorum|"
    r"dedicatione\s+basilicarum|apostolurum\s+petri\s+et\s+pauli",
    re.IGNORECASE,
)


def title_fingerprint(title: str) -> str:
    value = unicodedata.normalize("NFKC", title.removeprefix("File:")).lower()
    value = re.sub(r"\(ia\s+[^)]*\)", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\.(?:pdf)$", "", value, flags=re.IGNORECASE)
    value = re.sub(r"[^0-9a-zа-яё]+", " ", value, flags=re.IGNORECASE)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def final_discover(session, per_query: int):  # type: ignore[no-untyped-def]
    candidates, failures = strict.strict_discover(session, per_query)
    accepted: list[collector.Candidate] = []
    seen_titles: set[str] = set()
    for candidate in candidates:
        title = candidate.file_title.removeprefix("File:")
        if FALSE_POSITIVE.search(title):
            print(f"[strict-final-exclude] false-positive title={title}", flush=True)
            continue
        fingerprint = title_fingerprint(title)
        if fingerprint in seen_titles:
            print(f"[strict-final-exclude] semantic-duplicate title={title}", flush=True)
            continue
        seen_titles.add(fingerprint)
        accepted.append(candidate)
    print(
        f"[strict-final-total] before={len(candidates)} after={len(accepted)}",
        flush=True,
    )
    return accepted, failures


collector.discover = final_discover

if __name__ == "__main__":
    raise SystemExit(collector.main())
