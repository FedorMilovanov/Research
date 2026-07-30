#!/usr/bin/env python3
"""Corrected v2 runner for the official 59-object acquisition queue.

Corrections after review of v1 artifacts:
- NEB's generic web-app `manifest.json` is not a book or item manifest;
- Mayakovsky NEB cards remain catalog/viewer records until a real PDF is exposed;
- JSON is not auto-downloaded from ordinary HTML discovery;
- GitHub snapshots are pinned to an immutable commit SHA, not a moving branch ZIP.
"""
from __future__ import annotations

import importlib.util
import sys
from dataclasses import replace
from pathlib import Path
from urllib.parse import urlparse

import requests

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "official_core_acquisition_v1",
    HERE / "official_core_acquisition_40plus.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load v1 acquisition module")
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)

# Generic JSON links on institution sites are usually app/config manifests, not
# source objects. Structured data repositories are acquired through dedicated
# immutable GitHub snapshots below.
mod.FILE_EXTENSIONS = tuple(ext for ext in mod.FILE_EXTENSIONS if ext != ".json")

_original_candidates = mod.candidates


def corrected_candidates():
    queue = []
    for candidate in _original_candidates():
        if candidate.id.startswith("neb-mayakovsky-12v-"):
            candidate = replace(
                candidate,
                mode="audit-only",
                rights="NEB catalog/viewer record; no direct PDF confirmed by this pass",
                max_downloads=0,
                notes=(
                    "The catalog record is verified, but generic /manifest.json is excluded. "
                    "Acquire only a real item PDF or documented viewer export in a later manual/API pass."
                ),
            )
        queue.append(candidate)
    return queue


mod.candidates = corrected_candidates


def immutable_github_archive(session: requests.Session, candidate, total_state: dict):
    parts = urlparse(candidate.landing_url).path.strip("/").split("/")
    owner, repo = parts[0], parts[1]
    api = f"https://api.github.com/repos/{owner}/{repo}"
    metadata = mod.get(session, api).json()
    default_branch = metadata["default_branch"]
    commit = mod.get(session, f"{api}/commits/{default_branch}").json()["sha"]
    archive = f"https://codeload.github.com/{owner}/{repo}/zip/{commit}"
    directory = mod.FILES / candidate.project / candidate.id
    result = mod.download(session, candidate, archive, directory, total_state)
    result["commit_ref"] = commit
    result["repository"] = f"{owner}/{repo}"
    return {
        "http_status": 200,
        "final_url": candidate.landing_url,
        "page_verified": True,
        "discovered": [archive],
    }, [result]


mod.github_archive = immutable_github_archive

if __name__ == "__main__":
    raise SystemExit(mod.main())
