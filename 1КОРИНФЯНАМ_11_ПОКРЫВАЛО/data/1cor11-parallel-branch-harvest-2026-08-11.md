# 1 Cor 11:2–16 — parallel branch harvest — 2026-08-11

**Type:** `PROVENANCE-RECEIPT / PARALLEL-AGENT-HARVEST / DISCOVERY-QUARANTINE / NON-AUTHORITY / RESEARCH-ONLY / PUBLICATION-HOLD`

**Source branch inspected:** `arena/019fed70-research`  
**Target integration branch:** `agent/1cor11-citation-quarantine-20260810`

This receipt exists because the parallel branch contains genuinely distinct multi-agent acquisition provenance. It does **not** own claim grades and does not override evergreen owners.

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

At first inspection the two branches were diverged by 12 commits each. After this target branch added its first harvest receipt, the arena branch remained 12 unique commits ahead and became 13 commits behind the target branch. Its unique content delta remains concentrated in four existing evergreen files:

```text
dossiers/EXOUSIA_FORMAL_DOCUMENTARY_CORPUS.md
dossiers/MANUAL_READING_ACCESS_CHECKLIST.md
dossiers/QUOTATION_REFUTATION_SPEAKER_BOUNDARY.md
dossiers/RITUAL_DIVINATION_PROPHETIC_HEAD_STATE.md
```

This is a harvest target, **not** a reason to merge the branch wholesale. The target branch also contains newer multilingual/regional acquisition work absent from the arena branch.

```text
WHOLE_BRANCH_BLIND_MERGE = NO
CHERRY_PICK_UNVERIFIED_AGENT_ASSERTIONS = NO
HARVEST_DELTA_THEN_VERIFY = YES
```

## 2. Independently verified from primary/official routes in this pass

### 2.1 Apphe / IK Kalchedon 61 — direct PHI body CLOSED

Official PHI page:
- https://inscriptions.packhum.org/text/279287

Direct text:

```text
Ὀρβανίλλα,
θρεπτὴ Ἄπφης
προφήτιδος,
ζήσασα ἔτη ζκʹ·
μήτηρ Τυραννίς. ζῇ
```

The genitive sequence `θρεπτὴ Ἄπφης προφήτιδος` directly makes Apphe the bearer of `προφῆτις`; Orbanilla is her `θρεπτή`/fostling or ward. This inscription does **not** support reading Apphe as merely “a prophet's wife.” It still does not by itself settle whether the title denotes a formal independent oracle office rather than another title/status usage.

```text
APPHE_IK61_DIRECT_PHI_BODY = CLOSED_DIRECT
APPHE_PROPHETIS_NOUN_BEARER = A_DIRECT_BODY
APPHE_PROPHET_WIFE_READING_FROM_THIS_INSCRIPTION = NOT_SUPPORTED
APPHE_FORMAL_INDEPENDENT_ORACLE_OFFICE = B_C_AMBIGUOUS
APPHE_HEAD_HAIR_CODE = NOT_ATTESTED
```

**Required owner correction:** remove the stale direct-page terminal hold and narrow the old “oracle office vs prophet-wife” fork to the still-live **formal-office/status** question.

### 2.2 Alessandra Castilho da Costa — official UFMG article record

Official article:
- https://periodicos.ufmg.br/index.php/relin/article/view/55158
- DOI `10.17851/2237-2083.31.3.1404-1446`

The official abstract directly states that the study uses textual-discourse/argumentative analysis, identifies antagonistic Pauline and Corinthian points of view, and concludes that **vv.4–9 are quotations not endorsed by Paul**.

```text
COSTA_ARTICLE_IDENTITY = CLOSED_DIRECT_OFFICIAL
COSTA_VV4_9_UNENDORSED_QUOTATION = CLOSED_DIRECT_OFFICIAL_ABSTRACT
COSTA_DETAILED_VERSE_BY_VERSE_BODY_CLAIMS_FROM_ARENA = PENDING_INDEPENDENT_PDF_BODY_REOPEN
```

