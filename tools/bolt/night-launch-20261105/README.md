# Toolchain-only QB-snapshot rebuild entry

This local entry builds only Toolchain from source `9e39fa8a61392652bb28b75fc26216675bcad1d5`.
It does not push source or run QB. Full mode is prepared, not executed during the daytime task.

```
/bin/sh /home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/night-launch-20261105/launch.sh 9e39fa8a61392652bb28b75fc26216675bcad1d5 full
```

Root: `W/temp/night-20261105/toolchain` (must not exist).
Configuration: `W/temp/night-20261105/configs/toolchain/gbs.conf`.
Snapshot: `tizen-base-toolchain_20261030.061318`, packages and debug only.
`build.conf` SHA256: `8f201a0d58eb634e60a1f213f47fc09dfa953d9869cdc5724f326a76203587bf`.
QB1216409's child1216412 log resolves the original reference URL to this exact snapshot.

The existing gbs-driver layout, macros (jobs8, smp j8, customized j20), threads30,
MemoryMax=MemTotal−8GiB, swap0, CPUQuota1200%, nice10 and ionice2/7 remain local only.
The existing GBS driver uses its previously authorized noninteractive sudo calls;
there is no new credential prompt in this launcher.

`launch.sh SHA rehearsal` / `rehearsal-02` stop when the actual CMake command starts.
The first attempt is retained: the sampler copied the completed prep log before
GBS reset it, producing one restart. The new epoch handoff starts copying only the
new build log. Its independent fixture requires zero prep bytes, zero restarts,
and byte-identical copy. Resource reporting uses `.build.log` only for a rehearsal;
full validation still requires the bounded original successful GBS log.

`qb-reference.json` preserves QB identity/profile/FLAGS evidence. Automatic validation
requires all three SHA values to match QB, exact FLAGS (zero warnings), profile
counts, existing BOLT anchors/debugfiles/CRC, 23 RPM comparisons and 90 TUs against
QB clang. It compares all package differences; no source-spec spelling exception
is silently introduced. RPM header metadata and payload timestamps are reported
separately. Content proof uses doc60 rules plus the approved ET_REL-only relocation
of ALLOC file offsets after resized record sections. EXEC/DYN offsets remain strict.

The full build and its validation have **not** been run by this preparation task.
Inherited helper modules are retained for provenance; use only `launch.sh` as entry.
The old two-project coordinator is disabled; no Base-Dev job is dispatched.
