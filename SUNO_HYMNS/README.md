# SUNO Hymns & Dutch Reformed Hymn Research

**Project ID:** SUNO-HYMNS-NL  
**Snapshot date:** 2026-10-25  
**State:** third pass (2026-10-25). Existing-work inventory recorded; two historical questions advanced with primary witnesses; one new candidate researched to a lyric draft. Asset verification and prompt recovery remain open.

## Purpose

This scoped project records hymn and Scripture-song work prepared for **«Господь Бог — Сила Моя»**, initially focusing on Dutch Reformed devotional poetry and hymnody. It separates two related but non-interchangeable workstreams:

1. **SUNO / production:** lyric preparation, pronunciation and stress marks, style experiments, version management, audio/video export and metadata.
2. **Historical RESEARCH:** authors, original texts, editions, biblical references, melody directions, songbooks, Dutch Reformed church-song history, adaptation chains, source locators and rights boundaries.

A completed audio export is not evidence that a video or MP3 has been uploaded. A historical attribution in a product description is not verified merely because it appeared in an earlier draft.

## Read first

Before making changes, follow the Research repository instructions in this order:

1. Root AGENT_RULES.md.
2. Root CURRENT_AUTHORITY.md.
3. data/research-authority-registry-v1.json.
4. data/repository-evidence-policy-v2.json.
5. 00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md.
6. This project README, then the SUNO or RESEARCH lane README relevant to the task.

The root Research authority and evidence policy remain controlling. Nothing in this directory can redefine global source classes, HOLD semantics, rights rules, or publication approval. This is a scoped project index, not a replacement authority.

## Directory map

- **SUNO/README.md** — production workflow and state model.
- **SUNO/STATUS_LEDGER.md** — known prepared works, incomplete checks and publication boundaries.
- **SUNO/STYLE_AND_PRODUCTION_RULES.md** — accumulated user preferences and reproducibility rules.
- **SUNO/ASSET_MANIFEST.md** — reported local filenames, exports, metadata and unresolved verification.
- **SUNO/DUTCH-004_PRODUCTION_PACKAGE.md** — the next work: form decision, gloss, Russian draft, deviations, musical brief, authored prompt and a per-element status table.
- **SUNO/DUTCH-005_PRODUCTION_PACKAGE.md** — *Heerlijckheyds Loff* (1676, pp. 155–158): ten-stanza gloss, Russian adaptation v0.1, eight declared deviations, and two style directions for SUNO (one primary, one option).
- **SUNO/DUTCH-005_LYRIC_AND_STYLE_SHEET.md** — the copy sheet: the full Dutch text of all ten stanzas, the Russian lyric, the SUNO-tagged lyric and both style prompts in copy-ready blocks.
- **RESEARCH/README.md** — source-evidence method for historical hymn research.
- **RESEARCH/DUTCH_REFORMED_HYMNODY.md** — initial historical map of Dutch Reformed church singing.
- **RESEARCH/DUTCH_HYMN_CATALOG.md** — records for the three Dutch works developed in the conversation.
- **RESEARCH/DUTCH_HYMN_BACKLOG.md** — candidates not recorded as produced in the current project context.
- **RESEARCH/AUTHOR_*.md** — focused author dossiers.
- **RESEARCH/SOURCE_REGISTER.md** — human-readable view of the source registry.
- **RESEARCH/CLAIM_LEDGER.md** — claim-by-claim support, caveats and typed HOLDs.
- **RESEARCH/SONGBOOK_REGISTER.md** — publication editions and the actual access layer.
- **RESEARCH/GENRE_AND_CLASSIFICATION.md** — controlled distinctions between psalms, devotional songs, sonnets, later adaptations and modern settings.
- **RESEARCH/REVIEW_LOG_2026-10-25.md** — corrections made by the second audit and by the third and fourth passes.
- **RESEARCH/DOSSIER_HERT_STERCKTE_I_II.md** — the two poems of that title, their relation, and the 1664/1674 date question.
- **RESEARCH/CANDIDATE_DUTCH-004_DEN_NEDRIGEN_CHRISTEN.md** — researched candidate for the next production.
- **RESEARCH/DOSSIER_DUTCH-001_TRANSLATION_DECISIONS.md** — the eight translation decisions for *Schepselen niet en Jesus al*, with a confidence level per item.
- **RESEARCH/DOSSIER_DUTCH-002_TEXT_HISTORY.md** — the 14 → 7 → 5 stanza history across 1676, 1806 and 1938, with the exact collation.
- **RESEARCH/DOSSIER_DUTCH-003_REVIUS_SONNET.md** — the sonnet's dramaturgy, its turn at line 9, and the status of the discussed Russian rendering.
- **RESEARCH/CANDIDATE_DUTCH-CAND-021_HEERLIJCKHEYDS_LOFF.md** — identification of *Heerlijckheyds Loff* (1676, pp. 155–158) and the evidence gaps around it.
- **RESEARCH/COLLATION_GEZANG205_THREE_WAY.md** — 1676 → 1806 → 1938 stanza by stanza, with the 1938 text read from the printed bundel and the two corrections that followed.
- **RESEARCH/AUDIT_2026-10-25_PASS4.md** — the fourth-pass audit: what exists, what to add, what to correct, what is verified, what stays open.
- **HANDOFF_FOR_NEXT_AGENT.md** — continuation instructions for a new Arena/chat agent.
- **data/track-catalog-v1.json** — project-local machine-readable track catalog.
- **data/source-registry-v1.json** — project-local source registry.
- **data/author-registry-v1.json**, **data/claim-ledger-v1.json**, **data/songbook-registry-v1.json** — machine-readable authors, reviewed claims and edition histories.
- **scripts/validate_project_registry.py** — read-only state/cross-reference validation.

