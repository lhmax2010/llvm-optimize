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
work=/home/linhao/Toolchain/development/llvm-optimize
build_base=$work/temp/rebase-359934-20261111-r6
summary=$work/temp/night-20261111-r6
if [ "$dry_run" = yes ]; then
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
t_status=not_run
d_status=not_run
trap 'rc=$?; printf "NIGHT 已结束 %s T=%s D=%s\n" "$(date -Iseconds)" "$t_status" "$d_status"; exit "$rc"' 0
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
for project in toolchain basedev; do
    if [ -e "$build_base/$project" ] || [ -L "$build_base/$project" ]; then
        printf 'fresh root required: %s/%s\n' "$build_base" "$project"
        exit 1
    fi
done
run_project() {
    project=$1
    root=$build_base/$project
    unit=rebase359934r6-$project-full-controller-20261111.service
    project_status=failed
    launch_rc=0
    if [ "$project" = toolchain ]; then
        /bin/sh "$entry_dir/toolchain/launch.sh" "$source_sha" full || launch_rc=$?
    else
        /bin/sh "$entry_dir/basedev/launch.sh" "$source_sha" full basedev || launch_rc=$?
    fi
    if [ "$launch_rc" -eq 0 ]; then
        while :; do
            state=$(systemctl --user show "$unit" -p ActiveState --value) || state=
            if [ -z "$state" ]; then
                printf 'empty service state: %s; serial queue cannot safely continue\n' "$unit"
                printf 'NIGHT_PROJECT 已结束 %s %s {"status":"failed","reason":"controller-state-unavailable"}\n' "$(date -Iseconds)" "$project"
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
                *) printf 'unknown service state: %s\n' "$state"; printf 'NIGHT_PROJECT 已结束 %s %s {"status":"failed","reason":"unknown-controller-state"}\n' "$(date -Iseconds)" "$project"; return 2 ;;
            esac
        done
        result=$(python3 -B -c 'import json,sys; d=json.load(open(sys.argv[1])); assert d["status"] in ("ok","failed","stopped"),d; print(json.dumps(d,ensure_ascii=False,separators=(",",":")))' "$root/evidence/result.json") || result=
        if [ -n "$result" ]; then
            project_status=$(printf '%s\n' "$result" | python3 -B -c 'import json,sys; print(json.load(sys.stdin)["status"])') || project_status=
            [ -n "$project_status" ] || project_status=failed
        else
            result='{"status":"failed","reason":"missing-or-invalid-result.json"}'
        fi
    else
        result="{\"status\":\"failed\",\"reason\":\"launcher-failed\",\"exit_code\":$launch_rc}"
    fi
    printf 'NIGHT_PROJECT 已结束 %s %s %s\n' "$(date -Iseconds)" "$project" "$result"
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
[ "$t_status" = ok ] && [ "$d_status" = ok ]
