# 73 — OPEN VERIFICATION BACKLOG / HEART ARTICLES

**Date:** 2026-07-31
**Branch:** `arena/019fb9de-research`
**Mode:** audit backlog promoted into Research after owner authorized push on 2026-07-31. Initial entries were created in no-push mode; later entries are committed/pushed as repository research.
**Scope:** `СЕРИЯ СЕРДЦЕ` current heart-series research/article dossiers, especially post-V84 publication gate and R1–R9 article-research files.
**Status:** cumulative audit backlog; not a production claim; not a replacement for the source files it references.

---

## 0. What this pass looked for

User request: find what is still **unclosed**, **unverified**, or **not A+ / not fully source-safe** in the heart articles.

Working interpretation for this repo:

- `HOLD`, `PAGE-IMAGE-HOLD`, `BOOK-FULLTEXT-HOLD`, `LIVE-READBACK-HOLD` = evidence boundary remains.
- `НЕ ВЕРИФИЦИРОВАНО`, `кандидат`, `ЧАСТИЧНО`, `secondary aggregator`, `locator-only`, `REQUIRES_*` = not quote-ready.
- `A-` / historical extract / metadata / PDF link without page image = usable for orientation or paraphrase, but not A+ for exact quotation.
- Legacy pre-v48 quote-audit markers are not automatically live risks; V48 closed the 801-row quote-risk queue. This pass focuses on current/open article-writing and post-merge gates.

---

## 1. Current top-level open gates from V84I

Source: `72_V84I_POST_MERGE_TOTAL_AUDIT_AND_CLOSURE_GATES.md`.

### 1.1 Not fully closed current state

V84I final disposition is explicitly:

```text
NOT YET FULLY CLOSED
```

Open closure classes:

| ID | Area | Current status | Why it matters | Next action |
|---|---|---|---|---|
| PM-003 / PM-004 | Site TOC / reading time / progress for `tma-na-serdce` | open in governed Site issue `#509` | Reader navigation and book progress drift; source-of-truth config mismatch | Repair Site config, not runtime DOM patch; verify `34` min and total `727` |
| PM-005 | `/hard-texts/` landing architecture | cleanup path via Site PR `#510` | landing metadata/schema behind current four-chapter book architecture | Derive landing from active book config; verify no stale three-part chrome |
| PM-006 | live release witness | pending | main/source merge is not the same as live promoted bytes | Wait for final cleanup main SHA deployment; read live-release artifact |
| PM-009 | Timothy Rogers provenance | **Research closed as evidence-boundary 2026-08-01; Site issue may still exist** | Google Books is blocked in this sandbox; Michigan EEBO2 text is rights-restricted and cannot replace scan-first provenance | Do not direct-quote/translate Rogers Advice 1/5/6 as A+ until owner supplies/visually verifies scan images; use only as locator/search aid |

### 1.2 Evidence gates intentionally bounded

These do **not** necessarily block current wording, but they are not A+ quote-safe:

| Gate | Meaning | Rule |
|---|---|---|
| `BOOK-FULLTEXT-HOLD` for MLJ book | **closed as evidence-boundary 2026-08-01**: legal full text/page-level access not obtained | Do not quote book text or page numbers; use official MLJ sermon pages only within their own evidence class; not a continuing blocker unless owner provides legal text |
| `PAGE-IMAGE-HOLD` for new PDF quotations | **closed as evidence-boundary 2026-08-01**: parsed text / PDF text is not visual pagination | No new direct PDF quotation without page-image confirmation; for current dossiers use paraphrase or already-open HTML/text anchors only |
| Adams psychiatric generalizations | historical material filtered | `DO-NOT-IMPORT` for broad medical/psychiatric generalizations |
| organic/mixed/referral Adams observations | useful but limited | `LIMITED IMPORT`; no diagnosis/medication/taper/crisis instruction |

V84I’s important rule: **a HOLD is an evidence boundary, not a promise that the held material must be imported.**

---

## 2. Immediate high-priority verification targets

### 2.1 Rogers scan-first closure for `tma-na-serdce` — highest practical source task

Current authority chain:

- V84D supplied EEBO-TCP TOC locators: Preface, Advice 1 / 5 / 6.
- V84I says this still needs scan-first rights/provenance closure because Michigan EEBO-TCP is an encoded edition with redistribution restrictions.

What this pass found:

1. **Google Books has the 1691 scan record** for Timothy Rogers, *A Discourse concerning Trouble of Mind, and the disease of Melancholly*, publisher `T. Parkhurst & T. Cockerill`, 1691, original from the British Library, digitized 2015, length shown as 434 pages. URL:
   `https://books.google.com/books/about/A_Discourse_concerning_Trouble_of_Mind_a.html?id=yMRjAAAAcAAJ`
2. The Google Books accessible page for `pg=PR1` exposes OCR plus page-image links for the Preface and includes the start of **Advice 1**:
   `Melancholly seizes on the Brain and Spirits, and incapacitates them for Thought or Action...`
   URL pattern:
   `https://books.google.com/books?id=yMRjAAAAcAAJ&pg=PR1&output=html_text`
3. A non-primary extraction page reproduces Advice 5 and 6 text, but it must remain auxiliary because the site is not a neutral primary host. URL:
   `https://www.bible.ca/psychiatry/a-discourse-concerning-trouble-of-mind-and-the-disease-of-melancholly-timothy-rogers-1691ad.htm`
4. Wellcome Collection has a 1706 second-edition record via ECCO; useful as alternate edition metadata, not a substitute for the 1691 scan-first closure. URL:
   `https://wellcomecollection.org/works/f6n9nj8n`

Current result after continuation:

```text
ROGERS = CLOSED-AS-EVIDENCE-BOUNDARY / DO-NOT-A+ / DO-NOT-DIRECT-TRANSLATE-FROM-TCP
```

2026-08-01 direct check: Google Books scan/OCR endpoint returned a Google automated-query block in this sandbox; the direct image URL also failed. Michigan EEBO2/TCP fulltext was accessible enough to confirm the item and surrounding text, but its own rights notice is restrictive and therefore it **cannot** serve as the scan-first provenance required by V84I/issue #513. Bible.ca remains secondary extraction only.

Decision: do **not** keep treating this as an open promise to import Rogers. For Research/source discipline, Rogers Advice 1/5/6 are closed as a negative boundary: no A+ direct Russian translations and no page-image claim until the owner or a future pass visually verifies the 1691 scan images and records page/signature locators. Use Rogers only as historical locator/paraphrase support with explicit caveat.

### 2.2 MLJ *Spiritual Depression* full book

Current status after continuation:

```text
BOOK-FULLTEXT-HOLD / CLOSED-AS-EVIDENCE-BOUNDARY / DO-NOT-QUOTE-BOOK
```

Local files with this gate:

- `64_V84A_SOURCE_STATUS_AND_LLOYD_JONES_HOLD.md`
- `65_V84B_DEPRESSION_THEOLOGICAL_PRIMACY_AND_AXIS_CORRECTION.md`
- `66_V84C_EDITORIAL_COMPLETENESS_20PLUS_PRIMARY_PASSES.md`
- `71_V84H_DIRECT_SOURCE_CLEANUP_TRINITARIAN_AND_FINAL_EXACT_HEAD.md`
- `72_V84I_POST_MERGE_TOTAL_AUDIT_AND_CLOSURE_GATES.md`

Decision:

- do not continue hunting quotation websites for this book;
- do not quote book text or page numbers unless owner supplies legal text/owned scan/ebook;
- official MLJ sermon pages may be used only within their own metadata/description evidence class.

### 2.3 Adams PDF page-image gate

Current status after continuation:

```text
PAGE-IMAGE-HOLD / CLOSED-AS-EVIDENCE-BOUNDARY
```

The text may support paraphrase with explicit PDF-text locators, but not new direct quotation until page-image verification succeeds. This is now a negative permission boundary, not an open task to force import.

### 2.4 Goodwin full treatise page-image gate

Current status after continuation:

```text
SHORT-ANCHORS-CLOSED / LONG-QUOTE-PAGE-IMAGE-HOLD / CLOSED-AS-EVIDENCE-BOUNDARY
```

Wesley Center = historical extract, not full treatise. Monergism PDF text has now been read for short Goodwin anchors in R9, but page-image/detailed print locators for new long exact citations remain a boundary. Use the closed short anchors or paraphrase; do not claim page-image verification.

---

## 3. R-file article dossiers: open / not verified / not A+ queue

These are article-building dossiers rather than the already-merged `tma-na-serdce` lane. They were the original audit area to “fill and find”.

**Supersession note 2026-08-01:** this section preserves the early audit map. For current closure status, use the active queue in §8 and the safe-closure ledger in §13. Do not read an old row below as still open when §8/§13 marks it closed, blocked, or closed-as-boundary/no-use.

### 3.1 R1 — regeneration / III.2 `Рождение свыше`

Files:

- `62_R1_REGENERATION_EXEGESIS.md`
- `63_R1_REGENERATION_SYSTEMATICS.md`

Open not-A+ items:

| Item | Current issue | Needed closure |
|---|---|---|
| Carson PNTC / Schreiner NAC / Kruse PNTC locators | closed-as-paraphrase-only 2026-08-01 | no exact quote ambition; use only as position locators unless books opened |
| Bavinck RD IV | exact quote not verified | 1–2 exact paragraphs with edition/page, or paraphrase only |
| Whitefield born-again anecdote/stat | no primary source found; tradition varies | **BLOCKED AS DOCUMENTED FACT**; use only as labelled tradition or omit |
| Gill, *Body of Divinity*, Of Regeneration | needs 2–3 exact paragraphs and 1839 page locators | source extract + locator; clarify John 3:5 no-baptism argument |
| Boston regeneration/change characteristics | partially paraphrased | exact PDF/page split for real/thorough/supernatural/universal change |
| Stott and Sproul | Sproul `watershed` source closed via official Ligonier article 2026-08-01; Stott page remains optional | cite Sproul article; Stott exact TNTC page only if needed |
| Russian 1689 LBCF ch. 10 | translation choice open | choose stable Russian translation or mark own translation |

