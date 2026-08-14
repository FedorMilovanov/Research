#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import json
import lzma
import shutil
import sys
import tarfile
from pathlib import Path

import build_product_handoff_release as build
import validate_product_handoff as core

BUNDLE_NAME = "handoff-release.tar.xz"
INDEX_NAME = "bundle-index.json"
MANIFEST_NAME = "release-manifest.json"


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def deterministic_bundle(files: dict[str, bytes]) -> bytes:
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.USTAR_FORMAT) as tar:
        for name in sorted(files):
            payload = files[name]
            info = tarfile.TarInfo(name=name)
            info.size = len(payload)
            info.mode = 0o644
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            info.mtime = 0
            tar.addfile(info, io.BytesIO(payload))
    return lzma.compress(raw.getvalue(), format=lzma.FORMAT_XZ, preset=9)


def bundle_members(payload: bytes) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:xz") as tar:
        for member in tar.getmembers():
            if not member.isfile():
                raise build.ReleaseError(f"non-file member in immutable bundle: {member.name}")
            extracted = tar.extractfile(member)
            if extracted is None:
                raise build.ReleaseError(f"cannot read immutable bundle member: {member.name}")
            result[member.name] = extracted.read()
    return result


def compact_release(files: dict[str, bytes]) -> tuple[bytes, bytes, bytes, bytes]:
    bundle_a = deterministic_bundle(files)
    bundle_b = deterministic_bundle(files)
    if bundle_a != bundle_b:
        raise build.ReleaseError("deterministic bundle bytes differ across identical builds")
    if bundle_members(bundle_a) != files:
        raise build.ReleaseError("deterministic bundle round-trip changed release members")

    bundle_sha = sha256_bytes(bundle_a)
    manifest = json.loads(files[MANIFEST_NAME].decode("utf-8"))
    index = {
        "schema_version": build.SCHEMA_VERSION,
        "release_format_version": build.RELEASE_FORMAT_VERSION,
        "immutable": True,
        "research_authority_sha": build.AUTHORITY_SHA,
        "authority_digest_sha256": build.EXPECTED_AUTHORITY_DIGEST,
        "whole_authority_sha256": build.EXPECTED_AUTHORITY_DIGEST,
        "release_payload_sha256": manifest["release_payload_sha256"],
        "bundle_name": BUNDLE_NAME,
        "bundle_sha256": bundle_sha,
        "bundle_format": "tar+xz; sorted USTAR members; uid=gid=0; mtime=0; XZ preset=9",
        "member_count": len(files),
        "members": sorted(files),
        "expanded_member_sha256": {
            name: sha256_bytes(payload) for name, payload in sorted(files.items())
        },
        "deterministic_bundle_two_run_byte_equivalent": True,
        "release_path": f"1_PETER_BOT/product_handoff/releases/{build.EXPECTED_AUTHORITY_DIGEST}",
    }
    index_bytes = canonical_bytes(index)
    pointer = {
        "schema_version": build.SCHEMA_VERSION,
        "release_format_version": build.RELEASE_FORMAT_VERSION,
        "immutable_release": True,
        "research_authority_sha": build.AUTHORITY_SHA,
        "authority_digest_sha256": build.EXPECTED_AUTHORITY_DIGEST,
        "whole_authority_sha256": build.EXPECTED_AUTHORITY_DIGEST,
        "release_path": f"releases/{build.EXPECTED_AUTHORITY_DIGEST}",
        "bundle_path": f"releases/{build.EXPECTED_AUTHORITY_DIGEST}/{BUNDLE_NAME}",
        "bundle_sha256": bundle_sha,
        "bundle_index_path": f"releases/{build.EXPECTED_AUTHORITY_DIGEST}/{INDEX_NAME}",
        "ranking_disposition_w3q_123": "NO_PRODUCT_RANKING_ADMISSION",
    }
    pointer_bytes = canonical_bytes(pointer)
    return bundle_a, files[MANIFEST_NAME], index_bytes, pointer_bytes


def write_compact(output_root: Path, compact: tuple[bytes, bytes, bytes, bytes]) -> Path:
    bundle, manifest, index, pointer = compact
    release_dir = output_root / "releases" / build.EXPECTED_AUTHORITY_DIGEST
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True, exist_ok=True)
    (release_dir / BUNDLE_NAME).write_bytes(bundle)
    (release_dir / MANIFEST_NAME).write_bytes(manifest)
    (release_dir / INDEX_NAME).write_bytes(index)
    (output_root / "CURRENT_RELEASE.json").write_bytes(pointer)
    return release_dir


def verify_committed(verify_root: Path, compact: tuple[bytes, bytes, bytes, bytes]) -> None:
    bundle, manifest, index, pointer = compact
    release_dir = verify_root / "releases" / build.EXPECTED_AUTHORITY_DIGEST
    expected_names = {BUNDLE_NAME, MANIFEST_NAME, INDEX_NAME}
    actual_names = {p.name for p in release_dir.iterdir() if p.is_file()}
    if actual_names != expected_names:
        raise build.ReleaseError(
            f"committed compact release file set drift: expected {sorted(expected_names)}, got {sorted(actual_names)}"
        )
    expected = {
        release_dir / BUNDLE_NAME: bundle,
        release_dir / MANIFEST_NAME: manifest,
        release_dir / INDEX_NAME: index,
        verify_root / "CURRENT_RELEASE.json": pointer,
    }
    for path, payload in expected.items():
        if path.read_bytes() != payload:
            raise build.ReleaseError(f"committed compact release byte drift: {path}")

    committed_members = bundle_members((release_dir / BUNDLE_NAME).read_bytes())
    generated_files = build.build_release_files()
    if committed_members != generated_files:
        raise build.ReleaseError("committed bundle members differ from freshly derived authority release")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--verify-root")
    args = parser.parse_args()

    files = build.build_release_files()
    compact = compact_release(files)
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    release_dir = write_compact(output_root, compact)
    if args.verify_root:
        verify_committed(Path(args.verify_root), compact)

    index = json.loads((release_dir / INDEX_NAME).read_text(encoding="utf-8"))
    print(json.dumps({
        "status": "IMMUTABLE_COMPACT_HANDOFF_RELEASE_VALID",
        "research_authority_sha": build.AUTHORITY_SHA,
        "authority_digest_sha256": build.EXPECTED_AUTHORITY_DIGEST,
        "bundle_sha256": index["bundle_sha256"],
        "bundle_member_count": index["member_count"],
        "verified_committed_release": bool(args.verify_root),
        "w3q_123_disposition": "NO_PRODUCT_RANKING_ADMISSION",
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (build.ReleaseError, core.AuditError, AssertionError, OSError, ValueError, lzma.LZMAError, tarfile.TarError) as exc:
        print(f"IMMUTABLE_COMPACT_HANDOFF_RELEASE_FAIL: {exc}", file=sys.stderr)
        sys.exit(2)
