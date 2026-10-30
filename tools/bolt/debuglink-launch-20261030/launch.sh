#!/bin/sh
# No source edits. Default: the fresh evening root; rehearsal must be explicit.
set -eu
exec /usr/bin/python3 -B /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/debuglink-launch-20261030/launcher.py "${1:-full}"
