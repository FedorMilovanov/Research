# Перемещение отдела «Джон Гилл» в «БИОГРАФИИ» — запись о supersession и смене пути

**Дата:** 2026-10-25
**Тип записи:** `SUPERSEDED` (путь) · содержимое томов не переписано
**Операция:** `git mv "Джон Гилл" "БИОГРАФИИ/Джон Гилл"` (78 файлов, rename-детекция сохраняет историю)

## Уточнение при подготовке PR, 2026-10-27

Ниже сохранён исторический отчёт25октября;его формулы «все проходят» и
«78побайтно» не являются текущим свидетельством. Проверка по исходному
HEAD f38b194:все78файлов существуют на новом месте,71побайтно совпадает,
в семи изменены пути/навигация/исторические оговорки. Исходный архив и
матрица отдельно проверяются по неизменным blob pins. Название операции
`git mv` описывает намерение переноса, а не заменяет сравнение содержимого.

До коммита lossless-аудит также обнаруживал отсутствие нового пути вHEAD
и dirty inputs;его нельзя свести только к отсутствию Product-checkout.
Для текущей проверки получен настоящий Product-checkout и оба pinned
commit witnesses;окончательный результат проверяется после коммита.
Предыдущая таблица результатов ниже — историческая, не свежий CI.

---

## 1. Проверяемый вопрос

Можно ли переместить канонический отдел Гилла из корня репозитория в новый отдел «БИОГРАФИИ»,
не сломав machine-guarded authority graph, workflow-фильтры и validator-пути?

**Ответ:** да, при условии полной синхронной правки всех машинных ссылок. Фактическое состояние —
выполнено, все затронутые валидаторы проходят.

---

## 2. Что было сделано

| Шаг | Действие | Результат |
|---|---|---|
| 1 | Создан корень отдела `БИОГРАФИИ/` | новый канонический дом биографий |
| 2 | `git mv "Джон Гилл" → "БИОГРАФИИ/Джон Гилл"` | 78 файлов, содержимое байт-в-байт не тронуто |
| 3 | Синхронная правка всех путей `Джон Гилл/` → `БИОГРАФИИ/Джон Гилл/` | 28 файлов вне отдела + 4 файла внутри |
| 4 | Восстановление глубины относительных ссылок внутри отдела | `../` → `../../` для 5 ссылок на корень репозитория |
| 5 | Откат правки исторического архива `incoming/arena-auditor/2026-07-09/…` | blob SHA восстановлен, losslessness сохранён |
| 6 | Прогон всех затронутых валидаторов | PASS |

---

## 3. Полный реестр правок путей

### 3.1. Машинные и CI-критичные

| Файл | Ссылок | Что проверяет |
|---|---:|---|
| `scripts/gill-pr2-lossless-reconciliation-audit.mjs` | 15 | blob-pin, 480 ID, dossier-маркеры |
| `scripts/validate_gill_closed_book_families.py` | 2 | DOC/DISC_DOC пути |
| `scripts/validate_gill_rippon_claim_cards.py` | 3 | OWNER/DOC пути |
| `scripts/validate_repository_authority_integrity.py` | 1 | crosswalk путь |
| `data/gill-closed-book-families-2026-08-02.json` | 7 | `ownerDocuments` |
| `data/gill-rippon-1838-claim-cards-2026-08-04.json` | 1 | `ownerDocument` |
| `data/research-stage-closure-2026-08-02.json` | 1 | `semanticAuthority` |
| `ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json` | 4 | `path` записей корпуса |
| `.github/workflows/gill-closed-book-families.yml` | 14 | paths-фильтры pull_request и push |
| `.github/workflows/gill-pr2-lossless-reconciliation.yml` | 2 | `Джон Гилл/**` |
| `.github/workflows/research-closure-witness.yml` | 1 | witness-путь |
| `.github/workflows/research-stage-authority.yml` | 2 | paths-фильтры |
| `00_RESEARCH_CURRENT_AUTHORITY_2026-08-02.md` | 1 | ссылка на 75_ том |

### 3.2. Документационные

| Файл | Ссылок |
|---|---:|
| `README.md` (включая URL-кодированную ссылку) | 1 |
| `1КОРИНФЯНАМ_11_ПОКРЫВАЛО/04B_MASTER_SOURCE_LEDGER_SUPPLEMENT_2026-08-09.md` | 1 |
| `ИСКУПЛЕНИЕ/00_README_AND_NAVIGATION.md` | 1 |
| `ИСКУПЛЕНИЕ/05_SOURCE_REGISTRY_AND_ACQUISITION_QUEUE.md` | 2 |
| `ИСКУПЛЕНИЕ/12_HARD_TEXTS_EXTENT_CARDS.md` | 2 |
| `ИСКУПЛЕНИЕ/14_OWEN_DEATH_OF_DEATH_BOOK_IV_LOCATORS.md` | 1 |
| `ИСКУПЛЕНИЕ/15_CALVIN_III24_AND_DORT_II_LOCATORS.md` | 1 |
| `ИСКУПЛЕНИЕ/nt/00_NT_AUTHORITY_2026-10-07.md` | 1 |
| `ИСКУПЛЕНИЕ/synthesis/02_CONFLICT_LEDGER.md` | 3 |
| `ИСКУПЛЕНИЕ/synthesis/drafts/08_calvin-owen-amyraldianism.md` | 3 |
| `ИСКУПЛЕНИЕ/synthesis/data/synthesis-corpus-v1.json` | 1 |

