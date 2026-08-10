# 1 Коринфянам 11:2–16 — direct-source / recent-scholarship pass

**Дата:** 2026-08-10  
**Статус:** `DIRECT-PUBLISHER-CONTROL / RECENT-SCHOLARSHIP / SOURCE-SEPARATION / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Purpose

This pass follows the citation-fabrication quarantine and intentionally does **not** chase more unsourced agent summaries. It tests high-value live targets against publisher/institutional pages and identifies recent, real scholarship that the uploaded agent dump either missed or over-described.

Operational rules:

```text
AGENT_DUMP = DISCOVERY_ONLY
PUBLISHER_ABSTRACT != FULL_ARTICLE
BOOK_DESCRIPTION != PROOF_OF_HIDDEN_HISTORICAL_EVENTS
BIBLIOGRAPHIC_EXISTENCE != EXEGETICAL_CORRECTNESS
PEER_REVIEW != PROBABILITY_PROMOTION_AUTOMATICALLY
SECONDARY_QUOTE_CHAIN != DIRECT_BOOK_TEXT
NO_CORE_GRADE_CHANGE_WITHOUT_CLAIM_LEVEL_ADVERSARIAL_REVIEW = true
```

The global repository evidence classes remain `A1/A2/A3/B1/C/D`. For the sources below:

- official publisher/institutional metadata can establish bibliographic existence/provenance at `A2/A3` level;
- the scholarly exegetical argument itself is normally `B1` unless independently grounded by primary textual/archaeological controls;
- historical reconstruction remains reconstruction even when stated by the author or publisher.

---

# 1. Aldar Nõmmik — direct access map is now materially better

## 1.1 Official publication state

Official/institutional controls verify the work:

> Aldar Nõmmik, *Robes, Romans, and Rituals in First Corinthians: Paul and the Conflict over Head-Coverings*, Dissertationes Theologicae Holmienses 9.

Current publication routes include:

- Enskilda Högskolan Stockholm series page, which lists the dissertation and explicitly labels a `Fulltext i DiVA` route;
- Wipf & Stock edition, published 2025-08-11, 374 pp., ISBN 9798385259823;
- earlier 2024 BoD/EHS edition, 372 pp., ISBN 9789188906274;
- Google Books limited preview exposing contents/selected pages and author/publisher description.

### Routes

- EHS series: https://ehs.se/forskning/dth/
- Wipf & Stock: https://wipfandstock.com/9798385259823/robes-romans-and-rituals-in-first-corinthians/
- Google Books, Wipf edition: https://books.google.com/books?id=JjGFEQAAQBAJ
- Google Books, 2024 edition: https://books.google.com/books?id=2KQ1EQAAQBAJ

## 1.2 Separate the evidence substrate from the reconstructed Corinthian conflict

The Google Books contents and the independent 2025 Berglund citation permit an important **structural** refinement.

The 2024 edition contents expose a long pre-exegetical/background trajectory including:

- theory/method;
- visual/material evidence;
- a large section beginning around `Having a Garment Down from the Head`;
- a later `Capite velato Human Cognition and Group Dynamics` section around p.205;
- later explicit exegetical/argument sections;
- `Women as Scapegoats` at p.289;
- conclusions at p.317.

Carl Johan Berglund 2025 independently cites **Nõmmik pp.81–150** in his article bibliography when treating the 1 Cor 11 social/ritual background.

This is enough to enforce the following separation:

```text
NOMMIK_ROMAN_RITUAL_EVIDENCE_SUBSTRATE != NOMMIK_HIDDEN_CORINTH_TRIGGER
NOMMIK_MODEL_DESCRIPTION = AUTHOR/INSTITUTIONALLY_VERIFIED
NOMMIK_HIDDEN_CORINTH_EVENTS = C_SERIOUS_RECONSTRUCTION
NOMMIK_BACKGROUND_AND_RECONSTRUCTION_MUST_BE_CITED_SEPARATELY = true
```

This matters because the author/publisher description itself argues that some Corinthians sought ritual uniformity and pressed married women to remove head items. That is **what Nõmmik argues**, not direct evidence that the hidden event happened.

## 1.3 Locator caution

The 2024 and 2025 Google Books renderings expose slightly different/garbled TOC pagination in search output. Therefore:

```text
NOMMIK_EXACT_PRINT_PAGE_LOCATOR = LOCATOR_HOLD_UNLESS_EDITION_PINNED
NOMMIK_2024_PAGE != AUTOMATICALLY_NOMMIK_2025_PAGE
```

Do not quote a locator copied from search-snippet TOC output without checking the edition/object.

---

# 2. Carl Johan Berglund 2025 — real peer-reviewed reception of Nõmmik, but agent over-description must be held

## 2.1 Verified source

Carl Johan Berglund, “Paulus profetiska praktik och samhällets förväntningar i Första Korinthierbrevet 11–14,” *HYBRID* 3.1 (2025): 36–60. DOI `10.58412/hyb.v3i1.25747`.

Official university and SwePub records identify it as a **peer-reviewed scientific journal article**. The official abstract says Berglund argues that Paul:

1. assumes both men and women prophesy;
2. prioritizes a broad category of teaching gifts over more display-oriented gifts;
3. recommends that wives of male prophets avoid publicly correcting their husbands.

### Routes

- Åbo Akademi research record: https://research.abo.fi/en/publications/paulus-profetiska-praktik-och-samh%C3%A4llets-f%C3%B6rv%C3%A4ntningar-i-f%C3%B6rsta-k/
- SwePub record: https://swepub.kb.se/showrecord?d=swepub&f=&g=&m=50&n=3&q=k%C3%B6nsroller&r=&s=c&t=v&tab1=&tab2=&tab3=full&vw=full
- Journal page: https://publicera.kb.se/hyb/article/view/25747

## 2.2 What is directly established about Nõmmik reception

The official journal page bibliography cites:

> Aldar Nõmmik, *Robes, Romans, and Rituals in First Corinthians*, 81–150.

Thus:

```text
BERGLUND_2025_EXISTS = VERIFIED
BERGLUND_2025_PEER_REVIEWED = VERIFIED_INSTITUTIONAL
BERGLUND_CITES_NOMMIK_81_150 = VERIFIED_DIRECT_JOURNAL_PAGE
NOMMIK_HAS_EARLY_2025_SCHOLARLY_UPTAKE = VERIFIED_MINIMUM
```

But citation is **not** endorsement of the entire Nõmmik reconstruction.

## 2.3 Agent-dump overclaims held

The uploaded agent dump went further and attributed to Berglund detailed conclusions such as:

- the strangest element is the uncovered praying man;
- Nõmmik specifically gives the superior explanation of Paul’s order of discussion;
- Berglund supplies a particular textual objection to Peppiatt’s unmarked quotation proposal.

Those claims may be in the article, but the accessible official HTML metadata/abstract/reference page does not establish them. The direct PDF endpoint is advertised by SwePub/DiVA, but it was not retrievable through the current verified browser path during this pass.

Therefore:

```text
BERGLUND_AGENT_BODY_LEVEL_NOMMIK_ENDORSEMENT = LOCATOR_HOLD
BERGLUND_AGENT_BODY_LEVEL_PEPPIATT_CRITIQUE = LOCATOR_HOLD
BERGLUND_ABSTRACT_LEVEL_CLAIMS = VERIFIED
```

This is a correction of **provenance**, not necessarily a rejection of the body-level claims.

---

# 3. Morna D. Hooker 1964 — direct Cambridge apparatus closes several source-attribution questions

## 3.1 Verified article

M. D. Hooker, “Authority on her Head: An Examination of I Cor. xi. 10,” *New Testament Studies* 10.3 (1964): 410–416. DOI `10.1017/S0028688500024334`.

Cambridge Core directly exposes bibliographic metadata and substantial reference apparatus.

Route:

- https://www.cambridge.org/core/journals/new-testament-studies/article/abs/authority-on-her-head-an-examination-of-i-cor-xi-10/947E8A98C64ACEA00D2BD815F0F8BDE5

## 3.2 `ἐξουσία` active semantic control

Cambridge’s displayed p.413 n.6 records Hooker’s use of Ramsay/Allo against reading “authority on the head” as merely authority **to which the woman is subjected**. The note explicitly appeals to known active uses of `ἐξουσία` as power exercised rather than power passively undergone.

This gives direct publisher-level control for the historical Hooker line:

```text
HOOKER_EXOUSIA_ACTIVE_SEMANTIC_ARGUMENT = DIRECT_CAMBRIDGE_APPARATUS
EXOUSIA_WOMAN_SUBJECT = A_SYNTAX // unchanged
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH // unchanged
```

No claim-grade promotion is needed; this strengthens provenance for an existing grade.

## 3.3 Hooker has a distinct angel-function proposal

Cambridge’s displayed p.415 n.2 preserves an important nuance often lost in summaries. Hooker invokes traditions in which angels worshipped Adam and suggests a possible danger that angels could be misled into worshipping man if his “glory” were displayed.

This is **not the same model** as sexual Watchers desiring women.

```text
HOOKER_ANGELS_MISDIRECTED_WORSHIP_OF_HUMAN_GLORY = PUBLISHED_ALTERNATIVE
HOOKER_MODEL != WATCHERS_SEXUAL_THREAT_MODEL
HOOKER_MODEL != HUMAN_MESSENGERS_MODEL
```

The project should preserve this as a distinct reception/exegetical alternative without promoting it to the leading angelic-function grade.

---

# 4. Joseph A. Fitzmyer 1957 — publisher extract is stronger than generic secondary summaries

## 4.1 Verified article/extract

Joseph A. Fitzmyer, “A Feature of Qumrân Angelology and the Angels of I Cor. XI. 10,” *New Testament Studies* 4.1 (1957): 48–58. DOI `10.1017/S0028688500011395`.

Cambridge Core directly exposes the extract and reference apparatus.

Route:

- https://www.cambridge.org/core/journals/new-testament-studies/article/feature-of-qumran-angelology-and-the-angels-of-i-cor-xi-10/59CE5686A3600CB7F51184CD960286F1

## 4.2 Directly established minimum

The Cambridge extract states that Qumran evidence does not merely add another angel interpretation; Fitzmyer believes it adds a supporting detail to an already common interpretation and makes competing interpretations less probable.

The displayed p.51 apparatus also explicitly stresses active New Testament use of `ἐξουσία`: power exercised by the bearer.

The displayed p.55 apparatus connects angelic functions with texts such as Tobit 12:12, 1 Cor 4:9, Eph 3:10, 1 Tim 5:21 and Heb 1:14.

Safe current use:

```text
FITZMYER_QUMRAN_USED_TO_STRENGTHEN_HEAVENLY_ANGEL_READING = DIRECT_CAMBRIDGE_EXTRACT
FITZMYER_EXOUSIA_ACTIVE_NT_CONTROL = DIRECT_CAMBRIDGE_APPARATUS
HEAVENLY_HOLY_ANGELS_REFERENT = B_HIGH_LEADING // unchanged
EXACT_ANGELIC_FUNCTION = B_C // unchanged
```

Do not turn the accessible extract into a claim that the exact angelic function is closed.

---

# 5. Julie Newberry 2019 — genuinely useful source absent from the uploaded agent dump

## 5.1 Verified source

Julie Newberry, “Paul’s Allusive Reasoning in 1 Corinthians 11.7–12,” *New Testament Studies* 65.1 (2019): 43–58. DOI `10.1017/S0028688518000292`.

Cambridge Core directly exposes the abstract and detailed reference apparatus.

Route:

- https://www.cambridge.org/core/journals/new-testament-studies/article/abs/pauls-allusive-reasoning-in-1-corinthians-11712/EDE6D54A62D2265EA2C22291B6F2BA39

## 5.2 Why it matters

Newberry argues that Paul’s reasoning in 11:7–12 includes underappreciated echoes of the Zerubbabel discourse in **1 Esdras 4:13–41**, putting Genesis 1, Genesis 2 and 1 Esdras 4 into conversation.

Her abstract describes the resulting tension as:

- an assumed patriarchal gender hierarchy in 11:7–9;
- woman’s `authority` over her head in 11:10;
- counterbalancing allusions in 11:11–12 that redirect from status toward interdependence “in the Lord” and shared origin in God.

This is important because the current claim registry already carries:

```text
1_ESDRAS_4_INTERTEXT = B_C_SERIOUS_PROPOSED
```

Newberry gives a direct specialist-journal owner/source for that proposal.

```text
NEWBERRY_1_ESDRAS_INTERTEXT = DIRECT_CAMBRIDGE_ABSTRACT
NEWBERRY_WOMAN_AUTHORITY_V10 = DIRECT_CAMBRIDGE_ABSTRACT
NEWBERRY_INTERDEPENDENCE_COUNTERBALANCE = DIRECT_CAMBRIDGE_ABSTRACT
CORE_GRADE_CHANGE = NONE
```

This is a **real new source acquisition** relative to the uploaded dump, not an AI-generated citation.

---

# 6. Jill E. Marshall 2019 — uploaded-agent claim verified from Brill, with proper limits

## 6.1 Verified source

Jill E. Marshall, “Uncovering Traditions in 1 Corinthians 11:2–16,” *Novum Testamentum* 61.1 (2019): 70–87. DOI `10.1163/15685365-12341617`.

Brill’s official abstract directly states that Marshall identifies two **modified traditions**:

- 11:3 — a hierarchical perspective on male/female relationship;
- 11:11–12 — an interdependent perspective.

She argues that Paul does not simply recite known teaching but modifies it by addition/reformulation as part of the rhetorical argument.

Route:

- https://brill.com/view/journals/nt/61/1/article-p70_5.xml?language=en

## 6.2 Calibration

The uploaded agent dump’s basic description of this model is therefore source-backed.

But Marshall’s model is **not the same as** the larger Peppiatt/Shoemaker claim that 11:3–10 is an unmarked Corinthian quotation rejected by Paul.

```text
MARSHALL_TWO_MODIFIED_TRADITIONS = VERIFIED_DIRECT_BRILL_ABSTRACT
MARSHALL_MODEL != LARGE_QUOTATION_REFUTATION_MODEL
```

This distinction matters for future syntheses.

---

# 7. Alessandra Castilho da Costa 2023/2024 — significant Portuguese linguistic support for a quotation model

## 7.1 Verified source

Alessandra Castilho da Costa, “Identificando citações em 1 Coríntios 11:3–16: uma análise da orientação argumentativa e do ponto de vista,” *Revista de Estudos da Linguagem* 31.3: 1404–1446. DOI `10.17851/2237-2083.31.3.1404-1446`.

The official UFMG journal page identifies the author (Universidade Federal do Rio Grande do Norte) and directly states the method and result.

Route:

- https://periodicos.ufmg.br/index.php/relin/article/view/55158

## 7.2 Method and direct abstract result

Costa approaches the question **linguistically**, combining:

- Textual Discourse Analysis;
- Discursive Traditions;
- Argumentative Semantics;
- argumentative orientation and point of view.

The official abstract says the analysis finds antagonistic Pauline and Corinthian points of view and concludes that **vv.4–9 function as quotations not endorsed by the apostle**.

This is a valuable independent method because it is not merely another confessional replay of Peppiatt.

However:

```text
COSTA_VV4_9_UNENDORSED_QUOTATION = B1_PUBLISHED_LINGUISTIC_PROPOSAL
LARGE_QUOTATION_REFUTATION_CURRENT_GRADE = D_C_LOW // no automatic promotion
```

Why no promotion yet:

1. only the official abstract/result was directly inspected in this pass;
2. the full argumentative chain has not yet been adversarially audited against discourse markers, vv.2/10/11/16 and known Pauline quotation practice;
3. the current registry’s low grade is based on broader textual/discourse controls, so one new B1 proposal is evidence for re-opening a stress test, not a license to overwrite the registry.

### Action

Create a future adversarial mini-matrix:

```text
COSTA_2023/24
vs PEPPIATT_2015
vs SHOEMAKER_1987
vs MARSHALL_2019
vs CURRENT_VERSE_AUDIT
```

and test exact boundaries: `vv4–9`, `vv3–10`, or modified traditions without speaker change.

---

# 8. Luis Josué Salés 2024 — new current ideological/rhetorical alternative, not a neutral control

## 8.1 Verified source

Luis Josué Salés, “Paul and Pseudo-Paul: Authorship, Ideology, and the Difference of Androprimacy,” *Religions* 15.9 (2024): 1141. DOI `10.3390/rel15091141`.

Official open article:

- https://www.mdpi.com/2077-1444/15/9/1141

## 8.2 Relevant position

Salés coins/uses `androprimacy` for totalizing male precedence and reads 1 Cor 11:3–10 as a Corinthian subordinating logic that Paul challenges in 11:11–16. He explicitly treats the large-quotation/refutation model as the framework he finds plausible.

This is useful as evidence that the quotation model remains a **live published 2024 alternative**.

It is not a neutral linguistic control: the article has a broader ideological/authorship and women’s-ordination agenda, and its 1 Cor 11 segmentation is an adopted premise/argument, not a textual discovery.

```text
SALES_2024_QUOTATION_MODEL = REAL_PUBLISHED_B1_ALTERNATIVE
SALES_ANDROPRIMACY = AUTHOR_CONCEPTUAL_FRAME
SALES_DOES_NOT_BY_ITSELF_RAISE_QUOTATION_GRADE = true
```

---

# 9. Christie Goulart Chadwick 2022 — recent Portuguese/Brazilian hair-only proposal

## 9.1 Verified source

Christie Goulart Chadwick, “Véu ou penteado? Um estudo de 1 Coríntios 11 e o uso do véu na adoração / Headdress or Hairstyle? A Study of 1 Corinthians 11 and the Use of the Veil in Worship,” *Kerygma* 17.1 (2022), e01592. DOI `10.19141/1809-2454.kerygma.v17.n1.pe01592`.

Official journal route:

- https://unasp.emnuvens.com.br/kerygma/article/view/1592

The article is CC BY 4.0 and explicitly argues for a hairstyle rather than material-headcovering reading, appealing to archaeological and textual evidence and the absence of an overt noun “veil” in the Greek passage.

## 9.2 Calibration against current lexical controls

This is a genuine recent scholarly representative of the hair-only camp, useful especially because the uploaded dump did not contain it.

But the project already has stronger direct lexical controls:

```text
KATA_KEPHALES != OVERT_NOUN_VEIL
AND
AKATAKALYPTOS / COVERING_IDIOM + PRIMARY_PARALLELS -> MATERIAL_COVERING_B_HIGH_LEADING
```

Therefore:

```text
CHADWICK_HAIR_ONLY = REAL_PUBLISHED_ALTERNATIVE
HAIR_ONLY_WHOLE_PASSAGE = C_SERIOUS_ALTERNATIVE // unchanged
MATERIAL_COVERING = B_HIGH_LEADING // unchanged
```

Recency and archaeological illustration do not override the existing Greek-idiom audit.

---

# 10. Callie Callon 2024 — current open-access control remains the strongest recent address-scope source

Callie Callon, “Authority Over Whose Head? Did Paul Instruct Wives or All Women to Cover Their Heads (1 Corinthians 11:2–16)?,” *Harvard Theological Review* 117.4 (2024): 699–719. DOI `10.1017/S0017816024000300`.

Cambridge open access directly states her two neglected controls:

- slaves in the Corinthian community and their limited autonomy over sexuality/hair;
- ancient readings of Genesis material as addressing marriage rather than generic creation.

Her tentative conclusion: the exhortations more likely target free(d) married women.

Route:

- https://www.cambridge.org/core/journals/harvard-theological-review/article/authority-over-whose-head-did-paul-instruct-wives-or-all-women-to-cover-their-heads-1-corinthians-11216/5D602D820F9CA0E6C55906BDF68466ED

Current registry remains correctly calibrated:

```text
WIVES_VS_ALL_WOMEN = OPEN_B_C
CALLON_FREE_D_MARRIED_WOMEN_MODEL = B_C_SERIOUS_CURRENT_MODEL
```

No change.

---

# 11. Garland 2025 and Ciampa/Rosner — direct-book target status after this pass

## 11.1 Garland 2025

Official Baker/current digital catalog routes verify edition metadata and the fact of substantial updating, but this pass still did **not** obtain quote-safe direct text for the full current 11:2–16 section and notes.

```text
GARLAND_2025_SECTION = HOLD_FULL_SECTION
GARLAND_2003 != GARLAND_2025
NO_2025_POSITION_FROM_PRE_2025_SECONDARY_SOURCE = true
```

No web summary is allowed to fill this gap.

## 11.2 Ciampa/Rosner 2010

The book and section are bibliographically secure. Multiple independent secondary quotation chains converge on:

- p.509: their `κεφαλή` reading has a real authority/hierarchy component and cannot be reduced to “preeminence only”;
- p.533: they can describe the woman as having authority to pray and prophesy.

But the complete direct book bytes for pp.503–540 + notes remain unavailable in this pass.

```text
CIAMPA_ROSNER_P509_AUTHORITY_COMPONENT = STRONG_SECONDARY_ATTESTATION
CIAMPA_ROSNER_P533_WOMAN_AUTHORITY = STRONG_SECONDARY_ATTESTATION
CIAMPA_ROSNER_DIRECT_BOOK_SECTION = DETAIL_HOLD
```

No quote-safe promotion.

---

# 12. What changes in the research map

## 12.1 New verified acquisitions

```text
NEWBERRY_2019 = ADD
  function: 1 Esdras 4 + Genesis intertext / v10 authority / vv11-12 counterbalance