Priority: **P0** because III.2 is core architecture.

### 3.2 R2 — OT regeneration / Spirit indwelling bonus

File:

- `64_R2_OT_REGENERATION_INDWELLING.md`

Open not-A+ items:

| Item | Current issue | Needed closure |
|---|---|---|
| Hamilton Themelios / TrinJ PDFs | Themelios conclusion and TrinJ spectrum chart now verified | quote exact conclusion/chart from verified HTML/PDF text; no page-image claim |
| Ferguson, *The Holy Spirit* | documented mostly by audio/lectures | 1–2 book quotes with page locators or paraphrase only |
| Hamilton monograph | full book source wanted | legal book access; quote pages from ch. 2, 5–6, conclusion |
| Calvin / Augustine / Gill / Owen locators | some snippets are candidates | exact locator pass for John 7:39 and Pneumatologia/Goold refs |
| Spectrum position D names | not verified | do not name representatives until checked |
| Russian translations of Owen/Ferguson | unknown | bibliography pass |

Priority: **P1** unless the bonus is pulled into main article.

### 3.3 R3 — unregenerate struggle / civil righteousness

File:

- `65_R3_UNREGENERATE_STRUGGLE.md`

Open not-A+ items:

| Item | Current issue | Needed closure |
|---|---|---|
| Calvin Institutes II.3.3–4 | direct CCEL/Beveridge/Battles comparison open | exact source pass; choose English/Russian citation policy |
| Augustine *Contra Julianum* IV.3.25 | Latin/English not directly verified | PL / Fathers of the Church locator or no direct quote |
| `splendida vitia` attribution chain | Marshall article metadata/source not closed | establish whether formula is Augustine or later reception |
| Watson *Godly Man’s Picture* morality aphorism | quote collection only | **DO-NOT-DIRECT-QUOTE** unless primary locator is later found |
| Luther page in Packer/Johnston | page pin missing | edition/page check |
| Charnock / Bavinck / Hodge candidates | not yet verified | optional support quotes, not needed unless article wants them |
| Spurgeon “free will carried...” quote | apocryphal-risk / quote-book only | **DO NOT USE**; use verified Spurgeon sermon substitute |

Priority: **P1**.

### 3.4 R4 — four soils / temporary faith

File:

- `66_R4_FOUR_SOILS.md`

Open not-A+ items:

| Item | Current issue | Needed closure |
|---|---|---|
| Whitefield stony-ground quote | primary location not found | **ATTRIBUTED-ONLY / DO-NOT-DIRECT-QUOTE**; use Spurgeon/Calvin substitutes |
| Calvin Harmony / Luke 8:15 | full paragraph not fetched | CCEL/source readback |
| France NICNT / Carson EBC | page locators needed | print/ebook locators |
| Thomas Taylor 1621 | only title-level currently | Hail & Fire PDF exact paragraphs |
| Russian Calvin translation | page and translation policy open | verify Russian edition |
| Hebrews 6 bonus | deliberately not developed | keep as cross-link candidate, not this article’s full load |

Priority: **P1**.

### 3.5 R5 — two struggles

File:

- `67_R5_TWO_STRUGGLES.md`

Open not-A+ items:

| Item | Current issue | Needed closure |
|---|---|---|
| Owen, *Mortification*, ch. 2 | `Be killing sin...` was marked not verified in this run | **Now found at CCEL `mort.i.v.html`, Chapter II**; ready to patch in source file later |
| Owen continuation “unless he indeed be so” | candidate | exact CCEL/Goold locator |
| Owen builder-on-sand comparison | candidate | exact locator or remove |
| Mead peace of almost-Christian | candidate | PDF paragraph locator |
| Spurgeon on Luke 18 / false repentance | not verified | sermon number/PDF pass |
| Augustine VIII.9.21 | candidate | exact translation/source pass |
| Edwards signs headings | summary verified, exact headings candidates | CCEL/source extraction if headings quoted |

Priority: **P0** because article V.3 is core architecture.

### 3.6 R7a — Word and heart

File:

- `68_R7A_WORD_AND_HEART.md`

Open not-A+ items:

| Item | Current issue | Needed closure |
|---|---|---|
| Metzger on Heb. 4:2 | exact text/rating dropped/no-use | use open-reference variant layer only; do not cite Metzger |
| Lane / O’Brien / Schreiner / Ellingworth / Attridge | closed-as-no-direct-quote 2026-08-01 | do not summarize/cite as checked unless books opened; not a blocker |
| Watson “pandect of divine knowledge...” continuation | candidate | Tolle Lege / primary source check |
| Owen “Without the Holy Spirit we may as well burn our Bibles” | attributed but not found in Owen corpus | either exact Owen locator or use as unattributed/omit; Calvin is safer substitute |
| Gill on Heb. 4:2 | candidate | verify both readings in Gill text |
| Hasidic “words upon the heart” story | attribution open | verify Kotzker Rebbe or present anonymously/omit |

Priority: **P0** because VIII.1 is new core article.

### 3.7 R7b — Pharisee and disciple

File:

- `69_R7B_PHARISEE_DISCIPLE.md`

Open not-A+ items:

| Item | Current issue | Needed closure |
|---|---|---|
| Carson PNTC on John 5:39–40 | exact quote not verified | print/page locator or paraphrase only |
| Lloyd-Jones, *Studies in the Sermon on the Mount* | exact quote candidate | legal book access/page locator |
| Spurgeon self-righteousness quote | exact place not verified, sermon candidates #1949 / #2687 | search Spurgeon PDFs/source |
| Augustine sermon on publican/pharisee | sermon number uncertain | verify Sermo number and translation |
| Cyril on John 5:39 | early witness candidate | exact patristic source only if used |
| Russian Mead/Ryle translations | unknown | bibliography pass |

Priority: **P1**.

### 3.8 R8 — beholding glory / Christ Captor of the heart

File:

- `70_R8_BEHOLDING_GLORY.md`

Open not-A+ items:

| Item | Current issue | Needed closure |
|---|---|---|
| Owen, *Glory of Christ* | all quotes via snippets; chapter locators incomplete | CCEL/PDF exact pass; chapter/page per quote |
| κατοπτριζόμενοι excursus | content exists, editorial decision open | owner/editor choose main text vs footnote/dropdown |
| Belleville bibliography | conflicting data | verify edition details before citing |
| Hughes “expulsive force” quote | suspicious/anachronistic | **BLOCKED-AS-DIRECT-HUGHES-QUOTE**; use Chalmers/Owen/Calvin or anonymous synthesis |
| Spurgeon on 2 Cor. 3:18 | likely material but not found | spurgeongems index/source search |
| MLJ `Reflecting His Glory` | official page metadata/description extracted; no direct sermon quote | audio/transcript not needed unless future owner asks |
| Owen two-books synthesis | editorial synthesis lacks external exact quote | optional: Kapic/Ferguson/Packer intro search |
| theosis angle | dangerous scope creep | do not develop without owner theological decision |
| M’Cheyne “10 looks to Christ” | attribution already flagged as disputed in architecture | verify via Bonar or omit name |

Priority: **P0** because VIII.5 is core capstone.

### 3.9 R9 — Christ of Revelation

File:

- `71_R9_CHRIST_OF_REVELATION.md`

Open not-A+ items:

| Item | Current issue | Needed closure |
|---|---|---|
| Goodwin majesty/tender heart | short anchors closed via Monergism PDF text; long/page-image locators optional | use short anchors only unless page-image pass is done |
| Sproul, *Holiness of God* | official Ligonier quote-page subset closed; aggregator-only lines blocked | use verified Ligonier subset; no book-page claim |
| Ortlund / *Gentle and Lowly* | official Crossway Q&A/article judgment caveat closed; ch.15/lion-lamb wording book-page hold | use Crossway official wording; do not quote ch.15 snippets directly |
| Beale / Mounce on Rev 6:16, 19:13 | not directly used | optional evangelical commentary support |
| Rev 19:13 blood-on-garment option | needs deeper exegetical pass | Beale/Mounce/Osborne comparison |
| Patristic layer | not developed | optional; Victorinus/Irenaeus if owner wants |
| Baucham “sissified Jesus” | not verified | do not use unless primary source found |
| “Spurgeon lion for enemies / lamb for friends” | likely apocryphal | do not use; use verified Spurgeon substitutes already in R9 |

Priority: **P1/P0 depending on whether R9 becomes article or support block for R8/tma.**

---

## 4. Fast wins already visible

These can be patched later if owner says “заполняй”.

| Fast win | Evidence found | Patch target |
|---|---|---|
| Owen “Be killing sin...” | CCEL page `https://ccel.org/ccel/owen/mort/mort.i.v.html`, Chapter II includes: “Do you mortify; do you make it your daily work; be always at it whilst you live; cease not a day from this work; be killing sin or it will be killing you.” | `67_R5_TWO_STRUGGLES.md` quote bank item #12 |
| Rogers Advice 1 | Google/scan not visually accessible in this sandbox; EEBO2 rights-restricted | closed as negative boundary; no A+ direct translation |
| Rogers Advice 5–6 | secondary extraction/EEBO2 useful only as locator/search aid | closed as negative boundary; do not mark A+ until owner/future scan image pass |

---

## 5. Priority order for next filling pass

If continuing, do not try to close every candidate. Recommended order:

1. **Rogers scan-first closure** for existing `tma-na-serdce` public article — closed in Research as negative evidence boundary; remaining visual scan work belongs to owner/future Site issue if direct translations are still desired.
2. **Owen `Be killing sin` patch** in R5 — already found primary CCEL text; quick source-file correction.
3. **R8 Owen `Glory of Christ` exact locator pass** — high value for the P0 capstone.
4. **R1 Gill/Bavinck/Boston regeneration exact source cards** — supports P0 `Рождение свыше`.
5. **R7a Hebrews 4:2 textual/exegetical pass** — supports P0 `Сердце и Слово`.
6. MLJ full book is closed as `BOOK-FULLTEXT-HOLD / DO-NOT-QUOTE-BOOK` unless owner supplies legal text.

