# Steven J. Lawson — source ledger — 2026-09-27

**Corpus:** `LAWSON-2024-2026`  
**Status:** `ACTIVE / PUBLICATION_READY_WITH_GUARDRAILS`  
**Policy:** [`../data/repository-evidence-policy-v2.json`](../data/repository-evidence-policy-v2.json)

This ledger records **material sources and discovery leads**, not a claim that every linked page is equally authoritative. Source class, access state, and locator state must be read together.

Legend:

- `A1` participant-created primary record
- `A2` official transcript/report/primary institutional publication
- `A3` official event-specific institutional statement/decision
- `B1` high-quality secondary corroboration
- `C` context/discovery/unverified
- `D` excluded/unreliable

Access: `FULL_OBJECT_VERIFIED`, `PARTIAL_OBJECT`, `CATALOG_ONLY`, `LINK_ONLY`, `NOT_ACQUIRED`.

Locator: `EXACT_LOCATOR_VERIFIED`, `COARSE_LOCATOR_ONLY`, `LOCATOR_MISSING`.

---

## A. Core primary / institutional material

| ID | Date | Source | Class | Access | Locator | Use / notes |
|---|---:|---|---|---|---|---|
| SL-A01 | 2024-10-20 | Grace to You, **Thinking Biblically About Current Events: A Conversation with John MacArthur**, sermon 70-58 — https://www.gty.org/sermons/70-58/thinking-biblically-about-current-events-a-conversation-with-john-macarthur | A2 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | **Anchor source.** Nathan Busenitz asks about internal adversity; MacArthur names Steve Lawson, says he was exposed while in a position he had no right to occupy; behavior in leadership is fatal; theology appeared sound; warns of corrupting influence; conscience "completely scarred over" formulation; still calls Lawson a friend and expresses love/prayer. Need durable timestamp for final quote-safe publication. |
| SL-A02 | c. 2011–2012 | Grace to You, **Practical Concerns in the Local Church: An Interview with John MacArthur** — https://www.gty.org/sermons/print/GTY135/practical-concerns-in-the-local-church-an-interview-with-john-macarthur | A2 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED by phrase | MacArthur: fidelity measured "both in what they say and how they live"; "two ways to be a heretic": doctrinal and moral. General category, **not** a direct Lawson verdict. |
| SL-A03 | 2023-09-19 | Ligonier, **Stream for Free: London Conference** — https://www.ligonier.org/posts/2023-london-conference-messages | A2 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED by session listing | Confirms Lawson pre-conference session **Preach the Word** and conference participation. Does not itself provide full 1 Tim. 4:2 content description. |
| SL-A04 | 2023 | Ligonier, **2023 London Conference: Pilgrims and Exiles** — https://www.ligonier.org/posts/2023-london-conference-pilgrims-and-exiles | A2 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED by session listing | Independent official confirmation of Lawson at conference and pre-conference. |
| SL-A05 | 2025-03-12 | Steven Lawson X post — https://twitter.com/DrStevenJLawson/status/1899912459521319253 | A1 | PARTIAL_OBJECT | COARSE_LOCATOR_ONLY | Participant confession: sinful relationship with woman not wife; betrayal/deception; sole responsibility; claimed repentance, counseling and accountability. Direct platform object should be archived/durably acquired. |
| SL-A06 | 2025-03 | PDF preservation of Lawson statement — https://thechristianworldview.org/wp-content/uploads/2025/03/Steven-Lawson-statement.pdf | B1 preservation of A1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | Full text with account handle/date/time. Strong custody surrogate pending primary archive. |
| SL-A07 | 2026 | *Mercy in the Wilderness: How I Fell & What I Found*, ISBN 9798996167302 | A1 if acquired | NOT_ACQUIRED | LOCATOR_MISSING | **Required acquisition.** Current book-specific interior claims remain dependent on reviewers/catalog copy. |
| SL-A08 | 2024-10-20 | Official audio of Grace to You program 70-58 — `https://mic-development-us5p473zyq-core-4j1au-mediabucket-6bjazokcoje1.s3.us-east-1.amazonaws.com/Audio%2FSermons%2F70_58_db35a2d1dc.mp3` | A2 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (Lawson segment ≈19:00–24:00; key sentences 19:03 / 19:16–19:25 / 19:31 / 22:45 / 22:52–23:01 / 23:49) | Timestamp closure for SL-A01. Custody: `_work/gty70-58.mp3`, sha256 24162964450f397b43663b7674d80965557c23ff6a4265cee3131cfb24ada4dc. ASR used for locating only; wording authority = official GTY transcript. |
| SL-A09 | 2017-03-03 | Official audio, Shepherds' Conference 2017, General Session 14, Steven J. Lawson, *Jesus, The Good Shepherd* — `https://s3.amazonaws.com/media.shepherdsconference.org/2017/SC17-GS-2017-03-03-1530-LAWSONS.mp3` | A2 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (closing appeal 67:01–68:41; "unconverted shepherd" 68:17–68:23) | **Recovery of the original object behind the addendum §2 derivative transcript.** Custody: `_work/sc17_gs14_lawson.mp3`, sha256 195a8c44acc9383b6fc04f27eaef353839d8bfaf8046b3d36bdc34f5de696595. Supersedes the lilys.ai locator ≈01:11:35. See `06_PRIMARY_OBJECT_AND_STATUS_AUDIT_2026-09-27.md` §2. |
| SL-A10 | 2024-09-20 | OnePassion Ministries public statement, archived — `https://web.archive.org/web/20240920233142/https://onepassion.org/` | A3 (archived institutional object) | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (statement block on captured home page) | Closes the P1 OnePassion item. Custody: `_work/custody/onepassion_20240920233142.html`, sha256 a2b350d16e665070884e9165307bee15febcf64c36a48b8eefb88c0d1f60cea5. |
| SL-A11 | 2024-09-27 captures | Ligonier archived session pages for the 2023 London conference (Lawson sessions) — `…/web/20240927034417/…/preach-the-word-pre-conference`; `…/web/20240927115455/…/the-word-of-god-for-exiles` | A2 (archived official pages) | FULL_OBJECT_VERIFIED (title/attribution only; JS shell) | EXACT_LOCATOR_VERIFIED as to title/URL/date; content locator NOT available | Proves title, speaker and page history after Sep 2024; does not contain video id or description text. Custody: `_work/custody/ligonier_*.html`. |
| SL-A12 | observed 2026-09-27 | Ligonier live-site state — all five 2023 London conference pages featuring Lawson return 404; non-Lawson session pages return 200 | B1 (page-state observation) | FULL_OBJECT_VERIFIED as observation | EXACT_LOCATOR_VERIFIED as to HTTP status by URL | Recorded as a fact about the site, no motive inferred. Complements SL-A03/A04 (official pages that still list the sessions). |

---

## B. Initial removal and institutional response

| ID | Date | Source | Class | Access | Locator | Use / notes |
|---|---:|---|---|---|---|---|
| SL-B01 | 2024-09-20 | MinistryWatch, **Steven Lawson Removed from Ministry for ‘Inappropriate Relationship’** — https://ministrywatch.com/steven-lawson-removed-from-ministry-for-inappropriate-relationship/ | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED by quoted announcement | Preserves Trinity announcement: indefinite removal; elders informed of inappropriate relationship; repentance goal; compensation ends. |
| SL-B02 | 2024-09-19 | Not the Bee, contemporaneous Trinity statement copy — https://notthebee.com/article/popular-reformed-preacher-steve-lawson-has-been-removed-from-pastorate-after-an-inappropriate-relationship-with-an-unnamed-woman-was-discovered | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED by block quote | Corroborates original wording. |
| SL-B03 | 2024-09-19 | Charisma, **Steven Lawson Dismissed From Dallas Church Following an ‘Inappropriate Relationship’** — https://mycharisma.com/culture/steven-lawson-dismissed-from-dallas-church-following-an-inappropriate-relationship/ | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED by quote | Additional preservation of Trinity statement. |
| SL-B04 | 2024-09-20 | Charisma, **Steven Lawson Steps Down from OnePassion Ministries** — https://mycharisma.com/culture/steven-lawson-steps-down-from-onepassion-ministries/ | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED by quoted statement | Preserves OnePassion: Lawson confessed inappropriate relationship; sin disqualified him; resigned duties/events cancelled. |
| SL-B05 | 2024-09-23 | Roys Report, **Steve Lawson Resigns from OnePassion Ministries; Questions Remain Unanswered** — https://roysreport.com/steve-lawson-resigns-onepassion-ministries-questions-remain/ | B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Corroborates OnePassion and records Trinity elder Mark Becker response. |
| SL-B06 | 2024-09-25 | Chron, **Texas pastor, 73, had ‘inappropriate’ relationship with woman in 20s** — https://www.chron.com/culture/religion/article/texas-pastor-inappropriate-relationship-19792881.php | B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Quotes TMS/Busenitz communication: elder qualifications, one-woman man, above reproach, permanently disqualified. Also reports OnePassion. Acquire original TMS communication. |
| SL-B07 | 2024-09 | The Christian Worldview / Truth Network episode — https://www.truthnetwork.com/show/the-christian-worldview-david-wheaton/91169/ | B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Reads/preserves OnePassion and TMS wording. Useful corroboration, not substitute for original institutional object. |

---

## C. Phil Johnson / duration / age / disclosure / institutional proximity

