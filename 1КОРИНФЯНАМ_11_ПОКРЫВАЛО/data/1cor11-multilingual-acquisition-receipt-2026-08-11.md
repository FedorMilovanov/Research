# 1 Cor 11:2–16 — multilingual acquisition receipt — 2026-08-11

**Type:** `PROVENANCE-RECEIPT / MULTILINGUAL-SEARCH / REGIONAL-ACCESS / NON-AUTHORITY`  
**Controlling owners:** `00_CURRENT_INDEX_1COR11.md`, `dossiers/CURRENT_COMMENTARY_ACQUISITION_2025.md`, domain-specific evergreen dossiers.

This receipt records genuinely distinct provenance introduced by the multilingual/regional acquisition method. It does **not** own grades.

```text
LANGUAGE != EVIDENCE_GRADE
PUBLISHED_TRANSLATION != MACHINE_TRANSLATION
PUBLISHED_TRANSLATION_OF_EDITION_N != OTHER_EDITION_BODY
LIBRARY_HOLDING != BODY_READ
OFFICIAL_OR_LICENSED_SAMPLE_ROUTE != TARGET_BODY_READ
AUTHOR_SUMMARY != FULL_MONOGRAPH_BODY
SEARCH_SNIPPET != QUOTE_SAFE_BODY
```

## 1. Fee 1987 — Spanish direct body

User-supplied Nueva Creación 1994 Spanish translation directly identifies Eerdmans 1987 as the English original and exposes the complete 1 Cor 11:2–16 body.

```text
FEE_1987_FIRST_EDITION_BODY = CLOSED_DIRECT_VIA_PUBLISHED_SPANISH_TRANSLATION
FEE_1994_ES != FEE_REVISED_2014
GOOGLE_DRIVE_COPY = STORED
```

Detailed receipt:
- `data/1cor11-fee-1987-spanish-user-acquisition-2026-08-11.md`

## 2. Fee Revised 2014 — Portuguese + Spanish authorized lanes

### Portuguese Vida Nova / CLC

Official publisher route verifies the Portuguese edition is based on the **second English edition (2014)**. The official 52-page sample directly exposes the revised preface and localized TOC:

```text
11:2–16 = p616
11:2–6 = p626
11:7–12 = p645
11:13–16 = p660
11:17–34 = p668
```

Target exposition is not present in that sample.

### Portuguese OverDrive / Libby

OverDrive directly records the same Vida Nova ebook:

```text
TITLE = 1Coríntios: comentário exegético
AUTHOR = Gordon_D_Fee
FORMAT = ebook
ISBN = 9788527509268
PUBLISHER = Vida_Nova
RELEASE = 2022_05_27
READ_A_SAMPLE = AVAILABLE_ROUTE
LIBBY_LIBRARY_SEARCH = AVAILABLE_ROUTE
```

The OverDrive page itself states that this Portuguese edition is based on the second English edition of 2014. Its sample embed is a licensed route, but the current runtime does not render the target pages.

```text
FEE_PT_OVERDRIVE_LIBBY_ROUTE = VERIFIED_LICENSED_ROUTE
FEE_PT_OVERDRIVE_TARGET_11_2_16 = NOT_RENDERED_CURRENT_RUNTIME
```

### Spanish Tesoro Bíblico / Logos

Official 2024 Spanish edition is explicitly based on the revised English commentary published in 2014. Licensed look-inside exists; target 1 Cor 11 body is not exposed in the current preview.

```text
FEE_2014_PT_2019 = AUTHORIZED_REVISED_TRANSLATION_ROUTE
FEE_2014_PT_OVERDRIVE_2022 = LICENSED_EBOOK_ROUTE
FEE_2014_ES_2024 = AUTHORIZED_REVISED_TRANSLATION_ROUTE
FEE_2014_TARGET_EXPOSITION = NOT_YET_DIRECTLY_ACQUIRED
```

Owner:
- `00ZZZZZZZZZ_SOURCE_CARD_FEE_REVISED_2014_1COR11.md`