---

## 6. No-push note

Initial sweep was no-push. Owner later authorized integrating this audit into Research and pushing the branch; this file is now a repository backlog, still not a production/source authority.

---

## 7. Round 2 — corpus-wide grep audit and supersession control

### 7.1 Machine-scan result: where unresolved markers cluster

A second pass scanned all `СЕРИЯ СЕРДЦЕ/*.md` for `HOLD`, Russian/English unverified markers, `ЧАСТИЧНО`, `candidate`, `REQUIRES`, `A-`, `locator-only`, `PAGE-IMAGE`, and `BOOK-FULLTEXT`.

Important interpretation: high counts do **not** automatically mean live defects. Some files are compacted historical ledgers. The counts identify where to look, not what to publish.

| Rank | File | Signal | Audit interpretation |
|---:|---|---:|---|
| 1 | `29_DATA_TABLES_COMPACTED.md` | very high | Mostly compacted legacy data; do not manually mine unless reconciling an old CSV row. |
| 2 | `03_SOURCE_WORKFLOW_QUOTE_POLICY_WEB_VERIFICATION.md` | high | Rules/ledger file; many `locator` mentions are policy, not defects. |
| 3 | `25_QUOTE_BANK_EXACT_ANCHORS_AND_CANDIDATES.md` | high | **Active useful queue**: quote-card candidates and locator-only anchors. |
| 4 | `27_WEB_VERIFICATION_SOURCES_AND_LEDGER.md` | high | Source-class authority; contains A-/B distinctions and locator-only rules. |
| 5 | `71_R9_CHRIST_OF_REVELATION.md` | high | **Active article-dossier risk**: many `ЧАСТИЧНО` / aggregator quotes. |
| 6 | `67_R5_TWO_STRUGGLES.md` | high | **Active article-dossier risk**: many candidates, some can be closed quickly. |
| 7 | `70_R8_BEHOLDING_GLORY.md` | high | **Active P0 capstone risk**: Owen/Spurgeon/MLJ/source locators. |
| 8 | `68_R7A_WORD_AND_HEART.md` | medium-high | **Active P0 risk**: Heb 4:2 textual/source issues. |
| 9 | `64_R2_OT_REGENERATION_INDWELLING.md` | medium-high | Bonus/P1; multiple candidate locators. |
| 10 | `62_R1_REGENERATION_EXEGESIS.md` / `63_R1_REGENERATION_SYSTEMATICS.md` | medium-high | **Active P0 risk**: regeneration exact-source locking. |

Working conclusion:

```text
Primary active audit targets = V84I gates + R1/R5/R7a/R8/R9 + 25/27/28 ledgers.
Do not reopen V48 801/801 closed quote-risk queue unless a current article imports one of those rows as a quote.
```

### 7.2 Supersession notes: avoid false positives

The corpus contains historical statuses that later files supersede. Do not treat every old `TODO` as current.

| Old marker | Later/current control | Result |
|---|---|---|
| `57_V61...` says Owen *Dominion of Sin* verbatim = TODO | `58_V62_VERIFIED_QUOTE_CARDS_OWEN_BUNYAN_MARSHALL.md` closes Owen/Bunyan/Marshall HIGH candidates | Do **not** count V61 Owen TODO as still open unless reconciling the old file text itself. |
| `59_V63...` says Rogers verified via Monergism / bible.ca | V84D/V84I require scan-first provenance for the **public tma article’s direct Russian translations** | Rogers is not “unverified” generally, but **current public provenance is still not A+ until scan-image locators are recorded**. |
| Old ledgers mark Goodwin short anchors “safe” | V84D distinguishes Wesley extract vs full treatise link + `PDF-PAGE-IMAGE-HOLD` | For new Goodwin direct quotes, use V84D/H evidence classes, not older loose wording. |
| Perkins sometimes marked A via EEBO | V48/V27 say Perkins is locator-only until a concrete section/question is opened | Do not quote Perkins from secondary lead or TOC alone. |
| Monergism/DigitalPuritan PDFs often marked A- | Current policy says A- supports thesis/paraphrase but page-image or precise locators needed for exact quotation | A- is not A+. |

### 7.3 Older V49–V80 backlog: what remains genuinely useful

The old underdeveloped-gap queue is not “unclosed quote risk”; it is a source-mining wishlist. High-value remaining items that still recur in later files:

| Topic | Source(s) | Current state | Use only if... |
|---|---|---|---|
| Ames on conscience | William Ames, *Conscience with the Power and Cases Thereof* | repeatedly named, not fully mined | article needs exact taxonomy of erroneous/doubting/scrupulous conscience |
| Taylor on four soils | Thomas Taylor, 1621/1634 parable text | title/locator known, exact paragraphs not mined | V.2 `Четыре почвы` needs primary Puritan quote-cards |
| Bolton on afflicted conscience / Christian freedom | Robert Bolton / Samuel Bolton | located, not fully page-carded | article needs guardrail against premature comfort/despair or law/gospel confusion |
| Dyke deeper self-deceit | Daniel Dyke, *Mystery of Self-Deceiving* | V72 says next best pass is ch. XI–XXX | article wants pre-sin / during-sin / after-sin diagnostic chart |
| Zeal / joy / brotherly love distinctions | Edwards/Watson/Flavel/Brooks possible | V74 says useful later | article specifically treats holy affection vs counterfeit zeal/joy |
| Family-love / lawful loves becoming ruling loves | Baxter/Clarkson/Flavel/Burroughs | V75 says possible later | article moves beyond money/status to household/reputation/ministry idols |
| Conscience types after V77/V78 | Ames/Perkins/Baxter/Bolton | still possible layer | article focuses on tender/scrupulous/seared/erroneous conscience |

### 7.4 Quote bank `25_...`: current not-A+ buckets

`25_QUOTE_BANK_EXACT_ANCHORS_AND_CANDIDATES.md` should be read in layers:

1. **Ready exact anchors** exist for some core authors (Charnock, Owen, Edwards, Boston, Sibbes, Chalmers, Flavel, etc.) but still need careful edition/context if used as long quotes.
2. **Locator-only buckets** remain for Perkins, Baxter, and longer Goodwin passages.
3. **Candidate sections V67–V80** are not ready quotations unless they have exact text + locator + context note.

Specific candidate buckets still not A+:

| Section | Examples | Rule |
|---|---|---|
| V67 quote-card candidates | Manton, Charnock, Vincent page locking | Use as paraphrase until exact page/section locked. |
| V68 false peace / weak grace | Mead, Shepard, Brooks, Guthrie | Some later V68/V70/V63 material closes portions; still page-lock before direct quote. |
| V69 exact-anchor candidates | Burgess, Flavel, Shepard, Perkins, Bolton | Explicitly says “do not quote until page/locator checked.” |
| V75 creature comforts | Baxter, Clarkson, Flavel, Burroughs | Locator phrases only; do not quote as if extracted. |
| V77 temptation | Owen, Flavel, Gilpin, Brooks | Candidate ideas only; exact extraction required. |
| V78 conscience/liberty | 1689, Ames, Baxter, Bolton | Short confessional text may be ready; Ames/Baxter/Bolton require exact source pass. |
| V79 duties/formalism | Shepard, Charnock, Clarkson, Flavel, Owen, Baxter, Gurnall | Anchors only; quote-card extraction needed. |
| V80 spiritual pride | Baxter, Edwards, Brooks, Watson, Flavel | Source candidates, not final quotations. |

### 7.5 Source ledger `27_...`: current evidence-grade reminders

Key rules preserved from `27_WEB_VERIFICATION_SOURCES_AND_LEDGER.md`:

- `A` = primary text / scan / library digitization / CCEL / EEBO; usable for thesis, but exact quote still needs context.
- `A-` = accessible PDF/reprint without critical apparatus or with OCR/reprint caveats; usable for thesis, but exact quote requires context and locator check.
- `B` = publisher description / respectable overview; orienting, not load-bearing alone.
- `C/D` = blog/quote-site/unconfirmed; never quote as source authority.

Current sources with special caution:

| Source | Caution |
|---|---|
| Boston | older ledger says A-/B depending link; page anchors from early scans still useful if quoting. |
| Owen *Spiritual-Mindedness* | FP Church / PDFs useful; verify chapter/section before exact quote. |
| Sibbes / Brooks | Monergism/DigitalPuritan PDF = A-; good for thesis, but page/context lock before long quote. |
| Goodwin | older A-/B language narrowed by V84D; distinguish extract vs full treatise. |
| Perkins / Baxter | locator-only until opened section is copied and verified. |

### 7.6 Active “do-not-use / only-with-label” list

These are not just low-grade; they should be explicitly blocked unless verified:

| Item | File(s) | Current instruction |
|---|---|---|
| Baucham “sissified/needy Jesus” | `71_R9...` | Do not use without primary source. |
| “Spurgeon: lion for enemies / lamb for friends” | `71_R9...` | Treat as likely apocryphal; use verified Spurgeon substitutes instead. |
| Spurgeon “free will carried many souls to hell...” | `65_R3...` | **APOCRYPHAL-RISK / DO-NOT-USE**; use verified Spurgeon sermon substitute instead. |
| Owen “Without the Holy Spirit we may as well burn our Bibles” | `68_R7A...` | Attributed via Banner article but not located in Owen corpus; use Calvin substitute unless exact source found. |
| Hughes “expulsive force” on 2 Cor 3:18 | `70_R8...` | **BLOCKED-AS-DIRECT-HUGHES-QUOTE**; remove attribution unless primary book later proves it. |
| M’Cheyne “ten looks at Christ” | architecture/R8 context | Attribution disputed; verify via Bonar or omit name. |
| Broad Adams psychiatric claims | V81–V84 | `DO-NOT-IMPORT` as contemporary guidance. |

