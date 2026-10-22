# Approved copy cleanup, 2026-10-22

Result: P1 deleted; P2/P3 skipped because existing scripts consume them.
P4 upper and all other roots were outside the deletion scope.

- `per-item-results.json`: five required preconditions for each target.
- `dependency-review.json`, `script-references.json`: skip reasons and original lines.
- `before-*`, `immediate-*`: du, df, recursive lsof, fuser, mountinfo checks.
- `execution.json`, `rm-P1.*`: exact one removal command and return values.
- `after-*`, `remaining-parents-summary.json`: surviving parent files and their hashes.
- `space-summary.json`: df delta versus the three-copy 135.85 GiB estimate.
- `authorization-and-notes.json`: approved scope and lookup permission limitation.
- `validation.json`: arithmetic, appendix, and preservation consistency checks.

`collect.py` only reads target trees and writes evidence here. `execute-approved.py`
is the exact one-time execution record, not a general cleanup tool; do not rerun.
The empty lsof/fuser output with exit 1 means no match for these target paths.
These ordinary-user observations do not assert future process inactivity.
