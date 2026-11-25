# Held-out compiler throughput

Run the harness on Linux with Python 3.11+, GNU time and taskset. Provide a JSON
configuration with `variants` and `inputs`. Each runnable variant has
`status: "PASS"`, an absolute `clang` path, its `sha256`, the matching
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
runs use the private loader and integrated cc1. They never link or rebuild a
toolchain.

GNU time records user CPU, system CPU and peak RSS per TU. Monotonic wall time
covers the timed launcher and compiler. Serial totals are sums of TU wall
times. Parallel totals use elapsed time for a variant batch. The JSON includes
both totals, the raw per-TU values, and process-name and host snapshots at each
end of a round. Per-TU speedup uses paired elapsed times and the median for
that TU. Incomplete rounds are excluded from variant total summaries. The
median and IQR use inclusive quartiles. A single valid round has zero IQR by
construction.

Every successful object is compared byte for byte with V0. JSON stores both
object paths and digests. Markdown marks mismatches in red and retains the
timing measurements. All variants use the same working path for a given TU.
The script pauses below 6 GiB host MemAvailable. If this happens mid-compile it
stops its own compiler group, keeps the interrupted logs and repeats the sample
after recovery. That incomplete sample does not enter the compiler timings.

The process survey reads only Linux comm names. Generic names cannot identify
a project. An installation with a known unique name may supply it via
`--other-build-comm`; the status remains UNKNOWN without such a name.

Run the tests with `python3 -m unittest discover -s tools/bolt/bench -v`.
