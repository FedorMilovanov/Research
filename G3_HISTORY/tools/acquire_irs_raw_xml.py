#!/usr/bin/env python3
"""Acquire exact G3 IRS Form 990 e-file XML objects with custody metadata.

Research-only acquisition helper. It validates each known object ID against the
official IRS annual index before attempting the IRS public S3 XML object route.
Downloaded bytes are written only to the requested output directory and are
intended for an ephemeral GitHub Actions artifact unless separately promoted by
repository custody policy.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterable

EIN = "842403597"

TARGETS = [
    {
        "label": "FY2023",
        "index_year": 2024,
        "object_id": "202411429349300611",
        "required_components": ["IRS990", "IRS990ScheduleO"],
        "research_use": "Part IX functional expenses and Schedule O continuations",
    },
    {
        "label": "FY2024",
        "index_year": 2025,
        "object_id": "202541359349304489",
        "required_components": ["IRS990", "IRS990ScheduleL", "IRS990ScheduleO"],
        "research_use": "Schedule L interested-person transaction rows and filing context",
    },
    {
        "label": "FY2025",
        "index_year": 2026,
        "object_id": "202641339349303874",
        "required_components": ["IRS990", "IRS990ScheduleL", "IRS990ScheduleO"],
        "research_use": "Schedule L interested-person transaction rows and filing context",
    },
]

USER_AGENT = (
    "FedorMilovanov-Research-G3-IRS-Acquisition/1.0 "
    "(research-only; contact via repository FedorMilovanov/Research)"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def fetch(url: str, timeout: int = 120) -> tuple[bytes, dict[str, Any]]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
        },
    )
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = response.read()
            meta = {
                "requested_url": url,
                "final_url": response.geturl(),
                "status": getattr(response, "status", None),
                "content_type": response.headers.get("Content-Type"),
                "content_length_header": response.headers.get("Content-Length"),
                "bytes": len(body),
                "sha256": sha256_bytes(body),
                "elapsed_seconds": round(time.time() - started, 3),
            }
            return body, meta
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} for {url}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"URL error for {url}: {exc.reason}") from exc


def normalize_key(key: str) -> str:
    return "".join(ch for ch in key.upper() if ch.isalnum())


def locate_index_row(csv_bytes: bytes, object_id: str) -> dict[str, str]:
    text = csv_bytes.decode("utf-8-sig", errors="strict")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise RuntimeError("IRS index CSV has no header")

    normalized = {normalize_key(name): name for name in reader.fieldnames}
    object_col = None
    for candidate in ("OBJECTID", "OBJECT_ID", "RETURNID", "RETURN_ID"):
        key = normalize_key(candidate)
        if key in normalized:
            object_col = normalized[key]
            break
    if object_col is None:
        raise RuntimeError(f"Could not identify object-id column in IRS index: {reader.fieldnames}")

    ein_col = None
    for candidate in ("EIN", "TAXPAYEREIN"):
        key = normalize_key(candidate)
        if key in normalized:
            ein_col = normalized[key]
            break

    for row in reader:
        value = (row.get(object_col) or "").strip()
        if value == object_id:
            clean = {str(k): (v or "").strip() for k, v in row.items() if k is not None}
            if ein_col:
                row_ein = "".join(ch for ch in clean.get(ein_col, "") if ch.isdigit())
                if row_ein and row_ein != EIN:
                    raise RuntimeError(
                        f"Object {object_id} matched index but EIN {row_ein} != expected {EIN}"
                    )
            return clean
    raise RuntimeError(f"Object {object_id} not found in IRS index")


def iter_named(root: ET.Element, wanted: str) -> Iterable[ET.Element]:
    for elem in root.iter():
        if local_name(elem.tag) == wanted:
            yield elem


def flatten_leaves(elem: ET.Element) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def walk(node: ET.Element, path: list[str]) -> None:
        lname = local_name(node.tag)
        next_path = path + [lname]
        children = list(node)
        text = (node.text or "").strip()
        attrs = {local_name(k): v for k, v in node.attrib.items()}
        if not children:
            if text or attrs:
                rows.append(
                    {
                        "path": "/".join(next_path),
                        "tag": lname,
                        "text": text,
                        "attributes": attrs,
                    }
                )
            return
        if text:
            rows.append(
                {
                    "path": "/".join(next_path),
                    "tag": lname,
                    "text": text,
                    "attributes": attrs,
                    "container_text": True,
                }
            )
        for child in children:
            walk(child, next_path)

    walk(elem, [])
    return rows


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def acquire_target(target: dict[str, Any], out_root: Path) -> dict[str, Any]:
    label = target["label"]
    object_id = target["object_id"]
    year = target["index_year"]
    target_dir = out_root / label
    target_dir.mkdir(parents=True, exist_ok=True)

    index_url = f"https://apps.irs.gov/pub/epostcard/990/xml/{year}/index_{year}.csv"
    index_bytes, index_meta = fetch(index_url)
    (target_dir / f"index_{year}.csv").write_bytes(index_bytes)
    row = locate_index_row(index_bytes, object_id)
    write_json(target_dir / "IRS_INDEX_ROW.json", row)
    write_json(target_dir / "IRS_INDEX_FETCH.json", index_meta)

    xml_candidates = [
        f"https://s3.amazonaws.com/irs-form-990/{object_id}_public.xml",
        f"https://s3.amazonaws.com/irs-form-990/{object_id}.xml",
    ]
    xml_bytes: bytes | None = None
    xml_meta: dict[str, Any] | None = None
    attempts: list[dict[str, Any]] = []
    for url in xml_candidates:
        try:
            body, meta = fetch(url)
            attempts.append({"url": url, "success": True, **meta})
            xml_bytes = body
            xml_meta = meta
            break
        except Exception as exc:  # record every deterministic acquisition attempt
            attempts.append({"url": url, "success": False, "error": str(exc)})

    write_json(target_dir / "XML_FETCH_ATTEMPTS.json", attempts)
    if xml_bytes is None or xml_meta is None:
        raise RuntimeError(f"Could not acquire XML for {label} object {object_id}")

    xml_path = target_dir / f"{object_id}_public.xml"
    xml_path.write_bytes(xml_bytes)
    write_json(target_dir / "XML_FETCH.json", xml_meta)

    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as exc:
        raise RuntimeError(f"Downloaded object {object_id} is not parseable XML: {exc}") from exc

    component_summary: dict[str, Any] = {}
    for component in target["required_components"]:
        matches = list(iter_named(root, component))
        component_summary[component] = {"count": len(matches)}
        if not matches:
            continue
        for idx, match in enumerate(matches, start=1):
            suffix = "" if len(matches) == 1 else f"_{idx:02d}"
            fragment = ET.tostring(match, encoding="utf-8", xml_declaration=True)
            fragment_path = target_dir / f"{component}{suffix}.xml"
            fragment_path.write_bytes(fragment)
            leaves = flatten_leaves(match)
            write_json(target_dir / f"{component}{suffix}_LEAVES.json", leaves)
            component_summary[component].setdefault("objects", []).append(
                {
                    "file": fragment_path.name,
                    "bytes": len(fragment),
                    "sha256": sha256_bytes(fragment),
                    "leaf_count": len(leaves),
                }
            )

    all_top_level = []
    for elem in root.iter():
        lname = local_name(elem.tag)
        if lname.startswith("IRS") and lname not in all_top_level:
            all_top_level.append(lname)
    write_json(target_dir / "COMPONENT_SUMMARY.json", component_summary)
    write_json(target_dir / "IRS_TAG_INVENTORY.json", all_top_level)

    custody = {
        "label": label,
        "ein": EIN,
        "object_id": object_id,
        "index_year": year,
        "research_use": target["research_use"],
        "index": index_meta,
        "index_row": row,
        "xml": {
            **xml_meta,
            "file": xml_path.name,
        },
        "components": component_summary,
        "state": "EPHEMERAL_ACTION_ARTIFACT",
        "publication_eligible": False,
        "raw_xml": True,
    }
    write_json(target_dir / "CUSTODY.json", custody)
    return custody


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="g3-irs-acquisition-output")
    args = parser.parse_args()

    out_root = Path(args.output)
    out_root.mkdir(parents=True, exist_ok=True)

    run_summary: dict[str, Any] = {
        "ein": EIN,
        "targets": [],
        "errors": [],
        "state": "EPHEMERAL_ACTION_ARTIFACT",
        "publication_eligible": False,
    }

    for target in TARGETS:
        try:
            run_summary["targets"].append(acquire_target(target, out_root))
        except Exception as exc:
            run_summary["errors"].append(
                {
                    "label": target["label"],
                    "object_id": target["object_id"],
                    "error": str(exc),
                }
            )

    write_json(out_root / "SUMMARY.json", run_summary)
    if run_summary["errors"]:
        for error in run_summary["errors"]:
            print(f"ERROR {error['label']} {error['object_id']}: {error['error']}", file=sys.stderr)
        return 2

    for target in run_summary["targets"]:
        print(
            f"ACQUIRED {target['label']} {target['object_id']} "
            f"{target['xml']['bytes']} bytes sha256={target['xml']['sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
