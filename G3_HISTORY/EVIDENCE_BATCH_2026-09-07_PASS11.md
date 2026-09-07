# G3 HISTORY — evidence batch 2026-09-07 PASS11

**Status:** STAGING / PUBLICATION_HOLD  
**Purpose:** close two interpretive dead ends: (1) the unsupported claim that Michael O'Fallon was proven to have been forced off the G3 board in June 2023, and (2) the idea that the documented ProPublica v2 API can substitute for raw e-file XML when Schedule L / full Part IX detail is required.

## Provisional sources

| ID | Source | Class | Access | Use | Notes |
|---|---|---|---|---|---|
| G3-S099 | Michael O'Fallon Twitter/X post, status `1673411411513425920`, 2023-06-26 | A1 | ORIGINAL_LOCATOR_VERIFIED / CONTENT_PRESERVED_BY_CONTEMPORANEOUS_PUBLICATIONS | June 2023 board departure / stated reason | Evangelical Dark Web's contemporaneous update links directly to `https://twitter.com/SovMichael/status/1673411411513425920` and reproduces O'Fallon's first-person statement that the previous week he submitted resignations to the Conservative Baptist Network, G3 Ministries and Alpha and Omega Ministries. He says the reason was to prevent those ministries from having to answer continuing allegations tied to his Sovereign Nations work. Direct tweet body is not currently returned by the research browser, but immutable object identity is fixed and the text was preserved contemporaneously. |
| G3-S100 | Baptist News Global, `O'Fallon quits CBN, G3 and Alpha and Omega`, 2023-06-27 | B1 | FULL_OBJECT_VERIFIED / EXACT_LOCATOR_VERIFIED | independent preservation of participant resignation statement | BNG independently reports O'Fallon's June 26 statement and reproduces his description that he resigned the G3 board position and other roles. It also reports his stated rationale. This supports the participant-account layer without establishing whether private pressure or board discussions preceded his resignation. Locator: `https://baptistnews.com/article/ofallon-quits-cbn-g3-and-alpha-and-omega/`. |
| G3-S101 | Evangelical Dark Web, `Michael O'Fallon Removed From G3 Ministries Board`, 2023-06-26 | C | FULL_OBJECT_VERIFIED / EXACT_LOCATOR_VERIFIED / DIRECT_PARTICIPANT_LINK | archive-change discovery / competing interpretation | Before its update, the article inferred removal because O'Fallon disappeared from G3's board page and says Wayback had shown him listed June 10, with Jeff Pate and Jonathan Frazier appearing after the change. After publication it updated the story with O'Fallon's direct resignation statement. Its earlier `removed` interpretation and later skepticism about voluntariness are not facts established by the page change. Locator: `https://evangelicaldarkweb.org/2023/06/26/michael-ofallon-removed-from-g3-ministries-board/`. |
| G3-S102 | ProPublica Nonprofit Explorer API v2 documentation | A2 | FULL_OBJECT_VERIFIED / EXACT_LOCATOR_VERIFIED | API capability boundary / IRS-data provenance | ProPublica documents `GET /organizations/:ein.json` as returning organization data plus filing objects with extracted 40–120 data fields depending on form type, and documents `pdf_url` where available. The same documentation distinguishes this API/summary data from complete Form 990 XML documents, which contain full filing data including officers and tax schedules. Therefore the public v2 API is not documented as a Schedule-L-object endpoint. Locator: `https://projects.propublica.org/nonprofits/api/`. |

## Provisional claims

| ID | Claim | State | Support / boundary |
|---|---|---|---|
| G3-C130 | Michael O'Fallon publicly stated on June 26, 2023 that he had submitted his resignation from the G3 board (along with roles at CBN and Alpha and Omega) the previous week. | CORROBORATED | G3-S099 + G3-S100. Primary tweet locator is fixed; contemporaneous independent publication preserves the statement. |
| G3-C131 | It is established that G3 forcibly removed O'Fallon from the board because of the Christian Nationalism dispute. | REFUTED_AS_UNSUPPORTED | G3-S099–S101. A contemporaneous page-change report initially inferred removal, but O'Fallon's own public account says he resigned. Private pressure or disagreement remains possible but is not proven by the current record. |
| G3-C132 | O'Fallon's departure had no relationship at all to the 2023 political-theology conflict around G3. | UNVERIFIED | His stated reason explicitly concerned continuing allegations tied to his work and the burden on affiliated ministries, but the exact private board deliberations and causal mix remain unacquired. Avoid both forced-removal and no-relationship absolutes. |
| G3-C133 | The June 2023 board-page change is useful evidence for board chronology even though it cannot by itself determine whether the departure was voluntary or compelled. | CORROBORATED | G3-S101 + participant account. Board-page state and resignation mechanics are separate questions. |
| G3-C134 | ProPublica's documented v2 organization API provides a direct complete-Schedule-L XML endpoint sufficient to close Q001. | REFUTED | G3-S102. The API documents extracted filing fields and PDF links; ProPublica separately describes complete XML Form 990 documents as the full schedule-bearing data layer. |
| G3-C135 | For exact Schedule L / full Part IX closure, the authoritative acquisition target remains the raw IRS e-file XML (or an exact faithful rendering of that same XML), not the ProPublica summary API. | CORROBORATED | G3-S102 + existing canonical IRS bulk-route evidence. This is an acquisition-method finding, not a substantive finding about the transactions. |

## O'Fallon — article-safe reconstruction today

Safe:

> G3's public board roster changed in June 2023 during a heated dispute over Christian Nationalism and allied political-theology questions. A contemporary report initially interpreted Michael O'Fallon's disappearance from the roster as removal. O'Fallon then publicly said that he himself had submitted resignations from G3 and two other ministries the previous week, explaining that he did not want those organizations continually burdened by controversies attached to his work. The current public record therefore establishes his resignation and the timing of the board change, but not whether private pressure, board disagreement or the broader controversy also contributed.

Not safe:

> G3 fired O'Fallon for being too sympathetic to Christian Nationalism.

Also not safe:

> The Christian Nationalism dispute had nothing to do with his departure.

The first exceeds the participant account; the second exceeds the available causal evidence.

## Financial acquisition consequence

Do not spend additional research cycles trying to infer Schedule L rows from the documented ProPublica v2 API field set. Use that API for summary/extract checks only. Q001/Q002 closure still requires:

1. IRS annual index / monthly archive acquisition for the exact object IDs;
2. extraction of the exact e-file XML;
3. direct parsing of `IRS990ScheduleL`, `IRS990` Part IX/Part VII and Schedule O as applicable;
4. custody metadata/checksum for the extracted source object.

## Reconciliation note

- G3-S099 is a new original participant-object locator and should be retained canonically.
- G3-S100 is a distinct independent publication preserving the participant account.
- G3-S101 is useful for board-page/archive chronology but its `removed` framing must not be inherited.
- G3-S102 is a methodology/acquisition source; it should supplement, not replace, the canonical IRS source family.
