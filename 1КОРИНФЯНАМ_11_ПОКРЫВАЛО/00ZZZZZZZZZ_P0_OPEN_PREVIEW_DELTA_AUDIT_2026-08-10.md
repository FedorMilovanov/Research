# 1 Коринфянам 11:2–16 — P0 open-preview delta audit

**Дата:** 2026-08-10  
**Статус:** `RESEARCH-ONLY / OPEN-PREVIEW-EXHAUSTION / P0-DELTA / PUBLICATION-HOLD`  
**Цель:** максимально уменьшить зависимость от закрытых комментариев **до** запроса материалов у пользователя; не имитировать чтение закрытых страниц.

---

## 0. Жёсткое правило этого прохода

```text
DO_NOT_REQUEST_FROM_USER_IF_AGENT_CAN_ACCESS = true
DO_NOT_INFER_CURRENT_EDITION_POSITION_FROM_OLD_EDITION = true
DO_NOT_PROMOTE_SECONDARY_QUOTE_TO_PRIMARY_EVIDENCE = true
DO_NOT_TREAT_PREVIEW_METADATA_AS_FULL_EXEGESIS = true
NO_GRADE_CHANGE_WITHOUT_DIRECT_EVIDENCE = true
PRODUCT_WRITE = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
```

Этот слой отвечает не на вопрос «что, вероятно, думает комментатор», а на три более строгих вопроса:

1. Что удаётся подтвердить **прямо** из current edition / publisher / author-level route?
2. Что удалось закрыть на уровне macro-thesis, но не detailed exegesis?
3. Что честно остаётся `HOLD_FULL_SECTION` до section + notes?

---

# 1. P0-1 — Gordon D. Fee, NICNT Revised (2014)

## 1.1. Что подтверждено напрямую

**Current witness:** Gordon D. Fee, *The First Epistle to the Corinthians, Revised Edition*, NICNT, Eerdmans, 2014.

Primary routes:

- Eerdmans current product page: https://www.eerdmans.com/9780802871367/the-first-epistle-to-the-corinthians-revised-edition/
- Google Books current 2014 revised edition: https://books.google.com/books/about/The_First_Epistle_to_the_Corinthians_Rev.html?id=mk64EQAAQBAJ
- Biblia/Logos embedded preview resource: `LLS:NICNT67CO1_2ED`

Directly confirmed:

- revised edition, not 1987 first edition;
- publication date 2014-11-30;
- Eerdmans lists 1044 pages for the print edition;
- the revised edition explicitly takes account of substantial scholarship from the preceding twenty-five years;
- the embedded preview identifies copyright 1987/2014 and distinguishes `First edition 1987` / `Revised edition 2014`;
- open embedded preview currently exposes front matter/TOC but truncates before the relevant 11:2–16 exposition.

## 1.2. What is **not** promoted from secondary web quotations

Open web contains pages attributing detailed language to Fee Revised around p.563, including a preference for an external/material covering while acknowledging hairstyle as a viable alternative.

However:

```text
FEE_2014_DETAIL_FROM_SECONDARY_QUOTATIONS = DISCOVERY_ONLY
```

Reason: in this pass the exact revised page was not recovered through a direct book-text route. The old 1987 Fee position is well documented but cannot be silently substituted for the 2014 revision.

Therefore:

```text
FEE_REVISED_MATERIAL_COVERING_POSITION = HOLD_DIRECT_PAGE
FEE_REVISED_KEPHALE_POSITION = HOLD_DIRECT_PAGE
FEE_REVISED_EXOUSIA_POSITION = HOLD_DIRECT_PAGE
FEE_REVISED_ANGELS_POSITION = HOLD_DIRECT_PAGE
FEE_REVISED_PHYSIS_POSITION = HOLD_DIRECT_PAGE
FEE_REVISED_APPLICATION_POSITION = HOLD_DIRECT_PAGE
```

## 1.3. Delta for our synthesis

No core grade changes from Fee in this pass.

What changes is evidential hygiene:

- `Fee 1987` can be used as historical/continuity witness only;
- `Fee Revised 2014` remains a genuine P0 current-position control;
- no statement such as “Fee Revised definitely says X” should be made from an old-edition locator.

## 1.4. Remaining acquisition target

Still needed:

**approx. pp. 542–586 + notes/addendum**, full revised section.

Marginal value remains very high because this is a substantive revision and detailed direct text remains mostly closed.

---

# 2. P0-2 — Anthony C. Thiselton, NIGTC (2000)

## 2.1. New direct route that partially reduces uncertainty

