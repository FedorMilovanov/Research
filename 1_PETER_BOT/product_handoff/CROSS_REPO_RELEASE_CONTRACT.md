# Cross-repository Chapter 4–5 release audit contract

This contract defines a metadata bridge only. It creates no runtime dependency from bible-bot to Research.

Every product card derived from the Chapter 4–5 Research corpus must be traceable as:

`PRODUCT_CARD -> PRODUCT_REVIEW_RECORD -> RESEARCH_CLAIM_ID -> EFFECTIVE_RESEARCH_RECORD -> SOURCE OWNER -> INSPECTION DEPTH`

A release audit MUST fail if any edge cannot be resolved.

## Minimal product-side bridge

Each product card or its immutable review record must carry:

- `research_claim_id`: exact `w3q_*` ID.
- `research_authority_sha`: Research commit reviewed for the product card; never a floating branch.
- `research_handoff_schema_version`.
- `product_review_record_id`: stable ID for the separate product editorial/source review.
- `claimed_position`: `neutral` or `project`; must equal the effective Research position unless the product review is narrowing the claim.
- `claimed_confidence`: may stay equal or become more conservative; it may not be raised above Research authority.
- `source_ids`: subset/equal set explicitly used by the product claim; adding a source requires a new product review rather than inheriting unrelated Research depth.
- `claim_inspection_edge_ids` or the exact `(research_claim_id, source_id, owning_lane)` tuples used by review.
- `ranking_review_id`: required only if a card is proposed for ranking; Research handoff never supplies this implicitly.

## Release failures

Fail release when:

1. `research_claim_id` does not exist in the pinned Research authority.
2. the product wording is stronger than `product_safe_phrasing` or violates any `prohibited_overclaim` rule without a newly documented evidence lane.
3. product position changes `project -> neutral` or confidence is raised without a new reviewed provenance record.
4. a source is present only in the identity package but no claim/source owning inspection edge exists.
5. inspection depth is borrowed from another candidate or lane merely because the bibliographic `source_id` is the same.
6. a textual-critical claim turns named-witness evidence, secondary apparatus, ECM decision, or ECM-based commentary into a stronger witness-distribution/direct-dECM claim.
7. a 5:2 product card crosses evidence between `ἐπισκοποῦντες` and `κατὰ θεόν`.
8. a Research prototype is treated as an approved product card without a separate `product_review_record_id`.
9. ranking is enabled without an independent product ranking review satisfying the Chapter 3-style standard.

## Repository independence

bible-bot may vendor/export a reviewed immutable handoff snapshot or copy the minimal metadata above. It must not fetch Research at runtime. Release CI should validate the pinned Research SHA and trace metadata against the imported review artifact, not against a moving branch.
