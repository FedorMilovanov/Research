#!/usr/bin/env python3
"""Print deterministic evidence summaries from acquired IRS XML artifacts.

This tool does not fetch data and does not modify repository files. It reads the
raw return and JSON leaf indexes emitted by acquire_irs_raw_xml_v4.py and prints
stable, machine-readable summaries into GitHub Actions logs so evidence can be
audited without downloading artifact ZIPs.
"""
from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def emit(kind: str, payload: Any) -> None:
    print(json.dumps({"kind": kind, "payload": payload}, ensure_ascii=False, sort_keys=True))


def lname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def flatten(elem: ET.Element) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    def walk(node: ET.Element, path: list[str]) -> None:
        name = lname(node.tag)
        current = path + [name]
        children = list(node)
        text = (node.text or "").strip()
        attrs = {lname(k): v for k, v in node.attrib.items()}
        if not children:
            if text or attrs:
                out.append({"path": "/".join(current), "tag": name, "text": text, "attributes": attrs})
            return
        if text:
            out.append({"path": "/".join(current), "tag": name, "text": text, "attributes": attrs, "container_text": True})
        for child in children:
            walk(child, current)

    walk(elem, [])
    return out


def raw_components(root: Path, custody: dict[str, Any], component_names: set[str]) -> dict[str, list[dict[str, Any]]]:
    xml_meta = custody.get("xml") or {}
    raw_name = xml_meta.get("file")
    if not raw_name:
        raise SystemExit("custody XML filename missing")
    raw_path = root / raw_name
    if not raw_path.exists():
        raise SystemExit(f"raw XML missing: {raw_path}")
    xml_root = ET.parse(raw_path).getroot()
    found: dict[str, list[dict[str, Any]]] = {name: [] for name in component_names}
    for elem in xml_root.iter():
        name = lname(elem.tag)
        if name in component_names:
            found[name].append({"object_ordinal": len(found[name]) + 1, "leaves": flatten(elem)})
    return found


def emit_component_objects(kind_prefix: str, objects: list[dict[str, Any]]) -> None:
    emit(f"{kind_prefix}_object_count", len(objects))
    for obj in objects:
        leaves = obj["leaves"]
        emit(f"{kind_prefix}_object", {"object_ordinal": obj["object_ordinal"], "leaf_count": len(leaves)})
        for idx, leaf in enumerate(leaves, 1):
            emit(f"{kind_prefix}_leaf", {"object_ordinal": obj["object_ordinal"], "ordinal": idx, **leaf})


def relevant_asset_leaf(leaf: dict[str, Any]) -> bool:
    """Select balance-sheet / asset-sale leaves without schema guessing."""
    hay = (leaf.get("path", "") + " " + leaf.get("tag", "")).casefold()
    terms = (
        "sale", "asset", "gain", "loss", "receiv", "note", "loan",
        "land", "building", "equipment", "depreci", "property", "mortgage",
        "cash", "saving", "investment",
    )
    return any(term in hay for term in terms)


def emit_asset_trace(label: str, leaves: list[dict[str, Any]]) -> None:
    selected = [leaf for leaf in leaves if relevant_asset_leaf(leaf)]
    prefix = label.casefold()
    emit(f"{prefix}_asset_leaf_count", len(selected))
    for idx, leaf in enumerate(selected, 1):
        emit(f"{prefix}_asset_leaf", {"ordinal": idx, **leaf})


def relevant_program_service_leaf(leaf: dict[str, Any]) -> bool:
    """Select Part III mission/program-service narrative fields conservatively."""
    hay = (leaf.get("path", "") + " " + leaf.get("tag", "")).casefold()
    terms = (
        "programserviceaccomplishment",
        "programserviceaccom",
        "programsrvcaccom",
        "missiondesc",
        "activityormission",
        "significantnewprogram",
        "significantchange",
    )
    return any(term in hay for term in terms)


def emit_program_service_trace(label: str, leaves: list[dict[str, Any]]) -> None:
    selected = [leaf for leaf in leaves if relevant_program_service_leaf(leaf)]
    prefix = label.casefold()
    emit(f"{prefix}_program_service_leaf_count", len(selected))
    for idx, leaf in enumerate(selected, 1):
        emit(f"{prefix}_program_service_leaf", {"ordinal": idx, **leaf})


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
        form = root / "IRS990_LEAVES.json"
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
        if form.exists():
            leaves = read_json(form)
            context = [
                leaf for leaf in leaves
                if "Form990PartVIISectionAGrp" in leaf.get("path", "")
                or leaf.get("tag") in {
                    "VotingMembersGoverningBodyCnt", "VotingMembersIndependentCnt",
                    "GoverningBodyVotingMembersCnt", "IndependentVotingMemberCnt",
                    "ConflictOfInterestPolicyInd", "AnnualDisclosureCoveredPrsnInd",
                    "RegularMonitoringEnfrcInd", "FamilyOrBusinessRlnInd",
                    "BusinessRlnWithOrgMemInd", "BusinessRlnWithFamMemInd",
                    "BusinessRlnWith35CtrlEntInd", "EngagedInExcessBenefitTransInd",
                    "CompensationProcessCEOInd", "CompensationProcessOtherInd",
                }
            ]
            emit("governance_context_leaf_count", len(context))
            for idx, leaf in enumerate(context, 1):
                emit("governance_context_leaf", {"ordinal": idx, **leaf})
            emit_asset_trace(label, leaves)
            if label == "FY2025":
                emit_program_service_trace(label, leaves)

    elif label == "FY2022_LATER":
        form = root / "IRS990_LEAVES.json"
        if not form.exists():
            raise SystemExit(f"missing IRS990 leaves: {form}")
        leaves = read_json(form)
        emit("irs990_leaf_count", len(leaves))
        for idx, leaf in enumerate(leaves, 1):
            emit("irs990_leaf", {"ordinal": idx, **leaf})
        components = raw_components(root, custody, {"IRS990ScheduleD", "IRS990ScheduleM", "IRS990ScheduleO"})
        emit_component_objects("schedule_d", components["IRS990ScheduleD"])
        emit_component_objects("schedule_m", components["IRS990ScheduleM"])
        emit_component_objects("schedule_o", components["IRS990ScheduleO"])

    elif label == "FY2023":
        form = root / "IRS990_LEAVES.json"
        if not form.exists():
            raise SystemExit(f"missing IRS990 leaves: {form}")
        leaves = read_json(form)
        emit_asset_trace(label, leaves)
        components = raw_components(root, custody, {"IRS990ScheduleD", "IRS990ScheduleO"})
        emit_component_objects("schedule_d", components["IRS990ScheduleD"])
        emit_component_objects("schedule_o", components["IRS990ScheduleO"])
    else:
        raise SystemExit(f"unsupported summary label: {args.label}")

    print("G3_IRS_EVIDENCE_SUMMARY_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
