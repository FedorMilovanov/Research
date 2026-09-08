#!/usr/bin/env python3
"""Print deterministic evidence summaries from acquired IRS XML artifacts.

This tool does not fetch data and does not modify repository files. It reads the
JSON leaf indexes emitted by acquire_irs_raw_xml_v4.py and prints a stable,
machine-readable summary into GitHub Actions logs so evidence can be audited
without downloading the artifact ZIP.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def emit(kind: str, payload: Any) -> None:
    print(json.dumps({"kind": kind, "payload": payload}, ensure_ascii=False, sort_keys=True))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="g3-irs-acquisition-output")
    ap.add_argument("--label", required=True)
    args = ap.parse_args()

    root = Path(args.output) / args.label
    custody_path = root / "CUSTODY.json"
    if not custody_path.exists():
        raise SystemExit(f"missing custody file: {custody_path}")

    custody = read_json(custody_path)
    print("G3_IRS_EVIDENCE_SUMMARY_BEGIN")
    emit("custody", {
        "label": custody.get("label"),
        "ein": custody.get("ein"),
        "object_id": custody.get("object_id"),
        "batch_id": custody.get("batch_id"),
        "source_member": custody.get("source_member"),
        "xml": custody.get("xml"),
        "components": custody.get("components"),
    })

    label = args.label.upper()
    if label in {"FY2024", "FY2025"}:
        schedule_l = root / "IRS990ScheduleL_LEAVES.json"
        schedule_o = root / "IRS990ScheduleO_LEAVES.json"
        if not schedule_l.exists():
            raise SystemExit(f"missing Schedule L leaves: {schedule_l}")
        leaves_l = read_json(schedule_l)
        emit("schedule_l_leaf_count", len(leaves_l))
        for idx, leaf in enumerate(leaves_l, 1):
            emit("schedule_l_leaf", {"ordinal": idx, **leaf})
        if schedule_o.exists():
            leaves_o = read_json(schedule_o)
            emit("schedule_o_leaf_count", len(leaves_o))
            for idx, leaf in enumerate(leaves_o, 1):
                emit("schedule_o_leaf", {"ordinal": idx, **leaf})

    elif label == "FY2022_LATER":
        form = root / "IRS990_LEAVES.json"
        if not form.exists():
            raise SystemExit(f"missing IRS990 leaves: {form}")
        leaves = read_json(form)
        emit("irs990_leaf_count", len(leaves))
        # Print every leaf. The raw acquisition artifact remains the authority;
        # full leaf output avoids a hidden parser judgment about which Part IX
        # fields are material and lets the audit reconstruct row deltas exactly.
        for idx, leaf in enumerate(leaves, 1):
            emit("irs990_leaf", {"ordinal": idx, **leaf})
    else:
        raise SystemExit(f"unsupported summary label: {args.label}")

    print("G3_IRS_EVIDENCE_SUMMARY_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
