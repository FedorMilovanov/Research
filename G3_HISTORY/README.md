# G3 Ministries — evidence reconstruction corpus

**Corpus ID:** `G3-HISTORY-2026-09-07`  
**Status:** `ACTIVE / NOT PUBLICATION-AUTHORIZED`  
**Research branch:** `research/g3-history-20260907`  
**Research PR:** `#188` — Draft / Research checkpoint  
**Research cutoff:** 2026-09-08  
**Scope:** history, theology, governance, finances, institutional development, crises and closure/aftermath of G3 Ministries / G3 Church Network.

## Purpose

This corpus is a source-controlled reconstruction of G3 Ministries from its public conception in 2011 through the 2025–2026 leadership crises, operational wind-down and unresolved asset/legacy questions. It is intended to support a later long-form article / documentary dossier, not to function as a polemical brief for or against G3.

The governing repository evidence policy is [`../data/repository-evidence-policy-v2.json`](../data/repository-evidence-policy-v2.json). Publication is fail-closed under [`../00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md`](../00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md).

## Research principles

1. **The YouTube video `G3EX6PaPUmc` is a discovery lead, not evidence.** Its captions are used to generate claims and names that must then be checked against primary or independently corroborated sources.
2. **No moral exoneration by sympathy.** Real wrongdoing, including unattributed borrowing, deceptive anonymity, false statements, governance failures or other misconduct, is recorded when evidence supports it.
3. **No inflation by outrage.** Motive, criminal liability, conspiracy, fraud, institutional causation and individual culpability are not inferred merely because surrounding conduct is troubling.
4. **Local-church and parachurch roles are kept distinct.** Actions by Pray’s Mill Baptist Church elders, G3 officers, G3 directors and G3 Church Network actors are mapped by role and date.
5. **Event date != publication date != archive date != filing date.** Each is recorded separately when material.
6. **Primary documents outrank commentary.** Secondary and polemical outlets may locate evidence but cannot alone support disputed quote-safe claims.
7. **Absence of evidence is not evidence of absence.** Archive gaps, transport failures and access-control boundaries remain explicit gaps, not negative factual proof.
8. **Theological evaluation is separated from factual reconstruction.** A factual record may establish conduct without automatically resolving ecclesiological or pastoral-disqualification judgments.
9. **Digital state is evidence only of digital state.** Search indexes, stale pages, app-store metadata and storefronts are dated artifacts; they do not silently override event-specific statements, legal records or ownership evidence.
10. **Corrections are part of the evidence record.** If a later pass weakens or upgrades an earlier finding, the corpus records the change rather than preserving the more dramatic or older version.
11. **One physical evidence object is one evidence family.** IRS renderers, mirrors or republications do not become independent corroboration merely because multiple services expose the same underlying filing or statement.

## Evidence vocabulary

Repository-global source classes are used without local redefinition:

- `A1` — primary legal/governmental/participant-created record
- `A2` — official independent investigation/transcript/report or primary institutional publication
- `A3` — official event-specific statement, board decision or institutional document
- `B1` — high-quality secondary corroboration; not sole support for disputed quote-safe claims
- `C` — context/discovery/unverified source; never quote-safe
- `D` — excluded/unreliable/irrelevant/unidentified

Working claim states used in this corpus:

- `VERIFIED_PRIMARY`
- `CORROBORATED`
- `PARTIALLY_VERIFIED`
- `DISPUTED`
- `UNVERIFIED`
- `INFERENCE`
- `REFUTED`

These claim states do **not** replace the repository-global evidence classes.

## Canonical vs staging rule

`SOURCE_LEDGER.md`, `CLAIMS_LEDGER.md`, `OPEN_QUESTIONS.md`, the focused forensic masters and the P0 checkpoint are the current analytical authority.

`EVIDENCE_BATCH_*` / PASS files are dated acquisition history. They preserve what was known at each pass and may contain provisional IDs or states later upgraded by raw acquisition. They must **not** be counted as a second independent evidence system and must not override later canonical reconciliation.

## Current working periodization

