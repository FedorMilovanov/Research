#!/usr/bin/env python3
"""Read-only acquisition of the public FBC Lindale / Vimeo Titus 2 sermon object.

Purpose:
- resolve public media metadata through unauthenticated public routes only;
- inventory subtitles/captions when exposed;
- if possible, acquire only a short local audio segment around the dossier timestamp;
- hash/transcribe it locally;
- DELETE audio before artifact upload.

No cookies, passwords, account sessions, login bypasses, or private media URLs are used.
A completed diagnostic with ACCESS_HOLD is not media acquisition and does not promote ITEM_VERIFIED.
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

FBC_URL = "https://fbclindale.com/resources/sermons/titus-211-15/"
VIMEO_DIRECT = "https://vimeo.com/852173553"
VIMEO_PLAYER = "https://player.vimeo.com/video/852173553"
START = "00:32:30"
END = "00:36:30"
OUT = pathlib.Path(os.environ.get("G3_MEDIA_EVIDENCE_OUT", "g3-media-evidence"))
TMP = pathlib.Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "g3-titus-media"


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    try:
        p = subprocess.run(cmd, text=True, capture_output=True)
    except FileNotFoundError as exc:
        if check:
            raise
        return subprocess.CompletedProcess(cmd, 127, "", str(exc))
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


def safe_log(name: str, proc: subprocess.CompletedProcess[str]) -> None:
    (OUT / name).write_text(
        f"RETURN_CODE={proc.returncode}\n\nSTDOUT\n{proc.stdout}\n\nSTDERR\n{proc.stderr}",
        encoding="utf-8",
    )


def metadata_attempt(label: str, url: str, extra: list[str]) -> tuple[dict | None, subprocess.CompletedProcess[str]]:
    proc = run(["yt-dlp", "--dump-single-json", "--no-warnings", *extra, url], check=False)
    safe_log(f"metadata_attempt_{label}.txt", proc)
    if proc.returncode != 0:
        return None, proc
    try:
        data = json.loads(proc.stdout)
    except Exception:
        return None, proc
    return data, proc


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)

    receipt: dict[str, object] = {
        "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
        "official_fbc_page": FBC_URL,
        "vimeo_id": "852173553",
        "requested_segment": {"start": START, "end": END},
        "publication_authorized": False,
        "item_verified": False,
        "audio_binary_retained": False,
        "authentication_used": False,
    }

    versions = {}
    for name, cmd in {
        "yt_dlp": ["yt-dlp", "--version"],
        "ffmpeg": ["ffmpeg", "-version"],
        "ffprobe": ["ffprobe", "-version"],
    }.items():
        p = run(cmd, check=False)
        text = p.stdout or p.stderr
        versions[name] = text.splitlines()[0] if text else None
    receipt["tool_versions"] = versions

    candidates = [
        ("fbc_landing", FBC_URL, []),
        ("vimeo_player_with_fbc_referer", VIMEO_PLAYER, ["--referer", FBC_URL]),
        ("vimeo_direct_with_fbc_referer", VIMEO_DIRECT, ["--referer", FBC_URL]),
        ("vimeo_direct", VIMEO_DIRECT, []),
    ]

    selected: tuple[str, str, list[str], dict] | None = None
    attempts: list[dict[str, object]] = []
    for label, url, extra in candidates:
        metadata, proc = metadata_attempt(label, url, extra)
        attempts.append({
            "label": label,
            "url": url,
            "return_code": proc.returncode,
            "metadata_parsed": metadata is not None,
        })
        if metadata is not None and selected is None:
            selected = (label, url, extra, metadata)
    receipt["public_route_attempts"] = attempts

    if selected is None:
        receipt["acquisition_result"] = "ACCESS_HOLD"
        receipt["access_hold_reason"] = (
            "No unauthenticated public FBC/Vimeo route exposed yt-dlp media metadata. "
            "Direct Vimeo reported login-required in prior run; no credentials or cookies were supplied."
        )
        (OUT / "ACQUISITION_RECEIPT.json").write_text(
            json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        (OUT / "README.txt").write_text(
            "Diagnostic completed with ACCESS_HOLD. No original-media bytes were acquired.\n"
            "No cookies, credentials, or login bypasses were used. ITEM_VERIFIED remains false.\n",
            encoding="utf-8",
        )
        print(json.dumps(receipt, indent=2, ensure_ascii=False))
        return 0

    label, url, extra, metadata = selected
    receipt["selected_public_route"] = label
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
    (OUT / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    subs = run(["yt-dlp", "--list-subs", *extra, url], check=False)
    safe_log("subtitle_inventory.txt", subs)
    run([
        "yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs",
        "--sub-langs", "en.*,en", "--sub-format", "vtt/best", *extra,
        "-o", str(OUT / "captions.%(ext)s"), url
    ], check=False)

    template = str(TMP / "titus_segment.%(ext)s")
    dl = run([
        "yt-dlp", "--no-playlist", "-f", "bestaudio/best",
        "--download-sections", f"*{START}-{END}",
        "--force-keyframes-at-cuts", "-x", "--audio-format", "wav",
        *extra, "-o", template, url
    ], check=False)
    safe_log("yt_dlp_segment_log.txt", dl)
    if dl.returncode != 0:
        receipt["acquisition_result"] = "METADATA_ONLY_SEGMENT_HOLD"
        receipt["segment_return_code"] = dl.returncode
        (OUT / "ACQUISITION_RECEIPT.json").write_text(
            json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        (OUT / "README.txt").write_text(
            "Public metadata acquired, but the requested media segment was not. ITEM_VERIFIED remains false.\n",
            encoding="utf-8",
        )
        print(json.dumps(receipt, indent=2, ensure_ascii=False))
        return 0

    wavs = sorted(TMP.glob("titus_segment*.wav"))
    if not wavs:
        receipt["acquisition_result"] = "METADATA_ONLY_SEGMENT_HOLD"
        receipt["segment_note"] = "yt-dlp returned success but no WAV was produced"
        (OUT / "ACQUISITION_RECEIPT.json").write_text(
            json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(json.dumps(receipt, indent=2, ensure_ascii=False))
        return 0

    audio = wavs[0]
    probe = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration,size,bit_rate",
        "-of", "json", str(audio)
    ])
    receipt["segment"] = {
        "sha256": sha256(audio),
        "size_bytes": audio.stat().st_size,
        "ffprobe": json.loads(probe.stdout),
    }
    receipt["acquisition_result"] = "SEGMENT_ACQUIRED_EPHEMERALLY"

    whisper_cmd = shutil.which("whisper")
    if whisper_cmd:
        tr = run([
            whisper_cmd, str(audio), "--model", os.environ.get("WHISPER_MODEL", "base.en"),
            "--language", "en", "--task", "transcribe", "--fp16", "False",
            "--output_dir", str(OUT), "--output_format", "all", "--verbose", "False"
        ], check=False)
        safe_log("whisper_log.txt", tr)
        receipt["whisper_return_code"] = tr.returncode
        receipt["machine_transcript_only"] = True
    else:
        receipt["whisper_return_code"] = None
        receipt["machine_transcript_only"] = True
        receipt["whisper_note"] = "whisper CLI unavailable"

    audio.unlink(missing_ok=True)
    if TMP.exists():
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
