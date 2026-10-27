# Чарнок — матрица доступа к корпусу и локаторы

> **CHARNOCK-HANDOFF-V1 · wave40 · 2026-10-26**
> Роль: QUOTATION_OWNER. Текущий объём/пределы —[00](00_README_AND_NAVIGATION.md)
> и[16§20](16_SERIES_ARCHITECTURE_AND_PERSONS_CHAIN.md);статус доставки —
> `data/charnock-handoff-receipt-v1.json` после независимой проверки. Без квитанции закрытие не утверждается.
> Текущий конечный план —§12:16кандидатов/7research-only/1SVG. Все BLOCKED/PUBLICATION_HOLD;переводы и публичный допуск не подготовлены.
> Исходные транскрипции/старые выводы сохранены;противоречащие текущим решениям итоги HISTORICAL/SUPERSEDED,не разрешение публикации.


> **Текущий план цитат/иллюстраций — §12,wave39.**
> 16лексических кандидатов,7research-only,1общаяSVG;все BLOCKED/PUBLICATION_HOLD.
> Ранние счётчики ниже исторические,не текущая сертификация полного корпуса.


**Объект:** Stephen Charnock, B.D. (1628–1680)
**Том:** 06 отдела «Стивен Чарнок»
**Дата:** 2026-10-25

---

## 1. Проверяемый вопрос

К корпусу каких источников у нас есть доступ, на каком уровне (текст / метаданные / ничего),
и какие HOLD из этого следуют?

**Текущий ответ (wave28):** доступ и объём чтения различаются; актуальное
состояние ниже в §1A. Прежний ответ «нет доступа к Johnson1680» —
**SUPERSEDED**: текст уже получен, см.09. Нижние старые таблицы —
HISTORICAL, не текущая сертификация доступа/лицензий или полноты чтения.

---

## 1A. Текущая ограниченная матрица — wave28, 2026-10-25

| Объект | evidenceClass | accessState | locatorState | rightsState | publicationState | Владелец |
|---|---|---|---|---|---|---|
| Johnson1680, Adams & Veal, Wood1691, три поэтических/памятных объекта1680 | A1 — сами тексты, не каждая их атрибуция | PARTIAL_OBJECT — полный текст отдельных объектов/отрывков отмечен в томах; не общий архив сканов | EXACT_LOCATOR_VERIFIED для выделенных TCP-мест | PRIVATE_STUDY_ONLY; TCP-текст и снимки различать | BLOCKED | 08,09,11–14 |
| A32723, фолиант1682 | A1 | FULL_OBJECT_VERIFIED для SHA-pinned XML в текущем проходе; не полное чтение содержания/скана | EXACT_LOCATOR_VERIFIED для TEI-структуры и выбранных мест; не всех цитат | PRIVATE_STUDY_ONLY до раздельной проверки объекта/изображений | BLOCKED | 03,04;16 §8 |
| A32724, Supplement1683 | A1 | FULL_OBJECT_VERIFIED для SHA-pinned XML в текущем проходе | EXACT_LOCATOR_VERIFIED для структуры/выбранных мест | PRIVATE_STUDY_ONLY | BLOCKED | 03,04;16 §8 |
| Nichol1864–66/современные хосты | A1 — старый авторский текст; не A2 из-за сайта | PARTIAL_OBJECT — выбранные места, не полный локальный пяти-томный архив | COARSE_LOCATOR_ONLY для общего набора; отдельные цитаты имеют свои состояния | RIGHTS_UNKNOWN для конкретных файлов/репродукций | BLOCKED | 03,10 |
| Приходской регистр/New College/оригинал завещания | A1 — целевой документ | NOT_ACQUIRED | LOCATOR_MISSING для самого не полученного объекта | RIGHTS_UNKNOWN | BLOCKED | 01,02,05 |
| Аукционный каталог1680 | C — текущие сведения о доступе; класс самого документа отдельно | CATALOG_ONLY/частичные транзитные сведения, не подтверждённый здесь полный скан | COARSE_LOCATOR_ONLY | RIGHTS_UNKNOWN | BLOCKED | 03,04 §0X |
| Внешние книги, цитируемые Чарноком | A1 для выбранного текста; идентификации могут оставаться C | PARTIAL_OBJECT | индивидуально по04 | индивидуально по04 | BLOCKED | 04 §0X–0AB |

Для всех групп сохраняются применимые **ARCHIVE_HOLD, RIGHTS_HOLD,
PUBLICATION_HOLD**; для не проверенных по изображению буквальных цитат —
**LOCATOR_HOLD**. Полученный в сеансе XML не означает долговременного архива
первоисточника. Подсчёт элементов не означает чтение всех дискурсов.
Классы A2/A3 в старых строках, присвоенные только по имени современного
хоста/каталога, не являются текущей классификацией. Запись о сайте не
наследует автоматически класс авторского текста, размещённого на нём.

**HISTORICAL:** нижние §2–7 сохраняются для истории добычи. Старые задачи
«найти Johnson», «получить Calamy» не считать вновь открытыми без обращения
к томам-владельцам. Calamy1713/1727 уже рассмотрен в04 §0B–0B.1; отдельные
архивные/страничные вопросы при этом могут оставаться открытыми.