Primary/open bibliographic route:

- Google Books, *1 Corinthians: A Shorter Exegetical and Pastoral Commentary*:
  https://books.google.com/books/about/1_Corinthians.html?id=ZK1zclFQYgEC
- additional 2011 electronic/reprint route:
  https://books.google.com/books/about/1_Corinthians.html?id=CRbb9_QLVh8C

The publisher description directly says that Thiselton’s shorter commentary **draws on the exegesis of his 2000 NIGTC volume** and combines it with pastoral/application material.

This establishes:

```text
THISELTON_SHORTER_DERIVES_FROM_NIGTC = A_BIBLIOGRAPHIC
THISELTON_CORE_POSITION_CAN_BE_PARTIALLY_TRIANGULATED = true
THISELTON_NIGTC_TECHNICAL_NOTES_SUPERSEDED = false
```

The shorter commentary TOC places the 11:2–16 discussion inside a section beginning around p.169 (`Mutual Respect in Matters of Public ...`). The open Google Books route exposes metadata/TOC and common-term indexing, but not a stable full text of the relevant pages in this pass.

## 2.2. Secondary quote leads — intentionally not promoted

Search results reproduce recognizable Thiselton formulations on:

- `κεφαλή` as prominence / foremost / representative whole rather than a simple lexical identity with “authority over”;
- `ἐξουσία` in v.10 as a possible badge of honour / self-mastery.

These leads are important for target acquisition but remain:

```text
THISELTON_KEPHALE_SECONDARY_QUOTE = DISCOVERY_ONLY
THISELTON_EXOUSIA_SECONDARY_QUOTE = DISCOVERY_ONLY
```

until recovered from the direct NIGTC/shorter text itself.

## 2.3. Delta for acquisition priority

Thiselton remains P0 because:

- NIGTC 2000 is the technical argument with extensive lexical bibliography;
- the shorter commentary does **not** replace footnotes, lexical discussion, interaction with competing scholarship, or the detailed argument around pp.800–847.

But marginal uncertainty is now lower than before for **author-position discovery**.

```text
THISELTON_POSITION_DISCOVERY_DEPENDENCE = PARTIALLY_REDUCED
THISELTON_TECHNICAL_DELTA_DEPENDENCE = HIGH
```

## 2.4. Remaining target

Need full **pp.800–847 + notes**.

Known locators remain:

- section 11:2–16 begins p.800;
- `κεφαλή` around p.812;
- v.4 covering/long hair around p.823;
- vv.5–6 around p.828;
- vv.7–9 around p.834;
- `ἐξουσία` around p.838;
- `φύσις` around p.844;
- 11:17 begins p.848.

---

# 3. P0-3 — David E. Garland, BECNT 2nd ed. (2025)

## 3.1. Current edition is now independently locked

Primary/current routes:

- Baker Academic author/catalog route lists a distinct **1 Corinthians 2nd Edition** (ISBN 9781540962607).
- Perlego current edition page:
  https://www.perlego.com/book/4918566/1-corinthians-baker-exegetical-commentary-on-the-new-testament-pdf

Direct current-edition data:

- year: 2025;
- current second edition;
- publisher: Baker Academic;
- current ebook ISBN 9781493451692;
- current TOC retains the unit title **`VII. Headdress in Public Worship (11:2–16)`**;
- the current edition says it has been **updated throughout** for recent scholarship;
- it retains detailed interaction with the Greek text, ancient writings and extensive research.

## 3.2. Critical non-inference rule

The fact that the 2025 edition retains the same section title as the 2003 edition does **not** establish continuity of detailed exegesis.

```text
GARLAND_2003_TO_2025_SECTION_TITLE_CONTINUITY = A
GARLAND_2003_TO_2025_EXEGETICAL_CONTINUITY = HOLD
GARLAND_2025_UPDATED_THROUGHOUT = A_PUBLISHER
```

Therefore old 2003 page quotations may be retained as historical Garland evidence, but they must not be presented as the final current Garland position unless checked against 2025.

## 3.3. Specific unresolved current-edition deltas

The following require the current 2025 section itself:

```text
GARLAND_2025_MATERIAL_VS_HAIR = HOLD_FULL_SECTION
GARLAND_2025_KEPHALE = HOLD_FULL_SECTION
GARLAND_2025_ROMAN_SOCIAL_TRIGGER = HOLD_FULL_SECTION
GARLAND_2025_WIVES_VS_WOMEN = HOLD_FULL_SECTION
GARLAND_2025_EXOUSIA = HOLD_FULL_SECTION
GARLAND_2025_ANGELS = HOLD_FULL_SECTION
GARLAND_2025_PHYSIS = HOLD_FULL_SECTION
GARLAND_2025_V16_CUSTOM = HOLD_FULL_SECTION
GARLAND_2025_APPLICATION = HOLD_FULL_SECTION
```

