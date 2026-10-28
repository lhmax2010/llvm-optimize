%bcond_with x
%bcond_with wayland
%define HALTESTS_PACKAGE 1
%if 0%{?gcov:1}
%define HALTESTS_GCOV    1
%else
%define HALTESTS_GCOV    0
%endif

%define _tmpfilesdir /usr/lib/tmpfiles.d

Name:           libtbm
Version:        4.8.7
Release:        1
License:        MIT and Apache-2.0
Summary:        The library for Tizen Buffer Manager
Group:          System/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001:     %name.manifest
Source1002:     sw_sync.conf
Source1003:     run-unittest.sh

BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(hal-api-tbm)

%description
Description: %{summary}

%package devel
Summary:        Tizen Buffer Manager Library - Development
Group:          Development/Libraries
Requires:       libtbm = %{version}

%description devel
The library for Tizen Buffer Manager.

Development Files.

%if 0%{?gcov:1}
%package gcov
Summary: Tizen Buffer Manager gcov data package
Group: Development/Libraries

%description gcov
Tizen Buffer Manager gcno data for gcov
%endif

%if "%{HALTESTS_PACKAGE}" == "1"
%package haltests
Summary: Tizen Buffer Manager unit tests package
Group: System/Libraries

%description haltests
Test module for testing libtbm APIs

%package unittests
Summary: Tizen Buffer Manager unit tests package
Group: System/Libraries

%description unittests
Test module for testing libtbm APIs
%endif

%global TZ_SYS_RO_SHARE  %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:/usr/share}

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

%if %{with wayland}
%reconfigure --prefix=%{_prefix} --with-tbm-platform=WAYLAND  --with-haltests=${HALTESTS} --bindir=%{_bindir}/hal \
            --with-default-dlog=yes \
            CFLAGS="${CFLAGS} -Wall -Werror" LDFLAGS="${LDFLAGS} -Wl,--hash-style=both -Wl,--as-needed"
%else
%reconfigure --prefix=%{_prefix} --with-tbm-platform=X11  --with-haltests=${HALTESTS} --bindir=%{_bindir}/hal \
            CFLAGS="${CFLAGS} -Wall -Werror" LDFLAGS="${LDFLAGS} -Wl,--hash-style=both -Wl,--as-needed"
%endif

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%__mkdir_p %{buildroot}%{_tmpfilesdir}
install -m 0644 %SOURCE1002 %{buildroot}%{_tmpfilesdir}/sw_sync.conf

%__mkdir_p %{buildroot}%{_unitdir_user}
install -m 644 service/tbm-drm-auth-user.service %{buildroot}%{_unitdir_user}
install -m 644 service/tbm-drm-auth-user.path %{buildroot}%{_unitdir_user}

%if 0%{?gcov:1}
find haltests/ -name '*.gcno' -exec rm {} \;

builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%if "%{HALTESTS_PACKAGE}" == "1"
mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 %SOURCE1003 %{buildroot}%{_bindir}/tizen-unittests/%{name}/
%endif

%clean
rm -rf %{buildroot}

%pre
%__mkdir_p %{_unitdir_user}/basic.target.wants
ln -sf ../tbm-drm-auth-user.path %{_unitdir_user}/basic.target.wants/

%post
%if "%{HALTESTS_PACKAGE}" == "1"
if [ -f %{_bindir}/tbm-haltests ]; then
    rm -f %{_bindir}/tbm-haltests
fi
ln -s %{_bindir}/hal/tbm-haltests %{_bindir}/tbm-haltests

if [ -f %{_bindir}/tbm-unittests ]; then
    rm -f %{_bindir}/tbm-unittests
fi
ln -s %{_bindir}/hal/tbm-unittests %{_bindir}/tbm-unittests
%endif

%postun -p /sbin/ldconfig
rm -f %{_unitdir_user}/basic.target.wants/tbm-drm-auth-user.path

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING COPYING.Apache-2.0
%{_libdir}/libtbm.so.*
%{_unitdir_user}/tbm-drm-auth-user.path
%{_unitdir_user}/tbm-drm-auth-user.service
%{_tmpfilesdir}/sw_sync.conf

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%dir %{_includedir}
%{_includedir}/tbm_*.h
%{_libdir}/libtbm.so
%{_libdir}/pkgconfig/libtbm.pc

%if "%{HALTESTS_PACKAGE}" == "1"
%files haltests
%defattr(-,root,root,-)
%{_bindir}/hal/tbm-haltests

%files unittests
%defattr(-,root,root,-)
%{_bindir}/hal/tbm-unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
%endif

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
