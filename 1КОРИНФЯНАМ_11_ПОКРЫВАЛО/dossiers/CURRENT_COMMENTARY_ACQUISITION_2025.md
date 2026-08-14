# 1 Коринфянам 11:2–16 — current commentary acquisition 2025

**Статус:** `EVERGREEN-DOSSIER / CURRENT-COMMENTARIES / MULTILINGUAL-ACQUISITION / REGIONAL-LIBRARY-ROUTES / PAGINATION-CONTROL / TRANSPORT-LEDGER / RESEARCH-ONLY / PUBLICATION-HOLD`  
**Последнее обновление:** 2026-08-14

## 0. Authority rule

This dossier owns acquisition/transport state for current commentary targets and records materially distinct translated, licensed and regional-library access lanes when doing so prevents repeated dead-end searching.

Primary current targets:
- Mark Reasoner, *1 Corinthians* (Brill, 2025);
- Michael J. Gorman, *1 Corinthians* (Eerdmans, 2025);
- David I. Starling, *1 Corinthians* (Lexham Academic / EBTC, 2025).

Cross-target controls also include Garland 2025, Fee Revised 2014, Thiselton 2000, Ciampa/Rosner 2010 and high-value contextual works whose access state can change through translation or regional catalogues.

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

## 0.1 Multilingual / regional acquisition protocol — KNOWN-ROUTE SWEEP DISPOSITIONED 2026-08-14

The English-first audit reached real route-level ceilings, and Fee/Winter plus later regional-catalog discoveries demonstrated that an English public-preview ceiling is not automatically a global acquisition ceiling. Those materially distinct language/regional routes have now themselves been tested and classified. They remain valuable provenance and human-access lanes, but they no longer constitute an active agent search queue.

```text
ENGLISH_KNOWN_ROUTE_AUDIT = DISPOSITION_COMPLETE
MULTILINGUAL_KNOWN_ROUTE_SWEEP = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
REGIONAL_KNOWN_ROUTE_SWEEP = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
CURRENT_KNOWN_PUBLIC_AGENT_QUEUE_EMPTY = true
NEW_USER_PROVIDED_BODY = REOPEN_TRIGGER
NEW_RENDERABLE_AUTHORIZED_ROUTE = REOPEN_TRIGGER
NEW_MATERIALLY_DISTINCT_SOURCE = REOPEN_TRIGGER
REPEATING_ALREADY_TESTED_ROUTE = NOT_REOPEN_TRIGGER
```

```text
ENGLISH_PUBLIC_ROUTE_EXHAUSTED != MULTILINGUAL_ROUTE_EXHAUSTED_IN_PRINCIPLE
ENGLISH_PUBLIC_ROUTE_EXHAUSTED != REGIONAL_LIBRARY_ROUTE_EXHAUSTED_IN_PRINCIPLE
LANGUAGE_OF_ACCESS != SOURCE_EDITION
LANGUAGE != EVIDENCE_GRADE
PUBLISHED_TRANSLATION_OF_VERIFIED_TARGET_EDITION = AUTHOR_POSITION_BODY_CAPABLE
PUBLISHED_TRANSLATION_WORDING != ORIGINAL_LANGUAGE_QUOTE
TRANSLATION_PAGINATION != ORIGINAL_PAGINATION
TRANSLATION_OF_EDITION_1 != EDITION_2_BODY
MACHINE_TRANSLATED_WEBPAGE != PUBLISHED_TRANSLATION
LOCALIZED_OFFICIAL_SAMPLE = AUTHORIZED_ACCESS_ROUTE
REGIONAL_LIBRARY_BORROW = LAWFUL_INSTITUTIONAL_OR_LICENSED_ROUTE
LIBRARY_HOLDING != BODY_READ
SUBITO_OR_ILL_ROUTE != BODY_READ
LICENSED_FULLTEXT_RECORD != RUNTIME_FULLTEXT_BODY
```

A published translation can close the author's substantive position for the edition it actually translates only after edition identity **and the target body** are directly verified. It cannot be cited as verbatim original-language wording and it cannot transfer pagination across editions/languages.

