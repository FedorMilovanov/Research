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
# С круга 65 добавлена ещё одна: проб возмущением истории (три среды над одним деревом; числа обязаны
# не реагировать на рост `origin/main`, а в неполном клоне — отказывать словами). Он вызывается здесь же,
# потому что инструмент, который CI и доказательство не зовут, перестаёт ловить незаметно: ровно так
# пропал счётчик круга 62.
#
# С круга 64 к нему добавлены три проверки, которых в круге 63 не было: что порядок закрытия круга
# печатается без записи, что писатели записей не запускаются без подтверждённого номера, и что число
# среды, вписанное в сверяемое поле, ловится (в клонах вводится на минуту и откатывается `git
# checkout`). Файл по-прежнему называется round63 — по кругу, в котором он появился; проверки в нём
# не круговые, а именованные утраты (round61, round62) ничего не восстанавливают: прежнее имя
# `atonement_close_round.py` осталось занятом утраченным счётчиком, и новый инструмент нарочно
# называется иначе.
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
  # `set -u` поймал то, для чего эта строка теперь есть явно: `say` зовут с двумя аргументами, и
  # перенос метки на следующую строку без `\` молча превращал вторую половину в отдельную команду,
  # а шаг — в падение с «$2: unbound variable»
  : "${2:?say(<что>, <статус>[, fail]): статус обязателен — шаг без статуса неотличим от шага, которого не было}"
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
         scripts/atonement_round_close.py scripts/atonement_history_perturbation_probe.py \
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
declared=$(python3 -c "
import json
d = json.load(open('ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json', encoding='utf-8'))
for top in ('integrityGate', 'fourPointMassRegistry20261023'):
    blk = (d.get(top) or {}).get('cardProseCrossCheck20261026r60')
    if blk:
        print(blk['числа']['ссылокВнеОбходаЛана'])
        break
else:
    print('')
")
if [ -z "$declared" ]; then
  say "--cross root" "в реестре нет cardProseCrossCheck20261026r60 — сверять не с чем" fail
elif [ -n "$cross" ] && [ "$cross" = "$declared" ]; then
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
invk = sorted(k for k in corp["reproducibility20261022"] if k.startswith("pipelineScripts"))
if not invk:
    print("!! в реестре нет ни одного блока pipelineScripts — инвентарь инструментов снят с сверки")
    sys.exit(1)
inv = corp["reproducibility20261022"][invk[-1]]
same, lines_same = True, True
for rel, v in inv["файлы"].items():
    if not isinstance(v, dict):
        same = False
        continue
    raw = Path(rel).read_bytes()
    same &= hashlib.md5(raw).hexdigest() == v["md5"] and len(raw) == v["байт"]
    lines_same &= raw.count(b"\n") == v["строк"]
res.append(("инвентарь инструментов (%s: %d файла, %d B) равен байтам канона"
            % (invk[-1], inv["файлов"], inv["байт"]), same and lines_same))
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
res.append(("в аудите есть §9.3, §9.4 и §9.5; §9.5 называет проб и сводку по имени",
            "### 9.3" in doc and "### 9.4" in doc and "### 9.5" in doc
            and "atonement_history_perturbation_probe.py" in doc
            and "claimsPerRegistry" in doc))
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

echo "--- порядок закрытия круга и числа среды (круг 64) ---"
planout=$(python3 -B scripts/atonement_round_close.py --plan 2>&1)
plancode=$?
if [ "$plancode" = "0" ] && [ -z "$(git status --porcelain)" ] \
   && printf '%s' "$planout" | grep -q "писатели, только по явному подтверждению"; then
  say "close-round --plan печатает порядок и ничего не пишет" "да"
else
  say "close-round --plan" "код $plancode, грязь: $(git status --porcelain | head -1 | tr '\n' ' ')" fail
fi
before=$(md5sum ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json \
          ИСКУПЛЕНИЕ/data/atonement-library-index.json | md5sum | cut -d" " -f1)
refuse=$(python3 -B scripts/atonement_round_close.py --run --allow-appending-writers 2>&1)
rcode=$?
after=$(md5sum ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json \
         ИСКУПЛЕНИЕ/data/atonement-library-index.json | md5sum | cut -d" " -f1)
if [ "$rcode" = "2" ] && printf '%s' "$refuse" | grep -q "писатели разрешены флагом, но круг не назван" \
   && [ "$before" = "$after" ]; then
  say "писатели без номера круга не запущены, байты реестра не двинулись" "да"
else
  say "отказ запускать писателей" "код $rcode, байты целы: $([ "$before" = "$after" ] && echo да || echo нет)" fail
fi
python3 - <<'PYMUT'
import json
from pathlib import Path
p = Path("ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json")
c = json.loads(p.read_text(encoding="utf-8"))
c["integrityGate"]["shaCitationAudit20261023"]["gitObjectsConsidered"] = 14661
p.write_text(json.dumps(c, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
PYMUT
out=$(python3 -B scripts/atonement_reshoot_state.py --check 2>&1)
cc=$?
git checkout -- ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json
out2=$(python3 -B scripts/atonement_reshoot_state.py --check 2>&1)
if [ "$cc" != "0" ] && printf '%s' "$out" | grep -q "число обхода в сверяемом поле" \
   && printf '%s' "$out2" | grep -q "RE-SHOOT: PASS" && [ -z "$(git status --porcelain)" ]; then
  say "пересъёмщик ловит внедрённое число среды, откат побайтовый" "да"
else
  say "ловля числа среды" "код $cc; после отката: $(printf '%s' "$out2" | tail -1 | cut -c1-60)" fail
fi
cjk=$(python3 - <<'PYCJK'
import re
from pathlib import Path
lo, hi = chr(0x4E00), chr(0x9FFF)
files = ["ИСКУПЛЕНИЕ/18_SERIES_AUDIT_AND_ARCS_2026-10-26.md", "scripts/atonement_reshoot_state.py",
         "scripts/atonement_round_close.py", "scripts/atonement_proof_round63.sh",
         "scripts/atonement_history_perturbation_probe.py",
         "ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json"]
# цитаты исключаются тем же определением, что и в rules 19 и 2b: «ёлочки», `обратные кавычки`
# и "" — это чужое слово в чужом разборе, а не прилипшее при наборе. Первый вариант этого шага
# считал иероглифы по всему тексту и поймал цитату дефекта, которую круг 57 оставил нарочно.
QUOT = re.compile("\u00ab[^\u00bb]*\u00bb|`[^`]*`|\"[^\"\n]*\"")
bare = 0
quoted = 0
for f in files:
    t = Path(f).read_text(encoding="utf-8", errors="replace")
    stripped = QUOT.sub(" ", t)
    bare += sum(1 for ch in stripped if lo <= ch <= hi)
    quoted += sum(1 for ch in t if lo <= ch <= hi) - sum(1 for ch in stripped if lo <= ch <= hi)
print(bare, quoted)
PYCJK
)
read -r cjk_bare cjk_quoted <<< "$cjk"
if [ "$cjk_bare" = "0" ]; then
  say "восточного начертания в прозе и инструментах нет (в цитатах: $cjk_quoted)" "да"
else
  say "CJK-скан круга" "вне цитат: $cjk_bare (в цитатах $cjk_quoted) — правило гейта смотрит только сообщение коммита" fail
fi

echo "--- проб истории: сверяемые числа относятся к дереву, а не к клону (круг 65) ---"
timeout 120 python3 -B scripts/atonement_history_perturbation_probe.py --verdicts > /dev/null 2>&1 \
  && say "проб истории: способ отчёта различает 0/1/2" "да" \
  || say "проб истории: --verdicts" "отчёт проба не различает исход — см. вывод режима" fail
pout=$(timeout 900 python3 -B scripts/atonement_history_perturbation_probe.py HEAD --selftest 2>&1)
case "$pout" in
  *"ПРОБ ИСТОРИИ: PASS"*) say "проб истории: среды из одного дерева, дрейфа нет" "да" ;;
  *"СРЕДА НЕГОДНА"*)      say "проб истории" "среда не годна: $(printf '%s\n' "$pout" | tail -1 | cut -c1-64) — это не проверка" fail ;;
  *)                      say "проб истории" "$(printf '%s\n' "$pout" | tail -2 | tr '\n' ' ' | cut -c1-88)" fail ;;
