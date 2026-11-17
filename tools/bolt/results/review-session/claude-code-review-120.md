# Review: session-cleanup fixes H2→H3 (120, candidate db7ac04b)

## What I reviewed and ran

**Material**
- `db7ac04bd2b854b144f6e5c5fcf3a0aa9645c01e:packaging/clang-bolt-helper.py`, from a local clone of the product repository. SHA256 b0b65f814ccedc86d09bf4c37873074e03e7e53081ed5f8596d3b4e6308eb2a3.
  - `git diff b06ee2ac db7ac04b` touches only this file (+81/−26) and matches `tools/bolt/results/ps5-helper-118/resume120/helper.diff` byte for byte.
  - H3's parent is 61ef5d31, the same as H2's.
- `tests/test_118.py`, `test_119.py`, `test_120.py`, `owned_scenario.py`, `seccomp_scenario.py` and `test-118-kinds.json` under `resume120/tests/`.
- `docs/bolt/118_helper_fixes.md`, sections 118, 119 and 120.
- Codex's L1 text in `codex-review-114.md`, to know what L1 asked for.

**What I ran**
- **Tests.** `test_114` (34), `test_118` (19), `test_119` (6) and `test_120` (2), run against a scratch copy of the H3 helper: **all 61 pass.** I did not run the full 722-test suite; the remaining 661 results are the author's and I have not checked them.
- **Probes.** The same ownership-safe harness as in my 114 review, extended with new cases.
  - The harness makes itself a child subreaper and signals only its own runner child.
  - Afterwards it kills only its own unreaped children, through pidfds.
  - Faults are injected through proxy `os`/`signal` modules into the loaded helper, and target only one marked member in its own process group.
  - The new cases are:
    - all-EMFILE: every `pidfd_open` fails;
    - EACCES and EINVAL capability probes;
    - a transient and a persistent scan error on a non-member `/proc` entry;
    - a kill-pass deadline.
  - I ran 22 probes on H3 and 3 comparison probes on H2. I ran no RPM build, killed nothing by name or by bare PID, and left nothing running.
- **Mocks.** One in-process mock with no processes, to place the deadline inside the kill pass exactly.

Probe scripts are in `/tmp/claude-1000/-home-linhao-Toolchain-development-llvm-optimize/5e8aa240-5caa-4416-a0c4-218f8c1eb336/scratchpad/r17/probe/` (`harness.py`, `runner.py`). Results are in `results.jsonl` and `cmp.jsonl` in the same directory.

## Verdict

All six items are closed: **R1, R2, R3, L2, L1 and EACCES**. No earlier behaviour regressed. I found no new correctness problem: no path signals a retired or unpinned SID, and in pidfd mode no path signals an unpinned PID.

What remains is diagnostics and policy. None of it changes pass/fail:

| # | Severity | Item |
|---|---|---|
| N1 | low (diagnostic) | The text of `session_deadline()` is still copied into `errors`, so "scan incomplete; last observed members: " (sometimes with an empty list) reappears after complete scans. |
| N2 | policy note | Errors stick across rescans, so one transient error fails a step even after a complete, empty final scan. |
| N3 | info | A persistent scan error now costs the full drain and cleanup budgets (about 20 s) before failing. H2 failed at once. |
| N4 | style | The snapshot re-reads `/proc/<pid>/comm` by number, and the member list in the message is not bounded. |
| — | known limit | If `pidfd_open` fails for every member (process-wide EMFILE), pidfd mode cannot signal anything outside the leader's group. This is by design. |

## 1. Is each finding closed?

| Finding | Status | Evidence |
|---|---|---|
| **R1**: one pass after a member error | **Closed.** | `wait_session_exit` no longer breaks or raises on member errors. It records them in `errors`, then rescans and re-kills until a complete scan is empty or the deadline passes. Real probe (`eperm-delay`): the injected-EPERM member plus a spawner that forks every 50 ms. **Only the EPERM member survived.** H2 left 6 forked children. |
| **R2**: runtime `OSError` aborts cleanup | **Closed** for per-member errors. | `kill_session_member` errors are caught per member, and retried on later scans. This covers any `OSError` except ESRCH, and also a `GateError` from a malformed re-check stat. Real probe (`emfile`, `pidfd_open` EMFILE for one member): **1 survivor, the injected member.** H2 left 28. The mode is never switched after the probe. For the process-wide case, see the known limit below. |
| **R3**: empty, misleading drain-timeout message | **Closed** on the main path. | `bg-long`: `drain deadline; last observed members (last complete scan): 772692:sleep (S)`. `ninja-straggler` likewise names `773030:sleep (S)`. With no complete scan, the message is `could not verify that the session is empty; partial observations: …`. A fragment of the old text still leaks through `errors`; see N1. |
| **L2**: an incomplete or empty last scan must not erase the earlier observation | **Closed.** | `last_observed` and `snapshot` change only after a complete scan; `final_scan_incomplete` is set only in the scan-exception branch. `test_L2_*`, the 119 tests and `test_120` cover the four combinations, and pass. |
| **L1**: retirement publication order | **Closed.** | Both paths now clear `_ACTIVE_SESSION` before setting `session_retired`, so no point has the session retired while its SID is still published. The reverse window (cleared but not yet retired) is harmless: `record_cancel` never raises, and the leader is still unreaped there. `test_L1_*` checks this with a line trace; they pass. |
| **EACCES** chooses the logged fallback | **Closed.** | Probe `eacces-probe`: `SESSION_KILL_MODE=fallback-recheck errno=EACCES`, then the step succeeds. `einval-probe`: no mode line, and `call()` fails before `Popen`. ENOSYS, EPERM, EACCES and EINVAL are also tested with a real seccomp filter in a child, in `test_seccomp_*`. |

