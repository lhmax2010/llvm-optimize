#!/usr/bin/env bash
# Unit/error-injection tests plus actual ELF integration checks. Never compiles.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
workspace=$(cd -- "$here/.." && pwd)
static="$workspace/temp/toolchain-baseline/usr/bin/clang-22"
dynamic="$workspace/temp/spec-review-20260921/unpacked/snapshot-clang/usr/bin/clang-22"
arm=/home/linhao/GBS-ROOT-TIZEN-UNIFIED-LLVM/local/BUILD-ROOTS/scratch.armv7l.0/usr/bin/clang-22
bolt="$workspace/temp/bolt-final-20260918/optimized/bin/clang-22"
loader=/lib64/ld-linux-x86-64.so.2
while (($#)); do
    case "$1" in
        --static|--dynamic|--arm|--bolt|--loader)
            (($# >= 2)) || { echo "Missing value: $1" >&2; exit 2; }
            case "$1" in
                --static) static=$2 ;; --dynamic) dynamic=$2 ;; --arm) arm=$2 ;;
                --bolt) bolt=$2 ;; --loader) loader=$2 ;;
            esac; shift 2 ;;
        --help|-h)
            cat <<'HELP'
Usage: test_verify_toolchain_identity.sh [--static ELF] [--dynamic ELF]
       [--arm ELF] [--bolt ELF] [--loader ELF]
Default fixtures are this project's existing static baseline, downloaded dynamic
snapshot, ARM GBS clang, and BOLT artifact. Override paths on other machines.
Requires an x86_64 test host and all four real executable fixtures: missing inputs
FAIL instead of silently skipping the required positive/negative integration tests.
Only the native static compiler is queried with --version, through --loader.
ARM, dynamic, and BOLT files are read only; no compilation or binary modification.
Error-injection tools and synthetic wrappers live in a private temporary directory.
HELP
            exit 0 ;;
        *) echo "Unknown option: $1" >&2; exit 2 ;;
    esac
done
[[ $(uname -m) == x86_64 ]] || { echo 'Tests require x86_64 host for real ARM mismatch control' >&2; exit 2; }
for file in "$static" "$dynamic" "$arm" "$bolt" "$loader"; do
    [[ -f "$file" && -x "$file" ]] || { echo "Missing executable fixture: $file" >&2; exit 2; }
done
suite_tmp=$(mktemp -d "${TMPDIR:-/tmp}/llvm-identity-tests.XXXXXXXX")
trap 'chmod -R u+rwX -- "$suite_tmp"; rm -rf -- "$suite_tmp"' EXIT
bash_bin=$(command -v bash)
export IDENTITY_TEST_REAL_AWK=$(command -v awk)
export IDENTITY_TEST_REAL_STAT=$(command -v stat)
export IDENTITY_TEST_REAL_READELF=$(command -v readelf)
export IDENTITY_TEST_REAL_UNAME=$(command -v uname)
export IDENTITY_TEST_MARKER="$suite_tmp/executed"
mkdir "$suite_tmp/mock" "$suite_tmp/limited"
for name in readlink sha256sum stat od uname awk readelf cat; do
    ln -s "$(command -v "$name")" "$suite_tmp/limited/$name"
done
cat > "$suite_tmp/mock/awk" <<'MOCK'
#!/bin/bash
if [[ ${IDENTITY_TEST_MODE:-} == awk-sections && "$*" == *'print $1; n++'* ]]; then
    echo 'injected section parser error' >&2; exit 7
fi
if [[ ${IDENTITY_TEST_MODE:-} == awk-needed && "$*" == *'NEEDED'* ]]; then exit 7; fi
if [[ ${IDENTITY_TEST_MODE:-} == awk-machine && "$*" == *'key=Machine'* ]]; then exit 7; fi
exec "$IDENTITY_TEST_REAL_AWK" "$@"
MOCK
cat > "$suite_tmp/mock/stat" <<'MOCK'
#!/bin/bash
if [[ ${IDENTITY_TEST_MODE:-} == stat-size && $2 == %s ]]; then
    echo 'injected stat size error' >&2; exit 7
