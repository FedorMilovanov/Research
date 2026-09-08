# G3 HISTORY — open questions / proof-closure backlog

**Status:** ACTIVE / FAIL-CLOSED  
The goal is not metaphysical “100% knowledge.” The achievable target is **proof-complete reconstruction against an explicit claim set**, with every remaining uncertainty named rather than hidden.

## P0 — blocks major conclusions

### Q001 — What exactly appears in Schedule L for FY2024 and FY2025?

**Status:** `CLOSED / VERIFIED_PRIMARY` for the filed transaction rows; **misconduct inference remains prohibited**.

Exact IRS raw e-file objects were acquired on exact Research head `8a5fedc6a60965d27c472a2a6643fb4e9b1dfe08` by workflow run `34208135511`:

- FY2024 object `202541359349304489`, raw XML SHA-256 `c14f511cf66051b916748440594586b4db1ecdb0d07ab14ef05e01e92524aca3`;
- FY2025 object `202641339349303874`, raw XML SHA-256 `48846b93808c2ffcacac6dc1995fb7890a630ccef9f711fa8a27cd4445541ac2`.

Each return contains one `IRS990ScheduleL` business-transaction record involving an interested person.

| Filing | Interested person as filed | Relationship as filed | Transaction | Amount | Revenue sharing |
|---|---|---|---|---:|---|
| FY2024 | `KARIS L BUICE` | `Daughter of Board Member` | `SALARY` | **$30,409** | `false` |
| FY2025 | `KARIS L BUICE` | `Daughter of Board Member` | `SALARY` | **$31,880** | `false` |

Both Form 990 objects report `EngagedInExcessBenefitTransInd=false`, `BusinessRlnWithFamMemInd=true`, a conflict-of-interest policy, annual disclosure, regular monitoring/enforcement and a compensation-review process. Schedule O says board members discuss potential conflicts and that independent board members determine officer salaries according to market rates and standards.

**Allowed conclusion:** G3 disclosed salary paid to a person identified in the filing as the daughter of a board member. The amount and relationship are now primary filing facts.

**Not allowed:** converting Schedule L disclosure into `self-dealing`, `fraud`, `embezzlement`, `private enrichment` or an excess-benefit finding. The filing itself marks the excess-benefit indicator false. Also, Schedule L says only `Daughter of Board Member`; do not infer the specific parent from surname alone without separate evidence.

### Q002 — What caused the FY2023 expense jump from ~$1.010m to ~$2.072m?

**Status:** `CLOSED / VERIFIED_PRIMARY` at the Form 990 Part IX category-delta level.

The exact FY2023 raw IRS object `202411429349300611` and the amended FY2022 comparator were acquired. Both filings classified **100% of functional expenses as program services**, with management/general and fundraising reported as zero.

Exact row reconstruction:

| Part IX category | FY2022 | FY2023 | Delta |
|---|---:|---:|---:|
| Conferences / meetings | $436,274 | $1,253,557 | **+$817,283** |
| Advertising | $61,063 | $307,574 | **+$246,511** |
| Other salaries / wages | $289,120 | $292,784 | +$3,664 |
| Accounting | $5,400 | $8,995 | +$3,595 |
| Office | $52,793 | $57,252 | +$4,459 |
| Occupancy | $109,578 | $6,627 | **−$102,951** |
| Travel | $12,047 | $25,636 | +$13,589 |
| Depreciation | $11,177 | $15,138 | +$3,961 |
| Workshop / honorarium family | $13,500 | $23,988 | +$10,488 |
| Donor expenses | $11,875 | $10,000 | −$1,875 |
| Information technology | $0 | $28,707 | +$28,707 |
| Payroll taxes | $0 | $41,728 | +$41,728 |
| Dues / subscriptions | $7,359 | $0 | −$7,359 |
| **Total** | **$1,010,186** | **$2,071,986** | **+$1,061,800** |

The category deltas reconcile exactly to the total increase. Conference/meeting spending rose by **$817,283** and advertising by **$246,511**; together their increase slightly exceeds the total net increase because other categories, especially occupancy, moved downward.

**Allowed conclusion:** the filed expense jump was overwhelmingly a conference/event-and-advertising expansion at the Part IX row level. Payroll did not drive the reversal, and the filings do not show an administrative/fundraising-overhead spike.

**Boundary:** Form 990 classification is self-reported accounting evidence, not an independent forensic audit of prudence, pricing or arm’s-length terms.

