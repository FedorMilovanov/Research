# Tom Buck dossier — item-level audit registry

**Status:** ACTIVE / PUBLICATION_HOLD  
**Parent:** [`../BUCK_DOSSIER_AUDIT.md`](../BUCK_DOSSIER_AUDIT.md)

This directory prevents a core forensic error: the existence of a 17-sermon accusation dossier, or even the existence of 17 item-audit files, does **not** mean that 17 sermons have been independently adjudicated as plagiarism.

## Closure gates per sermon

A sermon is not `ITEM_VERIFIED` until all applicable gates are closed:

1. **SERMON_IDENTITY** — official church/date/media identity.
2. **ORIGINAL_AUDIO** — human-checked original audio/video at each allegation timestamp; automated STT alone is insufficient.
3. **SOURCE_OBJECT** — exact identified edition/page or earlier source object; secondary quotation alone is insufficient for quote-safe closure.
4. **DEPENDENCE_ANALYSIS** — each alleged parallel classified independently by specificity, source lineage and upstream-source controls.
5. **ATTRIBUTION_CONTEXT** — whether Buck names/cites the commentary or author in the immediate sermon context or elsewhere in the relevant section.

A source-lineage or specificity finding can strengthen or weaken an allegation without closing the original-audio/attribution gates.

## Reconciled registry — 2026-09-08 / PASS22

