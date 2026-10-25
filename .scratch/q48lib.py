import pathlib,re,json,unicodedata
T=pathlib.Path("/home/user/Research/.scratch/txt")
REPL={"ſ":"s","Æ":"AE","æ":"ae","œ":"oe","ﬁ":"fi","ﬂ":"fl","’":"'","‘":"'","“":'"',"”":'"',"́":"","̀":"","̂":"","̃":"","̄":"","̆":"","̇":"","̈":"","̌":"","‑":"","‐":"","‒":"","–":"","—":" ","‑":""}
def nmap(raw):
    """normalized text + карта позиций: idx[j] = индекс в raw для j-го знака нормализованной строки"""
    out=[];idx=[];i=0;n=len(raw)
    while i<n:
        ch=raw[i]
        if ch=="-" and i+1<n and raw[i+1] in "\n ":
            i+=1; continue
        if ch in " \n\t\r":
            if out and out[-1]!=" ": out.append(" "); idx.append(i)
            i+=1; continue
        r=REPL.get(ch,None)
        if r is None:
            d=unicodedata.normalize("NFD",ch)
            base=d[0]; marks=d[1:]
            if marks and not base.strip(): base=" "
            for k,c in enumerate(base.lower()):
                out.append(c); idx.append(i)
            i+=1; continue
        for c in r.lower():
            out.append(c); idx.append(i)
        i+=1
    return "".join(out),idx
def pages(tid):
    """{напечатанная страница: (raw_text, norm, idx)} по маркерам <pb n="N">"""
    t=(T/(tid+".xml")).read_text(encoding="utf-8",errors="replace")
    t=re.sub(r"<note[^>]*>.*?</note>"," ",t,flags=re.S)
    toks=re.split(r'(<pb\b[^>]*>)',t)
    cur="pre"; acc={}
    for tk in toks:
        m=re.match(r'<pb\b[^>]*?n="([^"]*)"',tk)
        if m:
            cur=m.group(1).strip(); acc.setdefault(cur,[]); continue
        acc.setdefault(cur,[]).append(tk)
    out={}
    for pg,segs in acc.items():
        raw=" ".join(re.sub(r"<[^>]+>"," ",s) for s in segs)
        raw=re.sub(r"\s+"," ",raw).strip()
        nx,idx=nmap(raw)
        out[pg]=(raw,nx,idx)
    return out
def ctx(raw,idx,nx,a,b,pad=260):
    ra=idx[max(0,a-0)] if a<len(idx) else 0
    rb=idx[min(len(idx)-1,b)] if idx else len(raw)
    return raw[max(0,ra-pad):min(len(raw),rb+pad)]
def find(tid,pats,limit=60,pat=None):
    P=pages(tid); hits=[]
    rx=[re.compile(p) if pat=="re" else re.compile(re.escape(nmap(p)[0])) for p in pats]
    for pg,(raw,nx,idx) in P.items():
        for k,r in enumerate(rx):
            for m in r.finditer(nx):
                hits.append({"page":pg,"pat":pats[k],"ctx":ctx(raw,idx,nx,m.start(),m.end())})
                if len(hits)>=limit: return hits
    return hits
if __name__=="__main__":
    import sys
    tid=sys.argv[1]; kind=sys.argv[2]; pats=sys.argv[3:]
    H=find(tid,pats,pat=kind)
    print(tid,"| совпадений:",len(H))
    for h in H:
        print("\n— с.",h["page"],"|",h["pat"])
        print("  ",h["ctx"][:520])
