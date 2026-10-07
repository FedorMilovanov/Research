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
6. Джон Мюррей, *Redemption Accomplished and Applied* (1955): владелец загрузил русский HTML-дамп `s3516.htm.zip`. Тело 1955 **полное** (предисловие + 15 глав). Переименован и лежит в Drive `02` как `PRIVATE_STUDY_ONLY`. `ARCHIVE_HOLD` на наличие текста снят. `RIGHTS_HOLD` + `PUBLICATION_HOLD` на цитаты остаются. Английский Banner/Eerdmans с страницами по-прежнему отсутствует. См. `09_…INTAKE…` и `10_…ARGUMENT_MAP…`.
7. HARD-тексты объёма: карта Мюррея **вне** RAA (`11`), рабочие карточки локусов (`12`), Дорт II / Кальвин / Оуэн (`13`). Закрыто как research-map, не как вердикт. 1 Тим. 2:4 и 2 Пет. 2:1 у Мюррея по-прежнему не разобраны; брошюра *The Atonement* §V — конденсат I.4; OPC 1948 закрывает ось offer (2 Пет. 3:9), не extent.
8. Локаторы PD 2026-10-07: Оуэн Book IV (`14`, CCEL TXT chunks 70–90; 1 Тим. 2:4 = 80–81; **2 Пет. 2:1 = 87–88**); Кальвин Inst. II.12 / II.16 / II.17 / III.24.15–17 (`15`, Beveridge 155 / 168 / **176–177** / 330–331); Дорт II.1–9 + Rejection I–VII (CRCNA reading copy **и** Schaff Latin chunk 165). Drive PDF Calvin 45 MB / Owen 42 MB — extraction cap 25 MB, страница Goold/Beveridge в *этих* файлах unchecked.
9. **Локаторы PD, волна 2026-10-07b.** Schaff/CCEL даёт Дорт **только по-латыни** — проверено по чанкам **163** (Head I, Rejectio), **164** (подписи делегатов), **165** (Head II + Rejectio): **английской колонки не существует**. Взамен выбрано английское PD-издание Канонов: **Scott 1841** (*The Articles of the Synod of Dort…*, пер. Thomas Scott, 1841; archive.org `articlesofsynodo1841syno`). Head II = **с. 282–286** (II.1 = 282, II.3 = 283, II.5 = 284, II.8 = 285); **Rejectio I–VII = с. 287–292** (I — 287, II — 288, III — 288–289, IV — 289, V — 290, VI — 291–292, VII — 292). Привязка: `search-inside` OCR + `page_numbers.json` (confidence 96) + оглавление издания. Полный английский текст артикулов I–IX **и** Rejectio I–VII перенесён в [`15` §B.5](15_CALVIN_III24_AND_DORT_II_LOCATORS.md). `accessState = transcribed-from-OCR`: текст набран с OCR-выдачи, артефакты распознавания сохранены, сверки с изображением страницы **не было**. [`15` §B.4](15_CALVIN_III24_AND_DORT_II_LOCATORS.md)
10. **WCF 8 локализован (2026-10-07b):** Schaff/CCEL `creeds3.txt` **chunks 182–183** = Chapter VIII *Of Christ the Mediator / De Christo Mediatore*, двуязычная колонка EN+LA; якоря 8.1 / 8.5 / 8.6 / 8.8 с номерами сносок Шаффа. Drive PDF WCF `1VSp4vU56X8uuYrp2SERkp2p0BRk-vQq4` = **16 179 601 bytes**, `read_file_text` → `extraction_status: empty` — скан без текстового слоя; страница этого файла не извлекаема, ретраить запрещено. [`15` §D](15_CALVIN_III24_AND_DORT_II_LOCATORS.md)
11. Quote-safe Product по-прежнему **NO**: английское PD-издание Дорта выбрано, но item-level сверки OCR со страницей не было; по WCF EN решение не принималось. `EVIDENCE_HOLD` и `PUBLICATION_HOLD` не сняты; Product HTML не начинался (см. §5).

## 2. Что не доказано

