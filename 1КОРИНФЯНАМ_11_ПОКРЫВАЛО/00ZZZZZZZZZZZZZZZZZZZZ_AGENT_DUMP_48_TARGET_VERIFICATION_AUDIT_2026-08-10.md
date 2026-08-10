# 1 Коринфянам 11:2–16 — verification audit агентского dump

**Дата:** 2026-08-10  
**Статус:** `48-TARGET-INDEPENDENT-VERIFICATION / RESEARCH-ONLY / FAIL-CLOSED / PUBLICATION-HOLD`

## 0. Задача и правило этого прохода

Проверен пользовательский agent-dump с множеством параллельных AI-поисков по 1 Кор 11:2–16. Dump используется только как **discovery feed**, а не как authority.

```text
AGENT_DUMP = DISCOVERY_ONLY
AGENT_PARAPHRASE != AUTHOR_POSITION
SECONDARY_QUOTE != CURRENT_EDITION_PAGE
RECENCY != AUTHORITY
NO_UPDATE_IF_NO_REAL_DELTA = true
```

Было проверено **48 независимых verification targets**. Повторные зеркала и дубли одного источника в счётчик не добавлялись.

Главный итог:

```text
CORE_GRADE_REVERSALS = 0
USEFUL_LOCATOR_UPDATES = 2
USEFUL_SOURCE_STATUS_UPDATES = 3
AGENT_OVERSTATEMENTS_BLOCKED = 8+
```

То есть этот проход **не создаёт новый экзегетический синтез**. Он укрепляет source hygiene и исправляет только реально полезные дельты.

---

# 1. Самые важные результаты

## 1.1 Fee Revised 2014: агентский конфликт разрешён

В dump встречались взаимоисключающие утверждения: в одной линии Fee представлен как сторонник внешнего покрытия, в другой — как сторонник проблемы распущенных волос/причёски.

Проверка revised edition через Eerdmans + две академические рецензии показывает:

- издание действительно revised, 2014;
- Fee сохраняет `κεφαλή` как **source / source of life / origin**;
- по 11:4–7 он **снова выбирает традиционное внешнее покрытие**, а не hair-only;
- revised edition добавляет bibliographic addendum по проблеме veiling women на **pp.565–567**;
- рецензенты отмечают, что основные выводы первого издания существенно не изменились.

Следовательно:

```text
FEE_2014_HAIR_ONLY_AS_PRIMARY_POSITION = REJECTED
FEE_2014_EXTERNAL_COVERING = VERIFIED_SECONDARY_CURRENT_EDITION_CONTROL
FEE_2014_KEPHALE_SOURCE = VERIFIED_SECONDARY_CURRENT_EDITION_CONTROL
FEE_2014_VEILING_ADDENDUM = PP_565_567
```

Это **не** снимает P0 `HOLD_FULL_SECTION`: нужен полный current-edition section + notes, но агентская характеристика Fee как hair-only больше не допускается.

## 1.2 Garland 2025: подтверждён точный диапазон, но не агентские подробности

Официальный Baker excerpt второго издания прямо даёт TOC:

```text
VII. Headdress in Public Worship (11:2–16) = p.468
VIII. Divisions at the Lord's Supper (11:17–34) = p.494
```

Поэтому текущий P0 locator можно сузить до:

```text
GARLAND_2025_1COR11_2_16 = PP_468_493 + NOTES
```

Но открытый официальный excerpt **не содержит сам раздел 468–493**. Поэтому следующие формулы из agent-dump не принимаются как позиция Garland-2025 без direct section read:

- что он в 2025 точно идентифицирует предмет как `palla/stola`;
- что снятие покрытия почти равносильно публичному объявлению себя незамужней;
- что он делает конкретную юридическую конструкцию «защиты» женщины;
- что его 2025-формулировка `κεφαλή` точно совпадает с пересказами первого издания;
- что его точная версия ангелов в 2025 уже верифицирована;
- что Callon 2024 может свидетельствовать о тексте издания Garland 2025.

Callon опубликована в 2024 году и, следовательно, её ссылки на Garland не могут служить direct evidence содержания второго издания 2025.

