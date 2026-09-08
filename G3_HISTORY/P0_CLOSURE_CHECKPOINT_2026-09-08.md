# G3 HISTORY — P0 closure checkpoint, 2026-09-08

**Status:** ACTIVE / STRUCTURAL / PUBLICATION_HOLD  
**Purpose:** canonical checkpoint for P0 financial/legal/governance closures after exact-head primary acquisition.

This checkpoint does not authorize publication and does not merge G3 research into `main`. It records what is now proved, what remains date-bounded, and which former HOLDs are obsolete.

## 1. Exact-head acquisition authority

The decisive IRS acquisition/readback ran on Research exact head:

`8a5fedc6a60965d27c472a2a6643fb4e9b1dfe08`

Workflow:

`G3 IRS raw XML acquisition` — run **`34208135511`** — **success**.

All three matrix jobs succeeded:

- `FY2022_LATER`;
- `FY2024`;
- `FY2025`.

The workflow checked out the actual PR head, not GitHub’s synthetic PR merge SHA, and emitted deterministic evidence summaries from the acquired primary bytes.

Repository authority integrity was also green on that exact head (`34208135444`). Georgia current-status acquisition was green (`34208135421`). A later Wayback rerun failed technically, but it does not invalidate the earlier successfully acquired and hashed July 21 official snapshot described below.

## 2. Q001 — FY2024/FY2025 Schedule L CLOSED

### FY2024

- object: `202541359349304489`;
- raw XML SHA-256: `c14f511cf66051b916748440594586b4db1ecdb0d07ab14ef05e01e92524aca3`;
- Schedule L SHA-256: `bc6442e39145162f663d45a9de9cd4a1d1c58b250a7dc9aa2f6105cb5d3ee248`.

Schedule L records:

- interested person: **`KARIS L BUICE`**;
- relationship: **`Daughter of Board Member`**;
- transaction: **`SALARY`**;
- amount: **$30,409**;
- revenue sharing: `false`.

### FY2025

- object: `202641339349303874`;
- raw XML SHA-256: `48846b93808c2ffcacac6dc1995fb7890a630ccef9f711fa8a27cd4445541ac2`;
- Schedule L SHA-256: `d95315d1208039c526d2ff3fca3ce9a364f6d47bf26e0882122baa19b6b99d1b`.

Schedule L records the same filed relationship/transaction description with amount **$31,880**.

Both filings report:

- `EngagedInExcessBenefitTransInd=false`;
- `BusinessRlnWithFamMemInd=true`;
- conflict-of-interest policy = true;
- annual disclosure = true;
- regular monitoring/enforcement = true;
- compensation-process indicators = true.

**Finding:** G3 disclosed salary paid to a person identified as the daughter of a board member in both years.

**Firewall:** the disclosure does **not** itself prove self-dealing, excess benefit, fraud, embezzlement or private enrichment. Do not infer the specific parent from surname alone; the filed relationship says only `Daughter of Board Member`.

## 3. Q002 — FY2022 → FY2023 expense reversal CLOSED

### Primary objects

FY2023:

- object `202411429349300611`;
- raw XML SHA-256 `c8eb0baa2265eadef2b6798c68868f91f8fde6ca9fbffe40e138877df92ce5c0`.

FY2022 amended comparator:

- acquisition target `202340569349300209`;
- matched IRS batch member basename `202322939349300637_public.xml`;
- raw XML SHA-256 `678b391e948adb6090107435369e175cf2694c69705e107f13be6befe361bc03`;
- return marks `AmendedReturnInd = X` and reports the authoritative FY2022 totals.

The target/member-name mismatch remains preserved as a provenance note rather than silently normalized.

### Exact Part IX delta

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

Both years classify all functional expenses as program services and report zero management/general and fundraising.

**Finding:** the 2023 reversal is explained at the filed Part IX category level primarily by conference/meeting expansion (**+$817,283**) and advertising (**+$246,511**), partly offset by lower occupancy. Payroll/admin is not the main filed driver.

**Boundary:** this is tax-return category evidence, not an independent audit of prudence, pricing or arm’s-length terms.

## 4. FY2022 real-estate provenance CLOSED; disposition question OPEN

Raw FY2022 Schedule M reports:

- one commercial-real-estate noncash contribution;
- amount **$590,000**;
- valuation method `BROKER ESTIMATION`.

Schedule D reports:

- land: **$354,000**;
- buildings: **$236,000**;
- equipment net: **$31,915**;
- total net land/building/equipment: **$621,915**.

The land + building amounts sum exactly to the $590,000 commercial-real-estate contribution. Schedule O says the amended return corrected missing FMV for an asset donated before year end.

By FY2023, net land/building/equipment had fallen sharply and a **$416,227 notes/loans receivable** balance appeared.

