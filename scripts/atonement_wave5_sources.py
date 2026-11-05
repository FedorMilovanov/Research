#!/usr/bin/env python3
"""Read-only Cyril/Johannine continuation controls (not a theological verdict).

Default verifies retained selections, source axes, boundaries and Git preimages.
--source-root additionally verifies FOUR actual pinned files, eleven Greek
context extractions and two whole-file lexical queries. It does NOT replay the
old 80/18-file packages or Prokopenko PDF, archive web HTTP, measure human reading,
authenticate Cyril's fragments, collate print/manuscripts or approve publication.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess

from atonement_wave3_sources import morphgnt_words
from atonement_wave4_sources import norm, sha256, git_blob, text_hash, web_text

ROOT = Path(__file__).resolve().parents[1]
CONTROL = "ИСКУПЛЕНИЕ/evidence/source_controls_wave5_2026-11-03.json"
REPORT = "ИСКУПЛЕНИЕ/evidence/synchronization_2026-11-02.json"
BASELINE = "1bb400f890b610cf1b5d282a7e5c910749537974"
RANGES = (
    ("JN1", "NT-JOHN", 1, 9, 18), ("JN5", "NT-JOHN", 5, 24, 29),
    ("JN8", "NT-JOHN", 8, 31, 47), ("JN10A", "NT-JOHN", 10, 11, 18),
    ("JN10B", "NT-JOHN", 10, 22, 30), ("JN11", "NT-JOHN", 11, 45, 57),
    ("JN12", "NT-JOHN", 12, 20, 36), ("JN17", "NT-JOHN", 17, 6, 26),
    ("1JN2", "NT-1JOHN", 2, 28, 29), ("1JN3", "NT-1JOHN", 3, 1, 10),
    ("1JN5", "NT-1JOHN", 5, 1, 5),
)
FILE_IDS = {"NT-JOHN", "NT-1JOHN", "PY-SBLGNT-README", "FIRST1K-CYRIL-METADATA"}
SOURCES = {
    "JOHANNINE-TEXT": {x[0] for x in RANGES} | {"NT-JOHN", "NT-1JOHN", "PY-SBLGNT-README"},
    "CYRIL-CONTEXTS": {"CYRIL-JN1", "CYRIL-JN8", "CYRIL-JN10"},
    "CYRIL-FRAGMENT-REVIEW": {"CYRIL-JN11-44", "CYRIL-JN11-52"},
}
WEB_ANCHORS = {
    "CYRIL-JN1": ("the whole world is God's own", "For since they received the Son through faith",
                   "For being partakers of Him through the Spirit", "we adopted by His Kindness",
                   "baptized into nought originate", "not by grace alone"),
    "CYRIL-JN8": ("we must not think that all the Jews", "it will not harmonize so to understand it here",
                   "for all are of God, both bad and good", "Consents, believes and lays up in his mind"),
    "CYRIL-JN10": ("who remains outside the fold?", "We say in reply", "pitying our fallen nature in its entirety",
                    "they will go down into Hades", "yet is not the same thing to all",
                    "let any one who can do so think out the more perfect meaning",
                    "united into one flock with the obedient of Israel", "and had not risen again"),
    "CYRIL-JN11-44": ("every one will be set free", "not under the dominion of sin",
                       "with a confession of faith"),
    "CYRIL-JN11-52": ("for all mankind", "by way of creation", "through faith into one fold, the Church"),
}
FALSE_BOUNDARIES = ("fullCorpusReadingClaimed", "wholeWorksRead", "printedCollationClaimed",
                    "cyrilOriginalGreekRead", "rawWebHtmlReceived", "publicationEligible",
                    "lexicalCountsProveInterpretation", "wholeCyrilEschatologySettled",
                    "punishmentDurationSettled", "universalFinalSalvationProved",
                    "creationAlternativeErased", "allKinshipSensesIdentical")
REPAIR_SUFFIXES = {"NT15", "C25", "H11", "P13", "NT09", "QMAP", "CALVIN", "F05", "F08", "F10",
                   "P04", "P06", "P18", "S04", "N00", "F00", "ROOT00", "NT-DATA", "F-DATA", "ROOT-DATA", "S-DATA"}
REQUIRED_REPAIRS = {"W5-" + s for s in REPAIR_SUFFIXES}


def context(words: dict, chapter: int, first: int, last: int) -> list[dict]:
    prefixes = {ref[:2] for ref in words}
    if len(prefixes) != 1 or not 1 <= first <= last or chapter < 1:
        raise ValueError("ambiguous book or invalid verse range")
    prefix = next(iter(prefixes))
    return [{"ref": f"{prefix}{chapter:02}{v:02}",
             "text": norm(" ".join(w["text"] for w in words[f"{prefix}{chapter:02}{v:02}"]))}
            for v in range(first, last + 1)]


def context_text(verses: list[dict]) -> str:
    return "\n".join(v["ref"] + " " + v["text"] for v in verses)


def lexical_query(words: dict) -> dict:
    """One book, exact lemmas: τέκνον followed by optional ONE ὁ then θεός.
    Not all kinship vocabulary, diminutives, nonadjacent phrases or exegesis.
    Occurrences (not unique verses) preserve the two tokens in 1 John 3:10.
    """
    hits, construction = [], []
    for ref, verse in words.items():
        for i, w in enumerate(verse):
            if w["lemma"] != "τέκνον":
                continue
            hits.append(ref)
            j = i + 1
            if j < len(verse) and verse[j]["lemma"] == "ὁ":
                j += 1
            if j < len(verse) and verse[j]["lemma"] == "θεός":
                construction.append(ref)
    return {"parsedVerses": len(words), "teknonOccurrences": hits, "childrenOfGodOccurrences": construction}


def check_controls(root: Path, report: dict, control: dict) -> list[str]:
    errors = []
    wave = report.get("wave5", {})
    if (wave.get("controls") != CONTROL or wave.get("baselineCommit") != BASELINE or
            wave.get("publicationEligible") is not False or wave.get("mergePerformed") is not False):
        errors.append("wave5: journal/control/merge boundary")
    for key in FALSE_BOUNDARIES:
        if control.get(key) is not False:
            errors.append(f"wave5: missing/overclaimed boundary {key}")
    if control.get("c25") != "OPEN" or control.get("interpretationStatus") != "ARGUED_PROVISIONAL_NOT_MACHINE_PROOF":
        errors.append("wave5: C25/preference cannot become doctrinal closure")
    policy = json.loads((root / "data/repository-evidence-policy-v2.json").read_text())
    axes = {"evidenceClass": "sourceClasses", "accessState": "accessStates", "locatorState": "locatorStates",
            "rightsState": "rightsStates", "publicationState": "publicationStates"}
    sources = control.get("sources", [])
    if len(sources) != len(SOURCES) or {s.get("id") for s in sources} != set(SOURCES):
        errors.append("wave5: source profiles missing/duplicate")
    for source in sources:
        for axis, vocab in axes.items():
            if source.get(axis) not in policy[vocab]:
                errors.append(f"wave5: invalid source axis {source.get('id')}/{axis}")
        if (source.get("publicationState") != "BLOCKED" or "PUBLICATION_HOLD" not in source.get("holds", []) or
                not source.get("version") or not source.get("readingScope") or not source.get("quoteSafeScope") or
                source.get("evidenceClass") != "A1" or source.get("contextVerified") is not True or
                source.get("locatorState") != "EXACT_LOCATOR_VERIFIED"):
            errors.append(f"wave5: scope/version/quote/publication boundary {source.get('id')}")
        if set(source.get("evidenceRefs", [])) != SOURCES.get(source.get("id")):
            errors.append("wave5: missing/dangling source evidence references")
        if source.get("id", "").startswith("CYRIL") and source.get("originalGreekRead") is not False:
            errors.append("wave5: English Cyril promoted to Greek")
        if source.get("id") == "CYRIL-FRAGMENT-REVIEW" and (
                source.get("textCompleteness") != "EXTANT_FRAGMENT" or
                source.get("attribution") != "PUBLISHED_UNDER_CYRIL_NOT_INDEPENDENTLY_AUTHENTICATED"):
            errors.append("wave5: Cyril fragment/attribution boundary")
        if source.get("id") == "CYRIL-CONTEXTS" and source.get("textCompleteness") != "SELECTED_CONTINUOUS_COMMENTARY_CONTEXTS":
            errors.append("wave5: Book VII fragment status must not be transferred to Books I/VI")
        if source.get("id") == "JOHANNINE-TEXT" and (source.get("rightsState") != "STORAGE_ONLY" or source.get("eulaNewlyRead") is not False):
            errors.append("wave5: README license statement is not new EULA/publication approval")
    files = control.get("files", [])
    if len(files) != len(FILE_IDS) or {f.get('id') for f in files} != FILE_IDS:
        errors.append("wave5: missing/duplicate file pins")
    for f in files:
        for key, size in (("commit", 40), ("gitBlob", 40), ("sha256", 64)):
            if not re.fullmatch(rf"[a-f0-9]{{{size}}}", f.get(key, "")):
                errors.append(f"wave5: invalid pin {key}")
        rel = Path(f.get("externalRelativePath", ""))
        if rel.is_absolute() or ".." in rel.parts or str(rel) == ".":
            errors.append("wave5: unsafe source path")
        if (type(f.get("bytes")) is not int or f["bytes"] < 1 or not f.get("byteVerifiedAtUtc") or
                f.get("sourceUrl") != f"https://github.com/{f.get('repo')}/blob/{f.get('commit')}/{f.get('path')}"):
            errors.append("wave5: incomplete actual byte receipt")
    extracts = control.get("greekContexts", [])
    expected_ranges = {x[0]: x[1:] for x in RANGES}
    if len(extracts) != len(RANGES) or {x.get("id") for x in extracts} != set(expected_ranges):
        errors.append("wave5: missing/duplicate Greek context")
    for x in extracts:
        if (x.get("sourceFile"), x.get("chapter"), x.get("firstVerse"), x.get("lastVerse")) != expected_ranges.get(x.get("id")):
            errors.append("wave5: Greek context range drift")
        verses = x.get("verses", [])
        spec = expected_ranges.get(x.get("id"))
        if spec:
            sid, ch, first, last = spec
            prefix = {"NT-JOHN": "04", "NT-1JOHN": "23"}[sid]
            if [v.get("ref") for v in verses] != [f"{prefix}{ch:02}{v:02}" for v in range(first, last + 1)]:
                errors.append("wave5: Greek verse coverage drift")
        if text_hash(context_text(verses)) != x.get("textSha256") or not verses or any(not v.get("text") for v in verses):
            errors.append("wave5: Greek context hash/empty")
    greek_by_ref = {v["ref"]: v["text"] for x in extracts for v in x.get("verses", [])}
    for ref, phrase in {
        "040112": "τέκνα θεοῦ γενέσθαι", "040113": "ἀλλ’ ἐκ θεοῦ ἐγεννήθησαν",
        "040529": "εἰς ἀνάστασιν κρίσεως", "040842": "Εἰ ὁ θεὸς πατὴρ ὑμῶν ἦν",
        "041016": "ἄλλα πρόβατα ἔχω", "041232": "πάντας ἑλκύσω",
        "041720": "τῶν πιστευόντων διὰ τοῦ λόγου αὐτῶν", "230302": "νῦν τέκνα θεοῦ ἐσμεν",
        "230310": "καὶ τὰ τέκνα τοῦ διαβόλου", "230501": "ἐκ τοῦ θεοῦ γεγέννηται",
    }.items():
        if phrase not in greek_by_ref.get(ref, ""):
            errors.append("wave5: critical Greek control lost: " + ref)
    # Whole-file queries are frozen mechanical observations, not reading counts.
    expected_lexical = {
        "NT-JOHN": {"parsedVerses": 866, "teknonOccurrences": ["040112", "040839", "041152"], "childrenOfGodOccurrences": ["040112", "041152"]},
        "NT-1JOHN": {"parsedVerses": 105, "teknonOccurrences": ["230301", "230302", "230310", "230310", "230502"], "childrenOfGodOccurrences": ["230301", "230302", "230310", "230502"]},
    }
    if control.get("lexicalResults") != expected_lexical or control.get("queryIsReading") is not False:
        errors.append("wave5: lexical scope/results/read distinction lost")
    observations = control.get("webObservations", [])
    if len(observations) != len(WEB_ANCHORS) or {x.get("id") for x in observations} != set(WEB_ANCHORS):
        errors.append("wave5: missing/duplicate rendered observation")
    for x in observations:
        if (x.get("rawHtmlReceived") is not False or x.get("rawObjectSha256") is not None or
                x.get("fetchTimestampUtc") is not None or x.get("hashScope") != "CAPTURED_SELECTED_RENDERED_PROSE_ONLY"):
            errors.append("wave5: rendered selection promoted to raw HTTP")
        body = web_text(x)
        if text_hash(body) != x.get("textSha256") or not x.get("contextRead"):
            errors.append("wave5: web hash/context missing")
        for phrase in WEB_ANCHORS.get(x.get("id"), ()):
            if norm(phrase) not in norm(body):
                errors.append(f"wave5: critical selection lost: {x.get('id')}: {phrase}")
        if x.get("id") == "CYRIL-JN10":
            roles = {s["id"]: s.get("voice") for s in x["selections"]}
            if roles.get("WHO-OUTSIDE-OBJECTION") != "OBJECTION_REPORTED" or roles.get("REPLY-ALL-NOT-SAME") != "AUTHOR_REPLY":
                errors.append("wave5: objection must not become Cyril's unqualified answer")
    discovery = control.get("greekCyrilDiscovery", {})
    if (discovery.get("metadataWork") != "In XII Prophetas" or discovery.get("scope") != "ONLY_PINNED_TLG4090_TREE" or
            discovery.get("johnGreekAcquired") is not False or discovery.get("globalAbsenceClaimed") is not False):
        errors.append("wave5: Prophets metadata is not John or global Greek absence")
    repairs = {r["id"]: r for r in report.get("repairs", []) if r["id"].startswith("W5-")}
    if set(repairs) != REQUIRED_REPAIRS or set(wave.get("repairIds", [])) != REQUIRED_REPAIRS:
        errors.append("wave5: repair coverage mismatch")
    snapshots, baseline_texts = wave.get("supersededSnapshots", []), {}
    paths = [s.get("path") for s in snapshots]
    if len(paths) != len(set(paths)) or {r["file"] for r in repairs.values()} - set(paths):
        errors.append("wave5: missing/duplicate baseline snapshots")
    for snap in snapshots:
        if snap.get("commit") != BASELINE:
            errors.append("wave5: wrong preimage baseline")
            continue
        proc = subprocess.run(["git", "show", f"{BASELINE}:{snap['path']}"], cwd=root, capture_output=True)
        raw = proc.stdout
        if proc.returncode or (sha256(raw), git_blob(raw), len(raw)) != (snap.get("sha256"), snap.get("blob"), snap.get("bytes")):
            errors.append("wave5: preimage byte mismatch: " + snap['path'])
        else:
            baseline_texts[snap['path']] = raw.decode()
    for r in repairs.values():
        present = r["removed"] in baseline_texts.get(r["file"], "")
        kind = "BASELINE_REMOVAL_OR_EXPLICIT_SUPERSESSION" if present else "ADDITIVE_GUARD_NOT_A_HISTORICAL_QUOTE"
        if r.get("rejectedWordingPresentInBaseline") is not present or r.get("controlType") != kind:
            errors.append("wave5: invented historical error: " + r['id'])
    for lane, name in (("", "atonement"), ("nt/", "nt"), ("fathers/", "fathers"), ("synthesis/", "synthesis")):
        d = json.loads((root / f"ИСКУПЛЕНИЕ/{lane}data/{name}-corpus-v1.json").read_text())
        review = d.get("cyrilJohannineReviewWave5", {})
        if review.get("controls") != CONTROL or review.get("c25") != "OPEN" or review.get("publicationEligible") is not False:
            errors.append("wave5: machine review drift: " + name)
        if name == "fathers":
            cards = [c for c in d["cards"] if c["cardId"] == "CYRA-3"]
            source = next((s for s in sources if s.get("id") == "CYRIL-CONTEXTS"), {})
            fields = (*axes, "quoteSafeScope", "readingScope", "version", "contextVerified", "holds")
            if (len(cards) != 1 or cards[0].get("sourceControl") != CONTROL or
                    cards[0].get("sourceControlId") != "CYRIL-CONTEXTS" or any(cards[0].get(k) != source.get(k) for k in fields)):
                errors.append("wave5: CYRA-3 card/source mismatch")
    ledger = (root / "ИСКУПЛЕНИЕ/synthesis/02_CONFLICT_LEDGER.md").read_text()
    c25 = re.search(r"(?ms)^## C-25\b.*?(?=^## |\Z)", ledger)
    if not c25 or not re.search(r"\*\*Статус:\*\*\s*`OPEN`", c25.group()):
        errors.append("wave5: C25 cannot silently close")
    return errors


def verify_sources(source_root: Path, control: dict) -> list[str]:
    errors, raw_by_id = [], {}
    base = source_root.resolve()
    for f in control["files"]:
        path = (base / f["externalRelativePath"]).resolve()
        if not path.is_relative_to(base):
            errors.append("wave5 replay: unsafe source path")
            continue
        try:
            raw = path.read_bytes()
        except OSError as exc:
            errors.append(f"wave5 replay: {f['id']}: {exc}")
            continue
        if (len(raw), sha256(raw), git_blob(raw)) != (f["bytes"], f["sha256"], f["gitBlob"]):
            errors.append("wave5 replay: file bytes changed: " + f["id"])
            continue
        raw_by_id[f["id"]] = raw
    parsed = {}
    for sid in control.get("lexicalResults", {}):
        try:
            parsed[sid] = morphgnt_words(raw_by_id[sid], 8)
            if lexical_query(parsed[sid]) != control["lexicalResults"][sid]:
                errors.append("wave5 replay: lexical results differ: " + sid)
        except (ValueError, KeyError, UnicodeError) as exc:
            errors.append(f"wave5 replay: unavailable/invalid Greek source {sid}: {exc}")
    for x in control.get("greekContexts", []):
        try:
            got = context(parsed[x["sourceFile"]], x["chapter"], x["firstVerse"], x["lastVerse"])
            if got != x["verses"] or text_hash(context_text(got)) != x["textSha256"]:
                errors.append("wave5 replay: context differs: " + x["id"])
        except (ValueError, KeyError) as exc:
            errors.append(f"wave5 replay: unavailable context {x['id']}: {exc}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--source-root", type=Path)
    args = ap.parse_args()
    try:
        control = json.loads((args.root / CONTROL).read_text())
        report = json.loads((args.root / REPORT).read_text())
        errors = check_controls(args.root, report, control)
        replay = verify_sources(args.source_root, control) if args.source_root else []
        errors += replay
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("WAVE5 SOURCES: FAIL —", exc)
        return 1
    print(json.dumps({"filePins": len(control["files"]), "greekContexts": len(control["greekContexts"]),
                      "selectedVerses": sum(len(x["verses"]) for x in control["greekContexts"]),
                      "renderedObservations": len(control["webObservations"]),
                      "sourceByteReplay": ("FAIL" if replay else "PASS") if args.source_root else "NOT_RUN",
                      "rawWebReplay": "NOT_AVAILABLE", "humanReadingMeasured": False, "publicationApproved": False}))
    for e in errors:
        print("FAIL:", e)
    print("WAVE5 SOURCES: " + ("FAIL" if errors else "PASS — bounded controls; C25 OPEN"))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
