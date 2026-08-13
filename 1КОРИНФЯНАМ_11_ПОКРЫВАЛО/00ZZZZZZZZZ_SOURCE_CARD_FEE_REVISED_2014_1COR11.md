# Source card — Gordon D. Fee, *The First Epistle to the Corinthians*, Revised Edition (2014), 1 Cor 11:2–16

**Дата аудита:** 2026-08-11  
**Статус:** `TECHNICAL-COMMENTARY / REVISED-EDITION-CALIBRATION / MULTILINGUAL-ACQUISITION / EXACT-TOC-CLOSED / TARGET-BODY-HOLD / RESEARCH-ONLY`

## 0. Purpose

Fee is repeatedly cited throughout the 1 Cor 11 literature, but several evidence objects must remain distinct:

```text
FEE_1987_FIRST_EDITION
FEE_1994_SPANISH_TRANSLATION_OF_1987
FEE_2014_REVISED_EDITION_MAIN_BODY
FEE_2014_NEW_BIBLIOGRAPHIC_ADDENDA/FOOTNOTE_UPDATES
FEE_2019_PORTUGUESE_TRANSLATION_OF_REVISED_2014
FEE_2019_KOREAN_TRANSLATION_OF_REVISED_2014
FEE_2024_SPANISH_TRANSLATION_OF_REVISED_2014
```

This card prevents four shortcuts:
1. assuming the 2014 Addendum is a hidden new commentary;
2. treating downstream quotations as direct revised body;
3. treating a translation of 1987 as 2014 evidence;
4. refusing a genuine published translation as direct author-position evidence merely because it is not English.

```text
LANGUAGE != EVIDENCE_GRADE
PUBLISHED_TRANSLATION_OF_VERIFIED_EDITION_CAN_VERIFY_AUTHOR_POSITION_FOR_THAT_EDITION
PUBLISHED_TRANSLATION_WORDING != ORIGINAL_LANGUAGE_QUOTE
TRANSLATION_PAGINATION != ORIGINAL_PAGINATION
```

---

# 1. English revised-edition identity

Direct Eerdmans/Logos/Biblia controls verify:

```text
AUTHOR = Gordon D. Fee
TITLE = The First Epistle to the Corinthians
EDITION = Revised Edition
SERIES = NICNT
PUBLISHER = Eerdmans
YEAR = 2014
PRINT_ISBN = 9780802871367
EBOOK_ISBN = 9781467440417
LOGOS_RESOURCE = LLS:NICNT67CO1_2ED
PAGES = 1044
```

The English Logos/Biblia preview verifies the revised object but does not render the target 1 Cor 11 body in the current route.

---

# 2. Exact English revised-edition 11:2–16 map

```text
C. Women and Men in Worship (11:2–16) ............. p542
1. An Argument from Culture and Shame (11:2–6) ... p550
Addendum ........................................... p565
2. An Argument from Creation (11:7–12) ............ p567
3. An Argument from Propriety (11:13–16) .......... p580
D. Abuse of the Lord's Supper (11:17–34) .......... p587
```

Thus:

```text
MAIN_11_2_16 = pp542_586
CULTURE_SHAME_EXPOSITION = pp550_564
ADDENDUM = starts p565; about 2 pages
CREATION_11_7_12 = pp567_579
PROPRIETY_11_13_16 = pp580_586
```

These are English 2014 revised-edition locators. Never transfer 1987 or translated pagination into this map.

---

# 3. New direct authorized route: Portuguese revised edition

Official Vida Nova / CLC controls verify:

```text
TITLE_PT = 1 Coríntios: Comentário exegético
AUTHOR = Gordon_D_Fee
PUBLISHER = Vida_Nova
EDITION_YEAR = 2019
PRINT_ISBN = 9788527509268
EBOOK_ISBN = 9786559671076
PAGES = 1168
ORIGINAL_TITLE = The First Epistle to the Corinthians
TRANSLATION_BASE = SECOND_ENGLISH_EDITION_2014
```

