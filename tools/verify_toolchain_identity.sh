#!/usr/bin/env bash
# Read-only identity checks; no workspace paths, root access, or Python required.
set -u -o pipefail
export LC_ALL=C
usage() {
    cat <<'HELP'
Usage: verify_toolchain_identity.sh [OPTIONS] [TOOLCHAIN_ROOT|BIN_DIR|CLANG]
No path: inspect the first executable clang in PATH (not shell aliases).
Roots: bin/clang, bin/clang-22, then usr/bin equivalents; bin dirs: clang, clang-22.
Directory inputs reject symlinks escaping that directory. Use an explicit ELF
path or inspect inside its root instead of accidentally selecting a host file.

  --expected-sha256 HEX  Require a SHA256 from a trusted release manifest.
  --expect-bolt STATE   Require present, partial, or absent observed markers.
                       present = .note.bolt_info; partial = only .bolt.org.*;
                       absent = neither (does NOT prove no historical BOLT).
  --loader PATH        Explicit native ELF loader for --version only.
  --library-path PATH  Loader search path; requires --loader.
  --no-exec            Skip --version; inspect without executing the input.
  -h, --help           Show this help.

Outputs include selected/resolved path, version, SHA256, ELF Machine, host arch,
BOLT sections/notes, full readelf -dW and NEEDED_LLVM_SHARED, and RPM ownership.
Architecture mismatch automatically skips execution, even with --loader, to
prevent binfmt/accel dispatch from mixing two binaries in one identity report.
Unknown architecture also skips execution and causes incomplete-inspection exit 2.
Wrappers with a shebang have WRAPPER=YES and are never executed automatically.
RPM ownership is INFORMATION ONLY: unowned files, RPM query errors, or missing
rpm do not constitute inspection failure. Original output/return code is retained.
Run inside the actual worker: e.g. /emul/usr or /emul/usr/bin/clang-22.
An RPM owner or BOLT marker alone does not prove provenance or performance.

Exit: 0 = inspection completed (not endorsement); 1 = SHA/BOLT expectation mismatch;
      2 = usage/read/tool/parse/version error or incomplete ELF inspection;
      3 = wrapper identified (without an inspection error or expectation mismatch).
Errors take precedence over expectation mismatches. Intentional --no-exec and
known architecture mismatch do not by themselves fail inspection.
Requires Bash 4+, coreutils (including od/uname), awk, readelf.
rpm is optional. timeout is optional; when present version queries have a 15s limit.
HELP
}
die() { printf 'INSPECTION=UNKNOWN\nERROR=%s\n' "$*" >&2; exit 2; }
expected= expect_bolt= loader= library_path= input= no_exec=0
while (($#)); do
    case "$1" in
        --expected-sha256|--expect-bolt|--loader|--library-path)
            (($# >= 2)) || die "missing value for $1"
            case "$1" in
                --expected-sha256) expected=$2 ;;
                --expect-bolt) expect_bolt=$2 ;;
                --loader) loader=$2 ;;
                --library-path) library_path=$2 ;;
            esac; shift 2 ;;
        --no-exec) no_exec=1; shift ;;
        -h|--help) usage; exit 0 ;;
        --) shift; (($# <= 1)) || die 'only one input path allowed'
            if (($#)); then [[ -z "$input" ]] || die 'duplicate input'; input=$1; shift; fi ;;
        -*) die "unknown option: $1" ;;
        *) [[ -z "$input" ]] || die 'only one input path allowed'; input=$1; shift ;;
    esac
done
if [[ -n "$expected" ]]; then
    [[ "$expected" =~ ^[[:xdigit:]]{64}$ ]] || die 'SHA256 must have 64 hex digits'
    expected=${expected,,}
fi
case "$expect_bolt" in ''|present|partial|absent) ;; *) die 'invalid --expect-bolt state' ;; esac
[[ -z "$library_path" || -n "$loader" ]] || die '--library-path requires --loader'
for tool in readlink sha256sum stat od uname awk readelf; do
    command -v "$tool" >/dev/null || die "missing $tool"
done
if [[ -n "$loader" ]]; then
    [[ -f "$loader" && -x "$loader" ]] || die 'loader is not executable'
    loader=$(readlink -f -- "$loader") || die 'cannot resolve loader'
fi
if [[ -z "$input" ]]; then input=$(type -P clang) || die 'clang not found in PATH'; fi
selected=$input; input_directory=
if [[ -d "$input" ]]; then
    input_directory=$(readlink -f -- "$input") || die 'cannot resolve input directory'
    selected=
    for relative in bin/clang bin/clang-22 usr/bin/clang usr/bin/clang-22 clang clang-22; do
        if [[ -f "$input/$relative" ]]; then selected=$input/$relative; break; fi
    done
    [[ -n "$selected" ]] || die 'no clang found in input directory'
