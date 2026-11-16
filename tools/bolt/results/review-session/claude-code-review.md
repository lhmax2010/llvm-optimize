# Review: session-based process tracking in clang-bolt-helper.py

## What I reviewed and ran

- **Commits.** Task 111 exists, so I reviewed commit 378f8d5c (tree ad3898ff, parent 61ef5d31).
  - Its helper differs from 110 (56902c58) by one comment only.
  - Its spec differs from 110 in two places: `BuildRequires: python3 >= 3.9` is now unconditional on x86_64, and the hybrid-off branch adds `-DTIZEN_HYBRID_LINK=OFF -UBUILD_SHARED_LIBS -ULLVM_TOOL_LLVM_DRIVER_BUILD`.
  - The 110 `final-product.diff` matches 92775bc3→56902c58 exactly.
  - I compared the helper against the 109 version (5b988002).
- **Real-process probes** against the 111 helper, on Linux 6.17 with Python 3.12. The build root has Python 3.14; I did not run there.
  - **Earlier cases:** a short and a long background child, a ninja straggler, a ninja timeout, and a first or second SIGTERM during the success-path wait.
  - **Adversarial cases:** I gave the helper module an `os` object whose `kill(pid, SIGKILL)` fails for one chosen member. That member sits in its own process group, like a ninja job. The kill either raises EPERM or does nothing, the latter simulating a D-state process. I combined this with timeout, a second signal, a third signal, and SIGTERM every 0.3 s.
- **rpm 4.14.1 expansion of the 111 spec.**
  - Default x86_64: identical to 109 apart from blank-line position, caused by the BuildRequires reorder.
  - Master off: the cmake line shows the three new options.

I did not run an RPM build.

## Verdict

The design is right. The SID really is pinned on every path that scans or kills.

All earlier cases pass with no survivors, including both ninja cases that failed with 109. The new typed `LiveDescendantsError` replaces the text match.

Real problems:

| # | Severity | Problem |
|---|---|---|
| A | medium-low | One member that cannot be signalled (EPERM) aborts the whole kill loop, so other killable members survive. |
| B | low | Repeated signals restart the 1 s kill pass in nested handlers, so termination can be postponed indefinitely. |
| C | very low | `reaped` is set after a `require` that runs after the reap, so one theoretical path kills by a SID that is no longer pinned. |

The rest are suggestions.

## 1. SID pinning

Yes, on every path that scans or kills.

**The kernel guarantee is stronger than "while the leader is unreaped."**
- The PID number is released only when no task uses it as a PID, a PGID or a SID. In `kernel/pid.c`, `__change_pid()` returns early while `pid_has_task()` is true for any type, and only then calls `free_pid()`.
- So the number cannot be handed to a new process while either the leader zombie exists or any process still has that SID.
- The PID allocator is also cyclic (`idr_alloc_cyclic`), so a freed number comes back only after wraparound. On this host `pid_max` is 4194304.

**The leader stays unreaped on every path where `_ACTIVE_GROUP` (now the SID) is set.**
- It is set only after `Popen` returns, and cleared before both `reap_child` calls and in `finally`.
- Nothing else reaps:
  - SIGCHLD is reset to `SIG_DFL` in `call()`;
  - the helper has no threads, no `os.wait()`/`waitpid(-1)`, and no `Popen.wait/poll/communicate`;
  - `subprocess._cleanup()` only reaps abandoned Popen objects, and ours is still referenced.
- `peek_child_exit` uses `WNOWAIT`.
- The deferred second-signal replay runs right after `_ACTIVE_GROUP = process.pid`, or with `None` when `Popen` raised; in that case Popen has already reaped the failed child.

**When cleanup gives up on a D-state member** and the code then reaps the leader, the SID stays pinned by that member, so there is still no reuse.

**The only exception is problem C.** On the success path, `require(reap_child(process) == rc, …)` reaps first and sets `reaped = True` only after the check. If the check failed, the cleanup would call `killpg(sid)` and scan a SID that could, in theory, be free. The session had been verified empty just before, and the two statuses cannot differ in practice. Fix it anyway:

```python
_ACTIVE_GROUP = None
reaped_rc = reap_child(process)
reaped = True
require(reaped_rc == rc, 'child exit status changed while reaping')
```

The same ordering exists in 109.

**Other details.**
- `killpg(sid)` is safe for the same reason: the leader's group number equals the SID and is pinned.
- On a zombie-only group it raises `ProcessLookupError`, which is caught.
- The `/proc/self/stat` PID check keeps the scan consistent with the helper's PID namespace.

## 2. Per-PID SIGKILL and PID reuse

**How likely?** Extremely unlikely, though not impossible by construction.
- The window between reading a member's stat and `os.kill` is at most one scan. That is 28 ms here, with 2944 processes.
- For a wrong kill, the member must exit and be reaped inside that window. Its number must also be unpinned: not a live PGID or SID, so not a ninja job's `sh` while that job still has live children.
- Then the allocator must wrap all of `pid_max` in the same window. With `pid_max = 4194304` that takes minutes even at 10k forks/s. The kernel default of 32768, which some containers have, still needs seconds.