CLC exposes an official downloadable sample PDF (`1corintios_comentario_exegetico_trecho`, 918.8 KB). The fetched object is 52 pages and directly exposes both the revised-edition preface and the translated TOC.

## 3.1 Direct Portuguese revised pagination

The official sample directly gives:

```text
C. Mulheres e homens no culto (11.2-16) ........... p616
1. Cultura e sentimento de vergonha (11.2-6) ...... p626
2. Criação (11.7-12) ............................... p645
3. Decoro (11.13-16) ............................... p660
D. Abusos contra a ceia do Senhor (11.17-34) ...... p668
```

Evidence class:

```text
FEE_PT_2019_EDITION_IDENTITY = CLOSED_DIRECT_OFFICIAL
FEE_PT_2019_TRANSLATES_REVISED_2014 = CLOSED_DIRECT_OFFICIAL
FEE_PT_2019_OFFICIAL_SAMPLE = CLOSED_DIRECT_PDF
FEE_PT_2019_REVISED_TOC = CLOSED_DIRECT_BODY
FEE_PT_2019_11_2_16_TARGET_EXPOSITION = NOT_PRESENT_IN_52_PAGE_SAMPLE
```

## 3.2 Revised preface now direct through the Portuguese translation

This is stronger than the previous review-only control. In Fee's own revised preface as directly exposed by the authorized Portuguese translation, he explains that:
- the first edition used the 1978 NIV;
- he later had access to the 2011 NIV text before publication;
- the revised edition allowed him to remove about twenty first-edition footnotes tied to translation problems;
- the technical literature on 1 Corinthians had expanded dramatically in the intervening quarter century;
- he also changed presentation conventions around chapter/verse language.

Therefore:

```text
FEE_2014_REVISION_MOTIVATION = CLOSED_DIRECT_AUTHOR_PREFACE_VIA_AUTHORIZED_TRANSLATION
NIV_2011_BASE_TEXT = CLOSED_DIRECT_AUTHOR_PREFACE
ABOUT_TWENTY_OLD_TRANSLATION_FOOTNOTES_REMOVED = CLOSED_DIRECT_AUTHOR_PREFACE
POST_1987_LITERATURE_UPDATE = CLOSED_DIRECT_AUTHOR_PREFACE
VERSE_NUMBER_PRESENTATION_CHANGE = CLOSED_DIRECT_AUTHOR_PREFACE
```

This does **not** by itself prove which individual 1 Cor 11 sentences changed. The target exposition still requires direct section body.

---

# 4. New authorized route: Spanish revised edition

Official Logos / Editorial Tesoro Bíblico verifies:

```text
TITLE_ES = La primera epístola a los Corintios: Nuevo Comentario Internacional del Nuevo Testamento
AUTHOR = Gordon_D_Fee
PUBLISHER = Editorial_Tesoro_Biblico
YEAR = 2024
PAGES = 1044
TRANSLATION_BASE = REVISED_ENGLISH_VERSION_2014
ACCESS = LOGOS_DIGITAL_EDITION / OJEAR_LIBRO
```

The product description explicitly states that the Spanish edition comes from the revised English commentary published in 2014.

```text
FEE_ES_2024_EDITION_IDENTITY = CLOSED_DIRECT_OFFICIAL
FEE_ES_2024_TRANSLATES_REVISED_2014 = CLOSED_DIRECT_OFFICIAL
FEE_ES_2024_LICENSED_LOOK_INSIDE_ROUTE = VERIFIED
FEE_ES_2024_11_2_16_TARGET_BODY = NOT_EXPOSED_CURRENT_PREVIEW
```

Do not confuse this with the Nueva Creación Spanish edition.

---

# 5. New authorized route: Korean revised edition

A materially distinct Korean licensed lane is now directly controlled.

Official Logos/Biblia copyright metadata identifies:

