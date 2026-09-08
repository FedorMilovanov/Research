# G3 Ministries — financial reconstruction

**Entity:** `G3 Ministries for the Church, Inc.`  
**EIN:** `84-2403597`  
**Status:** ACTIVE / PUBLICATION_HOLD  
**Primary source family:** official IRS TEOS e-file XML (`G3-S002` / `G3-S028`). ProPublica, Philanthropy.org and Cause IQ are derivative parser/cross-check surfaces of the same filing family and must not be counted as independent corroboration of IRS facts.

## IRS provenance anchors

| Fiscal year | IRS object / comparator | Current primary state |
|---|---|---|
| FY2022 amended comparator | acquisition target `202340569349300209`; official batch member `202322939349300637_public.xml`; raw SHA-256 `678b391e948adb6090107435369e175cf2694c69705e107f13be6befe361bc03` | **FULL_OBJECT_VERIFIED**; amended return; exact Part IX comparator + Schedule M/D acquired |
| FY2023 | `202411429349300611`; raw SHA-256 `c8eb0baa2265eadef2b6798c68868f91f8fde6ca9fbffe40e138877df92ce5c0` | **FULL_OBJECT_VERIFIED**; exact Part IX, asset-sale and balance-sheet leaves acquired |
| FY2024 | `202541359349304489`; raw SHA-256 `c14f511cf66051b916748440594586b4db1ecdb0d07ab14ef05e01e92524aca3` | **FULL_OBJECT_VERIFIED**; Schedule L acquired |
| FY2025 | `202641339349303874`; raw SHA-256 `48846b93808c2ffcacac6dc1995fb7890a630ccef9f711fa8a27cd4445541ac2` | **FULL_OBJECT_VERIFIED**; Schedule L, governance rows and program-history narrative acquired |

The FY2022 acquisition-target ID and IRS ZIP-member basename differ. That mismatch is preserved in custody metadata rather than silently normalized; the acquired return identifies itself as amended and reconciles to the authoritative FY2022 totals used below.

GitHub Actions acquisition artifacts are ephemeral research custody only. Raw acquisition does not itself authorize publication of filing bytes.

## Annual series

| FY | Revenue | Expenses | Annual result | Net assets | Program-service revenue | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2019 | $100 | $0 | +$100 | $100 | $0 | startup / 990-EZ period |
| 2020 | $204,510 | $29,901 | +$174,609 | $174,709 | $204,510 | program-service driven |
| 2021 | $1,471,335 | $1,054,265 | +$417,070 | $591,779 | $1,471,335 | rapid scale-up |
| 2022 | $1,735,978 | $1,010,186 | +$725,792 | $1,318,931 | $1,145,978 | strongest annual result in current series |
| 2023 | $1,705,689 | $2,071,986 | **−$366,297** | $1,043,850 | $1,509,078 | first large deficit; expenses rose by exactly $1,061,800 |
| 2024 | $1,212,253 | $1,401,429 | **−$189,176** | $854,674 | $863,485 | second deficit |
| 2025 | $399,645 | $950,642 | **−$550,997** | $304,459 | $248,846 | severe revenue collapse after 2025 leadership crisis / cancelled national event |

## Core verified observations

### 1. The financial decline predates the August 2026 scandal

The reversal begins in FY2023, not 2026. Therefore the 2026 Buck/anonymous-mailing crisis cannot by itself explain the prior financial deterioration.

FY2023 + FY2024 + FY2025 annual deficits sum to approximately **−$1.106m**. Net assets fell from approximately **$1.319m** at FY2022 year-end to **$304,459** at FY2025 year-end.

### 2. FY2023 expense reversal is now primary-closed at Part IX category level

Revenue remained nearly flat from FY2022 to FY2023, while expenses rose by exactly **$1,061,800**.

Both raw filings classify **100% of functional expenses as program services**, with management/general and fundraising reported as zero.

| Part IX category | FY2022 | FY2023 | Delta |
|---|---:|---:|---:|
| Conferences / meetings | $436,274 | $1,253,557 | **+$817,283** |
| Advertising | $61,063 | $307,574 | **+$246,511** |
| Other salaries / wages | $289,120 | $292,784 | +$3,664 |
| Accounting | $5,400 | $8,995 | +$3,595 |
| Office | $52,793 | $57,252 | +$4,459 |
| Occupancy | $109,578 | $6,627 | **−$102,951** |
| Travel | $12,047 | $25,636 | +$13,589 |
| Depreciation | $11,177 | $15,138 | +$3,961 |
| Workshop / honorarium family | $13,500 | $23,988 | +$10,488 |
| Donor expenses | $11,875 | $10,000 | −$1,875 |
| Information technology | $0 | $28,707 | +$28,707 |
| Payroll taxes | $0 | $41,728 | +$41,728 |
| Dues / subscriptions | $7,359 | $0 | −$7,359 |
| **Total** | **$1,010,186** | **$2,071,986** | **+$1,061,800** |

