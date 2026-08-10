# 1 Corinthians 11:10 — Theodoret guardian-angels attribution resolution

**Date:** 2026-08-10  
**Status:** `PATRISTIC-ATTRIBUTION / EXACT-PG-LOCATORS / PUBLISHED-TRANSLATION-LOCATOR / PRIMARY-PAGE-IMAGE-HOLD / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Authority / supersession

This is the **single retained branch owner** for the Theodoret guardian/assigned-angels attribution.

It consolidates the earlier branch locator-delta and attribution-resolution layers. Future work must update this file rather than create another Theodoret successor report.

```text
THEODORET_GUARDIAN_ANGELS_ATTRIBUTION = VERIFIED_AT_SOURCE_LOCATOR_LEVEL
THEODORET_DIRECT_GREEK_PAGE_AUTOPSY = HOLD
CORE_GRADE_REVERSALS = 0
```

---

# 1. Standalone commentary ownership

Theodoret of Cyrus, *Interpretatio epistulae I ad Corinthios*, is independently identified in **PG 82**, within the standalone Pauline commentary corpus.

Controls retained from the earlier locator pass:

- Mieczysław Paczkowski, “The Angelological Topics in Patristic Exegesis of 1Cor 11:10” / “Wątki angelologiczne w egzegezie patrystycznej 1Kor 11,10” (2023), DOI `10.31743/vp.15533`;
- Biblissima/BnF manuscript control: Paris, BnF Coislin 82, Theodoret’s Pauline commentary; 1 Corinthians occupies the relevant manuscript section;
- Migne PG 82 index independently identifies the standalone 1 Corinthians commentary.

Routes:

- Paczkowski: https://czasopisma.kul.pl/index.php/vp/article/view/15533
- Biblissima/BnF Coislin 82: https://portail.biblissima.fr/fr/ark%3A/43093/mdataa9131f7246a06e1c33669c7c65747f8b76ff370d
- PG 82 index: https://www.documentacatholicaomnia.eu/1815-1875%2C_Migne%2C_PG_Volumen_082_Rerum_Conspectus_Pro_Columnis_Ordinatus%2C_MGR.html

```text
THEODORET_1COR_COMMENTARY = DIRECTLY_IDENTIFIED_WORK
CATENA_FRAGMENT != STANDALONE_THEODORET_COMMENTARY
```

---

# 2. Exact PG locators

Paczkowski gives the exact standalone commentary locators:

```text
Theodoretus Cyrensis,
Interpretatio epistulae I ad Corinthios XI,
PG 82, 312D
PG 82, 313A
```

His discussion connects Theodoret’s explanation with:

```text
Acts 12:15
Matthew 18:10
```

These are the passages used to support angels assigned to / caring for human beings.

```text
THEODORET_PG_LOCATORS = PG82_312D_313A
THEODORET_ACTS_12_15 = STRONG_SPECIALIST_LOCATOR_CONTROL
THEODORET_MATT_18_10 = STRONG_SPECIALIST_LOCATOR_CONTROL
```

---

# 3. Published modern translation route

Published translation:

> Theodoret of Cyrus, *Commentary on the Letters of St Paul*, vol. 1, trans. Robert Charles Hill, Holy Cross Orthodox Press, 2001.

Volume 1 contains Romans and 1–2 Corinthians. The 1 Cor 11:10 explanation is repeatedly located at **p.205**.

Its controlled substance is:

```text
EXOUSIA = covering / display of subjection
ANGELS = those set over human beings / entrusted with their care
SUPPORT = Acts 12:15 + Matthew 18:10
```

Calibration:

```text
HILL_2001_P205 = EXACT_MODERN_TRANSLATION_LOCATOR_STRONGLY_CONTROLLED
HILL_P205_DIRECT_BOOK_BYTES_IN_CURRENT_RUNTIME = HOLD
```

The project does not make an unofficial reproduction the controlling source; its function is only to converge with the exact PG locators and scriptural references supplied by specialist scholarship.

---

# 4. Independent reception control

Henry Alford’s *Greek Testament* independently groups Theodoret with a guardian-angels interpretation.

This is **supporting reception evidence**, not the primary ownership proof.

```text
PACZKOWSKI_EXACT_PG_LOCATORS > ALFORD_CLASSIFICATION
STANDALONE_THEODORET_OWNER > CATENA_PROXIMITY
```

---

# 5. What is now closed

```text
THEODORET_GUARDIAN_ANGELS_SOURCE_ATTRIBUTION = VERIFIED
THEODORET_STANDALONE_COMMENTARY_OWNER = VERIFIED
THEODORET_PG_82_312D_313A = CLOSED_LOCATOR
THEODORET_HILL_VOL1_P205 = CLOSED_TRANSLATION_LOCATOR
THEODORET_ACTS_12_15_MATT_18_10_CHAIN = CLOSED_AT_LOCATOR_TRANSLATION_LEVEL
```

Source-near taxonomy:

```text
ANGELS = CELESTIAL ANGELS ASSIGNED/SET OVER HUMAN BEINGS
FUNCTION = CARE/OVERSIGHT
```

The label `guardian angels` is a convenient modern taxonomy; the source-near wording is preferable when precision matters.

---

# 6. What remains open

A direct rendered image / personal Greek-page autopsy of **PG 82, 312D–313A** has not yet been completed in the current controlled workflow.

A public-domain PG 82 PDF is known to exist, but the earlier runtime could not complete the page-image autopsy because of object-size/access limitations.

```text
THEODORET_EXACT_GREEK_WORDING_PERSONALLY_AUTOPSIED = false
THEODORET_PG_PAGE_IMAGE = HOLD
QUOTE_SAFE_GREEK_FROM_THIS_PASS = false
```

Do not generate a Greek quotation from memory or from a secondary transcription before direct page verification.

---

# 7. Catena firewall

Keep the standalone interpretation distinct from nearby catena material:

```text
THEODORET_GUARDIAN_ANGELS != PHOTIUS_WITNESS_ANGELS
THEODORET_GUARDIAN_ANGELS != CATENA_KYTILLOU_CHURCH_ANGELS
CATENA_NEIGHBOR_LABEL != STANDALONE_COMMENTARY_OWNER
```

The guardian/assigned-angels attribution is owned by the standalone PG/Hill route, not by an ambiguous Cramer-catena attribution chain.

---

# 8. Historical reception map

Current controlled diversity includes:

```text
TERTULLIAN = FALLEN_WATCHERS / GEN6
CHRYSOSTOM = HEAVENLY_ANGELS PRESENT AT WORSHIP
AMBROSIASTER = BISHOPS
SEVERIAN = REPORTS SOME SAY CHURCH PRIESTS
CLEMENT_FRAGMENT = RIGHTEOUS/VIRTUOUS HUMAN OBSERVERS
PHOTIUS = ANGELS AS WITNESSES/OBSERVERS OF SUBJECTION
THEODORET = ANGELS ASSIGNED OVER HUMANS / ENTRUSTED WITH THEIR CARE
VALENTINIAN_RECEPTION = ACHAMOTH-SOTERIOLOGICAL READING REPORTED BY IRENAEUS
```

Reception diversity is historically relevant but does not resolve Paul by vote-counting.

---

# 9. Project-level grade impact

```text
HEAVENLY_HOLY_ANGELS_REFERENT = B_HIGH_LEADING
ANGELS_AS_COSMIC_WITNESSES_PRESENT_ASSEMBLY = B_LEADING
EXACT_ANGELIC_FUNCTION = B_C
WATCHERS = C_SERIOUS_ALTERNATIVE
GUARDIAN_ASSIGNED_ANGELS_AS_PAULS_EXACT_MEANING = C_LOW
```

Why source closure does not promote the Pauline theory:

1. Theodoret is a fifth-century reception witness, not first-century evidence.
2. Acts 12:15 / Matt 18:10 establish conceptual availability of assigned angels, not Paul’s exact intention here.
3. 1 Cor 11:10 itself does not specify the angels’ exact function.
4. Other early readers assign different functions/referents.

```text
THEODORET_ATTRIBUTION_CONFIDENCE = UPGRADED
PAULINE_GUARDIAN_ANGEL_PROBABILITY = UNCHANGED
```

---

# 10. Result

```text
CORE_GRADE_REVERSALS = 0
THEODORET_STANDALONE_OWNER = CLOSED
THEODORET_PG_LOCATOR = CLOSED_PG82_312D_313A
THEODORET_HILL_LOCATOR = CLOSED_P205
THEODORET_GUARDIAN_ASSIGNED_ANGEL_RECEPTION = VERIFIED_AT_LOCATOR_TRANSLATION_LEVEL
THEODORET_DIRECT_PG_IMAGE_AUTOPSY = HOLD
GUARDIAN_ANGELS_AS_PAULS_EXACT_MEANING = C_LOW_UNCHANGED
EXACT_ANGELIC_FUNCTION = B_C_UNCHANGED
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
