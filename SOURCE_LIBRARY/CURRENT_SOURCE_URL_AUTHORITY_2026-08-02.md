# Source Library — current URL repair authority

**Дата:** 2026-08-02  
**Authority ID:** `SOURCE-URL-REPLACEMENTS-2026-08-02`  
**Статус:** `CURRENT / CONFIRMED TRANSPORT REPAIRS / RIGHTS UNCHANGED`  
**Machine registry:** `data/source-url-replacements-2026-08-02.json`

## 1. Назначение

Этот файл supersedes семь подтверждённых мёртвых/перемещённых URL и добавляет один version-history endpoint. Исторические audit reports сохраняют старые адреса как evidence того, что проверялось; активные consumers должны применять replacement registry.

## 2. Подтверждённые решения

| ID | Старый transport | Текущий transport | Evidence/rights effect |
|---|---|---|---|
| URLR-001 | CCEL `bcftoc.htm` | `bcf.htm` | только исправление навигации |
| URLR-002 | FEB Esenin `about.htm` | `rub.html` | только исправление точки входа |
| URLR-003 | FEB Esenin `sitemap.asp` | `sitemap.htm` | только исправление карты корпуса |
| URLR-004 | Duncan `all-items/` | `collection/all` | item-level rights hold сохраняется |
| URLR-005 | Duncan `historical/` | `collection/` | item-level rights hold сохраняется |
| URLR-006 | Duncan `works/` | `reference/isadora` | bibliography access, не image permission |
| URLR-007 | Qumran generic transcription index | pinned 4Q204 version `2025-11-11` | CC BY-SA transcription, не рукописная фотография |
| URLR-008 | — | 4Q204 changelog | version-history companion |

## 3. Правило композиции

```text
HISTORICAL AUDIT URL
+ CURRENT REPLACEMENT REGISTRY
= CURRENT TRANSPORT DECISION
```

Старый URL не удаляется молча из исторического closeout. Новый URL не используется для переписывания факта прошлой проверки.

## 4. Что URL repair не делает

Исправление адреса не означает:

- что источник стал более сильным;
- что полный текст или файл скачан;
- что цитата сверена по странице;
- что изображение public domain;
- что institution разрешает переиздание;
- что современный viewer endpoint является стабильным item manifest;
- что права на transcription распространяются на manuscript photo.

## 5. Duncan boundary

Duncan Archive остаётся `ITEM_LEVEL_RIGHTS_REVIEW_REQUIRED`. Перед использованием конкретного изображения нужны:

1. item URL;
2. creator/date/provenance;
3. rights holder и restriction text;
4. разрешённый use;
5. credit line;
6. Product owner.

Collection index — средство поиска, не blanket licence.

## 6. 4Q204 boundary

Для текстологического использования хранить вместе:

- pinned transcription version;
- changelog;
- дату доступа;
- лицензию transcription page;
- явную помету `НЕ ФАКСИМИЛЕ` для производной схемы.

IAA/Leon Levy photographs остаются link-only/permission-dependent.

## 7. Scope closure

```text
CONFIRMED URL REPAIRS = CLOSED
VERSION PIN = CLOSED
RIGHTS SEPARATION = CLOSED
HISTORICAL URL PRESERVATION = CLOSED
REMAINING TRUE-DEAD QUEUE = ACTIVE ITEM-BY-ITEM RESEARCH
```

Этот authority закрывает только подтверждённые восемь решений, а не объявляет всю историческую очередь из 45 строк автоматически исправленной.
