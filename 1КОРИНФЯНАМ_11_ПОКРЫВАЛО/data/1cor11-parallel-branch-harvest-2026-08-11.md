# 1 Cor 11:2–16 — parallel branch harvest — 2026-08-11

**Type:** `PROVENANCE-RECEIPT / PARALLEL-AGENT-HARVEST / DISCOVERY-QUARANTINE / NON-AUTHORITY / RESEARCH-ONLY / PUBLICATION-HOLD`

**Source branch inspected:** `arena/019fed70-research`  
**Target integration branch:** `agent/1cor11-citation-quarantine-20260810`

This receipt records only distinct provenance and verification state from parallel-agent harvesting. It does **not** own grades and must never override the controlling evergreen dossiers or claim registry.

```text
AGENT_OUTPUT = DISCOVERY_ONLY
BRANCH_ASSERTION != PRIMARY_SOURCE_VERIFICATION
BRANCH_DIRECT_BODY_LABEL != DIRECT_BODY_UNTIL_INDEPENDENTLY_REOPENED
LIBRARY_HOLDING != BODY_READ
PDF_OBJECT != PDF_BODY_READ
SEARCH_SNIPPET != QUOTE_SAFE_BODY
VERIFY_THEN_UPDATE_EVERGREEN_OWNER = REQUIRED
```

## 1. Branch delta shape

Latest comparison still shows `arena/019fed70-research` with **12 unique commits** relative to the target branch. Its unique content delta remains concentrated in four evergreen files:

```text
dossiers/EXOUSIA_FORMAL_DOCUMENTARY_CORPUS.md
dossiers/MANUAL_READING_ACCESS_CHECKLIST.md
dossiers/QUOTATION_REFUTATION_SPEAKER_BOUNDARY.md
dossiers/RITUAL_DIVINATION_PROPHETIC_HEAD_STATE.md
```

The older `agent/1cor11-arena-d-normalized-20260809` has no unique delta relative to the current target and is historical/behind.

```text
WHOLE_BRANCH_BLIND_MERGE = NO
CHERRY_PICK_UNVERIFIED_AGENT_ASSERTIONS = NO
HARVEST_DELTA_THEN_VERIFY = YES
```

The target branch also contains newer multilingual/regional acquisition work absent from the arena branch, so a wholesale merge would both import unverified reversals and overwrite newer source-control work.

---

# 2. Independently verified branch deltas

## 2.1 Apphe / IK Kalchedon 61 — direct PHI body

Primary PHI:
- https://inscriptions.packhum.org/text/279287

Direct text:

```text
Ὀρβανίλλα,
θρεπτὴ Ἄπφης
προφήτιδος,
ζήσασα ἔτη ζκʹ·
μήτηρ Τυραννίς. ζῇ
```

The genitive apposition `Ἄπφης προφήτιδος` makes Apphe herself the bearer of `προφῆτις`; Orbanilla is her `θρεπτή`.

```text
APPHE_IK61_DIRECT_PHI_BODY = CLOSED_DIRECT
APPHE_PROPHETIS_NOUN_BEARER = A_DIRECT_BODY
APPHE_PROPHET_WIFE_READING_FROM_THIS_INSCRIPTION = NOT_SUPPORTED
APPHE_FORMAL_INDEPENDENT_ORACLE_OFFICE = B_C_AMBIGUOUS
APPHE_HEAD_HAIR_CODE = NOT_ATTESTED
```

The remaining live question is formal office/status, **not** whether this text grammatically calls Apphe a prophet's wife.

## 2.2 Alessandra Castilho da Costa — full official UFMG PDF

Official record/PDF:
- https://periodicos.ufmg.br/index.php/relin/article/view/55158
- https://periodicos.ufmg.br/index.php/relin/article/view/55158/45585
- DOI `10.17851/2237-2083.31.3.1404-1446`

The complete official PDF was independently rendered/read in the target workflow.

