# FY2023 financial forensics — G3 Ministries

**Status:** PRIMARY FY2022/FY2023 PART IX DELTA CLOSED / $590K REAL-ESTATE SALE CLOSED AT FILING LEVEL / COUNTERPARTY + RECEIVABLE TERMS OPEN  
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

The asset-level readback was repeated on exact Research head `a5bb664578ad4c238fc7edbd821285a6647f3d53` in workflow run `34220049227`; it acquired the same raw FY2023 object and the same raw SHA-256 before emitting the balance-sheet and asset-sale leaves used below.

### FY2022 amended comparator

The later FY2022 return was acquired from official IRS batch `2023_TEOS_XML_10A`. The return identifies itself as amended (`AmendedReturnInd = X`) and reports the authoritative FY2022 totals used in the series: $1,735,978 revenue and $1,010,186 expenses.

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

## FY2022 donated real estate — primary provenance

The amended FY2022 raw return exposes the origin of the large property balance.

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

The land + building values sum exactly to **$590,000**, aligning with the single commercial-real-estate contribution reported on Schedule M.

Schedule O states the return was amended because of a **missing asset fair-market value that had been donated prior to year end**.

## FY2023 disposition — the filing now reports the sale

The exact FY2023 raw Form 990 closes the former question of whether the $590,000 property balance merely disappeared through an accounting reclassification.

The asset-sale group reports:

| Raw Form 990 field | FY2023 value |
|---|---:|
| `GrossAmountSalesAssetsGrp/OtherAmt` | **$550,000** |
| `LessCostOthBasisSalesExpnssGrp/OtherAmt` | **$590,000** |
| `GainOrLossGrp/OtherAmt` | **−$40,000** |
| `NetGainOrLossInvestmentsGrp/TotalRevenueColumnAmt` | **−$40,000** |

The balance sheet simultaneously reports:

- net land/building/equipment at beginning of year: **$621,915**;
- net land/building/equipment at end of year: **$16,777**;
- end-of-year equipment cost/basis: **$45,974**;
- accumulated depreciation: **$29,197**;
- end-of-year equipment book value: **$16,777**.

Thus the surviving $16,777 is fully explained by equipment. The FY2022 **$354,000 land + $236,000 building = $590,000** property balance is gone, while FY2023 reports an `Other` asset sale with **exactly $590,000 basis**, **$550,000 gross proceeds** and **$40,000 loss**.

**Primary reconstruction allowed:** the filings identify the FY2023 $550,000 asset sale as the disposition of the $590,000 donated commercial-real-estate asset at the accounting-object level. This is much stronger than the earlier inference from the falling L/B/E balance alone.

**Important correction:** a rendered summary that displays only `Sales of Assets −$40,000` can be misunderstood. In the raw return, **−$40,000 is the loss**, not the sale proceeds; the gross sale amount is **$550,000**.

## The $416,227 receivable — linkage remains open

The same FY2023 raw Form 990 reports a new end-of-year field:

- `OthNotesLoansReceivableNetGrp/EOYAmt` = **$416,227**.

This creates an obvious seller-financing hypothesis because it appears in the same year as the $550,000 real-estate disposition. The arithmetic difference is **$133,773** (`$550,000 − $416,227`).

However, the filing does **not** identify the debtor, note date, interest rate, maturity, collateral or transaction linkage in the acquired Schedule D/O content. The current raw filing therefore does **not yet prove** that the $416,227 receivable is the unpaid balance of the $550,000 property sale.

**Current classification:** `SELLER_FINANCING_HYPOTHESIS / NOT YET VERIFIED`.

### What remains open

- exact parcel / legal description of the donated-and-sold real estate;
- donor/grantor into G3;
- purchaser/grantee from G3;
- cash received at closing, if any;
- whether the $416,227 receivable is purchaser financing or an unrelated note;
- note interest, maturity, collateral and later payments/write-down;
- board authorization and any conflicts;
- whether any counterparty was related to an officer/director.

No related-party, inadequate-consideration or nonprofit-law conclusion may be drawn without those records.

## Property-record acquisition boundary

The research has now tested the available official public routes rather than relying on a secondary parcel mirror:

- Douglas County Clerk and Georgia DOR authority pages are reachable;
- Douglas qPublic is Cloudflare-blocked in the research runtime (`403`);
- GSCCCA Real Estate Name Search form and exact Douglas County parameters are publicly readable, but submitting the unauthenticated Name Search returns an automatic `frmLogin` interstitial rather than deed results;
- therefore no subscription/login/payment bypass is attempted.

A secondary property index describes `4979 Highway 5` as a 9.03-acre Pray’s Mill church/cemetery parcel with a much higher 2022 market-value projection. This remains a useful **counterboundary**, not title proof.

Accordingly, **4979 Highway 5 must not be identified as the $590,000 donated-and-sold property merely because G3 used that address as its corporate/principal address.** Parcel identity still requires deed/assessor evidence.

## Form 8282 guardrail

FY2023 Form 990 reports `Form8282PropertyDisposedOfInd=false`. That field must not be converted into a filing-compliance accusation concerning this real-estate sale. The Form 990 question mapped to that indicator concerns disposal of tangible personal property for which Form 8282 was required; the object reconstructed here is commercial real estate. Whether a separate Form 8282 filing obligation applied or was satisfied cannot be inferred from this checkbox alone.

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

### H4 — the donated commercial-real-estate asset was disposed in FY2023 for $550,000 against $590,000 basis

**Status: VERIFIED_PRIMARY AS FILING-LEVEL RECONSTRUCTION.**

FY2022 contains one $590,000 commercial-real-estate contribution and exactly $590,000 of land/building book value. FY2023 reports an `Other` asset sale with $590,000 basis, $550,000 gross amount and a $40,000 loss, while the land/building balance disappears and only equipment remains.

### H5 — the $416,227 receivable is seller financing from that sale

**Status: PLAUSIBLE / UNVERIFIED.**

Temporal coexistence and arithmetic are suggestive but not transaction identity. Trace the receivable through FY2024/FY2025 and obtain deed/note evidence.

### H6 — payroll / executive compensation caused most of the expense spike

**Status: REFUTED AS PRINCIPAL DRIVER.**

Wage delta is only +$3,664; payroll taxes add $41,728.

### H7 — administrative/fundraising bloat caused most of the expense spike

**Status: CONTRADICTED BY FILED FUNCTIONAL CLASSIFICATION.**

Both comparator years report zero management/general and zero fundraising.

### H8 — fraud / diversion / personal enrichment

**Status: UNSUPPORTED.**

The sale/loss and receivable are accounting facts, not evidence by themselves of diversion, improper consideration or personal benefit. Counterparty and transaction terms remain unknown.

## Article-safe financial wording after current closure

> G3’s financial reversal began in 2023 not because revenue collapsed, but because expenses roughly doubled while revenue remained almost flat. The raw IRS filings reconcile the increase category by category: conference and meeting costs rose by about $817,000 and advertising by about $247,000. A separate balance-sheet event is now clearer as well. G3 reported receiving commercial real estate valued at $590,000 in 2022; the 2023 raw return reports an asset sale for $550,000 against a $590,000 basis, producing a $40,000 loss, while the corresponding land-and-building balance disappears. The same return shows a new $416,227 notes/loans receivable, but the filing does not identify the debtor or explicitly link that receivable to the property sale. Deed and note records are therefore still required before naming the property, purchaser or financing terms.
