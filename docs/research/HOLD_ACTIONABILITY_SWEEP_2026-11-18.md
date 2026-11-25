# HOLD: что можно дозакрыть машинно, а что требует владельца

**Дата прохода:** 2026-11-18  
**База:** `main @ 3c43a43ed71471a1f8c535f32f6ded15acb1ce47`
**Режим:** read-only инвентаризация репозитория и метаданных Drive; без загрузки/выгрузки файлов, без Product writes, без снятия прав и без публикационного решения.

## Короткий ответ

В глобальной карте остаются пять открытых осей. Агент может самостоятельно закрывать только проверяемую машинную неопределённость и узкие источниковые долги, для которых уже есть доступный объект. Нельзя самостоятельно закрыть права, подписать Research → Product handoff, сыграть роль независимого рецензента или объявить старое зеркало актуальным.

В этом проходе сделаны одиннадцать безопасных шагов:

1. три нетипизированных употребления `HOLD` / `FORBIDDEN` прочитаны по record key и исходной строке; неоднозначных *непрочитанных* употреблений теперь нет, но corpus SSOT не переписан;
2. проект коррекции `G3-PUB-015` включён в G3 integrity gate: гейт защищает две даты, source/claim IDs, состояние `NOT_SIGNED`, supersession старого вывода и сохранение трёх HOLD. Подпись владельца этим не подменяется;
3. после подтягивания current main точная custody-квитанция Чарнока зарегистрирована как узкое закрытие архивной оси для неизменяемого 17-source snapshot. Поздние правки, внешние факсимиле, научная приёмка, права и публикация не закрыты;
4. из #621 выборочно принят только заранее проверенный двухфайловый STEPBible-пакет: закреплённый ZIP повторно скачан и пересчитан, JSON воспроизведён, offline-гейт и негативные тесты включены в CI. Закрыта неопределённость «verify each subdataset», но не права на вложенные произведения;
5. три official-core carrier повторно получены по pinned Git commits и сверены с полной квитанцией. Истечение CI artifact больше не означает потерю единственного носителя; отдельный offline/network гейт теперь проверяет всю тройку. Внутренняя custody-копия, чтение содержимого и права этим не закрыты;
6. ошибочная shallow-clone инструкция из #621 исправлена до явного remote-tracking refspec и безопасных precondition/backup границ. Fresh depth-1 fixture доказывает восстановление точной верхушки без потери настоящей локальной правки; корпус и его HOLD этим не меняются;
7. после интеграции current main новый ED-09 архив Чарнока воспроизведён из точного source Git SHA: все source bytes, inner manifest и deterministic ZIP совпали с durable-квитанцией, а текущие Drive metadata совпали по object ID, размеру и server SHA-256. Независимая проверка переводов, права и публикация не закрыты.
8. устаревший Actions-custody пакет #621 получил окончательный disposition `REJECTED / SUPERSEDED`: его три пути не импортированы и не создают параллельный SSOT. Для bounded G3 cohort каноническими остаются assessment 38 items и exact receipt только для 8 original ZIP; остальные 30 прямо остаются несохранёнными, а права и публикация заблокированы.
9. после интеграции main два новых corpus-specific значения в Charnock ED-02 receipt получили контекстное proposal-only соответствие: `ED02_LOCATOR_HOLD` → `LOCATOR_HOLD`, `ED06_INDEPENDENT_REVIEW_HOLD` → `EVIDENCE_HOLD`. Receipt не переписан, review остаётся `0/12`, а vocabulary gate снова воспроизводится.
10. rights matrix #621 принята только после ремонта: exact proposal set снова совпал с current corpus records, runtime dependency на отклонённый inventory удалена, contradictory network boundary исправлена и защищена тестами. Матрица остаётся `PROPOSAL_NOT_AUTHORITY`; права, публикация и corpus SSOT не изменены.
11. два official-core prose blobs получили окончательный disposition без verbatim-импорта: carrier-view пересобран только из принятой machine receipt и проверяется на точное совпадение, mixed gap-note отклонена как смесь Drive/artifact наблюдений и owner-only HOLD решений. Carrier-воспроизводимость не стала authority над чужими corpus SSOT.

## 1. Пять глобальных открытых осей

