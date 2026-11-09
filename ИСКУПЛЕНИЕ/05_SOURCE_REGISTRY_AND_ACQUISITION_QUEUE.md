# Искупление — source registry и очередь добычи

> **Дополнение 2026-11-06:** действующая тематическая очередь систематик, специальных книг и исследований — раздел **N** ниже: SYS-01–39, MON-01–46, ART-01–14. Сведения об издании, разрешённый фрагмент и реально прочитанный контекст разнесены. Старые карточки сохраняются; одно наличие имени не означает чтения.
>
> **Волна 1 / 2026-11-07:** [первичный адресный протокол Дабни–Девенант–Оуэн](evidence/WAVE1_DABNEY_DAVENANT_OWEN_PRIMARY_WITNESSES_2026-11-07.md). Веб-контекст собственной главы Дабни читается напрямую; латинские сегменты Девенанта §1/24/75 адресно прочитаны; собственный цифровой Оуэн III.VII проверен. **Уточнение W1-S0-02:** оригинальные печатные страницы Дабни 1878 **521 и 648 адресно просмотрены** (см. протокол с прямыми ссылками), но **не** вся глава; `DABNEY_OTHER_PAGES_HOLD` для 520/522/523. Факсимиле Девенанта 1650 доступно (печатная с. 21 просмотрена), однако текст веб-сегментов 1/24/75 в нём пока не локализован; `DAVENANT_LATIN_EDITION_HOLD` сохраняется. Общий `PUBLICATION_HOLD` и права современной литературы не сняты. Старые карточки не повышаются автоматически.

