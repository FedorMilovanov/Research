# G3 HISTORY — evidence batch 2026-09-08 PASS17

**Status:** STAGING / PUBLICATION_HOLD  
**Purpose:** close the FY2023 donated-real-estate disposition at raw-filing level, trace the resulting/adjacent notes-receivable balance through FY2025, and document the exhausted public archive/deed routes without inventing continuity or counterparty identity.

## Provisional sources

| ID | Source | Class | Access | Locator | Rights | Publication | Use / boundary |
|---|---|---|---|---|---|---|---|
| G3-S137 | Official IRS TEOS FY2023 raw XML, object `202411429349300611`, exact-head asset readback run `34220049227` | A1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Raw Form 990 reports `GrossAmountSalesAssetsGrp/OtherAmt=550000`, `LessCostOthBasisSalesExpnssGrp/OtherAmt=590000`, `GainOrLossGrp/OtherAmt=-40000`, beginning L/B/E $621,915, ending L/B/E $16,777 and `OthNotesLoansReceivableNetGrp/EOYAmt=416227`. Raw XML SHA-256 `c8eb0baa2265eadef2b6798c68868f91f8fde6ca9fbffe40e138877df92ce5c0`. This is an access/readback upgrade of the canonical FY2023 IRS object family, not an independent witness. |
| G3-S138 | Official IRS TEOS FY2024 raw XML, object `202541359349304489`, receivable-trace run `34220835523` | A1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Raw balance sheet carries `OthNotesLoansReceivableNetGrp` from BOY **$416,227** to EOY **$251,197**; non-interest-bearing cash rises $783,534 → $830,774; investment income reported **$22,683**. Raw XML SHA-256 `c14f511cf66051b916748440594586b4db1ecdb0d07ab14ef05e01e92524aca3`. Same underlying FY2024 filing already used for Schedule L; do not double-count. |
| G3-S139 | Official IRS TEOS FY2025 raw XML, object `202641339349303874`, receivable-trace run `34220835523` | A1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Raw balance sheet carries `OthNotesLoansReceivableNetGrp` from BOY **$251,197** to EOY **$153,000**; non-interest-bearing cash falls $830,774 → $228,435; investment income reported **$15,375**. Raw XML SHA-256 `48846b93808c2ffcacac6dc1995fb7890a630ccef9f711fa8a27cd4445541ac2`. Same underlying FY2025 filing already used for Schedule L; do not double-count. |
| G3-S140 | Internet Archive CDX + official G3 `Who We Are` path continuity acquisition, exact-head run `34219682146` | A2 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Corrected CDX query removed digest collapse and searched `g3min.org/about/who-we-are/` from 2026-07-21 through 2026-08-31. It returned exactly **one** capture, timestamp `20260721102641`, digest `2MX4NSFWIZ6RS5N2CO6SH5OZUM6AHKW2`; decoded snapshot contains all six board names. This proves archive-search exhaustion for that path/window, **not** roster continuity through late August. |
| G3-S141 | GSCCCA Real Estate public Name Search + Douglas County/Georgia DOR acquisition lane, runs `34218769001`, later schema/public-query runs through exact-head v2 | A1/A2 authority/access record | PARTIAL_OBJECT / ACCESS_GATE_VERIFIED | EXACT_ROUTE_VERIFIED | REFERENCE | Douglas County and Georgia DOR authority pages are reachable; qPublic is Cloudflare 403. GSCCCA public Real Estate Name Search form exposes real Douglas parameters (`intCountyID=48`, grantor/grantee/all-party and date fields), but unauthenticated POSTs for G3/Pray's Mill names return an automatic `frmLogin` interstitial instead of deed rows. No login, subscription, payment, premium search, document purchase or bypass was attempted. This is an access-boundary source, not deed evidence. |

## Provisional claims

