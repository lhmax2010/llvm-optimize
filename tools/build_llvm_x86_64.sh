#!/usr/bin/env bash
# Default is a read-only preflight; --run is required to start GBS.
set -euo pipefail
exec python3 "$(dirname "$(readlink -f "$0")")/build_llvm_x86_64.py" "$@"
