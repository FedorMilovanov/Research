# Том 94. X.1 citation review — «Суд сердца: два воскресения»

**Дата:** 2026-08-04  
**Authority ID:** `HEART-X1-CITATION-REVIEW-2026-08-04`  
**Entry:** `HEART-BOOK-X1`  
**Final-order position:** `16 / 18`  
**Reader authority:** `81_READER_CHAPTER_X1_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md`  
**Evidence owner:** `77_P0_JUDGMENT_TWO_RESURRECTIONS_2026-08-02.md`  
**Machine receipt:** `data/heart-x1-citation-review-2026-08-04.json`

## 1. Решение

```text
X.1 ENTRY CITATION PASS = COMPLETE
WHOLE-BOOK ENTRY CITATION PASSES = 3 / 18
WHOLE-BOOK ENTRY CITATION PASSES OPEN = 15 / 18
ASSEMBLED READER CITATION REVIEWS = 3 / 4
WHOLE-BOOK CITATION PASS = OPEN
```

X.1 закрывается как отдельный entry-level citation pass. Исторический disposition registry остаётся неизменённым и продолжает фиксировать предыдущее состояние `TRIAGED_OPEN`; настоящий том является последующим composed overlay.

## 2. Immutable source chain

```text
READER GIT BLOB = 0fe2b234c1249d1dc6f1e37103f63c850fb41b83
DOSSIER GIT BLOB = ae5c16ef129892e169596fbd90490b5d4f64aa43
P0 REGISTRY GIT BLOB = 71c26fed5de96cead1e2f8dcdedbfefc05f3e628
INVENTORY ENTRY SHA-256 = 7e27c913e38325dc86a2c35220a7f069e4c7c53fca7dac5c750dbfbf09659e99
```

Reader, evidence dossier и P0 registry этой транзакцией не переписываются. Permanent validator обязан остановиться при любом blob drift.

## 3. Scripture governance

```text
READER DETECTED REFERENCES = 3
DOSSIER DETECTED REFERENCES = 37
SCRIPTURE REFERENCES GOVERNED = 40 / 40
TRANSLATION VERSION IDENTIFIER REQUIRED = FALSE
```

Reader использует каноническую prose navigation прежде всего к Ин. 5, 1 Кор. 15 и Рим. 8. Evidence dossier расширяет locator-карту текстами о промежуточном состоянии, всеобщем воскресении, двух исходах, суде по делам, книге жизни и надежде во Христе.

Ни reader, ни dossier не утверждают verbatim passage конкретного русского перевода как новую прямую цитату. Поэтому translation-version identifier для этой entry не требуется.

## 4. Quotation-surface classification

```text
READER INLINE QUOTATION SEGMENTS = 6
READER MARKDOWN BLOCKQUOTES = 2
DOSSIER INLINE QUOTATION SEGMENTS = 20
DOSSIER MARKDOWN BLOCKQUOTES = 5
QUOTATION SURFACES CLASSIFIED = 33 / 33
READER DIRECT QUOTES = 0
DOSSIER DIRECT QUOTES APPROVED = 0
APPROVED DIRECT-QUOTE TRANSFER TO READER = 0
```

Reader surfaces состоят из пастырских shorthand-формул, риторических вопросов и собственных итоговых формул главы. Dossier surfaces включают технические выражения, канонические парафразы, нормативные авторские формулы и примеры чрезмерных или запрещённых выводов.

Markdown blockquotes являются authorial project formulas. Разметка blockquote или наличие кавычек не считается approved historical/source direct quote.

## 5. Governing claim and source chain

Immutable reader и dossier содержат диапазон claims `JUDG-01…JUDG-10`. Permanent validator требует этот exact range marker, затем выбирает в P0 registry ровно десять claims с этими ID и проверяет их binding к `HEART-P0-JUDGMENT`.

```text
GOVERNING DOSSIER ID = HEART-P0-JUDGMENT
GOVERNING CLAIMS = JUDG-01 … JUDG-10
CLAIMS REVIEWED = 10 / 10
CLAIMS CLOSED OR BOUNDARY-CLOSED = 10 / 10
GOVERNING SOURCE RECORDS = 8 / 8
```

Используемые source records:

