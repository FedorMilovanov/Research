# Том 106. I.1 reader assembly — «Что Библия называет сердцем»

**Дата:** 2026-08-04  
**Authority ID:** `HEART-I1-READER-ASSEMBLY-2026-08-04`  
**Entry:** `HEART-BOOK-I1`  
**Final-order position:** `1 / 18`  
**Reader:** `105_READER_CHAPTER_I1_WHAT_BIBLE_CALLS_HEART_2026-08-04.md`  
**Machine receipt:** `data/heart-i1-reader-assembly-2026-08-04.json`

## 1. Решение

```text
I.1 READER ASSEMBLY = COMPLETE
I.1 ENTRY CITATION PASS = OPEN
ASSEMBLED READERS = 7 / 18
MISSING STANDALONE FINAL READERS = 11
ENTRY CITATION PASSES COMPLETE = 6 / 18
ASSEMBLED READER CITATION REVIEWS = 6 / 7
WHOLE-BOOK READER ASSEMBLY = INCOMPLETE
WHOLE-BOOK CITATION PASS = OPEN
NEW DIRECT QUOTES APPROVED = 0
PRODUCT RELEASE = NOT CLAIMED
```

I.1 переводится из `PRODUCT_SOURCE_ONLY` в `ASSEMBLED_READER`. Citation completion не увеличивается в assembly-транзакции.

## 2. Immutable chain

```text
BASELINE INTEGRATION GIT BLOB = 06d67275c42c7a9c3bd0365044f358b4b7d7a895
PRECEDING CURRENT V3 GIT BLOB = 407c8d78baa966a3336e7bd60edfa51178b74f32
HISTORICAL TRIAGE GIT BLOB = de4d49cada15b231dfc31058aced4ec7a25928a2
READER GIT BLOB = a5d35df1a87ab39abc8a85b1d84f1b1ab03da105
READER SHA-256 = 0da103d12bf6dca8bf4aced0c9734052c8d6ef3501ffea7c3368f42708398d24
PRODUCT GIT BLOB = acc12804f5b2450efebbb6e0b2cabd31066ef48c
PRODUCT SHA-256 = 50657f3473c06e16d75ffe740828a9311f642562e824f148113ae28ff9b03c07
PRODUCT COMMIT = 0fbe7d1ead9ebd1bea867418e254da438ec63329
```

## 3. Selected assembly boundary

Standalone reader собирается из семнадцати exact Product sections:

```text
nepravilno-slyshim
vnutrenniy-chelovek
serdce-dusha-duh
bog-trebuet-vsyo
bog-vidit-serdce
serdce-myslit
serdce-reshaet
serdce-lyubit
serdce-chuvstvuet
serdce-govorit
serdce-sovest
serdce-veruet
hranit-serdce
serdce-boga
karta-pisaniya
tverdo-ne-dubinkoy
vyhod
```

```text
SELECTED PRODUCT SECTIONS = 17
SELECTED PRODUCT BYTES = 34463
SELECTED PRODUCT SCRIPTURE REFERENCES = 126
SELECTED PRODUCT QUOTATION SURFACES = 80
SELECTED PRODUCT EXTERNAL LINKS = 0
SELECTED PRODUCT INTERNAL LINKS = 2
```

Каждый section pinned собственным scoped SHA-256, byte count, reference count, quotation count и link count в machine receipt.

## 4. Explicit exclusions

```text
padshee-serdce = I.3 / II fallen-heart diagnosis
novoe-serdce = III.1 new-heart promise
istochniki = future I.1 citation-pass bibliography scope
```

Excluded sections не удаляются из Product и остаются частью historical full owner row. Они исключены только из assembly ownership, чтобы I.1 не поглощала последующие главы и не подменяла отдельный citation review.

## 5. Historical full Product owner

Historical inventory сканирует полный Product-файл:

```text
HISTORICAL FULL PRODUCT OWNER SURFACES = 1
HISTORICAL FULL PRODUCT REFERENCES = 142
HISTORICAL FULL PRODUCT QUOTATION SURFACES = 98
HISTORICAL FULL PRODUCT EXTERNAL LINKS = 0
HISTORICAL FULL PRODUCT INTERNAL LINKS = 4
HISTORICAL INVENTORY ENTRY SHA-256 = 5acd1ed1ec0f50707a694332ae4ed56c274f31294d67956999f7eb7437f8250d
```

Selected assembly scope не переписывает historical citation scope. Будущий I.1 citation pass обязан классифицировать полный row `142 / 98 / 4`, включая bibliography и excluded transitions.

## 6. Reader composition

