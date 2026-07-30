#!/usr/bin/env python3
"""Audit official OpenAI/Google URLs related to ChatGPT Google Drive uploads."""

from __future__ import annotations

import csv
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import requests

USER_AGENT = "TheLegendaryPoet-SourceAudit/1.0 (+https://github.com/FedorMilovanov/Research)"
TIMEOUT = 30

SOURCES: list[tuple[str, str, str]] = [
    # OpenAI help / release notes
    ("openai-help", "Apps in ChatGPT", "https://help.openai.com/en/articles/11487775-apps-in-chatgpt"),
    ("openai-help", "Google app data controls", "https://help.openai.com/en/articles/10408842-google-app-for-chatgpt-data-controls-faq"),
    ("openai-help", "Google Drive sync setup", "https://help.openai.com/en/articles/10948259-google-drive-app-with-sync-self-service-setup"),
    ("openai-help", "Apps with sync", "https://help.openai.com/en/articles/10847137-chatgpt-apps-with-sync"),
    ("openai-help", "File uploads FAQ", "https://help.openai.com/en/articles/8555545-file-uploads-faq"),
    ("openai-help", "ChatGPT release notes", "https://help.openai.com/en/articles/6825453-chatgpt-release-notes"),
    ("openai-help", "Admin app controls", "https://help.openai.com/en/articles/11509118-admin-controls-security-and-compliance-in-apps-enterprise-edu-and-business"),
    ("openai-help", "Plugins in ChatGPT and Codex", "https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex"),
    # OpenAI status history relevant to connectors/files/write actions
    ("openai-status", "Connectors and files outage July 19 2026", "https://status.openai.com/incidents/01KXXDNEAKEPRGFM661SBJJAM6"),
    ("openai-status", "Library upload errors July 13 2026", "https://status.openai.com/incidents/01KXDBYJ7BWBE2NRDAQTKPM5WK"),
    ("openai-status", "Elevated errors July 23 2026", "https://status.openai.com/incidents/01KY81XMFAV8KXNJGVNEMKAK15"),
    ("openai-status", "Conversation errors July 25-27 2026", "https://status.openai.com/incidents/01KYDN6YPS6ARY1EC9089N089G"),
    ("openai-status", "Connectors disconnected December 2025", "https://status.openai.com/incidents/01KC2MV5CHD4DX8A76FT4QEZEV"),
    ("openai-status", "Apps unselectable January 2026", "https://status.openai.com/incidents/01KESV314P64MK8XSV6Q5DCDJ2"),
    ("openai-status", "Connector write actions disabled April-May 2026", "https://status.openai.com/incidents/01KQDM1K1826RP1FFN86ZNA3WG"),
    ("openai-status", "Plus and Pro connector errors August 2025", "https://status.openai.com/incidents/01K2MTRK6ZWTEV75D5EGNSNEYA"),
    # Google Drive API guides/reference
    ("google-drive", "Upload file data", "https://developers.google.com/workspace/drive/api/guides/manage-uploads"),
    ("google-drive", "files.create", "https://developers.google.com/workspace/drive/api/reference/rest/v3/files/create"),
    ("google-drive", "Usage limits", "https://developers.google.com/workspace/drive/api/guides/limits"),
    ("google-drive", "Resolve errors", "https://developers.google.com/workspace/drive/api/guides/handle-errors"),
    ("google-drive", "Create folders", "https://developers.google.com/workspace/drive/api/guides/folder"),
    ("google-drive", "Create and manage files", "https://developers.google.com/workspace/drive/api/guides/create-file"),
    ("google-drive", "Search files and folders", "https://developers.google.com/workspace/drive/api/guides/search-files"),
    ("google-drive", "Files and folders overview", "https://developers.google.com/workspace/drive/api/guides/about-files"),
    ("google-drive", "Choose Drive API scopes", "https://developers.google.com/workspace/drive/api/guides/api-specific-auth"),
    ("google-drive", "Download and export files", "https://developers.google.com/workspace/drive/api/guides/manage-downloads"),
    ("google-drive", "Manage sharing", "https://developers.google.com/workspace/drive/api/guides/manage-sharing"),
    ("google-drive", "Shared drives overview", "https://developers.google.com/workspace/drive/api/guides/about-shareddrives"),
    ("google-drive", "Implement shared drive support", "https://developers.google.com/workspace/drive/api/guides/enable-shareddrives"),
    ("google-drive", "File resource", "https://developers.google.com/workspace/drive/api/reference/rest/v3/files"),
    ("google-drive", "files.list", "https://developers.google.com/workspace/drive/api/reference/rest/v3/files/list"),
    ("google-drive", "files.get", "https://developers.google.com/workspace/drive/api/reference/rest/v3/files/get"),
    ("google-drive", "files.update", "https://developers.google.com/workspace/drive/api/reference/rest/v3/files/update"),
    ("google-drive", "files.delete", "https://developers.google.com/workspace/drive/api/reference/rest/v3/files/delete"),
    ("google-drive", "files.copy", "https://developers.google.com/workspace/drive/api/reference/rest/v3/files/copy"),
    ("google-drive", "files.export", "https://developers.google.com/workspace/drive/api/reference/rest/v3/files/export"),
    # Google OAuth and account controls
    ("google-oauth", "OAuth 2.0 overview", "https://developers.google.com/identity/protocols/oauth2"),
    ("google-oauth", "OAuth scopes", "https://developers.google.com/identity/protocols/oauth2/scopes"),
    ("google-oauth", "OAuth best practices", "https://developers.google.com/identity/protocols/oauth2/resources/best-practices"),
    ("google-oauth", "OAuth policies", "https://developers.google.com/identity/protocols/oauth2/policies"),
    ("google-account", "Manage third-party connections", "https://support.google.com/accounts/answer/13533235?hl=en"),
    ("google-account", "Fix third-party connection issues", "https://support.google.com/accounts/answer/12917337?hl=en"),
    ("google-account", "Share account data with third-party apps", "https://support.google.com/accounts/answer/14012355?hl=en"),
    ("google-workspace", "Control third-party app access", "https://support.google.com/a/answer/7281227?hl=en"),
    ("google-workspace", "Authorize unverified third-party apps", "https://support.google.com/a/answer/9352843?hl=en"),
    ("google-workspace", "Context-Aware Access", "https://support.google.com/a/answer/12645308?hl=en"),
]


