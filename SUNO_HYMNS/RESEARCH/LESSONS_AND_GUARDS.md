# Lessons and guards — what went wrong, and what now stops it

**Started:** 2026-10-25, after the DUTCH-005 session (v0.5 → v0.8 in one day, ten image battles).
**Purpose:** the same classes of error kept recurring across agents and across revisions. This file names them, gives the evidence, and points at the check or rule that now catches each one. It is a working register, not an apology: add to it, do not rewrite it.

**Read this before** drafting a lyric, applying a review, or generating artwork. The mechanical guards are in `../scripts/` and run in CI; the editorial guards are in `../SUNO/STYLE_AND_PRODUCTION_RULES.md` § Failure guards.

---

## 1. Errors I made in this session

Each entry: what happened, what it cost, what stops it.

### 1.1 Rhyme bought with a word that is not in the line
Stanza 2's close read «Сердцу всех выше — кровь и любовь» to rhyme with «кровь». The Dutch line is `'t Hert boven alles gelden doet` — there is no "love" in it. The rhyme had been paid for with a word invented for it. Rolled back in v0.8.

**Cost:** one revision, and the rhyme column lost a stanza.
**Guard:** after any rhyme pass, every slot where rhyme changed a word must be listed with a verdict — *kept because …* or *reverted*. The table is `DUTCH-005_LYRICS.md` § What the rhyme cost. A rhyme that needs a word the source does not have is not a rhyme, it is a rewrite.

### 1.2 The same purchase left standing in another stanza
Stanza 1 has «прах» four times. The print has `op aard` three times and a **different** word in the last line (`niet waard`). The fourth «прах» exists for the rhyme — the identical trade rejected in 1.1, three stanzas away, in the same revision.

**Cost:** found by the owner, not by me; still open as a decision.
**Guard:** a trade accepted or rejected in one stanza sets the precedent for all ten. When two stanzas face the same trade, decide once and say so. Consistency is a fidelity issue: a text cannot be literal in stanza 1 and free in stanza 2 for the same reason.

### 1.3 Invented repetitions read as a refrain
Same root cause. The print's three-fold `op aard` is a device with a turn; a fourth repetition makes «прах» behave like a chorus — in a hymn the rules forbid adding a chorus to.

**Guard:** count the repetitions **in the source** before mirroring them, and check that the last slot really is a repetition. `SUNO/STYLE_AND_PRODUCTION_RULES.md` § Text preparation already forbids adding refrains; this is the same rule applied to a single word.

### 1.4 Overwriting a revision in place
v0.6 was rewritten in place as v0.7, and the previous text survived only in git. Later, the whole lyric file was regenerated from a script and the rhyme-cost table silently disappeared; the same rewrite shortened the changelog.

**Cost:** one lost table (restored from `f4e0dcf`), and a file that no longer matched its own registers.
**Guard:** a new revision goes to the same path **only** after the old one is retrievable (`git show <sha>:path`), and after any wholesale rewrite, diff the section headings against the previous commit. Headings are cheap to compare and catch lost content immediately.

### 1.5 Registers drifting behind the text
Three real defects, all found late:
- the production package still said **"five stress marks"** and listed `дару́ет`, which had left the text two revisions earlier;
- a status table said **v0.3** while the text was v0.8;
- a sentence appeared twice in a row — the residue of an edit applied twice.

**Cost:** documents that contradicted the shipped file, in a project whose whole value is that its documents can be trusted.
**Guard:** `scripts/check_revision_consistency.py`, now a CI step. It compares the prose against the files: the current revision must be named, no stale revision may appear except on a line that marks it as history or as a hypothetical, declared stress-mark counts must equal the marks actually present, and duplicated sentences fail.

### 1.6 A known-wrong title kept in the header for many turns
The Dutch title is «Хвала славе»; the project delivered under «Слава Господня», which drops `Loff` (praise) and adds a `Heere` the title does not contain. I recorded the problem in a file and left the header alone, on the grounds that renaming is the owner's call. The owner had to ask directly: «Перевод точно Слава Господня, а не Хвала Славе?»

**Cost:** every delivery in between carried the wrong title; the decision came one turn later than it should have.
**Guard:** *recording* a defect is not *raising* it. A known-wrong label belongs in the delivery header of the turn it is found — one line: "this title is a working placeholder, the Dutch reads X, decide" — not in a file section the owner may never open. Owner's call still means the owner's call; it does not mean silence.

### 1.7 Misread house terms — "battle"
"Баттл" in this project means **one generation producing two candidates side by side**; three battles means three generations, six images. I delivered three single images, then repeated the mistake once more before the owner spelled it out.

**Cost:** two wasted rounds and the owner's patience.
**Guard:** when a word looks like a house term of art, say the interpretation back in one line *before* spending the budget. Written down now in `STYLE_AND_PRODUCTION_RULES.md` § Failure guards so the next agent does not have to guess.

### 1.8 Long chained shell commands
Python edit + `git commit` + `git push` in one call, and a `sleep 115 && gh pr checks` gate: both timed out, the second one leaving the CI state unknown while I reported it as unknown.

**Guard:** editing, committing, pushing and reading CI are four short calls. Never sleep to wait for CI; ask for the status when it is asked for, and say plainly when it is unknown.

### 1.9 Treating a review as instructions
A review aimed at v0.5 arrived when the text was v0.7; four of its points were already fixed, one contradicted itself, one was wrong about the Dutch. Applying it wholesale would have regressed the text.

**Guard:** already in the standing rules — every reviewer claim needs a line of print or a gloss behind it. This session's count: **8 accepted, 4 rejected**. The rejections are as valuable as the acceptances and are logged with the print line that killed them (§ 2).

### 1.10 Claims about things never seen
`aard`/`waard`, the gloss of `ijdel`, the 2005 commentary — each was recorded as **a lead**, not as verified, and the file says which. The temptation is to write "the commentary says" when what happened is "a reviewer wrote that the commentary says".

**Guard:** keep the two verbs apart in the sentence itself: `X said the commentary glosses it as Y — not verified here`. A research register that cannot tell a lead from a check is worth nothing.

---

## 2. Errors from other agents and reviewers

Every one of these was checked against the 1676 print or the 1727 collation before being rejected. They are listed because the same mistakes will be made again by the next reviewer.

| Claim | Why it fails | Where recorded |
|---|---|---|
| "Our hymn is № 56 / № 131" | DBNL file numbers are not hymn numbers: `0056` is DUTCH-001, `0131` is a different poem entirely. Two wrong texts would have been transcribed | `TRANSCRIPTION_DUTCH-005_1676.md` § Title collision |
| "Stanza 8 lost a negation: `noch`" | The print reads `nog`, and `Min vermaackt` is affirmative — there is no negation to lose. Adopting it makes stanza 8 deny what stanza 9 affirms | `DUTCH-005_LYRICS.md` § Stanza 8 |
| "`Die` = the heavenly Beauty" | The stanza *adores* that Beauty; a clause about fading cannot be about her. `Die` reaches back to `wat hier schoon schijnt` | same |
| "The stanza-6 person clash is a Russian bug" | It is in the Dutch: plural noun, singular verb, then a turn to the second person. Smoothing it hides a feature of the print | `REVIEW_LOG` pass 14 |
| "`Жизнь добродетелей` mistranslates `der deugden leven`" | It is a correct genitive plural. The error was in the *closing* line of the stanza, which was fixed | `REVIEW_LOG` pass 15 |
| "The tripled word needs a finite verb" | The Dutch triples an infinitive (`lieven`), and the device runs 7–10. One finite form breaks it | same |
| "Stanza 8 says the Beauty vanishes" | Retracted by the same review half-way through; the reading is the one the project already had | same |
| A pasted full Russian version | Introduced «пустый обман», «кифара» for `Cijter` (a cither), «все языки человеков», «Сие» ×4, «прелести» for deceit, a fused 12-syllable line and a 15-syllable line | `REVIEW_LOG` earlier passes |

**Pattern, as it stood after v0.8:** reviewers are strongest on *syntax and calque* and weakest on *reference and enumeration*; the v0.8 pass took every syntactic point and rejected every claim about what the source says.

**Amendment, same day — the pattern was half wrong.** When the 2005 commentary was finally read (DBNL pp. 263–267), one rejected *lexical* claim turned out to be correct: `der deugden leven` is glossed *het deugdzame leven*, the virtuous life. I had overruled it by parsing the genitive myself and calling it a correct "life of the virtues". A second claim I had admitted only as a *lead* (`yd'le` = vergankelijk) was confirmed. So the real rule is narrower and less flattering:

> A reviewer is unreliable on **identifications and enumerations** — which poem, which number, which clause — and surprisingly often right on **what a word means**. Rejecting a lexical claim requires a gloss, not a parsing. If the gloss has not been read, the honest status is *lead*, not *rejected*.

That is why `rejected` in the log now needs a source line, and why this pass produced a source run with per-link status: `RESEARCH/DUTCH-005_SOURCE_RUN_50PLUS.md`.

---

## 3. Mechanical hazards

- **Combining acute and NFC.** A word written with `й` + U+0301 reads as a different string from the same word without it. Any accent check that compares raw strings silently passes. Normalise to NFD before testing, as `check_ru_lyric.py` does.
- **`\w` does not include combining marks.** Any word-shaped regex splits `соединена́` into fragments, so an accent counter built on `\w+` reports zero. Split on whitespace and punctuation instead. (This bug was in the first version of `check_revision_consistency.py`, in this session.)
- **Counting syllables by hand.** Always a script; hand counts were off twice.
- **One `grep` for a version string.** The same revision is written `DUTCH-005-RU v0.8` and `DUTCH-005-RU-v0.8`; a single pattern finds half the mentions and reports success.
- **`str.replace` with multi-line or table anchors.** It silently matches nothing. Grep the exact line, or slice between unique anchors.
- **No image tooling in the sandbox.** `PIL` and `file` are absent, so image dimensions cannot be verified locally; the generator's aspect ratio is taken on trust and the file is read visually instead.
- **DBNL is a text layer.** No claim about typography, drop capitals or `etc.` spacing can come from it. The italic markers in the transcription (`*pragt*`, `*Lusten*`, `*Goud*`) are DBNL emphasis, **not** evidence of the print's italics.

