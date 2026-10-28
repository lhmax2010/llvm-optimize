%bcond_with tizen
%if %{with tizen}
%define     _extra_make_flags           WITH_TIZEN=yes
%define     _fw_archive_prefix          firmware_ma2450
%define     _fw_version                 784
%endif

Name:       libmvnc
Summary:    Intel®  Movidius™  Neural Compute software developer kit
Version:    2.10.01.01
Release:    0
Group:      Development/Libraries
Packager:   Wook Song <wook16.song@samsung.com>
License:    Apache-2.0 and BSD-3-Clause and MIT
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source1001: LICENSE.BSD-3-Clause
Source1002: LICENSE.MIT
Patch0:     0001-API-Makefile-Revise-Makefile-for-API.patch
Patch1:     0002-API-Makefile-Generalize-Makefile.patch
Patch2:     0003-API-Makefile-Modifies-Makefile-to-generate-libmvnc.p.patch
Patch3:     0004-API-Makefile-Add-flag-to-skip-.-get_mvcmd.sh-when-it.patch
Patch4:     0005-API-XLinkConsole-Add-a-missing-header-include.patch
Requires(post): %{_sbindir}/udevadm %{_sbindir}/ldconfig
Requires(postun): %{_sbindir}/udevadm %{_sbindir}/ldconfig
Requires: mvnc-2450-firmware

BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  unzip

%description
This Intel® Movidius™ Neural Compute software developer kit (NCSDK) is
the legacy SDK provided for users of the Intel® Movidius™ Neural Compute Stick
(Intel® Movidius™ NCS). New users of this device as well as all users of the newer
Intel® Neural Compute Stick 2 should install the OpenVINO™ Toolkit.

%package devel
License: Apache-2.0
Summary: Development package to use NCSDK
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package provides headers and other miscellaneous files required to use NCSDK.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
cp %{SOURCE1} .
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
pushd api/src
%{__make} %{?_smp_mflags} %{?_extra_make_flags}
popd

%install
pushd api/src
%{__make} \
    DESTDIR=%{?buildroot:%{buildroot}} \
    PREFIX=%{_prefix} \
    INSTALLDIR=%{?buildroot:%{buildroot}}%{_prefix} \
    LIBDIR_NAME=%{_lib} \
    %{?_extra_make_flags} \
    basicinstall
rm %{buildroot}%{_libdir}/*.so
popd

%post
%{_sbindir}/udevadm control --reload-rules
%{_sbindir}/udevadm trigger
%{_sbindir}/ldconfig

%postun
%{_sbindir}/udevadm control --reload-rules
%{_sbindir}/udevadm trigger
%{_sbindir}/ldconfig

%post devel
cd %{_libdir} && ln -sf %{name}.so.0 %{name}.so
%{_sbindir}/ldconfig

%postun devel
rm -f %{_libdir}/%{name}.so
%{_sbindir}/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%license LICENSE.BSD-3-Clause
%license LICENSE.MIT
%{_libdir}/libmvnc.so.*
/etc/udev/rules.d/*

%files devel
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
