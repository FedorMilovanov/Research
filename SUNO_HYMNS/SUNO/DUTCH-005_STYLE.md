# DUTCH-005 — style

**Work:** DUTCH-005 · *Heerlijckheyds Loff* (Lodenstein, 1676)
**Status:** `AUTHORED_NOT_YET_SUBMITTED` — written in this repository, **never submitted to SUNO**. No generation exists.

This file holds **style only** — no lyrics. Lyrics: [`DUTCH-005_LYRICS.md`](DUTCH-005_LYRICS.md) · SUNO-ready text with labels: [`DUTCH-005_LYRICS_SUNO.md`](DUTCH-005_LYRICS_SUNO.md).

---

## 1. Primary — `PROMPT-DUTCH-005-V1`

Copy exactly; the registry holds this string byte-identically.

```
epic sacred organ hymn, 4/4, 116 bpm, D minor, deep pipe organ with 16-foot pedal and full plenum, Georgian-flavoured male monastic choir singing sustained parallel fifths, one strong low male lead voice declaiming syllabically in front of the choir, wide stone-church reverb, unhurried but never dragging, restrained crescendo across ten stanzas, clear diction and natural stress, no percussion, no guitars, no synthesizers
```

**Exclude:**

```
drums, percussion, electric bass, synth pads, EDM, cinematic string swells, belting, breathy or whispered lead, excessive vibrato, auto-tune artefacts, spoken word
```

---

## 2. Alternative — `DOCUMENTED_OPTION`, not a version

```
solemn organ and low strings hymn, 3/4, 104 bpm, F minor, great organ foundation stop and pedal drones, cello and contrabass doubling the bass line, a quartet of low male voices entering only from stanza 4, one solo bass cantor for the call lines, plain declamation, no percussion, no guitars
```

**Difference in intent.** §1 is a wall of monastic sound from the first bar. §2 holds the choir back until stanza 4, so the entry of voices marks the poem's own turn from the vanity of earth to the glory of heaven. Both are legitimate readings of the same text; the choice belongs to the owner and is not made here.

---

## 3. Settings that apply to either

| Field | Value |
|---|---|
| Structure | `[Intro — Organ pedal, 2 bars]` · ten stanza labels · `[Outro — Choir alone, last line, then silence]` |
| Echo | exactly one, inline, stanza 10: `(хвалить)` |
| Repetitions | only the print's own: the threefold call line and the tripled word |
| If the output drags or whispers | raise tempo, shorten the intro, tighten transitions — **never** cut stanzas |
| Forbidden by project rule | added refrains, invented lines, stacked `[Build]`/`[Pause]`/`[Instrumental]` tags |
| Register | clear diction, natural stress, a strong low male lead; no breathy, husky or gratuitously low delivery |

---

## 4. Why this brief, for this text

- **Length.** Ten stanzas of nine lines. At a slow tempo this runs long and flattens the poem's progression, so tempo and syllabic delivery are load-bearing, not decoration.
- **The device.** The tripled word `жизнь → любить → хвалить` needs space and clarity; a washed-out, whispery mix erases it. Hence the syllabic lead and the restrained crescendo rather than a full-voice start.
- **The turn.** The poem moves from vanity (1–6) to beauty and praise (7–10). §1 marks it dynamically; §2 marks it by adding voices. Either way the turn is marked.
- **No melody is claimed.** The printed direction `Voyse: Un jour &c.` is untraced and the 2005 apparatus says its origin is unknown and that it is not text 27's *Un jour*. Nothing here reconstructs the 1665 tune.
- **Scope.** This is a per-work decision. The no-guitar exclusion is local to this setting, and the 116 bpm figure belongs to this text only — neither is a project default.

---

## 5. Not in this file

- No lyrics and no lyric revision (they live in the two lyric files).
- No generated audio, duration, model name or file hash — nothing has been generated.
- No use of the 1938 Hymnal's reworking (*'t Oog omhoog, het hart naar boven!*, Bourgeois melody): a different, protected object.
