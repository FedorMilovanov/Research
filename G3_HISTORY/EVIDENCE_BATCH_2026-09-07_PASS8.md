# G3 HISTORY — evidence batch 2026-09-07 PASS8

**Status:** STAGING / PUBLICATION_HOLD  
**Purpose:** tighten the IRS acquisition route, FY2024/FY2025 governance bridge, and post-wind-down G3+/Press transfer boundaries without promoting transport failures or secondary subscriber reports into proof of transaction terms.

## Provisional sources

| ID | Source | Class | Access | Use | Notes |
|---|---|---|---|---|---|
| G3-S084 | IRS, `Form 990 series downloads` | A1 | FULL_OBJECT_VERIFIED / EXACT_LOCATOR_VERIFIED | authoritative XML acquisition route | IRS states that the page provides the most recent 990-series filings in XML, organized by year/month. The 2026 section exposes `index_2026.csv` plus monthly archives `2026_TEOS_XML_01A.zip` through at least `07A.zip`. This proves the raw filing is durably available through the IRS bulk system even though the current research transport cannot retrieve the CSV/ZIP payload. Locator: `https://www.irs.gov/charities-non-profits/form-990-series-downloads`. |
| G3-S085 | ProPublica Nonprofit Explorer, FY2025 full filing object `202641339349303874` | B1 / IRS-DERIVED | FULL_FILING_MANIFEST_VERIFIED / RENDERED_SCHEDULE_CONTENT_HOLD | FY2025 filing provenance, Schedule L existence, visible Part VII bridge | ProPublica states its full-filing pages reconstruct the tax document from raw IRS XML. FY2025 visibly reports Scott Aniol (`President As Of 05/2025`), Buck Braswell (`Director`) and Matt Broome (`Secretary`) in the summary, and the filing manifest includes Schedule L. The Schedule L rendered endpoint redirects to a temporary S3 object that the current web boundary refuses to open. Locator: `https://projects.propublica.org/nonprofits/organizations/842403597/202641339349303874/full`. |
| G3-S086 | philanthropy.org, G3 Ministries for the Church FY2024 Form 990 report | B1 / IRS-DERIVED | FULL_EXTRACT_VERIFIED / EXACT_LOCATOR_VERIFIED | complete FY2024 Part VII roster and functional-expense cross-check | The parser states its figures are drawn from IRS e-file XML and displays the complete FY2024 Part VII set: Scott Aniol, Virgil Walker, Joshua Buice, Tom Buck, Chip Thornton, Buck Braswell, Adam Burrell, Matt Broome and Jonathan Frazier. It also reports 7 voting governing-body members / 6 independent and 84% program-service allocation. Locator: `https://philanthropy.org/990/report/842403597/g3-ministries-for-the-church-inc`. |
| G3-S087 | Michelle Lesley, `On the G3 Scandal…` / tag mirrors preserving G3+ subscriber-email screenshot and transfer reporting | C | SCREENSHOT_REPRODUCTION / EXACT_PAGE_VERIFIED | G3+ subscriber notice; reported G3 Press linkage | Lesley says a G3+ subscriber supplied the Aug. 27 email screenshot. Her reproduced description says G3+ was `being acquired by another ministry`; subscribers were told their subscription/library/price would carry over. She separately reports that people asking about Living Heritage were told the same still-unnamed ministry was taking over G3+ and G3 Press. She explicitly says she has no insider information identifying the transferee. This is secondary preservation of a purported subscriber communication, not the transaction agreement. Locator: `https://michellelesley.com/2026/08/27/on-the-g3-scandal/`. |
| G3-S088 | David Morrill X post, status `2093094243070029884`, surfaced in search | C | ORIGINAL_LOCATOR_VERIFIED / CONTENT_INDEXED | transfer transparency questions / rumor boundary | Search indexing preserves Morrill discussing the subscriber notice and quoting its `being acquired by another ministry` language while raising valuation/governance questions. It does not identify the acquiring ministry or prove wrongdoing. Immutable locator: `https://x.com/coconservative7/status/2093094243070029884`. |
| G3-S089 | G3 Press storefront, `shop.g3min.org` | A2 | LIVE_PUBLIC_SURFACE_VERIFIED | post-wind-down storefront state | The public storefront remains crawlable and branded `© 2026 G3 Press`, with product/collection purchase surfaces. This proves a live digital commerce surface at crawl time, not who beneficially owns inventory/IP or whether the backend is still fulfilling orders. Locator example: `https://shop.g3min.org/collections/discounted`. |
| G3-S090 | Google Play, G3+ package `com.subsplashconsulting.s_V9572P` | A2 | LIVE_PLATFORM_METADATA_VERIFIED | app capabilities and dated platform state | Current opened storefront metadata describes streaming G3 conferences, audiobooks/courses/podcasts and reading the G3 Press eBook library; the opened surface reports `Updated on Jul 23, 2026`. This remains in conflict with a separate search surface previously reporting Sep. 4, so no exact post-scandal update event may be inferred. Locator: `https://play.google.com/store/apps/details?hl=en&id=com.subsplashconsulting.s_V9572P`. |

## Provisional claims

