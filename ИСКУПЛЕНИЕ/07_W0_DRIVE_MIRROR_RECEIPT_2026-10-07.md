# W0 — Drive mirror receipt (снапшот 2026-10-07)

**Дата загрузки:** 2026-10-07 (времена — Drive `created_time`)
**Корневая структура:** `07 — СЕРИЯ «ИСКУПЛЕНИЕ»` → `1VULVPNq4DbBFS5KvBDpSkJOlx4jbEQAV`
**Что это:** побайтное зеркало research-документов корпуса в Drive (для чтения вне IDE, для переноса между устройствами, для фиксации того, какая редакция была действующей 2026-10-07).
**Чем это НЕ является:** это **не** приёмка книг и **не** источник. Ни одна библиотечная позиция из `03_...` здесь не получена; `verifiedFileReceipts = 1` относится только к проверенному тексту Второго главы Дорта в `10_...`.

---

## 0a. Что лежит в `07`-дереве: прежнее чтение и его отзыв

В исходной редакции этого раздела десять документов, найденных при обходе `07`-дерева
(`00_README`, `01_INTRODUCTION`, `02_TERMS`, `03_ACQUISITION`, `04_RIGHTS`, `05_MASTER_MAP`,
`06_PRODUCT`, `07_AUTHORITY`, `08_MURRAY_SOURCE_CARD`, `09_MURRAY_ARGUMENT_MAP`), были помечены
как `SUPERSEDED-BY-MIRROR` на том основании, что они относятся к «более ранней части той же
сессии». **Это утверждение неверно и отзывается.** Эти документы не были вытеснены моими
зеркалами: они относятся к канонической линии темы, которая к тому моменту уже развивалась
в `main`-составляющей репозитория, и она же 2026-10-08 22:58–22:59Z разметила мои зеркала
как устаревшие. Направление замещения — обратное тому, что я записал.

## 0b. Фактическое состояние зеркал (проверено 2026-10-15 запросом к Drive)

| Объект (нынешнее имя) | file id | байты | где сейчас |
|---|---|---|---|
| `00 MASTER RESEARCH MAP AND CHARTER 2026-10-07 — HOLD` | `1ozlnTTepSyhFAj_hEsxNAwvF3Dc_R5tw` | 26 608 | `99 — HOLD — SUPERSEDED MIRRORS` |
| `01 W0 INTRODUCTION AND TERMINOLOGY 2026-10-07 — HOLD` | `10go1WoYIIFBjYXoiadPVbzWDHP88w_PD` | 44 734 | там же |
| `03 W0 SOURCE REGISTRY 2026-10-07 — HOLD` | `1is-gox1UYi-4Ie0GBvHoMbzxh2mj2oL-` | 39 479 | там же |
| `04 W0 COMPETING MODELS TAXONOMY 2026-10-07 — HOLD` | `1eZKED3ikOOt7z96nEyspV6RxvKxTfgAd` | 17 998 | там же |
| `05 W0 ACQUISITION FAMILIES AND DRIVE INTAKE 2026-10-07 — HOLD` | `1aigyR95l0DI8jMfxCTAKhvvm1RGffbVF` | 15 414 | там же |
| `06 PUBLICATION ARCHITECTURE FOR GOSPOD-BOG 2026-10-07 — HOLD` | `1_eb42tHpIRJkeZqLQ_HHuwpapX7hWiMF` | 17 905 | там же |
| `07 W0 DRIVE MIRROR RECEIPT 2026-10-07 — HOLD` | `1r4UNqlNv4xgBYf_vCI-R-hjyihyal-jr` | 7 729 | там же |
| `redemption-corpus-authority-2026-10-07.json — HOLD` | `1VVOS5a_Oq5wfNmbhQBGLbm6wfh-CFPAs` | 13 683 | там же |
| `README.md — HOLD` | `1tTA18HWLlF_GseQCC4hCymbWWn6fj349` | 9 451 | там же |
| `00 — AUTHORITY — W0-era name — HOLD` (×3, a/c/e) | `1AG1egmE…`, `1NQ12OhD…`, `1EqpEu8L…` | 11 330 / 11 785 / 12 623 | там же |

