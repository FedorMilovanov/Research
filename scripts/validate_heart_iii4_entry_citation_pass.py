#!/usr/bin/env python3
"""Validate the completed III.4 entry citation pass."""
from __future__ import annotations

import argparse, hashlib, importlib.util, json, re, subprocess, sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
BUILDER=ROOT/"scripts/build_heart_whole_book_citation_inventory.py"
R2=ROOT/"СЕРИЯ СЕРДЦЕ/64_R2_OT_REGENERATION_INDWELLING.md"
READER=ROOT/"СЕРИЯ СЕРДЦЕ/125_READER_CHAPTER_III4_HEART_AND_SPIRIT_2026-08-04.md"
ASSEMBLY=ROOT/"data/heart-iii4-reader-assembly-2026-08-04.json"
CURRENT=ROOT/"data/heart-entry-citation-pass-current-v8-2026-08-04.json"
RECEIPT=ROOT/"data/heart-iii4-citation-review-2026-08-04.json"
HUMAN=ROOT/"СЕРИЯ СЕРДЦЕ/127_III4_ENTRY_CITATION_PASS_2026-08-04.md"
WORKFLOW=ROOT/".github/workflows/heart-reader-assembly.yml"
PRODUCT_REL=Path("src/content/articles/serdce-i-duh.mdx")
BLOBS={R2:"0bc0cde5a85fe015ca8f394c3fda28074ce19577",READER:"bf34a453d7fc851bfda3a79eb0389418610c9681",ASSEMBLY:"b9dfda284cfa36d8ee6a7d970dc3bf2a9eeba7c9",CURRENT:"6736f90211e34c5dbb7d9943e617102b660bb5be",BUILDER:"6e8fb1af57bc72d26a9ca91d5b84b1fec3de7f12"}
PRODUCT_BLOB="1f8ede3dd03a2129bbf7d91d49689d25f0f72571"
SOURCE_SHAS={"PRODUCT":"d6b57fc6486e192f371daf430ab50dc7a6d9bdb99b5caa75ed5617d333b2ebe9","R2":"4aa919cf1c54d634852cf179bd006f27d197e0adbc41dbd1c286a0c0f39d9292"}
UNION_HASHES={"scriptureReferenceSetSha256":"7a587385428590ae7d679608a01507f23ea709cd5b3f0979773efc6fe6a62bb9","sourceSurfaceBaseManifestSha256":"823ede67a8913057b559db8185e5c35a942655964e0a2e73f71ae9595d062f9e","classifiedSurfaceManifestSha256":"2355e802be1f20e51d2550c3dc4ed3cbfdc3776b8ac32217df7252c68e0f9e64","roleSectionMapSha256":"a5fb8ff7f6358d6cf79cdcc08cc52197ea8fa0aeeb0796d332ff8c20ad3b46aa","sectionSummarySha256":"bd5192283b58bea3b8dd1532db2f3c83cbf258d5ce6be8456ed9f426b0d0f1db","externalLinkSetSha256":"c6585ad6c6612715ec1114ee8e85f72436b0c24a6238a97455fb7cb11cc6f431","internalLinkSetSha256":"c0bf668f80df6cdaf0430a572ee139872cbdc429f42749a540b37b4c6b6fbab5"}
ROLE_COUNTS={"ATTRIBUTED_WITNESS_OR_SOURCE_BANK_SURFACE":92,"EDITORIAL_STRUCTURAL_OR_CAUTION_SURFACE":27,"EXEGETICAL_SCRIPTURE_OR_DOCTRINAL_SURFACE":170}
URL_COUNTS={"DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD":6,"DOSSIER_SUPPORT_RECORD_NO_READER_TRANSFER":5,"DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE":19}
URL_REGISTRY_SHA="8a144607ecbe3bd671d78476060596f46762b02a690a2ca76fed86db97c67457"
INTERNAL_REGISTRY_SHA="aeeaf3a5481a2c94db93038732a08b7a11206158f3cfd3ce420df0ea263e8b10"
READER_SHA="6d4d26b32b605f1d2855f4f6ae51f145f98b6e4c39bfda19562fa81a46f7b56d"
EXPECTED_COUNTS={"finalBookEntries":18,"entryCitationPassComplete":12,"entryCitationPassOpen":6,"assembledReaders":12,"assembledReaderCitationReviewsComplete":12,"missingStandaloneFinalReaders":6,"productSourceOnlyEntries":2,"researchDossierOnlyEntries":4,"productSourceRepairsRequired":4,"dossierUrlHoldsRetained":46,"dossierSourceUrlRepairsRequired":2,"unresolvedInternalPathsRetained":1,"newDirectQuotesApproved":0}
errors=[]
def req(v:bool,m:str):
    if not v:errors.append(m)
