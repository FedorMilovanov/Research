#!/usr/bin/env python3
"""Robust read-only acquisition of exact G3 IRS e-file XML objects.

Uses official IRS annual indexes and TEOS batch ZIPs. Supports IRS ZIP members
whose compression method is not implemented by Python 3.12 by falling back to
installed archive CLIs (bsdtar/7z/unzip). Raw bytes and custody metadata remain
research-only ephemeral Action artifacts.
"""
from __future__ import annotations

import argparse, csv, hashlib, io, json, shutil, subprocess, sys, time, urllib.error, urllib.request, xml.etree.ElementTree as ET, zipfile
from pathlib import Path
from typing import Any

EIN="842403597"
TARGETS=[
    {"label":"FY2022_ORIGINAL","index_year":2023,"object_id":"202322939349300637","required":["IRS990"],"strict":False,
     "use":"candidate FY2022 Part IX baseline; ProPublica exposes this filing but IRS index may lack XML_BATCH_ID"},
    {"label":"FY2022_LATER","index_year":2023,"object_id":"202340569349300209","required":["IRS990"],"strict":True,
     "use":"later FY2022 filing candidate for authoritative pre-FY2023 Part IX baseline"},
    {"label":"FY2023","index_year":2024,"object_id":"202411429349300611","required":["IRS990","IRS990ScheduleO"],"strict":True,
     "use":"Part IX functional expenses and Schedule O"},
    {"label":"FY2024","index_year":2025,"object_id":"202541359349304489","required":["IRS990","IRS990ScheduleL","IRS990ScheduleO"],"strict":True,
     "use":"Schedule L interested-person rows and filing context"},
    {"label":"FY2025","index_year":2026,"object_id":"202641339349303874","required":["IRS990","IRS990ScheduleL","IRS990ScheduleO"],"strict":True,
     "use":"Schedule L interested-person rows and filing context"},
]
UA="FedorMilovanov-Research-G3-IRS-Acquisition/3.0 (research-only)"

def sha(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def lname(tag:str)->str: return tag.rsplit('}',1)[-1]
def norm(s:str)->str: return ''.join(c for c in s.upper() if c.isalnum())
def writej(path:Path,obj:Any)->None: path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')
def req(url:str): return urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"*/*"})

def fetch(url:str,timeout=180):
    st=time.time()
    try:
        with urllib.request.urlopen(req(url),timeout=timeout) as r:
            b=r.read()
            return b,{"requested_url":url,"final_url":r.geturl(),"status":getattr(r,'status',None),
                      "content_type":r.headers.get('Content-Type'),"bytes":len(b),"sha256":sha(b),
                      "elapsed_seconds":round(time.time()-st,3)}
    except urllib.error.HTTPError as e: raise RuntimeError(f"HTTP {e.code} for {url}: {e.reason}") from e
    except urllib.error.URLError as e: raise RuntimeError(f"URL error for {url}: {e.reason}") from e

def fetch_file(url:str,path:Path,timeout=600):
    st=time.time(); h=hashlib.sha256(); n=0
    try:
        with urllib.request.urlopen(req(url),timeout=timeout) as r, path.open('wb') as f:
            while True:
                c=r.read(1024*1024)
                if not c: break
                f.write(c); h.update(c); n+=len(c)
            return {"requested_url":url,"final_url":r.geturl(),"status":getattr(r,'status',None),
                    "content_type":r.headers.get('Content-Type'),"bytes":n,"sha256":h.hexdigest(),
                    "elapsed_seconds":round(time.time()-st,3)}
    except Exception:
        path.unlink(missing_ok=True); raise

def index_row(csv_bytes:bytes,oid:str):
    rd=csv.DictReader(io.StringIO(csv_bytes.decode('utf-8-sig')))
    if not rd.fieldnames: raise RuntimeError('IRS index has no header')
    mp={norm(x):x for x in rd.fieldnames}; oc=mp.get('OBJECTID'); ec=mp.get('EIN')
    if not oc: raise RuntimeError(f'No OBJECT_ID column: {rd.fieldnames}')
    for row in rd:
        if (row.get(oc) or '').strip()==oid:
            clean={k:(v or '').strip() for k,v in row.items() if k}
            if ec and ''.join(c for c in clean.get(ec,'') if c.isdigit()) not in ('',EIN):
                raise RuntimeError('EIN mismatch')
            return clean
    raise RuntimeError(f'Object {oid} not found in IRS index')

