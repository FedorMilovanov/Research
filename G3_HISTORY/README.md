# G3 Ministries — evidence reconstruction corpus

**Corpus ID:** `G3-HISTORY-2026-09-07`  
**Status:** `MERGED RESEARCH CHECKPOINT / NOT PUBLICATION-AUTHORIZED`  
**Current authority:** `main`  
**Research PR:** `#188` — merged 2026-09-08  
**Research merge commit:** `d88b146e6ebbf3182f9d16ff59f4ae0f97aa70e2`  
**Historical research head:** `02e4a191c87884771158afc38846d09a98ae6422`  
**Historical branch:** `research/g3-history-20260907` — retired after merge  
**Research cutoff:** 2026-09-08  
**Scope:** history, theology, governance, finances, institutional development, crises, operational wind-down and unresolved legacy/asset questions involving G3 Ministries / G3 Church Network.

## Purpose

This is a source-controlled reconstruction of G3 Ministries from public planning in 2011 through the 2025–2026 crises and aftermath. It is evidence infrastructure for later journalism/documentary work, not a polemical brief and not publication authorization.

Repository evidence authority:

- [`../data/repository-evidence-policy-v2.json`](../data/repository-evidence-policy-v2.json)
- [`../00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md`](../00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md)
- [`ENGINEERING_HARDENING_2026-09-08.md`](ENGINEERING_HARDENING_2026-09-08.md)
- [`DURABLE_CUSTODY_POLICY.md`](DURABLE_CUSTODY_POLICY.md)
- [`DURABLE_CUSTODY_MANIFEST.json`](DURABLE_CUSTODY_MANIFEST.json)

## Non-negotiable research rules

1. Primary, institutional, participant/recipient, secondary and discovery-only objects remain separate evidence classes.
2. One physical evidence object remains one evidence family; mirrors/renderers do not create independent corroboration.
3. Allegation documents prove what was alleged, not that every allegation is true.
4. Archive absence, HTTP failure and access control are not negative historical evidence.
5. Digital/platform/storefront/vendor state proves dated digital state, not beneficial ownership or legal closing.
6. Fact, testimony, inference, theological judgment and legal conclusion remain separate layers.
7. Corrections and downgrades are part of the research record; later canonical reconciliation controls over older PASS snapshots.
8. Machine transcription is diagnostic only and cannot by itself create quote-safe or `ITEM_VERIFIED` status.
9. `PUBLICATION_HOLD` is independent of whether the Research PR is eventually merged.

## Evidence vocabulary

Repository-global source classes:

- `A1` — primary legal/governmental/participant-created record
- `A2` — official independent investigation/transcript/report or primary institutional publication
- `A3` — official event-specific statement, board decision or institutional document
- `B1` — high-quality secondary corroboration; not sole support for disputed quote-safe claims
- `C` — context/discovery/unverified source; never quote-safe by itself
- `D` — excluded/unreliable/irrelevant/unidentified

Working claim states:

`VERIFIED_PRIMARY`, `CORROBORATED`, `PARTIALLY_VERIFIED`, `DISPUTED`, `UNVERIFIED`, `INFERENCE`, `REFUTED`.

## Canonical authority hierarchy

Current analytical authority:

- [`SOURCE_LEDGER.md`](SOURCE_LEDGER.md)
- [`CLAIMS_LEDGER.md`](CLAIMS_LEDGER.md)
- [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md)
- [`P0_CLOSURE_CHECKPOINT_2026-09-08.md`](P0_CLOSURE_CHECKPOINT_2026-09-08.md)
- focused forensic masters listed below.

`EVIDENCE_BATCH_*` / PASS files are append-only acquisition and reconciliation history. They do not override later canonical masters and must never be counted as independent evidence merely because the same object appears in several passes.

## Current working periodization

