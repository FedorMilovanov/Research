#!/usr/bin/env python3
"""Acquire current Georgia eCorp entity status for G3 by control number.

Read-only research helper. It submits the public Georgia Secretary of State
Business Search form for control number 19085916, follows the official result to
BusinessInformation, and preserves response bytes, request metadata, a plain-text
rendering, discovered links, and SHA-256 custody data.

It intentionally performs no filing, registration, certificate purchase,
payment, login, or mutation action.
"""

from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import http.cookiejar
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

BASE = "https://ecorp.sos.ga.gov"
SEARCH_URL = f"{BASE}/BusinessSearch"
CONTROL_NUMBER = "19085916"
USER_AGENT = (
    "FedorMilovanov-Research-G3-Georgia-Acquisition/1.0 "
    "(research-only read-only public-record lookup)"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


class FormParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.forms: list[dict[str, Any]] = []
        self.current: dict[str, Any] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: (v or "") for k, v in attrs}
        if tag.lower() == "form":
            self.current = {
                "action": ad.get("action", ""),
                "method": ad.get("method", "get").lower(),
                "inputs": [],
            }
        elif self.current is not None and tag.lower() in {"input", "button", "select", "textarea"}:
            self.current["inputs"].append(
                {
                    "tag": tag.lower(),
                    "name": ad.get("name", ""),
                    "type": ad.get("type", ""),
                    "value": ad.get("value", ""),
                    "id": ad.get("id", ""),
                }
            )

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "form" and self.current is not None:
            self.forms.append(self.current)
            self.current = None


class LinkTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []
        self.text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: (v or "") for k, v in attrs}
        if tag.lower() == "a":
            self._href = ad.get("href", "")
            self._text = []
        if tag.lower() in {"br", "p", "div", "tr", "li", "h1", "h2", "h3", "h4", "td", "th"}:
            self.text_parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href is not None:
            self.links.append({"href": self._href, "text": " ".join("".join(self._text).split())})
            self._href = None
            self._text = []
        if tag.lower() in {"p", "div", "tr", "li", "h1", "h2", "h3", "h4"}:
            self.text_parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)
        self.text_parts.append(data)

    def plain_text(self) -> str:
        raw = html.unescape("".join(self.text_parts))
        lines = [" ".join(line.split()) for line in raw.splitlines()]
        return "\n".join(line for line in lines if line)


