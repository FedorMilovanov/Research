# 1 Коринфянам 11:2–16 — deprecated legacy authority pointer

**Дата:** 2026-08-10  
**Статус:** `DEPRECATED-NAVIGATION-SHIM / PATH-PRESERVED / RESEARCH-ONLY / PUBLICATION-HOLD`

This historical path is preserved only so older links do not break. It is **not** a current authority file and must not supply grades, read order, relation types or Product data.

## Current route

Use:

1. [`00_CURRENT_INDEX_1COR11.md`](00_CURRENT_INDEX_1COR11.md) — navigation authority;
2. `00ZZZZZZZZZZZZZZZZZZ_CURRENT_CLAIM_REGISTRY_2026-08-10.md` — controlling claim grades;
3. `00ZZZZZ_SEGMENT_LEVEL_RELATION_MAP_1COR11_2_16_2026-08-10.md` — machine-facing relation types, subordinate to the claim registry for grades;
4. the specialized canonical audit / evergreen dossier named by the current index for evidence;
5. historical receipts only when distinct provenance is needed.

```text
THIS_FILE_CONTROLS_GRADES = false
THIS_FILE_CONTROLS_READ_ORDER = false
THIS_FILE_CONTROLS_RELATION_TYPES = false
THIS_FILE_CONTROLS_PRODUCT_DATA = false
CURRENT_INDEX_CONTROLS_NAVIGATION = true
CURRENT_CLAIM_REGISTRY_CONTROLS_GRADES = true
```

## Why the old synthesis was removed

This file previously called itself a “latest authority pointer” and embedded a snapshot of grades such as angel, Roman-trigger and `φύσις` labels. Those values can become stale while the controlling registry and evergreen owners continue to improve.

Keeping a second current-state summary here would recreate the supersession ladder this PR is removing.

```text
SNAPSHOT_GRADE_IN_LEGACY_POINTER = PROHIBITED
FILENAME_RECENCY != AUTHORITY
MORE_Z_CHARACTERS != MORE_CURRENT
DEPRECATED_POINTER != CURRENT_STATE_OWNER
```

The detailed historical version remains available in git history.

## Anti-sprawl / publication boundary

```text
DO_NOT_CREATE_NEW_Z_LADDER_POINTER = true
DO_NOT_CREATE_PASS_N_REPORT_IF_DOSSIER_EXISTS = true
UPDATE_EVERGREEN_DOSSIER = preferred
UPDATE_CURRENT_CLAIM_REGISTRY = only_if_grade_or_owner_changes
PRESERVE_OLD_PATH_AS_SHIM_IF_BACKLINKS_MAY_EXIST = true

PRODUCT_WRITE = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
RESEARCH_CLOSURE != PRODUCT_APPROVAL
```