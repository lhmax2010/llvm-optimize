# Hybrid LLVM + BOLT: external review revision

**BLOCKED — not ready for a full build or Gerrit upload.** The strict strip-all LOAD-byte gate requested in this review rejects the already certified ELF: removing nonloaded sections changes three section-table location fields in the ELF header, which itself belongs to the first LOAD. No exception has been applied. See [report 48 §7](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/48_review_fixes.md) before using these commits.

For code review, read **[0002-text-only.diff](0002-text-only.diff)** instead of the approximately 12.7 MB binary format-patch. It contains every helper/spec change, excluding only `packaging/clang-bolt-v2.fdata.xz`. The complete, applicable patch is `0002-packaging-optimize-x86_64-clang-with-BOLT.patch`. The previous `review-20261102` package remains unchanged; this package records the next review revision, including its unresolved gate.

## Commits and application

| Role | Commit | Parent |
|---|---|---|
| Base | `67619ec8bbbac7238a6cfc33a481ccfbcd12206f` | — |
| Hybrid | `38477c9b6e1401e5e1fe01fafa282ab92cf53887` | base above |
| BOLT, blocked draft | `bc0d58ffaab37dbcd88098ccb4c3734570345593` | hybrid above |

Final tree: `d2a5e457ecd5d439a9dd50b67fb561a5f0d67eb3`. Author, committer and sign-off: Hao Lin <hao.lin@samsung.com>. Original hybrid and BOLT Change-Ids are retained. Applying both patches to an independent index at the base reproduced this tree exactly. No source commit was pushed.

The intended sequence is ordinary build/install → installed-root snapshot → BOLT tool configuration/build certification → relink → strip-debug → rewrite/profile check → tiny/real checks → optional debug-symbol separation → strip-all/layout check → RUNPATH repair → optional debuglink → security/tiny/real checks → compare-root → cache release → native archive conversion → candidate installation → original platform post-processing once → post gate. BOLT may change the installed root only after compare-root. A preparation failure prevents candidate installation; later installation/post failures abort RPM creation, without rolling back the whole BUILDROOT.

Debug builds ship matching function symbols in `clang-debuginfo` and a CRC-checked `.gnu_debuglink`; release builds ship neither. Function names, including cold fragments, are supported; source-line localization is not implemented. `llvm-objcopy --only-keep-debug` crashes with SIGSEGV on these BOLT layouts; symbol separation uses eu-strip.

## Disabled-BOLT contract and rollback

`--without clang_bolt`, or changing the x86 bcond from `bcond_without` to `bcond_with`, disables the BOLT workflow. Relative to the same hybrid baseline, intended binary package contents and build behavior are unchanged; the source package additionally includes Source1200/profile and Source1201/helper. Both architectures without BOLT retain the same source-package addition.

The raw OFF expansions differ from the new hybrid parent by those two Source declarations **and 14 inherited empty lines** from BOLT conditional blocks. We do not claim byte equality. All nonempty lines other than the Sources are equal. Relative to 3ee2d847 OFF, the only change is this review's explicitly requested hybrid NEEDED assertion. See the complete unnormalized [debug diff](../../tools/bolt/results/review-fixes-20261103/parse-bc0d58ffaab3-retry1/off-debug-vs-hybrid.diff), [release diff](../../tools/bolt/results/review-fixes-20261103/parse-bc0d58ffaab3-retry1/off-release-vs-hybrid.diff), and [report 48 §15](../../docs/bolt/48_review_fixes.md).

## Validation boundary

