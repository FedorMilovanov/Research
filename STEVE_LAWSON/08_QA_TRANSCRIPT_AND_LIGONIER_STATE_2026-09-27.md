# Steven J. Lawson — 2022 marriage Q&A transcript acquired; 2017 Q&A attribution corrected; Ligonier-2023 state

**Corpus:** `LAWSON-2024-2026`
**Snapshot:** `2026-09-27`
**Status:** `ACTIVE / PUBLICATION_HOLD (reduced)`
**Companion:** [`06_PRIMARY_OBJECT_AND_STATUS_AUDIT_2026-09-27.md`](06_PRIMARY_OBJECT_AND_STATUS_AUDIT_2026-09-27.md), [`02_SOURCE_LEDGER_2026-09-27.md`](02_SOURCE_LEDGER_2026-09-27.md)

This pass reopened the YouTube caption route, which produced three results: the previously unreachable 2022 marriage Q&A transcript, an authoritative correction of a claim in the live dossier, and a documented state of the Ligonier 2023 London conference materials.

---

## 1. Method: the caption route reopened

`yt-dlp` subtitle downloads now succeed in this environment (previously blocked), while media downloads remain restricted; no `ffmpeg` is required for subtitles.

Two caption classes were captured:

- **publisher captions (human-made)** on the official Ligonier Ministries channel — these carry speaker labels (`LARSON:`, `SPROUL:`, `MOHLER:`, `MACARTHUR:`, `LAWSON:`), which makes them the authoritative transcript of the panel audio for this corpus (`A2`, exact locators);
- **auto-generated captions** on other channels (derivative; locating use only).

Captured objects (all in the 2026-09-27 acquisition cache; SHA-256 in [`DURABLE_CUSTODY_MANIFEST.json`](DURABLE_CUSTODY_MANIFEST.json)):

| File | Content | Class |
|---|---|---|
| `cap_MfnYgz_e17M.en.vtt` (50 313 B) | Ligonier 2017 National Conference Q&A, publisher captions with speaker labels | A2 |
| `cap_wuxWNjRANB8.en.vtt` (42 592 B) | Ligonier London 2023 pre-conference Q&A, publisher captions | A2 (Q&A only) |
| `cap_q-Z5ozrJ4QY.en.vtt` (161 577 B) | «Should I Marry Her?» (Preaching for God's Glory), auto captions | B1 derivative |
| `cap_Ey7kYHEpcyo.en.vtt` (291 633 B) | «The Word of God for Exiles» re-upload, auto captions | B1 derivative |
| `cap_4kiWzPN7RbU.en.vtt` (80 726 B) | Paul Washer commentary on the 2026 book, auto captions | C/B1 commentary |

---

## 2. 2022 Men's Bible Study Q&A, «Should I Marry Her?» — transcript acquired

**Objects**

- Published episode: *Should I Marry Her? | Steve Lawson Answers | Men's Bible Study Q&A*, **Truth Transforms** (channel/site «Preaching for God's Glory»), published **2022-05-09**; audio enclosure `TT00027_Lawson+on+Marriage_FINAL.m4a` — 18 799 442 bytes, duration 1291.75 s (21:32), `sha256 5fbac8e8bcaae69eb0d3a06066ae3b8c2b6fa4b5676f42402e171595cc03f49e`.
- RSS receipt: `https://preachingforgodsglory.org/truth-transforms?format=rss` (82 items).
- Video derivative of the same episode: `q-Z5ozrJ4QY` (21:47).