esac

echo "--- батарея мутаций (ловит ли гейт то, что обещает) ---"
out=$(timeout 1500 python3 -B scripts/run_atonement_mutation_battery.py 2>&1 | grep "поймано случаев")
case "$out" in
  *"непопаданий: 0"*"не проверено: 0"*) say "батарея: ${out#*случаев: }" "да" ;;
  *)                                      say "батарея" "${out:-нет строки результата}" fail ;;
esac

echo "--- ловушка правила, смягчённого кругом 65 ---"
tout=$(timeout 300 python3 -B scripts/atonement_reshoot_state.py --rule-trap 2>&1); tc=$?
if [ "$tc" = 0 ]; then
  case "$tout" in
    *"ЛОВУШКА ПРАВИЛА ДАТ: ловит незаконный порядок"*)
      say "ловушка правила дат: смягчение не есть заглушка" "да" ;;
    *)
      say "ловушка правила дат" "код 0, но вердикта нет: $(printf '%s' "$tout" | tail -1 | cut -c1-64)" fail ;;
  esac
else
  say "ловушка правила дат" "код $tc: $(printf '%s' "$tout" | tail -1 | cut -c1-64)" fail
fi

cd / && rm -rf "$WORK"
echo
if [ "$FAIL" -eq 0 ]; then
  echo "ДОКАЗАНО: $n проверок на чистом клоне, отказов нет"
else
  echo "НЕ ДОКАЗАНО: есть отказы — см. строки с «!!» и со статусом «нет»"
fi
exit "$FAIL"
