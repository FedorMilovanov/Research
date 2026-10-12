#!/usr/bin/env bash
# Единый прогон всех проверок под-корпуса ИСКУПЛЕНИЕ/nt.
#
# Зачем: проверки были разбросаны по четырём инструментам, и «всё зелёное»
# означало «я запустил то, что вспомнил». Здесь один вход, и он печатает числа,
# а не только «OK».
#
# Использование:  bash ИСКУПЛЕНИЕ/nt/tools/run_all_checks.sh
# Выходит с кодом 1, если хоть одна проверка упала (кроме известного красного
# Genesis 6, который печатается как BASELINE-RED и на код не влияет).
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
T="ИСКУПЛЕНИЕ/nt/tools"
fail=0

echo "=== 1. свидетели (пины sha256) ==="
bash "$T/fetch_nt_corpus.sh" 2>&1 | tail -2 || fail=1

echo; echo "=== 2. греческие цитаты против S1/S5 ==="
python3 "$T/verify_nt_citations.py" 2>&1 | tail -1 || fail=1

echo; echo "=== 3. то же с верхнеуровневыми файлами ==="
NT_EXTRA_CARDS="ИСКУПЛЕНИЕ/04_LIMITED_VS_UNIVERSAL_QUESTION_MAP.md:ИСКУПЛЕНИЕ/12_HARD_TEXTS_EXTENT_CARDS.md:ИСКУПЛЕНИЕ/00_README_AND_NAVIGATION.md:ИСКУПЛЕНИЕ/05_SOURCE_REGISTRY_AND_ACQUISITION_QUEUE.md" \
  python3 "$T/verify_nt_citations.py" 2>&1 | tail -1 || fail=1

echo; echo "=== 4. дисциплина карточек (ось, ссылки, чтения, запретные формулы) ==="
python3 "$T/check_nt_card_discipline.py" 2>&1 | tail -6 || fail=1

echo; echo "=== 5. сверка MT ↔ LXX ==="
python3 "$T/mt_lxx_collation.py" 2>&1 | tail -1 || fail=1

echo; echo "=== 6. аппарат SBLGNT ==="
python3 "$T/sbl_apparatus.py" 2>&1 | head -1 || fail=1

echo; echo "=== 7. аппарат по всем перикопам §3.2 ==="
python3 "$T/pericope_apparatus_sweep.py" 2>&1 | head -3 || fail=1

echo; echo "=== 8. валидаторы репозитория ==="
for v in research_root_authority repository_authority_integrity genesis6_authority_manifest; do
  python3 "scripts/validate_$v.py" >/dev/null 2>&1
  rc=$?
  if [ "$v" = genesis6_authority_manifest ] && [ "$rc" -ne 0 ]; then
    echo "  $v: BASELINE-RED (shallow clone: authorityBaseCommit недоступен) — не чиним"
  else
    echo "  $v: rc=$rc"; [ "$rc" -ne 0 ] && fail=1
  fi
done

echo
[ "$fail" -eq 0 ] && echo "ИТОГ: все проверки зелёные (кроме известного красного Genesis 6)." \
                  || { echo "ИТОГ: ЕСТЬ ПАДЕНИЯ."; exit 1; }
