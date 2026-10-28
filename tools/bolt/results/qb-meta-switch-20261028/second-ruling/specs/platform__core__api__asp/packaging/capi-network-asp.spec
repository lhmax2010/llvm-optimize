%define file_transfer_test no

Name:       capi-network-asp
Summary:    An Application Service Platform(ASP) libraries in Native API
Version:    0.1.23
Release:    1
Group:      Network & Connectivity/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
%if "%{file_transfer_test}" == "yes"
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(gssdp-1.0)
BuildRequires:  pkgconfig(gupnp-1.0)
%endif
BuildRequires:  pkgconfig(gmock)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Application Service Platform(ASP) library in Tizen C API

%package devel
Summary:  An Application Service Platform(ASP) in Native API (Development)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires: capi-base-common-devel

%description devel
An Application Service Platform(ASP) library in Tizen CAPI (Shared Library) (Development)

%package test
Summary:    ASP - ASP test binaries

%description test
Test Application for Application Service Platform(ASP)

%prep
%setup -q
chmod 644 %{SOURCE0}

%ifarch %{arm}
export ARCH=arm
%else
export ARCH=i586
%endif

%build

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
%if "%{file_transfer_test}" == "yes"
        -DTZ_SYS_RO_ETC=%{TZ_SYS_RO_ETC} \
        -DFILE_TRANSFER_TEST=1 \
%endif
%if 0%{?gtests:1}
		-DBUILD_GTESTS=ON \
%endif
        -DCMAKE_BUILD_TYPE=%{?build_type} \
        -DCMAKE_VERBOSE_MAKEFILE=ON \
        -DLIB_DIR:PATH=%{_libdir} \
        -DBIN_DIR:PATH=%{_bindir} \
        -DINCLUDE_DIR:PATH=%{_includedir} \
        -DLOCAL_STATE_DIR:PATH=%{_localstatedir} \
        -DDATA_ROOT_DIR:PATH=%{_datadir} \
        -DFULLVER=%{version} \
        -DMAJORVER=${MAJORVER}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest capi-network-asp.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/asp/*.h
%{_libdir}/*.so

%files test
%manifest asp-test.manifest
%attr(755,root,root) %{_bindir}/asp-test
%if 0%{?gtests:1}
%attr(755,root,root) %{_bindir}/asp-gtest
%endif
