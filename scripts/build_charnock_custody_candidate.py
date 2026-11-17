#!/usr/bin/env python3
"""Create a versioned, research-only Charnock source-byte custody candidate.

This snapshots current bytes of the fifteen paths selected in historical
custody manifest v2. It NEVER proves upload, destination readback or rights.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

CONTRACT = "CHARNOCK-CUSTODY-V3"
ROOT = Path(__file__).resolve().parents[1]
BASELINE = "data/charnock-custody-manifest-v2.json"
HOLDS = ["PUBLICATION_HOLD", "ARCHIVE_HOLD", "RIGHTS_HOLD", "EVIDENCE_HOLD"]


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def safe_file(root: Path, relative: str) -> Path:
    parts = PurePosixPath(relative)
    if parts.is_absolute() or not relative or any(p in (".", "..") for p in parts.parts):
        raise ValueError(f"Unsafe Charnock custody path: {relative}")
    base = root.resolve()
    source = base.joinpath(*parts.parts)
    target = source.resolve()
    if source.is_symlink() or not target.is_relative_to(base) or not target.is_file():
        raise ValueError(f"Missing or unsafe Charnock file: {relative}")
    return target


def build(root: Path, baseline_path: str, output_dir: Path, git_sha: str) -> dict:
    if re.fullmatch(r"[0-9a-f]{40}", git_sha) is None:
        raise ValueError("Source revision must be a full 40-digit git commit SHA")
    previous = json.loads(safe_file(root, baseline_path).read_text(encoding="utf-8"))
    if previous.get("contractId") != "CHARNOCK-CUSTODY-V2":
        raise ValueError("Incorrect historical custody baseline")
    file_set = previous.get("fileManifest", {})
    if not isinstance(file_set, dict) or len(file_set) != 15:
        raise ValueError("Expected exactly fifteen Charnock research source paths")
    contents: dict[str, bytes] = {}
    metadata: dict[str, dict] = {}
    for path in sorted(file_set):
        raw = safe_file(root, path).read_bytes()
        contents[path] = raw
        metadata[path] = {
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "gitBlobSha1": hashlib.sha1(
                b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw
            ).hexdigest(),
        }
    manifest = {
        "schemaVersion": 3,
        "contractId": CONTRACT,
        "authorityRole": "corpus-specific-supporting-only",
        "sourceGitSha": git_sha,
        "sourceSelection": baseline_path,
        "snapshotState": "BYTE_SNAPSHOT_CREATED",
        "custodyState": "PENDING_INDEPENDENT_DRIVE_SHA256_READBACK",
        "publicationState": "BLOCKED",
        "rightsState": "PRIVATE_STUDY_ONLY",
        "holds": HOLDS,
        "independentDestinationReceipt": None,
        "previousReceipt": "data/charnock-handoff-receipt-v1.json",
        "previousSnapshot": baseline_path,
        "fileManifest": metadata,
        "fileCount": len(metadata),
        "totalBytes": sum(value["bytes"] for value in metadata.values()),
        "verificationBoundary": "Local source-byte hashes, not remote destination or publication approval",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    basename = f"charnock-custody-v3-{git_sha[:12]}"
    archive = output_dir / f"{basename}.zip"
    with ZipFile(archive, "w") as store:
        for filename, raw in [("manifest.json", canonical_bytes(manifest))] + [
            (f"files/{path}", contents[path]) for path in sorted(contents)
        ]:
            info = ZipInfo(filename, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = (0o100644 & 0xFFFF) << 16
            store.writestr(info, raw, compress_type=ZIP_DEFLATED, compresslevel=9)
    packet = archive.read_bytes()
    report = {
        "schemaVersion": 1,
        "contractId": CONTRACT,
        "sourceGitSha": git_sha,
        "archiveName": archive.name,
        "archiveBytes": len(packet),
        "archiveSha256": hashlib.sha256(packet).hexdigest(),
        "manifestSha256": hashlib.sha256(canonical_bytes(manifest)).hexdigest(),
        "sourceFiles": len(metadata),
        "sourceBytes": manifest["totalBytes"],
        "destinationState": "NOT_UPLOADED_OR_VERIFIED",
        "publicationState": "BLOCKED",
        "receipt": None,
    }
    (output_dir / f"{basename}.json").write_bytes(canonical_bytes(report))
    with ZipFile(archive) as store:
        if json.loads(store.read("manifest.json")) != manifest:
            raise ValueError("Archive manifest mismatch")
        for path, raw in contents.items():
            if store.read(f"files/{path}") != raw:
                raise ValueError(f"Archive source mismatch: {path}")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--baseline", default=BASELINE)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--git-sha", required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.root, args.baseline, args.out_dir, args.git_sha), indent=2))


if __name__ == "__main__":
    main()
