#!/usr/bin/env python3
"""Validate the bounded III.4 Heart-and-Spirit reader assembly."""
from __future__ import annotations

import argparse, hashlib, importlib.util, json, re, subprocess, sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_heart_whole_book_citation_inventory.py"
R2 = ROOT / "СЕРИЯ СЕРДЦЕ/64_R2_OT_REGENERATION_INDWELLING.md"
READER = ROOT / "СЕРИЯ СЕРДЦЕ/125_READER_CHAPTER_III4_HEART_AND_SPIRIT_2026-08-04.md"
RECEIPT = ROOT / "data/heart-iii4-reader-assembly-2026-08-04.json"
CURRENT = ROOT / "data/heart-entry-citation-pass-current-v8-2026-08-04.json"
INTEGRATION = ROOT / "data/heart-whole-book-integration-2026-08-04.json"
TRIAGE = ROOT / "data/heart-entry-citation-dispositions-2026-08-04.json"
HUMAN = ROOT / "СЕРИЯ СЕРДЦЕ/126_III4_READER_ASSEMBLY_2026-08-04.md"
WORKFLOW = ROOT / ".github/workflows/heart-reader-assembly.yml"
PRODUCT_REL = Path("src/content/articles/serdce-i-duh.mdx")

BLOBS = {
    R2:"0bc0cde5a85fe015ca8f394c3fda28074ce19577",
    READER:"bf34a453d7fc851bfda3a79eb0389418610c9681",
    CURRENT:"6736f90211e34c5dbb7d9943e617102b660bb5be",
    INTEGRATION:"06d67275c42c7a9c3bd0365044f358b4b7d7a895",
    TRIAGE:"de4d49cada15b231dfc31058aced4ec7a25928a2",
    BUILDER:"6e8fb1af57bc72d26a9ca91d5b84b1fec3de7f12",
}
PRODUCT_BLOB = "1f8ede3dd03a2129bbf7d91d49689d25f0f72571"
OWNERS = {
    "PRODUCT": {
        "sha":"d6b57fc6486e192f371daf430ab50dc7a6d9bdb99b5caa75ed5617d333b2ebe9",
        "counts":(45,115,0,6,0,0),
        "hashes":("796b498e007c52399967ea3f358ada3848099df796fa7927e3e92c707db4f7b5","4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945","c0bf668f80df6cdaf0430a572ee139872cbdc429f42749a540b37b4c6b6fbab5","c07f44b3c737e5c16b6f71d4fd65b6688fdcbae83ad82c67bef391bdd5179091","737415ac94d7de6afda48fdb0db287a92d77192e25cb5a22dc2f5d3942e64a80"),
    },
    "R2": {
        "sha":"4aa919cf1c54d634852cf179bd006f27d197e0adbc41dbd1c286a0c0f39d9292",
        "counts":(93,174,30,0,0,0),
        "hashes":("62db12011cc5ecfd8f2f0c55a11176d00ca517c7c4ed2981543ebdb1344e2217","c6585ad6c6612715ec1114ee8e85f72436b0c24a6238a97455fb7cb11cc6f431","4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945","0f0a7f42d79bb7e6f5eca00cd99207d1539238456c3b1b7fa373ddc6e89537f7","13ab5f989c4e046906ee6b3811aeef862b1b246891fe24ac0e5c1100c4f6ebba"),
    },
}
UNION_HASHES = ("7a587385428590ae7d679608a01507f23ea709cd5b3f0979773efc6fe6a62bb9","c6585ad6c6612715ec1114ee8e85f72436b0c24a6238a97455fb7cb11cc6f431","c0bf668f80df6cdaf0430a572ee139872cbdc429f42749a540b37b4c6b6fbab5")
READER_SHA = "6d4d26b32b605f1d2855f4f6ae51f145f98b6e4c39bfda19562fa81a46f7b56d"
READER_REF_HASH = "e11949db71628dd3feab5b3d8301909999d0d0f4c66d304f0f83df36702a6644"
READER_HEADINGS = ["III.4. Сердце и Дух","Жизнь начинается без осуждения","Новый строй сердца","Бог живёт в верующем","Умерщвление Духом","Дух усыновления","Уже дети, ещё ожидающие","Помощь в немощи и двойное ходатайство","Цепь, которую держит Бог","Был ли Дух с ветхозаветными верующими","Ничто не отлучит"]
COUNTS = {"finalBookEntries":18,"assembledReaders":12,"missingStandaloneFinalReaders":6,"entryCitationPassComplete":11,"entryCitationPassOpen":7,"assembledReaderCitationReviewsComplete":11,"assembledReadersAwaitingCitationReview":1,"productSourceOnlyEntries":2,"researchDossierOnlyEntries":4,"productSourceRepairsRequired":4,"dossierUrlHoldsRetained":40,"dossierSourceUrlRepairsRequired":2,"unresolvedInternalPathsRetained":1,"newDirectQuotesApproved":0}
errors: list[str] = []

