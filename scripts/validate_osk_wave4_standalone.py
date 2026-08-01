#!/usr/bin/env python3
"""Fail-closed validation for OSK Wave 4 standalone pastoral-care/legal dossiers."""
from __future__ import annotations
import json, sys
from collections import Counter
from pathlib import Path
from typing import Any

R=Path(__file__).resolve().parents[1]
A={"A1","A2","A3"}
CLASSES=A|{"B1","C","D"}
ROUTES={"ANTISOVETY_CORE":21,"ANTISOVETY_CONDITIONAL":1,"DARK_SIDE_SERIES":7,"STANDALONE":3,"HOLD":1}
EXPECT={"grace-gray":18,"paul-wendy-guay":18,"franz-hengsbach":18}
STATUS={"grace-gray":"CRIMINAL_CONVICTION_AND_CONTESTED_CHURCH_RESPONSE","paul-wendy-guay":"DOCUMENTED_CORRESPONDENCE_CONTESTED_KNOWLEDGE_NO_ADJUDICATION","franz-hengsbach":"INTERIM_SCIENTIFIC_FINDING_NOT_CRIMINAL_JUDGMENT"}
FACT={"OFFICIAL_ARREST","COURT_CONVICTION","COURT_SENTENCE","COURT_APPEAL","FAMILY_COURT_ORDER","PROTECTIVE_ORDER","CRIMINAL_CHARGE","DISMISSAL","PRIMARY_MEDIA","INSTITUTIONAL_LETTER","COURT_DECLARATION","INTERNAL_MEMO","PARTY_ACCOUNT","PARTY_RESPONSE","SECONDARY_INVESTIGATION","DEFENSE_ANALYSIS","WITNESS_STATEMENT","PRIMARY_CORRESPONDENCE","PARTY_DENIAL","CONTEMPORANEOUS_NOTE","POLICE_REPORT","INSTITUTIONAL_APOLOGY","INSTITUTIONAL_RECORD","SECONDARY_TIMELINE","CURRENT_LEGAL_FRAMEWORK","INTERIM_SCIENTIFIC_REPORT","INSTITUTIONAL_SUMMARY","RESEARCH_PROJECT_RECORD","INSTITUTIONAL_STATEMENT","VICTIM_REPRESENTATIVE_POSITION","INDEPENDENT_COMMISSION_POSITION","INITIAL_DISCLOSURE","INSTITUTIONAL_MEMORY_RECORD","OFFICIAL_PUBLICATION_RECORD","INSTITUTIONAL_PUBLICATION_INDEX","SECONDARY_REPORT"}

def die(m:str)->None:
    print(f"ERROR: {m}",file=sys.stderr); raise SystemExit(1)
def load(path:str)->dict[str,Any]:
    p=R/path
    try: v=json.loads(p.read_text(encoding="utf-8"))
    except Exception as e: die(f"{path}: {e}")
    if not isinstance(v,dict): die(f"{path}: object required")
    return v
def txt(d:dict[str,Any],k:str,c:str)->str:
    v=d.get(k)
    if not isinstance(v,str) or not v.strip(): die(f"{c}: {k} required")
    return v.strip()

