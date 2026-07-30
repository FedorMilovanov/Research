# Финальный closeout тотального аудита — 30 июля 2026

**Репозитории:** `TheLegendaryPoet`, `gb-is-my-strength`, `Research`, `AuditRepo`  
**Статус:** `AUDIT COMPLETE / ACQUISITION CONTINUES / NO FALSE COMPLETION CLAIMS`

## Итог машинного прохода

- файлов просмотрено: **4 808**;
- внешних URL-вхождений: **12 096**;
- уникальных URL: **6 528**;
- источниковых кандидатов после удаления localhost, шаблонов, зависимостей, аналитики и собственных доменов: **4 892**;
- URL, повторно проверенных уточнённым проходом: **2 500**;
- SHA-дубли: **43 группы**; автоматическое удаление запрещено без проверки назначения.

## Исправленный результат DEAD-аудита

Сырые `404/410` нельзя было считать реальными проблемами. Третий проход повторно очистил и проверил **234** строки:

| Класс | Число |
|---|---:|
| Восстановлены после очистки URL или HTTPS | 134 |
| Реальная очередь ремонта источников | **45** |
| Обрезанные URL — ложное срабатывание | 24 |
| Технические или архивные ссылки | 13 |
| Мёртвые, но не источниковые ссылки | 12 |
| Шаблоны | 4 |
| Корневые service endpoints, не item-ссылки | 2 |

Полный список 45 строк находится в artifact-файле `dead-url-classification/true_dead_source_repair_queue.csv`.

## Подтверждённые замены первой очереди

| Старый адрес | Текущий адрес | Решение |
|---|---|---|
| `https://www.ccel.org/creeds/bcf/bcftoc.htm` | `https://www.ccel.org/creeds/bcf/bcf.htm` | заменить в ledger; CCEL также публикует современную текстовую навигацию `ccel/anonymous/bcf...` |
| `http://feb-web.ru/feb/esenin/about.htm` | `https://feb-web.ru/feb/esenin/rub.html` | заменить общей карточкой ЭНИ «Есенин» |
| `http://feb-web.ru/feb/esenin/sitemap.asp` | `https://feb-web.ru/feb/esenin/sitemap.htm` | заменить актуальной картой ЭНИ |
| `https://isadoraduncanarchive.org/all-items/` | `https://www.isadoraduncanarchive.org/collection/all` | заменить; изображения всё равно rights-per-item |
| `https://isadoraduncanarchive.org/historical/` | `https://www.isadoraduncanarchive.org/collection/` | заменить точкой входа в Print Media Collections |
| `https://isadoraduncanarchive.org/works/` | `https://www.isadoraduncanarchive.org/reference/isadora` | заменить библиографией Works by Isadora |
| `https://lexicon.qumran-digital.org/transcriptions/index.html` | `https://lexicon.qumran-digital.org/transcriptions/4Q204/2025-11-11/index.html` | для статьи о 4Q204 ссылаться на конкретную версию; лицензия страницы CC BY-SA 4.0 |
| — | `https://lexicon.qumran-digital.org/transcriptions/4Q204/changelog.html` | хранить как version history и фиксировать дату версии |

### Правовая граница Duncan Archive

Новая структура сайта жива, но сам архив прямо указывает, что права зависят от конкретной коллекции и многие изображения нельзя использовать без разрешения владельца. Поэтому обновление URL **не означает** разрешения на публикацию изображения.

## Acquisition-pass: исправление результата

Первый автоматический проход формально сообщил о 15 файлах, но ручная проверка установила:

- 12 файлов НЭБ были одинаковым служебным `/manifest.json` веб-приложения;
- это не тома Маяковского, не IIIF-манифесты и не item metadata;
- все 12 отклонены и исключены из архива.

### Реально приобретено

