# СЕРИЯ СЕРДЦЕ — current authority

**Дата:** 2026-08-04  
**Authority ID:** `HEART-CURRENT-AUTHORITY-2026-08-04`  
**Статус:** `CURRENT / ALL 18 ENTRIES OWNER-MAPPED / MANUSCRIPT ASSEMBLY, CITATION, LINE EDIT AND PRODUCT RELEASE OPEN`  
**Предыдущая authority:** `00_CURRENT_AUTHORITY_2026-08-02.md`

## 1. Текущая композиция authority

1. `00_CURRENT_AUTHORITY_2026-08-01.md` — R1–R9 source boundaries и исторический Site closure.
2. `74_SOURCE_CLOSURE_REGISTRY_2026-08-01.json` — 85-source machine authority.
3. `78_P0_ARCHITECTURE_CLOSURE_OVERLAY_2026-08-02.md` и `data/heart-p0-architecture-dossiers-2026-08-02.json` — три P0 evidence owners.
4. `data/heart-reader-assembly-2026-08-02.json` и том 82 — три assembled readers, final order и editorial decisions.
5. `data/heart-whole-book-integration-2026-08-04.json` и том 83 — baseline 18-entry owner/dedup/citation mapping.
6. `data/heart-vii-owner-closure-2026-08-04.json` и том 84 — VII source-owner overlay.
7. `data/heart-i4-owner-closure-2026-08-04.json` и том 85 — I.4 source-owner overlay.
8. `data/heart-x2-owner-closure-2026-08-04.json` и том 86 — X.2 glorification source-owner overlay.
9. `data/heart-x3-owner-closure-2026-08-04.json` и том 87 — X.3 conclusion-section overlay и финальные effective counts.

При конфликте по current owner state overlays применяются последовательно:

```text
baseline → VII → I.4 → X.2 → X.3
```

Исторические snapshots и evidence boundaries не переписываются.

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
FINAL-BOOK X.3 MANUSCRIPT = NOT ASSEMBLED
ALL 18 ENTRIES OWNER-MAPPED = TRUE
PRODUCT SOURCE OWNERS = 8
PRODUCT SECTION OWNERS = 1
RESEARCH DOSSIER OWNERS = 6
STANDALONE OWNER GAPS = 0
WHOLE-BOOK LINE EDIT = OPEN
WHOLE-BOOK CITATION PASS = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT RELEASE = NOT CLAIMED
NEW DIRECT QUOTES = 0
```

## 3. Overlay transaction ledger

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
PRODUCT SOURCE OWNERS = 8
PRODUCT SECTION OWNERS = 1
STANDALONE OWNER GAPS = 0
```

Ledger фиксирует последовательные authority transactions, а не конкурирующие current states.

## 4. Effective 18-entry integration state

| State | Count | Meaning |
|---|---:|---|
| `ASSEMBLED_READER` | 3 | P0 reader manuscript and evidence owner both exist |
| `PRODUCT_SOURCE_ONLY` | 8 | current Product source or source cluster exists; book citation/line-edit pass still required |
| `PRODUCT_SECTION_ONLY` | 1 | exact section owner exists inside an already-counted Product page |
| `RESEARCH_DOSSIER_ONLY` | 6 | evidence boundaries exist; reader manuscript still required |
| `OWNER_REQUIRED` | 0 | no remaining owner-discovery gap |

Equation:

```text
3 + 8 + 1 + 6 = 18
```

Unique Product pages mapped remain `9`; X.3 reuses the X.2 article only through a separate section boundary and therefore does not inflate the page count.

## 5. VII current owner

```text
Product commit = 0fbe7d1ead9ebd1bea867418e254da438ec63329
heartSeriesData blob = 553adbd67a459fa9e022f00b924e8c20201bf400
hardTextsSeriesConfig blob = 152c90b2dcee67d1683289445d0d2239905ed41c
primary = tma / tma-na-serdce / 34 min
support = skorb / serdce-pod-skorbyu / 28 min
```

Research owners: V84B, V84D and V84I.

```text
VII SOURCE OWNER CLUSTER = CLOSED
UNIFIED VII READER = NOT ASSEMBLED
VII BOOK-LEVEL CITATION INVENTORY = OPEN
```

## 6. I.4 current owner

```text
primary = telo / serdce-i-telo / 23 min
support = prolog / chto-bibliya-nazyvaet-serdcem / 39 min
```

Research owners: V81 and V82.

```text
I.4 SOURCE OWNER CLUSTER = CLOSED
UNIFIED I.4 READER = NOT ASSEMBLED
I.4 BOOK-LEVEL CITATION INVENTORY = OPEN
```

I.4 owns embodied inner-person integration. It does not absorb I.1's whole biblical definition or VII's depression/safety chapter.

