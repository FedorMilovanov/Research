# OPEN_HOLDS — открытые HOLD-ы реестров SUNO_HYMNS

Файл собран скриптом `scripts/render_hold_ledger.py` из `data/source-registry-v1.json` и `data/claim-ledger-v1.json`; сборка от 2026-10-28. **Вручную не править** — при изменении реестров пересобрать: `python3 scripts/render_hold_ledger.py`.

Смысл сводки: HOLD — это обещание, которое ещё не исполнено. Список ниже — перечень того, что в текстах рубрики **нельзя** выдавать за проверенное.

## Что означает каждый вид

- `ARCHIVE_HOLD` — источник существует, но содержание недоступно: пейволл, закрытый архив, недоступная книга, файл, который не удалось открыть.
- `LOCATOR_HOLD` — цитата есть, а точного локатора нет или он не сверен с печатным изданием: нет страницы, столбца, номера строки.
- `EVIDENCE_HOLD` — свидетельству не хватает силы: источник не приобретён, содержание известно по вторичному пересказу, утверждение держится на одном косвенном свидетельстве.
- `RIGHTS_HOLD` — права на воспроизведение не выяснены: цитировать минимально необходимым объёмом, целиком текст не перепечатывать.

## Сводка

| Вид | У источников | У тезисов |
|---|---|---|
| `ARCHIVE_HOLD` | 16 | 29 |
| `LOCATOR_HOLD` | 26 | 14 |
| `EVIDENCE_HOLD` | 3 | 11 |
| `RIGHTS_HOLD` | 124 | 43 |

`RIGHTS_HOLD` стоит почти на всём: это общая оговорка о правах, а не конкретная дыра. Отдельного внимания требуют три остальных вида.

## `ARCHIVE_HOLD`

**Источники**

- `SRC-ENSIE-VANDALE-1898` — Groot woordenboek der Nederlandsche taal (Van Dale, 1898) on Ensie  
  доступ: `LINK_ONLY`, локатор: `EXACT_LOCATOR_VERIFIED`, права: `PERMISSION_REQUIRED`
- `SRC-GTB-WNT-INTERFACE` — Geïntegreerde Taalbank — WNT/MNW/VMNW search interface  
  доступ: `LINK_ONLY`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-NL-LIEDERENBANK` — Nederlandse Liederenbank (Meertens Instituut / KNAW) — Dutch Song Database  
  доступ: `NOT_ACQUIRED`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-NL-LIEDERENBANK-9086` — Nederlandse Liederenbank record 9086 — Heerlijckheyds Loff (offline 2026-10-26)  
  доступ: `CATALOG_ONLY`, локатор: `EXACT_LOCATOR_VERIFIED`, права: `RIGHTS_UNKNOWN`
