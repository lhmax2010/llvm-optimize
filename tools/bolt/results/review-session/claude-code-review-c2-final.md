# Final review: 361624 next patch set, candidate C2 (5e58d656)

## What I checked

**Identity.**
- `archive/task144/source-c2` holds C2 `5e58d65678e2d936b28eb4458bbd73a51abe5e06`, tree `ef1ab363…`, parent `f346dd75…`. Author Dongkyun Son, with the same author date as PS4 `1ddecbe8`, which has the same parent.
- `git diff --full-index 1ddecbe8 5e58d656` is byte-identical to `task144/ps4-c2.diff`.
- The C2 message equals `c2-message.txt`, apart from git's trailing newline.

**Trees compared.** All exported from local objects into my scratchpad, with lazy fetch disabled:
- PS1 `da885208`, plus PS1 with `combined/C1.diff` applied (the fix set I reviewed in `claude-code-review-361624-fix.md`);
- PS4;
- C2;
- PS4's parent.

**Evidence read.**
- `checklist.json`, `cmake-probe.json`, `static.json` (summary), `ps4-parent-vs-ps5.diff`, `ps1-ps4.range-diff`.
- Docs 144, 145 and 146.
- `task146/unclassified-v2.json`, which I analysed entry by entry.
- `classification-v2-summary.json` and `clang-v2-raw-differences.txt` (skimmed).

**Not done.** No build, no Gerrit writes.

## Verdict

**C2 itself has no correctness problem, and it is ready to upload as far as code and packaging go.**

**The PM ruling reaches the right conclusion: none of the 131 differences comes from C2.** But its stated reasons are incomplete for 14 of the "128 `.relro_padding`" binaries:
- Their `.text`, and for some `.rodata`, `.eh_frame` or `.plt`/`.init`, differences were never compared at the instruction level.
- Three of them almost certainly contain the same default-linker code change as clang-22, not just a layout shift.

This is an evidence and wording correction to the ruling, not a defect in C2. Details are in section 5.

## 1. Is ps4-c2.diff correct on top of PS4?

- **`bolt/` in C2 equals C1, plus the wording fixes from my earlier review** (I checked with `diff -r` against PS1 with C1 applied):
  - `set(BOLT_LLVM_LINK_MODE "")` instead of the bare `set()`;
  - the runtime-flags comment moved into the `if(BOLT_BUILT_STANDALONE)` block;
  - the two X86 comments reworded to name the dylib condition.

  Nothing else differs.
- **PS4's `bolt/` is byte-identical to PS1's**, so the C1 analysis applies unchanged.
- **`llvm-tools-subpkgs.spec` in C2 equals C1's, plus PS4's own aarch64 `-mtune=cortex-a57.cortex-a53` fix**, which C2 keeps.
- **`llvm.spec`.** C2 changes only two hunks against PS4: removing `Requires: python3` with the comment fix, and the armv7l targets back to `ARM;BPF`. Every other PS1/PS4 change against the parent is untouched:
  - Obsoletes;
  - MLGO assets for incremental builds;
  - `--build-id=sha1`;
  - DESTDIR install and the libgomp/libiomp5 removal;
  - the analyzer file moves.
- **Nothing is duplicated.** There is a single `rm` of `libLLVMBOLT*.a`, a single `ExclusiveArch`, and one `LLVM_OPTIONAL_SOURCES` append. All 18 sites carry `${BOLT_LLVM_LINK_MODE}` exactly once.

## 2. In-tree with 361395

- **The code is identical to the parent.** With `${BOLT_LLVM_LINK_MODE}` replaced by `DISABLE_LLVM_LINK_LLVM_DYLIB`, C2's `bolt/` matches the parent everywhere except code that is inactive in-tree: the standalone-only blocks and the optional mirror source.
- **The variable is defined in time.** It is set before `add_subdirectory(lib/tools/unittests)`.
- **Every target is covered.** The 18 sites cover every BOLT library, tool, fuzzer and unit test that links LLVM. The runtime is plain static archives.
- **The in-tree configure now passes.** `cmake-probe.json` shows PS4 failing in-tree ("Found erroneous configuration for source file X86BoltMnemonicTables.cpp"). C2 configures, and `llvm-bolt`'s link uses the static `libLLVMX86*.a` components, with `link_libLLVM_so: false`.
- **B1 passes the BOLT gates.**
- **One evidence gap.** The B1 in-tree `llvm-bolt` NEEDED list was not retained in full. Only the gate verdict and the CMake link line remain (doc 145). The link line is sufficient for this conclusion.

