# Review of Gerrit 361624, patch set 1

Reviewed change: `packaging: split tool subpackages into a standalone llvm-tools-subpkgs spec`.

**Recommendation: request changes.** Building BOLT separately against an installed LLVM is a reasonable objective. PS1, however, also changes the in-tree BOLT linkage used by 361395, leaves the source/installed-LLVM compatibility contract unenforced, and includes unrelated changes to the main LLVM packages. Those should be corrected or separated before treating this as an independent, low-risk tool-package split.

This review distinguishes demonstrated source-level problems from integration risks. I have not demonstrated a duplicate command-line-option crash, an unresolved-symbol link failure, or an ARM package build failure, and do not claim any of those has occurred.

## Material and verification scope

Fetching `refs/changes/24/361624/1` from `https://review.tizen.org/gerrit/platform/upstream/llvm` failed because the endpoint requested credentials unavailable to this session. I read the supplied fallback diff in full:

`/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/hq-review-361395/round2/361624-ps1-own.diff`

Its size is **32,032 bytes**, SHA256 **`cc3639bb6de0afae14ec41eac26741c150c02102b357412eb293d93a49f4dc7d`**.

An existing local evidence repository contained the exact Git objects. I verified that `git diff da885208^ da885208` equals the supplied fallback byte-for-byte:

- PS1 commit: `da885208aeb52f55c448ff46873d242346727522`.
- Parent: `61ef5d31ca91025c414c748477bef0c64ddfa67c`.
- PS1 tree: `6f65022eea40016853aa77bbbbbb87f70f0fc7ce`.

All source line references below refer to the resulting PS1 tree, unless another revision is explicitly identified. I read the entire patch and both resulting spec files, the added X86 source files, and relevant complete BOLT CMake files. I also inspected the corresponding LLVM CMake/export logic, original X86 helper implementations, OpenMP install logic, and analyzer installation rules. For interaction with 361395, I inspected relevant spec/helper portions of the locally available PS4 commit `e9f16ee3c078f9a5ae563ee01e52ace27b28da4d`; this is not a full review of that separate change.

I compared the copied X86 helper bodies with their original implementations, including a whitespace-normalized comparison. I also consulted the LLVM 22.1.8 upstream sources and the CMake/RPM documentation linked below.

No LLVM build, RPM build, package upgrade transaction, installed-library export inspection, or rewritten-program execution was performed. The current environment did not have `cmake`, so an attempted small CMake variable probe could not run; the suffix analysis below follows the source and documented CMake semantics. Actual Tizen macro expansion and installed RPM dependency closure remain to be verified in a clean build root.

## 1. BOLT CMake changes and the in-tree consumer

### F1 — Important: standalone support changes the in-tree BOLT link policy

**Location:** removal of `DISABLE_LLVM_LINK_LLVM_DYLIB` throughout `bolt/lib/*/CMakeLists.txt`, `bolt/tools/*/CMakeLists.txt`, and `bolt/unittests/*/CMakeLists.txt`; representative resulting locations are `bolt/lib/Target/X86/CMakeLists.txt:31–38` and `bolt/tools/driver/CMakeLists.txt:14–20`. The mirror itself is conditional at `bolt/lib/Target/X86/CMakeLists.txt:27–28,43–44`.

The removals are unconditional. With `LLVM_LINK_LLVM_DYLIB=ON`, AddLLVM can therefore substitute the shared LLVM library for the component libraries for an **in-tree** BOLT as well as a standalone one. This is directly relevant to 361395: its PS4 spec enables shared LLVM linkage and adds BOLT in the LLVM build tree, with runtime disabled (`packaging/llvm.spec:403–414,633–634` in that revision).

This changes the tool that rewrites the shipped clang, its dependency graph, and potentially its startup registrations and resource use. It is not just a change to a separately shipped BOLT RPM. Moreover, if missing X86 exports are the reason the standalone mirror is necessary, the same shared-library link mode needs examination in-tree: the mirror is deliberately absent there. The source establishes that mismatch in policy; whether it produces undefined references depends on the actual libLLVM exports and link commands.

**Candidate modification:** retain the old static-component policy in-tree and opt into the new policy only standalone. Define a common argument before adding BOLT subdirectories:

```diff
--- a/bolt/CMakeLists.txt
+++ b/bolt/CMakeLists.txt
@@
 endif() # standalone
 
+set(BOLT_LLVM_LINK_MODE)
+if(NOT BOLT_BUILT_STANDALONE)
+  set(BOLT_LLVM_LINK_MODE DISABLE_LLVM_LINK_LLVM_DYLIB)
+endif()
+
 # Determine default set of targets to build -- the intersection of
```

At **every** site where PS1 removed `DISABLE_LLVM_LINK_LLVM_DYLIB`, restore it as `${BOLT_LLVM_LINK_MODE}`. For example:

```diff
--- a/bolt/tools/driver/CMakeLists.txt
+++ b/bolt/tools/driver/CMakeLists.txt
@@
 add_bolt_tool(llvm-bolt
   llvm-bolt.cpp
 
+  ${BOLT_LLVM_LINK_MODE}
 
   DEPENDS
--- a/bolt/lib/Target/X86/CMakeLists.txt
+++ b/bolt/lib/Target/X86/CMakeLists.txt
@@
   NO_EXPORT
 
+  ${BOLT_LLVM_LINK_MODE}
+
   DEPENDS
```

Applying this only to the driver would be insufficient: the libraries and auxiliary executables must follow a consistent policy. Merely setting a global variable to OFF is also not an exact substitute for the removed per-target argument, which participates in AddLLVM's target handling.

**Side effects:** standalone BOLT keeps the intended shared linkage; in-tree consumers retain their previous policy. If changing in-tree BOLT to shared linkage is intentional, make that a separately documented change and certify it together with 361395 instead of claiming isolation.

**Required validation:** compare the in-tree BOLT dependency closure and expanded link commands before/after; run 361395's dry-run and real-build task gates; then perform the rewrite, installed-clang identity/debug-file checks, and object comparisons using the combined changes. For standalone, inspect the link map and `DT_NEEDED`, and execute every shipped tool.

### F2 — General: clearing runtime flags is also unscoped

**Location:** `bolt/CMakeLists.txt:149–177`, especially the unconditional empty `CMAKE_C_FLAGS` and `CMAKE_CXX_FLAGS` passed to the runtime ExternalProject.

These assignments override environment-derived flags in every runtime-enabled BOLT build. The comment identifies a real reason to remove conflicting ISA options from a freestanding runtime, but clearing everything also discards potentially necessary ABI or target options. Forwarding `CMAKE_SYSROOT` does not reproduce every possible compiler flag.

This does **not** affect the runtime-disabled 361395 path described above. It does change other in-tree runtime-enabled builds.

**Candidate modification:** move the two empty assignments into `extra_args` under `if(BOLT_BUILT_STANDALONE)`, and remove the unconditional assignments from `CMAKE_ARGS`:

```diff
--- a/bolt/CMakeLists.txt
+++ b/bolt/CMakeLists.txt
@@
   set(extra_args "")
+  if(BOLT_BUILT_STANDALONE)
+    list(APPEND extra_args -DCMAKE_C_FLAGS= -DCMAKE_CXX_FLAGS=)
+  endif()
   if(CMAKE_SYSROOT)
@@
-               -DCMAKE_C_FLAGS=
-               -DCMAKE_CXX_FLAGS=
                ${extra_args}
```

Move/rewrite the adjacent comment to describe that scope. For a general-purpose cross-build solution, use an explicit runtime flag policy that retains ABI/target flags and removes only incompatible options; the scope fix alone is not such a policy.

**Side effects and tests:** existing in-tree runtime behavior remains unchanged. Verify the runtime compile command on x86_64 and aarch64, then actually instrument and run a program and collect its profile. Merely linking the optimizer does not test the freestanding runtime.

### Shared libLLVM: feasible, but not automatically certified

Linking BOLT to one matching libLLVM.so is not intrinsically unsafe. A single shared LLVM command-line registry can work. The hazards are mixing static LLVM implementations with the DSO, changed sets of linked static initializers, duplicate option registrations, and reliance on private LLVM interfaces.

I found no demonstrated `cl::opt` collision in this patch. In particular, treating every option name found under `llvm/lib` as a collision would be wrong: the default dylib component construction excludes LLVMTableGen (`llvm/tools/llvm-shlib/CMakeLists.txt:23–26`), so TableGen-only options are not evidence of a runtime collision.

