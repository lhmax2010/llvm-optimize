# RPM size evidence bundle

Read [SIZE_FINDINGS.md](SIZE_FINDINGS.md) first. Paths and `:line` citations are relative to this directory. Raw download bodies and readelf output are preserved without whitespace cleanup. RPM payloads are local only under `temp/qb_size/`; each extracted tree was deleted after recording.

| Output | Contents |
| --- | --- |
| [rpm_metadata.csv](rpm_metadata.csv) | Exact RPM URLs, SHA256, bytes, versions, payload compressor/flags |
| [package_summary.csv](package_summary.csv) | Compressed and unpacked totals, net deltas, presence counts |
| [files_compare.csv](files_compare.csv) | Every paired path, size, delta, hashes, all category labels and primary category |
| [top30_files.csv](top30_files.csv) | Largest file deltas in each package |
| [elf_detail.csv](elf_detail.csv) | Selected x86_64 clang/llvm ELF files and libLLVM control, both versions |
| [elf_sections.csv](elf_sections.csv) | All section sizes for the selected ELF files |
| [elf_all.csv](elf_all.csv) | All recorded ELF metadata for auditing the classification |
| [clang_accel_sources.csv](clang_accel_sources.csv) | Every accel path and same-snapshot x86_64 source hash matches |
| [clang_accel_unmatched.csv](clang_accel_unmatched.csv) | Unmatched paths and sizes |
| [category_summary.csv](category_summary.csv) | Mutually exclusive accounting, exact fractions and decimal percentages |
| [category_membership.csv](category_membership.csv) | All rule matches; overlapping amounts must not be added |
| [source_commits.csv](source_commits.csv) | Full commit IDs, original authors, dates and subjects |
| [source_changes.csv](source_changes.csv) | Every added/removed source line, topic, endpoint/series scope and evidence |
| [source_to_categories.csv](source_to_categories.csv) | Per-line category correspondence or 未对应, with limits |
| [source_context.csv](source_context.csv) | Unchanged qemu-accel collection/strip/subpackage/ELF-editing rules |

Offline regeneration from the repository root:

```sh
python3 -B docs/qb_1199098_vs_1178133/size_attribution/scripts/analyze_sources.py
python3 -B docs/qb_1199098_vs_1178133/size_attribution/scripts/analyze_coverage.py
python3 -B docs/qb_1199098_vs_1178133/size_attribution/scripts/write_findings.py
python3 -B docs/qb_1199098_vs_1178133/size_attribution/scripts/validate_outputs.py
```

`analyze_coverage.py` also runs `analyze_sizes.py`. The validation script checks local temporary-directory cleanup as well as evidence integrity; on another machine the cleanup field is null if the local collection directory is absent. Do not execute the product code saved in raw diffs/specs. See the report for failed HTTP responses and their successful replacement evidence; HTTP status is recorded in `raw/fetch_manifest.jsonl`.
