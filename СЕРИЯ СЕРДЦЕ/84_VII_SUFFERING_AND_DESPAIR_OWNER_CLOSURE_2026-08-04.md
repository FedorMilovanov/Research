# Том 84. VII «Сердце в страдании и унынии» — source-owner closure

**Дата:** 2026-08-04  
**Authority ID:** `HEART-VII-OWNER-CLOSURE-2026-08-04`  
**Base authority:** `data/heart-whole-book-integration-2026-08-04.json`  
**Machine overlay:** `data/heart-vii-owner-closure-2026-08-04.json`

```text
VII SOURCE OWNER CLUSTER = CLOSED
PRIMARY PRODUCT SOURCE = tma-na-serdce
SUPPORTING PRODUCT SOURCE = serdce-pod-skorbyu
UNIFIED VII READER = NOT ASSEMBLED
WHOLE-BOOK CITATION PASS = OPEN
OWNER GAPS REMAINING = 3
NEW DIRECT QUOTES = 0
PRODUCT RELEASE OF FINAL BOOK = NOT CLAIMED
```

## 1. Почему baseline показывал owner gap

Первый 18-entry manifest консервативно поставил VII в `OWNER_REQUIRED`, потому что отдельного файла с названием окончательной главы VII не было среди трёх новых P0 readers и R1–R9 dossiers.

Повторная проверка показала, что это был gap mapping, а не gap материала:

- Product уже содержит самостоятельную статью о тьме, унынии, телесно-душевной природе человека, реальной и ложной вине, диагнозе и safety boundaries;
- Product уже содержит отдельную companion-статью о скорби, провидении и плаче;
- Research main содержит полный V84 chain от богословской коррекции до source locator closure и post-merge total audit;
- V84I прямо фиксирует, что material text base complete для текущей publication stage.

Baseline 2026-08-04 сохраняется как честный snapshot до этого readback. Эта authority supersedes только disposition VII и эффективные счётчики.

## 2. Exact Product authority

```text
repository = FedorMilovanov/gb-is-my-strength
commit = 0fbe7d1ead9ebd1bea867418e254da438ec63329
core registry blob = 553adbd67a459fa9e022f00b924e8c20201bf400
satellite registry blob = 152c90b2dcee67d1683289445d0d2239905ed41c
```

### Primary source

```text
id = tma
slug = tma-na-serdce
minutes = 34
role = depression-darkness-body-soul-guilt-safety primary source
```

Reader-facing title: «Тьма на сердце». Управляющий вопрос: «Всегда ли уныние — грех?»

### Supporting source

```text
id = skorb
slug = serdce-pod-skorbyu
minutes = 28
role = suffering-providence-lament companion source
```

Reader-facing title: «Сердце под скорбью». Управляющая линия: страдание, провидение и плач.

Обе пары проверяются не по переписанному списку в Research, а по exact Product checkout и Git blob `hardTextsSeriesConfig.ts`.

## 3. Research authority chain

### V84B

`65_V84B_DEPRESSION_THEOLOGICAL_PRIMACY_AND_AXIS_CORRECTION.md`

Владеет богословским порядком и разделением уровней: человек перед Богом, общая повреждённость мира, телесные факторы, конкретная вина, субъективное переживание и clinical classification не смешиваются в один однородный список.

### V84D

`67_V84D_SOURCE_LOCATOR_AND_EVIDENCE_STATUS_CLOSURE.md`

Владеет source-integrity, locator и evidence-status corrections. Красивый пересказ не получает более сильного статуса, чем реально доступный источник.

### V84I

`72_V84I_POST_MERGE_TOTAL_AUDIT_AND_CLOSURE_GATES.md`

Владеет post-merge state и итоговой границей:

- material text base complete для текущей publication stage;
- theological and safety boundaries complete для текущей публикации;
- содержательные Product-источники находятся в `main`;
- historical HOLD и evidence restrictions сохраняются там, где они нужны.

## 4. Effective disposition VII

```text
previous primary state = OWNER_REQUIRED
effective primary state = PRODUCT_SOURCE_ONLY
citation state = PRODUCT_SOURCE_CITATION_PASS_REQUIRED
manuscript state = SOURCE_CLUSTER_SELECTED / UNIFIED READER NOT ASSEMBLED
```

Название `PRODUCT_SOURCE_ONLY` означает, что действующий reader-facing source cluster установлен. Оно не означает, что две статьи уже слиты в одну окончательную chapter manuscript.

## 5. Dedup owner

VII владеет:

- страданием и депрессивной тьмой;
- whole-person body/soul framing;
- различением реальной вины, ложной вины и страдания без доказанной личной вины;
- плачем и провидением;
- компетенцией, referral и urgent safety boundaries;
- запретом морализировать диагноз или автоматически диагностировать библейских лиц.

VII не должен повторно владеть:

- полной главой III.3 о покаянии, исповедании, restitution и плоде;
- III.3 distinctions между прощением, примирением, доверием и пригодностью к должности;
- полным богословием нового рождения;
- всей book-wide антропологией I.1.

## 6. Effective counts

```text
FINAL BOOK ENTRIES = 18
ASSEMBLED READER OWNERS = 3
PRODUCT SOURCE OWNERS = 6
RESEARCH DOSSIER OWNERS = 6
STANDALONE OWNER GAPS = 3
SELECTED PRODUCT SATELLITES FOR VII = 2
NEW DIRECT QUOTES = 0
```

Оставшиеся честные owner gaps:

1. I.4 `Внутренний человек и телесная жизнь`;
2. X.2 `Освобождённое сердце`;
3. X.3 `Заключительная надежда`.

## 7. Что закрыто

```text
VII PRODUCT SOURCE IDENTIFICATION = CLOSED
VII RESEARCH AUTHORITY IDENTIFICATION = CLOSED
VII SOURCE-OWNER CLUSTER = CLOSED
VII DEDUP BOUNDARY = CLOSED
FALSE OWNER_REQUIRED STATUS = SUPERSEDED
```

## 8. Что остаётся открытым

```text
UNIFIED VII READER = NOT ASSEMBLED
VII BOOK-LEVEL CITATION INVENTORY = OPEN
WHOLE-BOOK LINE EDIT = OPEN
WHOLE-BOOK CITATION PASS = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT RELEASE OF FINAL 18-ENTRY BOOK = NOT CLAIMED
```

Ни один новый direct quote не утверждён. Existing Product publication двух статей не является release witness окончательной 18-entry книги.

## 9. Решение

VII больше не является standalone owner gap. Текущий канонический owner — Product source cluster `tma` + `skorb`, ограниченный V84B/V84D/V84I. Следующий допустимый шаг для VII — bounded reader assembly и citation inventory, а не новое общее исследование депрессии с нуля.
