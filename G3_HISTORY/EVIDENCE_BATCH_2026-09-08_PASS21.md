# G3 HISTORY — evidence batch 2026-09-08 PASS21

**Status:** ACTIVE / STAGING-TO-CANONICAL / PUBLICATION_HOLD  
**Scope:** FBC Lindale original-media locator census for Buck Items 11–17 and bounded-audio acquisition manifest.

## 1. Official/public media locator census

Two independently useful public surfaces now converge on the late Buck sermon identities:

1. First Baptist Church of Lindale official sermon pages;
2. the public FBC Lindale RSS feed `https://feedpress.me/fbc-lindale`.

The official FBC pages directly identify the sermon title/date and embedded Vimeo object. The RSS feed exposes direct audio enclosures for the six items still inside its current 100-episode window.

### Exact-head RSS acquisition

Workflow: `G3 Buck RSS media locator inventory`  
Run: `34261223520`  
Research head: `2f6b844028cb3157619b7dcf2fb08036c86ba6de`  
Feed HTTP status: `200`  
Feed content type: `text/xml`  
Feed bytes: `114376`  
Feed SHA-256: `47297b27f9818dd24059851c0c6210b407c4637816a29b99d18fc68f77afb7f5`  
Artifact SHA-256: `50fd012bf5a1da802f3eeed16d31a85fafdfc37bb247a8b9b011646f871632bf`

The feed contained 100 episode rows. Six dossier sermons matched exactly by title **and** date; all six expose `audio/mpeg` enclosures. Eleven older dossier sermons are simply outside the current 100-row feed and are recorded as `NOT_IN_CURRENT_FEED`, not as absent media.

## 2. Late-sermon locator matrix

| Item | Sermon | Date | Official FBC page | Vimeo ID | RSS direct media state |
|---:|---|---|---|---:|---|
| 11 | Romans 7:1–6 | 2024-01-07 | `https://fbclindale.com/resources/sermons/romans-71-6/` | `900633606` | `NOT_IN_CURRENT_FEED`; official page remains primary locator |
| 12 | Romans 15:1–6 | 2025-10-19 | `https://fbclindale.com/resources/sermons/romans-151-6/` | `1128676834` | direct MP3 identified |
| 13 | Romans 16:25–27 | 2025-12-21 | `https://fbclindale.com/resources/sermons/romans-1625-27-2/` | `1149768050` | direct MP3 identified |
| 14 | Joshua 1:1–9 | 2026-01-18 | `https://fbclindale.com/resources/sermons/joshua-11-9/` | `1156717093` | direct MP3 identified |
| 15 | Joshua 2:1–24 | 2026-02-08 | `https://fbclindale.com/resources/sermons/joshua-21-24/` | `1163070006` | direct MP3 identified |
| 16 | Joshua 3:1–17 | 2026-02-15 | `https://fbclindale.com/resources/sermons/joshua-31-17/` | `1165204580` | direct MP3 identified |
| 17 | Joshua 4:1–24 | 2026-03-01 | `https://fbclindale.com/resources/sermons/joshua-41-24/` | `1169432943` | direct MP3 identified |

RSS GUID/direct-origin values for Items 12–17:

- Item 12: `https://s3.amazonaws.com/fbclindale.com/wp-content/uploads/2025/10/19135848/2025_10_19_AM.mp3`;
- Item 13: `https://s3.amazonaws.com/fbclindale.com/wp-content/uploads/2025/12/27192512/2025_12_21_AM.mp3`;
- Item 14: `https://s3.amazonaws.com/fbclindale.com/wp-content/uploads/2026/01/18161411/2026_01_18_AM.mp3`;
- Item 15: `https://s3.amazonaws.com/fbclindale.com/wp-content/uploads/2026/02/08135446/2026_02_08_AM.mp3`;
- Item 16: `https://s3.amazonaws.com/fbclindale.com/wp-content/uploads/2026/02/15143218/2026_02_15_AM.mp3`;
- Item 17: `https://s3.amazonaws.com/fbclindale.com/wp-content/uploads/2026/03/01204545/2026_03_01_AM.mp3`.

**Finding:** original-media identity/locator is no longer a discovery problem for Items 11–17. For Items 12–17, a public audio enclosure is directly identified from the FBC feed.

**Boundary:** locator verification is not content verification and does not close `ITEM_VERIFIED`.

## 3. Accusation timestamps re-read from the primary 31-page packet

The directly inspected accusation PDF supplies the following allegation timestamps used to bound the next acquisition. These timestamps identify what the accusers ask us to test; they do not independently prove the transcript rows.

### Item 11 — Romans 7:1–6

Key timestamps: `17:02`, `19:00`, `32:23`.

### Item 12 — Romans 15:1–6

High-value block: `16:00` and `17:31`; later row around `41:05`. The `trespasses/debts` illustration near `3:27` is already source-lineage-downgraded as a circulating joke and is therefore not prioritized for expensive media review.

### Item 13 — Romans 16:25–27

High-value sequence around `37:48`.

### Item 14 — Joshua 1:1–9

Rows around `17:58`, `28:41`, `30:50`, `32:12–33:20`. Existing audit grades this item lower than the strongest late items; acquisition is included for completeness but interpretation remains specificity-sensitive.

### Item 15 — Joshua 2:1–24

Rows around `5:18`, `7:20`, `10:29`, `20:39`, `32:30`, `33:09`, `33:32`, `43:43`.

### Item 16 — Joshua 3:1–17

Rows around `15:18`, `24:33`, `29:48`, `31:48`, `33:06`, `34:03`, `37:50`, `38:05`, `39:16`, `39:51`, `41:55`.

### Item 17 — Joshua 4:1–24

Rows around `9:23`, `11:45`, `12:18`, `31:31`, `33:42`, `35:18`, `43:12`, with late repeats referenced around `48:14` and `50:49`.

## 4. New bounded original-media lane

A new read-only/ephemeral acquisition tool is staged for Items 11–17. It will:

- use only public FBC sermon pages/media routes;
- acquire narrow windows surrounding the dossier timestamps rather than archive full sermons;
- hash each acquired source segment;
- run local Whisper only as a diagnostic;
- delete every audio/video binary before artifact upload;
- retain receipts, hashes and machine transcript JSON only;
- keep `machine_transcript_only=true` and `item_verified=false`.

The windows are deliberately wider than a single allegation sentence so attribution immediately around the disputed language is less likely to be clipped away. They still do **not** substitute for human listening or a whole-section attribution review.

## 5. Interpretation firewall

The next machine-transcript results may establish that alleged wording/subject matter is present in original FBC media and can expose obvious attribution tokens for targeted human review.

They may **not** by themselves establish:

- quote-safe verbatim wording;
- that attribution is absent from the sermon;
- literary dependence;
- plagiarism severity;
- or `ITEM_VERIFIED`.

The final gates remain human original-audio review + exact source edition + attribution context + dependence analysis.
