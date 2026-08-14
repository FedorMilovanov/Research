#!/usr/bin/env python3
import argparse, copy, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
HANDOFF = ROOT / "product_handoff"

OVERRIDES = [
    "question-overrides-wave3e.json",
    "question-overrides-wave3g.json",
    "question-overrides-wave3k.json",
    "question-overrides-wave3l.json",
    "question-overrides-wave3n.json",
]
CAND_RE = re.compile(r"question-candidates-wave3-(\d{3})-(\d{3})\.json$")
PROTO_RE = re.compile(r"mcq-prototypes-wave3[jm]?-(\d{3})-(\d{3})\.json$")
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
LAYER_RE = re.compile(r"wave(3[a-z0-9]*)", re.I)

class AuditError(RuntimeError): pass

def load(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)

def fail(cond, msg):
    if cond:
        raise AuditError(msg)

def cid(rec):
    return rec.get("id") or rec.get("candidate_id") or rec.get("question_id")

def source_id(rec):
    return rec.get("source_id") or rec.get("id")

def layer_of(path):
    m = LAYER_RE.search(path.name)
    return m.group(1).lower() if m else "base"

def norm_scope(rec):
    return rec.get("inspection_scope") or rec.get("inspectionScope") or rec.get("inspection_level") or "UNSPECIFIED"

def norm_access(rec):
    return rec.get("access_state") or rec.get("accessState") or "UNSPECIFIED"

def norm_role(rec):
    return rec.get("source_role") or rec.get("role") or "UNSPECIFIED"

def norm_limit(rec):
    return rec.get("claim_limit") or rec.get("claimLimit") or ""

def author_from_title(title):
    if not title or "," not in title:
        return None
    head = title.split(",", 1)[0].strip()
    return head if 2 <= len(head) <= 100 else None

def year_from_title(title):
    m = YEAR_RE.search(title or "")
    return int(m.group()) if m else None

def read_candidates():
    files = sorted((p for p in DATA.glob("question-candidates-wave3-*.json") if CAND_RE.search(p.name)),
                   key=lambda p: int(CAND_RE.search(p.name).group(1)))
    fail(not files, "no current wave3 candidate batches")
    records, ranges = [], []
    for p in files:
        m = CAND_RE.search(p.name)
        lo, hi = map(int, m.groups())
        obj = load(p)
        batch = obj.get("candidates")
        fail(not isinstance(batch, list), f"{p.name}: candidates missing")
        declared = (obj.get("counts") or {}).get("records", obj.get("records"))
        if declared is not None:
            fail(declared != len(batch), f"{p.name}: declared count {declared} != {len(batch)}")
        fail(len(batch) != hi - lo + 1, f"{p.name}: filename range != record count")
        ranges.append((lo, hi, p.name))
        records.extend(batch)
    expected = 1
    for lo, hi, name in ranges:
        fail(lo != expected, f"candidate batch gap/overlap before {name}: expected {expected}, got {lo}")
        expected = hi + 1
    ids = [cid(r) for r in records]
    fail(any(x is None for x in ids), "candidate without ID")
    dup = [x for x, n in Counter(ids).items() if n > 1]
    fail(bool(dup), f"duplicate candidate IDs: {dup}")
    return records, files

def apply_overrides(base):
    effective = {cid(r): copy.deepcopy(r) for r in base}
    provenance = {}
    batches = [p for p in DATA.glob("question-candidates-wave3-*.json") if CAND_RE.search(p.name)]
    for r in base:
        n = int(cid(r).split("_")[-1])
        owner = next(p.name for p in batches if int(CAND_RE.search(p.name).group(1)) <= n <= int(CAND_RE.search(p.name).group(2)))
        provenance[cid(r)] = ["base:" + owner]
    upgraded = []
    for name in OVERRIDES:
        p = DATA / name
        fail(not p.exists(), f"missing override authority {name}")
        obj = load(p)
        ovs = obj.get("overrides")
        fail(not isinstance(ovs, list), f"{name}: overrides missing")
        seen = set()
        for ov in ovs:
            qid = cid(ov)
            fail(not qid or qid not in effective, f"{name}: orphan override {qid}")
            fail(qid in seen, f"{name}: duplicate override {qid}")
            seen.add(qid)
            fields = ov.get("supersedesFields") or ov.get("supersedes_fields")
            fail(not isinstance(fields, list) or not fields, f"{name}:{qid}: missing supersedesFields")
            old_status = effective[qid].get("status")
            for field in fields:
                fail(field not in ov, f"{name}:{qid}: supersedes {field} but value missing")
                effective[qid][field] = copy.deepcopy(ov[field])
            if "status" in fields and old_status == "HOLD" and effective[qid].get("status") != "HOLD":
                fail("source_minimum" not in ov, f"{name}:{qid}: HOLD upgrade without source_minimum provenance")
                fail(not ov.get("do_not_claim"), f"{name}:{qid}: HOLD upgrade without overclaim boundary")
                upgraded.append((qid, name, old_status, effective[qid].get("status")))
            provenance[qid].append("override:" + name)
    for qid, rec in effective.items():
        rec["_provenance"] = provenance[qid]
    return effective, upgraded

