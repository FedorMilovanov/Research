# Research → public projection current authority

**Current authority ID:** `RESEARCH-PUBLIC-PROJECTION-CURRENT-2026-08-02`  
**Status:** `CURRENT / FAIL-CLOSED / NO AUTOMATIC PROMOTION`  
**Composition:** `base + overlay`  
**Research authority snapshot:** `1466b65a4449bac968a28d7da2d2b78db545e29e`  
**Product source snapshot:** `e604b97dbbe45cf9ba9e2a84551b799f0dac1a0e`  
**Production verification:** `NOT CLAIMED`

## Canonical machine entry point

Consumers must start with:

- [`data/public-projection-current-2026-08-02.json`](data/public-projection-current-2026-08-02.json)

It composes:

1. historical base queue [`data/public-projection-queue-2026-08-01.json`](data/public-projection-queue-2026-08-01.json);
2. required current overlay [`data/public-projection-osk-wave6-overlay-2026-08-01.json`](data/public-projection-osk-wave6-overlay-2026-08-01.json).

The base queue by itself is **not current authority**. A consumer that does not apply every overlay is invalid.

## Effective counts

- `PROMOTE: 0`
- `REFERENCE: 4`
- `SUPERSEDED: 0`
- `BLOCKED: 6`
- `total: 10`

## Effective record table

| Record | Disposition | Governing boundary |
|---|---|---|
| `heart-series-source-closure` | `REFERENCE` | Nine quote-safe claims only; `PUBLICATION_HOLD` |
| `osk-power-dark-side-standalone` | `REFERENCE` | `WAVES_1_TO_11_RESEARCH_CLOSED_PRODUCT_PUBLICATION_HOLD`; Wave 12 source route accepted, live deployment still unverified |
| `bratsky-listok-1906-1910` | `BLOCKED` | archive, locator, rights and publication holds |
| `baptist-archive-v156` | `BLOCKED` | scans/OCR/visual verification and route-level claim mapping required |
| `genesis6-enoch-hard-texts` | `REFERENCE` | active authority graph closed; reader wording still requires bounded re-verification |
| `gill-archive-families` | `BLOCKED` | closed-book provenance, locator and rights backlog |
| `biblical-atlas-primary-strengthening` | `BLOCKED` | Pihahiroth and map/base-image evidence and rights unresolved |
| `source-library-ephemera-63` | `BLOCKED` | archive approval is not route or publication approval |
| `source-library-editorial-40-pdf` | `REFERENCE` | research navigation only; embedded rights remain item-specific |
| `source-library-poet-portraits-45` | `BLOCKED` | human identity and item-level rights review required |

## OSK effective authority

The old base record `WAVES_1_TO_4_CLOSED_WAVE5_AND_SITE_TRANSFER_ACTIVE` is superseded.

Current OSK research/publication status remains:

```text
WAVES_1_TO_11_RESEARCH_CLOSED_PRODUCT_PUBLICATION_HOLD
21 CORE / 1 CONDITIONAL / 7 DARK_SIDE / 4 STANDALONE / 0 HOLD
```

Wave 12 source acceptance is now complete:

- Product PR `#810`;
- exact verified head `f39589d8920ae828c13ee5fd804a79433be7bd82`;
- source merge `e604b97dbbe45cf9ba9e2a84551b799f0dac1a0e`;
- route `/articles/diotrefy-nashego-vremeni/`;
- exact-head source/browser checks green;
- production/live verification: **not claimed**.

This source acceptance does not prove deployed bytes or authorize automatic promotion. `PUBLICATION_HOLD` remains until a separate same-release production witness verifies the live route, metadata, search, print, no-JS and browser behavior, followed by an explicit disposition decision.

## Non-negotiable rules

- Research presence is not publication approval.
- Source merge is not production verification.
- Drive or artifact custody is not a rights decision.
- A reachable URL is not verified content.
- `PROMOTE` requires zero holds, verified faithful wording and all applicable rights decisions.
- Overlays must be applied by record ID and effective counts must be recomputed.
- No corpus may silently reuse another corpus's evidence-class semantics.

## Validation

The composed authority is enforced by:

- [`scripts/validate_public_projection_queue.py`](scripts/validate_public_projection_queue.py)
- [`.github/workflows/public-projection-queue.yml`](.github/workflows/public-projection-queue.yml)
- [`scripts/validate_repository_authority_integrity.py`](scripts/validate_repository_authority_integrity.py)