**Asset follow-up now materially closed:** FY2022 Schedule M/D report one **$590,000 commercial-real-estate contribution**, consisting of $354,000 land + $236,000 buildings. Exact FY2023 raw Form 990 then reports `GrossAmountSalesAssetsGrp/OtherAmt = $550,000`, `LessCostOthBasisSalesExpnssGrp/OtherAmt = $590,000`, and `GainOrLossGrp/OtherAmt = −$40,000`; the $590,000 land/building balance disappears and only equipment remains. Thus the filings identify the FY2023 disposition of the donated $590,000 real-estate accounting object for **$550,000 gross proceeds with a $40,000 loss**. Counterparty, exact parcel and financing terms remain Q006A rather than Q002.

### Q003 — What was the exact G3 governing board immediately before the August 2026 crisis?

**Status:** `PARTIAL CLOSURE / VERIFIED_PRIMARY AS OF 2026-07-21 / LATE-AUGUST CONTINUITY IRREDUCIBLE ON CURRENT WAYBACK PATH`.

The exact official G3 `Who We Are` Wayback snapshot at timestamp `20260721102641` has been acquired and decoded. It explicitly labels **Board of Directors** and names:

- Buck Braswell;
- Matt Broome;
- Jon Norton;
- Matt Sikes;
- Dylan Joyner;
- Ron Mooney.

The archived payload and decoded HTML were independently hashed in the acquisition lane. The six-name roster is therefore no longer a secondary claim: it is **primary official-page evidence for July 21, 2026**.

A corrected Wayback continuity acquisition removed `collapse=digest` and queried the exact official path `g3min.org/about/who-we-are/` from **2026-07-21 through 2026-08-31**. Exact-head run `34219682146` returned:

- `CDX_CAPTURE_COUNT = 1`;
- only timestamp `20260721102641`;
- one digest;
- all six names present in that sole capture.

This documents **archive-search exhaustion for that exact path/window**. It does **not** prove that the roster remained unchanged through the late-August crisis; absence of a later snapshot is not continuity evidence.

**Remaining proof gate:** another primary object dated after July 21 — board minutes, resignation/appointment record, a different archived official surface, participant communication or equivalent — is required to say that the exact late-August board was unchanged.

### Q004 — When and why did Tom Buck, Jonathan Frazier, Chip Thornton, Adam Burrell and others leave the G3 board?

**Progress:** raw FY2024 Part VII directly identifies Buck, Thornton, Braswell, Burrell, Broome and Frazier as directors, with Joshua Buice as president/director. Raw FY2025 Part VII contains dated/transition-style role labels for Scott Aniol, Joshua Buice, Jonathan Frazier, Jon Norton, Buck Braswell, Matt Broome, Tom Buck, Chip Thornton and Adam Burrell, while the filing reports only **4 voting governing-body members, all 4 independent**. Thus Part VII is a reportable-person/role-history list, not a simple four- or nine-person snapshot.

Contemporaneous evidence keeps Tom Buck on the board at the May 12, 2025 Buice-crisis decision point. Current B1 testimony places his exit after May 12 and before Aniol’s official presidency effective July 9, 2025.

**Needed:** board minutes, resignation instruments, archived transition pages or first-person statements establishing exact departure dates and reasons. In particular, do not infer motives from later conflict narratives.

### Q005 — Was G3 legally dissolved in Georgia or merely operationally wound down?

**Status:** `CLOSED AS OF 2026-09-08 ACQUISITION / VERIFIED_PRIMARY`.

The Georgia Secretary of State official Business Search result for control no. `19085916` lists:

- `G3 Ministries for the Church, Inc.`;
- Domestic Nonprofit Corporation;
- status **`Active/Compliance`**;
- principal office `4979 Highway 5, Douglasville, GA 30135`;
- registered/designated agent `Scott Aniol`.

**Allowed conclusion:** at the dated official acquisition, G3 was **not shown as formally dissolved in Georgia** even though operations had publicly wound down.

**Boundary:** corporate status is time-sensitive. A later dissolution filing can change this answer and should be monitored. Federal tax-exempt status is a separate layer and must not be substituted for Georgia corporate status.

### Q006 — What happened to G3 Press, G3+, trademarks, subscriber relationships and other IP/assets?

**Status:** `OPEN / EVIDENCE_HOLD`.

Subscriber reporting supports that G3+ was to be acquired/transitioned to an unnamed `another ministry`; secondary reporting says the same unnamed ministry may receive/acquire G3 Press. No primary source currently names the transferee or supplies transaction terms.

Fresh Sep. 8 searches still do not surface a recipient-side announcement naming the acquirer. The most current reporting continues to describe `another`, as-yet-unnamed ministry. This is a negative search result, not proof that no transfer closed privately.

Current platform evidence shows G3-branded/storefront continuity and Treefort technical-platform involvement, but platform seller/developer metadata cannot establish beneficial ownership, asset-transfer completion, consideration or transaction counterparties. Living Heritage currently offers access that includes G3+ and has historic institutional ties to G3; its own May 17, 2026 privacy policy separately described G3 Ministries as the operator of G3+ while Living Heritage was a separate curriculum publisher. That pre-crisis separation plus current bundling supports a supplier/access relationship, **not proof that Living Heritage acquired G3+ or G3 Press**.

