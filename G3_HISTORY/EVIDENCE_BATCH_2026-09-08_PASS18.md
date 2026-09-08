# G3 HISTORY — evidence batch 2026-09-08 PASS18

**Status:** STAGING / PUBLICATION_HOLD  
**Purpose:** preserve a dated post-wind-down observation of G3+ / G3 Press public platform state, test whether current seller/developer/merchant-facing surfaces reveal a successor ministry, and prevent stale/live-state confusion from being turned into an ownership conclusion.

## Repository checkpoint

PASS18 begins from exact Research head:

`64dfcc29cef627dc1e7c6c0322d954a25c770b3b`

At that head PR #188 is Draft, mergeable, based on `b5785be744bc8eac14491b972bb99005f1e81322`, with 115 commits / 72 changed files / 10,250 additions / 0 deletions. All currently triggered exact-head PR workflows were terminal-green.

`PUBLICATION_HOLD=true` remains unchanged.

## Existing canonical source families reused

This pass does **not** multiply existing platform/store surfaces into fictitious independent witnesses.

- `G3-S032` — Google Play G3+ listing.
- `G3-S033` — Apple App Store G3+ / G3 Plus listings.
- `G3-S049` — direct `g3min.org` root live-state vs retained crawled/indexed pages.
- `G3-S050` — Google Play developer/support metadata; same underlying Google Play family as S032 for ownership-state purposes.
- `G3-S053` — G3 Press official commerce storefront.
- `G3-S019` — Michelle Lesley / subscriber-email discovery family for the reported unnamed successor ministry.

The observations below refresh those families rather than creating a second evidence system.

## Controlled observations on 2026-09-08

### 1. G3 main root remains unavailable live

Direct fetch of:

`https://g3min.org/`

returned **HTTP 503 Service Unavailable** on 2026-09-08.

Search/crawl indexes still expose older G3 pages, including pre-shutdown navigation and an already-cancelled 2027 conference. Those indexed pages remain stale-state evidence and must not be read as proof that G3 resumed ordinary operations.

This reconfirms the `live HTTP != search index != archived page` firewall already recorded at S049 / C059 / C060.

### 2. G3 Press storefront is live as a commerce surface

Direct fetch of:

`https://shop.g3min.org/`

succeeded on 2026-09-08.

The rendered storefront currently exposes:

- a cart and `Check out` control;
- United States / Canada currency selection;
- live product navigation;
- **143 products** in the principal catalog view;
- G3 Press / G3 Ministries merchandise and books;
- links back to G3 Ministries and G3 Plus;
- footer identity `© 2026 G3 Press`.

This upgrades the earlier 2026-09-07 observation at S053 from mere indexed/storefront visibility to a fresh direct-live commerce-surface observation.

**Boundary:** a functioning Shopify/storefront surface does not reveal merchant beneficial ownership, bank/payments beneficiary, inventory title, publishing rights, transaction closing, or fulfillment capacity. It therefore cannot identify the reported successor ministry by itself.

### 3. G3+ web application remains reachable

Direct fetch of:

`https://plus.g3min.org/`

resolved to the G3 Plus JavaScript web application shell on 2026-09-08.

The current legal routes remain reachable:

- `https://plus.g3min.org/legal/privacy-policy`
- `https://plus.g3min.org/legal/terms-of-service`

Both legal texts still identify the service as G3 / G3 Plus and direct users to `admin@g3min.org`; however, both are dated **2025-04-03**.

**Boundary:** current reachability of an old legal document is not proof that its named service provider is still the beneficial owner after a later private transaction. Treat the 2025 legal text as continuity metadata, not a 2026 ownership certificate.

### 4. Apple platform seller identity still points to G3

Current Apple App Store surfaces observed/crawled around 2026-09-08 show:

#### iOS/iPad G3+

App ID:

`1192776791`

Developer / provider:

`G3 Ministries For The Church, Inc.`

The listing continues to describe access to the G3 Press library and G3 ministry content.

#### Apple TV G3 Plus

A distinct 2026 tvOS listing is visible at App ID:

`6761784816`

Seller:

`G3 Ministries For The Church, Inc.`

