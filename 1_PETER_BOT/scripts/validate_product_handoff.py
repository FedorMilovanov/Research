#!/usr/bin/env python3
import argparse
import copy
import hashlib
import json
import re
import sys
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
SOURCE_EXTRA_INSPECTION_FILES = ["source-upgrade-wave3e.json"]
CAND_RE = re.compile(r"question-candidates-wave3-(\d{3})-(\d{3})\.json$")
PROTO_RE = re.compile(r"mcq-prototypes-wave3[jm]?-(\d{3})-(\d{3})\.json$")
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
LAYER_RE = re.compile(r"wave(3[a-z0-9]*)", re.I)
WORD_RE = re.compile(r"[A-Za-zΑ-ωΆ-ώА-Яа-яЁё0-9_]{3,}")

class AuditError(RuntimeError):
    pass

def load(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)

def fail(cond, msg):
    if cond:
        raise AuditError(msg)

def stable_hash(value):
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def cid(rec):
    return rec.get("id") or rec.get("candidate_id") or rec.get("question_id")

def source_id(rec):
    return rec.get("source_id") or rec.get("id")

def layer_of(path):
    m = LAYER_RE.search(path.name)
    return m.group(1).lower() if m else "base"

def norm_scope(rec):
    return rec.get("inspection_scope") or rec.get("inspectionScope") or rec.get("inspection_level") or rec.get("inspection_status") or "UNSPECIFIED"

def norm_access(rec):
    return rec.get("access_state") or rec.get("accessState") or "UNSPECIFIED"

def norm_evidence(rec):
    return rec.get("evidence_status") or rec.get("evidenceStatus") or "NOT_EXPLICITLY_LABELED"

def norm_role(rec):
    return rec.get("source_role") or rec.get("role") or rec.get("kind") or "UNSPECIFIED"

def norm_limit(rec):
    return rec.get("claim_limit") or rec.get("claimLimit") or ""

def source_title(rec, sid):
    return rec.get("title") or sid

def source_locator(rec):
    return rec.get("url") or rec.get("stable_locator") or rec.get("locator") or ""

def author_from_title(title):
    if not title or "," not in title:
        return None
    head = title.split(",", 1)[0].strip()
    return head if 2 <= len(head) <= 120 else None

def year_from_title(title):
    m = YEAR_RE.search(title or "")
    return int(m.group()) if m else None

def read_candidates():
    files = sorted(
        (p for p in DATA.glob("question-candidates-wave3-*.json") if CAND_RE.search(p.name)),
        key=lambda p: int(CAND_RE.search(p.name).group(1)),
    )
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
    field_provenance = {}
    batches = [p for p in DATA.glob("question-candidates-wave3-*.json") if CAND_RE.search(p.name)]
    for r in base:
        qid = cid(r)
        n = int(qid.split("_")[-1])
        owner = next(
            p.name
            for p in batches
            if int(CAND_RE.search(p.name).group(1)) <= n <= int(CAND_RE.search(p.name).group(2))
        )
        provenance[qid] = ["base:" + owner]
        field_provenance[qid] = {k: "base:" + owner for k in r.keys()}
    upgrades = []
    for name in OVERRIDES:
        path = DATA / name
        fail(not path.exists(), f"missing override authority {name}")
        rows = load(path).get("overrides")
        fail(not isinstance(rows, list), f"{name}: overrides missing")
        seen = set()
        for ov in rows:
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
                field_provenance[qid][field] = "override:" + name
            if "status" in fields and old_status == "HOLD" and effective[qid].get("status") != "HOLD":
                fail("source_minimum" not in ov, f"{name}:{qid}: HOLD upgrade without source_minimum provenance")
                fail(not ov.get("do_not_claim"), f"{name}:{qid}: HOLD upgrade without do_not_claim")
                upgrades.append((qid, name, old_status, effective[qid].get("status")))
            provenance[qid].append("override:" + name)
    for qid, rec in effective.items():
        rec["_provenance"] = provenance[qid]
        rec["_field_provenance"] = field_provenance[qid]
    return effective, upgrades

