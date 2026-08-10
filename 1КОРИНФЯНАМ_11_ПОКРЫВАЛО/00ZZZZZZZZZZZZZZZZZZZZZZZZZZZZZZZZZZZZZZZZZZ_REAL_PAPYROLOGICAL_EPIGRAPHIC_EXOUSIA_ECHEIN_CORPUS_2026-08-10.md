# 1 Коринфянам 11:10 — real papyrological / epigraphic `ἐξουσίαν ἔχειν` corpus

**Дата:** 2026-08-10  
**Статус:** `DIRECT-CORPUS / DOCUMENTARY-PAPYRI / ROMAN-EPIGRAPHY / EXOUSIA-SYNTAX / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Purpose

После карантина выдуманного `P.Oxy. 84.5575` нужен положительный ответ на вопрос:

> Что **реальная** документальная греческая база говорит о конструкции `ἐξουσίαν ἔχειν`?

Этот слой не ищет красивого совпадения со словами «голова / покрытие». Он проверяет реальную синтаксико-семантическую конструкцию в папирусах и надписях.

```text
REAL_CORPUS > PERFECT_BUT_FABRICATED_PARALLEL
ACTIVE_RIGHT_CONSTRUCTION != EXACT_1COR11_REFERENT_SOLVED
LEGAL_DOCUMENT != LITURGICAL_CONTEXT
```

---

# 1. Victoria Beatrix Fendel 2023 — systematic documentary-papyrus corpus

## 1.1 Direct publication and dataset

Direct Wiley article:

> Victoria Beatrix Fendel, “Support-Verb Constructions with Objects: Greek-Coptic Interference in the Documentary Papyri?” *Transactions of the Philological Society* 121.3 (2023): 382–403. DOI `10.1111/1467-968X.12279`.

Official routes:

- Wiley: https://onlinelibrary.wiley.com/doi/full/10.1111/1467-968X.12279
- Oxford University Research Archive article record: https://ora.ox.ac.uk/objects/uuid:26115075-f8bc-4d20-991d-f1a251b830cd
- underlying Oxford dataset: https://ora.ox.ac.uk/objects/uuid:28406bed-423d-4801-9691-d5d7caa94e2a
- dataset DOI: `10.5287/ora-dqmbwrvj6`

ORA exposes an `EXOUSIAN.xlsx` dataset (51.7 KB) associated with the article.

The article is open access under CC BY-NC-ND (ORA rights record).

---

# 2. Corpus scale — `ἐξουσίαν ἔχω` is not an exotic construction

Fendel searched `ἐξουσίαν` in the Duke Database of Documentary Papyri in February 2023.

Direct article results:

```text
DOCUMENTS_WITH_EXOUSIAN = 272
TOTAL_EXOUSIAN_TOKENS = 290
TOTAL_EXOUSIAN_ECHO = 190
```

By period/register her table gives:

```text
PTOLEMAIC_GREEK_300_0_BCE:
  higher register exousian echo = 9
  lower register = 1

ROMAN_GREEK_0_400_CE:
  higher register = 118 + 5 classified transitional/related
  lower register = 9

ROMAN/EARLY_BYZANTINE_TRANSITION:
  higher register = 5

EARLY_BYZANTINE_400_650:
  higher register = 41
  lower register = 7
