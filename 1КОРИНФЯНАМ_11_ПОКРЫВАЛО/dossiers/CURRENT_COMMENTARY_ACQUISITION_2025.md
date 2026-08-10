# 1 Коринфянам 11:2–16 — current commentary acquisition 2025

**Статус:** `EVERGREEN-DOSSIER / CURRENT-COMMENTARIES / MULTILINGUAL-ACQUISITION / PAGINATION-CONTROL / TRANSPORT-LEDGER / RESEARCH-ONLY / PUBLICATION-HOLD`  
**Последнее обновление:** 2026-08-11

## 0. Authority rule

This dossier owns acquisition/transport state for the current commentary targets and records cross-target access lanes when doing so prevents repeated dead-end searching.

Primary current targets:
- Mark Reasoner, *1 Corinthians* (Brill, 2025);
- Michael J. Gorman, *1 Corinthians* (Eerdmans, 2025);
- David I. Starling, *1 Corinthians* (Lexham Academic / EBTC, 2025).

Cross-target transport controls also include Garland 2025, Fee Revised 2014, Thiselton 2000, Ciampa/Rosner 2010 and newly discovered translated/licensed routes relevant to the same 1 Cor 11 acquisition problem.

```text
CURRENT_BOOK_EXISTS != 1COR11_POSITION_VERIFIED
PUBLISHER_TOC != CHAPTER_BODY
SEARCH_SNIPPET != QUOTE_SAFE_TEXT
PAGINATION_PLAUSIBLE != QUOTE_AUTHENTICATED
PREVIEW_EXISTS != TARGET_SECTION_EXPOSED
PREVIEW_NO_MATCH != BOOK_HAS_NO_SUCH_DISCUSSION
RECENCY != AUTHORITY
TERMINAL_EXTERNAL_ACCESS_HOLD != CLAIM_REFUTED
TERMINAL_EXTERNAL_ACCESS_HOLD = STOP_REPEATING_THE_SAME_TESTED_ROUTE
```

## 0.1 Multilingual acquisition rule — ACTIVE 2026-08-11

The previous English-first sweep found real terminal holds, but the Fee and Winter discoveries show that an English-route terminal state is not enough to close discovery globally.

```text
ENGLISH_PUBLIC_ROUTE_EXHAUSTED != MULTILINGUAL_ROUTE_EXHAUSTED
LANGUAGE_OF_ACCESS != SOURCE_EDITION
LANGUAGE != EVIDENCE_GRADE
PUBLISHED_TRANSLATION_OF_VERIFIED_TARGET_EDITION = AUTHOR_POSITION_BODY_CAPABLE
PUBLISHED_TRANSLATION_WORDING != ORIGINAL_LANGUAGE_QUOTE
TRANSLATION_PAGINATION != ORIGINAL_PAGINATION
TRANSLATION_OF_EDITION_1 != EDITION_2_BODY
MACHINE_TRANSLATED_WEBPAGE != PUBLISHED_TRANSLATION
LOCALIZED_OFFICIAL_SAMPLE = AUTHORIZED_ACCESS_ROUTE
REGIONAL_LIBRARY_BORROW = LAWFUL_INSTITUTIONAL_OR_LICENSED_ROUTE
```

A published translation can close the author's substantive position for the edition it actually translates, provided edition identity and the target body are directly verified. It cannot be cited as verbatim English wording and it cannot transfer pagination across editions/languages.

### Search lanes

Every high-value terminal commentary now receives a bounded multilingual reopen pass using:

```text
SPANISH = muestra | vista previa | edición revisada | texto completo | biblioteca | préstamo
PORTUGUESE = amostra | trecho | edição revisada | texto completo | biblioteca | empréstimo
GERMAN = Leseprobe | Volltext | Auflage | Bibliothek | Fernleihe
FRENCH = extrait | aperçu | texte intégral | édition | bibliothèque
ITALIAN = estratto | anteprima | testo completo | edizione | biblioteca
POLISH = fragment | podgląd | pełny tekst | wydanie | biblioteka
CHINESE = 全文 | 试读 | 修订版 | 图书馆
```

