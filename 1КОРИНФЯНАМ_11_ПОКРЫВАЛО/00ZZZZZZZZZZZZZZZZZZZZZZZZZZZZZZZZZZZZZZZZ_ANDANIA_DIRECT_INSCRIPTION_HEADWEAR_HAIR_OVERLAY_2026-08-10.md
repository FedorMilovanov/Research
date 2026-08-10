# 1 Коринфянам 11:2–16 — Andania direct inscription / headwear / hair overlay

**Дата:** 2026-08-10  
**Статус:** `DIRECT-INSCRIPTION / CGRN-PHI / HEADWEAR-HAIR-SEPARATION / DATE-DISPUTED / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Purpose

Этот слой заменяет зависимость от современных пересказов Andania прямым чтением IG V,1 1390 / CGRN 222.

Главный вопрос:

> Что надпись действительно предписывает о женской одежде, headwear и волосах — и что из этого можно безопасно сравнивать с 1 Cor 11?

Нельзя смешивать:

```text
CULT_OFFICE_HEADWEAR
INITIATE_HEADWEAR
PROCESSION_DRESS_CODE
HAIR_ORNAMENTATION
TEXTILE_VEIL
```

---

# 1. Direct text controls

## PHI Greek Inscriptions

Direct text:

- https://epigraphy.packhum.org/text/31826

PHI labels the inscription:

```text
IG V,1 1390
Messenia — Andania
92/91 BC
```

## CGRN 222

Critical ritual-norm edition:

- https://cgrn.ulg.ac.be/file/222/
- DOI: `10.54510/CGRN222`

CGRN title:

> Dossier of regulations concerning the mysteries at Andania

CGRN currently gives the date as **probably 23 AD**, while explicitly documenting the long-running alternative dating to c.91 BC and noting that the debate continues.

Therefore:

```text
ANDANIA_OBJECT = DIRECT_EPIGRAPHIC
ANDANIA_TRADITIONAL_DATE = 92/91_BC (PHI / older Achaean-era reconstruction)
ANDANIA_CGRN_PREFERRED_DATE = PROBABLY_23_AD
ANDANIA_EXACT_DATE = SCHOLARLY_DISPUTED
```

Do not silently cite one date as uncontested.

Chronological significance:

> under CGRN’s current preferred dating, the inscription would be essentially Pauline-period evidence; under the older dating it remains late-Hellenistic and still relatively close.

---

# 2. Headwear is explicitly prescribed for cult personnel

PHI lines 13–15 / direct Greek text:

```text
στεφάνων. στεφάνους δὲ ἐχόντω οἱ μὲν ἱεροὶ καὶ αἱ ἱεραὶ πῖλον λευκόν,
τῶν δὲ τελουμένων οἱ πρωτομύσται στλεγγίδα.
...
στεφανούσθωσαν δὲ πάντες δάφναι.
```

CGRN translates/summarizes this as a headwear section in which:

- `hieroi` **and `hierai`** wear a white felt `pilos`;
- first-time initiates wear a distinct headpiece (`stlengis` / tiara-like item in CGRN’s translation);
- at the commanded stage all are crowned with laurel.

Direct minimum:

```text
ANDANIA_HIERAI_WHITE_PILOS = A_EPIGRAPHIC
ANDANIA_HIEROI_WHITE_PILOS = A_EPIGRAPHIC
ANDANIA_PROTOMYSTAI_DISTINCT_HEADWEAR = A_EPIGRAPHIC
ANDANIA_LAUREL_WREATH_STAGE = A_EPIGRAPHIC
```

This immediately blocks the oversimplification:

```text
ANDANIA = FEMALE_CULTIC_BAREHEADEDNESS = FALSE_UNIVERSAL
```

At least some female cult officials are explicitly assigned headwear.

---

# 3. Women’s procession dress code separately regulates cosmetics, hair ornament and hairstyle

PHI lines 20–23 approximately:

```text
μὴ ἐχέτω δὲ μηδεμία χρυσία
μηδὲ φῦκος
μηδὲ ψιμίθιον
μηδὲ ἀνάδεμα
μηδὲ τὰς τρίχας ἀνπεπλεγμένας
...
```

The subject is explicitly feminine (`μηδεμία`) within the procession/dress regulation.

The prohibited items include:

- gold jewelry;
- rouge/cosmetic pigment;
- white lead;
- `ἀνάδεμα` — hair/head band or ornamental binding;
- hair in the `ἀναπλέκω` state (`ἀνπεπλεγμένας`).

Direct minimum:

```text
ANDANIA_WOMEN_GOLD_PROHIBITION = A_EPIGRAPHIC
ANDANIA_WOMEN_COSMETIC_PROHIBITIONS = A_EPIGRAPHIC
ANDANIA_WOMEN_ANADEMA_PROHIBITION = A_EPIGRAPHIC
ANDANIA_WOMEN_ANAPLEKO_HAIR_PROHIBITION = A_EPIGRAPHIC
```

Massey’s lexical case that `ἀναπλέκω` concerns braided/plaited/arranged hair rather than a normal verb for “unbinding/loosening hair” remains a specialist lexical interpretation, but the **existence of the hair prohibition itself is now primary-pinned**.

---

# 4. Hair regulation does not tell us whether all those women were veiled or unveiled

The crucial methodological point is negative.

The procession rule says that women must not have an `anadema` and must not have hair in the prohibited arranged/plaited state.

It does **not** say:

```text
ALL_PROCESSION_WOMEN_MUST_BE_UNVEILED
```

or:

```text
ALL_PROCESSION_WOMEN_MUST_WEAR_A_TEXTILE_VEIL
```

Moreover, the same inscription elsewhere explicitly assigns a white `pilos` to female `hierai`.

Thus the categories demonstrably coexist:

```text
HEADWEAR_RULES
+ HAIR_ORNAMENT_RULES
+ HAIRSTYLE_RULES
```

within a single ritual regulation.

Safe project result:

```text
ANDANIA_HAIR_RULE != PROOF_OF_NO_HEADWEAR
ANDANIA_HEADWEAR_RULE != PROOF_ALL_WOMEN_VEILED
HAIR_STATE_AND_HEADWEAR_ARE_SEPARABLE_REGULATORY_AXES = A_B_HIGH_COMPARATIVE_CONTROL
```

This independently supports the methodological core of Massey 2015 without adopting every one of Massey’s reconstructions.

---

# 5. “Pilos” must not be silently translated into Paul’s veil

The `πῖλος` is a specific felt cap/headpiece in this cultic regulation.

Therefore:

```text
ANDANIA_PILOS != PAULINE_KATA_KEPHALES_OBJECT_PROVED
ANDANIA_PILOS != ROMAN_PALLA
ANDANIA_PILOS != ROMAN_TOGA_CAPITE_VELATO
```

Its evidential use is category-level:

> Greek ritual law can prescribe specific headwear to women while separately controlling hairstyle and adornment.

It does not identify the exact artifact behind 1 Cor 11.

---

# 6. Social-status and role differentiation inside the inscription

The dress section distinguishes multiple female categories and price ceilings / garments, including:

- private women;
- girls;
- enslaved women;
- `hierai` women;
- `hierai` girls.

This means the Andania regulation itself is not a one-rule-for-all-females costume code.

Direct implication:

```text
ANCIENT_RITUAL_FEMALE_DRESS_CAN_BE_STATUS/ROLE_DIFFERENTIATED = A_EPIGRAPHIC
```

That is methodologically relevant to Callon/status-based 1 Cor 11 questions, while still not proving Callon’s Corinthian reconstruction.

```text
CALLON_STATUS_QUESTION = HISTORICALLY_PLAUSIBLE_CATEGORY
ANDANIA != CALLON_CORINTH_TRIGGER
```

---

# 7. Relation to Andania dating debate

The dating disagreement matters for how strongly the inscription can be called “contemporary”.

Current safe wording:

> IG V,1 1390 is a late-Hellenistic/early-Roman ritual regulation conventionally dated to 92/91 BCE in PHI and older scholarship; CGRN 222 currently prefers a date around 23 CE while documenting that the chronological debate remains open.

Do not write:

```text
ANDANIA_CERTAINLY_91_BC = FALSE_CERTAINTY
ANDANIA_CERTAINLY_23_AD = FALSE_CERTAINTY
```

If the 23 CE date gains broader closure, its value as a near-contemporary Pauline comparator rises; the basic ritual-dress observations do not depend on resolving the date.

---

# 8. Direct correction to popular/secondary Andania shortcuts

Reject:

```text
“the women at Andania had loose/unbound hair, therefore no veil”
“all Andanian women were bareheaded”
“all Andanian women wore a pilos”
“hair rule proves hairstyle-only reading of 1 Cor 11”
```

The direct inscription supports instead:

```text
SOME_FEMALE_CULT_OFFICIALS_HAVE_PRESCRIBED_HEADWEAR
WOMEN_HAVE_SEPARATE_HAIR/ORNAMENT_RESTRICTIONS
FEMALE_DRESS_RULES_VARY_BY_ROLE/STATUS
EXACT_HEADWEAR_OF_EVERY_PROCESSION_WOMAN = NOT_STATED
```

---

# 9. Relation to Lycosura correction

Andania and Lycosura now serve complementary primary controls:

```text
ANDANIA:
  explicit female categories
  explicit female hair/ornament restrictions
  explicit female cult-official headwear

