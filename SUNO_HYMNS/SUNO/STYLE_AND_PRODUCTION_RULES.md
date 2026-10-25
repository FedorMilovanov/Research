# SUNO style, lyric and export rules

This is a living project-local playbook. It records confirmed preferences and production QA; it is not a substitute for the exact per-track prompt.

## Style principles

1. Start with the text's genre and rhetorical arc. A penitential confession, quiet devotional song, Passion sonnet and Scripture cantata should not receive the same arrangement by default.
2. For Lodenstein, the context is seventeenth-century Dutch Reformed devotional song, not a generic medieval Catholic chant. Choose period-aware sacred textures without falsely claiming historically authentic instrumentation.
3. Known owner preferences: restrained dark acoustic atmosphere; strings, cello and contrabass may fit; avoid an unpleasantly harsh or “smoker-like” bass. Maintain diction clarity and deliberate dynamics.
4. If using choir/cantor, specify roles consistently. Scripture-song experiments used labels such as [Verse 1 — Cantor], [Cantor, Organ enters], [Cantor, Monks drone], [Growing] and [Full chant, all monks]. These are modern arrangement experiments, not evidence of historical performance practice.
5. Avoid overscoring every line. Changes in density should serve the lyric: quiet confession, measured exposition, controlled build, final culmination and silence where structurally appropriate.
6. Store each generated style prompt verbatim. If it cannot be recovered, mark NOT CAPTURED; do not manufacture an “original” prompt from memory.

## Historical sound versus modern adaptation

- A source's printed melody direction, when verified, belongs in Research as historical evidence.
- A new SUNO style prompt belongs in production metadata and must not be attributed to the historical poet.
- For *Schepselen niet en Jesus al*, the 1676 text gives a tune direction to *Rosemont waer gy vliedt*. This is a historical tune indication, not evidence that a modern SUNO take recreates the original arrangement.
- *Hy droech onse smerten* is cataloged as a sonnet; no original melody direction is verified in the current record. Treat any music as a modern setting unless a primary source is located.

## Pronunciation marks

- Inspect the exact inflected form in its sentence, not just the dictionary lemma.
- Add acute stress marks where SUNO has a plausible misreading or known model error. Do not unnecessarily accent every ordinary word in the final lyric.
- Preserve the actual grammatical form and meaning. A stress mark must not change a word into another word.
- Keep a clean literary lyric separately from the SUNO-readable stressed version.
- For biblical names and archaic/Church-Slavonic forms, conduct an explicit pronunciation check.
- If a source word is ambiguous or the translation may be wrong, resolve the textual/linguistic issue before adding a stress mark.

## Version discipline

Each version needs a stable ID, e.g. DUTCH-002-V1 and DUTCH-002-V2. Never overwrite V1 when generating V2. Record differences in vocal lead, tempo, instrumentation, dynamics, pronunciation corrections, ending, duration and export.

Before declaring READY_FOR_REVIEW, check:
- all stanzas and lines are present and in order;
- there are no accidental repeated or omitted verses;
- diction is intelligible and stress marks sound natural;
- there is no clipped beginning/end or unintended silence;
- audio and artwork match the intended title/version;
- title/artist/album/genre tags have been read back from the output file;
- public copy does not conflate historical source, Russian adaptation and modern arrangement.

## Export and metadata QA

Reported prior delivery patterns include H.264 1080p30 MP4s for YouTube and 320-kbps, 48-kHz stereo MP3s with embedded cover for Telegram. Verify rather than assume these settings for new exports.

Titles inside ID3 should be clean display titles without decorative quotation marks. Use ordinary spaces in filenames. Do not delete spaces or concatenate words when cleaning underscores; replace underscores with spaces if requested. If rewriting tags with ffmpeg, preserve the audio stream and cover where intended, strip generation metadata only when requested, then verify with ffprobe or a tag reader.

## Image and cover continuity

The owner prefers cinematic, restrained, muted grading rather than oversaturated red/orange. Cooler tones may appear in stone, shadow and ambient light while retaining natural warm focal light. Preserve approved composition and face unless a specific edit is requested. Record feedback so a later agent does not regenerate a rejected look. Do not claim the final DUTCH-003 cover is approved until the owner confirms the exact output.

## Publication and rights boundary

Historical source research, audio generation, export, metadata QA, artwork approval, public upload and publication verification are separate milestones. The production lane does not grant rights to a modern critical edition, translation, recording, portrait or generated image. Add a public URL only after checking the live target.
