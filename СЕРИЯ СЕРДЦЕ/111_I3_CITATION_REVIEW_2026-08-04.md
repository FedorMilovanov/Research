# Том 111. I.3 citation review — «Падшее сердце: Иеремия 17»

**Дата:** 2026-08-04  
**Authority ID:** `HEART-I3-CITATION-REVIEW-2026-08-04`  
**Entry:** `HEART-BOOK-I3`  
**Final-order position:** `3 / 18`  
**Reader authority:** `109_READER_CHAPTER_I3_FALLEN_HEART_JEREMIAH_17_2026-08-04.md`  
**Assembly receipt:** `data/heart-i3-reader-assembly-2026-08-04.json`  
**Machine review receipt:** `data/heart-i3-citation-review-2026-08-04.json`

## 1. Решение

```text
I.3 ENTRY CITATION PASS = COMPLETE
ENTRY CITATION PASSES COMPLETE = 8 / 18
ENTRY CITATION PASSES OPEN = 10 / 18
ASSEMBLED READERS = 8 / 18
ASSEMBLED READER CITATION REVIEWS = 8 / 8
MISSING STANDALONE FINAL READERS = 10
NEW DIRECT QUOTES APPROVED = 0
```

Закрывается только entry-level citation review I.3. Whole-book assembly, whole-book citation, transition/dedup, line edit, manuscript bundle and Product release remain open.

## 2. Immutable source chain

```text
I.3 ASSEMBLY RECEIPT BLOB = 2ae5a01ed0a2c9931b7a36f4991cf93bcec3fb7a
CURRENT V4 BLOB = d0ddea6cf1fc33dfab53ae9691aaf2d903d03b73
HISTORICAL TRIAGE BLOB = de4d49cada15b231dfc31058aced4ec7a25928a2
I.3 READER BLOB = a958066bff3010f14540d67c900c362bd88de98a
PRODUCT BLOB = dc27b7a06d37321a068e971c02af4a0df3028ae6
```

```text
I.3 READER SHA-256 = 6d00cbd44a7d3540faddcbdbc03bfff1fd1c5a441c380392010f973d76ce92f9
PRODUCT SHA-256 = 4292f76ff3e2fa15dfd682b5a421400ce9a62ec391109b3109aef14d72b224f0
```

No source or reader file is rewritten by this review.

## 3. Full Product owner review

```text
SCRIPTURE LOCATORS GOVERNED = 71 / 71
QUOTATION SURFACES CLASSIFIED = 224 / 224
EXTERNAL LINKS DISPOSITIONED = 15 / 15
INTERNAL TARGETS RESOLVED = 3 / 3
```

The full historical owner remains the complete review surface. The ten selected assembly sections from the preceding transaction do not replace the complete `71 / 224 / 15 / 3` Product row.

## 4. Quotation taxonomy

```text
SCRIPTURE DIRECT OR EXPLICIT TRANSLATION = 40
ATTRIBUTED THEOLOGICAL OR CONFESSIONAL DIRECT = 61
TITLE OR LINK LABEL = 58
EDITORIAL, LEXICAL OR CAPTION = 65
TOTAL = 224
```

Each normalized quotation hash belongs to exactly one class. Duplicate occurrences retain one semantic class across every occurrence.

```text
SCRIPTURE REFERENCE SET SHA-256 = 25a12fcd595c213eb09589c08b3be4a9b76d7cb24e586ba2b505f0b7fc6c56a1
QUOTATION MANIFEST SHA-256 = 120f305e7474a0baf3da7a068ea91159333a879e3fbe4a5f0f6b006a841e3d9b
CLASSIFICATION MAP SHA-256 = cc083ae3149eed2a989b2b1fcff16d5f02152664e40249a10e5cea10aeeace46
SECTION SUMMARY SHA-256 = f46b756c5f6e4f3afcda331d2e0ae94543ccabb24b6b02af537c78f1943df30e
```

Classification means governed review. It does not mean that 224 source surfaces are approved for transfer into the final-book reader.

## 5. Scripture governance

The Product source contains direct Russian Scripture fragments, explicit translation variants, lexical discussion and attributed theological quotations. The review keeps these categories distinct.

```text
SCRIPTURE VERSION BOUNDARY = SOURCE-DECLARED / CONTEXT-GOVERNED
SCRIPTURE SURFACES COPIED TO READER = 0
READER DIRECT SCRIPTURE QUOTATIONS = 0
```

The reader uses locator-only paraphrase and remains unchanged.

## 6. External-link review

All fifteen Product URLs receive an explicit disposition.

Positive live dispositions cover:

- an Internet Archive primary scan;
- CCEL source texts;
- the self-canonical Product article;
- official Desiring God articles;
- Monergism resources;
- the official Spurgeon sermon page.

Three original Product links require canonical replacement before Product publication:

```text
PRODUCT LINK REPAIRS REQUIRED = 3
```

### 6.1 Clarkson

The original Wayback URL is malformed. A direct Digital Puritan PDF for `Soul Idolatry Excludes Men Out of Heaven` is verified as the replacement authority.

```text
ORIGINAL STATUS = MALFORMED_ORIGINAL_URL
REPLACEMENT STATUS = VERIFIED
READER TRANSFER = 0
```

