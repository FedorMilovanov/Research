# G3 HISTORY — canonical reconciliation map for PASS3–PASS11

**Status:** ACTIVE / STRUCTURAL / PUBLICATION_HOLD  
**Purpose:** prevent staging batches from becoming a second evidence system or inflating corroboration counts.  
**Canonical baseline before this map:** `SOURCE_LEDGER.md` through `G3-S054`; `CLAIMS_LEDGER.md` through `G3-C068`.

This file does **not** itself promote a source or claim. It records how each provisional PASS3–PASS11 row must be handled in the next canonical-ledger rewrite.

## Repository schema authority

`data/repository-evidence-policy-v2.json` is controlling.

Canonical source rows must keep separate concepts separate:

- evidence class: `A1 / A2 / A3 / B1 / C / D`;
- access: `FULL_OBJECT_VERIFIED / PARTIAL_OBJECT / CATALOG_ONLY / LINK_ONLY / NOT_ACQUIRED`;
- locator: `EXACT_LOCATOR_VERIFIED / COARSE_LOCATOR_ONLY / LOCATOR_MISSING`;
- rights: `PUBLICATION_ELIGIBLE / STORAGE_ONLY / PRIVATE_STUDY_ONLY / PERMISSION_REQUIRED / RIGHTS_UNKNOWN`;
- publication state: `PROMOTE / REFERENCE / SUPERSEDED / BLOCKED`;
- holds are annotations, not source classes or access states.

Therefore free-form staging phrases such as `ORIGINAL_LOCATOR_VERIFIED / CONTENT_ACCESS_HOLD` must be normalized, e.g.:

- access = `LINK_ONLY`;
- locator = `EXACT_LOCATOR_VERIFIED`;
- rights = item-specific conservative value;
- publication = `REFERENCE` or `BLOCKED`;
- note/hold = `EVIDENCE_HOLD` / `ARCHIVE_HOLD` as appropriate.

Likewise canonical claim `State` stays within:

`VERIFIED_PRIMARY / CORROBORATED / PARTIALLY_VERIFIED / DISPUTED / UNVERIFIED / INFERENCE / REFUTED`.

Qualifiers such as `PRIMARY_LOCATOR`, `CONTENT_HOLD`, `AS_PARTICIPANT_ASSESSMENT` and `DATE_BOUNDARY` belong in the publication note, not the state field.

---

# 1. Source reconciliation

Legend:

- `NEW_CANONICAL` — distinct source object worth adding to the canonical ledger;
- `UPGRADE_EXISTING` — improve the canonical source row/access/locator; do not count twice;
- `ALIAS_UNDERLYING` — distinct presentation or citation of the same underlying evidence object; preserve provenance but no independent corroboration count;
- `STAGING_ONLY` — retain in acquisition history; no canonical source row currently needed.

## PASS3 — S055–S062

| Staging ID | Action | Canonical target / rationale |
|---|---|---|
| S055 | `NEW_CANONICAL` | Identified 2014 David Jackman/Crossway book sample. Distinct source object for Joshua Items 14–15. |
| S056 | `NEW_CANONICAL` | FBC Lindale official Jan–Mar 2026 Joshua sermon/archive surfaces. |
| S057 | `NEW_CANONICAL` | Jackman teaching archive establishing upstream authorial formula lineage. |
| S058 | `NEW_CANONICAL` | Official Feb. 6, 2026 Braswell G3 board-identification page; distinct dated object extending canonical S045. |
| S059 | `NEW_CANONICAL` | 2023 attendee report/photo source. Keep B1; media rights remain separate. |
| S060 | `NEW_CANONICAL` | 2020 participant report/photo source. Keep B1; media permission required. |
| S061 | `UPGRADE_EXISTING` | Upgrade canonical S036 (same Chapell 1998 source lineage) rather than count as another witness to the same text. If exact original journal object is truly acquired, S036 access/class should be revised accordingly. |
| S062 | `UPGRADE_EXISTING` | Canonical S037 already represents the same Mefferd/Jennifer Buck counterevidence family. Improve exact locator/access, do not duplicate. |

## PASS4 — S063–S071

