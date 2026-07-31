# Инвентаризация перехода «Баптистов России» к книжному движку

**Дата:** 2026-07-31

## Проверенные production-маршруты

Просмотрены HTML всех десяти текущих глав от `/noch-na-kure/` до `/spravochnik/`, landing, `data/series.json` и expansion-roadmap.

## Главный технический вывод

Каждая HTML-страница вручную повторяет:

- `10 частей · живая исследовательская серия`;
- `data-gbs2-total-min="229"`;
- `N из 10`;
- десять desktop-карточек;
- десять mobile-карточек;
- previous/next;
- подписи `часть` в hero и alt;
- reading-time/progress значения.

Поэтому добавление новых глав через ручную замену опасно. Нужен единый книжный source-of-truth, из которого генерируются rail, mobile sheet, previous/next, число опубликованных глав и общее время.

## Найденный баг

В части 4 HTML уже содержит визуальный `100%` при `done-min=55`, `part-min=21`, `total-min=229`. В частях 5–10 также стоит `100%`, хотя книга ещё не пройдена полностью.

Нужно разделить:

1. чтение текущей главы;
2. число завершённых глав;
3. общий прогресс книги.

## Целевая структура

- верхний объект `type: book`, `status: living-book`;
- уровни `part`, `chapter`, `appendix`;
- каждая глава сохраняет нынешний URL;
- planned-главы не публикуются как пустые страницы;
- «Справочник» переносится в приложения/аппарат;
- landing получает `Book`/`CollectionPage` только после metadata-аудита;
- chapter pages связываются с книгой через `isPartOf`;
- `dateModified` меняется только при содержательной правке.

## SYSTEM-проход

Отдельный SYSTEM PR должен изменить данные и генерацию навигации, а не массово переписывать десять HTML вручную. Проверки: JSON/schema, canonical, breadcrumbs, desktop/mobile TOC, previous/next, progress, RSS/sitemap/search, metadata, visual parity, exact-head CI и production witness.

Полная версия находится в `gb-is-my-strength/baptisty-rossii/research/82-book-engine-migration-inventory-2026-07-31.md`, lane `lane/baptists-book-research-integration-2026-07-31`.
