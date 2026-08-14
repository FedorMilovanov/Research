#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
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

DECODED_BUNDLE_NAME = "handoff-release.tar.xz"
CHUNK_PREFIX = DECODED_BUNDLE_NAME + ".part-"
CHUNK_SUFFIX = ".b64"
CHUNK_SIZE_CHARS = 12000
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


def encode_segments(bundle: bytes) -> dict[str, bytes]:
    encoded = base64.b64encode(bundle).decode("ascii")
    chunks = [
        encoded[offset : offset + CHUNK_SIZE_CHARS]
        for offset in range(0, len(encoded), CHUNK_SIZE_CHARS)
    ]
    return {
        f"{CHUNK_PREFIX}{index:03d}{CHUNK_SUFFIX}": (chunk + "\n").encode("ascii")
        for index, chunk in enumerate(chunks, start=1)
    }


def decode_segments(segment_files: dict[str, bytes]) -> bytes:
    names = sorted(segment_files)
    if not names:
        raise build.ReleaseError("immutable bundle has no base64 segments")
    joined = "".join(segment_files[name].decode("ascii").strip() for name in names)
    try:
        return base64.b64decode(joined, validate=True)
    except Exception as exc:
        raise build.ReleaseError(f"invalid immutable bundle base64 segments: {exc}") from exc


def compact_release(files: dict[str, bytes]) -> tuple[dict[str, bytes], bytes, bytes, bytes]:
    bundle_a = deterministic_bundle(files)
    bundle_b = deterministic_bundle(files)
    if bundle_a != bundle_b:
        raise build.ReleaseError("deterministic bundle bytes differ across identical builds")
    if bundle_members(bundle_a) != files:
        raise build.ReleaseError("deterministic bundle round-trip changed release members")

    segments = encode_segments(bundle_a)
    if decode_segments(segments) != bundle_a:
        raise build.ReleaseError("base64 segmented storage round-trip changed decoded bundle")

    bundle_sha = sha256_bytes(bundle_a)
    manifest = json.loads(files[MANIFEST_NAME].decode("utf-8"))
    chunk_records = [
        {
            "name": name,
            "sha256": sha256_bytes(payload),
            "bytes": len(payload),
            "base64_chars": len(payload.decode("ascii").strip()),
        }
        for name, payload in sorted(segments.items())
    ]
    index = {
        "schema_version": build.SCHEMA_VERSION,
        "release_format_version": build.RELEASE_FORMAT_VERSION,
        "immutable": True,
        "research_authority_sha": build.AUTHORITY_SHA,
        "authority_digest_sha256": build.EXPECTED_AUTHORITY_DIGEST,
        "whole_authority_sha256": build.EXPECTED_AUTHORITY_DIGEST,
        "release_payload_sha256": manifest["release_payload_sha256"],
        "storage_encoding": "ordered-base64-segments",
        "decoded_bundle_name": DECODED_BUNDLE_NAME,
        "decoded_bundle_sha256": bundle_sha,
        "decoded_bundle_format": "tar+xz; sorted USTAR members; uid=gid=0; mtime=0; XZ preset=9",
        "segment_size_chars": CHUNK_SIZE_CHARS,
        "segment_count": len(segments),
        "segments": chunk_records,
        "member_count": len(files),
        "members": sorted(files),
        "expanded_member_sha256": {
            name: sha256_bytes(payload) for name, payload in sorted(files.items())
        },
        "deterministic_bundle_two_run_byte_equivalent": True,
        "segment_round_trip_verified": True,
        "reconstruction": "Sort segment names, strip one trailing newline from each, concatenate ASCII base64, decode base64 to handoff-release.tar.xz, verify decoded_bundle_sha256, then extract tar.xz.",
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
        "bundle_index_path": f"releases/{build.EXPECTED_AUTHORITY_DIGEST}/{INDEX_NAME}",
        "storage_encoding": "ordered-base64-segments",
        "decoded_bundle_sha256": bundle_sha,
        "ranking_disposition_w3q_123": "NO_PRODUCT_RANKING_ADMISSION",
    }
    pointer_bytes = canonical_bytes(pointer)
    return segments, files[MANIFEST_NAME], index_bytes, pointer_bytes


def write_compact(output_root: Path, compact: tuple[dict[str, bytes], bytes, bytes, bytes]) -> Path:
    segments, manifest, index, pointer = compact
    release_dir = output_root / "releases" / build.EXPECTED_AUTHORITY_DIGEST
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in sorted(segments.items()):
        (release_dir / name).write_bytes(payload)
    (release_dir / MANIFEST_NAME).write_bytes(manifest)
    (release_dir / INDEX_NAME).write_bytes(index)
    (output_root / "CURRENT_RELEASE.json").write_bytes(pointer)
    return release_dir


def verify_committed(verify_root: Path, compact: tuple[dict[str, bytes], bytes, bytes, bytes]) -> None:
    segments, manifest, index, pointer = compact
    release_dir = verify_root / "releases" / build.EXPECTED_AUTHORITY_DIGEST
    expected_names = set(segments) | {MANIFEST_NAME, INDEX_NAME}
    actual_names = {p.name for p in release_dir.iterdir() if p.is_file()}
    if actual_names != expected_names:
        raise build.ReleaseError(
            f"committed segmented release file set drift: expected {sorted(expected_names)}, got {sorted(actual_names)}"
        )
    expected = {
        **{release_dir / name: payload for name, payload in segments.items()},
        release_dir / MANIFEST_NAME: manifest,
        release_dir / INDEX_NAME: index,
        verify_root / "CURRENT_RELEASE.json": pointer,
    }
    for path, payload in expected.items():
        if path.read_bytes() != payload:
            raise build.ReleaseError(f"committed segmented release byte drift: {path}")

    committed_segments = {
        name: (release_dir / name).read_bytes() for name in sorted(segments)
    }
    committed_bundle = decode_segments(committed_segments)
    generated_bundle = deterministic_bundle(build.build_release_files())
    if committed_bundle != generated_bundle:
        raise build.ReleaseError("committed segmented bundle differs from freshly derived authority bundle")
    if bundle_members(committed_bundle) != build.build_release_files():
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
        "status": "IMMUTABLE_SEGMENTED_HANDOFF_RELEASE_VALID",
        "research_authority_sha": build.AUTHORITY_SHA,
        "authority_digest_sha256": build.EXPECTED_AUTHORITY_DIGEST,
        "decoded_bundle_sha256": index["decoded_bundle_sha256"],
        "segment_count": index["segment_count"],
        "bundle_member_count": index["member_count"],
        "verified_committed_release": bool(args.verify_root),
        "w3q_123_disposition": "NO_PRODUCT_RANKING_ADMISSION",
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (build.ReleaseError, core.AuditError, AssertionError, OSError, ValueError, lzma.LZMAError, tarfile.TarError) as exc:
        print(f"IMMUTABLE_SEGMENTED_HANDOFF_RELEASE_FAIL: {exc}", file=sys.stderr)
        sys.exit(2)
