import sys,re
sys.path.insert(0,"/home/user/Research/.scratch")
from q48lib import pages,ctx
P=pages("A16626")
WANT=["98","242","249","250","264","274","357","359","362","406","573","636","657","699"]
rx=re.compile(r"pro omnibus",re.I)
print("страниц в карте:",len(P))
for pg in WANT:
    if pg not in P: print("\n### с.",pg,"— нет в карте (ключи рядом:",[k for k in P if k.isdigit() and abs(int(k)-int(pg))<=2][:6],")"); continue
    raw,nx,idx=P[pg]
    ms=list(rx.finditer(nx))
    print("\n### с. %s — вхождений %d" % (pg,len(ms)))
    for m in ms[:3]:
        print("   ",ctx(raw,idx,nx,m.start(),m.end(),pad=420).replace("\n"," ")[:760])
