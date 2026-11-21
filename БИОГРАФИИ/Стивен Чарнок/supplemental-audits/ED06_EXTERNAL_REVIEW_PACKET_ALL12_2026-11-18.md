# Чарнок ED-06 — единый пакет внешней рецензии 12 рабочих переводов (18.11.2026)

**RESEARCH_ONLY / CHECKSUM_VERIFIED / EXTERNAL_REVIEW 0/12 / NO_APPROVAL / NO_PUBLICATION.**

Это **транспортный пакет** неизменённых английских фрагментов и русских рабочих переводов. Автоматическое формирование не заменяет независимую филологическую рецензию и не даёт права публикации.

- Основание: Research/main, `data/charnock-series-editorial-plan-v1.json`.
- План: 2 464 207 байт; SHA-256 `31a309e2031a57b1d2368da0050feaf89c01c37581c9c507a001f104bef98ad3`; защищённый Git blob `5e1d2bf3f8bf35f19dc76adb0be38b48c5e73738`.
- Обнаружены все 12 позиций в **пяти** разделах канона. Проверка SHA-256: английские оригиналы **12/12 PASS**, русские черновики **12/12 PASS**.
- Состояние независимого подтверждения: **0/12**. Ни у одного элемента нет reviewer и reviewedTranslationSha256.
- Авторство: `CHARNOCK_BODY` = текст Чарнока; `VEEL_EDITORIAL` и `VEEL_ADAMS_EDITORIAL` = слова редакторов, нельзя выдавать за авторскую цитату.

## Реестр всех двенадцати

| ID | Поле канонического JSON | Роль | Источник / печатная TEI-страница | EN/RU checksum | Peer-review |
|---|---|---|---|---|---|
| `TR-TXT03` | `translationReview.items` | `CHARNOCK_BODY` | A32724 / 64 | PASS / PASS | NOT_PERFORMED |
| `TR-TXT08` | `translationReview.items` | `CHARNOCK_BODY` | A32726 / 7 | PASS / PASS | NOT_PERFORMED |
| `TR-VEEL` | `translationReview.items` | `VEEL_EDITORIAL` | B20167 / not specified | PASS / PASS | NOT_PERFORMED |
| `TR-MERCY` | `translationReview.items` | `CHARNOCK_BODY` | B20167 / 1 | PASS / PASS | NOT_PERFORMED |
| `TR-Q-04` | `editorialTranslationReview.items` | `VEEL_ADAMS_EDITORIAL` | A32723 / not specified | PASS / PASS | NOT_PERFORMED |
| `TR-Q-05` | `editorialTranslationReview.items` | `VEEL_ADAMS_EDITORIAL` | A32723 / not specified | PASS / PASS | NOT_PERFORMED |
| `TR-Q-10` | `editorialTranslationReview.items` | `VEEL_ADAMS_EDITORIAL` | A32723 / not specified | PASS / PASS | NOT_PERFORMED |
| `TR-Q-06` | `authorialTranslationReview.items` | `CHARNOCK_BODY` | A32724 / 20 | PASS / PASS | NOT_PERFORMED |
| `TR-Q-07` | `authorialTranslationReview.items` | `CHARNOCK_BODY` | A32723 / 222 | PASS / PASS | NOT_PERFORMED |
| `TR-Q-08` | `atheismReview.translation` | `CHARNOCK_BODY` | A32723 (родительская карточка) / 47 из родительской карточки | PASS / PASS | NOT_PERFORMED |
| `TR-Q-12` | `enmityReview.translations` | `CHARNOCK_BODY` | B20167 / not specified | PASS / PASS | NOT_PERFORMED |
| `TR-Q-16` | `enmityReview.translations` | `VEEL_EDITORIAL` | B20167 / not specified | PASS / PASS | NOT_PERFORMED |

## Правила работы независимого рецензента

