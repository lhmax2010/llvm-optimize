Name: hal-backend-security-auth
Summary: Security Auth backend library
Version: 1.0.0
Release: 0
Group: Security/Development
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1001: hal-backend-security-auth.manifest
BuildRequires: cmake
BuildRequires: pkgconfig(hal-rootstrap)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Security Auth backend library

%global rw_data_dir %{?TZ_SYS_DATA:%TZ_SYS_DATA/%name}%{!?TZ_SYS_DATA:/opt/data/auth-fw}

%prep
%setup -q
cp -a %{SOURCE1001} .

%build
%ifarch x86_64
ARCH_FLAG=x86_64
%endif
%ifarch armv7l
ARCH_FLAG=armv7l
%endif
%ifarch aarch64
ARCH_FLAG=aarch64
%endif
%ifarch riscv64
ARCH_FLAG=riscv64
%endif

%cmake ./ -DHAL_LIB_DIR=%{_hal_libdir} \
        -DRW_DATA_DIR:PATH=%{rw_data_dir} \
        -DARCH=${ARCH_FLAG} \
        -DCMAKE_BUILD_TYPE=%{?build_type:%build_type}%{!?build_type:Release}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}/hal/share/licenses/%{name}
cp -a LICENSE %{buildroot}/hal/share/licenses/%{name}/LICENSE

%files
%manifest hal-backend-security-auth.manifest
%{_hal_licensedir}/%{name}/LICENSE
%{_hal_libdir}/lib%{name}.so*
