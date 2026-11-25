#!/bin/sh
set -eu
test "$#" = 2
test "$2" = "$TASK157_REMOTE"
IFS=' ' read -r local_ref local_oid remote_ref remote_oid
test -n "$local_ref"
test "$local_oid" = "$TASK157_EXPECT_OID"
test "$remote_ref" = "$TASK157_EXPECT_REF"
case "$remote_ref" in
    refs/heads/sandbox/lhmax2025/llvm-pgo-only-*|refs/heads/sandbox/lhmax2025/llvm-pgo-bolt-*) ;;
    *) exit 3 ;;
esac
test "$remote_oid" = 0000000000000000000000000000000000000000 || {
    printf '%s\n' 'STOP: sandbox ref already exists' >&2
    exit 4
}
if IFS= read -r extra; then
    printf '%s\n' 'STOP: unexpected second update' >&2
    exit 5
fi