| Check | Before upload | Before release |
|---|---|---|
| Complete-recipe empty-component probe | PASS: 96 interfaces, zero empty | Rerun on an LLVM upgrade |
| Fatal empty-component check and three driver NEEDED assertions | Lightweight positive/negative tests PASS | Confirm in full build |
| Explicit-helper test suite | 375/375 PASS | Rerun after further changes |
| Old helper against debuglink tests | Expected failure, 29 errors / 30 tests | — |
| GBS export and Tizen RPM five-way parse | PASS | Repeat for final revision |
| RUNPATH exact-byte real-file gate | PASS, 13a07cb7 → 8c2429d8 | Confirm in full build |
| Platform debugfiles.list real-file gate | PASS | Confirm in full build |
| strip-all raw LOAD-byte real-file gate | **BLOCKED**, ELF section-table header fields differ | Must be resolved before build |
| Exact 67619ec8 vs hybrid RPM payload/archive comparison | NOT AVAILABLE: no exact-revision full-build product proven | Obtain suitable baseline if required |
| Current debug full build / RPMs / objects | NOT RUN | Required after gate is resolved |
| Release-mode full build | NOT RUN | Required |
| Quickbuild of this revision | PENDING; not triggered | Required |
| Package installation with normal dependency checking | NOT RUN for this revision; historical debuglink test used --nodeps | Required |
| Clang and LLD component CMake consumers | NOT RUN; prior target LLVM/clang-cpp smoke is not a substitute | Required |
| accel/worker artifact identity | NOT VERIFIED | Required |
| ARM build-root smoke tests | NOT RUN; macro parse is not runtime testing | Required |
| BOLT/relink resources for this revision | NOT MEASURED; historical data only | Measure on intended workers |
| Source-line localization cost | PENDING | Separate experiment/decision |
| llvm-objcopy only-keep-debug defect | OPEN, separate fix | Track independently |

Historical evidence: [39 old-text](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/39_use_old_text_final.md), [43 debuglink full build and installed crash localization](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/43_debuginfo_symbols.md), [37 RUNPATH](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/37_runpath_and_improvements.md), [53 hybrid with PM exceptions](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/main/docs/53_hybrid_local_validation.md). These results apply to their recorded revisions, not automatically to this patch.

## Tests

From the evidence repository root, with Python, a C compiler, CMake, readelf and strip available:

```sh
python3 -B tools/bolt/run_review_tests.py \
  --helper patches/review-20261103/files/packaging/clang-bolt-helper.py
```

`--helper` is mandatory. The runner prints its resolved path and SHA256 before discovering every `test_*.py`. The disk-fault subprocesses use that same helper; they cannot silently import a stale tools-directory copy. The local execution used the CMake binary from the newly prepared probe root, via its loader, because the host PATH did not provide CMake; no historical root was configured.

## Files and identities

| File | Purpose |
|---|---|
| `0001-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch` | Full hybrid format-patch |
| `0002-packaging-optimize-x86_64-clang-with-BOLT.patch` | Full BOLT format-patch, including binary profile |
| `0002-text-only.diff` | Review copy without the profile binary; all helper/spec changes |
| `0001-commit-message.txt`, `0002-commit-message.txt` | Full commit messages |
| `files/` | Eight complete text files at the final tree, original relative paths |
| `text-file-blobs.json` | Per-file blob OID, byte size and SHA256 |
| `text-files-ls-tree.txt` | Exact git ls-tree output for the eight files |
| `final-tree-top-level.txt` | Top-level final tree listing |
| `final-tree-ls-tree.txt.xz` | Complete recursive final tree listing, compressed |
| `source-identities.json` | Source commit chain, tree and blocked status |
| `SHA256SUMS` | SHA256 of every package file except the checksum file itself |

All package files have raw URLs under `https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/patches/review-20261103/` followed by the listed relative path. Binary Source1200 remains 9,735,212 bytes, SHA256 `52fd8522b8cceadebfb6bfc0a19f721f1072cff95c682b12b2c4dd5b0cc1e27f`; its content is unchanged. The fixed OPTIONS and 111 BOLT + 2 TF task-description whitelist are unchanged.

| Text file | Git blob OID |
|---|---|
| `clang/cmake/modules/AddClang.cmake` | `8583bbcaf4d1a3d4110892f1ccf8dc509c126018` |
| `clang/tools/driver/CMakeLists.txt` | `3d8acd37075adab99220774f5c7bd42eb281ac19` |
| `lld/cmake/modules/AddLLD.cmake` | `6866e7fc87fcb9841a99cb190b0fd03bd3531bb9` |
| `lld/tools/lld/CMakeLists.txt` | `eeb81ecd6f9d2a1aff10fd0d5c76349496720302` |
| `llvm/cmake/modules/AddLLVM.cmake` | `3f345d5f0a0ac3fcbf5fef4097ab4276926f4184` |
| `llvm/tools/llvm-ar/CMakeLists.txt` | `56f7a13c885fe2569363d48e88f2ea999d0d705b` |
| `packaging/clang-bolt-helper.py` | `a74ae36562255803f638259f58c8218dccf3b8f8` |
| `packaging/llvm.spec` | `7a51be894f830043acbf25e4d822fa1af51d4a06` |
