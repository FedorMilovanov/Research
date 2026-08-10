# 1 Corinthians 11:10 — Theodoret guardian-angels attribution resolution

**Date:** 2026-08-10  
**Status:** `PATRISTIC-ATTRIBUTION / PUBLISHED-TRANSLATION-VERIFIED / EXACT-PG-LOCATORS / GREEK-PAGE-AUTOPSY-HOLD / RESEARCH-ONLY`

## 0. Question

Earlier branch layers kept:

```text
THEODORET_GUARDIAN_ANGELS = STRONG_ATTRIBUTION / PRIMARY_LOCATOR_HOLD
```

This file resolves whether the guardian-angels reading is really Theodoret's own interpretation of 1 Cor 11:10, while preserving the remaining boundary between a verified published translation/PG locator and direct Greek-page autopsy.

---

# 1. Exact standalone Theodoret locators

M. C. Paczkowski, "Wątki angelologiczne w egzegezie patrystycznej 1Kor 11,10" (2023), cites the standalone Pauline commentary of Theodoret twice for this passage:

```text
Theodoretus Cyrensis,
Interpretatio epistulae I ad Corinthios XI,
PG 82, 312D
PG 82, 313A
```

Paczkowski further states that the bishop of Cyrus appeals in this context to:

```text
Acts 12:15
Matthew 18:10
```

Those are precisely the standard guardian-angel texts used to support the reading.

This is materially stronger than a generic modern attribution because it supplies the exact Patrologia Graeca columns in Theodoret's own standalone commentary rather than a catena fragment.

---

# 2. Published English translation control

Robert Charles Hill's published English translation is:

> Theodoret of Cyrus, *Commentary on the Letters of St Paul*, vol. 1, Holy Cross Orthodox Press, 2001.

Publisher metadata independently confirms:

```text
TRANSLATOR = Robert Charles Hill
PUBLISHER = Holy Cross Orthodox Press
VOLUME_1_CONTENT = Romans + 1-2 Corinthians
```

The 1 Cor 11:10 passage is cited at p.205 in multiple independent reproductions of Hill's translation. Its substance is:

```text
"authority" -> the covering / display of subjection
angels -> those set over human beings and entrusted with their care
supporting loci -> Acts 12:15 + Matthew 18:10
```

The coincidence between:

```text
Hill p.205
+ Paczkowski PG 82, 312D-313A
+ Acts 12:15 / Matt 18:10
```

makes the attribution to Theodoret secure at the published-translation / exact-primary-locator level.

---

# 3. Independent older commentary control

Henry Alford's Greek Testament commentary independently classifies Theodoret together with Theophylact and Jerome under the interpretation that the angels of 1 Cor 11:10 are guardian angels attached to believers.

This is not the controlling evidence, but it is an independent pre-modern-scholarship reception witness to the same attribution.

---

# 4. What is now closed

```text
THEODORET_GUARDIAN_ANGELS_ATTRIBUTION = VERIFIED
THEODORET_STANDALONE_COMMENTARY_OWNER = VERIFIED
THEODORET_PG_LOCATORS = 82,312D-313A
THEODORET_HILL_TRANSLATION_LOCATOR = VOL1_P205
THEODORET_USES_ACTS_12_15 = VERIFIED_BY_PUBLISHED_TRANSLATION/LOCATOR_CHAIN
THEODORET_USES_MATT_18_10 = VERIFIED_BY_PUBLISHED_TRANSLATION/LOCATOR_CHAIN
```

The source-specific interpretation is:

```text
ANGELS = GUARDIAN/CARETAKER ANGELS OVER HUMAN BEINGS
EXOUSIA = COVERING AS DISPLAY OF SUBJECTION
```

This records Theodoret's interpretation. It does **not** promote that interpretation to the project's leading modern exegetical grade.

---

# 5. What remains open

This pass did not obtain a direct image or directly rendered Greek page of PG 82, 312D-313A in the current runtime.

Therefore:

```text
THEODORET_EXACT_GREEK_WORDING_PERSONALLY_AUTOPSIED = false
THEODORET_PG_PAGE_IMAGE = HOLD
QUOTE_SAFE_GREEK_FROM_THIS_PASS = false
```

The English published translation may be cited with its bibliographic locator; a Greek quotation should still be checked directly against PG/critical Greek before publication.

---

# 6. Important separation from catena material

A previous catena pass showed how easily patristic authorship can be corrupted if `Τοῦ Αὐτοῦ` or ambiguous author labels are attached to the wrong preceding name.

The present resolution is different because it rests on:

```text
THEODORET_STANDALONE_PAULINE_COMMENTARY
+ EXACT_PG_COLUMNS
+ PUBLISHED_MODERN_TRANSLATION
```

not on an unattributed or ambiguously labelled catena chain.

Thus future agents must keep:

```text
THEODORET_GUARDIAN_ANGELS = TRUE_SOURCE_ATTRIBUTION
CATENA_NEIGHBORING_FRAGMENT = SEPARATE_SOURCE_PROBLEM
```

---

# 7. Effect on current angel map

Current historical-reception map can now safely include:

```text
Tertullian -> Watchers / fallen angels / Gen 6
Chrysostom -> heavenly angels present in worship
Ambrosiaster -> bishops
Severian -> reports "some say" church priests; personal endorsement not established
Clement fragment -> righteous/virtuous human observers
Theodoret -> guardian angels assigned to human beings
Valentinian tradition reported by Irenaeus -> Achamoth/Sophia mythic reading
```

Project-level grades remain distinct:

```text
HEAVENLY_HOLY_ANGELS_REFERENT = B_HIGH_LEADING
EXACT_ANGELIC_FUNCTION = B_C
WATCHERS = C_SERIOUS_ALTERNATIVE
GUARDIAN_ANGELS = C_LOW_RECEPTION_SUPPORTED
BISHOPS_CLERGY = D_C_LOW_RECEPTION
```

No core grade reversal follows merely from closing Theodoret's ownership.

---

# 8. Supersession rule

This file supersedes the earlier branch shorthand:

```text
THEODORET_GUARDIAN_ANGELS = STRONG_ATTRIBUTION / PRIMARY_LOCATOR_HOLD
```

with:

```text
THEODORET_GUARDIAN_ANGELS = VERIFIED_PUBLISHED_TRANSLATION_PLUS_EXACT_PG_LOCATORS
THEODORET_DIRECT_GREEK_PAGE_AUTOPSY = HOLD
```

---

# 9. Result

```text
CORE_GRADE_REVERSALS = 0
THEODORET_GUARDIAN_ANGELS = VERIFIED_SOURCE_ATTRIBUTION
THEODORET_PG_82_312D_313A = CLOSED_LOCATOR
THEODORET_HILL_VOL1_P205 = CLOSED_TRANSLATION_LOCATOR
DIRECT_GREEK_IMAGE_AUTOPSY = HOLD
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