**Carrier caveat.** The episode is a **third-party production**: a host introduces and frames the material ("this is at the men's Bible study, which is on every Thursday morning… here's a clip by Dr Stephen Lawson"), and Lawson's own audio runs as embedded clips. The original Thursday-morning Men's Bible Study recording has **not** been located. Until it is, quotations of Lawson from this episode must carry the carrier attribution («в эпизоде Truth Transforms, 9 мая 2022, по аудио Men's Bible Study Q&A») and remain subject to a human verification pass; machine transcription (faster-whisper `base.en`, whole episode; `small.en` precision windows on the two load-bearing passages) was used as a locator only.

**Content (timestamps within the episode)**

| Time | Wording (machine-transcribed, precision-checked) |
|---:|---|
| 3:28 | «Love gives, lust takes.» |
| 3:33–3:43 | «So if you really love someone, you want to give, you want to sacrificially give to meet their highest good. And lust takes for self-satisfaction and self-pleasure.» |
| 3:50–4:08 | orange analogy — the fruit is squeezed for its juice and then thrown away; «there are guys like that in relationships with women and then just discard them. That's just lust.» |
| 4:10 | «love desires to do anything and everything to seek that person's highest good» |
| 4:18–5:44 | the discernment list: the person «would have to be a believer»; ability to care for and support her; her family and parents as a consideration «not a deal killer»; how long you have known her; «can live with» vs «cannot live without»; «Does this person make you want to live for God and live for Christ?»; reciprocal input; «Are you equally yoked?» |
| 13:00–16:20 | exposition of Ephesians 5 (submission, headship, the husband as head, love as Christ loved the church, sanctification «by the washing of the water with the word») |
| 18:26–18:38 | «if you're a man looking for a wife, then make sure that she is a godly woman, that she is a respectful woman, that she's a submissive woman, that she submits to God's Word… that she understands the role in marriage and wants to honor Christ in everything» |

**Analytical note (interpretation, clearly labelled).** The episode is dated **May 2022**, i.e. inside the approximate window of the relationship later confessed (Phil Johnson's «about five years» implies roughly 2019–2024). In that window Lawson publicly taught that love gives and lust takes, and that a man should marry only a believer who makes him want to live for Christ. The corpus records the contrast as a fact about dates and content; it does **not** claim that Lawson was consciously describing himself, that the teaching was insincere, or that the relationship was identical with the pattern he warned against.

---

## 3. 2017 Ligonier Q&A — a live-dossier claim corrected

The live dossier claimed that in the 2017 National Conference Q&A Lawson «сам зачитывает вопрос» о лжеучителе and «модерировал» the discussion. The publisher captions of the official Ligonier video (`MfnYgz_e17M`) show the opposite:

- **all nineteen questions in the session are read by the moderator (`LARSON:`)** — including the false-teacher question at **00:32:22**;
- **Lawson speaks only three times** in the whole 44:36 session: 00:02:45 (on the meaning of «Reformed»), 00:16:55 (a one-line aside to MacArthur), and 00:38:08;
- the false-teacher answers came from **Sproul** (00:32:54: a false teacher is one who teaches falsehood), **Mohler** (00:33:11–00:33:50: the New Testament distinction between a false teaching and a person who is uncorrectable), and **MacArthur** (00:34:11–00:34:40: the non-negotiable essentials; 00:35:00–00:35:07: error versus heresy);
- Lawson's only contribution near this topic is at **00:38:08–00:38:31**, on a later question: he affirms MacArthur's essentials and says that if you cannot agree on them «you're really outside the faith».

The correction has been applied in the live dossier: dated editor's notes in `04_PRIOR_TEACHING_QA_AUDIT…` and `RESEARCH_DOSSIER.md` (superseded wording preserved there as editorial history), and a corrected sentence in the publication draft `ARTICLE_VK.md` (which carries no editorial-history apparatus; the superseded text remains in the repository history).

**Publication effect:** any sentence of the form «Лоусон сам задал/зачитал вопрос о лжеучителе» is no longer publishable. The accurate, still-strong formulation is: he *stood inside* that discussion environment, heard the definitions from Sproul/Mohler/MacArthur, and personally affirmed the essentials-and-«outside the faith» boundary — while his own case later turned out to concern life rather than doctrine.

---

## 4. Ligonier London 2023 — playlist state and the re-upload

**Playlist state (captured 2026-09-27, `PL30acyfm60fU3GItDZp4LYNpsHQeuiSs1`, 13 items).** The official «Pilgrims and Exiles» playlist contains the main sessions by Mbugua, Johnston, Parsons, Reeves, Nichols and Ferguson, the panel, the two main-conference Q&As (both including Lawson), and the pre-conference sessions by Reeves, Ferguson, Parsons and the pre-conference Q&A (including Lawson) — but **neither of Lawson's solo sessions**: «The Word of God for Exiles» (main) and «Preach the Word» (pre-conference) are absent. Combined with the 404s on the corresponding ligonier.org pages (recorded in `06`), the state is: his solo sessions are missing from both the site and the playlist, while his Q&A appearances remain. Recorded as an observation; **no motive is inferred**, and the counter-explanation (the solo sessions may never have been uploaded to this playlist) cannot be excluded from the outside.

**Re-upload.** `Ey7kYHEpcyo`, «The Word of God for Exiles - Dr. Steve Lawson», channel *The Reformed Man*, uploaded **2025-03-12**, 2668 s (44:28), 11 views, no description. Auto-captions were captured (291 633 B; `cap_Ey7kYHEpcyo.en.vtt`). Content confirmed: an exposition of **1 Peter 1:22–25** with the stated title «The Word of God for Exiles» — i.e. the missing main session. Notable passages (auto-captions, locating only): the Word of God «possesses the right to rule our lives… to bind our conscience» (~14:08–14:12); the Word as authoritative command rather than suggestion; the concluding preaching material. **Class: B1 derivative** — third-party carrier; **not quote-safe** until an official copy or independent corroboration is obtained.

---

## 5. 2026 reception — additions (commentary tier)

- Paul Washer (channel *Sola Scriptura / Keith Thompson*), «Is Steven Lawson's New Book a Slap in the Face to the Church?», 12:08, ~2026-09-23 (`4kiWzPN7RbU`): «My personal opinion regarding Steven Lawson is that the man is lost… I do not believe that Steven Lawson is regenerate… not because he slid into sin… because of how he's handling life after the sin was exposed»; describes the book as «the first step» toward returning to ministry. Opinion; report only with attribution.
- Justin Peters, «Didaché — Steve Lawson's New Book: Should It Have Been Written?», 48:37, ~2026-09-24 (`t4eGiYDrMpI`); no English captions retrievable.
- «Preaching for God's Glory» published further clips/commentary in the same window (`QXeLdZGhS2g`, `kB3ApzrWfho`, `Phi7zLbDDFE`, and `VFUU4FvfIXM` claiming «Steve Lawson contacted me!!!», ~4 days) — `C`; unverified, do not use as evidence without corroboration.

---

## 6. Open items after this pass

1. Human verification (listen-through) of the two load-bearing 2022 quotations; locate the original Men's Bible Study recording (Trinity Bible Church of Dallas, Thursdays, 2022) if it exists publicly.
2. Ligonier's own copies of the two 2023 Lawson sessions (app, archive.org, broadcaster copies) — the re-upload stays `B1` until then.
3. Unchanged from `06` §6: Trinity and TMS originals; the 2026 book object/page locators; the durable archive of the 2025-03-12 statement; Romans-2 broadcast audio; the VK article.
