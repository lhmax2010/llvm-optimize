%{!?dotnet_buildtype: %define dotnet_buildtype Release}
%{!?skiptests: %define skiptests 1}
%{!?skipfxtests: %define skipfxtests 1}
%{!?skipmscorlib: %define skipmscorlib 0}
%{!?skipmanaged: %define skipmanaged 0}
%{!?skipnugetpackage: %define skipnugetpackage 1}

%define dotnet_buildtype_clr %{dotnet_buildtype}
%define dotnet_buildtype_fx %{dotnet_buildtype}
%define dotnet_buildtype_host %{dotnet_buildtype}

%if "%{?dotnet_buildtype}" == "Checked"
    %define dotnet_buildtype_fx Debug
%endif

%define _binaries_in_noarch_packages_terminate_build   0
%define _unpackaged_files_terminate_build 0

%define skipmanagedtools 0

%ifarch %{ix86}
%define skipmanagedtools 1
%endif

%ifarch %{arm} aarch64 %{ix86} x86_64 riscv64
%else
%define skiptests 1
%define skipfxtests 1
%define skipnugetpackage 1
%endif

%define pgo_instrument 0
%define pgo_optimize 0

%define dotnet_version  10.0.10

Name:	    coreclr
Version:	10.0.10
Release:	0
Summary:	Microsoft .NET Runtime with Microsoft .NET foundation class libraries (CoreCLR and CoreFX)
Group:		Development/Languages
License:	MIT
URL:		  http://github.com/dotnet/runtime
Source0: %{name}-%{version}.tar.gz
Source1: %{name}.manifest

BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  libarchive-tools
BuildRequires:  python3
BuildRequires:  python3-xml
# libcoreclr.so
BuildRequires:  pkgconfig(libunwind)
BuildRequires:  pkgconfig(uuid)
# System.Globalization.Native.so
BuildRequires:  libicu-devel
BuildRequires:  tizen-release
# System.Net.Security.Native.so
# System.Net.Http.Native.so
BuildRequires:  krb5-devel
BuildRequires:  libcurl-devel
# No matter what tizen-release package you use in any profile
AutoReq: 0
Requires: glibc
Requires: libgcc
Requires: libstdc++
Requires: libunwind
Requires: libuuid
Requires: coreclr-dbgshim

# Accelerate python, clang
%ifarch armv7l
BuildRequires: python-accel-armv7l-cross-arm
BuildRequires: clang-accel-armv7l-cross-arm
%endif

%ifarch armv7hl
BuildRequires: python-accel-armv7hl-cross-arm
BuildRequires: clang-accel-armv7hl-cross-arm
%endif

%ifarch aarch64
BuildRequires: python-accel-aarch64-cross-aarch64
BuildRequires: clang-accel-aarch64-cross-aarch64
%endif

%ifarch riscv64
BuildRequires: python-accel-riscv64-cross-riscv64
BuildRequires: clang-accel-riscv64-cross-riscv64
%endif

BuildRequires:  cmake
BuildRequires:  llvm >= 3.8
BuildRequires:  llvm-devel >= 3.8
BuildRequires:  clang >= 3.8
BuildRequires:  clang-devel >= 3.8
%ifarch riscv64
%else
# lldb is not available for RISC-V right now
BuildRequires:  lldb >= 3.8
BuildRequires:  lldb-devel >= 3.8
%endif
BuildRequires:  gettext-tools
BuildRequires:  pkgconfig(openssl3)

# C include headers
BuildRequires:  libstdc++-devel
BuildRequires:  pkgconfig(lttng-ust)

BuildRequires:  libatomic
BuildRequires:  gcc-devel-static

%if 0%{skipmscorlib} && 0%{skipmanaged} && 0%{skipmanagedtools}
%else
%ifarch %{arm} aarch64 riscv64
BuildRequires:  patchelf
%endif
%ifarch %{ix86}
BuildRequires:  patchelf
BuildRequires:  glibc-64bit
BuildRequires:  libgcc-64bit
BuildRequires:  libstdc++-64bit
BuildRequires:  libunwind-64bit
BuildRequires:  libuuid-64bit
BuildRequires:  zlib-64bit
BuildRequires:  libopenssl3-64bit
%endif
%endif

%if 0%{pgo_instrument} || 0%{pgo_optimize}
BuildRequires:  binutils-gold
BuildRequires:  compiler-rt
%endif

%description
The CoreCLR repo contains the complete runtime implementation for .NET Core. It includes RyuJIT, the .NET GC, native interop and many other components. It is cross-platform, with multiple OS and CPU ports in progress. The .NET Core foundational libraries, called CoreFX. It includes classes for collections, file systems, console, XML, async and many others.

%package -n coreclr-test
Summary:    Dotnet Core Unit Test
Requires:    coreclr
AutoReqProv: no

%description -n coreclr-test
Unit Test objs

%package -n coreclr-devel
Summary:    Dotnet Core Development package
Requires:   coreclr

%description -n coreclr-devel
Headers and static libraries

%package -n mscorlib
Summary:	Core Library for MS .NET
Requires:	coreclr

%description -n mscorlib
The System.Private.CoreLib.dll for .NET Core Runtime (coreclr)

%if 0%{skipnugetpackage}
%else
%package -n corefx-oob-nuget-package
Summary:	Core foundational nuget packages for System.IO.Ports

%description -n corefx-oob-nuget-package
The System.IO.Ports nuget packages
%endif

%package -n corefx-native
Summary:	Core foundational native libraries
Requires:	coreclr
Requires:	mscorlib

%description -n corefx-native
The native part (.so) of dotnet core foundational libraries