- `SRC-NL-LIEDERENBANK-INDEX` — Nederlandse Liederenbank — records surfaced through search indexing while the site is offline  
  доступ: `LINK_ONLY`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-CLEM-COSGROVE` — Charles H. Cosgrove, «Clement of Alexandria and Early Christian Music», Journal of Early Christian Studies 14/3 (2006): 255–282  
  доступ: `NOT_ACQUIRED`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-CLEM-HYMNARC` — Hymnology Archive (Chris Fenner), страница о гимне «Στόμιον πώλων ἀδαῶν» — рукописи, издания, переводы, оценки  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-CLEM-OXY-PAPYRI` — Blumell & Wayment, Christian Oxyrhynchus: Texts, Documents, and Sources (Baylor, 2015) — сводка христианских папирусов Оксиринха  
  доступ: `NOT_ACQUIRED`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-CLEM-PHILLIPS` — C. S. Phillips, «Hymnody Past and Present» (1937) — формулировка о древнейшем датируемом христианском гимне (известна в цитате)  
  доступ: `NOT_ACQUIRED`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-EPIPHANIUS-PANARION-78` — Епифаний Саламинский, «Панарион», гл. 78 (против коллиридиан) — греческий текст по Migne PG 42, стб. 736–738, набранный и переведённый Eric Sowell (2012)  
  доступ: `PARTIAL_OBJECT`, локатор: `EXACT_LOCATOR_VERIFIED`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-OXY-TEXT` — Cosgrove 2011, текст и перевод Оксиринхского гимна (P.Oxy. XV 1786) с разметкой лакун  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-PRAVENC` — «Свете тихий» — Православная энциклопедия, т. 62, с. 54–55 (свящ. Михаил Желтов)  
  доступ: `FULL_OBJECT_VERIFIED`, локатор: `EXACT_LOCATOR_VERIFIED`, права: `PERMISSION_REQUIRED`
- `SRC-PHOS-SHOEMAKER-2008-KOLLYRIDIANS` — Stephen J. Shoemaker, «Epiphanius of Salamis, the Kollyridians, and the Early Dormition Narratives: The Cult of the Virgin in the Fourth Century», Journal of Early Christian Studies 16.3 (2008): 371–401, DOI 10.1353/earl.0.0185 — аннотация прочитана, полный текст за пейволлом  
  доступ: `LINK_ONLY`, локатор: `COARSE_LOCATOR_ONLY`, права: `PERMISSION_REQUIRED`
- `SRC-PHOS-SUBTUUM-RYL-PLATE` — P.Ryl. III 470 — цифровая копия папируса с текстом Ὑπὸ τὴν σὴν εὐσπλαγχνίαν (Манчестер, John Rylands Library, цифровые коллекции)  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-TEDEUM-TEXT` — Латинский текст Te Deum по римской официальной редакции (Liber Usualis) и древнейший список — Бангорский антифонарий  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PSALMENGEZ-1938-75` — Psalmen en Gezangen (Hervormde Bundel 1938), Gezang 75, p. 501, nr. 239  
  доступ: `CATALOG_ONLY`, локатор: `EXACT_LOCATOR_VERIFIED`, права: `RIGHTS_UNKNOWN`

**Тезисы**

- `CLM-NL-LIEDERENBANK-OFFLINE` — Access state of the Dutch Song Database  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-AUTHORSHIP` — Authorship  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-CLEM-METRE-WILAMOWITZ` — Размер по Виламовицу: исправен, с бытовой параллелью  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-CLEM-MS-ABSENT` — Новое препятствие: гимн отсутствует в одной из основных рукописей  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-CLEM-NEXT-READING` — Найдено и не открыто: следующее чтение  
  статус: `RESEARCH_OPEN`
- `CLM-PHOS-CLEM-NEXT-READING-2` — Следующее чтение: список уточнён до семи позиций с точными локаторами  
  статус: `RESEARCH_OPEN`
- `CLM-PHOS-CLEM-NEXT-READING-3` — Что читать следующим: список после прочтения описания кодекса  
  статус: `RESEARCH_OPEN`
- `CLM-PHOS-CLEM-NEXT-READING-4` — Что читать следующим: список после части 10  
  статус: `RESEARCH_OPEN`
- `CLM-PHOS-CLEM-NEXT-READING-5` — Что читать следующим: список после части 11  
  статус: `RESEARCH_OPEN`
- `CLM-PHOS-CLEM-NO-SECOND-EDITION` — Второго независимого издания греческого текста нет  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-CLEM-PAPYRUS-SEARCH` — Папирусный свидетель гимна: прямой поиск  
  статус: `REPORTED_NOT_INDEPENDENTLY_VERIFIED`
