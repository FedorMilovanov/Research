# 1 Коринфянам 11:10 — Theodoret guardian-angel locator delta

**Дата:** 2026-08-10  
**Статус:** `PATRISTIC-RECEPTION / TWO-ROUTE-PAGE-LOCATED / PG-LOCATOR-IDENTIFIED / DIRECT-PAGE-IMAGE-HOLD / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Purpose

The project previously carried:

```text
THEODORET_GUARDIAN_ANGELS = STRONG_SECONDARY_ATTRIBUTION / PRIMARY_LOCATOR_HOLD
```

The question was not whether later commentators associated Theodoret with guardian angels; that was already well attested. The unresolved provenance question was:

> Can the interpretation be pinned to Theodoret’s standalone commentary on 1 Corinthians with exact primary-edition / modern-translation locators, rather than inferred from a nearby catena fragment or circular modern citations?

The answer is now **yes at locator level**, but **not yet at direct page-image autopsy level**.

---

# 1. Standalone Theodoret commentary is independently controlled

Theodoret of Cyrus, *Interpretatio epistulae I ad Corinthios*, is published in:

> PG 82, cols.225D–376A.

Direct institutional / bibliographic controls:

- Mieczysław Paczkowski, “The Angelological Topics in Patristic Exegesis of 1Cor 11:10,” *Vox Patrum* (2023), DOI `10.31743/vp.15533`, bibliography listing Theodoret’s *Interpretatio epistulae I ad Corinthios*, PG 82, 225D–376A.
- Biblissima/BnF identifies manuscript Paris, BnF Coislin 82 as Theodoret’s Pauline commentary; 1 Corinthians occupies ff.55–104.
- Migne PG 82 index identifies *Interpretatio epistolæ I ad Corinthios* beginning at col.226 and II Corinthians at col.375.

Routes:

- Paczkowski journal page: https://czasopisma.kul.pl/index.php/vp/article/view/15533
- Biblissima Coislin 82: https://portail.biblissima.fr/fr/ark%3A/43093/mdataa9131f7246a06e1c33669c7c65747f8b76ff370d
- PG 82 index: https://www.documentacatholicaomnia.eu/1815-1875%2C_Migne%2C_PG_Volumen_082_Rerum_Conspectus_Pro_Columnis_Ordinatus%2C_MGR.html

Thus:

```text
THEODORET_1COR_COMMENTARY = DIRECTLY_IDENTIFIED_WORK
THEODORET_1COR11_REGION = INSIDE_CONTROLLED_STANDALONE_WORK
```

---

# 2. Paczkowski gives exact PG locators for the guardian-angel argument

Paczkowski’s dedicated specialist study gives two exact notes:

```text
Theodoretus Cyrensis, Interpretatio epistulae I ad Corinthios XI, PG 82, 312D
Theodoretus Cyrensis, Interpretatio epistulae I ad Corinthios XI, PG 82, 313A
```

His discussion explicitly notes that the bishop of Cyrus invokes:

- Acts 12:15 (`his angel`);
- Matthew 18:10 (`their angels always behold the face of my Father`).

Those are precisely the New Testament texts classically used to support the idea of angels assigned to individual human beings / believers.

Therefore:

```text
THEODORET_GUARDIAN_ANGEL_PG_LOCATOR = PG82_312D_313A
THEODORET_ACTS_12_15 = STRONG_SPECIALIST_PAGE_LOCATED
THEODORET_MATT_18_10 = STRONG_SPECIALIST_PAGE_LOCATED
```

This is substantially stronger than a generic historical-commentary attribution.

---

# 3. Independent modern translation route converges on the same interpretation

Official publisher metadata identifies:

> Theodoret of Cyrus, *Commentary on the Letters of St. Paul*, vol. 1, trans. Robert Charles Hill (Holy Cross Orthodox Press, 2001).

Volume 1 contains Romans and 1–2 Corinthians. First Corinthians begins around p.158 in the published volume.

A repeatedly cited passage is located at **p.205** and gives the v10 explanation in this sense:

- `authority` refers to the covering as a display of subjection;
- the angels are those set over human beings and entrusted with their care;
- Acts 12:15 and Matthew 18:10 are then cited as support.

Important source calibration:

```text
HILL_2001_P205 = EXACT_MODERN_TRANSLATION_LOCATOR_STRONGLY_ATTESTED
HILL_P205_DIRECT_BOOK_BYTES = HOLD
```

The project does **not** make the secondary websites carrying the quote the controlling source. They are useful because their exact page/edition attribution independently converges with Paczkowski’s PG locators and Scripture references.

The controlling ownership chain is:

```text
THEODORET_STANDALONE_COMMENTARY
-> PG82_312D_313A (specialist locator)
-> HILL_2001_P205 (modern translation locator)
```

---

# 4. Direct PG PDF exists, but page-image autopsy is not claimed

Wikimedia Commons exposes the complete public-domain file:

> `Patrologia Graeca Vol. 082.pdf`

with 854 pages / ~107 MB.

The current web runtime located the PDF but could not fetch the original because of the object size. Therefore the required page-image verification could not be completed inside this pass.

```text
PG82_PUBLIC_PDF = VERIFIED_AVAILABLE
PG82_312D_313A_SCREENSHOT_AUTOPSY = NOT_COMPLETED_RUNTIME_SIZE_LIMIT
```

This distinction matters. We now know **where** the primary passage is and have independent agreement on its content, but we do not say:

```text
DIRECT_PG_IMAGE_READ = true
```

until the actual columns are rendered/inspected.

---

# 5. Theodoret’s reception model can now be stated more precisely

At source-attribution level, the interpretation is no longer merely “Theodoret probably meant guardian angels.”

The page-located argument is:

```text
ANGELS = CELESTIAL ANGELS ASSIGNED/SET OVER HUMAN BEINGS
FUNCTION = CARE/OVERSIGHT OF HUMAN BEINGS
SUPPORT_TEXTS = ACTS_12_15 + MATT_18_10
```

Therefore the safe reception label is:

```text
THEODORET_GUARDIAN_OR_ASSIGNED_ANGELS = STRONG_TWO_ROUTE_PAGE_LOCATED_RECEPTION
```

The word `guardian` is a modern taxonomic label. The more source-near formulation is:

> angels set over human beings and entrusted with their care.

This avoids importing a later fully systematized guardian-angel doctrine beyond what the located argument itself supports.

---

# 6. Keep Theodoret distinct from the Cramer catena fragments

The preceding catena audit established:

- a Theodoret-labelled block reconstructing Corinthian women praying uncovered / some attempting to teach;
- a separate digitally-labelled `Κυτίλλου` block about angels established at churches (normalized author still HOLD);
- a secure Photius block where angels are witnesses/observers and `ἐξουσία` is read as a covering indicating male authority.

None of those should be substituted for Theodoret’s standalone guardian/assigned-angels argument.

Thus:

```text
THEODORET_GUARDIAN_ANGELS != PHOTIUS_WITNESS_ANGELS
THEODORET_GUARDIAN_ANGELS != CATENA_KYTILLOU_CHURCH_ANGELS
CATENA_PROXIMITY != STANDALONE_THEODORET_TEXT
```

The standalone PG/Hill route is now the owner for the guardian/assigned-angels interpretation.

---

# 7. Relation to broader patristic angel map

The reception map can now be sharpened:

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

This diversity is historically important but does not resolve Paul by patristic vote-counting.

---

# 8. Project-level grading impact

The source ownership improves. The core probability judgment does **not** automatically change.

```text
HEAVENLY_HOLY_ANGELS_REFERENT = B_HIGH_LEADING
ANGELS_AS_COSMIC_WITNESSES/PRESENT_ASSEMBLY = B_LEADING
EXACT_ANGELIC_FUNCTION = B_C
WATCHERS = C_SERIOUS_ALTERNATIVE
GUARDIAN/ASSIGNED_ANGELS_AS_PAULS_EXACT_MEANING = C_LOW
```

Why no promotion of the exact Pauline guardian-angels theory:

1. a fifth-century reception reading is not first-century proof;
2. Acts 12:15 / Matthew 18:10 show the conceptual availability of assigned angels, not that Paul must intend this function here;
3. Paul himself does not specify the angels’ exact function in 1 Cor 11:10;
4. other early readers supply substantially different angel functions.

Therefore:

```text
THEODORET_ATTRIBUTION_CONFIDENCE = UPGRADED
PAULINE_GUARDIAN_ANGEL_PROBABILITY = UNCHANGED
```

---

# 9. Supersession statement

This file supersedes only the provenance status:

```text
OLD:
THEODORET_GUARDIAN_ANGELS = STRONG_SECONDARY_ATTRIBUTION / PRIMARY_LOCATOR_HOLD

NEW:
THEODORET_GUARDIAN_ANGELS = STRONG_TWO_ROUTE_PAGE_LOCATED_RECEPTION
THEODORET_PRIMARY_PG_LOCATOR = PG82_312D_313A
THEODORET_MODERN_TRANSLATION_LOCATOR = HILL_2001_P205
DIRECT_PRIMARY_PAGE_IMAGE = HOLD
```

It does **not** supersede the project grade for the exact angelic function.

---

# 10. Result

```text
CORE_GRADE_REVERSALS = 0
THEODORET_STANDALONE_OWNER = CLOSED
THEODORET_PG_LOCATOR = CLOSED_PG82_312D_313A
THEODORET_HILL_LOCATOR = CLOSED_P205
THEODORET_GUARDIAN/ASSIGNED_ANGEL_RECEPTION = STRONG_PAGE_LOCATED
THEODORET_DIRECT_PG_IMAGE_AUTOPSY = HOLD_RUNTIME_SIZE_LIMIT
GUARDIAN_ANGELS_AS_PAULS_EXACT_MEANING = C_LOW_UNCHANGED
EXACT_ANGELIC_FUNCTION = B_C_UNCHANGED
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
