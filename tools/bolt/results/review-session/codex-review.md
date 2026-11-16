# Review: session-based cleanup in clang-bolt-helper.py

**Recommendation: modify before accepting the new cleanup implementation.** Tracking the session is the right correction for Ninja jobs that create their own process groups. The normal success, timeout and second-signal paths worked in the process tests I ran. However, the new raw per-PID SIGKILL loop can signal an unrelated process after PID reuse. The unreaped session leader does not protect those member PIDs. Use pidfds with membership revalidation, or another containment mechanism with equivalent guarantees, before relying on this in a shared build environment.

There are two smaller issues: exceptional unwinding can attempt session cleanup after the leader has already been reaped, and the force-exit handler can re-enter its cleanup loop and exceed its nominal one-second budget. The deadlines are cooperative rather than hard wall-clock bounds even without re-entry.

## Reviewed version and validation scope

I found task 111 and reviewed its additions on top of task 110:

| Input | Bytes | SHA256 |
|---|---:|---|
| `session-tracking-110-20261116/final-product.diff` | 7,358 | `92cadfb7f05124626fda3e87b57748444a7e0618b490c28c7fccad2e699db087` |
| `ps5-final-111-20261116/implementation.diff` | 1,564 | `a65e8241a60a5e0f14c30cb599b1d963f70409faaec5311b5cc361fc97ea16dc` |

Both are under `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/`. I also read task 111's `resume/unchanged-product-check.json` and `implementation-check.json`. The former identifies the same implementation diff; the latter records a comment-only helper change and the two spec fixes. I independently reconstructed the final files by applying both diffs with exact context checks to the previously verified preimage.

Resulting Git blob identities:

- `packaging/clang-bolt-helper.py`: `2ad38975b10dadc09ca0675f6dfa105daf1a4de7`, 2,020 lines.
- `packaging/llvm.spec`: `ce6284ae26e5bca06a9fc1703a4e34ce6f961d5e`, 992 lines.

**Helper line numbers below refer to that task-111 result.** Task 111 does not alter the session-control behavior. Its spec changes reset cached hybrid settings in off mode and retain Python 3.9 as a converter requirement; its helper comment corrects the SIGCHLD explanation. I found no additional process-control concern in those additions. This is not a new full review of the entire spec.

I ran Linux process tests using CPython 3.12.3, real sessions/process groups and real signals. Fault-injection tests selected otherwise difficult race windows. The test harness was a subreaper solely to clean up its own test descendants; production code is not a subreaper. No LLVM or RPM build was run, no natural kernel PID-reuse event was induced, and no real uninterruptible-sleep process was created. The pidfd candidate was exercised on this host, not on a Tizen worker kernel or Python 3.9 installation.

Temporary reconstructed files and tests are under `/tmp/codex-review-session-446b4c80/`, including `review-test-results.json` and `escape-force-results.json`. Product files were not changed.

## 1. SID pinning and lifecycle

### Correct on the intended ordinary paths

**Locations:** `clang-bolt-helper.py:152–158,190–237,291–356`.

`start_new_session=True` makes the direct child a session leader with SID equal to its PID. The leader's PID is not available for reuse while that child remains unreaped. With SIGCHLD reset to default and no competing reaper, `waitid(..., WNOWAIT)` observes termination without releasing that reservation. Thus the leader provides a suitable anchor while the success drain or ordinary error cleanup scans the session.

The parser selects the correct `/proc/<pid>/stat` fields: after the command-name closing parenthesis, `fields[3]` is the session ID and `fields[17]` is the thread count. Matching SID catches jobs that use `setpgid()` while remaining in the original session. Ordinary zombie/dead entries are excluded, while a zombie thread-group leader with additional threads remains conservatively counted.

The initial `killpg(sid, SIGKILL)` is safe against unrelated-group reuse while the original leader remains reserved: the session leader's original process-group number is the same pinned number. It does not, by itself, signal the other groups in that session.

