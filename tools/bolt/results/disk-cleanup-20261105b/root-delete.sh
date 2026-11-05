#!/bin/sh
set -eu
cd "$(dirname "$0")"
exec nice -n 19 ionice -c3 /usr/bin/python3 -B ./execute.py \
  /home/linhao/Toolchain/development/llvm-optimize/temp/runpath-fix-20261026/gbs-root \
  /home/linhao/Toolchain/development/llvm-optimize/temp/oldtext-final-20261027/gbs-root \
  /home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261030/gbs-root \
  /home/linhao/Toolchain/development/llvm-optimize/temp/pgo-resource-20261102 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/review-round3-continue-20261012 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/review-round4-20261012 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-build-20260929 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-v2-20260929 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-full-build-20260927 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/archive-followup-review-20261014 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/static-native-conversion-v2-20260924 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/static-native-conversion-v3-20260924 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-x86_64-archivefix \
  /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-release-consumer-20261014-lld \
  /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-release-consumer-20261014-bfd \
  /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-archive-consumer-bfd \
  /home/linhao/Toolchain/development/llvm-optimize/temp/gbs-root-archive-consumer-lld \
  /home/linhao/Toolchain/development/llvm-optimize/temp/release-x86-full-build-20261013 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/release-attribution-20261013 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261014 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261015-install-rehearsal \
  /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261016-source-order \
  /home/linhao/Toolchain/development/llvm-optimize/temp/llvm-strip-alternative-20260929 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/llvm-strip-x86_64-20261009 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-sandbox-20261019 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-local-20261023 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-link-20261015 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/llvm-hybrid-trial \
  /home/linhao/Toolchain/development/llvm-optimize/temp/llvm-archivefix-trial \
  /home/linhao/Toolchain/development/llvm-optimize/temp/qb-full-compare-20261105 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/followup-356949-ps2-message-20261014 \
  /home/linhao/Toolchain/development/llvm-optimize/temp/gnu-strip-merged-check-20261014 \
  /home/linhao/qb_analysis
