#!/usr/bin/env python3
"""Check SHA-256 values that documents claim for files inside this checkout.

A receipt like ``00_README_AND_NAVIGATION.md = 2a8d41c1…`` is a locator plus a
digest: the path says where, the hash says which bytes. Nothing re-read the
bytes, so a hash could describe an earlier revision, an edited file, or nothing
at all, and the document would still look verified.

This tool reads each 64-hex value in the Markdown, finds the repository file
named next to it, hashes that file and reports:

* ``match``     - the file in the checkout hashes to the claimed value;
* ``stale``     - the file exists, its bytes no longer hash to the claim;
* ``external``  - the hash names a file that is not in the checkout at all
  (a downloaded PDF, a scanned image): nothing local to hash;
* ``external-drive`` - the line is about a Google Drive object that merely has a
  repository-like name (``00_README_AND_NAVIGATION.md`` in Drive is not this
  repository's file), so the repository file of that name must not be hashed;
* ``unclaimed`` - the hash stands alone (a quote, a log, an inline example).

A manifest for an earlier packaging round is *expected* to go stale: it records
the bytes of that round. The tool therefore reports, and only refuses to pass
when asked to (`--check` fails on `stale`), because "stale" is a fact about a
snapshot, not automatically a defect.

It never rewrites the claim. A wrong hash is a finding; replacing it with the
current file's hash would turn a stale receipt into a fabricated fresh one.

    python3 -B scripts/verify_internal_digests.py --summary
    python3 -B scripts/verify_internal_digests.py -o data/internal-digests-verified.json
    python3 -B scripts/verify_internal_digests.py --check   # 1 on mismatch/unavailable
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA_VERSION = "internal-digests-verified/1"
AUTHORITY_ID = "INTERNAL-DIGESTS-2026-11-18"

HEX_RE = re.compile(r"\b[0-9a-f]{64}\b")
DRIVE_RE = re.compile(r"drive(File)?Id|drive\.google\.com|https?://drive|\bgoogle_drive\b", re.I)
# A Drive identifier is 25-50 URL-safe characters and is not a hex digest, so a
# row that carries one is a Drive table even when the word "drive" is absent.
ID_TOKEN_RE = re.compile(r"\b[A-Za-z0-9_-]{25,50}\b")
HEX_ONLY_RE = re.compile(r"[0-9a-fA-F]{25,}")
DIGEST_WORDS = re.compile(r"sha-?256|sha\u2011256|\u0445\u0435\u0448|checksum|digest|\u043a\u043e\u043d\u0442\u0440\u043e\u043b\u044c\u043d", re.I)
PATH_RE = re.compile(
    r"(?<![\w/.-])((?:[\w()+-][\w()+-]*/)*[\w()+-][\w()+-]*\.(?:md|json|txt|csv|zip|pdf|py|xml|tei|png|jpg|jpeg))"
)
SKIP_DIRS = (".git", "node_modules")
ROUND_MANIFEST_RE = re.compile(r"V\d+_SINGLE_ZIP_MANIFEST")
HANDOFF_RE = re.compile(r"handoff|ХЕНДОФФ|handover", re.I)


def source_kind(rel: str) -> str:
    """What kind of document makes the claim.

    A round manifest and a handoff table both record a *moment*: the bytes of
    that packaged round, the hashes that a receiving agent was handed. Their
    digests are expected to stop matching the working tree, and that is not a
    defect in the document. A live document claiming a digest of its neighbour
    is a different matter, so the two are counted apart.
    """
    if ROUND_MANIFEST_RE.search(rel):
        return "round-manifest"
    if HANDOFF_RE.search(rel):
        return "handoff"
    return "live-document"


def iter_markdown(root: Path) -> list[Path]:
    out = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        if any(part in rel.split("/")[:1] for part in SKIP_DIRS):
            continue
        out.append(path)
    return out


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve(candidate: str, source: Path, root: Path) -> Path | None:
    for base in (source.parent, root):
        path = (base / candidate).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            continue
        if path.is_file():
            return path
    return None


def classify(line: str, digest: str, source: Path, root: Path) -> dict:
    """Decide the state of one claimed digest on one line."""
    ids = [tok for tok in ID_TOKEN_RE.findall(line) if not HEX_ONLY_RE.fullmatch(tok)]
    if DRIVE_RE.search(line) or ids:
        return {"state": "external-drive", "paths": [], "marked": bool(DIGEST_WORDS.search(line))}
    candidates = [c for c in PATH_RE.findall(line) if not c.startswith(("http", "www."))]
    claimed_paths = []
    for candidate in candidates:
        resolved = resolve(candidate, source, root)
        if resolved is None:
            claimed_paths.append({"path": candidate, "state": "external"})
            continue
        state = "match" if sha256_of(resolved) == digest else "stale"
        claimed_paths.append({"path": candidate, "state": state})
    if not claimed_paths:
        return {"state": "unclaimed", "paths": []}
    states = {c["state"] for c in claimed_paths}
    if "match" in states:
        state = "match"
    elif "stale" in states:
        state = "stale"
    else:
        state = "external"
    return {"state": state, "paths": claimed_paths, "marked": bool(DIGEST_WORDS.search(line))}


def pair_claims(line: str) -> list[tuple[str, str]] | None:
    """Pair hashes with paths by order, or refuse when the counts disagree.

    A table row may list several digests for several files; pairing the first
    hash with the first path is right only when the row has one of each, or the
    same number of both. Otherwise the row is ambiguous and nothing is claimed.
    """
    hashes = HEX_RE.findall(line)
    paths = [c for c in PATH_RE.findall(line) if not c.startswith(("http", "www."))]
    if not hashes or not paths:
        return None
    if len(hashes) == len(paths):
        return list(zip(hashes, paths))
    if len(hashes) == 1 and len(paths) == 1:
        return [(hashes[0], paths[0])]
    if len(hashes) == 2 and len(paths) == 1:
        # A receipt row often carries two hashes for one file: the hash written in
        # an earlier receipt and the hash of the bytes at the time of writing.
        # Both are claims about the same path, so each is checked on its own.
        return [(hash_, paths[0]) for hash_ in hashes]
    return None


def verify(root: Path, skip_lines: int = 0) -> dict:
    findings = []
    by_state: dict[str, int] = {}
    stale_by_kind: dict[str, int] = {}
    files_touched: dict[str, int] = {}
    for path in iter_markdown(root):
        rel = path.relative_to(root).as_posix()
        if rel.startswith("incoming/"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if DRIVE_RE.search(line) or any(
                ID_TOKEN_RE.fullmatch(tok) and not HEX_ONLY_RE.fullmatch(tok)
                for tok in ID_TOKEN_RE.findall(line)
            ):
                for match in HEX_RE.finditer(line):
                    findings.append({
                        "file": rel, "line": lineno, "sha256": match.group(0),
                        "state": "external-drive", "paths": [],
                    })
                    by_state["external-drive"] = by_state.get("external-drive", 0) + 1
                continue
            pairs = pair_claims(line)
            for match in HEX_RE.finditer(line):
                if pairs is None:
                    if not PATH_RE.findall(line):
                        state = "unclaimed"
                    else:
                        state = "ambiguous"
                    by_state[state] = by_state.get(state, 0) + 1
                    findings.append({
                        "file": rel, "line": lineno, "sha256": match.group(0),
                        "state": state, "paths": [],
                    })
                    continue
                digest = match.group(0)
                claimed = [p for h, p in pairs if h == digest] or [p for _, p in pairs]
                paths = []
                for candidate in claimed:
                    resolved = resolve(candidate, path, root)
                    if resolved is None:
                        paths.append({"path": candidate, "state": "external"})
                    else:
                        paths.append({"path": candidate,
                                      "state": "match" if sha256_of(resolved) == digest else "stale"})
                states = {c["state"] for c in paths}
                state = "match" if "match" in states else ("stale" if "stale" in states else "external")
                by_state[state] = by_state.get(state, 0) + 1
                kind = source_kind(rel)
                if state == "stale":
                    files_touched[rel] = files_touched.get(rel, 0) + 1
                    stale_by_kind[kind] = stale_by_kind.get(kind, 0) + 1
                findings.append({
                    "file": rel, "line": lineno, "sha256": digest,
                    "state": state, "paths": paths, "sourceKind": kind,
                })
            continue
            for match in HEX_RE.finditer(line):
                result = classify(line, match.group(0), path, root)
                by_state[result["state"]] = by_state.get(result["state"], 0) + 1
                if result["state"] == "stale":
                    files_touched[rel] = files_touched.get(rel, 0) + 1
                findings.append({
                    "file": rel,
                    "line": lineno,
                    "sha256": match.group(0),
                    "state": result["state"],
                    "paths": result["paths"],
                })
    return {
        "schemaVersion": SCHEMA_VERSION,
        "authorityId": AUTHORITY_ID,
        "root": ".",
        "scope": {"markdownFiles": len(iter_markdown(root))},
        "totals": {
            "claims": len(findings),
            "byState": by_state,
            "filesWithStaleClaims": len(files_touched),
            "staleBySourceKind": stale_by_kind,
        },
        "staleByFile": dict(sorted(files_touched.items(), key=lambda kv: (-kv[1], kv[0]))),
        "findings": findings,
    }


PATHY_RE = re.compile(r"^[^\n]{1,160}\.(?:md|json|txt|csv|zip|pdf|py|xml|tei|png|jpg|jpeg)$")


def iter_json(root: Path) -> list[Path]:
    out = []
    for path in sorted(root.rglob("*.json")):
        rel = path.relative_to(root).as_posix()
        if rel.startswith(SKIP_DIRS) or rel.startswith("incoming/"):
            continue
        out.append(path)
    return out


def verify_json(root: Path) -> dict:
    """Check machine registries that pair one digest with one path in one object.

    A JSON record such as ``{"path": "data/x.json", "sha256": "…"}`` claims the
    bytes of a file inside the checkout. The pairing is only accepted when the
    object holds exactly one digest and exactly one path-like string; anything
    looser is not paired, because guessing which hash belongs to which file would
    manufacture a claim the record never made.
    """
    findings = []
    by_state: dict[str, int] = {}
    for path in iter_json(root):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        rel = path.relative_to(root).as_posix()

        def walk(node: object) -> None:
            if isinstance(node, dict):
                digests = [v for v in node.values() if isinstance(v, str) and HEX_RE.fullmatch(v)]
                paths = [v for v in node.values() if isinstance(v, str) and PATHY_RE.match(v)]
                if len(digests) == 1 and len(paths) == 1:
                    candidate = paths[0]
                    resolved = None
                    try:
                        maybe = (root / candidate).resolve()
                        maybe.relative_to(root)
                        resolved = maybe if maybe.is_file() else None
                    except (OSError, ValueError):
                        resolved = None
                    if resolved is None:
                        state = "external"
                    else:
                        state = "match" if sha256_of(resolved) == digests[0] else "stale"
                    by_state[state] = by_state.get(state, 0) + 1
                    findings.append({
                        "file": rel, "sha256": digests[0], "path": candidate, "state": state,
                    })
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        walk(data)
    return {
        "totals": {"records": len(findings), "byState": by_state},
        "findings": findings,
    }


def summary(report: dict) -> str:
    totals = report["totals"]
    states = totals["byState"]
    lines = [
        f"Markdown files scanned: {report['scope']['markdownFiles']}",
        "Digest claims by state: " + ", ".join(f"{k}={v}" for k, v in sorted(states.items())),
        f"Stale claims: {states.get('stale', 0)} in {totals['filesWithStaleClaims']} files "
        f"({totals['staleBySourceKind']})",
    ]
    for name, count in list(report["staleByFile"].items())[:10]:
        lines.append(f"  {count:4d}  {name}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("-o", "--output")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--check", action="store_true",
                        help="exit 1 when a live document's claim no longer matches the bytes")
    parser.add_argument("--only", choices=("stale", "external", "external-drive", "unclaimed", "ambiguous", "match"))
    parser.add_argument("--json-mode", action="store_true", help="check JSON records instead of Markdown lines")
    parser.add_argument("--no-json", action="store_true", help="skip the JSON pass in the report")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    if args.json_mode:
        payload = verify_json(root)
        states = payload["totals"]["byState"]
        print("JSON records: " + ", ".join(f"{k}={v}" for k, v in sorted(states.items())))
        for finding in payload["findings"]:
            if args.only and finding["state"] != args.only:
                continue
            print(f"  {finding['state']:9s} {finding['file']} {finding['sha256'][:12]}… -> {finding['path']}")
        if args.check and states.get("stale"):
            return 1
        return 0

    report = verify(root)
    if not args.no_json:
        report["jsonRecords"] = verify_json(root)["totals"]
    if args.only:
        report["findings"] = [f for f in report["findings"] if f["state"] == args.only]
    if args.output:
        Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    if args.summary or not args.output:
        print(summary(report))
    if args.only:
        for finding in report["findings"]:
            print(f"  {finding['state']:11s} {finding['file']}:{finding['line']} "
                  f"{finding['sha256'][:12]}… -> {', '.join(p['path'] for p in finding['paths']) or '-'}")
    live_stale = report["totals"]["staleBySourceKind"].get("live-document", 0)
    if args.check and live_stale:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
