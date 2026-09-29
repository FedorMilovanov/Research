# Steven J. Lawson — print-on-demand distribution / production-backend audit

**Snapshot:** 2026-09-29  
**Status:** `POD STATUS DIRECTLY CONFIRMED BY RETAILER / BROAD INTERNATIONAL DISTRIBUTION CONFIRMED / KDP-INGRAM-LIGHTNING SOURCE BACKEND NOT IDENTIFIED`

## 1. Executive finding

A current YES24 product record for Steven Lawson's *Mercy in the Wilderness* explicitly classifies the paperback as a **POD / made-to-order book**.

Source:
- https://www.yes24.com/product/goods/196694745

The listing labels the binding/edition:

> `[POD 주문제작도서]`

and separately warns customers that it is an **order-manufactured (POD) book** whose binding/printing quality may vary.

This is the strongest current public evidence that the physical edition is fulfilled through a **print-on-demand production model** rather than a conventional publisher print run with an obvious warehoused inventory.

At the same time, targeted searches do **not** identify the actual manufacturing/fulfillment backend. No reliable public record located in this pass ties ISBN `9798996167302` specifically to:

- Amazon KDP;
- IngramSpark;
- Lightning Source;
- Ingram Content Group as the printer;
- Bookvault;
- another named POD manufacturer.

Therefore the proper finding is:

> **POD is established; the POD platform/printer is not.**

---

## 2. YES24 — direct POD classification

Current product object:
- title: *Mercy in the Wilderness*;
- author: Steven Lawson;
- publisher: But God Press;
- publication date: Aug. 20, 2026;
- ISBN: `9798996167302`;
- pages: 124;
- dimensions: 140 × 216 mm;
- weight: approximately 153 g.

Most importantly, the record explicitly says:

> `POD 주문제작도서`

and includes a purchase notice explaining that the title is **made to order using POD production**.

### Evidence class

This is retailer metadata rather than a printer's own manufacturing statement, but it is much more specific than simply seeing slow fulfillment or a small publisher.

It directly identifies the commercial edition as POD.

### Safe conclusion

> **The international retail metadata identifies the paperback as print-on-demand / made-to-order.**

### Unsafe conclusion

> **It was printed by Amazon KDP.**

No source found establishes that.

---

## 3. Broad international distribution is independently visible

The same ISBN appears across numerous retailer/distributor surfaces with highly standardized bibliographic metadata:

### Bookshop.org
- Publisher: But God Press
- publication date: Aug. 20, 2026
- 124 pages
- 8.5 × 5.5 × 0.3 in.
- $14.99

Source:
- https://bookshop.org/p/books/mercy-in-the-wilderness/a404a74339c859b1

### Booktopia
- Publisher: But God Press
- Aug. 20, 2026
- 124 pages
- 21.59 × 13.97 × 0.66 cm
- ships in 5–7 business days

Source:
- https://www.booktopia.com.au/mercy-in-the-wilderness-steven-lawson/book/9798996167302.html

### IBS / Feltrinelli
- Publisher: But God Press
- 124 pages
- 216 × 140 mm
- roughly 150 g
- availability approximately three weeks

Sources:
- https://www.ibs.it/mercy-in-wilderness-libro-inglese-steven-lawson/e/9798996167302
- https://www.lafeltrinelli.it/mercy-in-wilderness-libro-inglese-steven-lawson/e/9798996167302

### Adlibris
- Publisher: But God Press
- Aug. 20, 2026
- 124 pages
- approximately 154 g
- described as an order item rather than ordinary shelf stock

Source:
- https://www.adlibris.com/fi/kirja/mercy-in-the-wilderness-9798996167302

### Orell Füssli
- Publisher: But God Press
- Aug. 20, 2026
- 124 pages
- 21.6 × 14 × 0.7 cm
- approximately 154 g
- fulfillment approximately three weeks

Source:
- https://www.orellfuessli.ch/shop/home/artikeldetails/A1081753908

### Barnes & Noble current commerce object
- identifies But God Press;
- lists the paperback at $14.99.

Source:
- https://shop.barnesandnoble.com/products/9798996167302

### Evidentiary implication

The book is not limited to a single Amazon marketplace listing. It entered a broad international bibliographic/retail feed under the same ISBN and core metadata.

That is fully compatible with POD distribution.

It still does not identify the upstream aggregator or manufacturer.

---

## 4. AbeBooks preserves a separate metadata branch

AbeBooks currently exposes the same ISBN in at least two forms:

1. an edition record saying:
   - publisher: **Steven Lawson**;
   - 122 pages;
2. a seller/distribution listing saying:
   - publisher: **But God Press**;
   - Aug. 2026.

Source:
- https://www.abebooks.com/9798996167302/Mercy-Wilderness-Fell-What-Found/plp

This metadata split was already analyzed in:
- `33_BOOK_METADATA_SPLIT_AMAZON_AUTHOR_PUBLISHER_SIGNAL_2026-09-29.md`
- `35_BOOK_COPYRIGHT_PAGE_PRIMARY_OBJECT_2026-09-29.md`

The new POD evidence does not resolve that split, but makes an author-controlled micro-imprint + automated distribution pipeline increasingly plausible.

---

## 5. The POD finding fits the ISBN architecture

Canonical ISBN audit:
- `34_ISBN_REGISTRANT_PREFIX_AND_MICRO_PUBLISHER_BLOCK_AUDIT_2026-09-29.md`

Known facts:

- publisher prefix: `979-8-9961673`;
- seven-digit U.S. registrant element;
- only one publication digit remains;
- structural capacity = 10 publication identifiers;
- print ISBN occupies slot `0`;
- copyright page assigns ebook slot `1`.

International ISBN guidance associates longer registrant elements with lower anticipated publisher output.

The independently observed POD status therefore aligns naturally with the existing bibliographic profile:

> very small ISBN allocation + one-title imprint footprint + global feed + made-to-order printing.

### Guardrail

The combination strongly supports a **micro-publisher/self-publishing-style production model**.

It still does not prove:

- Lawson personally purchased the ISBN block;
- Lawson personally opened the POD account;
- But God Press is a legal entity owned by Lawson;
- which company printed an individual copy.

---

## 6. KDP vs. IngramSpark vs. Lightning Source — search result

Targeted exact-ISBN searches were run for combinations with:

- `KDP`;
- `Amazon KDP`;
- `Ingram`;
- `Ingram Content Group`;
- `IngramSpark`;
- `Lightning Source`;
- `Lightning Source LLC`;
- `independently published`;
- `distributor`;
- `wholesaler`.

No reliable exact-title/ISBN object surfaced that names the production backend.

The exact ISBN also produced no useful title hit on public search surfaces restricted to:

- `ingramcontent.com`;
- `ipage.ingramcontent.com`;
- `ingramspark.com`;
- `lightningsource.com`.

### Why broad retail availability is not enough to identify Ingram

It would be tempting to infer Ingram simply because independent-bookstore and international retail channels carry the book.

That inference is too strong without an explicit wholesale/printer record. Multiple POD/distribution routes can put a title into online retail systems.

Likewise, Amazon availability does not prove KDP.

Therefore:

> **BACKEND = UNRESOLVED.**

---

## 7. Page-count discrepancy is real but not diagnostic

There are two recurring metadata values:

### 124 pages
Broad international feeds including Bookshop, Booktopia, YES24, IBS and Adlibris generally show **124 pages**.

### 122 pages
Amazon/Goodreads/AbeBooks-facing records commonly show **122 pages**.

This difference may reflect:

- numbered-content pages vs. total physical leaves/pages;
- blank/front/back matter handling;
- separate upstream metadata sources;
- normalization differences.

It is not evidence by itself of multiple physical editions, fraud or different printers.

### Research rule

Record the discrepancy but do not assign a cause unless a physical copy or authoritative production record resolves it.

---

## 8. Ebook ISBN remains assigned but publicly absent

The physical copyright page gives:

> Ebook ISBN `979-8-9961673-1-9`

Canonical primary-object file:
- `35_BOOK_COPYRIGHT_PAGE_PRIMARY_OBJECT_2026-09-29.md`

Fresh exact-ISBN and format searches again failed to locate a public ebook storefront/catalog object on ordinary indexed surfaces.

Current reviewers likewise noted the lack of a digital version at launch.

Therefore:

> **Ebook ISBN assigned / public ebook release still not located.**

This is relevant to production-chain reconstruction because a POD paperback may have been launched independently of a digital edition despite the assigned ISBN.

---

## 9. Article-ready wording

> The book's production model is now clearer. A current YES24 record explicitly labels *Mercy in the Wilderness* a POD, made-to-order book and warns customers about the characteristics of on-demand printing. The same ISBN is distributed broadly through Bookshop.org, Barnes & Noble and international booksellers, while the book itself names the tiny imprint But God Press and uses a ten-number U.S. ISBN block. Taken together, those facts strongly support an author-controlled micro-publisher/POD structure. They do not identify the actual production service: no reliable public record located so far ties the ISBN specifically to KDP, IngramSpark, Lightning Source or another printer.

---

## 10. Acquisition targets

### P0

1. Inspect a physical copy for printer/manufacturing marks, barcode-zone clues or final colophon information.
2. Locate authoritative wholesale metadata naming the distributor or manufacturer.
3. Search any invoice/shipping label images publicly posted by buyers for a lawful production-origin clue.
4. Obtain Bowker/Global Register registrant record for prefix `979-8-9961673`.

### P1

5. Look for Ingram iPage/library/vendor records if publicly accessible without credentials.
6. Check whether the ISBN appears in distributor ONIX feeds with a supplier identifier.
7. Continue exact ebook-ISBN search for a latent digital metadata record.
8. Determine whether the 122/124-page discrepancy is simply front/back-matter counting by comparing a physical copy.

## Research conclusion

> **PRINT-ON-DEMAND STATUS IS NOW DIRECTLY SUPPORTED BY CURRENT RETAILER METADATA: YES24 EXPLICITLY MARKS LAWSON'S PAPERBACK AS A POD / MADE-TO-ORDER BOOK. THE TITLE IS SIMULTANEOUSLY PRESENT IN A BROAD INTERNATIONAL RETAIL FEED UNDER BUT GOD PRESS, WHICH FITS THE ALREADY-ESTABLISHED SMALL ISBN BLOCK AND MICRO-IMPRINT PROFILE. HOWEVER, THE SPECIFIC PRODUCTION BACKEND REMAINS UNRESOLVED. NO RELIABLE SOURCE CURRENTLY IDENTIFIES KDP, INGRAMSPARK, LIGHTNING SOURCE OR ANOTHER NAMED PRINTER. POD SHOULD THEREFORE BE STATED AS FACT; THE PLATFORM SHOULD NOT BE GUESSED.**
