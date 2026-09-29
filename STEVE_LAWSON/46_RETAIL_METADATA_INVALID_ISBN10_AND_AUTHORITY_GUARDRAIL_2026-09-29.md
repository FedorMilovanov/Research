# Steven J. Lawson — retail metadata / invalid ISBN-10 normalization guardrail

**Snapshot:** 2026-09-29  
**Status:** `YES24 DERIVED ISBN10 FIELD DEMONSTRABLY INVALID UNDER ISBN STANDARD / RETAIL METADATA NORMALIZATION CONFIRMED / PRIMARY BOOK OBJECT + ISBN AGENCY RECORDS TAKE PRECEDENCE`

## 1. Executive finding

The current YES24 product record for *Mercy in the Wilderness* correctly lists the book's 13-digit ISBN:

> `9798996167302`

but also displays:

> `ISBN10 8996167304`

Source:
- https://www.yes24.com/product/goods/196694745

That ISBN-10 field is not a legitimate equivalent identifier for this book.

The **International ISBN Agency** explicitly states that a 13-digit ISBN beginning with `979`:

> **does not have an equivalent 10-digit ISBN**

and warns that attempts to convert 979 numbers back to 10 digits can create serious errors, including duplicate ISBNs and incorrect order fulfillment.

Official source:
- https://www.isbn-international.org/node/331

The Library of Congress gives the same rule:
- https://www.loc.gov/programs/preassigned-control-number/isbn-converter/

Therefore YES24's `8996167304` is an automatically generated or otherwise erroneous derived metadata value, not a valid ISBN-10 assigned to Lawson's book.

This provides a concrete demonstration that at least some retailer metadata in this title's distribution chain is **algorithmically normalized and fallible**.

---

## 2. What the standard says

The International ISBN Agency explains that:

- prior to 2007 ISBNs used 10 digits;
- modern ISBNs use 13 digits;
- 978-prefix ISBN-13 values allowed compatibility with older ISBN-10 records;
- newer `979` ISBNs are **not backwards compatible**;
- there is **no corresponding ISBN-10** for a 979 ISBN.

Official U.S.-prefix notice:
- https://www.isbn-international.org/node/331

The notice specifically warns publishers, libraries and retailers:

- do not attempt 979 → ISBN-10 conversion;
- record/transmit the full 13-digit ISBN only.

The Library of Congress independently says:

> “a 13-digit ISBN starting with 979 does not have an equivalent 10-digit ISBN.”

Source:
- https://www.loc.gov/programs/preassigned-control-number/isbn-converter/

Thus the rule is explicit, not inferred from check-digit mathematics.

---

## 3. Why `8996167304` can look plausible even though it is invalid as an equivalent ISBN

A naïve conversion routine can:

1. strip the `979` prefix;
2. treat the following nine digits as an old-style ISBN body;
3. calculate an ISBN-10 check digit.

That can produce a mathematically checkable ten-digit string.

But mathematical check-digit validity does **not** create an assigned ISBN or a legitimate equivalent identifier.

For 979-prefix publications, the standard expressly forbids treating such a value as the book's ISBN-10 counterpart.

Therefore:

> **`8996167304` may be algorithmically well-formed, but it is bibliographically invalid as an ISBN-10 equivalent for `9798996167302`.**

---

## 4. Evidentiary implication for the Lawson publishing audit

Several retailer surfaces disagree on Lawson's title:

- Amazon/AbeBooks branch: publisher sometimes shown as **Steven Lawson**;
- broad international feeds: publisher generally **But God Press**;
- page count: **122** on some surfaces vs. **124** on many international feeds;
- YES24: includes an impossible `ISBN10` derivative;
- physical copyright page: copyright Steven Lawson / published by But God Press / print + ebook ISBNs.

The invalid ISBN-10 is important because it proves that retailer/catalog fields can be transformed by software rather than copied verbatim from an authoritative publisher record.

### Authority hierarchy after this finding

For conflicts, prefer in this order:

1. **physical book object** for what the book itself prints;
2. **International ISBN Agency / Bowker / GRP** for registrant/publisher-of-record questions;
3. direct publisher/author production records if acquired;
4. distributor/wholesale metadata;
5. retailer metadata;
6. reseller normalization.

