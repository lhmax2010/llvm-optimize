%{!?buildtype: %define buildtype Release}

Name:      coreprofiler
Summary:   Managed code profiler for CoreCLR
Version:   1.2.1
Release:   1
Group:     Development/Toolchain
License:   MIT
Source0:   %{name}-%{version}.tar.gz
Source1000: coreprofiler.manifest

BuildRequires: cmake
BuildRequires: clang >= 3.8
BuildRequires: clang-devel >= 3.8
BuildRequires: llvm >= 3.8
BuildRequires: llvm-devel >= 3.8
BuildRequires: lldb >= 3.8
BuildRequires: lldb-devel >= 3.8
BuildRequires: libstdc++-devel
BuildRequires: coreclr-devel
# No matter what tizen-release package you use in any profile
AutoReq: 0
Requires: coreclr

# .NET Core Runtime
%define dotnettizendir  dotnet.tizen
%define netcoreappdir   %{dotnettizendir}/netcoreapp

%define sdk_install_prefix /home/owner/share/tmp/sdk_tools/%{name}

%description
This is a CoreCLR profiler for Tizen.

%prep
%setup -q
cp %{SOURCE1000} .

%build

export CFLAGS="--target=%{_host}"
export CXXFLAGS="--target=%{_host}"

%ifarch %{ix86}
export CFLAGS=$(echo $CFLAGS | sed -e 's/--target=i686/--target=i586/')
export CXXFLAGS=$(echo $CXXFLAGS | sed -e 's/--target=i686/--target=i586/')
%endif

%ifarch armv7l
%define _cmake_arch_args -DARM_SOFTFP=1
%endif

mkdir build
cd build
cmake .. \
    -DCMAKE_BUILD_TYPE=%{buildtype} \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
    -DCLR_SRC_DIR=%{_datarootdir}/%{netcoreappdir} \
    -DCLR_BIN_DIR=%{_datarootdir}/%{netcoreappdir} \
    -DCLR_CMAKE_LINUX_ID=tizen \
    %{?_cmake_arch_args}
make %{?jobs:-j%jobs}

%install
cd build
make install
mkdir -p %{buildroot}%{sdk_install_prefix}
cp install/* %{buildroot}%{sdk_install_prefix}
touch %{buildroot}%{sdk_install_prefix}/version-%{version}-%{release}

%files
%manifest coreprofiler.manifest
%{sdk_install_prefix}/*
