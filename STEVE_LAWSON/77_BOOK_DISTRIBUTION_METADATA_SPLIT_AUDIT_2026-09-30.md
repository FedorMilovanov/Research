# Steven J. Lawson — *Mercy in the Wilderness* distribution-metadata split

**Snapshot:** 2026-09-30  
**Status:** `MULTI-RETAILER UPSTREAM CLUSTER IDENTIFIED / EXPLICIT POD RETAIL SIGNAL / AUG-20 + 124PP VS SEP-1 + 122PP SPLIT / NO SECOND PHYSICAL EDITION PROVEN / PRIMARY COPYRIGHT PAGE STILL GOVERNS`

## 1. Executive finding

A fresh international retailer pass found a highly consistent metadata cluster for *Mercy in the Wilderness* that differs from the familiar Amazon/Goodreads presentation.

A broad group of independent/international booksellers carries the same record:

- **Publisher:** But God Press
- **Publish date:** August 20, 2026
- **Format:** paperback
- **Pages:** 124
- **ISBN/EAN:** 9798996167302
- dimensions approximately 8.5 × 5.5 inches / 21.59 × 13.97 cm

Examples:
- Bookshop.org: https://bookshop.org/p/books/mercy-in-the-wilderness/a404a74339c859b1
- Booktopia: https://www.booktopia.com.au/mercy-in-the-wilderness-steven-lawson/book/9798996167302.html
- Yes24 exact product page: https://www.yes24.com/product/goods/196694745
- Adlibris Finland: https://www.adlibris.com/fi/kirja/mercy-in-the-wilderness-9798996167302
- Orell Füssli: https://www.orellfuessli.ch/shop/home/artikeldetails/A1081753908
- IBS: https://www.ibs.it/mercy-in-wilderness-libro-inglese-steven-lawson/e/9798996167302
- Feltrinelli: https://www.lafeltrinelli.it/mercy-in-wilderness-libro-inglese-steven-lawson/e/9798996167302

The Bookshop.org, Booktopia, Yes24, Orell Füssli and Adlibris records all expose the same core 20-Aug / 124-page / But God Press identity.

By contrast, the public Goodreads/Amazon-facing cluster presents:

- **Published September 1, 2026**;
- **122 pages**;
- Amazon-facing metadata has at times displayed **Publisher: Steven Lawson** rather than But God Press.

Goodreads:
- https://www.goodreads.com/book/show/258369757-mercy-in-the-wilderness

AbeBooks catalog layer:
- https://www.abebooks.com/products/isbn/9798996167302

AbeBooks commonly shows 122 pages and `Publisher: Steven Lawson`, while at least one international AbeBooks seller record under the same ISBN simultaneously exposes `But God Press Aug 2026`.

## 2. Strongest direct retailer objects

### Bookshop.org

Current product metadata:

- Steven Lawson — author;
- Publisher: But God Press;
- Publish Date: August 20, 2026;
- Pages: 124;
- EAN/UPC: 9798996167302;
- 8.5 × 5.5 × 0.3 inches.

Source:
- https://bookshop.org/p/books/mercy-in-the-wilderness/a404a74339c859b1

### Booktopia

Current product metadata:

- paperback;
- 20 August 2026;
- 124 pages;
- Publisher: But God Press;
- ISBN: 9798996167302;
- dimensions 21.59 × 13.97 × 0.66 cm.

Source:
- https://www.booktopia.com.au/mercy-in-the-wilderness-steven-lawson/book/9798996167302.html

### Yes24 — explicit print-on-demand signal

The Korean Yes24 product page is especially valuable because it does more than repeat the same bibliographic fields.

It labels the title as:

- a directly imported foreign book;
- **`POD 주문제작도서`** — a POD / made-to-order book;
- with a notice explaining that it is manufactured on order and that binding/print quality may vary accordingly.

It also gives:

- publication date: 2026-08-20;
- 124 pages;
- 153 g;
- 140 × 216 mm;
- ISBN13: 9798996167302;
- publisher: But God Press.

Source:
- https://www.yes24.com/product/goods/196694745

### Evidentiary significance of the POD label

This is the strongest public retailer signal yet that the print edition participates in a **print-on-demand distribution pipeline** rather than conventional fixed-inventory trade publishing.

It materially strengthens the existing micro-imprint/self-publishing-style model.

