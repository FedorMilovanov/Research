# Research — current authority

**Дата:** 2026-08-03  
**Authority ID:** `RESEARCH-CURRENT-AUTHORITY-2026-08-02`  
**Статус:** `CURRENT / STAGE-BASED / FAIL-CLOSED`  
**Machine stage registry:** `data/research-stage-closure-2026-08-02.json`  
**Control plane:** `00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md`

## 1. Как читать текущий Research

Этот файл является корневой status/navigation authority. Он не заменяет corpus-specific evidence owners. Он определяет, какой этап реально доказан, какой boundary остаётся открытым и какой следующий lane допустим.

Порядок чтения:

1. этот root authority;
2. machine stage registry;
3. corpus current authority;
4. machine evidence/projection registry;
5. historical closeouts — только как provenance, не как текущий status.

`Закрыто` означает завершение названного этапа, а не исчезновение всякой будущей работы по теме. Source merge, CI, Research closure, reader assembly и production/live verification являются разными событиями.

## 2. Stage matrix

| Stage | Current state | Что доказано | Следующий lane |
|---|---|---|---|
| OSK Wave 12 | `SOURCE ACCEPTED / LIVE VERIFICATION OPEN` | Product PR `#810`, exact head `f39589d…`, source merge `e604b97…`, exact-head checks green, route source present | same-release production/live witness; explicit disposition decision |
| Heart P0 | `RESEARCH + THREE READER CHAPTERS CLOSED` | 3 dossiers, 17 sources, 26 claim nodes, 3 reader chapters, 18-entry order, 0 new direct quotes | whole-book line edit, citation pass, separate Product release |
| Atlas Pihahiroth | `RESEARCH CLOSED AS UNCERTAINTY GEOMETRY` | 8 textual constraints, 3 candidate corridors, no authoritative point | Product polygons, dated palaeowater layer, credits |
| Baptist scan acquisition | `REQUEST/RECEIPT SYSTEM CLOSED` | deterministic requests and fail-closed byte/OCR/rights receipts | external delivery, OCR, visual review |
| Gill closed books | `OWNERSHIP/ACCEPTANCE CLOSED` | 7 claim-owned acquisition families and receipt criteria | external acquisition family by family |
| Source URL repairs | `CONFIRMED SET CLOSED` | 7 replacements + 1 version-history endpoint; rights holds preserved | remaining true-dead queue item by item |

## 3. OSK — Wave 12 source accepted, production not claimed

Current authority:

- `PUBLIC_PROJECTION_CURRENT_AUTHORITY_2026-08-01.md`;
- `data/public-projection-current-2026-08-02.json`;
- `data/public-projection-osk-wave6-overlay-2026-08-01.json`;
- `00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md`.

Current proven result:

```text
ROUTE = /articles/diotrefy-nashego-vremeni/
PRODUCT PR = #810
EXACT VERIFIED HEAD = f39589d8920ae828c13ee5fd804a79433be7bd82
SOURCE MERGE = e604b97dbbe45cf9ba9e2a84551b799f0dac1a0e
EXACT-HEAD CHECKS = GREEN
DISPOSITION = REFERENCE
HOLDS = [PUBLICATION_HOLD]
PRODUCTION READBACK = NOT VERIFIED
NEW DIRECT QUOTES = 0
```

Wave 12 source acceptance does **not** prove deployed bytes. No production receipt exists in current authority. The next valid action is a separate same-release live witness for route bytes, metadata, search, print, no-JS and browser behavior, followed by an explicit decision whether `PUBLICATION_HOLD` may be removed.

Forbidden claims:

- `PROMOTE` before the live witness;
- `holds=[]` before the explicit disposition decision;
- `productionReadback=true` without an actual receipt;
- creation of placeholder receipt files merely to satisfy CI.

## 4. «СЕРИЯ СЕРДЦЕ» — evidence and three reader chapters assembled

Current authority:

- `СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-02.md`;
- `СЕРИЯ СЕРДЦЕ/78_P0_ARCHITECTURE_CLOSURE_OVERLAY_2026-08-02.md`;
- `data/heart-p0-architecture-dossiers-2026-08-02.json`;
- `data/heart-reader-assembly-2026-08-02.json`;
- `СЕРИЯ СЕРДЦЕ/82_BOOK_ASSEMBLY_DECISIONS_2026-08-02.md`;
- dossiers 75–77 and reader chapters 79–81.

Closed:

1. I.2 — «Сердце в Эдеме»;
2. III.3 — «Сокрушённое сердце: покаяние»;
3. X.1 — «Суд сердца: два воскресения»;
4. three reader-chapter assemblies;
5. 18-entry book order;
6. R9 and `katoptrizomenoi` editorial roles;
7. zero new direct quotations.

