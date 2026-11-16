# Review: LLVM speedup switches and successful-child process-group drain

**Overall:** the nested RPM conditionals are compatible with RPM 4.14.1, the switch truth table is correct for a fresh build, and the process-group change fixes the previously demonstrated successful-leader leak for the helper's supported process-group model. I found no blocking defect in that wait/fail implementation.

There are two packaging qualifications: the hybrid-off branch does not reset hybrid-related settings retained in a reused CMake cache, and the converter's Python minimum should not disappear when BOLT is disabled. Both have concrete fixes below. Neither establishes a failure in a fresh Quickbuild root already supplying a supported Python. Message-text matching is brittle but currently fails closed; replacing it with a typed exception is a maintenance improvement, not a current correctness blocker.

## Scope and evidence

I read the complete supplied product diff and supplied all-off/parent build diff, loaded both complete spec texts, and inspected the relevant spec sections and helper process-control/pipeline code. The supplied helper context is older than the patch preimage, as the request notes. For executable tests I used the exact previously reconstructed helper preimage, verified its blob identity, and applied this diff with exact hunk-context checks in a temporary directory.

Input identities:

| File | Bytes | SHA256 |
|---|---:|---|
| `resume2/final-product.diff` | 5,454 | `7f40a995282ffc31a941c6761bb50402c8353e84e2823128d3816f0cd78cdc5b` |
| `baseline-spec.txt` | 37,013 | `66c5bde9d0ca372ecf0f10bad0813520d19a25843c7306041f39ebc536b402fc` |
| `parent-spec.txt` | 22,040 | `d93a549206434c4512c60d5a96bfeb133b7aaf6ea13b8cd0302e06c1cb99b1c9` |
| `resume2/total-off-vs-parent-build.diff` | 8,910 | `3e25d70c688be4508bf6a80431a9d81fe9982b341e3bdbdd904ff797ddc9597e` |

The common directory for those files is `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/ps5-final-109-20261116/`.

The resulting Git blob identities are:

- `packaging/llvm.spec`: `43f0f5d2e6aa482569fa32c2ede639e75635c743`.
- `packaging/clang-bolt-helper.py`: `5b98800208e3619b7acc83961bcc1e0ab385a55e`.

**Locations below refer to those resulting files**, except explicitly identified parent/context references. No product files were edited.

Validation performed:

- Checked the exact upstream RPM 4.14.1 bcond definitions. The host has RPM 4.18.2, so I explicitly substituted the 4.14.1 definitions of `bcond_with`, `bcond_without`, `with`, and `defined` for the expansion tests. This tests the old macro semantics on the host parser; it is not a claim that I executed Tizen RPM 4.14.1.
- Expanded all eight master/hybrid/BOLT switch combinations for x86_64, armv7l and aarch64, with `_toolchain` initially defined and undefined: **48 combinations**. The fixtures explicitly expanded the final post-install macro, rather than assuming `rpmspec --parse` prints an unused macro body.
- Compared default expansion with the supplied baseline in all six architecture/project-mode cases; separately compared master-off x86_64 `%build` with the parent in both modes.
- Ran real subprocess/group tests on Linux with CPython 3.12.3, including a live descendant after a successful leader, a naturally draining descendant, cancellation during draining, and an injected `/proc` inspection failure.
- Read the installed `gbs build --help` to verify the `--define "X Y"` syntax.

No full LLVM build, RPM build, actual Tizen 4.14.1 post-chain execution, or BOLT-without-hybrid binary certification was performed. CMake was unavailable in this host environment; the reused-cache finding follows the explicit command-line difference and documented cache semantics, not an executed LLVM reconfigure.

## a. Switch logic, RPM 4.14 compatibility, and architecture isolation

### Correct for fresh builds

**Locations:** `llvm.spec:2–18,88–93,417–433,537–575,580–695,717–749,979–989`.

