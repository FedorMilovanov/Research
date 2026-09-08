# G3 HISTORY — P0 closure checkpoint, 2026-09-08

**Status:** ACTIVE / STRUCTURAL / PUBLICATION_HOLD  
**Purpose:** canonical checkpoint for the current primary-evidence closures and the remaining P0 boundaries.

This checkpoint does not authorize publication, does not merge G3 research into `main`, and does not convert accounting correlation, archive absence or platform continuity into stronger claims than the underlying evidence supports.

## 1. Current primary acquisition authority

The decisive raw-IRS evidence now rests on repeated exact-head acquisitions of the same primary objects.

### Core filing objects

| Filing | IRS object | Raw XML SHA-256 |
|---|---|---|
| FY2022 amended comparator | target `202340569349300209`; matched batch member `202322939349300637_public.xml` | `678b391e948adb6090107435369e175cf2694c69705e107f13be6befe361bc03` |
| FY2023 | `202411429349300611` | `c8eb0baa2265eadef2b6798c68868f91f8fde6ca9fbffe40e138877df92ce5c0` |
| FY2024 | `202541359349304489` | `c14f511cf66051b916748440594586b4db1ecdb0d07ab14ef05e01e92524aca3` |
| FY2025 | `202641339349303874` | `48846b93808c2ffcacac6dc1995fb7890a630ccef9f711fa8a27cd4445541ac2` |

Important exact-head runs:

- `34208135511` — FY2022/FY2024/FY2025 raw acquisition + deterministic Schedule L/Part IX readback;
- `34220049227` — FY2023 asset-sale readback on exact head `a5bb664578ad4c238fc7edbd821285a6647f3d53`;
- `34220835523` — four-year raw acquisition/receivable trace on exact head `c8bc08d44406c3bd461369f90accb3d1c43cf4fc`, all four matrix jobs green;
- `34233453690` — exact-head FY2025 full-leaf keyword trace on `1f75d2b831666128ccff025fc9f5a93c8a6dfd53`, establishing the Living Heritage separation narrative directly from raw `IRS990/Desc`.

The FY2022 target-object ID / ZIP-member basename mismatch remains preserved in custody metadata rather than silently normalized.

## 2. Q001 — FY2024/FY2025 Schedule L CLOSED

Raw Schedule L records one interested-person business transaction in each filing:

| Filing | Interested person | Relationship | Transaction | Amount | Revenue sharing |
|---|---|---|---|---:|---|
| FY2024 | `KARIS L BUICE` | `Daughter of Board Member` | `SALARY` | **$30,409** | `false` |
| FY2025 | `KARIS L BUICE` | `Daughter of Board Member` | `SALARY` | **$31,880** | `false` |

Both filings report `EngagedInExcessBenefitTransInd=false`, `BusinessRlnWithFamMemInd=true`, conflict-of-interest/disclosure/monitoring controls and compensation-review processes.

**Finding:** disclosed family-member salary is `VERIFIED_PRIMARY`.

**Firewall:** Schedule L presence does not prove self-dealing, excess benefit, fraud, embezzlement or private enrichment. The filed relationship does not identify the parent; surname alone is insufficient.

## 3. Q002 — FY2022 → FY2023 expense reversal CLOSED

Exact Part IX delta:

| Category | FY2022 | FY2023 | Delta |
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

Both filings classify all functional expenses as program services and report zero management/general and fundraising.

**Finding:** at the filed Part IX category level, the financial reversal was overwhelmingly conference/meeting plus advertising expansion. Payroll/admin did not drive the increase.

**Boundary:** Form 990 classification is self-reported accounting evidence, not an independent audit of prudence, vendor pricing or arm’s-length terms.

## 4. Q006A — donated real-estate sale CLOSED at filing level; counterparty/note linkage OPEN

### FY2022 provenance

Raw FY2022 Schedule M reports one commercial-real-estate noncash contribution:

- value: **$590,000**;
- valuation method: `BROKER ESTIMATION`.

Raw Schedule D reports:

- land: **$354,000**;
- buildings: **$236,000**;
- land + buildings: **$590,000**;
- equipment net: **$31,915**;
- total net land/building/equipment: **$621,915**.

Schedule O says the amended return corrected missing FMV for an asset donated before year end.

### FY2023 disposition

Exact raw FY2023 Form 990 reports:

- `GrossAmountSalesAssetsGrp/OtherAmt` = **$550,000**;
- `LessCostOthBasisSalesExpnssGrp/OtherAmt` = **$590,000**;
- `GainOrLossGrp/OtherAmt` = **−$40,000**;
- beginning net land/building/equipment = **$621,915**;
- ending net land/building/equipment = **$16,777**.

The surviving $16,777 is fully accounted for by equipment (`$45,974` basis less `$29,197` accumulated depreciation). The $590,000 land/building object therefore disappears in the same filing that reports an `Other` asset sale with exactly $590,000 basis.

**Finding:** at the filing/accounting-object level, the donated $590,000 commercial-real-estate asset was disposed in FY2023 for **$550,000 gross proceeds**, producing a **$40,000 loss**.

A derivative summary that displays `Sales of Assets −$40,000` is showing the **loss**, not the gross sale price.

### Notes/loans receivable trace

Raw balance sheets show a continuous receivable:

| Filing | BOY other notes/loans receivable | EOY other notes/loans receivable | Annual change | Reported investment income |
|---|---:|---:|---:|---:|
| FY2023 | $0 / no carried balance in reconstructed sequence | **$416,227** | **+$416,227** | $0 |
| FY2024 | **$416,227** | **$251,197** | **−$165,030** | **$22,683** |
| FY2025 | **$251,197** | **$153,000** | **−$98,197** | **$15,375** |

The carry-forward identity is exact: FY2023 EOY = FY2024 BOY; FY2024 EOY = FY2025 BOY.

**Finding:** the $416,227 amount is a real continuing notes/loans receivable that was paid down or otherwise reduced across the next two filings.

**Linkage status:** seller financing from the $550,000 property sale is **materially strengthened but still unverified**. The filings do not name the debtor, note date, interest rate, maturity, collateral or explicit transaction link. The FY2024/FY2025 investment-income amounts are likewise not identified as interest from this note.

**Remaining gate:** exact parcel/legal description, donor/grantor, purchaser/grantee, cash at closing, note/security instrument, interest/maturity/collateral, board approval/conflicts and subsequent disposition of the remaining $153,000.

### Official-record access boundary

- Douglas County Clerk / Georgia DOR authority surfaces are reachable;
- Douglas qPublic is Cloudflare-blocked (`403`) in the research runtime;
- GSCCCA public Real Estate Name Search form and Douglas parameters were acquired and submitted unauthenticated;
- result POSTs route automatically to `frmLogin` instead of deed rows;
- no login, subscription, payment, premium search or access-control bypass was attempted.

`4979 Highway 5` remains only a corporate/principal-address and parcel lead. Address overlap is not title evidence and does not identify the $590,000 property.

## 5. Q003 — July 21 board VERIFIED_PRIMARY; exact late-August continuity remains open

Official archived G3 `Who We Are` snapshot:

- original path: `http://g3min.org/about/who-we-are/`;
- timestamp: `20260721102641`;
- raw archived payload SHA-256: `a946cafd2e02252ebbf83deb19ee59015ca1a808cb7a214b85fb3468f71b5865`;
- decoded HTML SHA-256: `30908b37854208516bc7681d8a33e089e1335e611cc1c3fc9bcc8314250b5dd7`.

It labels **Board of Directors** and names Buck Braswell, Matt Broome, Jon Norton, Matt Sikes, Dylan Joyner and Ron Mooney.

The roster is `VERIFIED_PRIMARY` as of **2026-07-21**.