def read_sources():
    identity_lanes = defaultdict(list)
    inspection_lanes = defaultdict(list)
    files = sorted(DATA.glob("source-ledger-*.json")) + sorted(DATA.glob("source-quorum-*.json"))
    fail(not files, "no source ledgers/quorums")
    for p in files:
        obj = load(p)
        rows = obj.get("sources", [])
        fail(not isinstance(rows, list), f"{p.name}: sources is not a list")
        for row in rows:
            sid = source_id(row)
            fail(not sid, f"{p.name}: source without id")
            lane = {"path": str(p.relative_to(ROOT)), "layer": layer_of(p), "record": row}
            inspection_lanes[sid].append(lane)
            if p.name.startswith("source-ledger-"):
                identity_lanes[sid].append(lane)
    return identity_lanes, inspection_lanes

def claim_layer(rec):
    for item in reversed(rec["_provenance"]):
        if item.startswith("override:"):
            m = LAYER_RE.search(item)
            if m:
                return m.group(1).lower()
    return "base"

def choose_owner(rec, sid, identity_lanes, inspection_lanes):
    lanes = inspection_lanes.get(sid, [])
    fail(not lanes, f"{cid(rec)}: unresolved source id {sid}")
    target = claim_layer(rec)
    matching = [x for x in lanes if x["layer"] == target and "source-quorum-" in x["path"]]
    if len(matching) == 1:
        return matching[0], "MATCHING_OVERRIDE_QUORUM"
    fail(len(matching) > 1, f"{cid(rec)}:{sid}: multiple matching quorum owners")
    ledger = identity_lanes.get(sid, [])
    if len(ledger) == 1:
        return ledger[0], "BASE_LEDGER_NO_DEPTH_INHERITANCE"
    fail(len(ledger) > 1, f"{cid(rec)}:{sid}: multiple ledger owners")
    if len(lanes) == 1:
        return lanes[0], "SOLE_EXPLICIT_SOURCE_LANE"
    raise AuditError(f"{cid(rec)}:{sid}: ambiguous source owner lanes {[x['path'] for x in lanes]}")

def flags_for(rec):
    t = (rec.get("claim_type") or "").lower()
    tested = (rec.get("tested_distinction") or "").lower()
    ref = rec.get("reference") or ""
    src = " ".join(rec.get("source_minimum") or []).lower()
    flags = set()
    if t == "text": flags.add("DIRECT_TEXT")
    if t == "greek": flags.add("GREEK_FORM")
    if t == "greek" and any(k in tested for k in ("morph", "parse", "form", "participle")): flags.add("MORPHOLOGY")
    if any(k in tested for k in ("lex", "gloss", "semant")) or "lexicon" in src: flags.add("LEXICAL")
    if "/" in ref or any(k in tested for k in ("intertext", "quotation", "background", "lxx")): flags.add("INTERTEXT")
    if t == "history": flags.add("HISTORY")
    if t == "interpretation": flags.add("THEOLOGY")
    if rec.get("confidence") == "contested": flags.add("DISPUTED")
    if any(k in tested for k in ("variant", "apparatus", "textual")) or any(x in src for x in ("ecm_", "ntvmr")): flags.add("TEXTUAL_CRITICISM")
    if t == "application": flags.add("APPLICATION")
    return sorted(flags)

def domain_for(flags, rec):
    for x in ("TEXTUAL_CRITICISM","MORPHOLOGY","LEXICAL","INTERTEXT","HISTORY","THEOLOGY","APPLICATION","GREEK_FORM","DIRECT_TEXT"):
        if x in flags: return x
    return (rec.get("claim_type") or "UNKNOWN").upper()

def guard_policies():
    out = []
    for name in ("chapter4-guard-policy.json", "chapter5-guard-policy.json"):
        obj = load(HANDOFF / name)
        out.extend(obj.get("guard_records", []))
    return out