fi
[[ -f "$selected" && -r "$selected" ]] || die "not a readable regular file: $selected"
[[ -x "$selected" ]] || die "input is not executable: $selected"
[[ "$selected" = /* ]] || selected=$PWD/$selected
resolved=$(readlink -f -- "$selected") || die 'cannot resolve input'
if [[ -n "$input_directory" && "$input_directory" != / && "$resolved" != "$input_directory/"* ]]; then
    die "clang resolves outside input directory: $resolved; pass explicit ELF path or inspect inside its root"
fi
before=$(stat -Lc '%d:%i:%s:%y:%z' -- "$resolved") || die 'initial stat failed'
printf 'SELECTED_PATH=%s\nRESOLVED_PATH=%s\nEXECUTABLE=YES\n' "$selected" "$resolved"
status=0 mismatch=0 wrapper=0 is_elf=0 bolt_state=unknown
if size=$(stat -Lc %s -- "$resolved") && [[ "$size" =~ ^[0-9]+$ ]]; then
    printf 'SIZE_BYTES=%s\n' "$size"
else echo 'SIZE_BYTES=UNKNOWN'; status=2; no_exec=1; fi
sha_line=$(sha256sum < "$resolved") || die 'cannot hash input'
sha=${sha_line%% *}
[[ "$sha" =~ ^[[:xdigit:]]{64}$ ]] || die 'invalid sha256sum output'
printf 'SHA256=%s\n' "$sha"
if [[ -n "$expected" ]]; then
    if [[ "$sha" == "$expected" ]]; then echo 'EXPECTED_SHA256=PASS'
    else echo 'EXPECTED_SHA256=FAIL'; mismatch=1; fi
else echo 'EXPECTED_SHA256=NOT_PROVIDED'; fi
magic=$(od -An -tx1 -N4 -- "$resolved") || die 'cannot read ELF magic'
magic=${magic//[[:space:]]/}
header_field() {
    awk -v key="$1" '$0 ~ "^[[:space:]]*" key ":" {
        sub("^[[:space:]]*" key ":[[:space:]]*", ""); print; n++
    } END {if(n!=1) exit 2}' <<< "$header"
}
if [[ "$magic" == 7f454c46 ]]; then
    echo 'WRAPPER=NO'
    if header=$(readelf -hW -- "$resolved" 2>&1); then
        is_elf=1; echo 'ELF=YES'; printf '%s\n' "$header"
        machine=UNKNOWN; elf_class=UNKNOWN; host=UNKNOWN
        if ! machine=$(header_field Machine); then machine=UNKNOWN; status=2; fi
        if ! elf_class=$(header_field Class); then elf_class=UNKNOWN; status=2; fi
        if ! host=$(uname -m); then host=UNKNOWN; status=2; fi
        host_arch=unknown; elf_arch=unknown
        case "$host" in
            x86_64|amd64) host_arch=x86_64 ;; i?86) host_arch=x86 ;;
            aarch64|arm64) host_arch=aarch64 ;; armv*|arm) host_arch=arm ;;
            ppc64*) host_arch=ppc64 ;; riscv64) host_arch=riscv64 ;;
            riscv32) host_arch=riscv32 ;; s390x) host_arch=s390x ;;
        esac
        case "$machine/$elf_class" in
            'Advanced Micro Devices X86-64/ELF64') elf_arch=x86_64 ;;
            'Intel 80386/ELF32') elf_arch=x86 ;;
            'AArch64/ELF64') elf_arch=aarch64 ;; 'ARM/ELF32') elf_arch=arm ;;
            'PowerPC64/ELF64') elf_arch=ppc64 ;;
            'RISC-V/ELF64') elf_arch=riscv64 ;; 'RISC-V/ELF32') elf_arch=riscv32 ;;
            'IBM S/390/ELF64') elf_arch=s390x ;;
        esac
        printf 'ELF_MACHINE=%s\nHOST_ARCH=%s\n' "$machine" "$host"
        if [[ "$host_arch" == unknown || "$elf_arch" == unknown ]]; then
            echo 'ARCH_MISMATCH=UNKNOWN'; echo 'WARNING=Architecture could not be verified; execution disabled.'
            no_exec=1; status=2
        elif [[ "$host_arch" != "$elf_arch" ]]; then
            echo 'ARCH_MISMATCH=YES'; echo 'WARNING=FOREIGN ELF: execution disabled to prevent binfmt/accel dispatch.'
            no_exec=1
        else echo 'ARCH_MISMATCH=NO'; fi
    else
        echo 'ELF=UNKNOWN'; printf '%s\n' "$header"; status=2; no_exec=1
    fi
elif [[ "$magic" == 2321* ]]; then
    wrapper=1; no_exec=1; echo 'WRAPPER=YES'; echo 'ELF=NO'; echo 'ARCH_MISMATCH=NOT_APPLICABLE'
else
    echo 'WRAPPER=UNKNOWN'; echo 'ELF=UNKNOWN'; status=2; no_exec=1
fi

echo 'VERSION_BEGIN'
if ((no_exec)); then echo 'SKIPPED (no-exec, architecture guard, wrapper, or incomplete inspection)'
elif ((is_elf)); then
    cmd=("$selected" --version)
    if [[ -n "$loader" ]]; then
        cmd=("$loader"); [[ -z "$library_path" ]] || cmd+=(--library-path "$library_path")
        cmd+=("$selected" --version)
        printf 'QUERY_LOADER=%s\nQUERY_LIBRARY_PATH=%s\n' "$loader" "$library_path"
        echo 'NOTE=InstalledDir under explicit loader may describe the loader directory.'
    fi
    if command -v timeout >/dev/null; then cmd=(timeout 15s "${cmd[@]}"); fi
    "${cmd[@]}" 2>&1; rc=$?
    printf 'VERSION_EXIT=%s\n' "$rc"; ((rc == 0)) || status=2
else echo 'UNKNOWN (no executable ELF identity)'; status=2; fi
echo 'VERSION_END'

if ((is_elf)); then
    echo 'DYNAMIC_BEGIN'
    if dynamic=$(readelf -dW -- "$resolved" 2>&1); then
        printf '%s\n' "$dynamic"
        if needed=$(awk '/\(NEEDED\)/ {
            if(!match($0,/\[[^]]+\]/)) exit 2
            print substr($0,RSTART+1,RLENGTH-2)
        }' <<< "$dynamic"); then
            llvm_shared=NO
            while IFS= read -r library; do
                case "$library" in libLLVM*.so*|libclang-cpp*.so*) llvm_shared=YES ;; esac
            done <<< "$needed"
            printf 'NEEDED_LLVM_SHARED=%s\n' "$llvm_shared"
            [[ "$llvm_shared" != YES ]] || echo 'WARNING=LLVM implementation code is in shared libraries; inspect their identities too.'
        else echo 'NEEDED_LLVM_SHARED=UNKNOWN'; status=2; fi
    else printf '%s\n' "$dynamic"; echo 'NEEDED_LLVM_SHARED=UNKNOWN'; status=2; fi
    echo 'DYNAMIC_END'
    if sections=$(readelf -SW -- "$resolved" 2>&1); then
        if names=$(awk '/^[[:space:]]*\[[[:space:]]*[0-9]+\]/ {
            sub(/^[[:space:]]*\[[[:space:]]*[0-9]+\][[:space:]]*/, ""); print $1; n++
        } END {if(!n) exit 2}' <<< "$sections"); then
            bolt_note=0; bolt_org=0
            while IFS= read -r name; do
                case "$name" in .note.bolt_info) bolt_note=1 ;; .bolt.org.*) bolt_org=1 ;; esac
            done <<< "$names"
            if ((bolt_note)); then bolt_state=present
            elif ((bolt_org)); then bolt_state=partial
            else bolt_state=absent; fi
            printf 'BOLT_FEATURES=%s\n' "$bolt_state"
            if ! awk '/\.note\.bolt_info|\.bolt\.org\.|\.text\.cold|\.rodata\.cold|\.gnu_debuglink/' <<< "$sections"; then
                echo 'SECTION_DETAILS=UNKNOWN'; status=2
            fi
        else echo 'BOLT_FEATURES=UNKNOWN'; status=2; fi
    else printf '%s\n' "$sections"; echo 'BOLT_FEATURES=UNKNOWN'; status=2; fi
    echo 'ELF_NOTES_BEGIN'; readelf -nW -- "$resolved" 2>&1 || status=2; echo 'ELF_NOTES_END'
