import csv,re,json,sys
rows=list(csv.DictReader(open("/home/user/Research/.scratch/TCP.csv",encoding="utf-8-sig")))
want=["N03743","A62570","A62579","A15859","A09997","N03644","N03645","A16626","A12183","A09950","A09990","A09972","A09967"]
by={r["TCP"]:r for r in rows}
for w in want:
    r=by.get(w)
    print("\n---",w,"Есть" if r else "НЕТ В КАТАЛОГЕ")
    if r:
        for k in ("TCP","EEBO","VID","STC","Status","Author","Date","Title","Pages"):
            v=(r.get(k) or "").strip()
            print("   %-7s %s" % (k, v[:230]))
