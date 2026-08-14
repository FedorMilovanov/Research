# Agent E — second-pass adversarial handoff audit

Parent authority audited: `0142430af8ba80f28e0fd9cde669d32611a1d2af` (Research PR #183).

This pass deliberately did **not** rewrite Chapter 4/5 production content or Research prototype wording. It attacked the previous handoff audit for ways certainty or source depth could still be laundered.

## New findings compared with the first pass

### 1. CI/core semantic divergence existed

The first audit had safer `evidence_status != access_state` and Wave3e source-upgrade handling in `validate_product_handoff_ci.py`, while direct invocation of `validate_product_handoff.py` used weaker semantics. That is an audit defect because a local/manual run and CI could disagree about evidence depth.

Correction: all source/HOLD/depth semantics now live in the canonical core validator. The CI entrypoint only calls the core validator and does not monkeypatch evidence meaning.

### 2. Source ownership now follows field-level provenance

The previous owner resolver chose a quorum partly from the candidate's latest override layer. That could theoretically launder depth when a late override changed `status`, `keyed_concept`, or `do_not_claim` but did **not** author `source_minimum`.

Correction: every effective field now has provenance. Claim-source ownership follows the layer that last authored `source_minimum`, not the latest unrelated candidate override.

Each claim/source edge receives a stable `claim_inspection_edge_id` digest over claim ID, source ID, owner, access/evidence status, inspection scope, claim limit, and source-minimum provenance.

### 3. Access state and evidence status are structurally distinct

`FULL_OBJECT_VERIFIED`, `PARTIAL_OBJECT`, catalog/link availability, etc. are access facts. They cannot be emitted as claim evidence merely because the object exists.

If a source record has no explicit evidence status, generated handoff data says `NOT_EXPLICITLY_LABELED`; inspection scope and a conservative normalized depth class remain separate fields.

### 4. Source identity package exposes variants without depth laundering

Identity output now carries `known_titles`, `known_locators`, `known_types`, and `identity_variant_flag`. The exact audited corpus currently has zero conflicting/variant source identities under this normalization, but the validator will expose future drift instead of silently selecting a strongest record.

### 5. Prototype audit is substantially stricter

The first pass primarily checked structure, effective metadata, and source linkage. That was insufficient for the explicit rule that distractors themselves must not teach false certainty.

The second pass scans **wrong options only** for maximal certainty/evidence laundering, including:

- always/never certainty;
- lexical exclusivity;
- grammar-to-exegesis necessity;
- generic proof language;
- manuscript unanimity;
- one-source-to-consensus totalization;
- direct/automatic CBGM or ECM myths;
- formal-quotation overclaim;
- fabricated textual insertion certainty;
- historical/legal certainty unsupported by the claim lane;
- project position presented as neutral consensus.

Second-pass product-template classifications:

- `SAFE_TEMPLATE`: **26**
- `NEEDS_REWRITE`: **19**
- `COURSE_POSITION_ONLY`: **2**
- `NONCOMPETITIVE_ONLY`: **12**
- `REJECT_AS_PRODUCT_TEMPLATE`: **5**

`REJECT_AS_PRODUCT_TEMPLATE` IDs:

- `w3mcq_003` — `REFERENCE_DRIFT`
- `w3mcq_020` — `REFERENCE_DRIFT`
- `w3mcq_027` — `REFERENCE_DRIFT`
- `w3mcq_037` — `REFERENCE_DRIFT`
- `w3mcq_047` — `REFERENCE_DRIFT`

These five are **not silently normalized or rewritten by Agent E**. Product agents must not treat their linked candidate ID as permission to ignore the prototype metadata mismatch.

`NEEDS_REWRITE` IDs:

`w3mcq_033`, `w3mcq_036`, `w3mcq_038`, `w3mcq_040`, `w3mcq_041`, `w3mcq_042`, `w3mcq_043`, `w3mcq_044`, `w3mcq_045`, `w3mcq_046`, `w3mcq_049`, `w3mcq_050`, `w3mcq_054`, `w3mcq_056`, `w3mcq_057`, `w3mcq_058`, `w3mcq_060`, `w3mcq_062`, `w3mcq_064`.

A low automatic claim-alignment signal was recorded for `w3mcq_015`. Human readback shows the keyed answer is the Russian summary of the candidate's near-verbatim Greek comparison; therefore the low token overlap is retained as a **review signal**, not converted into a false content rejection.

### 6. Ranking audit found one discrepancy for separate review

Research ranking admission remains **0**. The stricter mechanical prefilter now surfaces `w3q_123` as an escalation/discrepancy candidate because it is neutral, high-confidence, direct edition-attribution text and its owning sources have relevant inspected depth.

It is **not promoted**. It remains Research `READY_NONCOMPETITIVE`, concerns a real 4:16 textual-variation unit, and requires separate product ranking review. See `RANKING_DISCREPANCY_W3Q123.md`.

### 7. Cross-repo integrity pins were strengthened

The minimal product bridge now pins:

- exact Research SHA;
- complete effective authority SHA-256 digest;
- exact effective claim digest;
- exact claim-inspection edge IDs;
- product review record ID.

This protects against `same ID, changed content/provenance` drift without creating a runtime dependency on Research.

## Current machine result

At the second-pass audited state before the final documentation commit:

- Ch4 = 72
- Ch5 = 72
- current HOLD = 0
- Research competitive candidates = 0
- Research ranking admissions = 0
- ranking discrepancy candidates = 1 (`w3q_123`)
- source identities = 112
- source identity variants = 0
- claim/source inspection edges = 282
- claim-specific blacklist records = 144
- global overclaim patterns = 26
- effective authority digest = `1f444991ecc2f180abdbe0f459148ba8dbf0a5045b1d8888e462683c78366c7d`

Final exact-head CI must be rerun after this documentation/update wave; green status from an earlier commit is not publication or merge approval.
