Name:		ttrace
Summary:    T-trace for tizen
Version:	1.1.0
Release:    1
Group:      System/Libraries
License:    Apache-2.0 and BSD-3-Clause
Source0:    %{name}-%{version}.tar.gz
SOURCE100:	packaging/ttrace.conf
SOURCE101:	packaging/sys-kernel-debug-tracing.mount
SOURCE102:	packaging/ttrace-marker.service
SOURCE103:	packaging/atrace-bootup.sh

BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(libsmack)
BuildRequires: pkgconfig(gmock)
BuildRequires: cmake

%if 0%{?gcov:1}
BuildRequires: lcov
%endif

%define keepstatic 1

# tizen_profile_name is for optional features that are not built in Tizen Public OBS.
%define TTRACE_PROFILE none
%if "%{?tizen_profile_name}" == "mobile"
%define TTRACE_PROFILE mobile
%else
%if "%{?tizen_profile_name}" == "tv"
%define TTRACE_PROFILE tv
%else
%if "%{?tizen_profile_name}" == "wearable"
%define TTRACE_PROFILE wearable
%endif
%endif
%endif

%define TTRACE_TIZEN_VERSION_MAJOR 2
%if 0%{?tizen_version_major} >= 3
%define TTRACE_TIZEN_VERSION_MAJOR 3
%endif

%define ATRACE_VERSION 1.1
%define ATRACE_HELPER_VERSION 1.0

%description
T-trace library

%package devel
Summary:    T-trace for tizen
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
T-trace library devel

%if 0%{?gcov:1}
%package gcov
Summary:  ttrace(gcov)
Group:    Development/Libraries
%description gcov
New T-trace library cov objects
%endif

%package unittests
Summary:	T-trace unittests binary

%description unittests
T-trace unittests binary

%prep
%setup -q

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

export CFLAGS="$CFLAGS -g -Wall -std=gnu99"
export CXXFLAGS="$CXXFLAGS -std=c++14 -fPIE -pie"

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIBDIR=%{_libdir} -DINCLUDEDIR=%{_includedir} \
      -DTTRACE_PROFILE=%{TTRACE_PROFILE} -DTTRACE_TIZEN_VERSION_MAJOR=%{TTRACE_TIZEN_VERSION_MAJOR} \
      -DMAJORVER=${MAJORVER} -DFULLVER=%{version} \
      -DATRACE_VERSION=%{ATRACE_VERSION} -DATRACE_HELPER_VERSION=%{ATRACE_HELPER_VERSION}
make %{?jobs:-j%jobs}

%check
(cd test && LD_LIBRARY_PATH=../src ctest -V)
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch --ignore-errors graph --no-external -q -d . -o ttrace.info
genhtml ttrace.info -o ttrace.out
%endif

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/usr/lib/tmpfiles.d
install -m 0644 %{SOURCE100} %{buildroot}/usr/lib/tmpfiles.d/ttrace.conf
install -m 0644 %{SOURCE101} %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE102} %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_bindir}
cp %{SOURCE103} %{buildroot}%{_bindir}
%install_service sysinit.target.wants ttrace-marker.service
%install_service sysinit.target.wants sys-kernel-debug-tracing.mount

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name 'atrace.cpp.gcno' -exec rm {} \;
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

cat << EOF > run-unittest.sh
#!/bin/bash
setup() {
	echo "setup start"
}

test_main() {
	echo "test_main start"
	/usr/bin/ttrace-unit-test
}

teardown() {
	echo "teardown start"
}

main() {
	setup
	test_main
	teardown
}

main "\$*"
EOF

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest ttrace.manifest
%defattr(-,root,root,-)
%{_libdir}/libttrace.so.*
%{_unitdir}/ttrace-marker.service
%{_unitdir}/sys-kernel-debug-tracing.mount
%attr(755,root,users) %{_bindir}/atrace
%attr(755,root,users) %{_bindir}/atrace-%{ATRACE_VERSION}
%attr(755,root,users) %{_bindir}/atrace-helper
%attr(755,root,users) %{_bindir}/atrace-helper-%{ATRACE_HELPER_VERSION}
%{_unitdir}/sysinit.target.wants/ttrace-marker.service
%{_unitdir}/sysinit.target.wants/sys-kernel-debug-tracing.mount
%attr(755,root,root) %{_bindir}/atrace-bootup.sh
/usr/lib/tmpfiles.d/ttrace.conf
%license LICENSE

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/libttrace.so
%{_libdir}/pkgconfig/*.pc

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files unittests
%{_bindir}/ttrace-unit-test
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
