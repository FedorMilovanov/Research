# Отступничество — source registry supplement 30+

**Дата:** 2026-09-30  
**Статус:** `ACTIVE EVIDENCE REGISTRY / RESEARCH-ONLY / PUBLICATION_HOLD`  
**Дополняет:** `apostasy/08_SOURCE_REGISTRY_70_PLUS_2026-09-29.md`  
**Глобальная политика:** `data/repository-evidence-policy-v2.json`

## 1. Назначение

Это **не ещё один список ссылок** и не замена базового реестра 70+. Цель — закрыть пробелы по новым узлам исследования: Послание Иуды, 2 Пет. 2, means of perseverance, сильные альтернативные конфессиональные чтения и text-critical material.

### Поля

- `Policy class` — класс по глобальному evidence policy:
  - `A1` — первичный текст автора / непосредственная participant-created запись;
  - `A2` — официальный институциональный/конфессиональный первичный текст;
  - `B1` — качественное вторичное академическое/экзегетическое свидетельство;
  - `C` — discovery/aggregator/denominational interpretation lead, не quote-safe само по себе.
- `Access` — `FULL_OBJECT_VERIFIED`, `PARTIAL_OBJECT`, `CATALOG_ONLY`, `LINK_ONLY`.
- `Locator` — `EXACT_LOCATOR_VERIFIED`, `COARSE_LOCATOR_ONLY`, `LOCATOR_MISSING`.
- `Claim role` — **что именно** источник может поддерживать.
- `Quote-safe` — по умолчанию `NO` до item-level повторной сверки edition/version/context, даже если полный текст доступен.

**Важно:** классификация не означает, что богословский вывод источника принят. Она означает только качество доступа/происхождения для конкретного claim.

---

## 2. Jude — текстология и структура предупреждения

| ID | Policy class | Source | Access | Locator | Claim role | Quote-safe |
|---|---|---|---|---|---|---|
| JS01 | B1 | Philipp F. Bartholomä, “Did Jesus Save the People out of Egypt? A Re-examination of a Textual Problem in Jude 5,” *Novum Testamentum* 50 (2008), DOI 10.1163/156853608X268903 — https://www.researchgate.net/publication/233497562_Did_Jesus_Save_the_People_out_of_Egypt_A_Re-examination_of_a_Textual_Problem_in_Jude_5 | PARTIAL_OBJECT | EXACT_LOCATOR_VERIFIED (article/pages metadata; claim text still partial) | three principal Jude 5 readings; serious defense of `Ἰησοῦς` | NO |
| JS02 | B1 | Jarl Fossum, “Kyrios Jesus as the Angel of the Lord in Jude 5–7,” *New Testament Studies* 33.2 (1987), 226–243, DOI 10.1017/S0028688500022645 — https://www.cambridge.org/core/journals/new-testament-studies/article/abs/kyrios-jesus-as-the-angel-of-the-lord-in-jude-57/4D476457F64A0D44F67FC4AC8E393A9F | PARTIAL_OBJECT | EXACT_LOCATOR_VERIFIED (pp. 226–243; abstract verified) | christological/intertextual handling of Jude 5–7; reading problem remains acknowledged | NO |
| JS03 | B1 | Daniel B. Wallace, NA28 changes summary — https://danielbwallace.com/2012/12/17/259/ | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | secondary confirmation that NA28 changed Jude 5 to `Ἰησοῦς`; points to textual debate | NO |
| JS04 | C | NET Bible textual note, Jude 5 — https://www.biblegateway.com/passage/?search=Jude+5-7&version=NET | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (Jude 5 note) | manuscript-reading summary/discovery bridge; not substitute for critical apparatus | NO |
| JS05 | C | BiblicalStudies.org.uk Jude bibliography — https://www.biblicalstudies.gospelstudies.org.uk/jude.php | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | discovery index for Jude scholarship, incl. Fossum and Winter on Jude 22–23 | NO |
| JS06 | B1 | S. C. Winter, “Jude 22–23: A Note on the Text and Translation,” *Harvard Theological Review* 87.2 (1994), 215–222; discovery via https://www.biblicalstudies.gospelstudies.org.uk/jude.php | CATALOG_ONLY | EXACT_LOCATOR_VERIFIED (bibliographic pages only) | text-critical issue in Jude 22–23; full object still required | NO |
| JS07 | A1 | Calvin, Commentary on Jude 20–25 — https://www.ccel.org/ccel/calvin/calcom45.viii.ii.viii.html?scrBook=Jude&scrCh=1&scrV=21 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | historical Reformed synthesis of building/prayer/keeping/mercy/divine preservation | NO |
| JS08 | A1 | Augustine, *On Rebuke and Grace* — https://www.newadvent.org/fathers/1513.htm | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | perseverance as divine gift; Jude 24 used in argument | NO |
| JS09 | A1 | Greek text access, Jude 6 — https://biblehub.com/text/jude/1-6.htm | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | `μὴ τηρήσαντας` / `τετήρηκεν` wordplay; lexical verification | NO_PUBLIC_QUOTE_DEPENDENCE |
| JS10 | A1 | Greek text access, Jude 12 — https://biblehub.com/text/jude/1-12.htm | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | `δὶς ἀποθανόντα ἐκριζωθέντα`; “twice dead/uprooted” wording | NO_PUBLIC_QUOTE_DEPENDENCE |
| JS11 | A1 | Greek text access, Jude 19 — https://biblehub.com/text/jude/1-19.htm | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | `πνεῦμα μὴ ἔχοντες` — opponents characterized as not having Spirit | NO_PUBLIC_QUOTE_DEPENDENCE |
| JS12 | A1 | Greek text access, Jude 21 — https://biblehub.com/text/jude/1-21.htm | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | imperative `τηρήσατε`; grammar of build/pray/keep/wait | NO_PUBLIC_QUOTE_DEPENDENCE |
| JS13 | A1 | Greek text access, Jude 24 — https://biblehub.com/text/jude/1-24.htm | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED | `φυλάξαι`, proving v.24 does **not** repeat v.21’s `τηρέω` | NO_PUBLIC_QUOTE_DEPENDENCE |

