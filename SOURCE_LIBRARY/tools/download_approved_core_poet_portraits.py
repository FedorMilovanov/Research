#!/usr/bin/env python3
"""Download the single canonical 45-record poet portrait allowlist.

The downloader does not contain a second selection list. It reads
`data/core-poet-portraits-allowlist-v2.json`, validates the human review contract,
re-fetches current Commons rights metadata, downloads original bytes unchanged,
and enforces exactly five distinct images for each of nine poets.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
ALLOWLIST_PATH = ROOT / "data/core-poet-portraits-allowlist-v2.json"
API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "TheLegendaryPoet-ApprovedCorePortraits/2.0 (+https://github.com/FedorMilovanov/Research)"
OPEN_LICENSE_PATTERNS = (
    "public domain", "pd-", "cc0", "cc by ", "cc-by-", "cc by-sa", "cc-by-sa",
    "creative commons attribution",
)
EXCLUDED_LICENSE_PATTERNS = (
    "fair use", "copyrighted", "noncommercial", "no derivatives", "all rights reserved",
)
EXT_FIELDS = "|".join([
    "LicenseShortName", "UsageTerms", "AttributionRequired", "Artist", "Credit",
    "Source", "DateTimeOriginal", "DateTime", "ImageDescription", "Categories",
])


@dataclass
class Record:
    number: int
    poet_key: str
    poet_name: str
    file_title: str
    review_decision: str
    identity_evidence: str
    local_file_name: str | None
    description_url: str
    original_url: str
    mime: str
    width: int | None
    height: int | None
    advertised_bytes: int | None
    downloaded_bytes: int | None
    sha256: str | None
    license_short_name: str
    usage_terms: str
    attribution_required: str
    artist: str
    credit: str
    source: str
    date: str
    image_description: str
    categories: str
    status: str
    notes: str
    checked_at_utc: str


def load_allowlist() -> list[dict[str, Any]]:
    value = json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    if value.get("schemaVersion") != 2:
        raise ValueError("portrait allowlist schemaVersion must be 2")
    policy = value.get("policy", {})
    for key in (
        "exactlyFivePerPoet", "identityRequiresMetadataAndHumanReview",
        "rightsRecheckedAtDownload", "archiveApprovalIsNotPublicationApproval",
        "itemLevelCreditRequired",
    ):
        if policy.get(key) is not True:
            raise ValueError(f"allowlist policy flag must be true: {key}")
    records = value.get("records")
    if not isinstance(records, list) or len(records) != 45:
        raise ValueError("portrait allowlist must contain exactly 45 records")
    seen_titles: set[str] = set()
    counts: Counter[str] = Counter()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"allowlist record {index} must be an object")
        for field in ("poetKey", "poetName", "commonsTitle", "reviewDecision"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                raise ValueError(f"allowlist record {index} missing {field}")
        evidence = record.get("identityEvidence")
        if not isinstance(evidence, list) or len(evidence) < 2 or not all(isinstance(item, str) and item.strip() for item in evidence):
            raise ValueError(f"allowlist record {index} requires metadata + human identity evidence")
        if record["reviewDecision"] != "APPROVED_REFERENCE":
            raise ValueError(f"allowlist record {index} is not approved for reference")
        title = record["commonsTitle"]
        if not title.startswith("File:") or title in seen_titles:
            raise ValueError(f"invalid/duplicate Commons title: {title}")
        seen_titles.add(title)
        counts[record["poetKey"]] += 1
    if len(counts) != 9 or set(counts.values()) != {5}:
        raise ValueError(f"allowlist must contain five records for each of nine poets: {dict(counts)}")
    return records


def clean_html(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(value))).strip()


def meta(ext: dict[str, Any], key: str) -> str:
    raw = ext.get(key, {})
    return clean_html(str(raw.get("value", ""))) if isinstance(raw, dict) else clean_html(str(raw))


def license_allowed(short: str, terms: str) -> bool:
    value = f"{short} {terms}".lower()
    return not any(pattern in value for pattern in EXCLUDED_LICENSE_PATTERNS) and any(
        pattern in value for pattern in OPEN_LICENSE_PATTERNS
    )


def request(session: requests.Session, url: str, *, params: dict[str, Any] | None = None, stream: bool = False) -> requests.Response:
    last: Exception | None = None
    for attempt in range(1, 7):
        time.sleep(0.35 if not stream else 0.10)
        try:
            response = session.get(url, params=params, stream=stream, allow_redirects=True, timeout=(30, 360))
            if response.status_code == 429:
                raw = response.headers.get("Retry-After", "")
                try:
                    wait = float(raw)
                except ValueError:
                    wait = attempt * 8.0
                response.close()
                if attempt < 6:
                    time.sleep(min(max(wait, 5.0), 90.0))
                    continue
            if response.status_code in {500, 502, 503, 504} and attempt < 6:
                response.close()
                time.sleep(min(attempt * 5.0, 45.0))
                continue
            return response
        except requests.RequestException as exc:
            last = exc
            if attempt < 6:
                time.sleep(min(attempt * 5.0, 45.0))
                continue
            raise
    raise RuntimeError(f"request failed: {last}")


def hydrate(session: requests.Session, titles: list[str]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for start in range(0, len(titles), 10):
        response = request(session, API, params={
            "action": "query", "format": "json", "formatversion": 2,
            "titles": "|".join(titles[start:start + 10]), "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata", "iiextmetadatafilter": EXT_FIELDS,
            "iiextmetadatalanguage": "en", "iimetadataversion": "latest",
        })
        response.raise_for_status()
        for page in response.json().get("query", {}).get("pages", []):
            infos = page.get("imageinfo") or []
            if infos:
                output[str(page.get("title", ""))] = infos[0]
        response.close()
    return output


def safe_stem(title: str, limit: int = 92) -> str:
    stem = re.sub(r"\.[A-Za-z0-9]{2,5}$", "", title.removeprefix("File:"))
    stem = re.sub(r'[\\/:*?"<>|]+', "_", stem)
    return re.sub(r"\s+", " ", stem).strip(" ._")[:limit] or "portrait"


def extension_for(mime: str, original_url: str) -> str:
    return {
        "image/jpeg": ".jpg", "image/png": ".png", "image/tiff": ".tif", "image/webp": ".webp",
    }.get(mime) or Path(original_url.split("?", 1)[0]).suffix or ".bin"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="approved-core-poet-portraits-45")
    parser.add_argument("--max-file-mb", type=int, default=100)
    parser.add_argument("--pause", type=float, default=0.25)
    args = parser.parse_args()

    selected = load_allowlist()
    root = Path(args.output)
    root.mkdir(parents=True, exist_ok=True)
    max_bytes = args.max_file_mb * 1024 * 1024
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT, "Api-User-Agent": USER_AGENT,
        "Accept": "application/json,image/*,*/*;q=0.8", "Referer": "https://commons.wikimedia.org/",
    })
    current = hydrate(session, [record["commonsTitle"] for record in selected])
    records: list[Record] = []
    seen_sha: set[str] = set()
    per_poet_index: dict[str, int] = {}

    for number, selection in enumerate(selected, start=1):
        poet_key = selection["poetKey"]
        poet_name = selection["poetName"]
        title = selection["commonsTitle"]
        reviewed = selection["reviewDecision"]
        identity = " | ".join(selection["identityEvidence"])
        checked = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        info = current.get(title)
        blank = dict(
            number=number, poet_key=poet_key, poet_name=poet_name, file_title=title,
            review_decision=reviewed, identity_evidence=identity, local_file_name=None,
            description_url="", original_url="", mime="", width=None, height=None,
            advertised_bytes=None, downloaded_bytes=None, sha256=None,
            license_short_name="", usage_terms="", attribution_required="", artist="",
            credit="", source="", date="", image_description="", categories="",
            status="", notes="", checked_at_utc=checked,
        )
        if not info:
            records.append(Record(**{**blank, "status": "MISSING", "notes": "Commons item not returned"}))
            continue
        ext = info.get("extmetadata") or {}
        short = meta(ext, "LicenseShortName")
        terms = meta(ext, "UsageTerms")
        original = str(info.get("url", ""))
        mime = str(info.get("mime", "")).lower()
        advertised = int(info["size"]) if info.get("size") is not None else None
        base = {
            **blank, "description_url": str(info.get("descriptionurl", "")),
            "original_url": original, "mime": mime,
            "width": int(info["width"]) if info.get("width") is not None else None,
            "height": int(info["height"]) if info.get("height") is not None else None,
            "advertised_bytes": advertised, "license_short_name": short,
            "usage_terms": terms, "attribution_required": meta(ext, "AttributionRequired"),
            "artist": meta(ext, "Artist"), "credit": meta(ext, "Credit"),
            "source": meta(ext, "Source"), "date": meta(ext, "DateTimeOriginal") or meta(ext, "DateTime"),
            "image_description": meta(ext, "ImageDescription"), "categories": meta(ext, "Categories"),
        }
        if mime not in {"image/jpeg", "image/png", "image/tiff", "image/webp"}:
            records.append(Record(**{**base, "status": "REJECTED_FORMAT", "notes": mime}))
            continue
        if not license_allowed(short, terms):
            records.append(Record(**{**base, "status": "REJECTED_LICENSE", "notes": f"{short}/{terms}"}))
            continue
        if advertised and advertised > max_bytes:
            records.append(Record(**{**base, "status": "REJECTED_SIZE", "notes": f"> {max_bytes}"}))
            continue

        response: requests.Response | None = None
        destination: Path | None = None
        try:
            response = request(session, original, stream=True)
            response.raise_for_status()
            poet_dir = root / poet_key
            poet_dir.mkdir(parents=True, exist_ok=True)
            index = per_poet_index.get(poet_key, 0) + 1
            local_name = f"{index:02d}__{safe_stem(title)}{extension_for(mime, original)}"
            destination = poet_dir / local_name
            digest = hashlib.sha256()
            size = 0
            with destination.open("wb") as handle:
                for chunk in response.iter_content(1024 * 1024):
                    if not chunk:
                        continue
                    size += len(chunk)
                    if size > max_bytes:
                        raise ValueError("stream exceeds file limit")
                    digest.update(chunk)
                    handle.write(chunk)
            response.close()
            response = None
            with Image.open(destination) as image:
                image.verify()
            sha = digest.hexdigest()
            if sha in seen_sha:
                destination.unlink(missing_ok=True)
                records.append(Record(**{**base, "downloaded_bytes": size, "sha256": sha, "status": "DUPLICATE_SHA256", "notes": "byte-identical duplicate rejected"}))
                continue
            seen_sha.add(sha)
            per_poet_index[poet_key] = index
            records.append(Record(**{
                **base, "local_file_name": f"{poet_key}/{local_name}", "downloaded_bytes": size,
                "sha256": sha, "status": "DOWNLOADED",
                "notes": "single canonical allowlist; rights rechecked; publication still requires route-level approval",
            }))
            print(f"[saved] {number}/{len(selected)} {poet_name} — {local_name}", flush=True)
        except Exception as exc:
            if response is not None:
                response.close()
            if destination is not None:
                destination.unlink(missing_ok=True)
            records.append(Record(**{**base, "status": "DOWNLOAD_FAILED", "notes": f"{type(exc).__name__}: {exc}"}))
        time.sleep(args.pause)

    downloaded = [record for record in records if record.status == "DOWNLOADED"]
    poet_names = dict.fromkeys(selection["poetName"] for selection in selected)
    counts_by_poet = {
        poet_name: sum(record.poet_name == poet_name and record.status == "DOWNLOADED" for record in records)
        for poet_name in poet_names
    }
    report = {
        "collection": "approved-core-poet-portraits-45",
        "allowlist": ALLOWLIST_PATH.relative_to(ROOT).as_posix(),
        "allowlist_sha256": hashlib.sha256(ALLOWLIST_PATH.read_bytes()).hexdigest(),
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "selected": len(selected), "downloaded": len(downloaded),
        "total_bytes": sum(record.downloaded_bytes or 0 for record in downloaded),
        "counts_by_poet": counts_by_poet,
        "license_counts": dict(Counter(record.license_short_name for record in downloaded)),
        "status_counts": dict(Counter(record.status for record in records)),
        "publication_approved": False,
        "records": [asdict(record) for record in records],
    }
    (root / "manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = list(Record.__dataclass_fields__)
    with (root / "manifest.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(asdict(record) for record in records)
    with (root / "SHA256SUMS.txt").open("w", encoding="utf-8") as handle:
        for record in downloaded:
            handle.write(f"{record.sha256}  {record.local_file_name}\n")
    (root / "README.md").write_text(
        "# Approved core poet portrait references\n\n"
        f"Canonical allowlist: `{report['allowlist']}`  \n"
        f"Allowlist SHA-256: `{report['allowlist_sha256']}`  \n"
        f"Selected: **{len(selected)}**  \nDownloaded: **{len(downloaded)}**  \n"
        "Archive approval is not publication approval. Identity and credits remain item-specific.\n",
        encoding="utf-8",
    )
    failures = {name: count for name, count in counts_by_poet.items() if count != 5}
    print(json.dumps({**{key: report[key] for key in ("selected", "downloaded", "total_bytes", "counts_by_poet", "license_counts", "status_counts")}, "failures": failures}, ensure_ascii=False))
    return 0 if len(downloaded) == 45 and not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
