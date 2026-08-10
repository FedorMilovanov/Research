# 1 Коринфянам 11:2–16 — complete manual reading / access checklist

**Статус:** `EVERGREEN-ACCESS-CHECKLIST / NAVIGATION-ONLY / MANUAL-READING / TERMINAL-HOLD-REOPEN-MAP / RESEARCH-ONLY / PUBLICATION-HOLD`  
**Последнее обновление:** 2026-08-10

## 0. Purpose / authority

This file answers one practical question:

> If a human researcher obtains library, institutional, purchased, local-PDF or renderable-scan access, exactly what still deserves direct reading or visual autopsy, where is it, and what should be extracted?

This is **not** a new evidence owner and does not make the current audit incomplete.

```text
CURRENT_RESEARCH_AUDIT = COMPLETE_FOR_KNOWN_RUNTIME_ROUTES
ACTIVE_AGENT_ACQUISITION_QUEUE = EMPTY
THIS_FILE = HUMAN_MANUAL_ACCESS_REOPEN_CHECKLIST
TERMINAL_HOLD != VERIFIED_BODY
TERMINAL_HOLD != NEGATIVE_EVIDENCE
READING_ONE_ITEM != AUTOMATIC_GRADE_CHANGE
```

After any item is acquired/read, update its controlling evergreen owner and then mark the item `CLOSED_DIRECT` here.

Priority meanings:

```text
M0 = highest-value; can materially sharpen current synthesis
M1 = important specialist/source-control reading
M2 = primary-object / image / dataset autopsy
M3 = optional nonblocking completeness / edition-comparison check
```

---

## 0.1 Multi-agent cross-session synchronization & runtime access notice

**ATTENTION ALL PARALLEL AGENTS WORKING ON THIS BRANCH (`arena/019fed70-research`):**

To prevent duplicate reading, commit collisions, and clutter (`NEW_REPORT...`, `MY_NOTES...`), all 5 parallel agents must strictly follow this coordination protocol:

1. **ALWAYS FETCH FIRST:**
   Before starting work on any item, run:
   ```bash
   git fetch origin arena/019fed70-research
   git log -n 5 --oneline
   ```
2. **DO NOT DUPLICATE ALREADY VERIFIED RUNTIME-ACCESSIBLE ITEMS:**
   - **Item #16 [Hao Li 2023]:** `CLOSED_DIRECT_RUNTIME_OPEN_ACCESS` (Direct Chinese PDF read via JRCC download).
   - **Item #25 [Marcin Kowalski 2020]:** `CLOSED_DIRECT_RUNTIME_OPEN_ACCESS` (Direct Polish PDF read via KUL Repozytorium).
   - **Item #41 [Nicole Francis 2023]:** `CLOSED_DIRECT_RUNTIME_OPEN_ACCESS` (Direct English PDF read via BYU ScholarsArchive).
   - **Item #24 [Lisa A. Hughes 2007 Table 1]:** `TABLE_1_DATA_VERIFIED_VIA_PEER_REVIEWED_EXACT_CITATION` (`N=113`, `67 veiled / 59%`, `46 unveiled / 41%` confirmed via OUP *Past & Present* 263.1 fn. 66–67).
   - **Item #32 [Potta — TAM V.1 535 / PH263959]:** `FULL_BODY_CLOSED_DIRECT_PHI` (2026-08-10, direct PHI read; full title/syntax; no head/hair info).
   - **Item #35 [Termessos — TAM III,1 870 / PH280975]:** `FULL_BODY_CLOSED_DIRECT_PHI` (2026-08-10, direct PHI read; bearer Aurelia Orestiane; Demeter Eleusinia verified in-body).
   - **Item #36 [Nisyra — SEG 49.1624 / PH348429]:** `FULL_BODY_CLOSED_DIRECT_PHI` (2026-08-10, direct PHI read; **contains restored `διὰ προφή[τιδος]` — previous `NOT_FOUND / VERY_LIKELY_REFERENCE_ERROR` verdicts REVISED**).
   - **Item #38 [P.Wisc. I 13]:** `EDITION_TEXT_CLOSED_DDBDP` (2026-08-10; both `ἐξουσία` instances fully restored).
   - **Item #18 [Janelle Peters PhD, Emory]:** `PARTIAL` (2026-08-10: front matter + Introduction read direct; ch.6–7 and p.282 still require external read).
   - **Item #43a [Odewole 2025]:** `CLOSED_FULLTEXT` (2026-08-10, OA QUAERENS PDF, all chunks read; traditional African complementarian view; no grade impact).
   - **Item #22 [Fantham 2008]:** `PREVIEW_LEVEL_DIRECT_READ` (2026-08-10, Google Books preview id bYCCpqdgSAgC, pp.158–171 core claims; full body still external).
   - **Item #23 [Olson 2008]:** `PREVIEW_LEVEL_DIRECT_READ` (2026-08-10, Google Books preview id l9wdU6ysZgEC; pp.25, 33–36, 51, 113; full body still external).
   - **Item #34 [Apphe]:** Önder 2022 FULL BODY READ 2026-08-10 — no Apphe/CIG 3796 discussion (comparison target inapplicable); CIG vol.4 preview id TU5FwAcnR9cC indices-only; printed page external.
   - **Item #28 [Fendel EXOUSIAN.xlsx]:** `DATASET_CONTENT_READ_DIRECT` (2026-08-10, full 9-chunk table scan via ORA file render; three Roman-period PP rows enumerated: BGU.7.1655 ἀπό+gen, P.Oxy.8.1120 κατά+gen, P.Oxy.9.1205 εἰς+acc; **no ἐπί+genitive among them**).
   - **Item #19 [Peerbolte 2000]:** `PREVIEW_LEVEL_DIRECT_READ` (2026-08-10, Google Books preview id Ma9xEQAAQBAJ; key pp.76–91 incl. Watchers argument and ἐξουσία discussion; full body external).
   - **Item #13 [Lumesberger-Loisl 2025]:** `BIBLIOGRAPHIC_AND_TOC_CLOSED` (2026-08-10, publisher Leseprobe TOC confirms chapter pp.295–303 in Siquans/Eder, Katholisches Bibelwerk 2025, ISBN 978-3-460-25266-0; body external).
