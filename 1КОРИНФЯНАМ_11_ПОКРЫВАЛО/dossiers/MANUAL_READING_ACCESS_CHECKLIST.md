# 1 Коринфянам 11:2–16 — complete manual reading / access checklist

**Статус:** `EVERGREEN-ACCESS-CHECKLIST / NAVIGATION-ONLY / MANUAL-READING / PARALLEL-BRANCH-RECONCILED / TERMINAL-HOLD-REOPEN-MAP / RESEARCH-ONLY / PUBLICATION-HOLD`  
**Последнее обновление:** 2026-08-14

## 0. Purpose / authority

This file answers one practical question:

> If a human researcher obtains library, institutional, purchased, local-PDF or renderable-scan access, exactly what still deserves direct reading or visual autopsy, where is it, and what should be extracted?

This is **not** an evidence owner and does not make the current audit incomplete. Claim grades live in the current claim registry; evidence lives in the controlling evergreen dossiers.

```text
ENGLISH_KNOWN_ROUTE_AUDIT = DISPOSITION_COMPLETE
MULTILINGUAL_KNOWN_ROUTE_SWEEP = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
REGIONAL_KNOWN_ROUTE_SWEEP = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
PARALLEL_BRANCH_HARVEST = RECONCILED_COMPLETE
THIS_FILE = HUMAN_MANUAL_ACCESS_REOPEN_MAP
THIS_FILE != ACTIVE_AGENT_ACQUISITION_QUEUE
TERMINAL_HOLD != VERIFIED_BODY
TERMINAL_HOLD != NEGATIVE_EVIDENCE
AGENT_BRANCH_CLOSED_DIRECT != TARGET_VERIFIED_BODY
READING_ONE_ITEM != AUTOMATIC_GRADE_CHANGE
```

After any item is acquired/read:

```text
1. update the controlling evergreen owner;
2. reassess only affected claims;
3. update this checklist status;
4. do not reopen unrelated research.
```

Priority meanings:

```text
M0 = highest-value current commentary / whole-model body
M1 = important specialist/source-control body
M2 = primary object / scan / dataset autopsy
M3 = optional nonblocking completeness / edition comparison
```

Status meanings:

```text
BODY_OPEN = body still deserves direct reading
PARTIAL = some direct/official control exists; specified remainder still open
CLAIM_CLOSED_IMAGE_OPTIONAL = substantive claim is closed; only image/printed-page custody remains
CLOSED_FOR_CLAIM = no substantive reacquisition needed unless a new source-specific reason appears
OPTIONAL = nonblocking completeness/model stress only
```

---

# 0.1 Parallel-agent reconciliation firewall

The branch `arena/019fed70-research` supplied useful discovery leads but is **not** an authority layer. Its unique delta was limited to four evergreen/checklist files. Three controlling owners have already been reconciled independently (`EXOUSIA`, `RITUAL`, `QUOTATION`); this file is the fourth.

Concrete reasons not to copy arena statuses blindly:

```text
ARENA_NISYRA = claimed restored prophetis in SEG49.1624
TARGET_DIRECT_PHI_CONTROL = no prophetis in target indexed text
RESULT = ARENA_REVERSAL_REJECTED

ARENA_BGU7_1655 = simple APO+GEN label
TARGET_DIRECT_EDITION = APO/EX apparatus complication
RESULT = DATASET_NORMALIZATION_CANNOT_REPLACE_CRITICAL_APPARATUS

ARENA_KOWALSKI = cross-file full-body/read-status mismatch
TARGET = official KUL item + official APCZ OA article/PDF-galley route closed, full body still render hold
```

Independently verified branch deltas already migrated to owners:

```text
APPHE_IK61_DIRECT_PHI_BODY = CLOSED_DIRECT
APPHE_PROPHET_WIFE_READING_FROM_THIS_INSCRIPTION = NOT_SUPPORTED
TERMESSOS_TAMIII1_870_DIRECT_PHI_INDEXED_BODY = CLOSED_DIRECT
TERMESSOS_870_FEMALE_PROPHETIS_NOUN_BEARER = CLOSED_DIRECT
POTTA_TAM_V1_535_DIRECT_PHI_INDEXED_BODY = CLOSED_DIRECT
POTTA_TAM_V1_535_FEMALE_PROPHETIS_NOUN_BEARER = CLOSED_DIRECT
P_WISC_I_13_EXOUSIA_LEXEME = FULLY_EDITORIALLY_RESTORED_IN_TARGET_FORMULA
P_OXY_8_1120 = KATA_PLUS_GENITIVE_CONTROL
P_OXY_9_1205 = EIS_PLUS_ACCUSATIVE_DIRECT_DDBDP
BGU_7_1655 = EXOUSIA_ECHEIN_DIRECT / APO_VS_EK_APPARATUS_CAUTION
FENDEL_PUBLISHED_CORPUS_BODY = CLOSED_DIRECT_WILEY
FENDEL_THREE_REPORTED_PP_DOCUMENTS = INDEPENDENTLY_CONTROLLED_AT_DOCUMENT_LEVEL
FENDEL_XLSX_BINARY_TARGET_READ = NO_OPTIONAL_REPRODUCIBILITY_CUSTODY
COSTA_FULL_OFFICIAL_UFMG_PDF = CLOSED_DIRECT
KOWALSKI_KUL_ITEM_AND_PDF_FILE_OBJECT = CLOSED_INSTITUTIONAL
KOWALSKI_APCZ_OFFICIAL_ARTICLE_AND_EXACT_PDF_GALLEY_ROUTE = CLOSED_OFFICIAL_OA_ROUTE / BODY_NOT_RENDERED
HUGHES_2007_FULL_PUBLISHED_BODY = CLOSED_DIRECT_AUTHOR_PROFILE
HUGHES_TABLE1_AND_TABLE2 = CLOSED_DIRECT_BODY
TORBUS_2023_FULL_PUBLISHED_BODY = CLOSED_DIRECT
LI_HAO_2023_FULL_52_PAGE_PDF_TEXT = CLOSED_DIRECT
WANG_2022_AUTHOR_UPLOADED_PUBLISHED_FULL_BODY = CLOSED_DIRECT_AUTHOR_UPLOAD
LABUDA_2019_FULL_OFFICIAL_PDF_TEXT = CLOSED_DIRECT
GATUMU_2020_FULL_OFFICIAL_OJS_PDF_TEXT = CLOSED_DIRECT
MCGINN_1996_AUTHOR_PROFILE_RENDERED_PUBLISHED_BODY = CLOSED_DIRECT
PARK_1990_OFFICIAL_JSTAGE_FULL_BODY = CLOSED_DIRECT_TEXT_LAYER
```

