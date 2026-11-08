#!/usr/bin/env python3
"""Read-only, fail-closed validation of the Names of God long-running workplan.

Validates task lifecycle, dependency graph, source provenance metadata,
navigation and snapshot consistency. Does NOT browse the web, listen to
lectures, collate manuscripts, verify external licensing or approve Product.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
PLAN = DATA / "names_research_workplan_v1.json"
BASELINE = DATA / "names_ledger_v1.json"
EXTENSION = DATA / "names_extension_ledger_v1.json"
SOURCES = DATA / "source_access_register_v1.json"
NAV = ROOT / "00_README_AND_NAVIGATION.md"
GUIDE = ROOT / "11_MASTER_RESEARCH_WORKPLAN_AND_ACCEPTANCE.md"
MEDIA = ROOT / "12_TMS_BARRICK_CHOU_SOURCE_REVIEW.md"
CORPUS_TESTS = ROOT / "test_validate_names_ledger.py"

ALLOWED_STATUSES = {
    "DONE", "IN_PROGRESS", "OPEN", "BLOCKED_SOURCE",
    "BLOCKED_ACCESS", "BLOCKED_ARTIFACT", "BLOCKED_DEPENDENCY",
}
EXPECTED_MEDIA_CATEGORIES = {"MEDIA-TMS-JZ-01", "MEDIA-CHOU-JZ-02",
                             "MEDIA-BARRICK-03", "MEDIA-BARRICK-04",
                             "MEDIA-BARRICK-05", "MEDIA-CHOU-06",
                             "MEDIA-LSB-07", "MEDIA-CHOU-TMS-08"}
EXPECTED_PRIMARY_TASKS = {f"NG-{n:02d}" for n in range(16)}
REQUIRED_EXPLANATIONS = (
    "NG-00", "NG-01", "NG-02", "NG-05", "NG-06", "NG-07",
    "NG-08", "NG-09", "NG-13", "NG-14", "NG-15",
)


def _count_attestations(data: dict) -> int:
    return sum(len(x.get("attestations", [])) for x in data.get("records", [])
               if isinstance(x, dict) and isinstance(x.get("attestations"), list))


def validate_names_workplan(
    plan: dict,
    *,
    baseline: dict,
    extension: dict,
    sources: dict,
    corpus_tests: str,
    navigation: str,
    guide: str,
    media_document: str,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(plan, dict):
        return ["workplan: plan is not an object"]
    if plan.get("schemaVersion") != 1 or plan.get("planId") != "NAMES_OF_GOD_MASTER_WORKPLAN":
        errors.append("workplan: schema/version/id drifted")
    if plan.get("statusOwner") != "ИМЕНА БОГА/data/names_research_workplan_v1.json":
        errors.append("workplan: sole machine status authority changed")
    if plan.get("humanGuide") != "ИМЕНА БОГА/11_MASTER_RESEARCH_WORKPLAN_AND_ACCEPTANCE.md":
        errors.append("workplan: human guide path changed")
    if plan.get("mediaResearch") != "ИМЕНА БОГА/12_TMS_BARRICK_CHOU_SOURCE_REVIEW.md":
        errors.append("workplan: lecture audit path changed")
    if set(plan.get("allowedStatuses", [])) != ALLOWED_STATUSES:
        errors.append("workplan: lifecycle state enum changed")
    if "no site or main mutations" not in str(plan.get("scope", "")):
        errors.append("workplan: research-only production boundary weakened")
    if not isinstance(plan.get("futureUpdateProtocol"), str) or "read this JSON first" not in plan["futureUpdateProtocol"]:
        errors.append("workplan: continual next-session update procedure lost")

    tasks = plan.get("tasks", [])
    if not isinstance(tasks, list):
        return errors + ["workplan: no task list"]
    ids: set[str] = set()
    task_map: dict[str, dict] = {}
    for task in tasks:
        if not isinstance(task, dict):
            errors.append("workplan: task is not an object")
            continue
        tid = task.get("id")
        if not isinstance(tid, str) or tid in ids or not re.fullmatch(r"NG-\d{2}", tid):
            errors.append(f"workplan: duplicate or malformed task ID {tid}")
            continue
        ids.add(tid)
        task_map[tid] = task
        if task.get("priority") not in ("P0", "P1", "P2"):
            errors.append(f"workplan: unknown priority {tid}")
        if task.get("status") not in ALLOWED_STATUSES:
            errors.append(f"workplan: status missing/invalid for {tid}")
        if not isinstance(task.get("title"), str) or len(task["title"]) < 10:
            errors.append(f"workplan: missing meaningful title {tid}")
        if not isinstance(task.get("acceptance"), list) or not task["acceptance"]:
            errors.append(f"workplan: measurable acceptance missing {tid}")
        if not isinstance(task.get("evidence"), list) or not task["evidence"]:
            errors.append(f"workplan: evidence anchors missing {tid}")
        if not isinstance(task.get("dependsOn"), list):
            errors.append(f"workplan: task dependencies malformed {tid}")
        if task.get("status") == "DONE":
            if (not task.get("closureAt") or
                task.get("verification") in (None, "NOT_APPLICABLE_UNTIL_DONE") or
                not task.get("evidence")):
                errors.append(f"workplan: {tid} DONE without witnessed closure evidence")
        elif task.get("closureAt") is not None:
            errors.append(f"workplan: {tid} has false closure timestamp")
    if ids != EXPECTED_PRIMARY_TASKS:
        errors.append("workplan: original sixteen stable NG task IDs missing or multiplied")
    graph: dict[str, list[str]] = {}
    for tid, task in task_map.items():
        deps = task.get("dependsOn", [])
        if not isinstance(deps, list):
            continue
        graph[tid] = deps
        if len(deps) != len(set(deps)):
            errors.append(f"workplan: repeated prerequisite for {tid}")
        for dep in deps:
            if dep not in ids:
                errors.append(f"workplan: {tid} has orphan dependency {dep}")
            if dep == tid:
                errors.append(f"workplan: {tid} depends upon itself")
    color: dict[str, int] = {}
    def dfs(node: str) -> None:
        if color.get(node) == 1:
            errors.append(f"workplan: dependency cycle at {node}")
            return
        if color.get(node) == 2:
            return
        color[node] = 1
        for dep in graph.get(node, []):
            if dep in graph:
                dfs(dep)
        color[node] = 2
    for tid in graph:
        dfs(tid)

    phases = plan.get("phases", [])
    if not isinstance(phases, list) or len(phases) != 5:
        errors.append("workplan: expected five ordered research phases")
    else:
        all_phase_tasks: list[str] = []
        for phase in phases:
            if not isinstance(phase, dict) or not isinstance(phase.get("tasks"), list):
                errors.append("workplan: invalid phase definition")
                continue
            if not phase.get("exit"):
                errors.append(f"workplan: missing phase exit for {phase.get('id')}")
            all_phase_tasks.extend(phase["tasks"])
        if set(all_phase_tasks) != ids or len(all_phase_tasks) != len(ids):
            errors.append("workplan: phase task coverage non-exhaustive or duplicate")

    media = plan.get("mediaQueue", [])
    if not isinstance(media, list):
        return errors + ["workplan: lecture queue missing"]
    media_ids: set[str] = set()
    for source in media:
        if not isinstance(source, dict):
            errors.append("workplan: invalid media entry")
            continue
        mid = source.get("id")
        if mid in media_ids or not isinstance(mid, str):
            errors.append(f"workplan: duplicate media ID {mid}")
        media_ids.add(mid)
        if not str(source.get("url", "")).startswith("https://"):
            errors.append(f"workplan: unsafe or missing source URL {mid}")
        if source.get("task") not in ids:
            errors.append(f"workplan: media {mid} points to non-existent task")
        if source.get("status") in ("WATCHED_WITH_AUDIO", "FULL_OBJECT_VERIFIED"):
            if source.get("verification") in (None, "PUBLISHER_COURSE_CATALOG_CHECKED_NOT_WATCHED",
                                               "TIMESTAMPED_THIRD_PARTY_TRANSCRIPT_SPOT_CHECKED_AUDIO_NOT_WATCHED"):
                errors.append(f"workplan: {mid} source falsely claimed fully watched")
        if not isinstance(source.get("verification"), str) or not source["verification"]:
            errors.append(f"workplan: {mid} has no honest source-verification boundary")
    if media_ids != EXPECTED_MEDIA_CATEGORIES:
        errors.append("workplan: TMS/Barrick/Chou core media queue lost provenance")

    recorded = plan.get("baseline", {})
    if not isinstance(recorded, dict):
        return errors + ["workplan: frozen snapshot missing"]
    checks = {
        "arenaRecords": len(baseline.get("records", [])),
        "extensionRecords": len(extension.get("records", [])),
        "contextAttestations": _count_attestations(baseline) + _count_attestations(extension),
        "sourceRegisterEntries": len(sources.get("records", [])),
        "regressionTests": len(re.findall(r"^    def test_", corpus_tests, re.MULTILINE)),
    }
    for k, current in checks.items():
        if recorded.get(k) != current:
            errors.append(f"workplan: baseline {k} snapshot drifted: saved={recorded.get(k)} current={current}")
    if (recorded.get("criticalCollationsCompleted") != 0 or
        recorded.get("productApprovals") != 0):
        errors.append("workplan: unearned critical collation or Product approval")
    if not all(r.get("publicationState") == "BLOCKED" for d in (baseline, extension, sources)
               for r in d.get("records", [])):
        errors.append("workplan: corpus unexpectedly published before editorial acceptance")
    if "11_MASTER_RESEARCH_WORKPLAN_AND_ACCEPTANCE.md" not in navigation or \
       "names_research_workplan_v1.json" not in navigation or \
       "12_TMS_BARRICK_CHOU_SOURCE_REVIEW.md" not in navigation:
        errors.append("workplan: master plan or media source omitted from research navigation")
    # The live navigation source count must match the machine source registry; old wave counts are historical.
    live_sources_anchor = f"[data/source_access_register_v1.json](data/source_access_register_v1.json) — **{len(sources.get('records', []))} источник"
    if live_sources_anchor not in navigation:
        errors.append("workplan: current source register count in navigation is stale")
    for key in REQUIRED_EXPLANATIONS:
        if key not in guide:
            errors.append(f"workplan: human-readable guide missing task {key}")
    for source_key in ("Joe Zhakevich", "Abner Chou", "William D. Barrick",
                       "foiequip.org/courses/gods-many-names",
                       "2hFKPHZL5qI", "0sjpFs3U6jI"):
        if source_key not in media_document:
            errors.append(f"workplan: expected lecture provenance missing {source_key}")
    return errors


def main() -> int:
    try:
        read = lambda p: p.read_text(encoding="utf-8")
        plan, baseline, extension, sources = [
            json.loads(read(p)) for p in (PLAN, BASELINE, EXTENSION, SOURCES)
        ]
        errors = validate_names_workplan(
            plan, baseline=baseline, extension=extension, sources=sources,
            corpus_tests=read(CORPUS_TESTS), navigation=read(NAV),
            guide=read(GUIDE), media_document=read(MEDIA),
        )
    except (OSError, ValueError, TypeError) as exc:
        print(f"FAIL: cannot load workplan and proof corpus: {exc}", file=sys.stderr)
        return 1
    if errors:
        for issue in errors:
            print("FAIL: " + issue, file=sys.stderr)
        return 1
    print(f"PASS: {len(plan['tasks'])} tasks, {len(plan['phases'])} phases, "
          f"{len(plan['mediaQueue'])} media records; exact corpus/source/test snapshot; "
          "no unearned closures or broken dependency graph")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
