# Review of the LLVM build-helper follow-up: H1–H5 and N1

**Recommendation: accept A+B as fixes for the stated follow-up requests, with qualified cleanup claims.** I found no newly introduced blocking defect in these changes. H2 closes the identified spawn/publication window without adding an inherited signal mask; H1/H5 restore representable SIGCHLD dispositions on normal unwinding; N1 correctly avoids an invalid restoration; H3 and H4 behave as intended.

However, the stronger claim that `call()` cannot leave a running orphaned process group is false. I reproduced an existing successful-leader cleanup hole. I also reproduced an existing nested-handler case in which two delivered signals do not trigger the advertised second-signal termination. These are real findings, distinguished below from regressions introduced by A or B. Fix the former before certifying a general “no running descendants after call” guarantee; the latter is a smaller follow-up unless exact second-signal escalation is a release requirement.

## Inputs and method

I read both supplied diffs in full:

| Input | Bytes | SHA256 |
|---|---:|---|
| A: `round2/candidate-vs-localPS4.diff` | 11,049 | `b4907d047a5a8bcfb95d015f8b17c37c7654c73307fb43d7a8ec87b3a547359b` |
| B: `round3/N1.diff` | 1,104 | `3da50bb165c63beba03e163870d4699744f710e099c99f7fe6e4f64d8ce2bb5f` |

Their common directory is `/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/hq-review-361395/`.

I read the affected functions and their relevant callers/callees in the supplied context, including process management, signal setup/restoration, archive inspection, converter workers/install unwinding, and post/debug-list handling. The context converter is slightly older than A's exact preimage: A also expects an existing startup diagnostic function. Rather than silently apply the diff to a different source, I obtained the exact preimage Git blobs from the existing local evidence repository, applied A and B in a temporary directory with exact hunk-context checks, and verified the resulting blob identities:

- `packaging/clang-bolt-helper.py`: `cf531695c971f5a7fd625c36ede7221097343310`, 1,962 lines.
- `packaging/llvm-static-archives-native.py`: `c2f74bfe2d01f9f65de90c56739acf719e5de4b7`, 1,091 lines.
- `packaging/llvm.spec`: `6a66edebc78cccc085ef13c34581868ed77fdb44`, 970 lines.

**All code locations below refer to A+B applied**, not the older context files. Product files were not modified.

I ran targeted tests using CPython 3.12.3 on Linux, including real subprocesses and real TERM/HUP delivery, deterministic trace injection at selected handler/finally boundaries, and synthetic normal/thin archives. These are not a full RPM build, a full archive conversion, or exhaustive scheduling tests on the target Python 3.9 runtime. The signal tests used a test-only subreaper to collect children orphaned by deliberately forced helper exits; that does not grant subreaper behavior to the production helpers.

Python's main-thread handler scheduling and the meaning of `getsignal() == None` are documented in the [Python signal reference](https://docs.python.org/3.9/library/signal.html). The existing `start_new_session` and `restore_signals` behavior is documented in the [subprocess reference](https://docs.python.org/3.9/library/subprocess.html).

## 1. H2: spawn critical section and signal races

### The intended spawn/publication fix is correct

**Locations:** `clang-bolt-helper.py:187–209,239–264,1918–1927`.

The important invariant is: once child creation can begin, `_SPAWNING` remains true until either the child's PGID is published or Popen has raised. A second cancellation records a deferred request while that invariant holds. It does not immediately kill the parent before `_ACTIVE_GROUP` is known.

The relevant interleavings are:

| Signal timing | Result in A+B |
|---|---|
| First signal before `check_cancel()` | No child is launched; the cancellation check fails. |
| First signal after the check but before/during Popen | It records cancellation. A child may still be launched, but the subsequent check takes the normal group-cleanup path. This does not promise zero work after cancellation. |
| Second signal before `_SPAWNING = True` | Immediate termination occurs before this call creates a child. |
| Second signal while Popen is running, or after it returns but before the result/PGID is stored | The signal is deferred; the newly created group can be published before escalation. |
| Second signal after `_ACTIVE_GROUP` is set but before `_SPAWNING` becomes false | Deferred escalation uses the published group. |
| Signal after `_SPAWNING = False`, including during the pending-signal test or reset | The ordinary second-signal branch sees the published group and kills it before terminating the helper. |
| Popen fails before providing a child | The inner finally clears the spawn flag and honors a pending second signal; with no pending second signal, normal exception handling runs. |

