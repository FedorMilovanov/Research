# Джон Гилл (1697–1771) — исследовательский отдел

**Дата создания:** 2026-07-06  
**Последняя интеграционная сверка:** 2026-07-09  
**Research snapshot:** `main@58e1ea5fab638812ae693a1d0b1e79c4dcb47131`  
**Site snapshot, проверенный audit:** `gb-is-my-strength@d00715e95b45a32872aae7e00a3030b4c0bf5c12`

> **Canonical home:** эта папка хранит тематические dossiers по Гиллу.  
> **Current status / supersession map:** [`31_GILL_DEPT_MASTER_MAP.md`](31_GILL_DEPT_MASTER_MAP.md).  
> **Evidence archive V1–V11:** [`../incoming/arena-auditor/2026-07-09/GILL_SERIES_EVIDENCE_ARCHIVE_V1_V11_001_480_2026-07-09.md`](../incoming/arena-auditor/2026-07-09/GILL_SERIES_EVIDENCE_ARCHIVE_V1_V11_001_480_2026-07-09.md).

## Текущий статус отдела

```text
Диапазон audit IDs: GILL-CONTENT-001…480
Тематические dossiers: 01–42
Production-код в этой ветке не менялся
```

Ручные totals по `P0`, `HOLD` и другим статусам здесь не поддерживаются: они быстро устаревают и неоднозначны без формального генератора. Для приоритета использовать текущую матрицу `31`, Section 5 в ней и compact index evidence archive.

### Порядок применения материалов

1. `31_GILL_DEPT_MASTER_MAP.md` — текущие решения, supersession и рабочие ограничения.
2. `AGENT_RULES.md` — текущая таксономия источников, статусов и parallel-work protocol.
3. Evidence archive — полные основания, история проходов и compact index `001…480`.
4. Этот README — навигация и правила входа.
5. Dossiers `01–42` — тематическая исследовательская история; отдельные формулировки могут быть `SUPERSEDED`, `CONTESTED` или `HOLD`.

Новый агент не должен считать поздний номер файла автоматически более надёжным и не должен брать раннюю формулировку из evidence archive без проверки позднего supersession.

**Caveat по evidence archive:** файл сохранён byte-for-byte как итог накопительных проходов V1–V11 ради provenance. Его внутренний заголовок `FINAL MASTER`, UI-пункт про A−/A+, старая taxonomy `Level D`, ранние очереди и provisional hypotheses являются историческим слоем, а не текущей инструкцией. Current wording/status брать из `AGENT_RULES.md` и `31`.

---

## Модель источников и статусов

Использовать корневой [`AGENT_RULES.md`](../AGENT_RULES.md).

Кратко:

- `Level A/B/C` — уровень доказательности для конкретного claim;
- `CONFIRMED / CONTESTED / HOLD / SUPERSEDED / EDITORIAL` — статус claim;
- source work и access host фиксируются отдельно;
- текст сайта — **TARGET**, а не источник для самоподтверждения.

`archive.org`, CCEL, The King’s Bible, Reformed Reader и другие площадки не получают уровень автоматически: важны конкретная копия, проверка текста и locator.

---

## Основные точки входа

| Задача | Входной файл | Примечание |
|---|---|---|
| Текущий статус и supersession | `31_GILL_DEPT_MASTER_MAP.md` | Читать первым |
| Полное обоснование audit findings | evidence archive в `incoming/arena-auditor/2026-07-09/` | Ранние проходы сохраняют исторические формулировки; проверять поздние corrections |
| Биография по Риппону | `17_BIOGRAPHICAL_PRIMARY_SOURCES_AND_VERIFICATION.md` | Возраст дочери и часть нормализаций уточнены в `31` и audit |
| Структура Doctrinal / Practical Divinity | `05_BODY_OF_DIVINITY_TOC_AND_ARTICLE_SKELETON.md` | 7 doctrinal + 4 practical books; edition mapping обязателен |
| *The Cause of God and Truth* | `12`, `19`, `21`, `23`, `27` | Использовать через `31`; Part IV и duty-faith имеют superseded/contested выводы |
| Завет и eternal justification | `08`, `23`, `25` | Цитаты и interpretive verdict хранить раздельно |
| Политическая теология | `38_THE_POLITICAL_THEOLOGY.md` | Корректирует упрощённое «полное отделение» из `10` |
| Spurgeon / Whitefield / Brown | archive + `30`, `35`, `36` | Многие яркие claims остаются HOLD или зависят от одной secondary chain |
| Site deployment | `31` + archive route-by-route | Пути относятся к указанному site snapshot и должны перепроверяться после движения site `main` |