A corrected CDX continuity query removed `collapse=digest` and searched the exact same official path from **2026-07-21 through 2026-08-31**. Exact-head run `34219682146` returned exactly one capture: `20260721102641`.

**Interpretation:** the archive search for that exact path/window is exhausted. This does **not** prove the board remained unchanged. Absence of a later capture is not continuity evidence.

**Remaining gate:** another dated primary object after July 21 — minutes, resignation/appointment record, another archived official surface or participant document.

## 6. Q005 — Georgia current status CLOSED AS OF ACQUISITION; detail/history route now exact-bounded

Official Georgia Secretary of State Business Search for control no. `19085916` reported:

- `G3 Ministries for the Church, Inc.`;
- Domestic Nonprofit Corporation;
- status **`Active/Compliance`**;
- principal office `4979 Highway 5, Douglasville, GA 30135`;
- registered/designated agent `Scott Aniol`.

The current result row embeds internal `businessId=2751672` in the official JavaScript navigation call. The acquisition parser was corrected to recognize that current markup and to reproduce the site's own detail POST contract.

Exact-head run `34244820320` on Research head `3d9b30ff4b0845b0def019a02c76584028926b8e` verified the search row and internal business ID. It then POSTed to `/BusinessSearch/BusinessInformation` with the official fields `businessId=2751672`, `businessType=Domestic Nonprofit Corporation`, `fromSearch=true`. The detail endpoint returned **HTTP 403**; query/path GET fallbacks also returned 403.

**Finding:** on the dated Sep. 8 acquisition G3 was not shown as formally dissolved in Georgia despite operational wind-down.

**Acquisition boundary:** current search-row state is primary-accessible; the detail/filing-history route is now exactly resolved but access-blocked. The absence of later filing IDs in the corpus is no longer attributable to an untested navigation method or parser omission.

**Boundary:** later corporate filings can change the current status; detail-route 403 does not prove later filings do not exist.

## 7. Q004 — governance chronology materially narrowed; public archive + Georgia detail routes exhausted

Raw FY2024 reports **7 voting governing-body members, 6 independent** and directly identifies Buice/Buck/Thornton/Braswell/Burrell/Broome/Frazier in director/officer roles.

Raw FY2025 reports **4 voting governing-body members, all 4 independent**, while Part VII contains transition/history-style rows for more people, including Aniol, Buice, Frazier, Norton, Braswell, Broome, Buck, Thornton and Burrell.

Therefore Part VII is not a one-date board snapshot. Exact resignation/start dates and motives still require minutes, resignation instruments or first-person records.

For May 1–July 20, 2025, both identified official historical roster paths have successful bounded empty-CDX acquisitions:

- `/about/who-we-are/` — successful run `34228201641`, all three monthly segments `VALID_EMPTY_CDX`;
- `/vision/leadership/` — successful run `34232494274` on head `ddaddeb8ac03892660dfb017ec9946b9379e33d5`, all three monthly segments `VALID_EMPTY_CDX`, combined state `VALID_EMPTY_ALL_LEGACY_SEGMENTS`.

A later Archive.org timeout/503 rerun is transport failure and does not negate those successful acquisitions.

The Georgia corporate family now also has exact early locators:

- Articles — filing `17370469`, 2019-06-06;
- 2019 Annual Registration — filing `17449198`, 2019-07-16, Buice CEO/CFO, Crowe Secretary, Buice registered agent;
- 2020/2021 Annual Registration — filing `18903966`, 2020-03-30, same officer/agent structure and Buice as filing authorizer with title `Director`.

These strengthen the early founder-centric corporate chronology but do not date 2025 exits/appointments. As documented in Q005, the current Georgia detail/history route is now exactly reproduced and 403-blocked.

**Finding:** both known official G3 roster-path searches and the unauthenticated Georgia detail/history route are exhausted as public transition-discovery paths. The exact director transition dates remain open because archive absence/access denial is not resignation or appointment evidence.

