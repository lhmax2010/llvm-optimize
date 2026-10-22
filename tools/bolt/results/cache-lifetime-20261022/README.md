# ThinLTO cache and BOLT artifact lifetime, 2026-10-22

Read-only analysis of 9e5675f57d122549997caffa39b655dfefc46fee.
No build, CMake/Ninja, product helper, Source1005, or cleanup was run.

- `source/`: exact git-show snapshots; paths and SHA256 in source-provenance.json.
- `source-excerpts.txt`: original line numbers, with excerpt-index.json.
- `historical/`: copied prior install/cache/link evidence and read-only Tizen scripts;
  origins and SHA256 in historical-provenance.json. These are not new 9e QB data.
- `historical-install-audit.json`: text-only scan of all 667 saved ordinary install scripts.
- `historical-bolt-link-edge.json`: saved Ninja text, not execution of Ninja.
- `historical-debug-cache-search.json`: historical RPM/DWARF text searches, no ELF execution.
- `policy-search.json`: exact source searches for explicit cache-pruning policy.
- `doc29-input.json`, `doc29-excerpts.txt`, `estimate.json`: historical numbers and bounded estimates.
- `validation.json`: identity/range/scope checks, not a product gate result.

The last content-dependent cache user is the clang relink (helper line 1160).
Reports and failure diagnostics still inspect cache metadata; missing cache is
accepted. The distinction is explicit in docs/bolt/30_cache_lifetime.md.

Lookup-only corrections: POSIX sh did not expand a brace expression used for two
file names; an initial relative temp search used the evidence repository; ignored
tar files required rg --files --no-ignore. All were resolved without product work.