COSTA_2023_2024 = ADD
  function: independent linguistic support for unendorsed quotation vv4-9

SALES_2024 = ADD
  function: current rhetorical/ideological quotation-model reception

CHADWICK_2022 = ADD
  function: current Brazilian hair-only/archaeological proposal

BERGLUND_2025 = KEEP_WITH_TIGHTER_PROVENANCE
  function: peer-reviewed 11-14 prophecy/social-context work; documented Nõmmik citation

MARSHALL_2019 = VERIFIED
  function: two modified traditions, NOT automatically large quotation

HOOKER_1964 = SOURCE_SPECIFIC_UPGRADE
  function: active exousia argument + distinct angel-worship danger proposal

FITZMYER_1957 = SOURCE_SPECIFIC_UPGRADE
  function: direct Cambridge Qumran/heavenly-angel extract + active exousia apparatus
```

## 12.2 No core claim-grade reversal

```text
CORE_GRADE_REVERSALS = 0
```

The current registry remains controlling.

The most interesting **future stress test** is now the large quotation/refutation hypothesis, because it has at least three distinguishable modern forms:

1. `Shoemaker/Peppiatt/Salés` — larger Corinthian quotation/refutation;
2. `Costa` — vv4–9 as unendorsed quotation on linguistic discourse grounds;
3. `Marshall` — modified Pauline traditions with different perspectives, without requiring a speaker-change theory.

These should not be collapsed into one “egalitarian quotation model.”

---

# 13. Next high-value actions

```text
P0_1 = Garland 2025 complete pp.468-493 + notes, direct current edition
P0_2 = Ciampa/Rosner pp.503-540 + notes, direct book
P0_3 = Nõmmik DiVA full dissertation bytes, edition-pinned locators
P0_4 = Costa full article adversarial discourse-marker audit
P1_1 = Hooker complete 410-416 if lawful full text route opens
P1_2 = Gundry-Volf full 151-171
P1_3 = Olson/Fantham Roman female dress/portrait direct sections
P1_4 = rights-safe visual source ledger for capite-velato statues/coins/reliefs
```

For visual work, keep **object identity, museum/archive source, date, findspot/provenance, rights and exact interpretive function** as separate fields. An image of a covered Roman figure demonstrates a depicted practice; it does not by itself prove Paul’s exact local target.

---

# 14. Publication boundary

```text
PRODUCT_WRITE = false
UI_IMPLEMENTATION = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
DIRECT_QUOTE_PROMOTION = false unless direct object + locator + context are verified
RECENT_SOURCE != AUTOMATIC_UPGRADE
```
