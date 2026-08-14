# 1 Peter Wave 3.0j2 — MCQ Editorial Self-Audit

**Status:** `RESEARCH EDITORIAL CORRECTION / NOT PRODUCTION`

The first Wave-3j readback was intentionally audited after the balanced answer-key manifest was already green at the design level.

That audit found a critical product lesson:

```text
BALANCED CORRECT POSITIONS != LEAK-FREE MCQ
```

A bank can have perfect `8/8/8/8` answer positions and still leak through:

- correct-option length;
- uniquely detailed wording;
- a very short keyed option against verbose distractors;
- distractors that are structurally parallel but intellectually absurd;
- lexical questions where the keyed option alone contains lemma + inflected form.

## Corrected prototypes

Nine prototypes receive authoring-time overrides:

- `w3mcq_008` — Prov 10:12 / 4:8: keyed explanation no longer uniquely longest;
- `w3mcq_009` — hospitality: `Без ропота` no longer leaks by extreme brevity;
- `w3mcq_011` — `πύρωσις`: all four options now have comparable lexical/contextual structure;
- `w3mcq_013` — 4:15 wrongdoing list: distractor lists now parallel the keyed list;
- `w3mcq_017` — 5:1 self-description: alternatives now have comparable completeness;
- `w3mcq_020` — elder contrasts: artificial unrelated triads replaced by reversals and near-miss readings of the actual text;
- `w3mcq_022` — 5:5 submission: alternatives now represent real referent/context overreads;
- `w3mcq_024` — mighty hand: pastoral/systematic overreaches made stylistically comparable;
- `w3mcq_029` — divine agency 5:10: non-keyed options no longer leak by being much shorter.

## What did not change

- 32 prototype IDs;
- linked candidate IDs;
- correct positions;
- `8/8/8/8` distribution;
- chapter split 16/16;
- source inheritance contract;
- `competitive_candidate=false`;
- the six substantive HOLDs.

## Effective-authoring order

For Wave-3 MCQ work the effective object is now resolved in this order:

1. candidate base record;
2. candidate overrides from Wave 3e/3g and later;
3. source upgrades/quorum controls;
4. Wave-3j base MCQ prototype;
5. Wave-3j2 MCQ override, if present.

A later MCQ override may improve wording/options but may not:

- change a substantive keyed claim;
- promote a HOLD;
- upgrade source inspection depth;
- remove a `do_not_claim` guard;
- change competitive/ranking eligibility.

## Regression contract

The effective 32-prototype bank must satisfy:

- exactly four non-empty options;
- normalized unique options;
- `0 <= correct < 4`;
- explanation equals `options[correct]` after overrides;
- correct-position Counter exactly `{0:8,1:8,2:8,3:8}`;
- all four positions used;
- no three identical correct positions consecutively;
- no simple `0,1,2,3` repeating cycle;
- no keyed answer should be identifiable merely because it is the only option written as a long explanation or the only option written as a bare word;
- distractors should encode nearby misconceptions, not jokes.

## Product lesson

The Chapter-3 answer-key incident taught us to measure position leakage.

Wave 3j2 extends that lesson:

```text
POSITION LEAKAGE
+ LENGTH LEAKAGE
+ VERBOSITY LEAKAGE
+ DISTRACTOR-PLAUSIBILITY LEAKAGE
= ONE AUTHORING-QUALITY PROBLEM
```

Future `bible-bot` banks should regression-test all four dimensions rather than treating option shuffle as a universal fix.

`GREEN_STRUCTURE != EDITORIAL_QUALITY_APPROVAL`.