1. **2011–2012 — conception and preparation**
2. **2013–2017 — church-centered conference growth**
3. **2018–2020 — Dallas Statement, coalition narrowing and legal institutionalization**
4. **2021–2022 — ecosystem expansion: G3 Press / G3+ / Church Network / journal**
5. **2023–2024 — scale, political-theology boundary disputes and financial reversal**
6. **2025 — Josh Buice crisis and attempted institutional reset**
7. **2026 — Tom Buck dossier / anonymous circulation / PMBC-G3 governance crisis**
8. **Aug–Sep 2026 — Church Network dissolution, announced conclusion of operations and unresolved asset/legal aftermath**

## Current strongest findings

- Public conception is directly pinned to an official **Aug. 10, 2011** G3 announcement; first conference was in 2013; legal nonprofit incorporation occurred in Georgia in 2019.
- Early national conferences were predominantly centered on gospel, church, Scripture, Trinity, Reformation, missions, worship and Christ; culture/political polemics nevertheless appeared in the wider G3 media ecosystem early.
- G3 deliberately expanded from conference to a multi-product ecosystem including publishing, streaming/media, a journal and a church network.
- G3’s ideological history is not a simple one-axis move `ever farther right`: social-justice/CRT boundaries hardened, while official 2023 G3/Scott Aniol material also resisted Christian Nationalism/theonomy and drew criticism from the right flank.
- The financial reversal begins in FY2023, before the 2025/2026 crises. Raw IRS Part IX reconciles the FY2022→FY2023 expense increase exactly: **+$1,061,800**, dominated by conferences/meetings **+$817,283** and advertising **+$246,511**. Payroll and administrative-overhead explanations do not match the filed category pattern.
- FY2024/FY2025 raw Schedule L rows disclose salary to `KARIS L BUICE`, identified only as `Daughter of Board Member`, at **$30,409** and **$31,880**. The filings report the excess-benefit indicator false. This is a disclosure fact, not a self-dealing/fraud finding, and the specific parent is not inferred from surname alone.
- FY2022 raw filings report one **$590,000 commercial-real-estate donation**. FY2023 reports an asset sale with **$550,000 gross proceeds**, **$590,000 basis** and **$40,000 loss**, while the corresponding land/building balance disappears. A new **$416,227** notes/loans receivable then declines to **$251,197** and **$153,000** in later filings. Seller financing is plausible but unverified pending deed/note evidence.
- Raw FY2025 `IRS990/Desc` states that G3 separated **Living Heritage Homeschool as an independent entity from G3 Ministries during 2025**. This is `VERIFIED_PRIMARY`; it does **not** identify Living Heritage as the unnamed 2026 G3+/G3 Press successor.
- The May 2025 Josh Buice crisis is supported by G3’s own statement and must be treated separately from the 2026 Buck controversy. Founders and recipient-journalism records independently sharpen target identity and the Voddie Baucham anonymous-email episode.
- Tom Buck is strongly anchored as a G3 board participant at the May 2025 Buice-crisis decision point. Current evidence places his departure after that episode and before Scott Aniol’s presidency became effective July 9, 2025, but exact resignation date/instrument and motive remain open.
- Both identified official May–July 2025 board-roster archive paths are exhausted for that transition window. Georgia’s public result row is acquired and its current internal business ID/official detail POST contract are resolved, but the finer BusinessInformation/filing-history request returns HTTP 403. Exact transition dates therefore require a genuinely new primary object or authorized filing-history access rather than another parser fix.
- An official archived G3 `Who We Are` snapshot on **July 21, 2026** primary-verifies a six-person Board of Directors: Buck Braswell, Matt Broome, Jon Norton, Matt Sikes, Dylan Joyner and Ron Mooney. Exact continuity through the late-August crisis remains open because no later primary roster object has been acquired.
- In 2026, real insufficient attribution by Tom Buck and overbroad/misleading aspects of the anonymous dossier can both be true simultaneously. All **17/17** accusation-sermon items now have dedicated forensic files, but **0/17** are declared `ITEM_VERIFIED` pending human-audio/source/attribution gates.
- Phil Johnson’s **original** Aug. 19, 2026 Pyromaniacs article is now directly acquired: he describes real unattributed commentary wording while distinguishing that from preaching others’ finished sermons. This cuts against both total-exoneration and `complete-sermon theft` narratives.
- The Titus 2 source-side chronology is materially stronger: a full PDF object of Bryan Chapell’s 1998 Titus article is identified, and Jennifer Buck’s own **April 7, 2022** G3 article publicly described serious analogous early-marriage circumstances before both Buck’s 2023 sermon and the 2026 plagiarism controversy. Therefore `Buck fabricated a marital history that never happened` is `REFUTED`; the separate wording/attribution question remains open pending original Buck audio and immediate attribution context.
- FBC Lindale’s response to the Buck allegations cannot accurately be reduced to `they did nothing`; available testimony and reproduced institutional material indicate review, outside consultation and corrective measures.
- Four Pray’s Mill pastors associated with G3 acknowledged improper anonymous external action, mischaracterization of Lindale’s process without all details, and interference with another autonomous church’s disciplinary process. The exact original G3 X status locator is now known (`2092237885915201773`), but its body is currently inaccessible after account removal/403; materially identical contemporaneous reproductions remain one underlying participant statement, not multiple independent witnesses. The exact mechanics of the pastors’ resignations remain disputed pending PMBC primary records.
- Claims about latex gloves, proven revenge motive, or federal mail-fraud liability remain below publication threshold.
- G3 Church Network dissolution and wider operational wind-down are supported, but the Georgia Secretary of State official acquisition on **Sep. 8, 2026** still listed `G3 Ministries for the Church, Inc.` as **Active/Compliance**. Operational wind-down therefore must not be described as completed formal Georgia corporate dissolution as of that observation.
- G3+/G3 Press disposition remains a genuine P0 question. Current storefront/app/access state shows continuity, not beneficial ownership. No acquired primary object yet names the 2026 transferee or supplies the transaction agreement, asset schedule, consideration, closing date or board approval/conflict record.
- A previous exact Google Play `Sep. 4, 2026 update` claim remains `DISPUTED` because different Google surfaces report Sep. 4 and Jul. 23 for the same package. Developer/support identity remains useful only as dated platform state.

