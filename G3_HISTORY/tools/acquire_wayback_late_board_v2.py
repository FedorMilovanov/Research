#!/usr/bin/env python3
"""Acquire and decode late-2026 archived G3 Who-We-Are pages.

Read-only research helper. Preserves exact Internet Archive response bytes and,
when the archived payload is transport-compressed (currently Zstandard), also
stores a decoded HTML representation for text/name verification. Raw and
decoded hashes are recorded separately. Nothing is publication-authorized.
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, subprocess, sys, time, urllib.error, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path

TARGET='http://g3min.org/about/who-we-are/'
KNOWN='20260721102641'
NAMES=['Buck Braswell','Matt Broome','Jon Norton','Matt Sikes','Dylan Joyner','Ron Mooney']
UA='FedorMilovanov-Research-G3-Wayback-Acquisition/2.0 (research-only)'
ZSTD_MAGIC=b'\x28\xb5\x2f\xfd'

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
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'*/*'})
    st=time.time()
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            b=r.read()
            return b,{
                'requested_url':url,'final_url':r.geturl(),
                'status':getattr(r,'status',None),
                'content_type':r.headers.get('Content-Type'),
                'content_encoding':r.headers.get('Content-Encoding'),
                'bytes':len(b),'sha256':sha(b),
                'elapsed_seconds':round(time.time()-st,3)
            }
    except urllib.error.HTTPError as e:
        body=e.read()
        raise RuntimeError(f'HTTP {e.code} {e.reason} url={url} body_sha256={sha(body)} bytes={len(body)}') from e
    except urllib.error.URLError as e:
        raise RuntimeError(f'URL error {e.reason} url={url}') from e

def decode_archived_payload(raw):
    """Return decoded bytes + method. Preserve raw bytes regardless."""
    if raw.startswith(ZSTD_MAGIC):
        zstd=shutil.which('zstd')
        if not zstd:
            raise RuntimeError('Zstandard payload detected but zstd CLI is unavailable')
        p=subprocess.run([zstd,'-d','-q','-c'],input=raw,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if p.returncode:
            raise RuntimeError('zstd decode failed: '+p.stderr.decode('utf-8','replace')[:500])
        return p.stdout,'zstd-cli'
    return raw,'identity'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',default='g3-wayback-late-board-output')
    a=ap.parse_args()
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    cdx='https://web.archive.org/cdx/search/cdx?'+urllib.parse.urlencode({
        'url':'g3min.org/about/who-we-are/','from':'20260721','to':'20260831',
        'output':'json','fl':'timestamp,original,statuscode,mimetype,digest,length',
        'filter':'statuscode:200','collapse':'digest'
    })
    summary={'target':TARGET,'known_snapshot':KNOWN,'errors':[],'captures':[],
             'state':'EPHEMERAL_ACTION_ARTIFACT','publication_eligible':False}
    try:
        b,m=get(cdx); (out/'CDX.json').write_bytes(b); writej(out/'CDX_FETCH.json',m)
        rows=json.loads(b.decode('utf-8'))
        if not isinstance(rows,list) or not rows: raise RuntimeError('CDX response has no rows')
        hdr=rows[0]; captures=[dict(zip(hdr,r)) for r in rows[1:] if len(r)==len(hdr)]
    except Exception as e:
        captures=[]; summary['errors'].append('CDX: '+str(e))
    if not captures:
        captures=[{'timestamp':KNOWN,'original':TARGET,'statuscode':'unknown',
                   'mimetype':'unknown','digest':'unknown','length':'unknown',
                   'fallback_known_locator':True}]
    if not any(c.get('timestamp')==KNOWN for c in captures):
        captures.insert(0,{'timestamp':KNOWN,'original':TARGET,'fallback_known_locator':True})

    seen=set()
    for c in captures[:30]:
        ts=c.get('timestamp',''); orig=c.get('original') or TARGET
        if not ts or ts in seen: continue
        seen.add(ts)
        url=f'https://web.archive.org/web/{ts}id_/{orig}'
        rec={'cdx':c,'snapshot_url':url}
        try:
            raw,meta=get(url,120)
            raw_fn=f'{ts}_who-we-are.raw'
            (out/raw_fn).write_bytes(raw)
            decoded,method=decode_archived_payload(raw)
            html_fn=f'{ts}_who-we-are.html'
            (out/html_fn).write_bytes(decoded)
            t=txt(decoded)
            (out/f'{ts}_who-we-are.txt').write_text(t,encoding='utf-8')
            hits={n:(n.casefold() in t.casefold()) for n in NAMES}
            rec.update({
                'fetch':meta,
                'raw_file':raw_fn,'raw_sha256':sha(raw),'raw_bytes':len(raw),
                'decoded_file':html_fn,'decoded_sha256':sha(decoded),'decoded_bytes':len(decoded),
                'decode_method':method,
                'text_sha256':sha(t.encode()),
                'name_hits':hits,
                'all_six_names_present':all(hits.values())
            })
        except Exception as e:
            rec['error']=str(e)
        summary['captures'].append(rec)

    writej(out/'SUMMARY.json',summary)
    ok=[c for c in summary['captures'] if c.get('fetch') and c.get('decoded_file')]
    if not ok:
        for e in summary['errors']: print('ERROR',e,file=sys.stderr)
        for c in summary['captures']:
            print('ERROR snapshot',c.get('snapshot_url'),c.get('error'),file=sys.stderr)
        return 2
    for c in ok:
        print('ACQUIRED',c['cdx'].get('timestamp'),'all6=',c.get('all_six_names_present'),
              'decode=',c.get('decode_method'))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