---

# 1. M0 — current technical commentaries and major whole-models

## 1. Mark Reasoner, *1 Corinthians* (Brill, 2025)

**Read:** Commentary 7, “Hair and Head Coverings in the Assembly (11:2–16),” approx. pp.432–451 + notes.  
**Where:** Brill BEC Series 3; official book/chapter TOC; Google Books limited preview / institutional access.  
**Extract:** veil vs hair; `κεφαλή`; v10 `ἐξουσία`; angels; `φύσις`; v16; trigger; authenticate circulated p.434/p.444 wording.

```text
STATUS = PARTIAL
CLOSED = BOOK_AND_COMMENTARY7_IDENTITY
OPEN = RICH_PREVIEW_REPRODUCTION + FULL_BODY_AND_NOTES
```

## 2. David E. Garland, *1 Corinthians*, BECNT 2nd ed. (2025)

**Read:** complete “VII. Headdress in Public Worship (11:2–16)” + notes; first record actual 2025 pagination.  
**Where:** Baker Academic / Logos / Perlego / institutional ebook; ISBN 9781540962607; ebook 9781493451692.  
**Extract:** every change from 2003; veil/hair; `κεφαλή`; `ἐξουσία`; angels; nature/custom; trigger.

```text
STATUS = BODY_OPEN
CLOSED = SECTION_IDENTITY
OPEN = 2025_PAGINATION + BODY + NOTES
DO_NOT_TRANSFER_2003_PAGINATION = true
```

## 3. Gordon D. Fee, NICNT Revised Edition (2014)

**Read:** pp.542–586 + notes; highest value pp.550–564, 565–566 Addendum, 567–579, especially pp.576–578 / p.576 n.123, and pp.580–586.  
**Where:** Eerdmans / Logos-Biblia `NICNT67CO1_2ED` / institutional ebook.  
**Extract:** revised wording vs 1987; v10; angels/Watchers; material practice; vv13–16.

```text
STATUS = BODY_OPEN
CLOSED = EXACT_REVISED_RANGES
OPEN = REVISED_2014_BODY_AND_NOTES
```

## 4. Anthony C. Thiselton, NIGTC (2000)

**Read:** pp.800–847 + notes.  
**Where:** NIGTC/Eerdmans / institutional library / lawful preview.  
**Extract:** material reconstruction; `κεφαλή`; `ἐξουσία`; angels; `φύσις`; v16; rhetoric.

Independent locator architecture is now controlled:

```text
P800 = mutuality/reciprocity 11:2-16
P812 = kephale meanings
P823 = 11:4
P828 = 11:5-6
P834 = 11:7-9
P838 = exousia 11:10
P844 = physis 11:14
P848 = next section
```

```text
STATUS = PARTIAL
CLOSED = TARGET_SECTION_ARCHITECTURE
OPEN = COMPLETE_BODY_WORDING + NOTES
```

## 5. Roy E. Ciampa & Brian S. Rosner, PNTC (2010)

**Read:** pp.503–540 + notes.  
**Where:** Eerdmans / institutional ebook / IxTheo licensed/ILL route / Google Books record.  
**Extract:** whole model; veil/hair; hierarchy/interdependence; v10; angels; nature/custom; v16.

```text
STATUS = BODY_OPEN
CLOSED = WORK_AND_RANGE
OPEN = DETAIL_BODY_AND_NOTES
```

## 6. David I. Starling, EBTC (2025)

**Read:** exact 1 Cor 11:2–16 exposition + notes.  
**Where:** Lexham Academic / Logos / Biblia embedded preview.  
**Extract:** veil/hair; creation; `κεφαλή`; v10; angels; nature/custom; synthesis.

```text
STATUS = BODY_OPEN
CLOSED = BOOK + PREVIEW/TOC_ROUTE
OPEN = TARGET_SECTION_BODY
```

## 7. Michael J. Gorman, *1 Corinthians* (Eerdmans, 2025)

**Read:** exact 1 Cor 11:2–16 section.  
**Where:** Eerdmans / licensed ebook / Libby-OverDrive / institutional access; ISBN 9780802882660; ebook 9781467465748.  
**Extract:** technical claims only where actual body makes them.

```text
STATUS = BODY_OPEN
CLOSED = BOOK_IDENTITY + LIBBY_OVERDRIVE_ROUTE
OPEN = TARGET_SECTION_BODY
```

## 8. Susanna Drake, *Veiling in the Late Antique World* (CUP, 2025)

**Read first:** ch.2 “Veils in Corinth,” pp.70–89 + notes; also relevant ch.1 material on material forms and transition from outer-garment covering to later separate/tighter veils.  
**Where:** Cambridge Core; book DOI `10.1017/9781009673518`; ch.2 DOI `10.1017/9781009673518.003`.  
**Extract:** exact garment/material claims; v10/angels/hair/`κεφαλή`; body vs summary/interview claims.