### 3.3. Внутри перемещённого отдела

| Файл | Правка |
|---|---|
| `БИОГРАФИИ/Джон Гилл/00_README_AND_NAVIGATION.md` | `../68_GILL_…`, `../69_GILL_…` → `../../…` |
| `БИОГРАФИИ/Джон Гилл/00_SOURCE_STATUS_CROSSWALK_V2.md` | `../data/repository-evidence-policy-v2.json` → `../../data/…` |
| `БИОГРАФИИ/Джон Гилл/00A_PR2_LOSSLESS_RECOVERY_AND_SUPERSESSION.md` | 4 ссылки `../incoming/…` → `../../incoming/…`; абсолютные self-ссылки приведены к новому пути |
| `БИОГРАФИИ/Джон Гилл/07_VVEDENIE_DEEP.md`, `17_…`, `77_…` | абсолютные упоминания отдела в тексте приведены к новому пути |

---

## 4. Исторический архив — сознательно НЕ переписан

`incoming/arena-auditor/2026-07-09/GILL_SERIES_EVIDENCE_ARCHIVE_V1_V11_001_480_2026-07-09.md`
содержит два упоминания `Джон Гилл/`. Этот файл — датированный lossless-снимок 2026-07-09, чей
blob SHA `baa3fccb6f67cd05117b2c4f0342867662a3fce0` запинен в
`scripts/gill-pr2-lossless-reconciliation-audit.mjs` как `expectedArchiveBlob` и продублирован
маркером `**Archive blob:**` в `БИОГРАФИИ/Джон Гилл/74_PR2_001_480_RECONCILIATION_MATRIX.md`.

**Решение:** правка откачена, blob восстановлен. Историческая запись пути `Джон Гилл/` сохраняется
как Evidence того, каким был путь на 9 июля 2026 года. Новая canonical-ссылка живёт здесь.

`LOCATOR_HOLD`/`ARCHIVE_HOLD` не снимаются: наличие файла и его blob-pin не доказывают содержательную
полноту 480 записей.

---

## 5. Состояние валидаторов после перемещения

| Валидатор | Результат |
|---|---|
| `validate_research_root_authority.py` | PASS |
| `validate_repository_authority_integrity.py` | PASS |
| `validate_research_stage_closure.py` | PASS |
| `validate_gill_closed_book_families.py` | PASS — 7 families, 1 durable file receipt, 1 edition-usable item, 0 quote-ready |
| `validate_gill_rippon_claim_cards.py` | PASS — 1 page-image-reviewed paraphrase-only claim, 0 direct quotes, 0 Product approvals |
| `validate_source_url_replacements.py` | PASS |
| `validate_public_projection_queue.py` | PASS |
| `gill-pr2-lossless-reconciliation-audit.mjs` | FAIL только на `GILL_PRODUCT_REPO must point to a checked-out gb-is-my-strength repository` — **предсуществующее окружение**, не вызванное перемещением (проверено `git stash`-сравнением) |
| `validate_branch_retirement_authority.py` | FAIL на отсутствующих `archive-ledgers/legacy-diverged-heads-20260801.*` и `source-library-ref-consolidation-20260801.*` — **предсуществующее**, к Гиллу не относится |

---

## 6. Границы допустимой формулировки

- Нельзя утверждать, что перемещение «улучшило» или «исправило» досье Гилла: оно не меняло ни одного
  содержательного утверждения.
- Нельзя утверждать, что новые пути «подтверждены публикацией»: перемещение — операция Research-layer.
- Нельзя удалять исторические упоминания `Джон Гилл/` в датированных архивах.

---

## 7. Права, архив и публикационные HOLD

- Права на тома Гилла не изменились: `publicationState` каждого тома сохраняется как был.
- Drive-копии (`01 — ДЖОН ГИЛЛ`) созданы через `copy_file`; оригиналы на месте.
- SHA-256 readback по копиям **не выполнялся**; custody копий — `TRANSFER_PENDING_VERIFICATION`.

---

## 8. Следующее проверяемое действие

1. После коммита перемещения перепрогнать `gill-pr2-lossless-reconciliation-audit.mjs` — оставшийся
   FAIL должен сократиться до единственного окруженческого (`GILL_PRODUCT_REPO`).
2. Проверить CI-workflow `gill-closed-book-families.yml` и `gill-pr2-lossless-reconciliation.yml` на
   реальном PR: paths-фильтры должны срабатывать при правке файлов внутри `БИОГРАФИИ/Джон Гилл/`.