def readj(p:Path)->dict[str,Any]:
    try:v=json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:errors.append(f"{p.relative_to(ROOT)}: {e}");return {}
    req(isinstance(v,dict),f"{p.relative_to(ROOT)} must be object");return v if isinstance(v,dict) else {}
def blob(root:Path,p:Path)->str:return subprocess.check_output(["git","hash-object",str(p)],cwd=root,text=True).strip()
def tsha(s:str)->str:return hashlib.sha256(s.encode()).hexdigest()
def jsha(v:Any,sort=False)->str:return tsha(json.dumps(v,ensure_ascii=False,separators=(",",":"),sort_keys=sort))
def norm(s:str)->str:s=re.sub(r"<[^>]+>"," ",s);return re.sub(r"\s+"," ",s).strip()
def qc(s:dict[str,Any])->int:return s["inlineQuotationSegments"]+s["markdownBlockquotes"]+s["htmlBlockquotes"]
def heads(text:str)->list[dict[str,Any]]:
    r=[]
    for m in re.finditer(r"(?m)^(#{1,4})\s+(.+?)\s*$",text):r.append({"offset":m.start(),"level":len(m.group(1)),"title":m.group(2).strip()})
    for m in re.finditer(r'<h([1-4])\s+[^>]*id="([^"]+)"[^>]*>(.*?)</h\1>',text,re.S|re.I):r.append({"offset":m.start(),"level":int(m.group(1)),"title":norm(m.group(3)),"id":m.group(2)})
    return sorted(r,key=lambda x:x["offset"])
def hfor(r:list[dict[str,Any]],off:int)->str:
    cur="frontmatter-or-introduction"
    for x in r:
        if x["offset"]>off:break
        cur=x["title"]
    return cur
def surfaces(text:str,owner:str,module:Any)->list[dict[str,Any]]:
    h=heads(text);out=[];pats=[("RUSSIAN",re.compile(r"«([^»\n]{8,})»")),("CURLY",re.compile(r"“([^”\n]{8,})”")),("MD_BLOCK",re.compile(r"(?m)^\s*>\s?(\S.*)$")),("HTML_BLOCK",re.compile(r"<blockquote[^>]*>(.*?)</blockquote>",re.S|re.I))]
    for typ,pat in pats:
        for m in pat.finditer(text):
            val=norm(m.group(1));sec=hfor(h,m.start());near=sorted({module.normalize_ref(x.group(0)) for x in module.SCRIPTURE_RE.finditer(text[max(0,m.start()-300):min(len(text),m.end()+300)])},key=str.casefold);out.append({"owner":owner,"position":m.start(),"section":sec,"type":typ,"sha256":tsha(val),"chars":len(val),"nearbyScripture":near})
    out.sort(key=lambda x:x["position"])
    for i,x in enumerate(out,1):x["ownerIndex"]=i;x.pop("position")
    return out
def contexts(text:str,url:str,hold:list[str],verified:list[str])->list[dict[str,Any]]:
    h=heads(text);out=[];cur=0
    while True:
        off=text.find(url,cur)
        if off<0:break
        c=norm(text[max(0,off-500):min(len(text),off+len(url)+500)]);out.append({"section":hfor(h,off),"contextSha256":tsha(c),"holdTerms":sorted({x for x in hold if x.casefold() in c.casefold()},key=str.casefold),"verifiedTerms":sorted({x for x in verified if x.casefold() in c.casefold()},key=str.casefold)});cur=off+1
    return out
def status(ctx:list[dict[str,Any]],fallback:str)->str:
    if any(x["holdTerms"] for x in ctx) or any("Открытые вопросы" in x["section"] for x in ctx):return "DOSSIER_OPEN_OR_DIRECT_QUOTE_HOLD"
    if any(x["verifiedTerms"] for x in ctx):return "DOSSIER_VERIFIED_OR_SAFE_CLOSURE_SOURCE"
    return fallback