def guard_matches(g, rec):
    if g.get("candidate_id") and g["candidate_id"] != cid(rec): return False
    if g.get("match_reference") and g["match_reference"] != rec.get("reference"): return False
    if g.get("match_reference_prefix") and not (rec.get("reference") or "").startswith(g["match_reference_prefix"]): return False
    if g.get("match_claim_type") and g["match_claim_type"] != rec.get("claim_type"): return False
    return True

def inspection_for(rec, identity_lanes, inspection_lanes):
    rows = []
    for sid in rec.get("source_minimum") or []:
        owner, why = choose_owner(rec, sid, identity_lanes, inspection_lanes)
        s = owner["record"]
        rows.append({
            "source_id": sid,
            "evidence_status": norm_access(s),
            "inspection_scope": norm_scope(s),
            "owning_lane": owner["path"],
            "claim_limit": norm_limit(s),
            "owner_resolution": why,
        })
    fail(not rows, f"{cid(rec)}: no source_minimum")
    return rows

def exact_claim_ready(rows):
    bad_markers = ("catalog", "metadata", "abstract", "page_inspected", "unspecified", "link_only")
    for row in rows:
        scope = row["inspection_scope"].lower()
        status = row["evidence_status"].lower()
        if any(x in scope for x in bad_markers) or "catalog" in status or "link" in status:
            return False
        if not any(x in scope for x in ("exact_", "full_", "relevant_", "partial_text_inspected")):
            return False
    return True

def make_handoff(rec, inspection, guards):
    flags = flags_for(rec)
    project = rec.get("position") == "project"
    contested = rec.get("confidence") == "contested" or "DISPUTED" in flags
    safe = rec.get("keyed_concept") or rec.get("candidate_claim") or rec.get("candidate") or rec.get("stem")
    if project:
        safe = "COURSE POSITION ONLY: " + safe
    elif contested:
        safe = "CONTESTED / ATTRIBUTION REQUIRED: " + safe
    prohibited = [rec.get("do_not_claim")] if rec.get("do_not_claim") else []
    for g in guards:
        if guard_matches(g, rec) and g.get("prohibited_overclaim"):
            prohibited.append(g["prohibited_overclaim"])
    can_obj = (
        rec.get("position") == "neutral" and rec.get("confidence") == "high"
        and rec.get("status") == "READY" and rec.get("claim_type") in {"text","greek"}
        and not any(f in flags for f in ("DISPUTED","TEXTUAL_CRITICISM","HISTORY","THEOLOGY","APPLICATION","LEXICAL"))
    )
    strict_rank_inputs = can_obj and "DIRECT_TEXT" in flags and exact_claim_ready(inspection)
    return {
        "candidate_id": cid(rec),
        "verse": rec.get("reference"),
        "short_claim": rec.get("keyed_concept") or rec.get("stem"),
        "claim_type": rec.get("claim_type"),
        "domain": domain_for(flags, rec),
        "confidence": rec.get("confidence"),
        "position": rec.get("position"),
        "project": project,
        "contested": contested,
        "source_ids": list(rec.get("source_minimum") or []),
        "source_evidence": inspection,
        "inspection_scope": [x["inspection_scope"] for x in inspection],
        "owning_lane": [x["owning_lane"] for x in inspection],
        "product_safe_phrasing": safe,
        "prohibited_overclaim": prohibited,
        "can_author_objective_mcq": can_obj,
        "can_author_course_position_mcq": project and rec.get("status") != "HOLD",
        "ranking_possible": False,
        "ranking_discrepancy_candidate": bool(strict_rank_inputs),
        "rationale": "Research READY is not product or ranking approval; permissions are bounded by position, confidence, claim type, owning-lane depth, and explicit overclaim guards.",
        "flags": flags,
        "effective_status": rec.get("status"),
        "effective_competitive_candidate": bool(rec.get("competitive_candidate")),
        "provenance": rec["_provenance"],
    }

def read_prototypes():
    files = sorted(p for p in DATA.glob("mcq-prototypes-wave3*-*.json") if PROTO_RE.search(p.name))
    rows = []
    for p in files:
        batch = load(p).get("prototypes")
        fail(not isinstance(batch, list), f"{p.name}: prototypes missing")
        rows.extend(copy.deepcopy(batch))
    ids = [x.get("prototype_id") for x in rows]
    fail(any(x is None for x in ids), "prototype without id")
    dup = [x for x,n in Counter(ids).items() if n > 1]
    fail(bool(dup), f"duplicate prototype IDs: {dup}")
    byid = {x["prototype_id"]: x for x in rows}
    op = DATA / "mcq-prototype-overrides-wave3j2.json"
    if op.exists():
        for ov in load(op).get("overrides", []):
            pid = ov.get("prototype_id")
            fail(pid not in byid, f"orphan prototype override {pid}")
            for k,v in ov.items():
                if k not in {"prototype_id","audit_reason"}:
                    byid[pid][k] = copy.deepcopy(v)
    return list(byid.values()), files