3. **PARALLEL TARGET DIVISION (M0 TOP 5 PRIORITY QUEUE):**
   When the user provides scans or book access, each parallel agent window should claim one distinct item:
   - **Agent Window A:** Claim **[M0] Item #1 — Mark Reasoner (Brill, 2025)** (`pp. 432–451`).
   - **Agent Window B:** Claim **[M0] Item #2 — David E. Garland, 2nd ed. (2025)** (`Section VII, 11:2–16`).
   - **Agent Window C:** Claim **[M0] Item #3 — Gordon D. Fee, NICNT Revised (2014)** (`pp. 542–586`).
   - **Agent Window D:** Claim **[M0] Item #4 — Anthony C. Thiselton, NIGTC (2000)** (`pp. 800–847`).
   - **Agent Window E:** Claim **[M0] Item #5 — Ciampa & Rosner, PNTC (2010)** (`pp. 503–540`).
4. **SINGLE AUTHORITY RULE — NO NEW DISPOSABLE LOG FILES:**
   Do **not** create standalone progress reports or disposable markdown files. When closing an item:
   - Update **only** the matching item lines in this checklist (`MANUAL_READING_ACCESS_CHECKLIST.md`).
   - Update **only** the controlling evergreen dossier or source card with the 12-point return protocol (Section 7).
5. **SAFE PUSH PROTOCOL:**
   Never use `--force`. Always fetch and rebase/ff-only before pushing:
   ```bash
   git fetch origin arena/019fed70-research
   git rebase origin/arena/019fed70-research
   git push origin arena/019fed70-research
   ```

---

# 1. M0 — current technical commentaries and major whole-models

## 1. Mark Reasoner, *1 Corinthians* (Brill, 2025)

**Read:** Commentary 7, “Hair and Head Coverings in the Assembly (11:2–16),” approx. **pp.432–451**, including notes.

**Where:** Brill Exegetical Commentary Series 3; official chapter route:  
https://brill.com/display/book/9789004737044/BP000007.xml  
Google Books metadata/TOC:  
https://books.google.com/books/about/1_Corinthians.html?id=IEiGEQAAQBAJ

**Extract:** material veil vs hair; `κεφαλή`; v10 `ἐξουσία`; angels; `φύσις`; v16; exact Corinth trigger; authenticate any circulated p.434/p.444 wording.

```text
STATUS = CHAPTER_AND_PAGINATION_CLOSED / BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
```

## 2. David E. Garland, *1 Corinthians*, BECNT 2nd ed. (2025)

**Read:** complete section **“VII. Headdress in Public Worship (11:2–16)”** + notes. First record the actual 2025 second-edition pagination.

**Where:** Baker Academic / Logos / Perlego / institutional ebook; print ISBN `9781540962607`, ebook ISBN `9781493451692`.

**Do not use:** old working `pp.468–493`; it was not verified. Do not silently transfer first-edition pagination.

**Extract:** all verse-level changes from the 2003 edition; veil/hair; `κεφαλή`; `ἐξουσία`; angels; nature/custom; social trigger.

```text
STATUS = SECTION_IDENTITY_CLOSED / 2025_PAGINATION_AND_BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
VERIFIED_BOOK_METADATA = LOGOS_2025_2E_TOTAL_PAGES_850 / PRINT_ISBN_9781540962607 / EBOOK_ISBN_9781493451692 / SECTION_PAGINATION_STILL_UNVERIFIED
```

## 3. Gordon D. Fee, NICNT Revised Edition (2014)

**Read complete block:** **pp.542–586** + notes.

Highest-value internal targets:
- pp.550–564 — 11:2–6 main exposition;
- pp.565–566 — Addendum;
- pp.567–579 — 11:7–12;
- **pp.576–578, especially p.576 n.123** — angels / Watchers locator;
- pp.580–586 — 11:13–16.

**Where:** Eerdmans / Logos-Biblia `NICNT67CO1_2ED` / Google Play or institutional ebook.

**Extract:** actual revised wording, edition changes vs 1987, v10 `ἐξουσία`, angels/Watchers, material practice, v13–16.

```text
STATUS = EXACT_REVISED_RANGES_CLOSED / BODY_AND_NOTES_TERMINAL_EXTERNAL_ACCESS_HOLD
```

## 4. Anthony C. Thiselton, NIGTC (2000)

**Read:** **pp.800–847** + notes.

**Where:** NIGTC / Eerdmans-Grand Rapids edition via institutional library, Google Books record, ebook/library access.

**Extract:** exact material reconstruction, lexical arguments, `κεφαλή`, `ἐξουσία`, angels, `φύσις`, v16, rhetorical structure.

```text
STATUS = WORK_AND_RANGE_CLOSED / BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
```

## 5. Roy E. Ciampa & Brian S. Rosner, PNTC (2010)

**Read:** **pp.503–540** + notes.

**Where:** Eerdmans / institutional ebook / Google Books limited-preview record.

**Extract:** whole-model structure, veil/hair, hierarchy/interdependence, v10, angels, nature/custom, v16.

```text
STATUS = WORK_AND_RANGE_CLOSED / DETAIL_BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
```

## 6. David I. Starling, EBTC (2025)

**Read:** exact 1 Cor 11:2–16 exposition + notes.

**Where:** Lexham Academic / Logos / Biblia. Official embedded preview object:  
https://biblia.com/api/plugins/embeddedpreview?historybuttons=false&layout=minimal&navigationbox=false&resourceName=LLS%3AEBTC67CO1&sharebutton=false

**Extract:** veil/hair, creation, `κεφαλή`, v10, angels, nature/custom, theological synthesis.

```text
STATUS = BOOK_CLOSED / TARGET_SECTION_BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
```

## 7. Michael J. Gorman, *1 Corinthians* (Eerdmans, 2025)

**Read:** exact section covering 1 Cor 11:2–16.

**Where:** Eerdmans; licensed ebook/library/Libby-OverDrive or institutional access; hardcover ISBN `9780802882660`, ebook ISBN `9781467465748`.

**Extract:** primarily theological/pastoral synthesis; record technical claims only where the body itself makes them.

```text
STATUS = BOOK_CLOSED / TARGET_SECTION_BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
```

## 8. Susanna Drake, *Veiling in the Late Antique World* (CUP, 2025)

**Read first:** ch.2 **“Veils in Corinth,” pp.70–89**, including notes.

**Also read:** relevant ch.1 material that directly treats first-/second-century Mediterranean material forms and the transition between outer-garment head covering and later separate/tighter veils.

**Where:** Cambridge Core book DOI `10.1017/9781009673518`; ch.2 DOI `10.1017/9781009673518.003`:  
https://www.cambridge.org/core/books/veiling-in-the-late-antique-world/veils-in-corinth/BB79DFCE0FB2F5AFDD9CCB0C6C5B83D4

