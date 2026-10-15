# Аудит ветки Research / НЗ — 2026-10-12

## Короткий ответ: что осталось

**Исправления этой ветки подготовлены к owner review для research merge.**
Не требуется выдавать богословский вердикт или снимать публикационные HOLD.
**Весь репозиторий не объявляется all-green:** один старый live-remote
retirement contract остаётся FAIL и требует отдельного решения владельца.
Публикация не одобрена: `BLOCKED` / `PUBLICATION_HOLD`.

| Уровень | Итог | Что делать |
|---|---|---|
| NT-код, SSOT, карточки и три связанные root-проверки | 14/14 PASS; 62 регрессионных теста | Review исправлений и merge только владельцем |
| Полный inventory репозиторных диагностик | 76/77 PASS, без изменения дерева | Отдельно решить legacy branch/archive drift, не удалять активные ветки |
| GitHub governance | main protection=false на момент аудита | Владелец/admin: решение по issue #196 и protection/check policy |
| Старый PR #212 | OPEN, другая ветка, старые результаты | Не мержить вместе с новой аудитной веткой; владелец решает supersession/closure |
| Публикация / Product | NOT READY, разрешения не даны | Отдельный rights/locator/series gate; полные корпуса в Git не переносить |

## 1. Scope и правила

Рабочая ветка — `arena/1f778815-research`; исходный session HEAD `731ae451`.
Main интегрирован; на 2026-10-12 `origin/main=50f1886a1d8a5569d6c244bee9287d7158bac55d`
является предком ветки. Root и parent authority не заменяются новой NT authority.
Прочитаны действующие `AGENT_RULES.md`, `CURRENT_AUTHORITY.md`, registry/evidence/
custody policies, topic authority/навигация и исторический NT-бриф; проверены
CI/validator inventory и связанные закрытые/открытые работы.

**Полнота здесь:** все 77 проверки восстановленного репозиторного inventory;
ручной содержательный аудит изменённого NT-слоя, его родительских цитат/реестра,
инструментов, acquisition и merge-контрактов. Это **не** повторная независимая
экзегеза каждого ранее слитого файла других корпусов или повторное получение
всех их внешних первоисточников. Product и ProductHeart использованы read-only,
не модифицированы. `.github/` и чужие authority validators не переделывались.

## 2. Существенные ошибки, которые исправлены

1. **Проверки пропускали реальные дефекты.** Убраны master/wildcard fallbacks,
   substring/glued-word/cross-verse matches, успех при missing/mismatch,
   удалении primary block или недостающей методике. Runner больше не прячет
   диагностику `head`/`tail`/`grep` и не исключает любое Genesis-падение.
2. **SSOT осей состояния.** Evidence/access/locator/rights/publication раздельны;
   canonical enums, исторические значения явно SUPERSEDED. Ни один из десяти
   commit/content pins не заменён. Добавлен отдельный filename digest; bytes
   означают содержимое файлов, не размер каталога. Все десять fresh codeload
   snapshots воспроизведены вне Git, включая Python 3.11.2 safe extraction.
3. **Методические gaps.** Закрыты исходные 147 пропусков syntax/context/OT
   блоков, исправлены неканонические оси и удалённая agents-ссылка. Сейчас
   90 непустых method cards, 89 text cards с explicit readings; служебные
   offer-разделы не маскируют отсутствие primary quotation. Нейтральное `N`
   и отрицательный результат Иакова остаются допустимыми, не выдуманы две модели.
4. **Грамматика и выводы.** Одно pi-an в Ин 6:37; номинатив katara в Гал 3:13;
   цитата Втор 21:23, не 27:26; артикли 1 Ин 2:2/4:10; один modifier в Откр 5:9.
   Настоящее время не автоматически непрерывность; артикль не исключает
   дистрибутивности; parallel indefinite/all не исключает широкий референт;
   particle ara не доказывает тождество всех спасительных объёмов.
5. **Производные счётчики.** Исправлены blood case counts, anti constructions,
   pantes NPM/VPM и 31 verse / 33 kosmos-token distinction. MT хранит слитные
   артикли Ис 53 в отдельных empty-surface slots; они есть в двух из трёх
   rab-случаев. Kpr `lex_utf8=122` — 102 verbs + 20 nouns, не 122 глагола.
6. **Ложные LXX-нули.** Ноль prefix не является нулём леммы. S5 содержит
   inflected simplex hilas и katallag verbs и apolytroseos noun. Положительные
   цифровые формы закреплены в тестах; old zero/verb/POS assertions отозваны,
   без молчаливой правки исходника. Полная LXX-лемматизация не заявляется.