```text
TITLE_KO = NICNT 고린도전서
AUTHOR = Gordon_D_Fee
TRANSLATOR = 최병필
PUBLISHER = 부흥과개혁사 / Revival_and_Reformation_Press
PRINT_YEAR = 2019
PRINT_ISBN = 9788960925489
LOGOS_RESOURCE = LLS:NICNT67CO1_2ED-KO
ORIGINAL_TITLE = The_First_Epistle_to_the_Corinthians_Revised_Edition
ORIGINAL_COPYRIGHT = 1987_2014_Gordon_D_Fee
ORIGINAL_PUBLISHER = Eerdmans
TRANSLATION_BASE = REVISED_ENGLISH_EDITION_2014
RIGHTS = TRANSLATED_AND_USED_BY_PERMISSION_OF_EERDMANS
```

Biblia explicitly states that the Korean edition is translated and used by permission of Wm. B. Eerdmans Publishing Co. The licensed Korean print object is independently catalogued by Korean booksellers and Google Books as the translation of *NICNT The First Epistle to the Corinthians, Revised Edition*.

The later licensed Korean ebook is also independently catalogued:

```text
EBOOK_YEAR = 2023
EBOOK_ISBN = 9788960928206
FORMAT = EPUB
```

The current public Biblia/retailer preview surfaces establish edition identity, rights and TOC/product metadata but do **not** expose the target 1 Cor 11:2–16 exposition deeply enough for body-level claims.

```text
FEE_KO_2019_EDITION_IDENTITY = CLOSED_DIRECT_OFFICIAL_BIBLIA
FEE_KO_2019_TRANSLATES_REVISED_2014 = CLOSED_DIRECT_OFFICIAL_BIBLIA
FEE_KO_2019_EERDMANS_PERMISSION = CLOSED_DIRECT_OFFICIAL_BIBLIA
FEE_KO_2019_LOGOS_RESOURCE = VERIFIED
FEE_KO_2023_LICENSED_EBOOK = VERIFIED
FEE_KO_2019_11_2_16_TARGET_BODY = NOT_EXPOSED_CURRENT_PREVIEW
```

This route is acquisition-capable if the licensed preview/library surface later exposes the target section. Route existence does not itself close any Fee 2014 exegetical wording.

---

# 6. First-edition firewall now strengthened by direct user copy

The user-provided PDF `Gordon D. Fee, Primera Epistola a Los Corintios.pdf` was page-autopsied. Its title/copyright pages establish:

```text
SPANISH_PUBLISHER = Nueva_Creacion
SPANISH_COPYRIGHT = 1994
ORIGINAL_COPYRIGHT = Eerdmans_1987
TRANSLATOR = Carlos_Alonso_Vargas
TRANSLATION_BASE = FEE_1987_FIRST_EDITION
```

The complete 1 Cor 11:2–16 body in that object is direct readable evidence for Fee's 1987 position. It has been stored in Google Drive and recorded in:
- `data/1cor11-fee-1987-spanish-user-acquisition-2026-08-11.md`

```text
FEE_1987_FIRST_EDITION_DIRECT_BODY = CLOSED_DIRECT
FEE_ES_1994_NUEVA_CREACION = TRANSLATION_OF_1987
FEE_ES_1994 != FEE_ES_2024_TESORO_BIBLICO
FEE_ES_1994 != FEE_2014_REVISED_BODY
```

This first-edition closure is valuable for later edition-delta comparison, but it cannot silently close the 2014 text.

---

# 7. What the 2014 Addendum is — and is not

A detailed review based on a 2014 review copy reports that the new addendum on 11:2–6 is primarily bibliographical material with a short introduction rather than a second substantive exposition. An independent DTS review likewise reports broad continuity alongside NIV/literature/footnote updating.