1. Сначала подтвердить английскую строку по указанному источнику и, по возможности, его факсимиле. Отмечать различия старой орфографии, пунктуации и редакционной передачи.
2. Проверить *каждое предложение*: субъект, местоимения, модальность, логические связки, цитаты из Библии, факт сокращений, богословские термины. Не заменять экспертизу согласием с ранее предложенным AI-решением.
3. Для каждой пары возвратить **ACCEPT / REVISE / REJECT**, квалификацию и подпись рецензента, дату, источники, мотивированную корректуру русского текста и только после утверждения её точный SHA-256.
4. Не менять утверждённый план, source/rights registry, protected copies, Telegraph, Telegram, очередь или архивные квитанции без отдельной редакционной процедуры.

## Указанные заранее вопросы к рецензенту (не готовые вердикты)

- **TR-Q-06**: субъект выражения It is also Prophetical — псалом; двусмысленное русское «он» нужно заменить. Оборот It seems ... Ecstatical оценить отдельно.
- **TR-Q-07**: active creation — Божья воля и сила творить; существующие от вечности воля и сила не равны сотворённому во времени миру. Уточнить оба This.
- **TR-Q-10**: английское sweetness of Practical эллиптически содержит подразумеваемое divinity; рассмотреть явное русское [богословия].
- **TR-Q-08**: source отсутствует только в дочернем элементе; родительский atheismReview.byteVerifiedContext фиксирует A32723, печатную страницу 47 и 244-й параграф в нумерации с нуля.
- **TR-Q-04/05/10, TR-VEEL, TR-Q-16**: редакционная речь Вила/Адамса не должна приписываться самому Чарноку.

## Полные исходные пары для независимой сверки

### 01. `TR-TXT03`

- Поле: `translationReview.items`; источник: `A32724`; роль: `CHARNOCK_BODY`; страница: 64.
- English SHA-256: `1ba91bc903f2b3d32b9e97622984f75e15520ddfeec97cdfe1eb76ae3c474921`; русский SHA-256: `e86a6c162d621abe22a3069b6d53603afa58908ee3620a7254ca130ac58a27f0`.
- Canonical row SHA-256: `not stored`; independentReview.state = NOT_PERFORMED.

**Английский оригинал (без правок):**

> Six men] A certain number. Whether the Holy Ghost alludes to a particular number of Nations, which the Chaldean Army might be composed of under their Prince, who reign'd over several Countries; or respects the other chief Captains or Marshals of his Army which are nam'd, Jer. 39.3. or speaks with reference to the other places wherein the City was assaulted by that Army, as some think, is uncertain.

**Русский рабочий черновик (без правок):**

> «Шесть мужей» — определённое число. Неясно, намекает ли Святой Дух на определённое число народов, из которых могло состоять халдейское войско под властью их государя, правившего несколькими странами; или имеет в виду других главных начальников или военачальников его войска, названных в Иер. 39:3; или говорит, как полагают некоторые, применительно к другим местам, в которых это войско штурмовало город.

**Рецензент:** NOT_REVIEWED; дата: —; замечания: —; финальный русский текст: —; approved reviewedTranslationSha256: null.

### 02. `TR-TXT08`

- Поле: `translationReview.items`; источник: `A32726`; роль: `CHARNOCK_BODY`; страница: 7.
- English SHA-256: `370640653f23a36b1262e4f6f06900690d846ff8def6a851bcded4890cb689c6`; русский SHA-256: `a516e5aa9a869d1ecb06191fd3e6e7cd0b95b39b46a414fc87696e149f391465`.
- Canonical row SHA-256: `not stored`; independentReview.state = NOT_PERFORMED.

**Английский оригинал (без правок):**

> 'Tis not a bare sight of things that is here meant by Gods eye, but a sight and knowledge in order to the Governing and disposing of them.

**Русский рабочий черновик (без правок):**

> Здесь под Божьим оком понимается не простое созерцание вещей, а видение и знание ради управления ими и их устроения.

**Рецензент:** NOT_REVIEWED; дата: —; замечания: —; финальный русский текст: —; approved reviewedTranslationSha256: null.

### 03. `TR-VEEL`

- Поле: `translationReview.items`; источник: `B20167`; роль: `VEEL_EDITORIAL`; страница: not specified.
- English SHA-256: `2fb361af0a7a0ada8cf7283513779c69479236e8f451716185d049e388fac67c`; русский SHA-256: `a624369c269a56e0b0d90e64029867cc1a1f8e953549c94eb08f92a203c9bc8d`.
- Canonical row SHA-256: `not stored`; independentReview.state = NOT_PERFORMED.

