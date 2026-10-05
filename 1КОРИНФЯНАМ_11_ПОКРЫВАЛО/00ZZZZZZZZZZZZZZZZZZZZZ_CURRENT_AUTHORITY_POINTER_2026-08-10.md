# 1 Коринфянам 11:2–16 — legacy current-authority pointer

**Дата:** 2026-08-10  
**Статус:** `DEPRECATED-NAVIGATION-SHIM / PATH-PRESERVED / RESEARCH-ONLY / PUBLICATION-HOLD`

## Current navigation

This historical path is intentionally preserved so older links do not break, but it is **no longer a current read-order owner**.

Use:

1. [`00_CURRENT_INDEX_1COR11.md`](00_CURRENT_INDEX_1COR11.md) — stable human-readable navigation authority;
2. `00ZZZZZZZZZZZZZZZZZZ_CURRENT_CLAIM_REGISTRY_2026-08-10.md` — controlling current claim grades;
3. the specialized dossier/audit named by the index for the claim being checked.

```text
THIS_FILE_CONTROLS_GRADES = false
THIS_FILE_CONTROLS_READ_ORDER = false
CURRENT_INDEX_CONTROLS_NAVIGATION = true
CURRENT_CLAIM_REGISTRY_CONTROLS_GRADES = true
```

## Why this file is now a shim

During the 2026-08-10 research marathon this file accumulated an ever-growing list of successor layers. That pattern caused navigation duplication:

```text
pointer
-> later pointer
-> later pointer
-> source delta
-> later correction
```

The current architecture replaces that ladder with:

```text
STABLE_INDEX
-> CLAIM_REGISTRY
-> EVERGREEN_DOSSIER_OR_CONTROLLING_AUDIT
-> HISTORICAL_RECEIPT_ONLY_WHEN_PROVENANCE_IS_NEEDED
```

The previous detailed contents remain available in git history and in the retained source-specific files. They are not repeated here.

## Anti-sprawl rule

```text
DO_NOT_CREATE_NEW_Z_LADDER_POINTER = true
DO_NOT_CREATE_PASS_N_REPORT_IF_DOSSIER_EXISTS = true
UPDATE_EVERGREEN_DOSSIER = preferred
UPDATE_CURRENT_CLAIM_REGISTRY = only_if_grade_or_owner_changes
PRESERVE_OLD_PATH_AS_SHIM_IF_BACKLINKS_MAY_EXIST = true
```

## Publication boundary

```text
PRODUCT_WRITE = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
RESEARCH_CLOSURE != PRODUCT_APPROVAL
```