Still open:

- whole-book line edit;
- whole-book citation pass;
- cross-chapter deduplication QA;
- separate Product implementation and release witness.

Three assembled chapters must not be described as a completely edited, cited or published book.

## 5. БИБЛЕЙСКИЙ АТЛАС — Pihahiroth closed honestly

Current authority:

- `БИБЛЕЙСКИЙ АТЛАС/00_CURRENT_AUTHORITY_2026-08-02.md`;
- `БИБЛЕЙСКИЙ АТЛАС/GEO-DOSSIER-pihahiroth.md`;
- `data/atlas-pihahiroth-authority-2026-08-02.json`.

Closed decision:

```text
TEXTUAL CONSTRAINTS = CLOSED
CANDIDATE CORRIDORS = CLOSED
MAP/RIGHTS CONTRACT = CLOSED
EXACT COORDINATE = UNRESOLVED
SINGLE AUTHORITATIVE POINT = FORBIDDEN
```

The remaining task is implementation of uncertainty polygons, not another general research pass.

## 6. Баптистские архивы — operational lane closed, files external

Current authority:

- `RUSSIAN_BAPTISTS_ARCHIVE/SCAN_ACQUISITION_CURRENT_AUTHORITY_2026-08-02.md`;
- `data/baptist-scan-acquisition-policy-v2.json`;
- `data/baptist-scan-receipts-v1.json`;
- `scripts/build_baptist_scan_request_package.py`.

Current honest receipt state:

```text
REQUEST PACKAGE = READY
VERIFIED FILE RECEIPTS = 0
OCR COMPLETE = 0
QUOTE READY = 0
```

Institutional/private delivery is an external dependency. A catalog card, holding row, filename or viewer manifest cannot be promoted to a scan receipt.

## 7. Джон Гилл — closed-book backlog owned, bytes still external

Current authority:

- `Джон Гилл/75_CLOSED_BOOK_FAMILY_ACQUISITION_AUTHORITY_2026-08-02.md`;
- `data/gill-closed-book-families-2026-08-02.json`.

The former undifferentiated backlog is replaced by seven bounded families: Park, Strother, Ascol, Walden, biographical primary witnesses, first editions and the canonical physical package. Each family has owner documents, claim scope, request queries and acceptance criteria.

```text
FAMILIES = 7
VERIFIED PACKAGE RECEIPTS = 0
QUOTE-READY FAMILIES = 0
NEW DIRECT QUOTES = 0
```

## 8. Source Library — confirmed URL set closed

Current authority:

- `SOURCE_LIBRARY/CURRENT_SOURCE_URL_AUTHORITY_2026-08-02.md`;
- `data/source-url-replacements-2026-08-02.json`.

Closed:

- seven confirmed replacements;
- one 4Q204 version-history endpoint;
- pinned 4Q204 transcription version;
- preserved Duncan item-level rights holds;
- separation of transcription rights from manuscript-photo rights.

The remaining true-dead queue is still active item-by-item work. The confirmed decisions do not claim closure of all historical rows.

## 9. Meaning of external dependency

An external dependency is not an unowned question. It has:

- a named owner stage;
- request/acceptance schema;
- receipt requirements;
- a prohibited false-completion boundary;
- a valid next action.

Examples are institutional scan delivery, closed-book full-text delivery and an independent production/live witness. CI cannot fabricate those bytes or observations.

## 10. Global forbidden claims

Do not claim:

- that every Baptist or Gill file has been acquired;
- that OCR is complete without byte receipt and page review;
- that Pihahiroth has one proven coordinate;
- that three Heart chapters mean the whole book is edited or published;
- that a repaired URL clears image rights;
- that a Research commit or Product source merge proves live deployment;
- that a CI result proves facts outside the contract it ran.

## 11. Current next-action order

1. **OSK:** obtain a same-release production/live witness; keep `REFERENCE + PUBLICATION_HOLD` until then.
2. **Heart:** run whole-book line edit, citation pass and deduplication QA; Product release remains separate.
3. **Atlas Product:** implement three uncertainty corridors with dated source/rights metadata.
4. **Baptist external lane:** send generated requests; append receipts only on actual file delivery.
5. **Gill external lane:** acquire one family at a time and map it to owner claims.
6. **Source Library:** continue the remaining true-dead URL queue item by item.

## 12. Decision

Authority `RESEARCH-CURRENT-AUTHORITY-2026-08-02` supersedes `00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md` only as root status/navigation. Historical and corpus evidence remains preserved. The previous root claim that OSK had `PROMOTE`, no holds and verified production readback is retracted as unsupported; current authority records only source acceptance and keeps the live-verification boundary open.
