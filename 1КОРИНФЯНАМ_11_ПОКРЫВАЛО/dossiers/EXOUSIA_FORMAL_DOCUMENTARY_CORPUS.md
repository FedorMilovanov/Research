# 1 Коринфянам 11:10 — `ἐξουσία` formal + documentary corpus

**Статус:** `EVERGREEN-CONTROLLING-DOSSIER / TEXTUAL-LEXICAL-DOCUMENTARY / RESEARCH-ONLY / PUBLICATION-HOLD`  
**Создано:** 2026-08-10

## 0. Назначение

Это устойчивое досье для текущего исследования `ἐξουσία` в 1 Кор 11:10.

Оно не заменяет current claim registry для grade, а собирает в одном месте:

- греческий текст и вариант `κάλυμμα`;
- синтаксическую форму `ἐξουσία + ἐπί`;
- точную таксономию библейских параллелей;
- систематическую документальную папирологию;
- реальные женские юридические/эпиграфические примеры;
- границы отрицательного поиска;
- открытые acquisition/HOLD.

Исторические `00ZZ...` файлы остаются provenance/receipt. Новые находки по этому узлу следует добавлять сюда, а не создавать очередной `pass_N` или `CURRENT_POINTER`.

```text
CLAIM_GRADE_OWNER = CURRENT_CLAIM_REGISTRY
THIS_DOSSIER = CONTROLLING_EVIDENCE_MAP_FOR_EXOUSIA
```

---

# 1. Текущий текст и минимальная синтаксическая база

1 Кор 11:10:

```text
διὰ τοῦτο ὀφείλει ἡ γυνὴ ἐξουσίαν ἔχειν ἐπὶ τῆς κεφαλῆς διὰ τοὺς ἀγγέλους
```

Минимум, который не зависит от богословской модели:

```text
SUBJECT = ἡ γυνή
VERBAL_CONSTRUCTION = ἐξουσίαν ἔχειν
PP = ἐπὶ τῆς κεφαλῆς
```

Следовательно:

```text
EXOUSIA_WOMAN_SUBJECT = A_SYNTAX
```

Сам этот факт не решает, **какое именно право/власть или отношение к голове** имеется в виду.

---

# 2. `ἐξουσίαν` против ранней `κάλυμμα`-традиции

Текущий textual control:

- перечисленная extant Greek manuscript tradition, включая P46 и основные кодексы, поддерживает `ἐξουσίαν`;
- `κάλυμμα` относится к ранней versional/patristic explanatory transmission/gloss stream;
- в текущем аппарате не подтверждён extant Greek NT manuscript, который давал бы `κάλυμμα` как конкурирующее исходное чтение 1 Кор 11:10.

Safe formulation:

```text
V10_GREEK_EXOUSIAN = OVERWHELMING_EXTANT_GREEK_MS_CONTROL
V10_KALYMMA = EARLY_VERSIONAL/PATRISTIC_GLOSS_STREAM
KALYMMA_AS_EXTANT_GREEK_MS_RIVAL = NOT_ESTABLISHED
```

Ириней/валентинианская передача veil-form показывает раннее **понимание/перефразирование**, но не доказывает, что Ириней имел греческий экземпляр 1 Кор с `κάλυμμα`.

```text
IRENAEUS_GREEK_EXEMPLAR_KALYMMA = UNPROVED
```

---

# 3. Базовая семантическая направленность `ἐξουσίαν ἔχειν`

Независимые линии сходятся в одном минимуме:

1. женщина — субъект конструкции в v10;
2. Pauline/NT употребления `ἐξουσία` обычно описывают право, способность, власть или область полномочия;
3. Hooker и Fitzmyer исторически подчёркивали активную семантическую силу;
4. documentary Greek показывает устойчивую конструкцию `ἐξουσίαν ἔχω` как активное обладание правом/полномочием;
5. реальные женщины в документах/надписях выступают носителями такого права.

Текущая калибровка:

```text
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH
EXOUSIA_EXACT_REFERENT = B_C
```

