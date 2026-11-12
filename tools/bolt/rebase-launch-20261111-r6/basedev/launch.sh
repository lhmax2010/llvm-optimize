#!/bin/sh
set -eu
[ "$#" -eq 3 ] || { echo 'usage: launch.sh SOURCE_SHA full|rehearsal|rehearsal-02 basedev' >&2; exit 2; }
NIGHT_SOURCE_SHA=$1; export NIGHT_SOURCE_SHA
shift
[ "$2" = basedev ] || exit 2
FINAL_PROJECT=basedev; export FINAL_PROJECT
case "$1" in
 full|rehearsal|rehearsal-02) exec python3 -B "$(dirname "$0")/launcher.py" "$1" ;;
 *) exit 2 ;;
esac
