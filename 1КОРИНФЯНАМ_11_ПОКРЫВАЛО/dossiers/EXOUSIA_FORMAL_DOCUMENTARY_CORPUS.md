# 1 Коринфянам 11:10 — `ἐξουσία` formal + documentary corpus

**Статус:** `EVERGREEN-CONTROLLING-DOSSIER / TEXTUAL-LEXICAL-DOCUMENTARY / SOURCE-ROUTES-PINNED / RESEARCH-ONLY / PUBLICATION-HOLD`  
**Последнее обновление:** 2026-08-10

## 0. Authority rule

This is the single evidence owner for the `ἐξουσία` node in 1 Cor 11:10.

It consolidates:

```text
GREEK_TEXT / KALYMMA_TRANSMISSION
FORMAL_EXOUSIA_EPI_TAXONOMY
FENDEL_DOCUMENTARY_CORPUS
FEMALE_DOCUMENTARY_RIGHT_BEARERS
BOUNDED_EXACT_HEAD_PARALLEL_SEARCH
ACQUISITION_HOLDS
```

Claim grades remain owned by the current claim registry.

```text
CLAIM_GRADE_OWNER = CURRENT_CLAIM_REGISTRY
THIS_DOSSIER = CONTROLLING_EVIDENCE_MAP_FOR_EXOUSIA
```

Future work updates this file; do not create another `V10 delta`, `female addendum`, `papyrology pass`, or current pointer for the same node.

---

# 1. Greek text and minimum syntax

1 Cor 11:10:

```text
διὰ τοῦτο ὀφείλει ἡ γυνὴ ἐξουσίαν ἔχειν ἐπὶ τῆς κεφαλῆς διὰ τοὺς ἀγγέλους
```

Minimum independent of theology:

```text
SUBJECT = ἡ γυνή
VERBAL_CONSTRUCTION = ἐξουσίαν ἔχειν
PP = ἐπὶ τῆς κεφαλῆς
EXOUSIA_WOMAN_SUBJECT = A_SYNTAX
```

This does not by itself solve the exact referent of `ἐξουσία`.

---

# 2. `ἐξουσίαν` vs `κάλυμμα` — textual transmission

## 2.1 Extant Greek manuscript control

STEP VarApp route:
- https://www.stepbible.org/?q=version%3DVarApp%40reference%3D1Cor.11

The listed extant Greek manuscript tradition, including P46 and major codices, supports `ἐξουσίαν`; the current apparatus route does not list an extant Greek NT manuscript with `κάλυμμα` as the rival reading.

```text
V10_GREEK_EXOUSIAN = OVERWHELMING_EXTANT_GREEK_MS_CONTROL
P46_EXOUSIAN = APPARATUS_ATTESTED
KALYMMA_AS_EXTANT_GREEK_MS_RIVAL = NOT_ESTABLISHED
```

## 2.2 Where `κάλυμμα` belongs

`κάλυμμα` appears in an early **versional / patristic / explanatory** stream, including Old Latin/Coptic/Armenian and Valentinian/Irenaean transmission categories in apparatus discussion.

```text
V10_KALYMMA = EARLY_VERSIONAL_PATRISTIC_GLOSS_OR_ALTERNATIVE_TRANSMISSION
V10_KALYMMA != EXTANT_GREEK_NT_MS_RIVAL
```

Independent peer-reviewed control:

Julie Newberry, *New Testament Studies*, Cambridge:
- https://www.cambridge.org/core/journals/new-testament-studies/article/abs/pauls-allusive-reasoning-in-1-corinthians-11712/EDE6D54A62D2265EA2C22291B6F2BA39

Newberry, citing Thiselton p.837, treats the textual support for `κάλυμμα` as weak and the form as an early gloss on `ἐξουσίαν`.

```text
KALYMMA_TEXTUAL_SUPPORT = WEAK_VERSIONAL_PATRISTIC
KALYMMA_AS_EARLY_GLOSS = STRONG_SCHOLARLY_TEXTUAL_ASSESSMENT
```

## 2.3 Irenaeus / Valentinian firewall

