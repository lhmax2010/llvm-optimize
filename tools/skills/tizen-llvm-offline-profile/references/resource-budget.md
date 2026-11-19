# Historical measurements and host policy

The timing and cgroup memory data below are historical measurements from a pinned x86_64 Tizen Toolchain setup. IR instrumentation built the compiler and runtime, followed by 23 sequential ARMv7/AArch64 training compiles. The later PGO/BOLT stages used a matching toolchain and an instrumented rewrite of the resulting PGO compiler. Earlier and later runs used different artifacts; the estimates cannot be summed into a guaranteed full pipeline duration. cgroup memory includes cache. This is not a per-process RSS measurement.

| Activity | Seconds | Peak cgroup bytes | Measurement scope |
|---|---:|---:|---|
| Instrumented Clang build | 4068.547 | 7227248640 | Configure plus compiler/profile runtime build |
| IR training | 201.930 | 1481818112 | 23 compiles |
| IR merge | 3.278 | 1824751616 | 23 raw profiles |
| PGO normal compile | 6176 | 21703991296 | Build log compile interval only |
| PGO ordinary install | 328 | 11565408256 | Build log install interval |
| BOLT tools | 418 | UNKNOWN | Build log tool build and checks |
| Relink and strip-debug | UNKNOWN | UNKNOWN | No isolated measurement |
| BOLT instrumentation | 77.954 | 17074352128 | Same-input instrumented rewrite |
| BOLT training | 379.427 | 3890348032 | 23 compiles |
| BOLT merge | 3.396 | 1585553408 | 23 fdata inputs |
| BOLT match rewrite | 44.984 | 8712601600 | Separate successful rewrite |
| Compression and final packaging | UNKNOWN | UNKNOWN | Full paired run pending |

Historical profile sizes were 746,313,472 B for 23 profraw files and 52,528,216 B for merged profdata. The 23 BOLT fdata files totaled 3,006,326,841 B. Historical root coexistence at sampled stage boundaries was 91,275,411,456 B. This boundary observation cannot identify the continuous filesystem peak. The 125.626 GiB planning lower bound includes earlier root estimates, known external profile/work files and a 30 GiB free-space reserve. It is not a guaranteed capacity limit.

Example tiers in the config are conservative planning inputs, not historical measurements. The normal tier uses a 24 GiB service cap with six jobs; reduced uses 22 GiB with two jobs. Verify the toolchain fits the cap and account for every mount. Use the approved values rather than treating these examples as deployment policy. Defer at most once, for 30 minutes or less, then report STOP when admission still fails. Use a unique lock path agreed with the host owner.

Run the wrapper on an approved host with a qualified configuration. For example, for the illustrative normal tier:

~~~sh
/usr/bin/systemd-run --user --wait --pipe --collect \
  -p MemoryMax=24G -p MemorySwapMax=0 -p CPUQuota=400% -p Nice=19 \
  -p IOSchedulingClass=idle \
  /usr/bin/python3 -B /path/to/skill/scripts/pgo_pair.py \
  --config /path/to/normal-profile-config.json --output /path/to/jobs/profile-pair
~~~

Capture the service exit, cgroup memory peak/events, disk samples, elapsed time and final controller summary. A reduced-tier retry requires a separate approved attempt with matching job limits and cgroup settings. Stop cleanly on a host resource breach, OOM, deadline, ambiguous state or lost lock. Keep the outputs and logs for diagnosis.

## One-shot stage admission

With resources.stage_admission enabled, set the stage cgroup MemoryMax to min(MemAvailable minus 6 GiB, standard cap). Full package builds use a 24 GiB cap and a 15 GiB floor. The PGO package build and BOLT tool build with relink use the 15 GiB linker floor. Historical peak caps are 120% of the measured peak, rounded up to a memory page. The instrumented build, IR training, profdata merge, BOLT instrumentation with training and merge, and BOLT match use that cap as their floor. Separate peaks were unavailable for BOLT tools with relink and manifest compression. Their cap uses the maximum observed pipeline peak at 120%. Manifest compression has a 1 GiB planning floor. The serial training, merge, rewrite and compression stages use one job. Build stages use floor(6 times MemoryMax divided by 24 GiB), with a minimum of two jobs.

Keep the existing disk admission budget and the 15 GiB disk and 6 GiB memory running stop lines. Sample admission once for each stage and retain the measured values in the summary.
