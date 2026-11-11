#!/bin/sh
set -eu
[ "$#" -ge 2 ] || { echo 'usage: launch.sh SOURCE_SHA full basedev | launch.sh SOURCE_SHA rehearsal|rehearsal-02 toolchain|basedev | launch.sh SOURCE_SHA night (legacy, do not use)' >&2; exit 2; }
NIGHT_SOURCE_SHA=$1; export NIGHT_SOURCE_SHA
shift
case "$1" in
 full) [ "$#" -eq 2 ] || exit 2; [ "$2" = basedev ] || exit 2; FINAL_PROJECT=basedev; export FINAL_PROJECT; exec python3 -B "$(dirname "$0")/launcher.py" full ;;
 night) [ "$#" -eq 1 ] || exit 2; exec python3 -B "$(dirname "$0")/night.py" ;;
 rehearsal|rehearsal-02) [ "$#" -eq 2 ] || exit 2; case "$2" in toolchain|basedev) FINAL_PROJECT=$2; export FINAL_PROJECT ;; *) exit 2 ;; esac; exec python3 -B "$(dirname "$0")/launcher.py" "$1" ;;
 *) exit 2 ;;
esac
