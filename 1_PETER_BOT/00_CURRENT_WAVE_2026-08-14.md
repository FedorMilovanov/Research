# 1 Peter Bot — Source Marathon Wave 1

**Date:** 2026-08-14  
**Status:** `SOURCE-MAP-ASSEMBLED / CLAIM-LEVEL-REVIEW-OPEN / RESEARCH-ONLY / PUBLICATION-HOLD`

## 1. Result

This wave builds a durable research base for the complete 1 Peter course rather than another undifferentiated bibliography.

- `04_SOURCE_INDEX.md` contains **96 discovery/navigation sources**.
- `data/source-ledger-v1.json` promotes **33 core sources** into the fail-closed machine control set.
- `01_GREEK_TEXT_MANUSCRIPTS_AND_LEXICA.md` contains a **40-lemma/family priority queue** for 1 Peter.

The discovery index is intentionally broader than the promoted ledger. A promising source can be worth preserving as a research lead before its full object or relevant section has been inspected. Such a lead is not silently upgraded into evidence.

The source hierarchy is intentionally asymmetric:

```text
GREEK SURFACE             -> SBLGNT for open machine-oriented comparison
MORPHOLOGY                -> MorphGNT/SBLGNT
CURRENT CRITICAL TEXT     -> NA28 current edition + GNT6 current 2026 text
DEEP 1 PETER APPARATUS    -> ECM IV Catholic Letters + NTVMR/Liste/manuscript images
LEXICAL SEMANTICS         -> BDAG / Danker / LSJ controls + context
SYNTAX                    -> grammar + major exegetical commentary
PROJECT THEOLOGY          -> TMS doctrinal statement + GTY/MacArthur
EVANGELICAL CONTROLS      -> Schreiner, Jobes, Davids, Grudem, Keener, Carson, Storms
ACADEMIC ADVERSARIAL      -> Horrell/Williams, Achtemeier, Elliott, peer-reviewed studies
HISTORICAL RECEPTION      -> public-domain Leighton/Lillie/Calvin/Brown/Bigg/Hort etc.
PEDAGOGY                  -> retrieval, spacing, feedback, successive relearning
```

## 2. NA28 / NA29 / GNT6 — exact current-state decision

As of 2026-08-14:

- **NA28 is still the current published Nestle–Aland edition.**
- The official Deutsche Bibelgesellschaft listing gives **NA29 a release date of 2027-02-28**.
- **GNT6 is already available in 2026**, and DBGS states that its Greek text is identical to the forthcoming NA29 text.
- GNT6 incorporates new ECM main-text work for Acts, Mark, and Revelation and includes additional papyri P128–P141 in its witness selection.
- For **1 Peter**, the crucial point is that the Catholic Letters were already revised from the ECM in NA28. INTF records 33 textual changes for the Catholic Letters relative to NA27 that were adopted in NA28. Therefore, buying/awaiting NA29 is not a reason to pretend that 1 Peter's main text has suddenly become obsolete.

Project consequence:

```text
BOT_OPEN_GREEK_BASE = SBLGNT + MorphGNT
TEXT_CRITICAL_REVIEW = NA28/GNT6 + ECM IV + NTVMR
NA29_STATUS = FORTHCOMING_EDITION
NA29_TEXT_STATUS = AVAILABLE_NOW_VIA_GNT6
1_PETER_ECM_STATUS = ALREADY_REFLECTED_IN_NA28
```

Do not simplify this to "NA29 is already published" or "NA28 is useless".

## 3. Manuscript strategy

Do not build a hand-curated pseudo-apparatus from a few famous codices. Use:

1. ECM IV for the Catholic Letters as the apparatus authority.
2. NTVMR / Kurzgefasste Liste for registered witnesses, metadata, images/transcriptions.
3. Individual high-value witnesses for teaching visual manuscript literacy.

Initial 1 Peter visual anchors include:

- **P72 (Bodmer VII–VIII)** — third/fourth century; substantial Catholic Epistles witness with indexed 1 Peter images.
- **P81** — fourth-century fragmentary witness including portions of 1 Peter.
- **Codex Sinaiticus (01)** — official manuscript portal for a major fourth-century witness.

A future manuscript question should usually ask something teachable such as how an apparatus or witness works, not make students memorize arbitrary sigla.

## 4. BDAG and Greek semantics

BDAG is a core paid lexical authority, not a source we are free to copy into the repository or bot. The bot should:

- store lemma + passage + claim we need to verify;
- consult BDAG legally for sense/range;
- paraphrase the result in our own learner-facing language;
- corroborate non-trivial syntax/semantics with a serious commentary or grammar;
- never use "BDAG says X" as a substitute for contextual exegesis;
- never copy long copyrighted definitions.

Danker’s *Concise Greek-English Lexicon* is especially useful as a bridge from specialist lexicography to explanations ordinary users can understand, but it is also copyrighted.

