#!/usr/bin/env python3
"""Use MediaWiki's documented list=search then prop=imageinfo workflow.

The original generator=search request combined file discovery with expensive
extmetadata hydration and returned no usable candidates. This adapter first
retrieves File-namespace titles through list=search, then requests imageinfo in
small batches with an explicit extmetadata filter. The original collector's
license gate, PDF validation, manifests, and downloader remain unchanged.
"""

from __future__ import annotations

from typing import Any

import crawl_commons_open_pdfs as collector

collector.SEARCH_QUERIES = [
    query.replace("filetype:pdf", "filemime:pdf")
    for query in collector.SEARCH_QUERIES
] + [
    "Есенин filemime:pdf",
    "Пушкин filemime:pdf",
    "Лермонтов filemime:pdf",
    "Блок filemime:pdf",
    "Маяковский filemime:pdf",
    "Бунин filemime:pdf",
    "Тютчев filemime:pdf",
    "Фет filemime:pdf",
    "Брюсов filemime:pdf",
    "Бальмонт filemime:pdf",
    "Северянин filemime:pdf",
    "Гумилев filemime:pdf",
    "Ахматова filemime:pdf",
    "Хлебников filemime:pdf",
    "Duncan filemime:pdf",
    "Russian poetry filemime:pdf",
    "Russian literature filemime:pdf",
]

EXT_FIELDS = "|".join(
    [
        "LicenseShortName",
        "UsageTerms",
        "AttributionRequired",
        "Artist",
        "Credit",
        "Source",
        "DateTimeOriginal",
        "DateTime",
    ]
)


def search_titles(session, query: str, limit: int) -> list[dict[str, Any]]:  # type: ignore[no-untyped-def]
    rows: list[dict[str, Any]] = []
    continuation: dict[str, Any] = {}
    while len(rows) < limit:
        params: dict[str, Any] = {
            "action": "query",
            "format": "json",
            "formatversion": 2,
            "list": "search",
            "srsearch": query,
            "srnamespace": 6,
            "srlimit": min(50, limit - len(rows)),
            "srprop": "size|wordcount|timestamp",
            **continuation,
        }
        response = collector.request(session, collector.API, params=params)
        response.raise_for_status()
        payload = response.json()
        rows.extend(payload.get("query", {}).get("search", []))
        if "continue" not in payload:
            break
        continuation = payload["continue"]
    return rows[:limit]


def hydrate_batch(session, titles: list[str], query: str) -> list[collector.Candidate]:  # type: ignore[no-untyped-def]
    params: dict[str, Any] = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "titles": "|".join(titles),
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiextmetadatafilter": EXT_FIELDS,
        "iiextmetadatalanguage": "en",
        "iimetadataversion": "latest",
    }
    response = collector.request(session, collector.API, params=params)
    response.raise_for_status()
    payload = response.json()
    output: list[collector.Candidate] = []
    for page in payload.get("query", {}).get("pages", []):
        infos = page.get("imageinfo") or []
        if not infos:
            continue
        info = infos[0]
        title = str(page.get("title", ""))
        mime = str(info.get("mime", ""))
        if mime != "application/pdf" and not title.lower().endswith(".pdf"):
            continue
        ext = info.get("extmetadata") or {}
        short_name = collector.metadata_value(ext, "LicenseShortName")
        usage_terms = collector.metadata_value(ext, "UsageTerms")
        if not collector.license_allowed(short_name, usage_terms):
            continue
        original_url = str(info.get("url", ""))
        description_url = str(info.get("descriptionurl", ""))
        if not original_url.startswith("https://upload.wikimedia.org/"):
            continue
        output.append(
            collector.Candidate(
                page_id=int(page.get("pageid", 0)),
                file_title=title,
                description_url=description_url,
                original_url=original_url,
                mime=mime,
                advertised_bytes=int(info["size"]) if info.get("size") is not None else None,
                width=int(info["width"]) if info.get("width") is not None else None,
                height=int(info["height"]) if info.get("height") is not None else None,
                license_short_name=short_name,
                usage_terms=usage_terms,
                attribution_required=collector.metadata_value(ext, "AttributionRequired"),
                artist=collector.metadata_value(ext, "Artist"),
                credit=collector.metadata_value(ext, "Credit"),
                source=collector.metadata_value(ext, "Source"),
                date=(
                    collector.metadata_value(ext, "DateTimeOriginal")
                    or collector.metadata_value(ext, "DateTime")
                ),
                query=query,
            )
        )
    return output


def discover_query(session, query: str, limit: int):  # type: ignore[no-untyped-def]
    rows = search_titles(session, query, limit)
    accepted: list[collector.Candidate] = []
    titles = [str(row.get("title", "")) for row in rows if row.get("title")]
    for start in range(0, len(titles), 10):
        accepted.extend(hydrate_batch(session, titles[start : start + 10], query))
    print(
        f"[query-result] searched={len(rows)} open-pdf={len(accepted)} query={query}",
        flush=True,
    )
    return accepted


collector.discover_query = discover_query

if __name__ == "__main__":
    raise SystemExit(collector.main())
