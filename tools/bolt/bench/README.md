# Held-out compiler throughput

Run the harness on Linux with Python 3.11+, GNU time and taskset. Provide a JSON
configuration with `variants` and `inputs`. Each runnable variant has
`status: "PASS"`, an absolute private `root`, an absolute `clang` path, its `sha256`, the matching
`loader` path and a list of `library_path` directories. Start with V0 as the
baseline. Use `"status": "PENDING"` for unavailable variants. Input rows have
unique `id`, absolute `path`, `sha256`, `package`, `language` (`c` or
`c++`) and a list of compile `flags` including `-O2`. Store the target
and any Tizen flags in that list. The runtime files and corpus can stay
outside the evidence checkout.

~~~sh
python3 tools/bolt/bench/bench.py /path/to/config.json /path/to/new-output --cpus 3
python3 tools/bolt/bench/bench.py /path/to/config.json /path/to/new-parallel-output --cpus 2-5 -j 4
~~~

Five rounds are the default. Each round compiles the entire manifest in each
selected variant and rotates the variant order. Available variants are
selected by default. Use `--variants V0,V1` to choose an explicit subset.
Single-worker runs compile TUs in manifest order. Use `-j N` for aggregate
throughput with up to four workers in one common affinity mask. The compile
runs use integrated cc1. The harness switches the private roots behind the
same path after each variant's workers finish. It places each variant's
loader at the same regular-file path because Clang reads the resolved
executable path from `/proc/self/exe`. Relative compiler, loader and library
paths must agree across variants.

Each variant gets an unscored warmup batch. GNU time records user CPU, system
CPU and peak RSS per TU. Total user plus system time is the primary metric.
Per-TU speedup uses paired CPU times. Monotonic wall time is secondary. Wall
totals sum selected serial samples or use the elapsed parallel batch time
when that batch needed no repeats. If wall time exceeds 1.5 times CPU time
and exceeds CPU time by more than one second, repeat the sample once at the
end of the round. Keep both records. Use a successful non-anomalous repeat
for scoring. Incomplete or still-anomalous batches are excluded from the
variant total summaries. The median and IQR use inclusive quartiles.

Every successful object is compared byte for byte with V0. JSON stores both
object paths and digests. Markdown marks mismatches in red and retains the
timing measurements. A mismatch also triggers a comparison of temporary
copies with `.GCC.command.line` removed. The raw object comparison remains
the correctness result. Retry objects and their comparison are retained.
All variants use the same working path for a given TU.
The script pauses below 6 GiB host MemAvailable. If this happens mid-compile it
stops its own compiler group, keeps the interrupted logs and repeats the sample
after recovery. That incomplete sample does not enter the compiler timings.

The process survey reads only Linux comm names. The report groups rounds as
quiet or with interference based on build-tool names at the start and end
of each round. Both snapshots include load averages. Generic names cannot
identify a project. An installation with a known unique name may supply it
via `--other-build-comm`; other-project status remains UNKNOWN without one.

Run the tests with `python3 -m unittest discover -s tools/bolt/bench -v`.
