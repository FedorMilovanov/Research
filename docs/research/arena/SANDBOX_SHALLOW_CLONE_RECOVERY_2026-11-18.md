# Песочница поднялась shallow-клоном: безопасное восстановление указателя ветки

**Дата:** 2026-11-18
**Роль:** рабочая записка о среде, `NOT_AUTHORITY` в отношении корпуса
**Источник исправленного черновика:** #621, git blob `aaef9274f73c258d22bad189d23eacc0b460b411`
**Граница:** процедура восстанавливает локальную историю и указатель уже существующей удалённой ветки. Она не меняет корпус, не создаёт evidence, не снимает HOLD и не разрешает публикацию.

## 1. Когда применять

Типичный набор признаков:

- `git rev-parse --is-shallow-repository` печатает `true`;
- `git log --oneline -1` показывает базовый коммит, хотя удалённая рабочая ветка ушла вперёд;
- `git status` показывает большой слой файлов верхушки ветки как незакоммиченные изменения;
- проверки, которым нужна история (`commitTimeChecks`, merge-base, чтение старых blob), честно отказываются работать.

Процедура ниже предназначена только для случая, когда известная ветка уже отправлена в `origin`, а нужные байты рабочего дерева находятся на диске. Если есть известные **неотправленные коммиты**, detached HEAD, неизвестное имя ветки или сомнение в том, какой remote является authority, нужно остановиться: этот рецепт не доказывает безопасную цель reset.

## 2. Почему исходная команда была недостаточна

Черновик #621 предлагал:

```text
git fetch origin arena/<ветка>
git reset --mixed origin/arena/<ветка>
```

В свежем single-branch/shallow clone первая команда обновляет `FETCH_HEAD`, но не обязана создать локальный remote-tracking ref `refs/remotes/origin/arena/<ветка>`. Следующий reset поэтому может ссылаться на несуществующее или старое имя. Исправление — fetch с явным refspec `refs/heads/...:refs/remotes/origin/...` и проверка полученного object ID до reset.

## 3. Безопасная процедура

Команды не переключают и не создают ветку. В Arena нужно использовать только закреплённую за текущей сессией ветку.

```bash
set -eu

branch=${RECOVERY_BRANCH:-$(git branch --show-current)}
test -n "$branch" || {
  echo "detached HEAD: задайте RECOVERY_BRANCH только после проверки authority" >&2
  exit 1
}

backup_dir=$(mktemp -d /tmp/research-shallow-recovery.XXXXXX)
git rev-parse HEAD > "$backup_dir/head-before.txt"
git status --porcelain=v1 > "$backup_dir/status-before.txt"
git diff --binary HEAD > "$backup_dir/tracked.patch"
git ls-files --others --exclude-standard -z \
  | tar --null --files-from=- -cf "$backup_dir/untracked.tar"
printf 'backup: %s\n' "$backup_dir"

if test "$(git rev-parse --is-shallow-repository)" = true; then
  git fetch --unshallow origin
fi

git fetch origin \
  "refs/heads/$branch:refs/remotes/origin/$branch"
target=$(git rev-parse --verify "refs/remotes/origin/$branch^{commit}")
printf 'target: %s\n' "$target"

git reset --mixed "$target"
```

Почему это сохраняет рабочие байты:

- `fetch` меняет только Git objects/refs;
- `reset --mixed` двигает `HEAD` и пересобирает index, но не переписывает working tree;
- `git diff --binary HEAD` сохраняет аварийную копию всех tracked-изменений относительно старого HEAD, включая staged слой;
- untracked-файлы отдельно сохранены в tar с NUL-разделителями.

Backup — страховка, а не новый SSOT. Не коммитить и не публиковать его; после проверки удалить по правилам среды. Если рабочее дерево содержит private material, не переносить backup во внешнее хранилище без отдельного разрешения.

## 4. Проверка результата

```bash
test "$(git rev-parse --is-shallow-repository)" = false
test "$(git rev-parse HEAD)" = \
  "$(git rev-parse "refs/remotes/origin/$branch")"
git diff --cached --exit-code
git status --porcelain=v1
```

Последняя команда должна показывать только настоящие локальные правки поверх полученной верхушки. Она не обязана быть пустой. После этого можно повторить тот гейт, который до восстановления истории отказался работать.

Локальный regression fixture воспроизводит fresh `--depth 1 --single-branch` clone, явным refspec получает ветку с изменённым и новым файлом, выполняет mixed reset и доказывает, что единственная дополнительная локальная строка сохранилась:

```bash
python3 -B -m unittest discover -s scripts \
  -p 'test_sandbox_shallow_clone_recovery.py' -v
```

Fixture использует только временные локальные repositories и `file://`; сеть и рабочий repository не изменяются.

## 5. Чего не делать

- Не использовать `git reset --hard`, `git checkout -f` или `git clean`: они могут уничтожить нужные рабочие байты.
- Не делать `git add -A` и один коммит всего видимого слоя: так история ветки превращается в дубликат.
- Не считать corpus-гейт сломанным, пока shallow-среда не восстановлена: отсутствие читаемой истории — не доказательство согласованности.
- Не подставлять предполагаемый SHA или ветку. Цель должна быть прочитана из точного remote-tracking ref, созданного явным refspec.
- Не делать force-push и не переключаться на другую ветку как часть восстановления.