### Jude evidence judgment

The corpus may safely use the following **research** conclusions now:

- Jude 5 has a real text-critical problem; do not pretend `Jesus` is uncontested.
- The wilderness judgment argument does not depend on solving the subject variant.
- Jude 21 and 24 do **not** use the same Greek verb for “keep”; theological/compositional parallel remains, lexical identity does not.
- Jude 22–23 must not support a finely divided pastoral taxonomy until critical-text closure.

---

## 3. Reformed primary/confessional line — preservation through means

| ID | Policy class | Source | Access | Locator | Claim role | Quote-safe |
|---|---|---|---|---|---|---|
| RF01 | A1 | John Owen, *The Nature and Causes of Apostasy from the Gospel*, TOC — https://ccel.org/ccel/owen/apostasy.toc.html | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (work/chapters) | Owen’s whole apostasy architecture; ch. I = Heb 6:4–6 | NO |
| RF02 | A1 | Owen, *Apostasy*, ch. I — https://ccel.org/ccel/owen/apostasy.i.v.html | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (chapter) | Heb 6; real privileges/operations distinguished from saving grace | NO |
| RF03 | A1 | Owen, *Apostasy*, ch. VI — https://ccel.org/ccel/owen/apostasy.i.x.html | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (chapter) | pride, sloth, world-love, Satan as causes/occasions of apostasy | NO |
| RF04 | A2 | Westminster Confession XVII — https://www.opc.org/documents/MESV_col.html | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (XVII.1–3) | Reformed perseverance: neither total nor final fall; ground in decree, Christ, Spirit, covenant | YES_CANDIDATE_AFTER_VERSION_LOCK |
| RF05 | A2 | 1689 Baptist Confession XVII — https://founders.org/library/chapter-17-the-perseverance-of-the-saints/ | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (17.1–3) | Particular Baptist perseverance; severe falls compatible with final preservation | YES_CANDIDATE_AFTER_VERSION_LOCK |
| RF06 | A2 | Canons of Dort, Fifth Head, Art. 6–14 — https://threeforms.org/canons-of-dort/ | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (Fifth Head, esp. Arts. 6, 8, 14) | God preserves true believers; **uses hearing, reading, meditation, exhortations, threats, promises, sacraments as means** | YES_CANDIDATE_AFTER_VERSION_LOCK |
| RF07 | A2 | CRCNA, Canons of Dort Fifth Head 13–14 — https://www.crcna.org/welcome/beliefs/confessions/canons-dort | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (Fifth Head 13–14) | independent official denominational witness to “means in perseverance” wording | YES_CANDIDATE_AFTER_VERSION_LOCK |
| RF08 | B1 | Sinclair Ferguson, “Apostasy and How It Happens,” Ligonier — https://www.ligonier.org/learn/articles/apostasy-and-how-it-happens | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | pastoral progression/drift of apostasy; modern Reformed synthesis | NO |

### Reformed control point

Dort Fifth Head Art. 14 is especially important because it gives an **official confessional**, not merely modern author, formulation of the thesis already emerging from Hebrews/Jude: warnings/threats are among the means by which God preserves and completes grace. This should become a central historical-theology anchor, not a decorative citation.

---

## 4. Arminius and Wesley — strongest non-Reformed counter-readings

