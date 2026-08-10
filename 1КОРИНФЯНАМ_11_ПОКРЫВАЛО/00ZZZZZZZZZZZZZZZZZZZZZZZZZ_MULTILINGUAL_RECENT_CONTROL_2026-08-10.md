# 1 Коринфянам 11:2–16 — multilingual recent control

**Дата:** 2026-08-10  
**Статус:** `MULTILINGUAL / RECENT / DIRECT-INSTITUTIONAL / RECEPTION-CONTROL / RESEARCH-ONLY / PUBLICATION-HOLD`

## 0. Purpose

The search was deliberately expanded beyond English-language scholarship. This layer records recent non-English or institutionally local work that can improve the literature map **without confusing recency with authority**.

```text
RECENT != PRIMARY
MASTER_THESIS != PEER_REVIEWED_SPECIALIST_ARTICLE
INSTITUTIONAL_REPOSITORY = STRONG_PROVENANCE_FOR_EXISTENCE/OBJECT
LOCAL_RECEPTION != CORE_CLAIM_UPGRADE
```

---

# 1. Klára Hamplová 2025 — full Czech thesis directly available

## 1.1 Object and provenance

Klára Hamplová, *Modlitba žen v 1 Kor 11,2–16. Sociokulturní kontext, exegeze a teologické poselství* [“Women’s Prayer in 1 Cor 11:2–16: Sociocultural Context, Exegesis and Theological Message”], diploma thesis, Charles University, Catholic Theological Faculty, Prague, 2025.

Official Charles University repository records:

- defended thesis;
- defense date: 3 September 2025;
- grade: `Excellent`;
- advisor: Jaroslav Brož;
- referee: Mireia Ryšková;
- language: Czech;
- full thesis PDF directly available from the institutional repository.

Routes:

- metadata/object: https://dspace.cuni.cz/handle/20.500.11956/205699
- full PDF: https://dspace.cuni.cz/bitstream/handle/20.500.11956/205699/120513785.pdf?isAllowed=y&sequence=1

Repository notice permits study/research access while restricting commercial use and misrepresentation of the work. Therefore:

```text
HAMPLOVA_OBJECT_EXISTENCE = A2_INSTITUTIONAL
HAMPLOVA_FULLTEXT_ACCESS = DIRECT
HAMPLOVA_PUBLICATION_STATE_FOR_PRODUCT = HOLD
HAMPLOVA_SCHOLARLY_WEIGHT = C_CONTEXTUAL_CURRENT_RECEPTION
```

The last line is a project weighting decision: this is a defended master-level thesis, not an independent specialist-journal control.

## 1.2 Full-text structure

The full PDF exposes a verse-by-verse exegetical chapter:

```text
11:3  p31
11:4  p34
11:5  p37
11:6  p41
11:7  p43
11:8  p46
11:9  p47
11:10 p49
11:11 p53
11:12 p55
11:13 p56
11:14 p58
11:15 p60
11:16 p62
conclusion p67
```

Exact PDF/display page should be kept distinct from printed thesis page.

## 1.3 v10 — independent current reception of active `ἐξουσία`

Hamplová translates v10 in her own working translation as the woman having authority **over her own head**.

Her discussion reports the traditional passive/subordination reading, then notes—following the literature she synthesizes—that neither the passive sense of `ἐξουσία` nor the idiom “have authority over” as subjection is supported by normal Greek usage. She treats the active/right/control reading as the most natural grammatical option while acknowledging tension with the preceding argument.

Safe project use:

```text
HAMPLOVA_V10_ACTIVE_WOMAN = CURRENT_CZECH_RECEPTION_SUPPORT
EXOUSIA_WOMAN_SUBJECT = A_SYNTAX // unchanged
EXOUSIA_ACTIVE_WOMAN_BEARER_PULL = B_HIGH // unchanged
```

This is **corroboration of a current reading**, not a new independent lexical proof, because her argument relies heavily on Fee/Thiselton and other secondary literature.

## 1.4 `διὰ τοῦτο` — useful current recognition of the discourse problem

Hamplová explicitly notes two possible functions of `διὰ τοῦτο`:

1. conclusion from preceding argument;
2. introductory phrase anticipating a reason that follows.

This is useful because it shows that the connective’s direction is a real exegetical issue in recent non-English work.

It does not override the project’s current primary discourse grade:

```text
DIA_TOUTO_V10_LINKS_BACKWARD = A_DISCOURSE
```

unless a stronger Greek discourse corpus establishes the cataphoric reading as preferable here.

## 1.5 `κεφαλή` and final synthesis

Hamplová’s conclusion reads `κεφαλή` primarily through origin/source plus mutual responsibility rather than simple superiority. Her hermeneutical synthesis treats the passage as a pastoral negotiation of order, dignity, freedom and unity under culturally conditioned social symbols.

This places her within a recognizable current egalitarian/source-oriented reception line.

