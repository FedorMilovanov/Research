# DUTCH-005 — style

**«Хвала Славе»** — Йодокус ван Лоденстейн (1620–1677)
*Heerlijckheyds Loff*, *Uyt-spanningen*, 1676, printed pp. 155–158.

**Status:** five directions, all `DOCUMENTED_NOT_YET_SUBMITTED` — written in this repository, **never submitted to SUNO**. None is chosen; the choice is the owner's. `STYLE-DUTCH-005-A` is marked **primary** only because the registry must carry one `promptText`, not because it is preferred.

Style only; no lyrics here. Lyrics: [`DUTCH-005_LYRICS.md`](DUTCH-005_LYRICS.md) · performable text: [`DUTCH-005_LYRICS_SUNO.md`](DUTCH-005_LYRICS_SUNO.md).

Every one of the five keeps the same floor: strictly syllabic, one syllable per note, no melisma, no stretched vowels, all ten verses in order with no cuts, no invented chorus, short introduction.

---

## A. Epic organ and Georgian-flavoured male monastic choir — `STYLE-DUTCH-005-A` · primary slot

```
epic sacred organ hymn, 4/4, 118 bpm, D minor, deep pipe organ with 16-foot pedal and full plenum, Georgian-flavoured male monastic choir in sustained parallel fifths, one clear tenor-baritone lead voice singing in front of the choir, strictly syllabic declamation, one syllable per note, no melisma, no stretched vowels, short two-bar organ introduction, all ten verses sung in order with no cuts, wide stone-church reverb but a forward, intelligible lead, restrained crescendo across the ten verses, no percussion, no guitars, no synthesizers
```

**Exclude:** drums, percussion, electric bass, synth pads, EDM, cinematic string swells, belting, breathy or whispered lead, husky voice, excessively low bass lead, heavy vibrato, melisma, vocal runs, auto-tune artefacts, spoken word, long instrumental interludes.

**For:** maximum monumentality. The poem is about the glory of heaven, and this is the register most listeners associate with that claim.
**Risk:** reverb plus a big plenum works against intelligibility on a 90-line text; the "forward lead" instruction is doing real work here.

## B. Renaissance wind consort with male voices — `STYLE-DUTCH-005-B`

```
Dutch seventeenth-century church music, 4/4, 112 bpm, D dorian, cornetto and two sackbuts leading, shawm doubling the tenor line, positive organ continuo, a consort of four male voices singing in thirds and fifths, one clear tenor soloist for the odd verses, strictly syllabic, no melisma, short two-bar intrada, all ten verses in order, bright forward articulation, dry-ish stone acoustic, no percussion, no guitars, no synthesizers
```

**Exclude:** drums, synth, electric instruments, heavy reverb, belting, breathy lead, melisma, vocal runs, long instrumental interludes.

**For:** the poem's own century. Cornetto and sackbut are what a Dutch town band actually played, and the bright, reedy timbre cuts through a long text far better than massed voices.
**Risk:** period winds can sound festive where the text is penitential in verses 1–6; the D-dorian mode and the syllabic setting are what hold it back.

## C. Viol consort, positive organ, solo tenor — `STYLE-DUTCH-005-C`

```
intimate consort hymn, 4/4, 100 bpm, G minor, two viols da gamba and a chamber organ with a stopped 8-foot flute, one solo tenor voice very close and dry, a second tenor joining only from verse 7, a third and fourth voice in verse 10, strictly syllabic, no melisma, no vibrato, unaccompanied first verse, all ten verses in order, quiet room acoustic, no percussion, no guitars, no synthesizers
```

**Exclude:** reverb wash, cathedral acoustic, drums, synth, electric bass, belting, breathy lead, melisma, vocal runs.

**For:** the owner's known preference for a restrained, dark acoustic sound. The ensemble grows verse by verse, so the arrangement itself traces the poem's ascent.
**Risk:** at 100 bpm the ten verses run long; verse 1 being unaccompanied helps the start, but the tempo must not drift below 100.