1. **2011–2012** — conception and preparation
2. **2013–2017** — church-centered conference growth
3. **2018–2020** — Dallas Statement, coalition narrowing and legal institutionalization
4. **2021–2022** — G3 Press / G3+ / Church Network / journal expansion
5. **2023–2024** — scale, political-theology boundary disputes and financial reversal
6. **2025** — Josh Buice crisis and attempted institutional reset
7. **2026** — Tom Buck dossier / anonymous circulation / PMBC-G3 governance crisis
8. **Aug–Sep 2026** — Church Network dissolution, announced operational wind-down and unresolved legal/asset aftermath

## Current strongest findings

### Institutional history / finances

- Public G3 planning is pinned to an official Aug. 10, 2011 announcement; the first conference occurred in 2013; Georgia nonprofit incorporation occurred in 2019.
- G3 deliberately expanded from conference ministry into publishing, streaming/media, a journal and a church network.
- The financial reversal begins in FY2023, before the 2025/2026 scandals. Raw IRS Part IX reconciles the FY2022→FY2023 expense increase of **$1,061,800**, dominated by conferences/meetings **+$817,283** and advertising **+$246,511**.
- FY2024/FY2025 Schedule L directly disclose salary to `KARIS L BUICE`, relationship `Daughter of Board Member`, at **$30,409** and **$31,880**. This is a disclosure fact, not a fraud/self-dealing finding; the filings do not name the parent.
- FY2022 filings report one **$590,000 commercial-real-estate donation**. FY2023 reports **$550,000 gross sale proceeds**, **$590,000 basis**, **$40,000 loss**, disappearance of the land/building accounting object, and a new **$416,227** notes/loans receivable later declining to **$251,197** and **$153,000**.
- Seller financing is plausible but unverified: exact parcel, buyer/grantee, deed/security instrument and note linkage remain a document/access hold.

### Living Heritage / G3+ / G3 Press

- Raw FY2025 `IRS990/Desc` primary-verifies that G3 separated **Living Heritage Homeschool as an independent entity during 2025**.
- That 2025 separation does **not** identify Living Heritage as the 2026 G3+ successor.
- A recipient-supplied G3+ subscriber email dated Aug. 27 now directly represents that **G3 Plus was being acquired by another ministry**, whose name was not yet being disclosed, and promises another notice **when the transition became final**.
- Current Q006 state is therefore:

`RECIPIENT_ARTIFACT_VERIFIED / ACQUISITION_IN_PROGRESS_REPRESENTED / TRANSFEREE_UNNAMED / COMPLETED_CLOSING_UNVERIFIED`.

- The visible email itself does not establish G3 Press as part of the same transaction. Press inclusion remains a weaker recipient/secondary layer pending a Press-specific transaction/recipient object.
- `Living Heritage = successor` and `Treefort = successor` are blocked. Living Heritage bundling and Treefort/app infrastructure are service/vendor evidence, not beneficial-ownership proof.
- Apple/Google G3 seller/developer metadata and the live G3+/Press surfaces are dated platform state only; they cannot prove either that a transfer closed or that it did not.

Canonical Q006 controls:

- [`ASSET_TRANSFER_FORENSICS.md`](ASSET_TRANSFER_FORENSICS.md)
- [`PRIMARY_SOURCE_G3PLUS_SUBSCRIBER_EMAIL_2026-08-27.md`](PRIMARY_SOURCE_G3PLUS_SUBSCRIBER_EMAIL_2026-08-27.md)
- [`ASSET_TRANSFER_TREEFORT_VENDOR_GUARDRAIL.md`](ASSET_TRANSFER_TREEFORT_VENDOR_GUARDRAIL.md)
- [`EVIDENCE_BATCH_2026-09-08_PASS23.md`](EVIDENCE_BATCH_2026-09-08_PASS23.md)

### Governance / legal status

