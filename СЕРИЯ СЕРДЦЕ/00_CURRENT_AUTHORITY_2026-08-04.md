# СЕРИЯ СЕРДЦЕ — current authority

**Дата:** 2026-08-04  
**Authority ID:** `HEART-CURRENT-AUTHORITY-2026-08-04`  
**Статус:** `CURRENT / EVIDENCE AND THREE P0 READERS CLOSED / ALL EIGHTEEN ENTRY OWNERS MAPPED / MANUSCRIPT AND CITATION PASSES OPEN`  
**Предыдущая authority:** `00_CURRENT_AUTHORITY_2026-08-02.md`

## 1. Текущая композиция authority

1. `00_CURRENT_AUTHORITY_2026-08-01.md` — R1–R9 source boundaries и исторический Site closure.
2. `74_SOURCE_CLOSURE_REGISTRY_2026-08-01.json` — 85-source machine authority.
3. `78_P0_ARCHITECTURE_CLOSURE_OVERLAY_2026-08-02.md` и `data/heart-p0-architecture-dossiers-2026-08-02.json` — три P0 evidence owners.
4. `data/heart-reader-assembly-2026-08-02.json` и том 82 — три assembled readers, final order и editorial decisions.
5. `data/heart-whole-book-integration-2026-08-04.json` и том 83 — baseline 18-entry owner/dedup/citation mapping.
6. `data/heart-vii-owner-closure-2026-08-04.json` и том 84 — superseding overlay для current owner state VII.
7. `data/heart-i4-owner-closure-2026-08-04.json` и том 85 — superseding overlay для current owner state I.4.
8. `data/heart-x2-owner-closure-2026-08-04.json` и том 86 — superseding overlay для current owner state X.2.
9. `data/heart-x3-owner-closure-2026-08-04.json` и том 87 — superseding overlay для current owner state X.3 и aggregate effective counts.

При конфликте по текущему статусу overlays применяются последовательно: baseline → VII → I.4 → X.2 → X.3. Исторические snapshots, evidence boundaries и transaction counts не переписываются.

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
I.4 SOURCE OWNER CLUSTER = CLOSED
UNIFIED I.4 READER = NOT ASSEMBLED
X.2 SOURCE OWNER = CLOSED
UNIFIED X.2 READER = NOT ASSEMBLED
X.3 CONCLUSION SECTION OWNER = CLOSED
ALL 18 ENTRY OWNERS = MAPPED
PRODUCT SOURCE OWNERS = 9
RESEARCH DOSSIER OWNERS = 6
STANDALONE OWNER GAPS = 0
WHOLE-BOOK LINE EDIT = OPEN
WHOLE-BOOK CITATION PASS = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT RELEASE = NOT CLAIMED
NEW DIRECT QUOTES = 0
```

### Overlay transaction ledger

```text
AFTER VII OVERLAY:
PRODUCT SOURCE OWNERS = 6
STANDALONE OWNER GAPS = 3

AFTER I.4 OVERLAY:
PRODUCT SOURCE OWNERS = 7
STANDALONE OWNER GAPS = 2

AFTER X.2 OVERLAY:
PRODUCT SOURCE OWNERS = 8
STANDALONE OWNER GAPS = 1

