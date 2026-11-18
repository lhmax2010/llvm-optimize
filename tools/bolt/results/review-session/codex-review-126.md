# Final confirmation: H4 → H5 UTF-8 handling

**Recommendation: accept H5.** I found no new wrong/unpinned-process signaling, failure-to-success conversion, hang, or unhandled scan/cleanup exception introduced by this change. The non-UTF-8 process-name case is fixed. The metadata read/write path does not introduce an encoding failure for an unchanged metadata file that this helper successfully wrote itself.

- H4: `7a7bc17467d4c5da9763e86e3c74a123b3ff0df2`
- H5: `ed922413c19b01d07e0ec6547771267f40ab5469`
- H5 helper SHA256: `82127f980162a4dd4510188012329ba49b1f56866469387371adb289d2c5e54e`
- Reviewer: Codex, 2026-11-17.

All source line references below refer to H5's `packaging/clang-bolt-helper.py`.

## Scope and identity

I read the complete supplied `tools/bolt/results/ps5-helper-126/helper.diff`, `docs/bolt/126_helper_utf8.md`, `candidate.json`, the final `run2/tests/test_126.py`, `owned_utf8_scenario.py`, the fixture correction, and relevant retained tests. I inspected the actual H5 process-control and metadata writer/reader code.

I independently retrieved the H5 helper from its Git object and matched the supplied H4→H5 diff against Git. Only the helper changed: +3/-2. The spec and other product files are unchanged in this comparison. No product file was modified during the review.

## Correctness and safety findings

**No blocking or mandatory correction found.**

### 1. Process-stat decoding and identity

At line 169, reading bytes and decoding with UTF-8 `surrogateescape` prevents arbitrary non-UTF-8 process-name bytes from raising UnicodeDecodeError before the scan can inspect the process.

The rest of the parser is unchanged: PID precedes the first space, the name is between the first `(` and final `)`, and numeric fields follow the final `)`. The six positional fields and their indices are unchanged. Invalid bytes preserved as surrogate escapes in the name do not become ASCII delimiters, alter the session/starttime fields, or participate in identity selection. Malformed numeric input still raises GateError rather than passing membership checks.

This one decoder is used by discovery, the self/PID-namespace check, and both pidfd/fallback rechecks. The change therefore fixes the decoding failure at all those call sites without adding a new signal path. OSError handling, deadlines, error accumulation and fail-closed behavior are unchanged.

### 2. Display conversion cannot raise for names produced by this decoder

At line 278, `comm.encode('utf-8', 'surrogateescape').decode('utf-8', 'replace')` reverses the byte-preserving decode, then creates displayable Unicode with replacement characters for invalid sequences.

For a name produced by line 169, this encoding step is valid: valid Unicode characters encode normally, and the low-surrogate escapes introduced for undecodable bytes map back to those bytes. Even UTF-8 byte sequences that would represent forbidden surrogate code points are treated as undecodable bytes and safely replaced on the final display decode.

The conversion does not modify `member.comm`, the tuple fields, or the signal target. It performs no I/O and remains inside the existing 20-member diagnostic cap. The previously accepted SID pinning, pidfd ownership, retirement ordering, error retry and cancellation code is unchanged.

An artificially supplied Python string containing a lone surrogate outside the surrogateescape byte range could still fail this encoding operation. That is not a name produced by `proc_stat()` from Linux procfs bytes, and I found no product path that supplies such a value. It is not a regression requiring a change to this patch.

### 3. Metadata: successfully helper-written content round-trips safely

**The answer to the explicit metadata question is no: the new read cannot create this encoding failure from an unchanged metadata file that `save()` successfully wrote.**

The relevant sequence is:

1. `call()` initially writes the invocation metadata through `save()` at lines 451–453, before spawning.
2. `save()` uses `json.dumps(..., ensure_ascii=False)` at lines 161–162.
3. `atomic_text()` opens its temporary file with explicit `encoding='utf-8'` and the default strict error handling, writes it, and replaces the destination only after successful completion (lines 143–158).
4. After the command and drain succeed, `call()` retires the SID and reaps the child at lines 489–493.
5. Line 496 decodes the metadata bytes explicitly as UTF-8 with surrogateescape, then parses JSON. Line 497 writes the same values plus `completed=True, rc=0` using `save()` again.

