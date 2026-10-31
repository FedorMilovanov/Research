#!/usr/bin/env python3
"""Pinned S1/TR/S7/S8 word-level controls. No manuscript/NA28 inference.

TR files use Robinson ASCII (theta=y, chi=c, final sigma=v). Comparison
normalizes this alphabet, Greek diacritics, case and punctuation; it is NOT
byte identity or a verdict about significant vs insignificant differences.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
sys.dont_write_bytecode = True
import unicodedata

from nt_sources import registry, witness_dir
from nt_refs import BOOKS, s1_sign_spans, s1_verses
from sbl_apparatus import Apparatus
from verify_nt_facts import OFFER_REFS

TR_CODES = ["MT", "MR", "LU", "JOH", "AC", "RO", "1CO", "2CO", "GA", "EPH",
            "PHP", "COL", "1TH", "2TH", "1TI", "2TI", "TIT", "PHM", "HEB",
            "JAS", "1PE", "2PE", "1JO", "2JO", "3JO", "JUDE", "RE"]
SUFFIX = {"S2": "SCV", "S3": "STV", "S4": "ELZ"}
GREEK_TO_ASCII = str.maketrans(dict(zip("αβγδεζηθικλμνξοπρστυφχψως", "abgdezhyiklmnxoprstufcqw s".replace(" ", ""))))
CONTROL_REFS = ["Мф 20:28", "Мф 26:28", "Мк 10:45", "Мк 14:24", "Ин 3:16",
                "Гал 1:4", "Деян 20:28", "Евр 2:9", "1 Тим 3:16", "1 Пет 3:18",
                "Откр 1:5", "Откр 5:9", "Откр 5:10"]


def greek_words(text: str) -> list[str]:
    decomposed = unicodedata.normalize("NFD", text.lower())
    bare = "".join(c for c in decomposed if not unicodedata.combining(c))
    return re.findall(r"[a-z]+", bare.translate(GREEK_TO_ASCII))


def parse_tr(text: str) -> dict[tuple[int, int], list[str]]:
    text = re.sub(r"\[[^\]]*\]", " ", text, flags=re.S)  # edition titles, not verse text
    marks = list(re.finditer(r"(?m)^\s*(\d+):(\d+)\s+", text))
    if not marks:
        raise ValueError("TR file has no verse markers")
    verses = {}
    for i, m in enumerate(marks):
        key = (int(m[1]), int(m[2]))
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        if key in verses:
            raise ValueError(f"duplicate TR verse marker: {key}")
        words = re.findall(r"[a-z]+", text[m.end():end].lower().replace("v", "s"))
        if not words:
            raise ValueError(f"empty TR verse: {key}")
        verses[key] = words
    return verses


def tr_verses(sid: str) -> dict[str, list[str]]:
    root = witness_dir(sid)
    result = {}
    for book, code in zip(BOOKS, TR_CODES):
        path = root / f"{code}.{SUFFIX[sid]}"
        for (ch, verse), words in parse_tr(path.read_text(encoding="utf-8-sig")).items():
            result[f"{book} {ch}:{verse}"] = words
    return result


def tregelles_controls() -> dict:
    codes = {"Мк": "Mark", "Гал": "Gal", "1 Пет": "1Pet", "Ин": "John", "Евр": "Heb"}
    verses = {}
    for line in (witness_dir("S8") / "TNT.txt").read_text().splitlines():
        m = re.match(r"(\w+)\.(\d+):(\d+)\s+(.+)$", line)
        if m:
            verses[f"{m[1]}.{m[2]}:{m[3]}"] = greek_words(m[4])
    result = {}
    for ref, phrase in {"Мк 14:24": "ὑπὲρ πολλῶν", "Гал 1:4": "περὶ τῶν ἁμαρτιῶν",
                        "1 Пет 3:18": "ἀπέθανεν", "Ин 3:16": "τὸν υἱὸν αὐτοῦ",
                        "Евр 2:9": "χάριτι θεοῦ"}.items():
        book, loc = ref.rsplit(" ", 1)
        key = f"{codes[book]}.{loc}"
        words = verses.get(key)
        if words is None:
            raise ValueError(f"S8 control verse missing: {key}")
        result[ref] = " " + " ".join(greek_words(phrase)) + " " in " " + " ".join(words) + " "
    return result


def computed_variants() -> dict:
    s1 = {ref: greek_words(" ".join(r[5] for r in rows)) for ref, rows in s1_verses().items()}
    tr = {sid: tr_verses(sid) for sid in SUFFIX}
    app = Apparatus()
    matrix = {}
    for ref in sorted(set(OFFER_REFS + CONTROL_REFS)):
        if ref not in s1 or any(ref not in data for data in tr.values()):
            raise ValueError(f"critical TR comparison verse missing: {ref}")
        matrix[ref] = {sid: s1[ref] == data[ref] for sid, data in tr.items()}
    controls = {"TR_Heb2_9_chariti": {sid: " cariti yeou " in " " + " ".join(data["Евр 2:9"]) + " " for sid, data in tr.items()},
                "TR_Mark14_24_peri": {sid: "peri pollwn" in " ".join(data["Мк 14:24"]) for sid, data in tr.items()},
                "TR_Matt26_28_new_covenant": {sid: "ths kainhs diayhkhs" in " ".join(data["Мф 26:28"]) for sid, data in tr.items()},
                "TR_1Tim3_16_theos": {sid: "yeos efanerwyh" in " ".join(data["1 Тим 3:16"]) for sid, data in tr.items()},
                "TR_Acts20_28_theos": {sid: "tou yeou" in " ".join(data["Деян 20:28"]) for sid, data in tr.items()},
                "S7_Heb2_9_explicit_readings": [{"wit": rd["wit"], "text": rd["text"]} for e in app.at("Евр 2:9") for rd in e["rdg"]],
                "S8_Tregelles": tregelles_controls()}
    for key, value in controls.items():
        if key != "S7_Heb2_9_explicit_readings" and not all(value.values()):
            raise ValueError(f"positive variant control failed: {key}: {value}")
    if any("NA" in rd["wit"] for rd in controls["S7_Heb2_9_explicit_readings"]):
        raise ValueError("Hebrews 2:9 S7 control changed: NA is explicitly cited")
    na_readings = [(e["lem"], rd["text"]) for entries in app.entries.values()
                   for e in entries for rd in e["rdg"] if "NA" in rd["wit"]]
    na_equal = sum(greek_words(lem) == greek_words(text) for lem, text in na_readings)
    verses = s1_verses()
    sign_rows = {ref: (s1_sign_spans(rows), len(app.at(ref))) for ref, rows in verses.items()}
    sign_bad = sorted(ref for ref, (a, b) in sign_rows.items() if a != b)
    from tregelles_attribution import check_tregelles_attribution
    treg = check_tregelles_attribution()
    treg_pin = {"stats": treg["stats"], "total": treg["total"],
                "contentMismatchRefs": sorted(r[0] for r in treg["mismatches"] if r[3] == "содержательное"),
                "scope": "Атрибуция S7 изданиям против текста S8 (Tregelles); орфографический допуск, "
                         "артефакты деления стиха отделены от содержательных расхождений. Рукописей не касается."}
    sign_agreement = {"s1Positions": sum(a for a, _ in sign_rows.values()),
                      "s7Entries": sum(b for _, b in sign_rows.values()),
                      "versesCompared": len(sign_rows),
                      "versesAgreeing": len(sign_rows) - len(sign_bad),
                      "mismatches": sign_bad,
                      "scope": "Число помеченных позиций S1 (поле 4) против числа <app> S7 по стихам; "
                               "одиночные ⸀/⸁ и открывающие ⸂/⸄ считаются за одну позицию. "
                               "Не сверка чтений и не атрибуция рукописям."}
    return {"normalization": "Robinson ASCII, no accents/case/punctuation; whole word sequence, not byte identity",
            "TRMutualWordEquality": {ref: tr["S2"][ref] == tr["S3"][ref] == tr["S4"][ref] for ref in matrix},
            "NAReadingWordProbe": {"citedReadings": len(na_readings), "equalWords": na_equal,
                                   "unequalWords": len(na_readings) - na_equal,
                                   "scope": "Mechanical word-sequence comparison, not complete or certified NA27/NA28 divergence. Abbreviated readings need interpretation."},
            "wordEquality": matrix, "controls": controls,
            "offerEqualInAllThreeTR": sum(all(matrix[ref].values()) for ref in OFFER_REFS),
            "signAgreement": sign_agreement,
            "tregellesAttribution": treg_pin}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump", action="store_true", help="diagnostic, not a PASS receipt")
    args = parser.parse_args()
    actual = computed_variants()
    if args.dump:
        print(json.dumps(actual, ensure_ascii=False, indent=2))
        return 0
    if actual != registry()["verifiedVariantControls"]:
        print("FAIL: word-level variant controls differ from SSOT; use --dump")
        return 1
    print(f"PASS: {len(actual['wordEquality'])} S1/TR verse controls, explicit Heb 2:9 S7 attribution, 5 S8 controls, "
          f"{actual['tregellesAttribution']['total']} S7->S8 attribution checks")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
