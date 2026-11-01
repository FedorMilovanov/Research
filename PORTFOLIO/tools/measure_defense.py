#!/usr/bin/env python3
"""Измеритель защитных свойств GitHub Actions по локальным клонам.

Зачем отдельный скрипт: числа вида «658/658 действий прибиты к SHA» стареют
молча. Здесь каждое число имеет определение в коде, поэтому его можно
пересчитать и увидеть, что именно считается.

    python3 measure_defense.py /tmp/sp          # каталог с клонами репозиториев
    python3 measure_defense.py /tmp/sp --json   # машиночитаемый вывод

Определения (важно, потому что от них зависят цифры в портфолио):

* workflow            — файл `.github/workflows/*.yml` или `*.yaml`;
* внешнее действие    — `uses:` вида `owner/repo[/path]@ref`; локальные `./…`
                        и `docker://…` считаются отдельно и в «пины» не входят;
* пин                 — ref целиком из 40 hex-символов;
* permissions         — ключ `permissions:` верхнего уровня в файле, а не в job;
* write-all           — значение `permissions: write-all` (или `permissions: {…: write-all}`),
                        а не слово в комментарии;
* триггер             — вхождение в блоке `on:` (`pull_request_target`, `workflow_run`);
* concurrency         — ключ `concurrency:` верхнего уровня;
* latest-раннер       — `ubuntu-latest` / `windows-latest` / `macos-latest` в `runs-on:`;
* secret scanning     — наличие `gitleaks` в тексте workflow (то есть шаг запущен,
                        а не упомянут в комментарии — это ограничение метода).

Скрипт намеренно не использует PyYAML: разбор по тексту достаточно точен для
перечисленных выше свойств и не требует установки зависимостей.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

USES = re.compile(r"^\s*(?:-\s*)?uses:\s*(?P<target>[^\s#]+)", re.MULTILINE)
EXTERNAL = re.compile(r"^(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+)")
FULL_SHA = re.compile(r"[0-9a-f]{40}$")
TOP_PERMISSIONS = re.compile(r"^permissions:\s*(?P<value>[^\n#]*)", re.MULTILINE)
TOP_CONCURRENCY = re.compile(r"^concurrency:", re.MULTILINE)
PULL_REQUEST_TARGET = re.compile(r"^\s*pull_request_target:\s*$", re.MULTILINE)
WORKFLOW_RUN = re.compile(r"^\s*workflow_run:\s*$", re.MULTILINE)
PERSIST_FALSE = re.compile(r"persist-credentials:\s*false")
TIMEOUT = re.compile(r"^\s+timeout-minutes:", re.MULTILINE)
LATEST_RUNNER = re.compile(r"(?:ubuntu|windows|macos)-latest")


def workflow_files(root: Path) -> list[Path]:
    directory = root / ".github" / "workflows"
    if not directory.is_dir():
        return []
    return sorted([*directory.glob("*.yml"), *directory.glob("*.yaml")])


def measure_repository(root: Path) -> dict[str, object]:
    files = workflow_files(root)
    stats: dict[str, object] = {
        "repository": root.name,
        "workflows": len(files),
        "external_uses": 0,
        "pinned_uses": 0,
        "unpinned_uses": [],
        "local_uses": 0,
        "docker_uses": 0,
        "workflows_with_permissions": 0,
        "permissions_write_all": 0,
        "pull_request_target": 0,
        "workflow_run": 0,
        "concurrency": 0,
        "persist_credentials_false": 0,
        "job_timeouts": 0,
        "workflows_with_latest_runner": 0,
        "gitleaks_workflows": [],
    }
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in USES.finditer(text):
            target = match.group("target")
            if target.startswith("./") or target.startswith("../"):
                stats["local_uses"] += 1
                continue
            if target.startswith("docker://"):
                stats["docker_uses"] += 1
                continue
            if not EXTERNAL.match(target.split("@", 1)[0]):
                continue
            stats["external_uses"] += 1
            ref = target.rsplit("@", 1)[-1]
            if FULL_SHA.fullmatch(ref):
                stats["pinned_uses"] += 1
            else:
                stats["unpinned_uses"].append(f"{path.name}:{target}")

        top = TOP_PERMISSIONS.search(text)
        if top:
            stats["workflows_with_permissions"] += 1
            if "write-all" in top.group("value"):
                stats["permissions_write_all"] += 1
        if TOP_CONCURRENCY.search(text):
            stats["concurrency"] += 1
        stats["pull_request_target"] += len(PULL_REQUEST_TARGET.findall(text))
        stats["workflow_run"] += len(WORKFLOW_RUN.findall(text))
        stats["persist_credentials_false"] += len(PERSIST_FALSE.findall(text))
        stats["job_timeouts"] += len(TIMEOUT.findall(text))
        if LATEST_RUNNER.search(text):
            stats["workflows_with_latest_runner"] += 1
        if "gitleaks" in text:
            stats["gitleaks_workflows"].append(path.name)
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repos_dir", nargs="?", default=".", help="каталог с клонами репозиториев")
    parser.add_argument("--json", action="store_true", help="вывести JSON вместо таблицы")
    args = parser.parse_args()

    base = Path(args.repos_dir).resolve()
    roots = [path for path in sorted(base.iterdir()) if path.is_dir() and (path / ".github").is_dir()]
    if not roots:
        parser.error(f"в {base} нет каталогов с .github — укажите каталог клонов")

    rows = [measure_repository(root) for root in roots]
    totals = {
        key: sum(int(row[key]) for row in rows)  # type: ignore[arg-type]
        for key in (
            "workflows",
            "external_uses",
            "pinned_uses",
            "local_uses",
            "docker_uses",
            "workflows_with_permissions",
            "permissions_write_all",
            "pull_request_target",
            "workflow_run",
            "concurrency",
            "persist_credentials_false",
            "job_timeouts",
            "workflows_with_latest_runner",
        )
    }
    totals["repositories"] = len(rows)
    totals["gitleaks_repositories"] = sum(1 for row in rows if row["gitleaks_workflows"])

    if args.json:
        print(json.dumps({"totals": totals, "repositories": rows}, ensure_ascii=False, indent=2))
        return 0

    print(f"репозиториев: {totals['repositories']}   workflow: {totals['workflows']}")
    print(f"внешних действий: {totals['external_uses']}   на 40-hex SHA: {totals['pinned_uses']}")
    print(f"локальных действий: {totals['local_uses']}   docker: {totals['docker_uses']}")
    print(f"workflow с permissions: {totals['workflows_with_permissions']}   permissions: write-all: {totals['permissions_write_all']}")
    print(f"pull_request_target: {totals['pull_request_target']}   workflow_run: {totals['workflow_run']}   concurrency: {totals['concurrency']}")
    print(f"persist-credentials: false: {totals['persist_credentials_false']}   job timeout-minutes: {totals['job_timeouts']}")
    print(f"workflow с -latest раннером: {totals['workflows_with_latest_runner']}")
    print(f"secret scanning (gitleaks): {totals['gitleaks_repositories']} из {totals['repositories']}")
    print()
    print(f"{'repository':26s} {'wf':>3s} {'uses':>4s} {'sha':>4s} {'perm':>4s} {'gitleaks':>8s}")
    for row in rows:
        print(
            f"{row['repository']:26s} {row['workflows']:3d} {row['external_uses']:4d} "
            f"{row['pinned_uses']:4d} {row['workflows_with_permissions']:4d} "
            f"{'да' if row['gitleaks_workflows'] else '—':>8s}"
        )
    unpinned = [item for row in rows for item in row["unpinned_uses"]]  # type: ignore[index]
    if unpinned:
        print("\nнеприбитые внешние действия:")
        for item in unpinned:
            print("  " + item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
