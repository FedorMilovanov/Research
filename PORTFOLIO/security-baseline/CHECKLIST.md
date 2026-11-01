# Чек-лист настроек, которые не выражаются файлом

Файлы дают сканирование и гейты, но часть защиты живёт только в настройках GitHub. Отмечай по мере включения; как только пункт закрыт — сохраняй скриншот и дату, чтобы в `AuditRepo` заменить `UNPROVEN` ссылкой на доказательство.

## 1. На уровне аккаунта (один раз)

- [ ] Двухфакторная аутентификация включена, recovery-коды сохранены вне репозитория.
- [ ] Приватность email: Settings → Emails → «Block command line pushes that expose my email».
- [ ] Единая идентичность коммитов: `user.name`/`user.email` = `noreply`-адрес; в каждом репозитории — `.mailmap` (см. `AGENT_HANDOFF.md` §3.7).
- [ ] SSH-ключ с парольной фразой или fine-grained token с минимальными правами; старые токены отозваны.
- [ ] Sessions: проверить активные сессии и устройства, лишние завершить.

## 2. На уровне репозитория (× 9)

| Репозиторий | Secret scanning | Push protection | Ruleset с обязательным `Security baseline` | Dependabot alerts |
|---|---|---|---|---|
| `mp3telegrambot` | ☐ | ☐ | ☐ | ☐ (уже есть) |
| `video-channel-manager` | ☐ | ☐ | ☐ | ☐ (уже есть) |
| `gb-is-my-strength` | ☐ | ☐ | ☐ | ☐ (уже есть) |
| `TheLegendaryPoet` | ☐ | ☐ | ☐ | ☐ |
| `Milovi_Cake` | ☐ | ☐ | ☐ | ☐ |
| `Milovi_School` | ☐ | ☐ | ☐ | ☐ |
| `bible-bot` | ☐ | ☐ | ☐ | ☐ |
| `AuditRepo` | ☐ | ☐ | ☐ | ☐ |
| `DeepMovieReview` | ☐ | ☐ | ☐ | ☐ |

Где включать: `Settings → Code security and analysis` (secret scanning, push protection, Dependabot alerts/security updates) и `Settings → Rules → Rulesets` (require status check, запрет force-push и удаления `main`, linear history — по вкусу).

## 3. Что обязательно должно быть обязательным

Ruleset для `main`:

- [ ] Pull request перед мержем (для репозиториев с одним человеком — допустимо 0 ревью, но PR обязателен).
- [ ] Обязательный статус-чек: `Security baseline` / `Secret scanning`.
- [ ] Обязательный статус-чек: основной CI репозитория (`CI`, `validate`, `Required PR Gate`).
- [ ] Запрет force-push.
- [ ] Запрет удаления ветки.
- [ ] Требование линейной истории — по желанию; ломает merge-коммиты.

## 4. Порядок, чтобы не сломать себя

1. Сначала PR с файлами и зелёным прогоном.
2. Потом ruleset, включающий этот прогон как обязательный.
3. Потом push protection: он блокирует push, поэтому включать после того, как история чиста (иначе первая же попытка пуша упрётся в старую находку).
4. После каждого шага — скриншот в `Research/PORTFOLIO/evidence/` с датой в имени файла.

## 5. Проверка, что всё работает

```bash
# 1. Файлы на месте
ls -1 .github/workflows/security-baseline.yml SECURITY.md .gitleaks.toml

# 2. Локальная гигиена workflow (та же логика, что в CI)
python3 - <<'PY'
import pathlib, re
for p in pathlib.Path(".github/workflows").glob("*.y*ml"):
    t = p.read_text(encoding="utf-8")
    assert "permissions:" in t, f"{p}: no permissions"
    for line in t.splitlines():
        s = line.strip()
        if s.startswith("uses:"):
            ref = s.split("uses:", 1)[1].split("#", 1)[0].strip().strip("'\"")
            if not ref.startswith("./"):
                assert re.search(r"@[0-9a-f]{40}$", ref), f"{p}: unpinned {ref}"
print("ok")
PY

# 3. Проверка истории на секреты (если gitleaks установлен локально)
gitleaks detect --source . --redact -v || true
```

## 6. Что считать успехом

- Ни одного workflow без `permissions:`.
- Ни одного `uses:` с тегом вместо SHA.
- Сканирование секретов во всех девяти репозиториях, а не в одном.
- `SECURITY.md` во всех девяти.
- В `AuditRepo` запись про branch protection перестаёт быть `UNPROVEN`: появляется скриншот ruleset с датой и именем обязательного чека.