---

## Инвентарь dossiers

Dossiers `01–42` сохранены как provenance и рабочая исследовательская история. Здесь они сгруппированы, чтобы не дублировать длинную рекламную таблицу.

| Диапазон | Кластер |
|---|---|
| `01–06` | первичная карта серии, структура трудов, ранние content-аудиты и site-index |
| `07–17` | введение, биография, систематика, завет, экклесиология, эсхатология, Троица, иврит |
| `18–30` | экзегеза, Cause verbatim, Уэсли, Откровение, этика, Practical Divinity, Whitefield |
| `31` | current master map / matrix |
| `32–37` | неономианство, Sabbath, молитва, legacy, Edwards, герменевтика |
| `38–42` | политическая теология, пневматология, христология, Писание, творение/провидение |

### Нумерация после `42`

Не создавать `43_...` автоматически. Новый номер допустим только когда:

1. тема действительно отсутствует в `01–42` и `31`;
2. проверены открытые PR и ветки;
3. определён canonical owner;
4. изменение внесено в navigation/map тем же PR.

Новые подтверждения существующих тем интегрируются в canonical owner, а не оформляются ещё одним перекрывающимся dossier.

---

## Критические supersession-указания

- `09`: John 6:37 как событие 1 ноября 1716 — **SUPERSEDED**; chronology сверять по `17`, `31` и relevant archive finding.
- `03/04`: планы отдельной Part IV — исторические предложения, не утверждённая архитектура.
- `07`: «Rippon засвидетельствовал 10+ млн слов» — **SUPERSEDED**; у Риппона более 10 000 printed sheets, word total — поздняя экстраполяция.
- `10` vs `38`: «полное отделение церкви от государства» — **SUPERSEDED** более точной политико-богословской формулой.
- `26`: указан неверный Archive item для *Good Works* — **HOLD / high-priority correction**.
- `27`: первичный Ин. 1:7 подтверждён, вывод «опровергает hyper-Calvinism» — **CONTESTED**, а не Level A conclusion.
- `29`: *Practical Divinity* имеет четыре books; appendix о proselyte baptism не создаёт Book V.
- `30`: Whitefield narrative зависит преимущественно от Ella/derivative chain — **HOLD** до независимой первичной опоры.
- `39/40/42`: цифровые CCEL route segments были ошибочно приняты за printed book numbers.
- Spurgeon: не смешивать 1859 foundation-stone event и источник, идентифицированный archive как sermon 369 (1861); exact edition/date проверять по finding locator.

Полный список и operational wording находятся в `31`; доказательства — в evidence archive.

---

## Связь с сайтом

На проверенном site snapshot production content находился преимущественно в:

```text
src/components/article-pilots/gill-context/
src/components/article-pilots/gill-part1/
src/components/article-pilots/gill-part2/
src/components/article-pilots/gill-part3/
src/components/article-pilots/gill-spravochnik/
```

Это snapshot, а не вечная карта. Перед новым deployment-аудитом повторно проверить актуальный site `main`.

Старые ссылки dossiers на `src/content/articles/dzhon-gill-*.mdx` считать историческими, пока current rendering path не подтверждён заново.

При исправлении claim проверять связанные слои:

```text
article body · quiz · glossary · timeline · TOC · SEO · share text · image caption/alt · bibliography
```

---

## Правило для следующих агентов

Перед новой работой:

1. прочитать `AGENT_RULES.md`, этот README, `31` и relevant archive finding;
2. проверить актуальный `main`, открытые PR и ветки;
3. работать в уникальной ветке;
4. повторно получить blob SHA перед изменением shared-файла;
5. не удалять содержательные старые dossiers — использовать supersession;
6. не считать сайты, копирующие Ella или друг друга, независимыми свидетелями;
7. не писать `верифицировано` без точного locator и отдельной проверки interpretation;
8. не создавать новые registries или numbered dossiers только потому, что они когда-то были предложены в раннем audit pass.