Use link-map inspection plus `--version`, `--help-hidden`, a real rewrite, and an instrumentation/profile run. Test `llvm-bolt`, its aliases, merge-fdata, heatmap, binary-analysis, and bat-dump. These checks cover different linked subsets and registration paths. A successful configure or an `ldd` listing alone does not establish safety.

## 2. X86 mirrors, correctness, and upgrade policy

### Current helper bodies: no mismatch found for the reviewed source

The checked-in `X86GenSubSuperRegisterBody.inc` and `X86GenNeedsAddressSizeOverrideBody.inc` are copied implementation bodies, despite their names; they are not frozen generated opcode-number tables. The instruction, mnemonic, register, and subtarget tables are generated during the standalone build from the source tree using installed llvm-tblgen (`bolt/lib/Target/X86/CMakeLists.txt:8–16`).

The two copied bodies match the corresponding original functions in `llvm/lib/Target/X86/MCTargetDesc/X86MCTargetDesc.cpp:750–941` and `118–169`, respectively, after whitespace normalization. I also checked the short-immediate mapping and the 16/32/64-bit memory helpers in `X86BoltMnemonicTables.cpp:37–92` against the original code. I found no omitted register cases or incorrect current branch in those copies.

That is a source comparison, not proof that locally generated enum/table values match an arbitrary installed libLLVM.

### F3 — Important: installed LLVM and TableGen versions are not bound to the source

**Location:** `packaging/llvm-tools-subpkgs.spec:3,7,10–25,41`; `bolt/CMakeLists.txt:38,47–49`; `bolt/lib/Target/X86/CMakeLists.txt:9–14`; `X86BoltMnemonicTables.cpp:19–33`.

The source version is 22.1.8, but the LLVM compiler, headers/CMake exports, TableGen provider, static archives, and libLLVM BuildRequires are unversioned. The runtime requirement on libllvm is also unversioned. A repository update can therefore supply a different LLVM with the old BOLT source, or upgrade the runtime library after BOLT is built.

This code consumes target-internal headers and generated register/opcode data. A SONAME dependency or a generic assertion that the C++ ABI still links does not certify those internal identities. Possible outcomes include configure/compile failure, link failure, or an executable whose private target data disagrees with the library. I am not asserting that every LLVM patch release changes this data; the defect is that the package does not enforce the compatibility assumption on which it relies.

**Minimum candidate modification:** version the LLVM-family dependencies and reject a mismatched LLVM package at configure time. For example:

```diff
--- a/packaging/llvm-tools-subpkgs.spec
+++ b/packaging/llvm-tools-subpkgs.spec
@@
-BuildRequires: llvm
-BuildRequires: llvm-devel
+BuildRequires: llvm = %{version}
+BuildRequires: llvm-devel = %{version}
@@
-BuildRequires: llvm-static-devel
+BuildRequires: llvm-static-devel = %{version}
@@
-BuildRequires: clang
-BuildRequires: libllvm
+BuildRequires: clang = %{version}
+BuildRequires: libllvm = %{version}
@@
-Requires: libllvm
+Requires: libllvm = %{version}
```

Also check `LLVM_PACKAGE_VERSION` and the selected llvm-tblgen version during standalone configuration. Source backports can change private data without changing 22.1.8, so this minimum needs a documented producer-identity policy: record and certify the LLVM source/configuration and actual provider NEVRs, and either constrain the approved provider EVR or rebuild/requalify BOLT when that provider changes. Do **not** use the tools package's own `%{release}` as though it were necessarily the libLLVM producer's release.

**Side effects:** tighter dependencies can deliberately prevent a tools build or upgrade until a compatible provider is available. That is preferable to silently accepting an unqualified private interface. Independent tool rebuilds are still possible against the same approved LLVM producer.

**Tests:** configure against the approved provider; negative tests with a different LLVM version and a different TableGen; package-manager tests for replacing libllvm while retaining bolt; record source/table hashes and provider identities in build evidence. Where same-version backports are permitted, test that policy explicitly rather than assuming version equality is sufficient.

### Suggestion: determine whether the mirror is needed before maintaining it

**Location:** `X86BoltMnemonicTables.cpp:9–15`, `bolt/lib/Target/X86/CMakeLists.txt:40–44`, and the new spec's `BuildRequires: llvm-static-devel` at line 15.

