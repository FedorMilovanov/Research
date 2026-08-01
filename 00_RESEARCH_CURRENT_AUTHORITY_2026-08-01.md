# Research — единая текущая evidence authority

**Дата:** 2026-08-01  
**Статус:** `ACTIVE ROOT AUTHORITY / WAVE-BASED CLOSURE`  
**Current base:** `729c1b75f9c9dfabaaae52c6be5b7fb868c0db38`

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
- `ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/36_WAVE2_CONDITIONAL_MONEY_POWER_CLOSURE_2026-08-01.md`;
- `ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/35_CURRENT_AUTHORITY_POWER_CASE_ROUTING_2026-08-01.md` — base Wave 1;
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
- OSK Wave 2: eight money/power cases, 56-source pass; effective routing
  `21 CORE / 1 CONDITIONAL / 7 DARK_SIDE / 3 STANDALONE / 1 HOLD`.

### Active

- Baptist archive scans/OCR/archive acquisition;
- Source Library dead-link, acquisition and rights queue;
- OSK Wave 3 dark-side/restoration and later standalone/blocked waves;
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