%package -n corefx-managed
Summary:	Core foundational managed libraries
Requires: coreclr
Requires: mscorlib
Requires: corefx-native
AutoReqProv: no

%description -n corefx-managed
The managed part (.dll) of dotnet core foundational class libraries

%package -n corefx-managed-devel
Summary:	Core foundational managed libraries for debugging (.pdb)
Requires: corefx-managed
AutoReqProv: no

%description -n corefx-managed-devel
The managed debugging files (.pdb) of dotnet core fundational class libraries

%package -n corefx-managed-ref
Summary:	Core foundational managed class libraries for developer
AutoReqProv: no

%description -n corefx-managed-ref
The managed part (.dll) of dotnet core foundational class libraries for developer

%if 0%{skipfxtests}
%else
%package -n corefx-test
Summary:	Dotnet Libraries Unit Test
Requires:   corefx-native
Requires:   corefx-managed
AutoReqProv: no

%description -n corefx-test
Unit Test objs
%endif

%package -n corefx-test-native
Summary:	Dotnet Libraries Unit Test, native part
Requires:   corefx-native
Requires:   corefx-managed

%description -n corefx-test-native
Unit Test objs, native part

%ifarch x86_64
%package -n crossgen2-mic
Summary:	Publish crossgen2 as a single file with self-contained
BuildArch: noarch
AutoReqProv: no

%description -n crossgen2-mic
Publish crossgen2 as a single file with self-contained
%endif

%prep
%setup -q -n %{name}-%{version}

%build
cp %{SOURCE1} .

%if 0%{skipmscorlib} && 0%{skipmanaged} && 0%{skipmanagedtools}
%else
%ifarch %{arm} aarch64 riscv64
# Detect interpreter name from cross-gcc
LD_INTERPRETER=$(patchelf --print-interpreter /emul/usr/bin/gcc)
LD_LOCAL_INTERPRETER=$(patchelf --print-interpreter ./.dotnet/dotnet)

if [ "$LD_INTERPRETER" = "$LD_LOCAL_INTERPRETER" ]; then
    echo "Skip patchelf"
else
LD_RPATH=$(patchelf --print-rpath /emul/usr/bin/gcc)
for file in $( find ./.dotnet ./.packages -name "dotnet" -type f -o -name "ilasm" -type f -o -name "ilc" -type f)
do
    patchelf --set-interpreter ${LD_INTERPRETER} ${file}
    patchelf --set-rpath ${LD_RPATH}:%{_builddir}/%{name}-%{version}/libicu-78.1/ ${file}
done
for file in $( find ./.dotnet ./.packages ./libicu-78.1 -iname "*.so" -or -iname "*.so.*" )
do
    patchelf --set-rpath ${LD_RPATH}:%{_builddir}/%{name}-%{version}/libicu-78.1/ ${file}
done

# Crossgen2 native x64 binary is used during build
patchelf --set-interpreter ${LD_INTERPRETER} .packages/microsoft.netcore.app.crossgen2.linux-x64/10.0.9/tools/crossgen2
patchelf --set-rpath ${LD_RPATH}:%{_builddir}/%{name}-%{version}/libicu-78.1/ .packages/microsoft.netcore.app.crossgen2.linux-x64/10.0.9/tools/crossgen2
fi
%endif

%ifarch %{ix86}
for file in $( find ./.dotnet ./.packages ./libicu-78.1 -iname "*.so" -or -iname "*.so.*" )
do
    patchelf --set-rpath %{_builddir}/%{name}-%{version}/libicu-78.1/ ${file}
done

# Crossgen2 native x64 binary is used during build
patchelf --set-rpath ${LD_RPATH}:%{_builddir}/%{name}-%{version}/libicu-78.1/ .packages/microsoft.netcore.app.crossgen2.linux-x64/10.0.9/tools/crossgen2
%endif
%endif

# disable asan build when global forced asan build
%{?asan:
export ASAN_OPTIONS=use_sigaltstack=false:`cat /ASAN_OPTIONS`
/usr/bin/gcc-unforce-options
export LD_LIBRARY_PATH=`pwd`/libicu-78.1
export CPPFLAGS="$CPPFLAGS -DHAS_ADDRESS_SANITIZER "
}

BASE_FLAGS=" --target=%{_host} -gdwarf-4 "

%ifarch x86_64
%define _barch  x64
%endif

%ifarch aarch64
%define _barch  arm64
%endif

%ifarch %{ix86}
%define _barch  x86
export CLANG_NO_LIBDIR_SUFFIX=1
BASE_FLAGS="$(echo $BASE_FLAGS | sed -e 's/--target=i686/--target=i586/')"
BASE_FLAGS="$BASE_FLAGS -mstackrealign"
%endif

%ifarch armv7l
%define _barch  armel
export CLANG_NO_LIBDIR_SUFFIX=1
%endif

%ifarch armv7hl
%define _barch  arm
export CLANG_NO_LIBDIR_SUFFIX=1
%endif

%ifarch riscv64
%define _barch  riscv64
%endif

%ifarch %{arm}
%define _tarch arm
%endif
%ifarch aarch64
%define _tarch arm64
%endif
%ifarch %{ix86}
%define _tarch x86
%endif
%ifarch x86_64
%define _tarch x64
%endif
%ifarch riscv64
%define _tarch riscv64
%endif