The veil-form in Valentinian/Ptolemaic material reported by Irenaeus is early reception/transmission evidence.

It does **not** establish:

```text
IRENAEUS_POSSESSED_GREEK_1COR_MS_WITH_KALYMMA = TRUE
```

Safe status:

```text
VALENTINIAN_PTOLEMY_VEIL_FORM = EARLY_ATTESTED_RECEPTION_TRANSMISSION
IRENAEUS_GREEK_EXEMPLAR_KALYMMA = UNPROVED
```

Possible mechanisms — gloss, free quotation, translation, explanatory adaptation, lost transmission state — remain open.

## 2.4 Exegetical implication

```text
EXOUSIA_LEXICALLY_MEANS_VEIL = FALSE
MATERIAL_COVERING_CONTEXT != EXOUSIA_TEXTUALLY_EQUALS_COVERING
```

A material-covering model may still be argued contextually; it must not replace the transmitted noun before exegesis begins.

---

# 3. Basic semantic direction of `ἐξουσίαν ἔχειν`

Independent lines converge:

1. woman is grammatical subject in v10;
2. Pauline/NT `ἐξουσία` normally describes right, power, capacity or domain;
3. Hooker/Fitzmyer emphasize active force;
4. documentary Greek recurrently uses `ἐξουσίαν ἔχω` as active possession of a right/power;
5. real female subjects are documentary bearers of such rights.

Current calibration:

```text
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH
EXOUSIA_EXACT_REFERENT = B_C
```

Strong active direction does **not** prove modern autonomy theology or one exact social reconstruction.

---

# 4. Formal taxonomy: `ἐξουσία` + `ἐπί`

Do not flatten semantically related biblical loci into identical syntax.

## A. Exact `ἔχω + ἐξουσία + ἐπί + genitive`

### Revelation 14:18

```text
ὁ ἔχων ἐξουσίαν ἐπὶ τοῦ πυρός
```

```text
REV_14_18 = EXACT_SUPPORT_VERB_PATTERN
SEMANTIC_DIRECTION = SUBJECT_HAS_AUTHORITY_OVER_DOMAIN
```

## B. Same lexemes/relation with fronted PP

### Revelation 20:6

```text
ἐπὶ τούτων ὁ δεύτερος θάνατος οὐκ ἔχει ἐξουσίαν
```

```text
REV_20_6 = EXACT_LEXEMES_AND_RELATION_DIFFERENT_WORD_ORDER
```

## C. `ἐξουσία + ἐπί + genitive`, different support verb

### Revelation 2:26

```text
δώσω αὐτῷ ἐξουσίαν ἐπὶ τῶν ἐθνῶν
```

### Daniel OG 3:97

```text
ἐξουσίαν δοὺς ἐφ’ ὅλης τῆς χώρας
```

```text
REV_2_26 = ACTIVE_AUTHORITY_OVER_DOMAIN_NOT_ECHO
DAN_OG_3_97 = LXX_SEMANTIC_PARALLEL_NOT_ECHO
```

## D. Different case

Luke 9:1 gives `ἐξουσίαν ἐπὶ πάντα τὰ δαιμόνια` with accusative.

## E. Related but not direct `ἐπί` complement

Sirach 17:2 `τῶν ἐπ’ αὐτῆς` is a genitive phrase meaning those/things on the earth, not a clean direct `ἐπί + genitive` complement to `ἐξουσία`.

### Formal conclusion

```text
AUTHORITY_OVER_DOMAIN_WITH_EXOUSIA = WELL_ATTESTED_BIBLICAL_GREEK
EXACT_ECHO_EPI_GEN = DIRECTLY_ATTESTED_REV_14_18
FRONTED_EQUIVALENT = REV_20_6
```

Blocked claims:

```text
EXOUSIA_EPI_GEN_HAS_NO_PARALLELS = FALSE
ALL_COMMONLY_LISTED_LOCI_ARE_EXACT_FORMAL_PARALLELS = FALSE
UNCOMMON = UNGRAMMATICAL = FALSE
SYNTAX_FORCES_PASSIVE_SIGN = FALSE
```

---

# 5. PKNT / Arzt-Grabner p.390

