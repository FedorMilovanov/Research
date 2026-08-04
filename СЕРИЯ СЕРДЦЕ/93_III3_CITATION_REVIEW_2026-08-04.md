# Том 93. III.3 citation review — «Сокрушённое сердце: покаяние»

**Дата:** 2026-08-04  
**Authority ID:** `HEART-III3-CITATION-REVIEW-2026-08-04`  
**Entry:** `HEART-BOOK-III3`  
**Final-order position:** `8 / 18`  
**Reader authority:** `80_READER_CHAPTER_III3_BROKEN_HEART_REPENTANCE_2026-08-02.md`  
**Evidence owner:** `76_P0_BROKEN_HEART_REPENTANCE_2026-08-02.md`  
**Machine receipt:** `data/heart-iii3-citation-review-2026-08-04.json`

## 1. Решение

```text
III.3 ENTRY CITATION PASS = COMPLETE
WHOLE-BOOK ENTRY CITATION PASSES = 2 / 18
WHOLE-BOOK ENTRY CITATION PASSES OPEN = 16 / 18
ASSEMBLED READER CITATION REVIEWS = 2 / 4
WHOLE-BOOK CITATION PASS = OPEN
```

III.3 закрывается как отдельный entry-level citation pass. Исторический disposition snapshot остаётся неизменённым и продолжает свидетельствовать предыдущее состояние `TRIAGED_OPEN`; настоящий том является последующим overlay.

## 2. Immutable source chain

```text
READER GIT BLOB = f7a8fe5032ceeb26d9acc4fd6f248ba5f92de29d
DOSSIER GIT BLOB = d54e86796a38f34a656829011ed17948cf6edb8f
P0 REGISTRY GIT BLOB = 71c26fed5de96cead1e2f8dcdedbfefc05f3e628
INVENTORY ENTRY SHA-256 = 91ccbce5aa0bf8a22c75af4ab984b09dd8928623666eaef30ded88cbb1fe4c73
```

Reader, evidence dossier и P0 registry не переписываются этой транзакцией. Validator обязан вычислить Git blob каждого immutable source и остановиться при любом drift.

## 3. Scripture governance

```text
READER DETECTED REFERENCES = 1
DOSSIER DETECTED REFERENCES = 20
SCRIPTURE REFERENCES GOVERNED = 20 / 20
TRANSLATION VERSION IDENTIFIER REQUIRED = FALSE
```

Reader содержит prose navigation к Псалму 50. Evidence dossier содержит канонические locator-ссылки и экзегетическую навигацию по покаянию, включая Псалом 50, 2 Кор. 7, Лк. 3, Деян. 20 и 26, Евр. 12, Мф. 27, Мк. 1, Лк. 19 и Иак. 5.

Ни reader, ни dossier не утверждают verbatim passage конкретного русского перевода как новую прямую цитату. Поэтому отсутствие translation-version identifier в этой главе не является незакрытым blocker.

## 4. Quotation-surface classification

```text
READER INLINE QUOTATION SEGMENTS = 16
READER MARKDOWN BLOCKQUOTES = 2
DOSSIER INLINE QUOTATION SEGMENTS = 19
DOSSIER MARKDOWN BLOCKQUOTES = 5
QUOTATION SURFACES CLASSIFIED = 42 / 42
READER DIRECT QUOTES = 0
DOSSIER DIRECT QUOTES APPROVED = 0
APPROVED DIRECT-QUOTE TRANSFER TO READER = 0
```

Кавычечные поверхности состоят из авторских формул, пастырских shorthand-формулировок, риторической речи, канонического пересказа, технических терминов и примеров запрещённых или недостаточных формулировок. Markdown blockquotes в reader и dossier являются собственными нормативными формулами проекта, а не перенесёнными историческими цитатами.

Наличие кавычек или blockquote-разметки само по себе не превращает поверхность в approved direct quote.

## 5. Governing claim and source chain

Immutable reader и dossier содержат диапазон claims `REP-01…REP-08`. Machine validator требует этот exact range marker, затем выбирает в P0 registry ровно восемь claims с этими ID и проверяет их binding к `HEART-P0-REPENTANCE`.

```text
GOVERNING DOSSIER ID = HEART-P0-REPENTANCE
GOVERNING CLAIMS = REP-01 … REP-08
CLAIMS REVIEWED = 8 / 8
CLAIMS CLOSED OR BOUNDARY-CLOSED = 8 / 8
GOVERNING SOURCE RECORDS = 7 / 7
```

