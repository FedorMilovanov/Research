"""Package the bounded Charnock corpus into the handoff archive.

Run this instead of assembling the zip by hand: the member list comes from a base
receipt, every member is re-hashed from disk (repository files) or from a local
fetch of the eleven EEBO-TCP objects, and the archive is written deterministically
(sorted members, fixed timestamps, fixed compression), so the same inputs always
produce the same SHA-256.

    python3 scripts/build_charnock_packet.py \
        --base-receipt data/charnock-handoff-receipt-v2.json \
        --xml-dir /tmp/wave41xml \
        --name CHARNOCK_FULL_BOUNDED_RESEARCH_wave42_2026-11-16.zip \
        --zip-out /tmp/wave42.zip \
        --manifest-out data/charnock-wave42-packet-manifest.json

Layout inside the archive: `manifest.json` at the root, then every member under
its repository-relative path (`xml/<id>.xml` for the TCP objects).

The script refuses to run when a member has drifted from the base receipt: a
packet must never be built from a tree that disagrees with the receipt it extends.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_MEMBER = "manifest.json"
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
PACKET_MANIFEST_ENCODING = "json.dumps(..., ensure_ascii=False, sort_keys=True, indent=2) + \\n, UTF-8"


def canonical_manifest_bytes(manifest: dict) -> bytes:
    return (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def member_pins(files: dict, xml_dir: Path | None) -> tuple[dict, list[str]]:
    """Re-read every member; return its pins plus the ones that moved since the base."""
    pins = {}
    drifted = []
    for path in sorted(files):
        pin = files[path]
        if path.startswith("xml/"):
            if xml_dir is None:
                raise ValueError(f"xml directory required for member {path}")
            source = Path(xml_dir) / Path(path).name
        else:
            source = ROOT / path
        if not source.is_file():
            raise ValueError(f"packet member is missing: {path} (looked at {source})")
        raw = source.read_bytes()
        current = {"bytes": len(raw), "sha256": sha256(raw)}
        if current != {"bytes": pin["bytes"], "sha256": pin["sha256"]}:
            drifted.append(path)
        pins[path] = current
    return pins, drifted


def changed_members(base_files: dict, pins: dict) -> list[str]:
    return [path for path in sorted(base_files) if base_files[path] != pins[path]]


def manifest_with(base_manifest: dict, pins: dict) -> dict:
    manifest = dict(base_manifest)
    manifest["files"] = pins
    return manifest


def write_zip(members: dict[str, bytes], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(members):
            info = zipfile.ZipInfo(name, date_time=FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, members[name])


def collect_members(pins: dict, manifest_bytes: bytes, xml_dir: Path | None) -> dict[str, bytes]:
    members = {MANIFEST_MEMBER: manifest_bytes}
    for path in sorted(pins):
        source = (Path(xml_dir) / Path(path).name) if path.startswith("xml/") else (ROOT / path)
        members[path] = source.read_bytes()
    return members


def build(base_receipt: str, name: str, zip_out: Path, manifest_out: Path | None,
          xml_dir: Path | None, allow_drift: bool = False) -> dict:
    receipt = json.loads((ROOT / base_receipt).read_text(encoding="utf-8"))
    base_files = receipt["sourceManifest"]["files"]
    pins, drifted = member_pins(base_files, xml_dir)
    changed = changed_members(base_files, pins)
    if drifted != changed:  # defensive: both views must agree
        raise ValueError(f"inconsistent drift accounting: {drifted} vs {changed}")
    if changed and not allow_drift:
        raise ValueError(
            "tree no longer matches the base receipt; pass --allow-drift to package "
            f"the declared changes: {', '.join(changed)}"
        )
    manifest = manifest_with(receipt["sourceManifest"], pins)
    manifest_bytes = canonical_manifest_bytes(manifest)
    if manifest_out is not None:
        manifest_out.parent.mkdir(parents=True, exist_ok=True)
        manifest_out.write_bytes(manifest_bytes)

    members = collect_members(pins, manifest_bytes, xml_dir)
    write_zip(members, zip_out)
    archive = zip_out.read_bytes()
    return {
        "state": "PACKET_BUILT",
        "name": name,
        "zipPath": str(zip_out),
        "zipBytes": len(archive),
        "zipSha256": sha256(archive),
        "manifestPath": str(manifest_out) if manifest_out else None,
        "manifestSha256": sha256(manifest_bytes),
        "manifestEncoding": PACKET_MANIFEST_ENCODING,
        "members": len(members),
        "repoMembers": sum(1 for path in pins if not path.startswith("xml/")),
        "xmlMembers": sum(1 for path in pins if path.startswith("xml/")),
        "changedSinceBaseReceipt": changed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-receipt", default="data/charnock-handoff-receipt-v2.json")
    parser.add_argument("--name", required=True, help="archive file name recorded in the receipt")
    parser.add_argument("--zip-out", required=True)
    parser.add_argument("--manifest-out", default=None)
    parser.add_argument("--xml-dir", default=None)
    parser.add_argument("--allow-drift", action="store_true",
                        help="package members that differ from the base receipt (declared wave edit)")
    args = parser.parse_args()
    report = build(
        args.base_receipt,
        args.name,
        Path(args.zip_out),
        Path(args.manifest_out) if args.manifest_out else None,
        Path(args.xml_dir) if args.xml_dir else None,
        allow_drift=args.allow_drift,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
