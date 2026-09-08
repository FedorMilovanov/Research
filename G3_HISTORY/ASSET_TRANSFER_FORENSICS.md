# G3 asset-transfer forensics — G3+, G3 Press and post-wind-down digital state

**Status:** ACTIVE / PUBLICATION_HOLD  
**Cutoff:** 2026-09-08  
**Question:** what can currently be proved about the reported transfer or continuation of G3+, G3 Press, subscriber relationships, publishing rights and related digital assets after G3 announced its operational wind-down?

This file is the canonical working dossier for Q006. Staging acquisition passes remain custody/history records and must not be counted as independent evidence.

## 1. What is actually reported

Current public reporting preserves a subscriber-facing statement that G3+ was expected to be acquired or transitioned to **another ministry**. Secondary reporting also says G3 Press may be part of the same transition.

No primary object acquired as of the cutoff:

- names the acquiring ministry;
- supplies an asset-purchase or assignment agreement;
- states consideration;
- gives a closing date;
- provides a board approval/recusal record;
- identifies which subscriber contracts, domains, platform accounts, trademarks, copyrights, inventory or publishing agreements transferred.

Therefore the statement **“G3+ and G3 Press were acquired by [named ministry]” remains unverified**.

## 2. Current live-state observations

### Main G3 site

Direct `https://g3min.org/` returned HTTP **503 Service Unavailable** on controlled observations Sep. 7 and Sep. 8, 2026.

Older search/crawl surfaces still expose pre-shutdown pages and navigation. That is stale/indexed state, not evidence that ordinary G3 operations resumed.

### G3 Press

Direct `https://shop.g3min.org/` remained reachable on Sep. 8, 2026 and rendered an active commerce surface with:

- cart and checkout controls;
- United States / Canada currency selection;
- a principal catalog view showing 143 products;
- G3 Press books and G3-branded products;
- links to G3 Ministries and G3 Plus;
- footer identity `© 2026 G3 Press`.

**What this proves:** a dated storefront/commerce surface remained live.

**What it does not prove:** merchant beneficial ownership, payment beneficiary, inventory title, publishing-right ownership, actual fulfillment status or legal transfer completion.

### G3+

Direct `https://plus.g3min.org/` remained reachable as the G3 Plus web application shell on Sep. 8, 2026.

The reachable Privacy Policy and Terms of Service still identify G3 / G3 Plus and direct users to `admin@g3min.org`, but both legal texts are dated **2025-04-03**. Their continued availability is continuity metadata, not a 2026 certificate of beneficial ownership.

## 3. App-store seller/developer identity

### Apple iOS/iPad

The current G3+ listing, app ID `1192776791`, continues to identify:

`G3 Ministries For The Church, Inc.`

as developer/provider.

### Apple TV

A separate G3 Plus tvOS listing, app ID `6761784816`, identifies:

- seller: `G3 Ministries For The Church, Inc.`;
- copyright: `© 2026 G3 Ministries`;
- subscriber destination: `plus.g3min.org`.

### Google Play

The current G3+ listing, package `com.subsplashconsulting.s_V9572P`, continues to expose G3 developer/support identity, including:

- G3 Ministries naming on the listing surfaces;
- `admin@g3min.org` support email;
- `4979 Highway 5, Douglasville, GA 30135` developer address.

The direct listing observed Sep. 8 displays `Updated on Jul 23, 2026`. Earlier indexed/crawl surfaces showed a conflicting Sep. 4 date. Preserve the conflict; the current direct surface favors Jul. 23 for the presently displayed field.

### Evidentiary boundary

Apple/Google seller/developer metadata is useful **platform-account state**. It cannot by itself establish or refute a private asset closing. Account migration may lag legal closing, remain temporarily under a transferor, or be technically delegated without changing beneficial ownership.

Therefore:

> `App stores still say G3, so no transfer occurred.`

is an invalid inference.

## 4. Living Heritage — separation is primary-verified; 2026 transferee identity is not

A controlled exact-head acquisition of the official FY2025 IRS e-file object materially upgrades one narrow point.

Raw object:

- IRS object `202641339349303874`;
- source member `202641339349303874_public.xml`;
- raw XML SHA-256 `48846b93808c2ffcacac6dc1995fb7890a630ccef9f711fa8a27cd4445541ac2`.

Exact-head workflow run `34233453690` on Research head `1f75d2b831666128ccff025fc9f5a93c8a6dfd53` searched all **401** Form 990 leaves for `Living`, `Heritage`, `Homeschool` and `separat`. It returned exactly **one** matching leaf:

`IRS990/Desc`.

That filed narrative states that during 2025 G3 separated **Living Heritage Homeschool as an independent entity from G3 Ministries**. The same narrative also describes 2025 G3 Press publishing, continued G3 Plus operation, leadership transition and other program changes.

### What is now VERIFIED_PRIMARY

- G3's FY2025 filed narrative says Living Heritage Homeschool was separated as an independent entity from G3 Ministries during 2025.
- Cause IQ's similar wording is therefore a derivative rendering/cross-check of the filing, not a new independent evidence family.

### What remains UNVERIFIED

Living Heritage currently offers access in which Premium membership includes G3+ access/content. That later commercial/access continuity does **not** establish that Living Heritage subsequently acquired:

- G3+ as an asset;
- G3 Press;
- G3 subscriber contracts;
- G3 domains;
- G3 app-store accounts;
- G3 trademarks;
- G3 Press inventory;
- author publishing rights;
- G3 corporate liabilities.

