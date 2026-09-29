# Steven J. Lawson — *Mercy in the Wilderness* distribution-metadata split

**Snapshot:** 2026-09-30  
**Status:** `MULTI-RETAILER UPSTREAM CLUSTER IDENTIFIED / AUG-20 + 124PP VS SEP-1 + 122PP SPLIT / NO SECOND PHYSICAL EDITION PROVEN / PRIMARY COPYRIGHT PAGE STILL GOVERNS`

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
- Adlibris: https://www.adlibris.com/
- Yes24: https://www.yes24.com/
- IBS: https://www.ibs.it/
- Feltrinelli: https://www.lafeltrinelli.it/
- Orell Füssli: https://www.orellfuessli.ch/

The Bookshop.org and Booktopia records are especially explicit and independently visible.

By contrast, the public Goodreads/Amazon-facing cluster presents:

- **Published September 1, 2026**;
- **122 pages**;
- Amazon-facing metadata has at times displayed **Publisher: Steven Lawson** rather than But God Press.

Goodreads:
- https://www.goodreads.com/book/show/258369757-mercy-in-the-wilderness

AbeBooks listings likewise commonly show 122 pages and in some records `Publisher: Steven Lawson`, while other seller metadata exposes But God Press / August 2026 information.

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

The near-identical field structure across geographically unrelated retail sites strongly suggests a shared upstream bibliographic/distribution feed rather than independent manual cataloging by each retailer.

That is an inference about metadata provenance, not identification of the specific distributor.

## 3. Contrasting Goodreads/Amazon-facing record

Goodreads currently reports:

- paperback;
- **122 pages**;
- Published **September 1, 2026**.

Source:
- https://www.goodreads.com/book/show/258369757-mercy-in-the-wilderness

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

## 4. What the split probably means — and what it does not

The repeated international pattern is consistent with at least two metadata layers:

### Layer A — distribution/bibliographic feed
- But God Press;
- Aug. 20, 2026;
- 124 pp.

### Layer B — Amazon/Goodreads-facing listing
- Sep. 1, 2026;
- 122 pp.;
- sometimes publisher shown as Steven Lawson.

Possible explanations include:

1. an upstream distributor metadata record created before the Amazon retail date;
2. preliminary vs finalized pagination metadata;
3. Amazon-specific normalization of publisher/registrant identity;
4. different counting conventions for numbered vs total printed pages;
5. a metadata revision between ingestion systems.

Current evidence does **not** establish:

- two different physical editions;
- a substantive revision between Aug. 20 and Sep. 1;
- a hidden earlier public launch;
- an Aug. 20 first-sale date;
- that Amazon intentionally changed the publisher field after criticism;
- the identity of the distributor feeding Bookshop/Booktopia/etc.

## 5. Why this strengthens the micro-imprint analysis

Before the copyright page was acquired, a broad `But God Press` retailer field might have been dismissed as a stray reseller artifact.

That is no longer tenable:

1. the **book itself** says `Published by But God Press`;
2. multiple independent retail systems repeat **But God Press**;
3. those systems share a coherent Aug. 20 / 124-page bibliographic record;
4. Amazon has separately surfaced `Steven Lawson` as publisher;
5. Steven Lawson is the named copyright holder.

The cleanest synthesis remains:

> **The book was produced through a very small author-controlled or author-adjacent publishing structure using But God Press as the internal imprint/publisher identity, while retailer systems expose at least two different metadata representations.**

This still does not identify the Bowker registrant or legal owner of the imprint.

## 6. Ebook negative update

The primary copyright page assigns:

> `9798996167319` — Ebook ISBN.

A fresh exact-ISBN search again produced no reliable indexed public retail/catalog object for that ebook.

The other mathematically valid slots in the ten-number prefix (`...2` through `...9`) likewise did not surface reliable public publication records in the targeted pass.

Therefore the earlier guardrail remains intact:

> **assigned ebook ISBN ≠ demonstrated publicly released ebook.**

## 7. Pagination guardrail

The 122 vs 124 discrepancy should not be used as evidence of deception or a covert second edition.

Retail metadata commonly differs because of:

- front/back matter counting;
- preliminary metadata;
- print-on-demand file revisions;
- platform conventions.

Until two physical copies with demonstrably different interiors are compared, the safe statement is simply:

> public metadata disagrees on pagination and date.

## 8. Publication-date guardrail

The existence of repeated Aug. 20 metadata does not prove readers could buy/receive the book on Aug. 20.

It may be:

- an assigned publication date in an upstream feed;
- a wholesale availability date;
- a metadata-creation date;
- an intended release date later superseded on Amazon.

Thus `September 1, 2026` should not automatically be rewritten as false, nor should `August 20, 2026` be presented as independently established first publication/on-sale date.

## 9. Article impact

No V6 thesis change is required.

If publication mechanics are discussed in a later revision, the stronger sentence is:

> Retail metadata is split. A broad international bookseller feed consistently identifies But God Press, Aug. 20, 2026 and 124 pages, while Goodreads/Amazon-facing records use Sep. 1 and 122 pages and Amazon has displayed Steven Lawson as publisher. The book itself resolves the most important point: it names Lawson as copyright holder and But God Press as publisher. The remaining discrepancy concerns metadata plumbing and legal registrant identity, not the authenticity of the imprint name.

## 10. Next high-value acquisition

1. Bowker / Global Register of Publishers lookup for prefix `979-8-9961673`.
2. Distributor/ONIX source identification for the Aug. 20 / 124-page cluster.
3. Physical-copy collation against the reported 122/124 counts.
4. Indexed/public object for ebook ISBN `9798996167319` if one appears.
5. Any other title assigned within publication elements `2–9`.

Do not spend large cycles on random retailer duplicates unless one exposes a new upstream field such as distributor, imprint address, registrant, edition statement, or manufacturing record.

## Research conclusion

> **THE FRESH RETAILER PASS IDENTIFIES A REAL, REPEATED METADATA SPLIT RATHER THAN A SINGLE-SITE TYPO. BOOKSHOP.ORG, BOOKTOPIA AND MULTIPLE INTERNATIONAL BOOKSELLERS CARRY A COMMON BUT GOD PRESS / AUGUST 20, 2026 / 124-PAGE RECORD FOR ISBN 9798996167302, WHILE GOODREADS/AMAZON-FACING DATA PRESENT SEPTEMBER 1 / 122 PAGES AND AMAZON HAS DISPLAYED STEVEN LAWSON AS PUBLISHER. THE PRIMARY COPYRIGHT PAGE STILL GOVERNS THE CORE FACTS: LAWSON IS THE COPYRIGHT HOLDER AND BUT GOD PRESS IS THE PUBLISHER/IMPRINT PRINTED INSIDE THE BOOK. THE SPLIT STRENGTHENS THE EXISTENCE OF MULTIPLE METADATA LAYERS BUT DOES NOT PROVE TWO EDITIONS, AN EARLIER PUBLIC SALE, OR THE LEGAL IDENTITY OF THE ISBN REGISTRANT.**