```text
FEE_2014_ADDENDUM_BIBLIOGRAPHIC_NATURE = STRONG_REVIEW_CONTROL
FEE_2014_ADDENDUM_DIRECT_BODY = STILL_NOT_ACQUIRED
FEE_2014_ADDENDUM_AS_MAJOR_NEW_EXEGESIS = NOT_SUPPORTED_BY_CURRENT_EVIDENCE
```

The direct Portuguese revised preface now independently confirms that substantial bibliographic and translation-base updating occurred across the revised edition, but it does not make the Addendum body direct.

---

# 8. Current exact-body status for 11:2–16

English routes already tested:

```text
BIBLIA_NICNT67CO1_2ED = OFFICIAL_EMBEDDED_PREVIEW / TARGET_BODY_NOT_EXPOSED
GOOGLE_BOOKS = METADATA_TOC_SELECTED_MATERIAL / TARGET_BODY_NOT_EXPOSED
GOOGLE_PLAY = SAMPLE_OBJECT / TARGET_BODY_NOT_EXPOSED
```

New language routes:

```text
PORTUGUESE_VIDA_NOVA_CLC = AUTHORIZED_REVISED_TRANSLATION / OFFICIAL_52_PAGE_SAMPLE / PREFACE_AND_TOC_DIRECT / TARGET_BODY_NOT_IN_SAMPLE
SPANISH_TESORO_BIBLICO_LOGOS = AUTHORIZED_REVISED_TRANSLATION / LICENSED_LOOK_INSIDE / TARGET_BODY_NOT_EXPOSED_CURRENT_PREVIEW
KOREAN_RNR_LOGOS_BIBLIA = AUTHORIZED_REVISED_TRANSLATION / OFFICIAL_RESOURCE_AND_RIGHTS_CLOSED / TARGET_BODY_NOT_EXPOSED_CURRENT_PREVIEW
```

Therefore the old global terminal wording is superseded:

```text
FEE_2014_ENGLISH_KNOWN_ROUTES = TERMINAL_EXTERNAL_ACCESS_HOLD
FEE_2014_MULTILINGUAL_REOPEN = ACTIVE
FEE_2014_PP542_586_OR_EQUIVALENT_TRANSLATED_TARGET_BODY = NOT_YET_DIRECTLY_ACQUIRED
FEE_2014_NOTES_11_2_16 = NOT_YET_DIRECTLY_ACQUIRED
```

No exact English quotation should be labelled `direct Fee 2014` unless the English page itself is acquired. A published revised translation can establish Fee's substantive position for the 2014 edition if its target body is acquired, but must be cited as translation evidence.

---

# 9. Angels — strong locator, still not target-body closure

Peer-reviewed scholarship places the revised Fee angel discussion at:

```text
Fee, First Epistle, pp576_578
```

A secondary quote chain assigns the anti-lustful-Watchers argument to:

```text
p576 n123
```

Current evidence class:

```text
FEE_2014_ANGELS_LOCATOR_576_578 = STRONG_PEER_REVIEWED_PAGE_LOCATOR
FEE_2014_N123_WATCHERS_REJECTION = STRONG_SECONDARY_QUOTE_LOCATOR
FEE_2014_N123_DIRECT_ENGLISH_PAGE = NOT_ACQUIRED
FEE_2014_EQUIVALENT_PT_ES_KO_ANGEL_SECTION = SEARCH_TARGET_ACTIVE
```

Do not promote the reproduced wording to quote-safe Fee text.

---

# 10. v16 — exhortative force, custom and command-level firewall

The direct revised TOC places 11:13–16 at pp.580–586. The exact English pages are still not directly acquired, but a page-specific secondary quotation chain now pins two Fee Revised observations to pp.585–586:

1. Fee treats the conclusion as explicitly dealing with church **custom/practice**, not as though `συνήθεια` itself meant a formal command;
2. he nevertheless reads the rejected “such practice” as the practice advocated by the contentious opponents, rather than taking v16 as a simple cancellation of the preceding argument.