Ни один из перенесённых объектов не был изменён по содержимому: перенос не создаёт новой
редакции и **не является** приёмкой — `receptionState` для всех строк §1 остаётся
`OBJECT-PRESENT-UNHASHED`, а для четырёх библиотечных копий §2 — `RECEIVED_UNHASHED`
(наличие объекта ≠ receipt; sha256 не считывались, их размер делает это нецелесообразным).

Карантиная папка: `99 — HOLD — SUPERSEDED MIRRORS (не удалять: старые копии, ID живы)` →
`1FK7_q8431ys6MAv_0zFsXfht1Dnl5wmd`, дочерняя к `07 — СЕРИЯ «ИСКУПЛЕНИЕ»`; создана 2026-10-08
08:36Z, мои объекты перенесены в неё 2026-10-08 22:58–22:59Z. File id и размеры сохранены,
то есть перенос не создавал копий и ничего не перезаписывал. В той же папке лежат и
собственные промежуточные ревизии канонического лана (`atonement-corpus-v1.json` по волнам,
`07 RIGHTS LEDGER · волна c…g`) — convention, а не адресованное нам действие.
Практические следствия: (1) в приёмных папках `00`/`01`/`02`/`03`/`06` зеркал корпуса больше нет;
(2) `02` сейчас содержит Murray-дампы и карточки канонической линии (см. §3a);
(3) повторную выгрузку этих файлов в `07`-дерево делать нельзя, пока владелец не решит
реконсилияцию; (4) `STALE`-строки §1–§3 этого файла остаются точным снимком 2026-10-07
и не должны читаться как текущее состояние.

## 1. Загруженные объекты (11 зеркал spine + этот документ = 12 строк)

| Файл в Drive | Папка | parent id | file id | байт | sha256 локального файла | created |
|---|---|---|---|---|---|---|

