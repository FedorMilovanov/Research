# 1 Коринфянам 11:2–16 — Roman Corinth visual archaeology / `capite velato` custody ledger

**Дата:** 2026-08-10  
**Статус:** `VISUAL-ARCHAEOLOGY / OBJECT-PROVENANCE / RIGHTS-CUSTODY / CHECKSUM-PINNED / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Authority rule

This is the single retained owner for the Roman Corinth `capite velato` object pair and their reusable image custody.

It combines:

```text
OBJECT_IDENTITY
FINDSPOT_PROVENANCE
DATE_CONTEXT
INTERPRETIVE_FUNCTION
IMAGE_RIGHTS
ORIGINAL_FILE_IDENTITY
LEGACY_CATALOGUE_MAPPING
```

Future work should update this ledger instead of adding a separate visual checksum/custody supplement.

Core boundary:

```text
VISUAL_OBJECT != EXEGETICAL_PROOF
OBJECT_METADATA != IMAGE_RIGHTS
PHOTO_FILENAME != PERSON_IDENTIFICATION_CERTAINTY
CHECKSUM = FILE_IDENTITY_CONTROL
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

- ASCSA Corinth excavation history: https://www.ascsa.edu.gr/excavations/ancient-corinth/about-the-excavations-1/history-timeline
- Paul D. Scotton, Catherine de Grazia Vanderpool, Carolynn Roncaglia, *The Julian Basilica: Architecture, Sculpture, Epigraphy*, *Corinth* XXII (ASCSA, 2022): https://www.ascsa.edu.gr/publications/book/?i=9780876610237
- AJA review identifying the `capite velato` sculptural pair: https://www.journals.uchicago.edu/doi/10.1086/725629

```text
CORINTH_S1116_EXISTS = A2_INSTITUTIONAL_ARCHAEOLOGY
CORINTH_S1116_FROM_JULIAN_BASILICA = A2
CORINTH_S1116_AUGUSTUS = SECURE
CORINTH_S1116_MALE_CAPITE_VELATO = A2
```

This establishes real Roman ritual/imperial head-covering iconography in the monumental environment of Corinth. It does **not** prove that Paul’s v4 target is exactly this practice.

---

## 1.2 Preferred open photograph + checksum

Commons file page:
- https://commons.wikimedia.org/wiki/File:Statue_of_Augustus_at_the_Archaeological_Museum_of_Corinth_on_January_10,_2020.jpg

Original binary:
- https://upload.wikimedia.org/wikipedia/commons/f/fe/Statue_of_Augustus_at_the_Archaeological_Museum_of_Corinth_on_January_10%2C_2020.jpg

```text
PHOTOGRAPHER = George E. Koronaios
PHOTO_DATE = 2020-01-10
DIMENSIONS = 4000x6000
MIME = image/jpeg
FILE_SIZE = 2568248_bytes
LICENSE = CC_BY_SA_4_0
SHA1 = 5bd067867204a13353d3175fa2c704d60163359a
```

Recommended attribution:

> Photo: George E. Koronaios, Wikimedia Commons, CC BY-SA 4.0. Object: Augustus, Archaeological Museum of Ancient Corinth, inv. S-1116.

```text
S1116_IMAGE_OBJECT_ID = STRONG
S1116_IMAGE_RIGHTS = OPEN_CC_BY_SA_4_0
S1116_IMAGE_CHECKSUM = PINNED
PUBLICATION_CANDIDATE = YES_AFTER_PRODUCT_RIGHTS_GATE
```

---

# 2. S-1088 — veiled Julio-Claudian male portrait head

## 2.1 Object provenance and identity firewall

```text
INVENTORY = S-1088
MATERIAL = marble
MUSEUM = Archaeological Museum of Ancient Corinth
FINDSPOT = Julian Basilica
HEAD_STATE = VEILED_CAPITE_VELATO_TYPE
PERSON_IDENTIFICATION = DISPUTED
```

Current safe label:

> **Veiled Julio-Claudian male portrait head, S-1088**.

Older and modern identifications have included Tiberius / Nero Caesar and other Julio-Claudian possibilities. AJA’s review of *Corinth XXII* describes the second `capite velato` statue cautiously as a Julio-Claudian prince, possibly Nero Caesar.

Routes:
- https://www.journals.uchicago.edu/doi/10.1086/725629
- secondary object bibliography/identity history: https://ancientrome.ru/art/artworken/img.htm?id=6018

```text
CORINTH_S1088_VEILED_MALE_HEAD = STRONG_OBJECT_CONTROL
S1088_EXACT_PERSON = OPEN_DISPUTED
S1088_AS_EMPEROR_NERO_CERTAIN = REJECTED
S1088_AS_NERO_CAESAR = PUBLISHED_IDENTIFICATION_NOT_CERTAINTY
```

---

## 2.2 Preferred open photograph + checksum

Commons file page:
- https://commons.wikimedia.org/wiki/File:Portrait_of_Nero,_1st_cent._A.D._(CAM_S-1088,_1-10-2020).jpg

Original binary:
- https://upload.wikimedia.org/wikipedia/commons/c/ca/Portrait_of_Nero%2C_1st_cent._A.D._%28CAM_S-1088%2C_1-10-2020%29.jpg

```text
PHOTOGRAPHER = George E. Koronaios
PHOTO_DATE = 2020-01-10
DIMENSIONS = 4000x6000
MIME = image/jpeg
FILE_SIZE = 10421038_bytes
LICENSE = CC_BY_SA_4_0
SHA1 = 0752c9a5dbd0269f8da48449e288a3c1e44abfc4
```

Recommended caption:

> Veiled Julio-Claudian male portrait head (often identified as Nero/Nero Caesar), Archaeological Museum of Ancient Corinth, inv. S-1088. Photo: George E. Koronaios, Wikimedia Commons, CC BY-SA 4.0.

```text
S1088_IMAGE_OBJECT_ID = STRONG_INVENTORY_MATCH
S1088_PERSON_ID = OPEN_DISPUTED
S1088_IMAGE_RIGHTS = OPEN_CC_BY_SA_4_0
S1088_IMAGE_CHECKSUM = PINNED
COMMONS_FILENAME_NERO != CERTAIN_PERSON_IDENTIFICATION
```

---

# 3. Archaeological meaning of the pair

S-1116 and S-1088 are stronger for local contextual background than generic Roman examples because both belong to **Roman Corinth itself**, in the Julian Basilica / forum monumental environment.

Safe conclusion:

```text
CAPITE_VELATO_ICONOGRAPHY_PRESENT_IN_ROMAN_CORINTH = VERY_STRONG
ROMAN_CAPITE_VELATO_BACKGROUND = A
```

Unsafe conclusions:

```text
EVERY_CORINTHIAN_MAN_WORSHIPPED_CAPITE_VELATO = FALSE_UNIVERSAL
PAUL_V4_EXACTLY_TARGETS_IMPERIAL_CULT = UNPROVED
CHRISTIAN_MEN_WERE_COPYING_THE_IMPERIAL_STATUES = UNPROVED
```

The 2022 ASCSA monograph is preferable to treating isolated older photographs or proof-texted catalogue entries as the complete archaeological context.

```text
CORINTH_LOCAL_VISUAL_BACKGROUND = A2_STRONG
EXEGETICAL_IDENTIFICATION_V4 = B_C
```

---

# 4. Legacy catalogue mapping

Older scholarship often uses Franklin P. Johnson, *Corinth IX.1* (1931) numbers rather than modern `S-` inventories. These are not additional objects.

## 4.1 Johnson no.134 -> S-1116

Gill 1990 and Boschung 1993 independently tie the Corinth `capite velato` Augustus to Johnson no.134; modern museum/ASCSA control identifies the object as S-1116.

```text
JOHNSON_1931_NO134 = AUGUSTUS_CAPITE_VELATO_CORINTH
MODERN_INVENTORY = S1116
LEGACY_TO_MODERN_MAPPING = HIGH_CONFIDENCE
```

## 4.2 Johnson no.137 -> S-1088

Gill’s second covered imperial image and later object bibliography map Johnson no.137 to modern S-1088.

```text
JOHNSON_1931_NO137 = MODERN_S1088
OBJECT = VEILED_JULIO_CLAUDIAN_MALE_HEAD
JOHNSON_PERSON_ID = NERO_SON_OF_GERMANICUS
CURRENT_PERSON_ID = DISPUTED
```

Object continuity is stronger than person-identification continuity.

## 4.3 Peters 2013 bridge

Later scholarship page-specifically cites Janelle Peters 2013 p.282 alongside the older Johnson catalogue route.

Current safe status:

```text
PETERS_2013_P282 = SECONDARY_PAGE_LOCATOR_TO_LEGACY_CORINTH_OBJECT_CHAIN
JOHNSON_NO134_TO_MODERN_S1116 = HIGH_CONFIDENCE
PETERS_P282_DIRECT_AUTOPSY = HOLD
```

Do not claim Peters herself used the modern inventory `S-1116` unless p.282 is directly read.

---

# 5. Duplicate-counting firewall

Do not count publication stages as independent archaeological objects:

```text
JOHNSON_NO134
GILL_1990_AUGUSTUS
PETERS_2013_LEGACY_ROUTE
MODERN_S1116
=
ONE_ANCHOR_OBJECT_TRADITION
```

Likewise:

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

# 6. Image-custody workflow

For any future product/import use:

```text
1. fetch original Commons binary;
2. compute SHA1/SHA256 locally;
3. compare with pinned custody record;
4. preserve photographer + CC attribution;
5. keep museum object identity separate from Commons filename;
6. record crops/transforms as derivative artifacts;
7. if Commons bytes changed, inspect file history and record a new custody event.
```

Rights boundary:

```text
CC_BY_SA_PHOTO_RIGHTS != RIGHT_TO_CLAIM_EXACT_PAULINE_TRIGGER
OPEN_PHOTO != MUSEUM_ENDORSEMENT
LICENSE != OBJECT_PROVENANCE
```

---

# 7. Preferred visual pair

### Anchor
**Augustus S-1116, capite velato, Julian Basilica, Corinth**

- secure identity;
- direct local archaeological context;
- high-resolution CC BY-SA 4.0 image;
- checksum pinned.

### Nuance object
**Veiled Julio-Claudian male head S-1088**

- second local veiled imperial image;
- disputed personal identity demonstrates why object identity and person label must be separated;
- high-resolution CC BY-SA 4.0 image;
- checksum pinned.

Preserve both even if the exact exegetical reconstruction of v4 changes.

---

# 8. Result

```text
CORE_GRADE_REVERSALS = 0
CORINTH_S1116 = SECURE_LOCAL_CAPITE_VELATO_ANCHOR
CORINTH_S1088 = SECURE_LOCAL_VEILED_MALE_OBJECT_PERSON_ID_OPEN
IMAGE_RIGHTS_AND_CHECKSUMS = PINNED_IN_SAME_LEDGER
ROMAN_CAPITE_VELATO_BACKGROUND = A
V4_EXACT_CAPITE_VELATO = B_C
VISUAL_OBJECT != EXEGETICAL_PROOF
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