## 3.4. Marginal-information consequence

Because this edition is both **new (2025)** and explicitly **updated throughout**, it now carries the greatest risk of hidden current-position drift if we rely on older citations.

This does not make Garland intrinsically “more authoritative” than Thiselton/Fee; it makes Garland 2025 **high marginal-information priority** for a delta audit.

---

# 4. P0-4 — Roy E. Ciampa & Brian S. Rosner, PNTC (2010)

## 4.1. Current commentary identity

Primary publisher route:

- Eerdmans: https://www.eerdmans.com/9780802837325/the-first-letter-to-the-corinthians/
- Google Books: https://books.google.com/books/about/The_First_Letter_to_the_Corinthians.html?id=dP-AEAAAQBAJ

Confirmed:

- PNTC;
- publication 2010-11-09;
- Eerdmans current page lists 990 pages;
- later IVP publication routes appear to be publication-format/territory routes, not evidence of a substantive new revised edition.

## 4.2. Major new direct author-level closure

A 2011 interview with Roy Ciampa specifically asks for the main message of **their coauthored commentary** on 1 Cor 11:2–16. Ciampa answers in first-person plural: `We argue ...`.

Direct interview:

https://newtestamentperspectives.blogspot.com/2011/07/interview-with-roy-ciampa-1-corinthians_31.html

The author-level summary establishes the following macro-thesis:

```text
CIAMPA_ROSNER_GLORY_HONOR_SHAME_FRAME = DIRECT_AUTHOR_SUMMARY
CIAMPA_ROSNER_HEADCOVERINGS_HAVE_ROMAN_SOCIAL_SIGNIFICANCE = DIRECT_AUTHOR_SUMMARY
CIAMPA_ROSNER_PUBLIC_CHURCH_MEETINGS_CONTEXT = DIRECT_AUTHOR_SUMMARY
CIAMPA_ROSNER_HUSBANDS_WIVES_SHAME_FRAME = DIRECT_AUTHOR_SUMMARY
CIAMPA_ROSNER_GENESIS_1_2_DEFENDS_AND_RELATIVIZES_DISTINCTIONS = DIRECT_AUTHOR_SUMMARY
```

Important qualification: Ciampa explicitly says he is oversimplifying because the commentary gives the full argument. Therefore this closes **macro-position discovery**, not detailed exegesis.

## 4.3. Consequence for wives/all-women issue

The interview uses **husbands and wives** when summarizing their principal concern.

This is genuine evidence that marriage is central in their model, but it does not by itself prove they limit every occurrence of `γυνή` in 11:2–16 exclusively to wives.

Therefore:

```text
CIAMPA_ROSNER_MARRIAGE_FRAME = B_HIGH_DIRECT_SUMMARY
CIAMPA_ROSNER_ALL_GYNE_EXCLUSIVELY_WIVES = HOLD_FULL_SECTION
```

This fits the project’s current `WIVES_VS_ALL_WOMEN = OPEN_B_C` rather than closing it.

## 4.4. What still requires pp.503–540 + notes

```text
CIAMPA_ROSNER_V3_KEPHALE = HOLD_DETAIL
CIAMPA_ROSNER_V4_6_EXACT_COVERING_FORM = HOLD_DETAIL
CIAMPA_ROSNER_V10_EXOUSIA = HOLD_DETAIL
CIAMPA_ROSNER_V10_ANGELS = HOLD_DETAIL
CIAMPA_ROSNER_V13_15_PHYSIS = HOLD_DETAIL
CIAMPA_ROSNER_V16_SYNETHIA = HOLD_DETAIL
CIAMPA_ROSNER_FOOTNOTE_SOURCE_CHAIN = HOLD_DETAIL
```

Known section locators:

- 11:2–16 p.503;
- v.3 p.506;
- vv.4–6 p.511;
- vv.7–12 p.522;
- vv.13–16 p.537.

## 4.5. Side benefit: direct control on 14:34–35

The same interview also directly confirms their canonical reconciliation:

- they regard interpolation as unlikely;
- they do **not** read the command as absolute female silence because 11:5 already permits female prayer/prophecy;
- their preferred reconstruction concerns inappropriate questions, with prophecy-evaluation treated as another weighed alternative.

