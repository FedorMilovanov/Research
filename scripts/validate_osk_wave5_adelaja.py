#!/usr/bin/env python3
"""Fail-closed validation for OSK Wave 5 Adelaja / King's Capital boundary."""
from __future__ import annotations
import json, sys
from pathlib import Path
from typing import Any

R=Path(__file__).resolve().parents[1]
A={"A1","A2","A3"}
CLASSES=A|{"B1","C","D"}
ROUTES={"ANTISOVETY_CORE":21,"ANTISOVETY_CONDITIONAL":1,"DARK_SIDE_SERIES":7,"STANDALONE":4,"HOLD":0}
FACTS={
"COURT_INDEX","COURT_PROCEDURAL_ORDER","COURT_FINAL_ORDER","COURT_APPEAL",
"CASSATION_SCREENING","CASSATION_PROCEDURAL_ORDER","CASSATION_SCHEDULING",
"CASSATION_FINAL_DISPOSITION","POST_CLOSURE_ORDER","COURT_HISTORY_INDEX",
"INSTITUTIONAL_ALLEGATION","INSIDER_ALLEGATION","PARTY_DENIAL","PARTY_STATEMENT",
"CO_DEFENDANT_STATEMENT","ADVOCACY_STATEMENT","PARTY_INTERVIEW","PARTY_MEDIA_INDEX",
"SECONDARY_PROCEDURAL_REPORT","SECONDARY_PROSECUTION_REPORT","SECONDARY_PUBLICATION",
"SECONDARY_TRIAL_REPORT","SECONDARY_INTERVIEW","SECONDARY_REPORT",
"SECONDARY_COMMENTARY","SECONDARY_DEFENSE_REPORT","COURT_MIRROR",
"SECONDARY_ALLEGATION_REPORT","PARTY_ARCHIVE","POST_CLOSURE_HISTORY","LEGAL_FRAMEWORK"
}
def die(m:str)->None:
    print("ERROR:",m,file=sys.stderr); raise SystemExit(1)
def load(p:str)->dict[str,Any]:
    try: x=json.loads((R/p).read_text(encoding="utf-8"))
    except Exception as e: die(f"{p}: {e}")
    if not isinstance(x,dict): die(f"{p}: object required")
    return x
def text(d:dict[str,Any],k:str,c:str)->str:
    v=d.get(k)
    if not isinstance(v,str) or not v.strip(): die(f"{c}: {k} required")
    return v.strip()

