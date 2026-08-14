# 1 Peter Chapters 4–5 product handoff audit scope

Parent Research authority: `0142430af8ba80f28e0fd9cde669d32611a1d2af` (PR #183 head at audit start).

This directory is an independent Research-to-product control plane. It is not a production question bank, publication approval, ranking approval, or replacement for the Research authority chain.

## Authority order

1. `data/question-candidates-wave3-*.json` is the base candidate universe.
2. Candidate field overrides apply in this order: `wave3e`, `wave3g`, `wave3k`, `wave3l`, `wave3n`, and only for fields named by each override's `supersedesFields` declaration.
3. `data/remaining-holds-wave3n.json` is the current HOLD authority. Earlier HOLD files and the frozen Wave3 snapshot are historical evidence, not current status.
4. Source identities and source inspection depth are separate authorities. A source ID match never imports a deeper inspection scope from another lane.
5. MCQ prototypes remain Research authoring material. They are audited against effective claims; they are never product cards by inheritance.

## Non-negotiable boundaries

`SOURCE_FOUND != CLAIM_PROVED`; `URL_EXISTS != SOURCE_INSPECTED`; `ABSTRACT != FULL_TEXT_EVIDENCE`; `BIBLIOGRAPHIC_IDENTITY != CLAIM_EVIDENCE`; `MORPHOLOGY != EXEGESIS`; `LEXICON_RANGE != PASSAGE_EXEGESIS`; `HISTORICAL_PLAUSIBILITY != TEXT`; `ONE_COMMENTATOR != CONSENSUS`; `PROJECT_POSITION != NEUTRAL_FACT`; `SECONDARY_APPARATUS != ECM`; `NAMED_MANUSCRIPT != TEXT_DECISION`; `ECM_TEXT_DECISION != MANUSCRIPT_UNANIMITY`; `ECM_BASED_COMMENTARY != DIRECT_DECM_READBACK`; `PEER_REVIEW_STATUS != PASSAGE_EVIDENCE`; `ZERO_RESEARCH_HOLDS != PRODUCTION_READY`; `READY != RANKING_READY`; `MCQ_PROTOTYPE != PRODUCT_CARD`; `GREEN_VALIDATOR != PUBLICATION_APPROVAL`.

## Exact-head audit observations before new handoff data

- PR #183 changed paths are confined to `1_PETER_BOT/**`; no bible-bot/runtime/product files are in the Research PR diff.
- No repository-root `AGENTS.md` exists at the pinned head. This audit therefore does not invent or infer missing repository instructions.
- The current README/Wave3n authority reports a 144-record universe, 72 Chapter 4 and 72 Chapter 5, with current HOLD count 0 and competitive count 0. These are treated as claims to be independently recomputed by the validator, not trusted constants.
- The final Wave3 snapshot predates Wave3n and can legitimately retain four historical HOLDs. Current status must be derived through the override chain plus `remaining-holds-wave3n.json`.
- Wave3n closes four distinct textual units: 4:14 (`w3q_031`), 5:2 `ἐπισκοποῦντες` (`w3q_050`), 5:2 `κατὰ θεόν` (`w3q_051`), and 5:12 `στῆτε / ἑστήκατε` (`w3q_075`). The two 5:2 units are independent and may not share evidence by proximity.
- Wave3n is ECM/CBGM-based secondary scholarly closure, not direct dECM witness readback and not manuscript unanimity.

## Output contract

`validate_product_handoff.py --emit-dir <dir>` deterministically emits:

- `chapter4-product-handoff.json`
- `chapter5-product-handoff.json`
- `claim-overclaim-blacklist.json`
- `source-identity-package.json`
- `claim-inspection-manifest.json`
- `prototype-audit.json`
- `ranking-audit.json`
- `integrity-summary.json`

The validator re-derives these from independent Research inputs. It does not compare one self-authored expected JSON object to itself.
