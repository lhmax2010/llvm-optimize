# Review: Gerrit 361624 PS1, platform/upstream/llvm (Tizen, LLVM 22.1.8)

"packaging: split tool subpackages into a standalone llvm-tools-subpkgs spec"
Commit da885208aeb5, parent 61ef5d31ca91.

## Scope and evidence

- **Diff reviewed.** Fetching from review.tizen.org failed here because HTTPS needs credentials. I reviewed the provided `361624-ps1-own.diff` instead (SHA256 `cc3639bb6de0afae14ec41eac26741c150c02102b357412eb293d93a49f4dc7d`), together with its recorded commit metadata (da885208).
- **Base files.**
  - `packaging/llvm.spec`: I used a local copy whose git blob ID equals the diff's pre-image, 8240282641a3.
  - 361395 PS4 own diff: read for the interaction questions.
- **Upstream llvmorg-22.1.8 sources.**
  - all of `bolt/`
  - `llvm/lib/Target/X86/`
  - `llvm/lib/Target/CMakeLists.txt`
  - `AddLLVM.cmake`, `LLVM-Config.cmake`, `LLVMConfig.cmake.in`
  - `llvm/tools/llvm-shlib/CMakeLists.txt`
  - `llvm/include/llvm/Support/Compiler.h`
  - `openmp/runtime/src/CMakeLists.txt`
  - the scan-build, scan-view and scan-build-py scripts
- **Published Tizen x86_64 RPMs** `libllvm`, `llvm-devel` and `llvm` 22.1.8-3.1, taken from a local repository cache.
- **Not done.**
  - I built nothing: no in-tree build, no standalone build, no gbs.
  - I had no armv7l, aarch64 or riscv64 build logs.
  - I did not see Tizen's rpmbuild debuginfo implementation, or how the release infrastructure builds a second spec in the same project.
  - Conclusions that depend on these are marked **Uncertain**, with the evidence that would settle them.

## Summary

The change should not be merged in this form. Three problems need fixing first:

1. **P1:** the bolt/ CMake changes also change the in-tree build. Combined with 361395 (x86_64, `LLVM_LINK_LLVM_DYLIB=ON`), the in-tree `llvm-bolt` would link against libLLVM.so and fail with undefined symbols. This happens whichever of the two changes lands second.
2. **P3:** nothing ties the standalone BOLT to the LLVM build it was compiled against. A version mismatch would cause silent mis-decoding or mis-encoding.
3. **P4:** `Requires: python3` on `llvm` adds python3 to every llvm/clang installation. The scripts it is meant for still do not work.

Two parts are sound:

- The X86 mirror is an exact copy of the 22.1.8 code.
- The DESTDIR change fixes a real bug.

The commit should be split (section 5).

| ID | Kind | Topic |
|---|---|---|
| P1 | Real problem, blocking with 361395 | Removing `DISABLE_LLVM_LINK_LLVM_DYLIB` changes the in-tree link |
| P2 | Real problem | Mirror TU is gated on standalone only, so a standalone static link gets duplicate symbols |
| P3 | Real problem | No version pinning between standalone BOLT and the installed libLLVM |
| P4 | Real problem | `Requires: python3` on `llvm`: new dependency, no working tool gained |
| P5 | Real problem (cost) | AArch64 and X86 targets added to armv7l LLVM for a BOLT that cannot optimize armv7l binaries |
| P6 | Real problem if the names were never published | `Obsoletes:` for packages that do not exist in this history |
| S1–S16 | Suggestions | See below |

## 1. bolt/ CMake changes

### P1 (blocking with 361395): the flag removal also changes the in-tree link

Affected: all 16 bolt CMakeLists hunks, for example `bolt/lib/Core/CMakeLists.txt` (old line 41) and `bolt/tools/driver/CMakeLists.txt` (old line 17).

**Mechanism.**

