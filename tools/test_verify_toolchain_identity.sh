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
trap 'rm -rf -- "$suite_tmp"' EXIT
bash_bin=$(command -v bash)
export IDENTITY_TEST_REAL_AWK=$(command -v awk)
export IDENTITY_TEST_REAL_STAT=$(command -v stat)
export IDENTITY_TEST_REAL_READELF=$(command -v readelf)
export IDENTITY_TEST_REAL_UNAME=$(command -v uname)
export IDENTITY_TEST_MARKER="$suite_tmp/executed"
mkdir "$suite_tmp/mock" "$suite_tmp/limited"
for name in readlink sha256sum stat od uname awk readelf; do
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
if [[ ${IDENTITY_TEST_MODE:-} == unknown-host ]]; then echo unknown_arch; exit 0; fi
if [[ ${IDENTITY_TEST_MODE:-} == uname-fail ]]; then exit 7; fi
exec "$IDENTITY_TEST_REAL_UNAME" "$@"
MOCK
cat > "$suite_tmp/mock/readelf" <<'MOCK'
#!/bin/bash
case "${IDENTITY_TEST_MODE:-}:$1" in
    fail-header:-hW|fail-sections:-SW|fail-dynamic:-dW|fail-notes:-nW) exit 7 ;;
    empty-sections:-SW) echo 'injected invalid section listing'; exit 0 ;;
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
cp "$suite_tmp/wrapper with spaces" "$suite_tmp/non-executable"
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
check static-native-query 0 'ARCH_MISMATCH=NO' --loader "$loader" "$static"
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
check not-executable 2 'not executable' "$suite_tmp/non-executable"
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
    check "$mode" 2 'WRAPPER=NO' --no-exec "$static"
done
export IDENTITY_TEST_MODE=rpm-owned
check rpm-information-owned 0 'fixture 0:22.1.8-1.x86_64' --no-exec "$static"
export IDENTITY_TEST_MODE=rpm-error
check rpm-information-error 0 'RPM_QUERY_EXIT=7' --no-exec "$static"
PATH="$suite_tmp/limited" check rpm-missing-information 0 'rpm missing; informational' --no-exec "$static"
PATH="$suite_tmp/limited" check timeout-missing-native-query 0 'VERSION_EXIT=0' --loader "$loader" "$static"
[[ ! -e "$IDENTITY_TEST_MARKER" ]] || { echo 'FAIL guard allowed execution' >&2; exit 1; }
printf '%s/%s PASS: real ARM mismatch, dynamic/static LLVM dependency controls, wrappers, expectations, and error propagation.\n' "$count" "$count"
