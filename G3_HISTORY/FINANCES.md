# G3 Ministries — financial reconstruction

**Entity:** `G3 Ministries for the Church, Inc.`  
**EIN:** `84-2403597`  
**Status:** ACTIVE / PUBLICATION_HOLD  
**Primary source family:** IRS Form 990 e-file data, cross-checked through ProPublica Nonprofit Explorer (`G3-S002`) and IRS-origin parsers.

## IRS provenance anchors

| Fiscal year | Filed | IRS / ProPublica object ID | Current acquisition state |
|---|---|---|---|
| FY2023 | 2024-05-21 | `202411429349300611` | summary verified; raw XML target identified |
| FY2024 | 2025-05-15 | `202541359349304489` | summary verified; PDF/XML links exposed; Schedule L object identified |
| FY2025 | 2026-05-13 | `202641339349303874` | summary verified; raw XML link exposed; Schedule L object identified |

ProPublica explicitly states that its full-filing reconstruction uses raw XML released by the IRS. The official IRS Form 990 Series Downloads page is the authoritative bulk-acquisition route for post-2021 e-file XML. Current tool access can identify the exact XML objects and rendered Schedule L objects but has not yet retrieved the Schedule L row content, so the interested-person analysis remains fail-closed.

## Annual series

| FY | Revenue | Expenses | Annual result | Net assets | Program-service revenue | Notes |
|---|---:|---:|---:|---:|---:|---|
| 2019 | $100 | $0 | +$100 | $100 | $0 | startup / 990-EZ period |
| 2020 | $204,510 | $29,901 | +$174,609 | $174,709 | $204,510 | program-service driven |
| 2021 | $1,471,335 | $1,054,265 | +$417,070 | $591,779 | $1,471,335 | rapid scale-up |
| 2022 | $1,735,978 | $1,010,186 | +$725,792 | $1,318,931 | $1,145,978 | strongest annual result in current series |
| 2023 | $1,705,689 | $2,071,986 | **−$366,297** | $1,043,850 | $1,509,078 | first large deficit; expenses nearly doubled vs 2022 |
| 2024 | $1,212,253 | $1,401,429 | **−$189,176** | $854,674 | $863,485 | still active institution, but second deficit |
| 2025 | $399,645 | $950,642 | **−$550,997** | $304,459 | $248,846 | severe revenue collapse after leadership crisis/cancelled national event |

## Core verified observations

### 1. The financial decline predates the August 2026 scandal

The reversal begins in FY2023, not 2026. Therefore a claim that the 2026 Buck/anonymous-mailing scandal alone caused the financial collapse is chronologically impossible.

### 2. FY2023 is the central unexplained turning point

Revenue stayed near FY2022 levels ($1.706m vs $1.736m), but expenses rose from ~$1.010m to ~$2.072m. Reported other salaries/wages in FY2023 were $292,784, only 14.1% of total expenses, so wage growth alone cannot explain the approximately $1.06m year-over-year increase in total spending.

**Open requirement:** acquire exact FY2023 Part IX functional-expense lines and Schedule O descriptions to identify event, production, travel, occupancy, professional-services, publishing and other expense components.

### 3. FY2024 spending is now functionally bounded

An IRS-origin Form 990 parser reports the following FY2024 allocation from Part IX:

- program services: **84% / approximately $1.2m**;
- management & general: **7% / approximately $93k**;
- fundraising: **9% / approximately $130k**;
- salaries, benefits & payroll (Part IX lines 5–10): **approximately $483k / 34%** of total expenses;
- year-end cash: **approximately $831k**;
- total assets: **$1,166,160**;
- total liabilities: **$311,486**;
- net assets: **$854,674**.

The same filing describes four pastor workshops and two large conferences with more than 2,000 attendees. This makes an evidence-free claim that FY2024 spending was principally private enrichment unsustainable. It does **not** explain the FY2023 spike or resolve Schedule L.

### 4. G3 was heavily dependent on program-service revenue

Approximate program-service share of total revenue:

- FY2020: 100%
- FY2021: 100%
- FY2022: 66%
- FY2023: 88.5%
- FY2024: 71.2%
- FY2025: 62.3%