def provenance_layer(marker):
    m = LAYER_RE.search(marker or "")
    return m.group(1).lower() if m else "base"

def source_contract_layer(rec):
    return provenance_layer((rec.get("_field_provenance") or {}).get("source_minimum", "base"))

def read_sources():
    identity_lanes = defaultdict(list)
    inspection_lanes = defaultdict(list)
    files = (
        sorted(DATA.glob("source-ledger-*.json"))
        + sorted(DATA.glob("source-quorum-*.json"))
        + [DATA / x for x in SOURCE_EXTRA_INSPECTION_FILES]
    )
    fail(not files, "no source authority files")
    for path in files:
        fail(not path.exists(), f"missing source authority {path.name}")
        rows = load(path).get("sources", [])
        fail(not isinstance(rows, list), f"{path.name}: sources is not a list")
        for row in rows:
            sid = source_id(row)
            fail(not sid, f"{path.name}: source without id")
            lane = {
                "path": str(path.relative_to(ROOT)),
                "layer": layer_of(path),
                "record": row,
                "lane_kind": (
                    "IDENTITY_LEDGER"
                    if path.name.startswith("source-ledger-")
                    else "INSPECTION_UPGRADE"
                    if path.name.startswith("source-upgrade-")
                    else "CLAIM_QUORUM"
                ),
            }
            inspection_lanes[sid].append(lane)
            if path.name.startswith("source-ledger-"):
                identity_lanes[sid].append(lane)
    return identity_lanes, inspection_lanes

def choose_owner(rec, sid, identity_lanes, inspection_lanes):
    lanes = inspection_lanes.get(sid, [])
    fail(not lanes, f"{cid(rec)}: unresolved source id {sid}")
    target = source_contract_layer(rec)
    matching = [
        x for x in lanes
        if x["layer"] == target and x["lane_kind"] in {"CLAIM_QUORUM", "INSPECTION_UPGRADE"}
    ]
    if len(matching) == 1:
        return matching[0], "MATCHING_SOURCE_MINIMUM_PROVENANCE_LANE"
    fail(len(matching) > 1, f"{cid(rec)}:{sid}: multiple source-minimum provenance owners")
    ledger = identity_lanes.get(sid, [])
    if len(ledger) == 1:
        return ledger[0], "SOLE_IDENTITY_LEDGER_NO_DEPTH_INHERITANCE"
    fail(len(ledger) > 1, f"{cid(rec)}:{sid}: multiple identity ledgers; explicit claim owner required")
    if len(lanes) == 1:
        return lanes[0], "SOLE_EXPLICIT_INSPECTION_LANE"
    raise AuditError(f"{cid(rec)}:{sid}: ambiguous source owner lanes {[x['path'] for x in lanes]}")

def inspection_depth_class(row):
    scope = (row.get("inspection_scope") or "").lower()
    ev = (row.get("evidence_status") or "").lower()
    limited = ("catalog", "metadata", "abstract", "unspecified", "link_only", "page_inspected")
    ready = ("exact_", "full_", "relevant_", "partial_text_inspected", "entry_inspected", "passage_inspected")
    if any(x in scope for x in limited) or any(x in ev for x in ("bibliographic", "abstract", "metadata")):
        return "LIMITED_OR_IDENTITY_ONLY"
    if any(x in scope for x in ready) or any(x in ev for x in ("inspected_primary", "inspected_passage", "inspected_entry", "inspected_full_text")):
        return "CLAIM_INSPECTION_PRESENT"
    return "UNCLASSIFIED_FAIL_CLOSED"