The arena branch reports a full official PDF read and much more detailed conclusions (v10, angels, v13, vv14–15). Those details remain discovery-only until the PDF body itself is independently re-rendered/read in the target workflow.

### 2.3 Nicole Francis 2023 — official BYU model control

Official BYU ScholarsArchive:
- https://scholarsarchive.byu.edu/studiaantiqua/vol22/iss1/6/

The institutional abstract directly verifies her alternative model: Paul is not primarily laying down a standalone prayer/prophecy dress code; rather, in a group-conflict setting he appeals to cultural norms involving hair and head coverings in order to reason through the hierarchy he presents.

```text
FRANCIS_2023_OBJECT = CLOSED_DIRECT_INSTITUTIONAL
FRANCIS_ROMAN_ANALOGY_NOT_PRIMARY_DRESS_CODE = CLOSED_DIRECT_ABSTRACT
FRANCIS_PDF_DOWNLOAD_ROUTE = VERIFIED
FRANCIS_FULL_PDF_BODY = CURRENT_RUNTIME_403_HOLD
```

Do not promote arena-only body details beyond this abstract ceiling until the PDF renders.

### 2.4 Hao Li 2023 — official JRCC object + OA PDF route

Official JRCC:
- https://ccspub.cc/jrcc/article/view/38
- DOI `10.29635/JRCC.202312_(21).0012`
- pp.267–318

The official page directly exposes the abstract and a `PDF (Chinese)` route. The abstract argues that the passage dialectically combines subordination language with mutual reciprocity/unity in an honor-shame setting, with Paul's main aim being reciprocal unity rather than a timeless absolute principle of female subordination.

```text
HAO_LI_2023_OBJECT = CLOSED_DIRECT_OFFICIAL
HAO_LI_2023_ABSTRACT = CLOSED_DIRECT
HAO_LI_2023_OFFICIAL_CHINESE_PDF_ROUTE = VERIFIED
HAO_LI_2023_FULL_PDF_BODY_IN_TARGET_RUNTIME = NOT_YET_RENDERED
```

The arena claim `CLOSED_DIRECT_RUNTIME_OPEN_ACCESS` is therefore not copied blindly; the target workflow keeps the body ceiling until the actual PDF bytes render here.

### 2.5 Nathanael Xuesheng Wang 2022 — new Chinese-route node

Official JRCC:
- https://ccspub.cc/jrcc/article/view/109
- DOI `10.29635/JRCC.202212_(19).0005`
- pp.80–111

The official abstract states that Wang treats the 1 Cor 11 instruction as “veil while praying and prophesying,” stresses women's participation in worship/ministry, and reads the covering instruction primarily in relation to how the young church is perceived socially. He treats 1 Cor 14:34–35 as a later interpolation.

```text
WANG_2022_OBJECT = CLOSED_DIRECT_OFFICIAL
WANG_2022_ABSTRACT = CLOSED_DIRECT
WANG_2022_CHINESE_PDF_ROUTE = VERIFIED
WANG_2022_FULL_BODY = NOT_YET_RENDERED_CURRENT_RUNTIME
```

This is a genuine multilingual discovery node and should enter the current-literature/multilingual radar at abstract level unless later direct body supersedes that ceiling.

### 2.6 P.Wisc. I 13 — restoration ceiling directly closed

Direct DDBDP text via the University of Grenoble Roman-law mirror:
- https://droitromain.univ-grenoble-alpes.fr/Negotia/Wisc1_DDBDP.gr.html

The opening testamentary formula is printed as:

```text
[ἐν ἀγυιᾷ. ἐφ᾽ ὃν μὲν περίειμι χρόνον ἔχειν με τὴν τῶν ἰδίων ἐξουσίαν πᾶσα]ν,
ὃ ἐὰν βούλωμαι, περὶ αὐτῶν ἐπιτελεῖν ...
```

The lexeme `ἐξουσίαν` itself is wholly inside the editorial brackets. Only the final `]ν` of `πᾶσαν` lies outside that reconstructed span at this point.