Unchanged and still closed: C and B (latch, deferred second signal), F1 (pidfd open → re-check → send → close), and removal of the group helpers.

## 2. Regression check: probes on H3

| Scenario | H3 result | Time (s) | Left for harness | Same as H2/111? |
|---|---|---:|---:|---|
| bg-short (sleep 3 after rc 0, SIGCHLD handler installed) | OK, SIGCHLD restored | 3.02 | 0 | yes |
| bg-long | live descendants, names the member | 10.02 | 0 | yes (better message) |
| first-wait (SIGTERM at 1 s during drain) | CANCELLED after the drain | 10.02 | 0 | yes (drain does not check cancel; known) |
| second-wait (SIGTERM at 1 s and 2 s) | runner killed by SIGTERM | 2.01 | 0 | yes |
| ninja-straggler (ninja 1.13.1) | live descendants | 10.3 | 0 | yes |
| ninja-timeout, pidfd mode | TIMEOUT | 2.06 | 0 | yes |
| ninja-timeout, fallback mode | TIMEOUT | 2.04 | 0 | yes |
| fallback, spawner + special member | TIMEOUT | 1.05 | 0 | yes |
| eperm-delay | TIMEOUT + cleanup error | 11.01 | 1 (injected) | **fixed** (H2: 6 forked children also survived) |
| emfile (one member) | TIMEOUT + cleanup error | 11.01 | 1 (injected) | **fixed** (H2: 28 survivors) |
| unkillable-delay | TIMEOUT + cleanup error | 11.01 | 1 (injected) | yes |
| hammer-unkillable (SIGTERM at 0.5, 0.8, 1.1) | killed by SIGTERM after the third | 1.4 | 1 (injected) | yes |
| second-cleanup-unkillable (SIGTERM at 0.5, 2.0) | killed 1.0 s after the second | 3.0 | 1 (injected) | yes |

Every "injected" survivor is the member made unkillable or undeniable by design. The harness then killed and reaped it as its own child.

No behaviour regressed. The two timing changes below occur only in paths that already failed (closed) on H2.

## 3. Remaining items

### N1 — "scan incomplete" still leaks from `session_deadline()` (low, diagnostic)

`expired()` itself follows the new rule. But `session_deadline()` still builds `'session deadline expired; scan incomplete; last observed members: …'`, and that text is added to `errors` in two places:
- the scan branch (line 309, before `expired()`);
- the kill-pass branch (line 329).

`expired()` then appends it after `errors:`:
- **Deadline inside a scan.** Real `first-wait` and `unkillable-delay` both end in `… final scan incomplete; errors: session deadline expired; scan incomplete; last observed members: ` with an **empty** list. That is the R3 fragment again.
  - A scan here takes about 4.5 ms (521 processes) and the sleep is 20 ms, so roughly one drain timeout in five lands inside a scan. Busier hosts make it more frequent.
- **Deadline inside the kill pass after a complete scan.**
  - Mock with three slow kills: `last observed members (last complete scan): 101:x (S), 102:x (S), 103:x (S); errors: session deadline expired; scan incomplete; last observed members: 101:S, 102:S, 103:S`. There is correctly no "final scan incomplete", but the errors tail still says "scan incomplete".
  - Real `eperm-delay` shows `…errors: PID 773275 errno=EPERM…; session deadline expired; scan incomplete; last observed members: 773275:S`.
  - This contradicts the stated rule that "final scan incomplete" appears only when a scan was actually cut short.

**Effect.** The message is noisy and partly contradictory. The error class and pass/fail are correct.

**Fix.** Either:
- don't record a `SessionDeadlineError` in `errors`, since `expired()` already reports the deadline; or
- give `session_deadline()` a neutral text such as "deadline expired during scan" / "during kill pass", with no member list.

**Why the tests miss it.** `test_120` and 119 inject a `SessionDeadlineError('deadline during scan')`, so they never see the real text. One test of the kill-pass deadline asserting `'scan incomplete' not in message` would cover it.

