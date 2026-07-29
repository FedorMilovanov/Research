#!/usr/bin/env python3
"""Correct Commons CirrusSearch PDF filtering to use filemime:pdf.

MediaWiki documents `filetype` as a broad media class (TEXT, OFFICE, VIDEO,
etc.). PDF files must be selected with `filemime:pdf`. This wrapper preserves
the collector's rights and verification logic while correcting and broadening
its discovery queries.
"""

from __future__ import annotations

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

if __name__ == "__main__":
    raise SystemExit(collector.main())