```text
P_WISC_I_13_EXOUSIA_FORMULA = EDITORIAL_RECONSTRUCTION
P_WISC_I_13_EXOUSIA_LEXEME_SURVIVING_LETTERS = NONE_VISIBLE_IN_PRINTED_EDITION
P_WISC_I_13_USE = FORMULA_RESTORATION_CONTROL
P_WISC_I_13_USE_AS_DIRECT_SURVIVING_EXOUSIA_LEXEME = FORBIDDEN
```

This independently confirms the useful arena correction and sharpens the older evergreen wording “restored in the relevant region.”

### 2.7 P.Oxy. VIII 1120 — `κατά + genitive` independently closed

A current peer-reviewed Oxford Academic article directly reproduces the documentary phrase from P.Oxy. 8.1120:

```text
μὴ ἔχων κατ' αὐτῆς ἐξουσίαν
```

The formal relation is therefore independently secure as `κατά + genitive` with active authority over a person.

```text
P_OXY_8_1120_KATA_GEN_EXOUSIA = CLOSED_DIRECT_PAGE_SPECIFIC_SCHOLARLY_QUOTATION
FENDEL_XLSX_ROW_IDENTITY_FOR_THIS_ITEM = STILL_REQUIRES_XLSX_IF_CLAIMED_AS_DATASET_ROW
```

### 2.8 BGU VII 1655 — direct edition exposes an apparatus complication

Berlin Papyrus Database directly prints line 33:

```text
αὐτο[ῦ] ἐξουσίαν ἕξ̣[ει] ἀ [[πο]](*) τῶν κ[λη]ρονόμω[ν] μου.
```

and the apparatus explicitly gives for line 2.33:

```text
\ἐκ/
```

So the arena shorthand `BGU.7.1655 = ἀπό + genitive` must **not** be promoted as a clean unqualified dataset reading before Fendel's XLSX row is actually opened. The direct edition records a correction/apparatus problem at precisely the preposition.

```text
BGU_7_1655_EXOUSIA_ECHEIN = CLOSED_DIRECT_DOCUMENTARY
BGU_7_1655_SIMPLE_APO_GEN_LABEL = NOT_SAFE_WITHOUT_APPARATUS_NOTE
BGU_7_1655_PREPOSITION = EDITION_APPARATUS_COMPLEXITY_APO_VS_EK
FENDEL_XLSX_STILL_NEEDED_FOR_HER_NORMALIZED_ROW
```

### 2.9 Nisyra / SEG 49.1624 — arena reversal REJECTED by direct PHI control

This was the most important branch-conflict test. The arena branch claimed that direct PHI contained restored `διὰ προφή[τιδος ...]` and therefore that the older reference-error verdict should be reversed.

Direct PHI control does **not** support that claim.

The PHI page for `SEG 49:1623` links its next inscription explicitly as **SEG 49:1624** to PHI object `348429`, confirming the old project crosswalk rather than an off-by-one object. PHI search output for `SEG 49:1624` gives the target text as the short Lydia dedication:

```text
Θεῷ Βασιλεῖ Διονο[ι— μετὰ τῶν]
ἰδίων πάντων κατ[ὰ ἐπιταγὴν]
```

No `προφῆτις` or restored `προφή[τιδος]` appears in the indexed target text.

```text
NISYRA_SEG49_1624_PHI_OBJECT = PH348429_CONFIRMED_BY_NEIGHBOR_LINK
NISYRA_SEG49_1624_DIRECT_INDEXED_TEXT = TWO_LINE_DEDICATION
NISYRA_SEG49_1624_VISIBLE_OR_RESTORED_PROPHETIS = NOT_PRESENT
ARENA_NISYRA_RESTORED_PROPHETIS_CLAIM = REJECTED
NISYRA_VERY_LIKELY_REFERENCE_ERROR_IN_NAWOTKA_FN77 = REINSTATED
INTENDED_REFERENCE = UNKNOWN
DO_NOT_GUESS = true
```

This is a concrete example where branch harvesting prevented a false grade/source reversal from entering the controlling owner.

## 3. High-value arena assertions still quarantined pending independent source reopen

