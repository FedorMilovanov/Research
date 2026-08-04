# Том 90. Citation inventory current overlay — «СЕРИЯ СЕРДЦЕ»

**Дата:** 2026-08-04  
**Authority ID:** `HEART-CITATION-INVENTORY-CURRENT-OVERLAY-2026-08-04`  
**Base current authority:** `00_CURRENT_AUTHORITY_2026-08-04.md`  
**Inventory authority:** `89_WHOLE_BOOK_CITATION_INVENTORY_2026-08-04.md`  
**Encoding authority:** `data/heart-whole-book-citation-inventory-2026-08-04.encoding.json`

## 1. Причина overlay

PR #108 сохранил deterministic inventory, encoded registry и validator, но merged workflow остался во временном bootstrap-режиме, а большой base-current snapshot не получил post-inventory navigation markers.

Этот overlay не переписывает историю и не создаёт новых содержательных claims. Он:

1. объявляет том 89 действующим post-inventory authority layer;
2. закрепляет восстановление permanent read-only validator gate;
3. уточняет текущий backlog после завершения inventory;
4. сохраняет все manuscript, citation-pass и release boundaries открытыми.

## 2. Текущий composed state

```text
ALL 18 ENTRIES OWNER-MAPPED = TRUE
ASSEMBLED READER OWNERS = 4
PRODUCT SOURCE OWNERS = 8
RESEARCH DOSSIER OWNERS = 6
STANDALONE OWNER GAPS = 0
CITATION INVENTORY = COMPLETE
FINAL BOOK ENTRIES SCANNED = 18 / 18
UNIQUE OWNER FILES = 31
OWNER SURFACES SCANNED = 38
UNIQUE SCRIPTURE REFERENCES = 1063
UNIQUE EXTERNAL LINKS = 414
UNIQUE INTERNAL ARTICLE LINKS = 22
MARKDOWN BLOCKQUOTE SURFACES = 1115
INLINE QUOTATION SURFACES = 3271
ENTRY CITATION PASS COMPLETE = 0 / 18
ENTRIES REQUIRING MANUAL BOOK REVIEW = 18 / 18
NEW DIRECT QUOTES APPROVED = 0
WHOLE-BOOK READER ASSEMBLY = INCOMPLETE
WHOLE-BOOK CITATION PASS = OPEN
WHOLE-BOOK TRANSITION AND DEDUP PASS = OPEN
WHOLE-BOOK LINE EDIT = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT RELEASE = NOT CLAIMED
```

## 3. Permanent gate

The Heart workflow must now execute:

```text
python3 scripts/validate_heart_whole_book_citation_inventory.py --product-root ../Product
```

Acceptance requires all of the following:

- verify four normalized base64 chunk hashes;
- decode the exact gzip stream;
- verify gzip and decoded JSON sizes and SHA-256;
- parse the full eighteen-entry inventory;
- execute a fresh read-only scan against pinned Product commit `0fbe7d1ead9ebd1bea867418e254da438ec63329`;
- compare the complete canonical JSON structures;
- leave both Research and Product checkouts clean.

The workflow must not generate the registry with `--write`, upload a bootstrap artifact or accept a dirty checkout as the permanent state.

## 4. Interpretation boundaries

```text
CITATION INVENTORY COMPLETE ≠ WHOLE-BOOK CITATION PASS COMPLETE
SCRIPTURE TOKEN DETECTED ≠ REFERENCE VERIFIED
QUOTATION SURFACE DETECTED ≠ DIRECT QUOTATION APPROVED
EXTERNAL LINK PRESENT ≠ SOURCE ADEQUATE
OWNER MAPPED ≠ READER MANUSCRIPT ASSEMBLED
```

No manuscript was changed by this repair. No quotation, locator, edition or Scripture version was approved by implication.

## 5. What is closed by this transaction

```text
POST-INVENTORY AUTHORITY NAVIGATION = CLOSED
PERMANENT INVENTORY WORKFLOW BINDING = CLOSED
BOOTSTRAP --write MODE IN PERMANENT CI = REMOVED
BOOTSTRAP ARTIFACT UPLOAD IN PERMANENT CI = REMOVED
ENCODED REGISTRY FRESH-SCAN DRIFT GUARD = BOUND
```

## 6. What remains open

```text
ENTRY-LEVEL CITATION DISPOSITION = 0 / 18
DIRECT-QUOTATION CANDIDATE CLASSIFICATION = OPEN
SCRIPTURE VERSION / ABBREVIATION NORMALIZATION = OPEN
MISSING LOCATORS AND EDITION IDENTIFIERS = OPEN
EXTERNAL-LINK ADEQUACY REVIEW = OPEN
NINE READER ASSEMBLIES = OPEN
WHOLE-BOOK TRANSITION AND DEDUP PASS = OPEN
WHOLE-BOOK LINE EDIT = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT RELEASE = NOT CLAIMED
```

## 7. Next canonical transaction

Build one explicit entry-disposition registry over the committed inventory. Each of the eighteen rows must preserve its detected surfaces and record:

- review state;
- Scripture-normalization blockers;
- quotation-classification blockers;
- source/locator/version blockers;
- external-link blockers;
- reader-assembly dependency;
- explicit citation-pass disposition.

The registry may close triage coverage for all eighteen entries, but it may not mark an entry citation-pass complete until its actual blockers have been reviewed and resolved.

## 8. Decision

Authority `HEART-CITATION-INVENTORY-CURRENT-OVERLAY-2026-08-04` composes the base current authority with the deterministic inventory. The inventory itself is complete, the permanent fail-closed gate is restored, and entry-level citation completion remains exactly `0 / 18`.
