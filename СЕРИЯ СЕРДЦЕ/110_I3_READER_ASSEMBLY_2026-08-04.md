# Том 110. I.3 reader assembly — «Падшее сердце: Иеремия 17»

**Дата:** 2026-08-04  
**Authority ID:** `HEART-I3-READER-ASSEMBLY-2026-08-04`  
**Entry:** `HEART-BOOK-I3`  
**Final-order position:** `3 / 18`  
**Reader:** `109_READER_CHAPTER_I3_FALLEN_HEART_JEREMIAH_17_2026-08-04.md`  
**Machine receipt:** `data/heart-i3-reader-assembly-2026-08-04.json`

## 1. Решение

```text
I.3 STANDALONE FINAL-BOOK READER = ASSEMBLED
COMPOSITION MODE = PARAPHRASE-ONLY
ASSEMBLED READERS = 8 / 18
MISSING STANDALONE FINAL READERS = 10
ENTRY CITATION PASSES COMPLETE = 7 / 18
I.3 ENTRY CITATION PASS = OPEN
ASSEMBLED READER CITATION REVIEWS = 7 / 8
NEW DIRECT QUOTES APPROVED = 0
```

Эта транзакция собирает только самостоятельный reader I.3. Полный citation review Product owner, всех 224 quotation surfaces, 15 external links, трёх internal links и source/bibliography adequacy остаётся отдельной следующей транзакцией.

## 2. Immutable chain

```text
CURRENT V4 BLOB = d0ddea6cf1fc33dfab53ae9691aaf2d903d03b73
WHOLE-BOOK INTEGRATION BLOB = 06d67275c42c7a9c3bd0365044f358b4b7d7a895
HISTORICAL TRIAGE BLOB = de4d49cada15b231dfc31058aced4ec7a25928a2
I.1 READER BLOB = a5d35df1a87ab39abc8a85b1d84f1b1ab03da105
I.2 READER BLOB = 204545a59477d92839245800f56791466bf45349
PART II R3 BLOB = ae55b1fad5cccbdb623c551a14222e0f51ec084a
PART II R4 BLOB = f82780e13cb064aa89c06427d11a938662fc3ff8
I.3 READER BLOB = a958066bff3010f14540d67c900c362bd88de98a
PRODUCT BLOB = dc27b7a06d37321a068e971c02af4a0df3028ae6
```

```text
I.3 READER SHA-256 = 6d00cbd44a7d3540faddcbdbc03bfff1fd1c5a441c380392010f973d76ce92f9
PRODUCT SHA-256 = 4292f76ff3e2fa15dfd682b5a421400ce9a62ec391109b3109aef14d72b224f0
```

## 3. Product ownership

Primary Product owner:

```text
src/content/articles/krajne-li-isporcheno-serdce.mdx
```

I.3 owns the full Jeremiah 17 diagnosis and its gospel-qualified application. The chapter must not absorb:

- I.1 book-wide definition and canonical survey of heart;
- I.2 creation, mutable obedience and Genesis fall sequence;
- Part II unregenerate-struggle ceiling and four-soils diagnosis.

## 4. Selected assembly boundary

```text
SELECTED ASSEMBLY SECTIONS = 10
SELECTED SOURCE SURFACES = 62 / 193 / 6 / 1
```

The four numbers are:

```text
62 unique Scripture locators
193 quotation surfaces
6 external support links
1 internal support link
```

Selected sections:

```text
istoricheskiy-fon
greh-vyrezannyy
dva-obraza-doveriya
serdce-istochnik-samoobmana
otnositsya-li-k-veruyushchemu
chto-izmenilos
kak-greh-stanovitsya-strukturoy
kak-nelzya-primenyat
praktika
velikaya-nadezhda
```

```text
SELECTED SOURCE BYTES = 100152
SELECTED SCRIPTURE SET SHA-256 = ebad12d8f1a9d8c1f0c1bd5fd4790ee49fd24f0d4e04626e5cd785cfdb2b702b
SELECTED SECTION MANIFEST SHA-256 = 8804a6e3488a8c5feea6c264b8d08e6ec8530852f452167a73a2db4f1919ebc2
```

## 5. Historical full-owner boundary

```text
HISTORICAL OWNER SURFACES = 71 / 224 / 15 / 3
```

The four numbers are:

```text
71 Scripture locators
224 quotation surfaces
15 external links
3 internal article links
```

These historical counts remain authoritative for the future I.3 entry citation pass. Reader assembly does not reinterpret the selected ten sections as the complete citation-review surface.

Excluded from assembly ownership:

```text
sec-quiz
zaklyuchenie
istochniki
literatura
spravka
```