- `HP0-S03` — SBL Greek New Testament;
- `HP0-S04` — Westminster Confession of Faith;
- `HP0-S08` — Second London Baptist Confession 1689, state after death and resurrection;
- `HP0-S09` — Second London Baptist Confession 1689, last judgment;
- `HP0-S13` — Calvin, *Institutes* III.25;
- `HP0-S15` — Watson, *Body of Divinity*;
- `HP0-S16` — Owen, *Vindiciae Evangelicae*, chapter XXXV;
- `HP0-S17` — Calvin, commentary on the Synoptic Gospels.

Каждый JUDG claim обязан сохранять status `CLOSED` или `BOUNDARY_CLOSED`, support IDs, locators и publication boundary. Каждый используемый source record обязан иметь URL и locator.

## 6. Entry blockers

```text
SCRIPTURE NORMALIZATION BLOCKER = RESOLVED
QUOTATION CLASSIFICATION BLOCKER = RESOLVED
EXTERNAL LINK BLOCKER APPLICABLE = FALSE
SOURCE-HEADING / BIBLIOGRAPHY OWNER BLOCKER APPLICABLE = FALSE
READER ASSEMBLY BLOCKER APPLICABLE = FALSE
REMAINING ENTRY BLOCKERS = 0
```

X.1 уже имеет отдельный assembled reader и governing evidence dossier. В двух owner surfaces отсутствуют external links, internal article links, footnote definitions и HTML blockquotes. Единственный source heading находится в dossier и не требует отдельного bibliography-owner repair.

## 7. Mutation boundary

```text
READER MANUSCRIPT CHANGES = 0
EVIDENCE DOSSIER CHANGES = 0
P0 REGISTRY CHANGES = 0
NEW HISTORICAL CLAIMS = 0
NEW DIRECT QUOTES APPROVED = 0
PRODUCT CHANGES = 0
```

Entry pass закрывается на уже существующей immutable source chain. Dossier wording не переносится автоматически в reader, а никакие новые эсхатологические схемы или исторические claims не добавляются.

## 8. Permanent gate

Heart workflow обязан выполнять:

```text
python3 scripts/validate_heart_x1_entry_citation_pass.py --product-root ../Product
```

Acceptance требует:

- immutable blob equality reader, dossier и P0 registry;
- exact claim-range markers `JUDG-01…JUDG-10`;
- fresh scan exact Product snapshot;
- Scripture counts `3 reader / 37 dossier / 40 unique`;
- reader quotation counts `6 inline + 2 blockquotes`;
- dossier quotation counts `20 inline + 5 blockquotes`;
- quotation-surface total `33`;
- отсутствие external/internal links, footnotes и HTML blockquotes;
- zero-direct-quote declarations reader и dossier;
- exact ten-claim and eight-source sets;
- полную claim/source/locator/publication-boundary chain;
- historical triage state `TRIAGED_OPEN`;
- preceding I.2 и III.3 completed passes;
- preceding composed count `2 / 18` и текущий `3 / 18`;
- чистые Research и Product checkouts.

Permanent CI не должен собирать diagnostic artifacts, использовать `--write`, изменять source files или маскировать собственные записи cleanup-командами.

## 9. Publication boundaries

```text
X.1 ENTRY CITATION PASS COMPLETE ≠ WHOLE-BOOK CITATION PASS COMPLETE
THREE COMPLETED ENTRIES ≠ EIGHTEEN COMPLETED ENTRIES
REFERENCE LOCATOR ≠ VERBATIM TRANSLATION QUOTE
AUTHORIAL BLOCKQUOTE ≠ HISTORICAL DIRECT QUOTE
JUDGMENT CLAIM SUPPORT ≠ SYSTEMATIC TIMELINE CLAIM
RESEARCH MERGE ≠ PRODUCT RELEASE
```

## 10. Что остаётся открытым

```text
ENTRY CITATION PASSES OPEN = 15 / 18
ASSEMBLED READER CITATION REVIEWS OPEN = 1 / 4
MISSING READER ASSEMBLIES = 14
WHOLE-BOOK TRANSITION / DEDUP PASS = OPEN
WHOLE-BOOK LINE EDIT = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT RELEASE = NOT CLAIMED
```

Следующая canonical entry transaction — X.3 `Заключительная надежда`, последняя из четырёх уже assembled reader entries.

## 11. Final disposition

Authority `HEART-X1-CITATION-REVIEW-2026-08-04` закрывает citation pass только для X.1. Whole-book completion становится `3 / 18`; все остальные publication and release gates остаются fail-closed.
