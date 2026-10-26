#!/usr/bin/env bash
# Доказательство чистого клона, круг 63.
#
# Смысл: проверить не «в песочнице, где я это писала», а в дереве, собранном из remote. Отдельно
# от рабочей копии проверяется ровно то, что иначе остаётся на слове автора круга: что инструменты
# лежат в каноне, что их байты совпадают с тем, что о них записано в реестре, и что числа реестра
# сходятся с деревом без моего участия.
#
# Запуск:  bash scripts/atonement_proof_round63.sh [ref]
# ref по умолчанию — HEAD текущей ветки; после мержа круг обязан быть доказан на origin/main.
#
# Прошлый такой скрипт (atonement_proof_round61.sh, десять шагов) погиб вместе с коммитом круга 62:
# он лежал в песочнице, а не в main. Этот написан заново и лежит в репозитории; текст прежнего не
# восстановлен, и притворяться, что восстановлен, круг не будет.
#
# Починка этого же круга, пропечатанная, потому что она о способе доказательства: первый вариант
# писал строку статуса через `test -f … && say ок || say нет`, и `say` в ветке «ок» возвращал
# ненулевой код (последняя команда функции — `[ "$3" = fail ]`), из-за чего вторая ветка выполнялась
# тоже и отчёт печатал «нет» по шесть раз рядом с «да». Функция теперь возвращает 0 явно, а
# развилки написаны через if/else: проверочный вывод, который зависит от кода возврата сообщения,
# неотличим от проверочного вывода, который зависит от состояния дерева.
set -uo pipefail

REF="${1:-HEAD}"
SANDBOX="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d /tmp/atonement-proof63.XXXXXX)"
FAIL=0
n=0

say() {
  n=$((n + 1))
  printf '%2d) %-60s %s\n' "$n" "$1" "$2"
  if [ "${3:-ok}" = "fail" ]; then FAIL=1; fi
  return 0
}

echo "клон ${REF} → ${WORK}"
git -C "$SANDBOX" log -1 --format='исходный коммит: %H %s' "$REF" | head -1

BRANCH="$(git -C "$SANDBOX" rev-parse --abbrev-ref HEAD)"
SHA="$(git -C "$SANDBOX" rev-parse "$REF")"
git clone -q --no-local --depth 1 --branch "$BRANCH" "file://$SANDBOX" "$WORK/clone" || git clone -q "file://$SANDBOX" "$WORK/clone"
cd "$WORK/clone" || { echo "не удалось склонировать"; exit 1; }
if ! git checkout -q "$SHA" 2>/dev/null; then
  git fetch -q origin "$SHA" && git checkout -q FETCH_HEAD
fi
# Полная история нужна не «для красоты», а потому что без неё правило 20 и пересъёмщик обязаны
# объявить недоказуемость: мы проверяем и то, что при неполной истории они объявляют недоказуемость словами, а не молчанием.
git fetch -q --unshallow origin "$BRANCH" 2>/dev/null || git fetch -q --deepen 2400 origin "$BRANCH" || true
git fetch -q origin "+refs/heads/main:refs/remotes/origin/main" || \
  git update-ref refs/remotes/origin/main "$(git rev-parse origin/$BRANCH 2>/dev/null || echo HEAD)"

if [ "$(git rev-parse --is-shallow-repository)" = "false" ]; then
  say "клон не shallow (в shallow git-замеры врут)" "да"
else
  say "клон не shallow" "нет — история не достана, git-замеры не исполнимы" fail
fi
if git rev-parse --verify -q origin/main > /dev/null; then
  say "локальный origin/main разрешается ($(git rev-list --count origin/main) коммитов)" "да"
else
  say "локальный origin/main" "нет — аудит sha-ссылок будет объявлен недоказанным" fail
fi

echo "--- содержательное состояние ---"
if [ -f "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json" ]; then
  say "корпус на месте ($(wc -c < "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json") B)" "да"
else
  say "корпус" "нет файла" fail
fi
for f in scripts/validate_atonement_corpus_integrity.py scripts/atonement_claim_register.py \
         scripts/atonement_reshoot_state.py scripts/atonement_drive_mirror_round63.py \
         scripts/atonement_library_index_round63.py scripts/run_atonement_mutation_battery.py \
         scripts/atonement_proof_round63.sh; do
  if [ -f "$f" ]; then
    say "инструмент в каноне: $(basename "$f") ($(wc -c < "$f") B)" "да"
  else
    say "инструмент в каноне: $f" "нет файла" fail
  fi
done
if git ls-files --error-unmatch scripts/atonement_reshoot_state.py > /dev/null 2>&1; then
  say "пересъёмщик чисел лежит в git, а не в песочнице" "да"
else
  say "пересъёмщик в git" "нет — круг 62 на этом же месте потерял всё" fail
fi

echo "--- числа реестра против дерева ---"
out=$(python3 -B scripts/validate_atonement_corpus_integrity.py 2>&1 | tail -1)
case "$out" in
  *"INTEGRITY: PASS"*) say "гейт на чистом клоне" "PASS" ;;
  *)                   say "гейт" "$out" fail ;;
esac
out=$(python3 -B scripts/atonement_reshoot_state.py --check 2>&1 | tail -1)
case "$out" in
  *"RE-SHOOT: PASS"*) say "пересъёмщик: --check" "${out#*PASS — }" ;;
  *)                  say "пересъёмщик: --check" "$out" fail ;;
esac
if [ -z "$(git status --porcelain)" ]; then
  say "ни одна сверка ничего не записала в чистом клоне" "да"
else
  say "сверки обязаны быть только читающими" "изменили дерево: $(git status --porcelain | head -2 | tr '\n' ' ')" fail