## 3. Romerowski 2006 — French direct full body

Sylvain Romerowski, “L’exousia sur la tête en 1 Corinthiens 11.10,” *Théologie évangélique* 5.2 (2006): 147–166, author-hosted PDF.

```text
ROMEROWSKI_2006_FULL_BODY = CLOSED_DIRECT_AUTHOR_HOSTED
MATERIAL_HEAD_COVERING = YES_IN_AUTHOR_MODEL
EXOUSIA_METONYMY = SERIOUS_PUBLISHED_COUNTERMODEL
HUSBANDS_AUTHORITY_SIGN = AUTHOR_PREFERRED_CONTEXTUAL_REFERENT
WOMANS_RIGHT = AUTHOR_ACKNOWLEDGES_AS_POSSIBLE_BEFORE_CONTEXTUAL_DECISION
ANGELS = HEAVENLY_WORSHIP_ANGELS
ACTIVE_EXOUSIA_PULL_FORCES_EXACT_REFERENT = FALSE
```

Owner updated:
- `dossiers/EXOUSIA_FORMAL_DOCUMENTARY_CORPUS.md`

## 4. Schirrmacher 1993 / revised 2002 — German monograph + author PDF routes

Author + Heidelberg controls verify *Paulus im Kampf gegen den Schleier: Eine alternative Auslegung von 1. Korinther 11,2–16*, first edition 1993, revised 5th edition 2002, 130 pp., ISBN `9783933372451`, with Heidelberg physical holding.

The author's own book page now directly exposes **three full-book PDF download routes**:

```text
BOOK_2002_PDF = AUTHOR_HOSTED_DOWNLOAD_ROUTE
BOOK_2007_ENGLISH_PDF = AUTHOR_HOSTED_DOWNLOAD_ROUTE
BOOK_2023_ENGLISH_PDF = AUTHOR_HOSTED_DOWNLOAD_ROUTE
```

The current web runtime resolves the exact PDF URLs but returns cache-miss on the binaries, so their existence is a stronger lawful acquisition route but not yet body closure.

Author summary directly describes a quotation/refutation model: Corinthian veil teaching driven ad absurdum in vv4–9, Pauline contradiction in vv10–15, and v16 denying universal binding force.

```text
SCHIRRMACHER_MODEL_EXISTENCE = CLOSED_DIRECT_AUTHOR_LIBRARY
SCHIRRMACHER_AUTHOR_SUMMARY = DIRECT
SCHIRRMACHER_AUTHOR_FULL_PDF_ROUTES = VERIFIED
SCHIRRMACHER_FULL_BOOK_BODY = NOT_YET_RENDERED_CURRENT_RUNTIME
```

Owner updated:
- `dossiers/QUOTATION_REFUTATION_SPEAKER_BOUNDARY.md`

## 5. Biguzzi — Italian hair-side route

Official EDB + Pontifical Gregorian University verify Giancarlo Biguzzi, *Velo e silenzio. Paolo e la donna in 1Cor 11,2–16 e 14,33b–36* (2001), 200 pp., ISBN `9788810302255`, with Gregorian physical holding.

A directly readable Italian 2009 synthesis of Biguzzi’s own position gives a substantive hair-side model:

```text
TRADITIONAL_MALE_CAP_FEMALE_VEIL_READING = QUESTIONED
GREEK_TEXT_WORD_VEIL = AUTHOR_SAYS_NOT_USED
VV14_15_HAIR = CENTRAL_CONTROL
SEX_DIFFERENTIATED_HAIRSTYLE = AUTHOR_MODEL
CORINTHIAN_MASCULINIZING_HAIRSTYLE = RECONSTRUCTION
HOMOSEXUALITY_SUSPICION = RECONSTRUCTION
```

```text
BIGUZZI_2009_DIRECT_SYNTHESIS = CLOSED_DIRECT_WEB_BODY
BIGUZZI_2001_MONOGRAPH_IDENTITY = CLOSED_DIRECT_PUBLISHER_LIBRARY
BIGUZZI_2001_FULL_BODY = NOT_YET_ACQUIRED
```

