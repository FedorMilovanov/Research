# Reader R6 — единое состояние чтения

**Дата:** 2026-07-22  
**Проект:** `FedorMilovanov/gb-is-my-strength`  
**Проверенный source baseline:** `a0c9c025b05eccfce0ab4818da250d05d1b65da0`  
**Рабочий issue:** `gb-is-my-strength#127`  
**Уровень верификации:** **A — проверено непосредственно по production source-коду**

## 1. Цель исследования

После Reader R1–R5 сайт уже получил:

- общие preferences и первый кадр;
- формальную модель `series / article / page / special`;
- правило `book = series + seriesShape=book`;
- нейтральный `SeriesReaderChrome` façade;
- единый `OverlayRuntime`;
- route registry и постоянные CI-контракты.

Следующий архитектурный долг — не новый визуальный «движок», а единое состояние пользователя:

```text
progress / resume
completed
manual saved articles
saved quotations / notes
series and book aggregation
cross-tab synchronization
```

Сейчас эти функции существуют, но принадлежат разным storage-схемам и API.

## 2. Проверенные владельцы состояния

### 2.1. Progress и resume — `BookmarkEngine`

**Источник:** `js/bookmark-engine.js`.

Проверено:

- ключ маршрута: `bookmark:<siteId>:<normalizedPath>`;
- payload version: `4`;
- сохраняются `section`, `progress`, `scrollY`, `completed`, `savedAt` и route metadata;
- отдельные cleanup/dismissed ключи;
- публичные методы включают `getCurrent`, `getAllForSite`, `getResumeCandidate`, `markCompleted`;
- состояние предназначено для автоматического «докуда дочитал».

**Вывод:** название `BookmarkEngine` историческое и двусмысленное. Это прежде всего progress/resume owner, а не ручные ленточные закладки.

### 2.2. Ручное сохранение материалов — Favorites

**Источник:** `js/floating-cluster-controller.js`.

Проверено:

- отдельный ключ `gb-favorites`;
- payload: URL, title, description, image, section, `addedAt`;
- лимит 50;
- код намеренно отделяет Favorites от `BookmarkEngine`.

**Вывод:** favorite и progress — разные пользовательские действия. Их нельзя слить в один boolean без потери смысла.

### 2.3. Цитаты и заметки — Highlights

**Источник:** `js/highlights.js`.

Проверено:

- отдельный ключ `gb-highlights-v1`;
- payload содержит цитату, URL, заголовок статьи, время сохранения и идентификатор;
- собственный canonical overlay, поиск, удаление, undo, export/share;
- данные читаются через `window.GBHighlights`.

`GillLearningSheet.astro` не создаёт второе хранилище заметок: он читает `GBHighlights.getAll()` и открывает canonical overlay.

**Вывод:** это правильная граница. R6 должен объединить индекс, маршрутизацию и счётчики, но не дублировать highlights UI или content payload.

## 3. Проверенное исходное требование пользователя

По восстановленной Claude-сессии «Визуальное оформление интерфейса Гилла» требовалось использовать реальную логику сайта:

- progress/resume «докуда дочитал»;
- сохранённые материалы;
- заметки/цитаты;
- понятные счётчики;
- согласованный порядок reader-разделов;
- без изобретения отдельной системы ленточных закладок.

Следовательно, R6 — слой согласования существующих функций, а не новый независимый feature.

## 4. Главные дефекты текущей модели

### R6-D1. Нет единого route identity

Разные владельцы самостоятельно нормализуют URL. Риск:

```text
/path
/path/
/path/index.html
/path/?utm=...
/path/#section
```

могут стать несколькими пользовательскими объектами.

### R6-D2. Нет общего versioned contract

Схемы `bookmark:*`, `gb-favorites`, `gb-highlights-v1` развиваются независимо. Нет одного места, где определены:

- namespace;
- payload version;
- migration order;
- canonical-vs-legacy precedence;
- corruption recovery;
- quota policy.

### R6-D3. Нет общего события изменения

Reader chrome, learning sheet, floating controls и будущая library surface вынуждены читать несколько stores вручную. Нет единого `subscribe()` и cross-tab contract.

### R6-D4. Series/book aggregation не формализована

Progress хранится route-by-route, но пользователь мыслит серией или книгой. Требуются доказанные правила:

- последняя открытая часть;
- процент серии;
- completed chapters;
- resume candidate;
- ручные favorites внутри series;
- notes count по route и series.

### R6-D5. Ошибки одного namespace могут повредить UX целиком

Corrupted JSON, quota failure или конфликт legacy/canonical state не должны уничтожать исправные данные других разделов.

## 5. Целевой façade

R6 не должен создавать мегакомпонент. Нужен data/runtime façade:

```text
GBReadingState
  normalizeRoute(input)
  describeRoute(input)

  getProgress(route)
  saveProgress(route, patch)
  listProgress(scope?)
  getResumeCandidate(scope?)
  setCompleted(route, completed)

  listFavorites(scope?)
  isFavorite(route)
  toggleFavorite(route, metadata)

  listNotes(scope?)
  getCounts(scope?)

  migrateLegacy()
  subscribe(listener)
  exportState()
```

UI consumers остаются разными, но больше не владеют storage-схемой.

## 6. Route identity contract

Одна каноническая `normalizeRoute()` должна:

1. использовать `URL` с текущим origin;
2. удалять query и hash из identity;
3. преобразовывать `/index.html` в `/`;
4. нормализовать trailing slash;
5. не менять регистр/Unicode без отдельного доказательства;
6. связывать route с public surface registry;
7. получать `surface`, `seriesId`, `seriesShape`, `pageId` из registry/config, а не угадывать по имени папки.

Пример канонического descriptor:

```json
{
  "route": "/articles/example/",
  "surface": "article",
  "seriesId": null,
  "seriesShape": null,
  "pageId": "article:example"
}
```

Для книги:

```json
{
  "route": "/articles/krajne-li-isporcheno-serdce/glava-3/",
  "surface": "series",
  "seriesId": "serdce",
  "seriesShape": "book",
  "pageId": "serdce:chapter-3"
}
```

## 7. Хранилище: решение пока не фиксировать преждевременно

До data-size/write-frequency аудита допустимы две модели:

### Вариант A — один versioned document

```text
gb:reading-state:v1
```

Плюсы: атомарная схема и export.  
Минусы: частая перезапись большого JSON при scroll progress.

### Вариант B — согласованный набор canonical keys

```text
gb:reading:progress:v1:<route>
gb:reading:favorites:v1
gb:reading:notes-index:v1
gb:reading:meta:v1
```

Плюсы: изоляция частых записей и ошибок.  
Минусы: сложнее атомарная миграция/export.

**Предварительный вывод:** progress, скорее всего, должен остаться route-scoped; meta/favorites/notes index — отдельными versioned namespaces под одним façade.

## 8. Миграционная политика

Обязательный порядок:

```text
read canonical
→ validate canonical namespace
→ read legacy only if canonical item absent
→ normalize route and payload
→ write canonical once
→ mark migration version
→ retain legacy compatibility until browser parity
```

Запрещено:

- переписывать все legacy keys на каждой загрузке;
- позволять устаревшему ключу откатывать новый canonical state;
- удалять legacy data в первой транзакции;
- создавать дубликаты при повторной миграции;
- молча очищать весь store из-за одного corrupted item.

## 9. События и cross-tab contract

Предлагаемые события:

```text
gb:reading-state-change
storage
```

Payload custom event:

```json
{
  "namespace": "progress|favorites|notes|completed",
  "route": "/canonical/route/",
  "seriesId": "optional",
  "reason": "save|toggle|migrate|external-storage",
  "version": 1
}
```

`subscribe(listener)` должен возвращать unsubscribe-функцию и дедуплицировать storage/custom-event echo.

## 10. Write policy

Progress writes:

- throttle/debounce;
- обязательный flush на `pagehide`;
- не писать одинаковый payload;
- не уменьшать более свежий progress без явного route reset;
- сохранять валидный section anchor вместе с scroll fallback;
- учитывать back/forward navigation.

Favorites/notes:

- user-action writes без scroll throttling;
- точная обработка quota failure;
- canonical state обновляется только после успешной записи.

## 11. Транзакции реализации

### R6.1 — inventory + contract

- полный readers/writers/key inventory;
- route identity contract;
- data-size, quota и write-frequency audit;
- dependency-free migration fixtures;
- corrupted/conflicting/canonical-precedence tests;
- source architecture doc + AuditRepo matrix.

### R6.2 — progress/resume façade

- façade поверх существующего `BookmarkEngine`;
- DOM/UX не меняются;
- series/book aggregation;
- cross-tab event;
- representative route parity.

### R6.3 — favorites façade

- ownership `gb-favorites` переносится под API;
- старые кнопки, CSS и тексты сохраняются;
- общий badge/count.

### R6.4 — notes index adapter

- чтение canonical highlights API;
- route/series filtering;
- counts;
- highlights content store и overlay не переписываются.

### R6.5 — unified library surface

Только после доказанной миграции:

```text
Продолжить
Сохранённые
Заметки
Завершено
```

## 12. Browser acceptance matrix

Проверить минимум:

- flat series;
- book route;
- standalone article;
- ordinary page;
- 320 / 360 / 390 / 430 px;
- desktop parity;
- refresh;
- back/forward;
- pagehide flush;
- cross-tab update;
- corrupted legacy item;
- conflicting canonical/legacy item;
- slash/index/query/hash dedupe;
- same quotation on different routes remains route-scoped;
- favorite and progress remain independent;
- migration is idempotent;
- no horizontal overflow;
- clean-tree and cache-bust invariants.

## 13. Зависимости и границы

До начала production-кода R6:

1. закрыть `gb-is-my-strength#58` точным Pages/blob witness;
2. удалить temporary production observer;
3. влить fresh highlights hardening для `#112`;
4. не смешивать R6 с Nagornaya runtime/content lanes.

Не входит в R6.1–R6.4:

- аккаунты и облачная синхронизация;
- TTS session persistence;
- quiz mechanics;
- reader redesign;
- удаление legacy keys;
- специальная логика карт/3D.

## 14. Вердикт

Техническая база универсальной reader-платформы уже существует. Главный следующий шаг — не ещё один engine, а формальный data contract над четырьмя существующими владельцами.

```text
R1–R5: unified presentation/runtime
R6: unified user reading state
```

При соблюдении транзакций R6 позволит менять progress, favorites и notes один раз на уровне платформы и получать одинаковое поведение в книге, обычной серии, одиночной статье и простой странице без массовых route-specific правок.