fi
exec "$IDENTITY_TEST_REAL_STAT" "$@"
MOCK
cat > "$suite_tmp/mock/uname" <<'MOCK'
#!/bin/bash
if [[ ${IDENTITY_TEST_MODE:-} == arm-host ]]; then echo armv7l; exit 0; fi
if [[ ${IDENTITY_TEST_MODE:-} == unknown-host ]]; then echo unknown_arch; exit 0; fi
if [[ ${IDENTITY_TEST_MODE:-} == uname-fail ]]; then exit 7; fi
exec "$IDENTITY_TEST_REAL_UNAME" "$@"
MOCK
cat > "$suite_tmp/mock/readelf" <<'MOCK'
#!/bin/bash
case "${IDENTITY_TEST_MODE:-}:$1" in
    fail-header:-hW|fail-sections:-SW|fail-dynamic:-dW|fail-notes:-nW) exit 7 ;;
    empty-sections:-SW) echo 'injected invalid section listing'; exit 0 ;;
    no-details:-SW) echo '  [ 1] .text PROGBITS 0000 0010 0010'; exit 0 ;;
    partial:-SW)
        set -o pipefail
        "$IDENTITY_TEST_REAL_READELF" "$@" | "$IDENTITY_TEST_REAL_AWK" '!/\.note\.bolt_info/'
        exit $? ;;