This is consistent with, but does not replace, the project’s broader independent textual audit of 14:34–35.

---

# 5. P0 claim delta matrix — what actually changed

| Node | Before this pass | New evidence | Result |
|---|---|---|---|
| Fee Revised identity | known | direct Eerdmans + embedded 2014 preview | strengthened metadata only |
| Fee detailed 11:2–16 | P0 closed | direct preview still truncates | **still HOLD** |
| Thiselton author-position route | mostly closed NIGTC | shorter commentary explicitly derives from NIGTC | **partial uncertainty reduction** |
| Thiselton technical argument | P0 | no stable full relevant pages | **still HOLD** |
| Garland current witness | 2025 2e known | current TOC + “updated throughout” locked | **continuity with 2003 must not be assumed** |
| Ciampa/Rosner macro-thesis | P0 detail only | direct Ciampa `We argue` summary | **macro-thesis partly closed** |
| Ciampa/Rosner lexical details | P0 | interview intentionally compressed | **still HOLD** |

No A/B/C core synthesis grade is changed solely by this pass.

---

# 6. Marginal-information priority after open-web exhaustion

This is **not** a ranking of scholarly quality. It ranks what closed material is most likely to add *new information* beyond what is already recovered.

## Tier P0-Δ1 — Garland 2025 2nd ed.

Reason:

- newest witness;
- explicitly updated throughout;
- detailed current section unavailable;
- old 2003 wording cannot be presumed current.

Need: complete `Headdress in Public Worship (11:2–16)` + notes.

## Tier P0-Δ1 — Fee Revised 2014

Reason:

- current revised position matters;
- revision explicitly engages 25 years of scholarship;
- current detailed section remains mostly closed.

Need: approx. pp.542–586 + notes/addendum.

## Tier P0-Δ2 — Thiselton NIGTC 2000

Reason:

- still unmatched for technical lexical/source-chain detail;
- but author-position discovery is partly triangulable through the shorter commentary.

Need: pp.800–847 + notes.

## Tier P0-Δ2 — Ciampa/Rosner PNTC 2010

Reason:

- direct author interview now closes macro-thesis;
- detailed lexical/footnote decisions still matter.

Need: pp.503–540 + notes.

Again: this ranking measures **marginal delta**, not intrinsic authority.

---

# 7. What this pass forbids agents from saying

Do **not** say:

- “Fee 2014 definitely retained every 1987 conclusion.”
- “Thiselton’s shorter commentary makes the NIGTC unnecessary.”
- “Garland 2025 is basically Garland 2003 with a new cover.”
- “Ciampa/Rosner address only married women in every verse.”
- “A retailer/secondary blog quote is equivalent to reading the current commentary page.”

Instead use:

```text
CURRENT_EDITION_DIRECT = claim can be attributed to current edition/author route
MACRO_CLOSED = author’s overall model is known
DETAIL_HOLD = verse-level argument/notes not directly recovered
DISCOVERY_ONLY = secondary quotation points us to a page but is not authority
```

---

# 8. Conservative synthesis after P0 delta pass

No reversal:

```text
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
KEPHALE_HEADSHIP_AUTHORITY = B_LEADING
KEPHALE_SOURCE_ONLY = C_VIABLE
EXOUSIA_WOMAN_SUBJECT = A_SYNTAX
EXOUSIA_REFERENT = B_C
HOLY_LITURGICAL_ANGELS = B_LEADING
WATCHERS = C
ROMAN_CAPITE_VELATO_BACKGROUND = A
EXACT_CORINTH_TRIGGER = B_RECONSTRUCTION
WIVES_VS_ALL_WOMEN = OPEN_B_C
WOMEN_PRAY_PROPHESY_11_5 = A
MUTUAL_INTERDEPENDENCE_11_11_12 = A
```

The P0 pass mostly improves **source discipline**, not conclusions.

---

# 9. Next closed-material protocol

If a P0 section becomes available later:

1. read the entire unit, not isolated page screenshots;
2. capture footnotes around the exact disputed node;
3. compare against the current adversarial audit, not against an old draft;
4. produce a `DELTA_RECEIPT` with only:
   - confirmed existing grade;
   - upgraded grade;
   - downgraded grade;
   - new unresolved issue;
   - superseded old assumption;
5. never overwrite the history silently.

Until then:

```text
P0_FULL_SECTION_HOLD = true
CORE_SYNTHESIS_REMAINS_ACTIVE = true
PUBLICATION_HOLD = true
```
