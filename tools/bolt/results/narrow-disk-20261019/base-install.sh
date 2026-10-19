#!/bin/sh

  
  RPM_SOURCE_DIR="/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging"
  RPM_BUILD_DIR="/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILD"
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
  RPM_BUILD_ROOT="/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64"
  export RPM_BUILD_ROOT
  
  PKG_CONFIG_PATH="${PKG_CONFIG_PATH}:/usr/lib64/pkgconfig:/usr/share/pkgconfig"
  export PKG_CONFIG_PATH 
  set -x
  umask 022
  cd "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILD"
    /bin/rm -rf "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64"
    /bin/mkdir -p "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT"
    /bin/mkdir "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64"

cd 'llvm-22.1.8'
cd build
cmake -DCMAKE_INSTALL_PREFIX=/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr -P cmake_install.cmake

# Reject debug-named buildroots before any BOLT action.
case $(printf '%s' '/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64' | LC_ALL=C tr '[:upper:]' '[:lower:]') in
  *debug*) echo 'BOLT buildroot absolute path contains debug' >&2; exit 1 ;;
esac
echo "BOLT_BUILDROOT_OK /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64"
python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py preflight || exit 1
python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py certified || exit 1
if [ -r /proc/self/stat ]; then echo BOLT_PROC_OK; else echo BOLT_PROC_MISSING; fi
# One relink: emit-relocs, then LLVM strip-debug, BOLT and full strip.
# The handed-off build owns its original ThinLTO cache; do not duplicate it.
# Default 16 GiB BOLT-stage write budget must leave 30 GiB on this filesystem.
BOLT_WORK="$PWD/clang-bolt"
mkdir -p "$BOLT_WORK" || exit 1
python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py disk-preflight "$BOLT_WORK" 17179869184 || exit 1
# File-list baseline is the actual ordinary CMake install, not a name whitelist.
python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py snapshot "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64" "$BOLT_WORK/install-before.json" || exit 1
cp install_manifest.txt "$BOLT_WORK/install-manifest-before.txt" || exit 1
cp -p bin/clang-22 "$BOLT_WORK/ordinary-clang-22" || exit 1
ninja -t commands -s bin/clang-22 > "$BOLT_WORK/link.original" || exit 1
python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py unpack /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-v2.fdata.xz "$BOLT_WORK/profile.fdata" || exit 1
cmake -S ../llvm -B . \
  '-DLLVM_ENABLE_PROJECTS=clang;lldb;clang-tools-extra;lld;compiler-rt;openmp;bolt' \
  -DBOLT_BUILD_TOOLS=OFF -DBOLT_ENABLE_RUNTIME=OFF \
  -DBOLT_INCLUDE_TESTS=OFF -DBOLT_TARGETS_TO_BUILD=X86 || exit 1
# Only certified BOLT tasks and the paired configure-refreshed TF anchor.
if LC_ALL=C NINJA_STATUS='[%f/%t] ' ninja -n llvm-bolt > "$BOLT_WORK/tool-dry-run.txt" 2>&1; then
  echo BOLT_TOOL_DRY_RUN_BEGIN
  cat "$BOLT_WORK/tool-dry-run.txt"
  echo BOLT_TOOL_DRY_RUN_END
else
  cat "$BOLT_WORK/tool-dry-run.txt"
  exit 1
fi
python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py tool-plan "$BOLT_WORK/tool-dry-run.txt" > "$BOLT_WORK/tool-plan.json" || exit 1
cat "$BOLT_WORK/tool-plan.json"
python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py tool-prepare "$PWD" "$BOLT_WORK/tool-plan.json" "$BOLT_WORK/tool-before.json" || exit 1
python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py disk-preflight "$PWD" 17179869184 || exit 1
if LC_ALL=C NINJA_STATUS='[%f/%t] ' ninja -j 1 llvm-bolt > "$BOLT_WORK/tool-build.txt" 2>&1; then
  echo BOLT_NINJA_EXIT_0 >> "$BOLT_WORK/tool-build.txt"
  cat "$BOLT_WORK/tool-build.txt"