- `CLM-PHOS-CLEM-SECOND-GREEK-TEXT` — Второй греческий текст найден и расходится с первым  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-CLEM-STRUCTURE-DISPUTED` — Счёт строк, деление и ссылка на место  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-CLEM-VERSE-COUNT` — Счёт стихов гимна по аппарату издания: 65  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-CLEM-WITNESS` — Рукописные свидетели гимна Климента  
  статус: `SUPPORTED_BY_SECONDARY_SOURCE_NEEDS_COLLATION`
- `CLM-PHOS-COLLYRIDIANS-RECONSIDERED` — Коллиридиане пересмотрены: по Шумейкеру 2008, это не язычницы и не поклонницы богини, а почитательницы святой  
  статус: `REPORTED_NOT_INDEPENDENTLY_VERIFIED`
- `CLM-PHOS-DATING-OPEN` — Date of composition  
  статус: `RESEARCH_OPEN`
- `CLM-PHOS-DORMITION-ORIGINS-PALESTINE` — Сказания об Успении — древнейшие свидетельства молитвы к Марии, и они из той же Палестины, что наш гимнал  
  статус: `REPORTED_NOT_INDEPENDENTLY_VERIFIED`
- `CLM-PHOS-EARLIEST-INTERCESSION-LIBER-REQUIEI` — Древнейшее свидетельство веры в ходатайство Марии — в сказании III века; и оно не делает её исключительной  
  статус: `REPORTED_NOT_INDEPENDENTLY_VERIFIED`
- `CLM-PHOS-EPIPHANIUS-COLLYRIDIANS` — Что Епифаний на самом деле говорит о почитании Марии: жертва запрещена, почитание — нет, а конца её он не знает  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-EPIPHANIUS-TIME-PROSKYNEO` — Граница Епифания проходит внутри почитания (τιμή против προσκυνέω), и он не протопротестант  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-MARIAN-DEVOTION-ORIGINS` — Откуда пошло почитание: свидетельств до 150 г. нет, культа — до середины IV в., а Ефес 431-го не создал его, а поджёг  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-MARIAN-EVIDENCE-KINDS` — Где лежат ранние свидетельства: не у отцов, а в апокрифах и богослужении — и главное из них то, что мы читали  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-NORELLI-INTERCESSION-CAUSE` — Норелли: сказания об Успении возникли из веры в ходатайство Марии — того самого, о котором наш гимн  
  статус: `REPORTED_NOT_INDEPENDENTLY_VERIFIED`
- `CLM-PHOS-OXY-LINE2-READING` — Строка 2 Оксиринхского гимна: чтением издания признано τὰν ἠῶ, πρυτανήω оставлено в аппарате  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-OXY-PLATE-LOCATED` — Снимок папируса P.Oxy. XV 1786 найден: файл POxy_1786.jpg на Викискладе, источник — Оксфорд, общественное достояние; но прочитать его я не могу  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-OXY-PW-EXTENT` — Что именно сохранилось на папирусе по строкам: строка 4 цела кроме одной буквы, строка 5 — последняя, её начало пропало, но ноты остались  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-OXY-PW-NOTATION-DISPUTED` — Спорят не только о словах: отдельные ноты Оксиринхского гимна читаются по-разному у Ханта, Вагнера, Пёльманна, Уиннингтон-Инграма и Уэста  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-SIX-BOOKS-BETHLEHEM-DATING` — «Шестикнижное сказание» — вифлеемская традиция: не менее пяти сирийских рукописей V–VI вв., датировка IV веком  
  статус: `REPORTED_NOT_INDEPENDENTLY_VERIFIED`

## `LOCATOR_HOLD`

**Источники**

- `SRC-HB-1938-PRINT` — Psalmen en Gezangen voor den Eeredienst (Hervormde Bundel, 1938) — printed object  
  доступ: `NOT_ACQUIRED`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-MEDITATIEN-1674` — Meditatien over eenige van 's Heeren Gods Eygenschappen (1674)  
  доступ: `NOT_ACQUIRED`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-AZBYKA` — Азбука веры, статья «Свете Тихий» — церковнославянский текст, русский перевод, толкование  
  доступ: `PARTIAL_OBJECT`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-BASIL-DATE` — Новая католическая энциклопедия, статья «Basil, St.» — датировка трактата De Spiritu Sancto  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-CLEM-COSGROVE` — Charles H. Cosgrove, «Clement of Alexandria and Early Christian Music», Journal of Early Christian Studies 14/3 (2006): 255–282  
  доступ: `NOT_ACQUIRED`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-CLEM-OXY-PAPYRI` — Blumell & Wayment, Christian Oxyrhynchus: Texts, Documents, and Sources (Baylor, 2015) — сводка христианских папирусов Оксиринха  
  доступ: `NOT_ACQUIRED`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-CLEM-PHILLIPS` — C. S. Phillips, «Hymnody Past and Present» (1937) — формулировка о древнейшем датируемом христианском гимне (известна в цитате)  
  доступ: `NOT_ACQUIRED`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-COOGAN-2019-ODES` — Jeremiah Coogan, приложение «16 Appendix: The Odes» (Oxford University Research Archive, 2019) — научный разбор рукописной традиции библейских Од: Александрийский кодекс, составление, издания  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-CPDL` — ChoralWiki (CPDL), 'Phos Hilaron' — Greek text and translations  
  доступ: `FULL_OBJECT_VERIFIED`, локатор: `COARSE_LOCATOR_ONLY`, права: `PUBLICATION_ELIGIBLE`
- `SRC-PHOS-DOXOLOGIA` — «Η Μεγάλη Δοξολογία» — греческий богослужебный текст Великого славословия  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-EPIPHANIUS-PANARION-78` — Епифаний Саламинский, «Панарион», гл. 78 (против коллиридиан) — греческий текст по Migne PG 42, стб. 736–738, набранный и переведённый Eric Sowell (2012)  
  доступ: `PARTIAL_OBJECT`, локатор: `EXACT_LOCATOR_VERIFIED`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-LATIN-RENDERINGS` — Латинские переложения Φῶς ἱλαρόν — `Lumen hilare` и `Iucunda lux tu gloriae` (форумные и блоговые свидетельства)  
  доступ: `PARTIAL_OBJECT`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-ODES` — Odes of Solomon — date, language and manuscripts (survey article, read as excerpts)  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-ODES-BOOK` — 'Book of Odes (Bible)' — survey of the Greek ode collections and of Codex Alexandrinus  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-OXY-COSGROVE-2011` — Cosgrove Ch. H., An Ancient Christian Hymn with Musical Notation: Papyrus Oxyrhynchus 1786: Text and Commentary (STAC 65; Tübingen: Mohr Siebeck, 2011) — прочитаны предисловие, оглавление и глава первая «Introduction» (с. V–11) по издательскому фрагменту PDF  
  доступ: `PARTIAL_OBJECT`, локатор: `EXACT_LOCATOR_VERIFIED`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-OXY-MIHALYKO-2019` — Mihálykó Á. T., The Christian Liturgical Papyri: An Introduction (STAC 114; Tübingen: Mohr Siebeck, 2019) — прочитаны титул, предисловие, оглавление, сокращения, издательское примечание и введение первой главы по издательскому фрагменту PDF  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-OXY-TEXT` — Cosgrove 2011, текст и перевод Оксиринхского гимна (P.Oxy. XV 1786) с разметкой лакун  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-POXY` — Oxyrhynchus hymn, P.Oxy. XV 1786 — datings and description (search excerpts, 2025 reporting)  
  доступ: `PARTIAL_OBJECT`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-RUSKLINE-BALMONT` — Л. Яцкевич, «Свете тихий… Заметки литературоведа» (Русская линия, 2018) — цитирует переложение К. Бальмонта  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-SDAMP` — Московская Сретенская духовная академия, «Песнопение вечерни „Свете Тихий“: богословско-филологический комментарий»  
  доступ: `PARTIAL_OBJECT`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-SUBTUUM` — 'Sub tuum praesidium' — survey of the Greek text, the Rylands papyrus 470 and the dating dispute  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-SUBTUUM-TEXT` — Греческий текст Ὑπὸ τὴν σὴν εὐσπλαγχνίαν (Sub tuum praesidium) и спор о датировке Райландского папируса 470  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-TEDEUM` — 'Te Deum' — authorship, date and liturgical history  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-TEDEUM-NCE` — Новая католическая энциклопедия, статья Te Deum (Мишель Угло): атрибуции по рукописям, датировка, состав, мелодия  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-PHOS-TEDEUM-TEXT` — Латинский текст Te Deum по римской официальной редакции (Liber Usualis) и древнейший список — Бангорский антифонарий  
  доступ: `PARTIAL_OBJECT`, локатор: `COARSE_LOCATOR_ONLY`, права: `RIGHTS_UNKNOWN`
