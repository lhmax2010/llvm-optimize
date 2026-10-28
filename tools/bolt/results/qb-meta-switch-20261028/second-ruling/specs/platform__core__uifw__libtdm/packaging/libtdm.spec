%define HALTESTS_PACKAGE 1
%define HALTESTS_GCOV    0

Name:           libtdm
Version:        3.4.0
Release:        0
Summary:        User Library of Tizen Display Manager
Group:          Development/Libraries
License:        MIT
Source0:        %{name}-%{version}.tar.gz
Source1001:	    %{name}.manifest
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(ttrace)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(hal-api-tdm)
BuildRequires:  gtest-devel 

%description
Common user library of Tizen Display Manager : libtdm front-end library

%package devel
Summary:        Devel of Tizen Display Manager Library
Group:          Development/Libraries
Requires:       libtdm = %{version}
Requires:       pkgconfig(libtbm)

%description devel
This supports frontend & backend library header and so

%package client
Summary:        Client library for Tizen Display Manager
Group:          Development/Libraries
Requires:       libtdm = %{version}

%description client
Tizen Display Manager Client Library

%package client-devel
Summary:        Client library for Tizen Display Manager
Group:          Development/Libraries
Requires:       libtdm-client = %{version}
Requires:       libtdm-devel

%description client-devel
Tizen Display Manager Client Library headers

%if "%{HALTESTS_PACKAGE}" == "1"
%package haltests
Summary: Tizen Display Manager unit tests package
Group: Development/Libraries

%description haltests
Test module for testing libtdm APIs
%endif

%global TZ_SYS_RO_SHARE  %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:/usr/share}

%package tools
Summary:        Tools for libtdm
Group:          Development/Utilities
Requires:       libtdm = %{version}

%description tools
This contains libtdm tools for fundamental testing

%prep
%setup -q
cp %{SOURCE1001} .

%build
HALTESTS="no"

%if "%{HALTESTS_PACKAGE}" == "1"
HALTESTS="yes"
%endif

%if "%{HALTESTS_GCOV}" == "1"
CFLAGS+=" -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV"
CXXFLAGS+=" -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV"
LDFLAGS+=" -lgcov"
%endif

%reconfigure --disable-static --with-haltests=${HALTESTS} --bindir=%{_bindir}/hal \
             --with-default-dlog=yes \
             --with-tdm-data-path=%{TZ_SYS_RO_SHARE}/tdm \
             CFLAGS="${CFLAGS} -Wall -Werror" \
             CXXFLAGS="${CXXFLAGS} -Wall -Werror" \
             LDFLAGS="${LDFLAGS} -Wl,--hash-style=both -Wl,--as-needed"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%__mkdir_p %{buildroot}%{_unitdir_user}
install -m 644 service/tdm-socket-user.service %{buildroot}%{_unitdir_user}
install -m 644 service/tdm-socket-user.path %{buildroot}%{_unitdir_user}

%remove_docs


%pre
%__mkdir_p %{_unitdir_user}/basic.target.wants
ln -sf ../tdm-socket-user.path %{_unitdir_user}/basic.target.wants/

%post
%if "%{HALTESTS_PACKAGE}" == "1"
if [ -f %{_bindir}/tdm-haltests ]; then
    rm -f %{_bindir}/tdm-haltests
fi
ln -s %{_bindir}/hal/tdm-haltests %{_bindir}/tdm-haltests
%endif
if [ -f %{_bindir}/tdm-monitor ]; then
    rm -f %{_bindir}/tdm-monitor
fi
ln -s %{_bindir}/hal/tdm-monitor %{_bindir}/tdm-monitor

if [ -f %{_bindir}/tdm-test-client ]; then
    rm -f %{_bindir}/tdm-test-client
fi
ln -s %{_bindir}/hal/tdm-test-client %{_bindir}/tdm-test-client

if [ -f %{_bindir}/tdm-test-server ]; then
    rm -f %{_bindir}/tdm-test-server
fi
ln -s %{_bindir}/hal/tdm-test-server %{_bindir}/tdm-test-server

%postun -p /sbin/ldconfig
rm -f %{_unitdir_user}/basic.target.wants/tdm-socket-user.path

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libtdm.so.*
%{_libdir}/tdm/libtdm-dummy.so
%{_libdir}/tdm/libtdm-virtual.so
%attr(750,root,root) %{_bindir}/hal/tdm-monitor
%{_unitdir_user}/tdm-socket-user.path
%{_unitdir_user}/tdm-socket-user.service

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/tdm.h
%{_includedir}/tdm_common.h
%{_includedir}/tdm_backend.h
%{_includedir}/tdm_helper.h
%{_includedir}/tdm_list.h
%{_includedir}/tdm_log.h
%{_includedir}/tdm_types.h
%{_includedir}/tdm_deprecated.h
%{_libdir}/pkgconfig/libtdm.pc
%{_libdir}/libtdm.so

%files client
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libtdm-client.so.*

%files client-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/tdm_client.h
%{_includedir}/tdm_client_types.h
%{_libdir}/pkgconfig/libtdm-client.pc
%{_libdir}/libtdm-client.so

%files tools
%manifest %{name}.manifest
%attr(750,root,root) %{_bindir}/hal/tdm-test-server
%{_bindir}/hal/tdm-test-client

%if "%{HALTESTS_PACKAGE}" == "1"
%files haltests
%defattr(-,root,root,-)
%{_bindir}/hal/tdm-haltests
%endif

%changelog
