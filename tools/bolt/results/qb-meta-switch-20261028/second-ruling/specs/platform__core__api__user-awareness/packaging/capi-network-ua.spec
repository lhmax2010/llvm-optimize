Name: capi-network-ua
Summary: User Awareness Framework CAPI
Version: 0.14.6
Release: 2
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(ua-api)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  gtest-devel
%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%if 0%{?ptest:1}
BuildRequires:  pkgconfig(deviced)
BuildRequires:  pkgconfig(power-defs)
%endif

%define _confdir /opt/data

%description
Activity API Library

%package devel
Summary: User Awareness Framework CAPI (devel)
Requires: %{name} = %{version}

%description devel
User Awareness Framework CAPI

%package test
Summary: User Awareness Framework test application
Group:   TO_BE/FILLED
Requires: %{name} = %{version}-%{release}

%description test
This package is for User Awareness Framework CAPI test application

%if 0%{?gcov:1}
%package gcov
Summary:    A User Awareness gcov Tool
Group:      Network & Connectivity/Development

%description gcov
User Awareness gcov objects
%endif

%prep
%setup -q

%build

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DBIN_INSTALL_DIR=%{_bindir} \
	-DINCLUDE_INSTALL_DIR=%{_includedir} \
	-DLIB_PATH=%{_lib} \
	-DSUSPEND_RESUME_TEST=%{?ptest:1}%{!?ptest:0} \
	-DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0} \
	-DBUILD_ASAN=%{?asan:1}

make %{?jobs:-j%jobs}

%install
%make_install

%if 0%{?gcov:1}
find .. -name '*.gcno' -printf '%%P\n' | tar cf %{name}-gcov.tar -C .. -T -
install -d -m 755 %{buildroot}%{_datadir}/gcov/obj
tar xf %{name}-gcov.tar -C %{buildroot}%{_datadir}/gcov/obj
%endif

%check
%if 0%{?asan} != 1
LD_LIBRARY_PATH=. LD_PRELOAD=tests/unittest/libuser-awareness-mock.so tests/unittest/tct-user-awareness-core
%endif
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info --exclude "*/unittest/*"
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%attr(644,-,-) %{_libdir}/lib%{name}.so
%attr(644,-,-) %{_libdir}/lib%{name}.so.*

%files devel
%manifest %{name}-devel.manifest
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*

%files test
%manifest %{name}.manifest
%attr(777,network_fw,network_fw) %{_bindir}/ua-test

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
