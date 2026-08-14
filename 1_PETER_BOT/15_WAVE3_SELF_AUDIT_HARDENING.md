# 1 Peter Wave 3.0b — Post-validator evidence hardening

**Status:** `CURRENT SUPPLEMENT / RESEARCH ONLY / NOT BOT PRODUCTION / NOT RANKING`

This supplement records findings from a manual content/evidence audit performed **after** Wave 3.0 had already passed the repository authority validator. It is intentionally additive: the original Wave 3.0 snapshot remains visible, while the machine candidate chunks and source ledger are corrected in the same commit as this file.

For the IDs and sources listed below, this supplement plus the current machine JSON files control over the earlier descriptive Wave 3.0 prose.

## Why this pass exists

A green structural validator cannot prove that every historical, lexical, or editorial claim has enough evidence. The post-validator audit therefore re-read the 90 candidates looking for:

- history claims backed only by the biblical text;
- interpretation claims whose source depth was weaker than the wording;
- mixed-script Unicode corruption in Greek;
- later technical meanings being read back into first-century vocabulary;
- one-background intertext/imaging certainty;
- application claims that needed reception/history control.

Rule:

```text
GREEN_VALIDATOR != EDITORIAL_OR_EVIDENCE_APPROVAL
SELF_AUDIT_FINDING -> FIX_OR_HOLD
```

## Candidate corrections

### `w3q_022` — 1 Peter 4:9 hospitality

Old weakness: the history candidate claimed broad early-Christian mission/economic background from SBLGNT alone.

Current boundary:
- the text establishes mutual hospitality without grumbling;
- Jennifer Strawbridge's peer-reviewed 2025 study places 4:9 inside 1 Peter's network of love, kinship, hospitality, and solidarity;
- exact lodging systems, missionary logistics, and economic duties of the original congregations remain reconstruction.

The question is still `history / medium / READY_NONCOMPETITIVE`.

### `w3q_035` — Χριστιανός and persecution dating

Christopher Byrley's full SBJT 21.3 (2017), 77–98 web article was inspected. Byrley surveys older Nero/Domitian/Trajan empire-wide dating models, the later local/social hostility model, and a median view that retains legal/violent threat.

Current question tests only this safe distinction:

> the label Χριστιανός is historical evidence, but it does not by itself choose one official empire-wide persecution regime or an exact date for the letter.

Byrley's own preferred persecution model remains one scholarly proposal, not consensus.

### `w3q_047` — Unicode integrity

Corrected mixed-script typo:

`μάрτυς` -> `μάρτυς`

The former form contained a Cyrillic `р` inside a Greek word. This was an editorial defect that the structural validator did not catch.

### `w3q_083` — kiss of love application

Strawbridge's article and Oxford's official repository record were inspected. Oxford identifies the article as peer reviewed and CC BY 4.0.

Relevant bounded result:
- 1 Peter's kiss of love functions in the field of embodied reconciliation, unity, hospitality, and solidarity;
- early Christian reception developed restrictions and ritual around kissing;
- therefore ancient seriousness does not prove that one unchanged physical greeting form is mandatory in every modern culture.

The candidate remains `application / project / medium / READY_NONCOMPETITIVE`.

### `w3q_084–085` — ποιμάνατε / κλήρων

Exact NET notes on 1 Peter 5:2–3 were inspected.

Safe bounded uses:
- the participles in 5:3 continue the shepherding command of 5:2 by describing how it is carried out;
- `τῶν κλήρων` is explained contextually as “the ones allotted,” those entrusted to the elders' care.

This does **not** replace the ECM apparatus for `ἐπισκοποῦντες`, and it does not provide a complete diachronic lexical history of `κλῆρος`.

### `w3q_088` — roaring lion background

Two controls now prevent a fake single-source certainty:

1. Byrley 2017 — full web article inspected; treats 5:8 in a broader cosmic-conflict/persecution framework and engages multiple lion-background proposals.
2. Tyler Hallstrom, JETS 65.3 (2022) — publisher abstract/opening inspected only; explicitly compares Jewish and Greco-Roman backgrounds and argues against highly particularized one-background interpretations.

Current candidate therefore asks whether one specific OT text must sit behind the roaring lion. The keyed concept is **no**: the text names the metaphor, while exclusive source identification requires additional evidence.

Hallstrom's detailed full-article argument remains subscription HOLD.

## New Wave 3 source controls

The Wave 3 source ledger grows from **14 to 18** bounded sources:

- `w3_byrley_adversary_2017` — full Southern Equip web article inspected; `FULL_OBJECT_VERIFIED`; rights unknown;
- `w3_hallstrom_lion_2022` — abstract/opening only; full body subscription HOLD;
- `w3_strawbridge_kiss_2025` — relevant publisher text + official Oxford rights record; CC BY 4.0;
- `w3_net_1p5_3` — exact NET 5:2–3 notes inspected; translation control, not ECM substitute.

## HOLD count

The canonical bank remains:

- **90 total candidates**;
- **45 Chapter 4 / 45 Chapter 5**;
- **46 READY**;
- **37 READY_NONCOMPETITIVE**;
- **7 HOLD**.

No HOLD was silently promoted merely because more secondary material was found.

The seven HOLDs remain:

1. final project position on 4:6;
2. 4:14 Spirit/glory apparatus unit;
3. 4:16 `ὀνόματι / μέρει`;
4. final Malachi-3 closure for 4:12–19;
5. 5:2 `ἐπισκοποῦντες`;
6. 5:2 `κατὰ θεόν`;
7. 5:12 `στῆτε / ἑστήκατε`.

## Publication boundary

```text
QUESTION_CANDIDATE_READY != PRODUCTION_READY
FULL_WEB_ARTICLE_INSPECTED != CONSENSUS
ABSTRACT_INSPECTED != FULL_ARTICLE_INSPECTED
TRANSLATION_NOTE != CRITICAL_APPARATUS
CC_BY != CURRENT_TEXTUAL_AUTHORITY
```

All Wave 3 candidates remain `competitive_candidate=false`.