```text
HAMPLOVA_KEPHALE_SOURCE/RELATIONAL = C_CURRENT_RECEPTION
KEPHALE_SOURCE_ONLY = C_VIABLE // unchanged
```

No grade promotion.

## 1.6 Important source-hygiene caution inside the thesis

Hamplová cites **Garland 2003**, not Garland 2025. Therefore nothing in this thesis can be used to prove Garland’s second-edition 2025 position.

```text
HAMPLOVA_CITES_GARLAND_2003
HAMPLOVA != GARLAND_2025_EVIDENCE
```

This reinforces the existing edition firewall.

---

# 2. Nicole Francis 2023/2024 — real recent alternative missed by the uploaded dump

## 2.1 Verified source

Nicole Francis, “A Pauline Dress Code or a Roman Analogy: Reinterpreting Paul’s Discourse in 1 Corinthians 11:1–16,” *Studia Antiqua* 22.1 (2023; repository/indexing surfaces also expose the issue in 2024).

Official BYU ScholarsArchive:

- https://scholarsarchive.byu.edu/studiaantiqua/vol22/iss1/6/

The journal page gives abstract, issue placement and downloadable PDF.

## 2.2 Model

Francis challenges the assumption that Paul’s primary purpose is to impose a prayer/prophesying dress code.

Her alternative is approximately:

```text
GROUP_CONFLICT
-> PAUL_PRESENTS/REASONS_THROUGH_HIERARCHICAL_STRUCTURE
-> HAIR/COVERING CULTURAL NORMS FUNCTION AS ANALOGICAL SUPPORT
-> THE PASSAGE'S PRIMARY POINT IS NOT A STANDALONE DRESS CODE
```

This is distinct from:

- `HAIR_ONLY`: Paul directly commands a hairstyle instead of cloth;
- `NOMMIK`: Paul responds to Roman ritual-uniformity pressure;
- `PEPPIATT/COSTA/SALES`: substantial lines belong to a Corinthian voice;
- `CALLON`: the recipients are specifically free(d) wives.

Therefore Francis deserves a separate model slot:

```text
FRANCIS_ROMAN_ANALOGY_NOT_DRESS_CODE = REAL_PUBLISHED_ALTERNATIVE
FRANCIS_MODEL_STATUS = C_CONTEXTUAL_YOUNG_SCHOLAR_JOURNAL
```

`Studia Antiqua` is a student-oriented academic journal; the article is real and useful for model diversity but should not be weighted like NTS/JBL/HTR.

## 2.3 Why useful

The model pressures a common hidden assumption:

```text
IF_PAUL_MENTIONS_COVERING/Hair
THEN
THE_PRIMARY_ILLOCUTION_MUST_BE_A_DRESS_CODE
```

That inference is not automatic. Francis is worth keeping as a hermeneutical/model control, even if the current project continues to think Paul gives real appearance instructions in vv4–6/13–16.

No core grade change.

---

# 3. German 2025 publication — bibliographic existence verified, content HOLD

Barbara Lumesberger-Loisl, “Kopftuchgebot für Christinnen?: Die ‘Verhüllung’ des Kopfes als Ausdruck der Geschlechterdifferenz (1 Kor 11,2–16),” in *Ist die Bibel frauenfeindlich?* (2025), pp.295–303.

IxTheo bibliographic record:

- https://ixtheo.de/Record/1925710505

Verified minimum:

```text
LUMESBERGER_LOISL_2025_EXISTS = BIBLIOGRAPHIC_VERIFIED
LANGUAGE = GERMAN
PAGES = 295_303
EXACT_ARGUMENT = HOLD_DIRECT_TEXT
```

No substantive thesis is attributed until direct text is acquired.

This is a deliberate fail-closed contrast with the uploaded agent dump, which repeatedly invented detailed arguments from bibliographic-looking records.

---

# 4. Multilingual search result

The useful current picture is:

```text
PORTUGUESE:
  Costa 2023/24 = serious linguistic quotation model
  Chadwick 2022 = real hair-only proposal

SWEDISH:
  Berglund 2025 = peer-reviewed 1 Cor 11–14 article; Nõmmik reception

CZECH:
  Hamplová 2025 = full defended thesis; active exousia / source-relational kephale reception

GERMAN:
  Lumesberger-Loisl 2025 = directly bibliographically verified; content HOLD
```

No evidence was found in this pass that overturns the current core grades.

The multilingual layer is valuable mainly because it prevents an English-only Status Quaestionis and reveals whether newer interpretive families are circulating independently across scholarly contexts.

---

# 5. Boundary

```text
CORE_GRADE_REVERSALS = 0
MULTILINGUAL_SEARCH = CONTINUE
MASTER_THESIS != SPECIALIST_PEER_REVIEW
BIBLIOGRAPHIC_RECORD != CONTENT
PUBLICATION_HOLD = true
PRODUCT_WRITE = false
```
