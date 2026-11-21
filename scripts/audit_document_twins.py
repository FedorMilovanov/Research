#!/usr/bin/env python3
"""Find documents that are the same text twice, and ask whether that is declared.

Two corpora can hold the same document under two names. Nothing notices: both
files look complete, both are cited, and a correction lands in one of them. The
document that was not corrected keeps answering questions in the old words, and
no receipt is stale, because neither copy claims anything about the other.

This tool compares the documents themselves, not their names:

* every Markdown file with at least ``--min-words`` words is turned into a set of
  8-word shingles (word tokens, punctuation dropped);
* candidates are proposed from a fixed 48-element sample of that set, so the run
  is deterministic and does not depend on input order or on a random seed;
* candidates are then measured exactly by Jaccard overlap of the full sets.

Reported states:

* ``identical-text`` - the same words in the same order (``sameBytes`` says whether
  even the bytes agree);
* ``superset``       - one text contains every non-empty line of the other, plus
  additions: a supplement that kept its base;
* ``near-identical`` - overlap >= ``--near``;
* ``shared-text``    - overlap >= 0.5: lineage, versions, common blocks.

A twin is not automatically a defect: a supplement is meant to repeat its base and
a version series is meant to share text. What is worth knowing is whether the
duplication is *declared*. The corpus convention is a master index line saying
``дубль файла 08`` or ``supplement к 04``, and the tool accepts only that shape:

* ``index-line``   - a line carries a declaration word, names one member, and
  points at the other either by file name or by ``файла NN`` / ``к NN``;
* ``version-name`` - the two file names are the same stem with different version
  markers (``v0_5``/``v0_6``, ``V5``/``V6``) or different trailing dates, so the
  copies announce themselves as generations of one document.

``--check`` fails only on an ``identical-text`` pair whose duplication nothing
declares. It is **not** wired into CI: today exactly one such pair exists, and that
is an open item for the lane that owns its index, not a licence for this tool to
rewrite somebody's master map.

    python3 -B scripts/audit_document_twins.py --summary
    python3 -B scripts/audit_document_twins.py -o data/document-twins-2026-11-18.json
    python3 -B scripts/audit_document_twins.py --only identical-text
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA_VERSION = "document-twins/1"
AUTHORITY_ID = "DOCUMENT-TWINS-2026-11-18"

SHINGLE = 8
SIGNATURE = 48
SAMPLE_STRIDE = 6
SKIP_DIRS = {".git", "node_modules", "incoming", ".venv", "__pycache__"}
WORD_RE = re.compile(r"[^\W_]+", re.UNICODE)
DECLARATION_RE = re.compile(
    r"\u0434\u0443\u0431\u043b|duplicate|\u043a\u043e\u043f\u0438|\bcopy\b|supplement"
    r"|\u0434\u043e\u043f\u043e\u043b\u043d\u0435\u043d|\u0432\u0435\u0440\u0441\u0438|\bversion\b"
    r"|\u043f\u0440\u0435\u0434\u044b\u0434\u0443\u0449|predecessor",
    re.I,
)
VERSION_RE = re.compile(r"[vV](\d+(?:[._]\d+)*)")
DATE_SUFFIX_RE = re.compile(r"_(\d{4}-\d{2}-\d{2})(?=\.md$)")


def tokens_of(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def shingles(tokens: list[str], size: int = SHINGLE) -> set[bytes]:
    if len(tokens) < size:
        return set()
    return {
        hashlib.blake2b(" ".join(tokens[i:i + size]).encode("utf-8"), digest_size=8).digest()
        for i in range(len(tokens) - size + 1)
    }


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


def fingerprint(root: Path, min_words: int) -> dict[str, dict]:
    records: dict[str, dict] = {}
    for path in iter_markdown(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        tokens = tokens_of(text)
        if len(tokens) < min_words:
            continue
        marks = shingles(tokens)
        if not marks:
            continue
        records[rel] = {
            "tokens": len(tokens),
            "lines": text.count("\n") + 1,
            "shingles": marks,
            "signature": tuple(sorted(marks)[:SIGNATURE]),
            "bytes": hashlib.sha256(path.read_bytes()).hexdigest(),
            "text": text,
            "lineset": {line.strip() for line in text.splitlines() if line.strip()},
        }
    return records


def candidate_pairs(records: dict[str, dict]) -> set[tuple[str, str]]:
    """Propose pairs from the fixed sample, never from a random seed."""
    buckets: dict[bytes, list[str]] = {}
    for rel, rec in records.items():
        for value in rec["signature"][::SAMPLE_STRIDE]:
            buckets.setdefault(value, []).append(rel)
    pairs: set[tuple[str, str]] = set()
    for members in buckets.values():
        if len(members) < 2 or len(members) > 64:
            continue
        members = sorted(members)
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                pairs.add((members[i], members[j]))
    return pairs


def declaration_lines(records: dict[str, dict]) -> list[tuple[str, str]]:
    """Every line that could declare a duplication, collected once."""
    out = []
    for rel, rec in records.items():
        for line in rec["text"].splitlines():
            if DECLARATION_RE.search(line):
                out.append((rel, line.strip()))
    return out


def lead_number(rel: str) -> int | None:
    match = re.match(r"0*(\d{1,3})[_\W]", Path(rel).name)
    return int(match.group(1)) if match else None


def declaration_for(a: str, b: str, lines: list[tuple[str, str]]) -> dict | None:
    """A line declares a duplication only if it names one file and points at the other.

    The pointer is either the other file's name or the corpus's own shorthand
    ``файла 08`` / ``к 04``. Bare numbers are not accepted: a line reading
    ``Лк 24:13`` contains both "24" and "13" and declares nothing.
    """
    name_a, name_b = Path(a).name, Path(b).name
    num_a, num_b = lead_number(a), lead_number(b)
    for rel, line in lines:
        for own, own_num, other_name, other_num in (
            (name_a, num_a, name_b, num_b),
            (name_b, num_b, name_a, num_a),
        ):
            if own not in line:
                continue
            if other_name in line:
                return {"kind": "index-line", "file": rel, "line": line[:300]}
            if other_num is not None and re.search(
                rf"(?:\u0444\u0430\u0439\u043b[а-яё]*|\bк)\s*`?0?{other_num}\b", line
            ):
                return {"kind": "index-line", "file": rel, "line": line[:300]}
    return None


def _stem_without_edition(name: str) -> tuple[str, str | None]:
    """Strip the edition markers a file name uses to announce its generation."""
    stem = name[:-3] if name.endswith(".md") else name
    stem = re.sub(r"^\d+[_\W]+", "", stem)
    stem = DATE_SUFFIX_RE.sub("", stem + ".md")[:-3] if DATE_SUFFIX_RE.search(stem + ".md") else stem
    version = VERSION_RE.search(stem)
    marker = version.group(1) if version else None
    if version:
        stem = stem[:version.start()] + "#" + stem[version.end():]
    return stem, marker


def version_kind(a: str, b: str) -> str | None:
    """Say whether the names themselves announce two generations of one document."""
    stem_a, ver_a = _stem_without_edition(Path(a).name)
    stem_b, ver_b = _stem_without_edition(Path(b).name)
    if ver_a and ver_b and ver_a != ver_b and stem_a == stem_b:
        return "version-name"
    return None


def classify(a: str, b: str, records: dict[str, dict], near: float,
             lines: list[tuple[str, str]]) -> dict:
    ra, rb = records[a], records[b]
    inter = ra["shingles"] & rb["shingles"]
    union = ra["shingles"] | rb["shingles"]
    overlap = len(inter) / len(union) if union else 0.0
    same_bytes = ra["bytes"] == rb["bytes"]
    superset_of = None
    if ra["lineset"] != rb["lineset"]:
        if ra["lineset"] <= rb["lineset"]:
            superset_of = b
        elif rb["lineset"] <= ra["lineset"]:
            superset_of = a
    if overlap >= 0.999:
        state = "identical-text"
    elif superset_of is not None and overlap >= 0.5:
        state = "superset"
    elif overlap >= near:
        state = "near-identical"
    elif overlap >= 0.5:
        state = "shared-text"
    else:
        state = "candidate-only"
    declared_by = declaration_for(a, b, lines)
    kind = None
    if declared_by:
        kind = declared_by["kind"]
    elif version_kind(a, b):
        kind = version_kind(a, b)
        declared_by = {"kind": kind, "file": None, "line": None}
    return {
        "a": a, "b": b,
        "overlap": round(overlap, 4),
        "sharedShingles": len(inter),
        "unionShingles": len(union),
        "sameBytes": same_bytes,
        "tokens": [ra["tokens"], rb["tokens"]],
        "lines": [ra["lines"], rb["lines"]],
        "supersetOf": superset_of,
        "state": state,
        "declared": kind is not None,
        "declaration": declared_by,
    }


def audit(root: Path, min_words: int = 200, near: float = 0.9) -> dict:
    records = fingerprint(root, min_words)
    lines = declaration_lines(records)
    pairs = [classify(a, b, records, near, lines) for a, b in sorted(candidate_pairs(records))]
    pairs = [p for p in pairs if p["state"] != "candidate-only"]
    pairs.sort(key=lambda p: (-p["overlap"], p["a"], p["b"]))
    by_state: dict[str, int] = {}
    undeclared = []
    for pair in pairs:
        by_state[pair["state"]] = by_state.get(pair["state"], 0) + 1
        if pair["state"] == "identical-text" and not pair["declared"]:
            undeclared.append({"a": pair["a"], "b": pair["b"], "overlap": pair["overlap"]})
    return {
        "schemaVersion": SCHEMA_VERSION,
        "authorityId": AUTHORITY_ID,
        "root": ".",
        "scope": {
            "markdownFiles": len(iter_markdown(root)),
            "documentsCompared": len(records),
            "minWords": min_words,
            "shingleWords": SHINGLE,
            "signatureElements": SIGNATURE,
        },
        "totals": {
            "pairs": len(pairs),
            "byState": by_state,
            "identicalTextUndeclared": len(undeclared),
            "declared": sum(1 for p in pairs if p["declared"]),
            "undeclaredIdenticalPairs": undeclared,
        },
        "findings": pairs,
    }


def summary(report: dict) -> str:
    scope, totals = report["scope"], report["totals"]
    lines = [
        f"Documents compared: {scope['documentsCompared']} of {scope['markdownFiles']} Markdown files"
        f" (>= {scope['minWords']} words, {scope['shingleWords']}-word shingles)",
        "Pairs above 0.5 overlap: "
        + (", ".join(f"{k}={v}" for k, v in sorted(totals["byState"].items())) or "none"),
        f"Declared: {totals['declared']}; identical text with no declaration:"
        f" {totals['identicalTextUndeclared']}",
    ]
    for pair in report["findings"]:
        mark = pair["declaration"]["kind"] if pair["declared"] else "UNDECLARED"
        lines.append(
            f"  {pair['overlap']:.3f} {pair['state']:15s} {mark:13s} {pair['a']} | {pair['b']}"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".")
    parser.add_argument("-o", "--output")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--check", action="store_true",
                        help="fail on an identical pair that nothing declares")
    parser.add_argument("--min-words", type=int, default=200)
    parser.add_argument("--near", type=float, default=0.9)
    parser.add_argument("--only", choices=("identical-text", "superset", "near-identical", "shared-text"))
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    report = audit(root, min_words=args.min_words, near=args.near)
    if args.only:
        report["findings"] = [p for p in report["findings"] if p["state"] == args.only]
    if args.output:
        Path(args.output).write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"wrote {args.output}", file=sys.stderr)
    if args.summary or not args.output:
        print(summary(report))
    if args.check and report["totals"]["identicalTextUndeclared"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