Clearing `_SPAWNING` before consuming `_DEFERRED_SECOND_SIGNAL` is not itself a lost-signal window. A fresh second/third signal in that interval takes the immediate path, with the PGID already available. If no fresh signal arrives, the saved request is replayed. Resetting the deferred variable before replay also avoids replaying the same saved value if execution were to continue in a test double.

Calling `record_cancel(pending, None)` from the finally is safe for this purpose: `_CANCEL_SIGNAL` is already set and `_SPAWNING` is false. It reaches the force-exit branch rather than deferring again. If another cancellation handler interrupts that replay, it also sees the published group. Under real default termination, neither invocation needs to return normally. Tests that mock `os.kill()` to return must not confuse the resulting artificial continuation with real execution.

**Observed tests:**

- One TERM injected after a real Popen had created the child but before returning to `call()`: helper exited 143; its direct child had been reaped.
- Two TERMs at that boundary: helper terminated by TERM; the spawned child terminated by SIGKILL.
- HUP injected immediately after the spawn flag was cleared, with one TERM already recorded: helper terminated by HUP; the child terminated by SIGKILL.
- HUP at the same boundary with a deferred second TERM already present: same group-kill result.
- Two TERMs followed by an injected Popen failure: helper terminated by TERM with no child created in that case.

These tests support the identified boundary fix. They do not prove behavior under every possible internal Popen failure after a partially completed fork. Standard exec/setup failures are handled by Popen itself; an arbitrary asynchronous exception or resource failure that prevents Popen from returning its child handle is a broader lifecycle problem, not something this boolean guard can universally solve. The installed cancellation handler deliberately does not raise on its first signal, which avoids that common source of interrupted construction.

### Child masks and dispositions

H2 adds neither `pthread_sigmask` nor `preexec_fn`, and does not change Popen's arguments. It therefore introduces no blocked cancellation mask inherited by the child. This preserves the pre-change subprocess launch behavior.

“Dispositions unchanged” should mean unchanged **relative to the old helper**, not identical to the parent's original signal state: the helper already resets SIGCHLD to default before spawning, `start_new_session=True` creates a new session, and normal exec/subprocess signal handling still applies. Inherited ignored TERM/INT/HUP remain subject to the existing CLI policy, which leaves them ignored.

A second signal is an emergency termination path. It sends SIGKILL to the known group and terminates the helper without completing its Python finally blocks or reaping every descendant. Grandchildren are collected by their adopter; the helper is not a subreaper. A process that escaped the group, or one stuck in uninterruptible kernel sleep, is outside an absolute “all descendants gone now” guarantee.

### R1 — Important, pre-existing: a successful leader can leave running descendants

**Location:** `clang-bolt-helper.py:265–276`; contrast error cleanup at `:283–298`.

When the direct child exits zero, the helper reaps it, clears `_ACTIVE_GROUP`, and records success without checking whether other processes remain in the group. A build wrapper can fork a background process and exit zero. That background process continues after `call()` returns; subsequent cancellation cannot find it through `_ACTIVE_GROUP`.

**Reproduction executed:** the child forked once; the leader printed the descendant PID and exited zero; the descendant slept for 30 seconds in the same process group. `call()` returned success while `/proc/<descendant>/stat` showed state `S`. The test then killed and reaped the descendant. This is a demonstrated lifecycle hole, not a theoretical Popen-window claim, and it exists before A.

**Candidate fix:** require a successful command's group to be quiescent before releasing its unreaped leader. Unexpected surviving descendants should fail the build and enter the existing kill/wait/reap path:

```diff
--- a/packaging/clang-bolt-helper.py
+++ b/packaging/clang-bolt-helper.py
@@
             if rc != 0:
                 primary = 'COMMAND_ERROR: COMMAND_FAILED rc=%d: %s' % (rc, argv[0])
                 raise GateError(primary)
+            require(not live_group_members(process.pid),
+                    'COMMAND_ERROR: command exited successfully with live descendants')
+            # The leader has exited and the group is quiescent. Stop exposing
+            # its PGID before waitpid releases the leader's PID reservation.
+            _ACTIVE_GROUP = None
             require(reap_child(process) == rc, 'child exit status changed while reaping')
             reaped = True
```

**Side effects:** a command that deliberately leaves background work now fails instead of appearing successful; this is appropriate for build steps whose outputs must be complete on return. Successful calls acquire an additional `/proc` scan and can fail if that scan is unavailable. This uses the helper's existing process-group inspection model; it is not a cgroup-level guarantee against adversarial forking or processes that leave the group.

