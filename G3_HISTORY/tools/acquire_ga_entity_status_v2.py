#!/usr/bin/env python3
"""Read-only acquisition of current Georgia eCorp entity status for G3.

Uses the public BusinessSearch page and submits the control-number search using
several MVC-compatible encodings because the site constructs its form in
JavaScript. Every attempt is preserved. No filing, payment, registration, or
mutation endpoint is touched.
"""
from __future__ import annotations
import argparse, hashlib, html, http.cookiejar, json, re, sys, time, urllib.error, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE='https://ecorp.sos.ga.gov'
SEARCH=BASE+'/BusinessSearch'
CONTROL='19085916'
UA='FedorMilovanov-Research-G3-Georgia-Acquisition/2.0 (research-only)'

def sha(b): return hashlib.sha256(b).hexdigest()
def writej(p,o): p.write_text(json.dumps(o,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')

class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self,d):
        d=' '.join(d.split())
        if d: self.parts.append(d)

def textify(b):
    p=Text(); p.feed(b.decode('utf-8','replace')); return '\n'.join(p.parts)

def opener():
    cj=http.cookiejar.CookieJar(); return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def do(op,url,method='GET',data=None,referer=None,timeout=60):
    hdr={'User-Agent':UA,'Accept':'text/html,application/xhtml+xml,*/*'}
    if referer: hdr['Referer']=referer
    if data is not None: hdr['Content-Type']='application/x-www-form-urlencoded'
    req=urllib.request.Request(url,data=data,headers=hdr,method=method); st=time.time()
    try:
        with op.open(req,timeout=timeout) as r:
            b=r.read(); return b,{'requested_url':url,'final_url':r.geturl(),'method':method,'status':getattr(r,'status',None),'content_type':r.headers.get('Content-Type'),'bytes':len(b),'sha256':sha(b),'elapsed_seconds':round(time.time()-st,3)}
    except urllib.error.HTTPError as e:
        body=e.read(); return body,{'requested_url':url,'final_url':e.geturl(),'method':method,'status':e.code,'reason':str(e.reason),'content_type':e.headers.get('Content-Type'),'bytes':len(body),'sha256':sha(body),'elapsed_seconds':round(time.time()-st,3)}

def candidate_payloads():
    obj={'SearchType':'ControlNo','SearchValue':CONTROL,'SearchCriteria':'Contains'}
    return [
      ('json_search', urllib.parse.urlencode({'search':json.dumps(obj,separators=(',',':'))}).encode()),
      ('mvc_dotted', urllib.parse.urlencode({'search.SearchType':'ControlNo','search.SearchValue':CONTROL,'search.SearchCriteria':'Contains'}).encode()),
      ('flat_fields', urllib.parse.urlencode(obj).encode()),
      ('form_controls', urllib.parse.urlencode({'SearchType':'ControlNo','txtControlNo':CONTROL,'SearchCriteria':'Contains'}).encode()),
    ]

def business_ids(s):
    pats=[r'BusinessInformation\?businessId=(\d+)',r'businessId[=:\"\']+(\d+)',r'/BusinessSearch/BusinessInformation/(\d+)']
    out=[]
    for p in pats:
        for m in re.findall(p,s,re.I):
            if m not in out: out.append(m)
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',default='g3-georgia-entity-output'); a=ap.parse_args(); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    op=opener(); summary={'control_number':CONTROL,'attempts':[],'errors':[],'state':'EPHEMERAL_ACTION_ARTIFACT','publication_eligible':False}
    home,hm=do(op,SEARCH); (out/'BUSINESS_SEARCH.html').write_bytes(home); writej(out/'BUSINESS_SEARCH_FETCH.json',hm)
    found=[]
    for idx,(name,payload) in enumerate(candidate_payloads(),1):
        b,m=do(op,SEARCH,'POST',payload,SEARCH); fn=f'SEARCH_RESPONSE_{idx}_{name}.html'; (out/fn).write_bytes(b); t=textify(b); (out/f'SEARCH_RESPONSE_{idx}_{name}.txt').write_text(t,encoding='utf-8'); ids=business_ids(b.decode('utf-8','replace'))
        hit=(CONTROL in t or CONTROL in b.decode('utf-8','replace'))
        rec={'name':name,'payload_sha256':sha(payload),'response':m,'control_present':hit,'business_ids':ids}; summary['attempts'].append(rec)
        for x in ids:
            if x not in found: found.append(x)
        if found: break
    if not found:
        summary['errors'].append('No businessId discovered from public BusinessSearch responses')
        writej(out/'SUMMARY.json',summary); return 2
    summary['business_ids']=found
    details=[]
    for bid in found[:5]:
        urls=[BASE+f'/BusinessSearch/BusinessInformation?businessId={bid}',BASE+f'/BusinessSearch/BusinessInformation/{bid}']
        ok=None
        for u in urls:
            b,m=do(op,u,'GET',None,SEARCH); txt=textify(b)
            if CONTROL in txt or 'G3 Ministries' in txt:
                ok=(u,b,m,txt); break
        if ok:
            u,b,m,txt=ok; (out/f'BUSINESS_INFORMATION_{bid}.html').write_bytes(b); (out/f'BUSINESS_INFORMATION_{bid}.txt').write_text(txt,encoding='utf-8'); details.append({'business_id':bid,'url':u,'fetch':m,'control_present':CONTROL in txt,'name_present':'G3 Ministries' in txt,'text_sha256':sha(txt.encode())})
    summary['details']=details
    if not details:
        summary['errors'].append('businessId found but BusinessInformation detail could not be verified as G3')
    writej(out/'SUMMARY.json',summary)
    if summary['errors']:
        for e in summary['errors']: print('ERROR:',e,file=sys.stderr)
        return 2
    print('ACQUIRED Georgia BusinessInformation businessId='+details[0]['business_id'])
    return 0
if __name__=='__main__': raise SystemExit(main())