| Staging ID | Action | Canonical target / rationale |
|---|---|---|
| S063 | `NEW_CANONICAL` | Official Dallas Statement `History and Formation`; distinct primary institutional history object. |
| S064 | `NEW_CANONICAL` | Official 2022 first Regional Conference article. |
| S065 | `NEW_CANONICAL` | Official 2023 Sovereignty of God study/theme anchor. |
| S066 | `UPGRADE_EXISTING` | Same July 2025 official Aniol appointment object already represented conceptually at S010. Expand S010 with exact locator and ecosystem-scale details; do not create false second official witness. |
| S067 | `UPGRADE_EXISTING` | Same IRS Form 990 bulk-download route already canonical S028. |
| S068 | `ALIAS_UNDERLYING` | Same official Feb. 6, 2026 Braswell object represented provisionally as S058. Keep one canonical object only. |
| S069 | `UPGRADE_EXISTING` | Same Michelle Lesley transfer/discovery page family already canonical S019. |
| S070 | `NEW_CANONICAL` | Official pre-2018 G3 political/cultural article/archive objects; distinct history evidence. |
| S071 | `NEW_CANONICAL` | 2019 Social Justice preconference contemporaneous record; B1 until official event schedule captured. |

## PASS5 — S072–S075

| Staging ID | Action | Canonical target / rationale |
|---|---|---|
| S072 | `UPGRADE_EXISTING` | Canonical S012 already represents Phil Johnson `Haman's Gallows`; replace old republication-only note with recovered original TeamPyro locator/access. |
| S073 | `NEW_CANONICAL` | Ethan Jago first-person resignation/investigation statement. |
| S074 | `NEW_CANONICAL` | MinistryWatch preservation of Ascol mailing-chain account. Independent publication object; still not substitute for Ascol original. |
| S075 | `UPGRADE_EXISTING` | Canonical S026 already represents Jon Benzinger; add exact first-person locator/access without duplicate count. |

## PASS6 — S076–S080

| Staging ID | Action | Canonical target / rationale |
|---|---|---|
| S076 | `NEW_CANONICAL` | Exact original Tom Ascol X status locator. Access should be `LINK_ONLY`, not `FULL_OBJECT_VERIFIED`, until content captured directly. |
| S077 | `NEW_CANONICAL` | Exact G3 Conference X status locator for Church Network dissolution; text preserved elsewhere. |
| S078 | `UPGRADE_EXISTING` | Underlying four-pastor participant letter already represented at S015/S042. Use this to improve text-preservation/provenance, not as another independent source. |
| S079 | `UPGRADE_EXISTING` | Same Michelle Lesley resignation-mechanics page already canonical S043. |
| S080 | `ALIAS_UNDERLYING` | Same FBC Lindale Aug. 25 institutional statement family already carried via S035/secondary reproductions. Preserve extra text provenance without counting a second FBC statement. |

## PASS7 — S081–S083

| Staging ID | Action | Canonical target / rationale |
|---|---|---|
| S081 | `NEW_CANONICAL` | Brent Detwiler contemporaneous compilation; C only, with strict one-compiler-object guardrail. |
| S082 | `NEW_CANONICAL` | Independent GNL episode index confirming MacArthur G3 Podcast E31 identity. |
| S083 | `STAGING_ONLY` | YouTube/index metadata adds limited episode identity and creates publication-date ambiguity; keep as discovery metadata unless later needed for a specific canonical claim. |

## PASS8 — S084–S090

| Staging ID | Action | Canonical target / rationale |
|---|---|---|
| S084 | `UPGRADE_EXISTING` | Same official IRS bulk-download route already canonical S028. |
| S085 | `UPGRADE_EXISTING` | Same FY2025 IRS filing represented through canonical S002. Add exact full-filing/object provenance; it is not an independent witness from the IRS XML. |
| S086 | `UPGRADE_EXISTING` | Same philanthropy.org FY2024 parser already canonical S029. Add complete Part VII names/details. |
| S087 | `UPGRADE_EXISTING` | Same Michelle Lesley transfer page / subscriber-email reproduction already canonical S019. |
| S088 | `NEW_CANONICAL` | David Morrill X transfer-transparency post is a distinct original participant/commentator object; C unless direct content capture supports higher class. |
| S089 | `UPGRADE_EXISTING` | Same official G3 Press storefront already canonical S053. |
| S090 | `UPGRADE_EXISTING` | Same Google Play G3+ app metadata family already canonical S032/S050. Preserve date conflict; do not create a third platform source row. |

## PASS9 — S091–S095

