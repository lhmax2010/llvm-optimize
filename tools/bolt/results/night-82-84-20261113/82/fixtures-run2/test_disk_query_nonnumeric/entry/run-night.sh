#!/bin/sh
# The legacy night.py is retained but deliberately not called.
set -u
[ "$#" -ge 1 ] && [ "$#" -le 2 ] || { echo 'usage: run-night.sh SOURCE_SHA [--dry-run]' >&2; exit 2; }
source_sha=$1
case "$source_sha" in *[!0123456789abcdef]*|'') echo 'full source SHA required' >&2; exit 2 ;; esac
sha_length=$(printf '%s' "$source_sha" | wc -c)
[ -n "$sha_length" ] && [ "$sha_length" -eq 40 ] || { echo 'full source SHA required' >&2; exit 2; }
dry_run=no
if [ "$#" -eq 2 ]; then
    [ "$2" = --dry-run ] || { echo 'expected --dry-run' >&2; exit 2; }
    dry_run=yes
fi
entry_dir=$(CDPATH= cd -P -- "$(dirname -- "$0")" && pwd)
[ -n "$entry_dir" ] || { echo 'empty entry directory' >&2; exit 1; }
work=/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/night-82-84-20261113/82/fixtures-run2/test_disk_query_nonnumeric/work
build_base=$work/temp/rebase-359934-20261111-r6
summary=$work/temp/night-20261111-r6
check_linger() {
    login_user=$(id -un) || login_user=
    [ -n "$login_user" ] || return 0
    linger=$(loginctl show-user "$login_user" -p Linger --value 2>/dev/null) || linger=
    if [ "$linger" = no ]; then
        printf 'NIGHT_WARNING %s Linger=no; queue depends on user remaining logged in\n' "$(date -Iseconds)"
    fi
}
if [ "$dry_run" = yes ]; then
    check_linger
    for project in toolchain basedev; do
        if [ "$project" = toolchain ]; then
            printf 'ARGV /bin/sh %s/toolchain/launch.sh %s full\n' "$entry_dir" "$source_sha"
        else
            printf 'ARGV /bin/sh %s/basedev/launch.sh %s full basedev\n' "$entry_dir" "$source_sha"
        fi
        printf 'SERVICE rebase359934r6-%s-full-controller-20261111.service\n' "$project"
        printf 'ROOT %s/%s\n' "$build_base" "$project"
        printf 'RESULT %s/%s/evidence/result.json\n' "$build_base" "$project"
    done
    printf 'LOG %s/night.log\n' "$summary"
    printf 'DRY_RUN 已结束 %s status=ok\n' "$(date -Iseconds)"
    exit 0
fi
mkdir -p -- "$summary" || exit 1
exec >> "$summary/night.log" 2>&1
exec < /dev/null
check_linger
t_status=not_run
d_status=not_run
night_reason=unexpected-exit
project=preflight
project_status=not_run
project_done=yes
project_end() {
    project_done=yes
    printf 'NIGHT_PROJECT 已结束 %s %s status=%s reason=%s\n' "$(date -Iseconds)" "$project" "$project_status" "$night_reason"
}
finish() {
    rc=$?
    trap - 0
    if [ "$project_done" = no ]; then
        project_status=stopped
        project_end
    fi
    printf 'NIGHT 已结束 %s T=%s D=%s reason=%s rc=%s\n' "$(date -Iseconds)" "$t_status" "$d_status" "$night_reason" "$rc"
    exit "$rc"
}
trap finish 0
trap 'night_reason=signal-1; exit 129' HUP
trap 'night_reason=signal-2; exit 130' INT
trap 'night_reason=signal-15; exit 143' TERM
for project in toolchain basedev; do
    if [ -e "$build_base/$project" ] || [ -L "$build_base/$project" ]; then
        night_reason=fresh-root-required
        project_status=stopped
        printf 'fresh root required: %s/%s\n' "$build_base" "$project"
        project_end
        exit 2
    fi
