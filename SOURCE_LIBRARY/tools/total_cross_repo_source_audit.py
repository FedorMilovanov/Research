#!/usr/bin/env python3
"""Deterministic cross-repository source/archive audit.

The program scans fresh shallow clones of the four public project repositories,
creates machine-readable queues, and never modifies tracked source files. URL
parsing is fail-closed: malformed text is classified, not allowed to crash or be
silently rewritten by a workflow step.
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests

OWNER = "FedorMilovanov"
REPOS = ("TheLegendaryPoet", "gb-is-my-strength", "Research", "AuditRepo")
TEXT_EXTS = {
    ".md", ".mdx", ".txt", ".html", ".htm", ".xml", ".json", ".jsonl",
    ".yaml", ".yml", ".toml", ".ini", ".cfg", ".csv", ".tsv", ".js",
    ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".css", ".scss", ".astro",
    ".py", ".sh", ".ps1", ".cmd", ".bat", ".sql", ".graphql", ".svg",
}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff", ".bmp", ".avif", ".svg"}
DOC_EXTS = {".pdf", ".doc", ".docx", ".odt", ".epub", ".djvu", ".mobi"}
ARCHIVE_EXTS = {".zip", ".7z", ".rar", ".tar", ".gz", ".bz2", ".xz"}
SKIP_DIRS = {".git", "node_modules", ".next", ".astro", ".cache", ".venv", "venv", "dist", "build", "coverage"}
URL_RE = re.compile(r"https?://[^\s<>'\"`\])}]+", re.I)
ATTR_RE = re.compile(r"(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.I)
MD_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SOURCE_WORDS = re.compile(
    r"source|reference|bibliograph|provenance|rights|license|licence|research|archive|"
    r"manuscript|audit|источник|литератур|библиограф|прав[ао]|лиценз|архив|рукопис",
    re.I,
)
SOURCE_MARKER_RE = re.compile(r"источник|sources?|bibliograph|references?|примечан|сноск|литератур", re.I)
EDITORIAL_RE = re.compile(r"(^|/)(articles?|biografii|hard-texts|content|poets?|research|baptisty-rossii)(/|$)", re.I)
USER_AGENT = "TheLegendaryPoet-SourceAudit/2.0 (+https://github.com/FedorMilovanov/Research)"


@dataclass(frozen=True)
class Thresholds:
    max_new_dead: int
    max_new_missing_local: int
    max_new_publication_provenance: int


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_read(path: Path, max_bytes: int = 4_000_000) -> str | None:
    try:
        if path.stat().st_size > max_bytes:
            return None
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def normalize_url(raw: str) -> str:
    return html.unescape(raw).rstrip(".,;:!?\")'»”")


def parse_domain(url: str) -> tuple[str, str]:
    try:
        parsed = urlparse(url)
    except ValueError as exc:
        return "[invalid-url-text]", f"ValueError: {exc}"
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return "[invalid-url-text]", "missing scheme or host"
    return parsed.netloc.lower().removeprefix("www."), ""


def should_skip(path: Path, root: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.relative_to(root).parts)


def local_target_exists(source: Path, target: str, repo_root: Path) -> tuple[bool, str]:
    target = html.unescape(target.strip())
    if not target or target.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:", "#", "//")):
        return True, "external-or-anchor"
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return True, "anchor"
    candidate = repo_root / target.lstrip("/") if target.startswith("/") else source.parent / target
    candidate = candidate.resolve()
    root_resolved = repo_root.resolve()
    if candidate != root_resolved and root_resolved not in candidate.parents:
        return True, "outside-repo"
    fallbacks = [
        candidate,
        candidate.with_suffix(".html") if not candidate.suffix else candidate,
        candidate / "index.html",
        repo_root / "public" / target.lstrip("/"),
        repo_root / "src" / target.lstrip("/"),
    ]
    for item in fallbacks:
        if item.exists():
            return True, item.relative_to(repo_root).as_posix()
    return False, candidate.relative_to(repo_root).as_posix()


def provenance_nearby(path: Path, repo_root: Path) -> bool:
    names = {
        "readme.md", "sources.md", "source.md", "rights.md", "license", "license.md",
        "provenance.md", "metadata.json", "manifest.json", "credits.md", "attribution.md",
        "источники.md", "права.md",
    }
    for parent in (path.parent, *list(path.parents)[:3]):
        if parent == repo_root.parent:
            break
        try:
            for child in parent.iterdir():
                if not child.is_file():
                    continue
                low = child.name.lower()
                if low in names or SOURCE_WORDS.search(low):
                    return True
                if child.stem.lower() == path.stem.lower() and child.suffix.lower() in {".md", ".txt", ".json", ".yaml", ".yml", ".csv"}:
                    return True
        except OSError:
            continue
        if parent == repo_root:
            break
    return False


def audit_url(session: requests.Session, url: str) -> dict[str, str | int | float]:
    domain, parse_error = parse_domain(url)
    if parse_error:
        return {
            "url": url, "status": "MALFORMED", "code": 0, "final_url": "",
            "content_type": "", "seconds": 0.0, "error": parse_error,
        }
    started = time.monotonic()
    try:
        response = session.get(url, timeout=(6, 14), allow_redirects=True, stream=True)
        code = int(response.status_code)
        final_url = response.url
        content_type = response.headers.get("content-type", "")[:160]
        response.close()
        if 200 <= code < 400:
            status = "OK"
        elif code in {401, 403, 429, 451}:
            status = "RESTRICTED"
        elif code in {404, 410}:
            status = "DEAD"
        elif 500 <= code < 600:
            status = "SERVER_ERROR"
        else:
            status = "HTTP_ERROR"
        return {
            "url": url, "status": status, "code": code, "final_url": final_url,
            "content_type": content_type, "seconds": round(time.monotonic() - started, 3), "error": "",
        }
    except requests.RequestException as exc:
        return {
            "url": url, "status": "REQUEST_ERROR", "code": 0, "final_url": "",
            "content_type": "", "seconds": round(time.monotonic() - started, 3),
            "error": f"{type(exc).__name__}: {exc}"[:300],
        }


def load_baseline(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def main() -> int:
    work = Path(os.environ.get("AUDIT_WORK", "_total_audit_work")).resolve()
    out = Path(os.environ.get("AUDIT_OUT", "total-audit-output")).resolve()
    baseline_path = Path(os.environ.get("AUDIT_BASELINE", "SOURCE_LIBRARY/audit-baseline.json"))
    thresholds = Thresholds(
        max_new_dead=int(os.environ.get("MAX_NEW_DEAD", "0")),
        max_new_missing_local=int(os.environ.get("MAX_NEW_MISSING_LOCAL", "0")),
        max_new_publication_provenance=int(os.environ.get("MAX_NEW_PUBLICATION_PROVENANCE", "0")),
    )
    shutil.rmtree(work, ignore_errors=True)
    shutil.rmtree(out, ignore_errors=True)
    work.mkdir(parents=True)
    out.mkdir(parents=True)

    for repo in REPOS:
        run(["git", "clone", "--depth", "1", f"https://github.com/{OWNER}/{repo}.git", str(work / repo)])

    inventory: list[dict] = []
    url_occurrences: list[dict] = []
    malformed_urls: list[dict] = []
    missing_local: list[dict] = []
    assets_without_provenance: list[dict] = []
    source_related: list[dict] = []
    content_without_sources: list[dict] = []
    hashes: dict[str, list[dict]] = defaultdict(list)
    repo_stats: dict[str, dict] = {}
    domain_counter: Counter[str] = Counter()

    for repo in REPOS:
        root = work / repo
        stats = Counter()
        for path in root.rglob("*"):
            if not path.is_file() or should_skip(path, root):
                continue
            rel = path.relative_to(root).as_posix()
            size = path.stat().st_size
            suffix = path.suffix.lower()
            if suffix in IMAGE_EXTS:
                kind = "image"
            elif suffix in DOC_EXTS:
                kind = "document"
            elif suffix in ARCHIVE_EXTS:
                kind = "archive"
            elif suffix in TEXT_EXTS or path.name.lower() in {"license", "readme", "cname"}:
                kind = "text"
            else:
                kind = "other"
            digest = ""
            if size <= 250_000_000:
                try:
                    digest = sha256_file(path)
                except OSError:
                    digest = ""
            if digest and size >= 512:
                hashes[digest].append({"repo": repo, "path": rel, "size": size})
            inventory.append({"repo": repo, "path": rel, "size_bytes": size, "extension": suffix, "kind": kind, "sha256": digest})
            stats["files"] += 1
            stats["size_bytes"] += size
            stats[f"kind:{kind}"] += 1

            if SOURCE_WORDS.search(rel):
                source_related.append({"repo": repo, "path": rel, "size_bytes": size, "reason": "path-keyword"})
            if kind in {"image", "document", "archive"} and not provenance_nearby(path, root):
                assets_without_provenance.append({
                    "repo": repo, "path": rel, "size_bytes": size, "kind": kind,
                    "reason": "no nearby README/source/rights/license/provenance sidecar detected",
                })

            text = safe_read(path) if kind == "text" else None
            if text is None:
                continue
            stats["text_files"] += 1
            urls_here: list[str] = []
            for raw in URL_RE.findall(text):
                url = normalize_url(raw)
                domain, parse_error = parse_domain(url)
                if parse_error:
                    malformed_urls.append({"repo": repo, "path": rel, "url": url, "error": parse_error})
                    continue
                urls_here.append(url)
                domain_counter[domain] += 1
                url_occurrences.append({"repo": repo, "path": rel, "url": url, "domain": domain})
            stats["url_occurrences"] += len(urls_here)

            links = [match.group(1).strip().split()[0] for match in MD_LINK_RE.finditer(text)]
            links += [match.group(1).strip() for match in ATTR_RE.finditer(text)]
            for target in dict.fromkeys(links):
                exists, resolved = local_target_exists(path, target, root)
                if not exists:
                    missing_local.append({"repo": repo, "source_path": rel, "target": target, "resolved_candidate": resolved})

            if EDITORIAL_RE.search(rel) and suffix in {".md", ".mdx", ".html", ".astro"}:
                if not urls_here and not SOURCE_MARKER_RE.search(text):
                    content_without_sources.append({
                        "repo": repo, "path": rel, "size_bytes": size,
                        "reason": "editorial content has no URL and no source/bibliography marker",
                    })
        repo_stats[repo] = dict(stats)

    duplicate_rows: list[dict] = []
    duplicate_groups = 0
    duplicate_bytes = 0
    for digest, items in hashes.items():
        if len(items) < 2:
            continue
        duplicate_groups += 1
        duplicate_bytes += items[0]["size"] * (len(items) - 1)
        for index, item in enumerate(items, 1):
            duplicate_rows.append({"sha256": digest, "group_size": len(items), "item_index": index, **item})

    unique_urls = sorted({row["url"] for row in url_occurrences})
    audit_cap = int(os.environ.get("URL_AUDIT_CAP", "1200"))
    urls_to_test = unique_urls[:audit_cap]
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "text/html,application/json,application/pdf,*/*;q=0.8"})
    url_results: list[dict] = []
    workers = int(os.environ.get("URL_AUDIT_WORKERS", "24"))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(audit_url, session, url): url for url in urls_to_test}
        for index, future in enumerate(as_completed(futures), 1):
            url_results.append(future.result())
            if index % 50 == 0:
                print(f"audited {index}/{len(urls_to_test)} URLs", flush=True)
    for url in unique_urls[audit_cap:]:
        url_results.append({
            "url": url, "status": "NOT_TESTED_CAP", "code": 0, "final_url": "",
            "content_type": "", "seconds": 0.0, "error": "beyond audit cap",
        })
    url_results.sort(key=lambda row: str(row["url"]))

    write_csv(out / "inventory.csv", ["repo", "path", "size_bytes", "extension", "kind", "sha256"], inventory)
    write_csv(out / "url_occurrences.csv", ["repo", "path", "url", "domain"], url_occurrences)
    write_csv(out / "malformed_url_occurrences.csv", ["repo", "path", "url", "error"], malformed_urls)
    write_csv(out / "url_audit.csv", ["url", "status", "code", "final_url", "content_type", "seconds", "error"], url_results)
    write_csv(out / "missing_local_links.csv", ["repo", "source_path", "target", "resolved_candidate"], missing_local)
    write_csv(out / "duplicate_files.csv", ["sha256", "group_size", "item_index", "repo", "path", "size"], duplicate_rows)
    write_csv(out / "assets_without_provenance.csv", ["repo", "path", "size_bytes", "kind", "reason"], assets_without_provenance)
    write_csv(out / "source_related_files.csv", ["repo", "path", "size_bytes", "reason"], source_related)
    write_csv(out / "editorial_content_without_sources.csv", ["repo", "path", "size_bytes", "reason"], content_without_sources)
    (out / "all_unique_urls.txt").write_text("\n".join(unique_urls) + "\n", encoding="utf-8")
    (out / "repo_stats.json").write_text(json.dumps(repo_stats, ensure_ascii=False, indent=2), encoding="utf-8")

    status_counts = Counter(str(row["status"]) for row in url_results)
    publication_provenance = [
        row for row in assets_without_provenance
        if row["repo"] in {"TheLegendaryPoet", "gb-is-my-strength"} and str(row["path"]).startswith("public/")
    ]
    summary = {
        "repositories": len(REPOS),
        "files": len(inventory),
        "unique_urls": len(unique_urls),
        "url_status": dict(status_counts),
        "malformed_urls": len(malformed_urls),
        "missing_local": len(missing_local),
        "duplicate_groups": duplicate_groups,
        "duplicate_bytes": duplicate_bytes,
        "assets_without_provenance": len(assets_without_provenance),
        "publication_assets_without_provenance": len(publication_provenance),
        "editorial_content_without_sources": len(content_without_sources),
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Total cross-repository source/archive audit",
        "",
        "Generated from committed audit code and fresh shallow clones. The validator did not rewrite its own source.",
        "",
        "## Executive summary",
        "",
        *(f"- {key}: **{value}**" for key, value in summary.items() if key != "url_status"),
        f"- URL status: `{summary['url_status']}`",
        "",
        "## Required review queues",
        "",
        "1. `url_audit.csv`: confirm DEAD and persistent server/network failures.",
        "2. `missing_local_links.csv`: distinguish broken paths from generated routes.",
        "3. `assets_without_provenance.csv`: resolve custody, license and publication rights.",
        "4. `editorial_content_without_sources.csv`: add source apparatus where the heuristic is correct.",
        "5. `malformed_url_occurrences.csv`: repair source text rather than patching the auditor at runtime.",
    ]
    (out / "TOTAL_CROSS_REPO_SOURCE_AUDIT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    baseline = load_baseline(baseline_path)
    baseline_dead = int(baseline.get("dead_urls", 0))
    baseline_missing = int(baseline.get("missing_local_links", 0))
    baseline_provenance = int(baseline.get("publication_assets_without_provenance", 0))
    failures: list[str] = []
    current_dead = int(status_counts.get("DEAD", 0))
    if current_dead - baseline_dead > thresholds.max_new_dead:
        failures.append(f"new DEAD URLs: {current_dead - baseline_dead} > {thresholds.max_new_dead}")
    if len(missing_local) - baseline_missing > thresholds.max_new_missing_local:
        failures.append(f"new missing local links: {len(missing_local) - baseline_missing} > {thresholds.max_new_missing_local}")
    if len(publication_provenance) - baseline_provenance > thresholds.max_new_publication_provenance:
        failures.append(
            "new publication assets without provenance: "
            f"{len(publication_provenance) - baseline_provenance} > {thresholds.max_new_publication_provenance}"
        )

    print("AUDIT_COMPLETE", json.dumps(summary, ensure_ascii=False), flush=True)
    if failures:
        for failure in failures:
            print(f"GATE_FAILURE: {failure}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
