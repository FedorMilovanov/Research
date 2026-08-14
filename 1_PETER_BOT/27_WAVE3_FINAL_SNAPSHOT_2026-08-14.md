# 1 Peter Source Marathon — Wave 3 Final Snapshot

**Date:** 2026-08-14  
**Status:** `RESEARCH COMPLETE FOR THIS WAVE / DRAFT PR / NOT PRODUCTION / PUBLICATION HOLD`

This file closes the current Wave-3 research marathon. It is a snapshot, not a new research lane.

## 1. Frozen parent reviewed before finalization

The finalization pass was built on:

`b2a0f806a6bc8f0d9a25f74f7833713f2ad139e6`

That parent already had:

- `Repository authority integrity #931 = SUCCESS`;
- 144 effective research candidates;
- 72 Chapter-4 candidates and 72 Chapter-5 candidates;
- 52 `READY`;
- 88 `READY_NONCOMPETITIVE`;
- 4 remaining `HOLD`;
- 64 MCQ research prototypes;
- 32 Chapter-4 MCQ prototypes and 32 Chapter-5 MCQ prototypes;
- exact combined correct-position counts `0=16, 1=16, 2=16, 3=16`.

No candidate or MCQ is promoted to production by this snapshot.

## 2. What the marathon now contains

The research branch now has an integrated control plane for:

- open Greek surface text and MorphGNT morphology;
- NA28 / GNT6 / forthcoming NA29 edition-state discipline;
- ECM / NTVMR textual-criticism workflow;
- named-manuscript literacy;
- bounded lexical semantics with Abbott-Smith / Moulton–Milligan controls;
- OT/LXX reuse classification;
- Chapters 4–5 passage-level research map;
- historical/social reconstruction guardrails;
- TMS project-position separation from neutral text claims;
- disputed-passage mapping;
- application guardrails;
- question-candidate authoring;
- distractor blueprints;
- answer-position leakage prevention;
- 64 four-option MCQ prototypes with exact position balance;
- explicit source-depth / rights / inspection-state boundaries.

## 3. Effective candidate corpus

After the Wave-3e / 3g / 3k / 3l override chain:

```text
TOTAL = 144
CHAPTER_4 = 72
CHAPTER_5 = 72
READY = 52
READY_NONCOMPETITIVE = 88
HOLD = 4
```

The effective-record rule is mandatory:

```text
BASE_CANDIDATE
-> LATER_CANDIDATE_OVERRIDE
-> SOURCE_UPGRADE_OR_QUORUM
-> MCQ_PROTOTYPE
-> MCQ_EDITORIAL_OVERRIDE
```

A superseded HOLD or older interpretation must never reappear merely because an early JSON file still contains the historical record.

## 4. MCQ authoring bridge

The research-only prototype layer contains:

```text
TOTAL_MCQS = 64
CHAPTER_4 = 32
CHAPTER_5 = 32
CORRECT_0 = 16
CORRECT_1 = 16
CORRECT_2 = 16
CORRECT_3 = 16
```

The prototype layer explicitly requires:

- four non-empty options;
- normalized option uniqueness;
- correct explanation matching the keyed option;
- no runtime shuffle as a substitute for bad authoring;
- no simple answer-position cycle;
- no three identical correct positions in a row in authored batches;
- distractors representing real nearby misconceptions;
- no HOLD claim used as a keyed answer;
- no source-depth upgrade caused merely by a prototype.

## 5. Four remaining fail-closed HOLDs

Only four candidate-level HOLDs remain:

### `HOLD-TC-4-14`
1 Peter 4:14 — Spirit/glory expansion textual unit.

Needs direct current ECM/dECM readback or a sufficiently explicit peer-reviewed ECM-based treatment.

### `HOLD-TC-5-2A`
1 Peter 5:2 — `ἐπισκοποῦντες` official ECM closure.

SBLGNT presence, Sinaiticus omission, and secondary apparatus are teachable data, but they do not substitute for current ECM closure.

### `HOLD-TC-5-2B`
1 Peter 5:2 — `κατὰ θεόν` official ECM closure.

This is a distinct variation problem and must not be collapsed into the `ἐπισκοποῦντες` question.

### `HOLD-TC-5-12`
1 Peter 5:12 — `στῆτε / ἑστήκατε` official ECM reasoning.

Witness counting, SBLGNT choice, or one early manuscript is insufficient to close the editorial question.

## 6. Important closures achieved

The marathon did close several earlier weak points without pretending consensus:

- 1 Peter 4:6 now has an explicit **project position**: believers evangelized while alive and now dead; the neutral scholarly dispute remains open and is labelled as such.
- 1 Peter 4:16 now teaches edition transparency: SBLGNT `ὀνόματι` vs ECM/NA28 `μέρει` through an inspected peer-reviewed ECM/CBGM treatment; this does not pretend direct dECM witness readback where it was not performed.
- Malachi 3 / 1 Peter 4:12–19 is classified as a serious proposed prophetic/imagery background, not a formal quotation.
- 1 Peter 5:10 four-verb questions are explicitly edition-bounded to SBLGNT and do not claim an invariant four-verb manuscript tradition.
- `ἀλλοτριεπίσκοπος`, `πύρωσις`, `λόγιον`, `ἐγκομβόομαι`, `ἀντίδικος`, `σθενόω`, `συνεκλεκτός` and related lexical units are taught with the rule `LEXICON RANGE != PASSAGE EXEGESIS`.

## 7. Scope integrity

Immediately before this final snapshot, PR #183 contained 71 changed files and every changed path was under:

`1_PETER_BOT/**`

No product repository, bot runtime, site code, workflows, shared Research authority files, or `main` branch were intentionally modified by this marathon.

## 8. Final governance boundary

```text
SOURCE_FOUND != CLAIM_PROVED
URL_EXISTS != SOURCE_INSPECTED
ABSTRACT != FULL_TEXT
CATALOG != PASSAGE_EVIDENCE
MORPHOLOGY != EXEGESIS
LEXICON_GLOSS != COMPLETE_CONTEXT
HISTORICAL_PLAUSIBILITY != BIBLICAL_TEXT_STATEMENT
ONE_SCHOLAR != CONSENSUS
PROJECT_POSITION != NEUTRAL_FACT
SECONDARY_APPARATUS != ECM
NAMED_MANUSCRIPT != ORIGINAL_TEXT_DECISION
QUESTION_CANDIDATE_READY != PRODUCTION_READY
MCQ_PROTOTYPE != RANKING_READY
GREEN_VALIDATOR != PUBLICATION_APPROVAL
RESEARCH_PR != BOT_PRODUCTION
```

## 9. Handoff

This wave is now intentionally stopped.

Next work should be a separate integration/editorial stage, not another source-marathon extension:

1. preserve the four textual HOLDs unless new direct ECM-quality evidence appears;
2. select production-worthy candidates from the 144 research records;
3. author/final-edit cards in the product repository under its own AGENTS/source policy;
4. retain noncompetitive treatment for disputed/project/application/history layers as required;
5. run fresh product-side source audit before ranking or publication.

`WAVE3_RESEARCH_COMPLETE != PUBLICATION_COMPLETE`.
