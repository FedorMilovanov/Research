# 1 Коринфянам 11:2–16 — current literature radar 2024–2026

**Дата:** 2026-08-10  
**Статус:** `CURRENT-LITERATURE-RADAR / RESEARCH-ONLY / ADVERSARIAL-INGRESS / PUBLICATION-HOLD`

## Цель

Проверить, не держится ли текущий корпус на литературе до 2024 года и не появились ли в 2024–2026 новые whole-model reconstructions, новые исторические аргументы или свежие академические давления, которые требуют отдельного узла.

Не включать публикацию только потому, что у неё свежая дата. Для ingress нужен хотя бы один из критериев:

1. новая реконструкция Sitz im Leben;
2. новый primary-data корпус;
3. новая синтаксическая/текстологическая аргументация;
4. новая синтезирующая монография/комментарий;
5. современная published edge-model, нужная для полноты adversarial map.

```text
RECENCY != AUTHORITY
PEER_REVIEW != CORRECTNESS
NEW_MODEL != GRADE_UPGRADE
PUBLICATION_DATE_MUST_BE_VERIFIED
```

---

# 1. Already ingested and not duplicated

## 1.1. Callie Callon — HTR 2024

**“Authority Over Whose Head? Did Paul Instruct Wives or All Women to Cover Their Heads (1 Corinthians 11:2–16)?”**  
*Harvard Theological Review* 117.4 (2024): 699–719.

Already fully ingested in the open-fulltext closure layer.

Current project result:

```text
CALLON_FREE_D_MARRIED_WOMEN_MODEL = B_C_SERIOUS_CURRENT_MODEL
WIVES_VS_ALL_WOMEN = OPEN_B_C
```

Do not duplicate as a “new discovery” in future radar passes.

## 1.2. Janelle Peters — 2025

**Paul and the Citizen Body: Egalitarian Athletics and Veiling Instructions in 1 Corinthians**, WUNT II 625, Mohr Siebeck, 2025.

Already ingested in:

`00ZZZZZZZZZ_SOURCE_CARD_JANELLE_PETERS_CITIZEN_BODY_2025_2026.md`

Current project node:

```text
PETERS_CITIZEN_BODY_MODEL = C_SERIOUS_CURRENT_MODEL
```

---

# 2. Aldar Nõmmik — major new current whole-model

## 2.1. Bibliographic identity

**Aldar Nõmmik, _Robes, Romans, and Rituals in First Corinthians: Paul and the Conflict over Head-Coverings_.**  
Dissertations Theologicae Holmienses 9.  
Academic dissertation; current Wipf & Stock edition published 2025-08-11, 374 pages.

Official publisher:

https://wipfandstock.com/9798385259823/robes-romans-and-rituals-in-first-corinthians/

Academic series/institutional listing:

https://ehs.se/forskning/dth/

Google Books also preserves the earlier dissertation publication metadata and identifies the work as Nõmmik’s dissertation.

Important access note:

The academic-series page explicitly advertises **Fulltext i DiVA**.

Therefore:

```text
NOMMIK_USER_ACQUISITION = false
NOMMIK_SELF_ACQUIRE_FULLTEXT = true
```

Do not ask the user for this book before exhausting the institutional full-text route.

## 2.2. Direct publisher thesis

The publisher describes a highly specific reconstruction:

- `capite velato` is the controlling Roman ritual comparandum;
- Paul and the Corinthians would have known the gesture;
- the disagreement concerns correct ritual procedure and efficacy of prayer/access to divine knowledge;
- some Corinthians are reconstructed as seeking **ritual uniformity**;
- on this model they wanted all association members, including married women from different cultures, to remove head coverings when praying/seeking divine knowledge, matching Roman men whom Paul had told not to pray with garments over the head;
- Paul responds by differentiating male and female ritual propriety: covered prayer is shameful for men, not for women; women may retain coverings/hair accessories during prayer/prophecy.

This is not merely “Gill again.”

## 2.3. Distinctive structure of the Nõmmik model

```text
ROMAN_CAPITE_VELATO
        +
RITUAL_COGNITION / DIVINE-KNOWLEDGE ACCESS
        +
CORINTHIAN_PRESSURE_FOR_UNIFORMITY
        ->
MALE UNCOVERING GENERALIZED BY SOME CORINTHIANS
        ->
PAUL REJECTS SAME-HEAD-PROCEDURE FOR BOTH SEXES
```

