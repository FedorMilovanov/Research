#!/usr/bin/env python3
"""Fast fail-closed G3 IRS TEOS raw XML acquisition.

Why v4 exists
-------------
IRS May 2025/2026 TEOS archives use Deflate64. Python 3.12 can list those ZIPs
but cannot decode members. v3 correctly fell back to external readers, but its
content-signature search spawned an external extractor once per XML member
(~80k processes for 2025_TEOS_XML_05A) and hit the 30-minute Actions timeout.

v4 extracts each candidate batch exactly once with the system `unzip`, then
scans extracted XML files locally for the exact EIN, tax period and independent
financial fingerprints. For split months it can fail over A -> B. Batch ZIPs and
temporary extracted directories are deleted before artifact upload; only the
matched raw return, selected component fragments and custody metadata remain.

The lane is read-only with respect to the repository and publication remains
fail-closed.
"""
from __future__ import annotations

import argparse, csv, hashlib, io, json, shutil, subprocess, sys, tempfile, time
import urllib.error, urllib.request, xml.etree.ElementTree as ET, zipfile
from pathlib import Path
from typing import Any

EIN = "842403597"
EIN_BYTES = (b"842403597", b"84-2403597")
UA = "FedorMilovanov-Research-G3-IRS-Acquisition/4.0 (research-only)"

TARGETS = {
    "FY2022_LATER": {
        "index_year": 2023,
        "object_id": "202340569349300209",
        "tax_period_end": "2022-12-31",
        "expected_revenue": "1735978",
        "expected_expenses": "1010186",
        "batch_candidates": ["2023_TEOS_XML_10A"],
        "required": ["IRS990"],
        "use": "authoritative FY2022 Part IX baseline candidate for FY2023 delta",
    },
    "FY2023": {
        "index_year": 2024,
        "object_id": "202411429349300611",
        "tax_period_end": "2023-12-31",
        "expected_revenue": "1705689",
        "expected_expenses": "2071986",
        "batch_candidates": ["2024_TEOS_XML_05A"],
        "required": ["IRS990", "IRS990ScheduleO"],
        "use": "Part IX functional expenses and Schedule O control",
    },
    "FY2024": {
        "index_year": 2025,
        "object_id": "202541359349304489",
        "tax_period_end": "2024-12-31",
        "expected_revenue": "1212253",
        "expected_expenses": "1401429",
        "batch_candidates": ["2025_TEOS_XML_05B", "2025_TEOS_XML_05A"],
        "required": ["IRS990", "IRS990ScheduleL", "IRS990ScheduleO"],
        "use": "Schedule L interested-person rows and filing context",
    },
    "FY2025": {
        "index_year": 2026,
        "object_id": "202641339349303874",
        "tax_period_end": "2025-12-31",
        "expected_revenue": "399645",
        "expected_expenses": "950642",
        "batch_candidates": ["2026_TEOS_XML_05A", "2026_TEOS_XML_05B"],
        "required": ["IRS990", "IRS990ScheduleL", "IRS990ScheduleO"],
        "use": "Schedule L interested-person rows and filing context",
    },
}


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def lname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def norm(s: str) -> str:
    return "".join(c for c in s.upper() if c.isalnum())


def writej(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def req(url: str):
    return urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})


def fetch(url: str, timeout: int = 180):
    started = time.time()
    try:
        with urllib.request.urlopen(req(url), timeout=timeout) as r:
            b = r.read()
            return b, {
                "requested_url": url,
                "final_url": r.geturl(),
                "status": getattr(r, "status", None),
                "content_type": r.headers.get("Content-Type"),
                "bytes": len(b),
                "sha256": sha_bytes(b),
                "elapsed_seconds": round(time.time() - started, 3),
            }
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} for {url}: {e.reason}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"URL error for {url}: {e.reason}") from e


def fetch_file(url: str, path: Path, timeout: int = 900):
    started = time.time(); h = hashlib.sha256(); n = 0
    try:
        with urllib.request.urlopen(req(url), timeout=timeout) as r, path.open("wb") as f:
            while True:
                chunk = r.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk); h.update(chunk); n += len(chunk)
            return {
                "requested_url": url,
                "final_url": r.geturl(),
                "status": getattr(r, "status", None),
                "content_type": r.headers.get("Content-Type"),
                "bytes": n,
                "sha256": h.hexdigest(),
                "elapsed_seconds": round(time.time() - started, 3),
            }
    except Exception:
        path.unlink(missing_ok=True)
        raise


