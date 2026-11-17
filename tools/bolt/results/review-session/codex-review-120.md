# Re-review: H2 → H3 session-cleanup hardening

Reviewed candidate: `db7ac04bd2b854b144f6e5c5fcf3a0aa9645c01e` (H3).
Previous candidate: `b06ee2ac62085748b1b137523582c989ac78184e` (H2).
Date: 2026-11-17. Reviewer: Codex.

**Recommendation: accept the R1, R2, L1 and EACCES changes, but fix the newly introduced unbudgeted diagnostic reads before treating the cleanup-deadline work as complete.** R3/L2's state tracking is substantially correct; a smaller residual wording issue remains. I found no new path in this delta that signals a retired SID, converts a cleanup error into success, silently switches a failing runtime pidfd operation to numeric signaling, or leaks an acquired pidfd. This is not a claim of guaranteed containment or a hard wall-clock bound.

## Material and verification scope

I read the complete supplied `tools/bolt/results/ps5-helper-118/resume120/helper.diff`, the process-control implementation from the H3 Git object, `test_118.py`, `test_119.py`, `test_120.py`, their `owned_scenario.py` and `seccomp_scenario.py` helpers, and `docs/bolt/118_helper_fixes.md`, including its final 120 continuation and delivery STOP. I also read `candidate.json`, `test-results.json`, and the relevant prior review findings. Unchanged product functionality outside process control was not re-reviewed.

I independently compared the H2/H3 Git diff with the supplied diff; they match. The extracted H3 helper SHA256 is:

`b0b65f814ccedc86d09bf4c37873074e03e7e53081ed5f8596d3b4e6308eb2a3`.

All product line references below refer to H3's `packaging/clang-bolt-helper.py`, not to a subsequently edited worktree. Test references are relative to `tools/bolt/results/ps5-helper-118/resume120/tests/`.

An active `gbs` process was present, so I did not start real child-process scenarios or repeat the full suite. I ran lightweight in-process tests, under MemoryMax=4 GiB, MemorySwapMax=0, CPUQuota=200%, nice 19 and idle I/O priority. No RPM build was run, and no process was killed by name or numeric PID. The real capability check only opened a pidfd for the review process itself and sent signal 0.

Fresh results: **19 test executions completed without assertion failures**:

- 11 selected supplied tests: seven mock tests plus the self-pidfd capability check from `test_118.py`, the no-child `test_first_partial_empty` from `test_119.py`, and both `test_120.py` tests.
- Five independent H3 probes: diagnostic reads exceeding the budget; diagnostic reads starting after a scan deadline; misleading scan-incomplete wording after a complete scan; discovery continuing after an entry EIO; and an incomplete scan followed by successful rescans still producing failure.
- Three tests of the proposed formatter correction on a scratch copy: complete-scan budgeting, already-expired partial-scan budgeting, and preservation of ordinary command-name output.

The defect probes pass by confirming the defects; this is not a claim that H3 passes the proposed regression requirements. Local evidence and scripts are in `/tmp/codex-review120-3z5rprjs/` (`tests.log`, `test-results.json`, `followup-tests.log`, `followup-results.json`, `review_tests.py`, `followup_tests.py`). Runtime was Python 3.12.3 on Linux `6.17.0-1033-oem`; I did not execute Python 3.9. The reviewed changes use Python 3.9-compatible constructs.

The report and result index record 722/722 tests and 12 separately counted probes. I did not independently rerun or audit every raw log in that run. The report explicitly distinguishes product/test success from the later delivery STOP and says some logs are local-only (docs/118 lines 130, 145–170, 191, 201–219); I have not treated the delivery STOP as a product-test failure or claimed the delivery audit completed.

## 1. Closure of the previous findings

| Finding | Assessment | H3 evidence and limits |
|---|---|---|
| R1: errors stop cleanup after one pass | **Closed for the reported control-flow defect.** | `wait_session_exit`, lines 276–344: the error collection lives outside the loop, each iteration takes a fresh scan, and an errored pass no longer exits immediately. It continues until a complete empty scan or the deadline. A complete empty scan with accumulated errors raises instead of succeeding. New members found by later scans are processed. See the separate diagnostic-budget regression below. |
| R2: one runtime OSError prevents processing other members | **Closed for the requested per-member errors.** | Discovery handles individual OSErrors at lines 239–246; signaling handles OSError and GateError at 331–336. ESRCH/disappearance is benign; other errors retain PID/errno, remain failures, and permit other members and subsequent retries. Runtime errors do not alter `_SESSION_KILL_MODE`. The fresh errno-matrix and EIO/rescan tests exercise these branches. |
| R3/L2: lost observations and false incomplete/unknown diagnostics | **Main classification fixed; wording follow-up remains.** | Lines 277–318 preserve the last complete nonempty observation independently of the current partial scan. A between-scans deadline does not set `final_scan_incomplete`; an actual failed scan does. `call`, lines 463–469, distinguishes an inspection failure from a live-descendant observation. Generic deadline text can still contradict this classification; see D2. |
| L1: clear active authority before retiring | **Closed.** | Both paths now clear `_ACTIVE_SESSION` before setting `session_retired`, lines 470–473 and 493–497. There is no state where the local flag is already retired but the emergency handler still sees an active SID. The first reap still occurs after both assignments. |
| EACCES at capability probe | **Closed.** | Lines 177–199 accept EACCES alongside ENOSYS/EPERM and log `SESSION_KILL_MODE=fallback-recheck errno=EACCES`. The acquired probe fd closes even when signal 0 fails. Other probe errors still fail before spawning. |