def req(ok: bool, msg: str) -> None:
    if not ok: errors.append(msg)
def readj(p: Path) -> dict[str,Any]:
    try: v=json.loads(p.read_text(encoding="utf-8"))
    except Exception as e: errors.append(f"{p.relative_to(ROOT)}: {e}"); return {}
    req(isinstance(v,dict),f"{p.relative_to(ROOT)} must be object"); return v if isinstance(v,dict) else {}
def blob(root: Path,p:Path)->str: return subprocess.check_output(["git","hash-object",str(p)],cwd=root,text=True).strip()
def tsha(s:str)->str: return hashlib.sha256(s.encode()).hexdigest()
def jsha(v:Any,sort=False)->str: return tsha(json.dumps(v,ensure_ascii=False,separators=(",",":"),sort_keys=sort))
def norm(s:str)->str:
    s=re.sub(r"<[^>]+>"," ",s); s=re.sub(r"[`*_#|>\[\](){}]"," ",s); return re.sub(r"\s+"," ",s).strip()
def qc(s:dict[str,Any])->int: return s["inlineQuotationSegments"]+s["markdownBlockquotes"]+s["htmlBlockquotes"]
def hs(text:str)->list[dict[str,Any]]:
    rows=[]
    for m in re.finditer(r"(?m)^(#{1,4})\s+(.+?)\s*$",text): rows.append({"offset":m.start(),"level":len(m.group(1)),"title":m.group(2).strip()})
    for m in re.finditer(r'<h([1-4])\s+[^>]*id="([^"]+)"[^>]*>(.*?)</h\1>',text,re.S|re.I): rows.append({"offset":m.start(),"level":int(m.group(1)),"title":norm(m.group(3)),"id":m.group(2)})
    return sorted(rows,key=lambda r:r["offset"])
def hfor(rows:list[dict[str,Any]],off:int)->str:
    cur="frontmatter-or-introduction"
    for r in rows:
        if r["offset"]>off: break
        cur=str(r["title"])
    return cur
def summary(text:str,module:Any)->dict[str,Any]:
    heads=hs(text); buckets={}
    pats=[("RUSSIAN",re.compile(r"«([^»\n]{8,})»")),("CURLY",re.compile(r"“([^”\n]{8,})”")),("STRAIGHT",re.compile(r'"([^"\n]{8,})"')),("MD_BLOCK",re.compile(r"(?m)^\s*>\s?(\S.*)$")),("HTML_BLOCK",re.compile(r"<blockquote[^>]*>(.*?)</blockquote>",re.S|re.I))]
    for typ,pat in pats:
        for m in pat.finditer(text):
            sec=hfor(heads,m.start()); b=buckets.setdefault(sec,{"quotationSurfaces":0,"types":Counter(),"scriptureNearby":set()}); b["quotationSurfaces"]+=1; b["types"][typ]+=1
            for x in module.SCRIPTURE_RE.finditer(text[max(0,m.start()-300):min(len(text),m.end()+300)]): b["scriptureNearby"].add(module.normalize_ref(x.group(0)))
    return {k:{"quotationSurfaces":v["quotationSurfaces"],"types":dict(sorted(v["types"].items())),"scriptureNearby":sorted(v["scriptureNearby"],key=str.casefold)} for k,v in sorted(buckets.items())}
def transfers(srcs:dict[str,str],reader:str)->list[str]:
    r=norm(reader); out=[]
    for owner,text in srcs.items():
        for s in re.split(r"(?<=[.!?])\s+",norm(text)):
            s=s.strip()
            if len(s)>=110 and s in r: out.append(owner+":"+tsha(s))
    return out