### Search lanes

When a genuinely new reopen trigger appears, use a bounded pass such as:

```text
SPANISH = muestra | vista previa | edición revisada | texto completo | biblioteca | préstamo
PORTUGUESE = amostra | trecho | edição revisada | texto completo | biblioteca | empréstimo
GERMAN = Leseprobe | Volltext | Auflage | Bibliothek | Fernleihe | Subito
FRENCH = extrait | aperçu | texte intégral | édition | bibliothèque | prêt
ITALIAN = estratto | anteprima | testo completo | edizione | biblioteca | prestito
POLISH = fragment | podgląd | pełny tekst | wydanie | biblioteka
CHINESE = 全文 | 试读 | 修订版 | 图书馆
JAPANESE = 図書 | 大学図書館 | 所蔵 | 試し読み
```

Query construction combines at least two of:
1. author;
2. original title;
3. translated/local biblical-book title;
4. ISBN/DOI/resource ID;
5. local access term;
6. local publisher/library catalogue.

### Route order

```text
1. original publisher / translated publisher catalogue
2. official PDF sample / publisher look-inside / Logos-Biblia language edition
3. licensed ebook sample: OverDrive/Libby, Perlego, Everand, VitalSource, RedShelf where lawful
4. regional university / national / theological library catalogue
5. institutional repository / author repository / OA disciplinary repository
6. ILL / Subito / licensed-fulltext record as an access route, not as body evidence
7. Google Books only for metadata / TOC / locator navigation unless actual target pages render
8. quote author only after direct target body is visible
9. terminalize a LANGUAGE/REGIONAL LANE after materially distinct lawful routes are tested
```

Do not infer a translation from a localized interface. A Spanish/Portuguese/German UI around an English book is still the English edition unless the bibliographic object says otherwise.

---

# 1. Mark Reasoner — Brill Exegetical Commentary Series 3 (2025)

Direct metadata:

```text
AUTHOR = Mark Reasoner
TITLE = 1 Corinthians
SERIES = Brill Exegetical Commentary Series 3
YEAR = 2025
EBOOK_ISBN = 9789004737044
PRINT_ISBN = 9789004737037
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
REASONER_11_2_16_APPROX_SPAN = pp432_451
```

Official chapter identity:

```text
Commentary 7 = Hair and Head Coverings in the Assembly (11:2–16)
```

English Brill/Google routes expose architecture, not readable pp.432–451.

### 1.1 German regional-library lane

IxTheo supplies a materially distinct route for the exact 2025 book:

```text
IXTHEO_RECORD = 1 Corinthians / Reasoner, Mark / Brill 2025
FORMAT = PRINT_BOOK
PHYSICAL_DESCRIPTION = XI_717_PAGES_IN_RECORD
ISBN = 9789004737037
HBZ_GATEWAY = AVAILABLE_ROUTE
FACHINFORMATIONSDIENSTE_ILL = AVAILABLE_ROUTE
SUBITO_DELIVERY = AVAILABLE_ROUTE
TABLE_OF_CONTENTS = LINKED
```

This is not target body in the current runtime; it is a verified institutional acquisition lane rather than body closure.

```text
REASONER_OFFICIAL_CHAPTER_IDENTITY = CLOSED
REASONER_DIRECT_11_2_16_BODY = NOT_YET_ACQUIRED
REASONER_ENGLISH_PUBLIC_PREVIEW_LANE = TERMINAL
REASONER_GERMAN_REGIONAL_ILL_LANE = VERIFIED_ROUTE / HUMAN_OR_INSTITUTIONAL_ACCESS
REASONER_VEIL_HAIR_POSITION = NOT_DIRECTLY_VERIFIED
REASONER_KEPHALE_POSITION = NOT_DIRECTLY_VERIFIED
REASONER_EXOUSIA_POSITION = NOT_DIRECTLY_VERIFIED
REASONER_ANGELS_POSITION = NOT_DIRECTLY_VERIFIED
REASONER_PHYSIS_POSITION = NOT_DIRECTLY_VERIFIED
REASONER_V16_POSITION = NOT_DIRECTLY_VERIFIED
REASONER_MULTILINGUAL_REGIONAL_REOPEN = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
```

