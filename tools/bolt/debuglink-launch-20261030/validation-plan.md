# Full build follow-up gates (unchanged from task 43)

The launch command completes full GBS packaging in a new root. It records
`build-ok-validation-pending`, never `validation PASS`. The daytime rehearsal
must not run the following gates because it produces no RPMs. After the full
build, the execution agent must perform these gates in order; stop at the first
failure, preserve originals and do not relax criteria.

1. Recheck commit 3ee2d84719e4bd358c0b2366161f70f2eb788313 and tree
   43d60f7523439fa0ccf4a61f668dd60622554606; clean source; config/build.conf
   SHA and actual macro environment. Capture full logs with hashes and timings.
2. Require BOLT_PIPELINE_PASS, BOLT_COMPARE_ROOT_PASS, BOLT_POST_GATE_PASS,
   cache release; profile N23592/M144032/S0/U1/Q383 and original thresholds.
   Strip-all SHA must be 13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8;
   after RUNPATH and before debuglink it must be
   8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf.
   Verify the new debuglink SHA chain, Build-ID, CRC, debug-file SHA/mode,
   installed and packaged bytes. The final debuglink ELF need not have the old
   no-debuglink SHA. Preserve ordinary/candidate, debug symbols, llvm-bolt,
   22 binary RPMs plus one source RPM independently, with SHA256SUMS.
3. Recheck 39's preserved products against their original 35-entry manifest.
   Compare all 23 RPM payloads against 39. Only the authorized spec/helper,
   clang debuglink and added usr/lib/debug/usr/bin/clang-22.debug may differ;
   classify ar member timestamp-only differences separately by proving every
   other byte, member order and member content SHA unchanged. No blanket ar
   exception. Existing task-43 compare.py/rpm_io.py and qualify.py are the
   reference implementations; substitute this new root/output paths only.
4. Compile all 90 preserved TU cases with ordinary and candidate from this
   build, using the same executable pathname/inode, exact original flags,
   target, verified inputs and platform libraries/resource directory. Compare
   full object bytes; require 90/90. Do not reuse 39's pass as this build's pass.
5. In a NEW test chroot, install the new clang and clang-debuginfo RPMs with
   needed dependencies. Check LLDB automatically finds the standard debuglink
   file (no manual add-symbol-file), Build-ID/CRC match, at least 20 distinct
   symbol addresses including main/cold sections, symbolizer function names,
   and the authorized crash/backtrace test. Manage temporary proc with a
   finally cleanup. Do not install into the host or a historical build root.
6. Report clang/debuginfo RPM and payload sizes against 39, total GBS wall time,
   symbol separation/add-debuglink times, actual cgroup/OOM/swap readings,
   BOLT RSS/time and sampled root-disk high water mark (not a continuous peak).
   Preserve failures and mark any unperformed test NOT RUN, not PASS.

All verification stays under full-20261030; no source edits, Gerrit/sandbox,
QB operations or deletion of existing directories. Any shell helper is POSIX sh.
