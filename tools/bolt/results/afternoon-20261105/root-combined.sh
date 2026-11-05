#!/bin/sh
# One sudo authentication for the two already authorized operations.
set -u
PATH=/usr/sbin:/usr/bin:/sbin:/bin
export PATH
cd "$(dirname "$0")"
rc3=0
/bin/sh item3/root-test.sh > item3/root.stdout 2> item3/root.stderr || rc3=$?
printf 'ITEM3_WRAPPER 已结束 %s status_code=%s\n' "$(date -Iseconds)" "$rc3"
rc4=0
/bin/sh item4/root-delete.sh > item4/root.stdout 2> item4/root.stderr || rc4=$?
printf 'ITEM4_WRAPPER 已结束 %s status_code=%s\n' "$(date -Iseconds)" "$rc4"
printf 'ROOT_TASKS 已结束 %s item3_rc=%s item4_rc=%s\n' "$(date -Iseconds)" "$rc3" "$rc4"
[ "$rc3" = 0 ] && [ "$rc4" = 0 ]