**Английский оригинал (без правок):**

> The Papers I have seen, and with Mr. Ashton's help, have (so far as was needful) compared the Transcription with them.

**Русский рабочий черновик (без правок):**

> Я видел эти бумаги и с помощью г-на Эштона сверил с ними переписанный текст — в той мере, в какой это было нужно.

**Рецензент:** NOT_REVIEWED; дата: —; замечания: —; финальный русский текст: —; approved reviewedTranslationSha256: null.

### 04. `TR-MERCY`

- Поле: `translationReview.items`; источник: `B20167`; роль: `CHARNOCK_BODY`; страница: 1.
- English SHA-256: `c28b9586d6f4636a8bc968910a2104e3c963763b25a6feb441d9f0d97ec3cb2c`; русский SHA-256: `ea0f037aea32f8f25502dc93a50374d49ab46c9f1384037c1d362ce2105e9b2c`.
- Canonical row SHA-256: `not stored`; independentReview.state = NOT_PERFORMED.

**Английский оригинал (без правок):**

> 2. God doth often make the chiefest Sinners Objects of his choicest Mercy.

**Русский рабочий черновик (без правок):**

> 2. Бог нередко делает величайших грешников предметом Своей драгоценнейшей милости.

**Рецензент:** NOT_REVIEWED; дата: —; замечания: —; финальный русский текст: —; approved reviewedTranslationSha256: null.

### 05. `TR-Q-04`

- Поле: `editorialTranslationReview.items`; источник: `A32723`; роль: `VEEL_ADAMS_EDITORIAL`; страница: not specified.
- English SHA-256: `bcc4dddc512d4afea8b95afb451e4a3534c80b6c6aceca3ea4e6a04a154528b2`; русский SHA-256: `f79b6197314267820f9a5c8d2e7a99742055e92dcb59efe15f0b104a99b986b9`.
- Canonical row SHA-256: `a86f173144f676994a755813cd61f062566ed31675a12fddd9fff2cf49751fb6`; independentReview.state = NOT_PERFORMED.

**Английский оригинал (без правок):**

> Though he make great use of Schoolmen, yet they are certainly more beholden to him, than he to them; he adopts their Notions, but he refines them too, and improves them, and reforms them from the barbarousness in which they were expressed, and dresseth them up in his own Language (so far as the nature of the matter will permit, and more clear terms are to be found) and so makes them intelligible to Vulgar Capacities, which in their original rudeness were obscure and strange, even to Learned Heads.

**Русский рабочий черновик (без правок):**

> Хотя он широко пользуется схоластами, они, несомненно, больше обязаны ему, чем он им: он перенимает их понятия, но также очищает их, улучшает и освобождает от варварской грубости, с которой они были выражены, облекая их в собственный язык (насколько допускает природа предмета и удаётся найти более ясные выражения), и тем самым делает их доступными обыкновенному разумению, тогда как в своей первоначальной грубой форме они были тёмными и странными даже для учёных умов.

**Рецензент:** NOT_REVIEWED; дата: —; замечания: —; финальный русский текст: —; approved reviewedTranslationSha256: null.

### 06. `TR-Q-05`

- Поле: `editorialTranslationReview.items`; источник: `A32723`; роль: `VEEL_ADAMS_EDITORIAL`; страница: not specified.
- English SHA-256: `4bd47b2aed471a844b99d7a64fe7fe2eb44789f8a932fa653fef6a4b98e98f23`; русский SHA-256: `bcedc5c224bb53f38e7bfa3a09587ff4b27e652b8dd11ad2330913f2177395bc`.
- Canonical row SHA-256: `8323187f3d54d52740f27313c517497ab2a1f77fa3472999f90edb9a0b01f087`; independentReview.state = NOT_PERFORMED.

**Английский оригинал (без правок):**

> THIS long since promised, and greatly expected Volume of the Reverend Authour upon the Divine Attributes, being Transcribed out of his own Manuscripts, by the unwearied diligence of those worthy Persons that undertook it, is now at last come to thy hands: Doubt not but thy Reading will pay for thy waiting, and thy satisfaction make full compensation for thy patience.