| ID | Date | Source | Class | Access | Locator | Use / notes |
|---|---:|---|---|---|---|---|
| SL-C01 | 2024-09-25 | Roys Report, **Steve Lawson Had ‘5-Year Relationship’ with Woman in Her 20s, GCC Pastor Says** — https://roysreport.com/steve-lawson-had-5-year-relationship-with-woman-in-her-20s-gcc-pastor-says/ | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED by preserved wording | Preserves Phil Johnson's deleted X post: approx. five years; late 20s; different state; later deletion/update. Claims require attribution. |
| SL-C02 | 2024-09-25 | ChurchLeaders, **Phil Johnson Claims ... Caught by ‘Girl’s Father’ and Forced To Confess** — https://churchleaders.com/news/497585-phil-johnson-claims-dr-steven-lawson-was-caught-by-girls-father-and-was-forced-to-confess-inappropriate-relationship.html | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED by preserved wording | Preserves Johnson claim that Lawson told elders only after father confronted/threatened exposure; also five-year/romantic/no-literal-fornication claim. |
| SL-C03 | 2024-09-25 | Protestia, **More Details Drop in Steve Lawson Scandal** — https://protestia.com/2024/09/25/breaking-more-details-drop-in-steve-lawson-scandal-she-was-in-her-twenties-developed-over-five-years-no-fornication/ | B1/C | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED by screenshot/quote | Additional preservation of deleted Johnson material. Outlet commentary should not be confused with Johnson's words. |
| SL-C04 | 2024-10-29 | Roys Report, **Steve Lawson Began His ‘Adulterous Affair’ ... When She Was a Student at The Master’s University, GCC Pastor Admits** — https://roysreport.com/steve-lawson-began-his-adulterous-affair-with-woman-when-she-was-a-student-at-the-masters-university-gcc-pastor-admits/comment-page-1/ | B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Quotes Johnson email acknowledging student status during some of period; reports Grace Books employment and employee statement re GCC membership eligibility; reports secretary's concern went to OnePassion employee, not GCC elders. Claims require attribution/care. |
| SL-C05 | 2025-01 | Christian Post, **Pastor Steve Lawson moved out of Texas after resignation: friend** — https://www.christianpost.com/news/pastor-steve-lawson-moved-out-of-texas-after-resignation-friend.html | B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Repeats Johnson claim: mid-20s; Master's student during part of affair; about five years; father caught them. Also Clint Archer comments about Tennessee/counseling. |
| SL-C06 | 2024-09-25 | Christian Research Network preservation — https://christianresearchnetwork.org/2024/09/25/more-details-drop-in-steve-lawson-scandal-she-was-in-her-twentiesdeveloped-over-five-years/ | C/B1 mirror | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Discovery/corroboration only; derivative of Johnson/Protestia reporting. |

**Privacy rule:** do not propagate images, name, address, family identifiers, or other deanonymizing material from these pages into the Research corpus unless a future authority explicitly finds it necessary. The analytical issue is accountability, not identification.

---

## D. December 2024 meeting / 2025 correction and public confession

| ID | Date | Source | Class | Access | Locator | Use / notes |
|---|---:|---|---|---|---|---|
| SL-D01 | meeting 2024-12-11; published 2025-01-10 | Protestia, **Exclusive: Steve Lawson Claims To Be Repentant, But Trinity Elders Aren't Buying It** — https://protestia.com/2025/01/10/exclusive-steve-lawson-claims-to-be-repentant-but-trinity-elders-arent-buying-it/ | B1/C | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Leaked meeting snapshot. **Mandatory companion fact:** editor's update says credible knowledgeable sources materially refuted claims and said Lawson was being shepherded in Tennessee and cooperating. Never cite first half without update. |
| SL-D02 | 2025-03-13 | Christian Post, **Steven Lawson breaks silence about inappropriate relationship** — https://www.christianpost.com/news/steven-lawson-breaks-silence-about-inappropriate-relationship.html | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED by quoted post | Corroborates X statement and links context. |
| SL-D03 | 2025-03-13 | Aquila Report, **Steve Lawson's Official Confession** — https://theaquilareport.com/steve-lawsons-official-confession/ | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | Full statement copy. |
| SL-D04 | 2025-03-13 | MinistryWatch, **Steve Lawson Breaks Silence** — https://ministrywatch.com/steve-lawson-breaks-silence/ | B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Independent contemporary report. |
| SL-D05 | 2025-03-13 | Evangelical Times, **Dr Steven Lawson writes ‘shattered heart’ letter of repentance** — https://www.evangelical-times.org/dr-steven-lawson-writes-shattered-heart-letter-of-repentance/ | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED by full text | Full-copy corroboration. |
| SL-D06 | 2025-03-12 | Protestia, **Steve Lawson Breaks His Silence** — https://protestia.com/2025/03/12/steve-lawson-breaks-his-silence/2/ | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | Includes direct X URL and full statement; commentary notes what letter does/doesn't address. |

---

## E. Lawson's earlier teaching: holiness, conscience, hypocrisy, pastoral life

| ID | Date | Source | Class | Access | Locator | Use / notes |
|---|---:|---|---|---|---|---|
| SL-E01 | 2014-03-07 | Conference notes PDF, **Session 8 — Steve Lawson — The Costly Discipline of a Godly Pastor, 1 Timothy 4:7b–10** — https://wordsofgrace.blog/wp-content/uploads/2014/03/8-lawson.pdf | B1/C | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Notes summarize Lawson stressing personal holiness/purity as vital to ministry. Not official transcript; no verbatim public quote without checking audio/original. |
| SL-E02 | 2018 copy of 2014 material | The Narrowing Path, **The Costly Discipline of a Godly Pastor by Steven J. Lawson** — https://thenarrowingpath.com/2018/05/31/the-costly-discipline-of-a-godly-pastor-by-steven-j-lawson/ | C | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Discovery/corroboration. |
| SL-E03 | 2023-09-19 | HopeLife video card, **Steven Lawson: Preach the Word (Pre-Conference)** — https://www.hopelife.org/watch/decj3vqcda0-steven-lawson-preach-the-word-pre-conference/20230919/ | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED as page description; video timestamp missing | Identifies content as 1 Tim. 4:2, hypocrisy of liars, branded/seared conscience, plus preaching/reproof. Says content belongs to Ligonier and identifies publication date. Pair with official Ligonier SL-A03. |
| SL-E04 | 2020 event schedule | Ligonier Events, 2020 West Coast Conference schedule — https://events.ligonier.org/2020-west-coast-conference-seattle/schedule/ | A2 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | Lawson session **Sound Teaching (2 Timothy 4:3)**; context for long-standing emphasis on sound doctrine. |
| SL-E05 | 2020 event schedule | same official schedule | A2 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | Lawson **Our Gracious God** / **A Heart for the Nations**; latter explicitly warns about hypocrisy in Jonah's attitude. Context only. |
| SL-E06 | 2012 | Scottish Reformed Conference audio index — https://www.scottishreformedconference.org/resources-2/audio/ | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED by listing | Lawson session **A God-Centred Life**; context/discovery only. |
| SL-E07 | undated index | Scribd, Romans commentaries/sermons index — https://de.scribd.com/document/966176131/Romer-Kommentare-Predigten | C | PARTIAL_OBJECT | COARSE_LOCATOR_ONLY | Discovery lead listing Lawson Romans 2 messages: **The Moralist Condemned**, **Condemned by the Law**, **True and False Circumcision**. Find official OnePassion/audio before quoting. |
| SL-E08 | 2026 secondary sermon | Elim Bible Chapel, Romans 2:17–29 — https://elimbiblechapel.com/2026/03/08/glorifying-god-from-the-heart-romans-217-29-mark-ottaway/ | C | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Uses Lawson as contemporary illustration and quotes his public confession; not evidence for original Lawson teaching. Context only. |

---

## F. Broader MacArthur false-teacher / life-and-doctrine framework

| ID | Date | Source | Class | Access | Locator | Use / notes |
|---|---:|---|---|---|---|---|
| SL-F01 | official GTY | **Practical Concerns in the Local Church** — https://www.gty.org/sermons/print/GTY135/practical-concerns-in-the-local-church-an-interview-with-john-macarthur | A2 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | Primary "doctrinal heretic / moral heretic" wording. |
| SL-F02 | 2019 | GTY, **God's Demand for Discernment** — https://www.gty.org/sermons/TM19-11/gods-demand-for-discernment-john-macarthur | A2 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | MacArthur on false teaching, discipline, and 2 Tim. 2/Jude categories. Supporting context, not Lawson-specific. |
| SL-F03 | official GTY study guide | **The Pathology of False Teachers** — https://www.gty.org/resources/study-guides/chapters/54-45/the-pathology-of-false-teachers | A2 | LINK_ONLY | LOCATOR_MISSING | Discovery lead for MacArthur's long-term false-teacher/conscience framework; fetch exact object before article quotation. |
| SL-F04 | 2019 anniversary interview | GTY, **Fighting the Good Fight: Fiftieth-Anniversary Interview** — https://www.gty.org/sermons/GTY173/fighting-the-good-fight-fiftieth-anniversary-interview-with-john-macarthur | A2 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | MacArthur argues a professed Christian life cannot be severed from repentance/changed life; useful theological context but not Lawson-specific. |

---

## G. 2026 book: catalog, authenticity, reviews

| ID | Date | Source | Class | Access | Locator | Use / notes |
|---|---:|---|---|---|---|---|
| SL-G01 | catalog date 2026-08-20 | YES24, **Mercy in the Wilderness** — https://www.yes24.com/product/goods/196694745 | B1 catalog | CATALOG_ONLY | EXACT_LOCATOR_VERIFIED by metadata fields | ISBN 9798996167302; 124 pp.; lists But God Press; carries marketing copy "My giftedness exceeded my godliness" / "unflinching confession." |
| SL-G02 | 2026 | AbeBooks ISBN record — https://www.abebooks.com/products/isbn/9798996167302 | B1 catalog | CATALOG_ONLY | EXACT_LOCATOR_VERIFIED by metadata | Lists 122 pp. and publisher "Steven Lawson". Metadata conflicts with YES24; do not silently harmonize. |
| SL-G03 | 2026-09-23 | Evangelical Times, **Is Steven Lawson's ‘confession book’ just an AI hoax?** — https://www.evangelical-times.org/is-steven-lawsons-confession-book-just-an-ai-hoax/ | B1/C | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Captures initial authenticity skepticism. Superseded in part by later primary-source confirmation reports. Useful chronology, not final verdict. |
| SL-G04 | 2026-09-24 | Evangelical Dark Web, **Why Steve Lawson's Book Is Not A Grift (Per Se)** — https://evangelicaldarkweb.org/2026/09/24/why-steve-lawsons-book-is-not-a-grift-per-se/ | B1/C | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Says authenticity confirmed since Monday; commentary cautiously pessimistic. Treat confirmation report as B1 pending named primary. |
| SL-G05 | 2026-09-21 | Evangelical Dark Web, **Steve Lawson Returns With New Book** — https://evangelicaldarkweb.org/2026/09/21/steve-lawson-returns-with-new-book/ | C/B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Early discovery, sample/price/page count, social endorsement lead; opinion-heavy. |
| SL-G06 | 2026-09-21 | Protestia, **Steve Lawson Releases ‘Unflinching Confession’ Book Detailing Road To Adulterous Affair** — https://protestia.com/2026/09/21/steve-lawson-releases-unflinching-confession-book-detailing-road-to-adulterous-affair/ | B1/C | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Reproduces book/sample promotional passages and ministry-success list. Use carefully; direct book acquisition preferred. |
| SL-G07 | 2026-09-25 | Protestia, **Mercy in the Wilderness: A Public Testimony That Says Too Little** — https://protestia.com/2026/09/25/mercy-in-the-wilderness-a-public-testimony-that-says-too-little/ | B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | **Key full review.** Reviewer says primary sources confirmed authorship; reports opening "details ... not important"; overloaded schedule, neglected communion, pride, complacency, harsh preaching, wife neglect; concrete refused marriage counseling due pride; critiques repetition/self-focus/lack of structural accountability. Page locators unavailable until book acquired. |
| SL-G08 | 2026-09-25 | ResponsiveReiding, **Steve Lawson's – Mercy in The Wilderness – Some thoughts** — https://responsivereiding.com/2026/09/25/steve-lawsons-mercy-in-the-wilderness-some-thoughts/ | B1/C | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | More sympathetic counter-review: says Lawson owns responsibility; distinguishes writing from pastoral restoration; questions wisdom/timing without inventing biblical prohibition. Useful balance. |
| SL-G09 | 2026-09-23 | The Wartburg Watch, **Steven Lawson ... Wrote a Book. Was It a Confession or an Excuse?** — https://thewartburgwatch.com/2026/09/23/steven-lawson-does-what-these-guys-often-do-he-wrote-a-book-was-it-a-confession-or-an-excuse/comment-page-1/ | C | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Critical commentary/discovery. Opinion source; never sole support for factual claims. |

