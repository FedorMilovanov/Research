# Cross-repository Chapter 4–5 release audit contract

This contract defines an **immutable metadata bridge only**. It creates no runtime dependency from `bible-bot` to Research and does not turn a Research prototype into a product card.

Every product card derived from the Chapter 4–5 Research corpus must be traceable as:

`PRODUCT_CARD -> PRODUCT_REVIEW_RECORD -> RESEARCH_CLAIM_ID -> EFFECTIVE_RESEARCH_RECORD -> SOURCE OWNER -> INSPECTION DEPTH`

A release audit MUST fail if any edge cannot be resolved.

## Exact authority pins

A product review must pin all of the following, not a branch name:

- `research_repository`: `FedorMilovanov/Research`.
- `research_authority_sha`: exact reviewed Research commit.
- `research_authority_digest_sha256`: digest of the complete effective Ch4/5 authority emitted by the canonical handoff validator.
- `research_claim_id`: exact `w3q_*` ID.
- `research_effective_claim_digest`: digest of the effective claim fields and their field-level provenance.
- `research_handoff_schema_version`.

If the SHA exists but either digest changes or cannot be reproduced, release fails. This prevents a copied claim ID from silently resolving to different wording, confidence, position, sources, or provenance.

## Minimal product-side review bridge

Each product card or its immutable review record must carry:

- `product_card_id`.
- `product_review_record_id`: stable ID for the separate product editorial/source review.
- the exact Research pins above.
- `claimed_position`: `neutral` or `project`; it may stay equal or become more conservative, never `project -> neutral` without a new independent evidence/review record.
- `claimed_confidence`: may stay equal or become more conservative; it may not be raised above Research authority.
- `claimed_claim_type`: must not recast interpretation/history/application as direct text or morphology as passage exegesis.
- `source_ids`: subset/equal set explicitly used by the product claim; adding a source requires a new product review rather than inheriting unrelated Research depth.
- `claim_inspection_edge_ids`: exact immutable edge IDs emitted by Research for the `(claim, source, owning_lane, depth, limit, provenance)` records actually used.
- `product_safe_phrasing_reviewed`: boolean plus reviewer record; Research wording is a ceiling, not automatic publication copy.
- `overclaim_blacklist_checked`: boolean plus the matched/cleared blacklist records.
- `ranking_review_id`: required only if a card is separately proposed for ranking; Research handoff never supplies this implicitly.

## Source identity boundary

`SOURCE_IDENTITY_PACKAGE != CLAIM_INSPECTION_LEDGER`.

The `bible-bot` root source registry may store bibliographic/work identity. It MUST NOT import a strongest inspection status from Research. Claim depth remains attached to the product review's exact `claim_inspection_edge_ids`.

The same work ID appearing in multiple lanes does not make those lanes interchangeable. A later candidate override also does not move source depth: owner resolution follows **field-level provenance of `source_minimum`**.

## Release failures

Fail release when:

1. `research_claim_id` does not exist at the pinned Research SHA.
2. `research_authority_digest_sha256` or `research_effective_claim_digest` cannot be reproduced exactly.
3. product wording is stronger than the bounded Research claim or violates a claim/global overclaim rule without a newly documented evidence lane and product review.
4. product position changes `project -> neutral`, confidence is raised, or claim type is made more objective without independently reviewed provenance.
5. a source is present only in the identity package but no exact claim/source inspection edge exists.
6. inspection depth is borrowed from another claim/lane merely because `source_id` matches.
7. a later unrelated Research override is used to inherit a later quorum instead of following `source_minimum` field provenance.
8. access/full-object status is presented as claim evidence status.
9. a textual-critical claim turns named-witness evidence, secondary apparatus, ECM decision, or ECM-based commentary into a stronger witness-distribution/direct-dECM claim.
10. a 5:2 product card crosses evidence between `ἐπισκοποῦντες` and `κατὰ θεόν`.
11. 5:10 four-verb wording is generalized beyond the named edition/textual base that supports it.
12. 5:12 `στῆτε / ἑστήκατε` is turned into manuscript unanimity or a fabricated direct-dECM witness list.
13. a Research prototype is treated as an approved product card without a separate `product_review_record_id`.
14. a prototype classified `NEEDS_REWRITE`, `COURSE_POSITION_ONLY`, `NONCOMPETITIVE_ONLY`, or `REJECT_AS_PRODUCT_TEMPLATE` is promoted contrary to that restriction.
15. ranking is enabled without an independent product ranking review satisfying the Chapter-3-style lane-local source-depth standard.

## Prototype bridge rule

Prototype IDs are audit references, not product identity. A product card may record `research_prototype_id` for lineage, but release authority comes from the effective Research claim plus the separate product review. Correct-index balancing or a green prototype structural test cannot waive a content-risk finding in a distractor.

## Repository independence

`bible-bot` may vendor/export a reviewed immutable handoff snapshot or copy the minimal metadata above. It must not fetch Research at runtime. Release CI should validate the pinned Research SHA and digests against the imported review artifact, never against a moving branch.

A root source identity registry remains identity-only, matching the Chapter-3 architecture: lane-local claim depth stays outside the root identity record.
