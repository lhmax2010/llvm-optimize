%define UTEST_PACKAGE 1
%define UTEST_GCOV    0

Name:		libwayland-tbm
Version:	0.9.0
Release:	0
Summary:	Wayland TBM Protocol
License:	MIT
Group:		Graphics & UI Framework/Wayland Window System
URL:		http://www.tizen.org/

Source: %name-%version.tar.gz
Source1001:	%name.manifest
BuildRequires:  autoconf automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  gtest-devel

%description
Wayland TBM Protocol for TIZEN

# libwayland-tbm-server package
%package -n libwayland-tbm-server
Group:		Graphics & UI Framework/Wayland Window System
Summary:	Wayland TBM server library

%description -n libwayland-tbm-server
Wayland tbm is a protocol for graphics memory management for TIZEN

# libwayland-tbm-client package
%package -n libwayland-tbm-client
Group:		Graphics & UI Framework/Wayland Window System
Summary:	Wayland TBM client library

%description -n libwayland-tbm-client
Wayland tbm is a protocol for graphics memory management for TIZEN

# libwayland-tbm devel package
%package devel
Summary:    Development header files
Group:		Graphics & UI Framework/Development
Requires:	libwayland-tbm-server = %version
Requires:	libwayland-tbm-client = %version
Requires:   pkgconfig(libtbm)

%description devel
Development header files for use with Wayland protocol

%if "%{UTEST_PACKAGE}" == "1"
%package unittests
Summary:    Wayland TBM unit test package
Group:		Graphics & UI Framework/Wayland Window System
%description unittests
Test module for testing wayland-tbm APIs
%endif

%global TZ_SYS_RO_SHARE  %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:/usr/share}

%prep
%setup -q
cp %{SOURCE1001} .

%build
UTEST="no"

%if "%{UTEST_PACKAGE}" == "1"
UTEST="yes"
%endif

%if "%{UTEST_GCOV}" == "1"
CFLAGS+=" -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV"
CXXFLAGS+=" -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV"
LDFLAGS+=" -lgcov"
%endif

%reconfigure --with-unittests=${UTEST} \
            --with-default-dlog=yes \
             CFLAGS="${CFLAGS} -Wall -Werror" \
             CXXFLAGS="${CXXFLAGS} -Wall -Werror" \
             LIBDIR=%{_libdir} \
             LDFLAGS="${LDFLAGS} -Wl,--hash-style=both -Wl,--as-needed"

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%post -n libwayland-tbm-client -p /sbin/ldconfig
%postun -n libwayland-tbm-client -p /sbin/ldconfig

%post -n libwayland-tbm-server -p /sbin/ldconfig
%postun -n libwayland-tbm-server -p /sbin/ldconfig

%files -n libwayland-tbm-server
%defattr(-,root,root)
%manifest %{name}.manifest
%license COPYING
%_libdir/libwayland-tbm-server.so.0*

%files -n libwayland-tbm-client
%defattr(-,root,root)
%manifest %{name}.manifest
%license COPYING
%_libdir/libwayland-tbm-client.so.0*
%{_bindir}/wayland-tbm-monitor

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%_includedir/wayland-tbm*.h
%_libdir/libwayland-tbm*.so
%_libdir/pkgconfig/wayland-tbm*.pc
%doc README TODO

%if "%{UTEST_PACKAGE}" == "1"
%files unittests
%defattr(-,root,root,-)
%{_bindir}/wayland-tbm-unittests
%endif

%changelog