`01_GREEK_TEXT_MANUSCRIPTS_AND_LEXICA.md` contains a 40-lemma priority queue for 1 Peter.

## 5. TMS position and independent controls

The course theology is anchored close to **The Master's Seminary**:

- grammatical-historical interpretation;
- substitutionary atonement;
- the church begins at Pentecost;
- church and Israel are not collapsed into one undifferentiated entity;
- pretribulational/premillennial eschatology;
- future earthly messianic kingdom and fulfillment of promises to Israel.

This is a **project-position layer**, not a trick by which every verse is forced to answer a systematic-theology question.

Thomas Schreiner remains a high-value exegete. TMS currently lists him as a D.Min guest lecturer, which is useful context, but it does not mean TMS and Schreiner are identical on every theological question. The course may use Schreiner strongly on grammar/context while explicitly retaining TMS as the project anchor where broader systems diverge.

## 6. Fee and Carson

No dedicated verse-by-verse Gordon Fee commentary on 1 Peter was established in this wave. Fee/Stuart are therefore classified as **hermeneutics**, especially valuable because their method is written for readers from ordinary church settings through seminary students.

D. A. Carson contributes in two different roles:

- a substantial freely readable exposition of 1 Peter 1:1–12;
- the 1 Peter treatment in the Beale/Carson *Commentary on the New Testament Use of the Old Testament*, useful for OT/intertext work.

Neither author should be cited as though he wrote a complete modern 1 Peter commentary when he did not.

## 7. Large legal/open historical works

Useful 150+ page historical/reception candidates include:

- John Lillie, *Lectures on the First and Second Epistles of Peter* — 500+ pages.
- John Brown, *Expository Discourses on First Peter* — about 800 pages.
- Charles Bigg, ICC *Peter and Jude* — 350+ pages.
- F. J. A. Hort, *The First Epistle of St Peter I.1–II.17* — about 190 pages.
- Robert Leighton, *Practical Commentary upon First Peter* — large public-domain editions.
- Calvin, *Commentaries on the Catholic Epistles* — public-domain full text.
- William Ames, *Analytical Exposition of Both Epistles of Peter* — public-domain historical source.

These are excellent for historical exegesis, devotional/pastoral reception, and sometimes older Greek observations. They do **not** outrank ECM, modern lexica, papyri, or current social-historical work simply because the PDF is large.

## 8. Rights / Drive decision

A Google Drive folder was created for this corpus, but this wave intentionally does **not** mirror modern copyrighted books.

Use Drive when:

- an open/public-domain object may disappear and durable custody has value;
- exact bytes/pages must be pinned for later quote verification;
- rights status is clear enough for storage.

Do not use Drive merely to duplicate a stable public web page. `DRIVE_PRESENCE != RIGHTS`.

## 9. Bot implications already supported by learning science

The course should not become "seminary trivia". The same evidence can feed multiple levels:

```text
LEVEL 1 — SIMPLE:
what the verse says; people, actions, argument, memorable anchor

LEVEL 2 — STANDARD:
context, OT background, one key Greek observation, why distractors are wrong

LEVEL 3 — DEEP:
morphology, syntax, intertext, manuscript/text-critical issue, competing interpretations

LEVEL 4 — RESEARCH:
source comparison, disputed-passage map, apparatus/manuscript literacy
```

Learning features with good empirical support include retrieval practice, spaced review, successive relearning, corrective feedback, confidence calibration, adaptive return of missed/low-confidence material, concise distractor explanations, and selective free recall. The exact interval schedule remains a product hypothesis to validate with bot data rather than a claim proved by one paper.

## 10. High-priority next research targets

1. Claim-level read of Jobes 2nd ed. on all of 1 Peter, especially Greek/LXX notes.
2. Claim-level read of Keener on social background and 3:18–22.
3. Direct Davids and Schreiner page-level comparison for disputed passages.
4. Full Crawford article before any exclusive `ἐπερώτημα` proposal.
5. ECM/NTVMR apparatus review of actual 1 Peter textual variants selected for the bot.
6. Build a verse-by-verse OT/LXX map for chapters 1–5.
7. Build a project-theology matrix: direct text vs TMS synthesis vs disputed interpretation.
8. Add a rights-verified acquisition ledger before any public-domain scan is copied to Drive.
9. Convert the 40-lemma Greek queue into claim cards with exact sense/grammar locators.
10. Use learning-science findings to design spaced review and confidence-aware mastery, not just more questions.

## Boundary

```text
SOURCE_FOUND != CLAIM_PROVED
ABSTRACT != FULL_TEXT
CATALOG_RECORD != BOOK_READ
DISCOVERY_INDEX != PROMOTED_CORE_LEDGER
PROJECT_POSITION != NEUTRAL_FACT
MORPHOLOGY != EXEGESIS
OLD_COMMENTARY != CURRENT_TEXTUAL_CRITICISM
DRIVE_OBJECT != PUBLICATION_RIGHTS
RESEARCH_BRANCH != BOT_PRODUCTION
```
