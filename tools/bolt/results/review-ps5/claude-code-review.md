# Review: H1–H5 + N1 follow-up (clang-bolt-helper.py, llvm-static-archives-native.py, llvm.spec)

## What I reviewed and how

**Inputs.**
- A: `round2/candidate-vs-localPS4.diff` (SHA256 `b4907d04…`).
- B: `round3/N1.diff` (SHA256 `3da50bb1…`), applied on top of A.

**Reconstructing the base.**
- `context/` holds the exact pre-images of the helper (blob `0c101ec17d97`) and the spec (`5a10febabbb3`).
- It does not hold the converter pre-image. `context/packaging__llvm-static-archives-native.py` is blob `fce59f78`, an older version without `log_startup_context()`. I took the converter pre-image `400c062e2a1e` from the local llvm-optimize-bolt git object store.

**Applying the patches.** A and N1 both apply cleanly. The resulting post-images match the diffs' index lines exactly: helper `cf531695c971`, converter `c2f74bfe2d01`, spec `6a66edebc78c`. Both Python files compile.

**Testing.** I ran everything below against these reconstructed files with Python 3.12.3 on x86_64 Linux. I did not run an RPM, gbs or QB build.

## Verdict

I found no real bug in the combined A+N1 result.

- N1 was needed: with A alone, `getsignal()` returning `None` makes `call()`'s `finally` raise `TypeError` (shown below).
- H2 closes the Popen→`_ACTIVE_GROUP` window. In every injection point I tested, the helper died by the signal and the child group was gone.
- H1 and H5 restore SIGCHLD only after the children are reaped.
- H3 preserves the previous path.
- H4 is correct for normal and thin archives.

The remaining items are residual risks that predate this patch, and suggestions.

## 1. H2: deferring the second signal during spawn

### Analysis

**Where handlers run.** Python runs `record_cancel` in the main thread, between bytecodes. The helper creates no threads, and every `call()` site is on the main thread, so `signal.signal()` from the `finally` is legal.

**Signal timing cases.**
- **A first signal during spawn** only sets `_CANCEL_SIGNAL`. Popen completes, then `peek_child_exit()` → `check_cancel()` raises, and the `except` path kills, waits for and reaps the group.
- **A second signal while `_SPAWNING` is set** is stored once; any later ones are dropped. That covers the signal arriving:
  - before the fork;
  - inside Popen;
  - after Popen returns but before `_ACTIVE_GROUP` is set;
  - in the `finally` before `_SPAWNING = False`.

  The `finally` then calls `record_cancel(pending)` with `_SPAWNING` false and `_ACTIVE_GROUP` already published. `record_cancel` sends SIGKILL to the group, sets `SIG_DFL` and re-raises the signal.
- **A signal after `_SPAWNING = False`** takes the immediate path, and `_ACTIVE_GROUP` is already set at that point.

**The PGID is valid when published.** With `start_new_session=True`, the child calls `setsid()` before exec. On success, `Popen` returns only after the exec pipe closes, so the child's PID is already its PGID.

**Popen raising.**
- On exec failure, CPython itself reaps the forked child (`os.waitpid` in `_execute_child`). SIGCHLD is `SIG_DFL` at that point, so the reap works.
- A deferred signal then terminates the helper, and there is no group to kill.

**Re-entrancy of `record_cancel` called from the `finally`.** A handler that runs in the middle of that call takes the immediate path; nothing is deferred because `_SPAWNING` is false.
- If it is the same signal number and arrives after `signal.signal(signum, SIG_DFL)`, it terminates the process directly.
- Either way, the group is killed first whenever `_ACTIVE_GROUP` is set.

**The child's signal mask and dispositions are unchanged.** The design never touches the mask, and Python's handlers reset to default across exec. Measured through `call()`:

| Helper started with | Child `SigBlk` | Child `SigIgn` | Notes |
|---|---|---|---|
| SIGCHLD ignored | 0 | 0 | SIGCHLD reset to default |
| SIGCHLD + SIGINT ignored | 0 | `0x2` | SIGINT stays ignored, matching a plain `subprocess.run` from the same parent |

**Injection test.** I injected real signals with `sys.settrace` at each line of the critical section (helper lines 254–265), plus inside Popen on its success and failure paths. Modes:
- first signal pre-recorded, then the second at each line;
- two real signals at one point;
- second signal deferred, then a third (SIGHUP) at each line from 257 to 265;
- second signal delivered inside Popen after the child exists;
- second signal delivered inside a Popen that then raises `FileNotFoundError`.

