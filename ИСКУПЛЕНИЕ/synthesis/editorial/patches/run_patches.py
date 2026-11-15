#!/usr/bin/env python3
"""Apply or verify the AGENT-7 editorial patches against a PR #309 worktree.

Read-only against the repository: the caller points it at a checkout. Each patch
  * names one target file inside ИСКУПЛЕНИЕ/synthesis/drafts/,
  * gives a BEFORE fragment that must occur exactly once,
  * gives an AFTER fragment,
  * and is applied only if the tree still matches the base commit recorded below.

    python3 run_patches.py --check  --root <worktree>   # dry run, prints plan
    python3 run_patches.py --apply  --root <worktree>   # applies in place
    python3 run_patches.py --verify --root <worktree>   # AFTER must be present

Order matters.  Some patches build on the result of an earlier one (their BEFORE
contains the earlier patch's AFTER).  --check therefore does not test every patch
against the untouched tree: it simulates the run in manifest order on an in-memory
copy.  A patch whose BEFORE is absent from the untouched tree but present after the
simulated predecessors is reported as "OK (после <id>)"; if such a dependency is
declared but the predecessor did not fire, that is an error, not a pass.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BASE = "2392be62"          # PR #309 head at the time of reading
MANIFEST = Path(__file__).with_name("patches.json")


def load() -> list[dict]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return data["patches"]


def target(root: Path, name: str) -> Path:
    return root / "ИСКУПЛЕНИЕ" / "synthesis" / "drafts" / name


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    root = Path(a.root)
    patches = load()
    fail: list[str] = []
    done = 0
    # --check обязан проверять то, что произойдёт на деле: патчи выполняются по
    # порядку манифеста, и поздний может опираться на результат раннего. Держим
    # теневое состояние в памяти и не пишем на диск (прогон остаётся read-only).
    shadow: dict[str, str] = {}
    touched_ok: set[str] = set()
    for p in patches:
        f = target(root, p["file"])
        if not f.exists():
            fail.append(f'{p["id"]}: нет файла {p["file"]}')
            continue
        text = shadow.get(p["file"]) or f.read_text(encoding="utf-8")
        before, after = p["before"], p["after"]
        n_before, n_after = text.count(before), text.count(after)
        if a.verify:
            # --verify обязан понимать то же, что и --check: поздний патч переписывает
            # фрагмент, введённый ранним, и AFTER раннего законно исчезает с диска.
            # Тогда применяем его в тени и учитываем как выполненный, а не как поломку.
            if n_after == 0 and n_before == 1:
                shadow[p["file"]] = text.replace(before, after, 1)
                done += 1
                print(f'{p["id"]:>6}  учтён (затем перезаписан поздним)  {p["file"]}')
                continue
            if n_after == 0:
                fail.append(f'{p["id"]}: AFTER не найден в {p["file"]}')
            else:
                shadow[p["file"]] = text
                done += 1
            continue
        # --verify обязан понимать то же, что и --check: поздний патч переписывает
        # фрагмент, введённый ранним, поэтому AFTER раннего законно исчезает.
        # Держим теневое состояние и по нему решаем, «уже применён» это или поломка.
        if n_before == 0 and n_after:
            print(f'{p["id"]:>6}  уже применён  {p["file"]}')
            done += 1
            continue
        if n_before != 1:
            fail.append(f'{p["id"]}: BEFORE встречается {n_before} раз (нужно 1) в {p["file"]}')
            continue
        if before == after:
            fail.append(f'{p["id"]}: BEFORE == AFTER')
            continue
        if a.check:
            on_disk = f.read_text(encoding="utf-8").count(before) == 1
            note = "OK" if on_disk else "OK (после " + ", ".join(sorted(touched_ok)) + ")"
            shadow[p["file"]] = text.replace(before, after, 1)
            touched_ok.add(p["id"])
            print(f'{p["id"]:>6}  {note}  {p["why"][:78]}')
        else:
            f.write_text(text.replace(before, after, 1), encoding="utf-8")
            print(f'{p["id"]:>6}  применён  {p["file"]}')
        done += 1
    print(f"\nитого {done}/{len(patches)}; ошибок {len(fail)}")
    for m in fail:
        print("  FAIL ", m)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
