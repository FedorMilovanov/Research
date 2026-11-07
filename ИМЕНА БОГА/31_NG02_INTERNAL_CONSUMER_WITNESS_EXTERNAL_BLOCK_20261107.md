# 31 — Internal consumer contract witness: 50 inline + 22 generic legacy

**NG-02, 2026-11-07 · RESEARCH_HOLD · NO PRODUCT/Arena DEPLOYMENT APPROVAL**

## Аудит действительно читающих код и данных

Исследованы source files, существующие read-only проверки и независимые JSON snapshots из Research, не только имена файлов. В baseline+extension 105 attestationId; 50 непосредственно имеют locusId, 55 не имеют (51+4). Из четырёх независимых locked contracts **50/50** именованных locusId точно и однозначно сопоставлены через оригинальный `recordId`, `verse`, `surface` с actual ledgers и новым sidecar. Пятый общий contract содержит **22/22** независимо зафиксированных свидетельства *без* locusId; все 22 однозначно сопоставлены с исторической sidecar-only группой, ни одна запись не пересекается с 50 inline.

| Проверенный исходный контракт | В Research | Наличие locator | Вывод |
| --- | ---: | --- | --- |
| `data/memorial_attestation_contract_v1.json` | 16 | 16 inline | Имя места/жертвенника и объекты: существующие locusId нельзя переименовывать |
| `data/speech_intertext_contract_v1.json` | 12 | 12 inline | Говорящие/греческие сопоставления привязаны к точным locator |
| `data/extension_attestation_contract_v1.json` | 14 | 14 inline | Новые формы оригинального корпуса, точные локусы |
| `data/core_name_lexeme_contract_v1.json` | 8 | 8 inline | ЯХВЕ и контекстно-зависимое эль, точные локусы |
| `data/attestation_contract_v1.json` | 22 | 0 inline | Общее свидетельство использует `baselineId`, `verse`, `surface`, `edition`; все 22 — sidecar-only |

Кроме совпадения ID проверяются `verse`, `surface`, `edition`, `sourceUrl`, `criticalEditionStatus`, `rightsState`, `publicationState`. **Отсутствие именованного локуса НЕ ошибка**, если контракт использует старый v1 формат.

## Что реально известно о внешних потребителях

Для ограниченной read-only проверки просмотрены списки/деревья файлов и GitHub default-branch индекс по `locusId` и смежным названиям для:
- `FedorMilovanov/gb-is-my-strength`, `main`;
- `FedorMilovanov/TheLegendaryPoet`, `main`;
- `FedorMilovanov/FedorMilovanov.github.io`, `main`.

Прямое индексируемое вхождение этих специфических Research-ключей **не обнаружено**. Однако отрицательный поиск по части кодовой базы **НЕ** удостоверяет отсутствие runtime API-импорта, другого репозитория, ещё не объединённой ветки, zip-прототипа, JavaScript bundle или уже развёрнутого приложения. Имена-значения, права и реальное поведение не подтверждены через сборку/деплой этих сайтов. Ни один внешний потребитель не помечен `VERIFIED`, `v2Gate` остаётся `BLOCKED_PENDING_EXTERNAL_CONSUMER_CONTRACT`.

## Архитектурное ограничение

Добавлен `data/names_consumer_compat_v1.json` — машинно читаемый инвентарь границ фактической проверки. Отдельный `validate_names_consumers.py` валидирует 50+22 cross-snapshot witness через оригинальные JSON и sidecar; `test_validate_names_consumers.py` содержит **25** позитивных/негативных тестов на точные значения, метаданные, подмену origin-parent, несанкционированную публикацию и фиктивный Product readiness. Эти проверки включены в единственный Names of God GitHub workflow.

**Важное различие:** структурное покрытие 105/105 claims и разрешаемые Research-side locator 105/105 — не согласованная внешняя v2-модель. Исходные 55 полей до сих пор отсутствуют; 50 старых полей нельзя менять; согласование всех внешних потребителей, dual-read контракт и одобрение владельца нужны до любой Product миграции.

## Дополнение: pinned external source-control witness (NG-02, 2026-11-07)

Это **узкий read-only аудит 8 реально прочитанных файлов** в трёх репозиториях, не доказательство отсутствия Product/Arena-потребителей. Полные 40-символьные revision SHA и blob SHA каждого файла зафиксированы в `data/names_consumer_compat_v1.json → sourceControlSnapshots` и защищены валидатором.

| Репозиторий / pinned commit | Прочитанные файлы и сокращённые Git blob SHA | Результат |
| --- | --- | --- |
| [gb-is-my-strength · 5e2db6f](https://github.com/FedorMilovanov/gb-is-my-strength/tree/5e2db6f0fdd0257818f1a215fca16d4cc884e2d8) | `src/pages/index.astro` · `dba91b0`; `src/data/site.ts` · `0f27139`; `src/pages/app/index.astro` · `b180391` | Astro homepage, SITE metadata, app page: прямого импорта данных «Имён Бога» в этих файлах нет |
| [TheLegendaryPoet · 46c66f2](https://github.com/FedorMilovanov/TheLegendaryPoet/tree/46c66f2251168d5aaebe1455b5ba96dad5a8c884) | `src/routes/routeModules.ts` · `fe54ccf`; `src/routes/route-contract.json` · `5ba4486`; `src/App.tsx` · `b524046` | Прочитаны React-router и root; прямого импорта Research в этих файлах нет |
| [FedorMilovanov.github.io · 117314e](https://github.com/FedorMilovanov/FedorMilovanov.github.io/tree/117314ef8a927d6eacfd135e1dfd347873c1cea0) | `index.html` · `96b66e2`; `portfolio/index.html` · `43d7a1a` | Root — редирект на `/gb-is-my-strength/`; portfolio — страница портфолио |

**Область вывода:** индекс + пути + содержимое именно указанных файлов по точным коммитам; другие ветки, chunks, динамические fetch, production bundle/deploy, оба исходных Arena ZIP и Product contract tests НЕ проверены. Поэтому `consumerContract=NOT_ATTESTED`, `runtimeVerified=false`, `v2Gate=BLOCKED_PENDING_EXTERNAL_CONSUMER_CONTRACT`, scholarly/rights/Product HOLD остаются неизменными.

Добавлены **4 негативных regression tests**: замена SHA коммита, замена SHA исходного файла, фиктивное `runtimeVerified=true`, удалённая entrypoint-запись. Локальный валидатор проверяет закреплённый snapshot, **не делает сетевых запросов к GitHub**, не подтверждает актуальный deployment. STOP_DISCOVERY: без нового exact import path, исходного Arena архива или pinned deployed build не повторять выборочный поиск по тем же файлам.

## Next bounded action

Собрать exact pinned revision и реально исполняемые consumer tests продукта (если он интегрирует данные), получить свидетельство чтения v1/v2 и отказа от сломанного old inline, после чего отдельным решением разрешить versioned v2. Если ни один внешний потребитель не существует, нельзя выдавать это за факт без деплой-проверки. Все оригинально-языковые академические claims и права источников остаются Research HOLD.
