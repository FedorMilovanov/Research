# 1 Коринфянам 11 — Cramer/Paris gr. 227 catena attribution firewall

**Дата:** 2026-08-10  
**Статус:** `PRIMARY-CATENA-EDITION / ATTRIBUTION-FIREWALL / PATRISTIC-RECEPTION / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Why this file exists

Catenae are unusually dangerous for source attribution. A page can preserve multiple excerpts under short author labels such as `Θεοδωρίτου`, `Ἰωάννου`, `Φωτίου`, followed by `Τοῦ Αὐτοῦ` (“of the same [author]”). If labels are not tracked linearly, a real ancient comment can easily be assigned to the wrong Father.

This file controls one such case in the Vatican-type catena on 1 Corinthians.

```text
CATENA_TEXT != SINGLE_AUTHOR_COMMENTARY
TOU_AUTOU = PREVIOUS_EXPLICIT_AUTHOR_LABEL
CATENA_LABEL != INDEPENDENT_AUTHENTICITY_PROOF
DIGITAL_TRANSCRIPTION_LABEL != SILENTLY_NORMALIZE_WITHOUT_CONTROL
```

---

# 1. Edition / object

Scaife ATLAS exposes:

> *Catena In Epistulam I Ad Corinthios (Typus Vaticanus) (e Cod. Paris. gr. 227)*

CTS URN:

`urn:cts:greekLit:tlg4102.tlg012.1st1K-grc1`

Scaife metadata identifies the source edition as:

> J. A. Cramer (ed.), *Catenae Graecorum Patrum in Novum Testamentum*, vol. 5 (Oxford: Oxford University Press, 1841).

Direct routes:

- work metadata: https://atlas.perseus.tufts.edu/library/urn:cts:greekLit:tlg4102.tlg012.1st1K-grc1/
- passage containing 1 Cor 11: https://atlas.perseus.tufts.edu/library/passage/urn:cts:greekLit:tlg4102.tlg012.1st1K-grc1:6-7/

The catena is compiled reception evidence. It is not automatically the same thing as consulting a critical edition of each named Father’s original standalone commentary.

---

# 2. Theodoret: a real labelled reconstruction of the Corinthian situation

Near the opening of the 1 Cor 11 unit, the catena explicitly labels a block:

`Θεοδωρίτου.`

The block states that Corinthian women had been accustomed not to cover their heads even at prayer, and that some, proud of eloquence, attempted to teach in church.

This is important **as Theodoret-attributed reception/reconstruction**.

Safe status:

```text
CATENA_THEODORET_CORINTHIAN_WOMEN_UNCOVERED_AT_PRAYER = DIRECT_LABELLED_CATENA_RECEPTION
CATENA_THEODORET_WOMEN_TRIED_TO_TEACH = DIRECT_LABELLED_CATENA_RECEPTION
THEODORET_RECONSTRUCTION = NOT_INDEPENDENT_FIRST_CENTURY_CORINTH_EVIDENCE
```

Do not use a fifth-century commentator’s reconstruction as though it were an archaeological report from first-century Corinth.

---

# 3. The angels “established at the churches” block — author label is not safe to normalize yet

A later block begins in the Scaife/Cramer digital transcription with the explicit label:

`Κυτίλλου.`

The same block continues through the statement that the woman should be covered because of the angels, glossing them as those:

`τοὺς ταῖς ἐκκλησίαις ἐνιδρυμένους παρὰ Θεοῦ`

— those established by God at/among the churches — who are distressed if the rule of propriety is neglected.

Critical source-hygiene point:

```text
DIGITAL_LABEL = ΚΥΤΙΛΛΟΥ
SILENT_NORMALIZATION_TO_CYRIL/KYRILLOS = NOT_AUTHORIZED_YET
```

The wording may reflect a transcription/OCR/edition issue, and the surrounding theology may suggest an identifiable Father, but this pass does **not** claim a normalized author until the printed Cramer page or manuscript label is directly checked.

Therefore:

```text
ANGELS_ESTABLISHED_AT_CHURCHES_READING = DIRECT_CATENA_FRAGMENT
EXACT_NORMALIZED_AUTHOR = ATTRIBUTION_HOLD
```

This corrects an intermediate overconfident working note that called the block “Cyril” before the label itself was inspected carefully.

---

# 4. `Ἰωάννου` block — do not confuse it with neighboring authors

After the `Κυτίλλου` block the catena explicitly switches to:

`Ἰωάννου.`

The ensuing material interprets male head covering broadly enough to include both garment and long hair and treats female covering as a sign associated with subjection/authority.

Because the label itself says only “John” in the catena transcription, this file does not use this fragment to create a new independent Chrysostom quotation without cross-control from Chrysostom’s directly transmitted homily.

Project rule:

```text
CATENA_IOANNOU != AUTOMATIC_NEW_CHRYSOSTOM_QUOTE
DIRECT_CHRYSOSTOM_HOMILY > CATENA_FOR_CHRYSOSTOM_ATTRIBUTION
```

---

# 5. Photius: `Τοῦ Αὐτοῦ` can be assigned securely by local label tracking

Later, immediately before the v10 interpretive block, the catena explicitly labels material:

`Φωτίου.`

The following paragraph begins:

`Τοῦ Αὐτοῦ.`

Because no intervening explicit author label occurs, `Τοῦ Αὐτοῦ` refers locally to **Photius**.

This gives a directly controlled catena attribution for a substantive v10 interpretation.

## 5.1 Photius on `ἐξουσία`

The fragment says the woman should have/display on her head the authority/lordship of the man to whom she is subject, realized through being covered; it explicitly treats the covering as something that may be called `ἐξουσία` because it indicates that authority.

Safe reception statement:

```text
PHOTIUS_V10_PASSIVE_SIGN_READING = DIRECT_CATENA_ATTRIBUTION
PHOTIUS_COVERING_AS_INDICATOR_OF_MALE_AUTHORITY = DIRECT_CATENA_ATTRIBUTION
```

This is **reception history**, not lexical proof that `ἐξουσία` itself normally means “veil” or “symbol of another person’s authority.” The project’s lexical/syntactic controls remain unchanged.

## 5.2 Photius on the angels

The same fragment says the angels are:

`μάρτυρες καὶ ἐπόπται`

— witnesses and overseers/observers — of the woman’s subjection.

Thus:

```text
PHOTIUS_ANGELS_AS_WITNESSES_OBSERVERS_OF_ORDER = DIRECT_CATENA_ATTRIBUTION
```

This is a genuine ancient/medieval reception variant that belongs near the broader “cosmic witnesses / assembly observers” family, but it does not automatically prove the original Pauline function.

---

# 6. Theodoret guardian-angels claim remains HOLD

Crucially, the inspected Cramer catena passage does **not** directly close the previously reported claim that Theodoret reads the angels of 1 Cor 11:10 specifically as personal guardian angels.

Theodoret-labelled material is present around vv7–16, but the directly inspected v10-region does not give a secure Theodoret-labelled guardian-angels gloss.

Therefore:

```text
THEODORET_GUARDIAN_ANGELS = STRONG_SECONDARY_ATTRIBUTION / PRIMARY_LOCATOR_HOLD
CATENA_DOES_NOT_CLOSE_THEODORET_GUARDIAN_ANGELS = true
```

Do not transfer the `Κυτίλλου` or Photius angel comments to Theodoret merely because Theodoret appears nearby in the catena.

---

# 7. Why this matters for the current angel map

Current reception map now has more sharply separated owners:

```text
TERTULLIAN = WATCHERS/GEN6
CHRYSOSTOM = HEAVENLY_ANGELS_PRESENT_AT_WORSHIP
AMBROSIASTER = BISHOPS
SEVERIAN = REPORTS_SOME_SAY_CHURCH_PRIESTS
CLEMENT_FRAGMENT = RIGHTEOUS/VIRTUOUS_HUMAN_OBSERVERS
PHOTIUS = ANGELS_AS_WITNESSES/OBSERVERS_OF_SUBJECTION
CATENA_KYTILLOU_BLOCK = ANGELS_ESTABLISHED_AT_CHURCHES / NORMALIZED_AUTHOR_HOLD
THEODORET_GUARDIAN_ANGELS = PRIMARY_LOCATOR_HOLD
```

This diversity supports the current project distinction:

```text
ANGEL_REFERENT != EXACT_ANGEL_FUNCTION
EXACT_ANGELIC_FUNCTION = B_C
PATRISTIC_DIVERSITY != ORIGINAL_MEANING_BY_VOTE
```

---

# 8. Catena attribution firewall for future agents

For every catena claim:

1. identify the catena edition/manuscript basis;
2. capture the **nearest preceding explicit author label**;
3. track whether an intervening label occurs;
4. resolve `Τοῦ Αὐτοῦ` only to the immediately controlling explicit label;
5. do not silently normalize a corrupt/odd digital label;
6. prefer a Father’s standalone critical text when available;
7. separate `catena attributes X to author Y` from `author Y certainly wrote X` where authenticity/transmission is not independently controlled.

Machine rule:

```text
CATENA_NEARBY_NAME != CLAIM_OWNER
TOU_AUTOU_WITHOUT_LABEL_TRACKING = NEVER_QUOTE_SAFE
CATENA_ATTRIBUTION != AUTHORIAL_AUTHENTICITY_AUTOMATICALLY
```

---

# 9. Result

```text
CORE_GRADE_REVERSALS = 0
PHOTIUS_V10_PASSIVE_SIGN_READING = DIRECT_CATENA_RECEPTION
PHOTIUS_ANGELS_WITNESSES_OBSERVERS = DIRECT_CATENA_RECEPTION
THEODORET_CORINTH_RECONSTRUCTION = DIRECT_CATENA_RECEPTION_NOT_FIRST_CENTURY_FACT
THEODORET_GUARDIAN_ANGELS = STILL_PRIMARY_LOCATOR_HOLD
KYTILLOU_BLOCK_NORMALIZED_AUTHOR = HOLD
CATENA_ATTRIBUTION_FIREWALL = REQUIRED
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
