#!/bin/sh
set -eu
[ "$#" -ge 2 ] || { echo 'usage: launch.sh SOURCE_SHA night | launch.sh SOURCE_SHA rehearsal toolchain|basedev' >&2; exit 2; }
NIGHT_SOURCE_SHA=$1; export NIGHT_SOURCE_SHA
shift
case "$1" in
 night) [ "$#" -eq 1 ] || exit 2; exec python3 -B "$(dirname "$0")/night.py" ;;
 rehearsal) [ "$#" -eq 2 ] || exit 2; case "$2" in toolchain|basedev) FINAL_PROJECT=$2; export FINAL_PROJECT ;; *) exit 2 ;; esac; exec python3 -B "$(dirname "$0")/launcher.py" rehearsal ;;
 *) exit 2 ;;
esac
