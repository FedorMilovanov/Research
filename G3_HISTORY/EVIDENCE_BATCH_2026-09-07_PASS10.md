# G3 HISTORY — evidence batch 2026-09-07 PASS10

**Status:** STAGING / PUBLICATION_HOLD  
**Purpose:** convert the vague `archived late-board` lead into a timestamped, exact archive target while preserving the distinction between archive-locator verification and direct snapshot-content verification.

## Provisional sources

| ID | Source | Class | Access | Use | Notes |
|---|---|---|---|---|---|
| G3-S096 | Wayback snapshot target for G3 `Who We Are`, timestamp `20260721102641` | A2 original-page archive target | EXACT_ARCHIVE_LOCATOR_VERIFIED / SNAPSHOT_CONTENT_ACCESS_HOLD | late-board roster | Evangelical Dark Web’s Aug. 19 and Aug. 26 articles link their phrase `recently archived board` directly to `https://web.archive.org/web/20260721102641/http://g3min.org/about/who-we-are/`. Clicking the link in the research browser exposes the exact Wayback URL/timestamp but Wayback returns cache miss through the current transport, so the archived page body itself has not been independently read in this environment. Original G3 path: `http://g3min.org/about/who-we-are/`; capture timestamp: **2026-07-21 10:26:41 UTC**. |
| G3-S097 | Evangelical Dark Web, `G3 Ministries Caught Launching Shadow Campaign To Persecute Tom Buck`, 2026-08-19 | C | FULL_OBJECT_VERIFIED / EXACT_LOCATOR_VERIFIED / DIRECT_WAYBACK_LINK_VERIFIED | late-board archive lead / Norton reporting | The article states that the most recently archived board listed Buck Braswell, Matt Broome, Jon Norton, Matt Sikes, Dylan Joyner and Ron Mooney and links that claim directly to G3-S096. It separately reproduces Protestia reporting that Norton was a current G3 board member. Polemical conclusions/motive claims are not inherited. Locator: `https://evangelicaldarkweb.org/2026/08/19/g3-caught-launching-shadow-campaign-to-persecute-tom-buck/`. |
| G3-S098 | Evangelical Dark Web, `G3 Finally Responds: Ends Church Network Subscription`, 2026-08-26 | C | FULL_OBJECT_VERIFIED / EXACT_LOCATOR_VERIFIED / DIRECT_WAYBACK_LINK_VERIFIED | duplicate archive-link corroboration | Independently within a later article by the same outlet, the same six-name roster is again tied to the exact same Wayback snapshot target. This is **not a second independent witness** to roster content; it confirms the outlet consistently meant one specific archived object. Locator: `https://evangelicaldarkweb.org/2026/08/26/g3-finally-responds-ends-church-network-subscription/`. |

## Provisional claims

| ID | Claim | State | Support / boundary |
|---|---|---|---|
| G3-C125 | The previously vague `latest archived G3 board` lead now resolves to a specific G3 `Who We Are` Wayback capture dated 2026-07-21 10:26:41 UTC. | VERIFIED_PRIMARY_LOCATOR | G3-S096 + direct outgoing-link inspection from G3-S097/G3-S098. This verifies archive object identity, not yet its body text. |
| G3-C126 | The 2026-07-21 G3 `Who We Are` snapshot directly displays the six-person roster Braswell/Broome/Norton/Sikes/Joyner/Mooney. | PARTIALLY_VERIFIED / SNAPSHOT_CONTENT_HOLD | G3-S097 and G3-S098 both attribute exactly that roster to G3-S096, but the research transport cannot read the Wayback body. Do not yet upgrade the roster to `VERIFIED_PRIMARY`. |
| G3-C127 | The six-person late-board claim is merely an untraceable assertion with no identifiable archive object behind it. | REFUTED | Exact Wayback timestamp and original path are now fixed at G3-S096. The remaining gap is content acquisition, not locator discovery. |
| G3-C128 | Buck Braswell’s board status at least through Feb. 6, 2026 is primary-supported independently of the July archive claim. | VERIFIED_PRIMARY | Existing official G3 Braswell pages (canonical late-board anchors). This gives one independently verified member inside the six-name secondary roster. |
| G3-C129 | The July 21 snapshot, if content-confirmed, would establish the exact board at the August crisis without further date caveat. | INFERENCE / DATE_BOUNDARY | A July 21 roster would be a very close pre-crisis snapshot, but a board change between July 21 and Aug. 2026 remains logically possible. For `immediately before crisis` wording, search for later captures/board actions as well. |

## What changed for Q003

Previous state:

`secondary six-name list / unknown archive object / ARCHIVE_HOLD`

New state:

`exact official-page archive target known / timestamp known / body transport-blocked`

This is a material improvement. The next acquisition is no longer `find the archive`; it is:

1. retrieve snapshot `20260721102641` through a transport that can read Wayback content;
2. preserve the page body/screenshot and checksum;
3. identify every person displayed in the board section and surrounding role labels;
4. search for captures between **2026-07-21 and the Aug. 2026 crisis** to exclude a subsequent roster change;
5. compare with FY2025 Part VII and individual official bios.

## Article-safe wording now

Safe:

> A contemporary secondary report tied its six-name late-board reconstruction to a specific archived G3 `Who We Are` page captured on July 21, 2026. The archive locator is now verified, but the snapshot body remains inaccessible through the current research transport, so the full roster is not yet treated as primary-verified.

Not yet safe:

> On the eve of the scandal, G3’s board definitively consisted of Braswell, Broome, Norton, Sikes, Joyner and Mooney.

## Duplicate-count guardrail

G3-S097 and G3-S098 point to the **same Wayback object**. They are not two independent confirmations of the six-person roster. Their evidentiary value is that two contemporaneous references by the same outlet expose the exact archive target consistently.
