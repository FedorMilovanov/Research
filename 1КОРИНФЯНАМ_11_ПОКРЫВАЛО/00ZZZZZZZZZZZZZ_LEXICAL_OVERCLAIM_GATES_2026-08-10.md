# Lexical overclaim gates — 1 Кор 11:2–16

**Дата:** 2026-08-10  
**Статус:** `FAIL-CLOSED / LEXICAL-GATES / RESEARCH-ONLY`

This file is a validator-facing checklist for future agents and article drafts.

## Gate 1 — omitted object in v4

Forbidden:

```text
κατὰ κεφαλῆς ἔχων = literally “wearing a veil”
```

Required distinction:

```text
κατὰ κεφαλῆς = down/over/from the head
ἔχων = having
object = contextually supplied
material covering = B_HIGH, not an overt noun in v4
```

## Gate 2 — cover vocabulary vs hair vocabulary

Do not collapse:

```text
κατακαλύπτω / ἀκατακάλυπτος
=
κομάω / κόμη
```

The first lexical field is cover/uncover; the second explicitly long hair/hair.

A hair-only model is allowed as C, but must pay this lexical burden.

## Gate 3 — `κεφαλή`

Forbidden absolutes:

```text
κεφαλή never carries leadership/prominence
κεφαλή always lexically means authority over
κεφαλή simply means source because v8 says woman is from man
```

Controls:

- Judges 11:11 gives `κεφαλή` alongside leader/chief language;
- Isaiah 7:8–9 gives relational/prominence head metaphors;
- v8 origin uses explicit `ἐκ` and is contextual evidence, not a dictionary definition.

Project:

```text
KEPHALE_HEADSHIP_AUTHORITY = B_LEADING
KEPHALE_SOURCE_ONLY = C_VIABLE
```

## Gate 4 — man/husband; woman/wife

Both senses are lexical for both nouns.

Forbidden:

```text
γυνή can only mean wife
γυνή can only mean woman
ἀνήρ can only mean husband
ἀνήρ can only mean man
```

Context must decide token-by-token; the whole addressee question remains `OPEN_B_C`.

## Gate 5 — `ἐξουσίαν ἔχειν`

Mandatory syntactic fact:

```text
ἡ γυνή = grammatical subject
ἐξουσίαν ἔχειν = what she is obliged to have
```

Pauline controls:

- 1 Cor 9:4 — subject has a right;
- 1 Cor 7:37 — subject has authority concerning his own will.

Wider controls with `ἐπί`:

- Matt 9:6;
- Rev 11:6.

Forbidden as a literal translation claim:

```text
ἐξουσία = “sign of her husband’s authority over her”
```

That reading may be argued contextually, but it supplies “sign” and an external authority-holder.

## Gate 6 — `φύσις`

Paul’s corpus blocks both reductions:

```text
φύσις = biology only
φύσις = arbitrary social convention only
```

Relevant Pauline uses include Rom 1:26; 2:14; 11:24; Gal 2:15.

Use:

```text
PHYSIS_SEXED_NATURALIZED_PROPRIETY = B_LEADING
EXACT_BIOLOGY_CULTURE_MIX = B_C
```

## Gate 7 — `περιβόλαιον`

Independent controls:

- Deut 22:12 LXX — wrap-around garments;
- Ps 101:27 LXX — parallel with `ἱμάτιον`;
- Heb 1:12 — mantle/garment imagery.

Thus normal lexical class is wrapping/covering/garment.

Forbidden:

```text
περιβόλαιον normally means testicle
```

Any ancient-physiology theory must be presented as a specialized reconstructive metaphor (`D/C-low`), not lexicon.

## Gate 8 — `ἀντί`

`ἀντί` supports substitution/exchange/correspondence relations.

It does not independently decide whether hair:

- replaces all external covering;
- analogically corresponds to an external covering;
- functions as a natural sex-differentiating counterpart.

Forbidden:

```text
ἀντί alone proves hair-only
ἀντί alone proves two-covering model
```

## Gate 9 — discourse connectors

Mandatory:

```text
διὰ τοῦτο v10 = inferential/anaphoric relation to prior argument
πλὴν v11 = qualification/transition
ὥσπερ ... οὕτως v12 = reciprocal comparative structure
```

Forbidden:

```text
πλὴν itself proves that Paul has switched from quoting Corinthians to his own voice
```

Quotation/refutation remains a structural hypothesis, not a lexical fact.

## Gate 10 — article drafting language

Use:

- “лексически допускает”;
- “синтаксис требует”;
- “корпус сильно поддерживает”;
- “контекстуально ведущее чтение”;
- “интерпретация добавляет невысказанный шаг”.

Avoid:

- “в греческом буквально написано X” when X is supplied;
- “это слово всегда означает X” without corpus proof;
- “словарь решил спор”.

## Publication boundary

```text
PRODUCT_WRITE = false
UI_IMPLEMENTATION = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
```
