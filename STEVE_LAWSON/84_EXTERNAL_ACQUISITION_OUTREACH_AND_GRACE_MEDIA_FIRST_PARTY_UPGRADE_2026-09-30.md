# Steven J. Lawson — external acquisition outreach and Grace Media first-party upgrade

**Snapshot:** 2026-09-30  
**Status:** `ACTIVE OUTBOUND ACQUISITIONS / PUBLIC-WEB SELF-SERVICE EXHAUSTED FOR THESE ITEMS / FIRST-PARTY GRACE MEDIA OBJECTS LOCATED`  
**Authority:** extends `81_`, `82_`, `83_`; does not reopen V6.

## 1. Purpose

The remaining biography/media gaps are no longer left as passive backlog. On 2026-09-30, exact requests were sent to the repositories or institutional holders most likely to possess the unresolved primary objects.

Rule:

> **A remaining item is now either closed by a source already in main, or attached to a concrete external acquisition request. Do not restart generic web crawling for the same object while an authoritative holder is being queried.**

This file also records a material provenance upgrade for Shepherds Conference 2006/2007: current official Grace Church App catalog objects now exist for the relevant sessions, independent of the legacy S3 filenames.

---

## 2. Shepherds Conference 2007 — current first-party catalog objects

### 2.1 General Session 2 — official Grace Church object

Current first-party object:

- `https://app.gracechurch.org/media/player/333`
- title: `General Session 2`
- date: `March 7, 2007`
- series: `Shepherds Conference 2007`
- details: `The Passion and Power of Apostolic Preaching`
- page exposes: `Download MP3 File (EN)`

The current Grace card does **not** display a teacher name in the indexed result. Near-contemporary reports already recorded in the biography lane identify Steve Lawson with Session II on March 7 and the Acts 2 apostolic-preaching session. Therefore:

> **Session identity/title/date = first-party official. Lawson speaker attribution = strongly supported by near-contemporary reports, but the current card itself is not used to manufacture a missing teacher field.**

This materially improves provenance over a bare S3 key or a later SermonAudio match.

### 2.2 General Session 8 Q&A — official Grace Church object

Current first-party object:

- `https://app.gracechurch.org/media/player/339`
- title: `General Session 8 - Q&A`
- teacher: `Keynote Panel`
- date: `March 9, 2007`
- details: `Q & A with Keynote Panel`
- page exposes: `Download MP3 File (EN)`

This confirms the event/session identity independently of the legacy candidate:

- `https://s3.amazonaws.com/media.shepherdsconference.org/2007/SC-2007-GS08-PANELK.mp3`

The actual MP3 bytes are not in custody yet because the current research runtime cannot follow the download path to binary bytes. Grace Media has therefore been asked for the direct current MP3 URL, legacy filename, panel list, and transcript if retained.

### 2.3 Shepherds Conference 2007 series

Current official series object:

- `https://api.gracechurch.org/news/series/325`
- `Shepherds Conference 2007`
- current series result exposes 35 messages and includes General Session 2 and General Session 8 in chronology.

This is a current institutional catalog layer and supersedes any assumption that the 2007 media survives only through orphaned legacy storage.

---

## 3. Shepherds Conference 2006 — current first-party Q&A object

Current first-party object:

- `https://app.gracechurch.org/media/player/287`
- title: `General Session 7 - Q&A with Keynote Panel`
- teacher: `Keynote Panel`
- date: `March 3, 2006`
- series: `Shepherds Conference 2006`
- details: `Friday Afternoon`
- page exposes: `Download MP3 File (EN)`

This independently confirms the identity of the legacy candidate:

- `https://s3.amazonaws.com/media.shepherdsconference.org/2006/SC-2006-GS07-PANELK.mp3`

Again, official catalog provenance is now closed; byte-level acquisition/transcription remains dependent on a working download route or response from Grace Media.

---

## 4. Direct-byte attempts — environment boundary

Three independent execution routes were tested for target media:

1. ordinary web open — binary URLs are not fetchable by the text web layer;
2. container/Python HTTP — runtime has no usable DNS egress to `churchandfamilylife.com` or `s3.amazonaws.com`;
3. authorized Remote Desktop Commander device — the only registered device is currently offline.

Therefore:

> **Failure to acquire bytes in the present session is an environment/network limitation, not evidence that the files are absent.**

Do not convert these failures into negative source findings.

---

## 5. Church & Family Life — active source request

Current public CFL pages still establish the episode records/synopses, while pass 48 derived two first-party-pattern candidate routes:

