# Искупление — source registry и очередь добычи

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
| R08 | P-REFORMED | John Gill, Body of Divinity VI.4 + *Cause* Part I | отдел `Джон Гилл/` | universal texts | EXISTS in Gill corpus | YES where Gill dossiers already verbatim | do not duplicate |
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
| M24 | P-CONFESSION-adj | OPC, *The Free Offer of the Gospel* (Murray/Stonehouse/Kuschke majority, 1948) | B5: Иез. 18/33; Мф. 23:37; Ис. 45:22; 2 Пет. 3:9. Не extent. Minority Young/Hamilton на той же странице | церковный отчёт, публично | https://opc.org/GA/free_offer.html прочитан (чанки 0–6/8) | paraphrase YES; не исповедание | LINK_ONLY |
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
| O04 | SECONDARY | Gill corpus in this repo | `Джон Гилл/27_…`, `12_CAUSE…`, `23_SECTION_LVII…`, `48_SOTERIOLOGY…` | не дублировать | follow Gill quote state |
| O05 | SECONDARY | Apostasy corpus | `apostasy/08_SOURCE_REGISTRY…`; `apostasy/12_2_PETER_2_CANONICAL_SUPPLEMENT_2026-09-30.md` | Heb 6/10 не решать заново; 2 Пет. 2:1 не решать системой искупления до экзегезы письма | follow apostasy |
| O06 | SECONDARY | Highway Murray *The Atonement* | https://www.the-highway.com/atonement_murray.html | copyright; paraphrase in `11` | NO |
| O07 | SCHOLARLY-OPEN | OPC Free Offer 1948 | https://opc.org/GA/free_offer.html | majority+minority; B5 | paraphrase of public church paper |
| O14 | LANE-REGISTRY | Реестр массы носителей позиции: `docs/research/atonement/35_four_point_authors_mass_registry.md` (151 строка, 12 эпох, классы `A1`/`A2`/`B1`/`B2`/`C`, очередь `Q-01`…`Q-82`) | — | источник новых кандидатов в эту очередь; по первичному изданию прочитано 17 % строк | NO, пока позиция в классе `C` |

---

## G. Очередь Wave 2 (добыча PD в Drive `01` и `04`)

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
14. Приоритет добычи задаёт реестр `35_` §17: сначала те `C`-строки, у которых текст уже открыт (Буньян — IA 24 с. / Chapel Library 30 с. плюс *The Baptist Quarterly* 21:3, сс. 126–130; Э. Б. Чейз и крещендобрический ролл — `middletownbiblechurch.org`; Сомюр — Aymon II 183 и 298, Swisser 1856, Niemeyer 729–739), потому что они закрывают сразу по несколько строк реестра.
15. Класс позиции поднимается (`C` → `B1`/`A2`/`A1`) только вместе с локатором по изданию и строкой очереди, снятой из `35_` §17: `C` без адресата и `A1` без страницы/колонки/параграфа — FAIL правила 23, то есть повышение класса «на глаз» технически невозможно.

Не качать и не класть: Murray, Packer 1959, Gibson 2013, Morris, Stott, Berkhof, Bavinck EN.

Если владелец покупает Murray — класть **только** в `02 — COPYRIGHT BIBLIOGRAPHY & ACQUISITION`, с пометкой `PRIVATE_STUDY_ONLY`. Публичные цитаты всё равно item-level.
| O08 | PRIMARY-TEXT | Editio Maior / BTC, Ioannis 11:47–11:56 | — | аппарат 11:52: варианты, влияющие на объём (`ἕν/ἓν`, `καί`); без него «разночтений нет» не утверждается | NO |
| O09 | PRIMARY-TEXT | LXX (Göttingen/Rahts): Иер 31:10; Иез 34:12; 37:21; Soph 3:19–20 | — | точная формула «рассеял — соберу» для `nt/15_` §2.3 | NO |
| O10 | PATRISTIC | Иоанн Златоуст, In Ioannem, homilia на 11:45–54 | — | древнее чтение «диаспора vs язычники»; у Кальвина на 12:32 процитирован, но место не снято | NO |
| O11 | PATRISTIC | Кирилл Александрийский, In Ioannem (кн. на 11:49–53) | — | «чада по предведению» vs «чада по обóжению» | NO |
| O12 | PATRISTIC | Августин, In Ioannis evangelium tractatus (на 11:45–57) | — | `multi in grege, non omnes`; владение текстом необходимо перед цитатами в полемике | NO |
| O13 | SECONDARY | Страницы изданий: Кальвин (Pringle 1840) на 11:52 и 12:32; Гилл; Алфорд; Бенгель; Уэсли; сверка атрибуции «только диаспора» (Jamieson-Fausset-Brown?) | StudyLight, BibleHub (перепечатки) | перевод `LOCATOR_PARTIAL`-записей `nt/15_` §5 и `13_` §2.5 в `LOCATOR_FULL` | NO |
