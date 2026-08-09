# 1 Коринфянам 11:2–16 — 51-link external verification ledger

**Дата проверки:** 2026-08-09  
**Статус:** `EXTERNAL-VERIFICATION / FAIL-CLOSED / RESEARCH-ONLY / PUBLICATION-HOLD`  
**Назначение:** независимая перепроверка параллельных agent-corpus `arena/019fe62b-research@883593bd3aedb4fbb67d1fb159ab363a847596dd` и `arena/019fe62d-research@1ae05904aad93bae59e7b655791c9dea5530758e` перед включением синтеза в `main`.

## 1. Правило счёта

Это **51 отдельная проверочная запись по URL**, а не заявление о «51 полностью прочитанной книге». Статусы различаются:

- `DIRECT_TEXT_VERIFIED` — на странице непосредственно проверен относящийся к тезису текст;
- `PRIMARY_ARCHIVE_VERIFIED` — проверен институциональный архив/объект;
- `SCHOLARLY_ARGUMENT_VERIFIED` — проверены статья/abstract/metadata и заявленный исследовательский аргумент;
- `BIBLIOGRAPHIC_VERIFIED` — подтверждены автор, издание, серия, дата, объём; это **не** page-level verification конкретного тезиса;
- `ACCESS_RETRY` — ссылка/объект идентифицированы, но текущий web-fetch вернул ошибку; такая запись не повышает confidence claim.

## 2. Реестр 51 проверки

