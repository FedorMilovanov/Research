# Patristic PG OCR verification workflow — coverage-aware evidence control

**Статус:** `EVERGREEN-DOSSIER / OCR-LOCATOR / PG118-LIVE-TEST / PATRISTIC-SOURCE-HYGIENE / RESEARCH-ONLY / PUBLICATION-HOLD`  
**Последняя проверка:** 2026-08-10

## 0. Назначение

В 2026 году появился открытый машинно-читаемый корпус *Patrologia Graeca*, который может резко ускорить поиск древних комментариев и фрагментов. Но OCR нельзя превращать в новый источник ложной точности.

Разрешённый pipeline:

```text
OCR CORPUS
-> LOCATE VOLUME / PDF PAGE / LINE
-> IDENTIFY ORIGINAL PG BINARY
-> OPEN ORIGINAL PG IMAGE
-> VERIFY AUTHOR LABEL / COLUMN / GREEK
-> ONLY THEN QUOTE-SAFE
```

Никогда:

```text
OCR HIT -> DIRECT PRIMARY QUOTE
```

---

# 1. Новый открытый ресурс 2026

## 1.1 Project / dataset

CGPG / *Patrologia Graeca (OCRized and analyzed texts)*.

Zenodo v3:

- DOI `10.5281/zenodo.19915273`;
- published April 2026;
- creators/project members: Jean-Marie Auwers, Chahan Vidal-Gorène, Bastien Kindt, Véronique Somers;
- Zenodo points to raw GitHub: `https://github.com/calfa-co/Patrologia-Graeca`.

Primary routes:

- https://zenodo.org/records/19915273
- https://github.com/calfa-co/Patrologia-Graeca

## 1.2 Technical paper

Chahan Vidal-Gorène and Bastien Kindt, “The Patrologia Graeca Corpus: OCR, Annotation, and Open Release of Noisy Nineteenth-Century Polytonic Greek Editions,” LREC 2026 / arXiv `2603.09470`.

- https://arxiv.org/abs/2603.09470

Reported performance/scale:

```text
CHARACTER_ERROR_RATE = 1.05_PERCENT
WORD_ERROR_RATE = 4.69_PERCENT
CORPUS_SCALE = ABOUT_6_MILLION_LEMMATIZED_POS_TAGGED_TOKENS
```

Thus:

```text
PG2026_OCR = HIGH_VALUE_LOCATOR_RESOURCE
PG2026_OCR != CRITICAL_EDITION
PG2026_OCR != ZERO_ERROR_TRANSCRIPTION
```

---

# 2. Current repository coverage — live README is controlling

An earlier connector snapshot exposed a different 33-volume list. A direct re-read of the current raw GitHub README showed that this list had changed. The earlier exact list is therefore superseded and must not be reused.

Current raw README coverage on 2026-08-10:

```text
3, 5, 6, 8, 9, 16.3, 21, 42,
67, 71, 73, 87.1, 101, 107, 109,
112, 113, 118, 121, 122, 123, 124, 125, 126,
134, 139, 146, 148, 151, 153, 155, 157, 158
```

Source-control rule:

```text
LIVE_RAW_README > EARLIER_CONNECTOR_SNAPSHOT_FOR_CURRENT_COVERAGE
COVERAGE_LIST_CAN_CHANGE = true
CHECK_VOLUME_LIVE_BEFORE_EVERY_NEGATIVE_SEARCH = mandatory
```

For current 1 Cor 11 targets:

```text
PG74_CYRIL = NOT_COVERED_CURRENTLY
PG82_THEODORET = NOT_COVERED_CURRENTLY
PG118_OECUMENIUS = COVERED_CURRENTLY
```

Therefore PG2026 does **not** by itself close:

- Cyril PG 74, 879–883 direct-image HOLD;
- Theodoret PG 82, 312D–313A direct-image HOLD.

---

# 3. File format and locator mapping

Current README documents aligned OCR output and paragraph metadata:

```text
$0 = PG volume
$8 = PDF page
$9 = starting line
```

Raw volume files include aligned text; linguistic tagged data are also distributed through Zenodo.

The key evidence use is locator generation:

```text
1. search OCR
2. capture $0 / $8 / $9
3. identify the exact edition PDF
4. inspect the corresponding PDF page image
5. compare author labels / surrounding context
6. record printed PG column if recoverable
7. then promote quotation status
```

---

# 4. OCR-risk firewall