## 2. HISTORICAL — прежняя матрица доступа

### 2.1. Корпус сочинений

| Ресурс | Идентификатор | evidenceClass | accessState | locatorState | rightsState | HOLD |
|---|---|---|---|---|---|---|
| **Nichol 1864–66, 5 vols** — каноническое издание | IA `completeworksofs0000char`; IA `completeworksofs00charuoft` | `A1` | **full text** | страницы проверяемы по OCR | public domain | — |
| Тот же набор, отдельные тома | IA `completeworksof01char`, `completeworksofs02char`, `completeworksofs03char`, `completeworksofs04char`, `completeworksofs05char` | `A1` | **full text** | страницы проверяемы | public domain | — |
| **EEBO-TCP** *A Discourse of Divine Providence* | `A79420.0001.001` | `A1` | **full text** | титульный лист и префаторий проверены (раздел `1:1` title page, `1:2` TO THE READER) | **TCP keyboarded text — CC0 1.0**; отказ не распространяется на page images | `LOCATOR_HOLD` только по печатной странице |
| **CCEL** — *Necessity of Regeneration* | `ccel.org/c/charnock/nec_regen` (html), `ccel.org/ccel/charnock/nec_regen.ii.html`, `ccel.org/ccel/c/charnock/nec_regen/cache/nec_regen.pdf` | `A2` | **full text** | — | — | — |
| **CCEL** — *Nature of Regeneration* | `ccel.org/ccel/charnock/nat_regen/nat_regen.i.html` | `A2` | **full text** | — | — | — |
| **CCEL** — *Efficient of Regeneration* | `ccel.org/ccel/charnock/efficient_regeneration/efficient_regeneration.{ii,iii}.html` | `A2` | **full text** | — | — | — |
| **CCEL** — *Word, Instrument of Regeneration* | `ccel.org/ccel/charnock/instr_regen/instr_regen.html`; `ccel.org/c/charnock/instr_regen/instr_regen.html` | `A2` | **full text** | — | — | — |
| **Digital Puritan** — vol. 1–5 | `digitalpuritan.net/Digital Puritan Resources/Charnock, Stephen/` (epub / txt.html / pdf) | `A2` | **full text** | — | — | — |
| **Digital Puritan** — vol. 3 (txt) | `…The Complete Works of Stephen Charnock (vol.3).txt.html` | `A2` | **full text** | — | — | — |
| **Digital Puritan** — vol. 1 individual titles | `Works (vol.1) Ind Titles/[SC] A Discourse Upon Spiritual Worship.pdf`; `…[SC] Practical Atheism.pdf` | `A2` | **full text** | — | — | — |
| **Gutenberg** 53527 | *The Existence and Attributes of God* (Baker Books reprint с биографией Symington) | `B1` | **full text** | — | репринт 1996 — в авторском праве издания, текст PD | `RIGHTS_HOLD` |
| **grace-ebooks** | `SC-Discourses-On-The-Existence-and-Attributes-of-God-Vol-1.pdf` | `A2` | доступен как PDF | — | — | — |
| **HathiTrust** | Record 001961147 (BX9315 .C427 1864); Record 008726777 | `A3` | metadata only | — | — | — |
| **Open Library** | OL21706307M; OL7026770M | `A3` | metadata only | — | — | — |
| **WorldCat** | OCLC 18480269 | `A3` | metadata only | — | — | — |
| **Monergism** — *A Treatise on Divine Providence* | `monergism.com/thethreshold/sdg/charnock/…` (pdf, epub) | `A2` | **full text** | — | — | — |
| **puritansermons** reprint (1844) | IA `puritansermons160001unse` (6 vols) | `A1` | **full text** | sermon 19 в vol. 2 | public domain | `CONFLICT-8` |
| ***The Sinfulness and Cure of Thoughts*** (Gen. 6:5) — **единственная прижизненная публикация** | Digital Puritan PDF: `digitalpuritan.net/Digital%20Puritan%20Resources/Cripplegate/The%20Morning%20Exercises%20at%20Cripplegate%20(vol.2)%20-%20Ind%20Works/%5BCG%20v2s19s%5D%20The%20Sinfulness%20and%20Cure%20of%20Thoughts%20(Stephen%20Charnock).pdf` | `A1` (содержание) / `A1` (репринт 1844) | **full text**, 35 pp. | sermon 19 в *Supplement to the Morning Exercise at Cripplegate*, репринт 1844 vol. 2 | public domain (1844) | `LOCATOR_HOLD`; `ARCHIVE_HOLD` **снят** |
| Репринт 1844, vol. 2 (Google Books) | `books.google.com/books?id=MuMEAAAAQAAJ` | `A1` | full text | «The Conclusion of the Supplement to the Morning Exercise at Cripplegate» | public domain | `LOCATOR_HOLD` |

### 2.2. Биографические свидетельства

