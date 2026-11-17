**Recommendation: accept the hardening under the explicitly approved fallback policy.** I found no new blocking regression in the reviewed process-control paths. F2/C's unsafe post-reap cleanup is fixed; F3/B's recursive emergency cleanup is fixed; and A's per-member permission-error abort is fixed. F1 is fixed in pidfd mode. It is deliberately only mitigated in fallback-recheck mode, which still has a final numeric-PID check-to-signal race.

There are two low-priority follow-ups: make the published active-session handle agree immediately with the retirement flag, and preserve the previous observed-member list when a subsequent scan times out before reading an entry. Neither finding demonstrates signaling an unpinned SID in this candidate. Separately, qualify the actual worker's kernel/seccomp policy: the requested fallback errno allowlist is implemented correctly, but it is not universal sandbox compatibility.

**Reviewed identity and scope**

- Candidate: `b06ee2ac62085748b1b137523582c989ac78184e`.
- Previous candidate: `378f8d5c94aeadd2a8618d04ad39a531529c726c`.
- Candidate helper SHA256: `4f89c605838af582940d288ec884b4dd1f28696b0cfce64804a2aace68b315ca`.
- I verified that the supplied helper.diff is exactly the Git diff between those two commits and that the inspected complete helper matches the candidate Git object. Line numbers below refer to that candidate's `packaging/clang-bolt-helper.py` unless another file is named.
- Read the supplied diff, all 34 tests in `tools/bolt/results/ps5-helper-114/tests/test_114.py`, and `docs/bolt/114_helper_hardening.md`; cross-checked the findings against both archived session reviews. Inspected the complete process-control and CLI bodies, including unchanged code needed to assess the new paths. This is not a fresh review of unrelated ELF/BOLT functionality or the RPM spec.
- No product file was changed, no RPM build was run, and nothing was pushed or posted. All test signals in this review used pidfds for test-owned processes; numeric-PID signaling paths were mocked. I did not run the archived global-pgrep probe scripts.

The report's 695/695 result is prior task evidence. I did not rerun that full suite in this review. Fresh checks are listed below, separately from that reported result.

**1. Previous findings and SID/PID lifetime**

| Finding | Result | Evidence and limit |
|---|---|---|
| F2/C: exception after actual reap can kill an unpinned SID | Closed for the reviewed call() lifecycle | Lines 415–419 and 431–444 retire local cleanup authority and clear the active handle before the final reap attempt. The exception path checks session_retired before scanning/killing, and retries reap only while returncode is None. |
| F3/B: another signal restarts emergency cleanup | Closed | Lines 329–340 latch _FORCE_EXITING before entering kill_session. A further callback skips the cleanup body and executes the finally termination path. cli() resets the latch for a new invocation. |
| F1: stale member PID can kill a replacement process | Closed in pidfd mode; explicitly not fully closed in fallback | Lines 206–223 open the pidfd before validating SID, then signal through that descriptor. The fallback retains the last check-to-os.kill window; its comment and mode log accurately disclose this. |
| A: EPERM on one member prevents later members being handled | Closed for the specified PermissionError/ProcessLookupError cases | Lines 270–287 continue the batch after permission denial, then fail. Lines 300–313 also attempt session processing after a denied leader-group kill. This is not a guarantee that every descendant has terminated after an error. |
| Partial or unreadable scan treated as empty | Closed | Lines 226–250 preserve partial observations in an exception; lines 283–289 handle errors before allowing an empty-session return. |
| Whole-scan deadline overrun | Improved as requested, not a hard real-time bound | The same absolute deadline reaches scan and member signaling, with checks per entry and after stat revalidation. A kernel call, scheduling delay, or Popen itself can still overrun wall time. The new comment acknowledges this. |
| Dead group helpers and misleading active-handle name | Closed | The old group functions are removed; the active handle is _ACTIVE_SESSION. |

The ordinary lifetime argument remains sound: start_new_session=True creates the child session; waitid(WNOWAIT) observes its exit without releasing the leader PID; call() does not use Popen.poll()/wait()/communicate() to reap it early; and SIGCHLD is set to default for the operation. This assumes the helper's existing single-owner model—no unrelated thread or injected competing reaper consumes its child status.

