# Independent release assessment — Research PR #183

## Decision

**READY_FOR_RESEARCH_MERGE**

This decision is limited to Research PR #183 at exact head `0142430af8ba80f28e0fd9cde669d32611a1d2af`. It is **not** product approval, publication approval, ranking approval, or permission to copy Research MCQ prototypes into bible-bot.

## Independent findings

- Audited parent SHA: `0142430af8ba80f28e0fd9cde669d32611a1d2af`.
- Effective corpus recomputed from candidate batches plus the declared override precedence: **144 total = 72 Chapter 4 + 72 Chapter 5**.
- Effective current HOLD count: **0**. The four Wave3l HOLDs are historical and correspond exactly to the four explicit Wave3n closure records (`w3q_031`, `w3q_050`, `w3q_051`, `w3q_075`). Historical HOLD files remain audit evidence and are not unioned into current state.
- Effective competitive candidate count: **0**.
- Source ownership: **112 source identities / 282 claim-to-source inspection edges** resolved by the handoff validator. The initially unresolved `w3_brown_allotriepiskopos_2006` edge was traced to the legitimate `source-upgrade-wave3e.json` authority and is treated as an inspection-only lane, not a global evidence-depth upgrade.
- Source identity, access state, evidence status, and inspection depth are separated. A bibliographic source ID cannot import a deeper inspection lane into another claim.
- No orphan candidate overrides, duplicate candidate IDs, duplicate prototype IDs, missing current source owners, current-HOLD contradictions, or accidental competitive admissions survived the validator.
- PR #183 changed paths are Research-only under `1_PETER_BOT/**`; no bible-bot/runtime/product path drift was found.
- Existing Repository authority integrity passed on the exact PR #183 head. The independent Chapter 4–5 handoff validator additionally recomputes the effective corpus rather than trusting that older run.

## Prototype audit

64 Research prototypes were reclassified against effective authority:

- `SAFE_TEMPLATE`: **28**
- `NEEDS_REWRITE`: **5** — `w3mcq_003`, `w3mcq_020`, `w3mcq_027`, `w3mcq_037`, `w3mcq_047`
- `COURSE_POSITION_ONLY`: **6** — `w3mcq_036`, `w3mcq_038`, `w3mcq_042`, `w3mcq_051`, `w3mcq_053`, `w3mcq_054`
- `NONCOMPETITIVE_ONLY`: **25**
- `REJECT_AS_PRODUCT_TEMPLATE`: **0**

`SAFE_TEMPLATE` still means only a bounded Research authoring template. It does not mean product-card approval. The five rewrite findings are not silently repaired here; future authors must resolve them under a separate editorial review if they want to reuse those prototypes.

## Independent ranking audit

**COMPETITIVE / RANKING ADMISSION = 0.**

The Chapter 3 adversarial standard was applied fail-closed: neutral/high/direct-looking material still requires exact claim-ready owning-lane inspection and a separate product ranking review. The mechanical discrepancy prefilter found **0** candidates that justify escalation. Research `READY` therefore remains distinct from `RANKING_READY`.

## Mandatory claim guards

- 4:6: keep project position separate from the open neutral scholarly dispute; morphology cannot settle chronology/location/audience identity.
- 4:12–19 / Malachi 3: serious proposed background is not a proven formal quotation or unique controlling intertext.
- 4:14: ECM-based scholarly closure is not direct dECM witness-table readback and not manuscript unanimity.
- 5:2 `ἐπισκοποῦντες` and 5:2 `κατὰ θεόν`: independent textual units; evidence must never cross by proximity.
- 5:10: four-verb set is edition-bounded to the inspected teaching base; morphology does not prove timing/prosperity.
- 5:12 `στῆτε / ἑστήκατε`: editorial/textual decision does not license an invented full witness list or unanimity claim.
- 5:13 Babylon: textual toponym does not by itself settle Rome vs literal/historical location theories.

The machine control plane also carries **144 claim-specific overclaim records** plus **20 global overclaim-pattern guards**.

## Merge-readiness criteria

PR #183 is Research-merge-ready because the effective corpus is internally consistent, the exact head is integrity-green, current HOLDs are genuinely zero, override/source provenance is preserved, source claims remain bounded to inspected lanes, and there is no product/runtime drift.

This assessment does **not** waive normal repository review/branch-protection requirements and does not authorize any bible-bot release.

## Exact owner text for removing Draft / merge review

> Independent Research audit completed for PR #183 at exact head `0142430af8ba80f28e0fd9cde669d32611a1d2af`. Effective corpus recomputes to 144 claims (72 Chapter 4 / 72 Chapter 5), current HOLD=0, competitive candidates=0; historical HOLDs resolve through the explicit Wave3n override chain; source ownership/provenance and Research-only path scope are intact. This is approval to move PR #183 from Draft into normal Research merge review only. It is not product, publication, or ranking approval. Merge remains subject to the repository's normal required checks and owner review.

The owner may use that text to mark PR #183 ready for review and proceed with normal Research merge review. This audit does not perform either action.