Results, recording the child PID from Popen itself:

- Every case where the signal fired ended with the helper killed by it (−15, or −1 for the SIGHUP third signal), and the child was dead within 3 s.
- Some lines emit no trace event in the single-signal mode (259, and 262–264, which run only when a signal is deferred). Those cases fell back to the normal first-signal cancellation; the child was still killed and reaped.
- No run left a surviving child.

**Can a group still be orphaned?** Not through these paths. Remaining risks, none of them introduced here:

1. **Invariant H2 now depends on.** If an exception escapes `Popen` after `fork()` but before Popen returns, CPython neither kills nor reaps the child; its `except:` only closes pipes. Example: an exception raised by a handler during the exec-pipe `os.read`. `call()` never sees the PID, so the group is orphaned.
   - Today this cannot happen. `record_cancel` only returns while `_SPAWNING` is set, and SIGINT has no `default_int_handler` because `cli()` replaces it, so there is no `KeyboardInterrupt`.
   - **Suggestion:** state the invariant in a comment: no handler may raise while `_SPAWNING` is set.
2. **Signal coalescing.** Two identical signals that arrive before the interpreter runs the handler (for example, while the main thread is inside `fork_exec`) produce one handler call. A quick double Ctrl-C can therefore become a graceful cancel instead of a kill. The group is still cleaned up by `call()`. This is a Python limitation and was present before.
3. **Escaped descendants.** Processes that left the group (`setsid`/`setpgid`) are not covered by `killpg`. If the helper itself is SIGKILLed, for example by an outer timeout, its group survives. Both are pre-existing. `PR_SET_PDEATHSIG` would need `preexec_fn`, which was rejected.

## 2. H1 and H5: restoring SIGCHLD

### `call()` (H1)

The restore is in the outer `finally`. Every path that leaves the `try` normally or by exception reaps first:
- success: `reap_child()` before `return`;
- other paths: `killpg` → `wait_group_exit` → `reap_child` in `except BaseException`, before re-raising.

Measured by wrapping `signal.signal` and checking `/proc/<child pid>` at the moment `SIG_IGN` is restored:

| Path | Child still present at restore? | SIGCHLD afterwards |
|---|---|---|
| success | no | `SIG_IGN` |
| rc=7 failure | no | `SIG_IGN` |
| timeout | no | `SIG_IGN` |
| cancel (child sends TERM to the helper) | no | `SIG_IGN` |
| `SystemExit` | no | `SIG_IGN` |
| `KeyboardInterrupt` | no | `SIG_IGN` |

On the second-signal path the process dies by signal and the `finally` never runs, which is acceptable.

**Why early restoration would matter.** On this kernel:
- an existing zombie survives a later `SIG_IGN` and can still be reaped;
- a child that exits while `SIG_IGN` is set is discarded, and `Popen.wait()` returned 0 for `exit 7`.

So an early restore would lose exit codes. It does not happen here, because:
- the only unreaped case is cleanup failure, where the leader is still alive after SIGKILL plus 11 s (D state). Its status has already been abandoned, the error is raised, and under `SIG_IGN` the kernel auto-reaps it later instead of leaving a zombie;
- the helper spawns children only through `call()`, which resets SIGCHLD to `SIG_DFL` before each spawn. No `subprocess`, `os.system` or fork call happens elsewhere while `SIG_IGN` is active.

### `install_main()` (H5)

The outer `try`/`finally` covers:
- argparse `SystemExit`;
- `install()` failures;
- the handler-restore block in `_install_main`.

All children are reaped before it runs:
- Each worker's `run()` reaps its child in `finally` with a blocking `os.wait4`.
- `with ThreadPoolExecutor` waits for all workers, including on exception.
- There is no other `Popen` in the converter.

The only exception is a child stuck in D state. There `os.waitid` blocks and the `finally` is never reached; that hang is pre-existing and documented in `run()`.

For the script itself, the restore happens just before exit and has no visible effect. It matters only for in-process callers such as tests, which is fine.

### N1

Verified. With A alone and `getsignal(SIGCHLD)` forced to return `None`, `call(['true'])` raises `TypeError: signal handler must be signal.SIG_IGN, signal.SIG_DFL, or a callable object` from the `finally`. That error would also replace any exception already in flight.

With N1 the call returns and SIGCHLD stays `SIG_DFL`. That is the only possibility, because a C-level handler cannot be reinstated from Python.

