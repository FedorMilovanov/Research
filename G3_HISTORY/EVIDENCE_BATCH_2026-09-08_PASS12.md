# G3 HISTORY — evidence batch 2026-09-08 PASS12

**Status:** STAGING / PUBLICATION_HOLD  
**Purpose:** tighten the remaining financial/legal/asset-transfer P0s with exact source-object routes, document repeated transport failures rather than treating them as missing evidence, and add the FY2025 program-activity baseline without converting derivative IRS surfaces into independent corroboration.

## Repository checkpoint

Before this evidence pass, branch `research/g3-history-20260907` was merged forward from current `main` without force/rebase. Exact checkpoint head: `17173a4552747889862f19be9522e7c5b97f2e0c`; compare at that point: **73 commits ahead / 0 behind**. PR #188 remained **Draft**, mergeable, and `Repository authority integrity` run `34160829126` completed **success** on that exact head.

This is repository-integrity evidence only. It does not change publication authority: `PUBLICATION_HOLD = true`.

## Provisional sources

| ID | Source | Class | Access | Locator | Rights | Publication | Use / boundary |
|---|---|---|---|---|---|---|---|
| G3-S103 | ProPublica Nonprofit Explorer — G3 FY2024 Form 990 document surface | A2 | PARTIAL_OBJECT | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | IRS-derived filing surface. FY2024 filed 2025-05-15; page explicitly flags reportable interested-person transactions and exposes PDF/XML links. PDF route resolves to a concrete `display_990` object but current research transport returns HTTP 403. This does not downgrade existence of the filing; it records a renderer-access failure. Locator: `https://projects.propublica.org/nonprofits/organizations/842403597`. |
| G3-S104 | ProPublica FY2024 e-file component route — `IRS990ScheduleL` for object `202541359349304489` | A2 | LINK_ONLY | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | BLOCKED | Exact raw-IRS-derived schedule renderer identified as `/nonprofits/full_filing/842403597/202541359349304489/IRS990ScheduleL`. It redirects to a signed `pp-990-rendered` S3 object that the current transport cannot fetch. Content therefore remains `EVIDENCE_HOLD`; no interested-person identity, amount or transaction type may be inferred. |
| G3-S105 | ProPublica FY2025 e-file component route — `IRS990ScheduleL` for object `202641339349303874` | A2 | LINK_ONLY | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | BLOCKED | FY2025 exact Schedule L renderer identified; same signed-S3 transport block. The organization summary independently shows the filing reported conflict-of-interest transactions, but that broad Schedule-L flag is not misconduct evidence. |
| G3-S106 | Cause IQ — G3 Form 990 PDF surfaces FY2023–FY2025 | B1 | LINK_ONLY | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | BLOCKED | Cause IQ exposes distinct `View PDF` links for FY2025, FY2024 and FY2023, but all three exact `view_990` routes returned HTTP 403 through current research transport. This is a second renderer family showing the same acquisition barrier. Cause IQ derives its financial/program data from Form 990 and must not be counted as independent corroboration of the underlying filing. Locator: `https://www.causeiq.com/organizations/g3-ministries-for-the-church,842403597/`. |
| G3-S107 | Cause IQ — FY2025 G3 program-area reconstruction from Form 990 | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | IRS-derived secondary parser. Reports that in 2025 G3 Press published 18 new books, bringing catalogue above 50; G3+ expanded to 500+ audiobooks; G3 Pastor-Theologian Collective launched; one Expository Preaching Workshop and one Biblical Worship Workshop were hosted at local churches; Church Network had 210 member churches; September 2025 national conference was cancelled after leadership transition; Living Heritage Homeschool separated as an independent entity. Use as derivative filing reconstruction pending direct raw XML. Same underlying FY2025 filing as G3-S105/earlier canonical IRS family. |
| G3-S108 | Philanthropy.org — FY2024 G3 filing parser | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | IRS e-file parser identifies FY2024 total expenses $1.401m, program allocation 84% (~$1.2m), management/general 7% (~$93k), fundraising 9% (~$130k), and one reported program service account describing four pastor workshops and two large conferences with 2,000+ attendees. Schedule manifest includes `L · Interested persons`. It explicitly states its figures are drawn from the IRS e-file. Do not count independently from FY2024 IRS filing. Locator: `https://philanthropy.org/990/report/842403597/g3-ministries-for-the-church-inc`. |
| G3-S109 | Georgia Secretary of State — G3 Articles of Incorporation, control no. `19085916`, filing no. `17370469`, 2019-06-06 | A1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Primary corporate charter. Establishes Domestic Nonprofit Corporation, perpetual duration, 501(c)(3)-restricted purposes, private-inurement prohibition and dissolution provisions. The dissolution clause authorizes dissolution by a two-thirds board vote and directs remaining assets, after liabilities, to qualifying exempt purposes/entities. It is a governing baseline if formal dissolution is proved; it does **not** by itself establish that dissolution occurred or that any pre-dissolution transfer was improper. Locator: `https://ecorp.sos.ga.gov/BusinessSearch/DownloadFile?filingNo=17370469`. |
| G3-S110 | Fresh current-status search across Georgia Secretary of State indexed surfaces, 2026-09-08 | A1 search route / discovery only | CATALOG_ONLY | COARSE_LOCATOR_ONLY | PUBLICATION_ELIGIBLE | BLOCKED | Exact control number and historical primary filings remain searchable, but no current `BusinessInformation` entity card or dissolution filing was retrieved through the present search transport. This is a negative acquisition result only. It cannot establish `Active`, `Administratively Dissolved`, or `Dissolved`. |
| G3-S111 | Michelle Lesley, `On the G3 Scandal…`, current crawl 2026-09-08 | B1 participant-adjacent secondary | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Continues to preserve the G3+ subscriber-transfer notice and describes the recipient as an as-yet unnamed ministry; reporting also says the same unidentified ministry is to acquire G3 Press. The source itself does not know the transferee identity. Locator: `https://michellelesley.com/2026/08/27/on-the-g3-scandal/`. |
| G3-S112 | Google Play current G3+ app metadata, crawl 2026-09-08 | A3 platform metadata | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Developer/about-developer still displays `G3 Ministries for the Church`, `admin@g3min.org`, and 4979 Highway 5. This is current platform account metadata only. It cannot establish beneficial ownership, legal asset-transfer completion, or whether an announced acquisition closed. Locator: `https://play.google.com/store/apps/details?id=com.subsplashconsulting.s_V9572P`. |

