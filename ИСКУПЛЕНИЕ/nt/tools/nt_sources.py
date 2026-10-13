#!/usr/bin/env python3
"""Pinned NT witness acquisition and byte verification; data never enter Git.

nt/data/nt-corpus-v1.json is the only source of repository/commit/digest pins.
A dataset digest concatenates all regular files sorted by UTF-8 relative path
(the existing LC_ALL=C contract), without separators. Validators only read.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
sys.dont_write_bytecode = True
import tarfile
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / "ИСКУПЛЕНИЕ/nt/data/nt-corpus-v1.json"
DIRS = {"S1": "pysblgnt/sblgnt", "S2": "textonly", "S3": "textonly",
        "S4": "textonly", "S5": "data", "S6": "tf/2021", "S7": "xml",
        "S8": "verse-per-line", "S9": "xml", "S10": "xml"}
OVERRIDES = {"S1": "NT_SBLGNT_DIR", "S5": "NT_LXX_DIR", "S6": "NT_MT_DIR"}


def registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def witnesses() -> dict[str, dict]:
    rows = registry()["textWitnesses"]
    result = {row["id"]: row for row in rows}
    if len(result) != len(rows) or set(result) != set(DIRS):
        raise ValueError("NT registry must contain exactly S1–S10, without duplicates")
    for sid, row in result.items():
        if not re.fullmatch(r"[\w.-]+/[\w.-]+", row.get("repository", "")):
            raise ValueError(f"{sid}: invalid repository")
        if not re.fullmatch(r"[0-9a-f]{40}", row.get("commit", "")):
            raise ValueError(f"{sid}: invalid commit pin")
        if not re.fullmatch(r"[0-9a-f]{64}", digest_pin(row)):
            raise ValueError(f"{sid}: invalid dataset digest")
        if row.get("textDir", DIRS[sid]) != DIRS[sid]:
            raise ValueError(f"{sid}: dataset directory contract drift")
    return result


def digest_pin(row: dict) -> str:
    return row.get("sha256OfDataset", row.get("sha256OfSet", ""))


def corpus_home() -> Path:
    home = Path(os.environ.get("NT_CORPUS_HOME", str(Path.home() / "nt-corpus"))).resolve()
    if home == ROOT or ROOT in home.parents:
        raise ValueError("NT_CORPUS_HOME must be outside the Research checkout")
    return home


def dataset_stats(path: Path) -> tuple[str, int, int]:
    if not path.is_dir():
        raise ValueError(f"dataset directory missing: {path}")
    entries = list(path.rglob("*"))
    if any(p.is_symlink() or "\n" in p.name or "\r" in p.name or not (p.is_dir() or p.is_file()) for p in entries):
        raise ValueError(f"symlink or special file inside dataset: {path}")
    files = sorted((p for p in entries if p.is_file()),
                   key=lambda p: p.relative_to(path).as_posix().encode("utf-8"))
    if not files:
        raise ValueError(f"empty dataset: {path}")
    digest = hashlib.sha256()
    size = 0
    for p in files:
        with p.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
                size += len(chunk)
    return digest.hexdigest(), len(files), size


def verify_dataset(sid: str, row: dict, path: Path) -> tuple[str, int, int]:
    actual = dataset_stats(path)
    if actual[0] != digest_pin(row):
        raise ValueError(f"{sid}: sha256 mismatch: {actual[0]} != {digest_pin(row)}")
    if "files" in row and actual[1] != row["files"]:
        raise ValueError(f"{sid}: file count {actual[1]} != {row['files']}")
    if "bytes" in row and actual[2] != row["bytes"]:
        raise ValueError(f"{sid}: byte count {actual[2]} != {row['bytes']}")
    if row.get("sha256OfSortedRelativePaths") != path_digest(path):
        raise ValueError(f"{sid}: relative filename inventory mismatch")
    return actual


def path_digest(path: Path) -> str:
    names = sorted(p.relative_to(path).as_posix().encode("utf-8")
                   for p in path.rglob("*") if p.is_file())
    return hashlib.sha256(b"\n".join(names)).hexdigest()


def safe_extract(tar: tarfile.TarFile, stage: Path) -> None:
    """Regular files/directories only; safe also on Python 3.11.2.

    Do not depend on the extractall(filter=...) backport. Never extract
    links, devices, absolute/traversing names or overwrite duplicate paths.
    """
    targets = set()
    for member in tar.getmembers():
        target = (stage / member.name).resolve()
        if (stage not in target.parents or target in targets or
                not (member.isfile() or member.isdir()) or
                ".." in Path(member.name).parts or Path(member.name).is_absolute()):
            raise ValueError(f"unsafe archive member: {member.name}")
        targets.add(target)
        if member.isdir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            source = tar.extractfile(member)
            if source is None:
                raise ValueError(f"archive file has no body: {member.name}")
            with source, target.open("xb") as out:
                shutil.copyfileobj(source, out)


def witness_dir(sid: str, *, verify: bool = True) -> Path:
    row = witnesses()[sid]
    override = os.environ.get(OVERRIDES.get(sid, ""), "").strip()
    path = (Path(override) if override else corpus_home() /
            f"{row['repository'].split('/')[1]}-{row['commit']}" / DIRS[sid])
    if verify:
        verify_dataset(sid, row, path)
    return path


def witness_file(sid: str, name: str, override: str = "") -> Path:
    path = Path(os.environ[override]) if override and os.environ.get(override) else witness_dir(sid) / name
    # An override must still refer to bytes from the verified pinned dataset.
    base = witness_dir(sid)
    canonical = base / name
    if not path.is_file() or not canonical.is_file() or path.read_bytes() != canonical.read_bytes():
        raise ValueError(f"{sid}: file override does not match pinned {name}")
    return path


def fetch_witness(sid: str, row: dict, home: Path) -> Path:
    home = home.resolve()
    if home == ROOT or ROOT in home.parents:
        raise ValueError("witness acquisition must stay outside the Research checkout")
    name = f"{row['repository'].split('/')[1]}-{row['commit']}"
    dest = home / name
    if dest.exists():
        return dest / DIRS[sid]
    home.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="nt-download-", dir=home) as tmp:
        stage = Path(tmp)
        archive = stage / "source.tar.gz"
        url = f"https://codeload.github.com/{row['repository']}/tar.gz/{row['commit']}"
        request = urllib.request.Request(url, headers={"User-Agent": "Research-NT-pinned-fetch"})
        with urllib.request.urlopen(request, timeout=90) as response, archive.open("wb") as out:
            for chunk in iter(lambda: response.read(1024 * 1024), b""):
                out.write(chunk)
        with tarfile.open(archive, "r:gz") as tar:
            safe_extract(tar, stage)
        source = stage / name
        verify_dataset(sid, row, source / DIRS[sid])
        source.rename(dest)
    return dest / DIRS[sid]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="acquire missing witnesses outside Git")
    args = parser.parse_args()
    failures = []
    for sid, row in witnesses().items():
        try:
            path = fetch_witness(sid, row, corpus_home()) if args.fetch else witness_dir(sid, verify=False)
            digest, count, size = verify_dataset(sid, row, path)
            print(f"{sid}: sha256 OK {digest} ({count} files, {size} bytes)")
        except (OSError, ValueError, tarfile.TarError) as exc:
            failures.append(f"{sid}: {exc}")
            print(f"FAIL {failures[-1]}", file=sys.stderr)
    if failures:
        return 1
    print("PASS: 10/10 pinned witness datasets verified; no publication approval")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, ValueError, tarfile.TarError) as exc:
        print(f"NT sources: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
