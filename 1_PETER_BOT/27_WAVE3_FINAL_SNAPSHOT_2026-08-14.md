# 1 Peter Source Marathon — Wave 3 Final Snapshot

**Date:** 2026-08-14  
**Status:** `RESEARCH COMPLETE / ZERO CANDIDATE HOLDS / DRAFT PR / NOT PRODUCTION / PUBLICATION HOLD`

This is the canonical Wave-3 research snapshot after the Wave-3n textual-closure extension.

Wave 3n does **not** erase the earlier Wave-3l checkpoint. The old files correctly record that four textual units were unresolved at that time. The later override/quorum layer supplies the effective state.

## 1. Frozen parent and closure extension

The original finalization pass was built on:

`b2a0f806a6bc8f0d9a25f74f7833713f2ad139e6`

That parent had:

- `Repository authority integrity #931 = SUCCESS`;
- 144 effective research candidates;
- 52 `READY`;
- 88 `READY_NONCOMPETITIVE`;
- 4 textual-critical `HOLD`;
- 64 MCQ research prototypes;
- exact combined correct-position counts `0=16, 1=16, 2=16, 3=16`.

Wave 3n subsequently closed those four candidate-level HOLDs using the **already-authorized peer-reviewed ECM-based textual-critical treatment route**, not by weakening the standard.

The publication-review route is recorded explicitly in `data/source-quorum-wave3n.json`: Bloomsbury Academic's external confidential peer-review policy controls the Williams–Horrell ICC publication route, while Stanojević is identified as a revised doctoral thesis and Gorgias states that doctoral dissertations receive external scholarly evaluation. This review-status metadata remains separate from passage evidence: `PEER_REVIEW_STATUS != PASSAGE_EVIDENCE`.

New Wave-3n authority files:

- `28_WAVE3N_ECM_CLOSURE_2026-08-14.md`;
- `data/source-quorum-wave3n.json`;
- `data/question-overrides-wave3n.json`;
- `data/remaining-holds-wave3n.json`.

No candidate or MCQ is promoted to production by this closure.

## 2. What the marathon now contains

The research branch has an integrated control plane for:

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
- explicit source-depth / rights / inspection-state boundaries;
- explicit ECM-quality closure records for the final four textual units.

## 3. Effective candidate corpus

After the complete override chain including Wave 3n:

```text
TOTAL = 144
CHAPTER_4 = 72
CHAPTER_5 = 72
READY = 52
READY_NONCOMPETITIVE = 92
HOLD = 0
COMPETITIVE_CANDIDATES = 0
```

The effective-record rule is mandatory:

```text
BASE_CANDIDATE
-> LATER_CANDIDATE_OVERRIDE (including Wave 3n)
-> SOURCE_UPGRADE_OR_QUORUM (including Wave 3n)
-> MCQ_PROTOTYPE
-> MCQ_EDITORIAL_OVERRIDE
```

A superseded HOLD must never reappear merely because an earlier JSON file preserves the historical record.

## 4. MCQ authoring bridge

The research-only prototype layer remains:

```text
TOTAL_MCQS = 64
CHAPTER_4 = 32
CHAPTER_5 = 32
CORRECT_0 = 16
CORRECT_1 = 16
CORRECT_2 = 16
CORRECT_3 = 16
```

The prototype layer still requires:

- four non-empty options;
- normalized option uniqueness;
- correct explanation matching the keyed option;
- no runtime shuffle as a substitute for bad authoring;
- no simple answer-position cycle;
- no three identical correct positions in a row in authored batches;
- distractors representing real nearby misconceptions;
- no source-depth upgrade caused merely by a prototype.

The fact that the four former HOLD candidates are now research-closed does not automatically add them to the existing MCQ prototype set and does not authorize ranking.

## 5. Final four textual closures

### `HOLD-TC-4-14` / `w3q_031`

**Effective state:** `READY_NONCOMPETITIVE`.