> **W1-S0-03 — актуализация 2026-11-07 (предыдущая запись W1-S0-02 выше — исторический срез):** Дабни 1878, **печатные с. [520](https://archive.org/details/syllabusnotesofc00dabn/page/520/mode/1up)–[523](https://archive.org/details/syllabusnotesofc00dabn/page/523/mode/1up)** плюс ранее проверенная 648 — узкие фотосвидетельства (`DABNEY_520_523_FACSIMILE_VERIFIED`), но не полный том. Девенант 1650, **печатные с. [1 / n10](https://archive.org/details/bim_early-english-books-1641-1700_dissertationes-du-_davenant-john-bp_1650/page/n10/mode/1up), [32 / n41](https://archive.org/details/bim_early-english-books-1641-1700_dissertationes-du-_davenant-john-bp_1650/page/n41/mode/1up), [69 / n78](https://archive.org/details/bim_early-english-books-1641-1700_dissertationes-du-_davenant-john-bp_1650/page/n78/mode/1up)** теперь локализуют онлайн-сегменты 1/24/75 соответственно (`DAVENANT_1650_THREE_PRINT_LOCI_VERIFIED`, **A2 только для этих фрагментов**). Старые `DABNEY_OTHER_PAGES_HOLD` и общий `DAVENANT_LATIN_EDITION_HOLD` **SUPERSEDED в узком вопросе локаторов**, но `DABNEY_FULL_BOOK_COLLATION_HOLD`, дипломатическая колляция латинского издания, `AI_TRANSLATION_HOLD`, `RIGHTS_HOLD` и `PUBLICATION_HOLD` остаются. Точные уровни, фактическое чтение и печатная пагинация — в [действующем протоколе](evidence/WAVE1_DABNEY_DAVENANT_OWEN_PRIMARY_WITNESSES_2026-11-07.md); страницы и кадры не считать отдельными полными приобретёнными книгами.

**Дата:** 2026-10-07
**Статус:** ACTIVE / EVIDENCE REGISTRY
**Правило:** запись в таблице не есть quote-safe. `QUOTE_SAFE=YES` только при полном тексте + локаторе + правах.

Легенда ярусов (локальная, совместимая с apostasy-реестром, не замена глобальной A1–D):

- **P-BIBLE** — Писание / язык
- **P-CONFESSION** — исповедание
- **P-PATRISTIC** — Отец
- **P-REFORMED** — реформатский/пуританский первоисточник
- **SCHOLARLY-OPEN** — открытая академия
- **MODERN-COPYRIGHT** — нужная книга XX–XXI вв.; полный файл без прав запрещён
- **LEAD** — нужна, текста нет
- **SECONDARY** — навигация

Custody по `artifact-custody-policy-v2.json`: `LINK_ONLY` / `PRIVATE_STUDY_ONLY` / `ACQUIRED_DURABLE` / …

---

## A. Писание и открытый языковой слой

| ID | Tier | Source | URL / locator | Supports | Status | Quote-safe | Custody |
|---|---|---|---|---|---|---|---|
| S01 | P-BIBLE | NA28 / ECM NT | product/research Bible corpus; не копировать критическое издание целиком | греческий НЗ | LEAD / use existing Bible tools | NO until edition+verse | LINK_ONLY |
| S02 | P-BIBLE | BHS / WLC OT | BHS доступен как S13 / nt S6; WLC-объект отдельно не приобретён | еврейский ВЗ | **PARTIAL via S13**: прежнее «MT не получен ни одним слоем» SUPERSEDED; текст S6 проверен, apparatus BHS не получен | YES для проверенного цифрового текста S6; не физический кодекс | см. S13; publication `BLOCKED` |
| S03 | P-BIBLE | LXX Rahlfs/Göttingen | эти издания отдельно не получены; цифровой Swete 1901 — S10 / nt S5 | LXX-культовый/лексический фон | **PARTIAL alternative**: Swete не равен Rahlfs/Göttingen; 14 сопоставлений в nt/11_, не полный apparatus | YES в scope S5; lemma-нули без лемматизации отозваны | S5 `STORAGE_ONLY`; publication `BLOCKED` |
| S04 | P-BIBLE | Синодальный / сопоставление русских | reader-facing цитаты только с указанием перевода | русская публикация | OPEN | YES with edition | LINK_ONLY |
| S05 | P-BIBLE | **MorphGNT / SBLGNT** (свидетель **S1** под-корпуса НЗ) | https://github.com/morphgnt/py-sblgnt @ `904fed08a14bffea6e1776d8c4c3eeb7c6092688`; sha256 `f95833b1…`, 9 822 443 байт; 137 554 словоформы | греческий текст + морфология для всех подсчётов `nt/` | **ACQUIRED** (вне Git, `/home/user/nt-corpus/`); **без критического аппарата** | YES для текста и разбора; **NO** для атрибуции рукописей | PRIVATE_STUDY_ONLY |
| S06 | P-BIBLE | **Scrivener 1894 Textus Receptus** (свидетель **S2**) | https://github.com/byztxt/greektext-scrivener @ `6049a43b135ed870f843b83eb6a04764fc796678`; PD; sha256 `783e510d…` | TR-сверка вариантов | **ACQUIRED** | YES (PD) | PRIVATE_STUDY_ONLY |
| S07 | P-BIBLE | **Stephens 1550 TR** (свидетель **S3**) | https://github.com/byztxt/greektext-stephens @ `4314af2042d9e77b2ce5c1c86d0c49325dd81684`; sha256 `8f5bc4b8…` | TR-сверка вариантов | **ACQUIRED** | YES (PD) | PRIVATE_STUDY_ONLY |
| S08 | P-BIBLE | **Elzevir TR** (свидетель **S4**) | https://github.com/byztxt/greektext-elzevir @ `94f31e2d2e8bd451d4d2f9739d13c419f7ce86c2`; sha256 `e7c730b9…` | TR-сверка вариантов | **ACQUIRED** | YES (PD) | PRIVATE_STUDY_ONLY |
| S14 | P-BIBLE | SBLGNT TEI / nt S7 | jjmccollum/sblgnt-tei @ 2a95589b2a9cb9b8bda5372650c7f55745ceecad; sha256 dc2888b9…; 6929 app / 4471 positions / 13 declared sigla | цифровая атрибуция изданиям | **FULL_OBJECT_VERIFIED**, exact digital locators; header NA 27 / 1979 — CONFLICT; NA silence ≠ agreement; NA28/UBS5 как полные editions не получены | YES как запись S7; NO как physical manuscript/codex attribution | `PUBLICATION_ELIGIBLE` (pinned CC BY 4.0); publication `BLOCKED` |
| S09 | P-BIBLE | Критический apparatus — общий вопрос | S14 / nt S7 и selected collations S18/S19 / nt S9/S10 | варианты, coverage, идентичность свидетелей | **PARTIAL / NOT CLOSED**: получены выборочные цифровые единицы; LOCATOR_HOLD по unit/question, qualifiers, named codices, full edition access. Прежнее «закрыт по существу» SUPERSEDED | NO для необоснованного общего closure | publication `BLOCKED`; source rights отдельно в nt SSOT |
| S10 | P-BIBLE | Swete LXX 1901, digital First1KGreek / nt S5 | nathans/lxx-swete @ 26bad3eb42bba98471d154c954e36a6f30a0279d; 55 files; sha256 5cf3ee82… | MT/LXX pairs и фон НЗ | **FULL_OBJECT_VERIFIED** как цифровой набор; 14 сопоставлений / 48 diagnostic pairs (47 читаются). Deut 21:23 locator conflict; prefix zeros не lemma absence. Старый LXX access-HOLD SUPERSEDED only for text | YES для bounded digital quotations; не полный печатный аппарат | `STORAGE_ONLY` (digital CC BY-SA 4.0, not code MIT); publication `BLOCKED` |
| S11 | SECONDARY | Tyndale **STEPBible-Data** | https://github.com/tyndale/STEPBible-Data (≈721 МБ; `Tagged-Bibles`, `Lexicons`, `Versification`) | кандидат на дополнительные издания и лексиконы для S09/S10 | NOT DOWNLOADED | NO | LINK_ONLY |
| S13 | P-BIBLE | BHSA-min / BHS Text-Fabric 2021 / nt S6 | ETCBC/bhsa-min @ f600a50fd902b6c9d31d67cf5611365df4169bce; sha256 51922d3b…; 56 files / 23213 verses / 426590 slots | MT lookup и ограниченные пары с S5 | **FULL_OBJECT_VERIFIED** как цифровой набор; exact slot/verse locators. Empty graphic article slots не удаляются; כפר lex_utf8 = 102 verbs + 20 nouns. Apparatus/physical codex не получен | YES для digital text/feature observations; NO для manuscript identification | `PRIVATE_STUDY_ONLY`; MIT относится к коду, не разрешению данных; publication `BLOCKED` |
| S15 | P-CONFESSION | Дорт II, English 1840 в каноническом 16_ | [16_](16_DORT_HEAD_II_ENGLISH_1840_PRIMARY_TEXT.md) §1, Articles III/V/VI/VIII; Scott/Latin control в 15_ §B.5–B.6 | институциональный исторический контроль, не Greek exegesis | **PARTIAL_OBJECT / A3**, exact local article + SHA в nt SSOT; не новый полный оригинал/скан. Covenant London future-date/three-copy/PD claims — HISTORICAL/UNVERIFIED, не рабочая provenance | YES только для локально проверенных 1840 excerpts; не proof of NT intent | `PUBLICATION_ELIGIBLE` только для принятого 1840 текста; publication `BLOCKED`; modern/ESV отдельно |
| S16 | P-BIBLE | **Tregelles**, *The Greek New Testament* (1857–1879), транскрипция Tyndale House 2009 (свидетель **S8** под-корпуса НЗ) | https://github.com/mrgreekgeek/tregelles-greek-nt @ `07ecf2165c9e404926365f5060b8150e0e19af49`; sha256 `52efbe59…`, 2 файла | независимая проверка аппарата S7: Мк 14:24 / Гал 1:4 / 1 Пет 3:18 / Ин 3:16 — **4 из 4 сошлись** | **ACQUIRED** (вне Git). **Аппарата нет** — 0 вхождений `א`, 0 сокращений версий, несмотря на титул «Various Readings in Full»; рукописный уровень `LOCATOR_HOLD` не закрывает | YES как текст; **NO** как аппарат | текст PD, транскрипция **CC BY-NC-SA 3.0** |
| S17 | P-BIBLE | Siglarium (nam8/sigla-lookup) | https://github.com/nam8/sigla-lookup ; CC BY 4.0 claimed | кандидат для siglum/codex/qualifier mapping | **LEAD / NOT_ACQUIRED**: словарь не полный apparatus и не проверенное соответствие всех ECM qualifiers. Идентификация не «невозможна в принципе»; нужен первичный catalogue/mapping | NO до object/locator verification; профиль голосов не ID | `RIGHTS_UNKNOWN` для конкретного output до проверки; publication `BLOCKED` |
| S18 | P-BIBLE | selected Mark collation / nt S9 | jjmccollum/comp-tc-mark @ 013b2f0db69cf577f866c75c82f5a98cbb558dc2; sha256 a9314ab4…; 148 active units / 119 verse locators / 284 declared records | digital selected UBS5-unit / ECM-record observations | **FULL_OBJECT_VERIFIED** как файл, не вся традиция. Mark 10:45 unit absence ≠ all-284 agreement; 24 reading-token aliases/qualifiers unmapped, LOCATOR_HOLD remains | YES как source record; NO как independent manuscript votes/named codex proof | `PUBLICATION_ELIGIBLE`: pinned LICENSE + TEI CC BY 4.0; publication `BLOCKED` |
| S19 | P-BIBLE | talk/example collations / nt S10 | jjmccollum/sbl-2023-talk @ 4ada2a729cc3e36ab29d101fe924e435d0a8bd54; sha256 5758c2bd…; 5 XML files | coded readings in Acts/Mark/Eph/1Pet/Rev | **FULL_OBJECT_VERIFIED** как набор файлов: Acts 9554/600, old Mark 147/167 (one quarantined impossible 28:8), Eph 42/36, 1Pet 36/64, Rev 70/33 (units/active declarations). Comments excluded; qualifiers unmapped | YES как selected raw collation records, not full UBS5/NA28 or independent vote weights | `PUBLICATION_ELIGIBLE` (pinned CC BY 4.0); publication `BLOCKED` |
| S12 | SECONDARY | PD-лексиконы (Thayer; PD-издания LSJ) | CCEL / archive.org | значения `λύτρον`, `ἀγοράζω`, `ἱλαστήριον` | разрешены брифом, в этой волне не привлекались | NO until locator | LINK_ONLY |


### A-2. Реестр под-корпуса `ot/` (ВЗ) — независимая нумерация

> Строки ниже — реестр ветхозаветного под-корпуса `ot/` (те же серии S, что и таблица выше). Нумерация у него **своя**: совпадение номеров S05–S19 с НЗ-свидетелями верхней таблицы — разные источники. Ссылки «S10», «S11», «S13», «S15», «S23» и т. п. в карточках и SSOT под-корпуса `ot/` относятся именно к этой таблице; верхняя таблица — реестр общего слоя (НЗ-свидетели и аппарат).

| ID | Tier | Source | URL | Supports | Status | Quote-safe | Custody |
|---|---|---|---|---|---|---|---|
| S05 | P-BIBLE | Studylight Interlinear (LXX Greek + BHS/WLC Hebrew на одной странице) | studylight.org/interlinear-study-bible/greek/{книга}/{гл-стих}.html: Быт. 32:20; Исх. 25:17; 30:12; Лев. 4:20; 17:11; Числ. 16:46; 35:33; Пс. 49:7 | MT и LXX для карточки `ot/01` | CHECKED (1z; издание LXX не указано) | NO until edition | LINK_ONLY |
| S06 | P-BIBLE | Blue Letter Bible LXX | blueletterbible.org/lxx/lev/17/1/ | второе зеркало Лев. 17:11 (LXX) | CHECKED (2z для Лев. 17:11) | NO | LINK_ONLY |
| S07 | P-BIBLE | Biblehub multilingual (Swete LXX; MT; переводы) | biblehub.com/multi/leviticus/17-11.htm | второе зеркало Лев. 17:11 | CHECKED (2z) | NO | LINK_ONLY |
| S08 | P-BIBLE | Sefaria API (MT; Revised JPS 2023 EN) | sefaria.org/api/texts/Leviticus.17.11 | MT Лев. 17:11 | CHECKED (MT only) | NO (JPS 2023 — под охраной; только иврит) | LINK_ONLY |
| S09 | EXCLUDED | Вторичный комментарий к LXX Leviticus (Brill), найденный только на пиратском хосте | хост не указан; **не открывался и не используется** | — | EXCLUDED | NO | NOT_STORED; нужен легальный экземпляр владельца |
| S10 | P-BIBLE | Swete 1909 LXX — цифровая транскрипция (Sollupulo/Swete-1909-LXX) | github.com/Sollupulo/Swete-1909-LXX (`1.Genesis`, `2.Exodus`, `3.Leviticus`, `4.Numbers`) | LXX Быт. 32:20; Исх. 25:16–17, 30:12; Лев. 4:20, 17:11; Числ. 16:46, 35:33; карточка 04 (волна 5): Быт. 4:10; 9:4–6; Лев. 1:5; 4:7; 16:14–19, 16:27; 17:4, 10–14; Втор. 12:23; 21:7–9; Исх. 12:7, 12:13; 24:6, 24:8 (сверка с ELI и SOL) | CHECKED (2z; ошибки транскрипции в Лев. 17:11) | NO (CC BY-SA 4.0; не копируется) | NOT_STORED; локаторы |
| S11 | P-BIBLE | LXX Swete 1930 — словарная транскрипция (eliranwong/LXX-Swete-1930) | github.com/eliranwong/LXX-Swete-1930 (`02-…word…csv`, `00-…versification.csv`) | сверка 8 локусов; Числ. 16:47; Пс. 48:8; карточка 04 (волна 5): сверка всех локусов карточки 04 (Быт.–Втор.; Пс. 50:16; Ос. 4:2; Ис. 1:15; Зах. 9:11) | CHECKED (только сверка) | NO (GPL-3.0; данные не копируются) Карточка 12 (волна 14): в ELI-своде `Dan` = OG, `Dat` = Феодотион (проверено на 9:9, 9:19, 9:24, 9:27, 11:31). | NOT_STORED |
| S12 | P-BIBLE | Swete 1887, т. I (Genesis–IV Kings), с apparatus | archive.org/details/oldtestamentingr01swet (djvu.txt, OCR) | apparatus: Лев. 17:11; Числ. 16:46–47 | CHECKED вручную (сигла B*/B² — проверить по изображению) | YES (PD); OCR не копируется | LINK_ONLY |
| S13 | P-BIBLE | MT морфология — openscriptures/morphhb (WLC, OSIS) | github.com/openscriptures/morphhb (`wlc/*.xml`) | леммы и морфология MT, V1–V8, Числ. 17:12; карточка 04 (волна 5): леммы и морфология B1–B29 и контролей K1–K3 (1818, 5315, 2236, 5137, 8210, 5355, 3722); кетив / кери Втор. 21:7 | CHECKED | YES с атрибуцией (аннотация CC BY 4.0; WLC — PD) | NOT_STORED |
| S14 | P-LEX | BDB — openscriptures/HebrewLexicon | github.com/openscriptures/HebrewLexicon (`BrownDriverBriggs.xml`, `LexicalIndex.xml`, readme) | глоссы כפר, כֹּפֶר, כַּפֹּרֶת (k.ct.ac, k.ct.ab, k.cu.ab, k.cu.ac, k.cv.ac, k.ct.ae); карточка 04 (волна 5): BDB d.br.aa (דם), g.co.aa (זרק), n.cj.aa (נזה), v.fh.aa (שפך), n.fe.ab / n.fe.aa (נקי / נקה); HebrewStrong.xml H1818, H3722, H2236, H5137, H8210, H5355, H5315 | CHECKED | YES с атрибуцией (текст PD; компиляция CC BY 4.0) | LINK_ONLY |
| S15 | P-LEX | LSJ — Perseus через cltk/greek_lexica_perseus | github.com/cltk/greek_lexica_perseus (`greek_english_lexicon_lsj_1.xml`, `greek_english_lexicon_lsj_2.xml`; README: MPL 1.1) | глоссы ἐξιλάσκομαι, ἐξιλασμός, ἐξίλασμα, ἱλαστήριον, λύτρον; карточка 04 (волна 5): αἷμα (том I, n2392), ῥαντισμός, ῥαίνω, πνικτός (том II); αἱματεκχυσία — статьи в Perseus-LSJ нет | CHECKED | YES с атрибуцией (MPL 1.1) | LINK_ONLY |
| S16 | P-BIBLE | NT греч. — morphgnt/sblgnt (колонка лемм; текст SBLGNT) | github.com/morphgnt/sblgnt (`61-…` … `87-Re`) | лемма-поиск по 27 книгам: ἐξιλάσκ- — 0 совпадений; ἱλάσκ-, ἱλασμ-, ἱλαστήρ-, λύτρ-, ἀντίλυτρ-; Евр. 9:22; карточка 04 (волна 5): леммы NT: αἷμα 97, ῥαντισμός 2, ῥαντίζω 4, αἱματεκχυσία 1, πνικτός 3, ἐκχέω 27, ἱλαστήριον 2, ἱλασμός 2; Евр. 9:19–22; Мф. 26:28; Лк. 22:19b–20 (скобки SBLGNT) | CHECKED | ЛОКАТОРЫ и короткие фразы (аннотация CC BY-SA 3.0; текст — SBLGNT EULA) | NOT_STORED |
| S17 | P-LIB | Göttingen Septuaginta — статус томов (Gen 1974, Exod 1991, Lev 1986, Num 1982; Псалтирь — проект с 2020) | adw-goe.de (страница Septuaginta); библиография Brill; SearchWorks | ARCHIVE_HOLD; какое издание решит вариант | CHECKED (библиография); текст не открыт | NO (печатное издание) | LINK_ONLY |
| S18 | P-LIB | Göttingen «Text History» (PDF-загрузки на странице ADW: Gen 1974, Num 1982, Lev 1986, Exod 1992) | adw-goe.de (та же страница) | кандидат для истории вариантов | NOT_OPENED (лицензию проверить перед загрузкой) | UNKNOWN | NOT_STORED |
| S19 | EXCLUDED | eliranwong/LXX-Rahlfs-1935 (текст Rahlfs; без лицензии) | github.com/eliranwong/LXX-Rahlfs-1935 | — | EXCLUDED (нет лицензии; текст Rahlfs охраняется) | NO | NOT_STORED; не использовать |
| S20 | CANDIDATE | Holmes–Parsons, VT Graecum cum variis lectionibus (1798–1827) | не открыт (сканы archive.org / Google Books — проверить) | возможный открытый apparatus шире Swete 1887 | NOT_OPENED | UNKNOWN (ожидается PD; проверить) | NOT_STORED |
| S21 | P-BIBLE | theancientbible.org — LXX Исаия 59 (греческий текст) | theancientbible.org/isaiah-lxx-59/ | второе зеркало Ис. 59:20 (ῥυόμενος; карточка `ot/02`) | CHECKED (2z условно: издание не указано) | NO (только сверка) | LINK_ONLY |
| S22 | EXCLUDED | Страницы LXX на основе Rahlfs (die-bibel.de; lire.la-bible.net) — видны только в выдаче поиска | die-bibel.de/bibel/LXX/EXO.13.1-EXO.13.16; lire.la-bible.net/bible/LXX/EXO.13 | — | EXCLUDED (текст Rahlfs; не открывались и не используются; см. S19) | NO | NOT_STORED |
| S23 | P-BIBLE | lxx-swete — LXX Swete (First1KGreek tlg0527; локальный клон; все книги ВЗ) | README клона: производная от OpenGreekAndLatin/First1KGreek, tlg0527 (`lxx-swete/data/`) | третье зеркало ВЗ для карточек 01–03 (Лев. 4–10; Числ. 5, 15, 18; Пс.; Ос.; Иез.; Ис. 53); только сверка; карточка 04 (волна 5): третье зеркало для Быт.–Втор. (карточка 04; сверка); два зеркала для Пс., Ос., Ис., Зах. | CHECKED (третье зеркало; опечатки в Лев. 4:4 и пропуск в Исх. 34:7 учтены) | NO (CC BY-SA 4.0; не копировать) | LINK_ONLY; NOT_STORED Проверка 2026-10-14: для Исаии текст S23 совпадает с кодексом A (издание Оттли 1904, F1K grc2) — 1254 из 1265 стихов; совпадений с grc1/B — 246. | Карточка 12 (волна 14): Дан. в S23 — те же файлы First1KGreek, что и F1K, в двух версиях (56.* = OG, 57.* = Феодотион); совпадение с F1K 401/408 (OG) и 404/412 (Th) стихов слово в слово; в Th гл. 12 обрыв после ст. 4; опечатки транскрипции зафиксированы в карточке (§4b).

---

## B. Исповедания — PD

| ID | Tier | Source | URL | Supports | Status | Quote-safe | Custody |
|---|---|---|---|---|---|---|---|
| C01 | P-CONFESSION | Canons of Dort, Second Head | **Schaff Latin chunk 165** https://www.ccel.org/ccel/schaff/creeds3/cache/creeds3.txt (EN-колонки в этом TXT **нет**: чанки 163–165 — латынь, проверено 2026-10-07); **Scott 1841 EN с. 282–286** — *The Articles of the Synod of Dort…*, пер. Thomas Scott, 1841, archive.org item `articlesofsynodo1841syno`, PD; **EN перевод 1840 г.** — Git [`16`](16_DORT_HEAD_II_ENGLISH_1840_PRIMARY_TEXT.md) (перенесён из Drive `01`, `10_W0_PRIMARY_TEXT_DORT_HEAD_II_AND_CALVIN_2026-10-07.md`, id `1hPs1aEWtwv1GHGHtZVtpWd8c91bQgAgo`): полный английский текст artt. I–IX (1840, Wikisource-транскрипция), **без Rejection**; CRCNA chunks 3–4 — reading copy, перевод 1986 copyright, не dump; карта `15` | sufficiency/efficiency; Rejection I–VII | LATIN PD LOCATED chunk 165; **EN PD EDITION SELECTED** = Scott 1841 (страницы по артикулам I–IX и по Rejectio I–VII); **EN full text** — Scott 1841: артикулы I–IX + Rejectio I–VII в `15` §B.5 (OCR, сличение §B.6); перевод 1840 г.: артикулы I–IX в `16` | Latin YES for research; EN — два независимых перевода, сличенные по латыни (`15` §B.6); сокращение Rejectio IV у Скотта зафиксировано; Product NO, пока действует `PUBLICATION_HOLD` | LINK_ONLY |
| C02 | P-CONFESSION | Westminster Confession ch. 8, 11 | Drive copy `1VSp4vU56X8uuYrp2SERkp2p0BRk-vQq4` (**16 179 601 bytes**, скан без текстового слоя: `read_file_text` → `empty`; страница не извлекаема, не ретраить); **Schaff/CCEL chunks 182–183** = Chapter VIII EN+LA; карта `15` §D | Посредник; объём (8.1 / 8.5 / 8.6 / 8.8); оправдание | **TEXT LOCATED**: Schaff chunks 182–183 (EN+LA, постатейно); **печатная страница закрыта 2026-10-08 и пересчитана: Harper 1919, vol. 3, с. 619–622** (прежний ряд 633–636 был в листах, смещение −14; см. `15` §D.1); Drive PDF — скан без текстового слоя, ось закрыта с доказательством | NO до item-level решения | ACQUIRED_DURABLE copy; locator по странице **снят**, по-прежнему цитировать по главе и статье |
| C03 | P-CONFESSION | WLC 38–59 | **не в томе Шаффа** — Schaff vol. III печатает только fac-simile титула и первой страницы (л. 688–689) и прямо пишет: «Want of space compels us to omit the Assembly's Larger Catechism» (л. 690). Рабочий локатор: *The Larger Catechism* 1813, IA `largercatechism00west`, лист − 12 = страница: **Q. 38 — с. 18; Q. 40 — с. 19; Q. 44 — с. 21; Q. 57 — с. 28; Q. 58–59 — с. 29**; verbatim и разбор — [`15` §D.2](15_CALVIN_III24_AND_DORT_II_LOCATORS.md) | личность и дело Христа; применение через purchased (Q. 59) | **LOCATED** (PD-скан + печатные страницы), изображение страницы не сверено | NO до item-level решения | LINK_ONLY |
| C04 | P-CONFESSION | Second London 1689 ch. 8, 11 | **Локатор параграфов получен (2026-10-12):** PD-скан 1850 г. (Charleston), IA `confessionoffait00char`, лист − 6 = страница, номер вверху страницы. Гл. VIII §5 = **с. 25**; §8 = **с. 25–26** («for whom Christ hath **obtained** eternal redemption»; WCF читает «purchased»); гл. XI §1 = **с. 29**. Текст — OCR полного текста; вторичная сверка с двумя независимыми транскрипциями (reformedreader.org, christreformedchurch.net) совпадает по §8.5 и §8.8; **сверка с факсимиле не делалась**. Подробно — [`15` §D.3](15_CALVIN_III24_AND_DORT_II_LOCATORS.md) | баптистский twin | **LOCATED (параграф, OCR)**; факсимиле — открыт | NO до сверки с факсимиле и item-level решения | LINK_ONLY |
| C05 | P-CONFESSION | Belgic Confession art. XIV–XXIII (XVI — выбор) | Schaff vol. III (1919), IA `creedsofchristen0003phil_c6k6`, лист − 14 = страница; локаторы и вербатим — [`15` §E.1](15_CALVIN_III24_AND_DORT_II_LOCATORS.md) | удовлетворение / вера / выбор (XVI «OF ETERNAL ELECTION») | **LOCATED; вербатим XVI, XX–XXII; XIV–XV, XXIII — только страницы** | NO до item-level решения | LINK_ONLY |
| C06 | P-CONFESSION | Heidelberg Catechism LD 5–7 (Q12–23), LD 15–16 (Q37–44) | Schaff vol. III, с. 311–321; разбивка LD — RCA; локаторы и вербатим — [`15` §E.2](15_CALVIN_III24_AND_DORT_II_LOCATORS.md) | необходимость Посредника; «only such as» (Q20); «whole human race» (Q37); «no otherwise than by the death of the Son of God» (Q40) | **LOCATED; вербатим Q12, Q15, Q20, Q21, Q37, Q40, Q44; прочие Q — только страницы** (LD 1–4, 8–14, 17–52 вне scope) | NO до item-level решения | LINK_ONLY |
| C07 | P-CONFESSION | Formula of Concord, Epitome XI (PD-печать Шаффа); Solid Declaration XI — отдельный пункт | для P6, не как наш канон; Schaff vol. III, с. 164–172 (Epitome XI), 9 (AC III) — [`15` §E.3](15_CALVIN_III24_AND_DORT_II_LOCATORS.md) | лютеранский universal call / «not willing that any should perish» / условие «know … and truly believe» | **LOCATED (Epitome XI); вербатим VIII, IX, XI, XII, XIII и AC III**; Solid Declaration XI — в Schaff III не напечатан; PD-локатор найден: Jacobs 1911 (archive.org `bookofconcordors0000ddhe`), SD XI на с. 649–664, вербатим XI.5/12/28/41/66/78/79/84 ([`15` §E.3a](15_CALVIN_III24_AND_DORT_II_LOCATORS.md)); визуальной сверки разворотов нет | NO до item-level решения | LINK_ONLY |

---

## C. Патристика и средневековье — PD

| ID | Tier | Source | URL | Supports | Status | Quote-safe | Custody |
|---|---|---|---|---|---|---|---|
| F01 | P-PATRISTIC | Athanasius, *On the Incarnation* | CCEL / New Advent | recapitulatio, смерть ради жизни | LEAD | NO | LINK_ONLY |
| F02 | P-PATRISTIC | Augustine on Rom 5 / John / predestination | New Advent | замещение / благодать; не делать его Owen | LEAD | NO | LINK_ONLY |
| F03 | P-PATRISTIC | Gregory of Nyssa / Gregory Nazianzen ransom notes | New Advent | выкуп; исторический фон «кому уплачено» | LEAD | NO | LINK_ONLY |
| F04 | P-REFORMED | Anselm, *Cur Deus Homo* | CCEL | satisfactio | LEAD / PD | NO until book/ch | LINK_ONLY |

---

## D. Реформация и пуритане — PD, часть уже на Drive

| ID | Tier | Source | URL / Drive | Supports | Status | Quote-safe | Custody |
|---|---|---|---|---|---|---|---|
| R01 | P-REFORMED | Calvin, *Institutes* II.12, II.16, II.17; III.24 | Drive 45 MB extract fail; Beveridge TXT: II.12 = 155; II.16 = 168; II.17 = 176–177; III.24.15–17 = 330–331 | природа/необходимость/merit; 1 Тим. 2:4 / 2 Пет. 3:9 | **LOCATED: CCEL TXT + печатная страница PD-скана Beveridge CTS 1845 vol. II — III.24.16 = с. 601–602, III.24.17 = с. 603–604** (исправлено 2026-10-11; «619–620» были листами). Drive PDF 45 MB — **не локатор**, только дубль текста (extraction cap, закрыто с доказательством). Item-level решение по Product принято только для III.24.16–17 | **ДА для III.24.16–17** по локатору «book.chapter.section + печатная страница»; остальные части Institutes — NO | copy + CCEL TXT + PD-скан |
| R02 | P-REFORMED | Calvin commentaries: Isa 53, John 3, 1 John 2, 1 Tim 2, Heb 2, 2 Pet | ~~CCEL `calcom45` reader login-wall~~ → **PD-скан найден 2026-10-08**: *Commentaries on the Catholic Epistles* (CTS, Edinburgh, 1855; пер. John Owen), IA `commentariesonca00calv`, `NOT_IN_COPYRIGHT`. **Локаторы: 1 Ин. 2:2 — с. 169 (стих) / 172 (начало разбора) / 173 (ключевой абзац); 2 Пет. 2:1 — с. 393; 2 Пет. 3:9 — с. 419–420.** Печатная страница = лист − 6 (три привязки колонтитулами + указатель тома). Реконструкция 2026-10-07 подтвердилась. CCEL `calcom45` по-прежнему пуст — не ретраить | extent texts | **research quote-safe с локатором** (было LEAD / wall); `PUBLICATION_HOLD` не снят | NO | LINK_ONLY |
| R02b | P-REFORMED | Calvin, *Commentaries on the Epistles to Timothy, Titus, and Philemon* (CTS, Edinburgh, **1856**) |
 IA `commentariesonep00calvuoft`, `NOT_IN_COPYRIGHT`, 430 листов |
 **1 Тим. 2:4–6 и Тит. 2:11** — локусы, которых в каноне не было |
 **PD-страницы найдены 2026-10-08**: 1 Тим. 2:4 — с. **54** (начало разбора) и **55** («classes of men, and not to individual persons»); 1 Тим. 2:5 — с. **56** («the fruit of the sacrifice… extends to all», обрыв OCR на сгибе); 1 Тим. 2:6 — с. **61** («that benefit which was universal and perpetual»); Тит. 2:11 — стих с. **316**, разбор с. **317**, сноска переводчика (Fr. Ser.) с. **317–318**. Смещение лист↔страница **ступенчатое** (листы 24–25, 36–37, 56–57, 74–75, 302–303, 368–371 без печатного номера): −4 / −10 / −16…−18. Привязки: 11 якорей, из них два по предметному указателю тома | extent texts; **Тит. 2:11 закрывает пробел сета карточек (H10)** | **research quote-safe с локатором**; `PUBLICATION_HOLD` не снят | NO | LINK_ONLY |
| R03 | P-REFORMED | Owen, *Works* (Goold) | Drive `1gfKY8eXGhV-HL5O4u1tVVcCRYNKx-dQY` | Death of Death обычно vol. 10 → **сверено: перепечатка Goold/Banner vol. X (1850)** | **LOCATED: PD-скан `worksofjohnowe185010owen`, лист − 16; 2 Пет. 2:1 — с. 362–363, 2 Пет. 3:9 — с. 348 и 543, «Proof 16» — с. 401** (2026-10-08/09). Drive PDF 42 MB — дубль, **не локатор** (extraction cap) | **ДА с локатором страницы**; `PUBLICATION_HOLD` не снят | copy |
| R04 | P-REFORMED | Owen, *Death of Death* standalone | CCEL TXT https://ccel.org/ccel/owen/deathofdeath/cache/deathofdeath.txt ; PDF/HTML те же URL; карта `14` | extent polemic | Book IV chunks 70–90 LOCATED (1 Tim 2:4 = 80–81; 2 Pet 2:1 = 87–88; Heb 10:29 = 88–89). **Четвёртая волна 2026-10-08 — страницы абзаца: 1 Тим. 2:6 — 307 и 371; Тит. 2:11 — 336 и 395** (Goold vol. X, лист − 16) | NO until Goold page → **страницы закрыты**, `PUBLICATION_HOLD` остаётся | LINK_ONLY + research map `14` |
| R05 | P-REFORMED | Goodwin, *Works* | Drive `1o9T7mIQxIH3ZB2EVc2hQsKdjEQM3SW-M` | Christ / redemption applied | ACQUIRED_COPY / locator unchecked | NO | copy |
| R06 | P-REFORMED | Turretin, *Institutio* (Latin PD; English P&R copyright) | Latin open; EN = RIGHTS_HOLD | elenctic loci on atonement | LEAD | Latin maybe; EN no | LINK_ONLY |
| R07 | P-REFORMED | Witsius, *Economy of the Covenants* | PD English 19c | covenant / suretyship | LEAD | NO | LINK_ONLY |
| R08 | P-REFORMED | John Gill, Body of Divinity VI.4 + *Cause* Part I | отдел `БИОГРАФИИ/Джон Гилл/` | universal texts | EXISTS in Gill corpus | YES where Gill dossiers already verbatim | do not duplicate |
| R09 | P-REFORMED | Charles Hodge, *Systematic Theology* III | CCEL | necessity/nature/extent | LEAD / PD | NO | LINK_ONLY |
| R10 | P-REFORMED | A.A. Hodge, *Outlines* / *Atonement* | PD | school of Princeton | LEAD | NO | LINK_ONLY |
| R11 | P-REFORMED | Dabney, *Syllabus* / *Theology* | PD | Southern Presbyterian | LEAD | NO | LINK_ONLY |
| R12 | P-REFORMED | W.G.T. Shedd, *Dogmatic Theology* | PD | penal substitution | LEAD | NO | LINK_ONLY |
| R13 | P-REFORMED | B.B. Warfield articles (d. 1921) | selected PD | plan of salvation; Calvin | LEAD | NO | LINK_ONLY |
| R14 | P-REFORMED | Jonathan Edwards, *Satisfaction of Christ* etc. | Yale/CCEL mix; rights item-level | | LEAD | NO | LINK_ONLY |
| R15 | P-REFORMED | Thomas Boston, *Fourfold State* / covenant of redemption | PD | surety | LEAD | NO | LINK_ONLY |

---

## E. Современные авторские — карточка, не пиратство

Полный PDF **не** класть. Покупка / библиотека / легальный eBook владельца.

| ID | Tier | Work | Why needed | Rights | Status | Quote-safe | Custody |
|---|---|---|---|---|---|---|---|
| M01 | MODERN-COPYRIGHT | John Murray, *Redemption Accomplished and Applied*, Eerdmans 1955; Banner 2014 ISBN 9781848714946; Eerdmans 2015 9780802873095 | педагогический хребет серии; necessity/nature/perfection/extent + ordo | in copyright | PRIVATE_STUDY RU HTML on Drive `02`; EN pages still missing | NO | PRIVATE_STUDY_ONLY |
| M21 | MODERN-COPYRIGHT | John Murray, *The Atonement* (P&R 1976 / Encyclopedia of Christianity) | конденсат RAA; §V Extent называет 2 Кор. 5; 1 Тим. 2:6; Евр. 2:9; 1 Ин. 2:2; 2 Пет. 2:1 только как purchase-lexeme | in copyright | публичная HTML https://www.the-highway.com/atonement_murray.html прочитана 2026-10-07; paraphrase only | NO | LINK_ONLY |
| M22 | MODERN-COPYRIGHT | Murray, «The Atonement and the Free Offer of the Gospel», *Collected Writings* 1:59–85 | definite atonement ↔ offer | in copyright | тела нет; Books at a Glance paywall | NO | LINK_ONLY |
| M23 | MODERN-COPYRIGHT | Murray, «The Atonement», CW 2:142–150 | короткий очерк | in copyright | тела нет | NO | LINK_ONLY |
| M24 | P-CONFESSION-adj | OPC, *The Free Offer of the Gospel* (Murray/Stonehouse/Kuschke majority, 1948) | B5: Иез. 18/33; Мф. 23:37; Ис. 45:22; 2 Пет. 3:9. Не extent. Minority Young/Hamilton на той же странице | церковный отчёт, публично | EN: https://opc.org/GA/free_offer.html прочитан целиком (чанки 0–7); полный EN-оригинал собран дословно и лежит на Drive `10.5`, id `1ZaZsYWWqA8HsdVdJMUAT52bGkFwyBPlP`, 56967 B, md5 `a9ccb9fb017e76ba2bb73a7f9aec9df6` (совпал с md5 Drive при заливке). RU-полный majority-доклад принят 2026-10-28 и прочитан целиком: Drive `10.5`, id `1DRgOqgLm27YPdw8ePlLixoawkaY22mDo`, 139776 B, md5 `527ac2739c26e2f3babae3ca571be6ef`; Minority в RU-файле нет; 1 Тим. 2:4 не разбирается вообще — карточка `19_` | paraphrase YES; не исповедание; RU — PRIVATE_STUDY (переводчик не указан) | LINK_ONLY |
| M25 | MODERN-COPYRIGHT | Murray, *The Epistle to the Romans* NICNT I (Eerdmans 1960) | Рим. 5:18 «все люди»; Рим. 8:32 | in copyright | страниц нет; вторичка p. 203 | NO | LINK_ONLY |
| M02 | MODERN-COPYRIGHT | J.I. Packer, Introductory Essay to Owen *Death of Death* (1959) | лучшее популярное объяснение, почему extent важен для евангелия | in copyright | CARD | NO | LINK_ONLY |
| M03 | MODERN-COPYRIGHT | David & Jonathan Gibson, eds., *From Heaven He Came and Sought Her* (Crossway 2013) | современная карта definite atonement, 21+ авторов | in copyright | CARD | NO | LINK_ONLY |
| M04 | MODERN-COPYRIGHT | Leon Morris, *The Apostolic Preaching of the Cross* | ἱλασμός, λύτρον, καταλλαγή | in copyright | CARD | NO | LINK_ONLY |
| M05 | MODERN-COPYRIGHT | John Stott, *The Cross of Christ* | nature, pastoral, propitiation | in copyright | CARD | NO | LINK_ONLY |
| M06 | MODERN-COPYRIGHT | Robert Letham, *The Work of Christ* | systematic loci | in copyright | CARD | NO | LINK_ONLY |
| M07 | MODERN-COPYRIGHT | Donald Macleod, *Christ Crucified* | nature | in copyright | CARD | NO | LINK_ONLY |
| M08 | MODERN-COPYRIGHT | Louis Berkhof, *Systematic Theology* | учебник; d. 1957, still treated as rights-hold | in copyright | CARD | NO | LINK_ONLY |
| M09 | MODERN-COPYRIGHT | Herman Bavinck, *Reformed Dogmatics* EN (Baker) | Dutch PD-ish; English trans copyright | EN rights-hold | CARD; Dutch later | NO | LINK_ONLY |
| M10 | MODERN-COPYRIGHT | Wayne Grudem, *Systematic Theology* | популярный учебник; не primary | in copyright | CARD | NO | LINK_ONLY |
| M11 | MODERN-COPYRIGHT | John Frame, *Salvation Belongs to the Lord* / ST | | in copyright | CARD | NO | LINK_ONLY |
| M12 | MODERN-COPYRIGHT | Thomas Schreiner essays / NT theology | extent texts, warning texts стык | in copyright | CARD | NO | LINK_ONLY |
| M13 | MODERN-COPYRIGHT | Michael Horton, *Lord and Servant* / ST | | in copyright | CARD | NO | LINK_ONLY |
| M14 | MODERN-COPYRIGHT | Bruce Demarest, *The Cross and Salvation* | ordo map | in copyright | CARD | NO | LINK_ONLY |
| M15 | MODERN-COPYRIGHT | I. Howard Marshall / Arminian-leaning NT | opposing case | in copyright | CARD | NO | LINK_ONLY |
| M16 | MODERN-COPYRIGHT | Grant Osborne / Witherington / Picirilli | opposing case | in copyright | CARD | NO | LINK_ONLY |
| M17 | MODERN-COPYRIGHT | Four Views on the Atonement / similar | pedagogy | in copyright | CARD | NO | LINK_ONLY |
| M18 | MODERN-COPYRIGHT | Oliver Crisp / Kevin Vanhoozer essays | nuance, not first wave | in copyright | CARD | NO | LINK_ONLY |
| M19 | MODERN-COPYRIGHT | J.C. Ryle, *Old Paths* / *Knots Untied* (частично PD depending on edition) | pastoral particular redemption + offer | check edition | LEAD | NO | LINK_ONLY |
| M20 | MODERN-COPYRIGHT | Spurgeon sermons on particular redemption + “Come” | many PD | PD sermons YES after locator | PD subset | YES with locator | LINK_ONLY / ingest later |

Покупка приоритет 1: **Murray RAA** (бумажная Banner/Eerdmans). Приоритет 2: Packer intro (часто в Banner Owen). Приоритет 3: Gibson & Gibson. Приоритет 4: Morris.

---

## F. Открытая академия / навигация

| ID | Tier | Source | URL | Notes | Quote-safe |
|---|---|---|---|---|---|
| O01 | SCHOLARLY-OPEN | CCEL Owen Death of Death | https://www.ccel.org/ccel/owen/deathofdeath | PD | after ingest |
| O02 | SCHOLARLY-OPEN | Archive.org Owen 1792 | https://archive.org/details/deathofdeathinde00owen | PD scan | after page |
| O03 | SECONDARY | Banner of Truth Murray product | https://banneroftruth.org/us/store/theology-books/redemption-accomplished-and-applied/ | TOC verified 2026-10-07 via public page | NO |
| O04 | SECONDARY | Gill corpus in this repo | `БИОГРАФИИ/Джон Гилл/27_…`, `12_CAUSE…`, `23_SECTION_LVII…`, `48_SOTERIOLOGY…` | не дублировать | follow Gill quote state |
| O05 | SECONDARY | Apostasy corpus | `apostasy/08_SOURCE_REGISTRY…`; `apostasy/12_2_PETER_2_CANONICAL_SUPPLEMENT_2026-09-30.md` | Heb 6/10 не решать заново; 2 Пет. 2:1 не решать системой искупления до экзегезы письма | follow apostasy |
| O06 | SECONDARY | Highway Murray *The Atonement* | https://www.the-highway.com/atonement_murray.html | copyright; paraphrase in `11` | NO |
| O07 | SCHOLARLY-OPEN | OPC Free Offer 1948 | https://opc.org/GA/free_offer.html | majority+minority; B5 | paraphrase of public church paper |
| O14 | LANE-REGISTRY | Реестр массы носителей позиции: `docs/research/atonement/35_four_point_authors_mass_registry.md` (203 строки, 13 эпох и слоёв + §20 круга 18, классы `A1`/`A2`/`B1`/`B2`/`C`, 119 адресатов очереди `Q-nn` по номерам строк) | — | источник новых кандидатов в эту очередь; по первичному изданию прочитано 14 % строк | NO, пока позиция в классе `C` |
| O15 | FINDING-AID | Указатель «For Whom Did Christ Die?» (`calvinandcalvinism.com`, `?page_id=7147`; разделы I–IV: 12 + 36 + 33 + 25 = 106 позиций; подстраницы кластеров: 1 Ин 2:2 — `?page_id=7309`) | — | сам указатель не цитируется как источник позиции: он даёт **адреса**, по которым ищется печать. Снято кругом 18: 6 страниц прочитаны с локатором, 13 из 16 частей оглавления — не прочитаны (FP-201, очередь Q-201). Права: транскрипты пользователя сайта, в корпус кладутся только выходные данные и наши страницы по изданию |

---

## G. Очередь Wave 2 (добыча PD — с 23.10.2026 в папку `10`, ранее `01` и `04`)

1. Ingest CCEL Owen *Death of Death* PDF/TXT в `01` с provenance card (source URL, access date, PD statement).
2. Anselm *Cur Deus Homo* (CCEL).
3. Athanasius *De Incarnatione*.
4. Hodge ST vol. 3 (CCEL).
5. Dort Head II отдельным документом: **Scott 1841 с. 282–286** (EN, скан + транскрипция; сейчас только OCR-фрагменты) **плюс** Schaff chunk 165 (латынь). Schaff EN-колонки не существует — проверено по чанкам 163–165, не искать её снова.
6. 1689 ch. 8 факсимиле/PD transcript.
7. Warfield “Atonement” / “Plan of Salvation” если PD.
8. Dabney loci.
9. Witsius relevant chapters.
10. Spurgeon PD sermons: particular redemption + gospel offer pair.
11. WCF ch. VIII: текст уже локализован (Schaff chunks 182–183). Следующий шаг по этой карточке — **печатная страница** тома Schaff (*Creeds of Christendom* III, издание 1919, PD на archive.org); в CCEL TXT пагинации нет.
12. Scott 1841 (`articlesofsynodo1841syno`): полная транскрипция с. 282–286 (артикулы II.1–9) и расписать по страницам Rejectio I–VII — сейчас закрыто только латынью Schaff 165.
13. ~~**Вопрос к владельцу:** перенос W0-пака в Git.~~ **Решено и сделано 2026-10-07 (вторая волна):** блоки первоисточника из `10_W0_PRIMARY_TEXT_DORT_HEAD_II_AND_CALVIN_2026-10-07.md` (Drive `01`, id `1hPs1aEWtwv1GHGHtZVtpWd8c91bQgAgo`, PD) перенесены в Git файлом [`16`](16_DORT_HEAD_II_ENGLISH_1840_PRIMARY_TEXT.md) — английский перевод Дорта II 1840 г. (арт. I–IX) и прочитанный фрагмент Кальвина на 1 Ин. 2:1–2. Служебная обвязка пакета (разделы верификации W0) в этот корпус не переносилась: она принадлежит другому корпусу. Drive-копия оставлена как есть.
14. Приоритет добычи задаёт реестр `35_` §17: сначала те `C`-строки, у которых текст уже открыт (Буньян — IA 24 с. / Chapel Library 30 с. плюс *The Baptist Quarterly* 21:3, сс. 126–130; Э. Б. Чейз и крещендобрический ролл — `middletownbiblechurch.org`; Сомюр — Aymon II 183 и 298, Swisser 1856, Niemeyer 729–739), потому что они закрывают сразу по несколько строк реестра. У круга 18 есть новый приоритет: шесть страниц указателя прочитаны **с печатным локатором** (Вермильи — *Predestination and Justification*, пер. Джеймса, назв. т. 8, сс. 16 и 62; Кимедонций — *The Redemption of Mankind*, London: Kingston, 1598, сс. 4–26 и кн. XI; Парей — *Certain learned and excellent discourses*, 1613, сс. 52–53; Твисс — *Doctrine of the Synod of Dort and Arles*, предисл. сс. 15–17, 3.1: 143–144, 3.2: 152, 3.3: 165; Уссер — *Whole Works* (Dublin: Hodges, Smith, 1864), т. 12, сс. 553–560 и 563–571; Хикман — *Patro-scholastico-dikaiösis* (Oxford: Lichfield, 1659), предисл.), и Буньян — *The Works* (Banner of Truth, 1991), т. 1: 334, 408–409, 416, 432, 526, 561–562. Эти строки поднимаются из `B1` в `A1` одним движением: снять титул и назвать лист.
15. Класс позиции поднимается (`C` → `B1`/`A2`/`A1`) только вместе с локатором по изданию и строкой очереди, снятой из `35_` §17: `C` без адресата и `A1` без страницы/колонки/параграфа — FAIL правила 23, то есть повышение класса «на глаз» технически невозможно.
16. Носитель, лежащий на Drive, проходит через индекс `ИСКУПЛЕНИЕ/data/atonement-library-index.json`: `rights`, `readState` по лестнице `unopened → pages_seen → locator_extracted → registry_linked` и `citedBy` на строки этого реестра. Пока позиция носителя `unopened`, она не имеет права ни на какую формулировку в статье — это исполняет правило 25 гейта, а не уговор. Очередь выше (п. 14) остаётся списком адресатов; её развёртка «что качать и куда» лежит в манифесте папки `10` на Drive, и оба списка обязаны сходиться номером `Q-nn`, иначе «поставлено в очередь» означает «забыто в двух местах».

Не качать и не класть: Murray, Packer 1959, Gibson 2013, Morris, Stott, Berkhof, Bavinck EN.

Если владелец покупает Murray — класть **только** в `02 — COPYRIGHT BIBLIOGRAPHY & ACQUISITION`, с пометкой `PRIVATE_STUDY_ONLY`. Публичные цитаты всё равно item-level.
| O08 | PRIMARY-TEXT | Editio Maior / BTC, Ioannis 11:47–11:56 | — | аппарат 11:52: варианты, влияющие на объём (`ἕν/ἓν`, `καί`); без него «разночтений нет» не утверждается | NO |
| O09 | PRIMARY-TEXT | LXX (Göttingen/Rahts): Иер 31:10; Иез 34:12; 37:21; Soph 3:19–20 | — | точная формула «рассеял — соберу» для `nt/15_` §2.3 | NO |
| O10 | PATRISTIC | Иоанн Златоуст, In Ioannem, homilia на 11:45–54 | — | древнее чтение «диаспора vs язычники»; у Кальвина на 12:32 процитирован, но место не снято | NO |
| O11 | PATRISTIC | Кирилл Александрийский, In Ioannem (кн. на 11:49–53) | — | «чада по предведению» vs «чада по обóжению» | NO |
| O12 | PATRISTIC | Августин, In Ioannis evangelium tractatus (на 11:45–57) | — | `multi in grege, non omnes`; владение текстом необходимо перед цитатами в полемике | NO |
| O13 | SECONDARY | Страницы изданий: Кальвин (Pringle 1840) на 11:52 и 12:32; Гилл; Алфорд; Бенгель; Уэсли; сверка атрибуции «только диаспора» (Jamieson-Fausset-Brown?) | StudyLight, BibleHub (перепечатки) | перевод `LOCATOR_PARTIAL`-записей `nt/15_` §5 и `13_` §2.5 в `LOCATOR_FULL` | NO |

## N. Тематическая библиотека и очередь чтения всей серии — 2026-11-06

Это расширение существующего реестра, а не второй источник статусов. Новые ID `SYS`, `MON`, `ART` не совпадают с локальными `S01…` НЗ/ВЗ. Задача — пройти связанные разделы систематического богословия и специальные споры, не ограничивая серию опровержением одного автора. Перечень приоритетный и расширяемый; «все систематики уже изучены» по нему заявлять нельзя.

**Обозначения чтения:** `КОНТЕКСТ` — собственные перечисленные места реально прочитаны, иногда в прежних волнах; `МЕТАДАННЫЕ` — проверена издательская/институциональная запись, не сама книга; `ФРАГМЕНТ` — получен разрешённый отрывок, точная область чтения названа; `ОЧЕРЕДЬ` — библиографический ориентир, релевантная редакция и полный раздел ещё должны быть получены. Для ОЧЕРЕДИ не утверждаются точные страницы и содержание непрочитанной главы. Статус источника в машинном контроле, право публикации и степень согласия с выводом остаются отдельными вопросами.

### N.1. Систематические и догматические труды

Для каждой систематики проверяется связка: учение о Боге и Троице → замысел → Лицо и священство Христа → природа/объём жертвы → союз со Христом → призыв/вера → оправдание → сохранение. Если цитата из главы об оправдании используется как ответ об объёме, нужно прочитать обе главы и переход между ними.

| ID | Автор и труд | Для чего нужен в серии | Фактическое чтение / следующий объект |
|---|---|---|---|
| SYS-01 | Кальвин, *Institutes*, собственные библейские комментарии | Человеческая природа, жертва, применение, избрание; развитие языка | КОНТЕКСТ II.12.1–4, II.16/17, IV.14.7, III.24 и названные комментарии; дополнить полные связанные главы и латинский контроль спорных мест |
| SYS-02 | Уильям Эймс, *The Marrow of Theology* | Ранняя реформатская система: посредник, выкуп, применение | ОЧЕРЕДЬ: выбрать проверяемую латинскую/английскую редакцию и все тематические главы |
| SYS-03 | Франциск Турретин, *Institutes of Elenctic Theology* | Удовлетворение, особое приобретение, вера и повторное взыскание | КОНТЕКСТ выбранных вопросов и страниц, зарегистрированных P05; пройти целый релевантный вопрос с objections/replies, не только заключение |
| SYS-04 | Герман Витсий, *The Economy of the Covenants* | Завет искупления, условия, impetration/application, вера | ОЧЕРЕДЬ полных разделов II–III по указанным темам; не выдавать наличие тома за чтение |
| SYS-05 | Иоганн Генрих Хайдеггер / Генрих Хеппе, догматические компендии | Собственные XVII-вековые утверждения и поздняя антология — разные источники | ОЧЕРЕДЬ: точные редакции; Хеппе использовать как указатель к цитируемым оригиналам |
| SYS-06 | Чарльз Ходж, *Systematic Theology* | Уголовное/денежное удовлетворение, результат, общий плод, вера | КОНТЕКСТ специальных мест P05; затем полные связанные разделы томов II–III |
| SYS-07 | А. А. Ходж, *Outlines of Theology* | Особое приобретение и применение при общих последствиях | КОНТЕКСТ собственных определённых мест; сверить все ответы релевантной главы, а не только цитату Прокопенко |
| SYS-08 | Роберт Л. Дабни, *Systematic Theology* | Критика популярного double payment при особом намерении | КОНТЕКСТ Extent и соседнего рассуждения; дополнить главы о воле, призыве и вере |
| SYS-09 | Уильям Г. Т. Шедд, *Dogmatic Theology* | Atonement/redemption, завет и отсроченное применение | КОНТЕКСТ/изображения выбранных страниц; исходный двухтомник и редакция Gomes 2003 не подменяют друг друга |
| SYS-10 | Огастас Х. Стронг, *Systematic Theology* (1907) | Реальная широкая баптистская система, вера и неевангелизированные | КОНТЕКСТ: весь Extent, section E, и избранные части Intercession; остальная система не объявлена прочитанной |
| SYS-11 | Герман Бавинк, *Reformed Dogmatics*, III, *Sin and Salvation in Christ*; IV | Христово дело и применение в органической системе | МЕТАДАННЫЕ английского III, Baker Academic 2006 / перевод John Vriend, ред. John Bolt; получить связанные главы III–IV; это не издание Eerdmans |
| SYS-12 | Герхардус Вос, *Reformed Dogmatics* | Завет, христология, сотериология и действие Духа | ОЧЕРЕДЬ: точное английское издание и релевантные вопросы, не только ответы об объёме |
| SYS-13 | Луис Беркхоф, *Systematic Theology* | Особая цель, общие блага, применение; собственная позиция и Marrow-men | КОНТЕКСТ отдельных мест прежних волн; проверить весь раздел объёма и соседние главы |
| SYS-14 | Роберт Л. Реймонд, *A New Systematic Theology of the Christian Faith* | Современный строгий синтез и толкование спорных мест | ОЧЕРЕДЬ релевантных глав; редакцию и страницы установить по объекту |
| SYS-15 | Джон Фрейм, *Systematic Theology* | Божья воля, замысел, природа и применение спасения | ОЧЕРЕДЬ тематических глав; не заменять более кратким *Salvation Belongs to the Lord* без указания |
| SYS-16 | Майкл Хортон, *The Christian Faith* | Завет, союз, представительство и достаточность | МЕТАДАННЫЕ официального издания Zondervan 2011; книга ещё не прочитана целиком или тематически |
| SYS-17 | Роберт Летэм, *Systematic Theology* | Троица, священство, союз и особое искупление | ОЧЕРЕДЬ полных тематических разделов; отдельно проверить его специальный *The Work of Christ* |
| SYS-18 | Джоэл Бики / Пол Смолли, *Reformed Systematic Theology*, тома II–III | Классическая линия с современной библиографией и практикой | МЕТАДАННЫЕ набора Crossway 2024, 4 тома/5216 с.; дата набора не присваивается каждому тому; тематические главы ещё получить |
| SYS-19 | Бики / Смолли, *Essentials of Reformed Systematic Theology* | Новая компактная контрольная систематика | МЕТАДАННЫЕ Crossway, 04.11.2025, 1088 с., ISBN 9781433590917. TOC: 47–49, 51, 55, 58–59; preview получен, эти главы в нём не объявлены прочитанными |
| SYS-20 | Уэйн Грудем, *Systematic Theology*, 2-е изд. | Сопоставить исходную цитату, обновлённый ответ, время/неизменность Бога | МЕТАДАННЫЕ Zondervan, 08.12.2020, 1616 с., ISBN 9780310517979; старый русский 2004 — отдельный объект; нужны глава об искуплении и связанные главы |
| SYS-21 | Стивен Уэллум, *Systematic Theology* и тематические труды | Христология, священство и новый завет | ОЧЕРЕДЬ: состав опубликованных томов/редакций проверить; не приписывать отсутствующему тому содержание сотериологии |
| SYS-22 | Мак-Артур / Мейхью, *Biblical Doctrine* (2017) | Строгий современный синтез и проверка точных книжных цитат | ОЧЕРЕДЬ оригинального релевантного раздела, включая 558; собственная проповедь проверена отдельно и не закрывает книжную колляцию |
| SYS-23 | Гордон Льюис / Брюс Демарест, *Integrative Theology* | Исторический обзор, типы теорий, декреты и объём | ОЧЕРЕДЬ всех используемых в статье параграфов вместе с их собственным решением; цитируемые ими первоисточники учитывать отдельно |
| SYS-24 | Миллард Эриксон, *Christian Theology* | Широкий евангельский контроль, терминология лапсарианства | ОЧЕРЕДЬ точной редакции/английского и цитируемого русского мест; не смешивать издания |
| SYS-25 | Льюис Сперри Чейфер, *Systematic Theology* | Диспенсациональная широкая система, представительство и приложение | ОЧЕРЕДЬ полного тематического комплекса, включая веру и избрание |
| SYS-26 | Чарльз Райри, *Basic Theology* | Собственное значение «умеренного кальвинизма» | ОЧЕРЕДЬ разделов об искуплении, избрании и обращении в точной редакции |
| SYS-27 | Генри Тиссен / Вернон Дёрксен, *Lectures in Systematic Theology* | Сравнить раннюю/пересмотренную модель и порядок решений | ОЧЕРЕДЬ двух самостоятельных изданий; дата 1949 не означает тождество редакции 1979 |
| SYS-28 | Якоб Арминий, *Works* | Условность избрания/применения и всеобщее искупление в собственных тезисах | ОЧЕРЕДЬ Declaration of Sentiments и полных диспутаций по Христу/спасению; поздние арминиане не заменяют автора |
| SYS-29 | Ричард Уотсон / Уильям Бёрт Поуп, богословские системы | Классическая уэслианская связь общего искупления и предваряющей благодати | ОЧЕРЕДЬ отдельных тематических глав каждого автора; не объединять разные системы в один голос |
| SYS-30 | Джон Майли, *Systematic Theology* | Правительственная модель, наказание и универсальное условие | ОЧЕРЕДЬ полного релевантного аргумента; название «арминианин» не устанавливает природу заместительства |
| SYS-31 | Франц Пипер, *Christian Dogmatics*; Дж. Теодор Мюллер, *Christian Dogmatics* | Конфессионально-лютеранский контроль: всеобщая жертва, благодать и вера | ОЧЕРЕДЬ собственных разделов и Lutheran Confessions; не путать автора Дж. Т. Мюллера с историком Ричардом А. Мюллером |
| SYS-32 | Томас Оден, *Systematic Theology* | Классическая экуменическая/уэслианская проверка природы и результата | ОЧЕРЕДЬ выбранной редакции христологического и сотериологического томов |
| SYS-33 | Фома Аквинский, *Summa Theologiae* III, qq. 46–49 и связанные loci | Удовлетворение, заслуга, жертва, достаточность и сообщение результата | ОЧЕРЕДЬ полных вопросов с возражениями и ответами; поздний слоган sufficient/efficient не заменяет автора |
| SYS-34 | Карл Барт, *Church Dogmatics* IV; Т. Ф. Торранс, *Atonement* | Заместительство, избрание, участие и универсалистское следствие | ОЧЕРЕДЬ собственных полных релевантных разделов; сравнивать самостоятельные модели, не общий ярлык |

| SYS-35 | Буллингер, *Decades*; Мускул, *Loci communes*; Пётр Мартир Вермигли, *Loci communes*; Джироламо Дзанки, догматические/исповедальные труды | Проверить раннее реформатство вне одной линии Кальвин → Оуэн: природа, достоинство и назначение жертвы | ОЧЕРЕДЬ оригинальных тематических мест каждого автора. Для посмертных компиляций установить исходный авторский фрагмент и редакционный слой; учение не выводится из общего названия |
| SYS-36 | Захария Урсин, комментарий к Гейдельбергскому катехизису | Вопрос 37 о страданиях/гневе и связанные вопросы о вере, принадлежности Христу и получении благ | ОЧЕРЕДЬ полного контекста и точной редакции. Установить происхождение каждого решающего фрагмента; пересказ самого катехизиса не равен комментариям его толкователя |
| SYS-37 | Аманд Полан, *Syntagma theologiae christianae* | Контроль ранней систематической архитектуры: декрет, Христово дело, получение и условия | ОЧЕРЕДЬ точного оригинала и связанных разделов. Библиографический поиск вывел каталог PRDL и научные указатели; это не чтение труда |
| SYS-38 | Петрус ван Мастрихт, *Theoretical-Practical Theology* | Континентальная схоластическая/практическая связь приобретения и применения; сопоставить латинский оригинал и новый перевод | ОЧЕРЕДЬ. Найдена издательская поисковая запись набора/томов, извлечение страниц заблокировано; состав нужного тома и точные страницы ещё установить |
| SYS-39 | Вильгельмус а Бракел, *The Christian’s Reasonable Service* | Нидерландская реформатская связь завета, посредничества, веры и пастырского применения | ОЧЕРЕДЬ. Издательская поисковая запись четырёхтомника найдена; сама страница/книга не получены. Нужны полные главы о завете, искуплении и вере |

Ранний континентальный контроль SYS-35–39 нужен прежде итогового тезиса о том, чему «первоначально учили реформаторы»: несколько общих формул Кальвина и несколько поздних строгих цитат не образуют сопоставимого исторического корпуса. Эти добавленные группы требуют чтения собственных оригиналов; поисковые указатели не удостоверяют ещё их доктрину.

Проверяемые издательские сведения: [Grudem](https://zondervanacademic.com/products/systematic-theology-second-edition), [Horton](https://zondervanacademic.com/products/the-christian-faith), [Beeke–Smalley, набор](https://www.crossway.org/books/reformed-systematic-theology-series-hcj/), [Essentials 2025](https://www.crossway.org/press-room/essentials-of-reformed-systematic-theology-hcj/). Это первичные сведения об изданиях, без переноса рекламных оценок на богословский вердикт.

### N.2. Специальные книги: строгая и широкая реформатская линия

| ID | Книга / автор | Вопрос и нужный объект | Состояние и ближайший шаг |
|---|---|---|---|
| MON-01 | Джон Оуэн, *The Death of Death in the Death of Christ* (1647) | Не только трилемма: цель, священство, вера, весь Book IV | КОНТЕКСТ конкретных прежних мест, II.4 и полный релевантный IV.5 по Евр. 10:29; полный том не объявлен прочитанным |
| MON-02 | Оуэн, *Exposition of Hebrews*, Works XXIII, с. 543–548; полученный титул 1855 | Сопоставить позднее Христово освящение с ранним набором ответов | ОРИГИНАЛ ПОЛУЧЕН: OCR тома, XML, титул и 6 страниц визуально прочитаны; внешний вариант сохранён, Христов предпочитается. Издание 1854 отдельно не коллировано; весь том не прочитан |
| MON-03 | Джон Девенант, *Dissertation on the Death of Christ*; латинские *Dissertationes duae* | Условное универсальное и особое приобретение веры, точное значение impetration | КОНТЕКСТ зарегистрированных страниц/сканов; расширить на весь тематический довод, проверить перевод латинского термина |
| MON-04 | Майкл Линч, новый перевод Девенанта (2024) | Сверка старого перевода и современного комментария | МЕТАДАННЫЕ прежней волны; получить весь собственный текст и отделить редакторское введение |
| MON-05 | Ашшер, Works XII, *True Intent and Extent* и ответ | Всеобщее удовлетворение, вера и двойное взыскание | КОНТЕКСТ: 553–560, 563–570 прочитаны; избранные сканы сверены. Целый том не прочитан |
| MON-06 | Амиро, *Brief Traitté de la predestination* (1634), последующие уточнения | Порядок декретов, две милости, приобретение условия, неевангелизированные | ОЧЕРЕДЬ законного французского оригинала; Djaballah/Muller не заменяют полного оригинала |
| MON-07 | Ричард Бакстер, *Catholik Theologie* (1675) и специальные ответы | Условное правовое установление и особое исполнение условия | ОЧЕРЕДЬ: заблокированный ранее доступ не выдаётся за полученный текст; выбрать открытый/библиотечный экземпляр |
| MON-08 | Джон Хоу / Эдмунд Калами / Эдвард Полхилл | Английские широкие модели и связь с исповедальными дискуссиями | ОЧЕРЕДЬ точных собственных произведений и протоколов; сначала установить объекты, а не приписать им одну коллективную книгу |
| MON-09 | А. А. Ходж, *The Atonement* | Юридическая природа, завет и приобретённый результат | КОНТЕКСТ отдельных зарегистрированных мест; прочитать полный релевантный раздел и ответ широкому оппоненту |
| MON-10 | Уильям Каннингем, *Historical Theology* | История удовлетворения и объёма | ОЧЕРЕДЬ релевантных глав с цитируемыми собственными авторами |
| MON-11 | Джон Мюррей, *Redemption Accomplished and Applied* (1955) | Основная связка приобретения/применения; природа и необходимость | Полный русский объект ранее получен и разобран по карте; английское пагинированное издание и все спорные цитаты не заменены русским дампом |
| MON-12 | Мюррей, *The Atonement*; Murray/Stonehouse, *The Free Offer of the Gospel* | Краткий extent и особый спор об открытом призыве | КОНТЕКСТ прежних волн; majority/minority ответ OPC — не одно исповедальное определение |
| MON-13 | Дэвид / Джонатан Гибсон (ред.), *From Heaven He Came and Sought Her* (2013) | 23 главы: история, экзегеза, система, пастырство; Williams 17–18 и Wellum 19 особенно | ФРАГМЕНТ: полный TOC и выбранное введение 33–36 прочитаны; нужные 461–516/517+ и весь том не получены |
| MON-14 | Населли / Сноубергер (ред.), *Perspectives on the Extent of the Atonement: 3 Views* (2015) | Trueman / Osborne–McCall / Hammett, каждый основной текст и каждый ответ | МЕТАДАННЫЕ/TOC издателя: 256 с., ISBN 9781433669712; полная книга нужна, а не три кратких описания |
| MON-15 | Адам Дж. Джонсон (ред.), *Five Views on the Extent of the Atonement* (2019) | Horton, Sanders, Levering, Louth, Greggs: традиции и пределы итогового охвата | МЕТАДАННЫЕ официального издателя, 02.07.2019, 256 с., ISBN 9780310527718; книга не прочитана |
| MON-16 | Гэри Л. Шульц, *A Multi-Intentioned View of the Extent of the Atonement*; диссертация 2008 | Полное особое приобретение и всеобщее обеспечение | КОНТЕКСТ диссертации 155, сн.195, 250–255 прежних волн; книга и диссертация — разные редакции; получить оставшиеся релевантные главы |
| MON-17 | Брюс Уэр, полные лекции и глава в *Whomever He Wills* | Несколько целей, всеобщая уплата, действенный призыв | КОНТЕКСТ собственной лекции; точный книжный раздел/ответ строгому оппоненту ещё получить |
| MON-18 | Дэвид Аллен, *The Extent of the Atonement* (2016) | Большой исторический/критический корпус широкого удовлетворения | ОЧЕРЕДЬ тематических глав и всех решающих цитат; рецензия Шрока — отдельный источник |
| MON-19 | Аллен, *The Atonement: A Biblical, Theological, and Historical Study of the Cross of Christ* | Широкая положительная система, не только критика строгих авторов | ОЧЕРЕДЬ: редакцию/оригинал подтвердить и сопоставить с более ранним трудом |
| MON-20 | Майкл Риккарди, *To Save Sinners: A Critical Evaluation of the Multiple Intentions View of the Atonement* | Современный строгий ответ именно multiple intentions | МЕТАДАННЫЕ Wipf & Stock, 12.04.2023, 402 с., ISBN 9781666746105; endorsement не заменяет чтение аргумента |
| MON-21 | Майкл Ф. Бёрд / Скотт Харроуэр (ред.), *Unlimited Atonement* (2023) | Недавний широкий реформатский ответ и глава о Боге | Книга не получена; полный review Cheek 2025 и учебный Chidester 2025 — самостоятельные источники |
| MON-22 | Майкл Дж. Линч, *John Davenant’s Hypothetical Universalism* (2021) | История английского HU, Дорт и лютеранский фон | МЕТАДАННЫЕ/прежние selected contexts; полный монографический аргумент ещё не прочитан |
| MON-23 | Ричард Снодди, *The Soteriology of James Ussher* (2014) | Вера, приобретение, акт и объект у Ашшера | ОЧЕРЕДЬ полной релевантной части; собственные письма Ашшера проверены независимо |
| MON-24 | Джонатан Д. Мур, *English Hypothetical Universalism* (2007) | Preston и английская история; отличие от Сомюра | ОЧЕРЕДЬ, включая собственные цитируемые первичные тексты; не все англичане одного типа |
| MON-25 | Брайан Армстронг, *Calvinism and the Amyraut Heresy* (1969) | Классическая историческая гипотеза об ортодоксии и Сомюре | ОЧЕРЕДЬ с ответами Muller/van Stam/других; библиографический ориентир подтверждён у Muller, не чтение книги |
| MON-26 | Ф. П. ван Стам, *The Controversy over the Theology of Saumur, 1635–1650* (1988) | Французские споры и реальные решения | ОЧЕРЕДЬ по ссылкам Muller; получить полные исходные документы спорных эпизодов |
| MON-27 | Ричард А. Мюллер, *Calvin and the Reformed Tradition* | Неоднородность раннего реформатства, терминология и порядок спасения | ОЧЕРЕДЬ полных нужных глав; статья 2009 прочитана отдельно и не равна книге |
| MON-28 | Пол Хартог, *Calvin on the Death of Christ: A Word for the World* (2023) | Новая широкая интерпретация Кальвина | Библиографический ориентир в собственной статье Hartog 2024; книгу получить и сравнить с ограничительными локусами |
| MON-29 | Алан Клиффорд, *Atonement and Justification*; *Calvinus*; *Amyraut Affirmed* | Широкая историческая линия и спор о методе | ОЧЕРЕДЬ точных редакций; Muller 2009 даёт библиографические указатели, не независимое чтение книг |
| MON-30 | Джонатан Рейнбоу, *The Will of God and the Cross* | Строгая историческая интерпретация Кальвина | ОЧЕРЕДЬ собственного аргумента и ответов; не выбирать только одну историческую монографию |
| MON-31 | Норман Даути, *The Death of Christ* (переработанное 1978) | Классический широкий критик и конкретные тексты | ОЧЕРЕДЬ полного тематического содержания; цитаты Прокопенко не заменяют оригинала |
| MON-32 | Джеймс Уайт, *The Potter’s Freedom*; полемические ответы | Строгая критика широкого обеспечения, дар веры и предупреждения | ОЧЕРЕДЬ точной книжной редакции/разделов; выбранная собственная статья 2003 учтена отдельно |

Основные легальные точки получения: [Gibsons, издательский фрагмент](https://g.christianbook.com/ns/pdf/sample/512761.pdf), [B&H, три позиции и TOC](https://www.bhpublishinggroup.com/products/perspectives-on-the-extent-of-the-atonement/), [Zondervan, пять позиций](https://zondervanacademic.com/products/five-views-on-the-extent-of-the-atonement), [Riccardi, точный подзаголовок и издание](https://wipfandstock.com/products/to-save-sinners-9781666746105). Главы ответов в сравнительных сборниках входят в задание чтения наравне с основными главами.

### N.3. Природа искупления, библейский фон и философская проверка

| ID | Труд | Цель | Статус / следующий шаг |
|---|---|---|---|
| MON-33 | Ансельм, *Cur Deus Homo* | Необходимость, удовлетворение и вопрос, чем отличается от уголовного заместительства | ОЧЕРЕДЬ полного диалога с возражениями Бозона; не только знаменитый вывод |
| MON-34 | Густаф Аулен, *Christus Victor* | Проверить историческую трёхчленную типологию и мотив победы | ОЧЕРЕДЬ собственного текста вместе с современной исторической критикой |
| MON-35 | Леон Моррис, *The Apostolic Preaching of the Cross*; *The Atonement* | Лексика выкупа/умилостивления/крови и цельная библейская картина | ОЧЕРЕДЬ конкретных полных глав; два труда не считать одним |
| MON-36 | Джон Стотт, *The Cross of Christ* | Положительная библейско-пастырская связь удовлетворения, заместительства и жизни | МЕТАДАННЫЕ centennial edition IVP 2021, 384 с., ISBN 9780830839100; тематические главы ещё прочитать |
| MON-37 | Стив Джеффри / Майкл Ови / Эндрю Сак, *Pierced for Our Transgressions* | Современная защита уголовного заместительства, исторические цитаты и ответы | ОЧЕРЕДЬ обеих частей и собственных первичных цитат; не только подборки сторонников |
| MON-38 | Джеймс Бейлби / Пол Эдди (ред.), *The Nature of the Atonement: Four Views* | Boyd / Schreiner / Reichenbach / Green — природа, не четыре объёма | МЕТАДАННЫЕ IVP 09.10.2006, 208 с., ISBN 9780830825707; нужны главы и взаимные ответы |
| MON-39 | Уильям Лейн Крейг, *Atonement and the Death of Christ* (2020) | Уголовное представительство, прощение, оправдание, философия права | МЕТАДАННЫЕ Baylor 15.06.2020, 328 с., ISBN 9781481312042; TOC проверен, главы 9–13 ещё получить |
| MON-40 | Оливер Крисп, *Participation and Atonement* (2022) | Реалистическое участие и удовлетворение, критика уголовного переноса | Полная рецензия Witt 2024 прочитана; собственная книга не получена и не заменена её пересказом |
| MON-41 | Крисп, *Deviant Calvinism*; *The Word Enfleshed* | Границы реформатского богословия, воплощение и гипотетический универсализм | ОЧЕРЕДЬ отдельных собственных глав/точных редакций; личная система не определяется одним заглавием |
| MON-42 | Джошуа Макнолл, *The Mosaic of Atonement* | Современное соединение разных библейских мотивов | ОЧЕРЕДЬ; сопоставить положительные связи, не только объявление «многогранности» |
| MON-43 | Адам Дж. Джонсон, *Atonement: A Guide for the Perplexed* и специальные эссе | Методы чтения теорий и соотношение единого дела/моделей | ОЧЕРЕДЬ выбранного собственного текста; редакторская роль в MON-15 — другой объект |
| MON-44 | Томас Макколл, *Forsaken*; Джерри Уоллс / Джозеф Донжелл, *Why I Am Not a Calvinist* | Троица, покинутость и сильные некальвинистские возражения | ОЧЕРЕДЬ полных релевантных частей каждого труда; не приписывать одну общую модель |
| MON-45 | Томас Шрайнер / Ардель Кэнедей, *The Race Set Before Us*; противоположные толкования предупреждений | Сохранение через предупреждения, реальные блага и окончательная утрата | ОЧЕРЕДЬ соответствующих полных разделов и самостоятельных ответов оппонентов |
| MON-46 | Roy Gane / Jacob Milgrom / David Moffitt, специальные труды о Левите и Евреям | Реальное культовое очищение, кровь, воскресение и священство | ОЧЕРЕДЬ: выбрать точные тематические книги/главы; никакой из них не считается автоматически согласной со строгим объёмом |

[IVP о четырёх моделях природы](https://www.ivpress.com/the-nature-of-the-atonement), [Baylor: Craig и полное оглавление](https://www.baylorpress.com/9781481312042/atonement-and-the-death-of-christ/), [IVP: Stott, издание 2021](https://www.ivpress.com/the-cross-of-christ). Эти новые первичные метаданные ограничены сведениями об издании. Рецензия на книгу — собственный аргумент рецензента и вторичный источник по книге.

### N.4. Статьи, реальные ответы и новые исследования

| ID | Объект | Что реально получено/прочитано | Значение и следующая проверка |
|---|---|---|---|
| ART-01 | R. A. Muller, *A Tale of Two Wills? Calvin and Amyraut on Ezekiel 18:23*, CTJ 44 (2009), 211–225 | Полный основной текст и примечания | Заключение не отдаёт общий спор одной стороне; получить французские оригиналы цитируемых мест Амиро |
| ART-02 | Andrew David Naselli, *John Owen’s Argument for Definite Atonement*, SBJT 14.4 (2010), 60–82 | Весь извлечённый объект получен; прочитаны введение и определённые контексты приобретения веры | Остальной текст прочитать; привести его собственные оценки, не только резюме Оуэна |
| ART-03 | Paul Hartog, *A Legacy Lost to the Reformed Imagination*, Religions 15.2 (2024), 228 | Полный объект получен; введение, вывод и определённые примечания прочитаны | §§2–6 ещё прочитать; затем сопоставить собственные лютеранские исповедания/Лютера, а не только вывод историка |
| ART-04 | Nicholas T. Batzig, *Hebrews 10:29: A Test Case in Reformed Hermeneutics* (2024) | Полный авторский текст | Реальный внутристоронний спор; его ссылки на Edwards/Owen ведут к нужным оригиналам |
| ART-05 | Peter J. Leithart, *Trampling Blood* (2013) | Полный основной авторский текст, реклама исключена | Сопоставлен с собственным ранним Owen IV.5; «внешнее» не значит «нереальное» |
| ART-06 | Arminian Perspectives, *Who Is Sanctified in Hebrews 10:29?* (2008) | Весь основной авторский текст, комментарии читателей исключены | Реальный ответ White/Owen; сильная синтаксическая критика и собственные слабые переходы выделены |
| ART-07 | James White, *Hebrews and the Atonement of Christ* (обновление 2003) | Выбранные собственные контексты Евр. 10 и полемики с Sungenis | Не выдавать за всю книгу или прямой ответ Прокопенко; сверить оригинал позднего Owen |
| ART-08 | William G. Witt, review Oliver Crisp, JAT 12 (2024), 733–737 | Полный пятистраничный PDF получен, весь основной текст прочитан | Различить его критику механизма и позицию книги, которую отдельно ещё получить |
| ART-09 | Lee Gatiss, review Lynch, JTS 75.2 (2024), 530–532 | Только библиографическая страница; текст заблокирован | Доступный библиотечный экземпляр; никакой аргумент рецензии не считается прочитанным |
| ART-10 | R. T. Mullins, *The Doctrine of God and Unlimited Atonement* (2023) | Официальная запись Helsinki прочитана; открытый AAM не удалось получить | Приоритет Бога/времени: получить законный текст главы; дата загрузки 2024 не меняет дату книги 2023 |
| ART-11 | Jonathan M. Cheek, review Bird/Harrower, JBTW 6.1 (2025), 94–99 | Прежняя волна: все шесть страниц PDF визуально прочитаны | Реальная недавняя строгая рецензия; изучить саму книгу и ответ её авторов, если опубликован |
| ART-12 | Chidester, учебная работа CH630 (27.05.2025) | Прежняя волна: основной текст 1–13 и библиография 14 прочитаны | Это учебная работа, не докторская диссертация/журнальная рецензия; cited originals отдельно |
| ART-13 | Allen, серия ответов *From Heaven*; Schrock, рецензия на Allen | Определённые собственные материалы прежних волн, не все части | Составить точную пару тезис → ответ → возражение; веб-дата загрузки не всегда дата создания |
| ART-14 | Kenneth Stewart (2008), Greaves (1965), Helm (1979), Rouwendal (2008), Nicole, Gatiss и исследования рецепции | Stewart/Helm прочитаны; Greaves основной 126–131 без продолжения примечаний на 125; остальные по собственным старым записям/очереди | Закрывать каждый исторический спор его собственным первичным объектом; один список имён не закрывает историю |

Новые доступные оригиналы: [Muller](https://www.calvin.edu/library/database/crcpi/fulltext/ctj/2009-442-211.pdf), [Naselli](https://cf.sbts.edu/equip/uploads/2015/10/SBJT-V14-N4_Naselli.pdf), [Hartog](https://www.mdpi.com/2077-1444/15/2/228), [Witt](https://jat-ojs-baylor.tdl.org/jat/article/download/626/669/1713). Недоступность полного [Gatiss](https://academic.oup.com/jts/article-abstract/75/2/530/7736936) и [Mullins](https://researchportal.helsinki.fi/en/publications/the-doctrine-of-god-and-unlimited-atonement) сохранена как конкретный предел, без пересказа непрочитанного.

### N.5. Очерёдность приобретения оригиналов и извлечения аргументов

**Первый пакет:** MON-13 главы Williams/Wellum; MON-14 все три позиции и ответы; MON-16 полный тематический Shultz; MON-20 Riccardi; MON-21 Bird/Harrower, включая ART-10. Эта группа максимально близка к существующему спору о нескольких намерениях и приобретении веры. Одновременно нужны поздний Owen и полные комментарии к Евр. 10/2 Пет. 2/1 Ин. 2. Следующий пакет — Lynch/Moore/Snoddy и французские оригиналы Амиро; затем историческая и межтрадиционная широта MON-15/ART-03 и собственные лютеранские источники.

**Базовая систематическая линия для первых статей:** SYS-01, 03, 06, 08, 09, 11, 13 и MON-11; современные проверки SYS-16, 18–20, 22–24; независимый широкий контроль SYS-28–31. Переход к следующему автору определяется вопросом, а не необходимостью собрать ещё десять названий. Ссылки каждого нового автора отслеживаются в обе стороны: предшествующий первоисточник и содержательный критик/ответ.

Для каждой прочитанной единицы фиксируются автор, название/редакция, язык, страница или точный раздел, полный контекст, тезис, собственные посылки, встречный довод, ответ и оставшаяся трудность. Прямая атрибуция, пересказ и наша реконструкция маркируются отдельно. Публичная серия получает связный вывод со ссылками; служебные детали хранения остаются в исследовательском контроле.

Проверка доступной подключённой библиотеки не обнаружила по точным использованным запросам новых полных экземпляров основных искомых современных монографий; это результат ограниченного поиска, а не утверждение об отсутствии книг во всём Drive или библиотеке владельца. Сторонние личные документы не переносятся в публичный репозиторий. Полные защищённые книги, извлечения и PDF хранятся отдельно в пределах исследования; в Git передаются библиография, краткий анализ и контрольные сведения.

## O. Выполненная первичная сверка Иуды и проповеди — 2026-11-06

MON-02 закрыта в части получения собственного позднего места Оуэна: издание 1855 года, с. 543–548, семь факсимиле с титулом. Очередь целых комментариев остаётся. В MON-01 дополнительно полностью прочитана гл. IX *Display* и участок IV.1 *Death* о всеобщем предложении; у Девенанта прочитаны ответы 14–16, с. 392–398, с собственным Петром/Иудой. Пастырский участок Пакера, полный *The Warrant of Faith* Сперджена, полная Session 7 Пайпера 2008, проповедь Риккарди 16.01.2022, статья Бике 2009 и *Free Grace* Уэсли дают реальный сравнительный материал. Именованная цена Иуды у Августина сверена с латинским оригиналом Ps.68, sermo II.11 и переводом; In Ioh.48.4–6 — отдельный контроль спасительного приобретения.

Число тематических групп остаётся **99: SYS-01–39, MON-01–46, ART-01–14**. Новые авторские имена из проповеди Сперджена относятся к существующему пакету основания веры и пуританской рецепции: Abraham Booth, *Glad Tidings to Perishing Sinners*; John Saltmarsh, *Free Grace*, с раздельной проверкой предисловия Huntington; Tobias Crisp и критикуемые Baxter, Alleyne, Rogers of Dedham, Shepherd (автор *The Sound Believer*), Thomas Hooker. Это названные Спердженом первичные цели поиска, а не прочитанные книги и не новые притворно закрытые группы. Оригиналы нужны для проверки его исторических оценок.

Текущая задача MON-22 — получить целый аргумент Lynch; собственные страницы Девенанта и прочитанная рецензия James Clark не заменяют книгу. MON-20/21 и ранее недоступная глава Mullins сохраняют прежние ограничения. Полные связанные главы систематик продолжают читаться по содержанию вопроса, без фиктивного зачёта многотомников. [Принятый результат и пределы](../docs/research/atonement/17_quote_mining_and_theological_equivocation.md), [поздний Оуэн](12_HARD_TEXTS_EXTENT_CARDS.md).

### AT-010-R9 — Coptic Isaiah 53:10 DECOT source access (2026-11-08)

Verified via direct DECOT API/XHTML: [sa212L.9 622148/2250](https://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docid=622148&pageID=2250&format=xhtml) — PHOTO_NOT_COLLATED; [sa211L 620292/3090](https://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docid=620292&pageID=3090&format=xhtml) — PROTECTED_IMAGE_ACCESS_HOLD; [CLM3469 622028/350](https://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docid=622028&pageID=350&format=xhtml) — PROTECTED_IMAGE_ACCESS_HOLD and CLM3469_EDITORIAL_READ_CONFLICT_HOLD versus Bąk 2023 p.869; [sa108L 620016/2575](https://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docid=620016&pageID=2575&format=xhtml) — TARGET_CLAUSE_NOT_PRESENT. Digital editorial transcriptions do not certify original glyphs. RIGHTS_HOLD and PUBLICATION_HOLD. Details and alternative interpretations in evidence/AT010_ARTICLE02_SEMANTIC_REVIEW_2026-11-07.md.

### AT-010-R17 — датированные транскрипции Кумрана (09.11.2026)

- **QD-4Q58-20260521:** [Qumran-Digital, 4Q58](https://lexicon.qumran-digital.org/transcriptions/4Q58/2026-05-21/index.html), VIII.19–22, Ис. 53:10–12; DIGITAL_EDITORIAL_TRANSCRIPTION_READ_TARGET_LINES; צילום/фотографии оригинальных чернил не коллированы, хранение музейных снимков не утверждено. На 53:11 стоит או֯[ר].
- **QD-1Q8-20250825:** [Qumran-Digital, 1Q8](https://lexicon.qumran-digital.org/transcriptions/1Q8/2025-08-25/index.html?v=2025-08-25), XXIII.21–25, Ис. 53:10–12, параллель по опубликованной цифровой редакции; цифровое чтение, не независимая фотография. [IAA / Leon Levy archive](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/1Q8-1?locale=en_US) указывает физический архив, не статус прочтения снимка.

Контрольная дискуссия: [memo R17](evidence/AT010_ARTICLE02_SEMANTIC_REVIEW_2026-11-07.md). 1Q8 (1QIsaᵇ, пещера 1) не путать с 4Q56 (4QIsaᵇ, пещера 4). GLYPH_PHOTO_HOLD, GOTTINGEN_APPARATUS_HOLD, RIGHTS_HOLD, PUBLICATION_HOLD, publicationEligible=false сохраняются.