**Open follow-up:** identify property disposition, counterparty, consideration, note terms, board authorization and later collection/write-down. No related-party/wrongdoing inference is currently established.

## 5. Q003 — July 21, 2026 board roster VERIFIED_PRIMARY

Wayback acquisition run `34164109246` acquired the exact official G3 `Who We Are` snapshot:

- original: `http://g3min.org/about/who-we-are/`;
- timestamp: `20260721102641`;
- raw archived payload SHA-256: `a946cafd2e02252ebbf83deb19ee59015ca1a808cb7a214b85fb3468f71b5865`;
- decoded HTML SHA-256: `30908b37854208516bc7681d8a33e089e1335e611cc1c3fc9bcc8314250b5dd7`.

The official page labels **Board of Directors** and names:

- Buck Braswell;
- Matt Broome;
- Jon Norton;
- Matt Sikes;
- Dylan Joyner;
- Ron Mooney.

This roster is **VERIFIED_PRIMARY as of 2026-07-21**.

**Still open:** exact continuity from July 21 to the late-August crisis date. Do not silently replace the date-bounded statement with `the board on the day of the crisis was exactly these six` until later primary continuity evidence is acquired.

## 6. Q005 — Georgia current status CLOSED AS OF ACQUISITION

Official Georgia Secretary of State Business Search for control no. `19085916` returned:

- `G3 Ministries for the Church, Inc.`;
- Domestic Nonprofit Corporation;
- status **`Active/Compliance`**;
- principal office `4979 Highway 5, Douglasville, GA 30135`;
- registered/designated agent `Scott Aniol`.

Current exact-head Georgia workflow `34208135421` completed successfully.

**Finding:** at the dated acquisition, G3 was **not shown as formally dissolved in Georgia**, even though it had announced operational wind-down.

**Boundary:** later filings can change corporate status.

## 7. Q004 — governance chronology materially upgraded, not closed

Raw FY2024 Form 990 reports 7 voting governing-body members, 6 independent, and Part VII identifies Scott Aniol, Virgil Walker, Joshua Buice, Tom Buck, Chip Thornton, Buck Braswell, Adam Burrell, Matt Broome and Jonathan Frazier in reportable roles.

Raw FY2025 reports **4 voting governing-body members, all 4 independent**, while Part VII includes transition/history rows for Scott Aniol, Buck Braswell, Matt Broome, Jonathan Frazier, Jon Norton, Joshua Buice, Tom Buck, Chip Thornton and Adam Burrell.

Therefore Part VII is not a one-date board snapshot. Exact resignation/departure dates and motives still require minutes, resignation instruments or first-person statements.

## 8. Q006 — G3+/Press/IP transferee remains OPEN

No primary source currently identifies the acquiring ministry or transaction terms for G3+/G3 Press.

Important negative boundary after Schedule L closure:

**FY2024/FY2025 Schedule L does not disclose a Living Heritage/G3+ or Press asset transfer.** It discloses the family-member salary transaction described above.

Living Heritage ↔ G3+ commercial/access continuity, app-store metadata, Treefort infrastructure and G3 storefront persistence are platform-state evidence only. They do not identify legal transferee, consideration, board approval or closing terms.

## 9. Current P0 matrix

| Question | Current state | Remaining gate |
|---|---|---|
| Q001 FY2024/FY2025 Schedule L | **CLOSED / VERIFIED_PRIMARY** | misconduct inference remains separately unsupported |
| Q002 FY2023 expense jump | **CLOSED / VERIFIED_PRIMARY** | vendor/project prudence is a separate finer-grained question |
| Q003 late-2026 board | **PARTIAL CLOSURE** | July 21 roster verified; exact late-Aug continuity still open |
| Q004 director departure chronology | **OPEN / materially narrowed** | primary resignation/minutes/transition records |
| Q005 Georgia dissolution status | **CLOSED AS OF ACQUISITION** | only later status changes can reopen |
| Q006 G3+/Press/IP transferee and terms | **OPEN** | named primary transferee + agreement/announcement/consideration |
| Q006A FY2022 real-estate disposition / FY2023 receivable | **OPEN** | property/counterparty/note records |

## 10. Remaining structural debt

Canonical ledgers still require a final promotion/rewrite pass for PASS3–PASS15 and the primary acquisitions without double-counting derivative views of the same filing/document.

Before article-ready status:

1. upgrade canonical IRS source/claim rows from old parser/HOLD language to raw-primary status;
2. update governance master text with July 21 primary board roster and raw FY2025 Part VII boundaries;
3. normalize legacy rights/publication-state columns without changing factual findings;
4. reconcile acquisition artifacts into durable custody metadata under repository policy;
5. refresh PR #188 body/counts and CI against the resulting exact head;
6. keep `PUBLICATION_HOLD=true`.
