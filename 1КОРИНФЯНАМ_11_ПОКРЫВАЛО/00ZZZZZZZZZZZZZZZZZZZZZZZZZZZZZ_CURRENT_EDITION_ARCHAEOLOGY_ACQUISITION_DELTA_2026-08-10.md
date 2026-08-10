# 1 Коринфянам 11:2–16 — current-edition / archaeology acquisition delta

**Дата:** 2026-08-10  
**Статус:** `CURRENT-EDITION-RADAR / ARCHAEOLOGY-CONTROL / FAIL-CLOSED / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Задача

Этот проход не пытается увеличить число ссылок. Он проверяет, появились ли после уже учтённых Callon 2024 / Nõmmik 2024–2025 новые комментарии и археологические синтезы, которые должны войти в P0/P1 acquisition queue.

Правила:

```text
NEW_BOOK_EXISTS != ITS_1COR11_POSITION_VERIFIED
CURRENT_EDITION != AUTOMATICALLY_BETTER_ARGUMENT
ARCHAEOLOGY_OF_CORINTH != SPECIFIC_1COR11_SUPPORT
PREVIEW_METADATA != QUOTE_SAFE_SECTION
RECENCY != AUTHORITY
```

---

# 1. David I. Starling 2025 — новый current-edition commentary target

## 1.1 Прямая библиографическая верификация

Embedded preview издательской цифровой экосистемы прямо идентифицирует:

> David I. Starling, *1 Corinthians*, Evangelical Biblical Theology Commentary, 2025.

Copyright-page preview также фиксирует:

- серия: Evangelical Biblical Theology Commentary;
- автор: David I. Starling;
- copyright 2025;
- Lexham Academic / Lexham Press;
- general editors: T. Desmond Alexander, Thomas R. Schreiner, Andreas J. Köstenberger.

Verified route:

- https://biblia.com/api/plugins/embeddedpreview?historybuttons=false&layout=minimal&navigationbox=false&resourceName=LLS%3AEBTC67CO1&sharebutton=false

## 1.2 Что НЕ удалось закрыть

В доступном preview/search path не извлечён сам комментарий к 1 Cor 11:2–16 и не получены его точные страницы/формулировки по:

- `κεφαλή`;
- external covering vs hair;
- `ἐξουσία` v10;
- angels;
- `φύσις`;
- v16.

Поэтому:

```text
STARLING_2025_BOOK = VERIFIED_CURRENT_COMMENTARY
STARLING_2025_1COR11_POSITION = CONTENT_HOLD
STARLING_2025_DIRECT_QUOTE = FORBIDDEN_UNTIL_SECTION_ACQUIRED
STARLING_2025 = P0_P1_CURRENT_EDITION_TARGET
```

Не выводить позицию автора из состава редакторов серии, конфессиональной среды или чужих рецензий.

---

# 2. David A. deSilva 2025 — новый current archaeological synthesis

## 2.1 Прямая верификация

Baker Academic каталог 2025 фиксирует:

> David A. deSilva, *Archaeology and the Ministry of Paul: A Visual Guide*, Baker Academic, April 2025, 320 pp., ISBN 9781540960955.

Издатель указывает более 250 полноцветных фотографий sites/artifacts и задачу использовать археологию для реконструкции реальных мест и ситуаций Павлова служения.

Official routes:

- https://bakeracademic.com/products/9781540960955_archaeology-and-the-ministry-of-paul
- https://bakeracademic.com/collections/bible-2025-new-releases

Digital/book-preview routes also verify the object:

- https://www.logos.com/product/374875/archaeology-and-the-ministry-of-paul-a-visual-guide
- https://www.everand.com/book/838442061/Archaeology-and-the-Ministry-of-Paul-Archaeology-and-the-New-Testament-A-Visual-Guide

## 2.2 Roman Corinth chapter

Published TOC/review control places the chapter:

```text
ROMAN_CORINTH = pp.126–156
```

This makes deSilva 2025 a high-value **current Corinth archaeology/context acquisition target**.

But inspected preview/search did not establish that this chapter specifically discusses:

- 1 Cor 11:2–16;
- S-1116 Augustus `capite velato`;
- S-1088;
- Julian Basilica head-covering iconography.

Therefore:

```text
DESILVA_2025_ROMAN_CORINTH_CHAPTER = VERIFIED
DESILVA_2025_1COR11_SPECIFIC_USE = LOCATOR_HOLD
DESILVA_2025_S1116_SPECIFIC_USE = LOCATOR_HOLD
DESILVA_2025 = P1_CURRENT_VISUAL_ARCHAEOLOGY_CONTROL
```

Do not cite deSilva as confirmation of the exact v4 `capite velato` reading until the relevant pages are directly read.

---

# 3. Cynthia L. Thompson 1988 — direct archaeology literature owner now pinned

## 3.1 Direct publisher control

University of Chicago / ASOR journal page directly verifies:

> Cynthia L. Thompson, “Hairstyles, Head-Coverings, and St. Paul: Portraits from Roman Corinth,” *The Biblical Archaeologist* 51.2 (June 1988): 99–115. DOI `10.2307/3210030`.

Direct route:

- https://www.journals.uchicago.edu/doi/10.2307/3210030

The official abstract explicitly says that discussions of 1 Cor 11:2–16 had paid too little attention to relevant archaeological evidence and that material unearthed over the preceding decades could clarify the historical context of Paul and Corinth.

Thus:

```text
THOMPSON_1988 = VERIFIED_DIRECT_ARCHAEOLOGY_B1
THOMPSON_SCOPE = ROMAN_CORINTH_PORTRAITURE_AND_1COR11
```

## 3.2 Relation to Gill/Oster and current assemblage control

David W. J. Gill’s 1990 article explicitly responds to Thompson and insists the Corinthian correspondence be read against a Roman-colonial, not merely generic Greek, backdrop.

Direct open-fulltext route:

- https://www.tyndalebulletin.org/article/30525-the-importance-of-roman-portraiture-for-head-coverings-in-1-corinthians-11-2-16

The current archaeology chain should therefore be represented as:

```text
THOMPSON_1988_LOCAL_PORTRAITS
-> OSTER_1988_1992_ROMAN_RITUAL/ARCHAEOLOGY
-> GILL_1990_ROMAN_PORTRAITURE_RESPONSE
-> ASCSA_CORINTH_XXII_2022_COMPLETE_JULIAN_BASILICA_ASSEMBLAGE
-> DESILVA_2025_CURRENT_ROMAN_CORINTH_VISUAL_SYNTHESIS_TARGET
```

This is methodologically stronger than citing a single statue photograph as a proof-text.

---

# 4. Current archaeology implication — no grade inflation

The expanded archaeology chain strongly supports the already-current minimum:

```text
ROMAN_CAPITE_VELATO_BACKGROUND = A
CORINTH_LOCAL_ROMAN_ICONOGRAPHIC_BACKGROUND = A2_STRONG
```

It does **not** newly prove:

```text
V4_EXACT_CAPITE_VELATO = A
CHRISTIAN_MEN_WERE_IMITATING_IMPERIAL_CULT = true
EXACT_CORINTH_TRIGGER = solved
```

Therefore current grades remain:

```text
V4_EXACT_CAPITE_VELATO = B_C
EXACT_CORINTH_TRIGGER = RECONSTRUCTION_LAYER
```

---

# 5. Current-edition acquisition map after this pass

## P0 direct commentary sections

```text
Thiselton NIGTC 2000: pp.800–847 + notes = HOLD
Fee NICNT Revised 2014: approx pp.542–586 + notes/addendum = HOLD
Garland BECNT 2nd ed. 2025: pp.468–493 + notes = HOLD
Ciampa/Rosner PNTC 2010: pp.503–540 + notes = DETAIL_HOLD
Starling EBTC 2025: exact 1 Cor 11:2–16 section = NEW_CONTENT_HOLD
```

## P1 archaeology/context

```text
Nõmmik DTH 9 full DiVA object = OFFICIAL_ROUTE_EXISTS / RUNTIME_HOLD
ASCSA Corinth XXII 2022 = CURRENT_ASSEMBLAGE_CONTROL
Thompson 1988 = DIRECT_LOCAL_PORTRAITURE_CONTROL
Gill 1990 = DIRECT_OPEN_ROMAN_PORTRAITURE_CONTROL
deSilva 2025 Roman Corinth pp.126–156 = CURRENT_SYNTHESIS_TARGET / SPECIFIC_1COR11_LOCATOR_HOLD
```

---

# 6. Search saturation rule

The 2025–2026 search surface contains many sermons, blog series, application essays and student projects. They are useful only if they lead to primary evidence or new specialist bibliography.

Do not promote merely because recently published:

```text
2025_2026_BLOG = NOT_CURRENT_SCHOLARSHIP_BY_DATE_ALONE
CURRENT_THESIS = CONTEXTUAL_RECEPTION_UNLESS_ARGUMENT_ADDS_PRIMARY_CONTROL
CURRENT_COMMENTARY = CONTENT_HOLD_UNTIL_RELEVANT_SECTION_READ
```

Callon 2024 remains the most consequential recent peer-reviewed article directly changing a live scope question in the current corpus. Nõmmik remains a major current monograph/reconstruction. Starling/deSilva are newly added **acquisition targets**, not pre-decided evidence for existing grades.

---

# 7. Result

```text
CORE_GRADE_REVERSALS = 0
NEW_CURRENT_COMMENTARY_TARGET = STARLING_2025
NEW_CURRENT_ARCHAEOLOGY_TARGET = DESILVA_2025_ROMAN_CORINTH_126_156
THOMPSON_1988_DIRECT_PUBLISHER_CONTROL = CLOSED
P0_DIRECT_TEXT_HOLDS = RETAINED
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
