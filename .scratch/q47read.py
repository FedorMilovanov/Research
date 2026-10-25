import re,pathlib,json,collections,unicodedata,subprocess,os
ROOT=pathlib.Path("/home/user/Research")
reg=(ROOT/"docs/research/atonement/35_four_point_authors_mass_registry.md").read_text()
q2row={}; tab={}; addr_row={}
for l in reg.split("\n"):
    m=re.match(r"^- Q-(0*\d+) — (.*)",l,re.S)
    if m: q2row["Q-%02d"%int(m.group(1))]=m.group(2)
    m=re.match(r"^\| (FP-0*(\d+)) \|(.*)\|\s*$",l)
    if m: tab["FP-%02d"%int(m.group(2))]=[x.strip() for x in m.group(3).split("|")]
for rid,cells in tab.items():
    for x in re.findall(r"Q-(\d+)"," ".join(cells)):
        q="Q-%02d"%int(x)
        if q in q2row and q not in addr_row: addr_row[q]=rid
pr=json.loads((ROOT/".scratch/q47probe.json").read_text())
first=pr["first"]; targets=[q for q in pr["adr_with"]]
def plain(s):
    s=re.sub(r'<g ref="char:EOLhyphen"/?>',"",s)
    s=re.sub(r"<[^>]+>"," ",s)
    s=s.replace("&amp;","&").replace("&quot;",'"')
    return re.sub(r"\s+"," ",s).strip()
def norm(s):
    s=s.replace("ſ","s").replace("ﬁ","fi").replace("ﬀ","ff").replace("æ","ae").replace("oe","oe")
    s=unicodedata.normalize("NFKD",s).lower()
    s=re.sub(r"[^a-z ]+"," ",s).replace("v","u")
    return re.sub(r"\s+"," ",s).strip()
def pages(t):
    """сегменты по маркерам печатных страниц: [(n, norm_text, orig_text)]"""
    segs=[]; cur=None
    pos=[(m.start(),m.group(1)) for m in re.finditer(r'<pb n="(\d+)"',t)]
    for i,(p,n) in enumerate(pos):
        end=pos[i+1][0] if i+1<len(pos) else len(t)
        raw=t[p:end]; body=plain(raw)
        segs.append((int(n),norm(body),body))
    return segs
def fetch(tid):
    f=ROOT/(".scratch/txt/%s.xml"%tid)
    if f.exists() and f.stat().st_size>2000: return f
    r=subprocess.run(["curl","-sS","-L","-H","Accept: application/vnd.github.raw",
        "https://api.github.com/repos/textcreationpartnership/%s/contents/%s.xml"%(tid,tid),"-o",str(f)],
        capture_output=True,text=True,timeout=240)
    return f if f.exists() and f.stat().st_size>2000 else None
QU=re.compile(r"[«]([^»]{15,})[»]")
res={}; nocite=[]
for q in targets:
    tid=first.get(q)
    if not tid: continue
    f=fetch(tid)
    if not f: nocite.append(q+": нет файла "+tid); continue
    t=f.read_text(encoding="utf-8",errors="replace")
    segs=pages(t)
    row=tab.get(addr_row.get(q,""),[])
    hay=" ".join(row)+" "+q2row.get(q,"")
    quotes=[x for x in QU.findall(hay) if not re.search(r"[а-яё]",x) and len(norm(x))>=14]
    quotes=[x for x in quotes if len(x.split())>=3]
    hits=[]
    for qt in quotes[:6]:
        nq=norm(qt)
        if len(nq)<14: continue
        for (pg,nt,ot) in segs:
            k=nt.find(nq)
            if k>=0:
                hits.append({"quote":qt,"page":pg,"ctx":ot[max(0,k-160):k+len(qt)+260],"tcp":tid,"row":addr_row.get(q)})
                break
        if hits and hits[-1]["quote"]==qt: break
    res[q]={"tcp":tid,"bytes":f.stat().st_size,"quotes":quotes[:6],"hits":hits[:2],"строк":len(secs) if False else len(segs)}
    if not quotes: nocite.append(q+" : нет цитаты латиницей/английском из 15 букв")
(ROOT/".scratch/q47read.json").write_text(json.dumps({"res":res,"nocite":nocite},ensure_ascii=False,indent=1))
print("адресов обработано:",len(res),"| с попаданием цитаты:",sum(1 for v in res.values() if v["hits"]))
for q,v in res.items():
    if v["hits"]:
        h=v["hits"][0]
        print("\n%s  %s  стр.%s\n   ЦИТАТА: %s\n   ТЕКСТ: %s"%(q,h["tcp"],h["page"],h["quote"][:110],re.sub(r"\s+"," ",plain(h["ctx"]))[:330]))
print("\nбез цитаты/прочее (%d):"%len(nocite)); [print("  ",x) for x in nocite[:40]]
