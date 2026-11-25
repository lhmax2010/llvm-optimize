# Pilot check only, not formal benchmark data

Rounds 1, jobs 1, CPUs [19].

One warmup batch per variant is excluded. The primary metric is user + system CPU time.

| Variant | Valid rounds | Median CPU (s) | CPU IQR (s) | Median wall (s) | Speedup vs V0 | Per-TU speedup Q1 / median / Q3 | Objects |
|---|---:|---:|---:|---:|---:|---|---|
| V0 | 1 | 15.970 | 0.000 | 16.098 | 1.000× | 1.000× / 1.000× / 1.000× | 0 same / 0 different / 0 unverified |
| V1 | 1 | 13.360 | 0.000 | 15.466 | 1.195× | 1.000× / 1.129× / 1.275× | 5 same / 0 different / 0 unverified |

## Quiet and interference rounds

Interference means that a sampled process name matched a build tool. Generic names cannot identify the owning project.

| Group | Variant | Valid rounds | Median CPU (s) | Median wall (s) |
|---|---|---:|---:|---:|
| quiet | V0 | 0 | — | — |
| quiet | V1 | 0 | — | — |
| interference | V0 | 1 | 15.970 | 16.098 |
| interference | V1 | 1 | 13.360 | 15.466 |

## Object differences, failures, and retries