| Ось | Что могу сделать сам | Что блокирует настоящее закрытие | Решение сейчас |
|---|---|---|---|
| `OPEN-HOLDS-VOCABULARY` | Измерять все значения, читать неоднозначные записи, проверять mapping и ловить drift | Нормализация полей в каждом corpus SSOT требует владельца корпуса и официального пересъёма | **Продвинуто, не закрыто** |
| `OPEN-PRIMARY-SOURCES` | Проверять уже названные доступные объекты, точные страницы, pinned GitHub bytes; писать отрицательные результаты | STEPBible-разбиение закрыто узко в HCR-32, а carrier-тройка — в HCR-33, но нет одного ограниченного списка остальных объектов; часть архивов/сканов недоступна в текущей сети или требует ручной визуальной проверки | **Продвинуто, HOLD** |
| `OPEN-RIGHTS` | Проверять наличие authority/rights record и внутреннюю непротиворечивость | Лицензия, договор, разрешение или решение владельца по конкретному объекту | **HOLD** |
| `OPEN-MIRRORS-BEHIND-HEAD` | Читать метаданные Drive и сравнивать размер/хеш с Git | На Drive нет текущих байтов трёх проверенных томов; новая загрузка не разрешена этим проходом | **HOLD** |
| `OPEN-INDEPENDENT-REVIEW` | Подготовить пакет, чек-лист и negative tests | Независимый человек-рецензент; агент не может рецензировать сам себя как внешняя сторона | **HOLD** |

## 2. Закрытая машинная неоднозначность `holds`

Инвентарь измеряет три употребления, которые нельзя было классифицировать по одному написанию:

| Record key | Контекст | Контекстное решение |
|---|---|---|
| `ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json#/stateCards/8/holds` → `HOLD` | исходная строка говорит `publication HOLD`; в записи уже есть `PUBLICATION_HOLD` | лишнего шестого HOLD нет; legacy-написание дублирует `PUBLICATION_HOLD` |
| `ИСКУПЛЕНИЕ/synthesis/data/synthesis-corpus-v1.json#/stateCards/1/holds` → `HOLD` | literal-marker fingerprint; в источнике это собирательное имя типизированных HOLD и статус недоступного издания | legacy status/marker; конкретные удержания уже перечислены рядом |
| `ИСКУПЛЕНИЕ/synthesis/data/synthesis-corpus-v1.json#/stateCards/3/holds` → `FORBIDDEN` | легенда C-10 прямо называет отсечённую формулировку | `status=FORBIDDEN`; не HOLD |

SSOT не переписан: `data/hold-value-mapping-proposal-v1.json` остаётся `PROPOSAL_ONLY`. `scripts/check_hold_vocabulary.py` теперь требует полного покрытия manual-употреблений по `(path, pointer, value)` и отказывает при пропавшем, лишнем или дублированном разрешении.

**Что реально закрыто:** отсутствие контекстной классификации.  
**Что не закрыто:** решение владельцев переписать non-canonical значения и переснять производные корпуса.

## 3. Чарнок: что уже закрыто и что ещё отстаёт

`data/charnock-editorial-book-receipt-v1-20261121.json` фиксирует отдельный неизменяемый пакет: 17 исходных файлов, включая 10 рабочих рукописей, editorial reader и review-документы; archive SHA-256 совпал после сырого Drive readback. Это закрывает архивную custody-ось **только для указанного snapshot**. Квитанция прямо исключает поздние правки, внешние факсимиле и независимую оценку перевода; `RIGHTS_UNKNOWN`, `publicationState=BLOCKED` и четыре содержательных HOLD остаются.

После #626 появился точный successor `data/charnock-editorial-book-receipt-v1-20261121-ed09.json`. Для `sourceGitSha=209c593fc23bcc32c29bc636b93bcf29d892e725` локально заново прочитаны все 17 members, воспроизведены inner manifest (`ed07ba1e0447919676988e21cbd6ab857286cac39712bef989f754cc820fa7a7`) и ZIP `1000295` B / SHA-256 `c4f719d5449e028568934ac2ea34a0defaf032ff06c007705aa4560f702e2efe`. Read-only запрос Drive вернул ровно один объект с заявленными ID, именем, размером и server SHA-256. Private ZIP в этом проходе не скачивался: raw readback зафиксирован исходной квитанцией. ED-09 audit и его тест не входят в 17 members; independent translation review остаётся `0/12`, rights `UNKNOWN`, publication `BLOCKED`. Это HCR-35, а не глобальное закрытие Чарнока.

Отдельно проверена актуальность рабочих зеркал 00/04/16. Поиск Google Drive выполнен только по метаданным и полному стабильному stem имени; содержимое не скачивалось и ничего не загружалось. Все три наиболее новые возвращённые записи уже известны репозиторному ledger/snapshot.

| Git-файл | Текущие Git bytes / MD5 | Возвращено кандидатов | Наиболее новый возвращённый кандидат | Вывод |
|---|---|---:|---|---|
| `00_README_AND_NAVIGATION.md` | `151534` / `9729bc4a4087051ad8f2b7a61ffc023f` | 37 | wave 40: `104472` / `21f0fc05522478e321af052ef43842cd` | не совпадает |
| `04_CHARACTER_MINISTRY_AND_THEOLOGY.md` | `406668` / `aaa904e78cb1c6af6c283cc2bcc029ea` | 25 | wave 38: `404419` / `bdbb2dd2304a50a9a271c56cb095769e` | не совпадает |
| `16_SERIES_ARCHITECTURE_AND_PERSONS_CHAIN.md` | `887094` / `d5d86542d0f6984845e8e820a057a0eb` | 24 | wave 40: `188283` / `9a85383d46b2cb1dff04d8480c9c7659` | не совпадает |