```text
GARLAND_2025_TOC_LOCATOR = A_OFFICIAL
GARLAND_2025_DETAILED_11_2_16_POSITION = HOLD_DIRECT_SECTION
GARLAND_2003_TO_2025_CONTINUITY = DO_NOT_ASSUME
```

## 1.3 Ciampa/Rosner: агентский active-exousia consensus переоценён

Denver Journal review Craig Blomberg действительно характеризует их модель как **soft hierarchicalism** и подтверждает:

- внешний covering вероятнее hair-only;
- вопрос связан с sexual/moral propriety;
- женщины реально интегрированы в worship context.

Но по v10 рецензент специально **возражает авторам** за добавление `sign of` перед authority, поскольку другие NT употребления `ἐξουσία + ἔχειν + ἐπί` обычно выражают exercise/control.

Следовательно agent-dump нельзя использовать для утверждения:

> «Ciampa/Rosner сами ясно принимают active authority-over-her-own-head reading».

Более точная запись:

```text
CIAMPA_ROSNER_EXTERNAL_COVERING = B_HIGH_CURRENT_COMMENTARY_CONTROL
CIAMPA_ROSNER_SOFT_HIERARCHICALISM = VERIFIED_REVIEW_CHARACTERIZATION
CIAMPA_ROSNER_ADD_SIGN_OF_EXOUSIA = VERIFIED_REVIEW_REPORT
BLOMBERG_OBJECTS_TO_SIGN_OF = VERIFIED
CIAMPA_ROSNER_ACTIVE_EXOUSIA_AS_SETTLED_AUTHOR_POSITION = REJECTED_OVERSTATEMENT
```

Это усиливает уже существующий проектный guardrail: active grammatical/semantic pull принадлежит прежде всего самому греческому синтаксису и независимым controls, а не предполагаемому «консенсусу четырёх комментариев».

## 1.4 Stuckenbruck 2001 — действительно полезный источник, но не grade changer

Проверены Durham repository и официальный Stone-Campbell Journal abstract.

Источник реальный, peer reviewed:

- Loren T. Stuckenbruck, “Why Should Women Cover Their Heads Because of the Angels? (1 Corinthians 11:10),” *Stone-Campbell Journal* 4.2 (2001): 205–234.

Официальный abstract важнее агентских пересказов. Он говорит, что Павел в 11:2–16 ведёт переговоры между theological ideals и assumptions о sexuality людей/ангелов; инструкции связаны с ordering of the cosmos; поэтому для автора **менее важно жёстко решить good vs bad angels**.

Это полезно как adversarial pressure на слишком простую дихотомию, но не отменяет primary-corpus результата проекта:

```text
HEAVENLY_HOLY_ANGELS_REFERENT = B_HIGH_LEADING
WATCHERS = C_SERIOUS_ALTERNATIVE
EXACT_ANGELIC_FUNCTION = B_C
```

Stuckenbruck добавляется как сильный **status-quaestionis / mixed-cosmic-order control**, но core grade не меняется.

## 1.5 Edsall и Kendrick: существование подтверждено; agent-specific details не переоценивать

### Edsall

Официальный JGRChJ abstract подтверждает:

- статья существует;
- она входит прямо в hair-vs-covering debate;
- переоценивает аргумент через Greco-Roman costume;
- видит проблему social and sexual propriety;
- Павел пытается совместить expected propriety и своё учение об equality in Christ.

Но из доступного official abstract **не следует автоматически** подробный agent claim, что именно Edsall доказывает конкретный перевод v16 или что `συνήθεια ≠ παράδοσις` само по себе делает норму «не доктриной».

```text
EDSALL_COSTUME_PROPRIETY = VERIFIED
EDSALL_V16_OPTIONALITY_CLAIM = NOT_PROMOTED
```

### Kendrick

SAGE подтверждает статью W. Gerald Kendrick, *The Bible Translator* 46.3 (1995), pp.336–343. Открытый неофициальный PDF-route в текущем harness закрыт антиботом, поэтому подробные цитаты из agent-dump не promoted без direct page read.

