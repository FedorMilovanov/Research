#!/usr/bin/env python3
"""Acquire exact G3 IRS Form 990 e-file XML objects with custody metadata.

Research-only acquisition helper. It validates each known object ID against the
official IRS annual index, reads the authoritative XML_BATCH_ID from that row,
downloads the corresponding official IRS TEOS batch ZIP, and extracts only the
exact return XML member. Large annual indexes and batch ZIPs are not retained in
the final Actions artifact; their hashes, sizes, URLs, and matched rows are.

Downloaded evidence remains an EPHEMERAL_ACTION_ARTIFACT unless separately
promoted under the repository custody policy.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
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
    "FedorMilovanov-Research-G3-IRS-Acquisition/1.1 "
    "(research-only; contact via repository FedorMilovanov/Research)"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def request(url: str) -> urllib.request.Request:
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
        },
    )


def fetch(url: str, timeout: int = 180) -> tuple[bytes, dict[str, Any]]:
    started = time.time()
    try:
        with urllib.request.urlopen(request(url), timeout=timeout) as response:
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


def fetch_to_path(url: str, path: Path, timeout: int = 300) -> dict[str, Any]:
    started = time.time()
    digest = hashlib.sha256()
    total = 0
    try:
        with urllib.request.urlopen(request(url), timeout=timeout) as response, path.open("wb") as out:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
                digest.update(chunk)
                total += len(chunk)
            return {
                "requested_url": url,
                "final_url": response.geturl(),
                "status": getattr(response, "status", None),
                "content_type": response.headers.get("Content-Type"),
                "content_length_header": response.headers.get("Content-Length"),
                "bytes": total,
                "sha256": digest.hexdigest(),
                "elapsed_seconds": round(time.time() - started, 3),
            }
    except urllib.error.HTTPError as exc:
        path.unlink(missing_ok=True)
        raise RuntimeError(f"HTTP {exc.code} for {url}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        path.unlink(missing_ok=True)
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


def batch_id_from_row(row: dict[str, str]) -> str:
    for key, value in row.items():
        if normalize_key(key) == "XMLBATCHID" and value.strip():
            return value.strip()
    raise RuntimeError("Matched IRS index row has no XML_BATCH_ID")


def batch_url_candidates(year: int, batch_id: str) -> list[str]:
    base = f"https://apps.irs.gov/pub/epostcard/990/xml/{year}/"
    names: list[str] = []
    for candidate in (batch_id, batch_id.upper(), batch_id[:-1] + batch_id[-1:].upper()):
        if candidate and candidate not in names:
            names.append(candidate)
    return [base + name + ".zip" for name in names]


def acquire_batch(year: int, batch_id: str, archive_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []
    for url in batch_url_candidates(year, batch_id):
        try:
            meta = fetch_to_path(url, archive_path)
            attempts.append({"url": url, "success": True, **meta})
            return meta, attempts
        except Exception as exc:
            attempts.append({"url": url, "success": False, "error": str(exc)})
    raise RuntimeError(f"Could not acquire IRS batch ZIP {batch_id}; attempts={attempts}")


def extract_exact_xml(archive_path: Path, object_id: str) -> tuple[bytes, dict[str, Any]]:
    try:
        with zipfile.ZipFile(archive_path) as archive:
            candidates = [name for name in archive.namelist() if object_id in Path(name).name]
            if not candidates:
                raise RuntimeError(f"Object {object_id} not present in IRS batch ZIP")
            preferred = [name for name in candidates if Path(name).name == f"{object_id}_public.xml"]
            member = preferred[0] if preferred else sorted(candidates)[0]
            xml_bytes = archive.read(member)
            info = archive.getinfo(member)
            return xml_bytes, {
                "member": member,
                "member_compressed_bytes": info.compress_size,
                "member_uncompressed_bytes": info.file_size,
                "member_crc32": f"{info.CRC:08x}",
                "member_sha256": sha256_bytes(xml_bytes),
                "matching_members": candidates,
            }
    except zipfile.BadZipFile as exc:
        raise RuntimeError(f"IRS batch download is not a valid ZIP: {exc}") from exc


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
    row = locate_index_row(index_bytes, object_id)
    batch_id = batch_id_from_row(row)
    write_json(target_dir / "IRS_INDEX_ROW.json", row)
    write_json(target_dir / "IRS_INDEX_FETCH.json", index_meta)

    # Do not retain the very large annual index in the uploaded Actions artifact.
    # Its exact URL, size, hash and matched row are enough to reproduce validation.
    archive_path = target_dir / f"{batch_id}.zip"
    batch_attempts: list[dict[str, Any]] = []
    try:
        batch_meta, batch_attempts = acquire_batch(year, batch_id, archive_path)
        write_json(target_dir / "BATCH_FETCH_ATTEMPTS.json", batch_attempts)
        write_json(target_dir / "BATCH_FETCH.json", batch_meta)
        xml_bytes, member_meta = extract_exact_xml(archive_path, object_id)
        write_json(target_dir / "BATCH_MEMBER.json", member_meta)
    finally:
        # Batch archives can be hundreds of MB. Preserve provenance/checksum, not
        # the whole container ZIP, in the ephemeral evidence package.
        archive_path.unlink(missing_ok=True)
        if batch_attempts and not (target_dir / "BATCH_FETCH_ATTEMPTS.json").exists():
            write_json(target_dir / "BATCH_FETCH_ATTEMPTS.json", batch_attempts)

    xml_path = target_dir / f"{object_id}_public.xml"
    xml_path.write_bytes(xml_bytes)
    xml_meta = {
        "file": xml_path.name,
        "bytes": len(xml_bytes),
        "sha256": sha256_bytes(xml_bytes),
        "source_batch_id": batch_id,
        "source_member": member_meta["member"],
    }
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

    all_irs_tags: list[str] = []
    for elem in root.iter():
        lname = local_name(elem.tag)
        if lname.startswith("IRS") and lname not in all_irs_tags:
            all_irs_tags.append(lname)
    write_json(target_dir / "COMPONENT_SUMMARY.json", component_summary)
    write_json(target_dir / "IRS_TAG_INVENTORY.json", all_irs_tags)

    custody = {
        "label": label,
        "ein": EIN,
        "object_id": object_id,
        "index_year": year,
        "research_use": target["research_use"],
        "index": index_meta,
        "index_row": row,
        "batch": {
            **batch_meta,
            "xml_batch_id": batch_id,
            "archive_retained": False,
        },
        "batch_member": member_meta,
        "xml": xml_meta,
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
            f"{target['xml']['bytes']} bytes sha256={target['xml']['sha256']} "
            f"batch={target['batch']['xml_batch_id']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
