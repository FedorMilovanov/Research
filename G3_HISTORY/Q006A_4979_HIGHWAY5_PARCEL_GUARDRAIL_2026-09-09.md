# Q006A — 4979 Highway 5 parcel guardrail, 2026-09-09

**Status:** DISCOVERY-LEVEL PARCEL LOCATOR / IDENTITY CONFLATION BLOCKED / TITLE+NOTE HOLD / PUBLICATION_HOLD

## 1. Problem

G3 repeatedly reports `4979 Highway 5, Douglasville, GA 30135` as its principal/mailing address. Because the FY2022 Form 990 also reports a $590,000 commercial-real-estate donation later sold in FY2023, it is easy to make an unsupported shortcut:

`G3 principal address = donated $590k real-estate asset`.

Current public parcel discovery strongly cautions against that shortcut.

## 2. Public assessor-derived locator

Multiple public property renderers tied to county-record data identify the 4979 Highway 5 parcel as:

- APN / parcel `00380250021` (formatted by one renderer as `0038-02-5- -00021`);
- approximately 9.03 acres;
- legal description `CHURCH/CEMETERY/9.03 ACRES, GA HWY 5`;
- one renderer exposes legal subdivision `PRAYS MILL BAPTIST CHURCH INC`;
- assessor-derived tax assessment/market-value fields are in the multi-million-dollar range, materially different from the $590,000 G3 donated-real-estate accounting object.

Relevant discovery surfaces include:

- `https://www.countyoffice.org/property-record-4979-hwy-5-douglasville-ga-30135-984/`;
- `https://www.zillow.com/homedetails/4979-Highway-5-Douglasville-GA-30135/248072363_zpid/`;
- `https://www.redfin.com/GA/Douglasville/4979-GA-5-30135/home/39594889`.

These are **secondary renderers of assessor/public-record data**, not title instruments. Their overlapping fields may derive from the same underlying county record and must not be counted as independent title corroboration.

## 3. Evidentiary consequence

The 4979 address is a valid G3 principal/mailing address and a valid parcel locator for the Pray's Mill campus area. It is **not** presently a valid identification of the FY2022 $590,000 donated commercial-real-estate object.

Controlled state:

`4979_HIGHWAY5 = PRINCIPAL_ADDRESS + DISCOVERY_PARCEL_LOCATOR`.

`4979_HIGHWAY5 == FY2022_DONATED_REAL_ESTATE = UNVERIFIED / DO_NOT_INFER`.

The difference between the assessor-derived campus valuation/description and the $590,000 donated asset further weakens casual conflation, but does not independently prove the donated asset was elsewhere because accounting basis/valuation and parcel-tax valuation are different concepts.

## 4. What remains required

Q006A still needs a title-level link:

1. deed/legal description for the donated asset;
2. grantor/donor identity;
3. grantee/recipient identity at donation;
4. FY2023 purchaser/grantee;
5. sale consideration/cash-at-closing;
6. security deed/note instrument if seller financing occurred;
7. explicit linkage between that note and the Form 990 receivable.

Current public qPublic/GSCCCA access barriers remain controls; no login, payment or access restriction was bypassed.

## 5. Publication rule

Do not write that G3 was donated, owned or sold the Pray's Mill 4979 Highway 5 campus merely because the same address appears on G3 filings.

Until a title instrument links the $590,000 accounting object to a parcel, property identity remains `UNVERIFIED`.

`PUBLICATION_HOLD = true`.