### 7.7 Next audit work if continuing without filling yet

If the task remains pure audit, the next useful pass is:

1. Build a compact **CSV-style queue** from R1–R9 with columns: `file`, `article`, `source`, `marker`, `risk`, `next action`, `priority`.
2. Reconcile `25` quote-bank candidates against later verified quote-card files `57–59` so already-closed HIGH/MEDIUM items stop showing up as open.
3. Create a separate **DO-NOT-USE registry** for apocryphal/quote-site items.
4. Create a **source-grade upgrade plan**: A-/locator-only → A+ exact quote cards.
5. Only after owner says “заполняй” begin patching source files and extracting exact quotes.


---

## 8. Active queue table — R1–R9 and current gates

This table is the practical audit queue to use before any filling/extraction pass.

| Queue ID | Priority | File | Article / lane | Source or issue | Current marker | Risk | Next action |
|---|---|---|---|---|---|---|---|
| V84I-ROGERS-01 | CLOSED-as-boundary | `72_V84I...` / V84D | `tma-na-serdce` | Timothy Rogers Advice 1/5/6 | Google scan blocked in sandbox; EEBO2 rights-restricted | no A+ direct translation/page-image claim | do not use direct translations until owner/future pass provides visual 1691 scan locators |
| V84I-MLJ-01 | CLOSED-as-boundary | V84A–V84I | depression/darkness lane | MLJ *Spiritual Depression* | `BOOK-FULLTEXT-HOLD / DO-NOT-QUOTE-BOOK` | book claims cannot become quote-ready | no further import unless owner supplies legal full text/owned scan |
| V84I-PDF-01 | CLOSED-as-boundary | V81–V84H | Adams/Goodwin/PDF sources | official PDFs | `PAGE-IMAGE-HOLD / DO-NOT-DIRECT-QUOTE` | parsed text ≠ image verification | paraphrase or use closed HTML/text anchors; no forced import |
| R1-EXE-01 | CLOSED-as-paraphrase-only | `62_R1...` | III.2 born again | Carson / Schreiner / Kruse | pages not directly opened | no direct quote; position-locator/paraphrase only | article burden covered by Scripture + closed older/systematic sources |
| R1-SYS-01 | PARTLY-CLOSED-local | `63_R1...` | III.2 born again | Gill, *Body of Divinity* | B6 Monergism HTML verified 2026-07-31 | Baptist regeneration quote cards now partially locked | optional print-page / additional Gill extraction remains |
| R1-SYS-02 | PARTLY-CLOSED-local | `63_R1...` | III.2 born again | Bavinck RD IV | Monergism RD4 ch.1 excerpt read 2026-07-31 | broad/restricted regeneration and immediate operation now excerpt-locked | Baker pages/Kuyper critique optional |
| R1-SYS-03 | CLOSED-local | `63_R1...` | III.2 born again | Boston regeneration/state of grace | GraceGems open text verified 2026-07-31 | real/thorough/supernatural/universal/lasting breakdown locked | early-scan/print page optional |
| R1-WHIT-01 | CLOSED-as-blocked-local | `62/63_R1...` | III.2 born again | Whitefield born-again anecdote/stat | no primary source found | blocked as documented fact | use verified Whitefield sermon instead; tradition only if labelled |
| R1-SPROUL-01 | CLOSED-local | `63_R1...` | III.2 born again | Sproul “regeneration precedes faith” / watershed | official Ligonier article verified 2026-08-01 | quote-safe at article level, no book page claim | print/book source optional only |
| R2-HAM-01 | PARTLY-CLOSED-local | `64_R2...` | OT regeneration bonus | Hamilton Themelios/TrinJ/monograph | Themelios HTML verified 2026-07-31; TrinJ survey chart verified 2026-08-01; Goodreads monograph quotes downgraded | conclusion and six-position chart locked | Hamilton monograph page locators still optional/open |
| R2-FERG-01 | P1 | `64_R2...` | OT regeneration bonus | Ferguson *The Holy Spirit* | lectures only | book citation missing | get 1–2 exact book locators or paraphrase by lecture only |
| R3-CALVIN-01 | CLOSED-local | `65_R3...` | struggle without regeneration | Calvin Institutes II.3.3–4 | CCEL/Beveridge readback done 2026-07-31 | civil righteousness wording now source-locked at CCEL level | Battles/Russian edition remains editorial check |
| R3-AUG-01 | P1 | `65_R3...` | struggle without regeneration | Augustine / `splendida vitia` chain | attribution not closed | classic misattribution risk | verify Latin/FOC or mark reception only |
| R3-SPURG-01 | CLOSED-as-blocked-local | `65_R3...` | struggle without regeneration | Spurgeon “free will carried...” | apocryphal-risk marked 2026-07-31 | do not use | use verified Spurgeon substitute |
| R4-WHIT-01 | CLOSED-as-attributed-local | `66_R4...` | four soils | Whitefield stony-ground quote | no primary locator found | attributed-only / do-not-direct-quote | use Spurgeon F1 / Calvin B2 substitutes |
| R4-TAYLOR-01 | PARTLY-CLOSED-local | `66_R4...` | four soils | Thomas Taylor 1621 | Hail&Fire title/PDF metadata + EEBO CC0 fulltext pages 118–120, 261–262 verified 2026-08-01 | stony/good-soil anchors now usable at open-text level | optional page-image/modernized-Hail&Fire comparison only |
| R4-COMM-01 | CLOSED-as-no-direct-quote | `66_R4...` | four soils | France / Carson | page locators not available | do not exact-quote; use paraphrase/locator only | article burden covered by Calvin/Taylor/Spurgeon/Ryle |
| R5-OWEN-01 | CLOSED-local | `67_R5...` | two struggles | Owen *Mortification* ch. 2 | CCEL verified 2026-07-31 | quote-card patched locally | print page not claimed |
| R5-OWEN-02 | CLOSED-local | `67_R5...` | two struggles | Owen “unless indeed he be so” / builder analogy | CCEL verified 2026-07-31 | exact context now patched | print/Goold page optional |
| R5-MEAD-01 | PARTLY-CLOSED-local | `67_R5...` | two struggles | Mead Agrippa/conscience + false peace + step VII struggle | CCEL verified 2026-07-31/2026-08-01 | candidates #5/#7 and step 7 closed | broader Q2–Q5 still open only if needed |
| R5-SPURG-01 | PARTLY-CLOSED-local | `67_R5...` | two struggles | Spurgeon Luke 18:13 publican | official Spurgeon Library sermon verified 2026-07-31 | Baptist preaching support found | optional broader Luke 18:9–14 sermon/syntax still open |
| R7A-METZ-01 | CLOSED-as-no-use | `68_R7A...` | heart and Word | Metzger Heb 4:2 | BibleHub/Meyer open-reference layer verified 2026-08-01 | article will not cite Metzger/NA28 rating | exact Metzger rating optional scholarly appendix only |
| R7A-COMM-01 | CLOSED-as-no-direct-quote | `68_R7A...` | heart and Word | Lane/O’Brien/Schreiner/Ellingworth/Attridge | not checked directly | do not use as checked summary | no blocker; reopen only with book access |
| R7A-OWEN-01 | CLOSED-as-attributed-only | `68_R7A...` | heart and Word | Owen “burn our Bibles” | Banner/Hamilton page verified but no Owen locator | do not quote as Owen | use Calvin/1689 substitutes unless exact Owen work/page is found |
| R7A-GILL-01 | CLOSED-local | `68_R7A...` | heart and Word | Gill Heb 4:2 | BibleStudyTools Gill readback done 2026-07-31 | both readings now pinned to public-domain mirror | print page not claimed |
| R8-OWEN-01 | PARTLY-CLOSED-local | `70_R8...` | beholding glory | Owen *Glory of Christ* | key quote cards #10–15 CCEL-verified 2026-07-31 | capstone Owen core now chapter-locked | optional print-page pass only |
| R8-GRAM-01 | editorial | `70_R8...` | beholding glory | κατοπτριζόμενοι | owner decision open | overload risk | decide main text vs footnote/dropdown |
| R8-HUGHES-01 | CLOSED-as-blocked-local | `70_R8...` | beholding glory | Hughes “expulsive force” | blocked as direct quote 2026-07-31 | do not attribute to Hughes | use Chalmers/Owen/Calvin or anonymous synthesis |
| R8-SPURG-01 | PARTLY-CLOSED-local | `70_R8...` | beholding glory | Spurgeon official “Glory!” support locator | official Spurgeon Library read 2026-07-31 | support quote located | optional dedicated 2 Cor 3:18 sermon search remains |
| R8-MLJ-01 | CLOSED-as-boundary | `70_R8...` | beholding glory | MLJ `Reflecting His Glory` | official MLJ page read 2026-07-31 | metadata/description/breakdown known | no direct sermon quote; audio/transcript not needed unless future owner asks |
| R8-MCHEYNE-01 | PARTLY-CLOSED-local | architecture/R8 | beholding glory | “ten looks at Christ” | Google Books p.239 verified 2026-07-31 | letter text/page locked; originality still open | do not claim Baxter origin without primary locus |
| R9-GOODWIN-01 | PARTLY-CLOSED-local | `71_R9...` | Christ of Revelation | Goodwin majesty+tenderness | Monergism PDF text verified 2026-08-01 for Introduction + Part II anchors | short anchors quote-safe as PDF-text, not page-image | long/page-image/print-page pass optional/open |
| R9-GILL-01 | CLOSED-local | `71_R9...` | Christ of Revelation | Gill on Rev 1:17; 2:23; 5:5–6; 19:15 | BibleStudyTools open text verified 2026-07-31 | Baptist/public-domain support layer now safer | print page and Isa 63:1 not claimed |
| R9-SPROUL-01 | PARTLY-CLOSED-local | `71_R9...` | Christ of Revelation | Sproul *Holiness of God* | official Ligonier quote-page subset verified 2026-08-01 | selected quotes usable without page claim | aggregator-only lines blocked unless book checked |
| R9-ORTLUND-01 | PARTLY-CLOSED-local | `71_R9...` | Christ of Revelation | Ortlund / Crossway | official Crossway Q&A/article verified 2026-08-01 | wrath/gentleness balance usable from official articles | ch.15 and lion/lamb book wording blocked until book page |
| R9-MACARTHUR-01 | PARTLY-CLOSED-local | `71_R9...` | Christ of Revelation | MacArthur/GTY on Thyatira and Rev 19 | official transcripts `90-475` and `66-71` verified 2026-07-31 | two GTY quote-cards now official-transcript support | other GTY links remain locator-level |
| R9-REV1913-01 | P1 | `71_R9...` | Christ of Revelation | Rev 19:13 blood | exegetical fork | interpretation risk | compare Beale/Mounce/Osborne if used |
| R9-BAUCHAM-01 | BLOCK | `71_R9...` | Christ of Revelation | Baucham “sissified Jesus” | not verified | polemical quote risk | do not use without primary source |
| R9-SPURG-APOC-01 | BLOCK | `71_R9...` | Christ of Revelation | Spurgeon lion/lamb quote | likely apocryphal | false attribution risk | use verified Spurgeon substitutes already found |

