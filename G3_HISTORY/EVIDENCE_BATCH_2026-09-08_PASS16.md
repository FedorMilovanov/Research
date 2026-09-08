# G3 HISTORY — evidence batch 2026-09-08 PASS16

**Status:** STAGING / PUBLICATION_HOLD  
**Purpose:** preserve exact-head IRS readback authority after P0 closure and open a disciplined property/deed lane for the FY2022 donated-real-estate → FY2023 receivable movement without falsely identifying the donated property or counterparty.

## Repository checkpoint

Before this pass, canonical master files were refreshed through Research head `6da30120c2d5cae762acfa6813d0b29b2ec179fe`:

- `OPEN_QUESTIONS.md`;
- `FINANCIAL_FORENSICS_2023.md`;
- `IRS_RAW_XML_ACQUISITION_GATE.md`;
- `P0_CLOSURE_CHECKPOINT_2026-09-08.md`;
- `GOVERNANCE.md`;
- `SOURCE_LEDGER.md`;
- `CLAIMS_LEDGER.md`.

PR #188 remained Draft, mergeable, and at that checkpoint was **102 commits ahead / 0 behind** main. `PUBLICATION_HOLD=true`.

## Provisional sources

| ID | Source | Class | Access | Locator | Rights | Publication | Use / boundary |
|---|---|---|---|---|---|---|---|
| G3-S132 | Official IRS TEOS raw XML acquired/read back through exact-head Research workflow `34208135511` | A1 / alias of canonical IRS filing family | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | **ALIAS_UNDERLYING / custody receipt, not an independent filing witness.** Run on exact Research head `8a5fedc6a60965d27c472a2a6643fb4e9b1dfe08`. FY2024 raw SHA `c14f511c…4aca3`; FY2025 raw SHA `48846b93…41ac2`; FY2022 amended comparator raw SHA `678b391e…1bc03`. Deterministic summary exposed Schedule L, Part VII, governance fields and FY2022 Part IX/D/M/O. Canonical authority remains G3-S002/G3-S028. |
| G3-S133 | Douglas County, Georgia Clerk of Superior Court — official deed/public-record access page | A1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Official county page states the Clerk records deeds/mortgages and links `Douglas County Deed Lookup`; real-estate records are public through the clerk. Current research browser hits a redirect loop when following the Cott deed-search target. This is an acquisition blocker, not evidence absence. Locator: `https://www.douglascountyga.gov/193/Clerk-of-Superior-Court`. |
| G3-S134 | Georgia Department of Revenue — `Property Records Online` county directory | A1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Official state directory maps Douglas County property records to `qpublic.net/ga/douglas/`. Establishes the authoritative assessor-search route for parcel/address identification. Locator: `https://dor.georgia.gov/property-records-online`. |
| G3-S135 | CountyOffice — property-record mirror for `4979 Hwy 5, Douglasville, GA 30135` | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | REFERENCE | REFERENCE | Secondary property-index surface. Reports parcel/APN `0038-02-5- -00021` / old parcel `0038025021`, legal description `CHURCH/CEMETERY/9.03 ACRES, GA HWY 5`, legal subdivision `PRAYS MILL BAPTIST CHURCH INC`, and 2022 market-value projection about $4.389m. Useful as a lead/counterboundary only; official qPublic/deed record is required for ownership/history. Locator: `https://www.countyoffice.org/property-record-4979-hwy-5-douglasville-ga-30135-984/`. |
| G3-S136 | Georgia Secretary of State — G3 corporate filings using `4979 Highway 5` as principal/registered/officer address | A1 / existing corporate-record family | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | **ALIAS_UNDERLYING to G3-S001**, not a property-title source. 2019/2020 corporate filings use 4979 Hwy 5 as G3’s principal/registered/officer address, but a corporate mailing/registered address does not prove G3 owned the real estate. |

## Provisional claims

