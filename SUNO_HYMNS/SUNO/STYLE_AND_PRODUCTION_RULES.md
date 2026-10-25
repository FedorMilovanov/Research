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

## Text preparation for SUNO — standing rules

These are project-wide working principles, adopted 2026-10-25 from the owner's notes. Per-work style decisions remain per-work and are recorded separately (see §"Per-work decisions").

1. **Keep the source text, the stanza order and the semantic structure**, unless the owner has explicitly permitted an adaptation. If an adaptation is permitted, it is labelled an adaptation and every departure is documented.
2. **Do not invent lines, refrains or repetitions.** Repeat text only where a musical or dramatic reason exists and can be stated. A printed `etc.` in a historical source is a *repeat instruction*, not a licence to add words.
3. **Use echo and whisper sparingly** — normally no more than one expressive echo per corresponding passage. If an effect fits inside a stanza, write it inline in parentheses rather than restructuring the stanza.
4. **Do not overload the lyric with technical tags** (`[Build]`, `[Pause]`, `[Instrumental]` and similar). Tags should help the performance, not displace words or lengthen the piece.
5. **For long texts that do not fit one generation, fix tempo first** — syllabic delivery, a short introduction, short transitions, no long instrumental gaps. Do **not** solve a length problem by arbitrarily deleting important stanzas or changing the meaning.
6. **Choose the musical style per work.** A per-work exclusion (for example, no guitar in the epic Lodenstein setting) is not a project-wide rule.
7. **Vocal default: clear diction, a strong and intelligible lead male voice, correct stress and natural pronunciation.** Avoid excessively breathy, whispered, hoarse or gratuitously low delivery unless a specific concept calls for it.
8. **Keep the literary translation separate from the musical adaptation.** Document and justify every departure from the source.

**Precedence.** Where a per-work decision and a standing rule conflict, the per-work decision wins — but it must be written down as a per-work decision, with its reason. The standing rules exist to prevent defaults from being invented silently.

**What these rules do not do.** They do not establish that any existing recording followed them. The three existing works have `NOT_CAPTURED` prompts, so compliance cannot be demonstrated retrospectively.

## Per-work decisions (not project defaults)

| Work | Decision | Status |
|---|---|---|
| DUTCH-001 | No single refrain across the eight stanzas — the Christological addresses vary in the source and must stay varied | `WORKING_DECISION` — see `../RESEARCH/DOSSIER_DUTCH-001_TRANSLATION_DECISIONS.md` |
| DUTCH-002 | Male monastic-style polyphony, powerful organ, epic and majestic; syllabic delivery; **112–120 BPM**; short intro and transitions; no long interludes; no stretched vowels — adopted because earlier generations came out too slow and whispered | `REPORTED_FROM_EARLIER_SESSIONS`, `NOT_CAPTURED` |
| DUTCH-002 | Guitar excluded | part of the above per-work brief only |
| DUTCH-003 | Either atmospheric guitar and cello, or a cappella with organ/cello/male ensemble entering after the sonnet's turn | `DISCUSSED_NOT_APPROVED` |
| DUTCH-004 | Chamber setting — cello, contrabass, theorbo, small organ pad, one flute line; two-voice choir from verse 4, four parts only in verse 7; ♩=65, 3/4 | `AUTHORED` in the production package; never generated |
| DUTCH-CAND-021 (*Heerlijckheyds Loff*) | Male monastic ensemble and epic organ — **and a duplication risk:** the same brief appears under DUTCH-002, and with no verbatim prompts held, it is not now determinable whether one prompt was reused for two poems | `DISCUSSED_NOT_APPROVED` |

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
