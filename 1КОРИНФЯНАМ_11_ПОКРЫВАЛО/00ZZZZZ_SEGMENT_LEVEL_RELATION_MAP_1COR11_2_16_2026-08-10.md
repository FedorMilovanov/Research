# 1 Коринфянам 11:2–16 — segment-level relation map

**Дата:** 2026-08-10  
**Последнее обновление:** 2026-08-14  
**Статус:** `SEMANTIC-RELATION-MAP / RESEARCH-ONLY / NOT-UI / PRODUCT-DATA-READY`  
**Назначение:** отделить прямые textual/syntactic relations от intertextual inference и historical reconstruction. Это исследовательская карта аргумента, а не визуальный дизайн.

## 1. Типы связей

```text
DIRECT_SYNTAX       = связь маркирована грамматикой/коннектором текста
DIRECT_SEMANTIC     = связь необходима по непосредственному смыслу фразы
DIRECT_DISCOURSE    = связь следует из локальной риторической/дискурсивной структуры
DIRECT_THEOLOGICAL  = теологическое утверждение прямо выражено самим текстом
INTERTEXT_STRONG    = ясная/широко признанная связь с Писанием
INTERTEXT_PROPOSED  = академически предложенный echo/allusion, но не explicit quotation
EXEGETICAL_B        = leading interpretive relation
EXEGETICAL_C        = serious competing relation
HISTORICAL_B_C      = plausible exact historical identification, but reconstruction remains material
HISTORICAL_D_C      = published low-confidence historical reconstruction
HISTORICAL_D        = edge/history-only reconstruction
NEGATIVE_BOUNDARY   = связь, которую нельзя рисовать как установленную
```

Confidence grades inside node-calibration blocks remain controlled by `CURRENT_CLAIM_REGISTRY`; relation type and claim grade are separate dimensions.

---

## 2. Узлы

| ID | Стих | Ключевой сегмент | Research function |
|---|---:|---|---|
| V02A | 2 | `Ἐπαινῶ ...` | praise frame |
| V02B | 2 | `τὰς παραδόσεις κατέχετε` | apostolic tradition frame |
| V03A | 3 | Christ → man as `κεφαλή` | head relation 1 |
| V03B | 3 | man → woman as `κεφαλή` | head relation 2 |
| V03C | 3 | God → Christ as `κεφαλή` | head relation 3 |
| V04A | 4 | man praying/prophesying | male worship action |
| V04B | 4 | `κατὰ κεφαλῆς ἔχων` | male head-state crux |
| V04C | 4 | dishonours his head | shame consequence |
| V05A | 5 | woman praying/prophesying | female worship action |
| V05B | 5 | `ἀκατακαλύπτῳ τῇ κεφαλῇ` | female uncovered crux |
| V05C | 5 | dishonours her head | shame consequence |
| V05D | 5 | same as shaven | analogy/intensification |
| V06A | 6 | if not covered → let her be shorn | reductio/conditional |
| V06B | 6 | if shorn/shaved shameful | shared propriety premise |
| V06C | 6 | let her be covered | conclusion |
| V07A | 7 | man ought not cover | male conclusion |
| V07B | 7 | image + glory of God | theological rationale |
| V07C | 7 | woman glory of man | relational rationale |
| V08A | 8 | woman from man | Genesis-origin rationale |
| V09A | 9 | woman because of/for man | Genesis-purpose rationale |
| V10A | 10 | `διὰ τοῦτο` | inferential connector |
| V10B | 10 | woman ought to have `ἐξουσία` on/over head | authority crux |
| V10C | 10 | `διὰ τοὺς ἀγγέλους` | angel rationale crux |
| V11A | 11 | `πλὴν` | qualification/counterbalance |
| V11B | 11 | neither woman without man | interdependence 1 |
| V11C | 11 | nor man without woman | interdependence 2 |
| V11D | 11 | `ἐν κυρίῳ` | christological/ecclesial frame |
| V12A | 12 | woman from man | first-creation origin |
| V12B | 12 | man through woman | generational counter-direction |
| V12C | 12 | all from God | ultimate-source closure |
| V13A | 13 | judge among yourselves | audience discernment |
| V13B | 13 | propriety of uncovered female prayer | local propriety question |
| V14A | 14 | `ἡ φύσις αὐτή` teaches | nature appeal |
| V14B | 14 | man long-haired → dishonour | male hair analogy |
| V15A | 15 | woman long-haired → glory | female hair analogy |
| V15B | 15 | hair given `ἀντὶ περιβολαίου` | natural-covering analogy crux |
| V16A | 16 | contentious person | dispute closure |
| V16B | 16 | `τοιαύτην συνήθειαν` | custom referent crux |
| V16C | 16 | we + churches of God | trans-local church appeal |