### N2 — errors stick across rescans (policy note, not a regression)

`errors` collects for the whole call, so a single transient problem fails the step even when the final complete scan is empty. The problem can be:
- one scan error on any `/proc` entry, including a non-member; or
- one failed signal to a member that then exits.

- **Probe `transient-scan`.** A successful command whose only background `sleep 0.5` exits normally; one injected EACCES on reading a non-member's stat in the second scan. Result: `COMMAND_ERROR: session cleanup/check failed; …`.
  - H2 failed the same case too (in 0.06 s rather than 0.53 s), so this is not a regression.
  - `test_member_runtime_errno_matrix_no_fallback` encodes it deliberately.
- **Assessment.** For `kill=True` this is right: we never confirmed that our signal landed. For the success drain it is stricter than needed, but it fails closed, and the trigger is rare: `/proc/<pid>/stat` is world-readable, and ESRCH/ENOENT are already excluded. Please confirm this is the intended policy.
- **Cosmetic.** This plain `GateError` is not caught by the two `except` clauses in `call()`. The step error therefore lacks the "command exited successfully" context that the other two drain outcomes carry.

### N3 — a persistent scan error now costs about 20 s (info)

When every scan is incomplete (for example, one `/proc/<pid>/stat` permanently unreadable), H3:
1. waits out the 10 s drain;
2. raises `could not verify …`;
3. then spends the 10 s cleanup budget the same way.

- Probe `persistent-scan`: 20.01 s on H3, against 0.03 s on H2.
- Both fail closed, so only latency changed, and only on hosts where some `/proc` stat files are unreadable. On such a host every BOLT step fails in both versions.
- Worth stating in the worker qualification note. No code change needed.

### N4 — snapshot details (style)

- **comm read by number.** `session_snapshot()` re-reads `/proc/<pid>/comm` by number after the scan. It is diagnostic only and never kill authority, but a reused PID can be labelled with another process's name. The scan already parses the stat line, whose second field is comm. Taking comm from there is race-free and saves one open per member per 20 ms.
- **Unbounded message.** The member list in the message has no limit. In the all-EMFILE probe, the cleanup error listed 225 members. Consider the first 20 plus a count.
- **Wording.** Kill-mode cleanup errors say "drain deadline" (for example `cleanup error: process session N drain deadline; …`). "cleanup deadline" would read better there.

### Known limit — process-wide `pidfd_open` failure

Probe `allemfile` makes every member `pidfd_open` fail with EMFILE:
- **H3:** retries for the full 10 s, fails closed, and lists every member. 225 forked children were left for the harness.
- **H2:** aborted at once, leaving 27.

The higher count only reflects that the spawner forked for 11 s instead of 1 s. Neither version can signal members outside the leader's process group in this state. Switching to `os.kill` mid-cleanup would reintroduce the PID-reuse window that pidfd mode exists to close, so the "never switch mode" rule is defensible. The trigger would need an fd leak in the helper itself, which holds few fds. I'd only document it.

One related corner remains. A `GateError('malformed process stat')` raised *during the scan* (not during a member re-check) still escapes `live_session_members` and the retry loop. The kernel never produces such a line, and races give ESRCH, so this is theoretical.

## 4. Tests

I ran four suites against the H3 copy, and all pass: 114 (34), 118 (19), 119 (6) and 120 (2).

The 118 labels in `test-118-kinds.json` match my reading: 5 real, 7 mixed and 7 mock.
- **Strongest additions.** `test_R1_permission_rescan_fork_real`, `test_R2_emfile_rescan_real` and `test_R2_enomem_rescan_real`, through `owned_scenario.py`.
  - Each builds a real session with members in separate process groups.
  - It injects the fault on the leader at the moment a new child is forked.
  - It then waits until each held pidfd becomes readable, which proves every process died.
  - This closes the "real R1/R2 test" gap from my 114 review.
- **Seccomp tests.** `test_seccomp_*` install a real filter in a child only, which is the right scope. The filter does not check `arch`, which is acceptable given the x86_64 assert.
- **119.** Real owned `Popen` plus a controlled scan and clock. A sound approach for diagnostic forms.
- **120.** Two pure mocks of the boundary: a deadline between scans and a deadline inside a scan.

**Missing tests:**
1. A deadline inside the kill pass after a complete scan, asserting no "scan incomplete" (N1).
2. A process-wide `pidfd_open` failure, documenting the expected fail-closed result.
3. A success drain with one transient non-member scan error, documenting the N2 policy.

## 5. Not reviewed

- The delivery-invariance STOP in `resume120/STOP.txt` and `STOP-add.txt`: a preparation error in the delivery check, not product code.
- The sandbox push itself.
- The 109/110 suites and P1/P2/S2 parsing. I did not rerun these and rely on the author's logs.
- QB/worker capability: whether real workers end up in pidfd or fallback mode remains an operational check.
