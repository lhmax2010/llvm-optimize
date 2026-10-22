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

  CFLAGS="${CFLAGS:--Os -fstack-protector -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument -momit-leaf-frame-pointer  -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables -fno-omit-frame-pointer -g}" ; export CFLAGS ; 
  CXXFLAGS="${CXXFLAGS:--Os -fstack-protector -Wno-unused-command-line-argument -Wno-error=unused-but-set-variable -Wno-error=unused-command-line-argument -momit-leaf-frame-pointer  -g2 -gdwarf-4 -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -Wformat -Wformat-security -fmessage-length=0 -frecord-gcc-switches -fdiagnostics-color=never -m64 -march=nehalem -msse4.2 -mfpmath=sse -fasynchronous-unwind-tables -fno-omit-frame-pointer -g}" ; export CXXFLAGS ; 
  LDFLAGS="${LDFLAGS:--Wl,-z,relro,--as-needed}" ; export LDFLAGS;

cd 'llvm-22.1.8'
ref=/usr/lib/rpm
mints=0
case $(uname -m) in
    aarch64) mints=20120610;;
    ppc64le) mints=20130610;;
    riscv64) mints=20160911;;
esac
for s in guess sub; do
    for c in $(find -maxdepth 8 -name "config.$s"); do
         grep -q config-patches@ $c || continue
         timestamp=$(sed -n "/^timestamp=/{s///;s/[-'\"]//g;p;q;}" $c | tr -d '')
         test -n "$timestamp" || timestamp=0
         test $timestamp -ge $mints || install -m 755 $ref/config.$s $c
     done
done

export AR=llvm-ar RANLIB=llvm-ranlib;
export CC=x86_64-tizen-linux-gnu-clang CXX=x86_64-tizen-linux-gnu-clang++;


cp /home/abuild/rpmbuild/SOURCES/llvm.manifest .



# Strip pre-existing optimization flags and remove performance-harming flags, then force -O3 + ThinLTO
OPTFLAGS_CFLAGS=$(echo "$CFLAGS" | sed \
    -e 's/\-O[0-9sz]//g' \
    -e 's/\-Ofast//g' \
    -e 's/\-fstack-protector-strong//g' \
    -e 's/\-fstack-protector-all//g' \
    -e 's/\-fstack-protector//g' \
    -e 's/\-fno-inline-functions//g' \
    -e 's/\-fno-omit-frame-pointer//g' \
    -e 's/\-momit-leaf-frame-pointer//g')
OPTFLAGS_CXXFLAGS=$(echo "$CXXFLAGS" | sed \
    -e 's/\-O[0-9sz]//g' \
    -e 's/\-Ofast//g' \
    -e 's/\-fstack-protector-strong//g' \
    -e 's/\-fstack-protector-all//g' \
    -e 's/\-fstack-protector//g' \
    -e 's/\-fno-inline-functions//g' \
    -e 's/\-fno-omit-frame-pointer//g' \
    -e 's/\-momit-leaf-frame-pointer//g')
export CFLAGS="$OPTFLAGS_CFLAGS -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument"
export CXXFLAGS="$OPTFLAGS_CXXFLAGS -O3 -flto=thin -fomit-frame-pointer -Wno-unused-command-line-argument"

# Set up MLGO AOT model paths from bundled verify assets
MLGO_AOT_DIR="$PWD/mlgo_verify_assets"
MLGO_BUILD_DIR="$PWD/build"
MLGO_RUNTIME_OBJECTS="${MLGO_AOT_DIR}/xla_runtime_objects/xla_compiled_cpu_function.cc.o;${MLGO_AOT_DIR}/xla_runtime_objects/cpu_function_runtime.cc.o;${MLGO_AOT_DIR}/xla_runtime_objects/custom_call_status.cc.o;${MLGO_AOT_DIR}/xla_runtime_objects/executable_run_options.cc.o;${MLGO_AOT_DIR}/xla_runtime_objects/runtime_single_threaded_matmul_f32.cc.o"
MLGO_REQUIRED_RUNTIME_OBJECTS="xla_compiled_cpu_function.cc.o cpu_function_runtime.cc.o custom_call_status.cc.o executable_run_options.cc.o runtime_single_threaded_matmul_f32.cc.o"