```text
KENDRICK_ARTICLE_EXISTENCE = A_BIBLIOGRAPHIC
KENDRICK_DETAILED_QUOTE_PROMOTION = HOLD_DIRECT_TEXT
```

---

# 2. 48-target verification ledger

Легенда:

- `ACCEPT` — источник/утверждение проверено и допустимо использовать;
- `ACCEPT_LIMITED` — проверен только конкретный слой;
- `NO_CHANGE` — уже правильно учтено в Research;
- `HOLD` — источник существует, но agent-specific claim требует direct text/current edition;
- `REJECT_AGENT_OVERCLAIM` — агент пошёл дальше источника.

| ID | Target | Что проверялось | Verdict / действие |
|---|---|---|---|
| V01 | Fee, Eerdmans official revised-edition page | edition/date/1044 pages/revision scope | `ACCEPT`; current edition confirmed |
| V02 | DTS Voice review of Fee Revised | revision motive; conclusions largely stable; kephale source pp.554–555 | `ACCEPT` |
| V03 | Denver Journal review of Fee Revised | current-edition position; external covering; source/origin | `ACCEPT`; blocks hair-only misattribution |
| V04 | Reading Acts review of Fee Revised | bibliography/addendum pp.565–567 | `ACCEPT_LIMITED`; locator promoted |
| V05 | Google Books Fee Revised | edition metadata/current pagination environment | `ACCEPT_LIMITED` |
| V06 | Thiselton NIGTC, Eerdmans official | 2000 / NIGTC / 1492 pages | `ACCEPT`; P0 unchanged |
| V07 | Thiselton Shorter, Eerdmans official | publisher says shorter draws on NIGTC exegesis | `ACCEPT_LIMITED`; triangulation only |
| V08 | Ciampa/Rosner, Eerdmans official | 2010 / PNTC / 990 pages | `ACCEPT` |
| V09 | Blomberg Denver review C/R | soft hierarchicalism, external covering, propriety, v10 “sign of” issue | `ACCEPT`; agent active-consensus overclaim rejected |
| V10 | Roy Ciampa interview | glory/honor/shame; Roman social significance; public worship | `ACCEPT_LIMITED`; macro-thesis only |
| V11 | Garland 2025 Baker official excerpt | edition + TOC | `ACCEPT`; 11:2–16 pp.468–493 |
| V12 | Garland 2025 Baker publisher metadata | second edition/current scholarship update | `ACCEPT`; no detailed section claims inferred |
| V13 | Callon, HTR 2024 | no consensus wives/all women; free(d) wives proposal | `NO_CHANGE`; already integrated |
| V14 | Callon full-text literature section | majority textile presupposition; palla/social-status argument | `NO_CHANGE`; model remains B/C serious |
| V15 | Callon citation to Garland | which Garland edition it can evidence | `REJECT_AGENT_OVERCLAIM`; 2024 cannot verify 2025 text |
| V16 | Massey, NTS 2007 | `κατακαλύπτω` / `κατὰ κεφαλῆς` and textile thesis | `NO_CHANGE`; strongly supports material covering |
| V17 | Edsall, JGRChJ 2013 | costume/social-sexual propriety frame | `ACCEPT`; no v16 overreach |
| V18 | Massey, Novum Testamentum 2011 | hair glory/natural covering compatible with veiling | `NO_CHANGE`; supports analogy distinction |
| V19 | Massey, JBL 2018 | male veiling; material covering wording | `NO_CHANGE`; Roman/v4 layer already calibrated |
| V20 | Gill, Tyndale Bulletin 1990 | Roman portraiture and covered male ritual imagery | `NO_CHANGE`; primary-context layer already integrated |
| V21 | Finney, JSNT 2010 | honor/status reconstruction | `NO_CHANGE`; exact local trigger remains reconstruction |
| V22 | Oster, NTS 1988 | Roman male ritual head covering/capite velato | `NO_CHANGE`; background A, trigger not A |
| V23 | Bruce Winter, *Roman Wives* ch.5 | unveiled wives/social convention reconstruction | `NO_CHANGE`; useful but not universal rule |
| V24 | Payne hairstyle line | arranged/loose hair and sexed presentation alternative | `NO_CHANGE`; hair-only remains C serious |
| V25 | Murphy-O’Connor, “Sex and Logic” | no-veiling / sexual-role reconstruction | `NO_CHANGE`; D/C-low to C edge model |
| V26 | Murphy-O’Connor, “Once Again” | woman controls head; human-messenger angels | `NO_CHANGE`; messenger model remains low |
| V27 | Murphy-O’Connor critique of interpolation | direct-Pauline defense against removal | `NO_CHANGE`; 11:3b–15 interpolation stays D/C-low |
| V28 | Troy W. Martin, JBL 2004 | physiology/testicle proposal exists | `NO_CHANGE`; proposal not lexical default |
| V29 | Mark Goodacre, JBL 2011 | criticism of `περιβόλαιον=testicle` | `NO_CHANGE`; D/C-low retained |
| V30 | Stuckenbruck, Durham repository | bibliographic/authorship/peer-review | `ACCEPT`; source newly pinned explicitly |
| V31 | Stuckenbruck, Stone-Campbell Journal abstract | cosmic ordering; good/bad angel dichotomy de-emphasized | `ACCEPT_LIMITED`; no core grade change |
| V32 | Fitzmyer, NTS 1957 | Qumran angelology supports a common angel interpretation | `NO_CHANGE`; holy/heavenly family remains leading |
| V33 | HTR “A Qumran Parallel to Paul” | holy angels with assembly; common Jewish background caution | `NO_CHANGE`; Qumran influence itself not required |
| V34 | Kendrick, *Bible Translator* 1995 | article existence/pages | `ACCEPT_BIBLIOGRAPHIC`; detailed agent quotes remain HOLD |
| V35 | Hooker, NTS 1964 | classic v10 authority article metadata | `NO_CHANGE`; direct full-text still desired for quotation promotion |
| V36 | Fitzmyer, NTS 1989 `κεφαλή` | serious authority/headship lexical argument exists | `NO_CHANGE`; supports possibility not exclusivity |
| V37 | Janelle Peters, Mohr Siebeck 2025 | citizen-body/body-control model | `NO_CHANGE`; already C serious current model |
| V38 | Peters earlier peer-reviewed work | creation/angels/interdependence pressure | `NO_CHANGE`; already integrated |
| V39 | Nõmmik, Wipf & Stock 2025 | capite-velato / ritual-uniformity model | `NO_CHANGE`; already separately adversarially audited |
| V40 | Nõmmik, Google Books TOC/sample | structure and open-route details | `NO_CHANGE`; no promotion without full-text bytes |
| V41 | Salés 2024 quotation/refutation proposal | current published long-quotation model | `NO_CHANGE`; recency does not remove hidden-speaker burden |
| V42 | Castilho da Costa linguistic quotation proposal | vv4–9 Corinthian-view model exists | `NO_CHANGE`; remains D/C-low edge node |
| V43 | Hamplová 2025 thesis | current reception/bibliographic control | `NO_CHANGE`; not peer to P0 technical commentaries |
| V44 | Gundry-Volf / Westfall debate controls | creation/gender alternatives remain serious literature | `NO_CHANGE`; no consensus shortcut |
| V45 | GNT6 official publisher | current published Greek base / future NA29 text identity | `NO_CHANGE`; PR #179 now merged |
| V46 | NA29 official publisher | NA29 not yet published; release 2027-02-28 | `NO_CHANGE`; blocks agent edition inflation |
| V47 | current textual-commentary route for GNT6 apparatus | apparatus is separate from text identity | `NO_CHANGE`; future apparatus ledger remains separate task |
| V48 | Robertson-Plummer / classic public commentary control | historical reception of covering/v10 ambiguity | `NO_CHANGE`; history does not override current lexical audit |