def inspection_for(rec, identity_lanes, inspection_lanes):
    rows = []
    for sid in rec.get("source_minimum") or []:
        owner, why = choose_owner(rec, sid, identity_lanes, inspection_lanes)
        s = owner["record"]
        edge = {
            "candidate_id": cid(rec),
            "source_id": sid,
            "evidence_status": norm_evidence(s),
            "access_state": norm_access(s),
            "inspection_scope": norm_scope(s),
            "inspection_depth_class": None,
            "owning_lane": owner["path"],
            "owning_lane_kind": owner["lane_kind"],
            "claim_limit": norm_limit(s),
            "owner_resolution": why,
            "source_minimum_provenance": (rec.get("_field_provenance") or {}).get("source_minimum"),
        }
        edge["inspection_depth_class"] = inspection_depth_class(edge)
        edge["claim_inspection_edge_id"] = "edge_" + stable_hash(
            {k: edge[k] for k in (
                "candidate_id", "source_id", "evidence_status", "access_state",
                "inspection_scope", "owning_lane", "claim_limit", "source_minimum_provenance"
            )}
        )[:20]
        rows.append(edge)
    fail(not rows, f"{cid(rec)}: no source_minimum")
    return rows

def exact_claim_ready(rows):
    return bool(rows) and all(x["inspection_depth_class"] == "CLAIM_INSPECTION_PRESENT" for x in rows)

def flags_for(rec):
    t = (rec.get("claim_type") or "").lower()
    tested = (rec.get("tested_distinction") or "").lower()
    ref = rec.get("reference") or ""
    src = " ".join(rec.get("source_minimum") or []).lower()
    flags = set()
    if t == "text":
        flags.add("DIRECT_TEXT")
    if t == "greek":
        flags.add("GREEK_FORM")
    if t == "greek" and any(k in tested for k in ("morph", "parse", "form", "participle")):
        flags.add("MORPHOLOGY")
    if any(k in tested for k in ("lex", "gloss", "semant")) or "lexicon" in src:
        flags.add("LEXICAL")
    if "/" in ref or any(k in tested for k in ("intertext", "quotation", "background", "lxx")):
        flags.add("INTERTEXT")
    if t == "history":
        flags.add("HISTORY")
    if t == "interpretation":
        flags.add("THEOLOGY")
    if rec.get("confidence") == "contested":
        flags.add("DISPUTED")
    if any(k in tested for k in ("variant", "apparatus", "textual")) or any(x in src for x in ("ecm_", "ntvmr")):
        flags.add("TEXTUAL_CRITICISM")
    if t == "application":
        flags.add("APPLICATION")
    return sorted(flags)

def domain_for(flags, rec):
    for value in (
        "TEXTUAL_CRITICISM", "MORPHOLOGY", "LEXICAL", "INTERTEXT",
        "HISTORY", "THEOLOGY", "APPLICATION", "GREEK_FORM", "DIRECT_TEXT"
    ):
        if value in flags:
            return value
    return (rec.get("claim_type") or "UNKNOWN").upper()

def guard_policies():
    out = []
    for name in ("chapter4-guard-policy.json", "chapter5-guard-policy.json"):
        obj = load(HANDOFF / name)
        out.extend(obj.get("guard_records", []))
    return out

def guard_matches(g, rec):
    if g.get("candidate_id") and g["candidate_id"] != cid(rec):
        return False
    if g.get("match_reference") and g["match_reference"] != rec.get("reference"):
        return False
    if g.get("match_reference_prefix") and not (rec.get("reference") or "").startswith(g["match_reference_prefix"]):
        return False
    if g.get("match_claim_type") and g["match_claim_type"] != rec.get("claim_type"):
        return False
    return True

def effective_claim_digest(rec):
    fields = {
        "candidate_id": cid(rec),
        "chapter": rec.get("chapter"),
        "reference": rec.get("reference"),
        "claim_type": rec.get("claim_type"),
        "position": rec.get("position"),
        "confidence": rec.get("confidence"),
        "status": rec.get("status"),
        "competitive_candidate": bool(rec.get("competitive_candidate")),
        "keyed_concept": rec.get("keyed_concept"),
        "tested_distinction": rec.get("tested_distinction"),
        "source_minimum": rec.get("source_minimum") or [],
        "do_not_claim": rec.get("do_not_claim"),
        "field_provenance": rec.get("_field_provenance"),
    }
    return stable_hash(fields)

