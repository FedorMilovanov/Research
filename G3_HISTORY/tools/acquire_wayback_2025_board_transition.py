#!/usr/bin/env python3
"""Acquire legacy G3 leadership-page captures around the May–July 2025 transition.

The current-era `/about/who-we-are/` path has already been exhaustively tested for
2025-05-01 through 2025-07-20 and returned three valid empty monthly CDX shards.
Search indexes independently expose the historical official route
`/vision/leadership/` with title `Who We Are`. This version tests that concrete
legacy route only; it does not repeat the exhausted current-era path.

Research-only, read-only acquisition. CDX is sharded by month. Every shard must
return valid JSON. Transient transport/HTTP failures receive a small bounded retry
budget; exhausted transport retries, non-retryable HTTP responses and parse/schema
failures fail closed. A valid empty result is archive coverage only, never evidence
of board continuity or absence.
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

TARGET = "http://g3min.org/vision/leadership/"
CDX_TARGET = "g3min.org/vision/leadership/"
WINDOWS = [
    ("20250501", "20250531", "2025-05"),
    ("20250601", "20250630", "2025-06"),
    ("20250701", "20250720", "2025-07-01_20"),
]
UA = "FedorMilovanov-Research-G3-2025-Legacy-Leadership/2.1 (research-only)"
ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"
RETRYABLE_HTTP = {429, 500, 502, 503, 504}
RETRY_DELAYS = (2, 6)

NAMES = [
    "Joshua Buice",
    "Josh Buice",
    "Tom Buck",
    "Chip Thornton",
    "Chipley Thornton",
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


def fetch(url: str, timeout: int = 120, attempts: int = 3):
    """Fetch with bounded retries for transient transport/5xx failures only."""
    for attempt in range(1, attempts + 1):
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
                    "attempt": attempt,
                    "max_attempts": attempts,
                }
        except urllib.error.HTTPError as exc:
            body = exc.read()
            message = (
                f"HTTP {exc.code} {exc.reason} url={url} "
                f"body_sha256={sha(body)} bytes={len(body)} attempt={attempt}/{attempts}"
            )
            if exc.code not in RETRYABLE_HTTP or attempt >= attempts:
                raise RuntimeError(message) from exc
        except urllib.error.URLError as exc:
            message = f"URL error {exc.reason} url={url} attempt={attempt}/{attempts}"
            if attempt >= attempts:
                raise RuntimeError(message) from exc
        except TimeoutError as exc:
            message = f"Timeout url={url} attempt={attempt}/{attempts}"
            if attempt >= attempts:
                raise RuntimeError(message) from exc

        delay = RETRY_DELAYS[min(attempt - 1, len(RETRY_DELAYS) - 1)]
        print("TRANSIENT_RETRY", f"attempt={attempt}/{attempts}", f"sleep={delay}s", url, file=sys.stderr)
        time.sleep(delay)

    raise RuntimeError(f"fetch exhausted unexpectedly url={url}")


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


def parse_cdx_rows(data: bytes, label: str) -> tuple[list[dict], str]:
    rows = json.loads(data.decode("utf-8"))
    if not isinstance(rows, list):
        raise RuntimeError(f"{label}: CDX JSON root is not a list")
    if not rows:
        return [], "VALID_EMPTY_CDX"
    header = rows[0]
    if not isinstance(header, list) or "timestamp" not in header:
        raise RuntimeError(f"{label}: CDX response has an invalid header row")
    captures = [
        dict(zip(header, row))
        for row in rows[1:]
        if isinstance(row, list) and len(row) == len(header)
    ]
    return captures, "CAPTURES_PRESENT" if captures else "VALID_HEADER_ZERO_ROWS"


def query_segment(out: Path, start: str, end: str, label: str) -> tuple[list[dict], dict]:
    params = {
        "url": CDX_TARGET,
        "from": start,
        "to": end,
        "output": "json",
        "fl": "timestamp,original,statuscode,mimetype,digest,length",
        "filter": "statuscode:200",
    }
    url = "https://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode(params)
    data, meta = fetch(url, 45)
    safe = label.replace("/", "_")
    (out / f"CDX_LEGACY_{safe}.json").write_bytes(data)
    write_json(out / f"CDX_LEGACY_{safe}_FETCH.json", meta)
    captures, state = parse_cdx_rows(data, label)
    return captures, {
        "label": label,
        "from": start,
        "to": end,
        "state": state,
        "capture_count": len(captures),
        "timestamps": [item.get("timestamp") for item in captures],
        "fetch": meta,
    }


def select_captures(captures: list[dict]) -> list[dict]:
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
    lines = text.splitlines()
    needles = (
        "board of directors",
        "board chairman",
        "board",
        "tom buck",
        "jonathan frazier",
        "leadership",
    )
    first = None
    for idx, line in enumerate(lines):
        low = line.casefold()
        if any(needle in low for needle in needles):
            first = idx
            break
    if first is None:
        return ""
    return "\n".join(lines[max(0, first - 10):min(len(lines), first + 110)])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="g3-wayback-2025-board-output")
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    summary = {
        "target": TARGET,
        "target_kind": "LEGACY_INDEX_DISCOVERED_WHO_WE_ARE_ROUTE",
        "windows": [{"from": a, "to": b, "label": c} for a, b, c in WINDOWS],
        "state": "EPHEMERAL_ACTION_ARTIFACT",
        "publication_eligible": False,
        "errors": [],
        "segments": [],
        "captures": [],
        "negative_result_boundary": (
            "Archive coverage is not evidence of board continuity, absence, resignation, or non-resignation."
        ),
    }

    captures: list[dict] = []
    for start, end, label in WINDOWS:
        try:
            rows, meta = query_segment(out, start, end, label)
            captures.extend(rows)
            summary["segments"].append(meta)
        except Exception as exc:
            summary["errors"].append(f"CDX {label}: {exc}")
            summary["segments"].append(
                {"label": label, "from": start, "to": end, "state": "ERROR", "error": str(exc)}
            )

    by_ts: dict[str, dict] = {}
    for item in captures:
        ts = item.get("timestamp", "")
        if ts:
            by_ts.setdefault(ts, item)
    captures = sorted(by_ts.values(), key=lambda item: item.get("timestamp", ""))

    summary["cdx_capture_count"] = len(captures)
    summary["cdx_timestamps"] = [item.get("timestamp") for item in captures]
    summary["distinct_digests"] = len({item.get("digest") for item in captures if item.get("digest")})
    if not summary["errors"] and not captures:
        summary["coverage_state"] = "VALID_EMPTY_ALL_LEGACY_SEGMENTS"

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
            raw, meta = fetch(snapshot_url, 90)
            raw_name = f"{ts}_legacy-leadership.raw"
            (out / raw_name).write_bytes(raw)
            decoded, method = decode_payload(raw)
            html_name = f"{ts}_legacy-leadership.html"
            (out / html_name).write_bytes(decoded)
            text = extract_text(decoded)
            text_name = f"{ts}_legacy-leadership.txt"
            (out / text_name).write_text(text, encoding="utf-8")
            context = board_context(text)
            (out / f"{ts}_legacy-board-context.txt").write_text(context, encoding="utf-8")
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
                    "board_heading_present": bool(re.search(r"board(?: of directors| chairman)?", text, re.I)),
                    "board_context": context[:14000],
                }
            )
        except Exception as exc:
            record["error"] = str(exc)
            summary["errors"].append(f"snapshot {ts}: {exc}")
        summary["captures"].append(record)

    write_json(out / "SUMMARY.json", summary)

    print("TARGET", TARGET)
    for segment in summary["segments"]:
        print("CDX_SEGMENT", segment.get("label"), segment.get("state"), "count=", segment.get("capture_count", 0))
    print("CDX_CAPTURE_COUNT", summary["cdx_capture_count"])
    print("CDX_TIMESTAMPS", ",".join(ts or "" for ts in summary["cdx_timestamps"]))
    print("DISTINCT_DIGESTS", summary["distinct_digests"])
    if summary.get("coverage_state"):
        print("COVERAGE_STATE", summary["coverage_state"])
    for record in summary["captures"]:
        if record.get("fetch"):
            present = [name for name, hit in record.get("name_hits", {}).items() if hit]
            print("ACQUIRED", record["cdx"].get("timestamp"), "NAMES", " | ".join(present))
            if record.get("board_context"):
                print("BOARD_CONTEXT_BEGIN", record["cdx"].get("timestamp"))
                print(record["board_context"][:6000])
                print("BOARD_CONTEXT_END", record["cdx"].get("timestamp"))
        else:
            print("SNAPSHOT_ERROR", record.get("snapshot_url"), record.get("error"), file=sys.stderr)

    if summary["errors"]:
        for error in summary["errors"]:
            print("ERROR", error, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