ap=argparse.ArgumentParser();ap.add_argument("--product-root",type=Path,required=True);a=ap.parse_args();proot=a.product_root.resolve();ppath=proot/PRODUCT_REL
for p,e in BLOBS.items():req(p.is_file(),f"missing {p.relative_to(ROOT)}");req(not p.is_file() or blob(ROOT,p.relative_to(ROOT))==e,f"blob drift {p.relative_to(ROOT)}")
req(ppath.is_file(),"Product owner missing");req(not ppath.is_file() or blob(proot,PRODUCT_REL)==PRODUCT_BLOB,"Product owner blob drift")
receipt=readj(RECEIPT);assembly=readj(ASSEMBLY);current=readj(CURRENT)
texts={"PRODUCT":ppath.read_text(encoding="utf-8") if ppath.is_file() else "","R2":R2.read_text(encoding="utf-8") if R2.is_file() else ""};reader=READER.read_text(encoding="utf-8") if READER.is_file() else ""
for o in texts:req(tsha(texts[o])==SOURCE_SHAS[o],f"{o} source SHA drift")
req(tsha(reader)==READER_SHA,"reader SHA drift")
spec=importlib.util.spec_from_file_location("inv",BUILDER);assert spec and spec.loader;mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
scans={"PRODUCT":mod.scan_owner(mod.p(str(PRODUCT_REL),"III.4 Product owner"),proot),"R2":mod.scan_owner(mod.r(str(R2.relative_to(ROOT)),"III.4 R2 owner"),proot)}
all_s=surfaces(texts["PRODUCT"],"PRODUCT",mod)+surfaces(texts["R2"],"R2",mod);base=[{k:x[k] for k in ("owner","ownerIndex","section","type","sha256","chars","nearbyScripture")} for x in all_s]
rolemap=receipt.get("fullOwnerReview",{}).get("roleSectionMap",{});classified=[]
for x in base:
    role=""
    for candidate,sections in rolemap.get(x["owner"],{}).items():
        if x["section"] in sections:role=candidate;break
    req(bool(role),f"unmapped surface section {x['owner']}::{x['section']}");classified.append({**x,"class":role})
sec={}
for x in classified:
    k=f"{x['owner']}::{x['section']}";b=sec.setdefault(k,{"surfaces":0,"classes":Counter(),"types":Counter()});b["surfaces"]+=1;b["classes"][x["class"]]+=1;b["types"][x["type"]]+=1
sec={k:{"surfaces":v["surfaces"],"classes":dict(sorted(v["classes"].items())),"types":dict(sorted(v["types"].items()))} for k,v in sorted(sec.items())}
refs=sorted(set(scans["PRODUCT"]["scriptureReferences"])|set(scans["R2"]["scriptureReferences"]),key=str.casefold);urls=sorted(scans["R2"]["externalLinks"],key=str.casefold);ints=sorted(scans["PRODUCT"]["internalArticleLinks"],key=str.casefold)
req((len(refs),len(all_s),len(urls),len(ints))==(136,289,30,6),"union count drift");req(qc(scans["PRODUCT"])==115 and qc(scans["R2"])==174,"owner quotation drift")
actual_hashes={"scriptureReferenceSetSha256":jsha(refs),"sourceSurfaceBaseManifestSha256":jsha(base),"classifiedSurfaceManifestSha256":jsha(classified),"roleSectionMapSha256":jsha(rolemap,True),"sectionSummarySha256":jsha(sec,True),"externalLinkSetSha256":jsha(urls),"internalLinkSetSha256":jsha(ints)}
req(actual_hashes==UNION_HASHES,"III.4 manifest hash drift");req(dict(sorted(Counter(x["class"] for x in classified).items()))==ROLE_COUNTS,"role counts drift")
link=receipt.get("externalLinkReview",{});method=link.get("method",{});ureg=[]
for u in urls:
    ctx=contexts(texts["R2"],u,method.get("holdTerms",[]),method.get("verifiedTerms",[]));ureg.append({"owner":"R2","url":u,"status":status(ctx,method.get("fallback","")),"occurrences":len(ctx),"sections":sorted({x["section"] for x in ctx},key=str.casefold),"contexts":ctx,"readerTransfer":False,"directQuoteBulkApproval":False})
req(sum(x["occurrences"] for x in ureg)==34,"URL occurrence drift");req(dict(sorted(Counter(x["status"] for x in ureg).items()))==URL_COUNTS,"URL status counts drift");req(jsha(ureg,True)==URL_REGISTRY_SHA,"URL registry drift")
ireg=[]
for p in ints:
    slug=p.removeprefix("/articles/").removesuffix("/");target=Path("src/content/articles")/(slug+".mdx");ireg.append({"path":p,"target":str(target),"exists":(proot/target).is_file(),"targetBlob":blob(proot,target) if (proot/target).is_file() else None,"readerTransfer":False})
