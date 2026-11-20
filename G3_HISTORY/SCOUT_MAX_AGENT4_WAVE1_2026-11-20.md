# G3 MAX — Агент №4 (СКАУТ) — Волна 1

**Дата:** 2026-11-20
**Агент:** №4 — независимый исследователь-разведчик, поисковик первоисточников
**Ветка:** `arena/963be9bc-research` (от `4219276` main) — **нет push в `lane/g3-history-source-and-handoff-20261118`**, результаты передаются как пакет
**Статус:** `RESEARCH_DRAFT / PUBLICATION_HOLD` — не является публикационным разрешением, не меняет seal `2026-09-09` и 16/21 `G3_PUB`
**Прочитаны до волны:** `AGENTS.md`, `AGENT_RULES.md`, `CURRENT_AUTHORITY.md` (2026-08-02 root), `data/repository-evidence-policy-v2.json`, `docs/research/SELF_PLAN_PROTOCOL.md`, весь `G3_HISTORY/` (main HEAD), Research PR #582 (HEAD `93d6f08a`), PR #584, PR #574, обзор NEWS/G3, история коммитов `lane/g3-history-source-and-handoff-20261118`
**Коллеги проверены:** Agent №1 (история/конференции) — параллельная ветка `d3d07164`/`582b193` с уже собранным `CONFERENCE_HISTORY.md`; Agent №2 (видео/аудио) — рабочий пакет 20.11.2026 с 0 прослушанных аудио, `CAPTIONS_READ` для HIST-06A/HIST-10/HIST-15; Agent №3 — критика/финансы — закрыт P0 на `CLAIMS_LEDGER` (C001–C068). Повторная инвентаризация не проводилась.

---

## 1. Две выбранные гипотезы волны

По правилу приоритетов P0–P3 и требованию «не более двух активных deliverable»:

### Гипотеза A — P0-критическая: независимая датировка истоков 2011

**Вопрос:** Можно ли подтвердить публикацию `Conference Announcement` 10.08.2011 независимым от подписи `Aug10` элементом, и что доказывает Wayback-маршрут `g3conference.com`?
**Ожидаемый результат:** один проверяемый объект + точный локатор, исправляющий распространённую ошибку «HTTP 200 = текущий оригинал» и «Aug10 = автоматически 10.08.2011».
**Критерий STOP:** после двух адресных проходов без нового объекта — STOP_DISCOVERY с осторожной формулировкой и HOLD.

### Гипотеза B — P1-важная: от анонса к фактически произнесённому докладу

**Вопрос:** Что из программ 2013–2017 действительно подтверждается как произнесённый доклад (GNL-видеоархив) vs анонс, и как отделить региональные события 2024 от национального?
**Ожидаемый результат:** один точный список реально сохранённых записей 2013 + два региональных события 2024 с организаторским первоисточником; уточнённая формулировка для редактора о границах атрибуции.
**Критерий STOP:** после сверки каталога GNL и двух organizer-страниц Tickettailor — переход к чтению/письму.

Общая очередь гипотез (не активны в этой волне): Q003 кризисный борт после 21.07.2026, Q004 транзит директоров 2025, Q006 титульный анализ Dallas Statement, видео-таймкоды Buck, финансовая parcel-связка.

---

## 2. Пакет открытий — компактные доказательные узлы

### DISCOVERY-2026-11-20-A01 — RSS-дата как независимый датирующий элемент для `Conference Announcement`

