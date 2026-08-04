#!/usr/bin/env python3
"""Temporary read-only III.4 citation/link decomposition."""
from __future__ import annotations

import argparse, hashlib, importlib.util, json, re, subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
R2 = ROOT / "СЕРИЯ СЕРДЦЕ/64_R2_OT_REGENERATION_INDWELLING.md"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/125_READER_CHAPTER_III4_HEART_AND_SPIRIT_2026-08-04.md"
ASSEMBLY = ROOT / "data/heart-iii4-reader-assembly-2026-08-04.json"
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v8-2026-08-04.json"
PRODUCT_REL = Path("src/content/articles/serdce-i-duh.mdx")
OUTPUT = ROOT / "iii4-citation-diagnostic.json"
EXPECTED = {
    R2:"0bc0cde5a85fe015ca8f394c3fda28074ce19577",
    READER:"bf34a453d7fc851bfda3a79eb0389418610c9681",
    ASSEMBLY:"b9dfda284cfa36d8ee6a7d970dc3bf2a9eeba7c9",
    CURRENT:"6736f90211e34c5dbb7d9943e617102b660bb5be",
    BUILDER:"6e8fb1af57bc72d26a9ca91d5b84b1fec3de7f12",
}
PRODUCT_BLOB="1f8ede3dd03a2129bbf7d91d49689d25f0f72571"
HOLD_TERMS=["НЕ ВЕРИФИЦИРОВАНО","не верифицирован","кандидат","Открытые вопросы","не использовать","неточно","не найден","не подтверд","сомнитель","проверить","HOLD","NO-DIRECT-QUOTE","BOOK-PAGE-HOLD","DO-NOT-DIRECT-QUOTE","перед публикацией","контрольное сличение","локатор"]
VERIFIED_TERMS=["ВЕРИФИЦИРОВАНО","SAFE CLOSURE","подтверждено","точная фраза","дословно","проверен","проверено","VERIFIED"]
EDITORIAL_TERMS=["Задача","место в книге","Вывод","структур","Чего избегать","Открытые вопросы","Статус","Итог","Коротко","Нашли неточность","Читайте также"]
ATTRIBUTED_TERMS=["Цитат","Источник","Источники","сверка","Первоисточник","Лексика","Hamilton","Хэмилтон","Owen","Оуэн","Warfield","Уорфилд","Ferguson","Фергюсон","Packer","Пакер","Murray","Мюррей","Cranfield","Крэнфилд","Lloyd-Jones","Ллойд"]

def blob(root:Path,p:Path)->str:return subprocess.check_output(["git","hash-object",str(p)],cwd=root,text=True).strip()
def sha(v:Any,sort=False)->str:
    s=v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,separators=(",",":"),sort_keys=sort)
    return hashlib.sha256(s.encode()).hexdigest()
def norm(s:str)->str:
    s=re.sub(r"<[^>]+>"," ",s); return re.sub(r"\s+"," ",s).strip()
def qcount(s:dict[str,Any])->int:return s["inlineQuotationSegments"]+s["markdownBlockquotes"]+s["htmlBlockquotes"]
def headings(text:str)->list[dict[str,Any]]:
    rows=[]
    for m in re.finditer(r"(?m)^(#{1,4})\s+(.+?)\s*$",text):rows.append({"offset":m.start(),"level":len(m.group(1)),"title":m.group(2).strip()})
    for m in re.finditer(r'<h([1-4])\s+[^>]*id="([^"]+)"[^>]*>(.*?)</h\1>',text,re.S|re.I):rows.append({"offset":m.start(),"level":int(m.group(1)),"title":norm(m.group(3)),"id":m.group(2)})
    return sorted(rows,key=lambda x:x["offset"])
def hfor(rows:list[dict[str,Any]],off:int)->str:
    cur="frontmatter-or-introduction"
    for r in rows:
        if r["offset"]>off:break
        cur=str(r["title"])
    return cur
def role(section:str)->str:
    if any(x.casefold() in section.casefold() for x in ATTRIBUTED_TERMS):return "ATTRIBUTED_WITNESS_OR_SOURCE_BANK_SURFACE"
    if any(x.casefold() in section.casefold() for x in EDITORIAL_TERMS):return "EDITORIAL_STRUCTURAL_OR_CAUTION_SURFACE"
    return "EXEGETICAL_SCRIPTURE_OR_DOCTRINAL_SURFACE"
