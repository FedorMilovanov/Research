# Steven J. Lawson — primary-object acquisition and 2026 status audit


> **Status note (2026-09-28):** This file is a **historical acquisition-pass snapshot**. Its OPEN/P0/P1 labels were later changed by `12_`–`17_`; current operational status is `19_CURRENT_STATUS_AND_ACQUISITION_QUEUE_2026-09-28.md`.
**Corpus:** `LAWSON-2024-2026`
**Snapshot:** `2026-09-27`
**Status:** `ACTIVE / PARTIAL P0 CLOSURE / PUBLICATION_HOLD (reduced)`
**Policy:** [`../data/repository-evidence-policy-v2.json`](../data/repository-evidence-policy-v2.json)
**Companion:** [`00_AUTHORITY_AND_SCOPE_2026-09-27.md`](00_AUTHORITY_AND_SCOPE_2026-09-27.md), [`02_SOURCE_LEDGER_2026-09-27.md`](02_SOURCE_LEDGER_2026-09-27.md)

This pass targeted the open `PUBLICATION_HOLD` queue from `00` §7 and the addendum P0 queue from `04` §7. It produced three durable acquisitions, one important correction of a previously derivative-only quote, and new 2026 status material.

---

## 0. What changed in this pass

| Target | Before | Now |
|---|---|---|
| Exact locator for the Lawson segment in GTY 70-58 | `COARSE_LOCATOR_ONLY` | **CLOSED** — second-level timestamps on the official audio, wording anchored to the official transcript |
| Original recording of Shepherds' Conference 2017, General Session 14 (Lawson) | derivative transcript only (`C/B1`) | **RECOVERED** — official conference MP3 acquired; the "unconverted shepherd" statement is now quote-safe with exact locators |
| Original OnePassion statement (2024-09-20) | B1 retellings only | **RECOVERED** — archived original object captured in custody |
| Ligonier 2023 London Lawson session pages | presumed live (ledger listed pages as reachable) | **OBSERVATION** — all five Lawson pages currently HTTP 404; non-Lawson pages 200; archived captures obtained |
| 2026 public-status picture (post-book) | not covered | **NEW** — conference listing episode (July 2026), authorship confirmation and critical reactions (September 2026) |
| Trinity statement original | pending | still pending (Wayback 403/504 on the church domain for Sep 2024 — Jan 2025) |
| Full book object / page locators | pending | still pending |
| Romans 2 official recordings | pending | still pending |
| Durable archive of the 2025-03-12 X statement | pending | still pending (archive.today rate-limited; Wayback has no capture) |

Method note (applies to §1–§2): machine transcription was used **only to locate** utterances in official audio. The **wording authority** remains (a) the official Grace to You transcript for GTY 70-58, and (b) the official conference recording itself for Shepherds' Conference 2017. ASR was performed locally with `faster-whisper` (`base.en`, int8, chunked 600-s decoding, PyAV/16 kHz mono) — timestamp precision ±1 s at sentence boundaries; no ASR text should be quoted where an official text object exists.

---

## 1. Grace to You 70-58 (2024-10-20) — timestamp closure

**Objects acquired**

- Official transcript page (A2): <https://www.gty.org/sermons/70-58/thinking-biblically-about-current-events-a-conversation-with-john-macarthur> — full text preserved in research scratch (`_work/gty70-58.txt`, 43 479 chars).
- Official audio (A2, same publication): `https://mic-development-us5p473zyq-core-4j1au-mediabucket-6bjazokcoje1.s3.us-east-1.amazonaws.com/Audio%2FSermons%2F70_58_db35a2d1dc.mp3`
  - Custody: `_work/gty70-58.mp3`, 56 345 173 bytes, 128 kbps 44.1 kHz mono.
  - `sha256: 24162964450f397b43663b7674d80965557c23ff6a4265cee3131cfb24ada4dc`
  - Container duration 3519 s; decoded ASR timeline 3527 s.

**Exact locators (official transcript wording + official audio time)**

| Time | Wording (per official transcript) |
|---:|---|
| ≈19:00 | "Well, I know you're talking about Steve Lawson." |
| 19:03 | "And I say that with the deepest agony in my soul." |
| 19:16–19:25 | "God is blessing this church in many, many ways, and that is one of the ways He is blessing us: to expose someone who is in a position they have no right to be in." |
| 19:31 | "To purify the church." |
| ≈19:33–19:40 | "the church has two options: one, get right; two, you're done… It is fatal to a church to have that kind of behavior in leadership." |
| ≈19:45 | "while none of us knew it or expected it because of the soundness of the theology… 'For Grace Church, that's enough. For The Master's Seminary, that's enough.'" |
| 21:52 | "…a corrupting influence while apparently having a positive influence." |
| 22:29 | "But again, as we get closer to the end, I think the Lord is purifying His church…" |
| 22:45 | "I don't love him any less than I've loved him for twenty-five years." |
| 22:52–23:01 | "I don't know how you preach past your conscience unless it's completely scarred over." |
| 23:49 | "But while my heart is crushed for the sinner, it is grateful for the Savior who is purifying His church." |