### 8.1 Source-access note for R8 Owen

During this audit, CCEL access to Owen *Meditations and Discourses on the Glory of Christ* worked through the fetch tool:

- Work info: `https://ccel.org/ccel/owen/glory.html`
- TOC: `https://ccel.org/ccel/owen/glory/glory.toc.html`
- Plain text endpoint exposed by CCEL: `https://ccel.org/ccel/o/owen/glory/cache/glory.txt`

The TOC confirms the exact chapter map needed by R8:

- Chapter I: explication of John 17:24;
- Chapters XII–XIV: differences between beholding Christ’s glory by faith now and by sight in heaven;
- second part, Chapter II: recovery of spiritual decays and fresh springs of grace.

This means R8’s former “WebFetch blocked” limitation is probably closable in the next filling pass. Still, no exact R8 quote-card was patched yet.

---

## 9. Audit-only disposition after Round 2

`ACTIVE OPEN GATES IDENTIFIED`

`FALSE-POSITIVE HISTORICAL TODOS SEPARATED`

`R1–R9 ACTIVE QUEUE BUILT`

`DO-NOT-USE ITEMS FLAGGED`

`NO SOURCE FILES PATCHED EXCEPT THIS AUDIT BACKLOG`

`NO COMMIT`

`PUSH AUTHORIZED AFTER INITIAL NO-PUSH AUDIT`

---

## 10. Article-architecture gaps, not just quote/source gaps

The book architecture file `61_BOOK_ARCHITECTURE_V2_CHAPTERS_AND_RESEARCH_TASKS.md` shows that several articles are still structurally open even before quote-level verification. This is a different kind of “not closed”: the planned article lane has no dedicated dossier or no article-ready source closure yet.

### 10.1 P0 backbone status

| Planned P0 article | Dedicated dossier exists? | Current closure status | What remains open |
|---|---:|---|---|
| I.2 `Сердце в Эдеме: каким было сотворено и как пало` | No dedicated R-file found | **OPEN / architecture gap** | Needs Genesis 1–3 + Rom 5 + James 1 source dossier; current material is scattered in biblical/canonical files. |
| III.2 `Рождение свыше` | Yes: `62_R1...`, `63_R1...` | **Research exists, source-lock mostly closed** | Gill/Bavinck/Boston closed; Whitefield anecdote blocked; modern commentaries closed-as-paraphrase-only unless books opened. |
| III.3 `Сокрушённое сердце: покаяние` | No dedicated R-file found | **OPEN / architecture gap** | Material exists scattered in R5, V84 depression/guilt, religious-heart files, but no focused Psalm 51 / 2 Cor 7 / true-false repentance dossier. |
| V.3 `Две борьбы` | Yes: `67_R5...` | **Research exists, source-lock mostly closed** | Owen, Mead step 7, Augustine VIII.9.21, Spurgeon Luke 18:13 support, and Edwards headings now closed; only optional body-level Edwards / broader Mead Q2–Q5 remain. |
| X.1 `Суд сердца: два воскресения` | No dedicated R-file found | **OPEN / architecture gap** | R9 points toward this article, but X.1 needs its own John 5:28–29 / Rev 20 / Luke 16 / 2 Thess 1 dossier. |
| VIII.1 `Сердце и Слово` | Yes: `68_R7A...` | **Research exists, source-lock open** | Heb 4:2 textual issue and commentary locators open. |
| VIII.5 `Христос — Пленитель сердца` | Yes: `70_R8...` | **Research exists, source-lock open** | Owen *Glory of Christ* exact locators and several quote candidates open. |

P0 conclusion:

```text
The P0 backbone is NOT fully closed at article-architecture level.
Three P0 articles still lack a dedicated dossier: Eden, Repentance, Judgment/two resurrections.
Four P0 articles have dossiers but still need source-locking: R1, R5, R7a, R8.
```

### 10.2 P1 / P2 planned articles with no dedicated closure

| Planned article | Priority in architecture | Current status | Next audit action |
|---|---|---|---|
| II.3 `Борьба без возрождения` | P1 | R3 dossier exists, source-lock partly open | Calvin is closed; Watson aphorism and Spurgeon free-will aphorism are blocked; Augustine Contra Julianum / splendida-vitia chain and some print locators remain open. |
| V.2 `Четыре почвы` | P1 | R4 dossier exists, source-lock open | Close Whitefield/Taylor/France/Carson locators. |
| Bonus `Возрождение в ВЗ` | P1 | R2 dossier exists, source-lock open | Close Hamilton/Ferguson/Calvin/Augustine/Gill/Owen locators. |
| VI.4 `Гнев, обида, прощение` | P1 | No dedicated R-file found | Needs focused dossier; current material scattered in speech/temptation/pastoral grids. |
| IX.2 `Тревожное сердце и покой Божий` | P1 | No dedicated R-file found | Needs John 14 / Phil 4 / Matt 6 / 1 Pet 5 focused dossier, with medical-anxiety guardrails. |
| II.4 `Ожесточение` | P2 | No dedicated R-file found | Needs Heb 3 / Pharaoh / Mark 3:5 / seared conscience dossier. |
| VIII.3 `Сердце в молитве` | P2 | Older `34_V54...` prayer layer exists, but no final R-style dossier | Audit whether V54 is sufficient or needs R-file extraction. |
| X.3 `Сердце дома: новое небо и новая земля` | P2 | No dedicated R-file found | Needs Rev 21–22 / Ps 73:26 final hope dossier. |
| V optional `Уверенность` | P3 | scattered in assurance files | Needs decision whether to remain optional or become article. |
| V/R7b `Фарисей и ученик` | P1 | R7b dossier exists, source-lock open | Close Carson/MLJ/Spurgeon/Augustine/Cyril candidates. |
| R9 `Христос Откровения` | later owner-driven P1/P0 support | R9 dossier exists, source-lock open | Decide if standalone article, R8 support block, or X.1 cross-link support. |

### 10.3 Architecture-level priority if continuing audit

If the goal is to find **unclosed articles**, not just unclosed quotes, the next missing-dossier audit order should be:

1. `Суд сердца: два воскресения` — because R9 already points to it and it closes the unbelieving line of the book.
2. `Сокрушённое сердце: покаяние` — because R5 assumes III.3 exists and many diagnostics depend on true/false repentance.
3. `Сердце в Эдеме` — because it is the first P0 gap in chapter I and grounds the fall/heart anthropology.
4. `Гнев, обида, прощение` and `Тревожное сердце` — P1 pastoral gaps.
5. `Ожесточение` and `Сердце дома` — P2 fullness gaps.

No new dossier was created in this pass; this is only the gap map.

---

## 11. Navigation / manifest / authority drift still open

This is another class of not-closed work: the latest research files exist, but the navigation and manifest layer does not yet represent them.

### 11.1 Main navigation does not know V81–V84I / R1–R9

A direct search found no references to V81–V84 / R1–R9 / V84I in the four main navigation/provenance files:

- `00_README_AND_NAVIGATION.md`
- `01_MASTER_INDEX_AND_SERIES_STRUCTURE.md`
- `31_MANIFESTS_ARCHIVE_STATS_AND_LEGACY_LOGS.md`
- `33_FILE_PROVENANCE_MAP.md`

Recent files not referenced there include:

```text
60_V81_JAY_ADAMS_PRIMARY_SOURCE_DEEPENING.md
61_BOOK_ARCHITECTURE_V2_CHAPTERS_AND_RESEARCH_TASKS.md
61_V82_PSYCHOTROPIC_MEDICATION_BODY_SOUL_BIBLICAL_COUNSELING.md
62_R1_REGENERATION_EXEGESIS.md
62_V83_MEDICATION_HOLD_CLOSURE_48_NEW_PASSES.md
63_R1_REGENERATION_SYSTEMATICS.md
63_V84_DEPRESSION_SIN_SUFFERING_GUILT_BURNOUT_DESPAIR.md
64_R2_OT_REGENERATION_INDWELLING.md
64_V84A_SOURCE_STATUS_AND_LLOYD_JONES_HOLD.md
65_R3_UNREGENERATE_STRUGGLE.md
65_V84B_DEPRESSION_THEOLOGICAL_PRIMACY_AND_AXIS_CORRECTION.md
66_R4_FOUR_SOILS.md
66_V84C_EDITORIAL_COMPLETENESS_20PLUS_PRIMARY_PASSES.md
67_R5_TWO_STRUGGLES.md
67_V84D_SOURCE_LOCATOR_AND_EVIDENCE_STATUS_CLOSURE.md
68_R7A_WORD_AND_HEART.md
68_V84E_INDEPENDENT_AUDIT_AND_CURRENT_AUTHORITY.md
69_R7B_PHARISEE_DISCIPLE.md
69_V84F_FINAL_EXACT_HEAD_CLOSURE.md
70_R8_BEHOLDING_GLORY.md
70_V84G_TRINITARIAN_CROSS_AND_DERELICTION_BOUNDARY.md
71_R9_CHRIST_OF_REVELATION.md
71_V84H_DIRECT_SOURCE_CLEANUP_TRINITARIAN_AND_FINAL_EXACT_HEAD.md
72_V84I_POST_MERGE_TOTAL_AUDIT_AND_CLOSURE_GATES.md
```

