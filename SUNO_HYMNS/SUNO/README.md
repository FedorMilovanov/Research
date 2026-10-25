# SUNO — production lane

## Purpose

This directory holds the production ledger for SUNO-created music based on historical Dutch devotional texts and practical conventions for reproducing releases. It is a production record, not historical evidence. Historical claims must be sourced in the RESEARCH lane.

## Project-local production states

Use one current state per work/version; if a work has different states by version, record them separately:

- NOT_STARTED — no lyric or generation work recorded.
- RESEARCH_IN_PROGRESS — source text, authorship, edition or adaptation chain is not clear enough for stable lyric work.
- LYRIC_DRAFT — a lyric draft exists, but no generation output is confirmed.
- SUNO_OUTPUT_GENERATED — a generation output is reported, but the export package is incomplete.
- ASSETS_PREPARED — audio export and expected cover/video assets are reported as created.
- READY_FOR_REVIEW — audio, tags, lyrics, image and historical credit have been checked together.
- PUBLISHED_VERIFIED — public publication is supported by a checked YouTube/Telegram URL or direct receipt.
- BLOCKED — a named unresolved dependency prevents progression.

These are project-local production states, not the root Research publicationState, source classes or HOLD values. ASSETS_PREPARED never implies PUBLISHED_VERIFIED.

## Per-version minimum record

For every version, capture:

1. stable work ID and version ID;
2. original title and author spelling, plus normalized display title;
3. source/edition/adaptation chain ID from the RESEARCH lane;
4. exact lyric file and revision identifier;
5. exact Suno style prompt, recorded verbatim;
6. exact section tags used in the lyric editor;
7. creation date, output filename, duration and format;
8. audio export and cover identifiers;
9. embedded metadata readback (title, artist, album, genre, cover presence);
10. YouTube and Telegram derivatives, technical properties and file hashes if available;
11. QA state, unresolved issues and public URL only after direct verification.

If an exact prompt or source lyric is unavailable, use NOT CAPTURED. Never rewrite a prompt from memory and label it exact.

## Delivery header — required on every handout

Every time a work is delivered to the owner — in chat or as a file — the first two lines are, in this order and in this order only:

1. **Title** — the historical title as printed, then the working Russian title if one exists.
2. **Author** — name with dates, and any later reviser named separately.

Nothing precedes them: not the status, not the analysis, not the prompt. The status and the rights caveats follow underneath, because a title and an author are the one thing the owner needs in order to decide whether to read further.

Short form for chat:

```
Название: <as printed> (<Russian working title, if any>)
Автор: <name> (<years>), <reviser if any>
```

Do not omit the author when the text is anonymous only because the attribution is uncertain — write `attribution uncertain` in the author field instead.

## Lyric and pronunciation workflow

Keep these artifacts separate:

- source-language historical text;
- normalized transcription text;
- literal translation for analysis;
- Russian literary adaptation;
- SUNO-ready lyric with vocal cues and optional stress marks;
- published/recorded take.

For Russian SUNO lyrics, preserve the owner's wording unless an explicit edit is requested. Add stress marks only where pronunciation ambiguity or known model errors warrant them; validate each word form in context. Do not confuse machine-pronunciation marks with final public spelling. Preserve ё where required. Keep labels such as [Verse 1 — Cantor], [Cantor, Organ enters], [Cantor, Monks drone], [Growing] and [Full chant, all monks] separate from the lyric body and consistent across versions.

Before generating, audit:
- historical names and theological terms;
- grammatical case and inflection in every stressed form;
- whether stress marks could be misread as text changes;
- stanza order and omitted/repeated lines;
- the distinction between Scripture quotation and lyric adaptation.

## Metadata and exports

Reported prior delivery patterns include H.264 1080p30 MP4s for YouTube and 320-kbps, 48-kHz stereo MP3s with embedded cover for Telegram. Verify rather than assume these settings for new exports.

Titles inside ID3 should be clean display titles without decorative quotation marks. Use ordinary spaces in filenames. Do not delete spaces or concatenate words when cleaning underscores; replace underscores with spaces if requested. If rewriting tags with ffmpeg, preserve the audio stream and cover where intended, strip generation metadata only when requested, then use ffprobe or a tag reader to verify the result.

## Current style guidance

The owner's accumulated preferences include restrained, dark acoustic sacred music; strings, cello and contrabass may be useful; avoid an unpleasantly harsh or “smoker-like” bass. A solemn historical/Reformed devotional atmosphere is generally appropriate. Scripture-song experiments have used cantor-led delivery, organ entering later, low monastic drone and a gradual build toward full chant.

These are preferences and examples, not a fixed prompt for every hymn. Choose style according to the text, voice, tempo, dynamic arc and intended listener. Exact final prompts used for existing Dutch tracks have not yet been collected into this repository.

## Canonical per-version records

Use LYRIC_REGISTER.md for historical/source text, normalized transcription, Russian adaptation and the exact SUNO-ready lyric. Use PROMPT_AND_VERSION_REGISTER.md to capture the submitted prompt verbatim and attach every generation/export to a stable version ID. Missing text/prompt remains NOT CAPTURED; do not infer it from the finished sound.

## Publication and rights boundary

Historical source research, audio generation, export, metadata QA, artwork approval, public upload and publication verification are separate milestones. The production lane does not grant rights to a modern critical edition, translation, recording, portrait or generated image. Add a public URL only after checking the live target.
