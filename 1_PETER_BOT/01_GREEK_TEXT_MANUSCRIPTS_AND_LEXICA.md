# Greek Text, Manuscripts, Lexica, and Grammar for 1 Peter

## 1. Working stack

| Layer | Canonical use |
|---|---|
| SBLGNT | open Greek surface-text comparison |
| MorphGNT | machine-checkable morphology/lemma data |
| NA28 | current published Nestle–Aland edition |
| GNT6 | current 2026 UBS text; same Greek main text as forthcoming NA29 |
| ECM IV Catholic Letters | deep text-history/apparatus authority for 1 Peter |
| NTVMR / Liste | witness registration, manuscript metadata, images/transcriptions |
| BDAG | modern lexical semantic control |
| Danker Concise | learner-friendly extended-definition control |
| BDF / grammars | syntax; never reduce syntax to morphology |
| LSJ / classical sources | historical semantic range, not sole NT contextual authority |

## 2. Edition-state guard

- `NA28 = CURRENT_PUBLISHED_NA`
- `NA29 = FORTHCOMING; official release 2027-02-28`
- `GNT6 = CURRENT_AVAILABLE_2026`
- `GNT6_MAIN_TEXT = FORTHCOMING_NA29_MAIN_TEXT`
- `1_PETER_CATHOLIC_LETTERS_TEXT = ECM-informed already in NA28`

If a future web page still says "NA29 in preparation for 2026", prefer the newer official NA29 product page for release-state, while keeping GNT6's statement about text identity.

## 3. Manuscript workflow for a bot claim

For every proposed textual-variant question:

1. Identify the exact 1 Peter verse.
2. Check NA28/GNT6 apparatus relevance.
3. Check ECM IV Catholic Letters for the full evidence structure.
4. Use NTVMR Liste to resolve GA witness metadata.
5. Inspect manuscript image/transcription when the teaching point requires it.
6. Separate:
   - manuscript actually reads X;
   - apparatus includes witness X;
   - editor reconstructs X as Ausgangstext;
   - a translation follows X.
7. Keep the question non-competitive until the variant is reduced to one objective proposition.

No "majority of manuscripts" or "oldest manuscript" claim from memory.

## 4. BDAG / lexicon protocol

Copyright-safe workflow:

```text
STORE IN RESEARCH:
lemma + inflected form + verse + proposed semantic question + source locator/status

DO NOT STORE:
copied long BDAG definitions or page scans without rights

BOT EXPLANATION:
our own concise paraphrase + context + explicit uncertainty where needed
```

A lexical claim becomes `high` only when the sense is sufficiently constrained by context and independent controls. A word with several viable contextual senses stays `medium/contested`.

## 5. Priority 1 Peter lemma queue

| Lemma / family | Passage focus | What to verify |
|---|---|---|
| `ἐκλεκτός / ἐκλογή` | 1:1; 2:4,6,9 | election language; distinguish lexeme from systematics |
| `παρεπίδημος` | 1:1; 2:11 | sojourner/temporary resident language |
| `διασπορά` | 1:1 | diaspora; literal/metaphorical referent is exegesis |
| `πρόγνωσις / προγινώσκω` | 1:2,20 | foreknowledge; lexical range ≠ complete predestination model |
| `ἁγιασμός` | 1:2 | sanctification/consecration context |
| `ἀναγεννάω` | 1:3,23 | new birth |
| `κληρονομία` | 1:4 | inheritance; OT background separate from lexical definition |
| `φρουρέω` | 1:5 | guard/protect |
| `δοκίμιον` | 1:7 | testing/genuineness; lexical/semantic distinction |
| `ἀναστροφή` | 1:15,18; 2:12; 3:1,2,16 | conduct/way of life |
| `τιμή / τίμιος` | 1:7,19; 2:4,6,7,17; 3:7 | honor/value family |
| `ἀποτίθημι` | 2:1; 3:21 compound context | put away/remove; avoid etymological shortcuts |
| `λογικός` | 2:2 | contested semantic nuance; needs lexical + commentary controls |
| `οἰκοδομέω` | 2:5 | build/be built; syntax and voice matter |
| `ἱεράτευμα` | 2:5,9 | priesthood; OT intertext controls required |
| `περιποίησις` | 2:9 | possession/acquisition; OT background |
| `ἀρετή` | 2:9 | excellencies/virtues/praise; context |
| `ὑποτάσσω` | 2:13,18; 3:1,5; 5:5 | submission; syntax/participants/context, not ideology by lemma |
| `ἐλευθερία` | 2:16 | freedom and servant-of-God frame |
| `ὑπογραμμός` | 2:21 | example/pattern |
| `ἀναφέρω` | 2:24 | bear/carry/offering range; Isa 53 intertext |
| `ἴαομαι` | 2:24 | heal; metaphorical/contextual force |
| `σκεῦος / ἀσθενέστερος` | 3:7 | weaker vessel phrase; morphology does not define dimension |
| `ἀπολογία` | 3:15 | defense/answer; does not select a modern apologetic school |
| `συνείδησις` | 3:16,21 | conscience; contextual construction matters |
| `κηρύσσω` | 3:19 | proclaim; verb alone does not identify audience/content |
| `πνεῦμα` | 3:18,19 | spirit; referents in disputed context require exegesis |
| `ἀντίτυπος` | 3:21 | antitype/correspondence; typological scope is exegesis |
| `ἐπερώτημα` | 3:21 | question/request/pledge-related history; no exclusive gloss by lexicon fiat |
| `σώζω` | 3:21; 4:18 | save; clause-level syntax/theology required |
| `ἀγάπη / ἐκτενής` | 4:8 | earnest love; discourse/application |
| `ξενίζω / ξένος` | 4:4,12 | strangeness/foreignness semantic family |
| `χαρίσμα` | 4:10 | gift/stewardship context |
| `ποιμαίνω` | 5:2 | shepherd; leadership image |
| `ἐπισκοπέω` | 5:2 textual issue | oversee; inspect apparatus before teaching variant-dependent claim |
| `κλῆρος` | 5:3 | allotted charge/lot; leadership context |
| `ταπεινόω` | 5:6 | humble; syntax and agency |
| `μέριμνα` | 5:7 | anxiety/care |
| `ἀντίδικος` | 5:8 | adversary/legal metaphor |
| `στερεός` | 5:9 | firm/steadfast |

## 6. Anti-fallacy gates

- Aorist does not mean "once-for-all theology" by tense alone.
- Passive morphology does not identify the theological agent unless syntax/context does.
- Genitive case does not choose a complete semantic category automatically.
- Etymology is not meaning.
- A dictionary gloss is not an exegesis.
- One possible classical sense is not automatically the Petrine sense.
- Shared morphology does not prove shared referent.
- A textual variant must be taught from the apparatus/witness evidence, not a preferred translation.