@dataclass
class Result:
    category: str
    title: str
    requested_url: str
    status: int | None
    final_url: str | None
    content_type: str | None
    elapsed_ms: int | None
    outcome: str
    error: str | None


def check(session: requests.Session, category: str, title: str, url: str) -> Result:
    started = time.monotonic()
    try:
        response = session.get(url, timeout=TIMEOUT, allow_redirects=True, stream=True)
        elapsed = round((time.monotonic() - started) * 1000)
        status = response.status_code
        content_type = response.headers.get("content-type", "").split(";", 1)[0] or None
        final_url = response.url
        response.close()
        if 200 <= status < 400:
            outcome = "OK"
        elif status in {401, 403, 429}:
            outcome = "RESTRICTED_OR_RATE_LIMITED"
        else:
            outcome = "HTTP_ERROR"
        return Result(category, title, url, status, final_url, content_type, elapsed, outcome, None)
    except requests.RequestException as exc:
        elapsed = round((time.monotonic() - started) * 1000)
        return Result(category, title, url, None, None, None, elapsed, "REQUEST_FAILED", f"{type(exc).__name__}: {exc}")


def write_outputs(results: Iterable[Result], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    rows = list(results)
    (output / "results.json").write_text(json.dumps([asdict(row) for row in rows], ensure_ascii=False, indent=2), encoding="utf-8")
    with (output / "results.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(Result.__annotations__))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)

    counts: dict[str, int] = {}
    for row in rows:
        counts[row.outcome] = counts.get(row.outcome, 0) + 1
    lines = [
        "# ChatGPT ↔ Google Drive upload: 46-link audit",
        "",
        f"- Checked: **{len(rows)}** official URLs",
        f"- Outcomes: `{counts}`",
        "",
        "## Interpretation",
        "",
        "An HTTP result only verifies that an official documentation/status endpoint is reachable from the runner. It does not prove that the user's OAuth token or ChatGPT connector runtime is healthy.",
        "",
        "## Results",
        "",
    ]
    for row in rows:
        lines.append(f"- `{row.outcome}` `{row.status or '-'}` — **{row.title}** — {row.requested_url}")
    (output / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "text/html,application/json;q=0.9,*/*;q=0.5"})
    results: list[Result] = []
    for index, source in enumerate(SOURCES, start=1):
        result = check(session, *source)
        results.append(result)
        print(f"[{index:02d}/{len(SOURCES)}] {result.outcome} {result.status or '-'} {result.title}", flush=True)
        time.sleep(0.35)
    write_outputs(results, Path("google-drive-upload-link-audit"))
    failed = [row for row in results if row.outcome == "REQUEST_FAILED"]
    return 1 if len(failed) > 8 else 0


if __name__ == "__main__":
    raise SystemExit(main())
