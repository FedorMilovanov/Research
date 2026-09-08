# G3 2027 National Conference — cancellation primary control, 2026-09-09

**Status:** VERIFIED_PRIMARY / OPERATIONAL_WINDDOWN CONTROL / PUBLICATION_HOLD  
**Question:** Was the previously advertised May 27–29, 2027 G3 National Conference actually canceled, or does the still-indexed promotional material indicate that the event remained active?

## 1. First-party transactional cancellation surface

G3's own event-registration route for the conference is:

`https://events.g3min.org/ordinaryfaithfulness`

The current first-party event object surfaced in web indexing with the title:

`Faithful in the Ordinary: Living All of Life for Christ`

and states explicitly:

- `Online Registration is Closed`;
- `This conference has been canceled`;
- registration is closed;
- registrations are being canceled and refunded in full.

This is the strongest current public event-state object because it is the G3-controlled registration/transaction surface for the event rather than a generic promotional shell.

**Claim state:**

`G3_2027_NATIONAL_CONFERENCE_CANCELED = VERIFIED_PRIMARY`.

`G3_2027_NATIONAL_CONFERENCE_REGISTRATIONS_REFUNDED_IN_FULL_AS_REPRESENTED = VERIFIED_PRIMARY_AS_FIRST_PARTY_REPRESENTATION`.

## 2. Stale/promotional surface conflict

At the same time, G3 search-indexed pages still expose the pre-cancellation promotion:

- `https://g3min.org/`
- `https://g3min.org/events/`
- `https://g3min.org/national-conference/`

Those indexed copies advertise:

`May 27–29, 2027 — Faithful in the Ordinary: Living All of Life for Christ`.

Controlled direct retrieval on Sep. 9 returned HTTP 503 for the root/events surface while a previously indexed copy of the national-conference page remained readable through search cache/indexing.

This creates a **surface-reconciliation problem**, not a substantive contradiction.

The correct precedence rule is:

`FIRST_PARTY_TRANSACTIONAL_CANCELLATION_STATE > STALE_OR_CACHED_PROMOTIONAL_SHELL`.

The indexed promotional shell must not be used to claim that G3 reversed the wind-down or restored the conference.

## 3. Historical context

On Aug. 26–27, contemporaneous secondary observers noted that the G3 website still advertised the May 2027 conference while G3 leadership and network operations were collapsing. That observation is consistent with the current finding: the public web shell lagged the operational decision.

Secondary observation is not required to establish cancellation because the G3-controlled registration object now does so directly.

## 4. What this closes

The following question is now closed at public-primary level:

> Was the May 27–29, 2027 G3 National Conference still an active future event after the operational wind-down?

**Answer:** No. The first-party registration surface states that it was canceled and registrations were being refunded.

## 5. What this does NOT close

This does not prove:

- the exact board vote or date on which the cancellation decision was made;
- which officer or employee executed the cancellation;
- the final amount of refunds paid;
- treatment of venue/vendor contracts;
- whether every other 2026/2027 G3-associated event was canceled;
- legal corporate dissolution;
- disposition of G3 Plus, G3 Press, intellectual property or subscriber assets.

## 6. Article-safe wording

> G3's public website continued to surface cached/promotional material for a May 2027 national conference after the ministry's collapse, but the ministry's own event-registration page now states that the conference was canceled, registration closed and registrations were being refunded in full. The stale promotional shell therefore should not be treated as evidence that G3 resumed normal conference operations.

`PUBLICATION_HOLD = true` remains independent of this closure.