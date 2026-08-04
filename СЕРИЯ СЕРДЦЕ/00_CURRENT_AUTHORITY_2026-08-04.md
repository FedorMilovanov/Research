# СЕРИЯ СЕРДЦЕ — current authority

**Дата:** 2026-08-04  
**Authority ID:** `HEART-CURRENT-AUTHORITY-2026-08-04`  
**Статус:** `CURRENT / EVIDENCE AND THREE P0 READERS CLOSED / EIGHTEEN-ENTRY MAPPING CLOSED / VII SOURCE OWNER CLUSTER CLOSED / MANUSCRIPT AND CITATION PASSES OPEN`  
**Предыдущая authority:** `00_CURRENT_AUTHORITY_2026-08-02.md`

## 1. Текущая композиция authority

1. `00_CURRENT_AUTHORITY_2026-08-01.md` — R1–R9 source boundaries и исторический Site closure.
2. `74_SOURCE_CLOSURE_REGISTRY_2026-08-01.json` — 85-source machine authority.
3. `78_P0_ARCHITECTURE_CLOSURE_OVERLAY_2026-08-02.md` и `data/heart-p0-architecture-dossiers-2026-08-02.json` — три P0 evidence owners.
4. `data/heart-reader-assembly-2026-08-02.json` и том 82 — три assembled readers, final order и editorial decisions.
5. `data/heart-whole-book-integration-2026-08-04.json` и том 83 — baseline 18-entry owner/dedup/citation mapping.
6. `data/heart-vii-owner-closure-2026-08-04.json` и том 84 — superseding overlay для current owner state VII и effective counts.

При конфликте по текущему статусу эта authority и overlay 2026-08-04 имеют приоритет. Baseline manifest сохраняется как проверяемый snapshot до VII readback; исторические evidence boundaries не переписываются.

## 2. Текущий статус

```text
R1-R9 SOURCE CLOSURE = CLOSED WITH NEGATIVE BOUNDARIES
THREE P0 EVIDENCE DOSSIERS = CLOSED
THREE P0 READER CHAPTERS = ASSEMBLED
R9 ROLE = CLOSED
KATOPTRIZOMENOI ROLE = CLOSED
FINAL ORDER = CLOSED
CROSS-CHAPTER OWNER RULES = CLOSED
18-ENTRY OWNER MAPPING = COMPLETE
VII SOURCE OWNER CLUSTER = CLOSED
UNIFIED VII READER = NOT ASSEMBLED
WHOLE-BOOK LINE EDIT = OPEN
WHOLE-BOOK CITATION PASS = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT RELEASE = NOT CLAIMED
NEW DIRECT QUOTES = 0
```

## 3. Effective 18-entry integration state

| State | Count | Meaning |
|---|---:|---|
| `ASSEMBLED_READER` | 3 | P0 reader manuscript and evidence owner both exist |
| `PRODUCT_SOURCE_ONLY` | 6 | current Product source or source cluster exists; book citation/line-edit pass still required |
| `RESEARCH_DOSSIER_ONLY` | 6 | evidence boundaries exist; reader manuscript still required |
| `OWNER_REQUIRED` | 3 | no standalone manuscript/source owner may yet be claimed |

Current Product core registry contains six items. Five map directly into the 18-entry book order; `spravochnik` remains an external book-end. VII additionally maps to two exact Product satellites, `tma` and `skorb`, through the pinned satellite registry.

## 4. VII current owner

### Exact Product witness

```text
Product commit = 0fbe7d1ead9ebd1bea867418e254da438ec63329
heartSeriesData blob = 553adbd67a459fa9e022f00b924e8c20201bf400
hardTextsSeriesConfig blob = 152c90b2dcee67d1683289445d0d2239905ed41c
primary = tma / tma-na-serdce / 34 min
support = skorb / serdce-pod-skorbyu / 28 min
```

### Research owners

- V84B — theological primacy and axis correction;
- V84D — source locator and evidence-status closure;
- V84I — post-merge material, theological and safety closure.

### Boundary

VII теперь `PRODUCT_SOURCE_ONLY`, а не `OWNER_REQUIRED`. Это означает source-owner closure, но не unified chapter completion:

```text
VII SOURCE OWNER CLUSTER = CLOSED
UNIFIED VII READER = NOT ASSEMBLED
VII BOOK-LEVEL CITATION INVENTORY = OPEN
```

## 5. Что больше не является backlog

- evidence dossiers для I.2, III.3 и X.1;
- reader manuscripts I.2, III.3 и X.1;
- роль R9;
- роль `κατοπτριζόμενοι` excursus;
- final 18-entry order;
- cross-chapter dedup ownership;
- вопрос «какой current owner у каждой из 18 позиций»;
- поиск source owners для VII `Сердце в страдании и унынии`;
- новое общее исследование депрессии, тьмы, body/soul и safety с нуля.

Эти решения нельзя снова объявлять открытыми без конкретного противоречащего evidence.

## 6. Настоящий следующий backlog

### Manuscript owner gaps

1. I.4 `Внутренний человек и телесная жизнь`;
2. X.2 `Освобождённое сердце`;
3. X.3 `Заключительная надежда`.

### Dossier-to-reader assembly

Reader manuscripts остаются несобранными для:

- II `Диагноз падшего сердца`;
- III.2 `Рождение свыше и обновление`;
- IV `Сердце и слово Божие`;
- VI `Сердце ученика и фарисея`;
- VII `Сердце в страдании и унынии` — Product source cluster выбран, единая глава не собрана;
- VIII `Взирая на славу Христа`;
- IX `Христос Апокалипсиса и сердце`.

### Whole-book QA

- read-only citation/reference inventory всех 18 entries;
- transitions и повторный dedup pass;
- единый manuscript bundle;
- whole-book line edit;
- отдельный Product release и live witness.

## 7. Fail-closed правила

- Mapping closure не равен manuscript completion.
- Product source cluster не считается единой reader chapter.
- Product source не считается прошедшим book-level citation pass автоматически.
- Research dossier не считается читательской главой.
- Отсутствующий owner нельзя подменить соседней главой или runtime-generated summary.
- Новая прямая цитата запрещена без locator/version/context и registry update.
- Negative boundaries registry 74, P0 dossiers и V84B/V84D/V84I обязательны для reader text.
- Депрессия, травма и телесная немощь не объявляются грехом по умолчанию.
- Диагноз не является ни нравственным приговором, ни сертификатом невиновности.
- Прощение, примирение, доверие и пригодность к должности не смешиваются.
- Одна millennial схема не выдаётся за лексическое значение Ин. 5 или Откр. 20.
- Research не может заявлять Product publication без отдельного exact-release witness.

## 8. Product snapshot boundary

```text
current Product core items = 6
book-matched Product core items = 5
selected Product satellites for VII = 2
Product pages currently mapped into book ownership = 7
```

Этот snapshot используется только для owner mapping. Existing publication отдельных материалов не утверждает, что final 18-entry manuscript уже собран или выпущен.

## 9. Решение

Authority `HEART-CURRENT-AUTHORITY-2026-08-04` теперь композирует baseline manifest и VII overlay. Серия имеет три честных owner gaps вместо четырёх. Следующая каноническая работа — закрыть I.4, X.2 и X.3, собрать reader manuscripts из существующих dossiers/source clusters и затем выполнить единый citation pass; whole-book line edit и Product release остаются отдельными транзакциями.
