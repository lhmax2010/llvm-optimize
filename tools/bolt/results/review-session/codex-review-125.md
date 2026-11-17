# Final review: H3 → H4 session-cleanup changes

**Recommendation: accept H4 for the requested scope.** I found no new correctness or safety problem that signals a wrong or unpinned process, turns a failure into success, or introduces a hang. D1 and D2 from my 120 review are closed. No mandatory product-code change follows from this review. Wording and fixture follow-ups are listed separately below.

Reviewed:

- H3: `db7ac04bd2b854b144f6e5c5fcf3a0aa9645c01e`
- H4: `7a7bc17467d4c5da9763e86e3c74a123b3ff0df2`
- File: `packaging/clang-bolt-helper.py`
- H4 helper SHA256: `90b6f9f37401e6010ef1b19597a4d2e28e18df9e8c8a7140a9b5e50e5dee2dbf`
- Review date: 2026-11-17; reviewer: Codex.

All product line references below are to H4. This is a review of the H3→H4 change and its process-control context, not a fresh review of unrelated BOLT/ELF/package functionality.

## Material and identity

I read the complete supplied `tools/bolt/results/ps5-helper-125/helper.diff`, `assertion-and-fixture-changes.json`, the new/retained `test_122.py`, `test_124.py` and `test_125.py` fixtures, relevant prior regression fixtures, and the report's final “125 续做” section and relevant preceding STOP records in `docs/bolt/122_helper_fixes.md`. I also read `candidate.json`, `test-source-differences.json`, `run2/test-results.json` and `run2/failure-list.json`.

I obtained the H4 helper from the Git object and checked it against the scratch test copy. The supplied H3→H4 diff matches the Git diff, apart from the index-line abbreviation. The Git comparison shows only the helper changed: +37/-19. The spec and other product files are outside this delta.

The top-level `tests/test_122.py` preserves the first-run fixture version. The corrected file that corresponds to the successful second run is `run2/tests/test_122.py`; I used that version for fresh tests. I did not mistake the first-run fixture failures or the earlier 122–124 STOP records for the final result.

## Findings affecting correctness or safety

**None found in this delta.** In particular:

1. **D1/N4: no diagnostic procfs reads remain.** At lines 168–178, `proc_stat()` extracts `comm` from the same text it already read for PID/state/group/session/starttime. Lines 250–261 carry that name into the member object. `session_snapshot()` at lines 270–281 uses only in-memory tuple data and the attribute. Neither that function nor `session_deadline()` initiates another `/proc/<pid>/comm` read. The previously demonstrated loop of diagnostic reads after deadline expiration has been removed, rather than merely given another timeout.

2. **The tuple change does not move identity fields.** The stat result still has six positional elements: PID, state, process group, thread count, session, starttime. A member still has three: PID, state, starttime. `_StatTuple` has an instance dictionary for `comm`; it does not replace tuple indexing, equality, hashing or ordering. `sorted(members)` and `list(members)` retain the actual member objects and their attributes. Slicing `member[:3]` drops the attribute only in local positional extraction, where no name is needed. Ordinary tuples used by existing callers/tests still work and display `?` when they have no name.

3. **Names cannot select the signal target.** The PID/SID/starttime checks remain positional. At lines 219–236, pidfd signaling still opens the fd, re-reads stat, checks the SID, sends through the fd, and closes in `finally`. Fallback still checks SID and starttime immediately before its numeric signal; its previously accepted residual race is unchanged. The new attribute is never consulted for membership, identity or signal delivery. Parentheses in a process name do not shift the identity fields: the parser still finds numeric fields after the final `)`; the name is extracted between the first `(` and final `)`.

4. **N4's cap is diagnostic only.** `session_snapshot()` takes at most 20 entries and appends `+N more`. The complete `members` list remains attached to inspection/deadline exceptions and remains the source of the signaling loop at lines 337–341. No member beyond the twentieth is silently exempted from cleanup. A fresh 25-member model verified that all 25 reach `kill_session_member()`.

5. **D2/N1: scan and signaling deadlines are separated correctly.** Scan entry, per-entry checks and scan completion use the default `phase='scan'`. The pre-open and post-recheck checks in `kill_session_member()`, and the per-member check in `wait_session_exit()`, explicitly pass `phase='signalling'`. Expiration still raises the same exception type and interrupts signaling; only the text and bounded snapshot construction differ. All call sites were checked. The discovery aggregate now correctly says `member read errors` and retains PID/errno.

6. **N2: fail-closed behavior is preserved.** The error dictionary remains outside the rescan loop. A complete empty scan with previously accumulated errors raises at lines 353–356; it does not erase those errors or emit a recovered-success result. A leader-group cleanup error still fails at lines 363–380 even if the subsequent inspection finishes. The earlier proposed transient-error recovery policy is absent from this final diff. Fresh tests covered both a transient scan error and a per-member signaling error followed by an empty scan; both still failed.

7. **Retirement, cancellation and reaping are unchanged.** The active SID is still cleared before retirement and before the final reap, at lines 488–491 and 511–515. Exception cleanup remains guarded by `session_retired`; reap retry remains guarded by `process.returncode is None`. The force-exit latch, deferred second signal during spawn, handler restore/self-resignal path, SIGCHLD restoration and command failure handling have no executable changes in H3→H4. I found no new route from a diagnostic object to a retired SID operation.

