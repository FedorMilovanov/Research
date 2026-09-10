# 1 Коринфянам 11 — Cramer/Paris gr. 227 catena attribution firewall

**Дата:** 2026-08-10  
**Статус:** `PRIMARY-CATENA-EDITION / ATTRIBUTION-FIREWALL / CYRIL-THEODORET-RECONCILED / PHOTIAN-SCHOLIA / TERMINAL-IMAGE-ACCESS-CALIBRATED / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Why this file exists

Catenae are unusually dangerous for source attribution. A page can preserve excerpts under short labels such as `Θεοδωρίτου`, `Ἰωάννου`, `Φωτίου`, followed by `Τοῦ Αὐτοῦ`. If labels are not tracked linearly, a real ancient comment can easily be assigned to the wrong Father.

```text
CATENA_TEXT != SINGLE_AUTHOR_COMMENTARY
TOU_AUTOU = PREVIOUS_CONTROLLING_EXPLICIT_AUTHOR_LABEL
CATENA_LABEL != INDEPENDENT_AUTHENTICITY_PROOF
DIGITAL_TRANSCRIPTION_LABEL != SILENTLY_NORMALIZE_WITHOUT_CONTROL
CATENA_SCHOLION != LOST_STANDALONE_COMMENTARY_DIRECTLY_AVAILABLE
```

Direct PG image transport state is delegated to `dossiers/PATRISTIC_PG_OCR_VERIFICATION_WORKFLOW.md` and synchronized here.

---

# 1. Edition / manuscript basis

Scaife ATLAS exposes:

> *Catena In Epistulam I Ad Corinthios (Typus Vaticanus) (e Cod. Paris. gr. 227)*

CTS URN:
`urn:cts:greekLit:tlg4102.tlg012.1st1K-grc1`

Scaife identifies:
> J. A. Cramer (ed.), *Catenae Graecorum Patrum in Novum Testamentum*, vol. 5 (Oxford, 1841).

Routes:
- https://atlas.perseus.tufts.edu/library/urn:cts:greekLit:tlg4102.tlg012.1st1K-grc1/
- https://atlas.perseus.tufts.edu/library/passage/urn:cts:greekLit:tlg4102.tlg012.1st1K-grc1:6-7/

Modern catena scholarship independently notes that Cramer principally used **Paris, BnF grec 227 (GA 1937)** for the Corinthian epistles and compared additional Oxford witnesses.

```text
CRAMER_1COR_CATENA = REAL_MANUSCRIPT_BASED_EDITION
CRAMER_CATENA != CRITICAL_EDITION_OF_EACH_FATHER
```

---

# 2. Theodoret-labelled Corinth reconstruction

Near the opening of the 1 Cor 11 unit the catena explicitly labels a block:

`Θεοδωρίτου.`

The block reconstructs Corinthian women as praying uncovered and some women as attempting public teaching.

```text
CATENA_THEODORET_CORINTH_RECONSTRUCTION = DIRECT_LABELLED_CATENA_RECEPTION
THEODORET_RECONSTRUCTION != FIRST_CENTURY_CORINTH_EVIDENCE
```

Theodoret’s assigned/guardian-angels interpretation is independently controlled through his standalone commentary at:

```text
PG82_312D_313A
Hill_2001_p205
```

with Acts 12:15 and Matthew 18:10.

```text
CATENA_THEODORET_TRIGGER_RECONSTRUCTION = CATENA_RECEPTION
THEODORET_GUARDIAN_ASSIGNED_ANGELS = STRONG_TWO_ROUTE_PAGE_LOCATED_STANDALONE_RECEPTION
PG82_ORIGINAL_SCAN_OBJECT = CLOSED_PUBLIC_DOMAIN
DIRECT_PG82_312D_313A_PAGE_IMAGE = TERMINAL_TRANSPORT_HOLD_CURRENT_RUNTIME
```

Do not transfer neighboring catena angel fragments to Theodoret.

---

# 3. `Κυτίλλου` strongly normalizes to Cyril of Alexandria

The Cramer/Scaife digital transcription repeatedly gives:

`Κυτίλλου.`

The associated block interprets the angels as:

`τοὺς ταῖς ἐκκλησίαις ἐνιδρυμένους παρὰ Θεοῦ`

Independent fragment-edition provenance establishes:

```text
CYRIL_1COR_FRAGMENT_CORPUS = Pusey_III_249_318 / PG74_856_916
CYRIL_1COR11_ANGEL_BLOCK = PG74_879_883_STRONGLY_LOCATED
```

The sequence and interpretation converge with the catena block.

```text
CATENA_KYTILLOU = STRONGLY_IDENTIFIED_AS_CYRIL_OF_ALEXANDRIA
EXPECTED_LABEL = ΚΥΡΙΛΛΟΥ
DIGITAL_KYTILLOU = CORRUPT_TRANSCRIPTIONAL_OR_EDITIONAL_FORM
PG74_ORIGINAL_SCAN_OBJECT = CLOSED_PUBLIC_DOMAIN
DIRECT_PG74_879_883_PAGE_IMAGE = TERMINAL_TRANSPORT_HOLD_CURRENT_RUNTIME
DIRECT_CRAMER_PRINT_LABEL_IMAGE = OPTIONAL_NONBLOCKING_IMAGE_CHECK
```

Methodological rule:

```text
ODD_LABEL -> DO_NOT_GUESS
ODD_LABEL + INDEPENDENT_FRAGMENT_CORPUS + SAME_SEQUENCE = CALIBRATED_NORMALIZATION
```

---

# 4. `Ἰωάννου` — generic John label firewall

After the Cyril/Kytilou block the catena switches to:

`Ἰωάννου.`

Because this label itself is only `John`, source ownership should be cross-controlled against directly transmitted Chrysostom before calling a specific scholion Chrysostom.

```text
CATENA_IOANNOU != AUTOMATIC_NEW_CHRYSOSTOM_QUOTE
DIRECT_CHRYSOSTOM_HOMILY > CATENA_FOR_CHRYSOSTOM_OWNER
```

---

# 5. Photius — secure local catena attribution

The catena explicitly labels:

`Φωτίου.`

The following v10 paragraph begins:

`Τοῦ Αὐτοῦ.`

No intervening explicit author label occurs; therefore `Τοῦ Αὐτοῦ` resolves locally to **Photius**.

## 5.1 `ἐξουσία`

The scholion explains the covering as indicating the authority/lordship of the man to whom the woman is subject.

```text
PHOTIUS_V10_PASSIVE_SIGN_READING = DIRECT_CATENA_ATTRIBUTION
PHOTIUS_COVERING_AS_INDICATOR_OF_MALE_AUTHORITY = DIRECT_CATENA_ATTRIBUTION
```

Reception history is not lexical proof that `ἐξουσία` normally means veil/sign.

## 5.2 Angels

The same scholion calls the angels:

`μάρτυρες καὶ ἐπόπται`

— witnesses and observers/overseers — of the woman’s subjection.

```text
PHOTIUS_ANGELS_AS_WITNESSES_OBSERVERS = DIRECT_CATENA_ATTRIBUTION
```

## 5.3 PG118 convergence

PG118 OCR page 409 preserves a substantially matching v10 block:
- `ἐξουσία` explained as `κάλυμμα`;
- covering as indication of male authority;
- angels as `μάρτυρες καὶ ἐπόπται`.

```text
CRAMER = OWNER_CONTROL
PG118 = INDEPENDENT_TRANSMISSIONAL_CONVERGENCE
PG118_UNLABELLED_BLOCK != OECUMENIUS_PERSONAL_VIEW_AUTOMATICALLY
PG118_ORIGINAL_SCAN_OBJECT = CLOSED_PUBLIC_DOMAIN
PG118_PAGE409_RENDER = TERMINAL_TRANSPORT_HOLD_CURRENT_RUNTIME
```

---

# 6. Photius transmission target corrected

Chiara Coppola’s Birmingham PhD, *A new analysis of the Scholia Photiana in the Pseudo-Oecumenian catena tradition* (2021), explains that Staab edited numerous scholia ascribed to Photius from the Typus Vaticanus / Erweiterte Typus catena traditions and that a fuller Pauline commentary may have been lost.

Institutional route:
- https://etheses.bham.ac.uk/id/eprint/11932

Jacopo Marcon, *The Pseudo-Oecumenian Catena on Romans* (De Gruyter, 2025), independently studies the Scholia Photiana and Pauline catena types.

Publisher DOI:
- `10.1515/9783111437842`

```text
PHOTIAN_SCHOLIA_IN_CATENAE = REAL_TEXTUAL_TRADITION
LOST_FULLER_PHOTIAN_PAUL_COMMENTARY = SCHOLARLY_HYPOTHESIS
EXTANT_STANDALONE_PHOTIUS_1COR_COMMENTARY_REQUIRED = FALSE_ASSUMPTION
PHOTIUS_STANDALONE_PG101_SEARCH = WRONG_OR_UNNECESSARY_TARGET_FOR_THIS_SCHOLION
PHOTIUS_1COR11_OWNER = CATENA_PRESERVED_SCHOLIA_PHOTIANA
```

---

# 7. Differentiated angel map

```text
TERTULLIAN = WATCHERS_GEN6
CHRYSOSTOM = HEAVENLY_ANGELS_PRESENT_AT_WORSHIP
AMBROSIASTER = BISHOPS
SEVERIAN = REPORTS_SOME_SAY_CHURCH_PRIESTS
CLEMENT_FRAGMENT = RIGHTEOUS_VIRTUOUS_HUMAN_OBSERVERS
CYRIL = ANGELS_ESTABLISHED_AT_OVER_CHURCHES
THEODORET = ANGELS_ASSIGNED_OVER_HUMANS_CARE_OVERSIGHT
PHOTIUS = ANGELS_AS_WITNESSES_OBSERVERS_OF_SUBJECTION
VALENTINIAN_RECEPTION = ACHAMOTH_SAVIOUR_ANGELIC_ATTENDANTS_REPORTED_BY_IRENAEUS
```

```text
ANGEL_REFERENT != EXACT_ANGEL_FUNCTION
EXACT_ANGELIC_FUNCTION = B_C
PATRISTIC_DIVERSITY != ORIGINAL_MEANING_BY_VOTE
```

---

# 8. Catena attribution firewall

For every catena claim:

1. identify catena edition/manuscript basis;
2. capture nearest controlling explicit author label;
3. track every intervening label;
4. resolve `Τοῦ Αὐτοῦ` only locally;
5. do not silently normalize corrupt labels;
6. compare with independently edited fragments/standalone works where available;
7. distinguish catena attribution from independently closed authorial authenticity;
8. do not demand a nonexistent standalone commentary when transmission scholarship identifies catena-preserved remnants.

```text
CATENA_NEARBY_NAME != CLAIM_OWNER
TOU_AUTOU_WITHOUT_LABEL_TRACKING = NEVER_QUOTE_SAFE
CATENA_ATTRIBUTION != AUTHORIAL_AUTHENTICITY_AUTOMATICALLY
LOST_COMMENTARY_HYPOTHESIS != EXTANT_STANDALONE_SOURCE
TRANSMISSIONAL_PARALLEL != INDEPENDENT_HISTORICAL_WITNESS
```

---

# 9. Final disposition

```text
PHOTIUS_V10_PASSIVE_SIGN_READING = DIRECT_CATENA_RECEPTION
PHOTIUS_ANGELS_WITNESSES_OBSERVERS = DIRECT_CATENA_RECEPTION
PHOTIUS_PG118_PARALLEL = STRONG_TRANSMISSIONAL_CONVERGENCE
PHOTIAN_SCHOLIA_CATENA_TRADITION = MODERN_SPECIALIST_CONTROL
PHOTIUS_STANDALONE_PG101_REQUIRED = REJECTED_ASSUMPTION

CYRIL_KYTILLOU_NORMALIZATION = STRONG_MULTI_ROUTE
CYRIL_PG74_SCAN_OBJECT = CLOSED_PUBLIC_DOMAIN
CYRIL_PG74_TARGET_RENDER = TERMINAL_TRANSPORT_HOLD_CURRENT_RUNTIME
THEODORET_GUARDIAN_ASSIGNED_ANGELS = STRONG_TWO_ROUTE_PAGE_LOCATED
THEODORET_PG82_SCAN_OBJECT = CLOSED_PUBLIC_DOMAIN
THEODORET_PG82_TARGET_RENDER = TERMINAL_TRANSPORT_HOLD_CURRENT_RUNTIME
CRAMER_PRINT_LABEL_IMAGE = OPTIONAL_NONBLOCKING

CATENA_ACTIVE_ACQUISITION_QUEUE_FOR_CURRENT_KNOWN_ROUTES = EMPTY
CORE_GRADE_REVERSALS = 0
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
