"""Regenerate the Charnock custody manifest from the handoff receipt.

The custody manifest must never be hand-edited: `manifestSha256` is derived from
the member map, and every member is re-hashed from disk before it is listed. If a
member no longer matches the receipt pins, the build fails instead of publishing a
manifest that quietly disagrees with the packet.

Usage:
    python3 scripts/build_charnock_custody_manifest.py            # write v3 manifest
    python3 scripts/build_charnock_custody_manifest.py --check    # verify, write nothing

Outputs (both deterministic, no clock reads):
    data/charnock-wave43-packet-manifest.json   -- byte-exact packet manifest
    data/charnock-custody-manifest-v5.json      -- custody manifest derived from it
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = "data/charnock-handoff-receipt-v4.json"
PACKET_MANIFEST_OUT = "data/charnock-wave43-packet-manifest.json"
CUSTODY_OUT = "data/charnock-custody-manifest-v5.json"

# The packet manifest is serialised exactly as the builder wrote it into the zip:
# sorted keys, indent 2, UTF-8, one trailing newline. sourceManifestSha256 pins
# these bytes, so the encoding is part of the contract, not a detail.
PACKET_MANIFEST_ENCODING = "json.dumps(..., ensure_ascii=False, sort_keys=True, indent=2) + \\n, UTF-8"
CUSTODY_SHA_METHOD = ("sha256 of the members-only fileManifest map serialised as "
                      + PACKET_MANIFEST_ENCODING
                      + "; the packet manifest itself (with counts/scope/holds) is pinned separately as sourceManifestSha256")


def _load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def packet_manifest_bytes(manifest: dict) -> bytes:
    """Serialise the packet manifest so its SHA-256 equals the receipt pin."""
    return (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def verified_members(files: dict, xml_dir: str | None = None) -> dict:
    """Re-hash every packet member on disk and refuse to publish any drift.

    Repository members are always re-hashed from the checkout. The eleven
    EEBO-TCP XML objects are not kept in the repository: they are re-hashed only
    when --xml-dir points at a local fetch, otherwise the entry carries the
    receipt pin and is labelled as such instead of pretending to be re-read.
    """
    out = {}
    for path in sorted(files):
        pin = files[path]
        target = ROOT / path
        if path.startswith("xml/") and not target.is_file():
            local = Path(xml_dir) / Path(path).name if xml_dir else None
            if local is not None and local.is_file():
                target = local
            else:
                out[path] = {
                    "bytes": pin["bytes"],
                    "sha256": pin["sha256"],
                    "verifiedFrom": "receipt-pin (object not present in checkout)",
                }
                continue
        if not target.is_file():
            raise ValueError(f"packet member is missing: {path}")
        raw = target.read_bytes()
        got = {"bytes": len(raw), "sha256": _sha(raw)}
        if got != {"bytes": pin["bytes"], "sha256": pin["sha256"]}:
            raise ValueError(
                f"packet member drifted from its receipt pin: {path} "
                f"(disk {got['bytes']}B/{got['sha256'][:12]}, pin {pin['bytes']}B/{pin['sha256'][:12]})"
            )
        # Provenance label is deliberately input-independent so the committed
        # manifest is byte-stable; --xml-dir only gates the check, it never
        # changes what is written.
        out[path] = dict(got, verifiedFrom=("receipt-pin (object not present in checkout)"
                                            if path.startswith("xml/") else "repo"))
    return out


def rehashed_xml_count(files: dict, xml_dir: str | None) -> int:
    """Replay the eleven TCP XML objects against their pins when they are local."""
    if not xml_dir:
        return 0
    count = 0
    for path, pin in files.items():
        if not path.startswith("xml/"):
            continue
        local = Path(xml_dir) / Path(path).name
        if not local.is_file():
            continue
        raw = local.read_bytes()
        if len(raw) != pin["bytes"] or _sha(raw) != pin["sha256"]:
            raise ValueError(f"XML object drifted from its registry pin: {path}")
        count += 1
    return count


def build(receipt_path: str = RECEIPT, xml_dir: str | None = None) -> tuple[dict, bytes]:
    receipt = _load(receipt_path)
    manifest = receipt["sourceManifest"]
    members = verified_members(manifest["files"], xml_dir)

    raw_manifest = packet_manifest_bytes(manifest)
    manifest_sha = _sha(raw_manifest)
    if manifest_sha != receipt["sourceManifestSha256"]:
        raise ValueError(
            "the receipt's sourceManifest does not reproduce its own sourceManifestSha256 "
            f"({manifest_sha} != {receipt['sourceManifestSha256']})"
        )

    # The custody manifest pins the member map alone; the packet manifest also
    # carries counts, scope and holds, so the two SHA-256 values are deliberately
    # different objects. Both are recorded so a reader cannot confuse them.
    pin_map = {path: {"bytes": item["bytes"], "sha256": item["sha256"]} for path, item in members.items()}
    if pin_map != manifest["files"]:
        raise ValueError("fileManifest map and packet manifest disagree on member hashes")
    custody_sha = _sha(packet_manifest_bytes(pin_map))

    custody = {
        "schemaVersion": 2,
        "contractId": "CHARNOCK-CUSTODY-V3",
        "createdAtUtc": receipt["verifiedAtUtc"],
        "createdBy": receipt["verifiedBy"],
        "authorityRole": "corpus-specific-supporting-only",
        "scope": receipt["scope"],
        "custodyState": receipt["custodyState"],
        "researchCompletion": receipt["researchCompletion"],
        "evidenceClass": receipt["evidenceClass"],
        "evidenceClassBoundary": receipt["evidenceClassBoundary"],
        "accessState": receipt["accessState"],
        "locatorState": receipt["locatorState"],
        "rightsState": receipt["rightsState"],
        "publicationState": receipt["publicationState"],
        "holds": list(receipt["holds"]),
        "derivedFrom": {
            "receipt": receipt_path,
            "receiptSha256": _sha((ROOT / receipt_path).read_bytes()),
            "sourceArtifactName": receipt["sourceArtifactName"],
            "sourceArchiveBytes": receipt["sourceArchiveBytes"],
            "sourceArchiveSha256": receipt["sourceArchiveSha256"],
            "sourceManifestPath": PACKET_MANIFEST_OUT,
            "sourceManifestSha256": manifest_sha,
        },
        "fileManifest": members,
        "fileCount": len(members),
        "totalBytes": sum(item["bytes"] for item in members.values()),
        "manifestSha256": custody_sha,
        "manifestSha256Method": CUSTODY_SHA_METHOD,
        "destinationProvider": receipt["destinationProvider"],
        "destinationObjectId": receipt["destinationObjectId"],
        "destinationPath": receipt["destinationPath"],
        "destinationParentIds": list(receipt["destinationParentIds"]),
        "destinationBytes": receipt["destinationBytes"],
        "destinationSha256Readback": receipt["destinationSha256Readback"],
        "verifiedAtUtc": receipt["verifiedAtUtc"],
        "verifiedBy": receipt["verifiedBy"],
        "verificationMethod": receipt["verificationMethod"],
        "verificationBoundary": receipt["verificationBoundary"],
        "supersedes": "data/charnock-custody-manifest-v4.json",
        "nextAction": (
            "Do not edit by hand. After any packet rebuild rerun "
            "python3 scripts/build_charnock_custody_manifest.py --receipt <new receipt> "
            "so the member map, totalBytes and manifestSha256 are recomputed."
        ),
        "regenerateWith": "python3 scripts/build_charnock_custody_manifest.py",
    }
    return custody, raw_manifest


def check(receipt_path: str = RECEIPT, xml_dir: str | None = None) -> dict:
    """Rebuild in memory and compare with what is committed on disk."""
    custody, raw_manifest = build(receipt_path, xml_dir)
    stored_packet = (ROOT / PACKET_MANIFEST_OUT).read_bytes()
    stored_custody = _load(CUSTODY_OUT)
    problems = []
    if stored_packet != raw_manifest:
        problems.append(f"{PACKET_MANIFEST_OUT} differs byte for byte from the regenerated manifest")
    if stored_custody != custody:
        problems.append(f"{CUSTODY_OUT} differs from the regenerated custody manifest")
    if stored_custody.get("manifestSha256") != custody["manifestSha256"]:
        problems.append("manifestSha256 in the committed custody manifest is stale")
    if problems:
        raise ValueError("; ".join(problems))
    return {
        "state": "CUSTODY_MANIFEST_REPRODUCIBLE",
        "fileCount": custody["fileCount"],
        "totalBytes": custody["totalBytes"],
        "manifestSha256": custody["manifestSha256"],
        "sourceArchiveSha256": custody["derivedFrom"]["sourceArchiveSha256"],
        "destinationObjectId": custody["destinationObjectId"],
        "destinationSha256Readback": custody["destinationSha256Readback"],
        "publicationState": custody["publicationState"],
        "xmlMembersRehashedFromDisk": rehashed_xml_count(_load(receipt_path)["sourceManifest"]["files"], xml_dir),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", default=RECEIPT)
    parser.add_argument("--xml-dir", default=None, help="local directory holding the eleven TCP XML objects")
    parser.add_argument("--check", action="store_true", help="verify without writing")
    args = parser.parse_args()

    if args.check:
        print(json.dumps(check(args.receipt, args.xml_dir), ensure_ascii=False, indent=2))
        return 0

    custody, raw_manifest = build(args.receipt, args.xml_dir)
    (ROOT / PACKET_MANIFEST_OUT).write_bytes(raw_manifest)
    (ROOT / CUSTODY_OUT).write_text(
        json.dumps(custody, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: custody[key] for key in ("fileCount", "totalBytes", "manifestSha256", "custodyState")},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