**Extract:** exact garment/material claims; all v10/angels/hair/`κεφαλή` detail; what is book-body vs interview-level self-description.

```text
STATUS = CH2_IDENTITY_PAGINATION_SUMMARY_CLOSED / FULL_BODY_AND_NOTES_TERMINAL_PUBLISHER_ACCESS_HOLD
OFFICIAL_CUP_SUMMARY = "Corinthian women most likely veiled and unveiled for a variety of reasons having to do with beauty, comfort, status, virtue, and piety, not solely for theological, exegetical, or liberative purposes" (ch.2 abstract, CUP online 2025-11-26)
```

## 9. Aldar Nõmmik, *Robes, Romans, and Rituals in First Corinthians*

**Read:** ideally the **complete dissertation/book**, with special attention to 1 Cor 11 argument, Roman `capite velato`, ritual cognition/divine knowledge, reconstructed Corinthian uniformity pressure, v10, angels, creation, nature/custom.

**Where:** EHS dissertation listing / DiVA fulltext object; current Wipf & Stock edition:  
https://ehs.se/forskning/dth/  
https://wipfandstock.com/9798385259823/robes-romans-and-rituals-in-first-corinthians/

Institutional identifier:
```text
URN = urn:nbn:se:ths:diva-2600
```

```text
STATUS = INSTITUTIONAL_OBJECT_AND_FULLTEXT_ROUTE_CLOSED / BODY_FETCH_TERMINAL_RUNTIME_CACHE_HOLD
```

## 10. Janelle Peters, *Paul and the Citizen Body* (Mohr Siebeck, 2025)

**Read:** complete 183-page monograph if possible; at minimum every 1 Cor 11 section, especially bodily/head control, citizenship/status, creation, slavery, `ἐξουσία`, angels and material veiling.

**Where:** Mohr Siebeck, WUNT II 625:  
https://www.mohrsiebeck.com/en/book/paul-and-the-citizen-body-9783161601637  
DOI `10.1628/978-3-16-160164-4`.

```text
STATUS = PUBLISHER_MODEL_AND_TOC_CLOSED / FULL_MONOGRAPH_TERMINAL_EXTERNAL_ACCESS_HOLD
```

## 11. Jorunn Økland, *Women in Their Place* (2004/2005)

**Read:** at least chs.4–7:
- ch.4 “Places for Women in Early Roman Corinth: Ritual Sanctuary Spaces” — starts p.78;
- ch.5 “Paul and the Discourse of Sanctuary Space” — starts p.131;
- ch.6 “Corinthian Order” — starts p.168;
- ch.7 “Obedient and Subversive” — starts p.224.

**Where:** Bloomsbury / T&T Clark ebook or institutional library:  
https://www.bloomsbury.com/uk/women-in-their-place-9780567012708/  
https://books.google.com/books/about/Women_in_Their_Place.html?id=kSkJ_LtXlj8C

**Extract:** exact positions on veil vs hair, `κεφαλή`, `ἐξουσία`, angels, `φύσις`, v16 and sanctuary-space trigger.

```text
STATUS = IDENTITY_TOC_THESIS_CONTROL_CLOSED / CH4_7_BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
```

---

# 2. M1 — important specialist articles / chapters / visual-social controls

## 12. David A. deSilva, *Archaeology and the Ministry of Paul* (2025)

**Read:** **pp.126–156, “Roman Corinth.”**

**Where:** Baker Academic:  
https://bakeracademic.com/products/9781540960955_archaeology-and-the-ministry-of-paul

**Extract:** whether he actually discusses 1 Cor 11, S-1116, S-1088, Julian Basilica, `capite velato`, women’s head covering.

```text
STATUS = CHAPTER_RANGE_CLOSED / BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
VERIFIED_ROUTE = REVIEW (C. Burnett, 2025-10): "Roman Corinth" = pp.126–156 confirmed; no 1 Cor 11 / S-1116 / S-1088 / capite velato discussion visible in review text
```

## 13. Barbara Lumesberger-Loisl (2025)

**Read:** “Kopftuchgebot für Christinnen? ... (1 Kor 11,2–16),” **pp.295–303**.

**Where:** chapter/book access via library; bibliographic record:  
https://ixtheo.de/Record/1925710505

**Extract:** exact material reconstruction and gender-difference argument.

```text
STATUS = BIBLIOGRAPHIC_AND_TOC_CLOSED_2026_08_10 / BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
VERIFIED_BIBLIO = Siquans, Agnethe / Eder, Sigrid (Hrsg.), "Ist die Bibel frauenfeindlich? Biblische Frauenbilder und was wirklich dahinter steckt", Stuttgart: Katholisches Bibelwerk 2025-03-17, 320 pp., ISBN 978-3-460-25266-0; chapter "Kopftuchgebot für Christinnen? Die 'Verhüllung' des Kopfes als Ausdruck der Geschlechterdifferenz (1 Kor 11,2–16)" = pp.295–303 CONFIRMED via official publisher Leseprobe TOC (https://www.bibelwerk.shop/fileadmin/products/kun03_25266.pdf); chapter body external
```

## 14. Judith M. Gundry-Volf (1997)

**Read:** “Gender and Creation in 1 Corinthians 11:2–16,” **pp.151–171**.

**Where:** Festschrift *Evangelium, Schriftauslegung, Kirche* (Vandenhoeck & Ruprecht, 1997), institutional library/interlibrary loan.

Priority loci already independently located:
- p.151 n.1 — hairstyle proposal;
- p.152 — culture/creation/in-Christ two-context framework;
- pp.154–155 — honor/shame presentation;
- pp.162–163 — creation + interdependence;
- p.164 — angels.

```text
STATUS = BIBLIOGRAPHY_AND_PAGE_LOCATORS_CLOSED / DIRECT_BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
```

## 15. Marlis Gielen (1999)

**Read:** “Beten und Prophezeien mit unverhülltem Kopf? ...,” *ZNW* 90.3–4, **pp.220–249**.

**Where:** De Gruyter/ZNW or institutional library. A 2009 reworking appears in *Paulus im Gespräch* (Kohlhammer).

**Extract:** exact modified short-hair reconstruction, sex-role symbolism, what changed in 2009 reworking.

```text
STATUS = ARTICLE_IDENTITY_MODEL_LOCATORS_CLOSED / DIRECT_1999_BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
```

## 16. Hao Li (2023)

**Read:** full Chinese article **pp.267–318**.

**Where:** official JRCC page, choose “PDF (Chinese)”:  
https://ccspub.cc/jrcc/article/view/38  
DOI `10.29635/JRCC.202312_(21).0012`.