| ID | Claim | State | Support / boundary |
|---|---|---|---|
| G3-C179 | The FY2023 raw filing reports an `Other` asset sale with **$550,000 gross proceeds**, **$590,000 basis** and a **$40,000 loss**. | VERIFIED_PRIMARY | G3-S137. The derivative `Sales of Assets −$40,000` label is the net loss, not the gross sale price. |
| G3-C180 | The filing sequence identifies that $590,000-basis FY2023 sale as the disposition of the single $590,000 commercial-real-estate contribution recorded in FY2022. | VERIFIED_PRIMARY_AS_FILING_RECONSTRUCTION | FY2022 Schedule M/D: one $590k commercial-real-estate contribution = $354k land + $236k buildings. FY2023: exact $590k asset-sale basis, land/building balance disappears and only equipment remains. This closes accounting-object identity; parcel/deed identity remains open. |
| G3-C181 | A notes/loans receivable appears at **$416,227** at FY2023 year end and is then carried down to **$251,197** at FY2024 year end and **$153,000** at FY2025 year end. | VERIFIED_PRIMARY | G3-S137–S139. Principal-like balance reductions are $165,030 in FY2024 and $98,197 in FY2025. |
| G3-C182 | The declining receivable proves the $550,000 property sale used seller financing. | PARTIALLY_VERIFIED / LINKAGE_HOLD | Timing, continuous BOY/EOY carry-forward, decreasing balances and later investment income make seller financing materially more plausible, but no acquired filing field names the debtor or explicitly links the note to the property sale. Deed/note/security instrument required before promotion. |
| G3-C183 | FY2024 investment income **$22,683** and FY2025 investment income **$15,375** are definitively interest paid on the property note. | UNVERIFIED | Same filings and timing are suggestive, but `InvestmentIncomeGrp` does not identify payer/source. Do not call these note-interest payments without a note, amortization schedule or explicit filing explanation. |
| G3-C184 | The exact official G3 `Who We Are` Wayback path has no capture after July 21 and through Aug. 31, 2026 in the corrected CDX query. | VERIFIED_PRIMARY_AS_ARCHIVE_STATE | G3-S140. This is a statement about the Internet Archive index for that path/window, not about whether G3's board changed. |
| G3-C185 | Because Wayback has no later snapshot, the July 21 six-person board definitely remained unchanged through the late-August crisis. | REFUTED_AS_INFERENCE | G3-S140. Absence of capture is not continuity evidence; another dated primary object is required. |
| G3-C186 | Public unauthenticated online deed search has already revealed the G3 property purchaser or parcel. | REFUTED | G3-S141. qPublic is blocked and GSCCCA result access routes to login; no deed row was acquired. |

## Receivable trace

| Filing | BOY other notes/loans receivable | EOY other notes/loans receivable | Change | Investment income |
|---|---:|---:|---:|---:|
| FY2023 | $0 / no prior carried balance in reconstructed sequence | **$416,227** | **+$416,227** | $0 |
| FY2024 | **$416,227** | **$251,197** | **−$165,030** | **$22,683** |
| FY2025 | **$251,197** | **$153,000** | **−$98,197** | **$15,375** |

The carry-forward identity is exact: FY2023 EOY = FY2024 BOY; FY2024 EOY = FY2025 BOY.

This materially strengthens the interpretation that the $416,227 amount is a continuing note/loan receivable rather than a transient parser artifact. It still does not establish the debtor or transaction origin.

## Current property hypothesis ladder

1. **VERIFIED_PRIMARY:** FY2022 contains one donated commercial-real-estate accounting object at $590,000.
2. **VERIFIED_PRIMARY:** FY2023 reports a sale of an `Other` asset for $550,000 against $590,000 basis, producing a $40,000 loss.
3. **VERIFIED_PRIMARY_AS_FILING_RECONSTRUCTION:** the sale is the disposition of that FY2022 $590,000 donated real-estate accounting object.
4. **VERIFIED_PRIMARY:** a $416,227 other notes/loans receivable appears at FY2023 EOY and declines to $251,197 and $153,000 over the next two filings.
5. **PLAUSIBLE / NOT CLOSED:** that receivable is seller financing from the property purchaser.
6. **UNVERIFIED:** FY2024/FY2025 investment income is interest on that same note.
7. **UNRESOLVED:** parcel, donor, purchaser, cash-at-closing, note/security terms, board approval/conflicts.

## Acquisition boundary

Do not repeat the same blocked routes as if they were new evidence:

- qPublic in current research runtime: Cloudflare 403;
- GSCCCA Name Search: public form/schema reachable, result POST routes to login;
- no subscription/account/payment authorization exists;
- no registry access failure may be turned into a negative deed finding;
- `4979 Highway 5` is a corporate/principal address and a Pray's Mill parcel lead, but address overlap is not title evidence and does not identify the $590,000 property.

The next legitimate closure requires a deed/title or note/security object from an accessible official record, a user-authorized subscription source, or a directly supplied primary document. No access control should be bypassed.

## Reconciliation note

PASS17 is staging, but its raw IRS findings should be promoted into the canonical financial/open-question/claims layers. G3-S137–S139 are access/readback upgrades of existing IRS filing objects, not new independent corroborating witnesses. G3-S140 is the archive-state closure object. G3-S141 records the government/search access boundary only.