1. The removal is unconditional. In an in-tree build with `LLVM_LINK_LLVM_DYLIB=ON`, `add_llvm_library` and `add_llvm_executable` now pass `USE_SHARED` (`AddLLVM.cmake:754`, `1106-1112`).
2. With `LLVM_DYLIB_COMPONENTS=all`, `llvm_config` then drops every component from the link (`LLVM-Config.cmake:73-95`). `LLVMX86Desc` is no longer linked, and everything must come from libLLVM.so.
3. libLLVM.so does not export X86Desc internals. `llvm/lib/Target/CMakeLists.txt:24-32` sets `CMAKE_CXX_VISIBILITY_PRESET hidden` for every target, "so we don't export all the Target classes in libLLVM.so".
   - I confirmed this on Tizen's `libLLVM.so.22.1` (22.1.8-3.1). It has 41,749 defined dynamic symbols.
   - None of these are among them: `llvm::X86::isNOP`, `isADD`, ...; `llvm::getX86SubSuperRegister`; `llvm::X86_MC::*`; `llvm::X86::getOpcodeForShortImmediateForm`.
   - `X86MCPlusBuilder.cpp` calls them at lines 102, 107, 319, 845, 1682, 1708 and 2682-2686.
4. `X86BoltMnemonicTables.cpp` is compiled only when `BOLT_BUILT_STANDALONE`, so nothing supplies these symbols in-tree.
5. 361395 builds `llvm-bolt` in-tree on x86_64 with `LLVM_LINK_LLVM_DYLIB=ON`. Its own AddLLVM change only affects clang, lld and llvm-ar, so for llvm-bolt it relies on the upstream flag.
   - With 361624 applied, `ninja llvm-bolt` in its `%install` stops with undefined-symbol errors.
   - That fails the x86_64 llvm build, because `clang_bolt` is on by default.
   - Even if the link succeeded, `llvm-bolt` would gain `DT_NEEDED libLLVM.so.22.1`, so it would no longer be the tool 361395 certified.

I did not run this build. The conclusion follows from the AddLLVM logic and the symbol table above.

**Answer to "should they be limited to BOLT_BUILT_STANDALONE?"** Yes, and also to dylib mode. Proposed fix (not built):

```diff
--- a/bolt/CMakeLists.txt
+++ b/bolt/CMakeLists.txt
@@ endif() # standalone
 endif() # standalone
 
+# Upstream links BOLT against LLVM component libraries even when
+# LLVM_LINK_LLVM_DYLIB=ON: libLLVM.so hides target-internal symbols
+# (llvm/lib/Target uses CMAKE_CXX_VISIBILITY_PRESET hidden). Only a
+# standalone build against an installed libLLVM.so links the dylib, and
+# then supplies the hidden X86 helpers itself (X86BoltMnemonicTables.cpp).
+if(BOLT_BUILT_STANDALONE AND LLVM_LINK_LLVM_DYLIB)
+  set(BOLT_LLVM_LINKAGE)
+else()
+  set(BOLT_LLVM_LINKAGE DISABLE_LLVM_LINK_LLVM_DYLIB)
+endif()
+
```

In each of the 16 files, put the line back as the variable instead of deleting it:

```diff
   NO_EXPORT
-  DISABLE_LLVM_LINK_LLVM_DYLIB
+  ${BOLT_LLVM_LINKAGE}
```

**Side effects of the fix.**

- In-tree builds go back to exactly the parent's behaviour.
- A standalone build with the dylib behaves the same as PS1.
- A standalone build without the dylib goes back to upstream behaviour (see P2).

**Tests.**

1. In the 361395 tree with this change:
   - `ninja llvm-bolt` links.
   - `readelf -d bin/llvm-bolt` shows no `libLLVM` `NEEDED` entry.
   - 361395's tool-plan whitelist still matches.
2. Standalone spec:
   - `readelf -d llvm-bolt` shows `libLLVM.so.22.1`.
   - `nm -C --defined-only llvm-bolt | grep 'X86::isNOP'` finds a definition.
   - `llvm-bolt --version` runs.
3. Standalone with `-DLLVM_LINK_LLVM_DYLIB=OFF` links without duplicate symbols. This needs native `libLLVM*.a`, which is the case on x86_64.

### P2: the mirror TU must be gated on dylib mode too

Location: `bolt/lib/Target/X86/CMakeLists.txt:27-29` and `43-45`.

**Failure.** A standalone build with `LLVM_LINK_LLVM_DYLIB=OFF` is supported upstream. In that case:

- `llvm-bolt` links `libLLVMX86Desc.a`.
- `LLVMInitializeX86TargetMC` pulls in `X86MCTargetDesc.cpp.o`, which defines `getX86SubSuperRegister` and the `X86_MC` helpers a second time.
- The link fails with duplicate symbols.

**Fix.** Use the same condition as in P1 for both blocks:

```diff
-if(BOLT_BUILT_STANDALONE)
+if(BOLT_BUILT_STANDALONE AND LLVM_LINK_LLVM_DYLIB)
   list(APPEND LLVMBOLT_TARGET_X86_SOURCES X86BoltMnemonicTables.cpp)
 endif()
 ...
-if(BOLT_BUILT_STANDALONE)
+if(BOLT_BUILT_STANDALONE AND LLVM_LINK_LLVM_DYLIB)
   target_compile_definitions(LLVMBOLTTargetX86 PRIVATE BOLT_STANDALONE_X86_TABLES=1)
 endif()
```

The source-list condition and the `#ifdef BOLT_STANDALONE_X86_TABLES` (`X86BoltMnemonicTables.cpp:27`) gate the same thing twice. One of them is enough.

### Is linking BOLT against libLLVM.so safe?

**cl::opt registration.** I tested this. A probe linked to Tizen's libLLVM.so 22.1.8-3.1 lists 2,024 registered option names. BOLT's sources define 358. None of them collide, so 22.1.8 will not abort with "Option registered more than once".

- BOLT declares two LLVM options `extern` (`RewriteInstance.cpp:75-76`): `X86AlignBranchBoundary` and `X86AlignBranchWithin32BBoundaries`. Both are hidden X86 symbols, but neither is used, so no reference is emitted.
- Visible side effect: `llvm-bolt` now also accepts about 2,000 LLVM options, such as `-print-after-all`. This is harmless, and `HideUnrelatedOptions` keeps them out of `--help`.
- The collision check should be repeated on each LLVM upgrade.

**Static initializers.** These are fine: BOLT's options register in libLLVM's registry, and target registration goes through the exported `LLVMInitialize*` entry points.

**ABI flags.**

- libLLVM exports `llvm::DisableABIBreakingChecks`, and the installed `abi-breaking.h` has `LLVM_ENABLE_ABI_BREAKING_CHECKS 0`, so the link-time ABI guard matches.
- RTTI is ON on both sides.
- The real ABI risk is version skew (P3).

**Other targets.**

- BOLT's AArch64 target uses only inline helpers (`AArch64_AM::`, `AArch64CC::`), so it needs no mirror.
- I found no hidden-symbol uses in the RISCV target.

### Runtime `CMAKE_C_FLAGS=` / `CMAKE_CXX_FLAGS=` (`bolt/CMakeLists.txt:168-173`)

This applies in-tree as well as standalone. For 361395 it has no effect, because that change sets `BOLT_ENABLE_RUNTIME=OFF`.

I think it is right to keep it unconditional, and the commit message should say so. In a Tizen llvm.spec build with the runtime enabled:

- `%build` exports `CXXFLAGS` with `-flto=thin` on x86_64.
- The runtime ExternalProject picks up the environment `CXXFLAGS`.
- The runtime archive would then contain bitcode.

Cost of clearing the flags: the runtime loses `-g` and any prefix-map flags. That is acceptable.

### `find_package(ZLIB/LibXml2 REQUIRED)` (`bolt/CMakeLists.txt:41-46`, standalone only)

- The installed `LLVMConfig.cmake` already runs `find_package(ZLIB)` and `find_package(LibXml2)` without REQUIRED (lines 205-218).
- The original failure was the missing -devel packages. The added lines turn that into an earlier, clearer error.
- Problem: they require both libraries even when the installed LLVM was built without them.

**S1.** Guard them with `if(LLVM_ENABLE_ZLIB)` and `if(LLVM_ENABLE_LIBXML2)`, and fix the comment.

## 2. Checked-in copies of the X86 code

### Correctness for 22.1.8: verified

I compared the copies against upstream llvmorg-22.1.8. Apart from the wrapper line, they are byte-identical:

| Copy | Upstream |
|---|---|
| `X86GenSubSuperRegisterBody.inc` | `X86MCTargetDesc.cpp:752-941` |
| `X86GenNeedsAddressSizeOverrideBody.inc` | `X86MCTargetDesc.cpp:121-169` |
| `isMemOperand`, `is16/32/64BitMemOperand` | `X86MCTargetDesc.cpp:80-115` |
| `getOpcodeForShortImmediateForm` | `X86EncodingOptimization.cpp:452-461` |

- Upstream compiles `is64BitMemOperand` only under `#ifndef NDEBUG`. The copy compiles it always, which is harmless.
- The signatures match their declarations at `X86MCTargetDesc.h:72-88`, `X86MCTargetDesc.h:154` and `X86EncodingOptimization.h:26`.
- The mnemonic tables and register info themselves are not checked in. They are generated from the source `.td` files at build time, which is correct.

### Comment corrections

- `X86BoltMnemonicTables.cpp:11-12` says BOLT links "a reduced LLVM that neither exports them from libLLVM.so nor ships linkable static archives".
  - Every upstream libLLVM.so hides these symbols; this is not something Tizen does.
  - On x86_64 the parent already converts `llvm-static-devel` archive members to native ELF, so those archives are linkable. I did not check what the published repository currently holds.
- The `X86Gen*.inc` file names are misleading. These files are hand copies, not TableGen output, and the standalone build also has real `X86Gen*.inc` files on its include path.
  - **S2.** Rename them, for example to `X86BoltMirror*.inc`.

### Maintenance risk

The risk is silent drift. If upstream changes one of these bodies, nothing fails: BOLT keeps using the old logic while libLLVM's encoder uses the new.

- These functions do change; the R16–R31 cases are additions for APX.
- The worst case is a wrong address-size-override or immediate-form decision with no build error.

### Better ways, ranked by cost

1. **(Cheapest, recommended for this change.)** Keep the mirror, apply P1/P2, and add a configure-time drift check. I tested the check below with cmake 3.31.2 in script mode:
   - against the real 22.1.8 `X86MCTargetDesc.cpp` it passes;
   - after a one-token change to the upstream copy it fails with FATAL_ERROR.

   ```cmake
   # bolt/lib/Target/X86/CMakeLists.txt, inside if(BOLT_BUILT_STANDALONE AND LLVM_LINK_LLVM_DYLIB)
   file(READ "${LLVM_MAIN_SRC_DIR}/lib/Target/X86/MCTargetDesc/X86MCTargetDesc.cpp" _bolt_x86_upstream)
   foreach(_body X86GenSubSuperRegisterBody.inc X86GenNeedsAddressSizeOverrideBody.inc)
     file(READ "${CMAKE_CURRENT_SOURCE_DIR}/${_body}" _bolt_x86_mirror)
     # Drop the provenance comment line and the opening brace.
     string(REGEX REPLACE "^//[^\n]*\n{\n" "" _bolt_x86_mirror "${_bolt_x86_mirror}")
     string(FIND "${_bolt_x86_upstream}" "${_bolt_x86_mirror}" _bolt_x86_pos)
     if(_bolt_x86_pos EQUAL -1)
       message(FATAL_ERROR "${_body} no longer matches upstream X86MCTargetDesc.cpp; re-sync the mirror")
     endif()
   endforeach()
   ```

   To cover the helpers that live in the `.cpp` (`isMemOperand`/`is*BitMemOperand`, `getOpcodeForShortImmediateForm`), move them into `.inc` files and check them the same way.

2. **Export the symbols from libLLVM.so.** This is the "symbols exported by libLLVM.so" option.
   - In Tizen's configuration `LLVM_ABI` expands to `visibility("default")`: the installed `llvm-config.h` defines `LLVM_ENABLE_LLVM_EXPORT_ANNOTATIONS`.
   - The patch would:
     - annotate the five declarations in `X86MCTargetDesc.h` and `X86EncodingOptimization.h` with `LLVM_ABI`;
     - wrap the generated mnemonic-table declarations (`X86MCTargetDesc.h:174`, `GET_X86_MNEMONIC_TABLES_H`) in `#pragma GCC visibility push(default)` / `pop`.
   - Gains: the mirror goes away on every architecture, drift becomes impossible, and an in-tree dylib link of BOLT becomes possible too.
   - Costs:
     - a local patch in `llvm/lib/Target/X86`;
     - one full LLVM rebuild;
     - libLLVM.so exports more symbols than upstream (additive only);
     - BOLT must require a libllvm that contains the patch, so P3 is still needed.
