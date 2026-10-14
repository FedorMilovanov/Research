#!/usr/bin/env bash
# Byte-identical pins are read from nt-corpus-v1.json, never duplicated here.
# Research checkout stays read-only; missing corpora are acquired outside Git.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$HERE/nt_sources.py" --fetch
