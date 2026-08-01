#!/usr/bin/env python3
import json, sys
from collections import Counter
from pathlib import Path

R=Path(__file__).resolve().parents[1]
A={"A1","A2","A3"}
FACT={"OFFICIAL_ACTION","SELF_ADMISSION","SECONDARY_REPORT","GOVERNANCE_RULE","ADVOCACY_SOURCE","PRIMARY_PUBLIC_TEACHING","INSTITUTIONAL_STATEMENT","PARTY_ALLEGATION","PARTY_DENIAL","OFFICIAL_INQUIRY","COURT_FILING_ALLEGATION","SETTLEMENT_DISMISSAL"}
EXPECT={"steven-lawson":7,"tullian-tchividjian":8,"sam-allberry":7,"andy-savage":8,"carl-lentz":8,"eddie-long":11}
STATUS={"steven-lawson":"DISQUALIFICATION_CONFESSION_NO_POWER_FINDING","tullian-tchividjian":"INCOMPLETE_DISCLOSURE_AND_PREMATURE_RESTORATION","sam-allberry":"INSTITUTIONAL_REASSESSMENT_AND_DEPOSITION","andy-savage":"MINIMIZATION_AND_INSTITUTIONAL_DEFENSIVENESS","carl-lentz":"ADMITTED_AFFAIR_CONTESTED_ABUSE","eddie-long":"ALLEGATION_SETTLEMENT_AND_FINANCIAL_ACCOUNTABILITY","perry-noble":"RESTORATION_CONTRAST_INHERITED_W2"}
ROUTES={"ANTISOVETY_CORE":21,"ANTISOVETY_CONDITIONAL":1,"DARK_SIDE_SERIES":7,"STANDALONE":3,"HOLD":1}

def die(x): print("ERROR:",x,file=sys.stderr); raise SystemExit(1)
def load(p):
    p=R/p
    try: x=json.loads(p.read_text(encoding="utf-8"))
    except Exception as e: die(f"{p.relative_to(R)}: {e}")
    if not isinstance(x,dict): die(f"{p.relative_to(R)}: object required")
    return x
def nonempty(x,k,c):
    v=x.get(k)
    if not isinstance(v,str) or not v.strip(): die(f"{c}: {k} required")
    return v

