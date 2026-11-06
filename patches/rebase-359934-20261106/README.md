# Review materials: based on Change 359934 PS10

Start with **0002-text-only.patch** for the BOLT code review; it contains every helper/spec change from 0002.patch and excludes only the profile binary. The existing 0002.patch remains the complete, applicable patch including Source1200.

## Baseline and commits

Apply 0001.patch, 0002.patch and 0003.patch in order to **13c3e223d9e1b35e4affb55255c5042f8c940f35** (Change **359934**, **PS10**, **NEW**), whose parent is **cf4b6777d056131e2534ecb460c5575327d99646** (Change **357163**, **NEW**). Both states were confirmed after the sandbox push on 2026-11-06 at 16:34 +08:00; this is not a claim that either change has merged into tizen_base.

| Patch | Commit | Title |
|---|---|---|
| 0001.patch | a73a7da32049569b1360e9c13d0633c168b8f173 | cmake: use hybrid LLVM linkage on x86_64 |
| 0002.patch | e08ed9edd94c302b151a5f65940db7650c5c3a5d | packaging: optimize x86_64 clang with BOLT |
| 0003.patch | 7d5e28ca89ed68e3360765bc4e42234eaaabae27 | packaging: fix x86 LLVM flags and archive mode |

The third commit only rearranged its message relative to a3d18c2d. Tree: 33d96ba16de757458e0a0cec5a2b89b2ef41a53f. The first two commits are unchanged. The explicit-lease sandbox update was recorded in [69 §5](../../docs/bolt/69_rebase_on_359934.md); no refs/for push was made. This material refresh does not modify or push LLVM source.

## Files for review

| Path | Purpose |
|---|---|
| 0001.patch / 0002.patch / 0003.patch | Complete patches in application order; existing files retained unchanged by this refresh. |
| 0002-text-only.patch | Complete textual BOLT patch, excluding only Source1200; full patch is 0002.patch. |
| converter-vs-ps10.diff | Full-index diff of the final archive converter against headquarters PS10. |
| files/clang/cmake/modules/AddClang.cmake | Full final text from 7d5e28ca89ed68e3360765bc4e42234eaaabae27; original relative path retained. |
| files/clang/tools/driver/CMakeLists.txt | Full final text from 7d5e28ca89ed68e3360765bc4e42234eaaabae27; original relative path retained. |
| files/lld/cmake/modules/AddLLD.cmake | Full final text from 7d5e28ca89ed68e3360765bc4e42234eaaabae27; original relative path retained. |
| files/lld/tools/lld/CMakeLists.txt | Full final text from 7d5e28ca89ed68e3360765bc4e42234eaaabae27; original relative path retained. |
| files/llvm/cmake/modules/AddLLVM.cmake | Full final text from 7d5e28ca89ed68e3360765bc4e42234eaaabae27; original relative path retained. |
| files/llvm/tools/llvm-ar/CMakeLists.txt | Full final text from 7d5e28ca89ed68e3360765bc4e42234eaaabae27; original relative path retained. |
| files/packaging/clang-bolt-helper.py | Full final text from 7d5e28ca89ed68e3360765bc4e42234eaaabae27; original relative path retained. |
| files/packaging/llvm-static-archives-native.py | Full final text from 7d5e28ca89ed68e3360765bc4e42234eaaabae27; original relative path retained. |
| files/packaging/llvm.spec | Full final text from 7d5e28ca89ed68e3360765bc4e42234eaaabae27; original relative path retained. |
| SHA256SUMS | SHA256 of every review-package file except this checksum manifest itself. |

## Source1200

The profile is not duplicated under files/. Its contents remain in the existing full 0002.patch.

- Filename: packaging/clang-bolt-v2.fdata.xz
- Bytes: 9735212
- SHA256: 52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f

Generation: full files use git show FINAL:path; converter diff uses git diff --full-index PS10 FINAL -- packaging/llvm-static-archives-native.py; textual BOLT patch uses git format-patch -1 --stdout --full-index BOLT -- . ":(exclude)packaging/clang-bolt-v2.fdata.xz". The textual diff was checked byte-for-byte against the two-commit git diff, with only the format-patch envelope excluded.

Validation/conflict resolution and the repaired Base-Dev rehearsal: [69_rebase_on_359934.md](../../docs/bolt/69_rebase_on_359934.md). Design v2: [tizen_llvm_speed_design_v2.md](../../docs/bolt/design/tizen_llvm_speed_design_v2.md).
