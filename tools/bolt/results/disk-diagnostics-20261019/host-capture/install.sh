#!/bin/sh

  
  RPM_SOURCE_DIR="/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging"
  RPM_BUILD_DIR="/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD"
  RPM_OPT_FLAGS="-O2 -g"
  RPM_ARCH="x86_64"
  RPM_OS="linux"
  RPM_BUILD_NCPUS="20"
  export RPM_SOURCE_DIR RPM_BUILD_DIR RPM_OPT_FLAGS RPM_ARCH RPM_OS RPM_BUILD_NCPUS
  RPM_DOC_DIR="/usr/share/doc"
  export RPM_DOC_DIR
  RPM_PACKAGE_NAME="llvm"
  RPM_PACKAGE_VERSION="22.1.8"
  RPM_PACKAGE_RELEASE="1"
  export RPM_PACKAGE_NAME RPM_PACKAGE_VERSION RPM_PACKAGE_RELEASE
  LANG=C
  export LANG
  unset CDPATH DISPLAY ||:
  unset DEBUGINFOD_URLS ||:
  RPM_BUILD_ROOT="/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64"
  export RPM_BUILD_ROOT
  
  PKG_CONFIG_PATH="${PKG_CONFIG_PATH}:/usr/lib64/pkgconfig:/usr/share/pkgconfig"
  export PKG_CONFIG_PATH 
  set -x
  umask 022
  cd "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD"
    /bin/rm -rf "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64"
    /bin/mkdir -p "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT"
    /bin/mkdir "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64"

cd 'llvm-22.1.8'
cd build
# Reject debug-named buildroots before any BOLT action.
case $(printf '%s' '/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64' | LC_ALL=C tr '[:upper:]' '[:lower:]') in
  *debug*) echo 'BOLT buildroot absolute path contains debug' >&2; exit 1 ;;
esac
BOLT_BUILD="$PWD"
BOLT_WORK="$PWD/clang-bolt"
BOLT_INSTALL_ROOT="/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64"
BOLT_PROFILE_SOURCE="/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-v2.fdata.xz"
export BOLT_BUILD BOLT_WORK BOLT_INSTALL_ROOT BOLT_PROFILE_SOURCE
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
    # The step transcript remains available in memory if its log cannot be written.
    printf '%s\n' "$bolt_output" | python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py disk-diagnose "$bolt_stage" /dev/stdin || true
    exit 1
  fi
}
bolt_step() {
  bolt_stage=$1
  shift
  bolt_checked "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py run-step "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" -- "$@"
}
bolt_capture() {
  bolt_stage=$1
  bolt_output=$2
  shift 2
  bolt_checked "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py run-step "$bolt_stage" "$BOLT_WORK/$bolt_stage.log" --output "$bolt_output" -- "$@"
}
# Observability only: sizes vary with this build, so no disk admission budget.
python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py disk-report begin
bolt_step ordinary-install cmake -DCMAKE_INSTALL_PREFIX=/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr -P cmake_install.cmake
echo "BOLT_BUILDROOT_OK /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64" || bolt_fail buildroot-output -
bolt_step preflight python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py preflight
bolt_step certified python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py certified
if [ -r /proc/self/stat ]; then echo BOLT_PROC_OK; else echo BOLT_PROC_MISSING; fi
# One relink: emit-relocs, then LLVM strip-debug, BOLT and full strip.
# The package build owns its original ThinLTO cache; do not duplicate it.
# File-list baseline is the actual ordinary CMake install, not a name whitelist.
bolt_step snapshot python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py snapshot "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64" "$BOLT_WORK/install-before.json"
bolt_step manifest-copy cp install_manifest.txt "$BOLT_WORK/install-manifest-before.txt"
bolt_step ordinary-copy cp -p bin/clang-22 "$BOLT_WORK/ordinary-clang-22"
bolt_capture link-command "$BOLT_WORK/link.original" ninja -t commands -s bin/clang-22
bolt_step unpack python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py unpack /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-v2.fdata.xz "$BOLT_WORK/profile.fdata"
bolt_step configure cmake -S ../llvm -B .   '-DLLVM_ENABLE_PROJECTS=clang;lldb;clang-tools-extra;lld;compiler-rt;openmp;bolt'   -DBOLT_BUILD_TOOLS=OFF -DBOLT_ENABLE_RUNTIME=OFF   -DBOLT_INCLUDE_TESTS=OFF -DBOLT_TARGETS_TO_BUILD=X86
# Only certified BOLT tasks and the paired configure-refreshed TF anchor.
echo BOLT_TOOL_DRY_RUN_BEGIN || bolt_fail dry-run-output -
LC_ALL=C NINJA_STATUS='[%f/%t] ' bolt_capture tool-dry-run "$BOLT_WORK/tool-dry-run.txt" ninja -n llvm-bolt
echo BOLT_TOOL_DRY_RUN_END || bolt_fail dry-run-output -
bolt_capture tool-plan "$BOLT_WORK/tool-plan.json" python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py tool-plan "$BOLT_WORK/tool-dry-run.txt"
bolt_step tool-prepare python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py tool-prepare "$PWD" "$BOLT_WORK/tool-plan.json" "$BOLT_WORK/tool-before.json"
LC_ALL=C NINJA_STATUS='[%f/%t] ' bolt_checked tool-build "$BOLT_WORK/tool-build.txt" python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py run-step tool-build "$BOLT_WORK/tool-build.txt" --success-marker BOLT_NINJA_EXIT_0 -- ninja -j 1 llvm-bolt
bolt_step tool-verify python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py tool-verify "$PWD" "$BOLT_WORK/tool-plan.json" "$BOLT_WORK/tool-build.txt"   "$BOLT_WORK/tool-before.json" "$BOLT_WORK/tool-build-verification.json"
python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py disk-report tool-built
bolt_step pipeline python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py pipeline "$PWD" "$BOLT_WORK" "$PWD/bin/llvm-bolt"
echo BOLT_PIPELINE_PASS || bolt_fail pipeline-output -
python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py disk-report pipeline
# BOLT configuration/build/rewrite must not change the ordinary installation.
# Do not reinstall: that would add BOLT libraries, unregistered aliases and exports.
bolt_step compare-root python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py compare-root "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64" "$BOLT_WORK/install-before.json"   "$BOLT_WORK/install-after-pipeline.json"
echo BOLT_COMPARE_ROOT_PASS || bolt_fail compare-root-output -
# Any subsequent buildroot mutation (including native archive conversion) must follow this gate.
bolt_step install-write-1 ln -sf /usr/bin/clang++ /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/clang++-22

