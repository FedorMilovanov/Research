import sys,re
sys.path.insert(0,"/home/user/Research/.scratch")
from q48lib import pages,ctx
def head(tid,pgs,n=200):
    P=pages(tid)
    for pg in pgs:
        if pg in P:
            raw=P[pg][0]
            print("  %s с. %s: %s" % (tid,pg,re.sub(r"\s+"," ",raw[:n])))
        else: print("  %s с. %s: —" % (tid,pg))
print("=== Bradwardine: заголовки вокруг 242—250 ===")
head("A16626",["232","233","240","241","242","248","249","250","251"],170)
P=pages("A16626")
raw,nx,idx=P["250"]
for pat in ["tacite","prædestinationis","de omnibus"]:
    for m in re.finditer(pat,nx,re.I):
        print("   с.250 /%s/: …%s…" % (pat,ctx(raw,idx,nx,m.start(),m.end(),pad=120)[:260]))
        break
print("\n=== Tillotson A62570: аргумент сермона перед 366 ===")
head("A62570",["360","361","362","363","364","365","366"],230)
print("\n=== Preston A09990 / A09950: «all men» + «condition» ===")
def flex(s):
    out=[]
    for ch in s.lower():
        if ch in "uv": out.append("[uv]")
        elif ch.isalnum(): out.append(re.escape(ch))
        else:
            if out and out[-1]=="\\W*": continue
            out.append("\\W*")
    return re.sub(r"^(\W\*)+","","".join(out))
for tid in ["A09990","A09950"]:
    P=pages(tid)
    for pat in ["woulde have all men","will haue all men","all men","condition"]:
        rx=re.compile(flex(pat),re.I); n=0; ex=[]
        for pg,(raw,nx,idx) in P.items():
            for m in rx.finditer(nx):
                n+=1
                if len(ex)<2: ex.append((pg,ctx(raw,idx,nx,m.start(),m.end(),pad=170)))
        print("  %s /%s/ → %d" % (tid,pat,n))
        for pg,c in ex:
            print("     с. %s : %s" % (pg,re.sub(r"\s+"," ",c)[:340]))
