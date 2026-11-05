#!/bin/sh
set -eu
status=failed
reason=precheck
finish() { printf 'CLEANUP_QB 已结束 %s status=%s reason=%s\n' "$(date -Iseconds)" "$status" "$reason"; }
trap finish EXIT
/usr/bin/python3 -B /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/disk-cleanup-20261105c/root-audit.py
reason=deletion
df -B1 /home
rm -rf --one-file-system -- /home/linhao/qb_analysis
[ ! -e /home/linhao/qb_analysis ]
df -B1 /home
status=ok
reason=approved-path-removed
