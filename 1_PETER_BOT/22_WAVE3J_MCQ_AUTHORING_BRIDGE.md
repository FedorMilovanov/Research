# 1 Peter Wave 3.0j — MCQ Authoring Bridge

**Status:** `RESEARCH PROTOTYPES / NOT PRODUCTION / NOT RANKING`

Wave 3.0j tests whether the research control plane can actually generate good four-option questions without losing its evidence boundaries.

It deliberately does **not** add new theological claims. It converts 32 already research-ready candidate nuclei into full MCQ prototypes:

- 16 from Chapter 4;
- 16 from Chapter 5;
- four options each;
- one explicitly keyed answer;
- all `competitive_candidate=false`;
- source authority inherited from the effective candidate after applying all Wave-3 override files.

## Why prototypes are separate from candidates

The 144-question candidate bank remains the research authority for claim nuclei.

The 32 MCQ prototypes are an **authoring bridge**:

```text
RESEARCH CLAIM NUCLEUS
      ↓
MCQ PROTOTYPE
      ↓
EDITORIAL REVIEW
      ↓
FINAL FOUR-OPTION BOT CARD
      ↓
ONLY THEN ranking/production decision
```

A prototype must never silently replace its source candidate.

## Answer-key contract

The 32 author-time correct positions are:

```text
2,0,3,1,1,3,0,2,
3,2,1,0,0,1,2,3,
2,3,1,0,1,0,3,2,
0,2,1,3,3,1,2,0
```

Distribution:

```text
0 = 8
1 = 8
2 = 8
3 = 8
```

Required invariants:

- all four positions used;
- exact 8/8/8/8 balance;
- no run of three identical correct positions;
- no simple repeating `0,1,2,3` cycle;
- no runtime randomness used to hide weak authoring;
- semantic answer identity must survive any later editorial option reordering.

This generalizes the Chapter-3 B/C/D lesson: answer-key leakage is an **authoring-quality defect**, not merely a runtime implementation detail.

## Distractor architecture

Wrong options are intended to represent nearby misconceptions, for example:

- morphology → theology overreach;
- historical plausibility → universal biography;
- OT reuse → verbatim quotation;
- suffering → automatic righteousness;
- participation in Christ's suffering → co-atonement;
- leadership → domination;
- humility → unlimited submission to abuse;
- devil resistance → invented ritual technique;
- edition-specific reading → all-manuscripts claim.

Reject distractors that are wrong only because they are absurd or completely unrelated.

## Coverage selection

### Chapter 4 prototypes

Selected nuclei cover:

- 4:1 Christ's suffering / `πέπαυται`;
- 4:2 human desires vs God's will;
- 4:4 social rupture;
- 4:6 morphology without disputed chronology closure;
- 4:7 eschatology → prayerful sobriety;
- 4:8 direct text and Prov 10:12 reuse distinction;
- 4:9 hospitality;
- 4:10 gifts/stewardship;
- 4:12 fiery trial vocabulary;
- 4:13 participation without co-atonement;
- 4:15 wrongdoing vs suffering for Christ;
- 4:16 Christian-name response;
- 4:18 very close Prov 11:31 LXX reproduction;
- 4:19 faithful Creator.

### Chapter 5 prototypes

Selected nuclei cover:

- 5:1 Peter's self-description;
- 5:2 shepherding and morphology;
- 5:2–3 ethical leadership contrasts;
- 5:4 Chief Shepherd;
- 5:5 humility / Prov 3:34;
- 5:6 humility under God's hand;
- 5:7 anxiety participle;
- 5:8–9 sobriety and resistance;
- 5:10 SBLGNT four-verb sequence with edition caveat inherited from override;
- 5:12 purpose statement;
- 5:13 `συνεκλεκτή` and Mark.

## Deliberate exclusions

Wave 3j does not prototype questions whose keyed answer would require choosing an unresolved HOLD:

- official project interpretation of 4:6;
- exact 4:14 official apparatus closure;
- final Malachi-3 classification;
- official ECM closure of 5:2 variants;
- official ECM reasoning for 5:12.

It also avoids using 4:16 as a simple one-edition textual question unless the edition is explicitly named.

## Source inheritance rule

Every prototype records:

`source_contract = inherit effective candidate source_minimum after all Wave 3 overrides`

That means authoring must resolve, in order:

1. original candidate;
2. any later candidate-specific override;
3. later source upgrades/quorum additions;
4. then the prototype.

A prototype cannot weaken a `do_not_claim` boundary or promote a source's inspection depth.

## Corpus accounting

Wave 3j adds **32 prototypes**, not 32 new research candidate IDs.

Therefore the research candidate corpus remains:

- **144 candidates**;
- **72 Chapter 4**;
- **72 Chapter 5**;
- **52 READY**;
- **86 READY_NONCOMPETITIVE**;
- **6 HOLD**.

Separately:

- **32 MCQ prototypes**;
- 16 Chapter 4 + 16 Chapter 5;
- correct-position distribution exactly 8/8/8/8.

`MCQ_PROTOTYPE != PRODUCTION_CARD`.
