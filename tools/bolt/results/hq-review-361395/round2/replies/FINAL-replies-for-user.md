# Replies for the next patch set (PS5)

The replies below refer to PS5 when they say "the next patch set".

## H1 — packaging/clang-bolt-helper.py:240 (PS3)

> SIGCHLD is set to SIG_DFL here and never restored, so the handler change persists for the rest of the build.

Agreed; the previous SIGCHLD disposition should be restored after cleanup (killing the process group if needed and reaping the child). This will be addressed in the next patch set with a finally block covering success and failure paths. The change currently persists within the helper process; it does not change the parent RPM shell's signal disposition. If the previous disposition is not available as a Python handler, the restore step will not pass None to signal.signal or mask the original error.

## H2 — packaging/clang-bolt-helper.py:250 (PS3)

> Popen with start_new_session=True is followed by _ACTIVE_GROUP assignment.

Agreed; the next patch set will defer a second cancellation only while spawning, publish the process-group ID, and then handle it immediately. The spawn-exception path is covered too. We will not use parent-side pthread_sigmask: a blocked mask is inherited across fork/exec and would block TERM, INT and HUP in the child. The fix keeps the child mask unchanged. PS5 also makes a step fail if it exits successfully while leaving processes running in its group.

## H3 — packaging/clang-bolt-helper.py:1056 (PS3)

> debugfiles.list is located via Path(ordinary).parent.parent.parent, which depends on the RPM build directory layout, and the check only verifies presence and a string match.

Agreed; the debugfiles.list path will be passed explicitly from the spec in the next patch set. The membership check is only one part of the post gate: the helper also verifies the installed executable and debug-file identities, debuglink CRC, and debug-file permissions. Those checks will remain in place.

## H4 — packaging/llvm-static-archives-native.py:133 (PS3)

> The GNU '//' long-name table is overwritten each time it appears, with no duplicate check.

Agreed; a second GNU long-name table should be rejected, even when the first table is empty. This will be addressed in the next patch set with an explicit seen-table flag. Valid archives with one table and archives without a long-name table will retain their current behavior.

## H5 — packaging/llvm-static-archives-native.py:994 (PS3)

> SIGCHLD is set to SIG_DFL in install_main() and not restored on exit (only one signal.signal call for SIGCHLD in the file).

Agreed; install_main should restore the original SIGCHLD disposition. This will be addressed in the next patch set with an outer finally block that also covers argument-parser exits and conversion failures. The reset is process-local and does not change the parent RPM shell's handler. If the previous disposition is not available as a Python handler, the restore step will not pass None to signal.signal or mask the original error.

## Q1 — Post-gate shell scope

Confirmed: the saved build log contains BOLT_POST_GATE_PASS and then successfully invokes bolt_optional for the post disk report. The RPM post macro is appended to the same install shell script in which bolt_status_exit and bolt_optional are defined; it is not a new shell invocation. Signal-exit fixtures cover status propagation; this successful build log does not execute the failure-only bolt_status_exit branch.

## Q2 — BOLT jump-past-end handling

The replacement is implemented by BOLT itself, not by clang-bolt-helper.py. BinaryFunction.cpp handles a branch to the exact end of a function, within its maximum extent, as a pattern produced by __builtin_unreachable; it emits a nop and records conditional branches for profile validation. The helper preserves the log and checks the candidate. The warning text alone is not sufficient to label every occurrence benign. This build has ten such replacements: five have been matched instruction by instruction to llvm_unreachable in the source; the other five have matching structure but are not yet individually closed. We do not describe all ten as benign.

## Q3 — Build parallelism

The saved build log confirms ninja -d keeprsp -j 6. The fallback mlgo_build_jobs=6 already exists in the parent commit; the outer job setting did not override it in this build. We will keep that policy in this series because changing ThinLTO concurrency affects linker memory. If needed, we can evaluate parallelism separately in another change.

## Q4 — Package size and stage resources

The requested accel-package unpacked size and setup-time measurement need the exact package and setup boundary; they cannot be inferred from the clang executable size. Please confirm the target accel package and whether setup includes dependency installation. In the saved build, BOLT begin through compare-root took 330 seconds, with a separate 15-second post gate. The largest recorded BOLT-scoped disk snapshot was 5,028,364,288 bytes; it is not a continuously measured peak or total buildroot usage.

## Q5 — Plugin symbol export

The current clang link does not combine libLLVM or libclang-cpp with its component archives. The recorded configuration has plugin support enabled, LLVM_EXPORT_SYMBOLS_FOR_PLUGINS disabled, and adds --export-dynamic to the statically linked clang. Exporting its symbols does not itself add another LLVM definition. This does not prove compatibility with an arbitrary plugin that brings its own LLVM copy; that case needs a plugin-specific loading check. The next validation will include a minimal plugin-loading case with the intended linking mode; no product change is proposed for this question.

## Q6 — Disabling the optimizations

Done in PS5. The llvm_speedup switch is enabled by default. Disabling it turns off hybrid linkage (Part 1) and the BOLT pipeline (Part 2), restoring the parent linking configuration and ordinary clang. ThinLTO/MLGO, fixed compilation flags and native archive conversion remain enabled. The fixed flags filter project options that clang does not accept; the converter and its safety checks remain independent of the two switches. The installed AddLLVM.cmake and AddClang.cmake texts still contain the conditional hybrid support, so disabling the switch does not restore the entire parent tree.

In the project's build configuration, add this in the Macros: section:

    %_without_llvm_speedup 1

For a local GBS build, use:

    gbs build --define '_without_llvm_speedup 1'

To restore the default, remove the macro definition. Setting it to 0 does not restore the default: the presence of the _without_ macro disables the feature.

The individual switches are hybrid_link and clang_bolt. Define _without_hybrid_link or _without_clang_bolt in the same way to disable that part alone. Disabling llvm_speedup overrides both individual switches. The hybrid-linkage-off/BOLT-on combination is supported by the configuration but has not yet been certified by an actual build.
