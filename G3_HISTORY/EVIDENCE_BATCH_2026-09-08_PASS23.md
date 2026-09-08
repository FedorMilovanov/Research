# G3 HISTORY — evidence batch 2026-09-08 PASS23

**Status:** ACTIVE / RECONCILIATION / PUBLICATION_HOLD  
**Scope:** post-PASS22 canonical cleanup, exact-head CI, G3+ subscriber-acquisition artifact, late-board/archive exhaustion and Douglas property-access boundary.

## 1. Exact working head entering PASS23

Research branch `research/g3-history-20260907` was normalized through commit:

`8b311f60e1cd6c84e6988ef3f19af2c1e4c7db96`

The commit promotes the stale Item 13–17 files to the original-media state already established by PASS22. It is a normal fast-forward descendant of the prior Research head; no rebase/force rewrite was used.

`main` remained `b5785be744bc8eac14491b972bb99005f1e81322` during this reconciliation window.

## 2. Buck Item 11–17 normalization is complete at file level

The late seven-item original-media matrix is now reflected in the canonical item files rather than only in PASS22:

- Item 11 — original media confirms the stronger law-dissolution / ordered antithesis material while text-driven Romans 7 analogy remains lower-specificity;
- Item 12 — original media confirms the long Christ-example/preincarnate-glory block; ordinary unity/worship and circulating illustration material remain lower weight;
- Item 13 — original media confirms the five-element Christ-work sequence; generic sonship remains low-specificity;
- Item 14 — original media confirms the sermon content but leaves KNOW/OBEY/MEDITATE at low structural specificity; this is a negative control;
- Item 15 — original media plus the Jackman publisher sample close both sides for several strong Joshua 2 candidates, while common theological rows remain lower weight;
- Item 16 — original media confirms the dense Buck-side cluster, with the improbable-time/trust causal sentence and Jackman-family hermeneutical question strongest; exact Jackman pp. 41–49 remain open;
- Item 17 — original media confirms the distinctive `spiritual memories are very short` phrase family; ordinary remembrance application remains low-specificity.

The global state remains **0/17 `ITEM_VERIFIED`** because machine transcripts are diagnostic rather than human quote-safe listening and because exact source/attribution gates remain open where applicable.

## 3. G3+ subscriber email — acquisition-in-progress evidence materially upgraded

A recipient-supplied screenshot hosted on Michelle Lesley's Aug. 2026 update is now treated as its own controlled underlying artifact.

Exact image locator:

`https://michellelesley.com/wp-content/uploads/2026/08/788262502_10164714609817440_6641838253964191423_n.jpg?w=640`

Lesley identifies the provider as a G3+ subscriber and places the email on Aug. 27, 2026. The visible G3-branded email represents that:

- G3 Ministries was winding down;
- G3 Plus **was being acquired by another ministry**;
- existing subscription/library/price continuity was represented to subscribers;
- the acquiring ministry's name was not yet disclosed;
- a later notice was promised when the transition became final.

This changes the strongest Q006 wording from `vague intended transfer reported` to:

`RECIPIENT_ARTIFACT_VERIFIED / ACQUISITION_IN_PROGRESS_REPRESENTED / TRANSFEREE_UNNAMED / COMPLETED_CLOSING_UNVERIFIED`.

The email does not itself say that G3 Press was included. Press inclusion remains supported only at a weaker recipient-reporting/secondary layer unless a transaction or recipient-side primary object closes it.

Canonical control file staged in this pass:

`PRIMARY_SOURCE_G3PLUS_SUBSCRIBER_EMAIL_2026-08-27.md`.

## 4. Successor identity remains unresolved — two false shortcuts explicitly blocked

### Living Heritage

The FY2025 raw IRS filing states that Living Heritage Homeschool was separated as an independent entity from G3 Ministries during 2025. Later G3+ access/bundling is real service-continuity evidence, but does not establish a 2026 transfer of G3+ ownership.

`Living Heritage acquired G3+` remains `UNVERIFIED`.

### Treefort

Current application privacy/terms/vendor surfaces are consistent with Treefort supplying branded-app/platform infrastructure. A technology vendor relationship does not identify beneficial ownership or the ministry transferee.

`Treefort = acquiring ministry` is therefore blocked as a category error absent a transaction/recipient object.

## 5. Late-board continuity — public Wayback route is now archive-exhausted for the target page

Exact-head workflow:

`G3 Wayback late-board acquisition`  
run `34270062889`  
head `8b311f60e1cd6c84e6988ef3f19af2c1e4c7db96`  
conclusion `success`.

CDX queried the official `g3min.org/about/who-we-are/` page for **2026-07-21 through 2026-08-31** and returned exactly one HTTP-200 capture:

`20260721102641`.

The raw and decoded object again lists Buck Braswell, Matt Broome, Jon Norton, Matt Sikes, Dylan Joyner and Ron Mooney. No later capture appears in the returned CDX universe for that page/window.

**Consequence:** July 21 remains the last primary archived roster available through this exact page/CDX route. The absence of a later capture is not evidence that the roster remained unchanged through late August.

Late-August continuity therefore becomes:

