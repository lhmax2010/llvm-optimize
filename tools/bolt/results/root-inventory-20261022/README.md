# 2026-10-22 read-only root inventory

No build, deletion, chmod, sudo, mount or source edit. The scripts in this
folder only read the inspected trees; their writes are report files here.
No Gerrit interaction. Report: docs/bolt/31_build_root_inventory.md.

- `scan.py`: physical mount discovery, byte-allocated `du`, df/ps/lslocks.
- `measure_units.py`: separate `du -sx` per candidate, so cross-root hardlinks
  do not hide a directory. Exit 1 permission errors remain in stderr.
- `inventory.json`, `inventory.tsv`: >5 GiB units, provenance and recommendations.
  Parent/child rows and independently counted hardlinks must not be summed.
- `activity.py`: filters the original `lsof -nP` by path boundary, records
  fuser/ps/locks and visible process mount tables. `fuser` alone is not recursive.
- `reclaim.py`: inode-level scenario for four nonoverlapping paths. It performs
  no removal or copy. It deducts a future preservation-copy allocation budget.
- `preserve-assets.json`, `additional-assets.json`: real byte sizes and SHA256;
  each file's inode/size/mtime was checked again after reading.
- `rpm-hardlinks.json`: actual device/inode comparison of the 22 RPM links.
- `exported-vcs.json`: read-only VCS lines of located existing exported specs.
- `annotations.json`, `cited-sources.json`: purpose/protection judgments and
  source-document line evidence. Unknown commits are not guessed.
- `report-validation.json`: data consistency checks, not a product/build test.

The global lsof original is retained at
`W/temp/bolt-v4-20261022-root-inventory/lsof-all.stdout` (W is the main repo).
Only original lines relevant to inventoried roots are published here.
Disk/process snapshots have different timestamps and are not atomic.

`annotations.json` is the reviewed annotation source; `annotate*.py` are
drafting helpers, not an unattended rescan/update workflow. The final lsof
original is `lsof-complete.stdout` in the same local temporary directory.
