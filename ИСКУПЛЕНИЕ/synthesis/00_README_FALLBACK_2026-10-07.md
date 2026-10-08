# README — fallback-хранилище под-корпуса synthesis (агент №4)

**Дата:** 2026-10-07
**Ветка сессии:** `arena/5fe5b33f-research` (от main `eee4624`)
**Статус:** `RESEARCH / NOT PUBLISHED / PUBLICATION_HOLD` — на всё под-корпус.

> **Статус 2026-10-08:** папка больше не является единственным домом. Файлы перенесены в Git `ИСКУПЛЕНИЕ/synthesis/` сессией-координатором (ветка `arena/dddc1326-research`, PR #209); копии на Drive обновлены по канону с сохранением ID. Ниже сохранено как история: почему материалы сначала оказались на Диске и что агент №4 успел / не успел сделать сам. Ветка агента `arena/5fe5b33f-research` на GitHub не существует (API 404) — поэтому перенос сделан в ветке координатора.

## Почему файлы здесь, а не в Git

Вся песочница E2B сессии (bash, read_file, write_file, edit_file, start_process, present_file) не инициализировалась **~40 минут**: 16+ попыток с разными cwd, путями и паузами — каждый вызов возвращает `Failed to initialize E2B workspace`. По правилу брифа «невозможно» заявляется только после 5+ обходов с доказательством — доказательство здесь.

Поэтому deliverables записаны в Google Drive, в папку корпуса (`07 — СЕРИЯ «ИСКУПЛЕНИЕ»`), как **fallback**. Drive presence **не снимает** ни один HOLD и **не заменяет** Git-канон.

## Что здесь лежит (канонные пути в Git)

| Drive-файл | Канонный путь в Git | Drive ID |
|---|---|---|
| `00_README_FALLBACK_2026-10-07.md` | (этот README; в Git не нужен, но полезен как история) | `1_KVxtWTpmuUeYVzngWxL0x3_EwjOK30h` |
| `00_SYNTHESIS_AUTHORITY_2026-10-07.md` | `ИСКУПЛЕНИЕ/synthesis/00_SYNTHESIS_AUTHORITY_2026-10-07.md` | `101_Q15IzPajiATl86OsaKUow0jArl58h` |
| `01_SERIES_PLAN_AND_ARTICLE_COUNT.md` | `ИСКУПЛЕНИЕ/synthesis/01_SERIES_PLAN_AND_ARTICLE_COUNT.md` | `1wjYa-bNbC_mrYScOSOavUCt1brG0So9p` |
| `02_CONFLICT_LEDGER.md` | `ИСКУПЛЕНИЕ/synthesis/02_CONFLICT_LEDGER.md` | `1Vn9Vzdiri98PgdehkPGAMsBoiIA_F7gX` |
| `03_PRACTICAL_AND_PASTORAL_NOTES.md` | `ИСКУПЛЕНИЕ/synthesis/03_PRACTICAL_AND_PASTORAL_NOTES.md` | `1Tbd2IsZ1Ls8gLwLW2TP4GSQBTP5IYNQH` |
| `drafts/01_what-is-atonement.md` | `ИСКУПЛЕНИЕ/synthesis/drafts/01_what-is-atonement.md` | `1MWqCtUztQF_jfI8ffIYX5aYjmQ5lq35L` |
| `data/synthesis-corpus-v1.json` | `ИСКУПЛЕНИЕ/synthesis/data/synthesis-corpus-v1.json` | `1ehznH7G-2etlICzPokOcaAYpQwHVVxqO` |

**Важно при переносе в Git:** файл `data/synthesis-corpus-v1.json` записан с **UTF-8 BOM** (ограничение коннектора: JSON-содержимое иначе парсится как объект). При переносе удалить BOM первой строкой (`sed -i '1s/^\xEF\xBB\xBF//' …` или вручную). Остальные файлы — чистый UTF-8 без BOM.

## Что НЕ сделано (и почему)

- **Нет файлов в Git-репозитории** — песочница недоступна.
- **Не запущены три валидатора** (`scripts/validate_research_root_authority.py`, `scripts/validate_research_stage_closure.py`, `scripts/validate_genesis6_authority_manifest.py` — ожидаемый локальный FAIL Genesis 6 на мелком клоне без `b654c537`); baseline на чистом HEAD не снят.
- **Нет commit / push / PR** — ветка `arena/5fe5b33f-research` отсутствует на GitHub (API 404, проверено).
- **CI не проверен** — PR не открыт.

## Что делать владельцу

1. **Восстановить песочницу** (перезапуск сессии / reconnect E2B) — единственное блокирующее действие.
2. Перенести 6 файлов по путям из таблицы в Git (BOM у JSON снять).
3. Прогнать три валидатора на чистом HEAD (baseline), затем на ветке; diff vs baseline.
4. Commit (по одному на шаг, ≤ ~400 строк, trailer `Co-authored-by: arena-agent <297053741+arena-agent@users.noreply.github.com>`), push в `arena/5fe5b33f-research`, открыть PR.
5. Не снимать `EVIDENCE_HOLD` / `PUBLICATION_HOLD` без явного решения.

## Что сделано (содержательно)

- Прочитан весь необходимый корпус: `AGENT_RULES.md`, `ИСКУПЛЕНИЕ/00_`–`15_` (все 16 файлов + `data/atonement-corpus-v1.json`), `.github/workflows/` (полный список), `scripts/validate_*.py` (ключевые: root authority, stage closure, genesis6).
- Составлена общая карта тезисов (T1–T8) по слоям с осями и статусами.
- Составлен план серии: минимум 4 / цель 13 / потолок 16–18 статей; первая статья — «Что такое искупление».
- Составлен реестр конфликтов C-01…C-15 (снято молча: 0).
- Написаны пастырские заметки с правилом «как не сломать совесть» с обеих сторон.
- Написан первый черновик статьи (слой A1) со шапкой `STATUS: DRAFT / NOT PUBLISHED / PUBLICATION_HOLD`, без единой цитаты современных авторов, Писание — Синодальный с локаторами-стихами, исповедания — по номерам статей.
- Записан SSOT `synthesis-corpus-v1.json`.