| ID | Claim | State | Support / boundary |
|---|---|---|---|
| G3-C173 | The prior IRS transport blocker is closed: exact-head workflow readback directly exposes FY2024/FY2025 Schedule L and the amended FY2022 Part IX/D/M/O objects. | VERIFIED_PRIMARY | G3-S132, but count underlying authority once with canonical G3-S002/G3-S028. |
| G3-C174 | Raw FY2022 Schedule M/D establish a $590,000 donated commercial-real-estate object whose land/building values are $354,000 + $236,000, while raw FY2023 later shows materially lower L/B/E and a $416,227 notes/loans receivable balance. | VERIFIED_PRIMARY | Canonical G3-S002/G3-S028; S132 preserves exact-head readback. This establishes the balance-sheet movement, not disposition mechanics. |
| G3-C175 | `4979 Highway 5` can be safely identified as the $590,000 commercial-real-estate donation to G3. | UNVERIFIED | G3-S135 cuts against casual identification: the secondary parcel record describes a Pray’s Mill church/cemetery parcel and projects a much larger 2022 market value. Corporate use of the address at S136 is not title evidence. Obtain official assessor/deed chain before identifying the donated asset. |
| G3-C176 | The fact that G3 used 4979 Highway 5 as principal/registered address proves G3 owned the Pray’s Mill church parcel. | REFUTED | G3-S136 is an address/agency record, not a deed. G3-S135 separately describes the parcel in Pray’s Mill terms. Ownership must come from assessor/deed authority. |
| G3-C177 | Failure to retrieve the Douglas County deed-search result through the current browser proves no relevant deed exists. | REFUTED | G3-S133 confirms the official deed-search route; current follow-through fails on transport redirect. Negative transport is not negative evidence. |
| G3-C178 | The FY2023 $416,227 receivable proves the donated property was sold to a related party or at an improper price. | UNVERIFIED | The accounting movement alone does not identify debtor, transaction type, collateral, price, relationship or board approval. Deed + note/counterparty evidence is required. |

## Property-identification protocol

Do not search by narrative theory first. Reconstruct the asset from records:

1. Search official Douglas qPublic for **G3 Ministries for the Church, Inc.**, relevant officer/registered addresses, and parcels associated with the $590k donation period.
2. Search official deed index for grantee/grantor variants:
   - `G3 MINISTRIES FOR THE CHURCH INC`;
   - `G3 MINISTRIES FOR THE CHURCH`;
   - `PRAYS MILL BAPTIST CHURCH INC`;
   - any entity surfaced by assessor/deed results.
3. Date window for acquisition: at least **2021-01-01 → 2023-12-31**, widened if grantor history requires it.
4. Preserve instrument/book/page, filing date, grantor, grantee, legal description, consideration/value and parcel ID.
5. If a 2023 disposition is found, search the same parcel and parties for security deed/promissory-note-related instruments that could explain the $416,227 receivable.
6. Cross-check but do not substitute tax-assessor value for transaction consideration or IRS book value.
7. Map any identified counterparty against Part VII/board/related-party records **only after identity is primary-closed**.

## Why 4979 Highway 5 must stay behind a firewall

Several independent evidence layers currently converge at the same address for different reasons:

- G3 used 4979 Hwy 5 as corporate/principal/registered address;
- Pray’s Mill uses the same location institutionally;
- the secondary parcel surface labels the 9.03-acre church/cemetery parcel in Pray’s Mill terms;
- G3’s FY2022 raw return reports a separate accounting object: a $590,000 commercial-real-estate contribution.

Those facts do **not** make all four objects identical.

Until official assessor/deed evidence joins them, the article must not say:

> Pray’s Mill donated its church property to G3 in 2022 and G3 sold it in 2023.

The current evidence supports only:

> G3 reported receiving commercial real estate valued at $590,000 in FY2022. By FY2023 its land/building/equipment balance had fallen sharply and a $416,227 receivable appeared. The identity, transfer history and counterparty of the donated real estate remain under investigation.

## Reconciliation note

PASS16 is staging.

- S132 is an acquisition/custody alias of the IRS primary filing family; **do not count it independently** from S002/S028.
- S133/S134 are authoritative acquisition routes, not transaction proof.
- S135 is B1 discovery/counterboundary only and cannot be the sole basis for ownership or deed-history claims.
- S136 is the existing Georgia corporate-record family; corporate address ≠ title.
- C173/C174 are already reflected in canonical financial masters; future canonical reconciliation should upgrade metadata rather than multiply claim counts.
