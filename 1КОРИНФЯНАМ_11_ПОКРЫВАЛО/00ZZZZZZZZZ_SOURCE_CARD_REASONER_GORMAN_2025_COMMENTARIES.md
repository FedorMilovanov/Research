# Source card — Mark Reasoner / Michael J. Gorman, 1 Corinthians commentaries (2025)

**Дата аудита:** 2026-08-10  
**Статус:** `CURRENT-2025-COMMENTARY-INGRESS / DIRECT-PUBLISHER-METADATA / BODY-HOLD / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Purpose

Current-literature radar already tracked Garland 2025, Peters, Nõmmik and other recent work, but a fresh search exposed a major technical 2025 commentary that was not represented in Research at all:

> Mark Reasoner, *1 Corinthians*, Brill Exegetical Commentary Series 3 (2025).

Michael J. Gorman's 2025 Eerdmans commentary was mentioned only briefly in the radar but did not have a calibrated source card.

These works must **not** be treated as equal evidence classes:

```text
REASONER_2025 = TECHNICAL_EXEGETICAL_COMMENTARY / HIGH_VALUE_DIRECT_SECTION_HOLD
GORMAN_2025 = THEOLOGICAL_PASTORAL_MISSIONAL_COMMENTARY / CURRENT_INTERPRETIVE_CONTROL
```

No claim grade changes until the exact 11:2–16 sections are directly acquired and adversarially tested.

---

# 1. Mark Reasoner — *1 Corinthians* (Brill, 2025)

## 1.1 Direct publisher identity

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

The commentary is a major current technical work, not a devotional or popular exposition.

The Brill chapter platform visibly organizes analysis through categories such as:

```text
Translation
Text-Critical Analysis
Grammatical Analysis
Historical Analysis
Theological Analysis
```

The publisher/book description also emphasizes first-century Roman Corinth, patristic commentary and Paul's call for church unity.

Therefore:

```text
REASONER_2025_TECHNICAL_WEIGHT = HIGH_CURRENT_COMMENTARY
REASONER_2025_RECENCY = VERIFIED
```

---

# 2. Dedicated 1 Cor 11:2–16 chapter — not a passing excursus

Brill's own table of contents gives a dedicated chapter:

> **Commentary 7 — “Hair and Head Coverings in the Assembly (11:2–16)”**

This is followed by:

> Commentary 8 — “Keep the Lord's Supper (11:17–34)”

Google Books independently exposes chapter starts in the contents/index:

```text
11:2–16 / Commentary 7 begins about p.321
11:17–34 / Commentary 8 begins p.432
```

Thus the head-covering section occupies roughly:

```text
pp.321–431
~111 pages before the Lord's Supper section begins
```

The exact final printed page of Commentary 7 should still be confirmed from the Brill chapter record/PDF; `321–431` is a chapter-boundary inference from Google Books start pages, not a directly rendered Brill page-range field.

Safe status:

```text
REASONER_11_2_16_DEDICATED_CHAPTER = DIRECT_BRILL_TOC
REASONER_11_2_16_START_PAGE = GOOGLE_BOOKS_321
REASONER_11_17_START_PAGE = GOOGLE_BOOKS_432
REASONER_11_2_16_APPROX_SPAN = 321_431_INFERRED_FROM_BOUNDARIES
```

This scale alone moves Reasoner into the high-value acquisition queue.

---

# 3. Why Reasoner is P0/P1 for this project

A current 100+ page technical treatment can potentially update several nodes at once:

```text
κεφαλή
material covering vs hair
male head-state
female head-state
ἐξουσία v10
angels
Genesis/creation
φύσις
v16
Roman Corinth background
patristic reception
```

The project currently holds exact pages for Garland 2025, Starling 2025 and other current commentaries. Reasoner is now at least as important as those for direct technical adjudication because:

1. it is from 2025;
2. the series is explicitly exegetical;
3. the passage gets an unusually long dedicated chapter;
4. the book foregrounds Roman Corinth and patristic interpretation;
5. it can test whether the current registry still reflects the newest full technical commentary landscape.

Queue:

```text
P0/P1 REASONER_2025_COMMENTARY_7_FULL_BODY = ACQUIRE
```

---

# 4. Reasoner position — current fail-closed boundary

The Brill chapter body is currently institution/login gated.

Google Books gives contents/index metadata but the present pass did **not** recover a reliable official verse-by-verse body for Commentary 7.

Low-quality/popular webpages currently reproduce purported exact Reasoner page quotations for vv.2–8 and other verses. Those pages are useful only as **locator signals**, because:

- they are not Brill;
- provenance of the copied text is not independently established in this pass;
- page numbers can be wrong or copied circularly;
- excerpts can omit qualifications/notes.

## 4.1 Direct falsification of some circulated page labels

Google Books gives a hard pagination boundary:

```text
COMMENTARY_7_11_2_16_START = 321
COMMENTARY_8_11_17_34_START = 432
```

Therefore **any claimed 11:2–16 quotation assigned to p.432 or later cannot have the cited page number correct in this edition**.

At least two currently circulating web attributions fail this test:

```text
"Reasoner 2025 p.434" assigned to 1 Cor 11:2 = IMPOSSIBLE_PAGE_LABEL
"Reasoner 2025 p.444" assigned to 1 Cor 11:8 = IMPOSSIBLE_PAGE_LABEL
```

Both pages fall after the direct Google Books start of Commentary 8 (11:17–34) at p.432.

A circulated `p.343` attribution for v.3 at least falls inside the possible Commentary 7 span, but its wording still remains **unverified** because the Brill body itself has not been acquired.

This demonstrates that the web quotation chain is not merely lower-quality in theory; its pagination is **proven corrupt in specific cases**.

New firewall:

```text
REASONER_WEB_QUOTE_WITH_PAGE >= 432 AND CLAIMED_VERSE <= 11_16 = REJECT_PAGE_LABEL
REASONER_WEB_QUOTE_INSIDE_321_431 = LOCATOR_ONLY_UNTIL_BRILL_TEXT
LOW_QUALITY_EXACT_WORDING != QUOTE_SAFE
```

Do not “repair” an impossible page citation by silently changing the page number. Reacquire the primary text.

Therefore do **not** promote from those sites claims such as:

```text
Reasoner says kephale = hierarchy/authority
Reasoner says all women, not wives
Reasoner requires material covering
Reasoner gives a specific v10 exousia meaning
Reasoner identifies the angels in a particular way
```

until the Brill chapter itself is acquired.

Current status:

```text
REASONER_KEPHALE_POSITION = HOLD
REASONER_VEIL_HAIR_POSITION_DETAIL = HOLD
REASONER_EXOUSIA_POSITION = HOLD
REASONER_ANGELS_POSITION = HOLD
REASONER_PHYSIS_POSITION = HOLD
REASONER_V16_POSITION = HOLD
```

The chapter title alone establishes that Reasoner treats **hair and head coverings** as the problem-space; it does not establish how he adjudicates them.

---

# 5. Reasoner acquisition routes

Direct lawful routes identified:

```text
BRILL_CHAPTER_PLATFORM = institutional login / paid PDF / preview
GOOGLE_BOOKS = contents/index + limited snippets
LIBRARY_EBOOK = possible institutional Brill access
```

Do not ask the user for a copy before exhausting institutional/library/preview access.

```text
REASONER_USER_ACQUISITION = SELF_EXHAUST_FIRST
```

---

# 6. Michael J. Gorman — *1 Corinthians* (Eerdmans, 2025)

## 6.1 Direct publisher identity

Eerdmans directly verifies:

> Michael J. Gorman, *1 Corinthians: A Theological, Pastoral, and Missional Commentary* (2025).

Direct metadata:

```text
AUTHOR = Michael J. Gorman
PUBLISHER = Eerdmans
PUBLICATION_DATE = 2025-03-06
EBOOK_ISBN = 9781467465748
HARDCOVER_ISBN = 9780802882660
LENGTH = 477 pages
```

Google Books independently confirms 477 pages and the March 6, 2025 publication date.

---

# 7. Gorman's evidence class

Eerdmans explicitly describes the volume as a commentary that:

- gives careful exposition of 1 Corinthians;
- stresses theological content;
- focuses on spiritual, pastoral and missional implications;
- interprets the letter around the church as **one, holy, catholic and apostolic**;
- includes reflection questions and topical sidebars.

This is a serious scholarly commentary, but its declared purpose differs from Brill Reasoner's technical exegetical series.

Therefore:

```text
GORMAN_2025 = R2/P1_CURRENT_THEOLOGICAL_COMMENTARY_CONTROL
GORMAN_2025 != PRIMARY_TECHNICAL_TEXT_CRITICAL_OWNER
```

It is valuable for:

```text
whole-passage synthesis
Pauline theology
church/ecclesiology
pastoral application
current reception
```

and less likely than Reasoner to be the controlling source for a disputed papyrological or grammatical microclaim.

---

# 8. Gorman 11:2–16 position — direct-section HOLD

The direct Eerdmans page does not expose the 11:2–16 body in this pass.

Google Books supplies book metadata/partial contents but did not expose a quote-safe relevant section.

A later 2026 article and other secondary sites summarize/quote Gorman as reading men and women as both praying/prophesying and the dispute in terms of culturally intelligible gender/modesty/order rather than a simple ban on female authority.

Those are **locator-only** until the Eerdmans text itself is acquired.

Therefore:

```text
GORMAN_11_2_16_DIRECT_BODY = HOLD
GORMAN_VEIL_HAIR_POSITION = HOLD
GORMAN_KEPHALE_POSITION = HOLD
GORMAN_EXOUSIA_POSITION = HOLD
GORMAN_ANGELS_POSITION = HOLD
```

Do not import a secondary paraphrase into the claim registry as “Gorman 2025 says”.

---

# 9. Relative acquisition priority

```text
P0/P1 Reasoner 2025 Commentary 7 = HIGH
P1 Gorman 2025 exact 11:2–16 section = MEDIUM_HIGH
```

Why Reasoner first:

```text
DEDICATED_LONG_SECTION
+ TECHNICAL_SERIES
+ TEXT_CRITICAL/GRAMMATICAL/HISTORICAL_METHOD
+ ROMAN_CORINTH_FOCUS
```

Why Gorman still matters:

```text
CURRENT_MAJOR_NT_SCHOLAR
+ DIRECT_2025_FULL_COMMENTARY
+ THEOLOGICAL_SYNTHESIS
+ ECCLESIOLOGICAL_APPLICATION
```

---

# 10. Effect on current literature radar

Reasoner is a genuine radar omission and should be added to the high-value current commentary queue.

Gorman was previously only a brief radar note; this card gives it proper evidence-class separation.

Current high-value 2025 commentary set now includes at minimum:

```text
GARLAND_2025_2E = P0_DIRECT_TEXT_HOLD
REASONER_2025_BRILL = P0/P1_DIRECT_CHAPTER_HOLD
STARLING_2025_EBTC = P0/P1_SECTION_HOLD
GORMAN_2025_EERDMANS = P1_THEOLOGICAL_SECTION_HOLD
```

Drake 2025 and Peters 2025 remain thematic/specialist monographs rather than verse-by-verse commentary equivalents.

---

# 11. No grade change from mere existence

The discovery of two current commentaries does **not** itself change any current claim.

```text
CORE_GRADE_REVERSALS = 0
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH
EXOUSIA_EXACT_REFERENT = B_C
```

Reasoner/Gorman matter because they are current pressure-tests still to be read directly, not because publication year is authority.

---

# 12. Result

```text
REASONER_2025 = GENUINE_MISSING_CURRENT_TECHNICAL_COMMENTARY
REASONER_COMMENTARY_7 = DIRECT_BRILL_TOC_VERIFIED
REASONER_CH7_START = P321_GOOGLE_BOOKS
REASONER_NEXT_SECTION_START = P432_GOOGLE_BOOKS
REASONER_APPROX_11_2_16_SPAN = P321_431_BOUNDARY_INFERENCE
REASONER_BODY = HOLD
REASONER_WEB_P434_AS_11_2 = REJECTED_IMPOSSIBLE_PAGE_LABEL
REASONER_WEB_P444_AS_11_8 = REJECTED_IMPOSSIBLE_PAGE_LABEL

GORMAN_2025 = VERIFIED_CURRENT_EERDMANS_COMMENTARY
GORMAN_EVIDENCE_CLASS = THEOLOGICAL_PASTORAL_MISSIONAL
GORMAN_11_2_16_BODY = HOLD

LOW_QUALITY_REASONER_QUOTES = DISCOVERY_ONLY
CORE_GRADE_REVERSALS = 0
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
SITE_PUBLICATION = false
```
