#!/usr/bin/env python3
"""Scoped, read-only replay of the third atonement synchronization wave.

The committed controls are extracts, not complete source objects. Optional replay
checks externally held bytes before parsing. Neither matching an extract, counting
a lemma, nor acquiring a complete file certifies human reading of that file.
No network access or writes occur in this checker.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CONTROL = "ИСКУПЛЕНИЕ/evidence/source_controls_2026-11-03.json"
BASELINE = "fbd0ab4d937175bec1df8c89fecf57ff5d9ce3e1"
TEI = "{http://www.tei-c.org/ns/1.0}"
OSIS = "{http://www.bibletechnologies.net/2003/OSIS/namespace}"
MT_BOOKS = set("Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh Esth Job Ps Prov Eccl Song Isa Jer Lam Ezek Dan Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech Mal".split())
PINS = {
    "OpenGreekAndLatin/First1KGreek": "ed91552c52530c8f5a3ddf2dd767e899372a804c",
    "openscriptures/morphhb": "3d15126fb1ef74867fc1434be1942e837932691f",
    "openscriptures/HebrewLexicon": "21c9add13bc727d3a951361778e97e3ff7afd1ce",
    "nathans/lxx-swete": "26bad3eb42bba98471d154c954e36a6f30a0279d",
    "eliranwong/LXX-Swete-1930": "1d3efc3c63bd384a4f3f07ed37eef54b0d45ac33",
    "morphgnt/py-sblgnt": "904fed08a14bffea6e1776d8c4c3eeb7c6092688",
}

REQUIRED_FILES = {
    "gregory29", "gregory30", "athanasius", "isaiah-grc1", "isaiah-grc2", "isaiah-metadata",
    "eli/00-Swete_versification.csv", "eli/01-Swete_word_with_punctuations.csv", "eli/README.md",
    "swete/README.md", "swete/utils/build.sh", "swete/utils/convert-swete.py", "swete/data/48.Isaias.txt",
    "lexicon/HebrewStrong.xml",
} | {"mt/" + book for book in MT_BOOKS} | {
    f"nt/{number}-{book}-morphgnt.txt" for number, book in enumerate(
        "Mt Mk Lk Jn Ac Ro 1Co 2Co Ga Eph Php Col 1Th 2Th 1Ti 2Ti Tit Phm Heb Jas 1Pe 2Pe 1Jn 2Jn 3Jn Jud Re".split(), 61)
}
REQUIRED_EXTRACTS = {
    "gregory29-20", "gregory30-19", "gregory30-20", "gregory30-21",
    "athanasius-19", "athanasius-20", "athanasius-21", "athanasius-25",
    "nt-64-Jn-11-52", "mt-Hos-13-14", "mt-Amos-7-2",
    "mt-Ps-51-20", "mt-Ps-51-21", "eli-Ps-50-20", "eli-Ps-50-21",
    "isaiah-grc1-53-5", "isaiah-grc2-53-5", "s23-Isa-1-12",
}
REQUIRED_REPAIRS = {
    "W3-OT11", "W3-OT15", "W3-NT15", "W3-F10", "W3-F04", "W3-F09", "W3-F01", "W3-F06", "W3-F00",
    "W3-C25", "W3-H11", "W3-P13", "W3-NT09", "W3-QMAP", "W3-P06", "W3-P18", "W3-MATRIX-CODE",
    "W3-METRIC-GATES", "W3-MASS", "W3-MASS-README", "W3-MATRIX-AUDIT", "W3-P04", "W3-ROOT13",
    "W3-NT00", "W3-OT11-PROVENANCE", "W3-OT-DATA", "W3-F-DATA", "W3-NT-DATA", "W3-ROOT-DATA", "W3-INDEX",
    "W3-ROOT00", "W3-OT00", "W3-F-SUMMARY", "W3-OT-BIB", "W3-MASS-SEMANTICS",
    "W3-P04-LEXICAL", "W3-S04-QUEUE", "W3-AUDIT-QUEUE",
}
ENGINEERING_FILES = {"scripts/atonement_sync_check.py", "scripts/test_atonement_sync.py",
                     ".github/workflows/atonement-corpus-integrity.yml"}


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).split())


def tokens(text: str) -> list[str]:
    text = "".join(c for c in unicodedata.normalize("NFD", text)
                   if not unicodedata.combining(c)).lower().replace("ς", "σ")
    return re.findall(r"[^\W\d_]+", text)


def tei_body_text(element: ET.Element) -> str:
    """Exclude editorial notes/heads; retain the tail after excluded elements."""
    if element.tag.rsplit("}", 1)[-1] in {"note", "head"}:
        return ""
    return (element.text or "") + "".join(
        tei_body_text(child) + (child.tail or "") for child in element)


def unique(elements: list[ET.Element], label: str) -> ET.Element:
    if len(elements) != 1:
        raise ValueError(f"nonunique/missing {label}: {len(elements)}")
    return elements[0]


def tei_segment(raw: bytes, locator: dict) -> str:
    root = ET.fromstring(raw)
    body = unique(root.findall(".//" + TEI + "body"), "TEI body")
    node = body
    for level in ("chapter", "section", "verse"):
        if level in locator:
            node = unique([el for el in node.iter(TEI + "div")
                           if el.get("subtype") == level and el.get("n") == str(locator[level])],
                          f"TEI {level} {locator[level]}")
    return normalized(tei_body_text(node))


def osis_words(raw: bytes) -> dict[str, list[dict]]:
    result = {}
    for verse in ET.fromstring(raw).iter(OSIS + "verse"):
        ref = verse.get("osisID")
        if not ref or ref in result:
            raise ValueError(f"duplicate/missing OSIS verse: {ref}")
        # Direct verse words: ketiv, without the qere/editorial words in <note>.
        result[ref] = [{"text": "".join(w.itertext()).replace("/", ""),
                        "lemma": re.findall(r"\d+", w.get("lemma", "")),
                        "morph": w.get("morph", "")}
                       for w in verse if w.tag == OSIS + "w"]
    return result


def morphgnt_words(raw: bytes, columns: int = 8) -> dict[str, list[dict]]:
    if columns not in (7, 8):
        raise ValueError("MorphGNT schema must be explicitly 7 or 8 columns")
    result = {}
    for lineno, line in enumerate(raw.decode("utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) != columns or not re.fullmatch(r"\d{6}", fields[0]):
            raise ValueError(f"MorphGNT schema mismatch on line {lineno}")
        text, lemma = fields[columns - 4], fields[columns - 1]
        if not re.search(r"[α-ωΑ-Ω\u1f00-\u1fff]", text + lemma):
            raise ValueError(f"MorphGNT word/lemma columns are not Greek: {lineno}")
        result.setdefault(fields[0], []).append({"text": text, "lemma": lemma, "morph": fields[2]})
    if not result:
        raise ValueError("empty MorphGNT input")
    return result


def eli_verses(versification: bytes, word_file: bytes) -> dict[str, str]:
    words, boundaries = {}, []
    for line in word_file.decode("utf-8-sig").splitlines():
        if not line.strip():
            continue
        ident, word = line.split("\t", 1)
        ident = int(ident)
        if ident in words:
            raise ValueError(f"duplicate ELI token id {ident}")
        words[ident] = word
    for line in versification.decode("utf-8-sig").splitlines():
        if line.strip():
            ident, ref = line.split("\t", 1)
            boundaries.append((int(ident), ref))
    if not words or not boundaries:
        raise ValueError("empty ELI input")
    result = {}
    for i, (start, ref) in enumerate(boundaries):
        end = boundaries[i + 1][0] if i + 1 < len(boundaries) else max(words) + 1
        if start >= end or ref in result or any(k not in words for k in range(start, end)):
            raise ValueError(f"invalid ELI verse range: {ref}")
        # CSV stores token IDs, not zero-based positions in a Python list.
        result[ref] = normalized(" ".join(words[k] for k in range(start, end)))
    return result


def s23_verses(raw: bytes) -> dict[str, str]:
    """Read the derivative token-per-line format; it is not an independent witness."""
    result: dict[str, list[str]] = {}
    current = None
    for lineno, line in enumerate(raw.decode("utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        fields = line.split(maxsplit=1)
        if len(fields) != 2 or not re.fullmatch(r"\d+\.\d+\.\d+", fields[0]):
            raise ValueError(f"S23 format mismatch on line {lineno}")
        ref, word = fields
        if ref != current and ref in result:
            raise ValueError(f"noncontiguous S23 verse: {ref}")
        result.setdefault(ref, []).append(word)
        current = ref
    if not result:
        raise ValueError("empty S23 input")
    return {ref: normalized(" ".join(words)) for ref, words in result.items()}


def blob_hash(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def byte_errors(raw: bytes, pin: dict, label: str) -> list[str]:
    if (len(raw), blob_hash(raw), hashlib.sha256(raw).hexdigest()) != (
            pin["bytes"], pin["blob"], pin["sha256"]):
        return [f"source bytes/hash mismatch: {label}"]
    return []


def extract_control(row: dict, files: dict[str, bytes], parsed: dict | None = None) -> str:
    raw = files[row["file"]]
    kind, loc = row["kind"], row["locator"]
    if kind == "tei":
        return tei_segment(raw, loc)
    if parsed is None:
        parsed = {}
    key = (kind, row["file"], row.get("wordsFile"))
    if key not in parsed:
        if kind == "osis":
            parsed[key] = osis_words(raw)
        elif kind == "morphgnt":
            parsed[key] = morphgnt_words(raw)
        elif kind == "eli":
            parsed[key] = eli_verses(raw, files[row["wordsFile"]])
        elif kind == "s23":
            parsed[key] = s23_verses(raw)
        else:
            raise ValueError(f"unknown extract kind: {kind}")
    value = parsed[key][loc["verse"]]
    return normalized(" ".join(w["text"] for w in value)) if kind in {"osis", "morphgnt"} else value


def verify_external(control: dict, source_root: Path) -> list[str]:
    """Fail closed on missing or changed files, then replay all frozen controls."""
    errors, files = [], {}
    for ident, pin in control["files"].items():
        rel = Path(pin["localRelativePath"])
        if rel.is_absolute() or ".." in rel.parts:
            errors.append(f"unsafe source path: {ident}")
            continue
        path = source_root / rel
        if not path.is_file():
            errors.append(f"source object missing: {ident}")
            continue
        raw = path.read_bytes()
        problems = byte_errors(raw, pin, ident)
        errors += problems
        if not problems:
            files[ident] = raw
    if errors:
        return errors  # Do not parse unverified bytes.
    parsed = {}
    for row in control["extracts"]:
        try:
            observed = extract_control(row, files, parsed)
            if observed != row["text"]:
                errors.append(f"extract differs from pinned source: {row['id']}")
        except (ValueError, KeyError, ET.ParseError) as exc:
            errors.append(f"cannot replay extract {row['id']}: {exc}")
    for row in control["greekTokenCounts"]:
        observed = Counter(tokens(tei_segment(files[row["file"]], {})))
        if observed[tokens(row["token"])[0]] != row["count"]:
            errors.append(f"normalized author-body token count differs: {row['file']}/{row['token']}")
    mt_files = {Path(pin["path"]).stem: files[ident] for ident, pin in control["files"].items()
                if pin["repo"] == "openscriptures/morphhb" and pin["path"].startswith("wlc/")}
    if set(mt_files) != MT_BOOKS:
        errors.append("MT search inventory is not exactly 39 biblical books (exclude VerseMap.xml)")
    mt_words = {book: parsed.get(("osis", "mt/" + book, None)) or osis_words(raw)
                for book, raw in mt_files.items()}
    for row in control["mtLemmaSearches"]:
        hits = []
        for book in sorted(row["books"]):
            for ref, words in mt_words[book].items():
                hits.extend(ref for w in words if row["lemma"] in w["lemma"])
        if hits != row["occurrences"]:
            errors.append(f"MT lemma inventory differs: {row['id']}")
    nt_files = {ident: files[ident] for ident, pin in control["files"].items()
                if pin["repo"] == "morphgnt/py-sblgnt" and ident.startswith("nt/")}
    if len(nt_files) != 27:
        errors.append("NT lemma search needs exactly 27 pinned books")
    nt_words = {ident: parsed.get(("morphgnt", ident, None)) or morphgnt_words(raw)
                for ident, raw in nt_files.items()}
    for row in control["ntLemmaSearches"]:
        hits = []
        for ident in sorted(nt_words):
            for ref, words in nt_words[ident].items():
                hits.extend(ref for w in words if w["lemma"] == row["lemma"])
        if hits != row["occurrences"]:
            errors.append(f"NT lemma inventory differs: {row['lemma']}")
    return errors


def check_controls(root: Path, report: dict, control: dict) -> list[str]:
    """Offline integrity, explicitly NOT a new acquisition or source replay."""
    errors = []
    if control.get("fullCorpusReadingClaimed") is not False or control.get("printedCollationClaimed") is not False:
        errors.append("wave3 must not claim full-corpus reading/printed collation")
    policy = json.loads((root / "data/repository-evidence-policy-v2.json").read_text(encoding="utf-8"))
    axes = {"evidenceClass": "sourceClasses", "accessState": "accessStates", "locatorState": "locatorStates",
            "rightsState": "rightsStates", "publicationState": "publicationStates"}
    if set(control.get("repositoryPins", {})) != set(PINS) or control["repositoryPins"] != PINS:
        errors.append("wave3 repository pin inventory changed")
    if not REQUIRED_FILES <= set(control.get("files", {})):
        errors.append("wave3 source-file inventory lost a required pinned object")
    for ident, pin in control.get("files", {}).items():
        if pin.get("commit") != PINS.get(pin.get("repo")):
            errors.append(f"wrong source pin: {ident}")
        if (not re.fullmatch(r"[0-9a-f]{40}", str(pin.get("blob", "")))
                or not re.fullmatch(r"[0-9a-f]{64}", str(pin.get("sha256", "")))
                or type(pin.get("bytes")) is not int or pin["bytes"] <= 0):
            errors.append(f"incomplete byte receipt: {ident}")
        rel = Path(pin.get("localRelativePath", ""))
        if not pin.get("localRelativePath") or rel.is_absolute() or ".." in rel.parts:
            errors.append(f"unsafe source path: {ident}")
        if pin.get("url") != f"https://github.com/{pin.get('repo')}/blob/{pin.get('commit')}/{pin.get('path')}":
            errors.append(f"source URL is not bound to its pin: {ident}")
        for field, vocab in axes.items():
            if pin.get(field) not in policy[vocab]:
                errors.append(f"missing/noncanonical source axis {ident}/{field}")
        if pin.get("publicationState") != "BLOCKED":
            errors.append(f"source replay cannot authorize publication: {ident}")
    extracts = control.get("extracts", [])
    ids = [r["id"] for r in extracts]
    if len(ids) < 221 or len(ids) != len(set(ids)) or not REQUIRED_EXTRACTS <= set(ids):
        errors.append("missing/duplicate wave3 extracts or reduced scoped coverage")
    for row in extracts:
        if row["file"] not in control["files"] or not row.get("locator") or not row.get("text"):
            errors.append(f"unbound/empty wave3 extract: {row['id']}")
        if row.get("kind") == "eli" and row.get("wordsFile") not in control["files"]:
            errors.append(f"ELI word inventory not pinned: {row['id']}")
    by_id = {row["id"]: row for row in extracts}
    if "λυτρον" not in tokens(by_id.get("gregory30-20", {}).get("text", "")):
        errors.append("Gregory30.20 ransom control lost")
    for name in ("greekTokenCounts", "mtLemmaSearches", "ntLemmaSearches"):
        if not control.get(name):
            errors.append(f"wave3 search inventory lost: {name}")
    relations = control.get("sourceRelationships", [])
    if not any(r.get("source") == "swete/data/48.Isaias.txt" and r.get("relation") == "DERIVED_NOT_INDEPENDENT"
               for r in relations):
        errors.append("S23 derivative/independence boundary lost")
    web = control.get("webExcerpts", [])
    if {r.get("id") for r in web} != {"WEB-ISAIAS", "WEB-WESLEY", "WEB-GILL"}:
        errors.append("web observation inventory changed or missing")
    for row in web:
        for field, vocab in axes.items():
            if row.get(field) not in policy[vocab]:
                errors.append(f"noncanonical web source axis: {row.get('id')}/{field}")
        if (not row.get("excerpts") or not row.get("url") or not row.get("locator")
                or not row.get("acquisitionMethod") or row.get("rawObjectSha256") is not None
                or row.get("fullWorkReadingClaimed") is not False or row.get("publicationState") != "BLOCKED"):
            errors.append(f"web excerpt promoted to an unobserved archive/full reading/publication: {row.get('id')}")
    wave = report.get("wave3", {})
    if wave.get("controls") != CONTROL or not wave.get("readingScope"):
        errors.append("wave3 missing control pointer/scoped reading declaration")
    scope = wave.get("readingScope", {})
    if scope.get("fullCorpusReadingClaimed") is not False or scope.get("printedCollationClaimed") is not False:
        errors.append("wave3 reading scope promoted to full reading/printed collation")
    if wave.get("publicationEligible") is not False or wave.get("remoteWritesPerformed") is not False:
        errors.append("wave3 local research does not establish publication or a remote write")
    repair_ids = wave.get("repairIds", [])
    actual_repairs = {r["id"]: r for r in report.get("repairs", []) if r["id"].startswith("W3-")}
    if (not REQUIRED_REPAIRS <= set(repair_ids) or set(repair_ids) != set(actual_repairs)
            or len(repair_ids) != len(set(repair_ids))):
        errors.append("wave3 repair inventory lost or unbound")
    snapshots = wave.get("supersededSnapshots", [])
    if not ENGINEERING_FILES <= set(wave.get("engineeringChanges", [])):
        errors.append("wave3 engineering-change provenance lost")
    required_snapshots = {r['file'] for r in actual_repairs.values()} | ENGINEERING_FILES
    if required_snapshots - {p.get('path') for p in snapshots}:
        errors.append("wave3 repaired files lack baseline byte snapshots")
    if not snapshots or len({r["path"] for r in snapshots}) != len(snapshots):
        errors.append("wave3 missing/duplicate baseline snapshots")
    for pin in snapshots:
        if pin.get("commit") != BASELINE:
            errors.append(f"unexpected wave3 baseline: {pin.get('path')}")
            continue
        proc = subprocess.run(["git", "show", f"{BASELINE}:{pin['path']}"], cwd=root, capture_output=True)
        if proc.returncode:
            errors.append(f"wave3 historical bytes unavailable: {pin['path']}")
        else:
            errors += byte_errors(proc.stdout, pin, pin["path"])
    if wave.get("currentLocalPdfReplay") != "NOT_RUN_RAW_OBJECT_ABSENT":
        errors.append("wave3 must preserve the distinction from the historical wave2 PDF replay")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, help="externally held source-materials directory; no downloads")
    args = parser.parse_args()
    control = json.loads((ROOT / CONTROL).read_text(encoding="utf-8"))
    report = json.loads((ROOT / "ИСКУПЛЕНИЕ/evidence/synchronization_2026-11-02.json").read_text(encoding="utf-8"))
    errors = check_controls(ROOT, report, control)
    if args.source_root:
        errors += verify_external(control, args.source_root)
    print(json.dumps({"result": "FAIL" if errors else "PASS", "errors": errors,
                      "extracts": len(control["extracts"]), "sourceFiles": len(control["files"]),
                      "sourceReplay": "RUN" if args.source_root else "NOT_RUN",
                      "fullCorpusReading": False, "printedCollation": False}, ensure_ascii=False))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
