#!/usr/bin/env python3
"""Read-only acquisition/diagnostic lane for the G3 FY2022 real-estate question.

Targets only public, unauthenticated government/search surfaces:
- Douglas County / Georgia DOR authority pages;
- Douglas County qPublic assessor search;
- GSCCCA Real Estate Index name-search landing/form.

The tool never logs in, creates an account, pays, orders copies, records documents,
or submits any filing. Search/access failures are preserved as transport/access
results and are never converted into evidence that a deed/property does not exist.
"""
from __future__ import annotations

import argparse
import hashlib
import http.cookiejar
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

UA = "FedorMilovanov-Research-G3-Property-Acquisition/1.0 (research-only; read-only public records)"

COUNTY_CLERK = "https://www.douglascountyga.gov/193/Clerk-of-Superior-Court"
GA_DOR = "https://dor.georgia.gov/property-records-online"
QP_SEARCH = "https://qpublic.schneidercorp.com/Application.aspx?App=DouglasCountyGA&Layer=Parcels&PageType=Search"
QP_GLOBAL = "https://qpublic.schneidercorp.com/Search"
GSCCCA = "https://search.gsccca.org/RealEstate/namesearch.asp"

QUERIES = [
    "G3 MINISTRIES FOR THE CHURCH INC",
    "G3 MINISTRIES FOR THE CHURCH",
    "PRAYS MILL BAPTIST CHURCH INC",
    "4979 HIGHWAY 5",
    "0038025021",
]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def writej(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]
    def handle_data(self, d):
        x=" ".join(d.split())
        if x: self.parts.append(x)


def textify(b: bytes) -> str:
    p=TextParser(); p.feed(b.decode("utf-8", "replace")); return "\n".join(p.parts)


class FormSchemaParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.forms=[]; self.current=None; self.select=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag.lower()=="form":
            self.current={"action":a.get("action"),"method":(a.get("method") or "GET").upper(),"inputs":[],"selects":[]}
            self.forms.append(self.current)
        elif self.current is not None and tag.lower()=="input":
            self.current["inputs"].append({k:a.get(k) for k in ("name","type","value","id")})
        elif self.current is not None and tag.lower()=="select":
            self.select={"name":a.get("name"),"id":a.get("id"),"options":[]}
            self.current["selects"].append(self.select)
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
    cj=http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))


def fetch(op, url: str, timeout: int=90):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,application/xhtml+xml,*/*"})
    started=time.time()
    try:
        with op.open(req,timeout=timeout) as r:
            b=r.read()
            return b,{"requested_url":url,"final_url":r.geturl(),"status":getattr(r,"status",None),
                      "content_type":r.headers.get("Content-Type"),"bytes":len(b),"sha256":sha(b),
                      "elapsed_seconds":round(time.time()-started,3)}
    except urllib.error.HTTPError as e:
        body=e.read()
        return body,{"requested_url":url,"final_url":e.geturl(),"status":e.code,"reason":str(e.reason),
                     "content_type":e.headers.get("Content-Type"),"bytes":len(body),"sha256":sha(body),
                     "elapsed_seconds":round(time.time()-started,3)}
    except Exception as e:
        return b"",{"requested_url":url,"status":None,"error":repr(e),"bytes":0,
                    "elapsed_seconds":round(time.time()-started,3)}


def save_fetch(out: Path, stem: str, body: bytes, meta: dict):
    (out/f"{stem}.html").write_bytes(body)
    (out/f"{stem}.txt").write_text(textify(body),encoding="utf-8")
    writej(out/f"{stem}_FETCH.json",meta)


def qpublic_checks(op, out: Path):
    results=[]
    body,meta=fetch(op,QP_SEARCH); save_fetch(out,"QP_SEARCH_LANDING",body,meta)
    results.append({"kind":"landing","fetch":meta,"text_sha256":sha(textify(body).encode())})
    for i,q in enumerate(QUERIES,1):
        url=QP_GLOBAL+"?"+urllib.parse.urlencode({"q":q})
        b,m=fetch(op,url); save_fetch(out,f"QP_QUERY_{i}",b,m)
        txt=textify(b)
        results.append({"kind":"query","query":q,"fetch":m,
                        "query_present":q.upper() in txt.upper(),
                        "g3_present":"G3 MINISTRIES" in txt.upper(),
                        "prays_mill_present":"PRAYS MILL" in txt.upper(),
                        "parcel_present":"0038025021" in re.sub(r"\D","",txt)})
    return results


def gsccca_checks(op, out: Path):
    body,meta=fetch(op,GSCCCA); save_fetch(out,"GSCCCA_NAME_SEARCH",body,meta)
    parser=FormSchemaParser()
    try: parser.feed(body.decode("utf-8","replace"))
    except Exception: pass
    writej(out/"GSCCCA_FORM_SCHEMA.json",parser.forms)
    txt=textify(body)
    return {"fetch":meta,"forms_found":len(parser.forms),
            "mentions_real_estate_index":"Real Estate" in txt,
            "mentions_search_name":"Search Name" in txt,
            "mentions_login":"Login" in txt,
            "note":"No authenticated or paid search is attempted. Form schema is preserved for a later fail-closed public-query patch if the unauthenticated endpoint permits it."}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",default="g3-douglas-property-output")
    a=ap.parse_args(); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    op=opener(); summary={"state":"EPHEMERAL_ACTION_ARTIFACT","publication_eligible":False,
                          "queries":QUERIES,"authority":{},"qpublic":[],"gsccca":{},"errors":[]}

    for stem,url in (("DOUGLAS_CLERK",COUNTY_CLERK),("GA_DOR_PROPERTY_RECORDS",GA_DOR)):
        b,m=fetch(op,url); save_fetch(out,stem,b,m); summary["authority"][stem]=m

    try: summary["qpublic"]=qpublic_checks(op,out)
    except Exception as e: summary["errors"].append({"stage":"qpublic","error":repr(e)})
    try: summary["gsccca"]=gsccca_checks(op,out)
    except Exception as e: summary["errors"].append({"stage":"gsccca","error":repr(e)})

    summary["closure_boundary"]={
        "property_identity_closed":False,
        "deed_chain_closed":False,
        "counterparty_closed":False,
        "receivable_terms_closed":False,
        "warning":"Transport/access results are not negative evidence. No property is identified as the FY2022 $590k donation without official assessor/deed evidence."
    }
    writej(out/"SUMMARY.json",summary)
    print(json.dumps({"authority":summary["authority"],"qpublic_attempts":len(summary["qpublic"]),
                      "gsccca":summary["gsccca"],"errors":summary["errors"]},indent=2))
    # Diagnostic lane is successful when it preserved the government authority and attempted both routes.
    return 0

if __name__=="__main__":
    raise SystemExit(main())
