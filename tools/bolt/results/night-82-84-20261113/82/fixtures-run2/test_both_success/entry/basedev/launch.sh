#!/bin/sh
set -eu
project=basedev
printf '%s
' "$project" >> "$MOCK_CALLS"
root=$MOCK_WORK/temp/rebase-359934-20261111-r6/$project
mkdir -p "$root/evidence"
if [ "$project" = toolchain ]; then
 printf 'accepted
' > "$root/controller-accepted"
 if [ "$MOCK_RC" -ne 0 ]; then exit "$MOCK_RC"; fi
fi
if [ "$project" = basedev ] && [ "$MOCK_MISSING_D" = yes ]; then exit 0; fi
status=ok
if [ "$project" = toolchain ]; then status=$MOCK_TSTATUS; fi
if [ "$project" = toolchain ] && [ "$MOCK_MISSING" = yes ]; then exit 0; fi
if [ "$project" = toolchain ] && [ "$MOCK_INVALID" = yes ]; then
 printf 'invalid json
' > "$root/evidence/result.json"
else
 printf '{"status":"%s","reason":"fixture"}
' "$status" > "$root/evidence/result.json"
fi
printf 'fixture last build line
' > "$root/evidence/rpm-build.log"
