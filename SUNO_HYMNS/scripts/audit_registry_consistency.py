#!/usr/bin/env python3
"""Аудит согласованности реестров: то, что гейты не проверяют.

`validate_project_registry.py` следит за схемой внутри JSON. Этот скрипт
проверяет связи **между файлами** — там, где расхождение не вызовет падения
гейта, но исказит работу:

1. дубликаты идентификаторов;
2. ссылки из претензий на несуществующие источники;
3. карточки источников и претензий в Markdown, их операционные состояния и HOLDs;
4. идентификаторы, упомянутые в исследовательских документах, но не
   существующие в реестрах;
5. числа источников и претензий, названные в прозе, против факта;
6. токены со смешанной кириллицей и латиницей — опечатки вроде «Сисebut».

Только чтение. Код возврата 1 при ошибках идентификаторов, ссылок или состояний.
Наблюдения о числах и смешанном алфавите — подсказки для ручной проверки, не ошибки гейта.
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


MIRROR_FIELDS = {
    "evidence class": "evidenceClass",
    "access": "accessState", "access state": "accessState",
    "locator": "locatorState", "locator state": "locatorState",
    "rights": "rightsState", "rights state": "rightsState",
    "publication": "publicationState", "publication state": "publicationState",
    "review state": "claimStatus", "holds": "holds",
}
SOURCE_STATES = ("evidenceClass", "accessState", "locatorState", "rightsState", "publicationState")


def _visible_metadata(text):
    """Mask fenced examples and HTML comments before looking for declarations."""
    lines = []
    fence = None
    comment = False

    def mask_comment(match):
        nonlocal comment
        comment = not match[0].endswith("-->")
        return " " * len(match[0])

    for line in text.splitlines(keepends=True):
        if fence is not None:
            if fence.fullmatch(line):
                fence = None
            lines.append("\n")
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})", line) if not comment else None
        if opening:
            marker = opening[1]
            fence = re.compile(r" {0,3}" + re.escape(marker[0])
                               + r"{" + str(len(marker)) + r",}[ \t]*(?:\r?\n)?")
            lines.append("\n")
            continue
        if comment:
            end = line.find("-->")
            if end < 0:
                lines.append("\n")
                continue
            line = " " * (end + 3) + line[end + 3:]
            comment = False
        lines.append(re.sub(r"<!--.*?(?:-->|$)", mask_comment, line))
    return "".join(lines)


def mirror_states(text):
    """Read declared fields, not incidental IDs/HOLDs in explanatory prose.

    The ledger retains dated revisions. A later explicitly declared field replaces
    that field only; a note-only revision must not erase a previous state or HOLD.
    This checks operational metadata, not equality of the scientific prose.
    """
    text = _visible_metadata(text)
    cards = {}
    headings = list(re.finditer(r"^#{1,6} (.+)$", text, re.M))
    labels = "|".join(re.escape(label) for label in MIRROR_FIELDS)
    field_re = re.compile(r"^(?:- )?(" + labels + r"):[ \t]*([^\n]*)$", re.M | re.I)
    # Sources/Level delimit existing compact rows, but are not state fields.
    compact_labels = labels + "|sources|level"
    separator_re = re.compile(
        r"(?:[ \t]+·[ \t]+|\.[ \t]+(?=HOLDs:))(?=(?:- )?(?:" + compact_labels + r"):)", re.I
    )
    for i, heading in enumerate(headings):
        ident = re.match(r"(?:Revised:\s*)?((?:SRC|CLM)-[A-Z0-9-]+)(?=\s|$)", heading[1])
        if not ident:
            continue
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        body = text[heading.end():end].replace("**", "").replace("`", "")
        # Only split an actual metadata line, and only before another field.
        # A quoted label in Notes/Limits must not become an operational override.
        body = "\n".join(separator_re.sub("\n", line) for line in body.splitlines()
                         if field_re.fullmatch(line))
        fields = cards.setdefault(ident[1], {})
        for match in field_re.finditer(body):
            field = MIRROR_FIELDS[match[1].lower()]
            if field == "holds":
                value = match[2].strip()
                if not value or value.removesuffix(".").casefold() in {"none", "none recorded", "нет", "—"}:
                    fields[field] = set()
                elif re.fullmatch(r"[A-Z][A-Z0-9_]+(?:[ \t]*[,;][ \t]*[A-Z][A-Z0-9_]+)*[.;]?", value):
                    fields[field] = set(re.findall(r"\b[A-Z][A-Z0-9_]+\b", value))
                else:
                    # Keep malformed text visible as a mismatch, never as an empty set.
                    fields[field] = {value}
            else:
                value = re.fullmatch(
                    r"([A-Z][A-Z0-9_]*)(?:[.;]|[ \t]+(?:\([^\n]*\)|—[^\n]*))?[ \t]*", match[2]
                )
                fields[field] = value[1] if value else None
    return cards


def check_mirror_states(records, text, state_fields, problems):
    cards = mirror_states(text)
    for record in records:
        ident = record["id"]
        if ident not in cards:
            problems.append(f"{ident}: нет отдельной Markdown-карточки")
            continue
        fields = cards[ident]
        for field in state_fields:
            if fields.get(field) != record[field]:
                problems.append(f"{ident}: Markdown {field}={fields.get(field)!r}, JSON {record[field]!r}")
        expected = set(record.get("holds", []))
        actual = fields.get("holds", set())
        if actual != expected:
            problems.append(f"{ident}: Markdown HOLDs={sorted(actual)}, JSON {sorted(expected)}")


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
    check_mirror_states(sources, src_md, SOURCE_STATES, problems)
    check_mirror_states(claims, clm_md, ("claimStatus",), problems)

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

    # 6. mixed-script tokens (this inventory also includes the prose scans above)
    all_docs = sorted(ROOT.glob("SUNO_HYMNS/**/*.md"))
    for doc in all_docs:
        for i, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
            for tok in line.split():
                core = tok.strip(".,;:()«»\"'—–-")
                if CYR.search(core) and LAT.search(core) and len(core) > 2:
                    notes.append(f"{doc.relative_to(ROOT)}:{i}: смешанная запись «{core}»")

    print(f"источников: {n_src}   претензий: {n_clm}")
    print(f"документов проверено: {len(all_docs)}")
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