Используемые source records:

- `HP0-S01` — MorphHB / WLC textual control;
- `HP0-S03` — SBL Greek New Testament;
- `HP0-S04` — Westminster Confession of Faith;
- `HP0-S07` — Second London Baptist Confession 1689, chapter 15;
- `HP0-S12` — Calvin, *Institutes* III.3;
- `HP0-S14` — Owen, exposition of Psalm 130;
- `HP0-S15` — Watson, *Body of Divinity*.

Каждый из восьми REP claims обязан сохранять status `CLOSED` или `BOUNDARY_CLOSED`, support IDs, locators и publication boundary. Каждый используемый source record обязан иметь URL и locator.

## 6. Entry blockers

```text
SCRIPTURE NORMALIZATION BLOCKER = RESOLVED
QUOTATION CLASSIFICATION BLOCKER = RESOLVED
EXTERNAL LINK BLOCKER APPLICABLE = FALSE
SOURCE-HEADING / BIBLIOGRAPHY OWNER BLOCKER APPLICABLE = FALSE
READER ASSEMBLY BLOCKER APPLICABLE = FALSE
REMAINING ENTRY BLOCKERS = 0
```

III.3 уже имеет отдельный assembled reader и governing evidence dossier. В двух owner surfaces отсутствуют external links, internal article links, footnote definitions и HTML blockquotes. Единственный source heading находится в evidence dossier и не требует отдельного bibliography-owner repair.

## 7. Mutation boundary

```text
READER MANUSCRIPT CHANGES = 0
EVIDENCE DOSSIER CHANGES = 0
P0 REGISTRY CHANGES = 0
NEW HISTORICAL CLAIMS = 0
NEW DIRECT QUOTES APPROVED = 0
PRODUCT CHANGES = 0
```

Закрытие entry pass основано на проверке уже существующей immutable source chain. Оно не создаёт новой редакции главы и не переносит dossier language в reader.

## 8. Permanent gate

Heart workflow обязан выполнить:

```text
python3 scripts/validate_heart_iii3_entry_citation_pass.py --product-root ../Product
```

Acceptance требует:

- immutable blob equality для reader, dossier и P0 registry;
- exact claim-range markers `REP-01…REP-08` в reader и dossier;
- fresh scan exact Product snapshot;
- reader/dossier/union Scripture counts `1 / 20 / 20`;
- reader quotation counts `16 inline + 2 blockquotes`;
- dossier quotation counts `19 inline + 5 blockquotes`;
- quotation-surface total `42`;
- отсутствие external/internal links, footnotes и HTML blockquotes;
- zero-direct-quote declarations в reader и dossier;
- exact governing P0 claim and source sets;
- полную claim/source/locator/publication-boundary chain;
- исторический triage state `TRIAGED_OPEN` без переписывания snapshot;
- preceding I.2 pass `1 / 18`;
- текущий composed count `2 / 18`;
- чистые Research и Product checkouts.

Permanent CI не должен собирать diagnostic artifact, использовать `--write`, изменять source files или очищать следы собственной записи перед cleanliness-check.

## 9. Publication boundaries

```text
III.3 ENTRY CITATION PASS COMPLETE ≠ WHOLE-BOOK CITATION PASS COMPLETE
TWO COMPLETED ENTRIES ≠ EIGHTEEN COMPLETED ENTRIES
REFERENCE LOCATOR ≠ VERBATIM TRANSLATION QUOTE
AUTHORIAL BLOCKQUOTE ≠ HISTORICAL DIRECT QUOTE
CLAIM SUPPORT PRESENT ≠ WHOLE-BOOK LINE EDIT COMPLETE
RESEARCH MERGE ≠ PRODUCT RELEASE
```

## 10. Что остаётся открытым

```text
ENTRY CITATION PASSES OPEN = 16 / 18
ASSEMBLED READER CITATION REVIEWS OPEN = 2 / 4
MISSING READER ASSEMBLIES = 14
WHOLE-BOOK TRANSITION / DEDUP PASS = OPEN
WHOLE-BOOK LINE EDIT = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT RELEASE = NOT CLAIMED
```

Следующая canonical entry transaction — X.1 `Суд сердца: два воскресения`, используя exact reader, P0 judgment dossier и governing source group.

## 11. Final disposition

Authority `HEART-III3-CITATION-REVIEW-2026-08-04` закрывает citation pass только для III.3. Whole-book completion становится `2 / 18`; все остальные publication and release gates остаются fail-closed.
