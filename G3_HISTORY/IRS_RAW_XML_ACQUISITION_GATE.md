# G3 HISTORY — IRS raw XML acquisition gate

**Status:** PRIMARY BYTES ACQUIRED / P0 FINANCIAL GATES CLOSED / PUBLICATION_HOLD  
**Last updated:** 2026-09-08  
**Authority:** official IRS TEOS bulk XML, exact-head acquisition workflow.

## Why this file exists

This file began as a transport-blocker runbook because ProPublica/CauseIQ renderers and signed-S3 schedule routes were inaccessible from the research web/container boundary. That blocker has now been bypassed correctly through the official IRS TEOS bulk XML archives.

The old state `RAW_OBJECT_ACQUISITION_HOLD` is **superseded** for FY2022/FY2023 Part IX and FY2024/FY2025 Schedule L.

## Exact acquired returns

| Fiscal year | IRS object / target | Exact-head acquisition result | Primary use | Status |
|---|---|---|---|---|
| FY2022 amended | target `202340569349300209`; matched IRS member `202322939349300637_public.xml` | raw XML SHA-256 `678b391e948adb6090107435369e175cf2694c69705e107f13be6befe361bc03` | Part IX comparator; Schedules D/M/O | **ACQUIRED** |
| FY2023 | `202411429349300611` | raw XML SHA-256 `c8eb0baa2265eadef2b6798c68868f91f8fde6ca9fbffe40e138877df92ce5c0` | Part IX, Schedule O, balance sheet | **ACQUIRED** |
| FY2024 | `202541359349304489` | raw XML SHA-256 `c14f511cf66051b916748440594586b4db1ecdb0d07ab14ef05e01e92524aca3` | Schedule L, Part VII/governance, Schedule O | **ACQUIRED** |
| FY2025 | `202641339349303874` | raw XML SHA-256 `48846b93808c2ffcacac6dc1995fb7890a630ccef9f711fa8a27cd4445541ac2` | Schedule L, Part VII/governance, Schedule O | **ACQUIRED** |

The decisive exact-head workflow is `G3 IRS raw XML acquisition` run **`34208135511`** on Research head **`8a5fedc6a60965d27c472a2a6643fb4e9b1dfe08`**. All matrix jobs (`FY2022_LATER`, `FY2024`, `FY2025`) completed successfully and checked out the exact PR head rather than the synthetic PR merge commit.

Actions artifacts remain **ephemeral research custody**, not publication authorization. The durable corpus therefore preserves object IDs, hashes, component hashes, run/head identity and derived factual rows while raw-byte storage remains governed separately by repository custody policy.

## Q001 — FY2024 / FY2025 Schedule L closure

Both raw filings contain one `IRS990ScheduleL` `BusTrInvolveInterestedPrsnGrp` object.

| Filing | Interested person | Relationship as filed | Amount | Transaction | Revenue sharing |
|---|---|---|---:|---|---|
| FY2024 | `KARIS L BUICE` | `Daughter of Board Member` | **$30,409** | `SALARY` | `false` |
| FY2025 | `KARIS L BUICE` | `Daughter of Board Member` | **$31,880** | `SALARY` | `false` |

The same raw Form 990 context reports in both years:

- `EngagedInExcessBenefitTransInd = false`;
- `BusinessRlnWithFamMemInd = true`;
- conflict-of-interest policy = true;
- annual disclosure = true;
- regular monitoring/enforcement = true;
- compensation-review process indicators = true.

Schedule O says board members discuss potential conflicts and that independent board members determine officer/key-employee salaries according to market rates and standards.

### Evidence classification

- `DISCLOSURE_EXISTS` — **VERIFIED_PRIMARY**.
- `TRANSACTION_FACTS_VERIFIED` — **VERIFIED_PRIMARY**.
- `CONFLICT_POLICY_CONTEXT_VERIFIED` — **VERIFIED_PRIMARY as self-reported governance procedure**.
- `MISCONDUCT` — **NOT ESTABLISHED**.

Do **not** infer the identity of the parent from surname alone. The filing says only `Daughter of Board Member`.

