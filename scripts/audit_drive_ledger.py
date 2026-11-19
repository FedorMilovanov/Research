#!/usr/bin/env python3
"""Check Drive-library ledger rows against Drive itself and against the local file.

A ledger row like

    | `00_README_AND_NAVIGATION.md` | `1sV3…X10` | 89100 | `89ad08d7…` |

claims three things at once: that object exists in Drive, that its size and MD5 are
those values, and that the local file named in the same row has exactly those bytes.
Nothing re-read any of that, so a row stays "verified-looking" while both sides move.

The tool joins three sources and never invents a fourth:

* the **ledger rows** parsed from the Markdown;
* a **Drive snapshot** (``--snapshot``) holding what Drive answered about specific
  object ids on a stated date - the connector is asked outside this script, because
  the check must stay offline and deterministic;
* the **local bytes**, hashed here.

States per row:

* ``drive-verified``      - Drive's size and MD5 equal the claim;
* ``drive-mismatch``      - Drive answered, but its values differ from the claim;
* ``drive-not-sampled``   - no snapshot entry for this id (the common case: one API
  call per object, and this pass read only a sample);
* ``local-current``       - the local file still hashes to the claim;
* ``local-moved-on``      - the local file exists but has different bytes.

The two axes are reported separately on purpose. A row can be ``drive-verified`` and
``local-moved-on`` at the same time, and that is exactly what a ledger of upload
moments looks like once the department is rewritten: Drive still holds the bytes that
were uploaded, while the working copy has grown.

    python3 -B scripts/audit_drive_ledger.py --summary
    python3 -B scripts/audit_drive_ledger.py -o data/drive-ledger-audit-2026-11-18.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA_VERSION = "drive-ledger-audit/1"
AUTHORITY_ID = "DRIVE-LEDGER-AUDIT-2026-11-18"

SKIP_DIRS = {".git", "node_modules", "incoming", ".venv", "__pycache__"}
ROW_RE = re.compile(
    r"\|\s*(?P<label>[^|]{1,200}?)\|\s*`?(?P<id>1[A-Za-z0-9_-]{27,43})`?\s*\|"
    # The checksum cell is 32 hex (MD5) or 64 hex (SHA-256). It must be bounded on both
    # sides: an unbounded {32} silently reads the first half of a SHA-256 as an MD5 and
    # then reports a mismatch against Drive's MD5 - a false accusation, not a finding.
    r"\s*(?P<size>[\d\s]{1,12})\|\s*`?(?P<hash>(?<![0-9a-fA-F])[0-9a-fA-F]{32}(?:[0-9a-fA-F]{32})?)(?![0-9a-fA-F])`?"
)
LOCAL_RE = re.compile(r"`([^`\n]+\.(?:md|json|txt|pdf|docx|xml))`")
# A row whose label carries a wave or a revision records one upload, not "now".
WAVE_RE = re.compile(r"wave\s*\d+|rev\s*\d+|_\d{4}-\d{2}-\d{2}", re.I)


def iter_markdown(root: Path) -> list[Path]:
    out = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if set(rel.parts) & SKIP_DIRS:
            continue
        if rel.parts[:1] == ("data",):
            continue
        out.append(path)
    return out


def parse_rows(root: Path) -> list[dict]:
    rows = []
    for path in iter_markdown(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            match = ROW_RE.search(line)
            if not match:
                continue
            label = match.group("label").strip()
            local = LOCAL_RE.search(label)
            rows.append({
                "file": rel,
                "line": lineno,
                "label": label[:120],
                "driveId": match.group("id"),
                "size": int(re.sub(r"\s", "", match.group("size")) or 0),
                "md5": match.group("hash").lower() if len(match.group("hash")) == 32 else None,
                "sha256": match.group("hash").lower() if len(match.group("hash")) == 64 else None,
                "localName": local.group(1) if local else None,
                "moment": bool(WAVE_RE.search(label)),
            })
    return rows


def find_local(name: str, source_dir: Path, root: Path) -> tuple[Path | None, int]:
    """Resolve a bare file name only when it is unique in its own tree.

    The same name can exist in several sub-folders of a department, and picking the
    first one would convict a row of "different bytes" while pointing at a different
    document. Ambiguity is reported, not resolved by guessing.
    """
    for base in (source_dir, root):
        candidates = sorted(base.rglob(name))
        if candidates:
            return (candidates[0], len(candidates)) if len(candidates) == 1 else (None, len(candidates))
    return None, 0


def md5_of(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit(root: Path, snapshot: dict | None = None) -> dict:
    objects = (snapshot or {}).get("objects", {})
    rows = parse_rows(root)
    findings = []
    drive_state: dict[str, int] = {}
    local_state: dict[str, int] = {}
    for row in rows:
        claimed = objects.get(row["driveId"])
        if claimed is None:
            dstate = "drive-not-sampled"
        elif row["md5"] is None:
            # SHA-256-only row: Drive's file metadata exposes MD5, never SHA-256, so the
            # byte claim cannot be confirmed without downloading. Size can be.
            dstate = ("drive-size-only"
                      if str(claimed.get("size")) == str(row["size"]) else "drive-size-mismatch")
        elif (str(claimed.get("size")) == str(row["size"])
              and (claimed.get("md5") or "").lower() == row["md5"]):
            dstate = "drive-verified"
        else:
            dstate = "drive-mismatch"
        drive_state[dstate] = drive_state.get(dstate, 0) + 1

        lstate, local_path, local_md5 = "local-unresolved", None, None
        if row["localName"]:
            source_dir = (root / row["file"]).parent
            local, matches = find_local(row["localName"], source_dir, root)
            if local is None and matches:
                lstate = "local-ambiguous"
            elif local is not None:
                local_path = local.relative_to(root).as_posix()
                local_md5 = md5_of(local)
                same = (row["md5"] is not None and local_md5 == row["md5"]
                        and local.stat().st_size == row["size"])
                lstate = "local-current" if same else "local-moved-on"
        local_state[lstate] = local_state.get(lstate, 0) + 1

        findings.append({
            "file": row["file"], "line": row["line"], "label": row["label"],
            "driveId": row["driveId"], "claimedSize": row["size"], "claimedMd5": row["md5"],
            "claimedSha256": row["sha256"],
            "moment": row["moment"],
            "driveState": dstate,
            "driveSize": None if claimed is None else claimed.get("size"),
            "driveMd5": None if claimed is None else claimed.get("md5"),
            "driveName": None if claimed is None else claimed.get("name"),
            "localState": lstate, "localPath": local_path, "localMd5": local_md5,
            "localMatches": find_local(row["localName"], (root / row["file"]).parent, root)[1]
            if row["localName"] else 0,
            "localSize": None if local_path is None else (root / local_path).stat().st_size,
        })
    return {
        "schemaVersion": SCHEMA_VERSION,
        "authorityId": AUTHORITY_ID,
        "root": ".",
        "scope": {
            "ledgerRows": len(rows),
            "distinctDriveIds": len({r["driveId"] for r in rows}),
            "rowsNamingLocalFile": sum(1 for r in rows if r["localName"]),
            "snapshotDate": (snapshot or {}).get("retrievedOn"),
            "objectsInSnapshot": len(objects),
        },
        "totals": {
            "drive": drive_state,
            "local": local_state,
            "driveVerifiedOfSampled": drive_state.get("drive-verified", 0),
        },
        "findings": findings,
    }


def summary(report: dict) -> str:
    scope, totals = report["scope"], report["totals"]
    lines = [
        f"Ledger rows: {scope['ledgerRows']} ({scope['distinctDriveIds']} distinct Drive ids,"
        f" {scope['rowsNamingLocalFile']} name a local file)",
        f"Drive side: " + ", ".join(f"{k}={v}" for k, v in sorted(totals["drive"].items()))
        + f"  [snapshot {scope['snapshotDate']}, {scope['objectsInSnapshot']} objects]",
        "Local side: " + ", ".join(f"{k}={v}" for k, v in sorted(totals["local"].items())),
    ]
    for finding in report["findings"]:
        if finding["driveState"] == "drive-verified" or finding["localState"] == "local-moved-on":
            lines.append(
                f"  {finding['driveState']:19s} {finding['localState']:15s}"
                f" size {finding['claimedSize']} -> drive {finding['driveSize']},"
                f" local {finding['localSize']}: {finding['label'][:60]}"
            )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".")
    parser.add_argument("--snapshot")
    parser.add_argument("-o", "--output")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    snapshot = None
    if args.snapshot:
        snapshot = json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
    report = audit(root, snapshot)
    if args.output:
        Path(args.output).write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"wrote {args.output}", file=sys.stderr)
    if args.summary or not args.output:
        print(summary(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