## D. Byzantine-style ison under a baritone cantor — `STYLE-DUTCH-005-D`

```
Byzantine-influenced sacred chant, free rubato over a slow pulse, E minor, one baritone cantor chanting the verses syllabically, a male choir holding a sustained ison drone on the tonic, a low bell-like organ pedal entering at verse 7, no melisma, no vibrato, all ten verses in order, narrow-range declamation, large but clear acoustic, no percussion, no guitars, no synthesizers
```

**Exclude:** melisma, vocal runs, wide melodic leaps, drums, synth, electric bass, belting, whispered lead, long instrumental interludes.

**For:** the strongest contrast of the five. The ison drone makes the tripled word land like a bell-strike, and free rubato suits a text that is closer to meditation than to hymnody.
**Risk:** free rubato is the exact failure mode this project has already suffered — a drifting, slow, half-whispered reading. Use only with a firm pulse underneath and a cantor who articulates consonants.

## E. Metrical chorale, unison male voices and organ — `STYLE-DUTCH-005-E`

```
Dutch metrical psalm style, 4/4, 126 bpm, A minor, unison male congregation singing a firm chorale melody, organ accompanying with clear manual voices and a pedal line, four-part harmony only on the last line of each verse, one precentor intoning the first line of each verse alone, strictly syllabic, no melisma, crisp consonants, all ten verses in order, no percussion, no guitars, no synthesizers
```

**Exclude:** drums, synth, electric bass, belting, breathy or whispered lead, melisma, vocal runs, heavy reverb, long instrumental interludes.

**For:** the safest of the five for completeness. Unison, syllabic, brisk and harmonically spare — nothing here invites the model to stretch a line, and ten verses fit comfortably.
**Risk:** least atmospheric. It serves the text rather than the mood, and would suit a release aimed at singing along rather than at listening.

---

## Comparison

| | A | B | C | D | E |
|---|---|---|---|---|---|
| Tempo | 118 (4/4) | 112 (4/4) | 100 (4/4) | free, slow pulse | 126 (4/4) |
| Mode | D minor | D dorian | G minor | E minor | A minor |
| Lead | tenor-baritone | tenor | tenor, close-miked | baritone cantor | precentor / unison |
| Ensemble | organ + monastic choir | cornetto, sackbuts, shawm, 4 voices | 2 viols, chamber organ, voices | ison drone choir | unison male voices + organ |
| Completeness risk | medium | low | medium-high | high | lowest |
| Character | monumental | period-bright | intimate | meditative | congregational |

**How they differ in one sentence each:** A floods the room; B puts a 17th-century town band in it; C takes the room away and leaves four voices; D turns the poem into chant; E turns it back into a psalm the congregation could sing.

## Settings that apply to all five

| Field | Value |
|---|---|
| Structure | `[Intro]` · ten `[Verse n]` tags · `[Outro]`; no chorus |
| Echo | at most one, inline, verse 10: `(хвалить)` |
| Repetitions | only the print's own: the threefold call line and the tripled word |
| If a verse is dropped | regenerate with `all ten verses, in order, no cuts`, raise tempo, shorten the intro — **never** cut stanzas |
| If it still truncates | split at the poem's seam (verses 1–5 / 6–10), same direction, same lead |
| Forbidden | added refrains, invented lines, stacked `[Build]`/`[Pause]`/`[Instrumental]` tags, a local `[Whisper]` against a global no-whisper instruction |

## Not claimed

- No melody is the 1665 tune. `Voyse: Un jour &c.` is untraced, and the 2005 apparatus says its origin is unknown and that it is not text 27's *Un jour*. Direction B is the closest to the poem's sound-world, but it is a modern reconstruction of a plausible idiom, not a recovery of the melody.
- No direction uses the 1938 Hymnal's reworking (*'t Oog omhoog, het hart naar boven!*, Bourgeois melody) — a different, protected object.
- These are per-work decisions. The no-guitar exclusion and every tempo figure belong to this work only, not to the project.
