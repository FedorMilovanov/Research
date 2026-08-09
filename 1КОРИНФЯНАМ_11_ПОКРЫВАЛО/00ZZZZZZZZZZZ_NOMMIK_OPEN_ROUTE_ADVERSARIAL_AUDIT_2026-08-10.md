# Aldar Nõmmik — open-route adversarial audit of the capite-velato / ritual-uniformity model

**Дата:** 2026-08-10  
**Статус:** `PRE-FULLTEXT / OPEN-ROUTE-ADVERSARIAL / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Scope and epistemic boundary

This audit does **not** pretend that the full dissertation PDF has been read.

Directly verified routes:

- University College Stockholm / EHS dissertation-defense page;
- EHS dissertation series listing, which explicitly marks the work `Fulltext i DiVA`;
- exact institutional URN: `urn:nbn:se:ths:diva-2600`;
- Wipf & Stock current 2025 edition page;
- Google Books limited preview, table of contents, searchable metadata/index terms;
- independent academic literature on the Roman background: Oster, Gill, Massey, Finney;
- a 2025 academic article by Carl Johan Berglund that already cites Nõmmik’s pp.81–150 in a live discussion of 1 Cor 11–14.

The current harness has not yet resolved the DiVA PDF bytes reliably. Therefore:

```text
NOMMIK_FULLTEXT_EXISTS = A_INSTITUTIONAL
NOMMIK_FULLTEXT_BYTES_READ = false
NO_FAKE_PAGE_LEVEL_CLAIMS = true
NOMMIK_USER_ACQUISITION_ALLOWED = false
DO_NOT_REQUEST_FROM_USER_IF_AGENT_CAN_ACCESS = true
```

The goal is to test everything the official/open routes actually establish and isolate the exact links that still require the full dissertation.

---

# 1. Model under test

Nõmmik’s official publisher/institutional summary proposes approximately this causal chain:

```text
Roman capite velato is familiar in Corinth
    ↓
Paul has instructed male Christians not to pray with a garment down over the head
    ↓
Some Corinthian interlocutors seek ritual uniformity
    ↓
They generalize male uncovering to all members
    ↓
Married women from different cultural backgrounds are pressured to remove everything from their heads
    ↓
The issue affects prayer / prophecy / access to divine knowledge
    ↓
Paul argues that covered prayer is shameful for men but not for women
    ↓
Women may retain coverings / hair accessories
    ↓