req(all(x["exists"] for x in ireg),"Product internal target missing");req(jsha(ireg,True)==INTERNAL_REGISTRY_SHA,"internal registry drift");req(ireg==receipt.get("internalLinkReview",{}).get("targets"),"internal target receipt drift")
rs=mod.scan_owner(mod.r(str(READER.relative_to(ROOT)),"III.4 reader"),proot);req((len(re.findall(r"(?u)\b[\wЁёА-Яа-я]+\b",reader)),len(rs["scriptureReferences"]),qc(rs),len(rs["externalLinks"]),len(rs["internalArticleLinks"]),rs["footnoteDefinitions"],len(rs["sourceHeadings"]))==(1681,15,0,0,0,0,0),"reader review drift")
req(receipt.get("authorityId")=="HEART-III4-CITATION-REVIEW-2026-08-04" and receipt.get("status")=="III4_ENTRY_CITATION_PASS_COMPLETE_ALL_TWELVE_READERS_REVIEWED_ZERO_NEW_DIRECT_QUOTES","receipt identity drift");req(receipt.get("effectiveCounts")==EXPECTED_COUNTS,"effective counts drift");req(receipt.get("fullOwnerReview",{}).get("quotationRoleCounts")==ROLE_COUNTS,"receipt role counts drift");req(receipt.get("externalLinkReview",{}).get("statusCounts")==URL_COUNTS,"receipt URL counts drift");req(receipt.get("externalLinkReview",{}).get("sourceUrlRepairsAdded")==0,"unexpected III.4 URL repairs");req(receipt.get("internalLinkReview",{}).get("newUnresolvedInternalPaths")==0,"unexpected III.4 unresolved paths")
req(assembly.get("authorityId")=="HEART-III4-READER-ASSEMBLY-2026-08-04" and assembly.get("publicationBoundary",{}).get("iii4EntryCitationPassComplete") is False,"assembly boundary drift");req(current.get("authorityId")=="HEART-ENTRY-CITATION-PASS-CURRENT-V8-2026-08-04","V8 authority drift")
pub=receipt.get("publicationBoundary",{});req(pub.get("iii4EntryCitationPassComplete") is True and pub.get("allCurrentlyAssembledReadersReviewed") is True,"publication state drift")
for k in ("wholeBookReaderAssemblyComplete","wholeBookCitationPassComplete","wholeBookTransitionDedupPassComplete","wholeBookLineEditComplete","manuscriptBundleComplete","productReleaseComplete","productSourceRepairsComplete","dossierUrlHoldsResolved","dossierSourceUrlRepairsComplete","unresolvedInternalPathsResolved"):req(pub.get(k) is False,f"falsely closes {k}")
human=HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
for m in ("HEART-III4-CITATION-REVIEW-2026-08-04","SCRIPTURE REFERENCES GOVERNED = 136 / 136","QUOTATION SURFACES CLASSIFIED = 289 / 289","EXEGETICAL / DOCTRINAL SURFACES = 170","ATTRIBUTED WITNESS SURFACES = 92","EDITORIAL / CAUTION SURFACES = 27","EXTERNAL LINKS DISPOSITIONED = 30 / 30","VERIFIED OR SAFE CLOSURE LINKS = 19","SUPPORT-ONLY LINKS = 5","OPEN OR DIRECT-QUOTE HOLDS = 6","PRODUCT INTERNAL TARGETS VERIFIED = 6 / 6","READER QUOTATION SURFACES = 0","READER LINKS = 0","ENTRY CITATION PASSES COMPLETE = 12 / 18","ASSEMBLED READER CITATION REVIEWS = 12 / 12","DOSSIER URL HOLDS RETAINED = 46","NEXT TRANSACTION = CURRENT V9 COMPOSITION",PRODUCT_BLOB,BLOBS[R2],BLOBS[READER],BLOBS[ASSEMBLY],BLOBS[CURRENT]):req(m in human,f"human marker missing {m}")
for x in ("ENTRY CITATION PASSES COMPLETE = 18 / 18","DOSSIER URL HOLDS RETAINED = 0","WHOLE-BOOK READER ASSEMBLY = COMPLETE","WHOLE-BOOK CITATION PASS = COMPLETE","PRODUCT RELEASE = COMPLETE","TODO","TBD"):req(x not in human,f"forbidden human marker {x}")
wf=WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.is_file() else "";req("validate_heart_iii4_entry_citation_pass.py" in wf,"workflow gate missing");req("diagnose_heart_iii4_citation.py" not in wf,"diagnostic leaked into workflow");req(not (ROOT/"scripts/diagnose_heart_iii4_citation.py").exists(),"temporary script remains");req(not (ROOT/".github/workflows/diagnose-heart-iii4-citation.yml").exists(),"temporary workflow remains")
if errors:
 print(f"Heart III.4 citation pass: FAIL ({len(errors)})",file=sys.stderr)
 for e in errors:print(f"- {e}",file=sys.stderr)
 raise SystemExit(1)
print("Heart III.4 citation pass: PASS — 136/289/30/6 governed, roles 170/92/27, links 19/5/6, targets 6/6, reviews 12/12")
