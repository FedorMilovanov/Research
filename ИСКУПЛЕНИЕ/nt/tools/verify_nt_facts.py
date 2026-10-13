#!/usr/bin/env python3
"""Recompute declared NT probes and narrow grammar facts, not theology.

A nearest inflected form/co-occurring lemma is a reproducible search probe,
NOT a dependency parse, a governed-case certificate or a proof of extent.
Text-Fabric empty forms can encode articles; lex_utf8 homographs need sp.tf.
"""
from __future__ import annotations

import argparse
import json
import hashlib
import sys
sys.dont_write_bytecode = True
from collections import Counter

from nt_sources import ROOT, registry
from nt_refs import s1_verses
from mt_lookup import MT
from mt_lxx_collation import LXX, LXX_ROOT, bare

VERBS = {"ἀποθνῄσκω", "δίδωμι", "παραδίδωμι", "τίθημι", "φείδομαι",
         "πάσχω", "σταυρόω", "προσφέρω", "λύω"}
OFFER_REFS = ["Мф 11:28", "Мф 22:3", "Мф 22:9", "Мф 22:14", "Мф 23:37",
              "Лк 13:34", "Лк 14:17", "Лк 14:23", "Лк 14:24", "Ин 5:40",
              "Ин 7:37", "Деян 13:46", "Деян 17:30", "Откр 22:17"]


def first_case(rows: list[list[str]], index: int) -> str:
    return next((r[2][4] for r in rows[index + 1:] if r[2][4] in "GNAD"), "NONE")


def computed_facts() -> dict:
    verses = s1_verses()
    rows = [r for rs in verses.values() for r in rs]
    total = Counter(r[7] for r in rows)
    preps = {p: dict(Counter(first_case(rs, i)
                            for rs in verses.values() for i, r in enumerate(rs)
                            if r[7] == p and r[1] == "P-"))
             for p in ("ὑπέρ", "ἀντί", "περί")}
    sin = 0
    for rs in verses.values():
        for i, r in enumerate(rs):
            if r[7] != "περί":
                continue
            for n in rs[i + 1:i + 5]:
                if n[1] == "P-":
                    break
                if n[7] == "ἁμαρτία" and n[2][4] == "G":
                    sin += 1
                    break
    l3 = {"ὑπέρ-tokens": sum(r[7] == "ὑπέρ" and r[1] == "P-" for r in rows),
          "ἀντί-tokens": total["ἀντί"], "ἀντί-governing-genitive": preps["ἀντί"].get("G", 0),
          "περί-tokens": total["περί"], "περί-genitive-of-hamartia": sin,
          "ὑπέρ-lemma": total["ὑπέρ"],
          "ὑπέρ-prepositional-P-": sum(r[7] == "ὑπέρ" and r[1] == "P-" for r in rows),
          "ὑπέρ-adverbial-D-2Co11:23": sum(r[7] == "ὑπέρ" and r[1] == "D-" for r in verses["2 Кор 11:23"]),
          "ὑπέρ-genitive-death/giving/offering-clauses": sum(
              r[7] == "ὑπέρ" and r[1] == "P-" and first_case(rs, i) == "G"
              for rs in verses.values() if {r[7] for r in rs} & VERBS for i, r in enumerate(rs)),
          "ἀντί-genitive": preps["ἀντί"].get("G", 0),
          "ἀντί-accusative": preps["ἀντί"].get("A", 0),
          "ἀντί-adverbial": sum(r[7] == "ἀντί" and r[1] != "P-" for r in rows)}
    l4 = {"πολύς-plural-forms": sum(r[7] == "πολύς" and r[2][5] == "P" for r in rows),
          "πολύς-plural-with-preceding-article": sum(
              r[7] == "πολύς" and r[2][5] == "P" and i > 0 and rs[i - 1][7] == "ὁ"
              for rs in verses.values() for i, r in enumerate(rs)),
          "κόσμος-in-John-gospel": sum(r[7] == "κόσμος" for ref, rs in verses.items() if ref.startswith("Ин ") for r in rs),
          "κόσμος-in-1John": sum(r[7] == "κόσμος" for ref, rs in verses.items() if ref.startswith("1 Ин ") for r in rs),
          "πᾶς-πάντες-surface-form": sum(r[5].casefold() == "πάντεσ" for r in rows),
          "πᾶς-πάντες-VPM": sum(r[7] == "πᾶς" and r[2][4:7] == "VPM" for r in rows),
          "πᾶς-πάντες-NPM": sum(r[7] == "πᾶς" and r[2][4:7] == "NPM" for r in rows),
          "πᾶς-with-ἄνθρωπος-verses": sum({"πᾶς", "ἄνθρωπος"} <= {r[7] for r in rs} for rs in verses.values()),
          "κόσμος-with-ὅλος-or-πᾶς-verses": sum("κόσμος" in {r[7] for r in rs} and bool({"ὅλος", "πᾶς"} & {r[7] for r in rs}) for rs in verses.values())}
    redemption = {"αἷμα", "λυτρόομαι", "λυτρωτής", "λύτρον", "λύτρωσις", "ἀντίλυτρον",
                  "ἀπολύτρωσις", "ἀγοράζω", "ἐξαγοράζω", "ἱλάσκομαι", "ἱλασμός", "ἱλαστήριον",
                  "καταλλάσσω", "καταλλαγή", "ἀποκαταλλάσσω"}
    lxx = LXX(LXX_ROOT)
    prefixes = {p: lxx.count_word(p) for p in
                ("ἱλαστηρι", "ἱλασμο", "ἱλασκ", "ἐξιλασκ", "ἐξιλασ", "καταλλασ", "καταλλαγ", "ἀπολυτρωσι", "ἀπολυτρωσ", "ἀγορα")}
    positive = {"Psalmi 24:11": "ἱλάσῃ", "Psalmi 78:9": "ἱλάσθητι",
                "Machabaeorum_ii 1:5": "καταλλαγείη", "Machabaeorum_ii 7:33": "καταλλαγήσεται",
                "Machabaeorum_ii 8:29": "καταλλαγῆναι",
                "Daniel_translatio_Graeca 4:30c": "ἀπολυτρώσεως"}
    found = {ref: word in lxx.verses.get(ref, []) for ref, word in positive.items()}
    if not all(found.values()):
        raise ValueError(f"positive LXX inflected-form controls failed: {found}")
    lxx_probes = {"prefixCounts": prefixes, "positiveInflectedForms": positive,
                  "simplexHilasNonNounTokens": sum(bare(w).startswith("ιλασ") and
                      not bare(w).startswith(("ιλασμο", "ιλαστηρ")) for ws in lxx.verses.values() for w in ws),
                  "scope": "Digital token/prefix counts in un-lemmatized S5, not complete lemma or semantic counts."}
    mt = MT()
    sp = mt._node_feature("sp.tf")
    articles = {}
    for ref in ("Isaiah 53:11", "Isaiah 53:12"):
        lo, hi = mt.slots[mt.by_ref[ref]]
        articles[ref] = sum(mt.lex.get(i) == "רב" and mt.lex.get(i - 1) == "ה"
                            and sp.get(i - 1) == "art" for i in range(lo, hi + 1))
    def tag(ref, word):
        return [r[2] for r in verses[ref] if r[5] == word]
    return {"derivedLexicalCounts": {"L3": l3, "L4": l4},
            "lxxProbes": lxx_probes,
            "bloodOwnCaseCounts": dict(Counter(r[2][4] for r in rows if r[7] == "αἷμα")),
            "prepositionNextInflectedCaseCounts": preps,
            "antiCausalFormulaCount": sum(r[7] == "ἀντί" and rs[i + 1][5] == "ὧν"
                                          for rs in verses.values() for i, r in enumerate(rs[:-1])),
            "offerSelectedVerses": len(OFFER_REFS),
            "offerSelectedVersesWithRedemptionLemma": sum(bool(redemption & {r[7] for r in verses[ref]}) for ref in OFFER_REFS),
            "grammar": {"Matthew11_28_deute_pos": [r[1] for r in verses["Мф 11:28"] if r[7] == "δεῦτε"],
                        "Matthew11_28_pantes_tags": tag("Мф 11:28", "πάντες"),
                        "John6_37_piAn_count": sum(r[5] == "πᾶν" for r in verses["Ин 6:37"]),
                        "Gal3_13_katara_tags": tag("Гал 3:13", "κατάρα"),
                        "Rev5_9_pas_lemma_count": sum(r[7] == "πᾶς" for r in verses["Откр 5:9"]),
                        "1John2_2_article_before_sins": sum(r[7] == "ἁμαρτία" and i > 0 and rs[i - 1][7] == "ὁ" for rs in [verses["1 Ин 2:2"]] for i, r in enumerate(rs)),
                        "1John4_10_article_before_sins": sum(r[7] == "ἁμαρτία" and i > 0 and rs[i - 1][7] == "ὁ" for rs in [verses["1 Ин 4:10"]] for i, r in enumerate(rs)),
                        "MT_Isa53_articles_before_rab": articles,
                        "MT_kpr_lex_utf8_by_sp": dict(Counter(sp.get(i) for i, lx in mt.lex.items() if lx == "כפר"))}}