---

## 4. What a delivery must pass before it is shown

1. **Counts from the file, not memory:** verses, lines, marks, rhyme slots — computed.
2. **Both lyric files identical** apart from tags, the declared echo and the marks (`check_ru_lyric.py`).
3. **Registers name the current revision; no stale counts** (`check_revision_consistency.py`).
4. **Every rhyme-forced word has a verdict**, and the same trade is decided the same way in every stanza.
5. **Every claim that came from a reviewer has a print line or is labelled a lead.**
6. **Open decisions surfaced in the delivery header**, not buried in a file.

---

## 5. Open defects as of this writing

- **Stanza 1: CLOSED in v0.9.** The fourth «прах» was removed on the owner's decision; the stanza now has three `прах` (5, 6, 8) and a close that does not rhyme — the print's shape. What settled it was not an argument but a decision: both stanzas that faced the same trade now resolve it the same way. This is the case to cite when the next review argues that a rhyme is worth a word.
- **Stanza 2** is out of the rhyme column after the v0.8 rollback; 4 stanzas meet standard B, 3 half, 3 not at all. The three failures end their call on words with no rhyme available.
- **Five stanzas** still carry calque-shaped openings (3, 5, 6, 8, 9) — the next editorial pass, and it needs the DBNL gloss for `crijgelijck`, `der deugden leven`, `enckel schijn`, `slijck`, `veerdig`/`genoegen`, `wakkerheyd`, `Menschen seden`.
- **Nothing has been generated.** No audio, no approved cover, no stanza signed off. Production state `LYRIC_DRAFT`.
- **Cover:** ten candidate rounds produced a chosen look (golden cathedral, figure with open arms, organ, host of angels) but no approved file; the images live outside the repository at `/home/user/images/dutch-005/` and are **not** in `ASSET_MANIFEST.md` yet.
