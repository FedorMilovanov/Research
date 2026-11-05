#!/usr/bin/env python3
"""Read-only controls for the bounded John 11:52 commentator/patristic review.

Default: validate the frozen observations, scope, references and Git preimages.
--source-root: additionally replay actual pinned file bytes and selected extracts.
A rendered web observation is NOT an archived HTTP object. Neither mode measures
human reading, proves an interpretation, authenticates Cyril's fragments, or
approves publication. Full source files stay outside the Research checkout.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CONTROL = "ИСКУПЛЕНИЕ/evidence/source_controls_wave4_2026-11-03.json"
REPORT = "ИСКУПЛЕНИЕ/evidence/synchronization_2026-11-02.json"
TEI = {"t": "http://www.tei-c.org/ns/1.0"}
SOURCE_IDS = {"CALVIN", "ALFORD", "CHRYSOSTOM", "AUGUSTINE", "CYRIL-FRAGMENT"}
EXTRACT_IDS = {"CALVIN-11-MD", "CALVIN-1-MD", "CALVIN-10-16-MD", "CALVIN-10-26-MD",
               "CHRYSOSTOM-65-EN", "CHRYSOSTOM-65-LA", "AUGUSTINE-49-EN", "AUGUSTINE-49-LA"}
BASELINE = 'fae5cc5953265ec0872bdae19b004470b9eb7a76'
REQUIRED_REPAIRS = {'W4-F-DATA', 'W4-NT-DATA', 'W4-ROOT-DATA', 'W4-F05', 'W4-H11', 'W4-NT15', 'W4-P13', 'W4-F10', 'W4-NT09', 'W4-F08', 'W4-CLOCK', 'W4-N00', 'W4-S04', 'W4-P06', 'W4-F04', 'W4-ROOT00', 'W4-P18', 'W4-F00', 'W4-QMAP', 'W4-P04', 'W4-C25', 'W4-CALVIN'}
FILE_IDS = {'NPNF07-XML', 'REFORMED-README', 'CALVIN-README', 'CALVIN-SHELL', 'CALVIN-INDEX', 'CALVIN10-MD', 'NPNF-README', 'PL35-XML', 'SOTW-METADATA', 'CALVIN11-MD', 'CLIO-METADATA', 'NPNF07-TXT', 'PL35-README', 'NPNF14-XML', 'FIRST1K-CYRIL-METADATA', 'CLIO-MONTFAUCON', 'CALVIN1-MD', 'NPNF14-TXT'}
REQUIRED_REFS = {
    "CALVIN": {"CALVIN-11-WEB", "CALVIN-1-WEB", "CALVIN-10-WEB", "CALVIN-11-MD", "CALVIN-1-MD", "CALVIN-10-16-MD"},
    "ALFORD": {"ALFORD-11-WEB"},
    "CHRYSOSTOM": {"CHRYSOSTOM-65-EN", "CHRYSOSTOM-65-LA"},
    "AUGUSTINE": {"AUGUSTINE-49-EN", "AUGUSTINE-49-LA", "AUGUSTINE-49-WEB"},
    "CYRIL-FRAGMENT": {"CYRIL-7-WEB"},
}
WEB_ANCHORS = {
    "CALVIN-11-WEB": ("The cause and pledge of this unity was the death of Christ", "by election", "even before they are called", "manifested by faith"),
    "CALVIN-1-WEB": ("is occupied by the Jews", "Having been engrafted into Christ by faith", "in various respects", "the beginning of our adoption"),
    "CALVIN-10-WEB": ("not only does he point out", "the secret election of God", "the effectual calling", "when he regenerates by his Spirit"),
    "ALFORD-11-WEB": ("τασσόμενοι εἰς ζωὴν αἰώνιον", "John 1:12", "among all nations", "the addition of the Evangelist"),
    "AUGUSTINE-49-WEB": ("Hoc Evangelista addidit", "secundum praedestinationem", "neque oves eius, nec filii Dei adhuc erant, qui nondum crediderant"),
    "CYRIL-7-WEB": ("for all mankind", "by way of creation", "But Satan", "through faith into one fold, the Church", "FRAGMENTS WHICH ARE EXTANT", "T. Randell", "These have been omitted", "public domain"),
}
EXTRACT_ANCHORS = {
    "CALVIN-11-MD": ("by election", "manifested by faith"),
    "CALVIN-1-MD": ("is occupied by the Jews", "in various respects"),
    "CALVIN-10-16-MD": ("secret election of God", "effectual calling"),
    "CALVIN-10-26-MD": ("they are reprobate",),
    "CHRYSOSTOM-65-EN": ("from what was about to be", "one body", "delivered from the punishment to come"),
    "CHRYSOSTOM-65-LA": ("ex eo quod futurum erat", "a futuro supplicio liberati fideles sunt"),
    "AUGUSTINE-49-EN": ("predestination", "still unbelieving were as yet neither His sheep nor the children of God"),
    "AUGUSTINE-49-LA": ("secundum praedestinationem", "neque oves ejus, nec filii Dei adhuc erant, qui nondum crediderant"),
}


def norm(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).split())


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def text_hash(text: str) -> str:
    return sha256(text.encode("utf-8"))


def web_text(row: dict) -> str:
    return "\n\n".join(s["text"] for s in row["selections"])


def extract(raw: bytes, selector: dict) -> str:
    """Deterministic, declared transformations only; never rewrite source bytes."""
    text = raw.decode("utf-8")
    kind = selector["kind"]
    if kind == "lines":
        lines = text.splitlines()
        a, b = selector["firstLine"], selector["lastLine"]
        if not 1 <= a <= b <= len(lines):
            raise ValueError("invalid one-based inclusive line range")
        return norm("\n".join(lines[a - 1:b]))
    if kind == "calvin-comments":
        first, last = selector["firstVerse"], selector["lastVerse"]
        # The italic lemma distinguishes a comment from the preceding verse
        # quotation. In John 10:16 and 11:53 the verse number occurs twice.
        starts = list(re.finditer(rf"(?m)^\*\*{first}\.\*\*\s+\*", text))
        if len(starts) != 1 or last < first:
            raise ValueError("ambiguous Calvin comment start/range")
        start = starts[0].start()
        end = re.search(rf"(?m)^\*\*{last + 1}\.\*\*", text[start:])
        if end is None:
            raise ValueError("Calvin comment end missing")
        selected = text[start:start + end.start()]
        selected = re.sub(r"\[\^\d+\]", "", selected)
        return norm(selected.replace("*", ""))
    if kind == "montfaucon-homily-section":
        tree = ET.fromstring(raw)
        homs = tree.findall(f".//t:div[@n='{selector['homily']}']", TEI)
        if len(homs) != 1:
            raise ValueError("ambiguous Montfaucon homily")
        sections = homs[0].findall(f"t:div[@n='{selector['section']}']", TEI)
        if len(sections) != 1:
            raise ValueError("ambiguous Montfaucon section")
        return norm("".join(sections[0].itertext()))
    if kind == "augustine-49-fragment":
        # The whole PL35 XML is malformed at 1551:17. This strictly parsed
        # bounded fragment does not pretend to repair/parse the whole object.
        before, after = '<title type="sub">TRACTATUS XLIX.</title>', '<title type="sub">TRACTATUS L.</title>'
        if text.count(before) != 1 or text.count(after) != 1:
            raise ValueError("ambiguous PL35 tractate boundary")
        a = text.index("</ab>", text.index(before)) + len("</ab>")
        b = text.rfind("<ab>", a, text.index(after))
        if b <= a:
            raise ValueError("invalid PL35 fragment boundary")
        fragment = ET.fromstring('<fragment xmlns="http://www.tei-c.org/ns/1.0">' + text[a:b] + '</fragment>')
        paragraphs = [norm("".join(p.itertext())) for p in fragment.findall("t:p", TEI)]
        # The OCR misnumbers the earlier Martha paragraph as 25 as well.
        # Select by number AND incipit; do not silently renumber either one.
        starts = [i for i, p in enumerate(paragraphs) if p.startswith("25. Multi ergo ex Judaeis")]
        if len(starts) != 1:
            raise ValueError("ambiguous PL35 49.25 incipit")
        selected = paragraphs[starts[0]:starts[0] + 4]
        if len(selected) != 4 or not all(re.match(rf"{n}\s*\.", p) for n, p in zip(range(25, 29), selected)):
            raise ValueError("PL35 49.25-28 sequence missing")
        return norm(" ".join(selected))
    raise ValueError(f"unsupported extractor: {kind}")


def check_controls(root: Path, report: dict, control: dict) -> list[str]:
    errors = []
    wave = report.get("wave4", {})
    if wave.get("controls") != CONTROL or wave.get("publicationEligible") is not False or wave.get("baselineCommit") != BASELINE:
        errors.append("wave4: journal/control boundary missing")
    for field in ("fullCorpusReadingClaimed", "wholeWorksRead", "printedCollationClaimed",
                  "allAuthorConsensusClaimed", "publicationEligible", "rawWebHtmlReceived"):
        if control.get(field) is not False:
            errors.append(f"wave4: overclaim/missing boundary {field}")
    policy = json.loads((root / "data/repository-evidence-policy-v2.json").read_text(encoding="utf-8"))
    sources = control.get("sources", [])
    if len(sources) != len(SOURCE_IDS) or {s.get("id") for s in sources} != SOURCE_IDS:
        errors.append("wave4: missing/duplicate commentator source")
    for source in sources:
        for field, allowed in (("evidenceClass", policy["sourceClasses"]), ("accessState", policy["accessStates"]),
                               ("locatorState", policy["locatorStates"]), ("rightsState", policy["rightsStates"]),
                               ("publicationState", policy["publicationStates"])):
            if source.get(field) not in allowed:
                errors.append(f"wave4: {source.get('id')} invalid independent axis {field}")
        if source.get("publicationState") != "BLOCKED" or not source.get("readingScope") or not source.get("version"):
            errors.append(f"wave4: {source.get('id')} scope/version/publication boundary")
        if source.get("quoteSafe") and (source.get("evidenceClass") not in ("A1", "A2", "A3") or
                                       source.get("locatorState") != "EXACT_LOCATOR_VERIFIED" or
                                       source.get("contextVerified") is not True or not source.get("quoteSafeScope")):
            errors.append(f"wave4: {source.get('id')} unbounded quote-safe claim")
        if source.get("id") == "CYRIL-FRAGMENT":
            if (source.get("attribution") != "PUBLISHED_UNDER_CYRIL_NOT_INDEPENDENTLY_AUTHENTICATED" or
                source.get("textCompleteness") != "EXTANT_FRAGMENT" or source.get("originalGreekRead") is not False or
                source.get("universalFinalSalvationProved") is not False or source.get("targetPageMarkers") != "133-134"):
                errors.append("wave4: Cyril fragment/attribution/faith/page boundary lost")
        if source.get("id") == "CHRYSOSTOM" and source.get("originalGreekRead") is not False:
            errors.append("wave4: Latin translation must not be reported as Greek verification")
    files = control.get("files", [])
    file_ids = [f.get("id") for f in files]
    if len(file_ids) != len(FILE_IDS) or set(file_ids) != FILE_IDS:
        errors.append("wave4: empty/duplicate file pins")
    for f in files:
        for key, length in (("commit", 40), ("gitBlob", 40), ("sha256", 64)):
            if not re.fullmatch(rf"[0-9a-f]{{{length}}}", f.get(key, "")):
                errors.append(f"wave4: {f.get('id')} invalid {key}")
        if not isinstance(f.get("bytes"), int) or f["bytes"] < 1 or not f.get("byteVerifiedAtUtc"):
            errors.append(f"wave4: {f.get('id')} missing actual byte receipt")
        rel = Path(f.get("externalRelativePath", ""))
        if rel.is_absolute() or ".." in rel.parts or str(rel) == ".":
            errors.append(f"wave4: unsafe external source path {rel}")
        expected_url = f"https://github.com/{f.get('repo')}/blob/{f.get('commit')}/"
        if not f.get("sourceUrl", "").startswith(expected_url):
            errors.append(f"wave4: {f.get('id')} URL/pin mismatch")
    extracts = control.get("extracts", [])
    if len(extracts) != len(EXTRACT_IDS) or {x.get("id") for x in extracts} != EXTRACT_IDS:
        errors.append("wave4: missing/duplicate bounded file extract")
    for x in extracts:
        if x.get("sourceFile") not in file_ids or text_hash(x.get("text", "")) != x.get("textSha256"):
            errors.append(f"wave4: {x.get('id')} extract identity/hash mismatch")
        for needle in EXTRACT_ANCHORS.get(x.get("id"), ()):
            if norm(needle).casefold() not in norm(x.get("text", "")).casefold():
                errors.append(f"wave4: {x.get('id')} critical text missing: {needle}")
    observations = control.get("webObservations", [])
    if len(observations) != len(WEB_ANCHORS) or {x.get("id") for x in observations} != set(WEB_ANCHORS):
        errors.append("wave4: missing/duplicate rendered web observation")
    for x in observations:
        if (x.get("rawHtmlReceived") is not False or x.get("hashScope") != "CAPTURED_SELECTED_RENDERED_PROSE_ONLY" or
            x.get("rawObjectSha256") is not None or x.get("fetchTimestampUtc") is not None):
            errors.append(f"wave4: {x.get('id')} rendered excerpt promoted to HTTP bytes")
        body = web_text(x)
        if text_hash(body) != x.get("textSha256") or not x.get("contextRead") or not x.get("version"):
            errors.append(f"wave4: {x.get('id')} web capture hash/context/version missing")
        for needle in WEB_ANCHORS.get(x.get("id"), ()):
            if norm(needle) not in norm(body):
                errors.append(f"wave4: {x.get('id')} critical web text missing: {needle}")
    known = set(file_ids) | EXTRACT_IDS | set(WEB_ANCHORS)
    for source in sources:
        refs = set(source.get("evidenceRefs", []))
        if not refs or refs - known or not REQUIRED_REFS.get(source.get("id"), set()) <= refs:
            errors.append(f"wave4: {source.get('id')} dangling/missing primary evidence references")
        if source.get("evidenceClass") != "A1":
            errors.append(f"wave4: {source.get('id')} own-text source role changed")
        if source.get("id") == "CALVIN" and (source.get("originalLanguageRead") is not False or source.get("independentMirrorsClaimed") is not False):
            errors.append("wave4: Calvin original-language/mirror independence overclaim")
    if control.get("pl35WholeDocumentParse") != {"status": "FAIL", "line": 1551, "column": 17, "sourceRepaired": False, "scopedFragmentParse": "PASS"}:
        errors.append("wave4: malformed whole XML must remain distinct from valid scoped fragment")
    if control.get("calvinDigitalDefect", {}).get("originAssignedToAIConversion") is not False:
        errors.append("wave4: repeated Jews defect not established as an AI-conversion error")
    time = control.get("timeProvenance", {})
    if time.get("moscowJustificationWithdrawn") is not True or time.get("historicalUtcInstantsRetained") is not True:
        errors.append("wave4: historical timezone provenance correction lost")
    repairs = {r["id"]: r for r in report.get("repairs", []) if r["id"].startswith("W4-")}
    if set(repairs) != REQUIRED_REPAIRS or set(wave.get("repairIds", [])) != REQUIRED_REPAIRS:
        errors.append("wave4: repair coverage mismatch")
    snapshots = wave.get("supersededSnapshots", [])
    paths = [s.get("path") for s in snapshots]
    if len(paths) != len(set(paths)) or {r["file"] for r in repairs.values()} - set(paths):
        errors.append("wave4: missing/duplicate pre-edit snapshots")
    baseline_texts = {}
    for snap in snapshots:
        if snap.get("commit") != wave.get("baselineCommit"):
            errors.append("wave4: preimage baseline mismatch")
            continue
        spec = f"{snap['commit']}:{snap['path']}"
        got = subprocess.run(["git", "show", spec], cwd=root, capture_output=True, check=False)
        if got.returncode or sha256(got.stdout) != snap.get("sha256") or git_blob(got.stdout) != snap.get("blob") or len(got.stdout) != snap.get("bytes"):
            errors.append(f"wave4: Git preimage byte mismatch: {snap['path']}")
        else:
            baseline_texts[snap["path"]] = got.stdout.decode("utf-8")
    for repair in repairs.values():
        was_present = repair["removed"] in baseline_texts.get(repair["file"], "")
        expected_type = "BASELINE_REMOVAL_OR_EXPLICIT_SUPERSESSION" if was_present else "ADDITIVE_GUARD_NOT_A_HISTORICAL_QUOTE"
        if repair.get("rejectedWordingPresentInBaseline") is not was_present or repair.get("controlType") != expected_type:
            errors.append(f"wave4: {repair['id']} invented historical-removal claim")
    # These new card records, unlike untouched legacy cards, have a scoped
    # source owner. Check the link, not just the presence of another A1 label.
    fathers = json.loads((root / "ИСКУПЛЕНИЕ/fathers/data/fathers-corpus-v1.json").read_text(encoding="utf-8"))
    by_source = {s["id"]: s for s in sources}
    for cid, sid in (("CHR-2", "CHRYSOSTOM"), ("AUG-2", "AUGUSTINE"), ("CYRA-2", "CYRIL-FRAGMENT")):
        cards = [c for c in fathers["cards"] if c["cardId"] == cid]
        if len(cards) != 1 or sid not in by_source:
            errors.append(f"wave4: missing/duplicate bounded card {cid}")
            continue
        card, source = cards[0], by_source[sid]
        fields = ("evidenceClass", "accessState", "locatorState", "rightsState", "publicationState", "quoteSafe", "quoteSafeScope", "readingScope", "version", "contextVerified", "holds")
        if card.get("sourceControl") != CONTROL or card.get("sourceControlId") != sid or any(card.get(k) != source.get(k) for k in fields):
            errors.append(f"wave4: {cid} card/source scope mismatch")
    for lane in ("", "nt/", "fathers/"):
        name = "atonement" if not lane else lane.rstrip("/")
        data = json.loads((root / f"ИСКУПЛЕНИЕ/{lane}data/{name}-corpus-v1.json").read_text(encoding="utf-8"))
        review = data.get("commentaryReviewWave4", {})
        if review.get("c25") != "OPEN" or review.get("controls") != CONTROL or review.get("publicationEligible") is not False:
            errors.append(f"wave4: {name} machine review drift")
    ledger = (root / "ИСКУПЛЕНИЕ/synthesis/02_CONFLICT_LEDGER.md").read_text(encoding="utf-8")
    c25 = re.search(r"(?ms)^## C-25\b.*?(?=^## |\Z)", ledger)
    if c25 is None or not re.search(r"\*\*Статус:\*\*\s*`OPEN`", c25.group()):
        errors.append("wave4: C25 cannot silently become closed")
    return errors


def verify_sources(source_root: Path, control: dict) -> list[str]:
    """No network, writes, source repair, or acceptance of a missing file."""
    errors, raw_by_id = [], {}
    base = source_root.resolve()
    for f in control["files"]:
        path = (base / f["externalRelativePath"]).resolve()
        if not path.is_relative_to(base):
            errors.append(f"wave4 replay: unsafe source path {path}")
            continue
        try:
            raw = path.read_bytes()
        except OSError as exc:
            errors.append(f"wave4 replay: {f['id']}: {exc}")
            continue
        if len(raw) != f["bytes"] or sha256(raw) != f["sha256"] or git_blob(raw) != f["gitBlob"]:
            errors.append(f"wave4 replay: file bytes changed: {f['id']}")
            continue
        raw_by_id[f["id"]] = raw
    for item in control["extracts"]:
        if item["sourceFile"] not in raw_by_id:
            errors.append(f"wave4 replay: {item['id']} unavailable verified source")
            continue
        try:
            got = extract(raw_by_id[item["sourceFile"]], item["selector"])
        except (ValueError, ET.ParseError, UnicodeError) as exc:
            errors.append(f"wave4 replay: {item['id']} extraction failed: {exc}")
            continue
        if got != item["text"] or text_hash(got) != item["textSha256"]:
            errors.append(f"wave4 replay: extract differs: {item['id']}")
    if "PL35-XML" in raw_by_id:
        try:
            ET.fromstring(raw_by_id["PL35-XML"])
        except ET.ParseError as exc:
            if exc.position != (1551, 17):
                errors.append(f"wave4 replay: unexpected whole-PL35 parse failure: {exc}")
        else:
            errors.append("wave4 replay: expected malformed PL35 silently changed/repaired")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--source-root", type=Path, help="external pinned-file directory; optional actual byte/extract replay")
    args = ap.parse_args()
    try:
        control = json.loads((args.root / CONTROL).read_text(encoding="utf-8"))
        report = json.loads((args.root / REPORT).read_text(encoding="utf-8"))
        errors = check_controls(args.root, report, control)
        replay_errors = verify_sources(args.source_root, control) if args.source_root else []
        errors += replay_errors
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"WAVE4 SOURCES: FAIL — {exc}")
        return 1
    print(json.dumps({"filePins": len(control["files"]), "fileExtracts": len(control["extracts"]),
                      "renderedWebObservations": len(control["webObservations"]),
                      "sourceByteReplay": ("FAIL" if replay_errors else "PASS") if args.source_root else "NOT_RUN",
                      "webHttpReplay": "NOT_AVAILABLE_RENDERED_OBSERVATIONS_ONLY", "printedCollation": False,
                      "humanReadingMeasured": False, "publicationApproved": False}, ensure_ascii=False))
    for error in errors:
        print("FAIL:", error)
    print("WAVE4 SOURCES: " + ("FAIL" if errors else "PASS — bounded controls, not complete works or doctrinal closure"))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
