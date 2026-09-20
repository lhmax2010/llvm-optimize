#!/usr/bin/env bash
# Read-only identity checks. No workspace paths, root access, or Python required.
set -u
export LC_ALL=C

usage() {
    cat <<'EOF'
Usage: verify_toolchain_identity.sh [OPTIONS] [TOOLCHAIN_ROOT|BIN_DIR|CLANG]
No path: inspect the first executable clang in PATH (not shell aliases).
A root is searched for bin/clang, bin/clang-22, then usr/bin equivalents.
A bin directory is searched for clang, then clang-22. Symlinks are resolved.
Directory inputs reject symlinks escaping that directory; inspect the explicit
ELF path or run inside the correct root instead of hashing a host path by mistake.

Options:
  --expected-sha256 HEX  Require an exact SHA256 from a trusted release manifest.
  --loader PATH         Explicit ELF loader for --version only; never installed.
  --library-path PATH   Loader library search path; requires --loader.
  --no-exec             Skip --version; inspect the file without executing it.
  -h, --help            Show this help.

Outputs: selected/resolved path, ELF type/machine, version, SHA256, observed BOLT
sections/notes, GNU build ID (if present), and host RPM database ownership.
Wrappers/non-ELF files are hashed and queried but NEVER executed automatically.
Run inside the actual build/accel worker namespace to identify its compiler.
An RPM owner does not prove unmodified bytes. A BOLT marker does not establish
provenance, profile quality, or throughput. Missing markers do not prove no BOLT.
Extracted RPM files are normally not owned in the host RPM database.

Exit: 0 = inspection completed (not an endorsement); 1 = expected SHA mismatch;
      2 = usage/read/tool/query failure or incomplete ELF/version inspection.
--no-exec is an intentional omission and does not itself cause exit 2.
Requires Bash, coreutils, awk and readelf; rpm is optional (UNKNOWN if absent).
EOF
}
die() { printf 'ERROR=%s\n' "$*" >&2; exit 2; }
expected= loader= library_path= input= no_exec=0
while (($#)); do
    case "$1" in
        --expected-sha256|--loader|--library-path)
            (($# >= 2)) || die "missing value for $1"
            case "$1" in
                --expected-sha256) expected=$2 ;;
                --loader) loader=$2 ;;
                --library-path) library_path=$2 ;;
            esac
            shift 2 ;;
        --no-exec) no_exec=1; shift ;;
        -h|--help) usage; exit 0 ;;
        --) shift; (($# <= 1)) || die 'only one input path is allowed'
            if (($#)); then [[ -z "$input" ]] || die 'duplicate input'; input=$1; shift; fi ;;
        -*) die "unknown option: $1" ;;
        *) [[ -z "$input" ]] || die 'only one input path is allowed'; input=$1; shift ;;
    esac
done
if [[ -n "$expected" ]]; then
    [[ "$expected" =~ ^[[:xdigit:]]{64}$ ]] || die 'expected SHA256 must contain 64 hex digits'
    expected=${expected,,}
fi
[[ -z "$library_path" || -n "$loader" ]] || die '--library-path requires --loader'
for tool in readlink sha256sum stat awk; do command -v "$tool" >/dev/null || die "missing $tool"; done
if [[ -n "$loader" ]]; then
    [[ -f "$loader" && -x "$loader" ]] || die 'loader is not an executable file'
    loader=$(readlink -f -- "$loader") || die 'cannot resolve loader'
fi
if [[ -z "$input" ]]; then
    input=$(type -P clang) || die 'clang not found in PATH'
fi
selected=$input
input_directory=
if [[ -d "$input" ]]; then
    input_directory=$(readlink -f -- "$input") || die 'cannot resolve input directory'
    selected=
    for relative in bin/clang bin/clang-22 usr/bin/clang usr/bin/clang-22 clang clang-22; do
        if [[ -f "$input/$relative" ]]; then selected=$input/$relative; break; fi
    done
    [[ -n "$selected" ]] || die 'no clang executable found in input directory'
fi
[[ -f "$selected" && -r "$selected" ]] || die "not a readable regular file: $selected"
[[ "$selected" = /* ]] || selected=$PWD/$selected
resolved=$(readlink -f -- "$selected") || die 'cannot resolve input'
if [[ -n "$input_directory" && "$input_directory" != / && "$resolved" != "$input_directory/"* ]]; then
    die "clang resolves outside input directory: $resolved; pass the explicit ELF path or inspect inside its root"
fi
before=$(stat -Lc '%d:%i:%s:%y:%z' -- "$resolved") || die 'cannot stat input'
sha_line=$(sha256sum < "$resolved") || die 'cannot hash input'
sha=${sha_line%% *}
printf 'SELECTED_PATH=%s\nRESOLVED_PATH=%s\n' "$selected" "$resolved"
printf 'SIZE_BYTES=%s\nSHA256=%s\n' "$(stat -Lc %s -- "$resolved")" "$sha"
status=0 mismatch=0
if [[ -n "$expected" ]]; then
    if [[ "$sha" == "$expected" ]]; then echo 'EXPECTED_SHA256=PASS'
    else echo 'EXPECTED_SHA256=FAIL'; mismatch=1; fi
else echo 'EXPECTED_SHA256=NOT_PROVIDED'; fi

is_elf=0
if command -v readelf >/dev/null; then
    if header=$(readelf -h -- "$resolved" 2>&1); then
        is_elf=1
        echo 'ELF=YES'
        printf '%s\n' "$header" | awk '/Class:|Type:|Machine:/ { print }'
    else
        echo 'ELF=UNKNOWN_OR_NON_ELF'; printf '%s\n' "$header"; status=2
    fi
else echo 'ELF=UNKNOWN (readelf missing)'; status=2; fi

echo 'VERSION_BEGIN'
if ((no_exec)); then echo 'SKIPPED (--no-exec)'
elif ((is_elf)); then
    cmd=("$selected" --version)
    if [[ -n "$loader" ]]; then
        cmd=("$loader")
        [[ -z "$library_path" ]] || cmd+=(--library-path "$library_path")
        cmd+=("$selected" --version)
        printf 'QUERY_LOADER=%s\nQUERY_LIBRARY_PATH=%s\n' "$loader" "$library_path"
        echo 'NOTE=InstalledDir under an explicit loader may describe the loader directory.'
    fi
    if command -v timeout >/dev/null; then cmd=(timeout 15s "${cmd[@]}"); fi
    "${cmd[@]}" 2>&1
    rc=$?
    printf 'VERSION_EXIT=%s\n' "$rc"
    ((rc == 0)) || status=2
else echo 'UNKNOWN (wrapper/non-ELF or unavailable ELF inspection; not executed)'; fi
echo 'VERSION_END'

if ((is_elf)); then
    if sections=$(readelf -SW -- "$resolved" 2>&1); then
        names=$(printf '%s\n' "$sections" | awk '
            /^[[:space:]]*\[[[:space:]]*[0-9]+\]/ {
                sub(/^[[:space:]]*\[[[:space:]]*[0-9]+\][[:space:]]*/, ""); print $1
            }')
        has_section() { printf '%s\n' "$names" | awk -v n="$1" '$0 == n {found=1} END {exit !found}'; }
        if has_section .note.bolt_info; then echo 'BOLT_FEATURES=PRESENT (.note.bolt_info)'
        elif printf '%s\n' "$names" | awk '/^\.bolt\.org\./ {found=1} END {exit !found}'; then
            echo 'BOLT_FEATURES=PARTIAL (.bolt.org.*; provenance UNKNOWN)'
        else echo 'BOLT_FEATURES=NOT_OBSERVED (does not prove no BOLT)'; fi
        printf '%s\n' "$sections" | awk '/\.note\.bolt_info|\.bolt\.org\.|\.text\.cold|\.rodata\.cold|\.gnu_debuglink/ {print}'
        echo 'ELF_NOTES_BEGIN'
        readelf -n -- "$resolved" 2>&1 || status=2
        echo 'ELF_NOTES_END'
    else echo 'BOLT_FEATURES=UNKNOWN'; printf '%s\n' "$sections"; status=2; fi
else echo 'BOLT_FEATURES=UNKNOWN'; fi

echo 'RPM_DATABASE=host (run in the actual worker/chroot for its ownership)'
if command -v rpm >/dev/null; then
    for path in "$selected" "$resolved"; do
        printf 'RPM_PATH=%s\n' "$path"
        rpm -qf --qf '%{NAME} %{EPOCHNUM}:%{VERSION}-%{RELEASE}.%{ARCH}\nSOURCE=%{SOURCERPM}\n' -- "$path" 2>&1
        rc=$?
        printf 'RPM_QUERY_EXIT=%s\n' "$rc"
        if ((rc != 0)); then
            echo 'RPM_OWNER=UNOWNED_OR_QUERY_ERROR (see original output)'
        fi
        [[ "$selected" != "$resolved" ]] || break
    done
else echo 'RPM_OWNER=UNKNOWN (rpm missing)'; fi
after=$(stat -Lc '%d:%i:%s:%y:%z' -- "$resolved") || die 'input disappeared during inspection'
if [[ "$before" != "$after" ]] || [[ "$(readlink -f -- "$selected")" != "$resolved" ]]; then
    echo 'IDENTITY_STABILITY=FAIL (file changed during inspection)'; status=2
else echo 'IDENTITY_STABILITY=PASS'; fi
((mismatch == 0)) || exit 1
exit "$status"
