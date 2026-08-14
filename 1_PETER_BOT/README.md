# 1 Peter Bot — Research Corpus

**Wave:** 2026-08-14 / Wave 3n closure  
**Status:** `RESEARCH-ONLY / ZERO CANDIDATE HOLDS / PUBLICATION-HOLD`  
**Research base:** `093cbfa541c6c94bd842dcb7ce52e6dc8ebfef88`  
**Working branch:** `agent/1peter-source-marathon`

This corpus supports the `bible-bot` First Peter course without collapsing textual criticism,
Greek, historical reconstruction, exegesis, project theology, and pedagogy into one undifferentiated
"source list".

## Read order

1. `00_CURRENT_WAVE_2026-08-14.md` — original source-marathon foundation.
2. `01_GREEK_TEXT_MANUSCRIPTS_AND_LEXICA.md` — Greek text, NA/UBS/ECM, manuscripts, lexicon protocol.
3. `02_EXEGETICAL_THEOLOGICAL_SOURCE_MAP.md` — TMS project anchor and independent controls.
4. `03_BOT_LEARNING_ARCHITECTURE.md` — scholarship-to-bot learning architecture.
5. `04_SOURCE_INDEX.md` — broad discovery/navigation index.
6. `27_WAVE3_FINAL_SNAPSHOT_2026-08-14.md` — canonical effective Wave-3 snapshot.
7. `28_WAVE3N_ECM_CLOSURE_2026-08-14.md` — final four textual-critical closures.
8. `data/wave3-final-snapshot.json` — machine-readable canonical Wave-3 state.
9. `data/source-quorum-wave3n.json` — ECM-quality evidence quorum for the final closures.
10. `data/question-overrides-wave3n.json` — effective overrides for `w3q_031`, `w3q_050`, `w3q_051`, `w3q_075`.
11. `data/remaining-holds-wave3n.json` — machine authority showing zero remaining candidate-level HOLDs.

## Effective Wave-3 inventory

```text
TOTAL_CANDIDATES = 144
CHAPTER_4 = 72
CHAPTER_5 = 72
READY = 52
READY_NONCOMPETITIVE = 92
HOLD = 0
COMPETITIVE_CANDIDATES = 0

TOTAL_MCQ_PROTOTYPES = 64
CHAPTER_4_MCQS = 32
CHAPTER_5_MCQS = 32
CORRECT_POSITION_COUNTS = 16 / 16 / 16 / 16
```

The four former textual HOLDs were closed in Wave 3n through the pre-existing **peer-reviewed ECM-based textual-critical treatment** route. The criterion was not relaxed, the publication-review route is recorded separately from passage evidence, and direct dECM witness-table readback is not claimed where it was not performed.

## Source-control principles

- Modern copyrighted books are bounded evidence references, not mirrored publication assets.
- Public-domain/open materials are acquisition candidates only when durable custody adds value.
- A Drive copy never creates publication rights.
- A source URL never proves a claim.
- A morphology tag never proves an interpretation.
- A named manuscript never decides the initial text by itself.
- Secondary apparatus never silently becomes ECM.
- An ECM textual decision does not mean manuscript unanimity.
- Peer-review status does not substitute for passage evidence.
- TMS/GTY may define the project's theological position, but never a neutral lexical or manuscript fact.

## Effective-record rule

Consumers must resolve the corpus in this order:

```text
BASE_CANDIDATE
-> LATER_CANDIDATE_OVERRIDE
-> SOURCE_UPGRADE_OR_QUORUM
-> MCQ_PROTOTYPE
-> MCQ_EDITORIAL_OVERRIDE
```

Historical files are intentionally retained. An earlier HOLD remains audit evidence, but it is not the effective record after a later authorized override.

## Product boundary

Nothing in this Research branch is automatically production-approved. `HOLD = 0` means the Wave-3 research candidate corpus has no unresolved candidate-level research HOLD after its current override chain. It does **not** mean:

```text
PRODUCTION_READY
COMPETITIVE_READY
PUBLICATION_AUTHORIZED
MERGE_AUTHORIZED
```

A claim moves to the bot only after product-side authoring, claim-specific wording review, metadata classification, source/editorial audit, ranking review, and the `bible-bot` exact-head gates required by its own repository policy.
