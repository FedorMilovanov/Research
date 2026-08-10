# 1 Коринфянам 11:2–16 — current commentary acquisition 2025

**Статус:** `EVERGREEN-DOSSIER / CURRENT-COMMENTARIES / PAGINATION-CONTROL / DIRECT-BODY-HOLDS / TRANSPORT-LEDGER / RESEARCH-ONLY / PUBLICATION-HOLD`  
**Последнее обновление:** 2026-08-10

## 0. Authority rule

This dossier owns the current 2025 commentary acquisition queue for:

- Mark Reasoner, *1 Corinthians* (Brill, 2025);
- Michael J. Gorman, *1 Corinthians* (Eerdmans, 2025);
- David I. Starling, *1 Corinthians* (Lexham Academic / EBTC, 2025).

It also records **transport attempts** for other high-value commentary targets when that prevents future agents from repeating the same preview route.

```text
CURRENT_BOOK_EXISTS != 1COR11_POSITION_VERIFIED
PUBLISHER_TOC != CHAPTER_BODY
SEARCH_SNIPPET != QUOTE_SAFE_TEXT
PAGINATION_PLAUSIBLE != QUOTE_AUTHENTICATED
PREVIEW_EXISTS != TARGET_SECTION_EXPOSED
PREVIEW_NO_MATCH != BOOK_HAS_NO_SUCH_DISCUSSION
RECENCY != AUTHORITY
```

Garland 2025, Fee Revised 2014, Thiselton 2000 and Ciampa/Rosner 2010 keep their own substantive owners/source cards where present. This dossier stores only cross-target acquisition state, not duplicate exegesis.

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

Brill / Google routes:
- https://brill.com/display/book/9789004737044/BP000007.xml
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

The presence of one impossible citation on the same page means the circulating quote bundle cannot be promoted wholesale. Each wording claim must be independently authenticated.

## 1.3 Direct-body transport status

The official Brill TOC identifies the dedicated chapter:

```text
Commentary 7 = Hair and Head Coverings in the Assembly (11:2–16)
```

Sequential Brill chapter-slot inference was tested as discovery only; the presumed next `BP...` route did not yield a readable target body in the current runtime.

```text
BRILL_CHAPTER_ID_SEQUENCE_INFERENCE != DIRECT_CHAPTER_BODY
REASONER_OFFICIAL_CHAPTER_IDENTITY = CLOSED
REASONER_DIRECT_11_2_16_BODY = HOLD
```

Position remains open:

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

Lawful routes tested in the current acquisition sequence:

```text
EERDMANS_PUBLISHER_OBJECT = VERIFIED
GOOGLE_BOOKS_LIMITED_PREVIEW_OBJECT = VERIFIED
OVERDRIVE_LIBBY_SAMPLE_ROUTE = VERIFIED_AS_LICENSED_ROUTE
TARGET_11_2_16_BODY_EXPOSED = NO_IN_CURRENT_RUNTIME
```

A dynamic sample route that does not expose the target section cannot be converted into a quotation by inference.

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

Official embedded preview:
- https://biblia.com/api/plugins/embeddedpreview?historybuttons=false&layout=minimal&navigationbox=false&resourceName=LLS%3AEBTC67CO1&sharebutton=false

It identifies:

```text
AUTHOR = David_I_Starling
SERIES = Evangelical_Biblical_Theology_Commentary
YEAR = 2025
PUBLISHER = Lexham_Academic_Lexham_Press
GENERAL_EDITORS = Alexander_Schreiner_Kostenberger
```

The preview was searched directly for target-section markers (`11:2–16`, covering vocabulary and related terms). The accessible preview surface exposes front matter / contents, not the required exposition.