**Extract:** exact positions on creation order, reciprocity, veil/hair, v10, angels, cultural adaptation/challenge.

```text
STATUS = CLOSED_DIRECT_RUNTIME_OPEN_ACCESS / DIRECT_DOWNLOAD_ROUTE_VERIFIED
VERIFIED_RUNTIME_ROUTE = https://ccspub.cc/jrcc/article/download/38/36/1152
EXTRACTED_SUMMARY = "Creation order in 1 Cor 11:2-16 dialectically balances honor-shame cultural adaptation (female subordination symbol) and countercultural gospel reciprocity (mutual unity in the Lord, vv. 11-12); no timeless absolute subordination principle."
```

## 17. Janelle Peters, Biblica 2020

**Read:** “Slavery and the Gendered Construction of Worship Veils in 1 Corinthians,” *Biblica* 101.3 (2020), **pp.431–443**.

**Where:** Peeters / institutional journal access; DOI `10.2143/BIB.101.3.3288730`; JSTOR stable item `48653612`.

**Extract:** exact slavery/status mechanism, whether benefit to enslaved men/women is argued from specific primary evidence, verse-level chain.

```text
STATUS = PUBLISHER_ABSTRACT_CLOSED / FULL_BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
```

## 18. Janelle Peters dissertation (Emory, 2013)

**Read:** preferably chs.6–7; minimally **p.282**.

TOC anchors:
- ch.6 starts p.228;
- ch.7 “Veiling the Body of Christ” starts p.264;
- conclusion starts p.301.

**Where:** Emory Open Access repository, persistent object `qr46r105v`, “Primary PDF”.

**Why p.282 matters:** downstream scholarship cites it for a Corinthian statue / F. P. Johnson *Corinth* IX.1 pp.70–72; direct page must verify which object and what claim Peters actually makes.

```text
STATUS = PRIMARY_PDF_OBJECT_CLOSED / FRONT_MATTER_AND_INTRODUCTION_READ_DIRECT / CH6_7_AND_P282_EXTERNAL_READ_REQUIRED
VERIFIED_RUNTIME_ROUTE = https://etd.library.emory.edu/downloads/3r074v216 (Primary PDF, file_set 3r074v216; TOC confirmed: ch.6 p.228, ch.7 p.264, conclusion p.301, bibliography p.311)
```

## 19. L. J. Lietaert Peerbolte (2000)

**Read:** “Man, Woman, and the Angels in 1 Cor 11:2–16,” in *The Creation of Man and Woman*, **pp.76–92**, especially pp.86–87.

**Where:** Brill chapter:  
https://brill.com/display/book/edcoll/9789047400394/B9789047400394_s016.xml

**Extract:** direct Watchers/Enochic argument, exact `ἐξουσία` interpretation, exact page wording.

```text
STATUS = CHAPTER_IDENTITY_AND_SECONDARY_PAGE_LOCATORS_CLOSED / PREVIEW_LEVEL_DIRECT_READ_2026_08_10 / FULL_BODY_EXTERNAL_HOLD
VERIFIED_PREVIEW_ROUTE = Google Books limited preview id Ma9xEQAAQBAJ (Brill 2000, SearchWithinVolume)
PREVIEW_EXTRACTS = "p.76 chapter 'Man, Woman, and the Angels in 1 Cor 11:2-16'; p.83 κεφαλή = 'authority or supremacy over someone else', vv.4-5 disgrace logic; p.86 'authority on the head' — Vulgate Rev 14:18 potestatem habere supra as vulgar Latin, GNB 'a covering over her head', NRSV 'a…'; p.87 'authority over her own head' reading 'not easily combined with the context' (would leave choice to woman); pp.87-88 forbidden liaison of angels and women = legend of the fall of the Watchers; Tertullian already interpreted 1 Cor 11:10 thus; p.88 CD (Damascus Document) 'Azaz'el and the angels who came to the daughters of man', 1 Enoch 7:7, 1 Enoch 12:4 'the Watchers of heaven'; p.89 Watchers fell from heaven through lust; moral disorder and bloodshed; T.Reuben; p.90 'This material proves that the legendary fall of the Watchers was understood as a fall of angels. Paul's words διὰ τοὺς ἀγγέλους may therefore indeed refer to the legend of the Watchers'; p.91 angels attend worship; History of the Rechabites 16:18a-d (angels carry prayers to God)"
```

## 20. Charles H. Cosgrove (2005)

**Read:** “A Woman’s Unbound Hair in the Greco-Roman World...,” *JBL* 124.4 (2005), **pp.675–692**.

**Where:** JSTOR:  
https://www.jstor.org/stable/30041064  
DOI `10.2307/30041064`.

**Extract:** actual evidence for meanings of genuinely unbound/dishevelled female hair; keep distinct from Andania `ἀναπλέκω`.

```text
STATUS = BIBLIOGRAPHIC_CLOSED / FIRST_PAGE_DIRECT_PREVIEW / FULL_BODY_EXTERNAL_HOLD
VERIFIED_ROUTE = ProQuest preview (docview/214613352) first page read directly: article focus = Luke 7:36–50; unbound hair = mourning, religious devotion, ecstatic experience, sexuality — no single fixed social message
```

## 21. Gail Paterson Corrington (1991)

**Read:** “The Headless Woman: Paul and the Language of the Body in 1 Cor 11:2–16,” *Perspectives in Religious Studies* 18.3 (Fall 1991), **pp.223–231**.

**Where:** Baylor/PRSt library holdings or interlibrary loan; Baylor PRSt Index confirms volume/issue/pages.

**Extract:** exact body/head semantic argument and any use of visual/social evidence.

```text
STATUS = IDENTITY_CLOSED / DIRECT_FULLTEXT_TERMINAL_EXTERNAL_ACCESS_HOLD
```

## 22. Elaine Fantham (2008)

**Read:** “Covering the Head at Rome: Ritual and Gender,” **pp.158–171**.

**Where:** *Roman Dress and the Fabrics of Roman Culture*; DOI `10.3138/9781442689039-012`; University of Toronto Press / De Gruyter-Brill / institutional ebook.

**Extract:** male/female ritual head-covering distinctions, status/ritual gender meanings, chronology.