Это означает:

```text
ACTIVE_SEMANTIC_DIRECTION = STRONG
EXACT_CONTEXTUAL_MEANING = OPEN
```

Не означает:

```text
MODERN_AUTONOMY_THEOLOGY = PROVED
NO_TEXTILE_SIGN_CAN_BE_INVOLVED = PROVED
EXACT_SCOPE_OF_AUTHORITY = SOLVED
```

---

# 4. Formal taxonomy: `ἐξουσία` + `ἐπί`

## 4.1 Почему нужна таксономия

В specialist literature встречается формулировка, что примеров `ἐξουσίαν ἔχειν ἐπί + genitive` много. Это корректно **семантически** только при условии, что не все перечисляемые loci объявляются одинаковыми формальными конструкциями.

Нужно различать:

```text
EXACT_ECHO_EPI_GEN
FRONTED_EPI_GEN_ECHO
EXOUSIA_EPI_GEN_WITH_OTHER_SUPPORT_VERB
EXOUSIA_EPI_ACC
GENITIVE_PHRASE_CONTAINING_EPI
```

---

## 4.2 Revelation 14:18 — самый чистый точный параллельный паттерн

```text
ὁ ἔχων ἐξουσίαν ἐπὶ τοῦ πυρός
```

Форма:

```text
ἔχω + ἐξουσίαν + ἐπί + genitive
```

Семантика:

```text
SUBJECT POSSESSES AUTHORITY OVER DOMAIN/OBJECT
```

Классификация:

```text
REV_14_18 = EXACT_SUPPORT_VERB_PATTERN
```

Это не head-covering parallel; это формальный active-authority parallel.

---

## 4.3 Revelation 20:6 — те же компоненты с вынесенным PP

```text
ἐπὶ τούτων ὁ δεύτερος θάνατος οὐκ ἔχει ἐξουσίαν
```

Форма:

```text
ἐπί + genitive [fronted]
+ subject
+ ἔχω + ἐξουσία
```

Классификация:

```text
REV_20_6 = EXACT_LEXEMES_AND_RELATION / DIFFERENT_WORD_ORDER
```

---

## 4.4 Revelation 2:26 — `δίδωμι`, не `ἔχω`

```text
δώσω αὐτῷ ἐξουσίαν ἐπὶ τῶν ἐθνῶν
```

Форма:

```text
δίδωμι + ἐξουσίαν + ἐπί + genitive
```

Классификация:

```text
REV_2_26 = ACTIVE_AUTHORITY_OVER_DOMAIN
SUPPORT_VERB != ἔχω
```

Нельзя считать его точным `ἐξουσίαν ἔχειν` параллелем.

---

## 4.5 Daniel OG 3:97 — related LXX authority-domain construction

Засвидетельствовано:

```text
ἐξουσίαν δοὺς ἐφ’ ὅλης τῆς χώρας
```

Форма:

```text
δίδωμι/δοὺς + ἐξουσίαν + ἐπί + genitive
```

Классификация:

```text
DAN_OG_3_97 = LXX_SEMANTIC_PARALLEL
NOT_EXACT_ECHO_SUPPORT_VERB
```

---

## 4.6 Luke 9:1 — `ἐπί + accusative`

```text
ἔδωκεν αὐτοῖς δύναμιν καὶ ἐξουσίαν ἐπὶ πάντα τὰ δαιμόνια
```

Форма:

```text
δίδωμι + ἐξουσίαν + ἐπί + accusative
```

Классификация:

```text
LUKE_9_1 = AUTHORITY_OVER_DOMAIN_SEMANTICS
CASE != GENITIVE
SUPPORT_VERB != ἔχω
```

---

## 4.7 Sirach 17:2 — не прямой `ἐπί`-комплемент

```text
ἔδωκεν αὐτοῖς ἐξουσίαν τῶν ἐπ’ αὐτῆς
```

Здесь:

```text
τῶν ἐπ’ αὐτῆς
```