```text
STATUS = BODY_OPEN
CLOSED = CH2_IDENTITY + PAGINATION + OFFICIAL_SUMMARY
OPEN = FULL_CH1_2_BODY_AND_NOTES
```

## 9. Aldar Nõmmik, *Robes, Romans, and Rituals in First Corinthians*

**Read:** ideally complete dissertation/book, especially 1 Cor 11, Roman `capite velato`, ritual cognition/divine knowledge, v10, angels, creation, nature/custom.  
**Where:** EHS/DiVA institutional object, URN `urn:nbn:se:ths:diva-2600`; Wipf & Stock edition; direct EHS dissertation interview/summary; Google Books limited preview.  
**Extract:** complete primary-evidence chain and page-level argument behind the capite-velato / ritual-uniformity reconstruction, especially where the full body qualifies the direct author self-description.

The EHS dissertation page now directly controls Nõmmik's own description of the model: `capite velato` is central; he frames Paul as handling Corinthian counterarguments/new practices; and the institutional summary explicitly reports his ritual-uniformity, prayer-efficacy/divine-knowledge and male/female head-state reconstruction. This is substantive author-model provenance, not full dissertation body.

```text
STATUS = PARTIAL
CLOSED = INSTITUTIONAL_OBJECT + FULLTEXT_ROUTE_IDENTITY + DIRECT_EHS_AUTHOR_SELF_DESCRIPTION + GOOGLE_BOOKS_LIMITED_PREVIEW_ARCHITECTURE
OPEN = FULL_BODY_RENDER + PAGE_LEVEL_EVIDENTIAL_CHAIN + EDITION_PINNED_LOCATORS
DIRECT_AUTHOR_SELF_DESCRIPTION != FULL_DISSERTATION_BODY
```

## 10. Janelle Peters, *Paul and the Citizen Body* (Mohr Siebeck, 2025)

**Read:** ideally complete 183-page monograph; minimum all 1 Cor 11 sections.  
**Where:** Mohr Siebeck, WUNT II 625; DOI `10.1628/978-3-16-160164-4`; lawful preview/library.  
**Extract:** bodily/head control; citizenship/status; creation; slavery; `ἐξουσία`; angels; material veiling.

```text
STATUS = PARTIAL
CLOSED = PUBLISHER_MODEL + TOC + PREVIEW_LEVEL_CONTROLS
OPEN = FULL_MONOGRAPH
```

## 11. Jorunn Økland, *Women in Their Place* (2004/2005)

**Read:** chs.4–7: ch4 p.78; ch5 p.131; ch6 p.168; ch7 p.224.  
**Where:** Bloomsbury/T&T Clark ebook/library; Google Books preview.  
**Extract:** veil vs hair; `κεφαλή`; `ἐξουσία`; angels; `φύσις`; v16; sanctuary-space trigger.

```text
STATUS = PARTIAL
CLOSED = IDENTITY + TOC + PREVIEW_LEVEL_CONTROL
OPEN = CONTIGUOUS_CH4_7_BODY
```

---

# 2. M1 — specialist articles / chapters / visual-social controls

## 12. David A. deSilva, *Archaeology and the Ministry of Paul* (2025)

**Read:** pp.126–156, “Roman Corinth.”  
**Where:** Baker Academic / institutional access.  
**Extract:** whether he actually discusses 1 Cor 11, S1116, S1088, Julian Basilica, `capite velato`, women's covering.

```text
STATUS = PARTIAL
CLOSED = CHAPTER_RANGE + PREVIEW_NEGATIVE_CONTROL
OPEN = COMPLETE_CHAPTER_BODY
```

## 13. Barbara Lumesberger-Loisl (2025)

**Read:** “Kopftuchgebot für Christinnen?... (1 Kor 11,2–16),” pp.295–303.  
**Where:** IxTheo / Katholisches Bibelwerk book/library; official TOC.  
**Extract:** exact material reconstruction and gender-difference argument.

```text
STATUS = BODY_OPEN
CLOSED = BIBLIOGRAPHY + EXACT_PAGES
OPEN = CHAPTER_BODY
```

## 14. Judith M. Gundry-Volf (1997)

**Read:** “Gender and Creation in 1 Corinthians 11:2–16,” pp.151–171.  
**Where:** *Evangelium, Schriftauslegung, Kirche* / institutional library / ILL.  
**Priority:** p151 n1; p152; pp154–155; pp162–163; p164.

```text
STATUS = BODY_OPEN
CLOSED = BIBLIOGRAPHY + PAGE_LOCATORS
OPEN = DIRECT_BODY
```

## 15. Marlis Gielen (1999)

**Read:** *ZNW* 90.3–4, pp.220–249; compare 2009 reworking if available.  
**Where:** De Gruyter/ZNW / institutional library.  
**Extract:** modified short-hair reconstruction; sex-role symbolism; later changes.

```text
STATUS = BODY_OPEN
CLOSED = ARTICLE_IDENTITY + MODEL_LOCATORS
OPEN = 1999_BODY + OPTIONAL_2009_COMPARISON
```

## 16. Hao Li (2023)

**Read:** Chinese article pp.267–318.  
**Where:** official JRCC, DOI `10.29635/JRCC.202312_(21).0012`; founding-center institutional PDF route.  
**Extract:** creation order; reciprocity; veil/hair; v10; angels; cultural adaptation/challenge.

The complete 52-page PDF text has now been read and absorbed into the retained Chinese-scholarship owner. Selected page-image screenshot attempts failed at runtime, so only image custody remains optional.

```text
STATUS = CLOSED_FOR_CLAIM
CLOSED = OFFICIAL_OBJECT + FULL_52_PAGE_PDF_TEXT + BODY_LEVEL_MODEL
OPTIONAL = PAGE_IMAGE_AUTOPSY_IF_RENDERER_RECOVERS
```

## 17. Janelle Peters, *Biblica* 2020

