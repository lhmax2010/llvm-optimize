# QB 1210836 / 1211014 read-only acquisition

Report: [44_qb_failure_1210836_1211014.md](../../../../docs/bolt/44_qb_failure_1210836_1211014.md).

- `1210836/`: parent 1210836, child 1210837.
- `1211014/`: parent 1211014, child 1211018.
- `*-full-log.txt.gz`: byte-exact Save downloads, gzip compressed. Line numbers refer to decompressed originals.
- `provenance.json`: original page/download URLs, retrieval times, sizes and SHA256. Wicket Save URLs are historical session-scoped navigation URLs, not authentication headers or exported cookies.
- `overview.*`, `child-overview-explicit.*`: actual overview text and screenshots. Initial `child-overview.*` landed on the remembered log tab and is retained with this qualification.
- `*-log-page.*`, `child-step-status.*`: log download pages and pipeline step statuses.
- `build-profiling.*`: route returned overview, not a profiling report.
- `html-report.*`, `gbs-reports*`: inspected report pages, no per-package logs exposed.
- `published-*.txt`: public artifact HTTP404 response bodies; these are not Base snapshot availability checks.
- `*-excerpts.txt`: numbered unaltered lines from downloaded logs.
- `*-search.json`: regular expressions, hit counts and full matching lines; zero hits apply only to these acquired logs.
- `timeline.tsv`, `package-log-availability.json`: stage and availability summaries.
- `visible-read-links.json`: filtered page-visible build/download links.
- `local39-*`: provenance and numbered excerpts from the previously committed local build log; not a new run.
- `privacy-check.json`: temporary headed login and empty token-field audit. No cookie, login form, credential or authentication-header export.
- `SHA256SUMS`: all evidence files except this checksum file itself.

No source changes, build commands, QB state changes, or Gerrit/sandbox writes were performed. Browser was closed after acquisition. There are no individual LLVM package logs in this bundle: both NGBS projects failed dependency repository resolution before package execution was observed.