| Корпус | Commit SHA | Размер | SHA-256 пакета |
|---|---|---:|---|
| `STEPBible/STEPBible-Data` | `b86d26cdb1f51729e73b5b4eb7f7ccadc5dfba39` | 100 920 275 | `6845fa9660c62301a0eec38c009ca34ef82647a9737529d8c56ac45d35182df0` |
| `openscriptures/morphhb` | `3d15126fb1ef74867fc1434be1942e837932691f` | 20 870 584 | `f56c150708b5d74719ecb709c712c31eae9855bca7b111fd82ec91b5d177b4c7` |
| `Faithlife/SBLGNT` | `c4d241a9c1c479a55b989ba35a4976c1d0b8052c` | 1 414 688 | `4fc2659ce10ec6f57552f22e039de927ed3e417c7b5a757f34f05dae530e4c0f` |

Итого: **3 неизменяемых snapshot**, **123 205 547 байт**.

### Лицензии

- `morphhb`: текст WLC public domain; lemma/morphology CC BY 4.0 с обязательной атрибуцией Open Scriptures Hebrew Bible Project;
- `SBLGNT`: CC BY 4.0;
- `STEPBible-Data`: лицензия проверяется для каждого набора отдельно; общий ZIP не даёт единого универсального разрешения на все вложенные данные.

## Репозиторные дефекты, закрытые в ходе аудита

1. `TheLegendaryPoet`: 13 production-изображений получили центральный `public/images/PROVENANCE.yml`; локальные реконструкции отделены от архивных фото.
2. `gb-is-my-strength`: досье о происхождении ярлыка «секта» получило claim-to-source матрицу и publication gate.
3. `Research`: `original_article_latest_uploaded.zip` получил размер, SHA-256, `HOLD`-границу и recovery tasks.
4. `AuditRepo`: три архивных QA PNG получили capture ledger; неизвестные URL/tool/operator остались `UNRESOLVED`.

## Что ещё реально нужно получить

### P0

1. **15 официальных академических единиц Есенина ИМЛИ**: шесть книг «Летописи» и девять книг ПСС. GitHub/Azure не смог установить соединение с `biblio.imli.ru`; зеркалами не заменять. Пока PDF-транспорт не восстановлен, ФЭБ служит полноценным текстовым научным доступом к ПСС и частично к «Летописи».
2. **12 томов Маяковского в НЭБ**: карточки томов подтверждены, но реальный PDF не был обнаружен. Статус `CATALOG/VIEWER-ONLY`, а не `DOWNLOADED`.
3. **Датированные imperial + Soviet primary usages** для статьи о слове «секта».

### P1

4. шесть datasets Пушкинского Дома через Dataverse DOI/API;
5. семь корзин электронных изданий Пушкинского Дома;
6. item-level public-domain тома Owen, Goodwin, Charnock, Flavel и Manton;
7. identity-verified portrait packs Пушкина, Лермонтова, Маяковского, Ахматовой, Гумилёва, Пастернака и Цветаевой;
8. отдельный rights review для Дункан и Лили Брик.

### LINK-ONLY / HOLD

9. P72 Vatican/DigiVatLib;
10. фотографии 4Q204 IAA/Leon Levy;
11. современная книга Drawnel;
12. NYPL/Duncan images без item-level permission;
13. современные издания и изображения без явной open-license.

## Оставшиеся технические задачи

- вручную разобрать 24 вероятные локальные ссылки; подтверждены опечатка в URL-пути `ТРУДНЫЕ ТЕКСТЫ`, четыре межрепозиторные Gill/AuditRepo ссылки и один внешний URL без схемы;
- не считать regex, `route.json`, `_app/index.html` и lossless snapshots реальными битым файлами;
- файл `research/GILL_DEEPENING_REPORT_2026-07-07.md` является процессным отчётом и отдельной библиографии не требует;
- 45 source URLs ремонтировать заменой на DOI, новую официальную карточку, стабильный каталог или архивную копию; не удалять доказательство молча.

## Хранение

Чистый acquisition v2 сохранён в Library:

`/The Legendary Poet — Source Archive/OFFICIAL CORE ACQUISITION 59 V2 — 2026-07-30/`

Финальный audit artifact сохранён в:

`/The Legendary Poet — Source Archive/AUDITS/TOTAL CROSS REPO SOURCE AUDIT — 2026-07-30/`