It shifts the reconstructed problem away from:

- only rebellious/unveiling women;
- only sexual modesty;
- only elite male status display;
- only hairstyle.

## 2.4. Why it deserves serious adversarial status

Explanatory strengths:

1. takes Roman ritual head-covering evidence seriously;
2. gives a single dispute that can encompass **men and women**, whereas many popular reconstructions explain only the women;
3. explains why prayer/prophecy and ritual head-state matter together;
4. naturally distinguishes male and female instructions rather than treating one side as an afterthought;
5. is a dissertation-length attempt, not a paragraph-level speculation.

Explanatory costs:

1. the exact Corinthian **uniformity demand** is reconstructed rather than stated;
2. “accessing divine knowledge” as a controlling conflict-frame must be demonstrated beyond generic prophecy/divination parallels;
3. cognitive-science framing may model plausibility without proving the historical trigger;
4. the theory must still explain `κεφαλή`, creation, `ἐξουσία`, angels, `φύσις`, and v16 without making them secondary decorations;
5. its claim that later interpreters broadly misunderstood the Sitz im Leben is historically large and needs independent reception testing.

## 2.5. Project calibration

```text
NOMMIK_RITUAL_UNIFORMITY_CAPITE_VELATO_MODEL = C_SERIOUS_CURRENT_RECONSTRUCTION
ROMAN_CAPITE_VELATO_BACKGROUND = A
NOMMIK_EXACT_CORINTHIAN_UNIFORMITY_TRIGGER = C
```

Why exact trigger remains C:

The Roman ritual background is independently strong; the specific hidden demand for all members to uncover is a historical reconstruction that is not explicitly preserved in Paul’s wording.

No downgrade of material covering:

```text
NOMMIK_DOES_NOT_SUPPORT_HAIR_ONLY_REDUCTION = true
```

His model presupposes real garments/head-coverings in the ritual dispute, even while hair accessories can enter the reconstructed female practice.

---

# 3. Luis Josué Salés — 2024 “androprimacy” / quotation-rejoinder model

## 3.1. Source

**Luis Josué Salés, “Paul and Pseudo-Paul: Authorship, Ideology, and the Difference of Androprimacy,” _Religions_ 15.9 (2024): 1141.**

Open peer-reviewed article:

https://www.mdpi.com/2077-1444/15/9/1141

## 3.2. Model

Salés proposes `androprimacy` as a category for male-precedence ideology.

For 1 Cor 11 he explicitly adopts:

```text
11:3–10 = Corinthian subordinative / androprimal view quoted by Paul
11:11–16 = Pauline rejoinder/subversion
```

He therefore treats the `πλὴν` movement and vv.11–12 mutuality as ideological rejection of the male-priority reasoning in the preceding block.

This is then contrasted with his reading of 1 Tim 2:11–15.

## 3.3. What is actually new

The **quotation/refutation architecture itself is not new**; the project already maps Murphy-O’Connor/Walker/quotation models and recent variants.

Salés contributes:

- a new ideological category (`androprimacy`);
- a current peer-reviewed restatement;
- a direct canonical comparison with 1 Tim 2.

But he does not supply a new manuscript delimiter or explicit ancient quotation mark.

## 3.4. Calibration

```text
SALES_ANDROPRIMACY_ANALYTICAL_CATEGORY = C_CURRENT_THEORETICAL_NODE
SALES_11_3_10_CORINTHIAN_QUOTATION = D_C_LOW
LARGE_QUOTATION_REFUTATION_MODEL = D_C_LOW_UNCHANGED
```

Reason:

- recency and peer review do not solve the primary structural problem;
- the text has no explicit quotation marker covering vv.3–10;
- vv.2–16 form a tightly connected argument under direct-Pauline reading without requiring an unmarked long quotation;
- the ideological contrast between vv.7–9 and 11–12 is real, but **qualification/counterbalance** is not equivalent to proof of different speakers.

Important adversarial value:

Salés forces the conservative model to explain why `πλὴν`, mutuality and `πάντα ἐκ τοῦ θεοῦ` are genuine argumentative limits rather than rhetorical afterthoughts.

