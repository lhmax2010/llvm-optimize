# Match and payload gates

## BOLT

Read the complete stdout/stderr of a trusted, successful rewrite and retain actual argv. The release invocation has exactly one -stale-threshold=5 and no infer-stale option, including an explicitly false setting. The parser uses the packaging helper's counter formats and integer comparisons.

| Counter | Meaning |
|---|---|
| N | Functions with nonempty execution profile |
| M | Functions in the input binary |
| S | Invalid or possibly stale profiles |
| U | Ignored profiled objects |
| Q | Profiled functions that could not be optimized |

N must be positive, M must be at least N, and S must be at most N. The mandatory N/M line appears once. Optional S/U/Q lines appear at most once; their absence denotes zero only for an authenticated successful complete log. Q is reported separately. R is (S+U)/(N+U), and S/N is the stale-function fraction. The gate requires both 100 × (S+U) ≤ 5 × (N+U) and 100 × S ≤ 5 × N. Percentage formatting does not decide the gate.

| N | S | U | Q | Outcome |
|---:|---:|---:|---:|---|
| 100 | 5 | 0 | 0 | Pass at equality |
| 95 | 0 | 5 | 0 | Pass at equality |
| 100 | 6 | 0 | 0 | Fail |
| 95 | 0 | 6 | 0 | Fail |
| 100 | 3 | 3 | 0 | Fail on R |
| 100 | 0 | 0 | 383 | Pass and record Q |

The count function is the packaging implementation. The file-level checker additionally requires a newline-terminated log and the exact threshold argv. Keep the rewrite status and trusted tool identity in the controller's receipt. A file assembled from pasted lines cannot establish completion and tool identity.

## Runtime dependencies

Use llvm-readelf to inspect ELF sections, symbol tables and dynamic entries. Check regular archives through readelf's member enumeration and reject malformed or external thin members. Reject __llvm_prf_* sections, __llvm_profile_* symbols and libclang_rt.profile* NEEDED libraries. Check the installed executable/shared payload and each static archive member after native conversion. Inspect the corresponding unstripped build artifacts if the release strips the required symbol table. Record missing coverage rather than treating a stripped symbol table as proof about local symbols. Do not use ldd on an .a file.
