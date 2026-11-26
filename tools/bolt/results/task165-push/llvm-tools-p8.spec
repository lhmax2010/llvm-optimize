Name:       llvm-tools-subpkgs
Summary:    Debugging/analysis tool subpackages for the Tizen LLVM toolchain
Version:    22.1.8
Release:    1
License:    NCSA
Group:      Development/Tools
Source0:    llvm-22.1.8.tar.gz
# Package scope: x86_64 and aarch64 build hosts. armv7l and i586 are
# excluded. riscv64 is also excluded, as a packaging scope choice and not
# for lack of upstream BOLT support: it would need its own RISCV target
# branch below and its own validation. Confirm the consumer matrix first.
ExclusiveArch: x86_64 aarch64
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: llvm = %{version}
BuildRequires: llvm-devel = %{version}
# llvm-static-devel: llvm-devel's LLVMExports.cmake validates the static
# imported targets (libLLVM*.a) at configure time; without the archives
# present, find_package(LLVM) aborts before bolt can link the dylib.
BuildRequires: llvm-static-devel = %{version}
# libomp: the exported target "omp" in LLVMExports-release.cmake references
# /usr/lib64/libomp.so; the configure-time existence check aborts without it.
BuildRequires: libomp = %{version}
# zlib-devel, libxml2-devel: the exported LLVM targets reference ZLIB::ZLIB
# and LibXml2::LibXml2 in their link interfaces (bolt standalone build)
BuildRequires: zlib-devel
BuildRequires: libxml2-devel
BuildRequires: clang
BuildRequires: libllvm = %{version}
BuildRequires: compiler-rt

# BOLT targets per build architecture: each must exist in the installed LLVM.
%ifarch x86_64
%global bolt_targets X86;AArch64
%else
%global bolt_targets AArch64
%endif

%description
Standalone subpackages for LLVM debugging and analysis tools:
 - bolt: BOLT post-link binary optimizer, built standalone against the
   installed LLVM toolchain (no full LLVM rebuild required)

The tools below now ship from the llvm and clang packages: llvm-xray, llvm-cov,
llvm-profgen and llvm-profdata from llvm; scan-build and the analyzer libexec
scripts from clang.
Changes to this spec only require
rebuilding this package (minutes), not the multi-hour LLVM build.

%package -n bolt
Summary: BOLT post-link binary optimizer
License: NCSA
# Same LLVM version; rpm also generates the libLLVM.so.22.1(LLVM_22.1)
# dependency. The provider release is intentionally not pinned: this
# package has its own release number, which must not be used for libllvm.
# ABI compatibility across libllvm releases stays a provider policy.
Requires: libllvm = %{version}

%description -n bolt
BOLT is a post-link binary optimizer that reorders code in the final
binary or DSO based on runtime profile data (perf LBR/PT samples, or
sampled instruction addresses without branch records via perf2bolt -ba)
to improve instruction cache and TLB utilization.

%prep
%setup -q -n llvm-22.1.8

# MANDATORY under gbs: gbs builds with _build_create_debug 1, so Tizen's
# patched rpmbuild injects the debuginfo/debugsource package sections
# itself; the standard debug_package macro would add them a second time
# and fail with "package already exists". NOTE: keep percent signs out of
# this comment -- rpmbuild expands macros even in comment lines.
# find-debuginfo.sh still runs from __debug_install_post and moves the
# separated debug files into bolt-debuginfo, named after the bolt
# subpackage; sources go to llvm-tools-subpkgs-debugsource. Compiler
# flags, including the debug options, come from the distribution CFLAGS
# and CXXFLAGS that the build section exports and CMake reads. The
# build-id linker flags in the build section tie each debug file to its
# binary.
%define debug_package %{nil}

%build
# ---- A. BOLT built standalone against the installed toolchain ----
# aarch64: Tizen's RPM optflags carry the GCC-only big.LITTLE tune name
# -mtune=cortex-a57.cortex-a53, which the clang driver rejects with
# "unsupported argument 'cortex-a57.cortex-a53' to option '-mtune='".
# Remap it to the plain core name clang accepts (same workaround the
# llvm and libcxx-runtimes specs apply).
%ifarch aarch64
CFLAGS="$(printf '%%s\n' "$CFLAGS" | sed 's/-mtune=cortex-a57\.cortex-a53/-mtune=cortex-a53/g')"
CXXFLAGS="$(printf '%%s\n' "$CXXFLAGS" | sed 's/-mtune=cortex-a57\.cortex-a53/-mtune=cortex-a53/g')"
export CFLAGS CXXFLAGS
%endif

