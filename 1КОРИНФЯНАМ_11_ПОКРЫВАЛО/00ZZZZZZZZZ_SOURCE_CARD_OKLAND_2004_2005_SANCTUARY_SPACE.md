# Source card — Jorunn Økland, *Women in Their Place* (2004/2005)

**Дата аудита:** 2026-08-10  
**Статус:** `FOUNDATIONAL-SPECIALIST-MONOGRAPH / CORINTH-ARCHAEOLOGY / GENDERED-RITUAL-SPACE / DIRECT-PUBLISHER-METADATA / BODY-DETAIL-HOLD / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Why this source is being added

Susanna Drake’s 2025 Cambridge bibliography includes Jorunn Økland’s *Women in Their Place*. A repository search on the current branch found no dedicated Økland owner by author/title or `sanctuary space` terminology.

This is not a current-2025 source and must **not** be inserted into the 2024–2026 radar as if newly published. It is a missing foundational specialist control for a distinct model:

```text
ARCHAEOLOGICAL_ROMAN_CORINTH
+ GENDER_DISCOURSE
+ RITUAL_SANCTUARY_SPACE
+ 1_CORINTHIANS_11_14
```

```text
MISSING_FROM_REPO != NEW_SCHOLARSHIP
OLD_BUT_FOUNDATIONAL != CURRENT_EDITION
DRAKE_CITES_OKLAND != DRAKE_ENDORSES_EVERY_OKLAND_CLAIM
```

---

# 1. Direct publisher identity

Bloomsbury / T&T Clark directly verifies:

> Jorunn Økland, *Women in Their Place: Paul and the Corinthian Discourse of Gender and Sanctuary Space*.

Publisher routes:

- https://www.bloomsbury.com/uk/women-in-their-place-9780567012708/
- https://www.bloomsbury.com/us/women-in-their-place-9780567084071/

Direct publisher description states that Økland:

- takes the archaeological remains at Corinth as a starting point;
- develops an interdisciplinary reading of Paul’s statements on women in 1 Cor 11–14;
- treats the Pauline assembly as ritual space distinct from domestic space;
- assesses the text against several gender models found in temple architecture, ritual and literary evidence.

Therefore the minimum source-specific model is:

```text
OKLAND_1COR11_14 = GENDER_AND_RITUAL_SANCTUARY_SPACE_MODEL
OKLAND_USES_CORINTH_ARCHAEOLOGY = DIRECT_PUBLISHER_VERIFIED
OKLAND_INTERDISCIPLINARY_MATERIAL_CULTURE_SCOPE = DIRECT_PUBLISHER_VERIFIED
```

---

# 2. Publication-history firewall

Different surfaces expose different format years/page systems.

The scholarly print citation is commonly:

> Jorunn Økland, *Women in Their Place: Paul and the Corinthian Discourse of Gender and Sanctuary Space*, JSNTSup 269 (London/New York: T&T Clark International, 2004), x + 328 pp.

Independent JTS bibliographic review confirms the 328-page print object and publication family.

Bloomsbury’s current product pages expose 2005 paperback/ebook metadata; Google Books exposes a 2005 A&C Black record with a different digital page count.

Therefore:

```text
OKLAND_ORIGINAL_SCHOLARLY_BOOK = 2004_PRINT_CITATION_FAMILY
OKLAND_BLOOMSBURY_CURRENT_FORMAT_RECORDS = 2005_FORMAT_METADATA
2004_2005 != TWO_DIFFERENT_ARGUMENTS_AUTOMATICALLY
DIGITAL_PAGE_COUNT != SAFE_PRINT_LOCATOR
```

Do not mix page locators across these format records.

---

# 3. Direct / strong thesis control

Anthony C. Thiselton’s *Journal of Theological Studies* review quotes Økland’s stated thesis from p.1 in substance: Paul’s exhortations about women’s ritual roles and ritual clothing in 1 Cor 11–14 structure/gender the Christian gathering as a ritual “sanctuary space.”

JTS route:

- https://academic.oup.com/jts/article-abstract/58/1/236/2931832

A separate scholarly review in ProQuest independently reproduces the same p.1 thesis and explains that, for Økland, ritual space is neither simply private nor public but a distinct socially constructed domain.

Safe source-specific result:

```text
OKLAND_THESIS_GENDERED_SANCTUARY_SPACE = STRONG_PAGE_SPECIFIC_REVIEW_CONTROL
OKLAND_MAIN_POINT_IS_NOT_SIMPLY_VEIL_OBJECT = STRONG_REVIEW_CONTROL
```

This does not yet authenticate every sentence of the book body.

---

# 4. Structure / archaeological emphasis

Google Books table of contents gives a useful acquisition map:

```text
CH2 FROM_WOMAN_TO_WOMAN_FROM_CHURCH_TO_EKKLESIA_SPACE = p6
CH3 GENDER_AETIOLOGIES_AND_DISCURSIVE_CONSTRUCTION_OF_SPACES = p39
CH4 PLACES_FOR_WOMEN_IN_EARLY_ROMAN_CORINTH_RITUAL_SANCTUARY_SPACES = p78
CH5 PAUL_AND_THE_DISCOURSE_OF_SANCTUARY_SPACE = p131
CH6 CORINTHIAN_ORDER = p168
CH7 OBEDIENT_AND_SUBVERSIVE = p224
```

Google Books route:

- https://books.google.com/books/about/Women_in_Their_Place.html?id=kSkJ_LtXlj8C

The TOC is navigational evidence, not direct proof of particular page-level arguments.

---

# 5. Distinction from existing models

Økland should not be collapsed into any one of these:

```text
MATERIAL_VEIL_ONLY
HAIR_ONLY
ROMAN_CAPITE_VELATO_TRIGGER
WIFE_FREEWOMAN_STATUS_ONLY
LARGE_QUOTATION_REFUTATION
```

Her direct publisher-level distinctiveness is the **space-and-gender architecture** of the Pauline ritual gathering, informed by Roman Corinthian archaeology/material culture.

This makes her especially useful as a control against reducing 1 Cor 11:2–16 to one portable clothing artifact detached from the assembly’s ritual/social space.

Project label:

```text
OKLAND_GENDERED_SANCTUARY_SPACE_MODEL = C_SERIOUS_FOUNDATIONAL_CONTEXTUAL_MODEL
```

This is a model-status label, not a claim-grade reversal.

---

# 6. Relation to Drake 2025

Drake’s Cambridge bibliography directly includes:

> Økland, Jorunn. *Women in Their Place: Paul and the Corinthian Discourse of Gender and Sanctuary Space*.

Cambridge bibliography route:

- https://www.cambridge.org/core/books/veiling-in-the-late-antique-world/bibliography/A39E22902B22BEF73750AE16C6527604

Safe inference:

```text
DRAKE_2025_KNOWS_AND_CITES_OKLAND = DIRECT_BIBLIOGRAPHIC_FACT
DRAKE_2025_ENDORSES_OKLAND_WHOLE_MODEL = NOT_ESTABLISHED
```

The two models can be compared later after direct chapter/body acquisition.

---

# 7. What remains HOLD

Without a direct full-body acquisition in this pass, do not assign Økland a detailed position on:

```text
OKLAND_MATERIAL_VEIL_VS_HAIR = HOLD
OKLAND_KEPHALE_EXACT_POSITION = HOLD
OKLAND_EXOUSIA_EXACT_POSITION = HOLD
OKLAND_ANGELS_EXACT_POSITION = HOLD
OKLAND_PHYSIS_EXACT_POSITION = HOLD
OKLAND_V16_EXACT_POSITION = HOLD
OKLAND_EXACT_CORINTH_TRIGGER = HOLD
```

Secondary descriptions may be used as locators only.

---

# 8. Acquisition priority

Because Økland is a monograph-length archaeological/gender-space treatment centered on 1 Cor 11–14, direct body acquisition is valuable but lower priority than current technical commentaries needed for current-edition closure.

```text
P0/P1 REASONER_2025_DIRECT_BODY
P0 GARLAND_2025_DIRECT_BODY
P1 DRAKE_2025_CH2_DIRECT_BODY
P1/P2 OKLAND_2004_CH4_7_DIRECT_BODY
```

---

# 9. No grade change

```text
CORE_GRADE_REVERSALS = 0
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
ROMAN_CAPITE_VELATO_BACKGROUND = A
EXACT_CORINTH_TRIGGER = RECONSTRUCTION_LAYER
OKLAND_GENDERED_SANCTUARY_SPACE_MODEL = C_SERIOUS_FOUNDATIONAL_CONTEXTUAL_MODEL
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
SITE_PUBLICATION = false
```