%define _reldir_clr                artifacts/bin/coreclr/linux.%{_barch}.%{dotnet_buildtype_clr}
%define _reldir_crossgen2          artifacts/bin/crossgen2_inbuild/%{_barch}/%{dotnet_buildtype_clr}
%define _reldir_fx_native          artifacts/bin/native/net10.0-linux-%{dotnet_buildtype_fx}-%{_barch}
%define _reldir_fx_managed         artifacts/bin/microsoft.netcore.app.runtime.linux-%{_barch}/%{dotnet_buildtype_fx}/runtimes/linux-%{_barch}/lib/net10.0/
%define _reldir_fx_withoob         artifacts/bin/runtime/net10.0-linux-%{dotnet_buildtype_fx}-%{_barch}
%define _reldir_fx_dotnet_host     artifacts/bin/testhost/net10.0-linux-%{dotnet_buildtype_fx}-%{_barch}
%define _reldir_crossgen2_publish  artifacts/bin/crossgen2_publish/%{_barch}/%{dotnet_buildtype_clr}
%define _reldir_fx_oob_nuget       artifacts/packages/%{dotnet_buildtype_clr}/Shipping

export CFLAGS="${BASE_FLAGS}"
export CXXFLAGS="${BASE_FLAGS}"
export ASMFLAGS="${BASE_FLAGS}"

%ifarch %{arm}
%if %{dotnet_buildtype} == "Release"
export CXXFLAGS="$CXXFLAGS -fstack-protector-strong -D_FORTIFY_SOURCE=2"
%else
export CXXFLAGS="$CXXFLAGS -fstack-protector-strong"
%endif
%endif

%if 0%{pgo_instrument}
%define _pgo_flags --pgoinstrument
%else
%if 0%{pgo_optimize}
# pgo optimization is enabled by default
%define _pgo_flags --pgodatapath %{_builddir}/%{name}-%{version}/pgodata/%{_barch}
%else
%define _pgo_flags --nopgooptimize
%endif
%endif

%define _native_opts --cmakeargs -DDISABLE_AGGRESSIVE_OPT=true
%define _managed_opts /p:DisableAggressiveOpt=true
%define _source_version_flags /p:EnableSourceLink=false /p:DisableSourceLink=true /p:EnableSourceControlManagerQueries=false /p:EmbedUntrackedSources=false
%define _build_args --keepnativesymbols true --arch %{_barch} --runtimeConfiguration %{dotnet_buildtype_clr} --librariesConfiguration %{dotnet_buildtype_fx} --hostConfiguration %{dotnet_buildtype_host} %{_source_version_flags} %{_native_opts} %{_managed_opts} /p:UseLocalAppHostPack=true
%define _build_args_release --keepnativesymbols true --arch %{_barch} --runtimeConfiguration Release --librariesConfiguration Release --hostConfiguration Release %{_source_version_flags} %{_native_opts} %{_managed_opts} /p:UseLocalAppHostPack=true

export NUGET_PACKAGES=%{_builddir}/%{name}-%{version}/.packages/
export DOTNET_CLI_HOME=%{_builddir}/%{name}-%{version}/.dotnet_cli_home/
export LD_LIBRARY_PATH=%{_builddir}/%{name}-%{version}/libicu-78.1/

sed -i "s,TIZEN_NUGET_PACKAGES_DIR,${NUGET_PACKAGES}," %{_builddir}/%{name}-%{version}/NuGet.config
sed -i "s,TIZEN_NUGET_PACKAGES_DIR,${NUGET_PACKAGES}," ${DOTNET_CLI_HOME}/.dotnet/toolResolverCache/1/coverlet.console
sed -i "s,TIZEN_NUGET_PACKAGES_DIR,${NUGET_PACKAGES}," ${DOTNET_CLI_HOME}/.dotnet/toolResolverCache/1/dotnet-reportgenerator-globaltool
sed -i "s,TIZEN_NUGET_PACKAGES_DIR,${NUGET_PACKAGES}," ${DOTNET_CLI_HOME}/.dotnet/toolResolverCache/1/microsoft.dotnet.xharness.cli
sed -i "s,TIZEN_NUGET_PACKAGES_DIR,${NUGET_PACKAGES}," ${DOTNET_CLI_HOME}/.dotnet/toolResolverCache/1/microsoft.visualstudio.slngen.tool

# Build native CoreCLR, native CoreFX and native host
./build.sh --portablebuild false %{_build_args} --subset clr.runtime+clr.spmi+libs.native+host.native --cmakeargs -DFEATURE_IBCLOGGER=true --cmakeargs -DFEATURE_ENABLE_NO_ADDRESS_SPACE_RANDOMIZATION=true --cmakeargs -DCLR_ADDITIONAL_LINKER_FLAGS=-Wl,-z,relro %{_pgo_flags}

%ifarch x86_64
./build.sh --portablebuild false %{_build_args} --subset clr.alljits --cmakeargs -DFEATURE_IBCLOGGER=true --cmakeargs -DFEATURE_ENABLE_NO_ADDRESS_SPACE_RANDOMIZATION=true --cmakeargs -DCLR_ADDITIONAL_LINKER_FLAGS=-Wl,-z,relro %{_pgo_flags}
%endif

%if 0%{skipmscorlib}
%else
# Build mscorlib (System.Private.CoreLib.dll)
./build.sh --portablebuild false %{_build_args} --subset clr.corelib
%endif

%if 0%{skipmanaged}
%else
# Build managed CoreFX
./build.sh %{_build_args} --subset libs.sfx+libs.oob

%if 0%{skipmanagedtools}
%else
# Build managed tools
./build.sh %{_build_args} --subset clr.tools

%endif

%if 0%{skipnugetpackage}
%else
# Build nuget packages for System.IO.Ports
./.dotnet/dotnet pack src/libraries/System.IO.Ports -c %{dotnet_buildtype_clr} -p:BuildReference=true -p:KeepNativeSymbols=true -p:NativeBinDir=%{_builddir}/%{name}-%{version}/%{_reldir_fx_native}/ -p:TargetRid=linux-%{_tarch} -p:StabilizePackageVersion=true
%endif

