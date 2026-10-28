# DUTCH-005 — three-way collation: 1676, 1727, 2005

**Why this file exists.** The earlier passes read the 1676 print only in part: the incipit, the tripled words, the tune line, the date and stanzas VIII–X. On 2026-10-26 both printings were read **in full**, stanza by stanza, and set against the 2005 critical edition. The result is below. It hardens the base **before** the Russian line in stanza III is touched.

**Witnesses.**
- **1676** — *Uyt-spanningen* (Utrecht: Willem Clerck), pp. 155–158; DBNL `lode002uyt_01_01_0061.php`, read in full 2026-10-26.
- **1727** — ninth edition, same pages; DBNL `lode002uyt_03_01_0062.php`, read in full 2026-10-26.
- **2005** — critical edition, item 56, pp. 263–267; DBNL `lode002uyt_02_01_0062.php`, read in full 2026-10-26.

**What was not seen, in any of the three:** the page itself. All three are text layers of digital facsimiles. Typography, drop capitals and the illustration `ill0155` remain unviewed.

## 1. Substantive differences between the two printings

| Place | 1676 | 1727 | 2005 | Reading to adopt |
|---|---|---|---|---|
| I.3 | 't Regte leven, **lieven**, loven | 't Rechte leven, **leven**, loven | lieven | **1676** — the tripled word must differ in each form; 1727 is a compositor's slip |
| VII.3 | **Vindt** alleen genoegen in | **Vind** alleen genoegen in | Vindt | **1676** — the subject is `Iesus`, third person |
| VII.8 | Mijn siel na boven **dat**, | Mijn siel na boven **dan**, | dan | **1727** — `dat` breaks the parallel with line 5, which reads `dan` |
| VIII.2 | Oorsaack van **wat** hier schoon schijnt | Oorsaack van **al wat** hier schoon schijnt | wat | **1676** — `al` is the later smoothing |
| VIII.5–6 | call line + abbreviated repeat (`U etc.`) | call line, repeat omitted | both lines printed | **1676** structure: eight printed lines plus the `. etc.` repeat instruction |
| X.1 | **Iesus lof** en Heerlijckheyd! | **Jesus loff** en Heerlijckheyd! | Jesus lof | spelling only |

Three of these five were already recorded (`CLM-DUTCH-005-VARIANTS`). **VII.3** is new: 1676 prints `Vindt`, 1727 prints `Vind`, and the 2005 edition silently agrees with 1676.

## 2. Spelling only, not variants

`pragt`/`pracht` (II.1); `crijgelijck`/`krijgelijck` (**III.2**); `cleeft`/`kleeft` (VI.4); `Cijter`/`Cyter` (X.3); `so`/`soo` (V.5); `costlijck`/`kostlijck` throughout; `Iesum`/`Jesum` (I.4); `lof`/`loff` and `Ougstmaand`/`Oogstmaand` in the dateline. The 1727 compositor modernised `c` to `k` and `u` to `v` systematically — that is orthography, not text.

## 3. What this settles for the Russian

**Stanza III, line 2** reads `Na dit leven crijgelijck` in 1676, `Na dit leven krijgelijck` in 1727, `Na dit leven crijgelijck` in 2005. The reading is **stable across all three witnesses** and glossed by the 2005 apparatus as the glorious eternal life *to be obtained after this life*. So the Russian line «После земных невзгод» is a defect of the adaptation, not a variant of the source, and the fix is decided on the Dutch, not on a conjecture.

**Stanza I, line 3** is the one place where a later printing is right and the first edition is wrong on the level of sense: `leven, leven, loven` cannot be — the poem's whole device is that the three forms differ. Recorded as an emendation with its reason, not as a silent correction.

**The drop capitals** are real: the 1676 text reads `H Oog!` because a capital `H` stands apart from the rest of the word, i.e. **HOOG!**. The transcription keeps the print's form; the copy does not need it.

## 4. Limits that survive this pass

- No page image of either printing has been inspected. Two impressions still disagree, so no wording is called *definitive*.
- The 1727 printing is not an independent witness in stemmatic terms: it may descend from a corrected copy of 1676.
- The illustration on p. 155 (`ill0155`) exists in the digital facsimile as a separate image file; it has not been opened, and nothing is claimed about it.

## 5. Image access — attempted 2026-10-25, and exactly where it stopped

The text layer is not the only thing DBNL holds. The 1676 volume is served as:

- `https://www.dbnl.org/tekst/lode002uyt_01_01/lode002uyt_01_01.pdf` — the text PDF;
- a separate **scan bundle** offered on the same page as «Download Scans» (18.17 MB for the 1676 print) next to the 9.41 MB text PDF and the ebook;
- single images per page, e.g. the cut that stands above `Voyse: Un jour &c.` on p. 155 at `https://www.dbnl.org/tekst/lode002uyt_01_01/lode002uyt_01ill0155.gif`.

None of these could be opened from this session: outbound HTTP from the sandbox is allowlisted to package and source-code hosts, so DBNL binaries and images are unreachable, and the page-fetch tool parses text and PDF *text* only, with the first 30 pages of a PDF — pp. 155–158 of a 425-page octavo are far outside that window, and the scans are images with no text layer at all.

**What this means, stated without softening:** the collation in § 1–§ 3 remains a collation of three *transcriptions*, one of them the first edition's. It is a stronger base than one transcription, but it is not a page-image collation, and the copy does not claim to be. The next session that has unrestricted network access needs exactly two addresses: the 1676 bundle above for pp. 155–158, and the 1681 anthology for p. 495 — `https://www.dbnl.org/tekst/stap007lust01_01/` (Claes Stapel, *Het lust-hof der zielen*, Alkmaar 1681; the text layer there is the one that interleaves two printed columns, which is precisely why the page image is wanted). Nothing else about this question is still unknown: it is an access question, not a research question.