является генитивной группой «того/тех, что на ней [земле]», а не чистым прямым `ἐπί + genitive`-комплементом к `ἐξουσία`.

Классификация:

```text
SIR_17_2 = RELATED_AUTHORITY_DOMAIN_EXAMPLE
NOT_FORMALLY_EXACT_EPI_COMPLEMENT
```

---

# 5. Вывод из formal taxonomy

Правильная формулировка:

```text
AUTHORITY_OVER_DOMAIN_WITH_EXOUSIA = WELL_ATTESTED_BIBLICAL_GREEK
EXACT_ECHO_EPI_GEN = DIRECTLY_ATTESTED_AT_LEAST_REV_14_18
FRONTED_EQUIVALENT = REV_20_6
```

Запрещённые shortcuts:

```text
"ἐξουσία + ἐπί + genitive has no parallels" = FALSE
"all six commonly listed loci are exact formal parallels" = FALSE
"uncommon in documentary papyri = ungrammatical in Greek" = FALSE
"syntax forces a passive sign" = FALSE
```

---

# 6. Arzt-Grabner / PKNT p.390 — что реально закрыто

Библиография:

> Peter Arzt-Grabner et al., *1. Korinther*, Papyrologischer Kommentar zum Neuen Testament 2 (2006).

Статус:

```text
PKNT2_BIBLIOGRAPHIC_EXISTENCE = VERIFIED_INSTITUTIONAL
AUTHOR_UPLOAD_ROUTE = VERIFIED_EXISTS
PKNT_P390_DIRECT_PAGE_BYTES = HOLD
```

Jill Marshall page-specifically cites p.390 for observation that `ἐξουσία` with `ἐπί + genitive` is **uncommon**.

До получения самой p.390 project-safe inference:

```text
PKNT_UNCOMMON = PAPYROLOGICAL/DOCUMENTARY_OBSERVATION
PKNT_UNCOMMON != UNATTESTED_GREEK
PKNT_UNCOMMON != ARGUMENT_FOR_PASSIVE_EXOUSIA_BY_ITSELF
```

Do not invent the exact wording of p.390.

---

# 7. Fendel 2023 — systematic documentary-papyrus corpus

Victoria Beatrix Fendel systematically searched documentary papyri for `ἐξουσίαν`.

Direct reported corpus:

```text
DOCUMENTS_WITH_EXOUSIAN = 272
TOTAL_EXOUSIAN_TOKENS = 290
TOTAL_EXOUSIAN_ECHO = 190
```

Roman-period higher-register `ἐξουσίαν ἔχω` complement table:

```text
INF = 105
ARTICULAR_INFINITIVE = 1
GENITIVE = 4
PP = 3
NO_OVERT_OBJECT = 2
LOST = 3
```

Key result:

```text
EXOUSIAN_ECHEIN_ROMAN_DOCUMENTARY_GREEK = STRONGLY_ATTESTED
ACTIVE_RIGHT/POWER_POSSESSION = NORMAL_DOCUMENTARY_DIRECTION
```

---

# 8. Fendel PP boundary

Fendel's published article table confirms **three Roman higher-register PP complements**, but the main article text/table does not list the three actual prepositions.

Oxford ORA exposes the associated dataset:

```text
EXOUSIAN.xlsx
```

but current runtime has not successfully acquired/parsing the binary file.

Therefore:

```text
FENDEL_ROMAN_PP_COUNT = 3_VERIFIED
FENDEL_ROMAN_PP_PREPOSITIONS = NOT_YET_ENUMERATED
FENDEL_ROMAN_PP_IS_EPI_GEN = NOT_ESTABLISHED
```

Known direct documentary female example PSI X 1115 has:

```text
περὶ αὐτοῦ
```

not `ἐπί + genitive`.

Never convert `PP=3` into `ἐπί/gen.=3` without reading the dataset rows.

---

# 9. Real female documentary / epigraphic bearers

## 9.1 PSI X 1115 — 28 Dec 152 CE, Tebtunis