```text
STARLING_OFFICIAL_BIBLIA_PREVIEW = VERIFIED
STARLING_PREVIEW_TARGET_SECTION = NOT_EXPOSED
PREVIEW_FRONT_MATTER != COMMENTARY_POSITION
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

# 4. Cross-target lawful-preview transport ledger

This section does **not** own the exegesis of Fee/Garland/Thiselton/Ciampa-Rosner. It records routes already exhausted in the current runtime so later passes do not re-run the same metadata-only search and mistake lack of preview for substantive evidence.

## 4.1 Fee Revised 2014

Substantive owner:
- `00ZZZZZZZZZ_SOURCE_CARD_FEE_REVISED_2014_1COR11.md`

Routes checked:

```text
BIBLIA_NICNT67CO1_2ED = OFFICIAL_EMBEDDED_PREVIEW / FRONT_MATTER_ONLY
GOOGLE_PLAY_REVISED_EDITION = VERIFIED_BOOK_SAMPLE_OBJECT
SEARCH_11_2 = NO_MATCH_IN_ACCESSIBLE_PREVIEW_INDEX
SEARCH_HEAD_COVERING = NO_MATCH_IN_ACCESSIBLE_PREVIEW_INDEX
SEARCH_P563 = NO_MATCH_IN_ACCESSIBLE_BIBLIA_SURFACE
```

Therefore:

```text
FEE_2014_PP542_586_DIRECT_BODY = HOLD
THIRD_PARTY_FEE_P563_WORDING != DIRECT_FEE_2014
```

The source card’s narrower p.576–578 / n.123 acquisition target remains more efficient than repeating broad preview searches.

## 4.2 Ciampa / Rosner 2010

Official Eerdmans object is verified:

```text
TITLE = The First Letter to the Corinthians
AUTHORS = Roy_E_Ciampa + Brian_S_Rosner
SERIES = PNTC
YEAR = 2010
PAGES = 990
```

Google Books limited-preview objects were searched for `11:2`, `head covering`, `covering` and `authority on her head`; the accessible index did not expose the target body.

```text
CIAMPA_ROSNER_OFFICIAL_BOOK_OBJECT = CLOSED
CIAMPA_ROSNER_GOOGLE_BOOKS_TARGET_BODY = NOT_EXPOSED
CIAMPA_ROSNER_2010_PP503_540 = DETAIL_HOLD
```

No negative inference about their actual interpretation follows from preview non-exposure.

## 4.3 Garland 2025 second edition

Baker Academic, Logos, Google Books and Perlego controls verify a genuine second edition:

```text
AUTHOR = David_E_Garland
TITLE = 1_Corinthians
SERIES = BECNT
EDITION = 2
YEAR = 2025
PRINT_ISBN = 9781540962607
EBOOK_ISBN = 9781493451692
PRINT_LENGTH_CONTROL = 872_pages_in_Google_Books_Perlego / 850_Logos_digital_metadata
```

Perlego's 2025 ebook table of contents directly identifies:

```text
VII. Headdress in Public Worship (11:2–16)
VIII. Divisions at the Lord's Supper (11:17–34)
```

The accessible 2025 preview/index surfaces do **not** expose a reliable second-edition page number for section VII or its body. The previously circulated/project-working locator `pp.468–493` was re-searched against Baker/Logos/Google/Perlego and was not verified.

The older **first edition (2003)** is a separate evidence object. Its table of contents places “Headdress in Public Worship (11:2–16)” at pp.505–532, but those pages must **not** be silently transferred to the 2025 second edition.

```text
GARLAND_2025_2E_BOOK_OBJECT = VERIFIED
GARLAND_2025_2E_11_2_16_SECTION_IDENTITY = CLOSED
GARLAND_2025_2E_11_2_16_PAGINATION = UNVERIFIED_HOLD
GARLAND_2025_2E_TARGET_SECTION_BODY = HOLD
GARLAND_2025_PP468_493 = RETRACT_AS_UNVERIFIED_LOCATOR
GARLAND_2003_PP505_532 != GARLAND_2025_PAGINATION
```

Do not reconstruct the 2025 revision by copying Garland’s older edition wording or pagination unless edition continuity is directly checked.

## 4.4 Thiselton 2000

Google Books exposes multiple records for the NIGTC commentary; the correct work identity is secure. Targeted searches for `11:2`, `head covering`, `veil` and p.800 did not expose the target body on the accessible preview surfaces.

```text
THISELTON_2000_WORK = VERIFIED
THISELTON_GOOGLE_BOOKS_TARGET_SECTION = NOT_EXPOSED
THISELTON_2000_PP800_847 = HOLD
```

A 2011 shorter commentary is a different evidence object and must not silently replace the 2000 NIGTC body.

---

# 5. Current commentary queue

```text
GARLAND_2025_2E_11_2_16 = P0_PAGINATION_AND_DIRECT_BODY_HOLD
REASONER_2025_PP432_451 = P0_P1_DIRECT_CHAPTER_HOLD
STARLING_2025_1COR11 = P0_P1_SECTION_HOLD
GORMAN_2025_1COR11 = P1_SECTION_HOLD
THISELTON_2000_PP800_847 = HOLD
FEE_REVISED_2014_APPROX_PP542_586 = HOLD
CIAMPA_ROSNER_2010_PP503_540 = DETAIL_HOLD
```

```text
PREVIEW_ROUTE_EXHAUSTED_FOR_CURRENT_RUNTIME != SOURCE_UNAVAILABLE_GLOBALLY
CURRENT_EDITION_STATUS_ALONE != CLAIM_GRADE
```

---

# 6. Acquisition method

```text
1. publisher chapter / ebook preview
2. lawful library / institutional route
3. Google Books contents/snippet only for navigation
4. quote only after direct section body
5. reconcile any page claim against publisher TOC before using it as falsifier
6. record exhausted preview routes so the next pass changes transport instead of repeating queries
```

Do not ask the user for a copy before exhausting lawful routes available to the runtime.

---

# 7. Audit lessons

```text
SEARCH_INDEX_STRIPPED_VERSE_LABEL != SAFE_MANUAL_MAPPING
CHAPTER_SEQUENCE_MUST_BE_RECONCILED_WITH_PUBLISHER_TOC
DERIVED_FIREWALL_MUST_BE_REAUDITED_IF_ITS_PAGINATION_PREMISE_FAILS
SELF_CORRECTION > PRESERVING_A_CONVENIENT_REJECTION
CURRENT_EDITION != POSITION_VERIFIED
PREVIEW_NO_MATCH != ABSENCE_FROM_BOOK
LICENSED_SAMPLE_ROUTE != TARGET_SECTION_READ
EDITION_1_PAGINATION != EDITION_2_PAGINATION_AUTOMATICALLY
PRECISE_UNVERIFIED_PAGE_RANGE > NO_LOCATOR_IS_FALSE_PRECISION
```

---

# 8. Result

```text
REASONER_2025 = VERIFIED_CURRENT_TECHNICAL_COMMENTARY
REASONER_11_2_16 = APPROX_PP432_451 / DIRECT_BODY_HOLD
GORMAN_2025 = VERIFIED_CURRENT_THEOLOGICAL_COMMENTARY / SECTION_HOLD
STARLING_2025 = VERIFIED_CURRENT_COMMENTARY / 1COR11_CONTENT_HOLD
GARLAND_2025_2E_11_2_16 = SECTION_IDENTITY_CLOSED / PAGINATION_HOLD / BODY_HOLD

FEE_CIAMPA_GARLAND_THISELTON_LAWFUL_PREVIEW_ROUTES = TESTED_NO_TARGET_BODY_EXPOSED
NEXT_PASS_FOR_THESE_TARGETS = CHANGE_TRANSPORT_NOT_REPEAT_METADATA_SEARCH

CORE_GRADE_REVERSALS = 0
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
SITE_PUBLICATION = false