A successful initial strict UTF-8 write guarantees that those file bytes are valid UTF-8. Surrogateescape does not introduce surrogates while decoding valid UTF-8. The helper's JSON serializer also distinguishes a literal backslash-u sequence from an actual surrogate: an argument containing the literal text `\udcff` is JSON-escaped and returns as literal text after parsing; it does not turn into U+DCFF. Valid Unicode, escaped control characters, and ordinary non-ASCII arguments remain writable after the read. The completion fields add no encoding-sensitive values.

There are two different cases that should not be confused with that invariant:

- **A surrogate already present in an argv/cwd string:** the initial strict `save()` can fail before spawning. `call()` catches that error and raises GateError. This limitation already exists in H4; changing the later reader does not create it. My test confirmed no Popen call and no session cleanup in this case.
- **Externally corrupted or replaced metadata:** invalid UTF-8 bytes, or externally supplied JSON escapes for lone surrogates, can result in a string that the strict writer rejects. The new reader is not a sanitizer for arbitrary metadata. I injected invalid-byte JSON into the post-reap read: write-back raised UnicodeEncodeError, `call()` converted it into GateError, and no scan/kill was attempted on the retired SID. The primary result stayed failure. This is not an unhandled scan/cleanup exception or a false success.

Other failures such as disk-full or permission errors remain possible, of course; the conclusion concerns the questioned encoding round trip, not a guarantee that all filesystem writes succeed.

## Fresh verification

**22 tests passed, zero failures/errors**, against the exact H5 helper in a scratch directory:

- 15 selected supplied tests: the new no-I/O replacement-rendering test; three tuple/name compatibility tests; both phase-deadline tests; and nine retained formatter, parser, error-label and deadline tests from the corrected run2 fixtures.
- Seven independent tests:
  1. Real `save()` → byte decode/JSON parse → `save()` metadata round trips, with non-ASCII text, non-BMP characters, literal surrogate-looking escape sequences, control characters, and a broad sample of Unicode scalar values.
  2. The successful `call()` metadata path using real metadata files and modeled child lifecycle operations.
  3. Invalid metadata injected after the modeled reap: GateError with UnicodeEncodeError as its cause, no SID cleanup, and `_ACTIVE_SESSION` cleared.
  4. An actual surrogate in argv: failure before spawn.
  5. Synthetic process-name byte fixtures, including every single byte 1–255 and malformed multibyte UTF-8 sequences: unchanged numeric fields, reversible cached name bytes, and strictly UTF-8-encodable diagnostics without I/O.
  6. Invalid numeric PID data: GateError, not success.
  7. A real owned child with `prctl` name `b'\xff\xfe'`: successful stat parsing and scanning, exclusion from the reviewer's foreign session, rejection of a foreign-SID signal attempt, then successful matching-SID pidfd cleanup. Cached-name formatting still worked after reap and produced replacement characters.

The real child was created by this test, its pidfd was held by the test, and all terminating signals used pidfd. It was waited/reaped. No process was killed by name or bare PID, and no RPM build was run. The metadata lifecycle fault cases used mocks for process operations; they are not claimed as real asynchronous-cancellation tests.

Resource limits were MemoryMax=4 GiB, MemorySwapMax=0, CPUQuota=200%, nice 19 and idle I/O priority. Host runtime: Python 3.12.3, Linux `6.17.0-1033-oem`. Python 3.9 was not executed; the changed APIs and error handlers are available for the stated Python 3.9+ runtime.

Fresh scripts and evidence:

- `/tmp/codex-review126-2brvxcm0/check.py`
- `/tmp/codex-review126-2brvxcm0/tests.log`
- `/tmp/codex-review126-2brvxcm0/results.json`

I did not independently rerun the reported 743-test suite or r18 probe. The report's final result is supplied evidence, not my fresh test count. The retained test correction from `Path.read_text` mocking to `Path.read_bytes` mocking is appropriate for the explicitly changed interface and preserves the name assertion.

## Decision

**Accept H5; no mandatory fix requested.** The byte-safe scan path and display normalization address the stated non-UTF-8-name failure without changing process identity or cleanup policy. The metadata change is safe for files the helper successfully wrote itself; invalid external metadata remains a reported failure after retirement/reap, not a successful step or an unsafe cleanup attempt. Existing fallback, session-escape and cooperative-deadline limitations remain unchanged.
