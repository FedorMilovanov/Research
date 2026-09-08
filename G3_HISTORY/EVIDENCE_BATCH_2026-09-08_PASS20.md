# G3 HISTORY — evidence batch 2026-09-08 PASS20

**Status:** ACTIVE / STAGING-TO-CANONICAL / PUBLICATION_HOLD  
**Scope:** Titus original-media breakthrough, live-content census access boundary, and G3+ successor negative search.

## 1. Buck Item 10 — original-media access gate materially upgraded

A read-only GitHub Actions lane acquired a public original-media segment for Tom Buck's FBC Lindale sermon `Titus 2:11–15` (2023-08-06).

### Exact acquisition authority

- workflow: `G3 Buck Titus original-media acquisition`;
- run: `34254294262`;
- Research head: `f086679ae47a36cb7e99e66beb4a63886449e1dc`;
- official landing page: `https://fbclindale.com/resources/sermons/titus-211-15/`;
- selected route: `fbc_landing`;
- public MP3 exposed by the official page: `https://s3.amazonaws.com/fbclindale.com/wp-content/uploads/2023/08/06124555/2023_08_06_AM.mp3`;
- authentication/cookies: **none**;
- requested window: `00:32:30–00:36:30`;
- acquired segment duration: 240 seconds;
- segment size: 23,040,104 bytes;
- segment SHA-256: `954041ea7b697ed98c27db8a852c8bb798db14ec44f69ec6e634046a2bd9729a`;
- audio binary retained in artifact: **false**;
- machine transcription: successful;
- `machine_transcript_only = true`;
- `item_verified = false`.

This removes the former technical proposition `original Buck media is inaccessible` for Item 10.

It does **not** close the human quotation/attribution gate.

### Machine-transcript diagnostic

The machine transcript in the acquired four-minute source window contains the marriage/application block involving Jennifer and Buck's description of early marital coldness/selfishness and later sensitivity to his wife's love. It also contains the adjacent holiness/application material.

Within this machine-generated four-minute window, no explicit `Chapell`, `Hughes`, or `commentator` token was detected.

**Firewall:** this is a machine diagnostic, not a quote-safe human transcript and not proof that attribution is absent outside the selected window. Before `ITEM_VERIFIED`, a human must check the original source audio and a sufficiently wide context before/after the alleged block.

### Corrected Item-10 state

The old `BUCK_AUDIO_HOLD` wording is now too broad.

Correct state:

`ORIGINAL_MEDIA_SEGMENT_ACQUIRED / MACHINE_TRANSCRIPT_ONLY / HUMAN_AUDIO_AND_WIDER_ATTRIBUTION_CONTEXT_HOLD`.

The separate biographical correction remains unchanged: Jennifer Buck's pre-controversy 2022 account blocks the claim that analogous marital circumstances were simply fabricated. Original-media acquisition does not erase the distinct wording/attribution question.

## 2. Public G3 content census — first live metadata route exhausted for now

Exact-head run `34254408853` on `1d5b9ee018deb0dbda8424fbfb873a64f99cc810` completed successfully as a diagnostic.

It returned:

- sitemap routes → HTTP 503;
- WordPress REST metadata route → HTTP 403;
- `0` sitemap URLs;
- `0` WP rows;
- acquisition result `PUBLIC_METADATA_ACCESS_HOLD`.

These zero rows are **not** a historical content denominator. The quantitative ideological-language HOLD therefore remains.

Canonical status: `CONTENT_CENSUS_ACQUISITION_STATUS_2026-09-08.md`.

Next route: archive-first metadata census, not another identical live WordPress retry.

## 3. G3+ / G3 Press successor — stronger screenshot wording, identity still open

A contemporaneous subscriber-email screenshot reproduced publicly states that G3+ was “being acquired by another ministry,” that access/library/price were expected to continue, and that the ministry name could not yet be shared; a later follow-up was promised when the transition became final.

This materially strengthens the proposition that G3 itself communicated an intended acquisition/transition to subscribers.

It still does **not** identify the acquiring ministry or prove legal closing/asset title.

Fresh Sep. 8 searches did not surface a recipient-side announcement naming:

- Right Response Ministries;
- Living Heritage;
- Treefort;
- or another named successor.

Right Response remains a speculative social-media lead. Living Heritage's 2025 separation is separately `VERIFIED_PRIMARY` from the raw IRS filing but does not establish 2026 acquisition. Treefort remains a technology/provider lead, not buyer evidence.

Q006 therefore remains:

`OPEN / INTENDED-TRANSFER COMMUNICATION STRENGTHENED / NAMED TRANSFEREE + TERMS HOLD`.

## 4. CI/readback reconciliation

The lone transient exact-head `G3 Wayback 2025 board transition acquisition` failure was rerun without a new commit. The rerun completed successfully. This restores a clean exact-head readback for the current six PR-triggered authority/acquisition workflows on `1d5b9ee018deb0dbda8424fbfb873a64f99cc810`.

The successful rerun does not create new historical evidence; it confirms the earlier archive-route exhaustion without the transient transport error.

## 5. Next controlled lane

A metadata-only FBC Lindale RSS inventory is being added to map all 17 accusation-sermon items against the official/public podcast feed without downloading sermon audio. Its purpose is to mass-close media locators where available and distinguish:

- `MEDIA_LOCATOR_VERIFIED`;
- `NOT_IN_CURRENT_FEED`;
- `AMBIGUOUS_MATCH`.

Locator coverage is not `ITEM_VERIFIED`.
