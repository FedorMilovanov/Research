# 1 Коринфянам 11:2–16 — Drake 2025 / `ἐξουσία + ἐπί` / freshness control

**Дата:** 2026-08-10  
**Статус:** `CURRENT-2025-SCHOLARSHIP / DIRECT-PUBLISHER-SUMMARY / PRIMARY-GREEK-CONTROL / PAPYROLOGY-BOUNDARY / FALSE-FRESHNESS / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Purpose

Этот проход закрывает три разных проблемы, которые нельзя смешивать:

1. действительно свежая крупная монография 2025 года с отдельной главой по 1 Кор 11;
2. синтаксическая калибровка `ἐξουσία + ἐπί + gen.` — `uncommon` не значит `unattested`;
3. фильтр ложной свежести, когда старые работы получают дату 2025 из-за повторной загрузки/индексации.

```text
PUBLISHER_SUMMARY != FULL_CHAPTER
UNCOMMON_CONSTRUCTION != UNGRAMMATICAL_CONSTRUCTION
BIBLICAL_PARALLEL != EXACT_1COR11_REFERENT
RECENT_UPLOAD_DATE != ORIGINAL_PUBLICATION_DATE
BOUNDED_NEGATIVE_SEARCH != GLOBAL_NONEXISTENCE
```

---

# 1. Susanna Drake 2025 — genuinely new Cambridge monograph and a dedicated Corinth chapter

## 1.1 Direct Cambridge metadata

Cambridge University Press directly verifies:

> Susanna Drake, *Veiling in the Late Antique World* (Cambridge University Press, 2025).

Book DOI:

- `10.1017/9781009673518`

Publisher routes:

- https://www.cambridge.org/core/books/veiling-in-the-late-antique-world/509F3EDBAAC1967415F6CD50105A5568
- https://www.cambridge.org/core/search?eventCode=SE-AU&filters%5BauthorTerms%5D=Susanna+Drake

Cambridge gives:

```text
ONLINE_PUBLICATION = 2025-11-26
PRINT_PUBLICATION = 2025-12-18
PRINT_PUBLICATION_YEAR = 2025
```

Thus later catalogue/podcast/repository labels that may display 2026 must not silently replace the publisher publication year.

## 1.2 Dedicated chapter

Chapter 2 is explicitly:

> “Veils in Corinth: Paul’s First Letter to the Corinthians,” pp.70–89.

Chapter DOI:

- `10.1017/9781009673518.003`

Direct Cambridge route:

- https://www.cambridge.org/core/books/veiling-in-the-late-antique-world/veils-in-corinth/BB79DFCE0FB2F5AFDD9CCB0C6C5B83D4

This is a **new 2025 specialist acquisition** relative to the current Research corpus.

```text
DRAKE_2025_BOOK = VERIFIED_CURRENT_CUP_MONOGRAPH
DRAKE_2025_CH2_PP70_89 = VERIFIED_CUP
DRAKE_2025_CH2_BODY = PAYWALL/DIRECT_BODY_HOLD
```

## 1.3 What Cambridge’s own chapter summary establishes

The official chapter summary says that Drake reads Paul as giving women instruction to **veil their heads when praying or prophesying in the assembly**.

It also states her historical thesis that women in the first-century Mediterranean world, including Corinthian women, most likely **veiled and unveiled for multiple reasons**, including:

- beauty;
- comfort;
- status;
- virtue;
- piety.

The summary explicitly rejects reducing the practice solely to theological, exegetical or liberative motives.

Safe source-level result:

```text
DRAKE_2025_MATERIAL_VEILING_MODEL = DIRECT_CUP_SUMMARY
DRAKE_2025_MULTIFACTOR_SOCIAL_SIGNIFICATION = DIRECT_CUP_SUMMARY
DRAKE_2025_SINGLE_CAUSE_DRESS_CODE_MODEL = REJECTED_BY_AUTHOR_SUMMARY
```

This is especially valuable because it independently converges with the project’s existing primary/material controls:

- Olson: prescriptive literature != simple behavioral census;
- Hughes: early-imperial funerary images are mixed;
- Plutarch/Valerius: female head-covering anecdotes are internally unstable;
- Andania/Lycosura: headwear and hairstyle can be separate regulatory axes;
- Stafford: later imagery remains heterogeneous.

But convergence is not a vote-counting proof.

## 1.4 What is NOT yet established from the paywalled chapter

The current Cambridge summary does not establish Drake’s detailed positions on:

```text
κεφαλή
ἐξουσία in v10
exact function of angels
hair-only vs hair-as-analogy arguments in vv13-15
exact social class/address scope
exact Roman capite-velato relation to v4
exact Corinth trigger
```

Therefore:

```text
DRAKE_EXOUSIA_POSITION = HOLD
DRAKE_KEPHALE_POSITION = HOLD
DRAKE_ANGELS_POSITION = HOLD
DRAKE_HAIR_ARGUMENT_DETAIL = HOLD
DRAKE_EXACT_CORINTH_TRIGGER = HOLD
```

Do not turn the publisher summary into a fabricated full-chapter review.

---

# 2. `ἐξουσία + ἐπί + gen.` — uncommon does not mean unattested

## 2.1 Why this correction is needed

Jill Marshall, citing Arzt-Grabner et al., *Papyrologischer Kommentar zum Neuen Testament* 2 (2006), p.390, notes that the combination of `ἐξουσία` with `ἐπί + genitive` is **uncommon**.

That observation can easily be over-expanded into a false claim such as:

```text
EXOUSIA_EPI_GEN = UNATTESTED
or
EXOUSIA_EPI_GEN = GRAMMATICALLY_SUSPICIOUS
```

Neither follows.

The PKNT volume itself is bibliographically verified through Universität Salzburg / the PKNT project, but direct p.390 remains unavailable in the current runtime.

```text
ARZT_GRABNER_PKNT2_2006 = VERIFIED_INSTITUTIONAL
PKNT_P390 = STRONG_DIRECTLY_CITED_PROVENANCE / DIRECT_PAGE_HOLD
```

## 2.2 Direct biblical Greek parallels

### Revelation 2:26

Greek textual tradition has:

```text
δώσω αὐτῷ ἐξουσίαν ἐπὶ τῶν ἐθνῶν
```

Here `ἐπί + genitive` marks a domain/object over which authority is given.

```text
REV_2_26_EXOUSIA_EPI_GEN = DIRECT_BIBLICAL_GREEK
SEMANTIC_DIRECTION = ACTIVE_AUTHORITY_OVER_DOMAIN
SUPPORT_VERB = δίδωμι, NOT ἔχω
```

### Revelation 14:18

The text has:

```text
ὁ ἔχων ἐξουσίαν ἐπὶ τοῦ πυρός
```

This is especially important because it combines:

```text
ἔχω + ἐξουσίαν + ἐπί + genitive
```

and means that the angel possesses authority/power over fire.

```text
REV_14_18_EXACT_SUPPORT_VERB_PATTERN = DIRECT_BIBLICAL_GREEK
REV_14_18_ACTIVE_BEARER = CLEAR
REV_14_18_EXACT_HEAD_PARALLEL = NO
```

### Revelation 20:6

The phrase is preposed:

```text
ἐπὶ τούτων ὁ δεύτερος θάνατος οὐκ ἔχει ἐξουσίαν
```

Again:

```text
ἐπί + genitive + ἔχω + ἐξουσία
```

with the semantic direction “the second death has no authority over these.”

```text
REV_20_6_ACTIVE_DOMAIN_RELATION = DIRECT_BIBLICAL_GREEK
```

### Daniel OG 3:97 / traditional numbering differences

Old Greek Daniel also supplies a related `ἐξουσία + ἐπί` authority-domain construction with `δίδωμι`, not `ἔχω`.

Use only as a related Septuagintal Greek control, not as an exact support-verb parallel.

## 2.3 Consequence

The safe formulation is:

```text
EXOUSIA_PLUS_EPI_GEN = UNCOMMON_IN_SOME_CORPORA
BUT
EXOUSIA_PLUS_EPI_GEN = CLEARLY_ATTESTED_AND_SEMANTICALLY_NORMAL_AS_ACTIVE_AUTHORITY_DOMAIN_RELATION
```

The strongest exact support-verb parallels above are Rev 14:18 and Rev 20:6.

Therefore future agents must not write:

```text
“ἐξουσία + ἐπί + genitive has no parallels” = FALSE
“the grammar forces ‘a sign on the head’” = FALSE
“the phrase is too unusual to mean active authority” = OVERCLAIM
```

---

# 3. Relation to Fendel 2023 documentary papyri

Victoria Beatrix Fendel’s systematic documentary-papyrus study remains the best current corpus-scale nonbiblical control.

Her direct Wiley article reports:

```text
TOTAL_EXOUSIAN_TOKENS = 290
TOTAL_EXOUSIAN_ECHO = 190
```

For Roman-period higher-register `ἐξουσίαν ἔχω` cases, her table gives:

```text
INF = 105
ARTICULAR_INFINITIVE = 1
GENITIVE = 4
PP = 3
NO_OVERT_OBJECT = 2
LOST = 3
```

Important limitation:

> The article’s main text/table does **not** enumerate the actual prepositions used in all three Roman-period PP cases.

Therefore:

```text
FENDEL_ROMAN_PP_COMPLEMENTS = 3_VERIFIED
FENDEL_ROMAN_PP_IS_EPI_GEN = NOT_ESTABLISHED_FROM_ARTICLE_TABLE
```

One already acquired direct female Roman-period documentary example is PSI X 1115 (AD 152), where the PP is:

```text
περὶ αὐτοῦ
```

not `ἐπί + genitive`.

This distinction must be preserved.

## 3.1 Bounded extra-biblical search result

The current bounded search did **not** locate a nonbiblical exact parallel:

```text
ἐξουσίαν ἔχειν ἐπὶ τῆς κεφαλῆς
```

or another clean documentary Roman-period `ἔχω + ἐξουσία + ἐπί + genitive` body/head construction.

That is a bounded acquisition result only:

```text
EXACT_NONBIBLICAL_HEAD_PARALLEL = NOT_FOUND_IN_BOUNDED_SEARCH
GLOBAL_NONEXISTENCE = NOT_CLAIMED
```

The real corpus remains much more useful than a fabricated “perfect” papyrus.

---

# 4. Why the active semantic pull remains strong but exact referent stays open

Current independent controls now include:

1. woman as grammatical subject in 1 Cor 11:10;
2. normal Pauline/NT active semantic use of `ἐξουσία`;
3. Hooker and Fitzmyer direct historical lexical arguments;
4. Fendel’s large documentary corpus;
5. female documentary/epigraphic right-bearers (PSI X 1115; TAM II 603, etc.);
6. direct biblical `ἔχω + ἐξουσία + ἐπί + genitive` constructions (Rev 14:18; 20:6).

Thus:

```text
EXOUSIA_WOMAN_SUBJECT = A_SYNTAX
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH_STRENGTHENED
EXOUSIA_EXACT_REFERENT = B_C_UNCHANGED
```

The constructional data do not tell us whether v10 means precisely:

- control/right concerning her own head;
- authority/right to pray or prophesy;
- authority-related status expressed in head presentation;
- another contextual relation.

They do make a purely passive lexical shortcut significantly more expensive:

```text
EXOUSIA_LEXICALLY_MEANS_VEIL_OR_SYMBOL_OF_MALE_AUTHORITY = REJECTED
```

A contextual/metonymic proposal is still logically possible but must be argued contextually, not asserted as the lexical meaning of `ἐξουσία`.

---

# 5. Standhartinger — another false-2025 freshness trap

ResearchGate currently displays Angela Standhartinger’s article as `October 2025`.

That is **not** the original publication date.

Direct institutional controls:

- Philipps-Universität Marburg bibliography lists:
  - lectio difficilior 2 (2002);
  - book version in Irene Dingel (ed.), *Feministische Theologie und Gender-Forschung*, Leipzig 2003, pp.43–66.
- Universität Mainz preserves the 8 May 2002 lecture/event description under the same title.
- the DOI itself encodes the 2002 lectio-difficilior issue: `10.36950/ld.02.2002.12844`.

Therefore:

```text
STANDHARTINGER_RESEARCHGATE_2025 = FALSE_FRESHNESS_REUPLOAD_OR_INDEX_DATE
STANDHARTINGER_ORIGINAL_ELECTRONIC = 2002
STANDHARTINGER_BOOK_VERSION = 2003_PP43_66
```

This joins the existing Penner/Vander Stichele freshness correction.

New cross-agent rule:

```text
RESEARCHGATE_YEAR != PUBLICATION_YEAR_WITHOUT_PRIMARY_BIBLIOGRAPHIC_CONTROL
DOI_ISSUE_METADATA + AUTHOR_INSTITUTIONAL_BIBLIOGRAPHY > PLATFORM_UPLOAD_DATE
```

---

# 6. Drake 2025 in relation to the current veil/hair map

Drake is especially important because she is both **recent** and methodologically resistant to monocausal social reconstruction.

At the current publisher-summary level, her chapter supports:

```text
MATERIAL_VEILING = REAL_PRACTICE_IN_AUTHOR_MODEL
WOMEN_VEIL_AND_UNVEIL = CONTEXT_DEPENDENT/MULTIFACTORIAL
EXACT_CORINTHIAN_SOCIAL_CAUSE = NOT_REDUCED_TO_ONE_CODE
```

This fits the project’s current broader conclusion:

```text
MATERIAL_COVERING = B_HIGH_LEADING
HAIR_ONLY = C_SERIOUS_ALTERNATIVE
FEMALE_STATUS/HAIR/COVERING_BACKGROUND = COMPLEX
EXACT_CORINTH_TRIGGER = RECONSTRUCTION_LAYER
```

No grade promotion is warranted from a publisher summary alone.

---

# 7. Current acquisition queue created by this pass

```text
P0 Drake 2025 ch.2 pp70-89 full body + notes = NEW_HIGH_VALUE_HOLD
P0 Arzt-Grabner PKNT 2 (2006) p390 + surrounding discussion = DIRECT_PAGE_HOLD
P1 Drake ch.1 ancient Mediterranean material relevant to first-century veiling = HOLD
P1 identify Fendel Roman PP rows from EXOUSIAN.xlsx and inspect actual prepositions = OPEN
P1 search nonbiblical literary/epigraphic ἐξουσία + ἐπί + gen beyond bounded web index = OPEN
```

If the full Drake chapter is acquired, test separately:

```text
material veil claim
exact historical trigger
social class/status differentiation
hair argument
kephale
exousia
angels
male practice
use of Corinthian archaeology
```

Do not treat the chapter summary as proof for any of those subclaims not explicitly stated by Cambridge.

---

# 8. Result

```text
CORE_GRADE_REVERSALS = 0