---

# 3. Agent-dump claims explicitly NOT promoted

The following recurring claims in the dump are useful as search leads only:

```text
GARLAND_2025_EXACT_PALLA_STOLA_POSITION = HOLD
GARLAND_2025_EXACT_ANGEL_MODEL = HOLD
GARLAND_2025_EXACT_KEPHALE_WORDING = HOLD
GARLAND_2025_ROMAN_LEGAL_PROTECTION_ARGUMENT = HOLD
FEE_2014_HAIR_ONLY = REJECTED
CIAMPA_ROSNER_ACTIVE_EXOUSIA_CONSENSUS = REJECTED_OVERSTATEMENT
THISELTON_UNIFORM_OF_MINISTRY_METAPHOR = HOLD
THISELTON_ISAIAH_6_AS_EXACT_ANGEL_SOLUTION = HOLD
EDSALL_SYNĒTHEIA_MEANS_NON_DOCTRINAL_OPTIONALITY = REJECTED_OVERREACH
KENDRICK_EXACT_QUOTES_FROM_PROXY_PDF = HOLD
UNVEILED_WOMAN_EQUALS_PROSTITUTE = REJECTED_UNIVERSALIZATION
GARLAND_2003_POSITION_EQUALS_GARLAND_2025_POSITION = DO_NOT_ASSUME
```