The comment claims the installed LLVM neither exports these functions nor ships linkable static archives. The new spec explicitly installs the static archives to satisfy imported-target checks. Moreover, the reviewed libLLVM CMake logic defaults to a broad component set. Neither observation proves that every required helper is exported, but the categorical explanation is not supported by the supplied package evidence.

First inspect the **actual installed** library with `llvm-nm -D --defined-only`/`readelf -Ws` and attempt a minimal link for each required helper. If they are exported with the required visibility, use them and remove the redundant mirror. If not, alternatives are explicitly exporting the small required interface from the matching libLLVM, or sharing implementation source through a deliberately maintained common facility. Pulling in a large static X86 archive alongside shared LLVM without inspecting the resulting closure is not a safe shortcut.

If the mirror remains, document it as a version-bound copy, correct the comment, and add parity tests covering register widths/high-byte registers/APX cases, address-size overrides, and mnemonic/short-immediate mappings. Generate the `.inc` tables with the matching TableGen as now; do not replace them with unchecked pre-generated numeric tables. This is primarily maintenance work, not evidence that the reviewed copies are currently incorrect.

## 3. Main llvm.spec changes

### F4 — Important for upgrades: Obsoletes does not complete a package replacement

**Location:** `packaging/llvm.spec:75–84,118–122,631–636`.

The new Obsoletes entries remove old package names without providing those capabilities. A downstream package requiring `llvm-prof-tools`, `llvm-xray`, or `clang-analyzer` can consequently become unsatisfiable. In addition, replacing clang-analyzer with llvm alone does not pull in clang, while analyzer wrappers are owned by the clang subpackage and require a compiler.

