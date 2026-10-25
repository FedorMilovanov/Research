#!/usr/bin/env python3
"""Пробник EEBO-TCP для реестра массы (круг 54).

Каналец, которым лан читает напечатанные листы: у textcreationpartnership каждый текст —
отдельный репозиторий, файл `<id>.xml` (TEI-P5). Этот скрипт его качает, кэширует и умеет три
вещи, которыми лан измерял строки реестра в кругах 52–53:

  fetch  <TCP-ID>…                 — скачать и посчитать дайджесты кэша (байты, md5, sha256)
  census <TCP-ID,….> --patterns F  — пройтись трафаретами по тому и напечатать попадания вместе
                                     с листом (n и facs), на котором они лежат
  pages  <TCP-ID>                  — карта листов и первые строки каждого листа (бегущие строки,
                                     напечатанные числа) — тем способом снят сдвиг нумерации
  imprint <TCP-ID>                 — титульные листы из <front> (срез по <body> глушит титул —
                                     дефект записан в §52 реестра, этот режим его обходит)

Три вещи, которые скрипт делает специально так, а не иначе:
  * поиск идёт по всему документу, а не по <body> — титул и препослание живут в <front>;
  * кроме обычного прохода есть буквальный (letters-only): набор разбит переносами и
    разрядкой, и в обычном проходе фраза молчит, будучи напечатанной;
  * молчание трафарета не превращается в отсутствие: режим печатает число трафаретов, которые
    не найдены, отдельной строкой, и ни один вызов не возвращает «отсутствует» как факт.
"""
from __future__ import annotations

import argparse, hashlib, io, json, os, re, sys, urllib.request

API = "https://api.github.com/repos/textcreationpartnership/%s/contents/%s.xml"
CACHE = os.environ.get("ATONEMENT_TCP_CACHE", ".scratch/tcp")
UA = "atonement-lane-probe/1 (recheck of the mass registry)"

TAG = re.compile(r"<[^>]+>")
PAGEBREAK = re.compile(r"<(pb|milestone)\b([^>]*)>", re.I)
NATTR = re.compile(r'\b(?:n|unit)\s*=\s*"([^"]*)"')
FACS = re.compile(r'\bfacs\s*=\s*"([^"]*)"')
LONGS = "æœſҝſ"


def cache_path(tcp_id: str) -> str:
    return os.path.join(CACHE, tcp_id + ".xml")


def fetch_one(tcp_id: str) -> tuple[str, bool]:
    path = cache_path(tcp_id)
    if os.path.isfile(path) and os.path.getsize(path) > 4096:
        return path, False
    os.makedirs(CACHE, exist_ok=True)
    url = API % (tcp_id, tcp_id)
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.raw",
                                              "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as fh:
        blob = fh.read()
    with open(path, "wb") as out:
        out.write(blob)
    return path, True


def digests(path: str) -> tuple[int, str, str]:
    b = io.open(path, "rb").read()
    return len(b), hashlib.md5(b).hexdigest(), hashlib.sha256(b).hexdigest()


def plain(text: str) -> tuple[str, list[int]]:
    """Текст без разметки, пробелы свёрнуты; map[i] — позиция i-го символа в raw-тексте."""
    out, map_ = [], []
    prev_space = False
    for m in re.finditer(r"<[^>]*>|[^<]+", text):
        s = m.group(0)
        if s[0] == "<":
            continue
        base = m.start()
        for j, ch in enumerate(s):
            if ch in " \t\r\n\f\v":
                if prev_space or not out:
                    continue
                out.append(" "); map_.append(base + j); prev_space = True
            else:
                out.append(ch); map_.append(base + j); prev_space = False
    return "".join(out), map_


def letters(text: str) -> tuple[str, list[int]]:
    """Буквы строчными, всё остальное выброшено; карта обратно в `text`."""
    keep, map_ = [], []
    for i, ch in enumerate(text):
        low = ch.lower()
        if low.isalpha() or low in LONGS:
            keep.append("s" if low == "ſ" else low)
            map_.append(i)
    return "".join(keep), map_


def page_map(text: str) -> list[tuple[int, str, str]]:
    """[(позиция в raw-тексте, номер листа, образ)] по <pb>/<milestone type=tcppage>."""
    out = []
    for m in PAGEBREAK.finditer(text):
        attrs = m.group(2)
        n = NATTR.findall(attrs)
        facs = FACS.search(attrs)
        label = n[0] if n else ""
        if "page" not in attrs.lower() and m.group(1).lower() == "milestone":
            continue
        out.append((m.start(), label, facs.group(1) if facs else ""))
    return out


