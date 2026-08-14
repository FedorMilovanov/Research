# 1 Peter Wave 3n — Final ECM-Quality Textual Closure

**Date:** 2026-08-14  
**Status:** `RESEARCH CLOSURE / ZERO CANDIDATE HOLDS / NOT PRODUCTION / NOT RANKING`

Wave 3n closes the four textual-critical HOLDs left by Wave 3l **without relaxing the closure criterion**.

The prior rule allowed closure by either:

1. direct current ECM/dECM unit readback; or
2. a sufficiently explicit current scholarly textual-critical treatment anchored in ECM data.

This wave uses the second route. It does **not** claim a direct dECM witness-table readback where one was not obtained.

## New evidence quorum

### Williams–Horrell, ICC 2023

Travis B. Williams and David G. Horrell, *1 Peter: A Critical and Exegetical Commentary, Volume 2: Chapters 3–5* (ICC; T&T Clark, 2023) is the principal current passage-level control.

The publisher describes the volume as providing dedicated text-critical notes for each passage. The authors explicitly state that their textual work benefits from the ECM Catholic Letters and CBGM.

For the four remaining units:

- **4:14** — the commentary maps the ancient `δύναμις` expansion, explicitly points to **ECM 182**, and prefers the shorter reading. The reasoning does not deny the antiquity of the expansion; it treats the variable expansion forms as secondary.
- **5:2 / `ἐπισκοποῦντες`** — the commentary explicitly points to **ECM 188–189**, discusses important omission witnesses and widespread inclusion, and on balance retains the participle.
- **5:2 / `κατὰ θεόν`** — the commentary treats this as a separate variation problem, not as part of a single binary package with `ἐπισκοποῦντες`, and prefers retaining the phrase.
- **5:12 / `στῆτε`** — the commentary prefers the aorist imperative `στῆτε` over the later majority perfect-indicative form, using both external and internal reasoning. It explains the declarative reading as an intelligible scribal smoothing of the harder imperative-in-relative-clause construction.

This source remains copyrighted. The corpus records only bounded claims and metadata; it does not mirror or republish the commentary.

## Independent ECM comparison control

Jovan Stanojević, *Orthodox New Testament Textual Scholarship: Antoniades, Lectionaries, and the Catholic Epistles* (Gorgias Press, 2021) supplies an independent published comparison of the Antoniades text with the ECM Catholic Epistles.

The relevant published collation records include:

- `1 Pet 4:14/21` — ECM side omits the `καὶ δυνάμεως` expansion represented in Antoniades;
- `1 Pet 5:2/26–28` — ECM side includes `κατὰ θεόν`, while Antoniades omits it;
- `1 Pet 5:12/46` — ECM side reads `στῆτε`, while Antoniades has the perfect form.

This is especially important for 5:12: the closure is no longer merely "a modern commentary prefers `στῆτε`". The exact ECM comparison address is independently published, while Williams–Horrell supply the textual reasoning.

## HOLD transitions

### `HOLD-TC-4-14` / `w3q_031`

```text
HOLD -> READY_NONCOMPETITIVE
```

Teach:

- the short current critical reading is preferred;
- the power expansion is a real ancient variant;
- textual preference does not erase reception history.

Do not teach:

- "one old manuscript proves the text";
- "the expansion is meaningless";
- a doctrinal conclusion from the mere presence/absence of `δύναμις`.

### `HOLD-TC-5-2A` / `w3q_050`

```text
HOLD -> READY_NONCOMPETITIVE
```

Teach:

- `ἐπισκοποῦντες` has serious omission evidence;
- ECM-based current treatment nevertheless prefers retention;
- textual closure is distinct from a full ecclesiological/polity conclusion.

### `HOLD-TC-5-2B` / `w3q_051`

```text
HOLD -> READY_NONCOMPETITIVE
```

Teach:

- `κατὰ θεόν` varies independently of `ἐπισκοποῦντες`;
- current ECM-aligned evidence supports retention;
- the two 5:2 units must remain separately addressable in authoring/tests.

### `HOLD-TC-5-12` / `w3q_075`

```text
HOLD -> READY_NONCOMPETITIVE
```

Teach:

- the current critical line is `στῆτε`;
- the perfect indicative is a genuine and historically influential variant;
- the preference rests on textual evidence and transmissional/intrinsic reasoning, not raw witness counting.

## Effective corpus after Wave 3n

```text
TOTAL = 144
CHAPTER_4 = 72
CHAPTER_5 = 72
READY = 52
READY_NONCOMPETITIVE = 92
HOLD = 0
COMPETITIVE_CANDIDATES = 0
```

The 64 MCQ research prototypes remain unchanged:

```text
CHAPTER_4 = 32
CHAPTER_5 = 32
CORRECT_0 = 16
CORRECT_1 = 16
CORRECT_2 = 16
CORRECT_3 = 16
```

No new competitive authorization is created by resolving a research HOLD.

## Effective-record rule

The resolution chain now includes Wave 3n:

```text
BASE_CANDIDATE
-> LATER_CANDIDATE_OVERRIDE (including Wave 3n)
-> SOURCE_UPGRADE_OR_QUORUM (including Wave 3n)
-> MCQ_PROTOTYPE
-> MCQ_EDITORIAL_OVERRIDE
```

Old Wave-3l files remain immutable historical evidence of what was unresolved at that checkpoint. Consumers must not resurrect those historical HOLDs after applying later overrides.

## Governance boundary after zero HOLD

```text
ZERO_RESEARCH_HOLDS != PRODUCTION_READY
ZERO_RESEARCH_HOLDS != COMPETITIVE_READY
ZERO_RESEARCH_HOLDS != PUBLICATION_AUTHORIZED
ECM_TEXT_DECISION != MANUSCRIPT_UNANIMITY
ECM_BASED_COMMENTARY != DIRECT_DECM_READBACK
TEXTUAL_CRITICISM != SYSTEMATIC_THEOLOGY
```

Research Wave 3 can now hand off with **zero candidate-level HOLDs** while preserving every production/ranking/editorial gate.