- `SRC-R-OVER-YSSEL-1630-WORK` — Over-Ysselsche sangen en dichten — 1630 edition as underlying work  
  доступ: `NOT_ACQUIRED`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`

**Тезисы**

- `CLM-DUTCH-001-DATE` — Date attributed to Schepselen niet en Jesus al  
  статус: `SUPPORTED_BY_SECONDARY_SOURCE_NEEDS_COLLATION`
- `CLM-DUTCH-001-TITLE-TUNE` — Schepselen niet en Jesus al title and tune  
  статус: `SUPPORTED_BY_SECONDARY_SOURCE_NEEDS_COLLATION`
- `CLM-DUTCH-003-SONNET-DRAMATURGY` — DUTCH-003: the sonnet's structure, turn and closing line  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-DUTCH-004-TEXT` — DUTCH-004 source text and title  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-CLEM-NEXT-READING-2` — Следующее чтение: список уточнён до семи позиций с точными локаторами  
  статус: `RESEARCH_OPEN`
- `CLM-PHOS-CLEM-PAPYRUS-SEARCH` — Папирусный свидетель гимна: прямой поиск  
  статус: `REPORTED_NOT_INDEPENDENTLY_VERIFIED`
- `CLM-PHOS-CLEM-WITNESS` — Рукописные свидетели гимна Климента  
  статус: `SUPPORTED_BY_SECONDARY_SOURCE_NEEDS_COLLATION`
- `CLM-PHOS-EPIPHANIUS-COLLYRIDIANS` — Что Епифаний на самом деле говорит о почитании Марии: жертва запрещена, почитание — нет, а конца её он не знает  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-IDENTITY` — Text of the hymn  
  статус: `SUPPORTED_BY_SECONDARY_SOURCE_NEEDS_COLLATION`
