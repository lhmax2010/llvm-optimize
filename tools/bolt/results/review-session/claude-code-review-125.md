# Final review: H3→H4 (125, candidate 7a7bc174)

## What I reviewed and ran

**Material**
- `7a7bc17467d4c5da9763e86e3c74a123b3ff0df2:packaging/clang-bolt-helper.py`, from a local clone of the product repository.
  - SHA256 90b6f9f37401e6010ef1b19597a4d2e28e18df9e8c8a7140a9b5e50e5dee2dbf, as in `candidate.json`.
  - `git diff db7ac04b 7a7bc174` touches only this file (+37/−19) and matches `tools/bolt/results/ps5-helper-125/helper.diff` byte for byte.
  - The parent is 61ef5d31, as for H2 and H3.
- `assertion-and-fixture-changes.json`, `failure-classification.md`, `new-fixture-correction.json`.
- `tests/test_124.py`, `tests/test_125.py`, and `run2/tests/test_122.py` (the corrected copy).
- `docs/bolt/122_helper_fixes.md`: sections 122, 123 and 125, plus the 124 headings.

**Tests**
- I ran, against a scratch copy of H4: `test_114` (34), `test_118` (19), `test_119` (6), `test_120` (2), `test_122` (11), `test_124` (2) and `test_125` (4). **All 78 pass.**
- `tests/test_122.py` is the pre-correction copy: it still builds 4-tuples with the name as an extra element, and fails against H4. The copy under `run2/tests/` is the one the second run used, and it passes. This matches `failure-classification.md`.
- I did not rerun the remaining 661 tests of the 739-test suite.

**Probes**
- The same ownership-safe harness as in 120: subreaper, signals only to its own runner, survivors killed only as its own unreaped children through pidfds.
- I ran 18 scenarios on H4, the same ones as on H3, including all-EMFILE.
- I also ran one new owned-process check, `badcomm.py`, under a subreaper wrapper, on both H4 and H3. It covers a process whose `comm` is not valid UTF-8.
- No RPM build, no kill by name or bare PID, nothing left running.
- Scripts are in `/tmp/claude-1000/-home-linhao-Toolchain-development-llvm-optimize/5e8aa240-5caa-4416-a0c4-218f8c1eb336/scratchpad/r17/probe/` (harness, runner, results in `results125.jsonl`) and `…/scratchpad/r18/probe/` (`badcomm.py`, `reaper.py`).
- On the "22 versus 19" note in the 125 doc: in 120, 19 H3 runs are in `results.jsonl`. The other three H3 runs (all-EMFILE, transient-scan, persistent-scan) and the three H2 comparisons are in `cmp.jsonl`.

## Verdict

**H3→H4 introduces no correctness or safety problem.** It signals no wrong or unpinned process, turns no failure into success, and adds no hang. I have no blocking finding for H4.

The change is diagnostics only:
- **Signalling is untouched.**
  - `kill_session_member` checks the same fields as before: `current[4] == sid`, plus `current[5] == starttime` in fallback mode.
  - The pidfd ordering (open → re-check → send → close) is unchanged.
  - The kill loop's control flow and the retirement and latch logic are unchanged.
- **The positional shape is preserved.**
  - `proc_stat` still returns 6 elements and members are still 3-element tuples.
  - `_StatTuple` is a plain `tuple` subclass with a `__dict__`. Equality, hash and sort ignore `comm`; `test_125` checks this.
  - Slicing (`member[:3]`) returns a plain tuple, and `session_snapshot` falls back to `?` through `getattr`. Older 3- and 4-tuple fixtures still format.
- **The formatter cannot fail or block.**
  - It does no I/O (checked by `test_125` with `Path.read_text` patched to fail) and can raise nothing for a 3-element member.
  - The 20-member cap works. All-EMFILE probe: `… +196 more;`.
- **Parsing `comm`.** `text.split('(',1)[1].rsplit(')',1)[0]` takes the first `(` and the last `)`. That is correct for names containing parentheses, and it sits inside the same `try` as before, so a missing `(` still becomes `malformed process stat`.

**Probe results on H4 equal H3 in every scenario.** Each line gives result, time in seconds, and processes left for the harness:

| Scenario | Result | Time (s) | Left for harness |
|---|---|---:|---:|
| bg-short | OK | 3.03 | 0 |
| bg-long | live descendants, drain deadline, `…:sleep (S)` | 10.02 | 0 |
| first-wait | CANCELLED after drain | 10.03 | 0 |
| second-wait | runner killed by SIGTERM | 2.01 | 0 |
| ninja-straggler | live descendants | 10.37 | 0 |
| ninja-timeout, pidfd | TIMEOUT | 2.05 | 0 |
| ninja-timeout, fallback | TIMEOUT | 2.05 | 0 |
| fallback adversarial | TIMEOUT | 1.05 | 0 |
| eperm-delay | TIMEOUT + `cleanup deadline` | 11.31 | 1 (injected) |
| emfile | TIMEOUT + `cleanup deadline` | 11.01 | 1 (injected) |
| unkillable-delay | TIMEOUT + `cleanup deadline` | 11.01 | 1 (injected) |
| hammer-unkillable | killed by SIGTERM after the third signal | 1.4 | 1 (injected) |
| second-cleanup-unkillable | killed 1.0 s after the second signal | 3.0 | 1 (injected) |
| eacces-probe | `fallback-recheck errno=EACCES`, OK | 0.02 | 0 |
| einval-probe | fails before spawn | 0.00 | 0 |
| transient-scan | still fails (N2 fail-closed kept) | 0.53 | 0 |
| persistent-scan | fails after about two budgets (N3 as documented) | 20.01 | 0 |
| all-EMFILE | fails; known limit, list capped | 11.01 | 225 (same as H3) |

SIGCHLD was restored in every scenario that returned. Every "injected" survivor is the member made unkillable by design.

## Pre-existing issue outside your three categories (not introduced by H4)

**A process name that is not valid UTF-8 aborts every session scan.**

This is not a wrong or unpinned signal, not failure-to-success, and not a hang. It is the same in H3: I reproduced it identically. I list it because it disables cleanup, and the fix is one line.

`proc_stat()` reads with `Path(path).read_text()`, which uses the locale encoding with strict errors. Under both `LANG=C.UTF-8` and `LANG=C`, Python 3.12's locale coercion makes that encoding UTF-8. Any process can set its `comm` to arbitrary bytes, through `prctl(PR_SET_NAME)` or by exec'ing a file with such a name. The resulting `UnicodeDecodeError` is raised before the `try`, and it is neither an `OSError` nor a `GateError`. It therefore escapes:
- the per-entry handling in `live_session_members`;
- the per-member handling in the kill loop;
- `wait_session_exit` and `kill_session`.

Owned-process results, identical on H4 and H3:
- **(A) A process outside the session.**
  - An unrelated owned process named `b'\xffbad\xfe'` exists anywhere on the host. A trivially successful step (`sh -c 'exit 0'`) then fails in 0.03 s: `COMMAND_ERROR: 'utf-8' codec can't decode byte 0xff…; cleanup error: 'utf-8' codec…`.
  - Every BOLT step on that host would fail closed for as long as the process lives.
- **(B) A session member in its own process group with such a name.**
  - A step that times out reports `TIMEOUT …; cleanup error: 'utf-8' codec…`.
  - The scan aborts, so only the leader's process group is killed (by `killpg`). The member survived, and my subreaper wrapper had to kill it.
  - With a forking member, any other members outside the leader's group would survive the same way.

**Effect.**
- The result stays a failure, so this is fail-closed.
- But cleanup becomes ineffective, and a process outside the session can block all BOLT steps.
- Likelihood in a Tizen build chroot or VM is low.

**Fix.** Read bytes and decode explicitly, for example `Path(path).read_bytes().decode('utf-8', 'surrogateescape')`, or `errors='replace'`. Every field the helper uses after `)` is ASCII, and `)` cannot be produced by the replacement, so parsing is unaffected. `comm` would then be shown with escapes.

## Follow-ups (wording and style only; none affects behaviour)

1. **Empty list after a genuine scan cut-off.** When the deadline cuts a scan short, the scan-phase text can still end in an empty list: `… final scan incomplete; errors: session deadline expired; scan incomplete; last observed members: `. The H4 `emfile` and `unkillable-delay` probes show it.
   - Under the new rule, "scan incomplete" is correct there.
   - The trailing "last observed members: " with nothing after it duplicates the main clause. Omit it when the list is empty.
2. **Deadline exactly at the end of a scan.** The `session_deadline(deadline, members)` after enumeration finishes (in `live_session_members`) labels a scan "incomplete" even when it has just completed. Harmless.
3. **The `errors` part of messages is unbounded.**
   - The member list is capped, but `errors` can still hold one entry per member PID. For example, with process-wide EMFILE before the scan reaches every member, or with many members that refuse signals.
   - Consider the same 20-entry cap on `errors`.
4. **Plain `GateError` lacks context.** The plain `GateError` from `wait_session_exit` (errors present but the final scan empty) still lacks the "command exited successfully" context in `call()`. Cosmetic; carried over from 120 N2.
5. **Stale test copy.** `tests/test_122.py` in the 125 result directory is the pre-correction copy, so running it reproduces the six first-run failures. Point readers at `run2/tests/test_122.py`, or note in the README which one is authoritative.

## Not reviewed

- The other 661 tests (I rely on the author's run2 log).
- The sandbox push and the commit-message checks.
- Python 3.9 compatibility (the host here is 3.12).
- Real worker qualification: which signalling mode workers end up in, and their `/proc` readability.