def make_handoff(rec, inspection, guards):
    flags = flags_for(rec)
    project = rec.get("position") == "project"
    contested = rec.get("confidence") == "contested" or "DISPUTED" in flags
    safe = rec.get("keyed_concept") or rec.get("candidate_claim") or rec.get("candidate") or rec.get("stem")
    if project:
        safe = "COURSE POSITION ONLY: " + str(safe)
    elif contested:
        safe = "CONTESTED / ATTRIBUTION REQUIRED: " + str(safe)
    prohibited = [rec.get("do_not_claim")] if rec.get("do_not_claim") else []
    for g in guards:
        if guard_matches(g, rec) and g.get("prohibited_overclaim"):
            prohibited.append(g["prohibited_overclaim"])
    objective_shape = (
        rec.get("position") == "neutral"
        and rec.get("confidence") == "high"
        and rec.get("status") == "READY"
        and rec.get("claim_type") in {"text", "greek"}
        and not any(f in flags for f in (
            "DISPUTED", "TEXTUAL_CRITICISM", "HISTORY", "THEOLOGY",
            "APPLICATION", "LEXICAL", "INTERTEXT"
        ))
    )
    can_obj = objective_shape and exact_claim_ready(inspection)
    discrepancy = objective_shape and exact_claim_ready(inspection)
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
        "ranking_discrepancy_candidate": bool(discrepancy),
        "rationale": (
            "Research READY is not product or ranking approval. Objective authoring additionally "
            "requires neutral/high/direct factual shape and claim-inspection-present source edges."
        ),
        "flags": flags,
        "effective_status": rec.get("status"),
        "effective_competitive_candidate": bool(rec.get("competitive_candidate")),
        "effective_claim_digest": effective_claim_digest(rec),
        "provenance": rec["_provenance"],
        "field_provenance": rec["_field_provenance"],
    }

def read_prototypes():
    files = sorted(
        (p for p in DATA.glob("mcq-prototypes-wave3*-*.json") if PROTO_RE.search(p.name)),
        key=lambda p: int(PROTO_RE.search(p.name).group(1)),
    )
    rows = []
    for p in files:
        batch = load(p).get("prototypes")
        fail(not isinstance(batch, list), f"{p.name}: prototypes missing")
        rows.extend(copy.deepcopy(batch))
    ids = [x.get("prototype_id") for x in rows]
    fail(any(x is None for x in ids), "prototype without id")
    dup = [x for x, n in Counter(ids).items() if n > 1]
    fail(bool(dup), f"duplicate prototype IDs: {dup}")
    byid = {x["prototype_id"]: x for x in rows}
    op = DATA / "mcq-prototype-overrides-wave3j2.json"
    if op.exists():
        for ov in load(op).get("overrides", []):
            pid = ov.get("prototype_id")
            fail(pid not in byid, f"orphan prototype override {pid}")
            old_correct = byid[pid].get("correct")
            for k, v in ov.items():
                if k not in {"prototype_id", "audit_reason"}:
                    byid[pid][k] = copy.deepcopy(v)
            fail(byid[pid].get("correct") != old_correct, f"{pid}: editorial override changed correct index")
    return [byid[x] for x in sorted(byid)], files

def load_content_risk_policy():
    obj = load(HANDOFF / "prototype-content-risk-policy.json")
    rows = obj.get("risk_patterns")
    fail(not isinstance(rows, list) or not rows, "prototype content-risk policy missing patterns")
    compiled = []
    for row in rows:
        fail(not row.get("id") or row.get("severity") not in {"rewrite", "warning"} or not row.get("regex"),
             "invalid prototype content-risk pattern")
        try:
            rx = re.compile(row["regex"])
        except re.error as exc:
            raise AuditError(f"invalid regex {row.get('id')}: {exc}")
        compiled.append((row["id"], row["severity"], rx))
    return compiled

def significant_tokens(text):
    stop = {
        "потому", "который", "которая", "которые", "этого", "этот", "эта", "как", "что",
        "это", "для", "при", "или", "нет", "the", "and", "with", "from", "that",
        "сам", "сама", "себе", "свою", "свои", "только",
    }
    return {x.lower() for x in WORD_RE.findall(str(text or "")) if x.lower() not in stop}