Circulated p.434/p.444 wording remains unverified. A secondary p.343 claim cannot belong to 11:3 in this edition and stays quarantined.

---

# 2. Michael J. Gorman — Eerdmans 2025

```text
TITLE = 1 Corinthians: A Theological, Pastoral, and Missional Commentary
PUBLICATION_DATE = 2025-03-06
EBOOK_ISBN = 9781467465748
HARDCOVER_ISBN = 9780802882660
PUBLISHER_LENGTH = 477_pages
LOGOS_DIGITAL_LENGTH = 453_pages
```

English publisher/Google routes do not expose the target section.

### 2.1 Licensed library lane

OverDrive directly records the exact 2025 Eerdmans ebook and exposes:

```text
OVERDRIVE_TITLE = EXACT_GORMAN_2025
FORMAT = EBOOK
ISBN = 9780802882660
LIBBY_LIBRARY_SEARCH = AVAILABLE
SAMPLE_EMBED_ROUTE = AVAILABLE
```

The target 1 Cor 11 section has not rendered in the accessible sample, so this is route verification rather than body closure.

```text
GORMAN_11_2_16_DIRECT_BODY = NOT_YET_ACQUIRED
GORMAN_PUBLIC_PREVIEW_LANE = TERMINAL_FOR_TARGET
GORMAN_OVERDRIVE_LIBBY_ROUTE = VERIFIED_LICENSED_ROUTE
GORMAN_VEIL_HAIR_POSITION = NOT_DIRECTLY_VERIFIED
GORMAN_KEPHALE_POSITION = NOT_DIRECTLY_VERIFIED
GORMAN_EXOUSIA_POSITION = NOT_DIRECTLY_VERIFIED
GORMAN_ANGELS_POSITION = NOT_DIRECTLY_VERIFIED
GORMAN_MULTILINGUAL_REGIONAL_REOPEN = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
```

First Spanish/Portuguese title-author passes found no verified translated edition. That result is bounded only.

---

# 3. David I. Starling — EBTC 2025

Official Biblia resource establishes:

```text
AUTHOR = David_I_Starling
TITLE = 1_Corinthians
SERIES = Evangelical_Biblical_Theology_Commentary
YEAR = 2025
PUBLISHER = Lexham_Academic
PRINT_ISBN = 9781683598183
DIGITAL_ISBN = 9781683598190
RESOURCE = LLS:EBTC67CO1
```

The accessible Biblia preview exposes front matter/contents but not the target section body.

A Spanish Logos storefront exposes the **same English digital resource** with `Ojear libro`. This is a localized retail interface, not a Spanish translation.

```text
STARLING_OFFICIAL_BIBLIA_PREVIEW = VERIFIED
STARLING_SPANISH_LOGOS_UI = SAME_ENGLISH_RESOURCE / NOT_TRANSLATION
STARLING_PREVIEW_TARGET_SECTION = NOT_EXPOSED
STARLING_2025_1COR11_POSITION = NOT_DIRECTLY_VERIFIED
STARLING_DIRECT_QUOTE = FORBIDDEN_UNTIL_SECTION_ACQUIRED
STARLING_MULTILINGUAL_REGIONAL_REOPEN = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
```

First Portuguese/Spanish translation searches found no verified translated edition.

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

### Spanish revised route

Official Logos/Tesoro Bíblico:

```text
TITLE_ES = La primera epístola a los Corintios: Nuevo Comentario Internacional del Nuevo Testamento
PUBLISHER = Editorial_Tesoro_Biblico
YEAR = 2024
PAGES = 1044
TRANSLATION_BASE = REVISED_ENGLISH_2014
FEE_ES_2024_LICENSED_LOOK_INSIDE = VERIFIED
FEE_ES_2024_TARGET_11_2_16_BODY = NOT_EXPOSED_CURRENT_PREVIEW
```

### Portuguese revised route — direct official sample

