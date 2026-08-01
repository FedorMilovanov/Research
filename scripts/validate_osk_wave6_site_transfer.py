#!/usr/bin/env python3
"""Fail-closed validation for OSK Wave 6 site-transfer publication ledger."""
from __future__ import annotations
import json, sys
from pathlib import Path
from typing import Any

R=Path(__file__).resolve().parents[1]
LEDGER=R/"data/osk-wave6-site-transfer-ledger-2026-08-01.json"
OVERLAY=R/"data/public-projection-osk-wave6-overlay-2026-08-01.json"
BASE_QUEUE=R/"data/public-projection-queue-2026-08-01.json"
AUTHORITY=R/"ОБРАТНАЯ СТОРОНА КАФЕДРЫ СЕРИЯ/40_WAVE6_SITE_TRANSFER_PUBLICATION_LEDGER_2026-08-01.md"
OVERLAY_MD=R/"PUBLIC_PROJECTION_OSK_WAVE6_OVERLAY_2026-08-01.md"
ROOT_AUTH=R/"00_RESEARCH_CURRENT_AUTHORITY_2026-08-01.md"

CORE={
"sbc-systemic","bill-hybels","brian-houston","rzim","mark-driscoll","james-macdonald",
"cj-mahaney","doug-wilson","bill-gothard","steve-timmis","jonathan-fletcher",
"paige-patterson","jerry-falwell-jr","mike-pilavachi","mike-bickle","robert-morris",
"nikolay-kuznetsov","evgeny-shin","stanislav-moskvitin","darrin-patrick","bethel-bolz-armstrong"}
CONDITIONAL={"david-platt"}
DARK={"steven-lawson","tullian-tchividjian","sam-allberry","andy-savage","carl-lentz","eddie-long","perry-noble"}
STANDALONE={"paul-wendy-guay","grace-gray","franz-hengsbach","sunday-adelaja"}

def die(m:str)->None:
    print("ERROR:",m,file=sys.stderr); raise SystemExit(1)
def load(p:Path)->dict[str,Any]:
    try: v=json.loads(p.read_text(encoding="utf-8"))
    except Exception as e: die(f"{p.relative_to(R)}: {e}")
    if not isinstance(v,dict): die(f"{p.relative_to(R)}: object required")
    return v
def nonempty(v:Any,c:str)->str:
    if not isinstance(v,str) or not v.strip(): die(f"{c}: non-empty string required")
    return v.strip()

