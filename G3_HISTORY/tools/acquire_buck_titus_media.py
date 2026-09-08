#!/usr/bin/env python3
"""Read-only acquisition of the public FBC Lindale / Vimeo Titus 2 sermon object.

Purpose:
- resolve public media metadata;
- inventory subtitles/captions;
- acquire only a short local audio segment around the dossier timestamp;
- hash/transcribe it locally;
- DELETE audio before artifact upload.

This tool does not make publication claims and does not promote ITEM_VERIFIED.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
from datetime import datetime, timezone

URL = "https://vimeo.com/852173553"
START = "00:32:30"
END = "00:36:30"
OUT = pathlib.Path(os.environ.get("G3_MEDIA_EVIDENCE_OUT", "g3-media-evidence"))
TMP = pathlib.Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "g3-titus-media"


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    p = subprocess.run(cmd, text=True, capture_output=True)
    if check and p.returncode != 0:
        raise RuntimeError(
            f"command failed ({p.returncode}): {' '.join(cmd)}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}"
        )
    return p


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)

    receipt: dict[str, object] = {
        "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_url": URL,
        "requested_segment": {"start": START, "end": END},
        "publication_authorized": False,
        "item_verified": False,
        "audio_binary_retained": False,
    }

    # Tool versions.
    versions = {}
    for name, cmd in {
        "yt_dlp": ["yt-dlp", "--version"],
        "ffmpeg": ["ffmpeg", "-version"],
        "ffprobe": ["ffprobe", "-version"],
    }.items():
        p = run(cmd, check=False)
        versions[name] = (p.stdout or p.stderr).splitlines()[0] if (p.stdout or p.stderr) else None
    receipt["tool_versions"] = versions

    # Public metadata.
    meta_proc = run(["yt-dlp", "--dump-single-json", "--no-warnings", URL])
    metadata = json.loads(meta_proc.stdout)
    (OUT / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    receipt["metadata"] = {
        "id": metadata.get("id"),
        "title": metadata.get("title"),
        "uploader": metadata.get("uploader"),
        "uploader_id": metadata.get("uploader_id"),
        "duration": metadata.get("duration"),
        "timestamp": metadata.get("timestamp"),
        "upload_date": metadata.get("upload_date"),
        "webpage_url": metadata.get("webpage_url"),
        "extractor": metadata.get("extractor"),
    }

    # Subtitle inventory (non-fatal if none exist).
    subs = run(["yt-dlp", "--list-subs", URL], check=False)
    (OUT / "subtitle_inventory.txt").write_text(
        f"RETURN_CODE={subs.returncode}\n\nSTDOUT\n{subs.stdout}\n\nSTDERR\n{subs.stderr}", encoding="utf-8"
    )

    # Try downloading subtitle files only; absence is not failure.
    run([
        "yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs",
        "--sub-langs", "en.*,en", "--sub-format", "vtt/best",
        "-o", str(OUT / "captions.%(ext)s"), URL
    ], check=False)

    # Acquire short public-media audio segment to ephemeral runner storage only.
    template = str(TMP / "titus_segment.%(ext)s")
    dl = run([
        "yt-dlp", "--no-playlist", "-f", "bestaudio/best",
        "--download-sections", f"*{START}-{END}",
        "--force-keyframes-at-cuts", "-x", "--audio-format", "wav",
        "-o", template, URL
    ])
    (OUT / "yt_dlp_segment_log.txt").write_text(dl.stdout + "\n" + dl.stderr, encoding="utf-8")

    wavs = sorted(TMP.glob("titus_segment*.wav"))
    if not wavs:
        raise RuntimeError("yt-dlp completed but no WAV segment was produced")
    audio = wavs[0]

    probe = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration,size,bit_rate",
        "-of", "json", str(audio)
    ])
    probe_json = json.loads(probe.stdout)
    receipt["segment"] = {
        "sha256": sha256(audio),
        "size_bytes": audio.stat().st_size,
        "ffprobe": probe_json,
    }

    # Machine transcript is explicitly staging evidence, not human verification.
    whisper_cmd = shutil.which("whisper")
    if whisper_cmd:
        tr = run([
            whisper_cmd, str(audio), "--model", os.environ.get("WHISPER_MODEL", "base.en"),
            "--language", "en", "--task", "transcribe", "--fp16", "False",
            "--output_dir", str(OUT), "--output_format", "all", "--verbose", "False"
        ], check=False)
        (OUT / "whisper_log.txt").write_text(tr.stdout + "\n" + tr.stderr, encoding="utf-8")
        receipt["whisper_return_code"] = tr.returncode
        receipt["machine_transcript_only"] = True
    else:
        receipt["whisper_return_code"] = None
        receipt["machine_transcript_only"] = True
        receipt["whisper_note"] = "whisper CLI unavailable"

    # Audio must not survive into artifact staging.
    audio.unlink(missing_ok=True)
    for p in TMP.iterdir():
        if p.is_file():
            p.unlink(missing_ok=True)
    receipt["audio_binary_retained"] = False

    (OUT / "ACQUISITION_RECEIPT.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUT / "README.txt").write_text(
        "Research-only original-media acquisition. The audio segment was used ephemerally and deleted.\n"
        "Any transcript here is machine-generated and MUST NOT be treated as human-verified quotation.\n"
        "ITEM_VERIFIED remains false until a human checks original audio + exact source edition + attribution context.\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        raise
