#!/bin/sh
bolt_fail() {
  python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py disk-diagnose "$1" "$2" || true
  exit 1
}
bolt_checked() {
  bolt_stage=$1
  bolt_log=$2
  shift 2
  if bolt_output=$("$@" 2>&1); then
    printf '%s\n' "$bolt_output" || bolt_fail "$bolt_stage-output" -
  else
    printf '%s\n' "$bolt_output" || true
    printf '%s\n' "$bolt_output" | python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py disk-diagnose "$bolt_stage" /dev/stdin || true
    exit 1
  fi
}
bolt_step() {
  bolt_stage=$1
  shift
  bolt_checked "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py run-step "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" -- "$@"
}
bolt_step fixture-step /bin/sh -c 'echo fixture failure >&2; exit 7'
echo SHOULD_NOT_RUN