**Tests:** add the successful-leader/background-child reproduction, assert failure and eventual group cleanup; retain a successful ordinary child fixture; test `/proc` read failure. Add a boundary test between direct-child reaping and PGID clearing: the current comment claiming that the leader remains unreaped while `_ACTIVE_GROUP` is exposed is not strictly true on the old success path. Clearing the active PGID before reaping a verified-quiescent group avoids that success-path stale-PGID interval. Error cleanup still needs its existing explicit failure accounting when group cleanup cannot finish.

### R2 — General, pre-existing: nested first handlers can miss escalation

**Location:** `clang-bolt-helper.py:195,209`.

The read of `_CANCEL_SIGNAL` and the first-signal assignment are separate operations. If another signal handler runs after the first invocation has selected the first-signal branch but before line 209 stores the signal, the nested invocation also sees `None`. Both handlers return as first-signal handlers; the outer assignment then overwrites the inner value.

**Reproduction executed:** deliver TERM, and use a trace hook at line 209 to deliver HUP before the outer assignment. Both handlers returned; `_CANCEL_SIGNAL` ended as TERM; the process did not take the immediate second-signal path. This trace deterministically selects an allowed scheduling boundary. It does not measure its natural frequency.

This does not undo H2's protection of a newly created group, and graceful cancellation is still recorded. It does mean that “the second delivered signal always forces termination” is stronger than the implementation. The issue predates A.

**Candidate approach:** record handler receipts with a non-callback built-in operation before classifying first versus subsequent receipts, and separate forced termination from receipt recording. For the supported CPython execution model, an append to a plain list supplies such a recording point. The following is a focused candidate, to be qualified on the target Python as well:

```diff
--- a/packaging/clang-bolt-helper.py
+++ b/packaging/clang-bolt-helper.py
@@
 _DEFERRED_SECOND_SIGNAL = None
+_CANCEL_RECEIPTS = []
 
 
-def record_cancel(signum, frame):
-    global _CANCEL_SIGNAL, _DEFERRED_SECOND_SIGNAL
-    if _CANCEL_SIGNAL is not None:
-        if _SPAWNING:
-            if _DEFERRED_SECOND_SIGNAL is None:
-                _DEFERRED_SECOND_SIGNAL = signum
-            return
-        # Kill the active descendant group before honoring an immediate second
-        # signal. The leader stays unreaped until call() has cleaned its group.
-        if _ACTIVE_GROUP is not None:
-            try: os.killpg(_ACTIVE_GROUP, signal.SIGKILL)
-            except ProcessLookupError: pass
-        # This second-signal path terminates by signal; original handlers are not restored.
-        signal.signal(signum, signal.SIG_DFL)
-        os.kill(os.getpid(), signum)
-        return
-    _CANCEL_SIGNAL = signum
+def force_cancel(signum):
+    if _ACTIVE_GROUP is not None:
+        try: os.killpg(_ACTIVE_GROUP, signal.SIGKILL)
+        except ProcessLookupError: pass
+    signal.signal(signum, signal.SIG_DFL)
+    os.kill(os.getpid(), signum)
+
+
+def record_cancel(signum, frame):
+    global _CANCEL_SIGNAL, _DEFERRED_SECOND_SIGNAL
+    _CANCEL_RECEIPTS.append(signum)
+    _CANCEL_SIGNAL = _CANCEL_RECEIPTS[0]
+    if len(_CANCEL_RECEIPTS) == 1:
+        return
+    if _SPAWNING:
+        if _DEFERRED_SECOND_SIGNAL is None:
+            _DEFERRED_SECOND_SIGNAL = signum
+        return
+    force_cancel(signum)
@@
                     pending = _DEFERRED_SECOND_SIGNAL
                     _DEFERRED_SECOND_SIGNAL = None
-                    record_cancel(pending, None)
+                    force_cancel(pending)
@@
     _SPAWNING = False
     _DEFERRED_SECOND_SIGNAL = None
+    _CANCEL_RECEIPTS.clear()
     previous = {sig: signal.getsignal(sig) for sig in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT)}
```

**Side effects and limits:** this makes escalation depend on recorded handler invocations, not an atomic ordering of kernel signal arrival; standard signals can coalesce and Python does not promise to deliver every send as a separate callback. It also adds state that tests invoking the handler directly must reset. Deferred escalation no longer calls the receipt handler and therefore does not invent another receipt. It preserves the no-mask-across-spawn design.

