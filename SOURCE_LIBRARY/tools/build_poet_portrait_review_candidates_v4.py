#!/usr/bin/env python3
"""Identity-category scoped and rate-limit-resilient portrait review wrapper.

This wrapper retains v2's recursive portrait-category discovery and v3's robust
network backoff, but rejects descendant portrait categories whose names do not
contain the current person's full name or a configured alias. This prevents,
for example, Nikolay Gumilev's photograph category from entering Anna
Akhmatova's review basket through a relationship edge in Commons categories.

The gate creates a review package. It does not assert that a depicted person is
correct; final identity approval remains manual and metadata-grounded.
"""

from __future__ import annotations

import re
import time
from typing import Any

import requests

import build_poet_portrait_review_candidates_v2 as base

ALIASES_BY_ROOT: dict[str, tuple[str, ...]] = {
    root: (person, *aliases)
    for person, root, aliases in base.PEOPLE
}

_original_portrait_categories = base.portrait_categories


def scoped_portrait_categories(
    session: requests.Session,
    root: str,
    depth: int,
    limit_per_category: int,
) -> list[str]:
    found = _original_portrait_categories(session, root, depth, limit_per_category)
    aliases = ALIASES_BY_ROOT.get(root, (root,))
    accepted: list[str] = []
    for category in found:
        normalized = re.sub(r"[_-]+", " ", category)
        if any(re.search(rf"(?<!\w){re.escape(alias)}(?!\w)", normalized, re.I) for alias in aliases):
            accepted.append(category)
    return accepted


def robust_get(
    session: requests.Session,
    url: str,
    *,
    params: dict[str, Any] | None = None,
    stream: bool = False,
) -> requests.Response:
    last: Exception | None = None
    for attempt in range(1, 9):
        time.sleep(0.60 if not stream else 0.15)
        try:
            response = session.get(
                url,
                params=params,
                stream=stream,
                timeout=(30, 240),
                allow_redirects=True,
            )
            if response.status_code == 429:
                retry_raw = response.headers.get("Retry-After", "")
                try:
                    retry_after = float(retry_raw)
                except ValueError:
                    retry_after = 8.0 * attempt
                response.close()
                if attempt < 8:
                    time.sleep(min(max(retry_after, 5.0), 90.0))
                    continue
                raise requests.HTTPError("Wikimedia API rate limit persisted after 8 attempts")
            if response.status_code in {500, 502, 503, 504}:
                status = response.status_code
                response.close()
                if attempt < 8:
                    time.sleep(min(attempt * 5.0, 45.0))
                    continue
                raise requests.HTTPError(f"Wikimedia server error persisted: {status}")
            return response
        except requests.RequestException as exc:
            last = exc
            if attempt < 8:
                time.sleep(min(attempt * 5.0, 45.0))
                continue
            raise
    raise RuntimeError(f"request failed: {last}")


base.portrait_categories = scoped_portrait_categories
base.get = robust_get

if __name__ == "__main__":
    raise SystemExit(base.main())
