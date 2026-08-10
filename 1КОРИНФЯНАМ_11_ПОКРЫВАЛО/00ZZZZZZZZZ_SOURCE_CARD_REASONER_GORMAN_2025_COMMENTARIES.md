# Source card — Mark Reasoner / Michael J. Gorman, 1 Corinthians commentaries (2025)

**Дата аудита:** 2026-08-10  
**Статус:** `CURRENT-2025-COMMENTARY-INGRESS / PAGINATION-CORRECTED / DIRECT-PUBLISHER-METADATA / BODY-HOLD / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Purpose

This card controls two current 2025 commentaries:

- Mark Reasoner, *1 Corinthians*, Brill Exegetical Commentary Series 3 (2025);
- Michael J. Gorman, *1 Corinthians: A Theological, Pastoral, and Missional Commentary* (Eerdmans, 2025).

They are different evidence classes:

```text
REASONER_2025 = TECHNICAL_EXEGETICAL_COMMENTARY / HIGH_VALUE_DIRECT_SECTION_HOLD
GORMAN_2025 = THEOLOGICAL_PASTORAL_MISSIONAL_COMMENTARY / CURRENT_INTERPRETIVE_CONTROL
```

No claim grade changes merely because either book exists.

---

# 1. Mark Reasoner — direct identity

Direct Brill metadata verifies:

```text
AUTHOR = Mark Reasoner
TITLE = 1 Corinthians
SERIES = Brill Exegetical Commentary Series
SERIES_VOLUME = 3
EBOOK_ISBN = 9789004737044
PRINT_ISBN = 9789004737037
PUBLISHER = Brill
PRINT_PUBLICATION_DATE = 2025-09-08
LENGTH = 732 pages
```

Direct Brill chapter route already verified for Commentary 4:

- https://brill.com/display/book/9789004737044/BP000007.xml

Brill's TOC identifies:

```text
Commentary 5 — Paul Responds to Questions on Marriage (7:1–40)
Commentary 6 — Food Offered to Idols (8:1–11:1)
Commentary 7 — Hair and Head Coverings in the Assembly (11:2–16)
Commentary 8 — Keep the Lord's Supper (11:17–34)
```

Google Books:

- https://books.google.com/books/about/1_Corinthians.html?id=IEiGEQAAQBAJ

---

# 2. Critical pagination correction

An earlier version of this card **misread the stripped Google Books contents rows** and mapped p.321 to 11:2–16 and p.432 to 11:17–34.

That was wrong.

Google Books displays verse-range labels with punctuation partly stripped. Read in sequence with the Brill TOC, the chapter starts are:

```text
7:1–40       -> p.277   // Commentary 5
8:1–11:1     -> p.321   // Commentary 6
11:2–16      -> p.432   // Commentary 7
11:17–34     -> p.452   // Commentary 8
12:1–14:40   -> p.476   // Commentary 9
15:1–58      -> p.590   // Commentary 10
16:1–24      -> p.638   // Commentary 11
```

Brill independently gives Commentary 4 as pp.238–276, which fits the Google Books sequence exactly: Commentary 5 begins p.277.

Therefore:

```text
REASONER_COMMENTARY_7_11_2_16_START = P432
REASONER_COMMENTARY_8_11_17_34_START = P452
REASONER_11_2_16_APPROX_SPAN = P432_451
REASONER_11_2_16_IS_111_PAGES = FALSE
```

The previous values:

```text
CH7_START = P321
NEXT_SECTION_START = P432
SPAN = P321_431
```

are **superseded and rejected**.

---

# 3. Consequence for circulated Reasoner quotations

Popular/low-quality webpages circulate purported Reasoner quotations assigned to:

```text
p.434 -> 1 Cor 11:2
p.343 -> 1 Cor 11:3
p.444 -> 1 Cor 11:8
```

The old card incorrectly rejected p.434 and p.444 as impossible because of the pagination error.

Correct status:

```text
P434_FOR_V2 = PAGINATION_PLAUSIBLE / WORDING_UNVERIFIED
P444_FOR_V8 = PAGINATION_PLAUSIBLE / WORDING_UNVERIFIED
P343_FOR_V3 = PAGINATION_IMPOSSIBLE_FOR_COMMENTARY_7_IN_THIS_EDITION
```

Why:

```text
11:2–16 = pp.432–451 approximately
```

Thus p.434 and p.444 lie inside the correct section, while p.343 lies in Commentary 6 (8:1–11:1), not Commentary 7.

This **does not authenticate** the wording copied by Wikipedia or other sites. It only corrects the page-location test.

New firewall:

```text
PAGINATION_PLAUSIBLE != QUOTE_AUTHENTICATED
LOW_QUALITY_EXACT_WORDING != QUOTE_SAFE
PAGE_NUMBER_CONTRADICTION = valid falsifier only after chapter pagination is directly controlled
DO_NOT_REJECT_P434_OR_P444_ON_PAGINATION
REJECT_P343_AS_V3_PAGE_LABEL_IN_2025_EDITION
```

Do not silently “repair” the p.343 citation. Reacquire Reasoner's actual body.

---

# 4. Reasoner's actual interpretive position remains HOLD

The Brill chapter body remains institution/login gated in the current route.

The chapter title establishes only the problem-space:

> Hair and Head Coverings in the Assembly (11:2–16)

It does **not** establish how Reasoner adjudicates veil vs hair, `κεφαλή`, `ἐξουσία`, angels, `φύσις`, or v16.

Current status:

```text
REASONER_KEPHALE_POSITION = HOLD
REASONER_VEIL_HAIR_POSITION_DETAIL = HOLD
REASONER_EXOUSIA_POSITION = HOLD
REASONER_ANGELS_POSITION = HOLD
REASONER_PHYSIS_POSITION = HOLD
REASONER_V16_POSITION = HOLD
```

Acquisition priority remains high because the commentary is current and technical, not because the section is unusually long.

```text
P0/P1 REASONER_2025_COMMENTARY_7_PP432_451 = ACQUIRE_DIRECT_BODY
```

---

# 5. Reasoner lawful acquisition routes

```text
BRILL_CHAPTER_PLATFORM = institutional login / paid PDF / preview
GOOGLE_BOOKS = contents/index + limited snippets
LIBRARY_EBOOK = possible institutional Brill access
```

Do not ask the user for a copy before exhausting lawful preview/library routes available to the runtime.

---

# 6. Michael J. Gorman — direct identity

Eerdmans directly verifies:

> Michael J. Gorman, *1 Corinthians: A Theological, Pastoral, and Missional Commentary* (2025).

Current metadata:

```text
AUTHOR = Michael J. Gorman
PUBLISHER = Eerdmans
PUBLICATION_DATE = 2025-03-06
EBOOK_ISBN = 9781467465748
HARDCOVER_ISBN = 9780802882660
LENGTH = 477 pages
```

Gorman's declared commentary type is theological, pastoral, and missional. It remains a serious current interpretive control but is not automatically the primary technical owner of a disputed papyrological or grammatical microclaim.

```text
GORMAN_2025 = P1_CURRENT_THEOLOGICAL_COMMENTARY_CONTROL
GORMAN_2025 != PRIMARY_TECHNICAL_TEXT_CRITICAL_OWNER
```

---

# 7. Gorman 11:2–16 position — direct-section HOLD

The direct Eerdmans route has not yielded a quote-safe 11:2–16 body in this pass.

Secondary 2026 material may serve as acquisition locators, but must not be promoted to direct Gorman wording.

```text
GORMAN_11_2_16_DIRECT_BODY = HOLD
GORMAN_VEIL_HAIR_POSITION = HOLD
GORMAN_KEPHALE_POSITION = HOLD
GORMAN_EXOUSIA_POSITION = HOLD
GORMAN_ANGELS_POSITION = HOLD
```

---

# 8. Relative acquisition priority

```text
P0/P1 Reasoner 2025 Commentary 7 pp432–451 = HIGH
P1 Gorman 2025 exact 11:2–16 section = MEDIUM_HIGH
```

Reasoner first because of:

```text
CURRENT_2025
+ TECHNICAL_EXEGETICAL_SERIES
+ TEXT_CRITICAL_GRAMMATICAL_HISTORICAL_METHOD
+ ROMAN_CORINTH_FOCUS
```

Not because of a false 100+ page section-length claim.

---

# 9. Current commentary radar

```text
GARLAND_2025_2E = P0_DIRECT_TEXT_HOLD
REASONER_2025_BRILL = P0/P1_DIRECT_CHAPTER_HOLD
STARLING_2025_EBTC = P0/P1_SECTION_HOLD
GORMAN_2025_EERDMANS = P1_THEOLOGICAL_SECTION_HOLD
```

Drake 2025 and Peters 2025 remain thematic/specialist monographs rather than verse-by-verse commentary equivalents.

---

# 10. No grade change

```text
CORE_GRADE_REVERSALS = 0
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH
EXOUSIA_EXACT_REFERENT = B_C
```

---

# 11. Audit lesson

This correction is itself a source-hygiene control:

```text
SEARCH_INDEX_STRIPPED_VERSE_LABEL != SAFE_MANUAL_MAPPING
CHAPTER_SEQUENCE_MUST_BE_RECONCILED_WITH_PUBLISHER_TOC
DERIVED_FIREWALL_MUST_BE_REAUDITED_IF_ITS_PAGINATION_PREMISE_FAILS
SELF_CORRECTION > PRESERVING_A_CONVENIENT_REJECTION
```

The old pagination-based rejection of p.434/p.444 must not propagate into later research.

---

# 12. Result

```text
REASONER_2025 = VERIFIED_CURRENT_TECHNICAL_COMMENTARY
REASONER_COMMENTARY_7 = DIRECT_BRILL_TOC_VERIFIED
REASONER_CH7_START = P432_GOOGLE_BOOKS_CORRECTED
REASONER_COMMENTARY_8_START = P452_GOOGLE_BOOKS_CORRECTED
REASONER_11_2_16_APPROX_SPAN = P432_451
REASONER_BODY = HOLD

REASONER_WEB_P434_AS_11_2 = PAGINATION_PLAUSIBLE / WORDING_UNVERIFIED
REASONER_WEB_P444_AS_11_8 = PAGINATION_PLAUSIBLE / WORDING_UNVERIFIED
REASONER_WEB_P343_AS_11_3 = REJECT_PAGE_LABEL_FOR_2025_EDITION

GORMAN_2025 = VERIFIED_CURRENT_EERDMANS_COMMENTARY
GORMAN_EVIDENCE_CLASS = THEOLOGICAL_PASTORAL_MISSIONAL
GORMAN_11_2_16_BODY = HOLD

CORE_GRADE_REVERSALS = 0
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
SITE_PUBLICATION = false
```