def locate(pmap: list[tuple[int, str, str]], pos: int) -> tuple[str, str]:
    cur = ("", "")
    for p, n, f in pmap:
        if p <= pos:
            cur = (n, f)
        else:
            break
    return cur


def load_patterns(path: str) -> list[tuple[str, str]]:
    out = []
    for ln in io.open(path, encoding="utf-8"):
        ln = ln.rstrip("\n")
        if not ln.strip() or ln.startswith("#"):
            continue
        label, _, phrase = ln.partition("\t")
        if not phrase:
            label, phrase = ln, ln
        out.append((label, phrase))
    return out


def snippet(text: str, lo: int, hi: int, pad: int = 120) -> str:
    a, b = max(0, lo - pad), min(len(text), hi + pad)
    return text[a:b].replace("\n", " ")


def cmd_fetch(ids):
    for i in ids:
        path, fresh = fetch_one(i)
        n, md5, sha = digests(path)
        print("%-8s %s %10d Б  md5 %s  sha256 %s" % (i, "скачан" if fresh else "кэш   ", n, md5, sha[:16]))


def cmd_pages(tcp_id, limit=400):
    text = io.open(cache_path(tcp_id), encoding="utf-8", errors="replace").read()
    pmap = page_map(text)
    print("листов: %d" % len(pmap))
    for k, (p, n, f) in enumerate(pmap[:limit]):
        nxt = pmap[k + 1][0] if k + 1 < len(pmap) else len(text)
        head = re.sub(r"\s+", " ", TAG.sub(" ", text[p:nxt]))[:78].strip()
        print("  %-8s %-22s %s" % (n, f.split(":")[-1], head))


def cmd_imprint(tcp_id):
    text = io.open(cache_path(tcp_id), encoding="utf-8", errors="replace").read()
    front = re.search(r"<front\b.*?</front>", text, re.S)
    seg = front.group(0) if front else text[:20000]
    body = re.sub(r"\s+", " ", TAG.sub(" ", seg))
    print(body[:2600])


def cmd_census(ids, patfile, ctx=110):
    pats = load_patterns(patfile)
    print("трафаретов: %d" % len(pats))
    for tcp_id in ids:
        raw = io.open(cache_path(tcp_id), encoding="utf-8", errors="replace").read()
        p, pmap_idx = plain(raw)
        lt, lmap = letters(p)
        pmap = page_map(raw)
        print("\n===== %s =====" % tcp_id)
        silent = 0
        for label, phrase in pats:
            pl = re.compile(re.escape(phrase), re.I)
            hits = []
            for m in pl.finditer(p):
                rp = pmap_idx[m.start()]
                hits.append((locate(pmap, rp), snippet(p, m.start(), m.end(), ctx), "plain"))
            lp = re.compile(re.escape(letters(phrase)[0]), re.I)
            n_letter = 0
            if lp.pattern:
                for m in lp.finditer(lt):
                    n_letter += 1
                    if len(hits) < 40:
                        rp = pmap_idx[lmap[m.start()]]
                        hits.append((locate(pmap, rp),
                                     snippet(p, lmap[m.start()], lmap[m.end()], ctx), "letters"))
            if not hits:
                silent += 1
            np_ = len([h for h in hits if h[2] == "plain"])
            print("  [%s] plain=%d letters=%d  %s" % (label, np_, n_letter, "" if hits else "МОЛЧИТ"))
            seen = set()
            for (n, f), snip, kind in hits[:14]:
                key = (n, snip[:40])
                if key in seen:
                    continue
                seen.add(key)
                print("      %-7s %-18s %s | %s" % (n, f.split(":")[-1], kind,
                                                     "…" + snip.strip()[:230] + "…"))
        print("  молчит трафаретов: %d из %d" % (silent, len(pats)))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("fetch")
    a.add_argument("ids", nargs="+")
    b = sp.add_parser("census")
    b.add_argument("ids", help="через запятую")
    b.add_argument("--patterns", required=True)
    b.add_argument("--ctx", type=int, default=110)
    c = sp.add_parser("pages")
    c.add_argument("id")
    c.add_argument("--limit", type=int, default=400)
    d = sp.add_parser("imprint")
    d.add_argument("id")
    ns = ap.parse_args(argv)
    if ns.cmd == "fetch":
        cmd_fetch([x.strip().upper() for x in ns.ids if x.strip()])
    elif ns.cmd == "census":
        cmd_census([x.strip().upper() for x in ns.ids.split(",") if x.strip()], ns.patterns, ns.ctx)
    elif ns.cmd == "pages":
        cmd_pages(ns.id.upper(), ns.limit)
    else:
        cmd_imprint(ns.id.upper())


if __name__ == "__main__":
    main()
