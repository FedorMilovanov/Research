# Research — current authority

**Дата:** 2026-08-02  
**Authority ID:** `RESEARCH-CURRENT-AUTHORITY-2026-08-02`  
**Статус:** `CURRENT / STAGE-BASED / FAIL-CLOSED`  
**Machine stage registry:** `data/research-stage-closure-2026-08-02.json`  
**Control plane:** `00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md`

## 1. Как читать текущий Research

Этот файл является единственной корневой status/navigation authority после 2026-08-02. Он не заменяет corpus-specific evidence owners. Он определяет, какой этап закрыт, каким witness это подтверждено и какой следующий lane допустим.

Порядок:

1. этот root authority;
2. machine stage registry;
3. corpus current authority;
4. machine evidence/receipt registry;
5. historical closeouts — только как provenance, не как текущий status.

`Закрыто` означает завершение названного этапа, а не исчезновение всякой будущей работы по теме.

## 2. Stage matrix

| Stage | Current state | Что доказано | Следующий lane |
|---|---|---|---|
| OSK Wave 12 | `CLOSED WITH CI + PRODUCTION READBACK` | public Product route, 181 sources, 73 reader links, 0 new direct quotes, projection `PROMOTE`, holds `[]` | maintenance / future editorial waves |
| Heart P0 | `RESEARCH CLOSED` | 3 dossiers, 17 sources, 26 claim nodes, negative boundaries | reader chapter assembly, book copyedit, later Product release |
| Atlas Pihahiroth | `RESEARCH CLOSED AS UNCERTAINTY GEOMETRY` | 8 textual constraints, 3 candidate corridors, no authoritative point | Product polygons, dated palaeowater layer, credits |
| Baptist scan acquisition | `REQUEST/RECEIPT SYSTEM CLOSED` | deterministic requests and fail-closed byte/OCR/rights receipts | external delivery, OCR, visual review |
| Gill closed books | `OWNERSHIP/ACCEPTANCE CLOSED` | 7 claim-owned acquisition families and receipt criteria | external acquisition family by family |
| Source URL repairs | `CONFIRMED SET CLOSED` | 7 replacements + 1 version-history endpoint; rights holds preserved | remaining true-dead queue item by item |

## 3. OSK — Product publication completed

Current authority:

- `PUBLIC_PROJECTION_CURRENT_AUTHORITY_2026-08-02_V2.md`;
- `data/public-projection-current-2026-08-02-v2.json`;
- `data/public-projection-osk-wave12-overlay-2026-08-02.json`;
- `data/osk-wave12-product-release-receipt-2026-08-02.json`;
- `data/public-projection-wave12-ci-receipt.json`;
- `ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/45_WAVE12_PRODUCT_PUBLICATION_RELEASE_2026-08-02.md`.

Result:

```text
/articles/diotrefy-nashego-vremeni/
PRODUCT CI = SUCCESS
PRODUCTION READBACK = VERIFIED
DISPOSITION = PROMOTE
HOLDS = []
AUTHORITY SOURCES = 181
READER LINKS = 73
NEW DIRECT QUOTES = 0
```

Wave 6 projection remains historical. Current projection is computed as historical base queue plus required Wave 12 overlay.

## 4. «СЕРИЯ СЕРДЦЕ» — research gaps closed

Current authority:

- `СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-02.md`;
- `СЕРИЯ СЕРДЦЕ/78_P0_ARCHITECTURE_CLOSURE_OVERLAY_2026-08-02.md`;
- `data/heart-p0-architecture-dossiers-2026-08-02.json`;
- dossiers 75–77.

Closed evidence scopes:

1. I.2 — Сердце в Эдеме;
2. III.3 — Сокрушённое сердце: покаяние;
3. X.1 — Суд сердца: два воскресения.

These themes must not reappear as `missing research`. Reader prose, transitions, deduplication and book-level production remain editorial work and require a separate Product witness.

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

## 7. Джон Гилл — closed-book backlog now owned

Current authority:

- `Джон Гилл/75_CLOSED_BOOK_FAMILY_ACQUISITION_AUTHORITY_2026-08-02.md`;
- `data/gill-closed-book-families-2026-08-02.json`.

The former undifferentiated backlog is replaced by seven bounded families: Park, Strother, Ascol, Walden, biographical primary witnesses, first editions and the canonical physical package. Each family has owner documents, claim scope, request queries and acceptance criteria.

Current honest receipt state:

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

The remaining true-dead queue is still an active item-by-item research lane. The eight confirmed decisions do not silently claim closure of all 45 historical rows.

## 9. Meaning of external dependency

An external dependency is not an unowned or undefined question. It has:

- a named owner stage;
- request/acceptance schema;
- receipt requirements;
- a prohibited false-completion boundary;
- a valid next action.

Examples are institutional scan delivery and closed-book full-text delivery. CI cannot fabricate those bytes. Therefore the correct completion is to close the internal preparation/validation stage and keep external delivery explicitly open.

## 10. Global forbidden claims

Do not claim:

- that every Baptist or Gill file has been acquired;
- that OCR is complete without a receipt and page review;
- that Pihahiroth has one proven coordinate;
- that three Heart dossiers mean the complete book is assembled or published;
- that a repaired URL clears image rights;
- that a Research commit alone proves Product deployment;
- that a CI receipt proves facts outside the contract it ran.

## 11. Current next-action order

1. **Heart:** assemble reader chapters 75–77 and then run book-level editorial QA.
2. **Atlas Product:** implement three uncertainty corridors with dated source/rights metadata.
3. **Baptist external lane:** send generated requests; append receipts only on actual file delivery.
4. **Gill external lane:** acquire one family at a time and map it to owner claims.
5. **Source Library:** continue remaining true-dead URL queue item by item.
6. **OSK:** normal maintenance; Wave 12 no longer belongs in publication backlog.

## 12. Decision

Authority `RESEARCH-CURRENT-AUTHORITY-2026-08-02` supersedes `00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md` only as root status/navigation. Historical and corpus evidence remains preserved. Every major open item now belongs to a defined next lane; no hidden undifferentiated backlog remains in the root authority.
