# Review log — SUNO_HYMNS project bootstrap

Date: 2026-10-25  
Branch: arena/dutch-hymns-suno-research-20261025  
Base snapshot originally inspected: f38b194a99fdc6cc66b86fcc4c1b217da7e945a0

## Changes identified by the second audit

1. **Two poems called Hert-sterckte in Jehova.** The critical edition distinguishes item 34 (I, dated 28 December 1673 with its own melody directions) and item 35 (II). The current Russian track follows the later Rutgers hymnbook chain for II; I has been added as a separate candidate.
2. **Date emendation for II.** The digital material reads 4 January 1674, but records that the original print erroneously says 1664 and the online colophon records a 1664→1674 correction. The specific date claim now carries EVIDENCE_HOLD until the original page image is checked.
3. **First edition versus critical edition.** The 1676 book is a primary historical witness and DBNL marks the underlying work Auteursrechtvrij; the digital rendering is diplomatic, with omissions and explicit editorial corrections. The 2005 critical edition by Ros and Strengholt is explicitly copyright-protected. The source registry now separates historical evidence class, access state and reproduction rights.
4. **Utrecht Hymni 1615 access layer.** The accessible DBNL item is the 1967 facsimile edited by Jan van Biezen and Marie Veldhuyzen, not an independent direct scan of the 1615 original. The facsimile is copyright-protected.
5. **Revius distinction.** The 1630 first-edition object has not been independently acquired; the exact sonnet page currently used comes from W.A.P. Smit's 1930–1935 scholarly edition. Composition date and original melody remain unverified.
6. **Status hygiene.** Production asset preparation, exact prompt capture, actual metadata readback, rights and public publication are recorded separately.
7. **Broader backlog.** Added directly locatable first-edition candidates with tune directions and a separate discovery queue for the broader Uyt-spanningen contents. Discovery items remain candidates; not all are necessarily hymns or appropriate for a full-length SUNO adaptation.
8. **Machine checks.** Added author, claim and songbook registries plus a read-only cross-reference/state validator. These are project-local tooling; they do not alter root authority or global evidence policy.

## Still open after this commit

- Inspect the actual 1676 page image for the 1664 misprint and resolve the date HOLD only with recorded visual evidence.
- Acquire / inspect the 1630 Revius leaf if a claim requires original punctuation, physical layout or edition variants.
- Recover exact lyric versions and verbatim SUNO prompts from an authoritative record.
- Read actual media metadata and identify the final Revius cover.
- Verify YouTube/Telegram publication URLs before any publication-status change.
- Continue rights review before redistributing a modern critical edition, facsimile, translation or recording.


The follow-up state pass removed source- and book-level EVIDENCE_HOLD where the uncertainty was narrower than the whole object. The 1664→1674 dispute remains on the specific claim CLM-HERT-II-DATE-1674. The DUTCH-001 tune/date and Revius 1630 first-edition claims are marked as needing primary-witness collation where the exact accessed text is a later scholarly edition.

---

# Third pass — 2026-10-25 (branch `arena/0bdf988d-research`)

Continuation of PR #236's lane, merged into the session branch. This pass read the historical witnesses directly instead of relying on the previous summaries.

## 1. Both *Hert-sterckte in Jehova* poems are in the 1676 first edition

Earlier records implied the two poems were known chiefly through the 2005 critical edition (item 34/35) and the 1971 anthology. They stand in the 1676 print itself: **I on pp. 78–81** (15 stanzas, 28 December 1673) and **II on pp. 82–84** (14 stanzas, 4 January 1674). Correction: `DUTCH_HYMN_CATALOG.md` had cited the item-34 page `…_02_01_0039.php` as the source of **II**; the correct item is 35, `…_02_01_0040.php`.

## 2. The relation between the two poems is textual, not merely titular

II has no tune of its own: it prints `Te singen als boven pag.78. Soet Geselschap dat met my, &c.`, and the 2005 apparatus states that the direction refers to the preceding text. The same apparatus cross-references I's line 89 (*In dien Ocean*) for II's opening *daar*. Together with the one-week interval and the shared place, II is a deliberate sequel. It is not a recension of I.

## 3. The date hold is narrowed, not lifted

- The DBNL colophon lists `p. 84: 1664 → 1674`, so the transcription's `1674` is an **emendation**.
- The **1727 ninth edition** independently prints `4 in Loumaand 1674`. This is the only *printed* witness in the project that actually reads 1674, and it was not previously recorded.
- The 1971 anthology prints 1674 and footnotes `Er staat abusievelijk: 1664`.
- The second listed correction, `p. 87: 1664 → 1674`, belongs to item **36**, *'t Verheven Herte* (11 January 1674) — **not** to II. A related correction at p. 7 (`1565 → 1665`) shows a recurring compositor-level digit fault.
- Chronological corroboration: in December 1673 Lodenstein was a French hostage; the group was printed in **1674** as *Meditatien over eenige van 's Heeren Gods Eygenschappen*.

`CLM-HERT-II-DATE-1674` therefore stays on `EVIDENCE_HOLD` — the 1676 leaf has still not been inspected — but the hold now covers only the literal reading of that impression. What is missing and where to look are recorded in the claim's `evidenceGap` / `nextCheck`.

## 4. New candidate researched: `DUTCH-004` — *Den nedrigen christen, Op Psalm 131*

Activated from `DUTCH-CAND-002`. Full text read on printed pp. 74–75 and collated against the 1727 edition; tune pointer resolved to printed p. 29; rights separated by layer; a Russian adaptation draft and a production package prepared. No melody was invented, no composition date inferred, and no generation was attempted.

## 5. Locator defect found and recorded

The numeric slug of a DBNL `lode002uyt_01_01_00NN.php` URL is a **chunk index, not a printed page**: slug `0036` shows pp. 74–75, `0039` shows pp. 82–84, `0084` shows p. 230. The colophon cites printed pages, so reading `p. 84` as `…_0084.php` lands on an unrelated poem. Recorded as `CLM-DBNL-SLUG-TRAP` and in the dossier.

## 6. Validator and CI

- The validator gained: globally unique version IDs; prompt text must be **byte-identical** to the published production package; `claimIds` cross-references with every claim either work-linked or explicitly `projectLevel`; `EVIDENCE_HOLD` must carry `evidenceGap` and `nextCheck`; orphan-source detection; backlog/catalog Markdown must equal the JSON ID sets; `PERMISSION_REQUIRED` must retain `RIGHTS_HOLD`; registries must agree on `asOf`.
- Each new rule was tested by deliberately breaking the data in a scratch copy and confirming a non-zero exit.
- Added `.github/workflows/suno-hymns-registry.yml` — path-scoped to `SUNO_HYMNS/**`, read-only, with an assertion that the validator does not modify the working tree and a duplicate-JSON-key check. It duplicates no existing workflow; no other workflow inspects `SUNO_HYMNS/`.

## Still open after this pass

- Inspect printed p. 84 of the 1676 impression (KB 4 B 1 / UBA 113: BALIE 250.D12 / the DBNL scan bundle) and record the reading.
- Acquire the 1674 *Meditatien* pamphlet and collate its four poems.
- Retry the Nederlandse Liederenbank when it returns online (offline since at least 2026-10-25, HTTP 403).
- Inspect the 1676 page images of pp. 74–75 to close the DUTCH-004 typography `LOCATOR_HOLD`.
- Recover the exact submitted SUNO prompts for DUTCH-001/002/003 — still `NOT_CAPTURED`; nothing was invented here to fill the gap.

# Fourth pass — 2026-10-25 (supplementary brief)

Scope: check the four works against a set of working notes from earlier sessions, without treating those notes as facts. Nothing in this pass changed any Russian lyric, because **no Russian lyric is stored in the repository**.

## 1. The 1806 hymn has seven stanzas, not five

Read in full: *Evangelische Gezangen* (1806), **LXVIII Zelfverloochening**, printed pp. 143–144. Seven numbered stanzas. The "five" figure belongs to the **1938** Hervormde Bundel, Gezang 205. The error is corrected in the track catalog, the source register and the new DUTCH-002 dossier.

## 2. The exact omissions in the 1938 form

Gezang 205 keeps 1806 stanzas 1, 2, 3, 6 and 7; **omits stanzas 4 and 5** (`Niets met al, niets zijn wij waardig…`; `U te danken zijn wij schuldig…`), while keeping the **last couplet of stanza 5** as the close of its own fourth stanza — a deletion plus a graft. It also replaces `zielverdervend eigen` with `trots, hoogmoedig eigen`, weakening a spiritual diagnosis into a moral one. Known only from two agreeing web transcriptions: `EVIDENCE_HOLD` until the printed bundel is collated.

## 3. DUTCH-001 read from the print, and the tune line corrected