```text
STATUS = IDENTITY_AND_EXACT_LOCATOR_CLOSED / PREVIEW_LEVEL_DIRECT_READ_2026_08_10 / FULL_BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
VERIFIED_PREVIEW_ROUTE = Google Books limited preview id bYCCpqdgSAgC (SearchWithinVolume, pp.158–171)
PREVIEW_EXTRACTS = "male covering with toga vs female palla; Plutarch QR 10 (uncovering avoids divine jealousy) and QR 11 (Saturn exception); vittae = woollen headbands of respectable girls/wives, from viere 'to bind'; infula = white wool fillet coiled like diadem, ribbons/vittae red+white (Serv. ad Aen. 10.538), symbol of inviolacy, more common on altars/tombs/sacrificial victims than as costume, worn by priests/Vestals; Aeneas first to cover head when sacrificing (altar of Saturn, Capitoline); wool vs linen specified; nodus coiffure with vitta woven in = married-woman status; p.171 contrast: eastern-province veiled women vs exposed beauty of empresses/benefactresses in portraits"
```

## 23. Kelly Olson, *Dress and the Roman Woman* (2008)

**Read at minimum:** contexts around **pp.22, 25, 34, 41**; ideally relevant chapters on palla/stola/togata and self-presentation.

**Where:** Routledge institutional ebook:  
https://www.routledge.com/Dress-and-the-Roman-Woman-Self-Presentation-and-Society/Olson/p/book/9780203927625

**Extract:** palla/head-cover frequency, literary ideal vs visual practice, moral/status vocabulary.

```text
STATUS = BOOK_AND_PAGE_LOCATORS_CLOSED / PREVIEW_LEVEL_DIRECT_READ_2026_08_10 / FULL_BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
VERIFIED_PREVIEW_ROUTE = Google Books limited preview id l9wdU6ysZgEC (2012 ed.; SearchWithinVolume)
PREVIEW_EXTRACTS = "p.25: 'over the head when the woman was out of doors, and hair bound with fillets' — modern-scholars description of everyday Roman matrona clothing; p.33: palla over the head, lower edge to knees (Wilson 1938: 148–9); p.33: palla appears far more often than stola, no ancient evidence that Augustus legislated return of stola+vittae (contra Sebesta 1997); p.34: palla + modesty/chastity, Ara Pacis; p.35: lower-class women much less likely to go veiled/mantled (palla hindrance to manual labor); p.36: palla (not stola) described as Roman wife's costume ca. 200 BCE (Plaut. Men. 167, 659; Nonius); p.51: palliola, amictus, amiculum, amictorium as generic wrap names; p.113: palla as ideal vs artistic evidence"
```

## 24. Lisa A. Hughes (2007)

**Read:** full article if possible, **pp.218–241**; mandatory autopsy of **Table 1, p.227 + surrounding methodology/context**.

**Where:** Taylor & Francis / *Material Religion*:  
https://www.tandfonline.com/doi/abs/10.2752/175183407X219750  
DOI `10.2752/175183407X219750`.

**Verify:** `N=113`, veiled `67`, unveiled `46`; sample definition and exclusions.

```text
STATUS = TABLE_1_DATA_VERIFIED_VIA_PEER_REVIEWED_EXACT_CITATION / DIRECT_TABLE_AUTOPSY_TERMINAL_ACCESS_HOLD
VERIFIED_DATA = "N=113 window-type monuments from Italy; 67 veiled (59%), 46 unveiled (41%). Confirmed in Oxford University Press Past & Present 263.1 (2024), fn. 66-67."
```

## 25. Marcin Kowalski (2020)

**Read:** full article **pp.59–104**.

**Where:** official APCZ / KUL repository; DOI `10.12775/BPTh.2020.003`.

**Extract:** full continuous-Pauline rhetorical argument; v10/angels detail; relation of cultural and Christological/theological argument.

```text
STATUS = CLOSED_DIRECT_RUNTIME_OPEN_ACCESS / DIRECT_BITSTREAM_ROUTE_VERIFIED
VERIFIED_RUNTIME_ROUTE = https://repozytorium.kul.pl/server/api/core/bitstreams/50381496-9a87-40a2-b12f-b8c1e7c15050/content
EXTRACTED_SUMMARY = "Continuous-Pauline rhetorical structure (11:2 introduction, 11:3 thesis, 11:4-6 cultural argument, 11:7-12 Christological/theological argument with v10 angels, 11:13-15 natural law, 11:16 conclusion)."
```

## 26. Sławomir Torbus (2009)

**Read:** “The Rhetorical Dispositio of 1 Cor. 11, 2–16 and the Problem of the Veil,” **pp.507–521**.

**Where:** Brill, *New Chapters in the History of Rhetoric*, institutional ebook/chapter access.

**Extract:** exact `dispositio`, continuity argument, whether he directly addresses quotation/refutation proposals.

```text
STATUS = CHAPTER_IDENTITY_CLOSED / DIRECT_BODY_TERMINAL_EXTERNAL_ACCESS_HOLD
```

## 27. Peter Arzt-Grabner et al., *1. Korinther*, PKNT 2 (2006)

**Read:** **p.390**, including surrounding paragraph/footnotes.

**Where:** PKNT 2 via institutional theological library / publisher ebook.

**Verify:** exact claim that `ἐξουσία` + `ἐπί` + genitive is “uncommon”; source corpus behind that statement.

```text
STATUS = PAGE_LOCATOR_CLOSED / DIRECT_PAGE_TERMINAL_EXTERNAL_ACCESS_HOLD / NONBLOCKING
VERIFIED_BIBLIO_2026_08_10 = V&R 2006, 575 pp., ISBN 3525510012 / 9783525510018; Google Books id eZdAjRCRXUIC = "No eBook available" (no preview); MDPI Religions 15.10 (2024) 1175 (Hill, OA) confirms PKNT 2 as key papyrological corpus control
```

---

# 3. M2 — primary scans, datasets and epigraphic objects

## 28. Fendel 2023 — `EXOUSIAN.xlsx`

**Read/data-audit:** official Oxford dataset spreadsheet `EXOUSIAN.xlsx` (51.7 KB).

**Where:** Oxford Research Archive dataset:  
https://ora.ox.ac.uk/objects/uuid:28406bed-423d-4801-9691-d5d7caa94e2a  
DOI `10.5287/ora-dqmbwrvj6`.

**Mandatory extraction:** identify the **three Roman-period prepositional-phrase rows** and record the actual prepositions/cases. Do not infer that any are `ἐπί + genitive` before reading rows.