Owner updated:
- `00ZZZZZZZZZZZZZZZZZ_HAIR_PHYSIS_PRIMARY_SOCIAL_CORPUS_AUDIT_2026-08-10.md`

## 6. Winter — Portuguese authorized translation route

Vida Nova verifies 2026 Portuguese translation *Cristianismo e paganismo: A influência da cultura na igreja de Corinto* of *After Paul Left Corinth* (print ISBN `9786559673933`; ebook `9786559673926`). Licensed preview exposes ch.6 architecture for 1 Cor 11:2–16; current official sample route does not expose readable chapter body.

```text
WINTER_PT_2026_IDENTITY = CLOSED_DIRECT_PUBLISHER
WINTER_PT_CH6_TOC = CLOSED_LICENSED_PREVIEW
WINTER_CH6_BODY = NOT_YET_DIRECTLY_ACQUIRED
```

## 7. Regional / licensed lanes

```text
REASONER_2025 = IXTHEO + HBZ_ILL_SUBITO_ROUTE
GORMAN_2025 = OVERDRIVE_LIBBY_ROUTE
GARLAND_2025_2E = CINII_EXACT_RECORD + DOSHISHA_AND_NANZAN_HOLDINGS
THISELTON_2000 = OVERDRIVE_LIBBY + PBTS_PHYSICAL_HOLDING
CIAMPA_ROSNER_2010 = IXTHEO_LICENSED_FULLTEXT_RECORD + HBZ_ILL_SUBITO
LUMESBERGER_LOISL_2025 = IXTHEO_GERMAN_ILL_ROUTE
OKLAND = BLOOMSBURY_LOOK_INSIDE + PERLEGO_LICENSED_PDF_ROUTE
```

All remain `BODY_NOT_ACQUIRED` unless target pages themselves become readable.

## 8. Lampe 2012 — German OA route

Heidelberg repository verifies Peter Lampe, “Paulus und die erotischen Reize der Korintherinnen (1 Kor 11,2–16),” 2012, pp.196–207, DOI `10.11588/heidok.00025278`, with official OA PDF route. Current runtime is blocked by host anti-bot behavior.

```text
LAMPE_2012_OBJECT = CLOSED_INSTITUTIONAL_METADATA
LAMPE_2012_OFFICIAL_OA_PDF_ROUTE = VERIFIED
LAMPE_2012_BODY = NOT_YET_DIRECTLY_READ
```

## 9. Łabuda 2019 — Polish repository route

Institutional/journal repository verifies Piotr Łabuda, “1 Kor 11,2-16 wyrazem mizoginizmu św. Pawła?”, *Śląskie Studia Historyczno-Teologiczne* 52.1 (2019): 5–22, with repository PDF route and open-license metadata.

```text
LABUDA_2019_OBJECT = CLOSED_INSTITUTIONAL_METADATA
LABUDA_2019_ABSTRACT = CLOSED_DIRECT
LABUDA_2019_PDF_ROUTE = VERIFIED
LABUDA_2019_FULL_BODY = NOT_YET_DIRECTLY_READ
```

## 10. Anderson Dias de Araújo 2009 — Portuguese Watchers route

Universidade Metodista de São Paulo repository directly verifies:
- Anderson Dias de Araújo, *Anjos vigilantes e mulheres desveladas: uma relação possível em 1 Coríntios 11,10?*;
- dissertation, Ciências da Religião, 2009-09-03;
- 138 folios;
- advisor Paulo Augusto de Souza Nogueira;
- CAPES sponsorship;
- handle `https://repositorio.metodista.br/handle/123456789/1481`;
- repository file `Anderson Dias de Araújo (2).pdf`, 723.54 KB.

The institutional abstract directly says the study tests Watchers-myth influence on 1 Cor 11:2–16/v10 and concludes there is strong evidence Paul knew the Watchers narrative and shared the relevant Second-Temple Jewish worldview.

