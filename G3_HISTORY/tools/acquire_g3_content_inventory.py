#!/usr/bin/env python3
"""Acquire a metadata-only inventory of public G3 content surfaces.

No article bodies are stored. The tool probes public sitemap and WordPress REST
metadata routes, records transport state, and emits only URL/date/title/author
metadata suitable for a reproducible corpus denominator.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import pathlib
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from urllib.parse import urljoin

import requests

BASE = "https://g3min.org/"
OUT = pathlib.Path(os.environ.get("G3_CONTENT_OUT", "g3-content-inventory"))
UA = "G3-History-Research/1.0 (metadata-only; no article-body archival)"
TIMEOUT = 25


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str) -> tuple[requests.Response | None, dict]:
    rec = {"url": url, "fetched_at_utc": datetime.now(timezone.utc).isoformat()}
    try:
        r = requests.get(url, headers={"User-Agent": UA, "Accept": "application/json,application/xml,text/xml,*/*"}, timeout=TIMEOUT)
        rec.update({
            "status": r.status_code,
            "content_type": r.headers.get("content-type"),
            "content_length_header": r.headers.get("content-length"),
            "final_url": r.url,
            "sha256": sha256_bytes(r.content),
            "bytes": len(r.content),
        })
        return r, rec
    except Exception as exc:
        rec.update({"status": None, "error": repr(exc)})
        return None, rec


def parse_sitemap_xml(data: bytes) -> tuple[str, list[dict]]:
    root = ET.fromstring(data)
    tag = root.tag.split("}")[-1]
    rows: list[dict] = []
    if tag == "sitemapindex":
        for sm in root:
            vals = {child.tag.split("}")[-1]: (child.text or "").strip() for child in sm}
            if vals.get("loc"):
                rows.append({"kind": "sitemap", "loc": vals.get("loc"), "lastmod": vals.get("lastmod")})
        return "sitemapindex", rows
    if tag == "urlset":
        for u in root:
            vals = {child.tag.split("}")[-1]: (child.text or "").strip() for child in u}
            if vals.get("loc"):
                rows.append({"kind": "url", "loc": vals.get("loc"), "lastmod": vals.get("lastmod")})
        return "urlset", rows
    return tag, rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    receipt = {
        "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
        "base": BASE,
        "metadata_only": True,
        "article_bodies_stored": False,
        "publication_authorized": False,
        "requests": [],
    }

    all_urls: dict[str, dict] = {}
    sitemap_candidates = [
        urljoin(BASE, "wp-sitemap.xml"),
        urljoin(BASE, "sitemap_index.xml"),
        urljoin(BASE, "sitemap.xml"),
    ]
    child_sitemaps: list[str] = []

    for url in sitemap_candidates:
        r, rec = fetch(url)
        receipt["requests"].append(rec)
        if r is None or r.status_code != 200:
            continue
        try:
            kind, rows = parse_sitemap_xml(r.content)
        except Exception as exc:
            rec["parse_error"] = repr(exc)
            continue
        rec["parsed_kind"] = kind
        rec["parsed_rows"] = len(rows)
        if kind == "sitemapindex":
            child_sitemaps.extend([row["loc"] for row in rows if row.get("loc")])
        elif kind == "urlset":
            for row in rows:
                all_urls[row["loc"]] = row

    # Bound child sitemap acquisition to avoid uncontrolled crawling.
    unique_children = list(dict.fromkeys(child_sitemaps))[:100]
    for url in unique_children:
        r, rec = fetch(url)
        receipt["requests"].append(rec)
        if r is None or r.status_code != 200:
            continue
        try:
            kind, rows = parse_sitemap_xml(r.content)
            rec["parsed_kind"] = kind
            rec["parsed_rows"] = len(rows)
            if kind == "urlset":
                for row in rows:
                    all_urls[row["loc"]] = row
        except Exception as exc:
            rec["parse_error"] = repr(exc)
        time.sleep(0.05)

    with (OUT / "sitemap_urls.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["kind", "loc", "lastmod"])
        w.writeheader()
        for row in sorted(all_urls.values(), key=lambda x: x.get("loc", "")):
            w.writerow({"kind": row.get("kind"), "loc": row.get("loc"), "lastmod": row.get("lastmod")})

    # WordPress REST post metadata only; no content/excerpt fields requested.
    wp_rows: list[dict] = []
    page = 1
    while page <= 100:
        url = urljoin(BASE, f"wp-json/wp/v2/posts?per_page=100&page={page}&_fields=id,date,modified,slug,link,title,author")
        r, rec = fetch(url)
        receipt["requests"].append(rec)
        if r is None:
            break
        if r.status_code in (400, 404) and page > 1:
            break
        if r.status_code != 200:
            break
        try:
            data = r.json()
        except Exception as exc:
            rec["json_error"] = repr(exc)
            break
        if not isinstance(data, list) or not data:
            break
        for item in data:
            title = item.get("title") or {}
            wp_rows.append({
                "id": item.get("id"),
                "date": item.get("date"),
                "modified": item.get("modified"),
                "slug": item.get("slug"),
                "link": item.get("link"),
                "title": title.get("rendered") if isinstance(title, dict) else title,
                "author": item.get("author"),
            })
        total_pages = r.headers.get("X-WP-TotalPages")
        rec["wp_total"] = r.headers.get("X-WP-Total")
        rec["wp_total_pages"] = total_pages
        if total_pages and page >= int(total_pages):
            break
        page += 1
        time.sleep(0.05)

    with (OUT / "wp_posts_metadata.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["id", "date", "modified", "slug", "link", "title", "author"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(wp_rows)

    receipt["summary"] = {
        "sitemap_unique_urls": len(all_urls),
        "child_sitemaps_seen": len(unique_children),
        "wp_post_rows": len(wp_rows),
    }
    if all_urls or wp_rows:
        receipt["acquisition_result"] = "METADATA_INVENTORY_ACQUIRED"
    else:
        receipt["acquisition_result"] = "PUBLIC_METADATA_ACCESS_HOLD"

    (OUT / "ACQUISITION_RECEIPT.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(receipt["summary"] | {"acquisition_result": receipt["acquisition_result"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
