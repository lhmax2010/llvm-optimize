# QB metadata switch: pre-upload evidence (2026-10-28)

Both reviews STOPPED and NOT UPLOADED. No Gerrit review IDs were created.
See docs/bolt/46_qb_meta_toolchain_switch.md for exact scope and stop conditions.

- metadata/: all original files for four relevant projects at master 7b2f2ae; SHA/path provenance in metadata-provenance.json. All project_config files unchanged.
- repos/: fixed snapshot metadata and package indexes. Base/Toolchain primary originals are already committed under tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots; their all-architecture parses are kept here. Unified primary checksums were verified against repomd.xml.
- base-missing-dependencies.json: raw and simple-macro-expanded spec dependencies, conditions, provides-name matches, versioned old binary Requires, and unresolved macro lines. Not a full RPM dependency solver.
- base-config-providers.* and unified-config-providers.*: all evaluated config directive RHS names and provider evidence. Substitute LHS names are triggers, not packages that must be installed. Keep and untriggered rules must not be equated with mandatory dependencies.
- unified-fixed-source-comparison.json / unified-repository-changes.tsv: fixed standard manifest vs current Toolchain and actual QB inventory. Metadata-only manifest comparison also retained; emulator-only repositories explain its different count.
- unified-missing-dependencies.json: old Unified RPM package names and Requires compared with new Unified and the hypothetical Unified+Base union. This union does not establish that QB can create the second DOD. Full Unified spec dependency certification was NOT RUN after the topology/source stop.
- qb/: authenticated overview and four complete read-only log downloads, gzip compressed. Only post-login rendered text/screenshot and download URLs are saved. No cookies/auth headers/forms. Actual recent job was GBS, no DOD creation command.
- mlgo/: four minimal C compile results, ELF outputs' identities, actual runtime loader listings, full stdout/stderr, URLs and checksums. RPM payloads stay under this task's temp directory, not committed. No RPM script/install, no linking or package build.
- debug-discovery.json / debug-layout.json: debug uses flat RPM files under debug/. Guessed debug/<arch>/ URLs returned404 and were corrected by inspecting the parent index; not a missing-debug verdict.
- scripts/: readonly collection/analysis and temporary compile scripts, tied to original local paths. They are evidence, not portable installers. No code/config mutations or upload logic.

The existing local fd60db96 two-line diff is base-existing.diff; no rebase or second local change was made. Debuglink work remains paused and excluded from this commit.
