"""Find (and optionally repair) dropped spaces in the Charnock corpus.

Someone ran a "compact the text" pass over this corpus at some point: spaces
between a number and a word, and after some punctuation, were deleted. The result
reads `Погребение30июля1680` and `книг:7объектов` — the records stay numerically
correct, which is why every existing validator passed, but the prose is damaged.

This script is a detector first and a repairer second:

    python3 scripts/audit_charnock_text_spacing.py                # report only
    python3 scripts/audit_charnock_text_spacing.py --dry-run      # show what would change

The two JSON files carry ~2300 derived hashes, and 123 of them pin rows that
live inside those same two files (`canonicalRowSha256` over a quotationPlan or
biographicalCoreReview row, and so on). wave45 repaired the JSON prose and
re-derived exactly those 123 pins, proving for every refreshed pin that the old
and new canonical bytes differ only in whitespace. Editing JSON values by hand
therefore means walking that graph; text-level `--apply` on a JSON file is
refused for that reason, and the value-level repair lives in
scripts/repair_charnock_json_prose_spacing.py. See
supplemental-audits/TEXT_SPACING_DEFECT_2026-11-16.md.

Two plan fields are byte-for-byte copies of `data/biographies-shared-atlas-v1.json`
shipped for other biographies, so they must stay verbatim: the scan excises them
and re-checks the equality instead of silently skipping them.

Repair is deliberately conservative: it only inserts a space, never deletes or
reorders characters, and it leaves anything that looks like a bibliographic or
scriptural reference alone (Psalm/Psalm-number forms, `p.265`, `vol.16`,
`§§21.138`, TCP ids such as `A71277`, `1Tim`-style Latin refs).
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "БИОГРАФИИ/Стивен Чарнок"
DATA_FILES = (
    "data/charnock-biographical-anchors-v1.json",
    "data/charnock-series-editorial-plan-v1.json",
)

# Scripture abbreviations that legitimately sit next to a chapter number: Пс32,
# Ин4, Рим3:9, 1Тим2:15. They are short and capitalised, so the lowercase-word
# rules below already skip them; they are listed to make the intent explicit.
SCRIPTURE = {
    "Пс", "Ин", "Рим", "Кор", "Лук", "Матф", "Мк", "Евр", "Откр", "Ис", "Иез",
    "Дан", "Ос", "Мих", "Авв", "Зах", "Мал", "Еф", "Флп", "Кол", "Тит", "Флм",
    "Иак", "Пет", "Иуд", "Суд", "Руф", "Езд", "Неем", "Есф", "Иов", "Притч",
    "Тим", "Флм", "Фес", "Гал", "Фил", "Еф",
    "Еккл", "Песн", "Плач", "Агг", "Соф", "Иоил", "Ам", "Авд", "Наум", "Соф",
}

# word directly before a number that is a reference marker, not a word needing a space
REF_WORDS = {"p", "pp", "vol", "vols", "no", "n", "ch", "chs", "f", "ff", "fol", "fols", "r", "v", "vv"}


ATLAS = ROOT / "data/biographies-shared-atlas-v1.json"
# (json file, dotted path inside it, key it must equal verbatim inside the atlas)
VERBATIM_SNAPSHOTS = (
    ("data/charnock-series-editorial-plan-v1.json", "routingReview.excludedLinksSnapshot", "excludedLinks"),
    ("data/charnock-series-editorial-plan-v1.json", "routingReview.edgeBoundarySnapshot", "edges"),
)


def text_for_scan(path: Path, report: dict, atlas_override: dict | None = None) -> str:
    """Read a corpus file, excising the subtrees that must stay verbatim.

    The two excluded snapshot fields are copies of a shared atlas file that other
    biographies also consume, so reflowing them would break the plan's own
    equality pin. They are excised only after the copy is re-verified: an
    exemption that no longer matches the atlas fails the audit instead of
    hiding a defect.
    """
    text = path.read_text(encoding="utf-8")
    name = str(path.relative_to(ROOT)).replace(os.sep, "/")
    rules = [r for r in VERBATIM_SNAPSHOTS if r[0] == name]
    if not rules:
        return text
    atlas = atlas_override if atlas_override is not None else json.loads(ATLAS.read_text(encoding="utf-8"))
    data = json.loads(text)
    for _, dotted, atlas_key in rules:
        node = data
        for part in dotted.split("."):
            node = node[part]
        if node != atlas[atlas_key]:
            raise ValueError(f"verbatim snapshot drifted from the shared atlas: {dotted}")
        report["verbatimSnapshotsVerified"] = report.get("verbatimSnapshotsVerified", 0) + 1
        parent = data
        parts = dotted.split(".")
        for part in parts[:-1]:
            parent = parent[part]
        del parent[parts[-1]]
    return json.dumps(data, ensure_ascii=False, indent=2)


def corpus_files(scope: str = "all") -> list[Path]:
    """scope='documents' limits the scan to the 18 reader-facing volumes."""
    files = sorted(CORPUS.glob("*.md"))
    if scope == "all":
        files += [ROOT / name for name in DATA_FILES]
    return [f for f in files if f.is_file()]


DIGIT_THEN_WORD = re.compile(r"(\d{1,4})([а-яё]{3,})")
WORD_THEN_DIGIT = re.compile(r"([А-Яа-яЁё]{2,})(\d{1,4})(?![\wА-Яа-яЁё])")
# Cyrillic only: `Рим3:9` and `09:51:57Z` must survive, so a digit after the
# colon is never treated as a missing space.
PUNCT_THEN_CHAR = re.compile(r"([;:])([А-Яа-яЁё])")
# The same pass also swallowed the space after an em dash ("—16§21.109").
# En dashes are left alone: they carry ranges ("27–28 июля"), and a digit before
# the dash means a span ("1660—1680"), not a sentence break.
DASH_THEN_TOKEN = re.compile(r"(?<!\d)—(?=[0-9А-Яа-яЁё§])")
# Number glued to a Latin abbreviation ("79TCP/11XML") or to a section sign
# ("16§§21.10"). The lookbehind protects source ids whose letters come first
# (A71277, B02133), which must never be split.
UNIT_ABBREV = "TCP|XML|SVG|SHA"
DIGIT_THEN_ABBREV = re.compile(
    r"(?<![A-Za-zА-Яа-яЁё0-9§._%‑–\-])"      # never split §0AB, -4FW, %5BCG, 2026_60PLUS
    r"(\d{1,4})(" + UNIT_ABBREV + r")\b"
)
DIGIT_THEN_SECTION = re.compile(r"(?<![A-Za-zА-Яа-яЁё0-9§])(\d{1,3})(§+)")


def word_digit_is_reference(word: str) -> bool:
    """True when `word`+number is a reference form, not prose that lost a space.

    The detector and the repairer MUST share this: a repairer that inserts a
    space the detector never flagged quietly rewrites `1Тим2:15` into
    `1Тим 2:15`, and the post-repair scan cannot see it because it agrees with
    the detector by construction.
    """
    # The whitelist is the whole guard. A length heuristic ("short and
    # capitalised") looks tempting, but it also spares real prose defects such as
    # `Год1628`, `Том03`, `Все6` — sentence-initial words that lost their space.
    return word in SCRIPTURE or word.lower() in REF_WORDS


def _context(text: str, start: int, end: int, pad: int = 32) -> str:
    left = max(0, start - pad)
    right = min(len(text), end + pad)
    return text[left:right].replace("\n", "⏎")


def findings(text: str) -> list[dict]:
    out = []
    for kind, pattern in (
        ("digit_then_word", DIGIT_THEN_WORD),
        ("word_then_digit", WORD_THEN_DIGIT),
        ("punct_then_char", PUNCT_THEN_CHAR),
        ("digit_then_abbrev", DIGIT_THEN_ABBREV),
        ("digit_then_section", DIGIT_THEN_SECTION),
        ("dash_then_token", DASH_THEN_TOKEN),
    ):
        for match in pattern.finditer(text):
            if kind == "word_then_digit" and word_digit_is_reference(match.group(1)):
                continue
            out.append(
                {
                    "kind": kind,
                    "match": match.group(0),
                    "context": _context(text, match.start(), match.end()),
                }
            )
    return out


def propose(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Insert the missing spaces; returns the new text and the (before, after) list."""
    changes: list[tuple[str, str]] = []

    def digit_word(match: re.Match) -> str:
        changes.append((match.group(0), f"{match.group(1)} {match.group(2)}"))
        return f"{match.group(1)} {match.group(2)}"

    def word_digit(match: re.Match) -> str:
        word = match.group(1)
        if word_digit_is_reference(word):
            return match.group(0)
        changes.append((match.group(0), f"{word} {match.group(2)}"))
        return f"{word} {match.group(2)}"

    def punct_char(match: re.Match) -> str:
        changes.append((match.group(0), f"{match.group(1)} {match.group(2)}"))
        return f"{match.group(1)} {match.group(2)}"

    text = DIGIT_THEN_WORD.sub(digit_word, text)
    text = WORD_THEN_DIGIT.sub(word_digit, text)
    text = PUNCT_THEN_CHAR.sub(punct_char, text)

    def digit_abbrev(match: re.Match) -> str:
        changes.append((match.group(0), f"{match.group(1)} {match.group(2)}"))
        return f"{match.group(1)} {match.group(2)}"

    def digit_section(match: re.Match) -> str:
        changes.append((match.group(0), f"{match.group(1)} {match.group(2)}"))
        return f"{match.group(1)} {match.group(2)}"

    text = DIGIT_THEN_ABBREV.sub(digit_abbrev, text)
    text = DIGIT_THEN_SECTION.sub(digit_section, text)

    def dash_token(match: re.Match) -> str:
        changes.append((f"—{match.string[match.end()]}", f"— {match.string[match.end()]}"))
        return "— "

    text = DASH_THEN_TOKEN.sub(dash_token, text)
    return text, changes