This supports the hypothesis that conference/product activity was economically central. It does **not** by itself prove which cancelled event caused which loss.

### 5. Three consecutive deficits materially depleted reserves

FY2023 + FY2024 + FY2025 annual deficits sum to approximately **−$1.106m**. Net assets fell from ~$1.319m at FY2022 year-end to ~$304k at FY2025 year-end.

### 6. No current evidence supports describing G3 as a financial scam

Available filings show substantial program activity and do not, by themselves, indicate diversion or embezzlement. Josh Buice was reported at $0 G3 compensation in the FY2024 filing. Scott Aniol and Virgil Walker received reportable operational compensation. Compensation levels may be analyzed comparatively, but high or low pay is not evidence of misconduct.

## Compensation snapshots

### FY2024

- Scott Aniol, Vice President: $137,941 reportable compensation + $19,833 other compensation.
- Virgil Walker, VP of Ministry Relations: $126,075 + $20,462 other compensation.
- Joshua Buice, President: $0 from G3 in reported compensation.
- Other salaries and wages: $239,761.

### FY2025

- Scott Aniol, President: $135,657 reportable compensation.
- Other salaries/wages: $303,309.
- Total assets: $388,982.
- Total liabilities: $84,523.
- Net assets: $304,459.

**Guardrail:** compensation must not be conflated with total income from other churches/ministries unless separately sourced.

## Program activity evidence

FY2024 filing descriptions report four pastor workshops and two large conferences with >2,000 attendees, plus publishing activity and continued Church Network operations. Thus FY2024 was financially weakening but operationally active.

FY2025 filing descriptions, as reproduced by IRS-origin nonprofit datasets, report 18 new G3 Press books, continued G3+ resources, approximately 210 Church Network member churches, one Expository Preaching Workshop and one Biblical Worship Workshop, the separation of Living Heritage Homeschool as an independent entity, the May Buice resignation, July Aniol appointment and cancellation of the planned September 2025 national conference.

## Schedule L — HIGH-PRIORITY HOLD

The FY2024 and FY2025 e-file manifests each contain an `IRS990ScheduleL` object, and the extracted filing data identifies reportable interested-person transactions. This **does not mean** the IRS found a conflict violation or wrongdoing. Schedule L is the disclosure schedule for certain loans, grants, business transactions or other transactions involving interested persons.

Known object targets:

- FY2024 filing: `202541359349304489` → `IRS990ScheduleL`
- FY2025 filing: `202641339349303874` → `IRS990ScheduleL`

Current status:

- `EVIDENCE_HOLD`
- schedule existence: verified
- exact Schedule L rows: not yet acquired
- no person, amount, business or impropriety may be alleged from schedule existence alone

Required fields before analysis:

1. interested person / relationship;
2. transaction category;
3. amount;
4. business/entity counterparty if any;
5. governing-body approval/process disclosure;
6. whether terms were ordinary/reasonable;
7. recurrence across FY2024/FY2025.

## Dissolution / asset-transfer constraint from the articles

The 2019 Georgia Articles of Incorporation state that the board may cease corporate activities and dissolve by a **two-thirds vote**. On dissolution, liabilities must be provided for first, and remaining assets must be disposed of for qualifying exempt purposes / qualifying 501(c)(3) organizations as the board determines.

This is an important legal-document baseline for the 2026 asset question. It does **not** establish that a formal dissolution vote occurred, which organization received any assets, whether G3+/Press was sold or donated, or whether a particular transaction satisfied all applicable duties.

## Working hypotheses — NOT FACTS

- `H-FIN-01`: FY2023 expense expansion reflected deliberate institutional scale-up around conference/media/publishing operations rather than illicit spending.
- `H-FIN-02`: cancellation of national conference activity in 2025 materially damaged program-service revenue because G3’s revenue model was unusually dependent on paid program activity.
- `H-FIN-03`: by 2026 the ministry had far less financial resilience than at its 2022 peak, making any governance/reputation shock more difficult to survive.
- `H-FIN-04`: any 2026 transfer of G3+/Press must be evaluated against the corporation’s nonprofit-purpose and dissolution-asset restrictions, but no transfer recipient or transaction terms are currently verified.

All hypotheses remain subordinate to exact filing and transaction evidence.