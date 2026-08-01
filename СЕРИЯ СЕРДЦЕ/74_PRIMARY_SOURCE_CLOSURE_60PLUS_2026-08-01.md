# 74 — PRIMARY SOURCE CLOSURE: 85-SOURCE CONTROL RUN

**Дата:** 2026-08-01  
**Область:** `СЕРИЯ СЕРДЦЕ`, R1–R9, V84 evidence-boundaries и спорные именные формулировки.  
**Режим:** source closure, не накопление новых красивых цитат.  

## 1. Результат

- Уникальных источников в registry: **85**.
- Первичных/open/официальных/академических источников по машинному классу: **81**.
- Зафиксированных спорных claims: **18**.
- Разрешены для прямого использования при указанном locator/context: **9**.
- Окончательно переведены в `REMOVE`, `PARAPHRASE-ONLY` или `RECEPTION-ONLY`: **9**.

Ни один старый `HOLD` больше не читается как бесконечное обещание «когда-нибудь найти книгу». Каждая спорная позиция получила конечное разрешение: точный первичный текст, официальный replacement, ограниченный парафраз либо удаление.

Машиночитаемая authority:

- `74_SOURCE_CLOSURE_REGISTRY_2026-08-01.json`;
- `scripts/check_heart_source_closure.py`;
- `.github/workflows/heart-source-closure.yml`.

## 2. Метод без костылей

1. Для каждого claim отделён **текст автора** от поздней формулы, пересказа, заголовка редактора и цитатника.
2. Для книг различены: скан/полный текст, официальный publisher/ministry material, библиографическая карточка и вторичная подсказка.
3. `quote_safe=true` разрешён только claim со ссылкой на зарегистрированный trusted source.
4. OCR/searchable PDF не превращается автоматически в page-image verification.
5. Если точный афоризм не найден, он не «спасается» ссылкой на автора: он удаляется и заменяется доказанным первичным текстом.
6. Контроль CI требует минимум 60 уникальных источников и минимум 50 trusted records.

## 3. Закрытие спорных вопросов

| Claim | Итог | Прямое использование | Решение |
|---|---|---:|---|
| `CLM-WHITEFIELD-ANECDOTE` — Whitefield repeated born-again anecdote/stat | `REMOVE` | нет | No primary locus for the anecdote was found. Remove as documented history; use Whitefield's actual sermon On Regeneration. |
| `CLM-WHITEFIELD-STONY` — Whitefield stony-ground wording | `OFFICIAL-REPLACEMENT` | да | Replace the unlocated wording with Whitefield's primary sermon Directions How to Hear Sermons. |
| `CLM-SPURGEON-FREE-WILL` — Spurgeon free will carried many souls to hell | `PRIMARY-VERIFIED` | да | Verified in sermon No. 224, Samson Conquered. Restore with exact sermon locator and context. |
| `CLM-SPURGEON-LION-LAMB` — Spurgeon lion for enemies / lamb for friends aphorism | `REMOVE` | нет | Exact aphorism not found in the official sermon corpus checked. Remove; use actual lion/Lamb material only. |
| `CLM-BAUCHAM-SISSIFIED` — Baucham sissified, needy Jesus | `PRIMARY-AUDIO-VERIFIED` | да | Verified by preserved official media clip; a contemporaneous report independently corroborates the Brokenness sermon wording. Cite as sermon/audio, not book text. |
| `CLM-OWEN-BURN-BIBLES` — Owen without the Spirit burn our Bibles | `OFFICIAL-REPLACEMENT` | да | Do not present the modern compression as Owen's verbatim sentence. Replace it with Owen's exact primary claims that Scripture becomes a dead letter without the Spirit's powerful efficacy and that the Spirit alone gives saving understanding. |
| `CLM-HUGHES-EXPULSIVE` — Hughes expulsive force on 2 Corinthians 3:18 | `REMOVE` | нет | Remove Hughes attribution. The load-bearing phrase belongs to Thomas Chalmers; cite Chalmers directly. |
| `CLM-AUGUSTINE-SPLENDIDA` — splendida vitia as verbatim Augustine | `RECEPTION-ONLY` | нет | Use only as a later reception label. Augustine's substantive argument may be cited from primary loci, but the Latin phrase is not quoted as Augustine. |
| `CLM-WATSON-MORALITY` — Watson morality aphorism from quote collection | `REMOVE` | нет | Remove the quote-collection wording unless a primary section is later opened. Watson remains usable through verified primary texts. |
| `CLM-MCHEYNE-TEN-LOOKS` — M'Cheyne ten looks at Christ | `PRIMARY-VERIFIED` | да | The wording is verified in M'Cheyne's letter as printed in Memoir and Remains. Do not claim that M'Cheyne coined it or that Baxter is its proven origin. |
| `CLM-KOTZKER-HEART` — Kotzker words on/on-in the heart story | `REMOVE` | нет | No adequate primary attribution was found. Remove the name and preferably the illustration; it may not be used as a historical claim. |
| `CLM-WATSON-PANDECT` — Watson Scripture is the pandect of divine knowledge | `PRIMARY-VERIFIED` | да | Verified in the 1670 EEBO-TCP text of Heaven Taken by Storm. |
| `CLM-HAMILTON-MONOGRAPH` — Hamilton monograph quote-site wording | `PARAPHRASE-ONLY` | нет | Remove Goodreads/quote-site book wording. Use Hamilton's peer-reviewed Themelios argument or paraphrase the monograph only with a legal edition. |
| `CLM-FERGUSON-BOOK` — Ferguson The Holy Spirit direct book quote | `OFFICIAL-REPLACEMENT` | да | Use Ferguson's official Ligonier teaching transcript. Do not make a book-page claim without the book. |
| `CLM-ORTLUND-CH15` — Ortlund chapter 15 lion/lamb wording | `OFFICIAL-REPLACEMENT` | да | Use Crossway's official Q&A and article; no unsupported chapter/page claim. |
| `CLM-ROGERS-ADVICE` — Rogers Advice 1, 5, 6 provenance | `PRIMARY-VERIFIED` | да | Closed through Site PR #510 visual 1691 scan readback: printed ii/PDF17, xii/PDF27, xiv/PDF29. EEBO-TCP remains search aid only. |
| `CLM-MLJ-BOOK` — MLJ Spiritual Depression book wording | `PARAPHRASE-ONLY` | нет | Do not quote the book without legal full text. Official sermon metadata/audio may support only what it actually exposes. |
| `CLM-PDF-LONG-QUOTES` — Long quotations from OCR/searchable PDFs without page image | `PARAPHRASE-ONLY` | нет | No long direct quote is authorized from OCR alone. Use short checked anchors or paraphrase; page-image verification is required for long quotations. |

## 4. Главные исправления прежнего ledger

### Spurgeon: free will

Старая классификация `APOCRYPHAL-RISK` отменена. Формула находится в первичном sermon locus: `Samson Conquered`, sermon №224. Разрешение: точная короткая цитата с названием и номером проповеди; не превращать её в систематическое определение воли.

### Baucham: “sissified, needy Jesus”

Старая классификация `not verified` отменена. Сохранились media witness и contemporaneous report проповеди. Разрешение: цитировать только как устную формулировку из проповеди `Brokenness`, не как книжный текст и не как самостоятельный богословский фундамент.

### Owen: “burn our Bibles”

Современный афористический вариант больше не выдаётся за дословную фразу Owen. Вместо него используются его первичные утверждения из `Pneumatologia`: без действенной работы Духа Писание остаётся для человека «dead letter», а спасительное понимание воли Божией требует особой просвещающей работы Духа. Это сильнее и точнее позднего лозунга.

### Hughes / Chalmers

Формула `expulsive power` возвращена Thomas Chalmers. Hughes attribution удалена. Нельзя переносить фразу Chalmers в Hughes только потому, что Hughes применяет сходную мысль.

### Whitefield

История-ответ «почему снова born again?» удалена как документированный факт. Содержательная нужда закрывается реальной проповедью `On Regeneration`. Старая непроверенная фраза о каменистой почве заменена первичной `Directions How to Hear Sermons`.

### Watson

`The Scripture is the pandect of divine knowledge` подтверждено в EEBO-TCP тексте `Heaven Taken by Storm` и разрешено. Другой morality aphorism из quote-collection удалён.

### Augustine

`splendida vitia` остаётся историей рецепции. Оно не оформляется как дословная цитата Augustine. Содержательная аргументация строится на `Contra Iulianum` и `City of God`.

### M’Cheyne

Фраза о десяти взглядах подтверждена как текст письма, напечатанный в `Memoir and Remains`. Разрешено утверждать только это. Не разрешено утверждать, что M’Cheyne первым создал формулу или что её происхождение от Baxter доказано.

### Rogers / MLJ / Ferguson / Hamilton / Ortlund

- Rogers: scan-first provenance закрыта Site PR `#510` точными printed/PDF locators.
- MLJ book: не цитируется без легального полного текста; официальный sermon page не подменяет книгу.
- Ferguson: книжная цитата заменена официальным Ligonier teaching transcript.
- Hamilton: Goodreads/book-snippet wording удалено; используется peer-reviewed Themelios layer.
- Ortlund: неподтверждённая книжная страница заменена официальными материалами Crossway.

## 5. Полный источниковый registry

| ID | Автор | Работа | Класс | Формат | Функция |
|---|---|---|---|---|---|
| `SRC-001` | George Whitefield | [On Regeneration](https://ccel.org/ccel/whitefield/sermons.li.html) | `primary_text` | HTML | R1 direct regeneration doctrine |
| `SRC-002` | George Whitefield | [Directions How to Hear Sermons](https://www.ccel.org/ccel/whitefield/sermons.xxx.html) | `primary_text` | HTML | R4 primary replacement for unlocated stony-ground wording |
| `SRC-003` | George Whitefield | [Selected Sermons](https://ccel.org/ccel/w/whitefield/sermons/cache/sermons.pdf) | `primary_text` | PDF | Whitefield corpus control |
| `SRC-004` | C. H. Spurgeon | [Samson Conquered](https://www.spurgeon.org/resource-library/sermons/samson-conquered/) | `official_author_archive` | HTML | R3 verifies free-will aphorism in sermon 224 |
| `SRC-005` | C. H. Spurgeon | [Among Lions](https://www.spurgeon.org/resource-library/sermons/among-lions/) | `official_author_archive` | HTML | R9 controls lion language; does not support old exact aphorism |
| `SRC-006` | C. H. Spurgeon | [The Lions' Den](https://www.spurgeon.org/resource-library/sermons/the-lions-den/) | `official_author_archive` | HTML | R9 verified substitute |
| `SRC-007` | C. H. Spurgeon | [David's Prayer in the Cave](https://www.spurgeon.org/resource-library/sermons/davids-prayer-in-the-cave/) | `official_author_archive` | HTML | R9 verified substitute |
| `SRC-008` | C. H. Spurgeon | [David's Prayer in the Cave](https://www.spurgeon.org/wp-content/uploads/2020/03/50_David_s_Prayer_in_the_Cave.pdf) | `official_author_archive` | PDF | R9 page-stable sermon PDF |
| `SRC-009` | Thomas Watson | [Heaven Taken by Storm](https://quod.lib.umich.edu/e/eebo/A65299.0001.001/1:4?rgn=div1&view=fulltext) | `primary_text` | EEBO-TCP | R7a verifies pandect of divine knowledge |
| `SRC-010` | Thomas Watson | [Heaven Taken by Storm item record](https://quod.lib.umich.edu/e/eebo/A65299.0001.001?view=toc) | `primary_bibliographic` | EEBO-TCP | edition and rights control |
| `SRC-011` | Thomas Watson | [Heaven Taken by Storm catalogue](https://catalog.folger.edu/record/153910) | `library_catalog` | Catalogue | 1669 edition control |
| `SRC-012` | John Owen | [Pneumatologia: name and doctrine of the Spirit](https://ccel.org/ccel/owen/pneum/pneum.i.v.ii.html) | `primary_text` | HTML | R7a primary replacement for burn-Bibles condensation |
| `SRC-013` | John Owen | [Understanding the Mind of God in Scripture](https://www.ccel.org/ccel/owen/pneum.i.xii.v.html) | `primary_text` | HTML | R7a Spirit and Scripture exact primary passage |
| `SRC-014` | John Owen | [Spirit's composition and disposal of Scripture](https://www.ccel.org/ccel/owen/pneum/pneum.i.xii.x.html) | `primary_text` | HTML | R7a sufficiency and illumination |
| `SRC-015` | John Owen | [Old Testament operations of the Spirit](https://www.ccel.org/ccel/owen/pneum.i.vi.i.html) | `primary_text` | HTML | R2 continuity/discontinuity |
| `SRC-016` | John Owen | [Pneumatologia, regeneration](https://www.ccel.org/ccel/owen/pneum/pneum.i.vii.i.html) | `primary_text` | HTML | R1/R2 regeneration |
| `SRC-017` | John Owen | [Mortification of Sin, chapter II](https://www.ccel.org/ccel/owen/mort.i.v.html) | `primary_text` | HTML | R5 killing sin quote |
| `SRC-018` | John Owen | [Mortification of Sin, chapter VII](https://www.ccel.org/ccel/owen/mort.i.x.html) | `primary_text` | HTML | R5 exact context |
| `SRC-019` | John Owen | [Of Temptation](https://www.ccel.org/ccel/owen/temptation.html) | `primary_text` | HTML | temptation and heart |
| `SRC-020` | John Owen | [Glory of Christ TOC](https://www.ccel.org/ccel/owen/glory/glory.toc.html) | `primary_text` | HTML | R8 chapter map |
| `SRC-021` | John Owen | [Glory of Christ plain text](https://ccel.org/ccel/o/owen/glory/cache/glory.txt) | `primary_text` | TXT | R8 corpus search |
| `SRC-022` | John Owen | [Works volume 3 scan](https://archive.org/details/worksofjohnowe03owen) | `primary_scan` | Scan/PDF | edition control for Pneumatologia |
| `SRC-023` | John Owen | [Works volume 3](https://books.google.com/books/about/The_Works_of_John_Owen.html?id=qHAuAAAAYAAJ) | `primary_scan` | Google Books | edition and pagination control |
| `SRC-024` | John Owen | [Works bibliography](https://johnowen.org/bibliography/) | `scholarly_bibliography` | HTML | work/edition identity |
| `SRC-025` | Thomas Boston | [Human Nature in Its Fourfold State](https://archive.org/details/humannatureinits00bostuoft) | `primary_scan` | Scan/PDF | R1/R3 anthropology |
| `SRC-026` | Thomas Boston | [Human Nature in Its Fourfold State, 1771](https://archive.org/details/bim_eighteenth-century_human-nature-in-its-four_boston-thomas_1771) | `primary_scan` | Scan/PDF | early edition control |
| `SRC-027` | 1689 London Baptist Confession | [Chapter 9, Of Free Will](https://www.bible-researcher.com/1689/chapter9.html) | `confessional_primary` | HTML | free-will and states |
| `SRC-028` | 1689 London Baptist Confession | [Chapter 21, Christian Liberty](https://www.the1689confession.com/1689/chapter-21) | `confessional_primary` | HTML | conscience/liberty |
| `SRC-029` | Westminster Assembly | [Westminster Confession](https://thewestminsterstandard.org/the-westminster-confession/) | `confessional_primary` | HTML | confessional comparison |
| `SRC-030` | Savoy Assembly | [Savoy Declaration](https://www.the-highway.com/savoy_declaration.html) | `confessional_primary` | HTML | confessional comparison |
| `SRC-031` | William Perkins | [A Golden Chaine](https://archive.org/details/goldenchaineorde00perk) | `primary_scan` | Scan/PDF | states and calling |
| `SRC-032` | William Perkins | [Cases of Conscience](https://quod.lib.umich.edu/e/eebo/A09365.0001.001?view=toc) | `primary_text` | EEBO-TCP | conscience locator |
| `SRC-033` | William Ames | [Conscience with the Power and Cases Thereof](https://quod.lib.umich.edu/e/eebo/A69129.0001.001?view=toc) | `primary_text` | EEBO-TCP | conscience taxonomy |
| `SRC-034` | Stephen Charnock | [Works vol. 3](https://www.digitalpuritan.net/Digital%20Puritan%20Resources/Charnock%2C%20Stephen/The%20Complete%20Works%20of%20Stephen%20Charnock%20%28vol.3%29.txt.html) | `primary_text` | TXT/HTML | practical atheism and regeneration |
| `SRC-035` | Thomas Manton | [Works vol. 4, James 1:21](https://www.ccel.org/ccel/manton/manton04.iv.html) | `primary_text` | HTML | R7a ingrafted word |
| `SRC-036` | Jonathan Edwards | [Religious Affections](https://www.ccel.org/ccel/edwards/affections.html) | `primary_text` | HTML | R5 signs and affections |
| `SRC-037` | Matthew Mead | [The Almost Christian Discovered](https://www.ccel.org/ccel/mead_matthew/almost.html) | `primary_text` | HTML | R5 false peace and struggle |
| `SRC-038` | Thomas Shepard | [The Sincere Convert, 1650](https://archive.org/details/bim_early-english-books-1641-1700_the-sincere-convert-_shepard-thomas_1650_0) | `primary_scan` | Scan/PDF | false conversion |
| `SRC-039` | Joseph Alleine | [An Alarm to the Unconverted](https://archive.org/details/alarmtounconvert00allerich) | `primary_scan` | Scan/PDF | conversion and false peace |
| `SRC-040` | William Guthrie | [The Christian's Great Interest](https://www.ccel.org/g/guthrie/interest/int.htm) | `primary_text` | HTML | assurance and saving change |
| `SRC-041` | Thomas Hooker | [The Poor Doubting Christian](https://archive.org/details/bim_early-english-books-1641-1700_the-poor-doubting-christ_hooker-thomas_1664) | `primary_scan` | Scan/PDF | assurance and self-qualification |
| `SRC-042` | Thomas Brooks | [Heaven on Earth](https://www.gracegems.org/Brooks/heaven_on_earth2.htm) | `primary_text_reproduction` | HTML | assurance |
| `SRC-043` | Walter Marshall | [The Gospel Mystery of Sanctification](https://www.monergism.com/thethreshold/articles/onsite/GospelMystery.pdf) | `primary_text_reproduction` | PDF | union and sanctification |
| `SRC-044` | Anthony Burgess | [Spiritual Refining](https://quod.lib.umich.edu/e/eebo/A30243.0001.001) | `primary_text` | EEBO-TCP | true/counterfeit grace |
| `SRC-045` | John Flavel | [Touchstone of Sincerity](https://archive.org/details/touchstoneofsinc00flav) | `primary_scan` | Scan/PDF | sincerity and assurance |
| `SRC-046` | Thomas Goodwin | [Works vol. 6](https://www.digitalpuritan.net/Digital%20Puritan%20Resources/Goodwin%2C%20Thomas/The%20Works%20of%20Thomas%20Goodwin%20%28vol.6%29.txt.html) | `primary_text_reproduction` | TXT/HTML | Christ's righteousness |
| `SRC-047` | Samuel Bolton | [The True Bounds of Christian Freedom](https://www.monergism.com/true-bounds-christian-freedom-ebook) | `primary_text_reproduction` | HTML/PDF | law/gospel and liberty |
| `SRC-048` | Daniel Dyke | [The Mystery of Self-Deceiving, 1633](https://archive.org/details/bim_early-english-books-1475-1640_the-mystery-of-self-dece_dyke-daniel_1633) | `primary_scan` | Scan/PDF | self-deceit |
| `SRC-049` | John Bunyan | [A Treatise of the Fear of God](https://quod.lib.umich.edu/e/eebo/A30211.0001.001/1:2.5?rgn=div2;view=fulltext) | `primary_text` | EEBO-TCP | fear of God |
| `SRC-050` | Robert Bolton | [Instructions for a Right Comforting Afflicted Consciences](https://ota.bodleian.ox.ac.uk/repository/xmlui/bitstream/handle/20.500.12024/A16330/A16330.html?isAllowed=y&sequence=5) | `primary_text` | TCP/HTML | afflicted conscience |
| `SRC-051` | Thomas Taylor | [The Parable of the Sower, 1621](https://www.hailandfire.com/library_books/H%26F_Taylor%28Thomas%29_ParableoftheSower1621.pdf) | `primary_text_reproduction` | PDF | R4 soils |
| `SRC-052` | Richard Sibbes | [The Bruised Reed](https://www.monergism.com/thethreshold/sdg/bruisedreed.html) | `primary_text_reproduction` | HTML | weak grace safeguard |
| `SRC-053` | Thomas Goodwin | [A Child of Light Walking in Darkness](https://www.monergism.com/thethreshold/sdg/goodwin/A%20Child%20of%20Light%20Walking%20in%20Darkness%20-%20Goodwin.pdf) | `primary_text_reproduction` | PDF | darkness/desertion |
| `SRC-054` | William Bridge | [A Lifting Up for the Downcast](https://www.monergism.com/thethreshold/sdg/bridge/A%20Lifting%20Up%20for%20the%20Downcast%20-%20Bridge.pdf) | `primary_text_reproduction` | PDF | downcast believer |
| `SRC-055` | Timothy Rogers | [A Discourse Concerning Trouble of Mind, 1706](https://archive.org/details/bim_eighteenth-century_a-discourse-concerning-t_rogers-timothy_1706) | `primary_scan` | Scan/PDF | edition control; Site uses 1691 scan locators |
| `SRC-056` | Timothy Rogers | [A Discourse Concerning Trouble of Mind, 1691](https://quod.lib.umich.edu/e/eebo2/A57573.0001.001/) | `primary_text_rights_limited` | EEBO-TCP | search/locator only, rights boundary |
| `SRC-057` | Richard Baxter | [Preservatives against Melancholy, 1713](https://archive.org/details/bim_eighteenth-century_preservatives-against-me_baxter-richard_1713) | `primary_scan` | Scan/PDF | historical melancholy |
| `SRC-058` | Richard Baxter | [A Christian Directory](https://quod.lib.umich.edu/e/eebo/A26892.0001.001/?view=toc) | `primary_text` | EEBO-TCP | pastoral directions |
| `SRC-059` | William Gurnall | [The Christian in Complete Armour](https://www.ccel.org/ccel/gurnall/armour/files/gurnal01a.pdf) | `primary_text_reproduction` | PDF | temptation and despair |
| `SRC-060` | Thomas Watson | [The Doctrine of Repentance, 1668](https://archive.org/details/bim_early-english-books-1641-1700_the-doctrine-of-repentan_watson-thomas_1668/page/n3/mode/2up) | `primary_scan` | Scan/PDF | repentance |
| `SRC-061` | Jeremiah Burroughs | [The Evil of Evils](https://www.monergism.com/thethreshold/sdg/burroughs/The%20Evil%20of%20Evils%20-%20Jeremiah%20Burroughs.pdf) | `primary_text_reproduction` | PDF | sin and repentance |
| `SRC-062` | Richard Sibbes | [The Returning Backslider](https://quod.lib.umich.edu/e/eebo2/A12190.0001.001?view=toc) | `primary_text` | EEBO-TCP | backsliding |
| `SRC-063` | John Flavel | [Christ Altogether Lovely](https://www.ccel.org/ccel/flavel/lovely.html) | `primary_text` | HTML | R8 Christ's glory |
| `SRC-064` | Thomas Goodwin | [The Heart of Christ](https://www.monergism.com/thethreshold/sdg/goodwin/The_Heart_of_Christ_-_Thomas_Goodwin.pdf) | `primary_text_reproduction` | PDF | R9 short anchors only |
| `SRC-065` | Thomas Shepard | [The Sound Believer](https://www.monergism.com/sound-believer-ebook) | `primary_text_reproduction` | HTML/PDF | duties and Christ |
| `SRC-066` | David Clarkson | [Soul Idolatry Excludes Men Out of Heaven](https://www.monergism.com/soul-idolatry-excludes-men-out-heaven) | `primary_text_reproduction` | HTML | heart idolatry |
| `SRC-067` | Jeremiah Burroughs | [Moses His Choice](https://quod.lib.umich.edu/e/eebo/A30592.0001.001?view=toc) | `primary_text` | EEBO-TCP | self-denial |
| `SRC-068` | Richard Gilpin | [Demonologia Sacra](https://quod.lib.umich.edu/e/eebo/A42781.0001.001) | `primary_text` | EEBO-TCP | temptation |
| `SRC-069` | Richard Capel | [Tentations: Their Nature, Danger, Cure](https://quod.lib.umich.edu/e/eebo/A17936.0001.001?view=toc) | `primary_text` | EEBO-TCP | temptation |
| `SRC-070` | James M. Hamilton Jr. | [Were Old Covenant Believers Indwelt by the Holy Spirit?](https://www.thegospelcoalition.org/themelios/article/were-old-covenant-believers-indwelt-by-the-holy-spirit/) | `academic_journal` | HTML | R2 official Themelios argument |
| `SRC-071` | Sinclair Ferguson | [Old Testament Indwelling of the Spirit](https://learn.ligonier.org/sermons/old-testament-indwelling-of-the-spirit) | `official_ministry_transcript` | HTML/Audio | R2 replaces unverified book quotation |
| `SRC-072` | R. C. Sproul | [The New Birth](https://learn.ligonier.org/articles/new-birth) | `official_ministry` | HTML | R1 regeneration precedes faith |
| `SRC-073` | Dane Ortlund | [Does Gentle and Lowly Ignore God's Wrath?](https://www.crossway.org/articles/does-gentle-and-lowly-ignore-gods-wrath/) | `official_publisher` | HTML | R9 official wrath/gentleness balance |
| `SRC-074` | Dane Ortlund | [Beset with Weakness](https://www.crossway.org/articles/beset-with-weakness/) | `official_publisher` | HTML | R9 official lion-like judgment/lamb-like tenderness replacement |
| `SRC-075` | Voddie Baucham | [Brokenness / Sissified Jesus clip](https://wretched.org/tv/voddie-baucham-sissified-jesus/) | `official_media` | Video | R9 primary-audio witness |
| `SRC-076` | Voddie Baucham | [Brokenness sermon contemporaneous report](https://justinwheeler.wordpress.com/2009/03/02/tcc-09-vodie-baucham-brokenness/) | `contemporaneous_transcript` | HTML | R9 exact wording corroboration, not sole authority |
| `SRC-077` | Robert Murray M'Cheyne | [Memoir and Remains](https://books.google.com/books/about/Memoir_and_Remains_of_the_Rev_Robert_Mur.html?id=dPU4AQAAMAAJ) | `primary_scan` | Google Books | R8 letter page locus |
| `SRC-078` | Timothy Rogers | [A Discourse Concerning Trouble of Mind](https://books.google.com/books/about/A_Discourse_concerning_Trouble_of_Mind_a.html?id=yMRjAAAAcAAJ) | `primary_scan` | Google Books | Rogers 1691 scan family; exact Site locators authoritative |
| `SRC-079` | BibleHub | [Hebrews 4:2 interlinear/text](https://biblehub.com/text/hebrews/4-2.htm) | `open_reference` | HTML | R7a textual-form control |
| `SRC-080` | Heinrich Meyer | [Hebrews 4 commentary](https://www.studylight.org/commentaries/eng/hmc/hebrews-4.html) | `public_domain_commentary` | HTML | R7a variant discussion |
| `SRC-081` | Thomas Chalmers | [The Expulsive Power of a New Affection](https://www.cslewisinstitute.org/resources/the-expulsive-power-of-a-new-affection/) | `primary_text_reproduction` | HTML | R8 correct source for expulsive-force language |
| `SRC-082` | Thomas Chalmers | [The Expulsive Power of a New Affection PDF](https://www.cslewisinstitute.org/wp-content/plugins/adorechurch-core/download/download.php?file=https%3A%2F%2Fwww.cslewisinstitute.org%2Fwp-content%2Fuploads%2FExpulsivePoweDiscourseIX.pdf) | `primary_text_reproduction` | PDF | R8 page-stable reproduction |
| `SRC-083` | Augustine | [Contra Iulianum, Migne edition](https://la.wikisource.org/wiki/Contra_Iulianum_%28ed._Migne%29) | `primary_text` | Latin HTML | R3 verified Augustine locus; not splendida vitia formula |
| `SRC-084` | Augustine | [City of God](https://www.newadvent.org/fathers/1201.htm) | `primary_text_reproduction` | HTML | R3 Augustine theology control |
| `SRC-085` | Martyn Lloyd-Jones | [Reflecting His Glory](https://www.mljtrust.org/sermon/reflecting-his-glory/) | `official_ministry` | Audio/metadata | R8 official sermon page; no invented transcript quote |

## 6. Публикационный контракт

Перед публикацией исторической цитаты обязательны:

1. автор;
2. точное произведение;
3. устойчивый locator — глава/раздел/sermon number/page;
4. контекст, не меняющий смысл;
5. evidence class;
6. отсутствие более поздней authority, которая ограничивает использование.

Запрещено:

- использовать publisher description как текст автора;
- использовать quote-site как доказательство;
- называть OCR page-image verification;
- оставлять спорную атрибуцию без конечного решения;
- переносить фразу одного автора другому;
- выдавать редакционное сжатие за дословную цитату.

## 7. Финальный disposition

```text
85 UNIQUE SOURCE RECORDS
81 TRUSTED PRIMARY / OPEN / OFFICIAL / ACADEMIC RECORDS
18 DISPUTED CLAIMS CLASSIFIED
NO C/D SOURCE CAN BECOME QUOTE-SAFE
OLD DANGLING HOLDS CONVERTED TO FINAL PERMISSION BOUNDARIES
SPURGEON FREE-WILL LOCUS RESTORED
BAUCHAM SERMON WORDING VERIFIED AS AUDIO/ORAL MATERIAL
OWEN MODERN APHORISM REPLACED BY OWEN PRIMARY TEXT
HUGHES MISATTRIBUTION REMOVED; CHALMERS RESTORED
WHITEFIELD ANECDOTE REMOVED; PRIMARY SERMONS USED
ROGERS SCAN-FIRST LOCATORS PRESERVED
PUBLICATION SOURCE-CLOSURE COMPLETE FOR THE LISTED CLAIMS
```
