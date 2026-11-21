# Очередь публикационного шлюза (18.11.2026)

**Что это.** Не новая политика и не разрешение. Это снятая по правилу композиции картина
product-side очереди: какие записи вообще существуют, в каком состоянии каждая, какие удержания
на ней висят и что именно требуется, чтобы запись могла сдвинуться.

**Зачем.** Класс `RIGHTS_HOLD` / `PUBLICATION_HOLD` — самый крупный открытый класс в репозитории
(2 573 и 1 448 канонических упоминаний). Он заблокирован не работой агента, а решением человека.
Пока решение не сформулировано по объектам, «закрыть» его нельзя — можно только сделать
очередь явной, чтобы решение принималось по списку, а не по памяти.

Физические права берутся из `data/physical-rights-ledger-2026-08-01.json` (7 записей, `driveCheckedAt`
2026-08-01) дословно: `rightsState` и `publicationEligible` переносятся, а не пересказываются.

**Источник и правило.** `data/public-projection-current-2026-08-02.json`:
база `data/public-projection-queue-2026-08-01.json` + оверлеи, применённые по `record id`
(правило композиции прямо запрещает читать базу без оверлеев). Снимок:
`data/publication-gate-queue-v1.json`, снят `scripts/publication_gate_status.py`.

## 1. Состояние: 10 записей, `PROMOTE` = 0

| Запись | Эффективное состояние | Удержания | Права (`physical-rights-ledger`) |
|---|---|---|---|
| `heart-series-source-closure` | REFERENCE | PUBLICATION | записи нет |
| `osk-power-dark-side-standalone` | REFERENCE (было BLOCKED; заменено оверлеем `A06-OSK-CURRENT-PROJECTION-2026-08-02`) | PUBLICATION | записи нет |
| `genesis6-enoch-hard-texts` | REFERENCE | PUBLICATION | записи нет |
| `source-library-editorial-40-pdf` | REFERENCE | RIGHTS | `REFERENCE_ONLY_ITEM_REVIEW_REQUIRED`, `publicationEligible=false` |
| `bratsky-listok-1906-1910` | BLOCKED | ARCHIVE + LOCATOR + RIGHTS + PUBLICATION | `SCAN_PAGE_AND_REUSE_REVIEW_REQUIRED`, `false` |
| `baptist-archive-v156` | BLOCKED | ARCHIVE + LOCATOR + RIGHTS + PUBLICATION | `ARCHIVE_CONTENT_AND_REUSE_NOT_OBTAINED`, `false` |
| `gill-archive-families` | BLOCKED | ARCHIVE + LOCATOR + RIGHTS + PUBLICATION | `UNKNOWN`, 0 объектов Drive |
| `biblical-atlas-primary-strengthening` | BLOCKED | EVIDENCE + LOCATOR + RIGHTS + PUBLICATION | `UNKNOWN`, 0 объектов Drive |
| `source-library-ephemera-63` | BLOCKED | RIGHTS + PUBLICATION | `ITEM_LEVEL_REVIEW_REQUIRED`, `false` |
| `source-library-poet-portraits-45` | BLOCKED | RIGHTS + PUBLICATION | `IDENTITY_AND_ITEM_RIGHTS_REVIEW_REQUIRED`, `false` |

Счётчики сходятся с заявленными в current-authority: `BLOCKED=6`, `REFERENCE=4`,
`PROMOTE=0`, `total=10`. Ни одна запись не повышена; `promoteRequiresNoHolds` и
`promoteRequiresAllPhysicalRightsEligible` не выполнены ни для одной.

## 2. Что проверено машинно, а что нет

Проверено (`scripts/publication_gate_status.py --check`):
- каждая `sourceAuthorities`-ссылка существует в рабочем дереве — **0 отсутствующих**;
- каждая запись сопоставлена с `physical-rights-ledger`: **7 из 10** имеют запись, и у всех семи
  `publicationEligible=false`; у трёх (`heart-series`, `osk`, `genesis6`) записи прав **нет** — их
  `PUBLICATION_HOLD` нечем оценить, пока объект не заведён в реестр прав;