- Georgia Secretary of State listed `G3 Ministries for the Church, Inc.` as **Active/Compliance** on Sep. 8, 2026. Operational wind-down therefore must not be called completed Georgia corporate dissolution at that cutoff.
- Official archived G3 `Who We Are` capture `20260721102641` primary-verifies a July 21, 2026 Board of Directors consisting of Buck Braswell, Matt Broome, Jon Norton, Matt Sikes, Dylan Joyner and Ron Mooney.
- Exact-head late-board CDX acquisition for Jul. 21–Aug. 31 returned only that capture. The exact target-page Wayback route is exhausted; absence of a later capture does **not** prove the roster stayed unchanged.
- Exact 2025 director transition mechanics remain a new-primary-evidence/document hold: both known G3 roster archive paths are exhausted for the critical window, while Georgia detail/history access is 403 unauthenticated.

### Buck / PMBC crisis

- Real insufficient attribution by Tom Buck and overbroad/misleading aspects of the anonymous dossier can both be true.
- All **17/17** accusation-sermon items have dedicated forensic files; **0/17** are `ITEM_VERIFIED` because human original-media listening, exact source edition/page and attribution context remain mandatory.
- Items **11–17** now have **7/7 successful bounded original-FBC-media acquisition**. Audio/video binaries were not retained in artifacts; machine transcripts are diagnostic only.
- The late-item results are deliberately non-binary: Items 11/12/13/15/17 have material source-dependence upgrades, Item 16 is dense but mixed, and Item 14 is a negative control where acquisition does not make the text-driven KNOW/OBEY/MEDITATE structure source-specific.
- Phil Johnson's original Aug. 19 Pyromaniacs article supports a real unattributed-commentary problem while distinguishing that from preaching other men's completed sermons.
- Bryan Chapell's 1998 Titus article anchors pre-Buck source lineage; Jennifer Buck's own Apr. 7, 2022 G3 article independently establishes analogous early-marriage circumstances before Buck's 2023 sermon and the 2026 controversy. The stronger claim that Buck simply fabricated a marriage biography is therefore `REFUTED`; wording/attribution remains separate.
- FBC Lindale did not simply ignore the allegations: acquired evidence describes review, outside consultation and corrective measures.
- Four PMBC pastors admitted improper anonymous external action/interference and mischaracterizing Lindale's handling without all details. The reproduced participant statement remains one underlying evidence family.
- PMBC resignation mechanics remain `DISPUTED`: participant wording says all four voluntarily resigned; secondary accounts describe deacon pressure/requirement for three and a voluntary Joyner resignation. No PMBC minutes/deacon record/resignation instrument resolves it.
- Matt Sikes' Aug. 16 pre-publication announcement is preserved as a separate primary-source control; it documents what leadership told the congregation before publication but does not settle the later resignation mechanics.
- Claims about latex gloves, proven revenge motive and federal mail-fraud liability remain below publication threshold.

## Current P0 boundary

The remaining P0 uncertainty is no longer ordinary search debt. It requires genuinely new primary evidence, authorized/access-controlled records or later state changes:

1. **G3+ successor/closing:** named transferee, final-transition/transaction object, terms, board approval/conflicts and closing date.
2. **G3 Press:** Press-specific recipient/transaction evidence plus title-level rights/inventory reconstruction.
3. **FY2022 real estate:** deed/legal description, grantor/grantee, security/note instrument and explicit receivable linkage.
4. **Crisis-day board:** another dated primary object after July 21.
5. **2025 director transitions:** resignation/minutes/appointment instruments or authorized filing history.

See [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md) and [`P0_CLOSURE_CHECKPOINT_2026-09-08.md`](P0_CLOSURE_CHECKPOINT_2026-09-08.md) for the route-exhaustion state machine.

## Corpus map

### Core authority

