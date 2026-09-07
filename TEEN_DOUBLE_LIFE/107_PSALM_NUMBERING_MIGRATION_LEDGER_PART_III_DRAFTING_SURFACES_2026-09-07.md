# Psalm Numbering Migration Ledger — Part III Drafting Surfaces

**Status:** PRE-DRAFT CORRECTION LEDGER / RESEARCH ONLY  
**Date:** 2026-09-07  
**Authority:** `105_BIBLE_QUOTATION_NUMBERING_TRANSLATION_AND_ORIGINAL_LANGUAGE_POLICY...` + `106_FINAL_EXEGESIS_CROSSCHECK...`  
**Purpose:** ensure the English/MT label `Psalm 50` for the hypocrisy passage cannot leak into the Russian product draft as `Пс. 50`.

---

# 0. Locked correction

Hypocrisy / “what right have you to declare my statutes?” passage:

- English/MT/commentary numbering: `Psalm 50:16–21` (often source packet extends to v.23);
- Russian Synodal publication numbering: **`Пс. 49:16–21`** (or `Пс. 49:16–23` if the selected passage includes the ending).

Russian `Пс. 50` is the penitential Psalm beginning «Помилуй меня, Боже...» (= MT/English Psalm 51).

---

# 1. Why old Research files are not being destructively rewritten

This PR is shared with a concurrent compression/architecture agent.

Older files preserve useful provenance:

- they often cite Calvin/CCEL pages titled `Psalm 50`;
- the English source itself genuinely uses MT/English numbering;
- rewriting every historical research mention now would create unnecessary shared-file collision risk and obscure why the mismatch occurred.

Therefore:

> **Research-source numbering may remain where it accurately names an English source; publication numbering must be normalized downstream.**

`105` and this ledger are downstream authority for the Russian draft.

---

# 2. Confirmed affected high-priority drafting surfaces

## A. `49_EXEGESIS_PASS_CHILDREN_WORSHIP_HYPOCRISY_AND_CHURCH_ACCESS_2026-09-07.md`

Contains section:

> `Psalm 50:16–21 — religious lips plus hated correction`

### Disposition

- Exegesis/content: **KEEP**.
- Calvin URL/title: **KEEP** as English-source identifier.
- Russian publication reference: **NORMALIZE TO Пс. 49:16–21**.

This file is exegesis provenance, not final Russian citation authority.

---

## B. `91_PART_III_SELECTED_SOURCE_PACKET_CHURCH_CHILDREN_WORSHIP_CHOIR_YOUTH_ACCESS_DISCIPLINE_2026-09-07.md`

This is the most important affected surface because it is the compact Part III drafting packet.

Contains:

> `Psalm 50:16–21 — religious lips + hatred of correction`

and repeatedly calls Calvin’s source `Psalm 50`.

### Disposition

- Biblical thesis: **GREEN**.
- Calvin source title/link: **GREEN as source metadata**.
- Body/drafting reference inherited from this packet: **MUST PASS THROUGH 105**.
- Russian body citation: **Пс. 49:16–21**.

### P0 rule

Future author must not copy the packet heading verbatim into Russian MDX.

---

## C. `100_PART_III_CHURCH_CHILDREN_CHOIR_YOUTH_HOLINESS_SELECTED_SOURCE_PACKET_2026-09-07.md`

Contains section:

> `Psalm 50 — the central “religious lips + rebellious life” text`

and `Ps. 50:16–23`.

### Disposition

- Argument: **KEEP**.
- Russian publication numbering: **Пс. 49:16–23** if using the full listed range.
- If only vv.16–21 are quoted/analyzed: **Пс. 49:16–21**.

---

# 3. Other Research/compression references found by PR-wide text scan

A PR-wide patch scan found multiple additional `Psalm 50` mentions outside the three files above, including:

- architecture/source-distribution summaries that list `Psalm 50` as the Church Companion/Part III source;
- reconciliation prose that describes `91_PART_III...` as strong on “Psalm 50 + Calvin”;
- audit material discussing the “unrepentant person singing/praying” issue;
- pre-draft gate lists saying the exact “Psalm 50” quotation still needs verification.

### Disposition

These are not independent errors in theology. They are **source-numbering inheritance**.

All such references are classified:

- `SOURCE LABEL` if naming Calvin/English commentary → may remain `Psalm 50`;
- `RUSSIAN SCRIPTURE REFERENCE` → must become `Пс. 49`;
- `AMBIGUOUS COMPRESSION SHORTHAND` → treat as unsafe until normalized through `105`.

---

# 4. Publication-source rule

When a drafter sees any of the following in Research:

- `Psalm 50`;
- `Ps. 50:16–21`;
- `Ps. 50:16–23`;
- “Calvin on Psalm 50”;

he must ask:

> Is this naming the English source edition, or is this supposed to be the Russian Bible reference shown to the reader?

Then:

## If English source title

Keep, e.g.:

> Calvin, commentary on Psalm 50 (MT/English numbering).

## If Russian reader-facing Bible reference

Use:

> **Пс. 49:16–21**

or the exact corresponding Russian range.

---

# 5. Recommended first-use scholarly form in Part III

At the first substantial use of the passage, an unobtrusive source note may say:

> **Пс. 49:16–21** (в англоязычных комментариях по масоретской нумерации — Ps 50:16–21).

After that use only:

> **Пс. 49**

No need to repeat double numbering throughout the article.

---

# 6. Calvin citation rule

Calvin/CCEL page is legitimately titled `Psalm 50:16–20` in its English numbering system.

Do not “correct” the URL/title into a nonexistent Calvin `Psalm 49` page.

Correct Russian presentation can therefore look conceptually like:

> Кальвин, комментируя **Пс. 49:16–21** (Ps 50 в используемом английском издании), обращает внимание на противоречие между исповеданием уст и ненавистью к исправлению.

This preserves both Russian reader accuracy and source discoverability.

---

# 7. Automation/QA idea for future product lane

Do **not** implement in Research.

But before publication, a targeted content check should search new Part III MDX for:

- `Пс. 50:16`;
- `Пс 50:16`;
- `Псалом 50:16`;

when the surrounding text contains:

- `уставы`;
- `завет`;
- `ненавидишь наставление`;
- `бросаешь за себя`.

If found, treat as likely numbering regression.

This can be a one-off drafting check; no new global validator is required unless repeated cross-language Psalm work demonstrates a systemic need.

---

# 8. Final drafting authority

For this passage, authority order is now:

1. Russian Synodal text/reference verified independently;
2. `105` Bible quotation/numbering policy;
3. `106` exegesis/application cross-check;
4. this `107` migration ledger;
5. older `49 / 91_PART_III / 100` source packets for argument/source provenance.

### Locked final line

> **Part III must cite the hypocrisy/worship passage as Пс. 49:16–21 (or through v.23 if used), never as Russian Пс. 50:16–21.**
