# V84D — SOURCE LOCATOR AND EVIDENCE-STATUS CLOSURE

**Дата:** 2026-07-29  
**Статус:** source-integrity authority / точечная коррекция V84C  
**Область:** Thomas Goodwin; Timothy Rogers; WHO burn-out wording; site source ledger  
**Production:** этот файл не публикует сайт и не заменяет богословскую архитектуру V84B–V84C

---

## 0. Причина коррекции

Финальный ручной readback V84C и связанной статьи обнаружил две реальные неточности evidence-status:

1. Wesley Center был назван «первичным полным HTML-текстом» Гудвина, хотя сама страница озаглавлена как **Extracts from the Works** и является историческим извлечением;
2. две русские цитаты Тимоти Роджерса были обозначены как верифицированные «по первоисточнику» без опубликованного локатора внутри трактата.

Эти неточности не меняют богословские выводы, но должны быть исправлены, потому что корпус запрещает повышать evidence-status красивой формулировкой.

V84D **supersedes только соответствующие source-status и locator claims V84C**. Все остальные выводы, editorial gates и 38-pass ledger V84C сохраняются.

---

# 1. THOMAS GOODWIN — ИСПРАВЛЕННЫЙ EVIDENCE MAP

## 1.1 Wesley Center

URL:

https://wesley.nnu.edu/john-wesley/a-christian-library/a-christian-library-volume-6/extracts-from-the-works-of-the-rev-thomas-goodwin-dd-part-i/

Правильный статус:

`P1-HISTORICAL-EXTRACT-HTML`

Разрешённое описание:

> Открытое историческое HTML-извлечение из *A Child of Light Walking in Darkness*, пригодное для проверки структуры аргумента и конкретных доступных фрагментов.

Запрещённые описания:

- `первичный полный HTML-текст`;
- `полное издание трактата`;
- `оригинальное издание 1659 года`.

Подтверждённые по доступному извлечению тезисы:

- Ис. 50:10 описывает боящегося Бога и слушающего Раба, который всё же идёт во тьме;
- тьма не сводится у Гудвина к известному сознательному греху или простому невежеству;
- душа может лишиться ощущения Божьего благоволения и ясного свидетельства о благодати, не лишившись самой благодати;
- страх, совесть и обвинение способны заставлять человека спотыкаться об обетования и делать ложные выводы.

## 1.2 Полный трактат в собрании сочинений

Индекс:

https://digitalpuritan.net/thomas-goodwin/

Прямая ссылка:

https://digitalpuritan.net/Digital%20Puritan%20Resources/Goodwin%2C%20Thomas/Works%20%28Vol.3%29%20Ind%20Titles/%5BTG%5D%20A%20Child%20of%20Light%20Walking%20in%20Darkness.pdf

Правильный статус текущего прохода:

`P1-FULL-TREATISE-LINK / PDF-PAGE-IMAGE-HOLD`

Что установлено:

- Digital Puritan Press указывает *The Works of Thomas Goodwin*, vol. 3;
- внутри `Certain Select Cases Resolved` отдельным полным текстом указан *A Child of Light Walking in Darkness*;
- объём отдельного PDF обозначен как 120 страниц.

Что не заявляется:

- что PDF постранично прочитан в этом проходе;
- что новая дословная цитата проверена по изображению страницы;
- что современный PDF является факсимиле первого издания.

## 1.3 Оригинальное издание

Folger catalog:

https://catalog.folger.edu/record/482667

Статус:

`P2-ORIGINAL-EDITION-METADATA`

Каталог фиксирует издание 1659 года и полный исторический заголовок. Metadata подтверждает существование и библиографию оригинального издания, но не заменяет чтение текста или page-image verification.

---

# 2. TIMOTHY ROGERS — ТОЧНЫЕ ЛОКАТОРЫ ЦИТАТ

## 2.1 Bibliographic / encoded-edition authority

University of Michigan EEBO-TCP:

https://quod.lib.umich.edu/e/eebo2/A57573.0001.001?view=toc

Статус:

`P1-ENCODED-EDITION-TOC / ACCESS-LIMITED`

Подтверждено:

- автор: Timothy Rogers;
- заглавие: *A Discourse Concerning Trouble of Mind and the Disease of Melancholly*;
- издание: London, 1691;
- отдельный раздел: *THE PREFACE: CONTAINING Several Advices to the Relations and Friends of Melancholly People*.

