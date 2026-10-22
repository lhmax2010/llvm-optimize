#!/bin/sh

  RPM_SOURCE_DIR="/home/abuild/rpmbuild/SOURCES"
  RPM_BUILD_DIR="/home/abuild/rpmbuild/BUILD"
  RPM_OPT_FLAGS="-Os -fstack-protector -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument -momit-leaf-frame-pointer  -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables -fno-omit-frame-pointer -g"
  RPM_ARCH="x86_64"
  RPM_OS="linux"
  export RPM_SOURCE_DIR RPM_BUILD_DIR RPM_OPT_FLAGS RPM_ARCH RPM_OS
  RPM_DOC_DIR="/usr/share/doc/packages"
  export RPM_DOC_DIR
  RPM_PACKAGE_NAME="llvm"
  RPM_PACKAGE_VERSION="22.1.8"
  RPM_PACKAGE_RELEASE="1"
  export RPM_PACKAGE_NAME RPM_PACKAGE_VERSION RPM_PACKAGE_RELEASE
  LANG=C
  export LANG
  unset CDPATH DISPLAY ||:
  RPM_BUILD_ROOT="/home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64"
  export RPM_BUILD_ROOT
  
  PKG_CONFIG_PATH="${PKG_CONFIG_PATH}:/usr/lib64/pkgconfig:/usr/share/pkgconfig"
  export PKG_CONFIG_PATH
  
  set -x
  umask 022
  cd "/home/abuild/rpmbuild/BUILD"
cd '/home/abuild/rpmbuild/BUILD'
rm -rf 'llvm-22.1.8'
/bin/gzip -dc '/home/abuild/rpmbuild/SOURCES/llvm-22.1.8.tar.gz' | /bin/tar -xof - 
STATUS=$?
if [ $STATUS -ne 0 ]; then
  exit $STATUS
fi
cd 'llvm-22.1.8'
/bin/chmod -Rf a+rX,u+w,g-w,o-w .
# 0001-Add-support-for-Tizen-toolchain-vendor.patch
echo "Patch #0 (0001-Add-support-for-Tizen-toolchain-vendor.patch):"
/bin/patch --no-backup-if-mismatch -p1  --fuzz=2 < /home/abuild/rpmbuild/SOURCES/0001-Add-support-for-Tizen-toolchain-vendor.patch

# 0002-Link-libclang_rt.asan.so-against-libatomic-when-nece.patch
echo "Patch #1 (0002-Link-libclang_rt.asan.so-against-libatomic-when-nece.patch):"
/bin/patch --no-backup-if-mismatch -p1  --fuzz=2 < /home/abuild/rpmbuild/SOURCES/0002-Link-libclang_rt.asan.so-against-libatomic-when-nece.patch

# 0003-Fix-armv7l-build-when-compiler-is-clang.patch
echo "Patch #2 (0003-Fix-armv7l-build-when-compiler-is-clang.patch):"
/bin/patch --no-backup-if-mismatch -p1  --fuzz=2 < /home/abuild/rpmbuild/SOURCES/0003-Fix-armv7l-build-when-compiler-is-clang.patch

# 0004-clang-add-support-for-LLVM-gold-plugin-in-case-of-ac.patch
echo "Patch #3 (0004-clang-add-support-for-LLVM-gold-plugin-in-case-of-ac.patch):"
/bin/patch --no-backup-if-mismatch -p1  --fuzz=2 < /home/abuild/rpmbuild/SOURCES/0004-clang-add-support-for-LLVM-gold-plugin-in-case-of-ac.patch

# 0005-Merge-MLGO-AOT-compilation-support-and-optimization-.patch
echo "Patch #4 (0005-Merge-MLGO-AOT-compilation-support-and-optimization-.patch):"
/bin/patch --no-backup-if-mismatch -p1  --fuzz=2 < /home/abuild/rpmbuild/SOURCES/0005-Merge-MLGO-AOT-compilation-support-and-optimization-.patch

# 0006-libcxxabi-declare-__gnu_unwind_frame-in-cxa_personal.patch
echo "Patch #5 (0006-libcxxabi-declare-__gnu_unwind_frame-in-cxa_personal.patch):"
/bin/patch --no-backup-if-mismatch -p1  --fuzz=2 < /home/abuild/rpmbuild/SOURCES/0006-libcxxabi-declare-__gnu_unwind_frame-in-cxa_personal.patch

# 0007-libcxx-backport-EH-ABI-forced-unwind-handling.patch
echo "Patch #6 (0007-libcxx-backport-EH-ABI-forced-unwind-handling.patch):"
/bin/patch --no-backup-if-mismatch -p1  --fuzz=2 < /home/abuild/rpmbuild/SOURCES/0007-libcxx-backport-EH-ABI-forced-unwind-handling.patch

mkdir -p mlgo_verify_assets
tar -C mlgo_verify_assets -xzf /home/abuild/rpmbuild/SOURCES/mlgo_x86_model.tar.gz

exit $?