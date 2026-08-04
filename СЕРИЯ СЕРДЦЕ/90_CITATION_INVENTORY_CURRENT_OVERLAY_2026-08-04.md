# Том 90. Citation inventory current overlay — «СЕРИЯ СЕРДЦЕ»

**Дата:** 2026-08-04  
**Authority ID:** `HEART-CITATION-INVENTORY-CURRENT-OVERLAY-2026-08-04`  
**Base current authority:** `00_CURRENT_AUTHORITY_2026-08-04.md`  
**Inventory authority:** `89_WHOLE_BOOK_CITATION_INVENTORY_2026-08-04.md`  
**Current encoding authority:** `data/heart-whole-book-citation-inventory-2026-08-04.v2.encoding.json`  
**Superseded transport:** `data/heart-whole-book-citation-inventory-2026-08-04.encoding.json`

## 1. Причина overlay

PR #108 сохранил deterministic inventory, encoded registry и validator, но merged workflow остался во временном bootstrap-режиме, а большой base-current snapshot не получил post-inventory navigation markers. Первый запуск permanent validator дополнительно доказал, что V1 chunks не реконструируют заявленный gzip stream.

Этот overlay не переписывает историю и не создаёт новых содержательных claims. Он:

1. объявляет том 89 действующим post-inventory authority layer;
2. закрепляет восстановление permanent read-only validator gate;
3. supersede-ит только повреждённый V1 transport новым V2 receipt;
4. уточняет текущий backlog после завершения inventory;
5. сохраняет все manuscript, citation-pass и release boundaries открытыми.

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

## 3. Versioned transport correction

```text
DECODED INVENTORY AUTHORITY = HEART-WHOLE-BOOK-CITATION-INVENTORY-2026-08-04
DECODED JSON BYTES = 285803
DECODED JSON SHA-256 = b25ff1a498057f6c20d92e5f98965338c40a9de752af198e9de97fefcf81b000
CURRENT TRANSPORT AUTHORITY = HEART-WHOLE-BOOK-CITATION-INVENTORY-ENCODING-V2-2026-08-04
CURRENT GZIP SHA-256 = e1aea3fdbe537972bfc9382d2fa0267d661dd70f5929602ecfcd50dda5f0f834
CORRUPTED V1 TRANSPORT = SUPERSEDED BY V2
```

V2 changes storage transport only. It is reconstructed from the same canonical JSON artifact and must decode to the same pinned JSON SHA before fresh-scan comparison. V1 remains historical evidence of the detected failure and is not accepted as current transport authority.

## 4. Permanent gate

The Heart workflow must execute:

```text
python3 scripts/validate_heart_whole_book_citation_inventory.py --product-root ../Product
```

Acceptance requires all of the following:

- verify the V2 manifest and four normalized base64 chunk hashes;
- decode the exact V2 gzip stream;
- verify gzip and decoded JSON sizes and SHA-256;
- require decoded JSON SHA `b25ff1a498057f6c20d92e5f98965338c40a9de752af198e9de97fefcf81b000`;
- parse the full eighteen-entry inventory;
- execute a fresh read-only scan against pinned Product commit `0fbe7d1ead9ebd1bea867418e254da438ec63329`;
- compare the complete canonical JSON structures;
- leave both Research and Product checkouts clean.

The workflow must not generate the registry with `--write`, upload a bootstrap artifact, mutate its own branch or accept a dirty checkout as the permanent state.

## 5. Interpretation boundaries

```text
CITATION INVENTORY COMPLETE ≠ WHOLE-BOOK CITATION PASS COMPLETE
SCRIPTURE TOKEN DETECTED ≠ REFERENCE VERIFIED
QUOTATION SURFACE DETECTED ≠ DIRECT QUOTATION APPROVED
EXTERNAL LINK PRESENT ≠ SOURCE ADEQUATE
OWNER MAPPED ≠ READER MANUSCRIPT ASSEMBLED
TRANSPORT REPAIRED ≠ INVENTORY CONTENT CHANGED
```

No manuscript was changed by this repair. No quotation, locator, edition or Scripture version was approved by implication.

## 6. What is closed by this transaction

```text
POST-INVENTORY AUTHORITY NAVIGATION = CLOSED
PERMANENT INVENTORY WORKFLOW BINDING = CLOSED
BOOTSTRAP --write MODE IN PERMANENT CI = REMOVED
BOOTSTRAP ARTIFACT UPLOAD IN PERMANENT CI = REMOVED
CORRUPTED V1 TRANSPORT = SUPERSEDED BY V2
V2 MANIFEST AND FOUR PARTS = COMMITTED
ENCODED REGISTRY FRESH-SCAN DRIFT GUARD = BOUND
```

## 7. What remains open

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

## 8. Next canonical transaction

Build one explicit entry-disposition registry over the committed inventory. Each of the eighteen rows must preserve its detected surfaces and record:

- review state;
- Scripture-normalization blockers;
- quotation-classification blockers;
- source/locator/version blockers;
- external-link blockers;
- reader-assembly dependency;
- explicit citation-pass disposition.

The registry may close triage coverage for all eighteen entries, but it may not mark an entry citation-pass complete until its actual blockers have been reviewed and resolved.

## 9. Decision

Authority `HEART-CITATION-INVENTORY-CURRENT-OVERLAY-2026-08-04` composes the base current authority with the deterministic inventory and the current V2 transport. The inventory itself is complete, the permanent fail-closed gate is restored, V1 transport is superseded, and entry-level citation completion remains exactly `0 / 18`.
