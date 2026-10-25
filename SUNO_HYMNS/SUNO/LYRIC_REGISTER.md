# Lyric and text-version register

This register is an acquisition and provenance checklist; it does not store copyrighted modern critical-edition texts or reconstruct missing lyrics.

## Required text layers

For each work/version, maintain separate records for:

1. **Historical source witness** — original spelling and edition, with source ID, exact locator and edition date.
2. **Normalized transcription** — editorial normalization explained and, when feasible, checked against a page image.
3. **Literal translation / gloss** — for analysis, with uncertainty and textual issues visible.
4. **Russian literary adaptation** — exact user-approved wording and version ID.
5. **SUNO-ready lyric** — the exact submitted lyric, with section labels and pronunciation/stress marks.
6. **Recorded take** — version ID pointing to the exact SUNO generation output and mix/export.

Never merge these into a single file or present the adaptation as a verbatim historical translation.

For DUTCH-004 all six layers are deliberately kept apart in one package: the 1676 Dutch text (§4 of the research dossier), a literal gloss, a Russian adaptation draft, a declared deviation table, a musical brief and a prospective prompt. The draft is an **adaptation**, and the gloss is the layer against which fidelity must be judged.

## Known capture state

| Work | Historical source | Russian lyric file | SUNO-ready lyric | Exact submitted prompt |
|---|---|---|---|---|
| DUTCH-001 | URL and title recorded; exact first-edition item locator still to improve | NOT IN REPOSITORY | NOT IN REPOSITORY | NOT CAPTURED |
| DUTCH-002 V1 | Source chain recorded; date of source II has EVIDENCE_HOLD | NOT IN REPOSITORY | NOT IN REPOSITORY | NOT CAPTURED |
| DUTCH-002 V2 | Same source text chain; separate recording version | NOT IN REPOSITORY | NOT IN REPOSITORY | NOT CAPTURED |
| DUTCH-003 V1 | Modern scholarly edition locator; original 1630 leaf not acquired | NOT IN REPOSITORY | NOT IN REPOSITORY | NOT CAPTURED |
| DUTCH-004 (draft) | 1676 print pp. 74–75, read in full; 1727 collation recorded | DUTCH-004-RU-DRAFT v0.1 in `DUTCH-004_PRODUCTION_PACKAGE.md` §3 | Not yet frozen; gloss in §2 | PROMPT-DUTCH-004-V1 authored, never submitted |

## Intake checklist

- Keep clean public lyric and pronunciation-marked SUNO lyric separate.
- Save the exact wording as actually submitted, not a reconstructed “equivalent”.
- Assign a lyric revision ID and record a short changelog for every correction.
- Record the source-text line/stanza used for each adapted section where feasible.
- Preserve editorial uncertainties, biblical references and source variants.
- Check rights for modern translations, critical editions and arrangements independently.