LYCOSURA:
  hair and covered-head prohibitions as distinct items
  exact gender mapping of κεκαλυμμένος disputed
```

Neither inscription supports a simplistic universal about Greek women.

Together they strongly support only the comparative methodological statement:

> ritual dress codes can regulate hair and headwear as distinct but interacting axes.

---

# 10. Effect on current 1 Cor 11 grades

No core grade reversal.

```text
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
HAIR_AS_NATURAL_ANALOGY = B_HIGH
EXACT_CORINTH_TRIGGER = RECONSTRUCTION_LAYER
WIVES_VS_ALL_WOMEN = OPEN_B_C
```

Andania strengthens background complexity and evidence discipline, not a single total model.

---

# 11. Result

```text
CORE_GRADE_REVERSALS = 0
ANDANIA_DIRECT_INSCRIPTION = CLOSED
ANDANIA_DATE = DISPUTED_91BC_VS_C23AD
ANDANIA_HIERAI_WHITE_PILOS = A_EPIGRAPHIC
ANDANIA_WOMEN_ANADEMA_AND_HAIR_RESTRICTIONS = A_EPIGRAPHIC
ANDANIA_HAIR_RULE_IMPLIES_NO_HEADWEAR = REJECTED
ANDANIA_ALL_WOMEN_HEADWEAR_FORM = NOT_STATED
HAIR_AND_HEADWEAR_DISTINCT_REGULATORY_AXES = A_B_HIGH_COMPARATIVE_CONTROL
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