```text
COSTA_V3 = PAULINE_POV
COSTA_VV4_9 = CORINTHIAN_POV_QUOTATION_NOT_ENDORSED_BY_PAUL
COSTA_VV10_16 = PAULINE_POV_REFUTATION
COSTA_V10_EXOUSIAN_ECHEIN = ACTIVE_WOMAN_AUTHORITY_READING
COSTA_V14_15 = DECLARATIVE_HAIR_ARGUMENT_IN_AUTHOR_MODEL
COSTA_V16 = DENIAL_OF_CORINTHIAN_COVER_UNCOVER_OBLIGATION_IN_AUTHOR_MODEL
COSTA_FULL_OFFICIAL_PDF = CLOSED_DIRECT
```

This improves attribution and adversarial testing only:

```text
LARGE_QUOTATION_TEXTUAL_FIT = D_C_LOW_UNCHANGED
CORE_GRADE_REVERSALS = 0
```

## 2.3 Nicole Francis 2023 — official institutional model control

Official BYU ScholarsArchive:
- https://scholarsarchive.byu.edu/studiaantiqua/vol22/iss1/6/

The institutional abstract directly verifies her alternative model: the passage is not primarily a standalone prayer/prophecy dress code; Paul uses Roman/social hair and head-covering norms as an analogy within group conflict and hierarchy reasoning.

```text
FRANCIS_2023_OBJECT = CLOSED_DIRECT_INSTITUTIONAL
FRANCIS_ROMAN_ANALOGY_NOT_PRIMARY_DRESS_CODE = CLOSED_DIRECT_ABSTRACT
FRANCIS_PDF_DOWNLOAD_ROUTE = VERIFIED
FRANCIS_FULL_PDF_BODY = CURRENT_RUNTIME_HOLD
```

## 2.4 Hao Li 2023 — official JRCC object/abstract

Official JRCC:
- https://ccspub.cc/jrcc/article/view/38
- DOI `10.29635/JRCC.202312_(21).0012`
- pp.267–318

The official abstract frames the passage as a dialectical combination of culturally embedded subordination language and reciprocal unity/interdependence rather than a timeless absolute principle of female subordination.

```text
HAO_LI_2023_OBJECT = CLOSED_DIRECT_OFFICIAL
HAO_LI_2023_ABSTRACT = CLOSED_DIRECT
HAO_LI_2023_OFFICIAL_CHINESE_PDF_ROUTE = VERIFIED
HAO_LI_2023_FULL_PDF_BODY_IN_TARGET_RUNTIME = NOT_FULLY_RENDERED
```

## 2.5 Nathanael Xuesheng Wang 2022 — new Chinese-route node

Official JRCC:
- https://ccspub.cc/jrcc/article/view/109
- DOI `10.29635/JRCC.202212_(19).0005`
- pp.80–111

The official abstract treats 1 Cor 11 as a veiling instruction during prayer/prophecy while stressing women's worship/ministry participation and social perception of the young church.

```text
WANG_2022_OBJECT = CLOSED_DIRECT_OFFICIAL
WANG_2022_ABSTRACT = CLOSED_DIRECT
WANG_2022_CHINESE_PDF_ROUTE = VERIFIED
WANG_2022_FULL_BODY = NOT_YET_RENDERED_CURRENT_RUNTIME
```

## 2.6 P.Wisc. I 13 — restoration ceiling

Direct DDBDP mirror:
- https://droitromain.univ-grenoble-alpes.fr/Negotia/Wisc1_DDBDP.gr.html

Printed formula begins:

```text
[ἐν ἀγυιᾷ. ἐφ᾽ ὃν μὲν περίειμι χρόνον ἔχειν με τὴν τῶν ἰδίων ἐξουσίαν πᾶσα]ν ...
```

The lexeme `ἐξουσίαν` is wholly within editorial brackets in the relevant formula.

```text
P_WISC_I_13_EXOUSIA_FORMULA = EDITORIAL_RECONSTRUCTION
P_WISC_I_13_EXOUSIA_LEXEME_SURVIVING_LETTERS = NONE_VISIBLE_IN_PRINTED_EDITION
P_WISC_I_13_USE = FORMULA_RESTORATION_CONTROL
P_WISC_I_13_USE_AS_DIRECT_SURVIVING_EXOUSIA_LEXEME = FORBIDDEN
```