Official Vida Nova / CLC:

```text
TITLE_PT = 1 Coríntios: Comentário exegético
PRINT_ISBN = 9788527509268
EBOOK_ISBN = 9786559671076
EDITION_YEAR = 2019
PAGES = 1168
TRANSLATION_BASE = SECOND_ENGLISH_EDITION_2014
OFFICIAL_SAMPLE = 52_PAGE_PDF
```

Direct Portuguese revised map:

```text
MULHERES_E_HOMENS_NO_CULTO_11_2_16 = p616
CULTURA_VERGONHA_11_2_6 = p626
CRIACAO_11_7_12 = p645
DECORO_11_13_16 = p660
LORDS_SUPPER_11_17_34 = p668
```

The official translated revised preface directly confirms Fee's revision rationale: 2011 NIV base, removal of about twenty old translation-related footnotes, incorporation of the greatly expanded post-1987 literature, and presentation changes.

```text
FEE_PT_2019_TRANSLATES_REVISED_2014 = CLOSED_DIRECT_OFFICIAL
FEE_PT_2019_OFFICIAL_SAMPLE = CLOSED_DIRECT_PDF
FEE_PT_2019_REVISED_PREFACE = CLOSED_DIRECT_BODY
FEE_PT_2019_REVISED_TOC = CLOSED_DIRECT_BODY
FEE_PT_2019_11_2_16_EXPOSITION_BODY = NOT_IN_52_PAGE_SAMPLE
```

Search indexing also surfaced a user-upload platform copy corresponding to the Portuguese volume. It is **not** accepted as the authorized acquisition route; it is discovery-only and adds no quote-safe body.

### Fee 1987 firewall

The user-provided Nueva Creación Spanish PDF is a published translation of the **1987 first edition**, not 2014. It is direct body for Fee 1987 and is stored in Google Drive; provenance receipt:
- `data/1cor11-fee-1987-spanish-user-acquisition-2026-08-11.md`

```text
FEE_1987_FIRST_EDITION_DIRECT_BODY = CLOSED_DIRECT
FEE_1987_SPANISH_1994 != FEE_2014_REVISED_BODY
FEE_1987_PAGINATION != FEE_2014_PAGINATION
FEE_1987_WORDING != FEE_2014_WORDING_AUTOMATICALLY
FEE_2014_MULTILINGUAL_REOPEN = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
FEE_2014_TARGET_EXPOSITION_BODY = STILL_NOT_DIRECTLY_ACQUIRED
```

## 4.2 Ciampa / Rosner 2010

```text
TITLE = The First Letter to the Corinthians
AUTHORS = Roy_E_Ciampa + Brian_S_Rosner
SERIES = PNTC
YEAR = 2010
PRINT_ISBN = 9780802837325
EBOOK_ISBN = 9781467426947
CIAMPA_ROSNER_2010_PP503_540 = TARGET_RANGE
```

First Spanish/Portuguese title-author search found no verified published translation of the volume.

### 4.2.1 IxTheo licensed/institutional lane

IxTheo has an exact electronic-book record:

```text
FORMAT = ELECTRONIC_BOOK
PHYSICAL_DESCRIPTION = 1_online_resource_836_pages
EBOOK_ISBN = 9781467426947
ONLINE_ACCESS = VOLLTEXT_LIZENZPFLICHTIG
HBZ_GATEWAY = AVAILABLE_ROUTE
FACHINFORMATIONSDIENSTE_ILL = AVAILABLE_ROUTE
SUBITO = AVAILABLE_ROUTE
```

The record exposes a long publisher-supplied contents map, but the target body is not rendered to this runtime.