The project’s recent catena work already shows why one-letter OCR errors matter:

- `Κυτίλλου` required independent convergence before normalization toward Cyril;
- `Τοῦ Αὐτοῦ` requires local author-label tracking;
- multiple Fathers can share a page;
- an OCR error in a proper name can create a false source owner.

At CER ~1.05% OCR remains unsafe by itself for:

```text
AUTHOR_LABEL_AUTOPSY
ACCENT/BREATHING_ARGUMENTS
RARE_PROPER_NAMES
ONE_LETTER_VARIANTS
TEXT_CRITICAL_READINGS
EXACT_QUOTE_PUNCTUATION
```

Rules:

```text
OCR_AUTHOR_LABEL = DISCOVERY_ONLY_UNTIL_IMAGE
OCR_TEXTUAL_VARIANT = NEVER_TEXT_CRITICAL_PROOF_BY_ITSELF
OCR_QUOTE = NOT_QUOTE_SAFE_UNTIL_IMAGE
```

---

# 5. PG118 live test — successful OCR localization of 1 Cor 11

## 5.1 Raw object successfully opened

Raw file:

- `PG118/PG118_text.txt`
- public GitHub raw object
- approximately 3970 OCR paragraphs/lines in the web rendering.

The current pass successfully searched and opened the 1 Cor 11 region.

```text
PG118_TEXT_BODY_READ = true
PG118_1COR11_HIT = true
```

## 5.2 1 Cor 11:2–16 region

The OCR places the beginning of the passage around:

```text
$0=118
$8=406
$9=1
```

and the v10 discussion crosses PDF pages 408–410.

The v10/Clement material is specifically located at:

```text
PDF_PAGE = 409
```

The OCR is visibly noisy (`κεραλῇ`, malformed accents/letters, etc.), which independently demonstrates why it cannot be quote-safe without image verification.

## 5.3 Photius-parallel v10 block

PG118 page 409 preserves a long interpretation in which:

- `ἐξουσία` is explained as `κάλυμμα`;
- the covering indicates the authority/lordship of the man;
- `διὰ τοὺς ἀγγέλους` is explained with angels as `μάρτυρες καὶ ἐπόπται` of the woman’s subjection.

This language closely matches the independently controlled Cramer catena block attributed locally to **Photius**.

Safe conclusion:

```text
PG118_PHOTIUS_PARALLEL_TRANSMISSION = STRONG_OCR_TEXTUAL_CONVERGENCE
PG118_UNLABELLED_BLOCK_OWNER_BY_ITSELF = NOT_ASSIGNED
CRAMER_AUTHOR_LABEL_CONTROL > PG118_UNLABELLED_OCR_FOR_OWNER
```

Do **not** call this “Oecumenius’s own interpretation” merely because it appears in PG118. The volume’s own preface describes compilation/abridgment of Chrysostom and named excerpts from other Fathers, including Photius.

## 5.4 Clement fragment independently located in PG118

Immediately after the witness/observer angel block the OCR explicitly reads in substance:

```text
Ὁ Κλήμης ἐν τρίτῳ τῶν ὑποτυπώσεων ...
```

and reports that Clement identifies the angels as righteous/virtuous human beings, with covering required so they are not scandalized toward fornication; the actual heavenly angels would see the woman even if covered.

Current status:

```text
CLEMENT_HYPOTYPOSES_BOOK3_FRAGMENT_PG118 = OCR_IMAGE_LOCATED
CLEMENT_FRAGMENT_PDF_PAGE = 409
CLEMENT_HUMAN_OBSERVER_READING = INDEPENDENTLY_RELOCATED_IN_PG118_OCR
DIRECT_IMAGE_VERIFIED = false
```

This strengthens provenance for the already-known Clement fragment without changing its project probability grade.

---

# 6. Original PG118 binary identified

Wikimedia Commons provides a public-domain original scan:

> `Patrologia Graeca Vol. 118.pdf`

Object metadata:

```text
PAGES = 684
FILE_SIZE = about 87.24 MB
SHA1 = ceaa386b11edb3e4ae01971ab15e66a433952998
PUBLIC_DOMAIN = true
```

The Commons page exposes navigation through page 409 and the original PDF binary.

Current runtime limitation:

```text
PG118_ORIGINAL_BINARY_IDENTIFIED = true
PG118_PAGE409_SCREENSHOT_AUTOPSY = NOT_COMPLETED
```

