#!/usr/bin/env python3
"""Editorially balanced v3 adapter for the Commons 120+ materials archive.

v2 removed many broad false positives but still allowed series dominance and
non-person objects bearing a poet's name. v3 splits journals, authors,
manuscript families, reformers, audio subjects and literary places into small
independent topics. Round-robin selection therefore enforces diversity before
any topic can contribute a second or third item.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import crawl_commons_project_materials_120plus as collector

Topic = collector.Topic

PORTRAIT_EXCLUDE = (
    r"museum|house|grave|burial|tomb|plaque|monument|statue|bust|estate|street|"
    r"school|library|book|cover|works|autograph|signature|memorial|collection|"
    r"stamp|coin|banknote|quote|with\b|family|group|cemetery|river|reservoir|"
    r"port\b|ship\b|cruise|boat\b|vessel|letter|drawing|at work|poem|noch|ramzes|"
    r"dacha|apartment|room|desk|archive|exhibition|poster|graffiti|mural|"
    r"музей|дом(?:а|ик)?\b|могил|захорон|таблич|памятник|стату|бюст|усадьб|"
    r"улиц|школ|библиотек|книг|облож|собрани|автограф|подпис|мемориал|"
    r"кладбищ|цитат|семь|групп|барельеф|порт\b|теплоход|корабл|судно|речн|"
    r"письм|рисунк|за работ|стих|комнат|квартир|архив|выстав|плакат|граффити"
)

collector.GLOBAL_EXCLUDE = collector.re.compile(
    r"football|soccer|baseball|basketball|hockey|airport|aircraft|album cover|"
    r"modern advertisement|logo\b|coat of arms|currency|coin\b|school yearbook|"
    r"medical|chemistry|botany|zoology|Wesley Duncan|Duncan Hunter|Akhmatov\b|"
    r"A\.\s*L\.\s*Blok|urbi et orbi|Sherlock|Manchester Literary|Young Asia",
    collector.re.IGNORECASE,
)


def periodical(name: str, query_name: str | None = None, cap: int = 3) -> Topic:
    q = query_name or name
    return Topic(
        "pdf",
        f"periodical-{collector.slugify(name, 'text/plain').split('.')[0].lower()}",
        (f'intitle:"{q}" filemime:pdf',),
        collector.re.escape(name),
        cap=cap,
    )


def portrait(name: str, cyr: str, pattern: str, cap: int = 4) -> Topic:
    return Topic(
        "portrait",
        f"portrait-{name.lower().replace(' ', '-')}",
        (
            f'intitle:"{name}" filetype:bitmap',
            f'intitle:"{cyr}" filetype:bitmap',
            f'"{name}" portrait filetype:bitmap',
        ),
        pattern,
        PORTRAIT_EXCLUDE,
        cap,
    )


def manuscript(name: str, cyr: str, pattern: str, cap: int = 2) -> Topic:
    return Topic(
        "ephemera",
        f"manuscript-{name.lower().replace(' ', '-')}",
        (
            f'"{name}" manuscript filetype:bitmap',
            f'"{cyr}" рукопись filetype:bitmap',
            f'"{cyr}" автограф filetype:bitmap',
        ),
        rf"(?=.*(?:{pattern}))(?=.*(?:manuscript|рукопис|autograph|автограф|letter|письм))",
        r"museum|house|monument|grave|plaque|edition cover|facsimile edition",
        cap,
    )


def place(name: str, cyr: str, pattern: str, cap: int = 1) -> Topic:
    return Topic(
        "ephemera",
        f"place-{name.lower().replace(' ', '-')}",
        (
            f'"{name}" house museum filetype:bitmap',
            f'"{cyr}" дом-музей filetype:bitmap',
            f'"{cyr}" музей-усадьба filetype:bitmap',
        ),
        rf"(?=.*(?:{pattern}))(?=.*(?:museum|музей|house|дом|estate|усадьб))",
        r"plaque|таблич|sign|вывеск|souvenir|gift shop|grave|могил|monument|памятник",
        cap,
    )


def audio(name: str, cyr: str, pattern: str, cap: int = 2) -> Topic:
    return Topic(
        "ephemera",
        f"audio-{name.lower().replace(' ', '-')}",
        (
            f'"{name}" poem filetype:audio',
            f'"{cyr}" стихотворение filetype:audio',
            f'"{cyr}" читает filetype:audio',
        ),
        pattern,
        r"contest|конкурс|lesson|урок|children|дет|podcast|interview|lecture|лекци",
        cap,
    )


collector.TOPICS = (
    # ---------------- PDF: separate small, named baskets ----------------
    periodical("Русский архив", cap=3),
    periodical("Мир искусства", cap=3),
    periodical("Золотое руно", cap=2),
    periodical("Аполлон", cap=2),
    periodical("Весы", cap=2),
    periodical("Вестник Европы", cap=2),
    periodical("Русская мысль", cap=2),
    periodical("Русское богатство", cap=2),
    periodical("Нива", cap=2),
    periodical("Северные цветы", cap=2),
    periodical("Современник", cap=2),
    periodical("Отечественные записки", cap=2),
    periodical("Русский вестник", cap=2),
    Topic("pdf", "avant-garde-roaring-parnassus", ('intitle:"Рыкающий Парнас" filemime:pdf', 'intitle:"Rykaiushchii Parnas" filemime:pdf'), r"рыкающ|rykaiush", cap=1),
    Topic("pdf", "avant-garde-futuristy", ('intitle:"Футуристы" filemime:pdf', 'intitle:"Futuristy" filemime:pdf'), r"футурист|futurist", r"young asia", 2),
    Topic("pdf", "avant-garde-victory-sun", ('intitle:"Победа над солнцем" filemime:pdf', 'intitle:"Pobeda nad solntsem" filemime:pdf'), r"победа над солнцем|pob.*solnt", cap=2),
    Topic("pdf", "avant-garde-marinetti", ('intitle:"Маринетти" футуризм filemime:pdf', 'intitle:"Marinetti" futurism filemime:pdf'), r"маринетти|marinetti", cap=2),
    Topic("pdf", "memoirs-belinsky", ('intitle:"воспоминания о Белинском" filemime:pdf',), r"воспоминан.*белинск", cap=2),
    Topic("pdf", "memoirs-pushkin", ('intitle:"Воспоминания о Пушкине" filemime:pdf', 'intitle:"Pushkin memoirs" filemime:pdf'), r"(?:воспоминан.*пушкин|pushkin.*memoir)", cap=2),
    Topic("pdf", "memoirs-tolstoy", ('intitle:"Воспоминания о Толстом" filemime:pdf', 'intitle:"Tolstoy memoirs" filemime:pdf'), r"(?:воспоминан.*толст|tolstoy.*memoir)", cap=2),
    Topic("pdf", "memoirs-blok", ('intitle:"Воспоминания о Блоке" filemime:pdf', 'intitle:"Alexander Blok memoir" filemime:pdf'), r"(?:воспоминан.*блок|blok.*memoir)", cap=2),
    Topic("pdf", "memoirs-mayakovsky", ('intitle:"Воспоминания о Маяковском" filemime:pdf', 'intitle:"Mayakovsky memoir" filemime:pdf'), r"(?:воспоминан.*маяков|mayakov.*memoir)", cap=2),
    Topic("pdf", "john-owen", ('intitle:"Works of John Owen" filemime:pdf',), r"works of john owen", cap=2),
    Topic("pdf", "thomas-goodwin", ('intitle:"Works of Thomas Goodwin" filemime:pdf',), r"works of thomas goodwin", cap=2),
    Topic("pdf", "calvin-institutes", ('intitle:"Institutes of the Christian Religion" Calvin filemime:pdf',), r"institutes of the christian religion", cap=2),
    Topic("pdf", "westminster-confession", ('intitle:"Westminster Confession" filemime:pdf',), r"westminster confession", cap=2),
    Topic("pdf", "baptist-principles", ('intitle:"People called Baptists" filemime:pdf', 'intitle:"Peculiar principles of the Baptists" filemime:pdf'), r"people called baptists|peculiar principles of the baptists", cap=2),
    Topic("pdf", "codex-sinaiticus-study", ('intitle:"Codex Sinaiticus" collation filemime:pdf', 'intitle:"Codex Sinaiticus Petropolitanus" filemime:pdf'), r"codex sinaiticus", cap=3),
    Topic("pdf", "enoch-qumran-study", ('intitle:"Book of Enoch" manuscript filemime:pdf', 'intitle:"Dead Sea Scrolls" Enoch filemime:pdf', 'intitle:"Qumran" Enoch filemime:pdf'), r"enoch|dead sea scroll|qumran", cap=3),

    # ---------------- portraits: exact identity, non-person objects excluded ----------------
    portrait("Sergei Yesenin", "Сергей Есенин", r"serge[yi].*yesenin|sergey.*esenin|сергей.*есенин"),
    portrait("Ivan Bunin", "Иван Бунин", r"ivan.*bunin|иван.*бунин"),
    portrait("Igor Severyanin", "Игорь Северянин", r"igor.*severyanin|игорь.*северянин"),
    portrait("Konstantin Balmont", "Константин Бальмонт", r"konstantin.*balmont|константин.*бальмонт"),
    portrait("Fyodor Tyutchev", "Фёдор Тютчев", r"fyodor.*tyutchev|ф[её]дор.*тютчев"),
    portrait("Apollon Maykov", "Аполлон Майков", r"apollon.*maykov|аполлон.*майков"),
    portrait("Valery Bryusov", "Валерий Брюсов", r"valer.*bryusov|валер.*брюсов"),
    portrait("Alexander Blok", "Александр Блок", r"alexander.*blok|александр.*блок"),
    portrait("Afanasy Fet", "Афанасий Фет", r"afanasy.*fet|афанасий.*фет|afanasy.*shenshin|афанасий.*шеншин"),
    portrait("Vladimir Mayakovsky", "Владимир Маяковский", r"vladimir.*maya?kov|владимир.*маяков"),
    portrait("Anna Akhmatova", "Анна Ахматова", r"anna.*akhmatova|анна.*ахматова"),
    portrait("Nikolay Gumilev", "Николай Гумилёв", r"nikolai?.*gumilev|николай.*гумил"),
    portrait("Boris Pasternak", "Борис Пастернак", r"boris.*pasternak|борис.*пастернак"),
    portrait("Alexander Pushkin", "Александр Пушкин", r"alexander.*pushkin|александр.*пушкин"),
    portrait("Mikhail Lermontov", "Михаил Лермонтов", r"mikhail.*lermontov|михаил.*лермонтов"),
    portrait("Marina Tsvetaeva", "Марина Цветаева", r"marina.*tsvetaeva|марина.*цветаева"),
    portrait("Osip Mandelstam", "Осип Мандельштам", r"osip.*mandelstam|осип.*мандельштам"),
    portrait("Velimir Khlebnikov", "Велимир Хлебников", r"velimir.*khlebnikov|велимир.*хлебников"),
    portrait("Zinaida Gippius", "Зинаида Гиппиус", r"zinaida.*gippius|зинаида.*гиппиус"),

    # ---------------- manuscripts: one/two per named author ----------------
    manuscript("Alexander Pushkin", "Александр Пушкин", r"alexander pushkin|александр пушкин", 2),
    manuscript("Mikhail Lermontov", "Михаил Лермонтов", r"mikhail lermontov|михаил лермонтов", 2),
    manuscript("Sergei Yesenin", "Сергей Есенин", r"serge[yi] yesenin|sergey esenin|сергей есенин", 2),
    manuscript("Vladimir Mayakovsky", "Владимир Маяковский", r"vladimir mayakovsky|владимир маяковский", 2),
    manuscript("Alexander Blok", "Александр Блок", r"alexander blok|александр блок", 2),
    manuscript("Anna Akhmatova", "Анна Ахматова", r"anna akhmatova|анна ахматова", 2),
    manuscript("Marina Tsvetaeva", "Марина Цветаева", r"marina tsvetaeva|марина цветаева", 2),
    manuscript("Boris Pasternak", "Борис Пастернак", r"boris pasternak|борис пастернак", 2),

    # ---------------- historical covers and posters ----------------
    Topic("ephemera", "cover-russian-futurism", ('Russian futurist book cover filetype:bitmap', 'русский футуризм обложка filetype:bitmap'), r"(?=.*(?:futur|футур))(?=.*(?:cover|облож|book|книг))", r"20(?:1|2)\d|exhibition|выстав", 4),
    Topic("ephemera", "cover-kruchenykh", ('Kruchenykh book cover filetype:bitmap', 'Крученых обложка filetype:bitmap'), r"(?=.*(?:kruchenykh|крученых))(?=.*(?:cover|облож|book|книг))", r"20(?:1|2)\d|reconstruction|facsimile edition", 3),
    Topic("ephemera", "cover-khlebnikov", ('Khlebnikov book cover filetype:bitmap', 'Хлебников обложка filetype:bitmap'), r"(?=.*(?:khlebnikov|хлебников))(?=.*(?:cover|облож|book|книг))", r"20(?:1|2)\d|exhibition", 3),
    Topic("ephemera", "cover-mayakovsky", ('Mayakovsky book cover filetype:bitmap', 'Маяковский обложка filetype:bitmap'), r"(?=.*(?:mayakov|маяков))(?=.*(?:cover|облож|book|книг))", r"20(?:1|2)\d|exhibition", 3),
    Topic("ephemera", "cover-silver-age-journals", ('Мир искусства обложка filetype:bitmap', 'Аполлон журнал обложка filetype:bitmap', 'Весы журнал обложка filetype:bitmap', 'Золотое руно обложка filetype:bitmap'), r"(?=.*(?:мир искусства|аполлон|весы|золотое руно))(?=.*(?:облож|cover|журнал))", r"20(?:1|2)\d|exhibition", 4),

    # ---------------- literary places: at most one per author ----------------
    place("Sergei Yesenin", "Сергей Есенин", r"yesenin|esenin|есенин"),
    place("Alexander Blok", "Александр Блок", r"alexander blok|александр блок"),
    place("Vladimir Mayakovsky", "Владимир Маяковский", r"mayakov|маяков"),
    place("Boris Pasternak", "Борис Пастернак", r"pasternak|пастернак"),
    place("Alexander Pushkin", "Александр Пушкин", r"pushkin|пушкин"),
    place("Mikhail Lermontov", "Михаил Лермонтов", r"lermontov|лермонтов"),
    place("Anna Akhmatova", "Анна Ахматова", r"akhmatova|ахматова"),
    place("Marina Tsvetaeva", "Марина Цветаева", r"tsvetaeva|цветаева"),

    # ---------------- manuscript families, small caps ----------------
    Topic("ephemera", "manuscript-codex-sinaiticus", ('Codex Sinaiticus filetype:bitmap',), r"codex sinaiticus", r"book cover|museum display|modern replica", 3),
    Topic("ephemera", "manuscript-dead-sea-scrolls", ('Dead Sea Scrolls manuscript filetype:bitmap', 'Qumran scroll manuscript filetype:bitmap'), r"dead sea scroll|qumran", r"museum display|replica|book cover|tourist", 3),
    Topic("ephemera", "manuscript-bodmer-p72", ('Papyrus Bodmer filetype:bitmap', 'P72 manuscript filetype:bitmap'), r"papyrus bodmer|(?:^|\W)p72(?:\W|$)", r"book cover|museum display|modern replica", 3),
    Topic("ephemera", "manuscript-hebrew-bible", ('Hebrew Bible manuscript filetype:bitmap', 'Masoretic manuscript filetype:bitmap'), r"hebrew bible manuscript|masoretic manuscript", r"book cover|modern replica", 3),

    # ---------------- reformers and Puritans: separate people ----------------
    Topic("ephemera", "portrait-calvin", ('John Calvin portrait filetype:bitmap',), r"john calvin", r"reverse|flipped|mirror|statue|monument|modern|plaque", 2),
    Topic("ephemera", "portrait-john-owen", ('John Owen portrait filetype:bitmap',), r"john owen", r"statue|monument|modern|book cover", 2),
    Topic("ephemera", "portrait-thomas-goodwin", ('Thomas Goodwin portrait filetype:bitmap',), r"thomas goodwin", r"statue|monument|modern|book cover", 2),
    Topic("ephemera", "portrait-martin-luther", ('Martin Luther portrait filetype:bitmap',), r"martin luther", r"statue|monument|modern|plaque", 2),
    Topic("ephemera", "westminster-assembly", ('Westminster Assembly engraving filetype:bitmap',), r"westminster assembly", r"modern|book cover", 2),

    # ---------------- audio: separate poets ----------------
    audio("Alexander Pushkin", "Александр Пушкин", r"pushkin|пушкин", 2),
    audio("Mikhail Lermontov", "Михаил Лермонтов", r"lermontov|лермонтов", 2),
    audio("Sergei Yesenin", "Сергей Есенин", r"yesenin|esenin|есенин", 2),
    audio("Vladimir Mayakovsky", "Владимир Маяковский", r"mayakov|маяков", 2),
    audio("Alexander Blok", "Александр Блок", r"alexander blok|александр блок", 2),
    audio("Anna Akhmatova", "Анна Ахматова", r"akhmatova|ахматова", 2),
    Topic("ephemera", "audio-free-russia-hymn", ('"The hymn of free Russia" filetype:audio', '"Гимн свободной России" filetype:audio'), r"hymn of free russia|гимн свободной россии", cap=1),
)

# Reject byte-identical files across the entire collection, not merely a bucket.
_seen_sha: set[str] = set()
_original_download = collector.download_candidate


def strict_download_candidate(session, candidate, archive_number, output_dir, max_bytes):  # type: ignore[no-untyped-def]
    record = _original_download(session, candidate, archive_number, output_dir, max_bytes)
    if record.status != "DOWNLOADED" or not record.sha256:
        return record
    if record.sha256 in _seen_sha:
        if record.local_file_name:
            (Path(output_dir) / record.local_file_name).unlink(missing_ok=True)
        record.status = "DUPLICATE_SHA256"
        record.archive_number = None
        record.local_file_name = None
        record.notes = "Byte-identical duplicate rejected by editorial v3 gate"
        return record
    _seen_sha.add(record.sha256)
    return record


collector.download_candidate = strict_download_candidate
collector.COLLECTION = "commons-project-materials-editorial-120plus"

if __name__ == "__main__":
    raise SystemExit(collector.main())