---

# 4. Klára Hamplová — 2025 master’s thesis

## 4.1. Source

**Klára Hamplová, “Women’s Prayer in 1 Cor 11:2–16: Sociocultural Context, Exegesis and Theological Message.”**  
Charles University, Catholic Theological Faculty; defended 2025-09-03.

Institutional repository:

https://dspace.cuni.cz/handle/20.500.11956/205699

The repository exposes the complete thesis (812.7 kB), abstracts, supervisor/opponent reports and defense record.

## 4.2. Scope

The institutional abstract says the thesis focuses on:

- `κεφαλή`;
- gender roles;
- early Corinthian community;
- historical, cultural and theological framework;
- linguistic/stylistic/argumentative exegesis;
- symbolic gestures, women’s status and liturgical participation.

## 4.3. Weight

This is useful as:

- a very recent bibliography radar;
- a Central European/Catholic reception control;
- a source-mining route for recent secondary literature.

But:

```text
HAMPLOVA_2025 = P3_CURRENT_THESIS_CONTROL
```

It is not treated as equivalent to a peer-reviewed major monograph or technical commentary.

Because the full text is openly available:

```text
HAMPLOVA_USER_ACQUISITION = false
```

A future bibliography-mining pass can inspect it directly if it points to sources absent from the present corpus.

---

# 5. Israel O. O. Odewole — 2025 article

## 5.1. Source

**Israel O. O. Odewole, “FEMINIST AGENDA: Paul’s View of Women in 1 Corinthians 11:2–16,” _QUAERENS: Journal of Theology and Christianity Studies_ 7.1 (2025): 18–33.**

Journal route:

https://jurnal.widyaagape.ac.id/index.php/quaerens/article/view/240

Full text is open under CC BY-NC-SA.

## 5.2. Research value

The article is useful mainly as **current reception history**: it explicitly frames the passage through contemporary feminist/ministry concerns and draws on older literature such as Walker, Wire, Witherington, Økland and broad church debates.

It does not appear, in this audit, to introduce:

- new manuscript evidence;
- new lexical corpus;
- new archaeological evidence;
- a uniquely demonstrated historical reconstruction.

Its argument also relies heavily on older secondary/popular commentary chains in places.

Calibration:

```text
ODEWOLE_2025 = P3_CURRENT_RECEPTION_NODE
EVIDENTIAL_GRADE_FOR_CORE_CLAIMS = D_C_LOW
```

Do not use it to update Greek/historical project grades.

---

# 6. Jason Garwood — 2026 contemporary counter-reading

## 6.1. Source

**Jason Garwood, _Paul & the Head Covering: A Biblical Reassessment_. Cross & Crown Books, 2026.**

Current Google Books metadata directly summarizes the thesis.

## 6.2. Thesis

The publisher/Google description says Garwood argues:

- Corinthians imported cultural customs into Paul’s teaching;
- Paul is correcting that confusion rather than mandating a universal covering;
- creation order and mutual authority remain;
- Christian freedom means no universal law requires head covering.

## 6.3. Weight

This is a useful **2026 contemporary non-universalist reception/edge node**, especially because it combines creation-order language with rejection of a universal covering law.

However, in the verified routes for this pass it is not established as a peer-reviewed academic monograph or a major academic-press contribution.

Calibration:

```text
GARWOOD_2026_NO_UNIVERSAL_COVERING_MODEL = D_C_LOW_CURRENT_EDGE
```

It should be represented in the “history/current debate” map, not weighted alongside Nõmmik/Peters/Callon/P0 technical commentaries.

---

# 7. False-freshness correction — Penner & Vander Stichele

Search/index platforms currently surface:

**Todd Penner & Caroline Vander Stichele, “Unveiling Paul: Gendering Ethos in 1 Corinthians 11:2–16”**

with misleading `October 2025` metadata on at least one repository page.

Authoritative university publication metadata gives:

```text
PUBLICATION_YEAR = 2005
```

The PDF itself identifies `lectio difficilior 2/2004`.

Therefore:

```text
PENNER_VANDER_STICHELE_CURRENT_2025 = false
```

This is an older socio-rhetorical/gender-ideology node, **not** new 2025 scholarship.