Query construction must combine at least two of:
1. author;
2. original title;
3. translated/local biblical-book title;
4. ISBN/DOI/resource ID;
5. local access term;
6. local publisher/library catalogue.

### Route order

```text
1. original publisher / translated publisher catalogue
2. official PDF sample / publisher “look inside” / Logos-Biblia language edition
3. licensed ebook sample: OverDrive/Libby, Perlego, Everand, VitalSource, RedShelf where lawful
4. regional university / national / theological library and institutional repository
5. Google Books only for metadata / TOC / locator navigation unless actual target pages render
6. quote author only after direct target body is visible
7. terminalize a LANGUAGE LANE only after its materially distinct lawful routes are tested
```

Do not infer a translation from a machine-translated retailer page. Do not infer edition continuity from matching title alone.

---

# 1. Mark Reasoner — Brill Exegetical Commentary Series 3 (2025)

Direct metadata:

```text
AUTHOR = Mark Reasoner
TITLE = 1 Corinthians
SERIES = Brill Exegetical Commentary Series 3
PRINT_PUBLICATION_DATE = 2025-09-08
EBOOK_ISBN = 9789004737044
PRINT_ISBN = 9789004737037
LENGTH = 732_pages
```

Corrected section map:

```text
7:1_40 = p277
8:1_11:1 = p321
11:2_16 = p432
11:17_34 = p452
12:1_14:40 = p476
15:1_58 = p590
16:1_24 = p638
REASONER_11_2_16_APPROX_SPAN = p432_451
```

Official chapter identity:

```text
Commentary 7 = Hair and Head Coverings in the Assembly (11:2–16)
```

English Brill/Google routes expose architecture, not readable pp.432–451.

```text
REASONER_OFFICIAL_CHAPTER_IDENTITY = CLOSED
REASONER_DIRECT_11_2_16_BODY = TERMINAL_EXTERNAL_ACCESS_HOLD_CURRENT_ENGLISH_ROUTES
REASONER_VEIL_HAIR_POSITION = NOT_DIRECTLY_VERIFIED
REASONER_KEPHALE_POSITION = NOT_DIRECTLY_VERIFIED
REASONER_EXOUSIA_POSITION = NOT_DIRECTLY_VERIFIED
REASONER_ANGELS_POSITION = NOT_DIRECTLY_VERIFIED
REASONER_PHYSIS_POSITION = NOT_DIRECTLY_VERIFIED
REASONER_V16_POSITION = NOT_DIRECTLY_VERIFIED
REASONER_MULTILINGUAL_REOPEN = ACTIVE_BOUNDED_SWEEP
```

Circulated p.434/p.444 wording remains unverified; p.343 cannot belong to 11:3 in this edition.

---

# 2. Michael J. Gorman — Eerdmans 2025

```text
TITLE = 1 Corinthians: A Theological, Pastoral, and Missional Commentary
PUBLICATION_DATE = 2025-03-06
EBOOK_ISBN = 9781467465748
HARDCOVER_ISBN = 9780802882660
LENGTH = 477_pages
```

English routes tested: Eerdmans object, Google Books limited preview, licensed OverDrive/Libby sample. Target section did not render.

```text
GORMAN_11_2_16_DIRECT_BODY = TERMINAL_EXTERNAL_ACCESS_HOLD_CURRENT_ENGLISH_ROUTES
GORMAN_VEIL_HAIR_POSITION = NOT_DIRECTLY_VERIFIED
GORMAN_KEPHALE_POSITION = NOT_DIRECTLY_VERIFIED
GORMAN_EXOUSIA_POSITION = NOT_DIRECTLY_VERIFIED
GORMAN_ANGELS_POSITION = NOT_DIRECTLY_VERIFIED
GORMAN_MULTILINGUAL_REOPEN = ACTIVE_BOUNDED_SWEEP
```

A first multilingual title/author pass on 2026-08-11 found no verified published Spanish/Portuguese edition of this 2025 commentary. This is a bounded search result, not a global nonexistence claim.