Marriage/property contract.

The female-side legal control includes:

```text
ἐξουσίαν ἔχειν οἰκονομεῖν ... ὡς ἐὰν αἱρῆται
```

Minimum semantic result:

```text
FEMALE_BEARER + EXOUSIAN_ECHEIN + RIGHT_TO_MANAGE/DISPOSE
```

This is a real Roman-period documentary construction, not a head-covering parallel.

---

## 9.2 TAM II 603 — Lalla, Tlos

Roman-period funerary inscription.

Core:

```text
ἐπὶ τῷ ἔχειν ἐξουσίαν τὴν Λάλλαν ... ζῶσα συνχωρῆσαι
```

Safe minimum:

```text
LALLA = FEMALE_RIGHT_BEARER
RIGHT = GRANT_PERMISSION_WHILE_ALIVE
```

Any bracketed restored wording must remain visibly restored.

---

## 9.3 TAM II 604 — neighboring formula

```text
ἕτερος δὲ οὐδὲ εἷς ἕξει ἐξουσίαν
οὔτε συνχωρῆσαί τινι οὔτε ἐνθάψαι τινά
```

Independent local confirmation:

```text
ECHEIN_EXOUSIAN + INFINITIVE = AUTHORITY/RIGHT_TO_DO_X
```

---

## 9.4 P.Wisc. I 13 — female testamentary formula

A female will preserves/restores a formula of full authority over one's property.

Important evidence class:

```text
FEMALE_TESTAMENTARY_EXOUSIA_FORMULA = REAL
EXACT_LETTERS_IN_RESTORED_REGION = NOT_ALL_INSCRIBED_CERTAINTY
```

Use as formulaic/restored support, not as an unqualified direct-letter quote.

---

## 9.5 P.Oxy. I 104 — 26 Dec 96 CE, semantic-near control

Female property-control language includes being `κυρία` of her own property and managing it as she chooses.

No `ἐξουσία` lexeme.

Class:

```text
FEMALE_PROPERTY_CONTROL_SEMANTICS = STRONG_NEAR_PARALLEL
LEXICAL_EXOUSIA_PARALLEL = NO
```

This distinction matters because it is chronologically close to the Pauline world but not lexical evidence for the noun itself.

---

# 10. Evidence-class ladder

Future agents should classify parallels this way:

```text
A. EXACT_FORMAL
   same core lexemes + support verb + syntactic relation

B. FORMAL_NEAR
   same exousia-domain syntax but different support verb/order/case

C. DOCUMENTARY_LEXICAL
   exousian echein in legal documentary context

D. FEMALE_BEARER
   woman as real legal subject of exousia/right

E. SEMANTIC_NEAR
   same kind of control/right without exousia lexeme

F. RECONSTRUCTION
   proposed exact Corinthian social meaning
```

Do not promote C/D/E into A.

---

# 11. The fabricated P.Oxy. 84.5575 lesson

The quarantined AI citation invented an unrealistically perfect parallel:

```text
woman
+ head covering
+ Roman custom
+ exousia
+ household control
```

Real evidence is distributed across separate sources instead.

Current firewall:

```text
REAL_CORPUS > PERFECT_FABRICATED_PARALLEL
NO_EXACT_HEAD_PARALLEL_FOUND != LICENSE_TO_INVENT_ONE
CONSTRUCTION_LEVEL_PARALLEL = VALID_EVIDENCE
```

---

# 12. Bounded negative: exact extra-biblical head phrase

Current bounded searches have not located a nonbiblical exact parallel of the form:

```text
ἐξουσίαν ἔχειν ἐπὶ τῆς κεφαλῆς
```

Safe status:

```text
EXACT_NONBIBLICAL_HEAD_PARALLEL = NOT_FOUND_IN_BOUNDED_SEARCH
GLOBAL_NONEXISTENCE = NOT_CLAIMED
```

This negative result concerns **acquisition**, not grammaticality.

---

# 13. What the corpus strengthens