If reap_child performs waitpid and then fails before setting returncode, the retry can report ECHILD. That is a visible failure, not permission to reacquire scan/kill authority from the old numeric PID. The fourth retirement test correctly checks this extra window. A metadata-write failure after successful reaping also cannot trigger a session kill. The SystemExit(0)+cleanup-error guard at lines 445–448 is useful: a successful exit request cannot turn failed cleanup into success.

The initial killpg(sid, SIGKILL) is still numeric, but its group identity is anchored by the unreaped leader while the helper uses it. The new per-member pidfd protection addresses a different lifetime: that anchor does not reserve every descendant PID. I found no new production call path that uses the session handle after its final reap has been attempted.

**Low-priority finding L1 — the literal retirement claim is slightly stronger than the publication order.**

Locations: lines 416–417 and 438–439. There is one assignment boundary where session_retired is already True but _ACTIVE_SESSION still contains the SID. A second-signal callback there can call kill_session. I reproduced that with a line-event injection and mocked signaling at line 417.

This is **not an unpinned-SID bug**: the reap has not started, so the original leader still anchors the number. It does mean “a retired SID is never used on any path” is not literally true. The actual safety statement, “no further scan/kill after final reap can release the identity,” holds.

Optional candidate, if retaining the stronger invariant in the report:

```diff
--- a/packaging/clang-bolt-helper.py
+++ b/packaging/clang-bolt-helper.py
@@ -413,8 +413,8 @@
                            str(error))
                 raise GateError(primary) from error
             # Retire scan/kill authority before a reap can release the SID.
+            _ACTIVE_SESSION = None
             session_retired = True
-            _ACTIVE_SESSION = None
             require(reap_child(process) == rc, 'child exit status changed while reaping')
             reaped = True
         text = log.read_text(errors='replace')
@@ -435,8 +435,8 @@
                     kill_session(process.pid, 10)
                 except Exception as failure:
                     cleanup.append(str(failure))
+            _ACTIVE_SESSION = None
             session_retired = True
-            _ACTIVE_SESSION = None
             if process.returncode is None:
                 try:
                     reap_child(process, 1)
```

Side effects: the emergency handle is withdrawn one assignment earlier. A signal in that tiny interval no longer retries the just-completed/attempted cleanup. An ordinary exception before the retirement assignment can still use the local, unreaped leader safely. Child commands, masks and compilation outputs are unchanged.

Test: inject immediately before session_retired=True on both success and failure paths and assert _ACTIVE_SESSION is already None; retain all existing reap fault-injection tests. This is a follow-up, not a release blocker on identity-safety grounds.

**2. pidfd acquisition, revalidation, failure and closure**

The pidfd sequence at lines 206–216 is correct:

1. Check the deadline.
2. Open a pidfd for the observed numeric PID.
3. Re-read /proc/<pid>/stat after acquisition.
4. Check the deadline again and require the current SID to match.
5. Send SIGKILL through the pidfd, then close it in finally.

Opening the pidfd alone would not fix reuse before the open. The post-open SID check supplies the missing ownership check. Conversely, if the process represented by the descriptor exits and the pathname is later reused, the descriptor does not retarget the replacement. It refers to the old process instance. Checking starttime is not required on this pidfd path; a newly observed process genuinely in the same still-anchored session is also within the step's cleanup scope.