## Provisional claims

| ID | Claim | State | Support / boundary |
|---|---|---|---|
| G3-C136 | FY2024 and FY2025 Schedule L objects are no longer merely inferred from filing flags; exact raw-IRS-derived renderer identities are known. | CORROBORATED | G3-S103–S105. Content itself remains inaccessible through current transport, so the people/amounts/types are still unknown. |
| G3-C137 | Failure to name the FY2024/FY2025 Schedule L interested persons is a current transport/acquisition limitation rather than evidence that Schedule L is absent. | CORROBORATED | Exact component routes exist; both ProPublica signed-S3 and independent Cause IQ PDF renderers fail through current transport. |
| G3-C138 | The fact that G3 reported Schedule L transactions proves a financial abuse/conflict-of-interest violation. | REFUTED | Schedule L is a broad disclosure schedule covering reportable transactions with interested persons. Transaction-specific facts and applicable governance context are required before misconduct language. |
| G3-C139 | G3 had substantive ministry/program activity in FY2025 despite the severe financial loss. | CORROBORATED | G3-S107, derivative of the FY2025 Form 990: 18 new books / catalogue >50, 500+ G3+ audiobooks, two local workshops, 210 network churches, Pastor-Theologian Collective, conference-model transition. This supports activity/scale, not efficiency, prudence or absence of misconduct. |
| G3-C140 | The 2025 loss can be described as proof that G3 had become a fictitious or inactive ministry shell. | REFUTED | G3-S107 shows reported program activity. This does not explain the loss or validate every expense. |
| G3-C141 | FY2024 expense allocation was approximately 84% program / 7% management-general / 9% fundraising, with about $1.2m of $1.401m total expenses reported as program services. | CORROBORATED | G3-S108. Underlying authority is the FY2024 Form 990; direct raw row acquisition remains preferred. |
| G3-C142 | The 2023 financial reversal can presently be attributed to a specific Part IX expense category. | UNVERIFIED | Exact FY2023 row-level Part IX/Schedule O content remains unacquired. Summary totals and program-ratio evidence narrow alternatives but do not identify the million-dollar delta. |
| G3-C143 | G3’s 2019 Articles contain a concrete nonprofit-dissolution asset-disposition rule and private-inurement restriction. | VERIFIED_PRIMARY | G3-S109. |
| G3-C144 | Those Articles prove that G3 formally dissolved in 2026. | REFUTED | Charter provisions govern what happens if dissolution occurs; they are not a dissolution filing. Current Georgia status remains unacquired. |
| G3-C145 | Any transfer of G3+ or G3 Press before formal dissolution necessarily violated the charter’s dissolution clause. | REFUTED | Timing and transaction form matter. Dissolution-specific disposition rules cannot be mechanically applied to an unproven pre-dissolution transaction; other nonprofit/fiduciary rules may still be relevant but require transaction facts. |
| G3-C146 | The publicly reported G3+ / G3 Press recipient remains unnamed as of the current 2026-09-08 search pass. | PARTIALLY_VERIFIED | G3-S111 plus fresh search. This is a dated public-record/search conclusion, not proof that no private agreement identifies the counterparty. |
| G3-C147 | Current Google Play metadata listing G3 as G3+ developer proves the announced acquisition did not close. | REFUTED | G3-S112. Store metadata may lag legal/operational transfers and cannot establish beneficial ownership. |