The strongest current page-specific chain is Harrison Perkins, “The Custom Of God’s Churches: Head Coverings And Cultural Appropriateness (Part 3),” which cites Fee Revised p.585 and pp.585–586 and reproduces short Fee wording. This is useful for locator/authentication, not a substitute for Fee’s own page image/body.

```text
FEE_2014_V16_RANGE = pp580_586_DIRECT_TOC
FEE_2014_V16_P585_586 = STRONG_PAGE_SPECIFIC_SECONDARY_LOCATOR
FEE_2014_V16_CUSTOM_NOT_FORMAL_COMMAND_DISTINCTION = STRONG_SECONDARY_ATTESTATION
FEE_2014_V16_SUCH_PRACTICE = CONTENT_OF_CONTENTIOUS_POSITION_IN_SECONDARY_ATTESTATION
FEE_2014_V16_DIRECT_ENGLISH_PAGE = NOT_ACQUIRED
```

The same page-specific discussion reports that Fee cites Troels Engberg-Pedersen’s specialist article:

> “1 Corinthians 11:16 and the Character of Pauline Exhortation,” *Journal of Biblical Literature* 110.4 (1991): 679–689.

JSTOR directly verifies Engberg-Pedersen’s article identity and pagination; its XML/body route remains a current runtime cache miss. Independent published reception pins his distinctive reading at p.684: `τοιαύτην συνήθειαν` refers to the **habit of contentiousness**, not to head-covering itself. Benjamin Edsall explicitly agrees with Engberg-Pedersen on the relevance of `συνήθεια` while rejecting that antecedent and preferring head-coverings; Peters 2025 likewise identifies Engberg-Pedersen’s p.684 position.

```text
ENGBERG_PEDERSEN_1991_IDENTITY_PP679_689 = DIRECT_JSTOR
ENGBERG_PEDERSEN_P684_CONTENTIOUSNESS_ANTECEDENT = STRONG_INDEPENDENT_PAGE_SPECIFIC_RECEPTION
ENGBERG_PEDERSEN_DIRECT_BODY = CURRENT_JSTOR_XML_PDF_CACHE_HOLD
EDSALL_DISAGREES_ON_EXACT_ANTECEDENT = PUBLISHED_COUNTERCONTROL
EXACT_V16_CUSTOM_ANTECEDENT = B_C_UNCHANGED
```

Project consequence:

```text
V16_ECCLESIAL_EXHORTATIVE_NORMATIVE_FORCE = B_HIGH_UNCHANGED
V16_FORMAL_COMMAND_AS_SUCH = NOT_ESTABLISHED_BY_SYNĒTHEIA_ALONE
V16_IDENTICAL_TIMELESS_GARMENT_FORM = UNPROVED
V16_CANCELS_VV2_15 = D_C_LOW_UNCHANGED
```

This is a **label/calibration clarification**, not a downgrade of v16’s translocal ecclesial weight.

---

# 11. Reopened target order

```text
P0A = Portuguese 2019 target section around local pp616_667, especially v10/angels equivalent of English pp576_578/n123
P0B = Korean 2019/2023 Logos-Biblia revised target section, especially v10/angels
P0C = Spanish 2024 Logos revised target section, especially v10/angels
P1 = English revised pp576_578/n123 if a new lawful/institutional route appears
P1 = English/translated complete 11:2-6 main body and Addendum
P1 = English revised pp580_586 / translated vv13-16 body, especially direct p585-586
```

Do not repeat the exhausted English preview endpoints as though they were new searches.

---

# 12. Edition / translation firewall

