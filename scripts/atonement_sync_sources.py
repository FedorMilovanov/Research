#!/usr/bin/env python3
"""Pinned digital witnesses for the atonement synchronization, not a Bible edition.

Full sources/cache stay OUTSIDE the repository. --fetch downloads only explicitly
pinned GitHub archives; without it this program makes no network requests.
--freeze writes a SMALL, explicitly dated control set for marked draft quotations
and the Greek passages under review. --verify re-extracts those controls from the
source bytes and checks their hashes. Neither command validates an interpretation,
scans a printed edition, proves independence of witnesses, or authorizes Product use.

Example (cache outside Git):
  python3 -B scripts/atonement_sync_sources.py --cache /path/to/cache --fetch
  python3 -B scripts/atonement_sync_sources.py --cache /path/to/cache --verify
"""
from __future__ import annotations

import argparse
import hashlib
import html
import io
import json
import re
import tarfile
import urllib.request
from pathlib import Path

from atonement_draft_citation_audit import collect, parse_ref

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "ИСКУПЛЕНИЕ/evidence/source_controls_2026-11-02.json"
SOURCES = {
    "rst": ("onlydotbible/rst", "00ae4ffbd7a4ac1fb70ebb941109439316e4f5c9"),
    "rsb": ("trevarj/rsb", "9290a72a95c906fbc9e5e35339dd695bf565b521"),
    "py-sblgnt": ("morphgnt/py-sblgnt", "904fed08a14bffea6e1776d8c4c3eeb7c6092688"),
}
USFM = dict(zip(
    "gen exo lev num deu jos jdg rut 1sa 2sa 1ki 2ki 1ch 2ch ezr neh est job psa pro ecc sng isa jer lam ezk dan hos jol amo oba jon mic nam hab zep hag zec mal mat mrk luk jhn act rom 1co 2co gal eph php col 1th 2th 1ti 2ti tit phm heb jas 1pe 2pe 1jn 2jn 3jn jud rev".split(),
    "Быт Исх Лев Чис Втор Нав Суд Руф 1Цар 2Цар 3Цар 4Цар 1Пар 2Пар Езд Неем Есф Иов Пс Прит Еккл Песн Ис Иер Плач Иез Дан Ос Иоил Ам Авд Ион Мих Наум Ав Соф Аг Зах Мал Мф Мк Лк Ин Деян Рим 1Кор 2Кор Гал Еф Фил Кол 1Фес 2Фес 1Тим 2Тим Тит Флм Евр Иак 1Пет 2Пет 1Ин 2Ин 3Ин Иуд Откр".split(),
))
# RSB identifiers are matched by file stem, NOT by a presumed NT book order.
RSB_STEMS = dict(zip(
    "byt ish lev chis vtor isnav sud ruf 1tsar 2tsar 3tsar 4tsar 1par 2par ezd nee esf iov ps prit ekk pesn is ier plach iez dan os ioil amos avd iona mih naum avv sof agg zah mal mf mk lk in deyan rim 1kor 2kor gal ef fil kol 1fes 2fes 1tim 2tim tit filim evr iak 1petr 2petr 1in 2in 3in iud otkr".split(),
    USFM.values(),
))
GREEK_BOOKS = dict(zip(
    "Mt Mk Lk Jn Ac Ro 1Co 2Co Ga Eph Php Col 1Th 2Th 1Ti 2Ti Tit Phm Heb Jas 1Pe 2Pe 1Jn 2Jn 3Jn Jud Re".split(),
    "Мф Мк Лк Ин Деян Рим 1Кор 2Кор Гал Еф Фил Кол 1Фес 2Фес 1Тим 2Тим Тит Флм Евр Иак 1Пет 2Пет 1Ин 2Ин 3Ин Иуд Откр".split(),
))
# Local source review includes these contexts even when the draft uses a paraphrase.
EXTRA_RU = ["Наум 1:3", "Рим 3:24–26", "Рим 8:29–34", "Тит 2:11–15",
            "1 Тим 2:1–6", "1 Тим 4:10", "2 Пет 2:1", "Евр 2:9–14",
            "Евр 10:26–29", "Евр 10:38–39", "1 Пет 1:2", "Рим 15:16",
            "Ис 53:5–6", "Ис 53:12", "2 Кор 5:14–21", "Ин 3:16–17",
            "Еф 5:25–27", "Ин 10:14–18", "Ин 17:9", "Мф 1:21", "Рим 5:17–19",
            "Пс 48:8", "Пс 49:8", "Пс 129:8", "Тит 3:5–6", "Евр 9:12", "Евр 10:14"]