**Русский рабочий черновик (без правок):**

> Этот давно обещанный и с большим нетерпением ожидавшийся том почтенного автора о Божественных атрибутах, переписанный с его собственных рукописей благодаря неутомимому усердию достойных людей, взявшихся за это дело, наконец оказался у тебя в руках: не сомневайся, что чтение вознаградит твоё ожидание, а удовлетворение вполне окупит твоё терпение.

**Рецензент:** NOT_REVIEWED; дата: —; замечания: —; финальный русский текст: —; approved reviewedTranslationSha256: null.

### 07. `TR-Q-10`

- Поле: `editorialTranslationReview.items`; источник: `A32723`; роль: `VEEL_ADAMS_EDITORIAL`; страница: not specified.
- English SHA-256: `9fc7225ac6093e457ab9cc6dbe8d13f9bcd143f482f8891d0331fffa34ca7da6`; русский SHA-256: `f33be02203f2db973410e900e67f2ef1169b0edc1424694f52b6afa060e91aa3`.
- Canonical row SHA-256: `e22265376e553be05b1d8045da860029e23e80b7505aefadb83da2a90c9c00ec`; independentReview.state = NOT_PERFORMED.

**Английский оригинал (без правок):**

> In the Doctrinal Part of several of his Discourses thou wilt find the depth of Polemical Divinity, and in his Inferences from thence the sweetness of Practical; some things which may exercise the profoundest Scholar, and others which may instruct and edifie the weakest Christian; nothing is more nervous than his Reasonings, and nothing more affecting than his Applications.

**Русский рабочий черновик (без правок):**

> В доктринальной части ряда его рассуждений ты найдёшь глубину полемического богословия, а в вытекающих из неё выводах — сладость практического; одно даст труд самому глубокому учёному, другое наставит и назидает самого немощного христианина; ничто не обладает большей силой, чем его рассуждения, и ничто не трогает сердце сильнее, чем его применения к жизни.

**Рецензент:** NOT_REVIEWED; дата: —; замечания: —; финальный русский текст: —; approved reviewedTranslationSha256: null.

### 08. `TR-Q-06`

- Поле: `authorialTranslationReview.items`; источник: `A32724`; роль: `CHARNOCK_BODY`; страница: 20.
- English SHA-256: `4a440d429b42963e6f19e3b1d2e490fa49dab84f2bef8576af03ffce89b0526a`; русский SHA-256: `0efac5e590105f210909a9701e590ee0a38fedef246a48042c6b014db8f4fbce`.
- Canonical row SHA-256: `879ce508fc97523635f161c0f85790d14858555b63f2fc98e070911ad7d836cb`; independentReview.state = NOT_PERFORMED.

**Английский оригинал (без правок):**

> THE Author of this Psalm, and the time when it was penn'd, are uncertain. Some think it was compos'd after the return of the Jews from Babylon, upon the Erection of the second Temple, and designed to be sung in their constant Publick Assemblies. Others think it was compos'd by David, when he brought the Ark to Sion, as the Repository for it, till the Building of the Temple, wherein it might honourably rest. It seems, whoever was the Author, to be Ecstatical. The Penman breaks out into a holy rapture and admiration of the firmness and stability of the Church. 'Tis also Prophetical of the Christian Church, of the glory of it, the largeness of its bounds, and perpetual duration.

**Русский рабочий черновик (без правок):**

> Автор этого псалма и время его написания неизвестны. Некоторые полагают, что он был составлен после возвращения иудеев из Вавилона, при возведении второго храма, и предназначался для пения на их регулярных общественных собраниях. Другие полагают, что его составил Давид, когда перенёс ковчег на Сион, где он должен был храниться до сооружения храма, в котором мог бы почивать с честью. Кто бы ни был автором, псалом, по-видимому, исполнен восторга. Его составитель разражается святым восхищением и изумлением перед прочностью и устойчивостью Церкви. Он также пророчествует о христианской Церкви, о её славе, об обширности её пределов и о её непреходящем существовании.

