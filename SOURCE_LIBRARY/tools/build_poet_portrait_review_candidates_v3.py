#!/usr/bin/env python3
"""Rate-limit-resilient wrapper for strict recursive portrait review v2."""

from __future__ import annotations

import time
from typing import Any

import requests

import build_poet_portrait_review_candidates_v2 as base


def robust_get(
    session: requests.Session,
    url: str,
    *,
    params: dict[str, Any] | None = None,
    stream: bool = False,
) -> requests.Response:
    last: Exception | None = None
    for attempt in range(1, 9):
        # Commons extmetadata is expensive; spacing requests avoids 429 bursts.
        time.sleep(0.55 if not stream else 0.15)
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
                response.close()
                if attempt < 8:
                    time.sleep(min(attempt * 5.0, 45.0))
                    continue
                raise requests.HTTPError(f"Wikimedia server error persisted: {response.status_code}")
            return response
        except requests.RequestException as exc:
            last = exc
            if attempt < 8:
                time.sleep(min(attempt * 5.0, 45.0))
                continue
            raise
    raise RuntimeError(f"request failed: {last}")


base.get = robust_get

if __name__ == "__main__":
    raise SystemExit(base.main())