done
stop_project() {
    night_reason=$1
    project_status=stopped
    project_end
    return 2
}
run_project() {
    project=$1
    project_done=no
    project_status=failed
    root=$build_base/$project
    unit=rebase359934r6-$project-full-controller-20261111.service
    if [ "$project" = basedev ]; then
        available=$(python3 -B -c 'import shutil; print(shutil.disk_usage("/home").free)') || available=
        case "$available" in ''|*[!0-9]*) stop_project disk-query-failed; return 2 ;; esac
        printf 'NIGHT_DISK %s available_bytes=%s minimum_bytes=85899345920\n' "$(date -Iseconds)" "$available"
        if [ "$available" -lt 85899345920 ]; then
            stop_project insufficient-space-before-D
            return 2
        fi
    fi
    project_status=started
    case "$project" in toolchain) t_status=started ;; basedev) d_status=started ;; esac
    launch_rc=0
    if [ "$project" = toolchain ]; then
        /bin/sh "$entry_dir/toolchain/launch.sh" "$source_sha" full || launch_rc=$?
    else
        /bin/sh "$entry_dir/basedev/launch.sh" "$source_sha" full basedev || launch_rc=$?
    fi
    if [ "$launch_rc" -ne 0 ]; then
        night_reason=launcher-failed-rc-$launch_rc
        project_end
        case "$launch_rc" in 129|130|143) return "$launch_rc" ;; *) return 2 ;; esac
    fi
    while :; do
        state=$(systemctl --user show "$unit" -p ActiveState --value) || state=
        if [ -z "$state" ]; then
            stop_project controller-state-query-failed
            return 2
        fi
        last=
        if [ -f "$root/evidence/rpm-build.log" ]; then
            last=$(tail -n 1 -- "$root/evidence/rpm-build.log") || last=
        elif [ -f "$root/controller.stdout" ]; then
            last=$(tail -n 1 -- "$root/controller.stdout") || last=
        fi
        [ -n "$last" ] || last='(no build log line yet)'
        printf 'NIGHT_PROGRESS %s %s state=%s last=%s\n' "$(date -Iseconds)" "$project" "$state" "$last"
        case "$state" in
            active|activating|deactivating|reloading) sleep 60 ;;
            inactive|failed) break ;;
            *) stop_project unknown-controller-state; return 2 ;;
        esac
    done
    service_rows=$(systemctl --user list-units --all --no-legend --no-pager --plain "rebase359934r6-$project-full-*")
    query_rc=$?
    if [ "$query_rc" -ne 0 ]; then
        stop_project project-services-query-failed
        return 2
    fi
    printf 'NIGHT_SERVICES %s %s\n%s\n' "$(date -Iseconds)" "$project" "$service_rows"
    service_check=$(printf '%s\n' "$service_rows" | python3 -B -c '
import sys
rows=[line.split() for line in sys.stdin if line.strip()]
if any(len(r)<4 for r in rows):
 print("invalid-list-units-output"); sys.exit(2)
active=[r[0]+":"+r[2] for r in rows if r[2] not in ("inactive","failed")]
if active:
 print("remaining-services="+",".join(active)); sys.exit(1)
print("all-project-services-ended")
')
    check_rc=$?
    if [ "$check_rc" -ne 0 ] || [ -z "$service_check" ]; then
        printf 'NIGHT_SERVICE_CHECK %s\n' "$service_check"
        stop_project project-services-not-confirmed-ended
        return 2
    fi
    result=$(python3 -B -c 'import json,sys; d=json.load(open(sys.argv[1])); assert isinstance(d,dict) and d.get("status") in ("ok","failed","stopped"),d; print(json.dumps(d,ensure_ascii=False,separators=(",",":")))' "$root/evidence/result.json") || result=
    if [ -z "$result" ]; then
        stop_project missing-or-invalid-result.json
        return 2
    fi
    project_status=$(printf '%s\n' "$result" | python3 -B -c 'import json,sys; print(json.load(sys.stdin)["status"])') || project_status=
    if [ -z "$project_status" ]; then
        stop_project result-status-query-failed
        return 2
    fi
    printf 'NIGHT_RESULT %s %s %s\n' "$(date -Iseconds)" "$project" "$result"
    night_reason=controller-result-$project_status
    project_end
    return 0
}
run_project toolchain
queue_rc=$?
t_status=$project_status
[ "$queue_rc" -eq 0 ] || exit "$queue_rc"
run_project basedev
queue_rc=$?
d_status=$project_status
[ "$queue_rc" -eq 0 ] || exit "$queue_rc"
night_reason=serial-builds-and-validation-finished
[ "$t_status" = ok ] && [ "$d_status" = ok ]