The exclusion means only that these sections were not used as reader composition owners. It does not delete them from the historical Product citation surface.

## 6. Reader result

```text
READER WORDS = 1708
READER SCRIPTURE LOCATORS = 13
READER QUOTATION SURFACES = 0
READER EXTERNAL LINKS = 0
READER INTERNAL LINKS = 0
READER FOOTNOTE DEFINITIONS = 0
PRODUCT QUOTATIONS COPIED = 0
PRODUCT LINKS COPIED = 0
LONG EXACT PRODUCT SENTENCES COPIED = 0
```

The reader preserves:

- the historical and covenant setting of Jeremiah 17;
- the movement from engraved sin to false trust and self-deception;
- the distinction between the primary diagnosis and its warning application to a believer;
- the reality of the new heart without perfectionism;
- concrete heart-examination under the gospel;
- the transition into Part II without duplicating its diagnosis.

## 7. Scanner false positives

The inventory scanner reports two source headings:

```text
Два источника доверия
Сердце как источник самообмана
```

They are ordinary theological chapter headings containing the lexical token `источник`. They are not source lists, bibliography headings or citation authorities.

```text
SOURCE-HEADING SCANNER RESULT = 2 LEXICAL FALSE POSITIVES
ACTUAL BIBLIOGRAPHY HEADINGS IN READER = 0
```

The permanent validator requires these exact two names, so a future change cannot silently convert the false-positive classification into a bibliography claim.

## 8. Ownership boundaries

```text
I.1 = definition and canonical survey
I.2 = creation and Genesis fall
I.3 = Jeremiah 17 exposition and gospel-qualified application
PART II = broader unregenerate struggle and four soils
```

I.3 may prepare the move into Part II but may not reproduce the R3 or R4 evidence dossiers as its own argument.

## 9. Permanent gate

Heart workflow must run:

```text
python3 scripts/validate_heart_i3_reader_assembly.py --product-root ../Product
```

Acceptance requires:

- all Research and Product immutable blobs;
- exact Product full SHA and reader SHA;
- historical `71 / 224 / 15 / 3` fresh scan;
- exact fifteen H2 sections;
- exact selected ten-section manifest;
- selected `62 / 193 / 6 / 1` fresh scan;
- reader `1708 / 13 / 0 / 0` fresh scan;
- exact scanner false-positive set;
- required reader headings and boundary markers;
- no Product sentence transfer at the material threshold;
- historical triage still `TRIAGED_OPEN`;
- current V4 still `7 / 18`;
- clean Research and Product checkouts.

## 10. Effective state

```text
HEART-BOOK-I3:
PRODUCT_SOURCE_ONLY
→ ASSEMBLED_READER_CITATION_OPEN
```

```text
ASSEMBLED READERS = 8 / 18
MISSING STANDALONE FINAL READERS = 10
ENTRY CITATION PASSES COMPLETE = 7 / 18
ENTRY CITATION PASSES OPEN = 11 / 18
PRODUCT SOURCE ONLY = 4
RESEARCH DOSSIER ONLY = 6
```

## 11. Fail-closed boundaries

```text
I.3 READER ASSEMBLED ≠ I.3 CITATION PASS COMPLETE
SELECTED 10 SECTIONS ≠ FULL CITATION SURFACE
PARAPHRASE-ONLY ≠ SOURCE CLAIMS ERASED
SCANNER SOURCE HEADING ≠ ACTUAL BIBLIOGRAPHY
8 READERS ≠ 8 COMPLETED CITATION PASSES
RESEARCH MERGE ≠ PRODUCT RELEASE
```

## 12. Remaining work

```text
I.3 ENTRY CITATION PASS = OPEN
MISSING STANDALONE FINAL READERS = 10
WHOLE-BOOK READER ASSEMBLY = INCOMPLETE
WHOLE-BOOK CITATION PASS = OPEN
WHOLE-BOOK TRANSITION / DEDUP PASS = OPEN
WHOLE-BOOK LINE EDIT = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT RELEASE = NOT CLAIMED
```

## 13. Next canonical transaction

Run a separate fail-closed I.3 entry citation pass over:

- immutable reader blob `a958066b...`;
- full Product owner blob `dc27b7a0...`;
- all `71` Scripture locators;
- all `224` quotation surfaces;
- all `15` external links;
- all `3` internal links;
- source and bibliography adequacy.

## 14. Final disposition

Authority `HEART-I3-READER-ASSEMBLY-2026-08-04` closes only the standalone reader assembly for I.3. Citation completion remains `7 / 18`; the I.3 citation pass is the required next transaction.
