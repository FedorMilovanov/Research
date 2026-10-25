# DUTCH-002 — text history across three hymnals (14 → 7 → 5 stanzas)

**Work:** `DUTCH-002`, Russian release title «Блаженно, блаженно — быть ничем»
**Source author:** Jodocus van Lodenstein · **later reviser:** Abraham Rutgers
**Dossier opened:** 2026-10-25 (fourth pass)
**Status of the Russian text:** **NOT IN THIS REPOSITORY.** No translation claim is made or implied here.

This dossier exists to fix one thing precisely: the stanza counts and the exact relation between the three forms. A previous statement held that the 1806 hymn has five stanzas. **It has seven.** The five-stanza form is the 1938 hymnal.

## 1. The three forms, verified

| Form | Witness | Stanzas | Status of verification |
|---|---|---|---|
| **1676** — *II. Hert-sterckte in Jehova. Op 1 Sam. 30:6* | *Uyt-spanningen*, Utrecht: Willem Clerck, 1676, **printed pp. 82–84** | **14** (I–XIV) | text read in full in the third pass; `SRC-L-1676-HERT-II-82-84` |
| **1806** — *Zelfverloochening*, **no. LXVIII** | *Evangelische Gezangen…* (1806), **printed pp. 143–144** | **7** (numbered 1–7) | read in full in this pass from the DBNL transcription; `SRC-RUTGERS-1806-68` |
| **1938** — *Zalig, zalig, niets te wezen*, **Gezang 205** | *Psalmen en Gezangen voor den Eeredienst* (Hervormde Bundel 1938) | **5** (numbered 1–5) | **not verified against the printed bundel**; see §4 for the evidence actually held |

The 1806 object's own title, as printed by DBNL, is *Evangelische Gezangen, om nevens het Boek der Psalmen bij den openbaren godsdienst in de Nederlandsche Hervormde Gemeenten gebruikt te worden*. The project registry previously recorded a shortened title; corrected to the printed one.

## 2. What the 1806 adaptation actually does

The 1806 hymn is **not a stanza-subset** of the 1676 poem. It is a reworking that recasts the opening and compresses the argument, roughly 2:1.

