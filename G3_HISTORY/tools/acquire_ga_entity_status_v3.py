#!/usr/bin/env python3
"""Read-only acquisition of current Georgia eCorp entity status for G3.

The Georgia search-result page itself is treated as sufficient current-state
government evidence when it returns the exact control number and a parsable
row. BusinessInformation detail acquisition remains a best-effort upgrade;
absence of an internal businessId must not turn a valid official search result
into a false-negative workflow failure.
"""
from __future__ import annotations
import argparse, hashlib, http.cookiejar, json, re, sys, time, urllib.error, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE='https://ecorp.sos.ga.gov'
SEARCH=BASE+'/BusinessSearch'
CONTROL='19085916'
EXPECTED_NAME='G3 Ministries for the Church, Inc.'
UA='FedorMilovanov-Research-G3-Georgia-Acquisition/3.1 (research-only)'

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
    cj=http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def do(op,url,method='GET',data=None,referer=None,timeout=60):
    hdr={'User-Agent':UA,'Accept':'text/html,application/xhtml+xml,*/*'}
    if referer: hdr['Referer']=referer
    if data is not None: hdr['Content-Type']='application/x-www-form-urlencoded'
    req=urllib.request.Request(url,data=data,headers=hdr,method=method); st=time.time()
    try:
        with op.open(req,timeout=timeout) as r:
            b=r.read()
            return b,{'requested_url':url,'final_url':r.geturl(),'method':method,
                      'status':getattr(r,'status',None),'content_type':r.headers.get('Content-Type'),
                      'bytes':len(b),'sha256':sha(b),'elapsed_seconds':round(time.time()-st,3)}
    except urllib.error.HTTPError as e:
        body=e.read()
        return body,{'requested_url':url,'final_url':e.geturl(),'method':method,
                     'status':e.code,'reason':str(e.reason),'content_type':e.headers.get('Content-Type'),
                     'bytes':len(body),'sha256':sha(body),'elapsed_seconds':round(time.time()-st,3)}

def candidate_payloads():
    obj={'SearchType':'ControlNo','SearchValue':CONTROL,'SearchCriteria':'Contains'}
    return [
      ('json_search', urllib.parse.urlencode({'search':json.dumps(obj,separators=(',',':'))}).encode()),
      ('mvc_dotted', urllib.parse.urlencode({'search.SearchType':'ControlNo','search.SearchValue':CONTROL,'search.SearchCriteria':'Contains'}).encode()),
      ('flat_fields', urllib.parse.urlencode(obj).encode()),
      ('form_controls', urllib.parse.urlencode({'SearchType':'ControlNo','txtControlNo':CONTROL,'SearchCriteria':'Contains'}).encode()),
    ]

def business_ids(s):
    # Georgia's current search-result grid navigates via JavaScript rather than
    # exposing a literal BusinessInformation?businessId=... href. Preserve the
    # older patterns too because the public markup has changed over time.
    pats=[
        r'navigateToBusinessInfo\(\s*(\d+)\s*,',
        r'BusinessInformation\?businessId=(\d+)',
        r'businessId[=:"\']+(\d+)',
        r'/BusinessSearch/BusinessInformation/(\d+)',
    ]
    out=[]
    for p in pats:
        for m in re.findall(p,s,re.I):
            if m not in out: out.append(m)
    return out

def parse_result_row(t):
    lines=[x.strip() for x in t.splitlines() if x.strip()]
    for i,x in enumerate(lines):
        if x==CONTROL and i>=1 and i+4 < len(lines):
            row={
                'business_name':lines[i-1],
                'control_number':x,
                'business_type':lines[i+1],
                'principal_office_address':lines[i+2],
                'registered_agent':lines[i+3],
                'status':lines[i+4],
            }
            if 'G3 Ministries' in row['business_name']:
                return row
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',default='g3-georgia-entity-output')
    a=ap.parse_args()
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    op=opener()
    summary={'control_number':CONTROL,'attempts':[],'errors':[],
             'state':'EPHEMERAL_ACTION_ARTIFACT','publication_eligible':False}
    home,hm=do(op,SEARCH)
    (out/'BUSINESS_SEARCH.html').write_bytes(home); writej(out/'BUSINESS_SEARCH_FETCH.json',hm)

    found=[]; verified_row=None
    for idx,(name,payload) in enumerate(candidate_payloads(),1):
        b,m=do(op,SEARCH,'POST',payload,SEARCH)
        fn=f'SEARCH_RESPONSE_{idx}_{name}.html'
        (out/fn).write_bytes(b)
        t=textify(b)
        (out/f'SEARCH_RESPONSE_{idx}_{name}.txt').write_text(t,encoding='utf-8')
        decoded=b.decode('utf-8','replace')
        ids=business_ids(decoded)
        row=parse_result_row(t)
        rec={'name':name,'payload_sha256':sha(payload),'response':m,
             'control_present':CONTROL in t or CONTROL in decoded,
             'business_ids':ids,'parsed_result':row}
        summary['attempts'].append(rec)
        for x in ids:
            if x not in found: found.append(x)
        if row and row['business_name']==EXPECTED_NAME:
            verified_row={'attempt':name,'response_sha256':m['sha256'],**row}
            break

    if not verified_row:
        summary['errors'].append('Exact G3 search-result row was not acquired from public BusinessSearch')
        writej(out/'SUMMARY.json',summary)
        return 2

    summary['verified_search_result']=verified_row
    summary['business_ids']=found
    details=[]
    for bid in found[:5]:
        for u in [BASE+f'/BusinessSearch/BusinessInformation?businessId={bid}',
                  BASE+f'/BusinessSearch/BusinessInformation/{bid}']:
            b,m=do(op,u,'GET',None,SEARCH); txt=textify(b)
            if CONTROL in txt or 'G3 Ministries' in txt:
                (out/f'BUSINESS_INFORMATION_{bid}.html').write_bytes(b)
                (out/f'BUSINESS_INFORMATION_{bid}.txt').write_text(txt,encoding='utf-8')
                details.append({'business_id':bid,'url':u,'fetch':m,
                                'control_present':CONTROL in txt,
                                'name_present':'G3 Ministries' in txt,
                                'text_sha256':sha(txt.encode())})
                break
    summary['details']=details
    summary['detail_upgrade_acquired']=bool(details)
    writej(out/'SUMMARY.json',summary)
    print('ACQUIRED Georgia current status:',verified_row['status'],
          'agent=',verified_row['registered_agent'],
          'business_ids=',','.join(found) if found else 'none',
          'detail_upgrade=',bool(details))
    return 0

if __name__=='__main__':
    raise SystemExit(main())