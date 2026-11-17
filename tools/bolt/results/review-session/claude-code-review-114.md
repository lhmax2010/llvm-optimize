# Review: session-cleanup hardening (114, candidate b06ee2ac)

## What I reviewed and ran

**Material**
- `b06ee2ac:packaging/clang-bolt-helper.py`. Its SHA256 is 4f89c605…, as in `candidate.json`.
- The 378f8d5c→b06ee2ac diff, which matches `tools/bolt/results/ps5-helper-114/helper.diff`.
- `test_114.py`, its log, and `docs/bolt/114_helper_hardening.md`.

**Probe method: only processes the test owns.** I replaced my earlier `pgrep` cleanup with a new harness.
- **Subreaper.** The harness first makes itself a child subreaper. It then runs each scenario in a runner child that it owns.
- **After the runner exits, any surviving descendant has been reparented to the harness.** The harness finds its own children by PPid, kills them through a pidfd, and reaps them.
- **These are unreaped children of the harness, so their PIDs cannot be reused.** Nothing is killed by name or by a bare PID.
- **Signals go only to the runner,** through `Popen.send_signal`.
- **Fault injection.** The runner gives the loaded helper module a proxy `signal` or `os` module. The proxy can make `pidfd_send_signal` fail with EPERM or do nothing (simulating a D-state process), or make `pidfd_open` fail with EMFILE. Each fault applies only to one marked member, which sits in its own process group.
- **Ninja and Python.** ninja 1.13.1 from the Tizen build root, run on Linux 6.17 with Python 3.12, in pidfd mode, plus one fallback run.

I ran no RPM build. Scripts: `/tmp/claude-1000/-home-linhao-Toolchain-development-llvm-optimize/5e8aa240-5caa-4416-a0c4-218f8c1eb336/scratchpad/r16/probe/` (`harness.py`, `runner.py`).

## Verdict

F2/C and F3/B are closed. F1 is implemented correctly. No retired or unpinned SID can be signalled, and in pidfd mode no unpinned PID can be either. All behaviour I tested against 111 is preserved.

Three problems remain, all in the error paths of the kill loop, plus one diagnostic regression:

| # | Severity | Problem |
|---|---|---|
| R1 | medium-low | A per-member error ends cleanup after one pass. A only half-closed. |
| R2 | medium-low | A runtime `OSError` from `pidfd_open` (or `proc_stat`) for one member aborts the whole cleanup. |
| R3 | low (diagnostic) | The drain timeout now always reports "scan incomplete" with an empty member list. |
| R4 | style | The deadline wording is misleading in general. |

## 1. Are the previous findings closed?

| Finding | Status | Evidence |
|---|---|---|
| **C**: reap before `reaped`, then kill by SID | **Closed.** | See below. |
| **B**: repeated signals restart cleanup | **Closed.** | `_FORCE_EXITING` admits one emergency pass; later signals go straight to the `finally` (`SIG_DFL` + re-raise). Real run, with an unkillable member and SIGTERM at 0.5, 0.8 and 1.1 s: the runner died by SIGTERM after the third signal. Second signal alone during a 10 s cleanup: died 1.0 s later (signal at 2.0 s, exit at 3.0 s). |
| **F1**: PID reuse between scan and kill | **Closed in pidfd mode.** | Open, then check SID, then send through the fd. Fallback re-checks SID and starttime; the remaining race is documented. |
| **A**: EPERM aborts cleanup | **Partly closed.** | Members later in the same pass are now signalled. Cleanup then stops after that one pass; see R1. |
| Removal of group helpers | Done. | |

Details on C:
- `session_retired` is set and `_ACTIVE_SESSION` cleared before `reap_child`.
- The cleanup path skips `kill_session` once the session is retired.
- It retries the reap only while `returncode is None`.
- `reaped = True` still comes after the `require`, but this no longer matters: the retired flag blocks the kill.
- The three fault points tested (before waitpid, after the real reap, during the metadata save), plus "after waitpid, before `returncode` is set", all avoid `kill_session`.

**Can a retired or unpinned ID be signalled?** I found no path.
- `killpg(sid)` and every scan run only while the leader is unreaped and not retired:
  - **cleanup:** guarded by `not session_retired`;
  - **signal handler:** guarded by `_ACTIVE_SESSION`, which is cleared together with the retirement and before any reap.
- A handler that runs between `session_retired = True` and `_ACTIVE_SESSION = None` still sees an unreaped leader, so that is safe.
- In pidfd mode, a member's identity is pinned by the fd. Fallback keeps the documented scan-to-kill race, narrowed by the starttime check.

## 2. The pidfd path

- **Ordering is correct:** `pidfd_open` → stat re-check of the SID → deadline check → `pidfd_send_signal` → close in `finally`.
  - **Reuse before the open:** the stat check shows a foreign SID and nothing is sent.
  - **Reuse after the open:** the send fails with ESRCH, which is caught as `ProcessLookupError`.
  - **Same number, new process in our session:** the send fails with ESRCH; the next scan finds the new process.
  - **No fd leak:** every exit after a successful open goes through `finally: os.close(fd)`. The only gap is a signal arriving between `pidfd_open` returning and the `try`. That signal can only be the terminal path, which ends the process anyway.
