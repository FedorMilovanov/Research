# Patristic PG OCR verification workflow — coverage-aware evidence control

**Статус:** `EVERGREEN-DOSSIER / OCR-LOCATOR / PATRISTIC-SOURCE-HYGIENE / RESEARCH-ONLY / PUBLICATION-HOLD`  
**Последняя проверка:** 2026-08-10

## 0. Назначение

В 2026 году появился открытый машинно-читаемый корпус *Patrologia Graeca*, который может резко ускорить поиск древних комментариев и фрагментов. Но OCR нельзя превращать в новый источник ложной точности.

Этот dossier задаёт единственный разрешённый pipeline:

```text
OCR CORPUS
-> LOCATE VOLUME / PDF PAGE / LINE
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
- Zenodo explicitly points to the raw GitHub repository:
  `https://github.com/calfa-co/Patrologia-Graeca`.

Primary dataset route:

- https://zenodo.org/records/19915273

Raw repository:

- https://github.com/calfa-co/Patrologia-Graeca

## 1.2 Technical paper

Chahan Vidal-Gorène and Bastien Kindt, “The Patrologia Graeca Corpus: OCR, Annotation, and Open Release of Noisy Nineteenth-Century Polytonic Greek Editions,” LREC 2026 / arXiv `2603.09470`.

Direct arXiv route:

- https://arxiv.org/abs/2603.09470

The paper reports approximately:

```text
CHARACTER_ERROR_RATE = 1.05_PERCENT
WORD_ERROR_RATE = 4.69_PERCENT
CORPUS_SCALE = ABOUT_6_MILLION_LEMMATIZED_POS_TAGGED_TOKENS
```

These are excellent OCR results for degraded nineteenth-century polytonic Greek, but **not zero-error text**.

Therefore:

```text
PG2026_OCR = HIGH_VALUE_LOCATOR_RESOURCE
PG2026_OCR != CRITICAL_EDITION
PG2026_OCR != ZERO_ERROR_TRANSCRIPTION
```

---

# 2. Current repository coverage — do not assume all PG volumes exist

The current project README lists the processed volumes as:

```text
19, 24, 27, 32, 33, 37,
53, 54, 55, 56, 57, 58, 59,
61, 62, 63, 64, 65, 67,
71, 73,
94,
102, 103, 104, 105, 106, 107,
116, 117, 118, 120, 122
```

Thus for the present 1 Cor 11 work:

```text
PG74_CYRIL = NOT_COVERED_CURRENTLY
PG82_THEODORET = NOT_COVERED_CURRENTLY
PG118_OECUMENIUS = COVERED_CURRENTLY
```

Critical rule:

```text
PROJECT_EXISTS != TARGET_VOLUME_EXISTS
```

The discovery of the 2026 corpus does **not** close:

- Cyril PG 74, 879–883 direct-image HOLD;
- Theodoret PG 82, 312D–313A direct-image HOLD.

Those volumes must still be checked through their actual PG scans / other critical editions.

---

# 3. File format and locator mapping

The repository README documents, for each processed volume:

```text
PG[volume]_text.txt
PG[volume]_lemma.txt
PG[volume]_pos.txt
```

Paragraph metadata use tags including:

```text
$0 = PG volume
$8 = PDF page
$9 = starting line on that page
```

The project further explains that line offsets map back to source-page images under the volume’s image structure.

This is the key evidential value:

> OCR hits can be converted into an **image locator**, instead of remaining detached searchable text.

Required workflow:

```text
1. search text/lemma corpus
2. capture $0 / $8 / $9
3. retrieve source page image
4. inspect the exact Greek line visually
5. compare surrounding author headings / catena transitions
6. record PG printed-column locator where possible
7. only then promote a quotation to direct-primary status
```

---

# 4. Why OCR is especially dangerous in the current project

Our recent catena work already demonstrated that one altered author label can create a false patristic owner.

Examples:

- Cramer/Scaife `Κυτίλλου` required independent work/edition convergence before normalization to Cyril;
- `Τοῦ Αὐτοῦ` can only be assigned by tracking the immediately controlling explicit author label;
- catena fragments can contain several Fathers on a single page;
- one letter in a proper name can change source ownership.

With a reported CER of ~1.05%, a corpus can be excellent for discovery while still being unsafe for:

```text
AUTHOR_LABEL_AUTOPSY
ACCENT/BREATHING_ARGUMENTS
RARE_PROPER_NAMES
ONE_LETTER_VARIANTS
TEXT_CRITICAL_READINGS
EXACT_QUOTE_PUNCTUATION
```

Therefore:

```text
OCR_AUTHOR_LABEL = DISCOVERY_ONLY_UNTIL_IMAGE
OCR_TEXTUAL_VARIANT = NEVER_TEXT_CRITICAL_PROOF_BY_ITSELF
OCR_QUOTE = NOT_QUOTE_SAFE_UNTIL_IMAGE
```

---

# 5. PG118 — useful future target, but not yet read in this runtime

The raw GitHub repository exposes a `PG118` directory with files including:

```text
PG118_text.txt
PG118_lemma.txt
PG118_pos.txt
```

PG118 contains Oecumenius / Pauline commentary material relevant to this project’s reception-history work.

However, the text file is several megabytes. The current GitHub connector identified the file/blob but did not return a usable complete body through the normal fetch path during this pass.

Therefore current state:

```text
PG118_PRESENT = VERIFIED_REPOSITORY
PG118_TEXT_BYTES_USEFULLY_PARSED_IN_THIS_PASS = false
PG118_1COR11_HIT = NOT_CLAIMED
```

Do not write that Clement/Oecumenius fragments were newly verified from PG118 until the actual OCR hit and source image are retrieved.

---

# 6. Existing Cyril / Theodoret status remains separate

## Cyril of Alexandria

Current source chain:

```text
Cyril 1 Cor fragment corpus = Pusey III 249–318 / PG74 856–916
1 Cor 11 angel block = PG74 879–883 strongly located
Cramer Kytilou -> Cyril = strong multi-route attribution
DIRECT PG74 IMAGE = HOLD
```

PG2026 cannot close the image hold because PG74 is not in current coverage.

## Theodoret

Current source chain:

```text
Standalone 1 Cor commentary = PG82 225D–376A
v10 locator = PG82 312D–313A
modern translation = Hill 2001 p205
assigned/guardian-angels reception = strong two-route page-located
DIRECT PG82 IMAGE = HOLD
```

PG2026 cannot close the image hold because PG82 is not in current coverage.

---

# 7. Evidence labels for corpus-assisted patristic work

Use these explicit states:

```text
OCR_DISCOVERY
  corpus hit only

OCR_IMAGE_LOCATED
  volume/page/line mapped, image not yet checked

DIRECT_IMAGE_VERIFIED
  source page visually inspected and Greek matched

DIRECT_IMAGE_PLUS_CRITICAL_EDITION
  image checked and controlled against a critical/modern edition
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

# 8. Current project use cases

High-value future use of the corpus:

1. search PG118 for Oecumenius/Clement reception around 1 Cor 11:10;
2. search covered volumes for parallel phrases about `ἐξουσία`, `κεφαλή`, `κατακαλύπτω`, angels and ecclesial ritual;
3. discover cross-patristic reuse of the same exegetical formula;
4. locate rare author labels in processed catena/commentary volumes;
5. generate image locators before any quotation enters synthesis.

Not valid uses:

```text
CORPUS_FREQUENCY = ORIGINAL_PAULINE_MEANING
LATE_PATRISTIC_USAGE = FIRST_CENTURY_SEMANTICS
OCR_MATCH = AUTHORIAL_AUTHENTICITY
OCR_ABSENCE = FATHER_NEVER_SAID_X
```

Coverage is partial, transmission is selective, and PG itself is not a modern critical corpus.

---

# 9. Coverage firewall for agents

Before every PG2026 search:

```text
CHECK_VOLUME_IN_README = mandatory
```

If volume absent:

```text
STOP
USE_ORIGINAL_PG_SCAN / PUSEY / CRITICAL_EDITION / MANUSCRIPT_ROUTE
DO_NOT_REPORT_NO_HIT
```

If volume present but no OCR hit:

```text
NO_OCR_HIT != PASSAGE_ABSENT
```

Possible causes include:

- OCR error;
- spelling/orthographic variation;
- page/layout omission;
- wrong target edition;
- wrong attribution;
- lemmatization failure.

---

# 10. Result

```text
PG2026_CORPUS = REAL_CURRENT_OPEN_RESEARCH_TOOL
ZENODO_V3 = APRIL_2026
RAW_GITHUB = calfa-co/Patrologia-Graeca
CER = 1.05_PERCENT
WER = 4.69_PERCENT

PG74_COVERAGE = false
PG82_COVERAGE = false
PG118_COVERAGE = true

CYRIL_DIRECT_IMAGE_HOLD = UNCHANGED
THEODORET_DIRECT_IMAGE_HOLD = UNCHANGED
PG118_BODY_READ = NOT_COMPLETED

OCR_LOCATOR -> PRIMARY_IMAGE -> QUOTE_SAFE = REQUIRED
OCR_ALONE -> QUOTE_SAFE = PROHIBITED
CORE_GRADE_REVERSALS = 0
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
