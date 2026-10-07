# W0 — Drive mirror receipt (снапшот 2026-10-07)

**Дата загрузки:** 2026-10-07 (времена — Drive `created_time`)
**Корневая структура:** `07 — СЕРИЯ «ИСКУПЛЕНИЕ»` → `1VULVPNq4DbBFS5KvBDpSkJOlx4jbEQAV`
**Что это:** побайтное зеркало research-документов корпуса в Drive (для чтения вне IDE, для переноса между устройствами, для фиксации того, какая редакция была действующей 2026-10-07).
**Чем это НЕ является:** это **не** приёмка книг и **не** источник. Ни одна библиотечная позиция из `03_...` здесь не получена; `verifiedFileReceipts = 1` относится только к проверенному тексту Второго главы Дорта в `10_...`.

---

## 0a. Что уже было в 07-дереве до этой приёмки (зафиксировано, а не проигнорировано)

При обходе дерева 2026-10-07 обнаружены объекты, созданные **до** загрузки зеркал. Они остаются на месте; этот раздел — их учёт.

### Книги (принадлежат владельцу Drive; копия, не перемещение)

| Файл | Папка | file id | байт | created | Состояние |
|---|---|---|---|---|---|
| `Owen, John — The Works of John Owen (PD copy).pdf` | `01 — PUBLIC DOMAIN LIBRARY` | `1gfKY8eXGhV-HL5O4u1tVVcCRYNKx-dQY` | 42084171 | 2026-10-07T15:58:33.454Z | `RECEIVED_UNHASHED / EVIDENCE_HOLD / RIGHTS: PD-CLAIM-UNVERIFIED` |
| `Goodwin, Thomas — The Works of Thomas Goodwin (PD copy).pdf` | `01 — PUBLIC DOMAIN LIBRARY` | `1o9T7mIQxIH3ZB2EVc2hQsKdjEQM3SW-M` | 27215853 | 2026-10-07T15:58:36.935Z | `RECEIVED_UNHASHED / EVIDENCE_HOLD / RIGHTS: PD-CLAIM-UNVERIFIED` |
| `Calvin, John — Institutes of the Christian Religion (PD copy).pdf` | `01 — PUBLIC DOMAIN LIBRARY` | `1DLcwFWyRXtTDBzdS_tHptGkoItoumVWZ` | 45351929 | 2026-10-07T15:58:35.362Z | `RECEIVED_UNHASHED / EVIDENCE_HOLD / RIGHTS: PD-CLAIM-UNVERIFIED` |
| `Westminster Confession of Faith (PD copy).pdf` | `04 — CONFESSIONS & HISTORICAL THEOLOGY` | `1VSp4vU56X8uuYrp2SERkp2p0BRk-vQq4` | 16179601 | 2026-10-07T15:58:38.739Z | `RECEIVED_UNHASHED / EVIDENCE_HOLD / RIGHTS: PD-CLAIM-UNVERIFIED` |

Владелец всех четырёх — аккаунт `oldpoet2025@gmail.com` (не агент). Их наличие в Drive **не является приёмкой**: по §3 политики `RECEIVED` требует sha256, а хеш этих объектов ещё не вычислен (объекты 16–45 МБ; хеширование выполняется на шаге, когда файл реально читается под конкретный claim, а не «на всякий случай»).

Что эти четыре объекта уже меняют: `RED-SRC-0303` (Institutes III.21–24), `RED-SRC-0304…0306` (Works Оуэна, в т. ч. том 10 с *Death of Death*), `RED-SRC-0308` (Goodwin), `RED-SRC-0005` (WCF VIII/XI) переходят с `ACCESS: NONE` на `ACCESS: OBJECT-PRESENT-UNREAD`. Это не право цитировать; это снятие барьера «добыть».

**Дефект исходного имени, требующий правки на стороне владельца:** у файла Оуэна `originalFilename` = `Owen, John — The Works of John Murray wait no — The Works of John Owen (PD copy).pdf` — черновое самоназвание попало в метаданные. Само имя в Drive корректно; править нужно исходное имя, и это решение владельца, а не агента.

### Сводки, созданные ранее в этой же волне (Google Docs)

| Документ | Папка | file id |
|---|---|---|
| `00 README AND NAVIGATION — Искупление (2026-10-07)` | 00 | `1qXjocuWb3xm747BLhtmDBNY4Pd_EhbgZbAlFVgZDqSk` |
| `00 CURRENT AUTHORITY — Искупление 2026-10-07` | 00 | `1bI3GKw5tpAV3uDHUxGwz42WmAa2i2giGkpT49USkMVM` |
| `01 MASTER RESEARCH MAP AND SERIES ARCHITECTURE` | 00 | `1_0I6d9OiRapJWQ9RzsgIAu73dxeArTJSI7ViRBMPlNw` |
| `02 TERMS, DEFINITIONS AND WHAT IS ATONEMENT` | 00 | `14EwvFHHCY3OlaMJ_tKQH7mGbr3Z3Fc5CqBNGrQNZO7A` |
| `06 PUBLICATION ARCHITECTURE FOR GOSPOD-BOG — do not implement yet` | 00 | `1mxYsP0RPDM8yNq_XCEJQXpDit96QP2z2KKww7psPcKs` |
| `08 Murray RAA source card — RIGHTS HOLD — no full text` | 02 | `1k2iVUPhMXwtV9hrAaZwlOM0YPW-V4JPCf8q4eR43zsA` |
| `03 BIBLICAL CORPUS AND REDEMPTION VOCABULARY` | 03 | `1xMwEx6UA2W4N8sE3b9DKRifRnko8T4-RNZfO0_IB-Cs` |
| `04 LIMITED VS UNIVERSAL QUESTION MAP — no verdict` | 05 | `1GFVUswVklNLz5VCtZRclMFj9b06nA4WUj1pjbIrtNaA` |
| `05 SOURCE REGISTRY AND ACQUISITION QUEUE` | 05 | `1yRVrEg-BglE8442TvZ5iIvr3WGGmEe5TOXADRtlmE4c` |
| `07 DRIVE LIBRARY AND RIGHTS LEDGER` | 06 | `1a1OFbfqzHEQfGS-WBPBRRfJR-a8hu6IMfRJwx9C5-UY` |

Решение по ним: они **не удаляются** и **не правятся задним числом**. Их статус — `SUPERSEDED-BY-MIRROR (чтение разрешено, цитирование запрещено, canonical — markdown в репозитории)`: реестр источников теперь ведёт `03_W0_SOURCE_REGISTRY_2026-10-07.md`, терминологию — `01_W0_INTRODUCTION_AND_TERMINOLOGY_2026-10-07.md`, карту вопроса — `04_W0_COMPETING_MODELS_TAXONOMY_2026-10-07.md`. Если владелец предпочитает видеть в Drive единый слой, эти десять объектов можно убрать вручную — но удаление не нужно для корректности корпуса, поэтому решение оставлено владельцу.

Отдельно: каталог `01 — ИСКУПЛЕНИЕ …`, упоминавшийся в черновике волны, при обращении 2026-10-07 не разрешился (Drive ответил `File not found`), то есть второй структуры сейчас нет и третья не создаётся: приём корпуса идёт только в `07`-дерево.

---

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
