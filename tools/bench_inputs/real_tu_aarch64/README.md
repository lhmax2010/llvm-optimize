# AArch64 profile v2 training inputs

The same ten LLVM source TUs as `../real_tu/selection.json`, freshly preprocessed
by the RPM baseline clang 22 for `aarch64-tizen-linux-gnu`. This is a separate
corpus; ARM training/holdout inputs are unchanged. Each `.flags.json` records the
target, input hash, source, original command, and full preprocessing command.

Sysroot: `/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.aarch64.0`.
Resource headers: workspace `temp/toolchain-baseline/usr/lib64/clang/22`.
Macro audit: workspace `temp/bolt-aarch64-v2-20260921/preprocess/target-predefined-macros.txt`
contains `__aarch64__` and neither `__arm__` nor `__x86_64__`.

Files above 10,000,000 bytes are referenced by absolute `input` in their sidecar.
In particular, `llvm_sema_SemaExprCXX.ii` (10,178,219 bytes) stays at:
`/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-aarch64-v2-20260921/preprocess/llvm_sema_SemaExprCXX.ii`.
Copy that audited input and adjust only its sidecar path when moving machines;
verify SHA256 before use. Do not relabel x86 or ARM preprocessed output as AArch64.

Pass both `--aarch64-real-tu-dir tools/bench_inputs/real_tu_aarch64` and
`--aarch64-sysroot <root>` to `tools/bench_toolchain.py`. These ten compilation
cases join the ARM 13 in the same interleaved run. Link/archive fixtures remain
ARM. Profile collection and comparison protocol/results are in `docs/20`.

A source under LLVM `lib/Target/ARM` describes ARM compiler internals, but compiling
that C++ source with the AArch64 triple exercises Clang's AArch64 code generator.
Source-directory names do not specify the target of the measured object.