A detail about the R3 classification: the absence of a separate `ever_completed_scan` Boolean is not itself a bug. A completed empty scan terminates immediately, either successfully or with accumulated errors. Therefore a deadline reached later with no saved complete nonempty observation really has no prior complete scan on that continuing path.

R2 does not mean every possible error anywhere in `/proc` handling is recoverable. For example, the `/proc/self/stat` identity check at line 231 is outside the enumeration try, and a malformed record producing a plain GateError during discovery is not the same as a GateError during the per-member signaling recheck. These remain fail-closed, and are not newly introduced by H3. `test_malformed_member_stat_does_not_abort_pass` injects the latter, not the former; its evidence should be described accordingly.

## 2. New issue D1 — diagnostic formatting bypasses the shared deadline

**Severity: medium / important robustness issue.** Not a demonstrated wrong-target signal or false success.

**Location:** `packaging/clang-bolt-helper.py:257–266`, called at lines 311 and 318, before the signaling loop at 319–336. The same function is reached by the emergency cleanup from line 387.

`session_snapshot()` adds one `/proc/<pid>/comm` read per observed member, without receiving or checking the shared absolute deadline. In particular, the SessionDeadlineError path formats partial observations before calling `expired()`. It therefore starts additional diagnostic I/O even when the scan has already exhausted its budget.

Concrete scenarios:

1. A complete scan returns many members close to the deadline. Formatting every command name consumes the remaining budget and continues after it. Signaling does not begin until all these reads finish, then immediately discovers that time has expired.
2. A scan is interrupted by its deadline with a large partial member list. The handler starts a fresh series of command-name reads despite already knowing the deadline was reached.

The independent fake-clock probes used ten members and a simulated 0.3 seconds per command-name read. With a 1-second budget, H3 issued all ten reads and finished formatting at approximately 3 seconds. When the scan itself advanced the clock to 2 seconds and raised SessionDeadlineError, H3 still issued all ten reads, reaching approximately 5 seconds. These are controlled scheduling models, not measurements claiming ordinary procfs reads take 0.3 seconds. They demonstrate that the code has no per-entry budget check in this new loop.

This differs from the accepted caveat at line 273 that one kernel operation can overrun: H3 can deliberately start many additional operations after expiration. It can delay the second-signal termination path and consume time that could otherwise have gone to killing members. It does not reset the force-exit latch or permit a second emergency cleanup entry.

**Candidate correction, directly applicable to H3:** pass the existing deadline into the formatter and explicitly truncate diagnostic detail when it expires. Keep scan completeness independent of diagnostic truncation.

```diff
--- a/packaging/clang-bolt-helper.py
+++ b/packaging/clang-bolt-helper.py
@@ -254,10 +254,15 @@
     return sorted(members)
 
 
-def session_snapshot(members):
-    """Describe a complete observation for diagnostics, never for signaling."""
+def session_snapshot(members, deadline):
+    """Best-effort names within the shared budget; never signal authority."""
     observed = []
-    for pid, state, starttime in members:
+    for index, (pid, state, starttime) in enumerate(members):
+        if time.monotonic() >= deadline:
+            observed.append('%d:? (%s); %d further entries omitted '
+                            '(diagnostic deadline reached)' %
+                            (pid, state, len(members)-index-1))
+            break
         try:
             comm = Path('/proc/%d/comm' % pid).read_text(errors='replace').strip()
         except OSError:
@@ -308,14 +313,14 @@
             final_scan_incomplete = True
             errors[str(error)] = None
             members = error.members
-            partial_snapshot = session_snapshot(members) if members else ''
+            partial_snapshot = session_snapshot(members, deadline) if members else ''
             if isinstance(error, SessionDeadlineError):
                 expired()
         else:
             final_scan_incomplete = False
             if members:
                 last_observed = list(members)
-                snapshot = session_snapshot(members)
+                snapshot = session_snapshot(members, deadline)
         if kill:
             # Retry errored members on later scans, and handle newly forked
             # members. Never switch signaling mode after the capability probe.
```

