#!/usr/bin/env python3
"""Curate a balanced 40+ Commons PDF corpus by title relevance and topic.

The broad discovery pass proved the binary pipeline but admitted incidental
search hits. This adapter uses title-focused searches, explicit relevance
patterns, and round-robin selection across poets/topics before the unchanged
rights, PDF-signature, page-count, size and SHA-256 verification runs.
"""

from __future__ import annotations

import re
from collections import defaultdict

import crawl_commons_open_pdfs as collector
import crawl_commons_open_pdfs_search_api as search_api

TOPICS: list[tuple[str, list[str], str]] = [
    ("esenin", ["intitle:Есенин filemime:pdf", "intitle:Yesenin filemime:pdf", "intitle:Esenin filemime:pdf"], r"есенин|yesenin|esenin"),
    ("duncan", ["intitle:Duncan filemime:pdf", "intitle:Дункан filemime:pdf", 'intitle:"My Life" Duncan filemime:pdf'], r"duncan|дункан|my life"),
    ("blok", ["intitle:Блок filemime:pdf", "intitle:Blok filemime:pdf", "intitle:Block Russian poet filemime:pdf"], r"(^|\W)блок(\W|$)|blok|alexander block"),
    ("mayakovsky", ["intitle:Маяковский filemime:pdf", "intitle:Mayakovsky filemime:pdf", "intitle:Maiakovski filemime:pdf"], r"маяковск|mayakov|maiakov"),
    ("pushkin", ["intitle:Пушкин filemime:pdf", "intitle:Pushkin filemime:pdf", "intitle:Puŝkin filemime:pdf"], r"пушкин|pushkin|puŝkin"),
    ("lermontov", ["intitle:Лермонтов filemime:pdf", "intitle:Lermontov filemime:pdf", "intitle:Lérmontov filemime:pdf"], r"лермонтов|lermontov|lérmontov"),
    ("bunin", ["intitle:Бунин filemime:pdf", "intitle:Bunin filemime:pdf"], r"бунин|bunin"),
    ("tyutchev", ["intitle:Тютчев filemime:pdf", "intitle:Tyutchev filemime:pdf", "intitle:Tiutchev filemime:pdf"], r"тютчев|tyutchev|tiutchev"),
    ("fet", ["intitle:Фет filemime:pdf", 'intitle:"Afanasy Fet" filemime:pdf', "intitle:Foeth filemime:pdf"], r"(^|\W)фет(\W|$)|afanasy fet|foeth"),
    ("gumilev", ["intitle:Гумилев filemime:pdf", "intitle:Гумилёв filemime:pdf", "intitle:Gumilev filemime:pdf"], r"гумил|gumilev|goumilev"),
    ("akhmatova", ["intitle:Ахматова filemime:pdf", "intitle:Akhmatova filemime:pdf"], r"ахматов|akhmatov"),
    ("khlebnikov", ["intitle:Хлебников filemime:pdf", "intitle:Khlebnikov filemime:pdf", "intitle:Chlebnikov filemime:pdf"], r"хлебников|khlebnikov|chlebnikov"),
    ("bryusov", ["intitle:Брюсов filemime:pdf", "intitle:Bryusov filemime:pdf", "intitle:Briusov filemime:pdf"], r"брюсов|bryusov|briusov"),
    ("balmont", ["intitle:Бальмонт filemime:pdf", "intitle:Balmont filemime:pdf"], r"бальмонт|balmont"),
    ("severyanin", ["intitle:Северянин filemime:pdf", "intitle:Severyanin filemime:pdf", "intitle:Severianin filemime:pdf"], r"северянин|severyanin|severianin"),
    ("russian-poetry", ['intitle:"Russian poetry" filemime:pdf', 'intitle:"русская поэзия" filemime:pdf', 'intitle:"Modern Russian poetry" filemime:pdf'], r"russian poetry|русск.{0,8}поэз|modern russian poetry"),
    ("silver-age", ['intitle:"Silver Age" Russian filemime:pdf', 'intitle:"Серебряный век" filemime:pdf'], r"silver age|серебр.{0,8}век"),
    ("sovremennik-pushkin", ['intitle:"Современник 1837" filemime:pdf'], r"современник\s+1837"),
]


def title_relevant(title: str, pattern: str) -> bool:
    normalized = title.removeprefix("File:")
    return re.search(pattern, normalized, flags=re.IGNORECASE) is not None


def curated_discover(session, per_query: int):  # type: ignore[no-untyped-def]
    topic_candidates: dict[str, list[collector.Candidate]] = defaultdict(list)
    failures: list[dict[str, str]] = []

    for topic, queries, pattern in TOPICS:
        seen_topic: set[str] = set()
        for query in queries:
            print(f"[curated-query] topic={topic} query={query}", flush=True)
            try:
                found = search_api.discover_query(session, query, per_query)
            except Exception as exc:
                failures.append(
                    {"query": query, "topic": topic, "error": f"{type(exc).__name__}: {exc}"}
                )
                continue
            for candidate in found:
                if candidate.original_url in seen_topic:
                    continue
                if not title_relevant(candidate.file_title, pattern):
                    continue
                seen_topic.add(candidate.original_url)
                candidate.query = f"topic:{topic}; {query}"
                topic_candidates[topic].append(candidate)
        print(
            f"[curated-topic-result] topic={topic} accepted={len(topic_candidates[topic])}",
            flush=True,
        )

    # Round-robin prevents one prolific author from filling the entire archive.
    ordered: list[collector.Candidate] = []
    seen_global: set[str] = set()
    active_topics = [topic for topic, _, _ in TOPICS]
    index = 0
    while active_topics:
        next_topics: list[str] = []
        for topic in active_topics:
            candidates = topic_candidates[topic]
            if index < len(candidates):
                candidate = candidates[index]
                if candidate.original_url not in seen_global:
                    seen_global.add(candidate.original_url)
                    ordered.append(candidate)
            if index + 1 < len(candidates):
                next_topics.append(topic)
        active_topics = next_topics
        index += 1

    print(
        "[curated-total] "
        + ", ".join(f"{topic}={len(topic_candidates[topic])}" for topic, _, _ in TOPICS)
        + f"; unique={len(ordered)}",
        flush=True,
    )
    return ordered, failures


collector.discover = curated_discover

if __name__ == "__main__":
    raise SystemExit(collector.main())
