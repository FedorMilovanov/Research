# Том 75. Closed-book family acquisition authority

**Дата:** 2026-08-02  
**Authority ID:** `GILL-CLOSED-BOOK-FAMILIES-2026-08-02`  
**Статус:** `FAMILY OWNERSHIP CLOSED / REQUEST CRITERIA CLOSED / EXTERNAL FILE RECEIPTS OPEN`  
**Machine registry:** `data/gill-closed-book-families-2026-08-02.json`  
**Прямые цитаты:** `0 approved`

## 1. Что исправляет этот том

Ранний backlog говорил о «закрытых книгах» как об одной неопределённой корзине. Теперь каждая семья имеет:

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
| `GILL-FAM-BIOGRAPHICAL-PRIMARY` | Rippon, Crosby, White and biographical witnesses | partial open-access acquisition required |
| `GILL-FAM-FIRST-EDITIONS` | dates, title pages, edition conflicts | partial open-access acquisition required |
| `GILL-FAM-CANONICAL-PHYSICAL-PACKAGE` | archive custody and registry mapping | package identity unresolved |

## 3. Receipt ladder

```text
CATALOG / ABSTRACT / PREVIEW
→ navigation only

FULL FILE RECEIVED
→ requires bytes + SHA-256 + durable receipt

EDITION VERIFIED
→ requires title page + pagination + edition identity

CLAIM USABLE
→ requires exact owner scope and locator

QUOTE READY
→ requires page-image readback + context + rights basis
```

Ни один уровень не выводится из имени файла или поискового результата.

## 4. Search audit boundary

Connected Drive searches по английским и русским названиям выполнены как discovery pass. Они не создают receipt автоматически. Даже найденный объект должен пройти byte-level materialization/readback и mapping к конкретной family.

Поэтому допустимо говорить:

> Поиск выполнен; verified package receipt в Research пока не установлен.

Недопустимо говорить:

> Файлов точно нет.

или:

> Файл найден по имени, значит источник закрыт.

## 5. Canonical physical package

Package считается установленным только при наличии:

1. устойчивого package name;
2. полного manifest;
3. file names и family IDs;
4. byte sizes;
5. SHA-256 каждого файла и пакета;
6. durable storage receipt;
7. mapping к witness registry/owners;
8. duplicate and placeholder rejection.

До этого `GILL-FAM-CANONICAL-PHYSICAL-PACKAGE` остаётся `PACKAGE_IDENTITY_UNRESOLVED`.

## 6. Что закрыто

```text
UNOWNED CLOSED-BOOK BACKLOG = CLOSED
FAMILY TAXONOMY = CLOSED
CLAIM SCOPE = CLOSED
REQUEST QUERIES = CLOSED
ACCEPTANCE CRITERIA = CLOSED
FALSE FULL-TEXT PROMOTION = BLOCKED
```

## 7. Что остаётся внешним

```text
INSTITUTIONAL / PRIVATE FILE DELIVERY = OPEN
BYTE RECEIPTS = 0
QUOTE-READY FAMILIES = 0
NEW DIRECT QUOTES = 0
```

Это не незакрытый исследовательский вопрос о том, что нужно искать. Это внешний acquisition dependency с определённым контрактом.

## 8. Next valid action

Получить одну конкретную family, записать receipt, проверить edition/страницы, затем открыть только claim-bounded follow-up в соответствующем owner document. Массовое «добавить всё найденное» запрещено.