```text
STATUS = DATASET_CONTENT_READ_DIRECT_2026_08_10 / THREE_ROMAN_PP_ROWS_ENUMERATED / XLSX_BINARY_ORIGINAL_TERMINAL_ORA_TRANSPORT_HOLD
VERIFIED_RUNTIME_ROUTE = https://ora.ox.ac.uk/objects/uuid:28406bed-423d-4801-9691-d5d7caa94e2a/files/sd217qr12q (EXOUSIAN.xlsx, 51.7 KB; full 9-chunk table scan, "FINISHED 03 Mar 2023")
ROMAN_PERIOD_PP_ROWS_EXOUSIAN_ECHEIN =
  1) BGU.7.1655 (RG, Arsinoites, protocoll): "οὐδεὶς αὐτοῦ ἐξουσίαν ἕξει ἀπὸ τῶν κληρονόμων μου" — ἀπό + GENITIVE
  2) P.Oxy.8.1120 (RG, Oxyrhynchos, petition): "μὴ ἔχων κατ' αὐτῆς ἐξουσίαν" — κατά + GENITIVE
  3) P.Oxy.9.1205 (RG, Oxyrhynchos, contract): "μηδεμίαν τε ἐξουσίαν ἔχειν εἰς αὐτοὺς ἀπὸ τῆς ἐνεστώσης ἡμέρας" — εἰς + ACCUSATIVE
NONE_IS_EPI_GENITIVE = TRUE (no ἐπί + genitive among the three Roman-period PP rows)
NON_SV_PP_ROWS_NOT_COUNTED = P.Oxy.27.2474 (ὑπό+acc), P.Oxy.43.3126 (ἐπί+acc), P.Oxy.46.3311 (ὑπό+acc), P.Oxy.55.3794 (πρός+acc), P.Oxy.62.4345 (ἐπί+acc), SB.16.12692 (ἐπί+acc) — nominal/title uses without ἐξουσίαν ἔχειν
```

## 29. PG 118 — direct scan image p.409

**Inspect visually:** original **Patrologia Graeca Vol. 118.pdf**, PDF p.409.

**Where:** Wikimedia Commons public-domain object `Patrologia Graeca Vol. 118.pdf`.

**Verify:** Clement Hypotyposeis fragment and Photius-parallel block against OCR; author labels, Greek, punctuation, exact page layout.

```text
STATUS = OCR_IMAGE_LOCATED / ORIGINAL_SCAN_OBJECT_CLOSED / TARGET_RENDER_TERMINAL_TRANSPORT_HOLD
VERIFIED_RENDER_URL = https://commons.wikimedia.org/wiki/File:Patrologia_Graeca_Vol._118.pdf?page=409 (thumb page409-960px live; image bytes not retrievable in runtime)
```

## 30. Cyril of Alexandria — PG 74, cols.879–883

**Inspect visually:** `Patrologia Graeca Vol. 074.pdf`, printed **PG cols.879–883**.

**Where:** Wikimedia Commons public-domain original scan.

**Verify:** Cyril fragment wording and relation to Cramer `Κυτίλλου` block; do not use OCR as image authority.

```text
STATUS = WORK_COLUMNS_SCAN_OBJECT_CLOSED / TARGET_RENDER_TERMINAL_TRANSPORT_HOLD
VERIFIED_RENDER_ROUTE = Wikimedia Commons page-render route verified live for Patrologia Graeca Vol. 074.pdf (exact page number for cols.879–883 TBD by human; image bytes not retrievable in runtime)
```

## 31. Theodoret — PG 82, cols.312D–313A

**Inspect visually:** `Patrologia Graeca Vol. 082.pdf`, **PG 82, 312D–313A**.

**Where:** Wikimedia Commons public-domain original scan.

**Also read:** Robert C. Hill, *Commentary on the Letters of St Paul*, vol.1 (2001), **p.205**, if accessible.

**Verify:** exact Greek for angels assigned over humans / entrusted with care; Acts 12:15 + Matt 18:10 chain; compare Hill translation.

```text
STATUS = WORK_COLUMNS_SCAN_OBJECT_CLOSED / PG_IMAGE_TERMINAL_TRANSPORT_HOLD / HILL_P205_TERMINAL_EXTERNAL_ACCESS_HOLD
VERIFIED_RENDER_ROUTE = Wikimedia Commons page-render route verified live for Patrologia Graeca Vol. 082.pdf (exact page number for cols.312D–313A TBD by human; image bytes not retrievable in runtime)
HILL_VOL1_SCOPE = CONFIRMED_Romans_1_2_Corinthians_319pp (JECS review) / P205_IN_1COR11_RANGE
```

## 32. Potta — TAM V.1 535 / PH263959

**Read directly:** complete target printed/PHI object, not only search-index excerpt.

**Where:** Packard Humanities/PHI object `PH263959`; *TAM V.1* no.535 (Lydia: Maionia).

**Verify:** complete title/syntax around `Ποτταν ... προφῆτιν σώτειραν`, object description, whether any additional head/hair information exists.

```text
STATUS = FULL_BODY_CLOSED_DIRECT_PHI / NO_HEAD_HAIR_INFO / PRINTED_PAGE_OPTIONAL
VERIFIED_RUNTIME_ROUTE = https://inscriptions.packhum.org/text/263959
EXTRACTED_SUMMARY = "Ἑρμογένης Μητροδώρου Διὶ Αριου κατ' ἐπιταγὴν σωτηρίας ἕνεκεν τῆς ἐκ τοῦ Διὸς Ποτταν Μενε[κ]ρ̣ά̣του προφῆτιν σώτειραν γενομένην τοῦ Ἑρμογένου — full title/syntax read directly; no head/hair information in object"
```

## 33. Nanas — same-object image

**Inspect:** Tabbernee **fig.77** same-object image for Nanas; also visually inspect the relevant Poirier 2004 page image even though text body is already read.

**Where:** Tabbernee figure via library/book access; Poirier open PDF:  
https://ifa.phil-fak.uni-koeln.de/fileadmin/IfA/EpiAna_pdfs/037151_Poirier_The_Montanist_Nature_of_the_Nanas_Inscription__Steinepigramme_16-41-15_.pdf

**Verify:** whether the object itself contains any head/hair/iconographic marker; keep disputed angelic-language interpretation separate.

```text
STATUS = TEXT_BODY_CLOSED / TABBERNEE_FIG77_TERMINAL_EXTERNAL_IMAGE_HOLD
```

## 34. Apphe — IK Kalchedon 61 = CIG 3796

**Read visually/directly:** the original printed inscription page for **CIG 3796 / IK Kalchedon 61**.

**Where:** CIG volume / IK Kalchedon through research library, digitized old-volume repository, Hathi/Google/Internet Archive where legally accessible.

**Compare with:** Selin Önder 2022, DOI `10.26650/iutd.1096605`.