def rowval(row,key):
    nk=norm(key)
    for k,v in row.items():
        if norm(k)==nk: return (v or '').strip()
    return ''

def batch_urls(year:int,bid:str):
    base=f'https://apps.irs.gov/pub/epostcard/990/xml/{year}/'
    names=[]
    for x in [bid,bid.upper(),bid.lower(),bid[:-1]+bid[-1:].upper() if bid else bid]:
        if x and x not in names: names.append(x)
    return [base+x+'.zip' for x in names]

def get_batch(year:int,bid:str,path:Path):
    attempts=[]
    for u in batch_urls(year,bid):
        try:
            m=fetch_file(u,path); attempts.append({"url":u,"success":True,**m}); return m,attempts
        except Exception as e:
            attempts.append({"url":u,"success":False,"error":str(e)})
    raise RuntimeError(f'Could not acquire batch {bid}: {attempts}')

def content_matches(data:bytes,row:dict[str,str])->bool:
    if EIN.encode() not in data: return False
    tp=rowval(row,'TAX_PERIOD')
    return not (tp and len(tp)>=4 and tp[:4].encode() not in data)

def external_read_member(zpath:Path,member:str):
    candidates=[]
    if shutil.which('bsdtar'):
        candidates.append(('bsdtar',['bsdtar','-xOf',str(zpath),member]))
    if shutil.which('7z'):
        candidates.append(('7z',['7z','x','-so',str(zpath),member]))
    if shutil.which('unzip'):
        candidates.append(('unzip',['unzip','-p',str(zpath),member]))
    errors=[]
    for name,cmd in candidates:
        p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if p.returncode==0 and p.stdout:
            return p.stdout,name
        errors.append({"tool":name,"returncode":p.returncode,
                       "stderr":p.stderr.decode('utf-8','replace')[:500]})
    raise RuntimeError(f'No external archive reader could extract {member}: {errors}')

def read_member(z:zipfile.ZipFile,zpath:Path,info:zipfile.ZipInfo):
    try:
        return z.read(info),'python-zipfile'
    except (NotImplementedError,RuntimeError) as e:
        msg=str(e).lower()
        if isinstance(e,NotImplementedError) or 'compression' in msg or 'supported' in msg:
            return external_read_member(zpath,info.filename)
        raise

def extract_member(zpath:Path,oid:str,row:dict[str,str]):
    identifiers=[oid,rowval(row,'DLN'),rowval(row,'RETURN_ID')]
    identifiers=[x for x in identifiers if x]
    with zipfile.ZipFile(zpath) as z:
        infos=[i for i in z.infolist() if not i.is_dir() and i.filename.lower().endswith('.xml')]
        names=[i.filename for i in infos]
        direct=[i for i in infos if any(x in Path(i.filename).name for x in identifiers)]
        method='filename_identifier'
        if not direct:
            method='content_signature'; direct=[]
            for i in infos:
                if i.file_size>5_000_000: continue
                try:
                    b,reader=read_member(z,zpath,i)
                except Exception:
                    continue
                if content_matches(b,row):
                    direct.append(i)
                    if len(direct)>1: break
        if not direct:
            raise RuntimeError(f'No matching XML member; identifiers={identifiers}; sample_members={names[:30]}')
        if len(direct)>1:
            exact=[i for i in direct if oid in Path(i.filename).name]
            if len(exact)==1: direct=exact
            else: raise RuntimeError(f'Ambiguous member match: {[i.filename for i in direct[:10]]}')
        i=direct[0]
        b,reader=read_member(z,zpath,i)
        return b,{"member":i.filename,"selection_method":method,"archive_reader":reader,
                  "member_compressed_bytes":i.compress_size,"member_uncompressed_bytes":i.file_size,
                  "member_crc32":f'{i.CRC:08x}',"member_sha256":sha(b),"identifiers":identifiers,
                  "xml_member_count":len(infos),"sample_members":names[:20]}

def flatten(elem):
    out=[]
    def walk(n,path):
        nm=lname(n.tag); p=path+[nm]; children=list(n); t=(n.text or '').strip()
        attrs={lname(k):v for k,v in n.attrib.items()}
        if not children:
            if t or attrs: out.append({"path":"/".join(p),"tag":nm,"text":t,"attributes":attrs})
            return
        if t: out.append({"path":"/".join(p),"tag":nm,"text":t,"attributes":attrs,"container_text":True})
        for c in children: walk(c,p)
    walk(elem,[]); return out