else echo 'NEEDED_LLVM_SHARED=UNKNOWN'; echo 'BOLT_FEATURES=UNKNOWN'; fi
if [[ -n "$expect_bolt" ]]; then
    if [[ "$bolt_state" == unknown ]]; then echo 'EXPECTED_BOLT=UNKNOWN'; status=2
    elif [[ "$expect_bolt" == "$bolt_state" ]]; then echo 'EXPECTED_BOLT=PASS'
    else echo 'EXPECTED_BOLT=FAIL'; mismatch=1; fi
fi

echo 'RPM_DATABASE=host; RPM ownership is information only (inspect in the actual worker/root)'
if command -v rpm >/dev/null; then
    for path in "$selected" "$resolved"; do
        printf 'RPM_PATH=%s\n' "$path"
        rpm -qf --qf '%{NAME} %{EPOCHNUM}:%{VERSION}-%{RELEASE}.%{ARCH}\nSOURCE=%{SOURCERPM}\n' -- "$path" 2>&1
        rc=$?; printf 'RPM_QUERY_EXIT=%s\n' "$rc"
        ((rc == 0)) || echo 'RPM_OWNER=UNOWNED_OR_QUERY_ERROR (informational; see original output)'
        [[ "$selected" != "$resolved" ]] || break
    done
else echo 'RPM_OWNER=UNKNOWN (rpm missing; informational)'; fi
if after=$(stat -Lc '%d:%i:%s:%y:%z' -- "$resolved") && final_path=$(readlink -f -- "$selected"); then
    if [[ "$before" != "$after" || "$final_path" != "$resolved" ]]; then
        echo 'IDENTITY_STABILITY=FAIL'; status=2
    else echo 'IDENTITY_STABILITY=PASS'; fi
else echo 'IDENTITY_STABILITY=UNKNOWN'; status=2; fi
((status == 0)) || exit "$status"
((mismatch == 0)) || exit 1
((wrapper == 0)) || exit 3
exit 0