| ID | Policy class | Source | Access | Locator | Claim role | Quote-safe |
|---|---|---|---|---|---|---|
| AW01 | A1 | Jacobus Arminius, “The Perseverance of the Saints,” *Works* vol. 1 — https://www.ccel.org/ccel/arminius/works1.iii.vii.html | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (section V) | historical nuance: Arminius says he had **not taught** that true believer finally perishes, but judged texts serious enough to require further inquiry | YES_CANDIDATE_AFTER_EDITION_LOCK |
| AW02 | A1 | Arminius, full vol. 1 PDF — https://ccel.org/ccel/a/arminius/works1/cache/works1.pdf | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (p. 176 in CCEL PDF for section V) | page-stable backup for AW01 | YES_CANDIDATE_AFTER_EDITION_LOCK |
| AW03 | A1 | John Wesley, Sermon 86, “A Call to Backsliders” — https://wesley.nnu.edu/john-wesley/the-sermons-of-john-wesley-1872-edition/sermon-86-a-call-to-backsliders/ | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY (sermon numbered paragraphs) | Wesley reads Heb 6/10 as concerning justified/sanctified persons and distinguishes recoverable backsliding from formal apostasy | NO_UNTIL_PARAGRAPH_LOCK |
| AW04 | A1 | Wesley, Sermon 86, same source | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | important anti-despair control: even grave backsliders are not to assume they committed final apostasy | NO_UNTIL_PARAGRAPH_LOCK |

### Counter-reading rule

Future articles must not reduce “Arminian” to a single sentence. Arminius himself was historically more cautious on final apostasy than later Wesleyan formulations; Wesley’s Sermon 86 supplies a much more explicit justified/sanctified reading of Hebrews 6 and 10. These should be represented separately.

---

## 5. Lutheran confessional line

| ID | Policy class | Source | Access | Locator | Claim role | Quote-safe |
|---|---|---|---|---|---|---|
| LU01 | A2 | Formula of Concord, Solid Declaration XI (Election) — https://bookofconcord.org/solid-declaration/ | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (XI.11–14 and surrounding section) | Lutheran election language acknowledges examples of people who do not persevere/fall away; doctrine must drive to Word, repentance, godliness, assurance rather than speculation/despair | YES_CANDIDATE_AFTER_VERSION_LOCK |
| LU02 | A2 | Formula of Concord, Solid Declaration XI — same source | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | broader Lutheran synthesis of election, means, falling away; needs paragraph-level extraction for publication | NO |

### Lutheran gap

Need an additional exact-locator pass on Formula of Concord paragraphs commonly cited for those who receive the Word with joy and later fall away, plus Apology/other Lutheran confessional texts concerning loss of faith/Spirit. Do **not** infer Lutheran position from secondary Reformed/Arminian descriptions.

---

## 6. Roman Catholic counter-position

| ID | Policy class | Source | Access | Locator | Claim role | Quote-safe |
|---|---|---|---|---|---|---|
| RC01 | A2 | John Paul II, *Veritatis Splendor* §68–69 — https://www.vatican.va/content/john-paul-ii/en/encyclicals/documents/hf_jp-ii_enc_06081993_veritatis-splendor.html | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (§68–69) | official Catholic witness quoting Trent: received grace of justification can be lost by apostasy and also mortal sin | YES_CANDIDATE_AFTER_VERSION_LOCK |
| RC02 | A2 | *Veritatis Splendor* Latin PDF, same claim with Trent citation — https://www.vatican.va/content/john-paul-ii/la/encyclicals/documents/hf_jp-ii_enc_06081993_veritatis-splendor.pdf | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (§68 / Trent references) | original-language institutional backup for RC01 | YES_CANDIDATE_AFTER_VERSION_LOCK |

### Catholic use rule

This material belongs in the **historical/confessional spectrum**, not as an exegetical proof of Hebrews/Jude. It shows that the Roman Catholic system has a different doctrine of post-justification loss than both classic Reformed perseverance and Wesleyan final-apostasy framing.

---

## 7. Free Grace alternative

| ID | Policy class | Source | Access | Locator | Claim role | Quote-safe |
|---|---|---|---|---|---|---|
| FG01 | C | Bob Wilkin / Grace Evangelical Society, “Does Hell Await Those Who Fall? — 2 Peter 2:18–22” — https://faithalone.org/grace-in-focus-articles/does-hell-await-those-who-fall/ | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (article passage) | Free Grace alternative: vv.18–22 shift referent to duped believers; warning not read as loss of eternal life | NO |
| FG02 | C | Grace Evangelical Society, “Is Hebrews 10:29 About Punishment or Chastisement?” — https://faithalone.org/radio/is-hebrews-1029-about-punishment-or-chastisement/ | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (episode/article page) | Free Grace reading: warning to believer; punishment/chastisement/reward framework rather than eternal loss | NO |

