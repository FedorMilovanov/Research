#!/usr/bin/env bash
# Применяет контур secret-scan к рабочему клону video-channel-manager
# и проверяет его собственным контрактом пинов из tests/.
#
#   bash apply.sh /путь/к/клону/video-channel-manager
#
# Скрипт ничего не пушит и не коммитит: он кладёт файл и запускает проверки,
# чтобы решение о коммите принимал человек.

set -euo pipefail

TARGET="${1:-}"
if [ -z "$TARGET" ] || [ ! -d "$TARGET/.github/workflows" ]; then
  echo "usage: bash apply.sh /path/to/video-channel-manager" >&2
  exit 2
fi

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/.github/workflows/secret-scan.yml"
DST="$TARGET/.github/workflows/secret-scan.yml"

if [ -e "$DST" ]; then
  if cmp -s "$SRC" "$DST"; then
    echo "skip (identical): .github/workflows/secret-scan.yml"
  else
    echo "refuse: .github/workflows/secret-scan.yml already exists and differs" >&2
    exit 1
  fi
else
  cp "$SRC" "$DST"
  echo "created: .github/workflows/secret-scan.yml"
fi

cd "$TARGET"

echo
echo "== контракт пинов и инварианты workflows =="
python3 -m pytest tests/test_github_action_pins.py tests/test_ref_binding_inventory.py -q

echo
echo "== YAML всех workflow =="
python3 - <<'PY'
import glob, yaml, sys
paths = sorted(glob.glob(".github/workflows/*.yml"))
bad = []
for path in paths:
    doc = yaml.load(open(path, encoding="utf-8"), Loader=yaml.BaseLoader)
    if not (isinstance(doc, dict) and "on" in doc and doc.get("jobs")):
        bad.append(path)
print(f"{len(paths)} workflow files, {len(bad)} invalid")
sys.exit(1 if bad else 0)
PY

echo
echo "готово: изменения не закоммичены"