| `README.md` | `00 — INDEX, AUTHORITY & SERIES MAP` | `1BAdPEiguZbar-Dg5Z3IfWWk0E-vaEnpL` | `1tTA18HWLlF_GseQCC4hCymbWWn6fj349` | 9778 | `a0f1d06c8c96965ab5a734b0f6c5e59d398b6183e4045ee3574f6d712e6f0672` | `2026-10-07T16:27:27Z` |
| `00_CURRENT_AUTHORITY_2026-10-07.md` | `00 — INDEX, AUTHORITY & SERIES MAP` | `1BAdPEiguZbar-Dg5Z3IfWWk0E-vaEnpL` | `1IzZxjBVl3BLrfcQH3r07SeeXbzu8yLOm` | 5581 | `da81d14d2629f7cd0984a212761ebab0970f2ee564980faa5258ff697e3388bf` | `2026-10-07T16:27:27Z` |
| `00_MASTER_RESEARCH_MAP_AND_CHARTER_2026-10-07.md` | `00 — INDEX, AUTHORITY & SERIES MAP` | `1BAdPEiguZbar-Dg5Z3IfWWk0E-vaEnpL` | `1ozlnTTepSyhFAj_hEsxNAwvF3Dc_R5tw` | 26608 | `05590d8661fe0a142e72b7326bfa520bb58464bb6d555b28f9de9a05a840fb2f` | `2026-10-07T16:27:27Z` |
| `01_W0_INTRODUCTION_AND_TERMINOLOGY_2026-10-07.md` | `00 — INDEX, AUTHORITY & SERIES MAP` | `1BAdPEiguZbar-Dg5Z3IfWWk0E-vaEnpL` | `10go1WoYIIFBjYXoiadPVbzWDHP88w_PD` | 44734 | `f46d984ea316a6bf313f3b9ebb0225341c36ce4fd2543e2839ec0eff1d2c0310` | `2026-10-07T16:27:27Z` |
| `06_PUBLICATION_ARCHITECTURE_FOR_GOSPOD_BOG_2026-10-07.md` | `00 — INDEX, AUTHORITY & SERIES MAP` | `1BAdPEiguZbar-Dg5Z3IfWWk0E-vaEnpL` | `1_eb42tHpIRJkeZqLQ_HHuwpapX7hWiMF` | 17905 | `265fb2c2c1c90959baa9b6dfe29ebd087b7f955424ff7af3a30811123acf19b3` | `2026-10-07T16:27:27Z` |
| `10_W0_PRIMARY_TEXT_DORT_HEAD_II_AND_CALVIN_2026-10-07.md` | `01 — PUBLIC DOMAIN LIBRARY` | `1BuYqlnPM1pIw-pCIFZLOKgGLL3hR1F4t` | `1hPs1aEWtwv1GHGHtZVtpWd8c91bQgAgo` | 16227 | `c39b06b66ea73c7ad231b998e88b6dc8b1cb1c017cf270acee0cdc6fa796efb5` | `2026-10-07T16:27:27Z` |
| `03_W0_SOURCE_REGISTRY_2026-10-07.md` | `02 — COPYRIGHT BIBLIOGRAPHY & ACQUISITION` | `1FdQlbxhVzhAdCPoS1lt2qEZMRPsaQNPI` | `1is-gox1UYi-4Ie0GBvHoMbzxh2mj2oL-` | 40603 | `0e41df791f3ae18da17c9b83fd1798902aa6193cc6960db2b11bf3a117da9d6c` | `2026-10-07T16:27:27Z` |
| `02_W0_SCRIPTURE_CORPUS_FOR_WHOM_2026-10-07.md` | `03 — SCRIPTURE, LEXICA & COMMENTARIES` | `17BZ9SUu5zp5VVFd5a0t8mFX8wEodHcIv` | `1dAMRTc7Tcy02oGt6HWX2RGYgB-IFx0Ap` | 32754 | `24c58d7131664b9b48dfbaaa78bd189284cc6cd413ab46082e55898648beaab8` | `2026-10-07T16:27:27Z` |
| `04_W0_COMPETING_MODELS_TAXONOMY_2026-10-07.md` | `04 — CONFESSIONS & HISTORICAL THEOLOGY` | `1ZTD2idu9oFO9Et1MSgfgtKMZZg63yUTw` | `1eZKED3ikOOt7z96nEyspV6RxvKxTfgAd` | 17998 | `0b2b58b44ed67ac8720b5dfb3b9a071ad4ea117ff207893612ec32b0ab0be8a7` | `2026-10-07T16:27:27Z` |
| `05_W0_ACQUISITION_FAMILIES_AND_DRIVE_INTAKE_2026-10-07.md` | `06 — RIGHTS, HOLD & PROVENANCE` | `1edsBGRg0oQw_G-75QYdaNvde7KKiCFQy` | `1aigyR95l0DI8jMfxCTAKhvvm1RGffbVF` | 15414 | `6e238df3d637904306db552e6a42c07b357f7081619fe205615a77999e4c6f99` | `2026-10-07T16:27:27Z` |
| `redemption-corpus-authority-2026-10-07.json` | `05 — SOURCE LEDGERS & CLAIM MAPS` | `13cx8Y86uaDRIullYpc8tneFxGbjPUlIJ` | `1VVOS5a_Oq5wfNmbhQBGLbm6wfh-CFPAs` | 16788 | `7915b9c7a031945f145d94a0b2b26fbae4835fdbfa6428413e24fba2fd60f24f` | `2026-10-07T16:27:27Z` |
| `07_W0_DRIVE_MIRROR_RECEIPT_2026-10-07.md` | `06 — RIGHTS, HOLD & PROVENANCE` | `1edsBGRg0oQw_G-75QYdaNvde7KKiCFQy` | `1r4UNqlNv4xgBYf_vCI-R-hjyihyal-jr` | 13575 | `dfd3786f96028aea488f45da68312df9c2d09c45747331185c94d34564121abb` | `2026-10-07T16:27:27Z` |