def validate_states(data: dict) -> list[str]:
    policy = json.loads((ROOT / "data/repository-evidence-policy-v2.json").read_text())
    errors = []
    for row in data["textWitnesses"] + data["historicalControls"]:
        for field, enum in [("evidenceClass", "sourceClasses"), ("accessState", "accessStates"),
                            ("locatorState", "locatorStates"), ("rightsState", "rightsStates"),
                            ("publicationState", "publicationStates")]:
            if row.get(field) not in policy[enum]:
                errors.append(f"{row['id']}: invalid {field}: {row.get(field)}")
        if set(row["holds"]) - set(policy["holds"]):
            errors.append(f"{row['id']}: non-canonical HOLD")
        if row["publicationState"] != "BLOCKED":
            errors.append(f"{row['id']}: publication remains blocked in this research lane")
    for row in data["historicalControls"]:
        source = ROOT / row["localRecord"]
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != row["sha256OfLocalRecord"]:
            errors.append(f"{row['id']}: local historical record missing/drifted")
            continue
        text = " ".join(source.read_text().split())
        for article, excerpt in row["verifiedExcerpts"].items():
            if f"**ARTICLE {article}.**" not in text or excerpt not in text:
                errors.append(f"{row['id']}: article/excerpt unavailable: {article}")
    if set(data["holds"]) != set(policy["holds"]):
        errors.append("global NT HOLDs differ from canonical policy")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump", action="store_true", help="display recomputed facts without claiming PASS")
    args = parser.parse_args()
    data = registry()
    actual = computed_facts()
    if args.dump:
        print(json.dumps(actual, ensure_ascii=False, indent=2))
        return 0
    errors = validate_states(data)
    if actual != data["verifiedComputedFacts"]:
        errors.append("computed NT/MT facts differ from SSOT; use --dump for the full diagnostic")
    by_id = {x["id"]: x for x in data["lexicalFields"]}
    for fid, counts in actual["derivedLexicalCounts"].items():
        for key, count in counts.items():
            if by_id[fid]["computedCounts"].get(key) != count:
                errors.append(f"{fid}: {key}: registry != computed {count}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: canonical operational states, derived probes, 14 offer verses and narrow Greek/MT grammar facts")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