# Standalone detection: CMAKE_SOURCE_DIR == bolt source dir
# => BOLT_BUILT_STANDALONE=TRUE, find_package(LLVM) finds the installed
# LLVM CMake package under the architecture libdir.
# LLVM_LINK_LLVM_DYLIB=ON is mandatory: BOLT must link libLLVM.so (libllvm);
# llvm-static-devel is installed only because the exported targets are
# validated at configure time.
#
# Require one provider Version-Release for these packages in this build
# root; all of them come from llvm.spec (drop libomp here if it ever gets
# its own source package). This is not a byte-identity check.
test "$(llvm-config --version)" = "%{version}" || exit 1
llvm_evr=""
for p in llvm llvm-devel llvm-static-devel libllvm libomp; do
    e=$(rpm -q --qf '%%{VERSION}-%%{RELEASE}' "$p") || exit 1
    if [ -n "$llvm_evr" ] && [ "$e" != "$llvm_evr" ]; then
        echo "LLVM provider mismatch: $p $e, expected $llvm_evr"
        exit 1
    fi
    llvm_evr=$e
done
echo "LLVM provider Version-Release consistency check passed: $llvm_evr"
mkdir -p bolt-build
cd bolt-build
cmake \
    -G Ninja \
    -S ../bolt \
    -B . \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DLLVM_LIBDIR_SUFFIX=`echo %{_lib} | sed s/lib//g` \
    -DLLVM_ENABLE_RTTI=ON \
    -DLLVM_LINK_LLVM_DYLIB=ON \
    -DCMAKE_EXE_LINKER_FLAGS="$LDFLAGS -Wl,--build-id=sha1" \
    -DCMAKE_SHARED_LINKER_FLAGS="$LDFLAGS -Wl,--build-id=sha1" \
    -DBOLT_INCLUDE_TESTS=OFF \
    -DBOLT_TARGETS_TO_BUILD="%{bolt_targets}" \
    -DLLVM_INCLUDE_TESTS=OFF
# bolt: driver + tools; bolt_rt: runtime archives (ExternalProject) for the
# build architecture.
ninja bolt bolt_rt
# Target registration check, kept in the build section so it also runs
# when the check section is skipped. It does not test a rewrite.
LC_ALL=C ./bin/llvm-bolt --version > bolt-version.txt 2>&1 || { cat bolt-version.txt; exit 1; }
cat bolt-version.txt
grep -Eq '^[[:space:]]*aarch64[[:space:]]+-' bolt-version.txt
%ifarch x86_64
grep -Eq '^[[:space:]]*x86-64[[:space:]]+-' bolt-version.txt
%endif

%install
# ---- A. bolt: install from the standalone build tree ----
cd bolt-build
DESTDIR=%{buildroot} ninja install
# The internal bolt static libs are build artifacts, not shipped content.
rm -f %{buildroot}%{_libdir}/libLLVMBOLT*.a
# perf2bolt and llvm-boltdiff are aliases of llvm-bolt: upstream installs them
# as symlinks (bolt/tools/driver/CMakeLists.txt), and llvm-bolt selects its
# mode from the name it is invoked as. Separate copies also collided on
# build-id in the debuginfo step.
ln -sf llvm-bolt %{buildroot}%{_prefix}/bin/perf2bolt
ln -sf llvm-bolt %{buildroot}%{_prefix}/bin/llvm-boltdiff
# llvm-bat-dump has no install rule; stage it from the build tree.
install -p -m 0755 bin/llvm-bat-dump %{buildroot}%{_prefix}/bin/
cd ..

%files -n bolt
%defattr(-,root,root,-)
%{_prefix}/bin/llvm-bolt
%{_prefix}/bin/perf2bolt
%{_prefix}/bin/llvm-boltdiff
%{_prefix}/bin/llvm-bolt-heatmap
%{_prefix}/bin/llvm-bolt-binary-analysis
%{_prefix}/bin/llvm-bat-dump
%{_prefix}/bin/merge-fdata
%{_libdir}/libbolt_rt_instr.a
%{_libdir}/libbolt_rt_hugify.a
