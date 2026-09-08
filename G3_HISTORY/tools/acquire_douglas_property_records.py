#!/usr/bin/env python3
"""Read-only acquisition lane for the G3 FY2022 real-estate question.

Targets only public, unauthenticated government/search surfaces:
- Douglas County / Georgia DOR authority pages;
- Douglas County qPublic assessor search (diagnostic only; currently Cloudflare-blocked);
- GSCCCA Real Estate Index public Name Search.

The tool never logs in, creates an account, pays, orders copies, records documents,
uses premium-only search features, or submits any filing. Search/access failures are
preserved as transport/access results and are never converted into evidence that a
deed/property does not exist.
"""
from __future__ import annotations

import argparse, hashlib, http.cookiejar, json, re, time, urllib.error, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

UA = "FedorMilovanov-Research-G3-Property-Acquisition/2.0 (research-only; read-only public records)"
COUNTY_CLERK = "https://www.douglascountyga.gov/193/Clerk-of-Superior-Court"
GA_DOR = "https://dor.georgia.gov/property-records-online"
QP_SEARCH = "https://qpublic.schneidercorp.com/Application.aspx?App=DouglasCountyGA&Layer=Parcels&PageType=Search"
QP_GLOBAL = "https://qpublic.schneidercorp.com/Search"
GSCCCA = "https://search.gsccca.org/RealEstate/namesearch.asp"
GSCCCA_BASE = "https://search.gsccca.org/RealEstate/"
DOUGLAS_COUNTY_ID = "48"
SEARCH_FROM = "01/01/2021"
SEARCH_TO = "12/31/2024"
NAME_QUERIES = [
    "G3 MINISTRIES FOR THE CHURCH INC",
    "G3 MINISTRIES FOR THE CHURCH",
    "G3 MINISTRIES",
    "PRAYS MILL BAPTIST CHURCH INC",
]
QP_QUERIES = NAME_QUERIES + ["4979 HIGHWAY 5", "0038025021"]

def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def writej(path: Path, obj: Any) -> None: path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True),encoding="utf-8")

class TextParser(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self,d):
        x=" ".join(d.split())
        if x: self.parts.append(x)

def textify(b: bytes) -> str:
    p=TextParser(); p.feed(b.decode("utf-8","replace")); return "\n".join(p.parts)

class FormSchemaParser(HTMLParser):
    def __init__(self): super().__init__(); self.forms=[]; self.current=None; self.select=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag.lower()=="form":
            self.current={"action":a.get("action"),"method":(a.get("method") or "GET").upper(),"inputs":[],"selects":[]}
            self.forms.append(self.current)
        elif self.current is not None and tag.lower()=="input":
            self.current["inputs"].append({k:a.get(k) for k in ("name","type","value","id")})
        elif self.current is not None and tag.lower()=="select":
            self.select={"name":a.get("name"),"id":a.get("id"),"options":[]}; self.current["selects"].append(self.select)
        elif self.current is not None and self.select is not None and tag.lower()=="option":
            self.select["options"].append({"value":a.get("value"),"text":""})
    def handle_data(self,d):
        if self.select is not None and self.select["options"]:
            t=" ".join(d.split())
            if t: self.select["options"][-1]["text"] += (" " if self.select["options"][-1]["text"] else "") + t
    def handle_endtag(self,tag):
        if tag.lower()=="select": self.select=None
        elif tag.lower()=="form": self.current=None

def opener():
    cj=http.cookiejar.CookieJar(); return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def fetch(op,url: str,timeout: int=90,method: str="GET",data: bytes|None=None,referer: str|None=None):
    headers={"User-Agent":UA,"Accept":"text/html,application/xhtml+xml,*/*"}
    if data is not None: headers["Content-Type"]="application/x-www-form-urlencoded"
    if referer: headers["Referer"]=referer
    req=urllib.request.Request(url,data=data,headers=headers,method=method); started=time.time()
    try:
        with op.open(req,timeout=timeout) as r:
            b=r.read(); return b,{"requested_url":url,"final_url":r.geturl(),"method":method,"status":getattr(r,"status",None),"content_type":r.headers.get("Content-Type"),"bytes":len(b),"sha256":sha(b),"elapsed_seconds":round(time.time()-started,3)}
    except urllib.error.HTTPError as e:
        body=e.read(); return body,{"requested_url":url,"final_url":e.geturl(),"method":method,"status":e.code,"reason":str(e.reason),"content_type":e.headers.get("Content-Type"),"bytes":len(body),"sha256":sha(body),"elapsed_seconds":round(time.time()-started,3)}
    except Exception as e:
        return b"",{"requested_url":url,"method":method,"status":None,"error":repr(e),"bytes":0,"elapsed_seconds":round(time.time()-started,3)}

def save_fetch(out: Path,stem: str,body: bytes,meta: dict):
    (out/f"{stem}.html").write_bytes(body); (out/f"{stem}.txt").write_text(textify(body),encoding="utf-8"); writej(out/f"{stem}_FETCH.json",meta)

def qpublic_checks(op,out: Path):
    results=[]
    body,meta=fetch(op,QP_SEARCH); save_fetch(out,"QP_SEARCH_LANDING",body,meta)
    results.append({"kind":"landing","fetch":meta,"text_sha256":sha(textify(body).encode())})
    for i,q in enumerate(QP_QUERIES,1):
        url=QP_GLOBAL+"?"+urllib.parse.urlencode({"q":q}); b,m=fetch(op,url); save_fetch(out,f"QP_QUERY_{i}",b,m); txt=textify(b)
        results.append({"kind":"query","query":q,"fetch":m,"query_present":q.upper() in txt.upper(),"g3_present":"G3 MINISTRIES" in txt.upper(),"prays_mill_present":"PRAYS MILL" in txt.upper(),"cloudflare_challenge":"Just a moment" in txt or "challenge-error" in txt,"text_preview":txt[:700]})
    return results

