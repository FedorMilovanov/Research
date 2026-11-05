# Когда портфолио можно считать готовым

Документ отвечает на один вопрос: **при каких условиях про этот каталог можно честно
сказать «всё»** — и, наоборот, какие условия не наступят никогда, сколько ни работай.

Короткий ответ: «всё» — это не «написано много текста», а **зелёный гейт плюс пустой
список того, что ещё можно закрыть имеющимися данными**. Публикационная готовность
текстов **не равна** завершению межрепозиторной программы: на 3 ноября 2026 года
профиль уже опубликован, метаданные заполнены и защита основных `main` проверена,
но остаются публикационные настройки, качество межрепозиторной документации и CI зависимостей. Четыре `UNPROVEN`-утверждения — отдельная, честно ограниченная
доказательная граница, а не замена незавершённым действиям (§3).


### Актуализация портфельного закрытия: 4 ноября 2026

Ниже **оперативное дополнение** к историческому срезу §3 от 3 ноября и измерениям от 1 ноября. Оно не переписывает сохранённые исходные результаты.

- **Astro:** [gb-is-my-strength #2265](https://github.com/FedorMilovanov/gb-is-my-strength/pull/2265) смержен (`98ad5c835008940134a15eb7bd84fdce9a62a8fb`), его GitHub Pages release и post-merge проверки завершены успешно. Последующие изменения `main` и выпусков сайта — отдельный контур релизного контроля.
- **Dependabot:** авторизованная проверка 04.11 вернула **0 открытых уведомлений для 16 доступных репозиториев**; архивный `baptist---2` возвращает HTTP 403 для Dependabot Alerts, поэтому нельзя выдавать это за API-подтверждённый «0/17».
- **Ветки:** `main` защищена у **15 из 16** репозиториев с веткой; частный `sermon_MP3_bot` — исключение (`protected=false`). Исторические cookie-сессии следует отозвать у провайдера: удаление из Git-дерева не отменяет их действительность.
- **Профиль:** [README](https://github.com/FedorMilovanov/FedorMilovanov), [RU](PORTFOLIO_RU.md), [EN](PORTFOLIO_EN.md) опубликованы. GitHub API подтверждает пустые Bio/website и **0 pinned repositories**. Закрытие требует прав владельца профиля; новый репозиторий не требуется.
- **Vosk:** [gb-vosk-tts #4](https://github.com/FedorMilovanov/gb-vosk-tts/pull/4) смержен; Apache-2.0 для производного порта и исходный MIT для словаря задокументированы. Риск **R11 = PARTIAL только по внешней модели**: 04.11 на живом сайте проверены HTTP 200 обе JS-копии со SPDX-заголовками и три юридических notice в `/legal/tts/`; provenance квантованных весов, reproduction и hosting notices остаются отдельным MODEL_RIGHTS_HOLD.
- **Изменения только по делу:** собственная ветка от проверенного `main` → содержательный commit → PR → CI на точном HEAD → merge → post-merge. Не делать косметические «пиар-коммиты» и дублирующие PR ради счётчиков, не отключать обязательные проверки.

### Актуализация: 5 ноября 2026 — публичная публикация и оставшиеся блокеры

Эта запись дополняет датированные срезы 01–04.11 и не пересчитывает исторические показатели `METRICS.csv`.

- **Отдельный сайт портфолио готов.** [PR #3 FedorMilovanov.github.io](https://github.com/FedorMilovanov/FedorMilovanov.github.io/pull/3) влит коммитом `2ff7db9eb9025e32960a8ebd1dbbca2b3154b894`. [GitHub Pages run 42072510490](https://github.com/FedorMilovanov/FedorMilovanov.github.io/actions/runs/42072510490) завершил сборку, публикационный отчёт и deploy успешно. Внешне проверены [RU](https://fedormilovanov.github.io/portfolio/) и [EN](https://fedormilovanov.github.io/portfolio/en/); прежний редирект корня `/` на богословский сайт сохранён.
- **Главный GitHub-профиль связан с сайтом.** [PR #3 FedorMilovanov](https://github.com/FedorMilovanov/FedorMilovanov/pull/3) влит как `6ca9c3d3330d2847a8357ff4236c27cdc86115be`: публично видны ссылки на RU/EN сайт вместе с прежними документами Research. Это **не** означает настройки GitHub Bio, Website или шести pinned repositories.
- **Очистка временных веток портфолио завершена 05.11.** После проверки merged PR и подтверждения, что `main` содержит соответствующие коммиты, удалены `feat/verified-portfolio-ru-en-20261105` в `FedorMilovanov.github.io` и `feat/link-portfolio-pages-20261105` в профильном репозитории; ветка слитого Research PR #334 удалена ранее. Это не изменяет содержимое опубликованных `main`.
- **Research #196 теперь ЗАКРЫТ реальной защитой, а не только кодом.** После [PR #298](https://github.com/FedorMilovanov/Research/pull/298) через авторизованный GitHub CLI в legacy branch protection добавлен обязательный job `Repository authority integrity` (GitHub Actions `app_id=15368`) с сохранением трёх прежних обязательных проверок и `strict=true`. Независимое чтение правил подтвердило `enforce_admins=true`, PR-rule, запрет force-push и удаления, а также требование разрешать обсуждения. Безусловно запускаемый на каждом PR [authority workflow](https://github.com/FedorMilovanov/Research/blob/main/.github/workflows/repository-authority-integrity.yml) включает G3 validators; отдельный path-filtered `G3 corpus integrity` намеренно не добавлен как глобально обязательный (он пропускает нерелевантные PR). [Issue #196 закрыт с доказательствами](https://github.com/FedorMilovanov/Research/issues/196). На merge-коммите портфельного [PR #334](https://github.com/FedorMilovanov/Research/pull/334) все четыре post-merge workflow, включая ранее выполнявшийся Atonement, завершились SUCCESS; защита повторно проверена 05.11.
- **HF Vosk card опубликована, права не сняты.** [Коммит `30bfb2bfaa9dec599ea97ff0c04166a595d4d7eb`](https://huggingface.co/CurtMil/gb-vosk-tts-model/commit/30bfb2bfaa9dec599ea97ff0c04166a595d4d7eb) документирует Alpha Cephei, BERT-only квантование и SHA-256 размещённых файлов. `MODEL_RIGHTS_HOLD` для внешних весов 0.9 сохраняется: карточка не заменяет лицензию и независимую проверку исходного архива.
- **Стадия 4 всё ещё неполная.** Сайт и профиль опубликованы; публикации на hh.ru и LinkedIn не подтверждены. Также не доказан отзыв исторических cookie-сессий частного `sermon_MP3_bot`, а тарифное ограничение защиты его `main` не снято. Эти остатки нельзя объявлять `DONE` только закрытием PR.


---

## 1. Машинный критерий

```bash
python3 PORTFOLIO/tools/check_claims.py
```

Гейт проверяет шесть вещей и падает при любом расхождении:

| Проверка | Что ловит |
|---|---|
| Считаемые утверждения из `CLAIMS.csv` | число в реестре не совпало с пересчётом по `METRICS.csv` / `MEDIA_METRICS.csv` |
| Реестр | дубли id, недопустимый статус, пустые `source` / `method` / `checked` |
| Индекс | файл есть, а в `README.md` о нём не сказано |
| Ссылки | относительная ссылка ведёт в никуда |
| Устаревшие числа | опровергнутое значение вернулось в документ текущего состояния |
| Паритет RU/EN | ключевое число есть в русской версии и нет в английской (или наоборот) |

`CLAIMS.csv` — реестр из 32 утверждений: `CONFIRMED` (14) — проверено внешним
наблюдением, `DERIVED` (14) — посчитано из CSV и пересчитывается при каждом прогоне,
`UNPROVEN` (4) — заявлено честно как непроверенное. Числа без записи в реестре в текстах
не используются.

---

## 2. Что уже готово

| Артефакт | Состояние | Чем подтверждено |
|---|---|---|
| `AUDIT_RU.md` | готов | 10 клонов, API, пересчёт всех чисел; 8 раундов проверки |
| `PORTFOLIO_RU.md` | готов к публикации | все числа из реестра, паритет с EN |
| `PORTFOLIO_EN.md` | готов к публикации | то же, плюс честный FAQ про ИИ и чужой TTS |
| `PROFILE_README.md` | **опубликован** | [профильный репозиторий](https://github.com/FedorMilovanov/FedorMilovanov) создан 03.11; с 05.11 README содержит ссылки на работающие [RU](https://fedormilovanov.github.io/portfolio/) и [EN](https://fedormilovanov.github.io/portfolio/en/) страницы, без плейсхолдеров и недоказанного числа слов |
| `METRICS.csv` | готов | 15 строк, `data_as_of=2026-11-01` |
| `MEDIA_PRACTICE.md` | готов | медиа-линия описана процессом, без счётчиков аудитории |
| `HISTORY_AND_PRINCIPLES.md` | готов | 17 836 коммитов, хронология, словарь |
| `DEFENSE_SYSTEMS.md` | готов | числа пересчитаны воспроизводимым скриптом |
| `DEFECT_CLASSES.md` | готов | 391 отчёт, 119 закрытий, 30 тем |
| `DEEP_SWEEP.md` | готов | ритм, пропускная способность PR, теги |
| `OPEN_SOURCE_PLAYBOOK.md` | готов | модель форка, 10 правил, целевые проекты |
| `GITHUB_DISCOVERABILITY.md` | готов | механика поиска, topics по репозиториям |
| `AGENT_HANDOFF.md` | готов | задание агенту с правом пуша |
| `security-baseline/` | готов | `install.sh` протестирован, контур стоит в `Research` |
| `wave1/` | **закрыт применением** | `mp3telegrambot` имел сканер; `video-channel-manager` PR [#755](https://github.com/FedorMilovanov/video-channel-manager/pull/755) влит в `main` (`e56b12a`), post-merge secret scan прошёл |
| `VERIFICATION_LOG.md` | ведётся | 15 разделов, включая найденные ошибки собственного гейта |
| `REVERIFICATION_2026-11-01.md` | готов | 33 подтверждено, 11 исправлено |
| `CLAIMS.csv` + `tools/` | готовы | гейт, измеритель защиты, 32 утверждения |

---

## 3. Исторический статус исполнения (срез 03.11.2026; обновление 04.11 — выше)

Таблица ниже **дополняет срез METRICS.csv/CLAIMS.csv от 01.11**, не подменяя
его неполным пересчётом. Закрытость определяется изменением в `main` или
явной проверкой, а не готовностью шаблона. Перед новым PR проверять открытые
работы других агентов и перечитывать свежий HEAD.

| Направление | Факт на 03.11.2026 | Следующее закрывающее действие |
|---|---|---|
| `video-channel-manager` — защитный контур и английский README | **Закрыто:** secret scan [#755](https://github.com/FedorMilovanov/video-channel-manager/pull/755), root `SECURITY.md` [#756](https://github.com/FedorMilovanov/video-channel-manager/pull/756), английский `README_EN.md` [#757](https://github.com/FedorMilovanov/video-channel-manager/pull/757) — все три в `main`; post-merge Gitleaks зелёный | не повторять завершённые патчи; отдельно от security продолжается неавторизованный к исполнению Telegram preflight |
| Секрет-сканирование портфеля | **Завершено 11/11:** конфигурации Gitleaks в `main` всех 11 основных проверенных продуктовых/инфраструктурных репозиториев; [DeepMovieReview #136](https://github.com/FedorMilovanov/DeepMovieReview/pull/136) влит как `9f568ea`, отдельный post-merge Gitleaks успешен | это **покрытие проверками, не гарантия 0 секретов**; не создавать повторные security PR |
| `DeepMovieReview` | **Закрыто:** [#136](https://github.com/FedorMilovanov/DeepMovieReview/pull/136) влит после 32 успешных PR checks + 1 neutral historical (Native iOS Safari в итоге прошёл); `main` secret scan успешен | флейки нативного iOS остаются самостоятельным CI-наблюдением, не поводом ослаблять gate; чужой draft #139 не затронут |
| Профиль GitHub | **Опубликован** в [FedorMilovanov/FedorMilovanov](https://github.com/FedorMilovanov/FedorMilovanov); README доступен публично | Bio/website профиля и закрепление репозиториев требуют действий владельца через UI или дополнительного `user` scope; текущий CLI не имеет таких прав |
| Описания и topics | **Закрыто 12/12:** авторизованный GitHub CLI выставил descriptions/topics для 11 основных репозиториев и `FedorMilovanov.github.io`, homepage 5/5; прежний `Milovi_Cake` description `Cakes site` заменён | проверять при изменении назначения проекта; не повторять уже выполненную волну |
| Два английских README | **Завершено 2/2:** `video-channel-manager` [#757](https://github.com/FedorMilovanov/video-channel-manager/pull/757) и `mp3telegrambot` [#435](https://github.com/FedorMilovanov/mp3telegrambot/pull/435) в `main`; последний — после 8/8 успешных проверок | не создавать новые переводы/дубли, при изменении контракта синхронизировать оба языка |
| `mp3telegrambot` зависимости и CVE | **Закрыто в `main`:** узкий [#436](https://github.com/FedorMilovanov/mp3telegrambot/pull/436) исправил `pyasn1`, а [Dependabot #437](https://github.com/FedorMilovanov/mp3telegrambot/pull/437) влит как [`c7f68cf`](https://github.com/FedorMilovanov/mp3telegrambot/commit/c7f68cf607d3a7aa2bb3c86a7eb422697e3a0289) после устранения несовместимости `google-genai`/`tenacity`, синхронизации с `main` и полного зелёного PR CI; **все 13 post-merge GitHub Actions runs завершились `success`** (проверено авторизованным `gh run list --commit`) | не повторять #436/#437; новые Dependabot PR рассматриваются отдельно и не сливаются без их собственных CI |
| Приватный `sermon_MP3_bot` | После [#1](https://github.com/FedorMilovanov/sermon_MP3_bot/pull/1) отслеживаемые cookie удалены из `main`, но остались в истории; Dependabot vulnerability alerts **включены** | владелец обязан отозвать старые cookie-сессии у провайдера; private `main` branch protection GitHub отклонил `403 Upgrade to GitHub Pro or make this repository public`; **не делать репозиторий публичным** и не заявлять этот риск закрытым |
| README / OWNER / ARCHITECTURE / CASE_STUDY / SECURITY | **Частичная публикационная волна закрыта в `main` и проверена:** [gb-vosk-tts #3](https://github.com/FedorMilovanov/gb-vosk-tts/pull/3) (`2e36900`), [Milovi_School #50](https://github.com/FedorMilovanov/Milovi_School/pull/50) (`4fcf206`), [Milovi_Cake #138](https://github.com/FedorMilovanov/Milovi_Cake/pull/138) (`7891708`), [bible-bot #187](https://github.com/FedorMilovanov/bible-bot/pull/187) (`a759812`), [AuditRepo #513](https://github.com/FedorMilovanov/AuditRepo/pull/513) (`5b203c2`). Документы содержат границы авторства, архитектурные доказательства и/или приватную security reporting policy; AuditRepo сохраняет строгий root-MD allowlist с регрессионным тестом | Остальные репозитории не сертифицированы массово; не плодить пустые OWNER/CASE ради галочки, сверять действующие AGENTS/authority, чужие PR и реальные источники |
| `.mailmap` | Массовое внедрение не подтверждено, спорный адрес требует подтверждения владельца | не приписывать авторство без сверки; не переписывать Git history |
| Числовой срез | `METRICS.csv`, `CLAIMS.csv` и `VERIFICATION_LOG.md` относятся к **01.11.2026** | после завершения security-волны воспроизводимо пересчитать новые числа, обновить связанные документы и запустить `check_claims.py` |
| Branch protection | **15/16 существующих default `main` защищены**, из них 13 основных/публичных проверены ранее, затем `baptist` и `baptist2` получили PR-only protection. `baptist---2` пустой и не имеет ветки; `sermon_MP3_bot` — единственное исключение (приватная ветка, ограничение тарифа GitHub Pro, API `403`). Ранее существующая legacy protection `AuditRepo` подтверждена (`validate`, `preflight`) | не подменять rulesets и checks фикцией, не отключать защиты ради мержа, не открывать доступ к приватному `sermon_MP3_bot` |
| Dependabot vulnerability alerts | **17/17 включены и повторно проверены** через GitHub API, в том числе старые публичные, пустой профильный и приватный `sermon_MP3_bot` | это механизм оповещения, **не** свидетельство отсутствия CVE или права на автоматический merge |
| Открытые уязвимости Dependabot | **Проверено API 03.11:** после [Milovi_School #52](https://github.com/FedorMilovanov/Milovi_School/pull/52) (`dd4d98e`, 5/5 PR workflow success) `minimatch` CVE-2026-118764 снят; **0 открытых alerts у Milovi School**. У `gb-is-my-strength` остались **2 Astro advisories**: [CVE-2026-114128](https://github.com/advisories/GHSA-98hj-9722-w3j8) (medium) и [CVE-2026-114127](https://github.com/advisories/GHSA-mpr7-6m5w-76rw) (low) | Существующий [Dependabot #2244](https://github.com/FedorMilovanov/gb-is-my-strength/pull/2244) красный, потому что `scripts/astro7-satteri-contract.mjs` намеренно требует Astro 7.2.9 / Satteri 0.3.8; patched Astro 7.3.3 использует Satteri 0.4.1, 7.4.4 — 0.4.6. Требуется проверяемая Satteri-миграция с owner SYSTEM scope; не обходить проверки и не редактировать чужую активную ветку |
| Публикация source vs production | **Milovi_School подтверждён live:** `https://french.milovicake.ru/release.json` ответил HTTP 200 exact `dd4d98ede5911e924ae182ebab5debd47e116715`, совпадает с security merge. `bible-bot` post-merge CI/CodeQL/Security Audit/Chapter integrity зелёные на `a759812`, но внешний Render/Telegram production acceptance отдельно не проверялся. **Milovi_Cake:** при проверке 03.11 live `/release.json` был `c60a9248…` против нового source `7891708…`, Pages deploy ещё выполнялся | Повторить точную live-SHA проверку `Milovi_Cake` после подтверждённого деплоя; не переносить факт зелёного source CI на production; не считать Render/Telegram provider state подтверждённым по GitHub |
| Публичные метрики | Трафик, выручка и некоторые медиа-показатели не наблюдаются из GitHub; срез `CLAIMS.csv` сохранён на 01.11 | не заявлять недоказанные результаты |

**Граница процентов (срез 03.11.2026):** конфигурационное покрытие Gitleaks **11/11 (100%)**
среди определённых 11 основных репозиториев; приоритетные английские README — **2/2 (100%)**.
Это **не** общий процент готовности портфолио и **не** утверждение о безопасности
всех 17 репозиториев аккаунта: исторические, приватные и пустые ветки требуют отдельной
классификации. Метрики `METRICS.csv`/`CLAIMS.csv` сохраняют исторический срез 01.11.
Общий достоверный процент невозможен без согласованных весов и полного повторного инвентаря.

---

## 4. Что не закроется никогда (и почему это нормально)

| Утверждение | Почему остаётся `UNPROVEN` |
|---|---|
| ≈365 000 слов авторской прозы | оценка методом извлечения текста, погрешность ±15 %; точный подсчёт потребовал бы разметки страниц |
| Доля зелёных прогонов CI | Агрегированный `total_count` ограничен 2 500, но оконный метод позволяет восстановить доступные runs; отдельный подсчёт по conclusion и attempts ещё не выполнен, доля успехов не доказана |
| Branch protection и rulesets | GitHub App в историческом срезе возвращал `403`, но 03.11 авторизованный пользовательский `gh` позволил **проверить и установить** реальную legacy branch protection для 13/13 выбранных репозиториев. Запись `UNPROVEN` в старом CSV не является текущим статусом |
| Трафик и выручка | нет доступа к аналитике; в портфолио не заявляются |

Правило простое: если утверждение нельзя проверить, оно либо помечено `UNPROVEN`,
либо не попадает в текст. Третьего варианта нет.

---

## 5. Четыре состояния готовности

Чтобы «готово» не означало «мне так кажется», у каталога четыре различимых состояния:

1. **Черновик** — текст есть, числа не сведены. Не публиковать.
2. **Согласовано** — `check_claims.py` зелёный, все числа в реестре.
3. **Готово к публикации** — плюс паритет RU/EN и отсутствие `UNPROVEN` в утвердительной форме.
   **Документы исследования достигли этой стадии; часть материала уже опубликована на GitHub.**
4. **Опубликовано** — материалы выложены (сайт, hh, LinkedIn, профиль-README) и ссылки
   на них добавлены в реестр. Требует действий владельца аккаунтов.
   **Частично исполнено (05.11.2026):** профильный README и отдельные страницы [RU](https://fedormilovanov.github.io/portfolio/) / [EN](https://fedormilovanov.github.io/portfolio/en/) опубликованы, ссылки взаимно связаны. Публикации на hh.ru и LinkedIn не подтверждены; полную стадию 4 не заявлять.

Разница между 3 и 4 — не качество текста, а факт публикации: портфолио в репозитории
и портфолио, которое размещено на внешних профессиональных площадках, — разные состояния. Публичный сайт готов; hh.ru и LinkedIn остаются отдельными неподтверждёнными площадками.

---

## 6. Что будет считаться регрессом

Гейт должен падать в этих случаях — если не падает, сломан гейт:

* правка числа в тексте без правки `CLAIMS.csv` (для считаемых величин);
* новый документ, не указанный в индексе;
* возврат опровергнутого значения — их перечень задан константой `STALE_TOKENS` в `tools/check_claims.py`, и в сам этот документ они не вписаны, иначе он ловил бы сам себя;
* расхождение ключевого числа между русской и английской версиями;
* битая относительная ссылка.

### Чего гейт не проверяет

Гейт сверяет документы **между собой** и с `METRICS.csv`. Он не ходит в GitHub и не
пересчитывает код: если завтра в репозиторий добавится новый workflow, `METRICS.csv`
устареет, а гейт останется зелёным. Соответствие реестра реальности проверяется
отдельно — `tools/measure_defense.py` по свежим клонам, вручную, с записью в
`VERIFICATION_LOG.md`. Это осознанное разделение: CI проверяет то, что можно проверить
за пять секунд, а сетевые измерения остаются ритуалом с датой.

Проверяется это не на словах: `check_claims.py` входит в CI `Research`
(`.github/workflows/portfolio-claims.yml`), поэтому регресс виден в PR, а не в переписке.

### Поправка к измерению CI (03.11.2026)

Исторический счётчик 119 919 был ошибочно представлен как полный; 40 000 в gb-is-my-strength оказалось лимитом GitHub API. Его нельзя использовать как актуальный точный результат. Для claim C-014 теперь применяется отдельный [CI_RUNS_2026-11-03.csv](CI_RUNS_2026-11-03.csv): 221 596 API-доступных запусков десяти репозиториев за 2026 год до 21:05:16 UTC 03.11.2026. Метод разбиения временных интервалов воспроизводится [tools/measure_ci_runs.py](tools/measure_ci_runs.py). METRICS.csv продолжает хранить исходный срез остальных метрик от 01.11, а не гибридный набор текущих чисел.