esac
exec "$IDENTITY_TEST_REAL_READELF" "$@"
MOCK
cat > "$suite_tmp/mock/rpm" <<'MOCK'
#!/bin/bash
if [[ ${IDENTITY_TEST_MODE:-} == rpm-owned ]]; then echo 'fixture 0:22.1.8-1.x86_64'; exit 0; fi
echo 'injected RPM database/unowned query error' >&2
exit 7
MOCK
cat > "$suite_tmp/recording-loader" <<'MOCK'
#!/bin/bash
: > "$IDENTITY_TEST_MARKER"
exit 99
MOCK
printf '#!/bin/sh\ntouch "%s"\n' "$IDENTITY_TEST_MARKER" > "$suite_tmp/wrapper with spaces"
printf 'not an ELF or script\n' > "$suite_tmp/non-elf"
cp /usr/bin/true "$suite_tmp/non-executable"
chmod +x "$suite_tmp/mock/"* "$suite_tmp/recording-loader" "$suite_tmp/wrapper with spaces" "$suite_tmp/non-elf"
chmod -x "$suite_tmp/non-executable"
count=0
check() {
    local name=$1 expected_rc=$2 expected_text=$3; shift 3
    local result rc
    set +e
    result=$("$bash_bin" "$here/verify_toolchain_identity.sh" "$@" 2>&1); rc=$?
    set -e
    if [[ "$rc" != "$expected_rc" || "$result" != *"$expected_text"* ]]; then
        printf 'FAIL %s: expected exit=%s text=%s; got exit=%s\n%s\n' "$name" "$expected_rc" "$expected_text" "$rc" "$result" >&2
        exit 1
    fi
    count=$((count+1)); printf 'PASS %02d %s\n' "$count" "$name"
}
check help 0 'timeout is optional' --help
check static-native-query 0 'VERSION_EXIT=0' --loader "$loader" "$static"
check static-no-shared 0 'NEEDED_LLVM_SHARED=NO' --no-exec "$static"
check dynamic-shared 0 'NEEDED_LLVM_SHARED=YES' --no-exec "$dynamic"
check actual-arm-mismatch 0 'ARCH_MISMATCH=YES' --loader "$suite_tmp/recording-loader" "$arm"
[[ ! -e "$IDENTITY_TEST_MARKER" ]] || { echo 'FAIL ARM executed through loader' >&2; exit 1; }
check actual-arm-skipped 0 'SKIPPED' --loader "$suite_tmp/recording-loader" "$arm"
check actual-arm-needed 0 'NEEDED_LLVM_SHARED=YES' "$arm"
check actual-arm-bolt-absent 0 'EXPECTED_BOLT=PASS' --expect-bolt absent "$arm"
check bolt-present 0 'EXPECTED_BOLT=PASS' --no-exec --expect-bolt present "$bolt"
check static-bolt-absent 0 'EXPECTED_BOLT=PASS' --no-exec --expect-bolt absent "$static"
check expect-present-negative 1 'EXPECTED_BOLT=FAIL' --no-exec --expect-bolt present "$static"
check expect-absent-negative 1 'EXPECTED_BOLT=FAIL' --no-exec --expect-bolt absent "$bolt"
check expect-partial-negative 1 'EXPECTED_BOLT=FAIL' --no-exec --expect-bolt partial "$bolt"
check wrapper 3 'WRAPPER=YES' "$suite_tmp/wrapper with spaces"
check wrapper-sha-mismatch 1 'EXPECTED_SHA256=FAIL' --expected-sha256 "$(printf '%064d' 0)" "$suite_tmp/wrapper with spaces"
[[ ! -e "$IDENTITY_TEST_MARKER" ]] || { echo 'FAIL wrapper executed' >&2; exit 1; }
check non-elf 2 'WRAPPER=UNKNOWN' "$suite_tmp/non-elf"
check not-executable 0 'EXECUTABLE=NO' "$suite_tmp/non-executable"
check invalid-expectation 2 'invalid --expect-bolt' --expect-bolt yes "$static"
sha=$(sha256sum < "$static"); sha=${sha%% *}
check sha-positive 0 'EXPECTED_SHA256=PASS' --no-exec --expected-sha256 "${sha^^}" "$static"
check sha-negative 1 'EXPECTED_SHA256=FAIL' --no-exec --expected-sha256 "$(printf '%064d' 0)" "$static"
check bad-sha 2 '64 hex digits' --expected-sha256 123 "$static"
check no-library-loader 2 'requires --loader' --library-path /tmp "$static"
ln -s "$static" "$suite_tmp/clang"
PATH="$suite_tmp:$PATH" check default-path 0 "SHA256=$sha" --no-exec
mkdir -p "$suite_tmp/escape/bin"; ln -s "$static" "$suite_tmp/escape/bin/clang"
check directory-escape 2 'outside input directory' --no-exec "$suite_tmp/escape"
check missing-file 2 'not a readable regular file' "$suite_tmp/absent"
export PATH="$suite_tmp/mock:$PATH"
export IDENTITY_TEST_MODE=partial
check partial-positive 0 'EXPECTED_BOLT=PASS' --no-exec --expect-bolt partial "$bolt"
check partial-reject-present 1 'EXPECTED_BOLT=FAIL' --no-exec --expect-bolt present "$bolt"
export IDENTITY_TEST_MODE=awk-sections
check awk-sections-failure 2 'BOLT_FEATURES=UNKNOWN' --no-exec --expect-bolt absent "$static"
export IDENTITY_TEST_MODE=awk-needed
check awk-needed-failure 2 'NEEDED_LLVM_SHARED=UNKNOWN' --no-exec "$static"
export IDENTITY_TEST_MODE=awk-machine
check awk-machine-failure 2 'ARCH_MISMATCH=UNKNOWN' --loader "$suite_tmp/recording-loader" "$static"
export IDENTITY_TEST_MODE=stat-size
check stat-size-failure 2 'SIZE_BYTES=UNKNOWN' --no-exec "$static"
export IDENTITY_TEST_MODE=unknown-host
check unknown-architecture 2 'ARCH_MISMATCH=UNKNOWN' --loader "$suite_tmp/recording-loader" "$static"
export IDENTITY_TEST_MODE=uname-fail
check uname-failure 2 'ARCH_MISMATCH=UNKNOWN' --loader "$suite_tmp/recording-loader" "$static"
for mode in fail-header fail-sections fail-dynamic fail-notes empty-sections; do
    export IDENTITY_TEST_MODE=$mode
    case $mode in
        fail-header) expected_text='ELF=UNKNOWN' ;;
        fail-sections|empty-sections) expected_text='BOLT_FEATURES=UNKNOWN' ;;
        fail-dynamic) expected_text='NEEDED_LLVM_SHARED=UNKNOWN' ;;
        fail-notes) expected_text='ELF_NOTES=UNKNOWN' ;;
    esac
    check "$mode" 2 "$expected_text" --no-exec "$static"