**Tests:** nested delivery before and after the first append, during first-signal classification, during deferred publication, and during `force_cancel`; test same and different signal numbers. Re-run all H2 group-kill tests. This candidate was not applied to the product and is not claimed to have completed target-runtime certification.

## 2. H1/H5/N1: SIGCHLD restoration and reaping guarantees

### H1 is correctly placed for ordinary unwinding

**Location:** `clang-bolt-helper.py:243–246,277–312`.

The original disposition is captured before the outer try, the helper switches to default before creating a child, and restoration happens after the exception cleanup block. On success the direct child is reaped before restoration. On an ordinary command failure, timeout, or first-signal cancellation, the helper attempts group kill, group quiescence and direct-child reaping before restoration. `SystemExit` and `KeyboardInterrupt` raised inside the protected region also pass through that cleanup before being re-raised.

I tested success, exit 7, timeout, and injected SystemExit/KeyboardInterrupt after child creation, starting with SIGCHLD ignored. In each case the original ignored disposition was restored and the direct child had already been reaped. The first-signal H2 test separately confirmed cancellation reaping.

The answer to “only after **all children are reaped on every path**?” is nevertheless **no**, for reasons that must not be hidden by the wording of H1:

- Cleanup operations have deadlines and can themselves fail. The finally restores SIGCHLD after cleanup has been attempted, not after a proof that every reap succeeded.
- The emergency second-signal path terminates the process; it does not execute normal restoration/reaping.
- The helper cannot waitpid arbitrary grandchildren without being their parent/subreaper.
- R1 permits live descendants on the successful-leader path.
- Arbitrary exceptions during process construction, or during cleanup itself, are not equivalent to the controlled first-signal path.

Restoring `SIG_IGN` does not itself create zombies. If restored while a direct child is still running, however, it can make that child's later exit status unavailable for explicit waiting. Restoring a custom handler can likewise allow that handler to consume a status. Do not suppress or downgrade cleanup failures. If the helper is to become an embedded/reusable process supervisor, explicitly define what happens when it cannot complete reaping; unconditional disposition restoration and an absolute reaping guarantee cannot both be asserted under those failures.

One existing diagnostic limitation remains: cleanup errors accumulated before re-raising SystemExit/KeyboardInterrupt are not appended to a new GateError (`:299–300`). This is not an H1 regression. It is worth logging those cleanup errors before the bare re-raise, while preserving the original exception and cancellation semantics.

### H5 covers argparse and the full conversion/install call

**Location:** `llvm-static-archives-native.py:1034–1091`; worker cleanup at `Commands.run()`, and executor unwinding in `convert()`.

Moving the original body to `_install_main()` and wrapping it with try/finally includes argparse's SystemExit, argument-validation failures, conversion/install errors, and the normal returned status. `log_startup_context()` and `getsignal()` occur before that try, but neither has yet changed SIGCHLD, so their placement does not leave a changed disposition unrestored.

In the normal converter paths, workers execute their own finally blocks and the executor is joined before installation unwinds to this outer restoration. The outer wrapper does not restore SIGCHLD halfway through ordinary worker cleanup. I tested argparse failure, a normal return, RuntimeError, SystemExit and KeyboardInterrupt at the delegated-body boundary; restoration worked. Those boundary tests do not substitute for a real multi-worker LLVM conversion/cancellation run.

The converter's documented scope remains relevant: it reaps direct children, signals group members, and is not a subreaper; it does not wait for every descendant after SIGKILL. OS failures or another exception interrupting its cleanup can still defeat an absolute reaping guarantee. H5 repairs the restoration coverage; it does not independently strengthen that process-control scope.

### N1 is necessary and correct, with an explicit limitation

**Location:** `clang-bolt-helper.py:311–312`; `llvm-static-archives-native.py:1086–1087`.

`getsignal()` can return `None` for a disposition not represented by a Python handler. `signal.signal(..., None)` is invalid. The new guard prevents that TypeError from masking a successful operation or its original failure. I tested both wrappers with `getsignal(SIGCHLD)` mocked to return None and a setter that rejects None.

In that case the helper resets SIGCHLD to default and leaves it default. It does **not** restore the unknown native handler. That is a reasonable documented limitation for these standalone build helpers. If exact native-handler restoration becomes a requirement for embedding them in another process, use an appropriate native sigaction facility or reject that unsupported embedding mode; None is not a restorable handler token.

## 3. H3: explicit debugfiles.list path and release builds