def surfaces(text:str,owner:str,module:Any)->list[dict[str,Any]]:
    heads=headings(text); out=[]
    pats=[("RUSSIAN",re.compile(r"«([^»\n]{8,})»")),("CURLY",re.compile(r"“([^”\n]{8,})”")),("MD_BLOCK",re.compile(r"(?m)^\s*>\s?(\S.*)$")),("HTML_BLOCK",re.compile(r"<blockquote[^>]*>(.*?)</blockquote>",re.S|re.I))]
    for typ,pat in pats:
        for m in pat.finditer(text):
            val=norm(m.group(1)); sec=hfor(heads,m.start()); left=max(0,m.start()-300); right=min(len(text),m.end()+300)
            refs=sorted({module.normalize_ref(x.group(0)) for x in module.SCRIPTURE_RE.finditer(text[left:right])},key=str.casefold)
            out.append({"owner":owner,"position":m.start(),"section":sec,"type":typ,"sha256":sha(val),"chars":len(val),"nearbyScripture":refs,"class":role(sec)})
    out.sort(key=lambda x:x["position"])
    for i,r in enumerate(out,1):r["ownerIndex"]=i;r.pop("position")
    return out
def contexts(text:str,url:str)->list[dict[str,Any]]:
    heads=headings(text); out=[]; cur=0
    while True:
        off=text.find(url,cur)
        if off<0:break
        c=norm(text[max(0,off-500):min(len(text),off+len(url)+500)])
        out.append({"section":hfor(heads,off),"contextSha256":sha(c),"holdTerms":sorted({x for x in HOLD_TERMS if x.casefold() in c.casefold()},key=str.casefold),"verifiedTerms":sorted({x for x in VERIFIED_TERMS if x.casefold() in c.casefold()},key=str.casefold)})
        cur=off+1
    return out
def url_status(url:str,ctx:list[dict[str,Any]])->str:
    if url.endswith(("`","*","**",",",";")):return "DOSSIER_SOURCE_URL_REPAIR_REQUIRED"
    if any(x["holdTerms"] for x in ctx) or any("Открытые вопросы" in x["section"] for x in ctx):return "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD"
    if any(x["verifiedTerms"] for x in ctx):return "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE"
    return "DOSSIER_SUPPORT_RECORD_NO_READER_TRANSFER"

ap=argparse.ArgumentParser();ap.add_argument("--product-root",type=Path,required=True);a=ap.parse_args();proot=a.product_root.resolve();ppath=proot/PRODUCT_REL
for p,e in EXPECTED.items():assert p.is_file() and blob(ROOT,p.relative_to(ROOT))==e,(p,blob(ROOT,p.relative_to(ROOT)) if p.is_file() else None,e)
assert ppath.is_file() and blob(proot,PRODUCT_REL)==PRODUCT_BLOB
spec=importlib.util.spec_from_file_location("inv",BUILDER);assert spec and spec.loader;mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
texts={"PRODUCT":ppath.read_text(encoding="utf-8"),"R2":R2.read_text(encoding="utf-8")}; scans={"PRODUCT":mod.scan_owner(mod.p(str(PRODUCT_REL),"III.4 Product owner"),proot),"R2":mod.scan_owner(mod.r(str(R2.relative_to(ROOT)),"III.4 R2 owner"),proot)}
reader_text=READER.read_text(encoding="utf-8");reader_scan=mod.scan_owner(mod.r(str(READER.relative_to(ROOT)),"III.4 reader"),proot)
surf=surfaces(texts["PRODUCT"],"PRODUCT",mod)+surfaces(texts["R2"],"R2",mod)
assert len(surf)==289 and qcount(scans["PRODUCT"])+qcount(scans["R2"])==289
base=[{k:r[k] for k in ("owner","ownerIndex","section","type","sha256","chars","nearbyScripture")} for r in surf]
classified=[{**r,"class":r["class"]} for r in base for _ in [next(x["class"] for x in surf if all(x.get(k)==r.get(k) for k in ("owner","ownerIndex")) )]]
role_counts=dict(sorted(Counter(r["class"] for r in classified).items()))
role_sections={}
for r in classified:role_sections.setdefault(r["owner"],{}).setdefault(r["class"],set()).add(r["section"])
role_sections={o:{c:sorted(v,key=str.casefold) for c,v in sorted(m.items())} for o,m in sorted(role_sections.items())}
section_summary={}
for r in classified:
    k=f"{r['owner']}::{r['section']}";b=section_summary.setdefault(k,{"surfaces":0,"classes":Counter(),"types":Counter()});b["surfaces"]+=1;b["classes"][r["class"]]+=1;b["types"][r["type"]]+=1
