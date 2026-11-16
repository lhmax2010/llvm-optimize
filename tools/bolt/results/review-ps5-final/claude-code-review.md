# Review: PS5 final follow-up (switches, R1, spawn comments)

## Inputs and what I ran

- I reviewed the candidate tree at `temp/ps5-final-109-20261116/source`, commit 92775bc3 (parent 61ef5d31).
  - Its blobs match the diff's post-image (spec 43f0f5d2, helper 5b988002).
  - `baseline-spec.txt` matches the pre-image (6a66edeb).
  - `parent-spec.txt` is byte-identical to 61ef5d31's spec.
- **Spec.** I expanded the spec with the real rpm 4.14.1 in the review build root. I used the same loader, macro path and project macro files as your `parse_switches.py`. Cases:
  - 3 architectures × default, master off, and master off with `_with_clang_bolt 1`;
  - the single switches, alone and combined;
  - `_without_llvm_speedup 0`;
  - master off with `with_clang_bolt 1` and `with_hybrid_link 1` defined directly.
- **Derived macros.** A scratch copy of the spec added an `echo` line in a `%verifyscript` section. It prints the derived macros and whether `__spec_install_post` contains the helper `post` call.
- **Dependency parsing.** I ran the dependency parser of the installed obs-build, `build 20160629-tizen20260814`, on the candidate spec. Variants:
  - a build config with a bare `%define`;
  - a build config with a `Macros:` section;
  - a `--define`.
- **Helper.** I ran the candidate `call()` in real processes:
  - background descendants;
  - ninja 1.13.1 from the Tizen build root;
  - first and second SIGTERM during the new 10 s wait;
  - a session-based variant of the cleanup, as a fix prototype.

I did not run an RPM build. Statements about the BOLT pipeline with hybrid linking off come from reading the code, not from a build.

## Verdict

- The switch logic is correct on rpm 4.14.1.
  - Default expansion is unchanged apart from 12 leading blank lines.
  - With the master switch off, no BOLT or hybrid part can turn on, on any architecture.
  - ARM is unaffected.
  - With everything off, the only differences from the parent are the intended ones.
- R1 is correct for descendants in the leader's own process group.
- Real problems:
  1. **(pre-existing, but it limits R1)** ninja starts every job in its own process group.
     - R1 does not see a straggler left by a ninja job.
     - The existing timeout/cancel cleanup kills ninja but leaves its running jobs alive.
     - I reproduced both. Tracking the session instead of the process group fixes both.
  2. **(small)** The failure path still clears `_ACTIVE_GROUP` after reaping the leader. That is the same PID-reuse window R1 just closed on the success path.
  3. **(documentation/procedure)** A bare `%define _without_llvm_speedup 1` in a project build config does nothing. It must go in the `Macros:` section, or be passed with `--define`.

## a. rpm 4.14 compatibility and switch logic

rpm 4.14.1 defines `bcond_without` as `%{!?_without_X:%global with_X 1}`, and `with` as `%{?with_X:1}%{!?with_X:0}`. Nested `%if` with `%global` only in the true branch works; no `%{expr:}` is needed.

Results from the 4.14.1 expansion (hy/bolt = derived macros; post = the helper `post` call is in `__spec_install_post`):

| Case | hy | bolt | post | Hybrid cmake + assertion | BOLT BR / keeprsp / %install / converter exit |
|---|---|---|---|---|---|
| x86_64 default | 1 | 1 | yes | yes | yes |
| x86_64 master off | 0 | 0 | no | no, `LINK_*_DYLIB=OFF` | no |
| x86_64 master off + `_with_clang_bolt 1` | 0 | 0 | no | no | no |
| x86_64 master off + `with_clang_bolt 1`, `with_hybrid_link 1` | 0 | 0 | no | no | no |
| x86_64 `_without_hybrid_link` | 0 | 1 | yes | no, `OFF` | yes |
| x86_64 `_without_clang_bolt` | 1 | 0 | no | yes | no |
| x86_64 both single switches off | 0 | 0 | no | no | no |
| armv7l / aarch64 default, master off, master off + `_with_clang_bolt` | – | – | no | no | no |
| aarch64 `_with_clang_bolt 1` | 1 | 1 | no | no | no |

