#!/usr/bin/env python3
"""Build a strict 40+ literary PDF corpus from Wikimedia Commons.

This second curation gate removes surname collisions found by the balanced
round-robin pass (for example Wesley Duncan, Duncan Hunter, a male Akhmatov,
an unrelated A. L. Blok and a Bryusov calendar). Candidates must match a full
author identity, a recognised literary work, an anthology, or a named
literary journal. The base collector still enforces open licenses, unchanged
original bytes, PDF signature, page count, size and SHA-256.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass

import crawl_commons_open_pdfs as collector
import crawl_commons_open_pdfs_search_api as search_api

collector.COLLECTION = "commons-russian-literature-strict-open-pdf-40plus"

GLOBAL_EXCLUDE = re.compile(
    r"wesley\s+duncan|duncan\s+d\.?\s+hunter|united\s+states.*duncan|"
    r"duncan\s+dunbar|ахматов(?:\W|$)|blok\s+a\.?\s*l\.?|"
    r"politicheskaya\s+literatura|первобытный\s+брюсов\s+календарь|"
    r"bunin\s+a\s+i\s+gde\s+nahodilisj|федор\s+федорович\s+тютчев",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Topic:
    name: str
    queries: tuple[str, ...]
    include: str
    per_topic_cap: int = 8


TOPICS: tuple[Topic, ...] = (
    Topic(
        "isadora-duncan",
        (
            'intitle:"Isadora Duncan" filemime:pdf',
            'intitle:"Айседора Дункан" filemime:pdf',
            'intitle:"My Life" Isadora filemime:pdf',
            'intitle:"Art of the Dance" Duncan filemime:pdf',
        ),
        r"isadora\s+duncan|айседор[аы]\s+дункан|my\s+life.*duncan|art\s+of\s+the\s+dance",
        5,
    ),
    Topic(
        "esenin",
        (
            'intitle:"Сергей Есенин" filemime:pdf',
            'intitle:"Sergei Yesenin" filemime:pdf',
            'intitle:"Sergey Esenin" filemime:pdf',
            'intitle:"Есенин" стихи filemime:pdf',
        ),
        r"сергей\s+(?:александрович\s+)?есенин|serge[yi]\s+yesenin|sergey\s+esenin|есенин.*стих",
        6,
    ),
    Topic(
        "blok",
        (
            'intitle:"Александр Блок" filemime:pdf',
            'intitle:"Alexander Blok" filemime:pdf',
            'intitle:"Стихи о Прекрасной даме" filemime:pdf',
            'intitle:"Двенадцать" Блок filemime:pdf',
            'intitle:"Дванацять" Блок filemime:pdf',
        ),
        r"александр.*блок|блок.*александр|alexander\s+blok|стихи\s+о\s+прекрасной\s+даме|дванадцять|двенадцать.*блок",
        8,
    ),
    Topic(
        "mayakovsky",
        (
            'intitle:"Владимир Маяковский" filemime:pdf',
            'intitle:"Vladimir Mayakovsky" filemime:pdf',
            'intitle:"Mayakovsky" poetry filemime:pdf',
            'intitle:"Простое как мычание" filemime:pdf',
            'intitle:"Что такое хорошо" Маяковский filemime:pdf',
        ),
        r"владимир.*маяковск|маяковск.*владимир|vladimir\s+maya?kov|mayakovsky|простое\s+как\s+мычание|что\s+такое\s+хорошо",
        8,
    ),
    Topic(
        "pushkin",
        (
            'intitle:"Александр Пушкин" filemime:pdf',
            'intitle:"Alexander Pushkin" filemime:pdf',
            'intitle:"Сочинения Пушкина" filemime:pdf',
            'intitle:"Пушкин" filemime:pdf',
        ),
        r"александр.*пушкин|пушкин.*александр|alexander\s+pushkin|сочинения.*пушкин|пушкин.*(?:биограф|истори|стих|сочин|материал)",
        10,
    ),
    Topic(
        "lermontov",
        (
            'intitle:"Михаил Лермонтов" filemime:pdf',
            'intitle:"Mikhail Lermontov" filemime:pdf',
            'intitle:"Сочинения Лермонтова" filemime:pdf',
            'intitle:"Лермонтов" filemime:pdf',
        ),
        r"михаил.*лермонтов|лермонтов.*михаил|mikhail\s+lermontov|сочинения.*лермонтов|лермонтов.*(?:личност|произвед|биограф|стих|сочин)",
        10,
    ),
    Topic(
        "bunin",
        (
            'intitle:"Иван Бунин" filemime:pdf',
            'intitle:"Ivan Bunin" filemime:pdf',
            'intitle:"The Village" "Ivan Bunin" filemime:pdf',
        ),
        r"иван.*бунин|бунин.*иван|ivan\s+bunin|the\s+village.*ivan\s+bunin",
        6,
    ),
    Topic(
        "tyutchev",
        (
            'intitle:"Федор Иванович Тютчев" filemime:pdf',
            'intitle:"Фёдор Иванович Тютчев" filemime:pdf',
            'intitle:"Fyodor Tyutchev" filemime:pdf',
            'intitle:"Tyutchev" poems filemime:pdf',
        ),
        r"ф[её]дор\s+иванович\s+тютчев|fyodor\s+tyutchev|tyutchev.*poem",
        6,
    ),
    Topic(
        "fet",
        (
            'intitle:"Афанасий Фет" filemime:pdf',
            'intitle:"Afanasy Fet" filemime:pdf',
            'intitle:"Шеншин" Фет filemime:pdf',
        ),
        r"афанасий.*фет|afanasy\s+fet|шеншин.*фет|фет.*шеншин",
        5,
    ),
    Topic(
        "gumilev",
        (
            'intitle:"Николай Гумилев" filemime:pdf',
            'intitle:"Николай Гумилёв" filemime:pdf',
            'intitle:"Nikolay Gumilev" filemime:pdf',
            'intitle:"Колчан" Гумилев filemime:pdf',
            'intitle:"Жемчуга" Гумилев filemime:pdf',
        ),
        r"николай.*гумил|гумил.*николай|nikolay\s+gumilev|колчан|жемчуга",
        7,
    ),
    Topic(
        "akhmatova",
        (
            'intitle:"Анна Ахматова" filemime:pdf',
            'intitle:"Anna Akhmatova" filemime:pdf',
            'intitle:"Ахматова" Вечер filemime:pdf',
            'intitle:"Akhmatova Vecher" filemime:pdf',
        ),
        r"анна.*ахматова|ахматова.*анна|anna\s+akhmatova|akhmatova.*vecher|ахматова.*вечер",
        6,
    ),
    Topic(
        "khlebnikov",
        (
            'intitle:"Велимир Хлебников" filemime:pdf',
            'intitle:"Velimir Khlebnikov" filemime:pdf',
            'intitle:"Хлебников" filemime:pdf',
        ),
        r"велимир.*хлебников|хлебников.*велимир|velimir\s+khlebnikov|khlebnikov.*velimir",
        6,
    ),
    Topic(
        "bryusov",
        (
            'intitle:"Валерий Брюсов" filemime:pdf',
            'intitle:"Valery Bryusov" filemime:pdf',
            'intitle:"Urbi et orbi" filemime:pdf',
            'intitle:"Стефанос" Брюсов filemime:pdf',
        ),
        r"валерий.*брюсов|брюсов.*валерий|valery\s+bryusov|urbi\s+et\s+orbi|стефанос",
        7,
    ),
    Topic(
        "balmont",
        (
            'intitle:"Константин Бальмонт" filemime:pdf',
            'intitle:"Konstantin Balmont" filemime:pdf',
            'intitle:"Под северным небом" filemime:pdf',
            'intitle:"Жар-Птица" Бальмонт filemime:pdf',
        ),
        r"константин.*бальмонт|бальмонт.*константин|konstantin\s+balmont|под\s+северным\s+небом|жар.?птица.*бальмонт|бальмонт.*жар.?птица",
        7,
    ),
    Topic(
        "severyanin",
        (
            'intitle:"Игорь Северянин" filemime:pdf',
            'intitle:"Igor Severyanin" filemime:pdf',
            'intitle:"Ананасы в шампанском" filemime:pdf',
        ),
        r"игорь.*северянин|северянин.*игорь|igor\s+severyanin|ананасы\s+в\s+шампанском",
        6,
    ),
    Topic(
        "poetry-anthologies",
        (
            'intitle:"Modern Russian poetry" filemime:pdf',
            'intitle:"Russian poetry" anthology filemime:pdf',
            'intitle:"Новая русская поэзия" filemime:pdf',
            'intitle:"Русская поэзия" антология filemime:pdf',
        ),
        r"modern\s+russian\s+poetry|russian\s+poetry.*antholog|новая\s+русская\s+поэзия|русская\s+поэзия.*антолог",
        7,
    ),
    Topic(
        "literary-journals",
        (
            'intitle:"Современник 1837" filemime:pdf',
            'intitle:"Аполлон" журнал filemime:pdf',
            'intitle:"Весы" журнал filemime:pdf',
            'intitle:"Золотое руно" журнал filemime:pdf',
            'intitle:"Русский архив" filemime:pdf',
        ),
        r"современник\s+1837|аполлон.*журнал|журнал.*аполлон|весы.*журнал|журнал.*весы|золотое\s+руно|русский\s+архив",
        12,
    ),
)


def accepted_for_topic(title: str, topic: Topic) -> bool:
    value = title.removeprefix("File:")
    if GLOBAL_EXCLUDE.search(value):
        return False
    return re.search(topic.include, value, flags=re.IGNORECASE) is not None


def strict_discover(session, per_query: int):  # type: ignore[no-untyped-def]
    buckets: dict[str, list[collector.Candidate]] = defaultdict(list)
    failures: list[dict[str, str]] = []

    for topic in TOPICS:
        seen: set[str] = set()
        for query in topic.queries:
            print(f"[strict-query] topic={topic.name} query={query}", flush=True)
            try:
                candidates = search_api.discover_query(session, query, per_query)
            except Exception as exc:
                failures.append(
                    {"topic": topic.name, "query": query, "error": f"{type(exc).__name__}: {exc}"}
                )
                continue
            for candidate in candidates:
                if candidate.original_url in seen or not accepted_for_topic(candidate.file_title, topic):
                    continue
                seen.add(candidate.original_url)
                candidate.query = f"strict-topic:{topic.name}; {query}"
                buckets[topic.name].append(candidate)
                if len(buckets[topic.name]) >= topic.per_topic_cap:
                    break
            if len(buckets[topic.name]) >= topic.per_topic_cap:
                break
        print(f"[strict-topic-result] {topic.name}={len(buckets[topic.name])}", flush=True)

    ordered: list[collector.Candidate] = []
    global_seen: set[str] = set()
    max_depth = max((len(buckets[topic.name]) for topic in TOPICS), default=0)
    for depth in range(max_depth):
        for topic in TOPICS:
            if depth >= len(buckets[topic.name]):
                continue
            candidate = buckets[topic.name][depth]
            if candidate.original_url in global_seen:
                continue
            global_seen.add(candidate.original_url)
            ordered.append(candidate)

    print(
        "[strict-total] "
        + ", ".join(f"{topic.name}={len(buckets[topic.name])}" for topic in TOPICS)
        + f"; unique={len(ordered)}",
        flush=True,
    )
    return ordered, failures


collector.discover = strict_discover

if __name__ == "__main__":
    raise SystemExit(collector.main())