else
  cat "$BOLT_WORK/tool-build.txt"
  exit 1
fi
python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py tool-verify "$PWD" "$BOLT_WORK/tool-plan.json" "$BOLT_WORK/tool-build.txt" \
  "$BOLT_WORK/tool-before.json" "$BOLT_WORK/tool-build-verification.json" || exit 1
cat "$BOLT_WORK/tool-build-verification.json"
python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py pipeline "$PWD" "$BOLT_WORK" "$PWD/bin/llvm-bolt" || exit 1
echo BOLT_PIPELINE_PASS
# BOLT configuration/build/rewrite must not change the ordinary installation.
# Do not reinstall: that would add BOLT libraries, unregistered aliases and exports.
python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py compare-root "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64" "$BOLT_WORK/install-before.json" \
  "$BOLT_WORK/install-after-pipeline.json" || exit 1
echo BOLT_COMPARE_ROOT_PASS
# Any subsequent buildroot mutation (including native archive conversion) must follow this gate.
ln -sf /usr/bin/clang++ /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/clang++-22

ln -sf clang /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/x86_64-pc-linux-gnu-clang
ln -sf clang++ /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/x86_64-pc-linux-gnu-clang++
# Use host triple and resource dir by default via <lang>.cfg
cat >> /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64//usr/bin/clang.cfg << EOF
-target x86_64-pc-linux-gnu
-resource-dir /usr/lib64/clang/22
EOF
ln -sf clang.cfg /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64//usr/bin/clang++.cfg

# copy lldb for sdk
mkdir -p /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/bin
mkdir -p /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/lib64

mv /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/lldb /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/bin
mv /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/lldb-argdumper /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/bin
mv /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/lldb-server /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/bin

ln -sf /home/owner/share/tmp/sdk_tools/lldb/bin/lldb /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/

cp -P /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib64/liblldb.so* /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/lib64/

# Install the clang python bits
mkdir -p /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64%{python3_sitelib}
cp -a ../clang/bindings/python/clang /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64%{python3_sitelib}/

rm -rf /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib64/debug/*
rm -rf /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib/libear/*
rm -rf /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib/libscanbuild/*

# Run after compilation has finished; these workers do not overlap build jobs.
# Preserve the standard RPM post-processing, including archive strip -g.
rm -rf "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILD/llvm-22.1.8/build/native-archive-conversion"
python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/llvm-static-archives-native.py --root "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64" \
    --build "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILD/llvm-22.1.8/build" \
    --evidence "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILD/llvm-22.1.8/build/native-archive-conversion" \
    --arch x86_64 \
    --compiler "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILD/llvm-22.1.8/build/bin/clang-22" \
    --disassembler "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILD/llvm-22.1.8/build/bin/llvm-dis" \
    --nm "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILD/llvm-22.1.8/build/bin/llvm-nm" \
    --jobs 4 --address-space-bytes 4294967296 || exit 1

# Candidate is fully stripped before the one unchanged platform post-processing chain.
python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py install "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64" "$BOLT_WORK/clang.candidate" \
  "$BOLT_WORK/install-state.json" "$BOLT_WORK/identity.json" || exit 1


    
    
    
    
    /usr/lib/rpm/brp-compress /usr 
    /usr/lib/rpm/brp-elfperms 
    /usr/lib/rpm/brp-strip /usr/bin/strip 
    /usr/lib/rpm/brp-strip-static-archive /usr/bin/strip 
    /usr/lib/rpm/brp-strip-comment-note /usr/bin/strip /usr/bin/objdump 
    /usr/lib/rpm/brp-remove-la-files 

 
    python3 /home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261013/v41/llvm-source/packaging/clang-bolt-helper.py post "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64" "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILD/llvm-22.1.8/build/clang-bolt/install-state.json" "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILD/llvm-22.1.8/build/clang-bolt/ordinary-clang-22" "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILD/llvm-22.1.8/build/clang-bolt/post-gate" --resource-dir "/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261019-narrow-disk/capture/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib64/clang/22" || exit 1 
    echo BOLT_POST_GATE_PASS