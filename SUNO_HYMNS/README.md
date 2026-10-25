# SUNO Hymns & Dutch Reformed Hymn Research

**Project ID:** SUNO-HYMNS-NL  
**Snapshot date:** 2026-10-25  
**State:** initialized; existing-work inventory recorded; historical research and asset verification remain open.

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
- **RESEARCH/README.md** — source-evidence method for historical hymn research.
- **RESEARCH/DUTCH_REFORMED_HYMNODY.md** — initial historical map of Dutch Reformed church singing.
- **RESEARCH/DUTCH_HYMN_CATALOG.md** — records for the three Dutch works developed in the conversation.
- **RESEARCH/DUTCH_HYMN_BACKLOG.md** — candidates not recorded as produced in the current project context.
- **RESEARCH/AUTHOR_*.md** — focused author dossiers.
- **RESEARCH/SOURCE_REGISTER.md** — sources, supported claims, locators, access and rights boundaries.
- **HANDOFF_FOR_NEXT_AGENT.md** — continuation instructions for a new Arena/chat agent.
- **data/track-catalog-v1.json** — project-local machine-readable track catalog.
- **data/source-registry-v1.json** — project-local source registry.

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

No public release status is promoted to verified in this repository snapshot. See the per-track ledger before making public claims.

## Non-negotiable research boundaries

- Do not collapse Lodenstein's dated 1674 poem, Rutgers's 1806 reworking, later Afrikaans hymn versions and the Russian lyric adaptation into one identical text.
- Do not describe Revius's original 14-line sonnet as a hymn with a documented original melody unless a primary source establishes that.
- Do not infer a melody, musical genre, lyric wording, Suno prompt or publication date from memory when the exact artifact is unavailable.
- A catalog page or reachable URL is not the same as full-object access; an exact title is not an exact locator; a historical public-domain text does not automatically clear rights in a modern critical edition, scan, translation or visual asset.
- Keep user-uploaded media and local Windows files outside Git unless explicitly transferred and their custody/rights are handled.
- Preserve historical distinctions and unresolved questions. Use OPEN, HYPOTHESIS, CONFLICT, SUPERSEDED or an appropriate HOLD rather than silently forcing a resolution.

## Next useful milestone

For each track, bring the exact lyric version, the verbatim Suno style prompt, the selected cover, final audio and metadata readback into a reproducible record. In parallel, advance one candidate from the Dutch hymn backlog using a primary-text locator and verified author/text/adaptation chain before creating another musical version.
