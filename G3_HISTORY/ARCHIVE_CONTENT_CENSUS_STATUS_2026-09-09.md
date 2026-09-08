# G3 archive content census — acquisition checkpoint, 2026-09-09

**Status:** `ARCHIVE_URL_FRAME_ACQUIRED / ARTICLE_DENOMINATOR_OPEN / QUANTITATIVE_LANGUAGE_HOLD / PUBLICATION_HOLD`  
**Purpose:** replace the failed live sitemap / WordPress-API denominator route with a reproducible metadata-only Wayback CDX discovery frame without converting URL discovery into topic prevalence claims.

## Exact acquisition

Workflow: `G3 archive content inventory acquisition`  
Run: `34288148002`  
Run attempt: `1`  
Research acquisition head: `ab719ff7870cbce0dd12ed79973dda16c79f72f8`  
Artifact: `g3-archive-content-inventory-34288148002-1`  
Artifact ID: `10080484091`  
Artifact ZIP digest: `sha256:da78c6e20275ec2c688c76688fb163833f98e09251ade104abe76733d7d2a45b`

Acquisition was metadata-only. It fetched CDX index responses, not archived article HTML bodies, images, audio, video or WARC payloads.

The workflow used the Internet Archive CDX resumption-key contract (`showResumeKey=true` followed by `resumeKey`) with:

- HTTP status filter `200`;
- mimetype filter `text/html`;
- `collapse=urlkey`;
- bounded retry handling;
- bounded resume-page safety limit;
- fail-closed parse/schema/invariant handling.

## Planned frame

Two historical domain families were queried over the relevant G3 eras:

- `g3conference.com`, 2011-01-01 through 2020-12-31;
- `g3min.org`, 2020-01-01 through 2026-12-31.

The v3 acquisition queried root and `www` spellings as explicit host-era controls. Wayback returned identical CDX witness sets for the two spellings inside each family:

- `g3conference.com` query: 178 rows;
- `www.g3conference.com` query: the same 178 rows;
- `g3min.org` query: 7,381 rows;
- `www.g3min.org` query: the same 7,381 rows.

Therefore the raw `15,118` witness-row count is **not** a content denominator and must not be interpreted as 15,118 independent pages. The duplicated host-query witnesses are a query-control artifact. Canonical URL normalization is the relevant discovery layer.

## Terminal result

`ACQUISITION_RESULT = ARCHIVE_URL_INVENTORY_ACQUIRED`

- planned host-era scans: **4**;
- completed host-era scans: **4**;
- CDX pages fetched: **18**;
- raw CDX witness rows: **15,118** including the deliberate duplicate root/`www` control queries;
- normalized unique URLs: **5,988**;
- transport holds: **0**;
- overflow holds: **0**;
- semantic/parse errors: **0**;
- `denominator_complete_for_planned_cdx_frame = true`.

Normalized unique URLs by family:

- `g3conference.com`: **142**;
- `g3min.org`: **5,846**.

Route-class discovery counts:

- `article_or_page_candidate`: **4,105**;
- `podcast_candidate`: **136**;
- `event_page_candidate`: **53**;
- `conference_page_candidate`: **1**;
- `navigation_or_taxonomy`: **1,677**;
- `navigation_or_landing`: **12**;
- `navigation_or_archive`: **4**.

These are **route heuristics**, not topic codes and not publication denominators.

## Anchor validation

The inventory recovers known first-party anchors from the independently verified qualitative research, including:

- `https://g3min.org/a-story-of-restorative-grace/` — first CDX witness `20220407120258`;
- `https://g3min.org/the-dangerous-intersection-of-christian-nationalism-and-ethnocentrism/` — `20230427140006`;
- `https://g3min.org/christian-faithfulness-the-biblical-alternative-to-christian-nationalism/` — `20230503050115`;
- `https://g3min.org/about/who-we-are/` — archive discovery present;
- `https://g3min.org/events/g3-2023-the-sovereignty-of-god/` — archive discovery present;
- multiple social-justice and Donald-Trump-era article URL anchors already known from qualitative work.

This validates the inventory as a useful historical discovery frame. Capture date remains archive-observation date unless an independent publication date is established; it must never be silently rewritten as publication date.

## What this closes

The earlier live-corpus blocker was:

`PUBLIC_METADATA_ACCESS_HOLD` because live sitemap routes returned HTTP 503 and the WordPress API returned HTTP 403.

That acquisition problem is now closed for archive URL discovery:

`ARCHIVE_URL_DISCOVERY_FRAME = ACQUIRED`.

We now have a reproducible, frozen URL universe suitable for the next adjudication stage rather than relying on search-result relevance.

## What this does **not** close

The artifact itself correctly preserves:

- `domain_era_attribution_closed = false`;
- `article_denominator_closed = false`;
- `topic_coding_authorized = false`;
- `quantitative_language_authorized = false`;
- `publication_authorized = false`.

Why:

1. URL existence in CDX is not proof that every route is an authored article.
2. The `article_or_page_candidate` class still mixes articles, product/library pages, static pages, embeds and other routes.
3. Archive coverage is not guaranteed to equal the complete historical publishing corpus.
4. Topic coding requires headline/dek/body/session context; keyword-only coding remains prohibited.
5. Historical domain-era attribution must be bounded before using early/late captures as G3 content.
6. Podcast, conference, article and product universes must remain separate denominators.

## Publication consequence

No statement such as the following is authorized from this artifact:

- `X% of G3 content was political`;
- `political material became dominant in year Y`;
- `social-justice content increased by Z%`;
- `most/rare/almost all G3 publications...`.

The qualitative conclusion remains the publication-safe level unless a later coding dataset closes the article/session denominator:

> G3’s main conference themes remained strongly theological/ecclesial, while cultural and political commentary existed in the broader media ecosystem before 2018 and later became more explicit in boundary conflicts. The 2023 Christian-Nationalism/theonomy dispute added a right-flank conflict rather than demonstrating a simple one-direction ideological move.

## Research closure rule

A fully coded quantitative corpus is **optional enrichment**, not a blocker for a bounded documentary article that avoids percentage/prevalence language.

For the current G3 publication route:

`QUANTITATIVE_IDEOLOGY = EXCLUDED_FROM_AUTHORIZED_CLAIM_SET`.

Reopen this lane only if the editorial product specifically requires numerical prevalence/trend claims. In that case the next work is deterministic route adjudication + stratified/full article sampling + source-context coding under `IDEOLOGY_CONTENT_CODING_PROTOCOL.md`, not another search-engine sweep.

`SEARCH RESULTS != CORPUS CENSUS` remains authoritative.