**Рецензент:** NOT_REVIEWED; дата: —; замечания: —; финальный русский текст: —; approved reviewedTranslationSha256: null.

### 09. `TR-Q-07`

- Поле: `authorialTranslationReview.items`; источник: `A32723`; роль: `CHARNOCK_BODY`; страница: 222.
- English SHA-256: `5b46e50e0579a5042503b30e7167812c77fbe9b9d4bf094a6d3fcee3cdd58805`; русский SHA-256: `cecf3c9e3006c757975feee59b726c7e5370958273cee3de6c9ec02242e1e38d`.
- Canonical row SHA-256: `b41da91e534e0ec3c412a57b48ff1595fecb91400a86116bff9e3730ddb14760`; independentReview.state = NOT_PERFORMED.

**Английский оригинал (без правок):**

> First, There was no change in God when he began to create the World in Time. The Creation was a real change, But the change was not subjectively in God, but in the Creature; the Creature began to be what it was not before. Creation is considered as active or passive; active Creation is the Will and Power of God to create; this is from Eternity, because God willed from Eternity to create in Time; This never had beginning, for God never began in time to understand any thing, to will any thing, or to be able to do any thing; but he alway understood, and alway willed those things which he determined from Eternity to produce in Time. The Decree of God may be taken for the Act decreeing, that is eternal and the same; or for the Object decreed, that is in Time: So that there may be a change in the Object, but not in the Will whereby the Object doth exsist.

**Русский рабочий черновик (без правок):**

> Во-первых, в Боге не произошло изменения, когда Он начал творить мир во времени. Сотворение было реальным изменением, но носителем изменения был не Бог, а творение; творение начало быть тем, чем прежде не было. Творение рассматривается как активное или пассивное; активное творение — это воля и сила Бога творить; оно от вечности, поскольку Бог от вечности восхотел сотворить во времени. Это никогда не имело начала: ведь Бог никогда не начинал во времени что-либо понимать, чего-либо желать или быть способным что-либо совершить; Он всегда понимал и всегда желал того, что от вечности определил произвести во времени. Божье определение можно понимать как акт определения — он вечен и остаётся тем же, — или как определённый предмет — он существует во времени. Поэтому изменение может быть в предмете, но не в воле, благодаря которой этот предмет существует.

**Рецензент:** NOT_REVIEWED; дата: —; замечания: —; финальный русский текст: —; approved reviewedTranslationSha256: null.

### 10. `TR-Q-08`

- Поле: `atheismReview.translation`; источник: `A32723 через atheismReview.byteVerifiedContext`; роль: `CHARNOCK_BODY`; страница: 47 из родительской карточки.
- English SHA-256: `0cbe2ee6fadf32f00e9e9ac803f5f5d99a606040c0609deff96180e45a784ea7`; русский SHA-256: `d809acc20a34942b963cf7515acf78613b03d54f9d06d0ed11ec830683e00b49`.
- Canonical row SHA-256: `4314618dcfb6adc7cba1d4fb10dd4bda902f99ae3bcedd798b202fd2bc9c6112`; independentReview.state = NOT_PERFORMED.

**Английский оригинал (без правок):**

> Men may have Atheistical hearts without Atheistical heads. Their reasons may defend the Notion of a Deity, while their hearts are empty of affection to the Deity: Jobs Children may curse God in their hearts, tho not with their lips.

**Русский рабочий черновик (без правок):**

> Сердца людей могут быть безбожными, даже если их головы не безбожны. Их рассудок может отстаивать представление о Божестве, тогда как в их сердцах нет любви к Божеству: дети Иова могут проклинать Бога в сердцах, хотя и не устами.

**Рецензент:** NOT_REVIEWED; дата: —; замечания: —; финальный русский текст: —; approved reviewedTranslationSha256: null.

### 11. `TR-Q-12`

- Поле: `enmityReview.translations`; источник: `B20167`; роль: `CHARNOCK_BODY`; страница: not specified.
- English SHA-256: `224b3646de8d8e37421592a5fd489a6373ff3edb442e0602f197a61c9df85d4f`; русский SHA-256: `ccf6f6ca06125ae9cf77f21a221e9c43a6f9de48237b96e9ec49c5708883025f`.
- Canonical row SHA-256: `07a12705776027a375b043e4a61fab491ca0d5eeb642e950d4310087dd23cb40`; independentReview.state = NOT_PERFORMED.

