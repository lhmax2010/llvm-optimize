# QB 1221204 / 1221207 evidence

Report: docs/bolt/71_qb_1221204_1221207.md.

- overview / parent full-log: authenticated read-only browser text, no credentials or browser storage.
- manifest / architecture build logs / RPM plan and downloads: public immutable RBS URLs, sizes and SHA256.
- buildconf-provenance: immutable dependency snapshot repomd location and measured uncompressed SHA; worker logs do not print a config SHA.
- comparison: strict 67 §8.1 comparator results. 34 binary packages PASS with zero changed payload bytes; 2 source packages FAIL with fully attributed converter/VCS changes.
- archive summary and gzip member records: 3853 converted members per project, all SHA equal; 11 native members per project retained. Duplicate package ownership of libarcher_static.a is checked but counted once.
- compare-adaptation.diff and comparison-code-provenance: comparator provenance; history roots remain read-only.
- The copied comparator internally calls its result item2-result/item2-end; this is the package-comparison substep of this task's ITEM1, not the sandbox task.
- Original >1 MiB manifest JSONs remain locally untracked; gzip versions are published without deleting originals.
- All shell commands were wrapped in serial systemd user services with MemoryMax=8G, MemorySwapMax=0, CPUQuota=400%, Nice=19, IOSchedulingClass=idle. No OOM.