- `CLM-PHOS-OXY-COSGROVE-AUTOPSY` — Текст и нотация у Косгроува проверены по папирусу, в том числе под большим увеличением  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-OXY-HYMNS-CORPUS-COMING` — Корпус христианских греческих гимнов на папирусе готовит Селин Грасьен: более 200 гимнов — адрес для будущих номеров серии  
  статус: `RESEARCH_OPEN`
- `CLM-PHOS-OXY-MIHALYKO-CORPUS` — По новейшему своду, литургических папирусов III века сохранился ровно один — на фоне 323 учтённых предметов  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-PHOS-OXY-SETTING-HYPOTHESES` — Где пелся Оксиринхский гимн: евхаристия (Вольбергс), агапа и солист (Уршпрунг) — три гипотезы, ни одна не доказана  
  статус: `REPORTED_NOT_INDEPENDENTLY_VERIFIED`
- `CLM-REVIUS-1630` — Hy droech onse smerten: first publication and genre  
  статус: `SUPPORTED_BY_SECONDARY_SOURCE_NEEDS_COLLATION`

## `EVIDENCE_HOLD`

**Источники**

- `SRC-HB-1938-PRINT` — Psalmen en Gezangen voor den Eeredienst (Hervormde Bundel, 1938) — printed object  
  доступ: `NOT_ACQUIRED`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-MEDITATIEN-1674` — Meditatien over eenige van 's Heeren Gods Eygenschappen (1674)  
  доступ: `NOT_ACQUIRED`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`
- `SRC-R-OVER-YSSEL-1630-WORK` — Over-Ysselsche sangen en dichten — 1630 edition as underlying work  
  доступ: `NOT_ACQUIRED`, локатор: `LOCATOR_MISSING`, права: `RIGHTS_UNKNOWN`

**Тезисы**

- `CLM-CAND-006-CRUYCE` — Candidate DUTCH-CAND-006: 't Cruyce van een christen, item 57  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-DUTCH-002-STANZAS-14-7-5` — DUTCH-002: stanza counts across the three forms  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-DUTCH-003-SONNET-DRAMATURGY` — DUTCH-003: the sonnet's structure, turn and closing line  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-DUTCH-005-TRANSMISSION-1681-1718` — DUTCH-005: reprints between the first edition and the nineteenth century  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-DUTCH-005-TUNE-SHIFT` — DUTCH-005: the tune direction changes between 1676 and 1718  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-DUTCH-005-VARIANTS` — DUTCH-005: variants between the 1676 and 1727 printings  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-HB-1938-75-TEXT` — 1938 hymnal: Gezang 75 is a three-stanza reworking  
  статус: `REPORTED_NOT_INDEPENDENTLY_VERIFIED`
