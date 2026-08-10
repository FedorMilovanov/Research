# 1 Коринфянам 11:2–16 — Lycosura / Massey gender correction overlay

**Дата:** 2026-08-10  
**Статус:** `CORRECTION-OVERLAY / DIRECT-INSCRIPTION / DIRECT-EPIGRAPHY / SUPERSEDES-MALE-SPLIT-OVERCLAIM / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Supersession scope

This file **supersedes only the male-specific Lycosura claims** in:

`00ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ_MASSEY_2015_ANDANIA_LYCOSURA_EPIGRAPHY_FULLTEXT_AUDIT_2026-08-10.md`

Specifically, it supersedes the earlier project shorthand:

```text
LYCOSURA_MALE_HEAD_COVERING_PROHIBITION = DIRECT_EPIGRAPHIC_CONTROL
```

and the related implication that the inscription itself clearly separates:

```text
women -> braided hair
men -> no covering
```

That split is **Massey/Dittenberger’s interpretation**, not an unambiguous statement of the surviving inscription.

All other unaffected findings of the Massey audit remain in force unless separately superseded.

---

# 1. Direct inscription — IG V 2,514

A direct scholarly digital edition from the Centre for the Greek Language exposes the relevant lines of IG V 2,514:

- https://www.greek-language.gr/digitalResources/ancient_greek/anthology/inscriptions/page_079.html

The key sequence is:

```text
μηδὲ τὰς τ[ρί]-
χας ἀμπεπλεγμένας μηδὲ κεκαλυμ-
μένος, μηδὲ ἄνθεα παρφέρην
```

The same edition dates the inscription to the late third / early second century BCE and identifies it as the Despoina sanctuary regulation from Lykosoura.

Its modern Greek translation treats the sequence under the generic sanctuary entrant:

- one is not to enter with hair arranged/bound up;
- nor with the head covered;
- nor decorated with flowers.

It does **not** introduce a separate male subject for `κεκαλυμμένος`.

Safe direct minimum:

```text
LYCOSURA_TEXT_HAS_BRAIDED/BOUND_HAIR_PROHIBITION = A_EPIGRAPHIC
LYCOSURA_TEXT_HAS_KEKALYMMENOS_COVERED_FORM = A_EPIGRAPHIC
LYCOSURA_EXPLICITLY_SAYS_TOUS_ANDRAS = FALSE
LYCOSURA_EXPLICIT_MALE_ONLY_COVERING_PROHIBITION = NOT_IN_TEXT
```

---

# 2. Voutiras 1999 — autopsy-based epigraphic treatment does not adopt the male split

Direct DAI journal PDF:

> Emmanuel Voutiras, “Opfer für Despoina: Zur Kultsatzung des Heiligtums von Lykosura IG V 2, 514,” *Chiron* 29 (1999): 233–250.

Official PDF:

- https://publications.dainst.org/journals/chiron/article/view/972/5339

Voutiras states that the text he prints follows the then-recent autopsy-based edition of Thür/Taeuber, substantially following Leonardos.

He also stresses that vv./lines 9–13 are **elliptical** and must be understood as dependent on an omitted/repeated `μὴ ἐξέστω` from the opening rule.

His German translation of the crucial sequence is generic:

```text
Es ist außerdem nicht erlaubt,
die Haare geflochten oder den Kopf bedeckt zu haben ...
```

That is: it is not permitted to have the hair braided **or the head covered**.

Voutiras does not insert a separate `men` subject.

Therefore:

```text
VOUTIRAS_1999_LYCOSURA_TRANSLATION = GENERIC_ENTRANT_HAIR_OR_HEAD_COVERING_PROHIBITION
VOUTIRAS_MALE_ONLY_COVERING_SPLIT = NOT_ADOPTED
LYCOSURA_LINES_9_13 = ELLIPTICAL_SYNTAX
```

Browser screenshot rendering of the DAI PDF was explicitly attempted on the key pages but returned a cache miss. The parsed publisher PDF text and page locators are direct; pixel verification remains unclosed.

```text
VOUTIRAS_PDF_TEXT = DIRECT
VOUTIRAS_SCREENSHOT = ATTEMPTED_CACHE_MISS
```

---

# 3. What Massey 2015 actually does

Direct JGRChJ PDF:

- https://www.jgrchj.net/volume11/JGRChJ11-4_Massey.pdf

Massey accurately prints the masculine form `κεκαλυμμένος` and notes the gender problem. His male-specific solution, however, comes through **Dittenberger’s expanded paraphrase**.

Massey reports Dittenberger as supplying:

```text
[τοὺς ἄνδρας]
```

before `κεκαλυμμένος` in order to make the covering prohibition apply specifically to men.

Massey then reasons conditionally:

```text
if Dittenberger’s retention ... as applying only to men is correct
```

and from that derives the two-sex split.

This is crucial source calibration:

```text
DITTENBERGER_TOUS_ANDRAS = EDITORIAL/PARAPHRASTIC_SUPPLEMENT
NOT = INSCRIBED_WORDS
MASSEY_MALE_ONLY_LYCOSURA = INTERPRETIVE_INFERENCE
NOT = DIRECT_EPIGRAPHIC_FACT
```

Massey’s stronger later phrasing (“only the men are told not to veil themselves”) should therefore be read as the conclusion of this interpretive chain, not as a literal translation of the inscription.

---

# 4. Karataş 2020 — current specialist sacred-dress literature reads the prohibition without the male split

Aynur-Michèle-Sara Karataş gives a broad specialist synthesis of Greek sanctuary dress codes.

Direct bibliographic/publication controls:

- Aynur-Michèle-Sara Karataş, “Greek Cults and Their Sacred Laws on Dress-code: The Laws of Greek Sanctuaries for Hairstyles, Jewelry, Make-up, Belts, and Shoes,” *Classical World* 113.2 (2020): 147–170. DOI `10.1353/clw.2020.0001`.
- Related broader article: “Greek cults and their sacred laws on dress-codes: The laws of Greek sanctuaries for clothing, colour, and penalties against misbehaviour,” *Revue des Études Anciennes* 122.2 (2020): 445–488, available via Persée.

In the *Classical World* synthesis, the Lykosoura entry in the table is categorized as prohibiting:

```text
gold, rings, shoes, braided hair, and veiled head
```

and the discussion states that IG V 2,514 prohibits braided hair and a veiled head. Karataş also notes generally that many sacred dress laws do not specify gender explicitly and interpreters must infer likely target groups contextually.

Therefore:

```text
KARATAS_2020_LYCOSURA = BRAIDED_HAIR + VEILED_HEAD_PROHIBITIONS
KARATAS_MALE_ONLY_SPLIT = NOT_USED
```

Karataş does not by herself decide the grammar; her importance is that a current specialist epigraphic/dress-code synthesis does **not** treat the male split as self-evident.

---

# 5. Grammatical issue — masculine form is real, male referent is not automatic

The inscription does contain masculine `κεκαλυμμένος`.

But the broader rule also uses generic masculine forms for sanctuary entrants, including `ἔχοντας`, which Massey himself notes is grammatically masculine but likely includes **both men and women**, since both are addressed in the inscription.

Therefore the simple inference:

```text
MASCULINE_GRAMMATICAL_FORM -> BIOLOGICALLY_MALE_ONLY_REFERENT
```

is not safe in this inscriptional context.

The competing possibilities include at least:

1. generic masculine referring to any entrant;
2. abrupt male-specific switch, as Dittenberger/Massey propose;
3. textual/editorial irregularity in an already elliptical/redacted regulation;
4. older emendation to a feminine form (Oepke/Lösch), which Massey rightly notes is not the transmitted form.

Current project calibration:

```text
LYCOSURA_KEKALYMMENOS_GRAMMATICAL_MASCULINE = A_TEXT
LYCOSURA_REFERENT_MALE_ONLY = C_BC_INTERPRETIVE
LYCOSURA_REFERENT_GENERIC_ENTRANT = B_C_VIABLE
EXACT_GENDER_MAPPING = OPEN
```

Do not silently emend the text to feminine. Do not silently insert `[τοὺς ἄνδρας]` either.

---

# 6. What survives from Massey’s Lycosura argument

Several important points remain valuable even after the correction.

### Survives strongly

```text
LYCOSURA_DISCUSSION_SHOWS_HAIR_AND_HEAD_COVERING_CAN_APPEAR_AS_SEPARATE_RULE_ITEMS = A/B_HIGH
ANAPLEKO/AMPEPLEGMENAS != CONVENTIONAL_UNBOUND_HAIR_VERB = STRONG_MASSEY_LEXICAL_CASE
HAIR_RULE != AUTOMATIC_PROOF_OF_HAIR_ONLY_INTERPRETATION = STRONG
```

The inscription itself mentions a hair condition and a covering condition separately, whatever the exact gender mapping.

### Does not survive as direct fact

```text
LYCOSURA_MEN_ALONE_FORBIDDEN_TO_VEIL = NOT_DIRECT
LYCOSURA_WOMEN_THEREFORE_EXPECTED_TO_VEIL = NOT_DIRECT
```

Massey’s inference that women’s veiling may be “logically assumed” loses significant force once the male-only premise is no longer treated as established.

Updated status:

```text
MASSEY_LYCOSURA_WOMEN_VEILED = C_RECONSTRUCTION
LYCOSURA_PROVES_WOMEN_VEILED = FALSE
LYCOSURA_PROVES_WOMEN_UNVEILED = FALSE
```

---

# 7. Larger implication for 1 Cor 11

This correction does **not** reverse the current leading material-covering grade, because that grade is grounded independently in:

- Pauline Greek lexical/idiomatic analysis;
- early material-covering reception;
- Roman male ritual evidence;
- distinct explicit hair vocabulary in vv14–15;
- other comparative sources.

It does, however, remove one overconfident historical bridge.

```text
MATERIAL_COVERING = B_HIGH_LEADING // unchanged
HAIR_ONLY = C_SERIOUS_ALTERNATIVE // unchanged
ROMAN_CAPITE_VELATO_BACKGROUND = A // unchanged
V4_EXACT_CAPITE_VELATO = B_C // unchanged
EXACT_CORINTH_TRIGGER = RECONSTRUCTION_LAYER
```

The correct use of Lykosoura is now:

> a Hellenistic ritual dress code can separately regulate hair arrangement and head covering; exact sex-specific mapping of the covering prohibition is disputed.

That is stronger source hygiene and weaker overclaim.

---

# 8. New no-overclaim rules

```text
LYCOSURA_KEKALYMMENOS_MASCULINE != MALE_ONLY_REFERENT_PROVED
DITTENBERGER_INSERTED_TOUS_ANDRAS != INSCRIPTION_TEXT
MASSEY_MALE_SPLIT = SCHOLARLY_INFERENCE
VOUTIRAS_GENERIC_TRANSLATION = IMPORTANT_ADVERSARIAL_CONTROL
KARATAS_VEILED_HEAD_READING = CURRENT_SPECIALIST_CONTROL
LYCOSURA != PROOF_WOMEN_WERE_VEILED
LYCOSURA != PROOF_WOMEN_WERE_UNVEILED
```

---

# 9. Result

```text
CORE_GRADE_REVERSALS = 0
LYCOSURA_MALE_HEAD_COVERING_PROHIBITION_AS_DIRECT_FACT = SUPERSEDED/REJECTED_OVERCLAIM
LYCOSURA_EXACT_GENDER_MAPPING = OPEN
LYCOSURA_HAIR_AND_COVERING_ARE_DISTINCT_RULE_ITEMS = RETAINED
MASSEY_2015_LYCOSURA_MALE_SPLIT = C_BC_SOURCE_RECONSTRUCTION
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