done
export IDENTITY_TEST_MODE=rpm-owned
check rpm-information-owned 0 'fixture 0:22.1.8-1.x86_64' --no-exec "$static"
export IDENTITY_TEST_MODE=rpm-error
check rpm-information-error 0 'RPM_QUERY_EXIT=7' --no-exec "$static"
PATH="$suite_tmp/limited" check rpm-missing-information 0 'rpm missing; informational' --no-exec "$static"
PATH="$suite_tmp/limited" check timeout-missing-native-query 0 'VERSION_EXIT=0' --loader "$loader" "$static"
[[ ! -e "$IDENTITY_TEST_MARKER" ]] || { echo 'FAIL guard allowed execution' >&2; exit 1; }
mkdir "$suite_tmp/binfmt-empty" "$suite_tmp/binfmt-arm" "$suite_tmp/binfmt-match" "$suite_tmp/binfmt-negative" "$suite_tmp/binfmt-bad"
printf 'enabled\ninterpreter /emul/qemu-arm\nflags: F\noffset 0\nmagic 7f454c46\nmask ffffffff\n' > "$suite_tmp/binfmt-arm/arm-accel"
printf 'enabled\ninterpreter /fixture/interpreter\nflags: F\noffset 1\nmagic 454c00\nmask ffff00\n' > "$suite_tmp/binfmt-match/generic"
printf 'enabled\ninterpreter /fixture/interpreter\nflags: F\noffset 0\nmagic 00000000\nmask ffffffff\n' > "$suite_tmp/binfmt-negative/unrelated"
printf 'enabled\nmagic nothex\n' > "$suite_tmp/binfmt-bad/broken"
check binfmt-empty-negative 0 'BINFMT_DISPATCH_POSSIBLE=NO' --no-exec --binfmt-extra-dir "$suite_tmp/binfmt-empty" "$static"
check binfmt-magic-negative 0 'BINFMT_DISPATCH_POSSIBLE=NO' --no-exec --binfmt-extra-dir "$suite_tmp/binfmt-negative" "$static"
check binfmt-offset-mask-positive 0 'BINFMT_DISPATCH_POSSIBLE=YES' --loader "$suite_tmp/recording-loader" --binfmt-extra-dir "$suite_tmp/binfmt-match" "$static"
check binfmt-arm-entry-native-positive 0 'BINFMT_DISPATCH_POSSIBLE=YES' --loader "$suite_tmp/recording-loader" --binfmt-extra-dir "$suite_tmp/binfmt-arm" "$static"
PATH="$suite_tmp/mock:$PATH" IDENTITY_TEST_MODE=arm-host check binfmt-arm-host-arch-match 0 'ARCH_MISMATCH=NO' --loader "$suite_tmp/recording-loader" --binfmt-extra-dir "$suite_tmp/binfmt-arm" "$arm"
PATH="$suite_tmp/mock:$PATH" IDENTITY_TEST_MODE=arm-host check binfmt-arm-host-guard 0 'BINFMT_DISPATCH_POSSIBLE=YES' --loader "$suite_tmp/recording-loader" --binfmt-extra-dir "$suite_tmp/binfmt-arm" "$arm"
check binfmt-malformed-fail-closed 2 'BINFMT_DISPATCH_POSSIBLE=UNKNOWN' --loader "$suite_tmp/recording-loader" --binfmt-extra-dir "$suite_tmp/binfmt-bad" "$static"
[[ ! -e "$IDENTITY_TEST_MARKER" ]] || { echo 'FAIL binfmt guard allowed execution' >&2; exit 1; }
# New v3 controls. Overrides are test-only and may never enable execution.
check extra-dir-missing 2 '--binfmt-extra-dir must exist' --no-exec --binfmt-extra-dir "$suite_tmp/missing" "$static"
mkdir "$suite_tmp/binfmt-name" "$suite_tmp/binfmt-extension" "$suite_tmp/binfmt-no-kind" "$suite_tmp/binfmt-unreadable"
printf 'enabled\noffset 0\nmagic 00000000\n' > "$suite_tmp/binfmt-name/arm-unrelated"
check name-only-hint 0 'BINFMT_DISPATCH_POSSIBLE=NAME_ONLY' --loader "$loader" --binfmt-extra-dir "$suite_tmp/binfmt-name" "$static"
check name-only-executes-native 0 'VERSION_EXIT=0' --loader "$loader" --binfmt-extra-dir "$suite_tmp/binfmt-name" "$static"
printf 'enabled\nextension .demo\n' > "$suite_tmp/binfmt-extension/generic"
ln -s "$static" "$suite_tmp/clang.demo"
check extension-match 0 'BINFMT_DISPATCH_POSSIBLE=YES' --loader "$suite_tmp/recording-loader" --binfmt-extra-dir "$suite_tmp/binfmt-extension" "$suite_tmp/clang.demo"
check extension-negative 0 'BINFMT_DISPATCH_POSSIBLE=NO' --loader "$loader" --binfmt-extra-dir "$suite_tmp/binfmt-extension" "$static"
printf 'enabled\ninterpreter /fixture/no-kind\n' > "$suite_tmp/binfmt-no-kind/generic"
check entry-without-match-kind 2 'BINFMT_REGISTRY=UNAVAILABLE_OR_MALFORMED' --binfmt-extra-dir "$suite_tmp/binfmt-no-kind" "$static"
check override-empty 0 'BINFMT_REGISTRY_OVERRIDDEN=YES' --binfmt-registry-dir "$suite_tmp/binfmt-empty" "$static"
check override-forces-no-exec 0 'SKIPPED' --binfmt-registry-dir "$suite_tmp/binfmt-empty" --loader "$suite_tmp/recording-loader" "$static"
check override-missing 2 'BINFMT_REGISTRY=UNAVAILABLE_OR_MALFORMED' --binfmt-registry-dir "$suite_tmp/missing" "$static"
chmod 000 "$suite_tmp/binfmt-unreadable"
check registry-unreadable-native 2 'BINFMT_REGISTRY=UNAVAILABLE_OR_MALFORMED' --binfmt-registry-dir "$suite_tmp/binfmt-unreadable" "$static"
check registry-unreadable-foreign 0 'BINFMT_REGISTRY=UNAVAILABLE_OR_MALFORMED' --binfmt-registry-dir "$suite_tmp/binfmt-unreadable" "$arm"
chmod 700 "$suite_tmp/binfmt-unreadable"
check registry-malformed-foreign 0 'ARCH_MISMATCH=YES' --binfmt-registry-dir "$suite_tmp/binfmt-bad" "$arm"
check non-executable-read-only 0 'IDENTITY_STABILITY=PASS' "$suite_tmp/non-executable"
check non-executable-skipped 0 'SKIPPED' --loader "$suite_tmp/recording-loader" "$suite_tmp/non-executable"
python3 - "$suite_tmp/riscv-header" <<'PYRISC'
from pathlib import Path
import sys
b=bytearray(Path('/usr/bin/true').read_bytes()); b[18:20]=(243).to_bytes(2,'little')
Path(sys.argv[1]).write_bytes(b);Path(sys.argv[1]).chmod(0o755)
PYRISC
check riscv-synthetic-header 0 'ELF_MACHINE=RISC-V' --no-exec "$suite_tmp/riscv-header"
check riscv-mismatch 0 'ARCH_MISMATCH=YES' --loader "$suite_tmp/recording-loader" "$suite_tmp/riscv-header"
check section-count-positive 0 'SECTION_DETAIL_MATCHES=1' --no-exec "$suite_tmp/non-executable"
IDENTITY_TEST_MODE=no-details check section-count-zero 0 'SECTION_DETAIL_MATCHES=0' --no-exec "$suite_tmp/non-executable"
[[ ! -e "$IDENTITY_TEST_MARKER" ]] || { echo 'FAIL v3 guard allowed execution' >&2; exit 1; }
printf '%s/%s PASS: real ARM mismatch, dynamic/static LLVM dependency controls, wrappers, expectations, and error propagation.\n' "$count" "$count"
