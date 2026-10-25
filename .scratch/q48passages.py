import sys,re
sys.path.insert(0,"/home/user/Research/.scratch")
from q48lib import pages,ctx
def flex(s):
    out=[]
    for ch in s.lower():
        if ch in "uv": out.append("[uv]")
        elif ch.isalnum(): out.append(re.escape(ch))
        else:
            if out and out[-1]=="\\W*": continue
            out.append("\\W*")
    return re.sub(r"^(\W\*)+","",s)
def grab(tid,page,pat,pad=650):
    P=pages(tid); raw,nx,idx=P[page]
    m=re.search(flex(pat),nx,re.I)
    if not m:
        m=re.search(pat.lower(),nx,re.I)
    if not m: return None
    s=ctx(raw,idx,nx,m.start(),m.end(),pad=pad)
    s=re.sub(r"\s+"," ",s).replace("ſ","s").replace("&amp;","&")
    s=re.sub(r"•+","",s); s=re.sub(r"-\s","",s)
    return s
for tid,page,pat in [
 ("N03743","64","universal redemption"),
 ("A62570","366","would have all men"),
 ("A16626","250","pro omnibus vt saluentur"),
 ("A16626","242","Eccleſia orat pro omnibus"),
 ("A15859","121","free loue of god"),
]:
    print("\n=====",tid,"с.",page)
    t=grab(tid,page,pat)
    print(t if t else "не нашёл")