**Locations:** `llvm.spec:960–970`; `clang-bolt-helper.py:1067–1077,1093–1102,1856,1913–1915`.

No defect found in the change.

- The added path is double-quoted and expands `%{_builddir}/%{buildsubdir}/debugfiles.list` as one shell argument. It no longer depends on how deep the ordinary-clang path happens to be.
- The existing macro captures the original post chain first; the added option does not alter that ordering. The invocation remains inside the x86_64/BOLT-enabled conditionals.
- The CLI requires the option in both modes, but it is an ordinary path string, not an argparse file-opening type. Passing a nonexistent path is allowed at parse time.
- For release identities without `debug_file`, post processing does not call the debug-list gate. The gate itself also returns `required: false` before testing the path. Release builds therefore do not need an actual debugfiles.list merely because the option is supplied.
- For debug identities, the path must exist and contain the expected installed symbol-file entry; a missing list continues to fail explicitly.

I tested a nonexistent path with a release identity and a valid list in a directory containing a space with a debug identity. Both behaved as intended.

Update existing CLI fixtures and any external callers of `post` to pass the newly mandatory option. Add negative debug fixtures for a missing list and a list omitting clang-22.debug. The actual Tizen macro chain's output filename should still be checked in its RPM integration test; I did not run rpmbuild here. The pre-existing unquoted `%{SOURCE1201}` is not introduced by H3, and the new debug-list argument itself is correctly quoted.

## 4. H4: GNU long-name table handling

**Location:** `llvm-static-archives-native.py:121–139`.

No defect found. A separate `seen_longnames` boolean is the correct distinction between “no table encountered” and “encountered a zero-length table.” Testing the byte string's truth value would miss the latter.

The flag is local to one `inspect()` invocation, is set on the first `//` header, and rejects a second one before replacing the previously recorded table. The stored-size and alignment checks still apply. This works for normal archives and thin archives because `//` is a special member whose table bytes are stored in the archive in either format.

The patch does not change thin-member payload interpretation or enable thin archives for installation: `validate_archive()` still rejects thin archives for conversion. It also does not claim to validate every GNU long-name-table property merely by rejecting duplication.

Executed fixtures covered both archive magics with:

- An empty first `//` followed by another table: rejected with the intended error.
- A nonempty first `//` followed by another table: rejected with the intended error.
- A single empty table: accepted by inspection.
- A single nonempty table and a member referencing offset zero: accepted by inspection.

Retain fixtures for no table, an out-of-range long-name reference, truncated table storage, and alignment errors in the regular parser suite. H4 does not create a reason to reject an otherwise supported archive containing exactly one table.

## 5. Tests, scope limits, and final decision

The executed focused checks passed for the requested changes. They also produced the two real pre-existing findings above. Temporary test artifacts, including the reconstructed A+B files and the primary result JSON, are under `/tmp/codex-review-ps5-05g9bu2m/`; these are local diagnostic artifacts, not committed tests or permanent build evidence.

Before merging, carry the important fixtures into the project's maintained suite and run them on its supported Python runtime:

1. Real spawned child plus two signals before PGID publication; one-signal cleanup; Popen failure with and without a deferred second signal.
2. Signals at the spawn-finally boundaries and during forced escalation, with an external harness that cleans and accounts for all test descendants.
3. SIGCHLD initially default, ignored, callable, and mocked None; ordinary success/error/timeout, argparse SystemExit, and explicit BaseException paths. For callable handlers, verify they are restored and do not consume the helper's child before its own wait.
4. Converter cancellation during real concurrent child commands and executor unwinding, not only a mocked delegated body.
5. H3's debug/release argument cases and all duplicate-table fixtures for both archive magics.
6. R1's successful leader with a live descendant; R2's nested first-handler boundary if the second-signal contract is strengthened.

No LLVM/RPM build was necessary to establish the source-level spawn ordering or the two reproductions. A real packaging test is still needed to certify the platform post-chain path and the full converter's integration behavior. These review tests do not establish generated-LLVM binary equivalence, and the patch does not purport to change the compiler pipeline itself.

**Final decision:** A+B correctly implement the intended H1–H5/N1 fixes for ordinary supported build execution. I would accept those changes rather than revert to blocking signals across spawn. Separately, fix R1 before claiming that successful `call()` completion guarantees no running group members; track R2 as a general pre-existing escalation defect. Describe H1/H5 as restoring representable SIGCHLD dispositions after normal cleanup/unwinding, not as guaranteeing that every child or grandchild is reaped under every failure and emergency termination path.