## 3. Standalone with the LLVM dylib

**The behaviour is identical to PS4**, because PS4's `bolt/` equals PS1's and my C1 analysis applies:
- the link-mode argument is empty;
- the mirror source and `BOLT_STANDALONE_X86_TABLES` are active;
- the runtime gets empty `CMAKE_C_FLAGS`/`CMAKE_CXX_FLAGS`.

B2 confirms this on x86_64:
- the binaries need `libLLVM.so.22.1`;
- `X86BoltMnemonicTables.cpp.o` is compiled;
- the runtime cache has empty C/C++ flags;
- `--version` lists `x86-64` and `aarch64`;
- both rewrite smoke tests pass.

**Not built:** an aarch64-host standalone build. The aarch64 rewrite smoke ran on the x86_64 host. The spec logic for aarch64 (targets `AArch64`, suffix `64`) is confirmed only by the static expansion.

## 4. Packaging

**No regression found.**
- **`llvm.spec`:** relative to PS4's parent, C2 contains only PS1's intended changes. The two C2 hunks return python3 and the armv7l targets to the parent's state.
- **RPM Requires:** `b1-audit-rpm-requires.json` is empty, so there is no Requires difference against the PS5 build.
- **`llvm-tools-subpkgs.spec`:** the same as C1, which I reviewed before:
  - version pins and the five-package Version-Release check;
  - per-architecture targets;
  - `ExclusiveArch: x86_64 aarch64`;
  - `$LDFLAGS` preserved;
  - suffix derived from `%{_lib}`;
  - single merge-fdata install;
  - `bolt` no longer requires `compiler-rt`.
- **B2 checks the result:** the package payload (7 tools plus 2 runtime archives), Requires, GNU_RELRO, and the debug build-id pairing.

## 5. The PM ruling on the 131 differences

**No C2 effect can hide among them.** The only paths by which C2 can change the x86_64 `llvm.spec` output are:
- **the in-tree `llvm-bolt` used by the 361395 pipeline.** It is not shipped; it only affects `clang-22` through its rewrite.
- **package metadata:** the python3 Requires, which is absent on both sides.

None of the 130 non-BOLT ELF files is built from anything C2 changes. For `clang-22`, a behavioural change in C2's `llvm-bolt` would show up in many functions, but 146,957 of 146,959 are identical.

**Each part of the ruling:**
- **`LLVMgold.so` and `ompdModule.so`: sound.**
  - The only differing section is `.gnu_debuglink`, and the C2 CRC equals the recomputed CRC of the C2 `.debug` file.
  - Neither has a build ID on either side. Both are CMake MODULE libraries, and PS4 sets only `CMAKE_EXE_LINKER_FLAGS`/`CMAKE_SHARED_LINKER_FLAGS`.
  - The `.debug` files differ through the release-specific source path (`llvm-22.1.8-2.1` against `-1`), which R-ID3b accepts.
- **`clang-22` Driver aliases: sound.**
  - Both remaining keys are the C1/C2 aliases of `clang::driver::Driver::Driver`.
  - The literal change (`movq $0;movb $0` becomes `movl $0x646c6c` ("lld"); `movq $3`) matches the parent's `-DCLANG_DEFAULT_LINKER=lld`, and `Driver.cpp.o` alone shows only that change (`driver-v2.json`).
  - The rest is BOLT block layout: PS5 has 427 hot plus 310 cold instructions, C2 has 732 with no cold fragment, and branch senses are inverted (`je` becomes `jne`). That is what BOLT does when the stored profile no longer matches a changed function. The profile was recorded on the PS5 binary, so this function is laid out without it.
  - So the explanation is consistent.
