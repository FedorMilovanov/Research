import sys,json,pathlib,re
sys.path.insert(0,"/home/user/Research/.scratch")
from q48lib import pages,ctx
read=json.loads(pathlib.Path("/home/user/Research/.scratch/q47read.json").read_text(encoding="utf-8"))["res"]
CAND=["Q-02","Q-12","Q-22","Q-58","Q-64","Q-74","Q-78","Q-81","Q-164","Q-167"]
def flexible(q):
    out=[]
    for ch in q:
        if ch.isalnum():
            c=ch.lower()
            out.append("[uv]" if c in "uv" else re.escape(c))
        else:
            if out and out[-1]=="\\W*": continue
            out.append("\\W*")
    s="".join(out).strip("\\W*")
    s=re.sub(r"^(\\W\*)+","",s); s=re.sub(r"(\\W\*)+$","",s)
    return s
res={}
for q in CAND:
    v=read.get(q) or {}
    tid=v.get("tcp"); quotes=v.get("quotes") or []
    if not tid or not quotes:
        res[q]={"tcp":tid,"проверено":0,"hits":[],"note":"нет файла или цитаты"}
        continue
    P=pages(tid)
    hits=[]
    for qi,qt in enumerate(quotes[:3]):
        pat=flexible(qt)
        if len(pat)<12: continue
        rx=re.compile(pat,re.I)
        for pg,(raw,nx,idx) in P.items():
            for m in rx.finditer(nx):
                hits.append({"quote":qt[:70],"page":pg,"ctx":ctx(raw,idx,nx,m.start(),m.end())[:420]})
                break
            if hits and hits[-1]["quote"]==qt[:70]: break
    res[q]={"tcp":tid,"цитат":len(quotes[:3]),"hits":hits[:6],"hit":bool(hits)}
    print("%-6s %-14s цитат %d → попаданий %d" % (q,tid,len(quotes[:3]),len(hits)))
    for h in hits[:3]:
        print("     с. %s | %s" % (h["page"],h["ctx"][:300].replace("\n"," ")))
pathlib.Path("/home/user/Research/.scratch/q48quotes.json").write_text(json.dumps(res,ensure_ascii=False,indent=1),encoding="utf-8")
print("\nитоги:",sum(1 for v in res.values() if v.get("hit")),"с попаданием из",len(CAND))