def scan(scope: str = "all") -> dict:
    report = {"scope": scope, "files": {}, "totalFindings": 0, "byKind": {}}
    for path in corpus_files(scope):
        text = text_for_scan(path, report)
        hits = findings(text)
        if not hits:
            continue
        kinds: dict[str, int] = {}
        for hit in hits:
            kinds[hit["kind"]] = kinds.get(hit["kind"], 0) + 1
            report["byKind"][hit["kind"]] = report["byKind"].get(hit["kind"], 0) + 1
        report["files"][str(path.relative_to(ROOT))] = {
            "count": len(hits),
            "byKind": kinds,
            "samples": hits[:5],
        }
        report["totalFindings"] += len(hits)
    report["state"] = "TEXT_SPACING_DEFECT_OPEN" if report["totalFindings"] else "TEXT_SPACING_CLEAN"
    return report


def apply(dry_run: bool, scope: str = "all") -> dict:
    summary = {"scope": scope, "files": {}, "totalInsertions": 0, "dryRun": dry_run}
    for path in corpus_files(scope):
        text = text_for_scan(path, summary)
        if path.suffix == ".json":
            if findings(text):
                raise ValueError(
                    f"{path.name} still has findings outside the verbatim snapshots; "
                    "repair JSON values with scripts/repair_charnock_json_prose_spacing.py, "
                    "never with a text-level --apply")
            continue
        fixed, changes = propose(text)
        if not changes:
            continue
        summary["files"][str(path.relative_to(ROOT))] = {
            "insertions": len(changes),
            "samples": changes[:5],
        }
        summary["totalInsertions"] += len(changes)
        if not dry_run:
            path.write_text(fixed, encoding="utf-8")
    summary["state"] = "TEXT_SPACING_REPAIRED" if not dry_run else "TEXT_SPACING_DRY_RUN"
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="count the repairs without writing")
    parser.add_argument("--apply", action="store_true", help="rewrite the corpus (requires --force)")
    parser.add_argument("--force", action="store_true", help="acknowledge that derived hashes will go stale")
    parser.add_argument("--fail-over", type=int, default=None, help="exit 1 when findings exceed N")
    parser.add_argument("--scope", choices=("all", "documents"), default="all",
                        help="documents = the 18 reader-facing volumes only (the two JSON files keep a known residue)")
    args = parser.parse_args()

    if args.apply and not args.force:
        parser.error("--apply would invalidate ~2900 derived hashes; pass --force only inside a hash-regeneration wave")
    if args.dry_run or args.apply:
        result = apply(dry_run=not args.apply, scope=args.scope)
    else:
        result = scan(scope=args.scope)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.fail_over is not None and result.get("totalFindings", 0) > args.fail_over:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