## Financial acquisition status after PASS12

### FY2024

Known:
- IRS/ProPublica object: `202541359349304489`;
- exact e-file components include main `IRS990`, Schedules A/B/D/J/L/O;
- exact Schedule L route identified;
- ProPublica PDF object identified but 403 through current transport;
- Cause IQ PDF object independently identified but 403 through current transport;
- derivative Part IX allocation: 84% program / 7% management / 9% fundraising.

Still required for P0 closure:
- raw `IRS990ScheduleL` body;
- exact Part IV trigger(s), Schedule L part(s), interested person/business identity, transaction category, amount/balance, correction flag if any;
- direct XML custody checksum.

### FY2025

Known:
- IRS/ProPublica object: `202641339349303874`;
- exact Schedule L renderer identified;
- substantive program narrative available through IRS-derived Cause IQ;
- current summary shows severe deficit but ongoing reported operations.

Still required:
- raw Schedule L body and Schedule O as applicable;
- exact transaction rows and context;
- raw XML custody.

### FY2023

Known:
- IRS/ProPublica object: `202411429349300611`;
- revenue $1,705,689; expenses $2,071,986; loss $366,297;
- salary/wage summary alone cannot explain the increase;
- prior derivative evidence points to near/all-program allocation.

Still required:
- exact Part IX row-level functional expense table;
- Schedule O continuation/explanations if present;
- direct comparison against FY2022 rows.

## Georgia / transfer proof test

If a formal 2026 dissolution is eventually acquired, test the post-G3 disposition through a transaction chain rather than rhetoric:

1. dissolution filing / effective date;
2. board resolution and vote threshold;
3. liabilities provided for;
4. exact asset list — G3+, Press inventory/IP, subscriber relationships, domains/trademarks, content licenses, cash/receivables;
5. transferee legal identity and tax-exempt status;
6. consideration / valuation / assumption of liabilities;
7. interested-person relationships and recusals;
8. author/content rights that had already reverted or been withdrawn before transfer;
9. closing/effective date and post-closing platform/storefront state.

Until those objects are acquired, words such as `asset stripping`, `self-dealing`, `gift to friends`, `fire sale` or `fraudulent transfer` remain prohibited.

## Reconciliation note

PASS12 is staging. For canonical rewrite:
- S103–S105 are **access/locator upgrades of the existing IRS/ProPublica filing family**, not new independent witnesses;
- S106–S108 are derivative parsers/renderers of the same filings and must not inflate corroboration counts;
- S109 is a genuinely distinct primary legal source;
- S110 is an acquisition log state, not substantive evidence of corporate status;
- S111 upgrades the transfer-status timeline but does not name the counterparty;
- S112 is a platform-state object only.

Do not append PASS12 IDs mechanically to the master ledgers without extending `EVIDENCE_RECONCILIATION_PASS3_PASS11.md` or creating its successor reconciliation map.