| Staging ID | Action | Canonical target / rationale |
|---|---|---|
| S091 | `NEW_CANONICAL` | Dave Jenkins original X status locator. Link-only until direct content capture; participant text preserved by contemporaneous source and current title state corroborates outcome. |
| S092 | `NEW_CANONICAL` | Darrell Harrison original X status locator. Distinct participant request object. |
| S093 | `NEW_CANONICAL` | Justin Peters original X status locator. Distinct content-removal request object. |
| S094 | `NEW_CANONICAL` | Contemporaneous preservation/direct-link bridge for Jenkins/Harrison/Peters. C or B1 only after editorial-quality judgment; polemical conclusions excluded. |
| S095 | `STAGING_ONLY` | Repeat live HTTP measurement of the same root-503 phenomenon already canonical S049; useful log entry, not a new independent source. |

## PASS10 — S096–S098

| Staging ID | Action | Canonical target / rationale |
|---|---|---|
| S096 | `NEW_CANONICAL` | Exact Wayback archive target for official G3 `Who We Are`, timestamp 2026-07-21 10:26:41 UTC. Normalize to access `LINK_ONLY`, locator exact, `ARCHIVE_HOLD` note; do **not** class snapshot content as verified until body acquired. |
| S097 | `NEW_CANONICAL` | Aug. 19 secondary report that exposes the exact Wayback link and attributed six-name roster. C; useful archive-discovery provenance. |
| S098 | `STAGING_ONLY` | Same outlet, same six-name assertion, same Wayback object. Adds consistency but no independent corroboration; preserve in PASS10 only. |

## PASS11 — S099–S102

| Staging ID | Action | Canonical target / rationale |
|---|---|---|
| S099 | `NEW_CANONICAL` | Michael O'Fallon original Twitter/X resignation status `1673411411513425920`. Link-only until direct body capture; participant text contemporaneously preserved. |
| S100 | `NEW_CANONICAL` | Baptist News Global independent next-day preservation of O'Fallon's first-person resignation account. |
| S101 | `NEW_CANONICAL` | Contemporaneous board-page-change/Wayback discovery report; C, and its `removed` interpretation must not be inherited. |
| S102 | `NEW_CANONICAL` | ProPublica API v2 documentation, used only for acquisition-method capability boundary. |

### Source-count consequence

PASS3–PASS11 contains **48 provisional source IDs (S055–S102)**, but they are **not 48 independent evidentiary sources**. The canonicalization plan deliberately collapses duplicate/access-upgrade families.

Examples that must count once for substantive corroboration:

- one IRS filing exposed through IRS → ProPublica → parser;
- one four-pastor letter reproduced by multiple outlets;
- one G3+ subscriber email discussed by Lesley/Morrill/others;
- one Jenkins X statement reproduced by a secondary outlet and corroborated by the later title state;
- one July 21 Wayback G3 board object referenced by multiple articles;
- one physical Buck accusation dossier registered at S014/S034.

---

# 2. Claim reconciliation

The next canonical rewrite should **not mechanically append C069–C135**. Several staging claims are refinements or duplicate formulations of existing canonical claims.

## PASS3 — C069–C076

| Claim | Action | Rationale |
|---|---|---|
| C069 | `NEW_CANONICAL` | Joshua 2 source-object closure on source side. |
| C070 | `NEW_CANONICAL` | Row-specificity distinction. |
| C071 | `NEW_CANONICAL` | Joshua 3 partial dependence candidates / dual-object hold. |
| C072 | `NEW_CANONICAL` | Braswell official board status through Feb. 6, 2026. Use this as the canonical Feb-2026 formulation. |
| C073 | `UPDATE_C030` | Named transferee remains unknown; do not duplicate same open question. |
| C074 | `UPDATE_C029` | Formal Georgia dissolution remains unverified. |
| C075 | `UPDATE_C040` | Fabricated-marriage claim already canonical refuted. |
| C076 | `UPDATE_C039` | Chapell pre-Buck lineage already canonical corroborated. |

## PASS4 — C077–C088

| Claim | Action | Rationale |
|---|---|---|
| C077 | `NEW_CANONICAL` | Dallas formation date/count/organizer. |
| C078 | `NEW_CANONICAL` | 2018→2019 social-justice boundary chronology. |
| C079 | `NEW_CANONICAL` | First 2022 regional event / ~700. |
| C080 | `NEW_CANONICAL` | 2023 national main theme. |
| C081 | `NEW_CANONICAL` | Blocks conflation of CN/theonomy debate with main conference theme. |
| C082 | `NEW_CANONICAL` | July 2025 ecosystem-scale statement. |
| C083 | `ALIAS_C072` | Same Feb. 6 Braswell claim. Do not retain twice. |
| C084 | `UPDATE_C032` | Six-name late board still unverified; later PASS10 strengthens locator only. |
| C085 | `UPDATE_C030` | Dated public-search state, not a separate durable factual proposition. |
| C086 | `NEW_CANONICAL` | Direct pre-2018 political/cultural G3 media. |
| C087 | `NEW_CANONICAL` | Blocks prevalence inference from search presence. |
| C088 | `NEW_CANONICAL_METHOD` | Raw IRS route / content hold. Could live in acquisition log rather than narrative claim if claim ledger remains article-focused. |

