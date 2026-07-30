#!/usr/bin/env python3
"""Strict editorial adapter for the Commons 120+ project-materials pass.

The first broad pass proved the binary and rights pipeline but admitted topical
false positives: generic memoirs, museums/graves in the portrait bucket, and
repetitive ephemera. This adapter keeps the same validation and provenance
machinery while enforcing full identities, object-type terms, explicit
exclusions, lower per-topic caps, and byte-identical SHA-256 deduplication.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import crawl_commons_project_materials_120plus as collector

Topic = collector.Topic

PORTRAIT_EXCLUDE = (
    r"museum|house|grave|burial|tomb|plaque|monument|statue|bust|estate|street|"
    r"school|library|book|cover|works|autograph|signature|memorial|collection|"
    r"stamp|coin|banknote|quote|with family|family|group|cemetery|"
    r"музей|дом(?:а|ик)?\b|могил|захорон|таблич|памятник|стату|бюст|усадьб|"
    r"улиц|школ|библиотек|книг|облож|собрани|автограф|подпис|мемориал|"
    r"кладбищ|цитат|семь|групп|барельеф"
)

collector.GLOBAL_EXCLUDE = collector.re.compile(
    r"football|soccer|baseball|basketball|hockey|airport|aircraft|album cover|"
    r"modern advertisement|logo\b|coat of arms|currency|coin\b|school yearbook|"
    r"medical|chemistry|botany|zoology|Wesley Duncan|Duncan Hunter|Akhmatov\b|"
    r"A\.\s*L\.\s*Blok|urbi et orbi",
    collector.re.IGNORECASE,
)

collector.TOPICS = (
    # -------------------- strict additional PDFs --------------------
    Topic(
        "pdf",
        "russian-periodicals",
        (
            'intitle:"Русский архив" filemime:pdf',
            'intitle:"Исторический вестник" filemime:pdf',
            'intitle:"Вестник Европы" filemime:pdf',
            'intitle:"Русская мысль" filemime:pdf',
            'intitle:"Русское богатство" filemime:pdf',
            'intitle:"Нива" журнал filemime:pdf',
        ),
        r"русский архив|исторический вестник|вестник европы|русская мысль|русское богатство|(?:^|\W)нива(?:\W|$)",
        cap=10,
    ),
    Topic(
        "pdf",
        "silver-age-periodicals",
        (
            'intitle:"Мир искусства" filemime:pdf',
            'intitle:"Золотое руно" filemime:pdf',
            'intitle:"Аполлон" журнал filemime:pdf',
            'intitle:"Весы" журнал filemime:pdf',
            'intitle:"Перевал" журнал filemime:pdf',
            'intitle:"Северные цветы" filemime:pdf',
        ),
        r"мир искусства|золотое руно|аполлон|(?:^|\W)весы(?:\W|$)|перевал|северные цветы",
        cap=10,
    ),
    Topic(
        "pdf",
        "russian-avant-garde",
        (
            'Russian futurism filemime:pdf',
            'Русский футуризм filemime:pdf',
            'Russian avant-garde literature filemime:pdf',
            'Имажинизм filemime:pdf',
            'Marinetti Futurism Russian filemime:pdf',
            'Kruchenykh filemime:pdf',
            'Khlebnikov futurism filemime:pdf',
        ),
        r"futuris|футур|avant.?garde|авангард|имажиниз|imagis|marinetti|крученых|kruchenykh|khlebnikov|хлебников",
        r"young asia",
        cap=8,
    ),
    Topic(
        "pdf",
        "russian-literary-memoirs",
        (
            'Russian literary memoirs filemime:pdf',
            'intitle:"Литературные воспоминания" filemime:pdf',
            'intitle:"Воспоминания" Пушкин filemime:pdf',
            'intitle:"Воспоминания" Толстой filemime:pdf',
            'intitle:"Воспоминания" Блок filemime:pdf',
            'intitle:"Воспоминания" Маяковский filemime:pdf',
            'intitle:"Письма русских писателей" filemime:pdf',
        ),
        r"(?=.*(?:russian|русск|pushkin|пушкин|tolst|толст|blok|блок|mayakov|маяков|literary|литератур))(?=.*(?:memoir|воспомин|letter|письм|переписк))",
        r"sherlock|scherlock|manchester|philosophical society|living authors of great britain|literary veteran",
        cap=6,
    ),
    Topic(
        "pdf",
        "puritan-reformed",
        (
            'intitle:"Works of John Owen" filemime:pdf',
            'intitle:"Works of Thomas Goodwin" filemime:pdf',
            'intitle:"Institutes of the Christian Religion" Calvin filemime:pdf',
            'intitle:"Westminster Confession" filemime:pdf',
            'intitle:"Puritan" theology filemime:pdf',
            'Reformed theology history filemime:pdf',
        ),
        r"john owen|thomas goodwin|institutes of the christian religion|westminster confession|puritan|reformed theolog",
        cap=8,
    ),
    Topic(
        "pdf",
        "baptist-protestant-history",
        (
            'Russian Baptists history filemime:pdf',
            'русские баптисты история filemime:pdf',
            'Protestantism Russia history filemime:pdf',
            'intitle:"History of the Baptists" filemime:pdf',
            'intitle:"Short history of the Baptists" filemime:pdf',
            'intitle:"People called Baptists" filemime:pdf',
        ),
        r"baptist|баптист|protestant|протестант|евангельск",
        r"texas|carolina|virginia|kentucky|tennessee|georgia|alabama|mississippi",
        cap=6,
    ),
    Topic(
        "pdf",
        "biblical-manuscripts",
        (
            'Codex Sinaiticus collation filemime:pdf',
            'Codex Sinaiticus Petropolitanus filemime:pdf',
            'Book of Enoch manuscripts filemime:pdf',
            'Dead Sea Scrolls manuscripts filemime:pdf',
            'Qumran manuscripts study filemime:pdf',
            'First Peter manuscript commentary filemime:pdf',
            'Papyrus Bodmer filemime:pdf',
        ),
        r"sinaitic|enoch|dead sea scroll|qumran|first peter|1 peter|papyrus bodmer|рукопис",
        cap=8,
    ),

    # -------------------- strict portrait references --------------------
    Topic("portrait", "esenin", ('intitle:"Sergei Yesenin" filetype:bitmap', 'intitle:"Сергей Есенин" filetype:bitmap', 'intitle:"Sergey Esenin" portrait filetype:bitmap'), r"serge[yi].*yesenin|sergey.*esenin|сергей.*есенин", PORTRAIT_EXCLUDE, 5),
    Topic("portrait", "bunin", ('intitle:"Ivan Bunin" filetype:bitmap', 'intitle:"Иван Бунин" filetype:bitmap'), r"ivan.*bunin|иван.*бунин", PORTRAIT_EXCLUDE, 5),
    Topic("portrait", "severyanin", ('intitle:"Igor Severyanin" filetype:bitmap', 'intitle:"Игорь Северянин" filetype:bitmap'), r"igor.*severyanin|игорь.*северянин", PORTRAIT_EXCLUDE, 5),
    Topic("portrait", "balmont", ('intitle:"Konstantin Balmont" filetype:bitmap', 'intitle:"Константин Бальмонт" filetype:bitmap'), r"konstantin.*balmont|константин.*бальмонт", PORTRAIT_EXCLUDE, 5),
    Topic("portrait", "tyutchev", ('intitle:"Fyodor Tyutchev" filetype:bitmap', 'intitle:"Фёдор Тютчев" filetype:bitmap'), r"fyodor.*tyutchev|ф[её]дор.*тютчев", PORTRAIT_EXCLUDE, 5),
    Topic("portrait", "maykov", ('intitle:"Apollon Maykov" filetype:bitmap', 'intitle:"Аполлон Майков" filetype:bitmap'), r"apollon.*maykov|аполлон.*майков", PORTRAIT_EXCLUDE, 5),
    Topic("portrait", "bryusov", ('intitle:"Valery Bryusov" filetype:bitmap', 'intitle:"Валерий Брюсов" filetype:bitmap'), r"valer.*bryusov|валер.*брюсов", PORTRAIT_EXCLUDE, 5),
    Topic("portrait", "blok", ('intitle:"Alexander Blok" filetype:bitmap', 'intitle:"Александр Блок" filetype:bitmap'), r"alexander.*blok|александр.*блок", PORTRAIT_EXCLUDE, 5),
    Topic("portrait", "fet", ('intitle:"Afanasy Fet" filetype:bitmap', 'intitle:"Афанасий Фет" filetype:bitmap', 'intitle:"Afanasy Shenshin" filetype:bitmap'), r"afanasy.*fet|афанасий.*фет|afanasy.*shenshin|афанасий.*шеншин", PORTRAIT_EXCLUDE, 5),
    Topic("portrait", "mayakovsky", ('intitle:"Vladimir Mayakovsky" filetype:bitmap', 'intitle:"Владимир Маяковский" filetype:bitmap'), r"vladimir.*maya?kov|владимир.*маяков", PORTRAIT_EXCLUDE, 5),
    Topic("portrait", "akhmatova", ('intitle:"Anna Akhmatova" filetype:bitmap', 'intitle:"Анна Ахматова" filetype:bitmap'), r"anna.*akhmatova|анна.*ахматова", PORTRAIT_EXCLUDE, 5),
    Topic("portrait", "gumilev", ('intitle:"Nikolay Gumilev" filetype:bitmap', 'intitle:"Николай Гумилёв" filetype:bitmap', 'intitle:"Nikolai Gumilev" filetype:bitmap'), r"nikolai?.*gumilev|николай.*гумил", PORTRAIT_EXCLUDE, 5),
    Topic("portrait", "pasternak", ('intitle:"Boris Pasternak" filetype:bitmap', 'intitle:"Борис Пастернак" filetype:bitmap'), r"boris.*pasternak|борис.*пастернак", PORTRAIT_EXCLUDE, 5),
    Topic("portrait", "pushkin", ('intitle:"Alexander Pushkin" portrait filetype:bitmap', 'intitle:"Александр Пушкин" портрет filetype:bitmap'), r"alexander.*pushkin|александр.*пушкин", PORTRAIT_EXCLUDE, 5),
    Topic("portrait", "lermontov", ('intitle:"Mikhail Lermontov" portrait filetype:bitmap', 'intitle:"Михаил Лермонтов" портрет filetype:bitmap'), r"mikhail.*lermontov|михаил.*лермонтов", PORTRAIT_EXCLUDE, 5),

    # -------------------- strict ephemera and mixed media --------------------
    Topic(
        "ephemera",
        "poet-manuscripts-letters",
        (
            'Pushkin manuscript filetype:bitmap', 'Пушкин рукопись filetype:bitmap',
            'Lermontov manuscript filetype:bitmap', 'Лермонтов рукопись filetype:bitmap',
            'Mayakovsky manuscript filetype:bitmap', 'Маяковский автограф filetype:bitmap',
            'Yesenin manuscript filetype:bitmap', 'Есенин автограф filetype:bitmap',
            'Alexander Blok manuscript filetype:bitmap', 'Блок рукопись filetype:bitmap',
            'Akhmatova manuscript filetype:bitmap', 'Ахматова автограф filetype:bitmap',
        ),
        r"(?=.*(?:pushkin|пушкин|lermontov|лермонтов|mayakov|маяков|yesenin|esenin|есенин|alexander blok|александр блок|akhmatova|ахматова))(?=.*(?:manuscript|рукопис|autograph|автограф|letter|письм))",
        r"museum|monument|grave|plaque|facsimile edition",
        12,
    ),
    Topic(
        "ephemera",
        "historic-poetry-covers-posters",
        (
            'Russian futurist book cover filetype:bitmap',
            'Kruchenykh book cover filetype:bitmap',
            'Khlebnikov book cover filetype:bitmap',
            'Mayakovsky book cover filetype:bitmap',
            'Russian poetry poster before 1930 filetype:bitmap',
            'русский футуризм обложка filetype:bitmap',
            'поэтический сборник обложка до 1930 filetype:bitmap',
        ),
        r"(?=.*(?:futur|футур|kruchenykh|крученых|khlebnikov|хлебников|mayakov|маяков|poetry|поэтич|стих))(?=.*(?:cover|облож|poster|плакат|афиш|book|книг))",
        r"exhibition 20\d\d|выставк.*20\d\d|museum of russian art 20\d\d",
        10,
    ),
    Topic(
        "ephemera",
        "literary-places",
        (
            'Sergei Yesenin museum filetype:bitmap',
            'Alexander Blok house museum filetype:bitmap',
            'Vladimir Mayakovsky museum filetype:bitmap',
            'Boris Pasternak house museum filetype:bitmap',
            'Pushkin house museum filetype:bitmap',
            'Lermontov estate museum filetype:bitmap',
        ),
        r"(?=.*(?:yesenin|esenin|есенин|alexander blok|александр блок|mayakov|маяков|pasternak|пастернак|pushkin|пушкин|lermontov|лермонтов))(?=.*(?:museum|музей|house|дом|estate|усадьб))",
        r"plaque|таблич|sign|вывеск|souvenir|gift shop",
        6,
    ),
    Topic(
        "ephemera",
        "biblical-manuscript-images",
        (
            'Codex Sinaiticus filetype:bitmap',
            'Dead Sea Scrolls filetype:bitmap',
            'Qumran manuscript filetype:bitmap',
            'Papyrus Bodmer filetype:bitmap',
            'P72 manuscript filetype:bitmap',
            'Greek New Testament papyrus filetype:bitmap',
            'Hebrew Bible manuscript filetype:bitmap',
        ),
        r"sinaitic|dead sea scroll|qumran|papyrus bodmer|(?:^|\W)p72(?:\W|$)|new testament papyrus|hebrew bible manuscript",
        r"modern replica|souvenir|museum display|book cover",
        10,
    ),
    Topic(
        "ephemera",
        "reformation-puritan-portraits",
        (
            'John Calvin portrait filetype:bitmap',
            'John Owen portrait filetype:bitmap',
            'Thomas Goodwin portrait filetype:bitmap',
            'Westminster Assembly engraving filetype:bitmap',
            'Martin Luther portrait filetype:bitmap',
            'Puritan divine portrait filetype:bitmap',
        ),
        r"john calvin|john owen|thomas goodwin|westminster assembly|martin luther|puritan",
        r"reverse|flipped|mirror|statue|monument|modern|plaque",
        8,
    ),
    Topic(
        "ephemera",
        "historic-russian-poetry-audio",
        (
            'Pushkin poem filetype:audio', 'Пушкин стихотворение filetype:audio',
            'Lermontov poem filetype:audio', 'Лермонтов стихотворение filetype:audio',
            'Yesenin poem filetype:audio', 'Есенин стихотворение filetype:audio',
            'Mayakovsky poem filetype:audio', 'Маяковский стихотворение filetype:audio',
            'Blok poem filetype:audio', 'Блок стихотворение filetype:audio',
            'Russian hymn 1917 filetype:audio',
        ),
        r"pushkin|пушкин|lermontov|лермонтов|yesenin|esenin|есенин|mayakov|маяков|alexander blok|александр блок|free russia|свободн.*росс",
        r"contest|конкурс|lesson|урок|children|дет|radio interview|modern podcast",
        8,
    ),
)

# Reject byte-identical files even when Commons exposes them under different titles.
_seen_sha_by_bucket: dict[str, set[str]] = defaultdict(set)
_original_download = collector.download_candidate


def strict_download_candidate(session, candidate, archive_number, output_dir, max_bytes):  # type: ignore[no-untyped-def]
    record = _original_download(session, candidate, archive_number, output_dir, max_bytes)
    if record.status != "DOWNLOADED" or not record.sha256:
        return record
    seen = _seen_sha_by_bucket[record.bucket]
    if record.sha256 in seen:
        if record.local_file_name:
            (Path(output_dir) / record.local_file_name).unlink(missing_ok=True)
        record.status = "DUPLICATE_SHA256"
        record.archive_number = None
        record.local_file_name = None
        record.notes = "Byte-identical duplicate rejected by strict v2 gate"
        return record
    seen.add(record.sha256)
    return record


collector.download_candidate = strict_download_candidate
collector.COLLECTION = "commons-project-materials-strict-120plus"

if __name__ == "__main__":
    raise SystemExit(collector.main())
