# Том 89. Whole-book citation/reference inventory — «СЕРИЯ СЕРДЦЕ»

**Дата:** 2026-08-04  
**Authority ID:** `HEART-WHOLE-BOOK-CITATION-INVENTORY-2026-08-04`  
**Encoding authority:** `data/heart-whole-book-citation-inventory-2026-08-04.encoding.json`  
**Builder:** `scripts/build_heart_whole_book_citation_inventory.py`  
**Validator:** `scripts/validate_heart_whole_book_citation_inventory.py`

```text
CITATION INVENTORY = COMPLETE
FINAL BOOK ENTRIES SCANNED = 18 / 18
ENTRY CITATION PASS COMPLETE = 0 / 18
ENTRIES REQUIRING MANUAL BOOK REVIEW = 18 / 18
WHOLE-BOOK CITATION PASS = OPEN
NEW DIRECT QUOTES APPROVED = 0
MANUSCRIPT REWRITES = 0
PRODUCT RELEASE = NOT CLAIMED
```

## 1. What this transaction closes

The owner map is already complete and four reader chapters are assembled. This transaction performs the first deterministic citation/reference inventory across all eighteen final-order entries without rewriting their text.

The scanner reads the current primary manuscript and governing support owners for each entry:

- four assembled Research readers;
- eight current Product-source entries;
- six Research-dossier-only entries;
- the exact five-section X.2 scope;
- the exact X.3 `vyhod` support section.

Product is read only from pinned commit:

```text
repository = FedorMilovanov/gb-is-my-strength
commit = 0fbe7d1ead9ebd1bea867418e254da438ec63329
```

Research source ownership is pinned to the post-X.3-reader snapshot:

```text
Research snapshot = 92bb7c3708b77f6e8344e8c29261d93ecea4debb
```

## 2. Exact encoded registry receipt

The deterministic JSON snapshot is retained as four normalized base64 chunks containing one gzip stream. The encoding is storage transport only; the validator must reconstruct and compare it against a fresh scan before acceptance.

```text
decoded JSON bytes = 285803
decoded JSON SHA-256 = b25ff1a498057f6c20d92e5f98965338c40a9de752af198e9de97fefcf81b000
gzip bytes = 46416
gzip SHA-256 = e1aea1238abea14bf8b7a4157bd36038c760073ce7932eacdb2582f473277dd8
base64 characters = 61888
chunks = 4 × 15472 characters
```

Permanent acceptance sequence:

1. verify each normalized chunk length and SHA-256;
2. concatenate and strictly decode base64;
3. verify gzip byte size and SHA-256;
4. decompress and verify JSON byte size and SHA-256;
5. parse the decoded registry;
6. run a fresh exact Research/Product scan;
7. compare the complete canonical JSON structures.

No committed snapshot can remain green after source drift.

## 3. Inventory counts

```text
FINAL BOOK ENTRIES = 18
ASSEMBLED READER ENTRIES = 4
PRODUCT SOURCE-ONLY ENTRIES = 8
RESEARCH DOSSIER-ONLY ENTRIES = 6
OWNER-REQUIRED ENTRIES = 0
UNIQUE OWNER FILES = 31
OWNER SURFACES SCANNED = 38
UNIQUE SCRIPTURE REFERENCES = 1063
UNIQUE EXTERNAL LINKS = 414
UNIQUE INTERNAL ARTICLE LINKS = 22
FOOTNOTE DEFINITIONS = 0
MARKDOWN BLOCKQUOTE SURFACES = 1115
HTML BLOCKQUOTE SURFACES = 0
INLINE QUOTATION SURFACES = 3271
SOURCE / REFERENCE HEADINGS = 20
ENTRY CITATION PASS COMPLETE = 0 / 18
ENTRIES REQUIRING MANUAL BOOK REVIEW = 18 / 18
NEW DIRECT QUOTES APPROVED = 0
```

These values describe detected surfaces, not editorial approvals.

## 4. What the scanner records

For every owner surface:

- surface type: Research or Product;
- path, owner role and exact section IDs where applicable;
- full-file and scoped SHA-256;
- scoped byte size;
- explicit Russian/English Scripture-reference tokens;
- external URLs;
- internal `/articles/` links;
- footnote-definition count;
- Markdown and HTML blockquote count;
- inline guillemet and curly-quote surfaces;
- headings that explicitly identify sources, bibliography, references or notes.

