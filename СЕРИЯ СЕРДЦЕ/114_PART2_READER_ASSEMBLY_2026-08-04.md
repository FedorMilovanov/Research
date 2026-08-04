# Том 114. Part II reader assembly — «Диагноз падшего сердца»

**Дата:** 2026-08-04  
**Authority ID:** `HEART-PART2-READER-ASSEMBLY-2026-08-04`  
**Entry:** `HEART-BOOK-II`  
**Final-order position:** `5 / 18`  
**Reader:** `113_READER_CHAPTER_II_FALLEN_HEART_DIAGNOSIS_2026-08-04.md`  
**Machine receipt:** `data/heart-part2-reader-assembly-2026-08-04.json`

## Decision

```text
PART II STANDALONE FINAL-BOOK READER = ASSEMBLED
COMPOSITION MODE = PARAPHRASE-ONLY
ASSEMBLED READERS = 9 / 18
MISSING STANDALONE FINAL READERS = 9
ENTRY CITATION PASSES COMPLETE = 8 / 18
PART II ENTRY CITATION PASS = OPEN
ASSEMBLED READER CITATION REVIEWS = 8 / 9
PRODUCT SOURCE LINK REPAIRS REQUIRED = 3
NEW DIRECT QUOTES APPROVED = 0
```

This transaction closes only Part II reader assembly. It does not review or approve the full R3/R4 citation surface.

## Immutable owners

```text
R3 BLOB = ae55b1fad5cccbdb623c551a14222e0f51ec084a
R4 BLOB = f82780e13cb064aa89c06427d11a938662fc3ff8
PRECEDING I.3 READER BLOB = a958066bff3010f14540d67c900c362bd88de98a
CURRENT V5 BLOB = 2ba8c381e636a9f1148fa30e3f010d595feb42a6
WHOLE-BOOK INTEGRATION BLOB = 06d67275c42c7a9c3bd0365044f358b4b7d7a895
HISTORICAL TRIAGE BLOB = de4d49cada15b231dfc31058aced4ec7a25928a2
PART II READER BLOB = 4cca195d034c70a7d3d6c3dd8edc9a04fcffcc20
```

```text
R3 SHA-256 = 12c4344acfc96050eaae35d98ed666102e62c700ead9db34c24681a914102efb
R4 SHA-256 = 1e5ff030fea335f64dda3a613898d1237d3a4e34d0c303d67f51a64af92e1964
READER SHA-256 = c7e37a30651bf96f77f2a2eba204251591edb2ab28aff1cc8332d6c72f99086d
```

## Source surface

R3 owns the unregenerate struggle ceiling:

```text
R3 = 50 Scripture locators / 304 quotation surfaces / 53 external links / 1 internal link
```

R4 owns the four-soils diagnosis:

```text
R4 = 68 Scripture locators / 133 quotation surfaces / 27 external links / 0 internal links
```

Historical union:

```text
HISTORICAL DOSSIER SURFACES = 118 / 437 / 80 / 1
```

The four numbers are Scripture locators, quotation surfaces, external links and internal links.

```text
SCRIPTURE SET SHA-256 = 5d78a0e23ed09e10f71dfcf9010269430c53faf2bd6ffe1225a3160ee9ffc4a6
EXTERNAL LINK SET SHA-256 = f5ce26d3f27bf9e6aa2c87e625d9b91875d580f296d02d80e974a27dd279187f
INTERNAL LINK SET SHA-256 = 340d19206af863e8b9a7098a84d47199360bec49d1062545c199a4fda8572c65
```

## Reader result

```text
READER WORDS = 1671
READER SURFACES = 20 / 0 / 0 / 0
READER SOURCE HEADINGS = 0
READER FOOTNOTE DEFINITIONS = 0
SOURCE QUOTATIONS COPIED = 0
SOURCE LINKS COPIED = 0
LONG EXACT SOURCE SENTENCES COPIED = 0
```

The reader holds together two source lanes:

1. real horizontal struggle and its vertical ceiling;
2. four hearts under one word.

It does not turn moral discipline into regeneration and does not treat every visible weakness as false faith.

## Ownership boundaries

```text
I.3 = full Jeremiah 17 exposition
PART II = unregenerate struggle ceiling + four soils
III.1 = promise of a new heart
III.2 = causal exposition of regeneration
V = conscience-only struggle versus Spirit-enabled warfare
```

Part II may point toward the promise of a new heart but may not absorb the regeneration chapters.

## Permanent gate

```text
python3 scripts/validate_heart_part2_reader_assembly.py --product-root ../Product
```

The validator requires:

- exact source, reader and governance blobs;
- exact source and reader SHA-256;
- fresh R3 and R4 scans;
- historical union `118 / 437 / 80 / 1`;
- reader `1671 / 20 / 0 / 0`;
- all required headings and boundary markers;
- no material sentence transfer from R3, R4 or I.3;
- historical Part II triage still open;
- current V5 still `8 / 18`;
- clean Research and Product checkouts.

## Effective state

```text
HEART-BOOK-II:
RESEARCH_DOSSIER_ONLY
→ ASSEMBLED_READER_CITATION_OPEN
```

```text
ASSEMBLED READERS = 9 / 18
MISSING STANDALONE FINAL READERS = 9
ENTRY CITATION PASSES COMPLETE = 8 / 18
ENTRY CITATION PASSES OPEN = 10 / 18
PRODUCT SOURCE ONLY = 4
RESEARCH DOSSIER ONLY = 5
```

## Fail-closed boundaries

```text
PART II READER ASSEMBLED ≠ PART II CITATION PASS COMPLETE
437 SOURCE SURFACES ≠ 437 DIRECT QUOTES APPROVED
9 READERS ≠ 9 COMPLETED CITATION PASSES
RESEARCH MERGE ≠ PRODUCT RELEASE
```

## Remaining work

```text
PART II ENTRY CITATION PASS = OPEN
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

Run a separate Part II entry citation pass over the immutable reader and the full R3/R4 `118 / 437 / 80 / 1` surface. Quote-bank status markers and unresolved source candidates must remain fail-closed.
