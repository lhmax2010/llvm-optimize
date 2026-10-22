# P2/P3 approved cleanup after explicit dependency waiver

The user waived only the historical script dependency precondition for P2/P3.
All path, filesystem, process, mount and overlay conditions were checked again.
P4 remains unapproved. The original 22 RPMs and all historical scripts are kept;
re-extract the original RPMs before any future rerun of those scripts.

- `before.json`: waiver, initial checks, du and historical script hashes.
- `before/after-P*-parent-inventory.json`: other parent entries and regular-file SHA256.
- `immediate-*.json`: fresh checks immediately before each removal.
- `execution.json`: exact two rm commands, results, df and preservation comparison.
- `rm-P2.*`, `rm-P3.*`: command stdout/stderr (all empty, both rc0).
- `space-summary.json`: observed filesystem free-space change.
- `validation.json`: evidence consistency results.

`cleanup.py` records this one-time action and imports the unchanged read-only
collector from `../approved-root-cleanup-20261022/collect.py` (SHA in before.json).
Do not rerun it. It never executes the three historical scripts.
The lsof/fuser rc1 and empty stdout/stderr indicate no match for the target paths
within ordinary-user visibility; /proc mountinfo scans had no read errors.
