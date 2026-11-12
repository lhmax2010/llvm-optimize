#!/bin/sh
set -eu
[ "$#" -eq 2 ] || { echo 'usage: launch.sh SOURCE_SHA rehearsal|rehearsal-02|full' >&2; exit 2; }
NIGHT_SOURCE_SHA=$1; export NIGHT_SOURCE_SHA
FINAL_PROJECT=toolchain; export FINAL_PROJECT
case "$2" in rehearsal|rehearsal-02|full) exec python3 -B "$(dirname "$0")/launcher.py" "$2" ;; *) exit 2 ;; esac