| # | Источник | URL | Что проверялось | Статус / вывод |
|---:|---|---|---|---|
| 1 | Deutsche Bibelgesellschaft, **GNT6** | https://shop.die-bibel.de/Greek-New-Testament-GNT6.-Standardausgabe/5310 | Текущая UBS Greek NT; какие ECM-изменения вошли; связь с NA29 | `DIRECT_TEXT_VERIFIED`: GNT6 уже издан; изменения ECM указаны для Acts/Mark/Revelation; текст заявлен идентичным NA29 |
| 2 | Deutsche Bibelgesellschaft, **NA29** | https://shop.die-bibel.de/Novum-Testamentum-Graece-NA29./5320 | Является ли NA29 уже опубликованным изданием | `DIRECT_TEXT_VERIFIED`: preorder; дата выхода 2027-02-28; на 2026-08-09 текущий опубликованный Nestle-Aland = NA28 |
| 3 | INTF, Editio Critica Maior overview | https://www.uni-muenster.de/INTF/forschung/ecm/index.html | Статус ECM и граница применимости | `PRIMARY_ARCHIVE_VERIFIED`: нельзя писать, что ECM Павловых посланий завершена; Pauline corpus остаётся не опубликованной завершённой ECM-линейкой |
| 4 | INTF Databases | https://www.uni-muenster.de/INTF/en/datenbanken/index.html | Институциональные manuscript/database routes | `PRIMARY_ARCHIVE_VERIFIED` |
| 5 | INTF ECM Revelation | https://www.uni-muenster.de/INTF/en/forschung/ecm_apokalypse.html | Подтверждение одной из реально опубликованных новых ECM-линий | `PRIMARY_ARCHIVE_VERIFIED` |
| 6 | Codex Sinaiticus, 1 Corinthians | https://codexsinaiticus.org/en/manuscript.aspx?book=38&chapter=10&lid=en&side=r&verse=17&zoomSlider=0 | Наличие перикопы у раннего крупного свидетеля, в т.ч. 11:10 | `PRIMARY_ARCHIVE_VERIFIED`; не использовать это как замену полному apparatus census |
| 7 | Tyndale House, 1 Cor 11:16 spelling/witness discussion | https://tyndalehouse.com/2018/11/15/removing-a-venerable-absurdity-of-spelling-luke-22-24-and-1-corinthians-11-16/ | Свидетельская база, включая P46/Sinaiticus/Claromontanus/Ephraemi | `SCHOLARLY_ARGUMENT_VERIFIED`; точный folio P46 из agent-ledger остаётся отдельным locator task |
| 8 | Plutarch, *Roman Questions* 1–24 | https://penelope.uchicago.edu/Thayer/e/roman/texts/plutarch/moralia/roman_questions%2A/a.html | Римское мужское `capite velato`, различие публичных норм мужчин/женщин | `DIRECT_TEXT_VERIFIED`: римская практика реальна; её применение к конкретным коринфским мужчинам = reconstruction, не direct fact |
| 9 | Philo, *Special Laws* III | https://www.earlyjewishwritings.com/text/philo/book29.html | Снятие женского head-dress / bare head / shame-modesty background | `DIRECT_TEXT_VERIFIED` |
| 10 | Mishnah Ketubot 7:6 | https://www.sefaria.org/Mishnah_Ketubot.7.6?with=Jerusalem+Talmud+Sotah | Позднейшая еврейская норма uncovered hair | `DIRECT_TEXT_VERIFIED`; использовать как reception/trajectory, не как прямой снимок Коринфа 50-х гг. |
| 11 | Bavli Ketubot 72a | https://www.sefaria.org/Ketubot.72a | Раббинское обсуждение uncovered head | `DIRECT_TEXT_VERIFIED`; хронологическая дистанция обязательна |
| 12 | Bavli Berakhot 24a | https://www.sefaria.org/Berakhot.24a.15-17?with=Halakhah | Волосы и позднейшая modesty/erva tradition | `DIRECT_TEXT_VERIFIED`; не превращать в доказательство апостольной ситуации |
| 13 | Israel Antiquities Authority, 1QSa | https://www.deadseascrolls.org.il/explore-the-archive/manuscript/1Q28a-1 | Реальный manuscript object `Rule of the Congregation` | `PRIMARY_ARCHIVE_VERIFIED` |
| 14 | Israel Museum, War Scroll | https://dss.collections.imj.org.il/war | Institutional object route для 1QM | `ACCESS_RETRY`: текущий fetch 502; claim не закрывать этим URL одним |
| 15 | University of Haifa, new annotated edition of 1QSa | https://cris.haifa.ac.il/en/publications/the-rule-of-the-congregation-from-cave-1-of-qumran-a-new-annotate/ | Современная критическая работа над 1QSa и DOI/metadata | `SCHOLARLY_ARGUMENT_VERIFIED` |
| 16 | Joseph A. Fitzmyer, Qumran angelology & 1 Cor 11:10 | https://www.cambridge.org/core/journals/new-testament-studies/article/abs/feature-of-qumran-angelology-and-the-angels-of-i-cor-xi-10/59CE5686A3600CB7F51184CD960286F1 | Кумранский фон для holy-angels reading | `SCHOLARLY_ARGUMENT_VERIFIED`: усиливает holy/liturgical-angels model, но Павел не идентифицирует ангелов прямо |
| 17 | John Chrysostom, Homily 26 on 1 Corinthians | https://www.newadvent.org/fathers/220126.htm | Ранняя рецепция veil/hair, women praying/prophesying, authority, mutuality | `DIRECT_TEXT_VERIFIED` |
| 18 | Tertullian, *On Prayer* | https://www.newadvent.org/fathers/0322.htm | Ранняя христианская практика и `because of angels` | `DIRECT_TEXT_VERIFIED` |
| 19 | Tertullian, *On the Veiling of Virgins* | https://www.newadvent.org/fathers/0403.htm | Watchers/fallen-angels interpretation | `DIRECT_TEXT_VERIFIED`: древняя линия, но не доказательство того, что Павел сам имел в виду Watchers |
| 20 | Clement of Alexandria, *Paedagogus* III | https://www.newadvent.org/fathers/02093.htm | Modesty/hair/head themes | `DIRECT_TEXT_VERIFIED`; не выдавать за verse-by-verse commentary на 1 Cor 11 |
| 21 | Joseph A. Fitzmyer, “Another Look at Kephalē” | https://www.cambridge.org/core/journals/new-testament-studies/article/abs/another-look-at-keah-in-1-corinthians-113/5497286E96F87DD654B9720F2B2AC753 | Лексический спор о `κεφαλή` | `SCHOLARLY_ARGUMENT_VERIFIED`: authority/superiority evidence существует |
| 22 | Wayne Grudem, survey of 2,336 examples | https://www.galaxie.com/article/trinj06-1-02 | Аргумент за authority-over и против source-only | `SCHOLARLY_ARGUMENT_VERIFIED`; число 2,336 — число рассмотренных occurrences, не 2,336 независимых примеров authority |
| 23 | Richard S. Cervin, rebuttal | https://www.galaxie.com/article/trinj10-1-07?highlight=repentance | Контраргумент к методике/примерному корпусу Grudem | `SCHOLARLY_ARGUMENT_VERIFIED`: спор реален и не закрывается слоганом «source refuted» |
| 24 | Wayne Grudem, response to recent studies | https://www.galaxie.com/article/trinj11-1-02 | Ответ Cervin/Payne/Kroeger и др. | `SCHOLARLY_ARGUMENT_VERIFIED`; подтверждает наличие продолжающегося scholarly dispute |
| 25 | M. D. Hooker, “Authority on her Head” | https://www.cambridge.org/core/journals/new-testament-studies/article/abs/authority-on-her-head-an-examination-of-i-cor-xi-10/947E8A98C64ACEA00D2BD815F0F8BDE5 | `ἐξουσίαν ἔχειν` в 11:10 | `SCHOLARLY_ARGUMENT_VERIFIED`: grammar requires taking seriously woman as subject who “has” authority/right |
| 26 | Julie Newberry, Paul’s allusive reasoning 11:7–12 | https://www.cambridge.org/core/journals/new-testament-studies/article/abs/pauls-allusive-reasoning-in-1-corinthians-11712/EDE6D54A62D2265EA2C22291B6F2BA39 | Creation/allusion, authority and mutuality | `SCHOLARLY_ARGUMENT_VERIFIED` |
| 27 | Jill Marshall, Paul/Plutarch/gender dynamics of prophecy | https://www.cambridge.org/core/journals/new-testament-studies/article/abs/paul-plutarch-and-the-gender-dynamics-of-prophecy/010C5933799D0757AAD949AB8497E3AF | Gender/prophecy contextual comparison | `SCHOLARLY_ARGUMENT_VERIFIED`; alternative historical framing retained |
| 28 | Preston T. Massey, meaning of `κατακαλύπτω` / `κατὰ κεφαλῆς ἔχων` | https://www.cambridge.org/core/journals/new-testament-studies/article/abs/meaning-of-and-in-1-corinthians-11216/3B94F4462B2AC39852FE16FBECD46E38 | Textile-covering philological case | `SCHOLARLY_ARGUMENT_VERIFIED`: strong support for material covering; not sufficient to mark hair-model impossible |
| 29 | Philip B. Payne, “Wild Hair and Gender Equality” | https://www.galaxie.com/article/pp20-3-03 | Hair/hairstyle alternative | `SCHOLARLY_ARGUMENT_VERIFIED`: serious alternative exists; therefore old `GRADE X` rejection is superseded |
| 30 | Richard Oster, “When Men Wore Veils to Worship” | https://www.cambridge.org/core/journals/new-testament-studies/article/abs/when-men-wore-veils-to-worship-the-historical-context-of-1-corinthians-114/BF33873F095E46516A3A43604F14E32E | Roman male veil/cult reconstruction for 11:4 | `SCHOLARLY_ARGUMENT_VERIFIED`: strong background reconstruction; not direct proof of every Corinthian male practice |
| 31 | David W. J. Gill, Roman portraiture | https://www.tyndalebulletin.org/article/30525-the-importance-of-roman-portraiture-for-head-coverings-in-1-corinthians-11-2-16 | Portraiture/status evidence in Roman Corinth | `SCHOLARLY_ARGUMENT_VERIFIED` |
| 32 | Cynthia L. Thompson, hairstyles/head-coverings/portraits | https://www.journals.uchicago.edu/doi/10.2307/3210030 | Archaeological portrait evidence and competing reading | `SCHOLARLY_ARGUMENT_VERIFIED`: background is contested in interpretation |
| 33 | Troy W. Martin, ancient physiology/peribolaion | https://www.researchgate.net/publication/228853120_Paul%27s_Argument_from_Nature_for_the_Veil_in_1_Corinthians_11_13-15_A_Testicle_Instead_of_a_Head_Covering | `περιβόλαιον`/ancient physiology proposal | `SCHOLARLY_ARGUMENT_VERIFIED` at metadata/abstract level; niche contested hypothesis, not publication foundation |
| 34 | Mark Goodacre, “Does peribolaion mean ‘testicle’?” | https://scholars.duke.edu/publication/735885 | Direct critique of Martin | `SCHOLARLY_ARGUMENT_VERIFIED`; supports demoting testicle theory to low-confidence controversy |
| 35 | Callie Callon, “Authority Over Whose Head?” | https://www.cambridge.org/core/journals/harvard-theological-review/article/authority-over-whose-head-did-paul-instruct-wives-or-all-women-to-cover-their-heads-1-corinthians-11216/5D602D820F9CA0E6C55906BDF68466ED | Wives vs all women scope | `SCHOLARLY_ARGUMENT_VERIFIED`: article explicitly reflects lack of consensus; all-women/unmarried scope must remain OPEN |
| 36 | Curt Niccum, external evidence 1 Cor 14:34–35 | https://www.cambridge.org/core/journals/new-testament-studies/article/abs/voice-of-the-manuscripts-on-the-silence-of-women-the-external-evidence-for-1-cor-14345/5045B323E5B1F82A873ED1706AD64677 | Manuscript/transposition evidence in the 14:34–35 dispute | `SCHOLARLY_ARGUMENT_VERIFIED`: 11:5 cannot by itself close the 14:34–35 textual/exegetical question |
| 37 | Peter Gurry/related Vaticanus response, “Are There Distigme-Obelos Symbols in Vaticanus?” | https://www.cambridge.org/core/journals/new-testament-studies/article/abs/are-there-distigmeobelos-symbols-in-vaticanus/F2507362D31D370A04A20583EE0E1575 | Counter-analysis of Vaticanus marginal-sign claim | `SCHOLARLY_ARGUMENT_VERIFIED`: interpolation argument remains disputed |
| 38 | “1 Cor 14.34–5 without ‘in All the Churches of the Saints’: External Evidence” | https://www.cambridge.org/core/journals/new-testament-studies/article/abs/1-cor-14345-without-in-all-the-churches-of-the-saints-external-evidence/D4D25E5F5D48A16F34BD806E24BE89AB | Further external-evidence analysis | `SCHOLARLY_ARGUMENT_VERIFIED`; keep separate from 1 Cor 11 core claim-set |
| 39 | Anthony C. Thiselton, NIGTC | https://www.eerdmans.com/9780802824493/the-first-epistle-to-the-corinthians/ | Edition/series/page count and scope | `BIBLIOGRAPHIC_VERIFIED`; exact 11:2–16 page claims still require page-level custody |
| 40 | Gordon D. Fee, NICNT revised | https://www.eerdmans.com/9781467440417/the-first-epistle-to-the-corinthians-revised-edition/ | Correct edition, date, size | `BIBLIOGRAPHIC_VERIFIED`; do not promote inferred page claims without access |
| 41 | Roy E. Ciampa & Brian S. Rosner, PNTC | https://www.eerdmans.com/9781467426947/the-first-letter-to-the-corinthians/ | Correct edition/series/date | `BIBLIOGRAPHIC_VERIFIED` |
| 42 | David E. Garland, BECNT | https://tst.bakeracademic.com/p/1-Corinthians-David-E-Garland/40358 | Correct edition/series/date/page count | `BIBLIOGRAPHIC_VERIFIED` |
| 43 | Crossway, ESV Expository Commentary Romans–Galatians | https://www.crossway.org/books/esv-expository-commentary-premiumhc-3/ | Автор 1 Corinthians в ESVEC | `DIRECT_TEXT_VERIFIED`: 1 Corinthians = **Andrew David Naselli**, не Thomas Schreiner; agent attribution corrected |
| 44 | Francis Watson, “The Authority of the Voice” | https://www.cambridge.org/core/journals/new-testament-studies/article/abs/authority-of-the-voice-a-theological-reading-of-1-cor-11216/FABA54ECB3573BAE1579923E51D409C1 | Interdependence / veil as likely material sign | `SCHOLARLY_ARGUMENT_VERIFIED`: binary hierarchical-vs-egalitarian framing is too crude |
| 45 | Themelios, gospel as interpretive key to 1 Cor 11 | https://www.thegospelcoalition.org/themelios/article/the-gospel-as-interpretive-key-to-1-corinthians-11/ | Recent conservative synthesis; cites Schreiner and critiques overuse of background | `SCHOLARLY_ARGUMENT_VERIFIED` as secondary synthesis; not primary authority |
| 46 | Thomas Schreiner lecture, 1 Corinthians Part 4 | https://www.biblicaltraining.org/learn/institute/survey-acts-revelation-nt504/nt504-10-i-corinthians-part-4 | Conservative acknowledgement of cultural uncertainty | `DIRECT_TEXT_VERIFIED`: Schreiner explicitly says exact custom is uncertain; supports calibrated rather than absolute application claims |
| 47 | Crossway/Naselli, Paul’s letters date/context | https://www.crossway.org/articles/where-when-and-why-were-each-of-pauls-letters-written/ | Contemporary conservative Corinth/date contextual summary | `BIBLIOGRAPHIC/CONTEXT_VERIFIED`; secondary source only |
| 48 | ASCSA Ancient Corinth history timeline | https://www.ascsa.edu.gr/excavations/ancient-corinth/about-the-excavations-1/history-timeline | Institutional Corinth chronology | `ACCESS_RETRY`: current fetch returned 502; do not count as direct text evidence in this pass |
| 49 | ASCSA Ancient Corinth excavation overview | https://www.ascsa.edu.gr/excavations/ancient-corinth/about-the-excavations-1 | Institutional excavation context | `ACCESS_RETRY`: current fetch returned 502 |
| 50 | ASCSA Demeter/Kore publication route | https://www.ascsa.edu.gr/publications/book/?i=9780876611838 | Institutional publication object | `ACCESS_RETRY`: current fetch returned 502; no claim promotion |
| 51 | ASCSA Metis Demeter/Kore resource | https://metis.ascsa.edu.gr/resource/a73b288be43b32c110da3976f711d042?feedback=true&image_id=52f3a1aa5d659e03cb784c70dc5286b2&tab=overview&view=preview | Material-culture object route | `ACCESS_RETRY`: cache miss in current fetch; retain as acquisition route only |