- `CLM-HEERLIJCKHEYD-RECEPTION` — Transmission of 'Heerlijckheyds Loff' and the 1938 trap  
  статус: `SUPPORTED_BY_SECONDARY_SOURCE_NEEDS_COLLATION`
- `CLM-HERT-II-DATE-1674` — Date of II. Hert-sterckte in Jehova  
  статус: `EVIDENCE_HOLD`
- `CLM-REES-MEDITATIEN-1674` — The four-poem Rees group and the 1674 pamphlet  
  статус: `SUPPORTED_WITH_SCOPE_LIMITS`
- `CLM-REVIUS-1630` — Hy droech onse smerten: first publication and genre  
  статус: `SUPPORTED_BY_SECONDARY_SOURCE_NEEDS_COLLATION`

## `RIGHTS_HOLD`: где права требуют отдельного решения

Источники, у которых права помечены как требующие разрешения или не выясненные и при этом текст не прочитан полностью:

- `SRC-AFR-L271` — Afrikaans Lied 271 — modern source-chain page  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`
- `SRC-AFR-L276` — Afrikaans Lied 276 — modern source-chain page  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`
- `SRC-ENSIE-VANDALE-1898` — Groot woordenboek der Nederlandsche taal (Van Dale, 1898) on Ensie  
  доступ: `LINK_ONLY`, права: `PERMISSION_REQUIRED`
- `SRC-HB-1938-PRINT-CALIBRATION` — Page map of the 1938 Hervormde Bundel — calibration points for locating an item  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`
- `SRC-HB-1938-PRINT-COLLATED` — Gezang 205 in the printed 1938 Hervormde Bundel — collated page images 724-725  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`
- `SRC-L-CHRISTEN-SANGERS` — Christen sangers — preface in the critical edition  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`
- `SRC-L-CRIT-2005` — Uyt-spanningen — critical edition and apparatus (2005)  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`
- `SRC-L-CRIT-2005-HEERLIJCKHEYD` — Critical-edition item 56 — Heerlijckheyds loff, p. 263  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`
- `SRC-L-CRIT-2005-INTRO` — Critical-edition introduction, 'Ds. Jodocus van Lodenstein en zijn Uyt-spanningen 1676', pp. 645-647  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`
- `SRC-L-CRIT-2005-MELODIEREGISTER` — Melodie-register of the 2005 critical edition, printed pp. 663-664  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`
- `SRC-L-HERT-I-1673-34` — I. Hert-sterckte in Jehova, Op 1 Sam. 30:6 — critical-edition item 34  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`
- `SRC-L-SCHEPSELEN-51` — Schepselen niet en Jesus al — critical-edition item 51  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`
- `SRC-PHOS-SHOEMAKER-2008-KOLLYRIDIANS` — Stephen J. Shoemaker, «Epiphanius of Salamis, the Kollyridians, and the Early Dormition Narratives: The Cult of the Virgin in the Fourth Century», Journal of Early Christian Studies 16.3 (2008): 371–401, DOI 10.1353/earl.0.0185 — аннотация прочитана, полный текст за пейволлом  
  доступ: `LINK_ONLY`, права: `PERMISSION_REQUIRED`
- `SRC-R-HY-DROEG` — Hy droech onse smerten — poem page in the W.A.P. Smit edition  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`
- `SRC-R-OVER-YSSEL-CONTENTS` — Over-Ysselsche sangen en dichten — scholarly edition contents  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`
- `SRC-UTRECHT-HYMNI-1615-1967` — Hymni ofte Loff-sangen — 1967 facsimile of a work first printed in 1615  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`
- `SRC-UTRECHT-HYMNI-1615-WORK` — Hymni ofte Loff-sangen — underlying 1615 original work  
  доступ: `PARTIAL_OBJECT`, права: `PERMISSION_REQUIRED`

## Порядок закрытия

1. HOLD снимается только после того, как сделано дело: источник прочитан, локатор сверен, права выяснены. Формулировки «проверено» без этого не пишутся.
2. При снятии HOLD правится и реестр, и зеркала; затем этот файл пересобирается.
3. Если дыру закрыть нельзя (архив недоступен), она остаётся в списке и прямо оговаривается в тексте рубрики.