Retail metadata remains useful for:

- discovery;
- availability;
- distribution footprint;
- price/format signals;
- POD classification where explicitly stated.

It should not override a stronger source simply because many storefronts repeat the same field.

---

## 5. Relation to Amazon's `Publisher: Steven Lawson` field

The current Amazon/AbeBooks-facing metadata branch showing:

> Publisher: Steven Lawson

remains a meaningful anomaly.

But the YES24 invalid-ISBN10 example strengthens the guardrail against treating any one retail field as if it were a direct Bowker lookup.

Possible explanations for Amazon's field still include:

- upstream registrant metadata;
- author-as-publisher normalization;
- reseller mapping;
- different source feeds;
- manual or automated metadata transformation.

Only the Bowker/Global Register publisher-of-record object can distinguish these cleanly.

Thus:

> **Amazon's `Publisher: Steven Lawson` is evidence of a metadata branch, not proof that Bowker names Lawson as registrant.**

---

## 6. Relation to POD finding

Canonical POD audit:
- `45_PRINT_ON_DEMAND_DISTRIBUTION_AND_PRODUCTION_BACKEND_AUDIT_2026-09-29.md`

YES24's explicit POD designation remains useful because it is a descriptive fulfillment/edition classification, not merely a fabricated identifier.

However, this new finding gives a general caution:

> even on the same page, some metadata can be reliable and other fields can be mechanically wrong.

Therefore the POD designation should be corroborated where possible, while the platform/printer must remain unresolved until directly identified.

---

## 7. Article-ready formulation

> Retail metadata around Lawson's book is useful but demonstrably imperfect. YES24 correctly lists the title's 979-prefix ISBN-13 yet also generates an “ISBN10” value. The International ISBN Agency explicitly says a 979 ISBN has no 10-digit equivalent and warns that attempts to create one cause duplicate and ordering errors. That concrete metadata failure matters when interpreting other storefront discrepancies—such as “Steven Lawson” versus “But God Press” as publisher or 122 versus 124 pages. The book's own copyright page and an eventual Bowker/Global Register record should outrank retailer normalization.

---

## 8. Publication guardrails

### Safe

- “YES24 displays a derived ISBN-10 that cannot be a legitimate equivalent under the ISBN standard.”
- “This demonstrates fallible retail metadata normalization.”
- “Retail publisher/page-count fields should not be treated as authoritative registrant records.”

### Unsafe

- “YES24's whole record is false.”
- “Because one field is wrong, its POD label is necessarily wrong.”
- “Amazon's publisher field is therefore wrong.”
- “But God Press is definitely the Bowker registrant.”

None of those follows.

---

## 9. Acquisition targets

1. Obtain Bowker/GRP record for `979-8-9961673`.
2. Obtain wholesale ONIX metadata and inspect source/field provenance.
3. Determine whether the 122/124 page discrepancy derives from different metadata generators.
4. Identify whether Amazon's `Steven Lawson` publisher field comes from registrant data, seller entry or automated normalization.
5. Preserve the physical book's barcode/copyright/imprint pages as highest-value production objects.

## Research conclusion

> **YES24 PROVIDES A RARE INTERNAL CONTROL ON THE QUALITY OF THIS BOOK'S RETAIL METADATA. THE PAGE LISTS THE VALID 979-PREFIX ISBN-13 BUT ALSO DISPLAYS `8996167304` AS AN ISBN-10. THE INTERNATIONAL ISBN AGENCY AND LIBRARY OF CONGRESS EXPLICITLY STATE THAT 979 ISBNs HAVE NO ISBN-10 EQUIVALENT. THIS IS THEREFORE A DEMONSTRABLE RETAIL-METADATA NORMALIZATION ERROR. IT DOES NOT INVALIDATE THE PAGE'S OTHER FIELDS, BUT IT PROVES THAT STORE-FACING METADATA CAN BE ALGORITHMICALLY TRANSFORMED AND MUST NOT BE CONFUSED WITH AUTHORITATIVE ISBN-REGISTRANT OR PRIMARY BOOK DATA.**
