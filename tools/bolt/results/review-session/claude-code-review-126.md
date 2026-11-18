# Confirmation review: H4→H5 (126, candidate ed922413)

## What I reviewed and ran

**Material**
- `ed922413c19b01d07e0ec6547771267f40ab5469:packaging/clang-bolt-helper.py`, from a local clone of the product repository. SHA256 82127f980162a4dd4510188012329ba49b1f56866469387371adb289d2c5e54e.
  - `git diff 7a7bc174 ed922413` touches only this file (+3/−2) and matches `tools/bolt/results/ps5-helper-126/helper.diff` byte for byte.
  - The parent is 61ef5d31, as for H2–H4.
- `docs/bolt/126_helper_utf8.md`, `all-text-read-sites.json`, `run2/tests/test_126.py` and `tests/owned_utf8_scenario.py`.

**Tests**
- I ran these against a scratch copy of H5, using the `run2/tests` copies for 122–126: `test_114` (34), `test_118` (19), `test_119` (6), `test_120` (2), `test_122` (11), `test_124` (2), `test_125` (4) and `test_126` (4).
- **All 82 pass.**
- I did not rerun the remaining 661 tests of the 743-test suite.

**Probes.** All are owned-process probes with the same subreaper harness as before. Signals go only to the harness's own runner, and survivors are killed only as its own unreaped children, through pidfds.
- **The 18 standing scenarios.** All match H4 in result class, exit code, signalling mode and processes left over. The only difference is all-EMFILE: 224 forked children against 225, a timing artefact of the forking member, as before.
- **The non-UTF-8 check from 125** (`badcomm.py` under `reaper.py`).
- **A new metadata check** (`meta.py`), run on both H5 and H4.
- No RPM build, no kill by name or bare PID, nothing left running.
- Scripts and results:
  - `/tmp/claude-1000/-home-linhao-Toolchain-development-llvm-optimize/5e8aa240-5caa-4416-a0c4-218f8c1eb336/scratchpad/r17/probe/results126.jsonl`
  - `…/scratchpad/r18/probe/` (badcomm, reaper)
  - `…/scratchpad/r19/probe/meta.py`

## Verdict

**Confirmed. H5 closes the non-UTF-8 process-name issue and introduces no correctness or safety problem.**
- It signals no wrong or unpinned process.
- It turns no failure into success.
- It adds no hang.
- It adds no unhandled exception in the scan or cleanup path.

### The three changes

1. **`proc_stat`: read bytes, then decode UTF-8 with surrogateescape.** This decode cannot raise.
   - The only thing that can contain arbitrary bytes is `comm`. It is carried as an attribute and never used for selection or signalling.
   - The fields the helper parses (pid, state, pgrp, session, threads, starttime) are kernel-written ASCII. Their parsing is unchanged.
   - `text.split('(',1)` and `rsplit(')',1)` still find the right delimiters, because surrogateescape never produces `(` or `)`.
   - The SID and starttime re-checks before a kill read through the same function, so they are unchanged.
2. **`session_snapshot`: surrogates become U+FFFD before formatting.**
   - Surrogates from step 1 are re-encoded with surrogateescape and decoded with `replace`, so the diagnostic text is always strict-UTF-8-encodable.
   - Only the snapshot is formatted from `comm`, and every message that names members goes through it. No lone surrogate can reach a `GateError` message, the log, or a later `save()`.
   - `'?'` and ordinary names pass through unchanged.
3. **Metadata read-back: bytes, then surrogateescape.** See below.

### Non-UTF-8 name, rerun on H5

Owned processes named `b'\xff…'`:
- **(A) The process is outside the session.**
  - On H4, `live_session_members` raised `UnicodeDecodeError`, and a trivially successful step failed in 0.03 s.
  - On H5 the scan succeeds, and `sh -c 'exit 0'` returns OK in 0.02 s.
- **(B) The process is a session member in its own process group, and the step times out.**
  - On H4 the report read `TIMEOUT …; cleanup error: 'utf-8' codec…`, and the member survived for the wrapper to kill.
  - On H5 the report is plain `TIMEOUT`, with no cleanup error. The member was killed by the helper, so the wrapper had nothing to clean.
- **Author's tests.** `test_126` covers the same cases, plus the 6/3-field shape and a check that the formatter's output is strict UTF-8. They pass.

## Your point: the metadata path through `save()`

**It cannot raise on content the helper itself wrote.**

The reasoning:
1. **The first write is strict.** It is `save()` before spawn: `json.dumps(…, ensure_ascii=False)` written through `atomic_text`, which opens with `encoding='utf-8'`. If any string written there (argv, cwd or the SIGCHLD text) contains a lone surrogate, that first write raises `UnicodeEncodeError`.
   - The raise happens before `Popen`, inside `call()`'s `try`. It becomes `GateError: COMMAND_ERROR: …` with no process spawned, and `atomic_text` removes its `.new` file.
   - That is a handled failure. It is the same on H4.
2. **So a helper-written file is always valid UTF-8,** and decoding valid UTF-8 with surrogateescape gives exactly the strict result.
3. **The read-back contains nothing the strict writer could not write.**
   - `json.dumps(ensure_ascii=False)` escapes only `"`, `\` and the control characters U+0000–U+001F.
   - It never writes a `\udcXX` escape: a surrogate would be emitted raw, and would already have failed at step 1.
   - `json.loads` therefore returns exactly the strings that were written.
4. **The second `save()` writes the same strings plus `completed` and `rc`,** so it cannot raise `UnicodeEncodeError`.

**Runs (`meta.py`, identical on H5 and H4 except where noted):**

| Case | Result | Spawned |
|---|---|---|
| a. argv containing `ü€😀`, `\x01\x1f\x7f`, U+2028, `"`, `\` and U+FFFD | **OK**; the metadata is valid UTF-8 with `completed: true` | 1 |
| b. argv containing `os.fsdecode(b'x\xff')` | `GateError` (cause `UnicodeEncodeError`) at the first `save()`; no `.new` left behind | 0 |
| c. cwd with a non-UTF-8 directory name | the same as b | 0 |
| d. the command itself overwrites the metadata file with an invalid byte | `GateError` after the reap. Cause on H5: `UnicodeEncodeError` at the write-back. Cause on H4: `UnicodeDecodeError` at the read. | 1 |
| e. the command writes a JSON `"\udc80"` escape | `GateError` (cause `UnicodeEncodeError`) at the write-back, on both | 1 |

Cases d and e are not content the helper wrote. They still end as a failure, never a success, and they happen after `session_retired` and the reap, so no cleanup or signalling runs. For helper-written content the metadata change is effectively a no-op. It only moves where foreign corrupt content fails. That is harmless, and it fails closed either way.

## Follow-ups (not correctness)

1. Cases b and c fail with a codec message rather than a clear "argv/cwd not UTF-8-encodable". This is pre-existing and cosmetic, and such paths are unlikely in a build root.
2. The `.argv.json` read-back could simply be strict, since only helper-written content is expected. Either choice is safe; no change is needed.
3. Earlier follow-ups (120/125 wording, the stale `tests/test_122.py` copy outside `run2`) are unchanged by H5.

## Not reviewed

- The other 661 tests (I rely on the author's run2 log).
- The sandbox push and the commit-message checks.
- Python 3.9 compatibility (the host here is 3.12).
- Worker-mode qualification.