```text
CIAMPA_ROSNER_ENGLISH_PUBLIC_PREVIEW_LANE = TERMINAL_FOR_TARGET
CIAMPA_ROSNER_IXTHEO_LICENSED_FULLTEXT_ROUTE = VERIFIED_ROUTE
CIAMPA_ROSNER_GERMAN_REGIONAL_ILL_ROUTE = VERIFIED_ROUTE / HUMAN_OR_INSTITUTIONAL_ACCESS
CIAMPA_ROSNER_DIRECT_11_2_16_BODY = NOT_YET_ACQUIRED
CIAMPA_ROSNER_MULTILINGUAL_REGIONAL_REOPEN = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
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
PDF_ISBN = 9781493451708
SECTION = VII. Headdress in Public Worship (11:2–16)
GARLAND_2025_PP468_493 = RETRACT_AS_UNVERIFIED_LOCATOR
GARLAND_2003_PP505_532 != GARLAND_2025_PAGINATION
```

Logos/Verbum exposes an official `See Inside` route but current indexed preview still does not expose the target section body.

### 4.3.1 Japanese university-holdings lane

CiNii directly records the exact 2025 second edition and identifies physical holdings at two Japanese universities:

```text
CINII_NCID = BD1853434X
EDITION = 2nd_edition
ISBN = 9781540962607
PHYSICAL = xxi_850_pages
HOLDING_1 = Doshisha_University_Library
HOLDING_2 = Nanzan_University_Reiners_Central_Library
```

This is a genuine regional institutional route, not direct body.

```text
GARLAND_2025_PUBLIC_PREVIEW_LANE = TERMINAL_FOR_TARGET
GARLAND_2025_JAPAN_UNIVERSITY_HOLDINGS = VERIFIED_ROUTE / HUMAN_OR_INSTITUTIONAL_ACCESS
GARLAND_2025_TARGET_BODY = NOT_YET_ACQUIRED
GARLAND_2025_MULTILINGUAL_REGIONAL_REOPEN = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
```

First Spanish/Portuguese pass found other Garland works and unrelated translated 1 Corinthians books but no verified translation of the 2025 BECNT second edition.

## 4.4 Thiselton 2000

```text
THISELTON_2000_WORK = VERIFIED
PRINT_ISBN = 9780802824493
EBOOK_ISBN = 9781467423403
THISELTON_2000_PP800_847 = TARGET_RANGE
```

No verified complete Spanish/Portuguese translation has been found in the bounded pass; downstream translated quotations do not count.

### 4.4.1 Licensed and physical-library routes

OverDrive directly records the exact Eerdmans NIGTC ebook and provides both a sample route and Libby library-search route. Separately, the Philippine Baptist Theological Seminary catalogue records an available physical copy of the exact 2000 volume.

```text
THISELTON_OVERDRIVE_SAMPLE_ROUTE = VERIFIED_LICENSED_ROUTE
THISELTON_LIBBY_LIBRARY_SEARCH = VERIFIED_ROUTE
THISELTON_PBTS_PHYSICAL_COPY = VERIFIED_AVAILABLE_HOLDING
THISELTON_TARGET_BODY = NOT_YET_ACQUIRED_CURRENT_RUNTIME
THISELTON_MULTILINGUAL_REGIONAL_REOPEN = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
```

---

# 5. Contextual target — Bruce W. Winter

The multilingual pass found a publisher-authorized Portuguese translation of Winter's *After Paul Left Corinth*:

```text
PORTUGUESE_TITLE = Cristianismo e paganismo: A influência da cultura na igreja de Corinto
AUTHOR = Bruce_W_Winter
PUBLISHER = Vida_Nova
EDITION_YEAR = 2026
PRINT_ISBN = 9786559673933
EBOOK_ISBN = 9786559673926
ORIGINAL_TITLE = After Paul Left Corinth: The Influence of Secular Ethics and Social Change
```

Vida Nova exposes an official sample-PDF route. The current runtime did not render that PDF body. A licensed Portuguese Everand preview directly exposes the translated chapter architecture:

```text
CH6 = Homens e esposas com véu e a contenciosidade cristã (1Coríntios 11.2-16)
SUB1 = O homem não deve cobrir a cabeça; [...] a mulher deve usar véu (11.7,10)
I = Homens de posição cobrem a cabeça
II = Novas esposas e o sinal da condição de casada
III = Reunião pública e os mensageiros
IV = Contenciosidade na igreja
```

