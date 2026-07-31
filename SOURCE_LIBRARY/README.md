# Source Library

Единая точка входа в межпроектную библиотеку источников, книг, изображений, рукописей и правовых решений.

## Главные индексы

- [MASTER_OPEN_ACCESS_SOURCE_INDEX_2026-07-30.md](MASTER_OPEN_ACCESS_SOURCE_INDEX_2026-07-30.md) — 80+ проверенных ссылок по Сергею Есенину, Айседоре Дункан, 4Q204, P72, SBLGNT, Codex Sinaiticus и вспомогательной литературе.
- [OFFICIAL_DIGITAL_COLLECTIONS_70PLUS_INDEX_2026-07-30.md](OFFICIAL_DIGITAL_COLLECTIONS_70PLUS_INDEX_2026-07-30.md) — 94 официальные точки входа: Library of Congress, NYPL, British Library, Bodleian, Cambridge, NTVMR, CSNTM, Vatican, Dead Sea Scrolls, Europeana, Gallica/BnF, российские библиотеки, архивы и музеи, портретные категории поэтов и открытые книжные каталоги.

Второй индекс является картой официальных коллекций, а не списком автоматически разрешённых production-файлов. Для каждого объекта отдельно проверяются карточка, provenance, лицензия и credit line.

## Финальный строгий корпус 40 PDF

- [COMMONS_RUSSIAN_LITERATURE_40PLUS_PDF_PASS_2026-07-30.md](COMMONS_RUSSIAN_LITERATURE_40PLUS_PDF_PASS_2026-07-30.md) — методика строгого поиска, права, очистка ложных совпадений и итоговый gate.
- [processed/COMMONS_STRICT_40_PROCESSING_INDEX_2026-07-30.md](processed/COMMONS_STRICT_40_PROCESSING_INDEX_2026-07-30.md) — состав всех 40 PDF, число страниц, тематические корзины, текстовый слой и контрольные SHA.
- Воспроизводимый workflow: [../.github/workflows/build-commons-russian-literature-open-pdf-archive.yml](../.github/workflows/build-commons-russian-literature-open-pdf-archive.yml).

Итог корпуса:

- 40 действительных PDF;
- 12 434 страницы;
- 610 183 443 байта;
- 39 Public Domain и 1 CC BY-SA 4.0;
- 40/40 совпадений SHA-256;
- 40/40 первых страниц отрендерены и визуально проверены;
- 19 развитых текстовых слоёв, 4 частичных, 17 scan-first.

Корпус является вспомогательной библиотекой старых изданий и периодики. Он не заменяет академические комментарии ИМЛИ, ФЭБ и РВБ. Использование отдельной фотографии или иллюстрации требует собственной проверки provenance и прав.

## Статусы

- `DOWNLOAD-OK` — официальный open access, public domain или открытая лицензия;
- `LINK-ONLY` — публично хранить ссылку и описание, но не бинарный объект;
- `PRIVATE-STUDY` — частный просмотр/скриншот без публичной публикации;
- `HOLD` — права или provenance не подтверждены;
- `CATALOG-ONLY` — запись каталога без доступного файла.

## Где хранить материалы

- GitHub: исследовательский текст, ссылки, provenance, цитатные ledgers, лицензии и решения.
- Частный Google Drive: официальные open-access PDF/JPEG, переписка учреждений, manifests и private-study screenshots.
- Постоянная Library-копия: резервные ZIP, пока Drive-коннектор недоступен.
- Не хранить публично: IAA/P72 факсимиле без разрешения, персональные данные из писем, современные книги сомнительного происхождения.

## Связанные проектные документы

- The Legendary Poet: https://github.com/FedorMilovanov/TheLegendaryPoet/blob/main/docs/ESENIN_DUNCAN_RESEARCH_DOSSIER_2026-07-30.md
- The Legendary Poet source policy: https://github.com/FedorMilovanov/TheLegendaryPoet/blob/main/docs/IMLI_RUSSIAN_LITERATURE_ARCHIVE.md
- The Legendary Poet source list: https://github.com/FedorMilovanov/TheLegendaryPoet/blob/main/docs/RESEARCH_SOURCES.md
- gospod-bog.ru manuscript-source integration: https://github.com/FedorMilovanov/gb-is-my-strength/blob/main/docs/research/OPEN_SOURCE_MANUSCRIPT_LIBRARY_4Q204_P72_2026-07-30.md
- Audit intake for The Legendary Poet: https://github.com/FedorMilovanov/AuditRepo/tree/main/projects/the-legendary-poet/incoming/gpt-5-6-source-library/2026-07-30
