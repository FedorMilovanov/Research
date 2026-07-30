#!/usr/bin/env python3
"""Total cross-repository source/archive audit for The Legendary Poet projects.

Clones the four public repositories, inventories all files, extracts and checks URLs,
finds missing local references, duplicate binaries, source-related documentation,
and assets that appear to lack nearby provenance/rights metadata.
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
from pathlib import Path
from urllib.parse import urlparse, unquote

try:
    import requests
except ImportError:
    requests = None

REPOS = [
    "TheLegendaryPoet",
    "gb-is-my-strength",
    "Research",
    "AuditRepo",
]
OWNER = "FedorMilovanov"

TEXT_EXTS = {
    ".md", ".mdx", ".txt", ".html", ".htm", ".xml", ".json", ".jsonl",
    ".yaml", ".yml", ".toml", ".ini", ".cfg", ".csv", ".tsv", ".js",
    ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".css", ".scss", ".astro",
    ".py", ".sh", ".ps1", ".cmd", ".bat", ".sql", ".graphql", ".svg",
}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff", ".bmp", ".avif", ".svg"}
DOC_EXTS = {".pdf", ".doc", ".docx", ".odt", ".epub", ".djvu", ".mobi"}
BINARY_ARCHIVE_EXTS = {".zip", ".7z", ".rar", ".tar", ".gz", ".bz2", ".xz"}
SKIP_DIRS = {".git", "node_modules", ".next", ".astro", ".cache", ".venv", "venv", "dist", "build", "coverage"}
SOURCE_WORDS = re.compile(
    r"source|sources|reference|references|bibliograph|provenance|rights|license|licence|"
    r"research|archive|manuscript|audit|источник|литератур|библиограф|прав[ао]|лиценз|архив|рукопис",
    re.I,
)
URL_RE = re.compile(r"https?://[^\s<>'\"`\])}]+", re.I)
ATTR_RE = re.compile(r"(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.I)
MD_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SOURCE_MARKER_RE = re.compile(r"источник|sources?|bibliograph|references?|примечан|сноск|литератур", re.I)


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_read(path: Path, max_bytes: int = 4_000_000) -> str | None:
    try:
        if path.stat().st_size > max_bytes:
            return None
        return path.read_text("utf-8", errors="replace")
    except Exception:
        return None


def normalize_url(raw: str) -> str:
    return html.unescape(raw).rstrip(".,;:!?\")'\u00bb\u201d")


def should_skip(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    return any(part in SKIP_DIRS for part in rel.parts)


def local_target_exists(source: Path, target: str, repo_root: Path) -> tuple[bool, str]:
    target = html.unescape(target.strip())
    if not target or target.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:", "#", "//")):
        return True, "external-or-anchor"
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return True, "anchor"
    target = unquote(target)
    if target.startswith("/"):
        candidate = repo_root / target.lstrip("/")
    else:
        candidate = source.parent / target
    try:
        candidate = candidate.resolve()
        repo_resolved = repo_root.resolve()
        if repo_resolved not in candidate.parents and candidate != repo_resolved:
            return True, "outside-repo"
    except Exception:
        pass
    if candidate.exists():
        return True, str(candidate.relative_to(repo_root))
    # Common static-site resolution fallbacks.
    fallbacks = [
        candidate.with_suffix(".html") if not candidate.suffix else candidate,
        candidate / "index.html",
        repo_root / "public" / target.lstrip("/"),
        repo_root / "src" / target.lstrip("/"),
    ]
    for fb in fallbacks:
        if fb.exists():
            try:
                return True, str(fb.relative_to(repo_root))
            except Exception:
                return True, str(fb)
    try:
        return False, str(candidate.relative_to(repo_root))
    except Exception:
        return False, str(candidate)


def provenance_nearby(path: Path, repo_root: Path) -> bool:
    stem = path.stem.lower()
    nearby_names = {
        "readme.md", "sources.md", "source.md", "rights.md", "license", "license.md",
        "provenance.md", "metadata.json", "manifest.json", "credits.md", "attribution.md",
        "источники.md", "права.md",
    }
    for parent in [path.parent, *list(path.parents)[:3]]:
        if parent == repo_root.parent:
            break
        try:
            for child in parent.iterdir():
                if child.is_file():
                    low = child.name.lower()
                    if low in nearby_names or SOURCE_WORDS.search(low):
                        return True
                    if child.stem.lower() == stem and child.suffix.lower() in {".md", ".txt", ".json", ".yaml", ".yml", ".csv"}:
                        return True
        except Exception:
            continue
        if parent == repo_root:
            break
    return False


def audit_url(url: str) -> dict[str, str | int | float]:
    if requests is None:
        return {"url": url, "status": "NO_REQUESTS", "code": 0, "final_url": "", "content_type": "", "seconds": 0.0, "error": "requests unavailable"}
    headers = {"User-Agent": "TheLegendaryPoet-SourceAudit/2026-07-30 (+https://github.com/FedorMilovanov/Research)"}
    started = time.monotonic()
    try:
        r = requests.get(url, headers=headers, timeout=(6, 14), allow_redirects=True, stream=True)
        elapsed = round(time.monotonic() - started, 3)
        code = int(r.status_code)
        ctype = r.headers.get("content-type", "")[:160]
        final = r.url
        r.close()
        if 200 <= code < 400:
            status = "OK"
        elif code in {401, 403, 429}:
            status = "RESTRICTED"
        elif code == 404:
            status = "DEAD"
        elif 500 <= code < 600:
            status = "SERVER_ERROR"
        else:
            status = "HTTP_ERROR"
        return {"url": url, "status": status, "code": code, "final_url": final, "content_type": ctype, "seconds": elapsed, "error": ""}
    except Exception as exc:
        return {"url": url, "status": "REQUEST_ERROR", "code": 0, "final_url": "", "content_type": "", "seconds": round(time.monotonic() - started, 3), "error": str(exc)[:300]}


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    work = Path(os.environ.get("AUDIT_WORK", "_total_audit_work")).resolve()
    out = Path(os.environ.get("AUDIT_OUT", "total-audit-output")).resolve()
    shutil.rmtree(work, ignore_errors=True)
    shutil.rmtree(out, ignore_errors=True)
    work.mkdir(parents=True)
    out.mkdir(parents=True)

    for repo in REPOS:
        run(["git", "clone", "--depth", "1", f"https://github.com/{OWNER}/{repo}.git", str(work / repo)])

    inventory: list[dict] = []
    url_occurrences: list[dict] = []
    missing_local: list[dict] = []
    assets_without_provenance: list[dict] = []
    source_related: list[dict] = []
    content_without_sources: list[dict] = []
    hashes: dict[str, list[dict]] = defaultdict(list)
    repo_stats: dict[str, dict] = {}
    domain_counter = Counter()

    for repo in REPOS:
        root = work / repo
        ext_counts = Counter()
        type_counts = Counter()
        dir_sizes = Counter()
        file_count = 0
        total_size = 0
        text_count = 0
        url_count = 0
        for path in root.rglob("*"):
            if not path.is_file() or should_skip(path, root):
                continue
            rel = path.relative_to(root).as_posix()
            size = path.stat().st_size
            suffix = path.suffix.lower()
            file_count += 1
            total_size += size
            ext_counts[suffix or "[no-ext]"] += 1
            topdir = rel.split("/", 1)[0]
            dir_sizes[topdir] += size
            if suffix in IMAGE_EXTS:
                kind = "image"
            elif suffix in DOC_EXTS:
                kind = "document"
            elif suffix in BINARY_ARCHIVE_EXTS:
                kind = "archive"
            elif suffix in TEXT_EXTS or path.name.lower() in {"license", "readme", "cname"}:
                kind = "text"
            else:
                kind = "other"
            type_counts[kind] += 1
            digest = ""
            if size <= 250_000_000:
                try:
                    digest = sha256_file(path)
                    if size >= 512:
                        hashes[digest].append({"repo": repo, "path": rel, "size": size})
                except Exception:
                    digest = ""
            inventory.append({
                "repo": repo,
                "path": rel,
                "size_bytes": size,
                "extension": suffix,
                "kind": kind,
                "sha256": digest,
            })

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
            text_count += 1
            urls_here = []
            for raw in URL_RE.findall(text):
                url = normalize_url(raw)
                if not url.startswith(("http://", "https://")):
                    continue
                urls_here.append(url)
                parsed = urlparse(url)
                domain = parsed.netloc.lower().removeprefix("www.")
                domain_counter[domain] += 1
                url_occurrences.append({"repo": repo, "path": rel, "url": url, "domain": domain})
            url_count += len(urls_here)

            links = [m.group(1).strip().split()[0] for m in MD_LINK_RE.finditer(text)]
            links += [m.group(1).strip() for m in ATTR_RE.finditer(text)]
            seen_local = set()
            for target in links:
                key = target
                if key in seen_local:
                    continue
                seen_local.add(key)
                exists, resolved = local_target_exists(path, target, root)
                if not exists:
                    missing_local.append({"repo": repo, "source_path": rel, "target": target, "resolved_candidate": resolved})

            # Editorial content with no obvious source apparatus.
            editorial_path = bool(re.search(r"(^|/)(articles?|biografii|hard-texts|content|poets?|research|baptisty-rossii)(/|$)", rel, re.I))
            if editorial_path and suffix in {".md", ".mdx", ".html", ".astro"}:
                if not urls_here and not SOURCE_MARKER_RE.search(text):
                    content_without_sources.append({
                        "repo": repo, "path": rel, "size_bytes": size,
                        "reason": "editorial content has no URL and no source/bibliography marker",
                    })

        repo_stats[repo] = {
            "files": file_count,
            "size_bytes": total_size,
            "text_files": text_count,
            "urls_occurrences": url_count,
            "extension_counts": dict(ext_counts.most_common()),
            "type_counts": dict(type_counts),
            "top_level_sizes": dict(dir_sizes.most_common()),
        }

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
    # Audit every URL up to a generous bound; preserve the remainder as NOT_TESTED.
    audit_cap = int(os.environ.get("URL_AUDIT_CAP", "1200"))
    urls_to_test = unique_urls[:audit_cap]
    url_results: list[dict] = []
    workers = int(os.environ.get("URL_AUDIT_WORKERS", "24"))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(audit_url, url): url for url in urls_to_test}
        for i, future in enumerate(as_completed(futures), 1):
            url_results.append(future.result())
            if i % 50 == 0:
                print(f"audited {i}/{len(urls_to_test)} URLs", flush=True)
    for url in unique_urls[audit_cap:]:
        url_results.append({"url": url, "status": "NOT_TESTED_CAP", "code": 0, "final_url": "", "content_type": "", "seconds": 0.0, "error": "beyond audit cap"})
    url_results.sort(key=lambda r: r["url"])

    write_csv(out / "inventory.csv", ["repo", "path", "size_bytes", "extension", "kind", "sha256"], inventory)
    write_csv(out / "url_occurrences.csv", ["repo", "path", "url", "domain"], url_occurrences)
    write_csv(out / "url_audit.csv", ["url", "status", "code", "final_url", "content_type", "seconds", "error"], url_results)
    write_csv(out / "missing_local_links.csv", ["repo", "source_path", "target", "resolved_candidate"], missing_local)
    write_csv(out / "duplicate_files.csv", ["sha256", "group_size", "item_index", "repo", "path", "size"], duplicate_rows)
    write_csv(out / "assets_without_provenance.csv", ["repo", "path", "size_bytes", "kind", "reason"], assets_without_provenance)
    write_csv(out / "source_related_files.csv", ["repo", "path", "size_bytes", "reason"], source_related)
    write_csv(out / "editorial_content_without_sources.csv", ["repo", "path", "size_bytes", "reason"], content_without_sources)
    (out / "all_unique_urls.txt").write_text("\n".join(unique_urls) + "\n", encoding="utf-8")
    (out / "repo_stats.json").write_text(json.dumps(repo_stats, ensure_ascii=False, indent=2), encoding="utf-8")

    status_counts = Counter(str(r["status"]) for r in url_results)
    source_by_repo = Counter(r["repo"] for r in source_related)
    assets_by_repo = Counter(r["repo"] for r in assets_without_provenance)
    content_gap_by_repo = Counter(r["repo"] for r in content_without_sources)
    missing_by_repo = Counter(r["repo"] for r in missing_local)

    lines = [
        "# Total cross-repository source/archive audit",
        "",
        "Generated by GitHub Actions from fresh shallow clones of all four `main` branches.",
        "",
        "## Executive summary",
        "",
        f"- repositories scanned: **{len(REPOS)}**",
        f"- files inventoried: **{len(inventory):,}**",
        f"- unique external URLs found: **{len(unique_urls):,}**",
        f"- URL occurrences: **{len(url_occurrences):,}**",
        f"- URLs live-audited: **{len(urls_to_test):,}** (cap {audit_cap:,})",
        f"- missing local link/reference candidates: **{len(missing_local):,}**",
        f"- duplicate SHA-256 groups: **{duplicate_groups:,}**",
        f"- estimated duplicate bytes beyond first copy: **{duplicate_bytes:,}**",
        f"- source/research/rights-related files: **{len(source_related):,}**",
        f"- binary assets lacking nearby provenance metadata by heuristic: **{len(assets_without_provenance):,}**",
        f"- editorial content files with no URL/source marker by heuristic: **{len(content_without_sources):,}**",
        "",
        "## Repository inventory",
        "",
        "| Repository | Files | Bytes | Text | URL occurrences | Source-related | Missing local refs | Assets w/o nearby provenance | Editorial source gaps |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for repo in REPOS:
        st = repo_stats[repo]
        lines.append(
            f"| `{repo}` | {st['files']:,} | {st['size_bytes']:,} | {st['text_files']:,} | {st['urls_occurrences']:,} | "
            f"{source_by_repo[repo]:,} | {missing_by_repo[repo]:,} | {assets_by_repo[repo]:,} | {content_gap_by_repo[repo]:,} |"
        )
    lines += ["", "## URL status", "", "| Status | Count |", "|---|---:|"]
    for status, count in status_counts.most_common():
        lines.append(f"| `{status}` | {count:,} |")
    lines += ["", "## Most referenced domains", "", "| Domain | Occurrences |", "|---|---:|"]
    for domain, count in domain_counter.most_common(40):
        lines.append(f"| `{domain}` | {count:,} |")
    lines += [
        "",
        "## Required human review queues",
        "",
        "1. `assets_without_provenance.csv`: decide whether each binary is public-domain/open-license, private study only, or must be removed/replaced.",
        "2. `editorial_content_without_sources.csv`: add bibliography/source apparatus where the heuristic is correct.",
        "3. `missing_local_links.csv`: distinguish actual broken links from runtime-generated routes.",
        "4. `url_audit.csv`: repair `DEAD`, review `RESTRICTED`, and retry temporary `REQUEST_ERROR`/`SERVER_ERROR` entries.",
        "5. `duplicate_files.csv`: remove redundant binaries only after confirming paths are not deliberate deployment copies.",
        "",
        "## Storage and publication policy",
        "",
        "- GitHub: code, manifests, URL indexes, rights/provenance ledgers, citations, checksums.",
        "- Library/Drive: large legal-to-store PDFs and original-resolution images.",
        "- Link-only: restricted viewers, archives with unclear redistribution rights, licensed manuscript photography.",
        "- Never infer that an open-access web page grants republication rights for embedded images.",
        "",
        "## Machine-readable outputs",
        "",
        "- `inventory.csv`",
        "- `repo_stats.json`",
        "- `url_occurrences.csv`",
        "- `url_audit.csv`",
        "- `all_unique_urls.txt`",
        "- `missing_local_links.csv`",
        "- `duplicate_files.csv`",
        "- `assets_without_provenance.csv`",
        "- `source_related_files.csv`",
        "- `editorial_content_without_sources.csv`",
    ]
    (out / "TOTAL_CROSS_REPO_SOURCE_AUDIT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("AUDIT_COMPLETE", json.dumps({
        "files": len(inventory), "unique_urls": len(unique_urls), "url_status": dict(status_counts),
        "missing_local": len(missing_local), "duplicate_groups": duplicate_groups,
        "assets_without_provenance": len(assets_without_provenance),
        "editorial_content_without_sources": len(content_without_sources),
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
