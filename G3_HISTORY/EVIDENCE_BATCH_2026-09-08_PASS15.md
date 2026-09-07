# G3 HISTORY — evidence batch 2026-09-08 PASS15

**Status:** STAGING / PUBLICATION_HOLD  
**Purpose:** reconstruct the G3+ technical/platform layer so app-store/privacy metadata is not misread as legal ownership evidence during the 2026 transfer investigation.

## Provisional sources

| ID | Source | Class | Access | Locator | Rights | Publication | Use / boundary |
|---|---|---|---|---|---|---|---|
| G3-S125 | G3+ web privacy policy at `plus.g3min.org`, last updated 2025-04-03 | A2 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | G3-controlled web-app policy calls G3 the `Service Provider`, says the application may collect email/name and other usage data, identifies third-party services, and directs privacy questions to `admin@g3min.org`. Current public text provides a pre-transfer/controller baseline; it does not prove that the same controller remains after any later closing. Locator: `https://plus.g3min.org/legal/privacy-policy`. |
| G3-S126 | Apple App Store — legacy/current iOS G3+ app `id1192776791` | A3 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Apple currently displays seller/developer `G3 Ministries For The Church, Inc.`, in-app G3+ subscriptions, copyright ©2023 G3 Ministries, and privacy/terms links to Treefort Systems. This is platform metadata and may lag legal transfer. Locator: `https://apps.apple.com/us/app/g3/id1192776791`. |
| G3-S127 | Google Play — G3+ package `com.subsplashconsulting.s_V9572P` | A3 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Current Google Play metadata lists developer `G3 Ministries for the Church`, `admin@g3min.org`, 4979 Highway 5, phone, and a Jul. 23, 2026 update on one localized surface. The package identifier retains a historical `subsplashconsulting` namespace while present app/privacy stack points elsewhere; package name is not ownership evidence. Locator: `https://play.google.com/store/apps/details?id=com.subsplashconsulting.s_V9572P`. |
| G3-S128 | Apple App Store — separate Apple TV `G3 Plus`, `id6761784816` | A3 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Current Apple TV app is separately listed as G3 Plus, seller/developer `G3 Ministries For The Church, Inc.`, copyright ©2026 G3 Ministries, and requires a G3 Plus subscription via `plus.g3min.org`. This is a useful 2026 technical-distribution baseline. Locator: `https://apps.apple.com/us/app/g3-plus/id6761784816`. |
| G3-S129 | Treefort Systems — current customer/product site | A2 third-party vendor primary | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Treefort currently presents G3+ as a customer/testimonial and explains its platform model: customers upload media/design their app, and Treefort launches branded apps across web, Play Store and App Store. Treefort identifies itself as Treefort Systems LLC, Idaho. This strongly supports technical vendor/platform status, not ownership of G3+ content/business. Locator: `https://treefortsystems.com/`. |
| G3-S130 | FusionAuth case study — Treefort white-label architecture | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Independent technical case study quotes Treefort’s co-founder describing Treefort as a white-label media streaming platform for organizations’ branded web/iOS/Android apps. This corroborates the platform-vendor interpretation of Treefort links in G3+. Locator: `https://fusionauth.io/blog/treefort-uses-fusionauth-for-all-auth`. |
| G3-S131 | Treefort 2025–2026 changelog | A2 third-party vendor primary | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | PUBLICATION_ELIGIBLE | REFERENCE | Treefort documents automated App Store/Play Store submissions, subscription-plan export fields, billing roles, and continued platform feature deployment through Aug–Sep 2026. This establishes a technical environment where app-store metadata, tenant data, billing/provider fields and app binaries can change on different timelines. Locator: `https://treefortsystems.com/changelog/`. |

## Provisional claims

