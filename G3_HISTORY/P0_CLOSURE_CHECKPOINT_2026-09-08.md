# G3 HISTORY — P0 closure checkpoint, 2026-09-08

**Status:** ACTIVE / STRUCTURAL / PUBLICATION_HOLD  
**Purpose:** preserve primary-evidence closures discovered after PASS15 before the next canonical `SOURCE_LEDGER` / `CLAIMS_LEDGER` reconciliation.

This checkpoint **supersedes stale HOLD wording** in `OPEN_QUESTIONS.md`, `GOVERNANCE.md`, and `EVIDENCE_RECONCILIATION_PASS3_PASS11.md` only for the narrow findings below. It does not authorize publication, does not merge the research into `main`, and does not convert dated evidence into broader causal conclusions.

## 1. Q002 — FY2023 Part IX is no longer an acquisition HOLD

Official IRS raw XML object:

- EIN: `84-2403597`
- object: `202411429349300611`
- official batch: `2024_TEOS_XML_05A`
- raw XML SHA-256: `c8eb0baa2265eadef2b6798c68868f91f8fde6ca9fbffe40e138877df92ce5c0`

The raw return reports total expenses of **$2,071,986** and allocates them entirely to program services, with management/general and fundraising reported as zero. The largest Part IX rows are:

- conferences / meetings: **$1,253,557**
- advertising: **$307,574**
- other salaries / wages: **$292,784**

Therefore the old proposition that exact FY2023 Part IX still had to be obtained is superseded.

**Allowed conclusion:** the filing itself does not support an explanation in which most of the FY2023 jump was classified as administrative/private expense.

**Still open:** a category-by-category explanation of the approximately $1.062m year-over-year increase requires the authoritative FY2022 Part IX baseline. ProPublica exposes two FY2022 filing objects (`202322939349300637` and `202340569349300209`); the later filing is now explicitly targeted in acquisition v3 so amended/resubmitted-return ambiguity is not silently ignored.

## 2. Q003 — official July 21, 2026 board roster acquired

Wayback acquisition run `34164109246` acquired the exact official G3 `Who We Are` snapshot:

- original: `http://g3min.org/about/who-we-are/`
- timestamp: `20260721102641`
- raw archived payload SHA-256: `a946cafd2e02252ebbf83deb19ee59015ca1a808cb7a214b85fb3468f71b5865`
- decoded HTML SHA-256: `30908b37854208516bc7681d8a33e089e1335e611cc1c3fc9bcc8314250b5dd7`

The official archived page explicitly labels **Board of Directors** and names:

- Buck Braswell
- Matt Broome
- Jon Norton
- Matt Sikes
- Dylan Joyner
- Ron Mooney

This upgrades the six-name roster from secondary/archive-discovery status to **VERIFIED_PRIMARY as of 2026-07-21**.

The first acquisition tool falsely reported `all_six_names_present=false` because the Wayback response body was Zstandard-compressed while being presented as an HTML object. Manual decode demonstrated the names. Acquisition v2 now preserves the raw payload, decodes Zstandard before text parsing, and records raw/decoded hashes independently.

**Still open:** July 21 must not be silently equated with the exact late-August crisis date. A later official snapshot or other primary continuity evidence is still preferable before saying “the board on the day of the crisis was exactly these six.”

## 3. Q005 — Georgia current corporate status acquired

Georgia Secretary of State acquisition run `34164109186` obtained an official Business Search result for control number `19085916`:

- business: `G3 Ministries for the Church, Inc.`
- type: `Domestic Nonprofit Corporation`
- principal office: `4979 Highway 5, Douglasville, GA, 30135, USA`
- registered/designated agent: `Scott Aniol`
- status: **`Active/Compliance`**

The workflow failed only because the v2 parser required an internal `businessId` for a detail-page upgrade even after the official search-result row had already been acquired. That is a tooling false negative, not an evidence failure. Acquisition v3 treats the exact official search-result row as sufficient for current-state status while keeping detail-page acquisition as a nonfatal upgrade.

**Allowed conclusion:** as of the official acquisition, G3 was **not shown as formally dissolved in Georgia**; it was listed `Active/Compliance`.

**Boundary:** operational wind-down is distinct from corporate dissolution, and a future filing could change the status after this dated observation.

## 4. Q001 — Schedule L is now an archive-extraction problem, not a network mystery

IRS run `34164109120` downloaded the official FY2024 and FY2025 TEOS batch ZIPs successfully:

- FY2024 batch `2025_TEOS_XML_05A.zip` — SHA-256 `9b0b49aa8b9a68b92cf22c14fcd5239c33a585efd1e00a9407499260156e8c1e`
- FY2025 batch `2026_TEOS_XML_05A.zip` — SHA-256 `1a0782742173325aecc131dc1bb399490f6958e0c71bf8dbad839f67dcded849`

Python 3.12 failed only when reading members with an unsupported ZIP compression method. Acquisition v3 adds a fail-closed external archive-reader fallback (`bsdtar` / `7z` / `unzip`) while retaining exact batch/member hashes.

No Schedule L interested person, amount, relationship, or transaction type is inferred until the raw XML component is actually extracted.

## 5. Current P0 closure state after this checkpoint

| Question | State after checkpoint | Remaining proof gate |
|---|---|---|
| Q001 FY2024/FY2025 Schedule L | **OPEN / materially narrowed** | extract raw XML members and inspect Parts I–IV |
| Q002 FY2023 expense jump | **PARTIAL CLOSURE** | FY2023 composition closed; FY2022 raw baseline/delta remains |
| Q003 late-2026 board | **PARTIAL CLOSURE** | July 21 official roster verified; exact late-August continuity still open |
| Q004 director departure chronology | **OPEN** | primary resignation/minutes/archived transitions |
| Q005 Georgia dissolution status | **CLOSED AS OF ACQUISITION DATE** | only later status changes can reopen |
| Q006 G3+/Press/IP transferee and terms | **OPEN** | named primary transferee + agreement/announcement/consideration |

## 6. Structural debt explicitly preserved

The canonical ledgers still stop at `G3-S054` / `G3-C068`. PASS3–PASS15 plus this checkpoint must be reconciled sequentially without double-counting underlying objects.

Before article-ready status:

1. promote/upgrade only canonical source objects;
2. update stale Q002/Q003/Q005 wording in master dossiers;
3. normalize legacy rights/publication-state columns;
4. make the corrected IRS/Georgia/Wayback workflows green on one exact PR head;
5. refresh PR #188 body/counts against that exact head;
6. keep `PUBLICATION_HOLD=true`.
