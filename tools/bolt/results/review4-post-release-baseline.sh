#!/bin/sh


  RPM_SOURCE_DIR="/home/abuild/bolt-work/bolt-v4-20261015-review4"
  RPM_BUILD_DIR="/home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILD"
  RPM_OPT_FLAGS="-O2 -g -m64 -fmessage-length=0 -Wp,-D_FORTIFY_SOURCE=2 -fstack-protector -funwind-tables -fasynchronous-unwind-tables"
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
  RPM_BUILD_ROOT="/home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT"
  export RPM_BUILD_ROOT
  
  PKG_CONFIG_PATH="${PKG_CONFIG_PATH}:/usr/lib64/pkgconfig:/usr/share/pkgconfig"
  export PKG_CONFIG_PATH
  
  set -x
  umask 022
  cd "/home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILD"

/bin/rm -rf "$RPM_BUILD_ROOT"
/bin/mkdir -p "$RPM_BUILD_ROOT"

cd 'llvm-22.1.8'
export AR=llvm-ar RANLIB=llvm-ranlib;
export CC=x86_64-tizen-linux-gnu-clang CXX=x86_64-tizen-linux-gnu-clang++;

cd build
cmake -DCMAKE_INSTALL_PREFIX=/home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/usr -P cmake_install.cmake
ln -sf /usr/bin/clang++ /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/usr/bin/clang++-22

ln -sf clang /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/usr/bin/x86_64-tizen-linux-gnu-clang
ln -sf clang++ /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/usr/bin/x86_64-tizen-linux-gnu-clang++
# Use host triple and resource dir by default via <lang>.cfg
cat >> /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT//usr/bin/clang.cfg << EOF
-target x86_64-tizen-linux-gnu
-resource-dir /usr/lib64/clang/22
EOF
ln -sf clang.cfg /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT//usr/bin/clang++.cfg

# copy lldb for sdk
mkdir -p /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/home/owner/share/tmp/sdk_tools/lldb/bin
mkdir -p /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/home/owner/share/tmp/sdk_tools/lldb/lib64

mv /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/usr/bin/lldb /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/home/owner/share/tmp/sdk_tools/lldb/bin
mv /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/usr/bin/lldb-argdumper /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/home/owner/share/tmp/sdk_tools/lldb/bin
mv /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/usr/bin/lldb-server /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/home/owner/share/tmp/sdk_tools/lldb/bin

ln -sf /home/owner/share/tmp/sdk_tools/lldb/bin/lldb /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/usr/bin/

cp -P /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/usr/lib64/liblldb.so* /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/home/owner/share/tmp/sdk_tools/lldb/lib64/

# Install the clang python bits
mkdir -p /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/usr/lib/python3.14/site-packages
cp -a ../clang/bindings/python/clang /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/usr/lib/python3.14/site-packages/

rm -rf /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/usr/lib64/debug/*
rm -rf /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/usr/lib/libear/*
rm -rf /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT/usr/lib/libscanbuild/*

# Run after compilation has finished; these workers do not overlap build jobs.
# Preserve the standard RPM post-processing, including archive strip -g.
rm -rf "/home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILD/llvm-22.1.8/build/native-archive-conversion"
python3 /home/abuild/bolt-work/bolt-v4-20261015-review4/llvm-static-archives-native.py --root "/home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT" \
    --build "/home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILD/llvm-22.1.8/build" \
    --evidence "/home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILD/llvm-22.1.8/build/native-archive-conversion" \
    --arch x86_64 \
    --compiler "/home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILD/llvm-22.1.8/build/bin/clang-22" \
    --disassembler "/home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILD/llvm-22.1.8/build/bin/llvm-dis" \
    --nm "/home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILD/llvm-22.1.8/build/bin/llvm-nm" \
    --jobs 4 --address-space-bytes 4294967296 || exit 1


    
    /usr/lib/rpm/check-buildroot
    
    /usr/lib/rpm//brp-compress 
    
    /usr/lib/rpm/brp-strip /bin/strip 
    /usr/lib/rpm/brp-strip-static-archive /bin/strip 
#    /usr/lib/rpm/brp-strip-comment-note /bin/strip /bin/objdump 

    /usr/lib/rpm/brp-python-hardlink 
    /usr/lib/rpm/tizen/find-docs.sh /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT 

    
    /usr/lib/rpm/tizen/find-isufiles.sh /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILD/llvm-22.1.8/isu.list 

    
    /etc/hal/rootstrap/hal-rootstrap-checker.sh /home/abuild/bolt-work/bolt-v4-20261015-review4 /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT x86_64 

    
    /etc/app-rootstrap/app-rootstrap-checker.sh /home/abuild/bolt-work/bolt-v4-20261015-review4 /home/abuild/bolt-work/bolt-v4-20261015-review4/post-capture/BUILDROOT x86_64 