```text
ARAUJO_2009_DISSERTATION_IDENTITY = CLOSED_DIRECT_INSTITUTIONAL
ARAUJO_2009_REPOSITORY_PDF_OBJECT = VERIFIED
ARAUJO_2009_ABSTRACT = CLOSED_DIRECT_INSTITUTIONAL
ARAUJO_2009_FULL_PDF_BODY = NOT_YET_RENDERED_CURRENT_RUNTIME
ARAUJO_WATCHERS_MODEL = REAL_PORTUGUESE_SCHOLARLY_NODE
WATCHERS_GRADE_CHANGE_FROM_ABSTRACT_ALONE = NO
```

## 11. Nathanael Xuesheng Wang 2022 — Chinese official OA journal route

Official *Journal of Research for Christianity in China* / 《中国基督教研究》 records:
- 王学晟 / Nathanael Xuesheng Wang;
- “蒙头祷告讲道还是闭口不言？——对哥林多前书中两段矛盾经文之探讨” / “Praying and Prophesying with Coverings or Remaining Silent: A Probe into the Two Contradictory Periopae in 1 Corinthians”;
- no.19 (2022), pp.80–111;
- DOI `10.29635/JRCC.202212_(19).0005`;
- official journal article page + PDF route;
- journal is open access and states CC BY-NC-ND 4.0 for its articles.

The official abstract directly says the author reads 1 Cor 11:2–16 as Paul supporting women's prayer/prophecy while requiring head covering primarily because of the young church's social image, not as a restriction on women's ministry. It separately treats 1 Cor 14:34–35 as a later interpolation.

```text
WANG_2022_CHINESE_ARTICLE_IDENTITY = CLOSED_DIRECT_OFFICIAL_JOURNAL
WANG_2022_OFFICIAL_OA_PDF_ROUTE = VERIFIED
WANG_2022_ABSTRACT = CLOSED_DIRECT_OFFICIAL
WANG_2022_FULL_PDF_BODY = NOT_YET_RENDERED_CURRENT_RUNTIME
WANG_2022_MATERIAL_COVERING_SOCIAL_IMAGE_MODEL = REAL_CHINESE_SCHOLARLY_NODE
GRADE_CHANGE_FROM_ABSTRACT_ALONE = NO
```

A downstream Chinese full-text mirror is discovery-only until compared against the official journal PDF.

## 12. Park 1990 — Japanese J-STAGE exact article route

Official J-STAGE directly verifies Heon-Wook Park / 朴憲郁, “礼拝共同体における κεφαλή の問題―Iコリント11:3–12について,” *New Testament Studies* / 『新約学研究』 18 (1990): 29–42, DOI `10.24758/jsnts.18.0_29`, with an open-access PDF route listed as 678 KB.

The Japanese title controls the passage identity as **1 Corinthians 11:3–12**. J-STAGE's English issue-level auto-title currently displays `1 Corinthians 1:3-12`; this conflicts with the Japanese title and DOI/article page and is treated as a metadata typo, not as a passage conflict.

```text
PARK_1990_JAPANESE_ARTICLE_IDENTITY = CLOSED_DIRECT_OFFICIAL
PARK_1990_JSTAGE = OPEN_ACCESS
PARK_1990_PDF_ROUTE = 678_KB_OFFICIAL
PARK_1990_BODY = TRANSPORT_REOPEN_CURRENT_RUNTIME
PARK_1990_ENGLISH_TOC_1COR1_3_12 = METADATA_TYPO
PARK_1990_KEPHALE_POSITION = NOT_INFERRED_FROM_TITLE
```

## 13. Vidović 2024 — Croatian exact chapter identity

Croatian national bibliography/CIP and the national biblical bibliography converge on Marinko Vidović, “Muškarac i žena u bogoštovnom kontekstu (1 Kor 11, 2-16),” in *Ali riječ Boga našeg ostaje dovijeka: zbornik u čast prof. dr. sc. Marijanu Vugdeliji, OFM*, ed. Domagoj Runje (Split, 2024), pp.203–242.

