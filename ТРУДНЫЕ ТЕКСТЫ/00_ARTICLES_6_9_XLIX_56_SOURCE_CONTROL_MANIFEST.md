# Статьи 6–9: контрольный manifest 56 источников и web-loci

**Дата:** 24 июля 2026 года  
**Статус:** `MARATHON-XLIX / 56-CONTROL-NODES / OFFICIAL-FIRST / PRIMARY-LINE-RESOLVED / RIGHTS-AUDITED / ACCESS-FAILURES-RECORDED`

---

## 1. Как считать этот manifest

Это не заявление, что 56 книг прочитаны от первой до последней страницы.

В manifest входят разные уровни проверки:

- `DIRECT-OFFICIAL` — официальный сайт института, издателя или владельца рукописи;
- `DIRECT-PRIMARY-TEXT` — непосредственно прочитанный греческий или рукописный текст;
- `DIRECT-FULL-FILE` — полный PDF/EPUB проверен в локальном корпусе;
- `PUBLISHER-METADATA` — библиография и аннотация проверены у издателя;
- `RIGHTS-CONTROL` — проверены правила воспроизведения изображения или текста;
- `ACCESS-BLOCKED` — источник найден, но полный текст или интерактивный аппарат не получен;
- `SECONDARY-LOCATOR` — точная страница известна через проверенный научный источник, но сама книга не открыта напрямую.

Правило результата:

```text
КОЛИЧЕСТВО ССЫЛОК
≠
КОЛИЧЕСТВО НЕЗАВИСИМЫХ АРГУМЕНТОВ

МЕТАДАННЫЕ
≠
ПРОЧИТАННАЯ СТРАНИЦА

ПРИНЯТАЯ СТРОКА ECM
≠
ПОЛНЫЙ АППАРАТ СВИДЕТЕЛЕЙ
```

---

# A. ECM, NA28 и CBGM — 11 контрольных узлов

