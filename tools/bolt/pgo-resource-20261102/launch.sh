#!/bin/sh
set -eu
exec /usr/bin/python3 -B /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/pgo-resource-20261102/driver.py "${1:-rehearsal}"
