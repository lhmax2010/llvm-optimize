# 试跑，非正式数据（151 G 链并行）

Rounds 1, jobs 1, CPUs [19].

| Variant | Valid rounds | Median total wall (s) | IQR (s) | Speedup vs V0 | Per-TU speedup Q1 / median / Q3 | Objects |
|---|---:|---:|---:|---:|---|---|
| V0 | 1 | 195.799 | 0.000 | 1.000× | 1.000× / 1.000× / 1.000× | 0 same / 0 different / 0 unverified |
| V1 | 1 | 281.435 | 0.000 | 0.696× | 1.253× / 2.194× / 4.475× | 🔴 0 same / 20 different / 0 unverified |

## Object differences and failures

- 🔴 Round 1 · V1 · zlib-compress · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-ELF · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-adler32 · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-Metadata · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-inffast · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-Driver · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-infback · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-InstrProfReader · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-gzclose · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-ScalarEvolution · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-inflate · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-ParentMapContext · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-gzwrite · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-ParseDecl · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-deflate · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-CoverageMappingGen · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-unzip · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-AArch64InstructionSelector · DIFFERENT.
- 🔴 Round 1 · V1 · zlib-zip · DIFFERENT.
- 🔴 Round 1 · V1 · llvm-X86ISelDAGToDAG · DIFFERENT.
