# build.conf project-wide audit, 2026-10-28

Read-only investigation; no package build, no Gerrit/QB changes.
Report: `docs/bolt/45_qb_meta_fix_and_snapshot.md`, sections 6–10.

- `config-classification.{json,tsv}`: all changed directives/macros, original line numbers and architecture conditions. Full input configs and diff remain in `../../../qb-meta-fix-and-snapshot-20261028/snapshots/` (repository path: tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots).
- `source-index-1.html`, `srpm-list.txt`, `spec-acquisition.json`, `specs/`: all 365 indexed SRPM recipes, 256 source package names. HTTP streams stop after the header-listed specs; prefix digest is NOT the entire RPM digest. `content_length` is the server-reported RPM length; each extracted spec has a full SHA256.
- `git-spec-provenance.json`, `git-specs/`: supplementary tizen_base branch reads; branch lookup and archive are separately recorded.
- `git-qb-spec-provenance.json`, `qb-specs/`: missing or version-mismatching recipes retrieved by explicit QB commit. No source scripts executed.
- `project-spec-coverage.json`: 245 current manifest repositories and 251 actual QB repositories; union 252. The 251 actual repositories all have matching-commit recipes. tensorflow2 appears only in the current manifest.
- `spec-macro-usage.*`: all 403 retained spec records, exact lines and comment flags; old and current variants intentionally coexist. `package-impact.*` has 285 labels, NOT 285 distinct current project repositories (source-package labels and Gerrit repository labels overlap).
- `project-impact.json`: 252 repository rows corresponding to the report; effects are conditional static analysis, not build outcomes.
- `critical-spec-excerpts.txt`, `macro-coverage.json`: branch-specific text and all 31 changed macro names, including zero direct matches.
- `query-*`, `query-results.json`: 24 read-only queryconfig calls, not RPM spec/build certification.
- `*-config-flow.txt`: original log line numbers. `toolchain-*`, `repository-*`, `*-history*`, `*-diffs.txt`: metadata and history evidence. `tools-override-example.txt` preserves an initial wrong-path lookup error; the corrected Tools files are named `tools-example-*`.
- `validation.json`: source completeness/SHA, local report links and preserved local commits.
- `scripts/`: collection/analysis scripts retained for inspection, with original absolute local paths. They write evidence locally, do not build packages or change project configuration. Not a portable installation script.

No evidence establishes the final NGBS merged RPM macro set. The unchanged Toolchain project_config and Base get_build_conf_text URL must not be conflated. No credentials/cookies/authentication headers are collected.