**Publication-gate effect:** item 1 of `00` §7 ("exact locator/timestamp for the Lawson segment in GTY 70-58") is **closed**. Direct quotation is now safe when the official transcript wording is used together with these timestamps.

---

## 2. Shepherds' Conference 2017, General Session 14 — original recording recovered

**Event object**

- Title: *Jesus, The Good Shepherd* (John 10:11–18), Steven J. Lawson.
- Slot: Friday, March 3, 2017, 3:30 p.m. — General Session 14 of the 2017 Shepherds' Conference ("We Preach Christ"), Grace Community Church.
- Official audio (A2, institutional publication of the event): `https://s3.amazonaws.com/media.shepherdsconference.org/2017/SC17-GS-2017-03-03-1530-LAWSONS.mp3`
  - Custody: `_work/sc17_gs14_lawson.mp3`, 67 576 229 bytes, 128 kbps 44.1 kHz joint stereo.
  - `sha256: 195a8c44acc9383b6fc04f27eaef353839d8bfaf8046b3d36bdc34f5de696595`
  - Container duration 4223 s (70:23); decoded ASR timeline 4233 s.

**The closing appeal, verified against the original recording**

| Time | Verbatim (transcribed from the official recording) |
|---:|---|
| 67:01 | "And as I close, as you would find yourself here tonight, are you a true shepherd of the flock" |
| 67:12 | "because they are false shepherds?" |
| 67:18 | "Do you know the good shepherd?" |
| 67:22 | "It is one thing to preach on the door of the sheep." |
| 67:26 | "It is one thing to do word studies on the door of the sheep." |
| 67:31 | "It is one thing to admire the door of the sheep." |
| 67:34 | "It is one thing to point others to the door of the sheep." |
| 67:38 | "It is one thing to have your toes right up to the door of the sheep." |
| 67:43–67:52 | "But have you ever taken that decisive step of faith and come all the way to saving faith in Jesus Christ yourself?" |
| 67:54–68:10 | "It could be possible that as you find yourself here today that you in reality are like these Pharisees. And if so, you are a thief and you are a robber and you are stealing glory from God." |
| 68:17–68:23 | "And if you have never believed upon Jesus Christ, it is possible to even be at the shepherd's conference and to be an unconverted shepherd." |
| 68:27–68:41 | "And so if you have never come by faith to the good shepherd, the Lord Jesus Christ, I call you today on his behalf that whosoever shall call upon the name of the Lord shall be saved." |
| 68:42–69:54 | narrow gate / broad way, wise and foolish builders; closing call "to come through the door of the sheep" |
| 70:00–70:29 | closing prayer |

**Correction of a now-superseded derivative locator.** The previously used derivative transcript (lilys.ai, `C/B1`) dated the same appeal to about `01:11:35`. That locator does **not** correspond to the official conference audio timeline; the correct locator on the original recording is `68:17–68:23` for the "unconverted shepherd" sentence. The derivative object is retained as a discovery lead only.

**Catalog observation (no motive inferred).** On 2026-09-27 the current `gracechurch.org` Shepherds' Conference 2017 catalog page lists General Sessions 1–13 and 15; General Session 14 is absent, as is Lawson's seminar session ("The Cost", Seminar Session 2, 3/2/2017). Wayback captures of the same page from 2024-12-03 and 2025-03-17 likewise lack them. The official MP3 file itself remains live and downloadable. This corpus records the catalog state as an archival fact; it does not assert why or when the listings changed, and no conclusion about intent may be drawn from it.

**Article effect.** The strongest pre-fall quotation in the corpus — a pastor warning pastors that a man can stand at the door, point others to it, and still be an "unconverted shepherd" — is no longer dependent on a derivative transcript. It is now quote-safe (`A2` official recording, `EXACT_LOCATOR_VERIFIED`).

---

## 3. OnePassion Ministries statement (2024-09-20) — archived original recovered

- Archived object (A3 statement as published by the ministry, preserved by the Internet Archive):
  `https://web.archive.org/web/20240920233142/https://onepassion.org/`
  - Retrieval date 2026-09-27; capture timestamp `20240920233142`.
  - Custody: `_work/custody/onepassion_20240920233142.html`, 172 771 bytes, `sha256: a2b350d16e665070884e9165307bee15febcf64c36a48b8eefb88c0d1f60cea5`.