## 2.7 P.Oxy. VIII 1120 — `κατά + genitive`

Independent current scholarly control reproduces:

```text
μὴ ἔχων κατ' αὐτῆς ἐξουσίαν
```

```text
P_OXY_8_1120_KATA_GEN_EXOUSIA = CLOSED_DIRECT_PAGE_SPECIFIC_SCHOLARLY_QUOTATION
```

This closes the documentary construction itself; Fendel's exact spreadsheet-row normalization remains a distinct dataset-body claim.

## 2.8 BGU VII 1655 — direct edition + apparatus complication

The Berlin papyrus edition prints the relevant region with `ἀ [[πο]](*)` and gives an apparatus correction `\ἐκ/` at the preposition.

```text
BGU_7_1655_EXOUSIA_ECHEIN = CLOSED_DIRECT_DOCUMENTARY
BGU_7_1655_SIMPLE_APO_GEN_LABEL = NOT_SAFE_AS_UNQUALIFIED_CRITICAL_READING
BGU_7_1655_PREPOSITION = EDITION_APPARATUS_COMPLEXITY_APO_VS_EK
```

Therefore arena's simplified `ἀπό + genitive` label may describe a normalized dataset row, but it cannot be silently substituted for the critical-edition apparatus.

## 2.9 P.Oxy. IX 1205 — `εἰς + accusative` independently CLOSED

Direct DDBDP transcription:
- https://droitromain.univ-grenoble-alpes.fr/Negotia/Oxy43_DDBDP.gr.html
- P.Oxy. IX 1205 = C.Pap.Jud. III 473; 14 April 291 CE.

Direct text contains:

```text
μηδὲ ἓν δίκ[α]ιον μηδεμίαν τε ἐξουσίαν ἔχειν εἰς αὐτοὺς ἀπὸ
[τῆς ἐνεστώσης ἡμέρας ...]
```

```text
P_OXY_9_1205_EXOUSIA_ECHEIN = CLOSED_DIRECT_DDBDP
P_OXY_9_1205_COMPLEMENT = EIS_PLUS_ACCUSATIVE
```

This independently corroborates the third arena-reported Roman-period PP construction at document level.

## 2.10 Fendel `EXOUSIAN.xlsx` — document-level convergence, dataset binary still held

Official Oxford Research Archive dataset:
- https://ora.ox.ac.uk/objects/uuid:28406bed-423d-4801-9691-d5d7caa94e2a
- DOI `10.5287/ora-dqmbwrvj6`
- official file listing: `EXOUSIAN.xlsx`, 51.7 KB.

Arena reports the three Roman-period PP rows as:

```text
BGU.7.1655 = ἀπό + genitive
P.Oxy.8.1120 = κατά + genitive
P.Oxy.9.1205 = εἰς + accusative
```

Target-workflow result:
- P.Oxy. VIII 1120 `κατά + genitive` independently corroborated;
- P.Oxy. IX 1205 `εἰς + accusative` independently corroborated from DDBDP;
- BGU VII 1655 independently closes the `ἐξουσίαν ἕξει` document but exposes an `ἀπό/ἐκ` apparatus complication;
- ORA directly verifies the spreadsheet file object, but the target runtime has **not** independently opened the XLSX binary itself.

```text
FENDEL_ORA_DATASET_OBJECT = CLOSED_OFFICIAL
EXOUSIAN_XLSX_FILE_IDENTITY = CLOSED_OFFICIAL
THREE_REPORTED_ROMAN_PP_DOCUMENTS = INDEPENDENTLY_CORROBORATED_AT_DOCUMENT_LEVEL
NO_EPI_GENITIVE_AMONG_THESE_THREE_DOCUMENT_LEVEL_CONTROLS = TRUE
FENDEL_XLSX_EXACT_ROW_NORMALIZATION = NOT_DIRECTLY_OPENED_IN_TARGET_RUNTIME
BGU_ROW_REQUIRES_APPARATUS_CAUTION = TRUE
```

Do not convert this into `TARGET_READ_XLSX = true` until the actual file body is independently opened.