Interpretation:

```text
Navigation/provenance is stale after V80.
A new reader can easily start from 00/01/33 and miss the actual current authority V84I plus the R-series architecture work.
```

This does not invalidate the files, but it is an **open governance/navigation task**.

### 11.2 V84H still says “CURRENT” in its own heading

`71_V84H_DIRECT_SOURCE_CLEANUP_TRINITARIAN_AND_FINAL_EXACT_HEAD.md` still labels itself:

```text
CURRENT CROSS-REPO AUTHORITY / ... / KEEP DRAFT
```

V84I explicitly supersedes this for current workflow state after merge. Therefore the repo currently relies on the reader finding V84I first. If they open V84H directly, they see stale `KEEP DRAFT / NO PRODUCTION CLAIM` language.

Required closure option:

- either leave V84H historical but add a very top-line supersession pointer to V84I;
- or make `00_README...` and `01_MASTER...` point to V84I as the first current authority.

### 11.3 Architecture file has internal revision drift

`61_BOOK_ARCHITECTURE_V2_CHAPTERS_AND_RESEARCH_TASKS.md` contains an initial table and later owner revisions that are not fully folded back into the table.

Examples:

| Location | Older statement | Later revision | Open task |
|---|---|---|---|
| Initial ch. VII heading | `Глава VII. Школа сердца` | later says rename to `Возрастание сердца` | normalize table heading |
| Initial ch. VIII table | only Spirit / Heart of Christ / Prayer | later adds VIII.1 `Сердце и Слово` and VIII.5 `Христос — Пленитель сердца` | update chapter VIII table |
| Initial count | `23 existing + 12 new + 1 bonus` | later says `23 existing + 15 new (+1 bonus)` | choose final count and update once |
| R9 | not present | later file `71_R9_CHRIST_OF_REVELATION.md` exists | decide whether R9 is architecture item, support block, or extra dossier |

This is an article-planning closure issue: the plan is readable, but not normalized into one final table.

### 11.4 Manifest / file-count drift

Current top-level markdown count in `СЕРИЯ СЕРДЦЕ` is now `107` files. The single-ZIP era manifests run through `V80_SINGLE_ZIP_MANIFEST.md`; there is no V81/V82/V83/V84 manifest layer.

Open manifest tasks:

| Item | Status |
|---|---|
| V81–V84 manifest | missing |
| R1–R9 research-run manifest | missing |
| post-merge V84I authority pointer in README/master | missing |
| updated provenance map for files 60–72 | missing |
| archive count / compactness policy after 50-file cap | unclear / stale |

This does not mean the corpus is unusable. It means the **navigation/packaging closure is behind the research content**.

### 11.5 Practical closure recommendation

If continuing in audit-only mode, next create a small table named something like:

```text
CURRENT_AUTHORITY_POINTERS_2026-07-31
```

inside this audit file or later in README, with:

1. `72_V84I...` = current post-merge cross-repo authority;
2. `61_BOOK_ARCHITECTURE...` = current book architecture, but with noted revision drift;
3. `62_R1`–`71_R9` = current new-article research dossiers;
4. `60_V81`–`71_V84H` = historical/source authorities for depression/medication/trinitarian boundaries, governed by V84I where workflow state differs;
5. `73_OPEN_VERIFICATION...` = local no-push audit backlog, not source authority.


---

## 12. Status-label inconsistencies and inherited “blocked fetch” caveat

A further audit pass checked the headings/status blocks of R1–R9 dossiers.

### 12.1 R-files still carry old environment caveats

Most R dossiers were produced in a session where direct fetch to CCEL / Monergism / archive.org / BibleHub was blocked. They often mark items as `ВЕРИФИЦИРОВАНО` only by search snippets, then tell the final editor to re-check links.

Files with explicit inherited blocked-fetch caveat:

| File | Caveat |
|---|---|
| `62_R1_REGENERATION_EXEGESIS.md` | direct fetch blocked; `ВЕРИФИЦИРОВАНО` = exact phrase found by web search; final re-check recommended |
| `63_R1_REGENERATION_SYSTEMATICS.md` | CCEL/Monergism/Spurgeongems blocked; pre-publication comparison required |
| `64_R2_OT_REGENERATION_INDWELLING.md` | direct fetch blocked; candidates require control fetch |
| `65_R3_UNREGENERATE_STRUGGLE.md` | CCEL/Monergism/NewAdvent/BibleHub blocked; final re-check recommended |
| `66_R4_FOUR_SOILS.md` | direct fetch blocked but file says ready to write; open questions remain |
| `67_R5_TWO_STRUGGLES.md` | egress blocked; many candidates still marked for вычитка |
| `68_R7A_WORD_AND_HEART.md` | direct access blocked; unverified candidates require book/e-source check |
| `70_R8_BEHOLDING_GLORY.md` | direct fetch blocked; Owen and others snippet-verified only |
| `71_R9_CHRIST_OF_REVELATION.md` | WebFetch blocked; many `ВЕРИФИЦИРОВАНО ЧАСТИЧНО` aggregator items |

Interpretation:

```text
Search-snippet verification is not A+ for exact quotation.
Any quote that matters in a public article must be re-checked through primary page/text access.
```

### 12.2 “Ready to write” does not always mean source-closed

`66_R4_FOUR_SOILS.md` says:

```text
Статус: research-досье, готово к написанию статьи.
```

But the same file still has open questions:

- Whitefield F2 primary location not found;
- Calvin Harmony paragraph still to verify;
- France / Carson print page locators are closed-as-no-direct-quote/paraphrase-only;
- Thomas Taylor 1621 exact paragraphs not extracted;
- Russian Calvin translation/page policy open.

Therefore its honest status for article use should be read as:

```text
CONTENT OUTLINE READY / EXACT SOURCE LOCK NOT CLOSED
```

The same caution applies more broadly to R1/R5/R7a/R8/R9: they may be strong enough to draft from, but not all exact citations are publication-ready.

### 12.3 R8 has a concrete inherited caveat now likely removable

R8’s biggest caveat was inability to open Owen *Glory of Christ*. Current audit confirmed CCEL work page, TOC and text endpoint are accessible. That makes R8 a good first candidate for a “caveat removal” pass:

| R8 old caveat | Current audit finding | Closure path |
|---|---|---|
| Owen quotes only search-snippet verified | CCEL TOC and text endpoint reachable now | Extract exact chapter anchors and update R8 quote-bank |
| chapter numbers not reliably assigned | CCEL TOC gives chapter map | Map each quote to chapter URL |
| plain text endpoint available | yes | Use for search; still cite stable chapter URL in article |

### 12.4 R9 has the highest partial-verification density

`71_R9_CHRIST_OF_REVELATION.md` originally had many `ВЕРИФИЦИРОВАНО ЧАСТИЧНО` markers because Sproul, Ortlund, Gill, Ryle and MacArthur items were often found through aggregators/snippets. Subsequent safe passes closed Gill, key GTY, Ryle, Goodwin short anchors, Sproul official Ligonier subset, and Ortlund official Crossway Q&A/article subset.

Practical rule:

- Scripture exegesis in R9 is usable as article backbone.
- Verified Spurgeon sermon material is the safest non-biblical quote layer.
- Sproul/Ortlund: use only official Ligonier/Crossway verified subset; old aggregator-only or book-page snippets remain blocked/direct-quote unsafe.
- Baucham and apocryphal Spurgeon stay blocked.

### 12.5 Needed status vocabulary cleanup

Recommended labels for later cleanup:

| Current loose label | Better label |
|---|---|
| `ВЕРИФИЦИРОВАНО` from search snippet only | `SNIPPET-VERIFIED / PRIMARY-RECHECK-REQUIRED` |
| `готово к написанию статьи` with open quote tasks | `CONTENT-READY / QUOTE-LOCK-OPEN` |
| `A-` PDF/reprint | `THESIS-OK / DIRECT-QUOTE-LOCATOR-REQUIRED` |
| `locator-only` | `PARAPHRASE-ONLY UNTIL SECTION OPENED` |
| `ВЕРИФИЦИРОВАНО ЧАСТИЧНО` via aggregator | `SECONDARY-AGGREGATOR / DO-NOT-QUOTE-DIRECTLY` |

This vocabulary cleanup is not mandatory before continuing audit, but it would prevent future agents from over-reading old labels.

---

## 13. Safe closure pass 2026-07-31 — cumulative Research/local ledger

Owner first authorized local closure runs without push, then explicitly authorized updating Research and pushing; earlier safe-closure batches were pushed through `98a4158`. This section remains cumulative: rows dated 2026-08-01 in the current continuation are local workspace changes until the next owner-authorized commit/push. All closures below were made only where a primary/open source could be read directly and where no print-page or page-image claim was needed. They do not make production/site claims.

### 13.1 Closed locally