**Safer options**, all available on Python 3.9 and Linux:

1. **`killpg` on each distinct PGID seen in the session** — recommended as the primary method; no extra kernel requirement.
   - Process groups cannot span sessions, because `setpgid` requires the same session. So a PGID observed in our session can only contain our processes while that group exists.
   - The group number stays pinned while any member lives.
   - `killpg` is atomic per group, and it also catches members forked into that group after the scan.
   - The scan already reads the PGID.
   - The residual risk is the same wraparound as above, and only if the whole group exits inside the window.
2. **pidfd**, for an exact per-process kill:
   ```python
   fd = os.pidfd_open(pid)                      # Python 3.9, Linux 5.3
   try:
       if proc_stat('/proc/%d/stat' % pid)[4] == sid:   # verify after pinning
           signal.pidfd_send_signal(fd, signal.SIGKILL) # Python 3.9, Linux 5.1
   finally:
       os.close(fd)
   ```
   - Opening first, then checking, is race-free.
     - If the number was reused before `pidfd_open`, the stat check sees a foreign session and skips it.
     - If the number is reused after the open, `pidfd_send_signal` fails with ESRCH and nobody is hit.
   - Fall back to options 1 and 3 on `AttributeError`, or on `OSError` with ENOSYS/EPERM. seccomp profiles in some containers block `pidfd_open`.
3. **Plain `os.kill`** as the last fallback, as now.

The current code is acceptable in practice. Option 1 is a small change and also makes the loop converge faster.

## 3. Scan and kill inside the signal handler

- **The basics hold.** Python runs handlers in the main thread between bytecodes. The scan keeps no shared state, so running it while the main thread is itself inside a scan or `kill_session` is safe.
- **Exceptions are caught.** `try/except Exception` covers everything the handler can raise from the scan or kill:
  - `GateError`, `LiveDescendantsError` and `OSError`;
  - a raw `FileNotFoundError` for `/proc/self/stat`, which is read outside the inner try.

  SIGINT goes to `record_cancel`, so no `KeyboardInterrupt` can come from it.
- **Deferred logic is unaffected.** While `_SPAWNING` is set the handler only records the signal. The replay after `Popen` runs `kill_session` in normal context, then re-raises with `SIG_DFL`.
- **The 1 s bound holds for a single second signal.** With an unkillable member, the helper died 1.0 s after the second SIGTERM, measured on the 10 s cleanup path.

**Problem B: re-entrancy.**
- A third signal arriving during the handler's `kill_session` runs `record_cancel` again, nested. It starts a fresh 1 s pass, then kills the process.
- Each further signal extends termination by up to 1 s.
- **Measured:** an unkillable member plus SIGTERM every 0.3 s kept the helper alive for the whole 8 s of signals. It died 0.9 s after they stopped.
- Each nesting also adds Python stack frames. Under sustained signals this would eventually raise `RecursionError`, possibly outside the `try`.
- It needs both an unkillable member and a supervisor that keeps re-sending, so the severity is low.

Fix: make the immediate-termination path run once.

```python
_TERMINATING = False
...
        if _TERMINATING:
            return                      # the first termination pass is already running
        _TERMINATING = True
        if _ACTIVE_GROUP is not None:
            try: kill_session(_ACTIVE_GROUP, 1)
            except Exception: pass
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)
```

Alternatively, block SIGTERM/SIGINT/SIGHUP with `signal.pthread_sigmask` around the kill, then set `SIG_DFL` and unblock; the pending signal then terminates the helper. The flag version is simpler. Reset the flag only in `cli()`, like the other globals.

## 4. Timeouts and possible hangs

Worst cases, with S = one scan (about 28 ms at 3k processes) plus the 20 ms sleep:

| Path | Worst case after the trigger |
|---|---|
| Step timeout T | T + 10 s (kill loop) + 1 s (reap) ≈ T + 11 s. Measured: 1 s timeout with an unkillable member gave `call()` returning after 11.06 s. |
| Success with stragglers | 10 s wait + 10 s kill + 1 s reap ≈ 21 s |
| First cancel signal | ≤ 10 ms to notice in `peek_child_exit`, then ≈ 11 s. During the success-path wait it is noticed only when the wait ends, so up to ≈ 21 s. |
| Second signal | ≈ 1 s + S, unless signals keep arriving (problem B) |

- **No path can hang.**
  - Every loop checks a monotonic deadline.
  - `kill`/`killpg` don't block.
  - `reap_child` is bounded.
  - An unkillable D-state member ends in `LiveDescendantsError` as a cleanup error, and the step still fails.
- **One thing I did not verify** on the target kernel: whether reading `/proc/<pid>/stat` can block. I don't know of it taking the mmap lock, unlike `cmdline`/`environ`/`maps`.
- After `kill=True` gives up, the error lists members that may already have SIGKILL pending from the last pass. Suggestion: wording such as "still alive after SIGKILL", or one final rescan before raising.

## 5. `setsid()` escape