- каждый `rightsLedgerIds` встречается в репозитории — **0 потерянных**;
- снимок совпадает с пересобранной очередью; новая запись, исчезнувшая запись, смена
  `disposition`/`effectiveHolds`/`nextAction` или новая суперсессия оверлеем — валит проверку;
- `PROMOTE` с непустыми `holds` — валит проверку (политика это запрещает).

Не проверено и не утверждается: наличие файла authority — не права; упоминание `rightsLedgerId`
в тексте — не разрешение; `nextAction` перенесён дословно из очереди, а не придуман.

## 3. Что требуется от человека — по классам, а не по одному объекту

| Класс записи | Что снимет | Чего это не сделает |
|---|---|---|
| `REFERENCE` + только `PUBLICATION_HOLD` (`heart-series`, `osk`, `genesis6`) | Решение о публикации конкретной страницы: какая страница, какие цитаты, какая версия текста | Не снимает `EVIDENCE_HOLD` там, где он есть (у `osk` он был снят оверлеем, у остальных не значился) |
| `REFERENCE` + `RIGHTS_HOLD` (`source-library-editorial-40-pdf`) | Правовое основание по каждому PDF (лицензия, PD-статус издания, письменное разрешение) | Не делает тексты quote-ready: сверка формулировок — отдельная ось |
| `BLOCKED` + `RIGHTS`/`PUBLICATION` (`source-library-ephemera-63`, `…portraits-45`) | То же плюс решение по изображениям: право на воспроизведение скана/портрета | Не подтверждает, что изображение то самое — это `IMAGE_CHECK_PENDING` |
| `BLOCKED` + `ARCHIVE`/`LOCATOR`/`RIGHTS`/`PUBLICATION` (`bratsky-listok`, `baptist-archive-v156`, `gill-archive-families`, `biblical-atlas`) | Сначала архив и точные страницы, потом права: без объекта права не о чем решать | Не позволяет объявить комплекс «изученным целиком» — запрет записан в `forbiddenPromotion` каждой записи |
| Записи без правового ряда (`heart-series`, `osk`, `genesis6`) | Сначала завести объект в `physical-rights-ledger` с состоянием прав, затем решать о публикации | Не заменяет решение о публикации: даже с правами нужен ограниченный тезис и сверенная формулировка |

Отдельно: композицию очереди уже проверяет канонический `scripts/validate_public_projection_queue.py`
(включая сверку с физическим леджером прав). `publication_gate_status.py` не заменяет его, а даёт
**статус-снимок** и ловит дрейф относительно снимка — то, чего у валидатора нет.

## 4. Отдельная находка: корпуса вне очереди

В очереди **10** записей. Это значит, что корпуса, у которых записи нет (Чарнок и «Биографии»,
«Искупление», «Баптисты», SUNO, «Обратная сторона» за пределами `osk`, и др.), не могут быть
повышены **арифметически**: `productWriteRequiresPromoteRecord` требует записи, а записи нет.
Отсутствие записи — не «почти готово», а отсутствие решения. Первый шаг для любого такого
корпуса — создать запись очереди решением владельца, и только затем говорить о правах,
локуторах и формулировках.

## 5. Воспроизводимость

```bash
python3 -B scripts/publication_gate_status.py --summary   # состояние и удержания
python3 -B scripts/publication_gate_status.py --check     # снимок не разошёлся с очередью
python3 -B scripts/publication_gate_status.py -o /tmp/pg.json && cmp /tmp/pg.json data/publication-gate-queue-v1.json
python3 -B -m unittest discover -s scripts -p 'test_publication_gate_status.py'
```

Скрипт read-only: он не пишет в очередь, не меняет `disposition`, не снимает удержаний.