8. **N3 is documentation only.** The comment at lines 477–478 explains that a failed success-drain inspection can be followed by a cleanup budget. It does not change either timeout or add a retry loop. The new formatter has a fixed maximum of 20 member iterations and no I/O, so it does not recreate D1's unbounded sequence of post-deadline procfs operations. This is still cooperative process cleanup, not a hard real-time bound on all kernel operations or Python bookkeeping.

## Fresh validation

**33 tests passed, zero failures/errors.** These were run against the exact H4 helper in a scratch directory, with MemoryMax=4 GiB, MemorySwapMax=0, CPUQuota=200%, nice 19 and idle I/O priority.

The run comprised:

- 25 selected supplied tests: three from review125, both review124 tests, nine retained review122 tests, both review120 tests, seven mock review118 tests plus its real self-pidfd capability check, and review119's no-child first-partial-empty case.
- Eight independent checks: delimiter/newline/empty process-name parsing without shifting identity fields; processing all 25 members despite the diagnostic cap; fail-closed after transient scan errors; fail-closed after member errors; deadline before pidfd open; deadline after open with descriptor closure and no signal; a real owned child's cached name after natural exit without diagnostic I/O; and real pidfd SID rejection followed by an authorized matching-SID kill.

For the real SID test, I created two direct children in separate sessions, held pidfds for both, verified that targeting the first child's PID with the second child's SID did not terminate it, and then verified that the matching SID operation did terminate the first child. Cleanup used only held pidfds for these test-owned children, followed by wait/reap. The natural-exit case used a pipe request to let its child exit normally. No process was killed by name or bare PID, and no RPM build was run. No product files were modified.

Fresh evidence:

- `/tmp/codex-review125-rntvkzxn/check.py`
- `/tmp/codex-review125-rntvkzxn/tests.log`
- `/tmp/codex-review125-rntvkzxn/results.json`

The host was Python 3.12.3 on Linux `6.17.0-1033-oem`. Python 3.9 was not executed; the changed tuple subclass, attributes, slicing and keyword-only argument use are compatible with the stated Python 3.9+ target.

I did not rerun the entire reported 739-test suite or the 19 archived process scenarios, and I did not exhaustively audit their raw logs. The supplied second-run summary reports 739/739 and an empty failure list. The report separately records 19 probes and explicitly discloses the first-run fixture failures. Those are supplied evidence, not results I independently reproduced in full. Repeated asynchronous-signal timing was not freshly stress-tested in this review; the relevant executable handler/lifetime code is unchanged.

## Assertion and fixture changes

The listed changes are consistent with the final implementation rather than hiding a safety failure:

- Moving name expectations from an extra tuple element to `.comm` preserves the old positional contracts and adds a separate name check.
- Updating mock stat/member factories from seven/four positional elements to six/three plus the attribute matches the production representation. PID/state/starttime and errno expectations remain checked.
- Updating the signaling-phase text expectation to `while signalling` retains both negative assertions against a falsely incomplete scan.
- Updating trace coordinates from the prior source layout to the same spawn/finally statements does not, by itself, relax their assertions. H4's corresponding statements are at lines 464 and 469.

The corrected run2 fixtures retain meaningful checks for tuple shape, cached names after exit, absence of diagnostic I/O, truncation counts, member-read error continuation and phase classification. The fresh independent tests additionally verify that diagnostic truncation does not truncate signaling and that preserved errors cannot become success.

## Wording/style/test-maintenance follow-ups only

These are optional follow-ups, not correctness/safety blockers:

- **Use the final three-element fixture shape consistently.** `run2/tests/test_124.py`, in `test_signalling_deadline_has_no_incomplete`, still supplies four-element plain member tuples. H4's `member[:3]` deliberately tolerates them and this test's phase assertion remains valid, but its fourth string is not a cached name. Updating it to three-element `_StatTuple` instances with `.comm` would make the fixture represent production inputs more closely. The dedicated tuple tests already cover the actual contract.
- **Consider escaping control characters in displayed names.** The cached `comm` is rendered verbatim at helper line 278. A name containing a newline can split a diagnostic across lines. This cannot change the chosen PID/SID, failure status or loop termination, and verbatim command-name rendering was already present in H3. If desired, escape newline/tab/control characters solely in the formatter and add a one-line-output test; leave the stored name and identity fields untouched.

The “20” limit applies to each formatted member list, not the entire aggregate of historical error strings. Avoid describing it as a universal maximum log length. This does not create a new hang or false-success path in the reviewed change.

## Final decision

**Accept H4.** D1/N4 and D2/N1 are resolved; N2 remains fail-closed; N3 is correctly documented without altering behavior. I found no new wrong/unpinned-process signaling, failure-to-success conversion or hang introduced by H3→H4. No mandatory fix is requested.

The existing limitations remain: fallback numeric signaling has a residual reuse race, descendants that create a new session escape this tracking model, denied/unkillable processes may survive an explicitly failed cleanup, and individual operations can exceed a cooperative deadline. This approval does not expand the previously stated containment or timing guarantees.
