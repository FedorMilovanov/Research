# Tom Buck dossier — item-level audit registry

**Status:** ACTIVE / PUBLICATION_HOLD  
**Parent:** [`../BUCK_DOSSIER_AUDIT.md`](../BUCK_DOSSIER_AUDIT.md)

This directory prevents a common forensic error: treating the existence of a 17-sermon accusation dossier as if all 17 sermons had already been independently adjudicated.

## Four independent closure gates per sermon

A sermon is not `ITEM_VERIFIED` until all applicable gates are closed:

1. **SERMON_IDENTITY** — official church/date/media identity.
2. **ORIGINAL_AUDIO** — human-checked original audio/video at each allegation timestamp; automated STT alone is insufficient.
3. **SOURCE_OBJECT** — exact identified edition/page or earlier source object; secondary quotation alone is insufficient for quote-safe closure.
4. **DEPENDENCE_ANALYSIS** — each alleged parallel classified independently as `A/B/C/S/U`, with source specificity and upstream-source checks.

Additional required field: **ATTRIBUTION_CONTEXT** — whether Buck names/cites the commentary or author in the immediate sermon context or elsewhere in the relevant section.

## Current registry

| # | Sermon | Date | Claimed comparator | Identity | Original audio | Source object | Dependence analysis | Current state |
|---:|---|---|---|---|---|---|---|---|
| 01 | Exodus 4:10–17 | 2017-03-05 | Philip Graham Ryken, *Exodus* | VERIFIED | HOLD | PARTIAL | ACTIVE | [`01_EXODUS_4_10_17_SOURCE_SPECIFICITY.md`](01_EXODUS_4_10_17_SOURCE_SPECIFICITY.md) |
| 02 | Exodus 5:1–9 | 2017-03-26 | Ryken, *Exodus* | VERIFIED from FBC archive | HOLD | HOLD | NOT_STARTED | — |
| 03 | Exodus 5:10–21 | 2017-04-02 | Ryken, *Exodus* | VERIFIED from FBC archive | HOLD | HOLD | NOT_STARTED | — |
| 04 | Ephesians 4:1–6 | 2022-09-18 | R. Kent Hughes, *Ephesians* | dossier + archive lead | HOLD | HOLD | NOT_STARTED | — |
| 05 | Ephesians 5:25–33 | 2022-11-20 | Hughes, *Ephesians* | dossier + archive lead | HOLD | HOLD | NOT_STARTED | — |
| 06 | Ephesians 6:5–9 | 2022-12-04 | Hughes, *Ephesians* | dossier + archive lead | HOLD | HOLD | NOT_STARTED | — |
| 07 | Romans 4:1–12 | 2023-04-30 | Hughes, *Romans* | VERIFIED from FBC archive | HOLD | HOLD | NOT_STARTED | — |
| 08 | Romans 5:6–11 | 2023-06-04 | Hughes, *Romans* | VERIFIED | HOLD | PARTIAL | ACTIVE | [`08_ROMANS_5_6_11_PETER_MILLER.md`](08_ROMANS_5_6_11_PETER_MILLER.md) |
| 09 | Titus 1:1–4 | 2023-06-18 | Hughes & Chapell, *1 & 2 Timothy and Titus* | VERIFIED from FBC archive | HOLD | HOLD | NOT_STARTED | — |
| 10 | Titus 2:11–15 | 2023-08-06 | Hughes & Chapell | VERIFIED | HOLD | PARTIAL / Chapell 1998 lineage corroborated | ACTIVE_PARENT_DOSSIER | source-lineage strong; exact Buck audio still HOLD |
| 11 | Romans 7:1–6 | 2024-01-07 | Hughes, *Romans* | dossier + archive lead | HOLD | HOLD | NOT_STARTED | — |
| 12 | Romans 15:1–6 | 2025-10-19 | Hughes, *Romans* | dossier + archive lead | HOLD | HOLD | NOT_STARTED | — |
| 13 | Romans 16:25–27 | 2025-12-21 | Hughes, *Romans* | dossier + archive lead | HOLD | HOLD | NOT_STARTED | — |
| 14 | Joshua 1:1–9 | 2026-01-18 | David Jackman, *Joshua* | dossier + archive lead | HOLD | HOLD | QUEUED | KNOW/OBEY/MEDITATE structural claim requires source-specificity control |
| 15 | Joshua 2:1–24 | 2026-02-08 | Jackman, *Joshua* | dossier + archive lead | HOLD | HOLD | NOT_STARTED | — |
| 16 | Joshua 3:1–17 | 2026-02-15 | Jackman, *Joshua* | dossier + archive lead | HOLD | HOLD | NOT_STARTED | — |
| 17 | Joshua 4:1–24 | 2026-03-01 | Jackman, *Joshua* | dossier + archive lead | HOLD | HOLD | QUEUED | distinctive-phrase claim requires original audio/source page |

## Progress interpretation

`2 item files exist` does **not** mean `2 sermons proven plagiarized`.

At present:

- **17/17** are identified by the accusation dossier;
- official FBC archive identities are independently visible for multiple sermons and will be normalized across all 17;
- **0/17** have all four closure gates independently completed in this research environment;
- item 01 and item 08 have already produced important **source-specificity corrections** to the dossier's binary framing;
- item 10 has strong pre-Buck source-lineage evidence but original Buck audio remains unverified.

No global numerical verdict (`45 proven instances`, `% plagiarized`, etc.) is permitted until the item matrix is complete.