**Английский оригинал (без правок):**

> In our Creation there was an union to God; in our Corruption a separation from Him, whence ariseth an opposition to him; so that it is not created, but corrupted Nature which is here meant.

**Русский рабочий черновик (без правок):**

> При нашем сотворении было единение с Богом; при нашем повреждении — отделение от Него, из которого возникает противостояние Ему; так что здесь имеется в виду не сотворённая, а повреждённая природа.

**Рецензент:** NOT_REVIEWED; дата: —; замечания: —; финальный русский текст: —; approved reviewedTranslationSha256: null.

### 12. `TR-Q-16`

- Поле: `enmityReview.translations`; источник: `B20167`; роль: `VEEL_EDITORIAL`; страница: not specified.
- English SHA-256: `7ba06fb7abc1a54a20ff5bbd09bf6e7a8bed0c7be674155376aeeccaa4151c32`; русский SHA-256: `aee11a44d2a22a2f7451efc5e4ee448c41d89889490af84aa93715161b698b3b`.
- Canonical row SHA-256: `2751ebf1f730508f5a0c978ba96373f589443cdc338c67b79a591a8a33a5f74b`; independentReview.state = NOT_PERFORMED.

**Английский оригинал (без правок):**

> As for the other Discourse, Of Man's Enmity against God, we cannot find when or where it was preached. I have been credibly informed, that the Author had a design (had it pleased God to have prolonged his days) to have preached largely about Original Sin, and then it is not unlikely that he might intend this present Treatise as one branch of it.

**Русский рабочий черновик (без правок):**

> Что касается другого рассуждения, «О вражде человека против Бога», мы не можем установить, когда и где оно было произнесено. Я получил заслуживающее доверия сообщение, что автор намеревался (если бы Богу было угодно продлить его дни) подробно проповедовать о первородном грехе; и тогда вполне возможно, что он мог предназначать настоящий трактат как одну из частей этого замысла.

**Рецензент:** NOT_REVIEWED; дата: —; замечания: —; финальный русский текст: —; approved reviewedTranslationSha256: null.

## Порядок внешнего решения

После получения двенадцати **реальных** заключений приложить отдельные signed review receipts, проверить reviewer independence, подготовить утверждённые русские строки и their exact SHA-256, затем отдельным PR согласовать protected JSON и разрешения. До этого ED-06 / RIGHTS_HOLD / PUBLICATION_HOLD остаются открыты.

Факсимиле сторонних цифровых библиотек **не включены** в пакет; ссылки на официальные записи допустимы, а повторное размещение изображений требует отдельного разрешения.


---

## Дополнение 21.11.2026 — точная граница свободного использования TCP-текста и факсимиле

**Проверено по прямой политике правообладателя транскрипции / `RESEARCH_ONLY` / `TCP_TEXT_REUSE_POLICY_VERIFIED` / `FACSIMILES_SEPARATE` / `NO_PUBLICATION_APPROVAL`.** Это **узкая проверка условий текстового источника**, не изменение machine `rightsState`, не утверждение русского перевода и не общая правовая экспертиза книги.

