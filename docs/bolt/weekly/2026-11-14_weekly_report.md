# Tizen LLVM Toolchain Optimization - Weekly Report (Nov 9-14, 2026)

Nov 14, 2026 · @Hao

## Summary

The x86\_64 LLVM optimization series is uploaded as one review, Change 361395, and is ready for HQ review. The final tree was built by QB 1226850 (Tizen-Base-Toolchain) and 1226851 (Tizen-Base-Dev) on x86\_64, armv7l and aarch64, and all 102 binary package payloads match the previous QB validation.

This week we also closed the BOLT relocation-warning question: every thread-local-storage access in the shipped clang was statically verified. A converter hardening follow-up is implemented and will be added as PS4 next week, after QB validation.

## Review request: Change 361395

Please review [Change 361395](https://review.tizen.org/gerrit/c/platform/upstream/llvm/+/361395) on tizen\_base. As HQ suggested, the three commits are combined into one change as three cumulative patch sets, and each patch set has a note explaining it. Changes 361396 and 361397 are abandoned and point to 361395.

| Patch set | Adds | Files | How to roll back |
| --- | --- | --- | --- |
| PS1 | Part 1: hybrid LLVM linkage on x86\_64. Tools use libLLVM/libclang-cpp; clang, lld and llvm-ar stay statically linked for qemu-accel | 6 CMake files, llvm.spec | Revert Part 1 |
| PS2 | Part 2: BOLT-optimized clang on x86\_64 with a prebuilt profile; the build fails on a stale profile or any failed check | clang-bolt-helper.py, clang-bolt-v2.fdata.xz (binary profile, 9.7 MB), llvm.spec | One line: bcond\_without clang\_bolt to bcond\_with |
| PS3 | Part 3: fixed x86\_64 compile/link flags and stricter checks in the static-archive converter | llvm.spec, llvm-static-archives-native.py | Revert Part 3 |

To review one part at a time, compare PS1 with PS2 (BOLT only) and PS2 with PS3 (flags and converter only). armv7l and aarch64 build behavior is unchanged; the only ARM payload change is the installed AddLLVM.cmake and AddClang.cmake text.

## Progress this week

All planned upload work for the first batch is complete; two follow-up items continue next week.

| Planned task | Status | What was done and what the result means |
| --- | --- | --- |
| Fix the remaining code review findings | Done | Three more review rounds were addressed. Examples: the static-archive converter now rejects assembler pass-through options (-Wa,), requires the compiler, disassembler and nm to report the same LLVM version, checks every relocation against an explicit x86\_64 size table, and cleans up child processes correctly when the build is cancelled. The final review round found no serious issues. |
| Rebase onto the merged HQ base | Done | HQ merged the parent changes 359934 (PS10) and 357163 (PS2) on Nov 11. Our three commits were rebased onto them without conflicts, and the current tizen\_base has exactly the same source tree, so the series applies unchanged. |
| Validate the final code on both projects and all three architectures | Done | Tizen-Base-Toolchain and Tizen-Base-Dev were built for x86\_64, armv7l and aarch64 from the final code. Every binary package (102 in total) has the same contents as the previously validated build, and all 1294 static libraries (22,520 object files) are identical file by file. On armv7l and aarch64 the build itself is unchanged; compared with the build before our changes, the only difference is the text of two CMake files (AddLLVM.cmake, AddClang.cmake) that are installed on every architecture. |
| Local full builds of both projects | Done | Complete package builds of both projects were run locally with the same snapshot and build configuration, then compared package by package with the reference builds. They match; the only difference is a build-path prefix inside Toolchain debug files. We also installed the packages and checked crash debugging of the BOLT-optimized clang: in a clang stack trace, all 21 frames were resolved to the correct function names by LLDB (cross-checked with llvm-symbolizer), so its debug symbols work. |
| Upload for review | Done | Uploaded to tizen\_base, then combined into one review, 361395, as HQ suggested: PS1 hybrid linkage, PS2 adds BOLT, PS3 adds fixed flags and converter checks. |
| Fix our local build-and-compare script | Done | This internal script runs the two project builds one after another and compares their packages. Review found that it treated unknown build-service states as finished. It now continues only after an explicit finished or failed state, records each build as started before launching it, and refuses to run the wrong project. Its test suite (30 cases, 14 of them new for these situations) passes in full. This script is not part of the Gerrit change. |
| Explain the BOLT warnings | Mostly done | BOLT prints two kinds of warnings while optimizing clang. "Failed to analyze 2804 relocations" is closed: these are thread-local-storage relocations that BOLT skips, and a function-by-function check of the shipped clang confirmed all thread-local accesses are still correct. "Jump past end, replacing with nop" (10 places) is BOLT's normal handling of code after an unreachable point: 2 places are proven against the LLVM source and 8 show the same pattern; details in the next section. |
| Converter hardening follow-up | In progress | Four extra defensive checks requested in review (details in the follow-up section) are implemented. All 119 automated tests pass: the existing converter tests plus new tests that feed malformed and boundary inputs for each check. Validation on real libraries and the PS4 upload are planned for next week. |
| Toolchain vs Base-Dev comparison and resource breakdown | Done | The BOLT input clang of the two projects was compared function by function: of 147,113 functions, 99,048 are identical, 47,997 differ only in relocated addresses, and 68 differ in machine code; the cause is still open. From existing build logs, build time was broken down by stage: normal compilation 43.6%, static-library conversion 22.0%, BOLT 18.7% of a local build. This is the basis for the upcoming build-resource reduction work. |

## BOLT verification results

Both BOLT warnings were analysed against the shipped clang; one is closed and one is mostly traced, and neither required a code change.

**"Failed to analyze 2804 relocations" - closed.** All 2804 are thread-local-storage relocations kept by --emit-relocs: R\_X86\_64\_TLSGD 1536, R\_X86\_64\_TLSLD 415, R\_X86\_64\_DTPOFF32 853. BOLT does not support these types and skips them; the linker had already relaxed the sequences (GD to IE, LD to LE). A function-by-function static check of the shipped x86\_64 clang of both projects (1187 functions with TLS accesses) found:

- all 1536 initial-exec loads still reference the same GOT slots, which carry R\_X86\_64\_TPOFF64 dynamic relocations;
- all 415 local-exec %fs:0 loads and their DTPOFF offsets are unchanged; BOLT only dropped redundant data16 padding;
- the leftover \_\_tls\_get\_addr PLT32 records were not applied to any instruction.

**"jump past end ... replacing with nop" (10 sites) - 2 proven, 8 matching.** BOLT treats a branch to the exact end of a function as the result of \_\_builtin\_unreachable() and replaces it with a nop; the branch can be taken only if an "unreachable" assumption is violated. Two sites (AArch64 isBranchOffsetInRange and getBranchDestBlock) are traced instruction by instruction to llvm\_unreachable. The other eight show the same structure but are not yet traced one by one.

The local and QB builds produced the same final clang (SHA256 e08724d8... for Toolchain, 1664b9d2... for Base-Dev), so these results apply to the QB packages.

## Follow-up: converter hardening (planned PS4)

Four defensive checks from the code review are implemented in llvm-static-archives-native.py and pass 119/119 tests; they will be added to 361395 as PS4 after QB validation. They do not change output for valid input.

- Validate the compressed section header (zlib or zstd type, power-of-two alignment) before its declared size is used.
- Require zero-width relocation markers to lie inside their target section.
- Reject SHT\_RELR sections in archive members.
- Log the inherited architecture flags and SIGTERM/SIGINT/SIGHUP states at startup.

Before upload: re-convert the real archives (all 3853 converted members must stay byte-identical), run QB on both projects and compare with 1226850/1226851, and run local full builds of both projects.

## Next week plan (Nov 16-20)

Next week's goal is PS4 on 361395 and the start of the PGO+BOLT work; review comments on 361395 take priority over both.

1. Address HQ review comments on 361395 as they arrive.
2. Free disk space on the local build machine (two full builds need about 151 GiB).
3. Validate the converter hardening: real-archive re-conversion, QB on both projects, local full builds; then upload PS4.
4. Finish tracing the remaining 8 "jump past end" sites.
5. Start the second batch: PGO+BOLT design decisions, resource report, and selection of 2-3 build-resource reduction candidates.
6. Prepare the QB A/B speed measurement of the final build (current speed figures are historical local measurements: about 0.856x compile time on x86\_64).

## Risks and decisions needed from HQ

The main need from HQ is the review of 361395; four further questions decide how the PGO work is packaged.

| Item | Question for HQ |
| --- | --- |
| Review of 361395 | Who will review, and when can we expect first comments? |
| Profiles in the source package | BOLT already ships a 9.7 MB profile. Adding PGO would add a prebuilt profile of about 52.5 MB. Is that acceptable, or should profiles be generated during the build (about 81 minutes more build time)? |
| PGO and llvm-static-devel | With PGO, the static library members in llvm-static-devel change too. Is that acceptable? |
| Speed measurement | Which A/A + A/B protocol version should the QB measurement follow, and is Chromium the right main workload? |
| QB builder limits | What memory and disk limits apply on QB workers? We only report measured values today. |
