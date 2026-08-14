# Independent release assessment — Research PR #183

## Decision

**READY_FOR_RESEARCH_MERGE**

This decision is limited to Research PR #183 at exact head `0142430af8ba80f28e0fd9cde669d32611a1d2af`. It is **not** product approval, publication approval, ranking approval, or permission to copy Research MCQ prototypes into bible-bot.

The second-pass audit is materially stricter than the first pass. It found additional product-template defects and one ranking discrepancy, but none changes the effective Research claim corpus, reopens a current HOLD, creates a fake source claim, or introduces product/runtime drift.

## Effective Research authority

- Audited parent SHA: `0142430af8ba80f28e0fd9cde669d32611a1d2af`.
- Effective corpus recomputed from candidate batches plus the declared override precedence: **144 total = 72 Chapter 4 + 72 Chapter 5**.
- Effective current HOLD count: **0**. The four Wave3l HOLDs are historical and correspond exactly to the four explicit Wave3n closure records (`w3q_031`, `w3q_050`, `w3q_051`, `w3q_075`).
- Effective competitive candidate count: **0**.
- Source ownership: **112 source identities / 282 claim-to-source inspection edges**.
- Source identity variants/conflicts detected by the new normalized identity audit: **0**.
- Effective authority digest for this parent corpus under handoff schema v2: `1f444991ecc2f180abdbe0f459148ba8dbf0a5045b1d8888e462683c78366c7d`.
- No orphan candidate overrides, duplicate candidate IDs, duplicate prototype IDs, missing current source owners, current-HOLD contradictions, or accidental Research competitive admissions survived the validator.
- PR #183 changed paths remain Research-only under `1_PETER_BOT/**`; no bible-bot/runtime/product drift was found.

## Source-depth hardening added by Agent E

The first-pass audit had one architectural weakness: some safe evidence semantics lived only in the CI wrapper. That has been removed.

The canonical validator now enforces:

1. `evidence_status`, `access_state`, and `inspection_scope` are distinct dimensions.
2. Missing explicit evidence status becomes `NOT_EXPLICITLY_LABELED`; access status is never substituted.
3. Source owner resolution follows **field-level provenance of effective `source_minimum`**, not the candidate's latest unrelated override.
4. A repeated `source_id` cannot automatically inherit the strongest/deepest lane.
5. Every effective claim has a stable claim digest.
6. Every claim/source inspection edge has a stable digest over owner, depth, limit, and provenance.
7. Source identity records expose title/locator/type variants without importing claim depth.

`w3_brown_allotriepiskopos_2006` remains correctly resolved through `source-upgrade-wave3e.json` as an inspection-only source lane, not a global evidence-depth upgrade.

## Second-pass prototype audit

64 Research prototypes were reclassified against exact effective authority and the explicit rule that **distractors may not teach false certainty merely because they are wrong answers**.

Current product-template dispositions:

- `SAFE_TEMPLATE`: **26**
- `NEEDS_REWRITE`: **19**
- `COURSE_POSITION_ONLY`: **2**
- `NONCOMPETITIVE_ONLY`: **12**
- `REJECT_AS_PRODUCT_TEMPLATE`: **5**

`REJECT_AS_PRODUCT_TEMPLATE`:

- `w3mcq_003` — `REFERENCE_DRIFT`
- `w3mcq_020` — `REFERENCE_DRIFT`
- `w3mcq_027` — `REFERENCE_DRIFT`
- `w3mcq_037` — `REFERENCE_DRIFT`
- `w3mcq_047` — `REFERENCE_DRIFT`

These five are not silently normalized. Their candidate linkage may still be useful for research history, but a product agent may not infer that a mismatched prototype reference is harmless.

`NEEDS_REWRITE`:

`w3mcq_033`, `w3mcq_036`, `w3mcq_038`, `w3mcq_040`, `w3mcq_041`, `w3mcq_042`, `w3mcq_043`, `w3mcq_044`, `w3mcq_045`, `w3mcq_046`, `w3mcq_049`, `w3mcq_050`, `w3mcq_054`, `w3mcq_056`, `w3mcq_057`, `w3mcq_058`, `w3mcq_060`, `w3mcq_062`, `w3mcq_064`.

The detected rewrite-risk families include absolute always/never claims, lexical exclusivity, grammar-to-exegesis necessity, generic “proves” language, consensus totalization, manuscript unanimity, CBGM automation myths, apparatus-is-unneeded claims, fake textual-insertion certainty, formal-quotation overclaim, and unsupported historical/legal certainty.

