Name:           tpk-backend
Summary:        Application installer backend for TPK
Version:        1.11.6
Release:        1
Group:          Application Framework/Package Management
License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz
Source1000:     tpk-backend.manifest
Source1001:     tpk-installer.manifest
Source1002:     tpk-installer-tests.manifest

Requires:       tpk-installer = %{version}
BuildRequires:  cmake
BuildRequires:  app-installers-tests
BuildRequires:  pkgconfig(app-installers)
BuildRequires:  pkgconfig(manifest-parser)
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(pkgmgr-parser)
BuildRequires:  pkgconfig(pkgmgr-types)
BuildRequires:  pkgconfig(tpk-manifest-handlers)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(ttrace)
BuildRequires:  pkgconfig(libgum)
BuildRequires:  pkgconfig(gmock)

%description
Backend for tizen package files

%package -n tpk-installer
Summary:    Tpk-installer library
Group:      Application Framework/Package Management

%description -n tpk-installer
This package contains tpk-installer library

#%package -n tpk-installer-devel
%package devel
Summary:    Tpk-installer development files
Group:      Application Framework/Package Management
Requires:   tpk-installer = %{version}

#%description -n tpk-installer-devel
%description devel
This package contains header files of tpk-installer library

%package -n tpk-installer-tests
Summary: Unit tests for tpk-installer
Requires: tpk-installer = %{version}

%description -n tpk-installer-tests
Unit tests for tpk-installer

%prep
%setup -q

cp %{SOURCE1000} .
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%ifnarch x86_64 aarch64
ISARC64=0
%else
ISARC64=1
%endif
%cmake . -DCMAKE_BUILD_TYPE=%{?build_type:%build_type} \
         -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
         -DISARC64=${ISARC64}

make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}/etc/package-manager/backend
ln -s %{_bindir}/tpk-backend %{buildroot}%{_sysconfdir}/package-manager/backend/tpk
ln -s %{_bindir}/tpk-backend %{buildroot}%{_sysconfdir}/package-manager/backend/rpm

%post -n tpk-installer-tests
/usr/sbin/setcap cap_chown,cap_dac_override,cap_fowner,cap_mac_override=eip %{_bindir}/tpk-installer-ut/smoke-test
/usr/sbin/setcap cap_chown,cap_dac_override,cap_fowner,cap_mac_override=eip %{_bindir}/tpk-installer-ut/smoke-test-helper
/usr/sbin/setcap cap_chown,cap_dac_override,cap_fowner,cap_mac_override=eip %{_bindir}/tpk-installer-ut/recovery-test
/usr/sbin/setcap cap_chown,cap_dac_override,cap_fowner,cap_mac_override=eip %{_bindir}/tpk-installer-ut/extensive-smoke-test

%check
export LD_LIBRARY_PATH=../../src/tpk:$LD_LIBRARY_PATH
ctest -V

%files
%{_sysconfdir}/package-manager/backend/tpk
%{_sysconfdir}/package-manager/backend/rpm
%license LICENSE
%manifest tpk-backend.manifest
%{_bindir}/tpk-backend

%files -n tpk-installer
%manifest tpk-installer.manifest
%{_sysconfdir}/package-manager/backendlib/libtpk.so
%{_libdir}/libtpk-installer.so*

#%files -n tpk-installer-devel
%files devel
%{_includedir}/app-installers/tpk/*.h
%{_includedir}/app-installers/tpk/*/*/*.h
%{_libdir}/pkgconfig/tpk-installer.pc

%files -n tpk-installer-tests
%manifest tpk-installer-tests.manifest
%{_bindir}/tpk-installer-ut/*
%{_bindir}/tpk-backend-unit-test
%ifnarch x86_64 aarch64
%{_datadir}/tpk-installer-ut/*
%endif
%{_libdir}/libtpk-smoke-utils.so*
%{_includedir}/app-installers/smoke_tests/tpk_smoke_utils.h

%changelog
* Thu Dec 18 2015 Pawel Sikorski <p.sikorski@samsung.com> 0.1-1
- initial files creation