This matters if those old packages were distributed. Their actual published versions and dependency consumers were not supplied, so I cannot claim a specific current upgrade transaction already fails. The patch nevertheless claims to implement the replacement, and the metadata does not fully express it. RPM distinguishes Obsoletes from Provides; see the [RPM dependency manual](https://rpm-software-management.github.io/rpm/manual/dependencies.html).

**Candidate metadata repair:** make the profiling replacements capabilities of llvm, and put the analyzer replacement on clang, which already requires the matching llvm package:

```diff
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@
-Obsoletes: clang-analyzer <= %{version}-%{release}
 Obsoletes: llvm-xray <= %{version}-%{release}
 Obsoletes: llvm-prof-tools <= %{version}-%{release}
+Provides: llvm-xray = %{version}-%{release}
+Provides: llvm-prof-tools = %{version}-%{release}
@@
 Requires: llvm = %{version}-%{release}
 Provides: libclang.so.%{version}
+Obsoletes: clang-analyzer <= %{version}-%{release}
+Provides: clang-analyzer = %{version}-%{release}
```

The Obsoletes boundary itself must be chosen from actual previously published EVRs. Separate specs can have different release counters; the new package's release is not automatically a correct migration cutoff. If these package names never shipped, remove the speculative migration metadata and describe that fact instead.

**Side effects/tests:** analyzer replacement now selects clang intentionally; test both explicit old-package installs and a synthetic dependent RPM requiring each old capability, including versioned requirements. Test upgrades from every supported old EVR and check for file conflicts. Verify scan-build, scan-view, scan-build-py and intercept-build in the resulting minimal installation.

There are pre-existing analyzer-content concerns to account for in that test: `llvm.spec:454–455` removes libear/libscanbuild contents, and the scan-view assets are not all in the same runtime subpackage as its launcher. Those are not newly introduced by PS1, so I do not label them new regressions. They do prevent concluding that `Requires: python3` alone establishes a complete analyzer replacement. Also correct the line 76 comment: scan-build itself is a Perl script; scan-view and the Python analyzer tools have Python requirements. A dependency cycle is not inherently forbidden by RPM, although avoiding an unnecessary llvm→clang dependency is a reasonable packaging choice.

### Broader behavior changes that should be separated and measured

**Build IDs — Important integration risk, not a proven build failure.** `llvm.spec:272–274` adds `--build-id=sha1` to the main LLVM executable/shared-library linker flags under `_toolchain`, not just to standalone BOLT and not just to x86_64. This changes build IDs and can change note size/layout relative to the previous linker default. It therefore invalidates an assumption that this commit only adds a tool package or leaves the LLVM binaries byte-identical. SHA1 here is an identifier format, not a security authentication claim.

Candidate: retain the sha1 flags in the new standalone spec and revert their addition to the main spec unless the main LLVM change has its own requirement and evidence. If retained, put it in a separate commit. Validate build-id links, debuginfo lookup and 361395's input/rewrite/debug-file gates on the resulting binaries; do not reuse previous binary hashes as proof. Test all affected `_toolchain` architectures, not just x86_64.

**ARM target expansion — Important cost/scope decision.** `llvm.spec:286–289` changes armv7l from ARM/BPF to ARM/AArch64/X86/BPF. This intentionally increases the LLVM producer's backend set, libraries and build work. It can increase package size and may increase peak link memory on the constrained ARM build. No measurements for that delta were supplied here.

There is a genuine dependency: BOLT's supported target intersection excludes ARM32 (`bolt/CMakeLists.txt:69–89`). Merely enabling an X86 BOLT target against an ARM/BPF-only libLLVM does not solve it. If an ARM-host BOLT that rewrites AArch64/X86 is a requirement, keep the backend expansion as a separate feature with resource and package-content measurements. Otherwise, initially exclude armv7l from the new tool package and keep the producer's target set unchanged. Do not describe this as ARM32 binary-rewriting support.

**DESTDIR — Correct direction.** `llvm.spec:417–425` addresses a real distinction between staging under DESTDIR and overriding a configured install prefix. The OpenMP install script uses DESTDIR for its compatibility aliases; using DESTDIR protects the build environment's `/usr/lib*`. Keep this fix, preferably separately from BOLT support. Verify that installation changes only the staging tree.

Removing staged libgomp/libiomp5 aliases is coherent with a policy that ships only libomp and leaves GNU OpenMP aliases to GCC. However, the GCC explanation does not explain ownership of the Intel-compatible `libiomp5.so` name. State that policy explicitly. The parent spec's libomp file list did not enumerate these aliases, so I have not established removal of a previously shipped alias. Consider configuring `LIBOMP_INSTALL_ALIASES=OFF` instead of creating and deleting them, if that matches the desired platform policy. Test both library-directory layouts and actual RPM ownership, including unchanged static-devel contents.

**MLGO fallback — General incremental-build robustness concern.** `llvm.spec:235–247` tests only directory existence. An interrupted extraction leaves a directory that causes the next build to skip extraction, and an existing directory can contain an older asset set. A fresh normal `%prep` build is a different case and need not be affected. Candidate: keep asset preparation in `%prep`, or extract to a temporary directory, validate the required files and source-archive identity, then publish it atomically; do not equate “directory exists” with “correct assets prepared.” Test an empty directory, interrupted extraction, changed asset archive, and the normal fresh path. Separate this developer incremental-build convenience from the package split.

## 4. New standalone spec

### F5 — General: the hard-coded libdir suffix is wrong for armv7l

**Location:** `packaging/llvm-tools-subpkgs.spec:80,105–106`; `llvm/cmake/modules/LLVMConfig.cmake.in:117`; `bolt/CMakeLists.txt:52–53`.

The new spec sets `LLVM_LIBDIR_SUFFIX=64` for every architecture. The main LLVM spec derives the suffix from `%{_lib}` (`llvm.spec:323`). On armv7l that means the installed LLVM uses `lib`, while the standalone cache requests `lib64`.

There is a subtlety: the generated LLVMConfig line is an unquoted `set(LLVM_LIBDIR_SUFFIX @LLVM_LIBDIR_SUFFIX@)`. For an empty configured suffix, it becomes `set(LLVM_LIBDIR_SUFFIX)`, which unsets a normal variable and can expose the cached `64` again. It does not reliably correct the command-line value. This follows the documented [CMake set/cache lookup behavior](https://cmake.org/cmake/help/latest/command/set.html).

This affects internal library paths and potentially generated RPATHs. Runtime is disabled on ARM and both archive directories are deleted, so I do **not** infer that the current ARM RPM must fail or that its loader necessarily cannot find libLLVM through normal search paths.

**Candidate modification:**

```diff
--- a/packaging/llvm-tools-subpkgs.spec
+++ b/packaging/llvm-tools-subpkgs.spec
@@
 mkdir -p bolt-build
 cd bolt-build
+llvm_libdir='%{_lib}'
 cmake \
@@
-    -DLLVM_LIBDIR_SUFFIX=64 \
+    -DLLVM_LIBDIR_SUFFIX="${llvm_libdir#lib}" \
+    -DCMAKE_INSTALL_LIBDIR="${llvm_libdir}" \
```

**Side effects/tests:** x86_64 retains lib64; armv7l uses lib. Check effective variables after LLVMConfig is included, generated build/install paths, installed RPATH/RUNPATH and the complete manifest on each supported host. Once confirmed, remove the misleading comment and compensating lib64 cleanup for ARM.

### F6 — General: merge-fdata is installed twice, bypassing CMake the second time

**Location:** `packaging/llvm-tools-subpkgs.spec:102,113–116`; `bolt/tools/merge-fdata/CMakeLists.txt:3`; `bolt/cmake/modules/AddBOLT.cmake:8–25`.

The spec says both bat-dump and merge-fdata use `add_bolt_executable` without install rules. This is false for merge-fdata: it uses `add_bolt_tool`, which supplies an install rule. After `ninja install` stages the executable, the manual copy overwrites it with the build-tree binary. That bypasses any install-time RPATH adjustment or other CMake binary installation transformation. Whether the two files happen to match in this configuration requires measurement; the redundant overwrite is unnecessary either way.

**Candidate modification:**

```diff
--- a/packaging/llvm-tools-subpkgs.spec
+++ b/packaging/llvm-tools-subpkgs.spec
@@
-# llvm-bat-dump and merge-fdata use add_bolt_executable which carries no
-# install rule; stage them manually from the build tree.
+# llvm-bat-dump uses add_bolt_executable without an install rule.
+# merge-fdata is installed by add_bolt_tool and must not be overwritten.
 install -p -m 0755 bin/llvm-bat-dump %{buildroot}%{_prefix}/bin/
-install -p -m 0755 bin/merge-fdata   %{buildroot}%{_prefix}/bin/
```

**Side effects/tests:** retain CMake's installed merge-fdata. Compare its dynamic tags and execute it with the build tree removed from access. A non-default LLVM installation prefix is a useful fixture for exposing accidental build-tree paths. Longer term, give bat-dump a proper install rule as well.

### Dependencies and build stages: findings and qualifications

- **llvm-static-devel and libomp BuildRequires are explained by export validation.** CMake imported-target files can check archives/libraries that BOLT does not directly link. Their presence is not proof of accidental static linkage. The spec's later comment claiming static archives are “not installed here” (`:67–69`) contradicts the BuildRequires and should be corrected. Reducing the exported dependency closure is a useful future way to reduce build-root preparation cost.
- **Additional dependency omissions are uncertain.** ZLIB and LibXml2 targets are explicitly created. Other exported LLVM dependencies depend on producer configuration. Test in a clean root rather than a populated development root; inspect the installed LLVMConfig and imported target interfaces for any additional required development packages. I have not established a definite missing libffi, zstd, or linker package from this patch alone. Python is currently pulled transitively by the new llvm runtime requirement; declaring direct tool-use BuildRequires is clearer, but its absence is not itself proof of failure here.
- **ARM runtime OFF is coherent.** BOLT's instrumentation runtime has host/target limitations. An ARM-host optimizer can still manipulate supported non-ARM binaries; do not advertise native ARM32 instrumentation. Verify the intended ARM-host workflows separately, including how the resulting runtime is supplied if instrumentation of another target is expected.
- **Compilation is not confined to `%build`.** `ninja bolt` does not explicitly build bat-dump; `ninja install` normally builds ALL and can compile it during `%install`. This is not evidence that bat-dump is missing from the RPM. For clearer resource and failure accounting, explicitly build every shipped executable in `%build`, then use `DESTDIR=... cmake --install .` without a build in `%install`. The runtime ExternalProject's `BUILD_ALWAYS` also merits inspection when measuring repeated work. Bound Ninja parallelism to a documented memory budget; the main spec already has a job limit, whereas this one uses bare ninja.
- **Debug-package claims need actual macro evidence.** `:52–61` unconditionally disables `debug_package` while asserting Tizen's patched RPM will inject packages and generate debuginfo. That may be correct for the stated GBS mode, but it is not portable RPM behavior and was not verified here. `CMAKE_BUILD_TYPE=Release` plus a sha1 build ID does not itself supply DWARF. In both debug and non-debug project configurations inspect the expanded post chain, produced debug/debugsource RPMs, build-id associations, and symbolization of a real stack. Narrow the comments to the modes actually tested. The reference to linker flags “above” is also misplaced: they appear later.
- **Version literals are a maintenance suggestion, not a present failure.** Use `Source0: llvm-%{version}.tar.gz` and `%setup -q -n llvm-%{version}` rather than repeating 22.1.8. Keep the provider compatibility policy from F3 separate from the tool package's release counter.
- **Aliases are sensible.** Keeping perf2bolt and llvm-boltdiff as symlinks preserves argv[0]-selected behavior and avoids packaging multiple identical ELF instances. Verify the RPM retains links, not copied files, and test all three invocation names.

## 5. Commit structure, evidence, and merge recommendation

### Split this change into reviewable units

The current commit message is principally a list of intermediate commits. It mixes support for a standalone consumer with changes to the LLVM producer and a package migration. I recommend this sequence:

1. **Fix the existing LLVM installation staging:** DESTDIR and an explicit OpenMP alias policy, with a staging-root/manifest test. This is independently useful.
2. **Add standalone BOLT CMake support:** imported dependency targets, a well-scoped shared-link policy, and only the X86 support actually needed after checking exports. Preserve in-tree behavior or explicitly certify its change with 361395.
3. **Add the standalone BOLT spec:** provider version/identity constraints, correct architecture libdirs, complete `%build` outputs, installation, debug packaging, resource limits and runtime tests. This realizes the fast-rebuild goal.
4. **Migrate old tool package names, if they actually shipped:** tested Obsoletes/Provides and complete analyzer runtime ownership/dependencies. If there is no deployed migration, remove that unrelated claim.
5. **Enable ARM-host BOLT through extra producer backends, if required:** separately justify cost, target support and new package contents.

Keep main-LLVM build-ID policy and skipped-`%prep` MLGO extraction in separate commits unless their necessity for one of those units is demonstrated. This avoids making a BOLT tool update depend on unrelated changes to every LLVM binary or the ARM backend set.

### What must be demonstrated before approval

1. **In-tree isolation or explicit combined certification.** With 361395 applied, prove the intended BOLT link mode, dependency closure, task-gate behavior, rewrite results and debug-file identities. Standalone success cannot substitute for this.
2. **Approved installed-LLVM identity.** Bind source, TableGen, headers/configuration and shared-library producer; test mismatch rejection and runtime upgrades.
3. **Clean-root standalone builds.** At least x86_64 and aarch64, plus armv7l if supported. Capture configuration, link maps, RPM dependency/file lists, dynamic tags and runtime/debuginfo smoke tests. Include a release/non-debug configuration, not only the debug-producing GBS mode.
4. **Real package transitions.** If the Obsoletes entries remain, test old package names and their dependents against actual published EVRs. Run analyzer/profiler tools after removing the build root and development-only packages not required by the runtime contract.
5. **Resource and content deltas.** Measure clean-root preparation separately from tool compile/link time. Record peak memory, disk and wall time, especially ARM producer backend expansion and standalone runtime builds. “Minutes” is a plausible objective, not evidence supplied by this diff.
6. **Correctness beyond startup.** Run a rewrite and the rewritten executable; run instrumentation/profile collection where supported; compare representative outputs with the original BOLT built against the same LLVM. Preserve the downstream-clang object and debug identity tests from 361395.

The package split does not inherently change the code generated by an installed clang, but PS1 includes changes to the LLVM producer and to the in-tree optimizer that can change shipped artifacts. Those are the reasons existing LLVM/BOLT evidence cannot simply be carried forward unchanged.

**Final assessment:** request changes to PS1. F1 and F3 are the primary merge concerns: the in-tree policy change is not isolated, and the private LLVM compatibility contract is unenforced. Complete the package migration if applicable, fix the ARM suffix and redundant merge-fdata copy, and separate or explicitly validate the producer-wide changes. The copied X86 implementations themselves show no current source mismatch; shared libLLVM linkage is viable once its exact provider and initialization/link closure are verified. Neither an inherent cl::opt collision nor an inevitable ARM link failure has been established by this review.