This correction is important because current-literature searches can be polluted by repository upload/reindex dates.

---

# 8. 2024–2026 radar ranking

## Tier R1 — material new adversarial pressure

1. **Callon 2024** — wives/free(d)-wives and slavery/body-autonomy; already ingested.
2. **Peters 2025** — citizen body, bodily/head control, creation/angels/interdependence; already ingested.
3. **Nõmmik 2025** — capite-velato + ritual-uniformity/cognitive-religion whole-model; **newly ingested here**.
4. **Garland 2025 2e** — current technical commentary; P0 HOLD.

## Tier R2 — current theoretical / canonical pressure

5. **Salés 2024** — androprimacy + vv.3–10 quotation / vv.11–16 rejoinder; structural model remains low.
6. **Gorman 2025** — current pastoral/theological commentary control already in P1 queue; no new technical grade without direct section.

## Tier R3 — current bibliography/reception/edge mapping

7. **Hamplová 2025** — open master’s thesis; source-mining/current reception.
8. **Odewole 2025** — current reception; low evidential weight for core exegesis.
9. **Garwood 2026** — current confessional/non-universalist edge node; low evidential weight until stronger academic apparatus is established.

---

# 9. New model taxonomy delta

Add one serious whole-model row:

```text
MODEL_N = NOMMIK_RITUAL_UNIFORMITY_CAPITE_VELATO
GRADE = C_SERIOUS_CURRENT_RECONSTRUCTION
```

Core sequence:

```text
Roman male capite velato known
-> Paul prohibits male covered prayer
-> some Corinthians generalize uncovered ritual appearance to all members
-> married women face pressure to remove culturally meaningful coverings/accessories
-> Paul rejects sex-neutral ritual uniformity
-> male and female head-state remains differentiated in prayer/prophecy
```

This model should be added to the next whole-model stress test rather than left as a bibliography footnote.

---

# 10. What the current radar changes — and does not change

## Changes

```text
NOMMIK_RITUAL_UNIFORMITY_CAPITE_VELATO_MODEL = C_SERIOUS_CURRENT_RECONSTRUCTION
SALES_ANDROPRIMACY = C_CURRENT_THEORETICAL_NODE
SALES_LARGE_QUOTATION = D_C_LOW_UNCHANGED
HAMPLOVA_2025 = P3_CURRENT_THESIS_CONTROL
ODEWOLE_2025 = P3_CURRENT_RECEPTION_NODE
GARWOOD_2026 = D_C_LOW_CURRENT_EDGE
PENNER_VANDER_STICHELE_2025_DATE = CORRECTED_TO_OLDER_PUBLICATION
```

## Does not change

```text
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
KEPHALE_HEADSHIP_AUTHORITY = B_LEADING
KEPHALE_SOURCE_ONLY = C_VIABLE
EXOUSIA_WOMAN_SUBJECT = A_SYNTAX
EXOUSIA_REFERENT = B_C
HOLY_LITURGICAL_ANGELS = B_LEADING
WATCHERS = C
ROMAN_CAPITE_VELATO_BACKGROUND = A
EXACT_CORINTH_TRIGGER = B_RECONSTRUCTION
WIVES_VS_ALL_WOMEN = OPEN_B_C
```

Nõmmik actually strengthens the importance of Roman ritual evidence while increasing uncertainty over **which exact Corinthian behavior triggered Paul**.

---

# 11. Next Research action generated by this radar

Because Nõmmik’s full dissertation is advertised through the institutional full-text route, the correct next step is **not** to ask the user for it.

Create a separate open-fulltext Nõmmik audit focused on:

1. primary `capite velato` evidence;
2. exact evidence for the Corinthian “uniformity” reconstruction;
3. `κεφαλή` treatment;
4. v10 `ἐξουσία` and angels;
5. vv13–15 hair/`φύσις`;
6. v16;
7. whether cognitive-science argument provides evidence or only explanatory modelling;
8. how the theory performs against our existing whole-model stress matrix.

Until that direct pass:

```text
NOMMIK_WHOLE_MODEL = C
NOMMIK_PRIMARY_EVIDENCE_CHAIN = HOLD_FULLTEXT_AUDIT
```

`PUBLICATION_HOLD=true`.