| Ресурс | evidenceClass | accessState | locatorState | HOLD |
|---|---|---|---|---|
| **McCosh, Introduction (1864)** | `B1` с `A1`-транзитом | **full text** (PDF; страницы доступны) | — | — |
| **Symington, Life and Character (1853)** | `B1` | **full text** (Gutenberg 53527) | — | — |
| **DNB vol. 10 (1887)** | `B1` | **full text** (Wikisource) | — | — |
| **Johnson funeral sermon 1680** | `A1` | **FULL TEXT получен** — EEBO-TCP `A46911.0001.001`, CC0 1.0, pp. 1–40 | **`checked`** — Charnock-материал pp. 33–40 | `LOCATOR_HOLD` только по печатному снимку |
| **Adams & Veal epistles** | `A1` | **full text** — EEBO-TCP `A79420.0001.001` раздел `1:2` (изд. 1684, CC0 1.0) | `checked` на уровне раздела EEBO-TCP | `LOCATOR_HOLD` по печатной странице |
| ***A treatise of divine providence* — 1-е изд. 1680** (`A32726.0001.001`, Wing **C3712**, ESTC R13224, 418 pp.) | `A1` | **ПОЛУЧЕН 2026-10-25** — титульный лист (узел `1:1`, с эпиграфом Пс. 103:19), лист «Advertisement» (`1:2`), эпистол «TO THE READER» (`1:3`) | **`checked`** на уровне узлов | **`RIGHTS_HOLD`**: каталог TCP даёт Restricted, страница Michigan — CC0; расхождение не разрешено. Эпистол идентичен эпистолу издания 1684 → `CONFLICT-12` по эпистолу закрыт |
| ***Several discourses upon the existence and attributes of God* — 1-е изд. 1682** (`A32723.0001.001`, Wing **C3711**, ESTC R15604, 866 pp.) | `A1` | **титульный лист ПОЛУЧЕН 2026-10-25** (узел `1:1`); остальной том не читался | `checked` для титульного листа | **Разрешает `CONFLICT-6`** (1682). `RIGHTS_HOLD` как у `A32726`. Внутренние титульные листы фолианта не читались |
| ***A supplement to the several discourses upon various divine subjects* — 1683** (`A32724.0001.001`, Wing **C3711C**, ESTC R24823, 158 pp.) | `A1` | **оглавление и первый дискурс ПОЛУЧЕНЫ 2026-10-25** (узлы `1:1`–`1:14`; начало «Sinfulness and Cure of Thoughts», Быт. 6:5, стр. 1) | `checked` для оглавления и стр. 1 | **Перепечатывает единственную прижизненную публикацию** со стр. 1 — `A1`-текст для колляции с broadside 1680. `RIGHTS_HOLD` как у `A32726` |
| **Ин. 16:9 и Ин. 17:3 — sermon'ы Чарнока, не размеченные** | `B1` | аттрибуция элегии 1680 (`A39134.0001.001`), сноски b и c | unchecked | **`CONFLICT-15`**: в фолианте 1682 и *supplement* 1683 дискурсов на эти тексты нет; sermon'ы не найдены |
| ***A sermon preached by the late eminent Mr. Steph. Charnock on 2 Cor. V. XIX.* — 1680** (`A32722.0001.001`, Wing **C3710**, ESTC S104952, 38 pp.) | `A1` | **титульный лист и начало sermon ПОЛУЧЕНЫ 2026-10-25** (узлы `1:1`, `1:2`) | `checked` для импринта и стр. 5–10 | Импринт: Thomas Milbourn for J.K., sold by Langley Curtis **in Goat-Court, on Ludgate-Hill**. Sermon начинается на стр. 5 — номера стр. 1–4 в TCP не читаются (`LOCATOR_HOLD`). `RIGHTS_HOLD` как у `A32726` |
| ***Death and the grave, without either sting or victory… Mr. Christopher Fowler*** (Anon., 1677; Wing **D501A**) | `A1` | **FULL TEXT получен 2026-10-25** — EEBO-TCP `A37311.0001.001`, CC0 1.0 | **`checked`** — один лист, узел `1:1` | Элегия + акростихи **CHRISTOPHER** (11 ст.) и **FOWLER** (6 ст.) + эпитафия + приписка. Даёт: две последние проповеди Fowler'а на **Ин. 16:8**; «Nahum the second»; «Joshua the sixth»; «low seat» у трапе Господней. `CONFLICT-14` |
| ***An elegy on the learned and zealous minister… Mr. Christopher Fowler… Monday the 15th of January, 1676/7*** (Anon., 1677; Wing **E420**) | `A1` | **FULL TEXT получен 2026-10-25** — EEBO-TCP `B03233.0001.001`, CC0 1.0 | **`checked`** — один лист, узел `1:1` | Открытие: «Art thou gone too… call not home so fast our Sons of Peace… Who will be left on Earth t' supply their room?» — та же топа, что в *New Poems* 1680. День недели в заглавке проверен вычислительно |
| **Приходской регистр St Michael's** | `A1` | **НЕ получен** | unchecked | `ARCHIVE_HOLD` |
| **Calendar of State Papers, Domestic** | `A1` | **НЕ получен** | unchecked | `ARCHIVE_HOLD`, `LOCATOR_HOLD` |
| **New College books / Fasti Oxonienses** | `A1` | **НЕ получен** | unchecked | `ARCHIVE_HOLD` |
| **Calamy, Account / Continuation** | `B1` | **НЕ получен** | unchecked | `ARCHIVE_HOLD` |
| **Wood, Athenae Oxonienses (ed. Bliss), iii. 1234–6** | `B1` | **НЕ получен** | unchecked | `ARCHIVE_HOLD` |
| **Parker, History of his own Time, p. 71** | `D` | **НЕ получен** | unchecked | — |
| **Wilson, Dissenting Churches, vol. i, pp. 331 sqq.** | `B1` | **НЕ получен** | unchecked | `ARCHIVE_HOLD` |
| **Urwick, Independency in Dublin in the Olden Time** | `B1` | **НЕ получен** | unchecked | `ARCHIVE_HOLD` |
| **Wood, Athenae Oxonienses 1691 — вход [429] + Fasti 1654** | `A1` | **FULL TEXT получен 2026-10-25** — EEBO-TCP `A71277.0001.001`, CC0 1.0 | **`checked`** — вход [429] на pp. 491–492; Fasti 1654 на p. 783 | `LOCATOR_HOLD` только по печатному снимку |
| **Bliss-редакция Wood 1813–20** (4 vols., колонки) | `A1` | **НЕ получен** | unchecked | `ARCHIVE_HOLD`; колонка входа [429] требует пересчёта |
| **1680 sermon on 2 Cor. 5:19 — скан страниц** | `A1` | **доступен как page images** — IA `bim_early-english-books-1641-1700_a-sermon-preached-_charnock-stephen_1680` (675 MB, микрофильм EEBO) | `image` — страницы видны, OCR не читаем | `LOCATOR_HOLD`; imprint частично разборчив, уточнение требует чтения титульного листа |
| **1680 Providence, 1st ed. — скан страниц** | `A1` | **доступен как page images** — IA `bim_early-english-books-1641-1700_a-treatise-of-divine-pro_charnock-stephen_1680` (675 MB, микрофильм EEBO) | `image` | `LOCATOR_HOLD`; сверка эпистола с изданием 1684 не выполнена → `CONFLICT-12` |
| ***An Elegy on the death of the truly reverend, learned and pious, Mr. Stephen Charnock, July 27, 1680*** (Anon.; 1680) | `A1` | **НЕ получен**; идентифицирован 2026-10-25 — WorldCat 606749756, в EEBO (ProQuest) | unchecked | `ARCHIVE_HOLD`; **приоритет высокий**: contemporaneous печатное attestation даты смерти 27 июля — см. `CONFLICT-10` |
| ***The sayings of that reverend and great preacher Mr. S. Charnock***, broadside, 1680 | `A1` | **FULL TEXT получен 2026-10-25** — EEBO-TCP `B02133.0001.001`, CC0 1.0 | **`checked`** — единственный лист, узел `1:1`, ~38 афоризмов | `LOCATOR_HOLD` только по печатному снимку |
| ***New poems upon the death of that eminent servant of God and truly pious and learned minister of the Gospel, Mr. Stephen Charnock who departed this life July 27, 1680*** (Anon. — «by a lover of all those who are lovers of the truth»; London: Thomas Snowden, 1680) | `A1` | **FULL TEXT получен 2026-10-25** — EEBO-TCP `A52960.0001.001`, CC0 1.0 | **`checked`** — узлы `1:1` (элегия 130 ст. + два акростиха + эпитафия 12 ст.) и `1:2` (колофон) | `LOCATOR_HOLD` только по печатному снимку. **Wing N715**; ESTC R35069. Содержит четыре эксклюзивных биографических сведения; `CONFLICT-10`, `CONFLICT-14` |
| ***An Elegy on the death of the truly reverend, learned and pious, Mr. Stephen Charnock, July 27, 1680*** (Anon.; London: Printed by **J.A.** for **Thomas Cockeril**, 1680) | `A1` | **FULL TEXT получен 2026-10-25** — EEBO-TCP `A39134.0001.001`, CC0 1.0 | **`checked`** — узлы `1:1` (элегия 100 ст. + 5 сносок-аттрибуций) и `1:2` (колофон) | **Wing E409**; ESTC R36110. `LOCATOR_HOLD`: метки страниц «122»/«120.» аномальны и с каталоговым объёмом (1 страница) не согласуются; печатник «J.A.» не идентифицирован; keyboarded text не сверялся со снимком |
| **Элегия 1680 — пять sermon'ов Чарнока по библейским текстам** (2 Пар. 16:9; Ин. 16:9; Ин. 17:3; Пс. 14:1; Наум 1:3) | `A1` (объект) / `B1` (аттрибуция) | **получено** — сноски элегии `A39134.0001.001` | `checked` на уровне сноски | `LOCATOR_HOLD`: сопоставление с каноническим изданием Nichol не выполнено |
| **Элегия 1680 — «Poole and Charnock» / «Three Nations»** | `B1` | **получено** — элегия `A39134.0001.001` | `checked` | идентификация «Poole» = Matthew Poole (1624–1679) — умозаключение отдела |
| **Полный каталог EEBO-TCP** (61 315 записей, `textcreationpartnership/Texts`, `TCP.json`) | `A1` (метаданные) | **получен 2026-10-25** | `checked` | служебный источник для Wing/ESTC/VID/EEBO-citation; не цитируется как источник содержания |
| **Christopher Fowler (1610–1678)**, изгнанный священник Reading, затем Kennington и Southwark — **кандидат в «Fowler's place»** | `B1` | **НЕ получен**; идентифицирован 2026-10-25 как гипотеза | unchecked | `ARCHIVE_HOLD`; требуется проверка по спискам проповедников *Morning Exercise* и Wilson, *Dissenting Churches* vol. i |
| *The Morning Exercise at Cripplegate*, 2-е изд. (Спб./Лонд., 1844), vol. 2 — sermon 19 Чарнока | `A1` | **full text** — Digital Puritan PDF (35 pp.); Google Books 1844 vol. 2 `MuMEAAAAQAAJ`; IA `puritansermons160001unse` vol. 2; Monergism | `checked` на уровне документа; постранично — **`LOCATOR_HOLD`** | `LOCATOR_HOLD` по странице; часть-титул заключительной части (1676?) не прочитан |
| **Oxford DNB**, ст. «Charnock, Stephen (1628–1680)», авт. Richard L. Greaves | `B1` | **НЕ получен полностью** (paywall); содержание по цитате | unchecked | `RIGHTS_HOLD` (подписка); Harrison-chaplaincy 1649–1650 и дата матрикуляции 30 мая 1642 требуют проверки |
| ***Bibliotheca Charnockiana***, London, 1680 — **печатный каталог аукциона библиотеки Чарнока, 4 октября 1680** | `A1` (объект) / `B1` (сведения о нём) | **НЕ получен**; в EEBO-TCP отсутствует (проверено по каталогу из 61 315 записей); значится в ESTC; сведения по Book Owners Online | unchecked | **`ARCHIVE_HOLD`** — требуется скан каталога. 1330 предмета; Latin theology 372, English divinity 256, Latin medicine **65**, European languages 75, pamphlets 314; продажа **£366 5s 1d**. См. том 03 §3G |
| **Завещание Стивена Чарнока, 25 июля 1680** | `A1` (документ) / `B1` (сведения) | **НЕ получен**; содержание по ODNB (Greaves) | unchecked | **`ARCHIVE_HOLD`** — оригинал в PCC/National Archives. £111, преимущественно родственницам; исполнительница и кузина — **вдова Ann Sykes**; ни жены, ни детей не упомянуто. См. том 01 §2.10 |

