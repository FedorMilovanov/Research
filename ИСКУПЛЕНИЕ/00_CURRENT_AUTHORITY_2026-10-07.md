# Искупление — current authority

**Дата:** 2026-10-07  
**Authority ID:** `ATONEMENT-CORPUS-AUTHORITY-2026-10-07`  
**Статус:** `CURRENT / CORPUS-SPECIFIC / ACTIVE RESEARCH / NOT PUBLICATION-READY`  
**Родительская root-authority:** [`CURRENT_AUTHORITY.md`](../CURRENT_AUTHORITY.md) → `00_RESEARCH_CURRENT_AUTHORITY_2026-08-02.md`  
**Evidence policy:** [`data/repository-evidence-policy-v2.json`](../data/repository-evidence-policy-v2.json)  
**Custody:** [`data/artifact-custody-policy-v2.json`](../data/artifact-custody-policy-v2.json)

Этот файл — corpus-specific owner evidence graph отдела «Искупление». Он **не** конкурирует с корневым Research root и **не** разрешает публикацию на `gospod-bog.ru`.

## 1. Что доказано на старте

1. Отдел создан в Research: каталог `ИСКУПЛЕНИЕ/`.
2. Рабочая архитектура серии зафиксирована как **изменяемая**: число статей может расти, порядок может меняться, флагман не заморожен.
3. Введение обязано начинаться с определения искупления и терминов, а не с лозунга «ограниченное искупление».
4. На Google Drive создан корпус [`07 — СЕРИЯ «ИСКУПЛЕНИЕ»`](https://drive.google.com/drive/folders/1VULVPNq4DbBFS5KvBDpSkJOlx4jbEQAV).
5. В PD-библиотеку скопированы уже имевшиеся public-domain объекты:
   - Owen, *Works* — [`1gfKY8eXGhV-HL5O4u1tVVcCRYNKx-dQY`](https://drive.google.com/file/d/1gfKY8eXGhV-HL5O4u1tVVcCRYNKx-dQY/view);
   - Calvin, *Institutes* — [`1DLcwFWyRXtTDBzdS_tHptGkoItoumVWZ`](https://drive.google.com/file/d/1DLcwFWyRXtTDBzdS_tHptGkoItoumVWZ/view);
   - Goodwin, *Works* — [`1o9T7mIQxIH3ZB2EVc2hQsKdjEQM3SW-M`](https://drive.google.com/file/d/1o9T7mIQxIH3ZB2EVc2hQsKdjEQM3SW-M/view);
   - Westminster Confession — [`1VSp4vU56X8uuYrp2SERkp2p0BRk-vQq4`](https://drive.google.com/file/d/1VSp4vU56X8uuYrp2SERkp2p0BRk-vQq4/view).
6. Джон Мюррей, *Redemption Accomplished and Applied* (1955): библиография, TOC и маршрут легальной добычи зафиксированы. **Полный PDF не размещён.** `RIGHTS_HOLD` + `ARCHIVE_HOLD`. Custody = `LINK_ONLY`, пока владелец не положит легально купленный экземпляр.

## 2. Что не доказано

- Ни одна читательская статья не готова.
- Ни один современный учебник (Мюррей, Пакер intro к Owen, Gibson & Gibson, Morris, Stott, Letham, Berkhof, Bavinck EN) не quote-safe.
- PD-копии Owen/Calvin/Goodwin/WCF имеют `accessState=acquired-copy`, но `locatorState=unchecked` до постраничной сверки нужных локусов.
- Product-route `/iskuplenie/` не предложен к внедрению.
- Корневой Research stage registry этот корпус ещё не включает; это сознательно. Смена root authority этим стартом не производится.

## 3. HOLD

| Флаг | Объект | Почему |
|---|---|---|
| `RIGHTS_HOLD` | Murray RAA; Packer 1959 intro; *From Heaven He Came and Sought Her*; Morris; Stott; Letham; Berkhof; Bavinck English; Grudem; Frame; Schreiner | авторское право XX–XXI вв. |
| `ARCHIVE_HOLD` | те же | полного легального объекта в корпусе нет |
| `LOCATOR_HOLD` | Owen *Death of Death* внутри *Works* PDF; Calvin II.16–17; Dort II; WCF 8 | копия есть, страница/том не сверены |
| `PUBLICATION_HOLD` | вся серия | research ≠ publication |
| `EVIDENCE_HOLD` | любой тезис об «ограниченном искуплении» как о единственном библейском выводе | экзегеза и honest opposing case ещё не закрыты |

## 4. Запрещённые формулировки на этом этапе

- «Мы уже доказали ограниченное искупление».
- «Кальвин учил тому же, что Оуэн, слово в слово».
- «Всеобщее искупление = либерализм / неверие».
- «Мюррей выложен на Drive полным текстом».
- «Серия закрыта / готова на сайт».
- Любая прямая цитата Мюррея, Пакера, Гибсона, Морриса, Стотта без легального экземпляра и локатора.

## 5. Следующий допустимый lane

1. Закрыть словарь и библейский корпус как research-map, не как статью.
2. Добыть PD-тексты: Owen *Death of Death* (CCEL/Archive), Hodge ST III, Dabney, Shedd, Warfield PD articles, Anselm *Cur Deus Homo*, Athanasius *De Incarnatione*, Canons of Dort (Schaff), 1689.
3. Владелец кладёт легальный Murray RAA в Drive `02 — COPYRIGHT…`, после чего снимается только `ARCHIVE_HOLD` на этот объект; `RIGHTS_HOLD` на публикацию цитат остаётся до item-level решения.
4. Не начинать Product HTML.

## 6. Связь с root

Этот файл не заносится в `data/research-authority-registry-v1.json` как root. Корневой owner остаётся `00_RESEARCH_CURRENT_AUTHORITY_2026-08-02.md`. Навигационная ссылка в README допустима как corpus entrypoint.