| 1806 stanza | Opening | Probable 1676 source | Relation |
|---|---|---|---|
| 1 | *Zalig! zalig, niets te wezen, / In ons eigen oog, voor God* | no single stanza; recasts the thesis of XIV (*Foey! Dat ick oyt onbedogt / 't Heyl in eygen voordeel sogt*) with IV.5–8 (`Alle eygen` renounced) | **new composition**, not versification |
| 2 | *Is ons zielverdervend eigen / Nog zoo dikwerf ongezind* | **II** (*het ziel-verdervend Eygen … ongesind / Sig tot 't heylsaam Niet te neygen, / Daar de Ziel maar ruste vindt*) | close reworking; `heylsaam Niet` dropped |
| 3 | *Wat wij hebben, of vermogen* | **V** (*'t Hoort den Hemel alles toe / Wat ick denck, en wat ick doe …*) | close reworking, reordered |
| 4 | *Niets met al, niets zijn wij waardig* | **VII** (*Wy sijn niet dan stof en eerd … Niets, ja niets en sijn wy weerdig*) + **VIII** (*Leent hy ons oyd eenig Goed*) | fusion of two stanzas |
| 5 | *U te danken zijn wij schuldig* | **VIII** (*Des wy Hem te dancken schuldig Sijn …*) + **IX** | fusion |
| 6 | *Vragen wij, wat goed of kwaad is* | **IX–XII** (God's hidden counsel; *Wat Hy doet is even goed*) | compression of four stanzas |
| 7 | *Mag uw naam maar eer ontvangen* | **XII–XIV**, closing by returning to the incipit | compression + new closing frame |

**Consequence for the source chain.** The 1676 stanzas with no counterpart in 1806 are the **autobiographical exile frame**: I (the fatherland, kindred, friends, *soete Slaverny*), III (the light of friendship, the house, *gulde vryheyd*), VI (the primal source and spring), XIII (the lonely seat among the Cherubim), and the *Rees* date line. The adaptation keeps the doctrinal spine and drops the occasional, autobiographical opening. That is a genre move — from an exile poem to a general hymn — and it is the reason the Russian text that follows 1806 cannot also be called a rendering of the 1676 poem.

Confidence in the mapping: **medium-high** for stanzas 2, 3, 4, 7 (near-verbatim parallels); **medium** for 1, 5, 6 (recomposition and fusion). This table is this project's collation of the two printed texts, not a claim taken from a published source.

## 3. The four expressions the notes flag

### 3.1 `zielverdervend eigen` — 1676 and 1806

- 1676, stanza II: *Maar het ziel-verdervend Eygen / Was'er in, end ongesind / Sig tot 't heylsaam Niet te neygen*.
- 1806, stanza 2: *Is ons zielverdervend eigen / Nog zoo dikwerf ongezind, / Om zich tot dien wil te neigen*.

The 2005 apparatus (B1, paraphrased) glosses *Eygen* as the self-directedness that seeks the satisfaction of its own desires rather than God's will, and notes Lodenstein's habit of substantivising adjectives — *eigen* belongs with the English Puritan idiom of **self-**. So the phrase is "soul-destroying own-ness / self-will", a condition, not a possession.

**Translation constraint:** do not render it as "своё" in the neutral sense of "one's own things", and do not import a modern psychological sense of "ego". **Decision status:** `PENDING_OWNER_REVIEW`; the literal gloss is settled, the Russian equivalent is not.

### 3.2 `heylsaam Niet` — 1676 only

1676, stanza II: *'t heylsaam Niet* — "the salutary Nothing". It is the poem's key paradox: the "nothing" is not nihilism but the renunciation that heals. **It does not survive into 1806**, which replaces the clause with *Om zich tot dien wil te neigen*. A Russian text following the 1806 line has no right to the phrase; a text following 1676 must keep the paradox. **Decision status:** `SOURCE_DEPENDENT — decide which form is being followed first`.

### 3.3 `'t Hoort den Hemel alles toe` — 1676 → `Alles hoort den Hemel toe` in 1806

1676, stanza V, opens with the clause; 1806, stanza 3, closes with it. The 1806 line **`Alles hoort den Hemel toe`** is therefore the same proposition in a different position — a real, if small, structural change, and one more reason not to treat the two as interchangeable. Confidence: **high** (both printed texts read).

### 3.4 `Voor 't geloof is alles goed` — the context, and why it must not be flattened

1806, stanza 6, in full:

> *Vragen wij, wat goed of kwaad is. / Voor 't geloof is alles goed; / Al wat d'uitvoer van uw' raad is, / Vader! dat is alles goed: / Altijd goed en wijsheid is 't, / Wat de Wijsheid zelv' beslist.*

The line is **not** a general assurance that everything turns out well for the believer. The stanza's subject is a question — "what is good or evil?" — and its answer is that what is good is **the execution of God's counsel** (*den raad*), which is "always good and wisdom, what Wisdom itself decides". The predication is about God's decree and its outworking, and the following stanza continues in the same register (*'t Ga ons slecht, of 't ga ons goed* — "let it go ill or well with us").

**Translation constraint:** render it as a statement about God's counsel being good, **not** as "для верующего всё хорошо". A rendering that makes it a subjective consolation is a doctrinal change, not a stylistic choice. Confidence: **high** — the printed stanza supplies its own explanation in the next three lines.

**Historical note worth keeping:** in the 1938 hymnal this stanza's first four lines are retained, but its last couplet is replaced by the closing couplet of the 1806 stanza 5 — see §4.

## 4. The 1938 form — five stanzas, and exactly which stanzas went

**Evidence held:** full-text transcriptions of Gezang 205 at <https://www.holyhome.nl/oud_hb/205.html> and <https://www.online-bijbel.nl/gezang/205/>, which agree line for line and are independent of each other; a partial third transcription at <https://zondagsarbeid.blogspot.com/2011/09/nederlandse-hervormde-bundel-1938.html>. These are **web transcriptions, not the printed bundel** — class B1 with limits, not quote-safe for a disputed claim.

**Composition of Gezang 205:**

| 1938 stanza | Content | Relationship to 1806 |
|---|---|---|
| 1 | *Zalig, zalig, niets te wezen…* | = 1806 st. 1, unchanged apart from spelling |
| 2 | *Is ons **trots, hoogmoedig** eigen…* | = 1806 st. 2 with **one word replaced**: `zielverdervend` → `trots, hoogmoedig` |
| 3 | *Wat wij hebben of vermogen … alles hoort de hemel toe* | = 1806 st. 3 |
| 4 | *Vragen wij, wat goed of kwaad is … Gij, o Heer, zo wijs als trouw, / weet best, wat ons schaden zou* | = 1806 st. **6**, lines 1–4, with the closing couplet of 1806 st. **5** appended |
| 5 | *Mag uw naam maar eer ontvangen…* | = 1806 st. 7 |

**Direct answer to the open question: the stanzas omitted in 1938 are 1806 stanzas 4 and 5** —
- st. 4, *Niets met al, niets zijn wij waardig; / Eischt Gij dan uw giften weêr…*, and
- st. 5, *U te danken zijn wij schuldig, / Maar ook, eischt Gij ons iets af…* —

with the **last two lines of st. 5 retained** and used to close the newly built stanza 4. So the reduction is not a clean deletion of two stanzas; it is a deletion plus a graft, which is exactly the kind of detail that a translation claiming to follow "the 1938 version" must reproduce or explicitly refuse.

**Confidence:** **medium-high** on the composition (two agreeing transcriptions); **not verified** against the printed book.

**The 1938 wording change is materially important.** Replacing `zielverdervend eigen` ("soul-destroying own-ness") with `trots, hoogmoedig eigen` ("proud, haughty own-ness") **removes the strongest word in the stanza** and converts a spiritual-diagnostic claim into a moral one. Any Russian text that renders the line as "гордое своё" is following 1938; one that renders "губящее душу своё" is following 1806. This must be decided, not drifted into.

**Next check to close this:** the printed 1938 bundel is available as a scan via Delpher (`Psalmen en gezangen voor den eeredienst der Nederlandsche Hervormde Kerk`, 1938, identifier `MMKB06:000000593`, page image 296 in the retrieved record). Collate Gezang 205 against it and record the page.

## 5. What the music notes are, and are not

The following were decisions discussed for **this composition only**. They are recorded here because they explain the shape of the existing two recordings, and they must **not** be promoted to project-wide defaults.

- Male monastic-style polyphony in a Georgian idiom; powerful organ; epic, majestic character; a strong lead male voice with a supporting ensemble.
- The **defect observed in earlier generations**: the vocal delivery came out excessively slow and whispered.
- Countermeasures considered: **112–120 BPM**, syllabic delivery, short transitions, a short introduction, no long instrumental interludes and no stretched vowels.

Status: `REPORTED_FROM_EARLIER_SESSIONS`, `NOT_CAPTURED`. No style prompt is in this repository for DUTCH-002 — the two verbatim prompts remain `NOT_CAPTURED`. It is **not** established that the 112–120 BPM decision was applied to either existing version; do not describe the existing recordings as meeting it. In particular, a reported duration of 433 s or 438 s for a seven-stanza text is compatible with a slow delivery, but duration alone cannot demonstrate tempo.

The project's general vocal guidance (clear diction, strong and intelligible lead, no default breathiness) now lives in `../SUNO/STYLE_AND_PRODUCTION_RULES.md`; the 112–120 BPM figure stays here, tied to this work.

## 6. Sequence and integrity rules for any future text

1. Follow the stanza order of whichever form is chosen — 1676, 1806 or 1938 — and say which.
2. Do not add lines or refrains. The 1676 poem has **no refrain**; the address pairs sit *inside* the stanza. The 1806 and 1938 forms gain a closing frame by returning to their own incipit, which is a feature of those forms, not a licence to invent one.
3. Keep the antitheses: own-ness vs the salutary nothing; what we have vs what belongs to heaven; God's counsel good vs our circumstances good or ill.
4. Do not present a text that follows 1806 or 1938 as a translation of the 1676 poem.

## Права

| Layer | Position |
|---|---|
| 1676 poem | public domain in substance; `RIGHTS_UNKNOWN` + `RIGHTS_HOLD` retained pending a captured DBNL rights statement |
| 1806 *Evangelische Gezangen* | public domain in substance (1806 imprint); the DBNL transcription is a separate modern object |
| 1938 Hervormde Bundel | **copyright status must be assessed before any use**; the bundel is a 20th-century publication and the transcriptions consulted are third-party web pages. `RIGHTS_UNKNOWN` + `RIGHTS_HOLD`; do not treat the 1938 wording as freely reusable |
| 2005 critical edition | `PERMISSION_REQUIRED` — paraphrase only |

## Следующее проверяемое действие

1. **Collate Gezang 205 against the printed 1938 bundel** (Delpher scan) and record the page; only then can the five-stanza composition be quoted rather than described.
2. Assess rights for the 1938 text and for the third-party transcriptions before using either.
3. Obtain the actual Russian lyric for DUTCH-002 V1 and V2 and record which historical form it follows; the present dossier cannot determine that from the repository.
4. Recover the two verbatim SUNO prompts; until then, the tempo question in §5 stays open.