EXTRA_GR = ["1 Ин 2:1–2", "1 Ин 4:10", "Евр 9:5", "Рим 3:24–26", "Рим 8:32–34", "Рим 5:18–19",
            "Тит 2:11–15", "1 Тим 2:1–6", "1 Тим 4:10", "2 Пет 2:1",
            "Евр 2:9–13", "2 Кор 5:14–15"]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def put_verse(out: dict, key: tuple, text: str, source: str) -> None:
    if key in out:
        raise ValueError(f"duplicate verse {key} in {source}")
    out[key] = (text, source)


def parse_rst_book(text: str, book: str, source: str) -> dict:
    """Keep verse identity across RST paragraph/dialogue breaks; never overwrite."""
    verses, previous = {}, None
    for line in text.splitlines():
        m = re.fullmatch(r"#(\d+):(\d+)#(.*)", line)
        if not m:
            continue
        value = html.unescape(re.sub(r"<[^>]+>", "", m[3]))
        key = (book, int(m[1]), int(m[2]))
        if key == previous:
            verses[key] = (verses[key][0] + " " + value, source)
        else:
            put_verse(verses, key, value, source)
        previous = key
    return verses


def load_sources(cache: Path) -> dict:
    result = {name: {} for name in SOURCES}
    # Use the publisher's explicit USFM mapping; RST has Catholic epistles before Paul.
    description = (cache / "rst/parsed66/description.yaml").read_text(encoding="utf-8")
    pairs = re.findall(r"file: ([^\n]+)\n\s+usfm: (\S+)", description)
    if len(pairs) != 66 or {u for _, u in pairs} != set(USFM):
        raise ValueError("RST book manifest is not the expected 66-book mapping")
    for filename, usfm in pairs:
        rel = f"parsed66/{filename}"
        parsed = parse_rst_book((cache / "rst" / rel).read_text(encoding="utf-8"), USFM[usfm], rel)
        for key, (text, source) in parsed.items():
            put_verse(result["rst"], key, text, source)
    seen = set()
    for path in sorted((cache / "rsb").glob("*.txt")):
        abbr = RSB_STEMS.get(path.stem.split("_", 1)[1])
        if abbr is None:  # Noncanonical books, including Sirach's unnumbered prologue.
            continue
        if abbr in seen:
            raise ValueError(f"duplicate RSB book {abbr}")
        seen.add(abbr)
        chapter = None
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.fullmatch(r"=== (\d+) ===", line.strip())
            if m:
                chapter = int(m[1])
                continue
            m = re.fullmatch(r"(\d+) (.*)", line)
            if m:
                if chapter is None:
                    raise ValueError(f"verse without chapter in {path.name}")
                put_verse(result["rsb"], (abbr, chapter, int(m[1])), m[2], path.name)
    if seen != set(USFM.values()):
        raise ValueError("RSB 66-book mapping incomplete")
    for path in sorted((cache / "py-sblgnt/pysblgnt/sblgnt").glob("*-morphgnt.txt")):
        abbr = GREEK_BOOKS[path.name.split("-")[1]]
        rel = path.relative_to(cache / "py-sblgnt").as_posix()
        by_verse = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            cols = line.split()
            if len(cols) != 8:
                raise ValueError(f"unexpected MorphGNT schema: {path.name}")
            bcv = cols[0]
            key = (abbr, int(bcv[2:4]), int(bcv[4:6]))
            by_verse.setdefault(key, []).append(cols[4])  # text, not lemma or gloss
        for key, words in by_verse.items():
            # Remove apparatus markers only; preserve accents, words, punctuation.
            text = re.sub(r"[\u2e00-\u2e0d]", "", " ".join(words))
            put_verse(result["py-sblgnt"], key, text, rel)
    if len({b for b, _, _ in result["py-sblgnt"]}) != 27:
        raise ValueError("Greek witness is not complete for 27 books")
    return result


def fetch(cache: Path) -> None:
    for name, (repo, commit) in SOURCES.items():
        url = f"https://codeload.github.com/{repo}/tar.gz/{commit}"
        data = urllib.request.urlopen(url, timeout=90).read()
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
            for member in archive.getmembers():
                if not member.isfile():
                    continue
                rel = Path(*Path(member.name).parts[1:])
                if rel.is_absolute() or ".." in rel.parts:
                    raise ValueError(f"unsafe archive member {rel}")
                if name == "rst" and not (rel.parts[0] == "parsed66" or str(rel) == "README.md"):
                    continue
                target = cache / name / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.extractfile(member).read())
        print(f"fetched {repo}@{commit}")


def ref_keys(refs: list[str]) -> set[tuple]:
    result = set()
    for ref in refs:
        parsed = parse_ref(ref)
        if parsed is None:
            raise ValueError(f"unresolved quotation/control reference: {ref}")
        book, chapter, first, last = parsed
        result.update((book, chapter, v) for v in range(first, last + 1))
    return result