Clearing `_ACTIVE_GROUP` before reaping is correct for the signal handler. It prevents the handler from using the SID after the normal cleanup path has intentionally released its anchor. The comment that this variable now contains a SID is important.

### F2 — General: the ordinary exception path can still use a SID after reaping

**Locations:** `:332–334` and `:346–356`.

The answer to “is the anchor retained on **all** paths that scan or kill?” is no. `reaped` becomes true only after `reap_child()` returns and its result passes `require()`. If an exception occurs after the actual waitpid has reaped the leader but before that flag is set, the outer exception handler still executes `kill_session(process.pid, 10)`. Clearing `_ACTIVE_GROUP` protects the signal handler but does not protect this direct call using the local `process.pid`.

I reproduced this with a wrapper that performed the real reap and then raised OSError. The exception path attempted `kill_session()` once with the already-reaped child's numeric SID and attempted another reap, which reported ECHILD. I intercepted the second kill call; no unrelated session was targeted in the test.

This is an exceptional-path weakness, not evidence that routine TERM/INT/HUP necessarily raises in that window. Their first-signal handler records cancellation instead of raising. A failure after reaping or another asynchronous exception nevertheless invalidates an unconditional “pinned on every path” claim. With a quiescent old session and PID reuse, the extra kill can act on a new session/group.

**Candidate change:** track retirement of the session-control handle separately from successful completion of reaping. Retire it before attempting the final reap, and never reacquire cleanup authority from a bare PID afterward:

```diff
--- a/packaging/clang-bolt-helper.py
+++ b/packaging/clang-bolt-helper.py
@@
     process = None; reaped = False; primary = None
+    session_retired = False
     previous = signal.getsignal(signal.SIGCHLD)
@@
                 raise GateError(primary) from error
+            session_retired = True
             _ACTIVE_GROUP = None
             require(reap_child(process) == rc, 'child exit status changed while reaping')
@@
         cleanup = []
         if process is not None and not reaped:
-            # Keep the unreaped leader as a SID anchor until session cleanup ends.
-            try:
-                kill_session(process.pid, 10)
-            except Exception as failure:
-                cleanup.append(str(failure))
+            if not session_retired:
+                # No final reap has been attempted while this handle is live.
+                try:
+                    kill_session(process.pid, 10)
+                except Exception as failure:
+                    cleanup.append(str(failure))
+            session_retired = True
             _ACTIVE_GROUP = None
-            try:
-                reap_child(process, 1)
-            except Exception as failure:
-                cleanup.append(str(failure))
+            if process.returncode is None:
+                try:
+                    reap_child(process, 1)
+                except Exception as failure:
+                    cleanup.append(str(failure))
```

**Side effects:** a reap error still fails the step, but it no longer causes a fresh scan/kill through a retired numeric SID. If the direct child has not actually been reaped, the code can still retry reaping. A failure during cleanup does not become success. This does not solve pre-existing cases in which Popen fails without returning any child handle.

**Tests:** inject an error before waitpid, after a real waitpid but before `reaped=True`, and during metadata writing after successful reaping. Assert that cleanup never signals a retired SID, that an available direct-child status is retained, and that all failures remain nonzero. Retain ordinary timeout/cancel tests and spawn-window tests.

## 2. Per-PID SIGKILL and PID reuse

### F1 — Important: the new scan-then-kill loop can kill an unrelated process

**Location:** `clang-bolt-helper.py:214–224`.

The loop saves numeric PIDs from a complete `/proc` scan and later passes them to `os.kill()`. During that interval a member can exit, be reaped by its parent/adopter, and have its PID reused by a process outside the session. The unreaped leader pins the SID and its own PID; it does not reserve every descendant PID in the scan result. Catching ProcessLookupError only handles a number that is unallocated at the time of kill. It does not protect an already reused number.

This matters in shared build environments: the replacement process can belong to another build under the same UID, or be signalable by a privileged build process. The scan-to-kill interval includes the remainder of the host-wide scan and earlier kill operations; it is not necessarily one adjacent pair of system calls.