def index_row(csv_bytes: bytes, oid: str):
    rd = csv.DictReader(io.StringIO(csv_bytes.decode("utf-8-sig")))
    if not rd.fieldnames:
        raise RuntimeError("IRS index has no header")
    mapped = {norm(x): x for x in rd.fieldnames}
    object_col = mapped.get("OBJECTID"); ein_col = mapped.get("EIN")
    if not object_col:
        raise RuntimeError(f"No OBJECT_ID column: {rd.fieldnames}")
    for row in rd:
        if (row.get(object_col) or "").strip() == oid:
            clean = {k: (v or "").strip() for k, v in row.items() if k}
            if ein_col:
                found = "".join(c for c in clean.get(ein_col, "") if c.isdigit())
                if found not in ("", EIN):
                    raise RuntimeError(f"EIN mismatch in IRS index: {found}")
            return clean
    raise RuntimeError(f"Object {oid} not found in IRS index")


def rowval(row: dict[str, str], key: str) -> str:
    nk = norm(key)
    for k, v in row.items():
        if norm(k) == nk:
            return (v or "").strip()
    return ""


def batch_url(year: int, batch_id: str) -> str:
    return f"https://apps.irs.gov/pub/epostcard/990/xml/{year}/{batch_id}.zip"


def archive_inventory(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as z:
        infos = [i for i in z.infolist() if not i.is_dir()]
        methods: dict[str, int] = {}
        for i in infos:
            methods[str(i.compress_type)] = methods.get(str(i.compress_type), 0) + 1
        xmls = [i for i in infos if i.filename.lower().endswith(".xml")]
        return {
            "member_count": len(infos),
            "xml_member_count": len(xmls),
            "compression_method_counts": methods,
            "sample_members": [i.filename for i in xmls[:20]],
        }


def extract_archive_once(zpath: Path, dest: Path) -> dict[str, Any]:
    unzip = shutil.which("unzip")
    if not unzip:
        raise RuntimeError("system unzip is required for Deflate64 TEOS batches")
    started = time.time()
    p = subprocess.run([unzip, "-qq", str(zpath), "-d", str(dest)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    meta = {
        "tool": unzip,
        "returncode": p.returncode,
        "elapsed_seconds": round(time.time() - started, 3),
        "stderr": p.stderr.decode("utf-8", "replace")[:2000],
    }
    if p.returncode != 0:
        raise RuntimeError(f"unzip failed rc={p.returncode}: {meta['stderr']}")
    return meta


def find_text(root: ET.Element, tag: str) -> str:
    for e in root.iter():
        if lname(e.tag) == tag and (e.text or "").strip():
            return (e.text or "").strip()
    return ""


def identity_from_xml(data: bytes) -> dict[str, str]:
    root = ET.fromstring(data)
    names = [
        (e.text or "").strip()
        for e in root.iter()
        if lname(e.tag) == "BusinessNameLine1Txt" and (e.text or "").strip()
    ]
    eins = [
        "".join(c for c in (e.text or "") if c.isdigit())
        for e in root.iter()
        if lname(e.tag) == "EIN" and (e.text or "").strip()
    ]
    return {
        "ein": EIN if EIN in eins else (eins[0] if eins else ""),
        "tax_period_end": find_text(root, "TaxPeriodEndDt"),
        "return_ts": find_text(root, "ReturnTs"),
        "revenue": find_text(root, "CYTotalRevenueAmt"),
        "expenses": find_text(root, "CYTotalExpensesAmt"),
        "business_names": " | ".join(names[:5]),
    }


def candidate_score(identity: dict[str, str], target: dict[str, Any]) -> tuple[int, list[str]]:
    score = 0; reasons = []
    if identity.get("ein") == EIN:
        score += 10; reasons.append("EIN")
    if identity.get("tax_period_end") == target["tax_period_end"]:
        score += 5; reasons.append("tax_period_end")
    if identity.get("revenue") == target["expected_revenue"]:
        score += 3; reasons.append("revenue")
    if identity.get("expenses") == target["expected_expenses"]:
        score += 3; reasons.append("expenses")
    if "G3 MINISTRIES" in identity.get("business_names", "").upper():
        score += 2; reasons.append("business_name")
    return score, reasons


def scan_extracted(extract_dir: Path, target: dict[str, Any]):
    candidates = []
    xml_paths = list(extract_dir.rglob("*.xml"))
    for p in xml_paths:
        try:
            data = p.read_bytes()
        except OSError:
            continue
        if not any(e in data for e in EIN_BYTES):
            continue
        try:
            ident = identity_from_xml(data)
        except ET.ParseError:
            continue
        score, reasons = candidate_score(ident, target)
        candidates.append((score, reasons, p, data, ident))

    if not candidates:
        rev = target["expected_revenue"].encode(); exp = target["expected_expenses"].encode()
        for p in xml_paths:
            try:
                data = p.read_bytes()
            except OSError:
                continue
            if rev not in data or exp not in data:
                continue
            try:
                ident = identity_from_xml(data)
            except ET.ParseError:
                continue
            score, reasons = candidate_score(ident, target)
            candidates.append((score, reasons, p, data, ident))

    candidates.sort(key=lambda x: x[0], reverse=True)
    if not candidates:
        return None, {"xml_files_scanned": len(xml_paths), "candidate_count": 0}

    top = candidates[0]
    if top[0] < 15:
        summary = [
            {"score": c[0], "reasons": c[1], "file": c[2].name, "identity": c[4]}
            for c in candidates[:10]
        ]
        raise RuntimeError(f"No candidate met identity threshold: {summary}")
    if len(candidates) > 1 and candidates[1][0] == top[0]:
        summary = [
            {"score": c[0], "reasons": c[1], "file": c[2].name, "identity": c[4]}
            for c in candidates[:10]
        ]
        raise RuntimeError(f"Ambiguous top identity candidates: {summary}")
    return top, {
        "xml_files_scanned": len(xml_paths),
        "candidate_count": len(candidates),
        "selected_score": top[0],
        "selected_reasons": top[1],
        "selected_identity": top[4],
    }


def flatten(elem: ET.Element):
    out = []
    def walk(node: ET.Element, path: list[str]):
        nm = lname(node.tag); pth = path + [nm]; kids = list(node)
        text = (node.text or "").strip(); attrs = {lname(k): v for k, v in node.attrib.items()}
        if not kids:
            if text or attrs:
                out.append({"path": "/".join(pth), "tag": nm, "text": text, "attributes": attrs})
            return
        if text:
            out.append({"path": "/".join(pth), "tag": nm, "text": text, "attributes": attrs, "container_text": True})
        for c in kids:
            walk(c, pth)
    walk(elem, [])
    return out


def save_return(label: str, target: dict[str, Any], out: Path, row: dict[str, str], index_meta: dict[str, Any],
                batch_meta: dict[str, Any], batch_id: str, member_path: Path, data: bytes, scan_meta: dict[str, Any]):
    d = out / label; d.mkdir(parents=True, exist_ok=True)
    raw = d / f"{target['object_id']}_public.xml"
    raw.write_bytes(data)
    root = ET.fromstring(data)
    components: dict[str, Any] = {}
    for comp in target["required"]:
        matches = [e for e in root.iter() if lname(e.tag) == comp]
        components[comp] = {"count": len(matches)}
        for idx, m in enumerate(matches, 1):
            suffix = "" if len(matches) == 1 else f"_{idx:02d}"
            frag = ET.tostring(m, encoding="utf-8", xml_declaration=True)
            fn = f"{comp}{suffix}.xml"
            (d / fn).write_bytes(frag)
            leaves = flatten(m)
            writej(d / f"{comp}{suffix}_LEAVES.json", leaves)
            components[comp].setdefault("objects", []).append({
                "file": fn, "bytes": len(frag), "sha256": sha_bytes(frag), "leaf_count": len(leaves)
            })
    missing = [x for x in target["required"] if components.get(x, {}).get("count", 0) == 0]
    writej(d / "COMPONENT_SUMMARY.json", components)
    if missing:
        raise RuntimeError(f"Matched return is missing required component(s): {missing}")
    custody = {
        "label": label,
        "ein": EIN,
        "object_id": target["object_id"],
        "research_use": target["use"],
        "index_row": row,
        "index_fetch": index_meta,
        "batch_id": batch_id,
        "batch": batch_meta,
        "source_member": member_path.name,
        "member_identity": scan_meta,
        "xml": {"file": raw.name, "bytes": len(data), "sha256": sha_bytes(data)},
        "components": components,
        "state": "EPHEMERAL_ACTION_ARTIFACT",
        "publication_eligible": False,
        "raw_xml": True,
        "batch_archive_retained": False,
    }
    writej(d / "CUSTODY.json", custody)
    writej(d / "IRS_INDEX_ROW.json", row)
    writej(d / "IRS_INDEX_FETCH.json", index_meta)
    return custody


def acquire(label: str, target: dict[str, Any], out: Path):
    d = out / label; d.mkdir(parents=True, exist_ok=True)
    year = target["index_year"]; oid = target["object_id"]
    idx_url = f"https://apps.irs.gov/pub/epostcard/990/xml/{year}/index_{year}.csv"
    idx, index_meta = fetch(idx_url)
    row = index_row(idx, oid)
    indexed_batch = rowval(row, "XML_BATCH_ID")
    batch_ids = list(target.get("batch_candidates") or [])
    if indexed_batch and indexed_batch not in batch_ids:
        batch_ids.insert(0, indexed_batch)
    if not batch_ids:
        raise RuntimeError("No batch candidates available for target")

    attempts = []
    for batch_id in batch_ids:
        with tempfile.TemporaryDirectory(prefix=f"g3-{label.lower()}-") as td:
            tmp = Path(td); zpath = tmp / f"{batch_id}.zip"; extract_dir = tmp / "xml"; extract_dir.mkdir()
            url = batch_url(year, batch_id)
            try:
                fetch_meta = fetch_file(url, zpath)
            except Exception as e:
                attempts.append({"batch_id": batch_id, "url": url, "stage": "download", "error": str(e)})
                continue
            inventory = archive_inventory(zpath)
            try:
                extraction = extract_archive_once(zpath, extract_dir)
                top, scan_meta = scan_extracted(extract_dir, target)
            except Exception as e:
                attempts.append({
                    "batch_id": batch_id, "url": url, "stage": "extract_or_scan", "fetch": fetch_meta,
                    "inventory": inventory, "error": str(e)
                })
                continue
            if top is None:
                attempts.append({
                    "batch_id": batch_id, "url": url, "stage": "identity_miss", "fetch": fetch_meta,
                    "inventory": inventory, "extraction": extraction, "scan": scan_meta
                })
                continue
            score, reasons, member_path, data, ident = top
            batch_meta = {
                "fetch": fetch_meta,
                "inventory": inventory,
                "extraction": extraction,
                "identity_score": score,
                "identity_reasons": reasons,
                "discovered_member": member_path.name,
                "discovered_member_bytes": len(data),
                "discovered_member_sha256": sha_bytes(data),
            }
            attempts.append({"batch_id": batch_id, "url": url, "stage": "matched", **batch_meta})
            writej(d / "BATCH_ATTEMPTS.json", attempts)
            return save_return(label, target, out, row, index_meta, batch_meta, batch_id, member_path, data, scan_meta)

    writej(d / "BATCH_ATTEMPTS.json", attempts)
    raise RuntimeError(f"Target not found in candidate batches: {[a.get('batch_id') for a in attempts]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="g3-irs-acquisition-output")
    ap.add_argument("--label", action="append", choices=sorted(TARGETS), help="target label; may be repeated")
    args = ap.parse_args()
    labels = args.label or ["FY2022_LATER", "FY2024", "FY2025"]
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    summary = {"ein": EIN, "labels": labels, "targets": [], "errors": [], "state": "EPHEMERAL_ACTION_ARTIFACT", "publication_eligible": False}
    for label in labels:
        try:
            summary["targets"].append(acquire(label, TARGETS[label], out))
        except Exception as e:
            summary["errors"].append({"label": label, "object_id": TARGETS[label]["object_id"], "error": str(e)})
    writej(out / "SUMMARY.json", summary)
    for t in summary["targets"]:
        print(f"ACQUIRED {t['label']} object={t['object_id']} member={t['source_member']} sha256={t['xml']['sha256']}")
    for e in summary["errors"]:
        print(f"ERROR {e['label']} {e['object_id']}: {e['error']}", file=sys.stderr)
    return 2 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
