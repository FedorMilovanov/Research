#!/usr/bin/env python3
"""Один прогон всех гейтов HOLD-контура.

Зачем: проверок стало пять, и каждая живёт отдельным скриптом со своим
`--check`. Пока они запускаются по памяти, набор проверок зависит от того, кто
и что вспомнил. Этот раннер фиксирует состав и порядок, ничего не записывает в
рабочее дерево и возвращает ненулевой код, если хотя бы один гейт упал.

    python3 -B scripts/run_research_gates.py
    python3 -B scripts/run_research_gates.py --verbose   # печатать вывод гейтов

Что проверяется:

1. `HOLD_INVENTORY.md`/`.json` совпадают с генератором (реестры не разъехались
   с отчётом).
2. Матрица прав совпадает с JSON и с фильтром инвентаря, категории и счётчики
   сходятся.
3. Разбор подкаталогов STEPBible согласован и закрепление (коммит, размер,
   SHA-256) не подменено.
4. Зеркало `SUNO_HYMNS/RESEARCH/OPEN_HOLDS.md` совпадает с реестрами SUNO
   (расхождение только в дате сборки — норма).
5. Действующая root authority резолвится через реестр, а не по имени файла.

Отдельно, как сведения, а не как приговор: сколько записей продвигаются в
публикацию с объявленным пробелом (`--promotion-gaps`) и сколько записей
объявлены недо-приобретёнными без HOLD (зеркальный аудит). Эти два числа
меняются от содержания работы, поэтому падать из-за них нельзя — но и молча
пропускать их нельзя.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

GATES = [
    ("HOLD inventory", ROOT, ["python3", "-B", "scripts/render_hold_inventory.py", "--check"]),
    ("Rights matrix", ROOT, ["python3", "-B", "scripts/render_rights_matrix.py", "--check"]),
    ("STEPBible subdataset terms", ROOT, ["python3", "-B", "scripts/stepbible_subdataset_terms.py", "--check"]),
    (
        "SUNO hold ledger",
        ROOT / "SUNO_HYMNS",
        ["python3", "-B", "scripts/render_hold_ledger.py", "--check"],
    ),
    ("Research root authority", ROOT, ["python3", "-B", "scripts/validate_research_root_authority.py"]),
]

INFORMATIONAL = [
    ("PROMOTE с объявленным пробелом", ROOT, ["python3", "-B", "scripts/audit_hold_coverage_gaps.py", "--promotion-gaps"]),
    ("Недо-приобретено без HOLD", ROOT, ["python3", "-B", "scripts/audit_hold_coverage_gaps.py"]),
    (
        "Недо-приобретено без поля holds",
        ROOT,
        ["python3", "-B", "scripts/audit_hold_coverage_gaps.py", "--no-holds-field"],
    ),
    (
        "HOLD назван прозой, а не полем",
        ROOT,
        ["python3", "-B", "scripts/audit_prose_holds.py"],
    ),
    (
        "Зеркала Drive: пары объект+коммит",
        ROOT,
        ["python3", "-B", "scripts/check_drive_mirror_pairs.py", "--summary"],
    ),
]


def run(cwd: pathlib.Path, cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main(argv: list[str]) -> int:
    verbose = "--verbose" in argv
    failed: list[str] = []
    for name, cwd, cmd in GATES:
        code, out = run(cwd, cmd)
        mark = "PASS" if code == 0 else "FAIL"
        print(f"[{mark}] {name}")
        if code != 0:
            failed.append(name)
            print(out.strip())
        elif verbose:
            print("       " + " ".join(out.strip().splitlines()[-1:]))

    for name, cwd, cmd in INFORMATIONAL:
        code, out = run(cwd, cmd)
        first = out.strip().splitlines()[0] if out.strip() else "(пусто)"
        print(f"[INFO] {name}: {first}")
        if code != 0:
            print(f"       гейт вернул {code}; это сведения, а не приговор")

    if failed:
        print(f"\nПровалено: {len(failed)} из {len(GATES)} — {', '.join(failed)}")
        return 1
    print(f"\nГейты HOLD-контура: {len(GATES)} из {len(GATES)} PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