def main()->None:
    w4=load("data/osk-wave4-source-registry-2026-08-01.json")
    w5=load("data/osk-wave5-source-registry-2026-08-01.json")
    if w5.get("authority_id")!="RESEARCH-OSK-AUTHORITY-2026-08-01-W5": die("authority id drift")
    if w5.get("base_authority_id")!=w4.get("authority_id"): die("authority chain drift")
    ov=load(text(w5,"decision_overlay","manifest"))
    ds=ov.get("decisions")
    if not isinstance(ds,list) or len(ds)!=1 or ov.get("effective_route_counts")!=ROUTES: die("decision/route drift")
    d=ds[0]
    if d.get("case_id")!="sunday-adelaja" or d.get("previous_route")!="HOLD": die("Adelaja previous route drift")
    if d.get("effective_route")!="STANDALONE" or d.get("status")!="FINAL_PROCEDURAL_CLOSURE_NO_MERITS_VERDICT": die("Adelaja final boundary drift")
    for k in ("article_lane","decision_reason"): text(d,k,"decision")
    for k in ("permitted_claims","blocked_claims"):
        if not isinstance(d.get(k),list) or not d[k]: die(f"{k} required")

    rows=[]
    shards=w5.get("source_shards")
    if not isinstance(shards,list) or len(shards)!=4: die("four source shards required")
    for p in shards:
        sh=load(p)
        if sh.get("authority_id")!=w5.get("authority_id") or not isinstance(sh.get("sources"),list) or len(sh["sources"])!=13:
            die(f"{p}: exact 13-record shard required")
        rows+=sh["sources"]
    if len(rows)!=52: die(f"52 sources required, got {len(rows)}")
    ids=[]; ac=ex=rp=qs=0
    for s in rows:
        if not isinstance(s,dict): die("source object required")
        sid=text(s,"id","source"); cid=text(s,"case_id",sid); cl=text(s,"source_class",sid); fs=text(s,"fact_status",sid)
        for k in ("title","issuer","purpose"): text(s,k,sid)
        if cid!="sunday-adelaja" or cl not in CLASSES or fs not in FACTS: die(f"{sid}: case/class/fact drift")
        u=s.get("url"); loc=s.get("repository_locator")
        if u is not None and (not isinstance(u,str) or not u.startswith("https://")): die(f"{sid}: HTTPS URL required")
        if loc is not None and (not isinstance(loc,str) or not loc.strip()): die(f"{sid}: invalid locator")
        if not u and not loc: die(f"{sid}: URL or locator required")
        if not isinstance(s.get("quote_safe"),bool): die(f"{sid}: quote_safe boolean required")
        if s["quote_safe"] and (cl not in A or not u): die(f"{sid}: quote-safe requires A-class exact URL")
        ids.append(sid); ac+=cl in A; ex+=bool(u); rp+=bool(loc); qs+=s["quote_safe"]
    if len(ids)!=len(set(ids)): die("duplicate source ids")
    if (ac,ex,rp,qs)!=(30,49,3,23): die(f"quality counter drift {(ac,ex,rp,qs)}")

    required={
      "W5-ADE-03":("COURT_FINAL_ORDER","A1"),
      "W5-ADE-11":("CASSATION_FINAL_DISPOSITION","A1"),
      "W5-ADE-14":("INSTITUTIONAL_ALLEGATION","A3"),
      "W5-ADE-19":("PARTY_DENIAL","A3"),
      "W5-ADE-48":("SECONDARY_ALLEGATION_REPORT","B1"),
      "W5-ADE-52":("LEGAL_FRAMEWORK","A1"),
    }
    by={s["id"]:s for s in rows}
    for sid,(fs,cl) in required.items():
        if sid not in by or by[sid]["fact_status"]!=fs or by[sid]["source_class"]!=cl: die(f"{sid}: required boundary missing")
    blocked=" ".join(d["blocked_claims"])
    for needle in ("Do not call Adelaja convicted","merits acquittal","court established pulpit promotion","2016 sexual allegations","authenticated primary media"):
        if needle not in blocked: die(f"blocked claim missing: {needle}")
    permitted=" ".join(d["permitted_claims"])
    for needle in ("7 December 2023","11 December 2025","standalone article"):
        if needle not in permitted: die(f"permitted claim missing: {needle}")

    c5={"wave5_decision_records":1,"wave5_source_records":52,"wave5_a_class_sources":30,
        "wave5_exact_url_sources":49,"wave5_repository_capture_sources":3,
        "wave5_quote_safe_sources":23,"effective_core_cases":21,
        "effective_conditional_cases":1,"effective_dark_side_cases":7,
        "effective_standalone_cases":4,"effective_hold_cases":0}
    if w5.get("wave5_counters")!=c5: die("Wave 5 counter drift")
    c4=w4.get("cumulative_counters")
    cum={"source_records":c4["source_records"]+52,"a_class_sources":c4["a_class_sources"]+30,
         "exact_url_sources":c4["exact_url_sources"]+49,
         "repository_capture_sources":c4["repository_capture_sources"]+3,
         "quote_safe_sources":c4["quote_safe_sources"]+23}
    if w5.get("cumulative_counters")!=cum: die(f"cumulative drift {cum}")

    authority=(R/"ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/39_WAVE5_ADELAJA_FINAL_BOUNDARY_2026-08-01.md").read_text(encoding="utf-8")
    root=(R/"00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md").read_text(encoding="utf-8")
    for marker in ("290","216","105","NO_MERITS_VERDICT","7 декабря 2023","11 декабря 2025","0 HOLD","SEPARATE DOSSIER REQUIRED"):
        if marker not in authority+root: die(f"authority marker missing: {marker}")
    print(f"OSK Wave 5 OK: 1 decision, 52 sources, A={ac}, exact={ex}, repo={rp}, quote-safe={qs}; routes {ROUTES}")
if __name__=="__main__": main()