3. **On x86_64, keep the static link.** Keep `DISABLE_LLVM_LINK_LLVM_DYLIB` even when standalone, and link against `llvm-static-devel`, which the spec already BuildRequires. That needs no mirror and matches upstream's design.
   - It needs two pieces of evidence: that the repository's archives contain native ELF members (check `llvm-readelf -h` on one member of `libLLVMX86Desc.a`), and the link time.
   - On arches where the archives are ThinLTO bitcode, a static link means running LTO over the LLVM libraries BOLT uses, which defeats the "minutes" goal.

## 3. llvm.spec changes

### `-Wl,--build-id=sha1` (`packaging/llvm.spec:273-274`)

The change is correct and useful.

- Current Tizen x86_64 binaries have no build-id. I checked `libLLVM.so.22.1`, `llc` and `llvm-tblgen` from 22.1.8-3.1. So today's -debuginfo packages have no `.build-id` links.
- Effects:
  - every ELF gains a 36-byte note;
  - -debuginfo packages gain `.build-id` symlinks;
  - every binary's bytes change, so any stored hash or certified evidence changes too.
- Scope: it is applied only in the `%{_toolchain}` branch. That covers x86_64 always, and other arches only in Toolchain builds.
- **S3.** Also add the flag to `CMAKE_MODULE_LINKER_FLAGS`. Otherwise `LLVMgold.so` (a MODULE library) and any plugins get no build-id.
- **Interaction with 361395.**
  - The `clang-22` link command that 361395 replays comes from `ninja -t commands`, so it picks up the flag automatically.
  - 361395's debug-file checks know a `clang_build_id` kind, but its certified evidence was produced without build-ids.
  - **Uncertain:** whether any of its gates fails. Evidence needed: re-run 361395's validation on top of this flag, and confirm that the BOLT-rewritten `clang-22` and its debug file carry matching build-ids.

### P4: `Requires: python3` on `llvm` (`packaging/llvm.spec:79`)

This adds a hard runtime dependency to `llvm`, and through `clang` (`Requires: llvm = ...`) to every clang installation and every build root that installs clang. Today's auto-generated requirement is only `/usr/bin/env`, because the scripts use `env` shebangs.

The tools the dependency is meant for still do not work:

- `analyze-build`, `intercept-build` and `scan-build-py` use `#!/usr/bin/env python3`. They import `libscanbuild`, which this spec deletes (`rm -rf %{buildroot}/usr/lib/libscanbuild/*`; the 3.1 RPM contains no `libscanbuild`).
- `scan-view` uses `#!/usr/bin/env python`, not `python3`, and needs `share/scan-view`, which is not shipped.
- `scan-build` is a Perl script (`#!/usr/bin/env perl`). The new comment calls scan-build a Python script, which is wrong.

**Fix.** Drop the line. If the analyzers are wanted, ship `libscanbuild`, `libear`, `share/scan-build` and `share/scan-view` in a subpackage that requires python3 and perl.

**Uncertain:** whether Tizen build roots already contain python3 for other reasons. If they do, the cost is image size on devices rather than build-root size.

### P6: Obsoletes (`packaging/llvm.spec:82-84`)

- `clang-analyzer`, `llvm-xray` and `llvm-prof-tools` do not exist in the parent.
- The tools spec is created by this very change, and in its final form it builds only `bolt`. These names existed only in the squashed intermediate commits.
- If they were never published, the lines do nothing useful. They also make any future subpackage with one of these names, at the same or a lower EVR, get removed when `llvm` is installed.
- **Evidence needed:** were any of these packages ever published to a Tizen repository? If not, remove the lines.

### %files edits

- `intercept-build` moves within `%files` (llvm).
- The six `libexec` analyzer entries move within `%files -n clang`. In the base they are already in `%files -n clang`, lines 619-624.

Both are pure reorders inside the same section with no effect.

