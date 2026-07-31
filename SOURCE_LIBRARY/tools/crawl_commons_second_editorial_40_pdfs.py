#!/usr/bin/env python3
"""Build a second balanced 40-PDF open archive from Wikimedia Commons.

This corpus deliberately differs from the first author-centred 40-PDF archive.
It focuses on Russian literary periodicals, Futurism/avant-garde, memoirs,
Reformed/Puritan primary texts, Baptist documents, and manuscript studies.

Discovery uses list=search + imageinfo/extmetadata, structured open-license
checks, topic-level caps, round-robin ordering, semantic-title deduplication,
PDF signature/page validation, and SHA-256. Parallel historical scans of the
same work are allowed only when they are distinct source objects; the manifest
marks them for comparative use rather than pretending they are different works.
"""

from __future__ import annotations

import re
import unicodedata
from collections import defaultdict, deque

import crawl_commons_open_pdfs as collector
import crawl_commons_open_pdfs_search_api as search_api  # noqa: F401 — patches discover_query


TOPICS: tuple[tuple[str, tuple[str, ...], str, str, int], ...] = (
    ("futuristy", ('intitle:"Futuristy" filemime:pdf', 'intitle:"Футуристы" filemime:pdf'), r"futuristy|футурист", r"young asia", 2),
    ("marinetti", ('intitle:"Маринетти" футуризм filemime:pdf', 'intitle:"Marinetti" futurism filemime:pdf'), r"маринетти|marinetti", "", 2),
    ("roaring-parnassus", ('intitle:"Рыкающий Парнас" filemime:pdf', 'intitle:"Rykaiushchii Parnas" filemime:pdf'), r"рыкающ|rykaiush", "", 2),
    ("victory-over-sun", ('intitle:"Победа над солнцем" filemime:pdf', 'intitle:"Pobeda nad solntsem" filemime:pdf'), r"победа над солнцем|pobeda nad solntsem", "", 2),
    ("belinsky-memoirs", ('intitle:"Литературные воспоминания" Белинский filemime:pdf', 'intitle:"воспоминания о Белинском" filemime:pdf'), r"воспоминан.*белинск|белинск.*воспоминан", "", 2),

    ("apollo", ('intitle:"Аполлон" журнал filemime:pdf', 'intitle:"Аполлон." filemime:pdf'), r"аполлон", r"apollo spacecraft|аполлонов", 4),
    ("vesy", ('intitle:"Весы" журнал filemime:pdf',), r"(?:^|\W)весы(?:\W|$)", "", 4),
    ("golden-fleece", ('intitle:"Золотое руно" filemime:pdf',), r"золотое руно", "", 4),
    ("mir-iskusstva", ('intitle:"Мир искусства" filemime:pdf',), r"мир искусства", "", 4),
    ("vestnik-evropy", ('intitle:"Вестник Европы" filemime:pdf',), r"вестник европы", "", 4),
    ("niva", ('intitle:"Нива" журнал filemime:pdf',), r"(?:^|\W)нива(?:\W|$)", "", 4),
    ("otechestvennye-zapiski", ('intitle:"Отечественные записки" filemime:pdf',), r"отечественные записки", "", 4),
    ("russkaya-mysl", ('intitle:"Русская мысль" filemime:pdf',), r"русская мысль", "", 4),
    ("russkii-arkhiv", ('intitle:"Русский архив" filemime:pdf',), r"русский архив", "", 4),
    ("russkoe-bogatstvo", ('intitle:"Русское богатство" filemime:pdf',), r"русское богатство", "", 3),
    ("severnye-tsvety", ('intitle:"Северные цветы" filemime:pdf',), r"северные цветы", "", 3),
    ("sovremennik", ('intitle:"Современник" 1837 filemime:pdf',), r"современник.*1837|1837.*современник", "", 3),
    ("russkii-vestnik", ('intitle:"Русский вестник" filemime:pdf',), r"русский вестник", "", 4),

    ("people-called-baptists", ('intitle:"The people called Baptists" filemime:pdf',), r"people called baptists", "", 2),
    ("baptist-principles", ('intitle:"peculiar principles of the Baptists" filemime:pdf',), r"peculiar principles of the baptists", "", 2),
    ("westminster-confession", ('intitle:"Westminster Confession of Faith" filemime:pdf', 'intitle:"Westminster Confession" filemime:pdf'), r"westminster confession", "", 2),
    ("calvin-institutes", ('intitle:"Institutes of the Christian religion" Calvin filemime:pdf',), r"institutes of the christian religion", "", 3),
    ("john-owen", ('intitle:"The works of John Owen" filemime:pdf',), r"works of john owen", "", 3),
    ("thomas-goodwin", ('intitle:"Works of Thomas Goodwin" filemime:pdf',), r"works of thomas goodwin", "", 2),

    ("sinaiticus-collation", ('intitle:"collation of the Codex Sinaiticus" filemime:pdf', 'intitle:"Codex Sinaiticus" collation filemime:pdf'), r"collation.*codex sinaiticus|codex sinaiticus.*collation", "", 3),
    ("enoch-studies", ('intitle:"Book of Enoch" filemime:pdf', 'intitle:"Psalms of Solomon" Enoch filemime:pdf', 'intitle:"proper names" Enoch filemime:pdf'), r"enoch|псалм.*соломон", r"modern novel|fiction", 4),
)

collector.COLLECTION = "commons-second-editorial-open-pdf-40"
collector.SEARCH_QUERIES = [query for _, queries, _, _, _ in TOPICS for query in queries]


def semantic_key(title: str) -> str:
    value = title.removeprefix("File:")
    value = re.sub(r"\.pdf$", "", value, flags=re.I)
    value = unicodedata.normalize("NFKD", value).lower()
    value = re.sub(r"\b(scan|scanned|copy|version)\b", " ", value)
    value = re.sub(r"[^a-zа-яё0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def balanced_discover(session, per_query):  # type: ignore[no-untyped-def]
    by_topic: dict[str, list[collector.Candidate]] = defaultdict(list)
    failures: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    seen_topic_keys: dict[str, set[str]] = defaultdict(set)

    for topic, queries, include, exclude, cap in TOPICS:
        for query in queries:
            print(f"[topic={topic}] {query}", flush=True)
            try:
                found = collector.discover_query(session, query, per_query)
            except Exception as exc:
                failures.append({"topic": topic, "query": query, "error": f"{type(exc).__name__}: {exc}"})
                continue
            for candidate in found:
                text = candidate.file_title
                if not re.search(include, text, re.I):
                    continue
                if exclude and re.search(exclude, text, re.I):
                    continue
                key = semantic_key(text)
                if candidate.original_url in seen_urls or not key or key in seen_topic_keys[topic]:
                    continue
                seen_urls.add(candidate.original_url)
                seen_topic_keys[topic].add(key)
                by_topic[topic].append(candidate)
                if len(by_topic[topic]) >= cap:
                    break
            if len(by_topic[topic]) >= cap:
                break
        print(f"[topic-result] {topic}={len(by_topic[topic])}", flush=True)

    queues = {topic: deque(items) for topic, items in by_topic.items() if items}
    active = deque(topic for topic, *_ in TOPICS if topic in queues)
    ordered: list[collector.Candidate] = []
    while active:
        topic = active.popleft()
        queue = queues[topic]
        if queue:
            ordered.append(queue.popleft())
        if queue:
            active.append(topic)
    return ordered, failures


collector.discover = balanced_discover

if __name__ == "__main__":
    raise SystemExit(collector.main())
