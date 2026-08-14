# 1 Peter Wave 3.0d — Application Deck, Source Quorum, and Challenge Blueprints

**Status:** `RESEARCH ONLY / NOT PRODUCTION / NOT RANKING`

Wave 3.0d addresses two weaknesses left after the 96-candidate verse-coverage pass:

1. Chapters 4–5 were still much stronger in text/Greek/interpretation than in carefully bounded application.
2. Several advanced questions needed an explicit **source-quorum / misconception-family** design before final four-option authoring.

## New application deck

Added `w3q_097–112`:

- 16 application candidates;
- 8 Chapter 4;
- 8 Chapter 5;
- all `claim_type=application`;
- all `position=project`;
- all `confidence=medium`;
- all `READY_NONCOMPETITIVE`;
- all `competitive_candidate=false`.

This brings the full Wave-3 candidate corpus to:

- **112 total**;
- **56 Chapter 4**;
- **56 Chapter 5**;
- **52 READY**;
- **53 READY_NONCOMPETITIVE**;
- **7 HOLD**.

The HOLD count is deliberately unchanged.

## Application design principle

Application cards do not ask “what inspiring sentence can we attach to the verse?” They test whether the learner can apply the text **without converting it into a harmful or unsupported absolute**.

### Chapter 4 application targets

- 4:1–2: readiness for faithful suffering != suffering as spiritual merit;
- 4:3–4: social rejection != permission to relapse or retaliate;
- 4:7: eschatological urgency != date-setting;
- 4:8: forgiving love != concealing abuse/crime or abolishing accountability;
- 4:9: hospitality != resentful performance or boundaryless exposure to danger;
- 4:10–11: spiritual gifts = stewardship/service, not personal spiritual status;
- 4:12–16: suffering as a Christian != every consequence of one's own wrongdoing;
- 4:19: entrusting oneself to the Creator != religious passivity.

### Chapter 5 application targets

- 5:1–4: human shepherds serve under the Chief Shepherd; the flock is not personal property;
- 5:2–3: leadership != coercion, shameful gain, or domination;
- 5:5: humility applies to all and cannot be weaponized only against younger/weaker people;
- 5:6–7: casting anxiety on God != denying distress or refusing wise human help;
- 5:8–9: resisting the devil = sober/watchful steadfast faith, not invented ritual technique;
- 5:10–11: restoration hope != prosperity timetable;
- 5:12: standing in grace != passivity or license;
- 5:4: future crown/accountability != present personal branding or self-exaltation.

## 1 Peter 4:6 source quorum strengthened

### David G. Horrell 2003

Cambridge publisher abstract inspected for:

David G. Horrell, “Who are ‘The Dead’ and When was the Gospel Preached to Them?: The Interpretation of 1 Pet 4.6,” *New Testament Studies* 49.1 (2003), 70–89.

The abstract is unusually useful because it explicitly reports two things:

1. the reading that the dead are Christians evangelized during life who had since died had become increasingly accepted in English commentaries;
2. Horrell himself argues that the alternative reading — proclamation to people already dead — is more plausible than those commentators admit.

This is **abstract-level** evidence only. His detailed arguments are not claimed inspected.

### Kerugma 2025

Publisher/search metadata and abstract identify a 2025 CC BY 4.0 article defending the now-dead-after-lifetime-evangelization reading.

The linked PDF was not successfully inspected in this wave, so the source remains abstract-bounded despite its open license.

### Result

The 4:6 state is stronger but **not more closed**:

```text
DISPUTE_MAP = STRONGER
PROJECT_POSITION = HOLD
COMPETITIVE_SINGLE_ANSWER = UNSAFE
```

Storms/Forbes + the recent Kerugma abstract represent one family; Horrell supplies a serious peer-reviewed counter-position. This is exactly the kind of passage where better research increases calibrated uncertainty rather than manufacturing certainty.

## Challenge blueprints

Added 16 challenge blueprints. These are **not final MCQ options**. Each records:

- verse/range;
- existing candidate basis;
- exact reasoning skill;
- correct claim nucleus;
- three realistic distractor families;
- a fairness guard.

Priority challenge skills:

1. 4:1 — morphology vs perfectionism;
2. 4:4 — context-sensitive `ἐν ᾧ` semantics;
3. 4:6 — grammar vs disputed chronology;
4. 4:7 — eschatology text vs systematic timetable;
5. 4:8 — strong proverbial reuse vs verbatim LXX;
6. 4:10–11 — stewardship vs exhaustive gift taxonomy;
7. 4:14 — stable text vs textual-variant HOLD;
8. 4:16 — Χριστιανός evidence vs emperor/date overclaim;
9. 4:18 — very close LXX reproduction vs loose echo;
10. 5:2–3 — stable shepherding ethics vs apparatus-sensitive polity proof;
11. 5:5 — close LXX reuse with visible subject adaptation;
12. 5:6–7 — syntax/pastoral care vs anxiety shaming;
13. 5:8–9 — explicit lion metaphor vs exclusive background identification;
14. 5:12 — Silvanus role vs grammatical overclaim;
15. 5:13 — grammar/toponym/history layers;
16. 4:6 — source-quorum awareness itself.

## Why the challenge layer matters

A “hard” question should be difficult because the learner must keep epistemic layers separate, not because one distractor mentions an unrelated king or obscure manuscript.

Good challenge item:

> Which claim goes beyond what the morphology can establish?

Bad challenge item:

> Which of these four random technical terms looks most scholarly?

The Challenge blueprints therefore prefer distractors that are **near-miss inferences**:

- real but overstated grammar;
- plausible but overconfident historical reconstruction;
- serious theological conclusion placed at the wrong evidence layer;
- real textual variant treated as settled without apparatus;
- genuine commentator position presented as consensus.

## Production boundary

Before any Wave 3.0d candidate becomes a bot card:

1. source minimum must be rechecked against current inspection scope;
2. source IDs must resolve after integration canonicalization;
3. three final distractors must match the blueprint family without becoming caricatures;
4. answer-position distribution must be calculated across the final lane;
5. answer-length and wording leakage must be regression-tested;
6. all application/project/contested items remain noncompetitive;
7. an independent source auditor should re-read the authored cards.

```text
APPLICATION_READY_NONCOMPETITIVE != RANKING_READY
CHALLENGE_BLUEPRINT != FINAL_QUESTION
SOURCE_QUORUM_MAP != CONSENSUS
MORE_RESEARCH != FORCED_CLOSURE
```