Some of these may ultimately prove close to an author’s actual position. The point is narrower: **the agent dump did not verify them to project standard**.

---

# 4. Useful deltas actually promoted

Only the following changes justify repository update in this pass:

1. **Garland 2025 exact current-section locator**
   - `11:2–16 = pp.468–493`;
   - full section + notes remains P0 HOLD.

2. **Fee Revised exact addendum locator**
   - veiling-women bibliographic addendum: `pp.565–567`;
   - current full section still required for direct quotation/detail closure.

3. **Fee hair-only misattribution blocked**
   - current-edition academic review reports Fee again opts for external covering.

4. **Ciampa/Rosner exousia characterization tightened**
   - do not cite them as proof of a settled active-own-authority consensus;
   - Blomberg reports their `sign of authority` wording and explicitly objects to the supplied `sign of`.

5. **Stuckenbruck 2001 explicitly pinned**
   - strong status-quaestionis source for angels/cosmic order;
   - does not change current angel grades.

6. **Garland-2025 continuity firewall strengthened**
   - pre-2025 sources and first-edition summaries cannot be silently attributed to second edition.

No other dump material crossed the threshold for a Research update.

---

# 5. Current synthesis after verification

No core reversal:

```text
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
KEPHALE_HEADSHIP_AUTHORITY = B_LEADING
KEPHALE_SOURCE_ONLY = C_VIABLE
WIVES_VS_ALL_WOMEN = OPEN_B_C
EXOUSIA_WOMAN_SUBJECT = A
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH
EXOUSIA_REFERENT = B_C
HEAVENLY_HOLY_ANGELS_REFERENT = B_HIGH_LEADING
ANGELS_AS_COSMIC_WITNESSES/PRESENT_ASSEMBLY = B_LEADING
EXACT_ANGELIC_FUNCTION = B_C
WATCHERS = C_SERIOUS_ALTERNATIVE
ROMAN_CAPITE_VELATO_BACKGROUND = A
V4_EXACT_CAPITE_VELATO = B_C
PHYSIS_SEXED_NATURALIZED_PROPRIETY = B_HIGH_LEADING
V16_TRANSLOCAL_CHURCH_APPEAL = A
V16_EXACT_CUSTOM_REFERENT = B_C
```

---

# 6. P0 acquisition after this pass

```text
1. Thiselton NIGTC 2000
   pp.800–847 + notes

2. Fee NICNT Revised 2014
   full 11:2–16 section, approx pp.542–586
   explicitly include addendum pp.565–567 + notes

3. Garland BECNT 2nd ed. 2025
   pp.468–493 + notes

4. Ciampa/Rosner PNTC 2010
   pp.503–540 + notes
```

No user request should be made while agent-access routes remain reasonably available.

---

# 7. Publication / Product boundary

```text
DO_NOT_REQUEST_FROM_USER_IF_AGENT_CAN_ACCESS = true
PRODUCT_WRITE = false
UI_IMPLEMENTATION = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
DIRECT_QUOTE_PROMOTION = false unless direct locator/object verified
```