But it does **not** identify the POD backend.

In particular, the current pass did not establish whether the manufacturing/distribution route is:

- IngramSpark / Lightning Source;
- Amazon KDP Print;
- another POD wholesaler;
- a regional reprint-on-demand service downstream from a different distributor.

Exact searches combining the ISBN with `Ingram`, `Lightning Source`, `POD`, and `print on demand` did not expose a reliable backend identifier beyond the Yes24 POD designation.

Therefore:

> **POD = STRONGLY SUPPORTED RETAIL/DISTRIBUTION CHARACTERISTIC; SPECIFIC POD PROVIDER = UNRESOLVED.**

## 3. Why the shared metadata probably has an upstream source

The near-identical field structure across geographically unrelated retail sites strongly suggests a shared upstream bibliographic/distribution feed rather than independent manual cataloging by each retailer.

Repeated fields include:

- But God Press;
- Aug. 20, 2026;
- 124 pages;
- ~140 × 216 mm;
- ~150–154 g;
- ISBN 9798996167302.

That is an inference about metadata provenance, not identification of the specific distributor.

The explicit POD marker now makes the next useful question more precise:

> **Which ONIX/POD wholesaler is feeding the Aug-20/124-page record?**

That is a better target than continuing to search for `But God Press` as though it were necessarily a conventional publishing house with a public staff/site/catalog.

## 4. Contrasting Goodreads/Amazon-facing record

Goodreads currently reports:

- paperback;
- **122 pages**;
- Published **September 1, 2026**.

Source:
- https://www.goodreads.com/book/show/258369757-mercy-in-the-wilderness

AbeBooks catalog metadata similarly reports:

- Publisher: Steven Lawson;
- 2026;
- 122 pages.

Source:
- https://www.abebooks.com/products/isbn/9798996167302

Contemporary Amazon-derived reporting likewise described:

- September 1 release;
- 122 pages;
- at least one Amazon state with `Publisher: Steven Lawson`.

The project already preserves the stronger primary-object fact that the copyright page itself says:

- Copyright © 2026 Steven Lawson;
- Published by But God Press, 2026;
- Print ISBN 979-8-9961673-0-2;
- Ebook ISBN 979-8-9961673-1-9.

Canonical primary-object file:
- `35_BOOK_COPYRIGHT_PAGE_PRIMARY_OBJECT_2026-09-29.md`

## 5. What the split probably means — and what it does not

The repeated international pattern is consistent with at least two metadata layers:

### Layer A — distribution/POD bibliographic feed
- But God Press;
- Aug. 20, 2026;
- 124 pp.;
- explicit POD/made-to-order labeling at Yes24.

### Layer B — Amazon/Goodreads-facing listing
- Sep. 1, 2026;
- 122 pp.;
- sometimes publisher shown as Steven Lawson.

Possible explanations include:

1. an upstream distributor metadata record created before the Amazon retail date;
2. preliminary vs finalized pagination metadata;
3. Amazon-specific normalization of publisher/registrant identity;
4. different counting conventions for numbered vs total printed pages;
5. a metadata revision between ingestion systems;
6. POD-file metadata that differs from consumer-listing metadata.

Current evidence does **not** establish:

- two different physical editions;
- a substantive revision between Aug. 20 and Sep. 1;
- a hidden earlier public launch;
- an Aug. 20 first-sale date;
- that Amazon intentionally changed the publisher field after criticism;
- the identity of the distributor/POD backend feeding Bookshop/Booktopia/Yes24/etc.

## 6. Why this strengthens the micro-imprint analysis

Before the copyright page was acquired, a broad `But God Press` retailer field might have been dismissed as a stray reseller artifact.

That is no longer tenable:

1. the **book itself** says `Published by But God Press`;
2. multiple independent retail systems repeat **But God Press**;
3. those systems share a coherent Aug. 20 / 124-page bibliographic record;
4. Yes24 explicitly describes the book as POD/made-to-order;
5. Amazon has separately surfaced `Steven Lawson` as publisher;
6. Steven Lawson is the named copyright holder.

The cleanest synthesis is now:

> **The book was produced through a very small author-controlled or author-adjacent publishing structure using But God Press as the internal imprint/publisher identity, with a public distribution record characteristic of print-on-demand, while retailer systems expose at least two different metadata representations.**