## PASS5 — C089–C095

| Claim | Action | Rationale |
|---|---|---|
| C089 | `NEW_CANONICAL` | Johnson March 27 participant chronology. |
| C090 | `NEW_CANONICAL` | Johnson assessment: real attribution failures ≠ finished-sermon theft. Normalize state to `CORROBORATED` with participant-assessment note. |
| C091 | `NEW_CANONICAL` | Jago’s own resignation/withdrawal/removal requests. |
| C092 | `NEW_CANONICAL` | Private Jago investigation does not independently prove every underlying allegation. |
| C093 | `NEW_CANONICAL` | Independent identifiable packet recipients. |
| C094 | `NEW_CANONICAL` | Ascol account of elder admission/claimed pastor consensus; testimony boundary. |
| C095 | `NEW_CANONICAL` | Consulted pastors’ reported denial creates real countertestimony. |

## PASS6 — C096–C102

| Claim | Action | Rationale |
|---|---|---|
| C096 | `NEW_CANONICAL_PROVENANCE` | Exact Ascol original post locator. Could instead live solely in source ledger if claim ledger is kept substantive. |
| C097 | `NEW_CANONICAL_PROVENANCE` | Exact G3 network-dissolution post locator. |
| C098 | `UPDATE_C027` | Same substantive Church Network dissolution claim. |
| C099 | `NEW_CANONICAL_SUBCLAIM` | Participant public characterization that all four resignations were voluntary. Needed because C048 records the conflict globally. |
| C100 | `NEW_CANONICAL_SUBCLAIM` | Lesley counter-report that three were required; state `DISPUTED`. |
| C101 | `NEW_CANONICAL` | Blocks inference `voluntary = wholly spontaneous/unrequested`. |
| C102 | `NEW_CANONICAL` | FBC event-specific chronology/first-admission characterization. |

## PASS7 — C103–C108

| Claim | Action | Rationale |
|---|---|---|
| C103 | `REFINE_C035` | October recording-time artifact within MacArthur episode. |
| C104 | `REFINE_C035` | `few weeks` vs early October chronology discrepancy. |
| C105 | `REFINE_C035` | `live` semantics alone do not establish intent. |
| C106 | `NEW_CANONICAL_INFERENCE` | Narrow recording-age discrepancy stronger than bare live-label accusation. |
| C107 | `UPDATE_C036` | Same institutional-culture inference remains unproved. |
| C108 | `NEW_CANONICAL_LOW_IMPACT` | Podcast E31 identity. Could remain in episode dossier rather than master claim ledger if keeping master lean. |

## PASS8 — C109–C117

| Claim | Action | Rationale |
|---|---|---|
| C109 | `MERGE_WITH_C088` | Raw IRS availability/transport blocker; one acquisition-method claim is enough. |
| C110 | `NEW_CANONICAL` | FY2025 visible Aniol/Braswell/Broome bridge, explicitly incomplete. |
| C111 | `NEW_CANONICAL` | FY2024 nine Part VII persons, with 7-voting-member caveat. |
| C112 | `NEW_CANONICAL` | FY24→FY25 proves transition, not exit reasons/dates. |
| C113 | `REFINE_C030` | G3+ subscriber notice says unnamed ministry acquisition/continuity; substantive positive layer. |
| C114 | `NEW_CANONICAL` | Press being handled by same unnamed ministry remains partially verified/transaction-object hold. |
| C115 | `NEW_CANONICAL_GUARDRAIL` | Right Response remains unverified rumor. |
| C116 | `MERGE_C058_C065` | Existing canonical claims already block platform-state→ownership inference. |
| C117 | `NEW_CANONICAL_GUARDRAIL` | Search failure does not prove Georgia active status. Could live under C029 publication note if keeping ledger compact. |

## PASS9 — C118–C124