## 2.11 Nisyra / SEG 49.1624 — arena reversal REJECTED

Arena claimed that PHI object `348429` contained restored `διὰ προφή[τιδος ...]` and that the older reference-error verdict should be reversed.

Independent PHI control does not support that claim. The PHI sequence identifies the target as SEG 49.1624 / PH348429 and the indexed target text is the short dedication:

```text
Θεῷ Βασιλεῖ Διονο[ι— μετὰ τῶν]
ἰδίων πάντων κατ[ὰ ἐπιταγὴν]
```

No `προφῆτις` is present in the indexed target text.

```text
NISYRA_SEG49_1624_PHI_OBJECT = PH348429_CONFIRMED
NISYRA_SEG49_1624_VISIBLE_OR_RESTORED_PROPHETIS = NOT_PRESENT_IN_DIRECT_INDEXED_TEXT
ARENA_NISYRA_RESTORED_PROPHETIS_CLAIM = REJECTED
NISYRA_VERY_LIKELY_REFERENCE_ERROR_IN_NAWOTKA_FN77 = REINSTATED
INTENDED_REFERENCE = UNKNOWN
DO_NOT_GUESS = true
```

This is the clearest demonstration that an agent's `CLOSED_DIRECT` label cannot function as an authority layer.

## 2.12 Kowalski 2020 — second official institutional file route

Official KUL repository independently verifies:
- Marcin Kowalski, “Między darem Bożym a konstruktem społecznym...,” *Biblica et Patristica Thoruniensia* 13.1 (2020): 59–104;
- institutional item and downloadable PDF-file object;
- continuous-Pauline abstract structure.

```text
KOWALSKI_V2 = INTRODUCTION
KOWALSKI_V3 = PAULINE_THESIS
KOWALSKI_V4_6 = CULTURAL_ARGUMENT
KOWALSKI_V7_12 = CHRISTOLOGICAL_THEOLOGICAL_ARGUMENT
KOWALSKI_V13_15 = NATURAL_LAW_ARGUMENT
KOWALSKI_KUL_ITEM = CLOSED_DIRECT_INSTITUTIONAL
KOWALSKI_KUL_PDF_FILE_OBJECT = CLOSED_DIRECT_INSTITUTIONAL
KOWALSKI_FULL_BODY_TARGET_RUNTIME = STILL_RENDER_HOLD
```

The arena checklist's `CLOSED_DIRECT_RUNTIME_OPEN_ACCESS` is therefore **not** copied as a full-body target-workflow state.

## 2.13 Thiselton 2000 — target architecture closed, detailed body still held

Independent preview/search control closes the internal architecture of pp.800–847, including the loci for `κεφαλή`, 11:4, 11:5–6, 11:7–9, `ἐξουσία` 11:10 and `φύσις` 11:14.

```text
THISELTON_TARGET_ARCHITECTURE = CLOSED
THISELTON_ARENA_DETAILED_TRANSLATION_EXCERPTS = PENDING_REPRODUCTION
THISELTON_FULL_TARGET_BODY = NOT_ACQUIRED
```

## 2.14 Reasoner 2025 — official chapter identity, rich preview remains quarantined

Official Brill book TOC confirms:

```text
COMMENTARY_7 = Hair and Head Coverings in the Assembly (11:2–16)
```

The current Brill page exposed by the runtime is a different chapter (`Commentary 4`, pp.238–276), while the book TOC lists Commentary 7. Therefore arena's richer Google-preview body details are not promoted merely from the Brill chapter identity.

```text
REASONER_BOOK_AND_COMMENTARY7_IDENTITY = CLOSED_OFFICIAL
REASONER_RICH_PREVIEW_DETAILS = HIGH_VALUE_ARENA_DISCOVERY_PENDING_REPRODUCTION
REASONER_FULL_BODY = NOT_ACQUIRED
```

## 2.15 Hughes 2007 — exact numerical table control strengthened

Official article:
- Lisa A. Hughes, “Unveiling the Veil: Cultic, Status, and Ethnic Representations of Early Imperial Freedwomen,” *Material Religion* 3.2 (2007): 218–241.
- DOI `10.2752/175183407X219750`.