7. **Колляции и аппарат.** XML-комментарии не считаются активными: 9997 raw
   file-unit rows вместо 9999, Марк включён дважды; 9850 в предпочтительном
   неперекрывающемся наборе. Невозможный Mark 28:8 quarantined, не перенумерован
   догадкой. Literal siglum tokens/compiled witnesses/qualifiers — не голоса
   независимых манускриптов. Unit absence не означает all-witness agreement.
   S7 не цитирует NA в Евр 2:9; NA header 27/1979 конфликтен, silence не agreement.
8. **История/источники.** Дорт — A3 для собственного синодального утверждения,
   не Библия первого порядка. Использован уже существующий английский 1840
   parent record; будущая веб-дата 2026-10-13, три копии и неизвестный PD-перевод
   сохранены как UNVERIFIED/SUPERSEDED. Parent OPC partial reading не потеряно.

Подробности — [`00_`](00_NT_AUTHORITY_2026-10-07.md),
[`11_`](11_NT_LXX_COLLATION.md), [`12_`](12_NT_TEXTUAL_APPARATUS.md),
[`13_`](13_DORT_HISTORICAL_CONTROL.md), [`SSOT`](data/nt-corpus-v1.json).
Формальный method PASS — structural floor, не сертификат хорошей экзегезы.

## 3. Проверено

| Проверка | Зафиксированный результат |
|---|---|
| Fresh download / extraction / unchanged content pins | 10/10 PASS; данные/сырые лицензии вне Git |
| Unit + pinned-data negative regressions | 62/62 PASS; в том числе wrong-book, missing input, unexpected word, tree mutation |
| Полный NT runner + three root checks | 14/14 PASS, tree unchanged; Genesis настоящий PASS, не baseline exemption |
| Required method inventory | 90 method / 89 text / 94 axis sections; 0 missing/empty blocks, 0 broken links |
| S1/TR/S7/S8 controls | 27 word comparisons; 5 S8 positives; S7 explicit attribution verified |
| Selected heading apparatus census | 174 verses / 89 app positions / 139 records / 85 no encoded app, не no variation |
| MT/LXX pairs | 48 probes: 47 читаемых + 1 зарегистрированно отсутствующий стих; unexpected missing fails |
| Repository diagnostic inventory | 76/77 PASS; includes read-only Product/Gill/Heart checks |
| Product snapshots | Product `efaf2a51b1fcc7b7d3f8c9558ecb5acf849df3b3`; Heart `0fbe7d1ead9ebd1bea867418e254da438ec63329` |

Предотчётный fixed-tree content SHA256:
`c3bea117dd39014ffc38bda82b9176e1f00a04ca3069f9d96609905885b45854`,
repository diagnostic HEAD `f25c0d2190b1b9677a6a7bb656663f771c0d1457`.
Старый 76/77 diagnostic baseline не выдаётся за новый receipt: проверки
повторены после исправлений последовательно. Финальное дерево с этим отчётом
также проверяется тем же runner; private raw logs не публикуются.

## 4. Единственный общий FAIL и CI-граница

`validate_branch_retirement_authority.py` сравнивает live refs/archive со старым
August retirement contract. FAIL включает active remote branch-set drift,
forensic archive head drift и отсутствующие recorded commit/ledgers. Он был
красным до NT-исправлений и остаётся красным после них; **код 1 не замаскирован**.
Это не разрешение удалить чужие/активные branches или переписать evidence manifest.
Владелец должен решить актуальность governance/archive contract отдельно.

GitHub CI — отдельное измерение: существующий integrity workflow не запускает
новый NT-suite. Local 14/14 и 62 теста не называются «NT CI SUCCESS».
Решение о подключении команды в CI — владельцу; нельзя выкладывать raw logs
study-only corpora как публичные artifacts. Branch protection не изменялось.

## 5. Не проверено / не разрешено

Полный NA28/UBS5, физические рукописи/полный BHS-LXX apparatus, первичный
catalogue qualifier/codex mapping, полная LXX lemma/POS/semantic annotation,
визуальная сверка S5 Deut 21:23 (digital merge/OCR conflict), бумажная страница
локального Dort 1840 record, самостоятельное повторное получение полного OPC.
Выполненные probes не превращают эти вопросы в закрытые.

Никакого Product write, выпуска, нового богословского вердикта, owner approval
или снятия `EVIDENCE_HOLD`/`PUBLICATION_HOLD`. Современные ограничения S1/S5/S6/S8
и secondary work учитываются отдельно от research merge.

## 6. Воспроизведение и решение владельца

```bash
# Без сети; missing corpus — FAIL, не auto-fetch.
bash ИСКУПЛЕНИЕ/nt/tools/run_all_checks.sh
# Только если надо получить missing snapshots вне checkout:
python3 ИСКУПЛЕНИЕ/nt/tools/nt_sources.py --fetch
```

**Владельцу:** review новую ветку/PR вместо прежних NT-результатов #212;
принять отдельное решение по legacy retirement/governance и CI coverage;
после review merge выполнять владельцем. Публикацию обсуждать отдельным gate,
а не ставить условием догматический итог этой research-ветки.
