# 1 Коринфянам 11:2–16 — Andania / Lycosura direct epigraphy + Massey 2015 owner

**Дата:** 2026-08-14  
**Статус:** `DIRECT-EPIGRAPHY-OWNER / MASSEY-FULLTEXT / ANDANIA-PHI-CGRN / LYCOSURA-CORRECTED / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Authority / self-correction rule

This is the single current owner for the Andania/Lycosura comparative epigraphy.

It preserves three evidence levels separately:

```text
DIRECT_INSCRIPTION_TEXT
MODERN_EPIGRAPHIC_EDITION_TRANSLATION
MASSEY_2015_INTERPRETATION
```

The earlier project shorthand that Lycosura **directly** says `men` are forbidden to cover is superseded inside this owner.

```text
DIRECT_TEXT > EDITORIAL_SUPPLEMENT > MODERN_RECONSTRUCTION
HAIR_RULE != HEADWEAR_RULE
COMPARATIVE_RITUAL_CODE != EXACT_CORINTH_TRIGGER
```

---

# 1. Massey 2015 — direct journal full text

> Preston T. Massey, “Dress Codes at Roman Corinth and Two Hellenic Sites: What do the Inscriptions at Andania and Lycosura Tell Us about 1 Corinthians 11.2–16?” *JGRChJ* 11 (2015): 51–81.

Routes:
- https://www.jgrchj.net/volume11/JGRChJ11-4_Massey.pdf
- https://jgrchj.net/volume11/?mode=abstracts&page=volume11

The journal PDF text was directly inspected. Screenshot rendering was attempted but not successfully completed in the earlier runtime, so pixel/page-image autopsy is not claimed.

```text
MASSEY_2015_PDF = DIRECT_JOURNAL_OBJECT
MASSEY_PDF_TEXT = DIRECTLY_INSPECTED
MASSEY_SCREENSHOT_RENDER = NOT_COMPLETED
```

Massey’s strongest durable methodological point is:

```text
HAIR_STATE != TEXTILE_COVERING_STATE
BRAIDED_PLAITED_HAIR != UNVEILED_HEAD
TEXT_MENTIONS_HAIR != TEXT_CANNOT_ALSO_REGULATE_HEADWEAR
```

His lexical case also strongly challenges the older translation of `ἀναπλέκω` as ordinary “unbound/loose hair”.

---

# 2. Andania — direct PHI/CGRN control

## 2.1 Object and dating

Direct text:
- PHI IG V,1 1390: https://epigraphy.packhum.org/text/31826
- CGRN 222: https://cgrn.ulg.ac.be/file/222/
- DOI `10.54510/CGRN222`

Dating must remain explicit:

```text
PHI_TRADITIONAL_DATE = 92_91_BCE
CGRN_CURRENT_PREFERRED_DATE = PROBABLY_23_CE
EXACT_DATE = SCHOLARLY_DISPUTED
```

Do not write either date as uncontested.

---

## 2.2 Explicit cult headwear

The inscription assigns headwear to cult personnel:

```text
στεφάνους δὲ ἐχόντω οἱ μὲν ἱεροὶ καὶ αἱ ἱεραὶ πῖλον λευκόν
```

and distinguishes first-time initiates’ headgear, followed by laurel-crowning at the prescribed stage.

```text
ANDANIA_HIEROI_WHITE_PILOS = A_EPIGRAPHIC
ANDANIA_HIERAI_WHITE_PILOS = A_EPIGRAPHIC
ANDANIA_PROTOMYSTAI_DISTINCT_HEADWEAR = A_EPIGRAPHIC
ANDANIA_LAUREL_WREATH_STAGE = A_EPIGRAPHIC
```

This directly blocks:

```text
ANDANIA = UNIVERSAL_FEMALE_CULTIC_BAREHEADEDNESS
```

---

## 2.3 Women’s hair/adornment rules are separate

The women’s procession/dress section includes:

```text
μηδὲ ἀνάδεμα
μηδὲ τὰς τρίχας ἀνπεπλεγμένας
```

alongside gold/cosmetic restrictions.

```text
ANDANIA_WOMEN_ANADEMA_PROHIBITION = A_EPIGRAPHIC
ANDANIA_WOMEN_ANAPLEKO_HAIR_PROHIBITION = A_EPIGRAPHIC
ANDANIA_HAIR_RULE != PROOF_OF_NO_HEADWEAR
```

The same regulation therefore demonstrably has distinct axes:

```text
HEADWEAR_RULES
HAIR_ORNAMENT_RULES
HAIRSTYLE_RULES
```

within one ritual code.

This is stronger and safer than inferring `hair mentioned -> textile impossible`.

---

## 2.4 Role/status differentiation

Andania distinguishes female categories including private women, girls, enslaved women and female cult personnel.

```text
ANCIENT_RITUAL_FEMALE_DRESS_CAN_BE_ROLE_STATUS_DIFFERENTIATED = A_EPIGRAPHIC
```

This makes status-sensitive historical questions legitimate but does not prove any particular Corinthian wives/free-wives reconstruction.

---

## 2.5 `pilos` is not Paul’s object by definition

```text
ANDANIA_PILOS != PAULINE_OBJECT_PROVED
ANDANIA_PILOS != ROMAN_PALLA
ANDANIA_PILOS != TOGA_CAPITE_VELATO
```

The valid comparison is category-level: ancient ritual law could prescribe female headwear while separately regulating hair.

---

# 3. Massey on Andania — what survives

Massey’s lexical comparison argues:

```text
ANAPLEKO = BRAID_PLAIT_CURL_BIND_UP_STYLING
NOT_NORMAL_VERB_FOR_UNBINDING_HAIR
```

His broader conclusion — hairstyle and textile covering can coexist — is strengthened by the direct Andania headwear/hair separation.

```text
ANDANIA_ANAPLEKO_AS_UNBOUND_HAIR = STRONGLY_CHALLENGED
HAIR_RULE != NO_TEXTILE_HEADWEAR = STRONG_COMPARATIVE_CONTROL
```

Do not jump from “hair rule does not exclude a veil” to “all women therefore wore a veil.”

---

# 4. Lycosura — direct text and correction

## 4.1 Surviving wording

Direct scholarly digital edition:
- https://www.greek-language.gr/digitalResources/ancient_greek/anthology/inscriptions/page_079.html

Key sequence:

```text
μηδὲ τὰς τ[ρί]-
χας ἀμπεπλεγμένας μηδὲ κεκαλυμ-
μένος, μηδὲ ἄνθεα παρφέρην
```

Direct minimum:

```text
LYCOSURA_HAIR_CONDITION_PROHIBITION = A_EPIGRAPHIC
LYCOSURA_KEKALYMMENOS_FORM = A_EPIGRAPHIC
LYCOSURA_EXPLICIT_TOUS_ANDRAS = FALSE
LYCOSURA_EXPLICIT_MALE_ONLY_COVERING_RULE = NOT_IN_SURVIVING_TEXT
```

The masculine form `κεκαλυμμένος` is real. The male-only referent is not automatically proved by that form in this elliptical regulation.

---

## 4.2 Voutiras 1999 — autopsy-based epigraphic control

> Emmanuel Voutiras, “Opfer für Despoina: Zur Kultsatzung des Heiligtums von Lykosura IG V 2, 514,” *Chiron* 29 (1999): 233–250.

Official DAI PDF:
- https://publications.dainst.org/journals/chiron/article/view/972/5339

Voutiras treats lines 9–13 as elliptical and translates the relevant rule generically: hair braided / head covered, without inserting a separate male subject.

```text
VOUTIRAS_LYCOSURA_TRANSLATION = GENERIC_ENTRANT_HAIR_OR_HEAD_COVERING_PROHIBITION
VOUTIRAS_MALE_ONLY_SPLIT = NOT_ADOPTED
LYCOSURA_LINES_9_13 = ELLIPTICAL_SYNTAX
```

Parsed publisher PDF text is direct; pixel screenshot verification was not completed in the earlier runtime.

---

## 4.3 Massey / Dittenberger male-only split is interpretation, not inscription text

Massey acknowledges the grammatical issue and follows a Dittenberger expansion supplying:

```text
[τοὺς ἄνδρας]
```

before the covering condition.

That phrase is **not surviving inscription wording**.

```text
DITTENBERGER_TOUS_ANDRAS = EDITORIAL_PARAPHRASTIC_SUPPLEMENT
MASSEY_MALE_ONLY_LYCOSURA = INTERPRETIVE_INFERENCE
MASSEY_MALE_ONLY_LYCOSURA != DIRECT_EPIGRAPHIC_FACT
```

The earlier project statement `LYCOSURA_MALE_HEAD_COVERING_PROHIBITION = DIRECT` is therefore superseded.

---

## 4.4 Karataş 2020 — current specialist control

> Aynur-Michèle-Sara Karataş, “Greek Cults and Their Sacred Laws on Dress-code: The Laws of Greek Sanctuaries for Hairstyles, Jewelry, Make-up, Belts, and Shoes,” *Classical World* 113.2 (2020): 147–170. DOI `10.1353/clw.2020.0001`.

Karataş summarizes Lykosoura as prohibiting braided hair and a veiled/covered head without making the male-only split self-evident, while noting more generally that gender often must be inferred contextually in sacred dress laws.

```text
KARATAS_LYCOSURA = BRAIDED_HAIR_PLUS_COVERED_HEAD_PROHIBITIONS
KARATAS_MALE_ONLY_SPLIT = NOT_USED
```

---

## 4.5 Current grammatical calibration

Competing possibilities remain:

1. generic masculine referring to an entrant;
2. male-specific switch as Dittenberger/Massey infer;
3. irregular/elliptical redaction;
4. older emendation to feminine — not the transmitted form.

```text
LYCOSURA_KEKALYMMENOS_GRAMMATICAL_MASCULINE = A_TEXT
LYCOSURA_REFERENT_MALE_ONLY = C_BC_INTERPRETIVE
LYCOSURA_REFERENT_GENERIC_ENTRANT = B_C_VIABLE
LYCOSURA_EXACT_GENDER_MAPPING = OPEN
```

Do not silently insert `[τοὺς ἄνδρας]`; do not silently emend to feminine.

---

# 5. What survives from Lycosura for 1 Cor 11

Strong surviving result:

```text
LYCOSURA_HAIR_AND_COVERING_APPEAR_AS_DISTINCT_RULE_ITEMS = A_B_HIGH
HAIR_RULE != AUTOMATIC_HAIR_ONLY_INTERPRETATION = STRONG
```

What does **not** survive as direct fact:

```text
LYCOSURA_MEN_ALONE_FORBIDDEN_TO_COVER = NOT_DIRECT
LYCOSURA_WOMEN_THEREFORE_EXPECTED_TO_VEIL = NOT_DIRECT
LYCOSURA_PROVES_WOMEN_VEILED = FALSE
LYCOSURA_PROVES_WOMEN_UNVEILED = FALSE
```

Massey’s specific inference that women’s veiling is logically assumed is therefore downgraded to reconstruction.

---

# 6. Shared Andania/Lycosura conclusion

The two inscriptions now serve complementary direct controls:

```text
ANDANIA:
  female role/status categories
  explicit female hair/adornment restrictions
  explicit female cult-official headwear