> Peter Arzt-Grabner et al., *1. Korinther*, Papyrologischer Kommentar zum Neuen Testament 2 (2006).

```text
PKNT2_BIBLIOGRAPHIC_EXISTENCE = VERIFIED_INSTITUTIONAL
PKNT_P390_DIRECT_PAGE_BYTES = HOLD
```

Jill Marshall page-specifically cites p.390 for the observation that `ἐξουσία` with `ἐπί + genitive` is **uncommon**.

Until p.390 is acquired:

```text
PKNT_UNCOMMON = PAPYROLOGICAL_OBSERVATION
PKNT_UNCOMMON != UNATTESTED_GREEK
PKNT_UNCOMMON != PASSIVE_EXOUSIA_PROOF
```

---

# 6. Fendel 2023 — systematic documentary corpus

## 6.1 Publication / dataset custody

Victoria Beatrix Fendel, “Support-Verb Constructions with Objects: Greek-Coptic Interference in the Documentary Papyri?” *Transactions of the Philological Society* 121.3 (2023): 382–403. DOI `10.1111/1467-968X.12279`.

Official routes:

- Wiley: https://onlinelibrary.wiley.com/doi/full/10.1111/1467-968X.12279
- Oxford ORA article: https://ora.ox.ac.uk/objects/uuid:26115075-f8bc-4d20-991d-f1a251b830cd
- Oxford dataset: https://ora.ox.ac.uk/objects/uuid:28406bed-423d-4801-9691-d5d7caa94e2a
- dataset DOI: `10.5287/ora-dqmbwrvj6`
- associated dataset file: `EXOUSIAN.xlsx`

## 6.2 Corpus scale

```text
DOCUMENTS_WITH_EXOUSIAN = 272
TOTAL_EXOUSIAN_TOKENS = 290
TOTAL_EXOUSIAN_ECHO = 190
```

Roman higher-register complement distribution:

```text
INFINITIVE = 105
ARTICULAR_INFINITIVE = 1
GENITIVE = 4
PREPOSITIONAL_PHRASE = 3
NO_OVERT_OBJECT = 2
LOST = 3
```

```text
EXOUSIAN_ECHEIN_ROMAN_DOCUMENTARY_GREEK = STRONGLY_ATTESTED
ACTIVE_RIGHT_POWER_POSSESSION = NORMAL_DOCUMENTARY_DIRECTION
```

## 6.3 PP boundary

The article confirms **three Roman higher-register PP complements** but does not enumerate the three prepositions in the published table/text.

The binary `EXOUSIAN.xlsx` remains the correct next acquisition target.

```text
FENDEL_ROMAN_PP_COUNT = 3_VERIFIED
FENDEL_ROMAN_PP_PREPOSITIONS = NOT_YET_ENUMERATED
FENDEL_ROMAN_PP_IS_EPI_GEN = NOT_ESTABLISHED
```

Never turn `PP=3` into `ἐπί/gen.=3` before reading the rows.

---

# 7. Real female documentary / epigraphic bearers

## 7.1 PSI X 1115 — Tephorsais, 28 Dec 152 CE

Direct documentary route:
- https://droitromain.univ-grenoble-alpes.fr/Negotia/PSI3_DDBDP.gr.html

Metadata:

```text
PSI_X_1115
TEBTYNIS_ARSINOITE
DATE = 152_12_28_CE
DOCUMENT = MARRIAGE_PROPERTY_CONTRACT
```

Core preserved legal sequence places control/ownership on Tephorsais’s side and includes:

```text
ἐξουσίαν ἔχειν οἰκονομεῖν περὶ αὐτοῦ
ὡς ἐὰν αἱρῆται
```

Safe result:

```text
TEPHORSAIS_FEMALE = A_DOCUMENT_CONTEXT
FEMALE_SIDE_PROPERTY_CONTROL = A_DOCUMENTARY
EXOUSIAN_ECHEIN_OIKONOMEIN = A_DOCUMENTARY
PERI_AUTOU_COMPLEMENT = A_DOCUMENTARY
CHOICE_LANGUAGE = A_DOCUMENTARY
```

Important:

```text
PSI_X_1115_PP = PERI_AUTOU
NOT EPI_GEN
```

Valid comparison: active female-side right/capacity.  
Invalid comparison: Paul’s exact head referent solved.

---

## 7.2 TAM II 603 — Lalla, Tlos

PHI:
- https://inscriptions.packhum.org/text/284492

Roman-period funerary inscription. Core:

```text
ἐπὶ τῷ ἔχειν ἐξουσίαν τὴν Λάλλαν ... ζῶσα συνχωρῆσαι
```

```text
LALLA = FEMALE_RIGHT_BEARER
RIGHT = GRANT_PERMISSION_WHILE_ALIVE
TAM_II_603_EXACT_DATE = HOLD_ROMAN_PERIOD_ONLY
```

Any bracketed restoration must remain visibly restored.

---

## 7.3 TAM II 604 — neighboring local formula

PHI:
- https://inscriptions.packhum.org/text/284493

```text
ἕτερος δὲ οὐδὲ εἷς ἕξει ἐξουσίαν
οὔτε συνχωρῆσαί τινι οὔτε ἐνθάψαι τινά
```

```text
TAM_II_604 = LOCAL_INDEPENDENT_ECHEIN_EXOUSIAN_RIGHT_TO_DO_X_CONTROL
```

This makes Lalla’s syntax locally unsurprising.

---

## 7.4 P.Wisc. I 13 — female will, 2nd century CE

Direct documentary route:
- https://droitromain.univ-grenoble-alpes.fr/Negotia/Wisc1_DDBDP.gr.html

The female testamentary formula includes a reconstructed statement of retaining full authority over her own property.

Critical firewall:

```text
FEMALE_TESTATOR = DOCUMENTARY_CONTEXT
EXOUSIA_FORMULA = EDITORIALLY_RESTORED_IN_RELEVANT_REGION
RESTORED_FORMULA != ALL_VISIBLE_PAPYRUS_LETTERS
```

Use as formulaic/editorial support, not unqualified letter-by-letter primary text.

---

## 7.5 P.Oxy. I 104 — Soeris, 26 Dec 96 CE

Direct documentary route:
- https://droitromain.univ-grenoble-alpes.fr/Negotia/Oxy3_DDBDP.gr.html

Female testator Soeris states in substance that she remains `κυρία` of her own property and may use/administer it as she chooses.

```text
P_OXY_I_104_DATE = 96_12_26_CE
FEMALE_PROPERTY_CONTROL = A_DOCUMENTARY
EXOUSIA_LEXEME_PRESENT = FALSE
USE_AS_EXOUSIA_LEXICAL_PARALLEL = FORBIDDEN
USE_AS_NEAR_SEMANTIC_FEMALE_RIGHT_CONTROL = VALID
```

---

# 8. Evidence-class ladder

Classify future parallels:

```text
A. EXACT_FORMAL
   same core lexemes + support verb + syntactic relation

B. FORMAL_NEAR
   same exousia-domain relation, different support verb/order/case

C. DOCUMENTARY_LEXICAL
   exousian echein in documentary/legal context

D. FEMALE_BEARER
   woman as real subject of exousia/right

E. SEMANTIC_NEAR
   similar control/right without exousia lexeme

F. RECONSTRUCTION
   proposed exact Corinthian social meaning
```

Do not promote C/D/E into A.

---

# 9. Fake P.Oxy. 84.5575 firewall

The quarantined agent citation invented an implausibly perfect parallel:

```text
woman + head covering + Roman custom + exousia + household control
```

Real evidence is distributed across separate sources.

```text
REAL_CORPUS > PERFECT_FABRICATED_PARALLEL
NO_EXACT_HEAD_PARALLEL_FOUND != LICENSE_TO_INVENT_ONE
CONSTRUCTION_LEVEL_PARALLEL = VALID_EVIDENCE
```

---

# 10. Bounded negative: exact extra-biblical head phrase

Current bounded search has not located a nonbiblical exact parallel:

```text
ἐξουσίαν ἔχειν ἐπὶ τῆς κεφαλῆς
```

