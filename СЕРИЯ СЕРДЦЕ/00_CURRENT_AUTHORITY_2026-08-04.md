# СЕРИЯ СЕРДЦЕ — current authority

**Дата:** 2026-08-04  
**Authority ID:** `HEART-CURRENT-AUTHORITY-2026-08-04`  
**Статус:** `CURRENT / EVIDENCE AND THREE P0 READERS CLOSED / EIGHTEEN-ENTRY OWNER MAPPING CLOSED / MANUSCRIPT AND CITATION PASSES OPEN`  
**Предыдущая authority:** `00_CURRENT_AUTHORITY_2026-08-02.md`

## 1. Текущая композиция authority

1. `00_CURRENT_AUTHORITY_2026-08-01.md` — R1–R9 source boundaries и исторический Site closure.
2. `74_SOURCE_CLOSURE_REGISTRY_2026-08-01.json` — 85-source machine authority.
3. `78_P0_ARCHITECTURE_CLOSURE_OVERLAY_2026-08-02.md` и `data/heart-p0-architecture-dossiers-2026-08-02.json` — три P0 evidence owners.
4. `data/heart-reader-assembly-2026-08-02.json` и том 82 — три assembled readers, final order и editorial decisions.
5. `data/heart-whole-book-integration-2026-08-04.json` и том 83 — current 18-entry owner/dedup/citation mapping.

При конфликте по текущему статусу эта authority и manifest 2026-08-04 имеют приоритет. Исторические evidence boundaries не переписываются.

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
WHOLE-BOOK LINE EDIT = OPEN
WHOLE-BOOK CITATION PASS = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT RELEASE = NOT CLAIMED
NEW DIRECT QUOTES = 0
```

## 3. 18-entry integration state

| State | Count | Meaning |
|---|---:|---|
| `ASSEMBLED_READER` | 3 | P0 reader manuscript and evidence owner both exist |
| `PRODUCT_SOURCE_ONLY` | 5 | current Product source exists; book citation/line-edit pass still required |
| `RESEARCH_DOSSIER_ONLY` | 6 | evidence boundaries exist; reader manuscript still required |
| `OWNER_REQUIRED` | 4 | no standalone manuscript owner may yet be claimed |

The current Product registry contains six core items. Five map into the 18-entry book order; `spravochnik` remains an external book-end rather than a numbered manuscript entry.

## 4. Что больше не является backlog

- evidence dossiers для I.2, III.3 и X.1;
- reader manuscripts I.2, III.3 и X.1;
- роль R9;
- роль `κατοπτριζόμενοι` excursus;
- final 18-entry order;
- cross-chapter dedup ownership;
- вопрос «какой current owner у каждой из 18 позиций».

Эти решения нельзя снова объявлять открытыми без конкретного противоречащего evidence.

## 5. Настоящий следующий backlog

### Manuscript owner gaps

1. I.4 `Внутренний человек и телесная жизнь`;
2. VII `Сердце в страдании и унынии`;
3. X.2 `Освобождённое сердце`;
4. X.3 `Заключительная надежда`.

### Dossier-to-reader assembly

Reader manuscripts остаются несобранными для:

- II `Диагноз падшего сердца`;
- III.2 `Рождение свыше и обновление`;
- IV `Сердце и слово Божие`;
- VI `Сердце ученика и фарисея`;
- VIII `Взирая на славу Христа`;
- IX `Христос Апокалипсиса и сердце`.

### Whole-book QA

- read-only citation/reference inventory всех 18 entries;
- transitions и повторный dedup pass;
- единый manuscript bundle;
- whole-book line edit;
- отдельный Product release и live witness.

## 6. Fail-closed правила

- Mapping closure не равен manuscript completion.
- Product source не считается прошедшим book-level citation pass автоматически.
- Research dossier не считается читательской главой.
- Отсутствующий owner нельзя подменить соседней главой или runtime-generated summary.
- Новая прямая цитата запрещена без locator/version/context и registry update.
- Negative boundaries registry 74 и P0 dossiers обязательны для reader text.
- Депрессия, травма и телесная немощь не объявляются грехом по умолчанию.
- Прощение, примирение, доверие и пригодность к должности не смешиваются.
- Одна millennial схема не выдаётся за лексическое значение Ин. 5 или Откр. 20.
- Research не может заявлять Product publication без отдельного exact-release witness.

## 7. Product snapshot boundary

```text
Product commit = 0fbe7d1ead9ebd1bea867418e254da438ec63329
heartSeriesData blob = 553adbd67a459fa9e022f00b924e8c20201bf400
current Product core items = 6
book-matched Product core items = 5
```

Этот snapshot используется только для owner mapping. Он не утверждает, что final 18-entry manuscript уже опубликован.

## 8. Решение

Authority `HEART-CURRENT-AUTHORITY-2026-08-04` supersedes authority 2026-08-02 только в current status/navigation layer. Серия перешла от P0 assembly к book-level integration: owner mapping закрыт, manuscript construction, citation pass, line edit и Product release остаются отдельными последующими транзакциями.