Direct Hughes Table 1 image has still not been autopsied in the target workflow. However, Grace Stafford's 2024 open-access peer-reviewed article in *Past & Present* gives an exact footnote to **Hughes, table 1, p.227** and reproduces the complete sample/counts:

```text
N = 113 window-type monuments from Italy
VEILED = 67 = 59 percent
UNVEILED = 46 = 41 percent
```

```text
HUGHES_TABLE_1_LOCATOR = CLOSED_PEER_REVIEWED_EXACT_CITATION
HUGHES_N_113 = CLOSED_PEER_REVIEWED_EXACT_CITATION
HUGHES_67_46_COUNTS = CLOSED_PEER_REVIEWED_EXACT_CITATION
HUGHES_59_41_PERCENTAGES = CLOSED_PEER_REVIEWED_EXACT_CITATION
HUGHES_DIRECT_TABLE_IMAGE_AUTOPSY = NOT_YET_CLOSED
```

This is stronger than arithmetic inference, but it remains a later exact scholarly citation rather than direct inspection of Hughes's table image.

---

# 3. High-value arena assertions still quarantined

## 3.1 Termessos / TAM III,1 870

Arena reports direct PHI body:

```text
τό(πος) Αὐρ(ηλίας) Ὀρεστιανῆς, ἱ(ερῶν) Ἐλευσι-
νίων προφήτιδος.
```

Independent controls verify the edition `TAM III,1` and a specialist list explicitly includes `TAM III,1 870 (Termessos)` among external `prophetis` inscriptions. The exact PHI target page/body has **not** yet been independently rendered in the target workflow.

```text
TERMESSOS_870_SPECIALIST_REFERENCE = CORROBORATED
TERMESSOS_870_DIRECT_BODY = HIGH_PRIORITY_ARENA_DISCOVERY_PENDING_PRIMARY_REOPEN
```

## 3.2 Potta / TAM V.1 535

The target object identity and specialist transcription are strongly controlled, but the exact direct PHI target-page body remains a reopen target in this workflow.

```text
POTTA_PHI_OBJECT_IDENTITY = CLOSED_DIRECT_SEARCH_SURFACE
POTTA_PROPHETIS_FULL_WORDING = STRONG_SPECIALIST_TRANSCRIPTION_CONTROL
POTTA_DIRECT_PHI_TARGET_PAGE = STILL_REOPEN_TARGET
```

## 3.3 Full-body/PDF/image holds

```text
KOWALSKI_2020_FULL_PDF_BODY = STILL_RENDER_HOLD
REASONER_2025_FULL_BODY = NOT_ACQUIRED
HAO_LI_CHINESE_PDF_FULL_BODY = NOT_FULLY_RENDERED
WANG_2022_CHINESE_PDF_FULL_BODY = NOT_RENDERED
FRANCIS_FULL_PDF_BODY = RUNTIME_HOLD
HUGHES_DIRECT_TABLE_IMAGE = NOT_AUTOPSIED
FANTHAM_OLSON_EXACT_ARENA_PREVIEW_WORDING = NOT_ALL_INDEPENDENTLY_REPRODUCED
```

---

# 4. Branch-conflict audit

The arena branch contains both useful discoveries and inconsistent/incorrect closure states.

Internal mismatch example:

```text
ARENA_MANUAL_KOWALSKI = CLAIMS_DIRECT_FULL_PDF_READ
ARENA_QUOTATION_OWNER_KOWALSKI = RETAINS_OLDER_PDF_ENDPOINT_HOLD
```

Externally falsified reversal:

```text
ARENA_NISYRA = CLAIMS_RESTORED_PROPHETIS_IN_SEG49_1624
TARGET_DIRECT_PHI_CONTROL = NO_PROPHETIS_IN_TARGET_INDEXED_TEXT
```

Critical-edition oversimplification:

```text
ARENA_BGU7_1655 = SIMPLE_APO_PLUS_GENITIVE
TARGET_DIRECT_EDITION = APO_VS_EK_APPARATUS_COMPLEXITY
```

