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

/bin/rm -rf "$RPM_BUILD_ROOT"
/bin/mkdir -p "$RPM_BUILD_ROOT"

cd 'llvm-22.1.8'
export AR=llvm-ar RANLIB=llvm-ranlib;
export CC=x86_64-tizen-linux-gnu-clang CXX=x86_64-tizen-linux-gnu-clang++;

cd build
cmake -DCMAKE_INSTALL_PREFIX=/home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/usr -P cmake_install.cmake
ln -sf /usr/bin/clang++ /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/clang++-22

ln -sf clang /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/x86_64-tizen-linux-gnu-clang
ln -sf clang++ /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/x86_64-tizen-linux-gnu-clang++
# Use host triple and resource dir by default via <lang>.cfg
cat >> /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64//usr/bin/clang.cfg << EOF
-target x86_64-tizen-linux-gnu
-resource-dir /usr/lib64/clang/22
EOF
ln -sf clang.cfg /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64//usr/bin/clang++.cfg

# copy lldb for sdk
mkdir -p /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/bin
mkdir -p /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/lib64

mv /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/lldb /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/bin
mv /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/lldb-argdumper /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/bin
mv /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/lldb-server /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/bin

ln -sf /home/owner/share/tmp/sdk_tools/lldb/bin/lldb /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/usr/bin/

cp -P /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib64/liblldb.so* /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/home/owner/share/tmp/sdk_tools/lldb/lib64/

# Install the clang python bits
mkdir -p /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib/python3.14/site-packages
cp -a ../clang/bindings/python/clang /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib/python3.14/site-packages/

rm -rf /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib64/debug/*
rm -rf /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib/libear/*
rm -rf /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64/usr/lib/libscanbuild/*

# Run after compilation has finished; these workers do not overlap build jobs.
# Preserve the standard RPM post-processing, including archive strip -g.
rm -rf "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/native-archive-conversion"
python3 /home/abuild/rpmbuild/SOURCES/llvm-static-archives-native.py --root "/home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64" \
    --build "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build" \
    --evidence "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/native-archive-conversion" \
    --arch x86_64 \
    --compiler "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/clang-22" \
    --disassembler "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-dis" \
    --nm "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-nm" \
    --jobs 4 --address-space-bytes 4294967296 || exit 1


    
    /usr/lib/rpm/find-debuginfo.sh \
    -j8 \
     \
     \
     \
     \
    --build-id-seed "22.1.8-1" \
     \
    --unique-debug-src-base "llvm-22.1.8-1.x86_64" \
     \
     \
     \
     \
    -S debugsourcefiles.list \
    "/home/abuild/rpmbuild/BUILD/llvm-22.1.8"\
    
   cp /usr/lib/rpm/debug.manifest /home/abuild/rpmbuild/BUILD/llvm-22.1.8/llvm-debuginfo.manifest 
   cp /usr/lib/rpm/debug.manifest /home/abuild/rpmbuild/BUILD/llvm-22.1.8/llvm-debugsource.manifest 
 

    /usr/lib/rpm/check-buildroot
    
    /usr/lib/rpm//brp-compress 
    
     
    /usr/lib/rpm/brp-strip-static-archive /bin/strip 
#    /usr/lib/rpm/brp-strip-comment-note /bin/strip /bin/objdump 

    /usr/lib/rpm/brp-python-hardlink 
    /usr/lib/rpm/tizen/find-docs.sh /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64 

    
    /usr/lib/rpm/tizen/find-isufiles.sh /home/abuild/rpmbuild/BUILD/llvm-22.1.8/isu.list 

    
    /etc/hal/rootstrap/hal-rootstrap-checker.sh /home/abuild/rpmbuild/SOURCES /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64 x86_64 

    
    /etc/app-rootstrap/app-rootstrap-checker.sh /home/abuild/rpmbuild/SOURCES /home/abuild/rpmbuild/BUILDROOT/llvm-22.1.8-1.x86_64 x86_64 