## Corpus map

### Core authority / navigation

- [`README.md`](README.md) — corpus purpose, principles, periodization and authority map
- [`TIMELINE.md`](TIMELINE.md) — dated reconstruction
- [`SOURCE_LEDGER.md`](SOURCE_LEDGER.md) — canonical source registry and evidence class
- [`CLAIMS_LEDGER.md`](CLAIMS_LEDGER.md) — canonical claim-level verification status
- [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md) — explicit proof-closure backlog
- [`P0_CLOSURE_CHECKPOINT_2026-09-08.md`](P0_CLOSURE_CHECKPOINT_2026-09-08.md) — current primary closures / remaining P0 matrix
- [`IRS_RAW_XML_ACQUISITION_GATE.md`](IRS_RAW_XML_ACQUISITION_GATE.md) — authoritative raw-IRS acquisition provenance and guardrails

### History / ideology / scale

- [`CONFERENCE_HISTORY.md`](CONFERENCE_HISTORY.md) — 2011 prehistory, conference themes, attendance and primary archive anchors
- [`IDEOLOGY_AND_COALITION.md`](IDEOLOGY_AND_COALITION.md) — coalition narrowing, social-justice boundary and right-flank political-theology conflict
- [`IDEOLOGY_CONTENT_CODING_PROTOCOL.md`](IDEOLOGY_CONTENT_CODING_PROTOCOL.md) — reproducible protocol required before quantitative ideological percentages are used

### Finance / governance / assets

- [`FINANCES.md`](FINANCES.md) — current overview of the Form 990 series, exact FY2023 delta, Schedule L, property disposition and receivable trace
- [`FINANCIAL_FORENSICS_2023.md`](FINANCIAL_FORENSICS_2023.md) — detailed raw FY2022/FY2023 Part IX and asset-sale reconstruction
- [`GOVERNANCE.md`](GOVERNANCE.md) — board/officer/PMBC overlap reconstruction
- [`DIRECTOR_TRANSITION_FORENSICS_2025.md`](DIRECTOR_TRANSITION_FORENSICS_2025.md) — date-bounded 2025 director-transition reconstruction and exhausted archive/Georgia public-detail routes
- [`ASSET_TRANSFER_AND_RIGHTS.md`](ASSET_TRANSFER_AND_RIGHTS.md) — platform/storefront/author-rights evidence and discovery ledger
- [`ASSET_TRANSFER_FORENSICS.md`](ASSET_TRANSFER_FORENSICS.md) — canonical Q006 analysis: Living Heritage separation vs unresolved 2026 G3+/Press transferee