The 1676 print, pp. 131–134, gives eight stanzas and the tune line **`Rosemont waar gy vliedt`** (the registry had the critical edition's `waer`). The eight Christological addresses were checked one by one and do differ — which is why a single universal refrain would be an adaptation, not a translation.

## 4. `Heerlijckheyds Loff` identified

A distinct ten-stanza poem, 1676 pp. 155–158, incipit `HOog! om hoog! mijn siel, na boven!`, tune line `Voyse: Un jour &c.`, dated 27 August 1665, item 56. The notes' `Heerlijckheyds Loff / Hoog, omhoog…` was one text, not two: the second element is the incipit. Registered as candidate `DUTCH-CAND-021` — **no work ID, no lyric, no prompt, no track**. The 1938 bundel's *'t Oog omhoog, het hart naar boven!* is a modernised reworking to a Bourgeois melody and must not be quoted as the 1665 poem; note that the 1938 bundel therefore holds **two** different Lodenstein hymns.

## 5. DUTCH-003 confirmed as a sonnet, and the discussed Russian line flagged

The 14-line text was checked line by line: octave of negations, turn at **line 9** with a doubled self-identification, six instruments in the order tree/cross → rope → nail → spear → scourge → bloodied crown, causal close. The discussed Russian turn («…я — виновник мук Твоих») converts an **agentive** claim into a claim of causation; that is a deviation to record if adopted, not an equivalent. The earlier Russian text is **not approved**.

## 6. Statuses separated, and no prompt invented

`SUNO/LYRIC_REGISTER.md` now carries a seven-state table (source text / verified translation / working draft / prompt / generation output / user-approved / unverified history) and states plainly that no work in the catalog has a verified translation. `SUNO/STYLE_AND_PRODUCTION_RULES.md` now carries the eight standing text rules, with a precedence note and a per-work table separating DUTCH-002's 112–120 BPM brief from project defaults.

## 7. Registry and gate

Six sources and eight claims added; candidate `DUTCH-CAND-021` mirrored in the backlog Markdown. `validate_project_registry.py` passes: 44 sources, 3 authors, 4 tracks, 33 claims, 9 songbooks.

## Still open after this pass

- Collate the printed 1938 Hervormde Bundel (Delpher `MMKB06:000000593`) for Gezang 205 and for *'t Oog omhoog*.
- WNT checks for the eight DUTCH-001 expressions; `in 't dorre stickt` and `Geven op de hand` remain low-confidence.
- Locate `heylsaam Niet`: **not present** in the 1806 text checked, so it belongs to the 1676 poem — the 1676 stanza has not been re-read for it in this pass.
- Acquire the 1630 Revius leaf.
- Recover the Russian drafts and the verbatim SUNO prompts for DUTCH-001/002/003.

# Fifth pass — 2026-10-25 (closing the evidence gaps that the fourth pass left)

Scope: take the four items the fourth-pass audit listed as "still open" and see which were actually reachable. Two closed, one moved, two are now documented dead ends with the reason.

## 1. `heylsaam Niet` — found

The phrase is in the **1676** poem, stanza **II, line 5** (`Sig tot 't heylsaam Niet te neygen`), read in full this pass at printed pp. 82–84. It is **not** in the 1806 hymn, which replaces the clause with `Om zich tot dien wil te neigen`. The open question is closed, and the phrase must never be quoted as 1806 wording.

The same reading turned up a related fact: the poem qualifies its "Nothing" three different ways — `heylsaam Niet` (II), `'t eyndeloos Niet` (IV), `'t grondloos Niet` (VIII). None is nihilism, and no translation should reduce them to one word.

## 2. Gezang 205 (1938) — collated against the printed book

The printed bundel was reached through Delpher page images (`MMKB06:000000593`, image pp. 724–725). Result: the five-stanza count and the composition are **print-verified**, and two fourth-pass details needed correcting.

- The stanza-2 change is a **pair**: `zielverdervend` → `trots, hoogmoedig` in line 1 **and** `Werp die trotsheid dan` → `werp dien hoogmoed dan` in line 5. The word for pride moves out of the prayer into the diagnosis.
- The couplet closing the 1938 fourth stanza is 1806 **stanza 5, lines 5–6**, grafted onto 1806 **stanza 6, lines 1–4**. It replaces 1806's own couplet, which asserted that what God decides *is* wisdom. The 1938 couplet asserts that God knows what would harm us. **The two hymnals therefore explain `Voor 't geloof is alles goed` differently** — decree in 1806, providence in 1938.
- Printed credits: melody `Johann Christoph Bach (1642—1703)`, text `Jodocus van Lodenstein … Bewerking van Abraham Rutgers (1751—1809)`. The Rutgers chain is now attested at the 1938 end too, and the 1938 tune is not the 1674 tune.
- **Rights:** Delpher marks the object *"Auteursrechtelijk beschermd"*. The 1938 bundel is protected, whatever the status of the 1676 poem.

New file: `COLLATION_GEZANG205_THREE_WAY.md`. Remaining gap: **stanza 1** of Gezang 205 was dropped by the page OCR and still rests on web transcriptions.

## 3. DUTCH-001 lexis — narrowed on internal evidence, still not dictionary-verified

`in 't dorre stickt` rhymes with `verquickt`, and the etymological record makes the "smother" sense of *stikken* the same word as *stikken* "to stitch", an intensivum of *steken*, glossed *"blijven steken, niet verder kunnen"*. The narrowed gloss is **stuck fast, choked, in the dry**. Confidence rises from low to medium; the status stays `PENDING_LEXICAL_CHECK`.

The WNT itself was **not** consultable: the Geïntegreerde Taalbank serves only a JavaScript shell, and Ensie's Van Dale 1898 is paywalled. Both are recorded as sources with their access limits, so no future pass can mistake an attempt for a lookup.

## 4. Two dead ends, now documented

- **Revius 1630.** DBNL's title record for the 1630 collection lists only the 1930–35 Smit edition as an *edition*; there is no transcription of the 1630 print. The leaf is still `NOT_ACQUIRED`.
- **`'t Oog omhoog` in the 1938 bundel.** Not located. What was established is the mechanism: the bundel prints the composer above an item and the author below (Gezang 204: `Louis Bourgeois` above, `Johannes Helder` below), which is how a 16th-century tune name attaches to a 20th-century item. The Bourgeois claim therefore stays `SUPPORTED_BY_SECONDARY_SOURCE_NEEDS_COLLATION`.

## 5. Registry and gate

Five sources and two claims added; four claims revised. `validate_project_registry.py` passes: **49 sources, 3 authors, 4 tracks, 35 claims, 9 songbooks**.

## Still open after this pass

- 1938 stanza 1 (page image, not OCR).
- The 1630 Revius leaf.
- WNT for the eight DUTCH-001 expressions and `wilt gy my`.
- Printed p. 84 of the 1676 impression (the 1674 hold).
- `'t Oog omhoog` in the 1938 bundel.
- The Russian drafts and verbatim SUNO prompts — unchanged, still absent.

# Sixth pass — 2026-10-25 (DUTCH-005: *Heerlijckheyds Loff* activated and packaged)

The owner asked for the Dutch hymn with SUNO styles "that we haven't done yet" — the text identified in the fourth pass as *Heerlijckheyds Loff* and left as a candidate. It is now a work.

## 1. Activation, with the catalog checked first

`DUTCH-CAND-021` → **`DUTCH-005`**. No duplicate was created: the research record stays in `CANDIDATE_DUTCH-CAND-021_HEERLIJCKHEYDS_LOFF.md`, and the production record is new. The two claims about this text had been `projectLevel` because no work existed; they now hang off the work, and the flag was removed rather than left as a lie.

## 2. The whole text read, and its shape recorded

All ten stanzas of the 1676 print (pp. 155–158) were read. Structure: four statement lines, a call line and its abbreviated repeat (`etc.` — a repeat instruction, not a lacuna), the tripled word with its object, the call again, a closing line. Stanza I is printed in full and is the metrical model for III–X. The tripled word moves **`leven` (III–VI) → `lieven` (VII–IX) → `loven` (X)** — the poem's architecture, inside the stanzas, not a chorus.

**Still not print-verified:** the page images have not been inspected, and the illustration `ill0155` has not been viewed.

## 3. What was authored, and what was deliberately not

Authored: a literal gloss, a Russian **adaptation** draft v0.1, an eight-row deviation table, a per-work musical brief, and two style directions.

Not authored: any claim that the Russian is a translation; any claim about the melody; any claim about the illustration; any generated audio; any publication. `PROMPT-DUTCH-005-V1` is `AUTHORED_NOT_YET_SUBMITTED`.

**Two uncertainties kept visible instead of smoothed:** I.7 has no expressed negation in the Dutch (elliptical reading adopted, the "costly" pun recorded as a secondary sense), and the tripled device is rendered with a noun in III–IX but an infinitive in X, where Dutch triples infinitives throughout.

## 4. Registry and gate

Three claims added; candidate activated; work added to the track catalog with `workType: DEVOTIONAL_SONG_WITH_TUNE_DIRECTION` and production state `LYRIC_DRAFT`. `validate_project_registry.py` passes: **49 sources, 3 authors, 5 tracks, 38 claims, 9 songbooks**.

## Still open on DUTCH-005

- Owner poetic revision of the Russian draft.
- The 1676 page images of pp. 155–158, and the illustration.
- Choice between the two style directions.
- The Dutch Song Database for *Un jour &c.* — no melody claim until then.

# Seventh pass — 2026-10-25 (artifact separation, lyric revision v0.2)

The owner pointed out that the delivery had mixed lyrics and style into one sheet, against the project's own rule.

## 1. The rule that was broken, quoted

`SUNO/README.md`: *"Keep these artifacts separate: source-language historical text; normalized transcription text; literal translation for analysis; Russian literary adaptation; SUNO-ready lyric with vocal cues and optional stress marks; published/recorded take."*
`SUNO/LYRIC_REGISTER.md`: *"Keep clean public lyric and pronunciation-marked SUNO lyric separate."*

One file holding Dutch text, gloss, Russian lyric, tags and style prompts is exactly what those two lines forbid.

## 2. What replaced it

`DUTCH-005_LYRIC_AND_STYLE_SHEET.md` is **deleted**. In its place, three files, each with one job:

| File | Contains | Does not contain |
|---|---|---|
| `SUNO/DUTCH-005_LYRICS.md` | clean Russian lyric, v0.2, changelog, rhyme/metre statement | tags, prompts, gloss |
| `SUNO/DUTCH-005_LYRICS_SUNO.md` | the same wording with section labels and the minimum stress marks | prompt text, analysis |
| `SUNO/DUTCH-005_STYLE.md` | style prompts only, primary + one option | any lyric |

The Dutch text and the literal gloss stay in the production package §2–§3, where the research lane expects them.

## 3. The lyric itself revised to v0.2

Nine changes, each with a reason in the lyric file's changelog: the stanza-1 clause restored as one sentence; the stanza-2 close given the right subject (`Сердце ставит выше всего` — the Dutch subject is the blood); stanza 3's vocative and `onsigtbaerlijck` restored; stanza 6's participle calque replaced and the call repeated in full rather than half; stanza 8's line shortened; stanza 9's false friend `обаяния` replaced by `отрада`; stanza 10's plural/singular address corrected.

**Rhyme is declared, not faked:** the Dutch rhymes its thrice-repeated call line with the closing line in all eight stanzas that use the device. The Russian reproduces the **device** everywhere and the **rhyme pair** only in stanzas 1, 2 and 10, leaving the rest unrhymed rather than filling them with words the Dutch does not have.

## 4. Registry

`DUTCH-005-RU-v0.2` with three `lyricFiles` paths; the claims ledger states why the artifacts are separate and quotes the rule. Validator passes: **49 sources, 3 authors, 5 tracks, 38 claims, 9 songbooks**.

# Eighth pass — 2026-10-25 (review response: tags, metre, diction, two-printing collation)

The owner reviewed the delivery and found six defects. Five were real and are fixed; one is a process failure that this pass records rather than argues about.

## 1. The delivered block was not Suno-ready

The lyric was shown with stanza numbers `1`–`10` and no structural tags. Numbers are editorial, not performance structure, and a model may read them as text. `SUNO/DUTCH-005_LYRICS_SUNO.md` now carries `[Intro]`, `[Verse 1]`…`[Verse 10]`, `[Outro]`, with three deliberate accents: verse 7 (lead alone, organ thins — the poem's turn), verse 8 (choir rejoins, building), verse 10 (full choir, one inline echo). **No `[Chorus]`** — the source has no refrain, and its repetitions are already inside the stanzas.

## 2. The metre claim was false

v0.2 asserted "7–8 syllables" while containing lines of 11, 12 and 13. The claim is withdrawn. Actual counts are now tabulated per stanza: statement 6–10, call 6–9, tripled 9–11, close 7–9. The honest conclusion is stated: that is sufficient for **syllabic declamation**, not for a fixed melodic setting, and a strictly metrical version would be a separate, larger revision.

## 3. Seven lines rewired

Stanzas 1, 2, 3, 6, 7, 8, 9 and 10 changed, each with a reason in the lyric's changelog: the invented "свет" removed; the blood restored as the subject in stanza 2; the vocative unambiguously marked in stanza 3; the sentence no longer broken across lines in stanza 6 and `в лоне` (comic in Russian) replaced; the subject of «готовая / находит» made explicit in stanza 7; `если что любить` replaced by `коль что любить` in 8 and 9; `кто здесь прах` given a parsable predicate in 10.

## 4. The style asked for the wrong voice

`one strong low male lead` became `one clear tenor-baritone lead`, with `no melisma, no stretched vowels, strictly syllabic, one syllable per note`, `short two-bar organ introduction`, `all ten verses sung in order with no cuts`, and prohibitions on a husky or excessively low lead and on long instrumental interludes. Tempo 116 → 118.

## 5. The source text is now collated across two printings

`Heerlyckheyds Loff` was fetched from the **1727 ninth edition**, which prints it at **the same pages 155–158** with the same title, tune line, stanza count and date. Four variants were found and recorded (`CLM-DUTCH-005-VARIANTS`), including the resolution of the `dat`/`dan` question at VII.8 in favour of `dan`.

## 6. The process failure

The `DUTCH-005` ID was assigned in the same pass that resolved the identity, on the strength of a transcription. That is what the record now states in `identityStatus: CONFIRMED_BY_TWO_PRINTINGS_TYPOGRAPHY_UNVERIFIED`, with the note that the ID was assigned before any page image was checked. **A green validator proves none of this**; it proves only that the repository's cross-references are consistent.

## 7. Validator

Extended so that a prompt may live in a dedicated style document: `version.promptDocuments` is now accepted, and the prompt must appear verbatim in at least one listed document. This follows the artifact split the lane already required; it does not weaken the drift check.

`validate_project_registry.py` passes: **50 sources, 3 authors, 5 tracks, 39 claims, 9 songbooks**.

# Ninth pass — 2026-10-25 (delivery format and five styles)

Two owner requirements, both now rules rather than habits of one work.

## 1. The header line

`SUNO/README.md` now specifies a **single line**, title first, author second, no labels:

```
«Слава Господня» — Йодокус ван Лоденстейн
```

The earlier wording of the rule (separate `Название:` and `Автор:` rows) was replaced, because the owner prefers the one-line form. The historical title, the source and the status follow underneath — never above.

## 2. Five style directions per work

`SUNO/STYLE_AND_PRODUCTION_RULES.md` now requires **five genuinely distinct directions**, not one, with a shared floor: syllabic declamation, one syllable per note, no melisma, no stretched vowels, intelligible lead, all stanzas in order, no invented chorus, short intro. Instrumentarium, region and era of the idiom, tempo, metre and the point of ensemble entry are free to differ.

`DUTCH-005_STYLE.md` was rewritten accordingly: A epic organ + Georgian monastic choir (118, D minor); B Renaissance wind consort — cornetto, sackbuts, shawm — with four male voices (112, D dorian); C viol consort + chamber organ + solo tenor, ensemble growing verse by verse (100, G minor); D Byzantine-style ison under a baritone cantor (free); E metrical chorale, unison male voices and organ (126, A minor). Each carries an exclude list, a purpose and its risk; the comparison table states completeness risk per direction, D highest and E lowest.

**A holds the primary slot only because the registry must carry one `promptText`.** No direction is preferred, and the choice is recorded as an open check.

## 3. Registry

`styleVariants` (five IDs) added to `DUTCH-005-RU-v0.3`, with a note that the primary slot is a registry necessity, not a preference. Validator passes: **50 sources, 3 authors, 5 tracks, 39 claims, 9 songbooks**.

# Tenth pass — 2026-10-25 (stanza 8, lines 3–4: "куда уйдёт?")

The owner asked where the beauty "goes". It goes nowhere: the Dutch verb is `verdwijnt`, **vanishes**, and there is no destination in it. The Russian `уйдёт` in v0.3 imported one.

Two defects in one line, both fixed in v0.4:

1. **Direction invented.** `уйдёт` → `пропадёт` (ceases to be, is gone), with no "where".
2. **Consequence invented.** The Dutch pairs two alternatives — `Min vermaackt, **of oyt** verdwijnt`, "pleases less **or ever** vanishes". v0.3 made the second a result of the first ("меньше радует — и уйдёт"). v0.4 restores the disjunction: `Меньше радует иль пропадёт`.

A third thing is now recorded as an **interpretation, not a settled reading**: the antecedent of `Die`. It may agree grammatically with `Schoonheyd` itself, which would make the addressed Beauty capable of vanishing — contradicting stanza IX and the poem's argument. The earthly-beauties reading is adopted for that reason and flagged as a choice.

Verse 8 in both lyric files, the changelog, the measured syllable table (line 4: 8 → 9) and `DUTCH-005-RU-v0.4` in the registry were updated together. Validator re-run.

# Eleventh pass — 2026-10-25 (full re-read of all ten stanzas; stress)

The owner asked for the whole text to be re-read line by line, not for reassurance, and reported two words the model had stressed wrongly: **драго́е** sung as *дра́гое*, **тре́пета** sung as *трепе́та*. Both were written correctly and unmarked — which is the defect: an unmarked word is a word the model guesses.

## 1. What was wrong in the wording

Twelve defects in v0.4, all in lines I had already passed:

- **I.4** — `maar` dropped: "there where one sees Jesus" instead of "**only** there". The stanza's whole argument rides on that word.
- **I.7** — the line could be read as a claim about ownership ("this is not your life") rather than about direction. Rewritten.
- **II.3** — **an image that was not in the text.** v0.4 read «как туман», a fog. The Dutch is `Lusten met 't gebruyck verdwijnen`: pleasures vanish *with the use of them*. Fog is mine, not Lodenstein's.
- **IV.5** — the vocative was lost (`O! yd'le siel`): «О, праздная» addressed nobody in particular.
- **IV.9** — `goedig schenckt` is "kindly bestows", not "grants mercy".
- **V.1** — «Жизнь добродетелей святых» said "the life **of the saints'** virtues": a possessive the Dutch does not have, plus saints who are not in the line.
- **VI.1** — singular relative with plural verb; `не знаете` had no agreeing subject.
- **VI.9** — "to begin virtue" is not Russian and loses `het deugdsaam leven`.
- **VII.1** — a comma split a single predicate.
- **VIII.2–4** — `wat hier schoon schijnt` = what **seems** beautiful here; the old line asserted beauty and left `Die` without a Russian antecedent.
- **X.5** — `mond` is the mouth, not speech.
- **X.8** — `кто` cannot refer to dust; `hier is stoff` needs `что`.

## 2. Pronunciation — two rules, not one, and both written down (pass 12)

The owner's correction after the over-marking: don't mark everything, do write **ё** everywhere it belongs, and do put stress on the words grammar actually makes hard — while remembering that a sung stress may move for the sake of a rhyme.

The mistake in pass 11 was treating "stress" as one problem. It is two:

1. **ё is orthography.** `всё`, `ещё`, `её`, `моё`, `нём`, `даёт`, `крадёт`, `пропадёт`, `пойдёт`, `живёт` — always written, never optional, in both lyric files and in prose. `все` (plural), `свет`, `Его` keep `е` and must not be "improved". A ё-word never gets an accent as well: the letter already carries the stress.
2. **A stress mark is a hint for the model**, and hints are rationed. It goes on a word when the same spelling can carry two stresses (`сто́ит`/`стои́т`), when the form's stress is not where a model defaults (imperatives, short participles on the ending, `-у́ет` verbs), when the word is long or compound, when it is a biblical name, or when it has been heard sung wrong. It does **not** go on monosyllables, ё-words or plain unambiguous polysyllables — and if the list passes about a dozen words it has stopped being selective.

Both rules are now in `STYLE_AND_PRODUCTION_RULES.md` § Pronunciation marks and summarised in `SUNO/README.md`, with the over-marking recorded as a rejected practice and the reason: an accent changes the text the model reads and can cost its delivery.

**Sung stress versus dictionary stress** is written down as its own rule, because it is real: rhyme and metre can move a stress legitimately, and the sung form then wins — recorded, not "corrected". What is not legitimate is a stress nothing in the stanza explains; that is a defect.

Applied to this text: **six** marks — `драго́е`, `тре́пета` (heard wrong), `сто́ит`, `помы́сли`, `соединена́`, `дару́ет` (rule). A rhyme check found nothing here that needs a shifted stress; `суета`/`тщета` and `хвалы` already fall where they should.

New mechanical check, `scripts/check_ru_lyric.py`: it lists every occurrence of a word that must carry ё in context (including `все`/`всё`, decided per line) and fails a file carrying more than a dozen accented words, so neither failure mode — lost ё, blanket marking — can come back unnoticed. Result on this text: 6 accented words; the only ё question is `все языки` (10.1), which is the correct plural.

`ё` audit of the whole lyric: no missing ё found; `всё`, `моё`, `Нём`, `даёт`, `крадёт`, `пропадёт`, `пойдёт`, `живёт` all printed with the dots.

## 3. Metre, re-counted

The syllable table was re-measured by machine rather than by eye and corrected in four places (V.1 11 → 10, V.2 6 → 5, VIII.1 8 → 9, X's close 8 → 11). Ranges as measured: statement 5–10, call 6–9, tripled 9–11, close 6–11. **No regular metre is claimed**; two short lines and one long line are declared with their reasons.

## 4. Registry

`DUTCH-005-RU-v0.5`; `lyricRevisionNote`, `researchViews.note`, `DUTCH_HYMN_CATALOG.md`, `PROMPT_AND_VERSION_REGISTER.md`, `STATUS_LEDGER.md`, `LYRIC_REGISTER.md` and `DUTCH-005_PRODUCTION_PACKAGE.md` (v0.5, deviations D-09…D-12) updated together. Two of those files still said v0.2 and v0.3 — stale, now fixed. Validator: **50 sources, 3 authors, 5 tracks, 39 claims, 9 songbooks**.
# Thirteenth pass — 2026-10-25 (a second review, checked against the print)

A review arrived with five "bugs", three of them called critical. The Dutch text was re-fetched from DBNL (1676, pp. 155–158) before anything was accepted, and that decided it: **three claims are wrong, five changes are right.** Both halves are recorded, because a rejected claim that keeps coming back is a liability.

## Accepted (v0.6)

1. **IX.5–9 — the anaphora was my error, and a serious one.** The Dutch is `Dit steelt mijn hert en al`. Russian «Всё это» points back at the earthly pleasures listed two lines above, so the stanza ended with loving the shadows above all. `Dit` points at the Beauty those pleasures are "but a shadow of". Fixed by direct address: «Ты моё сердце крадёшь… Тебя превыше всех люблю» — the same «Ты» stanza 8 used.
2. **VI.4 — «не расстались» was wrong.** `cleeft` = cleaves, sticks fast; `расстаться` = part from one another. Now «Доселе не отступили?».
3. **X.8 — `hier is stoff` is "here is matter", not "here is dust".** `stof` = material, as in `stof tot klagen`; the couplet rhymes `stoff`/`loff`. Now «Воспряньте все: есть предмет хвалы» — which also removes a plural imperative over a singular subject.
4. **IV.5–8 — `ydel` echoes the poem's own `Ydelheyd`** (stanza 2, «суета»). «Суетная душа, помысли» keeps the echo; «праздная» was the other legitimate reading and is recorded.
5. **VIII.2–4 — the clause had lost «здесь» and its anchor.** `wat hier schoon schijnt` = what seems beautiful **here**; the clause now runs straight on from «красы».

Two smaller ones: **I.7** «не в том» instead of «не о том» (the Russian for "does not consist in that"), and **II.2** «Всё, что драго» for «Всё драгое» — which removes the word that needed a stress mark. A word propped up by an accent is usually the wrong word, so the mark went with it. Marks are now five.

## Rejected — with the printed text in hand

1. **"Stanza 8 lost a negation; `noch` = neither… nor."** The print reads `Die door jaren, nog gewoonheyd / Min vermaackt, of oyt verdwijnt` — `nog`, not `noch`, with an affirmative verb and no negative anywhere in the clause. The proposed Russian «не померкнет, не пройдёт» inserts a negation the book does not have. **The claim would rewrite the poem to save an interpretation.**
2. **"`Die` is the heavenly Beauty."** The stanza adores that Beauty (`U, Schoonheyd, bid ick aan`); a clause saying it fades would contradict stanza 9. `Die` reaches back to `wat hier schoon schijnt` — the earthly things that merely seem beautiful.
3. **"The person shift in stanza 6 is a Russian bug."** It is in the Dutch: `Hersenlosen, die de snooden / Sonden doet, en daar in leeft` (plural noun, singular relative) then `Weet gy niet` (second person). The Russian mirrors it and the mirroring is recorded.
4. **Style, not text:** `Cijter` stays «цитра» (a cither, not a Greek lyre); `wakkerheyd` stays «бодрость»; «чуть вкусил» stays, because `Lusten met 't gebruyck verdwijnen` is exactly "pleasures vanish with the using".

## Title

`Heerlijckheyds Loff` is «Хвала славе» — `Loff` is praise. The working title «Слава Господня» drops "praise" and adds "Господня". Recorded, not renamed: the title is the owner's, and it is already the heading of every delivery and every record.

## Checks

Both lyric files: 90 lines, identical once the tags, the echo and the five accents are stripped. `check_ru_lyric.py`: 5 accented words, one ё question (`все языки`, 10.1, correct plural). Metre re-counted by machine and corrected in three cells. Validator: **50 sources, 3 authors, 5 tracks, 39 claims, 9 songbooks**.
# Fourteenth pass — 2026-10-25 (rhyme, standard B)

The owner asked for rhyme "as in the original" and chose **standard B**: lines 2 & 4 rhyme, the closing line rhymes with the call line, lines 1 & 3 free. The Dutch scheme and its cost were analysed first (`RHYME_PLAN_DUTCH-005.md`); this pass applies it.

## Result

**Six of ten stanzas carry the cadence rhyme; four do not.** Named, not patched:

- **met:** 1 (нет/свет · прах/прах), 2 (суета/тщета · кровь/любовь), 3 (невзгод/вперёд · око/высоко), 5 (Господней/Господней · соединена/сполна), 7 (отрада/услада · туда/навсегда).
- **half:** 8 (мнится/возвратится, but the close does not answer «поклоняюсь»), 10 (root rhyme хвалы/хвалу, as the Dutch has `stoff`/`loff`).
- **not met:** 4, 6, 9.

Why the four fail: the Russian call lines end on `помысли`, `вы`, `крадёшь`, `поклоняюсь` — words with no rhyme inside these stanzas. Buying one would mean rewriting the call itself, and the call is the poem's fixed device, sung three times per stanza.

## What it cost

Thirteen lines changed for rhyme, each listed with its price in `DUTCH-005_LYRICS.md`. The four most expensive: st.1 «зрят» → «свет» (`siet` is "sees"); st.1 `op aard` → «прах»; st.8's two alternatives (`Min vermaackt, of oyt verdwijnt` — pleases less **or** vanishes) fused into one process, «Слабеет и не возвратится»; st.5 «в святости Его» → «в святости Господней» (the possessive `sijn` is lost).

Three lines fell to five syllables (1.5, 1.6, 3.4). Recorded with the warning: if the tune cannot take a five-syllable line, give up the rhyme at that cadence, not the words.

**One mark disappeared for the right reason:** `дару́ет` left both stanzas' closes («даёт» / «даёт сполна»), so its accent went with the word. Marks: four.

## Also checked, from the third review that arrived the same day

- The 1676 contents were read: `Heerlijckheyds Loff.` (this work) and `'s Heeren Heerlijckheyts Loff.` (a different poem in the appendix). The claim "our hymn is № 56" is wrong — file `0056` is `Schepselen Niet en Iesus Al`, i.e. **DUTCH-001**. The warning about the title collision is right; the numbers attached to it are not.
- The `noch`-negation claim returned a third time and is still contradicted by the print: `nog`, affirmative verb, no negation in the clause.
- Metric defects in the version offered for adoption: VIII.2 twelve syllables, VIII.4 fifteen, IX.5 twelve, X.1 eleven, VI.7 twelve. Not adoptable under strict syllabic singing.

Validator: **50 sources, 3 authors, 5 tracks, 39 claims, 9 songbooks**.
# Fifteenth pass — 2026-10-25 (the "gold" pass: syntax review over the rhymed text)

A long review arrived aimed at v0.5 — it could not reach the repository, so it critiqued a text three revisions old. Eight points still applied to v0.7 and were taken. Four were rejected, one of them because the review contradicts itself.

## Taken

1. **IV — `yd'le` as transitory, not idle.** «Суетная» → «О бренная душа». The review reports the 2005 commentary glossing `ijdel` as *vergankelijk*. Recorded as a **lead**: that page has not been read here, and this reviewer's other Dutch claims have twice been wrong.
2. **VI — plural sins.** `de snooden sonden` is plural; «в грехе… творя его» flattened it. Now «в грехах живут, / Творя их».
3. **VI — the closing line.** «Начните жизнь добродетели» was a word-for-word calque of `het deugdsaam leven`. Now «Начните жизнь добродетельную».
4. **VII — `alleen`.** «Одна находит» could be read as "she" or as "one love". Now «В Нём одном находит усладу».
5. **IX — `menschen seden` plural.** «Любовь людская, людские нравы».
6. **IX — the missing `van`.** «Всё это — только тень её»: the shadow is *of* something.
7. **X — `Singt` is plural.** «Пой без конца» → «Пойте вовек».
8. **Tag hygiene.** Ten descriptive tags compete with the text for the model's attention; three structural ones do the work.

## Rolled back

**Stanza 2's close.** v0.7 read «Сердцу всех выше — кровь и любовь», bought for the rhyme with «кровь». «любовь» is not in that line of the Dutch (`'t Hert boven alles gelden doet`), and the rhyme had cost the sense. Back to «Сердцу цену даёт выше всех», and stanza 2 leaves the rhyme column. **That is the right direction of trade: rhyme may cost a word, not a meaning.**

## Rejected

1. **"Stanza 8 must be rebuilt; the Beauty is said to fade."** The review retracts this in the same document and lands on the reading v0.7 already used: `Die` = `wat hier schoon schijnt`, the earthly seeming-beauties. The print has no negation (`nog`, affirmative `Min vermaackt`).
2. **"`Жизнь добродетелей` mistranslates `der deugden leven`."** It is a correct rendering of the genitive plural. The error was in the *closing* line, and that is fixed.
3. **"`Где Иисуса любить` needs a finite verb."** The Dutch triples an infinitive (`lieven`), and the tripled word is an infinitive in 7–10. A finite verb in one stanza would break the device. The dash went instead.
4. **"Remove the echo `(хвалить)`."** Kept and flagged: one added repetition where the Dutch has three. If a take shows it is unnecessary, it goes.

## State

`DUTCH-005-RU v0.8`. Rhyme: four stanzas met, three half, three not met. Stress marks: four. Both lyric files 90 lines, identical apart from tags, the echo and the accents. Validator: **50 sources, 3 authors, 5 tracks, 39 claims, 9 songbooks**.

# Sixteenth pass — 2026-10-25 (title)

The owner chose the title: **«Хвала Славе»**. Recorded here because the fourteenth pass had left it open, and because the earlier note ("recorded, not renamed: the title is the owner's") is now spent.

Evidence, unchanged from the thirteenth pass: `Loff` = praise, `Heerlijckheyds` = genitive of `heerlijckheyd`, and the poem names the pair itself — `Iesus lof en Heerlijckheyd` (10.4), `Singt sonder eynden Iesus loff` (10.9). «Слава Господня» failed on two counts: it dropped the praise and imported a `Heere` that the Dutch title does not have; it also sat closer to the *other* hymn, `'s Heeren Heerlijckheyts Loff`.

Capitalisation «Славе» is the owner's spelling, kept as given.

Propagated: both lyric files, the style file, `SUNO/README.md` (delivery-header example), `STATUS_LEDGER.md`, `DUTCH_HYMN_CATALOG`, `track-catalog-v1.json` (`displayTitle` = «Хвала Славе», `displayTitleStatus` = `OWNER_APPROVED_TITLE`), transcription, package header. No wording changed; no rhyme, metre or stress count changed. Four marks, 90 lines, validator green.

# Seventeenth pass — 2026-10-25 (owner's question on stanza 1)

**Question:** «4 раза прах — так в оригинале или это ты придумал?» **Answer: the pattern is the print's, the word and the count are mine.**

The 1676 stanza I closes lines 5, 6 and 8 with `op aard` — "on earth" — and ends line 9 with a **different** word, `niet waard` — "not worth". Three repetitions, then a turn; the rhyme is `aard` / `waard`.

The Russian has «прах» in all four slots. So:

1. `aard` is *earth*, not *dust*; «прах» is my substitution in the biblical register, defensible but not the word.
2. The fourth «прах» was bought by the rhyme — the same transaction as stanza 2's «любовь», which v0.8 rolled back. It softens the stanza's last line from a turn into a repetition, and «прах» starts to behave like a refrain, which the source does not have.

Recorded in `DUTCH-005_LYRICS.md` § Stanza 1 with both versions printed, and the v0.7 rhyme-cost table restored (the v0.8 rewrite had dropped it). **Text not changed:** the decision is the owner's, and the consistency argument (stanza 2 already rolled back for the same reason) cuts both ways until they choose.

# Eighteenth pass — 2026-10-25 (retrospective: errors and guards)

At the owner's request, the session's failures were written up rather than left in the chat: `RESEARCH/LESSONS_AND_GUARDS.md`, with the editorial half also written into `SUNO/STYLE_AND_PRODUCTION_RULES.md` § Failure guards and a preflight pointer added to `HANDOFF_FOR_NEXT_AGENT.md`.

**The single most useful outcome is a new CI gate.** `scripts/check_revision_consistency.py` compares prose to files, and on its first run it caught three defects that had survived every previous pass in this session:

1. `DUTCH-005_PRODUCTION_PACKAGE.md` claimed **five stress marks** and listed `дару́ет`, a word that had left the text two revisions earlier. Now four, and the list matches the file.
2. The same package's status table said **v0.3** while the text was v0.8.
3. A sentence appeared twice in a row — an edit applied twice.

Structural validation could not see any of them: it proves ids, states and prompt identity, not that the prose still describes the text. Wired into `.github/workflows/suno-hymns-registry.yml` after the registry step; read-only, and covered by the workflow's existing "the validator modified the working tree" assertion.

Also recorded: the "battle" definition in `ASSET_MANIFEST.md` (one generation = two candidates), and the DUTCH-005 cover direction with its ten rejected rounds, so the look is not regenerated from scratch.

**Not claimed:** these guards prevent nothing by themselves. Two of the session's worst errors — the rhyme bought with «любовь» and the fourth «прах» — were editorial, and the only thing that caught them was the owner reading the text.

# Nineteenth pass — 2026-10-25 (owner's decision on stanza 1)

**Decision:** «Сердца твоего не стоит прах» → «Сердца твоего не стоит». The fourth «прах» removed; the first three kept.

That is exactly the shape the print has: `op aard` three times (5, 6, 8) and a close on a different word (`niet waard`, "not worth"). It also ends the inconsistency I had shipped in v0.8 — stanza 2 rolled back the same purchase, stanza 1 kept it.

**Consequences, all applied:**

- `DUTCH-005-RU v0.9`; changelog row added; stanza-1 section rewritten from "pending" to "decided".
- Rhyme table: stanza 1 met → **half** (`нет` / `свет` survives; «прах» no longer answers the close). Tally **three met, four half, three not met**.
- Metre: stanza 1 close 9 → **8** syllables; row is `6 · 6 · 6 · 8 | 5 | 9 | 8`.
- Cost table: the 1.9 row marked **reverted in v0.9**, like the stanza 2 row.
- SUNO twin updated; 90/90 lines still identical apart from tags, the echo and four marks; `check_ru_lyric.py` 0 accents in the clean file, 4 in the SUNO file.
- Registers, package, catalog `versionId` and revision note bumped to v0.9.
- `LESSONS_AND_GUARDS.md`: the stanza-1 open defect is closed, with the note that what settled it was a decision rather than an argument.

**Not decided, still open:** stanzas 2, 8 and 10 sit at half; 4, 6 and 9 fail; five stanzas still carry calque-shaped openings; no cover approved; nothing generated.

# Twentieth pass — 2026-10-25 (YouTube description, 50+ source run, and two corrections to my own record)

Work done: [`../SUNO/DUTCH-005_YOUTUBE.md`](../SUNO/DUTCH-005_YOUTUBE.md) — title options, description (4229 chars, channel markup `*bold*` / `_italic_`), pinned comment, tags; [`DUTCH-005_SOURCE_RUN_50PLUS.md`](DUTCH-005_SOURCE_RUN_50PLUS.md) — 75 addresses with per-link status.

**The important part is not the description.** Reading the commentary of the 2005 edition (DBNL, pp. 263–267) settled three glosses, and two of them go against my own earlier entries:

1. **`der deugden leven` = *het deugdzame leven*.** The reviewer whom I overruled in pass 15 was **right**; my rejection was wrong. The Russian line «Начните жизнь добродетельную» (fixed for other reasons) now has the gloss behind it; the tripled word «Жизнь добродетелей» does not, and is listed as open.
2. **`yd'le` = *vergankelijke*.** «О бренная душа» is confirmed. It had stood in the package as a *lead*, from a reviewer I did not trust; it is now a *check*.
3. **`Na dit leven crijgelijck` = the life *to be obtained after this life*.** So the Russian «После земных невзгод» (stanza 3, line 2) is **wrong in sense**, not merely flat: there are no "hardships" in the Dutch. This one is a defect in the shipped text and goes to v0.10.

Also confirmed: `goedig` = goedertieren, `Hersenlosen` = verstandelozen/dwazen, `snooden` = verlelijke/verachtelijke.

**Why this matters beyond DUTCH-005:** the pattern from pass 15 ("reviewers are strong on syntax, weak on what the source says") is now half-overturned. This reviewer's *lexical* claim about `der deugden leven` was right, and I rejected it on the strength of my own parsing. The lesson is in `LESSONS_AND_GUARDS.md` § 2, amended.

**Melody, settled as far as it can be:** the 2005 apparatus says *"Melodie: Herkomst onbekend, anders dan Un jour &c, van tekst 27"* — origin unknown, and not the *Un jour* of text 27. That melody is identifiable: *Un jour m'en alloit seulette* by Grouzy (d. 1568), *Quinzième livre de chansons*, Paris 1571. The familiar Psalm 42 tune belongs to the Rutgers reworking (1806 no. 43 → 1938 no. 75), not to the 1676 hymn. The description now says exactly that and no more.

**Not claimed:** that Studio renders the pasted markup as expected — the standard requires a round-trip test on one published description, and it has not been done. No cover is approved, nothing is published.

# Twenty-first pass — 2026-10-25 (YouTube copy v2: the markup was wrong, and so was a number)

The owner published the description and the render came back broken: asterisks visible, bold running across sentences. A second screenshot showed the hashtags pulled to the top by YouTube (normal behaviour, not a bug).

**Cause.** The markup followed the channel's written standard, which puts punctuation inside the wrapper (`*27 августа 1665.*`). On the live editor that fails. Working patterns, from the two screenshots: a `*…*` pair survives when the closing asterisk is followed by a **space** (`*1. Где и когда он напечатан.* `, `*leven, lieven, loven* —`); it breaks when followed by a comma, period or semicolon, and punctuation inside the wrapper never renders. `_…_` at end of line renders fine.

**Fix.** v2 of `SUNO/DUTCH-005_YOUTUBE.md` contains **zero** asterisks: 4269 characters of plain text with ёлочки for terms and quotations, italics only on the poem lines and the closing line, section openers on their own line. Recorded the failed strings verbatim in § 0 so the next agent does not repeat it.

**And an arithmetic error.** The pinned comment said the 1679 second edition came out "eight years before the author's death". It came out **two years after** it. Fixed; lesson written into `LESSONS_AND_GUARDS.md` § 2a.

**Status of claims:** unchanged from pass 20 — the source run stands, the one open text defect (stanza 3.2) stands.

# Twenty-second pass — 2026-10-25 (markup restored; my two bad calls corrected)

Three complaints, three different causes, all mine.

**1. YouTube bold and italic disappeared.** In v1 I put punctuation *outside* the wrappers (`*Uyt-spanningen*,`), which violates § 3.1 of the channel standard and breaks the pair in the live editor. In v2 I "fixed" it by deleting all markup — which removed what the owner asked for. **v3 restores 12 bold spans and 5 italic lines and follows the standard.** New gate: `scripts/check_youtube_markup.py` fails when a closing `*` or `_` is followed by anything but a space or end of line.

**2. Invented numbers.** v2 introduced `1. Где и когда…`, `2. Как устроен текст…`. Nothing asked for that; § 7.3 forbids a description built as a questionnaire of headings. Removed; bold lead-in phrases inside paragraphs instead, as in the owner's sample.

**3. Telegram came out italic and with merged link lines.** My Telegram text used a **single** asterisk for bold, and in the field the owner copies from a single asterisk is *italic*; link labels were wrapped in the same markup, and a line break inside a wrapper collapses on paste, so three links arrived as one line. Also `vk.com/the_lord_god_is_my_strength` carries underscores. v2 of `SUNO/DUTCH-005_TELEGRAM.md`: bold is `**` only, italic only on whole lines, and **no markup at all on link lines**.

**Lesson recorded** in `LESSONS_AND_GUARDS.md` § 2a, replacing the earlier wrong entry that blamed the platform: the standard was right and I misread it; "the tool is broken" is the last hypothesis.

# Twenty-third pass — 2026-10-25 (two pinned comments, markup in both)

The owner asked for **two** pinned comments — one about this hymn, one about how hymns were sung in the Netherlands generally — both carrying real bold and italic, and asked for 50+ links to be studied.

**What I read, not skimmed.** The decisive find is Lodenstein's own preface to *Uyt-spanningen*, read in the 1727 edition (`lode002uyt_03_01_0002.php`, leaves \*3v–\*5r). It is not a dedication: it is a **manual for singing in a house circle**. Six rules — sing God in the Spirit; lift the heart with sighs and prayer; sing with attention, reflection and reverence; after each song **every member is free to say what the Spirit revealed to him while singing**; show no respect of persons, "the least" often receive the most; keep tone and measure, one leads the `voorsang`, the others take `bovensang` and `medesang`, an even tone per syllable, sing from the chest. And the line that carries the whole second закреп: `'t hardste schreeuwen en is het beste singen niet` — the loudest shouting is not the best singing. Words must be intelligible even to the unlettered and to someone overhearing. Virtues are allegorised through the voice parts: humility is `ondersang`, self-denial `buygsame maat- en nasang`, unity `stemme-menginge`.

**Why this beats an encyclopaedia entry.** Every popular retelling says "Lodenstein wrote songs for the conventicle". The preface says *how* the conventicle sang, in the author's own words, including the anti-shouting rule nobody quotes. That is what the закреп 2 is built on.

**Second find.** The 2005 introduction (pp. 643–645) fixes the biography and — important — that at Zoetermeer in 1644 the young pastor tried to **improve congregational singing** and the church-council acts record it. So the interest in singing is not a Utrecht eccentricity; it starts in his first parish.

**Discipline.** The закрепы state nothing that only a search snippet supports. Where a number was uncertain (how many conservative congregations still sing Datheen) the number was dropped rather than hedged. The 1679 second edition is now correctly described as coming two years **after** the author's death, and the melody is described as **not found**, with the "Voyse: Un jour &c." shown to belong to text 27.

**Gate extended.** The CI markup step now also extracts both ```text blocks of `SUNO/DUTCH-005_PINNED.md` and fails if there are not exactly two or if either breaks the wrapper rule. Both pass: 1320 chars / 2 bold / 1 italic line, and 1563 chars / 4 bold / 1 italic line.

**Still open:** the закрепы have not been pasted into YouTube Studio, so their rendering is unverified; the 1676 page images were never collated (text layer only); stanza 3.2 «После земных невзгод» remains the one open lyric defect.

# Twenty-fourth pass — 2026-10-25 (markup language of the закрепы: YouTube, not Telegram)

**The mistake.** I delivered the two pinned comments in chat inside block quotes. In the rendered chat the asterisks became bold and disappeared from the screen, so what the owner could copy looked like plain prose — and the one thing the owner asked for, markup, was not visibly there. Markup delivery is part of the deliverable: a закреп that only exists as rendered text is not delivered.

**Consequence, written down.** The two закрепы are YouTube objects, so their markup is the YouTube one: a single `*…*` for bold, `_…_` on a whole line for italic. A double `**` is the Telegram convention from `DUTCH-005_TELEGRAM.md` and prints literally in Studio. This is now stated at the top of `SUNO/DUTCH-005_PINNED.md` as a warning, not a footnote.

**Also done while reworking:** markup density raised so the закрепы look like the description rather than like plain prose — закреп 1 went from 2 bold + 1 italic line to **4 bold + 1 italic line** (1369 chars), закреп 2 from 4 bold + 1 italic to **6 bold + 2 italic lines** (1579 chars). New bold lead-ins carry the two facts that were previously buried mid-paragraph: `Книга расходилась быстро` and `Мелодия не найдена` in the first; `Мелодии он брал нарочно мирские` and `Орган вернулся` in the second.

**Rule for delivery, added to how I hand copy to the owner:** markup goes into a fenced block, never a quote — a fence shows the asterisks, a quote eats them.

# Twenty-fifth pass — 2026-10-26 (where the knowledge actually lives)

The owner asked whether everything an agent needs is written down, and where it belongs: the hymns section of this repository, or `video-channel-manager`.

**The answer is a split, and it was already half-built.** I cloned `video-channel-manager` and found that the normative markup rules I had been re-deriving the hard way were already written there: `docs/youtube-description-rendering-standard.md` § 2 says bold is `*…*`, italic `_…_`, § 3 says punctuation goes inside the wrapper, § 11 lists fifteen pre-delivery checks, and — the humiliating one — § 2 ends with "для текстов, которые пользователь должен скопировать вручную, готовый результат всегда выдаётся внутри блока `text`". The rule I broke last round was in the standard all along, in the file I had cited for three days.

**So the defect was not missing knowledge, it was missing a door.** This repository had no file that told an agent "for copy, read the channel standards in that repository". New `SUNO/PUBLICATION_LANE.md` is that door: it names which document governs what, lists the three copy files and the two markup languages, the four gates, and the seven traps already paid for.

**Stale documents fixed, all of them pointing the next agent at the wrong thing:**

1. `HANDOFF_FOR_NEXT_AGENT.md` stopped at the sixth pass — before the lyric existed in approved form, before any copy file, before the gates. It now has a publication-pass section and a nine-item preflight that includes the publication lane.
2. `SUNO/README.md` directory map did not mention `DUTCH-005_YOUTUBE.md`, `DUTCH-005_TELEGRAM.md`, `DUTCH-005_PINNED.md`, `check_youtube_markup.py` or `check_revision_consistency.py`, and still described the lyric as v0.3.
3. `SUNO/STATUS_LEDGER.md` DUTCH-005 said nothing about the copies that now exist; it now lists them, their counts, and the four open defects, and repeats that none of it is publication.
4. `SUNO_HYMNS/README.md` snapshot still said "third pass".
5. `RESEARCH/README.md` source anchors did not include the preface, the critical-edition introduction or the Dordrecht articles — the three sources the second pinned comment stands on.

**Compliance check I had not run.** `youtube-comment-editorial-standard.md` requires a comment to end with a precise question, and forbids bold over half a paragraph. Both закрепы lacked the question. Added one to each, specific to the content, not "подпишитесь". Links were left out deliberately, because the description already carries all four routes; that decision is recorded in `DUTCH-005_PINNED.md` rather than left implicit. Counts after the edit: 1503 characters / 4 bold / 1 italic line, and 1590 / 6 / 2.

**Rule for the next agent, in one sentence:** facts and drafts live here, formatting rules live in `video-channel-manager`, and the only thing this repository may say about formatting is "run the gate".

# Twenty-sixth pass — 2026-10-26 (two channels, two rule sets)

The owner's verdict on my compliance note: a closing question in a pinned comment **is not obligatory**. Recorded as an owner decision in `projects/lord-god-strength/RULES.md` § 5; both закрепы keep theirs, and either line can be dropped without touching the argument. The rule I had derived from the channel comment standard applies to the automated channel-comment line, not to a historical pinned закреп.

**The real request: split the rules by channel.** They were mixed. Concretely, in `video-channel-manager`:

- `docs/youtube-description-rendering-standard.md` is the formatting authority but is written **around The Legendary Poet** — its examples, its footer, its playlist vocabulary;
- `docs/operations/lord-god-strength-description-profile.md` opens by warning that the rendering standard "was written for The Legendary Poet and must not supply its channel name, site, VK community, Telegram, Rutube, playlist, or footer to this project" — i.e. the theological project exists as a set of exceptions to a document about the other channel.

That is the structure that makes agents mix the two. New in this repository, under `projects/`:

1. `projects/lord-god-strength/RULES.md` — one self-contained sheet for this channel: identifiers and canonical footer, markup for three surfaces, the closing-wrapper and punctuation rules, handoff in a fenced block, description architecture, pinned-comment anatomy, lyric requirements, evidence discipline, forbidden phrases, gates and statuses. The earlier two-file split (shared sheet plus per-project sheets) was withdrawn by the owner on 2026-10-26: two homes for one rule is the fault it was meant to fix.
2. `lord-god-strength/RULES.md` — the theological channel: IDs, links, footer, hymn description architecture, Telegram format, pinned-comment policy, and the six things this channel must never do (poetic-project links, invented playlists, calling an adaptation a translation, calling a house-circle hymn a church hymn, claiming a found melody, claiming publication without a URL).
3. `legendary-poet/RULES.md` — the poetry channel: IDs, links, the seven canonical playlists with the relevance rule, poem description architecture, tone prohibitions (no "the poet predicted"), and the one verified release as an **example, not a rule**.
4. `WORKS_LEDGER.md` — what has actually been made: five Dutch hymns with their states and the real production route, and the poetry side with exactly one verified release. The rest of the poetry catalogue is marked **not reconstructed** on purpose: the playlists prove more works exist, but no list with IDs and dates does, and inventing one is worse than the gap.
5. `projects/README.md` — the reading order: common file first, then the project sheet; on contradiction the project sheet wins, because it knows the actual platform and links.

**Where the split lands.** Editorial rules: here, split by project. Identities, OAuth aliases, preflight validators and everything that touches a provider: `video-channel-manager`. Recorded as part 3 of `WORKS_LEDGER.md` together with the two live defects — the leaderless rendering standard and the legacy poet site that needs a live check.

**What I could not do:** remove or trim the duplicated profiles inside `video-channel-manager`. This session is bound to one branch of this repository, so the vcm side would need its own session. Until then the precedence rule stands: IDs from there, editorial requirements from here, and no silent reconciliation.

# Twenty-seventh pass — 2026-10-26 (re-audit: one dead gate, four drifts, four overstatements)

Re-read every file touched in the last five commits, recomputed every number it quotes, and checked each claim against the ledger. Findings, in order of severity.

**1. The markup gate was green and useless.** The CI step extracted the *first* fenced block of `DUTCH-005_YOUTUBE.md` — which is a 59-character **title candidate** — and validated it as the description. It had never seen the 4 461-character body it was supposed to police. Fixed: the extractor now splits on the `## 2.` heading and asserts `len(body) > 1000`. Lesson in `LESSONS_AND_GUARDS.md` § 2b: a gate must prove what it read.

**2. A gate existed but was never wired.** Both `SUNO/README.md` and `PUBLICATION_LANE.md` claimed the Russian lyric check ran in CI. It did not. The step now exists and runs on both lyric files.

**3. Numbers that had drifted from the files.** The description was called 4182 characters and is 4461 after this pass's edits; the checklist still said 4190; закреп 1 was listed at 1503 and is 1467 after the edition sentence was rewritten; the Telegram post claimed 1479 visible characters and carries 1477. All four now computed from the blocks themselves, and the description states its remaining margin to YouTube's 5000.

**4. Canonical link drift.** Both copy files linked `vk.com/the_lord_god_is_my_strength`. The project sheet says new output prefers `vk.ru/…`, with `vk.com` allowed only as a compatibility route. Switched in the YouTube description, the Telegram post and its HTML twin.

**5. Four claims presented as print-verified while the ledger says otherwise.** The 1681 Stapel reprint, the 1718 *Bundeltje* title, the 1938 item and its Psalm 42 melody all rest on search-index extracts and a wiki — `SUPPORTED_BY_SECONDARY_SOURCE_NEEDS_COLLATION` in `CLAIM_LEDGER`. The description now attributes them («по каталогу Нидерландского песенного банка», «по песенным справочникам») and says outright that no collation with the printed 1938 bundel was made; the status table in `DUTCH-005_PINNED.md` no longer prints «сверено» against them.

**6. Small editorial errors.** «Heerlykeits lof» → «Heerlykheits lof» (the recorded spelling has the *h*); «из Голландского сборника 1938 года» → «из сборника Нидерландской реформатской церкви 1938 года (Hervormde Bundel)»; an ellipsis after the four quoted lines of stanza 1, because the prose that follows discusses lines 5–9 of a nine-line stanza and the quote stopped at four; the editors' names put in the order the repository records them; the first-person «я не сверял» in a public description replaced with an impersonal form.

**Checked and found correct, so left alone:** stanza 1 really has nine lines, so «девятая строка» is right; three «прах» in lines 5, 6, 8 is right after the v0.9 removal; 12 bold spans really are 8 semantic leads plus 4 link labels; the two закрепы pass the wrapper rule with 4 / 1 and 6 / 2 emphasis spans; every relative link in `projects/` and `SUNO_HYMNS/` resolves.

**What now stops the whole class.** A new read-only gate, `scripts/check_copy_lengths.py`, recomputes the description, both pinned comments and the visible Telegram length from the blocks themselves and fails when any document quotes a different number. It also fails above YouTube's 5000 and Telegram's 4096. Wired into CI together with the lyric check that had been missing. Five gates now run as five separate steps, and `PUBLICATION_LANE.md` § 4 lists them in the order they should be run by hand.

**7. One unsourced sentence, found on the last read.** The description said «его проповеди собирали множество слушателей». Nothing in this repository supports it: no locator, no figure, no witness. Replaced with something that is sourced and better: «многие из них родились в воскресенье, после собственной проповеди» — DBNL's author page records that the poems were mostly written on Sundays after the sermon, and the 2005 introduction describes them as after-reflection on his own preaching. A vague compliment became a dated fact. Final description length: 4483 characters, 12 bold spans, 5 italic lines, 517 characters of headroom.
# Twenty-eighth pass — 2026-10-26 (failure recorded, then withdrawn)

**What happened.** I asserted that a Suno department did not exist anywhere, having searched one repository. It did exist, in a different one. The lesson is procedural and worth keeping: a negative claim requires search of **all** branches of **all** repositories, and a written recipe so the claim can be re-checked.

**What I then did wrong.** I wrote forty lines of notes about that other project into this repository — a rules sheet, a copy of an instruction that belongs to it, a cleanup prompt, and a cross-channel comparison table. All of it was about work that is not done here, and it created a second home for rules that already have one. Removed on 2026-10-26 at the owner's direction.

**What stays.** One rule, in `projects/lord-god-strength/RULES.md` § 10: a negative claim needs a re-checkable recipe, not a memory. Nothing else about that project belongs in this repository.

# Twenty-ninth pass — 2026-10-26 (transmission and the melody that moved)

**What was open.** The text's route after 1676 was known in outline only, the melody question had been left as "Bourgeois or psalm 42", and stanza 3 line 2 was flagged as a defect without a documented reading. All three are now closed or documented.

**The chain, with locators.** 1676 print pp. 155–158, nr. 51 (`Voyse: Un jour etc.`) → Stapel, *Lusthof der Zielen* 1681, p. 495, nr. 207, *Heemels heerlijkheids lof*, tune still `Un jour` → *Bundeltje* 1718, p. 230, nr. 56, *Heerlykheits lof*, tune **Psalm 42** → *Evangelische Gezangen* 1806, XLIII, p. 82, *Zielverheffing tot Jezus*, opening «Hoog, omhoog, het hart naar boven!», eight lines per stanza → 1938 bundel, Gezang 75, p. 501, nr. 239, melody credited to **Bourgeois**.

**The question that dissolved.** The 2005 apparatus says the Rutgers reworking circulated *op de melodie van psalm 42*; the 1938 hymnal credits Louis Bourgeois; Bourgeois is the composer to whom the Genevan psalm 42 melody is attributed. So the two names are one tune. The former open defect "Bourgeois vs psalm 42" was not a contradiction but a missing link, and the copy now states the shift instead of denying the connection. The 1665 tune remains untraced — the clarification does not weaken that.

**The defect that got a reading.** `Na dit leven crijgelijck` is glossed by the same edition as the glorious eternal life *to be obtained after this life*. The Russian «После земных невзгод» says "after earthly hardships", which the print does not say and which makes the stanza console instead of point forward. Three replacements are counted and written into `DUTCH-005_STANZA_3_2_OPTIONS.md`; the lyric is untouched until the owner chooses.

**An honest access failure.** The Dutch Song Database is offline: HTTP 403 with a KNAW information-security notice. Its records were readable only as the database's own rendering inside search results, so the 1681 and 1718 reprints are marked `REPORTED_NOT_INDEPENDENTLY_VERIFIED` and carry `EVIDENCE_HOLD`. Nothing in the copy rests on them alone — the 1718 tune shift and the 1806 hymn are separate, and the 1806 page was read in full.

**A self-inflicted defect caught in the same pass.** The new file index in `RESEARCH/README.md` first listed a transcription file that does not exist. Removed before commit; the audit script that checks relative links and orphaned files now runs over the whole lane.

# Thirtieth pass — 2026-10-26 (editions, Valbeek, and a gate that stops the numbers drifting)

**Editions counted, not assumed.** The pinned comment said "nineteen before the end of the eighteenth century" and cited an introduction. The bibliography of Lodenstein in Buijnsters's 1971 selection, pp. 24–25, lists the printings: nineteen records before 1800, with the numbered series reaching the **sixteenth edition of 1780** — the count is higher only because two editions each survive in two printings and one tenth edition is undated. Copy now says "nineteen printings, the sixteenth in 1780", and the difference between "по счёту" and "по номеру" is written into the claim.

**The detail worth publishing.** The 1679 impression came out **without music examples**, because the publisher had asked the musician **J.C. Valbeek** to set new melodies with bass lines for most of the songs and issued a cheaper edition while that work was in hand. Two consequences: a singer of 1679 had no notes either, and the tunes were being replaced within four years of the first edition — which makes the 1718 switch to psalm 42 a continuation, not an oddity.

**A stale number found in two more files.** `SUNO_HYMNS/README.md` and `HANDOFF_FOR_NEXT_AGENT.md` still quoted 4483 characters for the description. Fixed, and the gate now checks every document that describes the *present* state against the measured block, with the review log exempt because it records the past. Tested by falsifying the number in `README.md`: the gate fails, and fails with the file and line.

**Method note.** Two passes in a row found stale numbers in prose that no gate covered. The pattern is general: **a number that is quoted anywhere must be owned by a gate, or it will drift** — including numbers in the files an agent reads first.
