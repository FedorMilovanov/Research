# Том 85. I.4 «Внутренний человек и телесная жизнь» — source-owner closure

**Дата:** 2026-08-04  
**Authority ID:** `HEART-I4-OWNER-CLOSURE-2026-08-04`  
**Base authority:** `data/heart-whole-book-integration-2026-08-04.json`  
**Dependency:** `data/heart-vii-owner-closure-2026-08-04.json`  
**Machine overlay:** `data/heart-i4-owner-closure-2026-08-04.json`

```text
I.4 SOURCE OWNER CLUSTER = CLOSED
PRIMARY PRODUCT SOURCE = serdce-i-telo
SUPPORTING PRODUCT SOURCE = chto-bibliya-nazyvaet-serdcem
UNIFIED I.4 READER = NOT ASSEMBLED
WHOLE-BOOK CITATION PASS = OPEN
OWNER GAPS REMAINING = 2
NEW DIRECT QUOTES = 0
PRODUCT RELEASE OF FINAL BOOK = NOT CLAIMED
```

## 1. Причина повторной проверки

Baseline whole-book manifest поставил I.4 в `OWNER_REQUIRED`, оставив Product `prolog` только supporting owner. После закрытия VII был выполнен отдельный exact Product/Research readback.

Он показал, что I.4 имеет собственный source-owner cluster:

- Product satellite `serdce-i-telo` прямо владеет темой сердца, тела, членов, привычек, комфорта и аппетитов;
- Product core `chto-bibliya-nazyvaet-serdcem` задаёт book-wide whole-person определение сердца;
- V81 владеет внутренним человеком, намерениями, решениями, телесно закреплёнными дорожками и ограничениями исторических медицинских тезисов Адамса;
- V82 владеет телесно-духовным единством человека и medical-competence boundary.

Следовательно, gap относился к mapping, а не к отсутствию всякого владельца. Эта authority не утверждает, что готовая глава I.4 уже собрана из указанных материалов.

## 2. Exact Product authority

```text
repository = FedorMilovanov/gb-is-my-strength
commit = 0fbe7d1ead9ebd1bea867418e254da438ec63329
core registry blob = 553adbd67a459fa9e022f00b924e8c20201bf400
satellite registry blob = 152c90b2dcee67d1683289445d0d2239905ed41c
```

### Primary source

```text
id = telo
slug = serdce-i-telo
minutes = 23
role = heart-body-members-habits-appetites primary source
```

Reader-facing title: «Сердце и тело». Краткая Product-граница: «Члены как орудия, комфорт, аппетиты».

### Supporting source

```text
id = prolog
slug = chto-bibliya-nazyvaet-serdcem
minutes = 39
role = whole-person biblical-heart definition support
```

Product-пары и минуты проверяются по exact checkout и двум Git blobs, а не по переписанному Research-списку.

## 3. Research authority chain

### V81

`60_V81_JAY_ADAMS_PRIMARY_SOURCE_DEEPENING.md`

V81 удерживает:

- сердце как внутреннего человека, а не только эмоциональную часть личности;
- мышление, намерения, решения и мотивирующий источник внешней жизни;
- остаточный грех как поступок и телесно закреплённую привычную дорожку;
- необходимость проверяемых данных вместо претензии советника читать скрытые мотивы;
- запрет превращать исторические медицинские и психиатрические тезисы Адамса в современную рекомендацию проекта.

### V82

`61_V82_PSYCHOTROPIC_MEDICATION_BODY_SOUL_BIBLICAL_COUNSELING.md`

V82 удерживает:

- человека как телесно-духовное единство;
- реальность телесной болезни, боли, недосыпания, интоксикации и действия препаратов;
- несводимость совести, греха, веры, поклонения и надежды к биологическому описанию;
- запрет пастору без медицинской квалификации назначать, отменять или менять дозировку рецептурного препарата;
- недопустимость и биологического, и псевдодуховного редукционизма.

## 4. Effective disposition I.4

```text
previous primary state = OWNER_REQUIRED
effective primary state = PRODUCT_SOURCE_ONLY
citation state = PRODUCT_SOURCE_CITATION_PASS_REQUIRED
manuscript state = SOURCE_CLUSTER_SELECTED / UNIFIED READER NOT ASSEMBLED
```

`PRODUCT_SOURCE_ONLY` здесь означает, что current reader-facing sources и Research boundaries установлены. Это не означает автоматическую склейку Product-страниц в окончательную chapter manuscript.

## 5. Dedup owner

I.4 владеет:

- whole-person relation внутреннего человека и телесной жизни;
- влиянием тела без биологического редукционизма;
- членами тела как орудиями;
- телесно закреплёнными привычками и learned pathways;
- комфортом и аппетитами в связи с направлением сердца;
- medical-competence boundary.

I.4 не должен повторно владеть:

- полной лексической и канонической картой сердца из I.1;
- подробным материалом VII о депрессивной тьме, реальной/ложной вине и urgent safety;
- полной главой III.3 о покаянии;
- историческими медицинскими тезисами Адамса как современной clinical guidance.

## 6. Effective counts

```text
FINAL BOOK ENTRIES = 18
ASSEMBLED READER OWNERS = 3
PRODUCT SOURCE OWNERS = 7
RESEARCH DOSSIER OWNERS = 6
STANDALONE OWNER GAPS = 2
SELECTED PRODUCT SATELLITES = 3
NEW DIRECT QUOTES = 0
```

Оставшиеся owner gaps:

1. X.2 `Освобождённое сердце`;
2. X.3 `Заключительная надежда`.

## 7. Что закрыто

```text
I.4 PRODUCT SOURCE IDENTIFICATION = CLOSED
I.4 RESEARCH AUTHORITY IDENTIFICATION = CLOSED
I.4 SOURCE-OWNER CLUSTER = CLOSED
I.4 DEDUP BOUNDARY = CLOSED
FALSE OWNER_REQUIRED STATUS = SUPERSEDED
```

## 8. Что остаётся открытым

```text
UNIFIED I.4 READER = NOT ASSEMBLED
I.4 BOOK-LEVEL CITATION INVENTORY = OPEN
WHOLE-BOOK LINE EDIT = OPEN
WHOLE-BOOK CITATION PASS = OPEN
MANUSCRIPT BUNDLE = INCOMPLETE
PRODUCT RELEASE OF FINAL 18-ENTRY BOOK = NOT CLAIMED
```

Новые direct quotes не утверждены. Existing Product publication не является release witness окончательной книги.

## 9. Решение

I.4 больше не является standalone owner gap. Текущий канонический source cluster — Product `telo` + `prolog`, ограниченный V81/V82. Следующий I.4 lane — reader assembly и citation inventory, а не новое общее исследование тела и души с нуля.
