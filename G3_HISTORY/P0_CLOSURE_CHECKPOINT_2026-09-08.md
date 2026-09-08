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
- `34220835523` — four-year raw acquisition/receivable trace on exact head `c8bc08d44406c3bd461369f90accb3d1c43cf4fc`, all four matrix jobs green.

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

Raw balance sheets then show a continuous receivable:

| Filing | BOY other notes/loans receivable | EOY other notes/loans receivable | Annual change | Reported investment income |
|---|---:|---:|---:|---:|
| FY2023 | $0 / no carried balance in reconstructed sequence | **$416,227** | **+$416,227** | $0 |
| FY2024 | **$416,227** | **$251,197** | **−$165,030** | **$22,683** |
| FY2025 | **$251,197** | **$153,000** | **−$98,197** | **$15,375** |

The carry-forward identity is exact: FY2023 EOY = FY2024 BOY; FY2024 EOY = FY2025 BOY.

**Finding:** the $416,227 amount is a real continuing notes/loans receivable that was paid down or otherwise reduced across the next two filings.

**Linkage status:** seller financing from the $550,000 property sale is now **materially strengthened but still unverified**. The filings do not name the debtor, note date, interest rate, maturity, collateral or explicit transaction link. The FY2024/FY2025 investment-income amounts are likewise not identified as interest from this note.

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

It labels **Board of Directors** and names:

- Buck Braswell;
- Matt Broome;
- Jon Norton;
- Matt Sikes;
- Dylan Joyner;
- Ron Mooney.

The roster is `VERIFIED_PRIMARY` as of **2026-07-21**.

A corrected CDX continuity query removed `collapse=digest` and searched the exact same official path from **2026-07-21 through 2026-08-31**. Exact-head run `34219682146` returned exactly one capture: `20260721102641`.

**Interpretation:** the archive search for that exact path/window is exhausted. This does **not** prove the board remained unchanged. Absence of a later capture is not continuity evidence.

**Remaining gate:** another dated primary object after July 21 — minutes, resignation/appointment record, another archived official surface or participant document.

## 6. Q005 — Georgia current status CLOSED AS OF ACQUISITION

Official Georgia Secretary of State Business Search for control no. `19085916` reported:

- `G3 Ministries for the Church, Inc.`;
- Domestic Nonprofit Corporation;
- status **`Active/Compliance`**;
- principal office `4979 Highway 5, Douglasville, GA 30135`;
- registered/designated agent `Scott Aniol`.

**Finding:** on the dated Sep. 8 acquisition G3 was not shown as formally dissolved in Georgia despite operational wind-down.

**Boundary:** later corporate filings can change this state.

## 7. Q004 — governance chronology upgraded, not closed

Raw FY2024 reports **7 voting governing-body members, 6 independent** and directly identifies Buice/Buck/Thornton/Braswell/Burrell/Broome/Frazier in director/officer roles.

Raw FY2025 reports **4 voting governing-body members, all 4 independent**, while Part VII contains transition/history-style rows for more people, including Aniol, Buice, Frazier, Norton, Braswell, Broome, Buck, Thornton and Burrell.

Therefore Part VII is not a one-date board snapshot. Exact resignation/start dates and motives still require minutes, resignation instruments or first-person records.

## 8. Q006 — G3+/G3 Press/IP transferee remains OPEN

No acquired primary source names the 2026 acquiring ministry or supplies transaction terms for G3+ / G3 Press.

Fresh searches through Sep. 8 still surface only `another ministry` / an unnamed ministry. This is a documented negative search result, not proof that no private closing occurred.

Living Heritage pre-crisis policy material separately describes Living Heritage as a curriculum publisher and G3 Ministries as operator of G3+. Current Living Heritage access bundling therefore supports commercial/service continuity, not ownership. Treefort remains a technical white-label platform/vendor. App-store seller/developer metadata is platform state, not beneficial ownership.

FY2024/FY2025 Schedule L contains only the family-member salary disclosure described in Q001; it does not reveal a G3+/Press transfer.

**Remaining gate:** named recipient-side or G3 primary announcement, agreement/assignment, exact asset schedule, consideration, board approval/conflicts and closing date.

## 9. Current P0 matrix

| Question | Current state | Remaining gate |
|---|---|---|
| Q001 FY2024/FY2025 Schedule L | **CLOSED / VERIFIED_PRIMARY** | misconduct inference separately unsupported |
| Q002 FY2023 expense jump | **CLOSED / VERIFIED_PRIMARY** | vendor/project prudence is a finer-grained question |
| Q003 late-2026 board | **PARTIAL CLOSURE** | July 21 verified; exact-path Wayback exhausted; other late-Aug primary continuity needed |
| Q004 director transition chronology | **OPEN / materially narrowed** | resignation/minutes/transition records |
| Q005 Georgia dissolution status | **CLOSED AS OF ACQUISITION** | only later status change can reopen |
| Q006 G3+/Press/IP transferee and terms | **OPEN** | named primary transferee + transaction documents |
| Q006A FY2022 real estate / FY2023 receivable | **PARTIAL CLOSURE** | sale closed at filing level; parcel/counterparty/note linkage remains |

## 10. Structural reconciliation state

Staging evidence now extends through **PASS17**. These files preserve acquisition history and corrections; they are not a second independent evidence system.

Current important canonical promotions already completed:

- raw Schedule L findings → master financial/open-question/claims layers;
- FY2022→FY2023 exact Part IX delta → master financial/open-question layers;
- July 21 official board roster → governance/open-question layers;
- Georgia `Active/Compliance` → open-question/claims layers;
- FY2023 $550,000 sale / $590,000 basis / $40,000 loss → financial/open-question layers;
- Wayback exact-path exhaustion → open-question layer;
- PASS17 preserves the multi-year receivable trace pending final master wording normalization.

Remaining structural work before article-ready status:

1. normalize the multi-year receivable trace consistently across `FINANCIAL_FORENSICS_2023.md`, `OPEN_QUESTIONS.md`, master claims/source notes and article outline;
2. reconcile staging PASS3–PASS17 without double-counting aliases/access upgrades;
3. normalize legacy rights/publication-state columns;
4. preserve durable custody metadata for decisive acquired objects under repository policy;
5. refresh PR #188 body/counts against the resulting exact head and re-check branch/base/CI;
6. keep `PUBLICATION_HOLD=true`.