For every book entry, the registry then aggregates:

- unique Scripture references;
- external and internal links;
- quotation-surface count;
- direct-quote state inherited from its current authority;
- manual-review reasons;
- `entryCitationPassComplete = false`.

## 5. Interpretation boundary

The inventory is intentionally conservative.

### A quotation surface is not automatically a direct quotation

Markdown blockquotes, inline guillemets and curly quotation marks include several possible classes:

- Scripture quotations;
- historical quotations;
- source excerpts;
- technical terms;
- rhetorical or editorial quotation marks;
- already governed Product quotations.

The scanner records candidates. It does not silently classify, approve, reject or relocate them.

### A detected Scripture reference is not automatically normalized

The grammar detects explicit Russian and English Bible-book tokens with chapter/verse patterns. It does not prove:

- translation/version identity;
- correctness of the chapter or verse;
- consistency of abbreviations;
- whether the reference belongs in prose, a note or a source list;
- whether an implicit allusion was missed.

### A link is not automatically adequate evidence

Presence of a URL does not establish:

- accessibility;
- source quality;
- stable locator;
- correct edition or version;
- quotation support;
- rights or publication approval.

## 6. Why every entry remains open

Every one of the eighteen entries receives `BOOK_LEVEL_CITATION_REVIEW_REQUIRED`.

Additional reasons are attached where applicable:

- `READER_MANUSCRIPT_NOT_ASSEMBLED` for dossier-only entries;
- `EXTERNAL_LINKS_PRESENT`;
- `QUOTATION_SURFACES_PRESENT`;
- `FOOTNOTES_PRESENT` when detected;
- `NO_EXPLICIT_SOURCE_HEADING_IN_SCANNED_SCOPE` when no governed heading is present.

Therefore:

```text
CITATION INVENTORY COMPLETE ≠ CITATION PASS COMPLETE
1063 SCRIPTURE TOKENS ≠ 1063 VERIFIED REFERENCES
3271 INLINE QUOTATION SURFACES ≠ 3271 APPROVED DIRECT QUOTES
414 EXTERNAL LINKS ≠ 414 ADEQUATE SOURCES
OWNER MAP COMPLETE ≠ MANUSCRIPT BUNDLE COMPLETE
```

## 7. What is closed

```text
18-ENTRY SOURCE-PATH GRAPH = CLOSED
EXACT RESEARCH / PRODUCT READBACK = CLOSED
SECTION-AWARE X.2 / X.3 SCOPING = CLOSED
DETERMINISTIC CITATION-SURFACE EXTRACTION = CLOSED
ENCODED REGISTRY RECEIPT = CLOSED
FRESH-SCAN DRIFT COMPARISON = CLOSED
CITATION INVENTORY = COMPLETE
```

## 8. What remains open

```text
ENTRY CITATION DISPOSITION = 0 / 18
DIRECT-QUOTATION CANDIDATE CLASSIFICATION = OPEN
SCRIPTURE VERSION / ABBREVIATION NORMALIZATION = OPEN
MISSING LOCATORS AND EDITION IDENTIFIERS = OPEN
EXTERNAL-LINK ADEQUACY REVIEW = OPEN
WHOLE-BOOK CITATION PASS = OPEN
WHOLE-BOOK READER ASSEMBLY = INCOMPLETE
WHOLE-BOOK TRANSITION AND DEDUP PASS = OPEN
WHOLE-BOOK LINE EDIT = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT RELEASE = NOT CLAIMED
```

No manuscript was changed by the scan. No new direct quotation was approved by implication.

## 9. Next canonical transaction

The next lane is entry-level citation disposition, not another broad source search and not an automatic bulk rewrite.

For each entry, review the committed inventory and record:

1. Scripture references requiring version or abbreviation normalization;
2. historical/direct quotation candidates and their locator/version/context state;
3. external links requiring replacement, stronger evidence or stable locators;
4. missing source headings, bibliography owners or edition identifiers;
5. duplicated source explanations that should be owned by one chapter;
6. an explicit disposition that remains open until all identified blockers are resolved.

Only after those entry-level decisions can a later transaction claim whole-book citation closure.

## 10. Decision

The whole-book citation/reference inventory is complete as a read-only deterministic evidence map. The whole-book citation pass remains open, all eighteen entries require manual editorial review, entry-level citation completion remains `0 / 18`, and new direct-quote approval remains zero.
