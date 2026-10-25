# DUTCH-005 — style

**Work:** DUTCH-005 · *Heerlijckheyds Loff* (Lodenstein, 1676)
**Status:** `AUTHORED_NOT_YET_SUBMITTED` — written in this repository, **never submitted to SUNO**. No generation exists.

Style only; no lyrics here. Lyrics: [`DUTCH-005_LYRICS.md`](DUTCH-005_LYRICS.md) · performable text: [`DUTCH-005_LYRICS_SUNO.md`](DUTCH-005_LYRICS_SUNO.md).

---

## 1. Primary — `PROMPT-DUTCH-005-V1`

```
epic sacred organ hymn, 4/4, 118 bpm, D minor, deep pipe organ with 16-foot pedal and full plenum, Georgian-flavoured male monastic choir in sustained parallel fifths, one clear tenor-baritone lead voice singing in front of the choir, strictly syllabic declamation, one syllable per note, no melisma, no stretched vowels, short two-bar organ introduction, all ten verses sung in order with no cuts, wide stone-church reverb but a forward, intelligible lead, restrained crescendo across the ten verses, no percussion, no guitars, no synthesizers
```

**Exclude:**

```
drums, percussion, electric bass, synth pads, EDM, cinematic string swells, belting, breathy or whispered lead, husky voice, excessively low bass lead, heavy vibrato, melisma, vocal runs, auto-tune artefacts, spoken word, long instrumental interludes
```

## 2. What changed from v1, and why

| v1 | v2 | Reason |
|---|---|---|
| `one strong low male lead voice` | `one clear tenor-baritone lead voice` | a low bass lead darkens the diction and, on a long text, blurs the words. The project's preference is a clear, projecting tenor-baritone; the monumentality is carried by the organ and the choir, not by pushing the lead down |
| `116 bpm` | `118 bpm` | with ten verses of nine lines, a small tempo margin is worth more than a grander pace |
| `declaiming syllabically` | `strictly syllabic declamation, one syllable per note, no melisma, no stretched vowels` | "syllabic" alone was not enough; the model needs the prohibition spelled out, because long vowels are the main way this text would overrun |
| `restrained crescendo across ten stanzas` | `restrained crescendo across the ten verses` + `all ten verses sung in order with no cuts` | the crescendo is a shape, not a guarantee of completeness; completeness must be asked for explicitly |
| `wide stone-church reverb` | `wide stone-church reverb but a forward, intelligible lead` | reverb was working against intelligibility on a dense text; it stays, but not over the lead |
| — | `short two-bar organ introduction` | a long organ prelude eats the duration budget and delays the first line |
| — | `no long instrumental interludes` (in exclude) | same reason, stated where the model reads prohibitions |

## 3. Alternative — `DOCUMENTED_OPTION`, not a version

```
solemn organ and low strings hymn, 3/4, 112 bpm, F minor, great organ foundation stop and pedal drones, cello and contrabass doubling the bass line, a quartet of low male voices entering only from verse 4, one clear baritone cantor for the call lines, syllabic declamation, no melisma, plain diction, no percussion, no guitars
```

**Different intent, not a fallback.** §1 is a wall of monastic sound from bar one; §3 holds the choir back so that its entry marks the poem's own turn. §3 was previously set at 104 bpm with a bass cantor; both were raised and lightened for the same reason as §2 — intelligibility over depth.

## 4. Settings that apply to either

| Field | Value |
|---|---|
| Structure | `[Intro]` · ten `[Verse n]` tags · `[Outro]`; no chorus |
| Echo | exactly one, inline, verse 10: `(хвалить)` |
| Repetitions | only the print's own: the threefold call line and the tripled word |
| If a verse is dropped or compressed | add `all ten verses, in order, no cuts`, raise tempo, shorten the intro — **never** cut stanzas |
| If it still truncates | split the release at the poem's seam (verses 1–5 / 6–10), same style, same lead |
| Forbidden by project rule | added refrains, invented lines, stacked `[Build]`/`[Pause]`/`[Instrumental]` tags, local `[Whisper]` against a global no-whisper instruction |

## 5. Why this brief, for this text

- **Length.** Ten verses of nine lines, roughly 90 lines. At 118 bpm with strictly syllabic delivery the words fit; at a slower, more melismatic setting they do not, and the model will start compressing.
- **The device.** The tripled word `жизнь → любить → хвалить` needs every syllable audible; melisma and stretched vowels are what destroy it.
- **The turn.** Verses 1–6 are vanity and warning, 7–10 are beauty and praise. The structure tags put the change of texture where the text changes, which a style prompt alone cannot do.
- **Voice.** A tenor-baritone lead keeps the words forward. "Low" was a mistake: it sought gravity at the cost of diction.
- **No melody is claimed.** `Voyse: Un jour &c.` is untraced; the 2005 apparatus says its origin is unknown and that it is not text 27's *Un jour*.
- **Scope.** Per-work decision: the no-guitar rule and the 118 bpm belong to this setting only, not to the project.
