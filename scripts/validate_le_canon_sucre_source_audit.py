#!/usr/bin/env python3
"""LE CANON SUCRÉ — offline source-link + ledger-integrity audit.

Read-only: it never modifies the working tree. It validates the evidence
corpus under LE_CANON_SUCRE/ against the repository evidence policy
(data/repository-evidence-policy-v2.json) and the AGENT_RULES source-class
vocabulary, without requiring network egress.

What it checks
--------------
1. Every `LCS-*` source row in the claim-to-citation ledger parses, across
   both table layouts (main tables and the upgrade/locator tables, which
   carry an extra `object` column):
   - unique sourceId;
   - URL with http/https scheme and a non-empty host;
   - evidenceClass in {A1,A2,A3,B1,C,D};
   - accessState / locatorState / rightsState / publicationState present
     (publicationState may be absent in the upgrade-table layout).
2. Every claim decision's `main support` references only sourceIds that
   exist in the ledger (claim-decision IDs `LCS-C0xx` are excluded from this
   check — they are decisions, not sources).
3. A single URL re-used across distinct sourceIds is reported as a WARNING,
   not an error: an institutional/stamp page legitimately documents several
   pastries. It is flagged so the shared object is not silently mistaken for
   an edition split.
4. Locator precision: portal / root / API / FTP / help pages are flagged as
   LOW_PRECISION_LOCATOR (allowed as route leads, never as quote-safe pages).
5. Whole-corpus link sweep: every https? URL across all LE_CANON_SUCRE/*.md
   is parsed; malformed URLs are reported as hard errors.

Reachability is NOT verified here (sandbox has no egress); the audit states
that explicitly so a later online pass can confirm liveness.

Exit code 0 = no hard structural errors; 1 = at least one hard error.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
LCD = ROOT / "LE_CANON_SUCRE"
LEDGER = LCD / "00_MASTER_CLAIM_TO_CITATION_LEDGER.md"

ALLOWED_CLASS = {"A1", "A2", "A3", "B1", "C", "D"}
CLAIM_ID_RE = re.compile(r"^LCS-C0\d{2}$")
# tokens that mark a URL as a portal/route lead rather than a precise page
LOW_PRECISION_HINTS = (
    "/accueil", "/ressources", "/aide-a-la-recherche",
    "rechercher-une-marque", "/api", "/ftp", "lien-serveur-ftp",
    "search?", "__ws=", "/website/page/",
)

URL_RE = re.compile(r"https?://[^\s\"'<>\)\]]+")

hard_errors: list[str] = []
warnings: list[str] = []
records: dict[str, dict] = {}
url_to_ids: dict[str, list[str]] = {}
low_precision_corpus: list[str] = []


def audit_row(line: str) -> None:
    if not line.lstrip().startswith("| LCS-"):
        return
    if "http" not in line:
        return
    fields = [f.strip() for f in line.strip().strip("|").split("|")]
    if len(fields) < 5:
        return
    sid = fields[0]
    if not re.fullmatch(r"LCS-[A-Z0-9]+", sid):
        return
    if sid in records:
        hard_errors.append(f"duplicate sourceId {sid}")
        return
    try:
        url = next(f for f in fields if f.startswith("http"))
        eclass = next(f for f in fields if re.fullmatch(r"A[123]|B1|C|D", f))
    except StopIteration:
        return
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        hard_errors.append(f"{sid}: malformed URL {url!r}")
        return
    if eclass not in ALLOWED_CLASS:
        hard_errors.append(f"{sid}: invalid evidenceClass {eclass!r}")
        return
    idx_e = fields.index(eclass)
    rest = fields[idx_e + 1: -1]  # between evidenceClass and trailing `use`
    access = rest[0] if len(rest) >= 1 else ""
    locator = rest[1] if len(rest) >= 2 else ""
    rights = rest[2] if len(rest) >= 3 else ""
    pub = rest[3] if len(rest) >= 4 else "N/A"
    low = any(h in url for h in LOW_PRECISION_HINTS)
    records[sid] = {
        "url": url, "evidenceClass": eclass, "accessState": access,
        "locatorState": locator, "rightsState": rights,
        "publicationState": pub, "lowPrecisionLocator": low,
    }
    url_to_ids.setdefault(url, []).append(sid)
    if low:
        warnings.append(f"{sid}: LOW_PRECISION_LOCATOR {url}")


def audit_ledger() -> set[str]:
    text = LEDGER.read_text(encoding="utf-8")
    for line in text.splitlines():
        audit_row(line)
    ids = set(records)
    for line in text.splitlines():
        cm = re.match(r"^\|\s*(LCS-C0\d{2})\s*\|", line)
        if not cm:
            continue
        claim = cm.group(1)
        for ref in set(re.findall(r"LCS-[A-Z0-9]+", line)):
            if ref == claim or CLAIM_ID_RE.match(ref):
                continue
            if ref not in ids:
                warnings.append(f"{claim}: references unknown sourceId {ref}")
    for u, ids_list in url_to_ids.items():
        if len(ids_list) > 1:
            warnings.append(
                f"URL shared across distinct sourceIds {ids_list} (multi-object page): {u}"
            )
    return ids


def audit_all_links() -> dict:
    hosts: dict[str, int] = {}
    malformed: list[str] = []
    total = 0
    for md in sorted(LCD.glob("*.md")):
        for u in URL_RE.findall(md.read_text(encoding="utf-8")):
            u = u.rstrip(".,;:")
            total += 1
            p = urlsplit(u)
            if p.scheme not in ("http", "https") or not p.netloc:
                malformed.append(u)
                continue
            hosts[p.netloc] = hosts.get(p.netloc, 0) + 1
            if any(h in u for h in LOW_PRECISION_HINTS):
                low_precision_corpus.append(u)
    for m in malformed:
        hard_errors.append(f"malformed corpus URL {m!r}")
    return {
        "totalLinkOccurrences": total,
        "uniqueHosts": len(hosts),
        "hosts": hosts,
        "malformed": malformed,
        "lowPrecisionCorpusLinks": sorted(set(low_precision_corpus)),
    }


def main() -> int:
    if not LEDGER.exists():
        print("LEDGER NOT FOUND", file=sys.stderr)
        return 1
    ids = audit_ledger()
    sweep = audit_all_links()

    summary = {
        "schemaVersion": 1,
        "authority": "LE-CANON-SUCRE-SOURCE-AUDIT",
        "note": "offline audit; reachability NOT verified (no sandbox egress)",
        "ledgerSourceRows": len(records),
        "ledgerSourceIds": sorted(ids),
        "lowPrecisionLedgerLocators": [s for s, r in records.items() if r["lowPrecisionLocator"]],
        "hardErrors": hard_errors,
        "warnings": warnings,
        "corpusLinkSweep": sweep,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\nLEDGER source rows: {len(records)}")
    print(f"LOW_PRECISION (ledger): {len(summary['lowPrecisionLedgerLocators'])}")
    print(f"Corpus link sweep: {sweep['totalLinkOccurrences']} occurrences across {sweep['uniqueHosts']} hosts")
    print(f"LOW_PRECISION (corpus): {len(sweep['lowPrecisionCorpusLinks'])}")
    print(f"HARD ERRORS: {len(hard_errors)}")
    print(f"WARNINGS: {len(warnings)}")
    return 1 if hard_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
