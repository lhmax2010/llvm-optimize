%{!?dotnet_buildtype: %define dotnet_buildtype Release}

%define dotnet_version 10.0.10

Name:       coreclr-diagnostics
Version:    10.0.10
Release:    0
Summary:    Microsoft .NET Core runtime diagnostic tools
Group:      Development/Languages
License:    MIT
URL:        https://github.com/dotnet/diagnostics
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

BuildRequires: clang >= 3.8
BuildRequires: clang-devel >= 3.8
BuildRequires: cmake
BuildRequires: coreclr-devel
BuildRequires: corefx-managed
BuildRequires: gettext-tools
BuildRequires: pkgconfig(openssl3)
BuildRequires: libstdc++-devel
BuildRequires: llvm >= 3.8
BuildRequires: llvm-devel >= 3.8
BuildRequires: pkgconfig(libunwind)
BuildRequires: pkgconfig(lttng-ust)
BuildRequires: pkgconfig(uuid)
BuildRequires: python
BuildRequires: tizen-release
%ifnarch riscv64
BuildRequires: lldb >= 3.8
BuildRequires: lldb-devel >= 3.8
%endif

%ifarch armv7l
BuildRequires: python-accel-armv7l-cross-arm
BuildRequires: clang-accel-armv7l-cross-arm
BuildRequires: patchelf
%endif

%ifarch armv7hl
BuildRequires: python-accel-armv7hl-cross-arm
BuildRequires: clang-accel-armv7hl-cross-arm
BuildRequires: patchelf
%endif

%ifarch aarch64
BuildRequires: python-accel-aarch64-cross-aarch64
BuildRequires: clang-accel-aarch64-cross-aarch64
BuildRequires: patchelf
%endif

%ifarch riscv64
BuildRequires: python-accel-riscv64-cross-riscv64
BuildRequires: clang-accel-riscv64-cross-riscv64
BuildRequires: patchelf
%endif

%ifarch %{ix86}
BuildRequires: patchelf
BuildRequires: glibc-64bit
BuildRequires: libgcc-64bit
BuildRequires: libopenssl3-64bit
BuildRequires: libstdc++-64bit
BuildRequires: libunwind-64bit
BuildRequires: libuuid-64bit
BuildRequires: zlib-64bit
%endif

AutoReq: 0
Requires: coreclr
Requires: corefx-managed
Requires: glibc
Requires: libgcc
Requires: libstdc++
Requires: libunwind
Requires: libuuid

%description
This package contains components for basic .NET debugging and diagnostic support.

%package -n coreclr-dbgshim
Summary: This package contains libgdbshim (part of Diagnostics), CoreCLR Debug API.
AutoReqProv: no

%description -n coreclr-dbgshim
libdbgshim.so library (part of Diagnostics).

%prep
%setup -q -n %{name}-%{version}

%build
cp %{SOURCE1} .

%ifarch armv7l armv7hl aarch64 riscv64
# Detect interpreter name from cross-gcc
LD_INTERPRETER=$(patchelf --print-interpreter /emul/usr/bin/gcc)
LD_LOCAL_INTERPRETER=$(patchelf --print-interpreter .dotnet/dotnet)

if [ "$LD_INTERPRETER" = "$LD_LOCAL_INTERPRETER" ]; then
    echo "Skip patchelf"
else
LD_RPATH=$(patchelf --print-rpath /emul/usr/bin/gcc)
# Patch all ELF executables (dotnet, csc, vbc, etc.) and shared libraries
find .dotnet -type f | while read file; do
    if file "$file" | grep -q "ELF.*executable"; then
        patchelf --set-interpreter ${LD_INTERPRETER} "$file"
        patchelf --set-rpath ${LD_RPATH}:%{_builddir}/%{name}-%{version}/libicu-78.1/ "$file"
    fi
done
for file in $(find .dotnet libicu-78.1 -iname *.so -or -iname *.so.*)
do
    patchelf --set-rpath ${LD_RPATH}:%{_builddir}/%{name}-%{version}/libicu-78.1/ ${file}
done
fi
%endif

%ifarch %{ix86}
for file in $(find .dotnet libicu-78.1 -iname *.so -or -iname *.so.*)
do
    patchelf --set-rpath %{_builddir}/%{name}-%{version}/libicu-78.1/ ${file}
done
%endif

%{?asan:
export LD_LIBRARY_PATH=`pwd`/libicu-57.1
}
BASE_FLAGS=" --target=%{_host} -gdwarf-4 "

%ifarch x86_64
# Even though build architectur is x86_64, it will be running on arm board.
# So we need to pass the arch argument as arm.
%define _barch  %{?cross:%{cross}}%{!?cross:x64}
%else
%ifarch aarch64
%define _barch  arm64
%else
%ifarch riscv64
%define _barch  riscv64
%else
%ifarch %{ix86}
%define _barch  x86
export CLANG_NO_LIBDIR_SUFFIX=1
export DOTNET_GCHeapHardLimit=1C0000000
BASE_FLAGS=$(echo $BASE_FLAGS | sed -e 's/--target=i686/--target=i586/')
BASE_FLAGS="$BASE_FLAGS -mstackrealign"
%else
%ifarch armv7l
%define _barch  armel
export CLANG_NO_LIBDIR_SUFFIX=1
%else
%ifarch armv7hl
%define _barch  arm
export CLANG_NO_LIBDIR_SUFFIX=1
%else