### Free Grace evaluation rule

These are valuable because they break a false binary “Reformed vs Arminian.” But GES material is a **confessional/advocacy interpretation source**, not neutral scholarship; it must be used to represent the view, then tested exegetically against Hebrews/Peter.

---

## 8. 2 Peter 2 — direct competing interpretations

| ID | Policy class | Source | Access | Locator | Claim role | Quote-safe |
|---|---|---|---|---|---|---|
| P201 | A1 | John Gill, doctrinal treatment including 2 Pet. 2:1 — https://ccel.org/ccel/gill/doctrinal.vii.iv.html | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY | historical Particular Baptist/nonsoteriological purchase line; God/Deut 32 background | NO_UNTIL_EXACT_PARAGRAPH |
| P202 | A1 | Calvin, 2 Pet. 2:20–22 — https://biblehub.com/library/calvin/commentaries_on_the_catholic_epistles/2_peter_2_20-22.htm | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (2 Pet 2:20–22) | historical Reformed handling of knowledge/escape/relapse | NO_UNTIL_EDITION_LOCK |
| P203 | B1 | Thomas R. Schreiner, “Problematic Texts for Definite Atonement” — https://www.monergism.com/%E2%80%9Cproblematic-texts%E2%80%9D-definite-atonement-pastoral-and-general-epistles?page=1 | FULL_OBJECT_VERIFIED | COARSE_LOCATOR_ONLY (2 Peter 2:1 subsection visible; book edition/pages still needed) | phenomenological reading: false teachers appeared bought/knowing Christ; dog/pig later reveal nature | NO |
| P204 | C | BibleHub commentary aggregation, 2 Pet. 2:1 — https://www.biblehub.com/commentaries/2_peter/2-1.htm | FULL_OBJECT_VERIFIED | EXACT_LOCATOR_VERIFIED (verse page) | discovery map of historical actual-redemptive/general-purchase readings; never cite aggregator as final authority | NO |
| P205 | C | Westminster Annotations transcription/discovery — https://calvinandcalvinism.wordpress.com/2009/01/27/the-westminster-annotations-second-edition-on-2-peter-21-and-jude-4/ | PARTIAL_OBJECT | COARSE_LOCATOR_ONLY | historical lead for sufficient-price/professional readings; original 1651 edition still required | NO |

### 2 Peter publication gap

Before a standalone article is publication-candidate, obtain:

1. original-edition/page locator for Schreiner’s chapter;
2. primary/original scan or stable edition of Westminster Annotations;
3. at least one modern critical commentary on `δεσπότης`/`ἀγοράζω` with exact pages;
4. lexicon/critical-text support not mediated by aggregator;
5. a strong Wesleyan/Arminian scholarly treatment of 2:1 and 2:20–22, not only denominational blog material.

---

## 9. Source-count result and what it means

This supplement contains **36 distinct entries/uses** across textual criticism, primary historical theology, official confessions, modern exegesis and explicit counter-traditions. Combined with `apostasy/08_SOURCE_REGISTRY_70_PLUS_2026-09-29.md`, the topic now has **100+ mapped source entrypoints**.

That number is **not** a publication metric. A single exact primary locator that directly supports a claim is worth more than ten secondary URLs.

The next quality metric is:

> `reader-facing claim → biblical locus → exact primary/historical locator → strongest counter-reading → confidence/status`.

---

## 10. Remaining source gaps (priority)

### P0

- Jude 5: apparatus-level witness data from a critical edition, not NET/Wallace summaries alone.
- Jude 22–23: full Winter article or equivalent modern textual apparatus.
- Heb 10:29: modern critical grammars/commentaries on referent of `ἡγιάσθη` + primary Owen exact locator.
- 2 Pet 2:1: exact Schreiner book pages + modern critical commentaries + strong conditional-security scholarship.
- Heb 6:4–6: modern scholarly competing models with exact page locators, not only interviews/secondary summaries.

### P1

- John 15 branch-in-Christ interpretation matrix.
- Romans 11 corporate/individual cutting-off matrix.
- Gal 5:4 `ἐξεπέσατε τῆς χάριτος` matrix.
- Rev 2–3 per-letter warning matrix.
- 1 Cor 9:27 `ἀδόκιμος` in 9:24–10:13.

### P2

- broader patristic reception beyond Augustine/Chrysostom;
- post-Reformation Baptist/Puritan pastoral treatment;
- contemporary evangelical pastoral cases only after doctrinal/exegetical spine is settled.

Until these P0 gaps close, corpus remains `RESEARCH-ONLY / PUBLICATION_HOLD`.
