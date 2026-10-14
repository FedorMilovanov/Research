#!/usr/bin/env bash
# Fixed-tree NT + three root checks. No implicit download or Genesis exemption.
# --fetch is explicit; raw study-text logs remain outside Git.
set -euo pipefail
cd "$(dirname "$0")/../../.."
export PYTHONDONTWRITEBYTECODE=1
exec python3 ИСКУПЛЕНИЕ/nt/tools/run_audit.py "$@"
