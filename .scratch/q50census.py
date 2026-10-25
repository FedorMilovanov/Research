# -*- coding: utf-8 -*-
"""Круг 50: перепись всех 45 томов имени «Bunyan» из каталога EEBO-TCP (TCP.csv).
Считается по правилу 15zn: для каждого тома названы измеренные носители счёта,
а формулы ищутся не по одному тому: нуль по одному тому — это нуль по одному тому."""
import re, html, glob, json, pathlib, csv

FORM = {
 "удовлетворение за грехи мира": r"satisfaction[^.]{0,60}for the s?i?n?s of the worl|for the sins of the worl",
 "не за мир": r"not for the world|not for all the world",
 "умер за всех": r"(?:died|dyed|suffer(?:ed)?)[^.]{0,20}for all\b",
 "за всех людей": r"for all men|for every man|for all and everyone",
 "кто бы ни веровал": r"whosoever",
 "двойная уплата": r"(?:twice|a second time|two time|double payment|twice taker|again the same|the same debt again)",
 "только за избранных": r"onely for the Elect|only for the Elect|for the Elect\b",
 "отверженные": r"reprobate",
 "данные Отцом": r"gavest me|given me\b|those that thou gavest",
}
FILES = sorted(glob.glob(".scratch/bun/*.xml"))

def strip(s):
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()

def pblist(t):
    out = []
    for m in re.finditer(r'<pb\b([^>]*)/?>', t):
        n = re.search(r'\bn="([^"]*)"', m.group(1))
        out.append((m.start(), n.group(1) if n else None))
    return out

def page_of(pos, pbs):
    cur = None
    for p, n in pbs:
        if p > pos: break
        if n: cur = n
    return cur

def title_of(t):
    m = re.search(r"<title>(.*?)</title>", t, re.S)
    return strip(m.group(1))[:96] if m else "?"

def date_of(t):
    m = re.search(r"<date[^>]*>(.*?)</date>", t[t.index("<sourceDesc>"):], re.S) if "<sourceDesc>" in t else None
    return (m.group(1).strip() if m else "?")

rows = []
for f in FILES:
    t = pathlib.Path(f).read_text(encoding="utf-8")
    pbs = pblist(t)
    pb_all = len(re.findall(r"<pb\b", t)); pb_n = sum(1 for _, n in pbs if n)
    nums = len(re.findall(r"<num\b", t))
    rec = {"id": pathlib.Path(f).stem, "title": title_of(t), "date": date_of(t),
           "bytes": len(t), "pb": pb_all, "pb_n": pb_n, "num": nums, "hits": {}}
    for lab, pat in FORM.items():
        hits = [m.start() for m in re.finditer(pat, t, re.I)]
        pages = []
        for h in hits[:40]:
            pg = page_of(h, pbs)
            pages.append(pg)
        rec["hits"][lab] = {"n": len(hits), "pages": [p for p in pages if p][:12]}
    rows.append(rec)

tot = {lab: sum(r["hits"][lab]["n"] for r in rows) for lab in FORM}
vols_with = {lab: sum(1 for r in rows if r["hits"][lab]["n"]) for lab in FORM}
print("томов в переписи:", len(rows), "| байт:", sum(r["bytes"] for r in rows),
      "| делений <pb>:", sum(r["pb"] for r in rows), "| с печатным номером:", sum(r["pb_n"] for r in rows),
      "| <num>:", sum(r["num"] for r in rows))
print("\n%-30s %8s %8s" % ("формула", "вхожд.", "томов"))
for lab in FORM:
    print("%-30s %8d %8d" % (lab, tot[lab], vols_with[lab]))
print("\nтома с формулой «удовлетворение за грехи мира»:")
for r in rows:
    if r["hits"]["удовлетворение за грехи мира"]["n"]:
        print("   ", r["id"], r["date"], "| стр.", r["hits"]["удовлетворение за грехи мира"]["pages"], "|", r["title"][:70])
for lab in ("не за мир", "двойная уплата", "только за избранных"):
    print("\nтома с «%s»:" % lab)
    for r in rows:
        if r["hits"][lab]["n"]:
            print("   ", r["id"], r["date"], "| вхожд.", r["hits"][lab]["n"], "| стр.", r["hits"][lab]["pages"][:8], "|", r["title"][:60])
pathlib.Path(".scratch/q50census.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nряд pb по томам (первые/последние значения n):")
for r in rows[:6]:
    t = pathlib.Path(".scratch/bun/%s.xml" % r["id"]).read_text(encoding="utf-8")
    nn = [n for _, n in pblist(t) if n]
    print("   ", r["id"], r["pb"], "делений,", r["pb_n"], "с номером |", nn[:6], "…", nn[-4:])