def controls(cache: Path, data: dict, date: str) -> dict:
    citations = collect(ROOT / "ИСКУПЛЕНИЕ/synthesis/drafts")
    ru_keys = ref_keys([r["ref_use"] for r in citations] + EXTRA_RU)
    gr_keys = ref_keys(EXTRA_GR)
    out = {
        "schemaVersion": 1, "asOf": date,
        "scope": "Digital verse controls, not full printed-edition verification or theological adjudication.",
        "independence": "RST describes Logos/RBO ancestry; RSB describes bible.by ancestry. Independence beyond those declarations is not proved. The 2026-10-30 bible.by checks are not a third independent witness to RSB.",
        "publicationEligible": False,
        "rightsNote": "Russian witness READMEs declare public-domain text. MorphGNT README distinguishes SBLGNT text terms from CC BY-SA 3.0 morphology. No complete source object is committed; Product rights are not cleared by this research control.",
        "sources": {},
    }
    for name, (repo, commit) in SOURCES.items():
        keys = gr_keys if name == "py-sblgnt" else ru_keys
        rows, files = [], {"README.md"}
        if name == "rst":
            files.add("parsed66/description.yaml")
        for key in sorted(keys):
            if key not in data[name]:
                raise ValueError(f"missing control {name}: {key}")
            text, filename = data[name][key]
            files.add(filename)
            rows.append({"book": key[0], "chapter": key[1], "verse": key[2],
                         "text": text, "sourceFile": filename})
        out["sources"][name] = {
            "repository": repo, "commit": commit,
            "url": f"https://github.com/{repo}/tree/{commit}",
            "evidenceClass": "A1",
            "evidenceClassScope": "Primary witness to the text of this digital transcription, not to its genealogy or a theological conclusion.",
            "accessState": "FULL_OBJECT_VERIFIED",
            "objectScope": "Pinned digital source tree acquired in full; retained source-file bytes are hashed. Not a claim to have read the entire Bible or inspected printed pages.",
            "locatorState": "EXACT_LOCATOR_VERIFIED",
            "locatorScope": "Verse and source path in the identified digital version only.",
            "rightsState": "RIGHTS_UNKNOWN",
            "rightsScope": "Upstream declarations are recorded above; separate corpus-specific Product clearance has not been established.",
            "publicationState": "BLOCKED",
            "publicationScope": "Product promotion is not authorized by this Research control.",
            "printedPageCheck": False,
            "files": {f: {"sha256": sha256((cache / name / f).read_bytes()),
                          "bytes": (cache / name / f).stat().st_size} for f in sorted(files)},
            "chapterVerseNumbers": {"Тит|2": sorted(v for b, c, v in data[name] if b == "Тит" and c == 2)},
            "verses": rows,
        }
    return out


def verify(cache: Path, data: dict, control: dict) -> None:
    for name, witness in control["sources"].items():
        if (witness["repository"], witness["commit"]) != SOURCES[name]:
            raise ValueError(f"source pin drift: {name}")
        for file, expected in witness["files"].items():
            raw = (cache / name / file).read_bytes()
            if sha256(raw) != expected["sha256"] or len(raw) != expected["bytes"]:
                raise ValueError(f"source bytes changed: {name}/{file}")
        for chapter_ref, expected in witness["chapterVerseNumbers"].items():
            book, chapter = chapter_ref.split("|")
            actual = sorted(v for b, c, v in data[name] if b == book and c == int(chapter))
            if actual != expected:
                raise ValueError(f"chapter inventory mismatch: {name}/{chapter_ref}")
        for row in witness["verses"]:
            key = (row["book"], row["chapter"], row["verse"])
            if data[name].get(key) != (row["text"], row["sourceFile"]):
                raise ValueError(f"source/control mismatch: {name}/{key}")
    print("SOURCE CONTROLS: PASS — pins, file bytes, verse text and source locations match")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cache", required=True, type=Path)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--freeze", action="store_true")
    ap.add_argument("--as-of", help="required with --freeze, YYYY-MM-DD")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--control", type=Path, default=CONTROL)
    args = ap.parse_args()
    cache = args.cache.resolve()
    if cache == ROOT or ROOT in cache.parents:
        ap.error("full sources must be cached outside the repository")
    if args.freeze and (not args.as_of or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.as_of)):
        ap.error("--freeze requires an explicit --as-of YYYY-MM-DD")
    if args.fetch:
        fetch(cache)
    data = load_sources(cache)
    for name in ("rst", "rsb"):
        lines = [f"{b}\t{c}\t{v}\t{text}" for (b, c, v), (text, _) in sorted(data[name].items())]
        (cache / f"{name}.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{name}: {len(lines)} verse records, parsed using explicit book identifiers")
    if args.freeze:
        payload = controls(cache, data, args.as_of)
        args.control.parent.mkdir(parents=True, exist_ok=True)
        args.control.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote explicit control snapshot: {args.control}")
    if args.verify:
        verify(cache, data, json.loads(args.control.read_text(encoding="utf-8")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
