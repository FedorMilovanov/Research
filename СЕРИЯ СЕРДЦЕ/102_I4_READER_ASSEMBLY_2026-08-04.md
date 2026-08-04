# Том 102. I.4 reader assembly — «Внутренний человек и телесная жизнь»

**Дата:** 2026-08-04  
**Authority ID:** `HEART-I4-READER-ASSEMBLY-2026-08-04`  
**Entry:** `HEART-BOOK-I4`  
**Final-order position:** `4 / 18`  
**Reader:** `101_READER_CHAPTER_I4_INNER_PERSON_EMBODIED_LIFE_2026-08-04.md`  
**Machine receipt:** `data/heart-i4-reader-assembly-2026-08-04.json`

## 1. Решение

```text
I.4 READER ASSEMBLY = COMPLETE
I.4 ENTRY CITATION PASS = OPEN
ASSEMBLED READERS = 6 / 18
MISSING STANDALONE FINAL READERS = 12
ENTRY CITATION PASSES COMPLETE = 5 / 18
ASSEMBLED READER CITATION REVIEWS = 5 / 6
WHOLE-BOOK READER ASSEMBLY = INCOMPLETE
WHOLE-BOOK CITATION PASS = OPEN
NEW DIRECT QUOTES APPROVED = 0
PRODUCT RELEASE = NOT CLAIMED
```

I.4 переводится из `PRODUCT_SOURCE_ONLY` в `ASSEMBLED_READER`. Citation pass не закрывается в этой транзакции.

## 2. Immutable source chain

```text
I.4 OWNER CLOSURE GIT BLOB = 5a7aa3ef29571255708c49692a6232177b7bcf14
PRECEDING CURRENT V2 GIT BLOB = 66d2f46cf639d9825b5b09fc4e94111be3af2a11
READER GIT BLOB = d683ed3f1e8d699f0232f9ee7a30dc0fa2400d74
PRIMARY PRODUCT GIT BLOB = dca5863c614cf3a4f8503d52a79bb76e705c9d2c
SUPPORT PRODUCT GIT BLOB = acc12804f5b2450efebbb6e0b2cabd31066ef48c
V81 GIT BLOB = f5b3491acad2e6a68197d6c1191ea3b9fb74aa75
V82 GIT BLOB = d62d76abe607335861745cc732a9aad8edc3b743
PRODUCT COMMIT = 0fbe7d1ead9ebd1bea867418e254da438ec63329
```

Reader, Product sources, V81, V82, owner closure и current V2 остаются read-only.

## 3. Source ownership

### Primary Product owner

```text
src/content/articles/serdce-i-telo.mdx
FULL SHA-256 = 79a1ce46206e504d082d0af9094bd308afc6abe3163d432099263ca5229c3ec2
```

Exact section owners:

1. `telo-ne-vrag`;
2. `chleny-oruzhie`;
3. `hram-kuplennyj`;
4. `zhivaya-zhertva`;
5. `komfort-gospodin`;
6. `ustalost`;
7. `ne-hlebom-odnim`;
8. `tverdo-ne-dubinkoy`;
9. `kak-otlichit`;
10. `vyhod`.

```text
PRIMARY UNIQUE SCRIPTURE REFERENCES = 8
PRIMARY QUOTATION SURFACES = 43
PRIMARY EXTERNAL LINKS = 0
PRIMARY INTERNAL ARTICLE LINKS = 3
```

### Bounded Product support

```text
src/content/articles/chto-bibliya-nazyvaet-serdcem.mdx
FULL SHA-256 = 50657f3473c06e16d75ffe740828a9311f642562e824f148113ae28ff9b03c07
```

Exact support sections:

1. `vnutrenniy-chelovek`;
2. `serdce-dusha-duh`.

```text
SUPPORT UNIQUE SCRIPTURE REFERENCES = 6
SUPPORT QUOTATION SURFACES = 10
SUPPORT EXTERNAL LINKS = 0
SUPPORT INTERNAL ARTICLE LINKS = 0
```

Support ownership ограничено unified-inner-person и whole-person vocabulary. Полное определение библейского сердца остаётся за I.1.

### Combined Product source scope

```text
COMBINED UNIQUE SCRIPTURE REFERENCES = 14
COMBINED QUOTATION SURFACES = 53
COMBINED EXTERNAL LINKS = 0
COMBINED INTERNAL ARTICLE LINKS = 3
PRODUCT SOURCE QUOTATION SURFACES TRANSFERRED = 0
PRODUCT SOURCE LINKS TRANSFERRED = 0
```

## 4. Research boundaries

V81 используется для четырёх ограниченных положений:

- сердце как единый внутренний человек;
- различение нравственного направления, привычки и отдельного действия;
- телесно закреплённые пути старого поведения;
- положительная замена старого пути новым послушанием.

V81 не используется как современное медицинское руководство. Его рискованные исторические медицинские утверждения остаются маркированными позицией автора.

