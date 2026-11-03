#!/bin/sh
set -eu
case ${1-} in toolchain|basedev) FINAL_PROJECT=$1; export FINAL_PROJECT ;; *) echo 'usage: launch.sh toolchain|basedev rehearsal|full' >&2; exit 2 ;; esac
shift
exec python3 -B "$(dirname "$0")/launcher.py" "$@"
