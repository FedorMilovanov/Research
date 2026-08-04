# Том 83. Whole-book integration manifest — «СЕРИЯ СЕРДЦЕ»

**Дата:** 2026-08-04  
**Authority ID:** `HEART-WHOLE-BOOK-INTEGRATION-2026-08-04`  
**Machine manifest:** `data/heart-whole-book-integration-2026-08-04.json`  
**Reader authority:** `data/heart-reader-assembly-2026-08-02.json`

```text
18-ENTRY OWNER MAPPING = COMPLETE
ASSEMBLED READER OWNERS = 3
PRODUCT SOURCE OWNERS = 5
RESEARCH DOSSIER OWNERS = 6
STANDALONE OWNER GAPS = 4
WHOLE-BOOK LINE EDIT = OPEN
WHOLE-BOOK CITATION PASS = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT RELEASE = NOT CLAIMED
NEW DIRECT QUOTES = 0
```

## 1. Что закрывает этот том

Решение тома 82 требовало сначала сопоставить весь утверждённый 18-позиционный порядок с реальными владельцами. Теперь каждая позиция имеет ровно один primary state:

- `ASSEMBLED_READER` — готовая читательская глава с P0 evidence owner;
- `PRODUCT_SOURCE_ONLY` — действующий Product source существует, но ещё не включён в единый manuscript bundle и не прошёл book-level citation pass;
- `RESEARCH_DOSSIER_ONLY` — source boundaries закрыты, но читательская рукопись ещё не собрана;
- `OWNER_REQUIRED` — отдельный manuscript owner ещё не установлен и не может быть подменён соседней главой.

Это mapping closure, а не заявление о готовой книге.

## 2. Exact Product snapshot

```text
repository = FedorMilovanov/gb-is-my-strength
commit = 0fbe7d1ead9ebd1bea867418e254da438ec63329
path = src/components/article-pilots/_shared/heartSeriesData.ts
blob = 553adbd67a459fa9e022f00b924e8c20201bf400
current core items = 6
book-matched core items = 5
outside final 18-entry order = spravochnik
```

Current Product core:

1. `prolog` — `/articles/chto-bibliya-nazyvaet-serdcem/`;
2. `krajne` — `/articles/krajne-li-isporcheno-serdce/`;
3. `rimlyanam` — `/articles/rimlyanam-7-veruyushchiy-ili-neveruyushchiy/`;
4. `novoe` — `/articles/novoe-serdce/`;
5. `serdce-duh` — `/articles/serdce-i-duh/`;
6. `spravochnik` — `/articles/serdce-spravochnik/`.

`spravochnik` остаётся полезным Product book-end, но не выдаётся за одну из 18 глав окончательного manuscript order.

## 3. Полная owner matrix