def audit_prototypes(protos, effective, source_ok):
    out, pos = [], Counter()
    for p in sorted(protos, key=lambda x: int(x["prototype_id"].split("_")[-1])):
        pid, qid = p["prototype_id"], p.get("candidate_id")
        reasons, cls = [], None
        if qid not in effective:
            cls = "REJECT_AS_PRODUCT_TEMPLATE"; reasons.append("orphan candidate")
        else:
            c = effective[qid]
            opts, correct = p.get("options"), p.get("correct")
            if not isinstance(opts, list) or len(opts) != 4 or not isinstance(correct, int) or correct not in range(4):
                cls = "REJECT_AS_PRODUCT_TEMPLATE"; reasons.append("invalid option/correct schema")
            else:
                pos[correct] += 1
                if len({x.strip() for x in opts if isinstance(x,str)}) != 4:
                    cls = "NEEDS_REWRITE"; reasons.append("duplicate/invalid options")
                elif p.get("explanation") != opts[correct]:
                    cls = "NEEDS_REWRITE"; reasons.append("explanation != keyed option")
                elif p.get("reference") != c.get("reference"):
                    cls = "NEEDS_REWRITE"; reasons.append("reference drift")
                elif c.get("status") == "HOLD" or not source_ok.get(qid):
                    cls = "REJECT_AS_PRODUCT_TEMPLATE"; reasons.append("effective HOLD or unresolved source owner")
                elif c.get("position") == "project":
                    cls = "COURSE_POSITION_ONLY"; reasons.append("project position cannot be neutralized")
                elif c.get("status") == "READY_NONCOMPETITIVE" or c.get("confidence") != "high" or c.get("claim_type") in {"interpretation","history","application"}:
                    cls = "NONCOMPETITIVE_ONLY"; reasons.append("authority is noncompetitive/interpretive/limited confidence")
                else:
                    cls = "SAFE_TEMPLATE"; reasons.append("bounded neutral high-confidence Research template; still not a product card")
        out.append({"prototype_id":pid,"candidate_id":qid,"classification":cls,"reasons":reasons})
    fail(len(out) != 64, f"prototype count {len(out)} != 64")
    fail(pos != Counter({0:16,1:16,2:16,3:16}), f"correct-index balance drift: {dict(pos)}")
    return out, pos