def main()->None:
    w1=load("data/osk-case-routing-source-registry-2026-08-01.json")
    w2=load("data/osk-wave2-source-registry-2026-08-01.json")
    w3=load("data/osk-wave3-source-registry-2026-08-01.json")
    w4=load("data/osk-wave4-source-registry-2026-08-01.json")
    if w4.get("authority_id")!="RESEARCH-OSK-AUTHORITY-2026-08-01-W4" or w4.get("base_authority_id")!=w3.get("authority_id"): die("authority chain drift")
    ov=load(txt(w4,"decision_overlay","manifest")); ds=ov.get("decisions")
    if not isinstance(ds,list) or len(ds)!=3 or ov.get("effective_route_counts")!=ROUTES: die("decision/route drift")
    by={}
    for d in ds:
        if not isinstance(d,dict): die("decision object required")
        cid=txt(d,"case_id","decision")
        if d.get("effective_route")!="STANDALONE" or d.get("status")!=STATUS.get(cid): die(f"{cid}: route/status drift")
        for k in ("article_lane","decision_reason"): txt(d,k,cid)
        for k in ("permitted_claims","blocked_claims"):
            if not isinstance(d.get(k),list) or not d[k]: die(f"{cid}: {k} required")
        by[cid]=d
    if set(by)!=set(EXPECT): die("decision set drift")

    rows=[]
    shards=w4.get("source_shards")
    if not isinstance(shards,list) or len(shards)!=3: die("exactly three source shards required")
    for p in shards:
        sh=load(p)
        if sh.get("authority_id")!=w4.get("authority_id") or not isinstance(sh.get("sources"),list): die(f"{p}: shard drift")
        rows+=sh["sources"]
    if len(rows)!=54: die(f"54 sources required, found {len(rows)}")

    ids=[]; cnt=Counter(); ac=ex=rp=qs=0
    for s in rows:
        if not isinstance(s,dict): die("source object required")
        sid=txt(s,"id","source"); cid=txt(s,"case_id",sid); cl=txt(s,"source_class",sid); fs=txt(s,"fact_status",sid)
        for k in ("title","issuer","purpose"): txt(s,k,sid)
        if cid not in EXPECT or cl not in CLASSES or fs not in FACT: die(f"{sid}: case/class/fact drift")
        u=s.get("url"); loc=s.get("repository_locator")
        if u is not None and (not isinstance(u,str) or not u.startswith("https://")): die(f"{sid}: URL must be HTTPS or null")
        if loc is not None and (not isinstance(loc,str) or not loc.strip()): die(f"{sid}: invalid repository locator")
        if not u and not loc: die(f"{sid}: URL or locator required")
        if not isinstance(s.get("quote_safe"),bool): die(f"{sid}: quote_safe boolean required")
        if s["quote_safe"] and (cl not in A or not u): die(f"{sid}: quote-safe requires A-class exact URL")
        ids.append(sid); cnt[cid]+=1; ac+=cl in A; ex+=bool(u); rp+=bool(loc); qs+=s["quote_safe"]
    if len(ids)!=len(set(ids)) or dict(cnt)!=EXPECT: die(f"source ID/count drift: {dict(cnt)}")
    if (ac,ex,rp,qs)!=(41,31,23,18): die(f"quality counters drift: {(ac,ex,rp,qs)}")

    gray_conv=next((s for s in rows if s["id"]=="W4-GRA-02"),None)
    guay_witness=next((s for s in rows if s["id"]=="W4-GUA-01"),None)
    guay_denial=next((s for s in rows if s["id"]=="W4-GUA-03"),None)
    heng_report=next((s for s in rows if s["id"]=="W4-HEN-01"),None)
    if not gray_conv or gray_conv["fact_status"]!="COURT_CONVICTION" or gray_conv["case_id"]!="grace-gray": die("Gray conviction boundary missing")
    if not guay_witness or guay_witness["fact_status"]!="WITNESS_STATEMENT" or guay_witness["quote_safe"]: die("Guay witness boundary missing")
    if not guay_denial or guay_denial["fact_status"]!="PARTY_DENIAL": die("Guay denial boundary missing")
    if not heng_report or heng_report["source_class"]!="A2" or heng_report["fact_status"]!="INTERIM_SCIENTIFIC_REPORT" or not heng_report["quote_safe"]: die("Hengsbach interim-report boundary missing")

    blocked={cid:" ".join(d["blocked_claims"]) for cid,d in by.items()}
    checks={"grace-gray":["Do not transfer David Gray's conviction","every elder knew","parole-board"],"paul-wendy-guay":["knowingly covered up","judicial finding","current California reporting statute"],"franz-hengsbach":["criminally convicted","interim findings final","ritual-abuse","active protection"]}
    for cid,needles in checks.items():
        for n in needles:
            if n not in blocked[cid]: die(f"{cid}: blocked marker missing: {n}")

    c4={"wave4_decision_records":3,"wave4_source_records":54,"wave4_a_class_sources":41,"wave4_exact_url_sources":31,"wave4_repository_capture_sources":23,"wave4_quote_safe_sources":18,"effective_core_cases":21,"effective_conditional_cases":1,"effective_dark_side_cases":7,"effective_standalone_cases":3,"effective_hold_cases":1}
    if w4.get("wave4_counters")!=c4: die("Wave 4 counter drift")
    c3=w3.get("cumulative_counters")
    if not isinstance(c3,dict): die("Wave 3 cumulative counters missing")
    cum={"source_records":c3["source_records"]+54,"a_class_sources":c3["a_class_sources"]+41,"exact_url_sources":c3["exact_url_sources"]+31,"repository_capture_sources":c3["repository_capture_sources"]+23,"quote_safe_sources":c3["quote_safe_sources"]+18}
    if w4.get("cumulative_counters")!=cum: die(f"cumulative drift: {cum}")

    authority=(R/"ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/38_WAVE4_STANDALONE_PASTORAL_CARE_LEGAL_2026-08-01.md").read_text(encoding="utf-8")
    root=(R/"00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md").read_text(encoding="utf-8")
    for m in ("238","186","82","126-страничный","Zwischenbericht","2027","не уголовная","MacArthur covered up","David Gray"):
        if m not in authority+root: die(f"authority marker missing: {m}")
    print(f"OSK Wave 4 OK: 3 standalone decisions, 54 sources, A={ac}, exact={ex}, repo={rp}, quote-safe={qs}; routing unchanged")
if __name__=="__main__": main()