**S4.** Drop them to reduce churn and conflicts.

### P5: AArch64 and X86 targets on armv7l (`packaging/llvm.spec:288`)

**Cost.** This grows libLLVM.so, clang and the static archives on armv7l with two complete backends, on what is already the slowest architecture (the spec sets `QEMU_RESERVED_VA` there). It adds compile time and raises 32-bit address-space and memory pressure during the ThinLTO links.

**Benefit.** BOLT cannot optimize ARM32 binaries. An armv7l `llvm-bolt` could only rewrite x86_64 or aarch64 binaries, which has little use on armv7l devices. BOLT on a 32-bit host is also not something upstream tests (**Uncertain**; no armv7l build or run log seen).

**Fix.** Revert the targets line and add `ExclusiveArch: x86_64 aarch64 riscv64` to the tools spec.

If armv7l must stay, attach evidence for armv7l before and after:

- build time and peak memory;
- libLLVM.so size;
- an armv7l `llvm-bolt` smoke run on an aarch64 or x86_64 test binary.

### DESTDIR install and libgomp/libiomp5 removal (`packaging/llvm.spec:419-425`)

This is a correct fix for a real bug.

- `openmp/runtime/src/CMakeLists.txt:428-447` creates the `libgomp` and `libiomp5` links in `"$ENV{DESTDIR}${outdir}"`.
- `outdir` is computed at configure time from `CMAKE_INSTALL_PREFIX=/usr`.
- With the old prefix override (`-DCMAKE_INSTALL_PREFIX=%{buildroot}/usr -P ...`), the links went to the build host's real `/usr/lib64`, or failed silently.
- If they were created there, the build root's `libgomp.so.1` pointed at libomp for the rest of the build.

Package contents should not change: the links were never packaged before, and now they are created in the buildroot and removed.

**S5.**

- The comment says `/usr/lib`; on 64-bit it is `/usr/lib64` (`%{_libdir}`).
- `-DLIBOMP_INSTALL_ALIASES=OFF` would avoid creating the links at all. That changes the CMake cache, though, which matters for 361395's certified configuration, so the `rm` approach is the safer choice.
- Please attach an `rpm -qlp` comparison of all subpackages before and after. With DESTDIR, any other `install(CODE)` that used configure-time paths now writes into the buildroot.

**Conflict with 361395.** 361395 keeps the old install line as hunk context, so whichever change lands second needs a rebase. 361395's install-manifest copy and buildroot snapshots should keep working, but re-run its validation.

### MLGO assets in %build (`packaging/llvm.spec:235-247`)

- It is correct for short-circuit or incremental builds where `%prep` was skipped.
- It costs nothing in full builds, because the directory already exists.

**S6.**

- Add `|| exit 1` to each `tar`. The spec itself notes that `%build` does not guarantee `set -e`, so a failed extraction would surface later as a less clear configure error.
- Consider one macro shared by `%prep` and `%build`.
- This is unrelated to the tools split; see section 5.

## 4. The new spec (`packaging/llvm-tools-subpkgs.spec`)

### P3: no version pinning

Locations:

- unversioned dependencies: lines 10-11, 15, 24 and 41;
- hard-coded version: line 3 (`Version: 22.1.8`), line 7 (`Source0`) and line 50 (`%setup -n`).

**Why it matters.**

- Standalone BOLT compiles X86, AArch64 and RISCV opcode and register enums by running TableGen on the tarball's `.td` files.
- It then runs against whatever libLLVM.so is installed: the disassembler and MCInstrInfo tables come from the library.
- If the two differ, BOLT decodes or encodes with mismatched opcode numbers, and nothing reports an error.
- Nothing ties the two together today:
  - `BuildRequires: llvm-devel` and `Requires: libllvm` are unversioned;
  - the auto-generated `libLLVM.so.22.1()(64bit)` requirement pins only the SONAME;
  - `Version` is hard-coded independently of the installed LLVM.

**Fix (minimum).**

