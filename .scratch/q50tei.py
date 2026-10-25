# -*- coding: utf-8 -*-
"""Круг 50: разбор TEI A30198 (Bunyan, Reprobation asserted, 1674) и A30141
(Bunyan, The doctrine of the law and grace unfolded, 1685) — носители счёта,
выходные, и поиск формул по строке FP-136 / очереди Q-136.
Считается по правилу 15zn: отрицание или подтверждение счёта страниц
возможно только со списком измеренных носителей; локатор обязан называть систему счёта."""
import re, sys, pathlib, html

FILES = {"A30198": "docs of Reprobation asserted", "A30141": "Law and grace unfolded"}

def load(pid):
    return pathlib.Path(".scratch/%s.xml" % pid).read_text(encoding="utf-8")

def head(txt, tag):
    m = re.search(r"<%s>(.*?)</%s>" % (tag, tag), txt, re.S)
    if not m:
        return ""
    s = re.sub(r"<[^>]+>", " ", m.group(1))
    return html.unescape(re.sub(r"\s+", " ", s)).strip()

def carriers(txt):
    """все носители счёта, перечисленные, а не по одному признаку"""
    pb_all = re.findall(r"<pb\b[^>]*/?>", txt)
    pb_n = [p for p in pb_all if " n=" in p]
    pb_f = [p for p in pb_all if " facs=" in p]
    nums = re.findall(r"<num\b[^>]*>", txt)
    runs = re.findall(r"<milestone\b[^>]*unit=\"page\"[^>]*/?>", txt)
    return dict(pb=len(pb_all), pb_n=len(pb_n), pb_facs=len(pb_f), num=len(nums), milestone=len(runs))

def pb_list(txt):
    """позиции и значения печатных номеров"""
    out = []
    for m in re.finditer(r'<pb\b([^>]*)/?>', txt):
        at = m.group(1)
        n = re.search(r'\bn="([^"]*)"', at)
        f = re.search(r'\bfacs="([^"]*)"', at)
        out.append((m.start(), n.group(1) if n else None, f.group(1) if f else None))
    return out

def page_of(pos, pbs):
    cur = None
    for p, n, f in pbs:
        if p > pos:
            break
        if n:
            cur = (n, f)
        elif f and cur is None:
            cur = (None, f)
    return cur

def plain(txt, a, b):
    s = re.sub(r"<[^>]+>", "", txt[a:b])
    return html.unescape(re.sub(r"\s+", " ", s)).strip()

def grep(txt, pbs, pat, label, window=430, limit=14):
    hits = []
    for m in re.finditer(pat, txt, re.I):
        a = max(0, m.start() - 40)
        seg = plain(txt, a, m.end() + window)
        pg = page_of(m.start(), pbs)
        hits.append((pg, seg))
    print("\n--- %s: найдено %d" % (label, len(hits)))
    seen = set()
    for pg, seg in hits[:limit]:
        key = (pg[0] if pg else None, seg[:60])
        if key in seen:
            continue
        seen.add(key)
        print("    стр.=%s факс=%s | %s" % (pg[0] if pg else "?", (pg[1][-14:] if pg and pg[1] else "?"), seg[:400]))
    return hits

def main(pid):
    txt = load(pid)
    print("=" * 78)
    print(pid, "|", FILES.get(pid, ""))
    print("title:", head(txt, "title")[:300])
    print("imprint:", head(txt, "imprint")[:300])
    ext = re.search(r"<extent>(.*?)</extent>", txt, re.S)
    print("extent:", html.unescape(ext.group(1)).strip()[:200] if ext else "")
    notes = re.findall(r"<note\b[^>]*>(.*?)</note>", txt[:12000], re.S)
    print("заметки заголовка:", [html.unescape(re.sub(r"<[^>]+>", " ", x)).strip()[:160] for x in notes[:6]])
    print("носители счёта:", carriers(txt))
    pbs = pb_list(txt)
    nn = [n for _, n, _ in pbs if n]
    print("нумерованных pb: %d | первые: %s | последних: %s" % (len(nn), nn[:12], nn[-6:]))
    resets = [i for i in range(1, len(nn)) if nn[i].isdigit() and nn[i-1].isdigit() and int(nn[i]) < int(nn[i-1])]
    print("сбросов нумерации (по цифровым):", len(resets))
    print("всего делений:", len(pbs))
    return txt, pbs

if __name__ == "__main__":
    for pid in sys.argv[1:]:
        main(pid)
