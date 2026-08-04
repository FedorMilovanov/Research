# Том 91. Entry-level citation disposition triage — «СЕРИЯ СЕРДЦЕ»

**Дата:** 2026-08-04  
**Authority ID:** `HEART-ENTRY-CITATION-DISPOSITIONS-2026-08-04`  
**Machine registry:** `data/heart-entry-citation-dispositions-2026-08-04.json`  
**Validator:** `scripts/validate_heart_entry_citation_dispositions.py`

```text
DISPOSITION TRIAGE COVERAGE = 18 / 18
ENTRY CITATION PASS COMPLETE = 0 / 18
OPEN ENTRIES = 18 / 18
SCRIPTURE REVIEW REQUIRED = 18 / 18
QUOTATION REVIEW REQUIRED = 18 / 18
EXTERNAL-LINK REVIEW REQUIRED = 12 / 18
SOURCE-HEADING / BIBLIOGRAPHY OWNER REQUIRED = 7 / 18
READER ASSEMBLY REQUIRED = 14 / 18
NEW DIRECT QUOTES APPROVED = 0
WHOLE-BOOK CITATION PASS = OPEN
PRODUCT RELEASE = NOT CLAIMED
```

## 1. Что закрывает транзакция

Citation inventory уже зафиксировал обнаруженные поверхности. Этот слой не повторяет поиск и не выдаёт автоматическое одобрение. Он присваивает каждой из 18 глав один review lane, детерминированный набор blockers и следующий канонический шаг. Каждая строка связана SHA-256 с полной исходной inventory-entry.

Закрывается только полнота triage: ни одна глава больше не остаётся без явного citation-disposition lane.

## 2. Три review lane

1. `ASSEMBLED_READER_ENTRY_REVIEW` — четыре готовых reader manuscripts; можно начинать фактическую классификацию цитат, нормализацию ссылок Писания и проверку locators.
2. `PRODUCT_SOURCE_TO_READER_AND_CITATION_REVIEW` — восемь Product-source owners; сначала нужен book-reader assembly, затем entry citation pass.
3. `DOSSIER_TO_READER_AND_CITATION_REVIEW` — шесть Research dossiers; evidence boundaries сохраняются, но reader manuscript ещё не собран.

## 3. Entry matrix

| # | Entry | State | Scripture | External | Quotes | Lane |
|---:|---|---|---:|---:|---:|---|
| 1 | `HEART-BOOK-I1` — I.1 Что Библия называет сердцем | `PRODUCT_SOURCE_ONLY` | 142 | 0 | 98 | Product → reader |
| 2 | `HEART-BOOK-I2` — I.2 Сердце в Эдеме | `ASSEMBLED_READER` | 23 | 0 | 24 | assembled review |
| 3 | `HEART-BOOK-I3` — I.3 Падшее сердце: Иеремия 17 | `PRODUCT_SOURCE_ONLY` | 71 | 15 | 224 | Product → reader |
| 4 | `HEART-BOOK-I4` — I.4 Внутренний человек и телесная жизнь | `PRODUCT_SOURCE_ONLY` | 171 | 97 | 216 | Product → reader |
| 5 | `HEART-BOOK-II` — II Диагноз падшего сердца | `RESEARCH_DOSSIER_ONLY` | 118 | 80 | 437 | dossier → reader |
| 6 | `HEART-BOOK-III1` — III.1 Обещание нового сердца | `PRODUCT_SOURCE_ONLY` | 30 | 0 | 67 | Product → reader |
| 7 | `HEART-BOOK-III2` — III.2 Рождение свыше и обновление | `RESEARCH_DOSSIER_ONLY` | 115 | 67 | 609 | dossier → reader |
| 8 | `HEART-BOOK-III3` — III.3 Сокрушённое сердце: покаяние | `ASSEMBLED_READER` | 20 | 0 | 42 | assembled review |
| 9 | `HEART-BOOK-III4` — III.4 Сердце и Дух | `PRODUCT_SOURCE_ONLY` | 136 | 30 | 289 | Product → reader |
| 10 | `HEART-BOOK-IV` — IV Сердце и слово Божие | `RESEARCH_DOSSIER_ONLY` | 65 | 36 | 225 | dossier → reader |
| 11 | `HEART-BOOK-V` — V Сердце в борьбе с грехом | `PRODUCT_SOURCE_ONLY` | 203 | 120 | 755 | Product → reader |
| 12 | `HEART-BOOK-VI` — VI Сердце ученика и фарисея | `RESEARCH_DOSSIER_ONLY` | 123 | 28 | 274 | dossier → reader |
| 13 | `HEART-BOOK-VII` — VII Сердце в страдании и унынии | `PRODUCT_SOURCE_ONLY` | 47 | 20 | 171 | Product → reader |
| 14 | `HEART-BOOK-VIII` — VIII Взирая на славу Христа | `RESEARCH_DOSSIER_ONLY` | 66 | 1 | 447 | dossier → reader |
| 15 | `HEART-BOOK-IX` — IX Христос Апокалипсиса и сердце | `RESEARCH_DOSSIER_ONLY` | 111 | 7 | 207 | dossier → reader |
| 16 | `HEART-BOOK-X1` — X.1 Суд сердца: два воскресения | `ASSEMBLED_READER` | 40 | 0 | 33 | assembled review |
| 17 | `HEART-BOOK-X2` — X.2 Освобождённое сердце | `PRODUCT_SOURCE_ONLY` | 50 | 0 | 59 | Product → reader |
| 18 | `HEART-BOOK-X3` — X.3 Заключительная надежда | `ASSEMBLED_READER` | 115 | 7 | 209 | assembled review |