```diff
-BuildRequires: llvm
-BuildRequires: llvm-devel
-BuildRequires: llvm-static-devel
+BuildRequires: llvm = %{version}
+BuildRequires: llvm-devel = %{version}
+BuildRequires: llvm-static-devel = %{version}
@@ %package -n bolt
-Requires: libllvm
-Requires: compiler-rt
+Requires: libllvm = %{version}
@@ %build
+llvm_installed=$(sed -n 's/^set(LLVM_PACKAGE_VERSION \(.*\))$/\1/p' %{_libdir}/cmake/llvm/LLVMConfig.cmake)
+test "$llvm_installed" = "%{version}" || { echo "installed LLVM $llvm_installed != %{version}" >&2; exit 1; }
```

Notes on the fix:

- The installed `LLVMConfig.cmake` contains `set(LLVM_PACKAGE_VERSION 22.1.8)`.
- Pinning `= %{version}` matches any release of 22.1.8. It does not catch a Tizen patch to a `.td` file within the same version.
- For an exact match, either rebuild this package whenever llvm changes, or require the build-time EVR, for example a macro set from `rpm -q --qf '%%{VERSION}-%%{RELEASE}' libllvm`. Check that the macro does not break spec parsing outside the build root.
- **Uncertain:** whether Tizen's infrastructure rebuilds this spec automatically when llvm changes. Evidence needed: the project's build configuration.

**Side effects.** Building fails early when the repository's LLVM is a different version. That is the intended behaviour.

### armv7l handling

- **`-DLLVM_LIBDIR_SUFFIX=64` (line 80) has no effect.** `find_package(LLVM)` runs the installed `LLVMConfig.cmake` in the caller's scope, and that file sets `LLVM_LIBDIR_SUFFIX` itself (line 253 on x86_64: `64`).
  - On every architecture the installed value wins, so the libraries go to `%{_libdir}`.
  - The second `rm` (line 106) never matches anything, and its comment is wrong.
  - **S7.** Remove both.
- **`-DBOLT_ENABLE_RUNTIME=OFF` on armv7l (lines 86-88)** repeats the CMake default and is harmless.
- **The runtime `%files` entries (line 128) use `%ifnarch armv7l`,** but CMake builds the runtime only on x86_64, aarch64 and riscv64.
  - If this project builds i586 or i686 (the base spec mentions i686), `%files` lists runtime files that were never built, and the build fails.
  - **S8.** Use the positive list `%ifarch x86_64 aarch64 riscv64` in `%files`, and pass `-DBOLT_ENABLE_RUNTIME=ON/OFF` under the same condition so the two cannot disagree.
- See P5: I recommend not building this spec for armv7l at all.

### Debuginfo

The spec defines `%define debug_package %{nil}` (line 61) and claims that Tizen's patched rpmbuild still produces `bolt-debuginfo` and debugsource packages.

- **Uncertain.** I could not check Tizen's rpmbuild.
- Evidence needed: the RPM list from a gbs build of this spec, showing `bolt-debuginfo` with `/usr/lib/debug/.build-id/*` entries for `llvm-bolt`. Also the failure you get without the `%define`.
- **S9.** The comment says "the -Wl,--build-id=sha1 linker flags above", but the flags are in `%build`, below it.

### Hard-coded Version

- The version appears in four places: `Version`, `Source0`, `%setup -n`, and the mirrored code.
- **S10.** Define it once (`%define llvm_ver 22.1.8`) and rely on the P3 check to catch skew.

### Other issues in the new spec

- **S11: `Requires: compiler-rt` on `bolt` (line 42) is not needed at runtime.** The instrumentation runtime is BOLT's own `libbolt_rt_instr.a`, shipped in the same package.
- **S12: contradictory comments.**
  - `%build` (lines 66-69) says `llvm-static-devel` "is not installed here", but line 15 BuildRequires it.
  - Line 15's comment and the source comment disagree about whether the archives are usable.
  - Cost note: `llvm-static-devel` is about 0.5 GB installed (520,487,208 bytes in a local x86_64 22.1.8-1 build) and enters every build root of this spec.
- **S13: the explicit linker flags (lines 83-84) replace `$LDFLAGS`.** CMake initializes `CMAKE_*_LINKER_FLAGS` from `LDFLAGS` only when they are not given on the command line, so the distro's `-z relro` and `--as-needed` are dropped.
  - Use `"$LDFLAGS -Wl,--build-id=sha1"`, unless dropping them is deliberate (llvm.spec does the same).
