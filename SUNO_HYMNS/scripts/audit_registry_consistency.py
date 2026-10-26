#!/usr/bin/env python3
"""Аудит согласованности реестров: то, что гейты не проверяют.

`validate_project_registry.py` следит за схемой внутри JSON. Этот скрипт
проверяет связи **между файлами** — там, где расхождение не вызовет падения
гейта, но исказит работу:

1. дубликаты идентификаторов;
2. ссылки из претензий на несуществующие источники;
3. источники и претензии, отсутствующие в зеркалах Markdown;
4. идентификаторы, упомянутые в исследовательских документах, но не
   существующие в реестрах;
5. числа источников и претензий, названные в прозе, против факта;
6. токены со смешанной кириллицей и латиницей — опечатки вроде «Сисebut».

Только чтение. Код возврата 1, если найдено хоть что-то.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "SUNO_HYMNS" / "data"
RESEARCH = ROOT / "SUNO_HYMNS" / "RESEARCH"
SUNO = ROOT / "SUNO_HYMNS" / "SUNO"

SRC_JSON = DATA / "source-registry-v1.json"
CLM_JSON = DATA / "claim-ledger-v1.json"
SRC_MD = RESEARCH / "SOURCE_REGISTER.md"
CLM_MD = RESEARCH / "CLAIM_LEDGER.md"

ID_RE = re.compile(r"\b((?:SRC|CLM)-[A-Z0-9-]+)")
COUNT_RE = re.compile(
    r"(\d+)\s+(источник(?:а|ов)?|претензи(?:я|й|и)|claims?|sources?)", re.IGNORECASE
)
CYR = re.compile(r"[а-яА-ЯёЁ]")
LAT = re.compile(r"[a-zA-Z]")


def load(path, key):
    return json.loads(path.read_text(encoding="utf-8"))[key]


def main():
    problems = []
    notes = []

    sources = load(SRC_JSON, "sources")
    claims = load(CLM_JSON, "claims")
    src_ids = [s["id"] for s in sources]
    clm_ids = [c["id"] for c in claims]

    # 1. duplicates
    for label, ids in (("sources", src_ids), ("claims", clm_ids)):
        seen, dupes = set(), set()
        for i in ids:
            (dupes if i in seen else seen).add(i)
        if dupes:
            problems.append(f"дубликаты в {label}: {sorted(dupes)}")

    # 2. dangling source references from claims
    src_set = set(src_ids)
    for c in claims:
        for sid in c.get("sourceIds", []):
            if sid not in src_set:
                problems.append(f"{c['id']} ссылается на несуществующий {sid}")

    # 3. mirrors
    src_md = SRC_MD.read_text(encoding="utf-8") if SRC_MD.exists() else ""
    clm_md = CLM_MD.read_text(encoding="utf-8") if CLM_MD.exists() else ""
    missing_src_md = [i for i in src_ids if i not in src_md]
    missing_clm_md = [i for i in clm_ids if i not in clm_md]
    if missing_src_md:
        problems.append(f"нет в {SRC_MD.name}: {len(missing_src_md)} — "
                        f"например {missing_src_md[:5]}")
    if missing_clm_md:
        problems.append(f"нет в {CLM_MD.name}: {len(missing_clm_md)} — "
                        f"например {missing_clm_md[:5]}")

    # 4. ids mentioned in prose but absent from the registries
    known = src_set | set(clm_ids)
    docs = sorted(RESEARCH.glob("*.md")) + sorted(SUNO.glob("*.md"))
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        for m in ID_RE.findall(text):
            if m not in known:
                problems.append(f"{doc.relative_to(ROOT)}: упомянут несуществующий {m}")

    # 5. counts stated in prose
    n_src, n_clm = len(sources), len(claims)
    for doc in docs:
        for i, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
            for num, word in COUNT_RE.findall(line):
                n = int(num)
                w = word.lower()
                if w.startswith("источник"):
                    expected = n_src
                elif w.startswith("претензи"):
                    expected = n_clm
                elif w.startswith("claim"):
                    expected = n_clm
                else:
                    expected = n_src
                if n != expected:
                    notes.append(
                        f"{doc.relative_to(ROOT)}:{i}: названо «{num} {word}», "
                        f"в реестрах {expected} — проверить, не устарело ли"
                    )

    # 6. mixed-script tokens
    for doc in sorted(ROOT.glob("SUNO_HYMNS/**/*.md")):
        for i, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
            for tok in line.split():
                core = tok.strip(".,;:()«»\"'—–-")
                if CYR.search(core) and LAT.search(core) and len(core) > 2:
                    notes.append(f"{doc.relative_to(ROOT)}:{i}: смешанная запись «{core}»")

    print(f"источников: {n_src}   претензий: {n_clm}")
    print(f"документов проверено: {len(docs) + len(list(ROOT.glob('SUNO_HYMNS/**/*.md')))}")
    print()
    if problems:
        print("ПРОБЛЕМЫ:")
        for p in problems:
            print("  ✗", p)
    else:
        print("ПРОБЛЕМ НЕТ: идентификаторы, ссылки и зеркала согласованы.")
    if notes:
        print()
        print("К ПРОВЕРКЕ ВРУЧНУЮ:")
        for n in notes:
            print("  ?", n)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
