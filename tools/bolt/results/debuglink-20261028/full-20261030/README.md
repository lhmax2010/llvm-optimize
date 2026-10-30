# Debuglink full build, 2026-10-30/31

Build PASS; identity PASS; RPM23 PASS; object90 PASS.
New-chroot installation/debugger test NOT RUN: existing sudo chroot authorization returned `sudo: a password is required` at the first device-preparation command. No retry or alternate elevation. Overall validation stopped.

See docs/bolt/43 section 9. All original output is under temp/debuglink-20261028/full-20261030/. `artifact-manifest.json` maps original files to published files with both SHA256 values and sizes. Files larger than 1 MiB are gzip-compressed; decompression preserves original line numbering.

- `validation-summary.json`, `validation-final-audit.json`: outcome and clean shutdown.
- `validation/full-package.log.gz`: authoritative complete package log.
- `validation/rpm-summary.tsv`, `validation/rpm-comparison/`: all 23 payload comparisons and strict ar-date proofs.
- `validation/objects-current/result.json`, per-call logs: full 90-pair object comparison.
- `validation/installed-test/`: first command and authorization failure, no installation performed.
- `resource-summary.json`, `resources.jsonl.gz`, `du-root.jsonl`, `bolt-process.jsonl`: actual current-run data; UNKNOWN where unobserved.
- `validation-scripts/` and `validation/*.diff`: copied scripts with path-only changes.
- `build-gates/`: actual in-build gate reports and logs.
- `products-SHA256SUMS`: preserved 37-product identity list; binaries/RPMs remain local.

No source/launcher changes, Gerrit/sandbox pushes or QB actions.