def source_identity_package(identity_lanes, inspection_lanes):
    rows = []
    for sid in sorted(inspection_lanes):
        lane = identity_lanes.get(sid, [inspection_lanes[sid][0]])[0]
        r = lane["record"]
        title = r.get("title")
        rows.append({
            "source_id": sid,
            "title": title,
            "author": r.get("author") or author_from_title(title),
            "year": r.get("year") or year_from_title(title),
            "type": norm_role(r),
            "stable_locator": r.get("url"),
            "identity_verification_status": norm_access(r),
        })
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-dir")
    args = ap.parse_args()
    base, candidate_files = read_candidates()
    effective, upgrades = apply_overrides(base)
    identity_lanes, inspection_lanes = read_sources()
    guards = guard_policies()
    snapshot = load(DATA / "wave3-final-snapshot.json")
    current = load(DATA / "remaining-holds-wave3n.json")
    declared = current.get("candidate_corpus_after_overrides") or snapshot.get("candidate_corpus") or {}
    hold_ids = current.get("remaining_holds")
    fail(hold_ids is None or not isinstance(hold_ids, list), "current HOLD authority malformed")
    chapter_counts = Counter(r.get("chapter") for r in effective.values())
    status_counts = Counter(r.get("status") for r in effective.values())
    competitive = sum(bool(r.get("competitive_candidate")) for r in effective.values())
    fail(len(effective) != declared.get("total"), f"effective total {len(effective)} != declared {declared.get('total')}")
    fail(chapter_counts[4] != declared.get("chapter4") or chapter_counts[5] != declared.get("chapter5"), f"chapter counts drift: {dict(chapter_counts)}")
    fail(status_counts["HOLD"] != declared.get("hold"), f"HOLD count drift: {status_counts['HOLD']} vs {declared.get('hold')}")
    fail(len(hold_ids) != status_counts["HOLD"], "remaining_holds contradicts effective HOLD count")
    fail(competitive != declared.get("competitive_candidates"), f"competitive count drift: {competitive}")
    fail(snapshot.get("candidate_corpus") != declared, "wave3-final-snapshot candidate corpus != current hold authority")
    inspection_rows, source_ok = [], {}
    handoff = {4: [], 5: []}
    blacklist, discrepancies = [], []
    for qid in sorted(effective, key=lambda x: int(x.split("_")[-1])):
        rec = effective[qid]
        ins = inspection_for(rec, identity_lanes, inspection_lanes)
        source_ok[qid] = True
        inspection_rows.extend({"candidate_id":qid, **row} for row in ins)
        h = make_handoff(rec, ins, guards)
        handoff[rec["chapter"]].append(h)
        blacklist.append({"candidate_id":qid,"verse":rec.get("reference"),"prohibited_formulations":h["prohibited_overclaim"],"fail_closed":True})
        if h["ranking_discrepancy_candidate"]:
            discrepancies.append({"candidate_id":qid,"reason":"Mechanical direct-text/high/neutral/exact-depth prefilter only; no auto-upgrade. Separate product reviewer required."})
    fail(len(handoff[4]) != 72 or len(handoff[5]) != 72, "handoff chapter count drift")
    fail(any(not x["prohibited_formulations"] for x in blacklist), "claim without overclaim boundary")
    protos, proto_files = read_prototypes()
    proto_audit, pos = audit_prototypes(protos, effective, source_ok)
    proto_counts = Counter(x["classification"] for x in proto_audit)
    proto_chapters = Counter(effective[x["candidate_id"]]["chapter"] for x in proto_audit if x["candidate_id"] in effective)
    fail(proto_chapters != Counter({4:32,5:32}), f"prototype chapter counts drift: {dict(proto_chapters)}")
    ranking_rows = [{"candidate_id":x["candidate_id"],"ranking_possible":False,"mechanical_discrepancy_prefilter":x["ranking_discrepancy_candidate"],"reason":"Research authority is non-ranking; Chapter 3-style admission requires separate product review and exact owning-lane claim inspection."} for x in handoff[4] + handoff[5]]
    fail(any(x["ranking_possible"] for x in ranking_rows), "accidental ranking admission")
    identity = source_identity_package(identity_lanes, inspection_lanes)
    summary = {
        "authority_parent":"0142430af8ba80f28e0fd9cde669d32611a1d2af",
        "effective_total":len(effective),"chapter4":len(handoff[4]),"chapter5":len(handoff[5]),
        "current_holds":status_counts["HOLD"],"competitive_candidates":competitive,"status_counts":dict(status_counts),
        "prototype_count":len(proto_audit),"prototype_classification_counts":dict(proto_counts),
        "correct_position_counts":{str(k):pos[k] for k in range(4)},"overclaim_blacklist_records":len(blacklist),
        "source_identity_records":len(identity),"claim_source_inspection_edges":len(inspection_rows),
        "ranking_admitted":0,"ranking_discrepancy_candidates":len(discrepancies),
        "hold_status_upgrades_with_provenance":upgrades,"candidate_files":[p.name for p in candidate_files],"prototype_files":[p.name for p in proto_files]
    }
    outputs = {
        "chapter4-product-handoff.json":{"schema_version":1,"chapter":4,"records":handoff[4]},
        "chapter5-product-handoff.json":{"schema_version":1,"chapter":5,"records":handoff[5]},
        "claim-overclaim-blacklist.json":{"schema_version":1,"records":blacklist},
        "source-identity-package.json":{"schema_version":1,"warning":"SOURCE_IDENTITY_PACKAGE != CLAIM_INSPECTION_LEDGER","sources":identity},
        "claim-inspection-manifest.json":{"schema_version":1,"warning":"Inspection depth is lane-specific and may not be globally inherited by source identity.","edges":inspection_rows},
        "prototype-audit.json":{"schema_version":1,"records":proto_audit,"counts":dict(proto_counts)},
        "ranking-audit.json":{"schema_version":1,"admitted":0,"discrepancies":discrepancies,"records":ranking_rows},
        "integrity-summary.json":summary,
    }
    if args.emit_dir:
        outdir = Path(args.emit_dir); outdir.mkdir(parents=True, exist_ok=True)
        for name, obj in outputs.items():
            (outdir / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    try: main()
    except AuditError as e:
        print(f"HANDOFF_AUDIT_FAIL: {e}", file=sys.stderr); sys.exit(2)