%if 0%{skipfxtests}
%else
# Build CoreFX managed tests, which are arch specific
# TODO: check if /p:DisableImplicitFSharpCoreReference=true is needed
./build.sh --portablebuild false %{_build_args} --subset libs.pretest+libs.tests --testscope all /p:UseLocalAppHostPack=true
%endif
%endif

%if 0%{skiptests}
%else
# Build CoreCLR tests

%if %{dotnet_buildtype} != "Release"
# Build Release CoreCLR & CoreFX (these are required for some tests)

# Build native CoreCLR and native CoreFX
./build.sh --portablebuild false %{_build_args_release} --subset clr.runtime+clr.spmi+libs.native+host.native --cmakeargs -DFEATURE_IBCLOGGER=true --cmakeargs -DFEATURE_ENABLE_NO_ADDRESS_SPACE_RANDOMIZATION=true --cmakeargs -DCLR_ADDITIONAL_LINKER_FLAGS=-Wl,-z,relro %{_pgo_flags}

# Build mscorlib (System.Private.CoreLib.dll)
./build.sh --portablebuild false %{_build_args_release} --subset clr.corelib

# Build managed CoreFX
./build.sh %{_build_args_release} --subset libs.sfx+libs.oob
%endif

# Build native part of tests as non-portable (i.e. for Tizen)
BuildAllTestsAsStandalone=true ./src/tests/build.sh -%{dotnet_buildtype_clr} portablebuild=false -%{_barch} -priority1 skipmanaged skipgeneratelayout skiprestorepackages /p:__SkipPackageRestore=true /p:UseLocalAppHostPack=true -p:PublishAot=false -p:SelfContained=false -p:PublishSingleFile=false

# Build managed part of tests
BuildAllTestsAsStandalone=true ./src/tests/build.sh -%{dotnet_buildtype_clr} -%{_barch} -priority1 copynativeonly /p:UseLocalAppHostPack=true -p:PublishAot=false -p:SelfContained=false -p:PublishSingleFile=false
# TODO: check if /p:DisableImplicitFSharpCoreReference=true is needed
BuildAllTestsAsStandalone=true ./src/tests/build.sh -%{dotnet_buildtype_clr} -%{_barch} -priority1 skipnative skipgeneratelayout skiptestwrappers /p:UseLocalAppHostPack=true -p:PublishAot=false -p:SelfContained=false -p:PublishSingleFile=false
BuildAllTestsAsStandalone=true ./src/tests/build.sh -%{dotnet_buildtype_clr} -%{_barch} -priority1 generatelayoutonly /p:UseLocalAppHostPack=true -p:PublishAot=false -p:SelfContained=false -p:PublishSingleFile=false
%endif

%install
# .NET Core Runtime dir
%define dotnetdir       dotnet
%define netshareddir    %{dotnetdir}/shared
%define netcoreappdir   %{netshareddir}/Microsoft.NETCore.App/%{dotnet_version}
mkdir -p %{buildroot}%{_datadir}/%{netcoreappdir}
# for devel
mkdir -p %{buildroot}%{_datadir}/%{netcoreappdir}/native/minipal

# Test dirs
%define clrtestdir      /opt/usr/coreclr-tc
%define fxtestdir       /opt/usr/corefx-tc
mkdir -p %{buildroot}/%{clrtestdir}
mkdir -p %{buildroot}/%{fxtestdir}
mkdir -p %{buildroot}/%{fxtestdir}/coreroot

# CoreFX OOB nuget dir
%if 0%{skipnugetpackage}
%else
%define fxnugetdir       /corefx_oob_nuget_packages
mkdir -p %{buildroot}/%{fxnugetdir}
mkdir -p %{buildroot}/%{fxnugetdir}/System.IO.Ports
%endif

# .NET Tizen Runtime dir
%define dotnettizendir  dotnet.tizen
%define dotnetfwdir     %{dotnettizendir}/framework
mkdir -p %{buildroot}%{_datadir}/%{dotnettizendir}
mkdir -p %{buildroot}%{_datadir}/%{dotnetfwdir}
ln -sf %{_datadir}/%{netcoreappdir} %{buildroot}%{_datadir}/%{dotnettizendir}/netcoreapp

%ifarch x86_64
# .NET Tizen MIC dir
%define dotnetmicdir /opt/usr/dotnet/mic
mkdir -p %{buildroot}/%{dotnetmicdir}
%endif

# symlink to .NET version for compatibility
ln -sf %{dotnet_version} %{buildroot}%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/2.0.0
ln -sf %{dotnet_version} %{buildroot}%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/2.1.0
ln -sf %{dotnet_version} %{buildroot}%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/2.1.1
ln -sf %{dotnet_version} %{buildroot}%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/2.1.4
ln -sf %{dotnet_version} %{buildroot}%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/3.0.0
ln -sf %{dotnet_version} %{buildroot}%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/3.1.3
ln -sf %{dotnet_version} %{buildroot}%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/6.0.0
ln -sf %{dotnet_version} %{buildroot}%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/6.0.9
ln -sf %{dotnet_version} %{buildroot}%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/8.0.0
ln -sf %{dotnet_version} %{buildroot}%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/8.0.11

# CoreCLR native
cp %{_reldir_clr}/corerun                               %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_clr}/libclrjit.so                          %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_clr}/libclrgc.so                           %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_clr}/libcoreclr.so                         %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_clr}/libmscordaccore.so                    %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_clr}/libmscordbi.so                        %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_clr}/libcoreclrtraceptprovider.so          %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_clr}/libjitinterface_%{_tarch}.so          %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_clr}/ilasm                                 %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_clr}/ildasm                                %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_clr}/createdump                            %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_clr}/libdnetmemoryenum.so                  %{buildroot}%{_datadir}/%{netcoreappdir}