section_summary={k:{"surfaces":v["surfaces"],"classes":dict(sorted(v["classes"].items())),"types":dict(sorted(v["types"].items()))} for k,v in sorted(section_summary.items())}
urls=sorted(scans["R2"]["externalLinks"],key=str.casefold);ureg=[]
for url in urls:
    ctx=contexts(texts["R2"],url);ureg.append({"owner":"R2","url":url,"status":url_status(url,ctx),"occurrences":len(ctx),"sections":sorted({x["section"] for x in ctx},key=str.casefold),"contexts":ctx,"readerTransfer":False,"directQuoteBulkApproval":False})
internal=[]
for path in sorted(scans["PRODUCT"]["internalArticleLinks"],key=str.casefold):
    slug=path.removeprefix("/articles/").removesuffix("/");target=Path("src/content/articles")/(slug+".mdx");internal.append({"path":path,"target":str(target),"exists":(proot/target).is_file(),"targetBlob":blob(proot,target) if (proot/target).is_file() else None,"readerTransfer":False})
refs=sorted(set(scans["PRODUCT"]["scriptureReferences"])|set(scans["R2"]["scriptureReferences"]),key=str.casefold)
payload={"authorityId":"HEART-III4-CITATION-DIAGNOSTIC-2026-08-04","researchHead":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),"productCommit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=proot,text=True).strip(),"ownerCounts":{o:{"scriptureReferences":len(scans[o]["scriptureReferences"]),"quotationSurfaces":qcount(scans[o]),"externalLinks":len(scans[o]["externalLinks"]),"internalArticleLinks":len(scans[o]["internalArticleLinks"])} for o in scans},"union":{"scriptureReferences":len(refs),"quotationSurfaces":len(surf),"externalLinks":len(urls),"internalArticleLinks":len(internal),"scriptureReferenceSetSha256":sha(refs),"baseSurfaceManifestSha256":sha(base),"classifiedSurfaceManifestSha256":sha(classified),"roleSectionMapSha256":sha(role_sections,True),"sectionSummarySha256":sha(section_summary,True),"externalLinkSetSha256":sha(urls),"internalLinkSetSha256":sha([x["path"] for x in internal])},"roleCounts":role_counts,"roleSectionMap":role_sections,"sectionSummary":section_summary,"surfaceManifest":base,"classifiedSurfaceManifest":classified,"urlStatusCounts":dict(sorted(Counter(x["status"] for x in ureg).items())),"urlRegistry":ureg,"internalRegistry":internal,"reader":{"words":len(re.findall(r"(?u)\b[\wЁёА-Яа-я]+\b",reader_text)),"scriptureReferences":len(reader_scan["scriptureReferences"]),"quotationSurfaces":qcount(reader_scan),"externalLinks":len(reader_scan["externalLinks"]),"internalArticleLinks":len(reader_scan["internalArticleLinks"]),"footnoteDefinitions":reader_scan["footnoteDefinitions"],"sourceHeadings":reader_scan["sourceHeadings"],"gitBlob":blob(ROOT,READER.relative_to(ROOT)),"fullSha256":sha(reader_text)}}
assert payload["union"]["scriptureReferences"]==136 and payload["union"]["quotationSurfaces"]==289 and payload["union"]["externalLinks"]==30 and payload["union"]["internalArticleLinks"]==6
assert payload["reader"]["words"]==1681 and payload["reader"]["scriptureReferences"]==15 and payload["reader"]["quotationSurfaces"]==0 and payload["reader"]["externalLinks"]==0 and payload["reader"]["internalArticleLinks"]==0 and payload["reader"]["footnoteDefinitions"]==0 and payload["reader"]["sourceHeadings"]==[]
OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"union":payload["union"],"roleCounts":role_counts,"urlStatusCounts":payload["urlStatusCounts"],"internalRegistry":internal,"reader":payload["reader"],"outputSha256":sha(OUTPUT.read_text(encoding="utf-8"))},ensure_ascii=False,indent=2))