The following are **not rejected**; they are prioritized because the parallel branch reports direct closure. They remain discovery-only until the target workflow reaches the same primary body independently.

### 3.1 Fendel `EXOUSIAN.xlsx`

Arena reports the three Roman-period PP rows as:

```text
BGU.7.1655 = ἀπό + genitive
P.Oxy.8.1120 = κατά + genitive
P.Oxy.9.1205 = εἰς + accusative
```

Current audit refinement:
- P.Oxy.8.1120 `κατά + genitive` is independently corroborated;
- BGU VII 1655 has a direct-edition `ἀπό` / apparatus `ἐκ` complication, so the arena shorthand is not safe as written;
- P.Oxy.9.1205 exact complement remains to be independently reopened;
- the actual Fendel XLSX row normalization remains unread in this target runtime.

```text
FENDEL_ORA_DATASET_OBJECT = CLOSED_OFFICIAL
EXOUSIAN_XLSX_FILE_IDENTITY = CLOSED_OFFICIAL
FENDEL_THREE_PP_ROW_ENUMERATION = PARTIALLY_CORROBORATED_NOT_DATASET_BODY_CLOSED
```

### 3.2 Potta / TAM V.1 535

PHI search output now independently exposes the correct target object `TAM V,1 535`, location Maionia and `laurus`; the same search surface exposes the start/end of the Hermogenes dedication. A separate scholarly transcription reproduces the full formula including `Ποτταν ... προφῆτιν σώτειραν`, but the exact PHI target-page body has not yet rendered in the target workflow.

```text
POTTA_PHI_OBJECT_IDENTITY = CLOSED_DIRECT_SEARCH_SURFACE
POTTA_PROPHETIS_FULL_WORDING = STRONG_SPECIALIST_TRANSCRIPTION_CONTROL
POTTA_DIRECT_PHI_TARGET_PAGE = STILL_REOPEN_TARGET
```

### 3.3 Termessos / TAM III,1 870

Arena reports direct PHI body:

```text
τό(πος) Αὐρ(ηλίας) Ὀρεστιανῆς, ἱ(ερῶν) Ἐλευσι-
νίων προφήτιδος.
```

The exact target page has not yet been independently rendered. Nawotka's current specialist list does cite `TAM III,1 870 (Termessos)` among external `prophetis` inscriptions, so the arena claim is plausible and high priority, but body/noun-bearer syntax still requires primary reopening here.

```text
TERMESSOS_870_SPECIALIST_REFERENCE = CORROBORATED
TERMESSOS_870_DIRECT_BODY = HIGH_PRIORITY_ARENA_DISCOVERY_PENDING_REOPEN
```

### 3.4 Kowalski 2020

Arena manual checklist reports full Polish OA PDF read, while its own quotation evergreen file still retains the older `PDF_BYTES_TERMINAL_RUNTIME_ENDPOINT_HOLD` wording. This internal cross-file mismatch is exactly why branch assertions are not promoted automatically.

```text
KOWALSKI_ARENA_STATE = INTERNALLY_UNSYNCED
TARGET_WORKFLOW = REOPEN_OFFICIAL_PDF_BEFORE_PROMOTION
```

### 3.5 Reasoner 2025 preview details

Arena reports materially richer Google/publisher preview snippets for Commentary 7, including translation/section headings, v15/v16 wording fragments, and angels/authority notes.

```text
REASONER_ARENA_PREVIEW_DELTA = HIGH_VALUE_DISCOVERY
REASONER_DETAILED_POSITION = DO_NOT_PROMOTE_UNTIL_TARGET_PREVIEW_REPRODUCED
```

### 3.6 Lisa Hughes 2007 visual table

Arena reports exact peer-reviewed citation control for Table 1 (`N=113`, 67 veiled / 59%, 46 unveiled / 41%) but explicitly says this is **not direct table-image autopsy**.

```text
HUGHES_TABLE_NUMBERS = ARENA_PAGE_SPECIFIC_SECONDARY_OR_TEXTUAL_CONTROL
HUGHES_DIRECT_TABLE_IMAGE = NOT_YET_CLOSED_IN_TARGET_WORKFLOW
```