The national CIP fixes the volume at 376 pp. and ISBN `9789538460029`. No lawful full-chapter body was exposed by the present search routes.

```text
VIDOVIC_2024_CROATIAN_CHAPTER_IDENTITY = CLOSED_STRONG_NATIONAL_BIBLIOGRAPHIC
VIDOVIC_2024_RANGE = 203_242
VIDOVIC_2024_VOLUME_ISBN = 9789538460029
VIDOVIC_2024_FULL_BODY = ACQUISITION_OPEN
```

## 14. Won Joongum 2010 — Korean issue lineage + author-thesis route

The official KCI/RISS record for the 2020 Kim Seongie Olivia + Won Joongum article gives a later self-citation by Won to her own 2010 exact passage study:

`고린도전서 11:2-16에 대한 주석적 연구-아카타칼룹토스(akatakaluptos)를 중심으로`, `17:67–89`, 2010.

Because Won is herself co-author of the 2020 article this is stronger provenance than an unrelated secondary bibliography.

The serial lineage can now be narrowed substantially without inventing a primary article card. Sahmyook University's Theological Research Institute directly states that it published `신학리뷰` volumes 1–17. An independent Kyobo Scholar issue record directly identifies `신학리뷰 제17집` as a December 2010 issue of the Sahmyook University Theological Research Institute. Thus the self-citation's `17:67–89 / 2010` is a very strong fit to `신학리뷰 제17집`, but the target workflow still has not located the article's own primary database record.

A separate author-body route is also now closed at institutional-library identity level. The National Assembly Library of Korea directly records Won Joongum's MA thesis:

`바울 서신의 여성 관련 구절들에 대한 주석적 연구 : 성 차별적으로 보이는 내용들을 중심으로`

as a Sahmyook University Graduate School of Theology master's thesis, February 2010, call number `TM 220 -10-10`, electronic resource, with a KERIS full-text route plus TOC/abstract routes.

The broader thesis and the narrower `67–89` article may be genetically related, but they are **not treated as the same publication or identical body without direct comparison**.

```text
WON_2010_TITLE_PAGES_YEAR = STRONG_LATER_SELF_CITATION_CONTROL
SAHMYOOK_THEOLOGICAL_REVIEW_VOLS_1_17 = CLOSED_DIRECT_INSTITUTIONAL_HISTORY
SAHMYOOK_THEOLOGICAL_REVIEW_ISSUE_17 = CLOSED_ISSUE_LEVEL / 2010_12
WON_2010_ARTICLE_ISSUE17_MATCH = VERY_STRONG_LINEAGE_INFERENCE / NOT_PRIMARY_ARTICLE_CARD
WON_2010_PRIMARY_ARTICLE_RECORD = REOPEN
WON_2010_ARTICLE_FULL_BODY = REOPEN
WON_2010_MA_THESIS_IDENTITY = CLOSED_DIRECT_NATIONAL_LIBRARY
WON_2010_MA_THESIS_DATE = 2010_02
WON_2010_MA_THESIS_CALL_NUMBER = TM_220_10_10
WON_2010_MA_THESIS_KERIS_ROUTE = VERIFIED_ELECTRONIC_ROUTE
WON_2010_MA_THESIS_BODY = ACQUISITION_REOPEN
WON_2010_ARTICLE_BODY != WON_2010_THESIS_BODY_AUTOMATICALLY
DO_NOT_PROMOTE_ISSUE_INFERENCE_TO_PRIMARY_ARTICLE_CARD
```

## 15. Matos 2004 — Brazilian Portuguese official OA dissertation object

Official PUC Goiás TEDE repeatedly records Keila Carvalho de Matos, *Protagonismo e resistência de mulheres no discurso de Paulo em 1 Coríntios 11 e 14*, MA dissertation, advisor Ivoni Richter Reimer, with defense date **2004-12-10**. Repository facets mark the object `Acesso Aberto` and `application/pdf`.

