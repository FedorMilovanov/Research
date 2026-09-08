# G3 HISTORY — evidence batch 2026-09-07 PASS9

**Status:** STAGING / PUBLICATION_HOLD  
**Purpose:** recover immutable participant-post locators for author/content-rights exits and tighten the distinction between original-object identity, preserved text, and present platform access.

## Provisional sources

| ID | Source | Class | Access | Use | Notes |
|---|---|---|---|---|---|
| G3-S091 | Dave Jenkins X post, status `2090195310098432511` | A1 | ORIGINAL_LOCATOR_VERIFIED / CONTENT_ACCESS_HOLD / TEXT_PRESERVED_BY_CONTEMPORANEOUS_PUBLICATION | title-level rights return for *The Word Matters* | Evangelical Dark Web’s Aug. 21 contemporaneous article links directly to `https://x.com/DaveJJenkins/status/2090195310098432511` and reproduces Jenkins’ statement that G3 had returned the rights to *The Word Matters* and that he would reissue it through his own publishing ecosystem. X itself is not currently retrievable by the research browser. Current Servants of Grace / Theology for Life storefront independently shows the title under Jenkins’ present publishing ecosystem. Treat the status ID as primary-object identity and the reproduced wording as preserved participant text pending authenticated capture. |
| G3-S092 | Darrell B. Harrison X reply, status `2090238102795370770` | A1 | ORIGINAL_LOCATOR_VERIFIED / CONTENT_ACCESS_HOLD / TEXT_PRESERVED_BY_CONTEMPORANEOUS_PUBLICATION | Harrison rights-return request | The same contemporaneous article links directly to `https://x.com/D_B_Harrison/status/2090238102795370770` and reproduces Harrison asking Jenkins how he obtained his rights back, saying he had two co-authored G3 books and wanted their rights returned. This proves a public request/intention once the preserved text is accepted; it does **not** prove G3 later returned Harrison’s rights. |
| G3-S093 | Justin Peters X post, status `2090502046495670536` | A1 | ORIGINAL_LOCATOR_VERIFIED / CONTENT_ACCESS_HOLD / TEXT_PRESERVED_BY_CONTEMPORANEOUS_PUBLICATION | G3+ content-removal request | Evangelical Dark Web links directly to `https://x.com/JustinPetersMin/status/2090502046495670536` and preserves Peters’ statement that he formally requested removal of his and Jim Osman’s teaching material from G3/G3+. This is a platform/content-license withdrawal request, analytically distinct from book-copyright reversion. |
| G3-S094 | Evangelical Dark Web, `Justin Peters, Darrell Harrison and Dave Jenkins All Seek To End Relationship With G3`, 2026-08-21 | C/B1 for text preservation | FULL_OBJECT_VERIFIED / EXACT_LOCATOR_VERIFIED | contemporaneous preservation / direct-link bridge | The article contains direct X links for Jenkins, Harrison and Peters and reproduces their statements. Its polemical conclusions are not inherited. The direct participant-object locators are the important forensic upgrade. Locator: `https://evangelicaldarkweb.org/2026/08/21/justin-peters-darrell-harrison-and-dave-jenkins-all-seek-to-end-relationship-with-g3/`. |
| G3-S095 | Direct `g3min.org` root request on 2026-09-07 | A2 | LIVE_HTTP_STATE_VERIFIED | current root availability | A fresh direct request again returns HTTP 503 while search/crawl surfaces still expose a richly populated pre-shutdown home page. This repeats the earlier stale-index finding and should be treated as a dated live-state check, not a new independent institutional statement. |

## Provisional claims

| ID | Claim | State | Support / boundary |
|---|---|---|---|
| G3-C118 | The original Dave Jenkins public post underlying the reported *The Word Matters* rights return is now uniquely identified as X status `2090195310098432511`. | VERIFIED_PRIMARY | G3-S091. Full original content remains access-HOLD, but direct participant-object identity is fixed. |
| G3-C119 | Jenkins publicly said G3 returned the rights to *The Word Matters*, and the title now appears under his own Theology for Life/Servants of Grace publishing surface. | CORROBORATED | G3-S091 + current Jenkins-controlled publishing surface already canonicalized at G3-S054. The legal reversion instrument/effective date/residual inventory rights remain unacquired. |
| G3-C120 | The original Darrell Harrison reply underlying the rights-request report is X status `2090238102795370770`. | VERIFIED_PRIMARY | G3-S092. |
| G3-C121 | Harrison publicly requested guidance on recovering rights to two co-authored G3 books; completion of any rights return is not established. | CORROBORATED | G3-S092 + preserved contemporaneous text. Do not convert request into completed reversion. |
| G3-C122 | The original Justin Peters G3+ removal-request post is X status `2090502046495670536`. | VERIFIED_PRIMARY | G3-S093. |
| G3-C123 | Peters publicly requested removal of his and Jim Osman’s teaching material from G3/G3+. | CORROBORATED | G3-S093 + preserved contemporaneous text. This concerns hosted/licensed teaching content, not ownership of G3 Press publishing assets. |
| G3-C124 | The continued visibility of Peters/Jenkins/Harrison material on a stale G3 surface would prove their withdrawal/reversion requests were denied. | REFUTED | Digital/storefront state can lag licensing, inventory or rights changes. Title/content disposition must be established object by object. |

## Forensic consequence

The creator-exit layer is now more granular:

- **Jenkins:** reported request has progressed to a participant statement of completed title-rights return plus observable republication under his own current publishing ecosystem.
- **Harrison:** participant request/intention is directly locatable, but completed rights return remains open.
- **Peters/Osman:** participant request to remove hosted G3+ teaching content is directly locatable; this is a content-hosting/license issue, not book copyright.

These must not be collapsed into the sentence `authors got their rights back`.

## Access guardrail

A direct X status URL fixes original-object identity even when X returns cache miss/403. It does not by itself authorize exact quotation unless the text is preserved through a reliable authenticated capture or independently verifiable participant-controlled copy. The current contemporaneous article provides text preservation, while the direct status IDs provide provenance.

## Reconciliation note

- S091 should upgrade/corroborate the rights-return reporting already paired with canonical S054; do not double-count the Jenkins statement plus the same statement reproduced by multiple blogs.
- S092 sharpens canonical C068 by fixing Harrison’s original locator while leaving completion `UNVERIFIED`.
- S093 is a genuinely separate creator/content-withdrawal object.
- S095 is a repeat measurement of the digital-state phenomenon already canonicalized at S049 and should not be counted as a separate independent source.