- **Default expansion.** It is unchanged: after the leading blank lines, the body is byte-identical to the baseline on all three architectures (50 vs 38 leading blank lines).
- **Gating.** All six former `%{with clang_bolt}` uses now read `llvm_bolt_enabled`, and each is still inside `%ifarch x86_64`:
  - BuildRequires;
  - the ninja `-d keeprsp` line;
  - the `%install` pipeline;
  - the converter exit;
  - the candidate install;
  - `__spec_install_post`.
- **Hybrid parts.** The hybrid cmake options and the readelf assertion read `llvm_hybrid_enabled`, also inside `%ifarch x86_64`.
- **No path where master off still enables anything.**
  - Both derived macros are 0 when the master switch is off, whatever the individual switches say.
  - Every use reads only the derived macros.
- **armv7l/aarch64.** The derived macros can be 1 there (default `hy=1`; `_with_clang_bolt` gives `bolt=1`), but every use is behind `%ifarch x86_64`, so nothing changes. The expanded ARM specs show no difference.

## b. "All off" vs parent

I compared the whole expanded x86_64 spec, not only `%build`. Besides blank lines, there are three differences:

1. **The fixed-flags block** replaces the old `sed` stripping of CFLAGS/CXXFLAGS and also sets LDFLAGS. This is intended.
2. **`--debug-info yes`/`no` on the archive converter.** This is the intended converter check (Part 4).
3. **`Source1200` and `Source1201` stay declared.** This is harmless, and the helper docstring wants it for GBS.

On armv7l/aarch64, only item 3 differs.

The main cmake argv matches the parent's. The hybrid hooks in AddLLVM/AddClang/AddLLD and in the three tool CMakeLists do nothing when `TIZEN_HYBRID_LINK` is unset. I found no option that should have been restored but wasn't.

The design note says the three new cmake options are omitted when hybrid is off, not passed as OFF. That matches the parent.

Stale build directory: if one is reused (for example, incremental gbs builds after a default build), `TIZEN_HYBRID_LINK=ON` stays in CMakeCache. Even then, with `LLVM_LINK_LLVM_DYLIB=OFF` every hook is a no-op, because the interface rewrite returns early and the per-tool changes only matter when linking against the dylib. Harmless, but passing `-DTIZEN_HYBRID_LINK=OFF` in the off branch would make that explicit. The cost is that argv would no longer match the parent exactly.

## c. hybrid_link=off with clang_bolt=on

I found no code dependency.

- **Helper.** It never reads `TIZEN_HYBRID_LINK`, `LLVM_LINK_LLVM_DYLIB` or CMakeCache. Its only DT_NEEDED use is comparing the ordinary and candidate binaries from the same build.
- **clang-22.** It is statically linked in both modes, so the relink edge from `ninja -t commands -s bin/clang-22` has the same shape.
- **BOLT reconfigure.** It reuses the main configure's cache. llvm-bolt and the BOLT libraries do not link to the dylib in either mode.
- **readelf assertion.** It only exists with hybrid on. With hybrid off it would pass trivially, because nothing links to libLLVM.

Not verified: this combination has never been built. Three gates were certified on default builds, as far as I can tell:
- the exact 111-task tool-plan whitelist;
- the profile matching thresholds;
- the real/tiny comparisons.

If ninja's plan or clang-22's code layout differs, those gates fail closed with "unapproved BOLT task" or "profile R/S". That is a build failure, not a wrong product. One real build of this combination would settle it.

## d. How a project disables it

- **Local rpmbuild:** `rpmbuild --without llvm_speedup` (likewise `--without hybrid_link`, `--without clang_bolt`).
- **gbs:** `gbs build --define '_without_llvm_speedup 1'`.
  - depanneur forwards each `--define` to `build`.
  - `build` passes it both to the dependency resolver and to rpmbuild.
  - I confirmed the parser result: BOLT BuildRequires drop out.
- **Project build config** (OBS/Tizen format, or a local file passed with `gbs build -D`): put the macro in the `Macros:` section.
  ```
  Macros:
  %_without_llvm_speedup 1
  :Macros
  ```
  With the installed obs-build:
  - **`Macros:`.** `queryconfig rawmacros` emits this line into the build root's `.rpmmacros`, and the dependency parser drops `python3 >= 3.9`, `xz` and `elfutils`.
  - **Bare `%define`.** A bare `%define _without_llvm_speedup 1` line elsewhere in the config reaches neither rpmbuild nor the dependency parser. The build silently stays on.
  - I did not check the server-side OBS version.