Copyright:

`© 2026 G3 Ministries`

The tvOS listing directs subscribers to `plus.g3min.org`.

This is useful dated **platform-account identity** evidence. It is not a corporate-title opinion: App Store seller metadata can lag an asset transfer, remain temporarily under the transferor account, or be changed after a closing.

### 5. Google Play developer/support identity still points to G3

Current Google Play listing for package:

`com.subsplashconsulting.s_V9572P`

shows:

- app: `G3+`;
- developer identity: `G3 Ministries, Inc` / `G3 Ministries for the Church` across the current listing surfaces;
- support email: `admin@g3min.org`;
- developer address: `4979 Highway 5, Douglasville, GA 30135`;
- current direct listing display: `Updated on Jul 23, 2026`.

Earlier indexed/crawl surfaces exposed a conflicting Sep. 4 update date. The current direct listing therefore favors **Jul. 23, 2026** for the presently displayed Google Play update field, while the historical crawl conflict should remain preserved rather than silently erased.

Again, platform developer identity is not proof of beneficial ownership or transaction completion.

## Fresh successor-ministry search

Fresh public-web searches on 2026-09-08 for combinations of:

- `G3+` / `G3 Plus`;
- `G3 Press`;
- `another ministry`;
- `acquired` / `acquiring` / `successor`;
- `Living Heritage`;

still surfaced the same substantive public boundary:

- subscriber reporting says another ministry is/was expected to acquire G3+;
- secondary reporting says the same unnamed ministry may acquire G3 Press;
- no current primary announcement located in this pass names the ministry, identifies closing terms, or publishes an asset schedule.

Michelle Lesley expressly states she has no insider information identifying the acquiring ministry. Her report remains discovery/corroboration of the **reported intended transfer**, not proof of legal closing or transferee identity.

Living Heritage currently includes G3+ membership in Premium offerings, but that is commercial/access continuity only. It does not establish that Living Heritage acquired G3+, G3 Press, subscriber contracts, intellectual property, domains, app-store accounts, or inventory.

## Claim impact

### Q006 / G3-C030 — named successor ministry

**Remains UNVERIFIED / EVIDENCE_HOLD.**

The new evidence does **not** identify a transferee.

What it does establish is narrower and useful:

> As of 2026-09-08, public app-store seller/developer metadata still identifies G3, the G3+ web application remains reachable, and the G3 Press commerce storefront remains live. No public primary object located in this pass names the reported successor ministry or states closing terms.

### Transfer-not-occurred theory

The following inference remains **REFUTED / prohibited**:

> Because Apple/Google still say G3, the transfer definitely did not occur.

Platform-account metadata can lag a private closing or remain temporarily under the transferor account.

### G3-resumed-operations theory

The following inference remains **REFUTED / prohibited**:

> Because G3 Press and G3+ are still reachable, G3 reversed the announced operational wind-down.

The current evidence is layered:

- main `g3min.org` live root → 503;
- indexed/crawled old pages → still visible;
- G3 Press store → live;
- G3+ web app → reachable;
- app-store seller metadata → still G3;
- Georgia corporation → Active/Compliance at the dated official acquisition.

Those layers can coexist during wind-down, asset disposition, platform migration, inventory liquidation, or delayed account transfer.

## Next proof gate for Q006

Do **not** spend another cycle merely re-reading app-store metadata. The next material closure object must be one of:

1. successor-ministry announcement naming the acquisition;
2. G3 board/subscriber notice naming the recipient;
3. recipient-side Terms/Privacy/merchant identity after transfer;
4. app-store seller/developer-account change naming a new legal entity;
5. domain/tenant/account transfer evidence tied to a named entity;
6. asset-purchase/assignment agreement or public corporate filing;
7. title-by-title G3 Press assignment/reversion records sufficient to reconstruct which IP actually transferred.

Until one of those appears, `another ministry` remains the maximum supportable public description.

## Reconciliation note

PASS18 is staging. Its observations should be promoted by **updating** existing canonical source/claim families S032/S033/S049/S050/S053 and C030/C056–C060 rather than minting duplicate independent evidence rows.