One prototype, `w3mcq_015`, has a low automated lexical-alignment signal because its effective Research authority states the comparison mainly through the Greek sequence while the keyed option summarizes that comparison in Russian. Human readback keeps it as a review signal rather than fabricating a content defect.

These prototype findings are **product-handoff blocks**, not a claim that the effective 144-record Research authority is false. Agent E does not rewrite the prototype wording to improve pass rate.

## Independent ranking audit

**RANKING ADMISSION = 0.**

The adversarial Chapter-3-style prefilter now surfaces exactly one discrepancy candidate: **`w3q_123` (1 Pet 4:16)**.

Why it surfaces: it is a neutral, high-confidence, objectively answerable edition-attribution fact (`ECM/NA28 -> ἐν τῷ μέρει τούτῳ`) with relevant inspected source depth.

Why it is not promoted: it remains `READY_NONCOMPETITIVE`, lives inside a real textual-variation unit, and its source boundary forbids turning the secondary ECM/CBGM exposition into direct dECM witness readback. A separate product reviewer must decide whether edition-attribution facts inside known textual variants can ever satisfy product ranking policy.

See `RANKING_DISCREPANCY_W3Q123.md`.

## Mandatory claim guards

- 4:6: keep project position separate from the open neutral scholarly dispute; morphology cannot settle chronology/location/audience identity.
- 4:12–19 / Malachi 3: serious proposed background is not a proven formal quotation or unique controlling intertext.
- 4:14: ECM-based scholarly closure is not direct dECM witness-table readback and not manuscript unanimity.
- 4:16: edition attribution (`SBLGNT` vs `ECM/NA28`) must not become an imaginary unified “Greek text” or a fabricated witness census.
- 5:2 `ἐπισκοποῦντες` and 5:2 `κατὰ θεόν`: independent textual units; evidence must never cross by proximity.
- 5:10: four-verb set is edition-bounded; morphology does not prove timing/prosperity and the sequence is not universalized across manuscripts.
- 5:12 `στῆτε / ἑστήκατε`: editorial/textual decision does not license an invented full witness list, direct-dECM claim, or manuscript unanimity.
- 5:13 Babylon: textual toponym does not by itself settle Rome vs literal/historical location theories.

The machine control plane carries **144 claim-specific overclaim records** plus **26 global overclaim patterns**.

## Cross-repository release boundary

Product review must pin the exact Research SHA, the complete authority digest, each effective claim digest, and exact claim-inspection edge IDs. Pinning only `w3q_*` or only a source ID is insufficient.

The product root source registry may carry bibliographic identity only; it must not become a global “strongest source status” registry. This preserves the Chapter-3 identity-only / lane-local-depth architecture.

## Why PR #183 is still Research-merge-ready

The merge decision concerns the Research authority, not whether every Research MCQ prototype is a reusable product template.

The effective claim corpus is internally coherent at current authority, exact-head Research integrity is green, current HOLDs are genuinely zero, override/source provenance remains intact, source claims are bounded to inspected lanes, all Research competitive flags remain false, and no product/runtime files drifted into PR #183.

The newly found prototype reference drift and distractor-certainty issues are explicitly quarantined by the independent handoff audit rather than hidden or rewritten. They therefore **reduce product reuse permissions**; they do not upgrade claims or mask a Research HOLD.

This assessment does **not** waive normal repository review/branch-protection requirements and does not authorize any bible-bot release.

## Exact owner text for removing Draft / merge review

> Independent Research audit completed for PR #183 at exact head `0142430af8ba80f28e0fd9cde669d32611a1d2af`. Effective corpus recomputes to 144 claims (72 Chapter 4 / 72 Chapter 5), current HOLD=0, Research competitive candidates=0; historical HOLDs resolve through the explicit Wave3n chain; source ownership is field-provenance-bound and Research-only path scope is intact. The separate product-handoff audit has quarantined unsafe/rewrite-only Research prototypes and one ranking discrepancy without promoting them. This is approval to move PR #183 from Draft into normal Research merge review only. It is not product, publication, or ranking approval. Merge remains subject to the repository's normal required checks and owner review.

The owner may use that text to mark PR #183 ready for review and proceed with normal Research merge review. This audit does not perform either action.