---

# 3. David I. Starling — EBTC 2025

Official Biblia resource establishes the book/series identity but accessible preview is front matter/contents only.

```text
AUTHOR = David_I_Starling
SERIES = Evangelical_Biblical_Theology_Commentary
YEAR = 2025
PUBLISHER = Lexham_Academic_Lexham_Press
STARLING_OFFICIAL_BIBLIA_PREVIEW = VERIFIED
STARLING_PREVIEW_TARGET_SECTION = NOT_EXPOSED
STARLING_2025_1COR11_POSITION = TERMINAL_EXTERNAL_ACCESS_HOLD_CURRENT_ENGLISH_ROUTES
STARLING_DIRECT_QUOTE = FORBIDDEN_UNTIL_SECTION_ACQUIRED
STARLING_MULTILINGUAL_REOPEN = ACTIVE_BOUNDED_SWEEP
```

A first Portuguese/Spanish author/title pass on 2026-08-11 did not locate a verified translated edition. Do not infer Starling’s view from the series or editors.

---

# 4. Cross-target transport ledger

## 4.1 Gordon D. Fee — Revised Edition 2014

Substantive owner:
- `00ZZZZZZZZZ_SOURCE_CARD_FEE_REVISED_2014_1COR11.md`

### English revised edition

```text
EERDMANS_LOGOS_RESOURCE = LLS:NICNT67CO1_2ED
PRINT_YEAR = 2014
PRINT_ISBN = 9780802871367
ENGLISH_REVISED_11_2_16 = pp542_586
ENGLISH_TARGET_BODY = TERMINAL_EXTERNAL_ACCESS_HOLD_CURRENT_ENGLISH_ROUTES
```

### Spanish revised-edition route — NEW

Official Logos/Tesoro Bíblico product:
- *La primera epístola a los Corintios: Nuevo Comentario Internacional del Nuevo Testamento (NCINT)*;
- Gordon D. Fee;
- Editorial Tesoro Bíblico;
- 2024;
- 1044 pages.

The publisher page explicitly states that this Spanish edition derives from the **revised English version published in 2014**.

```text
FEE_SPANISH_2024_TESORO_BIBLICO_EDITION_IDENTITY = CLOSED_DIRECT_OFFICIAL
FEE_SPANISH_2024_TRANSLATES_REVISED_2014 = CLOSED_DIRECT_OFFICIAL
FEE_SPANISH_2024_LOGOS_LOOK_INSIDE_ROUTE = VERIFIED_LICENSED_ROUTE
FEE_SPANISH_2024_TARGET_11_2_16_BODY = NOT_EXPOSED_CURRENT_PREVIEW
```

### Portuguese revised-edition route — NEW, direct official sample

Official Vida Nova / CLC product:
- *1 Coríntios: Comentário exegético*;
- ISBN `9788527509268`;
- 1168 pages;
- first Portuguese edition is explicitly based on the **second English edition of 2014**;
- Vida Nova lists edition year 2019.

The official downloadable sample is a 52-page PDF and directly exposes the revised-edition preface plus the localized table of contents.

Direct Portuguese revised map:

```text
MULHERES_E_HOMENS_NO_CULTO_11_2_16 = p616
CULTURA_VERGONHA_11_2_6 = p626
CRIACAO_11_7_12 = p645
DECORO_11_13_16 = p660
LORDS_SUPPER_11_17_34 = p668
```

The direct translated revised preface also confirms Fee's own reasons for revision: switch from the old NIV base to the updated 2011 NIV, removal of about twenty translation-related footnotes from the first edition, and integration of the greatly expanded technical literature.

```text
FEE_PORTUGUESE_2019_TRANSLATES_REVISED_2014 = CLOSED_DIRECT_OFFICIAL
FEE_PORTUGUESE_OFFICIAL_SAMPLE = CLOSED_DIRECT_PDF
FEE_PORTUGUESE_REVISED_PREFACE = CLOSED_DIRECT_BODY
FEE_PORTUGUESE_REVISED_TOC_AND_LOCAL_PAGINATION = CLOSED_DIRECT_BODY
FEE_PORTUGUESE_11_2_16_EXPOSITION_BODY = NOT_IN_52_PAGE_SAMPLE
```

