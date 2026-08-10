# 1 Коринфянам 11:2–16 — quotation/refutation adversarial delta

**Дата:** 2026-08-10  
**Статус:** `ADVERSARIAL-STRESS-TEST / COSTA-BODY-READ / SHOEMAKER-SAGE / MARSHALL-BRILL / SALES-OPEN-FULLTEXT / NA28-CONTROL / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Why this layer exists

The current model matrix grades a large Corinthian quotation/refutation model in 1 Cor 11 as `D/C-low` because the transmitted text lacks an explicit quotation marker and the model must carry substantial discourse burden.

The recent-source pass discovered a real modern cluster that is stronger than a vague “Peppiatt says so” summary:

- Thomas R. Shoemaker 1987 — peer-reviewed structural/chiasm argument;
- Alessandra Castilho da Costa 2023/2024 — full linguistic/discourse analysis arguing vv4–9 are unendorsed quotations;
- Luis Josué Salés 2024 — open peer-reviewed adoption of vv3–10 as Corinthian query and vv11–16 as Pauline rejoinder;
- Jill E. Marshall 2019 — a distinct rhetorical model using **modified traditions**, not a large speaker-change quotation.

This pass asks two different questions that must not be conflated:

```text
Q1_SCHOLARLY_STATUS = is this a real published scholarly family?
Q2_TEXTUAL_FIT = does it best explain the transmitted Greek discourse?
```

A model can be a serious published alternative without becoming the leading textual explanation.

---

# 1. Direct source controls

## 1.1 Shoemaker 1987 — real peer-reviewed predecessor

Thomas R. Shoemaker, “Unveiling of Equality: 1 Corinthians 11:2–16,” *Biblical Theology Bulletin* 17.2 (1987): 60–63. DOI `10.1177/014610798701700204`.

SAGE’s official abstract states that Shoemaker:

- identifies a chiastic arrangement with structural emphasis on v10;
- translates v10 with woman having `liberty [exousia] over her head`;
- sees part of the veiling discussion as a quotation from people seeking women’s submission to veiling/hierarchy;
- reads Paul as responding that women’s liberty should not be withdrawn.

Official route:

- https://journals.sagepub.com/doi/10.1177/014610798701700204

Safe classification:

```text
SHOEMAKER_QUOTATION_MODEL_EXISTS = VERIFIED_PUBLISHER
SHOEMAKER_CHIASM_V10_CENTER = VERIFIED_ABSTRACT
SHOEMAKER_EXOUSIA_LIBERTY = VERIFIED_ABSTRACT
SHOEMAKER_FULL_BOUNDARY_DETAILS = ABSTRACT_LIMITED
```

The publication establishes a real scholarly lineage. It does not by itself prove the quotation boundary.

---

## 1.2 Costa 2023/2024 — strongest new linguistic argument located in this pass

Alessandra Castilho da Costa, “Identificando citações em 1 Coríntios 11:3–16: uma análise da orientação argumentativa e do ponto de vista,” *Revista de Estudos da Linguagem* 31.3: 1404–1446. DOI `10.17851/2237-2083.31.3.1404-1446`.

Official UFMG page:

- https://periodicos.ufmg.br/index.php/relin/article/view/55158

The official abstract says the article combines:

- Textual Discourse Analysis;
- Discursive Traditions;
- Argumentative Semantics;
- argumentative orientation;
- point-of-view analysis.

It concludes that vv4–9 are quotations not endorsed by Paul.

A CC BY full-text copy of the same DOI/object, exposed through the author/publication mirror, was substantially inspected in this pass. This allows us to test the argument rather than only record the abstract.

### Costa’s actual segmentation

```text
v3 = Pauline POV
vv4-9 = Corinthian POV / quotation
v10 = Pauline POV
vv11-12 = Pauline mutuality
v13 = Pauline declarative/propriety counterclaim in Costa's reading
vv14-15 = Pauline counterargument in Costa's reading
v16 = Pauline rejection of the Corinthian head-rule as church custom
```

This is **not** the same boundary as Salés (`vv3–10` as Corinthian query).

---

# 2. Costa’s strongest contributions

## 2.1 She supplies an explicit linguistic mechanism rather than a bare theological preference

Costa does not merely say “vv4–9 sound patriarchal, so Paul did not write them.” She models competing argumentative orientations and assigns propositions to a Pauline or Corinthian point of view.

That is a genuine methodological advance over popular quotation claims.

```text
COSTA_HAS_EXPLICIT_LINGUISTIC_MODEL = true
COSTA_QUOTATION_CLAIM != PURE_THEOLOGICAL_ASSERTION
```

## 2.2 She correctly pressures several real tensions

Her model foregrounds genuine textual pressure points:

- v10 makes the woman grammatical bearer of `ἐξουσία`;
- vv11–12 strongly affirm mutual interdependence;
- v15 calls long hair woman’s glory/natural covering;
- v16 contains a translocal church-practice appeal.

These are real controls already present in the current registry.

The quotation model therefore deserves to be represented in the literature map as a **serious published family**, not dismissed as an internet fringe idea.

## 2.3 She gives a concrete boundary: vv4–9

This is useful because “quotation/refutation” is often discussed without specifying exactly which words belong to the Corinthians.

Costa’s vv4–9 boundary is testable against discourse markers and the syntax of v10.

---

# 3. Major textual burdens in Costa’s model

## 3.1 The `διὰ τοῦτο` problem at v10 is the largest burden

The transmitted sequence is:

```text
v7  γάρ ...
v8  γάρ ...
v9  καὶ γάρ ...
v10 διὰ τοῦτο ...
```

On the surface, vv7–9 form a tightly linked explanatory chain and v10 begins:

> `διὰ τοῦτο` — “for this reason / therefore”.

The current verse audit correctly treats this as a direct discourse constraint:

```text
DIA_TOUTO_V10_LINKS_BACKWARD = A_DISCOURSE
```

If vv7–9 are a Corinthian position that Paul is rejecting, v10 must nevertheless present Paul’s own conclusion as “therefore” following immediately after that rejected material.

Costa handles this by making v3 the true Pauline causal basis for v10 and treating vv4–9 as an intervening refuted block. That is possible as a rhetorical construction, but it is an **extra discourse assumption** because the local connective naturally points to the immediately preceding creation/glory argument.

```text
COSTA_V10_BACKLINK_TO_V3_OVER_INTERVENING_VV4_9 = EXTRA_ASSUMPTION
```

This is the single strongest reason not to promote the model to leading status.

---

## 3.2 Costa’s v3 argument requires a highly specific semantic reconstruction

Costa interprets v3 in effect as:

```text
all humans have a head; even Christ has one
therefore man and woman share an attribute
therefore they are not contrary subjects
therefore contrary head treatment is not required
```

She then takes `κεφαλή` primarily as `source/origin`, using vv7–9 as cohesive/intertextual support.

Problems:

1. v3 presents three **relational metaphorical pairs**, not an explicit proposition “every human possesses an anatomical head”;
2. the current lexical audit grades `headship/authority` as `B_LEADING` and source-only as `C_VIABLE`;
3. using vv7–9 to prove the semantics of v3 while simultaneously assigning vv7–9 to the Corinthian voice creates a methodological tension: rejected Corinthian material becomes a major semantic anchor for Paul’s own v3.

Therefore:

```text
COSTA_V3_ALL_HUMANS_HAVE_HEAD_INFERENCE = INFERENTIAL_NOT_TEXTUAL
COSTA_KEPHALE_SOURCE_ONLY = CONTESTED_SEMANTIC_PREMISE
COSTA_V3_V7_9_COHESION_WHILE_V7_9_QUOTED = METHOD_TENSION
```

This does not falsify the model, but it means the quotation result is not independent of a disputed `κεφαλή` analysis.

---

## 3.3 Costa uses repunctuation/reclassification at vv13–15

The current NA28 presentation from Deutsche Bibelgesellschaft prints:

```text
v13 ... προσεύχεσθαι;
v14 οὐδὲ ἡ φύσις ...
v15 ... ἐστιν;
```

That is:

- v13 as a question;
- vv14–15 as a question ending after the male/female hair contrast.

Official NA28 route:

- https://www.die-bibel.de/bibel/NA28/1CO.11

Costa explicitly prefers a **declarative** reading at v13 and reads the nature/hair material so that it refutes rather than reinforces the earlier covering norm.

Important qualification:

```text
ANCIENT_MANUSCRIPT_PUNCTUATION != MODERN_NA28_PUNCTUATION
```

Modern punctuation is editorial and therefore cannot by itself refute Costa.

But the current critical edition’s punctuation shows that the conventional rhetorical-question reading is not a casual English-tradition accident. Costa must carry a real syntactic/discourse burden to repunctuate the passage.

```text
COSTA_V13_DECLARATIVE = POSSIBLE_BUT_AGAINST_NA28_EDITORIAL_PUNCTUATION
COSTA_V14_15_COUNTERREADING = REQUIRES_REPUNCTUATION/DISCOURSE_REANALYSIS
```

The project’s primary social-corpus audit independently finds strong ancient analogues for `nature -> sexed grooming propriety`, so Costa’s reversal also loses explanatory economy against that background.

---

## 3.4 v16 does not independently prove the quotation boundary

Costa argues that `τοιαύτην συνήθειαν` (“such a custom”) encapsulates the supposed Corinthian obligation:

```text
man uncover / woman cover
```

and that Paul says neither “we” nor the churches possess that rule.

This is a coherent possible antecedent analysis. But the current v16 audit established:

```text
SYNĒTHEIA_CUSTOM/PRACTICE = A_LEXICAL
V16_TRANSLOCAL_CHURCH_PRACTICE_APPEAL = A_TEXT
V16_NORMATIVE_FORCE = B_HIGH
V16_EXACT_CUSTOM_REFERENT = B_C
```

Because the exact referent of `τοιαύτην` remains disputed, v16 cannot be used as an independent A-level proof that vv4–9 were spoken by Corinthians.

```text
COSTA_V16_ANTECEDENT = C_VIABLE_READING
COSTA_V16_ANTECEDENT != QUOTATION_MARKER
```

---

# 4. Salés 2024 — useful because his boundary conflicts with Costa

Luis Josué Salés, “Paul and Pseudo-Paul: Authorship, Ideology, and the Difference of Androprimacy,” *Religions* 15.9 (2024): 1141. DOI `10.3390/rel15091141`.

Official full text:

- https://www.mdpi.com/2077-1444/15/9/1141

Salés explicitly reads:

```text
vv3-10 = Corinthian query / androprimal logic
vv11-16 = Pauline rejoinder
```

He emphasizes `πλὴν` at v11 as a strong adversative and argues vv11–12 ideologically subvert vv8–9.

This is significant but creates a critical control:

```text
COSTA_BOUNDARY = VV4_9
SALES_BOUNDARY = VV3_10
```

Two contemporary advocates agree that a quotation exists while disagreeing about where it begins and ends.

That boundary instability weakens any claim that the Greek itself transparently marks one quotation span.

## `πλὴν` is a real pivot but not a decisive speaker marker

The current verse audit already recognizes:

```text
PLEN_V11 = A_DISCOURSE_QUALIFICATION/COUNTERBALANCE
```

A strong adversative/qualifying pivot is fully compatible with one speaker correcting an over-reading of his own preceding argument.

Therefore:

```text
PLEN_V11_SUPPORTS_REAL_CONTRAST = true
PLEN_V11_PROVES_NEW_SPEAKER = false
```

Salés is a genuine published alternative, but his ideological `androprimacy` framework should not be confused with independent textual proof of quotation.

---

# 5. Marshall 2019 is an important control against false binary thinking

Jill E. Marshall, “Uncovering Traditions in 1 Corinthians 11:2–16,” *Novum Testamentum* 61.1 (2019): 70–87. DOI `10.1163/15685365-12341617`.

Official Brill abstract:

- https://brill.com/view/journals/nt/61/1/article-p70_5.xml?language=en

Marshall argues that Paul modifies inherited/traditional material:

```text
v3 = hierarchical tradition, modified/used by Paul
vv11-12 = interdependent tradition, modified/used by Paul
```

This explains tension without requiring a large speaker change.

Marshall therefore blocks a false binary:

```text
either flat Pauline monologue
or Corinthian quotation
```

A third model is:

```text
ONE_PAULINE_ARGUMENT_USING/REFORMULATING_DIFFERENT_TRADITIONS
```

This is especially important because v2 explicitly introduces `παραδόσεις`.

---

# 6. Newberry 2019 gives another continuity model

Julie Newberry, “Paul’s Allusive Reasoning in 1 Corinthians 11.7–12,” *New Testament Studies* 65.1 (2019): 43–58. DOI `10.1017/S0028688518000292`.

Cambridge abstract:

- https://www.cambridge.org/core/journals/new-testament-studies/article/abs/pauls-allusive-reasoning-in-1-corinthians-11712/EDE6D54A62D2265EA2C22291B6F2BA39

Newberry explicitly takes vv7–9 as Pauline patriarchal hierarchy, v10 as woman’s authority, and vv11–12 as counterbalancing interdependence.

This shows that the tension which motivates quotation models can be accounted for within a continuous Pauline argument:

```text
REAL_TENSION != MULTIPLE_SPEAKERS_REQUIRED
```

Her 1 Esdras proposal is itself an interpretive hypothesis, but it demonstrates a coherent non-quotation route through the same difficult transition.

---

# 7. Comparative matrix

| Node | Shoemaker | Costa | Salés | Marshall | Continuous current model |
|---|---|---|---|---|---|
| explicit large quotation | yes | yes | yes | no | no |
| proposed boundary | abstract not fully pinned here | vv4–9 | vv3–10 | N/A | N/A |
| v3 Pauline | likely/unclear from abstract | yes | no | yes, modified tradition | yes |
| vv7–9 Pauline | no under quotation | no | no | yes | yes |
| v10 Pauline | yes in Costa | yes | no | yes | yes |
| v11 contrast | corrective | Pauline | new rejoinder | second tradition | internal qualification |
| `διὰ τοῦτο` local continuity | structural burden | **major burden** | less boundary burden because v10 still quote, but v11 pivot bears more | natural | natural |
| v13 punctuation | not controlling here | declarative reinterpretation | question | not key | NA28 question |
| v14–15 | corrective | counterreading | Pauline rejoinder | not key | nature/hair analogy |
| v16 | rejection of opposing veil rule | rejects Corinthian rule | no such Corinthian custom | translocal closure within Pauline argument | translocal closure |
| speaker-change marker | structural/chiasm | inferred PdV conflict | `πλὴν` emphasis | not required | not required |

The key result is not “all quotation models fail.” It is:

> **The scholarly family is real, but its members require different quotation boundaries and different linguistic pivots.**

That is exactly what we would expect if the underlying tension is real but the speaker-change solution remains inferential.

---

# 8. Grade reconciliation: scholarly seriousness vs textual fit

The old single shorthand:

```text
LARGE_QUOTATION_REFUTATION = D_C_LOW
```

is too easy for future agents to misread as “no serious scholar argues this.”

The correct two-axis representation is:

```text
LARGE_QUOTATION_PUBLISHED_SCHOLARLY_FAMILY = C_SERIOUS / MULTIPLE_B1_SOURCES
LARGE_QUOTATION_TEXTUAL_FIT = D_C_LOW_TO_C_LOW
LARGE_QUOTATION_LEADING_MODEL = false
```

This is **not a core exegetical reversal**. It is a provenance/status refinement.

Why textual fit remains low:

1. no explicit quotation formula at the required boundary;
2. advocate boundaries differ (`vv4–9` vs `vv3–10`);
3. `διὰ τοῦτο` strongly pressures Costa’s boundary;
4. `πλὴν` supplies a natural internal qualification without requiring a new speaker;
5. Costa’s case partly depends on contested `κεφαλή`, punctuation, v13 and v16 readings;
6. Marshall/Newberry offer continuous-Pauline models that explain the same tensions without a speaker switch.

Why scholarly status rises:

1. Shoemaker is real peer-reviewed precedent;
2. Costa supplies a detailed modern linguistic analysis, not a devotional assertion;
3. Salés shows ongoing 2024 adoption in peer-reviewed literature;
4. the model belongs in a serious Status Quaestionis even if it is not the best textual solution.

---

# 9. Publication-safe formulation

Safe research prose:

> A substantial Corinthian-quotation reading is a genuine published minority model, represented in different forms from Shoemaker to recent linguistic and ideological studies. Its attraction is that it assigns the sharpest hierarchical material to a Corinthian voice and reads woman’s authority and mutual interdependence as Paul’s correction. The model, however, lacks an explicit quotation marker, its advocates disagree over the quotation boundaries, and key forms must reinterpret local discourse links such as `διὰ τοῦτο` and the punctuation/force of vv13–15. It should therefore be treated as a serious minority reconstruction rather than as an established solution.

Do **not** write:

```text
“modern linguistics proved vv4-9 are a quotation”
“Paul definitely rejects vv7-9 as Corinthian theology”
“πλὴν proves a new speaker begins at v11”
“NA28 punctuation proves Costa impossible”
```

All four are overclaims.

---

# 10. Current action

No change to the central current-registry verdict is authorized yet:

```text
CORE_GRADE_REVERSALS = 0
CURRENT_REGISTRY_LARGE_QUOTATION = D_C_LOW
```

But future agents must apply this status refinement:

```text
D_C_LOW = TEXTUAL_FIT_GRADE
NOT = SCHOLARLY_EXISTENCE_GRADE
```

If the main registry is later revised, prefer an explicit dual-axis row rather than a single ambiguous grade.

---

# 11. Remaining decisive evidence targets

For any future promotion of the quotation model, the useful targets are not more advocates. They are:

1. direct discourse-corpus evidence that unmarked quotations of comparable length in Paul can be bounded by the same markers;
2. a stronger explanation of `διὰ τοῦτο` at v10 under Costa’s vv4–9 boundary;
3. independent syntactic grounds for repunctuating vv13–15;
4. evidence that `τοιαύτην συνήθειαν` naturally points specifically to the obligations in vv6–7 rather than the contrary practice/contention;
5. early reception evidence preserving or independently implying a multi-speaker reading.

Until then, accumulation of additional modern advocates should **not** automatically raise textual probability.

---

## Boundary

```text
PRODUCT_WRITE = false
UI_IMPLEMENTATION = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
RECENCY != AUTHORITY
NUMBER_OF_ADVOCATES != TEXTUAL_PROOF
PUBLISHED_MODEL != EQUALLY_PROBABLE_MODEL
```
