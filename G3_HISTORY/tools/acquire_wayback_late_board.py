#!/usr/bin/env python3
"""Acquire late-2026 archived G3 Who-We-Are pages from the Internet Archive.

Read-only research helper. It queries CDX for captures around the August 2026
crisis, fetches exact `id_` snapshot bytes, records SHA-256/custody metadata and
extracts plain text/name hits. Nothing is promoted to publication automatically.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys, time, urllib.error, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path

TARGET='http://g3min.org/about/who-we-are/'
KNOWN='20260721102641'
NAMES=['Buck Braswell','Matt Broome','Jon Norton','Matt Sikes','Dylan Joyner','Ron Mooney']
UA='FedorMilovanov-Research-G3-Wayback-Acquisition/1.0 (research-only)'

def sha(b): return hashlib.sha256(b).hexdigest()
def writej(p,o): p.write_text(json.dumps(o,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')
class Text(HTMLParser):
    def __init__(self): super().__init__(); self.p=[]
    def handle_data(self,d):
        s=' '.join(d.split())
        if s: self.p.append(s)
def txt(b):
    p=Text(); p.feed(b.decode('utf-8','replace')); return '\n'.join(p.p)
def get(url,timeout=90):
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'*/*'}); st=time.time()
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            b=r.read(); return b,{'requested_url':url,'final_url':r.geturl(),'status':getattr(r,'status',None),'content_type':r.headers.get('Content-Type'),'bytes':len(b),'sha256':sha(b),'elapsed_seconds':round(time.time()-st,3)}
    except urllib.error.HTTPError as e:
        body=e.read(); raise RuntimeError(f'HTTP {e.code} {e.reason} url={url} body_sha256={sha(body)} bytes={len(body)}') from e
    except urllib.error.URLError as e: raise RuntimeError(f'URL error {e.reason} url={url}') from e

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',default='g3-wayback-late-board-output'); a=ap.parse_args(); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    cdx='https://web.archive.org/cdx/search/cdx?'+urllib.parse.urlencode({'url':'g3min.org/about/who-we-are/','from':'20260721','to':'20260831','output':'json','fl':'timestamp,original,statuscode,mimetype,digest,length','filter':'statuscode:200','collapse':'digest'})
    summary={'target':TARGET,'known_snapshot':KNOWN,'errors':[],'captures':[],'state':'EPHEMERAL_ACTION_ARTIFACT','publication_eligible':False}
    try:
        b,m=get(cdx); (out/'CDX.json').write_bytes(b); writej(out/'CDX_FETCH.json',m); rows=json.loads(b.decode('utf-8'))
        if not isinstance(rows,list) or not rows: raise RuntimeError('CDX response has no rows')
        hdr=rows[0]; captures=[dict(zip(hdr,r)) for r in rows[1:] if len(r)==len(hdr)]
    except Exception as e:
        captures=[]; summary['errors'].append('CDX: '+str(e))
    if not captures: captures=[{'timestamp':KNOWN,'original':TARGET,'statuscode':'unknown','mimetype':'unknown','digest':'unknown','length':'unknown','fallback_known_locator':True}]
    # Ensure the known exact target is attempted even if CDX collapse omits it.
    if not any(c.get('timestamp')==KNOWN for c in captures): captures.insert(0,{'timestamp':KNOWN,'original':TARGET,'fallback_known_locator':True})
    seen=set()
    for c in captures[:30]:
        ts=c.get('timestamp',''); orig=c.get('original') or TARGET
        if not ts or ts in seen: continue
        seen.add(ts); url=f'https://web.archive.org/web/{ts}id_/{orig}'
        rec={'cdx':c,'snapshot_url':url}
        try:
            body,meta=get(url,120); fn=f'{ts}_who-we-are.html'; (out/fn).write_bytes(body); t=txt(body); (out/f'{ts}_who-we-are.txt').write_text(t,encoding='utf-8'); hits={n:(n.lower() in t.lower()) for n in NAMES}; rec.update({'fetch':meta,'text_sha256':sha(t.encode()),'name_hits':hits,'all_six_names_present':all(hits.values())})
        except Exception as e: rec['error']=str(e)
        summary['captures'].append(rec)
    writej(out/'SUMMARY.json',summary)
    ok=[c for c in summary['captures'] if c.get('fetch')]
    if not ok:
        for e in summary['errors']: print('ERROR',e,file=sys.stderr)
        for c in summary['captures']: print('ERROR snapshot',c.get('snapshot_url'),c.get('error'),file=sys.stderr)
        return 2
    for c in ok: print('ACQUIRED',c['cdx'].get('timestamp'),'all6=',c.get('all_six_names_present'))
    return 0
if __name__=='__main__': raise SystemExit(main())