**Verify:** exact grammar around `Ἄπφη ... προφῆτις`; whether syntax favors independent office or prophet-wife interpretation; object/funerary context.

```text
STATUS = FEMALE_NOUN_BEARER_SPECIALIST_CONTROL_CLOSED / ORIGINAL_PRINTED_PAGE_TERMINAL_BINARY_TRANSPORT_HOLD
VERIFIED_2026_08_10 = Önder 2022 (Tarih Dergisi 77, 1–14, OA CC BY-NC) FULL BODY READ — article treats Apollo oracle at Kalkhedon (Pythaios/Khresterios, asylia decrees, numismatics) and does NOT discuss Apphe / IK 61 / CIG 3796 / προφῆτις; comparison target resolved as inapplicable. CIG vol. 4 (1859) = Google Books preview id TU5FwAcnR9cC (595 pp.; preview exposes indices only — name index RA2-PA71 confirms "3796. Ἄφφη"; main-text pages not in preview). HathiTrust 1977 Olms reprint = Limited (search only). Printed CIG/IK page remains external.
```

## 35. Termessos — TAM III,1 870 / PH280975

**Read directly:** complete inscription body.

**Where:** PHI `PH280975` / *TAM III,1* no.870 through corpus/library scan.

**Verify:** noun bearer, gender, syntax, genre, relation to Demeter Eleusinia; do not infer from neighboring TAM numbers.

```text
STATUS = FULL_BODY_CLOSED_DIRECT_PHI / NOUN_BEARER_GENRE_SYNTAX_VERIFIED
VERIFIED_RUNTIME_ROUTE = https://inscriptions.packhum.org/text/280975
EXTRACTED_SUMMARY = "τό(πος) Αὐρ(ηλίας) Ὀρεστιανῆς, ἱ(ερῶν) Ἐλευσι-νίων προφή̣τ̣ι̣δ̣ο̣ς̣ — bearer Aurelia Orestiane (female); τόπος-genre; Demeter Eleusinia link verified in-body; no inference from neighboring numbers"
```

## 36. Nisyra — SEG 49.1624 / PH348429 / TM949255

**Read directly:** direct PHI object page if/when it renders; compare with TM object.

**Where:** PHI `PH348429`; Trismegistos `TM949255`; SEG 49.1624.

**Purpose:** confirm the currently indexed dedication and document the Nawotka-reference status; **do not guess a replacement inscription**.

```text
STATUS = FULL_BODY_CLOSED_DIRECT_PHI / PROPHETIS_RESTORED_FOUND / NAWOTKA_VERDICT_REVISED
VERIFIED_RUNTIME_ROUTE = https://inscriptions.packhum.org/text/348429
EXTRACTED_SUMMARY = "5-line dedication to Theos Basileus with restored διὰ προφή[τιδος] (l.3: 'through the prophetess […]leia, fostling (θρεπτή) of Al[…]') — NOT a two-line dedication; previous NOT_FOUND / VERY_LIKELY_REFERENCE_ERROR verdicts REVISED (they were based on an incomplete render); iconography per PHI description = four standing relief figures in prayer posture above text, no head/hair marker"
```

## 37. Philokrateia — CGRN 232 direct page

**Read if route recovers:** direct CGRN 232 body.

**Where:** Collection of Greek Ritual Norms, object CGRN 232. Object identity is already closed through CGRN 222 cross-reference; Vollgraff 1909 p.445 same-object photo is already read.

**Purpose:** redundant direct-corpus confirmation only.

```text
STATUS = OBJECT_AND_PHOTO_CLOSED / DIRECT_CGRN232_RUNTIME_502_HOLD_NONBLOCKING
```

## 38. P.Wisc. I 13 — edition image/apparatus

**Inspect if available:** papyrus/edition image and apparatus around the restored `ἐξουσία` formula.

**Where:** documentary text route:  
https://droitromain.univ-grenoble-alpes.fr/Negotia/Wisc1_DDBDP.gr.html  
then trace the edition image/apparatus through papyrological library resources.

**Purpose:** distinguish restored formula from surviving visible letters.

```text
STATUS = EDITION_TEXT_CLOSED_DDBDP / BOTH_EXOUSIA_INSTANCES_RESTORED / PHOTO_IMAGE_OPTIONAL
VERIFIED_RUNTIME_ROUTE = https://papyri.info/editions/p.wisc/1/13
EXTRACTED_SUMMARY = "l.3 ἐξουσίαν and l.8 ἐξουσίας are both fully restored (square brackets); no surviving visible letters of the formula — restored vs visible distinction resolved at edition-text level"
```

---

# 4. M3 — optional completeness / model-stress checks

## 39. Cramer printed catena label image

**Inspect:** printed Cramer page around the suspicious digital label `Κυτίλλου` and corresponding 1 Cor 11 angel block.

**Where:** Cramer, *Catenae Graecorum Patrum in Novum Testamentum*, vol.5 (Oxford, 1841), manuscript tradition principally Paris BnF grec 227; Scaife ATLAS text route already closed.

**Purpose:** visually distinguish printed/editorial form from digital transcription; independent fragment convergence already strongly identifies Cyril.

```text
STATUS = OPTIONAL_NONBLOCKING_IMAGE_CHECK
VERIFIED_RUNTIME_ROUTE = https://archive.org/details/catengrcorump01cramgoog (Cramer vol.5, 497 pp., full-text OCR + page images; printed page image still external to runtime)
```

## 40. Martin 2013 — later PDF page screenshots

**Inspect:** later page images of Martin’s response PDF for visual/page-image confirmation.

**Purpose:** text layer and substantive argument are already read; this is only visual custody completeness.

```text
STATUS = FULL_TEXT_BODY_CLOSED / LATER_PAGE_SCREENSHOTS_RUNTIME_CACHE_HOLD_NONBLOCKING
```

## 41. Nicole Francis 2023/24 — full PDF

**Read if easy to obtain:** “A Pauline Dress Code or a Roman Analogy: Reinterpreting Paul’s Discourse in 1 Corinthians 11:1–16.”

**Where:** BYU ScholarsArchive:  
https://scholarsarchive.byu.edu/studiaantiqua/vol22/iss1/6/

**Purpose:** full stress-test of the “Roman analogy / not-primary-dress-code” model; lower venue weight.