- **The value does not matter**, in rpm and in obs-build alike. `_without_llvm_speedup 0` also disables, because bcond only tests whether the macro is defined. Document this, so nobody writes `0` expecting "on".
- **Checking an actual build log.**
  - The cmake line shows `-DLLVM_LINK_LLVM_DYLIB=OFF` and no `-DTIZEN_HYBRID_LINK`.
  - Neither `TIZEN_HYBRID_LINK_OK` nor `BOLT_PIPELINE_PASS` appears.
  - The `TIZEN_LLVM_NORMALIZED_FLAGS` line is still present.

## e. R1

### What is correct

- **The zombie leader is excluded.** `live_group_members` skips state Z/X unless threads > 1, and the leader stays unreaped as a PGID anchor. A short-lived background child (3 s) gives success after about 3 s.
- **A long-lived background child** in the same group gives this, after 10.06 s:

  `COMMAND_ERROR: command exited successfully with live descendants: process group N still alive: …`

  It then goes through killpg/wait/reap, and no survivors remain.
- **Second SIGTERM during the wait.** `_ACTIVE_GROUP` is still set during the wait, so `record_cancel` kills the group and re-raises. The helper dies by SIGTERM 1.0 s after the first signal, with no survivors.
- **Clearing `_ACTIVE_GROUP` before reaping on success is correct.** After the reap, the PID could be reused, and a late second signal would `killpg` the wrong group.
- **Deferred second signal.** No interaction: `_SPAWNING` is already false when R1 runs.
- **Message matching.** If the text check misses, the error is still raised, as a generic `COMMAND_ERROR`. The risk is only the label, not fail-open.

### Real problem 1: ninja jobs are outside the leader's process group (pre-existing; limits R1)

ninja 1.13.1 from the Tizen build root starts each job with its own PGID, in the same session:

```
PID     PPID    PGID    SID     CMD
529693  2476    529693  529693  ninja -j2 a b
529694  529693  529694  529693  /bin/sh -c sleep 7
529695  529693  529695  529693  /bin/sh -c sleep 7
```

Effects, reproduced with the candidate `call()`:

- **R1 misses ninja-job stragglers.** A ninja rule that leaves `(sleep 40) &` behind returns success in 0.07 s, and the straggler stays alive.
- **Timeout and cancel leave running ninja jobs behind.** The cleanup `os.killpg(process.pid, SIGKILL)` kills only ninja. With a 2 s timeout, all four job processes were still alive after the helper reported TIMEOUT. They had been reparented to the subreaper.
  - The same applies to the cancel path and to `record_cancel`'s second-signal `killpg`.
  - In the spec this concerns the `tool-build` step, `ninja -j %{mlgo_build_jobs} llvm-bolt`, with a 14400 s timeout.
  - The jobs keep compiling into the build tree after the step has failed. I did not check what this does to gbs teardown.

My PS5 review said H2 left no orphaned child. That was true for the children I tested, which stayed in the leader's group, but not for ninja's jobs.

Fix: track the session instead of the process group.
- `start_new_session=True` already makes the leader's PID the SID of every descendant that does not call `setsid()` itself.
- The unreaped zombie leader keeps that PID, so no unrelated session can have that SID.

```python
def proc_stat(path):
    ...
        return pid, fields[0], int(fields[3]), int(fields[17])   # session id, not pgrp

def kill_session(leader):
    for pid, _ in live_group_members(leader):        # now: members of session `leader`
        try: os.kill(pid, signal.SIGKILL)
        except ProcessLookupError: pass
```

Then use `kill_session` in place of `os.killpg` in the cleanup path and in `record_cancel`. In `record_cancel`, catch `Exception`, because the scan can raise.

With this prototype:
- the ninja straggler case fails after 10.15 s with the live-descendants error;
- the ninja timeout case leaves no survivors;
- the plain background case is unchanged.

Better still, repeat kill-and-scan until the session is empty or the deadline passes, so a fork between the scan and the kill is also handled. Descendants that call `setsid()` still escape; no option short of cgroups or a subreaper catches them. Add a regression test with a ninja job or an `os.setpgid(0, 0)` grandchild; the current tests only fork within the same group.

### Real problem 2: the failure path still reaps before clearing `_ACTIVE_GROUP` (small)

