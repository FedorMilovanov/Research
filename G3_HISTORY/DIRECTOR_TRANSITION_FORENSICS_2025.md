# G3 2025 director-transition forensics

**Status:** ACTIVE / DATE-BOUNDED / PUBLICATION_HOLD  
**Cutoff:** 2026-09-08  
**Purpose:** establish the strongest supportable dates for G3 board transitions after the May 2025 Josh Buice crisis without converting later testimony, Form 990 reporting rows, or archive gaps into exact resignation dates.

## 1. Why this file exists

The 2025 governance transition is easy to misstate because several evidence types describe different things:

- contemporaneous public reporting and social statements identify people serving on the board around the May crisis;
- a later official G3 announcement identifies Jonathan Frazier as board chairman and Scott Aniol as president;
- the FY2025 Form 990 contains reportable-person role-history rows but reports only four voting governing-body members;
- later testimony says Tom Buck stepped off the board between the Buice crisis and Aniol's presidency;
- the official `Who We Are` path has no Wayback captures for the critical May–July interval.

These layers can narrow a window. They do not supply an exact resignation instrument.

## 2. May 2025 — Tom Buck is still publicly anchored as a G3 board member

Contemporaneous May 2025 reporting explicitly identifies Tom Buck as a G3 board member during the Josh Buice crisis.

Christianity Today describes Buck as a Texas pastor and G3 board member and reproduces his public reaction to the crisis. ChurchLeaders likewise reports the board as including:

- Tom Buck;
- Chip Thornton;
- Buck Braswell;
- Adam Burrell;
- Matt Broome;
- Jonathan Frazier.

Buck's own public wording, reproduced in the reporting, says he was thankful for `all the men on the G3 Board` and stood behind `our decision`. This strongly anchors his participation in the board's handling of the Buice matter.

### Date boundary

The public crisis announcement and reactions cluster around **2025-05-12**, following the board's May 8 acceptance of Josh Buice's resignation.

**Allowed:** Tom Buck was serving as a G3 board member at the public May 2025 Buice-crisis decision point.

**Not allowed:** treating a later FY2025 Form 990 `DIRECTOR` row as proof that Buck remained on the board through Dec. 31, 2025. Part VII is a tax-period reportable-person surface, not a one-date roster.

## 3. July 2025 — official G3 leadership endpoint

G3's official announcement `Scott Aniol Named President of G3 Ministries`, published **2025-07-14**, states that Scott Aniol's presidency was effective **Wednesday, 2025-07-09**.

The same official announcement quotes:

**Jonathan Frazier — `Board Chairman, G3 Ministries`.**

This is an event-specific primary endpoint for Frazier's leadership role and Aniol's formal presidency.

### Date-conflict firewall

The FY2025 Form 990 later labels Aniol `PRESIDENT AS OF 05/2025`. That tax-return wording must not silently replace the event-specific official appointment date of **2025-07-09**. It may reflect retrospective/preparer shorthand or a transition period.

For the formal public appointment event, July 9 controls unless stronger corporate minutes or resolutions supersede it.

## 4. Tom Buck exit window

A September 2026 interview with David Morrill, who investigated the later Buck/G3 dispute, states that Buck:

- was on the G3 board;
- stepped off after the Josh Buice episode;
- stepped off before Scott Aniol became president.

This is useful witness/investigator testimony, but it is not Buck's resignation letter, board minutes, or a corporate filing.

Combined with the dated public endpoints, the strongest current supportable formulation is:

> **Tom Buck's G3-board exit is reported to have occurred after the May 2025 Buice crisis and before Scott Aniol's presidency became effective on July 9, 2025. The exact resignation date and instrument have not been obtained.**

### Evidence state

`SUPPORTED / B1 TESTIMONY + DATED ENDPOINTS / EXACT DATE OPEN`

Do not upgrade this to `VERIFIED_PRIMARY exact resignation date` without:

- Buck's first-person resignation statement;
- board minutes/resolution;
- dated corporate board record;
- or another contemporaneous primary object explicitly recording the departure.

## 5. Official-page Wayback acquisition — bounded negative result

A dedicated exact-head Research lane tested the official historical page:

`http://g3min.org/about/who-we-are/`

for the transition window.

Workflow:

`G3 Wayback 2025 board transition acquisition`

Successful run:

`34228201641`

Exact Research head:

`a4d53a1a1e6be488d60dc607d61ace68c3cba903`

The CDX query was split into independent monthly segments after a broad query produced a gateway timeout. Each segment completed with valid JSON and no captures:

| Segment | CDX state | Captures |
|---|---|---:|
| 2025-05-01 → 2025-05-31 | `VALID_EMPTY_CDX` | 0 |
| 2025-06-01 → 2025-06-30 | `VALID_EMPTY_CDX` | 0 |
| 2025-07-01 → 2025-07-20 | `VALID_EMPTY_CDX` | 0 |
| **Combined** | `VALID_EMPTY_ALL_SEGMENTS` | **0** |

