#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сверка аппарата S7 (TEI) с официальным аппаратом издателя SBLGNT.

Зачем
-----
S7 — сторонняя перекодировка (`jjmccollum/sblgnt-tei`). Официальный аппарат
издан SBL и Logos и лежит в `Faithlife/SBLGNT` (CC BY 4.0, v1.2 2023-07-10),
файлы `data/sblgntapp/text/<Книга>.txt`. Он и служит независимым контролем:
сколько единиц, в каких стихах, какие свидетели.

Как запускать
-------------
1) скачать 27 файлов (вне Git; сеть — только к api.github.com):
   python3 sblgnt_official_crosscheck.py --fetch /tmp/sblgntapp
2) сверить и, при совпадении, получить PASS:
   python3 sblgnt_official_crosscheck.py --dir /tmp/sblgntapp --check

Что доказывается и что нет
--------------------------
Доказывается: число единиц и раскладка свидетелей по стихам, а также то, какой
сиглой TEI обозначает NA28. НЕ доказывается: чтения рукописей (их нет ни там,
ни там) и полный аппарат NA28/UBS5 (в официальном аппарате NA28 приведён
сравнительно, а не своим аппаратом).
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True

from sbl_apparatus import Apparatus

PIN = Path(__file__).resolve().parent.parent / "data" / "sblgnt-official-apparatus-pin.json"
REPO = "Faithlife/SBLGNT"
DIR = "data/sblgntapp/text"
WIT = re.compile(r"\b(WHapp|WHspur|WHmarg|WH|Tregmarg|Treg|NA28|NA27|RP|NIV|Holmes|ECM|Greeven|TR)\b")
BOOK = {"Matt": "Мф", "Mark": "Мк", "Luke": "Лк", "John": "Ин", "Acts": "Деян", "Rom": "Рим",
        "1Cor": "1 Кор", "2Cor": "2 Кор", "Gal": "Гал", "Eph": "Еф", "Phil": "Флп", "Col": "Кол",
        "1Thess": "1 Фес", "2Thess": "2 Фес", "1Tim": "1 Тим", "2Tim": "2 Тим", "Titus": "Тит",
        "Phlm": "Флм", "Heb": "Евр", "Jas": "Иак", "1Pet": "1 Пет", "2Pet": "2 Пет",
        "1John": "1 Ин", "2John": "2 Ин", "3John": "3 Ин", "Jude": "Иуд", "Rev": "Откр"}


def fetch(target: Path) -> int:
    target.mkdir(parents=True, exist_ok=True)
    listing = subprocess.run(["curl", "-sSL", "-m", "60",
                              f"https://api.github.com/repos/{REPO}/contents/{DIR}"],
                             capture_output=True, text=True, check=True).stdout
    names = [row["name"] for row in json.loads(listing)]
    for name in names:
        blob = subprocess.run(["curl", "-sSL", "-m", "60",
                               f"https://api.github.com/repos/{REPO}/contents/{DIR}/{name}"],
                              capture_output=True, text=True, check=True).stdout
        payload = json.loads(blob)["content"]
        (target / name).write_text(base64.b64decode(payload).decode("utf-8"), encoding="utf-8")
    print(f"скачано файлов: {len(names)} → {target}")
    return 0


def groups(body: str) -> list[tuple[str, ...]]:
    out = []
    for segment in re.split(r"[\]\;]", body):
        found = WIT.findall(segment)
        if found:
            out.append(tuple(sorted(found)))
    return out


def parse(directory: Path) -> tuple[dict[str, list], Counter]:
    units: dict[str, list] = defaultdict(list)
    census: Counter = Counter()
    for path in sorted(directory.glob("*.txt")):
        book = BOOK.get(path.stem)
        if not book:
            continue
        chapter = verse = None
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.replace("\xa0", " ").rstrip()
            if not line.strip():
                continue
            head = re.match(r"^.+?\s(\d+):(\d+)\s*$", line)
            if head:
                chapter, verse = int(head[1]), int(head[2])
                continue
            both = re.match(r"^(\d+):(\d+)\s+(.*)$", line)
            if both:
                chapter, verse, body = int(both[1]), int(both[2]), both[3]
            else:
                single = re.match(r"^(\d+)\s+(.*)$", line)
                if single:
                    verse, body = int(single[1]), single[2]
                elif line.lstrip().startswith("•"):
                    body = line.lstrip()[1:].strip()
                else:
                    continue
            ref = f"{book} {chapter}:{verse}"
            part = groups(body)
            units[ref].append(tuple(sorted(part)))
            for group in part:
                for witness in group:
                    census[witness] += 1
    return units, census


def compare(directory: Path) -> dict:
    official, census = parse(directory)
    apparatus = Apparatus()
    tei: dict[str, list] = defaultdict(list)
    for ref, entries in apparatus.entries.items():
        for entry in entries:
            tei[ref].append(tuple(sorted(tuple(sorted(r["wit"])) for r in entry["rdg"])))
    hypotheses = {"без замены": {}, "NIV→NA28": {"NIV": "NA28"}, "NA→NA28": {"NA": "NA28"},
                  "NIV→NA28, NA→NIV": {"NIV": "NA28", "NA": "NIV"}}
    refs = sorted(set(official) | set(tei))
    scores = {}
    for name, mapping in hypotheses.items():
        exact = 0
        for ref in refs:
            left = sorted(tuple(sorted(tuple(sorted(mapping.get(w, w) for w in group)) for group in unit))
                          for unit in tei.get(ref, []))
            if left == sorted(official.get(ref, [])):
                exact += 1
        scores[name] = exact
    return {"verses": len(refs),
            "unitsOfficial": sum(len(v) for v in official.values()),
            "unitsTei": sum(len(v) for v in tei.values()),
            "officialCensus": dict(sorted(census.items())),
            "hypothesisMatches": scores}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", metavar="DIR")
    parser.add_argument("--dir")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write-pin", action="store_true")
    args = parser.parse_args()
    if args.fetch:
        return fetch(Path(args.fetch))
    if not args.dir:
        parser.error("нужен --dir или --fetch")
    directory = Path(args.dir)
    result = compare(directory)
    digests = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(directory.glob("*.txt"))}
    result["datasetSha256OfSortedFileDigests"] = hashlib.sha256(
        json.dumps(digests, sort_keys=True).encode()).hexdigest()
    result["files"] = len(digests)
    result["bytes"] = sum(p.stat().st_size for p in directory.glob("*.txt"))
    result["source"] = {"repository": REPO, "dir": DIR, "license": "CC BY 4.0",
                        "version": "v1.2 (2023-07-10)", "fetch": "api.github.com contents API"}
    if args.write_pin:
        PIN.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"пин записан: {PIN}")
        return 0
    if args.check:
        pinned = json.loads(PIN.read_text(encoding="utf-8"))
        if pinned != result:
            differing = [k for k in set(pinned) | set(result) if pinned.get(k) != result.get(k)]
            print(f"FAIL: сверка с пином разошлась: {sorted(differing)}")
            return 1
        print(f"PASS: {result['unitsOfficial']} единиц официального аппарата против "
              f"{result['unitsTei']} в S7; раскладка совпала в {result['hypothesisMatches']['NIV→NA28']} "
              f"стихах из {result['verses']}")
        return 0
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