---

## 3. Direct argument edges

| From | To | Type | Почему |
|---|---|---|---|
| V02A | V02B | DIRECT_SYNTAX | praise specified by remembrance/traditions |
| V03A/V03B/V03C | V04A–V05C | EXEGETICAL_B | v.3 introduces `head` wordplay/rationale for head conduct; exact semantic content of `κεφαλή` disputed |
| V04B | V04C | DIRECT_SYNTAX | participial head-state → dishonour |
| V05B | V05C | DIRECT_SYNTAX | uncovered state → dishonour |
| V05B | V05D | DIRECT_SYNTAX | `γάρ`: uncovered equated rhetorically with shaven state |
| V05D | V06A | DIRECT_SYNTAX | `γάρ`: conditional reductio continues comparison |
| V06A/V06B | V06C | DIRECT_SYNTAX | if shameful to shear/shave → cover |
| V07A | V07B/V07C | DIRECT_SYNTAX | `γάρ`: theological rationale for male/female distinction |
| V07C | V08A | DIRECT_SYNTAX | `γάρ`: explains woman as man's glory via origin |
| V08A | V09A | DIRECT_SYNTAX | `καὶ γάρ`: adds purpose/creation rationale |
| V08A/V09A | V10A | DIRECT_SYNTAX | `διὰ τοῦτο`: v.10 explicitly derives from preceding reasoning |
| V10A | V10B | DIRECT_SYNTAX | inferential conclusion: woman ought to have exousia |
| V10B | V10C | DIRECT_SYNTAX | `διὰ`: angels supplied as reason/rationale |
| V10B/V10C | V11A | DIRECT_SYNTAX | `πλὴν`: qualifying/counterbalancing move |
| V11A | V11B/V11C | DIRECT_SYNTAX | neither/nor pair defines qualification |
| V11B/V11C | V11D | DIRECT_SEMANTIC | mutuality specifically `in the Lord` |
| V11B/V11C | V12A/V12B | DIRECT_SYNTAX | `ὥσπερ ... οὕτως`: analogy explains mutuality |
| V12A/V12B | V12C | DIRECT_SYNTAX | `δέ`: ultimate source in God closes comparison |
| V13A | V13B | DIRECT_SYNTAX | command to judge introduces propriety question |
| V13B | V14A | DIRECT_SYNTAX | `οὐδὲ`: nature appeal adds support to judgment |
| V14A | V14B/V15A | DIRECT_SYNTAX | nature teaching expressed by male/female hair contrast |
| V15A | V15B | DIRECT_SYNTAX | `ὅτι`: glory claim grounded in hair-as-covering relation |
| V13B–V15B | V16A/V16B/V16C | DIRECT_DISCOURSE | v.16 closes dispute by appeal to shared practice; exact referent of `such custom` disputed |

---

## 4. Strong intertextual edges

| From | Target | Type | Calibration |
|---|---|---|---|
| V07B | Gen 1:26–27 | INTERTEXT_STRONG | image language |
| V08A | Gen 2:21–23 | INTERTEXT_STRONG | woman from man |
| V09A | Gen 2:18–23 | INTERTEXT_STRONG | woman created in relation to man/helper context |
| V12A | Gen 2:23 | INTERTEXT_STRONG | woman from man repeated |
| V12B | ordinary birth / Gen creation reversal in lived generation | DIRECT_SEMANTIC | men now come through women |
| V12C | God as ultimate source | DIRECT_THEOLOGICAL | explicit statement, not merely intertext |

---

## 5. Proposed intertextual edges — do not render as direct fact

| From | Target | Type | Status |
|---|---|---|---|
| V07C–V12C | 1 Esdras 4:13–41 | INTERTEXT_PROPOSED | Julie Newberry: cumulative echo; useful B/C proposal, not explicit citation |
| V10C | Qumran sacred-assembly angelology | INTERTEXT_PROPOSED | strong Second-Temple/heavenly-assembly background; supports `HEAVENLY_HOLY_ANGELS_REFERENT = B_HIGH_LEADING`, but does not identify Paul's exact angelic function |
| V10C | Gen 6 / Watchers tradition | INTERTEXT_PROPOSED | ancient Tertullian line; `WATCHERS = C_SERIOUS_ALTERNATIVE` |
| V10B/V10C | 1 Cor 6:2–3 judging angels | INTERTEXT_PROPOSED | modern internal-Pauline proposal; possible, not explicit |

---

## 6. Historical reconstruction edges