**Full statement text as captured (public statement block):**

> The board of OnePassion Ministries mournfully announces that just recently Steven J. Lawson confessed to the board that he has had an inappropriate relationship with a woman, a sin that has disqualified him from ministry. In response Steve has resigned from all his duties at OnePassion Ministries.
> All scheduled events and engagements have been canceled.
> Steve has confessed and regrets the damage he has caused to his family, the church, the reputation of OnePassion Ministries and most of all Jesus Christ.
> We are saddened for the glory of Christ in this matter. The truth of the gospel will continue go out to the lost world as it is empowered by the Holy Spirit and not by men. It is a reminder that we have been warned of the craftiness of the enemy.
> "Be sober-minded; be watchful. Your adversary the devil prowls around like a roaring lion, seeking someone to devour (1 Peter 5:8)."

**Publication-gate effect:** the OnePassion half of gate item 2 is now closed at the level of a preserved institutional object (`A3` origin, archived access). Trinity's own statement remains open; TMS's communication remains open.

---

## 4. Ligonier 2023 London conference — current availability observation

Checked on 2026-09-27 (`ligonier.org`):

| Page | Status |
|---|---|
| `…/preach-the-word-pre-conference` (Lawson) | **404** |
| `…/the-word-of-god-for-exiles` (Lawson) | **404** |
| `…/questions-and-answers-with-ferguson-lawson-parson-reev` (Lawson) | **404** |
| `…/questions-and-answers-with-ferguson-johnston-lawson-ni` (Lawson) | **404** |
| `…/questions-and-answers-with-ferguson-lawson-parsons-ree` (Lawson) | **404** |
| `…/the-ministry-of-prayer-pre-conference` (Reeves) | 200 |
| `…/ordinary-means-ministry-pre-conference` (Parsons) | 200 |
| `…/contend-for-the-faith-pre-conference` (Ferguson) | 200 |
| `…/elect-exiles` (Mbugua) | 200 |

Archived captures obtained for the two Lawson sessions (Internet Archive, late September 2024):
- `https://web.archive.org/web/20240927034417/https://www.ligonier.org/learn/conferences/pilgrims-and-exiles-2023-london-conference/preach-the-word-pre-conference` — title element confirms "*Preach the Word (Pre-Conference)* by Steven Lawson"; custody `_work/custody/ligonier_preachtheword_20240927034417.html`, `sha256: 31612e40d409200a2f45f36136d8f68892128cea8955b4200534a7972c5e7334`.
- `https://web.archive.org/web/20240927115455/https://www.ligonier.org/learn/conferences/pilgrims-and-exiles-2023-london-conference/the-word-of-god-for-exiles` — custody `_work/custody/ligonier_wordofgod_20240927115455.html`, `sha256: 9950ac3cd66ccb8aac38f64040aaebaa5e9faccfbcae966901c72d46fc7c7204`.

Limitations recorded:
- The archived HTML is a JavaScript shell: neither the video identifier nor the session description is present in the static capture. The capture proves title/attribution/URL history, not session content.
- The surviving third-party video card (`hopelife.org/watch/decj3vqcda0-steven-lawson-preach-the-word-pre-conference/20230919/`, fetched 200 on 2026-09-27, 15 176 bytes) still embeds a YouTube player. That embedded video id now resolves via YouTube oEmbed to unrelated content ("C. H. Spurgeon 24/7 Christian Radio Live Stream", channel `5KYRDR`), i.e. the original embed target is no longer identifiable through this page. The card's 2023-09-19 description (1 Timothy 4:2, hypocrisy of liars, branded/seared conscience) remains the stronger content description; it stays `B1` and is not quote-safe.
- Ligonier's YouTube channel still publicly hosts two Lawson items: the 2023 pre-conference *Questions & Answers with Ferguson, Lawson, Parsons, and Reeves* (`wuxWNjRANB8`, 40:08) and the 2024 National Conference stream including Lawson (`vgXk7uOp8sA`, 3:37:50). Neither substitutes for the removed *Preach the Word* session.

**Publication-gate effect:** gate item 3 (direct video/transcript of *Preach the Word*, exact 1 Tim. 4:2 timestamp) remains **OPEN**. Do not publish verbatim quotations attributed to that session.

---

## 5. 2026 public-status additions

### 5.1 Contending for the Faith conference episode (July 2026)