`PRIMARY JULY-21 ROSTER VERIFIED / TARGET-PAGE ARCHIVE ROUTE EXHAUSTED / CRISIS-DAY CONTINUITY DOCUMENT_HOLD`.

A new primary object from another surface, minutes, filing or dated institutional record is required to close the crisis-day roster.

## 6. May–July 2025 board-transition Wayback lane — transient transport failure, not content regression

On the same exact head, run `34270062847` failed in the acquisition step.

The failure is transport-specific:

- May segment: valid empty CDX;
- June segment: valid empty CDX;
- July 1–20 segment: Wayback CDX returned HTTP 503 after three bounded retries;
- acquisition exited code 2 rather than pretending an unavailable segment was empty.

This is the correct evidentiary behavior. The red check is not proof of a repository/content defect and cannot be relabeled green without a successful rerun or a workflow-policy correction that preserves the distinction between `valid empty` and `transport error`.

A single-job rerun was requested in this pass.

## 7. Douglas property/deed route — access boundary established, factual linkage still open

Exact-head workflow:

`G3 Douglas property record acquisition`  
run `34270062808`  
head `8b311f60e1cd6c84e6988ef3f19af2c1e4c7db96`  
conclusion `success`.

Artifact digest:

`sha256:0b8063f380651affb9ec1ec101dcb9c4ef7e13492b13ec2638958d232f2ac6b3`.

Controlled results:

- Douglas County Clerk landing surface: HTTP 200;
- Georgia DOR property-records routing surface: HTTP 200;
- GSCCCA public name-search form: HTTP 200;
- attempted GSCCCA result posts return a login/session shell rather than public deed result rows;
- qPublic search landing and direct search queries for G3/Pray's Mill/address/parcel return Cloudflare HTTP 403.

Therefore the public unauthenticated route has not produced the deed/counterparty/note instrument needed to link:

- FY2022 $590,000 commercial-real-estate contribution;
- FY2023 $550,000 gross sale / $590,000 basis / $40,000 loss;
- FY2023 $416,227 note/loan receivable and later declines.

Seller financing remains plausible but unverified. The 4979 Highway 5 Pray's Mill parcel must not be identified as the donated/sold property without deed proof.

Current state:

`IRS TRANSACTION NUMBERS VERIFIED / PUBLIC PROPERTY ROUTES EXHAUSTED OR ACCESS-CONTROLLED / PARCEL + COUNTERPARTY + NOTE DOCUMENT_HOLD`.

## 8. PMBC resignation mechanics — contradiction survives research pressure

Current evidence still has two incompatible procedural descriptions:

- the four-pastor participant letter, as reproduced, says all four voluntarily resigned;
- secondary reports say three were required by PMBC deacons to resign while Dylan Joyner resigned voluntarily, or otherwise describe deacons insisting on resignations.

The newly acquired Aug. 16 Matt Sikes announcement is useful pre-publication institutional-response evidence but does not resolve the later resignation mechanics.

No acquired PMBC minutes, deacon statement, resignation letters or congregational record settles the contradiction.

State remains:

`DISPUTED / PRIMARY PMBC DOCUMENT_HOLD`.

## 9. MacArthur January 2021 episode — source convergence, not corroboration

Repeat exact-phrase/archive searches continue to converge on the same adversarial compilation reproducing the October recording post, January live-event promotion, `few weeks` replies and later early-October clarification.

No independent archive/original email/social object was acquired in this pass.

Therefore:

- `live` semantics remains `PARTIALLY_VERIFIED / ARCHIVE_HOLD / INTENT_UNPROVED`;
- the `few weeks` versus early-October chronology discrepancy remains potentially stronger but still `ARCHIVE_HOLD`;
- systemic-deception conclusions remain blocked.

## 10. What “close everything” can and cannot mean at this evidence cutoff

The repository can close **research routes** without fabricating unavailable facts.

The following are now route-exhausted or access-controlled rather than merely neglected:

- crisis-day late-board continuity through the official `Who We Are` Wayback target;
- public unauthenticated Douglas/qPublic/GSCCCA property/deed search for the FY2022–FY2023 real-estate chain;
- currently known public searches for a named G3+ transferee;
- currently known public searches for PMBC primary resignation records;
- currently known independent archive routes for the MacArthur-2021 communication artifacts.

The remaining factual holds require **new primary evidence**, authenticated/public-record access, human listening, or later transaction/platform state. They must not be converted into invented closure merely because the open question is inconvenient.

## 11. Immediate repository gates after PASS23

Before PR #188 can be marked Ready or merged as a Research checkpoint:

1. the rerun of the sole red Wayback 2025-transition job must resolve terminally;
2. all current-head PR workflows must be terminal green, or an explicit policy-correct change must be reviewed and itself pass exact-head CI;
3. PR review threads/reviews/comments must be checked for unresolved debt;
4. compare against `main` must remain mergeable and without unexpected base drift;
5. PR body must be reconciled to the new immutable head and new Q006/PASS23 state;
6. `PUBLICATION_HOLD` remains true regardless of Research merge status.

This pass does not authorize publication or convert machine transcripts/recipient screenshots into conclusions beyond what their evidence class supports.