## 8. Q006 — G3+/G3 Press/IP transferee remains OPEN; Living Heritage 2025 separation CLOSED

No acquired primary source names the 2026 acquiring ministry or supplies transaction terms for G3+ / G3 Press.

Fresh searches through Sep. 8 still surface only `another ministry` / an unnamed ministry. This is a documented negative search result, not proof that no private closing occurred.

The FY2025 raw Form 990 now closes one related but distinct fact. Exact-head run `34233453690` searched all 401 `IRS990` leaves and found one relevant `IRS990/Desc` leaf. The filed narrative says G3 **separated Living Heritage Homeschool as an independent entity from G3 Ministries** during 2025.

**Verified primary:** 2025 Living Heritage separation from G3.

**Still unverified:** that Living Heritage was the unnamed ministry that acquired G3+, G3 Press or other G3 assets in the 2026 wind-down. Current G3+ access bundling is commercial/service continuity, not assignment/title evidence. App-store seller/developer metadata is likewise platform state, not beneficial ownership.

FY2024/FY2025 Schedule L contains only the family-member salary disclosure described in Q001; it does not reveal a G3+/Press transfer.

**Remaining gate:** named recipient-side or G3 primary announcement, agreement/assignment, exact asset schedule, consideration, board approval/conflicts and closing date.

## 9. Current P0 matrix

| Question | Current state | Remaining gate |
|---|---|---|
| Q001 FY2024/FY2025 Schedule L | **CLOSED / VERIFIED_PRIMARY** | misconduct inference separately unsupported |
| Q002 FY2023 expense jump | **CLOSED / VERIFIED_PRIMARY** | vendor/project prudence is a finer-grained question |
| Q003 late-2026 board | **PARTIAL CLOSURE** | July 21 verified; exact-path Wayback exhausted; other late-Aug primary continuity needed |
| Q004 director transition chronology | **OPEN / materially narrowed** | both known May–July archive routes + unauthenticated Georgia detail route exhausted; resignation/minutes/appointment records or authorized filing history needed |
| Q005 Georgia dissolution status | **CLOSED AS OF ACQUISITION** | only later status change can reopen; detail history presently 403-blocked |
| Q006 G3+/Press/IP transferee and terms | **OPEN / Living Heritage subclaim closed** | 2025 separation verified; named 2026 transferee + transaction documents still absent |
| Q006A FY2022 real estate / FY2023 receivable | **PARTIAL CLOSURE** | sale closed at filing level; parcel/counterparty/note linkage remains |

## 10. Structural reconciliation state

Staging evidence extends through **PASS18**. These files preserve acquisition history and corrections; they are not a second independent evidence system.

Current important canonical promotions completed:

- raw Schedule L findings → master financial/open-question/claims layers;
- FY2022→FY2023 exact Part IX delta → master financial/open-question layers;
- July 21 official board roster → governance/open-question layers;
- Georgia `Active/Compliance` → open-question/claims layers;
- FY2023 $550,000 sale / $590,000 basis / $40,000 loss and multi-year receivable trace → financial/open-question/checkpoint layers;
- late-2026 exact-path Wayback exhaustion → open-question/checkpoint layers;
- both known May–July 2025 historical roster paths → director-transition/checkpoint layers;
- Georgia search-result `businessId=2751672`, official detail POST contract and 403 access boundary → director-transition/checkpoint layers;
- exact early Georgia filing locators `17370469`, `17449198`, `18903966` → director-transition/checkpoint provenance;
- FY2025 Living Heritage separation → asset-transfer/checkpoint layers using the existing raw-IRS source family rather than a duplicate Cause IQ evidence family.

Repository-structure work remaining at this checkpoint is no longer evidence reconciliation debt. The remaining items are substantive proof gates listed above, plus PR metadata/exact-head validation. `PUBLICATION_HOLD=true` remains intentional until a later journalism/product handoff pins an immutable Research commit and frozen claim/source set.