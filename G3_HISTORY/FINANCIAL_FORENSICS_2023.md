# FY2023 financial forensics — G3 Ministries

**Status:** PRIMARY FY2022/FY2023 PART IX DELTA CLOSED / ASSET-MOVEMENT FOLLOW-UP OPEN  
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

Revenue remained almost flat while spending increased by exactly **$1,061,800**, or about **105%** year over year.

## Primary acquisition closure

### FY2023

The exact FY2023 e-file was acquired from the official IRS TEOS XML distribution rather than inferred from a nonprofit aggregator.

- EIN: `842403597`
- object ID: `202411429349300611`
- IRS batch: `2024_TEOS_XML_05A`
- raw XML SHA-256: `c8eb0baa2265eadef2b6798c68868f91f8fde6ca9fbffe40e138877df92ce5c0`
- acquired components include `IRS990`, `IRS990ScheduleA`, `IRS990ScheduleD`, `IRS990ScheduleO`
- **no `IRS990ScheduleL` component appears in FY2023**

### FY2022 amended comparator

The later FY2022 return was acquired from official IRS batch `2023_TEOS_XML_10A` in exact-head workflow run `34208135511`. The return identifies itself as amended (`AmendedReturnInd = X`) and reports the authoritative FY2022 totals used in the series: $1,735,978 revenue and $1,010,186 expenses.

- acquisition target object ID: `202340569349300209`
- discovered IRS batch member name: `202322939349300637_public.xml`
- raw XML SHA-256: `678b391e948adb6090107435369e175cf2694c69705e107f13be6befe361bc03`

**Provenance note:** the target object ID and the member basename differ. The acquisition matched the official-index target to an IRS batch member by exact EIN/tax period and financial identity. Preserve this mismatch in custody records rather than silently rewriting either identifier. The return content itself is explicitly amended and its totals match the FY2022 authoritative snapshot.

The Actions packages remain `EPHEMERAL_ACTION_ARTIFACT`; acquisition does not by itself authorize publication of the raw objects.

## Exact FY2022 → FY2023 Part IX reconstruction

Both filings classify **100% of functional expenses as program services**, with management/general and fundraising reported as zero.

| Part IX category | FY2022 | FY2023 | Delta |
|---|---:|---:|---:|
| Conferences / meetings | $436,274 | $1,253,557 | **+$817,283** |
| Advertising | $61,063 | $307,574 | **+$246,511** |
| Other salaries and wages | $289,120 | $292,784 | +$3,664 |
| Accounting | $5,400 | $8,995 | +$3,595 |
| Office expenses | $52,793 | $57,252 | +$4,459 |
| Occupancy | $109,578 | $6,627 | **−$102,951** |
| Travel | $12,047 | $25,636 | +$13,589 |
| Depreciation / depletion | $11,177 | $15,138 | +$3,961 |
| Workshop / honorarium family | $13,500 | $23,988 | +$10,488 |
| Donor expenses | $11,875 | $10,000 | −$1,875 |
| Information technology | $0 | $28,707 | +$28,707 |
| Payroll taxes | $0 | $41,728 | +$41,728 |
| Dues / subscriptions | $7,359 | $0 | −$7,359 |
| **Total** | **$1,010,186** | **$2,071,986** | **+$1,061,800** |

The row deltas reconcile **exactly** to the total increase.

Conference/meeting expense rose by **$817,283**. Advertising rose by **$246,511**. Their combined increase was **$1,063,794**, slightly larger than the total net expense increase because other rows partially offset it, most notably occupancy at **−$102,951**.

This closes the old question `what category drove the increase?` at the filed Part IX level.

## What the FY2023 filing says G3 did

Part III describes the year as including:

- four pastors workshops;
- a national conference with **8,300 attendees**;
- launch of the G3+ online streaming service;
- hiring a part-time administrative assistant and a part-time accounting manager;
- a seven-day UK Reformation tour;
- publication of twelve books and one music recording;
- growth of the church network to 211 churches.

This program narrative is context for the expense pattern. It proves what the organization reported doing; it does not prove every cost was prudent, efficiently priced or arm’s-length.

## What the exact delta rules out or materially narrows

### `Payroll caused the 2023 collapse`

**Refuted as the principal Part IX driver.**

Other salaries/wages increased only **$3,664** year over year. Payroll taxes add a new **$41,728** line in FY2023. Those movements are far too small to explain the $1.062m increase.

### `Administrative/fundraising overhead caused most of the spike`

**Contradicted by the filed functional classification.**

Both FY2022 and FY2023 report:

- management and general: **$0**;
- fundraising: **$0**;
- program services: **100% of functional expenses**.

This is self-reported accounting classification, not an external audit judgment. But an article cannot accurately describe the filings as showing a million-dollar administrative-overhead expansion.

### `The 2023 increase was mainly unexplained`

**No longer supportable at the Part IX category level.**