**Read:** “Slavery and the Gendered Construction of Worship Veils in 1 Corinthians,” pp.431–443.  
**Where:** Peeters / JSTOR 48653612 / DOI `10.2143/BIB.101.3.3288730`.  
**Extract:** slavery/status mechanism; primary evidence; verse chain.

A 2021 Michael Bird post points to the exact historical author-copy Academia URL, but that exact Peters page now returns 404. Bird reproduces the article's conclusion and confirms the broad equality/status direction, yet that secondary quotation is not a substitute for the full body.

```text
STATUS = BODY_OPEN
CLOSED = PUBLISHER_ABSTRACT + HISTORICAL_EXACT_AUTHOR_COPY_PROVENANCE_TRACE
OPEN = FULL_BODY
OLD_AUTHOR_COPY_URL = CURRENTLY_404
```

## 18. Janelle Peters dissertation (Emory, 2013)

**Read:** preferably chs.6–7; minimum p.282. TOC: ch6 p.228; ch7 p.264; conclusion p.301.  
**Where:** Emory OA object `qr46r105v`, Primary PDF.  
**Extract:** p282 Corinth statue/object identity and actual claim.

```text
STATUS = BODY_OPEN
CLOSED = INSTITUTIONAL_OBJECT + TOC + OPEN_ACCESS_RIGHTS_ROUTE
OPEN = CH6_7 + P282_DIRECT
```

## 19. L. J. Lietaert Peerbolte (2000)

**Read:** “Man, Woman, and the Angels in 1 Cor 11:2–16,” pp.76–92, esp.86–87.  
**Where:** Brill chapter.  
**Extract:** Watchers/Enochic argument; `ἐξουσία`; exact wording.

```text
STATUS = PARTIAL
CLOSED = CHAPTER_IDENTITY + PREVIEW/LOCATOR_CONTROL
OPEN = COMPLETE_DIRECT_BODY
```

## 20. Charles H. Cosgrove (2005)

**Read:** JBL 124.4, pp.675–692.  
**Where:** JSTOR 30041064; DOI `10.2307/30041064`.  
**Extract:** evidence for genuinely unbound/dishevelled female hair; separate from Andania `ἀναπλέκω`.

```text
STATUS = BODY_OPEN
CLOSED = BIBLIOGRAPHY + JSTOR_XML_ENDPOINT_IDENTITY
OPEN = FULL_BODY_XML_OR_PDF
```

## 21. Gail Paterson Corrington (1991)

**Read:** *Perspectives in Religious Studies* 18.3, pp.223–231.  
**Where:** Baylor/PRSt holdings / ILL.  
**Extract:** body/head semantics and visual/social evidence.

```text
STATUS = BODY_OPEN
CLOSED = IDENTITY + PAGES
OPEN = DIRECT_FULLTEXT
```

## 22. Elaine Fantham (2008)

**Read:** “Covering the Head at Rome: Ritual and Gender,” pp.158–171.  
**Where:** *Roman Dress and the Fabrics of Roman Culture* / institutional ebook; DOI `10.3138/9781442689039-012`.  
**Extract:** male/female ritual covering distinctions; status; chronology.

```text
STATUS = PARTIAL
CLOSED = IDENTITY + LOCATOR + SECONDARY/PREVIEW_DIRECTION
OPEN = COMPLETE_DIRECT_BODY / EXACT_ARENA_PREVIEW_WORDING_REPRODUCTION
```

## 23. Kelly Olson, *Dress and the Roman Woman* (2008)

**Read:** at minimum pp.22, 25, 34, 41 contexts; ideally palla/stola/togata chapters.  
**Where:** Routledge institutional ebook.  
**Extract:** palla/head-cover frequency; literary ideal vs visual practice; status vocabulary.

```text
STATUS = PARTIAL
CLOSED = BOOK + PAGE_LOCATORS + STRONG_REVIEW_CONTROL
OPEN = COMPLETE_DIRECT_BODY / EXACT_ARENA_PREVIEW_WORDING_REPRODUCTION
```

## 24. Lisa A. Hughes (2007)

The complete published body is now directly controlled through Lisa Hughes's University of Calgary author profile / linked Academia paper page, in addition to Taylor & Francis article identity.

Direct body includes:
- Table 1 p.227: `N=113`, `67 veiled (59%)`, `46 unveiled (41%)`;
- Table 2 inscription-preservation split;
- sample/preservation/cost methodology;
- direct evidence that respectable married freedwomen/matronae can be represented unveiled;
- explicit rejection of one universal status-veiling rule.

```text
STATUS = CLOSED_FOR_CLAIM
CLOSED = DIRECT_AUTHOR_PROFILE_FULL_PUBLISHED_BODY + TABLE1 + TABLE2 + METHODOLOGY + CONCLUSION
OPTIONAL = TAYLOR_FRANCIS_PUBLISHER_PDF_BYTE_OR_PAGE_IMAGE_CUSTODY
```

## 25. Marcin Kowalski (2020)

**Read:** full pp.59–104.  
**Where:** official APCZ publisher + KUL repository; DOI `10.12775/BPTh.2020.003`.  
**Already controlled:** official APCZ article page, exact OA PDF-galley action/link id `25039`, KUL institutional item + PDF file object, and abstract macrostructure (v2 intro; v3 Pauline thesis; vv4–6 cultural; vv7–12 Christological/theological; vv13–15 natural-law argument).

A distinct author-upload route also exists for Kowalski's later 2022 chapter on changing gender roles and 1 Cor 11, but its attachment binary still does not render in the current runtime. Do not substitute route existence for body reading.

