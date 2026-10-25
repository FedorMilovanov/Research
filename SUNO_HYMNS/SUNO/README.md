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

Every delivery to the owner — in chat or as a file — opens with **one line**: the Russian title in quotation marks, an em dash, the author's name. No labels, no separate "Название:" / "Автор:" rows.

```
«Хвала Славе» — Йодокус ван Лоденстейн
```

Rules for that line:

- the title comes **first**, the author **second**, always in that order;
- the title is the Russian working title in quotes; the historical title and its spelling go on the line below, not on the header line;
- the author carries dates in parentheses in documents: `Йодокус ван Лоденстейн (1620–1677)`; a chat delivery may use the bare name;
- a later reviser is named separately underneath, never merged into the author field;
- if the attribution is uncertain, the author field says so rather than being dropped.

Then, and only then, the historical title, the source and the status. Status, rights caveats and open questions never come before the title line.

## Lyric and pronunciation workflow

Keep these artifacts separate:

- source-language historical text;
- normalized transcription text;
- literal translation for analysis;
- Russian literary adaptation;
- SUNO-ready lyric with vocal cues and optional stress marks;
- published/recorded take.

For Russian SUNO lyrics, preserve the owner's wording unless an explicit edit is requested. Two rules, and they are different rules. **ё is always written** wherever Russian requires it — `всё`, `ещё`, `её`, `моё`, `нём`, every `-ёт` form — in both lyric files and in prose; `все` (plural), `свет`, `Его` keep `е`. **Stress marks are selective and decided by grammar:** mark a word when the same spelling can carry two stresses (`сто́ит`/`стои́т`), when the form's stress is not where a model defaults (`соединена́`, `помы́сли`, `дару́ет`), when the word is long or compound, when it is a biblical name, or when it has been **heard sung wrong** in a take. Never mark monosyllables, ё-words (the letter already carries the stress) or plain unambiguous polysyllables; if more than about a dozen words carry accents, the list has stopped being selective. A sung stress may legitimately differ from the dictionary one for the sake of rhyme or metre — then write the sung form and record why; if nothing in the stanza explains it, it is a mistake. Blanket marking was tried on 2026-10-25 and rejected by the owner: an accent changes the text the model reads and can cost its delivery. Full policy: `STYLE_AND_PRODUCTION_RULES.md` § Pronunciation marks; mechanical report: `scripts/check_ru_lyric.py`. Do not confuse machine-pronunciation marks with final public spelling. Preserve ё where required. Keep labels such as [Verse 1 — Cantor], [Cantor, Organ enters], [Cantor, Monks drone], [Growing] and [Full chant, all monks] separate from the lyric body and consistent across versions.

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

## Publication copies — three files, two markup languages

Copy for a finished track lives in one file per surface, all in this directory:

- `DUTCH-005_YOUTUBE.md` — title, description, hidden tags;
- `DUTCH-005_TELEGRAM.md` — the @lordchrist post;
- `DUTCH-005_PINNED.md` — the pinned YouTube comments.

**The two surfaces do not share markup.** YouTube: `*bold*`, `_italic_`, punctuation inside the wrapper. Telegram: `**bold**`, `*italic*`, italic on whole lines only, no markup on link lines. A single `*` is *italic* in Telegram and *bold* on YouTube; `**` prints literally on YouTube. Never copy one file's markup into the other without reformatting.

**Where the rules are normative:** `../projects/lord-god-strength/RULES.md` — one self-contained sheet for this channel, with no other channel's domains, playlists or footer in it. Exact channel IDs, community IDs, OAuth aliases and bot preflight belong to `video-channel-manager/docs/operations/*-description-profile.md`. The rendering standard there (`docs/youtube-description-rendering-standard.md`) remains the origin for platform behaviour, but it is written around the poetry project and has to be overridden for the theological one — a defect recorded in `../projects/WORKS_LEDGER.md`. `PUBLICATION_LANE.md` says which document governs what and lists the gates.

**Handoff to the owner:** always a fenced `text` block, never a quote — a quote renders the asterisks away and the markup never reaches the clipboard. Stated in `../projects/lord-god-strength/RULES.md` § 3, and in the channel standard; it was learned here the hard way in three rounds.

**A copy is not a publication.** The files above carry no URL and change no state. `PUBLISHED_VERIFIED` requires a checked public URL or a direct publication receipt, recorded in `STATUS_LEDGER.md`.

## Publication and rights boundary

Historical source research, audio generation, export, metadata QA, artwork approval, public upload and publication verification are separate milestones. The production lane does not grant rights to a modern critical edition, translation, recording, portrait or generated image. Add a public URL only after checking the live target.