This still does not identify the Bowker registrant, legal owner of the imprint, or POD provider.

## 7. Ebook negative update

The primary copyright page assigns:

> `9798996167319` — Ebook ISBN.

A fresh exact-ISBN search again produced no reliable indexed public retail/catalog object for that ebook.

The other mathematically valid slots in the ten-number prefix (`...2` through `...9`) likewise did not surface reliable public publication records in the targeted pass.

Therefore the earlier guardrail remains intact:

> **assigned ebook ISBN ≠ demonstrated publicly released ebook.**

## 8. Pagination guardrail

The 122 vs 124 discrepancy should not be used as evidence of deception or a covert second edition.

Retail metadata commonly differs because of:

- front/back matter counting;
- preliminary metadata;
- print-on-demand file revisions;
- platform conventions.

Until two physical copies with demonstrably different interiors are compared, the safe statement is simply:

> public metadata disagrees on pagination and date.

## 9. Publication-date guardrail

The existence of repeated Aug. 20 metadata does not prove readers could buy/receive the book on Aug. 20.

It may be:

- an assigned publication date in an upstream feed;
- a wholesale/POD availability date;
- a metadata-creation date;
- an intended release date later superseded on Amazon.

Thus `September 1, 2026` should not automatically be rewritten as false, nor should `August 20, 2026` be presented as independently established first publication/on-sale date.

## 10. Article impact

No V6 thesis change is required.

If publication mechanics are discussed in a later revision, the stronger sentence is:

> Retail metadata is split. A broad international bookseller/POD feed consistently identifies But God Press, Aug. 20, 2026 and 124 pages, while Goodreads/Amazon-facing records use Sep. 1 and 122 pages and Amazon has displayed Steven Lawson as publisher. At least one major international retailer explicitly labels the book POD/made-to-order. The book itself resolves the most important point: it names Lawson as copyright holder and But God Press as publisher. The remaining discrepancy concerns metadata/distribution plumbing and legal registrant identity, not the authenticity of the imprint name.

## 11. Next high-value acquisition

1. Bowker / Global Register of Publishers lookup for prefix `979-8-9961673`.
2. Distributor/ONIX/POD-backend identification for the Aug. 20 / 124-page cluster.
3. Physical-copy collation against the reported 122/124 counts.
4. Indexed/public object for ebook ISBN `9798996167319` if one appears.
5. Any other title assigned within publication elements `2–9`.
6. Manufacturing/printer marks from the physical copy, if present.

Do not spend large cycles on random retailer duplicates unless one exposes a new upstream field such as distributor, imprint address, registrant, edition statement, manufacturing record, or POD provider.

## Research conclusion

> **THE FRESH RETAILER PASS IDENTIFIES A REAL, REPEATED METADATA SPLIT RATHER THAN A SINGLE-SITE TYPO, AND THE YES24 RECORD ADDS AN IMPORTANT PRODUCTION SIGNAL: THE BOOK IS EXPLICITLY MARKETED THERE AS POD / MADE-TO-ORDER. BOOKSHOP.ORG, BOOKTOPIA, YES24, ORELL FÜSSLI, ADLIBRIS AND OTHER INTERNATIONAL BOOKSELLERS CARRY A COMMON BUT GOD PRESS / AUGUST 20, 2026 / 124-PAGE RECORD FOR ISBN 9798996167302, WHILE GOODREADS/AMAZON/ABEBOOKS-FACING DATA PRESENT SEPTEMBER 1 OR GENERIC 2026 / 122 PAGES AND HAVE DISPLAYED STEVEN LAWSON AS PUBLISHER. THE PRIMARY COPYRIGHT PAGE STILL GOVERNS THE CORE FACTS: LAWSON IS THE COPYRIGHT HOLDER AND BUT GOD PRESS IS THE PUBLISHER/IMPRINT PRINTED INSIDE THE BOOK. THE NEW POD SIGNAL STRENGTHENS THE AUTHOR-CONTROLLED MICRO-IMPRINT/SELF-PUBLISHING-STYLE MODEL, BUT IT DOES NOT IDENTIFY THE POD PROVIDER, PROVE TWO EDITIONS, ESTABLISH AN EARLIER PUBLIC SALE, OR RESOLVE THE LEGAL ISBN REGISTRANT.**