```text
STATUS = PARTIAL
CLOSED = APCZ_OFFICIAL_ARTICLE_PAGE + EXACT_OA_PDF_GALLEY_ROUTE_25039 + KUL_ITEM + KUL_PDF_FILE_OBJECT + CONTINUOUS_PAULINE_ABSTRACT_STRUCTURE + AUTHOR_2022_DOWNLOAD_ROUTE_IDENTITY
OPEN = FULL_2020_PDF_BODY_RENDER + RENDERABLE_AUTHOR_2022_BODY + V10_ANGELS_DETAIL
OFFICIAL_PDF_GALLEY_ROUTE != BODY_READ
```

## 26. Sławomir Torbus — 2009 historical chapter / 2023 direct continuity body

Torbus 2009, “The Rhetorical Dispositio of 1 Cor. 11, 2–16 and the Problem of the Veil,” pp.507–521, remains useful only for exact historical/edition comparison.

A materially stronger direct source now closes Torbus's substantive later position: his complete 2023 University of Wrocław / *Quaestiones Oralitatis* article, “Is 1 Corinthians 11:3b–15 an Interpolation?”, pp.41–53, is directly read under CC BY 4.0. It argues a coherent continuous 1 Cor 11:2–14:40 macrostructure, rejects interpolation, and directly reads v10 as the woman having control/right regarding her own head, while the proposed social mechanism remains reconstruction-layer.

```text
STATUS = OPTIONAL
CLOSED = TORBUS_2023_DIRECT_FULL_PUBLISHED_BODY + CONTINUITY_MODEL + V10_ACTIVE_WOMAN_CONTROL
OPTIONAL = TORBUS_2009_PP507_521_HISTORICAL_EDITION_COMPARISON
```

## 27. Peter Arzt-Grabner et al., PKNT 2 (2006)

**Read:** p.390 + surrounding paragraph/notes.  
**Where:** institutional theological library / publisher ebook.  
**Verify:** exact “uncommon” claim for `ἐξουσία + ἐπί + genitive` and corpus basis.

```text
STATUS = BODY_OPEN_NONBLOCKING
CLOSED = PAGE_LOCATOR
OPEN = DIRECT_P390
```

---

# 3. M2 — primary scans, datasets and epigraphic objects

## 28. Fendel 2023 — `EXOUSIAN.xlsx`

The actual Oxford spreadsheet binary `EXOUSIAN.xlsx` (51.7 KB) remains unopened in the current runtime, but it is no longer a substantive evidence blocker.

Why: Fendel's complete Wiley article is directly read and publishes the systematic corpus result (`272` documents, `290` `ἐξουσίαν` tokens, `190` `ἐξουσίαν ἔχω` instances plus complement distributions), and the three reported Roman-period PP documents have independently been checked at document level:

```text
P_OXY_8_1120 = KATA + GENITIVE
P_OXY_9_1205 = EIS + ACCUSATIVE / DIRECT_DDBDP
BGU_7_1655 = EXOUSIA_ECHEIN_DIRECT / APO_VS_EK_CRITICAL_APPARATUS_COMPLEXITY
NO_EPI_GENITIVE_AMONG_THE_THREE_DOCUMENT_LEVEL_CONTROLS = TRUE
```

```text
STATUS = CLOSED_FOR_CLAIM
CLOSED = DIRECT_WILEY_PUBLISHED_CORPUS + DATASET_OBJECT + FILE_IDENTITY + THREE_UNDERLYING_DOCUMENTS_AT_DOCUMENT_LEVEL
OPTIONAL = XLSX_BINARY_EXACT_ROW_NORMALIZATION_FOR_REPRODUCIBILITY
DO_NOT_CLAIM_XLSX_TARGET_READ = true
```

## 29. PG 118 — direct scan image p.409

The OCR locator and original public-domain scan object are closed. The target p.409 image remains a transport-only custody issue; the patristic scan owner has already terminalized the current route.

```text
STATUS = CLAIM_CLOSED_IMAGE_OPTIONAL
CLOSED = ORIGINAL_SCAN_OBJECT + OCR_LOCATOR + TARGET_PDF_PAGE_409
OPTIONAL = TARGET_PAGE_IMAGE_AUTOPSY_IF_NEW_RENDERABLE_ROUTE_APPEARS
```

## 30. Cyril of Alexandria — PG 74 cols.879–883

The original public-domain PG74 scan object and exact target columns are closed. PG74 is not in the current 2026 OCR corpus; current Commons binary transport cannot render the target page.

```text
STATUS = CLAIM_CLOSED_IMAGE_OPTIONAL
CLOSED = WORK + TARGET_COLUMNS_879_883 + ORIGINAL_SCAN_OBJECT
OPTIONAL = TARGET_IMAGE_AUTOPSY_IF_NEW_RENDERABLE_ROUTE_APPEARS
```

## 31. Theodoret — PG 82 cols.312D–313A

The standalone commentary range, target columns and original public-domain PG82 object are closed; Hill p.205 remains a modern-translation comparison route if accessible.

```text
STATUS = CLAIM_CLOSED_IMAGE_OPTIONAL
CLOSED = WORK + TARGET_COLUMNS_312D_313A + ORIGINAL_SCAN_OBJECT + STRONG_TWO_ROUTE_PAGE_LOCATOR
OPTIONAL = PG_IMAGE_AUTOPSY + HILL_P205_IF_NEW_ACCESS
```

## 32. Potta — TAM V.1 535 / PH263959

The first-party PHI Greek Inscriptions search surface now independently returns `TAM V,1 535`, Lydia: Maionia, and directly prints the formerly missing middle text:

```text
τῆς ἐκ τοῦ Διὸς
Ποτταν Μενε[κ]ρ̣ά̣-
του προφῆτιν σώ-
τειραν γενομένην
```

This closes Potta as the female `προφῆτις` noun-bearer and closes the `σώτειρα` wording at direct first-party indexed-text level. The exact object-page render / printed page remains optional custody only; it is no longer a substantive text blocker. The laurel-motif monument control remains separate from any neighboring veiled figure.