```

The exact table total is 190 constructions.

The dominant Roman-period genre is **higher-register documentary Greek**:

- contracts;
- agreements;
- sales;
- wills and related legal/administrative documents.

Therefore:

```text
EXOUSIAN_ECHEIN_DOCUMENTARY_GREEK = ESTABLISHED_RECURRENT_CONSTRUCTION
EXOUSIAN_ECHEIN_ROMAN_PERIOD = STRONGLY_ATTESTED
EXOUSIAN_ECHEIN_AS_ACTIVE_RIGHT/POWER = NORMAL_DOCUMENTARY_SEMANTICS
```

This is independent of Pauline theology.

---

# 3. What complements `ἐξουσίαν ἔχειν` in Roman documentary Greek

Fendel’s Roman-period table is particularly valuable for the grammar of the construction.

For Roman Greek higher-register examples she records approximately:

```text
INF = 105
ARTICULAR_INFINITIVE = 1
GENITIVE = 4
PREPOSITIONAL_PHRASE = 3
NO_OVERT_OBJECT = 2
LOST = 3
```

For Roman lower-register examples:

```text
GENITIVE = 6
INFINITIVE = 2
NO_OVERT_OBJECT = 1
```

She explicitly observes that **genitival objects occur across registers**, while accusative direct objects do not appear before the early Byzantine period in her corpus.

Safe implication:

```text
ROMAN_EXOUSIAN_ECHEIN_PLUS_INFINITIVE = VERY_NORMAL
ROMAN_EXOUSIAN_ECHEIN_PLUS_GENITIVE = NORMAL_ATTESTED
ROMAN_EXOUSIAN_ECHEIN_PLUS_PP = ATTESTED
ROMAN_EXOUSIAN_ECHEIN_PLUS_ACCUSATIVE_OBJECT = NOT_FOUND_IN_FENDEL_ROMAN_SAMPLE
```

This does not mechanically parse Paul’s `ἐπὶ τῆς κεφαλῆς`; it shows that a PP/genitival complement with an active `have authority/right` construction is entirely at home in postclassical documentary syntax.

---

# 4. Direct documentary semantic examples

Fendel gives representative formulae such as:

```text
ἐξουσίαν ἔχειν διοικεῖν / χρᾶσθαι καὶ οἰκονομεῖν
```

= to have the power/right to farm/use/manage.

She also quotes testamentary/legal wording such as:

```text
ἔχειν με τὴν τῶν ἰδίων ἐξουσίαν
ὃ ἐὰν βούλωμαι ἐπιτελεῖν καὶ μεταδιατίθεσθαι
```

in which the subject has authority/power over his own property to do/arrange what he wishes.

The semantic direction is consistently:

```text
SUBJECT -> POSSESSES/EXERCISES RIGHT OR POWER
```

not:

```text
SUBJECT -> PASSIVELY BEARS A SYMBOL OF SOMEONE ELSE'S AUTHORITY
```

This does not rule out a contextual/metonymic sign interpretation in 1 Cor 11:10, but it confirms that such a passive-sign interpretation requires **extra contextual semantic steps** rather than arising from the construction itself.

---

# 5. Real female-subject epigraphic control — TAM II 603, Tlos

## 5.1 Direct inscription

PHI Greek Inscriptions:

- https://inscriptions.packhum.org/text/284492

Citation:

```text
TAM II 603
Lycia, western — Tlos
Roman period
```

The funerary inscription concerns a tomb constructed by Hoples for himself, his daughter Lalla, and her descendants, with later permissions concerning burial couches.

The crucial lines 18–23 include:

```text
ἐπὶ τῷ μὴ ἔχειν τινὰ ἐξουσίαν ...
...
ἐπὶ τῷ ἔχειν ἐξουσίαν τὴν Λάλλαν
[ᾧ ἂν βούλητα]ι ζῶσα συνχωρῆσαι
```

Direct minimum:

```text
LALLA = GRAMMATICAL SUBJECT/BEARER OF EXOUSIAN ECHEIN
LALLA_IS_FEMALE = A_TEXT_CONTEXT
LALLA_HAS_AUTHORITY/RIGHT_WHILE_ALIVE_TO_GRANT_PERMISSION = A_EPIGRAPHIC
```

The restoration `[ᾧ ἂν βούληται]` is editorially bracketed and must remain marked as restored.

The uncontested core does not depend on every restored letter:

```text
ἐπὶ τῷ ἔχειν ἐξουσίαν τὴν Λάλλαν ... ζῶσα συνχωρῆσαι
```

plainly gives Lalla the legal authority/right to grant permission while living.

## 5.2 Context

This is funerary property/burial authorization, not worship or personal bodily autonomy.

Therefore the valid comparison is **construction-level**:

```text
FEMALE_SUBJECT + EXOUSIAN_ECHEIN + RIGHT_TO_AUTHORIZE_ACTION
```

Not:

```text
TLOS_LALLA = DIRECT_PARALLEL_TO_HEAD_COVERING
TLOS_LALLA_PROVES_WOMAN_CONTROLS_HER_HEAD_IN_1COR11
```

---

# 6. Neighboring Tlos control — TAM II 604

PHI TAM II 604, also from Tlos and explicitly labelled Roman Imperial period, gives a neighboring funerary rule:

```text
ἕτερος δὲ οὐδὲ εἷς ἕξει ἐξουσίαν
οὔτε συνχωρῆσαί τινι οὔτε ἐνθάψαι τινά
```

= no other person shall have authority/right either to grant permission to someone or to bury anyone.

Route:

- https://inscriptions.packhum.org/text/284493

This independently confirms the same local funerary/legal idiom:

```text
ECHEIN_EXOUSIAN + INFINITIVE = RIGHT/AUTHORITY_TO_DO_X
```

Thus TAM II 603’s Lalla clause is not an isolated bizarre usage.

---

# 7. What this does to the fake P.Oxy. 5575 episode

The fabricated agent claim invented an almost impossibly perfect parallel:

```text
woman
+ Roman custom
+ head covering
+ exousia
+ household control
```

Real documentary evidence is less sensational but methodologically stronger.

We now have:

```text
FENDEL_2023 = LARGE_REAL_PAPYRUS_CORPUS
TAM_II_603 = REAL_ROMAN_PERIOD_FEMALE_EXOUSIA_BEARER
TAM_II_604 = REAL_LOCAL_PARALLEL_FORMULA
```

Therefore future agents should never compensate for the absence of a perfect lexical parallel by inventing one.

New rule:

```text
NO_DIRECT_HEAD_PARALLEL_FOUND != LICENSE_TO_INVENT_HEAD_PARALLEL
CONSTRUCTION_LEVEL_PARALLEL_IS_VALID_EVIDENCE
```

---

# 8. Relation to Hooker / Fitzmyer / Pauline same-letter controls

Before this pass, the active reading already had several independent lines:

- woman is grammatical subject in 1 Cor 11:10;
- Pauline `ἐξουσία` usages are active right/power/capacity usages;
- Hooker’s Cambridge apparatus explicitly emphasizes active semantic force;
- Fitzmyer likewise adduces active NT usage.

Fendel and Tlos add **nonbiblical documentary/epigraphic** controls.

Thus the active-bearer result no longer depends on either egalitarian theology or a small literary corpus.

Current grade remains, now with stronger provenance:

```text
EXOUSIA_WOMAN_SUBJECT = A_SYNTAX
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH
EXOUSIA_EXACT_REFERENT = B_C
```

No promotion to A for exact meaning, because the documentary parallels do not tell us what the authority in v10 is **over/for** in the specific Pauline discourse.

---

# 9. What remains unresolved in v10

The real corpus helps with semantic direction but leaves the central referent question open.

Still live possibilities include:

- woman’s right/control regarding her own head;
- authority/right to pray/prophesy;
- authority-related status expressed via a covering;
- metonymic/sign reading requiring contextual supplementation;
- other contextually argued referents.

The construction itself strongly resists only the shortcut:

```text
EXOUSIA = VEIL/SYMBOL_OF_HUSBANDS_AUTHORITY_LEXICALLY
```

which is already rejected by the current project.

---

# 10. Dating boundary for TAM II 603

PHI labels TAM II 603 only:

```text
Roman period
```

This pass did not close a more precise year/century from a direct specialist dating source.

Therefore:

```text
TAM_II_603 = ROMAN_PERIOD
TAM_II_603_EXACT_DATE = HOLD
TAM_II_603_IS_STRICTLY_CONTEMPORARY_WITH_PAUL = NOT_CLAIMED
```

This is sufficient for a Roman-era constructional parallel but not for a “same decade” argument.

---

# 11. New no-overclaim controls

```text
FENDEL_CORPUS != 1COR11_COMMENTARY
DOCUMENTARY_LEGAL_EXOUSIA != EXACT_LITURGICAL_REFERENT
TAM_II_603_LALLA != HEAD_COVERING_PARALLEL
TAM_II_603_BRACKETED_RESTORATION != INSCRIBED_CERTAINTY
ROMAN_PERIOD != EXACT_PAULINE_DATE
ACTIVE_CONSTRUCTIONAL_PARALLEL != WOMANS_AUTONOMY_THEOLOGY_PROVED
```

---

# 12. Result

```text
CORE_GRADE_REVERSALS = 0
FENDEL_2023_EXOUSIAN_ECHEIN_CORPUS = DIRECT_SYSTEMATIC_CONTROL
EXOUSIAN_ECHEIN_190_DOCUMENTARY_INSTANCES = DIRECT_CORPUS_RESULT
ROMAN_DOCUMENTARY_EXOUSIAN_ECHEIN = STRONGLY_ATTESTED_ACTIVE_RIGHT/POWER_CONSTRUCTION
TAM_II_603_LALLA_FEMALE_ACTIVE_EXOUSIA = A_EPIGRAPHIC
TAM_II_604_LOCAL_RIGHT_TO_AUTHORIZE_FORMULA = A_EPIGRAPHIC
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH_STRENGTHENED_PROVENANCE
EXOUSIA_EXACT_REFERENT = B_C_UNCHANGED
FAKE_POXY_5575 = REMAINS_REJECTED
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