DRAKE_2025_CH2 = REAL_MAJOR_CURRENT_SPECIALIST_SOURCE
DRAKE_MATERIAL_VEILING = DIRECT_PUBLISHER_SUMMARY
DRAKE_MULTIFACTOR_SOCIAL_MODEL = DIRECT_PUBLISHER_SUMMARY
DRAKE_BODY_DETAILS = HOLD

EXOUSIA_EPI_GEN_BIBLICAL_GREEK = DIRECTLY_ATTESTED
REV_14_18_ECHO_EPI_GEN = EXACT_SUPPORT_VERB_PATTERN
REV_20_6_ECHO_EPI_GEN = EXACT_SUPPORT_VERB_PATTERN_PREPOSED
UNCOMMON != UNATTESTED

FENDEL_ROMAN_PP_COUNT = 3
FENDEL_ROMAN_PP_PREPOSITIONS = NOT_ENUMERATED_IN_ARTICLE_TABLE
EXACT_NONBIBLICAL_HEAD_PARALLEL = NOT_FOUND_IN_BOUNDED_SEARCH

STANDHARTINGER_2025_FRESHNESS = REJECTED
STANDHARTINGER_ORIGINAL = 2002_ELECTRONIC / 2003_BOOK

EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH_STRENGTHENED_PROVENANCE
EXOUSIA_EXACT_REFERENT = B_C_UNCHANGED
MATERIAL_COVERING = B_HIGH_LEADING_UNCHANGED
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