- In the cleanup block, `reap_child(process, 1)` runs first, and `_ACTIVE_GROUP = None` only happens in `finally`.
- A second signal in between makes `record_cancel` call `killpg` on a PID that has already been reaped.
- R1 closed exactly this window on the success path.

Fix: in the cleanup block, set `_ACTIVE_GROUP = None` right before `reap_child(process, 1)`. Do it after the kill and the wait, so a second signal during the wait still kills the group.

### Smaller points

- **Cancel latency.** A first SIGTERM during the wait is honored only when the wait ends. I measured 9.1 s after the signal.
  - The exit status is still right: `cli()` returns 128+15 from `_CANCEL_SIGNAL`.
  - The message reads `CANCELLED: … while handling: … live descendants …`.
  - If the group drains in time, `run_step`'s `check_cancel()` catches the cancel.
  - Optional: call `check_cancel()` in the success-path wait. Don't add it to `wait_group_exit` itself, because that function is also used in cleanup, where a raise would skip the cleanup.
- **/proc is now required on every successful call.** Before, only the cleanup path read it.
  - With /proc missing or from another PID namespace, every BOLT step now fails, for example with `COMMAND_ERROR: [Errno 2] … /proc/self/stat`. The `/proc/self/stat` read is outside the try block, so the error is a raw OSError, not a GateError.
  - The night builds logged `BOLT_PROC_OK`, so this is a fail-closed behaviour change, not a regression.
  - The spec still treats `BOLT_PROC_MISSING` as informational. Either make it fatal there with a clear message, or note that BOLT now needs /proc.
- **Matching by message text.** Prefer a typed exception or a return value:

  ```python
  class GroupAliveError(GateError): pass
  # wait_group_exit: raise GroupAliveError('process group %d still alive: ...')
  try:
      wait_group_exit(process.pid, 10)
  except GroupAliveError as error:
      primary = 'COMMAND_ERROR: command exited successfully with live descendants: '+str(error)
      raise GateError(primary) from error
  ```

  `run_step`'s `startswith('TIMEOUT:')` has the same pattern.
- **Cost.** In the normal case, R1 adds one /proc scan per `call()` on success, which is negligible. A false positive needs a descendant that legitimately outlives its parent for more than 10 s. I know of none among the commands the helper runs.

## f. Other

- **The new spawn comments are accurate.** `call()` contains the only `subprocess`/fork/exec site in the helper.
- **The parse test cannot detect a wrong post macro.** In `parse_switches.py`, the "BOLT off" check includes `BOLT_POST_GATE_PASS`. That text is inside the `__spec_install_post` macro body, which `rpmspec -P` never prints, so it cannot fail. Check the macro itself instead, for example with an `echo %{__spec_install_post}` probe as I did.
- **The derived macros can be 1 on ARM** (`llvm_hybrid_enabled` defaults to 1). That is harmless today, but a future use outside `%ifarch x86_64` would turn hybrid on there. Consider computing them inside `%ifarch x86_64`, or naming them `*_x86_64`.
- **Out-of-date text:**
  - The comment `# binutils-devel below also supplies readelf for the hybrid linkage assertion` now applies only when hybrid is on.
  - The helper docstring's "Rollback:" paragraph does not mention `llvm_speedup`.
  - Both are documentation only.

## Summary of requested changes

| # | Kind | Change |
|---|---|---|
| 1 | Real (pre-existing; limits R1) | Track and kill by session, not process group, so ninja jobs are covered by R1 and by timeout/cancel cleanup. Add a cross-group test. |
| 2 | Real (small) | In the cleanup path, clear `_ACTIVE_GROUP` before `reap_child`. |
| 3 | Procedure | Document disabling through `Macros:` or `--define`, not a bare `%define`. Note that any value disables. |
| 4 | Validation | Build `hybrid_link=off`, `clang_bolt=on` once before relying on it. |
| 5 | Optional | Typed exception instead of text match; cancel check in the success-path wait; /proc requirement; parse-test post-macro check; x86_64-only derived macros; comment/docstring updates. |

Probe scripts and outputs are in `/tmp/claude-1000/-home-linhao-Toolchain-development-llvm-optimize/5e8aa240-5caa-4416-a0c4-218f8c1eb336/scratchpad/r14/`:
- `rp/` holds the rpm 4.14.1 expansions;
- `obs/` holds the obs-build dependency-parser cases;
- `probe/` holds the R1 and signal probes;
- `sess-helper.py` is the session-based prototype.