**Side effects:** command names and the tail of the member list can be omitted at the deadline. The marker identifies the first omitted name/PID and the number of additional entries omitted; it does not claim those processes disappeared or that the process scan was incomplete. Normal snapshots retain their current form. Failure classification, accumulated errors, pidfd mode selection, kill authority and build outputs are unchanged. A single procfs read can still overrun; this is a cooperative budget, not hard real-time cancellation. The scratch-copy tests stopped after four reads in the complete-scan model and issued zero reads after an already-expired scan.

**Required tests:**

- Test the real formatter, rather than mocking `session_snapshot`, with a clock advanced by each mocked command-name read. Assert that no read starts at or after the deadline.
- Return SessionDeadlineError with nonempty partial members after expiration; assert no further command-name I/O occurs and the outcome stays unverified/partial.
- Complete a scan and exhaust the budget during formatting; assert the result remains LiveDescendantsError, retains the last-complete-scan label and has a diagnostic-truncation marker, without `final scan incomplete`.
- Exercise the emergency cleanup with this formatter and preserve the once-only latch tests.
- Update the first-partial-member expectation in `test_119.py`: it currently demands `PID:python` even after the scan has advanced beyond the deadline. Require the known PID and an explicit missing-name/truncation marker in that case. Do not demand a new procfs read after expiration. Retain name checks when there is budget.

Both supplied `test_118.py:46–67` and `test_120.py:6–20` replace `session_snapshot` with a constant string for the main diagnostic tests. Those tests usefully validate state transitions, but cannot catch this formatter regression.

## 3. Residual issue D2 — generic error text still misidentifies the failing phase

**Severity: low / diagnostic.** This does not change the failure result and need not independently block the change.

**Locations:** `packaging/clang-bolt-helper.py:202–206`, `253`, `324–330`.

Two misleading messages remain:

- `session_deadline()` always says `scan incomplete`, including when invoked during signaling after a completed scan. H3 now aggregates that text into the final error. A fresh model with one complete scan, then time consumed by the first member's signaling, produced:

  `... last observed members (last complete scan): 31:worker (S), 32:worker (S); errors: session deadline expired; scan incomplete; last observed members: 31:S, 32:S`

  The top-level `final_scan_incomplete` flag correctly remained false. The nested error text still contradicts the intended distinction. This can occur without the formatter problem: signaling or scheduling alone can consume the remaining budget.
- The discovery loop now catches all OSErrors, but its aggregate prefix still says `permission denied`. An injected EIO produced `scan incomplete; permission denied: PID 31 errno=EIO ...`. The errno is preserved, so the information is not lost, but the label is inaccurate.

**Candidate correction:** make the shared deadline message phase-neutral and the discovery error label broad enough for the errors now accepted there.

```diff
--- a/packaging/clang-bolt-helper.py
+++ b/packaging/clang-bolt-helper.py
@@ -202,7 +202,7 @@
 def session_deadline(deadline, members):
     if deadline is not None and time.monotonic() >= deadline:
         raise SessionDeadlineError(
-            'session deadline expired; scan incomplete; last observed members: '+
+            'session deadline expired; last observed members: '+
             ', '.join('%d:%s' % item[:2] for item in members), members)
 
 
@@ -250,7 +250,7 @@
         raise SessionInspectionError('cannot enumerate/read process session; scan incomplete: '+str(error), members) from error
     session_deadline(deadline, members)
     if denied:
-        raise SessionInspectionError('scan incomplete; permission denied: '+'; '.join(denied), members)
+        raise SessionInspectionError('scan incomplete; member read errors: '+'; '.join(denied), members)
     return sorted(members)
 
 
```

**Side effects:** diagnostic text changes only. The actual scan exception type and `final_scan_incomplete` state remain intact, so wait_session_exit can still identify a failed scan. Tests or downstream log consumers that match the old generic string need updating; none should infer scan completion from a deadline error emitted inside signaling.

**Tests:** add a complete-scan → signaling-timeout case that checks the entire exception, including its aggregated error suffix, not only the `final scan incomplete` phrase. Add an entry-EIO/EMFILE case that confirms other entries are processed and the result says `member read errors`, retaining PID and errno. Preserve the actual partial-scan diagnostic cases. Both proposed diffs passed `git apply --check` together against a scratch copy of the exact H3 helper.

## 4. Earlier behavior and safety invariants

I found no additional regression in the changed control flow, with the runtime-testing limits stated above:

- **SID lifetime:** the leader remains unreaped during scan/kill activity. Clearing `_ACTIVE_SESSION` before retirement and before reap removes emergency-handler authority first. The local `session_retired` guard still prevents later exception handling from scanning or killing after reap. `process.returncode is None` still controls reap retries. This assumes call() remains the sole reaper of its leader, as in the existing design; it is not protection against an unrelated competing waitpid implementation.
- **pidfd ordering:** lines 210–219 remain open → read current SID → deadline check → fd signal → close in finally. H3's additional exception handling is outside this ownership scope. Successful opens still close their fds when rechecks, signal sends or deadline checks fail. Runtime resource/permission errors are retained and retried, not silently downgraded.
- **Fallback:** only the pre-spawn probe gains EACCES. Runtime EACCES is still an aggregated cleanup error in the already selected mode. ENFILE/EMFILE/ENOMEM/EINVAL at the probe are not newly classified as capability absence. EACCES fallback remains weaker than pidfd: the SID/starttime recheck narrows, but does not eliminate, the numeric-PID reuse window. Worker-specific seccomp qualification remains necessary.
- **Emergency signals:** `_FORCE_EXITING`, deferred second-signal publication, and the restore-default/self-resignal finally block are unchanged except for a comment. A further signal during emergency cleanup still bypasses another cleanup entry and terminates. The new formatter can lengthen the first emergency pass if no further signal arrives, which is D1, not a latch failure. No child signal mask or inherited disposition is changed by this delta.
- **Success drain:** a zero-exit leader is not enough: a complete empty scan is still required. An unreadable scan is not treated as empty. Sticky errors intentionally make a later complete empty scan fail rather than erase an earlier cleanup/check problem.
- **Failure and timeout:** the error retry is intentionally longer than H2's early-abort behavior, up to the remaining budget. Cleanup failure remains attached to the command failure. SystemExit(0) cannot conceal cleanup failure. First cancellation still does not automatically shorten an already running drain wait; that is unchanged, not a newly fixed responsiveness guarantee.
- **SIGCHLD:** reset/restore and the `None` restoration guard at lines 429–432 and 513–516 are unchanged. The restoration guarantee is for the helper's direct-child handling; the code still does not adopt or reap grandchildren. A failed cleanup can leave a process alive, and forced termination is best effort. Do not interpret SIGCHLD restoration as proof that every descendant has been reaped.
- **Historical observations:** saved member lists are only diagnostics. Signaling uses the current scan's members, with pidfd acquisition/recheck, not `last_observed`. Command names are best-effort later reads and may change or disappear between the stat scan and `/proc/<pid>/comm`; they are not identity evidence and must never become a kill predicate.
- **Known limitations:** descendants that call setsid(), permission-denied/unkillable processes, fallback's numeric race and single-operation deadline overruns remain explicitly outside stronger containment guarantees. H3 does not claim to add cgroup containment or a subreaper.

## 5. Test quality and remaining evidence

The added tests are meaningful, but their evidence levels differ:

- `owned_scenario.py` drives real session members in separate process groups, injects a first-member failure, and creates another member during cleanup. That is a relevant R1/R2 scenario rather than a mock that merely asserts the implementation's loop shape. Its fault injection and subreaper cleanup mean it is a mixed test, not an untouched production-environment proof. I read it but did not run it in this pass.
- The errno matrix checks processing order and retry without runtime fallback; the new scan-error probes independently check that incomplete discovery stays a failure after a later empty scan.
- The L1 trace tests check `_ACTIVE_SESSION` at the exact retirement-assignment line on success and failure. They complement the earlier reap-boundary injections; they do not exhaust every asynchronous interleaving.
- The seccomp fixtures test the actual probe syscall failure rather than only mocking AttributeError. I did not rerun them. The selected send-probe EACCES test did verify descriptor closure and the exact log line, and the real self-probe selected pidfd on this host.
- The fake-clock tests are appropriate for distinguishing time expiring between scans from time expiring during a scan. Their mock of the new formatter leaves the D1 gap. The mixed diagnostic tests in `test_119.py` similarly cannot establish real wall-clock bounds because they control the clock and scans.

Before claiming the revised formatter is fully certified, add the missing formatter/signaling-deadline tests, update only the obsolete post-deadline name expectations, and rerun the supplied process-control regression suites under the existing owned-process harness. This re-review does not require another RPM build: no spec, flags, compiler invocation or product transformation changes in this delta.

**Final recommendation:** R1, R2, L1 and the EACCES selection change are closed. R3/L2's observation/classification logic is correct for the stated cases, with D2 as a small diagnostic follow-up. Fix D1's unbudgeted diagnostic loop and rerun the affected tests before accepting the cleanup deadline as hardened. No new wrong-session/wrong-process signal or fail-open success was demonstrated; the remaining concern is cleanup responsiveness plus diagnostic accuracy, not generated LLVM output.
