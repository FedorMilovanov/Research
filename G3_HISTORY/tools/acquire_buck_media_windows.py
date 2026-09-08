#!/usr/bin/env python3
"""Ephemeral original-media segment acquisition for high-value Tom Buck dossier items.

The script uses only public First Baptist Lindale sermon landing pages. It acquires
narrow windows around dossier timestamps, hashes/transcribes them locally, then
deletes all audio before any artifact upload.

Machine transcripts are diagnostics only: they are never human-verified quotation
and never promote an item to ITEM_VERIFIED.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ITEMS = {
    11: {
        "title": "Romans 7:1-6",
        "date": "2024-01-07",
        "page": "https://fbclindale.com/resources/sermons/romans-71-6/",
        "vimeo": "900633606",
        "windows": [("17_02_19_00", "00:16:30", "00:19:35"), ("32_23", "00:31:50", "00:33:10")],
    },
    12: {
        "title": "Romans 15:1-6",
        "date": "2025-10-19",
        "page": "https://fbclindale.com/resources/sermons/romans-151-6/",
        "vimeo": "1128676834",
        "windows": [("16_00_17_31", "00:15:30", "00:18:30"), ("41_05", "00:40:30", "00:41:35")],
    },
    13: {
        "title": "Romans 16:25-27",
        "date": "2025-12-21",
        "page": "https://fbclindale.com/resources/sermons/romans-1625-27-2/",
        "vimeo": "1149768050",
        "windows": [("37_48", "00:37:15", "00:39:15")],
    },
    14: {
        "title": "Joshua 1:1-9",
        "date": "2026-01-18",
        "page": "https://fbclindale.com/resources/sermons/joshua-11-9/",
        "vimeo": "1156717093",
        "windows": [("17_58", "00:17:20", "00:18:40"), ("28_41_33_20", "00:28:00", "00:33:50")],
    },
    15: {
        "title": "Joshua 2:1-24",
        "date": "2026-02-08",
        "page": "https://fbclindale.com/resources/sermons/joshua-21-24/",
        "vimeo": "1163070006",
        "windows": [
            ("05_18_10_29", "00:04:40", "00:11:15"),
            ("20_39", "00:19:50", "00:21:20"),
            ("32_30_33_32", "00:31:50", "00:34:15"),
            ("43_43", "00:43:10", "00:44:20"),
        ],
    },
    16: {
        "title": "Joshua 3:1-17",
        "date": "2026-02-15",
        "page": "https://fbclindale.com/resources/sermons/joshua-31-17/",
        "vimeo": "1165204580",
        "windows": [
            ("15_18", "00:14:40", "00:16:05"),
            ("24_33", "00:23:45", "00:25:15"),
            ("29_48_41_55", "00:29:10", "00:42:30"),
        ],
    },
    17: {
        "title": "Joshua 4:1-24",
        "date": "2026-03-01",
        "page": "https://fbclindale.com/resources/sermons/joshua-41-24/",
        "vimeo": "1169432943",
        "windows": [
            ("09_23_12_18", "00:08:50", "00:12:50"),
            ("31_31_35_18", "00:30:50", "00:36:00"),
            ("43_12", "00:42:35", "00:44:10"),
            ("48_14_50_49", "00:47:35", "00:51:20"),
        ],
    },
}


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    try:
        proc = subprocess.run(cmd, text=True, capture_output=True)
    except FileNotFoundError as exc:
        if check:
            raise
        return subprocess.CompletedProcess(cmd, 127, "", str(exc))
    if check and proc.returncode != 0:
        raise RuntimeError(f"command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stderr}")
    return proc


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_log(path: pathlib.Path, proc: subprocess.CompletedProcess[str]) -> None:
    path.write_text(
        f"RETURN_CODE={proc.returncode}\n\nSTDOUT\n{proc.stdout}\n\nSTDERR\n{proc.stderr}",
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--item", type=int, required=True, choices=sorted(ITEMS))
    args = ap.parse_args()
    cfg = ITEMS[args.item]

    out_root = pathlib.Path(os.environ.get("G3_BUCK_MEDIA_OUT", "g3-buck-media-evidence"))
    out = out_root / f"item-{args.item:02d}"
    out.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(os.environ.get("RUNNER_TEMP", "/tmp")) / f"g3-buck-item-{args.item:02d}"
    tmp.mkdir(parents=True, exist_ok=True)

    receipt: dict[str, object] = {
        "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
        "item": args.item,
        "sermon_title": cfg["title"],
        "sermon_date": cfg["date"],
        "official_fbc_page": cfg["page"],
        "expected_vimeo_id": cfg["vimeo"],
        "authentication_used": False,
        "publication_authorized": False,
        "item_verified": False,
        "machine_transcript_only": True,
        "audio_binary_retained": False,
        "windows": [],
    }

    meta_proc = run(["yt-dlp", "--dump-single-json", "--no-warnings", cfg["page"]], check=False)
    write_log(out / "metadata_attempt.txt", meta_proc)
    if meta_proc.returncode != 0:
        receipt["acquisition_result"] = "PUBLIC_MEDIA_METADATA_HOLD"
        (out / "ACQUISITION_RECEIPT.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
        print(json.dumps(receipt, indent=2))
        return 0
    try:
        metadata = json.loads(meta_proc.stdout)
    except Exception as exc:
        receipt["acquisition_result"] = "PUBLIC_MEDIA_METADATA_PARSE_HOLD"
        receipt["metadata_parse_error"] = repr(exc)
        (out / "ACQUISITION_RECEIPT.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
        print(json.dumps(receipt, indent=2))
        return 0

    receipt["resolved_media"] = {
        "id": metadata.get("id"),
        "title": metadata.get("title"),
        "duration": metadata.get("duration"),
        "webpage_url": metadata.get("webpage_url"),
        "extractor": metadata.get("extractor"),
    }
    (out / "RESOLVED_MEDIA.json").write_text(json.dumps(receipt["resolved_media"], indent=2), encoding="utf-8")

    whisper = shutil.which("whisper")
    for label, start, end in cfg["windows"]:
        template = str(tmp / f"{label}.%(ext)s")
        dl = run([
            "yt-dlp", "--no-playlist", "-f", "bestaudio/best",
            "--download-sections", f"*{start}-{end}", "--force-keyframes-at-cuts",
            "-x", "--audio-format", "wav", "-o", template, cfg["page"],
        ], check=False)
        write_log(out / f"yt_dlp_{label}.txt", dl)
        row: dict[str, object] = {"label": label, "start": start, "end": end, "download_return_code": dl.returncode}
        wavs = sorted(tmp.glob(f"{label}*.wav"))
        if dl.returncode != 0 or not wavs:
            row["state"] = "SEGMENT_HOLD"
            receipt["windows"].append(row)
            continue
        wav = wavs[0]
        probe = run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration,size,bit_rate",
            "-of", "json", str(wav),
        ], check=False)
        row.update({
            "state": "SEGMENT_ACQUIRED_EPHEMERALLY",
            "sha256": sha256(wav),
            "size_bytes": wav.stat().st_size,
            "ffprobe": json.loads(probe.stdout) if probe.returncode == 0 and probe.stdout else None,
        })
        if whisper:
            tr = run([
                whisper, str(wav), "--model", os.environ.get("WHISPER_MODEL", "base.en"),
                "--language", "en", "--task", "transcribe", "--fp16", "False",
                "--output_dir", str(out), "--output_format", "json", "--verbose", "False",
            ], check=False)
            write_log(out / f"whisper_{label}.txt", tr)
            # Whisper names output after the input stem. Rename deterministically if present.
            generated = out / f"{wav.stem}.json"
            target = out / f"machine_transcript_{label}.json"
            if generated.exists():
                generated.replace(target)
            row["whisper_return_code"] = tr.returncode
            row["machine_transcript_path"] = target.name if target.exists() else None
        else:
            row["whisper_return_code"] = None
            row["whisper_note"] = "whisper CLI unavailable"
        wav.unlink(missing_ok=True)
        receipt["windows"].append(row)

    for p in tmp.glob("*"):
        if p.is_file():
            p.unlink(missing_ok=True)
    receipt["audio_binary_retained"] = False
    acquired = sum(1 for row in receipt["windows"] if row.get("state") == "SEGMENT_ACQUIRED_EPHEMERALLY")
    receipt["acquisition_result"] = "SEGMENTS_ACQUIRED_EPHEMERALLY" if acquired else "SEGMENT_ACCESS_HOLD"
    receipt["segments_acquired"] = acquired
    receipt["segments_requested"] = len(cfg["windows"])
    (out / "ACQUISITION_RECEIPT.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "README.txt").write_text(
        "Research-only bounded original-media acquisition. No audio is retained.\n"
        "Machine transcripts are diagnostic and not quote-safe. ITEM_VERIFIED remains false until human audio/source/attribution review.\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "item": args.item,
        "result": receipt["acquisition_result"],
        "segments_acquired": acquired,
        "segments_requested": len(cfg["windows"]),
        "item_verified": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        raise