The probability is usually low on a quiet system with a large PID space, but it is not zero and cannot be quantified from these materials. PID churn, namespace/PID-space constraints and slow scans increase exposure. A low expected frequency is not a correctness guarantee for SIGKILL.

**Executed model:** I supplied a deterministic stale scan result whose PID now identified a separate, test-owned session. The current loop killed that process with SIGKILL. This models the lookup result after reuse; I did not force real kernel PID reuse. A candidate that opened a pidfd and then revalidated the SID skipped the unrelated process. The same candidate successfully killed a process whose actual SID matched.

### Recommended implementation: open pidfd, revalidate membership, signal through the fd

`os.pidfd_open()` and `signal.pidfd_send_signal()` are available in Python 3.9 on suitable Linux builds. Kernel support is a separate requirement: pidfd_open was added in Linux 5.3; pidfd_send_signal in Linux 5.1. The fd identifies a process instance instead of doing another numeric-PID lookup when sending the signal. See [pidfd_open(2)](https://man7.org/linux/man-pages/man2/pidfd_open.2.html), [pidfd_send_signal(2)](https://man7.org/linux/man-pages/man2/pidfd_send_signal.2.html), and the [Python 3.9 signal APIs](https://docs.python.org/3.9/library/signal.html#signal.pidfd_send_signal).

Opening a pidfd **after** the scan is not sufficient by itself: the number could already have been reused before the open. Revalidate session membership after opening it. If the fd refers to a still-live unrelated process, that process cannot simultaneously have its PID reused for the original session. If the fd's process has already died and the later `/proc` read sees a different process, sending through the old fd cannot kill that replacement.

The following candidate deliberately fails before spawning if the safe signaling API is unavailable. This is a policy choice, discussed under fallbacks below:

```diff
--- a/packaging/clang-bolt-helper.py
+++ b/packaging/clang-bolt-helper.py
@@
-def wait_session_exit(sid, timeout=10, *, kill=False):
+def require_pidfd_signalling():
+    require(callable(getattr(os, 'pidfd_open', None)) and
+            callable(getattr(signal, 'pidfd_send_signal', None)),
+            'session cleanup requires Python pidfd APIs')
+    try:
+        fd = os.pidfd_open(os.getpid(), 0)
+        try:
+            signal.pidfd_send_signal(fd, 0, None, 0)
+        finally:
+            os.close(fd)
+    except OSError as error:
+        raise GateError('session cleanup requires usable pidfds; check the '
+                        'host kernel and sandbox policy: '+str(error)) from error
+
+
+def kill_session_member(sid, pid):
+    try:
+        fd = os.pidfd_open(pid, 0)
+    except ProcessLookupError:
+        return
+    try:
+        try:
+            current = proc_stat('/proc/%d/stat' % pid)
+            if current[4] != sid:
+                return
+            signal.pidfd_send_signal(fd, signal.SIGKILL, None, 0)
+        except (FileNotFoundError, ProcessLookupError):
+            pass
+    finally:
+        os.close(fd)
+
+
+def wait_session_exit(sid, timeout=10, *, kill=False):
@@
             # Scan again after killing to catch forks during the previous scan.
             for pid, state in members:
-                try:
-                    os.kill(pid, signal.SIGKILL)
-                except ProcessLookupError:
-                    pass
+                kill_session_member(sid, pid)
@@
         if previous != signal.SIG_DFL:
             signal.signal(signal.SIGCHLD, signal.SIG_DFL)
+        require_pidfd_signalling()
         save(log.with_suffix(log.suffix+'.argv.json'),
```

The capability probe uses signal zero on the helper's own pidfd. It checks actual kernel/sandbox support before any child is created, rather than waiting for cancellation to discover that the API is unusable. The normal scan still requires the original session anchor; apply F2 as well.

**Side effects:** this raises the effective host requirement beyond “Python 3.9 on any Linux.” On supported hosts it adds short-lived fd operations, one member at a time, and a small per-call probe. File-descriptor exhaustion, permission errors or later sandbox changes can still make cleanup fail and must remain visible on ordinary failure paths. The emergency handler is best effort and can still terminate with incomplete cleanup.

**Required tests:** member exits before pidfd_open; PID replaced by an unrelated session before open; member exits after open; `/proc` disappears after open; a matching member; an unrelated matching numeric PID model; descriptor closure on every exception; ENOSYS/seccomp denial/absent Python APIs before Popen; resource exhaustion during cleanup. Run real multiple-process-group Ninja tests on the oldest supported worker kernel and Python build.

### Fallback choices

| Approach | Assessment |
|---|---|
| pidfd plus post-open SID validation | Recommended practical fix on supported Linux; prevents signaling a replacement merely because it has the same PID. |
| Re-read SID/start time immediately before raw `kill(pid)` | Narrows the race but does not close the final check-to-kill window. Suitable only as an explicitly accepted weaker policy, not an equivalent guarantee. |
| Kill each discovered process group | Catches Ninja's layout, but discovered group IDs can also disappear/reuse. It does not generally remove the identity race. Only the original leader's group has the stated anchor. |
| `killpg(sid)` alone | Safe while anchored, but repeats the original functional defect: it does not kill other groups in the session. |
| Per-step cgroup containment with a supported kill mechanism | Stronger option, also covering setsid descendants that remain in the cgroup; needs worker permissions/delegation and correct lifecycle setup. Not established by the current RPM helper. |
| Explicit unsupported-host failure before spawning | Safe default when the required signaling mechanism is unavailable; needs a clear diagnostic and worker compatibility check. |

Do not silently fall back from pidfd failure to the current raw-PID loop while continuing to claim unrelated-process safety. RPM 4.14.1 says nothing about the running Linux kernel's pidfd support. A parent/subreaper helps reap children, but making the helper a subreaper alone does not reserve live grandchildren against their current parents reaping them and does not solve this scan/kill race.

## 3. Cleanup inside the Python signal handler

### The handler is Python-level, but it is still re-entrant

**Locations:** `clang-bolt-helper.py:245–261,311–321`.

This is not a raw POSIX C signal handler executing arbitrary Python from an async-signal context. Python dispatches its handlers in the main interpreter thread. Therefore calling Python code here is not automatically a violation of the C async-signal-safe-function rules. The actual concerns are re-entry, delayed execution, blocking operations and exceptions. See [Python's signal execution model](https://docs.python.org/3.9/library/signal.html#execution-of-python-signal-handlers).

The existing spawn guard remains logically useful: while `_SPAWNING` is true, a second signal is recorded rather than starting cleanup with an unpublished SID. Once Popen returns and publishes its PID, the finally clears the flag and replays the saved signal. A fresh signal at that finally boundary sees the published SID. No new child signal mask is introduced.

The new `except Exception: pass` makes the emergency path best effort: an inspection/permission/timeout error is followed by termination of the helper, not proof of successful session cleanup. The leader's group is attempted first, which helps if `/proc` scanning fails, but jobs in other groups may survive that failure. This is acceptable only as an explicitly limited emergency behavior, with ordinary cancellation retaining useful cleanup diagnostics.

### F3 — General: another signal can recursively restart the cleanup budget

**Location:** `:252–259`; deadline placement at `:212–228`.

There is no force-exit-in-progress guard. While the second-signal handler is sleeping or scanning in `kill_session(..., 1)`, another TERM/INT/HUP can invoke `record_cancel()` again. It starts another one-second kill loop. Several deliveries can create nested scans and postpone self-termination. This is not the same as the earlier unpublished-child race.

**Executed test:** with a simulated unkillable session member, one second-signal handler began cleanup and another TERM arrived 0.25 seconds later. The actual handler/kill-loop code entered cleanup twice and terminated after approximately 1.267 seconds from the first force-cleanup request. The member and kill operations were mocked to avoid creating an unkillable process. This demonstrates deadline restart/re-entry, not a real kernel D-state test.

**Candidate change:** latch emergency cleanup before entering it; another cancellation during that cleanup immediately terminates instead of starting another scan. Use finally for the terminal action:

```diff
--- a/packaging/clang-bolt-helper.py
+++ b/packaging/clang-bolt-helper.py
@@
 _DEFERRED_SECOND_SIGNAL = None
+_FORCE_EXITING = False
@@
 def record_cancel(signum, frame):
-    global _CANCEL_SIGNAL, _DEFERRED_SECOND_SIGNAL
+    global _CANCEL_SIGNAL, _DEFERRED_SECOND_SIGNAL, _FORCE_EXITING
@@
-        # Kill the active session before honoring an immediate second signal.
-        # Bound the rescan so an unkillable member cannot delay termination.
-        if _ACTIVE_GROUP is not None:
-            try: kill_session(_ACTIVE_GROUP, 1)
-            except Exception: pass
-        # This second-signal path terminates by signal; original handlers are not restored.
-        signal.signal(signum, signal.SIG_DFL)
-        os.kill(os.getpid(), signum)
+        if _FORCE_EXITING:
+            signal.signal(signum, signal.SIG_DFL)
+            os.kill(os.getpid(), signum)
+            return
+        _FORCE_EXITING = True
+        try:
+            # Best-effort cleanup with a cooperative deadline. A further
+            # cancellation aborts it rather than recursively scanning again.
+            if _ACTIVE_GROUP is not None:
+                try: kill_session(_ACTIVE_GROUP, 1)
+                except Exception: pass
+        finally:
+            signal.signal(signum, signal.SIG_DFL)
+            os.kill(os.getpid(), signum)
         return
@@
 def cli():
-    global _CANCEL_SIGNAL, _SPAWNING, _DEFERRED_SECOND_SIGNAL
+    global _CANCEL_SIGNAL, _SPAWNING, _DEFERRED_SECOND_SIGNAL, _FORCE_EXITING
+    _FORCE_EXITING = False
     _SPAWNING = False
```

**Side effects:** a further signal can deliberately abandon remaining emergency cleanup. That should be documented as the final escape hatch, not advertised as successful cleanup. The first cancellation and spawn deferral remain unchanged. The guard prevents overlapping emergency scan loops but does not turn an individual scan into a hard one-second operation.

**Tests:** second signal during ordinary cleanup; third/fourth signals during the emergency scan, its sleep and per-member signaling; different signal numbers; deferred second signal replay after Popen success/failure; inherited ignored dispositions. Assert one emergency scan loop at most, expected signal termination, and no child launched before a deferred signal can be handled with its published SID.

The earlier first-handler read/store race discussed in the prior review is unchanged by this patch; this review does not claim that every kernel signal send maps to a distinct counted callback. Standard signals may coalesce. F3 addresses the newly expanded re-entrant cleanup work, not signal-counting guarantees in general.

## 4. Timeouts and possible hangs

**Locations:** `:209–237,270–289,311–354`.

The timeouts are **cooperative deadlines**, not hard total wall-clock bounds. `wait_session_exit()` checks its clock after a complete scan and, in kill mode, after all signals for that batch. A slow scan or a large batch can overrun the requested time before the check runs. I injected a 0.15-second scan into a wait with a 0.01-second timeout; it returned the timeout after 0.15 seconds. The comment promising that an unkillable member cannot delay termination needs that qualification.

Nominal budgets, excluding scheduling/I/O overrun and later diagnostics:

| Path | Nominal budget after launch/wait starts |
|---|---|
| Child execution timeout at T | T, then up to 10 s session cleanup and 1 s direct-child reap. |
| Leader exits zero near T, descendants never drain | Up to T, then 10 s drain, 10 s cleanup and 1 s reap. |
| First cancellation while child execution is being polled | Cancellation polling latency, then approximately the 10 s cleanup + 1 s reap budgets. |
| First cancellation during the success-drain wait | Up to the remaining 10 s drain before cleanup; the drain itself does not check cancellation. |
| Second signal outside spawning | Nominal 1 s emergency loop, then termination; currently subject to F3 and scan overrun. |
| Second signal while spawning | Deferred until Popen completes; the 1 s emergency budget has not started. |

There is no finite source-enforced worst-case bound across all paths:

- Popen creation/exec setup is outside the later child-execution timeout. Its guard intentionally defers escalation while the child handle is unpublished.
- A filesystem/kernel operation or heavily delayed scan is not interrupted merely because the monotonic deadline passed.
- Repeated force-signal re-entry currently resets the inner budget.
- SIGKILL does not guarantee immediate exit from uninterruptible kernel sleep. The loops normally report failure after their deadlines; they cannot make the kernel finish that task.
- Logging and subsequent error diagnostics are not all included in the local loop timeout.

There is no unconditional blocking wait for the leader in `reap_child()`; it uses WNOHANG and a deadline. That is good. The issue is the overall claim, not a newly introduced `waitpid(..., 0)` hang.

For better practical latency, propagate one absolute deadline through scanning and check it between `/proc` entries and member signals. A partial scan at deadline must report incomplete inspection, never return an apparently empty session. Keep cancellation checks optional for the normal success drain; cleanup must not immediately abort just because the first cancellation has been recorded. These changes reduce ordinary overrun but cannot create a hard kernel-I/O deadline. A hard guarantee needs an external supervisor with the appropriate containment/kill scope.

The timeout exception currently reports the last scanned member list. In kill mode that list may include processes just signaled and subsequently exited; treat it as last-observed membership rather than proof that each listed PID is still live at reporting time. A final rescan can improve diagnostics, subject to the same deadline qualification.

## 5. Descendants that call setsid()

### Acceptable only as an explicit workload constraint

**Location:** `clang-bolt-helper.py:210–211`.

The documented limitation is real: a descendant that creates a new session will no longer match the original SID. I tested a child that forked, had the descendant call setsid(), and then exited zero. `call()` returned success while the new-session descendant remained alive. The test harness killed and reaped it afterward.

Ninja 1.13's ordinary non-console job launch uses `POSIX_SPAWN_SETPGROUP`, not a new session. Therefore the new session approach covers the stated Ninja problem. The relevant upstream source is [Ninja v1.13.0 subprocess-posix.cc](https://github.com/ninja-build/ninja/blob/v1.13.0/src/subprocess-posix.cc#L81-L125).

Fork/exec normally preserves a session; a non-session/group-leader descendant can deliberately create a new one with setsid. See [setsid(2)](https://man7.org/linux/man-pages/man2/setsid.2.html). Ordinary foreground compiler, linker and shell jobs are a reasonable workload for session cleanup, but the executable's top-level name is not proof about every custom command it launches.

Common escape mechanisms to consider in build commands are:

- The `setsid` utility or a daemonizing service/wrapper.
- Python `Popen(start_new_session=True)` in a nested script or test runner.
- `daemon()` or an explicit daemonization sequence that includes setsid.
- A service manager or remote/distributed build service starting work outside this local session.

Changing process groups, shell job control, or simply running a command in the background is not by itself a new session. Do not confuse those with the setsid limitation. Conversely, a custom CMake/Ninja command can run any of the escaping wrappers above. Tests and remote compilation add more possibilities than the narrow certified LLVM build steps.

For the listed, controlled build steps, accepting this limitation is reasonable if the contract is “no live members left in the launched session” and the actual custom commands are checked. It is not sufficient for a claim that arbitrary descendants or all work started by a build step are contained. If that stronger claim is needed, use an appropriately delegated per-step cgroup or another external supervision boundary. A subreaper improves adoption/reaping, but is not an escape-proof containment boundary.

## 6. Other results, tests and final decision

### Correct aspects

- `LiveDescendantsError` replaces the previous message-prefix classification cleanly. Other scan failures remain errors rather than being mistaken for successful drainage.
- Normal zombie leaders do not cause false waits. A successful command with a short-lived child in another process group was allowed to drain.
- Session membership continues after the original parent exits; reparenting alone does not evade the SID scan.
- Cleanup retains the leader during its intended scan/signal work and clears the active SID before final reaping on both main paths. F2 is about exceptional re-entry into cleanup after that retirement, not the normal order.
- Task 111's corrected comment no longer claims ignored SIGCHLD universally turns failures into zero; its spec-only changes do not alter the session algorithm.

### Observed tests

| Test | Result |
|---|---|
| Leader exits zero; separate-PG child exits after 0.15 s | Success after approximately 0.197 s. |
| Execution timeout with a live separate-PG child | Failed after approximately 0.236 s for a 0.15 s execution timeout; child killed by SIGKILL. |
| Successful leader leaves persistent separate-PG child | Failed after approximately 10.140 s with the live-descendant diagnostic; child killed by SIGKILL. |
| Real second cancellation while separate-PG child is alive | Helper terminated by TERM, child by SIGKILL; approximately 0.114 s after the second signal. |
| Simulated stale scan PID now outside the target session | Current implementation killed the test process; pidfd plus SID validation skipped it. |
| pidfd signaling of a matching session member | Member killed successfully. |
| Exception injected after actual direct-child reap | Current implementation attempted session kill again. |
| Slow scan versus short timeout | Deadline overrun reproduced. |
| Another signal during emergency kill loop | Nested cleanup and deadline restart reproduced. |
| Descendant creates a new session | It escaped; helper returned success, consistent with the documented limitation. |

The fault-injection rows establish control-flow weaknesses; they are not measurements of natural PID-reuse probability or production scan latency. The tested pidfd member helper is evidence for that small candidate mechanism, not a claim that all proposed diffs were integrated and certified together.

### Additional maintained fixtures

Add these before relying on the revised contract:

1. Real Ninja 1.13 build jobs in distinct process groups, with success-drain failure, timeout, first cancellation and force cancellation.
2. pidfd acquisition/revalidation races and missing/denied kernel APIs, tested before spawning.
3. Retirement/reap fault injection so a dead numeric SID is never reused by cleanup.
4. Repeated signals during emergency cleanup and the Popen publication/finally boundaries.
5. Zombie-only sessions, a zombie leader with extra threads if a practical fixture is available, `/proc` disappearance and permission errors, and the intended PID namespace/mount configuration.
6. A setsid escape fixture explicitly documenting that the helper does not claim to contain it.

Inspection or signaling errors currently stop that cleanup attempt. On the ordinary path they are recorded; in the emergency handler they are suppressed before force-exit. Neither path can guarantee that all other session groups died after such an error. The actual build root must expose the relevant `/proc` records and permit signaling the children. I would not hide those errors or convert them into successful cleanup. Best-effort continuation after a per-member error can be considered separately, with error aggregation and the same identity safeguards.

Renaming `_ACTIVE_GROUP` to `_ACTIVE_SESSION` and removing unused group-only helpers would improve clarity, but those are suggestions rather than correctness requirements; the current explanatory comment is sufficient for this patch's compatibility needs.

**Final decision:** the move from process groups to sessions is justified and works for Ninja's separate-group jobs. **Change the raw per-PID kill mechanism before accepting the patch for shared-build use (F1).** Also retire SID cleanup authority independently of reaping success (F2), and prevent recursive emergency scan loops or explicitly weaken the force-exit timing contract (F3). Keep the setsid limitation explicit. Python 3.9 alone is not enough to select a race-safe pidfd policy: qualify the worker kernel/sandbox, and choose an explicit unsupported-host behavior rather than silently retaining the unsafe fallback.
