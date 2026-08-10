# Source card — Gordon D. Fee, *The First Epistle to the Corinthians*, Revised Edition (2014), 1 Cor 11:2–16

**Дата аудита:** 2026-08-10  
**Статус:** `P0-TECHNICAL-COMMENTARY / REVISED-EDITION-CALIBRATION / EXACT-TOC-CLOSED / BODY-NOTES-HOLD / RESEARCH-ONLY`

## 0. Purpose

Fee is repeatedly cited throughout the 1 Cor 11 literature, but three different evidence objects are easily conflated:

```text
FEE_1987_FIRST_EDITION
FEE_2014_REVISED_EDITION_MAIN_BODY
FEE_2014_NEW_BIBLIOGRAPHIC_ADDENDA/FOOTNOTE_UPDATES
```

This card prevents a common shortcut:

> assuming that the existence of a 2014 “Addendum” means Fee wrote a materially new exegesis of 11:2–6 there.

The direct/open evidence currently supports a more modest conclusion.

---

# 1. Direct edition identity

Direct Eerdmans/Logos/Biblia and Google Books controls verify:

```text
AUTHOR = Gordon D. Fee
TITLE = The First Epistle to the Corinthians
EDITION = Revised Edition
SERIES = NICNT
PUBLISHER = Eerdmans
YEAR = 2014
PRINT_ISBN = 9780802871367
EBOOK_ISBN = 9781467440417
```

The direct Logos/Biblia embedded preview shows the 2014 revised-edition title/copyright/front matter but truncates before the later exposition.

Google Books/retailer TOC independently identifies the revised internal structure.

---

# 2. Exact revised-edition 11:2–16 map

The current revised TOC gives:

```text
C. Women and Men in Worship (11:2–16) ........ p.542

1. An Argument from Culture and Shame (11:2–6) ... p.550
Addendum ........................................... p.565

2. An Argument from Creation (11:7–12) ............ p.567

3. An Argument from Propriety (11:13–16) .......... p.580

D. Abuse of the Lord's Supper (11:17–34) .......... p.587
```

Thus the revised head-covering unit occupies:

```text
MAIN_11_2_16 = pp.542–586
CULTURE_SHAME_EXPOSITION = pp.550–564
ADDENDUM = starts p.565, about 2 pages in TOC
CREATION_11_7_12 = pp.567–579
PROPRIETY_11_13_16 = pp.580–586
```

These are **2014 revised-edition locators**. Do not substitute 1987 page numbers when citing the revised edition.

---

# 3. What the 2014 Addendum is — and is not

A detailed 2014 review based on a review copy reports that the new addendum on the difficult veiling problem in 11:2–6 is primarily **bibliographical material with a short introduction, without additional commentary**.

The same reviewer observes a parallel bibliographic addendum to chapters 8–10 and notes that Fee did not generally rewrite those commentaries in response to all post-1987 scholarship.

An independent DTS review of the 2014 edition likewise says there do not appear to be substantial changes in Fee's conclusions overall, while noting updates tied to NIV 2011, newer literature and footnotes.

Evidence class:

```text
FEE_2014_ADDENDUM_BIBLIOGRAPHIC_NATURE = STRONG_REVIEW_CONTROL
FEE_2014_ADDENDUM_DIRECT_BODY = HOLD
FEE_2014_ADDENDUM_AS_MAJOR_NEW_EXEGESIS = NOT_SUPPORTED_BY_CURRENT_EVIDENCE
```

Important self-correction:

```text
OLD_WORKING_ASSUMPTION:
  "the 11:2–6 addendum may contain Fee's revised substantive position"

CURRENT:
  ADDENDUM_IS_PRIMARILY_BIBLIOGRAPHIC / MAIN_EXEGESIS_REMAINS_IN_BODY
```

Do not spend P0 acquisition effort on the addendum as though it were a hidden second commentary.

---

# 4. What genuinely changed in the revised edition

Direct publisher/front-matter controls and independent reviews establish several revision layers:

```text
NIV_2011_BASE_TEXT = major motivation
POST_1987_BIBLIOGRAPHY = added/updated
FOOTNOTES = updated in places, including lexical references
FORMAT/VERSE_NUMBER_HANDLING = revised
SOME_OTHER_SECTIONS = more materially revised
```

The reviews specifically flag 14:34–35 as a substantially revised controversial section.

They do **not** establish a comparable wholesale rewriting of 11:2–16.

Therefore:

```text
FEE_2014 != FEE_1987_WITH_ZERO_CHANGE
BUT
FEE_2014_1COR11 != PROVED_NEW_MODEL
```

The right task is source-specific comparison of the main 2014 body/notes against 1987, not presumption in either direction.

---

# 5. Current exact-body status for 11:2–16

Direct Logos/Biblia limited preview stops before 1 Cor 11.