| Text node | Historical proposal | Type | Rule |
|---|---|---|---|
| V04B | Roman male `capite velato` ritual/status | HISTORICAL_B_C | `ROMAN_CAPITE_VELATO_BACKGROUND = A`; exact identification of v4 with this ritual = `B_C`; exact Corinthian trigger remains reconstruction |
| V04B | Judaizing male prayer covering | HISTORICAL_D_C | record, do not promote |
| V05B/V06A | female veil as matronly/modesty/status marker | HISTORICAL_B_C | contextual status significance is serious; no one universal female veil law or exact local trigger is proved |
| V05A/V08A/V12A–B | free(d)-married-wives as primary practical scope | HISTORICAL_B_C | Callon/Massey provide a serious marital/status reconstruction, but practical all-women scope is now B-leading in the current registry and v12 resists one rigid wife/husband gloss |
| V05D/V06B | shaved woman = prostitute/adulteress | NEGATIVE_BOUNDARY | do not universalize; evidence insufficient for blanket equation |
| V14B | long male hair = specific homosexual role | HISTORICAL_D | Murphy-O'Connor/MacGregor edge model |
| V05B/V14–15 | loose hair = Dionysiac/ecstatic cult | HISTORICAL_D | possible reconstruction, not demonstrated local trigger |
| V10C | angels = bishops | HISTORICAL_D | Ambrosiaster reception, not Pauline lexical fact |
| V10C | angels = human church messengers | HISTORICAL_D_C | Murphy-O'Connor; possible semantic use of `angelos`, weak contextually |

---

## 7. Contested semantic nodes

### `κεφαλή` V03

```text
HEADSHIP/AUTHORITY/PREDOMINANCE -> B_LEADING
SOURCE/ORIGIN ONLY              -> C_VIABLE
PROMINENCE                      -> C/B depending formulation
ONE_FIXED_LEXICAL_GLOSS         -> prohibited
```

### practical scope — `ἀνήρ / γυνή`

```text
ALL_WOMEN / SEX_CLASS PRACTICAL SCOPE -> B_LEADING
FREE_D_MARRIED_WIVES_PRIMARY_SCOPE    -> C_SERIOUS_CURRENT_ALTERNATIVE
V12_RIGID_WIFE_HUSBAND_GLOSS          -> contextually awkward
EVERY_TOKEN_UNAMBIGUOUSLY_NON_MARITAL -> prohibited overclaim
```

Machine boundary:

```text
ALL_WOMEN_SCOPE_B_LEADING != EVERY_GYNE_TOKEN_CANNOT_MEAN_WIFE
ALL_WOMEN_SCOPE_B_LEADING != PETERS_WHOLE_MODEL_ADOPTED
```

### covering language V04–V06/V13

```text
TEXTILE/MATERIAL_COVERING -> B_HIGH_LEADING
HAIR/HAIRSTYLE_ONLY       -> C_SERIOUS_ALTERNATIVE
EXACT_MODERN_GARMENT_FORM -> HOLD / not reconstructable at A
```

### `ἐξουσία` V10

```text
WOMAN = GRAMMATICAL_SUBJECT            -> A_SYNTAX
AUTHORITY/RIGHT/POWER_SEMANTIC_CLASS   -> A_B_HIGH
ACTIVE_WOMAN_BEARER_PULL               -> B_HIGH
EXACT_REFERENT                         -> B_C
SIGN_OF_HUSBAND'S_AUTHORITY_PARAPHRASE -> C_WITH_EXTRA_SEMANTIC_STEPS
LEXICALLY = VEIL                       -> prohibited
```

Construction-level relation split owned by `dossiers/EXOUSIA_FORMAL_DOCUMENTARY_CORPUS.md`:

```text
EXOUSIA + EPI + DOMAIN                 -> well-attested Greek construction
V10 HEAD/HEAD-STATE AS CONTROL DOMAIN  -> EXEGETICAL_B relation
V10 HEAD-WORN METONYMIC/SIGN LOCATION  -> EXEGETICAL_C serious counterrelation
EXACT_SOCIAL_REALIZATION               -> remains B_C claim-level question
```

This relation preference is grounded in same-letter/NT support-verb usage, exact biblical `ἐξουσία + ἐπί + genitive` authority-over-domain parallels and the documentary corpus. It does **not** convert one contextual model into A-level syntax. Romerowski/Wang preserve real locative/metonymic countermodels; Delobel/Murphy-O'Connor, Wu, Callon and related active-control readings preserve the competing control-domain family.

Machine boundaries:

```text
ACTIVE_WOMAN_BEARER_PULL != EXACT_OWN_HEAD_OR_MINISTRY_REFERENT_PROVED
CONTROL_DOMAIN_RELATION_PREFERRED != EXACT_SOCIAL_REALIZATION_PROVED
HEAD-WORN_SYMBOL_READING != EXOUSIA_LEXICALLY_MEANS_SIGN
```

### `angels` V10

```text
ANGELS_INVOKED                               -> A_TEXT
HEAVENLY_HOLY_ANGELS_REFERENT               -> B_HIGH_LEADING
ANGELS_AS_COSMIC_WITNESSES_PRESENT_ASSEMBLY -> B_LEADING
EXACT_ANGELIC_FUNCTION                      -> B_C
WATCHERS/FALLEN                             -> C_SERIOUS_ALTERNATIVE
GUARDIAN_ANGELS                             -> C_LOW
HUMAN_MESSENGERS                            -> D_C_LOW
BISHOPS_CLERGY                              -> D_C_LOW_RECEPTION
CERTAIN_IDENTITY_OR_FUNCTION                -> prohibited
```

### `φύσις` V14

```text
V14_15_EVALUATIVE_SEX_CODE          -> A_TEXT
PHYSIS_SEXED_NATURALIZED_PROPRIETY  -> B_HIGH_LEADING
EXACT_BIOLOGY_CULTURE_MIX           -> B_C
PURE_BIOLOGY_ONLY                   -> rejected
PURE_ARBITRARY_CUSTOM_ONLY          -> rejected
```

### `τοιαύτην συνήθειαν` V16

```text
TRANS_LOCAL_CHURCH_PRACTICE_APPEAL       -> A_TEXT
V16_ECCLESIAL_EXHORTATIVE_NORMATIVE_FORCE -> B_HIGH
V16_NO_CONTRARY_ALTERNATIVE_PRACTICE     -> B_LEADING
EXACT_REFERENT                            -> B_C
CANCELS_VV2_15                            -> D_C_LOW
```

Machine boundaries:

```text
V16_NORMATIVE_FORCE != FORMAL_COMMAND_AS_SUCH
TRANS_LOCAL_PRACTICE != IDENTICAL_TIMELESS_GARMENT_ARTIFACT
REJECT_CANCELLATION_READING != EXACT_CUSTOM_ANTECEDENT_SOLVED
```

---

## 8. Macro-argument graph in Research terms

```text
TRADITION FRAME (v2)
    ↓
HEAD RELATIONS (v3)
    ↓ interpretive bridge B
HEAD CONDUCT IN PRAYER/PROPHECY (vv4-6)
    ↓ γάρ
IMAGE / GLORY (v7)
    ↓ γάρ / καὶ γάρ
GENESIS ORIGIN + PURPOSE (vv8-9)
    ↓ διὰ τοῦτο
EXOUSIA + ANGELS (v10)
    ↓ πλὴν
MUTUALITY IN LORD (v11)
    ↓ ὥσπερ...οὕτως
WOMAN FROM MAN / MAN THROUGH WOMAN / ALL FROM GOD (v12)
    ↓
AUDIENCE PROPRIETY JUDGMENT (v13)
    ↓ οὐδὲ
NATURE / HAIR ANALOGY (vv14-15)
    ↓
TRANS-LOCAL CHURCH PRACTICE CLOSURE (v16)
```

**Critical warnings:**

```text
HEAD_RELATIONS -> EXACT_GARMENT_MEANING = NOT_DIRECT_SYNTAX
ROMAN_CAPITE_VELATO -> V4_EXACT_PROBLEM = HISTORICAL_B_C, while the background fact itself is A
QUMRAN_ANGELIC_ASSEMBLY -> PAULS_EXACT_ANGEL_FUNCTION = NOT_DIRECT_IDENTITY
ACTIVE_EXOUSIA_SEMANTICS -> ONE_EXACT_SOCIAL_REFERENT = INVALID_SHORTCUT
ALL_WOMEN_SCOPE -> EVERY_TOKEN_NON_MARITAL = INVALID_SHORTCUT
V16_ECCLESIAL_NORM -> FORMAL_IDENTICAL_GARMENT_COMMAND = INVALID_SHORTCUT
```

---

## 9. Product handoff boundary

Эта карта может позднее стать semantic graph для интерактивной матрицы, но Research не определяет:

- layout;
- animation;
- colors;
- modal behavior;
- front-end component structure.

Research определяет только **nodes, relation types, confidence and negative boundaries**.

```text
PRODUCT_WRITE = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
CURRENT_CLAIM_REGISTRY = CONTROLLING_FOR_GRADES
THIS_MAP = MACHINE_FACING_RELATION_LAYER_NOT_GRADE_AUTHORITY
```