English TOC controls place ch.6 at pp.121–141 with subsection starts around pp.121, 123, 133 and 138.

```text
WINTER_PT_2026_EDITION_IDENTITY = CLOSED_DIRECT_PUBLISHER
WINTER_PT_OFFICIAL_SAMPLE_ROUTE = VERIFIED_ROUTE / RUNTIME_RENDER_HOLD
WINTER_PT_LICENSED_TOC_PREVIEW = CLOSED_DIRECT_PREVIEW
WINTER_CH6_TARGET_BODY = NOT_YET_DIRECTLY_ACQUIRED
WINTER_MULTILINGUAL_REOPEN = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
```

---

# 6. Native-language specialist lanes

The method applies to original-language scholarship too: search the native title before translated keywords.

## 6.1 Barbara Lumesberger-Loisl 2025

IxTheo directly identifies:
- `Kopftuchgebot für Christinnen?: Die „Verhüllung“ des Kopfes als Ausdruck der Geschlechterdifferenz (1 Kor 11,2-16)`;
- 2025;
- pp.295–303;
- ISBN `9783460252660`;
- German specialized-library / ILL availability.

```text
LUMESBERGER_LOISL_NATIVE_GERMAN_METADATA = CLOSED
LUMESBERGER_LOISL_GERMAN_ILL_ROUTE = VERIFIED_INSTITUTIONAL_ROUTE
LUMESBERGER_LOISL_BODY = STILL_HOLD
```

## 6.2 Marlis Gielen 1999

Native title:
- `Beten und Prophezeien mit unverhülltem Kopf? Die Kontroverse zwischen Paulus und der korinthischen Gemeinde um die Wahrung der Geschlechtsrollensymbolik in 1Kor 11,2–16`, ZNW 90.3–4 (1999), pp.220–249.

Search surfaced bibliographic/full-text-delivery routes but no directly renderable publisher body.

```text
GIELEN_NATIVE_GERMAN_SEARCH_LANE = TESTED
GIELEN_DIRECT_BODY = STILL_HOLD
```

## 6.3 Jorunn Økland

Bloomsbury's official product has a `Look Inside` route and sells the PDF ebook; Perlego lists a licensed PDF with chapter-level TOC.

```text
OKLAND_BLOOMSBURY_LOOK_INSIDE_ROUTE = VERIFIED
OKLAND_PERLEGO_LICENSED_PDF_ROUTE = VERIFIED
OKLAND_TARGET_CH4_7_BODY = NOT_DIRECTLY_ACQUIRED_CURRENT_RUNTIME
```

## 6.4 Peter Lampe 2012 — German OA route

Heidelberg University repository directly records:
- Peter Lampe, `Paulus und die erotischen Reize der Korintherinnen (1 Kor 11,2–16)`;
- in *Männerspezifische Bibelauslegung*;
- Göttingen, Vandenhoeck & Ruprecht, 2012;
- pp.196–207;
- DOI `10.11588/heidok.00025278`;
- official OA PDF route.

The repository PDF endpoint is presently blocked in this runtime by the host's anti-bot layer, so body is not reconstructed from title or secondary references.

```text
LAMPE_2012_OBJECT = CLOSED_DIRECT_INSTITUTIONAL_METADATA
LAMPE_2012_OFFICIAL_OA_PDF_ROUTE = VERIFIED
LAMPE_2012_PDF_RENDER = TERMINAL_RUNTIME_ANTIBOT_HOLD_CURRENT_ROUTE
LAMPE_2012_ARGUMENT = NOT_YET_DIRECTLY_READ
```

## 6.5 Piotr Łabuda 2019 — Polish repository route

The Theo-logos/KUL repository directly records:
- Piotr Łabuda, `1 Kor 11,2-16 wyrazem mizoginizmu św. Pawła?`;
- *Śląskie Studia Historyczno-Teologiczne* 52.1 (2019), pp.5–22;
- Polish;
- repository PDF `Labuda_1_Kor_11.pdf`;
- CC-BY-SA metadata/license.