A downstream date of `2007` conflicts with the university repository and is rejected for chronology. The repository still has not exposed the PDF bytes to the current runtime, so institutional object verification is kept distinct from body reading.

```text
MATOS_2004_OFFICIAL_TEDE_OBJECT = CLOSED_DIRECT_INSTITUTIONAL
MATOS_2004_DEFENSE_DATE = 2004_12_10
MATOS_2004_OA_PDF_OBJECT = VERIFIED_BY_REPOSITORY_METADATA
MATOS_2004_FULL_PDF_BODY = TRANSPORT_REOPEN
MATOS_2004_DATE_2007_DOWNSTREAM = REJECTED
```

## 16. 2026 German radar — Bieberstein context node

Katholische Universität Eichstätt-Ingolstadt's institutional repository records Sabine Bieberstein, “Anstößige Frisuren, provozierende Kleider und zu viel Schmuck: Neutestamentliche Blicke auf Haartracht, Schmuck und Kleider von Frauen,” *Welt und Umwelt der Bibel* 31 (Jan. 2026), no.119, pp.18–23.

The institutional abstract explicitly says the article sketches 1 Cor 11:2–16 together with 1 Tim 2:9–15 and 1 Pet 3:3 in relation to clothing, hairstyles, gender roles, and power. The repository marks full text as not freely accessible and the journal as non-peer-reviewed.

```text
BIEBERSTEIN_2026_IDENTITY_ABSTRACT = CLOSED_DIRECT_INSTITUTIONAL
BIEBERSTEIN_2026_FULL_BODY = NOT_OPEN
BIEBERSTEIN_2026_PEER_REVIEW = NO
BIEBERSTEIN_2026_ROLE = CONTEXT_RADAR_NOT_CORE_AUTHORITY
GRADE_CHANGE = NO
```

## 17. Current reopen queue after this sweep

```text
P0 REASONER_2025_FULL_BODY_AND_NOTES
P0 TERMESSOS_TAMIII1_870_DIRECT_PRIMARY_BODY
P0 KOWALSKI_2020_FULL_PDF_BODY
P1 MATOS_2004_FULL_PDF_BODY
P1 WON_2010_PRIMARY_ARTICLE_CARD_AND_BODY
P1 WON_2010_MA_THESIS_KERIS_BODY
P1 PARK_1990_JSTAGE_PDF_BODY
P1 VIDOVIC_2024_FULL_CHAPTER_BODY
```

Direct transport attempts in this runtime did not justify a body promotion for any of those still-open targets.

## 18. Search-state result

```text
ENGLISH_KNOWN_ROUTE_AUDIT = COMPLETE
MULTILINGUAL_REOPEN_SWEEP = ACTIVE
REGIONAL_LIBRARY_REOPEN_SWEEP = ACTIVE
NEW_DIRECT_NON_ENGLISH_BODY_FOUND = YES
NEW_AUTHORIZED_TRANSLATION_ROUTES_FOUND = YES
NEW_LICENSED_EBOOK_ROUTES_FOUND = YES
NEW_AUTHOR_FULL_PDF_ROUTES_FOUND = YES
NEW_INSTITUTIONAL_OR_OFFICIAL_OA_PDF_ROUTES_FOUND = YES
PARK_METADATA_TYPO_QUARANTINED = YES
WON_2010_ISSUE_LINEAGE_NARROWED = YES
WON_2010_PRIMARY_ARTICLE_CARD_CLOSED = NO
WON_2010_MA_THESIS_ROUTE_FOUND = YES
WON_2010_MA_THESIS_BODY_CLOSED = NO
MATOS_2004_BODY_CLOSED = NO
VIDOVIC_2024_BODY_CLOSED = NO
REASONER_2025_BODY_CLOSED = NO
TERMESSOS_TAMIII1_870_PRIMARY_GREEK_CLOSED = NO
CORE_GRADE_REVERSALS = 0
```

Do not return to a global `QUEUE_EMPTY` claim until the materially distinct multilingual/regional lanes are dispositioned.