### 6.2 Calvin on Jeremiah 17:9–10

The original CCEL study alias is retained as historical Product evidence, while a canonical CCEL commentary page is recorded as the verified replacement.

### 6.3 Brooks, Precious Remedies

The original Monergism `-ebook` alias is retained as historical evidence, while the current canonical Monergism resource is recorded as the replacement.

```text
EXTERNAL LINK REVIEW COMPLETE ≠ PRODUCT LINK REPAIR COMPLETE
```

The entry review can close because every link is dispositioned. Product publication remains fail-closed until the three original Product links are repaired in a separate Product transaction.

## 7. Internal-link review

```text
/articles/hermenevticheskaya-otsenka-hristotsentrichnoy-germenevtiki/
/articles/krajne-li-isporcheno-serdce/
/articles/rimlyanam-7-veruyushchiy-ili-neveruyushchiy/
```

All three targets exist on the exact pinned Product commit and are bound to exact Git blobs.

## 8. Reader result

```text
READER SCRIPTURE LOCATORS = 13
READER QUOTATION SURFACES = 0
READER EXTERNAL LINKS = 0
READER INTERNAL LINKS = 0
READER FOOTNOTE DEFINITIONS = 0
PRODUCT QUOTATION SURFACES COPIED = 0
PRODUCT LINKS COPIED = 0
NEW DIRECT QUOTES APPROVED = 0
```

The reader remains paraphrase-only and its content does not change in this transaction.

## 9. Historical governance

Historical triage remains immutable:

```text
HISTORICAL I.3 TRIAGE STATE = TRIAGED_OPEN
```

The current receipt is a later composed overlay. It does not rewrite the historical snapshot.

## 10. Entry blockers

```text
SCRIPTURE REVIEW BLOCKER = RESOLVED
QUOTATION CLASSIFICATION BLOCKER = RESOLVED
EXTERNAL LINK REVIEW BLOCKER = RESOLVED BY EXPLICIT DISPOSITIONS
INTERNAL LINK BLOCKER = RESOLVED
READER ASSEMBLY BLOCKER = RESOLVED
REMAINING ENTRY BLOCKERS = 0
```

Product link repair is a Product-publication blocker, not an unreviewed I.3 citation surface.

## 11. Permanent gate

Heart workflow must run:

```text
python3 scripts/validate_heart_i3_entry_citation_pass.py --product-root ../Product
```

Acceptance requires:

- immutable assembly, current V4, triage, reader and Product blobs;
- exact Product and reader SHA-256;
- fresh `71` Scripture reference scan and set hash;
- fresh `224` quotation scan;
- exact four-class taxonomy with no overlaps;
- exact occurrence counts `40 / 61 / 58 / 65`;
- exact manifest, classification and section-summary hashes;
- exact fifteen external URLs and disposition registry;
- exactly three replacement authorities;
- exact three internal target files and Git blobs;
- reader `13 / 0 / 0` scan;
- zero source transfer and zero new direct quotes;
- current effective counts `8 / 18`;
- clean Research and Product checkouts.

## 12. Effective state

```text
HEART-BOOK-I3:
ASSEMBLED_READER_CITATION_OPEN
→ ENTRY_CITATION_PASS_COMPLETE
```

```text
ENTRY CITATION PASSES COMPLETE = 8 / 18
ENTRY CITATION PASSES OPEN = 10 / 18
ASSEMBLED READERS = 8 / 18
ASSEMBLED READER CITATION REVIEWS = 8 / 8
MISSING STANDALONE FINAL READERS = 10
PRODUCT SOURCE ONLY = 4
RESEARCH DOSSIER ONLY = 6
```

## 13. Fail-closed boundaries

```text
224 SURFACES CLASSIFIED ≠ 224 DIRECT QUOTES APPROVED
15 LINKS DISPOSITIONED ≠ 15 LINKS COPIED INTO READER
3 REPLACEMENTS VERIFIED ≠ PRODUCT SOURCE ALREADY REPAIRED
I.3 PASS COMPLETE ≠ WHOLE-BOOK PASS COMPLETE
RESEARCH MERGE ≠ PRODUCT RELEASE
```

## 14. Remaining work

```text
MISSING STANDALONE FINAL READERS = 10
WHOLE-BOOK READER ASSEMBLY = INCOMPLETE
WHOLE-BOOK CITATION PASS = OPEN
WHOLE-BOOK TRANSITION / DEDUP PASS = OPEN
WHOLE-BOOK LINE EDIT = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT LINK REPAIRS REQUIRED = 3
PRODUCT RELEASE = NOT CLAIMED
```

## 15. Next canonical transaction

Compose a separate current V5 authority from immutable current V4 plus this I.3 receipt. After V5 merge, the next final-order reader transaction is Part II `Диагноз падшего сердца` from the R3/R4 dossier boundary.

## 16. Final disposition

Authority `HEART-I3-CITATION-REVIEW-2026-08-04` closes the I.3 entry citation pass at `8 / 18`, reviews all eight assembled readers at `8 / 8`, preserves zero new direct quotes and keeps three Product link repairs and every whole-book/Product release gate open.