1. [INTF — Genealogical Queries 2.0](https://intf.uni-muenster.de/cbgm/index_en.html) — `DIRECT-OFFICIAL`; база второго издания ECM Соборных посланий.
2. [INTF — Genealogical Queries 1.0](https://intf.uni-muenster.de/cbgm/en.html) — `DIRECT-OFFICIAL`; библиография первых выпусков ECM.
3. [INTF — Nestle–Aland 28](https://intf.uni-muenster.de/NA28/en.html) — `DIRECT-OFFICIAL`; издание и набор официальных corrections/downloads.
4. [INTF — Textual Changes in NA28](https://intf.uni-muenster.de/NA28/files/TextChangesNA28.pdf) — `DIRECT-OFFICIAL-PDF`; прямо утверждает принятие текста Соборных посланий из ECM2.
5. `INTF — Orthographical Standardization in NA28` — `DIRECT-OFFICIAL-INDEXED`; методический контроль, не источник новых вариантов наших стихов.
6. `INTF — Split Primary Line in ECM2` — `DIRECT-OFFICIAL-INDEXED`; контроль того, что primary line иногда бывает разделённой.
7. `INTF — Text attestation where the primary line is split in ECM2` — `DIRECT-OFFICIAL-INDEXED`; свидетельская аттестация split readings.
8. `INTF — Corrections, 2nd printing 2013` — `DIRECT-OFFICIAL-INDEXED`; проверка возможных исправлений NA28.
9. `INTF — Additional corrections, 2nd printing` — `DIRECT-OFFICIAL-INDEXED`.
10. `INTF — Corrections, 3rd–5th printings` — `DIRECT-OFFICIAL-INDEXED`; проверено отсутствие опубликованной коррекции, меняющей наши пять основных loci.
11. `ECM IV Catholic Letters, 2nd rev. ed., Stuttgart 2013` — `OFFICIAL-BIBLIOGRAPHIC-CONTROL`; физический полный аппарат остаётся `ACCESS-PENDING`.

---

# B. SBLGNT и сравнительный apparatus — 10 узлов

12. [SBL — SBL Greek New Testament](https://www.sbl-site.org/resources/digital-texts/sbl-greek-new-testament/) — `DIRECT-OFFICIAL`.
13. [SBL — Digital Texts](https://www.sbl-site.org/resources/digital-texts/) — `DIRECT-OFFICIAL`; поясняет отличие edition-comparison apparatus от рукописного аппарата.
14. [SBLGNT — 1 Peter PDF](https://www.sblgnt.com/download/revint/81-1%20Peter.pdf) — `DIRECT-PRIMARY-TEXT`.
15. [SBLGNT — 2 Peter PDF](https://www.sblgnt.com/download/revint/82-2%20Peter.pdf) — `DIRECT-PRIMARY-TEXT`.
16. [SBLGNT — Jude PDF](https://www.sblgnt.com/download/revint/86-Jude.pdf) — `DIRECT-PRIMARY-TEXT`.
17. [SBLGNT apparatus — comparison with ECM](https://biblia.com/books/sblgntapp/article/INTRO.11) — `DIRECT-COMPARATIVE-APPARATUS`; перечисляет все 39 расхождений SBLGNT/ECM в Соборных посланиях.
18. [Faithlife SBLGNT source repository](https://github.com/Faithlife/SBLGNT) — `DIRECT-OFFICIAL-SOURCE`; CC BY 4.0.
19. [SBLGNT front matter](https://www.sbl-site.org/assets/pdfs/bibletexts/SBLGNT/01-SBLGNT-Front.pdf) — `DIRECT-OFFICIAL-PDF`; описывает природу аппарата.
20. `SBLGNT direct text: 1 Pet 3:18` — `DIRECT-PRIMARY-TEXT`; чтение `ἔπαθεν`.
21. `SBLGNT direct text: 1 Pet 4:6` — `DIRECT-PRIMARY-TEXT`; `νεκροῖς εὐηγγελίσθη`, без `νῦν`.

---

# C. Ключевые ECM/SBLGNT loci — 5 отдельных проверок

22. `2 Pet 2:4` — SBLGNT `σειραῖς ζόφου`; locus отсутствует среди 39 расхождений с ECM — `ECM2-PRIMARY-LINE-RESOLVED`.
23. `Jude 14` — SBLGNT `Ἰδοὺ ἦλθεν κύριος ἐν ἁγίαις μυριάσιν αὐτοῦ`; locus отсутствует среди расхождений — `ECM2-PRIMARY-LINE-RESOLVED`.
24. `Jude 15` — SBLGNT `πάντας τοὺς ἀσεβεῖς`, ECM `πᾶσαν ψυχήν` — `EXPLICIT-ECM-DIFFERENCE-RESOLVED`.
25. `1 Pet 3:18` — SBLGNT `ἔπαθεν`; locus отсутствует среди расхождений — `ECM2-PRIMARY-LINE-RESOLVED`.
26. `1 Pet 4:6` — SBLGNT без `νῦν`; locus отсутствует среди расхождений — `ECM2-PRIMARY-LINE-RESOLVED`.

---

# D. P72 / Bodmer VII–VIII — 7 узлов

27. [CSNTM — Manuscript P72](https://manuscripts.csntm.org/Manuscript/Group/GA_P72) — `DIRECT-OFFICIAL-METADATA`; III–IV век, Bodmer VII–VIII, 95 листов.
28. `CSNTM P72 — 1 Pet 3:16–22 image group` — `DIRECT-COVERAGE-VERIFIED`.
29. `CSNTM P72 — 1 Pet 4:4–11 image group` — `DIRECT-COVERAGE-VERIFIED`.
30. `CSNTM P72 — 2 Pet 2:2–8 image group` — `DIRECT-COVERAGE-VERIFIED`.
31. `CSNTM P72 — Jude 13–18 image group` — `DIRECT-COVERAGE-VERIFIED`.
32. [DigiVatLib — Pap.Bodmer.VIII](https://digi.vatlib.it/view/MSS_Pap.Bodmer.VIII) — `DIRECT-OFFICIAL-IMAGE-OBJECT`.
33. [Vatican Library — Reproductions and Rights](https://www.vaticanlibrary.va/en/information-for-readers/photographic-reproductions.html) — `RIGHTS-CONTROL`; публикация требует отдельного разрешения.

---

# E. 4Q204 / 4QEnochᶜ — 8 узлов

34. [IAA — 4Q Enoch / 4Q204](https://www.deadseascrolls.org.il/explore-the-archive/manuscript/4Q204-1?locale=en_US) — `DIRECT-OFFICIAL-ARCHIVE`.
35. [IAA image B-359409](https://www.deadseascrolls.org.il/explore-the-archive/image/B-359409) — Plate 189, Fragment 1, full spectrum; `DIRECT-OFFICIAL-OBJECT-LOCATOR`.
36. [IAA image B-359410](https://www.deadseascrolls.org.il/explore-the-archive/image/B-359410) — Plate 189, Fragment 1, infrared; `DIRECT-OFFICIAL-OBJECT-LOCATOR`.
37. [IAA Terms & Conditions](https://www.deadseascrolls.org.il/terms) — `RIGHTS-CONTROL`; воспроизведение требует предварительного письменного разрешения.
38. Milik, *The Books of Enoch*, с. 183 — `DIRECT-FULL-FILE`; рукописный контекст.
39. Milik, с. 184 — `DIRECT-FULL-FILE`; транскрипция 4QEnᶜ 1 i 15–17.
40. Milik, с. 185–186 — `DIRECT-FULL-FILE`; перевод, скобки и комментарий.
41. Milik, Plate IX — `DIRECT-PLATE-REGISTERED`; фотографическое сопоставление с современным IAA-объектом требует осторожного crosswalk.

---

# F. Другие рукописные и цифровые контроли — 4 узла

42. [Codex Sinaiticus — Advanced Search](https://www.codexsinaiticus.org/en/search.aspx) — `DIRECT-OFFICIAL`; точный folio наших loci не извлечён из-за нестабильной passage-навигации.
43. [Codex Sinaiticus — electronic edition description](https://www.codexsinaiticus.org/en/project/edition.aspx) — `DIRECT-OFFICIAL-METHOD`.
44. `Codex Sinaiticus exact 1 Pet/Jude folio` — `ACCESS-PENDING`; не используется как доказательство принятой строки.
45. `NA28/ECM physical printed page` — `ACCESS-PENDING`; остаётся нужна для полного witness apparatus, но больше не нужна для определения primary line.

---

# G. Статья 6: Енох и Иуд. 14–15 — 4 узла

46. Nickelsburg, *1 Enoch 1*, с. 142–143, 148–149 — `DIRECT-FULL-FILE`.
47. Bauckham, *Jude, 2 Peter*, с. 93–96 — `DIRECT-FULL-FILE`.
48. Green, *Jude and 2 Peter*, с. 101–105 — `DIRECT-FULL-FILE`.
49. Timothy A. Lee, “Jude’s Use of a Kaige Edition of Enochic Scripture,” 206–224 — `ARTICLE-RANGE-AND-ARGUMENT-CONTROLLED`; модель остаётся гипотезой.

---

# H. Статьи 7–9 и закрытие локаторов — 7 узлов

50. Bauckham, с. 245–250 — `DIRECT-FULL-FILE`; 2 Пет. 2:4–5, Тартар, `σειραῖς / σιροῖς`.
51. Davids, *The Letters of 2 Peter and Jude*, с. 48–55, 224–226 — `DIRECT-FULL-FILE`.
52. Chad T. Pierce, [Durham thesis](https://etheses.dur.ac.uk/13/) — `DIRECT-OFFICIAL-FULL-PDF`; релевантные с. 183–237.
53. Wayne Grudem, [official article page](https://www.waynegrudem.com/christ-preaching-through-noah-1-peter-319-20-in-the-light-of-dominant-themes-in-jewish-literature) — `OFFICIAL-PAGE`; PDF за Cloudflare, длинные цитаты не используются.
54. David G. Horrell, [“Who Are ‘the Dead’?”](https://www.cambridge.org/core/journals/new-testament-studies/article/abs/who-are-the-dead-and-when-was-the-gospel-preached-to-them-the-interpretation-of-1-pet-46/66D1EF6323D7CD9AEEA78CF9AF8309AF) — `PUBLISHER-METADATA-AND-ABSTRACT`; NTS 49 (2003): 70–89.
55. Matthew R. Crawford, [JTS 67.1 article](https://academic.oup.com/jts/article/67/1/23/2451894) — `PUBLISHER-METADATA-AND-ABSTRACT`; полный текст закрыт.
56. [The Master’s Seminary — Doctrinal Statement](https://tms.edu/doctrinal-statement/) — `DIRECT-OFFICIAL`; разделы о Святом Духе и Церкви.

---

## 2. Дополнительные источники, проверенные, но не повышающие вес вывода

В контрольный проход также вошли:

- [Horrell, *Becoming Christian*](https://www.bloomsbury.com/us/becoming-christian-9780567423825/);
- [Williams–Horrell, ICC 1 Peter vol. 2](https://www.bloomsbury.com/uk/1-peter-9780567710611/);
- [Davids, *The First Epistle of Peter*](https://www.eerdmans.com/9780802825162/the-first-epistle-of-peter/);
- [Davids, *The Letters of 2 Peter and Jude*](https://www.eerdmans.com/9780802837264/the-letters-of-2-peter-and-jude/);
- [SBL Fonts](https://www.sbl-site.org/resources/fonts/);
- [Vatican Reproductions and Rights Office](https://www.vaticanlibrary.va/en/reproductions-and-rights-office.html).

Они важны для библиографии, доступа, шрифтов и лицензирования, но не считаются новыми независимыми доказательствами экзегетического вывода.

---

## 3. Что этот прогон реально изменил

```text
ECM2 / NA28 PRIMARY LINE
→ CLOSED FOR FIVE KEY LOCI

FULL WITNESS APPARATUS
→ STILL ACCESS-PENDING

4Q204 MODERN ARCHIVE OBJECT
→ IDENTIFIED

4Q204 IMAGE PUBLICATION RIGHT
→ PERMISSION REQUIRED

P72 COVERAGE
→ VERIFIED

P72 IMAGE PUBLICATION RIGHT
→ PERMISSION REQUIRED

SINAITICUS EXACT FOLIO
→ STILL PENDING, NO LONGER A P0 BLOCKER
```

---

## 4. Итог контроля количества

```text
NUMBERED CORE CONTROL NODES
→ 56

ADDITIONAL ACCESS / RIGHTS / PUBLISHER NODES
→ 6

TOTAL REVIEWED IN THIS PASS
→ 62
```

Число 62 описывает проверенные страницы, издания и access-points, а не 62 полностью прочитанные независимые монографии.