# CoreFX native
cp %{_reldir_fx_native}/libSystem.Globalization.Native.so                  %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_fx_native}/libSystem.IO.Compression.Native.so                 %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_fx_native}/libSystem.Native.so                                %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_fx_native}/libSystem.Net.Security.Native.so                   %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_fx_native}/libSystem.Security.Cryptography.Native.OpenSsl.so  %{buildroot}%{_datadir}/%{netcoreappdir}

# CoreFX native test
cp %{_reldir_fx_native}/libSystem.IO.Ports.Native.so                       %{buildroot}/%{fxtestdir}/coreroot

%if 0%{skipnugetpackage}
%else
# CoreFX nuget package
cp %{_reldir_fx_oob_nuget}/runtime.linux-%{_tarch}.runtime.native.System.IO.Ports.*[0-9].nupkg %{buildroot}/%{fxnugetdir}/System.IO.Ports
cp %{_reldir_fx_oob_nuget}/runtime.native.System.IO.Ports.*[0-9].nupkg                         %{buildroot}/%{fxnugetdir}/System.IO.Ports
cp %{_reldir_fx_oob_nuget}/System.IO.Ports.*[0-9].nupkg                                        %{buildroot}/%{fxnugetdir}/System.IO.Ports
%endif

# .NET Core Headers and static libraries
mkdir -p %{buildroot}%{_datadir}/%{netcoreappdir}/src/pal/src/
mkdir -p %{buildroot}%{_datadir}/%{netcoreappdir}/src/debug/
mkdir -p %{buildroot}%{_datadir}/%{netcoreappdir}/src/dlls/
mkdir -p %{buildroot}%{_datadir}/%{netcoreappdir}/src/coreclr/hosts/
cp -rf src/coreclr/inc                %{buildroot}%{_datadir}/%{netcoreappdir}/src/
cp -rf src/coreclr/pal/inc            %{buildroot}%{_datadir}/%{netcoreappdir}/src/pal/
cp -rf src/coreclr/pal/prebuilt       %{buildroot}%{_datadir}/%{netcoreappdir}/src/pal/
cp -rf src/coreclr/debug/inc          %{buildroot}%{_datadir}/%{netcoreappdir}/src/debug/
cp -rf src/coreclr/hosts/inc          %{buildroot}%{_datadir}/%{netcoreappdir}/src/coreclr/hosts/
cp -rf src/coreclr/pal/src/include    %{buildroot}%{_datadir}/%{netcoreappdir}/src/pal/src
cp -rf %{_reldir_clr}/lib             %{buildroot}%{_datadir}/%{netcoreappdir}
cp -rf src/native/minipal             %{buildroot}%{_datadir}/%{netcoreappdir}/native

# System.Private.CoreLib.dll
%if 0%{skipmscorlib}
%else
cp %{_reldir_clr}/IL/System.Private.CoreLib.dll     %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_clr}/IL/System.Private.CoreLib.pdb     %{buildroot}%{_datadir}/%{netcoreappdir}
%endif

# Managed tools and managed CoreFX
%if 0%{skipmanaged}
%else

%if 0%{skipmanagedtools}
%else

