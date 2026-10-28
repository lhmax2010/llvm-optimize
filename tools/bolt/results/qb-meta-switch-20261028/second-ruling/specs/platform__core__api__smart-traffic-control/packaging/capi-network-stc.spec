Name:       capi-network-stc
Summary:    A Smart Traffic Control (STC) libraries in Native API
Version:    0.0.43
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
BuildRequires: gtest-devel
%if 0%{?gcov:1}
BuildRequires: lcov
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Smart Traffic Control (STC) library in Tizen C API

%package devel
Summary:  An Smart Traffic Control (STC) in Native API (Development)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires: capi-base-common-devel

%description devel
An Smart Traffic Control (STC) library in Tizen CAPI (Shared Library) (Development)

%package test
Summary:    STC - STC test binaries

%description test
Test Application for Smart Traffic Control (STC)

%if 0%{?gcov:1}
%package gcov
Summary:  STC library(gcov)
Group:    Network/Testing
%description gcov
gcov objects for coverage test
%endif

%package unittests
Summary: %{name} unittests binary

%description unittests
unittests binary

%prep
%setup -q
chmod 644 %{SOURCE0}

%ifarch %{arm}
export ARCH=arm
%else
export ARCH=i586
%endif

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
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
		-DDEBUG_GCOV=%{?debug_gcov:1}%{!?debug_gcov:0} \
		-DBUILD_ASAN=%{?asan:1} \
        -DMAJORVER=${MAJORVER}
make %{?jobs:-j%jobs}

%if 0%{?gcov:1}
mkdir -p gcov-obj
find . -name '*.gcno' -exec cp '{}' gcov-obj ';'
%endif

%install
rm -rf %{buildroot}
%make_install
%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' ! -path '*/test/*' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%if 0%{?asan} != 1
cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/tct-stc-core
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
pushd unittest
./run_coverage.sh
popd
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest capi-network-stc.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_bindir}/stc_test
%attr(755,root,root) %{_bindir}/stc_test


%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/network/*.h
%{_libdir}/*.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%exclude %{_datadir}/gcov/obj/*/*/unittest/*
%endif

%if 0%{?asan} != 1
%files unittests
%{_bindir}/tct-stc-core
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
%endif
