# OSK public-projection overlay — current through Wave 11

**Current overlay authority:** `A06-OSK-CURRENT-PROJECTION-2026-08-02`  
**Supersedes:** `A06-OSK-WAVE6-PROJECTION-2026-08-01`  
**Base queue authority:** `A06-RESEARCH-PUBLIC-PROJECTION-2026-08-01`  
**Replaced record:** `osk-power-dark-side-standalone`  
**Research authority snapshot:** `1466b65a4449bac968a28d7da2d2b78db545e29e`  
**Product snapshot:** `efaf2a51b1fcc7b7d3f8c9558ecb5acf849df3b3`

## Effective decision

```text
REFERENCE / PUBLICATION_HOLD
WAVES_1_TO_11_RESEARCH_CLOSED_PRODUCT_PUBLICATION_HOLD
```

The historical base record that described Waves 1–4 and an active Wave 5 is no longer current. Waves 1–11 are recorded as completed Research/integration stages, with effective routing:

```text
21 CORE / 1 CONDITIONAL / 7 DARK_SIDE / 4 STANDALONE / 0 HOLD
```

This remains `REFERENCE`, not `PROMOTE`, because Wave 11 does not prove a live public release. Wave 12 must separately verify the exact Product commit, target route, bounded approved edits, build result and live-route witness.

## Effective counts

```text
PROMOTE: 0
REFERENCE: 4
SUPERSEDED: 0
BLOCKED: 6
total: 10
```

## Machine authority

- base queue: `data/public-projection-queue-2026-08-01.json`;
- current overlay: `data/public-projection-osk-wave6-overlay-2026-08-01.json`;
- canonical composition descriptor: `data/public-projection-current-2026-08-02.json`.

The base queue must never be consumed alone as current state.