V82 задаёт четыре обязательные границы:

- человек не сводится к телу;
- тело не объявляется несущественным;
- достаточность Писания не превращает Библию в медицинский справочник;
- пастырская помощь без соответствующей квалификации не подменяет клинические решения.

```text
V81 QUOTATION SEGMENTS TRANSFERRED = 0
V82 QUOTATION SEGMENTS TRANSFERRED = 0
NEW MEDICAL CLAIMS = 0
```

## 5. Reader composition

```text
COMPOSITION MODE = PARAPHRASE_ONLY
READER DETECTED SCRIPTURE REFERENCES = 9
READER QUOTATION SURFACES = 0
READER EXTERNAL LINKS = 0
READER INTERNAL ARTICLE LINKS = 0
READER DIRECT QUOTES = 0
NEW DIRECT QUOTES APPROVED = 0
```

Reader собирает одну линию:

1. сердце является единым внутренним человеком перед Богом;
2. этот человек живёт и действует телесно;
3. тело не является врагом и не получает престол;
4. решения сердца закрепляются в телесных привычках;
5. новое послушание требует конкретного выученного пути;
6. усталость требует одновременно телесной и нравственной оценки;
7. медицинская и пастырская компетенции не заменяют друг друга;
8. весь человек принадлежит Христу.

## 6. Dedup boundaries

```text
I.4 OWNS = embodied inner person, bodily members, learned pathways, bodily influence, weakness and competence boundaries
I.1 OWNS = complete biblical definition and vocabulary of the heart
VII OWNS = depression, despair, crisis safety and dedicated suffering treatment
```

I.4 не поглощает I.1 и VII. Она также не превращает body-soul unity в биологический детерминизм и не объявляет телесную немощь грехом по умолчанию.

## 7. State transition

```text
BEFORE:
I.4 = PRODUCT_SOURCE_ONLY
ASSEMBLED READERS = 5
MISSING READERS = 13
ENTRY CITATION PASSES COMPLETE = 5

AFTER:
I.4 = ASSEMBLED_READER
ASSEMBLED READERS = 6
MISSING READERS = 12
ENTRY CITATION PASSES COMPLETE = 5
```

Citation count не меняется, потому что assembly и citation review остаются отдельными транзакциями.

## 8. Remaining reader assemblies

```text
HEART-BOOK-I1
HEART-BOOK-I3
HEART-BOOK-II
HEART-BOOK-III1
HEART-BOOK-III2
HEART-BOOK-III4
HEART-BOOK-IV
HEART-BOOK-V
HEART-BOOK-VI
HEART-BOOK-VII
HEART-BOOK-VIII
HEART-BOOK-IX
```

```text
MISSING STANDALONE FINAL READERS = 12
PRODUCT SOURCE ONLY = 6
RESEARCH DOSSIER ONLY = 6
```

## 9. Permanent gate

```text
I.4 ASSEMBLY VALIDATOR = scripts/validate_heart_i4_reader_assembly.py
```

Heart workflow обязан выполнять:

```text
python3 scripts/validate_heart_i4_reader_assembly.py --product-root ../Product
```

Validator проверяет:

- immutable Research и Product blobs;
- exact twelve section IDs, SHA-256, bytes, references, quotation and link counts;
- V81/V82 boundary markers;
- reader title, required headings and word-count boundary;
- exact nine reader locators;
- zero reader quotation, link, footnote and blockquote surfaces;
- отсутствие material Product quotations, blockquotes и длинных дословных sentences;
- отсутствие длинных дословных V81/V82 sentences;
- historical owner and current V2 states;
- effective counts `6 readers / 12 missing / 5 citation passes`;
- clean Research and Product checkouts.

## 10. Fail-closed boundaries

```text
I.4 READER ASSEMBLY COMPLETE ≠ I.4 CITATION PASS COMPLETE
SIX READERS ASSEMBLED ≠ EIGHTEEN READERS ASSEMBLED
FIVE CITATION PASSES ≠ WHOLE-BOOK CITATION PASS COMPLETE
BODY-SOUL UNITY ≠ BIOLOGICAL DETERMINISM
BODILY WEAKNESS ≠ SIN BY DEFAULT
PASTORAL CARE ≠ MEDICAL PRACTICE
PRODUCT SOURCE PRESENT ≠ PRODUCT RELEASE
```

## 11. Следующая транзакция

Следующий шаг — отдельный I.4 entry citation pass. Он должен заново классифицировать reader locators, Product quotation surfaces, three internal links и V81/V82 evidence boundaries. До этого current citation completion остаётся `5 / 18`.

## 12. Final disposition

Authority `HEART-I4-READER-ASSEMBLY-2026-08-04` закрывает только сборку standalone reader I.4. Whole-book reader assembly, citation pass, transition/dedup, line edit, manuscript bundle и Product release остаются открытыми.