```text
STATUS = CLOSED_FOR_CLAIM
CLOSED = DIRECT_PHI_INDEXED_TARGET_BODY + FEMALE_PROPHETIS_NOUN_BEARER + SOTEIRA_WORDING + OBJECT_IDENTITY
OPTIONAL = DIRECT_OBJECT_PAGE_RENDER / PRINTED_PAGE_IMAGE / MONUMENT_CUSTODY
```

## 33. Nanas — same-object artifact image

Poirier's official University of Cologne PDF body and the printed page containing the complete edited inscription are now directly closed. The printed inscription contains no head/hair/veil wording. This does **not** substitute for visual inspection of the stone itself; Poirier points to Tabbernee fig.77 for the same-object artifact/image control.

```text
STATUS = CLAIM_CLOSED_IMAGE_OPTIONAL
CLOSED = POIRIER_OFFICIAL_PDF_BODY + COMPLETE_INSCRIPTION_PRINTED_PAGE_AUTOPSY + TEXTUAL_NO_HEAD_HAIR_WORDING
OPEN = TABBERNEE_FIG77_SAME_OBJECT_ARTIFACT_IMAGE_ONLY
PRINTED_TEXT_PAGE_AUTOPSY != SAME_OBJECT_ARTIFACT_IMAGE
```

## 34. Apphe — IK Kalchedon 61 = CIG 3796

**Substantive text claim is now closed directly from PHI.**  
Primary PHI text: `Ὀρβανίλλα, θρεπτὴ Ἄπφης προφήτιδος...`.

```text
APPHE_IS_PROPHETIS_NOUN_BEARER = CLOSED_DIRECT
APPHE_PROPHET_WIFE_READING_FROM_THIS_TEXT = NOT_SUPPORTED
APPHE_FORMAL_INDEPENDENT_ORACLE_OFFICE = STILL_INTERPRETIVE_B_C
```

Original printed CIG/IK page is now only an optional image/edition-custody check.

```text
STATUS = CLAIM_CLOSED_IMAGE_OPTIONAL
OPEN = PRINTED_PAGE_IMAGE_ONLY
```

## 35. Termessos — TAM III,1 870 / PH280975

The target-workflow PHI search/index now independently returns the target inscription and exact line:

```text
τό(πος) Αὐρ(ηλίας) Ὀρεστι-
ανῆς, ἱ(ερῶν) Ἐλευσι-
νίων προφήτ̣ι̣δ̣ο̣ς̣.
```

This directly closes Aurelia Oresteiane as the female `προφῆτις` noun-bearer in relation to the Eleusinian sacred context. `τόπος` is a place/locus marker and does not by itself prove detailed monument morphology. No head/hair code appears in the checked text.

```text
STATUS = CLOSED_FOR_CLAIM
CLOSED = DIRECT_PHI_INDEXED_TARGET_BODY + FEMALE_PROPHETIS_NOUN_BEARER + ELEUSINIAN_RELATION
OPTIONAL = PRINTED_EDITION_IMAGE / MONUMENT_MORPHOLOGY_CUSTODY
```

## 36. Nisyra — SEG 49.1624 / PH348429 / TM949255

Target-workflow PHI sequence/indexed text confirms the target object and shows the short dedication without `προφῆτις`; arena's claim of restored `διὰ προφή[τιδος]` is rejected. Intended source in Nawotka is unknown; do not guess.

```text
STATUS = CLOSED_FOR_CLAIM
CLOSED = PHI_OBJECT_CROSSWALK + INDEXED_TARGET_TEXT + VERY_LIKELY_REFERENCE_ERROR
OPTIONAL = DIRECT_TARGET_PAGE_IF_RUNTIME_EVER_RENDERS
```

## 37. Philokrateia — CGRN 232 direct page

Object identity and same-object Vollgraff p.445 photograph are already closed; direct CGRN 232 is redundant confirmation only.

```text
STATUS = OPTIONAL
CLOSED = OBJECT_IDENTITY + SAME_OBJECT_PHOTO
OPEN = DIRECT_CGRN232_PAGE_ONLY_IF_ROUTE_RECOVERS
```

## 38. P.Wisc. I 13 — edition image/apparatus

Direct DDBDP text has already closed the important ceiling: the target `ἐξουσίαν` lexeme is wholly inside editorial brackets.

```text
STATUS = CLAIM_CLOSED_IMAGE_OPTIONAL
CLOSED = RESTORATION_CEILING + NO_VISIBLE_SURVIVING_EXOUSIA_LETTERS_IN_PRINTED_FORMULA
OPEN = PAPYRUS/EDITION_IMAGE_AUTOPSY_ONLY
```

---

# 4. M3 — optional completeness / model stress

## 39. Cramer printed catena label image

**Inspect:** printed Cramer vol.5 page around digital `Κυτίλλου` / angel block.  
**Purpose:** printed-vs-digital transcription custody; fragment convergence already strongly identifies Cyril.

```text
STATUS = OPTIONAL
```

## 40. Martin 2013 — later PDF page screenshots

Substantive text/body already read; only visual/page-image custody remains.

```text
STATUS = OPTIONAL / FULL_TEXT_BODY_ALREADY_CLOSED
```

## 41. Nicole Francis 2023/24 — full PDF

**Read if easy:** “A Pauline Dress Code or a Roman Analogy...”  
**Where:** BYU ScholarsArchive.  
**Purpose:** full stress-test of Roman-analogy/not-primary-dress-code model.

```text
STATUS = OPTIONAL_PARTIAL
CLOSED = OFFICIAL_OBJECT + ABSTRACT_MODEL
OPEN = FULL_PDF_BODY
```

## 42. Garland first edition (2003) — edition comparison only

**Read only alongside 2025 edition:** pp.505–532.  
**Purpose:** identify actual 2025 changes; never substitute 2003 pages/text for 2025.

