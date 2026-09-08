# G3 HISTORY — P0 acquisition log — 2026-09-07

**Status:** ACTIVE / FORENSIC LOG  
**Purpose:** record what was actually acquired, what route was attempted, and why unresolved claims remain on HOLD.

## 1. IRS e-file acquisition

### Confirmed filing objects

- FY2023 — object `202411429349300611`, filed 2024-05-21.
- FY2024 — object `202541359349304489`, filed 2025-05-15.
- FY2025 — object `202641339349303874`, filed 2026-05-13.

### Confirmed provenance

ProPublica Nonprofit Explorer states that its full-filing viewer reconstructs Form 990 documents from raw XML released by the IRS. The official IRS Form 990 Series Downloads page provides bulk electronically filed XML by processing year/month.

### Schedule L

For FY2024 and FY2025, the ProPublica full-filing manifest exposes an `IRS990ScheduleL` rendered object. This upgrades `Schedule L exists` from an aggregator flag to a known schedule object associated with a specific IRS e-file filing.

### Retrieval blocker

The rendered schedule links redirect to temporary signed S3 objects. The current research web boundary rejects those redirects as unsafe, while direct XML-download endpoints return access errors in this environment. This is a tooling/acquisition blocker, **not evidence that the schedule is unavailable or empty**.

### Required next acquisition route

Retrieve the exact filing XML from the official IRS annual/monthly bulk archive outside the restricted redirect path, then extract:

- `IRS990ScheduleL`
- Part IX
- Part VII
- Schedule O

and store only the derived research facts / permitted durable artifact under repository custody rules.

## 2. FY2024 Part IX cross-check

A secondary parser that explicitly reproduces IRS Form 990 e-file data reports:

- 84% program services (~$1.2m)
- 7% management/general (~$93k)
- 9% fundraising (~$130k)
- salaries, benefits & payroll, Part IX lines 5–10: ~$483k
- cash: ~$831k
- 7 voting members; 6 independent

These figures are useful bounds but remain secondary to raw IRS XML for quote-safe/disputed analysis.

## 3. FY2023 expense spike

Known:

- FY2022 expense: $1,010,186
- FY2023 expense: $2,071,986
- increase: $1,061,800
- FY2023 other salaries/wages: $292,784 (14.1% of total expense)

Therefore payroll alone cannot explain the expense increase. Exact FY2023 functional lines remain required.

## 4. Georgia legal state

### Acquired primary records

2019 incorporation / Articles of Incorporation, control no. `19085916`:

- Domestic Nonprofit Corporation
- effective 2019-06-06
- principal address 4979 Highway 5, Douglasville
- registered agent Josh Buice at incorporation
- perpetual duration
- 501(c)(3) purpose / no-private-inurement clauses
- board may dissolve by two-thirds vote
- after liabilities, dissolution assets restricted to qualifying exempt purposes / qualifying 501(c)(3) recipients

2019 annual registration:

- Josh Buice — CEO
- Josh Buice — CFO
- David Crowe — Secretary

2020 annual registration (covering 2020/2021):

- Josh Buice — CEO
- Josh Buice — CFO
- David Crowe — Secretary

### Not acquired

- current 2026 Georgia business entity status
- post-Aug. 2026 Articles/Notice of Dissolution
- later annual-registration officer changes

No search-result absence is treated as proof that a dissolution filing does not exist.

## 5. FY2025 governance boundary

Visible IRS-derived FY2025 summary identifies:

- Scott Aniol — `President As Of 05/2025` (extracted filing label)
- Buck Braswell — Director
- Matt Broome — Secretary
- additional people hidden by summary UI

The extracted Aniol title label conflicts with the exact formal G3 announcement that the appointment was effective 2025-07-09. Therefore the tax-return label is not used as an appointment-date authority without raw Part VII/filing context.

The FY2025 return does not establish the August 2026 board.

## 6. G3+ / G3 Press transfer

### Established

Secondary reporting based on an Aug. 27 subscriber email says G3+ was to be acquired/transitioned to an unnamed `another ministry`; reports also suggest the same unnamed ministry was to receive/acquire G3 Press.

### Not established

- identity of transferee
- Right Response Ministries as transferee
- sale vs donation vs license vs operational handoff
- consideration/value
- liabilities assumed
- author/IP treatment
- date of legal closing

### Post-shutdown platform artifact

Google Play currently shows G3+ updated **2026-09-04**, while still displaying:

- developer identity: G3 Ministries
- support: `admin@g3min.org`
- Douglasville address
- existing G3 branding/content

Apple storefronts likewise still display `G3 Ministries For The Church, Inc.` as developer/seller.

Interpretation allowed: the product/platform remained publicly maintained or at least updated under G3 identity after the shutdown announcement.

Interpretation forbidden: this alone proves no transfer occurred, proves a particular buyer, or proves G3 reversed its shutdown.

## 7. P0 state after this pass

| P0 item | State | Change this pass |
|---|---|---|
| Schedule L FY2024/25 | EVIDENCE_HOLD | exact filing objects + schedule-object existence now pinned |
| FY2023 expense spike | EVIDENCE_HOLD | exact filing object pinned; payroll-only explanation excluded |
| Aug. 2026 board | ARCHIVE_HOLD | FY2025 filing boundary clarified; secondary six-name roster not promoted |
| board departures | EVIDENCE_HOLD | FY2024 / Jul. 2025 anchors improved |
| Georgia dissolution | EVIDENCE_HOLD | dissolution mechanics from Articles pinned; current state still missing |
| G3+/Press transfer | EVIDENCE_HOLD | unnamed-transfer claim retained; Right Response rumor rejected; Sep. 4 app artifact added |

## Rule

Tooling failure, blocked redirects, stale search indexes and hidden UI rows are recorded as acquisition limitations. They must never be silently converted into substantive historical conclusions.