def acquire(t,out):
    d=out/t['label']; d.mkdir(parents=True,exist_ok=True)
    y=t['index_year']; oid=t['object_id']
    idxurl=f'https://apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv'
    idx,im=fetch(idxurl); row=index_row(idx,oid); bid=rowval(row,'XML_BATCH_ID')
    writej(d/'IRS_INDEX_FETCH.json',im); writej(d/'IRS_INDEX_ROW.json',row)
    if not bid: raise RuntimeError('Matched row has no XML_BATCH_ID')
    zp=d/(bid+'.zip'); attempts=[]
    try:
        bm,attempts=get_batch(y,bid,zp)
        writej(d/'BATCH_FETCH.json',bm); writej(d/'BATCH_FETCH_ATTEMPTS.json',attempts)
        xb,mm=extract_member(zp,oid,row); writej(d/'BATCH_MEMBER.json',mm)
    finally:
        zp.unlink(missing_ok=True)
        if attempts and not (d/'BATCH_FETCH_ATTEMPTS.json').exists():
            writej(d/'BATCH_FETCH_ATTEMPTS.json',attempts)
    xp=d/(oid+'_public.xml'); xp.write_bytes(xb)
    xm={"file":xp.name,"bytes":len(xb),"sha256":sha(xb),"source_batch_id":bid,"source_member":mm['member']}
    writej(d/'XML_FETCH.json',xm)
    try: root=ET.fromstring(xb)
    except ET.ParseError as e: raise RuntimeError(f'Invalid XML {oid}: {e}') from e
    cs={}
    for comp in t['required']:
        ms=[e for e in root.iter() if lname(e.tag)==comp]; cs[comp]={"count":len(ms)}
        for j,m in enumerate(ms,1):
            s='' if len(ms)==1 else f'_{j:02d}'
            frag=ET.tostring(m,encoding='utf-8',xml_declaration=True)
            fn=f'{comp}{s}.xml'; (d/fn).write_bytes(frag)
            leaves=flatten(m); writej(d/f'{comp}{s}_LEAVES.json',leaves)
            cs[comp].setdefault('objects',[]).append({"file":fn,"bytes":len(frag),
                                                     "sha256":sha(frag),"leaf_count":len(leaves)})
    writej(d/'COMPONENT_SUMMARY.json',cs)
    missing=[x for x in t['required'] if cs.get(x,{}).get('count',0)==0]
    if missing: raise RuntimeError(f'Required component(s) absent from return: {missing}')
    custody={"label":t['label'],"ein":EIN,"object_id":oid,"index_year":y,"research_use":t['use'],
             "index":im,"index_row":row,"batch":{**bm,"xml_batch_id":bid,"archive_retained":False},
             "batch_member":mm,"xml":xm,"components":cs,"state":"EPHEMERAL_ACTION_ARTIFACT",
             "publication_eligible":False,"raw_xml":True}
    writej(d/'CUSTODY.json',custody); return custody

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',default='g3-irs-acquisition-output')
    a=ap.parse_args(); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    s={"ein":EIN,"targets":[],"errors":[],"warnings":[],"state":"EPHEMERAL_ACTION_ARTIFACT","publication_eligible":False}
    hard_fail=False
    for t in TARGETS:
        try: s['targets'].append(acquire(t,out))
        except Exception as e:
            rec={"label":t['label'],"object_id":t['object_id'],"strict":t.get('strict',True),"error":str(e)}
            if t.get('strict',True):
                s['errors'].append(rec); hard_fail=True
            else:
                s['warnings'].append(rec)
    writej(out/'SUMMARY.json',s)
    for e in s['warnings']: print(f"WARNING {e['label']} {e['object_id']}: {e['error']}",file=sys.stderr)
    for e in s['errors']: print(f"ERROR {e['label']} {e['object_id']}: {e['error']}",file=sys.stderr)
    for x in s['targets']:
        print(f"ACQUIRED {x['label']} {x['object_id']} {x['xml']['bytes']} bytes sha256={x['xml']['sha256']} reader={x['batch_member']['archive_reader']}")
    return 2 if hard_fail else 0

if __name__=='__main__':
    raise SystemExit(main())