AFTER X.3 OVERLAY / CURRENT:
PRODUCT SOURCE OWNERS = 9
STANDALONE OWNER GAPS = 0
```

Ledger фиксирует последовательные authority-транзакции, а не конкурирующие current states.

## 3. Effective 18-entry integration state

| State | Count | Meaning |
|---|---:|---|
| `ASSEMBLED_READER` | 3 | P0 reader manuscript and evidence owner both exist |
| `PRODUCT_SOURCE_ONLY` | 9 | current Product source, source cluster or section owner exists; book citation/line-edit pass still required |
| `RESEARCH_DOSSIER_ONLY` | 6 | evidence boundaries exist; reader manuscript still required |
| `OWNER_REQUIRED` | 0 | all final-order entries have deterministic source ownership |

Current Product core registry contains six items. Five map directly into the 18-entry book order; `spravochnik` remains an external book-end. VII maps to `tma` + `skorb`; I.4 maps to `telo` + supporting core `prolog`; X.2 and X.3 share one physical Product article through explicit section partitioning.

## 4. VII current owner

```text
Product commit = 0fbe7d1ead9ebd1bea867418e254da438ec63329
heartSeriesData blob = 553adbd67a459fa9e022f00b924e8c20201bf400
hardTextsSeriesConfig blob = 152c90b2dcee67d1683289445d0d2239905ed41c
primary = tma / tma-na-serdce / 34 min
support = skorb / serdce-pod-skorbyu / 28 min
```

Research owners: V84B theological correction, V84D source-integrity closure and V84I post-merge material/safety authority.

```text
VII SOURCE OWNER CLUSTER = CLOSED
UNIFIED VII READER = NOT ASSEMBLED
VII BOOK-LEVEL CITATION INVENTORY = OPEN
```

## 5. I.4 current owner

```text
primary = telo / serdce-i-telo / 23 min
support = prolog / chto-bibliya-nazyvaet-serdcem / 39 min
```

Research owners:

- V81 — inner person, decisions, intentions, embodied habits and historical-Adams boundary;
- V82 — body-soul unity, bodily influence and medical-competence boundary.

```text
I.4 SOURCE OWNER CLUSTER = CLOSED
UNIFIED I.4 READER = NOT ASSEMBLED
I.4 BOOK-LEVEL CITATION INVENTORY = OPEN
```

I.4 owns embodied inner-person integration. It does not absorb I.1's whole biblical definition or VII's depression/safety chapter.

## 6. X.2 current owner

```text
primary = osvobozhdennoe / osvobozhdennoe-serdce / 27 min
article path = src/content/articles/osvobozhdennoe-serdce.mdx
article blob = 16a2390da6e0d0382165fc8bf8b7150cb9253c1f
```

X.2 owns five exact Product sections:

- `chetyre-sostoyaniya`;
- `vopl-i-otvet`;
- `ne-besplotnoe-parenie`;
- `ne-sposobno-greshit`;
- `pobeda-nad-vragom`.

Research boundaries come from dossier 77 and reader 81: bodily resurrection remains personal and material, the judicial fork belongs to X.1, and no millennial system is smuggled into one lexical or grammatical observation.

```text
X.2 SOURCE OWNER = CLOSED
UNIFIED X.2 READER = NOT ASSEMBLED
X.2 BOOK-LEVEL CITATION INVENTORY = OPEN
```

## 7. X.3 current owner

X.3 shares the exact Product article with X.2 but has an independent semantic owner:

```text
product id = osvobozhdennoe
slug = osvobozhdennoe-serdce
article blob = 16a2390da6e0d0382165fc8bf8b7150cb9253c1f
section id = vyhod
section heading = Выход: сердце, наконец успокоенное
```

The `vyhod` section recalls the journey from corruption through new birth, conflict, idols, temptations, fear and darkness; turns from endless self-analysis to the face of God and final satisfaction; and ends in Christ-centred perseverance.

Research/editorial owners:

- R9 — the person, authority and glory of the risen Christ;
- book assembly authority 82 — X.3 as final entry and no reopened R10 dossier;
- X.2 authority 86 — explicit shared-file section partition.

```text
X.3 CONCLUSION SECTION OWNER = CLOSED
X.3 BOOK INTEGRATION = NOT COMPLETE
X.3 BOOK-LEVEL CITATION INVENTORY = OPEN
```

X.3 does not re-prove X.2 glorification and does not reopen X.1 judicial sequencing.

## 8. Что больше не является backlog

- evidence dossiers для I.2, III.3 и X.1;
- reader manuscripts I.2, III.3 и X.1;
- роль R9;
- роль `κατοπτριζόμενοι` excursus;
- final 18-entry order;
- cross-chapter dedup ownership;
- source-owner discovery для любой из 18 final-order entries;
- поиск source owners для VII, I.4, X.2 или X.3;
- новое общее исследование depression/body-soul, inner-person/body, glorification или concluding hope с нуля.

Эти решения нельзя снова объявлять открытыми без конкретного противоречащего evidence.

## 9. Настоящий следующий backlog

### Manuscript owner gaps

NONE — all 18 entries have deterministic owners

### Dossier-to-reader assembly

Reader manuscripts остаются несобранными или неинтегрированными для:

- I.1 `Что Библия называет сердцем` — Product source selected;
- I.3 `Падшее сердце: Иеремия 17` — Product source selected;
- I.4 `Внутренний человек и телесная жизнь` — Product source cluster selected;
- II `Диагноз падшего сердца` — Research dossiers selected;
- III.1 `Обещание нового сердца` — Product source selected;
- III.2 `Рождение свыше и обновление` — Research dossiers selected;
- III.4 `Сердце и Дух` — Product source plus R2 selected;
- IV `Сердце и слово Божие` — Research dossier selected;
- V `Сердце в борьбе с грехом` — Product source and dossiers selected;
- VI `Сердце ученика и фарисея` — Research dossier selected;
- VII `Сердце в страдании и унынии` — Product source cluster selected;
- VIII `Взирая на славу Христа` — Research dossier selected;
- IX `Христос Апокалипсиса и сердце` — Research dossier selected;
- X.2 `Освобождённое сердце` — exact Product source and doctrinal sections selected;
- X.3 `Заключительная надежда` — exact Product conclusion section selected.

The three assembled readers I.2, III.3 and X.1 remain governed by dossiers 75–77 and reader files 79–81.

### Whole-book QA

- read-only citation/reference inventory всех 18 entries;
- assemble or select reader manuscripts without adding unregistered claims;
- transitions and final dedup pass;
- one manuscript bundle with machine manifest;
- whole-book line edit;
- separate Product release and live witness.

## 10. Fail-closed правила

- Owner mapping closure не равен manuscript completion.
- Product source, cluster or section owner не считается final-book reader chapter.
- Product source не считается прошедшим book-level citation pass автоматически.
- Research dossier не считается читательской главой.
- Shared physical file does not imply shared semantic ownership; X.2 and X.3 remain section-partitioned.
- Новая прямая цитата запрещена без locator/version/context и registry update.
- Negative boundaries registry 74, P0 dossiers, V81/V82 and V84B/V84D/V84I обязательны для reader text.
- Исторические медицинские тезисы Адамса не являются current clinical guidance.
- Депрессия, травма и телесная немощь не объявляются грехом по умолчанию.
- Полная неспособность грешить принадлежит состоянию славы, а не нынешней христианской жизни.
- Телесное воскресение не подменяется бесплотным продолжением души.
- X.3 не добавляет новый R10 dossier и не вводит новые исторические или лексические claims.
- Одна millennial схема не выдаётся за лексическое значение Ин. 5 или Откр. 20.
- Research не может заявлять Product publication без отдельного exact-release witness.

## 11. Product snapshot boundary

```text
current Product core items = 6
book-matched Product core items = 5
selected Product satellites = 4
Product-owned final-order entries = 9
unique Product pages mapped = 9
```

X.2 and X.3 share one Product page through distinct section owners. Existing publication отдельных материалов не утверждает, что final 18-entry manuscript уже собран или выпущен.

## 12. Решение

Authority `HEART-CURRENT-AUTHORITY-2026-08-04` теперь композирует baseline и четыре owner overlays. Все 18 final-order entries имеют deterministic owners; owner discovery завершён. Следующая каноническая фаза — reader/manuscript assembly and a read-only citation inventory, followed by transitions, final deduplication, whole-book line edit and a separate Product release transaction.