```text
STATUS = OPTIONAL
```

## 43. Low-weight current edge/reception full bodies

### Odewole 2025

Israel O. O. Odewole, “FEMINIST AGENDA: Paul’s View of Women in 1 Corinthians 11:2–16,” *QUAERENS* 7.1 (2025): 18–33, DOI `10.46362/quaerens.v7i1.240`.

The official journal page controls identity, DOI, pages and CC BY-NC-SA 4.0; a matching public full journal-layout text now exposes pp.18–33 through the conclusion and references.

```text
STATUS = CLOSED_FOR_CLAIM
CLOSED = OFFICIAL_JOURNAL_IDENTITY + MATCHING_PUBLIC_FULL_PUBLISHED_BODY
WEIGHT = P3_CURRENT_RECEPTION / D_C_LOW_FOR_CORE_CLAIMS
CORE_GRADE_CHANGE = NONE
```

### Garwood 2026

Jason Garwood, *Paul & the Head Covering: A Biblical Reassessment* (2026) — confessional/non-universalist edge model.

```text
STATUS = OPTIONAL_LOW_WEIGHT_CURRENT_RECEPTION
FULL_BODY_CLOSURE = NOT_ASSUMED
```

---

# 5. Directly closed sources — do NOT reacquire merely for repetition

```text
DIDYMA_III7_2023_FULL_BODY = CLOSED_DIRECT_OFFICIAL
TRYPHOSA_N708_BODY_AND_TAF18 = CLOSED_DIRECT_OFFICIAL
DIDYMA_235B_FALSE_OLD_READING = CLOSED
DIDYMA_273_EXEMPLI_GRATIA_RESTORATION = CLOSED
PHILOKRATEIA_VOLLGRAFF_1909_P445_PHOTO = CLOSED_DIRECT_IMAGE
ERESOS_IG_XII_SUPPL_126 = CLOSED_DIRECT
IGVII_3111_BODY = CLOSED_DIRECT_IGVII
IGLSYR_1_51 = CLOSED_DIRECT_FALSE_PERSON_CONTROL
MILETOS_481 = CLOSED_DIRECT
AMMIAS_THYATEIRA = CLOSED_DIRECT
APPHE_IK61_TEXT = CLOSED_DIRECT_PHI
TERMESSOS_TAMIII1_870_BODY = CLOSED_DIRECT_PHI_INDEXED_TARGET
POTTA_TAM_V1_535_BODY = CLOSED_DIRECT_PHI_INDEXED_TARGET
NISYRA_SEG49_1624_REFERENCE_ERROR_CONTROL = CLOSED_FOR_CURRENT_CLAIM
P_WISC_I_13_RESTORATION_CEILING = CLOSED_DIRECT_DDBDP
P_OXY_8_1120_CONSTRUCTION = CLOSED_DOCUMENTARY_CONTROL
P_OXY_9_1205_CONSTRUCTION = CLOSED_DIRECT_DDBDP
PETERS_2021_OPEN_THEOLOGY = CLOSED_DIRECT_FULLTEXT
HAMPLOVA_2025 = CLOSED_DIRECT_INSTITUTIONAL_FULLTEXT
SALES_2024 = CLOSED_OPEN_FULLTEXT
COSTA_2023_2024 = CLOSED_DIRECT_FULL_OFFICIAL_UFMG_PDF
ROMEROWSKI_2006 = CLOSED_DIRECT_AUTHOR_HOSTED_FULL_PDF
STAFFORD_2024 = CLOSED_DIRECT_OXFORD
HUGHES_2007_FULL_PUBLISHED_BODY = CLOSED_DIRECT_AUTHOR_PROFILE
HUGHES_TABLE1_TABLE2_METHOD = CLOSED_DIRECT_BODY
THOMPSON_1988 = CLOSED_DIRECT_PUBLISHER_CONTROL
GILL_1990 = CLOSED_DIRECT_OPEN
ASCSA_CORINTH_XXII_OBJECT_CONTEXT = CLOSED_CURRENT_ASSEMBLAGE_CONTROL
GOODACRE_2011 = CLOSED_DIRECT_FULL_BODY
MARTIN_2013 = CLOSED_DIRECT_TEXT_BODY
HILTON_MATTHEWS_2008 = CLOSED_DIRECT_UKZN_PDF
FENDEL_2023_ARTICLE_BODY_AND_CORPUS_COUNTS = CLOSED_DIRECT
FENDEL_XLSX = OPTIONAL_ROW_REPRODUCIBILITY_ONLY
TORBUS_2023_FULL_BODY = CLOSED_DIRECT
PSI_X_1115 = CLOSED_DIRECT
TAM_II_603_604 = CLOSED_DIRECT
LI_HAO_2023_FULL_BODY = CLOSED_DIRECT_52_PAGE_PDF_TEXT
WANG_2022_PUBLISHED_BODY = CLOSED_DIRECT_AUTHOR_UPLOAD
LABUDA_2019_FULL_BODY = CLOSED_DIRECT_OFFICIAL_PDF_TEXT
GATUMU_2020_FULL_BODY = CLOSED_DIRECT_OFFICIAL_OJS_PDF_TEXT
MCGINN_1996 = CLOSED_DIRECT_AUTHOR_PROFILE_RENDERED_PUBLISHED_BODY
PARK_1990 = CLOSED_DIRECT_OFFICIAL_JSTAGE_FULL_BODY
ODEWOLE_2025_FULL_PUBLISHED_BODY = CLOSED_MATCHING_PUBLIC_JOURNAL_LAYOUT / LOW_WEIGHT_CURRENT_RECEPTION
NANAS_POIRIER_2004_OFFICIAL_PDF_BODY = CLOSED_DIRECT_UNIVERSITY_OF_COLOGNE
NANAS_POIRIER_COMPLETE_INSCRIPTION_PRINTED_PAGE_AUTOPSY = CLOSED_VISUAL_TEXT_PAGE
PG118_P409 = SCAN_OBJECT_AND_LOCATOR_CLOSED / IMAGE_OPTIONAL_TRANSPORT
PG74_879_883 = SCAN_OBJECT_AND_COLUMNS_CLOSED / IMAGE_OPTIONAL_TRANSPORT
PG82_312D_313A = SCAN_OBJECT_AND_COLUMNS_CLOSED / IMAGE_OPTIONAL_TRANSPORT
```