---

## 3. Локаторы, уже использованные в репозитории Research (сохранённые)

Ниже — Charnock locators, которые уже содержатся в корпусах Research. Они **сохраняются** и служат
точкой входа; см. том 07.

| Корпус Research | Том | Локатор | Использован для |
|---|---|---|---|
| `ИСКУПЛЕНИЕ/` | 07 ledger | Works 4:306, 4:496, 4:145, 4:251–252, 5:29, 5:96, 3:425 | Локаторы из 16 фрагментов, 7 из которых прочитаны |
| `TEEN_DOUBLE_LIFE/` | 52 | CCEL `nec_regen`, `nat_regen`, `efficient_regeneration`, `instr_regen` | Regeneration vs. restraint |
| `СЕРИЯ СЕРДЦЕ/` | 19 | Puritan source bank | Practical atheism; fourfold state |
| `СЕРИЯ СЕРДЦЕ/` | 43 | Digital Puritan vol. 3 | Two-state diagnostic; regeneration vs. conversion; predominancy of gracious habit |

**Статус этих локаторов:** `B1` (page numbers из digital edition, не сверенные с печатным
оригиналом Nichol 1864).

---

## 4. Что означает `locatorState` для quote-card

| Уровень | Требование |
|---|---|
| `verified` | страница сверена с печатным оригиналом (Nichol 1864 или первое издание) + запись в реестре |
| `digital` | страница/параграф из цифровой редакции; печатный оригинал не сверен |
| `unchecked` | есть текст, но нет страницы |
| `absent` | нет ни текста, ни страницы |