def alignment_signal(proto, rec):
    answer = proto["options"][proto["correct"]]
    a = significant_tokens(answer)
    authority = significant_tokens(" ".join([
        str(rec.get("keyed_concept") or ""),
        str(rec.get("tested_distinction") or ""),
        str(rec.get("stem") or ""),
    ]))
    shared = sorted(a & authority)
    ratio = round(len(shared) / max(1, len(a)), 3)
    return {
        "shared_tokens": shared[:20],
        "answer_token_coverage": ratio,
        "signal": "PRESENT" if shared else "LOW_REQUIRES_HUMAN_SEMANTIC_CHECK",
    }

def prototype_content_risks(proto, patterns):
    out = []
    correct = proto["correct"]
    for idx, option in enumerate(proto["options"]):
        if idx == correct:
            continue
        for rid, severity, rx in patterns:
            if rx.search(str(option)):
                out.append({
                    "option_index": idx,
                    "risk_id": rid,
                    "severity": severity,
                    "text": option,
                })
    return out

def audit_prototypes(protos, effective, inspection_by_claim):
    patterns = load_content_risk_policy()
    out = []
    positions = Counter()
    allowed_classes = {
        "SAFE_TEMPLATE", "NEEDS_REWRITE", "COURSE_POSITION_ONLY",
        "NONCOMPETITIVE_ONLY", "REJECT_AS_PRODUCT_TEMPLATE"
    }
    for p in protos:
        pid = p["prototype_id"]
        qid = p.get("candidate_id")
        rec = effective.get(qid)
        reasons = []
        reject = False
        if rec is None:
            out.append({"prototype_id": pid, "candidate_id": qid, "classification": "REJECT_AS_PRODUCT_TEMPLATE", "reasons": ["ORPHAN_CANDIDATE"]})
            continue
        opts = p.get("options")
        if not isinstance(opts, list) or len(opts) != 4 or any(not str(x).strip() for x in opts):
            reject = True
            reasons.append("INVALID_OPTIONS")
        if len({str(x).strip().casefold() for x in opts or []}) != 4:
            reject = True
            reasons.append("DUPLICATE_OPTIONS")
        correct = p.get("correct")
        if not isinstance(correct, int) or correct not in range(4):
            reject = True
            reasons.append("INVALID_CORRECT_INDEX")
        else:
            positions[correct] += 1
            if p.get("explanation") != opts[correct]:
                reject = True
                reasons.append("EXPLANATION_NOT_KEYED_OPTION")
        if p.get("reference") != rec.get("reference"):
            reject = True
            reasons.append("REFERENCE_DRIFT")
        if p.get("competitive_candidate") is not False:
            reject = True
            reasons.append("PROTOTYPE_COMPETITIVE_UPGRADE")
        if not str(p.get("source_contract") or "").strip():
            reject = True
            reasons.append("MISSING_SOURCE_CONTRACT")
        if rec.get("status") == "HOLD":
            reject = True
            reasons.append("CURRENT_HOLD")
        source_edges = inspection_by_claim.get(qid) or []
        if len(source_edges) != len(rec.get("source_minimum") or []):
            reject = True
            reasons.append("SOURCE_EDGE_COUNT_DRIFT")

        risks = [] if reject or not isinstance(correct, int) or correct not in range(4) else prototype_content_risks(p, patterns)
        rewrite_risks = [x for x in risks if x["severity"] == "rewrite"]
        warning_risks = [x for x in risks if x["severity"] == "warning"]
        if rewrite_risks:
            reasons.append("DISTRACTOR_FALSE_CERTAINTY_OR_EVIDENCE_LAUNDERING")
        align = {"signal": "UNAVAILABLE"} if reject else alignment_signal(p, rec)
        if align.get("signal") == "LOW_REQUIRES_HUMAN_SEMANTIC_CHECK":
            reasons.append("LOW_AUTOMATED_CLAIM_ALIGNMENT_SIGNAL")

        if reject:
            cls = "REJECT_AS_PRODUCT_TEMPLATE"
        elif rewrite_risks:
            cls = "NEEDS_REWRITE"
        elif rec.get("position") == "project":
            cls = "COURSE_POSITION_ONLY"
            reasons.append("PROJECT_POSITION")
        elif (
            rec.get("status") != "READY"
            or rec.get("confidence") != "high"
            or rec.get("claim_type") not in {"text", "greek"}
            or any(x in flags_for(rec) for x in ("DISPUTED", "TEXTUAL_CRITICISM", "HISTORY", "THEOLOGY", "APPLICATION", "LEXICAL", "INTERTEXT"))
        ):
            cls = "NONCOMPETITIVE_ONLY"
            reasons.append("NONCOMPETITIVE_AUTHORITY_SHAPE")
        else:
            cls = "SAFE_TEMPLATE"
            reasons.append("STRUCTURALLY_BOUNDED_NEUTRAL_TEMPLATE_ONLY")

        fail(cls not in allowed_classes, f"{pid}: unknown classification {cls}")
        out.append({
            "prototype_id": pid,
            "candidate_id": qid,
            "reference": p.get("reference"),
            "classification": cls,
            "reasons": reasons,
            "correct_index": correct,
            "wrong_option_risks": risks,
            "rewrite_risk_count": len(rewrite_risks),
            "warning_risk_count": len(warning_risks),
            "claim_alignment_signal": align,
            "effective_position": rec.get("position"),
            "effective_confidence": rec.get("confidence"),
            "effective_claim_type": rec.get("claim_type"),
            "effective_status": rec.get("status"),
            "effective_claim_digest": effective_claim_digest(rec),
            "source_edge_ids": [x["claim_inspection_edge_id"] for x in source_edges],
        })
    fail(len(out) != 64, f"prototype count {len(out)} != 64")
    fail(positions != Counter({0: 16, 1: 16, 2: 16, 3: 16}), f"correct-index balance drift: {dict(positions)}")
    return out

