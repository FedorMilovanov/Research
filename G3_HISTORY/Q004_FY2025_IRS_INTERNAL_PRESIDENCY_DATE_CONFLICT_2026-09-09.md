# Q004 — 2025 presidential transition primary closure and FY2025 IRS internal date conflict

**Status:** PRESIDENTIAL TRANSITION DATES VERIFIED_PRIMARY / IRS INTERNAL FIELD CONFLICT PRESERVED / BROADER DIRECTOR MECHANICS HOLD / PUBLICATION_HOLD  
**Raw IRS object:** `202641339349303874_public.xml`  
**Raw XML SHA-256:** `48846b93808c2ffcacac6dc1995fb7890a630ccef9f711fa8a27cd4445541ac2`  
**Post-merge acquisition witness:** workflow run `34282122035`, FY2025 artifact `10078056865`, artifact digest `sha256:002b35b94360a14d48581e31125c555922bed5b47c23ed5463651cdca5358e7f`.

## 1. Discovery and raw-filing verification

A fresh ProPublica rendering exposed Scott Aniol as `President As Of 05/2025`. That wording was treated only as a discovery lead and checked against the post-merge FY2025 raw IRS artifact.

The lead is real: the conflicting month field is present in the **primary FY2025 filing**, not created by ProPublica.

## 2. Part VII title rows

The raw FY2025 Form 990 XML contains these exact officer-title fields:

- `SCOTT ANIOL` — `PRESIDENT AS OF 05/2025`;
- `JOSHUA BUICE` — `PRESIDENT THROUGH 05/2025`.

These rows are part of the filed Part VII officer/director reporting.

## 3. Same filing's narrative says July

The same raw XML contains a program-history `Desc` stating that:

- founder and president Josh Buice resigned in May 2025;
- Dr. Scott Aniol was appointed president in **July 2025**.

Thus the raw filing itself contains a chronology tension:

`PART_VII_TITLE_FIELD: ANIOL AS OF 05/2025`

versus

`PROGRAM_NARRATIVE: ANIOL APPOINTED IN JULY 2025`.

## 4. Independent first-party board records resolve the presidential transition dates

### Buice resignation

Official G3 Board statement:

`https://g3min.org/statement-regarding-josh-buice/`

Dated May 12, 2025, it states that on **May 8**, after some board members privately encouraged Josh Buice to resign, the board received and **unanimously accepted his resignation as President of G3**.

This is a direct institutional/board statement about the action and date.

### Aniol appointment

Official G3 Board announcement:

`https://g3min.org/scott-aniol-named-president-of-g3-ministries/`

Dated July 14, 2025, it states:

- the Board of Directors appointed Dr. Scott Aniol President of G3 Ministries;
- the appointment was **effective Wednesday, July 9**.

This is a direct institutional/board statement with an explicit effective date.

## 5. Evidentiary consequence

The presidential succession no longer needs to remain date-open merely because Part VII contains `AS OF 05/2025`.

The better evidence hierarchy is:

1. direct board statement on resignation acceptance — May 8;
2. direct board announcement on appointment/effective date — July 9;
3. FY2025 narrative — consistent with a July appointment;
4. FY2025 Part VII title field — inconsistent `AS OF 05/2025`, preserved as an internal filing defect/tension rather than used to overwrite the direct board record.

Therefore:

`BUICE_RESIGNATION_ACCEPTED = 2025-05-08 / VERIFIED_PRIMARY`.

`ANIOL_PRESIDENCY_EFFECTIVE = 2025-07-09 / VERIFIED_PRIMARY`.

`FY2025_PART_VII_ANIOL_AS_OF_05_2025 = VERIFIED_PRIMARY_AS_FILED_FIELD / INTERNALLY_INCONSISTENT_WITH_NARRATIVE_AND_BOARD_ANNOUNCEMENT`.

## 6. What Q004 is now closed for — and what remains open

### Closed

The **presidential transition endpoints/dates** are primary-closed at the institutional-record level:

- Buice resignation accepted May 8, 2025;
- Aniol appointment effective July 9, 2025.

### Still open

Q004 is broader than the presidency. The following remain document-held unless separately primary-closed:

- exact Tom Buck resignation/removal/effective date;
- exact dates/mechanics for other director departures/additions;
- board vote/minutes beyond what the public statements disclose;
- any interim presidential/acting authority between May 8 and July 9;
- whether selection, internal approval and public announcement occurred on different dates before the effective date.

## 7. Article-safe wording

> G3's Board said it unanimously accepted Josh Buice's resignation as president on May 8, 2025, and later announced Scott Aniol's appointment as president effective July 9. The organization's FY2025 Form 990 broadly corroborates that transition but contains an internal timing defect: Part VII labels Aniol `President as of 05/2025`, while the same filing's narrative says he was appointed in July. The direct board records therefore control the presidential effective dates; broader director-transition mechanics still require separate records.

## 8. Research control

Do not silently normalize the Part VII field. Preserve the contradiction because it is part of the filed primary object and matters when auditing derivative renderers.

Do not extend the presidential-date closure to every 2025 board transition.

`PUBLICATION_HOLD = true`.