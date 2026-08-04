# Heart current entry citation state V9 — 2026-08-04

**Authority:** `HEART-ENTRY-CITATION-PASS-CURRENT-V9-2026-08-04`  
**Exact Research base:** `c7039d209a55c8ca5d4a59e3aed99b5b19d80a7d`  
**Previous current V8 blob:** `6736f90211e34c5dbb7d9943e617102b660bb5be`  
**III.4 citation receipt blob:** `ee8fc5302c18351c83d1d3b15010a67d162bd947`  
**III.4 assembly receipt blob:** `b9dfda284cfa36d8ee6a7d970dc3bf2a9eeba7c9`

## Composition rule

V9 is a delta-only current-state authority. It composes immutable V8 plus the squash-stable completed III.4 citation receipt. It does not rewrite V8, the III.4 reader, either III.4 source owner or any historical citation authority.

The only completed-entry set change is the addition of `HEART-BOOK-III4`.

## Current canonical counts

**ENTRY CITATION PASSES COMPLETE = 12 / 18**  
**ENTRY CITATION PASSES OPEN = 6 / 18**  
**ASSEMBLED READERS = 12 / 18**  
**ASSEMBLED READER CITATION REVIEWS = 12 / 12**  
**MISSING STANDALONE FINAL READERS = 6**  
**PRODUCT SOURCE ONLY = 2**  
**RESEARCH DOSSIER ONLY = 4**  
**NEW DIRECT QUOTES APPROVED = 0**

All twelve assembled readers are citation-reviewed. This does not mean the whole book is assembled: six final-order reader owners remain open.

## Completed entry set

1. `HEART-BOOK-I1`
2. `HEART-BOOK-I2`
3. `HEART-BOOK-I3`
4. `HEART-BOOK-I4`
5. `HEART-BOOK-II`
6. `HEART-BOOK-III1`
7. `HEART-BOOK-III2`
8. `HEART-BOOK-III3`
9. `HEART-BOOK-III4`
10. `HEART-BOOK-X1`
11. `HEART-BOOK-X2`
12. `HEART-BOOK-X3`

## Open final-order entries

Product-source-only reader gaps:

- `HEART-BOOK-V`
- `HEART-BOOK-VII`

Research-dossier-only reader gaps:

- `HEART-BOOK-IV`
- `HEART-BOOK-VI`
- `HEART-BOOK-VIII`
- `HEART-BOOK-IX`

The lanes are disjoint and exhaust the six-entry reader/citation backlog.

## III.4 delta

III.4 contributes exactly:

- one assembled and citation-reviewed entry;
- six retained dossier URL holds;
- zero new dossier URL repairs;
- zero new unresolved internal paths;
- six Product internal targets verified on the pinned Product commit;
- zero reader quotation transfer;
- zero reader link transfer;
- zero new direct quotes.

Its quotation taxonomy, URL-status registry and Product-target registry remain owned by the immutable III.4 citation receipt and are not duplicated as a second review in V9.

## Retained repair and hold backlog

**PRODUCT SOURCE REPAIRS REQUIRED = 4**

- I.3 retains three source URL repairs.
- III.1 retains one Scripture locator repair requiring `Флп. 1:6`.

III.1 also retains:

- one attributed theological locator hold;
- eight lexical-support locator holds.

**DOSSIER URL HOLDS RETAINED = 46**

- Part II: `15`;
- III.2: `25`;
- III.4: `6`.

No hold is promoted or silently closed.

**DOSSIER SOURCE URL REPAIRS REQUIRED = 2**

Both malformed III.2 URL tokens remain open:

- `https://www.monergism.com/regeneration-6\``;
- `https://www.reformedreader.org/ccc/1689lbc/english/Chapter10.htm**`.

**UNRESOLVED INTERNAL PATHS RETAINED = 1**

The retained unresolved path is Part II `/articles/opinion/`. III.2 `/articles/onsite/` remains an external-URL-fragment false positive. III.4 added no unresolved internal path because all six Product targets exist on the pinned commit.

## Publication boundary

**ALL CURRENTLY ASSEMBLED READERS REVIEWED = TRUE**  
**WHOLE-BOOK READER ASSEMBLY = INCOMPLETE**  
**WHOLE-BOOK CITATION PASS = OPEN**  
**WHOLE-BOOK TRANSITION / DEDUP PASS = OPEN**  
**WHOLE-BOOK LINE EDIT = OPEN**  
**MANUSCRIPT BUNDLE = INCOMPLETE**  
**PRODUCT SOURCE REPAIRS COMPLETE = FALSE**  
**DOSSIER URL HOLDS RESOLVED = FALSE**  
**DOSSIER SOURCE URL REPAIRS COMPLETE = FALSE**  
**UNRESOLVED INTERNAL PATHS RESOLVED = FALSE**  
**PRODUCT RELEASE = NOT CLAIMED**

## Next bounded transaction

**NEXT READER ASSEMBLY = HEART-BOOK-IV**

Part IV is the next final-order gap. Its reader must be assembled from the exact R7a dossier owner in a separate transaction. The Part IV citation pass and later current V10 composition must remain separate.