The FY2024/FY2025 Schedule L records do **not** identify a Living Heritage/G3+ transfer; they disclose the salary transaction described in Q001. Do not use Schedule L as circumstantial proof of the asset-transfer theory.

**Needed:** primary subscriber notice, board/corporate announcement, recipient-ministry announcement, transfer agreement, exact asset schedule, consideration/value, conflicts/recusals and closing date. Keep title-level author-rights reversions separate from platform/catalog ownership.

### Q006A — What happened to the donated FY2022 real estate and the FY2023 note/receivable?

**Status:** `PARTIAL CLOSURE / SALE VERIFIED_PRIMARY / PARCEL + COUNTERPARTY + NOTE LINKAGE OPEN`.

Raw FY2022 Schedule M reports one **$590,000 commercial-real-estate donation**; Schedule D reports **$354,000 land + $236,000 buildings = $590,000**.

Exact FY2023 raw Form 990 reports:

- gross amount from sale of `Other` assets: **$550,000**;
- cost/basis of those assets: **$590,000**;
- gain/loss: **−$40,000**;
- beginning net land/building/equipment: **$621,915**;
- ending net land/building/equipment: **$16,777**, fully accounted for by remaining equipment;
- new `OthNotesLoansReceivableNetGrp/EOYAmt`: **$416,227**.

Because FY2022 contains a single $590,000 commercial-real-estate contribution and exactly $590,000 of land/building value, while FY2023 reports a $590,000-basis asset sale and the entire land/building amount disappears, the filings identify the disposition of that donated real-estate accounting object in FY2023 for **$550,000 gross proceeds and a $40,000 loss**.

A common rendered summary labels this only as `Sales of Assets −$40,000`; that **−$40,000 is the loss, not the sale price**.

The simultaneously appearing **$416,227 notes/loans receivable** makes seller financing plausible, but the raw filing does not name the debtor or explicitly connect the note to the sale. The difference between $550,000 gross proceeds and $416,227 receivable is $133,773, but arithmetic coexistence is not transaction identity.

**Official-record acquisition status:** Douglas County/Georgia DOR authority pages are reachable. qPublic is Cloudflare-blocked in the research runtime. The GSCCCA public Real Estate Name Search form was acquired with its real Douglas County parameters and submitted unauthenticated, but each result is automatically redirected into `frmLogin`; no subscription/login/payment bypass was attempted. Wayback/search failure and registry access gates are not negative evidence.

**Needed now:** exact parcel/legal description, donor/grantor, purchaser/grantee, cash at closing, note/security instrument, interest/maturity/collateral, subsequent receivable collection/write-down, board authorization and conflict handling. Related-party or wrongdoing conclusions remain prohibited until those records exist.

## P1 — blocks strong narrative wording

### Q007 — Can the strongest Buck plagiarism examples be independently reproduced from original sermon audio?

Priority: Titus 2:11–15, Aug. 6, 2023, including cited marriage illustration around ~34:09.

**Needed:** original FBC/Vimeo audio and source commentary edition/page, exact transcript locator.

### Q008 — How many of the dossier’s ~45 alleged parallels are severe, moderate, weak or ordinary commentary dependence?

All 17 accusation-sermon items now have dedicated forensic files. **0/17 are declared `ITEM_VERIFIED`** because human-checked original audio, exact source edition and attribution context remain common closure gates.

Continue the row-level classification:

- verbatim extended borrowing;
- near-verbatim borrowing;
- appropriation of unique/personal illustration;
- close paraphrase;
- exegetical sequencing;
- structural similarity;
- commonplace theological overlap.

No global `45 proven instances`, `X% plagiarized` or `17 sermons plagiarized` verdict is permitted until those gates close.

### Q009 — Who physically prepared and mailed the 2026 packets?

**Established:** anonymous external circulation; recipient evidence for Texas postmark/false return address; participants admitted improper anonymous action.

**Not established:** every person’s physical act, use of gloves, exact mailing chain, source of return-address data.

### Q010 — Did deacons/congregation request the four PMBC elders’ resignations, or were resignations volunteered before such a request?

Their reproduced letter says all four voluntarily resigned; Michelle Lesley reports three were required by deacons and Dylan Joyner resigned voluntarily. These accounts may be procedurally reconcilable, but no primary PMBC deacon/congregational record has been acquired.

**Needed:** contemporaneous PMBC documentation or direct statement from authorized church representatives.

### Q011 — Was the stated motive correction/accountability, retaliation, institutional self-protection, or a mixture?

Motive requires communications or participant testimony. Conduct can be established without inventing motive.