## 2.2 Первая цитата

Русский фрагмент в статье:

> Меланхолия завладевает мозгом и духом и лишает их способности к мысли и действию… Когда этот тяжкий недуг глубоко укоренился, бороться с ним так же тщетно, как бороться с горячкой или плевритом, подагрой или каменной болезнью.

Локатор:

`The Preface: Containing Several Advices to the Relations and Friends of Melancholly People`, **Advice 1 — First**.

Текстовая опора начинается словами:

`Melancholly seizes on the Brain and Spirits, and incapacitates them for Thought or Action...`

и продолжает сравнение бесплодного волевого сопротивления с fever / phthisis / gout / stone.

## 2.3 Вторая цитата

Русский фрагмент в статье:

> Не понуждайте страдающего меланхолией к тому, чего он не может исполнить. Такие люди — как те, у кого переломаны кости, кто в великой боли и муке и оттого неспособен к действию.

Локатор:

`The Preface: Containing Several Advices to the Relations and Friends of Melancholly People`, **Advice 5 — Fifthly**.

Текстовая опора начинается словами:

`Do not urge your Friends under the Disease of Melancholly, to things which they cannot do.`

и далее сравнивает их с людьми, чьи bones are broken, находящимися в pain and anguish и потому неспособными к действию.

## 2.4 Publication rule

Разрешено:

- публиковать русский перевод с указанными локаторами `Preface, Advice 1` и `Preface, Advice 5`;
- ссылаться на EEBO-TCP bibliographic/TOC record;
- ясно говорить, что русский текст является переводом исторических фрагментов, а не современной медицинской формулой.

Запрещено без дополнительного page-image pass:

- указывать номер страницы первого издания;
- утверждать факсимильную пословную сверку;
- переносить гуморальную физиологию Роджерса в современную медицину;
- превращать его описание одного тяжёлого состояния в универсальную этиологию депрессии.

---

# 3. WHO BURN-OUT — СТРОГАЯ ФОРМУЛИРОВКА

Official WHO URL:

https://www.who.int/standards/classifications/frequently-asked-questions/burn-out-an-occupational-phenomenon

Разрешённая читательская формула:

> Выгорание в ICD-11 описано как профессиональный феномен хронического рабочего стресса, а не как медицинское заболевание или название всякого истощения.

Эта формула точнее прежнего сокращения «относится к хроническому рабочему стрессу», потому что сохраняет три границы WHO:

1. occupational context;
2. not classified as a medical condition;
3. not applicable to every area of life.

---

# 4. SITE CORRECTION

Связанный site PR:

`FedorMilovanov/gb-is-my-strength#498`

Предыдущий exact-green head:

`8202c7d8cef261ccf1d72b10a57d669a624c53b4`

Новый content head после source-integrity correction:

`c9554c86edddaa21c6dd3c9b293b486abeecd881`

Изменено только в `TmaNaSerdceBody.astro`:

- `опасность устанавливаются` → `риск оценивается`;
- burn-out приведён к строгой WHO-формуле;
- Rogers получил ссылку и локаторы `Preface, Advice 1 / Advice 5`;
- Goodwin разделён на полный трактат в Works vol. 3 и Wesley historical extract;
- прежняя формула `верифицирована по первоисточнику` заменена на проверяемое описание локаторов.

PageHead, reading time, TOC, CSS, JS, routes и соседние статьи не менялись.

Все зелёные workflows предыдущего SHA считаются историческими и **не переносятся** на новый head. Требуется новый exact-head CI.

---

# 5. FINAL SOURCE-INTEGRITY RULE

> Full text, historical extract, original-edition metadata, encoded TOC, PDF link and page-image verification — разные виды свидетельства. Тезис может быть богословски верным и всё же требовать понижения evidence-status. Исправление статуса не ослабляет аргумент; оно делает его честным и воспроизводимым.

---

# 6. DISPOSITION

- V84B сохраняет theological-order authority.
- V84C сохраняет editorial-completeness authority.
- V84D становится authority для Goodwin/Rogers source status, цитатных локаторов и WHO burn-out wording.
- Новые прямые исторические цитаты по-прежнему требуют локатора; для PDF — page-image verification.
- Production не заявляется до exact-head CI на `c9554c86edddaa21c6dd3c9b293b486abeecd881` или более новом фактическом head.