Это подтверждает `OPEN-MIRRORS-BEHIND-HEAD`, а не закрывает его. Поиск по имени не доказывает отсутствие переименованной копии; совпадение имени тоже не заменило бы хеш. Для закрытия нужна разрешённая загрузка текущих байтов, destination readback и новая квитанция. Права и публикация от этого всё равно не изменятся.

## 4. Ближайшие узкие задачи, где агент действительно поможет

1. **`G3-PUB-015`: почти готово, но не подписано.** Исследовательская поправка и машинный firewall готовы. Нужен явный `APPROVED`/`REJECTED` от Research owner; после него можно проверить точный Product SHA и отсутствие старой формулировки. До подписи `PRODUCT_PUBLICATION_HOLD` остаётся.
2. **STEPBible из карты #621 — выполнено как HCR-32.** Выборочно перенесены только `scripts/stepbible_subdataset_terms.py` и производный JSON; исходный ZIP `100920275` B / SHA-256 `6845fa9660c62301a0eec38c009ca34ef82647a9737529d8c56ac45d35182df0` повторно получен по pinned commit, а regenerated JSON структурно совпал. Карта различает семь верхнеуровневых наборов, ветвь CC BY-NC и ветвь CC BY-SA. Имена лицензий остаются заявлениями распространителя: `RIGHTS_HOLD`, `PUBLICATION_HOLD` и `PROMOTE=0` сохранены.
3. **Official-core carrier — выполнено как HCR-33; prose disposition — как HCR-39.** STEPBible-Data, `morphhb` и SBLGNT повторно скачаны по полным commit SHA; размеры и SHA-256 совпали для всей тройки. `scripts/check_official_core_reproducibility.py` проверяет квитанцию offline, требует exact generated Markdown и умеет повторить полный fetch/rehash. Ни один prose blob #621 не импортирован verbatim; mixed Drive/artifact/HOLD note отклонена. Это снимает только риск зависимости от истекающего CI artifact и неопределённость интеграции prose: архивы не объявлены прочитанными, сохранёнными на Drive или разрешёнными к публикации.
4. **Shallow-clone recovery note — выполнено как HCR-34.** Исходный документ не принят буквально: fetch без destination refspec заменён явным `refs/heads/$branch:refs/remotes/origin/$branch`, добавлены отказ для detached/неизвестной цели и аварийная копия tracked/untracked байтов. Локальный fixture создаёт fresh depth-1 single-branch clone и проверяет, что `reset --mixed` оставляет настоящую рабочую правку поверх точной remote-верхушки.
5. **Charnock ED-09 durable snapshot — выполнено как HCR-35.** `scripts/check_charnock_editorial_receipt.py --git-source` побайтово пересобирает ограниченный 17-source ZIP из точного Git commit и сверяет квитанцию; offline-режим и негативные тесты включены в CI. Это обновляет custody только для exact snapshot и не подменяет independent review, rights или publication authority.
6. **Actions custody из #621 — disposition закрыт как HCR-36.** Три dated source paths не импортированы. Их G3-часть замещена exact assessment и canonical 8-object receipt; гейт защищает IDs, bytes, digests, no-repack и обязательные HOLD. Это не объявляет сохранёнными остальные 30 items и весь Actions archive.
7. **Rights matrix из #621 — выполнено после ремонта как HCR-38.** Proposal-only список сверяется с current registries без параллельного inventory SSOT; датированные metadata не выдаются за current response. Это triage для владельца, а не rightsBasis, permission или снятие HOLD.
8. **Primary-source microbatch:** если владелец назовёт 1–3 конкретных locator/page HOLD, можно проверить их до конца и зафиксировать узкое отрицательное или положительное решение. Массовое «закрыть все источники» не воспроизводимо.
9. **Чарнок Drive mirror:** могу подготовить загрузочный manifest и последующий readback, но саму запись в Drive следует делать только после прямого разрешения на эти три текущих файла.
10. **Vocabulary intake current main — выполнено как HCR-37; migration остаётся owner-blocked.** Два новых Charnock labels покрыты в `PROPOSAL_ONLY` mapping без переписывания receipt. Field-by-field patch возможен только для выбранного corpus owner; глобальная автоматическая замена запрещена, потому что одинаковое слово `HOLD` уже имеет разные контекстные значения.

## 5. Жёсткие границы

- `PROMOTE=0` не менялся.
- `RIGHTS_HOLD` и `PUBLICATION_HOLD` не снимаются наличием, URL, хешем или Drive metadata.
- Никакие private bytes не скачивались и не переносились в Git.
- Никаких Drive writes, Product writes, слияния PR или deploy не выполнялось; current `main` интегрирован обычным merge-коммитом ветки.
- Новая классификация исправляет машинную неоднозначность, а не исторический/богословский вердикт.
