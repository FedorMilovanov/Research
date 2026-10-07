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
8. Локаторы PD 2026-10-07: Оуэн Book IV (`14`, CCEL TXT); Кальвин Inst. III.24.15–17 (`15`, Beveridge chunks 330–331); Дорт II.1–9 + Rejection I–VII как карта статей (CRCNA reading copy; Schaff PD chunk не пойман). Drive PDF Calvin 45 MB / Owen 42 MB — extraction cap 25 MB, страница Goold/Beveridge в *этих* файлах unchecked.

## 2. Что не доказано

- Ни одна читательская статья не готова.
- Мюррей RU HTML доступен для private study, но **не quote-safe** для Product (unnamed translation, нет page locator, copyright). Пакер, Gibson, Morris, Stott, Letham, Berkhof, Bavinck EN — по-прежнему без полного объекта.
- PD-копии Owen/Calvin/Goodwin/WCF имеют `accessState=acquired-copy`, но `locatorState=unchecked` до постраничной сверки нужных локусов.
- Product-route `/iskuplenie/` не предложен к внедрению.
- Корневой Research stage registry этот корпус ещё не включает; это сознательно. Смена root authority этим стартом не производится.

## 3. HOLD

| Флаг | Объект | Почему |
|---|---|---|
| `RIGHTS_HOLD` | Murray RAA; Packer 1959 intro; *From Heaven He Came and Sought Her*; Morris; Stott; Letham; Berkhof; Bavinck English; Grudem; Frame; Schreiner | авторское право XX–XXI вв. |
| `ARCHIVE_HOLD` | Packer 1959; Gibson 2013; Morris; Stott; современные ST | полного объекта нет. Murray RU HTML — исключение: тело есть |
| `LOCATOR_HOLD` | Owen Goold page в Drive *Works* PDF (42 MB); Calvin Drive PDF page (45 MB); Calvin II.16–17; Schaff Dort page; WCF 8 | копии/TXT есть; страница издания не сверена. Содержание Book IV и Inst. III.24 — в `14`/`15` |
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

1. Добить Оуэн Book IV Ch. III (1 Тим. 2:4) прямым CCEL TXT-чанком; Schaff Creeds III — чанк Head II (PD цитата вместо CRCNA dump).
2. Calvin II.16–17 nature — следующий Beveridge чанк. Drive PDF >25 MB не извлекать целиком.
3. Бумажный Banner/Eerdmans RAA и NICNT Romans — по желанию владельца, в `02`. CW / Packer 1959 не пиратить.
4. Не начинать Product HTML. `EVIDENCE_HOLD` на «ограниченное искупление доказано» остаётся.

## 6. Связь с root

Этот файл не заносится в `data/research-authority-registry-v1.json` как root. Корневой owner остаётся `00_RESEARCH_CURRENT_AUTHORITY_2026-08-02.md`. Навигационная ссылка в README допустима как corpus entrypoint.
