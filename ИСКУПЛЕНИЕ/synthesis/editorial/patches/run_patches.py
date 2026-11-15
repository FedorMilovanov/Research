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
    for p in patches:
        f = target(root, p["file"])
        if not f.exists():
            fail.append(f'{p["id"]}: нет файла {p["file"]}')
            continue
        text = f.read_text(encoding="utf-8")
        before, after = p["before"], p["after"]
        n_before, n_after = text.count(before), text.count(after)
        if a.verify:
            if n_after == 0:
                fail.append(f'{p["id"]}: AFTER не найден в {p["file"]}')
            else:
                done += 1
            continue
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
            print(f'{p["id"]:>6}  OK  {p["why"][:78]}')
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
