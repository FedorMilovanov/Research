# 1 Коринфянам 11:2–16 — Pauline quotation/slogan corpus control

**Дата:** 2026-08-10  
**Статус:** `PRIMARY-CORPUS / QUOTATION-BOUNDARY / ADVERSARIAL-CONTROL / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Question

Recent real scholarship (Shoemaker, Costa, Salés) makes a large Corinthian quotation/refutation model a genuine published minority family. The decisive next question is not whether scholars advocate it, but whether **Paul’s own quotation/slogan practice inside 1 Corinthians** supplies a close structural analogue for assigning vv4–9 or vv3–10 to a Corinthian voice without an explicit frame.

This audit therefore distinguishes:

```text
CAN_PAUL_QUOTE/REUSE_CORINTHIAN_WORDING_WITHOUT_MODERN_QUOTATION_MARKS? = YES
DOES_ABSENCE_OF_EXPLICIT_QUOTATIVE_FORMULA_BY_ITSELF_REFUTE_A_QUOTATION? = NO
DO_SHORT_DISPUTED_SLOGANS_PROVE_A_LONG_UNMARKED_BLOCK? = NO
QUOTE_EXISTENCE != QUOTE_BOUNDARY_CERTAINTY
SCHOLARLY_ADVOCACY != PRIMARY_CORPUS_PARALLEL
```

Primary Greek control route throughout:

- Deutsche Bibelgesellschaft NA28: https://www.die-bibel.de/bibel/NA28/1CO.1

Modern punctuation is editorial. The argument below does **not** treat quotation marks or punctuation in NA28 as manuscript characters.

---

# 1. Explicitly framed opponent speech exists in the same letter

## 1.1 1 Corinthians 1:12

Paul introduces the factional claims with an explicit speech frame:

```text
λέγω δὲ τοῦτο ὅτι ἕκαστος ὑμῶν λέγει·
```

followed by short first-person statements such as “I am of Paul / Apollos / Cephas / Christ.”

Minimum result:

```text
PAUL_CAN_EXPLICITLY_FRAME_CORINTHIAN_SPEECH = A_TEXT
```

This does not imply he must always do so.

Official route:

- https://www.die-bibel.de/bibel/NA28/1CO.1

## 1.2 1 Corinthians 15:12

Paul again explicitly attributes a proposition to some Corinthians:

```text
πῶς λέγουσιν ἐν ὑμῖν τινες ὅτι ἀνάστασις νεκρῶν οὐκ ἔστιν;
```

The following argument answers that proposition.

```text
EXPLICIT_OPPONENT_PROPOSITION_FRAME_IN_1COR = A_TEXT
```

Official route:

- https://www.die-bibel.de/bibel/NA28/1CO.15

These cases establish a same-letter control: Paul possesses clear quotative/attribution mechanisms when he explicitly identifies another voice.

---

# 2. 1 Corinthians 7:1 — source-frame is explicit, exact quotation boundary is not

Paul writes:

```text
Περὶ δὲ ὧν ἐγράψατε,
καλὸν ἀνθρώπῳ γυναικὸς μὴ ἅπτεσθαι·
```

The phrase `περὶ δὲ ὧν ἐγράψατε` explicitly signals a topic coming from the Corinthians’ letter.

But whether the immediately following maxim `καλὸν ... μὴ ἅπτεσθαι` is itself a verbatim Corinthian quotation remains interpretive.

Thus:

```text
LETTER_SOURCE_FRAME_7_1 = A_TEXT
EXACT_VERBATIM_QUOTATION_BOUNDARY_7_1 = INTERPRETIVE
```

This is a useful caution against both extremes:

- source framing can be explicit while wording ownership remains debated;
- source framing is stronger evidence than simply finding a difficult or ideologically tense proposition.

Official route:

- https://www.die-bibel.de/bibel/NA28/1CO.7

---

# 3. 1 Corinthians 6:12–13 — the classic “unmarked slogan” control is itself disputed

## 3.1 Primary sequence

The text contains short, aphoristic formulations:

```text
Πάντα μοι ἔξεστιν
ἀλλ’ οὐ πάντα συμφέρει·
Πάντα μοι ἔξεστιν
ἀλλ’ οὐκ ἐγὼ ἐξουσιασθήσομαι ὑπό τινος.
```

and in v13:

```text
Τὰ βρώματα τῇ κοιλίᾳ
καὶ ἡ κοιλία τοῖς βρώμασιν ...
```

Official route:

- https://www.die-bibel.de/bibel/NA28/1CO.6

These are among the most commonly proposed Corinthian slogans. Yet their attribution and exact boundaries remain debated in peer-reviewed scholarship.

## 3.2 Dodd 1996 — even 6:12 ownership is contested

Brian J. Dodd, “Paul’s Paradigmatic ‘I’ and 1 Corinthians 6.12,” *Journal for the Study of the New Testament* 18.59 (1996).

SAGE abstract/search apparatus presents Dodd as challenging the consensus that 6:12 is a Corinthian slogan and arguing that the first-person formulation may be Paul’s own paradigmatic rhetoric.

Route:

- https://journals.sagepub.com/doi/10.1177/0142064X9601805902

Safe result:

```text
UNMARKED_SLOGAN_6_12 = SERIOUS_BUT_DISPUTED_ATTRIBUTION
SHORT_APHORISTIC_FORM != CORINTHIAN_OWNERSHIP_PROVEN
```

## 3.3 Burk 2008 — discourse criteria can support slogan identification, but boundaries still require argument

Denny Burk, “Discerning Corinthian Slogans through Paul’s Use of the Diatribe in 1 Corinthians 6:12–20,” *Bulletin for Biblical Research* 18.1 (2008): 99–121.

Burk argues from diatribal/discourse structure for slogans in vv12, 13 and 18. The article explicitly engages the methodological problem of how interpreters identify slogans and quotation boundaries.

DOI: `10.2307/bullbiblrese.18.1.0099`.

This shows:

```text
UNMARKED_QUOTATION_CAN_BE_ARGUED_FROM_DISCOURSE = true
BUT
DISCOURSE_CRITERIA_MUST_BE_SHOWN_PASSAGE_BY_PASSAGE = true
```

## 3.4 Murphy-O’Connor differs again

Jerome Murphy-O’Connor’s published treatment of 6:12–20 identifies a different slogan configuration, including 6:13a and 6:18b.

Oxford route:

- https://academic.oup.com/book/8618/chapter/154572888

The precise disagreement is itself evidentially important:

```text
SLOGAN_MODEL_EXISTS
DOES_NOT_ENTAIL
SLOGAN_BOUNDARIES_ARE_TRANSPARENT
```

---

# 4. 1 Corinthians 10:23 — repeated maxim + immediate Pauline qualification

The phrase from 6:12 recurs:

```text
Πάντα ἔξεστιν
ἀλλ’ οὐ πάντα συμφέρει·
πάντα ἔξεστιν
ἀλλ’ οὐ πάντα οἰκοδομεῖ.
```

Official route:

- https://www.die-bibel.de/bibel/NA28/1CO.10

This is a strong example of a short maxim immediately counterbalanced by `ἀλλά` clauses.

Whatever its original ownership, the form demonstrates a pattern quite different from the proposed vv4–9 quotation:

```text
SHORT_MAXIM
+ IMMEDIATE_ANTITHETICAL_QUALIFICATION
```

not:

```text
MULTI_VERSE_EXPLANATORY_BLOCK
+ γάρ / καὶ γάρ chain
+ no local attribution frame
+ later “therefore” connective
```

Therefore 6:12/10:23 cannot simply be cited as a structural parallel proving a six- or eight-verse unmarked quotation.

---

# 5. 1 Corinthians 8:1,4 — “we know” formulas show shared/cited language can be difficult to allocate

The chapter contains formulations such as:

```text
οἴδαμεν ὅτι πάντες γνῶσιν ἔχομεν
```

and:

```text
οἴδαμεν ὅτι οὐδὲν εἴδωλον ἐν κόσμῳ ...
```

Official route:

- https://www.die-bibel.de/bibel/NA28/1CO.8

Scholars have variously treated such phrases as shared knowledge, Corinthian slogans, Pauline concessions, or language Paul adopts and qualifies.

The primary control is therefore methodological:

```text
SHARED_FIRST_PERSON_PLURAL_FORMULA != AUTOMATIC_EXTERNAL_QUOTE
PAUL_CAN_APPROPRIATE_AND_QUALIFY_SHARED_LANGUAGE = PLAUSIBLE
```

This again warns against equating ideological tension with a secure new speaker.

---

# 6. Methodological literature confirms the boundary problem is real

## 6.1 Roger Omanson

Roger L. Omanson, “Acknowledging Paul’s Quotations,” *The Bible Translator* 43 (1992): 201–213.

His work became a standard methodological control precisely because interpreters often propose Corinthian quotations without clearly articulating their identification criteria.

Use here:

```text
QUOTE_BOUNDARY_MUST_BE_JUSTIFIED_EXPLICITLY = METHODOLOGICAL_CONTROL
```

## 6.2 Watson & Culy 2018

Duane Watson and Martin Culy, *Quoting Corinthians: Identifying Slogans and Quotations in 1 Corinthians* (Pickwick, 2018).

Publisher description presents this as a book-length attempt to develop objective criteria for identifying quotations/slogans and apply them to eleven passages.

Official route:

- https://wipfandstock.com/9781532618437/quoting-corinthians/

Their very project cuts both ways:

1. Paul can echo or cite Corinthian material without a modern quotation apparatus;
2. therefore one needs **positive criteria**, not merely “this verse sounds inconsistent with Paul.”

The publication should not be used as a blanket authorization for every proposed quotation boundary.

## 6.3 Paul A. Holloway 2021

Paul A. Holloway, “Religious ‘Slogans’ in 1 Corinthians: Status Markers, Sophistic Values, and Theological Conflict,” *Journal of Theological Studies* 72.1 (2021): 125–154.

Oxford abstract distinguishes slogan-like maxims coined by rival teachers from other formulations plausibly coined by Paul himself in response to competitors.

Route:

- https://academic.oup.com/jts/article/72/1/125/6151684

This directly reinforces:

```text
SLOGAN_LIKE_FORM != OPPONENT_OWNERSHIP_AUTOMATIC
```

---

# 7. Primary-corpus comparison with 1 Corinthians 11:4–10

The proposed quotation block contains a dense explanatory sequence:

```text
v4 male praying/prophesying ...
v5 female praying/prophesying ...
v6 εἰ γὰρ ...
v7 οὐ γὰρ ...
v8 οὐ γάρ ...
v9 καὶ γάρ ...
v10 διὰ τοῦτο ...
```

The current project already grades the local connection:

```text
DIA_TOUTO_V10_LINKS_BACKWARD = A_DISCOURSE
```

In this audit, the inspected same-letter controls produce two broad classes:

### Class A — clearly attributed external/opponent speech

- 1:12 — explicit `ἕκαστος ... λέγει` frame;
- 15:12 — explicit `λέγουσιν ... τινες ὅτι` frame;
- 7:1 — explicit source/topic frame `περὶ δὲ ὧν ἐγράψατε`, though exact verbatim extent remains debated.

### Class B — proposed unmarked slogans/shared maxims

- 6:12;
- 6:13;
- 8:1 / 8:4;
- 10:23;
- other proposed short units.

These Class B examples are typically short/gnomic and their **ownership or boundaries are themselves contested**.

### Crucial negative result

Within the directly inspected controls in this pass, **no close same-letter parallel was verified** for:

```text
6–8 VERSES OF HOSTILE/OPPONENT SPEECH
WITHOUT A SOURCE/QUOTATIVE FRAME
WITH INTERNAL EXPLANATORY γάρ / καὶ γάρ COHESION
FOLLOWED BY PAUL'S OWN διὰ τοῦτο AS THE RESPONSE PIVOT
```

This is a bounded research result, not a universal impossibility claim:

```text
NO_CLOSE_PARALLEL_FOUND_IN_THIS_AUDIT != PAUL_COULD_NEVER_DO_IT
```

But it materially raises the burden of proof for Costa’s vv4–9 and Salés’s vv3–10 boundaries.

---

# 8. What this does to Costa / Shoemaker / Salés

## 8.1 What remains valid

```text
PAUL_CAN_REUSE/QUOTE_CORINTHIAN_LANGUAGE = TRUE
UNMARKED_SLOGAN_HYPOTHESES_ARE_REAL_SCHOLARSHIP = TRUE
ABSENCE_OF_EXPLICIT_FORMULA_ALONE_DOES_NOT_DISPROVE_QUOTATION = TRUE
```

Thus a simplistic rebuttal — “there are no quotation marks, therefore impossible” — is rejected.

## 8.2 What becomes harder

The quotation family still needs to explain simultaneously:

1. why the proposed block is much longer and more internally argumentative than the safest slogan parallels;
2. why there is no local attribution/source frame comparable to 1:12, 7:1 or 15:12;
3. why advocates disagree over the boundary (`vv4–9` Costa; `vv3–10` Salés; other spans in other authors);
4. why `διὰ τοῦτο` at v10 naturally follows the immediately preceding `γάρ` chain if those verses are rejected Corinthian material;
5. why `πλὴν` at v11 should signal a speaker switch rather than an internal qualification;
6. why repunctuation/reanalysis of vv13–15 should be preferred to the continuous reading;
7. how v2’s apostolic-tradition frame and v16’s translocal closure fit the speaker-allocation model.

## 8.3 Grade reconciliation

This primary-corpus pass strengthens the existing dual-axis result:

```text
LARGE_QUOTATION_PUBLISHED_SCHOLARLY_FAMILY = C_SERIOUS / MULTIPLE_B1
LARGE_QUOTATION_TEXTUAL_FIT = D_C_LOW
LARGE_QUOTATION_LEADING_MODEL = false
```

The previous adversarial delta used `D_C_LOW_TO_C_LOW` as a cautious range. After same-letter quotation/slogan controls, there is **no basis for promotion above the current registry’s D/C-low textual-fit grade**.

This is not because the model lacks serious advocates. It is because no close primary-corpus analogue was verified for its required **length + cohesion + boundary + connective structure**.

---

# 9. Strongest alternative to quotation remains a continuous argument with internal counterbalance

Two real modern models demonstrate that one need not choose between “flat hierarchy” and “different speaker”:

- Jill E. Marshall 2019 — Paul modifies different inherited traditions (hierarchical v3; interdependent vv11–12);
- Julie Newberry 2019 — Paul himself can move from patriarchal vv7–9 through woman’s authority v10 to interdependence vv11–12.

These continuous models fit the primary discourse sequence without requiring a hidden speaker boundary.

That does not prove either model in every detail, but it weakens the claim that internal tension **requires** a Corinthian quotation.

---

# 10. Publication-safe conclusion

Safe formulation:

> Paul demonstrably quotes or answers Corinthian speech elsewhere in the letter, and some proposed slogans may be unmarked. However, the clearest attributed speech is explicitly framed, while the classic unmarked slogan candidates are short and their ownership/boundaries remain debated. In the directly inspected same-letter corpus, no close parallel was found for treating the internally connected multi-verse argument of 1 Cor 11:4–9 (or 3–10) as hostile Corinthian speech without a source frame. The quotation/refutation model is therefore a genuine published minority reconstruction, but its textual fit remains low and must be argued from positive discourse criteria rather than from theological tension alone.

Do not write:

```text
“Paul never quotes without λέγει” = FALSE/OVERCLAIM
“6:12 proves he can quote six verses unmarked” = NON_SEQUITUR
“7:1 proves every following maxim is verbatim Corinthian” = OVERCLAIM
“ideological inconsistency proves speaker change” = FALSE_METHOD
“no close parallel found” = “impossible in Greek” = FALSE
```

---

# 11. Next decisive checks

The useful next moves are now narrower:

1. direct full Watson & Culy criteria/1 Cor 11 discussion if lawful access becomes available;
2. technical discourse work on `γάρ`, `καὶ γάρ`, `διὰ τοῦτο`, `πλὴν` in embedded/polyphonic discourse;
3. early reception: did any premodern reader independently perceive a Corinthian speaker boundary in vv3–10 or vv4–9?
4. direct current-commentary responses to quotation models (Garland 2025, Fee Revised, Ciampa/Rosner, Thiselton).

Accumulating further advocates without these controls should not alter probability.

---

## Boundary

```text
CORE_GRADE_REVERSALS = 0
LARGE_QUOTATION_TEXTUAL_FIT = D_C_LOW
LARGE_QUOTATION_SCHOLARLY_STATUS = C_SERIOUS_MULTIPLE_B1
PRODUCT_WRITE = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
```