## 7. X.2 current owner

```text
primary = osvobozhdennoe / osvobozhdennoe-serdce / 27 min
article path = src/content/articles/osvobozhdennoe-serdce.mdx
article blob = 16a2390da6e0d0382165fc8bf8b7150cb9253c1f
```

X.2 owns exactly:

- `chetyre-sostoyaniya`;
- `vopl-i-otvet`;
- `ne-besplotnoe-parenie`;
- `ne-sposobno-greshit`;
- `pobeda-nad-vragom`.

Research boundaries come from dossier 77 and reader 81.

```text
X.2 SOURCE OWNER = CLOSED
UNIFIED X.2 READER = NOT ASSEMBLED
X.2 BOOK-LEVEL CITATION INVENTORY = OPEN
```

## 8. X.3 current owner

```text
Product page = osvobozhdennoe-serdce
Product section = vyhod
section title = Выход: сердце, наконец успокоенное
state = PRODUCT_SECTION_ONLY
```

The section begins with the explicit whole-series claim `И вот последнее, к чему шла вся серия` and ends before `Источники и сверка`.

X.3 owns only:

- the final recap of the journey from corruption through regeneration and struggle;
- the turn from endless introspection to the face of God;
- final rest, satisfaction and perseverance in Christ;
- the closing pastoral contrast `Здесь — война. Там — Он.`

X.3 excludes all five X.2 glorification sections and introduces no new doctrine, historical claim or quotation package.

```text
X.3 CONCLUSION SECTION OWNER = CLOSED
FINAL-BOOK X.3 MANUSCRIPT = NOT ASSEMBLED
X.3 BOOK-LEVEL CITATION INVENTORY = OPEN
```

## 9. Что больше не является backlog

- evidence dossiers for I.2, III.3 and X.1;
- reader manuscripts I.2, III.3 and X.1;
- R9 role;
- `κατοπτριζόμενοι` role;
- final 18-entry order;
- cross-chapter dedup ownership;
- owner discovery for VII, I.4, X.2 and X.3;
- the question of current owner disposition for any of the 18 entries;
- another open-ended source marathon for depression, body/soul, glorification or the final conclusion.

## 10. Настоящий следующий backlog

### Manuscript owner gaps

```text
NONE / CLOSED
```

Owner discovery is complete. This does not mean reader manuscripts are complete.

### Dossier-to-reader assembly

Reader manuscripts remain unassembled for:

- I.4 `Внутренний человек и телесная жизнь`;
- II `Диагноз падшего сердца`;
- III.2 `Рождение свыше и обновление`;
- IV `Сердце и слово Божие`;
- VI `Сердце ученика и фарисея`;
- VII `Сердце в страдании и унынии`;
- VIII `Взирая на славу Христа`;
- IX `Христос Апокалипсиса и сердце`;
- X.2 `Освобождённое сердце`;
- X.3 `Заключительная надежда`.

### Whole-book QA

- one read-only citation/reference inventory across all 18 entries;
- manuscript assembly for dossier/source/section-owned entries;
- transitions and repeated-paragraph deduplication;
- heading, terminology and pastoral-warning normalization;
- whole-book line edit;
- one machine-readable manuscript bundle;
- separate Product release and live witness.

## 11. Fail-closed rules

- Owner mapping closure is not manuscript completion.
- A Product source or section is not automatically a final-book reader chapter.
- A Product source is not automatically book-level citation-pass complete.
- A Research dossier is not a reader chapter.
- `PRODUCT_SECTION_ONLY` may not be inflated into a second unique Product page.
- X.3 may not absorb X.2's five glorification sections.
- New direct quotation requires locator/version/context and registry update.
- R9's partially verified quotation warnings remain controlling.
- Historical medical claims from Adams are not current clinical guidance.
- Depression, trauma and bodily weakness are not declared sin by default.
- Complete inability to sin belongs to glory, not the present Christian life.
- Bodily resurrection is not replaced by disembodied continuation.
- One millennial system is not presented as the lexical meaning of John 5 or Revelation 20.
- Research cannot claim Product publication without a separate exact-release witness.

## 12. Product snapshot boundary

```text
current Product core items = 6
book-matched Product core items = 5
selected Product satellites = 4
selected Product section owners = 1
unique Product pages mapped = 9
Product-owned book entries = 9
```

Existing publication of individual pages does not mean the final 18-entry manuscript is assembled or released.

## 13. Decision

Authority `HEART-CURRENT-AUTHORITY-2026-08-04` now composes baseline, VII, I.4, X.2 and X.3 overlays. All eighteen entries have an owner disposition and standalone owner gaps are zero. The next canonical Heart work is manuscript assembly plus one whole-book citation/reference inventory; line edit, manuscript bundle and Product release remain separate later transactions.