The web PDF fetch returned an internal transport error despite the Commons object being valid. Therefore visual verification is still HOLD.

This is a **transport limitation**, not evidence against the OCR locator.

---

# 7. Existing Cyril / Theodoret status remains separate

## Cyril

```text
Cyril 1 Cor fragment corpus = Pusey III 249–318 / PG74 856–916
1 Cor 11 angel block = PG74 879–883 strongly located
Cramer Kytilou -> Cyril = strong multi-route attribution
PG74_IN_PG2026 = false
DIRECT_PG74_IMAGE = HOLD
```

## Theodoret

```text
Standalone 1 Cor commentary = PG82 225D–376A
v10 locator = PG82 312D–313A
modern translation = Hill 2001 p205
assigned/guardian-angels reception = strong two-route page-located
PG82_IN_PG2026 = false
DIRECT_PG82_IMAGE = HOLD
```

---

# 8. Evidence labels for corpus-assisted patristic work

```text
OCR_DISCOVERY
  corpus hit only

OCR_IMAGE_LOCATED
  volume/page/line mapped and source binary identified

DIRECT_IMAGE_VERIFIED
  source page visually inspected and Greek matched

DIRECT_IMAGE_PLUS_CRITICAL_EDITION
  image checked and controlled against critical/modern edition
```

For source ownership:

```text
CATENA_LABEL_OCR_ONLY
CATENA_LABEL_IMAGE_VERIFIED
STANDALONE_AUTHOR_TEXT_LOCATED
STANDALONE_AUTHOR_TEXT_IMAGE_VERIFIED
```

Never collapse these into generic `VERIFIED`.

---

# 9. Current project use cases

Immediate useful targets:

1. obtain/render PG118 page 409 and visually verify Clement + surrounding author transitions;
2. search PG118 for additional explicit named fragments around 1 Cor 11;
3. search current covered PG volumes for reused formulas around `ἐξουσία`, `κεφαλή`, `κατακαλύπτω`, angels and ritual order;
4. use OCR only to generate exact image locators;
5. keep original scan / critical edition as quote authority.

Not valid:

```text
CORPUS_FREQUENCY = ORIGINAL_PAULINE_MEANING
LATE_PATRISTIC_USAGE = FIRST_CENTURY_SEMANTICS
OCR_MATCH = AUTHORIAL_AUTHENTICITY
OCR_ABSENCE = FATHER_NEVER_SAID_X
```

---

# 10. Coverage firewall

Before every PG2026 search:

```text
READ_CURRENT_RAW_README
CHECK_TARGET_VOLUME
```

If volume absent:

```text
DO_NOT_REPORT_NO_HIT
USE_ORIGINAL_PG_SCAN / CRITICAL_EDITION / MANUSCRIPT_ROUTE
```

If volume present but search is empty:

```text
NO_OCR_HIT != PASSAGE_ABSENT
```

Possible causes include OCR error, spelling variation, wrong edition, omitted layout, lemmatization failure or attribution mismatch.

---

# 11. Result

```text
PG2026_CORPUS = REAL_CURRENT_OPEN_RESEARCH_TOOL
ZENODO_V3 = APRIL_2026
RAW_GITHUB = calfa-co/Patrologia-Graeca
CER = 1.05_PERCENT
WER = 4.69_PERCENT

EARLIER_EXACT_COVERAGE_LIST = SUPERSEDED_BY_LIVE_README
PG74_COVERAGE = false
PG82_COVERAGE = false
PG118_COVERAGE = true

PG118_1COR11_OCR = CLOSED
PG118_CLEMENT_FRAGMENT = OCR_IMAGE_LOCATED_PAGE409
PG118_PHOTIUS_PARALLEL = STRONG_TRANSMISSIONAL_CONVERGENCE
PG118_ORIGINAL_SCAN_SHA1 = ceaa386b11edb3e4ae01971ab15e66a433952998
PG118_PAGE409_DIRECT_IMAGE = HOLD_TRANSPORT

CYRIL_DIRECT_IMAGE_HOLD = UNCHANGED
THEODORET_DIRECT_IMAGE_HOLD = UNCHANGED

OCR_LOCATOR -> PRIMARY_IMAGE -> QUOTE_SAFE = REQUIRED
OCR_ALONE -> QUOTE_SAFE = PROHIBITED
CORE_GRADE_REVERSALS = 0
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
