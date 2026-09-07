# FY2023 financial forensics — G3 Ministries

**Status:** PRIMARY PART IX ACQUIRED / FY2022 CATEGORY-DELTA HOLD  
**Entity:** G3 Ministries for the Church, Inc. — EIN 84-2403597

## Why FY2023 matters

FY2023 is the first large financial reversal in the reconstructed G3 series:

- FY2022 revenue: **$1,735,978**
- FY2022 expenses: **$1,010,186**
- FY2022 result: **+$725,792**

versus:

- FY2023 revenue: **$1,705,689**
- FY2023 expenses: **$2,071,986**
- FY2023 result: **−$366,297**

Revenue therefore remained almost flat while spending increased by approximately **$1.062m / 105%** year over year.

## Primary acquisition closure

The exact FY2023 e-file has now been acquired from the official IRS TEOS XML distribution rather than inferred from a nonprofit aggregator.

- EIN: `842403597`
- object ID: `202411429349300611`
- official annual index: `https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv`
- IRS index batch: `2024_TEOS_XML_05a`
- batch member: `2024_TEOS_XML_05A/202411429349300611_public.xml`
- raw XML SHA-256: `c8eb0baa2265eadef2b6798c68868f91f8fde6ca9fbffe40e138877df92ce5c0`
- raw XML bytes: `27,791`
- source batch SHA-256: `8bf438490091c07a26105bfb9deedaeef062266990c14ad84ac7ea36199d54e8`
- acquired components: `IRS990`, `IRS990ScheduleA`, `IRS990ScheduleD`, `IRS990ScheduleO`
- **no `IRS990ScheduleL` component appears in this FY2023 object**

The Actions package remains `EPHEMERAL_ACTION_ARTIFACT`; acquisition does not by itself authorize publication of any raw object.

## Exact FY2023 Part IX

The filing reports **all $2,071,986 of functional expenses as program services**:

| Part IX category | Total | Program services | Share of total |
|---|---:|---:|---:|
| Conferences / meetings | $1,253,557 | $1,253,557 | 60.5% |
| Advertising | $307,574 | $307,574 | 14.8% |
| Other salaries and wages | $292,784 | $292,784 | 14.1% |
| Office expenses | $57,252 | $57,252 | 2.8% |
| Payroll taxes | $41,728 | $41,728 | 2.0% |
| Information technology | $28,707 | $28,707 | 1.4% |
| Travel | $25,636 | $25,636 | 1.2% |
| Workshops | $23,988 | $23,988 | 1.2% |
| Depreciation / depletion | $15,138 | $15,138 | 0.7% |
| Donor expenses | $10,000 | $10,000 | 0.5% |
| Accounting | $8,995 | $8,995 | 0.4% |
| Occupancy | $6,627 | $6,627 | 0.3% |
| **Total** | **$2,071,986** | **$2,071,986** | **100.0%** |

The same Part IX reports:

- management and general: **$0**;
- fundraising: **$0**.

This is now a primary filing fact, not a derivative ratio inference.

## What the filing itself says G3 did in FY2023

Part III describes the year as including:

- four pastors workshops;
- a national conference with **8,300 attendees**;
- launch of the G3+ online streaming service;
- hiring a part-time administrative assistant and a part-time accounting manager;
- a seven-day UK Reformation tour;
- publication of twelve books and one music recording;
- growth of the church network to 211 churches.

This program narrative is important context for the Part IX composition. It proves reported activity; it does not prove every cost was prudent, arm's-length, or economically efficient.

## Schedule O / amendment context

The raw Schedule O says the return was amended because of a **missing fair-market value for an asset donated before year end**. It does not say the amendment was made to revise functional expenses.

Schedule O also states that:

- the Form 990 was provided to board members for review, discussion and approval;
- board members discussed potential conflicts during board meetings;
- independent board members determined officer/key-employee compensation according to market rates and standards;
- the change in net assets included adding PayPal and Stripe accounts.

These are statements made by the organization in its filing, not independent verification that the procedures were always followed perfectly.

## Related-party / diversion boundary for FY2023

