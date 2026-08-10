# 1 Коринфянам 11:2–16 — Roman Corinth visual archaeology / `capite velato` custody ledger

**Дата:** 2026-08-10  
**Статус:** `VISUAL-ARCHAEOLOGY / CURRENT-ASSEMBLAGE / OBJECT-PROVENANCE / RIGHTS-CUSTODY / CHECKSUM-PINNED / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Authority rule

This is the single current owner for:

```text
ROMAN_CORINTH_HEAD_COVERING_ARCHAEOLOGY
S1116_S1088_OBJECT_IDENTITY
FINDSPOT_PROVENANCE
CURRENT_ASSEMBLAGE_CONTROL
IMAGE_RIGHTS_AND_CHECKSUMS
LEGACY_CATALOGUE_MAPPING
CURRENT_VISUAL_ARCHAEOLOGY_ACQUISITION
```

Future work updates this ledger instead of creating a new archaeology/checksum delta.

```text
VISUAL_OBJECT != EXEGETICAL_PROOF
OBJECT_METADATA != IMAGE_RIGHTS
PHOTO_FILENAME != PERSON_IDENTIFICATION_CERTAINTY
ARCHAEOLOGY_OF_CORINTH != SPECIFIC_1COR11_SUPPORT_AUTOMATICALLY
ROMAN_CAPITE_VELATO_BACKGROUND = A
V4_EXACT_CAPITE_VELATO = B_C
```

---

# 1. S-1116 — Augustus `capite velato`, Ancient Corinth

## 1.1 Object provenance

```text
OBJECT = marble statue of Augustus
INVENTORY = S-1116
MUSEUM = Archaeological Museum of Ancient Corinth
FINDSPOT = Julian Basilica, Ancient Corinth
EXCAVATION = ASCSA
ICONOGRAPHY = togate Augustus with toga fold over head in sacrificial/priestly representation
```

Primary/current archaeological routes:

- ASCSA excavation history: https://www.ascsa.edu.gr/excavations/ancient-corinth/about-the-excavations-1/history-timeline
- Paul D. Scotton, Catherine de Grazia Vanderpool, Carolynn Roncaglia, *The Julian Basilica: Architecture, Sculpture, Epigraphy*, *Corinth* XXII (ASCSA, 2022): https://www.ascsa.edu.gr/publications/book/?i=9780876610237
- AJA review of *Corinth XXII*: https://www.journals.uchicago.edu/doi/10.1086/725629

```text
CORINTH_S1116_EXISTS = A2_INSTITUTIONAL_ARCHAEOLOGY
CORINTH_S1116_FROM_JULIAN_BASILICA = A2
CORINTH_S1116_AUGUSTUS = SECURE
CORINTH_S1116_MALE_CAPITE_VELATO = A2
```

This establishes real Roman ritual/imperial head-covering iconography in Corinth’s monumental environment. It does **not** prove that Paul’s v4 target is exactly this practice.

## 1.2 Preferred open photograph + checksum

Commons:
- https://commons.wikimedia.org/wiki/File:Statue_of_Augustus_at_the_Archaeological_Museum_of_Corinth_on_January_10,_2020.jpg

Original:
- https://upload.wikimedia.org/wikipedia/commons/f/fe/Statue_of_Augustus_at_the_Archaeological_Museum_of_Corinth_on_January_10%2C_2020.jpg

```text
PHOTOGRAPHER = George_E_Koronaios
PHOTO_DATE = 2020_01_10
DIMENSIONS = 4000x6000
FILE_SIZE = 2568248_bytes
LICENSE = CC_BY_SA_4_0
SHA1 = 5bd067867204a13353d3175fa2c704d60163359a
```

Recommended attribution:

> Photo: George E. Koronaios, Wikimedia Commons, CC BY-SA 4.0. Object: Augustus, Archaeological Museum of Ancient Corinth, inv. S-1116.

---

# 2. S-1088 — veiled Julio-Claudian male portrait head

## 2.1 Object provenance / identity firewall

```text
INVENTORY = S-1088
MATERIAL = marble
MUSEUM = Archaeological Museum of Ancient Corinth
FINDSPOT = Julian Basilica
HEAD_STATE = VEILED_CAPITE_VELATO_TYPE
PERSON_IDENTIFICATION = DISPUTED
```

Safe label:

> Veiled Julio-Claudian male portrait head, S-1088.

AJA’s review of *Corinth XXII* describes the second `capite velato` statue cautiously as a Julio-Claudian prince, possibly Nero Caesar.

Routes:
- https://www.journals.uchicago.edu/doi/10.1086/725629
- secondary identity-history route: https://ancientrome.ru/art/artworken/img.htm?id=6018

```text
CORINTH_S1088_VEILED_MALE_HEAD = STRONG_OBJECT_CONTROL
S1088_EXACT_PERSON = OPEN_DISPUTED
S1088_AS_EMPEROR_NERO_CERTAIN = REJECTED
S1088_AS_NERO_CAESAR = PUBLISHED_IDENTIFICATION_NOT_CERTAINTY
```

## 2.2 Preferred open photograph + checksum

Commons:
- https://commons.wikimedia.org/wiki/File:Portrait_of_Nero,_1st_cent._A.D._(CAM_S-1088,_1-10-2020).jpg

Original:
- https://upload.wikimedia.org/wikipedia/commons/c/ca/Portrait_of_Nero%2C_1st_cent._A.D._%28CAM_S-1088%2C_1-10-2020%29.jpg

```text
PHOTOGRAPHER = George_E_Koronaios
PHOTO_DATE = 2020_01_10
DIMENSIONS = 4000x6000
FILE_SIZE = 10421038_bytes
LICENSE = CC_BY_SA_4_0
SHA1 = 0752c9a5dbd0269f8da48449e288a3c1e44abfc4
```

Recommended caption:

> Veiled Julio-Claudian male portrait head (often identified as Nero/Nero Caesar), Archaeological Museum of Ancient Corinth, inv. S-1088. Photo: George E. Koronaios, Wikimedia Commons, CC BY-SA 4.0.

```text
COMMONS_FILENAME_NERO != CERTAIN_PERSON_IDENTIFICATION
```

---

# 3. Direct archaeology literature chain

## 3.1 Cynthia L. Thompson 1988 — direct local portraiture control

> Cynthia L. Thompson, “Hairstyles, Head-Coverings, and St. Paul: Portraits from Roman Corinth,” *The Biblical Archaeologist* 51.2 (June 1988): 99–115. DOI `10.2307/3210030`.

Direct publisher route:
- https://www.journals.uchicago.edu/doi/10.2307/3210030

The official abstract explicitly states that discussion of 1 Cor 11:2–16 had paid too little attention to relevant archaeological evidence and that material excavated at Corinth could clarify the historical setting.

```text
THOMPSON_1988 = VERIFIED_DIRECT_ARCHAEOLOGY_B1
THOMPSON_SCOPE = ROMAN_CORINTH_PORTRAITURE_AND_1COR11
```

Do not overstate a specific object-level conclusion beyond the directly read body.

## 3.2 David W. J. Gill 1990 — Roman-colonial portraiture response

Direct open-fulltext route:
- https://www.tyndalebulletin.org/article/30525-the-importance-of-roman-portraiture-for-head-coverings-in-1-corinthians-11-2-16

Gill explicitly responds to Thompson and stresses that the Corinthian correspondence should be read against a Roman-colonial rather than merely generic Greek backdrop.

Gill’s older catalogue usage also helps bridge Johnson nos.134/137 to the modern S-1116/S-1088 object tradition.

```text
GILL_1990 = DIRECT_OPEN_ROMAN_PORTRAITURE_CONTROL
GILL_ROMAN_COLONIAL_CONTEXT = STRONG_PUBLISHED_BACKGROUND
```

## 3.3 ASCSA *Corinth XXII* 2022 — current assemblage owner

> Paul D. Scotton, Catherine de Grazia Vanderpool, Carolynn Roncaglia, *The Julian Basilica: Architecture, Sculpture, Epigraphy*, *Corinth* XXII (ASCSA, 2022).

This current monograph is preferred over treating an isolated legacy photograph/caption as the complete archaeological context.

```text
ASCSA_CORINTH_XXII_2022 = CURRENT_JULIAN_BASILICA_ASSEMBLAGE_CONTROL
```

## 3.4 David A. deSilva 2025 — current visual synthesis acquisition target

Baker Academic verifies:

> David A. deSilva, *Archaeology and the Ministry of Paul: A Visual Guide* (Baker Academic, April 2025), 320 pp., ISBN 9781540960955.

Official routes:
- https://bakeracademic.com/products/9781540960955_archaeology-and-the-ministry-of-paul
- https://bakeracademic.com/collections/bible-2025-new-releases

Published TOC/review control places:

```text
ROMAN_CORINTH = PP126_156
```

Current preview/search has **not** established that these pages specifically discuss:

```text
1COR11_2_16
S1116
S1088
JULIAN_BASILICA_HEAD_COVERING_ICONOGRAPHY
```

Therefore:

```text
DESILVA_2025_ROMAN_CORINTH_CHAPTER = VERIFIED
DESILVA_2025_1COR11_SPECIFIC_USE = LOCATOR_HOLD
DESILVA_2025_S1116_SPECIFIC_USE = LOCATOR_HOLD
DESILVA_2025 = P1_CURRENT_VISUAL_ARCHAEOLOGY_TARGET
```

Do not cite deSilva as confirmation of the exact v4 `capite velato` reading until the relevant pages are directly read.

---

# 4. Archaeological chain / no double counting

Current chain:

```text
THOMPSON_1988_LOCAL_PORTRAITS
-> OSTER_1988_1992_ROMAN_RITUAL_ARCHAEOLOGY
-> GILL_1990_ROMAN_PORTRAITURE_RESPONSE
-> ASCSA_CORINTH_XXII_2022_CURRENT_ASSEMBLAGE
-> DESILVA_2025_CURRENT_VISUAL_SYNTHESIS_TARGET
```

This is a publication/interpretation chain, not five independent archaeological objects.

```text
ARCHAEOLOGICAL_PUBLICATION_STAGE != NEW_OBJECT
CURRENT_SYNTHESIS != INDEPENDENT_FINDSPOT
```

Minimum strengthened background:

```text
ROMAN_CAPITE_VELATO_BACKGROUND = A
CORINTH_LOCAL_ROMAN_ICONOGRAPHIC_BACKGROUND = A2_STRONG
```

Not newly proved:

```text
V4_EXACT_CAPITE_VELATO = A
CHRISTIAN_MEN_WERE_IMITATING_IMPERIAL_CULT = true
EXACT_CORINTH_TRIGGER = solved
```

Current remains:

```text
V4_EXACT_CAPITE_VELATO = B_C
EXACT_CORINTH_TRIGGER = RECONSTRUCTION_LAYER
```

---

# 5. Archaeological meaning of S-1116 / S-1088

The pair is stronger for local background than generic Roman examples because both belong to Roman Corinth’s Julian Basilica/forum environment.

Safe:

```text
CAPITE_VELATO_ICONOGRAPHY_PRESENT_IN_ROMAN_CORINTH = VERY_STRONG
CORINTH_LOCAL_VISUAL_BACKGROUND = A2_STRONG
```

Unsafe:

```text
EVERY_CORINTHIAN_MAN_WORSHIPPED_CAPITE_VELATO = FALSE_UNIVERSAL
PAUL_V4_EXACTLY_TARGETS_IMPERIAL_CULT = UNPROVED
CHRISTIAN_MEN_WERE_COPYING_THE_IMPERIAL_STATUES = UNPROVED
```

---

# 6. Legacy catalogue mapping

Older scholarship uses Franklin P. Johnson, *Corinth IX.1* (1931) numbers.

## Johnson no.134 -> S-1116

Gill 1990 and Boschung 1993 independently tie the Corinth `capite velato` Augustus to Johnson no.134; modern ASCSA/museum control identifies S-1116.

```text
JOHNSON_1931_NO134 = AUGUSTUS_CAPITE_VELATO_CORINTH
MODERN_INVENTORY = S1116
LEGACY_TO_MODERN_MAPPING = HIGH_CONFIDENCE
```

## Johnson no.137 -> S-1088

Gill’s second covered imperial image maps through later object bibliography to S-1088.

```text
JOHNSON_1931_NO137 = MODERN_S1088
OBJECT = VEILED_JULIO_CLAUDIAN_MALE_HEAD
JOHNSON_PERSON_ID = NERO_SON_OF_GERMANICUS
CURRENT_PERSON_ID = DISPUTED
```

## Peters 2013 dissertation bridge — p.282 narrowed

Current Peters source genealogy identifies the exact work:

> Janelle Lynne Peters, “Leveling the Playing Field: Egalitarian Veils and Athletic Metaphors in 1 Corinthians.” PhD dissertation, Emory University, 2013.

Institutional metadata is controlled in:
- `00ZZZZZZZZZ_SOURCE_CARD_JANELLE_PETERS_CITIZEN_BODY_2025_2026.md`

```text
EMORY_OBJECT_ID = qr46r105v
REPOSITORY_STATUS = OPEN_ACCESS
CH6_CREATION_IN_CORINTHIAN_HOUSE_CHURCHES_AND_ROMAN_EMPIRE = starts_p228
CH7_VEILING_THE_BODY_OF_CHRIST = starts_p264
CONCLUSION = starts_p301
```

Therefore p.282 is deterministically **inside Peters’ veiling chapter**, not an unlocated page number.

Later scholarship page-specifically cites Peters p.282 in connection with a Corinthian statue and F. P. Johnson, *Corinth IX.1*, pp.70–72. That downstream citation is useful as an acquisition locator but does not replace Peters’ own page.

```text
PETERS_2013_DISSERTATION_OBJECT = DIRECT_INSTITUTIONAL_METADATA_CLOSED
PETERS_2013_P282 = CH7_VEILING_BODY_OF_CHRIST_DETERMINISTIC_PAGE_TARGET
PETERS_2013_P282_CORINTH_STATUE = SECONDARY_PAGE_LOCATOR
PETERS_2013_P282_DIRECT_AUTOPSY = HOLD_RUNTIME_PRIMARY_PDF_ENDPOINT
PETERS_P282_OBJECT_IDENTIFICATION = VERIFY_AGAINST_ASCSA_JOHNSON_CHAIN
```

Do not infer a modern inventory number or person identification from the downstream p.282 citation until Peters’ page itself is read. The archaeological objects remain owned by this ASCSA ledger, not by a secondary Peters citation.

---

# 7. Duplicate-counting firewall

```text
JOHNSON_NO134
GILL_1990_AUGUSTUS
MODERN_S1116
=
ONE_ANCHOR_OBJECT_TRADITION
```

```text
JOHNSON_NO137
GILL_1990_SECOND_COVERED_IMPERIAL_IMAGE
MODERN_S1088
=
ONE_OBJECT_TRADITION_WITH_CHANGING_PERSON_ID
```

```text
LEGACY_CATALOGUE_NUMBER != NEW_OBJECT
OBJECT_CONTINUITY != PERSON_IDENTIFICATION_CONTINUITY
MODERN_ASCSA_INVENTORY_ASSEMBLAGE > LEGACY_PERSON_LABEL_FOR_CURRENT_CAPTIONING
```

---

# 8. Image-custody workflow

```text
1. fetch original Commons binary
2. compute SHA1/SHA256 locally
3. compare with pinned custody record
4. preserve photographer + CC attribution
5. keep museum object identity separate from Commons filename
6. record crop/transform as derivative artifact
7. if bytes change, inspect file history and record new custody event
```

```text
CC_BY_SA_PHOTO_RIGHTS != RIGHT_TO_CLAIM_EXACT_PAULINE_TRIGGER
OPEN_PHOTO != MUSEUM_ENDORSEMENT
LICENSE != OBJECT_PROVENANCE
```

---

# 9. Preferred visual pair

### Anchor
**Augustus S-1116**

- secure identity;
- direct local archaeological context;
- high-resolution CC BY-SA image;
- checksum pinned.

### Nuance object
**Veiled Julio-Claudian male head S-1088**

- secure object identity;
- disputed personal identity;
- high-resolution CC BY-SA image;
- checksum pinned.

Preserve both even if the exact v4 reconstruction changes.

---

# 10. Acquisition queue

```text
P1 DESILVA_2025_ROMAN_CORINTH_PP126_156 = DIRECT_BODY_HOLD
P1 PETERS_2013_EMORY_QR46R105V_P282 = DIRECT_PAGE_HOLD
```

---

# 11. Result

```text
CORE_GRADE_REVERSALS = 0
THOMPSON_1988_DIRECT_PUBLISHER_CONTROL = CLOSED
GILL_1990_DIRECT_OPEN_CONTROL = CLOSED
ASCSA_CORINTH_XXII_2022 = CURRENT_ASSEMBLAGE_OWNER
DESILVA_2025 = CURRENT_SYNTHESIS_TARGET / SPECIFIC_LOCATOR_HOLD
PETERS_2013_DISSERTATION_OBJECT = DIRECT_INSTITUTIONAL_METADATA_CLOSED
PETERS_2013_P282 = DETERMINISTIC_CH7_PAGE_TARGET / DIRECT_PAGE_HOLD
CORINTH_S1116 = SECURE_LOCAL_CAPITE_VELATO_ANCHOR
CORINTH_S1088 = SECURE_LOCAL_VEILED_MALE_OBJECT_PERSON_ID_OPEN
IMAGE_RIGHTS_AND_CHECKSUMS = PINNED
ROMAN_CAPITE_VELATO_BACKGROUND = A
V4_EXACT_CAPITE_VELATO = B_C
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
