# 1 Коринфянам 11:2–16 — current authority pointer after Greek text-base audit

**Дата:** 2026-08-10  
**Статус:** `LATEST-AUTHORITY-POINTER / GNT6-CURRENT-BASE / RESEARCH-ONLY / PUBLICATION-HOLD`

## Start here

1. `00ZZZZZZZZZZZZZZZZZZ_CURRENT_CLAIM_REGISTRY_2026-08-10.md` — current exegetical claim grades.
2. `00ZZZZZZZZZZZZZZZZZZ_AUTHORITY_RECONCILIATION_AND_SUPERSESSION_2026-08-10.md` — authority/supersession rule.
3. **`00ZZZZZZZZZZZZZZZZZZZ_CURRENT_GREEK_TEXT_BASE_AND_TEXTUAL_RISK_AUDIT_2026-08-10.md`** — current Greek-edition contract.
4. `00Z_MAIN_SYNTHESIS_AUTHORITY_AND_SUPERSESSION_2026-08-09.md` — provenance/publication boundary.

---

## Current Greek text authority

```text
CURRENT_PUBLISHED_GREEK_BASE = GNT6_2025
FUTURE_NA29_TEXT = IDENTICAL_TO_GNT6_BY_OFFICIAL_PUBLISHER
NA29_PUBLISHED_AS_OF_2026_08_10 = false
NA29_SCHEDULED_PUBLICATION = 2027-02-28
COMPLETED_PAULINE_ECM_FOR_1COR = false
```

Do not call NA29 the currently published physical edition yet.

Do not describe 1 Cor 11 as using a completed Pauline ECM text.

---

## Text vs apparatus distinction

```text
GNT6_TEXT_EQUALS_FUTURE_NA29_TEXT = true
GNT6_APPARATUS_EQUALS_FUTURE_NA29_APPARATUS = DO_NOT_ASSUME
```

GNT6’s official description states that apparatus witness selection was comprehensively revised, including Pauline adjustments. A stable base text therefore does not mean apparatus information is frozen.

---

## Current claim snapshot remains controlled by registry

No exegetical core grade was changed by the edition-status audit.

The current registry still controls:

```text
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
KEPHALE_HEADSHIP_AUTHORITY = B_LEADING
CREATION_ORDER/ASYMMETRY = B_HIGH
EXOUSIA_WOMAN_SUBJECT = A
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH
EXOUSIA_REFERENT = B_C
HEAVENLY_HOLY_ANGELS_REFERENT = B_HIGH_LEADING
EXACT_ANGELIC_FUNCTION = B_C
WATCHERS = C_SERIOUS_ALTERNATIVE
PHYSIS_SEXED_NATURALIZED_PROPRIETY = B_HIGH_LEADING
ROMAN_CAPITE_VELATO_BACKGROUND = A
V4_EXACT_CAPITE_VELATO = B_C
WIVES_VS_ALL_WOMEN = OPEN_B_C
MUTUAL_INTERDEPENDENCE_11_11_12 = A
V16_TRANSLOCAL_CHURCH_PRACTICE_APPEAL = A
V16_EXACT_CUSTOM_REFERENT = B_C
```

---

## Future Greek/Russian matrix contract

The Product TЗ remains non-implemented, but Research now supplies the text-base requirement:

```text
greek_base_edition = GNT6_2025
textual_variant_risk = required per segment
semantic_uncertainty != textual_variant_uncertainty
text_authority != automatic redistribution_right
```

A future apparatus-level pass must directly inspect current GNT6/official manuscript evidence before assigning claim-specific variant-risk grades.

---

## Boundary

```text
DO_NOT_REQUEST_FROM_USER_IF_AGENT_CAN_ACCESS = true
PRODUCT_WRITE = false
UI_IMPLEMENTATION = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
```
