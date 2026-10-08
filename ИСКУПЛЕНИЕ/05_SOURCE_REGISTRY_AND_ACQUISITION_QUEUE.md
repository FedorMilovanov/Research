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
| S02 | P-BIBLE | BHS / WLC OT | то же | еврейский ВЗ | LEAD | NO | LINK_ONLY |
| S03 | P-BIBLE | LXX Rahlfs/Göttingen | то же | Септуагинта `ἱλάσκομαι` / `λύτρον` | LEAD | NO | LINK_ONLY |
| S04 | P-BIBLE | Синодальный / сопоставление русских | reader-facing цитаты только с указанием перевода | русская публикация | OPEN | YES with edition | LINK_ONLY |

---

## B. Исповедания — PD

| ID | Tier | Source | URL | Supports | Status | Quote-safe | Custody |
|---|---|---|---|---|---|---|---|
| C01 | P-CONFESSION | Canons of Dort, Second Head | **Schaff Latin chunk 165** https://www.ccel.org/ccel/schaff/creeds3/cache/creeds3.txt (EN-колонки в этом TXT **нет**: чанки 163–165 — латынь, проверено 2026-10-07); **Scott 1841 EN с. 282–286** — *The Articles of the Synod of Dort…*, пер. Thomas Scott, 1841, archive.org item `articlesofsynodo1841syno`, PD; **EN перевод 1840 г.** — Git [`16`](16_DORT_HEAD_II_ENGLISH_1840_PRIMARY_TEXT.md) (перенесён из Drive `01`, `10_W0_PRIMARY_TEXT_DORT_HEAD_II_AND_CALVIN_2026-10-07.md`, id `1hPs1aEWtwv1GHGHtZVtpWd8c91bQgAgo`): полный английский текст artt. I–IX (1840, Wikisource-транскрипция), **без Rejection**; CRCNA chunks 3–4 — reading copy, перевод 1986 copyright, не dump; карта `15` | sufficiency/efficiency; Rejection I–VII | LATIN PD LOCATED chunk 165; **EN PD EDITION SELECTED** = Scott 1841 (страницы по артикулам I–IX и по Rejectio I–VII); **EN full text** — Scott 1841: артикулы I–IX + Rejectio I–VII в `15` §B.5 (OCR, сличение §B.6); перевод 1840 г.: артикулы I–IX в `16` | Latin YES for research; EN — два независимых перевода, сличенные по латыни (`15` §B.6); сокращение Rejectio IV у Скотта зафиксировано; Product NO, пока действует `PUBLICATION_HOLD` | LINK_ONLY |
| C02 | P-CONFESSION | Westminster Confession ch. 8, 11 | Drive copy `1VSp4vU56X8uuYrp2SERkp2p0BRk-vQq4` (**16 179 601 bytes**, скан без текстового слоя: `read_file_text` → `empty`; страница не извлекаема, не ретраить); **Schaff/CCEL chunks 182–183** = Chapter VIII EN+LA; карта `15` §D | Посредник; объём (8.1 / 8.5 / 8.6 / 8.8); оправдание | **TEXT LOCATED**: Schaff chunks 182–183 (EN+LA, постатейно); Drive PDF page unchecked | NO до item-level решения | ACQUIRED_DURABLE copy; locator HOLD **по странице** (не по тексту) |
| C03 | P-CONFESSION | WLC 38–59 | CCEL / same WCF volume | личность и дело Христа | LEAD | NO | LINK_ONLY |
| C04 | P-CONFESSION | Second London 1689 ch. 8, 11 | открытые транскрипции; сверять с факсимиле | баптистский twin | LEAD | NO | LINK_ONLY |
| C05 | P-CONFESSION | Belgic Confession art. 20–22 | CCEL Schaff | удовлетворение / вера | LEAD | NO | LINK_ONLY |
| C06 | P-CONFESSION | Heidelberg Catechism LD 5–7, 15–16 | CCEL | необходимость Посредника | LEAD | NO | LINK_ONLY |
| C07 | P-CONFESSION | Formula of Concord / Lutheran | для P6, не как наш канон | лютеранское universal atonement | LEAD | NO | LINK_ONLY |

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
| R01 | P-REFORMED | Calvin, *Institutes* II.12, II.16, II.17; III.24 | Drive 45 MB extract fail; Beveridge TXT: II.12 = 155; II.16 = 168; II.17 = 176–177; III.24.15–17 = 330–331 | природа/необходимость/merit; 1 Тим. 2:4 / 2 Пет. 3:9 | LOCATED in CCEL TXT; Drive page unchecked | NO for Product | copy + CCEL TXT |
| R02 | P-REFORMED | Calvin commentaries: Isa 53, John 3, 1 John 2, 1 Tim 2, Heb 2, 2 Pet | ~~CCEL `calcom45` reader login-wall~~ → **PD-скан найден 2026-10-08**: *Commentaries on the Catholic Epistles* (CTS, Edinburgh, 1855; пер. John Owen), IA `commentariesonca00calv`, `NOT_IN_COPYRIGHT`. **Локаторы: 1 Ин. 2:2 — с. 169 (стих) / 172 (начало разбора) / 173 (ключевой абзац); 2 Пет. 2:1 — с. 393; 2 Пет. 3:9 — с. 419–420.** Печатная страница = лист − 6 (три привязки колонтитулами + указатель тома). Реконструкция 2026-10-07 подтвердилась. CCEL `calcom45` по-прежнему пуст — не ретраить | extent texts | **research quote-safe с локатором** (было LEAD / wall); `PUBLICATION_HOLD` не снят | NO | LINK_ONLY |
| R03 | P-REFORMED | Owen, *Works* (Goold) | Drive `1gfKY8eXGhV-HL5O4u1tVVcCRYNKx-dQY` | Death of Death обычно vol. 10 | ACQUIRED_COPY / volume-page unchecked | NO | copy |
| R04 | P-REFORMED | Owen, *Death of Death* standalone | CCEL TXT https://ccel.org/ccel/owen/deathofdeath/cache/deathofdeath.txt ; PDF/HTML те же URL; карта `14` | extent polemic | Book IV chunks 70–90 LOCATED (1 Tim 2:4 = 80–81; 2 Pet 2:1 = 87–88; Heb 10:29 = 88–89). Goold page open | NO until Goold page | LINK_ONLY + research map `14` |
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

Не качать и не класть: Murray, Packer 1959, Gibson 2013, Morris, Stott, Berkhof, Bavinck EN.

Если владелец покупает Murray — класть **только** в `02 — COPYRIGHT BIBLIOGRAPHY & ACQUISITION`, с пометкой `PRIVATE_STUDY_ONLY`. Публичные цитаты всё равно item-level.