```text
EXACT_NONBIBLICAL_HEAD_PARALLEL = NOT_FOUND_IN_BOUNDED_SEARCH
GLOBAL_NONEXISTENCE = NOT_CLAIMED
```

This is an acquisition result, not an argument that Paul’s Greek is ungrammatical.

---

# 11. What this corpus strengthens / does not solve

Strengthened:

```text
WOMAN_IS_SUBJECT = A
ACTIVE_RIGHT_POWER_SEMANTIC_PULL = B_HIGH
ACTIVE_AUTHORITY_OVER_DOMAIN_SYNTAX = ATTESTED
FEMALE_RIGHT_BEARERS_IN_ROMAN_DOCUMENTS = DIRECTLY_ATTESTED
```

Not solved:

```text
EXOUSIA_EXACT_REFERENT = B_C
```

Still-live contextual families include:

- control/right regarding head/head presentation;
- authority/right to pray/prophesy;
- authority/status signaled through covering/head presentation;
- contextual metonymic sign reading;
- other discourse-specific relations.

A passive sign interpretation requires contextual/metonymic argument; it is not the default lexical value of `ἐξουσίαν ἔχειν`.

---

# 12. No-overclaim rules

```text
KALYMMA_VERSIONAL_PATRISTIC != ORIGINAL_GREEK_PROVED
IRENAEUS_VEIL_FORM != IRENAEUS_GREEK_EXEMPLAR_PROVED
PATRISTIC_QUOTATION != BIBLICAL_MANUSCRIPT
FENDEL_CORPUS != 1COR11_COMMENTARY
FENDEL_PP_COUNT != EPI_GEN_COUNT
PSI_X_1115_FEMALE_EXOUSIA != PAULS_EXACT_REFERENT
P_WISC_I_13_RESTORED_FORMULA != ALL_SURVIVING_LETTERS
P_OXY_I_104_KYRIA != EXOUSIA_LEXICAL_EQUIVALENCE
ROMAN_EGYPT_PROPERTY_RIGHT != CORINTHIAN_LITURGICAL_RIGHT
FEMALE_LEGAL_AGENCY != MODERN_AUTONOMY_THEOLOGY
ACTIVE_SEMANTICS != EXACT_SOCIAL_TRIGGER_PROVED
```

---

# 13. Current acquisition queue

```text
P0 PKNT_2_2006_P390 + surrounding paragraph = DIRECT_PAGE_HOLD
P1 FENDEL_EXOUSIAN_XLSX = ACQUIRE_BINARY_AND_ENUMERATE_3_ROMAN_PP_ROWS
P1 SEARCH_NONBIBLICAL_EXACT_ECHO_EPI_GEN = CONTINUE
P1 P_WISC_I_13_EDITION_IMAGE_TEXT_APPARATUS = OPEN
P1 ADDITIONAL_FEMALE_ROMAN_RIGHT_BEARERS = ONLY_IF_HIGH_VALUE
```

Do not spend cycles looking for a cosmetically perfect head-covering parallel at the expense of corpus-quality evidence.

---

# 14. Result

```text
CORE_GRADE_REVERSALS = 0
V10_GREEK_TEXT_EXOUSIAN = STRONG_DIRECT_APPARATUS_CONTROL
KALYMMA = EARLY_VERSIONAL_PATRISTIC_GLOSS_STREAM
FENDEL_2023 = DIRECT_SYSTEMATIC_DOCUMENTARY_CORPUS
EXOUSIAN_ECHEIN_190_DOCUMENTARY_INSTANCES = DIRECT_CORPUS_RESULT
PSI_X_1115_AD152 = HIGH_VALUE_FEMALE_DOCUMENTARY_CONTROL
TAM_II_603_LALLA = A_EPIGRAPHIC_FEMALE_RIGHT_BEARER
TAM_II_604 = A_EPIGRAPHIC_LOCAL_RIGHT_FORMULA
P_WISC_I_13 = RESTORED_FORMULA_CONTROL
P_OXY_I_104_AD96 = NEAR_SEMANTIC_FEMALE_CONTROL_NOT_EXOUSIA
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH
EXOUSIA_EXACT_REFERENT = B_C
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```