# Q004 — FY2025 IRS internal presidency-date conflict, 2026-09-09

**Status:** VERIFIED_PRIMARY INTERNAL FILING CONFLICT / EXACT MECHANICS HOLD / PUBLICATION_HOLD  
**Raw IRS object:** `202641339349303874_public.xml`  
**Raw XML SHA-256:** `48846b93808c2ffcacac6dc1995fb7890a630ccef9f711fa8a27cd4445541ac2`  
**Post-merge acquisition witness:** workflow run `34282122035`, FY2025 artifact `10078056865`, artifact digest `sha256:002b35b94360a14d48581e31125c555922bed5b47c23ed5463651cdca5358e7f`.

## 1. Why this file exists

A fresh ProPublica rendering exposed Scott Aniol as `President As Of 05/2025`. That wording was treated only as a discovery lead. The post-merge raw IRS acquisition artifact was then re-read directly.

The lead is real: the conflicting dates are present in the **same primary FY2025 filing**, not created by ProPublica.

## 2. Part VII title rows

The raw FY2025 Form 990 XML contains these exact officer-title fields:

- `SCOTT ANIOL` — `PRESIDENT AS OF 05/2025`;
- `JOSHUA BUICE` — `PRESIDENT THROUGH 05/2025`.

These rows are part of the filed Part VII officer/director reporting.

## 3. Same filing's program-history narrative

The same raw XML contains a program-history `Desc` stating, in substance and explicitly, that:

- founder and president Josh Buice resigned **in May 2025**;
- Dr. Scott Aniol **was appointed president in July 2025**.

Thus the raw primary object contains an internal chronology tension:

`PART_VII_TITLE_FIELD: ANIOL AS OF 05/2025`

versus

`PROGRAM_NARRATIVE: ANIOL APPOINTED IN JULY 2025`.

## 4. Evidentiary consequence

The correct conclusion is **not** to choose whichever date best fits an external chronology.

The filing itself proves:

1. Buice's presidency is represented as ending in May 2025;
2. Aniol is represented as succeeding him during 2025;
3. the exact month/effective mechanics are internally inconsistent within the filing (`05/2025` title row versus `July 2025` narrative).

Therefore a sentence such as `the FY2025 Form 990 proves Aniol became president in July 2025` is too strong unless it explicitly identifies the July date as the filing's narrative representation and discloses the conflicting Part VII field.

Likewise, `the Form 990 proves Aniol became president in May 2025` is too strong for the same reason.

## 5. Correct Q004 state

`SUCCESSION_ENDPOINT = VERIFIED_PRIMARY`.

`BUICE_PRESIDENCY_ENDED_IN_MAY_2025 = VERIFIED_PRIMARY_AS_FILED_REPRESENTATION`.

`ANIOL_PRESIDENCY_EFFECTIVE_MONTH = INTERNALLY_CONFLICTED_IN_PRIMARY_FILING`.

`EXACT_APPOINTMENT_DATE / BOARD_ACTION / EFFECTIVE_DATE = DOCUMENT_HOLD`.

This strengthens the reason Q004 cannot be closed from Part VII alone.

## 6. How to write it safely

Article-safe wording:

> G3's FY2025 Form 990 records the 2025 presidential transition but is internally inconsistent about its timing: Part VII labels Scott Aniol `President as of 05/2025` and Josh Buice `President through 05/2025`, while the same filing's program narrative says Buice resigned in May and Aniol was appointed president in July. The filing therefore establishes the succession but not a single unambiguous effective month; minutes, appointment instruments or another direct corporate record would be needed to resolve the mechanics.

## 7. Reopen/closure evidence

To resolve the conflict, seek a materially distinct primary object:

- board minutes/resolution;
- signed appointment/acceptance record;
- direct G3 announcement with effective date;
- corporate filing identifying effective officer change;
- first-person statement specifically distinguishing selection, appointment, start-of-service or public announcement dates.

Do not use a secondary renderer to break a conflict already present in the primary filing.

`PUBLICATION_HOLD = true`.