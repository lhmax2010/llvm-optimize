Name:       capi-network-wifi-aware
Summary:    An Wi-Fi Aware libraries in Native API
Version:    0.2.0
Release:    1
Group:      Network & Connectivity/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:	%{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:	pkgconfig(gmock)
%if 0%{?gcov:1}
BuildRequires:  gtest-devel
BuildRequires:	lcov
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Wi-Fi Aware library in Tizen C API

%package devel
Summary:  Wi-Fi Aware in Native API (Development)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires: capi-base-common-devel

%description devel
An Wi-Fi Aware library in Tizen CAPI (Shared Library) (Development)

%package test
Summary:    Wi-Fi Aware - Wi-Fi Aware test binaries

%description test
Test Application for Wi-Fi Aware

%package cts-verifier
summary:	cts-verifier command app

%description cts-verifier
cts-verifier command app

%if 0%{?gcov:1}
%package gcov
Summary:	Coverage Data of %{name}

%description gcov
The %{name}-gcov package contains gcov objects

%package unittests
Summary:    %{name} unittests binary

%description unittests
unittests binary
%endif

%prep
%setup -q
chmod 644 %{SOURCE0}
cp %{SOURCE1} ./%{name}.manifest

%ifarch %{arm}
export ARCH=arm
%else
export ARCH=i586
%endif

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage -DBUILD_GCOV"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage -DBUILD_GCOV"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
%endif

%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
%endif


MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
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

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' ! -path '*/cts-verifier/*' ! -path '*/nan-test/*' -exec cp --parents '{}' "$gcno_obj_dir" ';'

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/wifi-aware-unittest
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
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}/
%endif

%check
%if 0%{?gcov:1}
export LD_LIBRARY_PATH=./src/:./tests/unittest/mocks/
LD_PRELOAD=./tests/unittest/mocks/libwifi-aware-mock.so ./tests/unittest/wifi-aware-unittest
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/network/*.h
%{_libdir}/*.so

%files test
%manifest %{name}.manifest
%attr(755,root,root) %{_bindir}/wifi-aware-test
%attr(755,root,root) %{_bindir}/wifi-aware-publish-test
%attr(755,root,root) %{_bindir}/wifi-aware-subscribe-test
%attr(755,root,root) %{_bindir}/wifi-aware-publish-matching-filter-test
%attr(755,root,root) %{_bindir}/wifi-aware-subscribe-matching-filter-test

%files cts-verifier
%attr(755,root,root) %{_bindir}/cts-verifier

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*

%files unittests
%{_bindir}/wifi-aware-unittest
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
%endif