def source_identity_package(identity_lanes, inspection_lanes):
    rows = []
    anomalies = []
    all_ids = sorted(inspection_lanes)
    for sid in all_ids:
        lanes = inspection_lanes[sid]
        identity = identity_lanes.get(sid, [])
        records = [x["record"] for x in lanes]
        preferred = identity[0]["record"] if identity else records[0]
        titles = sorted({source_title(x, sid).strip() for x in records if source_title(x, sid).strip()})
        locators = sorted({source_locator(x).strip() for x in records if source_locator(x).strip()})
        types = sorted({norm_role(x).strip() for x in records if norm_role(x).strip()})
        anomaly = len(titles) > 1 or len(locators) > 1 or len(types) > 1
        if anomaly:
            anomalies.append(sid)
        rows.append({
            "source_id": sid,
            "title": source_title(preferred, sid),
            "author": author_from_title(source_title(preferred, sid)),
            "year": year_from_title(source_title(preferred, sid)),
            "type": norm_role(preferred),
            "stable_locator": source_locator(preferred),
            "identity_verification_status": (
                "IDENTITY_LEDGER_RECORDED" if identity else "IDENTITY_DERIVED_FROM_EXPLICIT_RESEARCH_SOURCE_RECORD"
            ),
            "known_titles": titles,
            "known_locators": locators,
            "known_types": types,
            "identity_lane_paths": [x["path"] for x in identity],
            "identity_variant_flag": anomaly,
            "identity_only": True,
        })
    return rows, anomalies

