# 1 Коринфянам 11:2–16 — deep verification of the second agent-search dump

**Дата:** 2026-08-10  
**Статус:** `SECOND-AGENT-DUMP / 48PLUS-TARGET-DEEP-VERIFICATION / SOURCE-SPECIFIC-RECONCILIATION / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Purpose and method

Three new user-supplied agent-search files were treated as a **discovery feed**, not as authority.

This pass independently re-ran **48+ verification targets** across publisher pages, university repositories, journal abstracts/full text where available, current-edition reviews, Oxford Academic chapter abstracts, and institutional dissertation records.

```text
AGENT_OUTPUT = DISCOVERY_ONLY
AGENT_CORRECTION != VERIFIED_CORRECTION
SECONDARY_QUOTE != DIRECT_BOOK_TEXT
FIRST_EDITION_POSITION != CURRENT_EDITION_POSITION
PUBLISHED_ALTERNATIVE != EQUALLY_PROBABLE_ALTERNATIVE
NO_UPDATE_IF_NO_REAL_DELTA = true
```

The purpose is not to produce another synthetic commentary. It is to answer four questions:

1. Which new agent claims are actually source-backed?
2. Which earlier project statements need source-specific tightening?
3. Did any **claim grade** change?
4. Which newly located sources deserve a permanent control card?

Main result:

```text
CORE_GRADE_REVERSALS = 0
SOURCE_SPECIFIC_REFINEMENTS = YES
NEW_DIRECT_SOCIAL_MYTH_CONTROL = MONTIER_2015
NEW_OFFICIAL_NOMMIK_AUTHOR_SUMMARY_CONTROL = YES
FINNEY_ABSTRACT_RECONSTRUCTION = DIRECTLY_PINNED
CIAMPA_ROSNER_KEPHALE_AUTHORITY_COMPONENT = SECONDARY_ATTESTED_STRONG
CIAMPA_ROSNER_V10_WOMAN_AUTHORITY = SECONDARY_ATTESTED_STRONG
MURPHY_OCONNOR_HUMAN_MESSENGERS = DIRECT_OXFORD_ABSTRACT_PUBLISHED_ALTERNATIVE
```

No conservative-core synthesis is reversed.

---

# 1. Fee Revised 2014 — bibliographic and exegetical cleanup

## 1.1 Formal edition label

Eerdmans and current academic reviews identify the book as:

> Gordon D. Fee, *The First Epistle to the Corinthians*, **Revised Edition**, NICNT, 2014.

A review may colloquially call it a “second edition”, but the safe formal bibliographic label is **Revised Edition**.

```text
FEE_2014_FORMAL_EDITION_LABEL = REVISED_EDITION
FEE_2014_FORMAL_CITATION_AS_2ND_ED = AVOID
```

## 1.2 Current-edition position on covering

William W. Klein’s Denver Seminary review of the 2014 revision explicitly says Fee **again** chooses some kind of external covering/veil rather than a reference to short or loosed hair.

Same review also reports:

- `κεφαλή` = source/source of life/origin rather than hierarchy;
- woman’s `ἐξουσία` = freedom/right to choose over her head;
- a substantial addendum on the head-covering literature follows 11:6.

Earlier verification pinned the addendum to **pp.565–567**.

```text
FEE_EXTERNAL_COVERING = VERIFIED_CURRENT_EDITION_REVIEW
FEE_KEPHALE_SOURCE = VERIFIED_CURRENT_EDITION_REVIEW
FEE_EXOUSIA_ACTIVE_RIGHT = VERIFIED_CURRENT_EDITION_REVIEW
FEE_HAIR_ONLY_PRIMARY_POSITION = REJECTED_MISATTRIBUTION
```

This does not eliminate the P0 requirement to read the complete revised-edition section and notes before promoting direct quotations.

### Verified route

- Denver Journal / Denver Seminary, review of Fee Revised 2014: https://denverjournal.denverseminary.edu/the-denver-journal-article/the-first-epistle-to-the-corinthians-rev-ed/

---

# 2. Garland 2025 — strict 2003→2025 firewall

## 2.1 Series editors are not volume editors

Baker’s own catalog describes:

```text
1 Corinthians, 2nd ed. — David E. Garland
BECNT — Robert W. Yarbrough and Joshua W. Jipp, series editors
```

Therefore a normal bibliographic record should not represent Yarbrough/Jipp as editors of Garland’s individual volume.

```text
YARBROUGH_JIPP_ROLE = SERIES_EDITORS
YARBROUGH_JIPP_AS_VOLUME_EDITORS = REJECTED_BIBLIOGRAPHIC_MISATTRIBUTION
```

## 2.2 Publication metadata

Baker’s 2025/2026 catalogs verify:

- second edition;
- 2025 publication;
- ISBN 9781540962607;
- print catalog page count 872;
- updated throughout for recent scholarship.

Digital platforms may expose different digital page counts. Print pagination controls citation locators.

## 2.3 Current section locator remains

Official TOC already established:

```text
11:2–16 = pp.468–493
11:17–34 begins p.494
```

## 2.4 The critical firewall

The new agent files correctly noticed a recurring methodological error: secondary literature published before Garland 2025 often cites **Garland 2003**, and those quotations/page numbers cannot be relabeled as Garland 2025.

Thus:

```text
GARLAND_2003_POSITION != VERIFIED_GARLAND_2025_POSITION
GARLAND_2003_PAGE_LOCATOR != GARLAND_2025_PAGE_LOCATOR
CALLON_2024_CITATION_TO_GARLAND != DIRECT_EVIDENCE_FOR_GARLAND_2025
```

Until pp.468–493 + notes are directly read, statements about Garland’s exact 2025 handling of `κεφαλή`, `ἐξουσία`, angels, palla/stola, or legal/social status remain HOLD unless independently stated by the publisher or a current-edition review.

### Verified routes

- Baker Academic Fall 2025 catalog: https://online.flippingbook.com/view/193525704/12/
- Baker Academic Spring 2026 catalog: https://online.flippingbook.com/view/583246729/30/

---

# 3. Ciampa/Rosner — reconcile `κεφαλή` and `ἐξουσία` without forcing one label

This is the most useful correction in the new agent material.

## 3.1 `κεφαλή` in v3

The previous shorthand “Ciampa/Rosner = merely preeminence” is too weak.

Multiple independent secondary sources cite **Ciampa/Rosner p.509** for a formulation whose logic is:

- `head` may carry a prominent/preeminent nuance;
- nevertheless the flow of the argument assumes an honor/status hierarchy;
- in context the relationship includes an authority component.

The exact sentence is currently **secondary-attested**, not direct-book-verified in this harness.

```text
CIAMPA_ROSNER_KEPHALE_PREEMINENCE_ONLY = REJECTED_OVERSIMPLIFICATION
CIAMPA_ROSNER_KEPHALE_AUTHORITY_COMPONENT = STRONG_SECONDARY_ATTESTATION
CIAMPA_ROSNER_P509_DIRECT_TEXT = HOLD
```

This is fully compatible with the project’s existing broader grade:

```text
KEPHALE_HEADSHIP_AUTHORITY = B_LEADING
KEPHALE_SOURCE_ONLY = C_VIABLE
```

No grade change is required.

## 3.2 `ἐξουσία` in v10

The new agent files also correctly distinguish v3 from v10.

Independent secondary citations to **Ciampa/Rosner pp.530–533** report that they can speak of the woman as having authority to pray and prophesy, even while their broader reading retains ordered gender relations.

At the same time, Blomberg’s Denver review reports that Ciampa/Rosner supply `sign of` before `authority`, and he explicitly objects to that supplied phrase because the Greek construction strongly pulls toward the grammatical subject exercising authority/control.

Therefore the safe author-specific description is:

```text
CIAMPA_ROSNER_V10 = WOMAN_AUTHORITY/RIGHT_LANGUAGE_SECONDARY_ATTESTED
CIAMPA_ROSNER_SIGN_OF = REPORTED_BY_BLOMBERG
CIAMPA_ROSNER_EXACT_SYNTHESIS = DETAIL_HOLD_DIRECT_BOOK
```

The important conceptual point is not contradictory:

```text
RELATIONAL_ORDER_IN_V3
DOES_NOT_ENTAIL
PASSIVE_EXOUSIA_IN_V10
```

A commentator can affirm relational asymmetry/order in v3 and still treat the woman as a real bearer of liturgical authority/right in v10.

## 3.3 Source-hygiene rule

Do not write either of the following as settled:

> “Ciampa/Rosner are simply preeminence-only.”

or

> “Ciampa/Rosner simply read v10 as husband’s authority over the woman.”

Both flatten a more complex position.

### Current secondary routes

- Clearly Reformed, citing C/R p.509: https://clearlyreformed.org/4-questions-about-headship-and-head-coverings/
- Denver Journal review of C/R: https://denverjournal.denverseminary.edu/the-denver-journal-article/the-first-letter-to-the-corinthians/

P0 remains: **Ciampa/Rosner pp.503–540 + notes**.

---

# 4. Curtis E. Montier 2015 — direct control against the shaved-prostitute myth

This is the strongest genuinely new source discovered in the second dump.

## 4.1 Source status

Curtis E. Montier, *Let Her Be Shorn: 1 Corinthians 11 and Female Head Shaving in Antiquity*.

- MA thesis in History;
- University of North Texas;
- December 2015;
- 67 pages;
- DOI: 10.12794/metadc822830;
- open full text through UNT Digital Library.

## 4.2 What it directly establishes for our project

Montier began with a popular modern claim that an ancient woman with a shaved head was a prostitute, probably a temple prostitute.

His survey concludes that the evidence does **not** support treating shaved heads as the marker of temple prostitution. The UNT abstract states that Greek erotic art depicts prostitutes with long and short hair, covered and uncovered, while providing no artistic example establishing shaved prostitutes as the norm.

His thesis therefore provides a direct modern historical control for a project gate that was already present but previously depended on more distributed evidence.

```text
SHAVED_HEAD = TEMPLE_PROSTITUTE_MARKER = REJECTED_UNIVERSAL
SHAVED_WOMAN = PROSTITUTE = REJECTED_UNIVERSAL
PROSTITUTE_HAIR_STATE = VARIABLE_IN_SURVIVING_ARTISTIC_EVIDENCE
```

This **strengthens the evidence behind an existing no-overclaim rule**; it does not alter the exegesis of vv5–6 by itself.

## 4.3 Montier’s positive adultery reconstruction must also be calibrated

Montier argues that adultery punishment is the best explanation for the shame of female shaving.

That is his historical conclusion, not an A-level universal fact.

```text
MONTIER_ADULTERY_RECONSTRUCTION = C_TO_B_C_HISTORICAL_PROPOSAL
SHAVED_WOMAN_UNIVERSALLY_ADULTERESS = REJECTED
```

The project must not replace one universal myth (“prostitute”) with another (“adulteress”).

### Verified route

- UNT Digital Library: https://digital.library.unt.edu/ark:/67531/metadc822830/

---

# 5. Nõmmik — official institutional summary now pinned more strongly

The prior Nõmmik audit was deliberately pre-fulltext and already kept the whole model at C serious reconstruction. The new pass adds stronger institutional metadata and a direct author-summary control.

## 5.1 Official defense record

EHS / Enskilda Högskolan Stockholm records:

- dissertation defense: **17 January 2025**;
- title: *Robes, Romans, and Rituals in First Corinthians: Paul and the Conflict over Head-Coverings*;
- opponent: Richard E. DeMaris;
- institutional URN route: `urn:nbn:se:ths:diva-2600`.

## 5.2 Official author-level summary

The EHS page directly attributes to Nõmmik the claim that his study is, to his knowledge, the first extensive scholarly interpretation of 1 Cor 11:2–16 with Roman `capite velato` at the center.

The institutional summary also explicitly states his reconstructed conflict:

- Roman ritual head covering was familiar;
- some Corinthians sought a uniform practice;
- married women were pressed to remove what was on their heads to match uncovered men;
- Paul argues that covered prayer is shameful for men but not for women;
- women may retain coverings and hair accessories;
- the usual “rebellious women” story is not the only possible reconstruction.

These are no longer merely retailer paraphrases; they are direct institutional/author-summary evidence for **what Nõmmik’s model is**.

They do **not** prove that the reconstructed events actually happened.

```text
NOMMIK_MODEL_DESCRIPTION = A_AUTHOR/INSTITUTIONAL
NOMMIK_HIDDEN_CORINTH_EVENTS = C_SERIOUS_RECONSTRUCTION
ROMAN_CAPITE_VELATO_BACKGROUND = A
V4_EXACT_CAPITE_VELATO = B_C
```

No grade change.

### Verified route

- EHS defense page: https://ehs.se/kalender/disputation-aldar-nommik/

---

# 6. Mark Finney 2010 — exact reconstruction now pinned from journal abstract

The SAGE/JSNT abstract gives unusually precise direct evidence for Finney’s model.

It says the paper reads 1 Cor 11:2–16 through honor/shame and argues approximately:

- higher-status male Corinthians use head attire to maintain status distinctions;
- Paul insists on female head coverings to safeguard community honor;
- potential presence of unbelievers in worship matters to that reconstruction.

This means the project can safely represent **Finney’s own model** at this level without depending on tertiary summaries.

```text
FINNEY_HIGH_STATUS_MALE_HEAD_ATTIRE = DIRECT_ABSTRACT_MODEL
FINNEY_FEMALE_COVERING_COMMUNITY_HONOR = DIRECT_ABSTRACT_MODEL
FINNEY_NONBELIEVER_PRESENCE = DIRECT_ABSTRACT_MODEL
```

But Finney remains one historical reconstruction among several. It does not establish the exact Corinthian trigger as A.

```text
EXACT_CORINTH_TRIGGER = RECONSTRUCTION_LAYER
FINNEY_MODEL = B_C_SERIOUS_HISTORICAL_RECONSTRUCTION
```

### Verified route

- Mark Finney, JSNT 33.1 (2010), DOI 10.1177/0142064X10376002: https://journals.sagepub.com/doi/10.1177/0142064X10376002

---

# 7. Murphy-O’Connor — human messengers are a real published proposal, not an AI invention

Oxford Academic’s official abstract for Jerome Murphy-O’Connor, “1 Corinthians 11:2–16 Once Again,” pp.159–181, states that he:

- accepts an active/control reading of v10;
- takes that as requiring proper arrangement of the woman’s hair;
- suggests that `angels` may be **human messengers from other churches** because he finds heavenly-angel interpretations too subjective;
- revisits `κεφαλή` options and Corinthian dress evidence.

This is direct publisher-level evidence for the **existence and content of the alternative**.

```text
HUMAN_MESSENGERS_MODEL_EXISTS = A_PUBLICATION_STATUS
MURPHY_OCONNOR_HUMAN_MESSENGERS = DIRECT_OXFORD_ABSTRACT
HUMAN_MESSENGERS_LIKELIHOOD = LOW
```

The existence of a serious published advocate does not, by itself, raise the evidential fit of the model. Same-letter Pauline angel controls still strongly favor celestial beings.

Therefore the current project grade can remain:

```text
HUMAN_MESSENGERS_V10 = D_C_LOW
```

with a refined note:

> `published major-scholar alternative; low local Pauline fit`, not “internet fringe”.

### Verified route

- Oxford Academic, ch.11 abstract: https://academic.oup.com/book/8618/chapter-abstract/154575789

---

# 8. `φύσις` — the new agent files converge with, rather than overturn, the primary-corpus audit

The new files correctly reject the crude binary:

```text
PHYSIS = BIOLOGY_ONLY
vs
PHYSIS = ARBITRARY_LOCAL_CUSTOM_ONLY
```

The project had already tested Pauline usage, Numbers/Dio exceptions and Epictetus and reached:

```text
PHYSIS_SEXED_NATURALIZED_PROPRIETY = B_HIGH_LEADING
EXACT_BIOLOGY_CULTURE_MIX = B_C
```

The new agent language “culturally embodied perception of natural sexual distinction” is a useful prose paraphrase of that existing calibration, not a new grade.

No update to the claim registry is needed.

---

# 9. Female portraiture / veiling — useful caution remains, no universal rule

The new files push the archaeology problem appropriately:

- prescriptive literature can expect female covering in particular social/ritual situations;
- elite portraiture can show respectable women bareheaded;
- Roman status, marriage, freedom/slavery, location and ritual context matter;
- artistic portraiture is not a census of ordinary dress behavior.

Therefore the existing gates remain correct:

```text
ROMAN_FEMALE_PORTRAITURE != ONE_UNIVERSAL_VEIL_RULE
UNVEILED_WOMAN != UNIVERSALLY_PROSTITUTE
IDENTICAL_GARMENT_FORM_ACROSS_ALL_WOMEN = UNPROVED
```

The new evidence does not justify the opposite universal claim “respectable women normally went bareheaded.”

Olson/Fantham remain high-value background acquisition targets if a direct full section becomes accessible, but the project does not need to ask the user for them while agent-side routes remain available.

---

# 10. `περιβόλαιον` Martin–Goodacre — no change

The second dump accurately describes the publication history:

- Troy W. Martin 2004 proposed the physiology/testicle reading;
- Mark Goodacre 2011 challenged it;
- Martin 2013 replied.

But publication in JBL demonstrates only that the proposal deserved scholarly discussion, not that the lexical meaning “testicle” becomes probable.

The independent LXX/Hebrews lexical controls remain stronger for normal wrap/covering/garment semantics.

```text
PERIBOLAION_NORMAL_COVERING_SEMANTICS = A_LEXICAL
PERIBOLAION_TESTICLE_THEORY = D_C_LOW
```

No grade change.

---

# 11. Angels — preserve identity/function separation

The new agents sometimes move back toward a bundled claim such as “all four = good angels as guardians of order.” That remains too compressed.

Current safe calibration still separates:

```text
ANGELS_EXPLICITLY_INVOKED = A_TEXT
HEAVENLY_HOLY_ANGELS_REFERENT = B_HIGH_LEADING
ANGELS_AS_COSMIC_WITNESSES/PRESENT_ASSEMBLY = B_LEADING
EXACT_ANGELIC_FUNCTION = B_C
WATCHERS = C_SERIOUS_ALTERNATIVE
HUMAN_MESSENGERS = D_C_LOW_PUBLISHED_ALTERNATIVE
```

Stuckenbruck’s cosmic-order approach and Murphy-O’Connor’s human-messenger proposal are useful precisely because they pressure different layers without collapsing identity and function.

---

# 12. v16 — agent correction accepted, but no new grade

The third agent file correctly retracts an overstatement found in earlier AI synthesis:

> `συνήθεια` does not by itself mean “optional cultural custom”.

Our direct v16 audit had already established:

```text
SYNĒTHEIA_CUSTOM/PRACTICE = A_LEXICAL
V16_TRANSLOCAL_CHURCH_PRACTICE_APPEAL = A_TEXT
V16_NORMATIVE_FORCE = B_HIGH
V16_NO_CONTRARY/ALTERNATIVE_PRACTICE = B_LEADING
V16_EXACT_CUSTOM_REFERENT = B_C
V16_CUSTOM_OF_CONTENTION = C_VIABLE
V16_CANCELS_VV2_15 = D_C_LOW
```

No update required.

---

# 13. Accepted deltas from the three new agent files

| Delta | Verdict | Project action |
|---|---|---|
| Fee formal title = Revised Edition | `ACCEPT` | bibliographic gate |
| Fee = source/origin, external covering, active right | `ACCEPT_CURRENT_ED_REVIEW` | reinforces existing source-specific map |
| Garland Yarbrough/Jipp = series editors | `ACCEPT_OFFICIAL` | bibliographic correction |
| Garland 2003 claims cannot be relabeled 2025 | `ACCEPT` | hard edition firewall |
| C/R `κεφαλή` has real authority component | `ACCEPT_STRONG_SECONDARY_ATTESTED` | reject “preeminence-only” shorthand |
| C/R v10 can include woman’s liturgical authority/right | `ACCEPT_STRONG_SECONDARY_ATTESTED` | keep distinct from v3 order |
| Montier thesis exists/open | `ACCEPT_DIRECT` | new social-myth control card |
| shaved woman = temple prostitute | `REJECT_UNIVERSAL` | strengthened no-overclaim gate |
| shaved woman = adulteress universally | `REJECT_UNIVERSAL` | do not replace one myth with another |
| Nõmmik official model summary | `ACCEPT_DIRECT_INSTITUTIONAL` | strengthen model-description provenance |
| Nõmmik hidden events actually happened | `NO_PROMOTION` | whole model remains C serious |
| Finney high-status male/status model | `ACCEPT_DIRECT_ABSTRACT` | model description upgraded, likelihood not A |
| Murphy-O’Connor human messengers | `ACCEPT_DIRECT_OXFORD_ABSTRACT` | published-low alternative, no likelihood promotion |
| physis = culturally embodied sexed propriety | `NO_CHANGE` | already current B-high leading synthesis |
| all respectable women always veiled | `REJECT_UNIVERSAL` | existing gate retained |
| v16 = optional custom | `REJECT_OVERCLAIM` | existing v16 audit retained |

---

# 14. Agent claims explicitly blocked after verification

```text
FEE_KEPHALE_PREEMINENT = FALSE_MISATTRIBUTION
FEE_2014_PRIMARY_HAIR_ONLY = FALSE_MISATTRIBUTION
GARLAND_2025_POSITION_PROVED_BY_2003_PAGES = FALSE
GARLAND_2025_POSITION_PROVED_BY_CALLON_2024 = FALSE
YARBROUGH_JIPP_VOLUME_EDITORS = FALSE
CIAMPA_ROSNER_PREEMINENCE_ONLY = TOO_SIMPLE
CIAMPA_ROSNER_PASSIVE_HUSBAND_AUTHORITY_ONLY_IN_V10 = TOO_SIMPLE
ALL_FOUR_COMMENTATORS_HAVE_IDENTICAL_EXOUSIA = FALSE
ALL_FOUR_COMMENTATORS_HAVE_IDENTICAL_ANGEL_MODEL = FALSE
ALL_RESPECTABLE_ANCIENT_WOMEN_ALWAYS_VEILED = FALSE
SHAVED_WOMAN = TEMPLE_PROSTITUTE = FALSE_UNIVERSAL
SHAVED_WOMAN = ADULTERESS = FALSE_UNIVERSAL
JBL_PUBLICATION = PROBABILITY_PROMOTION = FALSE
PHYSIS = BIOLOGY_ONLY = FALSE
PHYSIS = OPTIONAL_LOCAL_FASHION_ONLY = FALSE
SYNĒTHEIA = OPTIONAL = FALSE
```

---

# 15. Deep-search result: what actually remains high-value

After the second 48+ target pass, the highest-value unresolved items are still **direct primary/current-edition access**, not more web paraphrase accumulation.

## P0 direct commentary holds

```text
Thiselton NIGTC 2000: pp.800–847 + notes
Fee NICNT Revised 2014: approx pp.542–586 + notes; pp.565–567 addendum explicitly included
Garland BECNT 2nd ed. 2025: pp.468–493 + notes
Ciampa/Rosner PNTC 2010: pp.503–540 + notes
```

## P1 specialist full-text targets if agent-accessible

- Nõmmik full DiVA dissertation bytes, especially v10/angels and exact causal reconstruction chapters;
- Hooker 1964 full article;
- Gundry-Volf full chapter/article;
- Olson 2008 exact female portrait/dress discussion;
- Fantham 2008 “Covering the Head at Rome: Ritual and Gender” full chapter;
- direct Ciampa/Rosner pp.509, 530–533 to replace secondary quotation chains.

## What is no longer worth chasing merely for volume

- more popular websites repeating “prostitute/shaved head” folklore;
- more unsourced summaries of Garland 2025;
- more generic complementarian/egalitarian labels without claim-level evidence;
- more secondary summaries of the same Martin/Goodacre controversy;
- more generic “angels were present in worship” statements that do not distinguish referent from exact function.

---

# 16. Current synthesis after this pass

```text
CORE_GRADE_REVERSALS = 0
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
KEPHALE_HEADSHIP_AUTHORITY = B_LEADING
KEPHALE_SOURCE_ONLY = C_VIABLE
WIVES_VS_ALL_WOMEN = OPEN_B_C
EXOUSIA_WOMAN_SUBJECT = A_SYNTAX
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH
EXOUSIA_EXACT_REFERENT = B_C
HEAVENLY_HOLY_ANGELS_REFERENT = B_HIGH_LEADING
ANGELS_COSMIC_WITNESS/PRESENT_ASSEMBLY = B_LEADING
EXACT_ANGELIC_FUNCTION = B_C
WATCHERS = C_SERIOUS_ALTERNATIVE
HUMAN_MESSENGERS = D_C_LOW_PUBLISHED_ALTERNATIVE
ROMAN_CAPITE_VELATO_BACKGROUND = A
V4_EXACT_CAPITE_VELATO = B_C
EXACT_CORINTH_TRIGGER = RECONSTRUCTION_LAYER
PHYSIS_SEXED_NATURALIZED_PROPRIETY = B_HIGH_LEADING
V16_TRANSLOCAL_APPEAL = A_TEXT
V16_NORMATIVE_FORCE = B_HIGH
V16_EXACT_REFERENT = B_C
```

---

# 17. Publication boundary

```text
DO_NOT_REQUEST_FROM_USER_IF_AGENT_CAN_ACCESS = true
PRODUCT_WRITE = false
UI_IMPLEMENTATION = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
DIRECT_QUOTE_PROMOTION = false unless direct locator/object verified
```