- Part 1 page ID: `65b01c4fad65a9d0a93e4e34`
- Part 2 page ID: `65ba8d2a33d020a85626fd6e`
- Part 1 historical YouTube ID: `dyP6ihi8znw`
- candidate Part 1 audio: `https://churchandfamilylife.com/s3/assets/podcasts/65b01c4fad65a9d0a93e4e34/audio.mp3`
- candidate Part 2 audio: `https://churchandfamilylife.com/s3/assets/podcasts/65ba8d2a33d020a85626fd6e/audio.mp3`

A current official app listing identifies Church & Family Life support as `info@cf.life` (with `colton@cf.life` as app support on another current listing). A source-verification request was sent to `info@cf.life` asking for direct audio URLs/files, transcripts/captions, duration/date metadata, and confirmation or rejection of the candidate paths.

Classification until response:

> **candidate first-party routes / active holder request / no byte receipt yet.**

---

## 6. Outbound acquisition ledger — dispatched 2026-09-30

### A. Reformed Theological Seminary — D.Min. project/title

Recipient: `library.jackson@rts.edu`  
Official contact source: RTS Jackson Library / RTS Library contact pages.  
Requested:

- exact Steven J. Lawson D.Min. major-project/dissertation title;
- author form;
- completion/graduation date;
- call number/catalog permalink/project identifier;
- abstract/TOC if public;
- confirmation if record is restricted or not retained.

Known institutional anchor supplied in request: `Steven Lawson (D.Min. '90)` plus official RTS statement that he received the D.Min. while pastoring in Little Rock.

**State:** `SENT / AWAITING HOLDER RESPONSE`.

### B. Texas Tech Southwest Collection / University Archives — football/Picadors + bylines

Recipient: `reference.swco@ttu.edu`  
Official reference desk source: Texas Tech Southwest Collection/Special Collections.  
Requested:

- Picadors/freshman football rosters, pressbooks, media guides, squad lists, scholarships/letters, team photographs ca. 1969–1973;
- varsity references to Steven/Steve Lawson;
- La Ventana / University Daily references;
- student-publication bylines/staff records relevant to the 1992 publisher claim that Lawson covered the Texas Rangers and Dallas Cowboys.

Known evidence supplied:

- official May 12, 1973 TTU commencement record places Steven James Lawson under B.B.A.;
- official RTS 2013 profile says he was recruited at quarterback and shifted to wide receiver at Texas Tech;
- previous archive work located physical football/Picadors pressbook holdings.

**State:** `SENT / AWAITING HOLDER RESPONSE`.

### C. Florida State University Special Collections — Tampa Times wedding page

Recipient: `lib-specialcollections@fsu.edu`  
Official FSU Special Collections contact.  
Requested research/duplication scan:

- *The Tampa Times*;
- April 20, 1981;
- page 14;
- Steve/Steven Lawson — Anne Crowell wedding item;
- ideally complete page, including the indexed `Wed Article (pt 1)` / related parts / photograph.

Known physical locator supplied:

- FSU `Film NP 367`, *The Tampa Times*, Jan. 1947–Aug. 1982.

**State:** `SENT / AWAITING HOLDER RESPONSE`.

### D. University Baptist Church, Fayetteville — early ministry dates/role

Recipient: `info@ubcfayetteville.org`  
Official current UBC contact.  
Requested:

- exact Lawson role/title;
- start/end dates around 1980–1981;
- whether college pastor/associate/minister/other;
- bulletin/directory/newsletter evidence;
- timing of departure toward The Bible Church of Little Rock if recorded.

Known anchor supplied: contemporary April 1981 newspaper identifies Lawson as a minister at UBC Fayetteville.

**State:** `SENT / AWAITING HOLDER RESPONSE`.

### E. The Bible Church of Little Rock — exact pastorate chronology

Recipient: `info@bclr.org`  
Official current church contact.  
Requested:

- exact start/end dates;
- formal title(s);
- installation/farewell/annual-report/bulletin/directory evidence;
- any church record of his role in the 1989 Billy Graham crusade.

Known current church history already lists `Dr. Steven J. Lawson` among prior pastors/expositors.

**State:** `SENT / AWAITING HOLDER RESPONSE`.

### F. Wheaton Archives & Special Collections — 1989 Arkansas Crusade scrapbooks

Recipient: `archives@wheaton.edu`  
Official current Archives & Special Collections contact.  
Requested targeted check of:

- CN 074;
- folders 8-2 / 8-3;
- 1989 Arkansas Crusade scrapbooks;
- Steven/Steve J. Lawson;
- Bible Church of Little Rock;
- counseling/follow-up role;
- counselor totals;
- attendance figures.

**State:** `SENT / AWAITING HOLDER RESPONSE`.

### G. Billy Graham Archive & Research Center — Little Rock 1989 campaign record