def opener() -> urllib.request.OpenerDirector:
    jar = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def fetch(op: urllib.request.OpenerDirector, url: str, data: bytes | None = None, timeout: int = 120) -> tuple[bytes, dict[str, Any]]:
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded" if data is not None else "text/plain",
            "Referer": SEARCH_URL,
        },
        method="POST" if data is not None else "GET",
    )
    started = time.time()
    try:
        with op.open(req, timeout=timeout) as response:
            body = response.read()
            return body, {
                "requested_url": url,
                "final_url": response.geturl(),
                "method": "POST" if data is not None else "GET",
                "status": getattr(response, "status", None),
                "content_type": response.headers.get("Content-Type"),
                "bytes": len(body),
                "sha256": sha256_bytes(body),
                "elapsed_seconds": round(time.time() - started, 3),
            }
    except urllib.error.HTTPError as exc:
        error_body = exc.read()
        raise RuntimeError(
            f"HTTP {exc.code} for {url}: {exc.reason}; body_sha256={sha256_bytes(error_body)} bytes={len(error_body)}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"URL error for {url}: {exc.reason}") from exc


def identify_search_form(forms: list[dict[str, Any]]) -> dict[str, Any]:
    candidates: list[tuple[int, dict[str, Any]]] = []
    for form in forms:
        names = [str(i.get("name", "")) for i in form.get("inputs", [])]
        ids = [str(i.get("id", "")) for i in form.get("inputs", [])]
        hay = " ".join(names + ids).lower()
        score = 0
        if "control" in hay:
            score += 10
        if "search" in hay:
            score += 3
        if "business" in hay:
            score += 2
        if form.get("method") == "post":
            score += 1
        candidates.append((score, form))
    if not candidates:
        raise RuntimeError("No form found on Georgia BusinessSearch page")
    candidates.sort(key=lambda item: item[0], reverse=True)
    if candidates[0][0] < 5:
        raise RuntimeError(f"Could not identify control-number search form; forms={forms}")
    return candidates[0][1]


def build_search_payload(form: dict[str, Any]) -> dict[str, str]:
    payload: dict[str, str] = {}
    control_name: str | None = None
    for field in form.get("inputs", []):
        name = str(field.get("name", ""))
        if not name:
            continue
        ftype = str(field.get("type", "")).lower()
        value = str(field.get("value", ""))
        lname = name.lower()
        lid = str(field.get("id", "")).lower()
        if ftype == "hidden":
            payload[name] = value
        if "control" in lname or "control" in lid:
            control_name = name
        # Preserve explicit submit/search control when it has a value.
        if ftype in {"submit", "button"} and value and ("search" in lname or "search" in lid):
            payload[name] = value
    if control_name is None:
        raise RuntimeError(f"Search form has no identifiable control-number field: {form}")
    payload[control_name] = CONTROL_NUMBER

    # Some eCorp versions use a search-type radio/hidden field. If a field name
    # clearly indicates search type, select control number conservatively.
    for field in form.get("inputs", []):
        name = str(field.get("name", ""))
        value = str(field.get("value", ""))
        if not name:
            continue
        lname = name.lower()
        lvalue = value.lower()
        if "search" in lname and "type" in lname and "control" in lvalue:
            payload[name] = value
    return payload


def find_business_information_url(body: bytes, base_url: str) -> str | None:
    text = body.decode("utf-8", errors="replace")
    patterns = [
        r'href=["\']([^"\']*BusinessSearch/BusinessInformation\?[^"\']+)["\']',
        r'(/BusinessSearch/BusinessInformation\?businessId=\d+[^"\'<>\s]*)',
        r'(BusinessInformation\?businessId=\d+[^"\'<>\s]*)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return urllib.parse.urljoin(base_url, html.unescape(match.group(1)))
    return None


def extract_status_fields(plain: str) -> dict[str, str]:
    labels = [
        "Business Name",
        "Control Number",
        "Business Type",
        "Business Status",
        "Business Purpose",
        "Principal Office Address",
        "Date of Formation / Registration Date",
        "State of Formation",
        "Jurisdiction",
        "Last Annual Registration Year",
        "Principal Record Address",
        "Registered Agent Name",
    ]
    result: dict[str, str] = {}
    normalized = plain.replace("\r", "")
    for idx, label in enumerate(labels):
        pattern = re.compile(re.escape(label) + r"\s*:\s*([^\n]+)", re.IGNORECASE)
        match = pattern.search(normalized)
        if match:
            result[label] = match.group(1).strip()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="g3-georgia-entity-output")
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    op = opener()
    summary: dict[str, Any] = {
        "control_number": CONTROL_NUMBER,
        "state": "EPHEMERAL_ACTION_ARTIFACT",
        "publication_eligible": False,
        "errors": [],
    }

    try:
        search_body, search_meta = fetch(op, SEARCH_URL)
        (out / "BUSINESS_SEARCH.html").write_bytes(search_body)
        write_json(out / "BUSINESS_SEARCH_FETCH.json", search_meta)

        fp = FormParser()
        fp.feed(search_body.decode("utf-8", errors="replace"))
        write_json(out / "BUSINESS_SEARCH_FORMS.json", fp.forms)
        form = identify_search_form(fp.forms)
        payload = build_search_payload(form)
        write_json(out / "BUSINESS_SEARCH_PAYLOAD_KEYS.json", {k: ("<token>" if "token" in k.lower() else v) for k, v in payload.items()})

        action = urllib.parse.urljoin(SEARCH_URL, form.get("action") or "")
        method = str(form.get("method", "get")).lower()
        encoded = urllib.parse.urlencode(payload).encode("utf-8")
        if method == "get":
            search_result_url = action + ("&" if "?" in action else "?") + urllib.parse.urlencode(payload)
            result_body, result_meta = fetch(op, search_result_url)
        else:
            result_body, result_meta = fetch(op, action, data=encoded)
        (out / "BUSINESS_SEARCH_RESULT.html").write_bytes(result_body)
        write_json(out / "BUSINESS_SEARCH_RESULT_FETCH.json", result_meta)

        result_parser = LinkTextParser()
        result_parser.feed(result_body.decode("utf-8", errors="replace"))
        (out / "BUSINESS_SEARCH_RESULT.txt").write_text(result_parser.plain_text(), encoding="utf-8")
        write_json(out / "BUSINESS_SEARCH_RESULT_LINKS.json", result_parser.links)

        info_url = find_business_information_url(result_body, result_meta.get("final_url") or action)
        if info_url is None:
            # Some versions render the information directly after search.
            plain_result = result_parser.plain_text()
            if CONTROL_NUMBER in plain_result and "Business Status" in plain_result:
                info_body = result_body
                info_meta = result_meta
                info_url = result_meta.get("final_url") or action
            else:
                raise RuntimeError("Search completed but no BusinessInformation URL/entity detail was found")
        else:
            info_body, info_meta = fetch(op, info_url)

        (out / "BUSINESS_INFORMATION.html").write_bytes(info_body)
        write_json(out / "BUSINESS_INFORMATION_FETCH.json", info_meta)
        ip = LinkTextParser()
        ip.feed(info_body.decode("utf-8", errors="replace"))
        plain = ip.plain_text()
        (out / "BUSINESS_INFORMATION.txt").write_text(plain, encoding="utf-8")
        write_json(out / "BUSINESS_INFORMATION_LINKS.json", ip.links)
        fields = extract_status_fields(plain)
        write_json(out / "ENTITY_FIELDS.json", fields)

        if CONTROL_NUMBER not in plain:
            raise RuntimeError(f"BusinessInformation response does not contain control number {CONTROL_NUMBER}")
        if "Business Status" not in plain:
            raise RuntimeError("BusinessInformation response lacks a Business Status field")

        summary.update(
            {
                "business_information_url": info_url,
                "search_fetch": search_meta,
                "result_fetch": result_meta,
                "business_information_fetch": info_meta,
                "entity_fields": fields,
                "status_verified_in_body": True,
            }
        )
    except Exception as exc:
        summary["errors"].append(str(exc))

    write_json(out / "SUMMARY.json", summary)
    if summary["errors"]:
        for err in summary["errors"]:
            print(f"ERROR: {err}", file=sys.stderr)
        return 2
    print(json.dumps(summary.get("entity_fields", {}), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
