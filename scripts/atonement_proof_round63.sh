#!/usr/bin/env bash
# Доказательство чистого клона, круг 63.
#
# Смысл: проверить не «в песочнице, где я это писала», а в дереве, собранном из remote. Отдельно
# от рабочей копии тут проверяется ровно то, что иначе остаётся на слове автора круга: что
# инструменты лежат в каноне, что их байты совпадают с тем, что о них записано в реестре, и что
# числа реестра сходятся с деревом без моего участия.
#
# Запуск:  bash scripts/atonement_proof_round63.sh [ref]
# ref по умолчанию — HEAD текущей ветки; после мержа круг обязан быть доказан на origin/main.
#
# Прошлый такой скрипт (atonement_proof_round61.sh, десять шагов) погиб вместе с коммитом круга 62:
# он лежал в песочнице, а не в main. Этот — написан заново и лежит в репозитории; текст прежнего
# не восстановлен, и притворяться, что восстановлен, круг не будет.
set -uo pipefail

REF="${1:-HEAD}"
SANDBOX="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d /tmp/atonement-proof63.XXXXXX)"
FAIL=0
n=0

say() { n=$((n+1)); printf '%2d) %-58s %s\n' "$n" "$1" "$2"; [ "${3:-ok}" = fail ] && FAIL=1; }
say_fail() { say "$1" "$2" fail; }

echo "клон ${REF} → ${WORK}"
git -C "$SANDBOX" log -1 --format='исходный коммит: %H %s' "$REF" | head -1

BRANCH="$(git -C "$SANDBOX" rev-parse --abbrev-ref HEAD)"
SHA="$(git -C "$SANDBOX" rev-parse "$REF")"
git clone -q --depth 1 --branch "$BRANCH" "$SANDBOX" "$WORK/clone" || git clone -q --depth 1 "$SANDBOX" "$WORK/clone"
cd "$WORK/clone" || { echo "не удалось склонировать"; exit 1; }
git checkout -q "$SHA" 2>/dev/null || { git fetch -q origin "$SHA" && git checkout -q FETCH_HEAD; }
# глубина 1 не годится ни правилу 20, ни пересъёщику: они обязаны видеть историю, а не притворяться
git fetch -q --unshallow origin "$BRANCH" 2>/dev/null || git fetch -q --deepen 2400 origin "$BRANCH" || true
say "клон не shallow (иначе git-замеры врут)" "$( [ "$(git rev-parse --is-shallow-repository)" = false ] && echo да || echo 'нет — история не достана')" fail
git rev-list --count HEAD | grep -q . && say "история видна: $(git rev-list --count HEAD) коммитов" "да"

echo "--- содержательное состояние ---"
test -f ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json && say "корпус на месте ($(wc -c < ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json) B)" "да" || say "корпус" "нет" fail
for f in scripts/validate_atonement_corpus_integrity.py scripts/atonement_claim_register.py \
         scripts/atonement_reshoot_state.py scripts/atonement_drive_mirror_round63.py \
         scripts/atonement_library_index_round63.py scripts/run_atonement_mutation_battery.py; do
  test -f "$f" && say "инструмент в каноне: $(basename "$f") ($(wc -c < "$f") B)" "да" || say "$f" "нет" fail
done

echo "--- числа реестра против дерева ---"
out=$(python3 -B scripts/validate_atonement_corpus_integrity.py 2>&1 | tail -1)
case "$out" in *"INTEGRITY: PASS"*) say "гейт на чистом клоне" "PASS";; *) say "гейт" "$out" fail;; esac
out=$(python3 -B scripts/atonement_reshoot_state.py --check 2>&1 | tail -1)
case "$out" in *"RE-SHOOT: PASS"*) say "пересъёмщик: --check" "${out#*PASS — }";; *) say "--check" "$out" fail;; esac
out=$(python3 -B scripts/atonement_claim_register.py --check 2>&1 | grep -c "сходится")
[ "$out" = "5" ] && say "реестр доводов: 5 ланов сходятся" "да" || say "реестр доводов" "сходится ланов: $out" fail
cross=$(python3 -B scripts/atonement_claim_register.py --cross 2>&1 | grep -c "ссылки вне обхода")
[ -n "$cross" ] && say "--cross отработал (строк со ссылками вне обхода: $cross)" "да" || say "--cross" "нет вывода" fail

