# 1 Коринфянам 11:2–16 — visual asset custody / checksum supplement

**Дата:** 2026-08-10  
**Статус:** `VISUAL-CUSTODY / RIGHTS-PINNED / CHECKSUM-PINNED / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Purpose

Основной visual archaeology ledger уже закрепляет object identity/provenance и права. Этот supplement добавляет **конкретную custody-информацию для открытых фотографий**, чтобы будущий агент не потерял правильный файл, не подменил его похожей картинкой и не переписал спорную идентификацию музейного объекта из названия Commons.

```text
OBJECT_ID != PHOTO_FILE
PHOTO_FILE_TITLE != ARCHAEOLOGICAL_IDENTIFICATION_CERTAINTY
COMMONS_PAGE != ORIGINAL_BINARY_URL
LICENSE != OBJECT_PROVENANCE
CHECKSUM = FILE_IDENTITY_CONTROL
```

---

# 1. S-1116 Augustus, Ancient Corinth — preferred open image

## Object

```text
OBJECT = Augustus, capite velato
INVENTORY = S-1116
MUSEUM = Archaeological Museum of Ancient Corinth
FINDSPOT = Julian Basilica, Corinth
```

Object/provenance remains controlled by ASCSA / *Corinth XXII*, not by the Commons caption.

## Preferred Commons asset

File page:

- https://commons.wikimedia.org/wiki/File:Statue_of_Augustus_at_the_Archaeological_Museum_of_Corinth_on_January_10,_2020.jpg

Original binary URL:

- https://upload.wikimedia.org/wikipedia/commons/f/fe/Statue_of_Augustus_at_the_Archaeological_Museum_of_Corinth_on_January_10%2C_2020.jpg

Direct Commons metadata:

```text
PHOTOGRAPHER = George E. Koronaios
DATE = 2020-01-10
DIMENSIONS = 4000 x 6000
MIME = image/jpeg
FILE_SIZE = 2,568,248 bytes
LICENSE = CC BY-SA 4.0
SHA1 = 5bd067867204a13353d3175fa2c704d60163359a
```

Commons description itself identifies inventory S-1116.

Recommended attribution:

> Photo: George E. Koronaios, Wikimedia Commons, CC BY-SA 4.0. Object: Augustus, Archaeological Museum of Ancient Corinth, inv. S-1116.

State:

```text
S1116_IMAGE_OBJECT_ID = STRONG
S1116_IMAGE_RIGHTS = OPEN_CC_BY_SA_4_0
S1116_IMAGE_CHECKSUM = PINNED
S1116_PUBLICATION_CANDIDATE = YES_AFTER_PRODUCT_RIGHTS_GATE
```

---

# 2. S-1088 veiled Julio-Claudian male — preferred open image with caption correction

## Object

```text
OBJECT = veiled Julio-Claudian male portrait head
INVENTORY = S-1088
MUSEUM = Archaeological Museum of Ancient Corinth
FINDSPOT = Julian Basilica
PERSON_IDENTIFICATION = DISPUTED
```

The Commons filename calls the sitter “Nero”. That filename must **not** be converted into an unqualified archaeological conclusion.

## Preferred Commons asset

File page:

- https://commons.wikimedia.org/wiki/File:Portrait_of_Nero,_1st_cent._A.D._(CAM_S-1088,_1-10-2020).jpg

Original binary URL:

- https://upload.wikimedia.org/wikipedia/commons/c/ca/Portrait_of_Nero%2C_1st_cent._A.D._%28CAM_S-1088%2C_1-10-2020%29.jpg

Direct Commons metadata:

```text
PHOTOGRAPHER = George E. Koronaios
DATE = 2020-01-10
DIMENSIONS = 4000 x 6000
MIME = image/jpeg
FILE_SIZE = 10,421,038 bytes
LICENSE = CC BY-SA 4.0
SHA1 = 0752c9a5dbd0269f8da48449e288a3c1e44abfc4
```

Recommended publication caption:

> Veiled Julio-Claudian male portrait head (often identified as Nero/Nero Caesar), Archaeological Museum of Ancient Corinth, inv. S-1088. Photo: George E. Koronaios, Wikimedia Commons, CC BY-SA 4.0.

State:

```text
S1088_IMAGE_OBJECT_ID = STRONG_INVENTORY_MATCH
S1088_PERSON_ID = OPEN/DISPUTED
S1088_IMAGE_RIGHTS = OPEN_CC_BY_SA_4_0
S1088_IMAGE_CHECKSUM = PINNED
S1088_FILENAME_NERO != CERTAIN_PERSON_IDENTIFICATION
```

---

# 3. Why checksums matter

The web has multiple crops/details/photos of both objects. Future image pipelines must not treat “same statue” as “same file”.

For any product/import workflow:

```text
1. fetch original URL;
2. compute SHA-1/SHA-256 locally;
3. compare with custody record where applicable;
4. preserve photographer/license attribution;
5. keep museum object caption separate from photographer filename;
6. record transformations/crops as derivative artifacts.
```

If the retrieved bytes no longer match the pinned Commons SHA-1 because the Commons file has been revised, do not assume corruption. Re-open the Commons file history and record the new revision/hash as a new custody event.

---

# 4. Rights and inference boundary

```text
CC_BY_SA_PHOTO_RIGHTS != RIGHT_TO_CLAIM_EXACT_PAULINE_TRIGGER
OPEN_PHOTO != MUSEUM_ENDORSEMENT
S1116_LOCAL_OBJECT = STRONG_BACKGROUND
S1088_SECOND_LOCAL_OBJECT = STRONG_BACKGROUND
ROMAN_CAPITE_VELATO_BACKGROUND = A
V4_EXACT_CAPITE_VELATO = B_C
PUBLICATION_HOLD = true
```

The two open photographs should be preserved as the preferred visual pair even if the exegetical grade of the exact v4 reconstruction later changes.