bolt_step install-write-2 ln -sf clang /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/x86_64-pc-linux-gnu-clang
bolt_step install-write-3 ln -sf clang++ /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/x86_64-pc-linux-gnu-clang++
# Use host triple and resource dir by default via <lang>.cfg
bolt_step clang-config /bin/sh -c 'cat >> "$1"' sh /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64//usr/bin/clang.cfg << EOF
-target x86_64-pc-linux-gnu
-resource-dir /usr/lib64/clang/22
EOF
bolt_step install-write-4 ln -sf clang.cfg /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64//usr/bin/clang++.cfg

# copy lldb for sdk
bolt_step install-write-5 mkdir -p /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/bin
bolt_step install-write-6 mkdir -p /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/lib64

bolt_step install-write-7 mv /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/lldb /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/bin
bolt_step install-write-8 mv /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/lldb-argdumper /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/bin
bolt_step install-write-9 mv /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/lldb-server /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/bin

bolt_step install-write-10 ln -sf /home/owner/share/tmp/sdk_tools/lldb/bin/lldb /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/

bolt_step install-write-11 cp -P /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib64/liblldb.so* /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/lib64/

# Install the clang python bits
bolt_step install-write-12 mkdir -p /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64%{python3_sitelib}
bolt_step install-write-13 cp -a ../clang/bindings/python/clang /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64%{python3_sitelib}/

bolt_step install-write-14 rm -rf /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib64/debug/*
bolt_step install-write-15 rm -rf /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib/libear/*
bolt_step install-write-16 rm -rf /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib/libscanbuild/*

# Run after compilation has finished; these workers do not overlap build jobs.
# Preserve the standard RPM post-processing, including archive strip -g.
bolt_step install-write-17 rm -rf "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD/llvm-22.1.8/build/native-archive-conversion"
bolt_step install-write-18 python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/llvm-static-archives-native.py --root "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64" \
    --build "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD/llvm-22.1.8/build" \
    --evidence "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD/llvm-22.1.8/build/native-archive-conversion" \
    --arch x86_64 \
    --compiler "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD/llvm-22.1.8/build/bin/clang-22" \
    --disassembler "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD/llvm-22.1.8/build/bin/llvm-dis" \
    --nm "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD/llvm-22.1.8/build/bin/llvm-nm" \
    --jobs 4 --address-space-bytes 4294967296 || exit 1

# Candidate is fully stripped before the one unchanged platform post-processing chain.
# Capture in memory: a full work filesystem must not break logging after commit.
if BOLT_INSTALL_OUTPUT=$(python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py install "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64" "$BOLT_WORK/clang.candidate" \
  "$BOLT_WORK/install-state.json" "$BOLT_WORK/identity.json" 2>&1); then
  printf '%s\n' "$BOLT_INSTALL_OUTPUT" || bolt_fail install-output -
else
  printf '%s\n' "$BOLT_INSTALL_OUTPUT" || true
  printf '%s\n' "$BOLT_INSTALL_OUTPUT" | python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py disk-diagnose install /dev/stdin || true
  exit 1
fi


    bolt_checked platform-post "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD/llvm-22.1.8/build/clang-bolt/platform-post.log" python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py run-step platform-post "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD/llvm-22.1.8/build/clang-bolt/platform-post.log" -- /bin/sh -e <<'BOLT_PLATFORM_POST' 
    
    
    
    
    /usr/lib/rpm/brp-compress /usr 
    /usr/lib/rpm/brp-elfperms 
    /usr/lib/rpm/brp-strip /usr/bin/strip 
    /usr/lib/rpm/brp-strip-static-archive /usr/bin/strip 
    /usr/lib/rpm/brp-strip-comment-note /usr/bin/strip /usr/bin/objdump 
    /usr/lib/rpm/brp-remove-la-files 

 
BOLT_PLATFORM_POST 
    bolt_checked post "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD/llvm-22.1.8/build/clang-bolt/post.log" python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py run-step post "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD/llvm-22.1.8/build/clang-bolt/post.log" -- python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py post "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64" "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD/llvm-22.1.8/build/clang-bolt/install-state.json" "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD/llvm-22.1.8/build/clang-bolt/ordinary-clang-22" "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILD/llvm-22.1.8/build/clang-bolt/post-gate" --resource-dir "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-disk-diagnostics/host-capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib64/clang/22" 
    echo BOLT_POST_GATE_PASS || exit 1 
    python3 -B /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py disk-report post