| Closure ID | File patched | Previous state | Closure made | Remaining boundary |
|---|---|---|---|---|
| SC-R5-OWEN-MORT-01 | `67_R5_TWO_STRUGGLES.md` | Owen “Be killing sin...” not verified in that run | Verified by CCEL `Of the Mortification of Sin`, ch. II, `mort.i.v.html`; added exact quote and locator | print page not claimed |
| SC-R5-OWEN-MORT-02 | `67_R5_TWO_STRUGGLES.md` | Owen ch. 7 continuation “unless indeed he be so” was candidate | Verified by CCEL `mort.i.x.html` | print page not claimed |
| SC-R5-OWEN-MORT-03 | `67_R5_TWO_STRUGGLES.md` | Owen “easier see without eyes...” was partial | Verified by CCEL `mort.i.x.html` | print page not claimed |
| SC-R5-OWEN-MORT-04 | `67_R5_TWO_STRUGGLES.md` | builder-without-foundation image was paraphrase/candidate | Verified exact paragraph by CCEL `mort.i.x.html`; added quote | print page not claimed |
| SC-R5-OWEN-MORT-05 | `67_R5_TWO_STRUGGLES.md` | Owen ch. 5–6 negative definition / ch. 8 universal obedience were candidate summaries | Verified CCEL `mort.i.viii.html` and `mort.i.xi.html`; added exact boundary phrases and second general rule | print page not claimed |
| SC-R5-MEAD-01 | `67_R5_TWO_STRUGGLES.md` | Mead Agrippa/conscience and false-peace lines were partial/candidate | Verified CCEL `almost.iii.i.html` and `almost.iii.viii.html` exact lines | print page not claimed; step 7 closed separately in SC-R5-MEAD-STEP7-01 |
| SC-R5-AUG-CONF-01 | `67_R5_TWO_STRUGGLES.md` | Augustine Confessions VIII.9.21 will/self formula was unverified candidate | Verified CCEL Schaff/NPNF exact sentence | Pusey/Chadwick print comparison optional |
| SC-R5-SPURGEON-01 | `67_R5_TWO_STRUGGLES.md` | Spurgeon Luke 18 support was unverified candidate | Verified official Spurgeon Library “A Sermon for the Worst Man on Earth” on Luke 18:13 | print page not claimed; broader Luke 18:9–14 syntax still open |
| SC-R5-EDWARDS-HEADINGS-01 | `67_R5_TWO_STRUGGLES.md` | Edwards 24 signs headings were CCEL/TGC summary with English headings candidates | Verified all Part II/III heading locators against CCEL `affections.toc.html` | body-level quotations still require section readback if used |
| SC-R8-OWEN-GLORY-01 | `70_R8_BEHOLDING_GLORY.md` | Owen *Glory of Christ* quote cards #10–15 were snippet-only | Verified CCEL chapter locators: `glory.i.iii`, `glory.i.iv`, `glory.i.xv`, `glory.i.xvii`, `glory.ii.iv` | print pagination optional, not claimed |
| SC-R8-OWEN-MORT-01 | `70_R8_BEHOLDING_GLORY.md` | “Be killing sin...” row only broadly attributed | Upgraded to CCEL ch. II locator `mort.i.v.html` | print page not claimed |
| SC-R8-CALVIN-2COR-01 | `70_R8_BEHOLDING_GLORY.md` | Calvin on 2 Cor. 3:18 was search-verified only | Verified CCEL Study / Calvin on 2 Cor. 3:18 for mirror language and image-restoration line | print page not claimed |
| SC-R8-CHALMERS-01 | `70_R8_BEHOLDING_GLORY.md` | Chalmers full expulsive-power paragraph was search/PDF-check pending | Verified open HTML sermon text section with the practical-moralist and expulsive-power lines | print/PDF page not claimed |
| SC-R8-MLJ-PAGE-01 | `70_R8_BEHOLDING_GLORY.md` | MLJ `Reflecting His Glory` was link-only / content unknown | Verified official MLJ Trust sermon page metadata, description, and breakdown | superseded by SC-R8-MLJ-NODIRECT-01: no direct sermon quote without transcript |
| SC-R8-MCHEYNE-01 | `70_R8_BEHOLDING_GLORY.md` | M'Cheyne “ten looks” attribution/page was disputed | Verified Google Books `Memoir and Remains`, p. 239, letter text; read Scriptorium Daily attribution caveat | letter text locked; pre-M'Cheyne/Baxter origin unconfirmed |
| SC-R8-SPURGEON-01 | `70_R8_BEHOLDING_GLORY.md` | Spurgeon on 2 Cor. 3:18 was source-discovery open | Verified official Spurgeon Library sermon “Glory!” cites 2 Cor. 3:18 and applies communion/conformity | not a dedicated 2 Cor. 3:18 sermon; optional further search remains |
| SC-R8-HUGHES-01 | `70_R8_BEHOLDING_GLORY.md` | Hughes “expulsive force” quote was suspicious/anachronistic | Marked blocked as direct Hughes quote; replace with Chalmers/Owen/Calvin or anonymous synthesis | may reopen only if primary Hughes book proves wording |
| SC-R7A-CALVIN-HEB-01 | `68_R7A_WORD_AND_HEART.md` | Calvin on Heb. 4:2 verified by snippet only | Verified via CCEL Study / Calvin on Hebrews 4:2 | print page not claimed |
| SC-R7A-GILL-HEB-01 | `68_R7A_WORD_AND_HEART.md` | Gill on Heb. 4:2 both readings was unverified candidate | Verified BibleStudyTools public-domain Gill page for Heb. 4:2 | print page not claimed |
| SC-R7A-MANTON-JAS-01 | `68_R7A_WORD_AND_HEART.md` | Manton on James 1:21 ingrafted word was unverified / blocked | Verified CCEL Works vol. 4 `manton04.iv.html` section on James 1:21 | print page not claimed; Psalm 119 Manton remains open |
| SC-R9-GILL-REV-01 | `71_R9_CHRIST_OF_REVELATION.md` | Gill Revelation notes were `ВЕРИФИЦИРОВАНО ЧАСТИЧНО` | Verified BibleStudyTools public-domain Gill pages for Rev. 1:17; 2:23; 5:5–6; 19:15 | print page not claimed; Isa 63:1 not closed |
| SC-R9-GTY-REV-01 | `71_R9_CHRIST_OF_REVELATION.md` | MacArthur / GTY Rev. 2 and Rev. 19 quotations were partial | Verified official GTY transcripts for `90-475` and `66-71` | official-ministry transcript support only; other GTY links not closed |
| SC-R9-RYLE-M23-01 | `71_R9_CHRIST_OF_REVELATION.md` | Ryle Matthew 23 stern-reproof line was partial | Verified GraceGems `m23.htm` exact phrase about loving heart using stern reproof | print page not claimed; John 2 handled separately in SC-R9-RYLE-JOHN2-01 |
| SC-R9-GTY-JOHNSON-01 | `71_R9_CHRIST_OF_REVELATION.md` | GTY / Jeremiah Johnson “tame the Lion” critique was partial/byline-snippet | Verified official GTY blog `B210315` and exact line | critique context only, not doctrinal foundation |
| SC-R4-CALVIN-HARMONY-01 | `66_R4_FOUR_SOILS.md` | Calvin Harmony B2 temporary-faith paragraph was partial / fetch-blocked | Verified CCEL `calcom32.ii.xix.html` paragraph on temporary faith / stony ground | print page not claimed; Luke 8:15 phrase optional |
| SC-R4-SPURGEON-WHITEFIELD-01 | `66_R4_FOUR_SOILS.md` | Spurgeon stony-ground sermon was partial; Whitefield stony-ground quote lacked primary locator | Verified official Spurgeon Library F1; marked Whitefield F2 attributed-only / do-not-direct-quote | Spurgeon print page not claimed; Whitefield can reopen only with primary locator |
| SC-R3-CALVIN-INST-01 | `65_R3_UNREGENERATE_STRUGGLE.md` | Institutes II.3.3–4 CCEL fetch had been blocked | Verified CCEL/Beveridge chapter readback at `institutes.iv.iv.html`; marked source-risk closed | Battles/Russian edition still editorial choice |
| SC-R3-WATSON-SPURGEON-BLOCK-01 | `65_R3_UNREGENERATE_STRUGGLE.md` | Watson morality quote and Spurgeon free-will aphorism remained quote-collection risks | Marked Watson direct quote as quote-collection-only and Spurgeon aphorism as apocryphal-risk / do-not-use | use Calvin or verified Spurgeon substitutes |
| SC-R1-GILL-REGEN-01 | `63_R1_REGENERATION_SYSTEMATICS.md` | Gill B6 was unverified Body of Divinity candidate | Verified Monergism HTML `Of Regeneration`; added exact anchors on large/strict regeneration and new creature/new man | print page not claimed; more Gill extraction optional |
| SC-R1-BAVINCK-01 | `63_R1_REGENERATION_SYSTEMATICS.md` | Bavinck RD IV exact material was open | Verified Monergism HTML excerpt from RD4 ch.1 for broad/restricted regeneration, Word/Spirit order, and immediate Spirit operation | Baker page numbers not claimed; Kuyper critique optional |
| SC-R1-BOSTON-REGEN-01 | `63_R1_REGENERATION_SYSTEMATICS.md` | Boston E3 regeneration-change characteristics were partial/paraphrase | Verified GraceGems open text breakdown of real/thorough/supernatural/universal/lasting change | print/early-scan page not claimed |
| SC-R1-WHITEFIELD-ANECDOTE-01 | `62_R1_REGENERATION_EXEGESIS.md` / `63_R1_REGENERATION_SYSTEMATICS.md` | Whitefield “why preach born again?” anecdote was unverified tradition | Marked blocked as documented fact; use only as labelled tradition or omit | verified Whitefield sermon remains available substitute |
| SC-R2-HAMILTON-01 | `64_R2_OT_REGENERATION_INDWELLING.md` | Hamilton Themelios conclusion/formula was fetch-blocked / partly snippet-based | Verified TGC/Themelios HTML conclusion and position spectrum | TrinJ chart closed separately in SC-R2-HAMILTON-TRINJ-01; book pages not claimed |
| SC-R2-CALVIN-JOHN739-01 | `64_R2_OT_REGENERATION_INDWELLING.md` | Calvin on John 7:39 surrounding context was open | Verified CCEL `calcom34.xiii.vii.html` for bright/illustrious Spirit and regeneration/new-creature line | print page not claimed |
| SC-R2-AUG-TRACT32-01 | `64_R2_OT_REGENERATION_INDWELLING.md` | Augustine Tractate 32 exact wording was candidate | Verified New Advent/NPNF HTML on John 7:39 and special manner of giving Spirit | print page not claimed |
| SC-R2-GILL-JOHN739-01 | `64_R2_OT_REGENERATION_INDWELLING.md` | Gill on John 7:39 was unverified candidate | Verified BibleStudyTools public-domain Gill page for John 7:39 | print page not claimed |
| SC-R2-WARFIELD-OTSPIRIT-01 | `64_R2_OT_REGENERATION_INDWELLING.md` | Warfield OT Spirit continuity phrases were snippet-level | Verified Monergism HTML article opening phrases directly | print/article page not claimed |
| SC-R2-OWEN-PNEUM-01 | `64_R2_OT_REGENERATION_INDWELLING.md` | Owen Pneumatologia W-10/W-11 had phrase-level verification but no chapter readback | Verified CCEL `Pneumatologia`, Book III, ch. I (`pneum.i.vii.i.html`) for OT regeneration and obscure OT revelation statements | Goold/print pagination optional, not claimed |
| SC-R2-HAMILTON-GOODREADS-01 | `64_R2_OT_REGENERATION_INDWELLING.md` | Hamilton monograph W-3/W-5/W-6 were marked verified via Goodreads quotes | Downgraded to `SECONDARY-QUOTE-SITE / BOOK-PAGE-HOLD`; direct quote blocked until B&H page/edition checked | use Themelios W-4 conclusion or paraphrase only |
| SC-R5-MEAD-STEP7-01 | `67_R5_TWO_STRUGGLES.md` | Mead step VII “strife and combat against sin” remained open | Verified CCEL `almost.iii.ii.html` and added quote-card 7a | broader Mead Q2–Q5 optional |
| SC-R4-TAYLOR-01 | `66_R4_FOUR_SOILS.md` | Taylor 1621 was title-only / source underused | Verified Hail&Fire PDF title/metadata and EEBO/TCP CC0 fulltext pages 118–120, 261–262 for stony/good-soil anchors | page-image and modernized-text comparison optional |
| SC-R4-RYLE-01 | `66_R4_FOUR_SOILS.md` | Ryle Matthew 13 / Mark 4 were verified only loosely/snippet-level | Verified CCEL/GraceGems Matthew 13 and GraceGems Mark 4 paragraphs | print page not claimed |
| SC-R4-FRANCE-CARSON-NOUSE-01 | `66_R4_FOUR_SOILS.md` | France/Carson exact page locators remained open | Closed as `NO-DIRECT-QUOTE / PARAPHRASE-ONLY`; article burden covered by verified Calvin/Taylor/Spurgeon/Ryle | reopen only with NICNT/EBC edition pages |
| SC-R7A-HEB42-OPENAPP-01 | `68_R7A_WORD_AND_HEART.md` | Hebrews 4:2 textual note depended on summaries and Metzger remained inaccessible | Verified BibleHub interlinear/text and Meyer/StudyLight readback for critical-form parsing and hearing/faith contrast | Metzger citation dropped/no-use in SC-R7A-METZGER-NOUSE-01 |
| SC-R7A-OWEN-BURN-01 | `68_R7A_WORD_AND_HEART.md` | “burn our Bibles” formula was attributed to Owen without corpus locator | Verified Banner/Hamilton secondary attribution; marked `SECONDARY-ATTRIBUTION / DO-NOT-DIRECT-QUOTE-AS-OWEN` | reopen only with Owen work/chapter/page |
| SC-R7A-COMM-NOUSE-01 | `68_R7A_WORD_AND_HEART.md` | Lane/O’Brien/Schreiner/Ellingworth/Attridge positions remained open | Closed as `NO-DIRECT-QUOTE / NOT-CHECKED`; do not use as verified summaries | reopen only with book access |
| SC-R9-GOODWIN-01 | `71_R9_CHRIST_OF_REVELATION.md` | Goodwin majesty+tenderness needed direct pass | Verified Monergism PDF text for Introduction and Part II/Heb. 4:15 short anchors | page-image/print page and long block quotes not claimed |
| SC-R9-RYLE-JOHN2-01 | `71_R9_CHRIST_OF_REVELATION.md` | Ryle John 2 zeal line was snippet/partial | Verified GraceGems `j02.htm` for temple-cleansing/holy-wrath and Christ-knows-heart paragraphs; old zeal wording not found and blocked for direct quote | use verified John 2 wording or find separate Ryle locator |
| SC-R1-SPROUL-WATERSHED-01 | `63_R1_REGENERATION_SYSTEMATICS.md` | Sproul “watershed” source/page was open | Verified official Ligonier article “The New Birth” for “Regeneration precedes faith” and “watershed assertion” wording | no book page claim |
| SC-R1-MODERN-COMM-NOUSE-01 | `62_R1_REGENERATION_EXEGESIS.md` | Carson/Schreiner/Kruse book pages remained open | Closed as `SECONDARY-CITATION / PARAPHRASE-ONLY`; no direct exact quote ambition | reopen only with PNTC/NAC pages |
| SC-R2-HAMILTON-TRINJ-01 | `64_R2_OT_REGENERATION_INDWELLING.md` | Hamilton TrinJ spectrum names/details remained open | Verified TrinJ PDF text for six-position spectrum and final chart | PDF page-image not claimed; monograph pages still hold |
| SC-R7A-METZGER-NOUSE-01 | `68_R7A_WORD_AND_HEART.md` | Metzger exact rating remained open | Closed as `METZGER-CITATION-DROPPED / NO-DIRECT-METZGER-QUOTE`; article uses open-reference variant layer only | exact Metzger/NA28 optional appendix work |
| SC-R8-MLJ-NODIRECT-01 | `70_R8_BEHOLDING_GLORY.md` | MLJ audio/transcript remained open | Closed as `NO-AUDIO-TRANSCRIPT / DO-NOT-DIRECT-QUOTE`; official page metadata enough for dossier | future audio pass only if owner asks |
| SC-R9-SPROUL-01 | `71_R9_CHRIST_OF_REVELATION.md` | Sproul quotes came through aggregators | Verified official Ligonier quote-page subset; blocked aggregator-only lines | no book page claim |
| SC-R9-ORTLUND-01 | `71_R9_CHRIST_OF_REVELATION.md` | Ortlund judgment caveat came through secondary snippets | Verified official Crossway Q&A/article on wrath/gentleness and “rich in mercy” | ch.15/lion-lamb book wording remains `BOOK-PAGE-HOLD` |
| SC-V84-ROGERS-BOUNDARY-01 | `73_OPEN_VERIFICATION_BACKLOG_2026-07-31.md` | Rogers scan-first task could not be visually closed | Google Books blocked; EEBO2 rights-restricted; closed as negative evidence boundary | no A+ direct translations until owner/future visual scan pass |
| SC-V84-MLJ-PDF-BOUNDARY-01 | `73_OPEN_VERIFICATION_BACKLOG_2026-07-31.md` | MLJ book and PDF page-image gates looked like open import tasks | Closed as evidence boundaries: do-not-quote book/PDF without legal fulltext/page image | not a promise to import |