def hidden_defaults(form: dict) -> dict[str,str]:
    out={}
    for inp in form.get("inputs",[]):
        n=inp.get("name"); typ=(inp.get("type") or "").lower(); val=inp.get("value")
        if n and typ=="hidden" and val is not None: out[n]=val
    return out

def gsccca_public_name_queries(op,out: Path,form: dict) -> list[dict]:
    action=form.get("action") or "names.asp?Type=0"
    endpoint=urllib.parse.urljoin(GSCCCA_BASE,action)
    base=hidden_defaults(form)
    records=[]
    seq=0
    for name in NAME_QUERIES:
        for include_mode in ("1","0"):
            seq += 1
            payload=dict(base)
            payload.update({
                "txtSearchType":"0",
                "bolInclude":include_mode,
                "txtSearchName":name,
                "txtFromDate":SEARCH_FROM,
                "txtToDate":SEARCH_TO,
                "txtPartyType":"2",
                "txtInstrCode":"ALL",
                "intCountyID":DOUGLAS_COUNTY_ID,
                "MaxRows":"100",
                "TableType":"1",
            })
            data=urllib.parse.urlencode(payload).encode()
            body,meta=fetch(op,endpoint,120,"POST",data,GSCCCA)
            stem=f"GSCCCA_RESULT_{seq:02d}"
            save_fetch(out,stem,body,meta)
            txt=textify(body); upper=txt.upper()
            rec={
                "query":name,
                "bolInclude":include_mode,
                "county_id":DOUGLAS_COUNTY_ID,
                "date_from":SEARCH_FROM,
                "date_to":SEARCH_TO,
                "party_type":"2",
                "instrument":"ALL",
                "payload_sha256":sha(data),
                "fetch":meta,
                "query_name_present":name.upper() in upper,
                "g3_present":"G3 MINISTRIES" in upper,
                "prays_mill_present":"PRAYS MILL" in upper,
                "login_language_present":"LOGIN" in upper,
                "book_language_present":"BOOK" in upper,
                "page_language_present":"PAGE" in upper,
                "grantor_language_present":"GRANTOR" in upper,
                "grantee_language_present":"GRANTEE" in upper,
                "no_records_language_present":any(x in upper for x in ("NO RECORDS","NO RESULTS","NO MATCH")),
                "text_preview":txt[:2500],
                "artifact_stem":stem,
            }
            records.append(rec)
    return records

def gsccca_checks(op,out: Path):
    body,meta=fetch(op,GSCCCA); save_fetch(out,"GSCCCA_NAME_SEARCH",body,meta)
    parser=FormSchemaParser()
    try: parser.feed(body.decode("utf-8","replace"))
    except Exception: pass
    writej(out/"GSCCCA_FORM_SCHEMA.json",parser.forms); txt=textify(body)
    name_form=next((f for f in parser.forms if (f.get("action") or "").lower().startswith("names.asp")),None)
    public_results=[]
    if name_form:
        public_results=gsccca_public_name_queries(op,out,name_form)
    return {"fetch":meta,"forms_found":len(parser.forms),"form_schema":parser.forms,"public_name_form_found":bool(name_form),"public_query_results":public_results,"mentions_real_estate_index":"Real Estate" in txt,"mentions_search_name":"Search Name" in txt,"mentions_login":"Login" in txt,"note":"Only the public Real Estate Name Search form is submitted. No login, premium search, payment, document purchase, or filing occurs."}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",default="g3-douglas-property-output"); a=ap.parse_args(); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    op=opener(); summary={"state":"EPHEMERAL_ACTION_ARTIFACT","publication_eligible":False,"name_queries":NAME_QUERIES,"search_window":{"from":SEARCH_FROM,"to":SEARCH_TO,"county_id":DOUGLAS_COUNTY_ID},"authority":{},"qpublic":[],"gsccca":{},"errors":[]}
    for stem,url in (("DOUGLAS_CLERK",COUNTY_CLERK),("GA_DOR_PROPERTY_RECORDS",GA_DOR)):
        b,m=fetch(op,url); save_fetch(out,stem,b,m); summary["authority"][stem]=m
    try: summary["qpublic"]=qpublic_checks(op,out)
    except Exception as e: summary["errors"].append({"stage":"qpublic","error":repr(e)})
    try: summary["gsccca"]=gsccca_checks(op,out)
    except Exception as e: summary["errors"].append({"stage":"gsccca","error":repr(e)})
    summary["closure_boundary"]={"property_identity_closed":False,"deed_chain_closed":False,"counterparty_closed":False,"receivable_terms_closed":False,"warning":"Search results require document-level inspection before property identity, donor, buyer, consideration, or note terms can be asserted. Transport/access failure is never negative evidence."}
    writej(out/"SUMMARY.json",summary)
    compact={"authority":summary["authority"],"qpublic_statuses":[r.get("fetch",{}).get("status") for r in summary["qpublic"]],"gsccca_public_name_form_found":summary.get("gsccca",{}).get("public_name_form_found"),"gsccca_queries":summary.get("gsccca",{}).get("public_query_results",[]),"errors":summary["errors"],"closure_boundary":summary["closure_boundary"]}
    print("=== G3 DOUGLAS PROPERTY PUBLIC NAME-SEARCH ACQUISITION ===")
    print(json.dumps(compact,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__": raise SystemExit(main())
