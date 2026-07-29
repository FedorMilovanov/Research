#!/usr/bin/env python3
"""Run the IMLI crawler with browser-compatible request headers.

Some ed-imli PDF endpoints accept the catalogue request but reject a direct
non-browser asset request. This wrapper keeps the same rights/provenance logic
and adds a normal browser User-Agent, Referer and From header. It does not
bypass authentication, payment, robots controls, or access restrictions.
"""

from __future__ import annotations

import crawl_imli_open_pdfs as crawler


BROWSER_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
)
OriginalSession = crawler.requests.Session


class BrowserCompatibleSession(OriginalSession):
    def __init__(self) -> None:
        super().__init__()
        self.headers.update(
            {
                "User-Agent": BROWSER_UA,
                "Referer": crawler.CATALOGUE,
                "From": "viktorcoy2012@gmail.com",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Upgrade-Insecure-Requests": "1",
            }
        )

    def request(self, method: str, url: str, **kwargs):  # type: ignore[no-untyped-def]
        headers = dict(kwargs.pop("headers", {}) or {})
        headers.setdefault("Referer", crawler.CATALOGUE)
        headers.setdefault("User-Agent", BROWSER_UA)
        return super().request(method, url, headers=headers, **kwargs)


crawler.USER_AGENT = BROWSER_UA
crawler.requests.Session = BrowserCompatibleSession


if __name__ == "__main__":
    raise SystemExit(crawler.main())