| ID | Claim | State | Support / boundary |
|---|---|---|---|
| G3-C166 | Treefort Systems is a technical white-label app/platform provider used by G3+, not presently evidenced as the announced 2026 G3+ acquiring ministry. | CORROBORATED | G3-S126/S129/S130. Current evidence describes a vendor/client platform relationship. No acquisition announcement or beneficial-ownership record names Treefort as transferee. |
| G3-C167 | Current Apple/Google metadata continues to identify G3 Ministries For The Church, Inc. as G3+ seller/developer while the public transfer is reported as pending/occurring to an unnamed ministry. | VERIFIED_PRIMARY_AS_PLATFORM_STATE | G3-S126–S128. Normalize canonical state to `VERIFIED_PRIMARY` with platform-state qualifier. This is not dispositive legal ownership. |
| G3-C168 | Google Play shows a G3+ update dated Jul. 23, 2026 on a current localized surface, placing active app distribution/maintenance very close to the August crisis. | VERIFIED_PRIMARY | G3-S127. This says nothing by itself about who performed the update or who owned the platform after August. |
| G3-C169 | The separate Apple TV G3 Plus app provides an additional 2026 distribution object tied publicly to G3 Ministries and `plus.g3min.org`. | VERIFIED_PRIMARY | G3-S128. Exact initial release date remains unacquired; copyright year alone is not a launch date. |
| G3-C170 | Treefort privacy/terms links on G3+ prove Treefort owns G3+ or is `Ministry X`. | REFUTED | G3-S129–S130 explain a white-label vendor model. Technical service-provider links are compatible with G3 or a successor ministry owning/controlling the media business. |
| G3-C171 | App-store seller/developer identity necessarily changes on the same date a private asset acquisition closes. | REFUTED | G3-S131 plus ordinary platform architecture: app ownership/tenant migration, store-account transfer, binary submission, billing-provider migration and legal closing can occur on different dates. A closing document is required. |
| G3-C172 | G3+ transfer reconstruction must distinguish at least legal asset owner, app-store seller account, Treefort tenant/platform customer, subscription merchant/provider, content licensor, domain controller and data controller. | INFERENCE | G3-S125–S131. Collapsing these roles would create false ownership conclusions. |

## G3+ role matrix after PASS15

| Role | Current public state | Evidentiary boundary |
|---|---|---|
| Historical/current named service provider on G3+ privacy page | `G3` | policy last updated 2025-04-03; may become stale |
| Apple iOS seller | `G3 Ministries For The Church, Inc.` | platform metadata, not closing instrument |
| Google Play developer | `G3 Ministries for the Church` | platform metadata |
| Apple TV seller | `G3 Ministries For The Church, Inc.` | platform metadata |
| White-label technical platform | Treefort Systems | vendor relationship strongly supported |
| Old Android package namespace | `com.subsplashconsulting...` | historical technical artifact; do not infer current vendor/owner |
| Web app | `plus.g3min.org` | current public route |
| Announced 2026 transferee | unnamed ministry | still unidentified |
| Living Heritage Premium G3+ entitlement | current paid bundle | supplier/fulfillment agreement unknown |

## Transfer acquisition implications

A post-closing proof package should seek separate evidence for:

1. asset-purchase/assignment agreement;
2. Treefort tenant/account transfer or customer-name change;
3. Apple developer/seller-account transfer date;
4. Google Play developer/account transfer date;
5. subscription merchant/provider migration;
6. domain/DNS ownership/control changes for `plus.g3min.org` if any;
7. privacy-policy/data-controller update;
8. user/subscriber data-transfer notice/consent basis;
9. content-license assignments from third-party ministries/authors;
10. G3 Press eBook/audiobook title-license continuity;
11. Living Heritage bulk/affiliate G3+ entitlement after closing.

A mismatch in dates among these layers is not automatically evidence of deception or improper transfer; migrations commonly have separate operational dates. The research must reconstruct the sequence before drawing conclusions.

## Reconciliation note

PASS15 is staging.

- S126/S127 overlap earlier Google/Apple platform-state sources; canonicalize as current access/metadata upgrades rather than duplicate witnesses.
- S129 is a genuinely distinct technical-vendor primary source.
- S130 is independent corroboration of Treefort’s white-label role, not an ownership source.
- S125 is G3-controlled policy text and can support historical/current public controller representation only within its dated boundary.
- C166–C172 should be reconciled with existing asset-transfer guardrails before master-ledger promotion.