fi
lanes=$(python3 -B scripts/atonement_claim_register.py --check 2>&1 | grep -c "сходится")
if [ "$lanes" = "5" ]; then
  say "реестр доводов: 5 ланов сходятся" "да"
else
  say "реестр доводов" "сходится ланов: $lanes" fail
fi
cross=$(python3 -B scripts/atonement_claim_register.py --cross 2>&1 | grep '^\[root\] сверка' \
        | grep -o 'ссылок вне обхода лана [0-9]*' | grep -o '[0-9]*$')
declared=$(python3 -c "import json;print(json.load(open('ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json'))['fourPointMassRegistry20261023']['cardProseCrossCheck20261026r60']['числа']['ссылокВнеОбходаЛана'])")
if [ -n "$cross" ] && [ "$cross" = "$declared" ]; then
  say "--cross root: ссылок вне обхода $cross — равно реестру" "да"
else
  say "--cross root" "съём ${cross:-нет вывода} ≠ реестр ${declared:-?}" fail
fi

echo "--- зеркала, записи, инвентарь ---"
python3 - <<'PY'
import hashlib, json, subprocess, sys
from pathlib import Path
corp = json.loads(Path("ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json").read_text(encoding="utf-8"))
rec = corp["driveMirrors"]["corpusSnapshotRound63_20261026"]
live = rec["живойСлепок"]
path = "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
blob = subprocess.run(["git", "show", f"{live['gitShaAtUpload']}:{path}"], capture_output=True).stdout
gmd5 = hashlib.md5(blob).hexdigest()
res = []
res.append(("слепок Drive = blob %s: %d B, md5 %s…" % (live["gitShaAtUpload"][:7], len(blob), gmd5[:12]),
            len(blob) == live["байт"] and gmd5 == live["md5Drive"]))
gap = Path(path).stat().st_size - len(blob)
res.append(("разрыв зеркала с деревом: записан %d, в этом дереве %d"
            % (rec["разрывСДеревом"]["байт"], gap), gap == rec["разрывСДеревом"]["байт"]))
cen = corp["libraryIndex20261023"]
idx = json.loads(Path("ИСКУПЛЕНИЕ/data/atonement-library-index.json").read_text(encoding="utf-8"))
recs = idx["records"]
res.append(("ценз индекса: реестр %d/%d, обход %d/%d" % (cen["records"], cen["files"], len(recs),
            len([r for r in recs if r.get("kind") == "file"])),
            cen["records"] == len(recs)))
inv = corp["reproducibility20261022"]["pipelineScripts20261026r63"]
same, lines_same = True, True
for rel, v in inv["файлы"].items():
    if not isinstance(v, dict):
        same = False
        continue
    raw = Path(rel).read_bytes()
    same &= hashlib.md5(raw).hexdigest() == v["md5"] and len(raw) == v["байт"]
    lines_same &= raw.count(b"\n") == v["строк"]
res.append(("инвентарь инструментов (%d файла, %d B) равен байтам канона" % (inv["файлов"], inv["байт"]),
            same and lines_same))
new = recs[-1]
res.append(("последняя запись индекса — живой слепок %s… (%d B, %s)"
            % (new["driveId"][:7], new["bytes"], new["rights"]),
            new["driveId"] == live["driveId"] and new["rights"] == "mirror_of_git"
            and new["role"] == "ssot-corpus-snapshot" and new["bytes"] == len(blob)))
old = [r for r in recs if r.get("driveId") == "1sQ_0B5-9WFnZfmVcJSkF3DIwSbkqf3Tn"]
res.append(("прежняя запись вытеснена (%s, имя начинается с «%s»)"
            % (old[0]["rights"], old[0]["name"][:8]) if old else "запись круга 60 в индексе не найдена",
            bool(old) and old[0]["rights"] == "HOLD_superseded" and old[0]["name"].startswith("УСТАРЕЛО")))
doc = Path("ИСКУПЛЕНИЕ/18_SERIES_AUDIT_AND_ARCS_2026-10-26.md").read_text(encoding="utf-8")
audit = corp["fourPointMassRegistry20261023"]["seriesAuditRound5820261026"]["файлАудита"]
res.append(("аудит: реестр знает %d B / %d строк, файл такой же" % (audit["байт"], audit["строк"]),
            audit["байт"] == len(doc.encode()) and audit["строк"] == doc.count("\n")))
res.append(("в аудите есть §9.3 этого круга", "### 9.3" in doc))
bad = 0
for msg, good in res:
    print("%3s) %s" % ("OK" if good else "!!", msg))
    if not good:
        bad += 1
sys.exit(0 if bad == 0 else 1)
PY
if [ $? -eq 0 ]; then
  say "сверка зеркал, инвентаря и бухгалтерии индекса" "сошлось"
else
  say "сверка зеркал и инвентаря" "расхождение — см. строки !!" fail
fi

echo "--- батарея мутаций (ловит ли гейт то, что обещает) ---"
out=$(timeout 1500 python3 -B scripts/run_atonement_mutation_battery.py 2>&1 | grep "поймано случаев")
case "$out" in
  *"непопаданий: 0"*"не проверено: 0"*) say "батарея: ${out#*случаев: }" "да" ;;
  *)                                      say "батарея" "${out:-нет строки результата}" fail ;;
esac

cd / && rm -rf "$WORK"
echo
if [ "$FAIL" -eq 0 ]; then
  echo "ДОКАЗАНО: $n проверок на чистом клоне, отказов нет"
else
  echo "НЕ ДОКАЗАНО: есть отказы — см. строки с «!!» и со статусом «нет»"
fi
exit "$FAIL"