def validate_hold_history():
    old = load(DATA / "remaining-holds-wave3l.json")
    current = load(DATA / "remaining-holds-wave3n.json")
    p0 = load(DATA / "p0-claim-holds-wave3.json")
    old_ids = {row.get("candidate_id") for row in old.get("remaining_holds", [])}
    closed_ids = {row.get("candidate_id") for row in current.get("closed_in_wave3n", [])}
    current_ids = {row.get("candidate_id") for row in current.get("remaining_holds", [])}
    fail(None in old_ids or None in closed_ids, "HOLD history missing candidate_id")
    fail(old_ids != closed_ids, f"Wave3l HOLD set != Wave3n closure set: {sorted(old_ids)} != {sorted(closed_ids)}")
    fail(bool(current_ids), f"Wave3n still has current HOLDs: {sorted(current_ids)}")
    fail((current.get("candidate_corpus_after_overrides") or {}).get("hold") != 0, "Wave3n declared HOLD count nonzero")
    fail(not isinstance(p0.get("targets"), list) or not p0.get("methodRules"), "P0 HOLD history malformed")
    return sorted(old_ids)

def validate_snapshot(effective):
    snap = load(DATA / "wave3-final-snapshot.json")
    counts = Counter()
    for rec in effective.values():
        counts["total"] += 1
        counts[f"chapter{rec.get('chapter')}"] += 1
        counts[rec.get("status", "UNKNOWN")] += 1
        counts["competitive"] += int(bool(rec.get("competitive_candidate")))
    expected = snap.get("candidate_corpus") or {}
    fail(counts["total"] != expected.get("total"), "snapshot total drift")
    fail(counts["chapter4"] != expected.get("chapter4"), "snapshot Ch4 drift")
    fail(counts["chapter5"] != expected.get("chapter5"), "snapshot Ch5 drift")
    fail(counts["READY"] != expected.get("ready"), "snapshot READY drift")
    fail(counts["READY_NONCOMPETITIVE"] != expected.get("ready_noncompetitive"), "snapshot READY_NONCOMPETITIVE drift")
    fail(counts["HOLD"] != expected.get("hold"), "snapshot HOLD drift")
    fail(counts["competitive"] != expected.get("competitive_candidates"), "snapshot competitive drift")
    return counts

def ranking_audit(handoffs):
    rows = []
    for h in handoffs:
        criteria = {
            "neutral": h["position"] == "neutral",
            "high_confidence": h["confidence"] == "high",
            "direct_text": "DIRECT_TEXT" in h["flags"],
            "objective_shape": h["claim_type"] == "text",
            "claim_ready_owning_lane": all(x["inspection_depth_class"] == "CLAIM_INSPECTION_PRESENT" for x in h["source_evidence"]),
            "no_project_theology": not h["project"],
            "no_dispute": not h["contested"],
            "no_textual_instability_flag": "TEXTUAL_CRITICISM" not in h["flags"],
            "research_competitive_candidate": h["effective_competitive_candidate"],
        }
        admitted = False
        discrepancy = all(v for k, v in criteria.items() if k != "research_competitive_candidate")
        rows.append({
            "candidate_id": h["candidate_id"],
            "criteria": criteria,
            "admitted": admitted,
            "discrepancy_candidate": discrepancy,
            "reason": (
                "Research authority explicitly has competitive_candidate=false; Chapter3-style criteria are shown "
                "adversarially and do not authorize automatic promotion."
            ),
        })
    return rows

