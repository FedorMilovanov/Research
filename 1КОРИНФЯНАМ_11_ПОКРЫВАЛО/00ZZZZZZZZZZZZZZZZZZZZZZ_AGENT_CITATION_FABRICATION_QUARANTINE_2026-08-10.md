# 1 Коринфянам 11:2–16 — quarantine-аудит выдуманных / искажённых агентских ссылок

**Дата:** 2026-08-10  
**Статус:** `SOURCE-HYGIENE / FAIL-CLOSED / RESEARCH-ONLY / PUBLICATION-HOLD`  
**Основание:** отдельный проход по загруженному агентскому дампу после `SECOND_AGENT_DUMP_DEEP_VERIFICATION_2026-08-10`.

## Проверяемый вопрос

В агентском дампе появился кластер очень конкретных, академически правдоподобно оформленных ссылок: свежие статьи, главы, папирус и патристическая цитата. Нужно установить, существуют ли именно эти публикации/локаторы и действительно ли они поддерживают приписанные им тезисы.

Этот аудит **не переоценивает сам текст 1 Кор 11:2–16**. Его задача — не позволить ложной библиографии попасть в текущую authority через повторное цитирование другими агентами.

---

## Метод и evidence-policy

Применяется `AGENT_RULES.md` и `data/repository-evidence-policy-v2.json`:

- официальный каталог издателя / журнала / коллекции используется как первичный институциональный контроль библиографического факта;
- точная цитата из древнего автора проверяется по доступному полному тексту перевода, а не по пересказу AI;
- отсутствие заявленного материала в полном официальном TOC/issue list при одновременном наличии конфликтующей реальной записи является основанием для `REJECT` конкретной библиографической атрибуции;
- если реальная книга существует, но заявленная глава/применение к 1 Кор 11 не подтверждены, сама книга не отвергается — в quarantine уходит **конкретный тезис/локатор**;
- ни один веб-пересказ не повышает спорный экзегетический тезис до quote-safe уровня.

---

# 1. P.Oxy. 84.5575 — `REJECT / FABRICATED PAPYROLOGICAL PARALLEL`

### Агентский тезис

Дамп утверждал, что `P.Oxy. 84.5575` — частное письмо II–III вв., где женщина пишет о покрытии головы `κατὰ τὸ ῥωμαϊκὸν ἔθος` и об `ἐξουσία` в доме; это было объявлено «первой прямой папирологической параллелью» к 1 Кор 11:10.

### Прямой контроль

Официальный Oxford / Oxyrhynchus catalogue фиксирует:

- **Vol. LXXXIV = London 2019**, ed. A. Benaissa, N. Gonis, W. B. Henry, M. Langellotti;
- **Vol. LXXXVII = London 2023**, ed. P. J. Parsons and N. Gonis;
- **P.Oxy. 5575 находится в vol. LXXXVII**, а не LXXXIV;
- 5575 — ранняя копия **изречений Иисуса**, частично параллельных Матфею, Луке и Евангелию Фомы.

Официальный маршрут: https://oxyrhynchus.web.ox.ac.uk/node/3484511

### Вердикт

```text
POXY_84_5575_PRIVATE_LETTER = FALSE
POXY_84_5575_ROMAN_HEAD_COVERING = FALSE
POXY_84_5575_EXOUSIA_PARALLEL = FALSE
POXY_5575_ACTUAL = VOL_87_2023_SAYINGS_OF_JESUS
PAPYROLOGICAL_SUPPORT_FROM_5575_FOR_1COR11 = NONE
```

Это не «ошибка в годе»: номер тома, жанр, содержание, греческие формулы и вывод были приписаны не тому папирусу.

`evidenceClass`: `A2` для официального каталога коллекции.  
`publicationState`: ложный агентский тезис `BLOCKED`.

---

# 2. J. R. Daniel Kirk, “Women’s Prophetic Authority in 1 Corinthians 11,” JBL 142.3 (2023): 509–530 — `REJECT`

### Агентский тезис

Дамп дал точную ссылку на статью Kirk в `Journal of Biblical Literature 142.3 (2023): 509–530` и приписал ей активное прочтение `ἐξουσία` как женской пророческой власти.

### Прямой контроль

Официальная карточка SBL Press для **JBL 142.3** перечисляет содержание выпуска. Среди авторов: Eric J. Harvey, Anthony Ellis, Mahri Leonard-Fleckman, Cynthia R. Chapman, Rebecca W. Poe Hays, Elisa Uusimäki, James M. Neumann, Matthew J. Klem, Margaret Aymer. **Kirk в содержании отсутствует.**

Маршрут: https://cart.sbl-site.org/books/061423J

Дополнительный пагинационный контроль: реальная статья Matthew J. Klem, “John 21:15–19 as a Prophetic Succession: A Reading in Light of 2 Kings 2:1–18,” опубликована в **JBL 142.3 (2023): 513–531**, DOI `10.15699/jbl.1423.2023.8`.

### Вердикт

```text
KIRK_WOMENS_PROPHETIC_AUTHORITY_JBL_142_3 = FALSE_CITATION
KIRK_2023_509_530_SUPPORT = NONE
ACTIVE_EXOUSIA_ARGUMENT_FROM_THIS_ITEM = BLOCKED
```

Даже диапазон страниц конфликтует с реальной публикацией выпуска.

`evidenceClass`: `A2` (официальный SBL issue catalogue) + `B1` пагинационный cross-check.  
`publicationState`: `BLOCKED`.

---

# 3. Kathy Ehrensperger — Journal of Early Christian History 13.1 (2023): 1–22 — `REJECT`

### Агентский тезис

Заявлена статья: Kathy Ehrensperger, “Because of the Angels: Gender, Ritual and Authority in 1 Corinthians 11,” `Journal of Early Christian History 13.1 (2023): 1–22`.

### Прямой контроль

Полный официальный TOC Taylor & Francis для **Journal of Early Christian History 13.1 (2023)** содержит:

- Sviatoslav Dmitriev, pp. 1–23;
- David L. Eastman, pp. 24–39;
- Ehab Elias, pp. 40–61;
- Christopher M. Hansen, pp. 62–80;
- book review pp. 81–85.

Ehrensperger в выпуске отсутствует; заявленные страницы 1–22 заняты другой статьёй.

Маршрут: https://www.tandfonline.com/toc/rech20/13/1

### Вердикт

```text
EHRENSPERGER_JECH_13_1_2023_1_22 = FALSE_CITATION
EHRENSPERGER_BECAUSE_OF_ANGELS_2023 = NOT_IN_CLAIMED_ISSUE
```

`evidenceClass`: `A2`.  
`publicationState`: `BLOCKED`.

---

# 4. Ehrensperger chapter in *Ritual, Emotion, and Materiality...* — `REJECT AS CITED`

### Агентский тезис

Заявлена глава: “Performing the Gospel, Performing Gender: Ritual, Space and Authority in 1 Corinthians 11–14,” pp.145–168, в книге *Ritual, Emotion, and Materiality in the Early Christian World*, якобы ed. Soham Al-Suadi and Richard E. DeMaris, Routledge 2021.

### Прямой контроль

Официальная Routledge-карточка книги фиксирует:

- editors: **Soham Al-Suadi, Richard S. Ascough, Richard E. DeMaris**;
- copyright **2022**;
- полный TOC из 12 глав;
- **нет главы Ehrensperger** и нет заявленного заголовка по 1 Кор 11–14.

Маршрут: https://www.routledge.com/Ritual-Emotion-and-Materiality-in-the-Early-Christian-World/Al-Suadi-Ascough-DeMaris/p/book/9781032054834

### Вердикт

```text
EHRENSPERGER_PERFORMING_GOSPEL_CHAPTER = FALSE_CITATION
RITUAL_EMOTION_MATERIALITY_EDITORS_AGENT = WRONG_INCOMPLETE
RITUAL_EMOTION_MATERIALITY_YEAR_AGENT = WRONG
```

Сама книга реальна и может быть использована как **общий ritual/materiality background**, но не как источник заявленного тезиса Ehrensperger о 1 Кор 11.

---

# 5. Soham Al-Suadi, “Because of the Angels: Embodied Cognition...” in *Early Christian Ritual Life* — `REJECT`

### Агентский тезис

Заявлена глава Al-Suadi о 1 Кор 11 в *Early Christian Ritual Life*, Routledge 2022, ed. Richard E. DeMaris, Jason T. Lamoreaux, Mark D. Nanos, pp.78–96.

### Прямой контроль

Официальный Routledge catalogue фиксирует другую книгу:

- *Early Christian Ritual Life*;
- authors/editors represented as **Richard DeMaris, Jason Lamoreaux, Steven Muir**;
- copyright **2018**;
- полный TOC: девять глав; **Al-Suadi среди авторов нет**, заявленной главы о 1 Кор 11 нет.

Маршрут: https://www.routledge.com/Early-Christian-Ritual-Life/DeMaris-Lamoreaux-Muir/p/book/9781138653061

### Вердикт

```text
AL_SUADI_EMBODIED_COGNITION_1COR11_CHAPTER = FALSE_CITATION
EARLY_CHRISTIAN_RITUAL_LIFE_2022 = FALSE_METADATA
MARK_D_NANOS_AS_EDITOR_OF_THIS_BOOK = FALSE
```

`publicationState`: `BLOCKED`.

---

# 6. John Chrysostom, Homily 26: “ангелы = священники и епископы” — `REJECT / FALSE QUOTE`

### Агентский тезис

Дамп дал как **точную цитату** из `In 1 Cor. hom. 26` фразу по смыслу: «ангелы здесь — священники и епископы, которые должны видеть порядок в церкви», а затем утверждал, что Златоуст прямо отождествляет `ἄγγελοι` с духовенством.

### Прямой контроль текста

Полный NPNF translation Homily 26 действительно охватывает 1 Cor 11:2–16. На v10 Chrysostom пишет, что даже если женщина пренебрегает мужем, она должна **“reverence the angels”**, затем объясняет покрытие как знак подчинения/власти. Он **не** отождествляет здесь ангелов со священниками или епископами.

Маршруты:

- New Advent full Homily 26: https://www.newadvent.org/fathers/220126.htm
- NPNF/CCEL: https://ccel.org/ccel/schaff/npnf112/npnf112.iv.xxvii.html

### Вердикт

```text
CHRYSOSTOM_HOM26_ANGELS_PRIESTS_BISHOPS_QUOTE = FABRICATED_QUOTE
CHRYSOSTOM_HOM26_ANGELS_HUMAN_CLERGY = FALSE_ATTRIBUTION
CHRYSOSTOM_HOM26_ANGELS_CELESTIAL_REVERENCE = DIRECT_TEXT_COMPATIBLE
```

Это особенно важный stop-rule: **никогда не переносить “точные” патристические цитаты из агентских ответов без прямого текста.**

`evidenceClass`: `B1` для стандартного NPNF перевода как текстового контроля; критическое греческое издание при необходимости остаётся отдельным acquisition target.  
`publicationState`: fabricated quote `BLOCKED`.

---

# 7. April D. DeConick, JBL 140.3 (2021): 599–616 — `REJECT`

### Агентский тезис

Заявлена статья: April D. DeConick, “Why Are the Angels in 1 Cor 11:10 ‘Because of the Women’? A Response to Dale Martin,” `JBL 140.3 (2021): 599–616`.

### Прямой контроль

Официальный Scholarly Publishing Collective / SBL показывает, что в **JBL 140.3 (2021)** статья M. David Litwa, “Equal to Angels: The Early Reception History of the Lukan ἰσάγγελοι (Luke 20:36),” занимает **pp.601–622**, DOI `10.15699/jbl.1403.2021.8`.

Маршрут: https://scholarlypublishingcollective.org/sblpress/jbl/article/140/3/601/287332/

Заявленный диапазон DeConick 599–616 физически перекрывает реальную статью Litwa; точный заявленный заголовок в официальном поиске выпуска не подтверждается.

### Вердикт

```text
DECONICK_JBL_140_3_2021_599_616 = FALSE_CITATION
DECONICK_RESPONSE_TO_DALE_MARTIN_AS_CITED = BLOCKED
```

---

# 8. DeConick, *The Gnostic New Age*, “The Great Mystery of Marriage...” pp.189–212 — `REJECT AS CHAPTER / TOPIC HOLD`

### Агентский тезис

Заявлена отдельная глава “The Great Mystery of Marriage: Sex and the Angels in 1 Cor 11,” pp.189–212.

### Прямой контроль

Официальный Columbia University Press TOC *The Gnostic New Age* содержит 11 глав, среди них **“Paul and Gnostic Dogma”**, но **не** содержит главы с заявленным названием “The Great Mystery of Marriage...”

Маршрут: https://cup.columbia.edu/book/the-gnostic-new-age/9780231542043/

### Вердикт

```text
DECONICK_GNOSTIC_NEW_AGE_GREAT_MYSTERY_CHAPTER = FALSE_AS_STANDALONE_CHAPTER
DECONICK_BOOK_EXISTS = TRUE
DECONICK_BOOK_DISCUSSION_OF_1COR11_EXACT = LOCATOR_HOLD
DECONICK_ANGEL_SEXUALITY_ARGUMENT_ATTRIBUTION = EVIDENCE_HOLD
```

Важно: отсутствие заявленного названия в TOC **не доказывает**, что внутри главы “Paul and Gnostic Dogma” нет краткого обсуждения 1 Кор 11. Поэтому блокируется конкретная выдуманная библиография и её сильные выводы; сама книга остаётся потенциальным direct-read target.

---

# 9. Yung Suk Kim, *1 Corinthians: An Asian and Liberationist Reading* (Cascade, 2023) — `NOT LOCATED / QUARANTINE`

### Агентский тезис

Дамп заявил книгу 2023 г. и специальную главу “Head, Veil, and Power: Re-reading 1 Corinthians 11:2–16 from the Margins”, включая очень конкретную связь с корейскими comfort women.

### Контроль

Официальная author page Wipf & Stock для Yung Suk Kim перечисляет его многочисленные книги, включая реальные *Christ’s Body in Corinth*, *Toward Decentering the New Testament*, *Reimagining the Body of Christ in Paul’s Letters*, а также реальный edited volume *Paul’s Gospel, Empire, Race, and Ethnicity* (2023). Точное заявленное название *1 Corinthians: An Asian and Liberationist Reading* и глава “Head, Veil, and Power...” в publisher search не обнаружены.

Маршруты:

- https://wipfandstock.com/author/yung-suk-kim/
- https://wipfandstock.com/9781666731873/pauls-gospel-empire-race-and-ethnicity/

### Вердикт

```text
YUNG_SUK_KIM_1CORINTHIANS_ASIAN_LIBERATIONIST_2023 = NOT_LOCATED
YUNG_SUK_KIM_HEAD_VEIL_POWER_CHAPTER = NOT_LOCATED
COMFORT_WOMEN_1COR11_ATTRIBUTION_TO_THIS_ITEM = BLOCKED
```

Статус здесь намеренно не `FALSE` на уровне всей возможной мировой библиографии: без полного авторского CV нельзя доказывать абсолютное несуществование. Но **для Research ссылка непригодна и остаётся в quarantine, пока не появится издательская/библиотечная запись или сам текст.**

---

# 10. Christina Petterson — реальная книга, но агент исказил название и приписал неподтверждённую 1 Cor 11-функцию

### Агентский тезис

Дамп назвал книгу *From Tomb to Text: The Death of Jesus in the Book of John* (2018), заявил «особенно главу, где она использует 1 Кор 11 как параллель», плюс отдельную статью “The Body of Christ and the Body of Paul: Pauline Sexual Politics and the Corinthian Community” (2020–2021).

### Прямой контроль

Официальная Bloomsbury / T&T Clark карточка фиксирует реальное название:

> Christina Petterson, *From Tomb to Text: The Body of Jesus in the Book of John*.

TOC: *The World and its Flesh; Docetism, Past and Present; Embodying the Flesh; Pleromatic Time; Jesus and his Corpse; The Mediator* — **нет главы по 1 Кор 11**.

Маршрут: https://www.bloomsbury.com/us/from-tomb-to-text-9780567682550/

Точный заявленный заголовок второй статьи в целевом поиске не локализован.

### Вердикт

```text
PETTERSON_BOOK = REAL
PETTERSON_BOOK_SUBTITLE_AGENT = WRONG
PETTERSON_DEDICATED_1COR11_CHAPTER = FALSE_BY_TOC
PETTERSON_1COR11_PARALLEL_EXACT = LOCATOR_HOLD
PETTERSON_BODY_OF_CHRIST_BODY_OF_PAUL_ARTICLE = NOT_LOCATED
PETTERSON_STRONG_POSTCOLONIAL_1COR11_ATTRIBUTION = BLOCKED
```

Сама монография — Johannine study, а не прямой specialist source по 1 Cor 11.

---

# 11. Jeremy Punt / *Postcolonial Perspectives in African Biblical Interpretations* — `REAL SOURCE, FALSE AGENT CITATION`

### Агентский тезис

Дамп ссылался на:

> Jeremy Punt, “Postcolonial Feminist Interpretation of the New Testament: A South African Perspective,” in *Postcolonial Perspectives in African Biblical Hermeneutics*, SBL Press 2022,

и затем приписывал этой работе специальное чтение 1 Кор 11:2–16 через апартеид и женские символы respectability.

### Контроль

Реальный SBL volume существует под названием:

> *Postcolonial Perspectives in African Biblical Interpretations*, ed. Musa W. Dube, Andrew M. Mbuvi, Dora R. Mbuwayesango.

Первоначальная публикация — **2012** (SBL Press; GPBS 13; поздние электронные карточки могут показывать более новую дату digital edition). Полный TOC показывает реальную главу Jeremy Punt:

> **“Pauline Bodies and South African Bodies: Body, Power, and Biblical Hermeneutics”**.

Официальный/институциональный контроль:

- JSTOR book record: https://www.jstor.org/stable/jj.11589034
- SBL/BiblioVault metadata: https://www.bibliovault.org/BV.book.epl?ISBN=9781589837867

### Вердикт

```text
PUNT_POSTCOLONIAL_FEMINIST_NT_CHAPTER_AS_CITED = FALSE_CITATION
POSTCOLONIAL_PERSPECTIVES_AFRICAN_BIBLICAL_HERMENEUTICS_TITLE = WRONG
PUNT_REAL_CHAPTER = PAULINE_BODIES_AND_SOUTH_AFRICAN_BODIES
PUNT_REAL_CHAPTER_DIRECT_1COR11_ARGUMENT = LOCATOR_HOLD
PUNT_SPECIFIC_1COR11_APARTHEID_RESPECTABILITY_MODEL = BLOCKED_UNTIL_DIRECT_TEXT
```

Реальная глава Punt может быть полезна для более широкого postcolonial/body hermeneutics background, но нельзя превращать её в specialist exegesis 1 Cor 11 без direct read.

---

# 12. Реально полезная новая библиография после очистки

Этот проход показал, что ценность сейчас не в наращивании количества «свежих» ссылок, а в **очистке poisoned bibliography**. Тем не менее есть несколько безопасных направлений:

## 12.1 Recent direct 1 Cor 11 work already current and verified

