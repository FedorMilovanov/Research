# SUNO Hymns & Dutch Reformed Hymn Research

**Project ID:** SUNO-HYMNS-NL  
**Snapshot date:** 2026-10-26  
**State:** publication pass (2026-10-26), plus a new lane opened the same day. DUTCH-005 carries a full publication package — YouTube titles, description, tags, two pinned comments and a Telegram post — and the owner reports it generated, covered and uploaded; no URL, file or take is held here, so nothing is marked published. **PHOS-001** (Φῶς ἱλαρόν, «Свет радостный») is a new, non-Dutch work: a Russian verse **translation** of six Greek lines and five style directions exist; nothing is generated. Earlier works keep their states; prompt recovery for DUTCH-001/002/003 is still open.

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
7. For anything that ends in a public post — title, description, pinned comment, Telegram post, tags — read `SUNO/PUBLICATION_LANE.md` before drafting. It names the normative channel standards, the three copy files and the gates, so no agent has to guess where a formatting rule lives.
8. `RESEARCH/LESSONS_AND_GUARDS.md` — the register of errors already made in this project, each with the guard that now catches it.

The root Research authority and evidence policy remain controlling. Nothing in this directory can redefine global source classes, HOLD semantics, rights rules, or publication approval. This is a scoped project index, not a replacement authority.

## Directory map

- **SUNO/README.md** — production workflow and state model.
- **SUNO/STATUS_LEDGER.md** — known prepared works, incomplete checks and publication boundaries.
- **SUNO/PUBLICATION_LANE.md** — the bridge to the channel standards: which repository is normative for markup and comment layout, the three copy files, the five gates, and the eight traps that already cost a release. Read this before editing any copy.
- **SUNO/DUTCH-005_YOUTUBE.md** — title options, the ready description (4598 characters, 12 bold and 5 italic spans), hidden tags, a checklist, and § 0: the verbatim post-mortem of the markup that broke live in Studio.
- **SUNO/DUTCH-005_TELEGRAM.md** — the @lordchrist post for the same hymn, in Telegram markup (`**bold**`, `*italic*`), with an HTML twin.
- **SUNO/DUTCH-005_PINNED.md** — two pinned comments for YouTube: one on the hymn, one on how the Dutch sang, both in YouTube markup and gated.
- **SUNO/STYLE_AND_PRODUCTION_RULES.md** — accumulated user preferences and reproducibility rules.
- **SUNO/ASSET_MANIFEST.md** — reported local filenames, exports, metadata and unresolved verification.
- **SUNO/DUTCH-004_PRODUCTION_PACKAGE.md** — the next work: form decision, gloss, Russian draft, deviations, musical brief, authored prompt and a per-element status table.
- **SUNO/DUTCH-005_PRODUCTION_PACKAGE.md** — *Heerlijckheyds Loff* (1676, pp. 155–158): ten-stanza gloss, Russian adaptation v0.1, eight declared deviations, and two style directions for SUNO (one primary, one option).
- **SUNO/DUTCH-005_LYRICS.md** — clean Russian lyric, revision v0.10, with changelog and a **measured** syllable table; the stanza 3.2 defect is fixed there and awaits the owner's signature.
- **SUNO/DUTCH-005_LYRICS_SUNO.md** — the same lyric with `[Intro]`/`[Verse n]`/`[Outro]` tags and three performance accents, for the SUNO editor.
- **SUNO/DUTCH-005_STYLE.md** — style only: **five** distinct directions A–E (organ/monastic, Renaissance wind consort, viol consort, Byzantine ison, metrical chorale), each with exclude list, purpose and risk.
- **RESEARCH/README.md** — source-evidence method for historical hymn research.
- **RESEARCH/DUTCH_REFORMED_HYMNODY.md** — initial historical map of Dutch Reformed church singing.
- **RESEARCH/DUTCH_HYMN_CATALOG.md** — records for the three Dutch works developed in the conversation.
- **RESEARCH/DUTCH_HYMN_BACKLOG.md** — candidates not recorded as produced in the current project context.
- **RESEARCH/AUTHOR_*.md** — focused author dossiers.
- **RESEARCH/SOURCE_REGISTER.md** — human-readable view of the source registry.
- **RESEARCH/CLAIM_LEDGER.md** — claim-by-claim support, caveats and typed HOLDs.
- **RESEARCH/SONGBOOK_REGISTER.md** — publication editions and the actual access layer.
- **RESEARCH/GENRE_AND_CLASSIFICATION.md** — controlled distinctions between psalms, devotional songs, sonnets, later adaptations and modern settings.
- **RESEARCH/LESSONS_AND_GUARDS.md** — errors already made in this project, each paired with the guard that now catches it. Read before drafting a lyric, applying a review or generating artwork.
- **RESEARCH/REVIEW_LOG_2026-10-25.md** — corrections made by the second audit and by every later pass, including the markup post-mortem and the pinned-comment pass.
- **RESEARCH/DUTCH-005_SOURCE_RUN_50PLUS.md** — the 75-link source run behind the description and the first pinned comment.
- **RESEARCH/DUTCH-005_SINGING_PRACTICE_SOURCES.md** — the 88-source run behind the second pinned comment: church singing, the organ ban, the voorzanger, the gezelschappen, and Lodenstein's own singing rules from the 1727 preface.
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
- **scripts/check_ru_lyric.py** — read-only Russian lyric audit: lists words that must carry ё in context, and fails a file that carries more than a handful of stress marks.
- **scripts/check_youtube_markup.py** — read-only markup gate: a closing `*` or `_` must be followed by a space or end of line, `**` is rejected, markup is rejected in the first paragraph.
- **scripts/check_revision_consistency.py** — read-only check that the prose names the current lyric revision and does not contradict the files.
- **scripts/check_copy_lengths.py** — read-only guard that recomputes the description, both pinned comments and the visible Telegram length, and fails when a document quotes a stale number.

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
    python SUNO_HYMNS/scripts/check_ru_lyric.py SUNO_HYMNS/SUNO/*LYRICS*.md
    python SUNO_HYMNS/scripts/check_revision_consistency.py

All five gates run as separate steps in `.github/workflows/suno-hymns-registry.yml`: registry validation, markup of the description and both pinned comments, quoted lengths against the files, revision consistency, and the Russian lyric check.

The validator does not repair or modify files. It fails closed on invalid global state values, unknown IDs, missing source references and misleading status combinations.

## Next useful milestone

For each **existing** track, bring the exact lyric version, the verbatim Suno style prompt, the selected cover, final audio and metadata readback into a reproducible record. Those prompts are still `NOT_CAPTURED`; they must be recovered from the owner, not reconstructed.

For **DUTCH-005**, the copy exists and is gated, the title separator is settled (✝), and the owner reports the hymn generated and uploaded with a cover. What the repository still lacks is the evidence: two URLs, the cover file, the exact prompt, and the sung wording of stanza 3. The copies are **not** publication and carry no URL.

For **DUTCH-004**, the immediate milestones are: the owner's poetic revision of the Russian draft; freezing the lyric and the prompt with a revision hash; and only then a first generation.

For the **historical research**, the two highest-value acquisitions are a page image of printed p. 84 of the 1676 impression (to close the narrowed date hold) and the 1674 *Meditatien* pamphlet.
