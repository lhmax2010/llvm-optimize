%{!?buildtype: %define buildtype RelWithDebInfo}

Name:       heaptrack
Summary:    heaptrack for dotnet apps
# Version corresponds to CMake @HEAPTRACK_VERSION_MAJOR@.@HEAPTRACK_VERSION_MINOR@.@HEAPTRACK_VERSION_PATCH@-@HEAPTRACK_VERSION_SUFFIX@
Version:    1.4.5
Release:    1
Group:      Application Framework/Application State Management
License:    GPL
Source0:    %{name}-%{version}.tar.gz
Source1001: heaptrack.manifest
%define	heaptrack_src heaptrack-%{version}
%define	heaptrack_build build-%{_target_platform}
AutoReqProv: no

ExcludeArch: armv7hl

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: clang
BuildRequires: glibc-devel
BuildRequires: libdw-devel
BuildRequires: libunwind-devel
BuildRequires: boost-devel
BuildRequires: boost-iostreams
BuildRequires: boost-program-options
BuildRequires: pkgconfig(zlib)
BuildRequires: coreclr-devel

# .NET Core Runtime
%define dotnettizendir  dotnet.tizen
%define netcoreappdir   %{dotnettizendir}/netcoreapp

%define sdk_install_prefix /home/owner/share/tmp/sdk_tools/%{name}

%description
Heaptrack for Tizen applications

%prep
%setup -q
cp %{SOURCE1001} .

%build

echo _target _target_cpu _target_arch _target_os _target_platform
echo %{_target}
echo %{_target_cpu}
echo %{_target_arch}
echo %{_target_os}
echo %{_target_platform}

%ifarch %{ix86}
export CFLAGS=$(echo $CFLAGS | sed -e 's/-mstackrealign//')
export CXXFLAGS=$(echo $CXXFLAGS | sed -e 's/-mstackrealign//')
%endif

%if "%{?buildtype}" == "Debug"
export CFLAGS=$(echo $CFLAGS | sed -e 's/-O2//' | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//')
export CXXFLAGS=$(echo $CXXFLAGS | sed -e 's/-O2//' | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//')
%endif

%define _coreclr_devel_directory %{_datarootdir}/%{netcoreappdir}

mkdir build
cd build
cmake \
  -DCMAKE_INSTALL_PREFIX=install \
  -DCMAKE_BUILD_TYPE=%{buildtype} \
  -DHEAPTRACK_BUILD_GUI=OFF \
  -DTIZEN=ON \
  ..

make %{?jobs:-j%jobs} VERBOSE=1

%ifarch %{arm}
%define arch_dir armel
%endif

%ifarch aarch64
%define arch_dir arm64
%endif

%ifarch x86_64
%define arch_dir amd64
%endif

%ifarch %{ix86}
%define arch_dir x86
%endif

%ifarch riscv64
%define arch_dir riscv64
%endif

export ENV_GCC_LIB_PATH=`gcc -print-file-name=`

export CFLAGS="--target=%{_host}"
export CXXFLAGS="--target=%{_host}"

cd ../profiler
ROOTFS_DIR=/ \
CC=clang CXX=clang++ \
cmake \
  -DCMAKE_INSTALL_PREFIX=../build/install \
  -DCMAKE_BUILD_TYPE=%{buildtype} \
  -DCMAKE_TOOLCHAIN_FILE=profiler/cross/%{arch_dir}/toolchain.cmake \
  -DCLR_BIN_DIR=%{_coreclr_devel_directory} \
  -DCLR_SRC_DIR=%{_coreclr_devel_directory} \
  -DCLR_ARCH=%{_target_cpu} \
  profiler
make %{?jobs:-j%jobs} VERBOSE=1
cd -

%install
cd build
make install
make -C ../profiler install
mkdir -p %{buildroot}%{sdk_install_prefix}
cp install/lib/heaptrack/*.so %{buildroot}%{sdk_install_prefix}
cp install/lib/heaptrack/libexec/* %{buildroot}%{sdk_install_prefix}
touch %{buildroot}%{sdk_install_prefix}/version-%{version}-%{release}

%files
%manifest heaptrack.manifest
%{sdk_install_prefix}/*
