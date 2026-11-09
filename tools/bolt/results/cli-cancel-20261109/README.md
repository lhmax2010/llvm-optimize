# cli cancellation fix and sandbox update

Report: docs/bolt/70_second_code_review_fixes.md §10.

fix.diff/final.diff contain the same four added helper lines. verify_commits.py checks unchanged first SHA/tree, byte-identical third commit diff/message, trailers, identities and final diff.

helper.stderr: 393 PASS; review70.stderr: 12 PASS; cli-cancel.stderr: 2 PASS (SIGHUP/SIGINT/SIGTERM and unchanged uncancelled KeyError).
parse/: 12 actual Tizen rpmspec expansions, byte-identical to 5a27edb4.
push.txt: exact combined output of the single lease-protected sandbox push.
ls-remote-before/after, chain-after, change-359934/change-357163: original read-only verification output.

Tests use retained-cleanup wrappers and new scratch paths. No complete build, sudo, QB operation, Gerrit review upload, or branch creation.
