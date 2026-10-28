Name:           wgt-backend
Summary:        Application installer backend for WGT
Version:        0.18.9
Release:        1
Group:          Application Framework/Package Management
License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz

Source1000:     wgt-backend.manifest
Source1001:     wgt-installer.manifest
Source1002:     wgt-installer-tests.manifest

Requires:       wgt-installer = %{version}
BuildRequires:  cmake
BuildRequires:  app-installers-tests
BuildRequires:  pkgconfig(app-installers)
BuildRequires:  pkgconfig(manifest-parser)
BuildRequires:  pkgconfig(wgt-manifest-handlers)
BuildRequires:  pkgconfig(pkgmgr-installer)
BuildRequires:  pkgconfig(pkgmgr-types)
BuildRequires:  pkgconfig(libwebappenc)
BuildRequires:  pkgconfig(tpk-installer)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(libgum)
BuildRequires:  pkgconfig(gmock)

%description
This is a package that installs the WGT backend of pkgmgr.

%package -n wgt-installer
Summary: Wgt-installer library
Group:   Application Framework/Package Management

%description -n wgt-installer
This package contains wgt-installer library

%package -n wgt-installer-devel
Summary:  Wgt-installer development files
Group:    Application Framework/Package Management
Requires: wgt-installer = %{version}

%description -n wgt-installer-devel
This package contains header files of wgt-installer library

%package -n wgt-installer-tests
Summary: Unit tests for wgt-installer
Requires: wgt-installer = %{version}

%description -n wgt-installer-tests
Unit tests for wgt-installer

%prep
%setup -q

cp %{SOURCE1000} .
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
%ifnarch x86_64 aarch64
ISARC64=0
%else
ISARC64=1
%endif
%cmake . -DCMAKE_BUILD_TYPE=%{?build_type:%build_type} \
         -DISARC64=${ISARC64}
make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}/etc/package-manager/backend
ln -s %{_bindir}/wgt-backend %{buildroot}%{_sysconfdir}/package-manager/backend/wgt

%post -n wgt-installer-tests
/usr/sbin/setcap cap_chown,cap_dac_override,cap_fowner,cap_mac_override=eip %{_bindir}/wgt-installer-ut/smoke-test
/usr/sbin/setcap cap_chown,cap_dac_override,cap_fowner,cap_mac_override=eip %{_bindir}/wgt-installer-ut/smoke-test-helper
/usr/sbin/setcap cap_chown,cap_dac_override,cap_fowner,cap_mac_override=eip %{_bindir}/wgt-installer-ut/hybrid-smoke-test-helper
/usr/sbin/setcap cap_chown,cap_dac_override,cap_fowner,cap_mac_override=eip %{_bindir}/wgt-installer-ut/extensive-smoke-test

%check
export LD_LIBRARY_PATH=../../src/wgt:$LD_LIBRARY_PATH
ctest -V

%files
%manifest wgt-backend.manifest
%license LICENSE
%{_sysconfdir}/package-manager/backend/wgt
%{_bindir}/wgt-backend
%{_datadir}/wgt-backend/default.png

%files -n wgt-installer
%manifest wgt-installer.manifest
%{_sysconfdir}/package-manager/backendlib/libwgt.so
%{_libdir}/libwgt-installer.so*
%{_libdir}/libhybrid-installer.so*

%files -n wgt-installer-devel
%{_includedir}/app-installers/wgt/*.h
%{_includedir}/app-installers/wgt/*/*.h
%{_includedir}/app-installers/wgt/*/*/*.h
%{_includedir}/app-installers/hybrid/*.h
%{_includedir}/app-installers/hybrid/*/*/*.h
%{_libdir}/pkgconfig/wgt-installer.pc

%files -n wgt-installer-tests
%manifest wgt-installer-tests.manifest
%{_bindir}/wgt-installer-ut/*
%{_bindir}/wgt-backend-unit-test
%ifnarch x86_64 aarch64
%{_datadir}/wgt-installer-ut/*
%endif
%{_libdir}/libwgt-smoke-utils.so*
%{_includedir}/app-installers/smoke_tests/wgt_smoke_utils.h

%changelog
* Thu Dec 18 2015 Pawel Sikorski <p.sikorski@samsung.com> 0.1-1
- initial files creation