### Crisis dossiers / primary controls

- [`BUICE_2025.md`](BUICE_2025.md) — founder anonymous-identity crisis and post-crisis institutional response
- [`BUCK_2026.md`](BUCK_2026.md) — 2026 Buck / PMBC / G3 crisis reconstruction
- [`BUCK_DOSSIER_AUDIT.md`](BUCK_DOSSIER_AUDIT.md) — reconciled 17-sermon accusation-object methodology and corpus state
- [`BUCK_ITEMS/README.md`](BUCK_ITEMS/README.md) — item registry for all 17 accusation-sermon forensic files
- [`PRIMARY_SOURCE_JENNIFER_BUCK_2022_RESTORATIVE_GRACE.md`](PRIMARY_SOURCE_JENNIFER_BUCK_2022_RESTORATIVE_GRACE.md) — `G3-S103`, pre-controversy first-person marital-history control for Titus item 10
- [`2021_MACARTHUR_LIVE_EPISODE.md`](2021_MACARTHUR_LIVE_EPISODE.md) — early communication-integrity warning lead; original-object archive hold remains
- [`PRAYS_MILL_AUTHORITY_AND_DISCIPLINE_LEADS.md`](PRAYS_MILL_AUTHORITY_AND_DISCIPLINE_LEADS.md) — PMBC authority/process leads and primary-record boundaries

### Evidence staging / forensic log

- `EVIDENCE_BATCH_2026-09-07_PASS2.md` through `EVIDENCE_BATCH_2026-09-08_PASS19.md` — append-only acquisition/reconciliation history; not a second evidence system
- [`EVIDENCE_RECONCILIATION_PASS3_PASS11.md`](EVIDENCE_RECONCILIATION_PASS3_PASS11.md) — historical reconciliation record for earlier staging identities
- [`RESEARCH_LOG_2026-09-07_P0.md`](RESEARCH_LOG_2026-09-07_P0.md) — acquisition attempts, blockers and P0 forensic log

### Media / future article

- [`MEDIA_LEDGER.md`](MEDIA_LEDGER.md) — photo/image candidates with item-level rights status
- [`drafts/ARTICLE_OUTLINE.md`](drafts/ARTICLE_OUTLINE.md) — non-publication-authorized long-form architecture reconciled to current claim boundaries

## Current P0 boundary

The remaining P0 items are not un-reconciled staging debt. They require genuinely new primary evidence:

1. **G3+/G3 Press/IP transfer:** named primary transferee + transaction object/terms;
2. **FY2022 real-estate follow-up:** parcel, buyer/grantee, deed/security instrument and explicit receivable/note linkage;
3. **late-board continuity:** a primary roster/continuity object after July 21, 2026 through the crisis;
4. **director transition mechanics:** exact resignation/start dates and reasons where not primary-closed.

## Product / journalism handoff boundary

A separate research-only architecture PR exists in `FedorMilovanov/gb-is-my-strength` for a future `/journal/` editorial vertical. That Product-side design does **not** authorize this corpus for publication.

Any future G3 dossier/article must:

1. pin an exact immutable Research commit / frozen claim set;
2. preserve P0/P1 uncertainty rather than filling gaps from narrative instinct;
3. carry item-level media rights decisions;
4. distinguish fact, testimony, allegation, interpretation, theological judgment and legal conclusion;
5. expose substantial corrections when the evidence changes.

## Publication status

**PUBLICATION_HOLD.** This branch contains active research. Draft PR #188 is a Research checkpoint only; it is not a release witness and does not authorize publication of allegations, screenshots, images, quotes or conclusions.