def main():
    w1=load("data/osk-case-routing-source-registry-2026-08-01.json")
    w2=load("data/osk-wave2-source-registry-2026-08-01.json")
    w3=load("data/osk-wave3-source-registry-2026-08-01.json")
    if w3.get("authority_id")!="RESEARCH-OSK-AUTHORITY-2026-08-01-W3" or w3.get("base_authority_id")!=w2.get("authority_id"): die("authority chain drift")
    ov=load(w3["decision_overlay"]); ds=ov.get("decisions")
    if not isinstance(ds,list) or len(ds)!=7 or ov.get("effective_route_counts")!=ROUTES: die("decision/route drift")
    by={}
    for d in ds:
        cid=nonempty(d,"case_id","decision"); st=nonempty(d,"status",cid)
        if d.get("effective_route")!="DARK_SIDE_SERIES" or STATUS.get(cid)!=st: die(f"{cid}: route/status drift")
        for k in ("article_lane","decision_reason"): nonempty(d,k,cid)
        for k in ("permitted_claims","blocked_claims"):
            if not isinstance(d.get(k),list) or not d[k]: die(f"{cid}: {k} required")
        by[cid]=d
    if set(by)!=set(STATUS): die("decision set drift")
    inherited=[f"W2-NOB-{i:02d}" for i in range(1,8)]
    if w3.get("inherited_source_ids")!=inherited or by["perry-noble"].get("inherited_source_ids")!=inherited: die("Noble inheritance drift")
    w2ids=set()
    for p in w2["source_shards"]:
        w2ids|={s["id"] for s in load(p)["sources"]}
    if not set(inherited)<=w2ids: die("inherited Noble source missing")

    rows=[]
    for p in w3.get("source_shards",[]):
        sh=load(p)
        if sh.get("authority_id")!=w3.get("authority_id") or not isinstance(sh.get("sources"),list): die(f"{p}: shard drift")
        rows+=sh["sources"]
    if len(rows)!=49: die(f"49 new sources required, found {len(rows)}")
    ids=[]; cnt=Counter(); ac=ex=rp=qs=0
    for s in rows:
        sid=nonempty(s,"id","source"); cid=nonempty(s,"case_id",sid); cl=nonempty(s,"source_class",sid); fs=nonempty(s,"fact_status",sid)
        for k in ("title","issuer","purpose"): nonempty(s,k,sid)
        if cid not in EXPECT or cl not in A|{"B1","C","D"} or fs not in FACT: die(f"{sid}: class/case/fact drift")
        u=s.get("url"); loc=s.get("repository_locator")
        if u is not None and (not isinstance(u,str) or not u.startswith("https://")): die(f"{sid}: HTTPS required")
        if not u and not loc: die(f"{sid}: URL or locator required")
        if not isinstance(s.get("quote_safe"),bool): die(f"{sid}: quote_safe boolean required")
        if s["quote_safe"] and (cl not in A or not u): die(f"{sid}: invalid quote-safe")
        ids.append(sid); cnt[cid]+=1; ac+=cl in A; ex+=bool(u); rp+=bool(loc); qs+=s["quote_safe"]
    if len(ids)!=len(set(ids)) or dict(cnt)!=EXPECT: die(f"source IDs/counts drift: {dict(cnt)}")
    if (ac,ex,rp,qs)!=(33,30,19,14): die(f"quality counters drift: {(ac,ex,rp,qs)}")

    long=[s for s in rows if s["case_id"]=="eddie-long" and s["fact_status"]=="COURT_FILING_ALLEGATION"]
    if len(long)!=2 or any(s["quote_safe"] for s in long): die("Long complaint boundary drift")
    k=next((s for s in rows if s["id"]=="W3-LEN-05"),None)
    if not k or k["fact_status"]!="PARTY_ALLEGATION": die("Kimes allegation boundary missing")
    checks={"carl-lentz":"unpublished Hillsong investigation","andy-savage":"criminally convicted","tullian-tchividjian":"weaponized counseling","steven-lawson":"ministry funds"}
    for cid,needle in checks.items():
        if needle not in " ".join(by[cid]["blocked_claims"]): die(f"{cid}: blocked claim missing")

    w3c={"wave3_decision_records":7,"wave3_new_source_records":49,"wave3_inherited_source_records":7,"wave3_reviewed_source_records":56,"wave3_a_class_sources":ac,"wave3_exact_url_sources":ex,"wave3_repository_capture_sources":rp,"wave3_quote_safe_sources":qs,"effective_core_cases":21,"effective_conditional_cases":1,"effective_dark_side_cases":7,"effective_standalone_cases":3,"effective_hold_cases":1}
    if w3.get("wave3_counters")!=w3c: die("Wave 3 counter drift")
    c1=w1["counters"]; c2=w2["wave2_counters"]
    cum={"source_records":c1["source_records"]+c2["wave2_source_records"]+49,"a_class_sources":c1["a_class_sources"]+c2["wave2_a_class_sources"]+ac,"exact_url_sources":c1["exact_url_sources"]+c2["wave2_exact_url_sources"]+ex,"repository_capture_sources":c1["repository_capture_sources"]+c2["wave2_repository_capture_sources"]+rp,"quote_safe_sources":c1["quote_safe_sources"]+c2["wave2_quote_safe_sources"]+qs}
    if w3.get("cumulative_counters")!=cum: die(f"cumulative drift: {cum}")
    text=(R/"ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/37_WAVE3_DARK_SIDE_REPENTANCE_RESTORATION_2026-08-01.md").read_text(encoding="utf-8")+(R/"00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md").read_text(encoding="utf-8")
    for m in ("184","145","64","PARTY_ALLEGATION","dismissal with prejudice","1 марта 2026","Steven Lawson","Eddie Long"):
        if m not in text: die(f"authority marker missing: {m}")
    print(f"OSK Wave 3 OK: 7 decisions, 49 new + 7 inherited; A={ac}, exact={ex}, quote-safe={qs}; routing unchanged")
if __name__=="__main__": main()