This is acceptable for these steps. I found nothing in the commands the helper runs that calls `setsid()`:

| Command | Behaviour |
|---|---|
| ninja | Jobs are spawned with a new process group (`POSIX_SPAWN_SETPGROUP`), not a new session. Verified: each job had its own PGID with SID equal to ninja's PID. |
| cmake configure / try_compile | Runs the build tool as normal children. |
| clang driver → lld; llvm-bolt (threads) | No `setsid`. |
| `/bin/sh` relink script | No `setsid`. |
| readelf, eu-strip, llvm-objcopy, symbolizer | No `setsid`. |

What commonly does escape, none of it used here:
- the `setsid` utility;
- daemonizing helpers: sccache server, distcc/icecc daemons, gpg-agent, dbus-launch, `ssh -f`, `screen`/`tmux`;
- Python tools that use `Popen(start_new_session=True)`.

The archive converter (Source1005) does use `start_new_session` itself, but the spec runs it directly, not through `call()`, so it is not affected.

If escapes ever matter, make the helper a child subreaper with `prctl(PR_SET_CHILD_SUBREAPER)` via ctypes. Escaped orphans then reparent to the helper and can be found by PPid. The helper would have to reap them by PID, never with `waitpid(-1)`, which could reap the leader. This is not needed now.

## 6. Other findings

### Problem A (real, medium-low): EPERM aborts cleanup

- `wait_session_exit(kill=True)` catches only `ProcessLookupError` from `os.kill`.
- `PermissionError` escapes on the first member the helper may not signal, for example a setuid program inside the step. That ends the kill loop: no further members are killed and no rescans happen.
- `kill_session` likewise lets `PermissionError` from `killpg` escape before the scan, although its comment says the group kill should not depend on the scan.
- **Measured:** EPERM simulated for one own-group member; a timeout with 1 s cleanup returned at once with `cleanup error: [Errno 1] Operation not permitted`. A second, killable member in another process group, with a higher PID, survived.

Fix:

```python
denied = []
for pid, state in members:
    try:
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except PermissionError:
        denied.append(pid)          # keep killing the rest; report at the deadline
```

In `kill_session`, catch `OSError` from `killpg` and continue to the scan. Then the deadline error reports the denied PIDs.

### Related (pre-existing, suggestion): `hidepid` on /proc

- The scan reads `/proc/<pid>/stat` for every process on the system.
- Under `hidepid=1`, reading another user's entry raises `PermissionError`. That is an `OSError`, which turns the whole scan into `cannot enumerate/read process session`, so every successful step would then fail.
- Real builds have a default /proc; the night builds logged `BOLT_PROC_OK`.
- Skipping unreadable entries per process would be more robust. Such processes belong to other users and couldn't be signalled anyway.

### Suggestions

- **Delete dead code.** `live_group_members` and `wait_group_exit` are no longer called. Nothing in the helper or the test suites references them.
- **Rename `_ACTIVE_GROUP`** to `_ACTIVE_SESSION`. The comment "name retained for callers" has no callers outside `call()` and `record_cancel()`.
- **Return type.** `proc_stat` now returns a 5-tuple with the session last, so the order is (pid, state, pgrp, threads, session). A named tuple would prevent index mistakes; the handler already uses `[0]`.
- **Spec (111).**
  - Unconditional `python3 >= 3.9` on x86_64 adds no new package, since `python3` was already required; it only adds a version floor in all modes.
  - The `-U` options are no-ops on a fresh build directory and clear stale cache entries otherwise.
  - Both are fine.
  - The default expansion now differs from 109 in where one blank line sits, as your parser adaptation records.
- **Tests.** The 110 suite covers cross-group timeout, failure and success, clear-before-reap and the typed error. Add:
  - EPERM on one member, with another member still killed;
  - a nested or repeated second signal with an unkillable member, checking the bound;
  - the `reaped` ordering from problem C.

## Summary

| # | Kind | Change |
|---|---|---|
| A | Real | Do not abort the kill loop on `PermissionError`; also continue after a `killpg` `OSError`. |
| B | Real (low) | Run the immediate-termination path once, with a flag or by blocking signals during the kill. |
| C | Real (very low) | Set `reaped = True` before the status `require`. |
| – | Suggestion | `killpg` per observed PGID, or pidfd with fallback, instead of a bare per-PID kill. |
| – | Suggestion | Skip unreadable /proc entries; remove dead group functions; rename `_ACTIVE_GROUP`; clearer deadline message; tests for A, B and C. |

The probe scripts are in `/tmp/claude-1000/-home-linhao-Toolchain-development-llvm-optimize/5e8aa240-5caa-4416-a0c4-218f8c1eb336/scratchpad/r15/probe/`:
- `adv.py` covers EPERM, unkillable members and the second and third signal;
- `adv2.py` covers EPERM with a second process group, and signal hammering.

The earlier probes are in `/tmp/claude-1000/-home-linhao-Toolchain-development-llvm-optimize/5e8aa240-5caa-4416-a0c4-218f8c1eb336/scratchpad/r14/probe/`.