Recipient: `archives@bgea.org`  
Current BGARC FAQ exposes this Archive email and 704-401-3200; research appointments are required for on-site access.  
Requested:

- Lawson committee role;
- counseling/follow-up rosters;
- final trained/certified/active counselor totals with definitions;
- peak/average attendance;
- final campaign / School of Evangelism / counseling reports;
- box/folder/catalog guidance.

**State:** `SENT / AWAITING HOLDER RESPONSE`.

### H. Grace Media — Shepherds 2007 GS2 / GS8

Recipient: `info@gracemedia.app`  
Official current Grace Media FAQ support address.  
Requested for media IDs 333 and 339:

- direct current MP3/download URLs;
- speaker attribution for 333;
- panel participant list for 339;
- original SC filename / legacy media ID;
- transcript if retained.

**State:** `SENT / AWAITING HOLDER RESPONSE`.

### I. Church & Family Life — Life Story Parts 1–2

Recipient: `info@cf.life`  
Current official app/developer support listing.  
Requested:

- direct audio URLs/files;
- transcripts/captions;
- duration/date metadata;
- confirmation/rejection of candidate audio routes.

**State:** `SENT / AWAITING HOLDER RESPONSE`.

### J. Texas Rangers — sportswriter provenance

Recipients:

- `publications@texasrangers.com`;
- CC `communications@texasrangers.com`.

Official Rangers contact page exposes both addresses; current front-office material identifies a Senior Advisor/Team Historian role overseeing archives and publications.

Requested check ca. 1971–1974 for Steve/Steven J. Lawson as credentialed writer/reporter/contributor covering the Rangers.

Explicit namesake guardrail included:

- **Steven George Lawson**, born Dec. 28, 1950, Oakland, left-handed pitcher for the 1972 Rangers, is **not** the subject.

**State:** `SENT / AWAITING HOLDER RESPONSE`.

### K. Dallas Cowboys — sportswriter provenance / routing

Recipient: `GuestComments@DallasCowboys.net`  
Official Cowboys current contact page exposes this customer-service route; no direct historical/PR email was publicly exposed in the checked current pages.  
Requested forwarding to football communications/publications/history for any ca. 1971–1974 record of Steve/Steven J. Lawson as writer/contributor/reporter.

**State:** `SENT / AWAITING HOLDER RESPONSE`.

---

## 7. Public-web findings added during the outbound pass

### BCLR current history

Current official church history explicitly lists:

- `Dr. Steven J. Lawson`

among pastors/expositors who led The Bible Church of Little Rock.

This strengthens institutional identity continuity but still does not supply exact start/end dates.

### UBC current historical continuity

Current official UBC history identifies the Fayetteville congregation as founded in 1953 and still operating at 333 W Maple Street. This verifies that the request is being sent to the same continuing congregation, not a guessed successor entity.

### Texas Rangers namesake trap is decisively documented

Current authoritative baseball sources identify another man:

- `Steven George Lawson`;
- born Dec. 28, 1950, Oakland, California;
- left-handed pitcher;
- 13 games for the Texas Rangers in 1972.

This namesake dominates ordinary search for `Steve Lawson + Texas Rangers`. Any future sportswriter research must exclude him explicitly.

### Rangers archival route is real

The current Texas Rangers front office includes a `Senior Advisor/Team Historian`, John Blake, whose official role includes archives and publications. The public contact page exposes Publications and Communications email routes. Therefore the sportswriter question now has a legitimate team-level archival path rather than only generic search.

---

## 8. What is now genuinely left

After this pass, no material biography/media P1 remains as an unowned generic-search task.

Outstanding items are now response- or access-dependent:

1. RTS D.Min. project bibliographic record — holder queried;
2. TTU football/Picadors and possible bylines — holder queried;
3. Tampa Times page 14 scan — holder queried;
4. UBC exact role/dates — church queried;
5. BCLR exact dates — church queried;
6. 1989 crusade archival calibration — Wheaton + BGARC queried;
7. SC2006/2007 direct MP3/transcripts — Grace Media queried; first-party catalog identity already upgraded;
8. CFL Life Story audio/transcripts — CFL queried;
9. sportswriter claim — TTU + Rangers + Cowboys queried.

This is the correct definition of `near-zero` for the current session:

> **all self-service public research routes are either closed, source-bounded, or converted into active requests to the primary holder.**

No honest research system can manufacture an archive response before the archive supplies it.

---

## 9. Article impact

None of these pending acquisitions is a V6 blocker.

Current article state remains:

> `PASS / PUBLICATION_READY_WITH_GUARDRAILS / NO V7 TRIGGER`.

A future response should change V6 only if it creates a genuine Tier-A contradiction under `70_` / `81_`. Otherwise it belongs as a biography precision upgrade or custody receipt.
