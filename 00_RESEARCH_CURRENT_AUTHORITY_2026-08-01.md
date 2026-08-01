# Research — единая текущая evidence authority

**Дата:** 2026-08-01  
**Статус:** `ACTIVE ROOT AUTHORITY / WAVE-BASED CLOSURE`  
**Current base:** `48fc47f7df447d87312a72be25e6b71718afde86`

## Назначение

Этот файл вводит общий словарь для всего `Research`. Исторические документы,
старые `HOLD`, версии, pass-отчёты и closeout-файлы не удаляются, но не могут
самостоятельно менять текущий статус без ссылки из актуальной authority соответствующего корпуса.

## Пять независимых видов незакрытости

1. `EVIDENCE_HOLD` — тезис не доказан достаточным источником.
2. `LOCATOR_HOLD` — источник существует, но нет точной страницы, абзаца, scan leaf
   или стабильного item URL.
3. `ARCHIVE_HOLD` — известна карточка/фонд/holding, но сам документ не получен.
4. `RIGHTS_HOLD` — содержание или файл есть, но происхождение/лицензия/право
   публичного использования не доказано.
5. `PUBLICATION_HOLD` — Research закрыт, но читательский текст, provenance,
   редакционная проверка или technical release ещё не завершены.

Слово `HOLD` без одного из этих префиксов считается недостаточно точным в новых
authority-файлах.

## Source classes

- `A1` — суд, закон, официальный государственный record, первичный архивный документ.
- `A2` — полный независимый investigation/review/report с известной методологией.
- `A3` — собственное официальное заявление, board record, письмо, протокол,
  институциональный документ.
- `B1` — сильная профессиональная вторичная публикация, используемая для поиска,
  сопоставления или описания позиции, но не как единственная опора спорного тезиса.
- `C` — блог, пересказ, advocacy или неподтверждённая публикация.
- `D` — цитата/факт без проверяемого locator.

## Quote policy

Прямая цитата разрешена только когда одновременно выполнены условия:

- источник `A1/A2/A3`;
- доступен точный URL или локальный первичный файл;
- указан page/paragraph/section locator, когда документ длинный;
- контекст проверен;
- quote не расширяет вывод документа.

Parsed text, OCR и repository paraphrase сами по себе не дают `quote_safe`.

## Current corpus authorities

- `СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-01.md`;
- `ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/39_WAVE5_ADELAJA_FINAL_BOUNDARY_2026-08-01.md`;
- `ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/38_WAVE4_STANDALONE_PASTORAL_CARE_LEGAL_2026-08-01.md`;
- `ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/37_WAVE3_DARK_SIDE_REPENTANCE_RESTORATION_2026-08-01.md`;
- `ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/36_WAVE2_CONDITIONAL_MONEY_POWER_CLOSURE_2026-08-01.md`;
- `ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/35_CURRENT_AUTHORITY_POWER_CASE_ROUTING_2026-08-01.md`;
- `data/genesis6-authority-manifest.json`;
- `data/genesis6-enoch-extension-authority-manifest.json`;
- Gill navigation/volumes 70–74 and their validators;
- `RUSSIAN_BAPTISTS_ARCHIVE` / grouped Baptist proof ledgers;
- `SOURCE_LIBRARY/TOTAL_SOURCE_AUDIT_CLOSEOUT_2026-07-30.md`;
- Biblical Atlas dossiers and `БИБЛЕЙСКИЙ АТЛАС/README.md`.

Where two historical files conflict, the newest explicitly named current authority
or machine ledger governs.

## Repository closure waves

### Completed

- Heart disputed-claim source closure: 85-source registry.
- Genesis/Enoch named Research blockers: closed; publication hold remains.
- OSK Wave 1: 33-case routing and 79-source register.
- OSK Wave 2: eight money/power cases and 56-source pass.
- OSK Wave 3: seven dark-side/restoration decisions and 49-source pass.
- OSK Wave 4: three standalone pastoral-care/legal dossiers and 54-source pass.
- OSK Wave 5: Adelaja / King’s Capital final procedural boundary and **52-source pass**.
- Cumulative OSK authority: **290 sources / 216 A-class / 197 exact URLs / 105 quote-safe**.
- Effective routing:
  `21 CORE / 1 CONDITIONAL / 7 DARK_SIDE / 4 STANDALONE / 0 HOLD`.
- All 33 OSK cases now have an explicit current route; no generic case-level HOLD remains.

### Active

- Baptist archive scans/OCR/archive acquisition;
- Source Library dead-link, acquisition and rights queue;
- OSK site-transfer/publication ledger for `gb-is-my-strength`;
- Atlas Pihahiroth/sea-crossing and primary-source strengthening;
- Gill closed-book/archive families.

## Fail-closed rule

A historic heading such as `VERIFIED`, `READY`, `CLOSED` or `Level A/B` is not
sufficient authority unless the governing machine registry or current authority
confirms:

- exact claim;
- exact source;
- permitted wording;
- remaining uncertainty;
- publication boundary.