## Q002 — FY2022 → FY2023 Part IX closure

Both raw returns classify all functional expenses as program services and report zero management/general and zero fundraising.

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

The delta reconciles exactly. Conference/meeting and advertising growth are the dominant filed category changes. Payroll and administrative-overhead narratives do not explain the reversal at the Part IX level.

This remains a self-reported tax-return classification, not an independent audit of whether every expenditure was prudent or arm’s-length.

## FY2022 donated-real-estate provenance

The amended FY2022 raw return also closes a previously unclear balance-sheet origin:

### Schedule M

- commercial real estate noncash contribution;
- contribution count: 1;
- Form 990 amount: **$590,000**;
- valuation method: `BROKER ESTIMATION`.

### Schedule D

- land: **$354,000**;
- buildings: **$236,000**;
- equipment net book value: **$31,915**;
- total net land/building/equipment: **$621,915**.

The $354,000 land + $236,000 buildings sum exactly to the $590,000 commercial-real-estate contribution. Schedule O says the FY2022 return was amended because of a missing fair-market value for an asset donated before year end.

This creates a separate follow-up: by FY2023 land/building/equipment had fallen sharply while a $416,227 notes/loans receivable balance appeared. Counterparty, disposition, consideration and note terms remain unresolved; no related-party or wrongdoing inference is permitted from the balance-sheet movement alone.

## FY2024 governance context from raw filing

The raw FY2024 return reports:

- 7 voting governing-body members;
- 6 independent;
- Part VII includes Scott Aniol, Virgil Walker, Joshua Buice, Tom Buck, Chip Thornton, Buck Braswell, Adam Burrell, Matt Broome and Jonathan Frazier;
- Part VII reportable-person count must not be equated mechanically with voting-board count.

Reported compensation includes:

- Scott Aniol: $137,941 reportable compensation + $19,833 other compensation;
- Virgil Walker: $126,075 reportable compensation + $20,462 other compensation;
- listed directors/officers in the remaining rows show $0 reportable compensation from G3 in those rows.

## FY2025 governance context from raw filing

The raw FY2025 return reports:

- 4 voting governing-body members;
- all 4 independent;
- Part VII includes transition/history rows for Scott Aniol, Buck Braswell, Matt Broome, Jonathan Frazier, Jon Norton, Joshua Buice, Tom Buck, Chip Thornton and Adam Burrell.

Part VII therefore cannot be read as a single-date nine-person board snapshot. It contains persons who held reportable roles during the tax period.

Notable filed titles include:

- Scott Aniol — `PRESIDENT AS OF 05/2025`;
- Joshua Buice — `PRESIDENT THROUGH 05/2025`;
- Jonathan Frazier — `CHAIR`;
- Jon Norton — `DIRECTOR`;
- Buck Braswell — `DIRECTOR`;
- Matt Broome — `SECRETARY`.

G3’s event-specific July 2025 announcement remains the stronger source for the formal effective date of Aniol’s presidency (`2025-07-09`). Tax-return title shorthand must not silently rewrite that event date.

## Historical renderer dead ends — retained only to prevent repeated work

The following routes were useful for discovery but are no longer blockers:

- ProPublica PDF/full-filing Schedule L renderers returned 403 or signed-S3 redirects inaccessible to the research transport;
- Cause IQ PDF routes returned 403;
- the local container could not directly retrieve the same hosts.

The official IRS TEOS bulk route solved the acquisition problem. Future agents should **not reopen Q001/Q002 merely because those renderers remain inaccessible**.

## Current completion state

- `Q001 Schedule L` — **CLOSED / VERIFIED_PRIMARY** for the filed rows and governance context; misconduct remains unproved.
- `Q002 FY2023 Part IX` — **CLOSED / VERIFIED_PRIMARY** including exact FY2022 comparator delta.
- donated-real-estate / FY2023 receivable disposition — **OPEN FOLLOW-UP**.
- raw-byte artifact retention — **EPHEMERAL CUSTODY**, governed separately from factual closure and publication authority.

`PUBLICATION_HOLD` remains in force for the overall G3 corpus.