- **Real tests:**
  - a matching owned member is killed;
  - an owned process in another session is skipped;
  - in pidfd mode, ninja timeout and ninja straggler both leave no survivors.

**R2: a runtime `pidfd_open` failure for one member aborts the whole cleanup.**
- The probe covers only the helper's own PID, once. At kill time, `pidfd_open` can still fail for one member with an errno other than ESRCH: EMFILE, ENFILE or ENOMEM. EINVAL is possible in theory if the number is reused by a thread between the scan and the open.
- `wait_session_exit` catches only:
  - `FileNotFoundError`;
  - `ProcessLookupError`;
  - `PermissionError`;
  - `SessionInspectionError`.
- Any other `OSError` escapes. `kill_session` re-raises only `GateError`, so the `OSError` ends the call, and the rest of the pass and all rescans are skipped.
- `kill_session_member` also raises a plain `GateError('malformed process stat')`, which `wait_session_exit` does not catch either. That ends the pass as well; `kill_session` only re-raises it.
- **Measured (EMFILE injected for one member):** the timeout cleanup returned after 0.06 s with `cleanup error: [Errno 24] …`. 28 session processes survived, including a killable spawner process and its children.

Fix: catch `OSError` (and `GateError`) per member, add them to `errors`, and continue. This keeps the "no silent downgrade" design: don't fall back to `os.kill`, just keep handling the other members and fail at the end.

## 3. Fallback selection

**The rule is sound.**
- `AttributeError` or ENOSYS: Python or the kernel lacks pidfd. pidfd_send_signal needs kernel 5.1 and pidfd_open needs 5.3, so a 5.1–5.2 kernel gives ENOSYS on the open.
- EPERM: the typical seccomp return value.
- Both select `fallback-recheck`.
- Any other errno fails the step before spawn (`test_pidfd_other_failure_blocks_spawn`), so it fails closed and never misreports.
- The mode is chosen once per helper process and logged on stderr. Stdout JSON is unaffected.

**Could a sandbox make every build fail?**
- **Common filters are fine:**
  - Docker ≥ 20.10 allows both syscalls; older Docker and podman return EPERM for unknown syscalls.
  - systemd `SystemCallFilter=` defaults to EPERM.
  - gVisor returns ENOSYS.
  - GBS chroots and OBS KVM workers have no filter.
- **Unusual filters would fail every BOLT step:**
  - one that returns an errno such as EACCES or EINVAL, chosen with `SCMP_ACT_ERRNO`;
  - one with a KILL or TRAP action, which ends the helper with SIGSYS at the first `call()`.

  Both are fail-closed and visible in the log. I don't know of a Tizen build environment with such a filter.
- Option, if you want to be generous: treat EACCES like EPERM. I would not widen the rule further.
- **A probe can pass while a runtime call fails** (resource limits); see R2. That is the more realistic gap.

Fallback mode works on a real process tree: with `pidfd_open` removed, the run logged `SESSION_KILL_MODE=fallback-recheck`, and a ninja timeout left no survivors.

## 4. Signal handling

- **Force-exit latch:** correct; measured under B above. A nested handler skips the cleanup and terminates immediately. The second signal's pass is abandoned, not restarted.
- **`finally` path:** `SIG_DFL` + `os.kill(self)` also covers an exception from `kill_session`, and a signal different from the second one: TERM then HUP ends with HUP.
- **Deferred second signal during spawn: unchanged.**
  - While `_SPAWNING` is set, the handler only records the signal.
  - The replay after `Popen` takes the latch, kills the published session, and terminates.
  - If `Popen` failed, `_ACTIVE_SESSION` is `None`, so the replay just terminates.
  - A third signal during spawn is dropped, but the replay terminates anyway.
- **No lost termination:**
  - The handlers run in the main thread with the signal unblocked, so the self-kill under `SIG_DFL` is delivered at once.
  - `cli()` installs handlers only for signals that were not ignored.
  - If two first signals race, the later one overwrites `_CANCEL_SIGNAL`. Both mean cancel; harmless.
- **Reset:** `_FORCE_EXITING` is reset only in `cli()`. That is enough, because the force path always ends the process.

## 5. Regressions against 111

| Case | 114 result |
|---|---|
| Short background child (3 s) | Success after 3.05 s; SIGCHLD handler restored |
| Long background child | Fails after 10.04 s; no survivors |
| ninja straggler | Fails after 10.1 s; no survivors |
| ninja timeout, pidfd mode | TIMEOUT after 2.1 s; no survivors |
| ninja timeout, fallback mode | TIMEOUT after 2.1 s; no survivors |
| First SIGTERM during the drain | CANCELLED after the 10 s drain; exit status from `_CANCEL_SIGNAL` as before |
| Second SIGTERM during the drain | Died by SIGTERM 1.0 s after it; no survivors |
| Unkillable member, no error (0.3 s per kill) | Loop kept rescanning: 11.0 s, only the unkillable member survived |

