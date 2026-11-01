# Волна 1: `video-channel-manager` — secret scanning

Статус: **патч готов и проверен, но не отправлен**. Пуш в этот репозиторий из текущей
сессии невозможен: токен GitHub, выданный песочнице, ограничен `Research`
(`git push` → `403`, `git/blobs` через API → `Resource not accessible by integration`).
Применение — одна команда, см. ниже.

## Что именно отсутствовало

| Контроль | Состояние до патча | Доказательство |
|---|---|---|
| Пины внешних действий на 40-hex SHA | есть, сильнее типового | `tests/_workflow_actions.py` + `tests/test_github_action_pins.py` |
| Обязательный комментарий версии `# vX.Y.Z` | есть | `assert_actions_pinned` бросает `ActionPinError` без него |
| Минимальные версии и запрет отката | есть | `MINIMUM_RELEASES`, `RETIRED_REFS` |
| Явные `permissions` и пины раннеров | есть (в тестах и в `ci.yml`) | `ubuntu-24.04`, `permissions:` в 32 workflow |
| Зависимости | есть | `pip-audit` в `ci.yml`, `.github/dependabot.yml` |
| Политика безопасности | есть, канонический документ — `docs/security.md` | `tests/test_repository_integrity_polish.py` требует в нём трёх формулировок |
| **Сканирование секретов в истории** | **отсутствует** | нет `gitleaks`, нет `.gitleaks.toml`, нет workflow |
| Корневой `SECURITY.md` | отсутствует | GitHub не покажет ссылку «Security policy» |

Единственный реальный пробел — последняя строка: репозиторий с provider-записями
(Telegram, VK, YouTube) ни разу не проверялся на утечку токенов ни в диффе, ни в истории.

## Что добавляется

`.github/workflows/secret-scan.yml` — один джоб `gitleaks`:

* триггеры: `push`/`pull_request` в `main`, недельный `schedule` (полная история),
  ручной `workflow_dispatch`;
* `fetch-depth: 0` — иначе проверка «нет ли секретов в репозитории» вырождается
  в проверку «нет ли секретов в диффе»;
* `permissions: contents: read`, `persist-credentials: false`, `ubuntu-24.04`,
  `timeout-minutes: 15`;
* действия запинованы в стиле репозитория: `actions/checkout@3d3c42e5… # v7.0.1`,
  `gitleaks/gitleaks-action@e0c47f4f… # v3.0.0` — обязательный комментарий версии
  присутствует, поэтому `test_github_action_pins.py` остаётся зелёным;
* `GITLEAKS_ENABLE_UPLOAD_ARTIFACT: false` — не требовать `actions: write`
  у read-only токена.

Сознательно **не добавляется**:

* джоб гигиены workflow (пины, `permissions`, запрет `write-all`) — его роль уже
  выполняет `pytest`-набор `tests/`, дублирование дало бы второй источник правды;
* корневой `SECURITY.md` — в репозитории есть канонический `docs/security.md`,
  и его содержание проверяется тестом; второй документ размыл бы единственный
  источник истины. Если нужна ссылка в UI GitHub, правильное решение — отдельный
  PR, который делает `docs/security.md` каноническим и ставит корневой файл-указатель.

## Проверка (выполнена локально, до отправки)

Репозиторий клонирован целиком (`3 194` коммита), файл положен в рабочее дерево:

```
tests/test_github_action_pins.py       9 → 9 passed   (до и после; 6 проверок контракта)
tests/test_github_action_pins.py
  + tests/test_ref_binding_inventory.py            15 passed   (после патча)
tests/test_repository_integrity_polish.py
  + tests/test_telegram_publisher_runtime_lock.py   8 passed
YAML: 32 workflow-файла, 0 невалидных; новый файл — jobs=[gitleaks], permissions={contents: read}
```

История проверена отдельно, чтобы недельный блокирующий прогон не покраснел на первом
же запуске — `git log --all -p` по всем `3 194` коммитам, шесть форм секретов
(Google API key, GitHub token, Telegram bot token `:AA…`, приватный ключ, `ya29.`,
AWS `AKIA`): **0 совпадений**. Это не заменяет gitleaks (у него шире набор правил,
включая энтропийные), но снимает вопрос «а вдруг там лежит старый токен».
Если CI всё же найдёт совпадение в документации (примеры ключей в аудитах),
лечится узкой записью `[allowlist] paths` в `.gitleaks.toml`, а не отключением правила.

## Применение

```bash
git clone https://github.com/FedorMilovanov/video-channel-manager.git
cd video-channel-manager
bash /path/to/Research/PORTFOLIO/wave1/video-channel-manager/apply.sh .
git switch -c arena/576cf1ae-video-channel-manager
git add .github/workflows/secret-scan.yml
git commit -m "Add history-wide secret scanning (gitleaks) to the CI contour"
git push -u origin arena/576cf1ae-video-channel-manager
gh pr create --fill --base main
```

`apply.sh` идемпотентен: повторный запуск печатает `skip (identical)` и ничего не делает.