# Managed crossgen2
mkdir -p %{buildroot}%{_datadir}/%{netcoreappdir}/crossgen2
cp %{_reldir_crossgen2}/crossgen2.dll                              %{buildroot}%{_datadir}/%{netcoreappdir}/crossgen2
cp %{_reldir_crossgen2}/ILCompiler.Diagnostics.dll                 %{buildroot}%{_datadir}/%{netcoreappdir}/crossgen2
cp %{_reldir_crossgen2}/ILCompiler.ReadyToRun.dll                  %{buildroot}%{_datadir}/%{netcoreappdir}/crossgen2
cp %{_reldir_crossgen2}/ILCompiler.TypeSystem.dll                  %{buildroot}%{_datadir}/%{netcoreappdir}/crossgen2
cp %{_reldir_crossgen2}/ILCompiler.DependencyAnalysisFramework.dll %{buildroot}%{_datadir}/%{netcoreappdir}/crossgen2
cp %{_reldir_crossgen2}/Microsoft.DiaSymReader.dll                 %{buildroot}%{_datadir}/%{netcoreappdir}/crossgen2
cp %{_reldir_crossgen2}/System.CommandLine.dll                     %{buildroot}%{_datadir}/%{netcoreappdir}/crossgen2
cp %{_reldir_crossgen2}/*.pdb                                      %{buildroot}%{_datadir}/%{netcoreappdir}/crossgen2

cp %{_reldir_clr}/libjitinterface_%{_tarch}.so                         %{buildroot}%{_datadir}/%{netcoreappdir}/crossgen2

# NativeAOT crossgen2
cp %{_reldir_crossgen2_publish}/native/crossgen2                   %{buildroot}%{_datadir}/%{netcoreappdir}/crossgen2

%endif

# Managed CoreFX
cp %{_reldir_fx_managed}/*.dll %{buildroot}%{_datadir}/%{netcoreappdir}
cp %{_reldir_fx_managed}/*.pdb %{buildroot}%{_datadir}/%{netcoreappdir}

# Copy files for test rpm
%if 0%{skipfxtests}
%else

mkdir artifacts/corefx_oob_nuget_packages
mkdir artifacts/corefx_tests
mkdir artifacts/corefx_tests/tests
mkdir artifacts/corefx_tests/coreroot
mkdir artifacts/corefx_tests/dotnet_host
mkdir -p artifacts/corefx_tests/dotnet_host/host/fxr/%{dotnet_version}
mkdir -p artifacts/corefx_tests/dotnet_host/shared/Microsoft.NETCore.App/

# Copy corefx tests with only required files to keep size smaller
for test_dir in `find ./artifacts/bin -type d -name "*.Tests"`; do
  test=$(basename $test_dir)
  mkdir artifacts/corefx_tests/tests/$test

  for FILE in `find $test_dir \( -name "*dll" -or -name "*.json" -or -name "*.resources" -or -name "*.pdb" -or -name "*.xml" -or -name "*.exe" -or -name "*.cs" -or -name "*.docx" -or -name "*.pfx" -or -name "*.so" -or -name "*.h" -or -name "*.config" -or -name "*.props" -or -name "ibm-fpgen.txt" \)`
  do
      cp $FILE artifacts/corefx_tests/tests/$test/
  done

  for DIR in `find $test_dir -type d \( -name "*TestFiles" -or -name "*TestData" -or -name "*NetworkFiles" -or -name "*Utils" -or -name "*Mono" -or -name "*TestFeeds" -or -name "*bitmaps" -or -name "*TestDataCertificates" -or -name "*live-ref-pack" -or -name "*tar" -or -name "*targz" -or -name "*strange" -or -name "*unarchived" -or -name "*XmlDocument" -or -name "*XmlSchema" -or -name "*Baselines" -or -name "*TestClasses" -or -name "*SqlXml.CreateReader" -or -name "*testroot" \)`
  do
      cp -r $DIR artifacts/corefx_tests/tests/$test/
  done
done

# Some tests require all files
for test in System.Runtime.Loader.Tests System.Resources.ResourceManager.Tests System.IO.Packaging.Tests; do
  test_dir=$(find ./artifacts/bin -type d -name $test)
  file_dir=$(find $test_dir -name $test.dll)
  file_dir=$(dirname $file_dir)
  cp -r $file_dir/* artifacts/corefx_tests/tests/$test/
done

for test_dir in `find artifacts/corefx_tests/tests/ -type d -name "*.Tests"`; do
  test=$(basename $test_dir)
  sed "s/COREFX_TEST_NAME/${test}/g" RunTests.sh > ${test_dir}/RunTests.sh
  chmod +x ${test_dir}/RunTests.sh

  cp artifacts/TargetingPack/xunit.* ${test_dir}
done

for test_dir in `find artifacts/corefx_tests/tests/ -type d -name "Invariant.Tests"`; do
  file=$(find ${test_dir} -name RunTests.sh)
  cp $file $file.bak
  sed "s/TMPDIR=\$tmpDir/CORECLR_GLOBAL_INVARIANT=1 TMPDIR=\$tmpDir/g" $file > $file.bak
  mv $file.bak $file
  chmod +x $file
done

# There are no tests in Microsoft.Extensions.DependencyInjection.Specification.Tests
rm -rf artifacts/corefx_tests/tests/Microsoft.Extensions.DependencyInjection.Specification.Tests

. /etc/os-release

cp %{_reldir_fx_withoob}/*.dll artifacts/corefx_tests/coreroot/
cp artifacts/bin/tizen.${VERSION_ID}-%{_barch}.%{dotnet_buildtype_host}/corehost/dotnet artifacts/corefx_tests/dotnet_host
cp artifacts/bin/tizen.${VERSION_ID}-%{_barch}.%{dotnet_buildtype_host}/corehost/libhostfxr.so artifacts/corefx_tests/dotnet_host/host/fxr/%{dotnet_version}
cp artifacts/bin/tizen.${VERSION_ID}-%{_barch}.%{dotnet_buildtype_host}/corehost/libhostpolicy.so artifacts/corefx_tests/coreroot/
ln -s ../../../coreroot/ artifacts/corefx_tests/dotnet_host/shared/Microsoft.NETCore.App/%{dotnet_version}
ln -s ../dotnet_host/dotnet artifacts/corefx_tests/coreroot/dotnet
cp %{_reldir_fx_dotnet_host}/shared/Microsoft.NETCore.App/%{dotnet_version}/Microsoft.NETCore.App.deps.json artifacts/corefx_tests/coreroot

mv artifacts/corefx_tests/tests %{buildroot}/%{fxtestdir}/
mv artifacts/corefx_tests/coreroot/* %{buildroot}/%{fxtestdir}/coreroot/
mv artifacts/corefx_tests/dotnet_host %{buildroot}/%{fxtestdir}/
cp runtest_fx.sh %{buildroot}/%{fxtestdir}/runtest.sh
chmod +x %{buildroot}/%{fxtestdir}/runtest.sh

%endif

%endif

# crossgen2-mic
%ifarch x86_64
cp %{_reldir_crossgen2_publish}/native/crossgen2 %{_reldir_crossgen2_publish}/crossgen2
crossgen2_naot="crossgen2 libjitinterface_x64.so libclrjit_universal_arm_x64.so libclrjit_universal_arm64_x64.so"
for name in $crossgen2_naot
do
  cp %{_reldir_crossgen2_publish}/$name    %{buildroot}%{dotnetmicdir}
done

result_list="ld-linux-x86-64.so.2"
search_ldd() {
  local path=$1
  local library_list=$2
  if [ -f "$path" ]; then
    ldd_result=$(/usr/bin/ldd "$path")
    echo "$ldd_result" | while read line
    do
      case "$line" in
        *GLIBC_*|*linux-vdso.so.1*|*ld-linux-x86-64.so.2*)
          ;;
        *)
          cut_path=`echo $line | cut -d ' ' -f3`
          cut_name=`echo $line | cut -d ' ' -f1`
          library_list="$library_list $cut_name"
          echo "$library_list"
          if [ -f "$cut_path" ]; then
            result_list="$result_list $(search_ldd "$cut_path" "$library_list")"
          fi
          ;;
      esac
    done
  fi
}

for name in $crossgen2_naot
do
  result_list="$result_list $(search_ldd %{_reldir_crossgen2_publish}/$name)"
  echo $name: | tee -a %{buildroot}%{dotnetmicdir}/crossgen2-mic.txt > /dev/null
  /usr/bin/ldd %{_reldir_crossgen2_publish}/$name | tee -a %{buildroot}%{dotnetmicdir}/crossgen2-mic.txt > /dev/null
done

unique_result=$(echo $result_list | tr ' ' '\n' | sort -u | tr '\n' ' ')
for name in $unique_result
do
  cp %{buildroot}/../../../../../lib64/$name    %{buildroot}%{dotnetmicdir}/$name
  echo $name: | tee -a %{buildroot}%{dotnetmicdir}/crossgen2-mic.txt > /dev/null
  /usr/bin/ldd %{buildroot}/../../../../../lib64/$name | tee -a %{buildroot}%{dotnetmicdir}/crossgen2-mic.txt > /dev/null
done

%endif

# coreclr-test
%if 0%{skiptests}
%else

cp runtest_clr.sh %{buildroot}/%{clrtestdir}/runtest.sh
chmod +x %{buildroot}/%{clrtestdir}/runtest.sh
cp unsupportedCrossgenLibs.%{_barch}.txt      %{buildroot}/%{clrtestdir}/unsupportedCrossgenLibs.txt | true
cp unsupportedCrossgenTests.%{_barch}.txt     %{buildroot}/%{clrtestdir}/unsupportedCrossgenTests.txt | true
cp unsupportedTests.%{_barch}.txt             %{buildroot}/%{clrtestdir}/unsupportedTests.txt | true
cp unsupportedGCStressTests.%{_barch}.txt     %{buildroot}/%{clrtestdir}/unsupportedGCStressTests.txt | true

%define _tcreldir artifacts/tests/coreclr/linux.%{_barch}.%{dotnet_buildtype_clr}
cp -r %{_tcreldir}/* %{buildroot}/%{clrtestdir}
find %{buildroot}/%{clrtestdir} -name "*.pdb" -exec rm {} \;
find %{buildroot}/%{clrtestdir} -name "*.cmd" -exec rm {} \;
rm -rf %{buildroot}/%{clrtestdir}/Tests/Core_Root/in
rm -rf %{buildroot}/%{clrtestdir}/Tests/Core_Root/sharedFramework
rm -rf %{buildroot}/%{clrtestdir}/Tests/Core_Root/PDB
rm -rf %{buildroot}/%{clrtestdir}/Tests/Core_Root/x64
rm -rf %{buildroot}/%{clrtestdir}/Tests/Core_Root/gcinfo
rm -rf %{buildroot}/%{clrtestdir}/Tests/Core_Root/inc
rm -rf %{buildroot}/%{clrtestdir}/Tests/Core_Root/lib
rm -rf %{buildroot}/%{clrtestdir}/Tests/Core_Root/IL
rm -rf %{buildroot}/%{clrtestdir}/Tests/Core_Root/crossgen2

%ifarch %{arm} aarch64 riscv64
rm -rf %{buildroot}/%{clrtestdir}/Tests/Core_Root/R2RDump/Microsoft.DiaSymReader.Native.x86.dll
rm -rf %{buildroot}/%{clrtestdir}/Tests/Core_Root/R2RDump/Microsoft.DiaSymReader.Native.amd64.dll
%endif

rm -rf %{buildroot}/%{clrtestdir}/Tests/Core_Root/ILCompiler.*.dll
rm -rf %{buildroot}/%{clrtestdir}/build/
rm %{buildroot}/%{clrtestdir}/Tests/Core_Root/superpmi \
   %{buildroot}/%{clrtestdir}/Tests/Core_Root/SOS_README.md \
   %{buildroot}/%{clrtestdir}/Tests/Core_Root/mcs \
   %{buildroot}/%{clrtestdir}/Tests/Core_Root/*.a \
   %{buildroot}/%{clrtestdir}/Tests/Core_Root/*.so \
   %{buildroot}/%{clrtestdir}/Tests/Core_Root/ilasm \
   %{buildroot}/%{clrtestdir}/Tests/Core_Root/ildasm

cp %{buildroot}/%{clrtestdir}/bin/*.so %{buildroot}/%{clrtestdir}/Tests/Core_Root
mv %{buildroot}/%{clrtestdir}/Tests/Core_Root %{buildroot}/%{clrtestdir}/coreroot
%endif

# test native
mkdir -p %{buildroot}/%{clrtestdir}/bin
cp %{_reldir_clr}/superpmi                          %{buildroot}/%{clrtestdir}/bin
cp %{_reldir_clr}/mcs                               %{buildroot}/%{clrtestdir}/bin
cp %{_reldir_clr}/libsuperpmi-shim-collector.so     %{buildroot}/%{clrtestdir}/bin
cp %{_reldir_clr}/libsuperpmi-shim-counter.so       %{buildroot}/%{clrtestdir}/bin
cp %{_reldir_clr}/libsuperpmi-shim-simple.so        %{buildroot}/%{clrtestdir}/bin

###
### Copy nupkg to nuget directory
###
mkdir -p %{buildroot}/nuget
cp ./nuget/*.nupkg %{buildroot}/nuget

# coreclr rpm
%files
%manifest %{name}.manifest
%dir %{_datadir}/%{dotnetdir}
%dir %{_datadir}/%{netcoreappdir}
%dir %{_datadir}/%{dotnettizendir}
%{_datadir}/%{netcoreappdir}/corerun
%{_datadir}/%{netcoreappdir}/libclrjit.so
%{_datadir}/%{netcoreappdir}/libclrgc.so
%{_datadir}/%{netcoreappdir}/libcoreclr.so
%{_datadir}/%{netcoreappdir}/libmscordaccore.so
%{_datadir}/%{netcoreappdir}/libmscordbi.so
%{_datadir}/%{netcoreappdir}/libcoreclrtraceptprovider.so
%{_datadir}/%{netcoreappdir}/libjitinterface_%{_tarch}.so
%{_datadir}/%{dotnettizendir}/netcoreapp
%{_datadir}/%{netcoreappdir}/ilasm
%{_datadir}/%{netcoreappdir}/ildasm
%{_datadir}/%{netcoreappdir}/createdump
%{_datadir}/%{netcoreappdir}/libdnetmemoryenum.so
%if 0%{skipmanaged}
%else

%if 0%{skipmanagedtools}
%else

%dir %{_datadir}/%{netcoreappdir}/crossgen2
%{_datadir}/%{netcoreappdir}/crossgen2/crossgen2.dll
%{_datadir}/%{netcoreappdir}/crossgen2/ILCompiler.Diagnostics.dll
%{_datadir}/%{netcoreappdir}/crossgen2/ILCompiler.ReadyToRun.dll
%{_datadir}/%{netcoreappdir}/crossgen2/ILCompiler.TypeSystem.dll
%{_datadir}/%{netcoreappdir}/crossgen2/ILCompiler.DependencyAnalysisFramework.dll
%{_datadir}/%{netcoreappdir}/crossgen2/Microsoft.DiaSymReader.dll
%{_datadir}/%{netcoreappdir}/crossgen2/System.CommandLine.dll

%{_datadir}/%{netcoreappdir}/crossgen2/libjitinterface_%{_tarch}.so
%{_datadir}/%{netcoreappdir}/crossgen2/crossgen2
%endif

%endif

# symlink to .NET version for compatibility
%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/2.0.0
%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/2.1.0
%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/2.1.1
%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/2.1.4
%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/3.0.0
%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/3.1.3
%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/6.0.0
%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/6.0.9
%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/8.0.0
%{_datadir}/%{netshareddir}/Microsoft.NETCore.App/8.0.11

%files -n coreclr-test
%manifest %{name}.manifest
%dir %{clrtestdir}
%{clrtestdir}/*

%files -n coreclr-devel
%manifest %{name}.manifest
%dir %{_datadir}/%{netcoreappdir}/lib
%dir %{_datadir}/%{netcoreappdir}/src
%dir %{_datadir}/%{netcoreappdir}
%dir %{_datadir}/%{netcoreappdir}/native/minipal
%{_datadir}/%{netcoreappdir}/lib/*
%{_datadir}/%{netcoreappdir}/src/*
%{_datadir}/%{netcoreappdir}/native/minipal/*

%if 0%{skipmscorlib}
%else
%{_datadir}/%{netcoreappdir}/System.Private.CoreLib.pdb
%endif

%if 0%{skipmanaged}
%else
%if 0%{skipmanagedtools}
%else
%{_datadir}/%{netcoreappdir}/crossgen2/*.pdb
%endif
%endif

%if 0%{skipmscorlib}
%else
%files -n mscorlib
%manifest %{name}.manifest
%{_datadir}/%{netcoreappdir}/System.Private.CoreLib.dll
%endif

%files -n corefx-native
%manifest %{name}.manifest
%{_datadir}/%{netcoreappdir}/libSystem.Globalization.Native.so
%{_datadir}/%{netcoreappdir}/libSystem.IO.Compression.Native.so
%{_datadir}/%{netcoreappdir}/libSystem.Native.so
%{_datadir}/%{netcoreappdir}/libSystem.Net.Security.Native.so
%{_datadir}/%{netcoreappdir}/libSystem.Security.Cryptography.Native.OpenSsl.so

%files -n corefx-test-native
%manifest %{name}.manifest
%{fxtestdir}/coreroot/libSystem.IO.Ports.Native.so
%if 0%{skipfxtests}
%else
%{fxtestdir}/coreroot/Microsoft.NETCore.App.deps.json
%{fxtestdir}/coreroot/dotnet
%{fxtestdir}/coreroot/libhostpolicy.so
%{fxtestdir}/dotnet_host/*
%endif

%if 0%{skipnugetpackage}
%else
%files -n corefx-oob-nuget-package
%manifest %{name}.manifest
%{fxnugetdir}/System.IO.Ports/*.nupkg
%endif

%if 0%{skipmanaged}
%else

%files -n corefx-managed
%manifest %{name}.manifest
%{_datadir}/%{netcoreappdir}/*.dll
%exclude %{_datadir}/%{netcoreappdir}/System.Private.CoreLib.dll

%files -n corefx-managed-devel
%manifest %{name}.manifest
%{_datadir}/%{netcoreappdir}/*.pdb
%exclude %{_datadir}/%{netcoreappdir}/System.Private.CoreLib.pdb

%if 0%{skipfxtests}
%else
%files -n corefx-test
%manifest %{name}.manifest
%{fxtestdir}/tests
%{fxtestdir}/coreroot/*.dll
%{fxtestdir}/runtest.sh
%endif

%endif

%files -n corefx-managed-ref
%manifest %{name}.manifest
/nuget/*.nupkg

%ifarch x86_64
%files -n crossgen2-mic
%manifest %{name}.manifest
%dir %{dotnetmicdir}
%{dotnetmicdir}/*
%endif

%if 0%{skipmscorlib}
%else
%post -n mscorlib
rm -f %{_datadir}/%{netcoreappdir}/*.Backup
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig
