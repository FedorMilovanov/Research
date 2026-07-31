# NEXT ACTIONS — РУССКИЕ БАПТИСТЫ

Приоритеты перечислены по ценности закрытия физического архива. Перед каждой операцией перечитать живой Dashboard и последние строки агентских реестров: параллельные агенты могут обновить статус.

## P0 — физические файлы

### 1. «Баптист» 1909 №20

- После загрузки год становится 24/24.
- Два независимых маршрута уже зафиксированы: Wikimedia Commons и читальный зал Московской центральной церкви ЕХБ.
- Не создавать новый объект, если файл появился у другого агента: сначала проверить Drive и `12 Drive Acquisitions`.
- После получения: проверить DJVU/PDF, страницы, SHA-256, загрузить в каноническую папку и обновить `01`, `02`, `03`, `04`, `11`, `12`.

### 2. «Братский вестник» 1945 №1 и №3

- №2 уже локален.
- Прямые официальные PDF подтверждены как 44 и 52 страницы.
- Текущий шлюз не передавал байты; статус не повышать до `IN DRIVE` без фактической загрузки.

### 3. «Утренняя звезда» 1910 №36

Доказательная цепочка:

- дата выпуска: 3 сентября 1910;
- исходное имя: `Утреняя_Звезда_от_3_сентября_1910_года.pdf`;
- размер: 24,5 МБ;
- Telegram message ID: `2600`;
- канал: `@sinichkinas`;
- экспорт подтвердил вложение, но не сохранил байты из-за лимита.

Нельзя подставлять PDF-ID по числовому шаблону.

## P0 — «Слово истины» 1918

Получить пять отсутствующих физических объектов:

- №1;
- №2;
- №3–4;
- №5–6;
- №7–8.

РГБ: основной запрос по шифрам `148/81`, `XVIII 6/178*` остаётся частично не отвеченным.  
РНБ: шифр `6/245`, заказ только через онлайн-магазин; до оплаты получить quote и состав.  
БАН и другие заявки уже отражены в `13 Institutional Requests`.

## P1 — «Братский листок» 1906–1910

### Контроль ряда

- 60 номинальных позиций;
- 22 локальных;
- 38 нелокальных;
- 15 утраченных вложений;
- 23 позиции без известного бинарного следа;
- extraction queue: P1=13, P2=20, P3=5.

### Telegram re-export — 15 oversized PDFs

Сырые `messages4.html` и `messages5.html` проверены по всем 15 точным Message ID. Они содержат метаданные, но **0 attachment href**, **0 скрытых media-атрибутов**, не содержат пути `files/...` или Telegram file ID/access hash. Повторный поиск скрытых ссылок внутри этих экспортов закрыт.

Надёжное действие:

1. Telegram Desktop → Settings → Advanced → Export Telegram data.
2. Выбрать нужный канал/чат, включить **Files**.
3. Поставить максимальный размер выше 12,4 MB; безопаснее 20–50 MB.
4. Сохранить экспорт вместе с каталогом `files/`.
5. Либо получить повторную пересылку оригиналов владельцем канала.
6. Либо извлечь приложения из проверенных parent PDF «Христианина».
7. После получения: исходное имя, Message ID, байты, SHA-256, страницы, первая и последняя страница, дефекты и сравнение с parent extraction.

Машинный список: [`bratsky_listok_telegram_missing_15_recovery_2026-07-31.csv`](bratsky_listok_telegram_missing_15_recovery_2026-07-31.csv).  
Рабочая инструкция: [`TELEGRAM_REEXPORT_BRATSKY_LISTOK_15_INSTRUCTION_2026-07-31.md`](TELEGRAM_REEXPORT_BRATSKY_LISTOK_15_INSTRUCTION_2026-07-31.md).

### Метод извлечения

1. Получить родительский PDF «Христианина».
2. Найти начало и конец приложения по печатному заголовку, колофону и пагинации.
3. Извлечь только полное приложение, сохраняя обложки и пустые страницы.
4. Визуально проверить первую/последнюю страницу.
5. Записать связь с parent PDF, страницы контейнера и SHA-256 извлечённого файла.
6. Не считать parent availability закрытием пробела до завершения пунктов 2–5.

### Ближайшие контейнеры

- 1906 №5: parent 86 страниц / 37,24 МБ; приложение не извлечено; точечный запрос БАН `NOT SENT`.
- 1906 №10: parent 47 страниц / 21 729 915 байт; SHA-1 `2108ab5c80b26a64fae96d97fb6e8a0a9d9e5908`.
- 1906 №12: parent 39 страниц / 17 876 397 байт; checksum pending.
- P1-контейнеров всего 13; все найдены, ни одно приложение не повышать до `LOCAL` без извлечения.

### Единый запрос БАН по восьми белым пятнам

Один объединённый запрос зарегистрирован в MASTER как `READY TO REQUEST — NOT SENT` для: 1907 №4; 1908 №6/№9; 1909 №5; 1910 №1/№3/№4/№5. БАН-реквизиты: `1197`, `1198`, `36/18985*`. Сначала получить подтверждение фактического наличия, номера/года на первой странице, пагинацию, состояние, последнюю страницу/колофон и предварительный расчёт. Полное копирование — только после отдельного согласования. Не объединять с запросом 1906 №5.

### Исправление 1906

Файл с источниковым названием «май 1906» печатно является приложением №6. Отсутствующий слот — №5. Не возвращать старую нумерацию.

## P1 — «Манна» 1918

Получить только титульный лист, выходные данные и колофон сначала. Это должно разрешить конфликт:

- Москва / «Слово истины» по ответу РГБ;
- Петроград / журнал «Гость» по родительской MARC-записи НЭБ.

Шифры РГБ: `V 239/277`, `V 239/276`. Полный скан заказывать после quote и согласования.

## P1 — «Гость»

- 70 источников интегрированы.
- 57 утраченных вложений, 0 точных дублей имён.
- 15 заявок подготовлены, не отправлены.
- Перед интеграцией новых строк перечитывать конец Source Register.
- Число 247 трактовать как месячные позиции, не как физические файлы.
- Получить страницы 156–175 и 261 монографии Kłaczkow через Śląska Biblioteka Cyfrowa; заявка `NOT SENT`.
- Приоритетные институции: Biblioteka Narodowa, WBST, KChB, William Fetler Museum/Latvian Biblical Centre, LNB, SBHLA.

## P2 — «Революция и церковь»

- 1919 №2: DJVU 48 страниц, 1,83 МБ; без известного дефекта.
- 1919 №6–8: DJVU 128 страниц, 5,91 МБ; отсутствует исходная с.40, продублирована с.46.
- Для №6–8 нужен второй скан или институциональная копия; дефектный DJVU всё равно сохранить как provenance object, но маркировать `DEFECTIVE`.

## Параллельная работа агентов

- Разные журнальные lanes могут работать одновременно.
- Перед записью общих README/status/grouped-файлов перечитывать свежий `main`.
- Использовать уникальные маркеры и idempotent append/upsert.
- При отклонённом push перечитать `origin/main`, повторно применить дельту и не заменять общий файл устаревшей полной копией.
- В Google Sheets писать в отдельные строки/ID; одну и ту же ячейку не обновлять параллельно без свежего readback.

## Обязательная фиксация загрузки

Для каждого файла:

- серия, год, номер/дата;
- каноническое имя;
- source page и direct binary URL;
- Drive ID и webViewLink;
- целевая папка;
- MIME;
- байты;
- страницы;
- SHA-256;
- дата получения;
- качество/дефекты;
- raw/canonical relationship;
- изменения в MASTER и GitHub.

## Запреты

- Не отправлять повторные заявки.
- Не начинать платные работы без согласования.
- Не удалять raw export.
- Не склеивать разные издания/тиражи одного номера.
- Не дробить сдвоенный выпуск.
- Не создавать PDF из web-скриншотов вместо исходного файла.
- Не считать viewer, каталог, Telegram metadata или фрагмент полным факсимиле.

## v130 — international archive and 1917–1926 file queue

Check the live Drive MASTER, `12 Drive Acquisitions`, `13 Institutional Requests` and current `main` before every action.

### P0 — file/page closure
1. Obtain the five early physical units of `Слово истины` 1918: no. 1; no. 2; no. 3–4; no. 5–6; no. 7–8.
2. Obtain title page, verso and colophon of the 31-page 1921 congress proceedings; preserve 1921/1922 imprint conflict until then.
3. Obtain the complete 81-page 1925 Plenum record; do not treat AR 881 extract as full closure.
4. Acquire `SBC Annual 1922` and visually check p. 91, item/paragraph 124 plus the complete FMB section.
5. Acquire Hoyt Porter, `Baptist World Movement`, pp. 275–282; hash and visually inspect all eight pages.
6. Acquire the complete Third Baptist World Congress proceedings and inspect Russian delegates, peace and relief contexts.
7. Inspect `Home and Foreign Fields`, April 1925, alleged pp. 9–11, before accepting or rejecting the `Слово истины` 1925 attribution.

### P1 — exact archive inventories
1. `AR 341` item inventory.
2. `AR 242` item inventory.
3. `AR 551-2`, box 045, three Porter folders.
4. `MF 7853` frames/items for Porter, Neprash, relief, union agreements and Fetler.
5. ABHS/International Ministries person-date-topic inventory for Lewis, Rushbrooke, Pavlov, Timoshenko, Neprash, Gill, Porter, Fetler, Russian Missionary Society and College Fund.
6. RUEBU historical catalogue/provenance, using AR 915 folder 118.7 as a correspondence lead.
7. Bethel Russian Mission detailed inventory.
8. Advertisements in `Слово истины` 1917 and late 1918 for publisher-series nos. 3–10.

### HOLD
- `Слово истины` 1922 issue row;
- alleged `Слово истины` 1925;
- 1921 congress imprint year;
- exact date of Pavlov's Stockholm report;
- College Fund transfer/expenditure/opening of a school;
- contents of unseen archive folders.

Full control: [Drive synthesis](https://docs.google.com/document/d/1-gnYokX17_0EVa4t6-6kc6R3OGWD6OD4Y6GnocXjADs/edit) and [source register](https://docs.google.com/spreadsheets/d/1b5leKk8uTouwZJZwuWkPXyU23wLKRfXin68bbWswJG4/edit).

## v132 — ARA / Baptist relief attribution gate

A new exact primary locator has been identified:

- `ARA Chart of Operations of Foreign and Domestic Relief Organizations in Five Famine Gubernias of the Ukraine, 1922`;
- Hoover Institution Library & Archives;
- `ARA Russia, box 134, folder 11`;
- official exhibition caption explicitly lists `Baptist` among relief participants.

This establishes a Baptist-labelled operation inside the ARA Ukrainian relief matrix. It does **not** establish which Baptist organization stood behind the row, and it does not connect the row directly to the Southern Baptist Foreign Mission Board, Everett Gill or Hoyt Echols Porter.

### P0 — exact closure request

Request only box 134, folder 11, beginning with:

1. a full-resolution image of the chart;
2. the folder inventory and adjacent explanatory sheets;
3. the five gubernia headings and the complete `Baptist` row;
4. every attached name, address, territory, quantity, agreement, financial/accounting reference and date.

Then compare the result with:

- AR 915 folders 91.20 and 92.6;
- AR 551-2, box 045;
- Porter/Gill and relief items in MF 7853;
- FMB annual and committee records already queued in v130.

### Attribution boundary

- The ARA item confirms institutional Baptist participation.
- A contemporary Associated Press notice of 23 December 1921 places Everett Gill in Russia and records his appeal for Christmas offerings for starving Russians; it proves presence and fundraising advocacy, not command of the charted operation.
- Porter remains the exact field-worker/archive route mapped in v130, but the chart caption does not name him.
- The ARA’s nonsectarian distribution rule is compatible with denominational fundraising; it is not evidence that one denomination owned the whole operation.

Until the chart and folder are inspected, keep the status:

`OFFICIAL CAPTION/LOCATOR VERIFIED — BAPTIST BODY AND RESPONSIBLE PERSON UNRESOLVED`.

Source routes:

- https://histories.hoover.org/bread-medicine/a-delicate-balance-in-ukraine/
- https://oac.cdlib.org/findaid/ark:/13030/tf996nb3ks
- https://texashistory.unt.edu/ark:/67531/metapth1534645/m1/1/
