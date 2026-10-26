# Том 75. Closed-book family acquisition authority

**Дата:** 2026-08-02  
**Последняя проверка:** 2026-08-04  
**Authority ID:** `GILL-CLOSED-BOOK-FAMILIES-2026-08-02`  
**Статус:** `FAMILY OWNERSHIP CLOSED / ONE DURABLE FILE RECEIPT / REMAINING ACQUISITION OPEN`  
**Machine registry:** `data/gill-closed-book-families-2026-08-02.json`  
**Прямые цитаты:** `0 approved`

## 1. Что исправляет этот том

Ранний backlog говорил о «закрытых книгах» как об одной неопределённой корзине. Теперь каждая family имеет:

- отдельный ID;
- owner documents;
- ограниченный claim scope;
- точные поисковые формулы;
- критерий достаточного файла;
- запрет повышать preview, abstract, bibliography или Drive-name до full-text evidence.

## 2. Семьи

| ID | Scope | Current state |
|---|---|---|
| `GILL-FAM-PARK` | decline thesis, hyper-Calvinism terminology, reception | external acquisition required |
| `GILL-FAM-STROTHER` | biography and doctoral scholarship | external acquisition required |
| `GILL-FAM-ASCOL` | gospel offer, duty faith, external call | external acquisition required |
| `GILL-FAM-WALDEN` | Gillites and later reception | external acquisition required |
| `GILL-FAM-BIOGRAPHICAL-PRIMARY` | Rippon, Crosby, White and biographical witnesses | one durable Rippon receipt; edition verified; claim follow-up required |
| `GILL-FAM-FIRST-EDITIONS` | dates, title pages, edition conflicts | partial open-access acquisition required |
| `GILL-FAM-CANONICAL-PHYSICAL-PACKAGE` | archive custody and registry mapping | package identity unresolved |

## 3. Receipt ladder

```text
CATALOG / ABSTRACT / PREVIEW
→ navigation only

FULL FILE RECEIVED
→ requires bytes + SHA-256 + durable receipt

EDITION VERIFIED
→ requires title page + pagination + edition identity + locator map

CLAIM USABLE
→ requires exact owner scope and locator

QUOTE READY
→ requires page-image readback + context + quote card + rights basis
```

Ни один уровень не выводится из имени файла или поискового результата.

## 4. Current receipt transaction

Для `GILL-FAM-BIOGRAPHICAL-PRIMARY` установлен один точный receipt:

- item: `GILL-BIO-RIPPON-1838-IA`;
- file: `briefmemoiroflif00ripp.pdf`;
- bytes: `9297102`;
- SHA-256: `362019ee851280e14eb4c6cd8bca70a30df957af225ac56c7c6d95bbaf461792`;
- durable provider: Google Drive;
- durable file ID: `1q4IFETrDu9bH8mGMIPQO38qQTVwxjxMu`;
- metadata readback confirmed the same `application/pdf` and byte size;
- title page, publisher advertisement and edition locator map were visually reviewed.

Это file-level receipt для одного open-access item. Он не является canonical physical package receipt и не закрывает другие семьи.

## 5. Search audit boundary

Connected Drive searches по английским и русским названиям остаются discovery pass, пока конкретный объект не проходит byte-level materialization/readback и mapping к family. Текущий Rippon receipt прошёл этот ladder; простые совпадения по имени всё ещё не проходят.

Поэтому допустимо говорить:

> Для Rippon 1838 установлен один durable file receipt; остальные внешние acquisition dependencies остаются открыты.

Недопустимо говорить:

> Наличие похожего имени в Drive означает verified full text.

## 6. Canonical physical package

Package считается установленным только при наличии:

1. устойчивого package name;
2. полного manifest;
3. file names и family IDs;
4. byte sizes;
5. SHA-256 каждого файла и пакета;
6. durable storage receipt;
7. mapping к witness registry/owners;
8. duplicate and placeholder rejection.

Один Rippon PDF не является этим пакетом. `GILL-FAM-CANONICAL-PHYSICAL-PACKAGE` остаётся `PACKAGE_IDENTITY_UNRESOLVED`.

## 7. Что закрыто

```text
UNOWNED CLOSED-BOOK BACKLOG = CLOSED
FAMILY TAXONOMY = CLOSED
CLAIM SCOPE = CLOSED
REQUEST QUERIES = CLOSED
ACCEPTANCE CRITERIA = CLOSED
FALSE FULL-TEXT PROMOTION = BLOCKED
RIPPON 1838 EXACT FILE RECEIPT = CLOSED
RIPPON 1838 EDITION VERIFICATION = CLOSED
```

## 8. Current counts and open boundaries

```text
DURABLE FILE RECEIPTS = 1
VERIFIED PACKAGE RECEIPTS = 0
QUOTE-READY FAMILIES = 0
NEW DIRECT QUOTES = 0
REMAINING INSTITUTIONAL / PRIVATE FILE DELIVERY = OPEN
```

Receipt closure не означает claim или quotation closure. Для Rippon остаётся owner-scoped claim follow-up; для остальных families остаётся external acquisition.

## 9. Next valid action

Для Rippon выбрать один конкретный claim, проверить page image и context window, создать одну quote card и обновить соответствующий owner document. Отдельно можно получать следующую family, но массовое «добавить всё найденное» и смешивание family receipts запрещены.