**Текущий уровень отдела:** `digital` для корпуса; **`checked`** для всех цитат из funeral sermon
Johnson 1680 (EEBO-TCP pp. 33–40) и из эпистола Adams & Veal (EEBO-TCP `A79420.0001.001` §1:2).

---

## 5. Границы допустимой формулировки

- Нельзя citing CCEL или Digital Puritan как «Nichol 1864, p. N» без постраничной сверки.
- Нельзя presenting IA-OCR как точный текст: требуется collation с печатным снимком.
- Нельзя утверждать, что архивный материал «отсутствует»: утверждается «не получен в данном
  контексте» — различие принципиально.
- Нельзя treating «leжит на Drive» как «процитировано».

---

## 6. Права, архив и публикационные HOLD

| Ресурс | rightsState | publicationState |
|---|---|---|
| Nichol 1864–66 | public domain (требуется фиксация provenance скана) | допустим после LOCATOR verification |
| Первые издания 1680–1702 | public domain | допустим после LOCATOR verification |
| EEBO-TCP | лицензия проверена: **TCP keyboarded text = CC0 1.0**; page images и сопроводительные файлы — вне отказа | допустим после LOCATOR verification |
| Gutenberg 53527 | текст PD; оформление Baker 1996 — право | `RIGHTS_HOLD` на оформление |
| Banner of Truth / Sovereign Grace репринты | в авторском праве | `RIGHTS_HOLD` |
| Портреты (Williams' Library; plate in folio) | права на репродукцию не проверены | `RIGHTS_HOLD` |

---

## 7. Следующее проверяемое действие

1. Скачать полный текст всех 5 томов Nichol 1864 из IA и построить постраничный index для
   quote-card кандидатов.
2. Найти и получить funeral sermon Johnson 1680 (EEBO/ESTC/Williams' Library).
3. Найти Calamy, *Continuation*, p. 83 в оригинале.
4. Найти запись Calendar of State Papers (Domestic) за 19–20 июня 1663.
5. Зафиксировать provenance каждого используемого скана (источник, дата скачивания, SHA-256).


## 10. Текущая дельта доступа: сборник 1676 — wave35

**Ограничение ранних таблиц:** значения доступа/прав в §§0–2 относятся к
моменту тех записей; для десяти закреплённых XML текущие состояния принадлежат
общему JSON. Раннее PRIVATE_STUDY_ONLY по A32723/24 не означает запрета на
ныне проверенный CC0 TCP-текст; page images этим не разрешаются. Ранее снятый
ARCHIVE_HOLD репринта не снимает HOLD оригинального первого выпуска.

Полностью получен A25478, *Supplement to the Morning-Exercise*, второе издание,
1676. Титул, посвящение, оглавление и sermon XIX проверены в объёме тома03 §13.
S.C.; pp.471–502; три места сопоставлены с A32724 pp.1/2/19. Посвящение19June1674
не датирует первый отпечаток. Инициалы плюс позднейшая атрибуция не доказывают
разрешения автора. Широкая формула «единственная прижизненная публикация» в
ранних строках остаётся ограниченной, не готовым исчерпывающим выводом.

Текущий объём:67TCP-опор/10XML,23ручных support-записи;12bibliographyUnits=
7печатных объектов+5семейств долгов,не12произведений. PUB-07 относится ко всему
сборнику, предметно исследована только требуемая часть. Полные пути,commit/SHA,
пять осей и HOLD — в общем JSON; точные текстовые локаторы FST-01–08 и три
editionComparisons. Основной WorksVol.II по-прежнему не получен.


## 11. Достижимая страница не равна полученной книге — wave36

Текущая дельта в03 §14. PRDL дал конкретный GB-кандидат1674
`UHPza-1yHckC`; получена оболочка viewer, не прочитано изображение титула.
Два текстовых маршрута HTTP500. Open Library второго фолианта дал
Human Verification. Эти ответы не маскируются как полный текст или каталог,
прочитанный сверх фактического объёма. Обход проверки/заказ сканов не выполнялись.

Два `acquisitionRequests` — неотправленные черновики с точными комплектами
проверки и критериями приёмки. receipt=null; ни ARCHIVE_HOLD, ни права
не снимаются. Нет приобретённых новых XML:67 anchor/10 XML;24 ручных support.
Авторизация первой печати и состав основного Vol.II остаются открытыми.
Реестр пяти состояний и текущий объём — общий JSON; ранние строки исторические.


## 12. Конечный исследовательский план цитат и иллюстраций — wave39, 2026-10-26

Текущий владелец — researchPreparationReview в
`data/charnock-biographical-anchors-v1.json`;исторические счётчики прежних волн
не действуют как текущие. Корпус неизменен:79TCP/11XML +28ручных опор,
40биографических решений,пять типизированных кейсов рецепции.
Эта таблица не перевод,не текст биографии и не публичное разрешение цитирования.

### 12.1. Что именно выбрано

16TEXT_CANDIDATE — оригинальные лексические фрагменты из семи полных XML,
а не16новых источников. Семь RESEARCH_ONLY — решения не переносить веб-фразу
как готовую прямую цитату. Всего23позиции покрывают все10документов.
Все BLOCKED/PUBLICATION_HOLD;translationState=NOT_PREPARED.
Машинные записи сохраняют отдельно evidenceClass/accessState/locatorState/
rightsState/publicationState/holds,не подменяя состояние доступа классом.

| ID | Опора / будущие документы | Решение | Проверенный локатор | Чей голос и предел |
|---|---|---|---|---|
| Q-01 | GOV-03 / INTRO | TEXT_CANDIDATE | 18; XXXVII;protection and exclusions | Instrument of Government1653:печатная нормативная статьяXXXVII,не слова Чарнока. Защита ограничена civil injury / public peace и не распространяется на Popery / Prelacy; это не равноправие всех исповеданий. |
| Q-02 | BIO-17 / I | TEXT_CANDIDATE | 491; точный текстовый локус | Anthony Wood1691:сообщение о смерти/возрасте,не актовая запись. 27июля1680/около52лет — утверждение Wood, не приходской регистр |
| Q-03 | CORE-06 / I | TEXT_CANDIDATE | ненумерованный; точный текстовый локус | Анонимный титул The Sayings1680:сообщение о смерти/погребении,не слова умершего и не приходский регистр. Титул листка сообщает28июля; CONFLICT с Wood27июля; не выбирать один день без оговорки. |
| Q-04 | TXT-14 / II, VI | TEXT_CANDIDATE | ненумерованный; точный текстовый локус | Veel & Adams,To the Reader1682:редакторская оценка работы со Schoolmen,не прямая речь Чарнока. Редакторская характеристика переработки Schoolmen; не проверка каждого заимствования и не принятие их системы целиком |
| Q-05 | TXT-11 / II | TEXT_CANDIDATE | ненумерованный; точный текстовый локус | Veel & Adams,To the Reader1682:редакторское заявление о рукописях,не полученный автограф. Редакторы заявляют переписку авторских рукописей; Wichens/Ashton названы в соседних сносках, не установлены как редакторы доктрины |
| Q-06 | TXT-18 / III | TEXT_CANDIDATE | 20; точный текстовый локус | Чарнок,Churches Stability:рассуждение об авторе/времени Пс87. Пс87: автор и время оставлены неопределёнными перед церковно-пророческим чтением; не установленная история возникновения псалма |
| Q-07 | TXT-06 / IV | TEXT_CANDIDATE | 222; точный текстовый локус | Чарнок:рассуждение о неизменности/творении. Неизменность: реальность творения объясняется изменением твари, не субъекта-Бога; не тезис о нереальности истории |
| Q-08 | TXT-05 / IV | TEXT_CANDIDATE | 47; точный текстовый локус | Чарнок:различение интеллектуального и практического атеизма. Практический атеизм: интеллектуальное признание Бога противопоставлено отсутствию сердечной привязанности; не тождество современному атеизму |
| Q-09 | BIB-02 / V | TEXT_CANDIDATE | ненумерованный; Advertisement;Ashton | Edward Veel,Advertisement1699:о работе Ashton и соединении материалов. По Veel, Ashton соединял материалы из многих разрозненных бумаг; роль не исчерпывалась механической переписью. |
| Q-10 | TXT-13 / VI | TEXT_CANDIDATE | ненумерованный; точный текстовый локус | Veel & Adams,To the Reader1682:редакторская характеристика доктринального разбора. Редакторы описывают связь доктринального/полемического разбора с практическими выводами; не вся книга сведена к отвлечённой метафизике |
| Q-11 | TXT-08 / IV, VII | TEXT_CANDIDATE | 7; точный текстовый локус | Чарнок,Providence1680:знание и управление. Провидение — знание ради управления, а не пассивное наблюдение; доктринальный тезис Чарнока, не доказанный механизм любого события |
| Q-12 | BIB-07 / VII | TEXT_CANDIDATE | 8; Enmity;Rom8:7 exposition | Чарнок,Enmity,печатная передача1699:сотворённая/повреждённая природа. Автор отличает сотворённую человеческую природу от повреждённой; атрибуция его аргумента, не универсальный вывод об антропологии всех пуритан. |
| Q-13 | TXT-04 / VII | TEXT_CANDIDATE | 101; точный текстовый локус | Чарнок:лексический разбор Пс32,не подтверждение этимологий современной филологией. Пс32:1–2: лексическое построение грех/прощение; число категорий не удостоверяет правильности всех этимологий |
| Q-14 | BIB-08 / VIII | TEXT_CANDIDATE | 148; bookseller list after second discourse | Книготорговое объявление в объекте1699:не отзыв читателя и не авторская речь Чарнока. Издание рекламирует Works в двух фолиантах; это не идентификация даты/тиража рекламируемого комплекта. |
| Q-15 | FST-08 / REFERENCE | TEXT_CANDIDATE | ненумерованный; Scripture table;pagination warning | Примечание печатного Scripture table:составитель явно не установлен;не утверждать авторство Чарнока. Предупреждение о повторных номерах и first/second folio не доказывает два отдельных тома;для физической структуры нужен экземпляр/скан. |
| Q-16 | BIB-04 / REFERENCE | TEXT_CANDIDATE | ненумерованный; Advertisement;Enmity | Edward Veel,Advertisement1699:неизвестные ему время/место Enmity. Место и время проповеди Enmity не установлены самим издателем; предполагаемая связь с планом Original Sin остаётся его гипотезой. |
| Q-17 | CTX-02 / INTRO | RESEARCH_ONLY | III;Deprivation | Act of Uniformity1662:нормативная статья,не личное судебное дело Чарнока. Отказ/неисполнение в срок влечёт лишение духовных должностей с оговоркой lawful impediment; это норма, не доказательство изгнания Чарнока из конкретного прихода1662 |
| Q-18 | CTX-04 / INTRO | RESEARCH_ONLY | I–IV;Penalties | Conventicle Act1670:штрафные нормы,не доказательство конкретного преследования. Слушатель5шиллингов первый/10повтор;проповедник£20/£40;хозяин£20;не смешивать фунты и шиллинги;этим актом не доказан смертный приговор за посещение |
| Q-19 | REC-05 / VIII | RESEARCH_ONLY | https://indieskriflig.org.za/index.php/skriflig/article/view/1706/2867#22 | Jan Hoek2014:оценка автора статьи,не академический консенсус. Hoek предлагает богословскую коррекцию порядка рассмотрения атрибутов; это его оценка, не установленная ошибка Чарнока и не консенсус исследователей. |
| Q-20 | REC-08 / VIII | RESEARCH_ONLY | https://www.apuritansmind.com/puritan-favorites/stephen-charnock-1628-1680/ | William Symington по атрибуции web-транскрипции;оригинальный выпуск/страница не сверены. Условное сравнение с Bunyan/Howe/Baxter внутри панегирика;не абсолютное ранжирование и не независимо подтверждённая психология Чарнока. |
| Q-21 | CTX-09 / INTRO | RESEARCH_ONLY | pp476–477;Holdsworth,fn54–59 | VCH,история Emmanuel:вторичное описание среды,не личное свидетельство Чарнока. Арест Holdsworth в 1643 и изгнание в 1644 описывают университетскую среду, не деятельность Чарнока. |
| Q-22 | REC-02 / VIII | RESEARCH_ONLY | Explanatory Notes and Quaint Sayings;v18 | Spurgeon,антология Psalm103:выдержка с атрибуцией Чарноку,не вся система. Подписанная выдержка;совпадение с A32723,p699,различие comma/semicolon и оформления не скрывать |
| Q-23 | CTX-16 / REFERENCE | RESEARCH_ONLY | paragraph3;Onlyon16November1657 | DIB,Henry Cromwell:вторичная хронология должностей,не оригинал акта назначения. По Barnard, lord deputy с 16 November 1657; lord lieutenant / governor-general с 6 November 1658. Первичные акты назначений не приобретены. |

TEXT_CANDIDATE допускается только при A1/A2/A3,FULL_OBJECT_VERIFIED,
EXACT_LOCATOR_VERIFIED,PUBLICATION_ELIGIBLE для текста и исходном
PUBLICATION_HOLD без иных нерешённых флагов. Кандидат ещё не финальная цитата:
фрагмент может быть частью предложения,его атрибуция/контекст обязательны.
RESEARCH_ONLY имеет quoteText=null;нельзя получить «разрешённую цитату»
из её observedText,из права на доступ или из числа прошедших тестов.

Q-02/Q-03 — одна обязательная конфликтная пара. Указание даты по Wood не
разрешает умолчать об иной дате титула;две печати не доказывают независимость.
Q-09/10/14/15/16 нельзя превратить в слова Чарнока:это редакторский/печатный
паратекст. Q-04/05 также принадлежат предисловию Veel/Adams.

### 12.2. Архив, версия и права

У каждой TEXT_CANDIDATE registry-запись хранит source/commit/SHA256 XML,
member `xml/<TCP-id>.xml`,Drive-основу и TEI-локатор. Аудитор сверяет SHA
фактических XML,уникальность probe и TEI-страницу,затем соответствие плана.
Архивная ссылка не заменяет печатный локатор и сама по себе не даёт quote-safe.

Десять XML находятся в основе wave35 `116ByRONJ6-YyCRcOZwgoLs6IR7jBlCUs`;
B02133 дополнительно в проверенном delta wave38
`1UHwzDnIzE9DoqCaHMK1QCggO-3wK1MXp`. Конкретные sourceSHA — в JSON,
не во вновь изобретённом каталоге. Это CC0 keyboarded text,не права на
page images,не сверенный автограф и не новоподготовленный перевод.

Для REC-05/REC-08 есть только выбранные ручные извлечения в
`data/charnock-reception-extracts-v1.json` (тот же wave38delta).
SHA закрепляет эти байты,а не исходный HTML/PDF;rawObjectSha256=null.
Hoek:CC BY2.0 из собственного notice,но архив исходника не закрыт.
Symington/Spurgeon:RIGHTS_UNKNOWN;VCH:PRIVATE_STUDY_ONLY;
DIB:PRIVATE_STUDY_ONLY в текущем реестре. Первичные веб-нормы1662/1670
не превращены в полные архивированные объекты;их ARCHIVE/RIGHTS/PUBLICATION_HOLD
сохранены. Во всех случаях отсутствие публичной цитаты — решение,не пропуск
проверки и не заявление,что источник недостоверен.

### 12.3. Иллюстрации

ILL-01: `БИОГРАФИИ/atlas/biographies-shared.svg`;локально проверены SHASVG и
`data/biographies-shared-atlas-v1.json`. Точный текст подписи и хеши — в
illustrations[0]. Общая проекция не самостоятельный исторический источник:
C/FULL_OBJECT_VERIFIED/EXACT_LOCATOR_VERIFIED/RIGHTS_UNKNOWN/BLOCKED,
EVIDENCE_HOLD/RIGHTS_HOLD/PUBLICATION_HOLD. Она выбрана только для исследования,
не как одобренная иллюстрация публичной серии.

Внешние портреты/титульные листы/автографы не выбраны;их нет в плане под
видом полученных изображений. Не нужны новые AI-портреты или отдельные карты
для каждой главы. При выборе новых изображений потребуется новый объект,
точный владелец/лицензия,архив и отдельное решение о допустимости.

### 12.4. Итог и остаток

Условие checklist16§8.4 о локаторах/архиве/правах **выполнено как фиксация
всех решений в данном конечном плане**,а не как разрешение всех цитат.
Шестое условие —финальная непротиворечивая сборка/квитанция—остаётся открытым.
Проверка прав при самом авторинге и публикационное одобрение не выполнены.