### Fee 1987 edition firewall

The user-provided Nueva Creación Spanish PDF is a published translation of the **1987 first edition**, not 2014. It is now direct body for Fee 1987 and stored in Google Drive; provenance receipt:
- `data/1cor11-fee-1987-spanish-user-acquisition-2026-08-11.md`

```text
FEE_1987_FIRST_EDITION_DIRECT_BODY = CLOSED_DIRECT
FEE_1987_SPANISH_1994 != FEE_2014_REVISED_BODY
FEE_1987_PAGINATION != FEE_2014_PAGINATION
FEE_1987_WORDING != FEE_2014_WORDING_AUTOMATICALLY
```

Current revised-body target therefore remains open, but now has two new authorized language lanes rather than a globally terminal public-route state.

```text
FEE_2014_MULTILINGUAL_REOPEN = ACTIVE
FEE_2014_TARGET_EXPOSITION_BODY = STILL_NOT_DIRECTLY_ACQUIRED
```

## 4.2 Ciampa / Rosner 2010

```text
TITLE = The First Letter to the Corinthians
AUTHORS = Roy_E_Ciampa + Brian_S_Rosner
SERIES = PNTC
YEAR = 2010
PAGES = 990
CIAMPA_ROSNER_2010_PP503_540 = TERMINAL_EXTERNAL_ACCESS_HOLD_CURRENT_ENGLISH_ROUTES
```

A first Spanish/Portuguese title-author sweep on 2026-08-11 did not locate a verified published translation of this PNTC volume. Secondary translated citations and user-upload platforms do not count.

```text
CIAMPA_ROSNER_MULTILINGUAL_REOPEN = ACTIVE_BOUNDED_SWEEP
NO_TRANSLATION_FOUND_IN_FIRST_PASS != NO_TRANSLATION_EXISTS
```

## 4.3 Garland 2025 second edition

```text
AUTHOR = David_E_Garland
TITLE = 1_Corinthians
SERIES = BECNT
EDITION = 2
YEAR = 2025
PRINT_ISBN = 9781540962607
EBOOK_ISBN = 9781493451692
SECTION = VII. Headdress in Public Worship (11:2–16)
GARLAND_2025_PP468_493 = RETRACT_AS_UNVERIFIED_LOCATOR
GARLAND_2003_PP505_532 != GARLAND_2025_PAGINATION
GARLAND_2025_TARGET_BODY = TERMINAL_EXTERNAL_ACCESS_HOLD_CURRENT_ENGLISH_ROUTES
```

First Spanish/Portuguese pass on 2026-08-11 found other Spanish Garland works and unrelated 1 Corinthians translations, but **no verified translation of the 2025 BECNT second edition**. Do not collapse those objects.

```text
GARLAND_2025_MULTILINGUAL_REOPEN = ACTIVE_BOUNDED_SWEEP
```

## 4.4 Thiselton 2000

```text
THISELTON_2000_WORK = VERIFIED
THISELTON_2000_PP800_847 = TERMINAL_EXTERNAL_ACCESS_HOLD_CURRENT_ENGLISH_ROUTES
```

A first Spanish/Portuguese sweep returned translated bibliographic references, outlines and downstream quotations, but no verified published translation of the complete 2000 NIGTC volume. The shorter 2006/2011 commentary is a different object.

```text
THISELTON_2000_MULTILINGUAL_REOPEN = ACTIVE_BOUNDED_SWEEP
DOWNSTREAM_TRANSLATED_QUOTE != PUBLISHED_TRANSLATION_BODY
```

---

# 5. Newly reopened contextual target — Bruce W. Winter

The multilingual pass found a genuine publisher-authorized Portuguese translation of Winter's *After Paul Left Corinth*:

```text
PORTUGUESE_TITLE = Cristianismo e paganismo: A influência da cultura na igreja de Corinto
AUTHOR = Bruce_W_Winter
PUBLISHER = Vida_Nova
EDITION_YEAR = 2026
PRINT_ISBN = 9786559673933
EBOOK_ISBN = 9786559673926
ORIGINAL_TITLE = After Paul Left Corinth: The Influence of Secular Ethics and Social Change
```

Vida Nova exposes an official sample-PDF route. In the current runtime that PDF endpoint did not render, so sample existence is verified but body is not claimed.

A licensed Everand Portuguese preview directly exposes the translated table of contents, including:

```text
CH6 = Homens e esposas com véu e a contenciosidade cristã (1Coríntios 11.2-16)
SUB1 = O homem não deve cobrir a cabeça; [...] a mulher deve usar véu (11.7,10)
I = Homens de posição cobrem a cabeça
II = Novas esposas e o sinal da condição de casada
III = Reunião pública e os mensageiros
IV = Contenciosidade na igreja
```

English TOC controls locate the chapter at pp.121–141, with subsections beginning pp.121, 123, 133 and 138.

```text
WINTER_PORTUGUESE_2026_EDITION_IDENTITY = CLOSED_DIRECT_PUBLISHER
WINTER_PORTUGUESE_OFFICIAL_SAMPLE_ROUTE = VERIFIED_ROUTE / RUNTIME_RENDER_HOLD
WINTER_PORTUGUESE_LICENSED_TOC_PREVIEW = CLOSED_DIRECT_PREVIEW
WINTER_CH6_TARGET_BODY = NOT_YET_DIRECTLY_ACQUIRED
WINTER_MULTILINGUAL_REOPEN = ACTIVE
```

This is a discovery/access delta, not a new grade by itself.

---

# 6. German/native-language specialist lanes found in the same sweep

The new method also changes how non-English originals are handled: search the work in its original language first rather than translating everything into English search terms.

### Barbara Lumesberger-Loisl 2025

IxTheo directly identifies:
- `Kopftuchgebot für Christinnen?: Die „Verhüllung“ des Kopfes als Ausdruck der Geschlechterdifferenz (1 Kor 11,2-16)`;
- 2025;
- pp.295–303;
- ISBN `9783460252660`;
- German library availability / specialized interlibrary-loan route.

```text
LUMESBERGER_LOISL_NATIVE_GERMAN_METADATA = CLOSED
LUMESBERGER_LOISL_GERMAN_ILL_ROUTE = VERIFIED_INSTITUTIONAL_ROUTE
LUMESBERGER_LOISL_BODY = STILL_HOLD
```

### Marlis Gielen 1999

Native German title and article identity remain secure:
- `Beten und Prophezeien mit unverhülltem Kopf? ...`, ZNW 90.3–4 (1999), pp.220–249.

Current German search surfaced bibliographic/full-text-delivery services but no directly renderable publisher body in this runtime.

```text
GIELEN_NATIVE_GERMAN_SEARCH_LANE = TESTED
GIELEN_DIRECT_BODY = STILL_HOLD
```

### Jorunn Økland

Bloomsbury's official product has a `Look Inside` route and sells the PDF ebook; Perlego also lists a licensed PDF with chapter-level TOC.

```text
OKLAND_BLOOMSBURY_LOOK_INSIDE_ROUTE = VERIFIED
OKLAND_PERLEGO_LICENSED_PDF_ROUTE = VERIFIED
OKLAND_TARGET_CH4_7_BODY = NOT_DIRECTLY_ACQUIRED_CURRENT_RUNTIME
```

---

# 7. Queue semantics after multilingual reopening

The former sentence `CURRENT_COMMENTARY_ACTIVE_ACQUISITION_QUEUE = EMPTY_FOR_CURRENT_PUBLIC_ROUTES` was correct for the English/current routes actually tested on 2026-08-10, but it is too broad after new language routes were discovered.

Use this instead:

```text
ENGLISH_KNOWN_ROUTE_AUDIT = DISPOSITION_COMPLETE
MULTILINGUAL_REOPEN_SWEEP = ACTIVE
MULTILINGUAL_NEW_AUTHORIZED_ROUTES_FOUND = YES
FEE_2014_PT_ES = AUTHORIZED_REVISED_EDITION_ROUTES_FOUND / TARGET_EXPOSITION_NOT_YET_EXPOSED
WINTER_2001_PT_2026 = AUTHORIZED_TRANSLATION_ROUTE_FOUND / CH6_BODY_NOT_YET_EXPOSED
CURRENT_COMMENTARY_ACTIVE_ACQUISITION_QUEUE = ACTIVE_ONLY_FOR_MATERIALLY_NEW_LANGUAGE_OR_REGIONAL_ROUTES
REPEAT_EXHAUSTED_ENGLISH_PREVIEW_ROUTE = NO
```

A target returns to terminal status only after the newly discovered language/regional lane itself is exhausted or classified.

---

# 8. Audit lessons

```text
SEARCH_INDEX_STRIPPED_VERSE_LABEL != SAFE_MANUAL_MAPPING
CHAPTER_SEQUENCE_MUST_BE_RECONCILED_WITH_PUBLISHER_TOC
CURRENT_EDITION != POSITION_VERIFIED
PREVIEW_NO_MATCH != ABSENCE_FROM_BOOK
LICENSED_SAMPLE_ROUTE != TARGET_SECTION_READ
EDITION_1_PAGINATION != EDITION_2_PAGINATION_AUTOMATICALLY
TRANSLATION_PAGINATION != SOURCE_PAGINATION
PUBLISHED_TRANSLATION_BODY_CAN_VERIFY_AUTHOR_POSITION_FOR_THAT_EDITION
PUBLISHED_TRANSLATION_BODY_CANNOT_CREATE_AN_ORIGINAL_LANGUAGE_QUOTE
MACHINE_TRANSLATION != PUBLISHED_TRANSLATION
PAYWALL != PERMISSION_TO_USE_DOWNSTREAM_QUOTE_AS_PRIMARY
TERMINAL_ACCESS_HOLD != SUBSTANTIVE_DISCONFIRMATION
BOUNDED_LANGUAGE_SEARCH != GLOBAL_NONEXISTENCE
```

---

# 9. Result

```text
REASONER_2025 = VERIFIED_CURRENT_TECHNICAL_COMMENTARY / MULTILINGUAL_REOPEN_ACTIVE
GORMAN_2025 = VERIFIED_CURRENT_COMMENTARY / MULTILINGUAL_REOPEN_ACTIVE
STARLING_2025 = VERIFIED_CURRENT_COMMENTARY / MULTILINGUAL_REOPEN_ACTIVE
GARLAND_2025_2E = SECTION_IDENTITY_CLOSED / MULTILINGUAL_REOPEN_ACTIVE
THISELTON_2000 = WORK_AND_RANGE_CLOSED / MULTILINGUAL_REOPEN_ACTIVE
CIAMPA_ROSNER_2010 = WORK_AND_RANGE_CLOSED / MULTILINGUAL_REOPEN_ACTIVE

FEE_1987_SPANISH_1994 = CLOSED_DIRECT_BODY
FEE_2014_PORTUGUESE_2019 = AUTHORIZED_REVISED_TRANSLATION / PREFACE_AND_TOC_CLOSED_DIRECT / 11_2_16_BODY_NOT_EXPOSED
FEE_2014_SPANISH_2024 = AUTHORIZED_REVISED_TRANSLATION / LICENSED_PREVIEW_ROUTE / 11_2_16_BODY_NOT_EXPOSED
WINTER_PORTUGUESE_2026 = AUTHORIZED_TRANSLATION_ROUTE / CH6_TOC_CLOSED / BODY_NOT_EXPOSED

ENGLISH_KNOWN_ROUTE_AUDIT = COMPLETE
MULTILINGUAL_REOPEN_SWEEP = ACTIVE
CORE_GRADE_REVERSALS = 0
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
SITE_PUBLICATION = false
```