# 1 Peter Bot — Research Corpus

**Wave:** 2026-08-14  
**Status:** `RESEARCH-ONLY / FAIL-CLOSED / PUBLICATION-HOLD`  
**Research base:** `093cbfa541c6c94bd842dcb7ce52e6dc8ebfef88`  
**Working branch:** `agent/1peter-source-marathon`

This corpus supports the `bible-bot` First Peter course without collapsing textual criticism,
Greek, historical reconstruction, exegesis, project theology, and pedagogy into one undifferentiated
"source list".

## Read order

1. `00_CURRENT_WAVE_2026-08-14.md` — what this wave actually established.
2. `01_GREEK_TEXT_MANUSCRIPTS_AND_LEXICA.md` — Greek text, NA/UBS/ECM, manuscripts, lexicon protocol.
3. `02_EXEGETICAL_THEOLOGICAL_SOURCE_MAP.md` — TMS project anchor and independent controls.
4. `03_BOT_LEARNING_ARCHITECTURE.md` — how to turn scholarship into a bot for ordinary learners and advanced users.
5. `04_SOURCE_INDEX.md` — broad discovery/navigation index with 96 classified links.
6. `data/source-ledger-v1.json` — promoted fail-closed control set for 33 core sources.
7. `data/public-domain-acquisition-candidates.json` — lawful durable-custody queue for large/open historical materials.

## Current inventory

- **96 discovery/navigation sources** in the human-readable index.
- **33 promoted core sources** in the machine-readable evidence/access/rights ledger.
- **40 priority Greek lemmas/families** in the Greek research queue.
- Modern copyrighted books are links/catalog records, not mirrored PDFs.
- Public-domain/open materials are acquisition candidates only when durable custody adds value.
- Google Drive folder exists for lawful durable objects: `1 Peter Bot — Source Materials`.
- A Drive copy never creates publication rights.
- A source URL never proves a claim.
- A morphology tag never proves an interpretation.
- TMS/GTY may define the project's theological position, but never a neutral lexical or manuscript fact.

## Discovery index versus core ledger

`04_SOURCE_INDEX.md` is deliberately broad. It records promising sources and provisional inspection labels so future waves can navigate quickly. It does **not** claim that all 96 sources have been inspected to the same depth.

`data/source-ledger-v1.json` is deliberately narrower. A source is promoted there only when this wave is willing to make its current inspection/access/rights state part of the durable control plane.

Therefore:

```text
DISCOVERY_LINK != PROMOTED_CORE_SOURCE
PROMOTED_CORE_SOURCE != CLAIM_PROVED
CLAIM_PROVED != PUBLICATION_AUTHORIZED
```

## Product boundary

Nothing in this Research branch is automatically production-approved. A claim moves to the bot only
after claim-specific evidence, wording review, metadata classification, ranking review, and the
`bible-bot` exact-head gates required by its own `AGENTS.md`.