## 4. Blocker semantics

- `SCRIPTURE_VERSION_ABBREVIATION_CONTEXT_REVIEW_REQUIRED` означает, что обнаруженный token ещё не подтверждает правильность ссылки, диапазона, сокращения или версии перевода.
- `QUOTATION_CLASSIFICATION_LOCATOR_REVIEW_REQUIRED` означает, что blockquote или кавычки ещё не классифицированы как Писание, историческая цитата, термин или редакционная речь.
- `EXTERNAL_LINK_ADEQUACY_STABILITY_REVIEW_REQUIRED` требует проверки качества, доступности, устойчивости и соответствия источника конкретному утверждению.
- `SOURCE_HEADING_OR_BIBLIOGRAPHY_OWNER_REQUIRED` фиксирует отсутствие явного governed source/bibliography heading в scanned scope.
- `READER_MANUSCRIPT_ASSEMBLY_REQUIRED_BEFORE_FINAL_CITATION_PASS` запрещает объявлять citation closure по dossier или Product source до появления финального book-reader текста.

## 5. Приоритет следующей фактической проверки

Начинать нужно с четырёх уже собранных readers, потому что только там текст главы существует в финальной reader-форме:

1. I.2 `Сердце в Эдеме`;
2. III.3 `Сокрушённое сердце: покаяние`;
3. X.1 `Суд сердца: два воскресения`;
4. X.3 `Заключительная надежда`.

Это порядок review readiness, а не богословской важности. Ни одна из четырёх глав пока не получает citation pass автоматически.

## 6. Fail-closed границы

```text
TRIAGED_OPEN ≠ CITATION PASS COMPLETE
INVENTORY ENTRY SHA MATCH ≠ REFERENCE VERIFIED
REVIEW LANE ASSIGNED ≠ READER ASSEMBLED
QUOTATION SURFACE COUNT ≠ DIRECT QUOTE COUNT
EXTERNAL LINK COUNT ≠ ADEQUATE SOURCE COUNT
```

Запрещено:

- массово переводить 18 строк в complete;
- считать Product publication финальным book-reader assembly;
- добавлять новые прямые цитаты без locator/version/context;
- переписывать manuscripts по результатам одной автоматической классификации;
- закрывать whole-book citation pass до отдельного подтверждения каждой entry.

## 7. Что закрыто

```text
EIGHTEEN-ENTRY DISPOSITION COVERAGE = CLOSED
REVIEW LANE ASSIGNMENT = CLOSED
BLOCKER CLASSIFICATION COVERAGE = CLOSED
ENTRY-TO-INVENTORY SHA BINDING = CLOSED
ENTRY CITATION PASS COMPLETE = 0 / 18
```

## 8. Что осталось

```text
ASSEMBLED-READER ENTRY REVIEWS = 0 / 4
PRODUCT-SOURCE READER ASSEMBLIES = 0 / 8
DOSSIER-TO-READER ASSEMBLIES = 0 / 6
SCRIPTURE NORMALIZATION REVIEWS = 0 / 18
QUOTATION CLASSIFICATION REVIEWS = 0 / 18
EXTERNAL-LINK ADEQUACY REVIEWS = 0 / 12
SOURCE-HEADING / BIBLIOGRAPHY OWNER RESOLUTIONS = 0 / 7
ENTRY CITATION PASS COMPLETE = 0 / 18
WHOLE-BOOK CITATION PASS = OPEN
```

## 9. Decision

Authority `HEART-ENTRY-CITATION-DISPOSITIONS-2026-08-04` closes deterministic triage coverage for all eighteen entries. Every entry remains `TRIAGED_OPEN`; citation completion remains `0 / 18`; new direct-quote approval remains zero. The next canonical lane is the first actual assembled-reader citation review, beginning with I.2.