- Lawson briefly appeared (2026-07-20) as a keynote/workshop speaker on the website of the **Contending for the Faith Expository Preaching & Teaching Conference** ("Be Ye Steadfast", November 3–5, 2026, Southaven, MS), presented by the Tennessee Baptist Missionary & Educational Convention. His name was removed within hours.
- Protestia's follow-up states that the organizers had invited Lawson but advertised him **before receiving his response**, that the listing was an internal misunderstanding, and that Lawson informed them he was **declining** the invitation, after which he was removed.
- Sources (all `B1`; the conference site is `C/B1` for the listing itself, now corrected):
  - Protestia, 2026-07-20: <https://protestia.com/2026/07/20/steve-lawson-briefly-appears-as-conference-speaker-then-is-purged-from-website/> (with update) and <https://protestia.com/2026/07/20/exclusive-steve-lawson-not-speaking-at-upcoming-preaching-conference/>
  - ChurchLeaders, 2026-07-20: <https://churchleaders.com/news/2220300-steven-lawson-contending-for-the-faith-speaking.html>
  - JubileeCast, 2026-07-21: <https://www.jubileecast.com/articles/38109/20260721/steven-lawson-quietly-removed-from-pastors-conference-after-organizers-mistake.htm>
  - Conference site: <https://thecontendingconference.com/>
- Status: the episode is evidence **against** an active public-ministry comeback as of July 2026; it must be reported with the organizers' correction, not as "Lawson tried to return".

### 5.2 Book authorship and reactions (September 2026)

- **Phil Johnson** (pastor/elder, Grace Community Church), in a post of 2026-09-23 (`https://x.com/phil_johnson_/status/2102909077630370285`), affirmed that the book is genuinely Lawson's; he added that Lawson "would not gain respect or trust back from those he betrayed by reinserting himself into public discussion", and that selling the nearly $15 book was a bad look. Reported by WORLD/The Sift, 2026-09-24: <https://wng.org/sift/pastor-affirms-steven-lawons-authorship-of-scandal-memoir-1790267569>.
- **Justin Peters** (Facebook, September 2026) said the writing style suggests AI even if authored by Lawson — reported in the same WNG item; a `C`-class counterclaim, noted only as a public disagreement.
- Critical reactions on X: Michael Foster (`https://x.com/thisisfoster/status/2101793067846033727`) called it an attempt to make money; another critic (`https://x.com/JCRyle/status/2102026271106429386`) argued a disqualified man should serve quietly in his local church; a supportive post `https://x.com/BlessedlyBound/status/2102033998604017688` urged patience. Endorsement: Todd Leonard, 2026-09-20 (`https://x.com/Micah68min/status/2101666221062074524`), who reports having spent time with Lawson recently.
- Commentary context: Evangelical Dark Web, 2026-09-24 (<https://evangelicaldarkweb.org/2026/09/24/why-steve-lawons-book-is-not-a-grift-per-se/>) — the "grift" concern is framed around future speaking, not book royalties; the piece also references the July conference episode as the reason for skepticism. Opinion source; not factual authority.

**Effect on gate item 4 (book):** the authenticity question is now materially stronger (a named GCC pastor's statement via a reputable outlet + multiple catalogue objects), but the **book object itself is still not acquired**, so interior claims — including the reported refused-marriage-counseling admission — remain attributed to the reviewer until a page-verified object exists.

---

## 6. Open queue after this pass (replaces `00` §7 and `04` §7 statuses)

`P0`
1. Full lawful copy of *Mercy in the Wilderness* with page locators (or verified excerpts) — replace reviewer-level attribution of the Anne-counseling admission.
2. Original Trinity Bible Church statement object (Sept. 2024) — Wayback capture for the church domain in Sep 2024 – Jan 2025 is currently 403; retry periodically, check social mirrors, and any church-newsletter reproductions.

`P1`
1. Durable archive of the 2025-03-12 statement (archive.today / Wayback of the X status).
2. Official OnePassion/broadcaster objects for the Romans 2 messages (*The Moralist Condemned*, *Condemned by the Law*, *True and False Circumcision*).
3. Direct video/transcript of the 2023 Ligonier pre-conference session — currently unavailable on the live site; continue searching mirrors (Ligonier app, conference bundles, deleted-video reuploads).

`P2`
1. Trinity/TMS public communications after September 2024, if any, that speak to accountability without invading family privacy.
2. Any on-record clarification of who holds final spiritual authority over Lawson's restoration process, and whether the 2026 book was reviewed by those pastors/elders.
3. A later primary statement from the woman or her family — currently offline; do not seek or publish identifying material.

---

## 7. Editorial guardrails touched by this pass (restated)

- The 2017 quote must be presented as a **general pastoral warning**, not as autobiography; the recording shows no self-application and none may be inferred.
- The GCC catalogue observation is recorded as a fact about a web page, with no motive; the original audio remains publicly available.
- The Ligonier 404 observation likewise carries no motive claim; it is consistent with, but not proof of, a deliberate post-2024 removal policy.
- The 2026 reactions are other people's judgments; the article may report them as such, and may not convert them into verified facts about Lawson's heart state.
