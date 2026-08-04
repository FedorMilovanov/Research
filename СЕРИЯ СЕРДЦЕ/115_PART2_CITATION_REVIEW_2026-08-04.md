# Том 115. Part II citation review — «Диагноз падшего сердца»

**Дата:** 2026-08-04  
**Authority ID:** `HEART-PART2-CITATION-REVIEW-2026-08-04`  
**Entry:** `HEART-BOOK-II`  
**Reader:** `113_READER_CHAPTER_II_FALLEN_HEART_DIAGNOSIS_2026-08-04.md`  
**Assembly receipt:** `data/heart-part2-reader-assembly-2026-08-04.json`  
**Machine review:** `data/heart-part2-citation-review-2026-08-04.json`

## Decision

```text
PART II ENTRY CITATION PASS = COMPLETE
ENTRY CITATION PASSES COMPLETE = 9 / 18
ENTRY CITATION PASSES OPEN = 9 / 18
ASSEMBLED READERS = 9 / 18
ASSEMBLED READER CITATION REVIEWS = 9 / 9
MISSING STANDALONE FINAL READERS = 9
PRODUCT SOURCE LINK REPAIRS REQUIRED = 3
NEW DIRECT QUOTES APPROVED = 0
```

## Immutable chain

```text
PART II ASSEMBLY RECEIPT BLOB = 7fe129945caa023e796e592d0c8fc07a01a89f69
CURRENT V5 BLOB = 2ba8c381e636a9f1148fa30e3f010d595feb42a6
HISTORICAL TRIAGE BLOB = de4d49cada15b231dfc31058aced4ec7a25928a2
SOURCE CLOSURE REGISTRY BLOB = c67243b7f180bd84c86a0a52b9134844fb221d90
R3 BLOB = ae55b1fad5cccbdb623c551a14222e0f51ec084a
R4 BLOB = f82780e13cb064aa89c06427d11a938662fc3ff8
PART II READER BLOB = 4cca195d034c70a7d3d6c3dd8edc9a04fcffcc20
```

## Full review surface

```text
SCRIPTURE LOCATORS GOVERNED = 118 / 118
QUOTATION SURFACES CLASSIFIED = 437 / 437
EXTERNAL LINKS DISPOSITIONED = 80 / 80
UNRESOLVED INTERNAL PATHS = 1
```

The review covers the complete R3/R4 dossier union, not only the prose used in the assembled reader.

## Dossier-role taxonomy

```text
EXEGETICAL SCRIPTURE OR LEXICAL SURFACES = 178
ATTRIBUTED WITNESS OR QUOTE-BANK SURFACES = 194
EDITORIAL, STRUCTURAL OR CAUTION SURFACES = 65
TOTAL = 437
```

```text
SOURCE SURFACE MANIFEST SHA-256 = d51a1de91ac865bf81c485797092637ff39d3b50ca59dbbaddec85e9cd2cb804
CLASSIFIED MANIFEST SHA-256 = f7cf291e9cecb4a3a9d5aa28ae0185982c54c477448ce3e1b3752501379538cc
ROLE MAP SHA-256 = be48bfb08f60853e858217c3df3a3456dc1b9a7d8235aed394ca5c39f3e65894
SECTION SUMMARY SHA-256 = b0932037fbc01a403aa22347d2c3065b6115a1513b3747a4b46fdeb926e6adf7
```

This taxonomy governs the role each surface plays in the dossiers. It does not promote every attributed or exegetical surface to a reader-facing direct quotation.

## External-link dispositions

```text
DOSSIER VERIFIED OR SAFE-CLOSURE SOURCES = 34
DOSSIER SUPPORT RECORDS / NO READER TRANSFER = 31
DOSSIER OPEN OR DIRECT-QUOTE HOLDS = 15
URL HOLDS RETAINED = 15
TOTAL = 80
```

The status is derived from exact dossier context, including existing `ВЕРИФИЦИРОВАНО`, `SAFE CLOSURE`, candidate, open-question and no-direct-quote markers.

```text
EXTERNAL LINK SET SHA-256 = f5ce26d3f27bf9e6aa2c87e625d9b91875d580f296d02d80e974a27dd279187f
DISPOSITION REGISTRY SHA-256 = 0811af3bd3865bc4dfd36f7d1f62048cdbd85f73c243512eb33410b07bbf8fe1
```

No URL is copied into the reader. A hold is a complete disposition, not an approval.

## Internal path

The historical R3 surface contains:

```text
/articles/opinion/
```

No matching `src/content/articles/opinion.mdx` exists on the pinned Product commit.

```text
INTERNAL PATH STATUS = UNRESOLVED GENERIC PATH
READER TRANSFER = FALSE
```

The path is not represented as a resolved Product article target.

## Reader result

```text
READER SCRIPTURE LOCATORS = 20
READER QUOTATION SURFACES = 0
READER EXTERNAL LINKS = 0
READER INTERNAL LINKS = 0
READER FOOTNOTES = 0
SOURCE SURFACES COPIED = 0
SOURCE LINKS COPIED = 0
NEW DIRECT QUOTES APPROVED = 0
```

## Source-status boundary

R3/R4 remain unchanged. The review preserves:

- verified and safe-closure markers;
- candidate and open-question markers;
- no-direct-quote closures;
- all unresolved source candidates.

```text
UNRESOLVED SOURCE CANDIDATES PROMOTED = 0
BULK DIRECT-QUOTE APPROVAL = FALSE
```

## Effective state

```text
HEART-BOOK-II:
ASSEMBLED_READER_CITATION_OPEN
→ ENTRY_CITATION_PASS_COMPLETE
```

```text
ENTRY CITATION PASSES COMPLETE = 9 / 18
ENTRY CITATION PASSES OPEN = 9 / 18
ASSEMBLED READERS = 9 / 18
ASSEMBLED READER CITATION REVIEWS = 9 / 9
MISSING STANDALONE FINAL READERS = 9
PRODUCT SOURCE ONLY = 4
RESEARCH DOSSIER ONLY = 5
```

## Permanent gate

```text
python3 scripts/validate_heart_part2_entry_citation_pass.py --product-root ../Product
```

The validator independently re-scans R3, R4 and the reader; rebuilds the role manifest and URL registry; checks exact counts, hashes, status markers, unresolved path, immutable authorities and clean checkouts.

## Fail-closed boundaries

```text
437 SURFACES CLASSIFIED ≠ BULK QUOTE APPROVAL
80 LINKS DISPOSITIONED ≠ 80 LINKS COPIED TO READER
URL HOLDS RETAINED ≠ URL HOLDS RESOLVED
PART II PASS COMPLETE ≠ WHOLE-BOOK PASS COMPLETE
RESEARCH MERGE ≠ PRODUCT RELEASE
```

## Remaining work

```text
MISSING STANDALONE FINAL READERS = 9
WHOLE-BOOK READER ASSEMBLY = INCOMPLETE
WHOLE-BOOK CITATION PASS = OPEN
WHOLE-BOOK TRANSITION / DEDUP PASS = OPEN
WHOLE-BOOK LINE EDIT = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT SOURCE LINK REPAIRS REQUIRED = 3
PRODUCT RELEASE = NOT CLAIMED
```

## Next transaction

Compose current V6 from immutable V5 plus this Part II receipt. The next final-order reader gap is III.1 `Обещание нового сердца`.
