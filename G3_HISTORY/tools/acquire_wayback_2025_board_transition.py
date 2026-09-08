#!/usr/bin/env python3
"""Acquire official G3 Who-We-Are captures around the May–July 2025 board transition.

Research-only, read-only acquisition. The lane queries every Wayback CDX timestamp
(no digest collapse) for the official G3 board page from 2025-05-01 through
2025-07-20, fetches a bounded set of captures that preserves every digest change,
decodes archived payloads, and records person-name hits plus nearby board text.

A successful run proves only what the archive returned. Zero captures is an archive
coverage result, not evidence that the board/page did not exist or did not change.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

TARGET = "http://g3min.org/about/who-we-are/"
CDX_TARGET = "g3min.org/about/who-we-are/"
FROM = "20250501"
TO = "20250720"
UA = "FedorMilovanov-Research-G3-2025-Board-Transition/1.1 (research-only)"
ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"

NAMES = [
    "Joshua Buice",
    "Tom Buck",
    "Chip Thornton",
    "Buck Braswell",
    "Adam Burrell",
    "Matt Broome",
    "Jonathan Frazier",
    "Scott Aniol",
    "Jon Norton",
    "Matt Sikes",
    "Dylan Joyner",
    "Ron Mooney",
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        value = " ".join(data.split())
        if value:
            self.parts.append(value)


def extract_text(data: bytes) -> str:
    parser = TextExtractor()
    parser.feed(data.decode("utf-8", "replace"))
    return "\n".join(parser.parts)


def fetch(url: str, timeout: int = 120):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            return data, {
                "requested_url": url,
                "final_url": response.geturl(),
                "status": getattr(response, "status", None),
                "content_type": response.headers.get("Content-Type"),
                "content_encoding": response.headers.get("Content-Encoding"),
                "bytes": len(data),
                "sha256": sha(data),
                "elapsed_seconds": round(time.time() - started, 3),
            }
    except urllib.error.HTTPError as exc:
        body = exc.read()
        raise RuntimeError(
            f"HTTP {exc.code} {exc.reason} url={url} body_sha256={sha(body)} bytes={len(body)}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"URL error {exc.reason} url={url}") from exc


def decode_payload(raw: bytes):
    if raw.startswith(ZSTD_MAGIC):
        zstd = shutil.which("zstd")
        if not zstd:
            raise RuntimeError("Zstandard payload detected but zstd CLI is unavailable")
        proc = subprocess.run(
            [zstd, "-d", "-q", "-c"],
            input=raw,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode:
            raise RuntimeError("zstd decode failed: " + proc.stderr.decode("utf-8", "replace")[:500])
        return proc.stdout, "zstd-cli"
    return raw, "identity"


def select_captures(captures: list[dict]) -> list[dict]:
    """Preserve first, last and every digest transition without duplicate timestamps."""
    rows = sorted(captures, key=lambda item: item.get("timestamp", ""))
    if not rows:
        return []
    chosen: list[dict] = []
    seen_ts: set[str] = set()
    previous_digest = object()

    def add(row: dict) -> None:
        ts = row.get("timestamp", "")
        if ts and ts not in seen_ts:
            chosen.append(row)
            seen_ts.add(ts)

    add(rows[0])
    for row in rows:
        digest = row.get("digest")
        if digest != previous_digest:
            add(row)
            previous_digest = digest
    add(rows[-1])
    return sorted(chosen, key=lambda item: item.get("timestamp", ""))


def board_context(text: str) -> str:
    """Return bounded text around the first board heading/name cluster for audit logs."""
    lines = text.splitlines()
    needles = ("board of directors", "board", "tom buck", "jonathan frazier")
    first = None
    for idx, line in enumerate(lines):
        low = line.casefold()
        if any(needle in low for needle in needles):
            first = idx
            break
    if first is None:
        return ""
    start = max(0, first - 8)
    end = min(len(lines), first + 80)
    return "\n".join(lines[start:end])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="g3-wayback-2025-board-output")
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    params = {
        "url": CDX_TARGET,
        "from": FROM,
        "to": TO,
        "output": "json",
        "fl": "timestamp,original,statuscode,mimetype,digest,length",
        "filter": "statuscode:200",
    }
    cdx_url = "https://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode(params)
    summary = {
        "target": TARGET,
        "window": {"from": FROM, "to": TO},
        "state": "EPHEMERAL_ACTION_ARTIFACT",
        "publication_eligible": False,
        "negative_result_boundary": (
            "Archive coverage is not evidence of board continuity, absence, resignation, or non-resignation."
        ),
        "errors": [],
        "captures": [],
    }

    captures: list[dict] = []
    try:
        cdx_bytes, cdx_meta = fetch(cdx_url, 90)
        (out / "CDX.json").write_bytes(cdx_bytes)
        write_json(out / "CDX_FETCH.json", cdx_meta)
        rows = json.loads(cdx_bytes.decode("utf-8"))
        if not isinstance(rows, list):
            raise RuntimeError("CDX JSON root is not a list")
        if rows:
            header = rows[0]
            if not isinstance(header, list) or "timestamp" not in header:
                raise RuntimeError("CDX response has an invalid header row")
            captures = [
                dict(zip(header, row))
                for row in rows[1:]
                if isinstance(row, list) and len(row) == len(header)
            ]
        else:
            # Wayback returns [] when the query is valid but has zero captures.
            # This is a bounded archive-coverage result, not a transport failure.
            captures = []
            summary["coverage_state"] = "VALID_EMPTY_CDX"
    except Exception as exc:
        captures = []
        summary["errors"].append("CDX: " + str(exc))

    captures = sorted(captures, key=lambda item: item.get("timestamp", ""))
    summary["cdx_capture_count"] = len(captures)
    summary["cdx_timestamps"] = [item.get("timestamp") for item in captures]
    summary["distinct_digests"] = len({item.get("digest") for item in captures if item.get("digest")})
    selected = select_captures(captures)
    summary["selected_capture_timestamps"] = [item.get("timestamp") for item in selected]

    for item in selected[:50]:
        ts = item.get("timestamp", "")
        original = item.get("original") or TARGET
        if not ts:
            continue
        snapshot_url = f"https://web.archive.org/web/{ts}id_/{original}"
        record = {"cdx": item, "snapshot_url": snapshot_url}
        try:
            raw, meta = fetch(snapshot_url, 120)
            raw_name = f"{ts}_who-we-are.raw"
            (out / raw_name).write_bytes(raw)
            decoded, method = decode_payload(raw)
            html_name = f"{ts}_who-we-are.html"
            (out / html_name).write_bytes(decoded)
            text = extract_text(decoded)
            text_name = f"{ts}_who-we-are.txt"
            (out / text_name).write_text(text, encoding="utf-8")
            context = board_context(text)
            (out / f"{ts}_board-context.txt").write_text(context, encoding="utf-8")
            hits = {name: (name.casefold() in text.casefold()) for name in NAMES}
            record.update(
                {
                    "fetch": meta,
                    "raw_file": raw_name,
                    "raw_sha256": sha(raw),
                    "decoded_file": html_name,
                    "decoded_sha256": sha(decoded),
                    "decode_method": method,
                    "text_file": text_name,
                    "text_sha256": sha(text.encode()),
                    "name_hits": hits,
                    "board_heading_present": bool(re.search(r"board(?: of directors)?", text, re.I)),
                    "board_context": context[:12000],
                }
            )
        except Exception as exc:
            record["error"] = str(exc)
        summary["captures"].append(record)

    write_json(out / "SUMMARY.json", summary)

    print("CDX_CAPTURE_COUNT", summary["cdx_capture_count"])
    print("CDX_TIMESTAMPS", ",".join(ts or "" for ts in summary["cdx_timestamps"]))
    print("DISTINCT_DIGESTS", summary["distinct_digests"])
    if summary.get("coverage_state"):
        print("COVERAGE_STATE", summary["coverage_state"])
    for record in summary["captures"]:
        if record.get("fetch"):
            present = [name for name, hit in record.get("name_hits", {}).items() if hit]
            print("ACQUIRED", record["cdx"].get("timestamp"), "NAMES", " | ".join(present))
        else:
            print("SNAPSHOT_ERROR", record.get("snapshot_url"), record.get("error"), file=sys.stderr)

    # CDX transport/parse failure is technical failure. A successful empty [] is
    # deliberately green because it documents a bounded archive-coverage gap.
    if summary["errors"]:
        for error in summary["errors"]:
            print("ERROR", error, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