## 3. Главные результаты этого прохода

1. **Текстологическая база исправлена:** на 2026-08-09 GNT6 уже опубликован; NA29 ещё нет (официальная дата 2027-02-28). Формула «NA29 — текущая опубликованная NA» запрещена.
2. **ECM Павловых посланий нельзя объявлять завершённой.** GNT6 указывает новые ECM-text changes из Acts/Mark/Revelation; этот факт не превращает 1 Corinthians в завершённый Pauline-ECM object.
3. **`κεφαλή` остаётся реальным scholarly dispute.** Conservative headship/authority reading имеет серьёзную поддержку; `source/origin` нельзя объявлять «опровергнутым».
4. **11:10:** `ἐξουσίαν ἔχειν` грамматически требует начать с того, что женщина является субъектом `ἔχειν`; перевод «знак чужой власти» — интерпретационный шаг, не лексическое значение `ἐξουσία`.
5. **Покрытие:** material covering получает сильную поддержку (Massey, patristic reception), но hair/hairstyle model — серьёзная конкурирующая модель, не `GRADE X`.
6. **Ангелы:** Qumran/early-Christian background делает holy/liturgical-angels reading ведущим `PROBABLE`; Watchers — древняя Tertullian line, но Павел не идентифицирует их прямо.
7. **Римский фон:** `capite velato` — реальная римская культовая практика; тезис «именно это делали мужчины коринфской церкви» остаётся исторической реконструкцией.
8. **Адресаты:** wives-vs-all-women остаётся открытым вопросом; современная HTR-дискуссия прямо фиксирует отсутствие консенсуса.
9. **11:5 vs 14:34–35:** факт женской молитвы/пророчества в 11:5 нельзя стирать, но им также нельзя одним ходом закрыть отдельный текстологический и экзегетический спор 14:34–35.
10. **Библиография:** ESV Expository Commentary по 1 Corinthians написан Andrew David Naselli; старое агентское приписывание этого комментария Schreiner считается исправленным.

## 4. Publication boundary

```text
51 URL VERIFICATION RECORDS != 51 FULL BOOK READS
BIBLIOGRAPHIC VERIFIED != PAGE-LEVEL CLAIM VERIFIED
PRIMARY BACKGROUND != DIRECT PROOF OF CORINTHIAN PRACTICE
PROBABLE != CERTAIN
RESEARCH MAIN MERGE != PRODUCT PUBLICATION
```

`PUBLICATION_HOLD` сохраняется. Этот реестр разрешает Research-синтез в `main`, но **не** перенос статей в Product.