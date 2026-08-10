# 1 Коринфянам 11:2–16 — Massey 2015 Andania/Lycosura epigraphy full-text audit

**Дата:** 2026-08-10  
**Статус:** `DIRECT-JOURNAL-FULLTEXT / EPIGRAPHY / HAIR-VS-VEIL / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Source and method

Direct journal PDF:

> Preston T. Massey, “Dress Codes at Roman Corinth and Two Hellenic Sites: What do the Inscriptions at Andania and Lycosura Tell Us about 1 Corinthians 11.2–16?” *Journal of Greco-Roman Christianity and Judaism* 11 (2015): 51–81.

Journal PDF:

- https://www.jgrchj.net/volume11/JGRChJ11-4_Massey.pdf

Journal volume/abstract:

- https://jgrchj.net/volume11/?mode=abstracts&page=volume11

The PDF text was directly inspected. Browser screenshot rendering was also attempted for key pages but the screenshot endpoint returned a cache miss; therefore this dossier does **not** claim a successful pixel/image-page verification. The parsed journal PDF text and page locators remain direct-object controls.

```text
MASSEY_2015_PDF = DIRECT_JOURNAL_OBJECT
PDF_TEXT = DIRECTLY_INSPECTED
PDF_SCREENSHOT_RENDER = ATTEMPTED_CACHE_MISS
```

---

# 1. What Massey is actually testing

Massey targets two claims often bundled together in 1 Cor 11 literature:

1. that Greek women in ritual contexts could appear without textile veils;
2. that references to hair arrangement imply that a textile covering is absent.

His key epigraphic comparanda are:

- Andania sacred law, c.95–90 BCE;
- Lycosura sacred law, broadly 2nd c. BCE, with later cultic continuity.

He is explicit that proximity does **not** establish direct influence on Corinth:

```text
ANDANIA_TO_CORINTH_DIRECT_INFLUENCE = SPECULATION/UNPROVED
LYCOSURA_TO_CORINTH_DIRECT_INFLUENCE = SPECULATION/UNPROVED
```

The valid use is comparative epigraphic/social-linguistic background.

---

# 2. Andania — `ἀναπεπλεγμένη` is not “unbound hair”

Massey focuses on the Andania hair prohibition and attacks an older translation tradition that treated `ἀναπεπλεγμένας` as hair “loosened” and hanging down.

His lexical/literary comparison argues:

```text
ἀναπλέκω / ἀναπεπλεγμένη = braid / plait / curl / bind-up styling
NOT = conventional Greek verb for loosening/unbinding hair
```

He adduces literary comparanda including Lucian and Athenaeus where the verb describes braided/plaited/curl-like or bound-up styles, frequently in contexts of elaboration, gold, luxury or sexual attractiveness.

Key direct PDF locators:

- pp.60–69, especially pp.61–69;
- article PDF parsed page indices P9–P18.

Safe result:

```text
ANDANIA_ANAPLEKO_AS_UNBOUND_HAIR = REJECTED_BY_MASSEY_LEXICAL_CASE
ANDANIA_HAIR_RULE = HAIRSTYLE/ORNAMENTATION_RULE
ANDANIA_HAIR_RULE != PROOF_OF_UNVEILING
```

This does not prove every woman at Andania wore a veil; it blocks using this term itself as evidence that hair was deliberately loosened and the head left materially uncovered.

---

# 3. Hair arrangement and textile veil can coexist

Massey’s most important methodological point is independent of whether one accepts every reconstruction he offers:

> a hairstyle statement and a textile-covering statement are not mutually exclusive categories.

He uses Homeric material to distinguish hair-binding accessories from an actual veil (`κρήδεμνον`). A woman can remove a veil without changing the underlying hairstyle, and can wear hair up/down/plaited while a separate veil remains present.

Thus:

```text
HAIR_STATE != TEXTILE_COVERING_STATE
BRAIDED/PLAITED_HAIR != UNVEILED_HEAD
UNBOUND_HAIR != NECESSARILY_UNVEILED_HEAD
```

This is an important adversarial control against arguments that infer:

```text
TEXT_MENTIONS_HAIR -> TEXT_CANNOT_ALSO_REFER_TO_VEIL
```

Current project implication:

```text
HAIR_AS_NATURAL_ANALOGY = B_HIGH // unchanged
MATERIAL_COVERING = B_HIGH_LEADING // provenance strengthened
HAIR_ONLY_WHOLE_PASSAGE = C_SERIOUS_ALTERNATIVE // still live, but this epigraphic argument does not strengthen it
```

---

# 4. Lycosura — hair prohibition and male covering prohibition are grammatically separable

The Lycosura sacred law includes a sequence that Massey prints and analyzes, including:

```text
μηδὲ τὰς τρίχας ἀμπεπλεγμένας,
μηδὲ κεκαλυμμένος
```

Massey follows the grammatical gender distinction in reading the first prohibition as directed to women’s braided/plaited hair and the masculine `κεκαλυμμένος` as directed to a man not being covered.

Article pp.69–73, especially the discussion around the inscription lines 10–11.

Safe source-specific result:

```text
LYCOSURA_FEMALE_BRAIDED_HAIR_PROHIBITION = DIRECT_EPIGRAPHIC_DISCUSSION
LYCOSURA_MALE_HEAD_COVERING_PROHIBITION = DIRECT_EPIGRAPHIC_DISCUSSION
HAIR_RULE_AND_COVERING_RULE_CAN_COEXIST_IN_ONE_RITUAL_CODE = STRONG_COMPARATIVE_CONTROL
```

This is particularly valuable for 1 Cor 11 because Paul likewise has:

- a male covering rule;
- a female head rule;
- an explicit later hair argument.

But:

```text
LYCOSURA_RULE = PAULS_DIRECT_SOURCE = UNPROVED
LYCOSURA = EXACT_CORINTH_TRIGGER = FALSE
```

---

# 5. Massey’s direct conclusion about the two inscriptions

At pp.79–81 Massey concludes that Andania/Lycosura do **not** provide conclusive evidence that married women in Greek cultic ritual appeared without veils merely because hair arrangement is discussed.

He argues that hair and veil are not contradictory and that the shift in 1 Cor 11:13–15 to long hair can be understood as a related but distinct argument rather than as a redefinition of all earlier covering language.

Source-specific claim:

```text
MASSEY_2015_FINAL_MODEL = TEXTILE_VEIL + DISTINCT_HAIR_ARGUMENT
MASSEY_2015_REJECTS_HAIR_REPLACES_VEIL
```

Project-level calibration remains more modest than Massey’s own final reconstruction:

```text
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
HAIR_AS_NATURAL_ANALOGY = B_HIGH
```

No automatic promotion to A: an epigraphic comparative case is not a noun `veil` inserted into 1 Cor 11:4–6.

---

# 6. Important limitation: Massey sometimes moves from “not excluded” to “likely assumed”

Massey sometimes reasons that where an inscription tells men not to veil and gives women a hair prohibition, women’s veiling may be logically assumed.

That inference is stronger than the inscriptional minimum.

The project must separate:

```text
INSCRIPTION_DOES_NOT_SAY_WOMEN_UNVEILED = STRONG
FROM
INSCRIPTION_PROVES_WOMEN_WERE_VEILED = STRONGER_RECONSTRUCTION
```

Therefore:

```text
MASSEY_LYCOSURA_WOMEN_VEILED = B_C_SOURCE_RECONSTRUCTION
LYCOSURA_DOES_NOT_ESTABLISH_UNVEILED_WOMEN = B_HIGH_NEGATIVE_CONTROL
```

This keeps the audit adversarial rather than merely adopting Massey.

---

# 7. Sexual/ostentatious hair-signaling — real background, exact Corinth trigger still open

Massey assembles literary examples in which elaborate/plaited/curling hair participates in:

- beauty display;
- luxury/ostentation;
- sexual attractiveness;
- gendered presentation.

This is compatible with the project’s existing background grade:

```text
GENDER/SEXUAL_SIGNALING_OF_GROOMING = B_HIGH_BACKGROUND
```

But it does not establish:

```text
CORINTHIAN_WOMEN_HAD_SEXUALLY_RISQUE_BRAIDS = FACT
EXACT_CORINTH_TRIGGER = SOLVED
```

The local Christian conflict remains reconstruction-layer.

---

# 8. Relation to Cosgrove 2005

Charles H. Cosgrove, “A Woman’s Unbound Hair in the Greco-Roman World,” *JBL* 124.4 (2005): 675–692, is now bibliographically direct through JSTOR/SBL-era journal indexing and is a high-value next control for the **actual social meanings of genuinely unbound/dishevelled female hair**.

This distinction matters:

```text
MASSEY: ANAPLEKO != UNBINDING
COSGROVE: WHAT ACTUAL_UNBOUND_HAIR_SIGNIFIED
```

Future synthesis should not use literary examples of truly unbound hair to redefine epigraphic `ἀναπλέκω` as “unbound”.

Acquisition status:

```text
COSGROVE_2005 = VERIFIED_BIBLIOGRAPHIC_B1
COSGROVE_FULLTEXT = P1_CONTENT_HOLD
```

---

# 9. Relation to current Roman female-dress visual controls

The epigraphic result should be held together with:

- Thompson 1988 — Roman Corinth portraits;
- Gill 1990 — Roman-colonial portraiture control;
- Olson 2008 — prescriptive literature vs visual evidence;
- Hughes 2007 — mixed early-imperial funerary representations;
- Stafford 2024 — later visual-method control;
- Fantham 2008 — ritual/gender chapter, body HOLD;
- ASCSA *Corinth XXII* 2022 — Julian Basilica assemblage.

Together they block both simplistic universals:

```text
ALL_RESPECTABLE_WOMEN_ALWAYS_VEILED = REJECT
GREEK_RITUAL_WOMEN_NORMALLY_UNVEILED = NOT_ESTABLISHED_AS_UNIVERSAL
```

---

# 10. Effect on Nõmmik / Roman-trigger models

Massey 2015 is not evidence for Nõmmik’s specific hidden-event reconstruction, but it reinforces a broader methodological possibility:

> multiple head/hair conventions can coexist within ritual dress codes without reducing the whole issue to one artifact.

This fits the project separation:

```text
ROMAN_CAPITE_VELATO_BACKGROUND = A
FEMALE_STATUS/HAIR/COVERING_BACKGROUND = COMPLEX
NOMMIK_HIDDEN_CORINTH_EVENTS = C_SERIOUS_RECONSTRUCTION
V4_EXACT_CAPITE_VELATO = B_C
```

---

# 11. Result

```text
CORE_GRADE_REVERSALS = 0
MASSEY_2015_DIRECT_FULLTEXT = CLOSED
ANDANIA_UNBOUND_HAIR_TRANSLATION = STRONGLY_CHALLENGED
LYCOSURA_HAIR_AND_MALE_COVERING_RULES = DIRECTLY_CONTROLLED
HAIR_RULE != NO_TEXTILE_VEIL = STRONG_COMPARATIVE_CONTROL
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
EXACT_CORINTH_TRIGGER = RECONSTRUCTION_LAYER
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
