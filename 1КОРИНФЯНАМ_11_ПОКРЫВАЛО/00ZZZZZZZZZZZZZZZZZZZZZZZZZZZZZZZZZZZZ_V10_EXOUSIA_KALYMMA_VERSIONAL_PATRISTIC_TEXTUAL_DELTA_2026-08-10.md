# 1 Коринфянам 11:10 — `ἐξουσίαν` / `κάλυμμα` versional-patristic textual delta

**Дата:** 2026-08-10  
**Статус:** `TEXTUAL-VARIANT / VERSIONAL-PATRISTIC / GREEK-MANUSCRIPT-CONTROL / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Question

Ранние версии и патристические цитаты иногда передают 1 Cor 11:10 в форме `veil/covering`, что легко превращается в слишком сильный тезис:

> “у Иринея / в раннем греческом тексте стояло `κάλυμμα` вместо `ἐξουσία`”.

Этот проход отделяет:

```text
EXTANT_GREEK_MANUSCRIPT_READING
VERSIONAL_READING
PATRISTIC_QUOTATION/PARAPHRASE
RECONSTRUCTED_GREEK_EXEMPLAR
EXEGETICAL_GLOSS
```

---

# 1. Greek manuscript tradition — `ἐξουσίαν`

STEP Bible’s VarApp aggregation for 1 Cor 11:10 lists `ἐξουσίαν` with a very broad Greek manuscript base including:

```text
P46
א
A B C D F G H K L P Ψ
0150
6 33 81 88 104 181 ...
Byzantine / lectionary tradition
```

Route:

- https://www.stepbible.org/?q=version%3DVarApp%40reference%3D1Cor.11

The same entry includes multiple versions and fathers on the `ἐξουσίαν` side.

The crucial minimum is:

```text
EXTANT_GREEK_MANUSCRIPT_SUPPORT_FOR_EXOUSIAN = OVERWHELMING/UNIFORM_IN_LISTED_WITNESSES
EXTANT_GREEK_MANUSCRIPT_SUPPORT_FOR_KALYMMA = NONE_LISTED
P46_EXOUSIAN = DIRECT_APPARATUS_ATTESTED
```

This strongly supports the current Greek text-base contract.

---

# 2. Where `κάλυμμα` actually appears in the apparatus tradition

STEP VarApp places `κάλυμμα` with **versional and patristic**, not extant Greek manuscript, witnesses, including categories such as:

```text
Old Latin it(c)
some Vulgate manuscripts
part of Bohairic Coptic
Armenian
Valentinians according to Irenaeus
Ptolemy according to Irenaeus (Greek attribution in apparatus tradition)
Irenaeus Latin tradition
selected patristic quotation traditions
```

The precise apparatus also shows mixed patristic transmission: some fathers/manuscript traditions are cited on both sides in different occurrences.

Therefore the right classification is:

```text
KALYMMA = EARLY_VERSIONAL/PATRISTIC_GLOSS_OR_ALTERNATIVE_TRANSMISSION
NOT = EXTANT_GREEK_NT_MANUSCRIPT_RIVAL
```

This distinction is essential.

---

# 3. Independent peer-reviewed control — Newberry / Thiselton

Julie Newberry’s *New Testament Studies* article, in detailed Cambridge apparatus, states that the textual support for `κάλυμμα` at v10 is weak and identifies it as an early gloss on `ἐξουσίαν`, citing Thiselton p.837.

Direct Cambridge route:

- https://www.cambridge.org/core/journals/new-testament-studies/article/abs/pauls-allusive-reasoning-in-1-corinthians-11712/EDE6D54A62D2265EA2C22291B6F2BA39

Safe result:

```text
KALYMMA_TEXTUAL_SUPPORT = WEAK_VERSIONAL/PATRISTIC
KALYMMA_AS_EARLY_GLOSS = STRONG_SCHOLARLY_TEXTUAL_ASSESSMENT
EXOUSIAN_CURRENT_TEXT = A_HIGH
```

No current grade change is needed; this improves witness precision.

---

# 4. Irenaeus / Valentinians — wording must be source-calibrated

The transmitted Irenaean report of Valentinian exegesis renders the Pauline line in `veil` form. ANF/CCEL editors historically inferred that Irenaeus “reads `κάλυμμα`”.

However, the apparatus-level data recommend a more careful formulation.

Do not write:

```text
IRENAEUS_POSSESSED_A_GREEK_1COR_MANUSCRIPT_WITH_KALYMMA = ESTABLISHED
```

What can be said:

```text
VALENTINIAN/PTOLEMY_TRADITION_REPORTED_BY_IRENAEUS_HAS_VEIL_FORM = EARLY_ATTESTED
IRENAEUS_LATIN_TRANSMISSION_HAS_VEIL_FORM = EARLY_PATRISTIC/VERSIONAL_EVIDENCE
RECONSTRUCTING_IRENAEUS_GREEK_NT_EXEMPLAR = HOLD
```

Possible causal explanations include:

- exegetical gloss;
- versional clarification;
- quotation adapted to the Valentinian interpretation;
- an early non-Greek transmission state;
- a Greek gloss no longer surviving in extant Greek NT manuscripts.

The current evidence does not require choosing one.

---

# 5. Patristic transmission is internally mixed

STEP’s apparatus lists some patristic traditions with occurrence counts on the `ἐξουσίαν` side and other occurrences on the `κάλυμμα` side (e.g. different occurrences/transmissions of Tertullian, Origen Latin, Chrysostom, Augustine).

That is a warning:

```text
A_FATHER_NAME_IN_APPARATUS != ONE_UNIFORM_TEXT_FORM_IN_ALL_CITATIONS
```

Patristic citation can be:

- free quotation;
- paraphrase;
- translator-mediated;
- manuscript-recension dependent;
- exegetically expanded.

Therefore patristic evidence is valuable for **early interpretation/transmission**, but less direct than an extant Greek biblical manuscript for reconstructing the Pauline text.

---

# 6. Why the gloss was attractive

The gloss is easy to explain historically even without assuming it was original:

```text
vv4–7 = repeated cover/uncover language
v10 = difficult ἐξουσία phrase
ancient interpreters commonly understand a head covering in the context
```

A clarifying `veil` term therefore removes an exegetical difficulty.

That direction of change is intrinsically plausible:

```text
DIFFICULT_EXOUSIA -> EXPLANATORY_VEIL
```

whereas replacing an obvious `veil` with cryptic `authority` across the entire surviving Greek manuscript tradition would require a much heavier transmission explanation.

This is an internal-textual argument, not manuscript proof by itself.

---

# 7. Implication for translation/exegesis

The textual result blocks a traditional shortcut:

```text
EXOUSIA_LEXICALLY_MEANS_VEIL = FALSE
```

The original/current Greek wording requires the interpreter to explain:

```text
ἐξουσίαν ἔχειν ἐπὶ τῆς κεφαλῆς
```

rather than replacing the noun with `veil` before exegesis begins.

A material covering may still be argued contextually, but:

```text
MATERIAL_COVERING_CONTEXT != EXOUSIA_TEXTUALLY_EQUALS_COVERING
```

Current grades remain:

```text
EXOUSIA_WOMAN_SUBJECT = A_SYNTAX
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH
EXOUSIA_EXACT_REFERENT = B_C
MATERIAL_COVERING = B_HIGH_LEADING
```

---

# 8. Updated textual no-overclaim rules

```text
KALYMMA_HAS_NO_LISTED_EXTANT_GREEK_MS_SUPPORT = TRUE
KALYMMA_HAS_EARLY_VERSIONAL/PATRISTIC_SUPPORT = TRUE
VERSIONAL/PATRISTIC_KALYMMA != ORIGINAL_GREEK_PROVED
IRENAEUS_VEIL_FORM != IRENAEUS_GREEK_EXEMPLAR_PROVED
PATRISTIC_FREE_QUOTATION != BIBLICAL_MANUSCRIPT
EXOUSIA != VEIL_LEXICALLY
```

---

# 9. Result

```text
CORE_GRADE_REVERSALS = 0
V10_GREEK_TEXT_EXOUSIAN = STRENGTHENED_TO_DIRECT_APPARATUS_CONTROL
KALYMMA = EARLY_GLOSS/VERSIONAL_PATRISTIC_ALTERNATIVE_NOT_GREEK_MS_RIVAL
IRENAEUS_GREEK_EXEMPLAR_KALYMMA = HOLD/UNPROVED
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