## Status language

The project production state and Research evidence state are separate dimensions.

Production uses project-local terms defined in SUNO/README.md. These labels do not replace the global Research fields evidenceClass, accessState, locatorState, rightsState, publicationState or typed HOLDs.

- **Prepared / exported:** an audio, cover or video file was reported as created.
- **Local asset:** a filename/path was reported in the user's Windows Downloads folder; the file has not therefore been committed to this repository.
- **Metadata verified:** embedded tags were read back from the actual output. A suggested or run command is not enough.
- **Published verified:** a concrete YouTube/Telegram URL or direct publication receipt has been checked.
- **Unknown / not verified:** do not guess. This is not the same as “not published”.

## Initial inventory

The retained working context records three Dutch historical works:

1. **«Всё сотворённое — ничто, Иисус — всё»** — Jodocus van Lodenstein; source title *Schepselen niet en Jesus al* / *Schepselen Niet en Iesus Al*. One WAV, one YouTube MP4 and one Telegram MP3 were reported prepared.
2. **«Блаженно, блаженно — быть ничем»** — Jodocus van Lodenstein, through the later seven-stanza *Zelfverloochening* reworking by Abraham Rutgers (1806). Two audio versions, two YouTube MP4s and two Telegram MP3s were reported prepared.
3. **«Он понёс наши скорби»** — Jacobus Revius; source sonnet *Hy droech onse smerten* (first published in 1630). An MP3 filename is known; embedded-tag readback and final artwork selection are not confirmed.

4. **«Смиренный христианин» (Psalm 131)** — Jodocus van Lodenstein, *Den nedrigen christen, Op Psalm 131* (1676, pp. 74–75). **Nothing produced.** A lyric draft and a production package exist; there is no SUNO output, no audio, no cover and no publication. Do not describe this work as recorded.

No public release status is promoted to verified in this repository snapshot. See the per-track ledger before making public claims.

## Non-negotiable research boundaries

- Do not collapse Lodenstein's dated 1674 poem, Rutgers's 1806 reworking, later Afrikaans hymn versions and the Russian lyric adaptation into one identical text.
- Do not describe Revius's original 14-line sonnet as a hymn with a documented original melody unless a primary source establishes that.
- Do not infer a melody, musical genre, lyric wording, Suno prompt or publication date from memory when the exact artifact is unavailable.
- A catalog page or reachable URL is not the same as full-object access; an exact title is not an exact locator; a historical public-domain text does not automatically clear rights in a modern critical edition, scan, translation or visual asset.
- Keep user-uploaded media and local Windows files outside Git unless explicitly transferred and their custody/rights are handled.
- Preserve historical distinctions and unresolved questions. Use OPEN, HYPOTHESIS, CONFLICT, SUPERSEDED or an appropriate HOLD rather than silently forcing a resolution.

## Read-only validation

From the repository root, run:

    python SUNO_HYMNS/scripts/validate_project_registry.py

The validator does not repair or modify files. It fails closed on invalid global state values, unknown IDs, missing source references and misleading status combinations.

## Next useful milestone

For each **existing** track, bring the exact lyric version, the verbatim Suno style prompt, the selected cover, final audio and metadata readback into a reproducible record. Those prompts are still `NOT_CAPTURED`; they must be recovered from the owner, not reconstructed.

For **DUTCH-004**, the immediate milestones are: the owner's poetic revision of the Russian draft; freezing the lyric and the prompt with a revision hash; and only then a first generation.

For the **historical research**, the two highest-value acquisitions are a page image of printed p. 84 of the 1676 impression (to close the narrowed date hold) and the 1674 *Meditatien* pamphlet.