### Q012 — Did any G3 board/staff member know about Josh Buice’s anonymous accounts before May 2025?

Official G3 statement says no. No contrary primary evidence currently acquired.

## P2 — history / institutional interpretation

### Q013 — Quantify G3’s ideological shift rather than describe it impressionistically

Construct a dated content sample from 2012–2026 across categories: gospel/church/Scripture, social justice/CRT, gender/sexuality, state/politics, Christian nationalism, worship, missions, education.

Current qualitative evidence already rejects a one-directional `ever farther right` narrative: social-justice/CRT became a stronger boundary after 2018, while 2023 G3/Scott Aniol material explicitly resisted Christian Nationalism/theonomy and drew criticism from the right flank.

### Q014 — Reconstruct conference attendance using primary/contemporary records

Need year-by-year numbers, venue changes and whether registrations vs actual attendance are being compared.

### Q015 — Reconstruct G3’s relationship network

Map G3 ↔ Pray’s Mill ↔ Founders ↔ Grace Community Church/TMS ↔ GBTS ↔ Just Thinking ↔ Religious Affections ↔ T4G-era speakers. Distinguish friendship/speaker overlap from formal institutional control.

### Q016 — January 2021 MacArthur “live” episode

Need independent copies/archives of:

- G3 promotional email calling event live;
- G3Conference tweets;
- Buice Oct. 4, 2020 post establishing recording timing;
- Jan. 7, 2021 Buice replies (“few weeks” / “early October”);
- any correction/explanation issued by G3.

Current source is polemical compilation; episode stays below quote-safe threshold.

### Q017 — What happened institutionally after Michael O’Fallon left in June 2023?

O’Fallon’s own participant post establishes that **he resigned** from G3 (along with other organizational roles). Therefore wording such as `G3 removed O’Fallon` is blocked. Exact board action and causal relationship to Christian-nationalism disputes remain unresolved.

### Q018 — Did G3’s 2025 “renewed vision” change actual governance or mostly messaging/products?

Compare board structure, policies, reporting mechanisms, conflict separation and decision-making before/after May 2025. Raw FY2025 filing and the primary July 2026 board page now provide stronger endpoints for this comparison.

## P3 — shutdown / legacy

### Q019 — What remains online, who controls domains/apps and which pages are stale?

The evidence layers visibly conflict in useful ways:

- direct `https://g3min.org/` returned HTTP 503 on the controlled Sep. 7 observation;
- older crawled/indexed deep pages still exposed pre-shutdown event/product links;
- app-store surfaces retained G3 developer/seller metadata;
- Pray’s Mill’s Sep. 7 leaders-page capture still listed resigned leaders and stale institutional bios.

These are evidence of **stale or lagging digital state**, not proof that resignations, shutdown or institutional changes were reversed.

**Needed:** DNS/domain ownership, hosting transitions, app-store seller history, fresh controlled captures and archived page-change timestamps.

### Q020 — What is the status of authors’ rights and inventory at G3 Press?

Dave Jenkins publicly reported title-level rights return for *The Word Matters* and his current publishing ecosystem now carries the title. Darrell Harrison’s public statement establishes a request/intention to recover rights, not completed reversion. Justin Peters/Andrew Rappaport content-removal requests concern hosting/licensing and must not be conflated with book copyright ownership.

Continue title-by-title rights/inventory reconstruction and obtain legal/primary transfer objects where possible.

### Q021 — What is Scott Aniol’s post-G3 institutional status beyond GBTS?

GBTS officially says he no longer serves on faculty. Pray’s Mill’s captured page still said he was professor, but that page is demonstrably stale against the later event-specific GBTS statement and cannot control present status. Other alleged/announced positions require current primary confirmation; do not infer disciplinary causation without statements.

### Q022 — When did Pray’s Mill update its public leadership records after the August resignations?

As of the 2026-09-07 crawl, the official PMBC leaders page still presented the four resigned men as pastors. This creates a bounded communications/archive question, not an office-status question.

**Needed:** archive snapshots before/after correction, any PMBC public explanation, and page modification evidence if available.

**Current status:** `ARCHIVE_HOLD`.

## Closure definition

The corpus can be considered **article-ready** only when:

1. all P0 questions are either verified or explicitly irreducible with documented search effort;
2. every high-impact allegation in `CLAIMS_LEDGER.md` is `VERIFIED_PRIMARY`, `CORROBORATED`, `REFUTED`, or intentionally presented as uncertainty;
3. financial and board tables have source/version locators;
4. quotes meet repository quote-safe contract;
5. media has item-level rights decisions;
6. article draft preserves the distinction between fact, testimony, interpretation, theological judgment and legal conclusion;
7. stale website/search/app metadata is explicitly dated and never substituted for event-specific evidence.
