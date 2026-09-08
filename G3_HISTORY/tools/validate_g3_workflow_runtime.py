#!/usr/bin/env python3
"""Validate runtime/action pinning and main-trigger coverage for G3 workflows."""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WF = REPO / ".github" / "workflows"
SETUP_PYTHON_V7 = "5fda3b95a4ea91299a34e894583c3862153e4b97"
UPLOAD_ARTIFACT_V7 = "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a"

ACQUISITION_WORKFLOWS = [
    "g3-archive-content-inventory-acquisition.yml",
    "g3-buck-media-windows.yml",
    "g3-buck-rss-media-inventory.yml",
    "g3-buck-titus-media-acquisition.yml",
    "g3-content-inventory-acquisition.yml",
    "g3-douglas-property-acquisition.yml",
    "g3-georgia-entity-acquisition.yml",
    "g3-irs-raw-acquisition.yml",
    "g3-wayback-2025-board-transition.yml",
    "g3-wayback-late-board-acquisition.yml",
]
PYTHON_WORKFLOWS = ACQUISITION_WORKFLOWS + ["g3-corpus-integrity.yml"]


def main() -> int:
    errors: list[str] = []

    for name in ACQUISITION_WORKFLOWS:
        path = WF / name
        if not path.is_file():
            errors.append(f"missing acquisition workflow: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        if "workflow_dispatch:" not in text:
            errors.append(f"{name}: missing workflow_dispatch")
        if "pull_request:" not in text:
            errors.append(f"{name}: missing pull_request")
        if "push:" not in text or "branches: [main]" not in text:
            errors.append(f"{name}: missing path-scoped push main coverage")
        if "cancel-in-progress: true" not in text:
            errors.append(f"{name}: missing cancel-in-progress")
        if "research/g3-history-20260907" in text:
            errors.append(f"{name}: references retired G3 branch")

        upload_refs = re.findall(r"actions/upload-artifact@([^\s#]+)", text)
        if upload_refs != [UPLOAD_ARTIFACT_V7]:
            errors.append(
                f"{name}: upload-artifact refs {upload_refs!r}, expected only {UPLOAD_ARTIFACT_V7}"
            )

    for name in PYTHON_WORKFLOWS:
        path = WF / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        refs = re.findall(r"actions/setup-python@([^\s#]+)", text)
        if refs != [SETUP_PYTHON_V7]:
            errors.append(f"{name}: setup-python refs {refs!r}, expected only {SETUP_PYTHON_V7}")
        if "python-version: '3.12.8'" not in text:
            errors.append(f"{name}: Python runtime is not pinned to 3.12.8")

    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        print(f"G3_WORKFLOW_RUNTIME=FAIL errors={len(errors)}", file=sys.stderr)
        return 2

    print(
        "G3_WORKFLOW_RUNTIME=PASS "
        f"acquisition_workflows={len(ACQUISITION_WORKFLOWS)} "
        f"python_workflows={len(PYTHON_WORKFLOWS)} "
        f"setup_python={SETUP_PYTHON_V7} "
        f"upload_artifact={UPLOAD_ARTIFACT_V7}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