```text
COMPOSITION MODE = PARAPHRASE_ONLY
READER WORD COUNT = 1811
READER DETECTED SCRIPTURE REFERENCES = 20
READER QUOTATION SURFACES = 0
READER EXTERNAL LINKS = 0
READER INTERNAL LINKS = 0
READER FOOTNOTES = 0
READER DIRECT QUOTES = 0
NEW DIRECT QUOTES APPROVED = 0
```

Reader формирует самостоятельную начальную карту:

1. сердце не сводится к эмоциям;
2. сердце обозначает внутреннего человека перед Богом;
3. сердце, душа, дух и ум описывают одного человека с разных сторон;
4. сердце мыслит, решает, желает, чувствует, говорит, верует и действует;
5. совесть нуждается в просвещении и очищении;
6. Бог требует всего человека и видит скрытое направление;
7. определение нельзя использовать для отрицания тела, обстоятельств или страдания;
8. дальнейшие главы раскрывают сотворённое, падшее, обновлённое и прославленное состояние сердца.

## 7. Dedup ownership

```text
I.1 OWNS = complete biblical definition and functional map of the heart
I.2 OWNS = heart in Eden and original goodness
I.3 / II OWN = fallen-heart diagnosis and Jeremiah 17 treatment
I.4 OWNS = embodied inner person, habits, bodily influence and competence boundaries
III.1 OWNS = new-heart promise and regeneration transition
```

I.1 может обозначить эти дальнейшие темы только как переходы. Она не разворачивает их вместо собственных глав.

## 8. No-copy boundary

```text
PRODUCT QUOTATION SEGMENTS COPIED = 0
PRODUCT BLOCKQUOTES COPIED = 0
PRODUCT LONG EXACT SENTENCES COPIED = 0
PRODUCT LINKS COPIED = 0
NEW HISTORICAL CLAIMS = 0
NEW DIRECT QUOTES APPROVED = 0
```

Reader не переносит Product Scripture wording, lexical quotations, historical quotations или bibliography links.

## 9. State transition

```text
BEFORE:
I.1 = PRODUCT_SOURCE_ONLY
ASSEMBLED READERS = 6
MISSING READERS = 12
ENTRY CITATION PASSES COMPLETE = 6

AFTER:
I.1 = ASSEMBLED_READER
ASSEMBLED READERS = 7
MISSING READERS = 11
ENTRY CITATION PASSES COMPLETE = 6
```

## 10. Remaining reader assemblies

```text
HEART-BOOK-I3
HEART-BOOK-II
HEART-BOOK-III1
HEART-BOOK-III2
HEART-BOOK-III4
HEART-BOOK-IV
HEART-BOOK-V
HEART-BOOK-VI
HEART-BOOK-VII
HEART-BOOK-VIII
HEART-BOOK-IX
```

```text
MISSING STANDALONE FINAL READERS = 11
PRODUCT SOURCE ONLY = 5
RESEARCH DOSSIER ONLY = 6
```

## 11. Permanent gate

```text
I.1 ASSEMBLY VALIDATOR = scripts/validate_heart_i1_reader_assembly.py
```

Heart workflow обязан выполнять:

```text
python3 scripts/validate_heart_i1_reader_assembly.py --product-root ../Product
```

Validator проверяет:

- immutable Research/Product blobs;
- exact seventeen-section manifest;
- selected aggregate `126 / 80 / 2`;
- full historical aggregate `142 / 98 / 4`;
- exact three excluded sections;
- reader structure, word boundary and `20 / 0 / 0` scan;
- отсутствие material quotations, blockquotes и длинных exact Product sentences;
- historical integration, triage and current V3 states;
- effective counts `7 readers / 11 missing / 6 citation passes`;
- clean Research and Product checkouts.

## 12. Fail-closed boundaries

```text
I.1 READER ASSEMBLY COMPLETE ≠ I.1 CITATION PASS COMPLETE
SELECTED ASSEMBLY 126 / 80 / 2 ≠ HISTORICAL CITATION SCOPE 142 / 98 / 4
SEVEN READERS ASSEMBLED ≠ EIGHTEEN READERS ASSEMBLED
SIX CITATION PASSES ≠ WHOLE-BOOK CITATION PASS COMPLETE
PRODUCT SOURCE PRESENT ≠ PRODUCT RELEASE
```

## 13. Следующая транзакция

Следующий шаг — отдельный I.1 entry citation pass over the full historical Product owner row and the new reader. До него current citation completion остаётся `6 / 18`.

## 14. Final disposition

Authority `HEART-I1-READER-ASSEMBLY-2026-08-04` закрывает только standalone assembly первой главы. Whole-book assembly, citation pass, transition/dedup, line edit, manuscript bundle и Product release остаются открытыми.
