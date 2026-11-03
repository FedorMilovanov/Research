#!/usr/bin/env python3
"""Read-only GitHub Actions run census with cap-safe UTC range partitioning.

GitHub may truncate total_count for a broad query. Every inclusive UTC-second
interval is recursively bisected until each count is below the conservative
2,500-result threshold. The two children never overlap or leave a gap.

Requires the GitHub CLI ('gh') authenticated for the owning account.
Only counts runs currently available via the GitHub REST API.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

OWNER = "FedorMilovanov"
UTC = dt.timezone.utc
REPOS = (
    "gb-is-my-strength", "TheLegendaryPoet", "video-channel-manager",
    "mp3telegrambot", "bible-bot", "Milovi_Cake", "Milovi_School",
    "DeepMovieReview", "Research", "AuditRepo",
)
THRESHOLD = 2500
START = "2026-01-01T00:00:00Z"


def parse_utc(value: str) -> dt.datetime:
    instant = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if instant.tzinfo is None:
        raise ValueError("UTC offset required")
    instant = instant.astimezone(UTC)
    if instant.microsecond:
        raise ValueError("UTC precision must be whole seconds")
    return instant


def stamp(value: dt.datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_count(repo: str, start: dt.datetime, end: dt.datetime) -> int:
    path = f"repos/{OWNER}/{repo}/actions/runs"
    interval = f"created={stamp(start)}..{stamp(end)}"
    result = subprocess.run(
        ["gh", "api", "-X", "GET", path, "-f", interval,
         "-f", "per_page=1", "--jq", ".total_count"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    try:
        count = int(result.stdout.strip())
    except ValueError as error:
        raise RuntimeError(f"Invalid count for {repo} {interval}") from error
    if count < 0:
        raise RuntimeError(f"Negative count for {repo} {interval}")
    return count


def census(repo: str, start: dt.datetime, end: dt.datetime) -> tuple[int, int]:
    count = get_count(repo, start, end)
    if count < THRESHOLD:
        return count, 1
    gap_seconds = int((end - start).total_seconds())
    if gap_seconds < 1:
        raise RuntimeError(f"Cannot partition capped UTC second: {repo} {stamp(start)}")
    midpoint = start + dt.timedelta(seconds=gap_seconds // 2)
    left, left_calls = census(repo, start, midpoint)
    right, right_calls = census(repo, midpoint + dt.timedelta(seconds=1), end)
    return left + right, 1 + left_calls + right_calls


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--through", default=stamp(dt.datetime.now(UTC).replace(microsecond=0)),
                        help="Inclusive UTC-second snapshot timestamp")
    parser.add_argument("--from-utc", default=START, help="Inclusive start timestamp")
    parser.add_argument("--owner", default=OWNER)
    parser.add_argument("--out", type=Path, help="Write semicolon-delimited CSV")
    args = parser.parse_args()
    if args.owner != OWNER:
        parser.error("This measurement is scoped to FedorMilovanov repositories")
    start, end = parse_utc(args.from_utc), parse_utc(args.through)
    if start > end:
        parser.error("Start after end")
    output = []
    for repo in REPOS:
        count, calls = census(repo, start, end)
        output.append({
            "repository": repo, "visible_runs": count, "api_requests": calls,
            "from_utc": stamp(start), "through_utc": stamp(end),
        })
        print(f"{repo}: {count} visible runs ({calls} API calls)", file=sys.stderr)
    fields = ["repository", "visible_runs", "api_requests", "from_utc", "through_utc"]
    if args.out:
        with args.out.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, delimiter=";")
            writer.writeheader()
            writer.writerows(output)
    print(json.dumps({
        "visible_runs_total": sum(row["visible_runs"] for row in output),
        "api_requests_total": sum(row["api_requests"] for row in output),
        "repositories": len(output), "from_utc": stamp(start),
        "through_utc": stamp(end),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