11:3–16 supplies theological, creation, authority, angelic and nature-based justification for sex-differentiated ritual head-state
```

The project must not grade this chain as a single proposition.

---

# 2. Node decomposition

## N1 — Roman `capite velato` existed as a male ritual practice

### Evidence

Oster 1988 specifically reconstructs the male issue in 11:4 against Roman ritual custom. Gill 1990 independently emphasizes Corinth’s Roman-colony setting and visual evidence of Roman male covered-head ritual. Massey 2018 further argues that the Greek of v4 and v6 points to material covering and explicitly builds on Oster/Gill/Finney.

### Grade

```text
N1_ROMAN_CAPITE_VELATO = A_HISTORICAL_BACKGROUND
```

This is not dependent on Nõmmik.

### Adversarial note

Even if Nõmmik’s entire causal reconstruction fails, N1 remains.

---

## N2 — Corinthian Christians would recognize the Roman gesture

### Supporting considerations

- Corinth was a Roman colony with Roman public imagery and ritual culture.
- Gill’s portraiture argument and Oster’s historical reconstruction make local recognition highly plausible.
- Nõmmik explicitly claims linguistic/conceptual linkage and familiarity.

### Limitation

Paul never writes, “you all know the Roman rite called capite velato.” Familiarity is historical inference.

### Grade

```text
N2_CORINTHIAN_RECOGNITION = B_HIGH_HISTORICAL_INFERENCE
```

---

## N3 — `κατὰ κεφαλῆς ἔχων` in v4 denotes a material object/garment

### Independent pressure

Massey 2018 argues that both `κατὰ κεφαλῆς ἔχων` and `κατακαλύπτω` belong to material-covering usage and not merely loose/long hair.

This fits the project’s existing leading textile reading.

### Competing reading

Hair-only/hairstyle models remain published and serious enough to retain C, especially because vv14–15 explicitly introduce hair.

### Grade

```text
N3_V4_MATERIAL_COVERING = B_HIGH
N3_V4_HAIR_ONLY = C_SERIOUS_ALTERNATIVE
```

### Nõmmik-specific question

Material covering does **not automatically** equal the specific Roman ritual `capite velato`.

```text
MATERIAL_OBJECT ≠ EXACT_ROMAN_RITE
```

---

## N4 — v4 specifically targets Roman `capite velato`

### Strength

- unusually strong historical fit for male covered prayer;
- Roman ritual is one of the few reconstructions that explains why a **man** would intentionally cover during religious performance;
- it explains the cultic/action context rather than generic street clothing.

### Weakness

- lexical material-covering evidence does not itself name the rite;
- Paul does not use the Latin label;
- other social/status uses of male head attire remain possible;
- Finney’s elite-status model shows that Roman dress evidence can support more than one causal story.

### Grade

```text
N4_V4_EXACT_CAPITE_VELATO = B_C
```

This is one of Nõmmik’s stronger distinctive links, but not A.

---

# 3. The central new causal leap

## N5 — Paul had previously told men not to perform covered-head ritual prayer

Nõmmik’s public summary reconstructs the Corinthians as matching women to “Roman men whom Paul had asked not to pray with garments over the head.”

The present letter does state the male prohibition in 11:4, but the full model appears to treat it as part of an existing instructional history between Paul and Corinth.

### Open-route limitation

Without the full argument, we cannot yet determine whether Nõmmik claims:

1. a prior oral Pauline instruction;
2. an inference from 11:4 itself;
3. a reconstructed earlier stage of the dispute.

### Grade

```text
N5_PRIOR_MALE_INSTRUCTION_HISTORY = HOLD_FULLTEXT
```

Do not silently convert the current written instruction into proof of a prior instruction.

---

## N6 — Corinthians generalized male uncovering into a universal ritual rule

This is the most distinctive hidden-event claim.

### Explanatory attraction

It solves a genuine problem: why would one controversy contain opposite male/female head-state instructions?

It also fits Nõmmik’s direct author-level portrayal of Corinthians as active interlocutors reasoning through Paul’s earlier teaching and developing implementation proposals in a multicultural association.

### Evidential cost

No surviving Corinthian letter says:

> “For uniformity, everyone should uncover.”

Paul does not explicitly quote that proposal.

The model must infer the proposal from the shape of Paul’s answer.

### Grade

```text
N6_CORINTHIAN_UNIFORMITY_RULE = C_SERIOUS_RECONSTRUCTION
```

This remains C even if historically elegant.

---

## N7 — the reconstructed rule applied specifically to married women of all cultures

Official summaries specify `married women of all cultures`.

### Possible support

- marriage/honor semantics fit many parts of 11:2–16;
- Ciampa’s direct summary of Ciampa/Rosner also foregrounds husbands/wives;
- Callon 2024 independently strengthens a free(d)-married-women model;
- multicultural Corinth provides a plausible environment for conflicting head customs.

### Problems

- `γυνή` remains lexically capable of “woman” or “wife” depending context;
- v12 complicates an exclusively-wife rendering;
- “all cultures” is sociological reconstruction, not wording in Paul.

### Grade

```text
N7_MARRIED_WOMEN_TARGET = B_C
N7_ALL_GYNE_EXCLUSIVELY_WIVES = OPEN_B_C
N7_ALL_CULTURES_UNIFORMITY_CONTEXT = C_RECONSTRUCTION
```

Nõmmik and Callon converge on marriage relevance by different routes; convergence strengthens the question, not automatic certainty.

---

# 4. Prayer, prophecy and “divine knowledge”

## N8 — prayer/prophecy are actual public religious performances

Paul explicitly says men and women pray/prophesy.

```text
N8_PRAYER_PROPHECY_ACTS = A_TEXT
WOMEN_PRAY_PROPHESY_11_5 = A
```

No historical model is needed to establish this.

---

## N9 — Roman divination/prayer provides a relevant comparator

`capite velato` occurred in Roman prayer/sacrifice/divinatory contexts. Nõmmik’s model gains plausibility because the Pauline issue is not merely dress but dress **during religious performance**.

```text
N9_RITUAL_PERFORMANCE_COMPARATOR = B_HIGH
```

---

## N10 — the exact Corinthian conflict was about efficacy of prayer / access to divine knowledge

Official summaries explicitly make this a central Nõmmik claim.

### Strength

- prophecy is a form of inspired/revelatory speech;
- chapters 12–14 are deeply concerned with spiritual manifestations and revelation;
- ritual cognition and efficacy are sensible categories for ancient religion.

### Weakness

11:2–16 itself foregrounds:

- honor/shame;
- head relations;
- creation;
- authority;
- angels;
- nature/hair;
- church practice.

It does not explicitly say, “your prayer is ineffective unless the ritual is performed correctly.”

### Grade

```text
N10_DIVINE_KNOWLEDGE_EFFICACY_TRIGGER = C
```

Until full-text evidence shows that the proposed efficacy conflict constrains more data than it imports, it remains a serious but hidden-cause reconstruction.

---

# 5. Verse-by-verse pressure test

## 11:2 — praise for traditions

### Fit

Nõmmik can naturally treat v2 as evidence that the dispute concerns implementation of prior Pauline teaching rather than wholesale rebellion.

This is one of the model’s underappreciated strengths.

### But

v2 does not tell us *which* prior instruction created the dispute.

```text
NOMMIK_V2 = NATURAL
CAUSAL_HISTORY_FROM_V2 = EXTRA_ASSUMPTION
```

---

## 11:3 — hierarchy of heads

Google Books TOC shows Nõmmik devotes an explicit major section to:

`Hierarchy of Heads: Foundational Premise, 1 Cor 11:3–6`.

This is important: the model does not simply discard v3 as unrelated.

### Open-route question

How does `κεφαλή` function in the causal model?

Possible options include:

- hierarchy/order justifies differentiated male/female ritual appearance;
- relational “head” structure frames shame toward another head;
- Christ/man/woman/God chain counters sex-neutral ritual uniformity.

Without the full pages, exact semantics are HOLD.

```text
NOMMIK_V3_INTEGRATION = PARTIAL_DIRECT_TOC
NOMMIK_KEPHALE_EXACT = HOLD_FULLTEXT
```

Project grade unchanged:

```text
KEPHALE_HEADSHIP_AUTHORITY = B_LEADING
KEPHALE_SOURCE_ONLY = C_VIABLE
```

---

## 11:4 — male covered prayer

This is the model’s strongest verse.

### Natural explanation

A Roman male cultic head-covering practice gives a concrete reason why Christian men in Roman Corinth might cover during prayer/prophecy.

### Stress score

```text
NOMMIK_V4 = NATURAL_TO_STRONG
```

The model is significantly stronger here than generic “men were doing something socially shameful” explanations.

---

## 11:5–6 — women uncovered / shaving comparison

### Model advantage

Nõmmik provides a symmetrical historical conflict: women uncover because some Corinthians extrapolate a universal ritual rule, not because women spontaneously revolt.

This explains why male and female instructions belong in one debate.

### Burden

The universalizing Corinthian rule is not explicit.

The shame/shaving rhetoric also has to be integrated with marital/status/honor meanings independently.

```text
NOMMIK_V5_6 = COMPATIBLE_WITH_EXPLANATORY_GAIN
UNIFORMITY_CAUSE = EXTRA_ASSUMPTION
```

---

## 11:7–9 — image/glory and creation order

This is a decisive stress point.

A complete model must explain why a ritual-uniformity dispute produces an extended Genesis-based argument.

### Possible fit

If Corinthians propose identical ritual head-state for men and women, Paul can appeal to creation differentiation to deny that identical ritual form follows from shared participation.

That is coherent.

### But

It is not obvious that Roman ritual uniformity alone generates:

- man as image/glory of God;
- woman as glory of man;
- woman from/for man.

These are theological arguments with their own weight.

```text
NOMMIK_V7_9 = COMPATIBLE
NOMMIK_V7_9_CAUSAL_NECESSITY = HOLD_FULLTEXT
```

Conservative creation/order reading remains stronger than any account that makes vv7–9 dispensable social rhetoric.

---

## 11:10 — `ἐξουσία` and angels

This is currently the hardest open-route gap.

Any whole model must explain:

- why `διὰ τοῦτο` follows vv7–9;
- why the woman is grammatical subject of `ἐξουσίαν ἔχειν`;
- what is on/over her head;
- why angels matter.

The official summaries do not provide Nõmmik’s detailed solution.

```text
NOMMIK_V10 = HOLD_MAJOR
```

The project must not infer that “authority” simply means permission to retain a veil because that would be reading the model into the phrase.

Current project controls remain:

```text
EXOUSIA_WOMAN_SUBJECT = A_SYNTAX
EXOUSIA_REFERENT = B_C
HOLY_LITURGICAL_ANGELS = B_LEADING
WATCHERS = C
```

If Nõmmik’s full treatment does not naturally integrate v10, that will be a major cost to the whole-model claim.

---

## 11:11–12 — `πλὴν`, interdependence and God

### Fit

A sex-differentiated ritual rule followed by mutual dependence can be coherent:

- differentiation is real;
- differentiation is not autonomous male superiority;
- both sexes remain mutually dependent “in the Lord”;
- all things ultimately derive from God.

### Strength

This prevents a caricature in which a capite-velato model must deny mutuality.

### Stress score

```text
NOMMIK_V11_12 = NATURAL_COMPATIBLE
```

No special hidden history is needed to accommodate these verses.

---

## 11:13 — appeal to judgment

A community already debating ritual uniformity could naturally be asked to judge the propriety of female uncovered prayer.

```text
NOMMIK_V13 = COMPATIBLE
```

But v13 does not independently prove the prior debate reconstructed by Nõmmik.

---

## 11:14–15 — `φύσις`, long hair and `περιβόλαιον`

This is another major stress point.

A strong Nõmmik model must explain why Paul moves from Roman ritual garment practice to sex-differentiated hair.

### Possible coherent role

Hair can function as an analogy/naturalized sign that male/female head presentation is not intended to be ritualistically identical.

That would support Paul’s resistance to sex-neutral ritual uniformity.

### Cost

The analogy still does not identify the underlying dispute as capite velato. Hair is equally usable by other material-covering models.

```text
NOMMIK_V14_15 = COMPATIBLE
NOMMIK_SPECIFIC_EXPLANATORY_ADVANTAGE_V14_15 = LOW_TO_HOLD
```

Current project:

```text
PHYSIS_EXACT_FORCE = B_C
HAIR_IS_NOT_IDENTICAL_TO_EXTERNAL_COVERING = B_HIGH_LEADING
```

---

## 11:16 — churches / custom

This verse tests whether the model can connect a highly local Roman dispute to Paul’s translocal church appeal.

### Possible fit

Paul may say Corinth is not free to establish a unique sex-neutral ritual innovation because the churches follow a shared practice.

This actually fits a reconstructed **local innovation** better than a model in which every church already has the exact same Roman social trigger.

### Remaining ambiguity

`τοιαύτην συνήθειαν` still has multiple possible referents.

```text
NOMMIK_V16 = COMPATIBLE
NOMMIK_V16_PROVES_UNIFORMITY_RECONSTRUCTION = false
V16_EXACT_CUSTOM_REFERENT = B_C
```

---

# 6. Whole-model stress matrix

Legend:

- `NATURAL` — model directly explains the datum with little extra machinery;
- `COMPATIBLE` — fits, but does not uniquely predict it;
- `EXTRA_ASSUMPTION` — needs a hidden historical step;
- `TENSION` — datum presses against model unless further argument succeeds;
- `HOLD` — open routes insufficient.

| Node | Nõmmik ritual-uniformity model | Comment |
|---|---|---|
| v2 prior traditions | `NATURAL` | active implementation dispute fits praise + correction |
| v3 head chain | `HOLD/COMPATIBLE` | dedicated Nõmmik section exists; exact semantics unread |
| v4 male covered prayer | `NATURAL` | strongest model node |
| v5–6 female uncovering | `NATURAL + EXTRA_ASSUMPTION` | symmetry gained, but universalization hidden |
| Roman Corinth | `NATURAL` | very strong independent background |
| textile covering | `NATURAL` | independently supported by Massey etc. |
| exact uniformity proposal | `EXTRA_ASSUMPTION` | no extant Corinthian statement |
| married women focus | `COMPATIBLE` | convergence with other marriage models; not exclusive proof |
| vv7–9 creation | `COMPATIBLE` | differentiation supports anti-uniformity; full causal fit unread |
| v10 exousia | `HOLD_MAJOR` | exact treatment needed |
| v10 angels | `HOLD_MAJOR` | exact treatment needed |
| vv11–12 mutuality | `NATURAL/COMPATIBLE` | differentiation + interdependence coherent |
| v13 propriety | `COMPATIBLE` | community judgment fits dispute |
| vv14–15 hair/nature | `COMPATIBLE` | analogy against sex-neutral presentation, not unique support |
| v16 churches/custom | `COMPATIBLE` | local innovation vs wider practice is coherent |
| prayer/prophecy | `NATURAL` | ritual context is a strength |
| exact prayer efficacy/divine knowledge trigger | `EXTRA_ASSUMPTION` | requires full evidence chain |

---

# 7. Comparison with neighboring Roman-context models

## Oster

Primary strength: explains **male covered worship** historically through Roman ritual ethos.

Nõmmik extends Oster by attempting to explain the female side and the full dispute.

```text
OSTER = STRONG_BACKGROUND / NARROWER_V4_RECONSTRUCTION
NOMMIK = BROADER_WHOLE_MODEL / HIGHER_RECONSTRUCTIVE_BURDEN
```

---

## Gill

Gill broadens the Roman-colony/portraiture frame and warns against treating Corinth as simply Greek.

Nõmmik is more causal and more specific.

```text
GILL = VISUAL_SOCIAL_BACKGROUND
NOMMIK = RITUAL_CAUSAL_MODEL
```

Gill’s mixed female portraiture remains a warning against any claim that Roman women followed one universal veil rule.

---

## Massey

Massey strongly reinforces material-covering semantics and Roman male veiling data.

This supports Nõmmik’s **starting point**, not his hidden Corinthian dialogue.

```text
MASSEY_MATERIAL_SEMANTICS -> SUPPORTS N1/N3
MASSEY != PROOF_OF_N6_UNIFORMITY_RULE
```

---

## Finney

Finney uses the same broad Roman/honor world but reconstructs higher-status male Corinthians signaling status through head attire and female covering safeguarding community honor.

This proves an important methodological point:

```text
SAME_ROMAN_DATA_CAN_SUPPORT_MULTIPLE_CAUSAL_RECONSTRUCTIONS
```

Therefore historical plausibility must not be confused with unique explanatory entailment.

---

## Callon

Callon’s 2024 free(d)-married-women model focuses social/body autonomy and slavery.

Nõmmik’s married-women emphasis may converge with Callon, but mechanisms differ:

```text
CALLON = SOCIAL_STATUS / BODY_AUTONOMY / MARRIAGE
NOMMIK = RITUAL_UNIFORMITY / ROMAN_MALE_PRAYER MODEL
```

Convergence on marriage increases confidence that marital status matters somewhere in the passage, but does not settle the referent of every `γυνή`.

---

## Peters

Peters 2025 frames bodily/head control through citizenship/status and ecclesial reconfiguration.

Nõmmik frames it through ritual procedure and group dynamics.

Both resist a simplistic “rebellious Corinthian women removed veils” narrative.

A future full-text comparison should ask whether:

- citizen-body/status transformation;
- ritual-uniformity/cognition;
- or a combined model

better explains the same head-state data with fewer hidden events.

---

# 8. Cognitive science of religion — evidence vs explanation

Nõmmik explicitly uses cognitive science of religion and a section on cognition/group dynamics.

This requires a strict methodological distinction.

## Legitimate use

Cognitive/social theory may explain why:

- ritual uniformity becomes attractive;
- visible head-state signals group membership;
- deviations produce conflict;
- ritual efficacy becomes cognitively salient.

## Illegitimate shortcut

A general theory of human ritual behavior cannot independently establish that **this particular Corinthian group actually made this particular proposal**.

Thus:

```text
COGNITIVE_MODEL_EXPLAINS_PLAUSIBILITY ≠ HISTORICAL_EVENT_EVIDENCE
```

Full-text audit must identify where Nõmmik supplies independent ancient/Pauline evidence for the event before using cognitive theory to explain it.

---

# 9. Falsification / promotion criteria

## What could promote Nõmmik’s exact trigger from C toward B?

Any combination of:

1. direct ancient evidence that mixed-sex associations in Roman Corinth pursued ritual head-state uniformity;
2. strong evidence that Paul’s wording preserves identifiable fragments of the Corinthians’ counterargument;
3. linguistic evidence making v4 specifically Roman cultic capite velato, not generic material covering;
4. a natural explanation of v10 authority + angels from the proposed dispute without auxiliary hypotheses;
5. primary evidence connecting ritual uncovering with access to divine knowledge in a context genuinely analogous to Corinthian prophecy;
6. evidence that the model predicts vv7–16 better than competing textile/order models.

## What would downgrade it?

1. full text relies primarily on general ritual theory for the hidden uniformity proposal;
2. v10 and angels are only appended rather than generated by the model;
3. creation argument has to be treated as rhetorical window-dressing;
4. Roman female evidence contradicts the proposed “all married women” pressure mechanism;
5. exact Greek in v4 supports material covering but not specifically `capite velato`;
6. v16 church-wide practice works only by importing the conclusion.

---

# 10. Interim verdict

Nõmmik deserves serious status because he attacks the **male problem** that many popular readings neglect and tries to explain both sexes within one Roman ritual dispute.

But the evidential hierarchy must remain:

```text
ROMAN_CAPITE_VELATO_EXISTS = A
CORINTH_KNOWS_ROMAN_RITUAL_WORLD = B_HIGH
V4_MATERIAL_COVERING = B_HIGH
V4_EXACT_CAPITE_VELATO = B_C
CORINTHIAN_SEX_NEUTRAL_UNIFORMITY_PROPOSAL = C
DIVINE_KNOWLEDGE_EFFICACY_AS_EXACT_TRIGGER = C
NOMMIK_WHOLE_MODEL = C_SERIOUS_CURRENT_RECONSTRUCTION
```

The model is **not refuted** by the open-route audit. It is also **not promoted** to leading B because the most novel links remain hidden-event reconstructions and v10 is still unread at detail level.

The current calibrated conservative synthesis remains more robust as a **text-level model** because it needs fewer unspoken historical events:

```text
material covering
+ sex-differentiated order / creation reasoning
+ woman’s real agency in v10
+ mutual interdependence vv11–12
+ broader church practice
```

Nõmmik may eventually improve the reconstruction of the **local trigger** without replacing that text-level synthesis.

---

# 11. Required next action

Continue trying to resolve the institutional DiVA bytes by URN:

`urn:nbn:se:ths:diva-2600`

If acquired, audit these sections first:

1. pp.81–150 — material garment / capite velato corpus (also independently cited by Berglund 2025);
2. cognition/group dynamics around pp.205–206;
3. exegesis beginning around p.230;
4. v10 treatment;
5. `φύσις` / hair;
6. conclusions around p.317;
7. ancient-literature index to spot-check primary evidence.

Until then:

```text
NOMMIK_PROMOTION_BLOCKED = true
PUBLICATION_HOLD = true
```
