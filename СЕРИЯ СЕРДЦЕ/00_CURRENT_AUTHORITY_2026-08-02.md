# СЕРИЯ СЕРДЦЕ — current authority

> **SUPERSEDED FOR CURRENT STATUS BY:** `00_CURRENT_AUTHORITY_2026-08-04.md`.  
> Этот файл сохраняется как immutable status snapshot после P0 closure и до whole-book owner mapping. Evidence boundaries ниже не отменены.

**Дата:** 2026-08-02  
**Authority ID:** `HEART-CURRENT-AUTHORITY-2026-08-02`  
**Статус:** `SUPERSEDED STATUS SNAPSHOT / EVIDENCE CLOSED FOR R1-R9 AND THREE P0 ARCHITECTURE DOSSIERS / EDITORIAL ASSEMBLY ACTIVE AT SNAPSHOT TIME`  
**Предыдущая authority:** `00_CURRENT_AUTHORITY_2026-08-01.md`

## 1. Текущая композиция authority

Эту серию нужно читать как композицию, а не выбирать последний большой файл по имени:

1. `00_CURRENT_AUTHORITY_2026-08-01.md` — status и source boundaries R1–R9;
2. `74_SOURCE_CLOSURE_REGISTRY_2026-08-01.json` — machine-readable source/claim closure R1–R9;
3. `74_PRIMARY_SOURCE_CLOSURE_60PLUS_2026-08-01.md` — человекочитаемый source closeout;
4. `78_P0_ARCHITECTURE_CLOSURE_OVERLAY_2026-08-02.md` — superseding authority для трёх P0 gaps;
5. `data/heart-p0-architecture-dossiers-2026-08-02.json` — machine-readable claims/sources/boundaries трёх P0 dossiers;
6. досье 75–77 — content owners для I.2, III.3 и X.1.

При конфликте по трём P0 темам overlay 78 и registry 2026-08-02 имеют приоритет над §5 authority 2026-08-01 и ранней book architecture.

## 2. Статусы

| Scope | Status | Authority |
|---|---|---|
| R1–R9 source closure | `CLOSED WITH PRESERVED NEGATIVE BOUNDARIES` | registry 74 + authority 2026-08-01 |
| I.2 Сердце в Эдеме | `EVIDENCE CLOSED / CHAPTER-READY` | dossier 75, claims EDEN-01…08 |
| III.3 Сокрушённое сердце | `EVIDENCE CLOSED / CHAPTER-READY` | dossier 76, claims REP-01…08 |
| X.1 Суд сердца: два воскресения | `EVIDENCE CLOSED / CHAPTER-READY` | dossier 77, claims JUDG-01…10 |
| reader chapter assembly | `ACTIVE EDITORIAL WORK` | this authority + overlay 78 |
| whole-book copyedit and deduplication | `OPEN EDITORIAL TASK` | future assembly authority |
| Product/site publication | `NOT CLAIMED` | requires separate Product release witness |

## 3. Что больше не является исследовательским долгом

- отдельное evidence-досье «Сердце в Эдеме»;
- отдельное evidence-досье о покаянии и сокрушении;
- отдельное evidence-досье о воскресении праведных/неправедных и последнем суде;
- source maps, locators и publication boundaries этих трёх глав;
- место трёх глав в последовательности книги.

Эти узлы не должны снова появляться в backlog как «нет исследования» без конкретного нового вопроса или опровержения evidence.

## 4. Следующий обязательный lane

Research lane завершён для названных P0 тем. Следующие операции относятся к editorial assembly:

1. собрать читательскую главу I.2 по dossier 75;
2. собрать читательскую главу III.3 по dossier 76;
3. собрать читательскую главу X.1 по dossier 77;
4. определить окончательную роль R9;
5. определить объём excursus `κατοπτριζόμενοι`;
6. утвердить final chapter table;
7. выполнить cross-chapter deduplication, transitions и book-level QA.

## 5. Fail-closed правила

- Новая прямая цитата запрещена без locator/version/context и registry update.
- `CLOSED` не означает право на неподтверждённую детализацию.
- `BOUNDARY_CLOSED` означает, что отрицательная граница обязательна для reader text.
- Досье нельзя заменять кратким summary, если summary стирает distinction.
- Депрессия, травма и телесная немощь не объявляются грехом по умолчанию.
- Прощение, примирение, доверие и пригодность к должности не смешиваются.
- Одна millennial схема не выдаётся за лексическое значение Ин. 5 или Откр. 20.
- Reader assembly не может утверждать, что книга или Site уже опубликованы.

## 6. Production boundary

Текущий статус на дату snapshot означал:

```text
RESEARCH EVIDENCE READY
BOOK ARCHITECTURE P0 READY
READER ASSEMBLY NOT YET COMPLETE
PRODUCT RELEASE NOT YET WITNESSED
```

## 7. Решение

Authority `HEART-CURRENT-AUTHORITY-2026-08-02` superseded authority 2026-08-01 only in status/navigation layer and for the three P0 gaps. Authority `HEART-CURRENT-AUTHORITY-2026-08-04` now supersedes this snapshot for current status after reader assembly and 18-entry owner mapping. Historical evidence and negative boundaries remain controlling.