Distinct digests: **0**.

### What this means

The exact official `Who We Are` path has no Wayback coverage in the tested May 1–July 20, 2025 interval.

### What this does NOT mean

It does not prove:

- that the board page did not exist;
- that no board change occurred;
- that Buck remained or departed on any specific date;
- that Frazier's chair role began on any specific date before the July announcement;
- that Wayback has no relevant material at a different historical URL.

The exact-path search is now **exhausted** and should not be repeated absent evidence that the historical URL differed.

## 6. FY2025 Form 990 — role history, not a roster snapshot

The raw FY2025 return reports:

- **4 voting governing-body members**;
- **4 independent**.

Part VII nevertheless contains reportable role rows for more than four people, including:

- Scott Aniol — `PRESIDENT AS OF 05/2025`;
- Buck Braswell — `DIRECTOR`;
- Matt Broome — `SECRETARY` / director indicator;
- Jonathan Frazier — `CHAIR` / director indicator;
- Jon Norton — `DIRECTOR`;
- Joshua Buice — `PRESIDENT THROUGH 05/2025` / director-officer;
- Tom Buck — `DIRECTOR`;
- Chip Thornton — `DIRECTOR`;
- Adam Burrell — `DIRECTOR`.

Therefore the nine reportable rows cannot be treated as a nine-person year-end board.

The filing is useful for proving that these people held reportable roles during the tax period and for showing governance contraction to four voting members. It is not sufficient to derive exact start/end dates for each director.

## 7. Jonathan Frazier transition state

Primary-closed endpoint:

- by the official July 14 announcement, Jonathan Frazier is explicitly **G3 Board Chairman**.

Later endpoint:

- the official July 21, 2026 `Who We Are` snapshot lists a six-person board that does **not** include Frazier.

Current evidence therefore proves that Frazier was chairman in July 2025 and was no longer on the official six-name board by July 21, 2026.

**Exact exit date remains open.**

Do not infer a reason for his departure without primary testimony/minutes.

## 8. Other May-2025 directors

### Chip Thornton

May 2025 reporting and FY2024/FY2025 tax evidence support board/director service. Exact exit date remains open.

### Adam Burrell

May 2025 reporting and FY2024/FY2025 tax evidence support board/director service. Exact exit date remains open.

### Buck Braswell

Unlike Buck/Thornton/Burrell/Frazier, Braswell has primary continuity into the official July 21, 2026 board snapshot.

### Matt Broome

Likewise has primary continuity into the official July 21, 2026 board snapshot.

## 9. Newer directors visible by FY2025 / July 2026

### Jon Norton

FY2025 raw Part VII contains a director row; July 21, 2026 official page confirms board membership. Exact start date remains open.

### Matt Sikes / Dylan Joyner / Ron Mooney

July 21, 2026 official board page confirms all three. Exact board start dates remain open because the tested May–July 2025 exact path has no Wayback coverage and no separate appointment instrument has yet been acquired.

## 10. Current transition matrix

| Person | Earliest/current strong endpoint | Later strong endpoint | Exact transition state |
|---|---|---|---|
| Tom Buck | board member at May 2025 crisis | later former board member; B1 testimony says exit before Jul 9 presidency | **exact exit date OPEN** |
| Jonathan Frazier | board member May 2025 | official Board Chairman Jul 14, 2025; absent Jul 21, 2026 official roster | **exact exit date OPEN** |
| Chip Thornton | board member May 2025 | FY2025 reportable director history; absent Jul 21, 2026 roster | **exact exit date OPEN** |
| Adam Burrell | board member May 2025 | FY2025 reportable director history; absent Jul 21, 2026 roster | **exact exit date OPEN** |
| Buck Braswell | board member May 2025 | official board Jul 21, 2026 | **continuity strongly supported** |
| Matt Broome | board member May 2025 | official board Jul 21, 2026 | **continuity strongly supported** |
| Jon Norton | FY2025 reportable director row | official board Jul 21, 2026 | **exact start date OPEN** |
| Matt Sikes | — | official board Jul 21, 2026 | **exact start date OPEN** |
| Dylan Joyner | — | official board Jul 21, 2026 | **exact start date OPEN** |
| Ron Mooney | — | official board Jul 21, 2026 | **exact start date OPEN** |

## 11. Next material proof gates

Do not repeat the exhausted May–July 2025 exact-path CDX search.

Material progress now requires one of:

1. a historical alternate G3 board-page URL with archive captures;
2. Buck/Thornton/Burrell/Frazier first-person resignation statements;
3. board minutes or corporate resolutions;
4. dated appointment announcements for Norton/Sikes/Joyner/Mooney;
5. Georgia corporate records that identify directors/officers at a finer date resolution;
6. authenticated internal/subscriber communications that explicitly date board changes.

Until then, the article should use date-bounded wording rather than an invented day-by-day board chronology.