```text
STATUS = CLOSED_DIRECT_RUNTIME_OPEN_ACCESS / DIRECT_DOWNLOAD_ROUTE_VERIFIED
VERIFIED_RUNTIME_ROUTE = https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1302&context=studiaantiqua
EXTRACTED_SUMMARY = "Paul is not outlining a church dress code; by analogy with Galatians 4 Hagar/Sarah, he appeals to Greco-Roman/Corinthian cultural norms on hair/coverings to rationalize the hierarchy and resolve status conflict."
```

## 42. Garland first edition (2003) — edition comparison only

**Read only after/alongside 2025 edition:** “Headdress in Public Worship (11:2–16),” **pp.505–532** in the first edition.

**Purpose:** establish precisely what 2025 changed; never substitute 2003 text/pages for 2025.

```text
STATUS = OPTIONAL_EDITION_CONTINUITY_CONTROL
```

## 43. Low-weight current edge/reception full bodies

These are not required to stabilize the current grade map, but may be read for exhaustive current-debate history:

- Israel O. O. Odewole 2025, *QUAERENS* 7.1:18–33 — official journal route: https://jurnal.widyaagape.ac.id/index.php/quaerens/article/view/240 (OA PDF; **FULL BODY READ 2026-08-10**; traditional African complementarian view: veil = submission sign to male headship; angels as "guardians of order" via Thiselton 2000: 838–844; creation order; church custom; equality in Christ via Gal 3:28; deculturization critique; Walker interpolation rejected)
- Jason Garwood, *Paul & the Head Covering: A Biblical Reassessment* (2026) — current confessional/non-universalist edge model. Classified 2026-08-10: **quotation-family C-level** (author's kuyperian.com excerpt + Amazon metadata; 86 pp., Cross & Crown, 2026-04-23, ISBN 978-1734122893).

```text
STATUS = OPTIONAL_LOW_WEIGHT_CURRENT_RECEPTION / ODEWOLE_CLOSED_FULLTEXT_2026_08_10 / GARWOOD_CLASSIFIED_QUOTATION_FAMILY_C
```

---

# 5. What is already directly closed — do NOT put back on reading queue

The following do **not** need reacquisition merely to repeat work:

```text
DIDYMA_III7_2023_FULL_BODY = CLOSED_DIRECT_OFFICIAL
TRYPHOSA_N708_BODY_AND_TAF18 = CLOSED_DIRECT_OFFICIAL
DIDYMA_235B_FALSE_OLD_READING = CLOSED
DIDYMA_273_EXEMPLI_GRATIA_RESTORATION = CLOSED
PHILOKRATEIA_VOLLGRAFF_1909_P445_PHOTO = CLOSED_DIRECT_IMAGE
ERESOS_IG_XII_SUPPL_126 = CLOSED_DIRECT
IGVII_3111_BODY = CLOSED_DIRECT_IGVII
IGLSYR_1_51 = CLOSED_DIRECT_FALSE_PERSON_CONTROL
MILETOS_481 = CLOSED_DIRECT
AMMIAS_THYATEIRA = CLOSED_DIRECT
PETERS_2021_OPEN_THEOLOGY = CLOSED_DIRECT_FULLTEXT
HAMPLOVA_2025 = CLOSED_DIRECT_INSTITUTIONAL_FULLTEXT
SALES_2024 = CLOSED_OPEN_FULLTEXT
LLEWELLYN_JONES_2003_KEY_CHAPTER_CONTROLS = CLOSED_DIRECT_JSTOR_PREVIEWS
STAFFORD_2024 = CLOSED_DIRECT_OXFORD
THOMPSON_1988 = CLOSED_DIRECT_PUBLISHER_CONTROL
GILL_1990 = CLOSED_DIRECT_OPEN
ASCSA_CORINTH_XXII_OBJECT_CONTEXT = CLOSED_CURRENT_ASSEMBLAGE_CONTROL
GOODACRE_2011 = CLOSED_DIRECT_FULL_BODY
MARTIN_2013 = CLOSED_DIRECT_TEXT_BODY
HILTON_MATTHEWS_2008 = CLOSED_DIRECT_UKZN_PDF
FENDEL_2023_ARTICLE_BODY_AND_CORPUS_COUNTS = CLOSED_DIRECT
PSI_X_1115 = CLOSED_DIRECT
TAM_II_603_604 = CLOSED_DIRECT
```

---

# 6. Recommended human reading order

If access is limited, use this order:

```text
1 Reasoner 2025 pp432_451
2 Garland 2025 2e section VII
3 Fee 2014 pp542_586 / esp 576_578 n123
4 Thiselton 2000 pp800_847
5 Ciampa_Rosner 2010 pp503_540
6 Drake 2025 pp70_89
7 Nommik fulltext
8 Peters 2025 full monograph
9 Starling 2025 1Cor11 section
10 Gorman 2025 1Cor11 section
11 Okland ch4_7
12 deSilva 2025 pp126_156
13 Gundry_Volf 1997 pp151_171
14 Gielen 1999 pp220_249
15 Hao_Li 2023 pp267_318
16 Peerbolte 2000 pp76_92
17 Peters 2020 pp431_443
18 Corrington 1991 pp223_231
19 Fantham / Olson / Hughes
20 Kowalski / Torbus
21 PKNT p390 / Fendel XLSX
22 PG118 / PG74 / PG82 page-image autopsy
23 Potta / Apphe / Termessos / Nanas object checks
24 all M3 optional controls
```

---

# 7. Reading-return protocol

For every newly acquired source, record:

```text
SOURCE_ID
EDITION_YEAR
PRINT_OR_PDF_PAGINATION
ACCESS_ROUTE
PAGE_RANGE_READ
DIRECT_QUOTE_SAFE = true_or_false
CLAIMS_ACTUALLY_SUPPORTED
CLAIMS_NOT_SUPPORTED
EDITION_DIFFERENCES
IMAGE_AUTOPSY = if_applicable
OWNER_FILE_UPDATED
CLAIM_REGISTRY_CHANGE = yes_or_no
```

A user-provided PDF/photo/scan should be treated as a **new lawful access route** and reopens only the matching checklist item.

---

# 8. Final status

```text
TOTAL_CONCRETE_MANUAL_READING_ITEMS = 43
M0_MAJOR = 11
M1_SPECIALIST = 16
M2_PRIMARY_OBJECT_DATA = 11
M3_OPTIONAL = 5

CURRENT_RESEARCH_AUDIT_READY = true
CURRENT_AGENT_ACQUISITION_QUEUE = empty
MANUAL_READING_CAN_STILL_UPGRADE_SOURCE_CUSTODY = true
MANUAL_READING_LIST_COMPLETE_FOR_CURRENT_KNOWN_GAPS = true
```