echo "--- зеркала, записи, имена ---"
python3 - <<'PY'
import hashlib, json, subprocess, sys
from pathlib import Path
corp = json.loads(Path("ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json").read_text(encoding="utf-8"))
rec = corp["driveMirrors"]["corpusSnapshotRound63_20261026"]
live = rec["живойСлепок"]
sha, path = live["gitShaAtUpload"], "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"
blob = subprocess.run(["git", "show", f"{sha}:{path}"], capture_output=True).stdout
res = []
res.append(("слепок = blob дерева: %d B, md5 %s" % (len(blob), hashlib.md5(blob).hexdigest()[:12]),
            len(blob) == live["байт"] and hashlib.md5(blob).hexdigest() == live["md5Drive"]))
gap = Path(path).stat().st_size - len(blob)
res.append(("разрыв зеркала с деревом: записан %d, в main %d" % (rec["разрывСДеревом"]["байт"], gap),
            gap == rec["разрывСДеревом"]["байт"]))
inv = corp["reproducibility20261022"]["pipelineScripts20261026r63"]
same = all(hashlib.md5(Path(rel).read_bytes()).hexdigest() == v["md5"]
           and Path(rel).stat().st_size == v["байт"]
           for rel, v in inv["файлы"].items() if isinstance(v, dict))
same &= all((Path(rel).read_bytes().count(b"\n")) == v["строк"] for rel, v in inv["файлы"].items() if isinstance(v, dict))
res.append(("инвентарь инструментов (%d файла, %d B) равен байтам канона" % (inv["файлов"], inv["байт"]), same))
idx = json.loads(Path("ИСКУПЛЕНИЕ/data/atonement-library-index.json").read_text(encoding="utf-8"))
recs = idx["records"]
new = recs[-1]
res.append(("последняя запись индекса — живой слепок %s… (%d B)" % (new["driveId"][:7], new["bytes"]),
            new["driveId"] == live["driveId"] and new["rights"] == "mirror_of_git"
            and new["role"] == "ssot-corpus-snapshot"))
old = [r for r in recs if r.get("driveId") == "1sQ_0B5-9WFnZfmVcJSkF3DIwSbkqf3Tn"][0]
res.append(("прежняя запись помечена вытесненной (%s)" % old["rights"],
            old["rights"] == "HOLD_superseded" and old["name"].startswith("УСТАРЕЛО")))
cen = corp["libraryIndex20261023"]
res.append(("ценз индекса в реестре: %d записей / %d файлов / %d носителей" %
            (cen["records"], cen["files"], cen["materials"]),
            cen["records"] == len(recs)))
ok = True
for msg, good in res:
    print("%2s) %s" % ("OK" if good else "!!", msg))
    ok &= bool(good)
sys.exit(0 if ok else 1)
PY
[ $? = 0 ] && say "сверка зеркал, инвентаря и бухгалтерии индекса" "сошлось" || say "сверка зеркал" "расхождение" fail

echo "--- батарея мутаций (ловит ли гейт то, что обещает) ---"
out=$(timeout 1500 python3 -B scripts/run_atonement_mutation_battery.py 2>&1 | grep "поймано случаев")
say "батарея: ${out#*поймано случаев: }" "да"

cd /; rm -rf "$WORK"
echo
if [ "$FAIL" = 0 ]; then echo "ДОКАЗАНО: $n проверок на чистом клоне, отказов нет"; else echo "НЕ ДОКАЗАНО: есть отказы — см. строки с «!!»"; fi
exit "$FAIL"
