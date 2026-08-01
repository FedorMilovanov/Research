# Source Library

Единая точка входа в межпроектную библиотеку источников, книг, изображений, рукописей и правовых решений.

Корпус подчиняется глобальной [`repository-evidence-policy-v2`](../data/repository-evidence-policy-v2.json) и [`artifact-custody-policy-v2`](../data/artifact-custody-policy-v2.json).

## Главные индексы

- [MASTER_OPEN_ACCESS_SOURCE_INDEX_2026-07-30.md](MASTER_OPEN_ACCESS_SOURCE_INDEX_2026-07-30.md) — проверенные точки входа по литературе, рукописям и вспомогательным материалам.
- [OFFICIAL_DIGITAL_COLLECTIONS_70PLUS_INDEX_2026-07-30.md](OFFICIAL_DIGITAL_COLLECTIONS_70PLUS_INDEX_2026-07-30.md) — официальные коллекции, библиотеки, архивы и музеи.

Индекс официальной коллекции не является списком автоматически разрешённых production-файлов. Для каждого объекта отдельно проверяются идентичность, полный объект, точный локатор, provenance, права, credit line и целевой маршрут.

## Корпус 40 PDF

- [COMMONS_RUSSIAN_LITERATURE_40PLUS_PDF_PASS_2026-07-30.md](COMMONS_RUSSIAN_LITERATURE_40PLUS_PDF_PASS_2026-07-30.md) — методика поиска и проверки.
- [processed/COMMONS_STRICT_40_PROCESSING_INDEX_2026-07-30.md](processed/COMMONS_STRICT_40_PROCESSING_INDEX_2026-07-30.md) — состав, страницы, тематические корзины, текстовый слой и SHA-256.
- [Воспроизводимый workflow](../.github/workflows/build-commons-russian-literature-open-pdf-archive.yml).

Зафиксированный исследовательский проход содержал 40 PDF, 12 434 страницы и SHA-256 для каждого объекта. Эти цифры описывают конкретный evidence package. GitHub Actions artifact с семидневным retention остаётся `EPHEMERAL_ACTION_ARTIFACT`, пока не создан durable receipt с destination object ID и SHA-256 readback.

## Независимые статусы

Старые значения `DOWNLOAD-OK`, `LINK-ONLY`, `PRIVATE-STUDY`, `HOLD`, `CATALOG-ONLY` были смешанными shorthand. Для новых и обновляемых записей используются отдельные оси:

### Access state

- `FULL_OBJECT_VERIFIED`
- `PARTIAL_OBJECT`
- `CATALOG_ONLY`
- `LINK_ONLY`
- `NOT_ACQUIRED`

### Custody state

- `EPHEMERAL_ACTION_ARTIFACT`
- `TRANSFER_PENDING_VERIFICATION`
- `ACQUIRED_DURABLE`
- `PRIVATE_STUDY_ONLY`

### Rights state

- `PUBLICATION_ELIGIBLE`
- `STORAGE_ONLY`
- `PRIVATE_STUDY_ONLY`
- `PERMISSION_REQUIRED`
- `RIGHTS_UNKNOWN`

### Publication state

- `PROMOTE`
- `REFERENCE`
- `SUPERSEDED`
- `BLOCKED`

`DOWNLOAD-OK` в исторической записи означает только успешный download в конкретном проходе; он не равен `ACQUIRED_DURABLE` и не равен `PUBLICATION_ELIGIBLE`. `HOLD` должен быть заменён типизированным `EVIDENCE_HOLD`, `LOCATOR_HOLD`, `ARCHIVE_HOLD`, `RIGHTS_HOLD` или `PUBLICATION_HOLD`.

## Где хранить материалы

- GitHub: authority, research text, URL indexes, provenance, citations, rights ledgers, checksums и durable receipts.
- Durable private storage: только объекты, для которых сохранены destination ID, размер и SHA-256 readback.
- Link-only: restricted viewers, нескачанные каталожные карточки и объекты с неясным правом перераспространения.
- Не публиковать: restricted facsimiles без разрешения, персональные данные из переписки и современные книги сомнительного происхождения.

## Связанные проекты

- [The Legendary Poet — Esenin/Duncan dossier](https://github.com/FedorMilovanov/TheLegendaryPoet/blob/main/docs/ESENIN_DUNCAN_RESEARCH_DOSSIER_2026-07-30.md)
- [The Legendary Poet source policy](https://github.com/FedorMilovanov/TheLegendaryPoet/blob/main/docs/IMLI_RUSSIAN_LITERATURE_ARCHIVE.md)
- [The Legendary Poet source list](https://github.com/FedorMilovanov/TheLegendaryPoet/blob/main/docs/RESEARCH_SOURCES.md)
- [gospod-bog.ru manuscript-source integration](https://github.com/FedorMilovanov/gb-is-my-strength/blob/main/docs/research/OPEN_SOURCE_MANUSCRIPT_LIBRARY_4Q204_P72_2026-07-30.md)
- [Audit intake](https://github.com/FedorMilovanov/AuditRepo/tree/main/projects/the-legendary-poet/incoming/gpt-5-6-source-library/2026-07-30)