ap=argparse.ArgumentParser(); ap.add_argument("--product-root",type=Path,required=True); a=ap.parse_args(); proot=a.product_root.resolve(); ppath=proot/PRODUCT_REL
for p,e in BLOBS.items(): req(p.is_file(),f"missing {p.relative_to(ROOT)}"); req(not p.is_file() or blob(ROOT,p.relative_to(ROOT))==e,f"blob drift {p.relative_to(ROOT)}")
req(ppath.is_file(),"Product owner missing"); req(not ppath.is_file() or blob(proot,PRODUCT_REL)==PRODUCT_BLOB,"Product blob drift")
receipt,current,integration=readj(RECEIPT),readj(CURRENT),readj(INTEGRATION)
texts={"PRODUCT":ppath.read_text(encoding="utf-8") if ppath.is_file() else "","R2":R2.read_text(encoding="utf-8") if R2.is_file() else ""}; reader=READER.read_text(encoding="utf-8") if READER.is_file() else ""
req(tsha(texts["PRODUCT"])==OWNERS["PRODUCT"]["sha"],"Product SHA drift"); req(tsha(texts["R2"])==OWNERS["R2"]["sha"],"R2 SHA drift"); req(tsha(reader)==READER_SHA,"reader SHA drift")
spec=importlib.util.spec_from_file_location("inv",BUILDER); assert spec and spec.loader; mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
scans={"PRODUCT":mod.scan_owner(mod.p(str(PRODUCT_REL),"III.4 Product owner"),proot),"R2":mod.scan_owner(mod.r(str(R2.relative_to(ROOT)),"III.4 R2 owner"),proot)}
sets={}
for owner in ("PRODUCT","R2"):
    s=scans[owner]; refs=sorted(s["scriptureReferences"],key=str.casefold); urls=sorted(s["externalLinks"],key=str.casefold); ints=sorted(s["internalArticleLinks"],key=str.casefold); heads=[{k:r[k] for k in r if k!="offset"} for r in hs(texts[owner])]
    actual=(len(refs),qc(s),len(urls),len(ints),s["footnoteDefinitions"],len(s["sourceHeadings"])); req(actual==OWNERS[owner]["counts"],f"{owner} counts drift")
    actualh=(jsha(refs),jsha(urls),jsha(ints),jsha(heads),jsha(summary(texts[owner],mod),True)); req(actualh==OWNERS[owner]["hashes"],f"{owner} manifests drift"); sets[owner]=(refs,urls,ints)