| # | Sermon | Date | Claimed comparator | Current forensic state | Remaining principal gate(s) | Item file |
|---:|---|---|---|---|---|---|
| 01 | Exodus 4:10–17 | 2017-03-05 | Philip Graham Ryken, *Exodus* | `SERMON_IDENTITY_VERIFIED / MIXED_SPECIFICITY` | exact Buck audio + attribution; exact source-side wording where needed | [`01_EXODUS_4_10_17_SOURCE_SPECIFICITY.md`](01_EXODUS_4_10_17_SOURCE_SPECIFICITY.md) |
| 02 | Exodus 5:1–9 | 2017-03-26 | Ryken, *Exodus* | `SERMON_IDENTITY_VERIFIED / MULTIPLE_DEPENDENCE_CANDIDATES` | original audio + exact book object + attribution | [`02_EXODUS_5_1_9_SOURCE_SPECIFICITY.md`](02_EXODUS_5_1_9_SOURCE_SPECIFICITY.md) |
| 03 | Exodus 5:10–21 | 2017-04-02 | Ryken, *Exodus* | `SERMON_IDENTITY_VERIFIED / STRONG_CUMULATIVE_DEPENDENCE_CANDIDATE / UPSTREAM_SOURCE_CORRECTION` | audio + exact book/source objects + attribution | [`03_EXODUS_5_10_21_SOURCE_LINEAGE.md`](03_EXODUS_5_10_21_SOURCE_LINEAGE.md) |
| 04 | Ephesians 4:1–6 | 2022-09-18 | R. Kent Hughes, *Ephesians* | `SERMON_IDENTITY_VERIFIED / MIXED_SPECIFICITY_PARALLELS` | audio + exact book object + attribution | [`04_EPHESIANS_4_1_6_SOURCE_SPECIFICITY.md`](04_EPHESIANS_4_1_6_SOURCE_SPECIFICITY.md) |
| 05 | Ephesians 5:25–33 | 2022-11-20 | Hughes, *Ephesians* | `SERMON_IDENTITY_VERIFIED / HUGHES_SPECIFIC_WORDING_CANDIDATES / TORNADO_ANECDOTE_ORIGIN_OVERSTATED` | audio + exact book object + attribution | [`05_EPHESIANS_5_25_33_SOURCE_LINEAGE.md`](05_EPHESIANS_5_25_33_SOURCE_LINEAGE.md) |
| 06 | Ephesians 6:5–9 | 2022-12-04 | Hughes, *Ephesians* | `SERMON_IDENTITY_AND_MEDIA_ID_VERIFIED / HISTORICAL_BLOCK_LIKELY_PROXIMATE_DEPENDENCE_BUT_NOT_HUGHES_ORIGINAL` | human audio + source/attribution closure | [`06_EPHESIANS_6_5_9_HISTORICAL_SOURCE_LINEAGE.md`](06_EPHESIANS_6_5_9_HISTORICAL_SOURCE_LINEAGE.md) |
| 07 | Romans 4:1–12 | 2023-04-30 | Hughes, *Romans* | `SERMON_IDENTITY_VERIFIED / HUGHES_SPECIFIC_SEQUENCE_CANDIDATE / MULTIPLE_DISTINCTIVENESS_CLAIMS_DOWNGRADED` | audio + exact book object + attribution | [`07_ROMANS_4_1_12_SOURCE_SPECIFICITY.md`](07_ROMANS_4_1_12_SOURCE_SPECIFICITY.md) |
| 08 | Romans 5:6–11 | 2023-06-04 | Hughes, *Romans* | `SERMON_IDENTITY_VERIFIED / STORY_SOURCE_NONUNIQUE` | exact verbal audio/source comparison + attribution | [`08_ROMANS_5_6_11_PETER_MILLER.md`](08_ROMANS_5_6_11_PETER_MILLER.md) |
| 09 | Titus 1:1–4 | 2023-06-18 | Hughes & Bryan Chapell | `SERMON_IDENTITY_VERIFIED / ONE_STRONGLY_HUGHES_CHAPELL_LINKED_FORMULATION / OTHER_ROWS_LOWER_SPECIFICITY` | audio + exact book object + attribution | [`09_TITUS_1_1_4_SOURCE_SPECIFICITY.md`](09_TITUS_1_1_4_SOURCE_SPECIFICITY.md) |
| 10 | Titus 2:11–15 | 2023-08-06 | Hughes & Chapell | `ORIGINAL_MEDIA_SEGMENT_ACQUIRED / MACHINE_TRANSCRIPT_CONFIRMS_MARRIAGE_BLOCK / SOURCE_LINEAGE_STRONG / BIOGRAPHICAL_FABRICATION_CLAIM_BLOCKED` | human audio + wider attribution; exact immediate source where needed | [`10_TITUS_2_11_15_AUTOBIOGRAPHY_AND_ATTRIBUTION.md`](10_TITUS_2_11_15_AUTOBIOGRAPHY_AND_ATTRIBUTION.md) |
| 11 | Romans 7:1–6 | 2024-01-07 | Hughes, *Romans* | `ORIGINAL_MEDIA_MACHINE_CONFIRMS_DISSOLVED-RELATIONSHIP_AND_ANTITHESIS_BLOCKS / TEXT-DRIVEN_ANALOGY_SEPARATED` | human audio + exact Hughes object + wider attribution | [`11_ROMANS_7_1_6_SOURCE_SPECIFICITY.md`](11_ROMANS_7_1_6_SOURCE_SPECIFICITY.md) |
| 12 | Romans 15:1–6 | 2025-10-19 | Hughes, *Romans* | `ORIGINAL_MEDIA_MACHINE_CONFIRMS_STRONG_CHRIST-EXAMPLE_GLORY_BLOCK / CIRCULATING-ILLUSTRATION_CORRECTION` | human audio + exact Hughes object + wider attribution; remaining rows separately | [`12_ROMANS_15_1_6_SOURCE_LINEAGE.md`](12_ROMANS_15_1_6_SOURCE_LINEAGE.md) |
| 13 | Romans 16:25–27 | 2025-12-21 | Hughes, *Romans* | `ORIGINAL_MEDIA_MACHINE_CONFIRMS_FIVE-ELEMENT_SEQUENCE / ONE_LOW-SPECIFICITY_ROW` | human audio + exact Hughes object + wider attribution | [`13_ROMANS_16_25_27_SOURCE_SPECIFICITY.md`](13_ROMANS_16_25_27_SOURCE_SPECIFICITY.md) |
| 14 | Joshua 1:1–9 | 2026-01-18 | David Jackman, *Joshua* | `ORIGINAL_MEDIA_CONFIRMS_TEXT-DRIVEN_KNOW_OBEY_MEDITATE_MATERIAL / NEGATIVE_CONTROL_LOW_SPECIFICITY` | exact Jackman wording + human audio/attribution if stronger verbal claim pursued | [`14_JOSHUA_1_1_9_STRUCTURE_SPECIFICITY.md`](14_JOSHUA_1_1_9_STRUCTURE_SPECIFICITY.md) |
| 15 | Joshua 2:1–24 | 2026-02-08 | Jackman, *Joshua* | `EXACT_JACKMAN_JOSHUA2_SAMPLE_PRIMARY-ANCHORED / ORIGINAL_MEDIA_MACHINE_CONFIRMS_MULTIPLE_STRONG_AND_WEAK_ROWS / MIXED_SPECIFICITY` | human audio + wider attribution; upstream controls where needed | [`15_JOSHUA_2_1_24_SOURCE_OBJECT_AND_SPECIFICITY.md`](15_JOSHUA_2_1_24_SOURCE_OBJECT_AND_SPECIFICITY.md) |
| 16 | Joshua 3:1–17 | 2026-02-15 | Jackman, *Joshua* | `ORIGINAL_MEDIA_MACHINE_CONFIRMS_DENSE_CLUSTER / STRONG_CAUSAL_AND_HERMENEUTICAL_SOURCE-FAMILY_ROWS / COMMON_ROWS_DOWNGRADED` | exact Jackman pp. 41–49 + human audio + wider attribution | [`16_JOSHUA_3_1_17_SOURCE_LINEAGE.md`](16_JOSHUA_3_1_17_SOURCE_LINEAGE.md) |
| 17 | Joshua 4:1–24 | 2026-03-01 | Jackman, *Joshua* | `ORIGINAL_MEDIA_MACHINE_CONFIRMS_DISTINCTIVE_MEMORY_PHRASE / JACKMAN-PHRASE_SOURCE-SPECIFIC` | human audio + exact Jackman pp. 51–57 + wider attribution | [`17_JOSHUA_4_1_24_MEMORY_PHRASE.md`](17_JOSHUA_4_1_24_MEMORY_PHRASE.md) |

## Progress interpretation after PASS22

- **17/17** accusation-sermon items have dedicated forensic files.
- PASS22 original-media matrix for Items **11–17 completed 7/7 success** on exact head `82a0d599…`.
- Items **10–17** now have an official original-media acquisition result or acquired bounded segment in the evidence chain.
- All acquired audio was used ephemerally and removed before artifact upload; retained artifacts contain receipts, hashes and machine transcripts only.
- The late original-media pass produced **strong upgrades, mixed results and a negative control**, not a one-way accusation confirmation.
- **0/17** are declared `ITEM_VERIFIED`: human listening, exact source objects and wider attribution remain open where applicable.
- Item 10 continues to block the leap from a textual-attribution question to the factual claim that Buck fabricated an analogous marriage history.
- Item 14 is a key anti-bias control: original audio confirms the conceptual content but does not make text-driven Joshua 1 structure a strong literary fingerprint.

## Numerical-verdict firewall

No global numerical verdict such as `45 proven instances`, `X% plagiarized`, or `17 sermons plagiarized` is permitted until the row-level matrix has human-checked audio, exact source objects, attribution context and dependence classification. Item-file coverage and media acquisition are **research coverage metrics**, not misconduct counts.
