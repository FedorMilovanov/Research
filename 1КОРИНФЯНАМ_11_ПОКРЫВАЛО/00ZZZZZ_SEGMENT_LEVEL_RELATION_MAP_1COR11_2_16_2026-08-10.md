# 1 Коринфянам 11:2–16 — segment-level relation map

**Дата:** 2026-08-10  
**Статус:** `SEMANTIC-RELATION-MAP / RESEARCH-ONLY / NOT-UI / PRODUCT-DATA-READY`  
**Назначение:** отделить прямые textual/syntactic relations от intertextual inference и historical reconstruction. Это исследовательская карта аргумента, а не визуальный дизайн.

## 1. Типы связей

```text
DIRECT_SYNTAX      = связь маркирована грамматикой/коннектором текста
DIRECT_SEMANTIC    = связь необходима по непосредственному смыслу фразы
INTERTEXT_STRONG   = ясная/широко признанная связь с Писанием
INTERTEXT_PROPOSED = академически предложенный echo/allusion, но не explicit quotation
EXEGETICAL_B       = leading interpretive relation
EXEGETICAL_C       = serious competing relation
HISTORICAL_B       = probable contextual reconstruction
HISTORICAL_D       = edge/history-only reconstruction
NEGATIVE_BOUNDARY  = связь, которую нельзя рисовать как установленную
```

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

## 4. Strong intertextual edges

| From | Target | Type | Calibration |
|---|---|---|---|
| V07B | Gen 1:26–27 | INTERTEXT_STRONG | image language |
| V08A | Gen 2:21–23 | INTERTEXT_STRONG | woman from man |
| V09A | Gen 2:18–23 | INTERTEXT_STRONG | woman created in relation to man/helper context |
| V12A | Gen 2:23 | INTERTEXT_STRONG | woman from man repeated |
| V12B | ordinary birth / Gen creation reversal in lived generation | DIRECT_SEMANTIC | men now come through women |
| V12C | God as ultimate source | DIRECT_THEOLOGICAL | explicit statement, not merely intertext |

## 5. Proposed intertextual edges — do not render as direct fact

| From | Target | Type | Status |
|---|---|---|---|
| V07C–V12C | 1 Esdras 4:13–41 | INTERTEXT_PROPOSED | Julie Newberry: cumulative echo; useful B/C proposal, not explicit citation |
| V10C | Qumran sacred-assembly angelology | INTERTEXT_PROPOSED / BACKGROUND_B | strengthens holy/liturgical angels; does not identify Paul's angels explicitly |
| V10C | Gen 6 / Watchers tradition | INTERTEXT_PROPOSED_C | ancient Tertullian line, weaker |
| V10B/V10C | 1 Cor 6:2–3 judging angels | INTERTEXT_PROPOSED_C | modern internal-Pauline proposal, possible but not explicit |

## 6. Historical reconstruction edges

| Text node | Historical proposal | Type | Rule |
|---|---|---|---|
| V04B | Roman male `capite velato` ritual/status | HISTORICAL_B | real background A; exact Corinth trigger B |
| V04B | Judaizing male prayer covering | HISTORICAL_D/C | record, do not promote |
| V05B/V06A | female veil as matronly/modesty/status marker | HISTORICAL_B | context supports significance, not one universal form |
| V05D/V06B | shaved woman = prostitute/adulteress | NEGATIVE_BOUNDARY | do not universalize; evidence insufficient for blanket equation |
| V14B | long male hair = specific homosexual role | HISTORICAL_D | Murphy-O'Connor/MacGregor edge model |
| V05B/V14–15 | loose hair = Dionysiac/ecstatic cult | HISTORICAL_D | possible reconstruction, not demonstrated local trigger |
| V10C | angels = bishops | HISTORICAL_D | Ambrosiaster reception, not Pauline lexical fact |
| V10C | angels = human church messengers | HISTORICAL_D/C | Murphy-O'Connor; possible semantic use of `angelos`, weak contextually |

## 7. Contested semantic nodes

### `κεφαλή` V03

```text
HEADSHIP/AUTHORITY/PREDOMINANCE -> B leading
SOURCE/ORIGIN ONLY             -> C viable
PROMINENCE                      -> C/B depending formulation
ONE FIXED LEXICAL GLOSS         -> prohibited
```

### covering language V04–V06/V13

```text
TEXTILE/MATERIAL COVERING -> B-high leading
HAIR/HAIRSTYLE ONLY       -> C serious alternative
EXACT MODERN GARMENT FORM -> HOLD / not reconstructable at A
```

### `ἐξουσία` V10

```text
WOMAN = GRAMMATICAL SUBJECT      -> A
AUTHORITY/RIGHT/POWER LEXEME     -> A lexical core
SIGN OF HUSBAND'S AUTHORITY      -> B/C contextual interpretation
WOMAN'S OWN AUTHORITY/CONTROL    -> C/B serious alternative
LEXICALLY = VEIL                 -> prohibited
```

### `angels` V10

```text
ANGELS INVOKED                   -> A
HOLY/LITURGICAL                  -> B leading
WATCHERS/FALLEN                  -> C
HUMAN/CLERGY/OTHER               -> D/C-low
CERTAIN IDENTITY                 -> prohibited
```

### `φύσις` V14

```text
SEX-DIFFERENTIATION/NATURAL PROPRIETY -> B
PURE BIOLOGY ONLY                       -> overclaim
PURE ARBITRARY CUSTOM ONLY              -> overclaim
CULTURALLY CONSTRUED NATURALNESS        -> C/B serious explanatory model
```

### `τοιαύτην συνήθειαν` V16

```text
TRANS-LOCAL CHURCH PRACTICE APPEAL -> A
EXACT REFERENT                       -> B/C
CANCELS VV2-15                       -> D / discourse-incoherent
```

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

**Critical warning:** стрелка `HEAD RELATIONS → exact garment meaning` не DIRECT_SYNTAX; она exegetical. Стрелка `Roman ritual → v4 exact problem` не direct; она historical B. `Qumran → holy angels` background B, not direct identity.

## 9. Product handoff boundary

Эта карта может позднее стать semantic graph для интерактивной матрицы, но Research не определяет:

- layout;
- animation;
- colors;
- modal behavior;
- front-end component structure.

Research определяет только **nodes, relation types, confidence and negative boundaries**.
