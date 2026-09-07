# G3 HISTORY — IRS raw XML acquisition gate

**Status:** P0 / ACQUISITION_GATE / PUBLICATION_HOLD  
**Last updated:** 2026-09-08  
**Authority goal:** acquire and checksum the exact IRS e-file XML objects needed to close FY2023 Part IX/Schedule O and FY2024/FY2025 Schedule L without relying on derivative web parsers.

## Why this file exists

The research no longer has an identification problem. The exact IRS/ProPublica object IDs and schedule families are known. The remaining problem is transport: current web PDF renderers and signed-S3 schedule renderers return 403 or are blocked after redirect, while the local container cannot resolve/download the public IRS/ProPublica hosts.

This file turns that blocker into a deterministic acquisition task rather than a recurring search exercise.

## Target returns

| Fiscal year | Filed | EIN | Exact e-file object ID | Required objects | Current status |
|---|---|---|---|---|---|
| FY2023 | 2024-05-21 | `842403597` | `202411429349300611` | `IRS990` Part IX; `IRS990ScheduleO` if present; Part IV schedule manifest | OBJECT_ID_VERIFIED / RAW_XML_NOT_ACQUIRED |
| FY2024 | 2025-05-15 | `842403597` | `202541359349304489` | `IRS990`; `IRS990ScheduleL`; `IRS990ScheduleO`; Schedule J if relevant to compensation-only questions | OBJECT_ID_VERIFIED / SCHEDULE_L_ROUTE_VERIFIED / RAW_XML_NOT_ACQUIRED |
| FY2025 | 2026-05-13 | `842403597` | `202641339349303874` | `IRS990`; `IRS990ScheduleL`; `IRS990ScheduleO` | OBJECT_ID_VERIFIED / SCHEDULE_L_ROUTE_VERIFIED / RAW_XML_NOT_ACQUIRED |

## Official IRS acquisition authority

IRS states that its Form 990 series download page provides the most recent 990-series filings in **XML**, organized by year/month. Current official public families include:

### 2024

Index:
`https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv`

Monthly archives:
`2024_TEOS_XML_01A.zip` through `2024_TEOS_XML_12A.zip`.

### 2025

Index:
`https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv`

Monthly archives include `2025_TEOS_XML_01A.zip` through `12A.zip`, with additional `11B`, `11C`, and `11D` shards.

### 2026

Index:
`https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv`

Current archives include `2026_TEOS_XML_01A.zip`, `02A`, `03A`, `04A`, `05A`, `05B`, `06A`, and `07A`.

Do **not** guess the target ZIP solely from filing month. Read the official index and use the row/object mapping.

## Index selection algorithm

For each target filing:

1. Acquire the official annual `index_YYYY.csv`.
2. Filter for EIN `842403597`.
3. Match the exact `Object ID` already known from the table above.
4. Preserve the complete matching index row, including return/form type, tax period, submission date, taxpayer/organization name, DLN and object ID fields exposed by the current IRS index schema.
5. Use the index mapping / object identity to locate the corresponding XML in the correct annual/monthly archive.
6. Do not substitute another filing for the same tax period unless amendment/resubmission status is explicitly reconciled.

## Required custody receipt

For each acquired archive and extracted XML object record:

- source URL;
- acquisition UTC timestamp;
- HTTP status;
- content length;
- archive filename;
- archive SHA-256;
- member filename/path containing the target object;
- extracted XML byte length;
- extracted XML SHA-256;
- exact object ID;
- EIN;
- tax period;
- parser/tool version used;
- whether the object is original raw XML or a transformed rendering.

A successful HTML render, screenshot, parser page or API summary is **not** a raw-XML custody receipt.

## FY2024 / FY2025 Schedule L parse gate

After raw XML acquisition, inspect the actual `IRS990ScheduleL` object and record, without editorial inference:

1. which Schedule L part(s) are present;
2. each interested-person/business name exactly as filed;
3. relationship / reason for interested-person status where the schema supplies it;
4. transaction type/category;
5. amount, balance or assistance value fields;
6. whether the transaction was corrected;
7. descriptive fields / Schedule O cross-references if any;
8. whether any named person is also a Part VII officer/director/key employee in the same filing;
9. whether the same transaction/person recurs in the adjacent filing year.

Then classify separately:

- `DISCLOSURE_EXISTS`;
- `TRANSACTION_FACTS_VERIFIED`;
- `CONFLICT_POLICY_CONTEXT_VERIFIED`;
- `MISCONDUCT` — **never inferred automatically** from Schedule L presence.

## FY2023 Part IX closure gate

The FY2023 question is not merely `program ratio`. Parse the full functional-expense rows:

- total expenses (col A);
- program services (col B);
- management/general (col C);
- fundraising (col D);
- compensation/officer lines;
- salaries/wages;
- payroll taxes/employee benefits if reported;
- professional fees;
- occupancy;
- travel;
- conferences/conventions/meetings if present;
- printing/publications;
- information technology;
- other expenses and Schedule O descriptions;
- any material row that explains the ~$1.062m FY2022→FY2023 expense increase.

Create a direct FY2022-vs-FY2023 row delta table. Do not attribute the increase until the row delta is computed from source data.

## Known renderer dead ends — do not repeat as if they were new work

### ProPublica

- FY2024 PDF `display_990` object resolves but returns HTTP 403 in current browser transport.
- exact FY2024/FY2025 `IRS990ScheduleL` e-file routes resolve to signed `pp-990-rendered` S3 URLs that the safety/web transport cannot fetch.
- ProPublica organization/API summary is useful for cross-checks but is not the complete Schedule L body.

### Cause IQ

Exact `View PDF` objects for FY2023/FY2024/FY2025 were identified; all returned HTTP 403 in the current web transport.

### Local container

Direct network retrieval of the relevant IRS/ProPublica hosts is unavailable in the current runtime. Do not treat DNS/network failure as source absence.

## Current derivative cross-checks — useful but not closure authority

- ProPublica summary: both FY2024 and FY2025 report conflict-of-interest transactions / Schedule L presence.
- Philanthropy.org FY2024 parser: approximately 84% program / 7% management-general / 9% fundraising; one reported program-service account around $1.2m for four pastor workshops + two large conferences / 2,000+ attendees.
- Cause IQ FY2025 parser: 18 new G3 Press books; catalogue >50; G3+ 500+ audiobooks; two local workshops; Church Network 210 churches; Pastor-Theologian Collective; conference-model transition.

These are cross-checks of the filing family, not independent witnesses.

## Completion criteria

`Q001 Schedule L` may be marked closed only when raw filing content (or an exact faithful primary rendering with full rows) is acquired and the transaction rows are recorded with custody evidence.

`Q002 FY2023 Part IX` may be marked closed only when full row-level FY2023 expense data and the relevant Schedule O descriptions are acquired and compared against FY2022.

Until then:

- no interested-person name or amount from inference;
- no `self-dealing`, `fraud`, `embezzlement`, `private enrichment`, or similar language;
- no claim that the 2023 expense jump was administrative, personal, or alternatively fully explained by program activity.

The correct status is **RAW_OBJECT_ACQUISITION_HOLD**.