| ID | Claim | State | Support / boundary |
|---|---|---|---|
| G3-C109 | The raw FY2025 IRS XML is not missing from the public-record system: IRS provides a 2026 index plus monthly XML ZIP archives; present failure is transport/acquisition, not evidence absence. | VERIFIED_PRIMARY_ROUTE | G3-S084 + object identity already established through G3-S085. Exact archive member still needs index/ZIP acquisition. |
| G3-C110 | ProPublica’s FY2025 full-filing page is explicitly reconstructed from raw IRS XML and visibly anchors Scott Aniol, Buck Braswell and Matt Broome in the filed Part VII summary. | CORROBORATED / IRS_DERIVED | G3-S085. This does not establish that these were the only officers/directors in FY2025. |
| G3-C111 | FY2024 Part VII can now be reconstructed as nine reported officers/directors/key employees: Aniol, Walker, Buice, Buck, Thornton, Braswell, Burrell, Broome and Frazier. | CORROBORATED / IRS_DERIVED | G3-S086. Distinguish the nine Part VII persons from the filing’s 7 voting governing-body members; not every Part VII person must be a voting director at year-end. |
| G3-C112 | The FY2024→FY2025 filing bridge proves a governance transition but does not by itself prove when or why Tom Buck, Chip Thornton, Adam Burrell, Jonathan Frazier or others left the board. | INFERENCE_STRONGLY_SUPPORTED | G3-S085 + G3-S086. Full FY2025 Part VII and dated board pages/minutes remain required for departure chronology. |
| G3-C113 | A reproduced Aug. 27 G3+ subscriber email says G3+ was being acquired by an unnamed `another ministry` and that subscriber continuity would be preserved. | PARTIALLY_VERIFIED / PRIMARY_EMAIL_HOLD | G3-S087 + G3-S088 preserve materially consistent language. Obtain original email with headers/screenshot provenance before quote-safe primary status. |
| G3-C114 | The same unnamed ministry was acquiring both G3+ and G3 Press. | PARTIALLY_VERIFIED / TRANSACTION_OBJECT_HOLD | G3-S087 reports this based on private admin/customer communications, while the known subscriber notice directly concerns G3+. No asset-transfer agreement, board resolution or transferee announcement has been acquired. |
| G3-C115 | Right Response Ministries is the G3+/Press transferee. | UNVERIFIED / RUMOR_ONLY | Search results preserve speculation framed as a question. No primary recipient statement, G3 announcement or transaction document currently identifies Right Response. |
| G3-C116 | A live G3 Press storefront and continuing G3+ app-store metadata after the announced wind-down prove that G3 Ministries retained beneficial ownership of those assets. | REFUTED_AS_UNSUPPORTED | G3-S089 + G3-S090 prove only live/stale platform state. Digital surfaces can persist during or after a transfer, shutdown, migration or wind-down. |
| G3-C117 | Failure to retrieve a current Georgia dissolution filing proves `G3 Ministries for the Church, Inc.` remains legally active. | REFUTED_AS_UNSUPPORTED | The Georgia incorporation/articles are primary, but no current entity-status object or post-August filing has yet been acquired. Search failure is not legal-status evidence. |

## Governance bridge — what changed and what remains unknown

The FY2024 filing is now stronger than the earlier three-name summaries because the IRS-derived parser exposes all nine Part VII persons. This gives a concrete pre-Buice-crisis baseline.

What it **does not** do is convert the FY2025 ProPublica three-name preview into a complete FY2025 board. `+ View more people` is an explicit warning that more Part VII rows may exist. Therefore:

- do not say `the FY2025 board consisted only of Aniol, Braswell and Broome`;
- do say those three are directly visible in the filed FY2025 summary;
- keep the alleged late-2026 six-person board `Braswell / Broome / Norton / Sikes / Joyner / Mooney` at `ARCHIVE_HOLD` until an official archived G3 board page is captured.

## IRS raw-acquisition route — narrowed again

The official IRS page confirms a deterministic route:

1. acquire `index_2026.csv`;
2. find object `202641339349303874` and its archive member/month;
3. acquire the corresponding `2026_TEOS_XML_XX.zip`;
4. extract the exact XML file;
5. parse `IRS990ScheduleL` and full `IRS990` Part VII/IX/O objects;
6. retain checksum + source URL + archive member as custody metadata.

Current browser can read the IRS HTML index page but rejects CSV/binary payloads; container DNS likewise cannot resolve the IRS host. This is a **tool-bound acquisition failure**, not a substantive evidence result.

## Asset-transfer boundary — stronger, still P0

The best current formulation is now:

> G3 told G3+ subscribers that the platform was being acquired by another ministry and represented that subscriptions/libraries/pricing would transition. Secondary reporting further says the same unnamed ministry was expected to take over G3 Press. The acquiring ministry, consideration, valuation, asset list, board approval, conflicts/recusals and legal completion remain unverified.

Do not write:

- `G3 sold G3+ to Right Response`;
- `G3 donated all assets to friends`;
- `the transfer was corrupt`;
- `the live storefront proves no transfer occurred`.

None of those claims currently clears the evidence threshold.

## Next acquisition targets created by PASS8

1. Original Aug. 27 G3+ subscriber email with headers or authenticated full-resolution capture.
2. IRS `index_2026.csv` row for object `202641339349303874`, then exact monthly ZIP/XML extraction.
3. Same workflow for FY2024 object `202541359349304489` and FY2023 object `202411429349300611`.
4. Complete FY2025 Part VII rows from raw XML.
5. Official archived G3 board page(s) between Jul. 2025 and Aug. 2026.
6. Current Georgia Secretary of State entity-status result plus any 2026 dissolution filing.
7. Recipient-ministry announcement / transfer agreement / board resolution for G3+ and G3 Press.
8. Original author-rights statements from Dave Jenkins and Darrell Harrison and title-level disposition evidence.

## Duplicate-count guardrail

- G3-S085 is another access surface for the same IRS FY2025 filing already represented in the canonical finance source family; reconcile as an access/provenance upgrade, not an independent witness.
- G3-S086 is an IRS-derived parser, not independent evidence against the underlying IRS filing.
- G3-S087 and G3-S088 appear to preserve/refer to the same G3+ subscriber communication and must not be counted as two independent confirmations of transaction terms.