There is no use of `%{expr:...}`. `%bcond_without`, `%bcond_with`, `%global`, `%if`, and `%{with ...}` support this construction in RPM 4.14.1. Its source defines bconds using macro existence, and the derived numeric macros are ordinary values suitable for `%if`. See [RPM 4.14.1 macros.in, conditional-build definitions](https://github.com/rpm-software-management/rpm/blob/rpm-4.14.1-release/macros.in#L88-L133).

For x86_64, the effective policy is:

| Master `llvm_speedup` | `hybrid_link` | `clang_bolt` | Hybrid enabled | BOLT enabled |
|---:|---:|---:|---:|---:|
| 0 | either | either | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 | 1 |

The nested master condition dominates both individual options. Normal `_without_llvm_speedup` input cannot be overridden merely by enabling an individual bcond.

I checked the affected consumers:

| Consumer | Result |
|---|---|
| BOLT-specific xz/elfutils requirements | Under x86_64 and `llvm_bolt_enabled`. |
| Hybrid CMake options | Under x86_64 and `llvm_hybrid_enabled`; explicit LLVM/Clang dylib-link OFF branch otherwise. |
| Ninja `-d keeprsp` | Uses `llvm_bolt_enabled`. |
| Hybrid driver NEEDED assertions | Use `llvm_hybrid_enabled`, inside x86_64. |
| BOLT configure/build/relink/rewrite, snapshot checks and cache release | Inside the x86_64/BOLT-derived condition. |
| Candidate installation | Same BOLT-derived condition. |
| BOLT post-install macro extension | Same condition; absent when disabled. |
| Converter's cancellation-aware shell wrapper | Selected only when the BOLT block defining the wrapper is present; otherwise retains `exit 1`. |
| Fixed flags and archive conversion itself | Remain enabled for x86_64 independently of both speedup options. |

The existing `Source1200`/`Source1201` declarations remain when disabled. Declaring sources is not running BOLT; this does not defeat the switch. Likewise, Python, binutils and other requirements used by LLVM/the converter need not all disappear merely because BOLT is off.

The derived macros are calculated outside `%ifarch`, so `llvm_hybrid_enabled` can numerically be 1 on ARM. That does not activate hybrid linking: every current use is architecture-guarded. Even explicitly requesting the individual BOLT bcond on ARM did not introduce BOLT build or post actions in the expansion matrix. No armv7l/aarch64 functional expansion difference was found.

**Default unchanged:** the expanded baseline and candidate were identical after removal of additional leading blank lines produced by the new definitions. Thus the executable expansion is unchanged by the switch additions; the raw parsed text is not literally byte-identical because of those blank lines. The helper's new group-drain behavior is, of course, an intentional default runtime change.

### P1 — General: switching an existing CMake tree off leaves cached hybrid settings

**Location:** `llvm.spec:418–427`.

The enabled branch writes these cache entries:

```text
TIZEN_HYBRID_LINK=ON
BUILD_SHARED_LIBS=OFF
LLVM_TOOL_LLVM_DRIVER_BUILD=OFF
```

The disabled branch omits all three. Omitting `-D` does not erase a cache entry. Therefore an enabled→disabled reconfigure of the same `build/` directory retains `TIZEN_HYBRID_LINK=ON` and the two forced settings, despite the derived RPM macro being zero. The explicit LLVM/Clang dylib-link OFF options do change the broad link policy, but they do not disable every branch conditioned on the retained Tizen-specific variable or restore every parent default.

This is a real incomplete rollback of cached configuration. It is **not** evidence that a fresh master-off Quickbuild activates hybrid linking, nor proof that a particular cached binary will still have libLLVM in NEEDED. The current expansion tests necessarily cannot detect retained cache values. CMake documents `-D` as creating/updating persistent cache entries and `-U` as removing them in its [command-line reference](https://cmake.org/cmake/help/latest/manual/cmake.1.html#options).

**Candidate fix:** reset the hybrid predicate explicitly and remove the two overrides whose parent behavior is to use defaults:

```diff
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@
     -DLLVM_TOOL_LLVM_DRIVER_BUILD=OFF \
 %else
+    -DTIZEN_HYBRID_LINK=OFF \
+    -UBUILD_SHARED_LIBS \
+    -ULLVM_TOOL_LLVM_DRIVER_BUILD \
     -DLLVM_LINK_LLVM_DYLIB=OFF \
     -DCLANG_LINK_CLANG_DYLIB=OFF \
 %endif
```

Alternatively, document and enforce a fresh CMake build directory whenever the switch combination changes. That is sufficient if mode transitions in a reused tree are intentionally unsupported, but should be stated with the project-disable instructions.

**Side effects:** the proposed commands only affect the hybrid-off x86_64 branch. They make the off-mode expanded command differ from the parent by explicit cache-reset operations in addition to fixed flags; the evidence description must then say “parent defaults restored,” not “only fixed flags differ textually.” Removing a cache override also removes a user's manually cached preference for those two options; that is consistent with a spec-owned mode, but should be intentional.

**Validation:** configure ON then OFF in the same small/LLVM build tree, and compare effective values and resulting link commands with a freshly configured OFF tree. Repeat OFF→ON. Test master-off and individual-hybrid-off. Do not rely solely on string absence in the RPM-expanded command.

### P2 — General, existing gap exposed by off modes: Python 3.9 is not solely a BOLT requirement

**Locations:** `llvm.spec:79–80,88–93,717–737`; previously supplied converter context `packaging__llvm-static-archives-native.py:4,161,650–652`.

The spec retains archive conversion when BOLT is off, correctly, but removes the only explicit `python3 >= 3.9` BuildRequires. The converter's supplied context requires Python 3.9 and uses interfaces such as `str.removesuffix` and `os.waitstatus_to_exitcode`. Unversioned `python3`/`python3-devel` dependencies do not encode that minimum.

This is not a newly introduced converter bug: the old individual BOLT-off mode already had the same dependency gap. The new master-off mode exposes it through another supported configuration. It would fail if a build repository satisfied the unversioned dependencies with an older Python. No such older interpreter was demonstrated in the current Tizen build root, and this review does not claim today's repository actually selects one.

**Candidate fix:** retain the minimum for all x86_64 modes, while keeping xz/elfutils BOLT-specific:

```diff
--- a/packaging/llvm.spec
+++ b/packaging/llvm.spec
@@
 BuildRequires: ninja
 %ifarch x86_64
-%if %{llvm_bolt_enabled}
 BuildRequires: python3 >= 3.9
+%if %{llvm_bolt_enabled}
 BuildRequires: xz elfutils
 %endif
 %endif
```

**Side effects/tests:** default enabled dependency semantics and other architectures remain unchanged; x86_64 off modes now request the interpreter their retained converter needs. Add a dependency-expansion assertion that the minimum remains in every x86_64 combination. Check the current packaged converter's declared minimum when maintaining this dependency; do not infer it solely from the BOLT helper's preflight.

## b. All off versus the parent

**Locations:** supplied `total-off-vs-parent-build.diff`; `llvm.spec:228–357,415–434,537–575`; parent spec `:280–290`.

For a **fresh configuration**, the supplied expanded `%build` difference contains only the fixed-flags policy replacing the parent's sed-based filtering. I independently reproduced a single corresponding diff hunk for x86_64 with `_toolchain` initially defined and undefined. I found no extra residual BOLT/hybrid command later in `%build`.

The restored options match the parent:

- `LLVM_LINK_LLVM_DYLIB=OFF` and `CLANG_LINK_CLANG_DYLIB=OFF`.
- No forced `TIZEN_HYBRID_LINK=ON`.
- No forced `BUILD_SHARED_LIBS=OFF` or `LLVM_TOOL_LLVM_DRIVER_BUILD=OFF`; a fresh build uses the same defaults as the parent.
- Ordinary Ninja invocation, without BOLT's `keeprsp` addition.
- No hybrid NEEDED assertion loop.

Keeping `LLVM_BUILD_LLVM_DYLIB=ON` and `CLANG_BUILD_CLANG_DYLIB=ON` is correct: the parent also builds those libraries. Building a shared library and selecting it for tool linkage are different controls. These ON values are not evidence that the master switch failed.

The fixed-flags policy intentionally includes CFLAGS, CXXFLAGS **and LDFLAGS**; its remaining difference is not limited to an optimization level. It continues to normalize project options and emit warnings. That follows the stated requirement and should be disclosed when describing rollback: this master switch does not restore the entire pre-series build policy or disable O3/ThinLTO/MLGO.

The converter also stays enabled outside `%build`. Accordingly, “all optimizations off” is an imprecise label for this mode. Prefer “hybrid and BOLT disabled; fixed flags, MLGO/ThinLTO and native archive conversion retained.” This is a documentation suggestion, not an additional code defect.

P1 is the exception to fresh-tree equivalence: absence of an option from the command line does not restore its default in an already configured tree.

## c. Hybrid off with BOLT on

**Locations:** `llvm.spec:424–427,580–695`; `clang-bolt-helper.py:677–712,1180 onward,1684–1712` in the reconstructed final helper.

I found no explicit helper or spec requirement that `llvm_hybrid_enabled` must be true when BOLT is enabled. The paths are deliberately independent:

- BOLT still receives its build dependencies, `keeprsp`, tool configure/build steps and final post checks.
- The ordinary link command is captured from the actual clang build, rather than hard-coded to a hybrid link line.
- The rewrite compares the candidate with that build's ordinary clang and installed security baseline.
- RUNPATH adjustment is derived from the ordinary installation. It does not hard-code a requirement to find libLLVM or libclang-cpp in NEEDED; the code handles no path tag on either side as well as matching path-tag kinds.
- The extra BOLT configure command does not turn `TIZEN_HYBRID_LINK` on.

Therefore there is no source-level reason to forbid this combination merely because most existing evidence was collected with hybrid enabled. But macro expansion does **not** certify the resulting binary or task graph. Changing the global linkage mode and restoring the parent LLVM-driver default can change the build graph, tool binaries, link command and resources.

Before advertising the combination as validated, run one fresh hybrid-OFF/BOLT-ON build or equivalent real-tree install rehearsal and retain:

1. Ordinary clang's actual link command and dynamic dependencies.
2. The BOLT dry-run/real-task gate results; reject unexpected ordinary LLVM rebuilds rather than widening the whitelist automatically.
3. Profile matching, rewrite, security, strip/debuglink and installed post checks.
4. Representative ordinary-versus-rewritten object comparisons.

This is an unperformed certification check, not a demonstrated failure or justification to couple the two switches. The additional CMake implementation files of the earlier series were not part of this small follow-up's supplied diff; this review does not newly certify every one of their off-mode branches.

## d. How a project disables it

These inputs must reach RPM **before** the spec's bcond declarations are evaluated.

In the build project's RPM macro configuration, define:

```spec
%define _without_llvm_speedup 1
```

With GBS, whose installed help specifies `--define` in `"X Y"` format:

```sh
gbs build -A x86_64 --define '_without_llvm_speedup 1'
```

With rpmbuild directly:

```sh
rpmbuild -ba packaging/llvm.spec --without llvm_speedup
```

For individual choices, use `_without_hybrid_link 1` or `_without_clang_bolt 1` instead, leaving the master enabled. For example:

```sh
gbs build -A x86_64 --define '_without_hybrid_link 1'
```

On x86_64 this selects hybrid OFF/BOLT ON by default. Defining the master-off macro overrides the effective individual selections.

RPM 4.14 bconds use **existence**, not the numeric value of `_without_*`. `_without_llvm_speedup 0` also disables it; I verified that expansion. Re-enable the default by removing/undefining the `_without_llvm_speedup` definition, not by assigning zero. Do not try to disable this with `with_llvm_speedup 0`: an existing `with_...` macro is true to `%{with ...}`. Avoid setting the internal `with_...` macros in project configuration, particularly alongside contradictory `_without_...` inputs.

Verify the effective spec after project-configuration merging, since another configuration layer can change which macros actually arrive. For mode transitions, use a fresh build tree unless P1 is fixed. No change to the project compiler choice is required to retain the fixed-flags/converter policy.

## e. R1: group drain, cancellation, PID lifetime and errors

**Locations:** `clang-bolt-helper.py:149–185,193–209,254–285,296–325`.

### The new success path is sound within its stated group model

The leader is observed with `waitid(..., WNOWAIT)` before the drain begins, so it remains unreaped. `live_group_members()` excludes ordinary `Z`/`X` entries with no remaining extra threads. Consequently, the leader's own zombie does not consume the ten-second grace period. The extra thread check correctly avoids treating a zombie thread-group leader with remaining live threads as fully drained.

During the wait, `_ACTIVE_GROUP` still identifies the anchored group. A second cancellation therefore retains the existing emergency behavior: kill the group, then terminate the helper by signal. The spawn/deferred-signal mechanism is unchanged by this patch. After the group has drained, clearing `_ACTIVE_GROUP` **before** `reap_child()` is the right order: there is then no live group left to signal, and releasing the leader's PID cannot leave an exposed stale PGID on that success path.

If a descendant is still alive at the drain deadline, the new GateError enters the existing group-kill/wait/reap cleanup because `reaped` is still false. The primary error records that the leader succeeded but the command did not finish its group. The command is not marked completed with rc=0 afterward.

The grace period allows legitimate short-lived descendants to finish without being mistaken for a leak. It does not establish that every descendant exited successfully: the helper has only the direct child's status. A wrapper that intentionally backgrounds work and fails to propagate its exit status remains an invalid build-command contract. This patch does not make such a wrapper reliable.

### Executed process tests

| Scenario | Observed result |
|---|---|
| Successful leader with no descendants | Returned successfully in approximately 0.054 s; no ten-second zombie wait. |
| Successful leader, descendant sleeps 0.15 s then exits | Returned successfully in approximately 0.197 s after drainage. |
| Successful leader, descendant sleeps 60 s | Failed in approximately 10.093 s with `command exited successfully with live descendants`; descendant terminated by SIGKILL. |
| Injected `/proc` enumeration error | Failed explicitly with the original inspection error; was not mislabeled as a successful command. |
| One TERM while a short-lived descendant was draining | Helper exit status 143; leader reaped; descendant finished. |
| Two TERMs while a persistent descendant was draining | Helper terminated by TERM; descendant terminated by SIGKILL. The external test harness reaped adopted processes. |

These tests used real process groups and a test-only subreaper so the deliberately forced-exit scenarios did not leave test zombies. Production code remains a process-group manager, not a subreaper.

### Timing and cancellation qualifications

- The ten-second drain is additional to the child execution timeout. A failed drain can then use the existing cleanup wait/reap deadlines. Do not describe the `timeout` argument as a strict total wall-time limit on `call()`.
- `wait_group_exit()` does not call `check_cancel()`. A first signal during this new grace wait can therefore wait until drainage or the deadline. The first-signal state is still retained and the CLI returns cancellation status; a second signal remains immediate. This is bounded cancellation latency, not a swallowed signal.
- If faster first-signal response is desired, add an optional cancellation check **only for the normal drain call**. Do not add an unconditional check to the shared cleanup wait, because cleanup must continue after cancellation.
- Every successful child now requires `/proc` group inspection. A build root where those process records are unreadable can fail a formerly successful command. That is a consequence of the new fail-closed invariant, not evidence that the inspection error should be ignored. Exercise the gate in the actual Quickbuild/chroot namespace and access policy.
- A process that leaves the process group, a descendant racing adversarially with a `/proc` scan, or uninterruptible kernel sleep is outside an absolute process-tree cleanup guarantee. This patch fixes the demonstrated same-group leak; it does not provide cgroup containment.

### S1 — Suggestion: use a typed timeout rather than recognize message text

**Location:** `clang-bolt-helper.py:177–185,274–281`.

The `startswith('process group %d still alive:' % process.pid)` check currently recognizes the error emitted by `wait_group_exit()`. Other GateErrors are re-raised, so a wording mismatch still fails the step. I found no silent-success path caused by this comparison.

Nevertheless, a later wording change can lose the intended classification, and a typed exception is clearer. A concrete alternative is:

```diff
--- a/packaging/clang-bolt-helper.py
+++ b/packaging/clang-bolt-helper.py
@@
-def wait_group_exit(group, timeout=10):
+class GroupDrainTimeout(GateError):
+    pass
+
+
+def wait_group_exit(group, timeout=10):
@@
-        require(time.monotonic() < deadline, 'process group %d still alive: %s' %
-                (group, ', '.join('%d:%s' % item for item in members)))
+        if time.monotonic() >= deadline:
+            raise GroupDrainTimeout('process group %d still alive: %s' %
+                                    (group, ', '.join('%d:%s' % item for item in members)))
@@
             try:
                 wait_group_exit(process.pid, 10)
-            except GateError as error:
-                if str(error).startswith('process group %d still alive:' % process.pid):
-                    primary = ('COMMAND_ERROR: command exited successfully with live descendants: '+
-                               str(error))
-                    raise GateError(primary) from error
-                raise
+            except GroupDrainTimeout as error:
+                primary = ('COMMAND_ERROR: command exited successfully with live descendants: '+
+                           str(error))
+                raise GateError(primary) from error
```

**Side effects/tests:** `GroupDrainTimeout` remains a GateError, so existing broad error handling and cleanup continue working. Test a typed timeout with changed wording, an unrelated GateError, and an OSError converted by `/proc` inspection. All must fail, with only the timeout classified as live-descendant exhaustion. This is optional hardening; the current text comparison is not a reason by itself to reject the patch.

## f. Other observations and release decision

### S2 — Suggestion: make the SIGCHLD comment precise

**Location:** `clang-bolt-helper.py:252–256`.

Centralizing child creation through `call()` is a useful invariant, and the file has only that Popen launch site. The warning against raising from cancellation handlers during unpublished spawning is also appropriate for the chosen design.

The wording “an inherited SIG_IGN would otherwise turn failed exit codes into 0” is too specific for all waiting APIs. Ignored SIGCHLD can make exit status unavailable; this helper's direct `os.waitid()` path can raise ChildProcessError rather than return zero. Some Popen fallback paths use zero when they cannot retrieve status, which explains the motivation, but the invariant should describe the underlying issue.

Suggested comment-only change:

```diff
--- a/packaging/clang-bolt-helper.py
+++ b/packaging/clang-bolt-helper.py
@@
             # All child processes must be started through call(): it resets
-            # SIGCHLD and reaps children itself; an inherited SIG_IGN would
-            # otherwise turn failed exit codes into 0.
+            # SIGCHLD and reaps children itself; an inherited SIG_IGN can
+            # otherwise discard exit status and defeat reliable failure reporting.
```

No runtime side effect or new test is required for that wording change. Keep the existing ignored-SIGCHLD child-failure fixture.

### Validation to retain

Carry these checks into the maintained suite:

1. RPM 4.14.1 native expansion on the actual platform, including the final post macro, for default, master-off, hybrid-only and BOLT-only modes. The host-parser tests support compatibility but do not replace the platform check.
2. A check that fixed flags and the converter invocation remain in all x86_64 modes, and ARM expansions remain unchanged.
3. Fresh and reused-tree switch transitions, or an explicit fresh-tree-only contract.
4. The R1 process fixtures above, plus cancellation at the new `_ACTIVE_GROUP = None` boundary and restoration of inherited SIGCHLD after normal cleanup.
5. One fresh hybrid-OFF/BOLT-ON pipeline qualification before claiming that combination is empirically certified.

Temporary reconstruction and test artifacts are under `/tmp/codex-review-ps5-final-hi0eg0w7/`, including `macro-results.json` and `group-results.json`. They are review diagnostics, not a claim of completed package certification.

**Final decision:** accept the RPM 4.14-compatible conditional structure and the R1 wait/fail/clear-before-reap implementation. For a fresh Quickbuild root with supported Python, no blocking failure was found in this follow-up. Fix P1 before promising that master-off fully rolls back a reused build tree, or explicitly require a fresh tree; fix P2 to express the converter's off-mode interpreter requirement. The typed exception and comment wording can be follow-up cleanup. The supplied all-off `%build` evidence is accurate for a fresh tree: its remaining functional difference is the intentionally retained fixed-flags policy, not a residual BOLT or hybrid build step.