**DISCOVERY-ID:** `SCOUT-A01` (предлагается как уточнение `G3-S003`; не новый независимый источник)
**Что найдено:** RSS-лента `http://www.g3conference.com/?feed=rss2`, захваченная Wayback `20110927042330` (и повторно `20110927042330id_`), содержит для `?p=1` элемент `<pubDate>Wed, 10 Aug 2011 17:12:27 +0000</pubDate>` c тем же инципитом `I am excited to announce the G3 Conference for January of 2013!` (Pastor Josh Buice) и GUID `http://www.g3conference.com/?feed=rss2&p=1`. Соседний пост `?p=99` (Steve Lawson, 24–26 Jan 2013) датирован `Fri, 23 Sep 2011 16:27:45 +0000`.
**Почему важно:** Исправляет уязвимость HIST-01. Видимая на странице карточка `Aug10` не содержит года; без внешнего элемента нельзя отличить 10.08.2011 от другой даты. RSS — независимый машиночитаемый элемент, фиксирующий, что публичное планирование существовало **не позднее 27.09.2011** (дата захвата) и по заявлению издателя — 10.08.2011. Ответ на вопрос Agent1 №5: какой элемент независимо датирует публикацию 10.08.2011 — именно `<pubDate>` RSS, а не текст `?p=1` или `hello-world`.
**Источник:** `https://web.archive.org/web/20110927042330id_/http://www.g3conference.com/?feed=rss2` (Wayback, `id_` — оригинальные байты без тулбара) + контроль `https://web.archive.org/web/20110927045808/http://www.g3conference.com/?cat=1` (визуальные карточки `Aug10` и `Sep23` с одинаковым инципитом) + `https://web.archive.org/web/20110928165117/http://www.g3conference.com/?p=99` (Lawson). Оригинал `g3min.org/hello-world` проверен 18.11.2026 как **ныне отдающий Lumena** при HTTP 200 — не оригинал.
**Фактически изучено:** `FULL_OBJECT_VERIFIED` для RSS (прочитан полный XML-фрагмент, 2 записи, строки pubDate/GUID), `PARTIAL_OBJECT` для html-страниц `?cat=1`/`?p=99` (карточки и заголовки). `id_` байты сохранены как текстовая выписка, не как бинарный артефакт Git.
**Результат проверки:** **ПОДТВЕРЖДЕНО** — public planning pinned к 2011, с независимой нижней границей 27.09.2011 и заявленной издательской датой 10.08.2011. Не доказывает, что G3 уже называлось `Ministries`; это Conference, не корпорация 2019.
**Новизна:** В `CONFERENCE_HISTORY.md` (main) и `EDITORIAL_HISTORY_EXTENSION_CANDIDATE` (PR #582, HIST-01) дата 2011 опиралась на `g3min.org/hello-world` + поисковый фрагмент. Настоящий захват даёт точный независимый локатор, отсутствовавший в действующем корпусе.
**Кому направлено:** Агент №1 (история/хронология) + владелец PR #582 (owner review 2026-11-18 п. a).
**Ответ независимой проверки:** ожидается (передано A1/Agent1).
**Публикационные ограничения:** `evidenceClass=A2` (официальная публикация организатора), `accessState=FULL_OBJECT_VERIFIED` (RSS) / `PARTIAL_OBJECT` (HTML), `locatorState=EXACT_LOCATOR_VERIFIED` (RSS pubDate line + capture timestamp), `rightsState=PRIVATE_STUDY_ONLY` до отдельной проверки (нет разрешения на републикацию полного текста), `publicationState=PUBLICATION_HOLD` (требует нового signed handoff для G3-HIST-PUB-01). Нельзя цитировать дословно длинный пассаж как русский перевод; только brief attributed paraphrase.

### DISCOVERY-2026-11-20-A02 — GNL-каталог 2013 как разделитель анонса и факта доклада

**DISCOVERY-ID:** `SCOUT-A02` (уточнение HIST-03)
**Что найдено:** На `https://www.gnli.com/titles/2013-G3-Conference-or-G3-Ministries/2908` (HTTP 200, 20.11.2026) сохраняются 9+ записей с точными заголовками, авторами и длительностями: Paul Washer `The Importance of Prayer…` 1:52:40, Donald Whitney `When God Turned His Back…` 1:03:21, Paul Washer `Penal Substitutionary Atonement…` 1:22:40, Voddie Baucham `Getting the Gospel Right` 56:48, Joel Beeke `What Really Is The Gospel?` 56:48, Steven Lawson `The Preaching of John Calvin…` 1:07:01, Tim Challies `Mission in a Changing World` 37:07, Steven Lawson `Why Preach the Intolerant Message…` 51:12, David Miller `Jesus Prays for His Followers` 35:17. Отдельно видны связные каталоги 2014 (11 эпизодов), 2016 (8), 2017 (18), 2019 (17), 2020 (14) — навигация со страницы 2013.
**Почему важно:** Разрешает замечание владельца PR #582 (задача 1): цифра `750 (2013)` из ретроспективы G3 (G3-S156) и позднего Krots (G3-S157) не может выдаваться за подтверждение Challies; повтор на сайте G3 — не вторая верификация. GNL-записи доказывают **факт произнесения** перечисленных докладов, а не полноту состава. Позволяет редактору писать: «среди фактически сохранённых докладов 2013 — …» и не заявлять `каждый анонс = выступил`.
**Источник:** `https://www.gnli.com/titles/2013-G3-Conference-or-G3-Ministries/2908` (страницы 1–2, live) + Wayback `https://web.archive.org/web/20111230095358id_/http://www.g3conference.com/?page_id=2` (тема `The Gospel: Message and Mission` для G3-2013). Для Challies — cross-check `https://missionalevangelists.blogspot.com/2013/01/g3-conference.html` (программа 25.01.2013, Main Session #3) как анонс, не как запись.
**Фактически изучено:** `PARTIAL_OBJECT` — прочитаны заголовки, имена, длительности, превью-изображения; видео/аудио **не прослушаны** (`VIDEO_SEGMENT_VERIFIED` отсутствует). Для цели «есть запись доклада» достаточно каталога; для цитат — требуется прослушивание.
**Результат проверки:** **ЧАСТИЧНО ПОДТВЕРЖДЕНО / УТОЧНЕНО**: 8–9 докладов 2013 имеют видеослед; объявлять весь список спикеров 2013 как выступивших — нельзя. Подтверждает, что Challies действительно был на сцене (совпадает анонс + запись), но не подтверждает число 750.
**Новизна:** В main `CONFERENCE_HISTORY.md` GNL-2013 упомянут как «третьесторонний каталог», без перечисления заголовков/длит. и без разграничения анонс/запись. Настоящая выписка даёт точные локаторы для PUB-02/03.
**Кому направлено:** Агент №1 + Agent №2 (передать видеопакет: GNL IDs 337163–337174 для независимой слуховой проверки по запросу владельца).
**Ответ независимой проверки:** ожидается.
**Публикационные ограничения:** `A2` (переразмещённый конференц-архив), `accessState=PARTIAL_OBJECT`, `locatorState=COARSE_LOCATOR_ONLY` (каталог, не таймкод), `rightsState=PRIVATE_STUDY_ONLY` (GNL-хостинг, не права на републикацию видео), `publicationState=PUBLICATION_HOLD`. Не копировать превью в репо.

### DISCOVERY-2026-11-20-A03 — два региональных события 2024 (не национальная конференция) + транскрипт Buice 18.01.2025

**DISCOVERY-ID:** `SCOUT-A03` (закрывает HIST-17/15/16 и разграничение 2024)
**Что найдено:**
- **TicketTailor organiser 1010697:** `2024 G3 Regional Conference (The Reformation Conference)` — `Thu May 9, 2024 8:00 AM – Sat May 11, 2024 1:30 PM CDT`, **Countryside Bible Church, Southlake, TX 76092** (250 Countryside Ct). Организатор `g3ministries`.
- **TicketTailor 1270768:** `2024 Cessationist Conference` — `Thu Oct 3, 2024 10:00 AM – Sat Oct 5, 2024 12:00 PM EDT`, **First Baptist Church of Mustang, Oklahoma 73064**, пакет `Bookstore` с описанием.
- **Buzzsprout 1939792/episodes/16458733** (The Christian Worldview, 18.01.2025) HTML+PDF: реплика Buice (транскрипт гостя) — `G3 started as a conference. We had a theology conference in 2013 in January … Every seat in our auditorium was filled with a waiting list a month early … until 2017 when we had the 500th anniversary of the Reformation and we did a conference on that subject and we went away from the church campus to a convention center and then it just started to just snowball … So early on it was just a conference, but after about 2020, we shifted from just being a conference … to being a content producing ministry where we have G3 press … as well as the development of the G3 church network … workshops … for worship as well as for expository preaching.` Это полный контекст переезда (≈2017, Reformation 500) и сдвига после ≈2020.
**Почему важно:** Закрывает две ошибки: (1) приписывать 2024 статус национальной конференции (ошибка, отмеченная в PR #582); доказано — два региональных события на чужих площадках; (2) смешивать рассказ Buice с оценкой Challies о причинах переезда. Challies (`you-me-and-g3`, 23.05.2025, A1 participant) подтверждает переход «из кампуса в convention center» и рост «hundreds → upwards of 6,000», но **не датирует** год; Buice датирует как воспоминание 2017 — это требует пометки `participant recollection`, не договор аренды.
**Источник:** `https://www.tickettailor.com/events/g3ministries/1010697` + `https://www.tickettailor.com/events/g3ministries/1270768` (live organiser pages, 20.11.2026) + `https://www.buzzsprout.com/1939792/episodes/16458733-why-jimmy-carter-s-faith-is-lauded-while-the-faith-of-others-is-loathed` (ep 3, 18.01.2025, host David Wheaton, guest Josh Buice, 53:59, Show Notes + Transcript) + PDF `https://thechristianworldview.org/wp-content/uploads/2025/01/2025-0118-Why-Jimmy-Carters-Faith-is-Lauded-While-the-Faith-of-Others-is-Loathed.pdf` (тот же выпуск, полный текст) + `https://www.challies.com/articles/you-me-and-g3/` (23.05.2025, стр. `Though I enjoyed…/Sure enough…`).
**Фактически изучено:** TicketTailor — `FULL_OBJECT_VERIFIED` (даты/площадки/организатор прочитаны); Buzzsprout — `TRANSCRIPT_READ` (`CAPTIONS_READ`) + PDF `READ_EXCERPTS` для Buice-реплики; **аудио не прослушано** (`AUDIO_SEGMENT_VERIFIED` отсутствует, timecode не измерен). Challies — `FULL_OBJECT_VERIFIED` (статья прочитана полностью, 2 чанка).
**Результат проверки:** **ПОДТВЕРЖДЕНО** для организаторских страниц 2024; **ПОДТВЕРЖДЕНО как свидетельство участника** для Buice 2017/2020-центра (не как независимый аудит). Для цитат требуется аудио-верификация с таймкодом.
**Новизна:** В `EDITORIAL_HISTORY_EXTENSION_CANDIDATE` (PR #582, 18.11.2026) Tickettailor-ссылки уже названы (HIST-?), но без выписки дат/площадок и без разграничения `regional vs national`; Buice-интервью уже в HIST-15/16, но без границы реплики и оговорки `after about 2020`. Настоящая выписка даёт точные локаторы.
**Кому направлено:** Агент №1 (история) — для G3-HIST-PUB-09; Агент №2 (медиа) — для `AUDIO_SEGMENT_VERIFIED` (п. a–c из owner review 18.11.2026 и запрос Agent1 №2 от 20.11.2026).
**Ответ независимой проверки:** ожидается от обоих.
**Публикационные ограничения:** `A3` (organiser page) / `A1` (participant statement Buice) / `A1 participant` Challies; `accessState=FULL_OBJECT_VERIFIED` (TicketTailor, Challies), `PARTIAL_OBJECT` (Buzzsprout transcript); `locatorState=EXACT_LOCATOR_VERIFIED` (TicketTailor даты/адреса), `COARSE_LOCATOR_ONLY` (Buice — без таймкода); `rightsState=PRIVATE_STUDY_ONLY` (транскрипт издателя, не свободная цитата); `publicationState=PUBLICATION_HOLD`. До handoff нельзя выпускать «2024 — не нац. конференция» как `PROMOTE`; только draft.

---

## 3. Отчёт по волне — что изменилось

### Три наиболее ценные находки (только реально полученное)

1. **RSS-pubDate 10 Aug 2011** — первый независимый датирующий элемент для `Conference Announcement` (нижняя граница 27.09.2011, заявка 10.08.2011). Меняет датировку из `HIST-01` из категории `SEARCH-CACHE` в проверяемую.
2. **GNL-2013 заголовки/длит. 9 докладов** — позволяет редактору PR #582 выполнить поручение «сверить 750/5600» и написать точную формулировку: ретроспектива G3 + Crotts ≠ подтверждение Challies; каталог ≠ число.
3. **Два Tickettailor-события 09–11 May и 03–05 Oct 2024** + полная Buice-реплика о 2017 Reformation 500 и `after about 2020` — закрывает пробел 2024 и границу атрибуции Challies/Buice.

### Одна главная исследовательская неожиданность / исправленная ошибка

**«HTTP 200 = оригинал» ложно, и «Aug10» без года — не дата.** На 18.11.2026 `g3min.org/hello-world` и `archives/?conf=2013` отдают Lumena Ministries при HTTP 200, а карточка `Aug10` на `g3conference.com/?cat=1` не содержит года. Без RSS `<pubDate>` утверждение «опубликовано 10.08.2011» остаётся недоказанным. Это не меняет смысл истории (2011 — всё равно до 2013/2019), но требует осторожной формулировки: `public planning NLT Sep 2011 (publisher states Aug 10, 2011)` и HOLD до архивного оригинала.

### Какие документы прочитаны и какие записи прослушаны

**Прочитано (FULL/PARTIAL):**
- Wayback `20110927042330id_/…?feed=rss2` — полный XML (2 поста, pubDates 10.08.2011 + 23.09.2011) — `FULL_OBJECT_VERIFIED`
- Wayback `20110927045808/…?cat=1`, `20110928165117/…?p=99`, `20111129140003/…/`, `20111230095358id_/…?page_id=2` — карточки/темы/даты — `PARTIAL_OBJECT`
- GNL `2013/2908` (стр. 1–2) + навигация на 2014/2016/2017/2019/2020 — заголовки/длит. — `PARTIAL_OBJECT`
- Challies `you-me-and-g3` (2 чанка) — `FULL_OBJECT_VERIFIED`
- Buzzsprout 16458733 (Show Notes + Transcript) + PDF христианского мировоззрения 18.01.2025 — Buice-реплика — `TRANSCRIPT_READ` / `READ_EXCERPTS`
- Tickettailor 1010697 + 1270768 — `FULL_OBJECT_VERIFIED`
- Statement site `20180907001508` (Introduction + I–V) — `PARTIAL_OBJECT` (сверка статуса, не полный текст Dallas Statement — см. HIST-08/19)

**Прослушано:**
- **0 аудио, 0 видео** — честно: `AUDIO_SEGMENT_VERIFIED` и `VIDEO_SEGMENT_VERIFIED` отсутствуют. Все временные метки ниже — издательские, не измеренные на слух. Это соответствует правилу «никогда не заявляй, что просмотрел, если прочитал только описание/субтитры».

### Какие точные материалы переданы другим агентам

- **Агенту №1 (история/хронология):** A01+RSS pubDate + вопрос №5 (какой элемент датирует 10.08.2011); A02 GNL-2013 список + предупреждение о 750/5600 не-независимости; A03 Tickettailor-2024 локаторы для PUB-09. Ссылка на `d3d071646/CONFERENCE_HISTORY.md` как контроль.
- **Агенту №2 (видео/аудио):** GNL IDs 337163–337174 (2013) для `WATCH_QUEUE`; Buzzsprout 16458733 PDF/HTML для `AUDIO_SEGMENT_VERIFIED` задачи a–c (вопрос Wheaton `what…impact of G3`, ответ Buice `Every seat…waiting list a month early`, граница `until 2017 … Reformation … convention center`, оговорка `after about 2020 … content producing ministry`). Прошу вернуть edition/URL, прослушанный диапазон, говорящего, начало/конец реплики или `AUDIO_HOLD`.
- **Агенту №3 (критика/финансы):** нет нового — Q005/Q006 сверка Lumena ждёт отдельного пакета (см. след. направление).

### Какие замечания от коллег получены

В этой волне — нет (первая волна на новой ветке). Использованы опубликованные owner reviews 18–20.11.2026 (в т.ч. `g3-max-research-lane-historical-20261121` с двумя результатами до STOP) и перекрёстные письма Agents 1–3 в PR #582 как входные условия. Возражения ожидаются как отдельные `issuecomment` от соответствующих агентов; обе версии сохраняются в конфликтном реестре до разрешения.

### Как изменились исторический корпус и будущий читательский текст

- **Не изменён canonical:** `G3_HISTORY/CLAIMS_LEDGER.md`, `TIMELINE.md`, `SOURCE_LEDGER.md` (G3-S003) оставлены без переписывания; любые изменения — только через владельца корпуса (owner) и новый signed handoff.
- **Предложено дляDraft:** осторожная формулировка для G3-HIST-PUB-01: *«Публичное планирование G3 конференции документировано не позднее 27 сентября 2011 (Wayback RSS, издатель датирует 10 Aug 2011); первая конференция — январь 2013 при Pray’s Mill Baptist Church, по участнику и региональным каталогам; корпорация — 06.06.2019.»* — с HOLD до архивного оригинала `?p=1`.
- **Предложено дляDraft:** PUB-02/03: *«Среди фактически сохранённых докладов G3 2013 — …(список 9 заголовков GNL)…; это подтверждает факт выступлений названных проповедников, но не полноту программы и не число 750.»*
- **Предложено дляDraft:** PUB-09: *«В 2024 национальная конференция не проводилась; организатор `g3ministries` на tickettailor проводил региональные события 9–11 May в Southlake, TX и 3–5 Oct в Mustang, OK.»* — с HOLD до handoff.

### Следующее самостоятельно выбранное приоритетное направление

По самостоятельности (P0 > P1 > P2):

1. **P0-следующее (если владелец одобрит):** довести Dallas Statement 2018 (HIST-19) до `A1/FULL_HTML_READ/SECTION_VERIFIED` без смешения с конференцией: сверить `History and Formation` ¶¶1–3 (14 участников, Herb’s House Dallas 19.06.2018, роль Buice/O’Fallon/Johnson, черновик Ascol) vs заголовки `Initial Signers/Signers` как не-протокол; вернуть точную формулировку, что *не доказано* (состав именно 19.06, правило для докладчиков).
2. **P1-следующее:** закрыть 2023 `The Sovereignty of God` (HIST-13) vs политико-богословский трек: pin оригинальной программы/статьи с `13 main + 15 breakout` и проверить, что трек христианского национализма — часть, а не тема.

Обе задачи — по одному конкретному объекту, с критерием STOP после двух адресных проходов.

---

## 4. Безопасность и границы

- Ни один `EVIDENCE_HOLD` / `LOCATOR_HOLD` / `ARCHIVE_HOLD` / `RIGHTS_HOLD` / `PUBLICATION_HOLD` не снят автоматически.
- DRM/запреты судебных баз/ограничения архивов не обходились.
- Конфиденциальные документы, частные данные, личные контакты не публикуются.
- Чужие рабочие ветки (`lane/g3-history-source-and-handoff-20261118`, `arena/2fec0e*` и др.) не редактировались.
- Новый канонический реестр не создавался; Product NEWS/G3 не менялся; публичные материалы не выпускались.
- Research-подтверждение ≠ разрешение на публикацию.

---

## 5. Приложение — точные локаторы (для независимой проверки)

| Объект | Локатор | Датировка |
|---|---|---|
| Wayback RSS | `https://web.archive.org/web/20110927042330id_/http://www.g3conference.com/?feed=rss2` — строки `<pubDate>Wed, 10 Aug 2011 17:12:27 +0000</pubDate>` для `?p=1`, `<pubDate>Fri, 23 Sep 2011 16:27:45 +0000</pubDate>` для `?p=99` | захват 27.09.2011 04:23:30 UTC |
| Карточки | `https://web.archive.org/web/20110927045808/http://www.g3conference.com/?cat=1` — `Aug10[0]` Conference Announcement `?p=1` + `Sep23[0]` Steve Lawson `?p=99` | захват 27.09.2011 04:58:08 UTC |
| Тема 2013 | `https://web.archive.org/web/20111230095358id_/http://www.g3conference.com/?page_id=2` — `The Gospel: Message and Mission` | захват 30.12.2011 |
| GNL 2013 | `https://www.gnli.com/titles/2013-G3-Conference-or-G3-Ministries/2908` — 9 видео-тайтлов с длит. (см. A02) | live 20.11.2026 |
| Challies | `https://www.challies.com/articles/you-me-and-g3/` — `Though I enjoyed…/Sure enough…` абзацы + сноска 1 `It is difficult to fact-check…` | 23.05.2025 |
| Buice interview | `https://www.buzzsprout.com/1939792/episodes/16458733-why-jimmy-carter-s-faith-is-lauded-while-the-faith-of-others-is-loathed` + PDF `https://thechristianworldview.org/wp-content/uploads/2025/01/2025-0118-Why-Jimmy-Carters-Faith-is-Lauded-While-the-Faith-of-Others-is-Loathed.pdf` — guest Josh Buice, host David Wheaton | 18.01.2025 08:00 CT, 53:59 |
| Regional 2024 | `https://www.tickettailor.com/events/g3ministries/1010697` — May 9–11, Countryside Bible Church, Southlake TX; `https://www.tickettailor.com/events/g3ministries/1270768` — Oct 3–5, First Baptist Mustang OK | live 20.11.2026 |
| Dallas (контроль) | `https://web.archive.org/web/20180907001508/https://statementonsocialjustice.com/` — Introduction + Scripture–Sin секции | захват 07.09.2018 00:15 UTC |

---

*Подпись волны:* Agent №4, G3 MAX SCOUT — независимая проверка, широкая свобода поиска, проверяемое доказательство.