---

## H. Additional contextual / corroborative reporting

| ID | Date | Source | Class | Access | Locator | Use / notes |
|---|---:|---|---|---|---|---|
| SL-H01 | 2024-09 | TruthScript, **The Fall of a Leader: Lessons from Steve Lawson's Removal** — https://truthscript.com/church/the-fall-of-a-leader-lessons-from-steve-lawsons-removal/ | C/B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Early contextual reaction; notes removal from institutional websites. Not needed for key factual claims. |
| SL-H02 | 2024-09-27 | MinistryWatch podcast episode 401 — https://ministrywatch.com/ep-401-steve-lawson-steve-morgan-and-the-network-and-vince-bantu/ | B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Contemporary roundup; corroborative only. |
| SL-H03 | 2024 year-end | Roys Report Lawson investigation index — https://roysreport.com/investigations/steve-lawson-trinity-bible-church-of-dallas/ | B1 index | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED as index | Useful map to Roys reporting; underlying articles carry the claims. |
| SL-H04 | 2025-03 | ChurchLeaders, **Steven Lawson Issues First Public Statement Since Admitting to Affair** — https://churchleaders.com/news/507673-steven-lawson-speaks-publicly-for-the-first-time.html/2 | B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Corroborates confession/accountability language. |
| SL-H05 | 2025-03 | Christian Research/BishopAccountability mirrors | C/B1 mirror | PARTIAL_OBJECT | COARSE_LOCATOR_ONLY | Redundant preservation only; prefer original reports above. |

---

## I. Sources deliberately *not* promoted to factual authority

The research pass encountered many blogs, social-media reactions, YouTube commentary, anonymous claims, and theological hot takes. They can suggest search terms but do not belong in the factual spine merely because they are rhetorically useful.

Examples of claims requiring stronger evidence before use:

- categorical statements that Lawson was never regenerate;
- claims that a "seared conscience" proves non-regeneration in every case;
- claims of criminality or legally defined pastoral abuse without a competent legal/source basis;
- assertions about the woman's motives or spiritual condition;
- claims that Grace Community Church or The Master's institutions knowingly covered up the relationship before September 2024;
- claims that Lawson's 2026 book was AI-generated, after later reports of confirmed authorship;
- assertions that the marriage has definitively failed or definitively been restored, absent direct reliable evidence.

These remain `C/D` until independently substantiated.

---

## J. Publication-critical source bundle

A final article can be built predominantly from a small high-value bundle:

1. **GTY 70-58 (2024-10-20)** — MacArthur/Busenitz direct post-scandal discussion.
2. **GTY GTY135** — MacArthur's general doctrine/life and moral-heretic category.
3. **Ligonier 2023 London official page** + **surviving Lawson video card** — *Preach the Word* / 1 Tim. 4:2 conscience-hypocrisy connection.
4. **Lawson March 12, 2025 statement** — direct public confession.
5. **Trinity / OnePassion / TMS preserved statements** — institutional disqualification framework.
6. **Roys Report Sep/Oct 2024** — Johnson-derived duration/age/disclosure/student-status claims, always attributed.
7. **2026 book catalog + full critical review + sympathetic review** — current book context with opposing evaluations.

Everything else should support, not drown, the argument.

---

## K. Open source-acquisition queue

Priority order:

- `P0` exact GTY timestamp for Lawson segment and conscience sentence;
- `P0` complete lawful copy of *Mercy in the Wilderness* with page locators;
- `P0` direct Ligonier/YouTube *Preach the Word* video/transcript and exact 1 Tim. 4:2 timestamp;
- `P1` Wayback/direct archived Trinity Sept. 19, 2024 statement;
- `P1` Wayback/direct OnePassion statement;
- `P1` original TMS/Busenitz email/official statement if publicly available;
- `P1` official OnePassion archive/audio for Lawson's Romans 2 exposition;
- `P2` durable archive of Lawson's March 12, 2025 X post;
- `P2` any on-record later statement from Lawson's pastors/elders that clarifies accountability without invading private-family matters.


---

## L. 2026 public-status sources (pass of 2026-09-27)

| ID | Date | Source | Class | Access | Locator | Use / notes |
|---|---:|---|---|---|---|---|
| SL-L01 | 2026-07-20 | Protestia, **Steve Lawson Briefly Appears As Conference Speaker, Then Is Purged From Website** + update — https://protestia.com/2026/07/20/steve-lawson-briefly-appears-as-conference-speaker-then-is-purged-from-website/ | B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Records the listing and its removal within hours; update states organizers advertised without his knowledge/consent and that he declined. |
| SL-L02 | 2026-07-20 | Protestia, **Exclusive: Steve Lawson Not Speaking at Upcoming Preaching Conference** — https://protestia.com/2026/07/20/exclusive-steve-lawson-not-speaking-at-upcoming-preaching-conference/ | B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | States the invitation and the decline; identifies the conference body (TBMEC, a regional body of the National Baptist Convention). |
| SL-L03 | 2026-07-20 | ChurchLeaders, **Disgraced Preacher Steven Lawson Removed From Conference Lineup After Declining Speaking Invite** — https://churchleaders.com/news/2220300-steven-lawson-contending-for-the-faith-speaking.html | B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Independent contemporary corroboration. |
| SL-L04 | 2026-07-21 | JubileeCast, **Steven Lawson Quietly Removed From Pastors Conference After Organizers' Mistake** — https://www.jubileecast.com/articles/38109/20260721/steven-lawson-quietly-removed-from-pastors-conference-after-organizers-mistake.htm | B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Corroboration; frames the comeback question. |
| SL-L05 | 2026-09-23 | Phil Johnson on X (authorship confirmation; criticism of reinsertion and pricing) — https://x.com/phil_johnson_/status/2102909077630370285 | A1 (participant post, not yet independently archived) | LINK_ONLY / PARTIAL_OBJECT | COARSE_LOCATOR_ONLY | Direct link preserved via SL-L06; full text not yet captured in custody. |
| SL-L06 | 2026-09-24 | WORLD / The Sift, **Pastor affirms Steven Lawson's authorship of scandal memoir** — https://wng.org/sift/pastor-affirms-steven-lawsons-authorship-of-scandal-memoir-1790267569 | B1 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (quotes Johnson; links to Johnson, Peters and reaction posts) | Strongest current confirmation path for book authenticity; also lists public reactions. |
| SL-L07 | 2026-09 | Justin Peters, Facebook post claiming the writing style suggests AI — https://www.facebook.com/JustinPetersMin/posts/1596058042563155/ | C | LINK_ONLY | COARSE_LOCATOR_ONLY | Public disagreement; do not promote without stronger material. |
| SL-L08 | 2026-09-24 | Evangelical Dark Web, **Why Steve Lawson's Book Is Not A Grift (Per Se)** — https://evangelicaldarkweb.org/2026/09/24/why-steve-lawons-book-is-not-a-grift-per-se/ | C/B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Opinion; useful for mapping the "return to platform" debate; references the July conference episode. |
| SL-L09 | 2026-07 | Contending for the Faith conference site — https://thecontendingconference.com/ | C/B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | The listing that contained Lawson's name has been corrected; current site lists the November 3–5, 2026 event in Southaven, MS. |

---

## O. Caption-route pass (2026-09-27)

The YouTube caption route reopened in this pass (`yt-dlp` subtitle downloads succeed; publisher captions are human-made and carry speaker labels; auto-captions are locating-only). New objects:

| ID | Date | Source | Class | Access | Locator | Use / notes |
|---|---:|---|---|---|---|---|
| SL-M01 | 2022-05-09 | *Truth Transforms* episode «Should I Marry Her? \| Steve Lawson Answers \| Men's Bible Study Q&A» (Preaching for God's Glory / preachingforgodsglory.org) — audio `TT00027_Lawson+on+Marriage_FINAL.m4a`, 18 799 442 B, 21:32 | A3/B1 (third-party published episode carrying Lawson's own audio) | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (episode timestamps; see `08_…` §2) | **Top transcript target — acquired.** Carrier caveat applies; human verification pending. sha256 5fbac8… |
| SL-M02 | 2017 | Ligonier Ministries official video `MfnYgz_e17M` (2017 National Conference Q&A), publisher captions with speaker labels | A2 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (00:32:22 moderator; 00:32:54 / 00:33:11–50 / 00:34:11–40 / 00:35:00–07 answers; 00:38:08–31 Lawson) | Basis of the attribution correction (L-038); supersedes the live-dossier claim. sha256 c657340d… |
| SL-M03 | 2026-09-27 | Official Ligonier YouTube playlist «Pilgrims and Exiles» `PL30acyfm60fU3GItDZp4LYNpsHQeuiSs1` — 13 items; Lawson solo sessions absent, Q&A appearances present | B1 (observation) | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (item list snapshot) | Page/playlist-state only; no motive. sha256 de1a38c2… |
| SL-M04 | 2025-03-12 upload | Re-upload «The Word of God for Exiles - Dr. Steve Lawson», channel *The Reformed Man*, `Ey7kYHEpcyo`, 2668 s, auto-captions 291 633 B | B1 (derivative carrier) | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY (auto-captions) | Research lead for the missing London-2023 main session (1 Pet 1:22–25); not quote-safe. sha256 482540e2… |
| SL-M05 | 2026-09 | Paul Washer commentary «Is Steven Lawson's New Book a Slap in the Face to the Church?» (`4kiWzPN7RbU`, 12:08, auto-captions captured) + Justin Peters «Didaché» video (`t4eGiYDrMpI`) + «Preaching for God's Glory» clips incl. «Steve Lawson contacted me!!!» (`VFUU4FvfIXM`) | C/B1 (opinion) | PARTIAL_OBJECT | COARSE_LOCATOR_ONLY | Reception/opinion tier only; the «contacted me» claim is unverified. |
| SL-M06 | 2022 | RSS receipt `https://preachingforgodsglory.org/truth-transforms?format=rss` (82 items; TT00027 enclosure) | A3/B1 (publication receipt) | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (item metadata) | Proves publication date, title, enclosure URL. sha256 12d0bd8d… |
| SL-M07 | 2023 | Ligonier pre-conference Q&A `wuxWNjRANB8` (London 2023) publisher captions | A2 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (topics in description; no 1 Tim 4:2/conscience content found in a full-text scan) | Weakens the earlier hypothesis that the «conscience» theme appears in this Q&A. sha256 e9acc3e2… |

**Guardrail.** None of the caption-derived items above (SL-M01, SL-M04, SL-M05) are quote-safe until the human verification pass required by policy; SL-M02 and SL-M07 are publisher captions (A2) and may be used with exact locators.

---

## P. Лондон-2023: Q&A-расшифровки и объект SermonAudio (2026-09-27, продолжение)

| ID | Дата | Источник | Класс | Доступ | Локатор | Примечание |
|---|---:|---|---|---|---|---|
| SL-M08 | 2023-09-19 (загрузка) | Официальное видео Ligonier Ministries «Questions & Answers with Ferguson, Lawson, Parsons, and Reeves» (2535 с), издательские субтитры с атрибуцией спикеров | A2 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (00:00:32–03:43; 00:15:41–18:35) | Реплики Лоусона извлечены (50 сегментов); sha256 `4b0d69d8…` |
| SL-M09 | 2023-09-19 (загрузка) | Официальное видео Ligonier Ministries «Questions & Answers with Ferguson, Johnston, Lawson, Nichols, and Reeves» (2490 с), издательские субтитры | A2 | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (00:06:26–06:55; 00:13:41–14:49; 00:25:48–28:50; 00:30:03–30:39) | 41 сегмент; sha256 `6e690e07…` |
| SL-M10 | 2023-10-11 (дата карточки) | SermonAudio, карточка «The Word of God for Exiles» (Sermon ID 10122311204054; 44:28; Category: Conference; Bible Text: 1 Peter 1:23; 2 Timothy 3:16-17; Broadcaster: Grace Audio Treasures; Series: Puritan Devotional) — страница и полное аудио | B1 (сторонняя трансляция; страница + аудио) | FULL_AUDIO_OBTAINED | EXACT_LOCATOR_VERIFIED (по аудио) | Аудио 32 173 613 B, 96 kbps mono, sha256 `6c968109…`, длительность 2668.16 с; тождество с реуплоадом `Ey7kYHEpcyo` подтверждено выборочной сверкой |
| SL-M11 | 2026-09-27 (захват) | SermonAudio, каталог спикера «Dr. Steven J. Lawson Sermons, Series & Articles» (296 записей) | B1 (состояние каталога) | PAGE_STATE | COARSE_LOCATOR_ONLY | Навигационный указатель; sha256 `e3f773f6…` |

**Обновление к SL-M10 (вечер 2026-09-27).** Аудио получено (корректный хост — `cloud.sermonaudio.com`; ошибочно реконструированный `media.sermonaudio.com` отдавал 502). Сверка четырёх выборочных окон (0:00–0:50; 13:50–14:40; 29:55–30:50; 42:30–44:28) совпала по тексту с авто-субтитрами реуплоада `Ey7kYHEpcyo`; тождество двух сторонних копий одной и той же лондонской сессии подтверждено. Первичный объект Ligonier отсутствует — цитаты сессии остаются B1-подкреплёнными (два независимых носителя); см. `09_LONDON_2023_QA_ADDENDUM_2026-09-27.md` §6.

**Guardrail.** SL-M08/SL-M09 — издательские субтитры (A2): цитаты допустимы с точными таймкодами; SL-M10/SL-M11 — только состояние каталога, не первичные объекты; тождество аудио не утверждать до сверки.

---

---

## Q. Образцы страниц книги и статус 2026 года (вечерний проход 2026-09-27)

| ID | Дата | Источник | Класс | Доступ | Локатор | Примечание |
|---|---:|---|---|---|---|---|
| SL-N01 | 2026-09-21 | Protestia, «Steve Lawson Releases 'Unflinching Confession' Book Detailing Road To Adulterous Affair» — статья, воспроизводящая **образцы страниц книги** (несколько абзацев подряд) | B1 (quote-carrier) | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (по извлечённому блоку) | Снимок `pr_0921.html` 367 030 B, sha256 `440f5b2b…`; извлечённый блок 10 678 знаков, sha256 `7b798d19…`. Дословный текст книги: «I could exegete and outline a passage, but I did not apply it to my own life»; «I first lost the battle in my heart before I lost it elsewhere». Номеров страниц нет — цитировать как «выпущенные образцы страниц». |
| SL-N02 | 2026-09-25 | Protestia, «Mercy in the Wilderness: A Public Testimony That Says Too Little» (дубль SL-G07, снимок добавлен) | B1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Снимок `pr_0925.html` 286 037 B, sha256 `f47c184e…` |
| SL-N03 | 2026-09-23 | The Wartburg Watch, «Steven Lawson Does What These Guys Often Do…» | B1/C | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Снимок `ww_0923.html` 136 765 B, sha256 `efa25c77…`; цитирует заявление 2025 г. и книгу; в комментариях — неподтверждённое утверждение со ссылкой на Ф. Джонсона (класс C; не повышать, третьих лиц не называть) |
| SL-N04 | 2026-09-21 | Evangelical Dark Web, «Steve Lawson Returns With New Book» | B1/C | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | Снимок `ewd_0921.html` 259 488 B, sha256 `cae843c8…`; формат — только бумага; об издателе «But God Press»: публичного присутствия нет |
| SL-N05 | 2026-09-27 | Негативный результат розыска + состояние инфраструктуры | — | NEGATIVE_RESULT | — | IA (Wayback) 503/пустые CDX; archive.today недоступен (HTTP 000); Google Books API 429; OpenLibrary книгу не знает; RU/VK-материал не найден (перечень подходов — в `10_…` §5) |

**Обновление к SL-G06.** Тот же материал теперь имеет байтовый снимок и извлечённый дословный блок; статус повышен с COARSE_LOCATOR_ONLY до EXACT_LOCATOR_VERIFIED по извлечённому блоку (номеров страниц по-прежнему нет).

**Guardrail.** SL-N01 цитируется только как «выпущенные образцы страниц книги»; SL-N03/SL-N04 — вторичные разборы, не источник истины; комментарии и слухи из SL-N03 в публикацию не идут.
---

---

## R. Заявление Trinity (реконструкция), статус X-объекта и персистентность OnePassion (проход 2026-09-27, поздний вечер)

| ID | Дата | Источник | Класс | Доступ | Локатор | Примечание |
|---|---:|---|---|---|---|---|
| SL-O01 | 2024-09-19/20 | Заявление старейшин Trinity Bible Church of Dallas — реконструкция текста по носителям: Christian Post, CHVN, The Independent, WFAA, Distractify, Banner of Truth | A3 через B1-носители | FULL_TEXT_RECONSTRUCTED | EXACT_LOCATOR_VERIFIED по носителям (пофразная таблица — `11_…` приложение A) | Пункты 1–4 подтверждены ≥5 носителями; пункты 5–8 (в корпусе отсутствовали) — 1–3 носителями каждый. Оригинальная страница церкви по-прежнему не найдена |
| SL-O02 | 2024-10-14 | Banner of Truth (Warren Peel), «When a Christian Leader Falls» | B1 (институциональная комментария) | FULL_OBJECT_VERIFIED (текст получен извлечением; `curl` → 403, защита от ботов) | страница сайта | Цитирует оба заявления; формула «restoration… even if that means he never stands in a pulpit again»; предупреждение против спекуляций. Учитывать, что текст до событий 2025–2026 гг. |
| SL-O03 | 2025-03-14 … 2025-08-16 | Wayback: снимки X-поста `1899912459521319253` (8 моментов; первый `20250314055735`) | A1-носитель (URL), текст не сохранён | URL_LEVEL_ARCHIVED / TEXT_LEVEL_MISSING | `web.archive.org/web/20250314055735/…` | Мартовские снимки — JS-оболочки (проверены обычный и `id_` режимы). Текст доступен только через B1-носители (SL-A05/SL-D06) |
| SL-O04 | 2025-07-06, 2025-08-16 | Снимки того же URL отдают страницу X «Nothing to see here… this page doesn’t exist» | Состояние объекта | PAGE_STATE | `_work/custody_20260927c/x_20250706011853.html` (5 855 B), `x_20250816121707.html` (5 852 B) | Фиксировать как «на эти даты URL отдавал страницу несуществования»; НЕ утверждать «автор удалил пост» |
| SL-O05 | 2025-01-23 | Wayback: страница «OnePassion Public Statement» с текстом «…disqualified him from ministry…» | A3 (page-state) | FULL_OBJECT_VERIFIED | `web.archive.org/web/20250123081434/https://onepassion.org` (77 097 B) | Заявление оставалось опубликованным минимум до 23.01.2025 — второй момент того же институционального текста |
| SL-O06 | 2026-09-27 | Негативные результаты | — | NEGATIVE_RESULT | — | archive.today: 429/нет ответа; timetravel — соединение не устанавливается; xcancel — HTTP 451; nitter.net / nitter.poast.org — недоступны; `tms.edu` снимков в Wayback нет; у домена церкви только снимок 2019 г. |

**Guardrail.** SL-O01 — реконструкция, не оригинал: цитировать с атрибуцией «заявление старейшин Trinity (19.09.2024), по публикациям носителей»; для пунктов 5–8 — с указанием конкретного издания. SL-O03/SL-O04 — архивное состояние, не вывод о причинах. SL-O02 — до 2025–2026 событий.
---

---

## S. Оригинал заявления Trinity найден; статус X и OnePassion (закрывающий проход 2026-09-27)

| ID | Дата | Источник | Класс | Доступ | Локатор | Примечание |
|---|---:|---|---|---|---|---|
| SL-P01 | 2024-09-19 17:01 UTC (захват) | Internet Archive: снимок главной страницы Trinity Bible Church of Dallas с блоком «ANNOUNCEMENT» — **оригинальное заявление старейшин** | **A3** (архивный снимок официальной страницы) | FULL_OBJECT_VERIFIED | `web.archive.org/web/20240919170126/https://www.trinitybibledallas.org/` (47 823 B; sha256 `5c5e1b98b9ca…`) | Заявление опубликовано блоком на главной, отдельной страницы не было. Точное время публикации 19.09.2024 в пределах суток не устанавливается |
| SL-P02 | 2024-09-14 14:21 UTC (захват) | Internet Archive: снимок главной страницы **до** заявления | A3 (page-state) | FULL_OBJECT_VERIFIED | 43 451 B; sha256 `86d38d8fa48a…` | «Latest Sermon: Doubts from a Dungeon, Dr. Steven J. Lawson, 8 сентября 2024» — последняя проповедь в Trinity по данным сайта |
| SL-P03 | 2024-09-19 23:08; 2024-09-20 09:25; 2024-10-01 04:57 (захваты) | Internet Archive: три дополнительных снимка с заявлением | A3 (page-state ×3) | FULL_OBJECT_VERIFIED | 46 787 / 46 789 / 40 555 B | Блок заявления **побайтово идентичен** первому снимку — правок не было |
| SL-P04 | 2026-09-27 | Извлечённый дословный текст заявления (1 494 знака) | производный объект | FULL_OBJECT_VERIFIED | sha256 `f7d46c8c1d84…`; файл `TRINITY_STATEMENT_VERBATIM_2024-09-19.txt` sha256 `a858c3bacc91…` | Содержит два предложения, отсутствовавших у всех носителей: дата начала служения «January 5, 2018» и «primacy of biblical exposition knit together by various men filling the pulpit each week» |
| SL-P05 | 2026-09-27 | X oEmbed: пост `1899912459521319253` → HTTP 404; аккаунт `@DrStevenJLawson` → HTTP 404; контрольные запросы Protestia → HTTP 200 | Состояние платформы | PUBLICLY_UNAVAILABLE (через публичный сервис X) | `publish.twitter.com/oembed` | Сервис рабочий (контроль), но ни пост, ни handle не отдаются. Не утверждать, кем/когда удалено |
| SL-P06 | 2026-09-27 | Фид подкаста OnePassion «The Bible Study with Steven Lawson» `feeds.simplecast.com/XFCLnrvQ` → HTTP 404 | Состояние распространения | FEED_DEAD | фид; сторонние каталоги: последний выпуск 2024-09-12 (класс C) | Остановка недельного учительского подкаста совпала с падением; эпизоды Romans доступны на сторонних платформах как локаторы |
| SL-P07 | 2026-09-27 | Живое состояние сайта церкви: старый домен 301 → `trinitybibledallas.org`; на главной имя Lawson не встречается; страниц `/news`, `/blog`, `/article`s, `/statement` нет | Состояние страницы | PAGE_STATE | карта сайта 976 URL | Фиксировать как состояние на дату; мотив не приписывать |

**Guardrail.** SL-P01 — архивный снимок официальной страницы: цитировать как заявление старейшин Trinity (19.09.2024) с указанием, что источник — архивная копия главной страницы. SL-P05/SL-P06/SL-P07 — состояния на дату, не выводы о причинах. Носители и реконструкция (`11_…`) сохраняются как сверка; расхождений с оригиналом нет.
---

---

## T. Жизненный цикл страницы «Leadership» и блока заявления (поздний проход 2026-09-27)

| ID | Дата | Источник | Класс | Доступ | Локатор | Примечание |
|---|---:|---|---|---|---|---|
| SL-Q01 | 2024-08-14 21:09 UTC (захват) | Internet Archive: страница «Leadership» Trinity Bible Church of Dallas **до** падения | A3 (page-state) | FULL_OBJECT_VERIFIED | `web.archive.org/web/20240814210908/https://www.trinitybibledallas.org/leadership` (38 560 B; sha256 `5d4f7a9673…`) | Первой строкой «Dr. Steven J. Lawson — Lead Preacher»; далее elders (Posey, Heidelbaugh, Stainback, Becker) и deacons. Институциональное подтверждение роли «Lead Preacher», а не «Elder» |
| SL-Q02 | 2024-09-19 17:01 UTC (захват) | Там же, **в день заявления** | A3 (page-state) | FULL_OBJECT_VERIFIED | 37 901 B; sha256 `b75bb03c32…` | Строка Лоусона отсутствует; состав elders и deacons не изменился. Подтверждено также снимками 20.09, 21.09, 23.09 (без изменений) |
| SL-Q03 | 2024-09-19 … 2024-10-08 (захваты) | Internet Archive: главная страница с блоком «ANNOUNCEMENT» | A3 (page-state) | FULL_OBJECT_VERIFIED | снимки 19.09, 01.10, 06.10, 08.10 (дважды) | Последний известный снимок с заявлением — **08.10.2024 20:38 UTC** (sha256 `94f79c80ad…`) |
| SL-Q04 | 2024-10-15 03:19 UTC (захват) и далее | Там же, без заявления | A3 (page-state) | FULL_OBJECT_VERIFIED | 43 830 B; sha256 `7ee8619435…`; далее снимки 05.11, 25.11, 04.12.2024, 07.01, 09.02, 13.03.2025 — тоже без заявления | Первый известный снимок без заявления — 15.10.2024. Дата снятия — между 08.10 и 15.10.2024; точнее не устанавливается |

**Guardrail.** SL-Q01…SL-Q04 — состояния архивных снимков: допустимо писать «карточка удалена не позднее публикации заявления», «блок заявления был снят между 8 и 15 октября 2024», без объяснения причин и без связывания с иными событиями.
---

---

## U. Спор о членстве и подотчётности (ноябрь 2024; проход 2026-09-27)

| ID | Дата | Источник | Класс | Доступ | Локатор | Примечание |
|---|---:|---|---|---|---|---|
| SL-U01 | 2024-11-08 | Protestia, «Steve Lawson Was Not a Pastor, Elder or Even a Member at Trinity Bible Church? An Update» — изложение подкаста *With All Wisdom* с дословными цитатами | B1/C | FULL_OBJECT_VERIFIED | snapshot `pr_1108.html` (400 033 B; sha256 `1bd163da39a4…`) | Цитаты: «He was not a pastor. He was not an elder… He was not a member of that church»; «the elders… are not the ones managing the Matthew 18 process… because they can't» |
| SL-U02 | 2024-11-14 | *With All Wisdom*, «Regarding G3's Statement About Steve Lawson» — позиция подкаста на собственном сайте | B1 (первично для позиции подкаста) | FULL_OBJECT_VERIFIED | `withallwisdom.org/2024/11/14/…` (snapshot `waw_1114.html`, 214 999 B; sha256 `ff3d59f68214…`) | Ключевое уточнение: речь о **формальном членстве**; их собеседник-сотрудник «waffled»; член церкви не смог подтвердить, что Лоусон прошёл формальный процесс |
| SL-U03 | 2024-11-14 | G3 Ministries (Josh Buice), заявление о членстве | B1 (по носителям; оригинал недоступен — `g3min.org` HTTP 403, архивного снимка нет) | FULL_TEXT_VIA_CARRIERS | цитируется дословно в `ewd_1115.html` (266 323 B; sha256 `9ac5afae…`) и `cl_buice.html` (369 608 B; sha256 `3063f7d5…`) | «The facts are clear—Steven Lawson and his wife are members of Trinity Bible Church. We have verified this information from two sources within Trinity Bible Church» |
| SL-U04 | 2024-11-15 | ChurchLeaders, «'Rumors'—G3 Ministries Founder Josh Buice Verifies…» | B1 | FULL_OBJECT_VERIFIED | snapshot `cl_buice.html` | Изложение позиции G3: удаление материалов Лоусона, снятие со всех мероприятий, оценка «vetting process» |
| SL-U05 | 2024-11-15 | Protestia, «Rubbing Salt in the Wounds» | B1/C | FULL_OBJECT_VERIFIED | snapshot `pr_1115.html` (528 841 B; sha256 `e96584e0…`) | Полемический ответ; фиксирует, что оспаривалось только членство, а не отсутствие старейшинства |
| SL-U06 | 2024-11-27 | Protestia, «Trinity Bible Church Not Doing Matthew 18 on Steve Lawson? Some Updates» | B1/C | FULL_OBJECT_VERIFIED | snapshot `pr_1127.html` (325 811 B; sha256 `2bf2064c…`) | «три главных тезиса» подкаста; цитаты о «rotating list of guest teachers»; заявление ведущих, что они не отказывались от сказанного |
| SL-U07 | 2025-05-12 | G3 Ministries, «Statement Regarding Josh Buice» | A3 (институциональное заявление, архивный снимок) | FULL_OBJECT_VERIFIED | `web.archive.org/web/20250512145032/https://g3min.org/statement-regarding-josh-buice/` (222 057 B; sha256 `a4c55bd1876e…`) | Контекст о авторе заявления о членстве: анонимные аккаунты/платформы, использовавшиеся для клеветы; «presently disqualified from serving as an elder». **Не является доказательством ложности заявления G3 о членстве** |
| SL-U08 | 2026-09-27 | Негативные результаты | — | NEGATIVE_RESULT | — | Публичного уточнения от Trinity по членству/дисциплине не найдено (архивы сайта, СМИ, соцсети); оригинал заявления G3 от 14.11.2024 недоступен (403, нет архивного снимка); аудио эпизода #98 не получено |

**Guardrail.** SL-U01/SL-U02/SL-U06 — позиция одной стороны (подкаст и его носители), не факт; SL-U03 — позиция другой стороны, цитируемая по носителям; SL-U07 — контекст об авторе, не аргумент о существе спора. Любое упоминание членства в статье обязано содержать обе позиции и указание, что церковь публично вопрос не комментировала.
---


---

## V. Книга «Mercy in the Wilderness», эпизод конференции и текущий статус (проход 2, 2026-09-27)

| ID | Дата | Источник | Класс | Доступ | Объект (файл / sha256) | Примечание |
|---|---:|---|---|---|---|---|
| SL-V01 | 2026-08-20 | Каталожная запись на книгу (ISBN 9798996167302): издатель **But God Press**, paperback, print-on-demand, 124 с., ISBN-10 8996167304; schema.org-метаданные совпадают | B1 (коммерческий каталог) | FULL_OBJECT_VERIFIED | — | Подтверждает издателя и POD-характер издания; постраничного содержания (TOC) нет |
| SL-V02 | 2026-09-21 | Protestia — анонс выхода книги | B1/C | FULL_OBJECT_VERIFIED | `_work/custody_20260927d/pr_book_0921.html` (367274 B; sha256 `266a3bc1385a5b96…`) | Описание издателя; публикация образцов страниц |
| SL-V03 | 2026-09-21 | Evangelical Dark Web (Ray Fava) — «Steve Lawson Returns With New Book» | B1/C | FULL_OBJECT_VERIFIED | `_work/custody_20260927d/ewd_book_0921.html` (259488 B; sha256 `f80656df325f5f2d…`) | $14.99 / 122 с.; «But God Press… not actually real, or is extremely private»; «tested the waters of a public return to no avail over the summer» |
| SL-V04 | 2026-09-21 | ChurchLeaders (Dale Chamberlain) — «Steven Lawson Releases 'Unflinching Confession'» | B1 | FULL_OBJECT_VERIFIED | `_work/custody_20260927d/cl_book_0921.html` (359066 B; sha256 `56626ecd5969531d…`) | Факт выхода книги и реакция; связанные материалы CL |
| SL-V05 | 2026-09-21 | JubileeCast — «…repentance or a comeback?» | B1 | FULL_OBJECT_VERIFIED | `_work/custody_20260927d/jc_book_0921.html` (62738 B; sha256 `e6068751cfb6019c…`) | Разграничивает прощение, восстановление общения и квалификацию для руководства |
| SL-V06 | 2026-09-23 | The Wartburg Watch — реакция на книгу | B1/C | FULL_OBJECT_VERIFIED | `_work/custody_20260927d/ww_book_0923.html` (143901 B; sha256 `5af118152a801120…`) | «Customer reviews are 2.1 on Amazon» (волатильно); требование бесплатного распространения |
| SL-V07 | 2026-09-25 | Protestia (David Morrill) — обзор книги «A Public Testimony That Says Too Little» | B1 (обзор) | FULL_OBJECT_VERIFIED | `_work/custody_20260927d/pr_review_0925.html` (286489 B; sha256 `4927a00aae9dbb9f…`) | Единственный содержательный разбор: начальная фраза книги; отказ от семейного консультирования; критика конкретности; два Amazon-профиля автора |
| SL-V08 | 2026-07-20 | Protestia — эпизод с конференцией + обновление с заявлением организаторов | B1/C (+ заявление организаторов) | FULL_OBJECT_VERIFIED | `_work/custody_20260927d/pr_conf_0720.html` (317299 B; sha256 `5b0bb59f879db5f5…`) | Список 26 → 24; «advertised… without his knowledge or consent… he intended to decline» |
| SL-V09 | 2026-07-20 | ChurchLeaders — о снятии с линейки спикеров после отказа | B1 | FULL_OBJECT_VERIFIED | `_work/custody_20260927d/cl_conf_0720.html` (359875 B; sha256 `c49ae2c9f36baf6b…`) | Независимое подтверждение эпизода; полная цитата исповеди 2025 г. из первоисточника-посредника |
| SL-V10 | 2026-07-21 | JubileeCast — о «внутреннем недоразумении» | B1 | FULL_OBJECT_VERIFIED | `_work/custody_20260927d/jc_conf_0721.html` (61070 B; sha256 `c9e0dbb9e29dedd0…`) | Третье независимое подтверждение |
| SL-V11 | 2026-09-22 | ChurchLeaders — «Fallen Pastors: Where Are They Now?» (раздел о Лоусоне) | B1 | FULL_OBJECT_VERIFIED | `_work/custody_20260927e/cl_fallen.html` (363500 B; sha256 `74028d0f0dc0b580…`) | 2026: Нэшвилл, Stephens Valley Church, «no leadership role»; Johnson: «permanently disqualified himself from pastoral ministry»; возраст 75 |
| SL-V12 | 2026-09-27 | Официальный письменный транскрипт GTY 70-58 — сегмент о Лоусоне (извлечён и сохранён как текст; авторитет wording — сама страница GTY) | A2 (официальная страница) | FULL_TEXT_RETRIEVED | `_work/custody_20260927e/GTY_70-58_LAWSON_SEGMENT_VERBATIM.txt` (7010 B; sha256 `eff2072ae7e658cb…`) | Абзацные локаторы к SL-A01/SL-A08; основание новой границы «unfaithful leaders» |
| SL-V13 | 2024-10-20 | Protestia — «John MacArthur Speaks Out on Steve Lawson» | B1/C | FULL_OBJECT_VERIFIED | `_work/custody_20260927d/pr_mac_1020.html` (294460 B; sha256 `9c9e1c1f1170df1d…`) | Пересказ, давший заголовок «That's Enough»; источник сверен с официальным транскриптом (SL-V12) |
| SL-V14 | 2024-10-30 | The Roys Report — о переписке Johnson/Staats: студентка The Master's College в период отношений; Grace Books (2021) | B1 (носитель переписки) | FULL_OBJECT_VERIFIED | `_work/custody_20260927e/trr_tmu.html` (439650 B; sha256 `5297428a15985336…`) | ATTRIBUTED_ONLY: сам e-mail-объект не опубликован целиком |
| SL-V15 | 2024-11-11 | Christian Post — «Photo emerges of woman with Steve Lawson at MacArthur's church» | B1 | FULL_OBJECT_VERIFIED | `_work/custody_20260927e/cp_photo.html` (65192 B; sha256 `82c272a2bf47da4c…`) | Переписка Johnson (секретарь; обещание увольнения старейшины; «not… pastoral abuse as defined by Texas law») **и** опасное отождествление Staats с участницей отношений |
| SL-V16 | 2026-09-27 | YouTube-канал «Steven Lawson Ministries» (@stevenlawsonministries9661, UCU_TblQ1tflE58vJT2IeG5g) — состояние платформы | A1 (наблюдение за публичной платформой) | OBSERVED | `_work/custody_20260927d/ch_UCU_TblQ1tflE58vJT2IeG5g.html` (1193287 B; sha256 `d4cdf344268c4679…`) | 59 видео, 234 подписчика, последние загрузки ≈4 года назад; признаков активности нет |
| SL-V17 | 2024-09-20 | MinistryWatch — об отстранении и снятии материалов (единственный найденный носитель действий Ligonier) | B1 | FULL_OBJECT_VERIFIED | `_work/custody_20260927d/mw_2024.html` (113005 B; sha256 `41ff04c901394bc7…`) | «Ligonier has removed Lawson as a teaching fellow and withdrawn his collection of writings and books»; OnePassion: «lawson had resigned» |
| SL-V18 | 2026-09-27 | Негативные результаты прохода | — | NEGATIVE_RESULT | — | Постраничные локаторы книги не получены (Google Books 429; библиотечные каталоги — нет записи; TOC отсутствует); Amazon 503 и без архивных снимков; официального заявления Ligonier нет; русскоязычный материал/пост ВКонтакте о Лоусоне не найден |

**Guardrail.** SL-V01…SL-V07 — о факте публикации книги и реакции; цитаты книги идут **только через обозревателя** (SL-V07). SL-V08…SL-V10 — документированный эпизод конференции (обязательная формулировка «приглашён, отказался»). SL-V12 добавляет абзацные локаторы к A2-якорю и **границу «unfaithful leaders»** (общее утверждение, не личный ярлык). SL-V14/SL-V15 — ATTRIBUTED_ONLY (переписка по носителям) с запретом на воспроизведение отождествления Staats ↔ участница. SL-V18 — негативные результаты.


---

## W. Институциональный след: состояние собственных страниц организаций (проход 3, 2026-09-28)

| ID | Дата | Источник | Объект (файл / sha256) | Примечание |
|---|---:|---|---|---|
| SL-W01 | 2024-09-16 | Ligonier, страница учителя Steven Lawson — захват | `_work/custody_20260927f/ligonier_lawson_20240916.html` (653858 B; sha256 `b1856691430b6dcd…`) | Полная биография: «founder and president of OnePassion Ministries», «a Ligonier Ministries teaching fellow», «professor of preaching and dean of D.Min. studies at The Master's Seminary», «teacher for the Institute for Expository Preaching», перечень книг |
| SL-W02 | 2024-09-23 | то же — захват | `_work/custody_20260927f/ligonier_lawson_20240923.html` (658080 B; sha256 `629f8b55f8fd8599…`) | Биография усечена до «founder of OnePassion Ministries in Dallas.» — титулы сняты в окне 16–23.09.2024 |
| SL-W03 | 2024-09-27 | то же — захват | `_work/custody_20260927f/ligonier_lawson_20240927.html` (658148 B; sha256 `a834f7b75db2a549…`) | Пояснения о причинах ещё нет |
| SL-W04 | 2024-10-09 | то же — захват | `_work/custody_20260927f/ligonier_lawson_20241009.html` (657103 B; sha256 `0906da965db6acbb…`) | Появляется официальная формулировка: «His content is no longer featured due to violations of our content policy.» |
| SL-W05 | 2026-09-28 | Ligonier, живая страница `learn.ligonier.org/teachers/steven-lawson` | `_work/custody_20260927f/ligonier_lawson_LIVE_20260928.html` (101583 B; sha256 `6863709586c1bb50…`) | Тот же текст по сей день; блок материалов «0 Results». HTTP 200 |
| SL-W06 | 2025-06-26 | то же — захват после переезда домена | `_work/custody_20260927f/ligonier_lawson_20250626.html` (103777 B; sha256 `878f8ae062ef8960…`) | Старый адрес отдаёт 308 → `learn.ligonier.org/teachers/steven-lawson`; страница жива |
| SL-W07 | 2024-07-10 | TMS, страница преподавателя — последний захват 200 | `_work/custody_20260927f/tms_lawson_20240710.html` (168762 B; sha256 `370e0828c56bc3de…`) | «Steven J. Lawson»; «Professor of Preaching & Dean of D.Min.»; «Lawson hosts The Institute for Expository Preaching…» |
| SL-W08 | 2024-09-20 | TMS, тот же адрес — первые захваты после объявления церкви | `_work/custody_20260927f/tms_lawson_20240920.html` (60 B; sha256 `d8531a1ac331414d…`) | HTTP 404 («404 Not Found…»). Окно изменения: 10.07–20.09.2024 |
| SL-W09 | 2026-09-28 | TMS, живое состояние | — | `tms.edu/faculty/steven-j-lawson/` → 404; индекс `tms.edu/faculty/` → 200 без упоминаний Lawson |
| SL-W10 | 2024-09-11 | Reformation Bible College, страница — последний захват 200 | `_work/custody_20260927f/rbc_lawson_20240911.html` (110575 B; sha256 `25f7705c66df3706…`) | «Steven J. Lawson — Visiting Professor… is a visiting professor at Reformation Bible College.» |
| SL-W11 | 2026-09-28 | RBC, живое состояние | — | `reformationbiblecollege.org/faculty/steven-j-lawson` → 404; раздел факультета (сейчас `/academics`) → 200 без упоминаний Lawson |
| SL-W12 | 2024-02-25 | Shepherds Conference, страница спикеров — захват (SC2024) | `_work/custody_20260927f/sc_speakers_20240225.html` (32740 B; sha256 `73367217319f6401…`) | В списке: «Steve Lawson — President, OnePassion Ministries» |
| SL-W13 | 2025-01-14 | Shepherds Conference, тот же адрес — захват (SC2025) | `_work/custody_20260927f/sc_speakers_20250114.html` (21664 B; sha256 `ba6a81ea674a2170…`) | Упоминаний Lawson нет |
| SL-W14 | 2026-09-28 | Shepherds Conference, живой список | — | 200; упоминаний Lawson нет |
| SL-W15 | 2026-09-28 | OnePassion Ministries, доступность сайта | — | TLS-рукопожатие обрывается (`SSLV3_ALERT_HANDSHAKE_FAILURE`); HTTP → Cloudflare 409; `fetch_page` → HTTP 500; архивных захватов главной после января 2025 нет. Наблюдение с оговоркой, без выводов |

**Guardrail.** Все объекты §W — класса A3 (страницы самих организаций) либо наблюдение состояния. Изменения указываются **окнами дат**; формулировка Ligonier «violations of our content policy» приводится дословно и **без конкретизации нарушений**; факт, что страница Ligonier осталась живой, обязателен к учёту. P1 «официальное заявление Ligonier» — **закрыт** (SL-W04/SL-W05).


---

## X. Подотчётность и экклезиология: первичное аудио стороны A и позиция пастора SVC (проход 4, 2026-09-28)

| ID | Дата | Источник | Объект (файл / sha256) | Примечание |
|---|---:|---|---|---|
| SL-X01 | 2026-09-28 | Официальный RSS-фид подкаста *With All Wisdom* (`feeds.buzzsprout.com/1484452.rss`) — 144 позиции | `_work/custody_20260928g/waw.rss` (240842 B; sha256 `49ee70d231f7f66a…`) | Перечень серии #96–#102 с датами и длительностями; A1-объект подкаста |
| SL-X02 | 2024-10-21…11-27 | Серия эпизодов: #96 (21.10), #97 (23.10), #98 (04.11), #99 (06.11), #100 (08.11), #101 (25.11), #102 (27.11) | — | Семь выпусков; ранее в корпусе фигурировал только #98 |
| SL-X03 | 2024-11-04 | Эпизод #98 — первичное аудио (MP3 24 634 300 B; sha256 `920ccdfb…`), расшифровка | `_work/custody_20260928g/waw_98.asr.txt` (43401 B; sha256 `ab2353293ca1cc1e…`) | 563 сегмента, 0–2025 с. Ключевое окно 704–770 с: «not a pastor… not a member» |
| SL-X04 | 2024-11-04 | Эпизод #98 — окно 715–740 с | `_work/custody_20260928g/waw98_key_not_a_pastor_704-770.mp3` (198513 B; sha256 `f4268228485b41bb…`) | Сотрудник церкви «verified everything we said»; «kind of waffled when I said, was he a member» |
| SL-X05 | 2024-11-04 | Эпизод #98 — окна 741–762 с и 965–996 с | `_work/custody_20260928g/waw98_key_1tim5-20_965-1000.mp3` (105525 B; sha256 `583c1039d478becc…`) | «elders… are not the ones managing the Matthew 18 process… because they can't»; требование публичного обличения (Иак 3:1; 1 Тим 5:20) |
| SL-X06 | 2024-11-04 | Эпизод #98 — интерпретация ведущих («lead guest preacher») | `_work/custody_20260928g/waw_98.asr.txt` (43401 B; sha256 `ab2353293ca1cc1e…`) | Их чтение роли Лоусона; не формулировка церкви |
| SL-X07 | 2024-11-27 | Эпизод #102 — первичное аудио (MP3 29 081 912 B; sha256 `c7b36a4c…`), расшифровка | `_work/custody_20260928g/waw_102.asr.txt` (49805 B; sha256 `2cc83dbc316e6384…`) | 681 сегмент, 0–2392 с. Экклезиологическая позиция и прямое слово к Trinity |
| SL-X08 | 2024-11-27 | Эпизод #102 — окно 68–215 с | `_work/custody_20260928g/waw102_key_exposing_structure_068-215.mp3` (441513 B; sha256 `d808d1c490e9989d…`) | «expose Trinity's church structure… at least partially the structure… is responsible»; «dynamic guest preachers» в разделе «what to expect» |
| SL-X09 | 2024-11-27 | Эпизод #102 — окна 350–393 с и 460–512 с | `_work/custody_20260928g/waw102_key_mandate_to_elders_460-512.mp3` (156501 B; sha256 `4f6f94ea6341a175…`) | Евр 13:17; мандат проповеди — старейшинам; «he wasn't even qualified to be preaching in that capacity» |
| SL-X10 | 2025-01-24 | The Roys Report — «Steve Lawson Attends TN Church Where Pastor Believes He Can Be Restored» (обновл. 11.06.2025) | `_work/custody_20260928g/trr_svc.html` (393542 B; sha256 `c4c6aa3f36efeaec…`) | Интервью с Jim Bachmann: не член SVC; дисциплина SVC невозможна; консультанты; старейшины; переезд «дать жене пространство»; поездка в Даллас в январе |
| SL-X11 | 2025-01-24 | Тот же материал — о членстве и дисциплине (третий голос) | `_work/custody_20260928g/trr_svc.txt` (21627 B; sha256 `5c30651587366843…`) | «believes Lawson was, and still is a member at Trinity»; «not under Trinity's discipline»; никто из Trinity не связывался; запрос TRR остался без ответа |
| SL-X12 | 2026-09-28 | Негативные результаты прохода | — | В фиде нет эпизодов 2026 года о Лоусоне; `withallwisdom.org` отдаёт HTTP 403 прямым запросам нашего окружения (страницы читаемы инструментом) |

**Guardrail.** SL-X03…SL-X09 — первичное аудио стороны A: дословные цитаты приводятся с таймкодами и с оговоркой «ASR-локатор, сверять на слух». Формулировка «lead guest preacher» — интерпретация ведущих. «Trinity admits we can't do anything» — их характеристика ответа неназванного сотрудника, не цитата церкви. SL-X10/SL-X11 — слова одного пастора (Bachmann) по носителю TRR: третий голос в споре о членстве, не решение спора. Сырые MP3 не хранятся (URL и sha256 зафиксированы).


---

## Y. Первоначальные формулировки и хронология спора (проход 5, расшифровка #96/#97/#101)

| ID | Дата | Источник | Объект (файл / sha256) | Примечание |
|---|---:|---|---|---|
| SL-Y01 | 2024-10-21 | Эпизод #96 — первичное аудио (MP3 25 905 089 B; sha256 `…`), расшифровка | `_work/custody_20260928g/waw_96.asr.txt` (45827 B; sha256 `bb60fa1610b10190…`) | 629 сегментов, 0–2156 с. Первоначальное изложение обвинений со ссылкой на Phil Johnson |
| SL-Y02 | 2024-10-21 / 2024-10-23 | Эпизоды #96 и #97 — расшифровки | `_work/custody_20260928g/waw_97.asr.txt` (40339 B; sha256 `e3094dd94839d953…`) | 521 сегмент (0–1917 с). Линия «не старейшина → нет подотчётности»; критика тезиса «старейшинам можно доверять» |
| SL-Y03 | 2024-10-21 | Эпизод #96, окно ≈700–790 с | `_work/custody_20260928g/waw_96.asr.txt` (45827 B; sha256 `bb60fa1610b10190…`) | Тезис о членстве звучит как чужой: «some have verified… some have said»; ведущий звонил в церковь — телефон молчит |
| SL-Y04 | 2024-10-21 | Эпизод #96, окно ≈530–575 с | `_work/custody_20260928g/waw_96.asr.txt` (45827 B; sha256 `bb60fa1610b10190…`) | Наблюдение стороны A: четыре недели без публичной коммуникации старейшин; «we just need to move on» — их пересказ, не цитата |
| SL-Y05 | 2024-11-25 | Эпизод #101 — первичное аудио (MP3 30 550 059 B), расшифровка и окна ≈90–203 с | `_work/custody_20260928g/waw_101.asr.txt` (54494 B; sha256 `c08d78b3c55663cd…`) | 724 сегмента, 0–2543 с. Хронология: их материал → «exactly 10 days later» заявление G3 → их ответ через сайт со ссылкой на сотрудника → «eight days» без ответа Trinity |
| SL-Y06 | 2024-11-25 | Эпизод #101, окна ≈141–178 с и ≈420–504 с | `_work/custody_20260928g/waw_101.asr.txt` (54494 B; sha256 `c08d78b3c55663cd…`) | Разграничение формального членства и «членства по умолчанию»; два требования к Trinity; «we are not upset at G3»; контраст с поведением другого пастора (Тони Эванс) как критерий |
| SL-Y07 | 2024-10-02 (обновл. 2026-08-14) | Christian Research Institute (equip.org), Anne Kennedy — «A Christian's Response to Pastor Lawson's Moral Failure», *Christian Research Journal* 47(4), помечено как Viewpoint | `_work/custody_20260928g/cri_lawson.html` (219844 B; sha256 `b956db68c41ebdeb…`) | Внешний институциональный разбор терминологии «moral failing» / «inappropriate relationship» |
| SL-Y08 | 2024-10-23 | Эпизод #97, окно ≈1222–1290 с | `_work/custody_20260928g/waw_97.asr.txt` (40339 B; sha256 `e3094dd94839d953…`) | Опыт одного из их старейшин в программе D.Min. под руководством Лоусона; критика тезиса о доверии старейшинам |

**Guardrail.** SL-Y01…SL-Y08 — первичное аудио стороны A: дословные цитаты с таймкодами, ASR-локатор, сверять на слух. Ключевое уточнение SL-Y03: **21.10.2024 тезис о членстве принадлежал не подкасту** («some have said»), своим он стал 04.11.2024 (#98). Слова «move on» — пересказ ведущих. SL-Y07 — внешний комментарий (Viewpoint), не источник фактов.

## N. Durable receipts

Byte-level receipts (locator, size, SHA-256, class, role) for the objects acquired on 2026-09-27 — GTY 70-58 official audio and transcript, Shepherds' Conference 2017 Session 14 official audio, the archived OnePassion statement and the two archived Ligonier pages — are recorded in [`DURABLE_CUSTODY_MANIFEST.json`](DURABLE_CUSTODY_MANIFEST.json). Raw third-party bytes are deliberately not promoted into Git; the `_work/` paths referenced above are the ephemeral acquisition cache of the 2026-09-27 session. Machine-transcription (ASR) files are locating derivatives only and are never the wording authority.

---

## M. Updated acquisition queue (supersedes section K statuses)

- `P0` complete lawful copy of *Mercy in the Wilderness* with page locators (or page-verified excerpts).
- ~~`P0` 2022 Men's Bible Study Q&A «Should I Marry Her?» transcript~~ — **audio + transcript acquired (SL-M01); human verification and original-recording search remain.**
- `P0` Trinity Bible Church original September 2024 statement object (Wayback 403/504 as of this pass; keep retrying).
- `P1` durable archive of the 2025-03-12 X statement (archive.today rate-limited; Wayback lacks a capture).
- `P1` official OnePassion/broadcaster objects for the Romans 2 messages.
- `P1` direct video/transcript for the 2023 Ligonier *Preach the Word* (live pages 404; archived pages are JS shells).
- `P2` 2026: clarification whether the book was reviewed by Lawson's current pastors/elders; who holds final authority; disposition of proceeds.
- `P1` RU/VK lead: recently posted Russian-language article/post about Lawson — not yet located; continue targeted search (VK internal search, Russian Christian media, Telegram mirrors).

---

## Z. Canonical current acquisition queue (2026-09-28)

**Operational authority:** `19_CURRENT_STATUS_AND_ACQUISITION_QUEUE_2026-09-28.md`. This section supersedes §K and §M **for present-day queue status only**; those sections remain historical records of earlier passes.

- `PUBLICATION GATE`: no unconditional P0 remains. Any retained book quotation/claim must be either page-verified **or** explicitly carrier/reviewer/publisher-attributed; otherwise remove/rephrase it.
- `P1`: direct/original `Preach the Word` 2023 media/transcript + exact 1 Tim 4:2 locator. Existence, Ligonier publication/distribution, subject matter and a surviving Ligonier-attributed video card are already established.
- `P1`: any public Trinity statement resolving formal membership / discipline; until then bilateral attribution is mandatory.
- `P1`: *With All Wisdom* #99/#100 acquisition/transcription. (`#96/#97/#98/#101/#102` are no longer open.)
- `P1`: original G3 2024-11-14 object; official OnePassion Romans 2 objects; original/public TMS/Busenitz object if available.
- `P1`: remaining unresolved cross-corpus verification objects after the closures recorded in `18_`/`19_`; 2026 accountability-chain objects; actual RU/VK object if that lead is intended for use.
- `P2`: lawful complete book/page locators as an evidence upgrade; later public institutional/accountability statements.

**Resolved statuses that must not reappear as generic OPEN:** GTY 70-58 locators; Trinity original; archived OnePassion statement; 2017 Session 14; Ligonier official status wording; 2022 marriage Q&A; London-2023 Q&As; WAW #96/#97/#98/#101/#102; Nashville pastor position. The 2025 X post is `PUBLICLY_UNAVAILABLE` via the tested public X route; the OnePassion feed is `FEED_DEAD` on the observed date.


---

## AA. External closure audit — 2026-09-28

This section records objects located in the final web audit **after** the bundle's last acquisition pass. It closes or narrows several leads from `18_` and supports the current status in `19_`. These entries do not retroactively change the evidence class of older carrier-based claims.

| ID | Date | Object | Class / access | What it establishes | Guardrail |
|---|---|---|---|---|---|
| SL-AA01 | 2023-09-19 | Ligonier Ministries, **“Stream for Free: London Conference”** — `https://www.ligonier.org/posts/2023-london-conference-messages` | **A1**, live first-party institutional page | Ligonier itself states that all London conference messages were available for free streaming and lists the pre-conference session **“Preach the Word — Steven Lawson.”** | Establishes existence and Ligonier distribution, not the exact spoken wording or timestamp. |
| SL-AA02 | 2023-09-19 | HopeLife, **“Steven Lawson: Preach the Word (Pre-Conference)”** — `https://www.hopelife.org/watch/decj3vqcda0-steven-lawson-preach-the-word-pre-conference/20230919/` | **B1 carrier**, live page explicitly attributing the video to Ligonier | Preserves the session card and description tying the message to **1 Tim. 4:2**, hypocritical liars and a conscience branded/seared as with a hot iron. | Use for subject/content description only until direct media/transcript and exact locator are recovered; no invented verbatim Lawson quote. |
| SL-AA03 | 2025-01-24 | Clint Archer, The Cripplegate, **“Steve Lawson Interview”** — `https://thecripplegate.com/steve-lawson-interview/` | **A2 first-person attributed account**, live full object | Archer says Lawson's counselors were chosen by spiritual leaders and reported to elders/OnePassion; describes the Nashville move, returned book advances and Lawson's understanding that he was permanently disqualified from elder-qualified ministry. | This is Archer's account, not a Trinity institutional statement. Do not use it to resolve the disputed membership/discipline question. |
| SL-AA04 | 2024-09-21 | Jon Benzinger thread preserved by Thread Reader — `https://threadreaderapp.com/thread/1837557542744215815.html` | **B1 carrier of a deleted first-person thread**, full text preserved | Preserves Benzinger's statement that in July 2018 he listened as Lawson lectured on **“28 Tragic Consequences of Sexual Sin in the Ministry.”** | Closes the witness claim only. It does **not** establish the lecture's complete content or all 28 points. |
| SL-AA05 | 2014-10-15 | Herald of Grace, **“The personal life of the preacher”** — `https://heraldofgrace.org/the-personal-life-of-the-preacher/` | **B1 publisher quotation**, live page | Attributes to Lawson the statement that the preacher's personal spirituality/godliness is the foundation of public preaching. | Quote as a published Lawson attribution; do not inflate it into evidence about his private state in 2014. |
| SL-AA06 | 2023-01-25 | Truth Transforms / Apple Podcasts, **“God cares more about your Godliness than your Giftedness \| Steve Lawson to Pastors”** — `https://podcasts.apple.com/nl/podcast/god-cares-more-about-your-godliness-than-your-giftedness/id1595208453?i=1000596592366` | **A2 platform/publisher metadata**, live episode object | Establishes a Lawson-to-pastors episode centered on godliness over giftedness. | The title/description is verified; quote exact spoken wording only from the audio/transcript. |
| SL-AA07 | 2019-11-26 | D. A. Carson, The Gospel Coalition, **“Can a Fallen Christian Leader Ever Be Restored?”** — `https://www.thegospelcoalition.org/article/fallen-christian-leader-restored/` | **A1 author/publisher object**, live text | Carson distinguishes restoration to the Lord/church from restoration to Christian leadership and begins by asking **“Restored to what?”** | Contextual theology only; not evidence about Lawson's facts or repentance. |
| SL-AA08 | 2018-10-30 | Jared C. Wilson, 9Marks, **“Can We Restore Pastors after Sexual Sin: A Longer Answer”** — `https://www.9marks.org/article/can-we-restore-pastors-after-sexual-sin-a-longer-answer/` | **A1 author/publisher object**, live text | Distinguishes restoration to fellowship from restoration/requalification to pastoral office; stresses church testing over time. | Contextual theology only. |
| SL-AA09 | 2009-04-20 | John Piper, Desiring God, **“Is It Possible to Restore a Pastor Who Has Sinned Sexually?”** — `https://www.desiringgod.org/interviews/is-it-possible-to-restore-a-pastor-who-has-sinned-sexually` | **A1 first-party ministry object**, audio/video/transcript | Piper distinguishes immediate forgiveness from the long rebuilding of trust and says a fallen pastor should make no claim on the church for rapid return. | Contextual theology only; Piper's position differs in details from permanent-disqualification views and should not be flattened into consensus. |
| SL-AA10 | 2020-04-24 | John Piper, Desiring God, **“What Sins Disqualify a Pastor for Life?”** — `https://www.desiringgod.org/interviews/what-sins-disqualify-a-pastor-for-life` | **A1 first-party ministry object**, transcript | Further develops Piper's qualification/reputation analysis. | Contextual theology only. |
| SL-AA11 | 2019-03-18 | Albert Mohler, The Gospel Coalition, **“Albert Mohler on Losing a Pastor to Immorality”** — `https://www.thegospelcoalition.org/video/mohler-losing-pastor-moral-failure/` | **A1/A2 published video + edited transcript** | Emphasizes higher standards, concentric accountability and congregational care after pastoral moral failure. | Contextual theology only. The page itself says to check the video before quoting the edited transcript verbatim. |
| SL-AA12 | 2026-09-25 | ResponsiveReiding, **“Steve Lawson's – Mercy in The Wilderness – Some thoughts”** — `https://responsivereiding.com/2026/09/25/steve-lawsons-mercy-in-the-wilderness-some-thoughts/` | **B1 substantive review**, live full object | Provides a more sympathetic counter-reading: sad yet hopeful, emphasizes Lawson's stated personal responsibility while questioning the timing of publication. | A review is not primary proof of disputed historical facts in the book. Use as reception/balance. |
| SL-AA13 | 2024-09 | MinistryWatch, **“Leaders Respond to Steven Lawson's Moral Disqualification”** — `https://ministrywatch.com/leaders-respond-to-steven-lawsons-moral-disqualification/` | **B1 contemporary carrier**, live text | Preserves Austin Duncan's statement that a previously scheduled speaker had **“permanently disqualified himself from pastoral ministry”** and disgraced Christ's name. | Attribution is multi-carrier verified, but a primary conference recording remains preferable for verbatim publication. |
| SL-AA14 | 2024-09 | ChurchLeaders, **“‘Permanently Disqualified’—Dr. Steven Lawson Removed…”** — `https://churchleaders.com/news/497390-permanently-disqualified-dr-steven-lawson-removed-from-the-masters-seminary-and-grace-community-church-websites.html` | **B1 independent contemporary carrier**, live text | Independently preserves the same Austin Duncan wording and conference context. | Corroborates attribution; does not replace a primary recording. |

**Closure effects.** SL-AA01–AA02 downgrade `Preach the Word` from “object not found” to **object/provenance/content established; exact media/transcript locator still open**. SL-AA03 closes the Clint Archer lead as an attributed first-person source. SL-AA04 closes the Benzinger **witness** claim while leaving the lecture itself open. SL-AA05–AA06 close the 2014/2023 godliness discovery leads. SL-AA07–AA11 close the contextual restoration/accountability source lane. SL-AA12 closes the “find a substantive counter-review” lead. SL-AA13–AA14 make the Austin Duncan attribution **multi-carrier verified**, while preserving the primary-recording upgrade.