Its abstract directly says Paul accepts women praying/prophesying in the assembly, rejects doing so with uncovered heads, and treats clothing/hairstyle/head covering as culturally situated. The current runtime could not fetch the PDF bytes, so only the abstract is direct at present.

```text
LABUDA_2019_OBJECT = CLOSED_DIRECT_INSTITUTIONAL_METADATA
LABUDA_2019_REPOSITORY_PDF_ROUTE = VERIFIED
LABUDA_2019_LICENSE = CC_BY_SA_AS_REPORTED_BY_REPOSITORY
LABUDA_2019_ABSTRACT = CLOSED_DIRECT
LABUDA_2019_FULL_BODY = TERMINAL_RUNTIME_FETCH_HOLD_CURRENT_ROUTE
```

These two nodes are search-method gains; they do not change core grades without body-level analysis.

---

# 7. Queue semantics after multilingual/regional route sweep

The former bounded-English statement `CURRENT_COMMENTARY_ACTIVE_ACQUISITION_QUEUE = EMPTY_FOR_CURRENT_PUBLIC_ROUTES` was reopened on 2026-08-11 after materially distinct language/regional routes were found. Those routes have now been individually classified as direct body, preview/route-only, human/institutional access, or terminal runtime/body HOLD. Therefore the known-route sweep is again disposition-complete.

Use:

```text
ENGLISH_KNOWN_ROUTE_AUDIT = DISPOSITION_COMPLETE
MULTILINGUAL_KNOWN_ROUTE_SWEEP = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
REGIONAL_KNOWN_ROUTE_SWEEP = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
MULTILINGUAL_NEW_AUTHORIZED_ROUTES_FOUND = YES
REGIONAL_INSTITUTIONAL_NEW_ROUTES_FOUND = YES
FEE_2014_PT_ES = AUTHORIZED_REVISED_EDITION_ROUTES_FOUND / TARGET_EXPOSITION_NOT_YET_EXPOSED
WINTER_2001_PT_2026 = AUTHORIZED_TRANSLATION_ROUTE_FOUND / CH6_BODY_NOT_YET_EXPOSED
REASONER_2025_IXTHEO_ILL = VERIFIED_ROUTE / HUMAN_OR_INSTITUTIONAL_ACCESS
CIAMPA_ROSNER_IXTHEO_LICENSED_ILL = VERIFIED_ROUTE / HUMAN_OR_INSTITUTIONAL_ACCESS
GARLAND_2025_CINII_HOLDINGS = VERIFIED_ROUTE / HUMAN_OR_INSTITUTIONAL_ACCESS
THISELTON_OVERDRIVE_PBTS = VERIFIED_ROUTE / HUMAN_OR_INSTITUTIONAL_ACCESS
CURRENT_COMMENTARY_ACTIVE_ACQUISITION_QUEUE = EMPTY_FOR_CURRENT_KNOWN_PUBLIC_ROUTES
CURRENT_COMMENTARY_REOPEN = ONLY_NEW_USER_BODY_OR_NEW_RENDERABLE_AUTHORIZED_OR_MATERIALLY_DISTINCT_SOURCE
REPEAT_EXHAUSTED_ENGLISH_PREVIEW_ROUTE = NO
REPEAT_ALREADY_CLASSIFIED_LANGUAGE_REGIONAL_ROUTE = NO
```

A classified human/library/purchase/login route remains useful for source-custody improvement but is not an active agent web-search blocker. Reopen only if a genuinely new renderable authorized route, user-provided body, or materially distinct source appears.

---

# 8. Audit lessons