---

# 6. Current human reading order

## A. Highest-value commentary bodies

```text
1 Reasoner_2025_full_Commentary7
2 Garland_2025_2e_section_VII
3 Fee_2014_pp542_586_especially_576_n123
4 Thiselton_2000_pp800_847_full_body
5 Ciampa_Rosner_2010_pp503_540
6 Drake_2025_ch1_2
7 Nommik_fulltext
8 Peters_2025_full_monograph
9 Starling_2025_1Cor11
10 Gorman_2025_1Cor11
11 Okland_ch4_7
```

## B. Highest-value remaining source/body reopen priorities

```text
P0 REASONER_RICH_PREVIEW_OR_FULL_BODY_REPRODUCTION
P0_P1 KOWALSKI_2020_FULL_PDF_BODY_FROM_ALREADY_CLOSED_OFFICIAL_APCZ_GALLEY_OR_RENDERABLE_AUTHOR_2022_BODY
P1 PETERS_2020_FULL_BODY
P1 PETERS_2013_CH6_7_P282_PRIMARY_PDF
P1 WON_2010_PRIMARY_ARTICLE_AND_THESIS_BODY
P1 VIDOVIC_2024_FULL_CHAPTER_BODY
P1 FRANCIS_FULL_PDF
P2 GUNDRY_VOLF_GIELEN_PEERBOLTE_CORRINGTON_DIRECT_BODIES
P2 FANTHAM_OLSON_EXACT_PAGE_AUTOPSY
```

Removed from the substantive reopen queue because the controlling owners are now closed:

```text
POTTA_TAMV1_535 = CLOSED_DIRECT_PHI_INDEXED_BODY / PRINTED_PAGE_AND_OBJECT_RENDER_OPTIONAL
TERMESSOS_870 = CLOSED_DIRECT_PHI
FENDEL_XLSX = OPTIONAL_REPRODUCIBILITY_CUSTODY_ONLY
HUGHES_2007 = CLOSED_DIRECT_AUTHOR_PROFILE_FULL_BODY
TORBUS_CONTINUITY = CLOSED_DIRECT_TORBUS_2023
PARK_1990 = CLOSED_DIRECT_OFFICIAL_JSTAGE_FULL_BODY
ODEWOLE_2025 = CLOSED_MATCHING_PUBLIC_FULL_PUBLISHED_BODY / LOW_WEIGHT_ONLY
NANAS_POIRIER_PRINTED_PAGE = CLOSED / TABBERNEE_FIG77_ARTIFACT_IMAGE_ONLY_REMAINS
PG118_PG74_PG82_CURRENT_IMAGE_ROUTES = TERMINALIZED_OPTIONAL_CUSTODY
```

Hao Li 2023 and Wang 2022 remain removed from the substantive reading queue because their published bodies are directly closed. Optional page-image/publisher-byte custody does not make them body blockers.

## C. Remaining specialist sequence

```text
12 deSilva_2025
13 Gundry_Volf_1997
14 Gielen_1999
16 Peerbolte_2000
17 Peters_2020
18 Peters_2013_ch6_7_p282
19 Cosgrove_2005
20 Corrington_1991
21 Fantham_Olson
22 Kowalski
23 PKNT_p390
24 Nanas_Tabbernee_fig77_same_object_image_only / Potta_printed_page_optional_only
25 M3_optional_controls
```

---

# 7. Reading-return protocol

For every newly acquired source record:

```text
SOURCE_ID
EDITION_YEAR
PRINT_OR_PDF_PAGINATION
ACCESS_ROUTE
PAGE_RANGE_READ
DIRECT_QUOTE_SAFE = true_or_false
CLAIMS_ACTUALLY_SUPPORTED
CLAIMS_NOT_SUPPORTED
EDITION_DIFFERENCES
IMAGE_AUTOPSY = if_applicable
OWNER_FILE_UPDATED
CLAIM_REGISTRY_CHANGE = yes_or_no
```

A user-provided PDF/photo/scan is a **new lawful access route** and reopens only the matching item.

---

# 8. Final status

```text
TOTAL_CATALOGUED_MANUAL_ITEMS = 43
M0_MAJOR = 11
M1_SPECIALIST = 16
M2_PRIMARY_OBJECT_DATA = 11
M3_OPTIONAL = 5

FORTY_THREE_ITEMS != FORTY_THREE_EQUAL_UNRESOLVED_GAPS
SEVERAL_ITEMS = PARTIAL_OR_CLAIM_CLOSED_IMAGE_OPTIONAL
CURRENT_RESEARCH_AUDIT_READY = true
ENGLISH_KNOWN_ROUTE_AUDIT = DISPOSITION_COMPLETE
MULTILINGUAL_KNOWN_ROUTE_SWEEP = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
REGIONAL_KNOWN_ROUTE_SWEEP = DISPOSITION_COMPLETE_FOR_CURRENT_KNOWN_ROUTES
PARALLEL_BRANCH_HARVEST = RECONCILED_COMPLETE
MANUAL_READING_CAN_STILL_UPGRADE_SOURCE_CUSTODY = true
MANUAL_READING_LIST_RECONCILED_WITH_TARGET_EVERGREEN_OWNERS = true
CORE_GRADE_REVERSALS = 0
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
SITE_PUBLICATION = false
```