Behaviour is preserved, with one exception.

**R3 (diagnostic regression): the drain timeout no longer names the processes.**
- 111 reported `process session N still alive: 552646:S, 552647:S`.
- 114 always reports `… live descendants: session deadline expired; scan incomplete; last observed members: ` with an empty list.
- Cause:
  - `wait_session_exit` clamps its sleep to the remaining time;
  - so the next iteration enters `live_session_members` after the deadline;
  - `session_deadline(deadline, [])` there raises `SessionDeadlineError` with no members;
  - the bottom `LiveDescendantsError` branch, which would list members, is effectively unreachable in drain mode.
- The step still fails, but the log now says the scan was incomplete (it wasn't) and loses the names of the lingering processes. Those names are what an operator needs.

Fix: keep the members from the last complete scan. When the deadline expires at the start of a scan, raise `LiveDescendantsError('process session %d still alive at deadline: …')` with them. Reserve "scan incomplete" for scans that really were interrupted or denied.

**R4 (style):** the bottom branch's message also says "scan incomplete", even after a complete scan. In the unkillable case I got `cleanup error: process session N deadline expired; scan incomplete; last observed members: 564006:S`.

**R1: one per-member error turns cleanup into a single pass.**
- After a pass with any entry in `errors`, `wait_session_exit` raises at once.
- The `PermissionError` case shows this, and also a partial scan, e.g. `hidepid=1`.
- It does not rescan until the deadline, so processes forked during that pass survive.
- **Measured:** EPERM injected for one member, plus a 0.3 s delay on that call. Six children that a killable spawner forked during the pass survived.
- The same scenario without the error (the unkillable case above) rescans and leaves only the unkillable member.
- `test_permission_member_does_not_stop_next` asserts this single-pass behaviour.

Fix: collect errors across passes; keep scanning and killing until the session is empty or the deadline passes; then raise with every error and the last observed members.

## 6. The 34 new tests

**Testing real behaviour (12):**
- the four retirement tests: real `call()` and child, with fault injection only in `reap_child`/`save`, and `kill_session` patched only to assert it is never called;
- `test_force_reentrant_real_short_timing`: real signals, with a stubbed slow cleanup;
- `test_pidfd_matching_owned_member_killed`;
- `test_pidfd_stale_pid_in_other_owned_session_skipped`;
- `test_fallback_stale_owned_session_safe`;
- `test_mode_logged_before_spawn`;
- `test_cleanup_error_is_failure` and `test_zero_systemexit_cannot_hide_cleanup_error`: real child, patched wait;
- `test_setsid_escape_owned_process_outside_scan`. This one is weak: it only shows that a different session is not in our session's scan.

**Control flow against mocks only (21):**
- the fd-closing tests with fake fd 71;
- the three mode-selection tests, plus the missing-send-API test;
- `test_pidfd_other_failure_blocks_spawn`;
- `test_fallback_revalidates_sid_and_starttime`;
- the permission, missing and leader-permission tests;
- the four `scan_context` tests;
- `test_partial_scan_still_kills_visible_member`;
- the four deadline tests;
- the two `record_cancel` mock tests.

These are reasonable unit tests of the decision logic, with three caveats:
- **Brittle:** the deadline tests feed `time.monotonic` a fixed list (`side_effect=[0,0,2]`), so they break if the number of clock calls changes, not if the behaviour does.
- **Encodes a defect:** `test_permission_member_does_not_stop_next` asserts the single-pass behaviour of R1.
- **Nothing checks the live-descendants message content,** which is how R3 got through.

**Text check (1):** `test_old_group_apis_removed`.

Cross-session behaviour with real processes (ninja, cross-group) is covered by the 110 suite, which now runs in pidfd mode on this host.

**Missing real tests:**
- fallback mode on a real cross-group tree (my probe passes);
- a runtime `pidfd_open` error for one member (R2);
- EPERM followed by a rescan (R1);
- the drain-timeout diagnostic naming the processes (R3).

My harness shows how to do these while signalling only owned processes:
- make the test a subreaper;
- kill only its own unreaped children through a pidfd;
- use fault-injection proxies on the helper's `os` and `signal` modules, so the real kill paths still run.

## Summary

| # | Kind | Change |
|---|---|---|
| R1 | Real | Keep rescanning and killing until the deadline after per-member errors; raise with the aggregated errors at the end. |
| R2 | Real | Catch `OSError` (and `GateError` from a stat re-check) per member in the kill loop, instead of letting one member abort cleanup. |
| R3 | Real (diagnostic) | Report the last complete scan's members as "still alive at deadline"; don't label a reached deadline "scan incomplete". |
| – | Suggestion | Optionally treat EACCES like EPERM at the probe; replace the `monotonic` side-effect lists with a fake clock; add real tests for R1–R3 and the fallback cross-group case. |

Everything else asked about is closed or preserved:
- F2/C;
- F3/B;
- F1 in pidfd mode;
- the shared deadline;
- removal of the group helpers;
- SIGCHLD restore;
- success drain, timeout, and first and second cancel.