At normal startup `getsignal(SIGCHLD)` reports `SIG_DFL` or `SIG_IGN`, never `None`. So this guards only against C code that installs a handler after startup. The converter receives the same fix.

## 3. H3: `--debugfiles-list`

**Equivalence.** The spec passes `"%{_builddir}/%{buildsubdir}/debugfiles.list"`. The old code computed `Path(ordinary).parent.parent.parent`, which is the same `%{_builddir}/%{buildsubdir}` directory, so behaviour is unchanged. find-debuginfo.sh writes `debugfiles.list` into the build directory it is given; the release override at `llvm.spec:34` passes `"%{_builddir}/%{?buildsubdir}"`.

**Spec quoting and macros.** Both are consistent with the neighbouring arguments in the same `%define __spec_install_post`: double-quoted, inside the backslash-continued body. `%{buildsubdir}` is defined when `%setup` is parsed, so it is set in `%install` even for short-circuit builds.

**Ordering.** The gate runs after `%{__bolt_original_spec_install_post}`, which includes the debug post step, so the list exists when the gate reads it in debug builds.

**Release builds without debug files.**
- The identity has no `debug_file` (it is only added on the `--debug-symbols` path, helper line 836), so `debugfiles_gate` returns `{'required': False}` before touching the path.
- `--debugfiles-list` is `required=True` but is never read there, so the missing file does not matter.

**Uncertain.** Whether Tizen's patched rpm writes the list to that directory in debug builds. This is the same assumption the old derivation made. Evidence: a debug-build log showing `BOLT_POST_GATE_PASS` with `package_list.path` pointing there.

## 4. H4: duplicate `//` tables

**The parser.** Long names are resolved only after the whole scan, using the last `longnames` value. Before H4, a second `//` table silently replaced the first.

**Results.** Tested on `ar` archives without a symbol index, so that inserting a header does not trip the index-offset check first. In each crafted case the second table has the same length as the first but different names.

| Input | Pre-H4 (blob 400c062e) | A+N1 |
|---|---|---|
| normal, long names | accepted | accepted |
| thin, long names | accepted | accepted |
| short names only | accepted | accepted |
| short names + one empty `//` | accepted | accepted |
| normal + second `//` | **accepted, members renamed** (`z_very_long…`, `xnother…`) | rejected: "duplicate GNU ar long-name table" |
| thin + second `//` | **accepted, members renamed** | rejected |
| normal, empty `//` before the real one | accepted | rejected |
| thin, empty `//` before the real one | accepted | rejected |

**Thin archives.** Correct: the `//` table is a special member, so `stored_size = size` and its data is read inline exactly as in normal archives.

**Real tool output.** GNU ar and llvm-ar write at most one `//` table, so no valid archive is rejected.

## 5. Other findings

**Real bugs:** none beyond the N1 one, which is already fixed.

**Already fixed in this base.** The SIGINT labelling problem in `log_startup_context()` that I raised earlier: `default_int_handler` is now reported as "default" and `None` as "non-python".

**Suggestions (style and robustness, not blocking):**

1. Add the invariant comment from section 1, risk 1, next to `_SPAWNING`.
2. `record_cancel(pending, None)` from ordinary code works, but a small named function such as `_honor_second_signal(signum)`, used by both the handler and the `finally`, would make the dual use obvious.
3. A deferred second signal still lets `Popen` run, and the new child is killed immediately afterwards. That is harmless. Skipping the spawn would not close any window, so leave it unless the extra process matters.
4. `debugfiles_gate`'s `require(debugfiles_list is not None)` duplicates argparse `required=True`. It is fine as an API guard; keep both or drop one.
5. Turn the probes above into regression tests:
   - line-by-line signal injection around the spawn;
   - the SIGCHLD restore ordering on all six paths;
   - `getsignal` returning `None`;
   - crafted duplicate `//` and empty-first `//` archives, normal and thin.

   The probe scripts are under `/tmp/claude-1000/-home-linhao-Toolchain-development-llvm-optimize/5e8aa240-5caa-4416-a0c4-218f8c1eb336/scratchpad/r13/probe/` (`h2.py` with `run_h2.py`, `mask.py`, `h1.py`, `n1.py`, `h4b.py`).
6. The `context/` copy of the converter is stale (blob `fce59f78`; the diff's pre-image is `400c062e`). Refresh it so that later reviewers read the right base.