LYCOSURA:
  hair and covered-head rules are distinct items
  exact sex-specific mapping of covering rule is disputed
```

Safe combined historical statement:

> Greek ritual dress codes can regulate hair and headwear as distinct but interacting axes; neither inscription supplies a universal rule for all women or Paul’s exact Corinthian artifact.

```text
HAIR_AND_HEADWEAR_DISTINCT_REGULATORY_AXES = A_B_HIGH_COMPARATIVE
DIRECT_INFLUENCE_ON_CORINTH = UNPROVED
EXACT_CORINTH_TRIGGER = RECONSTRUCTION_LAYER
```

---

# 7. Relation to actual unbound hair

Massey’s lexical point must remain distinct from evidence about genuinely unbound/dishevelled hair.

```text
MASSEY = ANAPLEKO_IS_NOT_NORMAL_UNBINDING_VERB
COSGROVE_2005 = SOCIAL_MEANINGS_OF_ACTUAL_UNBOUND_HAIR
```

Cosgrove remains a separate social-history control; do not use actual unbound-hair examples to redefine Andania’s `ἀναπλέκω`.

---

# 8. Current project impact

```text
CORE_GRADE_REVERSALS = 0
SCOPE_GRADE_PROMOTIONS = 1_ALL_WOMEN
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
HAIR_AS_NATURAL_ANALOGY = B_HIGH
EXACT_CORINTH_TRIGGER = RECONSTRUCTION_LAYER
ALL_WOMEN_PRACTICAL_SCOPE = B_LEADING_CONTEXTUAL
FREE_D_MARRIED_WIVES_PRIMARY_SCOPE = C_SERIOUS_CURRENT_ALTERNATIVE
```

The inscriptions strengthen evidence discipline and comparative complexity, not a single total model. Status-sensitive comparative evidence keeps the marital/free(d)-wives reconstruction serious, but it no longer owns a co-leading `OPEN_B_C` project state after the broader discourse/cross-status stress.

---

# 9. No-overclaim rules

```text
ANDANIA_HAIR_RULE != NO_HEADWEAR
ANDANIA_HIERAI_PILOS != ALL_WOMEN_SAME_HEADWEAR
ANDANIA_DATE = DISPUTED_91BCE_VS_C23CE
LYCOSURA_KEKALYMMENOS_MASCULINE != MALE_ONLY_REFERENT_PROVED
DITTENBERGER_TOUS_ANDRAS != INSCRIPTION_TEXT
MASSEY_MALE_SPLIT = SCHOLARLY_INFERENCE
LYCOSURA != PROOF_WOMEN_VEILED
LYCOSURA != PROOF_WOMEN_UNVEILED
RITUAL_COMPARAND != PAULS_DIRECT_SOURCE
```

---

# 10. Result

```text
CORE_GRADE_REVERSALS = 0
SCOPE_GRADE_PROMOTIONS = 1_ALL_WOMEN
MASSEY_2015_DIRECT_FULLTEXT = CLOSED
ANDANIA_DIRECT_INSCRIPTION = CLOSED
ANDANIA_HIERAI_WHITE_PILOS = A_EPIGRAPHIC
ANDANIA_WOMEN_HAIR_ADORNMENT_RESTRICTIONS = A_EPIGRAPHIC
ANDANIA_DATE = DISPUTED
LYCOSURA_DIRECT_TEXT = CLOSED
LYCOSURA_MALE_ONLY_DIRECT_FACT = REJECTED_OVERCLAIM
LYCOSURA_EXACT_GENDER_MAPPING = OPEN
HAIR_AND_HEADWEAR_DISTINCT_REGULATORY_AXES = A_B_HIGH_COMPARATIVE
ALL_WOMEN_PRACTICAL_SCOPE = B_LEADING_CONTEXTUAL
FREE_D_MARRIED_WIVES_PRIMARY_SCOPE = C_SERIOUS_CURRENT_ALTERNATIVE
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