urefs=sorted(set(sets["PRODUCT"][0])|set(sets["R2"][0]),key=str.casefold); uurls=sorted(set(sets["PRODUCT"][1])|set(sets["R2"][1]),key=str.casefold); uints=sorted(set(sets["PRODUCT"][2])|set(sets["R2"][2]),key=str.casefold)
req((len(urefs),qc(scans["PRODUCT"])+qc(scans["R2"]),len(uurls),len(uints))==(136,289,30,6),"union counts drift"); req((jsha(urefs),jsha(uurls),jsha(uints))==UNION_HASHES,"union hashes drift")
rs=mod.scan_owner(mod.r(str(READER.relative_to(ROOT)),"III.4 reader"),proot); rrefs=sorted(rs["scriptureReferences"],key=str.casefold)
req((len(re.findall(r"(?u)\b[\wЁёА-Яа-я]+\b",reader)),len(rrefs),qc(rs),len(rs["externalLinks"]),len(rs["internalArticleLinks"]),rs["footnoteDefinitions"],len(rs["sourceHeadings"]))==(1681,15,0,0,0,0,0),"reader counts drift"); req(jsha(rrefs)==READER_REF_HASH,"reader refs drift"); req([r["title"] for r in hs(reader)]==READER_HEADINGS,"reader headings drift"); req(transfers(texts,reader)==[],"long exact transfer")
for x in ("Hamilton","Хэмилтон","Owen","Оуэн","Warfield","Уорфилд","Ferguson","Фергюсон","BOOK-PAGE-HOLD","DO-NOT-DIRECT-QUOTE"): req(x not in reader,f"reader source-bank marker {x}")
for x in ("Рим. 8:1–4","Рим. 8:5–8","Рим. 8:9–11","Рим. 8:12–13","Рим. 8:14–17","Рим. 8:18–25","Рим. 8:26–27","Рим. 8:28–30","Рим. 8:34","Гал. 5:22–23","Числ. 11:29","Иез. 36:26–27","Ин. 7:39","Ин. 14:16–17","Евр. 11"): req(x in reader,f"missing anchor {x}")
entry=next((x for x in integration.get("entries",[]) if x.get("id")=="HEART-BOOK-III4"),{})
req(entry.get("order")==9 and entry.get("productOwner")=={"id":"serdce-duh","slug":"serdce-i-duh"} and entry.get("researchOwners")==[str(R2.relative_to(ROOT))],"integration III.4 drift")
req(current.get("authorityId")=="HEART-ENTRY-CITATION-PASS-CURRENT-V8-2026-08-04" and current.get("nextTransaction",{}).get("preferredEntryId")=="HEART-BOOK-III4","V8 boundary drift")
req(receipt.get("authorityId")=="HEART-III4-READER-ASSEMBLY-2026-08-04" and receipt.get("status")=="III4_STANDALONE_READER_ASSEMBLED_CITATION_PASS_OPEN","receipt identity drift"); req(receipt.get("effectiveCounts")==COUNTS,"receipt counts drift")
rr=receipt.get("reader",{}); req(rr.get("gitBlob")==BLOBS[READER] and rr.get("fullSha256")==READER_SHA and rr.get("words")==1681 and rr.get("scriptureReferences")==15 and rr.get("quotationSurfaces")==0 and rr.get("externalLinks")==0 and rr.get("internalArticleLinks")==0,"receipt reader drift")
u=receipt.get("historicalUnion",{}); req(tuple(u.get(k) for k in ("scriptureReferences","quotationSurfaces","uniqueExternalLinks","internalArticleLinks"))==(136,289,30,6),"receipt union drift")
req(receipt.get("nextTransaction",{}).get("preferredEntryId")=="HEART-BOOK-III4","receipt next drift")
pub=receipt.get("publicationBoundary",{}); req(pub.get("iii4ReaderAssemblyComplete") is True and pub.get("iii4EntryCitationPassComplete") is False and pub.get("allCurrentlyAssembledReadersReviewed") is False,"receipt publication boundary drift")
human=HUMAN.read_text(encoding="utf-8") if HUMAN.is_file() else ""
markers=("HEART-III4-READER-ASSEMBLY-2026-08-04","PRODUCT SCRIPTURE REFERENCES = 45","PRODUCT QUOTATION SURFACES = 115","PRODUCT INTERNAL LINKS = 6","R2 SCRIPTURE REFERENCES = 93","R2 QUOTATION SURFACES = 174","R2 EXTERNAL LINKS = 30","HISTORICAL UNION SCRIPTURE REFERENCES = 136","HISTORICAL UNION QUOTATION SURFACES = 289","HISTORICAL UNION EXTERNAL LINKS = 30","HISTORICAL UNION INTERNAL LINKS = 6","READER WORDS = 1681","READER SCRIPTURE REFERENCES = 15","READER QUOTATION SURFACES = 0","READER LINKS = 0","ASSEMBLED READERS = 12 / 18","ENTRY CITATION PASSES COMPLETE = 11 / 18","ASSEMBLED READER CITATION REVIEWS = 11 / 12","NEXT TRANSACTION = HEART-BOOK-III4 ENTRY CITATION PASS",PRODUCT_BLOB,BLOBS[R2],BLOBS[READER],BLOBS[CURRENT])
for m in markers: req(m in human,f"human marker missing {m}")
for x in ("ENTRY CITATION PASSES COMPLETE = 12 / 18","ASSEMBLED READER CITATION REVIEWS = 12 / 12","WHOLE-BOOK READER ASSEMBLY = COMPLETE","WHOLE-BOOK CITATION PASS = COMPLETE","PRODUCT RELEASE = COMPLETE","TODO","TBD"): req(x not in human,f"forbidden human marker {x}")
workflow=WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.is_file() else ""; req("validate_heart_iii4_reader_assembly.py" in workflow,"workflow gate missing"); req("diagnose_heart_iii4_reader_assembly.py" not in workflow,"diagnostic leaked")
req(not (ROOT/"scripts/diagnose_heart_iii4_reader_assembly.py").exists(),"temporary diagnostic remains"); req(not (ROOT/".github/workflows/diagnose-heart-iii4-reader-assembly.yml").exists(),"temporary workflow remains")
if errors:
    print(f"Heart III.4 reader assembly: FAIL ({len(errors)})",file=sys.stderr)
    for e in errors: print(f"- {e}",file=sys.stderr)
    raise SystemExit(1)
print("Heart III.4 reader assembly: PASS — union 136/289/30/6, reader 1681/15/0/0, readers 12/18, reviews 11/12, citation pass open")