The 2025 separation fact and the 2026 G3+ bundling are compatible with multiple legal/technical arrangements. They cannot be collapsed into the proposition `Living Heritage = the unnamed successor ministry`.

Until a recipient-side primary object names the acquisition or the platform/merchant legal identity changes to a named successor, `Living Heritage acquired G3+` remains a hypothesis rather than a finding.

## 5. G3 Press author-rights are not one monolithic asset

Title-level evidence already shows that rights/inventory questions can diverge by author and book.

For example, current Dave Jenkins / Servants of Grace / Theology for Life surfaces support post-G3 availability of *The Word Matters*, while public statements by other authors may establish only a request or intention to recover rights.

Do not convert one author’s completed or apparent title-level transition into a claim that the entire G3 Press catalog transferred or reverted in the same way.

The required reconstruction is title-by-title where the evidence permits it:

- copyright/contract rights;
- publishing license;
- digital files;
- ISBN/imprint status;
- physical inventory;
- storefront listing;
- fulfillment/distribution;
- completed reversion or assignment instrument.

## 6. Corporate-status boundary

Georgia Secretary of State records acquired Sep. 8, 2026 still list `G3 Ministries for the Church, Inc.` as **Active/Compliance**.

That status can coexist with announced operational wind-down and with asset transfer/liquidation activity. It does not prove G3 continues ordinary ministry operations, and it does not identify a transferee.

Likewise, a live store, live streaming application and active corporate registration can coexist during:

- wind-down;
- inventory liquidation;
- platform migration;
- staged asset assignment;
- servicing of existing subscribers;
- delayed app-store/account transfer.

## 7. Current claim matrix

| Claim | State | Why |
|---|---|---|
| G3 publicly/through subscriber communication contemplated transition of G3+ to another ministry | **PARTIALLY_VERIFIED / reported** | subscriber-reporting family; primary named recipient absent |
| A specific named ministry has been proved to be the G3+ transferee | **UNVERIFIED** | no primary recipient/transaction object |
| G3 Press definitely transferred with G3+ | **UNVERIFIED** | secondary reporting only; no agreement/recipient announcement |
| FY2025 G3 filing says Living Heritage Homeschool was separated as an independent entity from G3 | **VERIFIED_PRIMARY** | raw FY2025 `IRS990/Desc`, exact IRS object/SHA acquired |
| Living Heritage acquired G3+ in the 2026 wind-down | **UNVERIFIED** | 2025 separation + later access bundling are not assignment/title evidence |
| App-store seller identity remained G3 on Sep. 8 | **VERIFIED_PRIMARY as platform state** | Apple/Google current listings |
| G3 Press storefront remained live on Sep. 8 | **VERIFIED_PRIMARY as website state** | direct storefront observation |
| G3+ web app remained reachable on Sep. 8 | **VERIFIED_PRIMARY as website state** | direct web-app observation |
| Continued G3 seller metadata proves no transfer occurred | **REFUTED inference** | platform metadata can lag or remain delegated |
| Live G3+/Press surfaces prove G3 reversed its shutdown | **REFUTED inference** | live subservices can coexist with operational wind-down |

## 8. Proof gates that can materially close Q006

Do not spend further cycles merely repeating current app-store/storefront observations unless the state changes.

The next useful evidence must be one or more of:

1. a successor ministry’s primary announcement explicitly naming the acquisition;
2. a G3 board/subscriber communication explicitly naming the recipient;
3. a post-transfer Terms/Privacy/merchant record naming a different legal provider;
4. an Apple/Google seller/developer-account change naming a new legal entity;
5. domain, tenant or platform-account assignment evidence tied to a named entity;
6. asset-purchase, assignment or assumption agreement;
7. public corporate filing identifying the transfer or recipient;
8. title-level publishing-right assignments/reversions sufficient to reconstruct G3 Press disposition;
9. merchant/payment/fulfillment legal identity where publicly exposed and lawfully accessible.

Until one of those gates closes, the article-safe statement is:

> G3 announced an operational wind-down while G3+ and G3 Press remained publicly reachable. G3's FY2025 tax filing separately states that Living Heritage Homeschool had been separated as an independent entity during 2025. Reporting later indicated that another ministry was expected to take over G3+ and possibly G3 Press, but the acquiring ministry and transaction terms had not been established by a primary public record as of Sep. 8, 2026. Current Living Heritage bundling and app-store seller metadata document service/platform state; neither establishes the 2026 transferee by itself.

## 9. Evidence-family reconciliation

This dossier reconciles, rather than duplicates, the existing canonical families:

- `G3-S002` — raw IRS filing family, now including the FY2025 Living Heritage separation narrative;
- `G3-S019` — transfer discovery/subscriber-reporting family;
- `G3-S032` / `G3-S050` — Google Play platform identity family;
- `G3-S033` — Apple platform identity family;
- `G3-S049` — direct-root vs stale-index state;
- `G3-S053` — G3 Press storefront family;
- `G3-C030` — named-successor claim;
- `G3-C056`–`G3-C060` — platform/live-state guardrails.

Cause IQ's Living Heritage wording is derivative of the FY2025 filing and must not be counted as independent corroboration of the same separation fact.

`EVIDENCE_BATCH_2026-09-08_PASS18.md` remains a dated acquisition/reconciliation record; this file is the canonical analytical surface for Q006.