Google Books exposes metadata/contents but not a quote-safe full 11:2–16 section in the current route.

Thus:

```text
FEE_2014_PP542_586_DIRECT_BODY = HOLD
FEE_2014_PP565_566_ADDENDUM_DIRECT_BODY = HOLD
FEE_2014_NOTES_11_2_16 = HOLD
```

No exact quotation should be labelled `direct Fee 2014` unless the actual revised page has been acquired.

---

# 6. Angels — strong locator, not yet primary-body closure

A peer-reviewed Cambridge NTS article cites the revised Fee commentary specifically at:

```text
Fee, First Epistle, pp.576–578
```

for the angel question in 11:10.

A separate secondary quotation chain reproduces Fee's rejection of a lustful/fallen-angels threat reading and assigns it to:

```text
p.576 n.123
```

The reported argument is that the lustful-angels scenario is foreign to Pauline/contextual evidence and raises unresolved questions about why women would be endangered.

Current evidence class:

```text
FEE_2014_ANGELS_LOCATOR_576_578 = STRONG_PEER_REVIEWED_PAGE_LOCATOR
FEE_2014_N123_WATCHERS_REJECTION = STRONG_SECONDARY_QUOTE_LOCATOR
FEE_2014_N123_DIRECT_PAGE = HOLD
```

Do not promote the reproduced wording to quote-safe Fee text until p.576 n.123 itself is acquired.

The page locator is nevertheless useful because it sharply narrows the direct acquisition target.

---

# 7. Main P0 targets within Fee 2014

Instead of treating all 45 pages equally, direct acquisition should prioritize:

```text
P0A p.576 n.123 + surrounding vv10 angel discussion
P0B pp.576–578 complete v10/angel subsection
P0C v10 ἐξουσία note(s) within pp.567–579
P0D main 11:2–6 exposition pp.550–564
P1  addendum pp.565–566 for bibliography/source genealogy
P1  vv13–16 pp.580–586
```

Why p.576–578 first:

- exact peer-reviewed locator exists;
- angels remain a disputed project node;
- revised notes may contain post-1987 bibliography;
- this avoids wasting effort on already-understood TOC/bibliographic material.

---

# 8. Current Fee position must not be reconstructed from mixed editions

Historical secondary literature often cites Fee 1987 page numbers such as the early 500s for the covering discussion.

The 2014 revised structure moves the relevant main block to the mid-500s.

New firewall:

```text
FEE_CITATION_WITH_YEAR_2014 + 1987_PAGE_NUMBER = VERIFY_BEFORE_USE
FEE_QUOTE_WITHOUT_EDITION = EDITION_AMBIGUOUS
FEE_1987_WORDING != AUTOMATIC_2014_WORDING
```

A scholarly claim can remain substantively continuous across editions while the page/footnote changes; citation precision must still be edition-specific.

---

# 9. Relation to current project models

No grade change follows merely from Fee's continuing influence.

Existing project grades remain registry-owned:

```text
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH
EXOUSIA_EXACT_REFERENT = B_C
HEAVENLY_HOLY_ANGELS_REFERENT = B_HIGH_LEADING
WATCHERS = C_SERIOUS_ALTERNATIVE
```

Fee is valuable as a high-weight technical pressure-test, not as a vote that automatically decides the issue.

The reported p.576 n.123 anti-Watchers argument, once directly confirmed, will strengthen source provenance for keeping a lustful/fallen-angels model below the leading heavenly-angel reading, but it will not by itself close the entire angel question.

---

# 10. Open routes

Direct lawful routes identified:

```text
LOGOS/BIBLIA_EMBEDDED_PREVIEW = front matter only for current access
GOOGLE_BOOKS = metadata/TOC/selected material
GOOGLE_PLAY = free sample advertised
PERLEGO = subscription ebook route
LIBRARY/EBSCO = institutional holdings exist
```

No user-copy request should be made before these routes are exhausted where technically available.

---

# 11. Result

```text
FEE_2014_REVISED_EDITION = VERIFIED
FEE_11_2_16_REVISED_RANGE = 542_586
FEE_11_2_6_MAIN = 550_564
FEE_11_2_6_ADDENDUM = 565_566_APPROX
FEE_11_7_12 = 567_579
FEE_11_13_16 = 580_586

ADDENDUM_AS_NEW_MAJOR_EXEGESIS = REJECTED_WORKING_ASSUMPTION
ADDENDUM = PRIMARILY_BIBLIOGRAPHIC_ACCORDING_TO_REVIEW_CONTROL

FEE_ANGELS = PEER_REVIEWED_LOCATOR_PP576_578
FEE_WATCHERS_REJECTION = SECONDARY_LOCATOR_P576_N123
DIRECT_P576_N123 = HOLD

CORE_GRADE_REVERSALS = 0
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
SITE_PUBLICATION = false
```