%endif
%endif
%endif
%endif
%endif
%endif

export CFLAGS=$BASE_FLAGS
export CXXFLAGS=$BASE_FLAGS
export ASMFLAGS="${BASE_FLAGS}"

%define _buildtype %{dotnet_buildtype}
%define _artifacts artifacts/bin

%ifarch armv7l armv7hl
%if %{dotnet_buildtype} == "Release"
export CXXFLAGS="$CXXFLAGS -fstack-protector-strong -D_FORTIFY_SOURCE=2"
%else
export CXXFLAGS="$CXXFLAGS -fstack-protector-strong"
%endif
%endif

export TIZEN_LOCAL_BUILD=1
export NUGET_PACKAGES=%{_builddir}/%{name}-%{version}/.packages
export LD_LIBRARY_PATH=%{_builddir}/%{name}-%{version}/libicu-78.1

sed -i "s,TIZEN_NUGET_PACKAGES_DIR,${NUGET_PACKAGES}," %{_builddir}/%{name}-%{version}/NuGet.config

./build.sh --portablebuild=false -configuration %{_buildtype} -architecture %{_barch} -keepnativesymbols /p:NeedsPublishing=true /p:EnableSourceLink=false /p:EnableSourceControlManagerQueries=false /p:SkipTests=true

%install
%define diagnosticsdir   %{_datadir}/dotnet/shared/Microsoft.NETCore.App/%{dotnet_version}/SOS
%define dbgshimdir   %{_datadir}/dotnet/shared/Microsoft.NETCore.App/%{dotnet_version}

%ifarch x86_64
%define rid linux-x64
%else
%ifarch aarch64
%define rid linux-arm64
%else
%ifarch riscv64
%define rid linux-riscv64
%else
%ifarch %{ix86}
%define rid linux-x86
%else
%ifarch armv7l armv7hl
%define rid linux-arm
%else

%endif
%endif
%endif
%endif
%endif

# SOS
mkdir -p %{buildroot}%{diagnosticsdir}/%{rid}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/libsos.so %{buildroot}%{diagnosticsdir}/%{rid}
%ifnarch riscv64
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/libsosplugin.so %{buildroot}%{diagnosticsdir}/%{rid}
%endif
# put sosdocsunix.txt close to libsos.so copy (need for `help command`)
cp -f %{_artifacts}/linux.%{_barch}.%{_buildtype}/sosdocsunix.txt %{buildroot}%{diagnosticsdir}/%{rid}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/Microsoft.Bcl.AsyncInterfaces.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/Microsoft.Diagnostics.DebugServices.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/Microsoft.Diagnostics.DebugServices.Implementation.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/Microsoft.Diagnostics.ExtensionCommands.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/Microsoft.Diagnostics.NETCore.Client.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/Microsoft.Diagnostics.Runtime.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/Microsoft.Extensions.DependencyInjection.Abstractions.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/Microsoft.Extensions.Logging.Abstractions.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/Microsoft.Extensions.Options.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/Microsoft.Extensions.Primitives.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/Microsoft.FileFormats.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/Microsoft.SymbolStore.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/SOS.Extensions.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/SOS.Hosting.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/SOS.InstallHelper.dll %{buildroot}%{diagnosticsdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/System.CommandLine.dll %{buildroot}%{diagnosticsdir}

# Tools
for name in counters dump gcdump stack trace; do
  cp -f %{_artifacts}/dotnet-${name}/%{_buildtype}/net*/publish/*.dll %{buildroot}%{diagnosticsdir}
done
for so in `find %{buildroot}%{diagnosticsdir}/%{rid} -type f -name "*.so" -exec basename {} \;`; do
  ln -sf %{rid}/${so} %{buildroot}%{diagnosticsdir}
done
# put sosdocsunix.txt close to libsos.so copy (need for `help command`)
cp -f %{buildroot}%{diagnosticsdir}/%{rid}/sosdocsunix.txt %{buildroot}%{diagnosticsdir}

# remove CoreCLR system DLLs
rm -f %{buildroot}%{diagnosticsdir}/System.Collections.Immutable.dll
rm -f %{buildroot}%{diagnosticsdir}/System.Reflection.Metadata.dll
rm -f %{buildroot}%{diagnosticsdir}/System.Runtime.CompilerServices.Unsafe.dll
rm -f %{buildroot}%{diagnosticsdir}/System.Diagnostics.DiagnosticSource.dll

touch %{buildroot}%{diagnosticsdir}/version-%{version}-%{release}

# dbgshim
mkdir -p %{buildroot}%{dbgshimdir}
cp %{_artifacts}/linux.%{_barch}.%{_buildtype}/libdbgshim.so %{buildroot}%{dbgshimdir}


%files
%manifest %{name}.manifest
%{diagnosticsdir}/*

%files -n coreclr-dbgshim
%manifest %{name}.manifest
%{dbgshimdir}/libdbgshim.so