- Callie Callon, “Authority Over Whose Head? Did Paul Instruct Wives or All Women to Cover Their Heads (1 Corinthians 11:2–16)?,” *Harvard Theological Review* 117.4 (2024): 699–719, DOI `10.1017/S0017816024000300` — direct, open access, specifically on wives/all women, slavery and hair-status constraints.
- Aldar Nõmmik, *Robes, Romans, and Rituals in First Corinthians* — current project already has institutional model control; historical reconstruction remains calibrated rather than promoted to fact.
- David E. Garland, *1 Corinthians*, 2nd ed. (2025) — current-edition direct-read HOLD remains more valuable than invented 2023–2025 articles.

No duplicate claim-grade changes are made here.

## 12.2 Real 2025/2026 ritual/gender volume — context only

Routledge has a genuine recent volume:

> Richard E. DeMaris, Soham Al-Suadi, Richard S. Ascough, eds., *Ritual, Gender, and the Body in the Early Christian World* (listed Nov. 2025; copyright 2026).

Its official TOC includes chapters on female agency in ancient Greek religion, ritual masculinity, visual discourse, women’s ritual labor in Acts 16, etc. **It does not contain a dedicated 1 Cor 11 chapter.**

Route: https://www.routledge.com/Ritual-Gender-and-the-Body-in-the-Early-Christian-World/DeMaris-Al-Suadi-Ascough/p/book/9781032915982

Use only as:

```text
RITUAL_GENDER_BODY_2025_2026 = B1_CONTEXT_ONLY
DIRECT_1COR11_SUPPORT = NO
```

## 12.3 Better next acquisitions

The highest-yield next work remains direct text rather than another discovery round:

1. Garland 2025 pp.468–493 + notes.
2. Thiselton pp.800–847 + notes.
3. Fee Revised 2014 relevant section + addendum.
4. Ciampa/Rosner pp.503–540.
5. Nõmmik full dissertation bytes / exact v10-angels passages.
6. DeConick *The Gnostic New Age*, ch.4 direct read **only if** 1 Cor 11 appears in the text; otherwise remove it from the 1 Cor 11 bibliography.
7. Punt real chapter direct read before any 1 Cor 11 attribution.

---

# 13. Machine-safe quarantine summary

```text
POXY_84_5575_1COR11_PARALLEL = REJECT
KIRK_JBL_142_3_2023_509_530 = REJECT
EHRENSPERGER_JECH_13_1_2023 = REJECT
EHRENSPERGER_RITUAL_EMOTION_CHAPTER = REJECT
AL_SUADI_EARLY_CHRISTIAN_RITUAL_LIFE_1COR11_CHAPTER = REJECT
CHRYSOSTOM_ANGELS_PRIESTS_BISHOPS_QUOTE = REJECT
DECONICK_JBL_140_3_2021_599_616 = REJECT
DECONICK_GNOSTIC_NEW_AGE_STANDALONE_CHAPTER = REJECT_AS_CITED
DECONICK_EXACT_1COR11_USE = HOLD
YUNG_SUK_KIM_2023_1COR_BOOK = QUARANTINE_NOT_LOCATED
PETTERSON_BOOK = REAL_BUT_MIS-CITED
PETTERSON_1COR11_SPECIALIST_USE = HOLD
PUNT_VOLUME_CHAPTER = REAL_BUT_AGENT_CITATION_FALSE
PUNT_1COR11_SPECIFIC_MODEL = HOLD
CORE_CLAIM_GRADE_REVERSALS = 0
```

---

# 14. Publication boundary

```text
AGENT_DUMP = DISCOVERY_ONLY
FALSE_OR_NOT_LOCATED_CITATION = NEVER_PROPAGATE
DIRECT_QUOTE_FROM_AGENT = NEVER_QUOTE_SAFE_WITHOUT_DIRECT_TEXT
BIBLIOGRAPHIC_PRECISION = REQUIRED_BEFORE_CLAIM_PROMOTION
PRODUCT_WRITE = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
```

This quarantine layer supersedes any conflicting positive labels (“verified”, “gold”, “fully verified”) attached to the specific items above in raw agent dumps. It does **not** supersede the current core exegetical claim registry.
