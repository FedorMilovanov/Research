# Agent 06 — Research → public projection authority

**Дата:** 2026-08-01  
**Authority ID:** `A06-RESEARCH-PUBLIC-PROJECTION-2026-08-01`  
**Статус:** `CURRENT / FAIL-CLOSED / NO AUTOMATIC PROMOTION`  
**Research snapshot:** `48fc47f7df447d87312a72be25e6b71718afde86`  
**Product snapshot:** `efaf2a51b1fcc7b7d3f8c9558ecb5acf849df3b3`  
**AuditRepo snapshot:** `7b81f6a7e0cc246f9c8e65cd07766b371bdf9a6a`  
**Production claim:** `no`

## Назначение

Этот файл — единственная текущая authority для маршрута:

```text
Research corpus → publication disposition → public route/page type → physical rights boundary
```

Он не заменяет corpus authorities. Он связывает их с публикационным решением и запрещает вывод «есть в Research/Drive → можно публиковать».

Machine owners:

- `data/public-projection-queue-2026-08-01.json`;
- `data/physical-rights-ledger-2026-08-01.json`;
- CSV-проекции рядом с ними;
- `scripts/validate_public_projection_queue.py`;
- `.github/workflows/public-projection-queue.yml`.

## Dashboard

| Метрика | Значение |
|---|---:|
| Corpus records | **10** |
| `PROMOTE` | **0** |
| `REFERENCE` | **3** |
| `SUPERSEDED` | **0** |
| `BLOCKED` | **7** |
| Уже имеют public route | **7** |
| Связаны с physical-rights ledger | **7** |

**Решение текущего снимка:** ни один corpus record не получает автоматический `PROMOTE`. Product остаётся read-only для Agent 06, пока отдельная запись не выполнит все evidence, locator, archive, rights и publication gates.

## Current projection queue

| Record | Decision | Research status | Target | Holds |
|---|---|---|---|---|
| `heart-series-source-closure` | **REFERENCE** | EVIDENCE_CLOSED_85_SOURCES_18_CLAIMS | `/articles/chto-bibliya-nazyvaet-serdcem/`<br>`/articles/kak-hranit-serdce/`<br>`/articles/kak-menyaetsya-serdce/`<br>+18 routes | `PUBLICATION_HOLD` |
| `osk-power-dark-side-standalone` | **BLOCKED** | WAVES_1_TO_4_CLOSED_WAVE5_AND_SITE_TRANSFER_ACTIVE | `/articles/20-antisovetov-pastoru/` | `EVIDENCE_HOLD`, `PUBLICATION_HOLD` |
| `bratsky-listok-1906-1910` | **BLOCKED** | RESEARCH_PACKAGE_READY_SITE_PUBLICATION_FALSE | `/baptisty-rossii/`<br>`/baptisty-rossii/podpolnaya-pechat/` | `ARCHIVE_HOLD`, `LOCATOR_HOLD`, `RIGHTS_HOLD`, `PUBLICATION_HOLD` |
| `baptist-archive-v156` | **BLOCKED** | ACTIVE_MICROBATCH_V156 | `/baptisty-rossii/`<br>`/baptisty-rossii/dva-sezda-1884/`<br>`/baptisty-rossii/goneniya-i-sovest/`<br>+8 routes | `ARCHIVE_HOLD`, `LOCATOR_HOLD`, `RIGHTS_HOLD`, `PUBLICATION_HOLD` |
| `genesis6-enoch-hard-texts` | **REFERENCE** | NAMED_RESEARCH_BLOCKERS_CLOSED_PUBLICATION_HOLD | `/hard-texts/angely-pod-mrakom-iuda-6-7-2-petra-2/` | `PUBLICATION_HOLD` |
| `gill-archive-families` | **BLOCKED** | ACTIVE_ARCHIVE_FAMILIES_AFTER_PUBLIC_SUITE | `/articles/dzhon-gill-chast-1-chelovek/`<br>`/articles/dzhon-gill-chast-2-uchenyi/`<br>`/articles/dzhon-gill-chast-3-nasledie/`<br>+3 routes | `ARCHIVE_HOLD`, `LOCATOR_HOLD`, `RIGHTS_HOLD`, `PUBLICATION_HOLD` |
| `biblical-atlas-primary-strengthening` | **BLOCKED** | ACTIVE_PIHAHIROTH_SEA_CROSSING_AND_PRIMARY_SOURCE_STRENGTHENING | `/karty/`<br>`/karty/avraam/`<br>`/karty/ishod/` | `EVIDENCE_HOLD`, `LOCATOR_HOLD`, `RIGHTS_HOLD`, `PUBLICATION_HOLD` |
| `source-library-ephemera-63` | **BLOCKED** | PRIVATE_ARCHIVE_ACQUIRED_63_OF_63 | `NO_ASSIGNED_PRODUCT_ROUTE` | `RIGHTS_HOLD`, `PUBLICATION_HOLD` |
| `source-library-editorial-40-pdf` | **REFERENCE** | SEPARATE_RESEARCH_CORPUS | `RESEARCH_REFERENCE_NO_DIRECT_PUBLIC_ROUTE` | `RIGHTS_HOLD` |
| `source-library-poet-portraits-45` | **BLOCKED** | REVIEW_ALLOWLIST_READY_ORIGINALS_ARCHIVED | `NO_ROUTE_IN_GB_PRODUCT` | `RIGHTS_HOLD`, `PUBLICATION_HOLD` |