The category deltas reconcile exactly. Conference/meeting expense and advertising are the dominant filed drivers. Payroll did not drive the reversal.

**Boundary:** this is self-reported Form 990 functional classification, not an independent audit of prudence, vendor pricing or arm’s-length terms.

### 3. The old “administrative/private-spending spike” theory is not supported by the filed comparison

The comparator filings do not show a million-dollar management/fundraising expansion; they report zero in those functional columns. Likewise wages increased only **$3,664**, with **$41,728** of payroll taxes newly reported in FY2023.

An article may investigate vendors, contracts and event economics, but it must not describe the filed increase as chiefly payroll or administrative overhead.

### 4. Three consecutive deficits materially depleted reserves

The financial condition entering the 2026 governance crisis was much weaker than at the FY2022 peak. This supports a resilience/fragility interpretation, but it does not prove that any single scandal caused the institution’s eventual operational wind-down.

### 5. No acquired filing supports describing G3 as a financial scam

The filings show substantial program activity and do not establish diversion, embezzlement or private enrichment. Expense growth, deficits, a property loss and an interested-person disclosure are not themselves misconduct findings.

## FY2024/FY2025 Schedule L — CLOSED AT FILING LEVEL

Raw Schedule L rows have been acquired for both later years.

| Filing | Interested person | Filed relationship | Transaction | Amount | Revenue sharing |
|---|---|---|---|---:|---|
| FY2024 | `KARIS L BUICE` | `Daughter of Board Member` | `SALARY` | **$30,409** | `false` |
| FY2025 | `KARIS L BUICE` | `Daughter of Board Member` | `SALARY` | **$31,880** | `false` |

Both returns report:

- `EngagedInExcessBenefitTransInd=false`;
- `BusinessRlnWithFamMemInd=true`;
- conflict-of-interest policy/disclosure/monitoring indicators;
- compensation-review process indicators.

**Allowed:** G3 disclosed salary paid to a person identified in the filings as the daughter of a board member.

**Not allowed:** infer the specific parent from surname alone, or convert the disclosure into `self-dealing`, `fraud`, `embezzlement`, `private enrichment` or an excess-benefit finding.

FY2023 contains no Schedule L. Later-year Schedule L disclosures must not be back-projected into the 2023 expense reversal.

## FY2022 donated real estate → FY2023 disposition

The amended FY2022 raw return reports one noncash contribution in **commercial real estate**:

- count: **1**;
- reported value: **$590,000**;
- valuation method: `BROKER ESTIMATION`.

Schedule D reports:

- land: **$354,000**;
- buildings: **$236,000**;
- land + buildings: **$590,000**;
- equipment net: **$31,915**;
- total net land/building/equipment: **$621,915**.

The FY2023 raw return then reports:

| Field | FY2023 value |
|---|---:|
| gross amount from sale of `Other` assets | **$550,000** |
| cost/basis | **$590,000** |
| gain/loss | **−$40,000** |
| beginning net land/building/equipment | **$621,915** |
| ending net land/building/equipment | **$16,777** |

The ending $16,777 is fully accounted for by remaining equipment. At the filing/accounting-object level, the $590,000 donated land/building asset was therefore disposed in FY2023 for **$550,000 gross proceeds**, producing a **$40,000 loss**.

**Correction firewall:** a derivative display reading `Sales of Assets −$40,000` is showing the loss, not a $40,000 sale price.

## Notes/loans receivable trace

Raw balance sheets show a continuing receivable:

| Filing | Beginning | Ending | Change | Reported investment income |
|---|---:|---:|---:|---:|
| FY2023 | $0 / no carried balance in reconstructed sequence | **$416,227** | **+$416,227** | $0 |
| FY2024 | **$416,227** | **$251,197** | **−$165,030** | **$22,683** |
| FY2025 | **$251,197** | **$153,000** | **−$98,197** | **$15,375** |

The carry-forward is exact across filings.

The timing materially strengthens a seller-financing hypothesis for the $550,000 property sale, but the filings do **not** identify the debtor or expressly link the receivable/investment income to that sale.

**Current state:** property sale = `VERIFIED_PRIMARY` at filing/accounting-object level; seller financing / counterparty / note terms = `UNVERIFIED` pending deed and note/security evidence.

## Property-record access boundary

Official public routes were tested rather than replaced by address inference:

- Douglas County Clerk / Georgia DOR authority surfaces are reachable;
- Douglas qPublic is Cloudflare-blocked in the research runtime;
- the GSCCCA Real Estate Name Search form and Douglas County parameters were reconstructed, but unauthenticated result submission routes to login;
- no subscription, payment, login or access-control bypass was attempted.

`4979 Highway 5` is a corporate/principal-address and parcel lead only. It must not be identified as the donated-and-sold $590,000 property without deed/title evidence.

## Compensation snapshots

### FY2024

- Scott Aniol, Vice President: $137,941 reportable compensation + $19,833 other compensation.
- Virgil Walker, VP of Ministry Relations: $126,075 + $20,462 other compensation.
- Joshua Buice, President: $0 from G3 in the reported row.
- Other salaries and wages: $239,761.

### FY2025

- Scott Aniol, President: $135,657 reportable compensation.
- Other salaries/wages: $303,309.
- Total assets: $388,982.
- Total liabilities: $84,523.
- Net assets: $304,459.

**Guardrail:** G3 compensation must not be conflated with income from churches or other ministries unless separately sourced.

## Program activity evidence

FY2023 raw Part III reports, among other activity:

- four pastors workshops;
- a national conference with **8,300 attendees**;
- launch of G3+;
- a UK Reformation tour;
- twelve books and one music recording;
- church-network growth to 211 churches.

FY2024 filing material reports continued workshops/conferences and publishing/network activity.

The FY2025 raw `IRS990/Desc` program-history narrative also states that G3 separated **Living Heritage Homeschool as an independent entity from G3 Ministries during 2025**, alongside continued G3 Press/G3+ activity and the year’s leadership/program changes.

That is **VERIFIED_PRIMARY** for the 2025 separation. It does **not** establish that Living Heritage later acquired G3+, G3 Press or other G3 assets during the 2026 wind-down.

## Dissolution / asset-transfer constraints

The 2019 Georgia Articles of Incorporation provide a corporate dissolution framework, including board action and disposition of residual assets for qualifying exempt purposes after liabilities.

Separately, the Georgia Secretary of State current-status acquisition on **2026-09-08** lists `G3 Ministries for the Church, Inc.` as **Active/Compliance**. Therefore operational wind-down must not be described as completed formal Georgia dissolution as of that observation.

The corporate documents/status do not identify the 2026 recipient of G3+, G3 Press or other assets and do not establish transaction terms.

## Current hypothesis states

- `H-FIN-01` — FY2023 expense expansion was driven principally by conference/meeting and advertising growth: **VERIFIED_PRIMARY at Part IX category level**.
- `H-FIN-02` — 2025 event cancellation materially contributed to program-service revenue collapse: **PLAUSIBLE / exact causal allocation open**.
- `H-FIN-03` — by 2026 G3 had substantially less financial resilience than at the 2022 peak: **SUPPORTED by filed annual series**.
- `H-FIN-04` — the $416,227 receivable was seller financing from the FY2023 property sale: **PLAUSIBLE / UNVERIFIED**.
- `H-FIN-05` — payroll/executive compensation caused most of the FY2023 spike: **REFUTED as principal driver**.
- `H-FIN-06` — administrative/fundraising bloat caused most of the FY2023 spike: **CONTRADICTED by filed FY2022/FY2023 functional classification**.
- `H-FIN-07` — the property sale/loss or Schedule L salary disclosure proves fraud/diversion/private enrichment: **UNSUPPORTED**.
- `H-FIN-08` — Living Heritage’s 2025 separation proves it became the 2026 G3+/Press successor: **UNSUPPORTED / Q006 remains open**.

## Remaining high-value financial acquisitions

1. exact property parcel/legal description and deed chain;
2. purchaser/grantee identity;
3. note/security instrument and explicit receivable linkage;
4. interest, maturity, collateral and later collection/write-down of the remaining $153,000;
5. board authorization and conflict handling for the property transaction;
6. named primary transferee and transaction documents for G3+/G3 Press/IP assets.

## Article-safe financial wording

> G3’s financial reversal began in 2023 because expenses roughly doubled while revenue remained almost flat. The raw IRS filings reconcile the increase category by category: conference and meeting costs rose by about $817,000 and advertising by about $247,000, while payroll changes were far smaller. The filings also show that commercial real estate valued at $590,000 and donated in 2022 was sold in 2023 for $550,000 against a $590,000 basis, producing a $40,000 loss. A new $416,227 notes/loans receivable then declined through the next two filings, but the IRS records do not identify the debtor or explicitly connect the receivable to the property sale. Later Schedule L filings disclose salary paid to a person identified only as the daughter of a board member; that disclosure does not establish excess benefit or wrongdoing. Deed, note and transaction records remain necessary before naming counterparties or characterizing the financing.