```text
FEE_CITATION_WITH_YEAR_2014 + 1987_PAGE_NUMBER = VERIFY_BEFORE_USE
FEE_QUOTE_WITHOUT_EDITION = EDITION_AMBIGUOUS
FEE_1987_WORDING != AUTOMATIC_2014_WORDING
FEE_1987_PAGINATION != FEE_2014_PAGINATION
FEE_PT_2019_PAGINATION != ENGLISH_2014_PAGINATION
FEE_ES_2024_DIGITAL_LOCATOR != ENGLISH_2014_PRINT_PAGINATION
FEE_KO_2019_PAGINATION != ENGLISH_2014_PAGINATION
FEE_KO_2023_EBOOK_LOCATOR != ENGLISH_2014_PRINT_PAGINATION
TRANSLATED_DIRECT_BODY != ORIGINAL_LANGUAGE_VERBATIM_QUOTE
SECONDARY_FEE_PAGE_QUOTE != DIRECT_REVISED_BODY
```

---

# 13. Relation to current project models

No grade reversal follows merely from the new acquisition routes or the v16 page-specific secondary control.

```text
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH
EXOUSIA_EXACT_REFERENT = B_C
HEAVENLY_HOLY_ANGELS_REFERENT = B_HIGH_LEADING
WATCHERS = C_SERIOUS_ALTERNATIVE
V16_ECCLESIAL_EXHORTATIVE_NORMATIVE_FORCE = B_HIGH
V16_EXACT_CUSTOM_ANTECEDENT = B_C
IDENTICAL_TIMELESS_GARMENT_FORM = UNPROVED
CORE_GRADE_REVERSALS = 0
```

Fee remains a high-weight technical pressure-test, not a vote that automatically decides the issue.

---

# 14. Result

```text
FEE_2014_REVISED_EDITION = VERIFIED
FEE_2014_ENGLISH_11_2_16_RANGE = pp542_586
FEE_2014_ENGLISH_11_2_6_MAIN = pp550_564
FEE_2014_ENGLISH_ADDENDUM = pp565_566_APPROX
FEE_2014_ENGLISH_11_7_12 = pp567_579
FEE_2014_ENGLISH_11_13_16 = pp580_586

FEE_1987_FIRST_EDITION_DIRECT_BODY = CLOSED_DIRECT_VIA_AUTHORIZED_SPANISH_TRANSLATION
FEE_PT_2019 = AUTHORIZED_TRANSLATION_OF_REVISED_2014
FEE_PT_2019_REVISED_PREFACE = CLOSED_DIRECT
FEE_PT_2019_TOC = CLOSED_DIRECT
FEE_PT_2019_11_2_16_TARGET_BODY = NOT_IN_OFFICIAL_SAMPLE
FEE_ES_2024 = AUTHORIZED_TRANSLATION_OF_REVISED_2014
FEE_ES_2024_TARGET_BODY = NOT_EXPOSED_CURRENT_PREVIEW
FEE_KO_2019 = AUTHORIZED_TRANSLATION_OF_REVISED_2014
FEE_KO_2019_LOGOS_RESOURCE = LLS:NICNT67CO1_2ED-KO
FEE_KO_2019_RIGHTS = CLOSED_DIRECT_BIBLIA
FEE_KO_2023_EBOOK = VERIFIED_LICENSED
FEE_KO_TARGET_BODY = NOT_EXPOSED_CURRENT_PREVIEW

ADDENDUM_AS_NEW_MAJOR_EXEGESIS = REJECTED_WORKING_ASSUMPTION
FEE_ANGELS = PEER_REVIEWED_LOCATOR_PP576_578
FEE_WATCHERS_REJECTION = SECONDARY_LOCATOR_P576_N123
FEE_V16 = STRONG_SECONDARY_LOCATOR_PP585_586 / DIRECT_PAGE_HOLD
ENGBERG_PEDERSEN_1991 = DIRECT_JSTOR_IDENTITY / BODY_CACHE_HOLD

ENGLISH_KNOWN_ROUTE_AUDIT = COMPLETE
FEE_MULTILINGUAL_REOPEN = ACTIVE
TERMINAL_EXTERNAL_ACCESS_HOLD != VERIFIED_BODY
TERMINAL_EXTERNAL_ACCESS_HOLD != NEGATIVE_EVIDENCE
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
SITE_PUBLICATION = false
```