Размеры и хеши в таблице описывают **локальные canonical-файлы** на момент `2026-10-07T16:27:27Z`. Три объекта в Drive несут ревизию 16:22Z и потому отстают на одну локальную правку (`MIRROR-LAG`, canonical — репозиторий, по §3.1): `README.md`, `03_W0_SOURCE_REGISTRY_2026-10-07.md`, `redemption-corpus-authority-2026-10-07.json`. Расхождение состоит из §7a (реестр), §1a (README) и учёта предсуществующих объектов (JSON) — содержательных правок в Drive не теряется, зеркало синхронизируется на следующем шаге волны. Остальных расхождений нет, `STALE`-объектов нет.
MIME: `text/markdown` для `.md`, `application/json` для machine-registry. Конвертация в формат Google Docs не выполнялась — зеркало остаётся текстовым файлом, чтобы хеш совпадал.

## 2. Что в этих папках появится потом

| Папка | Разрешено | Запрещено |
|---|---|---|
| `01 — PUBLIC DOMAIN LIBRARY` | PD-тексты, у которых проверены **и** оригинал, **и** перевод/аппарат (Кальвин, Оуэн, Goodwin, Davenant, латынь Дорта, конфессиональные тексты, Толковая Библия) | переводы XX–XXI вв., репринты с заявлением прав издателя, «PD, потому что старое» без проверки |
| `02 — COPYRIGHT BIBLIOGRAPHY & ACQUISITION` | карточки изданий, выходные данные, легальные каналы доступа, статус очереди | полные тексты Мюррея, Gibson-сборника, Stott, Morris, Pinnock, Amyx, Bavinck и т. д. |
| `03 — SCRIPTURE, LEXICA & COMMENTARIES` | инвентари, лексические карточки по страницам словарей, собственные разбор-файлы |скан-копии и выгрузки из платных баз без прав |
| `04 — CONFESSIONS & HISTORICAL THEOLOGY` | акты и тексты с явным изданием | пересказы вместо текста |
| `05 — SOURCE LEDGERS & CLAIM MAPS` | зеркала machine-JSON, claim-карты | «улучшенные» версии задним числом |
| `06 — RIGHTS, HOLD & PROVENANCE` | манифесты, SHA256SUMS, provenance-заметки, HOLD-реестр | — |

## 3. Правила обращения с этим зеркалом

1. Drive — **проекция**, canonical — репозиторий. Правка в Drive не становится правкой корпуса: сначала файл меняется в `ИСКУПЛЕНИЕ/`, gate проходит зелёным, затем зеркало перезагружается и эта таблица получает новую строку.
2. Объект в Drive без записи в таблице = посторонний input; он попадает в разбор, а не в цитирование.
3. Любая цитата обязана ссылаться на издание и страницу, а не на `file id`.
4. При расхождении байтов локального файла и зеркала — действует локальный файл, зеркало помечается `STALE`.
5. Эта таблица не даёт прав на публикацию: `publicationEligible = false` для всех строк.

## 4. Итог волны по Drive

```text
STRUCTURE              = user-owned 07-дерево, 7 подпапок, соответствие слоям реестра зафиксировано
CORPUS MIRRORS PLACED  = 11 (+1: этот документ загружен в 06-папку после составления таблицы,
                           итог в дереве = 12 объектов; file id 1r4UNqlNv4xgBYf_vCI-R-hjyihyal-jr)
BOOKS RECEIVED         = 4 PD-COPIES PRESENT, 0 hash-verified RECEIVED receipts
COPYRIGHTED FULL TEXT PLACED = 0
QUOTE-READY SOURCES    = 1 (Dort Head II Arts I–IX)
NEXT ACTION            = RED-FAM-DORT-ACTS (Errors/Rejections), RED-FAM-REMONSTRANCE, RED-FAM-LEX
```
