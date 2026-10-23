# Hybrid local validation evidence

Source: 6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2. No source/spec edit or Gerrit/QB operation.

- Inputs/export: preflight.json, export-checks.json, build-command.json, build-metadata/.
- Primary build: build-result.json, controller-result.json, service.stdout/stderr, rpm-build.log.
- Disk: du-root-complete.jsonl (authoritative), du-root.jsonl (initial observer failure history), du-missing-coverage.json, timeline.tsv, disk-comparison.json, final-sizes.json. Missing samples are not zero/interpolated. The longest gap between successful periodic scans is 76.3 minutes.
- Resources: resources.jsonl.gz, build-result.json, concurrent-build-observation*.json. cgroup io.stat was not exposed.
- Packages: rpm-identities.json, rpm-size-comparison.json, rpm-name-check.json, install-rpms.json, rpm-installed-verify.json.
- NEEDED: linkage-188.json (166 default outputs); optional-target-* (first supplemental attempt failed); optional-remaining-* (18 remaining targets succeeded); linkage-188-supplemental.json (183 PASS, four missing, one ANALYSIS_PENDING). installed-needed-corrected.json passes 170 installed ELF paths. The initial installed-needed.json accidentally included four .debug files; retained with the correction explained.
- Runtime: runtime-final.json (144 PASS / 158 entries, 14 runtime dependency failures, zero missing shared libraries), runtime-equivalent/, runtime-baseline-comparison.json. Missing runtime dependencies were recorded; no extra packages were installed.
- Objects: objects-result.json, objects-summary.json, objects/ (90/90 byte-identical complete objects), tu-inputs.json. Binary objects stay in the retained root, not in Git.
- SDK/native: sdk-*.json, sdk-imported-files.tsv (329 records), native-smoke-result.json.
- Static archives: native-archive-summary.json.gz (Source1005), archives-result.json, archive-inspection.jsonl.gz (225 independent index/member checks).
- ARM parse only: parse-{armv7l,aarch64}.json, arm-parse-result.json, rpm-package-version.json.
- AnnotateFunctions exception: annotate-analysis.json, annotate-link-edge.txt, annotate-dynsym.json, annotate-plugin-smoke-corrected.json. The initial plugin probe argv was incorrect and is retained in annotate-plugin-smoke.json; the corrected driver forwarding probe succeeds. The frozen NEEDED expectation is not changed.
- Final state: final-input-audit.json. Source is clean; configuration hashes unchanged; task services inactive; root retained.

`compression-provenance.json` gives original and gzip SHA/size. Three large raw files remain locally and are published as gzip; they are not deleted. `evidence-manifest.json` indexes published bytes. Archived Python scripts were originally executed from `temp/hybrid-local-20261023`; they are auditing records, not instructions to rerun from this evidence directory. The full build ran once; subsequent nondefault targets and validation were excluded from its peak measurement.
