# Security baseline — единый защитный контур для девяти репозиториев

Готовый набор файлов, который закрывает главный разрыв из `DEFENSE_SYSTEMS.md`: сканирование секретов было в одном репозитории из девяти, `SECURITY.md` — в двух.

Все внешние действия прибиты к тем же SHA, которые уже используются в существующих workflow (`gitleaks-action@e0c47f4`, `actions/checkout@3d3c42e`, `setup-node@8207627`, `setup-python@5fda3b9`). Новых решений по цепочке поставки не вводится.

## Состав

| Файл | Куда | Что делает |
|---|---|---|
| `.github/workflows/security-baseline.yml` | каждый репозиторий | три джобы: секреты, зависимости, гигиена workflow |
| `.gitleaks.toml` | `mp3telegrambot` уже имеет; остальным — как шаблон | правила по умолчанию + узкий allowlist без путевых исключений |
| `SECURITY.md` | корень | модель секретов, приватный канал, поддерживаемые версии |
| `.github/dependabot.yml` | где нет (`TheLegendaryPoet`, `AuditRepo`) | недельные группы обновлений, без автомержа |
| `install.sh` | локально | копирует файлы, подставляет имя репозитория и стек |

## Как подключить (5 минут на репозиторий)

```bash
# из корня Research
cd PORTFOLIO/security-baseline && ./install.sh /путь/к/репозиторию

# затем
cd /путь/к/репозиторию
git checkout -b security/baseline
git add .github SECURITY.md
git -c user.name="Фёдор Милованов" commit -s -m "ci(security): add secret scanning, dependency audit and workflow hygiene gate"
git push -u origin security/baseline
```

Открыть PR и дождаться зелёного. Первый прогон намеренно строгий: если он падает на истории, это не повод ослаблять гейт — это находка.

## Что именно проверяется

**1. Секреты (`secrets`).** `gitleaks` по всей истории (`fetch-depth: 0`) на push, PR и раз в неделю по расписанию. Отчёт сохраняется артефактом даже при падении — иначе разбор невозможен.

**2. Зависимости (`dependencies`).**

- Python: если есть `requirements-lock.txt` / `requirements.txt` / `poetry.lock` — `pip-audit --strict` по первому найденному.
- Node: если есть `package-lock.json` — `npm audit --audit-level=high` (умеренные не валят сборку: иначе гейт станет шумом, как это уже произошло в `gb-is-my-strength` с двумя moderate-записями Astro).

**3. Гигиена workflow (`workflow-hygiene`).** Встроенная проверка того, что уже соблюдается вручную:

- каждое `uses:` указывает на полный 40-символьный SHA;
- каждый workflow объявляет `permissions:`;
- нет `permissions: write-all`;
- нет `pull_request_target` без явной проверки форка;
- в индексе нет `.env`, `cookies.txt`, `*.pem`, `*.key`.

Эта джоба — исполняемая версия правила «576/576 пинов». Раньше оно держалось на дисциплине, теперь на гейте.

## Порядок внедрения

| Волна | Репозитории | Почему так |
|---|---|---|
| 1 | `mp3telegrambot`, `video-channel-manager` | там уже есть часть защиты, риск конфликта минимален; `mp3` — эталон |
| 2 | `gb-is-my-strength`, `TheLegendaryPoet` | большие, активные, много workflow — проверка гигиены сразу даст результат |
| 3 | `Milovi_Cake`, `Milovi_School` | статические сайты, зависимостей мало |
| 4 | `bible-bot`, `AuditRepo`, `DeepMovieReview` | низкая активность, можно в конце |

Не подключать в `gb-vosk-tts` до решения по лицензии: репозиторий пересматривается целиком.

## Что baseline намеренно не делает

- Не включает CodeQL: он требует GitHub Advanced Security для приватных репозиториев, а для публичных уже работает в трёх репозиториях отдельно.
- Не включает secret scanning GitHub как настройку: это делается в Settings один раз и не описывается файлом (см. `CHECKLIST.md`).
- Не настраивает branch protection: это ruleset в настройках, файлом не выражается. Как только включишь — зафиксируй скриншотом и датой, чтобы `UNPROVEN` в `AuditRepo` можно было заменить ссылкой.
- Не трогает существующие workflow. Если в репозитории уже есть джоба `gitleaks` — не дублируй, оставь свою и подключи только hygiene-джобу.