The current critical line prefers the shorter 4:14 wording without the `δύναμις` expansion. Williams–Horrell 2023 explicitly discuss the variant with reference to ECM 182 and prefer the shorter reading; Stanojević 2021 independently records the corresponding ECM-side unit without the addition.

The ancient expansion remains part of the teaching record. `TEXTUAL_PREFERENCE != VARIANT_DID_NOT_EXIST`.

### `HOLD-TC-5-2A` / `w3q_050`

**Effective state:** `READY_NONCOMPETITIVE`.

`ἐπισκοποῦντες` has meaningful omission evidence. Williams–Horrell explicitly use ECM 188–189 and prefer retaining the participle after weighing external and internal considerations.

This closes the textual question, not the whole polity debate.

### `HOLD-TC-5-2B` / `w3q_051`

**Effective state:** `READY_NONCOMPETITIVE`.

`κατὰ θεόν` is a distinct textual unit and must not be collapsed into the participle variant. Current ECM-aligned evidence supports retention; Stanojević independently records the ECM-side reading at the exact 5:2 unit with the phrase present.

### `HOLD-TC-5-12` / `w3q_075`

**Effective state:** `READY_NONCOMPETITIVE`.

Stanojević records the exact ECM comparison address `1 Pet 5:12/46` with `στῆτε` on the ECM side. Williams–Horrell independently prefer `στῆτε`, using both external support and an internal/transmissional explanation for the later declarative form.

This closes the previous apparatus/reasoning HOLD without using witness counting or an oldest-manuscript-wins shortcut.

## 6. Important earlier closures preserved

The marathon also retains these earlier hardened conclusions:

- 1 Peter 4:6 has an explicit **project position**: believers evangelized while alive and now dead; the neutral scholarly dispute remains open and is labelled as such.
- 1 Peter 4:16 teaches edition transparency: SBLGNT `ὀνόματι` vs ECM/NA28 `μέρει` through an inspected ECM/CBGM treatment; this does not pretend direct dECM witness readback where it was not performed.
- Malachi 3 / 1 Peter 4:12–19 is classified as a serious proposed prophetic/imagery background, not a formal quotation.
- 1 Peter 5:10 four-verb questions are explicitly edition-bounded to SBLGNT and do not claim an invariant four-verb manuscript tradition.
- `ἀλλοτριεπίσκοπος`, `πύρωσις`, `λόγιον`, `ἐγκομβόομαι`, `ἀντίδικος`, `σθενόω`, `συνεκλεκτός` and related lexical units are taught with the rule `LEXICON RANGE != PASSAGE EXEGESIS`.

## 7. Scope integrity

All Wave-3n writes are under:

`1_PETER_BOT/**`

No product repository, bot runtime, site code, workflows, or `main` branch are part of this Research closure.

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
ECM_TEXT_DECISION != MANUSCRIPT_UNANIMITY
ECM_BASED_COMMENTARY != DIRECT_DECM_READBACK
PEER_REVIEW_STATUS != PASSAGE_EVIDENCE
QUESTION_CANDIDATE_READY != PRODUCTION_READY
MCQ_PROTOTYPE != RANKING_READY
ZERO_RESEARCH_HOLDS != PRODUCTION_READY
GREEN_VALIDATOR != PUBLICATION_APPROVAL
RESEARCH_PR != BOT_PRODUCTION
```

## 9. Handoff

Research Wave 3 is now closed with **zero candidate-level HOLDs**.

The next work is the separate integration/editorial stage:

1. resolve effective records through the full override/quorum chain;
2. select production-worthy candidates from the 144 research records;
3. author/final-edit cards in the product repository under its own source policy;
4. preserve noncompetitive treatment for disputed/project/application/history layers as required;
5. run fresh product-side source/editorial audit before ranking or publication.

`WAVE3_RESEARCH_COMPLETE != PUBLICATION_COMPLETE`.