| № | Book entry | Primary state | Текущий владелец |
|---:|---|---|---|
| 1 | I.1 Что Библия называет сердцем | `PRODUCT_SOURCE_ONLY` | Product `prolog` |
| 2 | I.2 Сердце в Эдеме | `ASSEMBLED_READER` | dossier 75 + reader 79 |
| 3 | I.3 Падшее сердце: Иеремия 17 | `PRODUCT_SOURCE_ONLY` | Product `krajne` |
| 4 | I.4 Внутренний человек и телесная жизнь | `OWNER_REQUIRED` | отдельный owner отсутствует; `prolog` только support |
| 5 | II Диагноз падшего сердца | `RESEARCH_DOSSIER_ONLY` | R3 dossier 65 + R4 dossier 66 |
| 6 | III.1 Обещание нового сердца | `PRODUCT_SOURCE_ONLY` | Product `novoe` |
| 7 | III.2 Рождение свыше и обновление | `RESEARCH_DOSSIER_ONLY` | R1 dossiers 62–63 |
| 8 | III.3 Сокрушённое сердце: покаяние | `ASSEMBLED_READER` | dossier 76 + reader 80 |
| 9 | III.4 Сердце и Дух | `PRODUCT_SOURCE_ONLY` | Product `serdce-duh` + R2 dossier 64 |
| 10 | IV Сердце и слово Божие | `RESEARCH_DOSSIER_ONLY` | R7a dossier 68 |
| 11 | V Сердце в борьбе с грехом | `PRODUCT_SOURCE_ONLY` | Product `rimlyanam` + dossiers 65–67 |
| 12 | VI Сердце ученика и фарисея | `RESEARCH_DOSSIER_ONLY` | R7b dossier 69 |
| 13 | VII Сердце в страдании и унынии | `OWNER_REQUIRED` | отдельный current manuscript owner отсутствует |
| 14 | VIII Взирая на славу Христа | `RESEARCH_DOSSIER_ONLY` | R8 dossier 70 |
| 15 | IX Христос Апокалипсиса и сердце | `RESEARCH_DOSSIER_ONLY` | R9 dossier 71 |
| 16 | X.1 Суд сердца: два воскресения | `ASSEMBLED_READER` | dossier 77 + reader 81 |
| 17 | X.2 Освобождённое сердце | `OWNER_REQUIRED` | отдельный current manuscript owner отсутствует |
| 18 | X.3 Заключительная надежда | `OWNER_REQUIRED` | отдельный current manuscript owner отсутствует |

## 4. Deduplication ownership

Manifest закрепляет не только пути, но и границы повторения:

- I.1 владеет book-wide определением сердца;
- I.2 владеет полной последовательностью Быт. 1–3;
- I.3 владеет развёрнутой экзегезой Иер. 17;
- III.1 владеет обетованием Иез. 36, III.2 — причинным объяснением рождения свыше, III.3 — покаянием и плодом;
- IV владеет принятием Слова и просвещением Духа;
- V владеет различением двух борьб;
- VI владеет различением ученика и религиозного самосохранения;
- VIII владеет созерцанием и преображением;
- IX владеет Личностью и властью воскресшего Христа;
- X.1 владеет судебной развилкой, X.2 — положительным прославлением, X.3 — book-level надеждой.

Соседняя глава может дать короткий переход, но не может повторить полный argument owner-главы.

## 5. Citation boundary

```text
P0 READER BOUNDARIES VALIDATED = 3
PRODUCT SOURCE CITATION PASS REQUIRED = 5
R-DOSSIER BOUNDARIES AVAILABLE / MANUSCRIPT REQUIRED = 6
OWNER AND CITATION PASS REQUIRED = 4
WHOLE-BOOK CITATION PASS = OPEN
NEW DIRECT QUOTES APPROVED = 0
```

Наличие Product page не означает, что её footnotes автоматически согласованы с будущим manuscript bundle. Наличие Research dossier не означает, что читательская глава уже написана. Отсутствующий owner нельзя маскировать копированием соседнего материала.

## 6. Что остаётся открытым

1. назначить или собрать manuscript owners для I.4, VII, X.2 и X.3;
2. собрать reader manuscripts для шести `RESEARCH_DOSSIER_ONLY` entries;
3. выполнить read-only citation/reference inventory всех 18 entries;
4. только затем провести whole-book line edit, transitions и повторный dedup pass;
5. создать единый manuscript bundle и отдельный Product release transaction.

## 7. Запрещённые ложные выводы

```text
18-ENTRY MAPPING COMPLETE ≠ MANUSCRIPT COMPLETE
SOURCE DOSSIER CLOSED ≠ READER CHAPTER ASSEMBLED
PRODUCT SOURCE EXISTS ≠ BOOK CITATION PASS COMPLETE
PUBLIC-DOMAIN SOURCE ≠ NEW DIRECT QUOTE APPROVED
RESEARCH COMPLETE ≠ PRODUCT RELEASED
```

## 8. Решение

Первый этап whole-book integration закрыт: все 18 позиций имеют проверяемый disposition и dedup owner. Следующий канонический шаг — не ещё один общий source marathon, а bounded manuscript-owner closure для четырёх gaps и затем единый read-only citation inventory.