- **"128 binaries differ in `.relro_padding`": incomplete.**
  - In `unclassified-v2.json`, every R-ID1b entry has `instruction_comparison: "not entered: at least one frozen prerequisite failed"`. No per-function comparison was made for any of the 128; only `lld` and `llvm-exegesis` were compared, and they passed.
  - For 114 of the 128, `.relro_padding` (NOBITS, no file bytes) is the only section outside the whitelist. The layout explanation is adequate for those.
  - **For the other 14, `.text` is also outside the whitelist:**

    | Binaries | Other unapproved sections | Likely cause |
    |---|---|---|
    | `libclang-cpp.so.22.1`, `libclang.so.22.1.8`, `clang-installapi` | `.text`, `.rodata`, `.eh_frame` (`clang-installapi` also `.eh_frame_hdr`) | They contain `clangDriver` (x86_64 links Clang statically), so they almost certainly carry the **same `Driver::Driver` code change from the parent's default LLD**, not only a layout shift. Expected and harmless, but the ruling attributes it to build-ID layout. |
    | `lldb-server` | `.text`, `.rodata`, `.eh_frame`, `.eh_frame_hdr` | Unknown. Possibly references across segments after the layout shift. Not shown. |
    | 9 compiler-rt shared runtimes (asan, dyndd, hwasan, hwasan_aliases, memprof, nsan, scudo_standalone, tsan, ubsan_standalone), plus `libomp.so` | `.text`; also `.plt`/`.init` for scudo and `.plt` for libomp | Consistent with displacements to GOT, PLT and data changing after the build-ID note moved the read-only segment. Not shown. |

**Recommendation.** Run the existing R-ID1 per-function comparison, the same one used for `lld` and `llvm-exegesis`, on these 14 before recording the ruling as final. Expected results:
- the compiler-rt runtimes, `libomp` and `lldb-server` are identical after address normalization;
- `libclang-cpp`, `libclang` and `clang-installapi` differ only in the `Driver::Driver` aliases, by the `"lld"` literal and length. They are not BOLT-optimized, so there should be no block-layout change.

Then reword the ruling accordingly. This does not block C2: none of these binaries depends on C2's changes. But the ruling as written claims more than its evidence shows.

## 6. Commit message

The new paragraphs describe the C2 content accurately:
- in-tree component link with the standalone dylib;
- the optional mirror, compiled and defined only for standalone dylib builds;
- runtime flags cleared only standalone;
- architectures, targets and registration check;
- provider version match and Version-Release check;
- LDFLAGS, libdir suffix, debug package note, single merge-fdata install;
- armv7l target list, no python3 Requires.

**Wording and accuracy follow-ups:**
1. **Rewritten bullet subjects.** The bullet list keeps the old local commit hashes (`3abe328e2c30`, `d3f74e4f484d`) but rewrites their subjects. `3abe328e2c30` was "build profiling tools and BOLT for armv7l", and now reads "keep the ARM and BPF targets on armv7l", the opposite of what that commit did. Either drop the hashes, which nobody outside the author's tree can resolve, or present the list as a summary of the squashed content rather than as commit references.
2. **The `compiler-rt` Requires is not mentioned.** The removal of `Requires: compiler-rt` from `bolt` is not in the message. One clause would cover it, for example "and drop the unused compiler-rt runtime requirement from bolt".
3. **The build-id bullet overstates its scope.** "add --build-id=sha1 to toolchain linker flags" covers executables and shared libraries only. MODULE libraries (`LLVMgold.so`, `ompdModule.so`) still have no build ID. Either say "executables and shared libraries", or add `CMAKE_MODULE_LINKER_FLAGS` in a follow-up; that is not a C2 regression.
4. **The trailers** `Signed-off-by: …` ×2 and `Co-Authored-By: Cline SR` are inherited from PS4. Adding one more `Signed-off-by` leaves the tree unchanged, as stated.

## Summary

| # | Item | Class |
|---|---|---|
| 1–4 | C2 content against PS4; in-tree, standalone and packaging behaviour | Correct; no problem found |
| 5 | Ruling text for 14 of the "128" binaries: `.text`/`.rodata`/`.eh_frame` never instruction-compared, and three carry the Driver default-linker change | Evidence gap in the ruling (not in C2): run the per-function comparison and reword |
| 6.1 | Old hashes with rewritten subjects in the message | Wording, but factually misleading for `3abe328e2c30` |
| 6.2–6.3 | `compiler-rt` Requires removal not mentioned; build-id scope | Wording |
| — | aarch64-host standalone build | Not run (uncertain, not a finding) |