def main()->None:
    ledger=load(LEDGER); overlay=load(OVERLAY); baseq=load(BASE_QUEUE)
    if ledger.get("schema_version")!=1 or ledger.get("authority_id")!="RESEARCH-OSK-AUTHORITY-2026-08-01-W6": die("ledger authority drift")
    if ledger.get("base_authority_id")!="RESEARCH-OSK-AUTHORITY-2026-08-01-W5": die("ledger base chain drift")
    if ledger.get("research_snapshot")!="446a83932d4ec446b4c87e2c7b2fb02aeeee49eb": die("research snapshot drift")
    if ledger.get("product_snapshot")!="efaf2a51b1fcc7b7d3f8c9558ecb5acf849df3b3": die("product snapshot drift")
    policy=ledger.get("policy")
    if not isinstance(policy,dict): die("policy object required")
    for key in ("researchClosureIsNotPublication","preserveConceptualCore","caseNamesRequireOwnerEditorialReview","darkSideAndStandaloneExcludedFromAntiCounselEvidence","productWriteRequiresSeparatePr"):
        if policy.get(key) is not True: die(f"policy {key} must be true")
    for key in ("automaticCaseInsertion","newDirectQuotesApproved"):
        if policy.get(key) is not False: die(f"policy {key} must be false")

    routes=ledger.get("effective_case_routes")
    if not isinstance(routes,dict): die("effective_case_routes required")
    expected={"ANTISOVETY_CORE":CORE,"ANTISOVETY_CONDITIONAL":CONDITIONAL,"DARK_SIDE_SERIES":DARK,"STANDALONE":STANDALONE,"HOLD":set()}
    for key,vals in expected.items():
        got=routes.get(key)
        if not isinstance(got,list) or set(got)!=vals or len(got)!=len(vals): die(f"{key} route set drift")
    all_cases=set().union(*expected.values())
    if len(all_cases)!=33: die("effective routes must cover exactly 33 cases")

    counts=ledger.get("counts")
    expected_counts={"antiCounselPointRecords":20,"futureArticleBundles":10,"coreCases":21,"conditionalCases":1,"darkSideCases":7,"standaloneCases":4,"holdCases":0,"cumulativeSources":290,"aClassSources":216,"exactUrlSources":197,"quoteSafeSources":105}
    if counts!=expected_counts: die(f"ledger count drift: {counts}")

    decision=ledger.get("existing_article_decision")
    if not isinstance(decision,dict): die("existing_article_decision required")
    if decision.get("disposition")!="REFERENCE" or decision.get("siteAction")!="PRESERVE_BODY_NO_CASE_ROSTER": die("article disposition drift")
    if decision.get("holds")!=["PUBLICATION_HOLD"]: die("article must retain only PUBLICATION_HOLD")
    if ledger.get("existing_route")!="/articles/20-antisovetov-pastoru/": die("existing route drift")
    if ledger.get("canonical_product_source")!="src/components/article-pilots/antisovetov/AntisovetovBody.astro": die("canonical source drift")

    points=ledger.get("point_records")
    if not isinstance(points,list) or len(points)!=20: die("exactly 20 point records required")
    seen=set()
    for p in points:
        if not isinstance(p,dict): die("point object required")
        n=p.get("pointNumber"); pid=p.get("id")
        if n not in range(1,21) or pid!=f"AS-{n:02d}" or n in seen: die(f"point identity drift: {pid}/{n}")
        seen.add(n)
        nonempty(p.get("heading"),pid); nonempty(p.get("claimBoundary"),pid)
        if p.get("existingAnchor")!=f"point-{n}": die(f"{pid}: anchor drift")
        if p.get("siteAction")!="PRESERVE_CONCEPTUAL_CORE" or p.get("bodyCaseInsertionApproved") is not False: die(f"{pid}: product insertion must remain blocked")
        if p.get("quoteMode")!="NO_NEW_DIRECT_QUOTES": die(f"{pid}: quote mode drift")
        primary=p.get("primaryCaseIds"); supporting=p.get("supportingCaseIds"); conditional=p.get("conditionalCaseIds")
        if not isinstance(primary,list) or not primary: die(f"{pid}: primary core evidence required")
        if not set(primary)<=CORE or not set(supporting or [])<=CORE: die(f"{pid}: non-core case entered primary/supporting evidence")
        if not set(conditional or [])<=CONDITIONAL: die(f"{pid}: invalid conditional case")
        if set(primary)&(DARK|STANDALONE) or set(supporting or [])&(DARK|STANDALONE): die(f"{pid}: dark/standalone evidence leak")
        if p.get("excludedRouteClasses")!=["DARK_SIDE_SERIES","STANDALONE"]: die(f"{pid}: exclusion contract drift")
    if seen!=set(range(1,21)): die("point number coverage drift")
    conditional_points={p["pointNumber"] for p in points if p.get("conditionalCaseIds")}
    if conditional_points!={4,19}: die(f"David Platt may appear only in points 4 and 19: {conditional_points}")

    bundles=ledger.get("future_article_bundles")
    if not isinstance(bundles,list) or len(bundles)!=10: die("exactly 10 future article bundles required")
    ids=set(); bundle_cases=set()
    for b in bundles:
        if not isinstance(b,dict): die("bundle object required")
        bid=nonempty(b.get("id"),"bundle"); ids.add(bid)
        route=nonempty(b.get("routeCandidate"),bid)
        if not route.startswith("/") or not route.endswith("/"): die(f"{bid}: invalid route candidate")
        nonempty(b.get("title"),bid); nonempty(b.get("publicationBoundary"),bid)
        cases=b.get("caseIds")
        if not isinstance(cases,list) or not cases or not set(cases)<=all_cases: die(f"{bid}: invalid case list")
        bundle_cases.update(cases)
    if len(ids)!=10: die("duplicate bundle ids")
    if not CORE<=bundle_cases or not DARK<=bundle_cases or not STANDALONE<=bundle_cases: die("future bundles must route all core/dark/standalone cases")
    if CONDITIONAL & bundle_cases: die("conditional comparator must not receive an automatic future article bundle")

    if overlay.get("schema_version")!=1 or overlay.get("authority_id")!="A06-OSK-WAVE6-PROJECTION-2026-08-01": die("overlay authority drift")
    if overlay.get("base_authority_id")!=baseq.get("authorityId"): die("overlay base authority drift")
    if overlay.get("supersedes_queue_record_id")!="osk-power-dark-side-standalone": die("overlay target drift")
    base_record=next((r for r in baseq.get("records",[]) if r.get("id")=="osk-power-dark-side-standalone"),None)
    if not base_record or base_record.get("disposition")!="BLOCKED" or "EVIDENCE_HOLD" not in base_record.get("holds",[]): die("expected stale A06 base record not found")
    effective=overlay.get("effective_record")
    if not isinstance(effective,dict) or effective.get("disposition")!="REFERENCE": die("effective overlay disposition drift")
    if effective.get("holds")!=["PUBLICATION_HOLD"]: die("overlay must remove EVIDENCE_HOLD but retain PUBLICATION_HOLD")
    if effective.get("researchStatus")!="WAVES_1_TO_5_EVIDENCE_CLOSED_290_SOURCES_WAVE6_LEDGER_READY": die("overlay research status drift")
    if overlay.get("effective_projection_counts")!={"PROMOTE":0,"REFERENCE":4,"SUPERSEDED":0,"BLOCKED":6,"total":10}: die("effective A06 counts drift")

    for authority in effective.get("sourceAuthorities",[]):
        if not (R/authority).exists(): die(f"overlay source authority missing: {authority}")

    text=AUTHORITY.read_text(encoding="utf-8")+OVERLAY_MD.read_text(encoding="utf-8")+ROOT_AUTH.read_text(encoding="utf-8")
    for marker in ("Wave 6","290","216","105","PRESERVE_BODY_NO_CASE_ROSTER","REFERENCE / PUBLICATION_HOLD","10 editorial bundles","NO PRODUCT WRITE"):
        if marker not in text: die(f"authority marker missing: {marker}")
    print("OSK Wave 6 OK: 20 point records, 10 future bundles, 33 routed cases; A06 OSK effective REFERENCE with PUBLICATION_HOLD and 0 PROMOTE")

if __name__=="__main__": main()