def overclaim_blacklist(handoffs):
    patterns = load(HANDOFF / "overclaim-patterns.json").get("patterns", [])
    pattern_ids = [x.get("id") for x in patterns if x.get("id")]
    return [{
        "candidate_id": h["candidate_id"],
        "verse": h["verse"],
        "flags": h["flags"],
        "prohibited_overclaim": h["prohibited_overclaim"],
        "global_pattern_ids": pattern_ids,
        "prototype_distractor_boundary": "The same prohibited certainty/evidence laundering is forbidden in wrong answer options.",
        "effective_claim_digest": h["effective_claim_digest"],
    } for h in handoffs]

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-dir", required=True)
    args = ap.parse_args()
    emit = Path(args.emit_dir)
    emit.mkdir(parents=True, exist_ok=True)

    historical_holds = validate_hold_history()
    base, candidate_files = read_candidates()
    effective, upgrades = apply_overrides(base)
    counts = validate_snapshot(effective)
    identity_lanes, inspection_lanes = read_sources()
    guards = guard_policies()

    handoffs = []
    inspection_by_claim = {}
    for qid in sorted(effective, key=lambda x: int(x.split("_")[-1])):
        rec = effective[qid]
        edges = inspection_for(rec, identity_lanes, inspection_lanes)
        inspection_by_claim[qid] = edges
        handoffs.append(make_handoff(rec, edges, guards))

    ch4 = [x for x in handoffs if effective[x["candidate_id"]].get("chapter") == 4]
    ch5 = [x for x in handoffs if effective[x["candidate_id"]].get("chapter") == 5]
    fail(len(ch4) != 72 or len(ch5) != 72, f"chapter counts drift Ch4={len(ch4)} Ch5={len(ch5)}")
    fail(counts["HOLD"] != 0, f"current HOLD count {counts['HOLD']}")
    fail(counts["competitive"] != 0, f"competitive candidate count {counts['competitive']}")

    protos, proto_files = read_prototypes()
    proto_audit = audit_prototypes(protos, effective, inspection_by_claim)
    identities, identity_anomalies = source_identity_package(identity_lanes, inspection_lanes)
    all_edges = [edge for qid in sorted(inspection_by_claim) for edge in inspection_by_claim[qid]]
    rank = ranking_audit(handoffs)
    blacklist = overclaim_blacklist(handoffs)

    authority_digest = stable_hash([
        {"candidate_id": x["candidate_id"], "effective_claim_digest": x["effective_claim_digest"]}
        for x in handoffs
    ])
    class_counts = dict(Counter(x["classification"] for x in proto_audit))
    risk_counts = Counter(
        risk["risk_id"] for row in proto_audit for risk in row.get("wrong_option_risks", [])
        if risk["severity"] == "rewrite"
    )
    summary = {
        "schema_version": 2,
        "authority_digest_sha256": authority_digest,
        "chapter4": len(ch4),
        "chapter5": len(ch5),
        "current_holds": counts["HOLD"],
        "historical_hold_ids_closed_by_wave3n": historical_holds,
        "competitive_candidates": counts["competitive"],
        "prototype_count": len(proto_audit),
        "prototype_classification_counts": class_counts,
        "prototype_rewrite_risk_counts": dict(risk_counts),
        "overclaim_blacklist_records": len(blacklist),
        "ranking_admitted": sum(x["admitted"] for x in rank),
        "ranking_discrepancy_candidates": sum(x["discrepancy_candidate"] for x in rank),
        "source_identity_records": len(identities),
        "source_identity_variant_ids": identity_anomalies,
        "source_identity_variant_count": len(identity_anomalies),
        "claim_source_inspection_edges": len(all_edges),
        "hold_status_upgrades_checked": [list(x) for x in upgrades],
        "candidate_files": [p.name for p in candidate_files],
        "prototype_files": [p.name for p in proto_files],
    }

    write_json(emit / "chapter4-product-handoff.json", {"schema_version": 2, "records": ch4})
    write_json(emit / "chapter5-product-handoff.json", {"schema_version": 2, "records": ch5})
    write_json(emit / "claim-overclaim-blacklist.json", {"schema_version": 2, "records": blacklist})
    write_json(emit / "source-identity-package.json", {
        "schema_version": 2,
        "invariant": "SOURCE_IDENTITY_PACKAGE != CLAIM_INSPECTION_LEDGER",
        "records": identities,
    })
    write_json(emit / "claim-inspection-manifest.json", {
        "schema_version": 2,
        "invariant": "CLAIM_INSPECTION_DEPTH_IS_EDGE_LOCAL_AND_FIELD_PROVENANCE_BOUND",
        "records": all_edges,
    })
    write_json(emit / "prototype-audit.json", {"schema_version": 2, "records": proto_audit})
    write_json(emit / "ranking-audit.json", {"schema_version": 2, "records": rank})
    write_json(emit / "integrity-summary.json", summary)

    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__":
    try:
        main()
    except AuditError as exc:
        print(f"HANDOFF_AUDIT_FAIL: {exc}", file=sys.stderr)
        sys.exit(2)