Python provides both APIs from 3.9, but availability of Python names and support by the executing kernel/policy are separate matters. See the official [os.pidfd_open documentation](https://docs.python.org/3.9/library/os.html#os.pidfd_open) and [signal.pidfd_send_signal documentation](https://docs.python.org/3.9/library/signal.html#signal.pidfd_send_signal).

I found no ordinary descriptor leak: successful opens in both the capability probe and member path have finally-based close coverage. Tests cover disappearing /proc state, denied signal sends, a missing send API after acquisition, and deadline expiry after revalidation. My real foreign-session/valid-session check left the parent fd count unchanged, 8 before and 8 after the two helper calls.

Runtime failures deliberately differ from initial capability selection:

| Runtime member failure | Current result |
|---|---|
| ESRCH / ProcessLookupError | Treat as gone and continue; a later complete empty scan may succeed. |
| FileNotFoundError while re-reading stat | Treat as gone and continue. |
| EPERM or EACCES mapped to PermissionError | Record the member failure, try later members, then raise a failed cleanup/check. No mode change. |
| ENOSYS, EMFILE, ENFILE, EINVAL or another non-permission OSError | Abort that pass immediately; call() reports cleanup failure. No silent fallback and no claim that later members were handled. |

I verified the runtime distinction with injected acquisition errors: ESRCH and both permission errnos reached both modeled members; ENOSYS and EMFILE stopped at the first. This is not a violation of A's stated permission-error requirement. It does limit the broader phrase “failure is aggregated”: **not every runtime failure is aggregated**. Under such failure, remaining jobs can survive; the RPM helper reports failure rather than guaranteeing containment.

Suggestion, if best-effort continuation for additional OSError cases is desired: change the per-member PermissionError catch at line 281 to OSError, after the existing disappearance/deadline catches, and retain the aggregated nonzero result. Do not change the mode after spawn. Add a two-member fixture where the first acquisition raises a non-permission OSError and the second uses a real owned pidfd. This is optional robustness, not necessary to close the specified A case; resource exhaustion or an unsupported API may make every subsequent attempt fail too.

**3. Fallback selection and seccomp compatibility**

Lines 177–196 implement the requested selection rule accurately: absent API/AttributeError, ENOSYS and EPERM select fallback-recheck; other probe errors escape before Popen. The mode is logged once when successfully selected and cached. Probe failure leaves the mode unset and produces no SESSION_KILL_MODE line; it does not silently select fallback.

**Yes, a seccomp policy can choose an errno that makes every spawning call fail on that build root.** In isolated test-owned subprocesses I installed actual filters denying pidfd_open with four different errnos:

| Filter return | Observed mode | Reached the Popen test sentinel? |
|---|---|---|
| ENOSYS | fallback-recheck, logged | Yes |
| EPERM | fallback-recheck, logged | Yes |
| EACCES | Unset; GateError before spawn | No |
| EINVAL | Unset; GateError before spawn | No |

The sentinel never launched a build command. These are real seccomp filters, not errno mocks. They demonstrate a compatibility possibility, **not evidence that a Tizen worker currently uses either failing policy**. Whether a failed call aborts the entire RPM or is handled by an optional wrapper depends on the caller; this helper-only review does not claim all RPM modes necessarily fail.

Seccomp's ERRNO action can supply the errno selected by the filter. Policies can also trap or terminate a process instead of returning a catchable error. A finite errno allowlist cannot promise universal compatibility. See the primary [Linux seccomp filter documentation](https://docs.kernel.org/userspace-api/seccomp_filter.html#return-values).

The distinction between EPERM and EACCES is a policy choice, not a pidfd implementation error. The earlier task explicitly chose the narrow rule. I would not silently turn EINVAL, EMFILE or arbitrary failures into the weaker mode. Before production use, qualify the probe inside the actual worker/root and record its selected mode and any errno. The report's host-kernel success does not establish that root's seccomp/LSM policy.

If a real supported worker denies pidfds using EACCES and fallback there is approved, the narrowly scoped compatibility patch is:

```diff
--- a/packaging/clang-bolt-helper.py
+++ b/packaging/clang-bolt-helper.py
@@ -188,7 +188,7 @@
         except AttributeError:
             mode = 'fallback-recheck'
         except OSError as error:
-            if error.errno not in (errno.ENOSYS, errno.EPERM):
+            if error.errno not in (errno.ENOSYS, errno.EPERM, errno.EACCES):
                 raise
             mode = 'fallback-recheck'
         print('SESSION_KILL_MODE='+mode, file=sys.stderr, flush=True)
```

Side effects: additional denied hosts use the explicitly weaker numeric recheck policy. This does not handle a seccomp kill/trap or guarantee that ordinary kill is permitted. Test both acquisition and send-probe EACCES, one fallback log line, descriptor closure after a successful open, and continued pre-spawn failure for resource/argument errors. **This is conditional advice, not a finding that the current worker requires this change.**

Fallback itself remains a known residual risk, lines 218–223: another process can replace the checked PID after the final SID/starttime read and before os.kill. Starttime is helpful validation, not an atomic handle. The current comment is accurate; keep the acceptance explicitly scoped to that weaker policy rather than claiming F1 is universally eliminated.

**4. Signals, the latch and the spawn window**

The _FORCE_EXITING latch is placed before the potentially lengthy emergency call. Once set, a later callback reaches finally without starting another scan. Exception paths also run finally. Resetting the incoming signal's disposition to SIG_DFL and resending it intentionally terminates the helper without restoring the original user handlers; this preserves the previous force-exit contract.

The latch is not a thread synchronization primitive, but this helper uses Python callbacks in the main interpreter thread. Nested delivery is the relevant concern. If another signal arrives just before the latch store, the nested callback can perform the force-exit operation; normal execution cannot then resume the outer cleanup after the process has terminated. A mock that makes self-termination return must not be mistaken for a real continuation path. Python documents the callback execution model in [Execution of Python signal handlers](https://docs.python.org/3.9/library/signal.html#execution-of-python-signal-handlers).

The deferred-second-signal mechanism at lines 394–405 remains intact:

- While spawning, a callback records the second signal rather than raising out of Popen.
- After Popen succeeds, the SID is published before _SPAWNING becomes false.
- On Popen failure, there is no published process handle to kill; the deferred terminal action still executes.
- A new signal between clearing _SPAWNING and replaying the saved signal sees the published identity and can terminate directly.
- There is no new pthread_sigmask/preexec_fn step, so this change does not introduce a blocked mask inherited by the child.

I reproduced one emergency entry followed by immediate HUP termination in a fresh owned subprocess. To honor the review's ban on bare-PID signaling, the test's self-resend was adapted to pidfd_send_signal on its own pidfd; the actual Python handler and disposition restoration ran, while kill_session was a deliberately slow mock. That proves the latch/termination scheduling, not execution of the full emergency scan under an actual unkillable process.

Two limits remain, rather than regressions:

- Standard signals can coalesce, and the old first-callback read/store sequence is not a promise to count every signal send. This patch fixes repeated cleanup after cancellation has been recorded; it does not make signal counting atomic.
- A further force signal may deliberately abandon cleanup. If a member is unkillable, permission-denied, or already escaped via setsid, immediate helper termination does not prove it died. The implementation and report should retain “best effort” for this path.

**5. Existing behavior and deadline diagnostics**

I found no unintended change to the reviewed normal contracts: an ordinary zero-exit command drains its session before final reap; long-lived descendants still fail the step; command failures/timeouts invoke cleanup; the first cancellation remains recorded; and a force cancellation terminates by signal. The mode probe is a new pre-spawn failure point, discussed above.

SIGCHLD restoration remains in call()'s outer finally at lines 458–461, including probe failure and argument/logging failures inside its try. Normal cleanup/reap happens first. If reap itself times out or fails, the previous disposition is still restored after that failed attempt; this is not an unconditional guarantee that all children have been reaped. In particular, restoring an inherited SIG_IGN can discard a later child exit status after an already-reported failure. That behavior predates this patch and is not silently converted to success here.

The first signal during success-drain still waits for that drain/check to finish before the higher-level cancellation result is returned. Popen startup, filesystem activity and scheduling are not all within the cooperative cleanup deadline. Neither behavior was newly introduced or claimed solved by this patch.

**Low-priority finding L2 — a new timed-out scan can erase the last useful observed-member snapshot.**

Locations: lines 227, 264–269 and 283–285. After one scan has observed members, the next scan can enter with an expired deadline and raise SessionDeadlineError(..., []). wait_session_exit replaces its members with this empty partial result. The final “last observed members” diagnostic then omits members that the immediately preceding scan actually observed. I reproduced this with a two-scan fault model. The step correctly fails; it never returns empty-session success.

Optional diagnostic-only candidate:

```diff
--- a/packaging/clang-bolt-helper.py
+++ b/packaging/clang-bolt-helper.py
@@ -257,6 +257,7 @@
     # Deadlines are cooperative; an individual kernel operation can overrun.
     if deadline is None:
         deadline = time.monotonic()+timeout
+    last_observed = []
     while True:
         errors = []
         deadline_error = None
@@ -282,9 +283,12 @@
                     errors.append('PID %d: %s' % (pid, error))
         if errors:
             if deadline_error is not None:
-                raise SessionDeadlineError("; ".join(errors), members)
+                observed = members or last_observed
+                raise SessionDeadlineError("; ".join(errors)+
+                    "; last observed snapshot: "+repr(observed), observed)
             raise GateError('session cleanup/check failed: '+'; '.join(errors)+
                             '; last observed members: '+repr(members))
+        last_observed = members
         if not members:
             return
         if time.monotonic() >= deadline:
```

Side effects: keep one prior snapshot for error reporting; do not use it to send signals or declare current liveness. The snapshot is explicitly historical and can contain already-exited processes. No cleanup retry or timeout budget is added.

Tests: a nonempty completed scan followed by an immediate incomplete scan with no entries must report the previous snapshot; a first-ever empty incomplete scan must still fail without inventing members; a partial current scan must report its observations. Also avoid interpreting the existing “with live descendants” prefix as proof of current liveness when the underlying exception is SessionDeadlineError: in that case the gate established only that an empty session could not be verified.

**6. Meaning and gaps of the 34 tests**

The new tests are useful regression tests, not merely mock calls that always turn green. Roughly twelve create real processes, often with fault injection; the other twenty-two exercise deterministic control/error paths. Important distinctions:

- Retirement tests, test_114.py:29–73, use actual child exits and real waitpid, then inject failures at the dangerous boundaries. Mocking kill_session makes an erroneous post-reap kill observable without actually risking a reused identity. These are particularly valuable.
- pidfd tests at lines 116–136 check a real foreign-session process and a real matching process, plus exception closure. The foreign-session case models a stale observation; it does not force kernel PID reuse.
- The force timing test at lines 92–114 uses real signals and a real helper process, but kill_session is replaced by sleep. It demonstrates one emergency entry, not successful cleanup of Ninja-style jobs.
- Permission tests at lines 176–213 verify iteration, error aggregation and partial-scan handling primarily with mocks. “The next member was attempted” is weaker evidence than “the next live process died.” My supplementary owned-process test exercised real pidfd delivery to that second member and verified its exit while the denied member remained alive until test cleanup.
- Deadline mocks at lines 219–245 test the branches precisely. They do not measure the maximum duration of an actual blocked /proc read or a large production process table.
- The setsid test at lines 251–257 creates a directly owned child already in another session. It checks session exclusion, not the full lifecycle of a descendant escaping a managed step. The older suite/report contains the fuller escape scenario; the new isolated test should not be described as proving containment.
- The seccomp and capability tests currently cover the specified mocked errors, not all supported-worker policies. Retain an actual-root capability check; consider adding the isolated ERRNO filter cases used here.

Useful additions are the two low-priority boundary fixtures above; runtime pidfd_open permission failures through wait_session_exit rather than only the member function; acquisition success followed by ESRCH from pidfd_send_signal; and a real owned multi-process-group EPERM case. Preserve the existing timeout/cancel/SIGCHLD and spawn-boundary regressions rather than replacing them with the new mock-only cases.

**Fresh validation performed for this review**

| Check | Result |
|---|---|
| Supplied safe subset: 27 tests | 27 passed. Seven tests involving additional numeric signaling/cleanup paths were not rerun unchanged under this review's stricter signaling rule. |
| Real pidfd foreign-SID skip and matching member kill | Foreign process survived the helper call; matching process exited by SIGKILL; fd count unchanged. |
| Two owned members, first acquisition denied, second signaled | Both attempted; second exited after real pidfd delivery; helper raised; denied member cleaned up by the test through its owned handle. |
| Actual isolated seccomp filters: ENOSYS/EPERM/EACCES/EINVAL | Outcomes exactly match the table above. No build command launched. |
| Runtime acquisition error matrix | ESRCH continues; permission failures aggregate; ENOSYS/EMFILE abort without fallback. |
| Real repeated-signal scheduling with pidfd self-resend adaptation | One emergency entry; terminated by HUP promptly after the further signal. |
| Retired-flag/publication boundary injection | Callback can still see the old active handle before it is cleared; leader is still unreaped. |
| Prior observation followed by incomplete empty scan | Failure retained, previous observed-member diagnostic lost. |

Probe scripts, raw results and the supplied-subset log are in `/tmp/codex-review114-i65lcrdo/`. The environment is CPython 3.12 on Linux `6.17.0-1033-oem`; this is not an actual Tizen worker/Python 3.9 qualification. Tests ran under the requested low-resource limits. All real signaling in these new probes used pidfds referring to processes created and held by the tests; no kill-by-name or bare-PID kill was executed. The product helper and repository were not modified.

**Final decision:** accept the changes as closure of the previously demonstrated defects, subject to the already accepted weaker fallback policy. No mandatory product-code correction emerged from this review. L1/L2 are small follow-ups; actual worker capability/seccomp qualification remains an operational requirement. Do not claim universal PID-reuse safety in fallback mode, guaranteed descendant containment after an error/force exit, or a hard wall-clock cleanup bound.