- [`TIMELINE.md`](TIMELINE.md)
- [`SOURCE_LEDGER.md`](SOURCE_LEDGER.md)
- [`CLAIMS_LEDGER.md`](CLAIMS_LEDGER.md)
- [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md)
- [`P0_CLOSURE_CHECKPOINT_2026-09-08.md`](P0_CLOSURE_CHECKPOINT_2026-09-08.md)
- [`IRS_RAW_XML_ACQUISITION_GATE.md`](IRS_RAW_XML_ACQUISITION_GATE.md)
- [`ENGINEERING_HARDENING_2026-09-08.md`](ENGINEERING_HARDENING_2026-09-08.md)
- [`DURABLE_CUSTODY_POLICY.md`](DURABLE_CUSTODY_POLICY.md)
- [`DURABLE_CUSTODY_MANIFEST.json`](DURABLE_CUSTODY_MANIFEST.json)

### Finance / governance / assets

- [`FINANCES.md`](FINANCES.md)
- [`FINANCIAL_FORENSICS_2023.md`](FINANCIAL_FORENSICS_2023.md)
- [`GOVERNANCE.md`](GOVERNANCE.md)
- [`DIRECTOR_TRANSITION_FORENSICS_2025.md`](DIRECTOR_TRANSITION_FORENSICS_2025.md)
- [`ASSET_TRANSFER_FORENSICS.md`](ASSET_TRANSFER_FORENSICS.md) — canonical Q006
- [`ASSET_TRANSFER_AND_RIGHTS.md`](ASSET_TRANSFER_AND_RIGHTS.md) — broader title/platform discovery reconstruction

### Crisis dossiers / primary controls

- [`BUICE_2025.md`](BUICE_2025.md)
- [`BUCK_2026.md`](BUCK_2026.md)
- [`BUCK_DOSSIER_AUDIT.md`](BUCK_DOSSIER_AUDIT.md)
- [`BUCK_ITEMS/README.md`](BUCK_ITEMS/README.md)
- [`PRIMARY_SOURCE_JENNIFER_BUCK_2022_RESTORATIVE_GRACE.md`](PRIMARY_SOURCE_JENNIFER_BUCK_2022_RESTORATIVE_GRACE.md)
- [`PRIMARY_SOURCE_PMBC_2026-08-16_PREPUBLICATION_ANNOUNCEMENT.md`](PRIMARY_SOURCE_PMBC_2026-08-16_PREPUBLICATION_ANNOUNCEMENT.md)
- [`PRIMARY_SOURCE_G3PLUS_SUBSCRIBER_EMAIL_2026-08-27.md`](PRIMARY_SOURCE_G3PLUS_SUBSCRIBER_EMAIL_2026-08-27.md)
- [`PRAYS_MILL_AUTHORITY_AND_DISCIPLINE_LEADS.md`](PRAYS_MILL_AUTHORITY_AND_DISCIPLINE_LEADS.md)
- [`2021_MACARTHUR_LIVE_EPISODE.md`](2021_MACARTHUR_LIVE_EPISODE.md)

### History / ideology / media

- [`CONFERENCE_HISTORY.md`](CONFERENCE_HISTORY.md)
- [`IDEOLOGY_AND_COALITION.md`](IDEOLOGY_AND_COALITION.md)
- [`IDEOLOGY_CONTENT_CODING_PROTOCOL.md`](IDEOLOGY_CONTENT_CODING_PROTOCOL.md)
- [`MEDIA_LEDGER.md`](MEDIA_LEDGER.md)
- [`drafts/ARTICLE_OUTLINE.md`](drafts/ARTICLE_OUTLINE.md)

### Acquisition history

`EVIDENCE_BATCH_2026-09-07_PASS2.md` through `EVIDENCE_BATCH_2026-09-08_PASS23.md` are append-only forensic history, not a second evidence system.

## Research closure vs publication

At PASS23, the current public evidence universe is **proof-route complete at P0 level** in the following sense: remaining major unknowns are explicitly attached to new-primary-evidence, human-source-review or authorized-access gates rather than to unperformed obvious searches.

This does **not** make the corpus article-ready automatically. Publication still requires quote-safe human review, item-level media/rights decisions, and a frozen immutable Research commit/claim set.

## Publication status

**PUBLICATION_HOLD.** Research merge/checkpoint completion does not authorize publication of allegations, screenshots, images, quotes or conclusions.