```text
SEARCH_INDEX_STRIPPED_VERSE_LABEL != SAFE_MANUAL_MAPPING
CHAPTER_SEQUENCE_MUST_BE_RECONCILED_WITH_PUBLISHER_TOC
CURRENT_EDITION != POSITION_VERIFIED
PREVIEW_NO_MATCH != ABSENCE_FROM_BOOK
LICENSED_SAMPLE_ROUTE != TARGET_SECTION_READ
LIBRARY_RECORD != TARGET_SECTION_READ
ILL_ROUTE != TARGET_SECTION_READ
EDITION_1_PAGINATION != EDITION_2_PAGINATION_AUTOMATICALLY
TRANSLATION_PAGINATION != SOURCE_PAGINATION
PUBLISHED_TRANSLATION_BODY_CAN_VERIFY_AUTHOR_POSITION_FOR_THAT_EDITION
PUBLISHED_TRANSLATION_BODY_CANNOT_CREATE_AN_ORIGINAL_LANGUAGE_QUOTE
LOCALIZED_STOREFRONT != TRANSLATED_EDITION
MACHINE_TRANSLATION != PUBLISHED_TRANSLATION
PAYWALL != PERMISSION_TO_USE_DOWNSTREAM_QUOTE_AS_PRIMARY
USER_UPLOAD_PLATFORM != AUTHORIZED_ROUTE
TERMINAL_ACCESS_HOLD != SUBSTANTIVE_DISCONFIRMATION
BOUNDED_LANGUAGE_SEARCH != GLOBAL_NONEXISTENCE
```

---

# 9. Result

```text
REASONER_2025 = VERIFIED_CURRENT_TECHNICAL_COMMENTARY / IXTHEO_HBZ_ILL_SUBITO_ROUTE_FOUND / BODY_NOT_ACQUIRED
GORMAN_2025 = VERIFIED_CURRENT_COMMENTARY / OVERDRIVE_LIBBY_ROUTE_VERIFIED / BODY_NOT_ACQUIRED
STARLING_2025 = VERIFIED_CURRENT_COMMENTARY / SPANISH_LOGOS_UI_IS_NOT_TRANSLATION / BODY_NOT_ACQUIRED
GARLAND_2025_2E = SECTION_IDENTITY_CLOSED / CINII_JAPAN_HOLDINGS_FOUND / BODY_NOT_ACQUIRED
THISELTON_2000 = WORK_AND_RANGE_CLOSED / OVERDRIVE_AND_PHYSICAL_LIBRARY_ROUTES_FOUND / BODY_NOT_ACQUIRED
CIAMPA_ROSNER_2010 = WORK_AND_RANGE_CLOSED / IXTHEO_LICENSED_FULLTEXT_ILL_ROUTE_FOUND / BODY_NOT_ACQUIRED

FEE_1987_SPANISH_1994 = CLOSED_DIRECT_BODY
FEE_2014_PORTUGUESE_2019 = AUTHORIZED_REVISED_TRANSLATION / PREFACE_AND_TOC_CLOSED_DIRECT / 11_2_16_BODY_NOT_EXPOSED
FEE_2014_SPANISH_2024 = AUTHORIZED_REVISED_TRANSLATION / LICENSED_PREVIEW_ROUTE / 11_2_16_BODY_NOT_EXPOSED
WINTER_PORTUGUESE_2026 = AUTHORIZED_TRANSLATION_ROUTE / CH6_TOC_CLOSED / BODY_NOT_EXPOSED

LAMPE_2012_GERMAN_OA_ROUTE = VERIFIED / RUNTIME_ANTIBOT_HOLD
LABUDA_2019_POLISH_REPOSITORY_ROUTE = VERIFIED / ABSTRACT_DIRECT / PDF_RUNTIME_FETCH_HOLD

ENGLISH_KNOWN_ROUTE_AUDIT = DISPOSITION_COMPLETE
MULTILINGUAL_KNOWN_ROUTE_SWEEP = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
REGIONAL_KNOWN_ROUTE_SWEEP = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
CURRENT_KNOWN_PUBLIC_AGENT_QUEUE_EMPTY = true
HUMAN_LIBRARY_PURCHASE_LOGIN_QUEUE = NOT_EMPTY
NEW_USER_PROVIDED_BODY = REOPEN_TRIGGER
NEW_RENDERABLE_AUTHORIZED_ROUTE = REOPEN_TRIGGER
NEW_MATERIALLY_DISTINCT_SOURCE = REOPEN_TRIGGER
CORE_GRADE_REVERSALS = 0
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
SITE_PUBLICATION = false
```
