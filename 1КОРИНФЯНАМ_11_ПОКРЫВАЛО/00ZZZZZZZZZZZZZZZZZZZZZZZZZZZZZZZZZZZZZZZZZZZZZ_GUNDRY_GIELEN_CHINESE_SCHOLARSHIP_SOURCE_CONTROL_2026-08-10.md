# 1 Коринфянам 11:2–16 — Gundry-Volf / Gielen / Chinese scholarship source-control delta

**Дата:** 2026-08-10  
**Статус:** `MULTILINGUAL-SCHOLARSHIP / SOURCE-ATTRIBUTION / FULLTEXT-HOLDS / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Purpose

Этот слой закрывает три часто цитируемых, но неравномерно доступных научных линии:

1. Judith M. Gundry-Volf 1997 — creation / gender / “in the Lord”;
2. Marlis Gielen 1999 — German hairstyle model and sex-role symbolism;
3. Hao Li 2023 — Chinese-language creation-order / contextualization study.

Главное правило:

```text
OFFICIAL_METADATA != FULL_ARGUMENT
PAGE_SPECIFIC_SECONDARY_ATTESTATION != DIRECT_CHAPTER_BODY
UNOFFICIAL_TEXT_MIRROR != QUOTE_SAFE_PRIMARY_PUBLICATION_OBJECT
ABSTRACT_RESULT != ARTICLE_BODY_CLOSED
```

---

# 1. Judith M. Gundry-Volf 1997 — bibliography direct, body still HOLD

## 1.1 Bibliographic ownership

Direct author CV / institutional and scholarly bibliography controls verify:

> Judith M. Gundry-Volf, “Gender and Creation in 1 Corinthians 11:2–16: A Study in Paul’s Theological Method,” in *Evangelium, Schriftauslegung, Kirche: Festschrift für Peter Stuhlmacher zum 65. Geburtstag*, ed. Jostein Ådna, Scott J. Hafemann, Otfried Hofius (Göttingen: Vandenhoeck & Ruprecht, 1997), 151–171.

Routes:

- Yale/author CV: https://yale.academia.edu/JudithGundry/CurriculumVitae
- BYU selected bibliography: https://byustudies.byu.edu/online-book/pauls-first-epistle-to-the-corinthians/2004

```text
GUNDRY_VOLF_1997_BIBLIOGRAPHY = DIRECT/INSTITUTIONAL_VERIFIED
GUNDRY_VOLF_FULL_CHAPTER_BODY = HOLD
```

## 1.2 Page-specific claims independently attested in Cambridge scholarship

Julie Newberry’s Cambridge *NTS* article gives exact Gundry-Volf page locators in its scholarly apparatus:

- p.162: Gundry-Volf on the Genesis-origin language around 1 Cor 11:8/12;
- p.163: Gundry-Volf emphasizes that Paul’s `ἐκ` / `διά` formulations preserve a difference between man and woman even while vv11–12 assert interdependence.

Cambridge route:

- https://www.cambridge.org/core/journals/new-testament-studies/article/abs/pauls-allusive-reasoning-in-1-corinthians-11712/EDE6D54A62D2265EA2C22291B6F2BA39

Safe result:

```text
GUNDRY_VOLF_CREATION_DIFFERENCE_PP162_163 = STRONG_PAGE_SPECIFIC_B1_ATTESTATION
GUNDRY_VOLF_INTERDEPENDENCE_DOES_NOT_ERASE_DIFFERENCE = STRONG_PAGE_SPECIFIC_B1_ATTESTATION
```

These page locators are stronger than generic internet summaries but still do not substitute for direct chapter custody.

## 1.3 Broader theological profile — multiple secondary controls, not direct body

Penner/Vander Stichele’s 2004/2005 discussion summarizes Gundry-Volf as reading the passage through two simultaneously operative social/theological contexts:

- culturally specific gender differentiation and avoidance of shame;
- egalitarian/mutualizing pressure in creation and especially Christian existence “in the Lord”.

Accessible text route (use as secondary discussion, not as direct Gundry body):

- https://www.researchgate.net/publication/400247524_Unveiling_Paul_Gendering_Ethos_in_1_Corinthians_112-16

Thus:

```text
GUNDRY_VOLF_CULTURAL_DIFFERENTIATION_PLUS_IN_LORD_EQUALIZING_PRESSURE = STRONG_SECONDARY_ATTESTED
```

## 1.4 Hair/hairstyle attribution — keep calibrated

Multiple bibliographic/secondary sources place Gundry-Volf in a hair/hairstyle rather than textile-veil family, but the direct chapter was not acquired in this pass.

Therefore:

```text
GUNDRY_VOLF_HAIR_MODEL = STRONG_SECONDARY_ATTESTED
GUNDRY_VOLF_EXACT_HAIR_FORM = FULLTEXT_HOLD
```

Do not write a direct quote or precise hairstyle reconstruction in Gundry-Volf’s name without pp.151–171.

---

# 2. Marlis Gielen 1999 — not simply “loose hair”; modified short-hair hypothesis

## 2.1 Verified publication and author-reprint structure

Original article:

> Marlis Gielen, “Beten und Prophezeien mit unverhülltem Kopf? Die Kontroverse zwischen Paulus und der korinthischen Gemeinde um die Wahrung der Geschlechtsrollensymbolik in 1Kor 11,2–16,” *Zeitschrift für die Neutestamentliche Wissenschaft* 90.3–4 (1999): 220–249.

Bibliographic record:

- https://eurekamag.com/research/102/674/102674589.php

Gielen later republished the study as a chapter in her own book:

> *Paulus im Gespräch: Themen paulinischer Theologie* (Kohlhammer, 2009).

Official/current ebook metadata:

- Google Play Books: https://play.google.com/store/books/details/Marlis_Gielen_Paulus_im_Gespr%C3%A4ch_Themen_paulinisch?id=cfB3DwAAQBAJ
- detailed TOC: https://www.schweitzer-online.de/ebook/Gielen/Paulus-im-Gespraech-Themen-paulinischer-Theologie/9783170231795/A22419061/

The official TOC is unusually informative. The chapter explicitly moves through:

```text
1. Problemstellung
2. Verweigerung einer Kopfbedeckung?
3. Verweigerung einer geordneten Haartracht?
4. Modifikation der Haartrachthypothese
5. paulinische Argumentation gegen das Verhalten der Frauen
```

Therefore:

```text
GIELEN_1999 = REAL_SPECIALIST_ZNW_ARTICLE
GIELEN_2009 = AUTHOR_REPRINT/REWORKED_CHAPTER_CONTEXT
GIELEN_TESTS_BOTH_COVERING_AND_HAIRSTYLE_HYPOTHESES = DIRECT_TOC_CONTROL
```

## 2.2 Her mature proposal is a modified short-hair model, not simply unbound hair

Multiple German scholarly/technical discussions summarize Gielen’s pp.231–237 as modifying the common hair hypothesis:

> Corinthian women are not primarily imagined as simply attending worship with loose/dishevelled hair; the proposed problem is women adopting **short hair**, thereby visually assimilating themselves to men and relativizing sex-role symbolism.

Strong German secondary control:

- *Welt der Bibel* bibliography/exegesis page: https://www.welt-der-bibel.de/bibliographie.1.2.erste_Brief_Paulus_Korinther.42.html
- later technical literature cites Gielen pp.231–237 specifically for the `Kurzhaarhypothese`.

Safe state:

```text
GIELEN_MODIFIED_SHORT_HAIR_MODEL = STRONG_MULTIPLE_SECONDARY_ATTESTED_PP231_237
GIELEN_SIMPLE_UNBOUND_HAIR_MODEL = MISLEADING_OVERSIMPLIFICATION
```

## 2.3 Textual-discovery mirror — useful but not quote-safe

An indexed mirror of Gielen’s 2009 book exposes substantial chapter text and confirms that she explicitly tests whether `ἀκατακάλυπτος` can be tied to hairstyle and whether vv5–6 / 13–15 form one semantic field.

Because this is not the publisher-controlled ebook object, the project may use it for **discovery/cross-checking**, but not as final quote-safe custody.

```text
GIELEN_BODY_DISCOVERY = SUBSTANTIAL_UNOFFICIAL_TEXT_MIRROR
GIELEN_DIRECT_QUOTE_SAFE_BODY = HOLD
```

## 2.4 Independent critique matters

Later German technical literature explicitly criticizes the short-hair model for solving vv4–6/13–15 at the price of reconstructing a very specific Corinthian practice not directly stated in the text.

Thus:

```text
GIELEN_SHORT_HAIR = REAL_SERIOUS_HISTORICAL_MODEL
GIELEN_SHORT_HAIR_EXACT_CORINTH_TRIGGER = RECONSTRUCTION_LAYER
```

Current project grade remains:

```text
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
```

Gielen improves the internal taxonomy of the hair family; she does not by herself promote it above the material-covering model.

---

# 3. Hao Li 2023 — genuine Chinese-language specialist article

## 3.1 Direct journal control

Official journal page:

- https://ccspub.cc/jrcc/article/view/38

Verified publication:

> Hao Li (Singapore Bible College), “Woman is Not Independent of Man. And Man is Not Independent of Woman: The Order of the Creation of Man and Woman in 1 Corinthians 11:2–16,” *Journal of Research for Christianity in China* 21 (2023): 267–318. Published 10 December 2023. DOI `10.29635/JRCC.202312_(21).0012`.

License shown by the journal: CC BY-NC-ND 4.0.

```text
LI_HAO_2023 = DIRECT_OFFICIAL_JOURNAL_RECORD
LI_HAO_PAGES = 267_318
LI_HAO_AFFILIATION = SINGAPORE_BIBLE_COLLEGE
```

## 3.2 Method and result — direct abstract

The official abstract states that Li combines:

- intertextuality;
- socio-cultural contextualization;
- the literary context of 1 Corinthians;
- sociological context;
- Second Temple Jewish interpretation history.

The abstract’s result is explicitly dialectical:

```text
female-to-male subordination relation
+
gender mutual reciprocity and unity
```

within both:

```text
cultural adaptation
+
countercultural intention
```

The concluding emphasis is that Paul’s principal aim is the establishment of mutual reciprocity/unity rather than an absolute transhistorical principle of female subordination derived from creation order.

Thus:

```text
LI_HAO_2023_CREATION_ORDER_DIALECTIC = DIRECT_ABSTRACT
LI_HAO_2023_HONOR_SHAME_CONTEXT = DIRECT_ABSTRACT
LI_HAO_2023_MUTUALITY_AS_MAIN_THEOLOGICAL_AIM = DIRECT_ABSTRACT
```

## 3.3 Full PDF status

The official article page exposes a Chinese PDF link. During this pass the PDF endpoint returned a cache miss.

Therefore:

```text
LI_HAO_OFFICIAL_PDF_EXISTS = VERIFIED
LI_HAO_FULL_BODY = RUNTIME_CONTENT_HOLD
LI_HAO_EXACT_V10_EXOUSIA_POSITION = HOLD
LI_HAO_EXACT_ANGEL_POSITION = HOLD
LI_HAO_EXACT_HEAD_COVERING_POSITION = HOLD
```

No body-level claims should be inferred from the abstract.

## 3.4 False freshness control

A 2025 Chinese web repost labels/publishes the article on 12 October 2025, but explicitly says it was originally carried in the 2023 issue and links the original journal item.

Therefore:

```text
LI_HAO_2025_WEB_DATE = REPOST_DATE
LI_HAO_ORIGINAL_SCHOLARLY_PUBLICATION = 2023
LI_HAO_2025_NEW_SCHOLARSHIP = FALSE_FRESHNESS
```

This reinforces the existing radar rule:

```text
WEB_REPOST_DATE != SCHOLARLY_PUBLICATION_DATE
```

---

# 4. Why these three sources matter together

They independently show that the serious literature cannot be flattened into two camps.

```text
GUNDRY_VOLF:
  creation difference + interdependence / in-Lord theological pressure

