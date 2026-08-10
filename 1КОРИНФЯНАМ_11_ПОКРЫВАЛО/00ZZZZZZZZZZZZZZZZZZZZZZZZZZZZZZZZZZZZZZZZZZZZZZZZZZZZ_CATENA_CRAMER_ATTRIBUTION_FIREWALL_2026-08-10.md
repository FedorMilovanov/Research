# 1 Коринфянам 11 — Cramer/Paris gr. 227 catena attribution firewall

**Дата:** 2026-08-10  
**Статус:** `PRIMARY-CATENA-EDITION / ATTRIBUTION-FIREWALL / CYRIL-THEODORET-RECONCILED / PHOTIAN-SCHOLIA / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Why this file exists

Catenae are unusually dangerous for source attribution. A page can preserve excerpts under short labels such as `Θεοδωρίτου`, `Ἰωάννου`, `Φωτίου`, followed by `Τοῦ Αὐτοῦ` (“of the same [author]”). If labels are not tracked linearly, a real ancient comment can easily be assigned to the wrong Father.

This file is now reconciled with the later Cyril and Theodoret provenance deltas and with modern research on **Scholia Photiana**.

```text
CATENA_TEXT != SINGLE_AUTHOR_COMMENTARY
TOU_AUTOU = PREVIOUS_CONTROLLING_EXPLICIT_AUTHOR_LABEL
CATENA_LABEL != INDEPENDENT_AUTHENTICITY_PROOF
DIGITAL_TRANSCRIPTION_LABEL != SILENTLY_NORMALIZE_WITHOUT_CONTROL
CATENA_SCHOLION != LOST_STANDALONE_COMMENTARY_DIRECTLY_AVAILABLE
```

---

# 1. Edition / manuscript basis

Scaife ATLAS exposes:

> *Catena In Epistulam I Ad Corinthios (Typus Vaticanus) (e Cod. Paris. gr. 227)*

CTS URN:

`urn:cts:greekLit:tlg4102.tlg012.1st1K-grc1`

Scaife identifies the edition as:

> J. A. Cramer (ed.), *Catenae Graecorum Patrum in Novum Testamentum*, vol. 5 (Oxford, 1841).

Routes:

- https://atlas.perseus.tufts.edu/library/urn:cts:greekLit:tlg4102.tlg012.1st1K-grc1/
- https://atlas.perseus.tufts.edu/library/passage/urn:cts:greekLit:tlg4102.tlg012.1st1K-grc1:6-7/

Modern catena scholarship independently notes that for both Corinthian epistles Cramer principally used **Paris, BnF grec 227 (GA 1937)** and compared additional Oxford witnesses.

Therefore:

```text
CRAMER_1COR_CATENA = REAL_MANUSCRIPT_BASED_EDITION
CRAMER_CATENA != CRITICAL_EDITION_OF_EACH_FATHER
```

---

# 2. Theodoret-labelled Corinth reconstruction

Near the opening of the 1 Cor 11 unit, the catena explicitly labels a block:

`Θεοδωρίτου.`

The block reconstructs Corinthian women as praying uncovered and some women as attempting public teaching.

Safe status:

```text
CATENA_THEODORET_CORINTH_RECONSTRUCTION = DIRECT_LABELLED_CATENA_RECEPTION
THEODORET_RECONSTRUCTION != FIRST_CENTURY_CORINTH_EVIDENCE
```

Later work in this branch independently closed Theodoret’s **assigned/guardian-angels** interpretation through his standalone commentary at:

```text
PG82_312D_313A
Hill 2001 p205
```

with Acts 12:15 and Matthew 18:10 as support texts.

Thus the current distinction is:

```text
CATENA_THEODORET_TRIGGER_RECONSTRUCTION = CATENA_RECEPTION
THEODORET_GUARDIAN_ASSIGNED_ANGELS = STRONG_TWO_ROUTE_PAGE_LOCATED_STANDALONE_RECEPTION
DIRECT_PG82_PAGE_IMAGE = HOLD
```

Do not transfer neighboring catena angel fragments to Theodoret.

---

# 3. `Κυτίλλου` is now strongly normalized to Cyril of Alexandria

The Cramer/Scaife digital transcription repeatedly gives the odd label:

`Κυτίλλου.`

The associated 1 Cor 11 block interprets the angels as:

`τοὺς ταῖς ἐκκλησίαις ἐνιδρυμένους παρὰ Θεοῦ`

— those established by God at/over the churches — who are distressed when propriety is neglected.

The first pass correctly refused to normalize this label by guesswork alone.

Independent fragment-edition provenance later established:

```text
CYRIL_1COR_FRAGMENT_CORPUS = Pusey III 249–318 / PG74 856–916
CYRIL_1COR11_ANGEL_BLOCK = PG74 879–883 STRONGLY_LOCATED
```

The same sequence and angel interpretation converge with the catena block.

Current status therefore supersedes the old HOLD:

```text
CATENA_KYTILLOU = STRONGLY_IDENTIFIED_AS_CYRIL_OF_ALEXANDRIA
EXPECTED_LABEL = ΚΥΡΙΛΛΟΥ
DIGITAL_KYTILLOU = CORRUPT/TRANSCRIPTIONAL_OR_EDITIONAL_FORM
DIRECT_PG74_PAGE_IMAGE = HOLD
DIRECT_CRAMER_PRINT_LABEL_IMAGE = HOLD
```

Methodological lesson:

```text
ODD_LABEL -> DO_NOT_GUESS
ODD_LABEL + INDEPENDENT_FRAGMENT_CORPUS + SAME_SEQUENCE = CALIBRATED_NORMALIZATION
```

---

# 4. `Ἰωάννου` — do not create a new Chrysostom quote from a generic John label

After the Cyril/Kytilou block the catena switches to:

`Ἰωάννου.`

The material interprets male head covering broadly enough to include garment and long hair and treats female covering in an authority/subjection framework.

Because the catena label itself is only `John`, source ownership should be cross-controlled against directly transmitted Chrysostom before calling it Chrysostom.

```text
CATENA_IOANNOU != AUTOMATIC_NEW_CHRYSOSTOM_QUOTE
DIRECT_CHRYSOSTOM_HOMILY > CATENA_FOR_CHRYSOSTOM_OWNER
```

This branch now has such a direct Chrysostom control for his main Homily 26 reconstruction, but the rule remains necessary for each specific scholion.

---

# 5. Photius — secure local catena attribution

Immediately before relevant interpretive material the catena explicitly labels:

`Φωτίου.`

The following v10 paragraph begins:

`Τοῦ Αὐτοῦ.`

No intervening explicit author label occurs. Therefore `Τοῦ Αὐτοῦ` resolves locally to **Photius**.

## 5.1 Photius on `ἐξουσία`

The scholion explains that the woman should have/display on her head the authority/lordship of the man to whom she is subject, realized through covering; the covering itself may be called `ἐξουσία` because it indicates male authority.

```text
PHOTIUS_V10_PASSIVE_SIGN_READING = DIRECT_CATENA_ATTRIBUTION
PHOTIUS_COVERING_AS_INDICATOR_OF_MALE_AUTHORITY = DIRECT_CATENA_ATTRIBUTION
```

This is reception history, not lexical proof that `ἐξουσία` normally means `veil` or `symbol of someone else’s authority`.

## 5.2 Photius on the angels

The same scholion calls the angels:

`μάρτυρες καὶ ἐπόπται`

— witnesses and observers/overseers — of the woman’s subjection.

```text
PHOTIUS_ANGELS_AS_WITNESSES_OBSERVERS = DIRECT_CATENA_ATTRIBUTION
```

## 5.3 PG118 gives independent transmission convergence

The 2026 CGPG OCR corpus locates on PG118 PDF page 409 a substantially matching v10 block:

- `ἐξουσία` explained as `κάλυμμα`;
- covering as indication of male authority;
- angels as `μάρτυρες καὶ ἐπόπται`.

PG118 does not by itself label that entire block as Photius, so source ownership still comes from Cramer’s explicit `Φωτίου -> Τοῦ Αὐτοῦ` sequence.

```text
CRAMER = OWNER_CONTROL
PG118 = INDEPENDENT_TRANSMISSIONAL_CONVERGENCE
PG118_UNLABELLED_BLOCK != OECUMENIUS_PERSONAL_VIEW_AUTOMATICALLY
```

---

# 6. Important correction: PG101 standalone search is not the right evidential target

An attempted search for a standalone Photius commentary in PG101 produced access/index failures. Modern specialist research clarifies why that route should **not** be treated as the required endpoint.

## 6.1 Coppola 2021

Chiara Coppola, University of Birmingham PhD:

> *A new analysis of the Scholia Photiana in the Pseudo-Oecumenian catena tradition* (2021).

Institutional route:

- https://etheses.bham.ac.uk/id/eprint/11932

Her abstract explains that Karl Staab edited numerous scholia ascribed to Photius from the **Typus Vaticanus** and **Erweiterte Typus** catena traditions and hypothesized that the scholia may derive from a more extended Pauline commentary by Photius that has since been **lost**.

Therefore:

```text
PHOTIAN_SCHOLIA_IN_CATENAE = REAL_TEXTUAL_TRADITION
LOST_FULLER_PHOTIAN_PAUL_COMMENTARY = SCHOLARLY_HYPOTHESIS
EXTANT_STANDALONE_PHOTIUS_1COR_COMMENTARY_REQUIRED = FALSE_ASSUMPTION
```

## 6.2 Marcon 2025

Jacopo Marcon, *The Pseudo-Oecumenian Catena on Romans* (De Gruyter, 2025), devotes a full chapter to:

> `The Scholia Photiana in the manuscripts of Staab’s Erweiterter Typus (CPG C165.3)`

and separately studies relationships among the Pauline catena types, including Typus Vaticanus.

Publisher route:

- De Gruyter/Brill book DOI `10.1515/9783111437842`.

This current scholarship supports treating **catena-preserved Photian scholia** as the primary surviving evidence class, rather than assuming that PG101 must contain a complete standalone Pauline commentary.

Current rule:

```text
PHOTIUS_STANDALONE_PG101_SEARCH = WRONG_OR_UNNECESSARY_TARGET_FOR_THIS_SCHOLION
PHOTIUS_1COR11_OWNER = CATENA_PRESERVED_SCHOLIA_PHOTIANA
POSSIBLE_LOST_FULL_COMMENTARY != EXTANT_OBJECT
```

This improves provenance without proving that every Photian-labelled scholion is authorially authentic beyond question.

---

# 7. Current differentiated angel map

```text
TERTULLIAN = WATCHERS/GEN6
CHRYSOSTOM = HEAVENLY_ANGELS_PRESENT_AT_WORSHIP
AMBROSIASTER = BISHOPS
SEVERIAN = REPORTS_SOME_SAY_CHURCH_PRIESTS
CLEMENT_FRAGMENT = RIGHTEOUS/VIRTUOUS_HUMAN_OBSERVERS
CYRIL = ANGELS_ESTABLISHED_AT/OVER_CHURCHES; ECCLESIAL_PROPRIETY
THEODORET = ANGELS_ASSIGNED_OVER_HUMANS; CARE/OVERSIGHT
PHOTIUS = ANGELS_AS_WITNESSES/OBSERVERS_OF_SUBJECTION
VALENTINIAN_RECEPTION = ACHAMOTH/SAVIOUR_ANGELIC_ATTENDANTS_REPORTED_BY_IRENAEUS
```

This diversity supports:

```text
ANGEL_REFERENT != EXACT_ANGEL_FUNCTION
EXACT_ANGELIC_FUNCTION = B_C
PATRISTIC_DIVERSITY != ORIGINAL_MEANING_BY_VOTE
```

---

# 8. Catena attribution firewall for future agents

For every catena claim:

1. identify catena edition and manuscript basis;
2. capture the nearest controlling explicit author label;
3. track every intervening label;
4. resolve `Τοῦ Αὐτοῦ` only locally;
5. do not silently normalize corrupt/odd labels;
6. compare with independently edited fragments/standalone works where they exist;
7. distinguish `catena attributes X to author Y` from `authorial authenticity independently closed`;
8. do **not** demand a nonexistent standalone commentary when modern transmission scholarship identifies the scholia as catena-preserved remnants.

Machine rules:

```text
CATENA_NEARBY_NAME != CLAIM_OWNER
TOU_AUTOU_WITHOUT_LABEL_TRACKING = NEVER_QUOTE_SAFE
CATENA_ATTRIBUTION != AUTHORIAL_AUTHENTICITY_AUTOMATICALLY
LOST_COMMENTARY_HYPOTHESIS != EXTANT_STANDALONE_SOURCE
TRANSMISSIONAL_PARALLEL != INDEPENDENT_HISTORICAL_WITNESS
```

---

# 9. Result

```text
CORE_GRADE_REVERSALS = 0

PHOTIUS_V10_PASSIVE_SIGN_READING = DIRECT_CATENA_RECEPTION
PHOTIUS_ANGELS_WITNESSES_OBSERVERS = DIRECT_CATENA_RECEPTION
PHOTIUS_PG118_PARALLEL = STRONG_TRANSMISSIONAL_CONVERGENCE
PHOTIAN_SCHOLIA_CATENA_TRADITION = MODERN_SPECIALIST_CONTROL
PHOTIUS_STANDALONE_PG101_REQUIRED = REJECTED_ASSUMPTION

CYRIL_KYTILLOU_NORMALIZATION = STRONG_MULTI_ROUTE
THEODORET_GUARDIAN_ASSIGNED_ANGELS = STRONG_TWO_ROUTE_PAGE_LOCATED

CATENA_ATTRIBUTION_FIREWALL = REQUIRED
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