Официальный FAQ [Text Creation Partnership (University of Michigan), §§10–12](https://www.textpartnership.net/pages/faq.html) устанавливает:

1. EEBO-TCP Phase I стал общедоступным **01.01.2015**, Phase II — **01.08.2020**; весь TCP-текстовый корпус доступен для свободного повторного использования.
2. В ответе на вопрос **«Are there any restrictions on my use of the TCP texts?»** проект прямо **не устанавливает ограничений** на использование собственных транскрипций: допускает переводить, редактировать, перерабатывать и переиздавать их, без обязательной атрибуции; TCP считает сам текст общественным достоянием и отказывается от возможной защиты собственных решений по набору и разметке. Указание TCP и точного ID источника **рекомендуется** как научная практика.
3. **Иное правило у изображений страниц:** TCP специально сообщает, что **не имел права распространять** предоставленные ProQuest/Gale/Readex сканы. Свободные условия TCP-текста **не дают** права на фотокопию, растровую страницу, коммерческий EEBO-факсимиле или чужую редакторскую публикацию.

**Применение к этим 12 карточкам:** `A32723`, `A32724`, `A32726`, `B20167` — ссылки на текстовые свидетели EEBO-TCP; для использования **самой TCP-транскрипции** политика источника не создаёт дополнительного разрешительного барьера. Но конкретные строки по-прежнему требуют сверки локатора, авторского/редакторского голоса и **независимой рецензии русского перевода (0/12)**; `reviewedTranslationSha256` не проставлен. Это не подтверждение цепочки прав на новый русский перевод, изображения издания или весь смешанный книжный корпус.

**Раздельный библиотечный маршрут:** [The Huntington, Library Rights and Permissions](https://www.huntington.org/library/library-rights-and-permissions) указывает, что не требует разрешения на публикацию материала, уже находящегося в общественном достоянии, но одновременно оставляет заявителю ответственность за проверку прав и ограничивает условия некоторых предоставляемых фотокопий частным исследованием. Не интерпретировать это как автоматическую лицензию на ещё не полученные изображения `Works II 1684/1699`.

**Точный результат:** `TCP_TEXT_REUSE_POLICY_CHECK = VERIFIED_NO_TCP_RESTRICTIONS`; `FACSIMILE_REPRODUCTION = NOT_CLEARED_BY_TCP_POLICY`; `INDEPENDENT_TRANSLATION_REVIEW = 0/12`; `ED-02 / ED-06 / ED-08 / RIGHTS_HOLD / PUBLICATION_HOLD = UNCHANGED`. Не создавать новую карточку SSOT и не переписывать исторические custody-квитанции на основании этой правовой справки.

---

## 21.11.2026 — обращения к независимым рецензентам направлены; письменных решений 0/12

**ED-06 / EXTERNAL_REVIEW_REQUEST_SENT / REVIEWER_NOT_APPOINTED / INDEPENDENT_REVIEW 0/12 / NO_APPROVAL.** Отправлены два независимых запроса:

- [Global Theological Ministries](https://gtmnow.org/contact/) — организация включает русский язык в программу перевода баптистских богословских материалов; запрошено направление к специалисту по русско-английской богословской колляции.
- [Read the Puritans](https://readthepuritans.org/translation-process) — проект описывает раздельную языковую и богословскую вычитку пуританских переводов; запрошен контакт опытного двуязычного рецензента.

В сообщениях ограничен объект проверки: **ровно 12 английско-русских пар**, наличие трёх уже отмеченных смысловых вопросов, сверка оригинала/перевода/источников/голоса автора или редактора, возврат письменных обоснованных ACCEPT / REVISE / REJECT по каждому ID. Полная книга и чужие сканы не отправлялись. Оплаты, условий найма или сроков третьих сторон не обещано. Все 12 статусов independentReview остаются NOT_PERFORMED и reviewedTranslationSha256 не заполняется до реальной подписи и проверки внешнего текста.

**Дополнительный вопрос рецензенту, не правка канона:** TR-MERCY, английское *choicest Mercy* и рабочее русское «драгоценнейшей милости». Следует оценить, не сдвинула ли русская эмоциональная характеристика смысл английской превосходной степени (особенная/наилучшая/избранная в данном контексте). Ранее подтверждённые редакционные вопросы TR-Q-06 / TR-Q-07 / TR-Q-10 и запрет приписывания слов Вила/Адамса Чарноку сохраняются.

**Правовая граница:** официальный [EEBO-TCP FAQ §§11–12](https://www.textpartnership.net/pages/faq.html) разрешает повторное использование собственных транскрипций TCP, включая перевод, но не предоставляет прав на сторонние факсимиле; [Huntington Library](https://www.huntington.org/library/library-rights-and-permissions) не требует разрешения для текстов общественного достояния, сохраняя ответственность исследователя за права третьих лиц и специальные условия выдачи копий. Это не заключение о правах на нынешнюю редакторскую компиляцию, современные изображения или всю книгу. RIGHTS_HOLD / PUBLICATION_HOLD сохраняются.