GIELEN:
  modified short-hair / sex-role-symbolism reconstruction

LI_HAO:
  creation-order subordination + reciprocity/unity within honor-shame contextualization
```

These are distinct models.

The common high-level lesson is:

> vv7–12 are widely treated as a deliberately complex theological unit in which real differentiation/asymmetry and real mutuality/interdependence must both be explained.

That supports the project’s current calibrated creation model without turning the number of agreeing scholars into evidence by vote.

Current grades remain:

```text
CREATION_ORDER/ASYMMETRY = B_HIGH
MUTUAL_INTERDEPENDENCE_11_11_12 = A
CALIBRATED_CREATION_MUTUAL_ORDER_MODEL = B_HIGH_LEADING
HARD_UNILATERAL_HIERARCHY = C
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
```

---

# 5. New source-hygiene controls

```text
GUNDRY_VOLF_BODY_NOT_ACQUIRED = DO_NOT_DIRECT_QUOTE
GIELEN_SHORT_HAIR != SIMPLE_UNBOUND_HAIR
GIELEN_UNOFFICIAL_TEXT_MIRROR != QUOTE_SAFE_PUBLISHER_OBJECT
LI_HAO_2023_ABSTRACT != FULL_ARTICLE_BODY
LI_HAO_2025_REPOST != NEW_2025_RESEARCH
MULTILINGUAL_RECENCY != AUTOMATIC_AUTHORITY
```

---

# 6. Acquisition queue

```text
P1 GUNDRY_VOLF_1997_PP151_171 = FULLTEXT_HOLD
P1 GIELEN_1999_PP220_249 / AUTHOR_REPRINT_CHAPTER = DIRECT_PUBLISHER_BODY_HOLD
P1 LI_HAO_2023_PP267_318_CHINESE_PDF = RETRY_OFFICIAL_PDF
```

Priority:

1. Gundry-Volf because it can close exact creation/v10/hair source ownership.
2. Gielen because it can map exact short-hair argument and its lexical hinges.
3. Li because abstract already closes the main model; full text would refine Second Temple/intertextual sources rather than likely alter current grades.

---

# 7. Result

```text
CORE_GRADE_REVERSALS = 0
GUNDRY_VOLF_SOURCE_ATTRIBUTION = STRENGTHENED_WITH_PAGE_SPECIFIC_B1_CONTROLS
GIELEN_MODEL = CORRECTED_TO_MODIFIED_SHORT_HAIR_NOT_SIMPLE_UNBOUND_HAIR
LI_HAO_2023_CHINESE_SPECIALIST_ARTICLE = ADDED
LI_HAO_2025_FALSE_FRESHNESS = BLOCKED
CURRENT_CREATION_MUTUALITY_CALIBRATION = RETAINED
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