Therefore:

```text
PARALLEL_BRANCH != SINGLE_COHERENT_AUTHORITY
MOST_RECENT_AGENT_EDIT != AUTOMATIC_TRUTH
CLOSED_DIRECT_LABEL != SOURCE_VERIFICATION
EVERGREEN_OWNER_UPDATE_REQUIRES_SOURCE_RECHECK
```

---

# 5. Integration queue after this pass

```text
CLOSED_VERIFIED_OR_STRONGLY_CONTROLLED_NOW:
  APPHE_DIRECT_PHI_BODY
  COSTA_FULL_OFFICIAL_PDF
  P_WISC_I_13_RESTORATION_CEILING
  P_OXY_8_1120_KATA_GEN_CONTROL
  BGU_7_1655_APPARATUS_CAUTION
  P_OXY_9_1205_EIS_ACC_DIRECT_DDBDP
  FENDEL_THREE_REPORTED_DOCUMENTS_DOCUMENT_LEVEL_CONTROL
  NISYRA_SEG49_1624_FALSE_ARENA_REVERSAL
  FRANCIS_OFFICIAL_ABSTRACT
  HAO_LI_OFFICIAL_OBJECT_ABSTRACT
  WANG_2022_OFFICIAL_OBJECT_ABSTRACT
  KOWALSKI_KUL_INSTITUTIONAL_FILE_OBJECT
  THISSELTON_TARGET_SECTION_ARCHITECTURE
  HUGHES_TABLE1_COUNTS_EXACT_PEER_REVIEWED_CITATION

OWNER_MIGRATION_NEXT:
  P0A = EXOUSIA_OWNER_ABSORB_PWISC_POXY8_BGU_POXY9_FENDEL_CALIBRATION
  P0B = RITUAL_OWNER_CORRECT_APPHE_FORK
  P0C = QUOTATION_OWNER_ABSORB_COSTA_FULL_BODY_AND_KOWALSKI_KUL_ROUTE
  P0D = MANUAL_CHECKLIST_REMOVE_NOW_CLOSED_DIRECT_OR_STRONGLY_CONTROLLED_ITEMS

PRIMARY_REOPEN_NEXT:
  P1A = TERMESSOS_TAMIII1_870_DIRECT_PHI_BODY
  P1B = FENDEL_EXOUSIAN_XLSX_BINARY
  P1C = REASONER_RICH_PREVIEW_REPRODUCTION
  P1D = KOWALSKI_FULL_PDF_BODY
  P1E = POTTA_DIRECT_PHI_TARGET_PAGE
  P2 = HUGHES_DIRECT_TABLE_IMAGE / FRANCIS_FULL_PDF / HAO_LI_TAIL / WANG_FULL_PDF / FANTHAM_OLSON_PAGE_AUTOPSY
```

---

# 6. Research-state result

```text
PARALLEL_BRANCH_HARVEST = ACTIVE
ARENA_UNIQUE_COMMITS_AT_LATEST_COMPARE = 12
ARENA_UNIQUE_CHANGED_EVERGREEN_FILES = 4
ARENA_NISYRA_FALSE_REVERSAL_CAUGHT = YES
P_OXY_9_1205_DIRECT_COMPLEMENT_CLOSED = YES
FENDEL_THREE_DOCUMENT_FORMS_INDEPENDENTLY_CORROBORATED = YES_WITH_BGU_APPARATUS_CAUTION
FENDEL_XLSX_BINARY_TARGET_READ = NO
HUGHES_TABLE1_EXACT_LATER_PEER_REVIEWED_COUNT_CONTROL = CLOSED
HUGHES_DIRECT_TABLE_AUTOPSY = NO
CORE_GRADE_REVERSALS = 0
MULTILINGUAL_REOPEN_SWEEP = ACTIVE
REGIONAL_LIBRARY_REOPEN_SWEEP = ACTIVE
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
SITE_PUBLICATION = false
```

This receipt is provenance, not a new authority layer. Once surviving deltas are migrated into their controlling evergreen owners, it should be reduced further rather than promoted.