The increase is mathematically reconciled. The dominant expansion is conferences/meetings and advertising.

What remains unknown is not the category allocation but finer-grained questions such as individual vendors, contracts, event economics and whether costs were prudent or arm’s-length.

### `The 2023 filing itself reports a related-party transaction / Schedule L`

**Refuted.**

FY2023 contains no Schedule L, and the relevant Part IV related-party/excess-benefit indicators are false.

FY2024/FY2025 Schedule L disclosures are later-year transactions and must not be back-projected into FY2023.

## FY2022 donated real estate — a newly closed provenance layer

The amended FY2022 raw return exposes an important balance-sheet event that was previously only visible indirectly.

### Schedule M

The filing reports one noncash contribution in the category **commercial real estate**:

- contribution count: **1**;
- value reported on Form 990: **$590,000**;
- valuation method: **`BROKER ESTIMATION`**.

### Schedule D

The same return reports:

- land: **$354,000** book value;
- buildings: **$236,000** book value;
- equipment: $45,974 cost, $14,059 accumulated depreciation, $31,915 book value;
- total net land/building/equipment: **$621,915**.

The land + building values sum exactly to **$590,000**, aligning with the commercial-real-estate contribution reported on Schedule M. This strongly anchors the source of the large FY2022 property balance without requiring speculation.

Schedule O states the return was amended because of a **missing asset fair-market value that had been donated prior to year end**.

## New asset-movement question: FY2022 → FY2023

At FY2022 year end:

- net land/building/equipment: **$621,915**.

At FY2023 year end, the later raw filing shows:

- net land/building/equipment: **$16,777**;
- a new notes/loans receivable balance of approximately **$416,227**;
- higher liabilities, including conference-related liabilities identified in Schedule D.

This is a real and material asset movement. It now deserves its own forensic lane.

**What is not established:**

- that the donated property was sold to a related party;
- that the $416,227 receivable was the sale note for that property;
- that consideration was inadequate;
- that any director/officer benefited;
- that the transaction violated nonprofit law.

**Needed next:** Georgia/local property records, deed/grantor-grantee history, any sale price, counterparty, note terms, board authorization and subsequent receivable collection/write-down.

## FY2024/FY2025 Schedule L boundary

Raw IRS Schedule L content has now also been acquired for later years. The filings report one interested-person business transaction in each year:

- FY2024: `KARIS L BUICE` — `Daughter of Board Member` — `SALARY` — **$30,409**;
- FY2025: same filed relationship/transaction description — **$31,880**.

Both returns report `EngagedInExcessBenefitTransInd=false` and `BusinessRlnWithFamMemInd=true`.

This establishes disclosed family-member salary transactions. It does **not** establish self-dealing, excess benefit, fraud or private enrichment. The specific parent must not be inferred from surname alone because the Schedule L relationship field says only `Daughter of Board Member`.

## Current explanation hierarchy

### H1 — conference/event expansion drove the FY2023 expense reversal

**Status: VERIFIED_PRIMARY at the Part IX category-delta level.**

Conference/meeting expense increased **$817,283**, by far the single largest positive delta.

### H2 — advertising expansion was the second major driver

**Status: VERIFIED_PRIMARY at the Part IX category-delta level.**

Advertising increased **$246,511**.

### H3 — broader ecosystem expansion contributed through smaller categories

**Status: SUPPORTED / project-level causal allocation incomplete.**

IT, travel, workshops and payroll taxes all increased, while the filing reports G3+ launch, publishing, workshops, tour and network expansion. The return does not provide a project ledger tying every dollar to each initiative.

### H4 — payroll / executive compensation caused most of the spike

**Status: REFUTED AS PRINCIPAL DRIVER.**

Wage delta is only +$3,664; payroll taxes add $41,728.

### H5 — administrative/fundraising bloat caused most of the spike

**Status: CONTRADICTED BY FILED FUNCTIONAL CLASSIFICATION.**

Both comparator years report zero management/general and zero fundraising.

### H6 — fraud / diversion / personal enrichment

**Status: UNSUPPORTED.**

The acquired FY2022/FY2023 filings do not establish diversion or embezzlement. Later Schedule L disclosures are ordinary disclosure objects until evidence establishes more.

## Article-safe financial wording after closure

> G3’s financial reversal began in 2023 not because revenue collapsed, but because expenses roughly doubled while revenue remained almost flat. The raw IRS filings now allow the increase to be reconciled category by category: conference and meeting costs rose by about $817,000, while advertising rose by about $247,000. Those two increases account for essentially the entire net rise in spending, partly offset by lower occupancy expense. Both 2022 and 2023 returns classified all functional expenses as program services and reported no management/general or fundraising allocation. That does not prove every expenditure was prudent or efficiently priced, but it rules out portraying the filings as evidence of a million-dollar administrative-payroll surge. A separate unresolved question concerns the large property/receivable movement between 2022 and 2023.
