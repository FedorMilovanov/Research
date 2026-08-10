# 1 Коринфянам 11:2–16 — current commentary acquisition 2025

**Статус:** `EVERGREEN-DOSSIER / CURRENT-COMMENTARIES / PAGINATION-CONTROL / DIRECT-BODY-HOLDS / RESEARCH-ONLY / PUBLICATION-HOLD`  
**Последнее обновление:** 2026-08-10

## 0. Authority rule

This dossier owns the current 2025 commentary acquisition queue for:

- Mark Reasoner, *1 Corinthians* (Brill, 2025);
- Michael J. Gorman, *1 Corinthians* (Eerdmans, 2025);
- David I. Starling, *1 Corinthians* (Lexham Academic / EBTC, 2025).

```text
CURRENT_BOOK_EXISTS != 1COR11_POSITION_VERIFIED
PUBLISHER_TOC != CHAPTER_BODY
SEARCH_SNIPPET != QUOTE_SAFE_TEXT
PAGINATION_PLAUSIBLE != QUOTE_AUTHENTICATED
RECENCY != AUTHORITY
```

Garland 2025, Fee Revised 2014, Thiselton 2000 and Ciampa/Rosner 2010 remain high-value acquisition targets but are not duplicated here if they have their own current source cards/audits.

---

# 1. Mark Reasoner — Brill Exegetical Commentary Series 3

Direct Brill metadata:

```text
AUTHOR = Mark Reasoner
TITLE = 1 Corinthians
SERIES = Brill Exegetical Commentary Series
SERIES_VOLUME = 3
PRINT_PUBLICATION_DATE = 2025-09-08
EBOOK_ISBN = 9789004737044
PRINT_ISBN = 9789004737037
LENGTH = 732_pages
```

Brill chapter route:
- https://brill.com/display/book/9789004737044/BP000007.xml

Google Books:
- https://books.google.com/books/about/1_Corinthians.html?id=IEiGEQAAQBAJ

## 1.1 Corrected section pagination

Brill TOC + Google Books sequence jointly establish:

```text
7:1_40 = p277
8:1_11:1 = p321
11:2_16 = p432
11:17_34 = p452
12:1_14:40 = p476
15:1_58 = p590
16:1_24 = p638
```

Therefore:

```text
REASONER_COMMENTARY_7_11_2_16_START = P432
REASONER_COMMENTARY_8_11_17_34_START = P452
REASONER_11_2_16_APPROX_SPAN = P432_451
REASONER_11_2_16_IS_111_PAGES = FALSE
```

The older derived mapping `p321–431 = 11:2–16` is rejected.

## 1.2 Circulated quote firewall

Low-quality webpages circulate page claims around p.434 / p.343 / p.444.

With corrected pagination:

```text
P434_AS_11_2 = PAGINATION_PLAUSIBLE / WORDING_UNVERIFIED
P444_AS_11_8 = PAGINATION_PLAUSIBLE / WORDING_UNVERIFIED
P343_AS_11_3 = PAGINATION_IMPOSSIBLE_IN_2025_EDITION
```

Do not authenticate wording merely because the page falls inside the correct section.

## 1.3 Position remains body-HOLD

```text
REASONER_VEIL_HAIR_POSITION = HOLD
REASONER_KEPHALE_POSITION = HOLD
REASONER_EXOUSIA_POSITION = HOLD
REASONER_ANGELS_POSITION = HOLD
REASONER_PHYSIS_POSITION = HOLD
REASONER_V16_POSITION = HOLD
```

Priority:

```text
P0_P1 REASONER_2025_COMMENTARY_7_PP432_451 = ACQUIRE_DIRECT_BODY
```

---

# 2. Michael J. Gorman — Eerdmans 2025

Direct publisher metadata:

> Michael J. Gorman, *1 Corinthians: A Theological, Pastoral, and Missional Commentary* (Eerdmans, 2025).

```text
PUBLICATION_DATE = 2025-03-06
EBOOK_ISBN = 9781467465748
HARDCOVER_ISBN = 9780802882660
LENGTH = 477_pages
```

Evidence class:

```text
GORMAN_2025 = CURRENT_THEOLOGICAL_PASTORAL_MISSIONAL_COMMENTARY
GORMAN_2025 != PRIMARY_TECHNICAL_TEXT_CRITICAL_OWNER
```

Current direct-section status:

```text
GORMAN_11_2_16_DIRECT_BODY = HOLD
GORMAN_VEIL_HAIR_POSITION = HOLD
GORMAN_KEPHALE_POSITION = HOLD
GORMAN_EXOUSIA_POSITION = HOLD
GORMAN_ANGELS_POSITION = HOLD
```

Priority:

```text
P1 GORMAN_2025_EXACT_11_2_16_SECTION = ACQUIRE
```

---

# 3. David I. Starling — EBTC 2025

Direct embedded-preview metadata identifies:

> David I. Starling, *1 Corinthians*, Evangelical Biblical Theology Commentary, 2025.

Verified route:
- https://biblia.com/api/plugins/embeddedpreview?historybuttons=false&layout=minimal&navigationbox=false&resourceName=LLS%3AEBTC67CO1&sharebutton=false

Current metadata control:

```text
AUTHOR = David_I_Starling
SERIES = Evangelical_Biblical_Theology_Commentary
YEAR = 2025
PUBLISHER = Lexham_Academic_Lexham_Press
GENERAL_EDITORS = Alexander_Schreiner_Kostenberger
```

Current runtime has not extracted a quote-safe 1 Cor 11:2–16 section or exact pages/positions on:

```text
KEPHALE
MATERIAL_COVERING_VS_HAIR
EXOUSIA
ANGELS
PHYSIS
V16
```

Therefore:

```text
STARLING_2025_BOOK = VERIFIED_CURRENT_COMMENTARY
STARLING_2025_1COR11_POSITION = CONTENT_HOLD
STARLING_2025_DIRECT_QUOTE = FORBIDDEN_UNTIL_SECTION_ACQUIRED
STARLING_2025 = P0_P1_CURRENT_EDITION_TARGET
```

Do not infer Starling’s position from series editors, confessional context or reviews.

---

# 4. Current commentary queue

```text
GARLAND_2025_2E_PP468_493 = P0_DIRECT_TEXT_HOLD
REASONER_2025_PP432_451 = P0_P1_DIRECT_CHAPTER_HOLD
STARLING_2025_1COR11 = P0_P1_SECTION_HOLD
GORMAN_2025_1COR11 = P1_SECTION_HOLD
THISELTON_2000_PP800_847 = HOLD
FEE_REVISED_2014_APPROX_PP542_586 = HOLD
CIAMPA_ROSNER_2010_PP503_540 = DETAIL_HOLD
```

Current edition status alone never upgrades a claim grade.

---

# 5. Acquisition method

```text
1. publisher chapter / ebook preview
2. lawful library / institutional route
3. Google Books contents/snippet only for navigation
4. quote only after direct section body
5. reconcile any page claim against publisher TOC before using it as falsifier
```

Do not ask the user for a copy before exhausting lawful routes available to the runtime.

---

# 6. Audit lessons

```text
SEARCH_INDEX_STRIPPED_VERSE_LABEL != SAFE_MANUAL_MAPPING
CHAPTER_SEQUENCE_MUST_BE_RECONCILED_WITH_PUBLISHER_TOC
DERIVED_FIREWALL_MUST_BE_REAUDITED_IF_ITS_PAGINATION_PREMISE_FAILS
SELF_CORRECTION > PRESERVING_A_CONVENIENT_REJECTION
CURRENT_EDITION != POSITION_VERIFIED
```

---

# 7. Result

```text
REASONER_2025 = VERIFIED_CURRENT_TECHNICAL_COMMENTARY
REASONER_11_2_16 = APPROX_PP432_451 / DIRECT_BODY_HOLD
GORMAN_2025 = VERIFIED_CURRENT_THEOLOGICAL_COMMENTARY / SECTION_HOLD
STARLING_2025 = VERIFIED_CURRENT_COMMENTARY / 1COR11_CONTENT_HOLD
CORE_GRADE_REVERSALS = 0
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
SITE_PUBLICATION = false
```