## 4. Branch-conflict audit

The parallel branch is valuable but not internally perfect. Two concrete classes are now established.

First, an internal cross-file mismatch:

```text
MANUAL_CHECKLIST_KOWALSKI = CLAIMS_DIRECT_FULL_PDF_READ
QUOTATION_EVERGREEN_KOWALSKI = STILL_TERMINAL_PDF_ENDPOINT_HOLD
```

Second, an externally falsified arena delta:

```text
ARENA_NISYRA = CLAIMS_RESTORED_PROPHETIS_IN_SEG49_1624
DIRECT_PHI_NISYRA = TWO_LINE_DEDICATION / NO_PROPHETIS
```

Therefore:

```text
PARALLEL_BRANCH != SINGLE_COHERENT_AUTHORITY
MOST_RECENT_AGENT_EDIT != AUTOMATIC_TRUTH
EVERGREEN_OWNER_UPDATE_REQUIRES_SOURCE_RECHECK
```

## 5. Integration queue generated by this harvest

```text
CLOSED_VERIFIED_NOW:
  APPHE_DIRECT_PHI_BODY
  P_WISC_I_13_RESTORATION_CEILING
  P_OXY_8_1120_KATA_GEN_CONTROL
  BGU_7_1655_APPARATUS_CAUTION
  NISYRA_SEG49_1624_FALSE_ARENA_REVERSAL
  COSTA_OFFICIAL_ABSTRACT
  FRANCIS_OFFICIAL_ABSTRACT
  HAO_LI_OFFICIAL_OBJECT_ABSTRACT
  WANG_2022_OFFICIAL_OBJECT_ABSTRACT

P0A = APPHE_OWNER_CORRECTION
P0B = NISYRA_OWNER_RETAIN_REFERENCE_ERROR_AND_RECORD_ARENA_FALSE_REVERSAL
P0C = TERMESSOS_TAMIII1_870_DIRECT_BODY_REOPEN
P0D = FENDEL_EXOUSIAN_XLSX_ROW_REOPEN
P0E = EXOUSIA_OWNER_ABSORB_PWISC_POXY_BGU_REFINEMENTS
P1A = COSTA_FULL_OFFICIAL_PDF_REOPEN
P1B = KOWALSKI_FULL_OFFICIAL_PDF_REOPEN
P1C = REASONER_PREVIEW_REPRODUCTION
P1D = POTTA_DIRECT_PHI_REOPEN
P1E = HAO_LI_CHINESE_PDF_REOPEN
P1F = WANG_2022_CHINESE_PDF_REOPEN
P2 = FRANCIS_FULL_PDF / HUGHES_TABLE_IMAGE / OTHER_NONBLOCKING_BODY_CONTROLS
```

## 6. Research-state result

```text
PARALLEL_BRANCH_HARVEST = ACTIVE
ARENA_UNIQUE_COMMITS_AT_LATEST_COMPARE = 12
ARENA_UNIQUE_CHANGED_EVERGREEN_FILES = 4
ARENA_NISYRA_FALSE_REVERSAL_CAUGHT = YES
INDEPENDENT_PRIMARY_OR_OFFICIAL_CONFIRMATIONS = APPHE + PWISC + POXY8_1120 + BGU7_1655 + NISYRA_CONTROL + COSTA_ABSTRACT + FRANCIS_ABSTRACT + HAO_LI_OBJECT_ABSTRACT + WANG_2022_OBJECT_ABSTRACT
HIGH_VALUE_UNVERIFIED_AGENT_DELTAS = QUARANTINED_NOT_DROPPED
CORE_GRADE_REVERSALS = 0
MULTILINGUAL_REOPEN_SWEEP = ACTIVE
REGIONAL_LIBRARY_REOPEN_SWEEP = ACTIVE
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
SITE_PUBLICATION = false
```

This receipt should be deleted or reduced after all surviving evidence deltas are migrated into their controlling evergreen owners. It is provenance, not a new authority layer.