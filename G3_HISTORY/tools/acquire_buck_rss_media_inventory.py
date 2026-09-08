#!/usr/bin/env python3
"""Metadata-only inventory of official FBC Lindale podcast media for the 17-sermon Buck dossier.

The tool fetches the public RSS feed and stores only episode metadata:
title, publication date, episode link, enclosure URL/type/length.
It does not download sermon audio or article bodies.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import pathlib
import re
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

FEED_URL = "https://feedpress.me/fbc-lindale"
OUT = pathlib.Path(os.environ.get("G3_BUCK_RSS_OUT", "g3-buck-rss-media-inventory"))
UA = "G3-History-Research/1.0 (metadata-only; no sermon-body/audio archival)"

MANIFEST = [
    (1, "Exodus 4:10-17", "2017-03-05"),
    (2, "Exodus 5:1-9", "2017-03-26"),
    (3, "Exodus 5:10-21", "2017-04-02"),
    (4, "Ephesians 4:1-6", "2022-09-18"),
    (5, "Ephesians 5:25-33", "2022-11-20"),
    (6, "Ephesians 6:5-9", "2022-12-04"),
    (7, "Romans 4:1-12", "2023-04-30"),
    (8, "Romans 5:6-11", "2023-06-04"),
    (9, "Titus 1:1-4", "2023-06-18"),
    (10, "Titus 2:11-15", "2023-08-06"),
    (11, "Romans 7:1-6", "2024-01-07"),
    (12, "Romans 15:1-6", "2025-10-19"),
    (13, "Romans 16:25-27", "2025-12-21"),
    (14, "Joshua 1:1-9", "2026-01-18"),
    (15, "Joshua 2:1-24", "2026-02-08"),
    (16, "Joshua 3:1-17", "2026-02-15"),
    (17, "Joshua 4:1-24", "2026-03-01"),
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = text.replace("–", "-").replace("—", "-").replace(":", " ")
    text = re.sub(r"\bdr\.?\s+tom\s+buck\b", "", text, flags=re.I)
    text = re.sub(r"\b\d{1,2}/\d{1,2}/\d{4}\b", "", text)
    text = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return " ".join(text.split())


def date_iso(raw: str | None) -> str | None:
    if not raw:
        return None
    try:
        return parsedate_to_datetime(raw).date().isoformat()
    except Exception:
        return None


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(
        FEED_URL,
        headers={"User-Agent": UA, "Accept": "application/rss+xml,application/xml,text/xml,*/*"},
    )
    acquired = datetime.now(timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
            status = getattr(r, "status", 200)
            final_url = r.geturl()
            content_type = r.headers.get("content-type")
    except Exception as exc:
        receipt = {
            "acquired_at_utc": acquired,
            "feed_url": FEED_URL,
            "metadata_only": True,
            "audio_downloaded": False,
            "publication_authorized": False,
            "acquisition_result": "RSS_ACCESS_HOLD",
            "error": repr(exc),
        }
        (OUT / "ACQUISITION_RECEIPT.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
        print(json.dumps(receipt, indent=2))
        return 0

    receipt = {
        "acquired_at_utc": acquired,
        "feed_url": FEED_URL,
        "final_url": final_url,
        "http_status": status,
        "content_type": content_type,
        "feed_bytes": len(data),
        "feed_sha256": sha256_bytes(data),
        "metadata_only": True,
        "audio_downloaded": False,
        "article_bodies_stored": False,
        "publication_authorized": False,
    }

    try:
        root = ET.fromstring(data)
    except Exception as exc:
        receipt["acquisition_result"] = "RSS_PARSE_HOLD"
        receipt["parse_error"] = repr(exc)
        (OUT / "ACQUISITION_RECEIPT.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
        print(json.dumps(receipt, indent=2))
        return 0

    items = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        pub_raw = (item.findtext("pubDate") or "").strip()
        link = (item.findtext("link") or "").strip()
        guid = (item.findtext("guid") or "").strip()
        enc = item.find("enclosure")
        items.append({
            "title": title,
            "title_norm": norm(title),
            "pub_date": date_iso(pub_raw),
            "pub_date_raw": pub_raw,
            "link": link,
            "guid": guid,
            "enclosure_url": enc.get("url") if enc is not None else None,
            "enclosure_type": enc.get("type") if enc is not None else None,
            "enclosure_length": enc.get("length") if enc is not None else None,
        })

    with (OUT / "rss_items_metadata.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["title", "pub_date", "link", "guid", "enclosure_url", "enclosure_type", "enclosure_length"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in items:
            w.writerow({k: row.get(k) for k in fields})

    matches = []
    for num, title, wanted_date in MANIFEST:
        nt = norm(title)
        candidates = [x for x in items if x["title_norm"] == nt]
        if not candidates:
            candidates = [x for x in items if nt and (nt in x["title_norm"] or x["title_norm"] in nt)]
        exact_date = [x for x in candidates if x["pub_date"] == wanted_date]
        chosen = exact_date[0] if exact_date else (candidates[0] if len(candidates) == 1 else None)
        if chosen is None:
            state = "NOT_IN_CURRENT_FEED" if not candidates else "AMBIGUOUS_MATCH"
            chosen = {}
        else:
            state = "MATCHED_EXACT_DATE" if chosen.get("pub_date") == wanted_date else "MATCHED_TITLE_DATE_MISMATCH"
        matches.append({
            "item": num,
            "manifest_title": title,
            "manifest_date": wanted_date,
            "state": state,
            "feed_title": chosen.get("title"),
            "feed_date": chosen.get("pub_date"),
            "link": chosen.get("link"),
            "guid": chosen.get("guid"),
            "enclosure_url": chosen.get("enclosure_url"),
            "enclosure_type": chosen.get("enclosure_type"),
            "enclosure_length": chosen.get("enclosure_length"),
        })

    with (OUT / "dossier_media_matches.csv").open("w", encoding="utf-8", newline="") as f:
        fields = list(matches[0].keys())
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(matches)

    matched = sum(1 for x in matches if x["state"].startswith("MATCHED"))
    matched_with_enclosure = sum(
        1 for x in matches if x["state"].startswith("MATCHED") and x.get("enclosure_url")
    )
    receipt["summary"] = {
        "rss_episode_rows": len(items),
        "dossier_items": len(MANIFEST),
        "matched_items": matched,
        "matched_with_enclosure": matched_with_enclosure,
        "not_in_current_feed": sum(1 for x in matches if x["state"] == "NOT_IN_CURRENT_FEED"),
        "ambiguous": sum(1 for x in matches if x["state"] == "AMBIGUOUS_MATCH"),
    }
    receipt["acquisition_result"] = "RSS_MEDIA_LOCATOR_INVENTORY_ACQUIRED"
    (OUT / "ACQUISITION_RECEIPT.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(receipt["summary"] | {"acquisition_result": receipt["acquisition_result"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