- **S14: build targets and install comments.**
  - `ninja bolt bolt_rt` (lines 93-97) does not build `llvm-bat-dump`; it gets built during `%install` by `ninja install`. Run plain `ninja` in `%build`.
  - `merge-fdata` uses `add_bolt_tool`, not `add_bolt_executable`, so `ninja install` already installs it. The comment at lines 113-114 is wrong; the extra `install` line is harmless.
  - Alternative: `ninja install-bolt install-bolt_rt`, which avoids installing and then deleting `libLLVMBOLT*.a`.
- **S15: Tizen packaging conventions.**
  - The `%files` section has no `%manifest`, unlike the base spec.
  - The `%description` describes tools that this spec no longer ships.
  - `License: NCSA` copies the base spec, but LLVM is Apache-2.0 WITH LLVM-exception. That is a pre-existing problem.
- **Uncertain: multi-spec builds.** Does Tizen's release and pre-build infrastructure build a second spec in this project, and does it order it after `llvm`? Evidence needed: the project's build configuration or a pre-build log listing both packages.

## 5. Should the commit be split?

Yes. The squashed message lists nine intermediate commits whose descriptions no longer match the final content. For example, "move tool subpackages to a standalone spec" now ships only `bolt`, and several intermediate steps were later reverted.

Suggested series, each one buildable on its own:

1. **packaging: install with DESTDIR; do not ship libgomp/libiomp5 links.** A standalone bug fix, and the only part with no BOLT dependency. It needs a rebase against 361395.
2. **packaging: add --build-id=sha1 to toolchain linker flags.** Include `CMAKE_MODULE_LINKER_FLAGS`, and coordinate with 361395's validation.
3. **packaging: extract MLGO assets in %build when %prep was skipped.** Add the `|| exit 1`.
4. **bolt: standalone build against an installed libLLVM.so.** The CMake gating (P1/P2), ZLIB/LibXml2, the runtime flags and the X86 mirror with its drift check.
   - It must not change the in-tree build.
   - It is a candidate for upstream submission, minus the mirror.
5. **packaging: add llvm-tools-subpkgs.spec (bolt).** With version pinning (P3), `ExclusiveArch`, and the fixes in section 4.
6. **Drop, or justify separately:**
   - the armv7l targets (P5);
   - `Requires: python3` (P4);
   - `Obsoletes` (P6);
   - the `%files` reorders (S4);
   - the "scan-build needs clang" comment.

**S16.** Write a commit message that describes the final content of each commit rather than the history of the series.

## Tests I ran

1. **Mirror versus upstream 22.1.8:** I extracted the added files from the diff and compared them with llvmorg-22.1.8. They are identical apart from the wrapper line; the line ranges are in section 2.
2. **Tizen libLLVM.so 22.1.8-3.1 symbols:**
   - 41,749 defined dynamic symbols.
   - None of the mirrored X86 symbols, and no `X86_MC`, `X86InstrInfo` or `X86Subtarget` symbols.
   - General MC, DWARF and Object APIs are exported.
3. **cl::opt collisions:**
   - I compiled a probe with the 22.1.8-3.1 llvm-devel headers, linked it to that libLLVM.so, and printed the registered options. (The host lacks `libxml2.so.16`, so I used a stub that only satisfies symbol binding; no XML code ran.)
   - It listed 2,024 unique option names.
   - A source scan of BOLT found 358 option names. The overlap is 0.
4. **Drift check:** cmake 3.31.2 in `-P` mode. It passes on 22.1.8 and fails with FATAL_ERROR after a one-token change to the upstream copy.
5. **llvm 22.1.8-3.1 RPM:**
   - the analyzer script shebangs are as listed in P4;
   - there is no `libscanbuild` and no `share/scan-*`;
   - the auto-generated requirements include `/usr/bin/env` but not python3.
6. **Build-ids:** none present in `libLLVM.so.22.1`, `llc` or `llvm-tblgen` from 22.1.8-3.1.

Not run: any LLVM or BOLT build, gbs build, armv7l, aarch64 or riscv64 test, or 361395 validation on top of this change.