| Claim | Action | Rationale |
|---|---|---|
| C118 | `NEW_CANONICAL_PROVENANCE` | Exact Jenkins original status locator. |
| C119 | `UPDATE_C067` | Same completed title-level reversion/republication conclusion, now stronger provenance. |
| C120 | `NEW_CANONICAL_PROVENANCE` | Exact Harrison original status locator. |
| C121 | `NEW_CANONICAL` | Harrison publicly requested rights return; completion still unverified. |
| C122 | `NEW_CANONICAL_PROVENANCE` | Exact Peters original status locator. |
| C123 | `NEW_CANONICAL` | Peters/Osman G3+ hosted-content removal request. |
| C124 | `NEW_CANONICAL_GUARDRAIL` | Stale surface cannot prove request denial. Could remain asset dossier-only if master claim ledger gets too granular. |

## PASS10 — C125–C129

| Claim | Action | Rationale |
|---|---|---|
| C125 | `NEW_CANONICAL_PROVENANCE` | Exact July 21 official-page archive target/timestamp. |
| C126 | `UPDATE_C032` | Six-person roster improves to `PARTIALLY_VERIFIED` on locator/provenance, but snapshot body still unacquired. |
| C127 | `STAGING_ONLY_META` | `untraceable assertion` is a research-status correction, not article claim. |
| C128 | `ALIAS_C072` | Same Braswell Feb. 6 primary claim. |
| C129 | `NEW_CANONICAL_GUARDRAIL` | July 21 snapshot cannot silently equal exact Aug-crisis roster if intervening changes possible. |

## PASS11 — C130–C135

| Claim | Action | Rationale |
|---|---|---|
| C130 | `NEW_CANONICAL` | O'Fallon publicly said he submitted resignation in June 2023. |
| C131 | `NEW_CANONICAL` | Forced removal because of CN dispute is unsupported by current record. Normalize state to `REFUTED` with scope `unsupported`, not proof that no pressure existed. |
| C132 | `NEW_CANONICAL_GUARDRAIL` | Opposite absolute (`no relationship to controversy`) also unverified. |
| C133 | `NEW_CANONICAL` | Board-page change still useful chronology independent of mechanics. |
| C134 | `NEW_CANONICAL_METHOD` | ProPublica v2 API is not documented as full Schedule L XML endpoint. Better in acquisition log if master claim ledger is article-only. |
| C135 | `MERGE_WITH_C088` | Raw IRS XML remains the Schedule L/Part IX closure target. |

---

# 3. Recommended canonical rewrite order

Do not edit `SOURCE_LEDGER.md` and `CLAIMS_LEDGER.md` in parallel or through multiple agents. The next owner should do one sequential CAS-safe pass:

1. **Source ledger first**
   - upgrade existing rows (`S002`, `S010`, `S012`, `S019`, `S026`, `S028`, `S029`, `S032/S050`, `S036`, `S037`, `S043`, `S053/S054`);
   - append only `NEW_CANONICAL` source objects with fresh canonical IDs;
   - put alias/superseded relationships in notes;
   - add explicit `Publication` column and normalize legacy `Rights=REFERENCE` drift in a dedicated schema migration or, if too large for this lane, leave a clearly scoped follow-up without inventing mixed values.

2. **Claim ledger second**
   - update existing C029/C030/C032/C035/C036/C039/C040/C027/C048/C058/C065/C067/C068 where later passes strengthened or narrowed them;
   - append only genuinely distinct high-value claims;
   - keep provenance-only/method-only propositions out of the article-facing claim layer unless the corpus intentionally wants a forensic-method claim class.

3. **Dossiers/timeline third**
   - update Q003 O'Fallon/late-board chronology;
   - update Q006 creator-rights provenance;
   - update P0 IRS acquisition log with the API dead-end closure;
   - do not alter `PUBLICATION_HOLD`.

4. **PR checkpoint last**
   - exact-head compare against current `main`;
   - refresh PR #188 body with the actual head/commit/file/addition counts;
   - read CI/workflow status at that exact head;
   - keep PR Draft.

# 4. Why this map is necessary

Without this reconciliation, the corpus could accidentally report false corroboration such as:

- `IRS + ProPublica + philanthropy.org = three independent sources` when all derive from one filing;
- `S014 + S034 = two Buck dossier sources` when they are one physical PDF;
- `ChurchLeaders + Crosswalk + four-pastor letter = multiple admissions` when several surfaces reproduce one letter;
- `Lesley + Morrill = two transfer notices` when both may be discussing one subscriber email;
- `two EDW articles = two confirmations of the final board` when both point to the same July 21 Wayback capture;
- `Jenkins current product page = another witness to what Jenkins tweeted` when it is independent only as evidence of present republication state, not of the historical wording of his tweet.

The canonical corpus must count **underlying evidence objects and genuinely independent witnesses**, not URLs.
