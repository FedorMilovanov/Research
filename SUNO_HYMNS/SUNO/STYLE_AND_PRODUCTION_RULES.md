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
9. **Буквальность изначально (owner's rule, 2026-10-27): when a rendering choice exists, take the more literal option first.** The literal option is the one closest to the source word, case, word order and syntax. Smoothing may be recorded as an alternative, but it is not the starting point, and every departure from the literal one is written down with its reason.

**What "literal first" means in practice (adopted with rule 9):**

- **Word order stays** wherever the target language allows it. Reordering is a departure and is documented as one.
- **Case stays.** A Greek vocative is rendered by a Russian vocative, not by a nominative, unless a per-work decision says otherwise.
- **Calques beat stylistic synonyms** where the calque is the exact equivalent: `μονογενής` → «единородный», not «единственный»; `δοξολογοῦμεν` → «славословим», not «славим»; `εὐχαριστοῦμεν` → «благодарим», not «спасибо говорим».
- **Church-Slavonic forms are not banned** — they are chosen when they are the literal equivalent («в вышних», «Вседержитель», «одесную»), and rejected when they are flavour («тихий» вместо «отрадный»). The test is literalness, not registered.
- **Precedence is unchanged:** an explicit owner decision about a given work — its title, its name, its register — wins over rule 9 and is recorded as a per-work decision below. Rule 9 governs the choices that are still open.

**Precedence.** Where a per-work decision and a standing rule conflict, the per-work decision wins — but it must be written down as a per-work decision, with its reason. The standing rules exist to prevent defaults from being invented silently.

**What these rules do not do.** They do not establish that any existing recording followed them. The three existing works have `NOT_CAPTURED` prompts, so compliance cannot be demonstrated retrospectively.

## Style delivery — five distinct directions per work

Adopted 2026-10-25 at the owner's direction. For every work, deliver **five style directions**, not one. One of them may be marked primary; the other four are documented options. Choosing between them is the owner's decision, and the five must be genuinely different from each other — different ensembles, different vocal weight, different historical or regional idiom — not five rewordings of the same prompt.

What every direction must keep, however different it sounds:

- **strictly syllabic delivery** — one syllable per note, no melisma, no stretched vowels;
- **intelligible lead** — clear diction, natural stress; no breathy, whispered or husky delivery, and no gratuitously low bass lead unless a concept needs it;
- **all stanzas in source order, no cuts**;
- **no invented chorus, refrain or lines**;
- short introduction and short transitions; long instrumental interludes counted against the text's duration budget.

What may differ freely: instrumentarium, vocal constitution, language region and era of the idiom, tempo, metre, density of polyphony, and the point at which the ensemble enters.

Each direction is recorded with: an ID, a one-line label, the prompt string, what is excluded, what it is for, and its risk. **Five prompts per work is the delivery minimum; none of them is "the" style until the owner picks one.**

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

Two separate jobs. **ё is orthography** — it is always written, everywhere. **Stress marks are a hint for the model** — they go on a few words, chosen by rule, never on all of them.

### 1. ё — always, everywhere it belongs

- Write **ё** in every word where Russian requires it: `всё`, `ещё`, `её`, `моё`, `твоё`, `своё`, `нём`, `живёт`, `даёт`, `поёт`, `идёт`, `пойдёт`, `пропадёт`, `крадёт`, and every other `-ёт` / `-ёшь` form, plus `тёмный`, `мёртвый`, `лёгкий`, `твёрдый`, `чёрный`, `жёлтый`, `тёплый`.
- This applies to **both** lyric files, to prose, and inside headings and quotations. A lyric that prints `все` for `всё` is simply a spelling error, not a stylistic choice.
- Do not swap a genuine `е` for `ё` to look archaic: `все` (plural) stays `все`, `свет` stays `свет`, `Его` stays `Его`.
- A **ё already carries the stress**, so a ё-word never gets an accent as well. Two marks on one word is a defect.
- Mechanical check: `python scripts/check_ru_lyric.py <files>` lists every occurrence of a word that must carry ё in context (`все/всё` included, decided per line). It reports; a human decides.

### 2. Stress marks — by grammar, on the words that need them

An accent is **not** an annotation. It is a change to the text the model reads: applied broadly it bends the diction, costs the model its own phrasing and flattens the delivery. So the rule is selective, and it is decided by grammar, not by taste.

**Mark a word when at least one of these is true:**

1. **The same spelling carries two stresses in Russian** and grammar decides which: `сто́ит` ("is worth") vs `стои́т` ("costs"); `узна́ю` / `узнаю́`; `до́ро́г`-type cases only where the line is genuinely ambiguous.
2. **The stress is fixed by the grammatical form but is not where a model defaults:** short feminine participles and adjectives on the ending (`соединена́`, `заключена́`, `рождена́`), imperatives (`помы́сли`, `воспря́нь`, `сомкни́`), `-у́ет` verbs often mis-stressed in speech (`дару́ет`, not `да́рует`).
3. **Long or compound words** where the stress is not audible from the stem: `драгоце́нная`, `прекрасне́йшая`, `благослове́нный`, `недоуме́ние`.
4. **Biblical names and Church-Slavonic forms**, checked explicitly: `Иису́с` (four syllables), `Госпо́день`, `Церко́вь`, `Богоро́дица`.
5. **A word heard sung wrong in an actual take.** This always earns a mark, whatever the rules above say.

**Never mark:**

- monosyllables (`зрят`, `ввысь`, `прах`, `тлен`, `свет`) — an accent cannot help and can be read as a vocal instruction;
- ё-words — the letter already sets the stress;
- plain polysyllables with one possible stress (`душа`, `сердце`, `любовь`, `Небо`, `жизнь`, `радость`) — these are the majority of any text and marking them is the blanket practice that was rejected;
- the same word twice in one stanza unless both occurrences are genuinely at risk.

**Then count.** If more than roughly a dozen words in a lyric carry accents, the list has stopped being selective — cut it back to the words the rules above actually reach. `scripts/check_ru_lyric.py --max-marks N` fails a file that exceeds the limit.

### 3. When singing overrides the dictionary

A sung stress is not always the dictionary stress, and this is legitimate:

- **Rhyme and assonance** can pull a stress onto the rhyming syllable, and a hymn that rhymes must be allowed to do it.
- **Metre and the tune** can lengthen or shift a stress; a syllable that is stressed in speech may sit on a weak beat.
- Where the sung form is deliberate, **write the sung stress, and record the case** in the deviation table with the reason. Do not "correct" a singer into an unrhymed line.
- Where the sung form is an accident of the model, that is an error, not a licence — fix it.
- The distinction is decided by the text, not by convenience: if the line rhymes and the shifted stress serves the rhyme, it is deliberate; if nothing in the stanza explains it, it is a mistake.

### 4. Two-layer discipline

- Accents live in the **SUNO-ready file only**; the clean literary lyric carries none, and no published text ever carries them.
- If a marked word is later edited, re-check the mark: a stale accent across an edit is a new defect.
- Keep the clean lyric, the marked lyric, the translation and the source text as separate files; never mix them.

### 5. Before adding any mark

- Inspect the exact inflected form in its sentence, not the dictionary lemma.
- If the wording itself may be wrong, resolve the text first, then mark it. Do not paper over a bad line with an accent.
- Check that the mark cannot be misread as a different word: `за́мок`/`замо́к`, `му́ка`/`мука́`, `сто́ит`/`стои́т`.

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

## Failure guards

Added 2026-10-25 after the DUTCH-005 session. Each line here answers an error that actually happened; the evidence is in [`../RESEARCH/LESSONS_AND_GUARDS.md`](../RESEARCH/LESSONS_AND_GUARDS.md).

1. **A rhyme may cost a word, never a meaning.** Any slot where rhyme changed a word gets a verdict in the work's lyric file — *kept because …* or *reverted*. A word that exists only for the rhyme is a rewrite.
2. **One trade, one decision, all stanzas.** If rhyme is rolled back in one stanza for a reason, the same trade in another stanza is rolled back too, in the same revision. Do not ship a text that is literal in stanza 1 and free in stanza 2 for the same cause.
3. **Count the source's repetitions before mirroring them.** Three `op aard` and a final `niet waard` is a device with a turn; four identical words is a refrain, and a refrain may not be invented.
4. **Never overwrite a revision in place.** Keep the previous text retrievable by path or by `git show`. After a wholesale rewrite, diff the section headings against the previous commit.
5. **Numbers come from the file, not from memory** — verses, lines, stress marks, rhyme slots. `scripts/check_ru_lyric.py` and `scripts/check_revision_consistency.py` are the two gates; the second is a CI step and fails on stale revisions, stale counts and duplicated sentences.
6. **A known-wrong label goes in the delivery header the turn it is found** — a working title, a misattributed line, a guessed date. Recording it in a file is not raising it.
7. **Say back a house term before spending budget.** "Баттл" = one generation that offers **two** candidates; three battles = six images. Misreading cost two rounds of artwork.
8. **Editing, committing, pushing and reading CI are four separate short commands.** Never sleep to wait for CI; if the state is unknown, say it is unknown.
9. **Keep the verbs apart:** "the reviewer said the commentary glosses it…" is a lead; "the print reads `nog`" is a check. A register that cannot tell them apart is worthless.

## Publication and rights boundary

Historical source research, audio generation, export, metadata QA, artwork approval, public upload and publication verification are separate milestones. The production lane does not grant rights to a modern critical edition, translation, recording, portrait or generated image. Add a public URL only after checking the live target.