- Ни одна читательская статья не готова.
- Мюррей RU HTML доступен для private study, но **не quote-safe** для Product (unnamed translation, нет page locator, copyright). Пакер, Gibson, Morris, Stott, Letham, Berkhof, Bavinck EN — по-прежнему без полного объекта.
- PD-копии Owen/Calvin/Goodwin/WCF имеют `accessState=acquired-copy`, но `locatorState=unchecked` до постраничной сверки нужных локусов. Исключение после волны 2026-10-07b: **текст** WCF 8 проверен по Schaff/CCEL (chunks 182–183), а страница Drive PDF WCF закрыта как не извлекаемая (скан без текстового слоя). По Owen/Calvin/Goodwin изменений нет.
- Product-route `/iskuplenie/` не предложен к внедрению.
- Корневой Research stage registry этот корпус ещё не включает; это сознательно. Смена root authority этим стартом не производится.

## 3. HOLD

| Флаг | Объект | Почему |
|---|---|---|
| `RIGHTS_HOLD` | Murray RAA; Packer 1959 intro; *From Heaven He Came and Sought Her*; Morris; Stott; Letham; Berkhof; Bavinck English; Grudem; Frame; Schreiner | авторское право XX–XXI вв. |
| `ARCHIVE_HOLD` | Packer 1959; Gibson 2013; Morris; Stott; современные ST | полного объекта нет. Murray RU HTML — исключение: тело есть |
| `LOCATOR_HOLD` | Owen Goold page в Drive *Works* PDF (42 MB); Calvin Drive PDF page (45 MB); **печатная страница тома Schaff по WCF 8**; **печатная страница тома Schaff по Дорту**; **сверка транскрипции Scott 1841 с изображением страницы** (`15` §B.5 — ручной перенос OCR) | копии/TXT есть; страница издания не сверена. Содержание Book IV (включая 2 Пет. 2:1), Inst. II.12/16/17/III.24, Dort Latin, Dort EN (артикулы I–IX + Rejectio I–VII, с. 282–292), WCF 8 EN+LA — в `14`/`15` |
| `LOCATOR_HOLD` (закрыт как вопрос, не как «найдено») | Schaff Dort **English** column; WCF 8 page в нашем Drive PDF | EN-колонки в Schaff/CCEL **нет** (чанки 163–165 — латынь, проверено). Drive PDF WCF = скан без текстового слоя (16 179 601 bytes, `extraction_status: empty`) — страница принципиально не извлекаема, не ретраить и не угадывать. Оба закрыты **заменой**: Scott 1841 pp. 282–286 (Дорт EN) и Schaff chunks 182–183 (WCF 8 EN+LA). Ось «страница бумажной книги» остаётся открытой |
| `PUBLICATION_HOLD` | вся серия | research ≠ publication |
| `EVIDENCE_HOLD` | любой тезис об «ограниченном искуплении» как о единственном библейском выводе | экзегеза и honest opposing case ещё не закрыты |

## 4. Запрещённые формулировки на этом этапе

- «Мы уже доказали ограниченное искупление».
- «Кальвин учил тому же, что Оуэн, слово в слово».
- «Всеобщее искупление = либерализм / неверие».
- «Мюррей quote-safe / готов для сайта».
- «Владельческий HTML = английский критический текст».
- «Серия закрыта / готова на сайт».
- Любая прямая цитата Мюррея, Пакера, Гибсона, Морриса, Стотта без легального экземпляра и локатора.

## 5. Следующий допустимый lane

1. ~~Schaff EN колонка Дорта~~ — **закрыто**: её не существует (чанки 163–165 = латынь); выбрано Scott 1841, с. 282–286. ~~WCF 8 page в Drive PDF~~ — **закрыто**: скан без текстового слоя; текст WCF 8 локализован (Schaff chunks 182–183). Дальше по этой оси: печатная страница тома Schaff 1919 (archive.org, PD) и **item-level сверка транскрипции Scott 1841 с изображением страницы** (без неё цитаты в Product невозможны). Не резать Calvin/Owen PDF >25 MB целиком.
2. Banner/Eerdmans RAA — по желанию владельца в `02`. Packer 1959 не пиратить.
3. Не начинать Product HTML. `EVIDENCE_HOLD` остаётся. Первая читательская статья — «Что такое искупление», не TULIP. Не объявлять 1 Тим. 2:4 / 2 Пет. 2:1 закрытыми *Мюрреем*.

## 6. Связь с root

Этот файл не заносится в `data/research-authority-registry-v1.json` как root. Корневой owner остаётся `00_RESEARCH_CURRENT_AUTHORITY_2026-08-02.md`. Навигационная ссылка в README допустима как corpus entrypoint.
