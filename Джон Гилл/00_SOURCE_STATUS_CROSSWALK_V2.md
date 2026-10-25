# John Gill source/access crosswalk v2

**Authority:** `GILL-SOURCE-STATUS-CROSSWALK-2026-08-02`  
**Status:** `CURRENT / SUPERSEDES THE “A1–X” SEMANTICS IN 00_README_AND_NAVIGATION.md`

The labels `A1/A2/A3/B1/B2/B3/C1/C2/X` used in older Gill volumes were a combined source-and-access shorthand. They are retained only as historical field values and must not be interpreted as the repository-wide evidence classes.

In particular, historical Gill `A3` meant “official bibliographic record without a full file.” Global `A3` now means an official event-specific statement, board decision or institutional document. These meanings are not interchangeable.

## Required normalized fields

Every new or materially updated Gill source record must separate:

- `evidenceClass`: global `A1/A2/A3/B1/C/D` from `../data/repository-evidence-policy-v2.json`;
- `accessState`: `FULL_OBJECT_VERIFIED`, `PARTIAL_OBJECT`, `CATALOG_ONLY`, `LINK_ONLY`, `NOT_ACQUIRED`;
- `locatorState`: `EXACT_LOCATOR_VERIFIED`, `COARSE_LOCATOR_ONLY`, `LOCATOR_MISSING`;
- `rightsState`: `PUBLICATION_ELIGIBLE`, `STORAGE_ONLY`, `PRIVATE_STUDY_ONLY`, `PERMISSION_REQUIRED`, `RIGHTS_UNKNOWN`;
- `publicationState`: `PROMOTE`, `REFERENCE`, `SUPERSEDED`, `BLOCKED`;
- typed holds where applicable.

## Legacy crosswalk

| Historical Gill value | Evidence interpretation | Access interpretation | Mandatory boundary |
|---|---|---|---|
| `A1` | usually primary source; assign global class case by case | `FULL_OBJECT_VERIFIED` | exact locator still required for quotations |
| `A2` | primary text reproduction; assign global class case by case | `FULL_OBJECT_VERIFIED` or `PARTIAL_OBJECT` | compare with facsimile/second witness where wording matters |
| `A3` | **not an evidence class** | `CATALOG_ONLY` | cannot support a verbatim claim |
| `B1/B3` | normally `B1`, occasionally global `A2` only for a genuine official primary report | full secondary object | no silent promotion to primary evidence |
| `B2` | `B1` or `C` | `PARTIAL_OBJECT` | abstract/preview is not page-verified evidence |
| `C1/C2` | `C` unless independently upgraded | varies | navigation/corroboration only; not quote-safe |
| `X` | no class assigned yet | `NOT_ACQUIRED` or `LOCATOR_MISSING` | retain appropriate HOLD |

## Migration rule

Old volumes need not be destructively rewritten. Any machine registry, new synthesis or Product transfer must apply this crosswalk and output normalized fields. A bare historical `A3`, `B2` or `X` may not cross the publication boundary.
