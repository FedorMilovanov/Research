# 1 Коринфянам 11:2–16 — Susanna Drake 2026 author-interview / materiality control

**Дата:** 2026-08-10  
**Статус:** `DIRECT-AUTHOR-INTERVIEW / MATERIALITY / SOCIAL-MULTIVALENCE / SOURCE-TYPE-SEPARATION / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Source-type warning

This file records a **public author interview**, not the peer-reviewed/publisher chapter text.

Source:

- Susanna Drake interviewed by Michael Motia, New Books Network, 8 June 2026, on *Veiling in the Late Antique World*.
- NBN route: https://newbooksnetwork.com/veiling-in-the-late-antique-world
- A searchable transcript is surfaced by the syndicated podcast transcript route.

The interview is valuable because the author explains her own argument in detail, but it must not be cited as though it were verbatim content from Cambridge chapter 2.

```text
AUTHOR_INTERVIEW = DIRECT_AUTHOR_SELF_DESCRIPTION
AUTHOR_INTERVIEW != PEER_REVIEWED_BOOK_BODY
TRANSCRIPT_SUMMARY != PRINT_PAGE_LOCATOR
```

---

# 1. Important publication-date correction

New Books Network labels the interview/book as:

```text
Cambridge UP, 2026
```

but Cambridge University Press directly gives:

```text
ONLINE_PUBLICATION = 2025-11-26
PRINT_PUBLICATION = 2025-12-18
PRINT_PUBLICATION_YEAR = 2025
```

Therefore the controlling bibliographic year remains **2025**.

```text
NBN_2026_BOOK_LABEL = SECONDARY_METADATA_MISMATCH
CAMBRIDGE_2025 = CONTROLLING_PUBLISHER_DATE
```

This is another example of why freshness must be checked against publisher metadata even when the later platform is reputable.

---

# 2. Drake explicitly refuses certainty about the hidden Corinthian event

In the interview, Drake stresses that Paul is the only surviving voice from the Corinthian situation and questions whether we can even be sure there was a recognizable bilateral “debate” in the form modern reconstructions often assume.

Safe author-model statement:

```text
DRAKE_HIDDEN_CORINTH_DEBATE = EPISTEMICALLY_UNCERTAIN
DRAKE_PAUL_ONLY_SURVIVING_VOICE = AUTHOR_INTERVIEW_CONTROL
```

This is highly compatible with the project’s existing boundary:

```text
EXACT_CORINTH_TRIGGER = RECONSTRUCTION_LAYER
```

It does not prove that no conflict or resistant practice existed. It rejects confidence beyond the surviving evidence.

---

# 3. Drake’s description of Paul’s rhetorical project

In her interview-level explanation of 1 Cor 11, Drake describes Paul as attempting to **fix/stabilize the meaning** of women’s veiling within the argumentative framework he supplies.

She identifies in Paul’s discourse:

- a God/Christ/man/woman hierarchy;
- the assumption that women actually pray and prophesy in the assembly;
- honor/dishonor language surrounding covered/uncovered presentation;
- appeal to nature/custom;
- the unexplained angel clause.

She reads Paul as assigning veiling a place inside a gendered hierarchical system, but her own historical argument resists assuming that this Pauline rhetorical assignment exhausts what veiling/unveiling actually meant to women in Corinth.

```text
DRAKE_PAUL_FIXES_MEANING_OF_VEIL = DIRECT_AUTHOR_INTERVIEW_MODEL
DRAKE_PAULINE_HIERARCHICAL_FRAME = DIRECT_AUTHOR_INTERVIEW_MODEL
DRAKE_WOMEN_PRAY_AND_PROPHESY_ASSUMED = DIRECT_AUTHOR_INTERVIEW_MODEL
```

This is source-specific description, not automatic endorsement by the project.

---

# 4. The key historical warning: veiled != subordinated in every social event; unveiled != liberated

Drake’s central caution is against the modern binary:

```text
VEILED = SUBMISSION/OPPRESSION
UNVEILED = FREEDOM/RESISTANCE
```

Her historical model is deliberately multivalent.

In the interview she discusses veiling as potentially participating in:

- beauty/fashion;
- display of textiles and wealth/status;
- privacy and control of social access/gaze;
- piety/religious ritual;
- modesty/virtue;
- allure and the ambiguity of concealment/revelation;
- grief in some male contexts;
- ritual office in male contexts.

Therefore:

```text
VEILING_SEMANTICS = MULTIVALENT_CONTEXT_DEPENDENT
UNVEILING != AUTOMATIC_RESISTANCE
VEILING != AUTOMATIC_SUBMISSION
```

This strengthens the project’s rejection of monocausal hidden-event reconstructions without determining the exact Pauline instruction.

---

# 5. Material form: outer garment vs later separate veil

A particularly useful material-history distinction appears in Drake’s interview.

For earlier ancient Mediterranean contexts, including the first and second centuries CE, she describes head covering frequently as achieved by drawing part of an **outer garment** over the head.

She contrasts this with later antique visual evidence in which one increasingly finds shorter/separate/tighter head veils that contain the hair more completely.

Safe result:

```text
EARLY_IMPERIAL_HEAD_COVERING != NECESSARILY_SEPARATE_HAT_OR_SCARF
OUTER_GARMENT_DRAWN_OVER_HEAD = HISTORICALLY_NORMAL_FORM
LATE_ANTIQUE_SEPARATE_TIGHTER_VEILS = LATER_VISUAL_DEVELOPMENT_IN_DRAKE_MODEL
```

This matters for 1 Cor 11 because modern readers often import a modern discrete “headscarf” object into a text whose covering language does not name a modern garment type.

But:

```text
DRAKE_INTERVIEW_DOES_NOT_IDENTIFY_ONE_EXACT_CORINTHIAN_GARMENT = true
```

---

# 6. Men and women can both veil, with different meanings

Drake also stresses that ancient head covering was not an exclusively female practice.

She discusses male ritual head-covering, especially priestly/sacrificial contexts, while female coverings could simultaneously express other social meanings.

Her use of the Ara Pacis is methodologically useful: the same visual/ritual environment can show men and women covered without requiring that the covering communicate the **same** social proposition for each person.

This reinforces the project distinction:

```text
SAME_ARTIFACT_OR_GESTURE != SAME_SOCIAL_MEANING_ACROSS_GENDER/ROLE
ROMAN_MALE_CAPITE_VELATO_BACKGROUND = A
FEMALE_VEILING_SOCIAL_MEANING = MULTIPLE/CONTEXTUAL
```

It also warns against arguments that infer a single “veil code” from one object class.

---

# 7. Relation to current Corinth archaeology

Current local Corinth visual anchors remain:

- S-1116 Augustus `capite velato`, Julian Basilica;
- S-1088 veiled Julio-Claudian male, exact identity disputed.

Drake’s materiality model does **not** turn these objects into proof of the exact v4 trigger.

Rather, it helps explain why the project should preserve separate axes:

```text
OBJECT = REAL_LOCAL_VISUAL_PRACTICE
GESTURE = HEAD_COVERING
SOCIAL_MEANING = ROLE/CONTEXT_DEPENDENT
PAULINE_TRIGGER = EXEGETICAL_RECONSTRUCTION
```

---

# 8. Relation to female portraiture and funerary samples

The interview’s multivalence is consistent with the already acquired mixed visual record:

- Hughes early-imperial funerary sample contains both veiled and unveiled women;
- Stafford late-antique sample contains both;
- Olson warns against collapsing prescriptive literature and portrait representation;
- Plutarch and Valerius preserve contradictory literary anecdotes regarding female head covering.

Drake adds an important interpretive reason **why** mixed evidence should not be treated as noise:

> the same covering gesture can perform several social functions rather than one stable binary code.

Project-level result:

```text
MIXED_VISUAL_RECORD = EXPECTABLE_UNDER_MULTIVALENT_MODEL
MIXED_VISUAL_RECORD != EVIDENCE_THAT_VEILING_WAS_MEANINGLESS
```

---

# 9. Later Christian reception in Drake’s author explanation

The interview distinguishes first-century social multivalence from later Christian interpretive narrowing.

Drake describes later authors such as Ambrosiaster, Chrysostom and Jerome as increasingly making female veiling serve explicit gender-subordination/modesty discourse, while Pauline authority itself becomes part of that reception history.

This fits the project’s existing principle:

```text
LATER_PATRISTIC_NORMATIVE_VEILING != DIRECT_FIRST_CENTURY_BEHAVIORAL_CENSUS
```

and strengthens the need to avoid projecting fourth/fifth-century Christian prescriptions directly backwards into Roman Corinth.

---

# 10. Source calibration

Use Drake 2025/2026 in the following order:

```text
1. CAMBRIDGE_CHAPTER_METADATA/SUMMARY = DIRECT_PUBLISHER_CONTROL
2. DRAKE_AUTHOR_INTERVIEW = DIRECT_AUTHOR_SELF_DESCRIPTION
3. LATER_REVIEWS/PODCAST_SUMMARIES = SECONDARY
```

If chapter 2 pp.70–89 becomes directly accessible, its body supersedes interview-level reconstructions for page-specific claims.

Until then:

```text
DRAKE_CH2_EXACT_PAGES_FOR_SUBCLAIMS = HOLD
DRAKE_INTERVIEW_CLAIMS = AUTHOR_INTERVIEW_SAFE_WITHOUT_PRINT_LOCATOR
```

---

# 11. Effect on current grades

No core reversal.

```text
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
FEMALE_VEILING_SOCIAL_BACKGROUND = COMPLEX/MULTIVALENT
EXACT_CORINTH_TRIGGER = RECONSTRUCTION_LAYER
V4_EXACT_CAPITE_VELATO = B_C
CORE_GRADE_REVERSALS = 0
```

The important gain is historical calibration, not a forced new verse-by-verse conclusion.

---

# 12. New no-overclaim rules

```text
PAULS_VEIL_MEANING != TOTAL_SOCIAL_MEANING_OF_VEILING
VEILED_WOMAN != AUTOMATICALLY_SUBMISSIVE_WOMAN
UNVEILED_WOMAN != AUTOMATICALLY_LIBERATED/REBELLIOUS_WOMAN
FIRST_CENTURY_HEAD_COVERING != NECESSARILY_MODERN_HEADSCARF
MALE_AND_FEMALE_COVERING != SAME_SEMANTICS_AUTOMATICALLY
AUTHOR_INTERVIEW != BOOK_PAGE
NBN_2026_LABEL != CAMBRIDGE_PUBLICATION_YEAR
```

---

# 13. Result

```text
DRAKE_2025 = MAJOR_CURRENT_SPECIALIST_SOURCE
DRAKE_2026_INTERVIEW = DIRECT_AUTHOR_MODEL_CONTROL
DRAKE_HIDDEN_DEBATE_CONFIDENCE = LOW/OPEN
DRAKE_VEILING_MULTIVALENCE = STRONG_DIRECT_AUTHOR_SELF_DESCRIPTION
DRAKE_EARLY_OUTER_GARMENT_HEAD_COVERING = AUTHOR_MATERIALITY_CONTROL
DRAKE_LATER_SEPARATE_VEIL_SHIFT = AUTHOR_MATERIALITY_CONTROL
CAMBRIDGE_2025 > NBN_2026_BIBLIOGRAPHIC_LABEL
CORE_GRADE_REVERSALS = 0
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