The FY2023 filing does **not** contain Schedule L. Part IV also reports `false` for the principal related-party/excess-benefit indicators exposed in the XML, including:

- `EngagedInExcessBenefitTransInd`;
- `LoanOutstandingInd`;
- `GrantToRelatedPersonInd`;
- `BusinessRlnWithOrgMemInd`;
- `BusinessRlnWithFamMemInd`;
- `BusinessRlnWith35CtrlEntInd`;
- `MaterialDiversionOrMisuseInd`.

This does not prove that no questionable decision could have occurred. It does mean that a claim of a **reported FY2023 Schedule-L/interested-person transaction** would be false on the acquired filing.

## What is now ruled out or materially narrowed

### `Payroll caused the 2023 collapse`

**Unsupported as the primary explanation.**

Other salaries/wages were **$292,784**, and payroll taxes were **$41,728**. Together they are far below the roughly $1.062m year-over-year increase in total expenses.

### `The missing million mainly went into management/fundraising overhead`

**Contradicted by the filed Part IX classification.**

The organization reported **$0 management/general and $0 fundraising** and classified all expenses as program services.

This classification is not a judgment that every expense was wise or correctly priced. But an article cannot accurately characterize the 2023 filing as showing a million-dollar administrative-overhead spike.

### `The 2023 filing itself reports a related-party transaction / Schedule L`

**Refuted.**

The acquired FY2023 XML has no Schedule L component and the relevant Part IV indicators are false.

## Working explanation hierarchy after primary Part IX acquisition

### H1 — conference / event costs were the dominant FY2023 expense category

**Status: VERIFIED AS COMPOSITION / YEAR-OVER-YEAR DELTA STILL OPEN.**

Conferences/meetings alone were **$1,253,557**, or **60.5% of all FY2023 expenses**. This is no longer a speculative hypothesis about the composition of FY2023 spending.

What remains to prove is how much this category increased from FY2022. The raw FY2022 Part IX must be acquired before writing that the *increase itself* was mainly conference-driven.

### H2 — broader ecosystem expansion contributed materially

**Status: STRONGLY PLAUSIBLE / causal allocation not fully separable.**

The filing itself reports the G3+ launch, publishing, workshops, a tour and church-network expansion. Advertising, IT, workshops and other program rows are visible separately, but the return does not provide a project-level cost ledger tying every dollar to each initiative.

### H3 — payroll / executive compensation caused most of the spike

**Status: LOW / unsupported.**

Visible wage and payroll-tax lines are too small relative to the increase.

### H4 — administrative/fundraising bloat caused most of the spike

**Status: CONTRADICTED BY FILED FUNCTIONAL CLASSIFICATION.**

The Part IX columns report 100% program services and zero management/fundraising.

### H5 — fraud / diversion / personal enrichment

**Status: UNSUPPORTED.**

No acquired FY2023 filing component supports diversion or embezzlement, and the return has no Schedule L. Later FY2024/FY2025 Schedule L objects are separate research questions and cannot be back-projected into 2023.

## Remaining proof gate: exact FY2022 category delta

To explain the **change**, not merely FY2023 composition, acquire the raw FY2022 filing and compare the same Part IX rows category by category.

Current acquisition target:

- primary candidate object: `202322939349300637`;
- a second FY2022 filing object also exists: `202340569349300209` and must be used as an amendment/resubmission control if the first object's totals do not match the authoritative FY2022 snapshot.

The target comparison is:

`FY2023 category amount − FY2022 category amount = exact category contribution to the ~$1.062m increase`.

Until that comparison is acquired, article-safe wording is:

> G3's financial reversal began in 2023 because expenses roughly doubled while revenue stayed almost flat. The raw IRS filing now shows that G3 classified every dollar of FY2023 expense as program service, with conferences and meetings alone accounting for about $1.254 million, or 60.5% of total spending. Payroll and payroll taxes were far too small to explain the increase by themselves. The remaining question is not what dominated FY2023 spending, but how much each category increased from FY2022; that requires the raw FY2022 Part IX comparison.
