#!/usr/bin/env bash
# Устанавливает security baseline в целевой репозиторий.
#
# Использование:
#   ./install.sh /путь/к/репозиторию [--force]
#
# Без --force существующие файлы не перезаписываются: печатается предупреждение.
set -euo pipefail

target="${1:-}"
force="${2:-}"

if [ -z "$target" ]; then
  echo "usage: $0 /path/to/repo [--force]" >&2
  exit 2
fi

if [ ! -d "$target/.git" ]; then
  echo "error: $target is not a git repository" >&2
  exit 2
fi

repo_name="$(basename "$(git -C "$target" rev-parse --show-toplevel)")"
src_dir="$(cd "$(dirname "$0")" && pwd)"

install_file() {
  local rel="$1"
  local dest="$target/$rel"
  mkdir -p "$(dirname "$dest")"

  if [ -e "$dest" ] && [ "$force" != "--force" ]; then
    echo "skip (exists): $rel"
    return 0
  fi

  sed "s/{{REPO}}/$repo_name/g" "$src_dir/$rel" > "$dest"
  echo "write: $rel"
}

install_file ".github/workflows/security-baseline.yml"
install_file "SECURITY.md"

# .gitleaks.toml создаётся только если его нет: существующий конфиг трогать нельзя.
if [ -e "$target/.gitleaks.toml" ]; then
  echo "skip (exists): .gitleaks.toml"
else
  cp "$src_dir/.gitleaks.toml" "$target/.gitleaks.toml"
  echo "write: .gitleaks.toml"
fi

# Dependabot — только если файла нет вовсе.
if [ -e "$target/.github/dependabot.yml" ]; then
  echo "skip (exists): .github/dependabot.yml"
else
  cp "$src_dir/dependabot.yml" "$target/.github/dependabot.yml"
  echo "write: .github/dependabot.yml"
fi

cat <<EOF

Готово. Дальше:

  cd $target
  git checkout -b security/baseline
  git add .github SECURITY.md .gitleaks.toml
  git commit -s -m "ci(security): add secret scanning, dependency audit and workflow hygiene gate"
  git push -u origin security/baseline

Затем открой PR. Первый прогон намеренно строгий: если он падает на истории —
это находка, а не повод ослабить гейт.

Не забудь настройки репозитория (файлом не выражаются):
  Settings → Code security → Secret scanning + Push protection → Enable
  Settings → Rules → New ruleset: require status check "Security baseline"
EOF