Полные маршруты, claim IDs, source authorities, fidelity status, media-lane requirements, next action и forbidden promotion хранятся в JSON/CSV owner.

## Physical files and rights

| Ledger ID | Physical state | Rights state | Verified Drive evidence | Publication eligible |
|---|---|---|---|---:|
| `DRV-EPHEMERA-63` | VERIFIED_COMPLETE_PACKAGE | ITEM_LEVEL_REVIEW_REQUIRED | `02 — APPROVED EPHEMERA 63`, `01 — ORIGINALS 01-16.zip` +4 | нет |
| `DRV-EDITORIAL-40` | VERIFIED_FILES_AND_CHECKSUMS_PARTIAL_VIEW | REFERENCE_ONLY_ITEM_REVIEW_REQUIRED | `00_SHA256SUMS.txt`, `01__My Life - Isadora Duncan.pdf` +1 | нет |
| `DRV-POET-PORTRAITS-45` | VERIFIED_APPROVED_FOLDER | IDENTITY_AND_ITEM_RIGHTS_REVIEW_REQUIRED | `01 — PEOPLE & PORTRAITS`, `02 — MEDIA — PORTRAITS & EPHEMERA` +1 | нет |
| `DRV-BRATSKY-REGISTER` | VERIFIED_REGISTER_NOT_COMPLETE_RUN | SCAN_PAGE_AND_REUSE_REVIEW_REQUIRED | `БРАТСКИЙ ЛИСТОК 1906–1910 — АУДИТ И РЕЕСТР — 2026-07-31`, `РУССКИЕ БАПТИСТЫ — MASTER ARCHIVE CATALOG` | нет |
| `DRV-BAPTIST-ARCHIVE` | VERIFIED_REGISTERS_AND_FINDING_AIDS | ARCHIVE_CONTENT_AND_REUSE_NOT_OBTAINED | `РУССКИЕ БАПТИСТЫ — CONSOLIDATED SOURCE REGISTER — 2026-07-31`, `SBHLA AR 915 — Albert Wardin Russian Baptists Collection — finding aid.pdf` +1 | нет |
| `DRV-GILL-ARCHIVE` | NOT_VERIFIED | UNKNOWN | не найден canonical package | нет |
| `DRV-BIBLICAL-ATLAS` | NOT_VERIFIED_CANONICAL_PACKAGE | UNKNOWN | не найден canonical package | нет |

### Что доказано Drive-проверкой

- private package `APPROVED EPHEMERA 63` физически существует и содержит четыре original ZIP parts плюс review package;
- отдельный editorial PDF corpus имеет checksum control и физические PDF objects;
- approved core poet portrait folders физически существуют;
- Bratsky Listok audit/register и Russian Baptists master registers существуют;
- Baptist consolidated source register и два archive finding aids существуют.

### Что Drive-проверка не доказывает

- item-level production licence;
- право воспроизводить scan/page/image;
- identity портретируемого лица;
- полноту Bratsky Listok run;
- наличие запрошенного archive folder content;
- canonical Gill или Biblical Atlas physical package.

## Corpus decisions

### `REFERENCE`

`REFERENCE` означает: authority можно использовать для навигации, проверки и ограничения формулировок, но она не является разрешением на автоматическую публикацию.

Текущие reference-only records:

- Heart source closure — existing public series требует claim-level reverify после 85-source closure;
- Genesis 6 / Enoch — named Research blockers закрыты, publication hold остаётся;
- second editorial 40-PDF corpus — research/reference archive без прямого route.

### `BLOCKED`

`BLOCKED` всегда содержит хотя бы один типизированный hold:

- `EVIDENCE_HOLD`;
- `LOCATOR_HOLD`;
- `ARCHIVE_HOLD`;
- `RIGHTS_HOLD`;
- `PUBLICATION_HOLD`.

Ни общий статус `READY/CLOSED`, ни archive holding, ни Drive presence не снимают эти блокеры.

## Cross-repo boundary

### Research

Владеет corpus authority, source/claim boundary, projection decision, physical-rights status, next action и forbidden promotion.

### Product

Не копирует этот registry и не меняется в Agent 06 при `PROMOTE = 0`. Будущий product PR обязан ссылаться на один конкретный `PROMOTE` record и сохранять его target claim/section/route boundary.

### AuditRepo

Получает отдельный evidence-only PR после merge Research authority. Он может зафиксировать exact Research merge SHA и отсутствие product delta, но не менять canonical counters без verifier-owned основания.

## Definition of done

- одна queue authority и один rights ledger;
- JSON + CSV projections;
- физические Drive objects проверены по metadata;
- каждый record имеет disposition, Research status, target, page type, claim boundary, public/fidelity state, rights/media boundary и next action;
- `PROMOTE` fail-closed;
- validator read-only;
- exact-head CI;
- review threads = 0;
- guarded merge;
- merged-main verification и branch cleanup;
- отдельный AuditRepo evidence PR;
- production deployment не заявляется.

## Следующий разрешённый шаг

После merge этой authority:

1. создать AuditRepo evidence-only record;
2. не создавать product PR, пока `PROMOTE = 0`;
3. при появлении первого `PROMOTE` — отдельная owner branch на один bounded corpus/route/claim set, без копирования Agent 06 registry.
