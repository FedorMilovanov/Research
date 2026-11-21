#!/usr/bin/env python3
"""Check the counters printed in the HOLD register against the artefacts they describe.

The register's §2 says "1 966 canonical LOCATOR_HOLD mentions". If the inventory is
regenerated and the number moves, that sentence keeps asserting the old value - it
becomes a quotation of a previous state of a file, which is the defect this whole
document keeps finding elsewhere. Nothing in the repo noticed, because a number in prose
is not a link and not a digest.

So each printed counter that has a machine home is declared here once, with the exact
artefact field it mirrors, and checked both ways:

* ``match``  - the register prints what the artefact says;
* ``stale``  - the register prints something else, and here is the truth;
* ``anchor-missing`` - the sentence the claim talks about is gone (renamed or deleted),
  which also has to be reported rather than silently skipped;
* ``source-missing`` - the artefact or field is missing.

``--check`` exits non-zero on anything but ``match``. It refuses to touch the register:
the point is to report the drift, not to launder it.

    python3 -B scripts/audit_register_claims.py --check
    python3 -B scripts/audit_register_claims.py --summary
    python3 -B scripts/audit_register_claims.py -o data/register-claims-audit-2026-11-18.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA_VERSION = "register-claims-audit/1"
AUTHORITY_ID = "REGISTER-CLAIMS-AUDIT-2026-11-18"
REGISTER = "docs/research/HOLDS_REGISTER_2026-11-18.md"

INVENTORY = "data/repository-holds-inventory-v1.json"
DIGESTS = "data/internal-digests-verified-2026-11-18.json"
TWINS = "data/document-twins-2026-11-18.json"
STAMPS = "data/state-stamps-2026-11-18.json"
LEDGER = "data/drive-ledger-audit-2026-11-18.json"
REGISTRY = "data/hold-closure-registry-v1.json"
LINKS = "data/relative-links-audit-2026-11-18.json"
REPAIRS = "data/text-integrity-repairs-2026-11-18.json"
PROPOSAL = "data/hold-value-mapping-proposal-v1.json"
PINNED = "data/pinned-github-locators-verified-2026-11-18.json"
QUEUE = "data/publication-gate-queue-v1.json"
# TWINS and STAMPS already exist as claim artefacts; these are their generated tables.

# label as printed in the register -> (artefact, field). The label is matched literally
# inside a markdown table row, so a reworded row is reported instead of passing silently.
CLAIMS: list[tuple[str, str, str]] = [
    # §2 machine slice
    ("просканировано текстовых файлов", INVENTORY, "totals.filesScanned"),
    ("файлов хотя бы с одним маркером", INVENTORY, "totals.filesWithMentions"),
    ("канонические упоминания `PUBLICATION_HOLD`", INVENTORY, "totals.mentions.PUBLICATION_HOLD"),
    ("канонические упоминания `LOCATOR_HOLD`", INVENTORY, "totals.mentions.LOCATOR_HOLD"),
    ("канонические упоминания `RIGHTS_HOLD`", INVENTORY, "totals.mentions.RIGHTS_HOLD"),
    ("канонические упоминания `ARCHIVE_HOLD`", INVENTORY, "totals.mentions.ARCHIVE_HOLD"),
    ("канонические упоминания `EVIDENCE_HOLD`", INVENTORY, "totals.mentions.EVIDENCE_HOLD"),
    ("строки, где флаг зафиксирован как действующий (`open`)", INVENTORY, "totals.mentionsByStatus.open"),
    ("строки, где флаг зафиксирован как снятый (`closed`)", INVENTORY, "totals.mentionsByStatus.closed"),
    ("строки без явного состояния (`unmarked`)", INVENTORY, "totals.mentionsByStatus.unmarked"),
    ("строки, где одновременно записаны и снятие, и сохранение (`mixed`)",
     INVENTORY, "totals.canonicalFlagLineStatesRecordedAsBothOpenAndClosed"),
    ("JSON-файлов с массивом `holds`", INVENTORY, "totals.filesWithJsonHolds"),
    # §13 signature states
    ("`match`", DIGESTS, "totals.byState.match"),
    ("`stale`", DIGESTS, "totals.byState.stale"),
    ("`external`", DIGESTS, "totals.byState.external"),
    ("`external-drive`", DIGESTS, "totals.byState.external-drive"),
    ("`ambiguous`", DIGESTS, "totals.byState.ambiguous"),
    ("`unclaimed`", DIGESTS, "totals.byState.unclaimed"),
    ("`git-object-id`", DIGESTS, "totals.byState.git-object-id"),
    # §18 unclaimed reasons
    ("`labelled-no-path`", DIGESTS, "totals.unclaimedByReason.labelled-no-path"),
    ("`bare-hash`", DIGESTS, "totals.unclaimedByReason.bare-hash"),
    ("`short-digest-no-path`", DIGESTS, "totals.unclaimedByReason.short-digest-no-path"),
    ("`artifact-not-in-tree`", DIGESTS, "totals.unclaimedByReason.artifact-not-in-tree"),
    ("`media-segment`", DIGESTS, "totals.unclaimedByReason.media-segment"),
    ("`corpus-digest`", DIGESTS, "totals.unclaimedByReason.corpus-digest"),
    # §15 twin states
    ("`identical-text`", TWINS, "totals.byState.identical-text"),
    ("`near-identical`", TWINS, "totals.byState.near-identical"),
    ("`shared-text`", TWINS, "totals.byState.shared-text"),
    ("`superset`", TWINS, "totals.byState.superset"),
    # §16 stamp states
    ("`current` — последний коммит в тот же день", STAMPS, "totals.byState.current"),
    ("`edited-after-stamp` — файл менялся после своей даты", STAMPS, "totals.byState.edited-after-stamp"),
    ("`stamp-ahead-of-history` — дата позже любого коммита", STAMPS,
     "totals.byState.stamp-ahead-of-history"),
    # Scopes that used to live in prose and had to be re-typed at every merge: they are
    # table rows now, generated from the reports like every other number here.
    ("сравнено документов", TWINS, "scope.documentsCompared"),
    ("документов в корпусе", TWINS, "scope.markdownFiles"),
    ("документов со своей датой", STAMPS, "totals.stamped"),
]

# Three or more cells: the register also has tables where the number sits in the
# second cell and a description follows in the third.
# The §2.1 corpus table is not transcribed by hand any more: 25 rows of counters that
# change whenever the inventory is regenerated would always be one regeneration behind.
CORPUS_BEGIN = "<!-- corpus-table:begin -->"
CORPUS_END = "<!-- corpus-table:end -->"


def fmt(number: int) -> str:
    """Thousands separator as a thin space - and only the digits, never the label."""
    return f"{number:,}".replace(",", "\u2009")


def render_corpus_table(inventory: dict) -> str:
    by_corpus = inventory.get("byCorpus", {})
    rows = []
    for name, block in by_corpus.items():
        rows.append((name, block.get("files", 0), sum(block.get("mentions", {}).values())))
    rows.sort(key=lambda item: (-item[2], -item[1], item[0]))
    lines = [CORPUS_BEGIN,
             "| Корпус | Файлов с маркерами | Канонических упоминаний |",
             "|---|---:|---:|"]
    for name, files, mentions in rows:
        label = "корневые файлы" if name == "_root" else f"`{name}/`"
        lines.append(f"| {label} | {files} | {fmt(mentions)} |")
    lines.append(CORPUS_END)
    return "\n".join(lines)


def replace_corpus_block(text: str, block: str) -> tuple[str, bool]:
    start, end = text.find(CORPUS_BEGIN), text.find(CORPUS_END)
    if start == -1 or end == -1 or end < start:
        return text, False
    return text[:start] + block + text[end + len(CORPUS_END):], True



# §2 is the inventory's own table. Same argument as §2.1: a hand-kept copy of counters that
# move whenever a file mentions a flag can only ever be one edit behind.
SLICE_BEGIN = "<!-- inventory-slice:begin -->"
SLICE_END = "<!-- inventory-slice:end -->"
SLICE_ROWS = [
    ("просканировано текстовых файлов", "totals.filesScanned"),
    ("файлов хотя бы с одним маркером", "totals.filesWithMentions"),
    ("канонические упоминания `PUBLICATION_HOLD`", "totals.mentions.PUBLICATION_HOLD"),
    ("канонические упоминания `LOCATOR_HOLD`", "totals.mentions.LOCATOR_HOLD"),
    ("канонические упоминания `RIGHTS_HOLD`", "totals.mentions.RIGHTS_HOLD"),
    ("канонические упоминания `ARCHIVE_HOLD`", "totals.mentions.ARCHIVE_HOLD"),
    ("канонические упоминания `EVIDENCE_HOLD`", "totals.mentions.EVIDENCE_HOLD"),
    ("строки, где флаг зафиксирован как действующий (`open`)", "totals.mentionsByStatus.open"),
    ("строки, где флаг зафиксирован как снятый (`closed`)", "totals.mentionsByStatus.closed"),
    ("строки без явного состояния (`unmarked`)", "totals.mentionsByStatus.unmarked"),
    ("строки, где одновременно записаны и снятие, и сохранение (`mixed`)",
     "totals.canonicalFlagLineStatesRecordedAsBothOpenAndClosed"),
    ("JSON-файлов с массивом `holds`", "totals.filesWithJsonHolds"),
]


def render_slice_table(inventory: dict) -> str:
    lines = [SLICE_BEGIN, "| Показатель | Значение |", "|---|---:|"]
    for label, field in SLICE_ROWS:
        node = inventory
        for part in field.split("."):
            node = node.get(part, {}) if isinstance(node, dict) else {}
        if isinstance(node, int):
            lines.append(f"| {label} | {fmt(node)} |")
    lines.append(SLICE_END)
    return "\n".join(lines)


def replace_slice_block(text: str, block: str) -> tuple[str, bool]:
    start, end = text.find(SLICE_BEGIN), text.find(SLICE_END)
    if start == -1 or end == -1 or end < start:
        return text, False
    return text[:start] + block + text[end + len(SLICE_END):], True



# Numbers that live inside sentences rather than tables: a pattern with one numeric group,
# the artefact field it must equal, and optionally the section that re-shot it. A claim
# that was true when written and has since been superseded is not an error to be silently
# edited away - the register keeps its history - but it must point at the section that
# carries the current value, and that section must exist below the claim.
PROSE_CLAIMS: list[dict] = [
    {"id": "drive-sample-in-section-11",
     "pattern": r"Проверено (?P<n>\d+) из \d+ объектов",
     "artefact": LEDGER, "field": "scope.distinctDriveIds", "supersededBy": "§19"},
    {"id": "fragment-links-in-section-11",
     "pattern": r"Ссылок с фрагментом в репозитории \*\*(?P<n>[\d\s\u2009]+)\*\*",
     "artefact": LINKS, "field": "totals.fragments.total"},
    # The vocabulary numbers were the least checked in the register: four places said the
    # same thing, nothing verified any of them, and one of them (39 files in the §2 row)
    # was simply wrong. They now have one home and a field each.
    {"id": "json-holds-files",
     "pattern": r"В (?P<n>\d+) JSON-файл(?:ах|е)(?=\s)",
     "artefact": INVENTORY, "field": "totals.filesWithJsonHolds"},
    {"id": "json-holds-values",
     "pattern": r"содержат (?P<n>[\d\s\u2009]+) значений",
     "artefact": INVENTORY, "field": "totals.jsonHoldsTotal"},
    {"id": "hold-vocabulary-values",
     "pattern": r"из них \*\*(?P<n>\d+) \(",
     "artefact": PROPOSAL, "field": "counts.values"},
    {"id": "hold-vocabulary-spellings",
     "pattern": r"\((?P<n>\d+) написаний\)",
     "artefact": PROPOSAL, "field": "counts.spellings"},
    {"id": "holds-array-files-in-section-2",
     "pattern": r"Гигиена машинных реестров \| (?P<n>\d+) файл(?:а|ов)?(?=\s+с массивом)",
     "artefact": INVENTORY, "field": "totals.filesWithJsonHolds"},
    # §10 quoted the gate's counts by hand; each now has a field in the queue snapshot.
    {"id": "gate-records",
     "pattern": r"Сейчас: (?P<n>\d+) записей",
     "artefact": QUEUE, "field": "len:records"},
    {"id": "gate-blocked",
     "pattern": r"`BLOCKED=(?P<n>\d+)`",
     "artefact": QUEUE, "field": "composedCounts.BLOCKED"},
    {"id": "gate-reference",
     "pattern": r"`REFERENCE=(?P<n>\d+)`",
     "artefact": QUEUE, "field": "composedCounts.REFERENCE"},
    {"id": "gate-promote",
     "pattern": r"`PROMOTE=(?P<n>\d+)`",
     "artefact": QUEUE, "field": "composedCounts.PROMOTE"},
    {"id": "gate-rights-ids-not-recorded",
     "pattern": r"\((?P<n>\d+)\s+потерянных",
     "artefact": QUEUE, "field": "checks.rightsIdsNotRecorded"},
    {"id": "gate-missing-authorities",
     "pattern": r"\((?P<n>\d+)\s+отсутствующих",
     "artefact": QUEUE, "field": "checks.recordsWithMissingAuthorityFile"},
    # printed by the generated §15 block, so the number has a home and a field
    {"id": "twins-pairs-above-threshold",
     "pattern": r"Пар выше порога: \*\*(?P<n>[\d\s\u2009]+)\*\*",
     "artefact": TWINS, "field": "totals.pairs"},
    {"id": "repairs-applied",
     "pattern": r"(?P<n>\d+) склеек «слово\+число\+слово» восстановлены",
     "artefact": REPAIRS, "field": "totals.repairedTokens"},
    {"id": "repairs-blocked",
     "pattern": r"(?P<n>\d+) остаются под квитанциями",
     "artefact": REPAIRS, "field": "totals.blockedTokens"},
]


def prose_audit(text: str, root: Path) -> list[dict]:
    findings = []
    for claim in PROSE_CLAIMS:
        entry = {"id": claim["id"], "artefact": claim["artefact"], "field": claim["field"],
                 "claimed": None, "actual": None, "line": None,
                 "supersededBy": claim.get("supersededBy")}
        actual, error = resolve(root, claim["artefact"], claim["field"])
        entry["actual"] = actual
        matches = list(re.finditer(claim["pattern"], text))
        if error:
            entry["state"] = "source-missing"
        elif not matches:
            entry["state"] = "anchor-missing"
        elif len({normalize(m.group("n")) for m in matches}) > 1:
            # Two copies of the sentence with two different numbers: which one is the claim?
            # The same number repeated is one claim stated twice, and the table path has
            # always read it that way - the two paths disagreed.
            entry["state"] = "anchor-ambiguous"
            entry["line"] = text[: matches[0].start()].count("\n") + 1
        else:
            match = matches[0]
            entry["claimed"] = normalize(match.group("n"))
            entry["line"] = text[: match.start()].count("\n") + 1
            if entry["claimed"] == actual:
                entry["state"] = "match"
            elif claim.get("supersededBy"):
                heading = "## " + claim["supersededBy"].lstrip("§") + "."
                position = text.find(heading)
                if position == -1 or position < match.start():
                    entry["state"] = "superseded-target-missing"
                else:
                    entry["state"] = "superseded"
            else:
                entry["state"] = "stale"
        findings.append(entry)
    return findings



LINKS_BEGIN = "<!-- links-slice:begin -->"
LINKS_END = "<!-- links-slice:end -->"
LINK_ROWS = [
    ("Markdown-файлов", "scope.markdownFiles"),
    # Labels must be unique in the whole document: §13 already has a row called `external`
    # (signatures), and a second one with a different value would be ambiguous, not a claim.
    ("ссылок `resolves`", "totals.byState.resolves"),
    ("ссылок `external`", "totals.byState.external"),
    ("ссылок `missing`", "totals.byState.missing"),
    ("ссылок `outside`", "totals.byState.outside"),
    ("ссылок `unqualified`", "totals.byState.unqualified"),
    ("ссылок `missing-anchor`", "totals.byState.missing-anchor"),
    ("ссылок с фрагментом (`total`)", "totals.fragments.total"),
    ("из них внутристраничных", "totals.fragments.inPage"),
    ("из них на другой файл", "totals.fragments.crossFile"),
    ("фрагментов резолвится", "totals.fragments.resolved"),
    ("дефектов разобрано (`explained`)", "totals.explained"),
    ("дефектов необъяснённых (`unexplained`)", "totals.unexplained"),
]


def _pick(data: dict, field: str):
    node = data
    for part in field.split("."):
        node = node.get(part, {}) if isinstance(node, dict) else None
    return node


def render_links_table(links: dict) -> str:
    lines = [LINKS_BEGIN, "| Показатель ссылок | Значение |", "|---|---:|"]
    for label, field in LINK_ROWS:
        value = _pick(links, field)
        if isinstance(value, int):
            lines.append(f"| {label} | {fmt(value)} |")
    lines.append(LINKS_END)
    return "\n".join(lines)


TWINS_BEGIN = "<!-- twins-states:begin -->"
TWINS_END = "<!-- twins-states:end -->"
TWINS_STATES = [
    ("identical-text", "дословно один текст (байты тоже совпадают)"),
    ("near-identical", "почти дословно: один текст вложен в другой"),
    ("superset", "надмножество: дополнение сохранило базу"),
    ("shared-text", "общие блоки и линии версий, не копии"),
]


def render_twins_table(twins: dict) -> str:
    by_state = _pick(twins, "totals.byState") or {}
    lines = [TWINS_BEGIN, "| Показатель | Значение |", "|---|---:|"]
    for label, field in (("сравнено документов", "scope.documentsCompared"),
                         ("документов в корпусе", "scope.markdownFiles")):
        value = _pick(twins, field)
        if isinstance(value, int):
            lines.append(f"| {label} | {fmt(value)} |")
    lines += ["", "| Состояние | Пар | Что это |", "|---|---:|---|"]
    for state, description in TWINS_STATES:
        if state in by_state:
            lines.append(f"| `{state}` | {fmt(by_state[state])} | {description} |")
    for state in sorted(set(by_state) - {s for s, _ in TWINS_STATES}):
        lines.append(f"| `{state}` | {fmt(by_state[state])} | — |")
    # The pairs that are not merely shared text are named, with the measured overlap:
    # the earlier hand-written table carried one of these details and lost the rest.
    named = [f for f in twins.get("findings", []) if f.get("state") != "shared-text"]
    if named:
        lines += ["", "| Пара | Состояние | Перекрытие |", "|---|---|---:|"]
        for item in sorted(named, key=lambda f: (f.get("state", ""), f.get("a", ""))):
            overlap = item.get("overlap")
            shown = f"{overlap:.3f}" if isinstance(overlap, (int, float)) else "—"
            lines.append(f"| `{item.get('a', '')}` ↔ `{item.get('b', '')}` | `{item.get('state', '')}` | {shown} |")
    lines += ["", f"Пар выше порога: **{fmt(_pick(twins, 'totals.pairs') or 0)}**."]
    lines.append(TWINS_END)
    return "\n".join(lines)


STAMPS_BEGIN = "<!-- stamps-states:begin -->"
STAMPS_END = "<!-- stamps-states:end -->"
STAMPS_STATES = [
    ("current", "`current` — последний коммит в тот же день"),
    ("edited-after-stamp", "`edited-after-stamp` — файл менялся после своей даты"),
    ("stamp-ahead-of-history", "`stamp-ahead-of-history` — дата позже любого коммита"),
    ("stamp-in-future", "`stamp-in-future` — дата позже сегодняшней (невозможна)"),
]


def render_stamps_table(stamps: dict) -> str:
    """States and the documents behind the interesting one, both read from the report."""
    by_state = _pick(stamps, "totals.byState") or {}
    lines = [STAMPS_BEGIN, "| Показатель | Значение |", "|---|---:|"]
    for label, field in (("документов со своей датой", "totals.stamped"),
                         ("документов в корпусе", "scope.markdownFiles")):
        value = _pick(stamps, field)
        if isinstance(value, int):
            lines.append(f"| {label} | {fmt(value)} |")
    lines += ["", "| Состояние | Документов |", "|---|---:|"]
    for state, description in STAMPS_STATES:
        lines.append(f"| {description} | {fmt(by_state.get(state, 0))} |")
    rows = [f for f in stamps.get("findings", []) if f.get("state") == "edited-after-stamp"]
    lines += ["", "**Отредактированы после своей даты** (с темой последнего коммита как уликой):",
              "", "| Документ | Дата в тексте | Последний коммит | Что пришло позже |",
              "|---|---|---|---|"]
    for item in sorted(rows, key=lambda f: f.get("file", "")):
        subject = (item.get("lastSubject") or "").strip()
        lines.append(
            f"| `{item.get('file', '')}` | {item.get('stamp', '')} | {item.get('lastCommit', '')} "
            f"| *{subject}* |")
    lines.append(STAMPS_END)
    return "\n".join(lines)


PINNED_BEGIN = "<!-- pinned-locators:begin -->"
PINNED_END = "<!-- pinned-locators:end -->"
PINNED_ROWS = [
    ("локаторов", "totals.locators"),
    ("заявленных SHA-256 совпало", "totals.match"),
    ("расхождений", "totals.mismatch"),
    ("без заявки", "totals.unclaimed"),
    ("недоступных", "totals.unavailable"),
    # one verified object can be cited in several documents; the first version of this
    # report kept only the first site, so the register's "7 files" had no field at all
    ("цитирований (мест)", "totals.citations"),
    ("файлов с цитированием", "totals.citationFiles"),
]


def render_pinned_table(pinned: dict) -> str:
    lines = [PINNED_BEGIN, "| Показатель | Значение |", "|---|---:|"]
    for label, field in PINNED_ROWS:
        value = _pick(pinned, field)
        if isinstance(value, int):
            lines.append(f"| {label} | {fmt(value)} |")
    lines += ["", "| Репозиторий | Коммит | Путь | Заявка | Байт (факт) | SHA-256 (факт) | Состояние |",
              "|---|---|---|---|---:|---|---|"]
    for item in pinned.get("locators", []):
        claim = "да" if (item.get("claimedSha256") or item.get("claimedBytes") is not None) else "—"
        digest = item.get("fetchedSha256") or "—"
        short = digest[:16] + "…" if digest != "—" else digest
        lines.append(
            f"| `{item.get('repo', '')}` | `{str(item.get('commit', ''))[:8]}` "
            f"| `{item.get('path', '')}` | {claim} | {item.get('fetchedBytes') or '—'} "
            f"| `{short}` | {item.get('state', '')} |")
    lines.append(PINNED_END)
    return "\n".join(lines)


def replace_between(text: str, begin: str, end: str, block: str) -> tuple[str, bool]:
    start, stop = text.find(begin), text.find(end)
    if start == -1 or stop == -1 or stop < start:
        return text, False
    return text[:start] + block + text[stop + len(end):], True


# name -> (marker pair, artefact, renderer). Adding a generated block here is the whole
# change needed for it to be written and checked; nothing else enumerates them.
SLICES = {
    "inventory": ((SLICE_BEGIN, SLICE_END), INVENTORY, render_slice_table),
    "corpus": ((CORPUS_BEGIN, CORPUS_END), INVENTORY, render_corpus_table),
    "links": ((LINKS_BEGIN, LINKS_END), LINKS, render_links_table),
    "pinned": ((PINNED_BEGIN, PINNED_END), PINNED, render_pinned_table),
    "twins": ((TWINS_BEGIN, TWINS_END), TWINS, render_twins_table),
    "stamps": ((STAMPS_BEGIN, STAMPS_END), STAMPS, render_stamps_table),
}


# Where each generated block lives in the register, for messages and reports. The gate
# iterates SLICES rather than this map, so adding a block cannot silently escape it.
SLICE_LABELS = {
    "inventory": "§2 машинный срез",
    "corpus": "§2.1 таблица по корпусам",
    "links": "§8 таблица ссылок",
    "pinned": "§11 таблица локаторов",
    "twins": "§15 таблица состояний дублей",
    "stamps": "§16 таблица состояний дат",
}


def slice_states(text: str, root: Path) -> dict[str, str]:
    states = {}
    for name, ((begin, end), artefact, renderer) in SLICES.items():
        path = root / artefact
        if not path.exists():
            states[name] = "source-missing"
            continue
        expected = renderer(json.loads(path.read_text(encoding="utf-8")))
        updated, found = replace_between(text, begin, end, expected)
        states[name] = "match" if found and updated == text else ("anchor-missing" if not found else "stale")
    return states


TABLE_ROW = re.compile(r"^\|\s*(?P<label>[^|]+?)\s*\|\s*(?P<value>-?[\d\s\u2009\u00a0]{1,12})\s*\|")
NUMBER_SPACES = " \u2009\u00a0"


def normalize(value: str) -> int | None:
    cleaned = "".join(ch for ch in value if ch not in NUMBER_SPACES)
    return int(cleaned) if cleaned.lstrip("-").isdigit() else None


def resolve(root: Path, artefact: str, field: str) -> tuple[int | None, str | None]:
    path = root / artefact
    if field.startswith("len:"):
        if not path.exists():
            return None, "source-missing"
        data = json.loads(path.read_text(encoding="utf-8"))
        key = field.split(":", 1)[1]
        if not isinstance(data.get(key), list):
            return None, "source-missing"
        return len(data[key]), None
    if not path.exists():
        return None, "source-missing"
    node = json.loads(path.read_text(encoding="utf-8"))
    for part in field.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return None, "source-missing"
    return (node, None) if isinstance(node, int) else (None, "source-missing")


def rows(text: str) -> dict[str, list[tuple[int, int]]]:
    """label -> [(printed value, line number)], every table row whose second cell is a number."""
    found: dict[str, list[tuple[int, int]]] = {}
    for lineno, line in enumerate(text.splitlines(), 1):
        match = TABLE_ROW.match(line.strip())
        if not match:
            continue
        value = normalize(match.group("value"))
        if value is None:
            continue
        found.setdefault(match.group("label").strip(), []).append((value, lineno))
    return found


def audit(root: Path, register: Path | None = None) -> dict:
    register = register or root / REGISTER
    text = register.read_text(encoding="utf-8")
    inventory_path = root / INVENTORY
    states = slice_states(text, root)
    printed = rows(text)
    prose = prose_audit(text, root)
    findings = []
    totals: dict[str, int] = {}
    for label, artefact, field in CLAIMS:
        actual, error = resolve(root, artefact, field)
        entry = {"label": label, "artefact": artefact, "field": field,
                 "claimed": None, "actual": actual, "line": None}
        hits = printed.get(label, [])
        if error:
            state = "source-missing"
        elif not hits:
            state = "anchor-missing"
        elif len({value for value, _ in hits}) > 1:
            # The same label printed with two different numbers: which one is the claim?
            entry["claimed"], entry["line"] = hits[0]
            state = "anchor-ambiguous"
        else:
            entry["claimed"], entry["line"] = hits[0]
            state = "match" if entry["claimed"] == actual else "stale"
        entry["state"] = state
        totals[state] = totals.get(state, 0) + 1
        findings.append(entry)
    for entry in prose:
        totals[entry["state"]] = totals.get(entry["state"], 0) + 1
        findings.append({**entry, "label": entry["id"]})
    return {
        "schemaVersion": SCHEMA_VERSION,
        "authorityId": AUTHORITY_ID,
        "register": register.relative_to(root).as_posix() if register.is_relative_to(root) else str(register),
        "scope": {"declaredClaims": len(CLAIMS) + len(PROSE_CLAIMS), "proseClaims": len(PROSE_CLAIMS),
                  "numericTableRows": sum(len(v) for v in printed.values())},
        "totals": totals,
        "sliceStates": states,
        "findings": findings,
    }


def summary(report: dict) -> str:
    totals = report["totals"]
    lines = [f"Заявленных счётчиков: {report['scope']['declaredClaims']} — " +
             ", ".join(f"{k}={v}" for k, v in sorted(totals.items())),
             *[f"Таблица {SLICE_LABELS.get(name, name)}: {state}"
               for name, state in report["sliceStates"].items()]]
    for finding in report["findings"]:
        if finding["state"] in ("match", "superseded"):
            continue
        where = f"стр.{finding['line']}" if finding["line"] else "строка не найдена"
        lines.append(f"  {finding['state']:14s} {where:16s} «{finding['label'][:52]}»: "
                     f"напечатано {finding['claimed']}, в артефакте {finding['actual']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check register counters against artefacts.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--register", default=None)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("-o", "--output", default=None)
    parser.add_argument("--write-corpus-table", action="store_true")
    parser.add_argument("--write-slice-table", action="store_true")
    parser.add_argument("--write-links-table", action="store_true")
    parser.add_argument("--write-pinned-table", action="store_true")
    parser.add_argument("--write-twins-table", action="store_true")
    parser.add_argument("--write-stamps-table", action="store_true")
    parser.add_argument("--write-all", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    register = Path(args.register) if args.register else None
    report = audit(root, register)
    if args.output:
        Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                     encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    if args.summary:
        print(summary(report))
    bad = [f for f in report["findings"] if f["state"] not in ("match", "superseded")]
    for name, state in report["sliceStates"].items():
        if state != "match":
            bad = bad + [{"state": state, "label": SLICE_LABELS.get(name, name),
                          "claimed": None, "actual": None, "line": None}]
    writes = []
    if args.write_all or args.write_corpus_table or args.write_slice_table or args.write_links_table \
            or args.write_pinned_table or args.write_twins_table or args.write_stamps_table:
        target = Path(args.register) if args.register else root / REGISTER
        text = target.read_text(encoding="utf-8")
        wanted = [name for name, flag in (("corpus", args.write_corpus_table),
                                          ("inventory", args.write_slice_table),
                                          ("links", args.write_links_table),
                                          ("pinned", args.write_pinned_table),
                                          ("twins", args.write_twins_table),
                                          ("stamps", args.write_stamps_table)) if flag]
        if args.write_all:
            wanted = list(SLICES)
        for name in wanted:
            (begin, end), artefact, renderer = SLICES[name]
            path = root / artefact
            if not path.exists():
                print(f"{artefact} missing", file=sys.stderr)
                return 1
            text, found = replace_between(text, begin, end, renderer(json.loads(path.read_text(encoding="utf-8"))))
            if not found:
                print(f"{name} markers not found", file=sys.stderr)
                return 1
            writes.append(name)
        target.write_text(text, encoding="utf-8")
        print(f"wrote {', '.join(writes)} into {target}", file=sys.stderr)
        return 0
    if args.check and bad:
        print(summary(report), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