### 13.2 Why these closures are safe

- They use open primary/public-domain text hosts (CCEL, GraceGems, Monergism public-domain pages, EEBO/TCP CC0 fulltext where rights permit), official ministry/publisher pages (Ligonier/Crossway/MLJ where applicable), or CCEL/BibleHub/StudyLight readback.
- They do not claim scan-image verification, printed page numbers, or critical-edition superiority.
- They do not change theological conclusions; they only upgrade evidence status and locators.
- They do not import any external source over Scripture; all uses remain subordinate support.

### 13.3 Remaining boundaries after this pass

| Boundary / optional remainder | Current disposition |
|---|---|
| Rogers Advice 1/5/6 scan-first closure | **closed as negative boundary**: Google scan blocked here; EEBO2 rights-restricted; do not A+/direct translate until owner/future visual scan pass |
| MLJ *Spiritual Depression* | **closed as evidence boundary**: `BOOK-FULLTEXT-HOLD / DO-NOT-QUOTE-BOOK` unless owner supplies legal fulltext/owned scan |
| Adams/Goodwin PDF page-image gates | **closed as evidence boundary**: parsed/PDF text is not page-image verification; use paraphrase or closed short anchors only |
| R8 MLJ audio/transcript + M’Cheyne prior-origin + optional Spurgeon dedicated-sermon search | MLJ direct sermon quote is now blocked/no-use unless transcript supplied; M’Cheyne prior-origin and dedicated Spurgeon sermon are optional, not blockers |
| R9 remaining GTY/book-page extras | Gill Revelation, GTY `90-475`/`66-71`, GTY Johnson B210315, Ryle Matthew 23, Goodwin short anchors, Ryle John 2, Sproul official quote subset, and Ortlund official Crossway Q&A/article are locally closed; only optional GTY extras and blocked book-page wording remain |
| R1 Gill/Bavinck/Boston/Whitefield | Gill B6, Bavinck RD4 excerpt, and Boston regeneration characteristics are locally closed at HTML level; Whitefield anecdote is blocked as documented fact; optional print-page policy remains open |
| R4 optional Taylor page-image/Whitefield primary locator | Calvin Harmony B2, Spurgeon F1, Taylor open-text anchors, and Ryle G4/G5 are closed; Whitefield F2 is attributed-only; France/Carson are closed-as-no-direct-quote/paraphrase-only, not blockers |
| R7a modern commentary positions | Calvin/Gill and BibleHub/Meyer open-reference layer are closed; Metzger exact rating dropped/no-use; Lane/O’Brien/Schreiner/Ellingworth/Attridge closed-as-no-direct-quote/not blockers |
| R2 Ferguson/Hamilton monograph pages | Hamilton Themelios conclusion, TrinJ survey chart, Warfield HTML, Owen CCEL ch. I, Calvin, Augustine, and Gill John 7:39 are locally closed; Ferguson/Hamilton monograph direct book quotes remain blocked/optional |
