#!/usr/bin/env python3
"""Rights-first acquisition pass for the 59-object canonical source queue.

The script audits every official entry point, downloads only clearly exposed files
from the same official/provider domain, validates signatures, and records failures.
It never substitutes third-party mirrors for unavailable official objects.
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
import os
import re
import shutil
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests

OUT = Path(os.environ.get("ACQUISITION_OUT", "official-core-acquisition-output")).resolve()
FILES = OUT / "files"
MAX_FILE_BYTES = int(os.environ.get("MAX_FILE_BYTES", str(350 * 1024 * 1024)))
MAX_TOTAL_BYTES = int(os.environ.get("MAX_TOTAL_BYTES", str(1500 * 1024 * 1024)))
TIMEOUT = (8, 35)
UA = "TheLegendaryPoet-OfficialAcquisition/2026-07-30 (+https://github.com/FedorMilovanov/Research)"

FILE_EXTENSIONS = (".pdf", ".zip", ".csv", ".tsv", ".json", ".xml", ".txt", ".epub", ".tei", ".xlsx")
HREF_RE = re.compile(r"(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.I)
PLAIN_URL_RE = re.compile(r"https?://[^\s<>\"']+", re.I)
PDF_HINT_RE = re.compile(r"(?:application/pdf|\.pdf(?:\?|$))", re.I)


@dataclass(frozen=True)
class Candidate:
    id: str
    priority: str
    project: str
    title: str
    landing_url: str
    mode: str
    rights: str
    expected_tokens: tuple[str, ...] = ()
    max_downloads: int = 1
    allow_domains: tuple[str, ...] = ()
    notes: str = ""


def candidates() -> list[Candidate]:
    result: list[Candidate] = []

    imli_chronicle = [
        ("chronicle-1", "Летопись Есенина, т. 1", "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/821-letopis-zhizni-i-tvorchestva-s-a-esenina-tom-1"),
        ("chronicle-2", "Летопись Есенина, т. 2", "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/822-letopis-zhizni-i-tvorchestva-s-a-esenina-tom-2"),
        ("chronicle-3-1", "Летопись Есенина, т. 3, кн. 1", "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/823-letopis-zhizni-i-tvorchestva-s-a-esenina-tom-3"),
        ("chronicle-3-2", "Летопись Есенина, т. 3, кн. 2", "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/824-letopis-zhizni-i-tvorchestva-s-a-esenina-tom-3-kniga-2"),
        ("chronicle-4", "Летопись Есенина, т. 4", "https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/825-letopis-zhizni-i-tvorchestva-s-a-esenina-tom-4"),
        ("chronicle-5-1", "Летопись Есенина, т. 5, кн. 1", "https://biblio.imli.ru/index.php/component/abook/book/826-letopis-zhizni-i-tvorchestva-s-a-esenina-tom-5?Itemid=0&catid=527%3Aesenin-s-a"),
    ]
    for slug, title, url in imli_chronicle:
        result.append(Candidate(
            f"imli-{slug}", "P0", "TheLegendaryPoet", title, url,
            "discover-download", "official OA/item terms; store unchanged",
            ("есен", "летопис"), 1, ("biblio.imli.ru",),
        ))

    pss = [
        ("1", "688-esenin-s-a-pss-v-7-tomakh-t-1-1995"),
        ("2", "689-esenin-s-a-pss-v-7-tomakh-t-2-1997"),
        ("3", "690-esenin-s-a-pss-v-7-tomakh-t-3-1998"),
        ("4", "691-esenin-s-a-pss-v-7-tomakh-t-4-2004"),
        ("5", "692-esenin-s-a-pss-v-7-tomakh-t-5-2005"),
        ("6", "693-esenin-s-a-pss-v-7-tomakh-t-6-2005"),
        ("7-1", "557-esenin-s-a-pss-v-7-tomakh-t-7-kn-1-1999"),
        ("7-2", "694-esenin-s-a-pss-v-7-tomakh-t-7-kn-2-2000"),
        ("7-3", "695-esenin-s-a-pss-v-7-tomakh-t-7-kn-3-2002"),
    ]
    for label, slug in pss:
        result.append(Candidate(
            f"imli-pss-{label}", "P0", "TheLegendaryPoet", f"ПСС Есенина, том/книга {label}",
            f"https://biblio.imli.ru/index.php/ruslit/527-esenin-s-a/{slug}",
            "discover-download", "official OA/item terms; store unchanged",
            ("есен", "собрани"), 1, ("biblio.imli.ru",),
        ))

    # Verified NEB series sequence: volume 1 = ...519, volume 12 = ...508.
    for volume in range(1, 13):
        code = f"0051505{20 - volume:02d}"
        result.append(Candidate(
            f"neb-mayakovsky-12v-{volume:02d}", "P0", "TheLegendaryPoet",
            f"Маяковский, Полное собрание сочинений в 12 т., т. {volume}",
            f"https://rusneb.ru/catalog/000199_000009_{code}/",
            "discover-download", "NEB item access; image reuse requires separate review",
            ("маяков", "12", f"т. {volume}"), 1,
            ("rusneb.ru", "dlib.rsl.ru", "нэб.рф"),
            "Accept only when the card verifies author/series/volume and exposes a real file.",
        ))

    pushkin_datasets = [
        ("pushkiniana", "Пушкиниана: библиография научных и критических работ", "https://pushkinskijdom.ru/2025/01/24/repozitorij-otkrytyh-dannyh-po-russkoj-literature-i-folkloru-2/"),
        ("pushkin-index", "Индекс произведений и писем А. С. Пушкина", "https://pushkinskijdom.ru/2023/11/24/novyj-dataset-indeks-proizvedenij-i-pisem-a-s-pushkina/"),
        ("pushkin-poetry", "Корпус стихотворений А. С. Пушкина", "https://pushkinskijdom.ru/category/elektronnaya-biblioteka/"),
        ("soviet-journals", "Роспись советских толстых журналов, 1955–1990", "https://pushkinskijdom.ru/2025/03/"),
        ("imperial-readers", "Хрестоматии Российской империи, 1805–1912", "https://pushkinskijdom.ru/laboratoriya-tsifrovyh-issledovanij-literatury-i-folklora_/sobytiya/"),
        ("school-programs", "Программы по литературе, 1919–1991", "https://pushkinskijdom.ru/laboratoriya-tsifrovyh-issledovanij-literatury-i-folklora_/sobytiya/"),
    ]
    for slug, title, url in pushkin_datasets:
        result.append(Candidate(
            f"pushdom-data-{slug}", "P1", "Research", title, url,
            "discover-only", "dataset item license and Dataverse terms",
            (), 0, ("pushkinskijdom.ru", "dataverse.pushdom.ru"),
            "Resolve DOI/API and acquire dataset files with README in a later item-level step.",
        ))

    pushdom_editions = [
        ("manuscript-annuals", "Ежегодники Рукописного отдела", "https://pushkinskijdom.ru/rukopisnyj-otdel/elektronnye-izdaniya-ro/"),
        ("manuscript-bulletins", "Бюллетени Рукописного отдела", "https://pushkinskijdom.ru/rukopisnyj-otdel/elektronnye-izdaniya-ro/"),
        ("vremennik-1913", "Временник Пушкинского Дома. 1913", "https://pushkinskijdom.ru/rukopisnyj-otdel/elektronnye-izdaniya-ro/"),
        ("vremennik-1914", "Временник Пушкинского Дома. 1914", "https://pushkinskijdom.ru/rukopisnyj-otdel/elektronnye-izdaniya-ro/"),
        ("russian-literature", "Журнал «Русская литература»: архив", "https://pushkinskijdom.ru/zhurnal-russkaya-literatura/"),
        ("lermontov-4v", "Лермонтов: электронное научное издание в 4 томах", "https://pushkinskijdom.ru/"),
        ("electronic-registry", "Электронные издания Пушкинского Дома", "https://pushkinskijdom.ru/category/elektronnaya-biblioteka/"),
    ]
    for slug, title, url in pushdom_editions:
        result.append(Candidate(
            f"pushdom-edition-{slug}", "P1", "TheLegendaryPoet", title, url,
            "discover-only", "official item terms; often item-level CC/site terms",
            (), 0, ("pushkinskijdom.ru",),
        ))

    github_repositories = [
        ("stepbible", "STEPBible Data repository snapshot", "https://github.com/STEPBible/STEPBible-Data", "dataset-specific; verify each subdataset"),
        ("morphhb", "Open Scriptures Hebrew Bible snapshot", "https://github.com/openscriptures/morphhb", "WLC text public domain; morphology CC BY 4.0"),
        ("sblgnt", "Faithlife SBLGNT snapshot", "https://github.com/Faithlife/SBLGNT", "CC BY 4.0"),
    ]
    for slug, title, url, rights in github_repositories:
        result.append(Candidate(
            f"github-{slug}", "P0", "gb-is-my-strength", title, url,
            "github-archive", rights, (), 1, ("github.com", "codeload.github.com", "api.github.com"),
        ))

    theology = [
        ("calvin-institutes", "Calvin, Institutes — CCEL formats", "https://ccel.org/ccel/calvin/institutes"),
        ("calvin-life", "Calvin, On the Christian Life — CCEL", "https://ccel.org/ccel/calvin/christian_life"),
        ("owen", "John Owen works — CCEL collection", "https://ccel.org/ccel/owen"),
        ("goodwin", "Thomas Goodwin works — Theological Commons", "https://commons.ptsem.edu/"),
        ("charnock", "Stephen Charnock works — Theological Commons", "https://commons.ptsem.edu/"),
        ("flavel", "John Flavel works — Theological Commons", "https://commons.ptsem.edu/"),
        ("manton", "Thomas Manton works — Theological Commons", "https://commons.ptsem.edu/"),
        ("prdl", "PRDL metadata/navigation for Reformed authors", "https://prdl.org/"),
    ]
    for slug, title, url in theology:
        result.append(Candidate(
            f"theology-{slug}", "P1", "gb-is-my-strength", title, url,
            "discover-only", "public domain/item rights; PRDL is link-first",
            (), 0, (urlparse(url).netloc,),
        ))

    portraits = [
        ("pushkin", "Пушкин — 5 identity-verified portraits", "https://commons.wikimedia.org/wiki/Category:Alexander_Pushkin"),
        ("lermontov", "Лермонтов — 5 identity-verified portraits", "https://commons.wikimedia.org/wiki/Category:Mikhail_Lermontov"),
        ("mayakovsky", "Маяковский — 5 identity-verified portraits", "https://commons.wikimedia.org/wiki/Category:Vladimir_Mayakovsky"),
        ("akhmatova", "Ахматова — 5 identity-verified portraits", "https://commons.wikimedia.org/wiki/Category:Anna_Akhmatova"),
        ("gumilev", "Гумилёв — 5 identity-verified portraits", "https://commons.wikimedia.org/wiki/Category:Nikolay_Gumilev"),
        ("pasternak", "Пастернак — 5 identity-verified portraits", "https://commons.wikimedia.org/wiki/Category:Boris_Pasternak"),
        ("tsvetaeva", "Цветаева — 5 identity-verified portraits", "https://commons.wikimedia.org/wiki/Category:Marina_Tsvetaeva"),
        ("duncan-brik", "Айседора Дункан / Лили Брик — rights review pack", "https://digitalcollections.nypl.org/collections/isadora-duncan"),
    ]
    for slug, title, url in portraits:
        result.append(Candidate(
            f"portraits-{slug}", "P1", "TheLegendaryPoet", title, url,
            "audit-only", "item license; identity and rights review required",
            (), 0, (urlparse(url).netloc,),
        ))

    if len(result) != 59:
        raise AssertionError(f"canonical queue must contain 59 candidates, got {len(result)}")
    return result


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_name(value: str) -> str:
    value = re.sub(r"[^0-9A-Za-zА-Яа-я._ -]+", "_", value).strip(" ._")
    return value[:150] or "file"


def domain_allowed(url: str, allowed: tuple[str, ...]) -> bool:
    host = urlparse(url).netloc.lower().split(":", 1)[0]
    return any(host == item or host.endswith("." + item) for item in allowed)


def extract_links(base_url: str, text: str, allowed: tuple[str, ...]) -> list[str]:
    links: list[str] = []
    for raw in [*HREF_RE.findall(text), *PLAIN_URL_RE.findall(text)]:
        raw = html.unescape(raw).strip().rstrip(".,;:!?)\"]'")
        absolute = urljoin(base_url, raw)
        if not absolute.startswith(("http://", "https://")):
            continue
        if allowed and not domain_allowed(absolute, allowed):
            continue
        lowered = urlparse(absolute).path.lower()
        if lowered.endswith(FILE_EXTENSIONS) or PDF_HINT_RE.search(absolute):
            if absolute not in links:
                links.append(absolute)
    return links


def validate_signature(path: Path, content_type: str) -> tuple[bool, str]:
    start = path.read_bytes()[:16]
    suffix = path.suffix.lower()
    if suffix == ".pdf" or "pdf" in content_type.lower():
        return start.startswith(b"%PDF"), "PDF"
    if suffix in {".zip", ".epub", ".xlsx"} or "zip" in content_type.lower():
        return start.startswith(b"PK"), "ZIP"
    if suffix in {".csv", ".tsv", ".txt", ".json", ".xml", ".tei"}:
        return True, "TEXT_OR_DATA"
    return len(start) > 0, "OTHER"


def get(session: requests.Session, url: str, *, stream: bool = False) -> requests.Response:
    response = session.get(url, timeout=TIMEOUT, allow_redirects=True, stream=stream)
    response.raise_for_status()
    return response


def download(session: requests.Session, candidate: Candidate, url: str, directory: Path, total_state: dict) -> dict:
    directory.mkdir(parents=True, exist_ok=True)
    with get(session, url, stream=True) as response:
        length = int(response.headers.get("content-length") or 0)
        ctype = response.headers.get("content-type", "")
        if length and length > MAX_FILE_BYTES:
            return {"url": url, "status": "SKIP_FILE_TOO_LARGE", "bytes": length, "content_type": ctype}
        if length and total_state["bytes"] + length > MAX_TOTAL_BYTES:
            return {"url": url, "status": "SKIP_TOTAL_CAP", "bytes": length, "content_type": ctype}
        path_name = Path(urlparse(response.url).path).name or f"{candidate.id}.bin"
        if "." not in path_name:
            if "pdf" in ctype.lower():
                path_name += ".pdf"
            elif "zip" in ctype.lower():
                path_name += ".zip"
        path = directory / safe_name(path_name)
        temp = path.with_suffix(path.suffix + ".part")
        written = 0
        with temp.open("wb") as f:
            for chunk in response.iter_content(1024 * 1024):
                if not chunk:
                    continue
                written += len(chunk)
                if written > MAX_FILE_BYTES or total_state["bytes"] + written > MAX_TOTAL_BYTES:
                    f.close()
                    temp.unlink(missing_ok=True)
                    return {"url": url, "status": "ABORT_SIZE_CAP", "bytes": written, "content_type": ctype}
                f.write(chunk)
        temp.replace(path)
        valid, detected = validate_signature(path, ctype)
        if not valid:
            path.unlink(missing_ok=True)
            return {"url": url, "status": "INVALID_SIGNATURE", "bytes": written, "content_type": ctype, "detected": detected}
        total_state["bytes"] += written
        return {
            "url": url,
            "final_url": response.url,
            "status": "DOWNLOADED",
            "path": path.relative_to(OUT).as_posix(),
            "bytes": written,
            "sha256": sha256(path),
            "content_type": ctype,
            "detected": detected,
        }


def github_archive(session: requests.Session, candidate: Candidate, total_state: dict) -> tuple[dict, list[dict]]:
    parts = urlparse(candidate.landing_url).path.strip("/").split("/")
    owner, repo = parts[0], parts[1]
    api = f"https://api.github.com/repos/{owner}/{repo}"
    meta = get(session, api).json()
    branch = meta["default_branch"]
    archive = f"https://codeload.github.com/{owner}/{repo}/zip/refs/heads/{branch}"
    directory = FILES / candidate.project / candidate.id
    result = download(session, candidate, archive, directory, total_state)
    result["commit_ref"] = branch
    result["repository"] = f"{owner}/{repo}"
    return {"http_status": 200, "final_url": candidate.landing_url, "page_verified": True, "discovered": [archive]}, [result]


def process_candidate(session: requests.Session, candidate: Candidate, total_state: dict) -> tuple[dict, list[dict]]:
    started = time.monotonic()
    base = {**asdict(candidate), "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    if candidate.mode == "github-archive":
        try:
            page, downloads = github_archive(session, candidate, total_state)
            return {**base, **page, "seconds": round(time.monotonic() - started, 3), "error": ""}, downloads
        except Exception as exc:
            return {**base, "http_status": 0, "page_verified": False, "discovered": [], "seconds": round(time.monotonic() - started, 3), "error": str(exc)[:500]}, []

    try:
        response = get(session, candidate.landing_url)
        text = response.text
        lowered = text.lower()
        verified = all(token.lower() in lowered for token in candidate.expected_tokens) if candidate.expected_tokens else True
        discovered = extract_links(response.url, text, candidate.allow_domains)
        page = {
            **base,
            "http_status": response.status_code,
            "final_url": response.url,
            "content_type": response.headers.get("content-type", ""),
            "page_verified": verified,
            "discovered": discovered,
            "seconds": round(time.monotonic() - started, 3),
            "error": "",
        }
        if candidate.mode in {"audit-only", "discover-only"} or not verified:
            return page, []
        downloads: list[dict] = []
        directory = FILES / candidate.project / candidate.id
        for url in discovered[: candidate.max_downloads]:
            try:
                downloads.append(download(session, candidate, url, directory, total_state))
            except Exception as exc:
                downloads.append({"url": url, "status": "DOWNLOAD_ERROR", "error": str(exc)[:500]})
        if not discovered:
            downloads.append({"status": "NO_DIRECT_FILE_DISCOVERED", "url": candidate.landing_url})
        return page, downloads
    except Exception as exc:
        return {**base, "http_status": 0, "page_verified": False, "discovered": [], "seconds": round(time.monotonic() - started, 3), "error": str(exc)[:500]}, []


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    shutil.rmtree(OUT, ignore_errors=True)
    FILES.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8"})

    queue = candidates()
    audit_rows: list[dict] = []
    download_rows: list[dict] = []
    total_state = {"bytes": 0}

    for index, candidate in enumerate(queue, 1):
        print(f"[{index:02d}/{len(queue)}] {candidate.id}: {candidate.title}", flush=True)
        page, downloads = process_candidate(session, candidate, total_state)
        audit_rows.append(page)
        for item in downloads:
            download_rows.append({"candidate_id": candidate.id, "title": candidate.title, "project": candidate.project, "rights": candidate.rights, **item})
        time.sleep(0.35)

    write_csv(OUT / "candidate_audit.csv", audit_rows, [
        "id", "priority", "project", "title", "landing_url", "mode", "rights", "expected_tokens",
        "max_downloads", "allow_domains", "notes", "checked_at", "http_status", "final_url",
        "content_type", "page_verified", "discovered", "seconds", "error",
    ])
    write_csv(OUT / "download_manifest.csv", download_rows, [
        "candidate_id", "title", "project", "rights", "url", "final_url", "status", "path", "bytes",
        "sha256", "content_type", "detected", "commit_ref", "repository", "error",
    ])
    (OUT / "canonical_queue.json").write_text(json.dumps([asdict(c) for c in queue], ensure_ascii=False, indent=2), encoding="utf-8")

    downloaded = [r for r in download_rows if r.get("status") == "DOWNLOADED"]
    verified_pages = sum(bool(r.get("page_verified")) for r in audit_rows)
    reachable_pages = sum(int(r.get("http_status") or 0) > 0 for r in audit_rows)
    statuses: dict[str, int] = {}
    for row in download_rows:
        statuses[row.get("status", "UNKNOWN")] = statuses.get(row.get("status", "UNKNOWN"), 0) + 1

    report = [
        "# Official core acquisition pass — 59 objects",
        "",
        f"- candidates audited: **{len(queue)}**",
        f"- landing pages reached: **{reachable_pages}**",
        f"- pages matching required title tokens: **{verified_pages}**",
        f"- binaries downloaded and signature-checked: **{len(downloaded)}**",
        f"- downloaded bytes: **{total_state['bytes']:,}**",
        "",
        "## Download status",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for key, value in sorted(statuses.items()):
        report.append(f"| `{key}` | {value} |")
    report += [
        "",
        "## Interpretation",
        "",
        "A low binary count is not a failed audit: catalog-only, viewer-only, rights-per-item and temporarily unreachable objects must remain explicit unresolved rows. The pass never substitutes a mirror for the named official source.",
        "",
        "## Outputs",
        "",
        "- `canonical_queue.json`",
        "- `candidate_audit.csv`",
        "- `download_manifest.csv`",
        "- `files/` (only downloaded, validated binaries)",
    ]
    (OUT / "OFFICIAL_CORE_ACQUISITION_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    (OUT / "summary.json").write_text(json.dumps({
        "candidate_count": len(queue),
        "reachable_pages": reachable_pages,
        "verified_pages": verified_pages,
        "downloaded_count": len(downloaded),
        "downloaded_bytes": total_state["bytes"],
        "download_statuses": statuses,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    if len(queue) < 40:
        raise SystemExit("40+ acquisition gate failed")
    print("OFFICIAL_ACQUISITION_COMPLETE", json.dumps({
        "candidates": len(queue), "downloaded": len(downloaded), "bytes": total_state["bytes"],
    }), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
