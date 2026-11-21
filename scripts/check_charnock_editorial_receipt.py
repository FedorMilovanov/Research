#!/usr/bin/env python3
"""Validate and, when the source commit is present, rebuild the ED-09 archive.

Offline receipt gate:
    python3 -B scripts/check_charnock_editorial_receipt.py --check

Exact source reconstruction (fetch the receipt's sourceGitSha first when needed):
    git fetch --no-tags origin 209c593fc23bcc32c29bc636b93bcf29d892e725
    python3 -B scripts/check_charnock_editorial_receipt.py --git-source

The checker proves carrier/source accounting only. It does not approve translations,
rights, publication, or independent review.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data" / "charnock-editorial-book-receipt-v1-20261121-ed09.json"
BASE = Path("БИОГРАФИИ") / "Стивен Чарнок"
MANUSCRIPT_NAMES = (
    "INTRO_MIR_STEPHEN_CHARNOCK_WORKING_DRAFT.md",
    "I_CHELOVEK_KEMBRIDZH_DUBLIN_LONDON_WORKING_DRAFT.md",
    "II_UCHENYI_I_PROPOVEDNIK_WORKING_DRAFT.md",
    "III_CHARNOCK_AND_SCRIPTURE_FROM_TEXT_TO_SERMON_WORKING_DRAFT.md",
    "IV_BOGOSLOVSKII_PORTRET_WORKING_DRAFT.md",
    "V_KAK_PROPOVEDI_STALI_KNIGAMI_WORKING_DRAFT.md",
    "VI_GLAVNAYA_KNIGA_BYTIE_I_ATRIBUTY_WORKING_DRAFT.md",
    "VII_ZA_PREDELAMI_GLAVNOI_KNIGI_WORKING_DRAFT.md",
    "VIII_CHARNOCK_POSLE_CHARNOCKA_WORKING_DRAFT.md",
    "REFERENCE_KHRONOLOGIYA_TRUDY_ISTOCHNIKI_WORKING_DRAFT.md",
)
SUPPORT_PATHS = (
    BASE / "reader-preview" / "CHARNOCK_FULL_BOOK_EDITORIAL_READER_2026-11-21.md",
    BASE / "reader-preview" / "README.md",
    BASE / "supplemental-audits" / "ED02_LINGENDES_84_87_TO_CHARNOCK_621_ALIGNMENT_2026-11-18.md",
    BASE / "supplemental-audits" / "ED06_EXTERNAL_REVIEW_PACKET_ALL12_2026-11-18.md",
    BASE / "supplemental-audits" / "ED06_ALL12_TRANSLATION_CONTEXT_REVIEW_2026-11-17.md",
    BASE / "supplemental-audits" / "ED06_THREE_ENGLISH_WITNESS_TRIANGULATION_2026-11-18.md",
    Path("data") / "charnock-series-editorial-plan-v1.json",
)
SOURCE_PATHS = tuple(
    sorted(
        [BASE / "manuscripts" / name for name in MANUSCRIPT_NAMES] + list(SUPPORT_PATHS),
        key=lambda path: path.as_posix(),
    )
)
EXPECTED_HOLDS = ["EVIDENCE_HOLD", "LOCATOR_HOLD", "RIGHTS_HOLD", "PUBLICATION_HOLD"]
SHA40 = re.compile(r"[0-9a-f]{40}\Z")
SHA64 = re.compile(r"[0-9a-f]{64}\Z")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_receipt(path: Path) -> tuple[dict | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [f"не читается {display_path(path)}: {exc}"]
    if not isinstance(data, dict):
        return None, ["корень квитанции должен быть JSON object"]
    return data, []


def validate_receipt(data: dict, root: Path = ROOT) -> list[str]:
    errors: list[str] = []

    exact = {
        "schemaVersion": 1,
        "receiptId": "CHARNOCK-ED09-EDITORIAL-17-SOURCE-2026-11-21",
        "evidenceRole": "scope-limited-supplemental-corpus-custody-not-publication-authority",
        "archiveFormat": "REPRODUCIBLE_ZIP_WITH_INNER_SOURCE_MANIFEST",
        "sourceFileCount": 17,
        "manuscriptCount": 10,
        "editorialReaderCount": 1,
        "externalFacsimilesIncluded": False,
        "sourceDestinationExactByteMatch": True,
        "evidenceState": "FULL_EDITORIAL_SOURCE_SNAPSHOT_DURABLE_VERIFIED",
        "rightsState": "RIGHTS_UNKNOWN",
        "publicationState": "BLOCKED",
        "independentTranslationReview": "0/12; ED09 includes unsigned editorial corrections only",
        "historicalReceiptsUnmodified": True,
    }
    for field, expected in exact.items():
        if data.get(field) != expected:
            errors.append(f"{field}: ожидалось {expected!r}, получено {data.get(field)!r}")

    commit = data.get("sourceGitSha")
    if not isinstance(commit, str) or not SHA40.fullmatch(commit):
        errors.append("sourceGitSha должен быть полным lowercase Git SHA")
    elif data.get("archiveFileName") != f"charnock-full-editorial-book-{commit[:12]}.zip":
        errors.append("archiveFileName не связан с sourceGitSha")

    if data.get("holds") != EXPECTED_HOLDS:
        errors.append(f"holds должны точно сохранять {EXPECTED_HOLDS!r}")

    archive_bytes = data.get("archiveBytes")
    destination_bytes = data.get("destinationBytesReadback")
    if not isinstance(archive_bytes, int) or archive_bytes <= 0:
        errors.append("archiveBytes должен быть положительным integer")
    if destination_bytes != archive_bytes:
        errors.append("destinationBytesReadback расходится с archiveBytes")

    archive_hash = data.get("archiveSha256")
    destination_hash = data.get("destinationSha256Readback")
    for field, value in (
        ("archiveSha256", archive_hash),
        ("destinationSha256Readback", destination_hash),
        ("sourceManifestSha256", data.get("sourceManifestSha256")),
    ):
        if not isinstance(value, str) or not SHA64.fullmatch(value):
            errors.append(f"{field} должен быть полным lowercase SHA-256")
    if destination_hash != archive_hash:
        errors.append("destinationSha256Readback расходится с archiveSha256")

    if not isinstance(data.get("sourceTotalBytes"), int) or data.get("sourceTotalBytes", 0) <= 0:
        errors.append("sourceTotalBytes должен быть положительным integer")

    previous = data.get("previousReceipt")
    if not isinstance(previous, str) or not (root / previous).is_file():
        errors.append("previousReceipt не указывает на существующую квитанцию")

    identities = data.get("sourceMemberIdentity")
    if not isinstance(identities, dict) or not identities:
        errors.append("sourceMemberIdentity должен содержать проверяемые members")
    else:
        allowed = {path.as_posix() for path in SOURCE_PATHS}
        for path, identity in identities.items():
            if path not in allowed:
                errors.append(f"sourceMemberIdentity содержит путь вне bounded 17-source scope: {path}")
            if not isinstance(identity, dict):
                errors.append(f"sourceMemberIdentity[{path}] должен быть object")
                continue
            if not isinstance(identity.get("bytes"), int) or identity.get("bytes", 0) <= 0:
                errors.append(f"sourceMemberIdentity[{path}].bytes некорректен")
            if not isinstance(identity.get("gitBlobSha1"), str) or not SHA40.fullmatch(identity["gitBlobSha1"]):
                errors.append(f"sourceMemberIdentity[{path}].gitBlobSha1 некорректен")
            if not isinstance(identity.get("sha256"), str) or not SHA64.fullmatch(identity["sha256"]):
                errors.append(f"sourceMemberIdentity[{path}].sha256 некорректен")

    return errors


def git_blob(raw: bytes) -> str:
    prefix = b"blob " + str(len(raw)).encode("ascii") + b"\0"
    return hashlib.sha1(prefix + raw).hexdigest()


def canonical_json(data: object) -> bytes:
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def build_manifest(commit: str, rows: dict[str, bytes]) -> dict:
    return {
        "schema": "charnock-editorial-book-custody-v1",
        "sourceGitSha": commit,
        "manuscriptCount": 10,
        "sourceFileCount": len(rows),
        "scope": (
            "10 working manuscripts, full editorial reader, navigation and supporting textual "
            "research; no image/facsimile license, independent expert review or publication approval"
        ),
        "holds": EXPECTED_HOLDS,
        "files": {
            path: {
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "gitBlobSha1": git_blob(raw),
            }
            for path, raw in rows.items()
        },
    }


def build_archive(manifest: dict, rows: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, raw in rows.items():
            info = zipfile.ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        info = zipfile.ZipInfo("SOURCE_MANIFEST.json", date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(
            info,
            canonical_json(manifest),
            compress_type=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        )
    return stream.getvalue()


def read_git_rows(commit: str, root: Path = ROOT) -> tuple[dict[str, bytes], list[str]]:
    rows: dict[str, bytes] = {}
    errors: list[str] = []
    for path in SOURCE_PATHS:
        key = path.as_posix()
        proc = subprocess.run(
            ["git", "show", f"{commit}:{key}"],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode:
            message = proc.stderr.decode("utf-8", errors="replace").strip()
            errors.append(f"не читается {commit}:{key}: {message}")
            continue
        rows[key] = proc.stdout
    return rows, errors


def validate_git_source(data: dict, root: Path = ROOT) -> list[str]:
    commit = data.get("sourceGitSha")
    if not isinstance(commit, str) or not SHA40.fullmatch(commit):
        return ["sourceGitSha некорректен; source reconstruction не выполняется"]

    rows, errors = read_git_rows(commit, root)
    if errors:
        return errors
    if list(rows) != sorted(rows):
        errors.append("17-source path order не детерминирован")
    if len(rows) != 17:
        errors.append(f"ожидалось 17 source members, получено {len(rows)}")
        return errors

    manifest = build_manifest(commit, rows)
    manifest_bytes = canonical_json(manifest)
    archive = build_archive(manifest, rows)

    comparisons = {
        "sourceFileCount": len(rows),
        "sourceTotalBytes": sum(len(raw) for raw in rows.values()),
        "sourceManifestSha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "archiveBytes": len(archive),
        "archiveSha256": hashlib.sha256(archive).hexdigest(),
    }
    for field, actual in comparisons.items():
        if data.get(field) != actual:
            errors.append(f"{field}: квитанция {data.get(field)!r}, реконструкция {actual!r}")

    identities = data.get("sourceMemberIdentity") or {}
    files = manifest["files"]
    for path, expected in identities.items():
        if files.get(path) != expected:
            errors.append(f"sourceMemberIdentity расходится с реконструкцией: {path}")

    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="offline receipt invariants")
    mode.add_argument("--git-source", action="store_true", help="also rebuild from sourceGitSha")
    parser.add_argument("--receipt", type=Path, default=RECEIPT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    data, errors = load_receipt(args.receipt)
    if data is not None:
        errors.extend(validate_receipt(data))
        if args.git_source and not errors:
            errors.extend(validate_git_source(data))
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    mode = "receipt + reconstructed 17-source archive" if args.git_source else "receipt"
    print(f"Charnock ED-09: PASS ({mode}; rights/publication/review unchanged)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