Independent provenance now supports:

```text
WOMAN_IS_SUBJECT = A
ACTIVE_RIGHT/POWER_SEMANTIC_PULL = B_HIGH
ACTIVE_AUTHORITY_OVER_DOMAIN_SYNTAX = ATTESTED
FEMALE_RIGHT_BEARERS_IN_ROMAN_DOCUMENTS = DIRECTLY_ATTESTED
```

Thus a reading that makes `ἐξουσία` lexically mean:

```text
veil
symbol
sign of husband's authority
```

cannot be obtained from the noun/construction alone.

A contextual/metonymic **sign interpretation remains logically arguable**, but it must be argued from discourse/history, not presented as the ordinary lexical value of `ἐξουσία`.

---

# 14. What the corpus does NOT solve

Still open:

```text
EXACT_REFERENT_OF_EXOUSIA = B_C
```

Live contextual proposals include, among others:

- control/right regarding her own head/head presentation;
- authority/right to pray and prophesy;
- status/authority signaled through covering/head presentation;
- a contextual metonymic authority-sign reading;
- other discourse-specific relations.

The corpus does not automatically decide between them.

---

# 15. Relation to Peters / Jantsch / modern active readings

Modern models that connect v10 with female agency or head control include Peters, Jantsch and others.

The documentary/formal corpus gives those models a **real active-semantic substrate**.

But:

```text
ACTIVE_SEMANTICS != JANTSCH_EXACT_HAIR_TRIGGER_PROVED
ACTIVE_SEMANTICS != PETERS_CITIZEN_BODY_MODEL_PROVED
ACTIVE_SEMANTICS != WESTFALL_EXACT_REFERENT_PROVED
```

Historical reconstruction remains a separate evidence layer.

---

# 16. Current acquisition queue

```text
P0 PKNT 2 (2006) p390 + surrounding paragraph = DIRECT_PAGE_HOLD
P1 Fendel EXOUSIAN.xlsx = ACQUIRE_BINARY_AND_ENUMERATE_3_ROMAN_PP_ROWS
P1 search nonbiblical literary/epigraphic exact ἔχω + ἐξουσία + ἐπί/gen = CONTINUE
P1 locate additional female Roman documentary subjects = CONTINUE_IF_HIGH_VALUE
P1 verify P.Wisc restored formula against edition image/text apparatus = OPEN
```

Do not spend cycles searching for a cosmetically perfect head-covering parallel at the expense of corpus-quality evidence.

---

# 17. Current result

```text
CORE_GRADE_REVERSALS = 0

EXOUSIA_WOMAN_SUBJECT = A_SYNTAX
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH
EXOUSIA_EXACT_REFERENT = B_C

V10_EXOUSIAN_GREEK = STRONG_TEXTUAL_CONTROL
KALYMMA = EARLY_GLOSS/TRANSMISSION_STREAM

REV_14_18 = EXACT_ECHO_EPI_GEN_FORMAL_CONTROL
REV_20_6 = FRONTED_EXACT_LEXEME/RELATION_CONTROL
REV_2_26 = DIDOMI_EPI_GEN_FORMAL_NEAR
DAN_OG_3_97 = DIDOMI_EPI_GEN_LXX_NEAR
LUKE_9_1 = DIDOMI_EPI_ACC_NEAR
SIR_17_2 = GENITIVE_PHRASE_WITH_INTERNAL_EPI / NOT_EXACT

FENDEL_2023 = SYSTEMATIC_DOCUMENTARY_CONTROL
FENDEL_ROMAN_PP_COUNT = 3
FENDEL_PP_PREPOSITIONS = HOLD_DATASET

FEMALE_EXOUSIA_BEARERS = DIRECTLY_ATTESTED
EXACT_NONBIBLICAL_HEAD_PARALLEL = NOT_FOUND_IN_BOUNDED_SEARCH

PUBLICATION_HOLD = true
PRODUCT_WRITE = false
SITE_PUBLICATION = false
```