mkdir -p build
cd build
cmake \
    -G Ninja \
    -DTIZEN=1 \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DLLVM_HOST_TRIPLE=x86_64-tizen-linux-gnu \
    -DLLVM_DEFAULT_TARGET_TRIPLE=x86_64-tizen-linux-gnu \
    -DLLVM_TARGET_TRIPLE_ENV=x86_64-tizen-linux-gnu \
    -DCMAKE_ASM_FLAGS="$CFLAGS" \
    -DCMAKE_C_FLAGS="$CFLAGS" \
    -DCMAKE_CXX_FLAGS="$CXXFLAGS" \
    -DCMAKE_SHARED_LINKER_FLAGS="-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections" \
    -DCMAKE_EXE_LINKER_FLAGS="-fuse-ld=lld -flto=thin -ffunction-sections -fdata-sections -Wl,--gc-sections" \
    -DLLVM_USE_LINKER=lld \
    -DLLVM_ENABLE_LTO=Thin \
    -DCMAKE_RANLIB=/usr/bin/llvm-ranlib \
    -DCMAKE_AR=/usr/bin/llvm-ar \
    -DLLVM_ENABLE_ASSERTIONS=No \
    -DLLVM_ENABLE_RTTI=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_TARGETS_TO_BUILD='X86;ARM;AArch64;BPF' \
    -DCLANG_ENABLE_ARCMT=OFF \
    -DLLVM_BUILD_LLVM_DYLIB=ON \
    -DCLANG_BUILD_CLANG_DYLIB=ON \
    -DLLVM_LINK_LLVM_DYLIB=OFF \
    -DCLANG_LINK_CLANG_DYLIB=OFF \
    -DLLVM_ENABLE_PROJECTS="clang;lldb;clang-tools-extra;lld;compiler-rt;openmp" \
    -DLLVM_ENABLE_PER_TARGET_RUNTIME_DIR=OFF \
    -DLLVM_BUILD_EXAMPLES=OFF \
    -DLLVM_INCLUDE_EXAMPLES=OFF \
    -DLLVM_BUILD_TESTS=OFF \
    -DLLVM_INCLUDE_TESTS=OFF \
    -DLLVM_ENABLE_DOXYGEN=OFF \
    -DLLVM_BUILD_DOCS=OFF \
    -DLLVM_INCLUDE_DOCS=OFF \
    -DLLVM_OPTIMIZED_TABLEGEN=ON \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DLLVM_LIBDIR_SUFFIX=`echo lib64 | sed s/lib//g` \
    -DCLANG_RESOURCE_DIR="../lib64/clang/22" \
    -DLLVM_BINUTILS_INCDIR=/usr/include \
    -DLLVM_PARALLEL_COMPILE_JOBS=6 \
    -DLLVM_PARALLEL_LINK_JOBS=2 \
    -DTENSORFLOW_AOT_PATH="${MLGO_AOT_DIR}/mlgo_sysroot" \
    -DLLVM_MLGO_EXPORT_TF_XLA_RUNTIME=OFF \
    -DLLVM_MLGO_EMBED_TF_XLA_RUNTIME_OBJECTS="${MLGO_RUNTIME_OBJECTS}" \
    -DLLVM_OVERRIDE_MODEL_HEADER_INLINERSIZEMODEL="${MLGO_AOT_DIR}/InlinerSizeModel.h" \
    -DLLVM_OVERRIDE_MODEL_OBJECT_INLINERSIZEMODEL="${MLGO_AOT_DIR}/InlinerSizeModel.o" \
    -DLLVM_OVERRIDE_MODEL_HEADER_REGALLOCEVICTMODEL="${MLGO_AOT_DIR}/RegAllocEvictModel.h" \
    -DLLVM_OVERRIDE_MODEL_OBJECT_REGALLOCEVICTMODEL="${MLGO_AOT_DIR}/RegAllocEvictModel.o" \
    ../llvm


# Full build using ninja (already in build/ directory after cd build)
ninja -d keeprsp -j 6 || exit 1


exit $?